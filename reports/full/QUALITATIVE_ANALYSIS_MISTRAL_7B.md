# Qualitative Analysis Addendum (Dataset-Only)
## Purpose
This addendum responds to the need for deeper qualitative interpretation of the CSS results. It connects the aggregate statistics to actual counterfactual sentence pairs and explains why role reversal and negation behave differently under the same metric pipeline.
## How cases were selected
All cases below are selected reproducibly from the current full result tables. For each pair, metric values are averaged across the three primary models and all 13 layers. Pairs are then ranked within each phenomenon by mean Frobenius shift and by absolute GPT-2 average-surprisal delta. Four diagnostic buckets are reported per phenomenon: high/high, high/low, low/high, and low/low.
## Surface-form diagnostics
| Phenomenon | Pairs | Mean lexical Jaccard | Median lexical Jaccard | Mean abs length delta | Mean edit distance | Mean Frobenius shift | Mean abs avg surprisal delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| negation | 1500 | 0.4853 | 0.5000 | 1.0013 | 9.6000 | 0.1255 | 0.4918 |
| role_reversal | 1500 | 0.7973 | 0.7778 | 0.0467 | 19.4920 | 0.0675 | 0.4031 |

## Main qualitative findings
1. Negation shows larger average representation shifts partly because many source pairs are not pure one-token negation edits. They often combine a polarity cue with a predicate or category contrast, for example affirmative category membership versus a negated foil.
2. Role reversal has higher lexical overlap and usually near-zero length change, so its mean shift magnitude can be smaller even when the semantic event structure changes sharply.
3. This explains why aggregate mean shift and layer-wise correlation do not contradict each other: mean shift asks how large the movement is, while correlation asks whether item-level movement ranks track surprisal deltas.
4. Frobenius is qualitatively useful because it can capture changes in token-token relational geometry that are washed out by one pooled sentence vector.
5. The qualitative audit also surfaces generated-data artifacts, including occasional article mismatches, lexical substitutions, and implausible role-reversal continuations. These artifacts do not invalidate the dataset-only diagnostic, but they require conservative claim language and explain why we avoid human-comprehension claims.

## Case studies
### negation
#### high shift high surprisal
- Pair id: `neg_000531`
- Sentence: A ruler is a stationary.
- Counterfactual: A ruler is not a toy.
- Metrics: mean Frobenius=0.1520, mean cosine=0.1168, mean L2=6.1867, mean token-aligned=0.1185, abs avg surprisal delta=2.0447
- Surface controls: lexical Jaccard=0.5000, abs length delta=1, edit distance=9
- Interpretation: Both diagnostics move together: the contextual geometry changes strongly and GPT-2 also assigns a large probability shift to the counterfactual. These are the clearest examples of aligned structural sensitivity.
#### high shift low surprisal
- Pair id: `neg_001439`
- Sentence: A scissor is a tool.
- Counterfactual: An scissor is not a plant.
- Metrics: mean Frobenius=0.1599, mean cosine=0.1324, mean L2=6.8936, mean token-aligned=0.2703, abs avg surprisal delta=0.0193
- Surface controls: lexical Jaccard=0.4286, abs length delta=1, edit distance=10
- Interpretation: The representation moves strongly even though average surprisal barely changes. This is evidence that hidden-state geometry can capture a structural or lexical relation that is not reducible to sentence-level predictive difficulty.
#### low shift high surprisal
- Pair id: `neg_000039`
- Sentence: A person is a mammal.
- Counterfactual: A person is not a reptile.
- Metrics: mean Frobenius=0.0980, mean cosine=0.0651, mean L2=4.7147, mean token-aligned=0.0664, abs avg surprisal delta=1.2369
- Surface controls: lexical Jaccard=0.5000, abs length delta=1, edit distance=10
- Interpretation: GPT-2 surprisal changes strongly while the averaged representation shift is small. This is the complementary dissociation: probabilistic expectation and representation geometry are related diagnostics, but one is not a substitute for the other.
#### low shift low surprisal
- Pair id: `neg_000275`
- Sentence: A church is a building.
- Counterfactual: A church is not a toy.
- Metrics: mean Frobenius=0.1082, mean cosine=0.0790, mean L2=5.3235, mean token-aligned=0.0718, abs avg surprisal delta=0.0028
- Surface controls: lexical Jaccard=0.5000, abs length delta=1, edit distance=10
- Interpretation: Both diagnostics are small. These cases help define the lower-sensitivity baseline and show that the pipeline is not mechanically assigning large shifts to every edit.
### role_reversal
#### high shift high surprisal
- Pair id: `role_001243`
- Sentence: The teacher asked which student the question had belonged.
- Counterfactual: The teacher asked which question the student had answered.
- Metrics: mean Frobenius=0.1033, mean cosine=0.0620, mean L2=4.3984, mean token-aligned=0.1641, abs avg surprisal delta=1.5487
- Surface controls: lexical Jaccard=0.7778, abs length delta=0, edit distance=20
- Interpretation: Both diagnostics move together: the contextual geometry changes strongly and GPT-2 also assigns a large probability shift to the counterfactual. These are the clearest examples of aligned structural sensitivity.
#### high shift low surprisal
- Pair id: `role_000347`
- Sentence: The musician remembered which groupie the security guard had stopped.
- Counterfactual: The security guard remembered which groupie the musician had invited.
- Metrics: mean Frobenius=0.1430, mean cosine=0.0990, mean L2=6.2439, mean token-aligned=0.2428, abs avg surprisal delta=0.0006
- Surface controls: lexical Jaccard=0.8000, abs length delta=0, edit distance=27
- Interpretation: The representation moves strongly even though average surprisal barely changes. This is evidence that hidden-state geometry can capture a structural or lexical relation that is not reducible to sentence-level predictive difficulty.
#### low shift high surprisal
- Pair id: `role_000389`
- Sentence: The butler explained which guest the host had invited.
- Counterfactual: The butler explained which guest the host had seem.
- Metrics: mean Frobenius=0.0175, mean cosine=0.0073, mean L2=1.3048, mean token-aligned=-0.0000, abs avg surprisal delta=1.4654
- Surface controls: lexical Jaccard=0.7778, abs length delta=0, edit distance=6
- Interpretation: GPT-2 surprisal changes strongly while the averaged representation shift is small. This is the complementary dissociation: probabilistic expectation and representation geometry are related diagnostics, but one is not a substitute for the other.
#### low shift low surprisal
- Pair id: `role_000806`
- Sentence: The novelist showed which poet the writer had admired.
- Counterfactual: The novelist showed which writer the poet had admired.
- Metrics: mean Frobenius=0.0243, mean cosine=0.0121, mean L2=1.9335, mean token-aligned=0.0785, abs avg surprisal delta=0.0068
- Surface controls: lexical Jaccard=1.0000, abs length delta=0, edit distance=10
- Interpretation: Both diagnostics are small. These cases help define the lower-sensitivity baseline and show that the pipeline is not mechanically assigning large shifts to every edit.

## Interpretation for presentation
When presenting the results, say that Slide 14 is pooled mean magnitude across models, layers, and pairs, while the later correlation slides ask whether pair-level shifts are rank-aligned with surprisal. Negation can therefore have larger average shift while role reversal shows a cleaner shift-surprisal relationship. The qualitative examples make this distinction concrete.

## Scope boundary
This remains a dataset-only qualitative analysis. It explains model-output artifacts and representation-shift behavior using sentence examples and surface controls. It does not introduce human-alignment claims.
