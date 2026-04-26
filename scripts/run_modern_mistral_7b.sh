#!/usr/bin/env bash
set -euo pipefail

uv run python -m css.representations.extract_hidden \
  --config configs/experiments/regular_modern_mistral_7b.yaml \
  --output results/manifests/extract_hidden_modern_mistral_7b_manifest.json

uv run python -m css.metrics.compute_all_metrics \
  --config configs/experiments/regular_modern_mistral_7b.yaml \
  --output results/metrics/modern_mistral_7b_metrics.csv \
  --warnings-output results/metrics/modern_mistral_7b_metric_warnings.json

uv run python -m css.stats.dataset_only_summary \
  --config configs/experiments/regular_modern_stats_mistral_7b.yaml

uv run python -m css.analysis.qualitative_cases \
  --config configs/experiments/regular_modern_qualitative_mistral_7b.yaml
