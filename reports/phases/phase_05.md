# Phase 05 Report: GPT-2 Surprisal

Status: complete

What ran:
- `uv run python -m css.surprisal.gpt2_surprisal --config configs/experiments/surprisal.yaml`

Outputs:
- `results/surprisal/gpt2_surprisal.csv`
- `results/surprisal/key_region_coverage.json`

Notes:
- Key-region coverage reached 100% on pilot.
- This is the primary surprisal pipeline; MLM PLL remains optional.
