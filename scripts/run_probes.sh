#!/usr/bin/env bash
set -euo pipefail

uv run python -m css.probes.train_linear_probe \
  --config configs/experiments/full_probes.yaml \
  --output results/probes/probe_results_full.csv \
  --pred-output results/probes/probe_predictions_full.csv \
  --summary-output results/probes/selectivity_summary_full.csv \
  --summary-json-output results/probes/selectivity_summary_full.json

echo "Full probe training complete."
