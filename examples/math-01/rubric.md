# Rubric — math-01

| Item | Must pass | Weight |
|---|---|---|
| Format | `answer.json` parses; exactly keys `count`, `sum`; both exact integers | Must pass — otherwise score 0 |
| Count | equals independently derived number of idempotents (2^k for k distinct prime factors) | Must pass |
| Sum | equals independently derived total | Must pass |

## Partial credit

None. The answer is two integers; a wrong value is a wrong value. This mirrors how our
delivery graders treat exact-answer tasks.

## Known failure modes we check for

- Solver brute-forces `x` in `[0, n)` and hits floating-point or modulo bugs on the
  `11^3` component — accepted only if the final integers are right; method is free.
- Answer stored as string or float (`32.0`) — rejected by format rule, by design.
