# Phase 12 Report: Secondary Salience Experiment

Status: complete (exploratory)

What ran:
- `uv run python -m css.salience.token_contributions --config configs/experiments/salience_full.yaml`
- `uv run python -m css.salience.evaluate_salience --config configs/experiments/salience_full.yaml`

Outputs:
- `results/salience/token_contributions_full.csv` (174000 rows)
- `results/salience/salience_eval_full.csv` (16 summary rows)

Overall salience snapshot:
- Recall@1: `0.1336`
- Recall@3: `0.5063`
- MRR: `0.3965`
- AUC: `0.2423`

Notes:
- Salience remains secondary/exploratory.
- GPT-2 token-word alignment was corrected in cache extraction and salience was rerun end-to-end.
