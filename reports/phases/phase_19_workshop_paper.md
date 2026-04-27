# Phase 19 Report: Workshop Paper Drafting and Review

Status: in progress

Purpose:
- Verify experiment artifacts after the Gemma extension.
- Generate paper-specific figures.
- Draft a regular-paper submission in IJCAI 2026 format for the LogiSymb workshop.
- Run three harsh review-and-revision cycles and archive critiques plus changes.

Completed so far:
- Checked current LogiSymb workshop page and IJCAI author kit.
- Downloaded IJCAI-ECAI 2026 formatting files into `reports/workshop_paper/format/`.
- Regenerated full salience and plot outputs.
- Verified expected row counts for data, metrics, surprisal, probes, consistency summaries, and metric warnings.
- Generated paper-local figures in `reports/workshop_paper/figures/`.
- Wrote `reports/workshop_paper/EXPERIMENT_AUDIT.md`.
- Wrote and committed the first anonymous IJCAI-format TeX draft.
- Completed round 1 reviewer pass with four personas.
- Added surface-control residual analyses, output Wilson CIs, and revised paper figures.
- Rewrote the draft around robust role-reversal results and weaker artifact-sensitive negation results.
- Expanded references and exact modern-model citations.
- Completed round 2 reviewer pass and fixes.
- Corrected source-dataset cardinality wording and dataset citation metadata.
- Regenerated figures with embedded TrueType fonts instead of Type 3 fonts.
- Completed round 3 final review pass and source-level fixes.
- Added final compile checklist and stale-PDF warning.
- Inspected the user-compiled PDF pages and fixed the visible problems: missing references, line-number overlap, and overly compressed method coverage.
- Embedded references directly in the TeX source and removed stale generated PDF/aux/log artifacts.
- Added final author names, IIIT Hyderabad affiliation, and email addresses.
- Replaced prose cross-references with explicit figure/table numbers and widened multi-panel plots.

Next:
- Rebuild the paper PDF on a machine with LaTeX installed.
- Inspect the rebuilt PDF visually and resolve any compile warnings.
