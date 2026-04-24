from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import torch
from tqdm.auto import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer

from css.common.config import load_yaml
from css.common.io import ensure_dir, read_jsonl


def _overlap(a_start: int, a_end: int, b_start: int, b_end: int) -> bool:
    return max(a_start, b_start) < min(a_end, b_end)


def _collect_key_spans(row: dict[str, Any], side: str) -> list[tuple[int, int]]:
    spans = row.get("edited_spans", {}).get(side, [])
    out: list[tuple[int, int]] = []
    for span in spans:
        out.append((int(span["char_start"]), int(span["char_end"])))
    return out


def _score_sentence(
    text: str,
    key_spans: list[tuple[int, int]],
    tokenizer: Any,
    model: Any,
    device: torch.device,
    max_length: int,
) -> dict[str, float]:
    enc = tokenizer(
        text,
        return_tensors="pt",
        return_offsets_mapping=True,
        add_special_tokens=False,
        truncation=True,
        max_length=max_length,
    )
    offsets = [(int(s), int(e)) for s, e in enc["offset_mapping"][0].tolist()]
    enc.pop("offset_mapping")
    input_ids = enc["input_ids"].to(device)

    if input_ids.shape[1] < 2:
        return {"total": 0.0, "avg": 0.0, "key": 0.0, "key_count": 0}

    with torch.no_grad():
        logits = model(input_ids=input_ids).logits

    shift_logits = logits[:, :-1, :]
    shift_labels = input_ids[:, 1:]
    log_probs = torch.log_softmax(shift_logits, dim=-1)
    nll = (
        -log_probs.gather(dim=-1, index=shift_labels.unsqueeze(-1))
        .squeeze(-1)[0]
        .detach()
        .cpu()
        .numpy()
    )

    total = float(np.sum(nll))
    avg = float(np.mean(nll))

    key_vals = []
    for tok_idx in range(1, len(offsets)):
        start, end = offsets[tok_idx]
        if end <= start:
            continue
        if any(_overlap(start, end, ks, ke) for ks, ke in key_spans):
            key_vals.append(float(nll[tok_idx - 1]))
    key_total = float(np.sum(key_vals)) if key_vals else 0.0
    return {"total": total, "avg": avg, "key": key_total, "key_count": len(key_vals)}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compute GPT-2 autoregressive surprisal for CSS pairs."
    )
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", default=None)
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()

    cfg = load_yaml(args.config)
    _ = args.seed if args.seed is not None else int(cfg.get("seed", 13))

    dataset_path = str(cfg["dataset"])
    model_name = str(cfg.get("model", "gpt2"))
    max_length = int(cfg.get("max_length", 128))
    output_path = str(args.output or cfg.get("output_path", "results/surprisal/gpt2_surprisal.csv"))

    device = torch.device("cpu")
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    model = AutoModelForCausalLM.from_pretrained(model_name).eval()

    rows = read_jsonl(dataset_path)
    out_rows: list[dict[str, Any]] = []
    coverage = 0

    for row in tqdm(rows, desc="gpt2-surprisal"):
        key_s = _collect_key_spans(row, "s")
        key_cf = _collect_key_spans(row, "s_cf")
        s_stats = _score_sentence(str(row["s"]), key_s, tokenizer, model, device, max_length)
        cf_stats = _score_sentence(str(row["s_cf"]), key_cf, tokenizer, model, device, max_length)
        if s_stats["key_count"] > 0 and cf_stats["key_count"] > 0:
            coverage += 1

        out_rows.append(
            {
                "pair_id": row["id"],
                "phenomenon": row["phenomenon"],
                "model": model_name,
                "total_surprisal_s": s_stats["total"],
                "total_surprisal_cf": cf_stats["total"],
                "avg_surprisal_s": s_stats["avg"],
                "avg_surprisal_cf": cf_stats["avg"],
                "delta_total_surprisal": cf_stats["total"] - s_stats["total"],
                "delta_avg_surprisal": cf_stats["avg"] - s_stats["avg"],
                "abs_delta_avg_surprisal": abs(cf_stats["avg"] - s_stats["avg"]),
                "key_region_surprisal_s": s_stats["key"],
                "key_region_surprisal_cf": cf_stats["key"],
                "delta_key_region_surprisal": cf_stats["key"] - s_stats["key"],
                "key_region_count_s": s_stats["key_count"],
                "key_region_count_cf": cf_stats["key_count"],
            }
        )

    df = pd.DataFrame(out_rows).sort_values(["phenomenon", "pair_id"]).reset_index(drop=True)
    ensure_dir(Path(output_path).parent)
    df.to_csv(output_path, index=False)

    coverage_rate = coverage / max(len(rows), 1)
    report_path = Path("results/surprisal/key_region_coverage.json")
    ensure_dir(report_path.parent)
    pd.Series(
        {"coverage_rate": coverage_rate, "covered_pairs": coverage, "total_pairs": len(rows)}
    ).to_json(report_path)
    print(f"wrote {output_path} rows={len(df)}")
    print(f"wrote {report_path} coverage={coverage_rate:.3f}")


if __name__ == "__main__":
    main()
