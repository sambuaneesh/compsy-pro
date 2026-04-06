from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

from css.common.config import load_yaml
from css.common.io import ensure_dir


def _pair_side_metrics(group: pd.DataFrame) -> dict[str, float]:
    ranked = group.sort_values("salience_score", ascending=False).reset_index(drop=True)
    ranked["rank"] = np.arange(1, len(ranked) + 1)
    gold = ranked[ranked["is_gold"] == 1]
    if gold.empty:
        return {"recall_at_1": np.nan, "recall_at_3": np.nan, "mrr": np.nan, "auc": np.nan}

    first_gold_rank = int(gold["rank"].min())
    recall_at_1 = float(first_gold_rank <= 1)
    recall_at_3 = float(first_gold_rank <= 3)
    mrr = 1.0 / float(first_gold_rank)

    auc = np.nan
    if ranked["is_gold"].nunique() > 1:
        auc = float(roc_auc_score(ranked["is_gold"], ranked["salience_score"]))

    return {"recall_at_1": recall_at_1, "recall_at_3": recall_at_3, "mrr": mrr, "auc": auc}


def _aggregate(rows: list[dict[str, Any]], keys: list[str], scope: str) -> list[dict[str, Any]]:
    frame = pd.DataFrame(rows)
    if frame.empty:
        return []
    out = []
    if not keys:
        g = frame
        out.append(
            {
                "scope": scope,
                "n_pair_sides": len(g),
                "recall_at_1": float(g["recall_at_1"].mean()),
                "recall_at_3": float(g["recall_at_3"].mean()),
                "mrr": float(g["mrr"].mean()),
                "auc": float(g["auc"].mean()) if g["auc"].notna().any() else np.nan,
            }
        )
        return out

    grouped = frame.groupby(keys, as_index=False)
    for _, g in grouped:
        entry = {k: g.iloc[0][k] for k in keys}
        entry["scope"] = scope
        entry["n_pair_sides"] = len(g)
        entry["recall_at_1"] = float(g["recall_at_1"].mean())
        entry["recall_at_3"] = float(g["recall_at_3"].mean())
        entry["mrr"] = float(g["mrr"].mean())
        entry["auc"] = float(g["auc"].mean()) if g["auc"].notna().any() else np.nan
        out.append(entry)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate salience ranking against gold spans.")
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    cfg = load_yaml(args.config)
    contrib_path = str(cfg["output_contrib_path"])
    eval_path = str(cfg["output_eval_path"])
    contrib = pd.read_csv(contrib_path)

    pair_rows: list[dict[str, Any]] = []
    group_keys = ["model", "phenomenon", "pair_id", "side"]
    for _, g in contrib.groupby(group_keys):
        model = str(g.iloc[0]["model"])
        phenomenon = str(g.iloc[0]["phenomenon"])
        pair_id = str(g.iloc[0]["pair_id"])
        side = str(g.iloc[0]["side"])
        metrics = _pair_side_metrics(g)
        pair_rows.append(
            {
                "model": model,
                "phenomenon": phenomenon,
                "pair_id": pair_id,
                "side": side,
                **metrics,
            }
        )

    summary_rows: list[dict[str, Any]] = []
    summary_rows.extend(_aggregate(pair_rows, ["model", "phenomenon"], "model_phenomenon"))
    summary_rows.extend(_aggregate(pair_rows, ["model"], "model"))
    summary_rows.extend(_aggregate(pair_rows, ["phenomenon"], "phenomenon"))
    summary_rows.extend(_aggregate(pair_rows, [], "overall"))

    eval_df = pd.DataFrame(summary_rows)
    ensure_dir(Path(eval_path).parent)
    eval_df.to_csv(eval_path, index=False)
    print(f"wrote {eval_path} rows={len(eval_df)}")


if __name__ == "__main__":
    main()
