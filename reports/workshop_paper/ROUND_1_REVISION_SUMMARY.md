# Workshop Paper Round 1 Revision Summary

Date: 2026-04-27

## Main Reviewer Concerns Addressed

- The paper now defines the logical/structural object explicitly: role reversal is predicate-argument permutation `R(a,b) -> R(b,a)`, while negation is framed conservatively as a negated counterfactual because the source data mix polarity with predicate/category foils.
- The paper now foregrounds the role/negation asymmetry instead of selling pooled positive cells as the main result.
- Surface-control residual correlations are now included and reported.
- Frobenius is defined exactly: word matrices exclude special tokens, rows are L2-normalized, unequal lengths are handled with an `n x m` cross-similarity matrix, and negative similarities are clipped by `K(X)=max(X,0)`.
- Probe setup now includes labels, split, seeds, feature type, classifier, and random-label control.
- Output consistency now includes exact prompt, forced-choice likelihood scoring, and Wilson confidence intervals.
- Citations were expanded to include argument-role diagnostics, behavioral testing, HANS/NLI controls, RSA/CKA, exact modern model cards, and the public dataset snapshot.
- Paper figures were regenerated with unclipped titles and non-overlapping legends.

## New Analysis Tables

- `reports/workshop_paper/tables/surface_controlled_correlations.csv`
- `reports/workshop_paper/tables/surface_controlled_summary.csv`
- `reports/workshop_paper/tables/frob_surface_correlations.csv`
- `reports/workshop_paper/tables/frob_surface_correlation_summary.csv`
- `reports/workshop_paper/tables/output_consistency_wilson_ci.csv`
- `reports/workshop_paper/tables/reproducibility_snapshot.json`

## Key Revised Result

After residualizing lexical Jaccard, absolute length delta, and edit distance:

- Role reversal remains robust: Frobenius mean Spearman `0.241`, positive in `39/39` baseline cells.
- Negation is weak/mixed: Frobenius mean Spearman `-0.011`, positive in `15/39` baseline cells.

This changes the paper story from "both phenomena broadly positive" to:

> CSS strongly supports role-reversal structural sensitivity; negation exposes useful but artifact-sensitive consistency gaps in the current public dataset.

## Remaining Risks

- Null-pair controls such as random pairs, passive paraphrases, and synonym substitutions are still not implemented.
- Output consistency still uses one prompt template.
- The local machine cannot compile LaTeX because `pdflatex` is unavailable; the user-compiled PDF should be checked after BibTeX and reruns.
