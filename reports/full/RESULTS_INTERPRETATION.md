# Results Interpretation (Dataset-Only)
## Research Question Answers
### RQ1: Do representation-shift metrics respond consistently to minimal structural edits across layers and models?
Yes, with metric-dependent consistency.
- Significant positive cells (FDR<0.05): delta_cos=50, delta_frob=52, delta_l2=47, delta_token_aligned=32.
- Cosine/Frobenius/L2 show broad positive alignment patterns; token-aligned shift is more mixed and phenomenon-sensitive.
- Frobenius layer peaks are concentrated in mid-to-late layers for role reversal, and early layers for negation.

Top Frobenius layer peaks by model/phenomenon:
- negation | bert-base-uncased: layer 0, rho=0.1542, q=4.39e-09
- negation | gpt2: layer 0, rho=0.1314, q=6.91e-07
- negation | roberta-base: layer 0, rho=0.1176, q=9.74e-06
- role_reversal | bert-base-uncased: layer 7, rho=0.3286, q=5.69e-38
- role_reversal | gpt2: layer 10, rho=0.3180, q=1.1e-35
- role_reversal | roberta-base: layer 7, rho=0.3683, q=3.38e-47

### RQ2: Does Frobenius shift add complementary value beyond cosine?
Yes, in most layer/model/phenomenon cells.
- Positive incremental cells (delta_adj_r2>0): 70/78.
- Mean incremental gain: delta_adj_r2=0.0114.
- Cells with FDR-significant Frobenius coefficient: 54.
- Interpretation: matrix-geometry information contributes beyond centroid-only similarity in this setup.

### RQ3: How do probes and surprisal interact with representation-shift diagnostics?
Probe selectivity is consistently positive, while its layer-wise coupling with metric-surprisal correlation strength is weak.
- Selectivity-vs-Frobenius-correlation coupling: Spearman=-0.0112, Pearson=0.0126.
- Interpretation: probe quality and metric-surprisal alignment are both meaningful, but mostly complementary rather than redundant signals.

## Overall Interpretation
- The results support robust dataset-level structural sensitivity claims for role reversal and negation.
- Frobenius shift is empirically useful as a complementary metric.
- Claims remain at representation/diagnostic level and do not imply human-cognition equivalence.

## Qualitative Interpretation Addendum
The review request for deeper qualitative analysis is addressed in `reports/full/QUALITATIVE_ANALYSIS.md`.

Key qualitative conclusions:
- Slide-level mean shift and layer-wise correlation are not contradictory. Mean shift measures average movement magnitude; correlation measures whether item-level movement ranks track GPT-2 surprisal deltas.
- Negation has larger pooled mean shifts partly because the source pairs often include both a negation cue and a predicate/category contrast, not only a single inserted `not`.
- Role reversal has much higher lexical overlap and near-zero length change, so its pooled shift magnitude can be smaller while its shift-surprisal ranking remains cleaner.
- Generated-data artifacts exist in the source examples, including article mismatch, lexical substitutions, and implausible continuations. These artifacts strengthen the need for conservative dataset-only claim language.

Surface-form audit:
- Negation: mean lexical Jaccard `0.4853`, mean absolute length delta `1.0013`, mean Frobenius shift `0.0584`.
- Role reversal: mean lexical Jaccard `0.7973`, mean absolute length delta `0.0467`, mean Frobenius shift `0.0197`.

Representative qualitative cases:
- High shift / low surprisal negation: `A hammer is an instrument.` -> `A hammer is not a dessert.` This shows hidden-state geometry can move strongly without a large average surprisal delta.
- Low shift / high surprisal role reversal: `The cashier counted which bills the robber had given.` -> `The cashier counted which robber the bills had given.` This shows surprisal can change strongly even when averaged geometry moves less.
