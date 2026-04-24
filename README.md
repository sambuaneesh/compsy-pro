# Compsy

Counterfactual structural probing experiments for language models with human-aligned psycholinguistic evaluation.

## Quick Start (Modern Stack)

1. Install dependencies and create the project environment:
```bash
uv sync --all-groups
```

2. Run quality gates:
```bash
uv run ruff check .
uv run ruff format --check .
uv run ty check
uv run pytest
```

3. Copy `.env.example` to `.env` and set secrets (already done locally in this workspace).

## Project Layout

- `src/`: implementation code
- `tests/`: tests
- `docs/`: project documentation and decisions
- `papers/`: reference papers

## Core Principle

Use `uv` and the Astral toolchain (`ruff`, `ty`) by default for all Python workflows.

## Pilot Pipeline

Run the end-to-end pilot (Phases 2-8):

```bash
bash scripts/run_pilot.sh
```

## Full Pipeline

Run full extraction/metrics/surprisal:

```bash
bash scripts/run_full_metrics.sh
```

Run full probes:

```bash
bash scripts/run_probes.sh
```

Run annotation fallback + stats:

```bash
bash scripts/run_stats.sh
```

Run secondary salience + figures/tables:

```bash
bash scripts/run_salience_and_plots.sh
```
