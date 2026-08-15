# Audit 2 T0 auditor kickoffs — fill only at freeze

Status: **KICKOFF TEMPLATES ONLY — DO NOT DISPATCH WITH ANY PLACEHOLDER UNRESOLVED. NO VERDICT, ACCEPTANCE, AUTHORIZATION, OR ACTION IS CREATED BY THIS FILE.** The pre-WP-A freeze does not yet exist, so its full SHA must remain `<FREEZE_SHA>` until R16/R20 supplies it. (`C:\tmp\lane_kick\X6.md:40-42`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS_FILL_2026-08-15.md:21-31`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_HANDOFF_PACKAGE.md:180-185`)

Audit 2 duration remains **NO SOURCED ESTIMATE**. Record measured actuals; do not invent or pre-allocate a duration. (`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:60`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md:150-177`)

## Placeholder inventory — resolve every token before dispatch

Every angle-bracket token used anywhere in either prompt is listed here. The dispatcher must replace every token from the stated frozen source, then verify that no `<...>` token remains. An unresolved required field is `UNKNOWN`, not an invitation to infer it. (`C:\tmp\lane_kick\X6.md:40-42`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:44-64`)

| Placeholder | State now | What fills it | Authoritative dispatch-time source |
|---|---|---|---|
| `<FREEZE_SHA>` | `UNKNOWN` | Full R16 pre-WP-A frozen checkpoint SHA | R16 freeze output as bound by the final R20 Packet-10 manifest. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS_FILL_2026-08-15.md:21`; `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:55-60`) |
| `<BASE_SHA>` | `UNKNOWN` | Full comparison-base SHA | Lead-pinned R16 comparison base. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS_FILL_2026-08-15.md:22`) |
| `<BASE_TO_FREEZE_DIFF_PATH>`, `<BASE_TO_FREEZE_DIFF_SHA256>` | `UNKNOWN` | Exact base-to-freeze patch path and SHA-256, including an explicitly recorded empty patch if applicable | R16 `R16_BASE_TO_FREEZE.patch` record and final R20 manifest. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS_FILL_2026-08-15.md:22`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md:47-53`) |
| `<FROZEN_FILE_LIST_PATH>`, `<FROZEN_FILE_LIST_SHA256>` | `UNKNOWN` | Frozen tracked-tree/file-list path and its SHA-256 | R16 frozen file-list output as bound by R20. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS_FILL_2026-08-15.md:23`; `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:55-60`) |
| `<BOUNDED_REVIEW_PATH_LIST>` | `UNKNOWN` | Exact newline-separated source/evidence paths the auditor may inspect after the named documents; no directory wildcard | Dispatcher copies the exact review-member paths from the final R20 bundle and R16 frozen file list. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md:43-55`; `C:\tmp\lane_kick\X6.md:47-48`) |
| `<CANDIDATE_COMMIT>` | `UNKNOWN` | Full integrated product-candidate commit identity | Lead-pinned candidate identity bound by R16/R20; the old candidate anchor must not be carried forward. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS_FILL_2026-08-15.md:24`) |
| `<CANDIDATE_ARTIFACT_PATH>`, `<CANDIDATE_ARTIFACT_SHA256>` | `UNKNOWN` | Final frozen candidate artifact path and recomputed SHA-256 | R16 identity records and final R20 manifest. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md:47-53`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_HANDOFF_PACKAGE.md:57-59`) |
| `<CANDIDATE_MANIFEST_PATH>`, `<CANDIDATE_MANIFEST_SHA256>` | `UNKNOWN` | Final frozen candidate manifest path and recomputed SHA-256 | R16 identity records and final R20 manifest. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md:47-53`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_HANDOFF_PACKAGE.md:57-59`) |
| `<EVIDENCE_SNAPSHOT_ROOT>`, `<EVIDENCE_SNAPSHOT_INDEX>`, `<EVIDENCE_SNAPSHOT_SHA256>` | `UNKNOWN` | Immutable read-only evidence root, its exact index, and the index SHA-256 | Final R20 bundle; copied digest strings alone are insufficient when recomputation is required. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md:45-55`) |
| `<FINAL_WPI_CLOSURE_RECORD>`, `<FINAL_WPI_EVIDENCE_INDEX>` | `UNKNOWN` | Final WP-I closure-record and evidence-index paths | Completed Packet 9/R15 outputs bound by R16/R20. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS_FILL_2026-08-15.md:28`; `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:54-60`) |
| `<FINAL_ACCEPTANCE_MATRIX>` | `UNKNOWN` | Exact-current final acceptance-matrix path | Final matrix after all pre-freeze review outcomes, bound by R20. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS_FILL_2026-08-15.md:30`) |
| `<FINAL_D026_REGISTER>` | `UNKNOWN` | Completed final D026 map/register, including rows 1-9 and exact RED/GREEN locations | Final R20 bundle after closure evidence exists. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS_FILL_2026-08-15.md:31`) |
| `<FREEZE_TIME_LEDGER_SOURCE>` | `UNKNOWN` | Owner-ratified freeze-time ledger path and exact identity | R18 recalculation plus R19 owner ratification; the 2026-08-15 snapshot does not pre-ratify the freeze-time figure. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:62-78`; `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:57-59`) |
| `<CONSOLIDATED_AUTHORITY_RECORD>` | `UNKNOWN` | Final bound Packet-11 authority/go-no-go record path and exact identity | R18/R19 Packet-11 completion as bound by R20. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS_FILL_2026-08-15.md:75-76`; `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:57-60`) |
| `<PACKET10_MANIFEST_PATH>`, `<PACKET10_MANIFEST_SHA256>` | `UNKNOWN` | One authoritative, final Packet-10 dispatch manifest path and SHA-256, identical for both auditors | R20 output after R16-R19. (`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:55-60`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS_FILL_2026-08-15.md:81`) |
| `<CLAUDE_AUDIT_WORKTREE>` | `UNKNOWN` | Absolute path of Claude's audit-only worktree at `<FREEZE_SHA>` | Dispatcher creates a worktree separate from the implementer and Codex worktrees. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:65-80`) |
| `<CODEX_AUDIT_WORKTREE>` | `UNKNOWN` | Absolute path of Codex's audit-only worktree at `<FREEZE_SHA>` | Dispatcher creates a worktree separate from the implementer and Claude worktrees. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:65-80`) |
| `<CLAUDE_P10_PYTHON>` | `UNKNOWN` | Absolute executable path of Claude session's valid locked Linux CPython 3.12 environment | R17/Packet-10 environment record for Claude's isolated execution. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS_FILL_2026-08-15.md:63-65`) |
| `<CODEX_P10_PYTHON>` | `UNKNOWN` | Absolute executable path of Codex session's valid locked Linux CPython 3.12 environment | R17/Packet-10 environment record for Codex's isolated execution. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS_FILL_2026-08-15.md:63-65`) |
| `<EXPECTED_PASS_COUNT>` | `UNKNOWN` | Exact frozen-suite pass count | R17 frozen locked-environment execution record. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS_FILL_2026-08-15.md:49-57`) |
| `<EXPECTED_SKIP_COUNT>`, `<EXPECTED_XFAIL_COUNT>` | `UNKNOWN` | Exact frozen-suite skip and xfail counts | R17 frozen locked-environment execution record. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS_FILL_2026-08-15.md:56`) |
| `<OBSERVED_ADJUDICATED_ANOMALY_SET>`, `<ANOMALY_SIGNATURES>` | `UNKNOWN` | Exact observed/adjudicated frozen anomaly set and exact signatures; write `NONE` only if R17 explicitly records none | R17 frozen execution/anomaly record; the definition expects no failures, but the observed set may not be inferred before the run. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS_FILL_2026-08-15.md:51-57`) |
| `<BASELINE_SOURCE>`, `<BASELINE_SOURCE_SHA256>` | `UNKNOWN` | Frozen suite/anomaly baseline record path and SHA-256 | R17 record as bound by R20. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS_FILL_2026-08-15.md:57`; `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:56-60`) |
| `<CONFIG_RESCAN_RECORD>` | `UNKNOWN` | Freeze-time pytest-configuration and temporary-artifact rescan record | R17/Packet-10 freeze-time rescan. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS_FILL_2026-08-15.md:65`) |
| `<CLAUDE_REPORT_PATH>` | `UNKNOWN` | The sole writable Claude report path, outside every audit worktree, with basename `AUDIT2_CLAUDE_T0_YYYY-MM-DD.md` | Dispatcher selects the output root/date at launch; the dispatch plan recommends this report name and one report per auditor. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md:61-66`) |
| `<CODEX_REPORT_PATH>` | `UNKNOWN` | The sole writable Codex report path, outside every audit worktree, with basename `AUDIT2_CODEX_T0_YYYY-MM-DD.md` | Dispatcher selects the output root/date at launch; the dispatch plan recommends this report name and one report per auditor. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md:61-66`) |

Fixed suite definitions do not need placeholders: `EXPECTED_EXIT_CODE=0`, `EXPECTED_FAIL_COUNT=0`, and the definition-level expected failures are `NONE EXPECTED`; the actual frozen observation and adjudication still come from R17. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS_FILL_2026-08-15.md:49-57`)

