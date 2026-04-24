# Phase 07 Report: Annotation Pilot

Status: complete (pipeline), human data pending

What ran:
- `uv run python -m css.annotation.make_batches ...`
- `uv run python -m css.annotation.simulate_annotations ...`
- `uv run python -m css.annotation.aggregate_annotations ...`
- `uv run python -m css.annotation.agreement ...`

Outputs:
- `data/annotations/annotation_batch_pilot.csv`
- `data/annotations/human_css_0_5.csv`
- `data/annotations/human_css_aggregated.csv`
- `results/annotation/agreement_report.json`

Important:
- Current annotation file is **SIMULATED** to test pipeline continuity while real annotators are unavailable.
- Replace with real human ratings before paper claims.
