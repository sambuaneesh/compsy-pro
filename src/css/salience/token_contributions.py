from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from css.common.config import load_yaml
from css.common.io import ensure_dir
from css.metrics.matrix_norms import frobenius_similarity
from css.representations.cache_io import load_hidden_cache
from css.representations.pooling import row_l2_normalize


def _safe_name(name: str) -> str:
    return name.replace("/", "__")


def _char_overlap(a_start: int, a_end: int, b_start: int, b_end: int) -> bool:
    return max(a_start, b_start) < min(a_end, b_end)


def _gold_token_indices(
    word_spans: list[tuple[int, int]], edited_spans: list[dict[str, Any]]
) -> set[int]:
    gold: set[int] = set()
    for i, (w_start, w_end) in enumerate(word_spans):
        for span in edited_spans:
            if _char_overlap(w_start, w_end, int(span["char_start"]), int(span["char_end"])):
                gold.add(i)
                break
    return gold


def _normalize_scores(x: np.ndarray) -> np.ndarray:
    if x.size == 0:
        return x
    x = np.maximum(x.astype(np.float32), 0.0)
    denom = float(x.sum())
    if denom <= 0.0:
        return np.zeros_like(x, dtype=np.float32)
    return x / denom


def _contribution_vectors(
    a: np.ndarray, b: np.ndarray, *, clip_negative: bool = True, row_normalize: bool = True
) -> tuple[np.ndarray, np.ndarray]:
    x = a.astype(np.float32)
    y = b.astype(np.float32)
    if row_normalize:
        x = row_l2_normalize(x)
        y = row_l2_normalize(y)
    cross = x @ y.T
    if clip_negative:
        cross = np.maximum(cross, 0.0)
    row_contrib = cross.sum(axis=1)
    col_contrib = cross.sum(axis=0)
    return _normalize_scores(row_contrib), _normalize_scores(col_contrib)


def _loo_drops(
    a: np.ndarray, b: np.ndarray, *, clip_negative: bool = True, row_normalize: bool = True
) -> tuple[np.ndarray, np.ndarray]:
    base = frobenius_similarity(
        a, b, clip_negative=clip_negative, row_normalize=row_normalize, eps=1e-9
    )
    if a.shape[0] == 0 or b.shape[0] == 0:
        return np.zeros(a.shape[0], dtype=np.float32), np.zeros(b.shape[0], dtype=np.float32)

    row_drops = np.zeros(a.shape[0], dtype=np.float32)
    for i in range(a.shape[0]):
        if a.shape[0] == 1:
            row_drops[i] = np.float32(base)
            continue
        sim = frobenius_similarity(
            np.delete(a, i, axis=0),
            b,
            clip_negative=clip_negative,
            row_normalize=row_normalize,
            eps=1e-9,
        )
        row_drops[i] = np.float32(max(0.0, base - sim))

    col_drops = np.zeros(b.shape[0], dtype=np.float32)
    for j in range(b.shape[0]):
        if b.shape[0] == 1:
            col_drops[j] = np.float32(base)
            continue
        sim = frobenius_similarity(
            a,
            np.delete(b, j, axis=0),
            clip_negative=clip_negative,
            row_normalize=row_normalize,
            eps=1e-9,
        )
        col_drops[j] = np.float32(max(0.0, base - sim))

    return _normalize_scores(row_drops), _normalize_scores(col_drops)


def _layer_map_from_metrics(metrics_path: str) -> dict[tuple[str, str], int]:
    metrics = pd.read_csv(metrics_path)
    grouped = (
        metrics.groupby(["model", "phenomenon", "layer"], as_index=False)["delta_frob"]
        .mean()
        .sort_values(["model", "phenomenon", "delta_frob"], ascending=[True, True, False])
    )
    top = grouped.groupby(["model", "phenomenon"], as_index=False).first()
    return {(str(r["model"]), str(r["phenomenon"])): int(r["layer"]) for _, r in top.iterrows()}


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute token salience contributions.")
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    cfg = load_yaml(args.config)
    layer_map = _layer_map_from_metrics(str(cfg["metrics_path"]))
    cache_root = str(cfg.get("cache_root", "cache"))
    output_path = str(cfg["output_contrib_path"])

    rows: list[dict[str, Any]] = []
    for model_name in cfg["models"]:
        for dataset_path in cfg["datasets"]:
            stem = Path(str(dataset_path)).stem
            cache_path = (
                Path(cache_root)
                / "hidden"
                / _safe_name(str(model_name))
                / stem
                / "hidden_cache.pkl"
            )
            if not cache_path.exists():
                continue
            payload = load_hidden_cache(cache_path)
            for item in payload["items"]:
                phenomenon = str(item["phenomenon"])
                key = (str(model_name), phenomenon)
                if key not in layer_map:
                    continue
                layer = layer_map[key]
                layer_payload = item["layers"][str(layer)]
                a = layer_payload["s_word_matrix"]
                b = layer_payload["s_cf_word_matrix"]
                if a.shape[0] == 0 or b.shape[0] == 0:
                    continue

                s_words = list(item["s_words"])[: a.shape[0]]
                s_cf_words = list(item["s_cf_words"])[: b.shape[0]]
                s_spans = list(item["s_word_spans"])[: a.shape[0]]
                s_cf_spans = list(item["s_cf_word_spans"])[: b.shape[0]]
                if len(s_words) < a.shape[0]:
                    s_words.extend([f"tok_{i}" for i in range(len(s_words), a.shape[0])])
                if len(s_cf_words) < b.shape[0]:
                    s_cf_words.extend([f"tok_{i}" for i in range(len(s_cf_words), b.shape[0])])

                row_contrib, col_contrib = _contribution_vectors(a, b)
                row_loo, col_loo = _loo_drops(a, b)

                score_s = 0.5 * row_contrib + 0.5 * row_loo
                score_cf = 0.5 * col_contrib + 0.5 * col_loo
                score_s = _normalize_scores(score_s)
                score_cf = _normalize_scores(score_cf)

                gold_s = _gold_token_indices(s_spans, item["edited_spans"]["s"])
                gold_cf = _gold_token_indices(s_cf_spans, item["edited_spans"]["s_cf"])

                for i, token in enumerate(s_words):
                    rows.append(
                        {
                            "pair_id": item["pair_id"],
                            "phenomenon": phenomenon,
                            "model": str(model_name),
                            "layer": layer,
                            "side": "s",
                            "token_index": i,
                            "token": token,
                            "contrib_cross": float(row_contrib[i]),
                            "contrib_loo_drop": float(row_loo[i]),
                            "salience_score": float(score_s[i]),
                            "is_gold": int(i in gold_s),
                        }
                    )

                for j, token in enumerate(s_cf_words):
                    rows.append(
                        {
                            "pair_id": item["pair_id"],
                            "phenomenon": phenomenon,
                            "model": str(model_name),
                            "layer": layer,
                            "side": "s_cf",
                            "token_index": j,
                            "token": token,
                            "contrib_cross": float(col_contrib[j]),
                            "contrib_loo_drop": float(col_loo[j]),
                            "salience_score": float(score_cf[j]),
                            "is_gold": int(j in gold_cf),
                        }
                    )

    df = pd.DataFrame(rows)
    if df.empty:
        raise SystemExit("No salience rows were generated")
    df = df.sort_values(
        ["model", "phenomenon", "pair_id", "side", "salience_score"], ascending=False
    ).reset_index(drop=True)
    ensure_dir(Path(output_path).parent)
    df.to_csv(output_path, index=False)
    print(f"wrote {output_path} rows={len(df)}")


if __name__ == "__main__":
    main()