---

# Dispatch prompt 1 — Claude Audit 2 T0

You are the first of two independent Audit 2 T0 auditors. Use a **fresh standalone Claude `claude-opus-5` session at effort `xhigh`**, with no resume/continue and no implementer-session context. Do not receive or inspect the Codex auditor's response, reasoning, findings, or verdict until your report is sealed. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:9-22`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md:37-41`)

## Mandatory preflight — before reading or executing anything

1. Confirm the session header first: model is exactly `claude-opus-5`, effort is exactly `xhigh`, this is a fresh session, and the session can execute the mandated suite and write `<CLAUDE_REPORT_PATH>`. If any field is wrong or unavailable, stop before audit work and return `BLOCK`; exact model/effort unavailability is not a silent-fallback condition. (`C:\tmp\lane_kick\X6.md:51-54`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md:11-18`)
2. Verify that every angle-bracket placeholder in this prompt has been replaced. If one remains, record it as `UNKNOWN`, write a minimal `BLOCK` report to `<CLAUDE_REPORT_PATH>`, and stop. The freeze SHA must not be inferred. (`C:\tmp\lane_kick\X6.md:40-42`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS_FILL_2026-08-15.md:21-31`)
3. Capture the session-start monotonic reading with `<CLAUDE_P10_PYTHON> -c "import time; print(time.monotonic_ns())"` immediately after the header and placeholder checks. The session must meter monotonic start/finish and the named work phases so Audit 3/Gate 6 can be priced from actuals. (`C:\tmp\lane_kick\X6.md:43-46`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md:166-177`)
4. Create or open exactly one output file, `<CLAUDE_REPORT_PATH>`, outside the worktree. Write and flush the session-header confirmation and raw start reading before audit work; this is the write-capability proof. Write no other deliverable or repository file. Each auditor produces exactly one independent report. (`C:\tmp\lane_kick\X6.md:49-54`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md:61-66`)

