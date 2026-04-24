# Qualitative Analysis Addendum (Dataset-Only)
## Purpose
This addendum responds to the need for deeper qualitative interpretation of the CSS results. It connects the aggregate statistics to actual counterfactual sentence pairs and explains why role reversal and negation behave differently under the same metric pipeline.
## How cases were selected
All cases below are selected reproducibly from the current full result tables. For each pair, metric values are averaged across the three primary models and all 13 layers. Pairs are then ranked within each phenomenon by mean Frobenius shift and by absolute GPT-2 average-surprisal delta. Four diagnostic buckets are reported per phenomenon: high/high, high/low, low/high, and low/low.
## Surface-form diagnostics
| Phenomenon | Pairs | Mean lexical Jaccard | Median lexical Jaccard | Mean abs length delta | Mean edit distance | Mean Frobenius shift | Mean abs avg surprisal delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| negation | 1500 | 0.4853 | 0.5000 | 1.0013 | 9.6000 | 0.0584 | 0.4918 |
| role_reversal | 1500 | 0.7973 | 0.7778 | 0.0467 | 19.4920 | 0.0197 | 0.4031 |

## Main qualitative findings
1. Negation shows larger average representation shifts partly because many source pairs are not pure one-token negation edits. They often combine a polarity cue with a predicate or category contrast, for example affirmative category membership versus a negated foil.
2. Role reversal has higher lexical overlap and usually near-zero length change, so its mean shift magnitude can be smaller even when the semantic event structure changes sharply.
3. This explains why aggregate mean shift and layer-wise correlation do not contradict each other: mean shift asks how large the movement is, while correlation asks whether item-level movement ranks track surprisal deltas.
4. Frobenius is qualitatively useful because it can capture changes in token-token relational geometry that are washed out by one pooled sentence vector.
5. The qualitative audit also surfaces generated-data artifacts, including occasional article mismatches, lexical substitutions, and implausible role-reversal continuations. These artifacts do not invalidate the dataset-only diagnostic, but they require conservative claim language and explain why we avoid human-comprehension claims.

## Case studies
### negation
#### high shift high surprisal
- Pair id: `neg_001015`
- Sentence: A spider is an arthropod.
- Counterfactual: A spider is not an plant.
- Metrics: mean Frobenius=0.0796, mean cosine=0.0655, mean L2=27.9760, mean token-aligned=0.0642, abs avg surprisal delta=1.6061
- Surface controls: lexical Jaccard=0.5714, abs length delta=1, edit distance=11
- Interpretation: Both diagnostics move together: the contextual geometry changes strongly and GPT-2 also assigns a large probability shift to the counterfactual. These are the clearest examples of aligned structural sensitivity.
#### high shift low surprisal
- Pair id: `neg_001105`
- Sentence: A hammer is an instrument.
- Counterfactual: A hammer is not a dessert.
- Metrics: mean Frobenius=0.0763, mean cosine=0.0626, mean L2=28.5618, mean token-aligned=0.0517, abs avg surprisal delta=0.0037
- Surface controls: lexical Jaccard=0.4286, abs length delta=1, edit distance=11
- Interpretation: The representation moves strongly even though average surprisal barely changes. This is evidence that hidden-state geometry can capture a structural or lexical relation that is not reducible to sentence-level predictive difficulty.
#### low shift high surprisal
- Pair id: `neg_000733`
- Sentence: A verb is a word.
- Counterfactual: A verb is not a noun.
- Metrics: mean Frobenius=0.0404, mean cosine=0.0317, mean L2=27.5056, mean token-aligned=0.0364, abs avg surprisal delta=1.4568
- Surface controls: lexical Jaccard=0.5000, abs length delta=1, edit distance=7
- Interpretation: GPT-2 surprisal changes strongly while the averaged representation shift is small. This is the complementary dissociation: probabilistic expectation and representation geometry are related diagnostics, but one is not a substitute for the other.
#### low shift low surprisal
- Pair id: `neg_000563`
- Sentence: A horse is a beast.
- Counterfactual: A horse is not a lion.
- Metrics: mean Frobenius=0.0424, mean cosine=0.0342, mean L2=27.2849, mean token-aligned=0.0392, abs avg surprisal delta=0.0053
- Surface controls: lexical Jaccard=0.5000, abs length delta=1, edit distance=9
- Interpretation: Both diagnostics are small. These cases help define the lower-sensitivity baseline and show that the pipeline is not mechanically assigning large shifts to every edit.
### role_reversal
#### high shift high surprisal
- Pair id: `role_000328`
- Sentence: The singer revealed which composer the pirate had kidnapped.
- Counterfactual: The singer revealed which opera the composer had composed.
- Metrics: mean Frobenius=0.0462, mean cosine=0.0389, mean L2=6.5533, mean token-aligned=0.0509, abs avg surprisal delta=1.5148
- Surface controls: lexical Jaccard=0.6000, abs length delta=0, edit distance=19
- Interpretation: Both diagnostics move together: the contextual geometry changes strongly and GPT-2 also assigns a large probability shift to the counterfactual. These are the clearest examples of aligned structural sensitivity.
#### high shift low surprisal
- Pair id: `role_001000`
- Sentence: The gardener planted which queen the flower had blooming.
- Counterfactual: The gardener planted which flower the queen had requested.
- Metrics: mean Frobenius=0.0402, mean cosine=0.0308, mean L2=5.5198, mean token-aligned=0.0720, abs avg surprisal delta=0.0146
- Surface controls: lexical Jaccard=0.7778, abs length delta=0, edit distance=19
- Interpretation: The representation moves strongly even though average surprisal barely changes. This is evidence that hidden-state geometry can capture a structural or lexical relation that is not reducible to sentence-level predictive difficulty.
#### low shift high surprisal
- Pair id: `role_000157`
- Sentence: The cashier counted which bills the robber had given.
- Counterfactual: The cashier counted which robber the bills had given.
- Metrics: mean Frobenius=0.0138, mean cosine=0.0084, mean L2=3.8891, mean token-aligned=0.0405, abs avg surprisal delta=1.1860
- Surface controls: lexical Jaccard=1.0000, abs length delta=0, edit distance=12
- Interpretation: GPT-2 surprisal changes strongly while the averaged representation shift is small. This is the complementary dissociation: probabilistic expectation and representation geometry are related diagnostics, but one is not a substitute for the other.
#### low shift low surprisal
- Pair id: `role_000806`
- Sentence: The novelist showed which poet the writer had admired.
- Counterfactual: The novelist showed which writer the poet had admired.
- Metrics: mean Frobenius=0.0031, mean cosine=0.0013, mean L2=1.6110, mean token-aligned=0.0246, abs avg surprisal delta=0.0068
- Surface controls: lexical Jaccard=1.0000, abs length delta=0, edit distance=10
- Interpretation: Both diagnostics are small. These cases help define the lower-sensitivity baseline and show that the pipeline is not mechanically assigning large shifts to every edit.

## Interpretation for presentation
When presenting the results, say that Slide 14 is pooled mean magnitude across models, layers, and pairs, while the later correlation slides ask whether pair-level shifts are rank-aligned with surprisal. Negation can therefore have larger average shift while role reversal shows a cleaner shift-surprisal relationship. The qualitative examples make this distinction concrete.

## Scope boundary
This remains a dataset-only qualitative analysis. It explains model-output artifacts and representation-shift behavior using sentence examples and surface controls. It does not introduce human-alignment claims.
