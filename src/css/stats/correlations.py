from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import pearsonr, spearmanr

from css.common.config import load_yaml
from css.common.io import ensure_dir
from css.stats.multiple_comparisons import benjamini_hochberg


def _bootstrap_corr(
    x: np.ndarray, y: np.ndarray, *, method: str, n_boot: int = 300, seed: int = 13
) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    vals = []
    n = len(x)
    for _ in range(n_boot):
        idx = rng.integers(0, n, size=n)
        xb = x[idx]
        yb = y[idx]
        if method == "spearman":
            corr, _ = spearmanr(xb, yb)
        else:
            corr, _ = pearsonr(xb, yb)
        vals.append(float(corr))
    return float(np.quantile(vals, 0.025)), float(np.quantile(vals, 0.975))


def _z(series: pd.Series) -> pd.Series:
    s = series.astype(float)
    std = s.std(ddof=0)
    if std == 0:
        return s * 0.0
    return (s - s.mean()) / std


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compute CSS pilot correlation and incremental-value stats."
    )
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    cfg = load_yaml(args.config)
    out_dir = Path(str(cfg["output_dir"]))
    ensure_dir(out_dir)

    metrics = pd.read_csv(cfg["metrics_path"])
    ann = pd.read_csv(cfg["annotation_agg_path"])
    surprisal = pd.read_csv(cfg["surprisal_path"])
    probes = pd.read_csv(cfg["probe_path"]) if Path(cfg["probe_path"]).exists() else pd.DataFrame()

    df = metrics.merge(
        ann[["pair_id", "phenomenon", "mean_change"]], on=["pair_id", "phenomenon"], how="inner"
    )
    df = df.merge(
        surprisal[["pair_id", "phenomenon", "abs_delta_avg_surprisal"]],
        on=["pair_id", "phenomenon"],
        how="left",
    )

    if not probes.empty:
        probe_conf = probes.groupby(["model", "phenomenon", "layer"], as_index=False)[
            "macro_f1"
        ].mean()
        probe_conf = probe_conf.rename(columns={"macro_f1": "probe_confidence_l"})
        df = df.merge(probe_conf, on=["model", "phenomenon", "layer"], how="left")
    else:
        df["probe_confidence_l"] = np.nan

    unique_keys = (
        df[["model", "phenomenon", "layer"]]
        .drop_duplicates()
        .sort_values(["model", "phenomenon", "layer"])
    )

    corr_rows: list[dict[str, Any]] = []
    for _, key_row in unique_keys.iterrows():
        model = str(key_row["model"])
        phenomenon = str(key_row["phenomenon"])
        layer = int(key_row["layer"])
        g = df[(df["model"] == model) & (df["phenomenon"] == phenomenon) & (df["layer"] == layer)]
        if len(g) < 20:
            continue
        y = g["mean_change"].to_numpy(dtype=float)
        for metric in ["delta_cos", "delta_frob", "delta_l2", "delta_token_aligned"]:
            x = g[metric].to_numpy(dtype=float)
            sp_rho, sp_p = spearmanr(x, y)
            pe_r, pe_p = pearsonr(x, y)
            sp_lo, sp_hi = _bootstrap_corr(x, y, method="spearman")
            pe_lo, pe_hi = _bootstrap_corr(x, y, method="pearson")
            corr_rows.append(
                {
                    "model": model,
                    "phenomenon": phenomenon,
                    "layer": int(layer),
                    "metric": metric,
                    "n": len(g),
                    "spearman_rho": float(sp_rho),
                    "spearman_p": float(sp_p),
                    "spearman_ci_lo": sp_lo,
                    "spearman_ci_hi": sp_hi,
                    "pearson_r": float(pe_r),
                    "pearson_p": float(pe_p),
                    "pearson_ci_lo": pe_lo,
                    "pearson_ci_hi": pe_hi,
                }
            )

    corr_df = pd.DataFrame(corr_rows)
    if corr_df.empty:
        raise SystemExit("No correlation rows generated")

    corr_df["spearman_q"] = benjamini_hochberg(corr_df["spearman_p"].tolist())
    corr_df["pearson_q"] = benjamini_hochberg(corr_df["pearson_p"].tolist())
    corr_df.to_csv(out_dir / "correlations.csv", index=False)
    corr_df[
        [
            "model",
            "phenomenon",
            "layer",
            "metric",
            "spearman_ci_lo",
            "spearman_ci_hi",
            "pearson_ci_lo",
            "pearson_ci_hi",
        ]
    ].to_csv(out_dir / "bootstrap_cis.csv", index=False)

    # H2 incremental value test: Delta_frob beyond Delta_cos + controls.
    h2_rows: list[dict[str, Any]] = []
    for _, key_row in unique_keys.iterrows():
        model = str(key_row["model"])
        phenomenon = str(key_row["phenomenon"])
        layer = int(key_row["layer"])
        g = df[(df["model"] == model) & (df["phenomenon"] == phenomenon) & (df["layer"] == layer)]
        if len(g) < 25:
            continue
        d = g.copy()
        d["z_y"] = _z(d["mean_change"])
        d["z_cos"] = _z(d["delta_cos"])
        d["z_frob"] = _z(d["delta_frob"])
        d["z_len"] = _z(d["length_delta"])
        d["z_jacc"] = _z(d["lexical_jaccard"])

        x1 = sm.add_constant(d[["z_cos", "z_len", "z_jacc"]], has_constant="add")
        m1 = sm.OLS(d["z_y"], x1).fit()
        x2 = sm.add_constant(d[["z_cos", "z_frob", "z_len", "z_jacc"]], has_constant="add")
        m2 = sm.OLS(d["z_y"], x2).fit()
        h2_rows.append(
            {
                "model": model,
                "phenomenon": phenomenon,
                "layer": int(layer),
                "n": len(d),
                "adj_r2_cos": float(m1.rsquared_adj),
                "adj_r2_cos_frob": float(m2.rsquared_adj),
                "delta_adj_r2": float(m2.rsquared_adj - m1.rsquared_adj),
                "beta_z_frob": float(m2.params.get("z_frob", np.nan)),
                "p_z_frob": float(m2.pvalues.get("z_frob", np.nan)),
            }
        )

    h2_df = pd.DataFrame(h2_rows)
    if not h2_df.empty:
        h2_df["p_z_frob_q"] = benjamini_hochberg(h2_df["p_z_frob"].fillna(1.0).tolist())
        h2_df.to_csv(out_dir / "h2_incremental.csv", index=False)

    # Hypothesis test digest.
    h1_support = corr_df[
        (corr_df["metric"].isin(["delta_cos", "delta_frob"])) & (corr_df["spearman_rho"] > 0)
    ].shape[0]
    h2_support = h2_df[h2_df["delta_adj_r2"] > 0].shape[0] if not h2_df.empty else 0
    h3_layers_var = corr_df.groupby(["model", "phenomenon", "metric"])["layer"].apply(
        lambda s: int(s.loc[s.idxmax()])
    )
    h4_corr = corr_df[corr_df["metric"] == "delta_frob"]["spearman_rho"].mean()

    with (out_dir / "hypothesis_tests.md").open("w", encoding="utf-8") as f:
        f.write("# Pilot Hypothesis Summary\n\n")
        f.write(f"- H1 positive-correlation cells (delta_cos/delta_frob): {h1_support}\n")
        f.write(f"- H2 cells with positive delta_adj_r2 when adding delta_frob: {h2_support}\n")
        f.write(
            f"- H3 indicative layer peaks by phenomenon/metric generated: {len(h3_layers_var)} groups\n"
        )
        f.write(
            f"- H4 mean spearman for delta_frob (context with surprisal separately modeled): {h4_corr:.4f}\n"
        )
        f.write(
            "- H5 controls partially covered in pilot (random-label probe controls, lexical covariates).\n"
        )

    print(f"wrote {out_dir / 'correlations.csv'} rows={len(corr_df)}")
    if not h2_df.empty:
        print(f"wrote {out_dir / 'h2_incremental.csv'} rows={len(h2_df)}")
    print(f"wrote {out_dir / 'hypothesis_tests.md'}")


if __name__ == "__main__":
    main()