## Scope and non-authority

Audit only the Linux-port and staging-acceptance evidence for the already frozen pre-WP-A artifact at full SHA `<FREEZE_SHA>`. Check frozen source/candidate/artifact/manifest/evidence identity; WP-L Phase-2 closure and preserved open/BLOCKED items; final WP-I closure including rows 1-24 and the successor; chain of custody, preregistration order, RUNIDs, and hashes; the mandated suite and frozen anomaly set; D026 RED/GREEN evidence; authority/budget/order/Stage-1/freeze compliance; and the accepted section 10.1 access grammar plus composite section 10.2 proof. The audit reviews this checkpoint and does not create it. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:24-42`)

This prompt authorizes no host, network, SSH, deployment, service, credential, broker/exchange, ARM, order, TESTNET/mainnet, Pine, parity, MTC, trading, merge-to-master, push, economic, product-code, acceptance, or authorization action. Do not implement or repair anything and do not contact or mutate a host. (`C:\tmp\lane_kick\X6.md:57-61`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:39-42`)

## Identity and independence gate

Use only audit worktree `<CLAUDE_AUDIT_WORKTREE>`. It must be separate from the implementer and Codex worktrees and must resolve to the same full frozen SHA used by the other auditor. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:65-80`)

Before review, run and record verbatim:

```text
resolved worktree path: <CLAUDE_AUDIT_WORKTREE>
git -C <CLAUDE_AUDIT_WORKTREE> rev-parse HEAD
git -C <CLAUDE_AUDIT_WORKTREE> status --porcelain
```

Require `git rev-parse HEAD` to equal `<FREEZE_SHA>` exactly and the status output to be empty. At the end, run and record the same path, HEAD, and status commands again; the final status must also be empty. A mismatch or non-empty pre/post cleanliness proof is `BLOCK`. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:67-80`; `C:\tmp\lane_kick\X6.md:36-39`)

