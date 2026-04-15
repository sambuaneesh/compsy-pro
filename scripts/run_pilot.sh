#!/usr/bin/env bash
set -euo pipefail

bash scripts/sync_external_dataset.sh
uv run python -m css.data.import_extending_psycholinguistic_dataset --config configs/data/external_import.yaml
uv run python -m css.data.merge_datasets \
  --inputs data/css_pairs/role_pilot_100.jsonl data/css_pairs/neg_pilot_100.jsonl \
  --output data/css_pairs/pilot_all_200.jsonl
uv run python -m css.data.validate_schema --config configs/experiments/pilot.yaml --output results/data_validation/pilot_schema_validation.json

uv run python -m css.representations.extract_hidden --config configs/experiments/pilot.yaml --force
uv run python -m css.metrics.compute_all_metrics --config configs/experiments/pilot.yaml
uv run python -m css.surprisal.gpt2_surprisal --config configs/experiments/surprisal.yaml
uv run python -m css.probes.train_linear_probe --config configs/experiments/probes.yaml

uv run python -m css.stats.dataset_only_summary --config configs/experiments/stats.yaml

echo "Pilot pipeline complete."
