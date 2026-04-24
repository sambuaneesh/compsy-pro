# Phase 12 Report: Secondary Salience Experiment

Status: complete (exploratory)

What ran:
- `uv run python -m css.salience.token_contributions --config configs/experiments/salience_full.yaml`
- `uv run python -m css.salience.evaluate_salience --config configs/experiments/salience_full.yaml`

Outputs:
- `results/salience/token_contributions_full.csv` (135000 rows)
- `results/salience/salience_eval_full.csv` (16 summary rows)

Overall salience snapshot:
- Recall@1: `0.0989`
- Recall@3: `0.5696`
- MRR: `0.3974`
- AUC: `0.1883`

Notes:
- Salience remains secondary/exploratory.
- GPT-2 token-word alignment mismatch required robust truncation logic in this phase.
