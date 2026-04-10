from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

from css.common.config import load_yaml
from css.common.io import ensure_dir


def _z(series: pd.Series) -> pd.Series:
    s = series.astype(float)
    std = s.std(ddof=0)
    if std == 0:
        return s * 0.0
    return (s - s.mean()) / std


def _build_frame(cfg: dict[str, Any]) -> pd.DataFrame:
    metrics = pd.read_csv(cfg["metrics_path"])
    ann_raw = pd.read_csv(cfg["annotation_raw_path"])
    surprisal = pd.read_csv(cfg["surprisal_path"])
    probes = pd.read_csv(cfg["probe_path"]) if Path(cfg["probe_path"]).exists() else pd.DataFrame()

    df = metrics.merge(
        ann_raw[["pair_id", "phenomenon", "annotator_id", "human_change_0_5"]],
        on=["pair_id", "phenomenon"],
        how="inner",
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
    df["probe_confidence_l"] = df["probe_confidence_l"].fillna(0.0)
    df["abs_delta_avg_surprisal"] = df["abs_delta_avg_surprisal"].fillna(0.0)
    return df


def _fit_layer(df_layer: pd.DataFrame) -> dict[str, Any]:
    frame = df_layer.copy()
    frame["z_delta_cos"] = _z(frame["delta_cos"])
    frame["z_delta_frob"] = _z(frame["delta_frob"])
    frame["z_abs_surprisal"] = _z(frame["abs_delta_avg_surprisal"])
    frame["z_probe_conf"] = _z(frame["probe_confidence_l"])
    frame["z_len"] = _z(frame["length_delta"])
    frame["z_jacc"] = _z(frame["lexical_jaccard"])
    frame["human_change"] = frame["human_change_0_5"].astype(float)
    frame["pair_group"] = frame["pair_id"].astype(str)
    frame["annotator_group"] = frame["annotator_id"].astype(str)

    numeric_terms = [
        "z_delta_cos",
        "z_delta_frob",
        "z_abs_surprisal",
        "z_probe_conf",
        "z_len",
        "z_jacc",
    ]
    active_terms = [t for t in numeric_terms if frame[t].std(ddof=0) > 0]

    fit = None
    used_terms: list[str] = []
    last_error: Exception | None = None
    # Retry by progressively dropping numeric predictors if the mixed model is singular.
    for n_keep in range(len(active_terms), -1, -1):
        trial_terms = active_terms[:n_keep]
        rhs = [*trial_terms, "C(phenomenon)", "C(model)"]
        formula = "human_change ~ " + " + ".join(rhs)
        model = smf.mixedlm(
            formula,
            data=frame,
            groups=frame["pair_group"],
            vc_formula={"annotator": "0 + C(annotator_group)"},
            re_formula="1",
        )
        try:
            fit = model.fit(reml=False, method="lbfgs", maxiter=300, disp=False)
            used_terms = trial_terms
            break
        except Exception as exc:  # pragma: no cover - runtime robustness path
            last_error = exc
            continue

    if fit is None:
        raise RuntimeError(f"mixedlm_failed: {last_error}") from last_error

    out = {
        "n": len(frame),
        "llf": float(fit.llf),
        "aic": float(fit.aic),
        "bic": float(fit.bic),
        "converged": bool(fit.converged),
        "used_terms": ",".join(used_terms),
    }
    for name in numeric_terms:
        out[f"beta_{name}"] = float(fit.params.get(name, np.nan))
        out[f"p_{name}"] = float(fit.pvalues.get(name, np.nan))
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Run layer-wise mixed-effects models.")
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    cfg = load_yaml(args.config)
    out_dir = Path(str(cfg["output_dir"]))
    ensure_dir(out_dir)
    output = Path(args.output) if args.output else out_dir / "mixed_effects_summary.csv"

    df = _build_frame(cfg)
    rows = []
    for layer, g in df.groupby("layer"):
        layer_num = int(float(str(layer)))
        if len(g) < 80:
            continue
        try:
            row = _fit_layer(g)
            row["layer"] = layer_num
            rows.append(row)
        except Exception as exc:  # pragma: no cover - robust run logging
            rows.append({"layer": layer_num, "error": str(exc), "n": len(g)})

    result = pd.DataFrame(rows).sort_values("layer").reset_index(drop=True)
    result.to_csv(output, index=False)
    print(f"wrote {output} rows={len(result)}")


if __name__ == "__main__":
    main()