If you have received any Codex verdict, reasoning, or findings before sealing your report, stop and return `BLOCK` for compromised independence; do not use the information. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:16-18`; `C:\tmp\lane_kick\X6.md:36-39`)

## Bounded reading list

Read these exact documents and no directory wholesale:

1. `AGENTS.md`
2. `MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md`
3. `MTC_COMMAND_CENTER/_AI_MEMORY/AI_RULES.md`
4. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md`
5. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md`
6. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS_FILL_2026-08-15.md`
7. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_HANDOFF_PACKAGE.md`
8. `<PACKET10_MANIFEST_PATH>` — expected SHA-256 `<PACKET10_MANIFEST_SHA256>`
9. `<FROZEN_FILE_LIST_PATH>` — expected SHA-256 `<FROZEN_FILE_LIST_SHA256>`
10. `<BASE_TO_FREEZE_DIFF_PATH>` — expected SHA-256 `<BASE_TO_FREEZE_DIFF_SHA256>`; base `<BASE_SHA>`, freeze `<FREEZE_SHA>`
11. `MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/UNIT_CLOSURE_RECORD.md`
12. `MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/EVIDENCE_INDEX.md`
13. `<FINAL_WPI_CLOSURE_RECORD>`
14. `<FINAL_WPI_EVIDENCE_INDEX>`
15. `<FINAL_ACCEPTANCE_MATRIX>`
16. `<FINAL_D026_REGISTER>`
17. `<FREEZE_TIME_LEDGER_SOURCE>`
18. `<CONSOLIDATED_AUTHORITY_RECORD>`
19. `<BASELINE_SOURCE>` — expected SHA-256 `<BASELINE_SOURCE_SHA256>`
20. `<CONFIG_RESCAN_RECORD>`
21. `<EVIDENCE_SNAPSHOT_INDEX>` at immutable root `<EVIDENCE_SNAPSHOT_ROOT>` — expected index SHA-256 `<EVIDENCE_SNAPSHOT_SHA256>`
22. The exact newline-separated paths in `<BOUNDED_REVIEW_PATH_LIST>`

The frozen session contract supplies only the scope/plan, actual diff/files, test/evidence package, readiness material, and required repository rules, without implementer-session context. Do not replace the exact list with a broad repository scan. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:44-49`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md:43-55`; `C:\tmp\lane_kick\X6.md:47-48`)

## Frozen bindings to verify independently

Record and recompute, rather than merely copy, every binding the Packet-10 manifest marks recomputable:

- frozen SHA `<FREEZE_SHA>`, base `<BASE_SHA>`, and exact base-to-freeze diff;
- candidate commit `<CANDIDATE_COMMIT>`;
- artifact `<CANDIDATE_ARTIFACT_PATH>` / `<CANDIDATE_ARTIFACT_SHA256>`;
- candidate manifest `<CANDIDATE_MANIFEST_PATH>` / `<CANDIDATE_MANIFEST_SHA256>`;
- immutable evidence root/index and all identities the index requires;
- WP-L and WP-I closure/evidence identities;
- final acceptance matrix, D026 register, authority record, and freeze-time ledger; and
- preregistration ordering, RUNID accounting, hashes, Stage-1 ordering, section 10.1 grammar, and composite section 10.2 proof. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:26-37`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md:45-55`)

If required evidence is not present in the immutable snapshot and no separately authorized read-only evidence root is provided, do not infer it or contact a host; return `BLOCK` if the missing evidence prevents the required determination. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md:55`; `C:\tmp\lane_kick\X6.md:57-61`)

## Mandated suite — execute exactly

