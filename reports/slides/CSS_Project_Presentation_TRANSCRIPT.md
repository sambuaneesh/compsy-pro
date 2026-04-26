# CSS Project Presentation Transcript (Detailed Concept Version)

This document is a **presenter script** for `CSS_Project_Presentation.tex`.
It is intentionally detailed so you can present from first principles, not just read slide bullets.

How to use this script:
- For each slide, start with **Core message**.
- Use **Concept explanation** to teach the idea clearly.
- Use **Figure reading** on plot slides to narrate what viewers should look at.
- Use **Reviewer defense** lines when challenged.

---

## Slide 1: Title

### Core message
We are presenting a controlled representational analysis project: **Counterfactual Structural Sensitivity (CSS)**.

### Concept explanation (say this clearly)
The project is about checking what changes **inside** a language model when we make minimal edits to a sentence.  
We are not asking “does the model output the right final answer?” alone.  
We are asking: when meaning changes structurally, does internal geometry move in a meaningful and measurable way?

### Speaking script
“Our project is Counterfactual Structural Sensitivity, or CSS. We use sentence pairs where one sentence is minimally edited into a counterfactual form. Then, layer by layer, we measure representation shifts. The core framing is representational diagnostics under controlled edits.”

### Reviewer defense
“Our claims are bounded to representation-level evidence and statistical consistency. We do not overclaim cognitive equivalence with humans in this run.”

---

## Slide 2: Roadmap

### Core message
The talk is structured as a rigorous chain: motivation -> protocol -> setup -> results -> claim boundary.

### Concept explanation
Many reviewer objections come from “results-first storytelling.”  
This slide prevents that by showing method and statistical gates before interpretations.

### Speaking script
“I’ll first define the linguistic problem, then the CSS protocol and metrics, then the experimental setup, then the RQ-based results, and finally what we can and cannot claim.”

### Reviewer defense
“This order reduces post-hoc narrative bias because each claim is attached to predeclared analysis objectives.”

---

## Slide 3: Motivation

### Core message
Minimal edits can produce major semantic changes even when lexical overlap is high.

### Concept explanation
Two phenomena:
- **Role reversal**: same words, different who-did-what-to-whom.
- **Negation**: proposition polarity flips with minimal surface edit.

Example:
- “The chef praised the waiter.”
- “The waiter praised the chef.”

Lexical bag is nearly unchanged, but event semantics is inverted.

### Speaking script
“This motivates CSS. If representations encode structure, then these minimal edits should induce reliable internal shifts. If representations are mostly surface-driven, we expect weak, unstable, or inconsistent movement.”

### Reviewer defense
“Counterfactual minimal pairs control lexical confounds better than unconstrained sentence pairs.”

---

## Slide 4: Research Questions

### Core message
RQ1 checks consistency, RQ2 checks incremental utility of Frobenius, RQ3 checks relation between probes and shift-surprisal diagnostics.

### Concept explanation
- **RQ1 (robustness)**: do shift metrics respond consistently across models/layers?
- **RQ2 (incremental value)**: does Frobenius add information after cosine is already included?
- **RQ3 (diagnostic relation)**: are probe selectivity and metric-surprisal alignment the same thing or complementary?

### Speaking script
“These RQs are deliberately orthogonal: sensitivity existence, additional value, and diagnostic interaction.”

### Reviewer defense
“Each RQ has a dedicated result artifact and explicit statistics, not qualitative interpretation only.”

---

## Slide 5: CSS Protocol

### Core message
Pipeline: sentence pair -> hidden states -> shift metrics -> probes + surprisal -> statistical summary.

### Concept explanation
Let original sentence be \(s\), counterfactual be \(s_{cf}\).  
For each model and each layer \(l\), extract hidden states \(h_l(s)\) and \(h_l(s_{cf})\).  
Compute multiple shifts from these states.  
Then run:
- probing diagnostics,
- surprisal diagnostics,
- statistical tests and corrections.

Why layer-wise:
Different layers encode different abstractions. If we collapse early, we lose that structure.

