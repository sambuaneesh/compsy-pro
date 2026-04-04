from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from css.common.config import load_yaml
from css.common.io import ensure_dir, write_json
from css.common.text import levenshtein_distance, lexical_jaccard, token_len
from css.metrics.cosine import cosine_shift
from css.metrics.matrix_norms import frobenius_shift
from css.metrics.token_shift import aligned_token_shift
from css.representations.cache_io import load_hidden_cache


def _safe_name(name: str) -> str:
    return name.replace("/", "__")


def _iter_cache_paths(cfg: dict[str, Any]) -> list[tuple[str, str, str]]:
    out: list[tuple[str, str, str]] = []
    cache_root = str(cfg.get("cache_root", "cache"))
    for model_name in cfg["models"]:
        for dataset_path in cfg["datasets"]:
            stem = Path(str(dataset_path)).stem
            cache_path = str(
                Path(cache_root)
                / "hidden"
                / _safe_name(str(model_name))
                / stem
                / "hidden_cache.pkl"
            )
            out.append((str(model_name), str(dataset_path), cache_path))
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute CSS metrics from hidden caches.")
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", default="results/metrics/layer_metrics.csv")
    parser.add_argument("--warnings-output", default="results/metrics/metric_warnings.json")
    parser.add_argument("--clip-negative", action="store_true", default=True)
    parser.add_argument("--no-clip-negative", action="store_true")
    parser.add_argument("--row-normalize", action="store_true", default=True)
    parser.add_argument("--no-row-normalize", action="store_true")
    args = parser.parse_args()

    cfg = load_yaml(args.config)
    clip_negative = not args.no_clip_negative
    row_normalize = not args.no_row_normalize

    rows_out: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []

    for model_name, dataset_path, cache_path in _iter_cache_paths(cfg):
        if not Path(cache_path).exists():
            warnings.append(
                {
                    "type": "missing_cache",
                    "model": model_name,
                    "dataset_path": dataset_path,
                    "cache_path": cache_path,
                }
            )
            continue

        payload = load_hidden_cache(cache_path)
        items = payload["items"]
        for item in items:
            for layer, values in item["layers"].items():
                s_mean = values["s_mean"].astype(np.float32)
                s_cf_mean = values["s_cf_mean"].astype(np.float32)
                s_mat = values["s_word_matrix"].astype(np.float32)
                s_cf_mat = values["s_cf_word_matrix"].astype(np.float32)

                delta_cos = cosine_shift(s_mean, s_cf_mean)
                sim_frob, delta_frob = frobenius_shift(
                    s_mat,
                    s_cf_mat,
                    clip_negative=clip_negative,
                    row_normalize=row_normalize,
                )
                delta_l2 = float(np.linalg.norm(s_mean - s_cf_mean))
                delta_token = aligned_token_shift(
                    words_a=item["s_words"],
                    words_b=item["s_cf_words"],
                    matrix_a=s_mat,
                    matrix_b=s_cf_mat,
                )

                if sim_frob < -1e-6 or sim_frob > 1.00001:
                    warnings.append(
                        {
                            "type": "sim_frob_out_of_range",
                            "pair_id": item["pair_id"],
                            "model": model_name,
                            "layer": layer,
                            "sim_frob": sim_frob,
                        }
                    )

                s_text = str(item["s"])
                s_cf_text = str(item["s_cf"])
                rows_out.append(
                    {
                        "pair_id": item["pair_id"],
                        "phenomenon": item["phenomenon"],
                        "model": model_name,
                        "dataset_path": dataset_path,
                        "layer": int(layer),
                        "pooling": "mean_non_special",
                        "delta_cos": delta_cos,
                        "sim_frob": sim_frob,
                        "delta_frob": delta_frob,
                        "delta_l2": delta_l2,
                        "delta_token_aligned": delta_token,
                        "token_count_s": token_len(s_text),
                        "token_count_cf": token_len(s_cf_text),
                        "length_delta": abs(token_len(s_text) - token_len(s_cf_text)),
                        "lexical_jaccard": lexical_jaccard(s_text, s_cf_text),
                        "edit_distance": levenshtein_distance(s_text, s_cf_text),
                        "split": item["split"],
                        "template_id": item["template_id"],
                    }
                )

    df = (
        pd.DataFrame(rows_out)
        .sort_values(["model", "phenomenon", "pair_id", "layer"])
        .reset_index(drop=True)
    )
    out_path = Path(args.output)
    ensure_dir(out_path.parent)
    df.to_csv(out_path, index=False)

    summary = (
        df.groupby(["model", "phenomenon", "layer"])[
            ["delta_cos", "delta_frob", "delta_l2", "delta_token_aligned"]
        ]
        .mean()
        .reset_index()
    )
    summary_path = out_path.parent / "layer_metrics_summary.csv"
    summary.to_csv(summary_path, index=False)

    write_json(args.warnings_output, {"warnings": warnings, "n_warnings": len(warnings)})
    print(f"wrote {out_path} rows={len(df)}")
    print(f"wrote {summary_path} rows={len(summary)}")
    print(f"wrote {args.warnings_output} warnings={len(warnings)}")


if __name__ == "__main__":
    main()
