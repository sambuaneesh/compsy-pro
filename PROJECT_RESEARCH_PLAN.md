# Counterfactual Structural Sensitivity (CSS): Research Plan

## 1. Refined title and abstract-level framing

**Refined title:**  
**Counterfactual Structural Sensitivity: Human-Aligned Probing of Language Model Representations under Minimal Linguistic Edits**

**Short title:** Counterfactual Structural Sensitivity (CSS)

**Abstract-level framing:**  
This project introduces **Counterfactual Structural Sensitivity (CSS)**, a protocol for testing whether language-model representations respond in linguistically meaningful ways to minimal counterfactual edits. CSS constructs paired sentences differing by controlled edits—role reversal, negation, and attachment changes—extracts layer-wise hidden representations from BERT, RoBERTa, and GPT-2, and measures representational shifts using centroid cosine, Frobenius/matrix-norm similarity, L2 shift, and token-aligned shift. The central evaluation asks whether these representation shifts align with **human semantic-change judgments** on a 0–5 scale. The project links four signals: internal representation shift, recoverable linguistic information from probes, autoregressive surprisal, and human semantic-change ratings. The work is positioned as a controlled, representation-level complement to minimal-pair benchmarks such as BLiMP and to psycholinguistic LM diagnostics, not as a claim that LMs process language like humans.

## 2. Final problem statement

Given a sentence `s` and a minimally edited counterfactual `s_cf`, do internal representations of pretrained language models change in a way that tracks the semantic impact of the edit, and does that change align with human ratings of semantic change?

Formally, for item `i`, model `m`, layer `l`, edit phenomenon `p`, representation function `R_l^m(.)`, and human semantic-change score `y_i in [0,5]`, estimate whether:

```text
Delta_l^m(s_i, s_i_cf) = distance_or_shift(R_l^m(s_i), R_l^m(s_i_cf))
```

predicts `y_i`, after controlling for surface overlap, length, tokenization, template family, edit type, surprisal, and probe-derived recoverability.

The primary dependent variable is **human semantic-change judgment**, not acceptability, grammaticality, truth, reading time, or brain response.

## 3. Hypotheses H1-H5

**H1: Human-aligned shift.**  
Layer-wise representational shift between `s` and `s_cf` will positively correlate with human semantic-change ratings. Larger human-rated semantic changes should generally yield larger representation shifts.

**H2: Matrix-norm complementarity.**  
Frobenius/matrix-norm shift will explain variance in human semantic-change ratings beyond centroid cosine shift, especially for edits where local token-token relations matter, such as role reversal and attachment changes.

**H3: Phenomenon-specific layer profiles.**  
Sensitivity profiles will differ by phenomenon. Negation may show strong lexical/scope-sensitive effects in lower-to-middle layers; role reversal and attachment may show stronger effects in middle-to-upper layers. This is a directional hypothesis, not a guarantee of a fixed universal peak layer.

**H4: Surprisal as complementary, not sufficient.**  
GPT-2 autoregressive surprisal features will predict part of the variance associated with plausibility and processing difficulty, but representation-shift metrics will retain explanatory value for human semantic-change judgments after surprisal controls.

**H5: Robustness under controls.**  
CSS effects should remain detectable under length, lexical-overlap, tokenization, template-split, lexical-split, and random-label/selectivity controls. If an effect disappears under these controls, it is treated as a confounded or exploratory result.

## 4. Contributions and novelty claims, with caveats

### Primary contributions

1. **CSS protocol:** a reusable counterfactual protocol for measuring layer-wise structural sensitivity under minimal edits.
2. **Human-aligned semantic-change evaluation:** 0–5 human judgments for a balanced subset of role reversal, negation, and attachment pairs.
3. **Representation-comparison expansion:** comparison of centroid cosine shift with Frobenius/matrix-norm shift adapted from matrix-norm text similarity.
4. **Layer-wise interpretability bridge:** joint analysis of shift metrics, probes, surprisal, and human semantic-change judgments.
5. **Controls-first probing:** selectivity controls, random-label controls, template splits, lexical splits, tokenization controls, and length/overlap covariates.

### Caveats

- The project evaluates **alignment with human semantic judgments**, not human real-time processing or neural activity.
- The generated datasets are controlled and useful for causal comparisons, but they may not represent naturalistic distributional language use.
- Probing accuracy is not interpreted as direct evidence that a model “knows” a linguistic structure unless it survives selectivity and lexical controls.
- Attachment ambiguity is the riskiest phenomenon and should be interpreted with the strongest caveats if template artifacts remain.

