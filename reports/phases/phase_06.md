# Phase 06 Report: Probes With Controls

Status: complete

What ran:
- `uv run python -m css.probes.train_linear_probe --config configs/experiments/probes.yaml`

Outputs:
- `results/probes/probe_results.csv`
- `results/probes/probe_predictions.csv`
- `results/probes/selectivity_summary.csv`
- `results/probes/selectivity_summary.json`

Notes:
- Pilot includes role and negation probes over layers with 5 seeds.
- Random-label control included and selectivity reported.
