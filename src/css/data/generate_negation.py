from __future__ import annotations

import argparse
import random
from typing import Any

from css.common.config import load_yaml
from css.common.io import write_jsonl
from css.common.text import find_span_or_raise
from css.data.build_pair import build_pair_record
from css.data.lexicons import load_csv_rows
from css.data.split_data import split_from_id


def _make_affirmative(agent: str, base: str, past: str, patient: str) -> str:
    _ = base
    return f"The {agent} {past} the {patient}."


def _make_negative(agent: str, base: str, patient: str) -> str:
    return f"The {agent} did not {base} the {patient}."


def generate_negation_pairs(n: int, seed: int) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    nouns = [r["noun"] for r in load_csv_rows("data/lexicons/nouns_animacy.csv")]
    verbs = load_csv_rows("data/lexicons/verbs_roles.csv")
    out: list[dict[str, Any]] = []

    while len(out) < n:
        subj, obj = rng.sample(nouns, k=2)
        verb = rng.choice(verbs)
        s_pos = _make_affirmative(subj, verb["verb_base"], verb["verb_past"], obj)
        s_neg = _make_negative(subj, verb["verb_base"], obj)

        edit_type = "insert_not" if len(out) % 2 == 0 else "remove_not"
        if edit_type == "insert_not":
            s = s_pos
            s_cf = s_neg
            neg_s, neg_cf = 0, 1
        else:
            s = s_neg
            s_cf = s_pos
            neg_s, neg_cf = 1, 0

        pair_id = f"neg_{len(out) + 1:06d}"
        split = split_from_id(pair_id, train=0.7, dev=0.15)

        s_spans: list[dict[str, Any]] = [find_span_or_raise(s, verb["verb_base"], "predicate")]
        cf_spans: list[dict[str, Any]] = [find_span_or_raise(s_cf, verb["verb_base"], "predicate")]
        if neg_s == 1:
            s_spans.append(find_span_or_raise(s, "not", "negation_cue"))
        if neg_cf == 1:
            cf_spans.append(find_span_or_raise(s_cf, "not", "negation_cue"))

        out.append(
            build_pair_record(
                pair_id=pair_id,
                phenomenon="negation",
                s=s,
                s_cf=s_cf,
                edit_type=edit_type,
                source="templated",
                template_id="neg_aux_not_v01",
                split=split,
                gold_label={
                    "role_direction_s": None,
                    "role_direction_cf": None,
                    "negation_s": neg_s,
                    "negation_cf": neg_cf,
                    "attachment_s": None,
                    "attachment_cf": None,
                },
                edited_spans={"s": s_spans, "s_cf": cf_spans},
                linguistic_metadata={
                    "subject": subj,
                    "object": obj,
                    "verb_base": verb["verb_base"],
                    "verb_past": verb["verb_past"],
                    "negation_scope": "main_predicate",
                },
            )
        )

    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate negation css_pair_v1 JSONL")
    parser.add_argument("--config", default="configs/data/negation.yaml")
    parser.add_argument("--n", type=int, default=None)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    cfg = load_yaml(args.config)
    n = int(args.n or cfg["n"])
    output = str(args.output or cfg["output_path"])
    seed = int(cfg["seed"])

    rows = generate_negation_pairs(n=n, seed=seed)
    write_jsonl(output, rows)
    print(f"wrote {output} rows={len(rows)}")

    pilot_n = cfg.get("pilot_n")
    pilot_output = cfg.get("pilot_output_path")
    if args.n is None and pilot_n and pilot_output:
        pilot_rows = rows[: int(pilot_n)]
        write_jsonl(str(pilot_output), pilot_rows)
        print(f"wrote {pilot_output} rows={len(pilot_rows)}")


if __name__ == "__main__":
    main()
