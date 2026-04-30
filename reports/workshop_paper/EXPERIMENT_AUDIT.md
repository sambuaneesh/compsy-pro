# Experiment Audit for LogiSymb Regular-Paper Draft

Date: 2026-04-26

## Submission Target

- Venue: IJCAI-ECAI 2026 Workshop on Logical and Symbolic Reasoning of Large Language Models.
- Workshop date/location: August 15, 2026, Bremen, Germany.
- Submission deadline: May 31, 2026 AoE.
- Regular-paper length: 4--10 pages, excluding references and supplementary material.
- Required format: IJCAI 2026 format.
- Review: double-blind through OpenReview.
- Relevance: the workshop explicitly lists logical consistency, including negation consistency and implication consistency, as topics of interest.

Sources checked:
- Workshop site: https://sites.google.com/view/ijcai-2026-logisymb
- IJCAI accepted-workshops listing: https://2026.ijcai.org/accepted-workshops/
- IJCAI author kit: https://www.ijcai.org/authors_kit

## Artifact Completeness

| Artifact | Expected | Observed | Status |
| --- | ---: | ---: | --- |
| Role-reversal pairs | 1500 | 1500 | pass |
| Negation pairs | 1500 | 1500 | pass |
| Merged dataset | 3000 | 3000 | pass |
| Baseline metric rows | 3000 pairs x 3 models x 13 layers = 117000 | 117000 | pass |
| Mistral metric rows | 3000 pairs x 33 layers = 99000 | 99000 | pass |
| Gemma metric rows | 3000 pairs x 35 layers = 105000 | 105000 | pass |
| GPT-2 surprisal rows | 3000 | 3000 | pass |
| Probe result rows | 390 | 390 | pass |
| Output-consistency summary rows | 12 | 12 | pass |

## Metric-Warning Audit

| Run | Warning count | Status |
| --- | ---: | --- |
| Baseline BERT/RoBERTa/GPT-2 metrics | 0 | pass |
| Mistral metrics | 0 | pass |
| Gemma metrics | 0 | pass |

## Core Results for Paper

Baseline representation diagnostics:
- Significant positive metric-surprisal cells for cosine/Frobenius: 102.
- Frobenius incremental value over cosine: positive adjusted-R2 gain in 70/78 baseline cells.
- Mean Frobenius incremental gain: 0.0114 adjusted R2.
- Mean probe selectivity: 0.5096.

Surface-controlled revision:
- After rank-residualizing lexical Jaccard, absolute length delta, and edit distance, role reversal remains robust.
- Role-reversal Frobenius mean Spearman after controls: 0.2410, positive in 39/39 baseline cells.
- Negation Frobenius mean Spearman after controls: -0.0107, positive in 15/39 baseline cells.
- The paper's primary representation claim should emphasize role reversal and describe negation as artifact-sensitive.

Modern decoder output consistency:
- GPT-2 has poor identity-control accuracy and is treated as a biased behavioral baseline.
- Mistral identity-control accuracy: 1.0000 for role and negation.
- Mistral counterfactual rejection: 0.7340 role, 0.6520 negation.
- Gemma identity-control accuracy: 0.9993 role, 1.0000 negation.
- Gemma counterfactual rejection: 0.9687 role, 0.8140 negation.

Modern decoder hidden-state CSS:
- Mistral Frobenius incremental value: positive in 59/66 cells.
- Gemma Frobenius incremental value: positive in 48/70 cells.
- Strongest Mistral role Frobenius-surprisal alignment: layer 6, Spearman rho 0.3244, q=1.15e-35.
- Strongest Gemma role Frobenius-surprisal alignment: layer 6, Spearman rho 0.3190, q=2.25e-34.

## Figure Set Generated for Draft

Paper-local figures:
- `reports/workshop_paper/figures/output_consistency_accuracy.pdf`
- `reports/workshop_paper/figures/modern_decoder_frob_curves.pdf`
- `reports/workshop_paper/figures/frob_incremental_comparison.pdf`
- `reports/workshop_paper/figures/baseline_frob_layer_heatmap.pdf`

Baseline full figures regenerated:
- `results/figures/dataset_counts.pdf`
- `results/figures/metric_means_by_phenomenon.pdf`
- `results/figures/layer_correlation_curves.pdf`
- `results/figures/frob_layer_heatmap.pdf`
- `results/figures/rq1_significance_profile.pdf`
- `results/figures/rq2_positive_rate_heatmap.pdf`
- `results/figures/rq3_interaction_bars.pdf`
- `results/figures/surprisal_vs_shift.pdf`

## Claim Boundaries

- No primary human-annotation claims are made.
- The paper must not claim that LMs process language like humans.
- The paper may claim that CSS detects systematic representation shifts under controlled structural edits and that these shifts partially align with model surprisal and output-level consistency.
- Attachment/PP ambiguity is future work, not part of current claims.
- Dataset artifacts are explicitly acknowledged: article mismatches, category-foil substitutions, and some implausible role-reversal continuations.

## Notes for Drafting

- Frame role reversal as event-structure / argument-role consistency.
- Frame negation as polarity / negation-consistency sensitivity.
- Present Frobenius as complementary, not as uniformly superior.
- Keep Mistral and Gemma as regular-paper extension models, while BERT/RoBERTa/GPT-2 remain the controlled primary CSS baseline.
