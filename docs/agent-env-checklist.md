# Design checklist for RL / agent evaluation environments

How we design and review every agent environment we deliver. Public summary of
our internal checklist — the same review we run before a package ships.

## 1. Task definition

- [ ] **Initial state** is fully specified: seed data, filesystem image, running
      services — everything the agent will see at step 0.
- [ ] **Goal condition** is externally checkable: a final state (files written,
      records updated, services configured) rather than a vibe.
- [ ] **Constraints** (deadline, budget, allowed tools) are stated in the
      instruction, not implied.

## 2. Determinism & reproducibility

- [ ] The environment rebuilds from a committed definition (Dockerfile / VM image
      manifest); nothing depends on undocumented host state.
- [ ] The agent runs `network_mode = no-network` unless the task explicitly needs
      live resources; the verifier states its own `network_mode`.
- [ ] A fresh checkout can reset the environment to step 0 (reset/replay is
      possible).

## 3. Verifier design

- [ ] The verifier checks **outcomes** (files, records, service state), not prose.
- [ ] Where the answer space allows gaming, the verifier **re-derives** the ground
      truth instead of storing it (see `examples/math-01`).
- [ ] Contract tests are **binary**; partial credit is reserved for rubrics with
      explicitly weighted dimensions.
- [ ] Cited evidence is checked **verbatim** against the workspace
      (see `examples/agent-01`) — paraphrase and fabrication are rejected.
- [ ] The verifier has been tested against a **known-wrong solution** and a
      **reward-hacking solution**, not only the golden path.

## 4. Anti-reward-hacking review

- [ ] "Solve by editing the tests" is impossible: tests/verifier is read-only
      from the agent's mount.
- [ ] Red herrings are planted deliberately (unrelated warnings, stale configs)
      and the rubric penalizes blaming them.
- [ ] Sensitive side effects (external calls, destructive ops) are impossible by
      sandboxing, not by instruction.

## 5. Difficulty & acceptance

- [ ] The task is graded to a difficulty band (L1/L2/L3) before delivery.
- [ ] Acceptance measurement uses a **uniform budget** (fixed model tier, attempt
      count, tool access) recorded with the delivery, so the number has a口径.
- [ ] Failure trajectories are kept as evidence for the delivery review.

## 6. Packaging

```
<task>/
  instruction.md            # what the model sees
  manifest (task.toml)      # metadata, budgets, network modes
  environment/              # deterministic rebuild definition
  tests/ or verify_output   # private or public verifier
  solution/                 # golden path (private)
  validation.json           # acceptance record
```

Consistent packaging is what lets a reviewer reproduce the whole loop: rebuild →
run → verify → compare against the acceptance record.
