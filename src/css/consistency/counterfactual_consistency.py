from __future__ import annotations

import argparse
import random
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import torch
from tqdm.auto import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.tokenization_utils_base import PreTrainedTokenizerBase

from css.common.config import load_yaml
from css.common.io import ensure_dir, read_jsonl


def _set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def _dtype_from_name(name: str) -> torch.dtype | None:
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
    key = name.lower()
    if key not in dtype_map:
        raise ValueError(f"Unsupported torch_dtype={name}")
    return dtype_map[key]


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


def _make_prompt(sentence_a: str, sentence_b: str, phenomenon: str) -> str:
    if phenomenon == "role_reversal":
        criterion = "the same event with the same participant roles"
    elif phenomenon == "negation":
        criterion = "the same polarity and predicate meaning"
    else:
        criterion = "the same meaning"
    return (
        "Decide whether two sentences preserve the same meaning.\n"
        f"Criterion: They must describe {criterion}.\n"
        f"Sentence 1: {sentence_a}\n"
        f"Sentence 2: {sentence_b}\n"
        "Answer yes or no.\n"
        "Answer:"
    )


def _format_prompt(
    *,
    prompt: str,
    tokenizer: PreTrainedTokenizerBase,
    use_chat_template: bool,
) -> str:
    if not use_chat_template:
        return prompt
    chat_template = getattr(tokenizer, "chat_template", None)
    if not chat_template:
        return prompt
    return str(
        tokenizer.apply_chat_template(
            [{"role": "user", "content": prompt}],
            tokenize=False,
            add_generation_prompt=True,
        )
    )


def _score_candidate(
    *,
    prompt: str,
    candidate: str,
    tokenizer: PreTrainedTokenizerBase,
    model: Any,
    device: torch.device,
    max_length: int,
) -> float:
    prompt_ids = tokenizer(prompt, add_special_tokens=False)["input_ids"]
    candidate_ids = tokenizer(candidate, add_special_tokens=False)["input_ids"]
    input_ids = prompt_ids + candidate_ids
    if len(input_ids) > max_length:
        input_ids = input_ids[-max_length:]
        prompt_len = max(len(input_ids) - len(candidate_ids), 0)
    else:
        prompt_len = len(prompt_ids)

    ids = torch.tensor([input_ids], dtype=torch.long, device=device)
    with torch.no_grad():
        logits = model(input_ids=ids).logits

    log_probs = torch.log_softmax(logits[:, :-1, :], dim=-1)
    labels = ids[:, 1:]
    token_log_probs = log_probs.gather(dim=-1, index=labels.unsqueeze(-1)).squeeze(-1)[0]

    first_candidate_pos = max(prompt_len - 1, 0)
    candidate_log_probs = token_log_probs[
        first_candidate_pos : first_candidate_pos + len(candidate_ids)
    ]
    if candidate_log_probs.numel() == 0:
        return float("-inf")
    return float(candidate_log_probs.mean().detach().cpu())


def _predict_yes_no(
    *,
    prompt: str,
    tokenizer: PreTrainedTokenizerBase,
    model: Any,
    device: torch.device,
    max_length: int,
) -> dict[str, Any]:
    yes_score = _score_candidate(
        prompt=prompt,
        candidate=" yes",
        tokenizer=tokenizer,
        model=model,
        device=device,
        max_length=max_length,
    )
    no_score = _score_candidate(
        prompt=prompt,
        candidate=" no",
        tokenizer=tokenizer,
        model=model,
        device=device,
        max_length=max_length,
    )
    pred = "yes" if yes_score >= no_score else "no"
    return {
        "predicted_label": pred,
        "score_yes": yes_score,
        "score_no": no_score,
        "margin_yes_minus_no": yes_score - no_score,
    }


def _load_model(cfg: dict[str, Any]) -> tuple[PreTrainedTokenizerBase, Any, torch.device]:
    model_name = str(cfg["model"])
    trust_remote_code = bool(cfg.get("trust_remote_code", False))
    dtype = _dtype_from_name(str(cfg.get("torch_dtype", "default")))
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    tokenizer = AutoTokenizer.from_pretrained(
        model_name, use_fast=True, trust_remote_code=trust_remote_code
    )
    tokenizer = tokenizer if isinstance(tokenizer, PreTrainedTokenizerBase) else None
    if tokenizer is None:
        raise ValueError(f"tokenizer for {model_name} is not a PreTrainedTokenizerBase")
    if tokenizer.pad_token_id is None and tokenizer.eos_token_id is not None:
        tokenizer.pad_token = tokenizer.eos_token

    kwargs: dict[str, Any] = {"trust_remote_code": trust_remote_code}
    if dtype is not None:
        kwargs["torch_dtype"] = dtype
    if cfg.get("device_map") is not None:
        kwargs["device_map"] = cfg["device_map"]
    max_memory = _max_memory_from_config(cfg)
    if max_memory is not None:
        kwargs["max_memory"] = max_memory
    if cfg.get("low_cpu_mem_usage") is not None:
        kwargs["low_cpu_mem_usage"] = bool(cfg["low_cpu_mem_usage"])

    model = AutoModelForCausalLM.from_pretrained(model_name, **kwargs).eval()
    if cfg.get("device_map") is None:
        model.to(device)
    else:
        device = _device_from_model(model)
    return tokenizer, model, device


