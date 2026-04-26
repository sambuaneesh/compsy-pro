# IJCAI-ECAI 2026 LogiSymb Submission Plan

Last checked: 2026-04-26

Target workshop:
**Workshop on Logical and Symbolic Reasoning of Large Language Models (LogiSymb), IJCAI-ECAI 2026**

Primary URL:
https://sites.google.com/view/ijcai-2026-logisymb

Accepted-workshops listing:
https://2026.ijcai.org/accepted-workshops/

OpenReview submission site:
https://openreview.net/group?id=ijcai.org/IJCAI-ECAI/2026/Workshop/LogiSymb

IJCAI author kit:
https://www.ijcai.org/authors_kit

## Workshop Details

Venue:
- IJCAI-ECAI 2026, Bremen, Germany.
- Workshop page lists the workshop date as **August 15, 2026**.
- IJCAI-ECAI 2026 overall conference dates are **August 15-21, 2026**.
- IJCAI workshop proposal page says workshops are held immediately before the main conference, **August 15-17, 2026**.

Stated workshop focus:
- Logical question answering.
- Logical consistency.
- LLM failures under multiple premises and constraints.
- Contradictory responses across related questions.
- Deduction, induction, and abduction in LLMs.
- Neuro-symbolic integration, constraint-based methods, memory-augmented methods.

Topics explicitly listed:
- Logical question answering of LLMs.
- Chain-of-thought reasoning of LLMs.
- External tool use, including logic solvers.
- Logical consistency, including implication consistency and negation consistency.
- Mathematical and symbolic reasoning, including proof writing via logical rules.

Fit for our CSS project:
- Strongest fit: **logical consistency / negation consistency / compositional consistency / interpretability of internal representations**.
- We should frame role reversal as event-structure consistency and argument-role reversal, not as generic psycholinguistics.
- We should frame negation as logical polarity sensitivity and negation-consistency diagnostics.
- We should avoid claiming we solve logical QA or solver-based reasoning.

## Important Dates

All deadlines are Anywhere on Earth (AoE).

| Item | Date |
| --- | --- |
| Submission deadline | May 31, 2026 |
| Notification of acceptance | June 14, 2026 |
| Workshop date on workshop page | August 15, 2026 |
| IJCAI-ECAI 2026 conference | August 15-21, 2026 |

## Submission Format

Paper types:
- **Regular papers**: 4 to 10 pages, excluding references and supplementary material.
- **Tiny/Short papers**: 2 to 4 pages, excluding references and supplementary material.

Formatting:
- IJCAI-ECAI 2026 format.
- The IJCAI author kit includes `ijcai26.tex`, `ijcai26.sty`, `named.bst`, `ijcai26.bib`, and a Word template.
- Abstract should be at most 200 words according to the IJCAI formatting guide.
- IJCAI style uses two-column layout and 10-point body font.
- No page numbers, headers, or footers in the style.

Anonymity:
- Workshop review is double-blind.
- Submissions must remove author names, affiliations, acknowledgments, and identifying information.
- Camera-ready can restore author information if accepted.

Archival status:
- The workshop says contributions are **non-archival**.
- It welcomes unpublished manuscripts and previously accepted/published papers, provided there is no dual-submission policy violation.

Submission system:
- OpenReview.

Awards:
- Oral Presentation Awards.
- Outstanding Paper Awards.
- One Best Paper Award.

## Critical Reviewer Assessment of Current Project

### Current Strengths

The project is much stronger now than before the qualitative update:
- Full dataset-only pipeline is complete for 3000 pairs.
- Three baseline model families are covered: BERT, RoBERTa, GPT-2.
- All 13 layers are analyzed.
- Four representation-shift metrics are computed.
- GPT-2 surprisal is computed for all pairs.
- Probe selectivity controls are included.
- Qualitative case studies now explain the aggregate results.
- The claim boundary is conservative and defensible.

