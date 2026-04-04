import numpy as np

from css.metrics.matrix_norms import frobenius_shift, frobenius_similarity


def test_frobenius_similarity_identity() -> None:
    a = np.array([[1.0, 0.0], [0.0, 1.0]], dtype=np.float32)
    sim = frobenius_similarity(a, a)
    assert 0.99 <= sim <= 1.01


def test_frobenius_shift_range() -> None:
    a = np.array([[1.0, 0.0], [0.0, 1.0]], dtype=np.float32)
    b = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=np.float32)
    sim, delta = frobenius_shift(a, b)
    assert 0.0 <= sim <= 1.1
    assert -0.1 <= delta <= 1.1
