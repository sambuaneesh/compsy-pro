# Round 3 Revision Changes

## Implemented

- Narrowed the abstract to role-reversal cosine/Frobenius/L2 shifts.
- Added explicit H2 for negated counterfactuals and stated its failure mode.
- Added caveat that directed rows derived from the same source pair are not clustered in inferential summaries.
- Removed the incorrect claim that the main table reports percentile intervals.
- Clarified Frobenius clipping rationale.
- Reworded Gemma Frobenius extension as mixed but positive on average.
- Qualified modern-decoder role claims as qualitative, not surface-controlled.
- Expanded compile checklist with stale-artifact cleanup, optional `latexmk`, and `bbl`/`blg` checks.

## Not Implemented

- Clean PDF compilation remains external because LaTeX is not installed on this machine.
- Null-pair, paraphrase, passive, and non-identical positive controls remain future work.
