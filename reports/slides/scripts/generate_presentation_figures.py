from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid")


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _load_pair_jsonl(path: str) -> pd.DataFrame:
    return pd.read_json(path, lines=True)


def make_dataset_counts(out_dir: Path) -> None:
    role = _load_pair_jsonl("data/css_pairs/role_1500.jsonl")
    neg = _load_pair_jsonl("data/css_pairs/neg_1500.jsonl")
    role["phenomenon"] = "Role Reversal"
    neg["phenomenon"] = "Negation"
    df = pd.concat([role, neg], ignore_index=True)

    total = df.groupby("phenomenon", as_index=False).size().rename(columns={"size": "pairs"})
    split = (
        df.groupby(["phenomenon", "split"], as_index=False)
        .size()
        .rename(columns={"size": "pairs"})
        .sort_values(["phenomenon", "split"])
    )

    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.2), gridspec_kw={"width_ratios": [1, 1.35]})
    ax1, ax2 = axes

    sns.barplot(
        data=total,
        x="phenomenon",
        y="pairs",
        hue="phenomenon",
        palette=["#22577A", "#38A3A5"],
        legend=False,
        ax=ax1,
    )
    ax1.set_ylim(0, 1700)
    ax1.set_ylabel("Counterfactual Pairs")
    ax1.set_xlabel("")
    ax1.set_title("Total by Phenomenon")
    for i, v in enumerate(total["pairs"]):
        ax1.text(i, v + 28, f"{int(v)}", ha="center", va="bottom", fontsize=10)

    sns.barplot(
        data=split,
        x="split",
        y="pairs",
        hue="phenomenon",
        palette=["#22577A", "#38A3A5"],
        ax=ax2,
    )
    ax2.set_ylabel("Pairs")
    ax2.set_xlabel("Split")
    ax2.set_title("Split-wise Composition")
    ax2.legend(title="phenomenon", loc="upper right")

    fig.suptitle("Dataset Composition (Role Reversal + Negation)", y=0.995)
    fig.tight_layout(rect=[0.0, 0.0, 1.0, 0.94])
    fig.savefig(out_dir / "dataset_counts.pdf")
    plt.close(fig)


def make_metric_means(out_dir: Path) -> None:
    metrics = pd.read_csv("results/metrics/layer_metrics_full.csv")
    metrics = metrics[metrics["phenomenon"].isin(["role_reversal", "negation"])].copy()
    metrics["phenomenon"] = metrics["phenomenon"].map(
        {"role_reversal": "Role Reversal", "negation": "Negation"}
    )

    raw = (
        metrics.groupby("phenomenon", as_index=False)[
            ["delta_cos", "delta_frob", "delta_l2", "delta_token_aligned"]
        ]
        .mean()
        .melt(id_vars=["phenomenon"], var_name="metric", value_name="mean_value")
    )
    raw["metric"] = raw["metric"].map(
        {
            "delta_cos": r"$\Delta_{cos}$",
            "delta_frob": r"$\Delta_{frob}$",
            "delta_l2": r"$\Delta_{L2}$",
            "delta_token_aligned": r"$\Delta_{token}$",
        }
    )

    scaled = raw.copy()
    scaled["scaled_value"] = scaled.groupby("metric")["mean_value"].transform(
        lambda s: s / s.max() if s.max() != 0 else s
    )

    fig, axes = plt.subplots(
        1,
        3,
        figsize=(13.0, 4.4),
        gridspec_kw={"width_ratios": [2.25, 1.0, 2.25]},
    )
    ax_raw_small = axes[0]
    ax_raw_l2 = axes[1]
    ax_scaled = axes[2]

    raw_small = raw[raw["metric"] != r"$\Delta_{L2}$"]
    raw_l2 = raw[raw["metric"] == r"$\Delta_{L2}$"]

    sns.barplot(
        data=raw_small,
        x="metric",
        y="mean_value",
        hue="phenomenon",
        palette=["#2A9D8F", "#E76F51"],
        ax=ax_raw_small,
    )
    ax_raw_small.set_title("Raw Means: Cosine / Frobenius / Token-Aligned")
    ax_raw_small.set_xlabel("")
    ax_raw_small.set_ylabel("Mean Shift")
    ax_raw_small.legend(title="phenomenon", loc="upper left")

    sns.barplot(
        data=raw_l2,
        x="metric",
        y="mean_value",
        hue="phenomenon",
        palette=["#2A9D8F", "#E76F51"],
        ax=ax_raw_l2,
    )
    ax_raw_l2.set_title("Raw Means: L2")
    ax_raw_l2.set_xlabel("")
    ax_raw_l2.set_ylabel("Mean Shift")
    ax_raw_l2.legend_.remove()

    sns.barplot(
        data=scaled,
        x="metric",
        y="scaled_value",
        hue="phenomenon",
        palette=["#2A9D8F", "#E76F51"],
        ax=ax_scaled,
    )
    ax_scaled.set_ylim(0, 1.08)
    ax_scaled.set_title("Within-Metric Normalized Means")
    ax_scaled.set_xlabel("")
    ax_scaled.set_ylabel("Relative Mean Shift")
    ax_scaled.legend(title="phenomenon", loc="upper right")

    fig.suptitle("Mean Shift Magnitude by Metric and Phenomenon", y=0.995)
    fig.tight_layout(rect=[0.0, 0.0, 1.0, 0.96])
    fig.savefig(out_dir / "metric_means_by_phenomenon.pdf")
    plt.close(fig)


