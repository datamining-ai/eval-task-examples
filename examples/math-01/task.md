# math-01 — Idempotent residues modulo a composite

**Band:** L2 · **Format:** single-number answer, JSON file · **Verifier:** `verify.py` (independent recomputation — the expected answer is *not stored anywhere*)

## Task

Let

```
n = 2^5 · 3^2 · 5 · 7 · 11^3
```

An integer `x` with `0 ≤ x < n` is called **idempotent mod n** when `x² ≡ x (mod n)`.

Write a file `answer.json` containing exactly two keys:

```json
{"count": <how many idempotents exist in [0, n)>, "sum": <their sum>}
```

Rules:

- Report exact integers. No other keys, no commentary in the file.
- You may use any correct method; the verifier does **not** contain a stored answer — it re-derives the expected values through an independent route (CRT construction over prime-power components) and compares.

## Try it

```
python verify.py < answer.json
```

`verify.py` prints `ACCEPT` or `REJECT` with the first mismatching field, and the derived ground truth on ACCEPT. Reference runtime: well under one second (the verifier never brute-forces all n residues).

## Rubric

See [rubric.md](rubric.md). What the verifier checks:

1. File parses as JSON with exactly the keys `count` and `sum`.
2. `count` equals the independently derived number of idempotents.
3. `sum` equals the independently derived total.
4. Both are exact integers (no floats, no strings).

## Why this example exists

It demonstrates our verification philosophy: a grader that re-derives the ground truth by a *different algorithm* than any reasonable solver would use. Storing the expected answer inside the verifier invites answer-extraction and reward hacking; recomputing it makes the verifier the strongest part of the package.
