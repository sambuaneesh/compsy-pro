# Full Run Phase Progress Index

Updated: `2026-04-24`

Dataset migration note (2026-04-24):
- Role + negation sources were switched to `extending_psycholinguistic_dataset`.
- Canonical JSONL files were regenerated via importer.
- Any full-model metrics/probes/stats produced before this migration should be treated as pre-migration and rerun for final reporting.

- Phase 09: `reports/phases/phase_09.md` (full extraction/metrics scale-up)
- Phase 10: `reports/phases/phase_10.md` (annotation fallback)
- Phase 11: `reports/phases/phase_11.md` (full stats + mixed effects)
- Phase 12: `reports/phases/phase_12.md` (secondary salience)
- Phase 13: `reports/phases/phase_13.md` (figures/tables/paper packaging)
- Phase 14: `reports/phases/phase_14.md` (final audit)
- Phase 15: `reports/phases/phase_15_dataset_source_migration.md` (role/negation source migration)

Core full artifacts:
- Metrics: `results/metrics/layer_metrics_full.csv`
- Surprisal: `results/surprisal/gpt2_surprisal_full.csv`
- Probes: `results/probes/probe_results_full.csv`
- Stats: `results/stats/full/`
- Salience: `results/salience/`
- Figures: `results/figures/`
