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


def generate_attachment_pairs(n: int, seed: int) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    nouns = [r["noun"] for r in load_csv_rows("data/lexicons/nouns_animacy.csv")]
    pp_rows = load_csv_rows("data/lexicons/pp_instruments_attributes.csv")

    edit_types = ["vp_to_np", "ambiguous_to_vp", "ambiguous_to_np"]
    out: list[dict[str, Any]] = []

    while len(out) < n:
        subject = rng.choice(nouns)
        row = rng.choice(pp_rows)
        obj = row["head_np"]
        pp_np = row["pp_np"]
        vp_verb = row["head_vp"]

        ambiguous = f"The {subject} {vp_verb} the {obj} with the {pp_np}."
        vp_dis = f"With the {pp_np}, the {subject} {vp_verb} the {obj}."
        np_dis = f"The {subject} {vp_verb} the {obj} who had the {pp_np}."

        edit_type = edit_types[len(out) % len(edit_types)]
        if edit_type == "vp_to_np":
            s, s_cf = vp_dis, np_dis
            att_s, att_cf = "VP_attachment", "NP_attachment"
        elif edit_type == "ambiguous_to_vp":
            s, s_cf = ambiguous, vp_dis
            att_s, att_cf = "ambiguous", "VP_attachment"
        else:
            s, s_cf = ambiguous, np_dis
            att_s, att_cf = "ambiguous", "NP_attachment"

        pair_id = f"attach_{len(out) + 1:06d}"
        split = split_from_id(pair_id, train=0.7, dev=0.15)

        out.append(
            build_pair_record(
                pair_id=pair_id,
                phenomenon="attachment",
                s=s,
                s_cf=s_cf,
                edit_type=edit_type,
                source="templated",
                template_id="attach_pp_v01",
                split=split,
                gold_label={
                    "role_direction_s": None,
                    "role_direction_cf": None,
                    "negation_s": None,
                    "negation_cf": None,
                    "attachment_s": att_s,
                    "attachment_cf": att_cf,
                },
                edited_spans={
                    "s": [
                        find_span_or_raise(
                            s, f"with the {pp_np}" if "with the" in s else f"the {pp_np}", "pp_span"
                        ),
                        find_span_or_raise(s, obj, "head_np"),
                    ],
                    "s_cf": [
                        find_span_or_raise(
                            s_cf,
                            f"with the {pp_np}" if "with the" in s_cf else f"the {pp_np}",
                            "pp_span",
                        ),
                        find_span_or_raise(s_cf, obj, "head_np"),
                    ],
                },
                linguistic_metadata={
                    "attachment_site": "pp_attachment",
                    "attachment_class_s": att_s,
                    "attachment_class_cf": att_cf,
                    "pp_span_text": f"the {pp_np}",
                    "head_candidate_1": obj,
                    "head_candidate_2": vp_verb,
                },
            )
        )

    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate attachment css_pair_v1 JSONL")
    parser.add_argument("--config", default="configs/data/attachment.yaml")
    parser.add_argument("--n", type=int, default=None)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    cfg = load_yaml(args.config)
    n = int(args.n or cfg["n"])
    output = str(args.output or cfg["output_path"])
    seed = int(cfg["seed"])

    rows = generate_attachment_pairs(n=n, seed=seed)
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
