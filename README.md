# eval-task-examples

Example evaluation tasks and verification harnesses from [DataMining](https://www.datamining.cloud) — original tasks designed for frontier models and agents.

DataMining builds original, expert-authored task data for training and evaluating frontier models and agents: coding, complex reasoning, multimodal, and agent capability lines. Founded by PhD researchers from the School of Software, Peking University; delivered to leading technology companies including ByteDance, Alibaba, and Tencent.

## What this repository is

A small, self-contained showcase of **how our tasks are structured and verified** — not a dump of our commercial dataset. Every example here:

- is **originally authored** for this repository (never scraped or recycled),
- ships with a **runnable verification script** (the same philosophy as our delivery format: executable, reproducible, no human grading),
- includes a **rubric** describing what a correct solution must satisfy.

## Contents

```
examples/
  math-01/     number-theory problem + verification + rubric
  coding-01/   small engineering task + unit tests + grading script
  agent-01/    tool-orchestration task + output validator + rubric
docs/
  agent-env-checklist.md    design checklist for RL/agent environments (anti-reward-hacking)
  task-authoring-guide.md   how we author and contamination-check tasks
```

Run any verifier with Python 3.9+:

```
python examples/math-01/verify.py
python examples/coding-01/verify.py
python examples/agent-01/verify.py
```

## What we actually deliver

Commercial deliveries are far larger and harder than these examples — for scale and difficulty bands see the [delivered datasets overview](https://www.datamining.cloud/en/datasets/) and the [Frontier Task Difficulty Report 2026](https://www.datamining.cloud/en/reports/frontier-task-difficulty-2026.html).

- **Coding**: repository-level SWE tasks, algorithmic engineering (aligned with Frontier SWE / Deep SWE / Frontier-Eng / ALE-Bench difficulty bands)
- **Reasoning**: expert-level math, physics, chemistry (HLE-style, L3 band)
- **Agents**: long-horizon tool-use and desktop automation (APEX Agents / ALE / Toolathlon style)
- **Multimodal**: figure- and screen-grounded reasoning (HLE-VL style)

## Contact

- Website: https://www.datamining.cloud
- Email: contact@datamining.cloud

## License

MIT — see [LICENSE](LICENSE). The task format is ours to keep improving; you are welcome to adapt the structure for your own evaluation pipelines.
