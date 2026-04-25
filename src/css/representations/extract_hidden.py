from __future__ import annotations

import argparse
import gc
import random
import sys
from pathlib import Path
from typing import Any

import numpy as np
import torch
import transformers
from tqdm.auto import tqdm
from transformers import AutoConfig, AutoModel, AutoTokenizer
from transformers.tokenization_utils_base import PreTrainedTokenizerBase

from css.common.config import load_yaml
from css.common.hash_utils import sha256_file, sha256_json
from css.common.io import ensure_dir, read_jsonl
from css.common.text import simple_word_spans
from css.representations.cache_io import save_hidden_cache, write_cache_metadata
from css.representations.pooling import mean_pool


def _safe_name(name: str) -> str:
    return name.replace("/", "__")


def _set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def _device_from_model(model: Any) -> torch.device:
    try:
        return next(model.parameters()).device
    except StopIteration:
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def _max_memory_from_config(cfg: dict[str, Any]) -> dict[int | str, str] | None:
    raw = cfg.get("max_memory")
    if raw is None:
        return None
    if not isinstance(raw, dict):
        raise TypeError("max_memory must be a mapping such as {'0': '14GiB', 'cpu': '64GiB'}")
    parsed: dict[int | str, str] = {}
    for key, value in raw.items():
        parsed[int(key) if str(key).isdigit() else str(key)] = str(value)
    return parsed


def _word_index_map(
    text: str, offsets: list[tuple[int, int]]
) -> tuple[list[str], list[tuple[int, int]], dict[int, int]]:
    words = simple_word_spans(text)
    mapping: dict[int, int] = {}
    for tok_idx, (start, end) in enumerate(offsets):
        if end <= start:
            continue
        best_idx: int | None = None
        best_overlap = 0
        for word_idx, (_, w_start, w_end) in enumerate(words):
            overlap = min(end, w_end) - max(start, w_start)
            if overlap > best_overlap:
                best_overlap = overlap
                best_idx = word_idx
        if best_idx is not None and best_overlap > 0:
            mapping[tok_idx] = best_idx
    return [w for w, _, _ in words], [(s, e) for _, s, e in words], mapping


def _extract_side(
    *,
    text: str,
    tokenizer: PreTrainedTokenizerBase,
    model: Any,
    max_length: int,
    device: torch.device,
    has_cls: bool,
    has_last_token: bool,
) -> dict[str, Any]:
    enc = tokenizer(
        text,
        return_tensors="pt",
        return_offsets_mapping=True,
        truncation=True,
        max_length=max_length,
        add_special_tokens=True,
    )
    offsets = [(int(s), int(e)) for s, e in enc["offset_mapping"][0].tolist()]
    input_ids = enc["input_ids"][0].tolist()
    attention_mask = enc["attention_mask"][0].tolist()
    enc.pop("offset_mapping")
    enc = {k: v.to(device) for k, v in enc.items()}

    with torch.no_grad():
        outputs = model(**enc, output_hidden_states=True)

    hidden_states = outputs.hidden_states
    if hidden_states is None:
        raise ValueError("model did not return hidden states")

    words, word_spans, token_to_word = _word_index_map(text, offsets)
    non_special_token_indices = [
        i for i, (s, e) in enumerate(offsets) if e > s and attention_mask[i] == 1
    ]

    layers: dict[str, Any] = {}
    for layer_idx, h in enumerate(hidden_states):
        arr = h[0].detach().cpu().numpy().astype(np.float32)  # [seq, dim]
        word_vectors: list[np.ndarray] = []
        for word_idx in range(len(words)):
            token_idxs = [t for t, w in token_to_word.items() if w == word_idx]
            if not token_idxs:
                continue
            word_vectors.append(arr[token_idxs].mean(axis=0).astype(np.float32))

        if word_vectors:
            word_matrix = np.vstack(word_vectors).astype(np.float16)
            mean_vec = mean_pool(word_matrix.astype(np.float32))
        else:
            dim = arr.shape[-1]
            word_matrix = np.zeros((0, dim), dtype=np.float16)
            mean_vec = np.zeros((dim,), dtype=np.float32)

        cls_vec = None
        if has_cls and len(input_ids) > 0:
            cls_vec = arr[0].astype(np.float32)

        last_vec = None
        if has_last_token and non_special_token_indices:
            last_vec = arr[non_special_token_indices[-1]].astype(np.float32)

        layers[str(layer_idx)] = {
            "word_matrix": word_matrix,
            "mean": mean_vec,
            "cls": cls_vec,
            "last": last_vec,
        }

    return {
        "text": text,
        "words": words,
        "word_spans": word_spans,
        "offsets": offsets,
        "input_ids": input_ids,
        "layers": layers,
    }


