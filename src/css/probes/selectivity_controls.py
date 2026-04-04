from __future__ import annotations

import numpy as np


def random_label_control(y_train: np.ndarray, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    shuffled = np.array(y_train, copy=True)
    rng.shuffle(shuffled)
    return shuffled
