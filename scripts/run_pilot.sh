#!/usr/bin/env bash
set -euo pipefail

uv run python -m css.data.generate_role --config configs/data/role.yaml
uv run python -m css.data.generate_negation --config configs/data/negation.yaml
uv run python -m css.data.generate_attachment --config configs/data/attachment.yaml
uv run python -m css.data.merge_datasets \
  --inputs data/css_pairs/role_pilot_100.jsonl data/css_pairs/neg_pilot_100.jsonl data/css_pairs/attach_pilot_100.jsonl \
  --output data/css_pairs/pilot_all_300.jsonl
uv run python -m css.data.validate_schema --config configs/experiments/pilot.yaml --output results/data_validation/pilot_schema_validation.json

uv run python -m css.representations.extract_hidden --config configs/experiments/pilot.yaml --force
uv run python -m css.metrics.compute_all_metrics --config configs/experiments/pilot.yaml
uv run python -m css.surprisal.gpt2_surprisal --config configs/experiments/surprisal.yaml
uv run python -m css.probes.train_linear_probe --config configs/experiments/probes.yaml

uv run python -m css.annotation.make_batches --config configs/experiments/surprisal.yaml --input data/css_pairs/pilot_all_300.jsonl --output data/annotations/annotation_batch_pilot.csv --n-per-phenomenon 30
uv run python -m css.annotation.simulate_annotations --batch data/annotations/annotation_batch_pilot.csv --output data/annotations/human_css_0_5.csv --annotators 3
uv run python -m css.annotation.aggregate_annotations --input data/annotations/human_css_0_5.csv --output data/annotations/human_css_aggregated.csv
uv run python -m css.annotation.agreement --input data/annotations/human_css_0_5.csv --output results/annotation/agreement_report.json

uv run python -m css.stats.correlations --config configs/experiments/stats.yaml

echo "Pilot pipeline complete."
