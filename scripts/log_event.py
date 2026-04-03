"""Append structured incremental logs for CSS project phases."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
from pathlib import Path


def _now_utc_iso() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _git_commit() -> str | None:
    try:
        out = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
        return out
    except Exception:
        return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Append a JSONL incremental log event.")
    parser.add_argument("--phase", type=int, required=True, help="Phase number, e.g., 0..14")
    parser.add_argument("--event-type", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--status", choices=["ok", "warn", "fail"], default="ok")
    parser.add_argument("--artifact", action="append", default=[])
    parser.add_argument("--command", default="")
    parser.add_argument("--notes", default="")
    args = parser.parse_args()

    log_dir = Path("logs/incremental")
    log_dir.mkdir(parents=True, exist_ok=True)
    path = log_dir / f"phase_{args.phase:02d}.jsonl"

    record = {
        "ts_utc": _now_utc_iso(),
        "phase": args.phase,
        "event_type": args.event_type,
        "summary": args.summary,
        "artifacts": args.artifact,
        "command": args.command,
        "status": args.status,
        "git_commit": _git_commit(),
        "notes": args.notes,
    }

    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=True) + "\n")

    print(f"logged -> {path}")


if __name__ == "__main__":
    main()
