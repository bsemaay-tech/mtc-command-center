# Audit 2 auditor session inputs

Status: prepared template. Do not dispatch until every freeze prerequisite is satisfied
and every placeholder or blocker below is resolved.

## 1. Required independent sessions

Run two fresh, independent flagship sessions against the same frozen SHA:

1. Claude `claude-opus-5`, effort `xhigh`.
2. Codex `gpt-5.6-sol`, effort `xhigh`.

Do not use `--resume` or `--continue`. Do not provide either auditor with the other
auditor's prompt response, verdict, reasoning, or findings before both initial verdicts
are sealed. Do not provide implementer-session context.

The unresolved GLM-5.2 supplemental-versus-omitted decision is recorded in
`OPEN_QUESTIONS_FOR_DISPATCHER.md`. It does not change the two-flagship acceptance floor.

## 2. Scope contract

Audit 2 accepts or rejects only the Linux-port and staging acceptance evidence for the
frozen pre-WP-A artifact at the exact freeze SHA. It checks:

- frozen source, candidate, artifact, and manifest identity;
- WP-L Phase 2 closure and preserved open/BLOCKED items;
- WP-I staging-verification closure;
- transport chain of custody, preregistration ordering, RUNID accounting, and hashes;
- the mandated suite result and its accepted anomaly set;
- D026 RED/GREEN evidence for every new test offered as closure evidence;
- authority, budget, and sequencing compliance.

Audit 2 does not:

- implement or repair code, scripts, tests, or documentation;
- contact or mutate a staging or production host;
- authorize credentials, ARM, orders, broker/exchange contact, TESTNET/mainnet, deployment,
  master merge, WP-V/KVM2, or any economic action;
- accept an open or BLOCKED item by inference;
- begin or authorize WP-A;
- rely on an implementer transcript or a prior auditor session.

## 3. Frozen input bundle for each session

Each session must receive only the frozen scope contract, frozen plan if one is adopted,
actual diff and files at the frozen SHA, test evidence, this readiness package, and the
required repository rules. At dispatch, replace every placeholder below with an exact
path or full value:

| Input | Dispatch-time value |
|---|---|
| Full frozen SHA | `PRODUCED-AT-FREEZE` |
| Base SHA and exact base-to-freeze diff | `PRODUCED-AT-FREEZE` |
| Frozen file list | `PRODUCED-AT-FREEZE` |
| Candidate identity | `2ce41e34bceb599d80af24c5c33d835820ec321b` plus recomputed artifact/manifest hashes |
| WP-L Phase 2 closure record | `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\UNIT_CLOSURE_RECORD.md` |
| WP-L Phase 2 evidence index | `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\EVIDENCE_INDEX.md` |
| WP-I closure and evidence index | `BLOCKED-UPSTREAM: no exact paths recorded in the permitted inputs` |
| Freeze-time ledger source | `PRODUCED-AT-FREEZE` |
| D026 RED-location register | `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\AUDIT2_READINESS_PACKAGE\AUDIT2_D026_RED_LOCATIONS.md` |

## 4. Isolated-worktree contract

For each flagship auditor:

1. Create a separate audit-only worktree at the exact full frozen SHA. Do not reuse the
   implementer's worktree or the other auditor's worktree.
2. Before review, record `git rev-parse HEAD` and require it to equal the frozen SHA.
3. Before review, record `git status --porcelain` and require empty output.
4. Run the mandated suite and all allowed evidence-reproduction commands only in that
   isolated worktree or against explicitly handed immutable evidence roots.
5. Do not edit source or evidence.
6. After review, record `git status --porcelain` again and require empty output.
7. Attach both cleanliness outputs and the resolved worktree path to the verdict artifact.

If the SHA differs or either cleanliness proof is non-empty, return BLOCK.

## 5. Mandated test suite and baseline

DISPATCH BLOCKER: the permitted kickoff inputs do not record the exact mandated test-suite
command. They also do not identify the exact test IDs or exact expected output for the
accepted anomaly set. The only recorded description is that the current baseline includes
two permitted `test_order_state.py` gc-referent failures.

Before dispatch, the Lead must fill and freeze all fields below from an authoritative
source:

```text
MANDATED_COMMAND=<exact command>
EXPECTED_EXIT_CODE=<exact integer>
EXPECTED_PASS_COUNT=<exact integer>
EXPECTED_FAIL_COUNT=2
EXPECTED_FAILURE_1=<exact test id and accepted output/signature>
EXPECTED_FAILURE_2=<exact test id and accepted output/signature>
EXPECTED_SKIP_XFAIL_COUNTS=<exact values>
BASELINE_SOURCE=<exact path at frozen SHA>
```

No auditor may choose a substitute command or infer the baseline. Each canonical auditor
must execute the mandated suite. An auditor unable to execute it must return BLOCK;
non-execution is not acceptance.

## 6. D026 instructions

For every new test offered as proof that a named defect is closed, the auditor must:

1. locate the exact recorded RED command and real output;
2. confirm RED was produced against the exact pre-fix behavior or an equivalent deliberate
   mutation/falsification;
3. restore the accepted implementation and confirm GREEN with the recorded command and
   real output;
4. state explicitly whether that test's RED and GREEN were verified.

If safe reversion is impractical, require an independent mutation/falsification. If neither
exists, classify the test as supplemental, not closure evidence. The current location
status is in `AUDIT2_D026_RED_LOCATIONS.md`.

## 7. Required verdict output

Each session returns exactly one verdict: PASS, PASS-WITH-NITS, REQUEST_CHANGES, or BLOCK.
PASS-WITH-NITS may contain optional nits only and no required repair. Each required finding
must include a reproducible command or comparison, the exact affected file, and observed
versus expected behavior. The dispatching Lead independently reproduces every required
finding on real source and records unreproduced findings with evidence rather than dropping
them.
