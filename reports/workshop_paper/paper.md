# Counterfactual Structural Sensitivity: Dataset-Only Probing of Language Model Representations under Minimal Linguistic Edits

## Abstract

We present Counterfactual Structural Sensitivity (CSS), a controlled protocol for testing whether layer-wise hidden-state shifts under minimal structural edits are systematic and model-consistent under a strict dataset-only setup. CSS targets role reversal and negation edits with paired sentences and evaluates representation shifts using cosine, Frobenius-style matrix norms, L2, and token-aligned metrics across BERT, RoBERTa, GPT-2, and modern instruction-decoder extensions. We combine these shifts with linear probes, GPT-2 surprisal features, qualitative audits, and an output-level counterfactual consistency experiment. The primary claim is structural sensitivity and metric behavior under controlled edits, not human-like processing.

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
- regular-paper extensions: `mistralai/Mistral-7B-Instruct-v0.3`, `google/gemma-3-4b-it`

Layers:
- baseline models: embedding plus transformer layers `1..12` (indexed `0..12` in code).
- Mistral extension: embedding plus decoder layers, indexed `0..32`.
- Gemma extension: embedding plus decoder layers, indexed `0..34`.

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

## 8. Results and Research-Question Answers

### RQ1: Do shift metrics respond consistently across layers/models?

Yes, with clear metric dependence.

- Positive significant cells (FDR<0.05):
  - `delta_cos`: `50/78`
  - `delta_frob`: `52/78`
  - `delta_l2`: `47/78`
  - `delta_token_aligned`: `32/78`
- Role reversal shows stronger and broader positive alignment than negation for most metrics.
- Frobenius peak layers:
  - Negation peaks at layer `0` for all three models.
  - Role reversal peaks in middle-to-late layers (`7` for BERT/RoBERTa, `10` for GPT-2).

Interpretation:
- Cosine/Frobenius/L2 are robust structural-sensitivity diagnostics in this setup.
- Token-aligned shift is informative but less stable across all cells.

### RQ2: Does Frobenius add value beyond cosine?

Yes, in most cells.

- Positive `delta_adj_r2` when adding Frobenius: `70/78` cells.
- Mean incremental gain: `0.0114` adjusted-`R^2`.
- FDR-significant Frobenius coefficient cells: `54/78`.

Interpretation:
- Matrix-geometry information contributes predictive signal beyond centroid-only shifts.
- Complementarity is strongest for role-reversal conditions.

### RQ3: How do probes and surprisal interact with shift diagnostics?

Probe selectivity is consistently positive, but coupling to metric-surprisal correlation strength is weak.

- Mean selectivity: `0.5096` (macro-F1 gap vs random-label control).
- Selectivity vs metric-correlation coupling:
  - `delta_frob`: Spearman `-0.0112`, Pearson `0.0126` (near zero).

Interpretation:
- Probes and metric-surprisal alignment provide complementary diagnostics.
- Neither signal is a direct substitute for the other.

### RQ4: Do modern decoder outputs preserve consistency under the same counterfactual edits?

Partially. We added a forced-choice output-level diagnostic:
- identical sentence control: expected `yes`
- counterfactual role/negation pair: expected `no`

Modern decoder results:
- Mistral identity controls: `1.0000` accuracy for both role reversal and negation
- Mistral counterfactual rejection: `0.7340` for role reversal and `0.6520` for negation
- Gemma identity controls: `0.9993` for role reversal and `1.0000` for negation
- Gemma counterfactual rejection: `0.9687` for role reversal and `0.8140` for negation

Interpretation:
- The identity-control results verify that the prompt is usable for instruction models.
- Mistral is far from ceiling on counterfactual rejection, while Gemma is substantially stronger but still imperfect on negation.
- GPT-2 is retained only as a biased baseline for this behavioral task because its identity controls are poor.

### RQ5: Does the modern decoder show CSS-style hidden-state sensitivity?

Yes. Mistral hidden-state metrics were computed for all 3000 pairs across 33 layers, producing `99000` layer-level rows and `0` Frobenius warnings.

Mistral mean shifts:
- negation: `delta_cos=0.0943`, `delta_frob=0.1255`, `delta_l2=5.7434`, `delta_token_aligned=0.0722`
- role reversal: `delta_cos=0.0399`, `delta_frob=0.0675`, `delta_l2=3.4933`, `delta_token_aligned=0.1124`

