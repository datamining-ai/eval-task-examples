# Delivery notes — coding data lines (public summary)

Official delivery statements for our three coding data lines, with model-in-the-loop measurements under a uniform budget. Numbers on this page come from our internal acceptance runs; caveats in [Frontier Task Difficulty Report 2026](https://www.datamining.cloud/en/reports/frontier-task-difficulty-2026.html) apply.

**Uniform budget:** GPT-5.6 Sol (xhigh reasoning tier), 4 valid attempts per task, same execution environment and grading as delivery acceptance.

## DeepSWE

Evaluates coding agents on bug repair, feature extension, and algorithm implementation in real open-source repositories.

- Delivered: 5 example task packages, each with a full repository baseline, task brief, reference implementation, private tests, and execution traces.
- Under the uniform budget: every task was solved at most 2 of 4 attempts; **3 of 5 tasks were solved zero times**.

## Frontier SWE

Evaluates coding agents on engineering problems: concurrent resource management, complex business data flows, persistent storage.

- Delivered: 4 examples with full evaluation materials.
- Under the uniform budget: every task was solved at most 2 of 4 attempts; **1 task was solved zero times**.

## ProgramBench

Evaluates coding agents on rebuilding a complete command-line program from public documentation and restricted black-box queries.

- Delivered: 3 examples, 515 test inputs in total, with reference programs, hidden scoring, coverage evidence, and environment-restore materials.
- Engineering validation and candidate regression completed on all three.
- Under the uniform budget: every task was solved at most 2 of 4 attempts.

## What a task package looks like

See `examples/deepswe-01-rustworkx/` for the **public view** of one real DeepSWE task (instruction + manifest). A full package additionally contains the parts we never publish, because publishing them would destroy the task's evaluation value:

```
deep_rustworkx_simple_gnm/
  instruction.md            # shown to the model          (public below)
  task.toml                 # task metadata               (public below)
  environment/              # Dockerfile, baseline repo, workspace seed
  tests/                    # private contract tests + hidden head tests
  solution/                 # golden patch + solve script
  validation.json           # acceptance validation record
```

## Contact

- Website: <https://www.datamining.cloud>
- Email: <contact@datamining.cloud>
- Report: [Frontier Task Difficulty Report 2026](https://www.datamining.cloud/en/reports/frontier-task-difficulty-2026.html)
