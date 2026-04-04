# Phase 04 Report: CSS Metrics

Status: complete

What ran:
- `uv run python -m css.metrics.compute_all_metrics --config configs/experiments/pilot.yaml`

Outputs:
- `results/metrics/layer_metrics.csv`
- `results/metrics/layer_metrics_summary.csv`
- `results/metrics/metric_warnings.json`

Notes:
- No Frobenius out-of-range warnings in pilot.
- Metrics include cosine, Frobenius, L2, and token-aligned shift.
