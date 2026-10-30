# Rubric — coding-01

| Item | Must pass | Weight |
|---|---|---|
| API surface | `TopKCounter(k)` / `add` / `top_k` / `merge` all present and callable | Must pass |
| Ordering | `top_k` = count desc, ties lexicographic ascending | Must pass |
| Cap | at most `k` items returned | Must pass |
| `k <= 0` | raises `ValueError` | Must pass |
| Merge | absorbs counts; `other` unchanged after merge | Must pass |
| Differential | 200 seeded cases match the naive oracle | Must pass |

## Scoring

Binary. Any failed case → REJECT. This mirrors our delivery grading: contract
tests are pass/fail; there is no partial credit for "almost correct" tie-breaking,
because downstream RL training consumes the failure as a wrong signal.

## Why binary + differential

Hand-written corner cases are guessable; the seeded differential run is not.
Together they reject solutions that hard-code the visible cases — an early,
cheap reward-hacking check.
