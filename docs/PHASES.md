# CSS Execution Phases

Last updated: `2026-04-24`

This is the canonical phase order for implementing:
**Counterfactual Structural Sensitivity: Human-Aligned Probing of Language Model Representations under Minimal Linguistic Edits**.

## Phase 0: Governance, Tooling, and Reproducibility Baseline

Objective:
- Lock repo process and experiment hygiene before model work.

Deliverables:
- `AGENTS.md` finalized and enforced.
- `pyproject.toml` + `uv.lock` synced.
- pre-commit hooks installed and passing.
- incremental log system initialized.

Exit criteria:
- `uv run ruff check .`, `uv run ty check`, `uv run pytest` all pass.
- logging command can append structured entries.

## Phase 1: Schema and Config Freeze (v1)

Objective:
- Implement and freeze `css_pair_v1`, cache metadata schema, metric schema.

Deliverables:
- schema validators and tests.
- `configs/data/*.yaml`, `configs/experiments/pilot.yaml`.
- schema changelog and hash utility.

Exit criteria:
- schema validator passes on sample files.
- config hash + dataset hash emitted in run manifests.

## Phase 2: Lexicons and Dataset Generation Pipeline

Objective:
- Build/ingest role, negation, and attachment datasets with strict controls.

Deliverables:
- `import_extending_psycholinguistic_dataset.py`, `generate_attachment.py`.
- `split_data.py`, `validate_schema.py`.
- pilot data files: 100/100/100.

Exit criteria:
- no duplicate IDs, full required metadata, surface controls complete.
- lexical/template split diagnostics generated.

## Phase 3: Representation Extraction and Caching

Objective:
- Extract hidden states for BERT, RoBERTa, GPT-2 (embedding + 12 layers).

Deliverables:
- extraction, pooling, token-alignment, cache I/O modules.
- cache metadata with versions/hashes/seeds/dtype.

Exit criteria:
- cache reload works without re-tokenization.
- word-level aggregation validated.

## Phase 4: Core CSS Metrics

Objective:
- Compute `delta_cos`, `sim_frob`, `delta_frob`, `delta_l2`, `delta_token_aligned`.

Deliverables:
- metric modules + `compute_all_metrics.py`.
- anomaly report for out-of-range Frobenius values.

Exit criteria:
- deterministic reruns with identical outputs.
- unit tests for matrix norm math pass.

## Phase 5: GPT-2 Surprisal Pipeline

Objective:
- Compute primary autoregressive surprisal features.

Deliverables:
- token-level and sentence-level surprisal outputs.
- key-region surprisal extraction.

Exit criteria:
- >=98% key-region coverage or documented failures.
- primary stats-ready surprisal table generated.

## Phase 6: Probe System With Selectivity Controls

Objective:
- Train linear probes for role/negation/attachment with robust controls.

Deliverables:
- probe dataset builder, trainer, selectivity controls.
- 5-seed results for random/template/lexical splits.

Exit criteria:
- each probe result has matching control score.
- selectivity summary exported.

## Phase 7: Human Annotation Pilot and Calibration

Objective:
- Run pilot annotation to validate prompt and agreement.

Deliverables:
- 60-90 annotated items, 3 annotators/item.
- agreement report and prompt revision decision.

Exit criteria:
- agreement sufficient for full collection or revised prompt frozen.

## Phase 8: Pilot Integration and Go/No-Go

Objective:
- Test H1-H4 signal viability on pilot end-to-end.

Deliverables:
- pilot correlations by layer/model/phenomenon.
- preliminary mixed-model fit.
- pilot figures/tables.

Exit criteria:
- interpretable layer curves.
- stable metric computation and reproducible rerun.

## Phase 9: Full Data and Full Cache Build

Objective:
- Scale to 1,500 x 3 phenomena and all 3 models.

Deliverables:
- full pair datasets validated.
- full hidden-state caches and metrics.

Exit criteria:
- full manifests with hashes and environment metadata.
- storage/runtime report documented.

## Phase 10: Full Human Annotation

Objective:
- Produce primary human target set (minimum 300 balanced pairs).

Deliverables:
- raw annotation CSV + aggregated CSV.
- agreement diagnostics and disagreement flags.

Exit criteria:
- minimum annotator coverage met.
- quality checks pass.

## Phase 11: Final Statistics for H1-H5

Objective:
- Run final hypothesis tests with controls and corrections.

Deliverables:
- Spearman/Pearson tables by layer.
- mixed-effects models with random intercepts.
- bootstrap CIs and BH-FDR corrected results.

Exit criteria:
- H1-H5 status table complete.
- incremental value test (`Delta_frob` over `Delta_cos`) complete.

## Phase 12: Secondary Salience Experiment

Objective:
- Evaluate token/span salience ranking from CSS metrics.

Deliverables:
- salience contribution files.
- Recall@1, Recall@3, MRR (AUC optional).

Exit criteria:
- explicitly labeled exploratory in outputs.

## Phase 13: Paper and Artifact Packaging

Objective:
- Produce workshop-ready manuscript and reproducibility package.

Deliverables:
- main paper draft, appendix, figures, tables, references.
- reproducibility checklist and runbook.

Exit criteria:
- all claims map to traceable scripts and logged runs.
- limitations and non-overclaim framing included.

## Phase 14: Final Audit and Submission Readiness

Objective:
- Validate completeness, consistency, and workshop fit.

Deliverables:
- final gap report, checklist closure, submission bundle.

Exit criteria:
- all primary deliverables complete.
- repo can rerun core pipeline from clean checkout.