### Speaking script
“The key design choice is to keep analysis pairwise and layer-indexed from start to finish. We do not flatten early to one score per model.”

### Reviewer defense
“All steps are config-driven and reproducible, so each result row can be traced back to data hash, config hash, model, seed, and code path.”

---

## Slide 6: Data Source and Scale

### Core message
Dataset-only track with a public source and 3000 total pairs.

### Concept explanation
We use only:
- role reversal pairs (1500),
- negation pairs (1500),
from the public psycholinguistic source repository.

This preserves transparency and reproducibility.

### Figure reading (how it looks)
- **Left panel**: two bars of equal height (1500 each), confirming balanced phenomenon counts.
- **Right panel**: grouped bars by split (`train`, `dev`, `test`) and phenomenon.
  - Negation: train 1049, dev 234, test 217.
  - Role reversal: train 1045, dev 261, test 194.

### Interpretation
Balanced phenomenon counts reduce class-skew bias in aggregate comparisons.  
Split-level mismatch is minor and explicitly visible.

### Speaking script
“The dataset is balanced by phenomenon, and split composition is transparent. This improves fairness of cross-phenomenon comparisons.”

### Reviewer defense
“Public-source data makes the pipeline independently auditable.”

---

## Slide 7: Modeling Setup

### Core message
Three fixed model families: BERT, RoBERTa, GPT-2; all layers analyzed.

### Concept explanation
- **BERT-base**: bidirectional masked-LM encoder.
- **RoBERTa-base**: stronger BERT-family training recipe.
- **GPT-2**: autoregressive LM, also used for surprisal.

Layer extraction:
- Layer 0 (embedding) + layers 1..12.

Representation units:
- sentence pooled vectors (primary),
- token matrices (primary),
- CLS / last-token (secondary ablations).

### Speaking script
“This gives architecture diversity while keeping compute reproducible and controlled.”

### Reviewer defense
“The objective is representational mechanism testing, not leaderboard chasing with large opaque models.”

---

## Slide 8: Metric Intuition (What each metric means)

### Core message
Each metric captures a different type of representational movement.

### Concept explanation with intuition
- **\(\Delta_{cos}\)**: directional change between pooled vectors.
  - If two vectors point similarly, cosine shift is small.
  - Think: “semantic direction changed or not?”
- **\(\Delta_{frob}\)**: change in token-level interaction geometry.
  - Operates on token matrices, not only centroids.
  - Think: “did relational structure inside the sentence representation change?”
- **\(\Delta_{L2}\)**: absolute displacement magnitude.
  - Think: “how far did we move in vector space?”
- **\(\Delta_{token}\)**: average local token perturbation after alignment.
  - Think: “how much local token representations changed at corresponding positions?”

### Why all four are needed
One metric can miss effects another captures.  
Example: two vectors may keep direction (small cosine shift) but move far in magnitude (large L2), or token relations may change even when pooled vectors look similar.

### Reviewer defense
“Using multiple metrics avoids single-view overfitting of interpretation.”

---

## Slide 9: Metric Definitions (math slide)

### Core message
Formal definitions make claims testable and non-ambiguous.

### Concept explanation line by line
1. \[
\Delta_{\cos}^{(l)} = 1 - \cos(\mu_l(s), \mu_l(s_{cf}))
\]
\(\mu_l(\cdot)\) is mean-pooled sentence representation at layer \(l\).  
Range intuition: closer to 0 means very similar direction; larger means stronger directional change.

2. Frobenius similarity and shift:
\[
\text{sim}_{frob}^{(l)} = \frac{\|K(\hat A_l,\hat B_l)\|_F}
{\sqrt{\|K(\hat A_l,\hat A_l)\|_F\|K(\hat B_l,\hat B_l)\|_F+\epsilon}},
\quad
\Delta_{frob}^{(l)} = 1-\text{sim}_{frob}^{(l)}
\]
Here \(A_l,B_l\) are normalized token matrices for \(s,s_{cf}\).  
\(\|\cdot\|_F\) measures matrix energy.  
Intuition: compares relational token geometry, not just one averaged vector.

