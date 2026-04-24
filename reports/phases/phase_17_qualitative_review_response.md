# Phase 17 Report: Qualitative Review Response

Status: complete

Purpose:
- Address review feedback requesting deeper qualitative analysis.
- Connect aggregate CSS metrics to concrete sentence-pair behavior.
- Explain why mean shift magnitude and layer-wise shift-surprisal correlation are not contradictory.

Implemented artifacts:
- `src/css/analysis/qualitative_cases.py`
- `configs/experiments/qualitative_full.yaml`
- `results/qualitative/pair_level_summary.csv`
- `results/qualitative/surface_summary.csv`
- `results/qualitative/qualitative_cases.csv`
- `reports/full/QUALITATIVE_ANALYSIS.md`

Main qualitative findings:
- Negation has lower mean lexical overlap (`0.4853`) and about one token of average length change, so larger pooled mean shifts are expected.
- Role reversal has higher mean lexical overlap (`0.7973`) and near-zero average length change, so its smaller pooled mean shift does not contradict cleaner shift-surprisal correlations.
- Source-generated examples contain occasional article mismatches, lexical substitutions, and implausible continuations; this supports conservative dataset-only claim language.
- High/low Frobenius-surprisal dissociation cases show that representation geometry and GPT-2 surprisal are complementary diagnostics.

Documentation updates:
- `reports/full/RESULTS_INTERPRETATION.md`
- `reports/workshop_paper/paper.md`
- `reports/slides/CSS_Project_Presentation.tex`
- `reports/slides/CSS_Project_Presentation_TRANSCRIPT.md`
- `README.md`
- `PROJECT_RESEARCH_PLAN.md`

Verification:
- `uv run ruff check src/css/analysis/qualitative_cases.py src/css/analysis/__init__.py` passes.
- `uv run python -m css.analysis.qualitative_cases --config configs/experiments/qualitative_full.yaml` regenerates qualitative tables and report.

