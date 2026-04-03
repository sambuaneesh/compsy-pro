# Workflow

Last updated: `2026-04-24`

## Daily Development Flow

1. Sync environment:
```bash
uv sync --all-groups
```

2. Implement feature in small increments.

3. Run gates:
```bash
uv run ruff check .
uv run ruff format --check .
uv run ty check
uv run pytest
```

4. Update docs for behavioral/tooling changes.

5. Commit with conventional message.

## Commit Cadence

- Commit every logical chunk (small, reviewable, reversible).
- Avoid large mixed commits.
- Include docs updates in the same commit when relevant.
- After each logical chunk, append an incremental JSONL log event in `logs/incremental/`.

## Environment and Secrets

- Store secrets in `.env` only.
- `.env` is gitignored and should never be committed.
- Use `.env.example` as the template for required variables.

## Download and Long-Running Tasks

- Start long downloads (models/datasets) early when planning experiments.
- Document source, version, and checksum when available.
- Keep large binaries out of Git and use tracked metadata instead.

## Incremental Logging Command

```bash
uv run python scripts/log_event.py \
  --phase 0 \
  --event-type chore \
  --summary "ran tooling checks and committed baseline" \
  --artifact pyproject.toml \
  --artifact uv.lock
```
