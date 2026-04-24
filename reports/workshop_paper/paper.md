# Counterfactual Structural Sensitivity: Dataset-Only Probing of Language Model Representations under Minimal Linguistic Edits

## Abstract

We present Counterfactual Structural Sensitivity (CSS), a controlled protocol for testing whether layer-wise hidden-state shifts under minimal structural edits are systematic and model-consistent under a strict dataset-only setup. CSS targets role reversal and negation edits with paired sentences and evaluates representation shifts using cosine, Frobenius-style matrix norms, L2, and token-aligned metrics across BERT, RoBERTa, and GPT-2 layers. We combine these shifts with linear probes (including random-label selectivity controls) and GPT-2 surprisal features. The primary claim is structural sensitivity and metric behavior under controlled edits.

## 1. Introduction

Language models succeed on many benchmarks, but it is still unclear whether internal representations systematically encode structural meaning changes under minimal edits. Prior work often focuses on output behavior; CSS focuses on hidden-state response under controlled counterfactual transformations.

## 2. Related Work

- Minimal-pair linguistic evaluation (BLiMP; Warstadt et al., 2020).
- Representation probing and selectivity controls (Hewitt and Liang, 2019).
- Psycholinguistic diagnostics for role and negation sensitivity (Ettinger, 2020; Lee et al., 2024).
- Matrix-norm similarity (vor der Brück and Pouly, 2019).
- Surprisal in psycholinguistics (Levy, 2008).

## 3. CSS Protocol

Pipeline:

`sentence -> counterfactual edit -> hidden states -> representation shift -> probes + surprisal -> dataset-level analysis`

Phenomena:
- role reversal
- negation

Primary datasets:
- `role_1500.jsonl`
- `neg_1500.jsonl`

Current source split:
- role + negation imported from `text-machine-lab/extending_psycholinguistic_dataset`

## 4. Models and Representations

Models:
- `bert-base-uncased`
- `roberta-base`
- `gpt2`

Layers:
- embedding plus transformer layers `1..12` (indexed `0..12` in code).

Representations:
- mean-pooled sentence vectors (primary)
- word-level contextual token matrices (primary)
- CLS / last-token ablations (secondary)

## 5. Metrics

Primary per-layer metrics:
- `delta_cos`
- `sim_frob`, `delta_frob`
- `delta_l2`
- `delta_token_aligned`

Primary target:
- structural shift behavior under controlled edits.

## 6. Probes and Surprisal

Probes:
- linear probes by layer for role/negation.
- random-label controls with selectivity reporting.

Surprisal:
- GPT-2 autoregressive token surprisal.
- sentence-level and edited-region deltas.

## 7. Dataset-Only Statistics

Primary analyses:
- Spearman correlation between per-layer CSS metrics and surprisal deltas.
- Pearson as secondary.
- bootstrap confidence intervals.
- BH-FDR correction across layer-wise tests.
- incremental value test for `delta_frob` beyond `delta_cos`.

## 8. Secondary Salience Experiment

Exploratory salience ranks edited spans using:
- Frobenius cross-matrix contribution
- leave-one-out Frobenius drop
- combined token salience score

Evaluation:
- Recall@1
- Recall@3
- MRR
- AUC (when label density permits)

## 9. Limitations

- This project does not include human annotation.
- Claims are restricted to dataset-only structural sensitivity diagnostics.
- Findings should not be interpreted as evidence of human-like language processing.

## 10. Reproducibility

All runs are config-driven and traceable by dataset hash, config hash, model ID, seed, and package versions. Incremental JSONL logs track all meaningful execution blocks.

## References

References are maintained in `reports/appendix/references.md` and will be formatted for workshop submission.
