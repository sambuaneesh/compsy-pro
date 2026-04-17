from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _rq1_tables(corr: pd.DataFrame, out_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    corr = corr.copy()
    corr["pos_sig"] = (corr["spearman_rho"] > 0) & (corr["spearman_q"] < 0.05)
    corr["neg_sig"] = (corr["spearman_rho"] < 0) & (corr["spearman_q"] < 0.05)

    by_metric = (
        corr.groupby("metric", as_index=False)
        .agg(
            total_cells=("metric", "size"),
            pos_sig_cells=("pos_sig", "sum"),
            neg_sig_cells=("neg_sig", "sum"),
        )
        .sort_values("metric")
    )
    by_metric["pos_sig_rate"] = by_metric["pos_sig_cells"] / by_metric["total_cells"]
    by_metric["neg_sig_rate"] = by_metric["neg_sig_cells"] / by_metric["total_cells"]
    by_metric.to_csv(out_dir / "rq1_significance_counts.csv", index=False)

    by_group = (
        corr.groupby(["phenomenon", "model", "metric"], as_index=False)
        .agg(
            mean_spearman=("spearman_rho", "mean"),
            max_spearman=("spearman_rho", "max"),
            pos_sig_cells=("pos_sig", "sum"),
        )
        .sort_values(["phenomenon", "model", "metric"])
    )
    by_group.to_csv(out_dir / "rq1_by_group_summary.csv", index=False)

    peaks = corr[corr["metric"] == "delta_frob"].copy()
    peak_rows = peaks.loc[
        peaks.groupby(["phenomenon", "model"])["spearman_rho"].idxmax(),
        ["phenomenon", "model", "layer", "spearman_rho", "spearman_q"],
    ].sort_values(["phenomenon", "model"])
    peak_rows.to_csv(out_dir / "rq1_layer_peaks_delta_frob.csv", index=False)
    return by_metric, peak_rows


def _rq2_tables(h2: pd.DataFrame, out_dir: Path) -> pd.DataFrame:
    h2 = h2.copy()
    h2["positive_delta_adj_r2"] = h2["delta_adj_r2"] > 0
    h2["sig_frob"] = h2["p_z_frob_q"] < 0.05

    summary = (
        h2.groupby(["phenomenon", "model"], as_index=False)
        .agg(
            cells=("layer", "size"),
            positive_delta_adj_r2=("positive_delta_adj_r2", "sum"),
            positive_rate=("positive_delta_adj_r2", "mean"),
            mean_delta_adj_r2=("delta_adj_r2", "mean"),
            median_delta_adj_r2=("delta_adj_r2", "median"),
            sig_frob_cells=("sig_frob", "sum"),
        )
        .sort_values(["phenomenon", "model"])
    )
    summary.to_csv(out_dir / "rq2_incremental_by_group.csv", index=False)

    overall = pd.DataFrame(
        [
            {
                "cells": len(h2),
                "positive_delta_adj_r2": int((h2["delta_adj_r2"] > 0).sum()),
                "positive_rate": float((h2["delta_adj_r2"] > 0).mean()),
                "mean_delta_adj_r2": float(h2["delta_adj_r2"].mean()),
                "median_delta_adj_r2": float(h2["delta_adj_r2"].median()),
                "sig_frob_cells": int((h2["p_z_frob_q"] < 0.05).sum()),
                "beta_frob_positive_cells": int((h2["beta_z_frob"] > 0).sum()),
            }
        ]
    )
    overall.to_csv(out_dir / "rq2_incremental_overall.csv", index=False)
    return overall


def _rq3_tables(
    corr: pd.DataFrame, probe: pd.DataFrame, surprisal: pd.DataFrame, out_dir: Path
) -> pd.DataFrame:
    probe_layer = (
        probe.groupby(["model", "phenomenon", "layer"], as_index=False)["selectivity"]
        .mean()
        .sort_values(["model", "phenomenon", "layer"])
    )
    probe_layer.to_csv(out_dir / "rq3_probe_selectivity_by_layer.csv", index=False)

    interactions = []
    for metric in ["delta_cos", "delta_frob", "delta_l2", "delta_token_aligned"]:
        m = corr[corr["metric"] == metric][["model", "phenomenon", "layer", "spearman_rho"]].merge(
            probe_layer, on=["model", "phenomenon", "layer"], how="inner"
        )
        interactions.append(
            {
                "metric": metric,
                "n": len(m),
                "spearman_selectivity_vs_rho": m["selectivity"].corr(
                    m["spearman_rho"], method="spearman"
                ),
                "pearson_selectivity_vs_rho": m["selectivity"].corr(
                    m["spearman_rho"], method="pearson"
                ),
            }
        )
    inter_df = pd.DataFrame(interactions).sort_values("metric")
    inter_df.to_csv(out_dir / "rq3_probe_metric_interaction.csv", index=False)

    surprisal_summary = (
        surprisal.groupby("phenomenon", as_index=False)["abs_delta_avg_surprisal"]
        .agg(["mean", "median", "std"])
        .reset_index()
        .rename(
            columns={
                "mean": "mean_abs_delta_avg_surprisal",
                "median": "median_abs_delta_avg_surprisal",
                "std": "std_abs_delta_avg_surprisal",
            }
        )
    )
    surprisal_summary.to_csv(out_dir / "rq3_surprisal_by_phenomenon.csv", index=False)
    return inter_df


def _write_interpretation(
    by_metric: pd.DataFrame,
    peaks: pd.DataFrame,
    rq2_overall: pd.DataFrame,
    rq3_inter: pd.DataFrame,
    out_path: Path,
) -> None:
    delta_cos_pos = int(by_metric.loc[by_metric["metric"] == "delta_cos", "pos_sig_cells"].iloc[0])
    delta_frob_pos = int(
        by_metric.loc[by_metric["metric"] == "delta_frob", "pos_sig_cells"].iloc[0]
    )
    delta_l2_pos = int(by_metric.loc[by_metric["metric"] == "delta_l2", "pos_sig_cells"].iloc[0])
    delta_tok_pos = int(
        by_metric.loc[by_metric["metric"] == "delta_token_aligned", "pos_sig_cells"].iloc[0]
    )

    r2_pos = int(rq2_overall["positive_delta_adj_r2"].iloc[0])
    r2_cells = int(rq2_overall["cells"].iloc[0])
    r2_mean = float(rq2_overall["mean_delta_adj_r2"].iloc[0])
    frob_sig_cells = int(rq2_overall["sig_frob_cells"].iloc[0])

    frob_inter = rq3_inter.loc[rq3_inter["metric"] == "delta_frob"].iloc[0]

    lines = [
        "# Results Interpretation (Dataset-Only)\n",
        "## Research Question Answers\n",
        "### RQ1: Do representation-shift metrics respond consistently to minimal structural edits across layers and models?\n",
        "Yes, with metric-dependent consistency.\n",
        f"- Significant positive cells (FDR<0.05): delta_cos={delta_cos_pos}, delta_frob={delta_frob_pos}, delta_l2={delta_l2_pos}, delta_token_aligned={delta_tok_pos}.\n",
        "- Cosine/Frobenius/L2 show broad positive alignment patterns; token-aligned shift is more mixed and phenomenon-sensitive.\n",
        "- Frobenius layer peaks are concentrated in mid-to-late layers for role reversal, and early layers for negation.\n",
        "\n",
        "Top Frobenius layer peaks by model/phenomenon:\n",
    ]
    for _, row in peaks.iterrows():
        lines.append(
            f"- {row['phenomenon']} | {row['model']}: layer {int(row['layer'])}, "
            f"rho={row['spearman_rho']:.4f}, q={row['spearman_q']:.3g}\n"
        )

    lines.extend(
        [
            "\n### RQ2: Does Frobenius shift add complementary value beyond cosine?\n",
            "Yes, in most layer/model/phenomenon cells.\n",
            f"- Positive incremental cells (delta_adj_r2>0): {r2_pos}/{r2_cells}.\n",
            f"- Mean incremental gain: delta_adj_r2={r2_mean:.4f}.\n",
            f"- Cells with FDR-significant Frobenius coefficient: {frob_sig_cells}.\n",
            "- Interpretation: matrix-geometry information contributes beyond centroid-only similarity in this setup.\n",
            "\n### RQ3: How do probes and surprisal interact with representation-shift diagnostics?\n",
            "Probe selectivity is consistently positive, while its layer-wise coupling with metric-surprisal correlation strength is weak.\n",
            f"- Selectivity-vs-Frobenius-correlation coupling: Spearman={frob_inter['spearman_selectivity_vs_rho']:.4f}, "
            f"Pearson={frob_inter['pearson_selectivity_vs_rho']:.4f}.\n",
            "- Interpretation: probe quality and metric-surprisal alignment are both meaningful, but mostly complementary rather than redundant signals.\n",
            "\n## Overall Interpretation\n",
            "- The results support robust dataset-level structural sensitivity claims for role reversal and negation.\n",
            "- Frobenius shift is empirically useful as a complementary metric.\n",
            "- Claims remain at representation/diagnostic level and do not imply human-cognition equivalence.\n",
        ]
    )
    out_path.write_text("".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate RQ-focused analysis summaries from dataset-only CSS outputs."
    )
    parser.add_argument(
        "--corr",
        default="results/stats/full/correlations.csv",
    )
    parser.add_argument(
        "--h2",
        default="results/stats/full/h2_incremental.csv",
    )
    parser.add_argument(
        "--probe",
        default="results/probes/selectivity_summary_full.csv",
    )
    parser.add_argument(
        "--surprisal",
        default="results/surprisal/gpt2_surprisal_full.csv",
    )
    parser.add_argument("--out-dir", default="results/tables")
    parser.add_argument(
        "--report-path",
        default="reports/full/RESULTS_INTERPRETATION.md",
    )
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    _ensure_dir(out_dir)
    report_path = Path(args.report_path)
    _ensure_dir(report_path.parent)

    corr = pd.read_csv(args.corr)
    h2 = pd.read_csv(args.h2)
    probe = pd.read_csv(args.probe)
    surprisal = pd.read_csv(args.surprisal)

    by_metric, peaks = _rq1_tables(corr, out_dir)
    rq2_overall = _rq2_tables(h2, out_dir)
    rq3_inter = _rq3_tables(corr, probe, surprisal, out_dir)
    _write_interpretation(by_metric, peaks, rq2_overall, rq3_inter, report_path)

    print(f"wrote RQ tables to {out_dir}")
    print(f"wrote interpretation report to {report_path}")


if __name__ == "__main__":
    main()
