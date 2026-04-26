# Qualitative Analysis Addendum (Dataset-Only)
## Purpose
This addendum responds to the need for deeper qualitative interpretation of the CSS results. It connects the aggregate statistics to actual counterfactual sentence pairs and explains why role reversal and negation behave differently under the same metric pipeline.
## How cases were selected
All cases below are selected reproducibly from the current full result tables. For each pair, metric values are averaged across the model `google/gemma-3-4b-it` and 35 layers indexed `0..34`. Pairs are then ranked within each phenomenon by mean Frobenius shift and by absolute GPT-2 average-surprisal delta. Four diagnostic buckets are reported per phenomenon: high/high, high/low, low/high, and low/low.
## Surface-form diagnostics
| Phenomenon | Pairs | Mean lexical Jaccard | Median lexical Jaccard | Mean abs length delta | Mean edit distance | Mean Frobenius shift | Mean abs avg surprisal delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| negation | 1500 | 0.4853 | 0.5000 | 1.0013 | 9.6000 | 0.0071 | 0.4918 |
| role_reversal | 1500 | 0.7973 | 0.7778 | 0.0467 | 19.4920 | 0.0021 | 0.4031 |

## Main qualitative findings
1. Negation shows larger average representation shifts partly because many source pairs are not pure one-token negation edits. They often combine a polarity cue with a predicate or category contrast, for example affirmative category membership versus a negated foil.
2. Role reversal has higher lexical overlap and usually near-zero length change, so its mean shift magnitude can be smaller even when the semantic event structure changes sharply.
3. This explains why aggregate mean shift and layer-wise correlation do not contradict each other: mean shift asks how large the movement is, while correlation asks whether item-level movement ranks track surprisal deltas.
4. Frobenius is qualitatively useful because it can capture changes in token-token relational geometry that are washed out by one pooled sentence vector.
5. The qualitative audit also surfaces generated-data artifacts, including occasional article mismatches, lexical substitutions, and implausible role-reversal continuations. These artifacts do not invalidate the dataset-only diagnostic, but they require conservative claim language and explain why we avoid human-comprehension claims.

## Case studies
### negation
#### high shift high surprisal
- Pair id: `neg_001361`
- Sentence: A cloud is an atmospheric.
- Counterfactual: A cloud is not a star.
- Metrics: mean Frobenius=0.0107, mean cosine=0.0089, mean L2=2061.2940, mean token-aligned=0.0000, abs avg surprisal delta=1.9573
- Surface controls: lexical Jaccard=0.4286, abs length delta=1, edit distance=11
- Interpretation: Both diagnostics move together: the contextual geometry changes strongly and GPT-2 also assigns a large probability shift to the counterfactual. These are the clearest examples of aligned structural sensitivity.
#### high shift low surprisal
- Pair id: `neg_001105`
- Sentence: A hammer is an instrument.
- Counterfactual: A hammer is not a dessert.
- Metrics: mean Frobenius=0.0096, mean cosine=0.0078, mean L2=1869.0923, mean token-aligned=0.0000, abs avg surprisal delta=0.0037
- Surface controls: lexical Jaccard=0.4286, abs length delta=1, edit distance=11
- Interpretation: The representation moves strongly even though average surprisal barely changes. This is evidence that hidden-state geometry can capture a structural or lexical relation that is not reducible to sentence-level predictive difficulty.
#### low shift high surprisal
- Pair id: `neg_001497`
- Sentence: A camel is a mammals.
- Counterfactual: A camel is not a reptile.
- Metrics: mean Frobenius=0.0058, mean cosine=0.0047, mean L2=1457.3893, mean token-aligned=0.0025, abs avg surprisal delta=2.1186
- Surface controls: lexical Jaccard=0.5000, abs length delta=1, edit distance=10
- Interpretation: GPT-2 surprisal changes strongly while the averaged representation shift is small. This is the complementary dissociation: probabilistic expectation and representation geometry are related diagnostics, but one is not a substitute for the other.
#### low shift low surprisal
- Pair id: `neg_001261`
- Sentence: A spruce is a tree.
- Counterfactual: A spruce is not a bush.
- Metrics: mean Frobenius=0.0056, mean cosine=0.0047, mean L2=1377.5630, mean token-aligned=0.0025, abs avg surprisal delta=0.0117
- Surface controls: lexical Jaccard=0.5000, abs length delta=1, edit distance=8
- Interpretation: Both diagnostics are small. These cases help define the lower-sensitivity baseline and show that the pipeline is not mechanically assigning large shifts to every edit.
### role_reversal
#### high shift high surprisal
- Pair id: `role_000328`
- Sentence: The singer revealed which composer the pirate had kidnapped.
- Counterfactual: The singer revealed which opera the composer had composed.
- Metrics: mean Frobenius=0.0048, mean cosine=0.0041, mean L2=986.4079, mean token-aligned=0.0030, abs avg surprisal delta=1.5148
- Surface controls: lexical Jaccard=0.6000, abs length delta=0, edit distance=19
- Interpretation: Both diagnostics move together: the contextual geometry changes strongly and GPT-2 also assigns a large probability shift to the counterfactual. These are the clearest examples of aligned structural sensitivity.
#### high shift low surprisal
- Pair id: `role_000866`
- Sentence: The boy scolded which jeweler the burgler had robbed.
- Counterfactual: The boy scolded which burglar the jeweler had identified.
- Metrics: mean Frobenius=0.0039, mean cosine=0.0028, mean L2=907.3272, mean token-aligned=0.0037, abs avg surprisal delta=0.0378
- Surface controls: lexical Jaccard=0.6000, abs length delta=0, edit distance=17
- Interpretation: The representation moves strongly even though average surprisal barely changes. This is evidence that hidden-state geometry can capture a structural or lexical relation that is not reducible to sentence-level predictive difficulty.
#### low shift high surprisal
- Pair id: `role_000157`
- Sentence: The cashier counted which bills the robber had given.
- Counterfactual: The cashier counted which robber the bills had given.
- Metrics: mean Frobenius=0.0013, mean cosine=0.0011, mean L2=1017.1789, mean token-aligned=0.0043, abs avg surprisal delta=1.1860
- Surface controls: lexical Jaccard=1.0000, abs length delta=0, edit distance=12
- Interpretation: GPT-2 surprisal changes strongly while the averaged representation shift is small. This is the complementary dissociation: probabilistic expectation and representation geometry are related diagnostics, but one is not a substitute for the other.
#### low shift low surprisal
- Pair id: `role_000740`
- Sentence: The four-year-old boy knew which hero the dragon had slain.
- Counterfactual: The four-year-old boy knew which dragon the hero had slain.
- Metrics: mean Frobenius=0.0006, mean cosine=0.0005, mean L2=634.4417, mean token-aligned=0.0025, abs avg surprisal delta=0.0007
- Surface controls: lexical Jaccard=1.0000, abs length delta=0, edit distance=10
- Interpretation: Both diagnostics are small. These cases help define the lower-sensitivity baseline and show that the pipeline is not mechanically assigning large shifts to every edit.

## Interpretation for presentation
When presenting this model-specific addendum, separate magnitude from correlation. Magnitude summarizes how far this model's hidden states move on average, while correlation asks whether pair-level shifts rank-align with surprisal deltas. The qualitative examples make this distinction concrete.

## Scope boundary
This remains a dataset-only qualitative analysis. It explains model-output artifacts and representation-shift behavior using sentence examples and surface controls. It does not introduce human-alignment claims.
