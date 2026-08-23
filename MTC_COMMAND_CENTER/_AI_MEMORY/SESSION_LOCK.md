# SESSION_LOCK — workstream write ownership

Rewritten 2026-08-11. The old file was a single unused "Status: unlocked" line; it did not
prevent the 2026-08-10 concurrent-session collision on the transport set
(`11_TRIAGE/WPI_BLOCKS_DRAFT/CONCURRENT_SESSION_NOTICE_2026-08-10_2130.md`). This version
is the mechanism behind `AI_RULES.md` § Autonomous Session Invariants, rule 2.

## Protocol

1. **Before the first write** to any file belonging to a workstream below, set yourself as
   OWNER on that row (session label + local timestamp) and commit the change with your
   first substantive commit.
2. **One writable owner per workstream.** Everyone else is read-only on that workstream's
   files. Auditing (read-only review, reports written to your OWN workstream row or a new
   file) is always allowed.
3. **Release at handoff**: set the row back to UNCLAIMED in your final memory write-back
   (Gate 7).
4. **Stale locks:** a row older than 24h with no commits touching that workstream may be
   taken over — record the takeover with a dated note in the Log section.
5. **On finding a foreign uncommitted edit** in a workstream you own: stop writing there,
   preserve the edit (commit it labelled as foreign/partial), write a dated notice, ask the
   owner (Barış) which session should own the row. Never revert or overwrite it silently.

## Ownership table

| Workstream | Files (primary home) | Owner | Since |
|---|---|---|---|
| RP6-P0 block | `11_TRIAGE/WPI_BLOCKS_DRAFT/` RP6* | **UNCLAIMED** — released 2026-08-12 20:45 | — |
| RP7-WPI-RO block | `11_TRIAGE/WPI_BLOCKS_DRAFT/` RP7* | **Codex Lead `019fe77c`** — preserved partial repair; serialized writer only | 2026-08-14 10:30 +03 |
| Transport set | `11_TRIAGE/WPI_BLOCKS_DRAFT/` transport/run_p0/run_ro/remote_* | **UNCLAIMED** — released 2026-08-12 20:45 | — |
| §10.2 prover / SEC102 | `11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/` SEC102*, pathscope* | **Codex Lead `019fe77c`** — final owner-authorized Pathscope cycle | 2026-08-14 10:30 +03 |
| Successor prereg draft | `11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/` WPI_*PREREG* | **UNCLAIMED** — released 2026-08-12 20:45 | — |
| Audit-2 readiness package | `11_TRIAGE/AUDIT2_READINESS_PACKAGE/` | **Codex Lead `019fe77c`** — documentation and freeze preparation only | 2026-08-14 10:30 +03 |
| Shared memory layer | `_AI_MEMORY/` handoffs, rules, routing | **Codex Lead `/root`** — Map #96 planning fold only; `LIVE_TRADING_GATE.md`, handoff and next-step records; no runtime, host, credential or economic action | 2026-08-23 22:19 +03 |
| Gemini adviser route | `11_TRIAGE/GEMINI_PRO_*` plus external launcher/project config | **UNCLAIMED** — released 2026-08-16 22:19 +03 | — |
| Backend/Dashboard V2 design record | `IBKR_PAPER_BRIDGE/docs/30_V2_BACKEND_AND_DASHBOARD_DESIGN_DECISIONS.md` | **UNCLAIMED** — released 2026-08-17 00:54 +03; foreign partial preserved | — |
| Bridge Help / System Map | `IBKR_PAPER_BRIDGE/bridge/static/` Help-only UI, `IBKR_PAPER_BRIDGE/tests/test_dashboard_static.py`, and Help/Wiki reference docs | **UNCLAIMED** — released cleanly at Gate 7 | 2026-08-17 03:54 +03 |
| Worktree cleanup + Phase Watch V3 review | `11_TRIAGE/WORKTREE_*`, `11_TRIAGE/PHASE_WATCH_V3_*`, worktree registry | **UNCLAIMED** — claimed and released same run by Fable Lead cleanup session, 2026-08-18 (work complete, records committed) | — |

**All rows released 2026-08-12 20:45** by the Fable session "sabaha kadar çalışma planı" at its
clean stop (Gate 7). Everything it produced is committed and pushed through `d4a07438`. **The
next session should claim the rows it intends to write before its first write** — and note that
tonight's four Claude Pro audit lanes are READ-ONLY on the block workstreams (each writes only
its own verdict file), so they do not require ownership of RP6/RP7/transport/pathscope.

Workstreams not listed: add a row before writing.

