from css.surprisal.gpt2_surprisal import _collect_key_spans, _overlap


def test_overlap() -> None:
    assert _overlap(0, 2, 1, 3)
    assert not _overlap(0, 1, 1, 2)


def test_collect_key_spans() -> None:
    row = {"edited_spans": {"s": [{"char_start": 4, "char_end": 8}]}}
    assert _collect_key_spans(row, "s") == [(4, 8)]
