# coding-01 — TopKCounter with deterministic tie-breaking

**Band:** L1–L2 · **Format:** Python module · **Verifier:** `verify.py` (fixed assertions + seeded randomized cross-check against a naive oracle)

## Task

Implement `topk.py` exposing:

```python
class TopKCounter:
    def __init__(self, k: int): ...
    def add(self, item: str) -> None: ...
    def top_k(self) -> list[str]: ...
    def merge(self, other: "TopKCounter") -> None: ...
```

Semantics:

- `add(item)` records one occurrence.
- `top_k()` returns the up-to-`k` most frequent items, ties broken by ascending lexicographic order.
- `merge(other)` absorbs `other`'s counts into `self` and leaves `other` unchanged.
- `k <= 0` must raise `ValueError`.

Implement it **from scratch** — no `collections.Counter.most_common`, no external libraries beyond the standard library.

## Verify

Save your implementation as `submission.py` next to `verify.py`, then:

```
python verify.py
```

The verifier imports your module and runs:

1. fixed assertions (empty counter, ties, merge semantics, k<=0 rejection);
2. a seeded randomized differential test (200 cases) against a naive oracle built on plain dicts.

Prints `ACCEPT` or `REJECT` with the first failing case. Python 3.9+.

## Rubric

See [rubric.md](rubric.md).

## Why this example exists

It shows how we grade small engineering tasks: a fixed assertion set for known corner cases, plus a randomized differential test against an oracle written in a deliberately different style. Differential testing catches solutions that pass hand-written cases by accident.