3. \[
\Delta_{L2}^{(l)}=\|\mu_l(s)-\mu_l(s_{cf})\|_2
\]
Pure Euclidean movement magnitude.

4. \[
\Delta_{token}^{(l)}=\frac{1}{|M|}\sum_{(i,j)\in M}\left(1-\cos(h_i^{(l)},h_{j,cf}^{(l)})\right)
\]
\(M\) is alignment map of corresponding positions/spans.

### Speaking script
“This slide is where we convert intuition into computable definitions. It also prevents ambiguity about what exactly is being measured.”

### Reviewer defense
“Frobenius is framed as an adaptation to contextual token matrices, not as a direct copy of static embedding document scoring.”

---

## Slide 10: Probes and Controls

### Core message
We evaluate recoverability of linguistic signals with linear probes, but use selectivity controls to avoid overclaiming.

### Concept explanation
Probe tasks:
- Role: agent vs patient.
- Negation: negation presence.

Danger with probes:
High probe score can come from memorization, spurious lexical cues, or probe capacity.

Control solution:
\[
\text{Selectivity}=\text{Task Macro-F1}-\text{Random-label Macro-F1}
\]
If selectivity is high, there is real task signal beyond trivial fitting.

Multi-seed evaluation:
Shows stability and avoids single-seed luck.

### Speaking script
“Probe accuracy alone is not enough; selectivity is our anti-memorization control.”

### Reviewer defense
“This directly follows the critique in Hewitt & Liang, so we are not using naive probe methodology.”

---

## Slide 11: Surprisal Signal

### Core message
Surprisal provides a probabilistic processing signal from GPT-2.

### Concept explanation
\[
\text{surprisal}(t_i)=-\log P(t_i|t_1,\dots,t_{i-1})
\]
Interpretation:
- low probability token -> high surprisal,
- high probability token -> low surprisal.

Derived sentence features:
- total surprisal,
- average surprisal,
- absolute delta between original and counterfactual.

Why this complements representation shift:
Shift metrics measure geometry movement; surprisal measures predictive expectation.

### Speaking script
“Surprisal is not a replacement for representation shift. It is a complementary signal about prediction difficulty.”

### Reviewer defense
“Primary surprisal remains autoregressive GPT-2, avoiding construct mixing with bidirectional pseudo-likelihood.”

---

## Slide 12: Statistical Objectives

### Core message
We predefine objective families and inferential controls.

### Concept explanation
- **D1**: correlation between shift metrics and surprisal by layer/model/phenomenon.
- **D2**: incremental regression gain from adding \(\Delta_{frob}\) to cosine baseline.
- **D3**: layer-profile differences.
- **D4**: selectivity stability.

Regression form:
\[
z(y)\sim z(\Delta_{cos})+z(\Delta_{frob})+z(length)+z(overlap)
\]
Standardizing variables improves coefficient comparability.

Inference controls:
- bootstrap CIs for uncertainty,
- BH-FDR correction for multiple comparisons across cells/layers.

### Speaking script
“Without correction, layer-wise analysis can inflate false positives. So we control multiplicity explicitly.”

### Reviewer defense
“This statistical discipline is a core reason our claims are robust.”

---

## Slide 13: Experiment Matrix and Coverage

### Core message
Coverage is full and systematic, not selective.

### Concept explanation
Counts:
- 3000 pairs,
- 3 models,
- 13 layers,
- 4 metrics,
- 117000 metric rows,
- 3000 surprisal rows,
- 390 probe rows.

Why this matters:
Results come from broad combinatorial coverage, reducing risk of cherry-picked snapshots.

### Speaking script
“This table demonstrates execution completeness for the dataset-only scope.”

---

## Slide 14: Mean Shift Magnitude by Phenomenon

### Core message
Negation induces larger average representation shifts than role reversal, but scale handling matters.

### Figure reading (what it looks like)
Three panels:
- Left: grouped bars for \(\Delta_{cos}, \Delta_{frob}, \Delta_{token}\) raw means.
- Middle: single grouped bar for \(\Delta_{L2}\) raw means (separate scale).
- Right: normalized bars (each metric scaled within itself) for fair visual comparison.