Strongest current contribution:
**CSS is a reproducible protocol for probing whether hidden representations react systematically to controlled logical/structural edits, especially negation and argument-role reversal.**

### Current Weaknesses

As a critical reviewer, I would raise these concerns:

1. **Workshop fit is good but not perfect.**
   The workshop is centered on logical question answering and logical consistency. Our project is representational probing, not output-level logical QA.

2. **Model suite is somewhat dated for a 2026 LLM workshop.**
   BERT, RoBERTa, and GPT-2 are good scientific baselines, but reviewers may ask why no modern decoder-only LLM is included.

3. **No direct output-level consistency result.**
   We show hidden-state sensitivity and surprisal, but not whether models answer paired logical prompts consistently.

4. **Dataset artifacts are real.**
   The qualitative audit found generated-data issues such as article mismatches, lexical substitutions, and implausible continuations. We can manage this with claim boundaries, but reviewers may still question dataset quality.

5. **No human annotation.**
   This is acceptable because the current scope is dataset-only, but it prevents human-alignment claims.

6. **Frobenius gain is consistent but moderate.**
   Mean adjusted-R2 gain is positive but small (`0.0114`). We should sell it as complementary signal, not as a major performance jump.

## Are Current Results Enough?

For a **Tiny/Short paper (2-4 pages)**:
- Yes, current results are enough if framed tightly.
- Recommended title framing:
  **Counterfactual Structural Sensitivity: Dataset-Only Diagnostics for Negation and Argument-Role Consistency in Language Model Representations**
- Main story:
  controlled logical edits -> layer-wise hidden-state shifts -> Frobenius complementarity -> qualitative dissociations.

For a **Regular paper (4-10 pages)**:
- Borderline as-is.
- I would not submit a full regular paper without at least one additional experiment that makes the work more clearly relevant to LogiSymb.

## Recommended Additions Before Drafting Final Regular Paper

### Priority 1: Add one modern decoder-only LLM

Rationale:
The workshop is about LLMs. GPT-2 is useful for surprisal but weak as a 2026 LLM representative.

Recommended minimal add:
- `Qwen/Qwen3-8B` if compute allows.
- `meta-llama/Llama-3.1-8B` if license/access is manageable.
- `mistralai/Mistral-7B-Instruct-v0.3` as a strong open 7B instruction model.
- `google/gemma-3-4b-it` as a lighter modern option if GPU memory is constrained.

Practical note:
- For hidden-state extraction, base or instruct causal models can work through Hugging Face `output_hidden_states=True`.
- 7B/8B models will likely require GPU memory planning, batching, `bfloat16`/`float16`, and possibly quantization.
- If compute is constrained, use a **500-pair qualitative/diagnostic subset** first, not all 3000 pairs.

Best cost-quality choice:
- Add **one** modern model, not many.
- Prefer `Qwen/Qwen3-8B` or `Mistral-7B-Instruct-v0.3` for a regular paper.
- Prefer `google/gemma-3-4b-it` if hardware is limited.

### Priority 2: Add output-level logical consistency probes

Rationale:
This directly targets the workshop focus.

Minimal experiment:
- Convert a subset of negation and role-reversal pairs into yes/no or forced-choice prompts.
- Ask models whether statements are logically consistent with the original sentence.
- Measure pair consistency:
  - negation flip consistency
  - role reversal consistency
  - contradiction rate
  - answer flip rate

Example:
- Context: `The chef praised the waiter.`
- Query 1: `Did the chef praise the waiter?`
- Query 2: `Did the waiter praise the chef?`
- Desired behavior: yes/no should differ unless both events are independently stated.

Why this matters:
- It gives reviewers an external behavior result linked to internal representation shifts.
- Then we can test whether larger CSS shifts predict output inconsistency or answer-flip behavior.

### Priority 3: Add dataset quality tags

Rationale:
Qualitative audit already found artifacts. We should turn this into a controlled analysis.

