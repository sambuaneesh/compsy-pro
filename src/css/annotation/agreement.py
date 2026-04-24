from __future__ import annotations

import argparse
import itertools

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from css.common.io import write_json


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute agreement stats for CSS annotations.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="results/annotation/agreement_report.json")
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    annotators = sorted(df["annotator_id"].unique().tolist())
    pairwise = []
    for a, b in itertools.combinations(annotators, 2):
        da = df[df["annotator_id"] == a][["pair_id", "human_change_0_5"]].rename(
            columns={"human_change_0_5": "a"}
        )
        db = df[df["annotator_id"] == b][["pair_id", "human_change_0_5"]].rename(
            columns={"human_change_0_5": "b"}
        )
        merged = da.merge(db, on="pair_id", how="inner")
        if len(merged) < 5:
            continue
        rho, _ = spearmanr(merged["a"], merged["b"])
        pairwise.append(float(rho))

    rating_range = df.groupby("pair_id")["human_change_0_5"].agg(
        lambda s: float(np.max(s) - np.min(s))
    )
    disagreement_pct = float((rating_range >= 3.0).mean()) if len(rating_range) else 0.0

    report = {
        "n_rows": len(df),
        "n_pairs": int(df["pair_id"].nunique()),
        "n_annotators": len(annotators),
        "mean_pairwise_spearman": float(np.mean(pairwise)) if pairwise else None,
        "median_pairwise_spearman": float(np.median(pairwise)) if pairwise else None,
        "pct_pairs_range_ge_3": disagreement_pct,
    }
    write_json(args.output, report)
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
