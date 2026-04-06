# Phase 14 Report: Final Audit and Submission Readiness

Status: conditionally complete

Checklist status:
1. `role_1500.jsonl`, `neg_1500.jsonl`, `attach_1500.jsonl` validate: pass.
2. Hidden states cached for `bert-base-uncased`, `roberta-base`, `gpt2`: pass.
3. Metrics computed for all pairs/layers/models: pass (`175500` rows).
4. Annotation target availability:
   - pipeline fallback present (`300` balanced pairs, 3 annotators/item, simulated).
   - publication requirement (real human annotations) still pending.
5. Probes + controls run: pass (full probe outputs + selectivity summaries).
6. GPT-2 surprisal computed: pass (`4500` rows).
7. H1-H5 statistical tables with CIs/FDR: pass (`results/stats/full/*`).
8. Figures/tables script-generated: pass.
9. Workshop paper draft + appendix exists: pass.
10. Incremental serialized logs and reproducibility traceability: pass.

Release risk summary:
- Primary blocker for camera-ready scientific claims: replace simulated annotations with real human ratings.
- All engineering and reproducibility infrastructure is in place for that swap without schema changes.
