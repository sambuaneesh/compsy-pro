# CSS Project Presentation Transcript

This transcript is aligned to `CSS_Project_Presentation.tex` slide order.
Use it as a speaking script during presentation and Q&A.

## Slide 1: Title

Script:
Today we present **Counterfactual Structural Sensitivity (CSS)**, a controlled framework for testing how language-model representations respond to minimal linguistic edits. The core question is not whether models are human-like, but whether internal representation shifts are systematic and interpretable under structural counterfactuals.

Reviewer defense:
This framing is intentionally conservative. We are making representation-level claims with reproducible diagnostics, not broad cognitive claims.

## Slide 2: Roadmap

Script:
The talk flows in five steps: motivation, protocol and metrics, setup, results by research question, and claim boundary. This structure is deliberate: each major claim appears only after we show the exact measurement and statistical gate used to support it.

Reviewer defense:
We separate method from result to reduce post-hoc interpretation risk.

## Slide 3: Motivation

Script:
This slide defines the core linguistic pressure test: tiny edits can alter event structure while keeping most words the same. The table shows two archetypes:
- Role reversal: same lexical items, swapped semantic roles.
- Negation: same proposition skeleton, polarity changed.

Why this matters:
If representation shifts are meaningful, these minimal edits should create measurable internal movement. If models are mostly surface-driven, shifts may be weak, noisy, or inconsistent across layers.

Reviewer defense:
The pair design controls lexical overlap and isolates structural perturbation better than unconstrained sentence comparisons.

## Slide 4: Research Questions

Script:
RQ1 asks whether representation-shift metrics consistently react to structural edits.
RQ2 asks whether Frobenius/matrix-norm shift adds information beyond centroid cosine.
RQ3 asks whether probe selectivity and shift-surprisal correlation capture the same signal or complementary signals.

Why these three:
They partition the project into robustness (RQ1), incremental utility (RQ2), and diagnostic interaction (RQ3).

Reviewer defense:
Each RQ has a dedicated quantitative output and significance gate. No claim is based on visual inspection alone.

## Slide 5: CSS Protocol

Script:
This equation-style pipeline is the full protocol:
sentence pair -> layer-wise hidden states -> shift metrics -> probes and surprisal -> statistics.
The important point is that all analysis remains pairwise and layer-indexed. We do not collapse prematurely to a single model score.

Why this design:
It preserves where effects happen, not just whether they happen. Layer locality is essential for interpretability and for checking phenomenon-specific behavior.

Reviewer defense:
The protocol is config-driven and reproducible; every artifact is traceable to model, seed, hashes, and script path.

## Slide 6: Data Source and Scale

Script:
We use a public psycholinguistic dataset source with exactly two primary phenomena: role reversal and negation, totaling **3000 counterfactual pairs**.  
In the figure:
- Left panel shows balanced totals: 1500 negation, 1500 role reversal.
- Right panel shows split composition:
  - Negation: train 1049, dev 234, test 217
  - Role reversal: train 1045, dev 261, test 194

What this means:
The dataset is balanced by phenomenon, with slight split-level asymmetry that is small and visible, not hidden.

Reviewer defense:
Using a public source improves auditability and avoids introducing unverifiable custom data artifacts.

## Slide 7: Modeling Setup

Script:
We intentionally use three canonical model families:
- BERT-base (bidirectional encoder baseline),
- RoBERTa-base (optimized BERT-family baseline),
- GPT-2 (autoregressive baseline, also used for surprisal).

For each model we extract hidden states from layer 0 through 12 and evaluate both pooled sentence vectors and token-level matrices. CLS and GPT-2 last-token vectors are included as secondary ablations, not primary claims.

Why this is defensible:
These models are stable, widely understood, and still strong enough to test representational diagnostics without confounding from very large proprietary architectures.

## Slide 8: Metric Intuition

Script:
This slide gives the conceptual role of each metric:
- Delta_cos: directional shift.
- Delta_frob: relational geometry shift across token matrices.
- Delta_L2: absolute displacement magnitude.
- Delta_token: local aligned token perturbation.