Bind `P10_WORKTREE` to `<CLAUDE_AUDIT_WORKTREE>` and `P10_PYTHON` to `<CLAUDE_P10_PYTHON>`, then execute this exact Linux command without substituting a different suite command:

```bash
cd -- "$P10_WORKTREE" && \
env -u PYTHONHOME -u PYTHONPATH -u PYTEST_ADDOPTS -u PYTEST_PLUGINS \
  PYTHONUTF8=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
  "$P10_PYTHON" -m pytest IBKR_PAPER_BRIDGE/tests -q \
  -p anyio.pytest_plugin -p no:cacheprovider
```

The definition expects exit code `0`, `<EXPECTED_PASS_COUNT>` passes, `0` failures, `<EXPECTED_SKIP_COUNT>` skips, and `<EXPECTED_XFAIL_COUNT>` xfails. The authoritative observed/adjudicated anomaly set is `<OBSERVED_ADJUDICATED_ANOMALY_SET>` with signatures `<ANOMALY_SIGNATURES>`; do not infer that set or carry forward provisional historical failures. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS_FILL_2026-08-15.md:37-67`)

Record the exact command, environment bindings, monotonic suite start/finish, runtime, exit code, counts, node IDs/signatures for any anomaly, and real stdout/stderr. Inability to execute the mandated suite is `BLOCK`; non-execution cannot support acceptance. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:82-104`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md:57-66`)

## D026 reproduction

For every new test offered as proof that a named defect is closed, use `<FINAL_D026_REGISTER>` to reproduce the exact RED against supplied pre-fix behavior or an equivalent supplied mutation, then reproduce GREEN on the accepted frozen implementation. State separately for every test whether you personally verified both arms and quote the real commands/output. If neither arm can be reproduced, classify the test as supplemental rather than closure evidence. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:106-116`)

Do not edit frozen product code or evidence. Use only immutable pre-fix/mutation material supplied by the frozen bundle and scratch execution outside the tracked worktree; if the required reproduction cannot be performed within those boundaries, report the limitation and do not claim closure. (`C:\tmp\lane_kick\X6.md:57-61`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:69-76`)

## Metering record

Use `<CLAUDE_P10_PYTHON> -c "import time; print(time.monotonic_ns())"` at every phase boundary. In `<CLAUDE_REPORT_PATH>`, include raw monotonic start/finish readings and calculated seconds for:

- total session;
- active document/source review, excluding the three separately timed phases below;
- mandated-suite runtime;
- evidence and D026 reproduction time; and
- cumulative active report-writing time, summing the preflight-header write and every later report-writing segment while excluding review, suite, and evidence-reproduction intervals.

Also record model, effort, checkpoint, frozen SHA, worktree identity, commands, output bytes/lines where available, suite counts, D026-pair count, finding count, verdict, and whether re-audit is required. Do not estimate missing time; label it `UNKNOWN` with the reason. (`C:\tmp\lane_kick\X6.md:43-46`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md:166-177`)

## Sole report file and verdict

Write only `<CLAUDE_REPORT_PATH>`. Include:

1. verbatim session-header preflight and write-capability confirmation;
2. independence statement and confirmation that no Codex result was seen;
3. full frozen SHA, resolved worktree path, and pre/post HEAD and cleanliness outputs;
4. bounded documents and frozen paths actually read;
5. identity/hash/diff recomputations and chain-of-custody results;
6. exact suite command/environment and real output/baseline comparison;
7. a per-test D026 RED/GREEN table;
8. authority/order/scope and hard-exclusion assessment;
9. limitations and every finding;
10. complete metering record; and
11. exactly one overall verdict. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md:61-66`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:118-124`)

Allowed verdicts only:

