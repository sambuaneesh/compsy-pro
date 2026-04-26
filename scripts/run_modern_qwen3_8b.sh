#!/usr/bin/env bash
set -euo pipefail

uv run python -m css.representations.extract_hidden \
  --config configs/experiments/regular_modern_qwen3_8b.yaml \
  --output results/manifests/extract_hidden_modern_qwen3_8b_manifest.json

uv run python -m css.metrics.compute_all_metrics \
  --config configs/experiments/regular_modern_qwen3_8b.yaml \
  --output results/metrics/modern_qwen3_8b_metrics.csv \
  --warnings-output results/metrics/modern_qwen3_8b_metric_warnings.json

uv run python -m css.stats.dataset_only_summary \
  --config configs/experiments/regular_modern_stats_qwen3_8b.yaml

uv run python -m css.analysis.qualitative_cases \
  --config configs/experiments/regular_modern_qualitative_qwen3_8b.yaml

