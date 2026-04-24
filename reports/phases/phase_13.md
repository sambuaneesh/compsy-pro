# Phase 13 Report: Paper and Artifact Packaging

Status: complete

What ran:
- `uv run python -m css.plots.plot_layer_curves --config configs/experiments/plots_full.yaml`
- `uv run python -m css.plots.plot_ablation_tables --config configs/experiments/plots_full.yaml`

Primary outputs:
- Figures:
  - `results/figures/layer_correlation_curves.pdf`
  - `results/figures/probe_selectivity_curves.pdf`
  - `results/figures/surprisal_vs_human.pdf`
- Tables:
  - `results/figures/top_layer_by_metric.csv`
  - `results/figures/frob_incremental_positive.csv`
  - `results/figures/frob_incremental_summary.csv`
  - mirrored in `results/tables/`
- Paper/appendix drafts:
  - `reports/workshop_paper/paper.md`
  - `reports/appendix/annotation_prompt.md`
  - `reports/appendix/references.md`

Notes:
- All figures and tables are script-generated.
- Paper framing preserves the non-overclaim rule (human-alignment, not human-equivalence).