## 5. Holes, confounds, and fixes

| Hole or confound | Risk | Fix |
|---|---|---|
| Length changes from negation insertion | Larger shifts may reflect added tokens | Include length delta, token count delta, edit distance, and mean-pooling controls; report no-negator pooling ablation |
| Tokenization differences across models | BPE/WordPiece fragmentation affects matrices | Use word-level aggregation as primary; subword-level as ablation |
| Lexical overlap dominates | High overlap may hide semantic change | Include lexical-overlap covariate; use role reversal as a high-overlap semantic-change stress test |
| Template artifacts | Probes may learn template ID | Template split; report within-template and held-out-template performance |
| Lexical memorization in probes | High probe accuracy may not reflect representation encoding | Random-label/selectivity controls; lexical split by nouns, verbs, PP heads, and negators |
| Role probe surface-order shortcut | Active SVO makes first NP agent | Add passive and cleft controls in probe data; probe target noun role, not just sentence order |
| Negation lexical cue shortcut | Probe may detect “not” only | Exclude negation tokens from pooled features; add scope or no-negator ablation |
| Attachment labels are noisy | “With the telescope” can remain genuinely ambiguous | Use disambiguating paraphrase pairs and store ambiguity status; make attachment conclusions conservative |
| Matrix norms may be length-sensitive | Larger matrices can inflate norms | Use normalized matrix-norm similarity; include length covariates and length-matched subsets |
| Human score noise | Low agreement weakens correlations | Use 3-5 annotators/item, attention checks, agreement metrics, and bootstrap CIs |
| Surprisal not comparable across MLMs and AR LMs | BERT/RoBERTa PLL is not GPT-2 surprisal | GPT-2 surprisal is primary; MLM PLL is optional and reported separately |

## 6. Dataset plan

### 6.1 Role reversal data: `role_1500.jsonl`

**Goal:** Create high-lexical-overlap pairs where agent and patient/theme roles are reversed.

Example:

```text
s:    The chef praised the waiter.
s_cf: The waiter praised the chef.
```

Required metadata: `agent_s`, `patient_s`, `agent_cf`, `patient_cf`, `verb`, `voice`, `animacy`, `reversibility`, `plausibility_class`, `template_id`, `edited_spans`.

Design:

- 1,500 generated pairs.
- Active transitive templates as the core CSS set.
- Additional passive/cleft variants for role-probe controls.
- Verb classes balanced across communication, transfer, perception, contact, emotion, and social-action verbs.
- Noun lexicons split across train/dev/test to prevent lexical leakage.
- Plausibility controlled by pairing reversible events separately from asymmetric events.

Primary label:

```text
role_direction = agent_patient_mapping
edit_type = swap_agent_patient
```

### 6.2 Negation data: `neg_1500.jsonl`

**Goal:** Create minimal edits that insert, remove, or alter sentential/predicate negation.

Example:

```text
s:    The judge approved the request.
s_cf: The judge did not approve the request.
```

Design:

- 1,500 pairs.
- Balanced edit types:
  - `insert_not`
  - `remove_not`
  - `replace_affirmative_with_negative_aux`
  - optional `never` / `no longer` subset
- Keep tense, subject, object, and main predicate constant where possible.
- Store negation cue span and scope span.
- Include no-negator pooling ablation to test whether shift/probes rely only on the explicit token.

Primary labels:

```text
negation_s in {0,1}
negation_cf in {0,1}
negation_scope = predicate_span
edit_type = insert_not | remove_not | ...
```

### 6.3 Attachment ambiguity data: `attach_1500.jsonl`

**Goal:** Test representation sensitivity to minimal or near-minimal changes in attachment interpretation, especially PP attachment.

Because pure PP-attachment minimality is difficult without lexical confounds, store attachment as a controlled disambiguation phenomenon with explicit caveats.

Example family:

```text
ambiguous: The detective saw the man with the telescope.
vp_disambig: With the telescope, the detective saw the man.
np_disambig: The detective saw the man who had the telescope.
```

CSS pairs may compare `vp_disambig` vs `np_disambig`, or ambiguous vs disambiguated variants.

Design:

- 1,500 records, preferably as triplets internally:
  - ambiguous base
  - VP-attachment paraphrase
  - NP-attachment paraphrase
- Pair records generated from these triplets:
  - `ambiguous_to_vp`
  - `ambiguous_to_np`
  - `vp_to_np`
- Store `attachment_site`, `attachment_class_s`, `attachment_class_cf`, `pp_span`, `head_candidate_1`, `head_candidate_2`.
- Run attachment analyses both with and without lexical PP-head controls.
- Treat attachment as primary only if controls pass; otherwise mark as exploratory.

