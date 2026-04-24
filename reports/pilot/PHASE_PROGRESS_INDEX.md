# CSS Pilot Progress Index (Phases 0-8)

Last updated: `2026-04-24`

## Completed Phases

- Phase 0: tooling/governance baseline
- Phase 1: schema/config freeze
- Phase 2: pilot + full dataset generation and validation
- Phase 3: hidden-state extraction/caching
- Phase 4: CSS metric computation
- Phase 5: GPT-2 surprisal
- Phase 6: probes with random-label controls
- Phase 7: annotation pipeline pilot (currently simulated ratings)
- Phase 8: integrated pilot statistics and go/no-go summary

## Where To Look

- Phase reports: `reports/phases/phase_03.md` ... `reports/phases/phase_08.md`
- Incremental logs: `logs/incremental/phase_00.jsonl` ... `phase_08.jsonl`
- Pilot metrics: `results/metrics/`
- Pilot surprisal: `results/surprisal/`
- Pilot probes: `results/probes/`
- Pilot annotation artifacts: `data/annotations/` and `results/annotation/`
- Pilot stats: `results/stats/`

## Current Limitation

- `data/annotations/human_css_0_5.csv` is synthetic for pipeline continuity.
- Replace with real human annotation before final paper claims on human alignment.

## Re-run Pilot End-to-End

```bash
bash scripts/run_pilot.sh
```