def _extract_dataset_for_model(
    *,
    model_name: str,
    dataset_path: str,
    cache_root: str,
    max_length: int,
    seed: int,
    config_hash: str,
    torch_dtype: torch.dtype | None,
    trust_remote_code: bool,
    device_map: str | None,
    max_memory: dict[int | str, str] | None,
    low_cpu_mem_usage: bool | None,
) -> tuple[str, str]:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = AutoTokenizer.from_pretrained(
        model_name, use_fast=True, trust_remote_code=trust_remote_code
    )
    tokenizer = tokenizer if isinstance(tokenizer, PreTrainedTokenizerBase) else None
    if tokenizer is None:
        raise ValueError(f"tokenizer for {model_name} is not a PreTrainedTokenizerBase")
    if tokenizer.pad_token_id is None and tokenizer.eos_token_id is not None:
        tokenizer.pad_token = tokenizer.eos_token

    model_config = AutoConfig.from_pretrained(model_name, trust_remote_code=trust_remote_code)
    model_kwargs: dict[str, Any] = {"trust_remote_code": trust_remote_code}
    if torch_dtype is not None:
        model_kwargs["torch_dtype"] = torch_dtype
    if device_map is not None:
        model_kwargs["device_map"] = device_map
    if max_memory is not None:
        model_kwargs["max_memory"] = max_memory
    if low_cpu_mem_usage is not None:
        model_kwargs["low_cpu_mem_usage"] = low_cpu_mem_usage
    model = AutoModel.from_pretrained(model_name, **model_kwargs)
    model.eval()
    if device_map is None:
        model.to(device)
    else:
        device = _device_from_model(model)

    has_cls = tokenizer.cls_token_id is not None
    has_last = bool(getattr(model_config, "is_decoder", False)) or not has_cls

    rows = read_jsonl(dataset_path)
    items: list[dict[str, Any]] = []
    for row in tqdm(rows, desc=f"extract:{model_name}:{Path(dataset_path).stem}"):
        side_s = _extract_side(
            text=str(row["s"]),
            tokenizer=tokenizer,
            model=model,
            max_length=max_length,
            device=device,
            has_cls=has_cls,
            has_last_token=has_last,
        )
        side_cf = _extract_side(
            text=str(row["s_cf"]),
            tokenizer=tokenizer,
            model=model,
            max_length=max_length,
            device=device,
            has_cls=has_cls,
            has_last_token=has_last,
        )
        layers: dict[str, Any] = {}
        for key in side_s["layers"]:
            layers[key] = {
                "s_word_matrix": side_s["layers"][key]["word_matrix"],
                "s_cf_word_matrix": side_cf["layers"][key]["word_matrix"],
                "s_mean": side_s["layers"][key]["mean"],
                "s_cf_mean": side_cf["layers"][key]["mean"],
                "s_cls": side_s["layers"][key]["cls"],
                "s_cf_cls": side_cf["layers"][key]["cls"],
                "s_last": side_s["layers"][key]["last"],
                "s_cf_last": side_cf["layers"][key]["last"],
            }

        items.append(
            {
                "pair_id": row["id"],
                "phenomenon": row["phenomenon"],
                "template_id": row["template_id"],
                "split": row["split"],
                "s": row["s"],
                "s_cf": row["s_cf"],
                "gold_label": row.get("gold_label"),
                "edited_spans": row.get("edited_spans"),
                "s_words": side_s["words"],
                "s_cf_words": side_cf["words"],
                "s_word_spans": side_s["word_spans"],
                "s_cf_word_spans": side_cf["word_spans"],
                "layers": layers,
            }
        )

    dataset_stem = Path(dataset_path).stem
    out_dir = ensure_dir(Path(cache_root) / "hidden" / _safe_name(model_name) / dataset_stem)
    cache_path = str(out_dir / "hidden_cache.pkl")
    metadata_path = str(out_dir / "metadata.json")
    tokenized_metadata_path = str(
        Path(cache_root) / "tokenized" / _safe_name(model_name) / f"{dataset_stem}.json"
    )
    ensure_dir(Path(tokenized_metadata_path).parent)

    payload = {
        "schema_version": "css_hidden_cache_v1",
        "model_name": model_name,
        "dataset_path": dataset_path,
        "items": items,
    }
    save_hidden_cache(cache_path, payload)

    metadata = {
        "schema_version": "css_hidden_cache_v1",
        "model_name": model_name,
        "dataset_path": dataset_path,
        "dataset_sha256": sha256_file(dataset_path),
        "config_sha256": config_hash,
        "layers": "embedding_plus_12",
        "pooling": [
            "mean_non_special",
            "cls_if_available",
            "last_if_available",
            "token_matrix_word_level",
        ],
        "dtype": "float16_matrices_float32_pools",
        "seed": seed,
        "python_version": ".".join(map(str, list(sys.version_info[:3]))),
        "torch_version": torch.__version__,
        "transformers_version": transformers.__version__,
        "device": str(device),
        "model_torch_dtype": str(torch_dtype) if torch_dtype is not None else "default",
        "cache_path": cache_path,
    }
    write_cache_metadata(metadata_path, metadata)
    write_cache_metadata(
        tokenized_metadata_path,
        {"model_name": model_name, "dataset_path": dataset_path, "rows": len(rows)},
    )

    del model
    del tokenizer
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    return cache_path, metadata_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract hidden states and cache them for CSS.")
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", default=None, help="optional manifest output override")
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    cfg = load_yaml(args.config)
    seed = int(args.seed if args.seed is not None else cfg.get("seed", 13))
    _set_seed(seed)

    models = [str(m) for m in cfg["models"]]
    datasets = [str(d) for d in cfg["datasets"]]
    cache_root = str(cfg.get("cache_root", "cache"))
    max_length = int(cfg.get("max_length", 128))
    dtype_name = str(cfg.get("torch_dtype", "default")).lower()
    dtype_map = {
        "default": None,
        "auto": None,
        "float32": torch.float32,
        "fp32": torch.float32,
        "float16": torch.float16,
        "fp16": torch.float16,
        "bfloat16": torch.bfloat16,
        "bf16": torch.bfloat16,
    }
    if dtype_name not in dtype_map:
        raise ValueError(f"Unsupported torch_dtype={dtype_name}")
    torch_dtype = dtype_map[dtype_name]
    trust_remote_code = bool(cfg.get("trust_remote_code", False))
    device_map = str(cfg["device_map"]) if cfg.get("device_map") is not None else None
    max_memory = _max_memory_from_config(cfg)
    low_cpu_mem_usage = (
        bool(cfg["low_cpu_mem_usage"]) if cfg.get("low_cpu_mem_usage") is not None else None
    )
    config_hash = sha256_json(cfg)

    manifest = {
        "experiment_name": cfg.get("experiment_name", "unknown"),
        "config_path": args.config,
        "config_sha256": config_hash,
        "seed": seed,
        "runs": [],
    }

    for model_name in models:
        for dataset_path in datasets:
            dataset_stem = Path(dataset_path).stem
            out_dir = Path(cache_root) / "hidden" / _safe_name(model_name) / dataset_stem
            cache_path = out_dir / "hidden_cache.pkl"
            if cache_path.exists() and not args.force:
                print(f"skip existing {cache_path}")
                continue
            cache_path_s, metadata_path_s = _extract_dataset_for_model(
                model_name=model_name,
                dataset_path=dataset_path,
                cache_root=cache_root,
                max_length=max_length,
                seed=seed,
                config_hash=config_hash,
                torch_dtype=torch_dtype,
                trust_remote_code=trust_remote_code,
                device_map=device_map,
                max_memory=max_memory,
                low_cpu_mem_usage=low_cpu_mem_usage,
            )
            manifest["runs"].append(
                {
                    "model_name": model_name,
                    "dataset_path": dataset_path,
                    "cache_path": cache_path_s,
                    "metadata_path": metadata_path_s,
                }
            )
            print(f"cached model={model_name} dataset={dataset_path}")

    manifest_path = args.output or "results/manifests/extract_hidden_manifest.json"
    write_cache_metadata(manifest_path, manifest)
    print(f"wrote {manifest_path}")


if __name__ == "__main__":
    main()
