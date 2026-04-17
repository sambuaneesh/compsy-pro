# Future Work and Scope-Reentry Notes

Last updated: 2026-04-25

## Current Scope Snapshot

The final active run is locked to:
- role reversal
- negation

The attachment/PP-ambiguity module remains available in data and scripts but is excluded from the current final claim set.

## Why Attachment Was Excluded in Final Claims

- The final track was constrained to a strict external-source dataset scope for faster completion and cleaner reproducibility.
- Attachment is typically noisier and needs stronger controls for robust claims.

## Re-Enable Plan for Attachment (PP/Ambiguity) in a Future Iteration

1. Re-enable attachment in full configs:
   - `configs/experiments/full.yaml`
   - `configs/experiments/full_probes.yaml`
   - `configs/experiments/salience_full.yaml`
2. Rebuild merged dataset to include all three phenomena (`full_all_4500`).
3. Rerun full pipeline:
   - extraction
   - metrics
   - probes
   - surprisal
   - stats
4. Add stronger attachment-specific controls (template split and lexical-head split) before final interpretation.

## Human Evaluation: When It Is Required vs Optional

Human evaluation is **not automatically required** just to include attachment.

- If the goal is still dataset-only structural sensitivity diagnostics:
  - human annotation is optional.
  - claims stay at representation-level behavior.

- If the goal is human-alignment claims (for any or all phenomena, including attachment):
  - human annotation is required.
  - ratings should be collected on a balanced subset and integrated into final statistics.

## Recommended Two-Track Strategy

- Track A (fast): dataset-only three-phenomena run, no human-alignment claims.
- Track B (stronger paper claim): add human ratings and report human-alignment analyses.