### 6.4 Human semantic-change annotation: `human_role_0_5.csv` plus combined file

Human annotation should cover 200-500 pairs, balanced across phenomena.

Recommended course-project target:

```text
300 total pairs = 100 role + 100 negation + 100 attachment
3 annotators per pair
```

Stretch target:

```text
500 total pairs
5 annotators per pair
```

Prompt:

> You will see two English sentences. Rate how much the core meaning changes from Sentence A to Sentence B. Use 0 for no meaning change and 5 for a very large meaning change. Focus on who did what to whom, whether the event happened, and what phrase attaches to what. Do not rate grammar or writing style unless it changes the meaning.

Scale:

| Score | Meaning |
|---:|---|
| 0 | Same meaning / paraphrase |
| 1 | Tiny wording or detail change |
| 2 | Small semantic change, same event mostly preserved |
| 3 | Clear semantic change, same topic/event frame |
| 4 | Major change in event/state/roles/scope |
| 5 | Opposite, incompatible, role-reversed, or radically different meaning |

Collect optional confidence and fluency/plausibility ratings to control for bad items.

### 6.5 STS-B / STR-2022 calibration: `sts_alignment/`

Use STS-B as a semantic-similarity calibration set and STR-2022 as a semantic-relatedness calibration set.

Protocol:

- Sample 500 STS-B pairs and map `semantic_change = 5 - similarity`.
- Sample 500 STR-2022 pairs and analyze relatedness separately from similarity.
- Do not train the CSS metrics on STS-B/STR; use them as sanity checks for whether shift metrics behave sensibly outside the counterfactual data.
- Report separately because semantic similarity, semantic relatedness, and counterfactual semantic change are related but non-identical constructs.

### 6.6 Salience-detection extension

Define salience as **the degree to which an edited token/span or structurally implicated token/span accounts for the representation shift and human-rated semantic change**.

Secondary experiment:

- Gold salient spans: edit cue, swapped arguments, negation cue/scope, PP/head candidates.
- Compute token contribution scores from matrix norms and token-aligned shift.
- Evaluate whether gold edited/structural spans rank highly:
  - Recall@1, Recall@3
  - MRR
  - AUC if span-level labels are available
- Optional human salience stretch: ask annotators to highlight words responsible for the semantic change.

## 7. Exact data schema

### 7.1 Pair JSONL schema

Each line in `data/css_pairs/{phenomenon}_1500.jsonl`:

```json
{
  "id": "role_000001",
  "schema_version": "css_pair_v1",
  "phenomenon": "role_reversal",
  "s": "The chef praised the waiter.",
  "s_cf": "The waiter praised the chef.",
  "edit_type": "swap_agent_patient",
  "source": "templated",
  "template_id": "role_active_transitive_v01",
  "split": "train",
  "gold_label": {
    "role_direction_s": "chef_agent_waiter_patient",
    "role_direction_cf": "waiter_agent_chef_patient",
    "negation_s": null,
    "negation_cf": null,
    "attachment_s": null,
    "attachment_cf": null
  },
  "linguistic_metadata": {
    "agent_s": "chef",
    "patient_s": "waiter",
    "agent_cf": "waiter",
    "patient_cf": "chef",
    "verb_s": "praised",
    "verb_cf": "praised",
    "voice_s": "active",
    "voice_cf": "active",
    "tense": "past",
    "animacy": "animate_animate",
    "plausibility_class": "reversible_plausible"
  },
  "edited_spans": {
    "s": [
      {"label": "agent", "text": "chef", "char_start": 4, "char_end": 8},
      {"label": "patient", "text": "waiter", "char_start": 20, "char_end": 26}
    ],
    "s_cf": [
      {"label": "agent", "text": "waiter", "char_start": 4, "char_end": 10},
      {"label": "patient", "text": "chef", "char_start": 22, "char_end": 26}
    ]
  },
  "surface_controls": {
    "token_len_s": 5,
    "token_len_cf": 5,
    "char_len_s": 27,
    "char_len_cf": 27,
    "lexical_jaccard": 1.0,
    "levenshtein_distance": 12
  },
  "human_change": null,
  "notes": ""
}
```

### 7.2 Human annotation CSV schema

`data/annotations/human_css_0_5.csv`:

```csv
pair_id,phenomenon,s,s_cf,annotator_id,batch_id,human_change_0_5,confidence_1_5,fluency_s_1_5,fluency_cf_1_5,plausibility_s_1_5,plausibility_cf_1_5,changed_words,attention_check,created_at
```

