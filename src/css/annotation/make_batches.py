from __future__ import annotations

import argparse
import random
from collections import defaultdict
from typing import Any

import pandas as pd

from css.common.config import load_yaml
from css.common.io import ensure_dir, read_jsonl


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create balanced annotation batches from CSS pairs."
    )
    parser.add_argument("--config", required=True)
    parser.add_argument("--input", default=None)
    parser.add_argument("--output", default="data/annotations/annotation_batch_pilot.csv")
    parser.add_argument("--n-per-phenomenon", type=int, default=30)
    parser.add_argument("--seed", type=int, default=13)
    args = parser.parse_args()

    cfg = load_yaml(args.config)
    input_path = str(args.input or cfg.get("dataset", "data/css_pairs/pilot_all_300.jsonl"))
    rows = read_jsonl(input_path)
    rng = random.Random(args.seed)

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["phenomenon"])].append(row)

    selected: list[dict[str, Any]] = []
    for _phenomenon, items in grouped.items():
        rng.shuffle(items)
        selected.extend(items[: args.n_per_phenomenon])

    rng.shuffle(selected)
    out_rows = []
    for i, row in enumerate(selected, start=1):
        out_rows.append(
            {
                "batch_item_id": i,
                "pair_id": row["id"],
                "phenomenon": row["phenomenon"],
                "s": row["s"],
                "s_cf": row["s_cf"],
                "annotation_prompt_version": "css_human_change_v1",
            }
        )

    ensure_dir("data/annotations")
    pd.DataFrame(out_rows).to_csv(args.output, index=False)
    print(f"wrote {args.output} rows={len(out_rows)}")


if __name__ == "__main__":
    main()