Color coding:
- Negation bars are consistently taller than role reversal across panels.

### Exact values to mention
- Negation means:
  - \(\Delta_{cos}=0.0478\)
  - \(\Delta_{frob}=0.0584\)
  - \(\Delta_{L2}=27.8753\)
  - \(\Delta_{token}=0.0502\)
- Role reversal means:
  - \(\Delta_{cos}=0.0124\)
  - \(\Delta_{frob}=0.0197\)
  - \(\Delta_{L2}=4.1960\)
  - \(\Delta_{token}=0.0408\)

### Interpretation
Negation often inserts explicit polarity cues (e.g., “not”), creating broad movement across embedding geometry.  
Role reversal can still be semantically major while requiring subtler redistribution of relational structure.

### Important nuance (say this)
“Larger mean shift does not automatically imply stronger coupling with surprisal or better diagnostic utility. We test those separately in later slides.”

### Reviewer defense
“Separating L2 scale and normalized view prevents visual misinterpretation from metric unit differences.”

---

## Slide 15: Qualitative Audit: Why the Patterns Differ

### Core message
The qualitative audit explains why the mean-shift slide and the correlation slides can point in different directions.

### Concept explanation
Slide 14 was a pooled magnitude summary: it asked “how large is the average representational movement?”  
The next correlation slides ask a different question: “do pair-level shifts rank together with GPT-2 surprisal deltas?”

Those are not the same statistic. A phenomenon can have large average movement but weak item-level ordering, or smaller average movement but cleaner rank alignment.

### Table reading
The table compares surface properties:
- Negation lexical Jaccard is lower: 0.4853.
- Role reversal lexical Jaccard is higher: 0.7973.
- Negation average length delta is about one token.
- Role reversal average length delta is almost zero.
- Negation mean Frobenius shift is larger: 0.0584 vs 0.0197.

### Interpretation
Negation pairs often do more than insert `not`; many also change the predicate or category foil. So negation creates broad surface and semantic movement.  
Role reversal preserves much more lexical content and sentence length, so it can have smaller mean magnitude while still creating a strong event-structure change.

### Reviewer defense
“This slide directly addresses the possible objection that Slide 14 and the layer-wise correlation plots contradict each other. They do not: they answer different statistical questions.”

---

## Slide 16: Qualitative Case Studies

### Core message
Actual sentence pairs show why representation geometry and surprisal are complementary diagnostics.

### Figure/table reading
This slide shows two dissociation examples:
- High Frobenius / low surprisal negation.
- Low Frobenius / high surprisal role reversal.

### Example 1 interpretation
“A hammer is an instrument” -> “A hammer is not a dessert” has high Frobenius shift but almost zero average surprisal delta.  
This means hidden geometry moves strongly, likely because the semantic category relation changes, but the average GPT-2 predictive difficulty does not change much.

### Example 2 interpretation
“The cashier counted which bills the robber had given” -> “The cashier counted which robber the bills had given” has low average Frobenius shift but high surprisal delta.  
This means GPT-2 finds the counterfactual probabilistically surprising, but the averaged representation geometry does not move as strongly.

### Takeaway
This is the qualitative reason for using multiple diagnostics. CSS should not collapse to only surprisal, only cosine, or only Frobenius.

### Reviewer defense
“These are not cherry-picked claims; they are selected from reproducible high/low quantile buckets generated from the full result tables.”

---

## Slide 17: Layer-Wise Correlation Curves

### Core message
Correlation patterns are strongly phenomenon-dependent and layer-structured.

### Figure reading (what it looks like)
Six panels: top row negation (BERT/GPT-2/RoBERTa), bottom row role reversal (same model order).  
Two lines in each panel:
- blue = \(\Delta_{cos}\),
- orange = \(\Delta_{frob}\).

X-axis: layer 0..12.  
Y-axis: Spearman rho with surprisal delta.