Why multiple metrics:
A single metric can be blind to important change types. Direction, magnitude, and token-structure geometry are different views of sensitivity.

Reviewer defense:
We do not cherry-pick one metric. We report all four and expose disagreement when it exists.

## Slide 9: Metric Definitions

Script:
Here we formalize each metric at layer \(l\).  
Delta_cos and Delta_L2 are sentence-level pooled-vector distances.  
Delta_frob is a matrix-norm similarity adaptation over normalized token matrices, then converted to shift by \(1-\text{sim}\).  
Delta_token is average aligned token cosine shift.

Why Frobenius is introduced:
Centroid cosine compresses token structure into one vector. Frobenius preserves pairwise token interaction structure through matrix geometry.

Reviewer defense:
We explicitly frame Frobenius as an adaptation for contextual token matrices, not a claim of identical semantics to older static-word settings.

## Slide 10: Probes and Controls

Script:
Probes are linear, layer-wise, and phenomenon-specific (role and negation).  
The critical control is random-label selectivity:
\[
\text{selectivity} = \text{task F1} - \text{control F1}
\]
This directly follows probe-selectivity caution from Hewitt and Liang.

Why this matters:
Raw probe accuracy can overstate representational encoding if the probe memorizes artifacts. Selectivity corrects for that.

Reviewer defense:
We report multi-seed behavior to ensure stability rather than a single favorable run.

## Slide 11: Surprisal Signal

Script:
Surprisal is computed from GPT-2 autoregressive probabilities:
\[
-\log P(t_i \mid t_1,\dots,t_{i-1})
\]
We use total, average, and absolute deltas between original and counterfactual sentences.
Key region coverage is 100%, so edited zones are fully represented in the surprisal analysis table.

Why GPT-2 surprisal:
It gives a clean left-to-right probabilistic signal and avoids mixing it with bidirectional pseudo-likelihood constructs in the primary track.

## Slide 12: Statistical Objectives

Script:
We define four objectives:
- D1 correlation structure,
- D2 incremental value of Frobenius over cosine,
- D3 layer-profile characterization,
- D4 probe selectivity stability.

The linear form shown is the controlled regression template with normalized variables and covariates such as length and overlap. We use bootstrap intervals and BH-FDR correction for multiplicity.

Reviewer defense:
This is important for reviewers concerned about multiple layer tests and inflated false positives. We apply explicit correction.

## Slide 13: Experiment Matrix and Coverage

Script:
This table gives coverage scope:
- 3000 pairs,
- 3 models,
- 13 layers each,
- 4 primary metrics,
- 117000 metric rows,
- 3000 surprisal rows,
- 390 probe rows.

Why this matters:
Claims are not based on a tiny pilot slice. The matrix is full and combinatorial across model, layer, metric, and phenomenon.

## Slide 14: Mean Shift Magnitude by Phenomenon

Script:
This three-panel figure is intentionally structured to avoid misleading scale effects:
- Left: raw means for cosine, Frobenius, token-aligned.
- Middle: raw L2 alone (because L2 scale is much larger).
- Right: within-metric normalization for cross-metric comparison.

What we see:
- Negation has larger mean shifts than role reversal for all metrics.
- Numeric means:
  - Negation: Delta_cos 0.0478, Delta_frob 0.0584, Delta_L2 27.8753, Delta_token 0.0502
  - Role reversal: Delta_cos 0.0124, Delta_frob 0.0197, Delta_L2 4.1960, Delta_token 0.0408

Why this pattern is plausible:
Negation inserts lexical and compositional polarity signals, producing broad representational movement. Role reversal is structurally strong but often lexically symmetric, which can produce smaller average geometric displacement in pooled space.

Reviewer defense:
We separate raw and normalized views to avoid overinterpreting L2 due to unit scale.

## Slide 15: Layer-Wise Correlation Curves

Script:
This figure has six panels: 2 phenomena x 3 models. Each panel plots Spearman rho across layers for Delta_cos and Delta_frob.

What it shows:
- Role reversal panels are strongly positive (roughly 0.2 to 0.37).
- Negation panels are weaker and mixed, with near-zero and some negative segments.
- The two metrics often track closely, but Frobenius slightly leads in some regions.

