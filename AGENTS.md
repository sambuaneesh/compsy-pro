# AGENTS.md

This repository implements **Counterfactual Structural Sensitivity (CSS)** for the course project:

**Counterfactual Structural Sensitivity: Human-Aligned Probing of Language Model Representations under Minimal Linguistic Edits**

The project asks whether language model internal representations change in linguistically meaningful ways under role reversal, negation, and attachment edits, and whether those changes align with 0-5 human semantic-change judgments.

## Non-negotiable project rules

1. **Do not pivot the project.** The core pipeline is:
   ```text
   sentence -> counterfactual edit -> hidden states -> representation shift -> probes + surprisal -> human alignment
   ```
2. **Primary phenomena:** role reversal, negation, attachment ambiguity.
3. **Primary models:** `bert-base-uncased`, `roberta-base`, `gpt2`.
4. **Primary metrics:** cosine shift, Frobenius/matrix-norm shift, L2 shift, token-aligned shift.
5. **Primary human target:** 0-5 semantic-change judgment.
6. **Primary surprisal source:** GPT-2 autoregressive surprisal.
7. **Do not overclaim human cognition.** Use "human-aligned semantic judgments" unless actual reading-time or brain data is collected.
8. **Every script must be config-driven and reproducible.**
9. **Do not silently change schemas.** Any schema change requires version bump and migration note.
10. **Every result must be traceable to a dataset hash, config hash, model identifier, package versions, and random seed.**

## Canonical repository structure

```text
css-counterfactual-probing/
  AGENTS.md
  README.md
  CITATION.cff
  requirements.txt
  pyproject.toml
  configs/
  data/
  src/css/
  cache/
  results/
  reports/
  tests/
  scripts/
```

## Agent roles

### 1. Project Lead / Config Guardian

**Responsibilities**

- Own `configs/`.
- Maintain schema versions:
  - `css_pair_v1`
  - `css_hidden_cache_v1`
  - `css_metrics_v1`
- Ensure every command can run from a config file.
- Maintain experiment manifests:
  - `configs/experiments/pilot.yaml`
  - `configs/experiments/full.yaml`
- Freeze configs before full-scale runs.

**Inputs**

- Research plan.
- Existing configs.
- Agent outputs.

**Outputs**

- Validated config files.
- `results/manifests/*.json`.
- Changelog entries for schema or config changes.

**Definition of done**

- `python -m css.data.validate_schema --config configs/experiments/pilot.yaml` passes.
- All config files include seed, model name, dataset path, output path, and cache policy.
- Full-run config is frozen before scaling.

---

### 2. Data Generation Agent

**Responsibilities**

- Implement:
  - `src/css/data/import_extending_psycholinguistic_dataset.py`
  - `src/css/data/generate_attachment.py`
  - `src/css/data/split_data.py`
  - `src/css/data/validate_schema.py`
- Generate:
  - `data/css_pairs/role_1500.jsonl`
  - `data/css_pairs/neg_1500.jsonl`
  - `data/css_pairs/attach_1500.jsonl`
- Include train/dev/test/human split labels.
- Compute surface controls:
  - token length
  - character length
  - lexical Jaccard
  - edit distance
  - length delta
- Store `edited_spans` with character offsets.

**Dependencies**

- External source dataset:
  - `data/external/extending_psycholinguistic_dataset/data/ROLE-1500.txt`
  - `data/external/extending_psycholinguistic_dataset/data/NEG-1500-SIMP-GEN.txt`
- Lexicons in `data/lexicons/` (attachment generation).
- Configs in `configs/data/`.

**Outputs**

- JSONL pair files.
- Validation report:
  - `results/data_validation/{phenomenon}_validation.json`
- Split summaries:
  - counts by phenomenon, edit type, template, lexical group.

**Definition of done**

- 1,500 valid records per phenomenon.
- No duplicate `id`.
- No empty span fields for relevant phenomena.
- Train/dev/test splits do not leak held-out lexical items in lexical-split mode.
- Attachment data includes ambiguity/disambiguation metadata.

---

### 3. Representation Extraction Agent

**Responsibilities**

