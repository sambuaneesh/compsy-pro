from __future__ import annotations

import argparse

from css.common.io import read_jsonl, write_jsonl


def main() -> None:
    parser = argparse.ArgumentParser(description="Merge multiple JSONL files")
    parser.add_argument("--inputs", nargs="+", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    rows = []
    for path in args.inputs:
        rows.extend(read_jsonl(path))

    rows = sorted(rows, key=lambda r: str(r.get("id", "")))
    write_jsonl(args.output, rows)
    print(f"wrote {args.output} rows={len(rows)}")


if __name__ == "__main__":
    main()