Aggregated file:

```csv
pair_id,phenomenon,n_annotators,mean_change,median_change,sd_change,mean_confidence,mean_fluency_s,mean_fluency_cf,agreement_flag
```

### 7.3 Representation cache metadata schema

`cache/hidden/{model_name}/{dataset_name}/metadata.json`:

```json
{
  "schema_version": "css_hidden_cache_v1",
  "model_name": "bert-base-uncased",
  "transformers_version": "PINNED",
  "torch_version": "PINNED",
  "dataset_sha256": "HASH",
  "config_sha256": "HASH",
  "layers": "embedding_plus_12",
  "pooling": ["cls", "mean_non_special", "token_matrix_word_level"],
  "dtype": "float16_matrices_float32_pools",
  "created_at": "ISO_TIMESTAMP",
  "seed": 13
}
```

### 7.4 Layer metrics schema

`results/metrics/layer_metrics.parquet`:

```csv
pair_id,phenomenon,model,layer,pooling,delta_cos,sim_frob,delta_frob,delta_l2,delta_token_aligned,token_count_s,token_count_cf,length_delta,lexical_jaccard,edit_distance
```

### 7.5 Probing results schema

`results/probes/probe_results.csv`:

```csv
phenomenon,probe_name,model,layer,seed,split_type,feature_type,accuracy,macro_f1,auroc,ece,control_accuracy,control_macro_f1,selectivity,n_train,n_dev,n_test,config_sha256
```

### 7.6 Surprisal results schema

`results/surprisal/gpt2_surprisal.csv`:

```csv
pair_id,phenomenon,model,total_surprisal_s,total_surprisal_cf,avg_surprisal_s,avg_surprisal_cf,delta_total_surprisal,delta_avg_surprisal,abs_delta_avg_surprisal,key_region_surprisal_s,key_region_surprisal_cf,delta_key_region_surprisal
```

## 8. Exact model list and why each model is included

| Model | HF identifier | Why included |
|---|---|---|
| BERT base uncased | `bert-base-uncased` | Bidirectional masked LM baseline; includes CLS representation; widely used in psycholinguistic diagnostics |
| RoBERTa base | `roberta-base` | BERT-family model with optimized pretraining recipe; tests whether BERT-family conclusions are robust to pretraining changes |
| GPT-2 small | `gpt2` | Autoregressive LM; primary source for token/sentence surprisal; contrasts bidirectional encoders with left-to-right representations |

All three are 12-layer transformer models with tractable course-project compute requirements.

## 9. Exact representation extraction protocol

1. Load model/tokenizer from pinned Hugging Face identifiers.
2. Set:
   - `model.eval()`
   - `torch.no_grad()`
   - `output_hidden_states=True`
   - fixed seed
3. Extract embedding layer plus all 12 hidden layers.
4. Preserve token metadata:
   - subword tokens
   - offsets
   - special-token masks
   - word IDs where available
5. Primary unit:
   - word-level matrices, produced by mean-pooling subwords belonging to the same word.
6. Secondary unit:
   - raw subword matrices as tokenization ablation.
7. Pooling:
   - BERT/RoBERTa: CLS and mean over non-special word tokens.
   - GPT-2: mean over word tokens and last-token vector; no CLS.
8. Token matrices:
   - `H_l(s) in R^{T x d}`
   - exclude special tokens for matrix metrics.
9. Cache:
   - write pooled vectors and token matrices by model/dataset/layer.
   - store checksums for dataset, config, and model name.
10. Do not recompute hidden states during metric/probe/statistics scripts unless `--force` is passed.

## 10. Exact metrics

### 10.1 Cosine shift

```text
sim_cos_l = cos(pool_l(s), pool_l(s_cf))
Delta_cos_l = 1 - sim_cos_l
```

Primary pooling: mean over non-special word tokens. CLS is a BERT/RoBERTa ablation.

### 10.2 Frobenius/matrix-norm shift

Let `A = H_l(s)` and `B = H_l(s_cf)`, after word-level token aggregation and row-wise L2 normalization.

```text
S_cross = A_norm @ B_norm.T
S_self_A = A_norm @ A_norm.T
S_self_B = B_norm @ B_norm.T
K(M)_ij = max(0, M_ij)

sim_frob_l =
  ||K(S_cross)||_F /
  sqrt(||K(S_self_A)||_F * ||K(S_self_B)||_F + epsilon)

Delta_frob_l = 1 - sim_frob_l
```