Why this matters:
Sensitivity is clearly phenomenon-dependent and layer-dependent. We are not seeing a single universal curve, which supports the need for structured per-phenomenon analysis.

Reviewer defense:
Plotting per phenomenon avoids the averaging artifact that can hide divergent behavior.

## Slide 16: Frobenius Heatmap Across Layers

Script:
This heatmap isolates Delta_frob correlations by model/layer/phenomenon. Dot markers indicate FDR-significant cells.

Visual interpretation:
- Role reversal side is broadly warm (positive) with dense significance dots.
- Negation side is mixed: some warm regions, some cool (negative) regions depending on model and layer.

What this means:
Frobenius is highly informative for role reversal and selectively informative for negation. The significance overlay prevents color-only interpretation errors.

Reviewer defense:
We combine effect magnitude and corrected significance in one view to avoid “bright color equals claim” mistakes.

## Slide 17: Probe Selectivity Across Layers

Script:
This figure shows three model panels, each with negation and role curves plus seed-level 95% ribbons.

What we see:
- Curves stay near 0.50 selectivity across layers.
- Overall mean selectivity is 0.5096.
- Model means are tightly clustered: BERT 0.5078, GPT-2 0.5112, RoBERTa 0.5099.
- Phenomenon means are similarly close: negation 0.5102, role 0.5090.

Interpretation:
Probe signal is robust and stable across models/layers, not a single-point anomaly.

Reviewer defense:
The ribbon widths show variance transparently; this is not a hidden single-seed report.

## Slide 18: Frobenius Shift vs Surprisal Delta

Script:
This is a density plot (hexbin) with per-phenomenon regression lines.
- Left panel (role reversal): clear positive slope.
- Right panel (negation): near-flat trend.

Supporting stats:
- Role reversal Pearson ~0.3599, Spearman ~0.3400.
- Negation Pearson ~0.0474, Spearman ~-0.0169.

Interpretation:
The shift-surprisal relationship is phenomenon-specific. Frobenius aligns with surprisal strongly for role reversal but weakly for negation, indicating that probabilistic difficulty and representational geometry are related but not interchangeable.

Reviewer defense:
We use density instead of raw scatter to avoid overplotting distortion with thousands of points.

## Slide 19: Incremental Value of Frobenius

Script:
This histogram shows \(\Delta\) adjusted-\(R^2\) when adding Delta_frob on top of a cosine baseline.
- Dashed line at zero is the no-gain threshold.
- Most mass lies to the right of zero.
- Summary box: positive in 70/78 cells, mean gain 0.0114, median 0.0069.

Interpretation:
Frobenius adds small but consistent explanatory value beyond cosine.

Reviewer defense:
The claim is incremental, not dominant. We explicitly present gain size and distribution, not just count of positive cells.

## Slide 20: RQ1 Answer

Script:
This stacked-bar figure decomposes positive and negative significant fractions per metric (FDR-corrected).

Key counts:
- Delta_cos: +50 / -6
- Delta_frob: +52 / -6
- Delta_L2: +47 / -5
- Delta_token: +32 / -32

Interpretation:
Cosine, Frobenius, and L2 show broad positive sensitivity. Token-aligned is intentionally more mixed, likely because local alignment can react differently than pooled/global geometry.

Reviewer defense:
We do not hide the mixed token-aligned result; it is shown explicitly and discussed as a diagnostic difference, not a failure.

## Slide 21: RQ2 Answer

Script:
This slide has two heatmaps:
- Left: positive-rate of incremental gain.
- Right: mean \(\Delta\) adjusted-\(R^2\) gain by model and phenomenon.

Values:
- Overall positive cells: 70/78.
- Overall mean gain: 0.0114.
- FDR-significant Frobenius coefficient in 54/78 cells.
- Perfect positive-rate cells in role reversal for GPT-2 and RoBERTa (1.00 each).

Interpretation:
Complementarity is broad and strongest in role-reversal settings.

