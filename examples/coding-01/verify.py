#!/usr/bin/env python3
"""Verifier for coding-01 (TopKCounter).

Grades the submission at examples/coding-01/submission.py: fixed assertions
plus a seeded randomized differential test against a naive oracle. The weak
(seeded) random source is intentional — differential tests must be
deterministic so failures are reproducible; nothing here is cryptographic.

Usage: python verify.py
Exit codes: 0 = ACCEPT, 1 = REJECT.
"""
import importlib
import random
import sys
import traceback

SUBMISSION_MODULE = "submission"


def load_submission():
    try:
        return importlib.import_module(SUBMISSION_MODULE)
    except ImportError:
        print("REJECT: submission.py not found next to verify.py "
              "(save your implementation as submission.py)")
        sys.exit(1)
    except Exception:
        print("REJECT: submission failed to import:")
        traceback.print_exc()
        sys.exit(1)


def check(cond, msg):
    if not cond:
        print(f"REJECT: {msg}")
        sys.exit(1)


def oracle_topk(counts, k):
    """Naive reference: plain dict, sort by (-count, item)."""
    items = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:k]
    return [name for name, _ in items]


def main():
    mod = load_submission()
    TopKCounter = getattr(mod, "TopKCounter", None)
    check(TopKCounter is not None, "TopKCounter class not found")

    # --- fixed assertions -------------------------------------------------
    c = TopKCounter(3)
    check(c.top_k() == [], "top_k on empty counter must be []")
    c.add("b")
    c.add("b")
    c.add("a")
    check(c.top_k() == ["b", "a"], "counts 2,1 -> ['b','a']")
    c.add("a")
    c.add("a")
    check(c.top_k() == ["a", "b"], "counts 3,2 -> ['a','b']")
    c.add("c")
    check(c.top_k() == ["a", "b", "c"], "must cap at k=3")

    try:
        TopKCounter(0)
        check(False, "k<=0 must raise ValueError")
    except ValueError:
        pass

    # merge semantics: m1 {x:2}, m2 {x:1, y:2}; merged {x:3, y:2}
    m1 = TopKCounter(2)
    m1.add("x")
    m1.add("x")
    m2 = TopKCounter(2)
    m2.add("x")
    m2.add("y")
    m2.add("y")
    m1.merge(m2)
    check(m1.top_k() == ["x", "y"], "merged counts x=3, y=2 -> ['x','y']")
    check(m2.top_k() == ["y", "x"], "merge must leave `other` unchanged (m2 keeps x=1, y=2)")

    # --- randomized differential test ------------------------------------
    vocab = [f"item_{i:02d}" for i in range(12)]
    for case in range(200):
        r = random.Random(1000 + case)
        k = r.randint(1, 5)
        a = TopKCounter(k)
        b = TopKCounter(k)
        items_a = [r.choice(vocab) for _ in range(r.randint(0, 40))]
        items_b = [r.choice(vocab) for _ in range(r.randint(0, 40))]
        for it in items_a:
            a.add(it)
        for it in items_b:
            b.add(it)
        merged = TopKCounter(k)
        merged.merge(a)
        merged.merge(b)
        exp = {}
        for it in items_a + items_b:
            exp[it] = exp.get(it, 0) + 1
        got = merged.top_k()
        want = oracle_topk(exp, k)
        check(got == want, f"differential case {case}: got {got}, want {want}")

    print("ACCEPT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