### What to point out
- Bottom row (role reversal): curves are clearly positive and relatively high (~0.2 to ~0.37).
- Top row (negation): curves are weak/mixed, near zero and sometimes negative.
- In several panels orange slightly exceeds blue, hinting Frobenius advantage in some regions.

### Interpretation
Role reversal yields a stronger monotonic relation between representation shift and surprisal than negation does.  
This suggests phenomenon-specific representational dynamics rather than one universal behavior.

### Reviewer defense
“We show per-phenomenon panels specifically to avoid averaging away opposite trends.”

---

## Slide 18: Frobenius Heatmap Across Layers

### Core message
Frobenius behavior is detailed by model/layer/phenomenon with significance overlay.

### Figure reading (what it looks like)
Two side-by-side heatmaps:
- Left = role reversal.
- Right = negation.

Rows = models (BERT, GPT-2, RoBERTa).  
Columns = layers 0..12.  
Color map centered at 0:
- warm colors = positive correlation,
- cool colors = negative correlation.

Black dots on cells indicate FDR-significant rho.

### What to emphasize
- Role reversal map is mostly warm with many dots: broad significant positive alignment.
- Negation map has mixed warm/cool regions and fewer clustered positives.

### Interpretation
Frobenius is especially informative for role reversal and conditionally informative for negation.

### Reviewer defense
“Significance markers prevent color-only claims and keep effect-size and inferential validity tied together.”

---

## Slide 19: Probe Selectivity Across Layers

### Core message
Probe selectivity is positive and stable across models/layers/phenomena.

### Figure reading (what it looks like)
Three panels by model (BERT, GPT-2, RoBERTa).  
Each panel has two lines:
- negation,
- role reversal,
with shaded 95% seed-level intervals.

Y-axis range is narrow around ~0.44 to ~0.57, which visually highlights stability.

### Exact numbers
- Overall mean selectivity: **0.5096**.
- By model:
  - BERT: 0.5078
  - GPT-2: 0.5112
  - RoBERTa: 0.5099
- By phenomenon:
  - Negation: 0.5102
  - Role reversal: 0.5090

### Interpretation
Selectivity is consistently positive and tightly clustered, supporting genuine recoverable signal with control-adjusted robustness.

### Reviewer defense
“We show uncertainty ribbons and multi-seed variation explicitly; this is not single-seed reporting.”

---

## Slide 20: Frobenius Shift vs Surprisal Delta

### Core message
Association between Frobenius shift and surprisal delta differs sharply by phenomenon.

### Figure reading (what it looks like)
Two hexbin panels:
- Left = role reversal.
- Right = negation.

Axes:
- X = mean \(\Delta_{frob}\),
- Y = \(|\Delta\) average surprisal\(|\).

Hexagon shading indicates point density (darker = more pairs).  
Red regression line shown per panel.

### What to point out
- Role reversal: visibly positive slope.
- Negation: near-flat slope.

### Supporting statistics
- Role reversal:
  - Pearson ~0.3599
  - Spearman ~0.3400
- Negation:
  - Pearson ~0.0474
  - Spearman ~-0.0169

### Interpretation
Frobenius-shift and surprisal relationship is strong for role reversal, weak for negation.  
This indicates heterogeneity: not all structural edit types map to surprisal in the same way.

### Reviewer defense
“Hexbin avoids overplotting artifacts that standard scatter would introduce for dense pair clouds.”

---

## Slide 21: Incremental Value of Frobenius

### Core message
Adding Frobenius to cosine baseline improves explanatory performance in most cells.

### Figure reading (what it looks like)
Histogram of \(\Delta\) adjusted-\(R^2\) across 78 cells:
- dashed vertical line at 0 (no incremental gain),
- most bars lie right of 0,
- KDE curve overlays distribution.

Summary box on the plot:
- positive cells: **70/78**
- mean gain: **0.0114**
- median gain: **0.0069**

### Interpretation
Frobenius gives **consistent but moderate** incremental value.  
Claim is complementarity, not replacement of cosine.

### Reviewer defense
“We report full distribution and effect size, not just a binary positive-count claim.”

---

## Slide 22: RQ1 Answer (Structural Sensitivity Consistency)

