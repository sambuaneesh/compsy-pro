# Phase 11 Report: Final Statistics for H1-H5

Status: complete

What ran:
- `uv run python -m css.stats.correlations --config configs/experiments/stats_full.yaml`
- `uv run python -m css.stats.mixed_effects --config configs/experiments/stats_full.yaml`

Outputs:
- `results/stats/full/correlations.csv` (468 rows)
- `results/stats/full/bootstrap_cis.csv`
- `results/stats/full/h2_incremental.csv` (117 rows)
- `results/stats/full/mixed_effects_summary.csv` (13 layer fits)
- `results/stats/full/hypothesis_tests.md`

Key run notes:
- Spearman/Pearson FDR-corrected tables regenerated after full probe coverage refresh.
- Mixed-effects runner now applies robust predictor fallback when singularity is detected; all 13 layers fit with `converged=True`.
- Boundary convergence warnings from `statsmodels` remain but no layer-level fit failures persisted.

Interpretation boundary:
- Results are pipeline-valid and traceable.
- Final scientific interpretation still depends on replacing simulated annotations.
