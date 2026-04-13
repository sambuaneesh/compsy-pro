#!/usr/bin/env bash
set -euo pipefail

bash scripts/sync_external_dataset.sh
uv run python -m css.data.import_extending_psycholinguistic_dataset --config configs/data/external_import.yaml
uv run python -m css.data.generate_attachment --config configs/data/attachment.yaml

uv run python -m css.data.merge_datasets \
  --inputs data/css_pairs/role_1500.jsonl data/css_pairs/neg_1500.jsonl data/css_pairs/attach_1500.jsonl \
  --output data/css_pairs/full_all_4500.jsonl

uv run python -m css.data.validate_schema \
  --config configs/experiments/full.yaml \
  --output results/data_validation/full_schema_validation.json

uv run python -m css.representations.extract_hidden \
  --config configs/experiments/full.yaml

uv run python -m css.metrics.compute_all_metrics \
  --config configs/experiments/full.yaml \
  --output results/metrics/layer_metrics_full.csv \
  --warnings-output results/metrics/metric_warnings_full.json

uv run python -m css.surprisal.gpt2_surprisal \
  --config configs/experiments/surprisal_full.yaml

echo "Full extraction/metrics/surprisal complete."
