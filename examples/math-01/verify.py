#!/usr/bin/env python3
"""Independent verifier for math-01 (idempotent residues mod a composite).

The expected answer is NOT stored here. It is re-derived via CRT construction
over prime-power components: each maximal prime-power factor p^k contributes
exactly two local idempotents (0 and 1), and every global idempotent is a CRT
combination of one local choice per prime power. We enumerate those combinations
and compare against the reported values.

Usage: python verify.py < answer.json
Exit codes: 0 = ACCEPT, 1 = REJECT.
"""
import json
import sys

PRIME_POWERS = [2 ** 5, 3 ** 2, 5, 7, 11 ** 3]


def crt_combine(residues, moduli):
    """Combine x_i ≡ r_i (mod m_i) for pairwise-coprime moduli."""
    x, M = 0, 1
    for r, m in zip(residues, moduli):
        t = ((r - x) % m) * pow(M, -1, m) % m
        x += M * t
        M *= m
    return x, M


def derive():
    """Return (count, sum) of idempotents mod n, derived independently."""
    k = len(PRIME_POWERS)
    total, s = 0, 0
    for mask in range(1 << k):
        c = tuple((mask >> i) & 1 for i in range(k))
        x, n = crt_combine(c, PRIME_POWERS)
        total += 1
        s += x
    return total, s, n


def main():
    raw = sys.stdin.read()
    try:
        ans = json.loads(raw)
    except Exception as e:
        print(f"REJECT: answer is not valid JSON ({e})")
        return 1

    if not isinstance(ans, dict) or set(ans) != {"count", "sum"}:
        print("REJECT: answer must be a JSON object with exactly keys 'count' and 'sum'")
        return 1
    for key in ("count", "sum"):
        if not isinstance(ans[key], int) or isinstance(ans[key], bool):
            print(f"REJECT: '{key}' must be an exact integer")
            return 1

    count, total_sum, n = derive()
    if ans["count"] != count:
        print(f"REJECT: count mismatch (got {ans['count']}, derived {count})")
        return 1
    if ans["sum"] != total_sum:
        print(f"REJECT: sum mismatch (got {ans['sum']}, derived {total_sum})")
        return 1
    print(f"ACCEPT  (n = {n}, count = {count}, sum = {total_sum})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
