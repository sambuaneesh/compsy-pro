from __future__ import annotations

import numpy as np


def mean_pool(matrix: np.ndarray) -> np.ndarray:
    if matrix.size == 0:
        return np.zeros((matrix.shape[-1],), dtype=np.float32)
    return matrix.mean(axis=0, dtype=np.float32)


def row_l2_normalize(matrix: np.ndarray, eps: float = 1e-9) -> np.ndarray:
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    return matrix / np.clip(norms, eps, None)