Minimal implementation:
- Automatically tag pairs for:
  - article mismatch (`a`/`an`)
  - lexical Jaccard bands
  - length-delta bands
  - high edit distance
  - suspicious role continuations (`had talked`, `had blooming`, etc.)
- Re-run core stats on:
  - all pairs
  - clean subset
  - artifact-flagged subset

Reviewer value:
- Shows robustness and honesty.
- Prevents dataset-quality criticism from becoming fatal.

### Priority 4: Add one salience example figure/table

Rationale:
The salience experiment exists but is not central in the current paper.

Minimal addition:
- Show token/span contribution for 2-4 qualitative examples.
- Tie Frobenius contribution back to edited spans.

This makes the paper more interpretable without huge compute.

## Recommended Paper Strategy

### If submitting short paper

Use current results.

Paper structure:
1. Motivation: logical edits and hidden-state sensitivity.
2. CSS protocol.
3. Dataset and models.
4. Metrics and statistics.
5. Main quantitative results.
6. Qualitative case studies.
7. Limitations and claim boundary.

Main claim:
**CSS shows that representation-shift metrics, especially Frobenius-style token-matrix geometry, provide complementary diagnostics for negation and argument-role consistency under controlled counterfactual edits.**

### If submitting regular paper

Add:
1. One modern decoder-only LLM.
2. Output-level logical consistency experiment.
3. Clean-subset robustness analysis.

Regular paper section plan:
1. Introduction.
2. Related work.
3. CSS protocol.
4. Dataset and artifact-aware controls.
5. Representation metrics.
6. Output-level logical consistency.
7. Quantitative results.
8. Qualitative analysis.
9. Salience examples.
10. Limitations.

## Go / No-Go Decision

Current state:
- **Go for Tiny/Short paper.**
- **Conditional go for Regular paper**, only if we add at least output-level logical consistency or one modern LLM.

My recommendation:
Submit a **4-page short paper** if time is tight. It will be defensible and clean.

If we have 1-2 extra working days:
- Add output-level consistency first.
- Add a modern LLM second.

If we have GPU access and more time:
- Target a regular paper with modern model + consistency + clean-subset robustness.

## Immediate Draft Checklist

1. Decide paper type: short vs regular.
2. If short: compress current paper into 4 IJCAI pages.
3. If regular: run at least output-level consistency before drafting final claims.
4. Prepare anonymous IJCAI LaTeX template.
5. Remove author-identifying text from submission PDF.
6. Include qualitative analysis as a compact table, not a long appendix.
7. Keep title focused on logical/structural consistency, not human alignment.
8. Mention dataset artifacts in limitations.
9. Do not claim human-like processing.
10. Submit via OpenReview before May 31, 2026 AoE.

## Source Notes

Workshop page:
- Date/location: August 15, 2026, Bremen, Germany.
- Scope: logical question answering and logical consistency.
- Topics: logical QA, chain-of-thought, tool use/logic solvers, logical consistency, mathematical/symbolic reasoning.
- Deadline: May 31, 2026 AoE.
- Notification: June 14, 2026 AoE.
- Submission: OpenReview.
- Paper lengths: regular 4-10 pages, short/tiny 2-4 pages.
- Format: IJCAI 2026.
- Review: double-blind.
- Contributions: non-archival.

IJCAI accepted-workshops page:
- Confirms workshop listing as “Proposal for IJCAI-ECAI 26 Workshop on Logical and Symbolic Reasoning of Large Language Models.”

IJCAI author kit:
- Provides the IJCAI-ECAI 2026 formatting files.
- Formatting guide notes a 200-word abstract maximum and standard IJCAI two-column format.

Model references checked:
- `Qwen/Qwen3-8B`: https://huggingface.co/Qwen/Qwen3-8B
- `meta-llama/Llama-3.1-8B`: https://huggingface.co/meta-llama/Llama-3.1-8B
- `mistralai/Mistral-7B-Instruct-v0.3`: https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3
- `google/gemma-3-4b-it`: https://huggingface.co/google/gemma-3-4b-it

