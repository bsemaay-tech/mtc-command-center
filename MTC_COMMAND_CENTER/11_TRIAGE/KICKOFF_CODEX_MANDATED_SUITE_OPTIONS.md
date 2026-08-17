# KICKOFF — Codex: the mandated-suite decision (P10-10), options for the owner

You are Codex, ANALYST. Working dir `C:\LAB\Tradingview_LAB_CLEAN`. No host, no network, no
commit, no block-byte edits, **and do not run the test suite**. Write exactly ONE new file:
`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_MANDATED_SUITE_OPTIONS_2026-08-12.md`.
Never git checkout/reset/stash.

## Why this is the highest-value open item
`AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md` found five Audit-2 components with **no producing
step**. Four are technical, and **three of them cascade from one**: `P10-10`, the mandated-suite
definition. `P10-11` (the frozen-SHA execution record) cannot be specified while the command is
unchosen, and `P10-12` (the accepted anomaly register) cannot be adjudicated without a baseline.

**P10-10 is a decision, not a document.** This kickoff prepares that decision for the owner. It
does **not** make it, and it does not run anything.

## What P10-10 must eventually contain
Per `AUDIT2_AUDITOR_SESSION_INPUTS.md:82-100`: `MANDATED_COMMAND`, `EXPECTED_EXIT_CODE`,
pass/fail counts, every accepted-failure test ID and output signature, skip/xfail counts, and
`BASELINE_SOURCE` at the frozen SHA.

## What to produce

1. **What test surfaces actually exist in this repo.** Enumerate them from the bytes — test
   directories, runner configuration, CI definitions, any documented suite command in
   `AGENTS.md`, README files, or prior handoffs. For each: where it lives, how it is invoked, and
   roughly what it covers. Cite `file:line`. Do not run any of them.
2. **The historical anchor, treated carefully.** Older records mention a baseline including "two
   permitted `test_order_state.py` gc-referent failures" and a `1359 passed` suite run. Locate
   every such historical claim, state its source and date, and assess whether it can serve as a
   `BASELINE_SOURCE` today or whether it is stale. **The refreshed package expressly forbids
   inferring the old two-failure example as current** — so treat these as history to be
   adjudicated, never as the answer.
3. **Options, with honest trade-offs.** Give the owner 2–4 concrete choices for what the mandated
   suite should be — e.g. the full repository suite, a scoped subset bound to WP-I's touched
   surfaces, or a named CI configuration. For each: what it would prove, what it would miss, how
   long it plausibly takes, how stable its pass set is likely to be, and what makes its
   `EXPECTED_EXIT_CODE` and anomaly set determinable.
4. **The anomaly-set requirement, stated as a gate.** Whatever is chosen, an empty anomaly set
   must be an **observed and adjudicated** result, never a hardcoded count — this is the same
   defect class as RP6's `dynamic_targets=0` literal found today. Say concretely what procedure
   would make the anomaly set *observed*.
5. **A Lead recommendation** with the reason in one paragraph, and an explicit statement of what
   the owner is actually being asked to decide.

## Rules
- **Do not execute the suite or any test.** This is a scoping and options document; a run needs
  its own authorization and its own recorded conditions.
- Every claim carries `file:line`.
- If a candidate surface cannot be assessed without running it, say so rather than guessing at
  counts. Guessed counts are exactly what P10-12 forbids.
- Do not write the P10-10 record itself. Options only.

Print the candidate surfaces found, the historical baseline claims located, and the recommended
option.
