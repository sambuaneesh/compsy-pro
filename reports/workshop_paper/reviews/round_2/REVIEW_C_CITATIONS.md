# Round 2 Review C: Citations and Related Work

## Must Fix

- Dataset cardinality was risky: source papers describe 750 source pairs while CSS files contain 1,500 directed rows. The paper should say "1,500 directed CSS rows derived from 750 source pairs."
- The GitHub dataset citation used year 2026 even though the pinned commit is dated 2023-10-13.
- The existing compiled PDF is stale and unresolved; do not submit it.

## Should Fix

- Keep exact model-card citations for Mistral v0.3 and Gemma 3 4B IT.
- Add access notes for Hugging Face and GitHub references.
- Add arXiv DOI/eprint metadata where possible.

## Acceptance Risk

Medium if cardinality wording and stale PDF are fixed; otherwise reviewers may question data provenance.