def make_layer_correlation_by_phenomenon(out_dir: Path) -> None:
    corr = pd.read_csv("results/stats/full/correlations.csv")
    corr = corr[corr["metric"].isin(["delta_cos", "delta_frob"])].copy()
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

    model_order = ["BERT", "GPT-2", "RoBERTa"]
    phen_order = ["Negation", "Role Reversal"]
    metric_colors = {"delta_cos": "#4C72B0", "delta_frob": "#DD8452"}

    fig, axes = plt.subplots(2, 3, figsize=(12.8, 6.1), sharex=True, sharey=True)
    for r, phen in enumerate(phen_order):
        for c, model in enumerate(model_order):
            ax = axes[r, c]
            sub = corr[(corr["phenomenon"] == phen) & (corr["model"] == model)].sort_values("layer")
            for metric in ["delta_cos", "delta_frob"]:
                sm = sub[sub["metric"] == metric]
                ax.plot(
                    sm["layer"],
                    sm["spearman_rho"],
                    marker="o",
                    label=metric,
                    color=metric_colors[metric],
                )
            ax.set_title(f"{phen} | {model}", fontsize=12)
            ax.grid(True, alpha=0.25)
            if c == 0:
                ax.set_ylabel("Spearman rho")
            if r == 1:
                ax.set_xlabel("Layer")

    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(
        handles, labels, title="metric", loc="upper center", bbox_to_anchor=(0.5, 0.985), ncol=2
    )
    fig.suptitle("Layer-wise Correlation Curves by Phenomenon (with surprisal)", y=0.995)
    fig.tight_layout(rect=[0.0, 0.0, 1.0, 0.90])
    fig.savefig(out_dir / "layer_correlation_curves.pdf")
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
    corr["sig"] = corr["spearman_q"] < 0.05

    fig, axes = plt.subplots(1, 2, figsize=(11.8, 4.6), sharey=True)
    for ax, ph in zip(axes, ["Role Reversal", "Negation"], strict=True):
        sub = corr[corr["phenomenon"] == ph]
        heat = sub.pivot(index="model", columns="layer", values="spearman_rho")
        sig = sub.pivot(index="model", columns="layer", values="sig").fillna(False)
        sns.heatmap(
            heat,
            cmap="RdBu_r",
            center=0.0,
            cbar=(ph == "Negation"),
            ax=ax,
            linewidths=0.2,
            linecolor="white",
        )
        # Overlay significance marker for q<0.05.
        for yi, model in enumerate(heat.index):
            for xi, layer in enumerate(heat.columns):
                if bool(sig.loc[model, layer]):
                    ax.text(
                        xi + 0.5, yi + 0.5, "•", ha="center", va="center", color="black", fontsize=8
                    )

        ax.set_title(ph)
        ax.set_xlabel("Layer")
        ax.set_ylabel("" if ph == "Negation" else "Model")

    fig.suptitle("Layer-wise Spearman Correlation for Frobenius Shift (dot = FDR < 0.05)", y=0.98)
    fig.tight_layout(rect=[0.0, 0.0, 1.0, 0.93])
    fig.savefig(out_dir / "frob_layer_heatmap.pdf", bbox_inches="tight")
    plt.close(fig)


