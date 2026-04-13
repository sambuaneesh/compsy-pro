# Setup

## 1) Python and Environment

This project uses `uv` with a pinned Python in `.python-version`.

```bash
uv sync --all-groups
```

## 2) Secrets

Create `.env` from `.env.example` and set:

- `HF_TOKEN`
- `HUGGINGFACE_HUB_TOKEN`

The `.env` file is gitignored and should never be committed.

## 3) Quality Gates

```bash
uv run ruff check .
uv run ruff format --check .
uv run ty check
uv run pytest
```

## 4) External Dataset Sync (Role + Negation)

```bash
bash scripts/sync_external_dataset.sh
```

If already cloned, pull updates:

```bash
bash scripts/sync_external_dataset.sh
```

## 5) Git Hooks

Install hooks:

```bash
uv run pre-commit install --hook-type pre-commit --hook-type pre-push
```
