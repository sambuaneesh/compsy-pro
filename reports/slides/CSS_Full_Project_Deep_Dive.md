---
marp: true
theme: default
paginate: true
size: 16:9
title: Counterfactual Structural Sensitivity (CSS)
author: Compsy Project Repository (commit 76ee726)
description: End-to-end deep technical walkthrough with methods, math, implementation, results, caveats, and references.
---

# Counterfactual Structural Sensitivity (CSS)
## Human-Aligned Probing of LM Representations under Minimal Linguistic Edits

Deep technical walkthrough (full repository implementation and experiment artifacts)

- Project repo: `/home/srinath/Shyshtum/compsy`
- Snapshot commit: `76ee726`
- Date: 2026-04-24

---

# Deck Scope

This deck is intentionally exhaustive and includes:

- Problem framing and exact claims/non-claims.
- All hypotheses (H1-H5) and mathematical definitions.
- Dataset schemas, generation logic, and controls.
- Full implementation map (modules, configs, scripts, logs).
- Full run outputs (metrics, probes, surprisal, stats, salience).
- Reproducibility, failure modes, and next-step fixes.

---

# Reading Guide

Sections:

1. Scientific framing and hypotheses.
2. Literature and rationale.
3. Dataset design and generation.
4. Representation extraction and metrics.
5. Probes, surprisal, annotation, statistics.
6. Full run outputs and interpretation.
7. Engineering pipeline and reproducibility.
8. Known limitations and concrete remediation plan.
9. References and appendices.

---

# Core Research Problem

Language models achieve strong task performance, but:

- It is unclear whether internal representations encode structural linguistic meaning.
- Small counterfactual edits can radically alter meaning for humans.
- Output-level correctness alone does not reveal representational geometry.

Key question:

Do hidden-state shifts under minimal linguistic edits align with human semantic-change judgments?

---

# Why Counterfactual Minimal Edits?

Minimal edit protocols isolate structural changes while limiting lexical confounds.

Primary phenomena:

- Role reversal (agent/patient swap).
- Negation insertion/removal.
- Attachment disambiguation.

Examples:

- Role: “The driver ignored the passenger.” ↔ “The passenger ignored the driver.”
- Negation: “The writer interviewed the coach.” ↔ “The writer did not interview the coach.”
- Attachment: “With the microscope, ...” ↔ “... who had the microscope.”

---

# Scientific Claim Boundary (Strict)

Primary claim:

- Some layer-wise representation shifts may align with human semantic-change ratings.

Explicit non-claim:

- This project does not claim language models process language like humans.
- No reading-time or neuro data were collected; this is semantic-judgment alignment only.

(Ettinger, 2020; Lee et al., 2024 motivate this caution.)

---

# Final Project Title

Counterfactual Structural Sensitivity:
Human-Aligned Probing of Language Model Representations under Minimal Linguistic Edits

Target venue framing:

- IJCAI-ECAI 2026 workshop fit: logical/symbolic reasoning lens via controlled structural edits and interpretability.

---

# Formal Pipeline (Canonical)

\[
\text{sentence} \rightarrow \text{counterfactual edit} \rightarrow \text{hidden states} \rightarrow \text{representation shifts} \rightarrow \text{probes + surprisal} \rightarrow \text{human alignment}
\]

Repository non-negotiable:

- This pipeline was preserved throughout all phases.
- No pivot to unrelated objectives.

Source: `AGENTS.md`

---

# Hypotheses (H1-H5)

- **H1 Human-aligned shift**: Larger representation shifts correlate with larger human 0-5 change scores.
- **H2 Frobenius complementarity**: Matrix-norm shift adds explanatory value beyond centroid cosine.
- **H3 Phenomenon-specific layer profiles**: Role/negation/attachment peak differently by layer.
- **H4 Surprisal complementarity**: GPT-2 surprisal contributes but does not replace representation metrics.
- **H5 Control robustness**: Effects should survive controls (length, overlap, split controls, selectivity).

Source: `PROJECT_RESEARCH_PLAN.md`

---

# Novelty Statement

Not novel:

- Minimal pairs per se (BLiMP already established broad minimal-pair evaluation; Warstadt et al., 2020).

Novel combination here:

- Counterfactual minimal edits + layer-wise hidden shifts + matrix-norm adaptation + human change ratings + selectivity-controlled probes + surprisal covariates.

---

# Literature Signals Incorporated

- BLiMP minimal-pair evaluation (Warstadt et al., 2020).
- Role/negation psycholinguistic diagnostics (Ettinger, 2020).
- Argument-role sensitivity in modern LMs (Lee et al., 2024).
- Probe selectivity controls (Hewitt & Liang, 2019).
- Matrix-norm similarity motivation (vor der Brück & Pouly, 2019).
- Surprisal theory (Levy, 2008).
- Optional CKA/RSA context (Kornblith et al., 2019; Kriegeskorte et al., 2008).

---

# Model Choices (Primary)

Exactly three primary models:

- `bert-base-uncased` (Devlin et al., 2019)
- `roberta-base` (Liu et al., 2019)
- `gpt2` (Radford et al., 2019)

Rationale:

- Bidirectional encoder baseline (BERT family).
- Strong optimized BERT-family variant (RoBERTa).
- Autoregressive model for canonical surprisal (GPT-2).

---

# Phase Roadmap Implemented

Full lifecycle tracked in `docs/PHASES.md`:

- Phase 0: governance/tooling baseline.
- Phase 1-2: schemas/configs/data generation.
- Phase 3-8: pilot extraction through pilot stats.
- Phase 9-14: full scaling, annotation fallback, final stats, salience, packaging, audit.

