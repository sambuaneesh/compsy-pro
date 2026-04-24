from __future__ import annotations

import argparse
import hashlib
from typing import Any

from css.common.io import read_jsonl, write_jsonl


def split_from_id(identifier: str, train: float, dev: float) -> str:
    h = int(hashlib.sha256(identifier.encode("utf-8")).hexdigest(), 16) % 10_000
    u = h / 10_000.0
    if u < train:
        return "train"
    if u < train + dev:
        return "dev"
    return "test"


def apply_splits(rows: list[dict[str, Any]], train: float, dev: float) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        copied = dict(row)
        copied["split"] = split_from_id(str(row["id"]), train=train, dev=dev)
        out.append(copied)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Recompute deterministic train/dev/test split field"
    )
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--train", type=float, default=0.7)
    parser.add_argument("--dev", type=float, default=0.15)
    args = parser.parse_args()

    rows = read_jsonl(args.input)
    rows = apply_splits(rows, train=args.train, dev=args.dev)
    write_jsonl(args.output, rows)
    print(f"wrote {args.output} rows={len(rows)}")


if __name__ == "__main__":
    main()
