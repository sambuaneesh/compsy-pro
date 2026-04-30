# Round 1 Review A: Methods and Statistics

## Must Fix

- Add surface-control analyses. The original draft correlated CSS shifts with GPT-2 surprisal without modeling lexical Jaccard, length delta, or edit distance, even though the qualitative audit shows role and negation differ strongly in these controls.
- Do not present pooled significant-cell counts as the primary evidence. The 78 cells reuse the same items across layers and models, so they are not independent evidence units.
- Make the asymmetry explicit: role reversal is strong and stable, while negation is weak or mixed in several baseline cells.
- Define the Frobenius metric exactly. The draft used an opaque `K(.)` function without specifying clipping, normalization, special-token exclusion, or unequal-length handling.
- Reframe Frobenius as a small in-sample incremental association unless cross-validated or permutation-backed evidence is added.

## Should Fix

- Add or discuss null/surface baselines such as identical pairs, random pairs, lexical substitutions, and same-template non-counterfactuals.
- Report confidence intervals, not only p-values.
- Make clear that modern-decoder hidden-state correlations use GPT-2 surprisal as a fixed external covariate.
- Expand probe details: labels, split, features, regularization, seeds, random-label control.

## Acceptance Risk

High before revision. The core idea is useful, but reviewers can reject if dataset artifacts and repeated tests carry too much of the evidential burden.
