from __future__ import annotations

from dataclasses import dataclass
from typing import Any

PHENOMENA = {"role_reversal", "negation", "attachment"}
PAIR_SCHEMA_VERSION = "css_pair_v1"


@dataclass(frozen=True)
class ValidationIssue:
    pair_id: str
    field: str
    message: str


REQUIRED_TOP_LEVEL_FIELDS = [
    "id",
    "schema_version",
    "phenomenon",
    "s",
    "s_cf",
    "edit_type",
    "source",
    "template_id",
    "split",
    "gold_label",
    "edited_spans",
    "surface_controls",
    "human_change",
]


def _require_type(value: Any, expected: type, field: str, pair_id: str) -> ValidationIssue | None:
    if not isinstance(value, expected):
        return ValidationIssue(
            pair_id=pair_id, field=field, message=f"expected {expected.__name__}"
        )
    return None


def validate_pair_record(row: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    pair_id = str(row.get("id", "<missing_id>"))

    for field in REQUIRED_TOP_LEVEL_FIELDS:
        if field not in row:
            issues.append(ValidationIssue(pair_id, field, "missing required field"))

    if issues:
        return issues

    if row["schema_version"] != PAIR_SCHEMA_VERSION:
        issues.append(
            ValidationIssue(
                pair_id,
                "schema_version",
                f"expected '{PAIR_SCHEMA_VERSION}', got '{row['schema_version']}'",
            )
        )

    if row["phenomenon"] not in PHENOMENA:
        issues.append(ValidationIssue(pair_id, "phenomenon", f"must be one of {sorted(PHENOMENA)}"))

    checks: list[tuple[str, type]] = [
        ("id", str),
        ("s", str),
        ("s_cf", str),
        ("edit_type", str),
        ("source", str),
        ("template_id", str),
        ("split", str),
        ("gold_label", dict),
        ("edited_spans", dict),
        ("surface_controls", dict),
    ]
    for field, t in checks:
        issue = _require_type(row[field], t, field, pair_id)
        if issue:
            issues.append(issue)

    spans = row.get("edited_spans", {})
    for side in ("s", "s_cf"):
        side_spans = spans.get(side)
        if not isinstance(side_spans, list) or not side_spans:
            issues.append(
                ValidationIssue(pair_id, f"edited_spans.{side}", "must be non-empty list")
            )
            continue
        for k, span in enumerate(side_spans):
            if not isinstance(span, dict):
                issues.append(ValidationIssue(pair_id, f"edited_spans.{side}[{k}]", "must be dict"))
                continue
            for key in ("label", "text", "char_start", "char_end"):
                if key not in span:
                    issues.append(
                        ValidationIssue(pair_id, f"edited_spans.{side}[{k}].{key}", "missing")
                    )

    surface = row.get("surface_controls", {})
    for key in (
        "token_len_s",
        "token_len_cf",
        "char_len_s",
        "char_len_cf",
        "lexical_jaccard",
        "levenshtein_distance",
    ):
        if key not in surface:
            issues.append(ValidationIssue(pair_id, f"surface_controls.{key}", "missing"))

    return issues
