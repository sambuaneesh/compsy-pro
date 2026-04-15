from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid")


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def make_dataset_counts(out_dir: Path) -> None:
    df = pd.DataFrame(
        {
            "Phenomenon": ["Role Reversal", "Negation"],
            "Pairs": [1500, 1500],
        }
    )
    fig, ax = plt.subplots(figsize=(7.5, 4.0))
    sns.barplot(
        data=df,
        x="Phenomenon",
        y="Pairs",
        hue="Phenomenon",
        palette=["#22577A", "#38A3A5"],
        legend=False,
        ax=ax,
    )
    ax.set_ylim(0, 1700)
    ax.set_ylabel("Number of Counterfactual Pairs")
    ax.set_xlabel("")
    ax.set_title("Dataset Composition")
    for i, v in enumerate(df["Pairs"]):
        ax.text(i, v + 30, f"{v}", ha="center", va="bottom", fontsize=11)
    fig.tight_layout()
    fig.savefig(out_dir / "dataset_counts.pdf")
    plt.close(fig)


def make_metric_means(out_dir: Path) -> None:
    metrics = pd.read_csv("results/metrics/layer_metrics_full.csv")
    summary = (
        metrics.groupby("phenomenon", as_index=False)[
            ["delta_cos", "delta_frob", "delta_l2", "delta_token_aligned"]
        ]
        .mean()
        .melt(id_vars=["phenomenon"], var_name="metric", value_name="mean_value")
    )
    summary["phenomenon"] = summary["phenomenon"].map(
        {"role_reversal": "Role Reversal", "negation": "Negation"}
    )
    fig, ax = plt.subplots(figsize=(9, 4.2))
    sns.barplot(
        data=summary,
        x="metric",
        y="mean_value",
        hue="phenomenon",
        palette=["#2A9D8F", "#E76F51"],
        ax=ax,
    )
    ax.set_xlabel("")
    ax.set_ylabel("Mean Shift")
    ax.set_title("Mean Shift Magnitude by Metric and Phenomenon")
    ax.tick_params(axis="x", rotation=12)
    fig.tight_layout()
    fig.savefig(out_dir / "metric_means_by_phenomenon.pdf")
    plt.close(fig)


def make_h2_distribution(out_dir: Path) -> None:
    h2 = pd.read_csv("results/stats/full/h2_incremental.csv")
    fig, ax = plt.subplots(figsize=(7.6, 4.0))
    sns.histplot(h2["delta_adj_r2"], bins=20, kde=True, color="#1D3557", ax=ax)
    ax.axvline(0.0, color="black", linestyle="--", linewidth=1.2)
    ax.set_xlabel(r"$\Delta$ Adjusted $R^2$ (adding Frobenius)")
    ax.set_ylabel("Count")
    ax.set_title("Incremental Value Distribution of Frobenius Shift")
    fig.tight_layout()
    fig.savefig(out_dir / "h2_delta_adj_r2_distribution.pdf")
    plt.close(fig)


def make_frob_heatmap(out_dir: Path) -> None:
    corr = pd.read_csv("results/stats/full/correlations.csv")
    corr = corr[corr["metric"] == "delta_frob"].copy()
    corr["phenomenon"] = corr["phenomenon"].map(
        {"role_reversal": "Role Reversal", "negation": "Negation"}
    )
    corr["model"] = corr["model"].map(
        {
            "bert-base-uncased": "BERT",
            "roberta-base": "RoBERTa",
            "gpt2": "GPT-2",
        }
    )
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.2), sharey=True)
    for ax, ph in zip(axes, ["Role Reversal", "Negation"], strict=True):
        sub = corr[corr["phenomenon"] == ph].pivot(
            index="model", columns="layer", values="spearman_rho"
        )
        sns.heatmap(
            sub,
            cmap="RdBu_r",
            center=0.0,
            cbar=(ph == "Negation"),
            ax=ax,
            linewidths=0.2,
            linecolor="white",
        )
        ax.set_title(ph)
        ax.set_xlabel("Layer")
        ax.set_ylabel("" if ph == "Negation" else "Model")
    fig.suptitle("Layer-wise Spearman Correlation for Frobenius Shift", y=1.02)
    fig.tight_layout()
    fig.savefig(out_dir / "frob_layer_heatmap.pdf")
    plt.close(fig)


def main() -> None:
    out_dir = Path("results/figures")
    _ensure_dir(out_dir)
    make_dataset_counts(out_dir)
    make_metric_means(out_dir)
    make_h2_distribution(out_dir)
    make_frob_heatmap(out_dir)
    print(f"Wrote presentation figures to {out_dir}")


if __name__ == "__main__":
    main()
