from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

ROOT = Path(__file__).resolve().parents[3]
ASSETS = ROOT / "reports" / "slides" / "assets"

sns.set_theme(style="whitegrid", context="talk")


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            out.append(json.loads(line))
    return out


def _save(fig: plt.Figure, name: str) -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    fig.savefig(ASSETS / name, dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_data_split_distribution() -> None:
    rows = _read_jsonl(ROOT / "data" / "css_pairs" / "full_all_4500.jsonl")
    df = pd.DataFrame(rows)[["phenomenon", "split"]]
    ctab = (
        df.groupby(["phenomenon", "split"], as_index=False)
        .size()
        .pivot(index="phenomenon", columns="split", values="size")
        .fillna(0)
    )
    ctab = ctab.reindex(columns=[c for c in ["train", "dev", "test"] if c in ctab.columns])
    fig, ax = plt.subplots(figsize=(12, 6))
    ctab.plot(kind="bar", stacked=True, ax=ax, colormap="Set2")
    ax.set_title("Full Dataset Split Distribution by Phenomenon")
    ax.set_xlabel("Phenomenon")
    ax.set_ylabel("Number of Pairs")
    ax.legend(title="Split")
    _save(fig, "mid_data_split_distribution.png")


def plot_edit_type_counts() -> None:
    rows = _read_jsonl(ROOT / "data" / "css_pairs" / "full_all_4500.jsonl")
    df = pd.DataFrame(rows)[["phenomenon", "edit_type"]]
    counts = df.groupby(["phenomenon", "edit_type"], as_index=False).size()
    fig, ax = plt.subplots(figsize=(14, 6))
    sns.barplot(data=counts, x="edit_type", y="size", hue="phenomenon", ax=ax)
    ax.set_title("Edit-Type Counts in Full Dataset")
    ax.set_xlabel("Edit Type")
    ax.set_ylabel("Count")
    ax.tick_params(axis="x", rotation=20)
    _save(fig, "mid_edit_type_counts.png")


def plot_metrics_coverage_heatmap() -> None:
    metrics = pd.read_csv(ROOT / "results" / "metrics" / "layer_metrics_full.csv")
    cov = metrics.groupby(["model", "phenomenon"], as_index=False).size()
    table = cov.pivot(index="model", columns="phenomenon", values="size")
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.heatmap(table, annot=True, fmt=".0f", cmap="Blues", ax=ax)
    ax.set_title("Metric Rows Coverage (Model x Phenomenon)")
    ax.set_xlabel("Phenomenon")
    ax.set_ylabel("Model")
    _save(fig, "mid_metrics_coverage_heatmap.png")


def plot_delta_frob_layer_curves() -> None:
    metrics = pd.read_csv(ROOT / "results" / "metrics" / "layer_metrics_full.csv")
    agg = (
        metrics.groupby(["model", "phenomenon", "layer"], as_index=False)["delta_frob"]
        .mean()
        .sort_values(["model", "phenomenon", "layer"])
    )
    g = sns.relplot(
        data=agg,
        x="layer",
        y="delta_frob",
        hue="phenomenon",
        col="model",
        kind="line",
        marker="o",
        height=4.2,
        aspect=1.15,
        facet_kws={"sharey": False},
    )
    g.set_axis_labels("Layer", "Mean Delta_frob")
    g.figure.suptitle("Layer-wise Frobenius Shift Profiles", y=1.03)
    _save(g.figure, "mid_delta_frob_layer_curves.png")


def plot_surprisal_by_phenomenon() -> None:
    surprisal = pd.read_csv(ROOT / "results" / "surprisal" / "gpt2_surprisal_full.csv")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(
        data=surprisal,
        x="phenomenon",
        y="abs_delta_avg_surprisal",
        hue="phenomenon",
        dodge=False,
        ax=ax,
    )
    if ax.legend_ is not None:
        ax.legend_.remove()
    ax.set_title("GPT-2 |Delta Average Surprisal| by Phenomenon")
    ax.set_xlabel("Phenomenon")
    ax.set_ylabel("|Delta Avg Surprisal|")
    _save(fig, "mid_surprisal_by_phenomenon.png")


def plot_probe_coverage_heatmap() -> None:
    probes = pd.read_csv(ROOT / "results" / "probes" / "probe_results_full.csv")
    cov = probes.groupby(["model", "phenomenon"], as_index=False).size()
    table = cov.pivot(index="model", columns="phenomenon", values="size")
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.heatmap(table, annot=True, fmt=".0f", cmap="Greens", ax=ax)
    ax.set_title("Probe Result Coverage (Model x Phenomenon)")
    ax.set_xlabel("Phenomenon")
    ax.set_ylabel("Model")
    _save(fig, "mid_probe_coverage_heatmap.png")


def plot_probe_selectivity_curves() -> None:
    sel = pd.read_csv(ROOT / "results" / "probes" / "selectivity_summary_full.csv")
    g = sns.relplot(
        data=sel,
        x="layer",
        y="selectivity",
        hue="phenomenon",
        col="model",
        kind="line",
        marker="o",
        height=4.2,
        aspect=1.15,
        facet_kws={"sharey": False},
    )
    g.set_axis_labels("Layer", "Selectivity (Task F1 - Control F1)")
    g.figure.suptitle("Probe Selectivity Curves (Full Run)", y=1.03)
    _save(g.figure, "mid_probe_selectivity_curves.png")


def plot_correlation_summary_heatmap() -> None:
    corr = pd.read_csv(ROOT / "results" / "stats" / "full" / "correlations.csv")
    corr = corr[corr["metric"].isin(["delta_cos", "delta_frob"])]
    agg = corr.groupby(["model", "phenomenon", "metric"], as_index=False)["spearman_rho"].mean()
    agg["cell"] = agg["phenomenon"] + " | " + agg["metric"]
    table = agg.pivot(index="model", columns="cell", values="spearman_rho")
    fig, ax = plt.subplots(figsize=(14, 5))
    sns.heatmap(table, annot=True, fmt=".3f", cmap="coolwarm", center=0.0, ax=ax)
    ax.set_title("Mean Spearman Correlation by Model (Delta_cos / Delta_frob)")
    ax.set_xlabel("Phenomenon | Metric")
    ax.set_ylabel("Model")
    _save(fig, "mid_correlation_summary_heatmap.png")


def plot_h2_incremental_distribution() -> None:
    h2 = pd.read_csv(ROOT / "results" / "stats" / "full" / "h2_incremental.csv")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(h2["delta_adj_r2"], bins=30, kde=True, ax=ax, color="#4C72B0")
    ax.axvline(0.0, color="black", linestyle="--", linewidth=1)
    ax.set_title("H2 Incremental Value Distribution (Delta Adj-R²)")
    ax.set_xlabel("Delta Adj-R² when adding Delta_frob")
    ax.set_ylabel("Layer-cell Count")
    _save(fig, "mid_h2_incremental_distribution.png")


def plot_salience_overall_bars() -> None:
    sal = pd.read_csv(ROOT / "results" / "salience" / "salience_eval_full.csv")
    overall = sal[sal["scope"] == "overall"].iloc[0]
    m = pd.DataFrame(
        {
            "metric": ["recall_at_1", "recall_at_3", "mrr", "auc"],
            "value": [
                overall["recall_at_1"],
                overall["recall_at_3"],
                overall["mrr"],
                overall["auc"],
            ],
        }
    )
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=m, x="metric", y="value", hue="metric", legend=False, ax=ax, palette="mako")
    ax.set_title("Salience Evaluation (Overall)")
    ax.set_xlabel("Metric")
    ax.set_ylabel("Score")
    ax.set_ylim(0, 1)
    _save(fig, "mid_salience_overall_bars.png")


def main() -> None:
    plot_data_split_distribution()
    plot_edit_type_counts()
    plot_metrics_coverage_heatmap()
    plot_delta_frob_layer_curves()
    plot_surprisal_by_phenomenon()
    plot_probe_coverage_heatmap()
    plot_probe_selectivity_curves()
    plot_correlation_summary_heatmap()
    plot_h2_incremental_distribution()
    plot_salience_overall_bars()
    print(f"wrote plots to {ASSETS}")


if __name__ == "__main__":
    main()
