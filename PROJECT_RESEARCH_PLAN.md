# Counterfactual Structural Probing: Working Plan

Last updated: `2026-04-24` (Asia/Kolkata)

## 1) Consolidated Understanding

Core question:
- Do LLM internal representations change in a linguistically meaningful way under minimal counterfactual edits (role reversal, negation, attachment changes), and do those changes align with human semantic judgments?

Current high-level pipeline:
- `sentence -> counterfactual edit -> hidden states -> representation shift -> probes + surprisal -> human alignment`.

Target contributions:
- A Counterfactual Structural Sensitivity (CSS) protocol.
- Human-aligned evaluation (0-5 semantic change annotations).
- Layer-wise analysis linking structure, surprisal, and recoverable linguistic info.

## 2) What Changed From Email Guidance

From Raja:
- Add **Frobenius norm / matrix-norm based comparison** in addition to cosine.
- Use N19-1181 as methodological grounding for matrix-norm similarity.

Interpretation for this project:
- Representation shift should not rely on cosine alone.
- Add matrix-level similarity between token embedding sets (per layer), then convert to shift.

## 3) Paper Readout (Relevant to Your Study)

### 3.1 N19-1181 (Matrix Norms)

Useful import:
- Build a pairwise similarity matrix between elements from text A and text B.
- Use norms (Frobenius/L1,1/2-norm) as robust alternatives to centroid cosine.
- Matrix norm can emphasize strong matches and reduce noise from many weak matches.

Actionable adaptation for your setup:
- At each layer `l`, represent sentence `s` as token matrix `H_l(s) in R^{T x d}`.
- Build cross-sentence similarity matrix `S_l = norm_tokens(H_l(s)) @ norm_tokens(H_l(s'))^T`.
- Normalize and compute matrix-norm similarity:
`sim_frob_l(s,s') = ||K(S_l)||_F / sqrt(||K(S_l_ss)||_F * ||K(S_l_s's')||_F)`,
where `K` zeroes negative entries, as in N19.
- Define shift:
`Delta_frob_l = 1 - sim_frob_l`.

### 3.2 Special Collection (Psycholinguistics + LMs)

Practical implications for experiment design:
- Bigger models are not always better for some human online measures (notably reading-time fitting).
- Surprisal alone is incomplete; memory/interference style signals can add explanatory power.
- Reader/task/domain alignment affects cognitive fit; generic scaling can hurt interpretability.
- For your paper, model comparison should include interpretability/human-alignment, not only raw LM quality.

## 4) Implementation Blueprint (Concrete)

### 4.1 Data Modules

`data/`
- `role_1500.jsonl`
- `neg_1500.jsonl`
- `attach_1500.jsonl` (from BLiMP-style attachment-focused subsets + curated pairs)
- `human_role_0_5.csv` (200-500 annotated pairs)
- `sts_alignment/` (STR-2022 + STS-B slices for semantic calibration)

Each pair record:
- `id, phenomenon, s, s_cf, edit_type, gold_label(optional), human_change(optional)`.

### 4.2 Representation Extraction

`src/extract_hidden.py`
- Models: `bert-base-uncased`, `roberta-base`, `gpt2`.
- Save token-level hidden states for all layers.
- Save pooled variants:
- `cls` (when available),
- mean-pool over non-special tokens,
- token-matrix (for matrix norm metrics).

### 4.3 Shift Metrics

`src/metrics.py`
- Cosine shift: `Delta_cos_l = 1 - cos(pool_l(s), pool_l(s_cf))`.
- Frobenius/matrix shift: `Delta_frob_l` (N19-style adaptation above).
- Optional robustness metrics:
- `Delta_l2_l = ||pool_l(s)-pool_l(s_cf)||_2`,
- `Delta_token_mean_l` (mean token-wise cosine drop after alignment).

### 4.4 Probing

`src/probes.py`
- Linear probes per layer:
- role labels (agent/patient direction),
- negation presence,
- attachment class.
- Report:
- accuracy, macro-F1, calibration (ECE optional),
- phenomenon-wise and model-wise breakdown.

### 4.5 Surprisal

`src/surprisal.py`
- Token surprisal with autoregressive scoring.
- Comparable sentence-level features:
- total surprisal,
- average surprisal,
- surprisal difference (`s_cf - s`),
- key-region surprisal (edited span only).

### 4.6 Human Alignment & Statistics

`src/analyze_alignment.py`
- Correlate per-pair shifts with human 0-5 judgments (Spearman primary, Pearson secondary).
- Layer-wise mixed effects:
- DV: human score,
- predictors: `Delta_cos_l`, `Delta_frob_l`, surprisal features, probe confidence,
- random intercept by item.
- Bootstrap CIs for all core correlations.

### 4.7 Outputs

`results/`
- layer curves (`Delta` vs layer, per phenomenon/model),
- correlation heatmaps,
- probe performance curves,
- ablation tables (cosine-only vs cosine+frob vs +surprisal).

## 5) Recommended Experiment Matrix (v1)

Models:
- BERT-base, RoBERTa-base, GPT-2.

Phenomena:
- Role reversal, Negation, Attachment.

Primary metrics:
- `Delta_cos`, `Delta_frob`, probe F1, surprisal deltas.

Main tests:
- H1: `corr(Delta, human_change) > 0`.
- H2: `Delta_frob` adds explanatory power over `Delta_cos`.
- H3: middle vs higher layers have different sensitivity profiles by phenomenon.

Ablations:
- pooling method,
- token normalization on/off,
- K(negative->0) on/off for matrix norms,
- sentence length control.

## 6) Long-Lead Downloads / Setup (Important)

Current environment status:
- Python is `3.8.5`.
- `transformers`, `datasets`, `huggingface-cli` are not installed.

This is the first bottleneck. Use a modern env (`3.10+`, preferably `3.11`) before experiments.

### 6.1 Model Weights (minimum required files)

- `google-bert/bert-base-uncased`: ~`441 MB`
- `FacebookAI/roberta-base`: ~`502 MB`
- `openai-community/gpt2`: ~`551 MB`

Total minimum model payload: ~`1.49 GB` (+ cache/index overhead).

### 6.2 Datasets (HF mirrors)

- `vkpriya/str-2022`: ~`1.0 MB`
- `nyu-mll/blimp`: ~`4.0 MB`
- `nyu-mll/glue` (includes STS-B among others): ~`162 MB`

Total dataset payload from these three: ~`167 MB`.

### 6.3 Likely Time-Consuming Tasks

- Installing PyTorch + Transformers stack.
- Downloading model weights (~1.5GB baseline; more if you add larger checkpoints).
- If you later scale to larger models (e.g., `roberta-large`, `gpt2-xl`), download and runtime costs grow sharply.

## 7) Suggested Immediate Execution Order

1. Create isolated Python 3.11 env and install core stack.
2. Start model/data prefetch in background.
3. Implement data schema + pair loaders.
4. Implement hidden-state extraction and cache format.
5. Add cosine + Frobenius shift metrics.
6. Add probes.
7. Add surprisal scoring.
8. Run pilot on 100 pairs/phenomenon.
9. Freeze config, then full run.

## 8) Notes / Open Assumptions

- `STR-2022` is interpreted as the Semantic Textual Relatedness dataset (5500 pairs).
- Attachment subset selection from BLiMP needs explicit phenomenon list before full run.
- Metrics names `CSC/MESC/SRIT` should be fixed in writing with precise equations before experiments to avoid post-hoc renaming.
