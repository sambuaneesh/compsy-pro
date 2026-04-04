from __future__ import annotations

import numpy as np

from css.metrics.cosine import cosine_shift
from css.representations.token_alignment import align_words_exact, positional_fallback


def aligned_token_shift(
    *,
    words_a: list[str],
    words_b: list[str],
    matrix_a: np.ndarray,
    matrix_b: np.ndarray,
) -> float:
    alignments = align_words_exact(words_a, words_b)
    if not alignments:
        alignments = positional_fallback(words_a, words_b)
    if not alignments:
        return 0.0
    vals = []
    for i, j in alignments:
        if i >= matrix_a.shape[0] or j >= matrix_b.shape[0]:
            continue
        vals.append(cosine_shift(matrix_a[i].astype(np.float32), matrix_b[j].astype(np.float32)))
    if not vals:
        return 0.0
    return float(np.mean(vals))