Strongest Mistral Frobenius-surprisal alignment:
- negation: layer `0`, Spearman rho `0.1750`, FDR q `2.31e-11`
- role reversal: layer `6`, Spearman rho `0.3244`, FDR q `1.15e-35`

Gemma hidden-state metrics were also computed for all 3000 pairs across 35 layers, producing `105000` layer-level rows and `0` Frobenius warnings.

Gemma mean shifts:
- negation: `delta_cos=0.0058`, `delta_frob=0.0071`, `delta_l2=1555.0256`, `delta_token_aligned=0.0024`
- role reversal: `delta_cos=0.0014`, `delta_frob=0.0021`, `delta_l2=894.1732`, `delta_token_aligned=0.0039`

Strongest Gemma Frobenius-surprisal alignment:
- negation: layer `0`, Spearman rho `0.0851`, FDR q `0.0015`
- role reversal: layer `6`, Spearman rho `0.3190`, FDR q `2.25e-34`

Frobenius complementarity remains visible in the modern decoders: adding Frobenius beyond cosine improves adjusted `R^2` in `59/66` Mistral cells and `48/70` Gemma cells.

## 9. Qualitative Analysis

To make the aggregate findings interpretable, we add a dataset-only qualitative audit over actual counterfactual pairs. For each pair, metric values are averaged across all three models and all 13 layers, then ranked within phenomenon by mean Frobenius shift and absolute GPT-2 average-surprisal delta. We inspect four buckets per phenomenon: high shift/high surprisal, high shift/low surprisal, low shift/high surprisal, and low shift/low surprisal.

The qualitative audit explains the apparent tension between mean-shift and correlation plots. Negation has larger pooled mean shifts, but this does not imply stronger rank alignment with surprisal. Many negation examples in the source dataset combine a negation cue with a predicate or category foil, so they introduce both polarity and lexical/category changes. Role reversal examples often preserve much higher lexical overlap and near-zero length change, which can yield smaller average geometric displacement but cleaner item-level ordering against surprisal.

Surface diagnostics support this reading:
- Negation: mean lexical Jaccard `0.4853`, mean absolute length delta `1.0013`, mean Frobenius shift `0.0584`.
- Role reversal: mean lexical Jaccard `0.7973`, mean absolute length delta `0.0467`, mean Frobenius shift `0.0197`.

Representative dissociations:
- High Frobenius / low surprisal negation: `A hammer is an instrument.` -> `A hammer is not a dessert.`
- Low Frobenius / high surprisal role reversal: `The cashier counted which bills the robber had given.` -> `The cashier counted which robber the bills had given.`

These examples show why CSS should be interpreted as a multi-diagnostic framework: representation geometry and surprisal are complementary, not interchangeable. The audit also surfaces generated-data artifacts such as article mismatches, lexical substitutions, and implausible continuations. This reinforces the conservative claim boundary: the current project supports dataset-level representational diagnostics, not human-comprehension claims.

## 10. Secondary Salience Experiment

Exploratory salience ranks edited spans using:
- Frobenius cross-matrix contribution
- leave-one-out Frobenius drop
- combined token salience score

Evaluation:
- Recall@1
- Recall@3
- MRR
- AUC (when label density permits)

## 11. Limitations

- This project does not include human annotation.
- Claims are restricted to dataset-only structural sensitivity diagnostics.
- Findings should not be interpreted as evidence of human-like language processing.
- The qualitative audit shows that generated source data contains occasional fluency and plausibility artifacts, so item-level examples must be interpreted as diagnostic cases rather than naturalistic comprehension materials.
- `meta-llama/Llama-3.1-8B` requires gated access; the available token did not permit access to this model.
- `Qwen/Qwen3-8B` is configured but close to the 16GB GPU memory boundary in fp16; Mistral-7B-Instruct-v0.3 and Gemma-3-4B-IT are the completed modern decoder results.

## 12. Reproducibility

All runs are config-driven and traceable by dataset hash, config hash, model ID, seed, and package versions. Incremental JSONL logs track all meaningful execution blocks.

## References

References are maintained in `reports/appendix/references.md` and will be formatted for workshop submission.
