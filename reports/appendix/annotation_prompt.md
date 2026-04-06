# CSS Human Semantic-Change Annotation Prompt (v1)

Task:
- You will see two sentences: `S` and `S'`.
- Rate how much the meaning changes from `S` to `S'` on a 0-5 scale.

Scale:
- `0`: same meaning / paraphrase.
- `1`: very small change.
- `2`: small but clear change.
- `3`: moderate change.
- `4`: large change.
- `5`: very large semantic change.

Guidance:
- Focus on semantic change, not grammar preference.
- Ignore punctuation/style differences if meaning is unchanged.
- Use the full scale.
- If uncertain between two values, choose the lower value.

Additional fields:
- confidence (`1-5`)
- fluency of each sentence (`1-5`)
- plausibility of each sentence (`1-5`)
- optional changed words note.

Attention checks:
- Some duplicate pairs appear to monitor consistency.
- Some obvious paraphrase/non-paraphrase controls are included.