Ablations:

- no row normalization
- no `K` clipping
- subword-level instead of word-level
- length-matched subset only

### 10.3 L2 shift

```text
Delta_l2_l = ||pool_l(s) - pool_l(s_cf)||_2
```

Use z-scored version in regressions.

### 10.4 Token-aligned shift

Build word alignment using exact token matches plus edit metadata. For aligned word pairs `(i,j)`:

```text
Delta_token_aligned_l =
  mean_{(i,j) in alignment} [1 - cos(h_l(s)_i, h_l(s_cf)_j)]
```

Report:

- all aligned tokens
- content words only
- edited/structurally implicated spans only
- unedited context only

### 10.5 Optional CKA/RSA

Use CKA/RSA only as exploratory dataset-level geometry analysis:

- CKA: compare full representation matrices across item sets/layers.
- RSA: compare model representational dissimilarity matrices with human semantic-change dissimilarity matrices.

Do not use CKA/RSA as primary per-pair metrics.

## 11. Exact probing experiments

### General probe setup

- Linear/logistic probes only for primary results.
- Features:
  - sentence mean pool
  - CLS where available
  - span vectors for relevant arguments/cues
- Splits:
  - random split
  - template split
  - lexical split
- Seeds: 5.
- Metrics:
  - accuracy
  - macro-F1
  - AUROC where binary
  - expected calibration error if feasible
  - selectivity = task score - random-label control score

### 11.1 Role probe

Task: predict whether a target noun span is agent or patient/theme.

Data:

- Include active, passive, and role-reversed sentences.
- Use target-span representation and sentence context.
- Avoid a trivial "first noun = agent" probe.

Features:

```text
[target_span_vector, other_argument_span_vector, predicate_span_vector]
```

Labels:

```text
target_role in {agent, patient}
```

Controls:

- surface-position baseline
- active-only vs active+passive comparison
- lexical split over nouns and verbs
- random target-role labels by word type/template

### 11.2 Negation probe

Task A: predict negation presence.

Task B, stretch: predict whether a target predicate is in the scope of negation.

Features:

- sentence pool
- predicate span
- cue + predicate span
- no-negator pool ablation: remove negation cue tokens from pooling

Controls:

- negation-token lexical baseline
- split by negator type
- random-label/selectivity control

### 11.3 Attachment probe

Task: predict attachment class.

Labels:

```text
attachment_class in {VP_attachment, NP_attachment}
```

Features:

```text
[head_candidate_1_span, head_candidate_2_span, pp_span, sentence_pool]
```

Controls:

- PP-head lexical split
- template split
- ambiguous vs disambiguated subset analysis
- random-label/selectivity control

## 12. Exact surprisal experiments

### 12.1 GPT-2 autoregressive surprisal: primary

Use GPT-2 token log probabilities:

```text
surprisal(t_i) = -log p(t_i | t_1 ... t_{i-1})
```

Compute:

- total sentence surprisal
- average token surprisal
- `delta_total_surprisal = total(s_cf) - total(s)`
- `delta_avg_surprisal = avg(s_cf) - avg(s)`
- `abs_delta_avg_surprisal`
- key-region surprisal:
  - role: verb and swapped arguments
  - negation: negation cue, auxiliary, main predicate, following object/complement
  - attachment: PP span and candidate heads

### 12.2 BERT/RoBERTa pseudo-log-likelihood: optional

Use PLL only as a secondary acceptability/plausibility score for masked LMs:

```text
PLL(s) = sum_i log p_MLM(w_i | s with w_i masked)
```

Report separately from GPT-2 surprisal because PLL is bidirectional and not a left-to-right processing predictor.

## 13. Human alignment experiments

### Annotation protocol

- Balanced 200-500 pairs.
- Recommended: 300 pairs, 3 annotators each.
- Annotators see randomized pair order.
- Include duplicate checks and obvious sanity checks.
- Collect:
  - semantic-change 0-5
  - confidence 1-5
  - optional fluency/plausibility 1-5
  - optional changed-words span

### Agreement

Report:

- Krippendorff's alpha or ordinal alpha
- ICC for mean ratings
- mean pairwise Spearman/Pearson
- percentage of items with rating range >= 3 as disagreement flag

### Alignment

Primary:

```text
Spearman(mean_human_change, Delta_metric_l)
```

Secondary:

```text
Pearson(mean_human_change, Delta_metric_l)
```

Run by:

- model
- layer
- phenomenon
- metric
- pooled all phenomena with phenomenon fixed effects

## 14. Salience detection

### Definition

