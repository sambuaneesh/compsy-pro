# Compsy

Counterfactual structural probing experiments for language models using a strict dataset-only evaluation track.

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

4. Sync external psycholinguistic source data (required for role + negation):
```bash
bash scripts/sync_external_dataset.sh
```

## Project Layout

- `src/`: implementation code
- `tests/`: tests
- `docs/`: project documentation and decisions
- `papers/`: reference papers

## Core Principle

Use `uv` and the Astral toolchain (`ruff`, `ty`) by default for all Python workflows.

## Dataset Source (Current)

- Role reversal and negation come from:
  - `text-machine-lab/extending_psycholinguistic_dataset`
  - imported through `python -m css.data.import_extending_psycholinguistic_dataset`
- Active full dataset is `data/css_pairs/full_all_3000.jsonl` (role + negation only).

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

Run dataset-only stats:

```bash
bash scripts/run_stats.sh
```

Run secondary salience + figures/tables:

```bash
bash scripts/run_salience_and_plots.sh
```

Run final RQ analysis summaries:

```bash
uv run python scripts/analyze_results_for_rq.py
```

Key interpretation output:

- `reports/full/RESULTS_INTERPRETATION.md`

Future-scope note (including attachment/PP re-entry and human-eval conditions):

- `reports/full/FUTURE_WORK.md`
