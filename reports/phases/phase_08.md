# Phase 08 Report: Pilot Integration and Go/No-Go

Status: complete

What ran:
- `uv run python -m css.stats.correlations --config configs/experiments/stats.yaml`

Outputs:
- `results/stats/correlations.csv`
- `results/stats/bootstrap_cis.csv`
- `results/stats/h2_incremental.csv`
- `results/stats/hypothesis_tests.md`

Pilot criteria snapshot:
- Hidden-state cache: pass
- Frobenius boundedness: pass (`n_warnings = 0`)
- Agreement pipeline: pass (simulated pilot)
- Layer-wise variance: pass
- Surface controls present: pass

Go/No-Go:
- **Go for engineering scale-up.**
- **No-go for publication-level human-alignment claims until real human annotations replace simulated data.**
