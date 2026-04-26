from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import pandas as pd

from css.common.config import load_yaml
from css.common.io import ensure_dir

METRICS = ["delta_cos", "delta_frob", "delta_l2", "delta_token_aligned"]


def _flatten_pair(row: pd.Series) -> dict[str, Any]:
    surface = row["surface_controls"]
    metadata = row["linguistic_metadata"]
    return {
        "pair_id": row["id"],
        "phenomenon": row["phenomenon"],
        "s": row["s"],
        "s_cf": row["s_cf"],
        "edit_type": row["edit_type"],
        "split": row["split"],
        "token_len_s": int(surface["token_len_s"]),
        "token_len_cf": int(surface["token_len_cf"]),
        "length_delta": int(surface["token_len_cf"]) - int(surface["token_len_s"]),
        "abs_length_delta": abs(int(surface["token_len_cf"]) - int(surface["token_len_s"])),
        "lexical_jaccard": float(surface["lexical_jaccard"]),
        "levenshtein_distance": int(surface["levenshtein_distance"]),
        "source_file": str(metadata.get("source_file", "")),
        "source_pair_index": int(metadata.get("source_pair_index", -1)),
        "direction": str(metadata.get("direction", "")),
    }


def _load_pair_frame(path: str | Path) -> pd.DataFrame:
    pairs = pd.read_json(path, lines=True)
    return pd.DataFrame([_flatten_pair(row) for _, row in pairs.iterrows()])


def _pair_summary(metrics_path: str, surprisal_path: str, pairs_path: str) -> pd.DataFrame:
    metrics = pd.read_csv(metrics_path)
    surprisal = pd.read_csv(surprisal_path)
    pairs = _load_pair_frame(pairs_path)
    metric_models = sorted(str(model) for model in metrics["model"].dropna().unique())
    metric_layers = sorted(int(layer) for layer in metrics["layer"].dropna().unique())

    metric_summary = (
        metrics.groupby(["pair_id", "phenomenon"], as_index=False)[METRICS]
        .mean()
        .rename(columns={metric: f"mean_{metric}" for metric in METRICS})
    )
    summary = (
        pairs.merge(metric_summary, on=["pair_id", "phenomenon"], how="inner")
        .merge(
            surprisal[
                [
                    "pair_id",
                    "phenomenon",
                    "avg_surprisal_s",
                    "avg_surprisal_cf",
                    "delta_avg_surprisal",
                    "abs_delta_avg_surprisal",
                    "delta_key_region_surprisal",
                ]
            ],
            on=["pair_id", "phenomenon"],
            how="inner",
        )
        .sort_values(["phenomenon", "pair_id"])
    )

    summary["frob_percentile_in_phenomenon"] = summary.groupby("phenomenon")[
        "mean_delta_frob"
    ].rank(pct=True)
    summary["surprisal_percentile_in_phenomenon"] = summary.groupby("phenomenon")[
        "abs_delta_avg_surprisal"
    ].rank(pct=True)
    summary.attrs["metric_models"] = metric_models
    summary.attrs["metric_layer_count"] = len(metric_layers)
    summary.attrs["metric_layer_min"] = min(metric_layers) if metric_layers else None
    summary.attrs["metric_layer_max"] = max(metric_layers) if metric_layers else None
    return summary


def _surface_summary(summary: pd.DataFrame) -> pd.DataFrame:
    return (
        summary.groupby("phenomenon", as_index=False)
        .agg(
            n_pairs=("pair_id", "size"),
            mean_abs_length_delta=("abs_length_delta", "mean"),
            median_abs_length_delta=("abs_length_delta", "median"),
            mean_lexical_jaccard=("lexical_jaccard", "mean"),
            median_lexical_jaccard=("lexical_jaccard", "median"),
            mean_levenshtein_distance=("levenshtein_distance", "mean"),
            median_levenshtein_distance=("levenshtein_distance", "median"),
            mean_delta_frob=("mean_delta_frob", "mean"),
            mean_abs_delta_avg_surprisal=("abs_delta_avg_surprisal", "mean"),
        )
        .sort_values("phenomenon")
    )