### Core message
Cosine, Frobenius, and L2 show broad positive significant sensitivity; token-aligned is mixed.

### Figure reading (what it looks like)
Stacked bars by metric:
- teal = positive significant fraction,
- orange = negative significant fraction,
FDR < 0.05.

Labels above bars show +count/-count.

### Exact counts
- \(\Delta_{cos}\): +50 / -6
- \(\Delta_{frob}\): +52 / -6
- \(\Delta_{L2}\): +47 / -5
- \(\Delta_{token}\): +32 / -32

### Interpretation
Global metrics show robust directional sensitivity.  
Token-aligned metric is balanced positive/negative, indicating local perturbation behavior is more context-sensitive and not always aligned with global trends.

### Reviewer defense
“The mixed token-aligned result is explicitly reported; we do not suppress inconvenient diagnostics.”

---

## Slide 23: RQ2 Answer (Frobenius Complementarity)

### Core message
Frobenius complementarity is widespread across model-phenomenon groups.

### Figure reading (what it looks like)
Two heatmaps:
- Left heatmap: positive-rate of \(\Delta\)adj-\(R^2 > 0\).
- Right heatmap: mean \(\Delta\)adj-\(R^2\).

Rows = models, columns = phenomena.

### Values to state
Overall:
- positive cells: **70/78**
- mean gain: **0.0114**
- FDR-significant Frobenius coefficient cells: **54/78**

By group (mean gain):
- Negation/BERT: 0.008
- Negation/GPT-2: 0.006
- Negation/RoBERTa: 0.018
- Role/BERT: 0.006
- Role/GPT-2: 0.018
- Role/RoBERTa: 0.012

Positive-rate highlights:
- GPT-2 role reversal: 1.00
- RoBERTa role reversal: 1.00

### Interpretation
Frobenius adds value across most settings and is especially consistent in role reversal groups.

### Reviewer defense
“We show both sign robustness and magnitude. Either metric alone can be misleading.”

---

## Slide 24: RQ3 Answer (Probe vs Metric-Correlation Coupling)

### Core message
Probe selectivity is strong, but coupling to metric-surprisal rho is weak.

### Figure reading (what it looks like)
Grouped bars by metric for Spearman and Pearson coupling values with vertical bootstrap CI bars.
Horizontal zero-line helps see direction.

### Values
Point estimates:
- \(\Delta_{cos}\): Spearman -0.0523, Pearson -0.0483
- \(\Delta_{frob}\): Spearman -0.0112, Pearson 0.0126
- \(\Delta_{L2}\): Spearman -0.0345, Pearson -0.0384
- \(\Delta_{token}\): Spearman 0.0421, Pearson 0.1126

Bootstrap 95% CIs generally include zero.

### Interpretation
High selectivity does not necessarily imply strong metric-surprisal correlation.  
These diagnostics capture related but distinct aspects of model behavior.

### Reviewer defense
“We explicitly treat this as partial evidence and avoid overinterpreting near-zero correlations.”

---

## Slide 25: Research Questions Final Answers

### Core message
Concise conclusion table tied directly to RQ definitions.

### Speaking script
“RQ1: yes, robust sensitivity for cosine/Frobenius/L2.  
RQ2: yes, Frobenius adds incremental value in most cells.  
RQ3: partial, probes are strong but coupling is weak, so diagnostics are complementary.”

### Reviewer defense
“This summary is evidence-linked; each line is backed by prior plots/tables in the deck.”

---

## Slide 26: Key Quantitative Summary

### Core message
Single-slide numeric audit of project outcomes.

### Numbers to state clearly
- Significant positive cells (\(\Delta_{cos}\)+\(\Delta_{frob}\)): **102**
- Positive incremental cells for Frobenius: **70**
- Mean incremental gain: **0.0114**
- Mean probe selectivity: **0.5096**
- Frobenius metric warnings: **0**

### Interpretation
The pipeline is both statistically productive and numerically stable.

### Reviewer defense
“Combining inferential counts, effect sizes, and QA status gives a complete reliability snapshot.”

