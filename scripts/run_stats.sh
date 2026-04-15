#!/usr/bin/env bash
set -euo pipefail

uv run python -m css.stats.dataset_only_summary \
  --config configs/experiments/stats_full.yaml

echo "Full dataset-only stats complete."
