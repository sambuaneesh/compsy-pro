from __future__ import annotations

from collections import defaultdict


def align_words_exact(words_a: list[str], words_b: list[str]) -> list[tuple[int, int]]:
    buckets: dict[str, list[int]] = defaultdict(list)
    for j, w in enumerate(words_b):
        buckets[w.lower()].append(j)

    used_b: set[int] = set()
    alignments: list[tuple[int, int]] = []

    for i, w in enumerate(words_a):
        candidates = buckets.get(w.lower(), [])
        chosen = next((j for j in candidates if j not in used_b), None)
        if chosen is not None:
            used_b.add(chosen)
            alignments.append((i, chosen))

    return alignments


def positional_fallback(words_a: list[str], words_b: list[str]) -> list[tuple[int, int]]:
    n = min(len(words_a), len(words_b))
    return [(i, i) for i in range(n)]