Status:

- All phases completed with logs; Phase 14 marked conditionally complete pending real annotations.

---

# Repository Governance

Key constraints enforced (`AGENTS.md`):

- Config-driven reproducible scripts.
- Fixed primary models/phenomena/metrics.
- Schema discipline (`css_pair_v1`, `css_hidden_cache_v1`).
- Traceability with hashes, seeds, versions.
- Incremental serialized logs (JSONL) per phase.

---

# Engineering Stack

Modern stack used:

- Package/runtime: `uv` + `pyproject.toml` + `uv.lock`.
- Lint/format/type/test: `ruff`, `ty`, `pytest`, `pre-commit`.
- Model stack: `torch`, `transformers`, `tokenizers`.
- Stats stack: `scipy`, `statsmodels`, `scikit-learn`.

---

# Environment Snapshot

System snapshot (`SYSTEM_SPECS.md`):

- OS: Ubuntu 22.04.5
- CPU: AMD Ryzen 9 7950X3D
- GPU: NVIDIA GeForce RTX 5060 Ti (CUDA 13.0 driver stack)
- RAM: 30 GiB

Project runtime snapshot (`uv` env):

- Python 3.14.3
- torch 2.11.0+cu130
- transformers 5.6.2
- tokenizers 0.22.2
- numpy 2.4.4, pandas 3.0.2, scipy 1.17.1, sklearn 1.8.0, statsmodels 0.14.6

---

# Data Modules (Primary)

Generated files:

- `data/css_pairs/role_1500.jsonl`
- `data/css_pairs/neg_1500.jsonl`
- `data/css_pairs/attach_1500.jsonl`
- merged full set: `data/css_pairs/full_all_4500.jsonl`

Pilot files also generated (100/100/100 + merged pilot 300).

---

# Dataset Cardinalities

Per phenomenon:

- Role reversal: 1500
- Negation: 1500
- Attachment: 1500

Merged full:

- Total: 4500 pairs

Split distribution in merged full:

- Train: 3169
- Dev: 697
- Test: 634

---

# Deterministic Splitting Rule

Split assignment function (`split_data.py`):

- `u = sha256(id) % 10000 / 10000`
- if `u < 0.7`: train
- else if `u < 0.85`: dev
- else: test

Properties:

- Deterministic and reproducible by ID only.
- No random split drift across reruns.

---

# Lexicon Inputs

Lexicon sources:

- `nouns_animacy.csv`: 20 nouns
- `verbs_roles.csv`: 15 verb entries
- `pp_instruments_attributes.csv`: 8 PP templates

These feed templated generation scripts:

- `generate_role.py`
- `generate_negation.py`
- `generate_attachment.py`

---

# Role Dataset Generation Logic

Template:

- `The {agent} {verb_past} the {patient}.`
- Counterfactual swaps agent/patient.

Edit type:

- `swap_agent_patient`

Metadata fields include:

- agent/patient identities (s and s_cf), verb base/past, animacy class, lexical groups.

---

# Role Dataset Example

ID: `role_000001`

- `s`: The driver ignored the passenger.
- `s_cf`: The passenger ignored the driver.

Edited spans:

- `s`: agent=driver, patient=passenger
- `s_cf`: agent=passenger, patient=driver

---

# Negation Dataset Generation Logic

Affirmative template:

- `The {subj} {verb_past} the {obj}.`

Negative template:

- `The {subj} did not {verb_base} the {obj}.`

Balanced edit types:

- `insert_not`: 750
- `remove_not`: 750

---

# Negation Dataset Example

ID: `neg_000001`

- `s`: The writer interviewed the coach.
- `s_cf`: The writer did not interview the coach.

Edited spans include:

- predicate span
- negation cue span (`not`) on negated side

---

# Attachment Dataset Generation Logic

Forms:

- Ambiguous PP form.
- VP-disambiguated form.
- NP-disambiguated relative-clause form.

Edit types (balanced):

- `vp_to_np`: 500
- `ambiguous_to_vp`: 500
- `ambiguous_to_np`: 500

---

# Attachment Dataset Example

ID: `attach_000001`

- `s`: With the microscope, the passenger observed the scientist.
- `s_cf`: The passenger observed the scientist who had the microscope.

Edited spans:

- PP span
- NP head span

---

# JSONL Pair Schema (`css_pair_v1`)

Required top-level fields:

- `id, schema_version, phenomenon, s, s_cf, edit_type, source, template_id, split`
- `gold_label, edited_spans, surface_controls, human_change`

Additional fields used:

- `notes`
- `linguistic_metadata` (phenomenon-specific controls)

Source: `src/css/data/schema.py`, `build_pair.py`

---

# Gold Label Fields

`gold_label` keys:

- `role_direction_s`, `role_direction_cf`
- `negation_s`, `negation_cf`
- `attachment_s`, `attachment_cf`

Semantics:

- Exactly one phenomenon has active non-null labels per item; others remain `null`.

---

# Surface Control Fields

Computed automatically:

- `token_len_s`, `token_len_cf`
- `char_len_s`, `char_len_cf`
- `lexical_jaccard`
- `levenshtein_distance`

Purpose:

- Covariates for robustness checks and regression controls.

---

# Surface Control Summary (Observed)

Role (1500):

- lexical Jaccard: constant 0.333333
- token length: constant 5

Negation (1500):

- lexical Jaccard: constant 0.428571
- token lengths: 5-7 (mean 6)

Attachment (1500):

- lexical Jaccard: 0.30-0.625 (mean ~0.475)
- token lengths: 8 or 9 (mean ~8.67 on counterfactual side)