- Implement:
  - `src/css/representations/extract_hidden.py`
  - `src/css/representations/pooling.py`
  - `src/css/representations/token_alignment.py`
  - `src/css/representations/cache_io.py`
- Extract hidden states for all layers:
  - embedding layer
  - layers 1-12
- Save:
  - mean-pooled vectors
  - CLS vectors where available
  - GPT-2 last-token vectors
  - word-level token matrices
  - subword metadata
- Use word-level aggregation as primary.

**Dependencies**

- JSONL data from Data Generation Agent.
- Model configs.
- Tokenizers and model identifiers pinned in configs.

**Outputs**

- Hidden-state caches under:
  - `cache/hidden/{model}/{dataset}/`
- Tokenization metadata under:
  - `cache/tokenized/{model}/{dataset}/`
- Cache manifest:
  - `cache/hidden/{model}/{dataset}/metadata.json`

**Definition of done**

- Cache can be loaded without re-tokenizing.
- Special tokens are excluded from primary mean-pool and token matrices.
- Word/subword alignment unit tests pass.
- Cache manifest includes model name, package versions, config hash, dataset hash, dtype, and seed.

---

### 4. Metric Computation Agent

**Responsibilities**

- Implement:
  - `src/css/metrics/cosine.py`
  - `src/css/metrics/matrix_norms.py`
  - `src/css/metrics/token_shift.py`
  - `src/css/metrics/compute_all_metrics.py`
- Compute per-pair, per-model, per-layer:
  - `delta_cos`
  - `sim_frob`
  - `delta_frob`
  - `delta_l2`
  - `delta_token_aligned`
- Implement ablations:
  - K clipping on/off
  - row normalization on/off
  - word vs subword matrix
  - length-matched subset flags

**Dependencies**

- Hidden-state caches.
- Pair JSONL surface controls.

**Outputs**

- `results/metrics/layer_metrics.parquet`
- `results/metrics/layer_metrics_summary.csv`
- Warnings file for numerical anomalies.

**Definition of done**

- Frobenius similarities are usually in `[0,1]`; any out-of-range values are flagged with pair/model/layer IDs.
- Metrics reproduce exactly when rerun with same config.
- Unit tests verify Frobenius formula on small matrices.
- Metrics table includes all required covariates.

---

### 5. Probe Agent

**Responsibilities**

- Implement:
  - `src/css/probes/build_probe_dataset.py`
  - `src/css/probes/train_linear_probe.py`
  - `src/css/probes/selectivity_controls.py`
- Train linear probes by layer for:
  - role target-span role: `agent` vs `patient`
  - negation presence and optional scope
  - attachment class: `VP_attachment` vs `NP_attachment`
- Run controls:
  - random-label control
  - template split
  - lexical split
  - surface baseline
- Use 5 seeds.

**Dependencies**

- Hidden-state caches.
- Pair metadata.
- Configs in `configs/experiments/probes.yaml`.

**Outputs**

- `results/probes/probe_results.csv`
- `results/probes/probe_predictions.parquet`
- `results/probes/selectivity_summary.csv`

**Definition of done**

- Every reported probe has corresponding control score.
- Selectivity is computed as task metric minus control metric.
- Role probe uses active/passive controls or otherwise explicitly reports surface-order confound.
- Probe configs include regularization, seed, feature type, split type, and layer list.

---

### 6. Surprisal Agent

**Responsibilities**

- Implement:
  - `src/css/surprisal/gpt2_surprisal.py`
  - optional `src/css/surprisal/mlm_pll.py`
- GPT-2 primary:
  - total sentence surprisal
  - average token surprisal
  - delta total
  - delta average
  - key-region surprisal
- BERT/RoBERTa PLL optional and secondary only.

**Dependencies**

- Pair JSONL with edited/key spans.
- GPT-2 tokenizer and model config.

**Outputs**

- `results/surprisal/gpt2_surprisal.csv`
- optional `results/surprisal/mlm_pll.csv`
- key-region coverage report.

**Definition of done**

- GPT-2 scoring has unit tests on short strings.
- Key-region extraction succeeds for at least 98% of items or failures are documented.
- BERT/RoBERTa PLL is never mixed with GPT-2 AR surprisal in the same primary claim.

