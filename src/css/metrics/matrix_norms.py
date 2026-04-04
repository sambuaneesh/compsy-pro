from __future__ import annotations

import numpy as np

from css.representations.pooling import row_l2_normalize


def _clip_non_negative(matrix: np.ndarray, enabled: bool) -> np.ndarray:
    return np.maximum(matrix, 0.0) if enabled else matrix


def frobenius_similarity(
    a: np.ndarray,
    b: np.ndarray,
    *,
    clip_negative: bool = True,
    row_normalize: bool = True,
    eps: float = 1e-9,
) -> float:
    if a.size == 0 or b.size == 0:
        return 0.0
    x = a.astype(np.float32)
    y = b.astype(np.float32)
    if row_normalize:
        x = row_l2_normalize(x)
        y = row_l2_normalize(y)

    s_cross = _clip_non_negative(x @ y.T, enabled=clip_negative)
    s_self_x = _clip_non_negative(x @ x.T, enabled=clip_negative)
    s_self_y = _clip_non_negative(y @ y.T, enabled=clip_negative)

    numer = float(np.linalg.norm(s_cross, ord="fro"))
    denom = float(
        np.sqrt(np.linalg.norm(s_self_x, ord="fro") * np.linalg.norm(s_self_y, ord="fro") + eps)
    )
    if denom <= 0.0:
        return 0.0
    return numer / denom


def frobenius_shift(
    a: np.ndarray,
    b: np.ndarray,
    *,
    clip_negative: bool = True,
    row_normalize: bool = True,
    eps: float = 1e-9,
) -> tuple[float, float]:
    sim = frobenius_similarity(
        a,
        b,
        clip_negative=clip_negative,
        row_normalize=row_normalize,
        eps=eps,
    )
    return sim, 1.0 - sim