def make_probe_selectivity_with_ci(out_dir: Path) -> None:
    probe = pd.read_csv("results/probes/probe_results_full.csv")
    probe = probe[probe["phenomenon"].isin(["role_reversal", "negation"])].copy()
    probe["model"] = probe["model"].map(
        {
            "bert-base-uncased": "BERT",
            "roberta-base": "RoBERTa",
            "gpt2": "GPT-2",
        }
    )
    probe["phenomenon"] = probe["phenomenon"].map(
        {"role_reversal": "Role Reversal", "negation": "Negation"}
    )

    summary = (
        probe.groupby(["model", "phenomenon", "layer"], as_index=False)["selectivity"]
        .agg(
            mean="mean",
            lo=lambda s: np.quantile(s, 0.025),
            hi=lambda s: np.quantile(s, 0.975),
        )
        .sort_values(["model", "phenomenon", "layer"])
    )

    fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.1), sharey=True)
    model_order = ["BERT", "GPT-2", "RoBERTa"]
    color_map = {"Negation": "#4C72B0", "Role Reversal": "#DD8452"}
    for ax, model in zip(axes, model_order, strict=True):
        sub_m = summary[summary["model"] == model]
        for ph in ["Negation", "Role Reversal"]:
            sub = sub_m[sub_m["phenomenon"] == ph]
            ax.plot(sub["layer"], sub["mean"], marker="o", label=ph, color=color_map[ph])
            ax.fill_between(sub["layer"], sub["lo"], sub["hi"], alpha=0.18, color=color_map[ph])
        ax.set_title(model)
        ax.set_xlabel("Layer")
        ax.grid(True, alpha=0.25)
    axes[0].set_ylabel("Probe selectivity")
    axes[-1].legend(title="phenomenon", loc="lower right")

    fig.suptitle("Probe Selectivity Across Layers with Seed-Level 95% Intervals", y=0.995)
    fig.tight_layout(rect=[0.0, 0.0, 1.0, 0.92])
    fig.savefig(out_dir / "probe_selectivity_curves.pdf")
    plt.close(fig)


def make_surprisal_vs_shift(out_dir: Path) -> None:
    metrics = pd.read_csv("results/metrics/layer_metrics_full.csv")
    surprisal = pd.read_csv("results/surprisal/gpt2_surprisal_full.csv")
    merged = metrics.merge(
        surprisal[["pair_id", "phenomenon", "abs_delta_avg_surprisal"]],
        on=["pair_id", "phenomenon"],
        how="inner",
    )
    merged = merged.groupby(["model", "phenomenon", "pair_id"], as_index=False)[
        ["delta_frob", "abs_delta_avg_surprisal"]
    ].mean()
    merged["phenomenon"] = merged["phenomenon"].map(
        {"role_reversal": "Role Reversal", "negation": "Negation"}
    )

    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.3), sharey=True)
    for ax, ph in zip(axes, ["Role Reversal", "Negation"], strict=True):
        sub = merged[merged["phenomenon"] == ph]
        hb = ax.hexbin(
            sub["delta_frob"],
            sub["abs_delta_avg_surprisal"],
            gridsize=35,
            cmap="Blues",
            mincnt=1,
            linewidths=0.0,
        )
        sns.regplot(
            data=sub,
            x="delta_frob",
            y="abs_delta_avg_surprisal",
            scatter=False,
            color="#D62728",
            line_kws={"linewidth": 2.0},
            ax=ax,
        )
        ax.set_title(ph)
        ax.set_xlabel("Mean delta_frob")
        ax.grid(True, alpha=0.2)
    axes[0].set_ylabel("|delta avg surprisal| (GPT-2)")
    cb = fig.colorbar(hb, ax=axes.ravel().tolist(), shrink=0.88)
    cb.set_label("Pair density")
    fig.suptitle("Frobenius Shift vs Surprisal Delta (density + per-phenomenon trend)", y=0.995)
    fig.subplots_adjust(top=0.82, wspace=0.18, right=0.92)
    fig.savefig(out_dir / "surprisal_vs_shift.pdf")
    plt.close(fig)


