# Full Run Phase Progress Index

Updated: `2026-04-26`

Dataset migration note (2026-04-24):
- Role + negation sources were switched to `extending_psycholinguistic_dataset`.
- Canonical JSONL files were regenerated via importer.
- Post-migration full rerun completed (2026-04-24): extraction, metrics, surprisal, probes, stats, salience, and plots were regenerated.

- Phase 09: `reports/phases/phase_09.md` (full extraction/metrics scale-up)
- Phase 10: `reports/phases/phase_10.md` (legacy, not part of dataset-only gate)
- Phase 11: `reports/phases/phase_11.md` (legacy human-annotation stats track)
- Phase 12: `reports/phases/phase_12.md` (secondary salience)
- Phase 13: `reports/phases/phase_13.md` (figures/tables/paper packaging)
- Phase 14: `reports/phases/phase_14.md` (final audit)
- Phase 15: `reports/phases/phase_15_dataset_source_migration.md` (role/negation source migration)
- Phase 16: `reports/phases/phase_16_post_migration_full_rerun.md` (post-migration full recomputation)
- Phase 17: `reports/phases/phase_17_qualitative_review_response.md` (qualitative review response)
- Phase 18: `reports/phases/phase_18_regular_paper_extension.md` (modern decoders and output-level consistency)

Dataset-only claim policy:
- final claims use role + negation from the GitHub dataset only
- no human-annotation dependency in primary results

Core full artifacts:
- Metrics: `results/metrics/layer_metrics_full.csv`
- Surprisal: `results/surprisal/gpt2_surprisal_full.csv`
- Probes: `results/probes/probe_results_full.csv`
- Stats: `results/stats/full/`
- Qualitative analysis: `results/qualitative/`
- Output consistency: `results/consistency/`
- Modern decoder extension: `results/metrics/modern_mistral_7b_metrics.csv`, `results/stats/modern_mistral_7b/`
- Salience: `results/salience/`
- Figures: `results/figures/`