---

# Data Validation

Validation script:

- `python -m css.data.validate_schema --config configs/experiments/full.yaml`

Outcome (`results/data_validation/full_schema_validation.json`):

- total rows: 4500
- total issues: 0
- duplicate IDs: 0
- status: `ok`

---

# Dataset Hashes (Full Run)

From full schema validation:

- role_1500 SHA256: `5f2a31dc7097b798f12dab87f84972368ee684c7e747ca0f60ec647e5213d58b`
- neg_1500 SHA256: `4b2678fdb81e8c897e52e15e821030f07b133ef4681f9713d64d4559714142e2`
- attach_1500 SHA256: `5b34d13cbc620d71c6244c45be6248183172f5c28a58efe0b7294d756f44c08d`

Full config hash:

- `d8164e97ab119a8fe9dec5ac4d7bac564d9c30e65154fc2b8c592b417c172805`

---

# Representation Extraction: Inputs

Config:

- `configs/experiments/full.yaml`
- models: BERT, RoBERTa, GPT-2
- layers 0..12
- max length 128
- seed 13

Implementation:

- `src/css/representations/extract_hidden.py`

---

# Representation Extraction: Tokenization

Tokenizer settings:

- fast tokenizer (`use_fast=True`)
- `return_offsets_mapping=True`
- truncation enabled
- special tokens included

Word mapping:

- words computed via simple span splitter.
- each token mapped to word by token start offset containment.
- subword-to-word aggregation via mean.

---

# Representation Units Stored Per Layer

Per side (`s`, `s_cf`) and layer:

- `word_matrix` (float16, word-level contextual vectors)
- `mean` (float32 pooled sentence vector)
- `cls` (when available)
- `last` (GPT-2 last non-special token vector)

Stored in cache payload under `items[*].layers`.

---

# Caching Artifacts

Main cache path pattern:

- `cache/hidden/{model}/{dataset_stem}/hidden_cache.pkl`

Metadata path:

- `cache/hidden/{model}/{dataset_stem}/metadata.json`

Manifest:

- `results/manifests/extract_hidden_manifest.json`
- Full run entries: 9 (3 models × 3 datasets)

---

# Cache Metadata Fields

Metadata includes:

- `schema_version`: `css_hidden_cache_v1`
- `model_name`, `dataset_path`
- `dataset_sha256`, `config_sha256`
- `layers`, `pooling`, `dtype`, `seed`
- `python_version`, `torch_version`, `transformers_version`
- `device`, `cache_path`

This enforces run traceability.

---

# Extraction Hardware/Device Used

From full metadata files (`cache/hidden/*/*/metadata.json`):

- Device for all full caches: `cuda`
- Dtype policy: `float16_matrices_float32_pools`
- torch: `2.11.0+cu130`
- transformers: `5.6.2`

---

# Metric Definitions: Cosine Shift

Cosine similarity:

\[
\cos(\mathbf{a},\mathbf{b}) = \frac{\mathbf{a}\cdot\mathbf{b}}{\|\mathbf{a}\|\|\mathbf{b}\|+\epsilon}
\]

Shift:

\[
\Delta_{\cos} = 1 - \cos(\mathbf{a},\mathbf{b})
\]

Implementation: `src/css/metrics/cosine.py`

---

# Metric Definitions: Frobenius Similarity (Adapted)

Given word matrices \(A \in \mathbb{R}^{m \times d}\), \(B \in \mathbb{R}^{n \times d}\):

1. Optional row L2 normalization.
2. Similarity matrices:
   - \(S_{\times} = \max(0, AB^\top)\) if clipping on.
   - \(S_A = \max(0, AA^\top)\)
   - \(S_B = \max(0, BB^\top)\)
3. Frobenius similarity:

\[
\text{sim}_{\text{frob}} = \frac{\|S_{\times}\|_F}{\sqrt{\|S_A\|_F\|S_B\|_F+\epsilon}}
\]

\[
\Delta_{\text{frob}} = 1 - \text{sim}_{\text{frob}}
\]

Implementation: `src/css/metrics/matrix_norms.py`

---

# Metric Definitions: L2 and Token-Aligned Shift

Sentence-level L2 shift:

