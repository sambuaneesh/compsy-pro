# Counterfactual Structural Sensitivity: Human-Aligned Probing of Language Model Representations under Minimal Linguistic Edits

## Abstract

We present Counterfactual Structural Sensitivity (CSS), a controlled protocol for testing whether layer-wise hidden-state shifts under minimal structural edits align with human semantic-change judgments. CSS targets role reversal, negation, and attachment edits with paired sentences and evaluates representation shifts using cosine, Frobenius-style matrix norms, L2, and token-aligned metrics across BERT, RoBERTa, and GPT-2 layers. We combine these shifts with linear probes (including random-label selectivity controls) and GPT-2 surprisal features. The primary claim is human alignment of representational sensitivity, not equivalence to human language processing.

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

`sentence -> counterfactual edit -> hidden states -> representation shift -> probes + surprisal -> human alignment`

Phenomena:
- role reversal
- negation
- attachment ambiguity

Primary datasets:
- `role_1500.jsonl`
- `neg_1500.jsonl`
- `attach_1500.jsonl`

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

Human target:
- 0-5 semantic-change ratings.

## 6. Probes and Surprisal

Probes:
- linear probes by layer for role/negation/attachment.
- random-label controls with selectivity reporting.

Surprisal:
- GPT-2 autoregressive token surprisal.
- sentence-level and edited-region deltas.

## 7. Human Alignment and Statistics

Primary analyses:
- Spearman correlation between mean human change and per-layer CSS metrics.
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

- Human cognition claims are out of scope; results are framed as alignment with semantic judgments only.
- Attachment may remain noisier than role and negation.
- Synthetic annotation fallbacks are for pipeline validation and not final scientific claims.

## 10. Reproducibility

All runs are config-driven and traceable by dataset hash, config hash, model ID, seed, and package versions. Incremental JSONL logs track all meaningful execution blocks.

## References

References are maintained in `reports/appendix/references.md` and will be formatted for workshop submission.
