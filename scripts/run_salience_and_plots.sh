#!/usr/bin/env bash
set -euo pipefail

uv run python -m css.salience.token_contributions \
  --config configs/experiments/salience_full.yaml

uv run python -m css.salience.evaluate_salience \
  --config configs/experiments/salience_full.yaml

uv run python -m css.plots.plot_layer_curves \
  --config configs/experiments/plots_full.yaml

uv run python -m css.plots.plot_ablation_tables \
  --config configs/experiments/plots_full.yaml

echo "Salience + plots complete."
