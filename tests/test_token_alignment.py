from css.representations.token_alignment import align_words_exact, positional_fallback


def test_align_words_exact() -> None:
    a = ["the", "chef", "praised", "the", "waiter"]
    b = ["the", "waiter", "praised", "the", "chef"]
    pairs = align_words_exact(a, b)
    assert len(pairs) >= 3


def test_positional_fallback() -> None:
    pairs = positional_fallback(["a", "b"], ["x", "y", "z"])
    assert pairs == [(0, 0), (1, 1)]
