# Incremental Serialized Logs

Purpose:
- Maintain high-granularity, machine-readable project history for reproducibility and paper drafting.

Format:
- JSON Lines (`.jsonl`), one event per line.
- One file per phase:
  - `phase_00.jsonl`, `phase_01.jsonl`, ..., `phase_14.jsonl`

Required fields per event:

```json
{
  "ts_utc": "2026-04-24T05:20:00Z",
  "phase": 0,
  "event_type": "setup|data|extract|metrics|surprisal|probe|annotation|stats|salience|paper|chore",
  "summary": "Short description of action",
  "artifacts": ["path/or/id"],
  "command": "uv run ...",
  "status": "ok|warn|fail",
  "git_commit": "optional_sha",
  "notes": "optional details"
}
```

Rules:
- Append logs in time order.
- Never rewrite historical lines; append corrections as new events.
- Add at least one log event per meaningful action block.
- Include the resulting commit SHA whenever available.
