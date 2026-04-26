# AGENTS.md

This repository implements Counterfactual Structural Sensitivity (CSS) for:

Counterfactual Structural Sensitivity: Probing Language Model Representations under Minimal Linguistic Edits

Current scope is strictly dataset-only and uses the GitHub source dataset:
`text-machine-lab/extending_psycholinguistic_dataset`.

## Non-negotiable project rules

1. Do not pivot the core pipeline:
   sentence -> counterfactual edit -> hidden states -> representation shift -> probes + surprisal -> dataset-level analysis
2. Primary phenomena are only:
   - role reversal
   - negation
3. Primary models are fixed:
   - `bert-base-uncased`
   - `roberta-base`
   - `gpt2`
4. Primary metrics are fixed:
   - cosine shift
   - Frobenius/matrix-norm shift
   - L2 shift
   - token-aligned shift
5. Primary surprisal source is GPT-2 autoregressive surprisal.
6. No human-annotation dependency is allowed in primary claims, scripts, or gates.
7. Every script must be config-driven and reproducible.
8. Do not silently change schemas. Any schema change needs a version bump and migration note.
9. Every result must be traceable to dataset hash, config hash, model id, package versions, and seed.

## Canonical repository structure

```text
css-counterfactual-probing/
  AGENTS.md
  README.md
  pyproject.toml
  configs/
  data/
  src/css/
  cache/
  results/
  reports/
  tests/
  scripts/
  logs/incremental/
```

## Active implementation roles

### 1. Project Lead / Config Guardian

Responsibilities:
- own `configs/`
- freeze `configs/experiments/pilot.yaml` and `configs/experiments/full.yaml`
- enforce deterministic seeds and output locations
- publish run manifests in `results/manifests/`

Definition of done:
- `python -m css.data.validate_schema --config configs/experiments/pilot.yaml` passes
- full config is frozen before scaling

### 2. Data Agent

Responsibilities:
- import role and negation pairs from external GitHub dataset:
  - `src/css/data/import_extending_psycholinguistic_dataset.py`
- validate schema and controls:
  - `src/css/data/validate_schema.py`
  - `src/css/data/split_data.py`
- generate:
  - `data/css_pairs/role_1500.jsonl`
  - `data/css_pairs/neg_1500.jsonl`
  - merged `data/css_pairs/full_all_3000.jsonl`

Definition of done:
- 1500 valid rows each for role and negation
- no duplicate ids
- schema validation reports are clean

### 3. Representation Agent

Responsibilities:
- `src/css/representations/extract_hidden.py`
- `src/css/representations/pooling.py`
- `src/css/representations/token_alignment.py`
- cache hidden states and metadata under `cache/hidden/`

Definition of done:
- all layers cached (embedding + 1..12)
- metadata includes model, versions, hashes, dtype, seed

### 4. Metrics Agent

Responsibilities:
- `src/css/metrics/compute_all_metrics.py`
- `src/css/metrics/cosine.py`
- `src/css/metrics/matrix_norms.py`
- `src/css/metrics/token_shift.py`

Definition of done:
- per-pair, per-layer, per-model metrics written
- Frobenius anomalies logged (if any)

### 5. Probe Agent

Responsibilities:
- `src/css/probes/train_linear_probe.py`
- `src/css/probes/selectivity_controls.py`
- run selectivity controls with 5 seeds

Definition of done:
- probe outputs include task and control scores
- selectivity summaries generated

### 6. Surprisal Agent

Responsibilities:
- `src/css/surprisal/gpt2_surprisal.py`
- compute sentence and edited-region deltas

Definition of done:
- full surprisal table generated for merged dataset
- key-region coverage report generated

### 7. Statistics Agent (Dataset-Only)

Responsibilities:
- `src/css/stats/dataset_only_summary.py`
- compute:
  - metric vs surprisal correlations
  - bootstrap CIs
  - BH-FDR adjusted p-values
  - Frobenius incremental value over cosine for surprisal target

Definition of done:
- outputs exist in `results/stats/full/`
- no annotation files are required

### 8. Salience + Plotting Agent

