# CSS Execution Phases (Dataset-Only)

Last updated: `2026-04-24`

This phase plan is locked to role + negation from the GitHub source dataset.

## Phase 0: Tooling and Reproducibility Baseline

Objective:
- lock `uv` environment, lint/type/test gates, and incremental logging.

Exit criteria:
- `uv run ruff check .`
- `uv run ty check`
- `uv run pytest`

## Phase 1: Schema and Config Freeze

Objective:
- freeze `css_pair_v1`, cache metadata schema, and experiment configs.

Exit criteria:
- schema validation passes on pilot and full configs.

## Phase 2: Data Import and Validation

Objective:
- import role and negation from external GitHub dataset.

Exit criteria:
- `role_1500.jsonl` and `neg_1500.jsonl` validated.

## Phase 3: Hidden-State Extraction

Objective:
- extract and cache hidden states for BERT, RoBERTa, GPT-2 (layers 0..12).

Exit criteria:
- cache manifests complete and reloadable.

## Phase 4: Metrics

Objective:
- compute cosine/Frobenius/L2/token-aligned shifts for all pairs/layers/models.

Exit criteria:
- metrics table complete, deterministic rerun verified.

## Phase 5: GPT-2 Surprisal

Objective:
- compute AR surprisal features and edited-region coverage.

Exit criteria:
- full surprisal table generated with coverage report.

## Phase 6: Probes and Selectivity

Objective:
- train role and negation probes with random-label controls and 5 seeds.

Exit criteria:
- selectivity summaries complete.

## Phase 7: Dataset-Only Statistics

Objective:
- run metric-surprisal correlations, bootstrap CIs, FDR correction, and Frobenius incremental tests.

Exit criteria:
- `results/stats/full/*` complete.

## Phase 8: Salience and Figures

Objective:
- generate salience outputs and all figures/tables from scripts.

Exit criteria:
- figures/tables reproducibly generated from current outputs.

## Phase 9: Packaging

Objective:
- finalize report/slides language for dataset-only claims and submission readiness.

Exit criteria:
- no human-annotation dependency in claims or required pipeline steps.
