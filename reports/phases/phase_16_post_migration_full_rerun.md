# Phase 16: Post-Migration Full Rerun (2026-04-24)

## Objective

Recompute final-claim artifacts after switching role/negation to the external psycholinguistic dataset and locking dataset-only scope.

## Commands Executed

```bash
bash scripts/run_full_metrics.sh
bash scripts/run_probes.sh
bash scripts/run_stats.sh
bash scripts/run_salience_and_plots.sh
```

## Regenerated Artifacts

- Metrics:
  - `results/metrics/layer_metrics_full.csv` (117000 rows)
  - `results/metrics/layer_metrics_summary.csv`
  - `results/metrics/metric_warnings_full.json` (0 warnings)
- Surprisal:
  - `results/surprisal/gpt2_surprisal_full.csv` (3000 rows)
  - `results/surprisal/key_region_coverage_full.json` (coverage 1.0)
- Probes:
  - `results/probes/probe_results_full.csv` (390 rows)
  - `results/probes/probe_predictions_full.csv`
  - `results/probes/selectivity_summary_full.csv` (78 rows)
  - `results/probes/selectivity_summary_full.json`
- Statistics:
  - `results/stats/full/correlations.csv` (312 rows)
  - `results/stats/full/h2_incremental.csv` (78 rows)
  - `results/stats/full/hypothesis_tests.md`
- Salience + plots:
  - `results/salience/token_contributions_full.csv` (133044 rows)
  - `results/salience/salience_eval_full.csv`
  - `results/figures/*`

## Current Final-Claim Boundary

- Migration-related rerun requirement is closed.
- Dataset-only full pipeline is complete with no human-annotation dependency.