def _choose_case(
    frame: pd.DataFrame,
    *,
    category: str,
    used_source_indices: set[int],
) -> pd.Series:
    candidates = frame.copy()
    frob_pct = candidates["frob_percentile_in_phenomenon"]
    surprisal_pct = candidates["surprisal_percentile_in_phenomenon"]

    if category == "high_shift_high_surprisal":
        mask = (frob_pct >= 0.75) & (surprisal_pct >= 0.75)
        candidates["case_score"] = frob_pct + surprisal_pct
    elif category == "high_shift_low_surprisal":
        mask = (frob_pct >= 0.75) & (surprisal_pct <= 0.35)
        candidates["case_score"] = frob_pct + (1.0 - surprisal_pct)
    elif category == "low_shift_high_surprisal":
        mask = (frob_pct <= 0.35) & (surprisal_pct >= 0.75)
        candidates["case_score"] = (1.0 - frob_pct) + surprisal_pct
    elif category == "low_shift_low_surprisal":
        mask = (frob_pct <= 0.35) & (surprisal_pct <= 0.35)
        candidates["case_score"] = (1.0 - frob_pct) + (1.0 - surprisal_pct)
    else:
        raise ValueError(f"Unknown qualitative category: {category}")

    filtered = candidates[mask].copy()
    if filtered.empty:
        filtered = candidates.copy()
    unused = filtered[~filtered["source_pair_index"].isin(used_source_indices)]
    if not unused.empty:
        filtered = unused
    selected = filtered.sort_values(["case_score", "pair_id"], ascending=[False, True]).iloc[0]
    used_source_indices.add(int(selected["source_pair_index"]))
    return selected


def _case_table(summary: pd.DataFrame) -> pd.DataFrame:
    rows = []
    categories = [
        "high_shift_high_surprisal",
        "high_shift_low_surprisal",
        "low_shift_high_surprisal",
        "low_shift_low_surprisal",
    ]
    for _, frame in summary.groupby("phenomenon"):
        used_source_indices: set[int] = set()
        for category in categories:
            selected = _choose_case(
                frame, category=category, used_source_indices=used_source_indices
            )
            row = selected.to_dict()
            row["qualitative_category"] = category
            rows.append(row)
    out = pd.DataFrame(rows)
    cols = [
        "qualitative_category",
        "phenomenon",
        "pair_id",
        "s",
        "s_cf",
        "edit_type",
        "mean_delta_frob",
        "mean_delta_cos",
        "mean_delta_l2",
        "mean_delta_token_aligned",
        "abs_delta_avg_surprisal",
        "delta_avg_surprisal",
        "lexical_jaccard",
        "abs_length_delta",
        "levenshtein_distance",
        "source_pair_index",
        "direction",
    ]
    return out[cols].sort_values(["phenomenon", "qualitative_category"])


def _fmt(value: float) -> str:
    return f"{value:.4f}"


def _category_label(category: str) -> str:
    return category.replace("_", " ")


def _category_interpretation(category: str) -> str:
    if category == "high_shift_high_surprisal":
        return (
            "Both diagnostics move together: the contextual geometry changes strongly and GPT-2 also "
            "assigns a large probability shift to the counterfactual. These are the clearest examples "
            "of aligned structural sensitivity."
        )
    if category == "high_shift_low_surprisal":
        return (
            "The representation moves strongly even though average surprisal barely changes. This is "
            "evidence that hidden-state geometry can capture a structural or lexical relation that is "
            "not reducible to sentence-level predictive difficulty."
        )
    if category == "low_shift_high_surprisal":
        return (
            "GPT-2 surprisal changes strongly while the averaged representation shift is small. This "
            "is the complementary dissociation: probabilistic expectation and representation geometry "
            "are related diagnostics, but one is not a substitute for the other."
        )
    if category == "low_shift_low_surprisal":
        return (
            "Both diagnostics are small. These cases help define the lower-sensitivity baseline and "
            "show that the pipeline is not mechanically assigning large shifts to every edit."
        )
    return "This case is an item-level diagnostic example."


