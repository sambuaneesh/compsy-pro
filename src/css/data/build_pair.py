from __future__ import annotations

from typing import Any

from css.common.text import levenshtein_distance, lexical_jaccard, token_len
from css.data.schema import PAIR_SCHEMA_VERSION


def base_surface_controls(s: str, s_cf: str) -> dict[str, Any]:
    return {
        "token_len_s": token_len(s),
        "token_len_cf": token_len(s_cf),
        "char_len_s": len(s),
        "char_len_cf": len(s_cf),
        "lexical_jaccard": round(lexical_jaccard(s, s_cf), 6),
        "levenshtein_distance": levenshtein_distance(s, s_cf),
    }


def build_pair_record(
    *,
    pair_id: str,
    phenomenon: str,
    s: str,
    s_cf: str,
    edit_type: str,
    source: str,
    template_id: str,
    split: str,
    gold_label: dict[str, Any],
    edited_spans: dict[str, list[dict[str, Any]]],
    linguistic_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    row: dict[str, Any] = {
        "id": pair_id,
        "schema_version": PAIR_SCHEMA_VERSION,
        "phenomenon": phenomenon,
        "s": s,
        "s_cf": s_cf,
        "edit_type": edit_type,
        "source": source,
        "template_id": template_id,
        "split": split,
        "gold_label": gold_label,
        "edited_spans": edited_spans,
        "surface_controls": base_surface_controls(s, s_cf),
        "human_change": None,
        "notes": "",
    }
    if linguistic_metadata:
        row["linguistic_metadata"] = linguistic_metadata
    return row