Responsibilities:
- `src/css/salience/token_contributions.py`
- `src/css/salience/evaluate_salience.py`
- `src/css/plots/plot_layer_curves.py`
- `src/css/plots/plot_ablation_tables.py`

Definition of done:
- all figures/tables are script-generated from current result files

### 9. Qualitative Analysis Agent

Responsibilities:
- `src/css/analysis/qualitative_cases.py`
- generate representative high/low Frobenius and surprisal case studies
- audit surface-form differences between role reversal and negation
- update qualitative interpretation notes without introducing human-annotation claims

Definition of done:
- `results/qualitative/qualitative_cases.csv` exists
- `reports/full/QUALITATIVE_ANALYSIS.md` explains aggregate patterns with actual sentence pairs
- slides and presenter transcript mention the qualitative audit

## Coding standards

- Python package root is `src/css/`.
- Use type hints on public functions.
- Scripts support `--config`; support `--output`, `--seed`, `--force` where relevant.
- Use `logging` for pipeline scripts.
- Deterministically sort outputs before writing.
- Avoid notebook-only results.

## Incremental serialized logging (mandatory)

Append every meaningful work block to:
- `logs/incremental/phase_XX.jsonl`

Use:

```bash
uv run python scripts/log_event.py --phase <N> --event-type <type> --summary "<summary>" --artifact <path>
```

Never rewrite historical log lines. Append corrective entries when needed.

## Reproducibility checklist

Every full run archives:
- git commit hash
- configs used
- dataset checksums
- model ids (`bert-base-uncased`, `roberta-base`, `gpt2`)
- package versions
- seed values
- hardware note and dtype/batch size
- hidden-cache metadata
- exact stats and plotting scripts used

## Citation discipline

When relevant, cite:
- Devlin et al. 2019 (BERT)
- Liu et al. 2019 (RoBERTa)
- Radford et al. 2019 (GPT-2)
- Warstadt et al. 2020 (BLiMP framing)
- Hewitt and Liang 2019 (probe selectivity)
- Levy 2008 (surprisal)
- vor der Bruck and Pouly 2019 (matrix norms)
- Ettinger 2020, Lee et al. 2024 (psycholinguistic LM diagnostics)

## Expected pipeline commands

Pilot:

```bash
bash scripts/run_pilot.sh
```

Full:

```bash
bash scripts/run_full_metrics.sh
bash scripts/run_probes.sh
bash scripts/run_stats.sh
bash scripts/run_salience_and_plots.sh
bash scripts/run_qualitative_analysis.sh
```

## Primary vs exploratory

Primary:
- role + negation
- all four representation shift metrics
- GPT-2 surprisal
- probe selectivity controls
- dataset-only statistical summaries

Exploratory:
- salience detection
- extra datasets not in the GitHub source
- additional models beyond the three fixed baselines

Regular-paper extension track:
- Keep the three baseline models as the primary CSS comparison set.
- Add modern decoder-only LLMs only as an extension layer for regular-paper claims.
- Candidate modern decoders:
  - `mistralai/Mistral-7B-Instruct-v0.3`
  - `Qwen/Qwen3-8B`
  - `Qwen/Qwen3-4B` as a practical public fallback for 16GB GPUs
  - `google/gemma-3-4b-it` only if gated Hugging Face access is available
  - `meta-llama/Llama-3.1-8B` only if gated Hugging Face access is available
- Output-level counterfactual consistency is an extension experiment, not a replacement for hidden-state CSS:
  identical sentence control -> expected `yes`
  counterfactual edit pair -> expected `no`
- Treat output-level results as forced-choice behavioral diagnostics. Do not overclaim them as full logical reasoning or human-aligned semantic judgments.
- If 7B/8B models exceed GPU memory, prefer config-driven `device_map: auto` and documented CPU offload over ad-hoc code edits.

## Final definition of done

Repository is complete when:
1. `role_1500.jsonl` and `neg_1500.jsonl` validate.
2. Hidden states are cached for all three models.
3. Metrics are computed for all pairs, layers, and models.
4. Probes and selectivity controls run successfully.
5. GPT-2 surprisal is computed for all pairs.
6. Dataset-only stats tables and CIs are generated.
7. Figures/tables are script-generated.
8. Reproducibility checklist is complete.