---

## Slide 27: Claim Boundary and Validity

### Core message
Strong claims inside scope, explicit non-claims outside scope.

### Concept explanation
Supported:
- dataset-level representational sensitivity diagnostics.

Not claimed:
- direct human cognition equivalence in this dataset-only run.

Why this improves quality:
Scientific strength is not maximum ambition; it is accurate claim-scope matching.

### Speaking script
“This boundary is deliberate and protects validity. We claim exactly what the evidence supports.”

### Reviewer defense
“Boundary precision is a strength, not a weakness.”

---

## Slide 28: Remaining Work

### Core message
Core experiments are done; remaining work is synthesis and packaging.

### Speaking script
“Remaining steps are manuscript polish, final curation of D1-D4 result tables, and submission/presentation packaging.”

### Interpretation
No fundamental pipeline gap is pending for this scope.

---

## Regular-Paper Extension Slides: Output Consistency and Modern Decoder CSS

### Core message
The project now has modern decoder extensions and a direct output-level consistency diagnostic.

### Speaking script
“For the regular-paper version, we added two modern instruction decoders: Mistral-7B-Instruct-v0.3 and Gemma-3-4B-IT. This matters because BERT, RoBERTa, and GPT-2 are scientifically useful baselines, but a 2026 logical-reasoning workshop will expect evidence on current decoder-style LLMs. We use these models in two ways: first as behavioral forced-choice models, and second as hidden-state CSS models.”

“In the output consistency slide, the identity control is the sanity check. We give the model two identical sentences and expect ‘yes’. Mistral gets 100 percent identity accuracy for both phenomena. Gemma gets 99.9 percent for role reversal and 100 percent for negation. So the prompt format is working for instruction models. GPT-2 fails identity controls because it has a strong ‘no’ bias in this forced-choice setup, so we do not overinterpret GPT-2’s high counterfactual rejection.”

“For Mistral, counterfactual rejection is 73.4 percent for role reversal and 65.2 percent for negation. For Gemma, the corresponding numbers are 96.9 percent and 81.4 percent. This comparison is useful: Gemma is much stronger, especially on role reversal, but negation is still not solved. So the behavioral extension is not just saying modern models fail; it shows model-dependent sensitivity under the same controlled edit protocol.”

“In the modern decoder representation slide, we show that the hidden-state CSS pipeline also runs on current decoders. Mistral contributes 99,000 rows: 3,000 pairs times 33 layers. Gemma contributes 105,000 rows: 3,000 pairs times 35 layers. Both runs have zero Frobenius warnings. For both models, negation has larger pooled cosine, Frobenius, and L2 shifts, while role reversal has larger token-aligned shift. That means global sentence geometry moves more for negation, but token-local correspondences are more disrupted for role reversal.”

“The strongest role-reversal Frobenius-surprisal alignment is very similar across the two modern decoders: Mistral peaks at layer 6 with rho 0.3244, and Gemma also peaks at layer 6 with rho 0.3190. That is useful evidence because it says the role-reversal pattern is not just a BERT/RoBERTa/GPT-2 artifact. Negation remains more early-layer and lexically driven, which is consistent with the qualitative audit showing that negation examples often combine polarity cues with predicate or category changes.”

### Reviewer defense
“This extension addresses two likely reviewer objections: the original model suite was older, and the original results were only representational. Mistral and Gemma add modern decoders and output-level behavior measures, while the hidden-state results show that CSS is not limited to encoder-style baselines.”

---

## Slide 31: Conclusion

### Core message
Project completion for dataset-only CSS scope is achieved with consistent evidence.

### Speaking script
“We completed the full CSS pipeline on role reversal and negation across BERT, RoBERTa, and GPT-2 over all layers and four primary metrics. The central result is that Frobenius shift provides measurable complementary signal beyond cosine in most settings.”

### Closing line
“So this project contributes a reproducible and statistically grounded structural-sensitivity diagnostic framework.”

---

## Slide 32: References

### Core message
Methodological components are grounded in standard literature.

