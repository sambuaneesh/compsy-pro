# Phase 15: Dataset Source Migration (2026-04-24)

## Objective

Adopt `text-machine-lab/extending_psycholinguistic_dataset` as the canonical source for role and negation modules.

## Changes Implemented

- Added importer:
  - `src/css/data/import_extending_psycholinguistic_dataset.py`
- Added config:
  - `configs/data/external_import.yaml`
- Updated run scripts:
  - `scripts/run_pilot.sh`
  - `scripts/run_full_metrics.sh`
- Regenerated canonical datasets:
  - `data/css_pairs/role_1500.jsonl`
  - `data/css_pairs/neg_1500.jsonl`
  - `data/css_pairs/attach_1500.jsonl` (unchanged generator)
  - merged pilot/full JSONL files
- Wrote provenance manifest:
  - `results/data_validation/external_dataset_manifest.json`

## Validation

- `pilot_schema_validation.json`: `status=ok`, `issues=0`
- `full_schema_validation.json`: `status=ok`, `issues=0`
- Updated split summaries:
  - `results/data_validation/pilot_split_summary.json`
  - `results/data_validation/full_split_summary.json`

## Notes

- Role/negation model outputs generated before migration should be considered pre-migration artifacts.
- Full extraction/metrics/probes/stats should be rerun on migrated data before final submission claims.