- `PASS` — no required changes.
- `PASS-WITH-NITS` — accepting, optional nits only, zero required repairs.
- `REQUEST_CHANGES` — at least one required repair.
- `BLOCK` — the workflow cannot safely continue. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md:111-120`)

Every required finding must name the exact file, observed behavior, expected behavior, and a reproducible command or comparison. Do not make an acceptance or authorization decision; the Lead independently reproduces required findings and owns the later checkpoint decision. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:118-124`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md:120`)

After the final worktree path/HEAD/status check, capture and record the raw session-finish monotonic reading, calculate the phase durations, append the timing record and verdict, and seal `<CLAUDE_REPORT_PATH>` before any result is shared with the Codex auditor. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md:166-177`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:16-18`)

---

# Dispatch prompt 2 — Codex Audit 2 T0

**Dispatcher transport requirement:** launch this kickoff in a fresh Codex session with `--dangerously-bypass-approvals-and-sandbox`; otherwise the session can silently start with `sandbox: read-only` and be unable to execute or write. This flag grants transport capability only and does not relax any scope or exclusion below. The auditor must confirm the actual session header before doing any work. (`C:\tmp\lane_kick\X6.md:51-54`)

You are the second of two independent Audit 2 T0 auditors. Use a **fresh standalone Codex `gpt-5.6-sol` session at reasoning effort `xhigh`**, with no resume/continue and no implementer-session context. Do not receive or inspect the Claude auditor's response, reasoning, findings, or verdict until your report is sealed. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:9-22`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md:37-41`)

## Mandatory preflight — before reading or executing anything

1. Confirm the session header first: model is exactly `gpt-5.6-sol`, reasoning effort is exactly `xhigh`, the session is fresh, sandbox/approval state reflects `--dangerously-bypass-approvals-and-sandbox` rather than read-only, and the session can execute the mandated suite and write `<CODEX_REPORT_PATH>`. If any field is wrong or unavailable, stop before audit work and return `BLOCK`; exact model/effort unavailability is not a silent-fallback condition. (`C:\tmp\lane_kick\X6.md:51-54`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md:11-18`)
2. Verify that every angle-bracket placeholder in this prompt has been replaced. If one remains, record it as `UNKNOWN`, write a minimal `BLOCK` report to `<CODEX_REPORT_PATH>`, and stop. The freeze SHA must not be inferred. (`C:\tmp\lane_kick\X6.md:40-42`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS_FILL_2026-08-15.md:21-31`)
3. Capture the session-start monotonic reading with `<CODEX_P10_PYTHON> -c "import time; print(time.monotonic_ns())"` immediately after the header and placeholder checks. The session must meter monotonic start/finish and the named work phases so Audit 3/Gate 6 can be priced from actuals. (`C:\tmp\lane_kick\X6.md:43-46`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md:166-177`)
4. Create or open exactly one output file, `<CODEX_REPORT_PATH>`, outside the worktree. Write and flush the session-header confirmation and raw start reading before audit work; this is the write-capability proof. Write no other deliverable or repository file. Each auditor produces exactly one independent report. (`C:\tmp\lane_kick\X6.md:49-54`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md:61-66`)

## Scope and non-authority

Audit only the Linux-port and staging-acceptance evidence for the already frozen pre-WP-A artifact at full SHA `<FREEZE_SHA>`. Check frozen source/candidate/artifact/manifest/evidence identity; WP-L Phase-2 closure and preserved open/BLOCKED items; final WP-I closure including rows 1-24 and the successor; chain of custody, preregistration order, RUNIDs, and hashes; the mandated suite and frozen anomaly set; D026 RED/GREEN evidence; authority/budget/order/Stage-1/freeze compliance; and the accepted section 10.1 access grammar plus composite section 10.2 proof. The audit reviews this checkpoint and does not create it. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:24-42`)

This prompt authorizes no host, network, SSH, deployment, service, credential, broker/exchange, ARM, order, TESTNET/mainnet, Pine, parity, MTC, trading, merge-to-master, push, economic, product-code, acceptance, or authorization action. Do not implement or repair anything and do not contact or mutate a host. (`C:\tmp\lane_kick\X6.md:57-61`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:39-42`)

## Identity and independence gate

Use only audit worktree `<CODEX_AUDIT_WORKTREE>`. It must be separate from the implementer and Claude worktrees and must resolve to the same full frozen SHA used by the other auditor. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:65-80`)

Before review, run and record verbatim:

```text
resolved worktree path: <CODEX_AUDIT_WORKTREE>
git -C <CODEX_AUDIT_WORKTREE> rev-parse HEAD
git -C <CODEX_AUDIT_WORKTREE> status --porcelain
```

