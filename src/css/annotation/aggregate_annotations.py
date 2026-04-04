from __future__ import annotations

import argparse

import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate CSS human annotation ratings.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="data/annotations/human_css_aggregated.csv")
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    agg = (
        df.groupby(["pair_id", "phenomenon"])
        .agg(
            n_annotators=("annotator_id", "nunique"),
            mean_change=("human_change_0_5", "mean"),
            median_change=("human_change_0_5", "median"),
            sd_change=("human_change_0_5", "std"),
            mean_confidence=("confidence_1_5", "mean"),
            mean_fluency_s=("fluency_s_1_5", "mean"),
            mean_fluency_cf=("fluency_cf_1_5", "mean"),
        )
        .reset_index()
    )
    agg["agreement_flag"] = agg["sd_change"].fillna(0.0) <= 1.25
    agg.to_csv(args.output, index=False)
    print(f"wrote {args.output} rows={len(agg)}")


if __name__ == "__main__":
    main()
