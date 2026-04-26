#!/usr/bin/env bash
set -euo pipefail

uv run python -m css.analysis.qualitative_cases --config configs/experiments/qualitative_full.yaml

