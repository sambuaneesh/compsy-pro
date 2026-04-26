# Counterfactual Structural Sensitivity (CSS): Dataset-Only Plan

## Scope Lock (Final)

This project is now locked to a strict dataset-only track.

- Data source: `text-machine-lab/extending_psycholinguistic_dataset`
- Phenomena used:
  - role reversal (`ROLE-1500.txt`)
  - negation (`NEG-1500-SIMP-GEN.txt`)
- Canonical converted outputs:
  - `data/css_pairs/role_1500.jsonl`
  - `data/css_pairs/neg_1500.jsonl`
  - merged `data/css_pairs/full_all_3000.jsonl`

No human annotation is part of the primary pipeline.

## Core Pipeline

```text
sentence -> counterfactual edit -> hidden states -> representation shift
-> probes + GPT-2 surprisal -> dataset-level statistics
```

## Models

Primary baseline models:
- `bert-base-uncased`
- `roberta-base`
- `gpt2`

Layers: embedding + transformer layers 1..12 (indexed 0..12 in outputs).

Regular-paper extension models:
- `mistralai/Mistral-7B-Instruct-v0.3` as the preferred modern instruction decoder if accessible and computationally feasible.
- `Qwen/Qwen3-8B` as the stronger Qwen target, with `device_map: auto`/CPU offload required on 16GB GPUs.
- `Qwen/Qwen3-4B` as a practical public fallback when 8B hidden-state extraction is too slow or memory constrained.
- `google/gemma-3-4b-it` and `meta-llama/Llama-3.1-8B` are configured only if the available Hugging Face token has gated-model access.

## Primary Metrics

- `delta_cos`
- `sim_frob` and `delta_frob`
- `delta_l2`
- `delta_token_aligned`

## Probes

- role probe: `agent` vs `patient`
- negation probe: presence/absence
- controls:
  - random-label control
  - selectivity reporting
  - multi-seed runs

## Surprisal

Primary psycholinguistic signal:
- GPT-2 autoregressive surprisal
- total, average, and counterfactual delta features
- key-region coverage report

## Dataset-Only Statistical Targets

- D1: correlation of shift metrics with `abs_delta_avg_surprisal`
- D2: incremental value of `delta_frob` beyond `delta_cos`
- D3: model/phenomenon-specific layer profiles
- D4: probe selectivity stability across layers
- D5: qualitative case-study audit for high/low shift and surprisal dissociations
- D6: output-level counterfactual consistency for regular-paper positioning:
  identical sentence controls should receive `yes`;
  counterfactual role/negation pairs should receive `no`;
  report accuracy, yes-rate bias, and forced-choice score margins.

Outputs:
- `results/stats/full/correlations.csv`
- `results/stats/full/bootstrap_cis.csv`
- `results/stats/full/h2_incremental.csv`
- `results/stats/full/hypothesis_tests.md`
- `results/qualitative/qualitative_cases.csv`
- `results/consistency/*counterfactual_consistency.csv`
- `results/consistency/summary/consistency_report.md`
- `reports/full/QUALITATIVE_ANALYSIS.md`

## Reproducibility Requirements

Every full run must archive:
- git commit hash
- config files
- dataset checksums
- model ids
- package versions
- random seed
- hidden-state cache metadata

Incremental serialized logs are mandatory:
- `logs/incremental/phase_XX.jsonl`
- append-only event records via `scripts/log_event.py`

## Final Deliverables

1. Full extraction/metrics/surprisal run on role+negation.
2. Full probe/selectivity run for all models and layers.
3. Dataset-only stats and figures.
4. Qualitative case-study audit explaining aggregate patterns with actual sentence pairs.
5. Regular-paper extension results for at least one modern decoder or one output-level consistency experiment.
6. Slides and paper narrative aligned to dataset-only claims.
7. Reproducibility checklist and run manifests complete.
