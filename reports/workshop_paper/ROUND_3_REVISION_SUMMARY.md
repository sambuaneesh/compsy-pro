# Workshop Paper Round 3 Revision Summary

Date: 2026-04-27

Round 3 was a final source-level review. The paper is now a complete first submission draft at the TeX/BibTeX/source level.

## Final Source-Level Status

- Citation keys are internally complete.
- Figure PDFs use embedded CID TrueType fonts, not Type 3 fonts.
- The paper states the role/negation asymmetry conservatively.
- Output-level results are framed as a forced-choice stress test.
- Dataset cardinality is stated as directed CSS rows derived from source pairs.
- Compile instructions include clean rebuild commands and PDF-font/log checks.
- After inspecting the user-compiled PDF, line numbers were disabled in the clean draft because they collided with two-column text.
- The bibliography is now embedded directly in the TeX source so the paper no longer depends on BibTeX; two `pdflatex` passes are sufficient.
- The source now includes additional coverage and reproducibility detail so the draft is less compressed.
- Author names, affiliation, and emails were restored for the non-anonymous/camera-ready style requested by the user.
- Prose references to figures and tables were changed to explicit numbers to avoid `??` figure/table references in partially compiled PDFs.
- Multi-panel result plots were changed to full-width floats to improve legibility and reduce crowding.

## Remaining Hard Blocker

The previously compiled PDF was stale and has been removed. Rebuild on a machine with a working LaTeX installation before submission.
