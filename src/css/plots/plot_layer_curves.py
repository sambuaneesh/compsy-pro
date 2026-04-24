from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from css.common.config import load_yaml
from css.common.io import ensure_dir

sns.set_theme(style="whitegrid")


def _plot_correlations(corr_path: str, out_dir: Path) -> None:
    corr = pd.read_csv(corr_path)
    corr = corr[corr["metric"].isin(["delta_cos", "delta_frob"])]
    if corr.empty:
        return
    agg = (
        corr.groupby(["model", "layer", "metric"], as_index=False)["spearman_rho"]
        .mean()
        .sort_values(["model", "layer", "metric"])
    )
    fig, axes = plt.subplots(1, agg["model"].nunique(), figsize=(16, 4), sharey=True)
    if isinstance(axes, np.ndarray):
        axes = axes.flatten().tolist()
    elif not isinstance(axes, (list, tuple)):
        axes = [axes]
    for ax, (model, g) in zip(axes, agg.groupby("model"), strict=False):
        sns.lineplot(data=g, x="layer", y="spearman_rho", hue="metric", marker="o", ax=ax)
        ax.set_title(str(model))
        ax.set_xlabel("Layer")
        ax.set_ylabel("Spearman rho")
    fig.tight_layout()
    fig.savefig(out_dir / "layer_correlation_curves.pdf")
    plt.close(fig)


def _plot_probe_selectivity(probe_path: str, out_dir: Path) -> None:
    probe = pd.read_csv(probe_path)
    if probe.empty:
        return
    agg = (
        probe.groupby(["model", "phenomenon", "layer"], as_index=False)["selectivity"]
        .mean()
        .sort_values(["model", "phenomenon", "layer"])
    )
    g = sns.relplot(
        data=agg,
        x="layer",
        y="selectivity",
        hue="phenomenon",
        col="model",
        kind="line",
        marker="o",
        facet_kws={"sharey": True},
        height=4,
        aspect=1.1,
    )
    g.set_axis_labels("Layer", "Probe selectivity")
    g.figure.tight_layout()
    g.figure.savefig(out_dir / "probe_selectivity_curves.pdf")
    plt.close(g.figure)


def _plot_surprisal_vs_shift(metrics_path: str, surprisal_path: str, out_dir: Path) -> None:
    metrics = pd.read_csv(metrics_path)
    surprisal = pd.read_csv(surprisal_path)
    merged = metrics.merge(
        surprisal[["pair_id", "phenomenon", "abs_delta_avg_surprisal"]],
        on=["pair_id", "phenomenon"],
        how="inner",
    )
    merged = merged.groupby(["model", "phenomenon", "pair_id"], as_index=False)[
        ["delta_frob", "abs_delta_avg_surprisal"]
    ].mean()
    if merged.empty:
        return
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.scatterplot(
        data=merged,
        x="delta_frob",
        y="abs_delta_avg_surprisal",
        hue="phenomenon",
        alpha=0.75,
        s=30,
        ax=ax,
    )
    sns.regplot(
        data=merged,
        x="delta_frob",
        y="abs_delta_avg_surprisal",
        scatter=False,
        color="black",
        ax=ax,
    )
    ax.set_xlabel("Mean delta_frob")
    ax.set_ylabel("|delta avg surprisal| (GPT-2)")
    fig.tight_layout()
    fig.savefig(out_dir / "surprisal_vs_shift.pdf")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate layer-wise CSS figures.")
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    cfg = load_yaml(args.config)
    out_dir = ensure_dir(str(cfg["output_dir"]))
    _plot_correlations(str(cfg["correlations_path"]), out_dir)
    _plot_probe_selectivity(str(cfg["probe_summary_path"]), out_dir)
    _plot_surprisal_vs_shift(str(cfg["metrics_path"]), str(cfg["surprisal_path"]), out_dir)
    print(f"wrote figures to {out_dir}")


if __name__ == "__main__":
    main()
