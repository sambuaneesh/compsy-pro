from __future__ import annotations

from pathlib import Path

from css.data.import_extending_psycholinguistic_dataset import (
    _normalize_sentence,
    _role_spans,
    import_negation,
    import_role,
)


def test_normalize_sentence_trims_and_punctuates() -> None:
    assert _normalize_sentence("the cat sat,") == "The cat sat."


def test_role_spans_extract_agent_and_patient_tokens() -> None:
    text = "The journalist investigated which athlete the team had recruited."
    spans, labels = _role_spans(text)
    assert labels["agent"] == "team"
    assert labels["patient"] == "athlete"
    assert {s["label"] for s in spans} == {"agent", "patient"}


def test_import_role_creates_bidirectional_records(tmp_path: Path) -> None:
    role_path = tmp_path / "ROLE-1500.txt"
    role_path.write_text(
        "\n".join(
            [
                "the journalist investigated which athlete the team had recruited,",
                "the journalist investigated which team the athlete had joined,",
            ]
        ),
        encoding="utf-8",
    )
    rows = import_role(source_path=role_path, split_train=0.7, split_dev=0.15)
    assert len(rows) == 2
    assert rows[0]["id"] == "role_000001"
    assert rows[1]["id"] == "role_000002"
    assert rows[0]["s"] == "The journalist investigated which athlete the team had recruited."
    assert rows[1]["s"] == "The journalist investigated which team the athlete had joined."
    assert rows[0]["phenomenon"] == "role_reversal"


def test_import_negation_creates_insert_and_remove_records(tmp_path: Path) -> None:
    neg_path = tmp_path / "NEG-1500-SIMP-GEN.txt"
    neg_path.write_text(
        "\n".join(
            [
                "A cat is an animal,",
                "A cat is not a machine,",
            ]
        ),
        encoding="utf-8",
    )
    rows = import_negation(source_path=neg_path, split_train=0.7, split_dev=0.15)
    assert len(rows) == 2
    assert rows[0]["edit_type"] == "insert_not"
    assert rows[1]["edit_type"] == "remove_not"
    assert rows[0]["gold_label"]["negation_s"] == 0
    assert rows[0]["gold_label"]["negation_cf"] == 1
    assert rows[1]["gold_label"]["negation_s"] == 1
    assert rows[1]["gold_label"]["negation_cf"] == 0