Reviewer defense:
We provide both sign consistency and effect magnitude; either alone can mislead.

## Slide 22: RQ3 Answer

Script:
Bars show correlation between probe selectivity and metric-correlation strength, with 95% bootstrap CIs.

What we see:
- Point estimates are near zero for most metrics.
- CIs mostly cross zero.
- Token-aligned Pearson is slightly positive but still uncertainty-overlapping zero.

Interpretation:
Probe selectivity and shift-surprisal correlation are largely complementary rather than redundant diagnostics.

Reviewer defense:
We explicitly avoid claiming strong coupling when uncertainty intervals do not support it.

## Slide 23: Research Questions Final Answers

Script:
This table is the concise take-home:
- RQ1: yes, consistent structural sensitivity for cosine/Frobenius/L2.
- RQ2: yes, Frobenius provides measurable incremental value.
- RQ3: partial, strong probes but weak coupling with correlation strength.

Why this slide exists:
It ties the earlier evidence chain directly back to the predeclared questions.

## Slide 24: Key Quantitative Summary

Script:
This is a reviewer-friendly audit table:
- 102 significant positive cells (Delta_cos + Delta_frob combined),
- 70 positive Frobenius incremental cells,
- Mean incremental gain 0.0114,
- Mean probe selectivity 0.5096,
- Frobenius metric warnings: 0.

Interpretation:
The pipeline is numerically stable and the primary findings are supported by multiple, independent summaries.

## Slide 25: Claim Boundary and Validity

Script:
This is a deliberate boundary slide.
What we support: robust dataset-level structural sensitivity diagnostics.
What we do not claim: direct human cognitive equivalence in this run.

Why this is important:
A strong presentation is not just strong results; it also has precise claim boundaries. This protects scientific validity and avoids overclaiming.

Reviewer defense:
By stating limitations explicitly, we pre-empt the common critique that representation studies overinterpret cognitive alignment.

## Slide 26: Remaining Work

Script:
Remaining work is presentation and manuscript packaging:
- final claim-language consistency,
- final D1-D4 table curation,
- submission packaging and rehearsal.

Why modest remaining scope:
Core computation and analysis are already complete. Remaining tasks are synthesis and communication, not foundational reruns.

## Slide 27: Conclusion

Script:
The project has completed the full CSS pipeline for role reversal and negation across BERT, RoBERTa, and GPT-2 with four primary metrics and full layer coverage.
The central empirical conclusion is that Frobenius-based structural shift contributes complementary information beyond cosine in most model-layer cells.

Closing line:
The framework is now ready for external review as a reproducible, bounded, dataset-only representational analysis.

## Slide 28: References

Script:
Use this slide to anchor method lineage:
- model foundations (BERT, RoBERTa, GPT-2),
- benchmarking/probing context (BLiMP, Hewitt & Liang),
- psycholinguistic grounding (Levy surprisal),
- matrix-norm motivation (vor der Br\"uck & Pouly),
- and public dataset source.

Reviewer defense:
Every core component has a citation basis; no critical method component is uncited.

## Optional Q&A Anchors (Use If Challenged)

Q1: Why no human annotation in this version?  
A: This track is intentionally dataset-only to keep scope reproducible within timeline. Claims are restricted to representation diagnostics and are stated with that boundary.

Q2: Why should Frobenius be trusted beyond cosine?  
A: We do not ask for trust by assertion. We show incremental tests over cosine with 70/78 positive cells and nontrivial mean \(\Delta\) adjusted-\(R^2\), plus corrected significance counts.

Q3: Why only three base models?  
A: They provide architecture diversity (bidirectional encoders + autoregressive LM) with stable, reproducible compute. This is a controlled baseline suite, not an exhaustive leaderboard.

Q4: Why is negation weaker than role reversal in several plots?  
A: Negation effects can distribute across lexical cue and scope patterns, so pooled geometric/surprisal relationships are less uniformly monotonic. That heterogeneity is shown transparently.

Q5: Is token-aligned instability a problem?  
A: It is expected for a local metric under varied edit locality. We treat it as complementary and explicitly report both positive and negative significant fractions.
