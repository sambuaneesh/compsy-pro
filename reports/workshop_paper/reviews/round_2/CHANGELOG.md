# Round 2 Revision Changes

## Implemented

- Added explicit hypotheses and failure criteria in the introduction.
- Reworded dataset cardinality as 1,500 directed CSS rows derived from 750 source pairs per phenomenon.
- Changed dataset repository citation from 2026 to 2023 and added commit date/access metadata.
- Reframed output consistency as a preliminary forced-choice stress test.
- Added sign-aware FDR counts to the main surface-control table.
- Softened causal/semantic wording from "evidence of structural sensitivity" to "evidence consistent with structural sensitivity."
- Regenerated figures with Matplotlib `pdf.fonttype=42` and verified figures no longer use Type 3 fonts.
- Added figure/table references in prose and clarified GPT-2 output-baseline interpretation.

## Not Implemented

- Null-pair controls and non-identical positive output controls remain future work because they require new experiment design and compute beyond this revision pass.
