from __future__ import annotations

import argparse
from collections import Counter
from typing import Any

from css.common.config import load_yaml
from css.common.hash_utils import sha256_file, sha256_json
from css.common.io import read_jsonl, write_json
from css.data.schema import validate_pair_record


def _extract_paths(config: dict[str, Any]) -> list[str]:
    if "datasets" in config and isinstance(config["datasets"], list):
        return [str(p) for p in config["datasets"]]
    maybe = []
    for k in ("role_path", "negation_path", "attachment_path"):
        if k in config:
            maybe.append(str(config[k]))
    if maybe:
        return maybe
    raise ValueError("Could not infer dataset paths from config")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate css_pair_v1 JSONL files")
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", default="results/data_validation/schema_validation_report.json")
    args = parser.parse_args()

    cfg = load_yaml(args.config)
    paths = _extract_paths(cfg)

    report: dict[str, Any] = {
        "config_path": args.config,
        "config_hash": sha256_json(cfg),
        "datasets": [],
        "total_rows": 0,
        "total_issues": 0,
        "status": "ok",
    }

    for path in paths:
        rows = read_jsonl(path)
        issues: list[dict[str, str]] = []
        ids = [row.get("id", "") for row in rows]
        duplicate_count = sum(v - 1 for v in Counter(ids).values() if v > 1)
        for row in rows:
            for issue in validate_pair_record(row):
                issues.append(
                    {"pair_id": issue.pair_id, "field": issue.field, "message": issue.message}
                )

        dataset_info = {
            "path": path,
            "sha256": sha256_file(path),
            "rows": len(rows),
            "duplicate_id_excess": duplicate_count,
            "issues_count": len(issues),
            "issues_preview": issues[:50],
        }
        report["datasets"].append(dataset_info)
        report["total_rows"] += len(rows)
        report["total_issues"] += len(issues) + duplicate_count

    if report["total_issues"] > 0:
        report["status"] = "fail"

    write_json(args.output, report)
    print(f"wrote {args.output} status={report['status']} issues={report['total_issues']}")

    if report["status"] != "ok":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
