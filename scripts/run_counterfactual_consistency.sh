#!/usr/bin/env bash
set -euo pipefail

uv run python -m css.consistency.counterfactual_consistency \
  --config configs/experiments/regular_modern_gpt2_consistency.yaml

uv run python -m css.consistency.counterfactual_consistency \
  --config configs/experiments/regular_modern_mistral_7b_consistency.yaml

uv run python -m css.consistency.counterfactual_consistency \
  --config configs/experiments/regular_modern_qwen3_4b_consistency.yaml

uv run python -m css.consistency.summarize_consistency \
  --config configs/experiments/regular_consistency_summary.yaml
