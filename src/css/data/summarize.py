from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from typing import Any

from css.common.io import read_jsonl, write_json


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize CSS pair files")
    parser.add_argument("--inputs", nargs="+", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    summary: dict[str, Any] = {
        "total_rows": 0,
        "by_phenomenon": Counter(),
        "by_edit_type": Counter(),
        "by_template_id": Counter(),
        "by_split": Counter(),
        "split_by_phenomenon": defaultdict(Counter),
    }

    for path in args.inputs:
        for row in read_jsonl(path):
            summary["total_rows"] += 1
            p = str(row["phenomenon"])
            summary["by_phenomenon"][p] += 1
            summary["by_edit_type"][str(row["edit_type"])] += 1
            summary["by_template_id"][str(row["template_id"])] += 1
            summary["by_split"][str(row["split"])] += 1
            summary["split_by_phenomenon"][p][str(row["split"])] += 1

    summary["by_phenomenon"] = dict(summary["by_phenomenon"])
    summary["by_edit_type"] = dict(summary["by_edit_type"])
    summary["by_template_id"] = dict(summary["by_template_id"])
    summary["by_split"] = dict(summary["by_split"])
    summary["split_by_phenomenon"] = {k: dict(v) for k, v in summary["split_by_phenomenon"].items()}

    write_json(args.output, summary)
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