---

### 7. Human Annotation Agent

**Responsibilities**

- Implement:
  - `src/css/annotation/make_batches.py`
  - `src/css/annotation/aggregate_annotations.py`
  - `src/css/annotation/agreement.py`
- Create balanced annotation batches.
- Randomize pair order and sentence order where appropriate.
- Include attention checks and duplicates.
- Aggregate human scores.

**Dependencies**

- Human subset split from Data Generation Agent.
- Annotation prompt in `reports/appendix/annotation_prompt.md`.

**Outputs**

- `data/annotations/human_css_0_5.csv`
- `data/annotations/human_css_aggregated.csv`
- `results/annotation/agreement_report.json`

**Definition of done**

- 200-500 pairs annotated.
- At least 3 annotators per pair.
- Agreement metrics computed.
- Items with high disagreement flagged.
- Annotation prompt and scale are archived.

---

### 8. Statistics Agent

**Responsibilities**

- Implement:
  - `src/css/stats/correlations.py`
  - `src/css/stats/bootstrap.py`
  - `src/css/stats/multiple_comparisons.py`
  - `src/css/stats/mixed_effects.R`
- Run H1-H5 tests.
- Compute:
  - Spearman primary correlations
  - Pearson secondary correlations
  - bootstrap CIs
  - FDR-corrected p-values
  - mixed-effects regressions
  - nested model comparison for Frobenius incremental value

**Dependencies**

- Metrics table.
- Human aggregated and raw annotation files.
- Surprisal results.
- Probe results.

**Outputs**

- `results/stats/correlations.csv`
- `results/stats/bootstrap_cis.csv`
- `results/stats/mixed_effects_summary.csv`
- `results/stats/hypothesis_tests.md`

**Definition of done**

- Each hypothesis H1-H5 has a result table.
- All p-values in multi-layer analyses have FDR-adjusted values.
- Regression predictors are z-scored.
- Mixed model includes item and annotator random intercepts when using raw annotations.
- Full scripts rerun from clean checkout.

---

### 9. Salience Agent

**Responsibilities**

- Implement:
  - `src/css/salience/token_contributions.py`
  - `src/css/salience/evaluate_salience.py`
- Compute salience scores from:
  - Frobenius row/column contributions
  - leave-one-out matrix-norm contribution
  - token-aligned cosine drop
- Evaluate against gold edited/structural spans.

**Dependencies**

- Token matrices.
- Edited span metadata.
- Metrics.

**Outputs**

- `results/salience/token_contributions.parquet`
- `results/salience/salience_eval.csv`

**Definition of done**

- Gold spans mapped to token indices.
- Recall@1, Recall@3, MRR reported.
- Salience results clearly labeled secondary/exploratory.

---

### 10. Plotting and Paper Agent

**Responsibilities**

- Implement:
  - `src/css/plots/plot_layer_curves.py`
  - `src/css/plots/plot_ablation_tables.py`
- Produce:
  - layer-wise correlation curves
  - Frobenius vs cosine comparison plots
  - probe selectivity curves
  - surprisal-vs-human plots
  - ablation tables
- Draft workshop paper.

**Dependencies**

- Stats outputs.
- Probe outputs.
- Surprisal outputs.
- Bibliography.

**Outputs**

- `results/figures/*.pdf`
- `results/tables/*.csv`
- `reports/workshop_paper/paper.md`
- `reports/appendix/*.md`

**Definition of done**

- Every plot is generated by a script.
- Every figure/table has a source data file.
- Paper states primary vs exploratory claims.
- Limitations section explicitly avoids human-cognition overclaims.

---

## Coding standards

- Python package root: `src/css/`.
- Use type hints for public functions.
- All scripts must support:
  - `--config`
  - `--output`
  - `--seed`
  - `--force` where recomputation is possible
- Use `logging`, not `print`, for pipeline scripts.
- Use deterministic sorting before writing outputs.
- Avoid notebook-only results. Notebooks may inspect outputs but cannot be the only source of a result.
- Unit tests go in `tests/`.
- Large generated caches must not be committed unless explicitly configured.