Require `git rev-parse HEAD` to equal `<FREEZE_SHA>` exactly and the status output to be empty. At the end, run and record the same path, HEAD, and status commands again; the final status must also be empty. A mismatch or non-empty pre/post cleanliness proof is `BLOCK`. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:67-80`; `C:\tmp\lane_kick\X6.md:36-39`)

If you have received any Claude verdict, reasoning, or findings before sealing your report, stop and return `BLOCK` for compromised independence; do not use the information. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:16-18`; `C:\tmp\lane_kick\X6.md:36-39`)

## Bounded reading list

Read these exact documents and no directory wholesale:

1. `AGENTS.md`
2. `MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md`
3. `MTC_COMMAND_CENTER/_AI_MEMORY/AI_RULES.md`
4. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md`
5. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md`
6. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS_FILL_2026-08-15.md`
7. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_HANDOFF_PACKAGE.md`
8. `<PACKET10_MANIFEST_PATH>` — expected SHA-256 `<PACKET10_MANIFEST_SHA256>`
9. `<FROZEN_FILE_LIST_PATH>` — expected SHA-256 `<FROZEN_FILE_LIST_SHA256>`
10. `<BASE_TO_FREEZE_DIFF_PATH>` — expected SHA-256 `<BASE_TO_FREEZE_DIFF_SHA256>`; base `<BASE_SHA>`, freeze `<FREEZE_SHA>`
11. `MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/UNIT_CLOSURE_RECORD.md`
12. `MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/EVIDENCE_INDEX.md`
13. `<FINAL_WPI_CLOSURE_RECORD>`
14. `<FINAL_WPI_EVIDENCE_INDEX>`
15. `<FINAL_ACCEPTANCE_MATRIX>`
16. `<FINAL_D026_REGISTER>`
17. `<FREEZE_TIME_LEDGER_SOURCE>`
18. `<CONSOLIDATED_AUTHORITY_RECORD>`
19. `<BASELINE_SOURCE>` — expected SHA-256 `<BASELINE_SOURCE_SHA256>`
20. `<CONFIG_RESCAN_RECORD>`
21. `<EVIDENCE_SNAPSHOT_INDEX>` at immutable root `<EVIDENCE_SNAPSHOT_ROOT>` — expected index SHA-256 `<EVIDENCE_SNAPSHOT_SHA256>`
22. The exact newline-separated paths in `<BOUNDED_REVIEW_PATH_LIST>`

The frozen session contract supplies only the scope/plan, actual diff/files, test/evidence package, readiness material, and required repository rules, without implementer-session context. Do not replace the exact list with a broad repository scan. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:44-49`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md:43-55`; `C:\tmp\lane_kick\X6.md:47-48`)

## Frozen bindings to verify independently

Record and recompute, rather than merely copy, every binding the Packet-10 manifest marks recomputable:

- frozen SHA `<FREEZE_SHA>`, base `<BASE_SHA>`, and exact base-to-freeze diff;
- candidate commit `<CANDIDATE_COMMIT>`;
- artifact `<CANDIDATE_ARTIFACT_PATH>` / `<CANDIDATE_ARTIFACT_SHA256>`;
- candidate manifest `<CANDIDATE_MANIFEST_PATH>` / `<CANDIDATE_MANIFEST_SHA256>`;
- immutable evidence root/index and all identities the index requires;
- WP-L and WP-I closure/evidence identities;
- final acceptance matrix, D026 register, authority record, and freeze-time ledger; and
- preregistration ordering, RUNID accounting, hashes, Stage-1 ordering, section 10.1 grammar, and composite section 10.2 proof. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:26-37`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md:45-55`)

If required evidence is not present in the immutable snapshot and no separately authorized read-only evidence root is provided, do not infer it or contact a host; return `BLOCK` if the missing evidence prevents the required determination. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md:55`; `C:\tmp\lane_kick\X6.md:57-61`)

## Mandated suite — execute exactly

Bind `P10_WORKTREE` to `<CODEX_AUDIT_WORKTREE>` and `P10_PYTHON` to `<CODEX_P10_PYTHON>`, then execute this exact Linux command without substituting a different suite command:

```bash
cd -- "$P10_WORKTREE" && \
env -u PYTHONHOME -u PYTHONPATH -u PYTEST_ADDOPTS -u PYTEST_PLUGINS \
  PYTHONUTF8=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
  "$P10_PYTHON" -m pytest IBKR_PAPER_BRIDGE/tests -q \
  -p anyio.pytest_plugin -p no:cacheprovider
