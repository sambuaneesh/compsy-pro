from __future__ import annotations

import numpy as np


def benjamini_hochberg(p_values: list[float]) -> list[float]:
    if not p_values:
        return []
    p = np.array(p_values, dtype=float)
    n = len(p)
    order = np.argsort(p)
    ranked = p[order]
    q = np.empty(n, dtype=float)
    prev = 1.0
    for i in range(n - 1, -1, -1):
        rank = i + 1
        val = ranked[i] * n / rank
        prev = min(prev, val)
        q[i] = prev
    q_final = np.empty(n, dtype=float)
    q_final[order] = np.clip(q, 0.0, 1.0)
    return q_final.tolist()