## Incremental serialized logging (mandatory)

- All meaningful work blocks must append a JSONL event in `logs/incremental/phase_XX.jsonl`.
- Use:
  ```bash
  uv run python scripts/log_event.py --phase <N> --event-type <type> --summary "<summary>" --artifact <path>
  ```
- Event schema is defined in `logs/incremental/README.md`.
- Do not edit historical log lines; append corrective events instead.

## Reproducibility checklist

Every full run must archive:

- Git commit hash.
- All config files.
- Dataset checksums.
- Model identifiers:
  - `bert-base-uncased`
  - `roberta-base`
  - `gpt2`
- Package versions:
  - Python
  - PyTorch
  - Transformers
  - tokenizers
  - numpy
  - pandas
  - scipy
  - scikit-learn
  - statsmodels or R/lme4
- Random seeds.
- Hardware note: CPU/GPU, dtype, batch size.
- Cached hidden-state metadata.
- Exact statistical scripts.
- Annotation prompt and anonymized annotation file.

## Citation discipline

Use and cite the following references in the paper and README when their ideas are used:

- Matrix norms for similarity: vor der Brück and Pouly 2019.
- External role/negation source dataset: text-machine-lab extending_psycholinguistic_dataset.
- Minimal-pair benchmark framing: Warstadt et al. 2020 BLiMP.
- Semantic relatedness calibration: Abdalla et al. 2023 STR-2022.
- Semantic similarity calibration: GLUE / STS-B and SemEval STS.
- Models: Devlin et al. 2019 BERT; Liu et al. 2019 RoBERTa; Radford et al. 2019 GPT-2.
- Psycholinguistic LM diagnostics: Ettinger 2020; Lee et al. 2024.
- Probe controls: Hewitt and Liang 2019.
- Surprisal: Levy 2008; GPT-2 scoring as AR LM.
- MLM PLL: Salazar et al. 2020, optional only.
- CKA/RSA: Kornblith et al. 2019 and Kriegeskorte et al. 2008, optional only.
- Mixed effects / FDR / bootstrap as used in statistics section.

## Pipeline commands expected by final implementation

Pilot:

```bash
bash scripts/sync_external_dataset.sh
python -m css.data.import_extending_psycholinguistic_dataset --config configs/data/external_import.yaml
python -m css.data.generate_attachment --config configs/data/attachment.yaml --n 100
python -m css.data.validate_schema --config configs/experiments/pilot.yaml

python -m css.representations.extract_hidden --config configs/experiments/pilot.yaml
python -m css.metrics.compute_all_metrics --config configs/experiments/pilot.yaml
python -m css.surprisal.gpt2_surprisal --config configs/experiments/pilot.yaml
python -m css.probes.train_linear_probe --config configs/experiments/probes.yaml
python -m css.stats.correlations --config configs/experiments/stats.yaml
```

Full run:

```bash
bash scripts/run_full_metrics.sh
bash scripts/run_probes.sh
bash scripts/run_stats.sh
```

## Definitions of primary vs exploratory

Primary:

- H1-H5.
- Human semantic-change alignment.
- Cosine vs Frobenius comparison.
- GPT-2 surprisal as covariate.
- Selectivity-controlled probes.

Exploratory:

- BERT/RoBERTa PLL.
- CKA/RSA.
- Salience detection.
- Attachment results if controls fail.
- Any additional model beyond BERT/RoBERTa/GPT-2.

## Final definition of done for the repository

The project is complete when:

1. `role_1500.jsonl`, `neg_1500.jsonl`, and `attach_1500.jsonl` validate.
2. Hidden states are cached for all three models.
3. Metrics are computed for all pairs, layers, and models.
4. Human annotation exists for at least 300 balanced pairs, or documented course-project fallback is used.
5. Probes and controls are run.
6. GPT-2 surprisal is computed.
7. H1-H5 tables are generated with bootstrap CIs and FDR correction.
8. Figures and tables are script-generated.
9. Workshop paper draft exists with limitations and bibliography.
10. Reproducibility checklist is complete.
