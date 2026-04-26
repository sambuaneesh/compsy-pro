from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import pandas as pd
from scipy.stats import pearsonr, spearmanr

from css.common.config import load_yaml
from css.common.io import ensure_dir

SHIFT_METRICS = ["delta_cos", "delta_frob", "delta_l2", "delta_token_aligned"]


def _read_consistency(paths: list[str]) -> pd.DataFrame:
    frames = []
    for path in paths:
        if not Path(path).exists():
            continue
        frame = pd.read_csv(path)
        frame["source_path"] = path
        frames.append(frame)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def _summarize(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    return (
        df.groupby(["model", "phenomenon", "condition"], as_index=False)
        .agg(
            n=("pair_id", "size"),
            accuracy=("correct", "mean"),
            yes_rate=("predicted_label", lambda s: float((s == "yes").mean())),
            mean_margin_yes_minus_no=("margin_yes_minus_no", "mean"),
            median_margin_yes_minus_no=("margin_yes_minus_no", "median"),
        )
        .sort_values(["model", "phenomenon", "condition"])
    )


def _metric_frame(metrics_path: str | None) -> pd.DataFrame | None:
    if metrics_path is None:
        return None
    metrics = pd.read_csv(metrics_path)
    present = [metric for metric in SHIFT_METRICS if metric in metrics.columns]
    if not present:
        return None
    return (
        metrics.groupby(["model", "phenomenon", "pair_id"], as_index=False)[present]
        .mean()
        .rename(columns={metric: f"mean_{metric}" for metric in present})
    )


def _margin_correlations(df: pd.DataFrame, metrics: pd.DataFrame | None) -> pd.DataFrame:
    if df.empty or metrics is None:
        return pd.DataFrame()
    counterfactual = df[df["condition"] == "counterfactual"].copy()
    counterfactual["no_margin"] = -counterfactual["margin_yes_minus_no"]

    rows: list[dict[str, Any]] = []
    for output_model, output_frame in counterfactual.groupby("model"):
        merged = output_frame.merge(
            metrics,
            on=["phenomenon", "pair_id"],
            how="inner",
            suffixes=("_output", "_metric"),
        )
        if merged.empty:
            continue
        for metric_model, metric_frame in merged.groupby("model_metric"):
            for phenomenon, ph_frame in metric_frame.groupby("phenomenon"):
                for metric in SHIFT_METRICS:
                    column = f"mean_{metric}"
                    if column not in ph_frame.columns or ph_frame[column].nunique() < 2:
                        continue
                    if ph_frame["no_margin"].nunique() < 2:
                        continue
                    spearman = spearmanr(ph_frame[column], ph_frame["no_margin"])
                    pearson = pearsonr(ph_frame[column], ph_frame["no_margin"])
                    rows.append(
                        {
                            "output_model": output_model,
                            "metric_model": metric_model,
                            "phenomenon": phenomenon,
                            "metric": metric,
                            "n": len(ph_frame),
                            "spearman_r": spearman.statistic,
                            "spearman_p": spearman.pvalue,
                            "pearson_r": pearson.statistic,
                            "pearson_p": pearson.pvalue,
                        }
                    )
    return pd.DataFrame(rows).sort_values(["output_model", "metric_model", "phenomenon", "metric"])


def _write_report(path: Path, summary: pd.DataFrame, correlations: pd.DataFrame) -> None:
    ensure_dir(path.parent)
    lines = [
        "# Output-Level Counterfactual Consistency Summary\n\n",
        "This report evaluates whether a causal language model assigns higher forced-choice likelihood "
        "to `yes` for identical sentence controls and to `no` for counterfactual role-reversal or "
        "negation pairs. The experiment is a dataset-only behavioral diagnostic, not a human-alignment "
        "experiment.\n\n",
        "## Accuracy and Bias\n\n",
    ]
    if summary.empty:
        lines.append("No consistency rows were available.\n")
    else:
        lines.append(
            "| Model | Phenomenon | Condition | n | Accuracy | Yes-rate | Mean yes-minus-no margin |\n"
        )
        lines.append("| --- | --- | --- | ---: | ---: | ---: | ---: |\n")
        for _, row in summary.iterrows():
            lines.append(
                f"| {row['model']} | {row['phenomenon']} | {row['condition']} | "
                f"{int(row['n'])} | {row['accuracy']:.4f} | {row['yes_rate']:.4f} | "
                f"{row['mean_margin_yes_minus_no']:.4f} |\n"
            )

    lines.append("\n## CSS Shift Versus Output Discrimination\n\n")
    lines.append(
        "For counterfactual rows, `no_margin = score(no) - score(yes)`. Positive correlations mean "
        "larger representation shifts are associated with stronger output-level rejection of the "
        "counterfactual as meaning-preserving.\n\n"
    )
    if correlations.empty:
        lines.append("No metric-margin correlations were available for the supplied inputs.\n")
    else:
        lines.append("| Output model | Metric model | Phenomenon | Metric | n | Spearman r | p |\n")
        lines.append("| --- | --- | --- | --- | ---: | ---: | ---: |\n")
        for _, row in correlations.iterrows():
            lines.append(
                f"| {row['output_model']} | {row['metric_model']} | {row['phenomenon']} | "
                f"{row['metric']} | {int(row['n'])} | {row['spearman_r']:.4f} | "
                f"{row['spearman_p']:.3g} |\n"
            )

    path.write_text("".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize output-level consistency results.")
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    cfg = load_yaml(args.config)
    output_dir = ensure_dir(cfg.get("output_dir", "results/consistency/summary"))
    consistency = _read_consistency([str(path) for path in cfg["consistency_paths"]])
    summary = _summarize(consistency)
    metrics = _metric_frame(cfg.get("metrics_path"))
    correlations = _margin_correlations(consistency, metrics)

    summary_path = output_dir / "consistency_summary.csv"
    correlations_path = output_dir / "consistency_metric_correlations.csv"
    report_path = output_dir / "consistency_report.md"
    summary.to_csv(summary_path, index=False)
    correlations.to_csv(correlations_path, index=False)
    _write_report(report_path, summary, correlations)
    print(f"wrote {summary_path} rows={len(summary)}")
    print(f"wrote {correlations_path} rows={len(correlations)}")
    print(f"wrote {report_path}")


if __name__ == "__main__":
    main()
