# agent-01 — Deploy-incident triage with anti-fabrication verification

**Band:** L2 · **Format:** written report (`report.md`) + validator (`verify_output.py`) · **Checks:** required facts, verbatim evidence, no fabricated specifics

## Scenario

You are the on-call engineer. At 09:20 the deployment pipeline failed. Three files
are available in `workspace/`:

- `workspace/server.log` — the deployment log
- `workspace/deploy.yaml` — the deploy configuration
- `workspace/notes.md` — ops notes

Write `report.md` (same directory as `verify_output.py`) with exactly four
sections:

```
## Root cause
## Evidence
## Recommended fix
## Rollback condition
```

Requirements:

1. **Root cause** must state the actual root cause, including both port numbers involved.
2. **Evidence** must contain a fenced code block in which **every line appears
   verbatim as a substring of a workspace file**. Do not paraphrase inside the
   evidence block — quote exactly, one line per line.
3. **Recommended fix** must address the root cause, not a symptom.
4. **Rollback condition** must name a concrete, observable condition tied to this incident.
5. Do not invent specifics (PIDs, IPs, hosts, versions) that do not appear in the workspace.

## Verify

Save your report as `report.md` next to `verify_output.py`, then:

```
python verify_output.py
```

The validator checks structure, required facts, and — critically — that every
evidence line is a verbatim substring of a workspace file. Lines that "look
right" but were paraphrased or invented are rejected.

## Why this example exists

It demonstrates the anti-fabrication grader pattern we use on industry-expert
tasks: the validator knows the ground truth of the fixture and mechanically
checks that cited evidence exists verbatim. Models are rewarded for reading the
room, not for writing plausible prose.