def _limit_rows(rows: list[dict[str, Any]], cfg: dict[str, Any]) -> list[dict[str, Any]]:
    max_pairs = cfg.get("max_pairs")
    max_pairs_per_phenomenon = cfg.get("max_pairs_per_phenomenon")
    if max_pairs is None and max_pairs_per_phenomenon is None:
        return rows

    sorted_rows = sorted(rows, key=lambda r: (str(r["phenomenon"]), str(r["id"])))
    if max_pairs_per_phenomenon is not None:
        limit = int(max_pairs_per_phenomenon)
        counts: dict[str, int] = {}
        limited = []
        for row in sorted_rows:
            phenomenon = str(row["phenomenon"])
            counts[phenomenon] = counts.get(phenomenon, 0)
            if counts[phenomenon] >= limit:
                continue
            limited.append(row)
            counts[phenomenon] += 1
        sorted_rows = limited

    if max_pairs is not None:
        sorted_rows = sorted_rows[: int(max_pairs)]
    return sorted_rows


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Score output-level yes/no counterfactual consistency."
    )
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    cfg = load_yaml(args.config)
    seed = int(cfg.get("seed", 13))
    _set_seed(seed)

    dataset_path = str(cfg["dataset"])
    model_name = str(cfg["model"])
    max_length = int(cfg.get("max_length", 256))
    output_path = Path(str(cfg["output_path"]))
    summary_path = Path(str(cfg["summary_path"]))
    use_chat_template = bool(cfg.get("use_chat_template", False))

    tokenizer, model, device = _load_model(cfg)
    rows = _limit_rows(read_jsonl(dataset_path), cfg)
    out: list[dict[str, Any]] = []

    for row in tqdm(rows, desc=f"consistency:{model_name}"):
        examples = [
            {
                "condition": "identity_control",
                "sentence_b": str(row["s"]),
                "gold_label": "yes",
            },
            {
                "condition": "counterfactual",
                "sentence_b": str(row["s_cf"]),
                "gold_label": "no",
            },
        ]
        for ex in examples:
            prompt = _format_prompt(
                prompt=_make_prompt(str(row["s"]), ex["sentence_b"], str(row["phenomenon"])),
                tokenizer=tokenizer,
                use_chat_template=use_chat_template,
            )
            pred = _predict_yes_no(
                prompt=prompt,
                tokenizer=tokenizer,
                model=model,
                device=device,
                max_length=max_length,
            )
            out.append(
                {
                    "pair_id": row["id"],
                    "phenomenon": row["phenomenon"],
                    "model": model_name,
                    "condition": ex["condition"],
                    "gold_label": ex["gold_label"],
                    "predicted_label": pred["predicted_label"],
                    "correct": pred["predicted_label"] == ex["gold_label"],
                    "score_yes": pred["score_yes"],
                    "score_no": pred["score_no"],
                    "margin_yes_minus_no": pred["margin_yes_minus_no"],
                    "s": row["s"],
                    "s_eval": ex["sentence_b"],
                    "edit_type": row["edit_type"],
                    "split": row["split"],
                }
            )

    df = pd.DataFrame(out).sort_values(["phenomenon", "pair_id", "condition"])
    ensure_dir(output_path.parent)
    df.to_csv(output_path, index=False)

    summary = (
        df.groupby(["model", "phenomenon", "condition"], as_index=False)
        .agg(
            n=("pair_id", "size"),
            accuracy=("correct", "mean"),
            yes_rate=("predicted_label", lambda s: float((s == "yes").mean())),
            mean_margin_yes_minus_no=("margin_yes_minus_no", "mean"),
        )
        .sort_values(["model", "phenomenon", "condition"])
    )
    ensure_dir(summary_path.parent)
    summary.to_csv(summary_path, index=False)

    print(f"wrote {output_path} rows={len(df)}")
    print(f"wrote {summary_path} rows={len(summary)}")


if __name__ == "__main__":
    main()
