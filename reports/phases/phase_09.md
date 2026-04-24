# Phase 09 Report: Full Cache Build and Full Metrics

Status: complete

What ran:
- `uv run python -m css.representations.extract_hidden --config configs/experiments/full.yaml --force`
- `uv run python -m css.metrics.compute_all_metrics --config configs/experiments/full.yaml ...`
- `uv run python -m css.surprisal.gpt2_surprisal --config configs/experiments/surprisal_full.yaml`

Outputs:
- Full hidden caches for BERT, RoBERTa, GPT-2 across role/negation/attachment full datasets.
- `results/metrics/layer_metrics_full.csv`
- `results/metrics/metric_warnings_full.json`
- `results/surprisal/gpt2_surprisal_full.csv`
- `results/surprisal/key_region_coverage_full.json`

Notes:
- Full metrics rows: 175,500
- Frobenius out-of-range warnings: 0
- Full surprisal rows: 4,500 (key-region coverage: 1.0)
