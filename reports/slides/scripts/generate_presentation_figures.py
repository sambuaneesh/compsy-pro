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
    small = summary[summary["metric"] != "delta_l2"].copy()
    large = summary[summary["metric"] == "delta_l2"].copy()

    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.2), gridspec_kw={"width_ratios": [3.5, 1.2]})
    ax_left, ax_right = axes

    sns.barplot(
        data=small,
        x="metric",
        y="mean_value",
        hue="phenomenon",
        palette=["#2A9D8F", "#E76F51"],
        ax=ax_left,
    )
    ax_left.set_xlabel("")
    ax_left.set_ylabel("Mean Shift")
    ax_left.set_title("Cosine / Frobenius / Token-Aligned")
    ax_left.tick_params(axis="x", rotation=12)
    ax_left.legend(title="phenomenon", loc="upper left")

    sns.barplot(
        data=large,
        x="metric",
        y="mean_value",
        hue="phenomenon",
        palette=["#2A9D8F", "#E76F51"],
        ax=ax_right,
    )
    ax_right.set_xlabel("")
    ax_right.set_ylabel("Mean Shift")
    ax_right.set_title("L2")
    ax_right.tick_params(axis="x", rotation=12)
    ax_right.legend_.remove()

    fig.suptitle("Mean Shift Magnitude by Metric and Phenomenon", y=0.99)
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
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.5), sharey=True)
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
    fig.suptitle("Layer-wise Spearman Correlation for Frobenius Shift", y=0.98)
    fig.tight_layout(rect=[0.0, 0.0, 1.0, 0.93])
    fig.savefig(out_dir / "frob_layer_heatmap.pdf", bbox_inches="tight")
    plt.close(fig)


def make_rq1_significance_profile(out_dir: Path) -> None:
    rq1 = pd.read_csv("results/tables/rq1_significance_counts.csv")
    rq1["metric"] = rq1["metric"].map(
        {
            "delta_cos": r"$\Delta_{cos}$",
            "delta_frob": r"$\Delta_{frob}$",
            "delta_l2": r"$\Delta_{L2}$",
            "delta_token_aligned": r"$\Delta_{token}$",
        }
    )
    fig, ax = plt.subplots(figsize=(8.5, 4.2))
    sns.barplot(
        data=rq1,
        x="metric",
        y="pos_sig_rate",
        color="#2A9D8F",
        ax=ax,
    )
    ax.set_ylim(0, 1.0)
    ax.set_xlabel("Metric")
    ax.set_ylabel("Positive Significant Rate")
    ax.set_title("RQ1: Fraction of Positive Significant Cells (FDR < 0.05)")
    for i, (_, row) in enumerate(rq1.iterrows()):
        ax.text(
            i,
            row["pos_sig_rate"] + 0.02,
            f"{int(row['pos_sig_cells'])}/{int(row['total_cells'])}",
            ha="center",
            va="bottom",
            fontsize=10,
        )
    fig.tight_layout()
    fig.savefig(out_dir / "rq1_significance_profile.pdf")
    plt.close(fig)


def make_rq2_heatmap(out_dir: Path) -> None:
    rq2 = pd.read_csv("results/tables/rq2_incremental_by_group.csv")
    pivot = rq2.pivot(index="model", columns="phenomenon", values="positive_rate")
    pivot = pivot.rename(
        index={
            "bert-base-uncased": "BERT",
            "roberta-base": "RoBERTa",
            "gpt2": "GPT-2",
        },
        columns={"role_reversal": "Role Reversal", "negation": "Negation"},
    )
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    sns.heatmap(
        pivot,
        annot=True,
        fmt=".2f",
        cmap="YlGnBu",
        vmin=0.0,
        vmax=1.0,
        cbar_kws={"label": "Positive Delta Adj-R2 Rate"},
        ax=ax,
    )
    ax.set_xlabel("Phenomenon")
    ax.set_ylabel("Model")
    ax.set_title("RQ2: Frobenius Complementarity by Model and Phenomenon")
    fig.tight_layout()
    fig.savefig(out_dir / "rq2_positive_rate_heatmap.pdf")
    plt.close(fig)


def make_rq3_interaction(out_dir: Path) -> None:
    rq3 = pd.read_csv("results/tables/rq3_probe_metric_interaction.csv")
    rq3 = rq3.melt(
        id_vars=["metric"],
        value_vars=["spearman_selectivity_vs_rho", "pearson_selectivity_vs_rho"],
        var_name="corr_type",
        value_name="value",
    )
    rq3["metric"] = rq3["metric"].map(
        {
            "delta_cos": r"$\Delta_{cos}$",
            "delta_frob": r"$\Delta_{frob}$",
            "delta_l2": r"$\Delta_{L2}$",
            "delta_token_aligned": r"$\Delta_{token}$",
        }
    )
    rq3["corr_type"] = rq3["corr_type"].map(
        {
            "spearman_selectivity_vs_rho": "Spearman",
            "pearson_selectivity_vs_rho": "Pearson",
        }
    )
    fig, ax = plt.subplots(figsize=(8.5, 4.2))
    sns.barplot(data=rq3, x="metric", y="value", hue="corr_type", ax=ax)
    ax.axhline(0.0, color="black", linewidth=1.0)
    ax.set_xlabel("Metric")
    ax.set_ylabel("Correlation")
    ax.set_title("RQ3: Probe Selectivity vs Metric-Correlation Coupling")
    fig.tight_layout()
    fig.savefig(out_dir / "rq3_interaction_bars.pdf")
    plt.close(fig)


def main() -> None:
    out_dir = Path("results/figures")
    _ensure_dir(out_dir)
    make_dataset_counts(out_dir)
    make_metric_means(out_dir)
    make_h2_distribution(out_dir)
    make_frob_heatmap(out_dir)
    make_rq1_significance_profile(out_dir)
    make_rq2_heatmap(out_dir)
    make_rq3_interaction(out_dir)
    print(f"Wrote presentation figures to {out_dir}")


if __name__ == "__main__":
    main()
