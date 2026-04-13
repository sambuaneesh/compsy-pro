from __future__ import annotations

import argparse
import logging
import re
from pathlib import Path
from typing import Any

from css.common.config import load_yaml
from css.common.hash_utils import sha256_file
from css.common.io import write_json, write_jsonl
from css.data.build_pair import build_pair_record
from css.data.split_data import split_from_id

LOGGER = logging.getLogger(__name__)
TOKEN_RE = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")


def _read_lines(path: Path) -> list[str]:
    lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        raise ValueError(f"No non-empty lines found in {path}")
    return lines


def _normalize_sentence(text: str) -> str:
    clean = " ".join(text.strip().split())
    clean = clean.rstrip(",.")
    if not clean:
        raise ValueError("Empty sentence after normalization")
    if clean[0].islower():
        clean = clean[0].upper() + clean[1:]
    return f"{clean}."


def _token_spans(text: str) -> list[tuple[str, int, int]]:
    return [(m.group(0), m.start(), m.end()) for m in TOKEN_RE.finditer(text)]


def _find_last_idx(words: list[str], candidates: set[str]) -> int | None:
    for idx in range(len(words) - 1, -1, -1):
        if words[idx] in candidates:
            return idx
    return None


def _span_from_token(label: str, token: tuple[str, int, int]) -> dict[str, int | str]:
    return {"label": label, "text": token[0], "char_start": token[1], "char_end": token[2]}


def _role_spans(text: str) -> tuple[list[dict[str, int | str]], dict[str, str]]:
    tokens = _token_spans(text)
    if not tokens:
        raise ValueError(f"No tokens found in: {text}")

    lowered = [tok.lower() for tok, _, _ in tokens]
    aux_idx = _find_last_idx(lowered, {"had", "has"})
    agent_idx = len(tokens) - 1 if aux_idx is None or aux_idx == 0 else aux_idx - 1

    marker_idx = _find_last_idx(lowered, {"which", "that"})
    if marker_idx is not None and marker_idx + 1 < len(tokens):
        patient_idx = marker_idx + 1
    else:
        patient_idx = max(0, agent_idx - 1)

    if patient_idx == agent_idx:
        if agent_idx + 1 < len(tokens):
            patient_idx = agent_idx + 1
        elif agent_idx > 0:
            patient_idx = agent_idx - 1

    agent_tok = tokens[agent_idx]
    patient_tok = tokens[patient_idx]
    spans = [
        _span_from_token("agent", agent_tok),
        _span_from_token("patient", patient_tok),
    ]
    labels = {"agent": agent_tok[0].lower(), "patient": patient_tok[0].lower()}
    return spans, labels


def _negation_spans(text: str) -> tuple[list[dict[str, int | str]], int]:
    tokens = _token_spans(text)
    if not tokens:
        raise ValueError(f"No tokens found in: {text}")

    lowered = [tok.lower() for tok, _, _ in tokens]
    not_idx = _find_last_idx(lowered, {"not"})
    spans: list[dict[str, int | str]] = []

    spans.append(_span_from_token("predicate", tokens[-1]))
    if not_idx is not None:
        spans.append(_span_from_token("negation_cue", tokens[not_idx]))
        return spans, 1

    return spans, 0


def _build_role_record(
    *,
    pair_id: str,
    s: str,
    s_cf: str,
    split_train: float,
    split_dev: float,
    source_file: str,
    source_pair_index: int,
    direction: str,
) -> dict[str, Any]:
    s_spans, s_labels = _role_spans(s)
    s_cf_spans, s_cf_labels = _role_spans(s_cf)
    split = split_from_id(pair_id, train=split_train, dev=split_dev)
    return build_pair_record(
        pair_id=pair_id,
        phenomenon="role_reversal",
        s=s,
        s_cf=s_cf,
        edit_type="swap_agent_patient_external",
        source="extending_psycholinguistic_dataset",
        template_id="role_ext_psycholing_v1",
        split=split,
        gold_label={
            "role_direction_s": f"{s_labels['agent']}_agent_{s_labels['patient']}_patient",
            "role_direction_cf": f"{s_cf_labels['agent']}_agent_{s_cf_labels['patient']}_patient",
            "negation_s": None,
            "negation_cf": None,
            "attachment_s": None,
            "attachment_cf": None,
        },
        edited_spans={"s": s_spans, "s_cf": s_cf_spans},
        linguistic_metadata={
            "source_file": source_file,
            "source_pair_index": source_pair_index,
            "direction": direction,
            "parse_strategy": "token_heuristic",
        },
    )


def _build_neg_record(
    *,
    pair_id: str,
    s: str,
    s_cf: str,
    edit_type: str,
    split_train: float,
    split_dev: float,
    source_file: str,
    source_pair_index: int,
    direction: str,
) -> dict[str, Any]:
    s_spans, neg_s = _negation_spans(s)
    s_cf_spans, neg_cf = _negation_spans(s_cf)
    split = split_from_id(pair_id, train=split_train, dev=split_dev)
    return build_pair_record(
        pair_id=pair_id,
        phenomenon="negation",
        s=s,
        s_cf=s_cf,
        edit_type=edit_type,
        source="extending_psycholinguistic_dataset",
        template_id="neg_ext_psycholing_v1",
        split=split,
        gold_label={
            "role_direction_s": None,
            "role_direction_cf": None,
            "negation_s": neg_s,
            "negation_cf": neg_cf,
            "attachment_s": None,
            "attachment_cf": None,
        },
        edited_spans={"s": s_spans, "s_cf": s_cf_spans},
        linguistic_metadata={
            "source_file": source_file,
            "source_pair_index": source_pair_index,
            "direction": direction,
            "parse_strategy": "token_heuristic",
        },
    )


