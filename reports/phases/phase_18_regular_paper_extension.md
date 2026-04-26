# Phase 18 Report: Regular-Paper Extension

Status: complete for Mistral-7B extension

Purpose:
- Strengthen the work from a short/workshop-style CSS study toward a regular-paper submission.
- Add output-level counterfactual consistency so the project connects more directly to logical-consistency review criteria.
- Add modern decoder-only model support while preserving the original baseline CSS scope.

Implementation changes:
- Added `src/css/consistency/counterfactual_consistency.py` for forced-choice yes/no scoring.
- Added `src/css/consistency/summarize_consistency.py` for consistency accuracy, yes-rate bias, margin summaries, and CSS-shift/no-margin correlations.
- Updated hidden-state extraction to support modern decoder loading with `torch_dtype`, `trust_remote_code`, `device_map`, `max_memory`, and `low_cpu_mem_usage`.
- Added configs for Mistral-7B-Instruct-v0.3, Qwen3-8B, Qwen3-4B fallback, Gemma-3-4B-IT, and Llama-3.1-8B.

Access/compute notes:
- `google/gemma-3-4b-it` is gated for the available Hugging Face token and cannot be run until access is approved.
- `meta-llama/Llama-3.1-8B` is also gated for the available Hugging Face token.
- `Qwen/Qwen3-8B` is public but downloads about 16.4GB in fp16, which is too close to the 16GB GPU limit for reliable non-offloaded runs.
- `mistralai/Mistral-7B-Instruct-v0.3` is accessible and completed successfully.
- `Qwen/Qwen3-4B` is configured as a practical fallback if 7B/8B extraction is too slow.

Completed results:
- GPT-2 output-level consistency completed on all 3000 pairs.
- GPT-2 shows a strong `no` bias: high apparent counterfactual rejection but poor identity-control accuracy, so it should be described as a biased baseline rather than a valid instruction-following logical-consistency model.
- Mistral output-level consistency completed on all 3000 pairs:
  - identity controls: `1.0000` accuracy for role reversal and negation
  - counterfactual role reversal: `0.7340` accuracy
  - counterfactual negation: `0.6520` accuracy
- Mistral hidden-state extraction completed for role and negation.
- Mistral metric computation wrote `99000` rows and `0` Frobenius warnings.
- Mistral dataset-only stats wrote `results/stats/modern_mistral_7b/`.
- Mistral qualitative cases wrote `reports/full/QUALITATIVE_ANALYSIS_MISTRAL_7B.md`.

Definition of done for this phase:
- Complete output-level consistency for at least one modern decoder: done with Mistral-7B-Instruct-v0.3.
- Run hidden-state CSS metrics for at least one modern decoder if compute permits: done with Mistral-7B-Instruct-v0.3.
- Regenerate consistency summaries and update the paper/slides/docs with modern-model results: reports updated; slides/paper can now be revised from the generated tables.
- Log any gated-model or OOM failures explicitly rather than silently dropping models: Gemma gating and Qwen3-8B memory boundary documented.
