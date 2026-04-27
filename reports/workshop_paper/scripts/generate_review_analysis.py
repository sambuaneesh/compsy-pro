from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm, pearsonr, spearmanr
from sklearn.linear_model import LinearRegression

OUT_DIR = Path("reports/workshop_paper/tables")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def _rank_residual(values: pd.Series, controls: pd.DataFrame) -> np.ndarray:
    y = values.rank(method="average").to_numpy(dtype=float)
    x = controls.rank(method="average").to_numpy(dtype=float)
    reg = LinearRegression().fit(x, y)
    return y - reg.predict(x)


def _safe_corr(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    if len(x) < 3 or np.allclose(x, x[0]) or np.allclose(y, y[0]):
        return float("nan"), float("nan")
    corr = pearsonr(x, y)
    return float(corr.statistic), float(corr.pvalue)


def partial_surface_control() -> pd.DataFrame:
    metrics = pd.read_csv("results/metrics/layer_metrics_full.csv")
    surprisal = pd.read_csv("results/surprisal/gpt2_surprisal_full.csv")[
        ["pair_id", "phenomenon", "abs_delta_avg_surprisal"]
    ]
    df = metrics.merge(surprisal, on=["pair_id", "phenomenon"], how="inner")
    df["abs_length_delta"] = df["length_delta"].abs()

    control_cols = ["lexical_jaccard", "abs_length_delta", "edit_distance"]
    rows = []
    for (phenomenon, model, layer, metric), group in df.groupby(
        ["phenomenon", "model", "layer", "pooling"]
    ):
        if metric != "mean_non_special":
            continue
        for shift in ["delta_cos", "delta_frob", "delta_l2", "delta_token_aligned"]:
            controls = group[control_cols]
            raw = spearmanr(group[shift], group["abs_delta_avg_surprisal"])
            x_res = _rank_residual(group[shift], controls)
            y_res = _rank_residual(group["abs_delta_avg_surprisal"], controls)
            partial_r, partial_p = _safe_corr(x_res, y_res)
            rows.append(
                {
                    "phenomenon": phenomenon,
                    "model": model,
                    "layer": int(layer),
                    "metric": shift,
                    "n": len(group),
                    "raw_spearman": float(raw.statistic),
                    "raw_p": float(raw.pvalue),
                    "surface_controlled_spearman": partial_r,
                    "surface_controlled_p": partial_p,
                }
            )
    out = pd.DataFrame(rows).sort_values(["phenomenon", "model", "metric", "layer"])
    out.to_csv(OUT_DIR / "surface_controlled_correlations.csv", index=False)

    summary = (
        out.groupby(["phenomenon", "metric"], as_index=False)
        .agg(
            mean_raw_spearman=("raw_spearman", "mean"),
            mean_surface_controlled_spearman=("surface_controlled_spearman", "mean"),
            positive_surface_cells=("surface_controlled_spearman", lambda s: int((s > 0).sum())),
            cells=("surface_controlled_spearman", "size"),
        )
        .sort_values(["phenomenon", "metric"])
    )
    summary.to_csv(OUT_DIR / "surface_controlled_summary.csv", index=False)
    return summary


def surface_correlations() -> pd.DataFrame:
    metrics = pd.read_csv("results/metrics/layer_metrics_full.csv")
    metrics["abs_length_delta"] = metrics["length_delta"].abs()
    rows = []
    for (phenomenon, model, layer), group in metrics.groupby(["phenomenon", "model", "layer"]):
        for control in ["lexical_jaccard", "abs_length_delta", "edit_distance"]:
            corr = spearmanr(group["delta_frob"], group[control])
            rows.append(
                {
                    "phenomenon": phenomenon,
                    "model": model,
                    "layer": int(layer),
                    "control": control,
                    "spearman": float(corr.statistic),
                    "p": float(corr.pvalue),
                }
            )
    out = pd.DataFrame(rows).sort_values(["phenomenon", "model", "control", "layer"])
    out.to_csv(OUT_DIR / "frob_surface_correlations.csv", index=False)
    summary = (
        out.groupby(["phenomenon", "control"], as_index=False)
        .agg(
            mean_spearman=("spearman", "mean"),
            max_abs_spearman=("spearman", lambda s: float(s.abs().max())),
        )
        .sort_values(["phenomenon", "control"])
    )
    summary.to_csv(OUT_DIR / "frob_surface_correlation_summary.csv", index=False)
    return summary


def output_accuracy_ci() -> pd.DataFrame:
    summary = pd.read_csv("results/consistency/summary/consistency_summary.csv")
    z = norm.ppf(0.975)
    rows = []
    for _, row in summary.iterrows():
        n = int(row["n"])
        p = float(row["accuracy"])
        denom = 1.0 + z**2 / n
        center = (p + z**2 / (2 * n)) / denom
        half = z * np.sqrt((p * (1 - p) / n) + (z**2 / (4 * n**2))) / denom
        out = row.to_dict()
        out["accuracy_ci_low"] = float(max(0.0, center - half))
        out["accuracy_ci_high"] = float(min(1.0, center + half))
        rows.append(out)
    out_df = pd.DataFrame(rows)
    out_df.to_csv(OUT_DIR / "output_consistency_wilson_ci.csv", index=False)
    return out_df


def reproducibility_snapshot() -> None:
    manifest = json.loads(
        Path("results/data_validation/external_dataset_manifest.json").read_text()
    )
    snapshot = {
        "project_git_commit": _read_cmd("git rev-parse HEAD"),
        "external_dataset_git_commit": _read_cmd(
            "git -C data/external/extending_psycholinguistic_dataset rev-parse HEAD"
        ),
        "role_source_sha256": manifest["role_source_sha256"],
        "negation_source_sha256": manifest["negation_source_sha256"],
        "seed": 13,
        "baseline_models": ["bert-base-uncased", "roberta-base", "gpt2"],
        "modern_models": ["mistralai/Mistral-7B-Instruct-v0.3", "google/gemma-3-4b-it"],
    }
    Path(OUT_DIR / "reproducibility_snapshot.json").write_text(
        json.dumps(snapshot, indent=2) + "\n", encoding="utf-8"
    )


def _read_cmd(cmd: str) -> str:
    import subprocess

    return subprocess.check_output(cmd, shell=True, text=True).strip()


def main() -> None:
    sctrl = partial_surface_control()
    fsurf = surface_correlations()
    ci = output_accuracy_ci()
    reproducibility_snapshot()
    print("surface-controlled summary")
    print(sctrl.to_string(index=False))
    print("frobenius surface correlation summary")
    print(fsurf.to_string(index=False))
    print("output CI rows", len(ci))


if __name__ == "__main__":
    main()
