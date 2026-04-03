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


def generate_role_pairs(n: int, seed: int) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    nouns = load_csv_rows("data/lexicons/nouns_animacy.csv")
    verbs = load_csv_rows("data/lexicons/verbs_roles.csv")

    noun_vals = [r["noun"] for r in nouns]
    noun_group = {r["noun"]: r["group"] for r in nouns}
    out: list[dict[str, Any]] = []

    while len(out) < n:
        agent, patient = rng.sample(noun_vals, k=2)
        verb = rng.choice(verbs)
        verb_past = verb["verb_past"]

        s = f"The {agent} {verb_past} the {patient}."
        s_cf = f"The {patient} {verb_past} the {agent}."
        pair_id = f"role_{len(out) + 1:06d}"
        split = split_from_id(pair_id, train=0.7, dev=0.15)

        record = build_pair_record(
            pair_id=pair_id,
            phenomenon="role_reversal",
            s=s,
            s_cf=s_cf,
            edit_type="swap_agent_patient",
            source="templated",
            template_id="role_active_transitive_v01",
            split=split,
            gold_label={
                "role_direction_s": f"{agent}_agent_{patient}_patient",
                "role_direction_cf": f"{patient}_agent_{agent}_patient",
                "negation_s": None,
                "negation_cf": None,
                "attachment_s": None,
                "attachment_cf": None,
            },
            edited_spans={
                "s": [
                    find_span_or_raise(s, agent, "agent"),
                    find_span_or_raise(s, patient, "patient"),
                ],
                "s_cf": [
                    find_span_or_raise(s_cf, patient, "agent"),
                    find_span_or_raise(s_cf, agent, "patient"),
                ],
            },
            linguistic_metadata={
                "agent_s": agent,
                "patient_s": patient,
                "agent_cf": patient,
                "patient_cf": agent,
                "verb_s": verb_past,
                "verb_cf": verb_past,
                "verb_base": verb["verb_base"],
                "voice_s": "active",
                "voice_cf": "active",
                "tense": "past",
                "animacy": "animate_animate",
                "plausibility_class": "reversible_plausible",
                "agent_group": noun_group[agent],
                "patient_group": noun_group[patient],
            },
        )
        out.append(record)

    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate role reversal css_pair_v1 JSONL")
    parser.add_argument("--config", default="configs/data/role.yaml")
    parser.add_argument("--n", type=int, default=None)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    cfg = load_yaml(args.config)
    n = int(args.n or cfg["n"])
    output = str(args.output or cfg["output_path"])
    seed = int(cfg["seed"])

    rows = generate_role_pairs(n=n, seed=seed)
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