def import_role(
    *,
    source_path: Path,
    split_train: float,
    split_dev: float,
) -> list[dict[str, Any]]:
    raw = _read_lines(source_path)
    if len(raw) % 2 != 0:
        raise ValueError(f"Expected even number of role lines, got {len(raw)} in {source_path}")

    out: list[dict[str, Any]] = []
    for pair_idx in range(0, len(raw), 2):
        a = _normalize_sentence(raw[pair_idx])
        b = _normalize_sentence(raw[pair_idx + 1])
        rec_a = _build_role_record(
            pair_id=f"role_{len(out) + 1:06d}",
            s=a,
            s_cf=b,
            split_train=split_train,
            split_dev=split_dev,
            source_file=source_path.name,
            source_pair_index=(pair_idx // 2) + 1,
            direction="forward",
        )
        out.append(rec_a)
        rec_b = _build_role_record(
            pair_id=f"role_{len(out) + 1:06d}",
            s=b,
            s_cf=a,
            split_train=split_train,
            split_dev=split_dev,
            source_file=source_path.name,
            source_pair_index=(pair_idx // 2) + 1,
            direction="reverse",
        )
        out.append(rec_b)
    return out


def import_negation(
    *,
    source_path: Path,
    split_train: float,
    split_dev: float,
) -> list[dict[str, Any]]:
    raw = _read_lines(source_path)
    if len(raw) % 2 != 0:
        raise ValueError(f"Expected even number of negation lines, got {len(raw)} in {source_path}")

    out: list[dict[str, Any]] = []
    for pair_idx in range(0, len(raw), 2):
        first = _normalize_sentence(raw[pair_idx])
        second = _normalize_sentence(raw[pair_idx + 1])
        first_is_neg = " not " in f" {first.lower()} "
        second_is_neg = " not " in f" {second.lower()} "

        if first_is_neg == second_is_neg:
            LOGGER.warning(
                "Ambiguous negation pair ordering in %s pair=%s; preserving line order.",
                source_path.name,
                (pair_idx // 2) + 1,
            )
            affirmative = first
            negated = second
        elif first_is_neg:
            affirmative = second
            negated = first
        else:
            affirmative = first
            negated = second

        rec_insert = _build_neg_record(
            pair_id=f"neg_{len(out) + 1:06d}",
            s=affirmative,
            s_cf=negated,
            edit_type="insert_not",
            split_train=split_train,
            split_dev=split_dev,
            source_file=source_path.name,
            source_pair_index=(pair_idx // 2) + 1,
            direction="forward",
        )
        out.append(rec_insert)
        rec_remove = _build_neg_record(
            pair_id=f"neg_{len(out) + 1:06d}",
            s=negated,
            s_cf=affirmative,
            edit_type="remove_not",
            split_train=split_train,
            split_dev=split_dev,
            source_file=source_path.name,
            source_pair_index=(pair_idx // 2) + 1,
            direction="reverse",
        )
        out.append(rec_remove)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Import role/negation data from extending_psycholinguistic_dataset"
    )
    parser.add_argument("--config", default="configs/data/external_import.yaml")
    parser.add_argument("--output-role", default=None)
    parser.add_argument("--output-neg", default=None)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    cfg = load_yaml(args.config)

    source_root = Path(str(cfg["source_root"]))
    role_source = source_root / str(cfg["role_source_file"])
    neg_source = source_root / str(cfg["negation_source_file"])
    if not role_source.exists() or not neg_source.exists():
        raise FileNotFoundError(
            "Required external dataset files are missing. "
            "Run: git clone https://github.com/text-machine-lab/extending_psycholinguistic_dataset "
            "data/external/extending_psycholinguistic_dataset"
        )
    output_role = Path(str(args.output_role or cfg["output_role_path"]))
    output_neg = Path(str(args.output_neg or cfg["output_negation_path"]))
    split_train = float(cfg.get("split_ratios", {}).get("train", 0.7))
    split_dev = float(cfg.get("split_ratios", {}).get("dev", 0.15))

    role_rows = import_role(source_path=role_source, split_train=split_train, split_dev=split_dev)
    neg_rows = import_negation(source_path=neg_source, split_train=split_train, split_dev=split_dev)
    write_jsonl(output_role, role_rows)
    write_jsonl(output_neg, neg_rows)
    LOGGER.info("wrote %s rows=%s", output_role, len(role_rows))
    LOGGER.info("wrote %s rows=%s", output_neg, len(neg_rows))

    pilot_n = int(cfg.get("pilot_n", 100))
    pilot_role_output = cfg.get("pilot_role_output_path")
    pilot_neg_output = cfg.get("pilot_neg_output_path")
    if pilot_role_output:
        write_jsonl(str(pilot_role_output), role_rows[:pilot_n])
        LOGGER.info("wrote %s rows=%s", pilot_role_output, pilot_n)
    if pilot_neg_output:
        write_jsonl(str(pilot_neg_output), neg_rows[:pilot_n])
        LOGGER.info("wrote %s rows=%s", pilot_neg_output, pilot_n)

    manifest_output = cfg.get("manifest_output")
    if manifest_output:
        manifest = {
            "source_repo_url": cfg.get("source_repo_url", ""),
            "source_root": str(source_root),
            "role_source_file": str(role_source),
            "negation_source_file": str(neg_source),
            "role_source_sha256": sha256_file(role_source),
            "negation_source_sha256": sha256_file(neg_source),
            "output_role_path": str(output_role),
            "output_negation_path": str(output_neg),
            "output_role_rows": len(role_rows),
            "output_negation_rows": len(neg_rows),
        }
        write_json(str(manifest_output), manifest)
        LOGGER.info("wrote %s", manifest_output)


if __name__ == "__main__":
    main()