In CSS, a span is salient if it is either:

1. directly edited, or
2. structurally implicated by the edit, and
3. its representation contributes disproportionately to the model's sentence-pair shift.

Examples:

- role reversal: agent, patient, main verb
- negation: negation cue, auxiliary, predicate scope
- attachment: PP span and competing attachment heads

### Matrix-norm salience score

For token `i` in `s`, compute row contribution:

```text
row_contrib_i = ||K(S_cross[i, :])||_2
drop_contrib_i = sim_frob_full - sim_frob_without_row_i
```

For token `j` in `s_cf`, compute column contribution analogously.

Evaluate whether gold salient spans rank highly.

### Secondary experiment

- Predict gold edit/salience spans from token contribution scores.
- Metrics: Recall@1, Recall@3, MRR, AUC.
- Compare:
  - Frobenius token contributions
  - token-aligned cosine drop
  - gradient-free leave-one-out
  - attention weights only as a weak baseline if included

## 15. Statistical analysis

### Correlations

For each model, phenomenon, layer, and metric:

```text
rho = Spearman(mean_human_change, Delta_metric_l)
```

Bootstrap 95% CIs over items, stratified by phenomenon.

### Regression

Primary mixed model over individual annotations:

```text
human_change_ij ~
  z(Delta_cos_l) +
  z(Delta_frob_l) +
  z(abs_delta_avg_surprisal) +
  z(probe_confidence_l) +
  phenomenon +
  model +
  z(length_delta) +
  z(lexical_jaccard) +
  (1 | item_id) +
  (1 | annotator_id)
```

Run separately by layer family or preselected layers to reduce multiple testing. For all-layer analyses, treat as exploratory or apply correction.

### Incremental value test for H2

Compare nested models:

```text
M_cos:    human_change ~ Delta_cos + controls
M_cos_f:  human_change ~ Delta_cos + Delta_frob + controls
```

Report:

- likelihood-ratio test if assumptions are met
- AIC/BIC
- cross-validated R² or RMSE
- standardized beta for `Delta_frob`

### Multiple comparisons

Use Benjamini-Hochberg FDR within planned families:

- correlation tests across layers for each model/phenomenon/metric
- probe tests across layers
- salience tests across phenomena

### Effect sizes

Report:

- Spearman rho and CI
- standardized beta
- ΔR²
- macro-F1 and selectivity
- layer peak and layer-center-of-mass

### Ablations

- pooling: mean vs CLS vs GPT-2 last-token
- token unit: word vs subword
- matrix norm: K on/off, normalization on/off
- length-matched subset
- lexical/template split
- model family
- phenomenon-specific analysis

## 16. Step-by-step execution order

1. **Freeze schema v1.**
   - Implement JSONL, human CSV, metrics schemas.
   - Create config files and checksum utilities.

2. **Generate pilot data.**
   - 100 role, 100 negation, 100 attachment.
   - Run automatic validation and manual spot check.

3. **Implement representation extraction.**
   - Start with BERT and GPT-2.
   - Cache all layers.
   - Verify token/word alignment.

4. **Implement metrics.**
   - Cosine, Frobenius, L2, token-aligned shift.
   - Run metrics on pilot.

5. **Run annotation pilot.**
   - 30-60 pairs, 3 annotators.
   - Check scale clarity and agreement.
   - Revise annotation instructions only before full data collection.

6. **Implement surprisal.**
   - GPT-2 total, average, and key-region surprisal.
   - Add BERT/RoBERTa PLL only after primary pipeline works.

7. **Implement probes.**
   - Linear probes for role, negation, attachment.
   - Add selectivity and lexical/template splits.

8. **Freeze configs.**
   - Commit config checksums.
   - No schema or prompt changes after this without new version.

9. **Scale data and extraction.**
   - Generate 1,500 pairs per phenomenon.
   - Run all three models.
   - Cache hidden states and metrics.

10. **Full annotation.**
    - 300-500 pairs.
    - Aggregate and compute agreement.

11. **Run final stats.**
    - Correlations, mixed models, ablations, CIs.
    - Produce tables and plots.

12. **Write workshop paper.**
    - Main text: CSS protocol, core results, controls.
    - Appendix: templates, schema, prompts, ablations.

## 17. Repository structure