### Speaking script
“These references cover model foundations, probing caveats, surprisal theory, matrix-norm motivation, and dataset source. They define the methodological lineage of the whole pipeline.”

### Reviewer defense
“Every core method element in our pipeline has an explicit citation anchor.”

---

## Expanded Concept Notes (for difficult questions)

### 1. Why can negation have larger mean shifts but weaker correlation with surprisal?
Because **mean shift magnitude** and **correlation with surprisal deltas** are different statistics.  
Negation may cause broad representation movement from polarity cues, but that movement may not scale monotonically with surprisal differences across items.  
Role reversal may create more orderly ranking behavior relative to surprisal, producing stronger rho despite smaller average shift.

### 2. Why use Spearman as primary correlation?
Spearman tests monotonic rank association and is robust to nonlinear scaling and heavy tails.  
Pearson is reported as secondary for linear sensitivity check.

### 3. Why not use only one “best” metric?
Different metrics capture different geometry:
- direction (\(\Delta_{cos}\)),
- magnitude (\(\Delta_{L2}\)),
- relational token structure (\(\Delta_{frob}\)),
- local perturbation (\(\Delta_{token}\)).
Single-metric reporting would undercharacterize representation dynamics.

### 4. What exactly does “incremental value” mean here?
We fit a baseline model with cosine and controls, then add Frobenius.  
\(\Delta\) adjusted-\(R^2\) > 0 means explanatory improvement after complexity penalty.  
So positive rate 70/78 means this improvement generalizes across most model-layer-phenomenon cells.

### 5. Why linear probes?
Linear probes keep interpretation cleaner: if a simple decoder can recover the signal, representation likely encodes it explicitly enough for linear readout.  
High-capacity nonlinear probes can blur representation-vs-probe-capacity attribution.

### 6. Why not claim human alignment in this final deck?
Because this run does not include fresh human annotation as a primary evidence source.  
Claim discipline keeps the project scientifically defensible in review.

### 7. How to answer “Why only base models?”
Base models provide architecture diversity and reproducible compute budget with established literature baselines.  
For the regular-paper version, we also add Mistral-7B-Instruct-v0.3 and Gemma-3-4B-IT, so the project is no longer limited to only older base models.

### 8. If asked whether Frobenius “wins” cosine
Do not say “wins.” Say:
“Frobenius is complementary. It adds consistent incremental signal over cosine in most cells, with moderate effect size.”

### 9. If asked about token-aligned mixed behavior
Say:
“Token-local sensitivity is inherently context-dependent and can diverge from global sentence-level geometry; that is why we keep it as a complementary diagnostic rather than sole criterion.”

### 10. If asked about reproducibility
Say:
“All stages are script-generated, config-driven, and hash/seed traceable; figures are generated from tables, not manually edited.”

---

## Fast 30-Second Summary (backup close)

“We built a reproducible CSS pipeline to test representational sensitivity under minimal counterfactual edits. Across 3000 pairs, 3 models, 13 layers, and 4 metrics, we find robust structural sensitivity for cosine/Frobenius/L2, broad incremental value of Frobenius over cosine (70/78 cells), strong and stable probe selectivity (~0.51), and weak coupling between probe selectivity and metric-surprisal correlation. Claims are intentionally bounded to dataset-level representational diagnostics.”

## Fast 30-Second Summary With Regular-Paper Extension

“We built CSS as a reproducible diagnostic for minimal role-reversal and negation edits. The baseline study covers 3000 pairs, BERT, RoBERTa, GPT-2, all layers, four shift metrics, probes, surprisal, qualitative analysis, and salience. For the regular-paper extension, we add Mistral-7B-Instruct-v0.3 and Gemma-3-4B-IT. Mistral gets perfect identity-control accuracy but only 73.4 percent role-reversal rejection and 65.2 percent negation rejection. Gemma is stronger, with 96.9 percent role-reversal rejection and 81.4 percent negation rejection, but still not perfect. We also compute modern-decoder hidden-state CSS across 99,000 Mistral rows and 105,000 Gemma rows, with Frobenius still adding complementary value beyond cosine.”
