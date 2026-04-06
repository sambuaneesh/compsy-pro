from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from css.common.config import load_yaml
from css.common.io import ensure_dir


def _top_layers(corr_path: str, out_dir: Path) -> None:
    corr = pd.read_csv(corr_path)
    top = (
        corr.sort_values(["model", "phenomenon", "metric", "spearman_rho"], ascending=False)
        .groupby(["model", "phenomenon", "metric"], as_index=False)
        .first()
        .sort_values(["model", "phenomenon", "metric"])
    )
    top.to_csv(out_dir / "top_layer_by_metric.csv", index=False)


def _frob_incremental(h2_path: str, out_dir: Path) -> None:
    h2 = pd.read_csv(h2_path)
    positive = h2[h2["delta_adj_r2"] > 0].sort_values(
        ["delta_adj_r2", "model", "phenomenon", "layer"], ascending=[False, True, True, True]
    )
    positive.to_csv(out_dir / "frob_incremental_positive.csv", index=False)

    summary = h2.groupby(["model", "phenomenon"], as_index=False).agg(
        mean_delta_adj_r2=("delta_adj_r2", "mean"),
        max_delta_adj_r2=("delta_adj_r2", "max"),
    )
    summary.to_csv(out_dir / "frob_incremental_summary.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate CSS ablation summary tables.")
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    cfg = load_yaml(args.config)
    out_dir = ensure_dir(str(cfg["output_dir"]))
    _top_layers(str(cfg["correlations_path"]), out_dir)
    _frob_incremental(str(cfg["h2_path"]), out_dir)
    print(f"wrote tables to {out_dir}")


if __name__ == "__main__":
    main()