```text
css-counterfactual-probing/
  AGENTS.md
  README.md
  CITATION.cff
  requirements.txt
  pyproject.toml
  configs/
    data/
      role.yaml
      negation.yaml
      attachment.yaml
    models/
      bert_base_uncased.yaml
      roberta_base.yaml
      gpt2.yaml
    experiments/
      pilot.yaml
      full.yaml
      probes.yaml
      surprisal.yaml
      stats.yaml
  data/
    raw/
    css_pairs/
      role_1500.jsonl
      neg_1500.jsonl
      attach_1500.jsonl
    annotations/
      human_css_0_5.csv
      human_css_aggregated.csv
    sts_alignment/
      sts_b_slice.csv
      str_2022_slice.csv
    lexicons/
      nouns_animacy.csv
      verbs_roles.csv
      pp_instruments_attributes.csv
  src/
    css/
      data/
        generate_role.py
        generate_negation.py
        generate_attachment.py
        validate_schema.py
        split_data.py
      representations/
        extract_hidden.py
        token_alignment.py
        pooling.py
        cache_io.py
      metrics/
        cosine.py
        matrix_norms.py
        token_shift.py
        compute_all_metrics.py
      probes/
        build_probe_dataset.py
        train_linear_probe.py
        selectivity_controls.py
      surprisal/
        gpt2_surprisal.py
        mlm_pll.py
      annotation/
        make_batches.py
        aggregate_annotations.py
        agreement.py
      stats/
        correlations.py
        mixed_effects.R
        bootstrap.py
        multiple_comparisons.py
      salience/
        token_contributions.py
        evaluate_salience.py
      plots/
        plot_layer_curves.py
        plot_ablation_tables.py
  cache/
    hidden/
    tokenized/
  results/
    metrics/
    probes/
    surprisal/
    stats/
    salience/
    figures/
    tables/
  reports/
    workshop_paper/
      paper.md
      bibliography.bib
      figures/
    appendix/
  tests/
    test_schema.py
    test_matrix_norms.py
    test_token_alignment.py
    test_surprisal.py
    test_reproducibility.py
  scripts/
    run_pilot.sh
    run_full_metrics.sh
    run_probes.sh
    run_stats.sh
```

## 18. AGENTS.md-ready task plan

See the accompanying `AGENTS.md` file. It defines agent roles, dependencies, outputs, definitions of done, coding standards, citation discipline, and reproducibility rules.

## 19. Minimum viable pilot

**Purpose:** Determine whether CSS is viable before full-scale annotation and extraction.

Scope:

- Data:
  - 100 role pairs
  - 100 negation pairs
  - 100 attachment pairs
- Models:
  - BERT base uncased
  - GPT-2 small
  - RoBERTa optional if time permits
- Metrics:
  - mean-pool cosine shift
  - Frobenius matrix shift
  - L2 shift
- Human data:
  - 60-90 annotated pairs
  - 3 annotators/item
- Surprisal:
  - GPT-2 total/average/key-region
- Probes:
  - one role probe and one negation probe with random-label controls
  - attachment probe optional

Pilot success criteria:

1. Hidden-state extraction works and is cached reproducibly.
2. Frobenius metric returns bounded similarities in `[0,1]` except flagged numerical issues.
3. Human annotation agreement is acceptable enough to proceed or the prompt is revised before freezing.
4. At least one representation metric shows interpretable layer-wise variance.
5. Surface controls can be computed for all items.

## 20. Full-scale experiment matrix

| Component | Full setting |
|---|---|
| Phenomena | role reversal, negation, attachment |
| Pair count | 1,500 per phenomenon |
| Models | BERT base uncased, RoBERTa base, GPT-2 small |
| Layers | embedding + 12 transformer layers |
| Pooling | mean, CLS where available, GPT-2 last-token optional |
| Matrix unit | word-level primary, subword-level ablation |
| Metrics | cosine, Frobenius, L2, token-aligned |
| Surprisal | GPT-2 AR primary; MLM PLL optional |
| Probes | 3 phenomenon probes x 3 models x 12 layers x 5 seeds |
| Controls | lexical split, template split, random-label, length/overlap covariates |
| Human annotation | 300-500 pairs, 3-5 annotators/item |
| Stats | Spearman/Pearson, mixed models, bootstrap CIs, FDR correction |
| Salience | secondary span-ranking experiment |

## 21. Paper outline for workshop submission

1. **Title and abstract**
2. **Introduction**
   - Minimal counterfactual edits as a controlled test of structural sensitivity.
   - Human-aligned semantic-change judgments as the evaluation target.
3. **Related work**
   - Minimal-pair LM evaluation.
   - Psycholinguistic diagnostics.
   - Representation probing and selectivity.
   - Matrix-norm similarity.
   - Surprisal as a psycholinguistic predictor.
