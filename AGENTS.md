# AGENTS Operating Guide

This file defines the default operating rules for all future work in this repository.

## 1) Non-Negotiable Tooling Baseline

- Use **`uv`** for Python lifecycle management (Python versions, environments, dependencies, scripts).
- Use **`ruff`** for linting + formatting.
- Use **`ty`** for type checking.
- Use **`pytest`** for tests.
- Use **`pre-commit`** for local quality gates.

Do not use raw `pip`, `virtualenv`, or ad-hoc global installs unless explicitly required.

## 2) Command Policy

Use these command patterns by default:

- Dependency sync: `uv sync --all-groups`
- Add dependency: `uv add <pkg>`
- Add dev dependency: `uv add --group dev <pkg>`
- Run scripts/tools: `uv run <cmd>`
- One-off tool execution: `uvx <tool> ...`

## 3) Coding Quality Policy

Before every commit:

1. `uv run ruff check .`
2. `uv run ruff format --check .`
3. `uv run ty check`
4. `uv run pytest`

If any gate fails, fix before commit.

## 4) Commit Policy (Frequent Checkpoints)

- Commit after each logical feature chunk (roughly every 15-45 minutes of meaningful progress).
- Use Conventional Commit style:
- `feat: ...`
- `fix: ...`
- `docs: ...`
- `chore: ...`
- Keep commits small, scoped, and reversible.
- Prefer using `scripts/checkpoint_commit.sh` to enforce checks + commit in one step.

## 5) Documentation Policy

Every meaningful implementation change must update docs in `docs/`:

- Tooling/stack changes: `docs/STACK_AND_TOOLING.md`
- Workflow/process changes: `docs/WORKFLOW.md`
- Experiment decisions or assumptions: `docs/DECISIONS.md`

If a decision changes behavior, document rationale and date.

## 6) Secrets and Environment

- Secrets belong in `.env` only.
- `.env` must stay gitignored.
- Never hardcode tokens in source code, tests, docs, or notebooks.
- Use `python-dotenv` (or equivalent) for local secret loading.

## 7) Data and Artifact Hygiene

- Keep raw/intermediate/generated heavy files out of Git.
- Track only metadata/config/scripts needed for reproducibility.
- Document download sources and preprocessing in docs.

## 8) Experiment Reproducibility

Each experiment run should capture:

- code commit SHA
- config/version info
- model + dataset versions
- output path and timestamp

Store this metadata in run outputs and summarize in docs.
