from __future__ import annotations

import numpy as np


def cosine_similarity(a: np.ndarray, b: np.ndarray, eps: float = 1e-9) -> float:
    denom = max(float(np.linalg.norm(a) * np.linalg.norm(b)), eps)
    return float(np.dot(a, b) / denom)


def cosine_shift(a: np.ndarray, b: np.ndarray) -> float:
    return 1.0 - cosine_similarity(a, b)