4. **CSS protocol**
   - Data construction.
   - Model extraction.
   - Metrics.
   - Human annotation.
5. **Experiments**
   - Representation shift.
   - Probes.
   - Surprisal.
   - Human alignment.
   - Controls and ablations.
6. **Results**
   - Layer curves.
   - H1-H5 tests.
   - Phenomenon differences.
   - Matrix norm vs cosine.
7. **Salience extension**
   - Short secondary section if results are ready.
8. **Limitations**
   - Synthetic data.
   - Human judgments not processing data.
   - Attachment ambiguity.
   - Small model set.
9. **Conclusion**
   - CSS as a reproducible protocol for counterfactual structural sensitivity.
10. **Appendix**
    - Templates, schemas, annotation instructions, hyperparameters, full tables.

## 22. Risks and fallback plans

| Risk | Fallback |
|---|---|
| Human agreement is low | Revise prompt before full run; collapse 0-5 into low/medium/high; use median ratings |
| Frobenius does not outperform cosine | Report as negative result; emphasize CSS protocol and boundary conditions |
| Attachment data too noisy | Keep role and negation as primary; mark attachment as exploratory |
| Probes memorize lexical cues | Report selectivity; use lexical/template split as primary; reduce claims |
| Hidden cache too large | Store pooled vectors for all items and token matrices only for human subset; use float16 |
| GPT-2 surprisal weakly related to human scores | Present as complementary plausibility feature; do not overclaim |
| BERT/RoBERTa PLL too slow | Drop PLL; keep GPT-2 surprisal primary |
| Timeline too short | Complete MVP with 2 models, 2 phenomena, 150-300 human annotations |

## 23. Bibliography

- Abdalla, Mohamed, Krishnapriya Vishnubhotla, and Saif M. Mohammad. 2023. *What Makes Sentences Semantically Related? A Textual Relatedness Dataset and Empirical Study*. EACL.
- Barr, Dale J., Roger Levy, Christoph Scheepers, and Harry J. Tily. 2013. *Random effects structure for confirmatory hypothesis testing: Keep it maximal*. Journal of Memory and Language.
- Bates, Douglas, Martin Maechler, Ben Bolker, and Steve Walker. 2015. *Fitting Linear Mixed-Effects Models Using lme4*. Journal of Statistical Software.
- Benjamini, Yoav, and Yosef Hochberg. 1995. *Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing*. Journal of the Royal Statistical Society Series B.
- Cer, Daniel, Mona Diab, Eneko Agirre, Inigo Lopez-Gazpio, and Lucia Specia. 2017. *SemEval-2017 Task 1: Semantic Textual Similarity*. SemEval.
- Devlin, Jacob, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. 2019. *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. NAACL.
- Ettinger, Allyson. 2020. *What BERT Is Not: Lessons from a New Suite of Psycholinguistic Diagnostics for Language Models*. TACL.
- Hewitt, John, and Percy Liang. 2019. *Designing and Interpreting Probes with Control Tasks*. EMNLP-IJCNLP.
- Kornblith, Simon, Mohammad Norouzi, Honglak Lee, and Geoffrey Hinton. 2019. *Similarity of Neural Network Representations Revisited*. ICML.
- Kriegeskorte, Nikolaus, Marieke Mur, and Peter Bandettini. 2008. *Representational Similarity Analysis*. Frontiers in Systems Neuroscience.
- Lee, Eun-Kyoung Rosa, Sathvik Nair, and Naomi Feldman. 2024. *A Psycholinguistic Evaluation of Language Models' Sensitivity to Argument Roles*. Findings of EMNLP.
- Levy, Roger. 2008. *Expectation-based syntactic comprehension*. Cognition.
- Liu, Yinhan, et al. 2019. *RoBERTa: A Robustly Optimized BERT Pretraining Approach*. arXiv.
- Radford, Alec, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, and Ilya Sutskever. 2019. *Language Models are Unsupervised Multitask Learners*. OpenAI.
- Salazar, Julian, Davis Liang, Toan Q. Nguyen, and Katrin Kirchhoff. 2020. *Masked Language Model Scoring*. ACL.
- vor der Brück, Tim, and Marc Pouly. 2019. *Text Similarity Estimation Based on Word Embeddings and Matrix Norms for Targeted Marketing*. NAACL.
- Wang, Alex, Amanpreet Singh, Julian Michael, Felix Hill, Omer Levy, and Samuel R. Bowman. 2018/2019. *GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding*.
- Warstadt, Alex, et al. 2020. *BLiMP: The Benchmark of Linguistic Minimal Pairs for English*. TACL.
