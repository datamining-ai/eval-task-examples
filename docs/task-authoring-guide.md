# Task authoring & contamination guide

How we author original tasks and screen them for contamination before delivery.
Public summary of our internal process.

## 1. Source selection & provenance

- Prefer **public, citable sources**: company filings, standards documents,
  published specs, real system behavior. Record the source per task; a task
  without provenance cannot be defended during acceptance review.
- Synthetic scenarios must be labeled as synthetic — both in the instruction
  ("explicitly simulated around genuine historical disclosures") and in the
  package metadata.
- Never carry client-confidential material into a task. If a scenario is
  inspired by delivery work, it must be rebuilt from public sources with all
  identifiers changed.

## 2. Originality & contamination screening

Before a task enters the pool:

- [ ] Search the core scenario terms plus the solution key against public
      benchmarks and repos (SWE-bench family, HumanEval/MBPP, academic sets in
      the same domain).
- [ ] Check the **solution key** specifically: if the answer is findable as a
      known constant, a famous puzzle, or a repo's actual bug — re-synthesize
      parameters until it is not.
- [ ] Keep a screening log (what was searched, what was found, what was changed).

## 3. Verifier-first authoring

Write the verifier **before** the task is finalized:

1. Decide what outcome constitutes "solved".
2. Write the mechanical check (re-derive, don't store; binary contracts;
   verbatim evidence rules — see `agent-env-checklist.md` §3).
3. Test the verifier against a known-wrong solution and a reward-hacking
   solution.
4. Only then freeze the instruction text.

## 4. Difficulty banding

Every task is graded L1 / L2 / L3 before delivery:

| Band | Meaning |
|---|---|
| L1 | Within current frontier-model capability with standard tooling |
| L2 | Solved sometimes under a uniform acceptance budget; failure modes are informative |
| L3 | At or beyond the current frontier; near-zero success under budget |

Bands are calibrated by measurement, not intuition: fixed model tier, fixed
attempt count, fixed tool access (the "uniform budget" rule from our
[delivery notes](delivery-notes-code.md)).

## 5. QA review — five dimensions

Every task passes a contradiction-style QA review before delivery:

1. **Prompt completeness** — everything needed to solve is present and unambiguous.
2. **File & identifier consistency** — names, paths, IDs match across all files.
3. **Solution correctness & derivability** — the reference solution follows from
   the materials, and every claim in it traces to a source.
4. **Cross-file consistency** — no file contradicts another; red herrings are
   deliberate and documented.
5. **Rubric quality** — gradable as written; the rubric penalizes the failure
   modes the task is designed to expose.

## 6. Acceptance measurement

- Fixed budget (model tier, attempts, tool access) recorded with the delivery.
- Report pass@k with the denominator; a task solved 2/4 is reported as 2/4, and
  never-solved counts are stated explicitly.
- Failure trajectories are archived as acceptance evidence.

## 7. What never enters a delivered package

- Client-confidential material, client names, or identifiers.
- Scraped or recycled public-benchmark items.
- Verifiers that store the answer where the solver can reach it.
