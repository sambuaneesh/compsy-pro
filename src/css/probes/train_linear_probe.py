from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from css.common.config import load_yaml
from css.common.io import ensure_dir, write_json
from css.probes.build_probe_dataset import (
    ProbeDataset,
    build_attachment_probe_dataset,
    build_negation_probe_dataset,
    build_role_probe_dataset,
)
from css.probes.selectivity_controls import random_label_control
from css.representations.cache_io import load_hidden_cache


def _safe_name(name: str) -> str:
    return name.replace("/", "__")


def _build_probe_data(
    phenomenon: str, payload: dict[str, Any], layer: int
) -> tuple[str, ProbeDataset]:
    if phenomenon == "role_reversal":
        return "role_probe", build_role_probe_dataset(payload, layer)
    if phenomenon == "negation":
        return "negation_probe", build_negation_probe_dataset(payload, layer)
    if phenomenon == "attachment":
        return "attachment_probe", build_attachment_probe_dataset(payload, layer)
    raise ValueError(f"unsupported phenomenon {phenomenon}")


def _fit_and_score(
    x: np.ndarray,
    y: np.ndarray,
    *,
    seed: int,
    test_size: float,
    solver: str,
    max_iter: int,
    c: float,
) -> dict[str, float]:
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=test_size, random_state=seed, stratify=y
    )
    clf = Pipeline(
        [
            ("scaler", StandardScaler()),
            (
                "lr",
                LogisticRegression(
                    solver=solver,
                    max_iter=max_iter,
                    C=c,
                    random_state=seed,
                ),
            ),
        ]
    )
    clf.fit(x_train, y_train)
    y_pred = clf.predict(x_test)
    y_prob = clf.predict_proba(x_test)[:, 1] if len(np.unique(y)) == 2 else None

    task_accuracy = float(accuracy_score(y_test, y_pred))
    task_macro_f1 = float(f1_score(y_test, y_pred, average="macro"))
    task_auroc = float(roc_auc_score(y_test, y_prob)) if y_prob is not None else float("nan")

    y_train_control = random_label_control(y_train, seed=seed)
    ctrl = Pipeline(
        [
            ("scaler", StandardScaler()),
            (
                "lr",
                LogisticRegression(
                    solver=solver,
                    max_iter=max_iter,
                    C=c,
                    random_state=seed,
                ),
            ),
        ]
    )
    ctrl.fit(x_train, y_train_control)
    y_ctrl = ctrl.predict(x_test)
    control_accuracy = float(accuracy_score(y_test, y_ctrl))
    control_macro_f1 = float(f1_score(y_test, y_ctrl, average="macro"))

    return {
        "accuracy": task_accuracy,
        "macro_f1": task_macro_f1,
        "auroc": task_auroc,
        "control_accuracy": control_accuracy,
        "control_macro_f1": control_macro_f1,
        "selectivity": task_macro_f1 - control_macro_f1,
        "n_train": len(x_train),
        "n_test": len(x_test),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Train layer-wise linear probes with controls.")
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", default="results/probes/probe_results.csv")
    parser.add_argument("--pred-output", default="results/probes/probe_predictions.csv")
    parser.add_argument("--summary-output", default=None)
    parser.add_argument("--summary-json-output", default=None)
    args = parser.parse_args()

    cfg = load_yaml(args.config)
    layers = range(int(cfg["layers"]["start"]), int(cfg["layers"]["end_inclusive"]) + 1)
    seeds = [int(s) for s in cfg["probe"]["seeds"]]
    test_size = float(cfg["probe"].get("test_size", 0.2))
    solver = str(cfg["probe"].get("solver", "liblinear"))
    max_iter = int(cfg["probe"].get("max_iter", 300))
    c = float(cfg["probe"].get("C", 1.0))
    cache_root = str(cfg.get("cache_root", "cache"))

    rows_out: list[dict[str, Any]] = []
    pred_rows: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []

    for model_name in cfg["models"]:
        for dataset_path in cfg["datasets"]:
            stem = Path(str(dataset_path)).stem
            cache_path = (
                Path(cache_root)
                / "hidden"
                / _safe_name(str(model_name))
                / stem
                / "hidden_cache.pkl"
            )
            if not cache_path.exists():
                skipped.append(
                    {"reason": "missing_cache", "model": model_name, "dataset_path": dataset_path}
                )
                continue

            payload = load_hidden_cache(cache_path)
            items = payload["items"]
            if not items:
                continue
            phenomenon = str(items[0]["phenomenon"])
            probe_name, _ = _build_probe_data(phenomenon, payload, layer=0)

            for layer in layers:
                _, probe_ds = _build_probe_data(phenomenon, payload, layer=layer)
                x = probe_ds.x
                y = probe_ds.y
                if x.shape[0] < 20 or len(np.unique(y)) < 2:
                    skipped.append(
                        {
                            "reason": "insufficient_data",
                            "model": model_name,
                            "dataset_path": dataset_path,
                            "layer": layer,
                            "n": int(x.shape[0]),
                            "classes": len(np.unique(y)),
                        }
                    )
                    continue

                for seed in seeds:
                    scores = _fit_and_score(
                        x,
                        y,
                        seed=seed,
                        test_size=test_size,
                        solver=solver,
                        max_iter=max_iter,
                        c=c,
                    )
                    rows_out.append(
                        {
                            "phenomenon": phenomenon,
                            "probe_name": probe_name,
                            "model": model_name,
                            "dataset_path": dataset_path,
                            "layer": layer,
                            "seed": seed,
                            "split_type": cfg["probe"].get("split_type", "random"),
                            "feature_type": "span_vector"
                            if probe_name == "role_probe"
                            else "sentence_mean",
                            "accuracy": scores["accuracy"],
                            "macro_f1": scores["macro_f1"],
                            "auroc": scores["auroc"],
                            "ece": np.nan,
                            "control_accuracy": scores["control_accuracy"],
                            "control_macro_f1": scores["control_macro_f1"],
                            "selectivity": scores["selectivity"],
                            "n_train": scores["n_train"],
                            "n_dev": 0,
                            "n_test": scores["n_test"],
                            "config_sha256": "pending",
                            "solver": solver,
                            "max_iter": max_iter,
                            "C": c,
                        }
                    )
                pred_rows.append(
                    {
                        "phenomenon": phenomenon,
                        "probe_name": probe_name,
                        "model": model_name,
                        "layer": layer,
                        "n_examples": int(x.shape[0]),
                    }
                )

    df = (
        pd.DataFrame(rows_out)
        .sort_values(["model", "phenomenon", "layer", "seed"])
        .reset_index(drop=True)
    )
    ensure_dir(Path(args.output).parent)
    df.to_csv(args.output, index=False)
    pd.DataFrame(pred_rows).to_csv(args.pred_output, index=False)
    if not df.empty:
        summary = (
            df.groupby(["phenomenon", "probe_name", "model", "layer"])[
                ["macro_f1", "control_macro_f1", "selectivity", "accuracy", "control_accuracy"]
            ]
            .mean()
            .reset_index()
        )
    else:
        summary = pd.DataFrame()
    default_summary_path = Path(args.output).with_name("selectivity_summary.csv")
    default_summary_json_path = Path(args.output).with_name("selectivity_summary.json")
    summary_output = Path(args.summary_output) if args.summary_output else default_summary_path
    summary_json_output = (
        Path(args.summary_json_output) if args.summary_json_output else default_summary_json_path
    )
    summary.to_csv(summary_output, index=False)
    write_json(summary_json_output, {"skipped": skipped, "n_results": len(df)})
    print(f"wrote {args.output} rows={len(df)}")
    print(f"wrote {args.pred_output} rows={len(pred_rows)}")
    print(f"wrote {summary_output} rows={len(summary)}")
    print(f"wrote {summary_json_output}")


if __name__ == "__main__":
    main()
