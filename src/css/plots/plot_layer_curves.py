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


def _plot_surprisal_vs_human(surprisal_path: str, ann_path: str, out_dir: Path) -> None:
    surprisal = pd.read_csv(surprisal_path)
    ann = pd.read_csv(ann_path)
    merged = surprisal.merge(
        ann[["pair_id", "phenomenon", "mean_change"]], on=["pair_id", "phenomenon"], how="inner"
    )
    if merged.empty:
        return
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.scatterplot(
        data=merged,
        x="abs_delta_avg_surprisal",
        y="mean_change",
        hue="phenomenon",
        alpha=0.75,
        s=30,
        ax=ax,
    )
    sns.regplot(
        data=merged,
        x="abs_delta_avg_surprisal",
        y="mean_change",
        scatter=False,
        color="black",
        ax=ax,
    )
    ax.set_xlabel("|delta avg surprisal| (GPT-2)")
    ax.set_ylabel("Mean human change (0-5)")
    fig.tight_layout()
    fig.savefig(out_dir / "surprisal_vs_human.pdf")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate layer-wise CSS figures.")
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    cfg = load_yaml(args.config)
    out_dir = ensure_dir(str(cfg["output_dir"]))
    _plot_correlations(str(cfg["correlations_path"]), out_dir)
    _plot_probe_selectivity(str(cfg["probe_summary_path"]), out_dir)
    _plot_surprisal_vs_human(str(cfg["surprisal_path"]), str(cfg["annotation_agg_path"]), out_dir)
    print(f"wrote figures to {out_dir}")


if __name__ == "__main__":
    main()