def make_h2_distribution(out_dir: Path) -> None:
    h2 = pd.read_csv("results/stats/full/h2_incremental.csv")
    pos = int((h2["delta_adj_r2"] > 0).sum())
    total = len(h2)
    mean_gain = float(h2["delta_adj_r2"].mean())
    median_gain = float(h2["delta_adj_r2"].median())

    fig, ax = plt.subplots(figsize=(7.6, 4.0))
    sns.histplot(h2["delta_adj_r2"], bins=20, kde=True, color="#1D3557", ax=ax)
    ax.axvline(0.0, color="black", linestyle="--", linewidth=1.2)
    ax.set_xlabel(r"$\Delta$ Adjusted $R^2$ (adding Frobenius)")
    ax.set_ylabel("Count")
    ax.set_title("Incremental Value Distribution of Frobenius Shift")
    ax.text(
        0.98,
        0.95,
        f"Positive cells: {pos}/{total}\nMean: {mean_gain:.4f}\nMedian: {median_gain:.4f}",
        ha="right",
        va="top",
        transform=ax.transAxes,
        fontsize=10,
        bbox={"facecolor": "white", "alpha": 0.85, "edgecolor": "#BBBBBB"},
    )
    fig.tight_layout()
    fig.savefig(out_dir / "h2_delta_adj_r2_distribution.pdf")
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
    rq1["pos_rate"] = rq1["pos_sig_cells"] / rq1["total_cells"]
    rq1["neg_rate"] = rq1["neg_sig_cells"] / rq1["total_cells"]

    fig, ax = plt.subplots(figsize=(8.5, 4.2))
    ax.bar(rq1["metric"], rq1["pos_rate"], color="#2A9D8F", label="Positive significant")
    ax.bar(
        rq1["metric"],
        rq1["neg_rate"],
        bottom=rq1["pos_rate"],
        color="#E76F51",
        label="Negative significant",
    )
    ax.set_ylim(0, 1.0)
    ax.set_xlabel("Metric")
    ax.set_ylabel("Significant Fraction")
    ax.set_title("RQ1: Significant Fraction by Metric (FDR < 0.05)")
    ax.legend(loc="upper right")

    for i, (_, row) in enumerate(rq1.iterrows()):
        ax.text(
            i,
            row["pos_rate"] + row["neg_rate"] + 0.02,
            f"+{int(row['pos_sig_cells'])} / -{int(row['neg_sig_cells'])}",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    fig.tight_layout()
    fig.savefig(out_dir / "rq1_significance_profile.pdf", bbox_inches="tight")
    plt.close(fig)


def make_rq2_heatmap(out_dir: Path) -> None:
    rq2 = pd.read_csv("results/tables/rq2_incremental_by_group.csv")
    rq2["model"] = rq2["model"].map(
        {
            "bert-base-uncased": "BERT",
            "roberta-base": "RoBERTa",
            "gpt2": "GPT-2",
        }
    )
    rq2["phenomenon"] = rq2["phenomenon"].map(
        {"role_reversal": "Role Reversal", "negation": "Negation"}
    )

    rate = rq2.pivot(index="model", columns="phenomenon", values="positive_rate")
    gain = rq2.pivot(index="model", columns="phenomenon", values="mean_delta_adj_r2")

    fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.3))
    sns.heatmap(
        rate,
        annot=True,
        fmt=".2f",
        cmap="YlGnBu",
        vmin=0.0,
        vmax=1.0,
        cbar_kws={"label": "Positive delta_adj_r2 rate"},
        ax=axes[0],
    )
    axes[0].set_title("Positive-Rate Heatmap")
    axes[0].set_xlabel("Phenomenon")
    axes[0].set_ylabel("Model")

    sns.heatmap(
        gain,
        annot=True,
        fmt=".3f",
        cmap="magma",
        cbar_kws={"label": "Mean delta_adj_r2"},
        ax=axes[1],
    )
    axes[1].set_title("Mean Gain Heatmap")
    axes[1].set_xlabel("Phenomenon")
    axes[1].set_ylabel("")

    fig.suptitle("RQ2: Frobenius Complementarity by Model and Phenomenon", y=0.995)
    fig.tight_layout(rect=[0.0, 0.0, 1.0, 0.91])
    fig.savefig(out_dir / "rq2_positive_rate_heatmap.pdf")
    plt.close(fig)


