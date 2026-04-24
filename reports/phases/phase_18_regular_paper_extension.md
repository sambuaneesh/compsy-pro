# Phase 18 Report: Regular-Paper Extension

Status: in progress

Purpose:
- Strengthen the work from a short/workshop-style CSS study toward a regular-paper submission.
- Add output-level counterfactual consistency so the project connects more directly to logical-consistency review criteria.
- Add modern decoder-only model support while preserving the original baseline CSS scope.

Implementation changes:
- Added `src/css/consistency/counterfactual_consistency.py` for forced-choice yes/no scoring.
- Added `src/css/consistency/summarize_consistency.py` for consistency accuracy, yes-rate bias, margin summaries, and CSS-shift/no-margin correlations.
- Updated hidden-state extraction to support modern decoder loading with `torch_dtype`, `trust_remote_code`, `device_map`, `max_memory`, and `low_cpu_mem_usage`.
- Added configs for Mistral-7B-Instruct-v0.3, Qwen3-8B, Qwen3-4B fallback, Gemma-3-4B-IT, and Llama-3.1-8B.

Current access/compute notes:
- `google/gemma-3-4b-it` is gated for the available Hugging Face token and cannot be run until access is approved.
- `Qwen/Qwen3-8B` is public but downloads about 16.4GB in fp16, which is too close to the 16GB GPU limit for reliable non-offloaded runs.
- `mistralai/Mistral-7B-Instruct-v0.3` is accessible and is the preferred listed modern decoder currently being run.
- `Qwen/Qwen3-4B` is configured as a practical fallback if 7B/8B extraction is too slow.

Completed results:
- GPT-2 output-level consistency completed on all 3000 pairs.
- GPT-2 shows a strong `no` bias: high apparent counterfactual rejection but poor identity-control accuracy, so it should be described as a biased baseline rather than a valid instruction-following logical-consistency model.

Definition of done for this phase:
- Complete output-level consistency for at least one modern decoder.
- Run hidden-state CSS metrics for at least one modern decoder if compute permits.
- Regenerate consistency summaries and update the paper/slides/docs with modern-model results.
- Log any gated-model or OOM failures explicitly rather than silently dropping models.