| Master architecture planning documents (kernel fold branch) | `11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md`, `11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md`, `11_TRIAGE/WAYFINDER_KERNEL_FOLD_2026-08-23.md` | **RELEASED** - map #67 kernel fold complete 2026-08-23; work confined to branch `feature/wayfinder-fold-map67-20260823` (worktree C:\WFFOLD67, from master `3d6a621c`) | 2026-08-23 |
| Master architecture planning documents (Map #96 fold branch) | `11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md`, `11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md`, `11_TRIAGE/REQUIREMENTS_TRACEABILITY_REGISTER_2026-08-22.md`, `11_TRIAGE/WAYFINDER_SAFETY_OPERATIONS_FOLD_2026-08-23.md` | **Codex Lead `/root`** — issue #111 documentation fold in isolated worktree `C:\WF111`; single writer; implementation authorized: NO | 2026-08-23 22:19 +03 |
| Master architecture planning documents (lifecycle fold branch) | `11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md`, `11_TRIAGE/WAYFINDER_LIFECYCLE_FOLD_2026-08-23.md` | **RELEASED** — map #54 lifecycle fold complete 2026-08-23; work confined to branch `feature/wayfinder-fold-map54-20260823` (worktree C:\WFFOLD54, based on the #37 fold branch) | 2026-08-23 |
| Master architecture planning documents (fold branch) | `11_TRIAGE/MASTER_*_2026-08-2*.md`, `11_TRIAGE/WAYFINDER_DECISION_FOLD_2026-08-23.md` | **RELEASED** — wayfinder fold complete 2026-08-23; work confined to branch `feature/wayfinder-fold-20260823` (worktree C:\WFOLD) | 2026-08-23 |

## Log

- **2026-08-23 (kernel fold, map #67):** Claude Fable 5 claimed and released the kernel-fold
  row for the owner-decided map #67 fold (fold task GH #77): new brief section 9.7 (kernel &
  economic-honesty governance), two rows added to the section-6.5 admission-mechanics block,
  amendment paragraphs on WP-P0-20 (seed named + acceptance additions) and WP-P0-30 (collector =
  earliest deliverable, most-time-critical wave-1 flag), plus fold record
  `11_TRIAGE/WAYFINDER_KERNEL_FOLD_2026-08-23.md` (control-parity checklist v1, statistical-battery
  definition v1, known-divergence register, corrections incl. VEN-C/VEN-E label). Branch
  `feature/wayfinder-fold-map67-20260823` from master `3d6a621c`; main checkout untouched.
  Requirements 60; packages 75; owner docs untouched; nothing authorized (D-12). MATERIAL -
  fresh G1 round recommended.

- **2026-08-23 (lifecycle fold, map #54):** Claude Fable 5 claimed and released the
  lifecycle-fold row for the owner-decided map #54 fold (fold task GH #66): eight anchored
  amendments to the brief (§6.3 banner, §6.4 brownfield carrier, §6.5 admission mechanics,
  §6.6 succession sentence, new §6.9 tail/re-entry/succession, §11.5 one-ledger paragraph,
  A-18 re-worded, §17.2/§17.2b cohort cross-refs) plus fold record
  `11_TRIAGE/WAYFINDER_LIFECYCLE_FOLD_2026-08-23.md` (mapping table, worthiness checklist
  v0.1 DRAFT, record-type register, registry-retirement deferral note). Work happened ONLY on
  branch `feature/wayfinder-fold-map54-20260823` stacked on `feature/wayfinder-fold-20260823`
  (`46fb8159`); the main checkout untouched. Requirement count stays 60; package count stays
  75; no owner document edited; nothing authorized (D-12). Amendments declared MATERIAL —
  fresh G1 round recommended before G1-IA on affected packages.

- **2026-08-23 (wayfinder fold):** Claude Fable 5 claimed and released the planning-documents
  row for the owner-decided wayfinder fold (decision map GH #37, ticket #49): six packages
  added (WP-P0-26…30, WP-V4-09), thirteen amended in place, the brief's §17.2 ghost
  dependencies re-pointed, package count 69→75; fold record
  `11_TRIAGE/WAYFINDER_DECISION_FOLD_2026-08-23.md`. Work happened ONLY on branch
  `feature/wayfinder-fold-20260823` from accepted base `764da27f` — the main checkout and its
  foreign uncommitted edits were not touched, and no other branch's SESSION_LOCK state is
  overwritten by this branch-local record. No owner outcome reworded; requirement count stays
  60; nothing authorized. A fresh G1 acceptance round over the amended set is recommended
  before G1-IA on affected packages.
- **2026-08-18 ~17:10 +03:** Fable Lead cleanup session claimed-and-released the
  new "Worktree cleanup + Phase Watch V3 review" row in a single run: 124
  worktrees deregistered (115 clean, 9 ACL husks), 36 rescue branches pushed,
  Phase Watch V3 ledger verified + GLM-5.2 REQUEST_CHANGES supplemental verdict
  recorded, T0 pair live-probed capacity-blocked. The concurrent "Bridge V2
  continuation" session was notified of the lane split before any shared write.
  All records committed from `C:\WTCLEAN_CTRL` (`chore/worktree-cleanup-20260818`).

- **2026-08-17 03:54 +03:** Codex Lead `01a00921` completed a clean Gate-7
  release of the Shared memory layer and Bridge Help / System Map rows. The
  accepted local Help feature is committed at `d71bc073`, its acceptance record
  at `7697c07b`, and the consolidated seven-workstream status/disposition at
  `511298f0`. Nothing was deployed and no host or economic action occurred.
  The dirty six-file memory rotation and dirty `docs/30` working copy remain
  preserved, unaccepted, and unchanged.

- **2026-08-17 00:55 +03:** After receiving the prior cap report, Barış
  explicitly instructed the overnight session to continue all safe work without
  waiting for further approvals. Codex Lead `01a00921` reclaimed the Help/Wiki
  and shared-memory rows and opened a materially fresh T1 truth-only cycle for
  the two recorded source-truth defects. This does not authorize runtime,
  trading, host, deployment, credential, broker, or economic changes.

- **2026-08-17 00:54 +03:** Codex Lead `01a00921` released the Help/Wiki,
  design-record, and shared-memory rows at a clean stop. The seven-workstream
  owner roadmap is committed. The complete Help implementation remains
  uncommitted and preserved in `C:\BRIDGE_HELP_IMPL` because the fresh round-2
  flagship review found two documentation truth defects and exhausted the T1
  two-round cap. `NEXT_STEPS.md` records the exact repair and explicit cap-waiver
  boundary. The unrelated design-record partial remains preserved and was not
  included, overwritten, or accepted.

- **2026-08-16 22:38 +03:** Codex Lead `01a00921` claimed the Bridge Help /
  System Map row for the owner-requested interactive Wiki and diagram update.
  Product scope remains the frozen T1 non-economic Help-only contract; no
  runtime, API, trading, host, deployment, credential, or economic change.

- **2026-08-16 22:21 +03:** Codex Lead `01a00921` claimed the design-record and
  shared-memory rows after Gemini 3.7 Flash High produced isolated draft
  `e8e8ce7f`. Codex will transfer only independently verified content, correcting
  the draft's V1 service-model error and premature technology choices. No
  product, host, network, credential, control, or economic action is authorized.

- **2026-08-16 22:19 +03:** Codex Lead `01a00ad1` released the Gemini and shared-memory
  rows. Direct headless terminal commands remained permission-denied under bounded grants, so
  the dangerous bypass was not used and the route was restored to explicit terminal denial.
  Allowlisted file coding remains operational. Gemini produced the requested same-VPS decision
  draft in `C:\GEMINI`, committed as `e8e8ce7f`; the owning thread will inspect and transfer it.
  This session did not touch the canonical Bridge design-decision file.

- **2026-08-16 22:08 +03:** Owner authorized terminal access for Gemini inside its dedicated
  `C:\GEMINI` worktree. Codex Lead `01a00ad1` claimed the Gemini and shared-memory rows for a
  bounded sandboxed command allowlist, read-only-at-rest config, one short live probe, and
  concise handoff. Git mutation, network/install/deploy commands, credentials, protected paths,
  and canonical/frozen checkout access remain excluded.

- **2026-08-16 22:06 +03:** Codex Lead `01a00921` released the Dashboard V2
  design-record and shared-memory rows. Exact Claude was session-limit blocked;
  no design-record byte changed. The owner-approved content and fresh KVM2
  read-only result are queued in `NEXT_STEPS.md` and `GLOBAL_HANDOFF.md`.

- **2026-08-16 22:03 +03:** Codex Lead `01a00921` claimed the Dashboard V2
  design-record and shared-memory rows for the owner's requested hosting/access
  decision only. Scope: record VPS-hosted Bridge dashboard, private-first access,
  current KVM2 not-installed status, and current/planned distinction. No product,
  host, deployment, network, credential, control, or economic action is writable.

- **2026-08-16 21:52 +03:** Codex Lead `01a00921` released the Help/Wiki and
  shared-memory rows after commit `838adb95` added the full Exchange-plane and
  Observation/Control-plane requirements to the frozen implementation package.
  Product implementation remains blocked until the exact counterpart capacity
  reset; no dashboard source or live surface changed.

- **2026-08-16 21:47 +03:** Codex Lead `01a00921` reclaimed the Help/Wiki and
  shared-memory rows only to add the owner's Exchange-plane explanation and the
  truthful current-versus-future Observation/Control access boundary to the
  frozen implementation contract. No dashboard source, runtime, host, network,
  broker, credential, ARM, or economic action is writable under this claim.

- **2026-08-16 21:39 +03:** Codex Lead `01a00ad1` released the Gemini and shared-memory
  rows after the isolated coder pilot passed. The separate launcher allows only explicitly
  named unprotected files in `C:\GEMINI`; its one-file live edit passed, Codex reviewed it,
  the temporary file was removed, and the worktree is clean. The requested Help/System Map
  drawings and SQLite+WAL black-box/logbook sentence was added to `NEXT_STEPS.md`; no Help or
  dashboard implementation file was touched.

- **2026-08-16 21:30 +03:** Owner authorized a separate Gemini CLI coder route without a
  long audit cycle. Codex Lead `01a00ad1` claimed the Gemini and shared-memory rows for a
  dedicated isolated worktree, explicit file scope, one harmless live edit, Codex review,
  and concise handoff. The existing read-only route remains unchanged; protected trading,
  credentials, deployment, commit, push, and merge remain excluded.

- **2026-08-16 21:45 +03:** Codex Lead `01a00921` released the Help/Wiki and
  shared-memory rows after recording the clean counterpart-capacity blocker.
  Gate 1 and the exact prompt are committed; no dashboard source was partially
  edited. Resume after the exact Claude capacity reset.

- **2026-08-16 21:40 +03:** Codex Lead `01a00921` claimed the shared-memory
  row only to record the clean Help/Wiki capacity blocker and immediate resume
  instruction. No product or protected runtime surface is writable under this
  claim.

- **2026-08-16 21:30 +03:** Codex Lead `01a00921` claimed the new Bridge Help /
  System Map workstream for the owner-requested interactive, explanatory Wiki.
  Scope is static Help UI, its tests, and a shared AI-readable knowledge source.
  Trading logic, strategy/risk/order behavior, APIs, configuration, deployment,
  credentials, hosts, and economic actions remain excluded.

- **2026-08-16 20:59 +03:** Codex Lead `01a00921` released the design-record
  and shared-memory rows after A11, A12, the change log, source links, and Gate-7
  handoff were complete. Fresh read-only T2 `gpt-5.6-sol` medium review returned
  PASS with no findings or nits. No implementation or live surface changed.

- **2026-08-16 20:58 +03:** Codex Lead `01a00921` claimed the shared-memory row
  only for the required final handoff and next-step record for the accepted A11
  documentation change. No source, configuration, host, deployment, or trading
  surface is writable under this claim.

- **2026-08-16 20:44 +03:** Codex Lead `01a00921` reclaimed only the
  Backend/Dashboard V2 design-record row for the owner-requested documentation
  of MTC_V2 versus Bridge order/exit lifecycle ownership. No implementation,
  configuration, host, deployment, broker, trading, or economic surface is writable.

- **2026-08-16 20:31 +03:** Codex Lead `01a00921` released the
  Backend/Dashboard V2 design-record row after the owner-requested B7 sourcing
  decision was added and a fresh read-only T2 review returned PASS. No code,
  configuration, credential, host, deployment, trading, or economic surface changed.

- **2026-08-16 20:22 +03:** Codex Lead `01a00921` claimed only the
  Backend/Dashboard V2 design record for the owner-requested documentation of
  Dashboard Codex-subscription use versus VPS LLM-gate API use. No implementation,
  configuration, credential, host, deployment, trading, or economic surface is writable.

- **2026-08-16 20:20 +03:** Codex Lead `01a00ad1` released the shared-memory and Gemini
  adviser rows at the owner's requested safe stop. Gemini CLI 1.1.13 is installed and the
  pinned read-only helper preflight passes for `gemini-3.7-flash-high`; the overlong final
  independent audit was interrupted at owner direction, so no final dual-flagship acceptance
  is claimed and coding access remains disabled.

- **2026-08-16 18:55 +03:** Owner authorized a new bounded cycle to make Gemini a safe
  read-only repo adviser now; coding access remains future-only and disabled. Codex Lead
  `01a00ad1` reclaimed only the shared-memory row for hardening, QA, and acceptance records.

- **2026-08-16 18:33 +03:** Codex Lead `01a00ad1` released the shared-memory row. The
  Gemini route is installed and live probes pass, but final T0 Codex round 3 returned
  `REQUEST_CHANGES`, exhausting the three-round cap. Claude acceptance was not run and
  the route remains not repo-ready pending explicit owner direction.

- **2026-08-16 17:23 +03:** Owner explicitly directed Codex to perform the implementation
  instead of waiting for Claude. Codex Lead `01a00ad1` reclaimed only the shared-memory
  row for that narrow override; independent T0 acceptance requirements remain unchanged.

- **2026-08-16 17:16 +03:** Codex Lead `01a00ad1` released the shared-memory row.
  Google AI Pro authentication and the external synthetic probes succeeded, but the
  required Claude Opus counterpart hit its session limit before Gate 2 and resets at
  18:10 Europe/Chisinau. No helper, Antigravity project config, Toolbox row, routing
  index, trading source, or protected surface was changed.

- **2026-08-16 17:09 +03:** Codex Lead `01a00ad1` claimed only the shared-memory row
  for the owner-requested Google AI Pro / Gemini 3.7 Flash read-only CLI route. Scope is
  local routing metadata and handoff only; no trading, Pine, parity, MTC, Bridge, host,
  deployment, broker, credential-value, or economic surface is writable.

- **2026-08-16 09:53 +03:** Codex Lead claimed only the shared-memory row to register
  the owner-requested AI-memory continuity audit/repair task, committed the task and
  handoff at `3996e810`, and released the row. No other workstream was touched.

- **2026-08-14 10:30 +03:** Codex Lead `019fe77c` claimed RP7, Pathscope, and
  Audit-2 readiness. The existing uncommitted `RP7-WPI-RO.sh` edit is the
  preserved partial from this same Lead's quota-interrupted Claude repair lane;
  it will not be reset, stashed, overwritten, or exposed to a second writer.
  Pathscope and RP7 writers will be serialized.

- **2026-08-13 ~09:00: all rows remain UNCLAIMED — released** by the Fable overnight session
  (2026-08-12 20:50 → 2026-08-13 09:00). Honest note: that session wrote to RP6/RP7/transport/
  pathscope/prereg/Audit-2 workstreams via dispatched lanes without first claiming rows (it was
  the only active Lead; no collision occurred — the RP7 auditor detected the Lead's own
  concurrent commits and attributed them correctly). Everything committed and pushed through
  the rows-1-9 r3 repair. In-flight at release: the Lead's verbatim r19/r17 RP6 fence runs
  (results go to the next session; see FRESH_SESSION_HANDOFF_2026-08-13_MORNING.md §7 tail).

- 2026-08-11: file rewritten from stub to ownership mechanism after the 2026-08-10
  transport collision (two sessions writing the same artifact family; detected, work
  dropped by one session, no data lost — see the concurrent-session notice).
- **2026-08-12 20:45: all rows RELEASED** by the Fable session "sabaha kadar çalışma planı" at
  its clean stop. That session held every WP-I row for the 2026-08-12 day run (~11 hours,
  ~45 commits). No foreign uncommitted edits were found in any owned workstream at release.
  One process note worth carrying: **two dispatched lanes independently refused Lead
  instructions that would have overwritten a prior lane's committed record** — once on the
  D026 recheck file, once on a GLM verdict path. Both surfaced instead of overwriting. That is
  the ownership discipline working, and it argues for keeping the "write exactly one NEW file"
  convention rather than naming existing paths in kickoffs.
- 2026-08-11 14:15: Fable overnight Lead `7e05aabf` (session "Sabaha kadar otonom çalışma
  planı" successor) claimed all five WP-I rows. Verified via session listing that the rule
  author ("Codex gece çalışması değerlendirmesi" session) committed `15d48088` at 13:46:53
  as its final act and is no longer running — exactly one active Lead loop exists.
- 2026-08-23 evening: Fable Lead (wayfinder session) claimed + released the map-#78 explorer fold workstream on branch feature/wayfinder-fold-map78-20260823 (worktree C:\WF86, base ab35ca66); scope: brief SEC 11.6 + 12.2 + KLineChart row, plan WP-P0-14/P0-18/V3-01/V3-11 amendment text, fold doc WAYFINDER_EXPLORER_FOLD_2026-08-23.md. Single-session fold, no other workstream touched.
- 2026-08-23 evening: Codex Lead claimed + released the map-#79 execution-critique fold workstream on branch feature/wayfinder-fold-map79-20260823 (worktree C:\WF93, base a01de9c5); scope: brief execution-doctrine/carrier/v9 amendments, plan WP-P0-31 plus named carrier amendments, traceability count/mapping note, fold doc WAYFINDER_EXECUTION_CRITIQUE_FOLD_2026-08-23.md. Documentation-only fold; no protected runtime or owner outcome file touched.
