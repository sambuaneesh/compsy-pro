#!/usr/bin/env bash
set -euo pipefail

uv run python -m css.annotation.make_batches \
  --config configs/experiments/annotation_full.yaml \
  --input data/css_pairs/full_all_4500.jsonl \
  --output data/annotations/annotation_batch_full.csv \
  --n-per-phenomenon 100

uv run python -m css.annotation.simulate_annotations \
  --batch data/annotations/annotation_batch_full.csv \
  --output data/annotations/human_css_0_5_full.csv \
  --annotators 3

uv run python -m css.annotation.aggregate_annotations \
  --input data/annotations/human_css_0_5_full.csv \
  --output data/annotations/human_css_aggregated_full.csv

uv run python -m css.annotation.agreement \
  --input data/annotations/human_css_0_5_full.csv \
  --output results/annotation/agreement_report_full.json

uv run python -m css.stats.correlations \
  --config configs/experiments/stats_full.yaml

uv run python -m css.stats.mixed_effects \
  --config configs/experiments/stats_full.yaml

echo "Full annotation fallback + stats complete."