def make_rq3_interaction(out_dir: Path) -> None:
    corr = pd.read_csv("results/stats/full/correlations.csv")
    probe = pd.read_csv("results/tables/rq3_probe_selectivity_by_layer.csv")

    metrics = ["delta_cos", "delta_frob", "delta_l2", "delta_token_aligned"]
    rows = []
    rng = np.random.default_rng(13)
    n_boot = 1500

    for metric in metrics:
        frame = corr[corr["metric"] == metric][
            ["model", "phenomenon", "layer", "spearman_rho"]
        ].merge(
            probe[["model", "phenomenon", "layer", "selectivity"]],
            on=["model", "phenomenon", "layer"],
            how="inner",
        )
        x = frame["selectivity"].to_numpy(float)
        y = frame["spearman_rho"].to_numpy(float)
        n = len(frame)

        for corr_type, fn in [
            ("Spearman", lambda a, b: pd.Series(a).corr(pd.Series(b), method="spearman")),
            ("Pearson", lambda a, b: pd.Series(a).corr(pd.Series(b), method="pearson")),
        ]:
            obs = float(fn(x, y))
            boot_vals = []
            for _ in range(n_boot):
                idx = rng.integers(0, n, size=n)
                boot_vals.append(float(fn(x[idx], y[idx])))
            lo = float(np.quantile(boot_vals, 0.025))
            hi = float(np.quantile(boot_vals, 0.975))
            rows.append(
                {
                    "metric": metric,
                    "corr_type": corr_type,
                    "value": obs,
                    "ci_lo": lo,
                    "ci_hi": hi,
                }
            )

    rq3 = pd.DataFrame(rows)
    metric_labels = {
        "delta_cos": r"$\Delta_{cos}$",
        "delta_frob": r"$\Delta_{frob}$",
        "delta_l2": r"$\Delta_{L2}$",
        "delta_token_aligned": r"$\Delta_{token}$",
    }
    rq3["metric_label"] = rq3["metric"].map(metric_labels)

    order = [metric_labels[m] for m in metrics]
    fig, ax = plt.subplots(figsize=(8.8, 4.4))
    sns.barplot(
        data=rq3,
        x="metric_label",
        y="value",
        hue="corr_type",
        order=order,
        ax=ax,
    )
    ax.axhline(0.0, color="black", linewidth=1.0)
    ax.set_xlabel("Metric")
    ax.set_ylabel("Correlation")
    ax.set_title("RQ3: Probe Selectivity vs Metric-Correlation Coupling (95% bootstrap CI)")

    # Add CI error bars on top of bars.
    for patch, (_, row) in zip(ax.patches, rq3.iterrows(), strict=False):
        x = patch.get_x() + patch.get_width() / 2
        y = row["value"]
        yerr = np.array([[y - row["ci_lo"]], [row["ci_hi"] - y]])
        ax.errorbar(x, y, yerr=yerr, fmt="none", ecolor="black", elinewidth=1.0, capsize=3)

    fig.tight_layout()
    fig.savefig(out_dir / "rq3_interaction_bars.pdf")
    plt.close(fig)


def main() -> None:
    out_dir = Path("results/figures")
    _ensure_dir(out_dir)
    make_dataset_counts(out_dir)
    make_metric_means(out_dir)
    make_layer_correlation_by_phenomenon(out_dir)
    make_frob_heatmap(out_dir)
    make_probe_selectivity_with_ci(out_dir)
    make_surprisal_vs_shift(out_dir)
    make_h2_distribution(out_dir)
    make_rq1_significance_profile(out_dir)
    make_rq2_heatmap(out_dir)
    make_rq3_interaction(out_dir)
    print(f"Wrote presentation figures to {out_dir}")


if __name__ == "__main__":
    main()