def _write_report(
    *,
    report_path: Path,
    summary: pd.DataFrame,
    surface: pd.DataFrame,
    cases: pd.DataFrame,
) -> None:
    ensure_dir(report_path.parent)
    lines: list[str] = []
    lines.append("# Qualitative Analysis Addendum (Dataset-Only)\n")
    lines.append("## Purpose\n")
    lines.append(
        "This addendum responds to the need for deeper qualitative interpretation of the CSS results. "
        "It connects the aggregate statistics to actual counterfactual sentence pairs and explains why "
        "role reversal and negation behave differently under the same metric pipeline.\n"
    )

    lines.append("## How cases were selected\n")
    metric_models = summary.attrs.get("metric_models", [])
    layer_count = summary.attrs.get("metric_layer_count")
    layer_min = summary.attrs.get("metric_layer_min")
    layer_max = summary.attrs.get("metric_layer_max")
    if len(metric_models) == 1:
        model_scope = f"the model `{metric_models[0]}`"
    else:
        model_scope = f"{len(metric_models)} models: " + ", ".join(
            f"`{model}`" for model in metric_models
        )
    layer_scope = (
        f"{layer_count} layers indexed `{layer_min}..{layer_max}`"
        if layer_count is not None and layer_min is not None and layer_max is not None
        else "the available hidden-state layers"
    )
    lines.append(
        "All cases below are selected reproducibly from the current full result tables. "
        f"For each pair, metric values are averaged across {model_scope} and {layer_scope}. "
        "Pairs are then ranked within each phenomenon by mean Frobenius shift and by absolute GPT-2 "
        "average-surprisal delta. Four diagnostic buckets are reported per phenomenon: high/high, "
        "high/low, low/high, and low/low.\n"
    )

    lines.append("## Surface-form diagnostics\n")
    lines.append(
        "| Phenomenon | Pairs | Mean lexical Jaccard | Median lexical Jaccard | "
        "Mean abs length delta | Mean edit distance | Mean Frobenius shift | Mean abs avg surprisal delta |\n"
    )
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n")
    for _, row in surface.iterrows():
        lines.append(
            f"| {row['phenomenon']} | {int(row['n_pairs'])} | "
            f"{_fmt(row['mean_lexical_jaccard'])} | {_fmt(row['median_lexical_jaccard'])} | "
            f"{_fmt(row['mean_abs_length_delta'])} | {_fmt(row['mean_levenshtein_distance'])} | "
            f"{_fmt(row['mean_delta_frob'])} | {_fmt(row['mean_abs_delta_avg_surprisal'])} |\n"
        )

    lines.append("\n## Main qualitative findings\n")
    lines.append(
        "1. Negation shows larger average representation shifts partly because many source pairs "
        "are not pure one-token negation edits. They often combine a polarity cue with a predicate "
        "or category contrast, for example affirmative category membership versus a negated foil.\n"
    )
    lines.append(
        "2. Role reversal has higher lexical overlap and usually near-zero length change, so its "
        "mean shift magnitude can be smaller even when the semantic event structure changes sharply.\n"
    )
    lines.append(
        "3. This explains why aggregate mean shift and layer-wise correlation do not contradict each "
        "other: mean shift asks how large the movement is, while correlation asks whether item-level "
        "movement ranks track surprisal deltas.\n"
    )
    lines.append(
        "4. Frobenius is qualitatively useful because it can capture changes in token-token relational "
        "geometry that are washed out by one pooled sentence vector.\n"
    )
    lines.append(
        "5. The qualitative audit also surfaces generated-data artifacts, including occasional article "
        "mismatches, lexical substitutions, and implausible role-reversal continuations. These artifacts "
        "do not invalidate the dataset-only diagnostic, but they require conservative claim language "
        "and explain why we avoid human-comprehension claims.\n"
    )

    lines.append("\n## Case studies\n")
    for phenomenon, frame in cases.groupby("phenomenon"):
        lines.append(f"### {phenomenon}\n")
        for _, row in frame.iterrows():
            lines.append(f"#### {_category_label(str(row['qualitative_category']))}\n")
            lines.append(f"- Pair id: `{row['pair_id']}`\n")
            lines.append(f"- Sentence: {row['s']}\n")
            lines.append(f"- Counterfactual: {row['s_cf']}\n")
            lines.append(
                f"- Metrics: mean Frobenius={_fmt(row['mean_delta_frob'])}, "
                f"mean cosine={_fmt(row['mean_delta_cos'])}, "
                f"mean L2={_fmt(row['mean_delta_l2'])}, "
                f"mean token-aligned={_fmt(row['mean_delta_token_aligned'])}, "
                f"abs avg surprisal delta={_fmt(row['abs_delta_avg_surprisal'])}\n"
            )
            lines.append(
                f"- Surface controls: lexical Jaccard={_fmt(row['lexical_jaccard'])}, "
                f"abs length delta={int(row['abs_length_delta'])}, "
                f"edit distance={int(row['levenshtein_distance'])}\n"
            )
            lines.append(
                f"- Interpretation: {_category_interpretation(str(row['qualitative_category']))}\n"
            )

    lines.append("\n## Interpretation for presentation\n")
    if len(metric_models) > 1:
        lines.append(
            "When presenting the baseline aggregate results, say that the pooled mean-magnitude slide "
            "averages across models, layers, and pairs, while the later correlation slides ask whether "
            "pair-level shifts are rank-aligned with surprisal. Negation can therefore have larger "
            "average shift while role reversal shows a cleaner shift-surprisal relationship. The "
            "qualitative examples make this distinction concrete.\n"
        )
    else:
        lines.append(
            "When presenting this model-specific addendum, separate magnitude from correlation. "
            "Magnitude summarizes how far this model's hidden states move on average, while correlation "
            "asks whether pair-level shifts rank-align with surprisal deltas. The qualitative examples "
            "make this distinction concrete.\n"
        )

    lines.append("\n## Scope boundary\n")
    lines.append(
        "This remains a dataset-only qualitative analysis. It explains model-output artifacts and "
        "representation-shift behavior using sentence examples and surface controls. It does not "
        "introduce human-alignment claims.\n"
    )

    report_path.write_text("".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate qualitative CSS case studies from full result tables."
    )
    parser.add_argument("--config", default="configs/experiments/qualitative_full.yaml")
    args = parser.parse_args()

    cfg = load_yaml(args.config)
    out_dir = ensure_dir(cfg["output_dir"])
    report_path = Path(str(cfg["report_path"]))

    summary = _pair_summary(
        str(cfg["metrics_path"]),
        str(cfg["surprisal_path"]),
        str(cfg["pairs_path"]),
    )
    surface = _surface_summary(summary)
    cases = _case_table(summary)

    summary.to_csv(out_dir / "pair_level_summary.csv", index=False)
    surface.to_csv(out_dir / "surface_summary.csv", index=False)
    cases.to_csv(out_dir / "qualitative_cases.csv", index=False)
    _write_report(report_path=report_path, summary=summary, surface=surface, cases=cases)

    print(f"wrote {out_dir / 'pair_level_summary.csv'} rows={len(summary)}")
    print(f"wrote {out_dir / 'surface_summary.csv'} rows={len(surface)}")
    print(f"wrote {out_dir / 'qualitative_cases.csv'} rows={len(cases)}")
    print(f"wrote {report_path}")


if __name__ == "__main__":
    main()