```

The definition expects exit code `0`, `<EXPECTED_PASS_COUNT>` passes, `0` failures, `<EXPECTED_SKIP_COUNT>` skips, and `<EXPECTED_XFAIL_COUNT>` xfails. The authoritative observed/adjudicated anomaly set is `<OBSERVED_ADJUDICATED_ANOMALY_SET>` with signatures `<ANOMALY_SIGNATURES>`; do not infer that set or carry forward provisional historical failures. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS_FILL_2026-08-15.md:37-67`)

Record the exact command, environment bindings, monotonic suite start/finish, runtime, exit code, counts, node IDs/signatures for any anomaly, and real stdout/stderr. Inability to execute the mandated suite is `BLOCK`; non-execution cannot support acceptance. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:82-104`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md:57-66`)

## D026 reproduction

For every new test offered as proof that a named defect is closed, use `<FINAL_D026_REGISTER>` to reproduce the exact RED against supplied pre-fix behavior or an equivalent supplied mutation, then reproduce GREEN on the accepted frozen implementation. State separately for every test whether you personally verified both arms and quote the real commands/output. If neither arm can be reproduced, classify the test as supplemental rather than closure evidence. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:106-116`)

Do not edit frozen product code or evidence. Use only immutable pre-fix/mutation material supplied by the frozen bundle and scratch execution outside the tracked worktree; if the required reproduction cannot be performed within those boundaries, report the limitation and do not claim closure. (`C:\tmp\lane_kick\X6.md:57-61`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:69-76`)

## Metering record

Use `<CODEX_P10_PYTHON> -c "import time; print(time.monotonic_ns())"` at every phase boundary. In `<CODEX_REPORT_PATH>`, include raw monotonic start/finish readings and calculated seconds for:

- total session;
- active document/source review, excluding the three separately timed phases below;
- mandated-suite runtime;
- evidence and D026 reproduction time; and
- cumulative active report-writing time, summing the preflight-header write and every later report-writing segment while excluding review, suite, and evidence-reproduction intervals.

Also record model, effort, checkpoint, frozen SHA, worktree identity, commands, output bytes/lines where available, suite counts, D026-pair count, finding count, verdict, and whether re-audit is required. Do not estimate missing time; label it `UNKNOWN` with the reason. (`C:\tmp\lane_kick\X6.md:43-46`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md:166-177`)

## Sole report file and verdict

Write only `<CODEX_REPORT_PATH>`. Include:

1. verbatim session-header preflight and write-capability confirmation;
2. independence statement and confirmation that no Claude result was seen;
3. full frozen SHA, resolved worktree path, and pre/post HEAD and cleanliness outputs;
4. bounded documents and frozen paths actually read;
5. identity/hash/diff recomputations and chain-of-custody results;
6. exact suite command/environment and real output/baseline comparison;
7. a per-test D026 RED/GREEN table;
8. authority/order/scope and hard-exclusion assessment;
9. limitations and every finding;
10. complete metering record; and
11. exactly one overall verdict. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md:61-66`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:118-124`)

Allowed verdicts only:

- `PASS` — no required changes.
- `PASS-WITH-NITS` — accepting, optional nits only, zero required repairs.
- `REQUEST_CHANGES` — at least one required repair.
- `BLOCK` — the workflow cannot safely continue. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md:111-120`)

Every required finding must name the exact file, observed behavior, expected behavior, and a reproducible command or comparison. Do not make an acceptance or authorization decision; the Lead independently reproduces required findings and owns the later checkpoint decision. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:118-124`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md:120`)

After the final worktree path/HEAD/status check, capture and record the raw session-finish monotonic reading, calculate the phase durations, append the timing record and verdict, and seal `<CODEX_REPORT_PATH>` before any result is shared with the Claude auditor. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md:166-177`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:16-18`)
