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
