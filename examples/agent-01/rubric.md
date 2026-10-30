# Rubric — agent-01

| Item | Must pass | Weight |
|---|---|---|
| Structure | four sections present, in order | Must pass |
| Root cause | names the configured-vs-actual port pair (5433 vs 5432) | Must pass |
| Evidence | fenced block; every line verbatim from a workspace file; ≥2 lines | Must pass |
| Fix | addresses the config value, not a symptom (e.g., not "retry more") | Must pass |
| Rollback | concrete observable condition referencing port 5432 | Must pass |
| No fabrication | does not blame the unrelated disk warning; no invented PIDs/IPs | Must pass |

## Grader notes

The mechanical checks live in `verify_output.py`. Human/LLM review adds only the
two judgement calls the validator cannot make: whether the fix addresses the
cause, and whether the rollback condition is operationally sane.

## Common failure modes observed with this fixture family

- Paraphrased evidence ("the app tried 5433 three times" instead of quoting the
  log line) — rejected by the verbatim rule.
- Root cause blamed on the red-herring warning (71% disk) — the fixture includes
  it deliberately, to reward actual cross-file reasoning (notes.md contradicts
  deploy.yaml, server.log confirms).
- Rollback conditions like "monitor and see" — rejected as non-concrete.
