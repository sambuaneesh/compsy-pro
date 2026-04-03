from __future__ import annotations

import re
from collections import Counter


def simple_word_spans(text: str) -> list[tuple[str, int, int]]:
    return [(m.group(0), m.start(), m.end()) for m in re.finditer(r"\S+", text)]


def lexical_jaccard(s1: str, s2: str) -> float:
    w1 = set(t.lower() for t, _, _ in simple_word_spans(s1))
    w2 = set(t.lower() for t, _, _ in simple_word_spans(s2))
    if not w1 and not w2:
        return 1.0
    return len(w1 & w2) / len(w1 | w2)


def levenshtein_distance(a: str, b: str) -> int:
    if a == b:
        return 0
    if len(a) < len(b):
        a, b = b, a
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        cur = [i]
        for j, cb in enumerate(b, start=1):
            ins = cur[j - 1] + 1
            dele = prev[j] + 1
            sub = prev[j - 1] + (ca != cb)
            cur.append(min(ins, dele, sub))
        prev = cur
    return prev[-1]


def token_len(text: str) -> int:
    return len(simple_word_spans(text))


def find_span_or_raise(text: str, token: str, label: str) -> dict[str, int | str]:
    idx = text.lower().find(token.lower())
    if idx < 0:
        raise ValueError(f"Token '{token}' not found for label '{label}' in: {text}")
    return {"label": label, "text": token, "char_start": idx, "char_end": idx + len(token)}


def deterministic_choice_counts(words: list[str]) -> dict[str, int]:
    return dict(Counter(words))