\[
\Delta_{L2} = \|\mu(s)-\mu(s')\|_2
\]

Token-aligned shift:

- align words by exact lexical match (fallback positional).
- average token-wise cosine shifts:

\[
\Delta_{\text{tok}} = \frac{1}{|M|}\sum_{(i,j)\in M}\left(1-\cos(h_i,h'_j)\right)
\]

Implementation: `src/css/metrics/token_shift.py`

---

# Metric Computation Engine

Module:

- `src/css/metrics/compute_all_metrics.py`

Per record writes:

- pair/model/phenomenon/layer identifiers
- all four shifts + `sim_frob`
- covariates (`length_delta`, lexical_jaccard, edit distance, split, template)

Output:

- `results/metrics/layer_metrics_full.csv`

---

# Full Metrics Run Output

File:

- `results/metrics/layer_metrics_full.csv`

Rows:

- 175,500 = 4500 pairs × 3 models × 13 layers

Per model rows:

- BERT: 58,500
- RoBERTa: 58,500
- GPT-2: 58,500

---

# Metric Sanity Checks

Warning file:

- `results/metrics/metric_warnings_full.json`

Outcome:

- `n_warnings = 0`
- No out-of-range Frobenius anomalies flagged.

This passed the boundedness sanity criterion.

---

# Mean Metric Magnitudes (Full)

Global means over 175,500 rows:

- `delta_cos`: 0.02434
- `delta_frob`: 0.02980
- `delta_l2`: 30.32968
- `delta_token_aligned`: 0.07075

Interpretation:

- Relative scales differ by metric family; cross-metric comparisons require standardization in regression.

---

# Layer Peaks by Model/Phenomenon (Delta Frob)

Highest mean `delta_frob` layer per model × phenomenon:

- BERT/attachment: L12 (0.0800)
- BERT/negation: L12 (0.1380)
- BERT/role: L0 (0.0490)
- RoBERTa/attachment: L0 (0.0542)
- RoBERTa/negation: L0 (0.0923)
- RoBERTa/role: L0 (0.0343)
- GPT-2/attachment: L7 (0.0291)
- GPT-2/negation: L9 (0.0211)
- GPT-2/role: L5 (0.0050)

---

# Surprisal Theory

Autoregressive surprisal (Levy, 2008):

\[
\text{surprisal}(w_i) = -\log P(w_i \mid w_{<i})
\]

Project choice:

- GPT-2 autoregressive scoring is primary.
- MLM pseudo-log-likelihood is secondary/optional (Salazar et al., 2020).

---

# GPT-2 Surprisal Implementation

Module:

- `src/css/surprisal/gpt2_surprisal.py`

Per pair outputs:

- total surprisal (`s`, `s_cf`)
- average surprisal (`s`, `s_cf`)
- delta total, delta average
- absolute delta average
- key-region surprisal totals/counts

---

# Surprisal Key-Region Extraction

Key spans:

- taken from `edited_spans` in each side.

Token-level selection:

- tokenizer offsets compared against edited char spans.
- overlap criterion determines key token inclusion.

Coverage files:

- pilot: `key_region_coverage_pilot.json`
- full: `key_region_coverage_full.json`

---

# Surprisal Full Output Summary

File:

- `results/surprisal/gpt2_surprisal_full.csv`

Rows:

- 4500 (all full pairs)

Coverage:

- full coverage rate: 1.0
- covered pairs: 4500/4500

---

# Surprisal by Phenomenon (Abs Delta Avg)

Mean absolute delta average surprisal:

- attachment: 0.2225
- role reversal: 0.2852
- negation: 1.4186

Interpretation:

- Negation edits induce substantially larger GPT-2 expectation shifts in this synthetic setup.

---

# Probe Design (Primary)

Module set:

- `build_probe_dataset.py`
- `train_linear_probe.py`
- `selectivity_controls.py`

Classifier:

- Logistic regression in a standardized pipeline.
- Full config uses solver `liblinear`, `max_iter=300`, `C=1.0`.
- Seeds: 11, 13, 17, 19, 23.

---

# Probe Targets by Phenomenon

Role probe:

- token-level vectors at edited spans
- class: agent (1) vs patient (0)

Negation probe:

- sentence mean vectors
- class from `gold_label.negation_s`/`negation_cf`

Attachment probe:

- sentence mean vectors
- class mapping: VP_attachment (1) vs NP_attachment (0)

---

# Selectivity Control

Random-label control:

- shuffles training labels with fixed seed.
- trains same model and evaluates against true test labels.

Selectivity definition:

\[
\text{selectivity} = \text{macro-F1}_{task} - \text{macro-F1}_{control}
\]

Reference motivation: Hewitt & Liang (2019)

---

# Probe Output Files (Full)

- `results/probes/probe_results_full.csv`
- `results/probes/probe_predictions_full.csv`
- `results/probes/selectivity_summary_full.csv`
- `results/probes/selectivity_summary_full.json`

Rows:

- probe results: 325
- probe prediction summary rows: 65

---

# Probe Coverage Matrix

Observed results by model/phenomenon:

- BERT: role + negation (65 each)
- RoBERTa: role + negation (65 each)
- GPT-2: negation only (65)

Skipped cells:

- 52 layer-cells skipped as `insufficient_data` (single-class).

---

# Probe Skips: Root Causes (Code-Level)

1. Attachment probes single-class:

- builder uses `gold.get(f"attachment_{side}")` with `side in {s, s_cf}`
- for `s_cf`, key becomes `attachment_s_cf` (nonexistent)
- only `attachment_s` seen; ambiguous labels dropped; VP-only subset survives.

2. GPT-2 role single-class:

- GPT-2 word-matrix/word-list misalignment affects span-index mapping and class balance.

---

# Probe Aggregate Scores (Full)

Averages over 325 rows:

- task macro-F1: 1.0000
- control macro-F1: 0.4918
- selectivity: 0.5082

Interpretation caveat:

- Perfect F1 with random row-level split on templated data likely reflects task easiness and/or leakage-like simplicity.
- Must be re-evaluated with stricter lexical/template splits and corrected label extraction.

---

# Human Annotation Design

Prompt and scale:

- `reports/appendix/annotation_prompt.md`
- 0-5 semantic-change rating
- extra fields: confidence, fluency, plausibility

Full target in plan:

- minimum 300 pairs balanced across phenomena with at least 3 annotators/item.

---

# Annotation Execution Status

Current full annotation files:

- `data/annotations/annotation_batch_full.csv` (300 pairs)
- `data/annotations/human_css_0_5_full.csv` (900 rows)
- `data/annotations/human_css_aggregated_full.csv` (300 rows)
- `results/annotation/agreement_report_full.json`

Critical status:

- These are simulated fallback annotations (pipeline completion aid), not real human collection.

---

# Annotation Agreement (Fallback Data)

From `agreement_report_full.json`:

- pairs: 300
- annotators: 3
- rows: 900
- mean pairwise Spearman: 0.6331
- median pairwise Spearman: 0.6330
- pct pairs with range >= 3: 0.0

Interpretation:

- This is synthetic agreement and cannot support publication-level behavioral claims.

---

# Statistical Pipeline Inputs

Full stats config (`configs/experiments/stats_full.yaml`) merges:

- metrics: `results/metrics/layer_metrics_full.csv`
- surprisal: `results/surprisal/gpt2_surprisal_full.csv`
- probe outputs: `results/probes/probe_results_full.csv`
- annotation (raw + aggregated) full fallback files

Outputs go to:

- `results/stats/full/`

---

# Correlation Analysis (Primary)

Per model × phenomenon × layer:

- Spearman (primary)
- Pearson (secondary)
- Bootstrap CIs (300 samples)
- BH-FDR correction on p-values

Metrics tested:

- `delta_cos`, `delta_frob`, `delta_l2`, `delta_token_aligned`

---

# Correlation Output Coverage

`results/stats/full/correlations.csv`:

- 468 rows
- 3 models × 3 phenomena × 13 layers × 4 metrics

FDR result summary:

- Spearman q<0.05 cells: 0

Mean Spearman by metric:

- delta_cos: -0.0076
- delta_frob: -0.0107
- delta_l2: -0.0145
- delta_token_aligned: -0.0338

---

# H2 Incremental Test (Frobenius Beyond Cosine)

Per cell OLS comparison:

- Base: \( z_y \sim z_{\cos} + z_{len} + z_{jacc} \)
- Extended: \( z_y \sim z_{\cos} + z_{frob} + z_{len} + z_{jacc} \)

Output:

- `results/stats/full/h2_incremental.csv`

Summary:

- rows: 117
- positive \(\Delta\)adj-\(R^2\): 40
- q<0.05 on Frobenius term: 0
- mean \(\Delta\)adj-\(R^2\): 0.00037

---

# Mixed-Effects Modeling

Implemented in:

- `src/css/stats/mixed_effects.py`

Per-layer formula:

\[
\text{human\_change} \sim z\_{{\Delta cos}} + z\_{{\Delta frob}} + z\_{{|\Delta surprisal|}} + z\_{{probe\_conf}} + C(\text{phenomenon}) + C(\text{model}) + z\_{len} + z\_{jacc}
\]

Random effects:

- random intercept by pair (`groups=pair_id`)
- annotator variance component (`vc_formula` on annotator ID)

---

# Mixed-Effects Output Summary

File:

- `results/stats/full/mixed_effects_summary.csv`

Rows:

- 13 (layers 0..12)

Convergence:

- All fits converged; boundary warnings observed during fitting.

Effect significance (p<0.05 counts across layers):

- z_delta_cos: 0
- z_delta_frob: 0
- z_abs_surprisal: 0
- z_probe_conf: 0
- z_len: 0
- z_jacc: 0

---

# Hypothesis Digest File

`results/stats/full/hypothesis_tests.md` reports:

- H1 positive-correlation cells (cos/frob): 123
- H2 positive \(\Delta\)adj-\(R^2\) cells: 40
- H3 peak-layer groups generated: 36
- H4 mean Spearman for delta_frob: -0.0107
- H5 note indicates controls partially covered

Important caveat:

- H5 line text still references pilot wording; treat as a formatting mismatch, not a data rerun failure.

---

# Salience Experiment Positioning

Status:

- Explicitly exploratory/secondary.

Goal:

- Rank tokens/spans that most contribute to representation shift.
- Compare rankings with edited gold spans.

Modules:

- `src/css/salience/token_contributions.py`
- `src/css/salience/evaluate_salience.py`

---

# Salience Scoring Components

Per token:

- cross-matrix contribution (row/column sum of \(AB^\top\))
- leave-one-out Frobenius drop

Combined score:

\[
\text{salience} = 0.5 \cdot \text{cross\_contrib} + 0.5 \cdot \text{loo\_drop}
\]

Normalized to probability-like per-side token scores.

---

# Salience Layer Selection

Operational choice:

- Use layer with highest mean `delta_frob` per model × phenomenon.

Source:

- derived from `results/metrics/layer_metrics_full.csv`

This keeps salience tied to phenomenon/model-specific sensitivity peaks.

---

# Salience Robustness Patch

Observed issue:

- GPT-2 had mismatched `len(words)` vs matrix rows due offset-word alignment behavior.

Patch behavior:

- truncate words/spans to matrix row count
- pad fallback token names when needed
- proceed with safe indexing

Result:

- salience full run completed without index failures.

---

# Salience Outputs

- `results/salience/token_contributions_full.csv` (135,000 rows)
- `results/salience/salience_eval_full.csv` (16 summary rows)

Overall summary (`scope=overall`):

- Recall@1: 0.0989
- Recall@3: 0.5696
- MRR: 0.3974
- AUC: 0.1883

---

# Figure and Table Generation

Modules:

- `src/css/plots/plot_layer_curves.py`
- `src/css/plots/plot_ablation_tables.py`

Generated artifacts:

- `results/figures/layer_correlation_curves.pdf`
- `results/figures/probe_selectivity_curves.pdf`
- `results/figures/surprisal_vs_human.pdf`
- `results/figures/top_layer_by_metric.csv`
- `results/figures/frob_incremental_positive.csv`
- `results/figures/frob_incremental_summary.csv`

Mirrored tables in `results/tables/`.

---

# Full Pipeline Scripts Added

Full-run orchestrators:

- `scripts/run_full_metrics.sh`
- `scripts/run_probes.sh`
- `scripts/run_stats.sh`
- `scripts/run_salience_and_plots.sh`

Pilot orchestrator retained:

- `scripts/run_pilot.sh`

All scripts use `uv run` for consistency.

---

# Incremental Logging System

Mandatory serialized logs:

- `logs/incremental/phase_XX.jsonl`

Appender:

- `scripts/log_event.py`

Events include:

- UTC timestamp, phase, event type, summary, artifacts, command, status, git commit.

---

# Logging Coverage

Observed phase logs:

- `phase_00` through `phase_14`
- every file has events
- corrective events appended instead of rewriting history

Examples:

- phase 09: extract + metrics + surprisal completion
- phase 11: full stats completion and correction
- phase 12/13: salience and plotting completion

---

# Quality Gates

Continuous checks used before commits:

- `uv run ruff check .`
- `uv run ruff format --check .`
- `uv run ty check`
- `uv run pytest`

Current test status:

- 8 tests passed (`test_schema`, `test_matrix_norms`, `test_surprisal`, `test_token_alignment`, smoke tests)

---

# Git Milestones

Key commits:

- `f2a1ce9` bootstrap uv-first stack
- `1e54a6a` phase 1 schema/config scaffolding
- `97111a1` full data generation
- `134fd34` phase 3-8 modules
- `693eb0b` start full extraction/metrics
- `3c4de4d` full tooling + salience + plotting
- `560aca3` full phases 9-14 artifacts
- `76ee726` env auto-load fix

---

# Full Artifact Matrix (High Level)

Data:

- validated pair datasets + merged full set

Representations:

- hidden caches for 3 models × 3 datasets

Metrics:

- full layer metrics (175,500 rows) + no numeric warnings

Surprisal:

- full GPT-2 surprisal (4,500 rows, 100% key coverage)

Probes:

- partial due single-class skips (325 rows generated)

Stats:

- correlations + H2 incremental + mixed effects

Salience:

- full contributions + evaluation

---

# Current Scientific Readout (As Implemented)

What is strong:

- Full engineering pipeline, reproducibility, and traceability are in place.
- Representation metrics and surprisal pipelines run fully on all required data/models.
- Statistics and salience modules are operational end-to-end.

What is currently not publication-strong:

- Human ratings are simulated fallback.
- Probe coverage has known label/key and alignment issues.
- No FDR-significant correlations with current fallback labels.

---

# Why Correlation Signals Are Weak Here

Primary reason:

- Annotation targets are synthetic fallback, not real human judgments.

Likely secondary contributors:

- Probe extraction bug (`*_s_cf` key mismatch).
- GPT-2 word alignment limitations for span-sensitive probing.
- templated data simplicity and random splits.

Conclusion:

- Do not interpret these numbers as final scientific findings.

---

# High-Impact Fixes Needed Before Paper Claims

1. Replace simulated annotations with real human collection (>=300 balanced).
2. Fix probe label keying for `negation_cf` and `attachment_cf`.
3. Harden GPT-2 word/span mapping in extraction for role probes.
4. Re-run probes under lexical/template split controls.
5. Recompute full stats and figures with corrected inputs.

---

# Probe Bug Detail: Key Naming

Current probe code pattern:

- `gold.get(f"negation_{side}")`
- `gold.get(f"attachment_{side}")`
- where `side` is `s` or `s_cf`

Expected gold keys:

- `negation_s`, `negation_cf`
- `attachment_s`, `attachment_cf`

Issue:

- `*_s_cf` does not exist; counterfactual side labels are dropped.

---

# Probe Bug Detail: Consequence

Attachment consequence:

- only `attachment_s` used
- many `s` labels are `ambiguous` and filtered out
- remaining class mostly VP -> single-class training (skip)

Negation consequence:

- only `negation_s` used
- still two classes because generator alternates insertion/removal in original side

---

# GPT-2 Span Alignment Issue

Observation:

- GPT-2 caches often had fewer word vectors than words.

Detected pattern:

- role/neg/attach GPT-2 layer matrices had row counts (e.g., 2-3) for sentences with 5-9 words.

Impact:

- role probe span indexing under-represents expected spans/classes.
- salience required truncation-safe handling.

---

# Mixed-Effects vs Planned Formula

Plan intended random intercepts for both item and annotator with rich model structure.

Implemented:

- random intercept by pair + annotator variance component.

This is acceptable operationally, but final paper should:

- report exact fitted structure,
- justify any deviations from pre-plan,
- and optionally replicate in R `lme4` for cross-check.

---

# Primary vs Exploratory (Status in This Repo)

Primary pipelines complete:

- data, representations, metrics, GPT-2 surprisal, core stats.

Exploratory completed:

- salience ranking and evaluation.

Primary claim blockers:

- real annotation data not yet plugged in.
- probe bugs/coverage not yet corrected.

---

# Reproducibility Checklist Status

Included:

- commit hash, config files, dataset hashes
- model IDs and seeds
- package/runtime versions
- cached hidden metadata
- script-generated outputs
- phase logs

Remaining for camera-ready scientific reproducibility:

- finalized real annotation protocol execution records and anonymized real ratings.

---

# Security / Secret Handling

Operational behavior:

- `.env` supported and auto-loaded through shared config module (`python-dotenv`).
- tokens are not hardcoded in scripts.

Recommendation:

- keep `.env` out of version control
- rotate and scope-access tokens used for data/model downloads

---

# Command Catalog (Pilot)

Pilot end-to-end (existing script):

```bash
bash scripts/run_pilot.sh
```

Main components inside:

- data generation + merge + validation
- extraction + metrics + surprisal + probes
- annotation fallback + aggregation + agreement
- pilot stats

---

# Command Catalog (Full)

Full run sequence:

```bash
bash scripts/run_full_metrics.sh
bash scripts/run_probes.sh
bash scripts/run_stats.sh
bash scripts/run_salience_and_plots.sh
```

These scripts generated current full artifacts in `results/`.

---

# File Map: Data Layer

Core modules:

- `src/css/data/schema.py`
- `src/css/data/build_pair.py`
- `src/css/data/generate_role.py`
- `src/css/data/generate_negation.py`
- `src/css/data/generate_attachment.py`
- `src/css/data/split_data.py`
- `src/css/data/validate_schema.py`

Outputs:

- `data/css_pairs/*.jsonl`
- `results/data_validation/*.json`

---

# File Map: Representation Layer

- `src/css/representations/extract_hidden.py`
- `src/css/representations/pooling.py`
- `src/css/representations/token_alignment.py`
- `src/css/representations/cache_io.py`

Outputs:

- `cache/hidden/...`
- `cache/tokenized/...`
- `results/manifests/extract_hidden_manifest.json`

---

# File Map: Metrics Layer

- `src/css/metrics/cosine.py`
- `src/css/metrics/matrix_norms.py`
- `src/css/metrics/token_shift.py`
- `src/css/metrics/compute_all_metrics.py`

Outputs:

- `results/metrics/layer_metrics*.csv`
- `results/metrics/metric_warnings*.json`

---

# File Map: Probe Layer

- `src/css/probes/build_probe_dataset.py`
- `src/css/probes/selectivity_controls.py`
- `src/css/probes/train_linear_probe.py`

Outputs:

- `results/probes/probe_results*.csv`
- `results/probes/probe_predictions*.csv`
- `results/probes/selectivity_summary*.{csv,json}`

---

# File Map: Surprisal Layer

- `src/css/surprisal/gpt2_surprisal.py`
- `src/css/surprisal/mlm_pll.py` (optional secondary)

Outputs:

- `results/surprisal/gpt2_surprisal*.csv`
- `results/surprisal/key_region_coverage*.json`

---

# File Map: Stats Layer

- `src/css/stats/correlations.py`
- `src/css/stats/bootstrap.py`
- `src/css/stats/multiple_comparisons.py`
- `src/css/stats/mixed_effects.py`
- `src/css/stats/mixed_effects.R` (placeholder)

Outputs:

- `results/stats/full/*`

---

# File Map: Salience + Plot Layer

Salience:

- `src/css/salience/token_contributions.py`
- `src/css/salience/evaluate_salience.py`

Plots/tables:

- `src/css/plots/plot_layer_curves.py`
- `src/css/plots/plot_ablation_tables.py`

Outputs:

- `results/salience/*`
- `results/figures/*`
- `results/tables/*`

---

# File Map: Reports and Logs

Reports:

- `reports/phases/phase_03.md` ... `phase_14.md`
- `reports/full/PHASE_PROGRESS_INDEX.md`
- `reports/workshop_paper/paper.md`
- `reports/appendix/*`

Logs:

- `logs/incremental/phase_00.jsonl` ... `phase_14.jsonl`

---

# Full Run Coverage Matrix (Implemented vs Planned)

| Component | Planned | Implemented status |
|---|---:|---|
| Pair data | 4500 | ✅ complete |
| Hidden caches | 3 models × 3 datasets | ✅ complete |
| Layer metrics | all pairs/layers/models | ✅ complete |
| GPT-2 surprisal | all pairs | ✅ complete |
| Probes | all target tasks/layers/models | ⚠️ partial (skips) |
| Human annotations | 300+ real | ⚠️ fallback simulated |
| Correlation + H2 stats | full | ✅ complete |
| Mixed effects | full | ✅ complete (with boundary warnings) |
| Salience | exploratory | ✅ complete |
| Figures/tables | script-generated | ✅ complete |

---

# Phase Completion Summary

From reports and logs:

- Phase 0-8: pilot complete.
- Phase 9: full extraction/metrics/surprisal complete.
- Phase 10: full annotation fallback complete.
- Phase 11: full stats + mixed effects complete.
- Phase 12: salience complete.
- Phase 13: paper/figure packaging complete.
- Phase 14: final audit complete (conditional flag).

---

# Conditional Completion Criterion

Phase 14 status:

- Engineering pipeline complete.
- Scientific claim readiness conditional.

Condition to clear:

- Replace fallback simulated annotations with real human annotations.
- Re-run corrected probe pipeline and downstream stats.

---

# Immediate Action Plan (Operational)

Step 1:

- collect real annotations on current `annotation_batch_full.csv` format.

Step 2:

- patch probe label key extraction:
  - explicit keys `negation_s`, `negation_cf`, `attachment_s`, `attachment_cf`.

Step 3:

- patch/validate GPT-2 span mapping in extraction.

Step 4:

- rerun full probes/stats/plots.

Step 5:

- freeze final claims and tables for manuscript.

---

# Suggested Additional Controls (Before Submission)

- Template split and lexical split probe runs (not only random split).
- Length-matched and overlap-matched subset analyses.
- Optional CKA/RSA as supplemental representational geometry check.
- Optional BERT/RoBERTa PLL as explicitly secondary analysis.

---

# Workshop Narrative Recommendation

Primary narrative:

- CSS is an evaluation protocol and engineering framework for controlled representational diagnostics.
- Emphasize reproducibility and transparent limitations.

Secondary narrative:

- Present current full run as infrastructure and preliminary signal map.
- Reserve stronger interpretation for post-real-annotation rerun.

---

# Reference Style Used in Deck

In-slide references:

- Bracket short form, e.g., [Devlin et al., 2019].

Bibliography:

- Full citation list at deck end.

All repository-specific claims cite exact artifact paths.

---

# References (Models)

- Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2019). BERT: Pre-training of deep bidirectional transformers for language understanding.
- Liu, Y., Ott, M., Goyal, N., et al. (2019). RoBERTa: A robustly optimized BERT pretraining approach.
- Radford, A., Wu, J., Child, R., et al. (2019). Language models are unsupervised multitask learners.

---

# References (Evaluation + Probing)

- Warstadt, A., Parrish, A., Liu, H., et al. (2020). BLiMP: A benchmark of linguistic minimal pairs for English.
- Hewitt, J., & Liang, P. (2019). Designing and interpreting probes with control tasks.
- Ettinger, A. (2020). What BERT is not: Lessons from a new suite of psycholinguistic diagnostics.
- Lee, et al. (2024). Argument-role sensitivity evaluation in language models.

---

# References (Similarity / Surprisal / Stats)

- vor der Brück, T., & Pouly, M. (2019). ACL paper on matrix norms for embedding-based similarity.
- Levy, R. (2008). Expectation-based syntactic comprehension.
- Salazar, J., Liang, D., Nguyen, T. Q., & Kirchhoff, K. (2020). Masked language model scoring.
- Kornblith, S., Norouzi, M., Lee, H., & Hinton, G. (2019). Similarity of neural network representations revisited.
- Kriegeskorte, N., Mur, M., & Bandettini, P. (2008). Representational similarity analysis.

---

# References (Datasets / Calibration Context)

- Abdalla, M., et al. (2023). STR-2022 relatedness shared task.
- GLUE / STS-B benchmark documentation and prior SemEval STS tasks.

Note:

- STS-B and STR are calibration context datasets in plan, not primary CSS human target.

---

# Repository Artifact References

Core documents:

- `AGENTS.md`
- `PROJECT_RESEARCH_PLAN.md`
- `docs/PHASES.md`
- `reports/phases/phase_09.md` ... `phase_14.md`
- `reports/workshop_paper/paper.md`

Core outputs:

- `results/metrics/layer_metrics_full.csv`
- `results/surprisal/gpt2_surprisal_full.csv`
- `results/probes/probe_results_full.csv`
- `results/stats/full/*`
- `results/salience/*`

---

# Appendix A: Key Config Files

- `configs/experiments/full.yaml`
- `configs/experiments/full_probes.yaml`
- `configs/experiments/surprisal_full.yaml`
- `configs/experiments/stats_full.yaml`
- `configs/experiments/salience_full.yaml`
- `configs/experiments/plots_full.yaml`
- `configs/experiments/annotation_full.yaml`

---

# Appendix B: Full Stats Output Files

- `results/stats/full/correlations.csv`
- `results/stats/full/bootstrap_cis.csv`
- `results/stats/full/h2_incremental.csv`
- `results/stats/full/mixed_effects_summary.csv`
- `results/stats/full/hypothesis_tests.md`

---

# Appendix C: Probe Output Fields (Selected)

From `probe_results_full.csv`:

- `phenomenon`, `probe_name`, `model`, `dataset_path`, `layer`, `seed`
- `accuracy`, `macro_f1`, `auroc`
- `control_accuracy`, `control_macro_f1`, `selectivity`
- `solver`, `max_iter`, `C`

---

# Appendix D: Surprisal Output Fields (Selected)

From `gpt2_surprisal_full.csv`:

- `total_surprisal_s`, `total_surprisal_cf`
- `avg_surprisal_s`, `avg_surprisal_cf`
- `delta_total_surprisal`, `delta_avg_surprisal`
- `abs_delta_avg_surprisal`
- `key_region_surprisal_s`, `key_region_surprisal_cf`
- `delta_key_region_surprisal`

---

# Appendix E: Metrics Output Fields (Selected)

From `layer_metrics_full.csv`:

- identifiers: `pair_id`, `phenomenon`, `model`, `dataset_path`, `layer`
- primary metrics: `delta_cos`, `sim_frob`, `delta_frob`, `delta_l2`, `delta_token_aligned`
- controls: `token_count_s`, `token_count_cf`, `length_delta`, `lexical_jaccard`, `edit_distance`
- split/template metadata: `split`, `template_id`

---

# Appendix F: Salience Output Fields (Selected)

From `token_contributions_full.csv`:

- `pair_id`, `phenomenon`, `model`, `layer`, `side`
- `token_index`, `token`
- `contrib_cross`, `contrib_loo_drop`, `salience_score`
- `is_gold`

From `salience_eval_full.csv`:

- `scope`, `n_pair_sides`, `recall_at_1`, `recall_at_3`, `mrr`, `auc`

---

# Appendix G: Export Instructions

If Marp CLI is available:

```bash
npx @marp-team/marp-cli reports/slides/CSS_Full_Project_Deep_Dive.md -o reports/slides/CSS_Full_Project_Deep_Dive.html
npx @marp-team/marp-cli reports/slides/CSS_Full_Project_Deep_Dive.md --pdf -o reports/slides/CSS_Full_Project_Deep_Dive.pdf
```

---

# Appendix H: Final Takeaway

Engineering objective achieved:

- End-to-end CSS pipeline exists and runs at full scale with full artifact traceability.

Scientific objective pending finalization:

- Real human annotations + probe fixes + rerun are required before final workshop claims.

This repository is now structured to make that final pass straightforward and auditable.

