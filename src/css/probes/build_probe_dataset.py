from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np


@dataclass
class ProbeDataset:
    x: np.ndarray
    y: np.ndarray
    pair_ids: list[str]
    side: list[str]
    labels_text: list[str]


def _char_span_to_word_index(
    char_start: int, word_spans: list[list[int]] | list[tuple[int, int]]
) -> int | None:
    for idx, (start, end) in enumerate(word_spans):
        if char_start >= int(start) and char_start < int(end):
            return idx
    return None


def _label_side_suffix(side: str) -> str:
    if side == "s":
        return "s"
    if side == "s_cf":
        return "cf"
    raise ValueError(f"unsupported side: {side}")


def build_role_probe_dataset(cache_payload: dict[str, Any], layer: int) -> ProbeDataset:
    xs: list[np.ndarray] = []
    ys: list[int] = []
    pair_ids: list[str] = []
    sides: list[str] = []
    labels_text: list[str] = []

    layer_k = str(layer)
    for item in cache_payload["items"]:
        if item["phenomenon"] != "role_reversal":
            continue
        spans = item.get("edited_spans", {})
        for side in ("s", "s_cf"):
            matrix = item["layers"][layer_k][f"{side}_word_matrix"].astype(np.float32)
            word_spans = item[f"{side}_word_spans"]
            for span in spans.get(side, []):
                if span["label"] not in {"agent", "patient"}:
                    continue
                idx = _char_span_to_word_index(int(span["char_start"]), word_spans)
                if idx is None or idx >= matrix.shape[0]:
                    continue
                xs.append(matrix[idx])
                ys.append(1 if span["label"] == "agent" else 0)
                pair_ids.append(item["pair_id"])
                sides.append(side)
                labels_text.append(span["label"])

    if not xs:
        return ProbeDataset(
            x=np.zeros((0, 1), dtype=np.float32),
            y=np.zeros((0,), dtype=np.int64),
            pair_ids=[],
            side=[],
            labels_text=[],
        )

    return ProbeDataset(
        x=np.vstack(xs),
        y=np.array(ys, dtype=np.int64),
        pair_ids=pair_ids,
        side=sides,
        labels_text=labels_text,
    )


def build_negation_probe_dataset(cache_payload: dict[str, Any], layer: int) -> ProbeDataset:
    xs: list[np.ndarray] = []
    ys: list[int] = []
    pair_ids: list[str] = []
    sides: list[str] = []
    labels_text: list[str] = []
    layer_k = str(layer)

    for item in cache_payload["items"]:
        if item["phenomenon"] != "negation":
            continue
        gold = item.get("gold_label", {})
        for side in ("s", "s_cf"):
            suffix = _label_side_suffix(side)
            label = gold.get(f"negation_{suffix}")
            if label is None:
                continue
            vec = item["layers"][layer_k][f"{side}_mean"].astype(np.float32)
            xs.append(vec)
            ys.append(int(label))
            pair_ids.append(item["pair_id"])
            sides.append(side)
            labels_text.append("negated" if int(label) == 1 else "affirmative")

    if not xs:
        return ProbeDataset(
            x=np.zeros((0, 1), dtype=np.float32),
            y=np.zeros((0,), dtype=np.int64),
            pair_ids=[],
            side=[],
            labels_text=[],
        )

    return ProbeDataset(
        x=np.vstack(xs),
        y=np.array(ys, dtype=np.int64),
        pair_ids=pair_ids,
        side=sides,
        labels_text=labels_text,
    )


def build_attachment_probe_dataset(cache_payload: dict[str, Any], layer: int) -> ProbeDataset:
    xs: list[np.ndarray] = []
    ys: list[int] = []
    pair_ids: list[str] = []
    sides: list[str] = []
    labels_text: list[str] = []
    layer_k = str(layer)
    mapping = {"VP_attachment": 1, "NP_attachment": 0}

    for item in cache_payload["items"]:
        if item["phenomenon"] != "attachment":
            continue
        gold = item.get("gold_label", {})
        for side in ("s", "s_cf"):
            suffix = _label_side_suffix(side)
            label_text = gold.get(f"attachment_{suffix}")
            if label_text not in mapping:
                continue
            vec = item["layers"][layer_k][f"{side}_mean"].astype(np.float32)
            xs.append(vec)
            ys.append(mapping[label_text])
            pair_ids.append(item["pair_id"])
            sides.append(side)
            labels_text.append(str(label_text))

    if not xs:
        return ProbeDataset(
            x=np.zeros((0, 1), dtype=np.float32),
            y=np.zeros((0,), dtype=np.int64),
            pair_ids=[],
            side=[],
            labels_text=[],
        )

    return ProbeDataset(
        x=np.vstack(xs),
        y=np.array(ys, dtype=np.int64),
        pair_ids=pair_ids,
        side=sides,
        labels_text=labels_text,
    )
