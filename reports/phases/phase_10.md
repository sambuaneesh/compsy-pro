# Phase 10 Report: Full Human Annotation (Fallback Mode)

Status: complete (fallback)

What ran:
- `uv run python -m css.annotation.make_batches --config configs/experiments/annotation_full.yaml --input data/css_pairs/full_all_4500.jsonl --output data/annotations/annotation_batch_full.csv --n-per-phenomenon 100`
- `uv run python -m css.annotation.simulate_annotations --batch data/annotations/annotation_batch_full.csv --output data/annotations/human_css_0_5_full.csv --annotators 3`
- `uv run python -m css.annotation.aggregate_annotations --input data/annotations/human_css_0_5_full.csv --output data/annotations/human_css_aggregated_full.csv`
- `uv run python -m css.annotation.agreement --input data/annotations/human_css_0_5_full.csv --output results/annotation/agreement_report_full.json`

Outputs:
- `data/annotations/annotation_batch_full.csv` (300 pairs; 100 per phenomenon)
- `data/annotations/human_css_0_5_full.csv` (900 rows; 3 annotators/item)
- `data/annotations/human_css_aggregated_full.csv` (300 rows)
- `results/annotation/agreement_report_full.json`

Agreement snapshot:
- mean pairwise Spearman: `0.6331`
- median pairwise Spearman: `0.6330`
- high-disagreement rate (`range >= 3`): `0.0`

Notes:
- This phase currently uses synthetic annotations to keep the full pipeline executable end-to-end.
- Replace with real human ratings before publication claims.
