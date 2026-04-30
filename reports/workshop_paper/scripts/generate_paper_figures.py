from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

OUT_DIR = Path("reports/workshop_paper/figures")
OUT_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams.update(
    {
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
    }
)
sns.set_theme(style="whitegrid", context="paper", font_scale=0.9)


def savefig(fig: plt.Figure, name: str) -> None:
    fig.tight_layout(pad=0.35)
    fig.savefig(OUT_DIR / name, bbox_inches="tight")
    plt.close(fig)


def plot_consistency() -> None:
    df = pd.read_csv("results/consistency/summary/consistency_summary.csv")
    df = df[
        df["model"].isin(["gpt2", "mistralai/Mistral-7B-Instruct-v0.3", "google/gemma-3-4b-it"])
    ]
    df["model_label"] = df["model"].map(
        {
            "gpt2": "GPT-2",
            "mistralai/Mistral-7B-Instruct-v0.3": "Mistral-7B-Inst.",
            "google/gemma-3-4b-it": "Gemma-3-4B-IT",
        }
    )
    df["phenomenon"] = df["phenomenon"].map(
        {"role_reversal": "Role reversal", "negation": "Negation"}
    )
    df["condition"] = df["condition"].map(
        {"identity_control": "Identity control", "counterfactual": "Counterfactual rejection"}
    )

    fig, axes = plt.subplots(1, 2, figsize=(6.9, 2.35), sharey=True)
    for ax, condition in zip(axes, ["Identity control", "Counterfactual rejection"], strict=True):
        sub = df[df["condition"] == condition].copy()
        sns.barplot(
            data=sub,
            x="model_label",
            y="accuracy",
            hue="phenomenon",
            palette=["#2A9D8F", "#E76F51"],
            ax=ax,
        )
        ax.set_title(condition)
        ax.set_xlabel("")
        ax.set_ylabel("Accuracy" if condition == "Identity control" else "")
        ax.set_ylim(0, 1.08)
        ax.tick_params(axis="x", rotation=20)
        ax.legend_.remove()
        for container in ax.containers:
            ax.bar_label(container, fmt="%.2f", fontsize=6, padding=1)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="lower center",
        ncol=2,
        frameon=False,
        bbox_to_anchor=(0.5, -0.18),
    )
    savefig(fig, "output_consistency_accuracy.pdf")


def plot_modern_decoder_frob_curves() -> None:
    frames = []
    for label, path in [
        ("Mistral-7B-Inst.", "results/stats/modern_mistral_7b/correlations.csv"),
        ("Gemma-3-4B-IT", "results/stats/modern_gemma3_4b/correlations.csv"),
    ]:
        df = pd.read_csv(path)
        df = df[df["metric"] == "delta_frob"].copy()
        df["model_label"] = label
        frames.append(df)
    corr = pd.concat(frames, ignore_index=True)
    corr["phenomenon"] = corr["phenomenon"].map(
        {"role_reversal": "Role reversal", "negation": "Negation"}
    )

    fig, axes = plt.subplots(1, 2, figsize=(6.9, 2.35), sharey=True)
    for ax, phen in zip(axes, ["Role reversal", "Negation"], strict=True):
        sub = corr[corr["phenomenon"] == phen].sort_values("layer")
        sns.lineplot(
            data=sub,
            x="layer",
            y="spearman_rho",
            hue="model_label",
            marker="o",
            linewidth=1.5,
            markersize=4,
            palette=["#4C72B0", "#DD8452"],
            ax=ax,
        )
        ax.axhline(0.0, color="black", linewidth=0.7, alpha=0.6)
        ax.set_title(phen)
        ax.set_xlabel("Layer")
        ax.set_ylabel(r"Spearman $\rho$" if phen == "Role reversal" else "")
        ax.legend_.remove()

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="lower center",
        ncol=2,
        frameon=False,
        bbox_to_anchor=(0.5, -0.18),
    )
    savefig(fig, "modern_decoder_frob_curves.pdf")


def plot_incremental_comparison() -> None:
    rows = []
    for label, path in [
        ("Baselines", "results/stats/full/h2_incremental.csv"),
        ("Mistral", "results/stats/modern_mistral_7b/h2_incremental.csv"),
        ("Gemma", "results/stats/modern_gemma3_4b/h2_incremental.csv"),
    ]:
        df = pd.read_csv(path)
        rows.append(
            {
                "group": label,
                "cells": len(df),
                "positive_cells": int((df["delta_adj_r2"] > 0).sum()),
                "mean_delta_adj_r2": float(df["delta_adj_r2"].mean()),
            }
        )
    out = pd.DataFrame(rows)
    out["positive_rate"] = out["positive_cells"] / out["cells"]
    out.to_csv(OUT_DIR / "frob_incremental_comparison.csv", index=False)

    fig, axes = plt.subplots(1, 2, figsize=(6.9, 2.35))
    sns.barplot(data=out, x="group", y="positive_rate", color="#2A9D8F", ax=axes[0])
    axes[0].set_ylim(0, 1.05)
    axes[0].set_xlabel("")
    axes[0].set_ylabel("Fraction positive")
    axes[0].set_title(r"Cells with $\Delta$adj-$R^2 > 0$")
    for i, row in out.iterrows():
        axes[0].text(
            i,
            row["positive_rate"] + 0.03,
            f"{row['positive_cells']}/{row['cells']}",
            ha="center",
            fontsize=7,
        )

    sns.barplot(data=out, x="group", y="mean_delta_adj_r2", color="#DD8452", ax=axes[1])
    axes[1].set_xlabel("")
    axes[1].set_ylabel(r"Mean $\Delta$adj-$R^2$")
    axes[1].set_title("Mean incremental gain")
    savefig(fig, "frob_incremental_comparison.pdf")


def plot_baseline_heatmap_copy() -> None:
    corr = pd.read_csv("results/stats/full/correlations.csv")
    corr = corr[corr["metric"] == "delta_frob"].copy()
    corr["model_label"] = corr["model"].map(
        {"bert-base-uncased": "BERT", "roberta-base": "RoBERTa", "gpt2": "GPT-2"}
    )
    corr["phenomenon"] = corr["phenomenon"].map(
        {"role_reversal": "Role reversal", "negation": "Negation"}
    )
    fig, axes = plt.subplots(1, 2, figsize=(6.9, 2.35), sharey=True)
    for ax, phenomenon in zip(axes, ["Role reversal", "Negation"], strict=True):
        sub = corr[corr["phenomenon"] == phenomenon].pivot(
            index="model_label", columns="layer", values="spearman_rho"
        )
        sub = sub.reindex(["BERT", "RoBERTa", "GPT-2"])
        sns.heatmap(
            sub,
            ax=ax,
            cmap="vlag",
            center=0,
            vmin=-0.15,
            vmax=0.38,
            cbar=phenomenon == "Negation",
            cbar_kws={"label": r"Spearman $\rho$", "shrink": 0.8},
            linewidths=0.2,
            linecolor="white",
        )
        ax.set_title(phenomenon)
        ax.set_xlabel("Layer")
        ax.set_ylabel("")
        ax.tick_params(axis="x", rotation=0, labelsize=6)
        ax.tick_params(axis="y", rotation=0)
    savefig(fig, "baseline_frob_layer_heatmap.pdf")


def main() -> None:
    plot_consistency()
    plot_modern_decoder_frob_curves()
    plot_incremental_comparison()
    plot_baseline_heatmap_copy()
    print(f"wrote paper figures to {OUT_DIR}")


if __name__ == "__main__":
    main()
