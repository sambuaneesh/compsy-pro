# Workshop Paper Round 2 Revision Summary

Date: 2026-04-27

Round 2 focused on remaining acceptance-blocking issues after the surface-control rewrite.

## Fixed

- Source cardinality now says `1,500 directed CSS rows derived from 750 source pairs`, avoiding conflict with the source paper.
- The repository dataset citation now uses the pinned 2023 commit date and an access note.
- The paper now includes explicit hypotheses and failure criteria for role reversal and output-level counterfactual stress testing.
- Output-level results are now called a stress test, not a complete behavioral consistency evaluation, because no non-identical positive controls are included.
- The main surface-control table now reports sign-aware FDR counts.
- Figures were regenerated with embedded CID TrueType fonts instead of Type 3 fonts.
- The TeX source references all main figures/tables in prose.

## Remaining Submission Hygiene

- `pdflatex` and `bibtex` are not installed on this machine, so the PDF in the folder is stale and should not be submitted.
- Compile on a LaTeX machine using BibTeX and at least two reruns.
- After compiling, inspect the log for unresolved citations, unresolved references, overfull boxes, and Type 3 fonts.
