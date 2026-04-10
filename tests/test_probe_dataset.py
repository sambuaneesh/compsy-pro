from __future__ import annotations

import numpy as np

from css.probes.build_probe_dataset import (
    build_attachment_probe_dataset,
    build_negation_probe_dataset,
)
from css.representations.extract_hidden import _word_index_map


def test_negation_probe_uses_s_and_cf_labels() -> None:
    payload = {
        "items": [
            {
                "pair_id": "neg_000001",
                "phenomenon": "negation",
                "gold_label": {"negation_s": 0, "negation_cf": 1},
                "layers": {
                    "0": {
                        "s_mean": np.array([1.0, 0.0], dtype=np.float32),
                        "s_cf_mean": np.array([0.0, 1.0], dtype=np.float32),
                    }
                },
            }
        ]
    }
    ds = build_negation_probe_dataset(payload, layer=0)
    assert ds.x.shape == (2, 2)
    assert ds.y.tolist() == [0, 1]
    assert ds.side == ["s", "s_cf"]


def test_attachment_probe_uses_cf_key_and_balances_labels() -> None:
    payload = {
        "items": [
            {
                "pair_id": "attach_000001",
                "phenomenon": "attachment",
                "gold_label": {"attachment_s": "VP_attachment", "attachment_cf": "NP_attachment"},
                "layers": {
                    "0": {
                        "s_mean": np.array([1.0, 0.0], dtype=np.float32),
                        "s_cf_mean": np.array([0.0, 1.0], dtype=np.float32),
                    }
                },
            }
        ]
    }
    ds = build_attachment_probe_dataset(payload, layer=0)
    assert ds.x.shape == (2, 2)
    assert ds.y.tolist() == [1, 0]
    assert ds.side == ["s", "s_cf"]


def test_word_index_map_handles_whitespace_prefixed_offsets() -> None:
    text = "The driver ignored the passenger."
    # Mimics BPE offsets that may include leading whitespace.
    offsets = [(0, 3), (3, 10), (11, 18), (19, 22), (22, 33), (0, 0)]
    words, _, mapping = _word_index_map(text, offsets)
    assert words == ["The", "driver", "ignored", "the", "passenger."]
    assert mapping[0] == 0
    assert mapping[1] == 1
    assert mapping[2] == 2
    assert mapping[3] == 3
    assert mapping[4] == 4
    assert 5 not in mapping
