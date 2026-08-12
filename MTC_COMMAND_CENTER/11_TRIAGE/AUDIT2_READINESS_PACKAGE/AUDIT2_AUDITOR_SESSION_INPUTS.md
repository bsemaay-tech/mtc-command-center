# Audit 2 auditor session inputs

Status: prepared template; NOT READY FOR DISPATCH. [refreshed 2026-08-12]

[refreshed 2026-08-12] Do not dispatch until every freeze prerequisite is satisfied
and every placeholder or blocker below is resolved from one authoritative frozen-SHA
bundle.

## 1. Required independent sessions

[refreshed 2026-08-12] Audit 2 is T0 and uses exactly these two required sessions:

1. Fresh Claude `claude-opus-5`, effort `xhigh`.
2. Fresh Codex `gpt-5.6-sol`, effort `xhigh`.

[refreshed 2026-08-12] Do not use `--resume` or `--continue`. Do not provide either
auditor with the other auditor's response, verdict, reasoning, or findings before both
initial verdicts are sealed. Do not provide implementer-session context.

[refreshed 2026-08-12] GLM is neither an open dispatcher choice nor an automatic third
auditor. The permanent tier policy fixes the Audit 2 roster above. Only a later explicit
owner contract may designate a broader review.

## 2. Scope contract

[refreshed 2026-08-12] Audit 2 accepts or rejects only the Linux-port and staging
acceptance evidence for an already frozen pre-WP-A artifact at the exact frozen SHA. It
checks:

- frozen source, candidate, artifact, manifest, and evidence identity;
- WP-L Phase 2 closure and preserved open/BLOCKED items;
- WP-I staging-verification closure, including rows 1-24 and the final successor;
- transport chain of custody, preregistration ordering, RUNID accounting, and hashes;
- the mandated-suite result and its exact accepted anomaly set;
- D026 RED/GREEN evidence for every new test offered as closure evidence;
- authority, budget, ordering, and Stage-1/final-freeze compliance; and
- the accepted section 10.1 access grammar plus the composite section 10.2 proof.

[refreshed 2026-08-12] Audit 2 does not implement or repair any artifact, contact or
mutate a host, authorize credentials or economic action, accept an open item by inference,
begin WP-A, create either freeze, or rely on an implementer transcript or prior auditor
session.

## 3. Frozen input bundle for each session

[refreshed 2026-08-12] Each session receives only the frozen scope contract, frozen
plan if adopted, actual diff and files at the frozen SHA, test/evidence package, this
readiness package, and required repository rules. Replace every placeholder below at
dispatch.

| Input | Dispatch-time value |
|---|---|
| Full frozen SHA | `NOT-YET-AVAILABLE` [refreshed 2026-08-12] |
| Base SHA and exact base-to-freeze diff | `NOT-YET-AVAILABLE` [refreshed 2026-08-12] |
| Frozen file list | `NOT-YET-AVAILABLE` [refreshed 2026-08-12] |
| Candidate identity | [refreshed 2026-08-12] Current candidate anchor is `2ce41e34bceb599d80af24c5c33d835820ec321b`; final artifact and manifest hashes must be recomputed at freeze. |
| WP-L Phase 2 closure record | `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\UNIT_CLOSURE_RECORD.md` [refreshed 2026-08-12] |
| WP-L Phase 2 evidence index | `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\EVIDENCE_INDEX.md` [refreshed 2026-08-12] |
| Current non-final WP-I artifacts | [refreshed 2026-08-12] `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPI_BLOCKS_DRAFT\` and `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\`; see `AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md`. These known paths are not a closure record. |
| Final WP-I closure and evidence index | `NOT-YET-AVAILABLE` [refreshed 2026-08-12] |
| Freeze-time ledger source | `NOT-YET-AVAILABLE` [refreshed 2026-08-12] |
| Current acceptance matrix | `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\AUDIT2_READINESS_PACKAGE\AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md` [refreshed 2026-08-12] |
| D026 RED-location register | `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\AUDIT2_READINESS_PACKAGE\AUDIT2_D026_RED_LOCATIONS.md` [refreshed 2026-08-12] |

## 4. Isolated-worktree contract

[refreshed 2026-08-12] For each flagship auditor:

1. Create a separate audit-only worktree at the exact full frozen SHA. Do not reuse the
   implementer's or the other auditor's worktree.
2. Record `git rev-parse HEAD` and require exact equality with the frozen SHA.
3. Record `git status --porcelain` and require empty output before review.
4. Run the mandated suite and allowed evidence-reproduction commands only in that
   isolated worktree or against explicitly handed immutable evidence roots.
5. Do not edit source or evidence.
6. Record `git status --porcelain` again after review and require empty output.
7. Attach both cleanliness outputs and the resolved worktree path to the verdict.

[refreshed 2026-08-12] If the SHA differs or either cleanliness proof is non-empty,
return BLOCK.

## 5. Mandated test suite and baseline

[refreshed 2026-08-12] DISPATCH BLOCKER: the authoritative command, test IDs, exact
counts, output signatures, and frozen-SHA baseline are wholly unresolved. The earlier
description of two `test_order_state.py` gc-referent failures is not an accepted current
baseline and must not be repeated as one.

Before dispatch, fill and freeze all fields below from one authoritative source:

```text
MANDATED_COMMAND=<exact command>
EXPECTED_EXIT_CODE=<exact integer>
EXPECTED_PASS_COUNT=<exact integer>
EXPECTED_FAIL_COUNT=<exact integer>
EXPECTED_FAILURE_1=<exact test id and accepted output/signature, if any>
EXPECTED_FAILURE_2=<exact test id and accepted output/signature, if any>
EXPECTED_SKIP_XFAIL_COUNTS=<exact values>
BASELINE_SOURCE=<exact path at frozen SHA>
```

[refreshed 2026-08-12] No auditor may choose a substitute command or infer the anomaly
set. Each required auditor must execute the mandated suite. Inability to execute requires
BLOCK; non-execution is not acceptance.

## 6. D026 instructions

[refreshed 2026-08-12] For every new test offered as proof that a named defect is
closed, the auditor must locate and reproduce the exact RED command/output against the
pre-fix behavior or an equivalent mutation, restore the accepted implementation, reproduce
GREEN, and state whether both arms were verified. If neither safe reversion nor an
independent falsification exists, the test is supplemental rather than closure evidence.

[refreshed 2026-08-12] The corrected WP-L/B3 locations and the explicitly incomplete
current WP-I map are in `AUDIT2_D026_RED_LOCATIONS.md`. A current audit RED without a
repaired and finally accepted GREEN remains open.

## 7. Required verdict output

[refreshed 2026-08-12] Each session returns exactly one verdict: PASS,
PASS-WITH-NITS, REQUEST_CHANGES, or BLOCK. PASS-WITH-NITS may contain optional nits only.
Each required finding must identify the exact file, observed and expected behavior, and a
reproducible command or comparison. The dispatching Lead independently reproduces each
required finding and records any unreproduced finding with evidence rather than dropping it.
