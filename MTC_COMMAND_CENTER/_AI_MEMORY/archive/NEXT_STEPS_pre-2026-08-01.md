# NEXT_STEPS — ARCHIVE (entries dated before 2026-08-01)

> Rotated out of the live file 2026-08-15 (Lesson Ladder Stage 1). Content below moved
> verbatim from NEXT_STEPS.md (was lines 2503-3623 at rotation time).

## GLM SUPPLEMENTAL ROUTING POLICY — IMPLEMENTED 2026-07-27

Policy codified in `AGENTS.md` §GLM SUPPLEMENTAL ROUTING (canonical, do not copy table elsewhere). Cross-references added to all required files. Stale `claude-opus-4-8` → `claude-opus-5` fixed in `SPRINT_WORKFLOW.md`.

- **[AI: Barış] AUTHORIZE (separate gate):** reconfigure the external helper that currently hard-maps all three tiers to GLM-5.2. No external config was changed in this update; this requires explicit Barış authorization before any helper change.
- **[AI: Any] MONITOR (Sep 2026):** temporary 1× off-peak quota cap expires Sep 2026. When quota rules change or new model entitlements are confirmed, update `AGENTS.md` §GLM SUPPLEMENTAL ROUTING (time-stamped facts are there).
- **[AI: Any] VERIFY on route change:** if active Z.AI route changes, confirm GLM-5.1 Coding Plan entitlement and update Tier 3 in `AGENTS.md` accordingly.
- **[AI: Any] HOLD:** no runtime, tool, broker, Pine, or schema changes in scope. Changes are doc/memory only.

## KVM2 MASTER PROGRAM — REPAIR CYCLE 2 ACTIVE / CLAUDE QUOTA BLOCKER (2026-07-26)

- **[AI: Codex] SCHEDULED:** one-time same-thread continuation
  `resume-kvm2-plan-repair-after-claude-reset` will run at 10:51
  Europe/Chisinau after the reported Claude reset.
- **[AI: Claude] FIRST AFTER 10:50 EUROPE/CHISINAU:** run the preserved focused
  repair prompt
  `11_TRIAGE/KVM2_MASTER_PLAN_REPAIR_CYCLE2_ROUND1_PROMPT_2026-07-26.md`
  against only the two plan documents and joint audit prompt. This is repair
  round 1 of the newly authorized cycle; do not replace Claude with another
  implementer.
- **[AI: Codex] THEN:** independently verify 77 unique exact Evidence/Stop task
  blocks, hashes, task counts, P5-05A/P5-06 and P6-03/P6-04/P6-05 dependencies,
  Phase-9 independent Gate 6 manifest acceptance and install→observe→remove
  sequencing, authority separation, privacy, sizes, crosswalk 1–10, and all
  original R3/DS findings.
- **[AI: Codex + Claude Opus] AUDIT:** only after lead validation passes, run fresh
  exact `gpt-5.6-sol` `xhigh` and `claude-opus-5` `xhigh` no-fallback audits. A
  non-accepting verdict returns to the same Claude implementer; maximum three
  repair/re-audit rounds in this new cycle.
- **[AI: Any] HOLD:** the current working hashes are not execution acceptance.
  No VPS/runtime, install, secret, network, deploy, cutover, TESTNET, ARM, lab,
  reprovision, purchase, mainnet, staging, commit, push, or PR action.

Current unaccepted working hashes: master
`3C61B08B17867C2EEB602FD407CF327C95FF7446DB492304DDB6A926A3E8EF3C`;
execution companion
`CB4C686A161CA8D40DC6C1C235B6371A4ADE1DCDDA23D2535259F39E0177C885`.

## KVM2 MASTER PROGRAM — FINAL AUDIT REQUEST_CHANGES / LOOP EXHAUSTED (2026-07-26)

Canonical joint inputs:

- `11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_MASTER_PLAN_2026-07-25.md`
- `11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md`
- `11_TRIAGE/KVM2_MASTER_PLAN_MULTI_MODEL_AUDIT_REPORT_2026-07-26.md`

- **[AI: Barış] NEW-CYCLE GATE:** explicitly authorize a new bounded repair cycle.
  The prior three-round repair/re-audit limit is exhausted; do not silently start
  a fourth round.
- **[AI: Claude] REQUIRED REPAIR:** apply only R3-01 through R3-07 and DS-F-01
  from the consolidated report. Preserve preparation-only status and all runtime
  authority separations.
- **[AI: Codex] REQUIRED RE-AUDIT:** after new joint hashes are frozen,
  independently reproduce the dependency graph, authority chain, task schema,
  crosswalk, privacy scan, and all required findings at exact
  `gpt-5.6-sol` `xhigh`.
- **[AI: Claude] DEFERRED CANONICAL AUDIT:** when credits are available, run a
  fresh exact `claude-opus-5` `xhigh`, no-fallback/no-resume audit. The current
  missing Opus verdict is not evidence.
- **[AI: Any] HOLD:** no install, deploy, secret transfer, runtime/API/process,
  cutover, TESTNET, ARM, lab admission, network change, reprovision, purchase,
  or mainnet action. The lower Bridge VPS Deploy task remains BLOCKED.

Frozen current hashes: master
`10C79396D63DE330BD4F920146B8CDB0C39C10C342233AEAE4E1C8B9CCD12F02`;
execution companion
`8706621CE52010465B408B265267F7320078E2A79F01533E85513335619615D9`.

## KVM2 MASTER PROGRAM — PLAN READY / ALL EXECUTION GATED (2026-07-25)

Canonical master plan:
`11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_MASTER_PLAN_2026-07-25.md`.

- **[AI: Any] FIRST:** re-verify drift-prone VPS, repo, PR, SHA, Windows writer,
  bridge state, listener, and audit facts. Resolve the audit-model wording conflict
  between current `AGENTS.md`/D020 and the older Bridge VPS task before launching
  any audit.
- **[AI: Claude] PREPARATION:** produce the two-profile clean rebuild kit
  (`temporary-testnet-lab` and `future-trading-only`) with trusted inputs, locked
  dependencies, service/firewall/ownership manifests, secret inventory without
  values, consistent state recovery, encrypted off-host restore proof, teardown,
  credential rotation, and reproducible bootstrap evidence. Do not install.
- **[AI: Any] AUDIT:** submit the immutable master plan and each executable child
  artifact to fresh exact-model Gate 5/Gate 6 review under the current canonical
  roster. Maximum three non-accepting repair rounds; no fallback.
- **[AI: Barış] OWNER GATES:** bridge deploy, cutover, ARM, each AI-lab workload,
  network exposure, destructive reprovision, purchase, and mainnet remain separate
  explicit decisions. AI-lab admission is forbidden until the canonical
  bridge-only stability window is accepted.
- **[AI: Any] HOLD:** no GitHub self-hosted runner, public bridge/webhook control
  path, agent Docker socket, heavy backtest, local large LLM, or mainnet on the
  mixed/lab image.

No install, deploy, secret, runtime, cutover, TESTNET, ARM, lab, network,
reprovision, purchase, or mainnet action is currently authorized.

## BRIDGE VPS DEPLOY — VPS READY / DEPLOY BLOCKED (2026-07-25)

Canonical preparation task:
`11_TRIAGE/BRIDGE_VPS_DEPLOY_TASK_LIST_2026-07-25.md`.

- **[AI: Claude] BUILD/AUDIT HANDOFF GATE:** prepare an exact clean merged release
  SHA containing accepted TS-P0 plus Linux deployment repairs, pinned/hash-locked
  Python 3.12 venv dependencies, non-root hardened systemd, private loopback-only
  control access, state-continuity policy, and complete release/rollback evidence.
  Obtain fresh independent Gate 5 and Gate 6 acceptance; do not deploy.
- **[AI: Any] READ-ONLY VERIFICATION GATE:** before any owner decision, re-verify
  live PR/SHA/runtime/reconcile/order/position/port/audit state because the task
  snapshot can drift. Preserve the dirty-main-worktree ban and single-writer stop
  sequence. The current exact `gpt-5.6-sol` `xhigh` verdict is **BLOCK with zero
  optional nits**; the HTTP-429 Opus attempt is not evidence.
- **[AI: Barış] OWNER GATES:** formally choose database migration versus a
  conservative risk-state reset; later authorize deploy only after exact audits;
  authorize ARM separately, if ever. The >=10-day counter starts only at the final
  approved VPS ARM. No current merge/deploy/install/secret/runtime/TESTNET/ARM
  authority; mainnet remains forbidden.

## TS-P1-001 SECOND-REPAIR RE-AUDIT BLOCK — immutable holder repair required

- **[AI: Claude] NOW:** run
  `11_TRIAGE/CLAUDE_TSP1001_REPAIR3_PROMPT_2026-07-21.md` against exact parent
  `a15a6b1f6648016fe99278fe993daa2c1b49b923`. Fix only the writable `_pairs`
  holder; create one new local child commit.
- **[AI: Codex] AFTER REPAIR:** independently audit the new immutable commit without
  repairing it in the audit pass.
- **[AI: Baris] OWNER GATE:** only after technical PASS, accept or reject the PROPOSED
  TS-P1-001 contract and five open design questions.
- **[AI: Any] HOLD:** do not create or execute TS-P1-002; no push/PR/merge/migration/
  testnet/P2RT/deployment authority.

Verified: parent RED 5 failed/80 passed; repaired focused 85/85; full 303/303 both
CWDs; compile clean; oracle 44/121; F2-R closed. Residual direct-slot mutation evidence
is in `11_TRIAGE/CODEX_TSP1001_REAUDIT2_2026-07-21.md` (**BLOCK**).

## TS-P1-001 RE-AUDIT BLOCK — second bounded repair required

- **[AI: Claude] NOW:** run
  `11_TRIAGE/CLAUDE_TSP1001_REPAIR2_PROMPT_2026-07-20.md` against exact parent
  `851d88a084875e48b63fba455cb7b27f357c5ac4`. Fix only mutable proxy referents and
  hostile-metaclass error escape; create one new local child commit.
- **[AI: Codex] AFTER REPAIR:** independently re-audit the new immutable commit; do
  not repair it in the audit pass.
- **[AI: Baris] OWNER GATE:** only after technical PASS, accept or reject the PROPOSED
  TS-P1-001 invariant contract and its five open design questions.
- **[AI: Any] HOLD:** do not create or execute TS-P1-002. No push, PR mutation, merge,
  migration, testnet, P2RT, or deployment authority is implied.

Verified evidence: repair regressions RED on parent (5 failed/75 passed), repaired
focused 80/80, full 298/298 from both CWDs, compile clean, scope clean, oracle 44/121.
Residual F1-R/F2-R runtime attacks are in
`11_TRIAGE/CODEX_TSP1001_REAUDIT_2026-07-20.md` (**BLOCK**).

## TS-P1-001 AUDIT BLOCK — repair commit and independent re-audit required

- **[AI: Claude] NOW:** run
  `11_TRIAGE/CLAUDE_TSP1001_REPAIR_PROMPT_2026-07-20.md` in a fresh session against
  audited parent `5140e062b8c1f3fcc78e96c7357060c60a51285d`. Fix only the reproduced
  mutable-policy and exception-contract findings; create one new local repair commit.
- **[AI: Codex] AFTER REPAIR:** independently re-audit the new immutable commit. Do
  not act as builder in the re-audit pass.
- **[AI: Baris] OWNER GATE:** after a passing re-audit, accept or reject the PROPOSED
  TS-P1-001 invariant contract, including the five open design questions.
- **[AI: Any] HOLD:** do not create or execute a TS-P1-002 build prompt yet. No push,
  PR mutation, merge, migration, testnet, P2RT, or deployment authority is implied.

Audit evidence: `11_TRIAGE/CODEX_TSP1001_AUDIT_2026-07-20.md` (**BLOCK**). Scope,
semantic parent RED, 74 focused tests, 292 full tests from both CWDs, compile, and the
121-pair/44-legal oracle passed; the mutable backing seeds and unsafe/unreason-coded
exceptions block acceptance.

## 🟦 39-TASK SEQUENCE START — TS-P1-001 builder then independent Codex audit

Barış selected the workflow: Claude builds one backlog task and reports; Codex audits
the immutable commit, routes BLOCK back to repair or PASS forward to the next task.
First task: TS-P1-001 canonical order-state invariants. Prompts:

- Claude builder: `11_TRIAGE/CLAUDE_TSP1001_BUILD_PROMPT_2026-07-20.md`
- Codex auditor/manager: `11_TRIAGE/CODEX_TSP1001_AUDIT_MANAGER_PROMPT_2026-07-20.md`

One task at a time. No next task, push, merge, deploy, migration, or testnet action is
implied by build/audit success. TS-P1-001 invariant contract remains Barış-accepted only
after the independent audit and explicit owner review.

## ✅ TS-P0 DOCUMENTATION CLOSEOUT DONE — PR #25 ready at `cfb08b81`

N3/N4/N5 are closed. The tracked contract markers and N5 limitation were committed
as `cfb08b81` and pushed; PR #25 is OPEN, non-draft, CLEAN, with available checks
passing: https://github.com/bsemaay-tech/mtc-command-center/pull/25. N3/N4 live only
in pre-existing untracked main-worktree docs and remain deliberately uncommitted;
they were not smuggled into the TSP0 branch.

- **[AI: Barış] MERGE GATE:** still requires an explicit “merge PR #25” instruction.
- **[AI: Barış] DEPLOY GATE/TIMING:** separately decide after merge and after the chosen
  Day 1 v2 checkpoint; deployment would interrupt the current window.
- **[AI: Codex|Claude] NEXT LARGE TASK AFTER TS-P0 MERGE:** design TS-P1-001 canonical
  order-state invariant contract for Barış review; no implementation before its gate.

Report: `11_TRIAGE/CODEX_TSP0_DOC_CLOSEOUT_REPORT_2026-07-20.md`.

## ✅ TS-P0 published + Day 1 v2 OPEN 2026-07-20

Owner gates are closed: hash scope approved, release-evidence contract approved, and
sticky reset policy confirmed with 300-second tolerance. Exact audited commit
`44338d61` was pushed on `feature/ts-p0-baseline`; draft PR #25 targets `master`:
https://github.com/bsemaay-tech/mtc-command-center/pull/25. **No merge or deploy.**

Day 1 v2: monitoring PC awake policy verified (sleep/hibernate/lid action all disabled
on AC and DC); exactly one task start and one ARM succeeded. Run
`paper-20260720090332` is ARMED paper/testnet from `2026-07-20T09:05:10Z`, task Running,
fresh reconcile, positions/orders empty, P2RT clean at `008e065e`, thresholds unchanged.
Record: `11_TRIAGE/CODEX_TSP0_PUBLICATION_DAY1V2_2026-07-20.md`.

- **[AI: Any] MONITOR DAY 1 v2 READ-ONLY:** keep evidence categories separate; any
  interruption resets the continuous window under the confirmed sticky policy.
- **[AI: Codex] NEXT DOCS-ONLY CLOSEOUT:** execute
  `11_TRIAGE/CODEX_TSP0_REMAINING_DOCS_PROMPT_2026-07-20.md` for N3/N4/N5 and approval
  markers. No commit/push/PR mutation until a separate reviewed docs-only gate.
- **[AI: Barış] PR #25:** merge and deploy remain explicitly unapproved.

## ✅ INCIDENT FOLLOW-UP 2026-07-20: Day 1 v1 closed; Day 1 v2 opened

Bridge died with system sleep; logon-trigger restart at 08:57 died again in ~66s
(second standby). Continuous window = ARM 18:52Z → ~04:27Z ≈ **9h35m**, then INTERRUPTED.
Not related to any TSP0 session. Record: `11_TRIAGE/INCIDENT_D1V1_SLEEP_STOP_2026-07-20.md`.

- **RESOLVED:** Barış selected the awake-PC policy and authorized Day 1 v2. Exactly one
  task start and one ARM succeeded; see the top entry and execution record.
- **STANDING LIMIT:** local remains validation-tier; definitive uninterrupted evidence
  remains planned for VPS.

## ✅ TS-P0 BLOCK REPAIR RE-AUDIT PASS 2026-07-20 — published at `44338d61`

Fable independently re-audited the Codex nine-file repair: **PASS, zero new findings**
(`11_TRIAGE/FABLE_TSP0_BLOCK_REPAIR_AUDIT_2026-07-20.md`). Reproduced: 218×2 both CWDs;
RED 9F/45P vs HEAD (copy-aside, byte-exact restore); F1a×4/F1b/F2×5/F3 replays all
fail-closed; overbroad-denylist attack clean (real-tree hash set unchanged); real-pair
exit 2 incl. `repo_dirty`; P2RT untouched. Auditor committed the audited state as
**`44338d61`** to end the uncommitted-repair hazard. Barış later closed all three owner
gates and authorized exact-SHA publication; draft PR #25 is open with no merge/deploy.

- **[AI: Any] DOCS NITS (small, unblocked):** close N3 integration-note, N4 three stale
  ADR "Proposed status" sentences, N5 symlink limitation — docs-only pass.
- **DONE:** hash scope approved; release contract approved; sticky reset policy confirmed
  with 300-second tolerance; exact `44338d61` pushed and draft PR #25 opened.
- **[AI: Barış] REMAINING GATE:** any docs follow-up commit/push, PR merge, or deploy needs
  a separate explicit instruction.

Repair report: `11_TRIAGE/CODEX_TSP0_BLOCK_REPAIR_REPORT_2026-07-19.md`.

## ⛔ CODEX TS-P0 CROSS-AUDIT BLOCK 2026-07-19 — repair before push/PR

- **[AI: Claude] TS-P0-003 REQUIRED REPAIR:** malformed persisted timestamp
  evidence (especially `window_interrupted_ts`) must fail DOWN, and future
  liveness must not count as fresh. Add committed invalid-meta/future-clock tests.
- **[AI: DeepSeek] TS-P0-002 REQUIRED REPAIR:** validate manifest container and
  scalar types before dereference; re-signed `"hashes": []` must return a
  structured exit 2 without traceback. Add wrong-shape tests.
- **[AI: DeepSeek] TS-P0-001 REQUIRED REPAIR:** extend/document secret exclusions
  for conventional `*.env` and `*.secrets`; decide `key.txt`; add spy/no-leak tests.
- **[AI: Codex] RE-AUDIT AFTER REPAIR:** rerun focused 14/11/21, 210/210 both
  CWDs, real-pair integration, and the three failed adversarial probes. Keep
  `C:\P2RT` read-only. Report: `11_TRIAGE/CODEX_TSP0_AUDIT_2026-07-19.md`.
- **[AI: Barış] PUSH/PR GATE:** remains blocked. The final-HEAD integration's
  third `source_tree_hash_mismatch` reason is correct and must not be removed by
  weakening the declared hash scope.

## ✅ DEPLOYED + WINDOW OPEN 2026-07-19 — Day 1 v1 ARMED on `008e065e`; monitor + TS-P0-001 next

Barış approved and Fable executed the full deploy gate: PR #24 merged (`008e065e`),
`C:\P2RT` deployed + verified (32/164 tests in deployed tree), `MTC-Bridge-P2` started
18:50:25Z, run `paper-20260719185026` paper/testnet ARMED ~18:52:44Z. Record:
`11_TRIAGE/DEPLOY_TSP1007_WINDOW_D1_2026-07-19.md`.

- **[AI: Any] WINDOW MONITORING:** check bridge log + `/api/status` + events periodically;
  this window's risk-gate enforcement evidence COUNTS (first deployed audited wiring).
  Categories stay separate (connectivity / reconnect / scheduler / risk-enforcement).
  Definitive ≥10d D3 on VPS remains end-of-month plan.
- ~~**[AI: Claude] PHASE 0 BUILD CHAIN (Barış directed 2026-07-19, Fable builds)**~~
  **DONE 2026-07-19:** TS-P0-001..004 built in `C:\TSP0` (`feature/ts-p0-baseline`,
  commits `fa449ce2`/`42d0ca9f`/`7777273f` + docs-only P0-004), 210/210 both CWDs,
  no push/deploy, window untouched. Report: `11_TRIAGE/FABLE_TSP0_BUILD_REPORT_2026-07-19.md`.
- ~~**[AI: Codex] INDEPENDENT TS-P0 AUDIT**~~ **FABLE AUDIT DONE 2026-07-19:
  PASS-WITH-NITS** (`11_TRIAGE/FABLE_TSP0_INDEPENDENT_AUDIT_2026-07-19.md`).
  Fresh Fable session executed the full 12-point checklist: 210/210 both CWDs,
  3 RED proofs reproduced, real-pair integration exit 2 + P2RT untouched, re-sign
  attack caught, exhaustive window sweep verified. 5 nits: N1 release_evidence
  exit-1 crash on re-signed non-dict `hashes`; N2 `prod.env` denylist gap;
  N3 handoff's stale integration expectation (3 drift reasons at HEAD is CORRECT);
  N4 three residual "Proposed status" sentences (ADR-0020:62/0025:51/0029:49);
  N5 symlink digest-oracle note. **[AI: Barış]** decide: accept Fable audit or
  also run Codex cross-audit per `CODEX_TSP0_AUDIT_PROMPT_2026-07-19.md`; push/PR
  of `feature/ts-p0-baseline` stays gated until then.
- **[AI: Codex|Claude] TS-P0 NIT-FIX BUILD (after Codex audit reconciled):**
  execute `11_TRIAGE/TSP0_NITFIX_BUILD_PROMPT_2026-07-19.md` — N1 exit-code fix
  (TDD, subprocess RED), N2 conditional on Barış hash-scope answer, N4 three ADR
  wording fixes, N5+N3 doc corrections; one commit in C:\TSP0, no push. Stage 2
  push/PR separately gated on Barış's 3 approvals.
- **[AI: Barış] TS-P0 decisions after audit:** (1) TS-P0-001 hash scope confirm
  (RUNTIME_BASELINE_CONTRACT.md), (2) TS-P0-002 release-evidence contract approval
  (currently DRAFT), (3) TS-P0-003 window reset-policy confirm (currently PROPOSED).
- **[AI: Claude|Codex] NON-BLOCKING NITS (fold into full TS-P1-007):**
  add committed tests for `ORDER_OVERFILL` + `FILL_ROLE_CONFLICT`; persist the conflicting
  role fill as evidence (retention asymmetry); close the narrow ENTRY_REMAINDER_LIVE
  crash window (missed DISARM only); fix stale "INSERT OR REPLACE" comment at
  `tests/test_interim_risk_wiring.py:674`.
- **[AI: Barış]** live/mainnet remains BLOCKED (gate unsigned); D017 funding exclusion
  stands until TS-P1-005 funding ledger.

## ✅ INTERIM TS-P1-007 ROUND-4 AUDIT PASS-WITH-NITS 2026-07-19 — deploy executed above

Fable independently audited `acb83b5b` and issued **PASS-WITH-NITS**
(`11_TRIAGE/FABLE_INTERIM_TSP1007_ROUND4_AUDIT_2026-07-19.md`). All builder evidence
reproduced (32×2 focused, 164×2 full, parent red 8F/24P exact-match, half-exit 1F vs
`066b49cc`) plus 14 independent adversarial probes, all pass. All five round-3 BLOCK
findings closed.

## INTERIM TS-P1-007 ROUND-4 REPAIR BUILT 2026-07-18 - audited PASS-WITH-NITS above

Codex commit **`acb83b5b`** in clean `C:\P1IF` repairs the round-3 late/conflicting-fill,
partial-decision, live-entry-remainder, overfill, atomic-close, and semantic-test findings.
Evidence: **32x2 focused; 1x2 regression; 164x2 full; parent semantic red 8F/24P; old-code
half-exit red 1F; final clean 32P**. Audit brief:
`11_TRIAGE/FABLE_INTERIM_TSP1007_ROUND4_AUDIT_HANDOFF_2026-07-19.md`.

- ~~**[AI: Claude] FABLE INDEPENDENT AUDIT 2026-07-19**~~ DONE 2026-07-19: PASS-WITH-NITS.
- **[AI: Barış] DEPLOY GATE:** remains separate and unspent. No push, PR, merge, or deploy before
  explicit owner approval. D017 funding exclusion is unchanged.
- The round-3 repair bullets immediately below are completed by `acb83b5b` and now
  independently confirmed by Fable; retained as audit trace.

## ⛔ INTERIM TS-P1-007 ROUND-3 RE-AUDIT BLOCKED 2026-07-18 — do not push/deploy

Codex audited `3fa13f3e` code plus documentation-only D017 commit `b11a2e36`. Scope and reported suites passed (**24×2 focused; 156×2 full; regression ×2; semantic red 5F/19P**), but late/conflicting fills can still rewrite closed PnL or leave unprotected exposure. Report: `11_TRIAGE/CODEX_INTERIM_TSP1007_REAUDIT2_2026-07-18.md`.

- **[AI: Claude] REQUIRED REPAIR:** closed trades must be immutable. Detect `exit_qty > entry_qty`, mixed SL/TP/CLOSE races, and any distinct post-close fill; persist the anomaly separately and force reconciliation/quarantine without rewriting canonical PnL. Make close + `TRADE_CLOSED` atomic.
- **[AI: Claude] REQUIRED REPAIR:** replace mutable `INSERT OR REPLACE` fill semantics with insert-once outcomes. Exact duplicates are no-ops; changed payloads for an existing `fill_id` fail closed; partial-exit decisions remain idempotent across restart.
- **[AI: Claude] REQUIRED REPAIR:** do not terminally close a flat partial entry while its owned entry remainder is live. Cancel/confirm or quarantine it; a later entry fill must never become `FOREIGN_POSITION_IGNORED`. Add restart/reconcile proof.
- **[AI: Claude|DeepSeek] TEST REPAIR:** make the half-exit engine test cross the old `-2000` daily boundary; its current old-code phantom loss is only `-100`, so the test is not semantic red evidence.
- **[AI: Codex] RE-AUDIT:** rerun both-CWD suites and semantic red proof, plus mixed SL/TP, conflicting duplicate, partial-decision duplicate, late-entry, crash-window, and reconciliation attacks.
- **[AI: Barış] DEPLOY GATE:** remains separate and unspent. D017 funding exclusion is accepted and is not the current blocker; no monitoring window may count before a non-BLOCK audit and separate deploy approval.

## 2026-07-18 REVIEW OUTCOME — pending Barış approvals + corrections applied [AI: Fable]

Devil's-advocate review of the 2026-07-17 package: **PROCEED WITH REQUIRED CORRECTIONS** (full record: GLOBAL_HANDOFF 2026-07-18). Corrections applied same day. Pending Barış approvals, in priority order:

1. ⛔ **Interim TS-P1-007 round-3 audit BLOCK.** D017 accepted interim funding exclusion, but `3fa13f3e` remains unsafe under post-close overfill/mixed-role fills, conflicting duplicate IDs, and late fills from a remaining partial-entry order. Complete the narrow repairs above, then independent re-audit; no push/PR/deploy or risk-control monitoring window yet.
2. ✅ **PR #23 MERGED 2026-07-18T12:20:45Z** (merge commit `abda6717`; Barış approval, executed by Fable). Verified: `74e0990b` is an ancestor of `origin/master` and `git diff 74e0990b origin/master -- IBKR_PAPER_BRIDGE/` is empty — master bridge tree is byte-identical to the deployed runtime. TS-P0-001 manifests must baseline against post-merge master.
3. ✅ **ADR ratification COMPLETE — D016 + same-day addendum (2026-07-18):** Barış accepted ALL TWELVE (ADR-0018 through 0029); files + index flipped. Qualifications: 0020/0024 direction-only (evidence-gated); 0029 framework-only — live gate UNSIGNED, live/mainnet BLOCKED, nothing operational signed.
4. ✅ **Scheduler policy — DONE 2026-07-18:** `StopIfGoingOnBatteries=False` on `MTC-Bridge-P2` (set by Fable; task stayed `Ready`); Task Scheduler history ENABLED (Barış ran the admin wevtutil command). `DisallowStartIfOnBatteries` remains True (untouched — task will not START while on battery; flag to Barış if unwanted).

## TRADING-SYSTEM ROADMAP — SINGLE IMMEDIATE NEXT TASK 2026-07-17 [AI: DeepSeek]

**TS-P0-001 — Add a read-only repository/runtime baseline manifest and drift checker.**

Governing ADRs: ADR-0019 and ADR-0027. Canonical task card:
`09_DOCS\ROADMAPS\TRADING_SYSTEM\05_IMPLEMENTATION_BACKLOG.md#ts-p0-001--add-a-read-only-repositoryruntime-baseline-manifest-and-drift-checker`.

Exact scope:

- Add an offline CLI that compares an explicitly supplied repository root and runtime root.
- Read Git HEAD/status and selected bridge source/config hashes; emit deterministic JSON and Markdown evidence.
- Exit `0` for exact clean match, `2` for drift/dirty/missing runtime, and `3` for invalid evidence input.

Required files:

- `IBKR_PAPER_BRIDGE\tools\check_runtime_baseline.py`
- `IBKR_PAPER_BRIDGE\tests\test_runtime_baseline.py`
- `IBKR_PAPER_BRIDGE\docs\RUNTIME_BASELINE_CONTRACT.md`
- One dated run report plus normal `GLOBAL_HANDOFF.md`/`NEXT_STEPS.md`/`ACTIVE_FILES.md` updates.

Acceptance criteria and tests:

- Manifest reports schema version, canonical paths, repository/runtime commits and dirty flags, selected hashes, config hash and explicit verdict.
- Unit coverage: clean match, commit drift, dirty repo/runtime, missing runtime, changed config, invalid Git output, stable ordering, secret-safe output and no-mutation behavior.
- One audited read-only local invocation must report the current repository/runtime relationship while leaving both trees unchanged.

Explicit out of scope: no branch merge, checkout, deploy, restart, ARM/DISARM/KILL, HTTP/exchange call, credential read, database or scheduler action, dependency/config/schema change, or trading/risk/order/strategy behavior change. `C:\P2RT` remains protected. The bridge API was unavailable during the 2026-07-17 roadmap baseline, so the prior Day 0 v5 window must not be represented as currently active or uninterrupted.

## ❌ P2 DAY 0 v5 CLOSED 2026-07-18 — killed by scheduler battery policy 2026-07-16 ~17:32 (see `11_TRIAGE/INCIDENT_P2_BATTERY_STOP_2026-07-16.md`); 300s fix remains deployed + field-proven; NO active window; daily D3 check suspended until next approved window

Task B (`79976577`+`74e0990b`, PR #23 draft) Fable-audited **PASS** and deployed same day:
P2RT detached `74e0990b`, 132×2 both CWDs (incl. inside P2RT), supervisor `MTC-Bridge-P2`, run
`paper-20260716132819`, >13-min gate, ONE ARM, flat. **Live proof: a real HL outage during the
gate ended with the first fresh bar 118s after reconnect — the old 60s trigger (v4 killer)
would have disarmed; the 300s window absorbed it** (zero DATA_STALE/ERROR). Full record:
`11_TRIAGE/FABLE_AUDIT_P2_TIMEOUT_FIX_2026-07-16.md` + GLOBAL_HANDOFF same date.
- **[AI: Any]** daily D3 check: `/api/status` ARMED + fresh reconcile + `[]`/`[]` + P2RT pinned
  `74e0990b` clean. Benign ~10-min feed cycles + `RECONCILE_FAILED_TOLERATED` WARNs = expected.
  **Jul-18 planned PC-off = window boundary (v5 resets), NOT an incident.** Definitive ≥10-day
  D3 on the VPS (end of month).
- **[AI: Codex]** NEXT: PR #22 edit round —
  `11_TRIAGE/CODEX_PR22_REQUIRED_EDITS_PROMPT_2026-07-16.md` (10 required edits + A2
  claim-narrowing + adversarial tests proven failing on `f72b377a`); STOP for Fable re-review.
- **[AI: Claude]** re-review the edit round on real code; then the single formal run-approval
  question to Barış.
- **[AI: Barış]** merge decisions: PR #23 (deployed fix), PRs #20/#21 (docs-only) — any time.

## ~~🔴 P2 DISARMED — Day 0 v4 died 2026-07-15T20:22:44Z~~ RESOLVED by Day 0 v5 above

Day 0 v4 lived 8h20m; reconcile N=3 tolerance WORKED; killer was `data_restore_timeout_s=60s`.
Barış approved 60→300s 2026-07-16 → Codex Task A (Gate-5, BLOCK, Fable-verified) + Task B
(timeout fix) both delivered 2026-07-16; deploy = Day 0 v5 (section above).

## 🔴 FAZ3B PR #22 — independent Gate-5 = BLOCK (Fable-verified 2026-07-16); 10 REQUIRED EDITS queued

Codex Gate-5 (`11_TRIAGE/CODEX_GATE5_FINDINGS_PR22_2026-07-16.md`) found 4 FATAL areas; Fable
confirmed ALL on real code (`11_TRIAGE/FABLE_AUDIT_CODEX_GATE5_PR22_2026-07-16.md`): A4 primary
DSR non-executable (engine NaN at grid_n=1, no du_cell tool exists), A5 gauntlet geometry
mutable/unasserted, A6 runner argv+manifest+commit+post-run guard bypasses, A9 pre-reg §8↔§10
decision-table contradictions. 108/108 tests reproduce; engine byte-identity holds; virginity
scan clean (local corpus). **No run, no approval question, D016 unspent** until:
- **[AI: Codex]** execute `11_TRIAGE/CODEX_PR22_REQUIRED_EDITS_PROMPT_2026-07-16.md` (after
  Task B): 10 edits + A2 claim-narrowing + adversarial tests proven failing on `f72b377a`.
- **[AI: Claude]** independent re-review of the edit round on real code; then present the
  run-approval question to Barış.

## ✅ P2 DAY 0 v4 ARMED 2026-07-15T12:02:42.856537Z + ALL PRs MERGED (Fable audit PASS)

Outage-tolerance fix deployed (P2RT detached `1465f8f0`, 130 tests); one ARM; zero
FAILED/TOLERATED/STALE since; flat. **Master consolidated `8721bce0`: PR #16/#17/#18/#19 all
MERGED** (Fable finished #19 registry + handoff union after Codex correctly stopped; e0651f94
Day-0-v4 report folded in; bridge suite 130 on master). Full record: GLOBAL_HANDOFF
`[Claude Fable 5] 2026-07-15 — DEPLOY (Day 0 v4) + PR MERGE AUDIT`.
- **[AI: Any]** daily D3 check unchanged; **Day 0 v4 resets at the Jul 18 planned PC-off — that
  is a window boundary, NOT a safety incident.** Definitive ≥10-day D3 runs on the VPS (end of
  month). Benign feed noise now suppressed from Telegram; `RECONCILE_FAILED_TOLERATED` (WARN, no
  disarm) during a real outage = correct new behavior, not a failure.
- **[AI: Any, low priority]** tidy master `NEXT_STEPS.md` union artifacts (superseded FAZ3B/bridge
  sections) next session; remove merged worktrees C:/BTOL, C:/FZ3G5.

## CRYPTO PAPER BRIDGE P2 — TIMEOUT FIX BUILT; FABLE AUDIT/DEPLOY LOCKED 2026-07-16 [AI: Claude]

Approved 60-to-300-second data-restore timeout wiring is built in commit `79976577` on
`feature/ibkr-bridge-final`. Final focused tests failed on pre-fix code (`1 failed, 2 passed`), then
passed after the fix (`3 passed`); both full suites pass `132 passed, 1 warning` from both
supported CWDs. `bars.py` is unchanged. Report:
`11_TRIAGE/P2_DATA_RESTORE_TIMEOUT_REPORT_2026-07-16.md`.

- **[AI: Claude]** independently audit real code at `79976577`, rerun both full suites, and
  reproduce the focused failure against pre-fix code. Do not trust the Codex report.
- **[AI: Claude|Codex]** only after Fable records PASS, execute the existing single testnet
  deploy window: detach `C:\P2RT` to the audited tip, rerun both suites, supervisor start,
  at least 10-minute gate including verified fresh bars, then exactly one authorized ARM.
- **[AI: Any]** until audit PASS, keep the runtime DISARMED and leave clean detached
  `C:\P2RT` at `1465f8f0`. Mainnet remains forbidden.

## SUPERSEDED — CRYPTO PAPER BRIDGE P2 ARMED, NEW DAY 0 2026-07-15T06:48:16.619336Z

Fable-audited race fix `da44d1ff` is deployed in detached `C:\P2RT` at `cc4ce67d`. Run
`paper-20260715063657` passed the required 10-minute reconnect gate and two post-ARM reconciles.
Exactly one ARM request/transition occurred; final state was ARMED and reconcile-ready with
positions/orders `[]` and zero ERROR/reconcile-failure/defer events.

- **[AI: Any]** daily read-only D3 check: state/reconcile freshness, WARN/ERROR events, equity,
  process/commit identity, all positions/orders, and native stops for any owned position.
- **[AI: Claude|Codex]** on any safety anomaly: preserve evidence, DISARM safely if necessary,
  diagnose, and do not repeat ARM without a fresh complete gate.
- **[AI: Barış]** keep the host/supervisor available for at least 10 uninterrupted calendar days;
  any shutdown or critical runtime change resets the P2 clock.
- Evidence: `IBKR_PAPER_BRIDGE/docs/03_STATUS.md` and
  `MTC_COMMAND_CENTER/11_TRIAGE/P2_RACE_FIX_REPORT_2026-07-14.md`.

## SUPERSEDED — P2 RACE FIX BUILT; AUDIT/DEPLOY LOCKED 2026-07-14

Commit `da44d1ff` on `feature/ibkr-bridge-final` implements the atomic reconnect client swap,
narrow rebuild-only reconcile deferral, and deterministic regressions. Both full suites passed
`127 passed, 1 warning`; report: `11_TRIAGE/P2_RACE_FIX_REPORT_2026-07-14.md`.

- **[AI: Claude]** Fable adversarial audit on the real commit and independent suite rerun.
- **[AI: Barış]** only after Fable PASS, explicitly approve or reject Task 4's single deploy/re-arm
  window. No approval is inferred from the build request.
- **[AI: Claude|Codex]** after both gates, execute Task 4 exactly once with its stop conditions;
  otherwise leave `C:\P2RT` and the DISARMED runtime untouched.

## SUPERSEDED — P2 ARMED, D3 STARTED 2026-07-13

Day 0 started `2026-07-13T13:00:28.6218649Z` after incident containment, commit `59c334c0`, full
tests `119 passed` from both roots, and a real
`DISCONNECT -> RECONNECT -> DATA_RESTORED -> two reconciles` gate. Runtime is pinned at `C:\P2RT`;
## BRANCH CONSOLIDATION — FABLE AUDIT DONE 2026-07-13: content PASS + 1 MAJOR finding

Codex's queue 2a–2c + Telegram test-isolation work **VERIFIED PASS** on real code/runs (Fable,
2026-07-13): golden ancestor confirmed, 122/122 both CWDs independently re-run at `960369b9`,
secret greps 0, no push (branches absent on origin), bridge-vs-master conflict probe clean.
Full audit record: GLOBAL_HANDOFF `[Claude Fable 5] 2026-07-13 — CONSOLIDATION AUDIT`.
- ~~P2RT git identity repair~~ **DONE 2026-07-13 (Barış approved, Fable executed):**
  `git -C C:/P2RT checkout --detach 54278b66` — pre/post diffs empty, zero file writes, bridge
  stayed ARMED. P2RT `git log` truthful again; branch freed. Daily pinned-identity check can use
  `git -C C:/P2RT log --oneline -1` (= `54278b66` detached) + `diff 54278b66 --stat` empty.
- ~~push/open four PRs~~ **DONE 2026-07-13 (Barış approved):** PR #16 bridge → #17 UI →
  #18 faz3b-prereg → #19 donchian, merge in that order; secret scans zero; recommended
  union-resolution for `GLOBAL_HANDOFF.md`/`NEXT_STEPS.md` conflicts noted in PR bodies.
- **[AI: Barış]** merge PRs #16→#17→#18→#19 in order on GitHub (union-resolve shared handoff
  files in #17..#19). P2RT sync to the consolidated tip stays a planned restart-window decision.
- ~~queue 3: Gate-5 adversarial review~~ **DONE 2026-07-13**: Codex verdict FATAL (`1859910c`),
  Fable re-verified decisive claims on raw artifacts/code — CONFIRMED. Prereg marked BLOCKED
  (`f32a354c`); PR #18 updated. See FAZ 3B section below for the D016 decision now owed by Barış.

## CRYPTO PAPER BRIDGE P2 — 🔴 DISARMED 2026-07-15T08:40:06Z (real HL outage; Day 0 v3 dead after 1h52m); POLICY DECISION PENDING

Second real Hyperliquid testnet outage in ~26h (`ServerError` on reconnect ×5 AND on the
reconcile REST call) → fail-closed disarm. **Race fix HELD (zero DEFERRED, zero
NotConfigured) — not a code defect.** Both safety triggers (reconcile single-strike +
DATA_STALE after ~80s) fire on any ~2-min exchange outage → **P2 ≥10 days unreachable
without an outage-tolerance policy change.** Zero exposure; equity intact; reconcile
recovered 08:42:07Z. ⚠️ No `DATA_RESTORED` seen after recovery yet — verify fresh bars
before any ARM.
- ~~policy decision~~ **DONE 2026-07-15: Barış approved option (a).** Codex prompt written:
  `11_TRIAGE/CODEX_P2_OUTAGE_TOLERANCE_PROMPT_2026-07-15.md` — reconcile N=3 consecutive-strike
  tolerance + ~5-min reconnect budget before DATA_STALE + notify-threshold (suppress routine
  DISCONNECT/RECONNECT-attempt1/DATA_RESTORED) + tests. Fail-closed principle preserved.
- ~~build policy fix (Tasks 1-4)~~ **DONE + Fable audit PASS 2026-07-15** (`0e644b52`, 130 tests
  both CWDs, 4 new tests proven failing on pre-fix code, trade-path safety verified). Task 5
  deploy CLEARED on Barış go; Task 6 PR merges CLEARED.
- **[AI: Barış] 🔴 P2 bridge PROCESS is DOWN** (supervisor exited ~09:57Z; DISARMED/flat/safe —
  monitoring gap only, no trading risk). Your go on the Task-5 deploy is now the clean restart
  (brings the audited fix live, Day 0 v4 validation-tier). Or say the word to relaunch the
  supervisor on old code just to restore monitoring. Runbook:
  `11_TRIAGE/CODEX_P2_OUTAGE_TOLERANCE_PROMPT_2026-07-15.md` §Task 5.
- **[AI: Codex]** on Barış go: Task 5 deploy (child already stopped → detach P2RT to audited tip
  → suites → supervisor → gate → ONE ARM → Day 0 v4) + Task 6 PR merges #16→#19.
- **[AI: Any]** do NOT re-ARM before Fable audit PASS + full gate incl. verified fresh bars.
- **PC uptime (Barış 2026-07-15):** ON now → Jul 18 Sat (~2h off) → ON → Jul 20 (~2h off am)
  → 6 days uninterrupted → pattern continues. **VPS end of month.** No pre-VPS window reaches
  ≥10 uninterrupted days — any PC ARM is policy VALIDATION; the definitive D3 clock starts on
  the VPS. Planned PC-offs are window boundaries, NOT safety incidents.

Superseded record (Day 0 v3, dead): DAY 0 v3 = 2026-07-15T06:48:16.619336Z [AI: Any]

Race incident (Day 0 v2 died 16:46:42Z Jul 13) → fix `da44d1ff` (atomic client swap +
RECONCILE_DEFERRED guard; 127 tests; new tests proven failing on pre-fix code) → Fable audit
PASS → Task-4 single restart window executed 2026-07-15: `C:\P2RT` detached at `cc4ce67d`
(race fix + conftest Telegram isolation + golden all live), run `paper-20260715063657`,
pre-ARM gate passed, ONE ARM at 06:48:16Z, zero ERROR/FAILED/DEFERRED, live proof: reconcile
succeeded INSIDE a reconnect window (06:47:26). Deploy audit: GLOBAL_HANDOFF
`[Claude Fable 5] 2026-07-15 — DEPLOY AUDIT: PASS`. PR #16 tip `8e53439e`.
- **[AI: Any]** daily read-only D3 check: state/reconcile freshness, WARN+ events (benign =
  ~10-min DISCONNECT→RECONNECT attempt=1→DATA_RESTORED; occasional single RECONCILE_DEFERRED
  during a rebuild is expected and harmless), equity, positions/orders + native stops,
  process identity, pinned check = P2RT detached `cc4ce67d` + clean status.
- **[AI: Claude|Codex]** any safety anomaly: preserve evidence, DISARM if needed, diagnose;
  no re-ARM without fresh complete gate. **D3 target: ≥10 uninterrupted days → 2026-07-25+.**

Previous window record (superseded): Day 0 RESET to `2026-07-13T15:17:05.383618Z` after the approved EMA-8 trail fix `f209acd2`
(SMA-8 → exact QuantLens EMA convention) landed in `C:\P2RT` and one clean deploy+re-ARM cycle
(run `paper-20260713150651`, tests `121 passed` from both roots, one ARM_REQUEST, post-ARM
reconnect gate passed). Fable audited 2026-07-13 against real code/runs: PASS. Earlier Day 0
(`13:00:28Z`, `59c334c0`, 119 tests) is superseded — that run auto-disarmed at `13:29:59Z` on
`DATA_STALE` (fail-closed worked). Runtime is pinned at `C:\P2RT` at `54278b66`;
Task Scheduler must never be redirected to the parallel-agent research checkout.
- **[AI: Any]** daily read-only D3 check: state/reconcile freshness, WARN/ERROR events, equity,
  process/commit, all positions/orders, and native stops for any owned position.
- **[AI: Claude|Codex]** any safety anomaly: preserve evidence, DISARM safely if needed, diagnose;
  do not repeat ARM without a fresh complete gate.
- Evidence: `IBKR_PAPER_BRIDGE/docs/19_P2_RECONNECT_INCIDENT_2026-07-13.md`.
- ~~**[AI: Codex]** test-suite Telegram leak fix~~ **DONE 2026-07-13** in `960369b9`: autouse
  conftest fixture patches `resolve_telegram_credentials` at both import sites; focused tests
  `2 passed`, both full suites `122 passed`. Runtime code untouched. `C:\P2RT` was not synced, so
  its old conftest can still emit test messages until the next planned sync window.
- Known-benign noise: Hyperliquid testnet WS expires connections ~every 10-11 min
  (`opcode=8 'Expired'` in runtime log); `DISCONNECT -> RECONNECT attempt=1 -> DATA_RESTORED`
  chains in Telegram are normal. Optional notify-threshold change (only attempt>1 / STALE)
  deferred to the VPS restart window — P2 config frozen.
- Evidence committed on `feature/ibkr-bridge-final` at `59352bb3`:
  `IBKR_PAPER_BRIDGE/docs/19_P2_RECONNECT_INCIDENT_2026-07-13.md`.

## ✅ DONCHIAN CRYPTO LADDER DONE 2026-07-13 (Claude Fable 5) — NULL
GEN_DONCHIAN_BREAKOUT × {BTCUSD, ETHUSD} × {1h, 4h} through the full canonical ladder
(pre-approved 2026-07-13): **0/4 PASS, 0 robust_final — 3 REJECTED + 1 INSUFFICIENT_TRADES
(ETHUSD 4h, 9 trades). Nothing promotable, nothing forward-paper; bridge export NOT READY.**
The US-equities-10m Donchian lead does NOT transfer to crypto 1h/4h. Verdict report:
`11_TRIAGE/DONCHIAN_CRYPTO_LADDER_VERDICT_2026-07-13.md`; artifacts
`03_QUANTLENS/research/donchian_crypto_ladder_2026-07-13/`; registries updated (validator PASS).
- **[AI: Barış]** optional: if crypto Donchian is ever revisited, it needs a NEW pre-registered
  design (longer-history crypto source + multi-symbol family + Faz-3b swept exits) — re-running
  this grid is deterministic and yields identical nulls (A19).

## 🚀 CRYPTO PAPER BRIDGE — Hyperliquid (was "IBKR"; broker PIVOTED 2026-07-06, design FINAL on `feature/ibkr-bridge-final` 52b13f6f; read `IBKR_PAPER_BRIDGE/docs/` 00→01→05→02→07 before touching. IBKR closed (KKTC), Signum rejected (no native stop) — see 07_BROKER_DECISION)
- ~~run external design audits~~ DONE 2026-07-06: 7 reports in `IBKR_PAPER_BRIDGE/docs/audits/`.
- ~~triage audit reports, adopt accepted findings~~ **DONE 2026-07-06** (Claude Fable 5): 21 adopted clusters amended in place; record + rejections in `IBKR_PAPER_BRIDGE/docs/05_AUDIT_RESOLUTION.md`. Build plan now honestly **2 days** (Day 1 mock core, Day 2 IBKR hardening).
- **[AI: Barış]** review corrected `IBKR_PAPER_BRIDGE/docs/03_STATUS.md` and commits `d431dfab..0f6e241d`; decide whether to merge/continue `feature/ibkr-bridge-final`.
- ~~**[AI: Barış]** prep Hyperliquid **testnet** API wallet per `06_HYPERLIQUID_SETUP.md`.~~ DONE 2026-07-12: dedicated `MTC-bridge-test` agent authorized; Windows user credential formats validated without disclosure.
- ~~**[AI: Claude|Codex]** BUILD DAY: execute `IBKR_PAPER_BRIDGE/docs/02_BUILD_PLAN_1DAY.md` tasks 1-11 in order, commit per task, mock-first.~~ DONE 2026-07-07 (Codex GPT-5): 13 task commits through Task 11; tests pass; dry-run demo verified; P0 smoke written but not run.
- ~~**[AI: Codex]** corrective scaffold-to-P1 pass from `docs/09_CODEX_FIX_PROMPT.md`.~~ DONE 2026-07-07: Broker protocol decoupling, strategy stops/live positions, resting order lifecycle, persisted duplicate guard, persisted KILL, Hyperliquid native trigger fake-SDK tests, dashboard real rows/status/bars/screenshots, and lifecycle tests. Full suite 37 passed. Caveat: chart screenshot uses local SVG fallback; actual Lightweight Charts visible rendering remains a focused follow-up.
- **[AI: Codex|Claude]** focused dashboard chart follow-up: make the visible Trading chart use a reliable bundled/local Lightweight Charts path or formally accept the SVG fallback for P1 mock demo; verify with screenshots.
- ~~**[AI: Codex]** support Hyperliquid Unified account balances, preserve string-shaped exchange errors, and cleanly disconnect the smoke websocket.~~ DONE 2026-07-12 in `944a5323`; both full suites `70 passed`.
- **[AI: Barış]** do not transfer funds or change account mode; `unifiedAccount` correctly shares the 999 mock USDC balance across Spot/Perps.
- ~~**[AI: Codex]** add conservative Hyperliquid price rounding and run exactly one approved P0 attempt.~~ DONE 2026-07-12 in `42018032`; local suites `72 passed`, attempt failed cleanly on real `positionTpsl` response cardinality, zero open orders/positions.
- ~~**[AI: Codex]** locally harden `positionTpsl` response-shape handling, redacted diagnostics, and deterministic owned-cloid cleanup.~~ DONE 2026-07-12 in `09a7a92f`; both full suites `89 passed`.
- ~~**[AI: Codex]** implement E1 user-registry fallback and run one re-approved P0 smoke.~~ DONE 2026-07-12 in `25cee696`; source=`user_registry`, both suites `92 passed`, attempt 5 reached testnet and exposed the native trigger-type rejection.
- ~~**[AI: Codex]** implement G1 normalTpsl entry grouping and the bounded G2 fallback, then run attempt 6.~~ DONE 2026-07-12 in `a4de4a6e`; both suites `98 passed`, normalTpsl returned a resting entry plus `waitingForFill` child state, and C3 cleanup passed.
- **[AI: Any] 🔴 ACTIVE — GO-LIVE PLAN: `IBKR_PAPER_BRIDGE/docs/16_GO_LIVE_PLAN.md` is the single
  authoritative task ladder from here to P2 (testnet live loop).** Barış 2026-07-12 blanket-approved
  ALL of it incl. bounded P0 smokes until pass, B6 fill smoke, and ALL of Phase D (P2 ARM). Any model
  picks the first unchecked box in its §3 and executes per its §1 rules WITHOUT asking; human input
  only at its §0-İ points (Telegram creds, PC uptime, mainnet=forbidden; QuantLens registration İ4
  is now complete).
  P1 audited PASS; P0 attempt 6 proved the wire format (resting entry + `waitingForFill` child); W1
  (pending-child parser) is the current first task.
- ~~**[AI: Barış]** approve QuantLens İ4 registration and unblock the real golden.~~ **DONE
  2026-07-13**: `keltner_trail_ema8` is registered and the real golden is ready; 858/858 entry
  signals match. Evidence: `IBKR_PAPER_BRIDGE/docs/18_GOLDEN_REPORT.md`. Honest caveat: the
  bridge exit trail is SMA-8 while QuantLens `trail_ema8` is EMA-8, so exit parity is not claimed.
- **[AI: Claude|Codex]** P3 later (≥30d): produce the slippage + operational signal-parity report
  to `11_TRIAGE/`; the QuantLens/golden prerequisite is complete.

## 🔧 MCC APP AUDIT FOLLOW-UPS (audit 2026-07-05: `11_TRIAGE/MCC_APP_AUDIT_2026-07-05.md`; Barış answered all open questions; quick wins DONE same session on `feature/mcc-audit-fixes`)
- ~~fix backtest_reader nested-run glob + heartbeat_reader parents index~~ DONE 2026-07-05 (115 tests pass; July runs + heartbeat visible).
- ~~register faz3b_stage1 in RESEARCH_RUN_REGISTRY~~ DONE 2026-07-05.
- ~~refresh REPORT_MANIFEST + CURRENT_STATUS; retire SESSION_LOG~~ DONE 2026-07-05.
- ~~parity artifacts migrated to `12_PARITY_PINETS/`~~ DONE 2026-07-05 (byte-identical parity status; paths.local.json updated locally — git-ignored, other machines must update their own).
- ~~scoring pass `mcc_night_tail.sh` over July stage dirs~~ **DONE 2026-07-05** (Barış approved): 716 new scorecard_v2 cards (turtle_sweep 36, stageA_v2_multiasset 302, variants 182, archetypes 196), **promotable=0 across all 716** (consistent with known nulls). Dashboard verified: scorecards 837→1553, all 4 runs listed. Gotchas: `mcc_night_tail.sh` needs `MEGA_BUNDLE_MANIFEST` set (else CPCV = all N_A "No dataset found") + Windows-style `C:/` RUN_DIR + `PYTHONUTF8=1` (run_python_clean exec wrapper decodes as cp1254 otherwise). Tail's own "dashboard visible" check greps stage-name run_id → false NO now that reader names runs `<run>/<stage>` — cosmetic [AI: DeepSeek].
- ~~fix 39 VARIANT_LOG_REGISTRY.json validator errors~~ **DONE 2026-07-05**: added `research_run_id` to all 19 variants (derived from real `impl`+`created_utc`: archetypes→overnight_archetypes_2026-07-03, turtle→turtle_heavy_2026-07-01, missing-knobs→overnight_full_2026-07-02), registered those 3 runs in RESEARCH_RUN_REGISTRY, removed schema-invalid top-level `note` (content lives in overnight NEXT_STEPS sections). Validator now PASS.
- ~~build CURRENT_STATUS auto-derive tool~~ **DONE 2026-07-05**: `03_QUANTLENS/tools/derive_current_status.py` (dry-run default; `--apply` writes; `--check` exits 1 on drift). Derives phase from newest GLOBAL_HANDOFF `## ` topic + summary from its first paragraph + next_recommended_action from first open NEXT_STEPS bullet. Safety fields (mode=read_only, live_trading=false) hardcoded. Hand-refresh dies.
- ~~Home + tail visibility + header pills cleanup~~ **DONE 2026-07-05**: Home "Data as of" freshness line (already shipped); `mcc_night_tail.sh` dashboard-visible check now resolves MCC root by name-walk + matches `<run>/<stage>` run_id (was false NO); removed hardcoded "Local Engine: Idle"/"Token Mode" header pills → single "Read-only" pill.
- **[AI: Claude, optional]** Strategy Intelligence per-section "as of" chips (Home done; SI still could show evidence date per gate/verdict section).
- ~~System Test / Fake Money Lab page~~ **DONE 2026-07-05** (Barış approved design+impl): new read-only nav page `system_test_reader.py` + renderSystemTest; scans `03_QUANTLENS/system_test/*/`, shows plumbing counts only (888/888/888/≈444, 0 unexplained), sticky amber firewall banner, V1.1-V5 gate ladder. Renamed 'Paper Trading'->'Promotion Readiness' to kill the naming collision. Design: `11_TRIAGE/SYSTEM_TEST_LAB_PAGE_DESIGN_2026-07-05.md`. 120 API tests, live render verified.
- **[AI: Barış]** run-manifest discovery contract (audit §6.1) — decide if wanted before next big orchestrated sweep.


## FAZ 3B — SWEPT EXIT_MODE (D016 Path A scope freeze approved; passive accrual only)
## 🔶 FAZ 3B — SWEPT EXIT_MODE (Stage-2 prereg BLOCKED by Gate-5 FATAL 2026-07-13 — D016 decision now = path choice)
Scope: `00_AGENT_PROTOCOLS/FAZ3B_EXIT_SWEEP_SCOPE.md`. Chain D013→D014→D015 done: engine landed,
self-parity byte-identical (goldens never recaptured), Stage-1 discovery run COMPLETE 2026-07-05
(`03_QUANTLENS/research/faz3b_stage1_20260705/STAGE1_REPORT.md`): H1 confirmed at 1h — clean cell
GEN_KELTNER_BREAKOUT × AAPL × 1h × trail_ema8 STRONG_PASS union-DSR 0.581; H0 holds at 10m;
honest confound: first-ever 1h fixed_2R baseline itself robust on KELTNER SPY/QQQ. PR #15 merged.
- ~~Original Stage-2 draft + Gate-5~~ **CLOSED/BLOCKED 2026-07-13**: Codex FATAL findings
  `11_TRIAGE/CODEX_GATE5_FINDINGS_FAZ3B_STAGE2_2026-07-13.md` were independently confirmed by
  Fable; all six proposed held-out symbols were historically contaminated, the 12-grid was
  re-optimization, and existing gauntlet tools were exit-blind. The old draft can never run.
- ~~**[AI: Barış] choose Path A/B**~~ **DONE — D016 PATH A APPROVED 2026-07-13**. New temporal
  holdout frozen in `00_AGENT_PROTOCOLS/FAZ3B_STAGE2_FORWARD_CONFIRM_PREREG_2026-07-13.md`:
  scored 1h sessions 2026-07-14 through 2028-07-13; SPY/IWM, XLF/XLE, XLV/XLP across three
  diversity groups; primary `{50,10,2.0}` only plus four diagnostic star points. Earliest possible
  evaluation 2028-07-14. Today: zero compute and no data ingestion.
- **[AI: Codex, needs separate Barış approval]** build exit-aware CPCV/multi-window/PBO tooling
  exactly to the new prereg section 8 contract; default fixed-2R self-parity must stay byte-identical.
- **[AI: Any]** before any future-data unblinding, complete the artifact-level historical Keltner
  trial ledger. Registry-only checks are forbidden; scan result JSONs in both backtest-result roots.
- **[AI: Barış]** after the fixed window closes: separately approve non-performance data inventory,
  then Gate-5, then exactly one smoke/full evaluation. D016 itself authorizes none of these.
- ~~draft Stage-2 pre-reg~~ DONE 2026-07-13, then ~~Gate-5 adversarial review~~ **DONE 2026-07-13
  — VERDICT FATAL, Fable-verified on raw artifacts/code (findings `1859910c`, banner `f32a354c`,
  PR #18):** (1) all 6 "held-out" symbols already swept — June-29 overnight covered ALL 51 bundle
  symbols at Keltner 1h → NO untouched 1h symbol exists in the canonical bundle; registry proved
  NOT to be an evidence inventory; (2) CPCV/multiwindow tools are exit-blind (simulate_slice
  defaults fixed_2R) and PBO lacks a per-config matrix → §6 gauntlet unexecutable as written;
  (3) 12-set grid = 75% of discovery grid = re-optimization. Current draft can NEVER get D016.
- **[AI: Barış] 🔴 D016 DECISION = choose path:** **(a) RECOMMENDED — deferred forward
  confirmation:** freeze a pre-registered forward window now (bars after 2026-06-26, evaluate
  e.g. after 2026-12-31, pre-named symbols + ≥2 diversity groups); zero compute today, truly
  virgin data. **(b) close Faz3b as INCONCLUSIVE** (Stage-1 AAPL stays research-only, family
  gets no confirmation attempt). Either way requires NEW prereg + fresh Gate-5 before any run.
- **[AI: Codex, needs Barış approval — prerequisite for path (a) and any future exit-mode
  confirmation]** exit-aware gauntlet tooling task: `cpcv_validator.py` + `multiwindow_oos.py`
  must pass `row.exit_mode` into `simulate_slice` and stamp it in outputs; PBO needs a
  per-config×period return-matrix contract (Gate-5 findings §F/§G/§J + REQUIRED EDITS 9-11 are
  the spec). Own code review + self-parity discipline; separate approval.
- **[AI: Any]** register `overnight_multiasset_2026-06-29` in RESEARCH_RUN_REGISTRY; add the
  "virginity check = scan 05_BACKTEST_RESULTS + research JSONs, never registry-only" rule to
  prereg templates.
- **[AI: Barış]** 2026-08-01: Gate V5 day-30 review of the SYSTEM_TEST vertical-slice track (CLOSED at
  V1.1; legs V2-V4 deliberately unopened).

## SYSTEM_TEST_ONLY VERTICAL SLICE - Gate V0 planning approved 2026-07-02

Baris approved Gate V0 planning and selected `STG002 / QL_ALPHA_LINK_8EMA_1H`
as the benchmark. This is a fake-money systems-plumbing benchmark only:
SYSTEM_TEST_ONLY / NOT STRATEGY_APPROVED / NO REAL MONEY.

**Next:**
- ~~**[AI: Codex|Claude]** write a draft implementation plan only for the local
  core slice: signal emitter, localhost receiver, reconciliation reporter, and
  induced-failure drills. No code yet.~~ DONE 2026-07-02:
  `00_AGENT_PROTOCOLS/SYSTEM_TEST_VERTICAL_SLICE_IMPLEMENTATION_PLAN.md`.
- ~~**[AI: Codex|Claude]** prepare a narrow Fable audit prompt for that
  implementation plan before any code is approved.~~ DONE 2026-07-02:
  `11_TRIAGE/FABLE_AUDIT_PROMPT_SYSTEM_TEST_VERTICAL_SLICE_PLAN_2026-07-02.md`.
- ~~**[AI: Baris]** send the Fable audit prompt to Fable and bring back the
  report before implementation approval.~~ DONE 2026-07-02: Fable verdict was
  `SAFE ONLY AFTER PLAN FIXES`; Codex applied the plan-text fixes.
- ~~**[AI: Baris]** approve or reject the implementation plan.~~ DONE
  2026-07-02: Baris approved implementation with the exact SYSTEM_TEST_ONLY
  sentence. Codex implemented V1 local modules/tests only. No replay run,
  schema files, backtests, servers, broker/exchange/testnet, TradingView,
  WunderTrading, Pine, parity, `MTC_V2`, `02_MTC_BACKTEST`, or `07_ADAPTERS`
  work was performed.
- ~~**[AI: Baris|Codex]** before the first local replay run, resolve the output
  root guard.~~ DONE 2026-07-02: Baris approved the pre-run readiness patch.
  `.gitignore` now ignores `MTC_COMMAND_CENTER/03_QUANTLENS/system_test/`,
  `git check-ignore` confirms `_probe` is ignored, and
  `run_local_replay(...)` exists as a tested importable entry function. No real
  STG002 replay run was performed.
- ~~**[AI: Baris|Codex]** approve/run the separate Step 9.1 replay-run
  sentence.~~ DONE 2026-07-02: Baris approved exactly one local
  SYSTEM_TEST_ONLY replay. Codex ran it through `run_local_replay(...)` into
  `03_QUANTLENS/system_test/stg002_system_test_replay_20260702T171958Z/`.
  Result: `status=OK`, `EXPECTED=888`, `ENTRY=444`, `EXIT=444`,
  `RECEIVED accepted=888`, `duplicates=0`, `rejected=0`,
  `simulated_fills=888`, `round_trips=444`, `unexplained=0`.
- ~~**[AI: Baris|Codex]** review the completed local run artifacts and decide
  whether to send a narrow read-only Fable audit prompt for the result.~~ DONE
  2026-07-02/04: Fable audited run + implementation (PASS), drafted the V1.1
  LOW-fix dispatch; executor implemented (7-file allowlist); Fable audited the
  diff and committed. Focused pytest **43 passed**. **Slice V1.1 CLOSED** —
  clean pause point reached. Remaining slice work only via new gates:
  V2 (TV alerts) / V3 (Wunder demo) / V4 (testnet), each Baris-approval-gated
  and deliberately NOT opened (no robust strategy exists to justify them);
  Gate V5 day-30 review due **2026-08-01**.
- **[AI: Baris]** separate explicit approval is required before any server,
  CLI, dashboard execution UI, engine-forward signal generation, schema file,
  broker, exchange, testnet, TradingView, WunderTrading, Pine, parity,
  `MTC_V2`, paper trading, or live trading path.
- **[AI: Baris|Codex] Optional separate approval:** decide whether to add a
  SUPERSEDED banner to stale STG002 `PROMOTE_TO_*` / forward-paper docs. This
  is not part of the vertical slice implementation plan.

## 🔷 STRATEGY PARAM-SPEC REGISTRY — Faz 1-4 DONE 2026-07-01 (Claude Opus 4.8) → PR #15 open
Branch `feature/strategy-param-specs`, pushed, **PR [#15](https://github.com/bsemaay-tech/mtc-command-center/pull/15) open (NOT merged)**. Faz 1: declarative per-strategy param spec (generator code=truth + overlay → `05_REGISTRY/STRATEGY_PARAM_SPECS.json`, 20 strat, 1122 combos, 1,201,662 cases) surfaced in Strategy Detail §4. Faz 2: honest MTC_V2/Pine parity readiness (no 1:1 Pine impl for the 20 generics → `deferred_until_promotion` + `parity_contract` that a Pine port must replicate the global exec model; 2 review-Pine refs marked needs_reconciliation). Faz 3: first missing-knob variant `GEN_DONCHIAN_TURTLE` (Turtle structural stop) via monkey-patch `03_QUANTLENS/tools/variant_missing_knobs.py` (engine untouched), origin=variant/UNVALIDATED, in VARIANT_LOG, smoke OK. Faz 4: runbook §3.5 canonical case-count definition. API 112 passed, renders verified.
**Next:**
- **[AI: Barış]** review + merge PR #15.
- **[AI: Claude, approval-gated] Faz 3b:** TRUE trailing opposite-channel EXIT + short-side need an engine-core `simulate_slice` change (dynamic stop / direction) — affects ALL strategies → explicit approval before touching the shared simulator.
- ~~validate `GEN_DONCHIAN_TURTLE`~~ **DONE 2026-07-01** (turtle_heavy overnight): 357-cell full-universe + deep CPCV/PBO. **robust_final 0**; structural stop beat base in only 40% of cells (no systematic edge). Confirmed A21 (CPCV/PBO ≠ DSR) at 51×7 scale. Report: `05_BACKTEST_RESULTS/turtle_heavy_2026-07-01/MORNING_REPORT.md`; lessons `OVERNIGHT_LESSONS_2026-07-01.md`. **Do NOT pursue Faz 3b trailing-exit** — the structural-stop result does not motivate the engine-core change.
- **[AI: Claude] extend variants:** the remaining Faz-3 missing_knobs across the 20 strategies (promote fixed knobs like TRIPLE_EMA 5/13/50, BB mult, 8EMA period; add filters) — each a NEW variant in VARIANT_LOG, not a mutation of the base strategy.

## ✅ OVERNIGHT MULTI-ASSET SWEEP DONE 2026-06-30 (Claude Opus 4.8) — nothing promotable
Largest sweep to date: 7,140 cells (51 sym × 7 TF × 20 strat) on `native_multiasset_alpaca_2026-06-28`, 20 workers, one clean ~27-min pass. PASS 184 / STRONG_PASS 172 / BH-FDR 19 / **dsr_robust 2 (tiny-sample) / robust_final 0**. Report: `05_BACKTEST_RESULTS/overnight_multiasset_2026-06-29/MORNING_REPORT.md`. Dashboard shows run COMPLETED. **No existing strategy is robust on any asset class/TF — confirmed at scale.**
**Next [AI: Barış|Claude]:** the open path is **NEW strategy logic** (the crypto-era library does not transfer; re-sweeping is deterministic and yields identical nulls). If a lead is pursued (e.g. metals/DONCHIAN-intraday showed largest raw returns), require portfolio/CPCV + a pre-registered confirmation grid — expect the same null per prior pooled-DSR test. Results dir `overnight_multiasset_2026-06-29/` (17MB JSON + checkpoint) is local research output — not committed (git-ignored bulk); regenerable.

## ✅ ONBOARDING / AI_MEMORY HARDENING DONE 2026-06-29 (Claude Opus 4.8) — PR #5–#8 merged
2-round cold-onboarding audit (6 models). Closed all consensus gaps → onboarding now uniform across all 7 job types (backtest/scoring/dashboard/verdict/memory/git/tools). Fixes: repo-identity + DATA & LAUNCH (PR #5); W3 results→dashboard map + runner/DSR/pickup doc-sync (PR #6); W4 verdict authoring procedure `03_QUANTLENS/_user_guide/13_AI_VERDICT_AUTHORING_PROCEDURE.md` (PR #7); engine soft-guard for unset MEGA_BUNDLE_MANIFEST (PR #8). Audit prompts: `11_TRIAGE/COLD_ONBOARDING_AUDIT_PROMPT_{,v2_}2026-06-29.md` [AI: Any].
**Optional follow-ups [AI: Claude|Barış]:** (1) re-run the v2 audit as a regression to confirm W3/W4 now score PASS; (2) promote v2 prompt to a permanent `_AI_MEMORY/ONBOARDING_SELFTEST.md` run after every onboarding-contract change; (3) author real QuantLens verdicts using the new procedure (212 strategies currently un-verdicted/`NEEDS_CLARIFICATION`).

## ✅ IMPECCABLE UI PILOT (2026-06-21 → 2026-07-13) — COMPLETE on `feature/mcc-ui-impeccable-fixes`
Setup DONE: product context `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/MCC_PRODUCT_CONTEXT.md` + design context `MTC_COMMAND_CENTER/11_TRIAGE/STRATEGY_INTELLIGENCE_DESIGN_CONTEXT.md` (North Star "The Quiet Terminal"; preserves existing dark command-center identity) + `.claude/launch.json`. Original Strategy-Detail critique = **30/40 Good** (`.impeccable/critique/2026-06-21T15-56-19Z__r-08-dashboard-app-apps-web-app-js-strategy-detail.md`).
Polish pass **COMPLETE**; honest re-score = **32/40 Good** (not inflated to impeccable): `MTC_COMMAND_CENTER/11_TRIAGE/UI_AUDITS/IMPECCABLE_PILOT_R3/CRITIQUE_RESCORE_2026-07-13.md`. Frontend scope remained `08_DASHBOARD_APP/apps/web/{app.js,styles.css}`.
1. ~~[P1] a11y contrast~~ **DONE 2026-06-28 (DeepSeek v4 Pro + Codex + Claude audit)** — empty-state values now use `--muted #94a3b8` (~7.4:1 on all dark backgrounds, AA safe). Styled via `styles.css` only (10 selectors). Claude audit: PASS WITH NITS; no code fix required. Temporary reports removed after audit.
2. ~~[P1] a11y focus~~ **DONE 2026-06-28 (Codex GPT-5 + Claude audit PASS WITH NITS)** — global `:focus-visible` ring added, the 4 STAGE workflow cards are native `<button type="button">` controls, reduced-motion CSS disables the pulsing amber dot, and `tests/test_strategy_detail_a11y_static.py` guards the contract. Claude audit required no code fix.
3. ~~[P2] side-stripe bars~~ **DONE 2026-06-21 (Claude Opus 4.8, commit `0172d940`)** — `.gate-card .bar` was removed and replaced with full-border tint + faint background per state.
4. ~~[P2] boilerplate dedup~~ **DONE** — implementation `6da2735c`; before/after screenshot evidence committed in `adeb889b`. Full-credit notes are hidden; partial/zero notes remain.
5. ~~[P2] triple gate-state~~ **DONE** — implementation `e819ac02`; dead helper/CSS cleanup + before/after evidence committed in `93114a61`. Persistent right rail is canonical.
Verification: live `:8765/dashboard` Strategy Detail, committed screenshots under `11_TRIAGE/UI_AUDITS/IMPECCABLE_PILOT_R3/screenshots/`, `node --check` PASS, focused a11y test `2 passed`, canonical dashboard API suite `120 tests` / `OK`. No trading/Pine/MTC_V2/parity/schema/data-contract change.

## ▶ AI TOOL INTEGRATION ROADMAP (filed 2026-06-20, Claude Opus 4.8) — STATUS 2026-06-22: ALL PHASES 1–5 COMPLETE. Remaining = operator config only (n8n notify channel) + re-open DEFERs (LiteParse on scanned PDF, Claude-Video on indicator-screencast, Taste-Skill on a marketing page).
Source backlog + actionable plan + Claude critique live in `09_DOCS\AI_TOOLING\`:
- `MTC_AI_TOOLS_MASTER_INTEGRATION_BACKLOG.md` (catalog), `AI_TOOL_INTEGRATION_PLAN.md` (do this), `CLAUDE_REVIEW_OF_CODEX_BACKLOG.md` (what to drop).
Read `AI_TOOL_INTEGRATION_PLAN.md` before ANY AI-tool work. Phases (each Barış-approval-gated):
1. **Phase 1 — docs/instructions/memory** `[AI: Claude|Barış]` — DONE in part (this filing). PENDING APPROVAL: add a tool-roadmap + DeepSeek-routing pointer block to `AGENTS.md` and `_AI_MEMORY/START_HERE.md` (high-traffic contracts → don't edit without approval). Diffs first.
2. **Phase 2 — knowledge consolidation (light)** `[AI: Any]` — keep decisions in `09_DOCS\AI_TOOLING\`, research in `09_DOCS`, ops state in `_AI_MEMORY`. Do NOT build a new `00_KNOWLEDGE_BASE` tree.
3. **Phase 3 — local tools (pilot-gated, run §6 checklist FIRST)** `[AI: Claude|Barış]` — order: MarkItDown → LiteParse → CodeBurn → Graphify (Graphify downgraded to pilot). Compare MarkItDown/LiteParse to built-in pdf/docx/xlsx skills before adding a dependency.
   - DONE 2026-06-21: **MarkItDown** (0.1.6, `C:\tmp\mtc_markitdown_venv`, Py3.13) + **CodeBurn** (v0.9.12 global npm) piloted on real data → **both KEEP**. Reports `09_DOCS/AI_TOOLING/pilots/{markitdown,codeburn}_pilot.md`. CodeBurn finding: DeepSeek harness underused (Opus $563 + Codex $377 vs DeepSeek $2.44).
   - DONE 2026-06-21: **LiteParse piloted → ⏸️DEFER** (`liteparse` 2.0.0, ephemeral `C:\tmp\mtc_liteparse_venv`, Py3.13; 2.1.1 has no win/py3.13 wheel). Synthetic-PDF A/B ties MarkItDown on text PDFs; real edge (scanned-PDF OCR+spatial) untestable — 0 PDFs in repo — and needs Tesseract/LibreOffice/ImageMagick. Overlaps kept MarkItDown → not promoted. Report `09_DOCS/AI_TOOLING/pilots/liteparse_pilot.md`. Re-open when a real scanned strategy PDF lands. **→ Phase 3 now COMPLETE** (MarkItDown KEEP+promoted, CodeBurn KEEP, Graphify KEEP-on-demand, LiteParse DEFER).
   - DONE 2026-06-21: **Graphify piloted → KEEP on-demand** (`graphifyy` 0.8.44 via uv tool; local/keyless code graph; accurate `affected`/`explain`/`query`; graphs git-ignored; not auto, not whole-repo; `graphify install` skill-reg deferred). Report `09_DOCS/AI_TOOLING/pilots/graphify_pilot.md`.
   - DONE 2026-06-21 (Barış item 1): **MarkItDown promoted to permanent** — committed wrapper `03_QUANTLENS/tools/markitdown_ingest.py` (self-bootstraps git-ignored Py3.13 venv at `03_QUANTLENS/tools/.venvs/markitdown`, converts intake docs→.md; dry-run default). `.gitignore` updated; old `C:\tmp` venv removed; composes with (doesn't edit) `route_user_intake.py`. Still open: periodic `codeburn status` at session boundaries (CodeBurn stays global npm, no repo change).
4. **Phase 4 — research/UI pilots (branch-isolated)** `[AI: Claude|Barış]` — Claude-Video, Impeccable, Design-Extract, Taste-Skill on `feature/ui-*` only; no data-contract/registry/backtest change.
   - DONE: **Impeccable** (Strategy Detail polish, merged).
   - DONE 2026-06-22: **Design-Extract** (`designlang`) → KEEP on-demand inspiration only; wrapper `03_QUANTLENS/tools/design_extract.ps1`. `pilots/design-extract_pilot.md`.
   - DONE 2026-06-22: **Taste-Skill** (`leonxlnx/taste-skill`) → **DEFER/do-not-install**: its SKILL.md self-excludes dashboards/data-tables/product-UI (MTC's domain); Impeccable already owns that. Evaluated via `C:\tmp` clone, not installed. `pilots/taste-skill_pilot.md`. Reusable idea: its anti-default discipline + variance/motion/density dials as a checklist when running Impeccable.
   - DONE 2026-06-22: **Claude-Video** (`bradautomates/claude-video`) → **DEFER/do-not-install**. Piloted on a real Barış-supplied strategy video (TradingLab pullback, `youtu.be/Ju-cTa_dHAk`, 9m52s) via a reproduced pipeline (yt-dlp + already-installed ffmpeg + YouTube auto-captions + Claude vision; no repo install, all in `C:\tmp`). **A/B:** transcript-only already gave the full strategy; 24-frame sample added ~zero — the video is an animated explainer / pure price-action (no platform UI, no indicator settings to recover). Frame value is **content-gated**: only an indicator-config *screencast* beats transcript. Tool itself unnecessary (pipeline reproducible with installed tools). Report `pilots/claude-video_pilot.md`.
   - DONE 2026-06-22 (Claude Opus 4.8): the two doc-only branches are now MERGED to master (merge `5bcb66c9`) + deleted (local+remote): `feature/ui-design-extract` → `pilots/design-extract_pilot.md`; `feature/audit-second-eyes` (superset, contained design-extract) → `09_DOCS/AI_TOOLING/SECOND_EYES_AUDIT_2026-06-22.md`. Only `AI_TOOL_INTEGRATION_PLAN.md` + this file conflicted; resolved `--ours` (kept master's corrected §5/Phase4). Net delta = the 2 new docs only. Stale empty `feature/handoff-note` also removed; `C:\tmp` pilot leftovers (design_extract_out, second_eyes_*) cleaned.
   - **→ Phase 4 now COMPLETE** (Impeccable + Design-Extract = KEEP on-demand; Taste-Skill + Claude-Video = DEFER). Next AI-tool work = Phase 5 (n8n watchdog), which is BLOCKED until a stable backtest progress/log emitter exists.
5. **Phase 5 — side-service automation** `[AI: Barış|Claude]` — n8n watchdog for long backtests; needs a stable progress/log emitter first.
   - DONE 2026-06-22 (Claude Opus 4.8) — **stable emitter prerequisite SHIPPED** (branch `feature/run-progress-emitter`, TDD). Design: `09_DOCS/AI_TOOLING/RUN_PROGRESS_EMITTER_DESIGN_2026-06-22.md`. Canonical contract `mtc.run_progress/v1` + `mtc.run_status/v1` under `03_QUANTLENS/tools/overnight_runs/progress/<run_id>/` (heartbeat.json · events.jsonl · status.json · `_latest.json`; git-ignored). Parts: `progress_emitter.py` (lib+CLI, atomic writes, env-gated `MTC_RUN_EMITTER` → NullEmitter off so opted-out runs byte-identical), `run_emitter_supervisor.py` (liveness tick + guaranteed terminal status even on crash + `republish_native_status` adapter that reads the sweep runner's EXISTING `run_status.json` → **engine NOT edited, parity-safe**), and `heartbeat_reader.py` upgraded to strict v1 with two-timestamp **dead/stalled/running** derivation + legacy `_heartbeat*.json` fallback. Tests: tools 15 passed, API suite 86 passed (no regression); CLI smoke proved ok + crash paths.
   - DONE 2026-06-22 (Claude Opus 4.8) — **Phase 5 proper SHIPPED → Phase 5 COMPLETE.** `run_watchdog.py` (TDD): one-shot poll of `progress/_latest.json` → derives running/stalled/dead/done/failed (shared `derive_run_state` in `progress_emitter.py`), fires ONE notification per (run_id,state) alert transition (de-dupe via `_watchdog_state.json`), local log always + opt-in `--webhook-url` (no outward send without a URL). n8n workflow `03_QUANTLENS/tools/n8n/mtc_backtest_watchdog.workflow.json` + ops `09_DOCS/AI_TOOLING/PHASE5_WATCHDOG_OPS.md` (n8n or Windows Task Scheduler). AGENTS.md AI-TOOL-AUTO-USE gained a long-backtest→supervisor+watchdog trigger. Tools tests 22 passed; API suite 86 passed; CLI dedupe smoke verified. **Only operator action left:** wire the n8n Notify node to a real Telegram/Email/Slack channel + activate schedule.
REJECTED beyond Codex's list (see critique): **Headroom** (MITM proxy, ~5% saving), **NotebookLM-py** (unofficial API), **Webwright** (redundant with existing browser MCPs). Already-exists (don't rebuild): model routing = `_deepseek_driver`; review prompts = `04_SHARED\prompts\05_ai_workflow`. Hard rule: no install/integration without explicit Barış approval, tool by tool; no pine/MTC_V2/parity/schema/broker touch.

## ▶ DASHBOARD night-artifact contract LIVE 2026-06-15 (Claude Opus 4.8) — reader done, artifacts pending
Read-only `night_artifacts` reader + 5 schemas shipped; dashboard wired to consume run_plan/run_status/backtest_profile_result/top_results/artifact_index/leaderboard_delta/benchmark_update_candidate. **No such artifacts exist yet** → official profile buckets correctly empty, legacy scorecard rows quarantined.
Next when ready:
1. DONE 2026-06-15 (run_plan part + audit patch): `build_run_plan.py` generates draft review-only `run_plan.json`+`artifact_index.json`+`run_plan.md`; reader discovers usable; Planner/Advanced Artifacts/SI §4/Result Explorer artifact panel populated. Audit follow-up applied: no silent BTCUSDT default (universe `needs_freeze` when unresolved), schema enforces read-only/no-execution safety fields, SI §4 wired to run plan. STILL NEEDED: real `backtest_profile_result.json` + `top_results.json` for a validated strategy/profile to populate official buckets + KPIs (writer outside read-only app). No fakes. Also: freeze the US_EQUITIES symbol universe (`--symbols`) before any approval.
2. Implement interactive Result Explorer filters (currently placeholder; enable when profile rows real).
3. Snapshot warm-up prefetch at server start to kill ~12s cold load.
4. No promotion / no KPI fabrication; absent metrics stay `—`.
5. DONE 2026-06-15: Home metric aggregation fix — strategy-level counts deduped by base id (no count > Total), Evidence/System row counts split out + labelled; SI Gate1 section shows best Gate 1 passing version + All Versions. Report: `11_TRIAGE/HOME_METRIC_AGGREGATION_PATCH_REPORT_2026-06-15.md`.
6. DONE 2026-06-15 (RESOLVED open decision): Home canonical universe — `Total Strategies` = pipeline rows (registry fallback), Total back to **176**; scorecard-only ids shown as "Scorecard-only Strategy IDs" orphan metric (36). Gate metrics canonical-only. Report: `11_TRIAGE/HOME_CANONICAL_UNIVERSE_PATCH_REPORT_2026-06-15.md`.
7. DONE 2026-06-15: Hardening — invariant test `tests/test_home_metric_invariants.py` (no strategy count > Total; orphan exclusion; registry fallback); "Needs Attention"→"Needs Review" rename + tooltip (broad heuristic, not strict blockers); audit prompt `11_TRIAGE/NEXT_CODEX_AUDIT_PROMPT_HOME_CANONICAL_UNIVERSE_2026-06-15.md`. PENDING USER: run that Codex audit. FUTURE: orphan-id drill-down + promotion path; real action-queue/blocker model to make Needs Review precise; jsdom JS test harness to retire Python mirror.
8. DONE 2026-06-16: First profile-separated result artifact pilot (Option A). Read-only converter `03_QUANTLENS/tools/build_profile_result_artifact.py` turned real soak `MEGA_results_iter_1_*` into schema-valid `backtest_profile_result.json` (pilot dir, 4 SOURCE_NAKED rows, RESEARCH_ONLY, universe_mismatch recorded). Reader shows profile_result_rows=4. Report: `11_TRIAGE/FIRST_PROFILE_RESULT_ARTIFACT_PILOT_REPORT_2026-06-15.md`.
9. DONE 2026-06-16: Research-only UI hardening — badges (RESEARCH ONLY/UNIVERSE MISMATCH/NON-ROBUST/PROFILE MAPPING INTERPRETED) across Result Explorer/SI §5/Leaderboard/Advanced Artifacts; reader forwards provenance+profile_mapping. Report: `11_TRIAGE/PROFILE_RESULT_RESEARCH_ONLY_UI_HARDENING_REPORT_2026-06-15.md`. Resolves item (a) above.
10. DONE 2026-06-16: OPS BLOCKER resolved — `run_dashboard_server.ps1` now single-instance. Root cause (from server log): supervisor restarted `pythonw serve` every 5s; when port 8765 already bound each new process failed bind + exited same-second (endless churn), and multiple unguarded launcher copies raced → pile-up. Fix: launcher checks port 8765 + `/healthz mode=read_only` and logs `skip launch` (exit 0) if already running; supervised loop re-checks port each iteration and exits instead of churning; flags `-StatusOnly`/`-ForceRestart`/`-KillStaleMccOnly`; strict kill filter (python/pythonw + cmdline mcc_readonly + serve only — never unrelated python; default mode kills nothing); bounded `dashboard_launcher.log` + 256KB truncation on `dashboard_server.log`. Verified: 2 launches → both skip, proc count stays **1**; `POST`→405; `/healthz`+`/api/snapshot?refresh=1`=200; **69 API tests OK**; `node --check` PASS. NOTE: no auto-start trigger exists (launcher comment names a non-existent task; no Run key/Startup/VBS). If logon auto-start wanted, register ONE guarded scheduled task calling the launcher (self-skips) — left as manual user action. Report: `11_TRIAGE/DASHBOARD_LAUNCHER_SINGLE_INSTANCE_PATCH_REPORT_2026-06-15.md`.
11. BLOCKED 2026-06-28: (b) native US-equities-10m soak cannot be generated from current repo data. DeepSeek audit + Codex verification found no US equities provider, no US equities 10m OHLCV on disk, no frozen symbol universe, and only crypto proxy/research-only result evidence. Status: **DATA PROVIDER / SYMBOL UNIVERSE REQUIRED**. Codex assessment: `11_TRIAGE/NATIVE_US_EQUITIES_10M_CODEX_ASSESSMENT_2026-06-28.md`; worker report: `11_TRIAGE/_tmp_native_us_equities_10m_audit_2026-06-28/WORKER_REPORT.md`. UPDATE 2026-06-28: Baris exported TradingView `BATS:SPY` 10m Chart Data CSV chunks into `00_INBOX/USER_INTAKE/`; next worker should run the prepared handoff `11_TRIAGE/CLAUDE_PROMPT_FINISH_TRADINGVIEW_SPY_10M_NATIVE_SMOKE_2026-06-28.md` to consolidate/validate data, build a SPY 10m bundle if valid, and run only a `SMOKE ONLY / NOT PROMOTABLE` one-symbol smoke if safe. **DONE 2026-06-28 (Claude Opus 4.8) — SMOKE SHIPPED, infra blocker partially lifted for SPY.** Consolidated SPY export validated PASS (20,094 clean RTH-only 10m bars, 0 dups/gaps/OHLC-violations, no volume, adjustment unknown) → `11_TRIAGE/TRADINGVIEW_SPY_10M_DATA_VALIDATION_2026-06-28.md`. Built native bundle `03_QUANTLENS/data/native_us_equities_10m_spy_tradingview_2026-06-28/` (`normalized/BATS_SPY_10m.csv` + `manifests/dataset_manifest.json`). Ran the smallest cell (1 strat × SPY × 10m, 75 trials, `MEGA_OUTPUT_DIR` redirected so nothing touched `05_BACKTEST_RESULTS`): exit 0, **real** result = `INSUFFICIENT_TRADES` (17 lockbox trades, net −0.773% vs B&H +8.90%, robust_final=false). `SMOKE ONLY / NOT PROMOTABLE`. Report `11_TRIAGE/SPY_10M_NATIVE_SMOKE_REPORT_2026-06-28.md`. NO `backtest_profile_result.json` / `top_results.json` generated (one-row insufficient-trades smoke). **UPDATE 2026-06-28 (Barış approved multi-symbol):** QQQ+AAPL validated PASS (identical clean structure); 3-symbol bundle `03_QUANTLENS/data/native_us_equities_10m_us3_tradingview_2026-06-28/` + 3-cell smoke (exit 0, output redirected): SPY/QQQ=INSUFFICIENT_TRADES, AAPL=FAIL, all net-negative & below buy&hold, all robust_final=false → still SMOKE ONLY / NOT PROMOTABLE, no artifacts. All 10m chart data is in `00_INBOX/USER_INTAKE/` (SPY/QQQ/AAPL only). **PARAM SWEEP DONE 2026-06-28 (Barış approved) → 8EMA SHELVED on US equities.** All 75 grid configs × SPY/QQQ/AAPL, full + lockbox OOS: 0/75 positive SPY, 0/75 QQQ, 1/75 AAPL (breakeven noise, 16 OOS trades). Zero beat buy&hold. Report `11_TRIAGE/SPY_QQQ_AAPL_10M_8EMA_PARAM_SWEEP_2026-06-28.md`. Pipeline proven on native US-equities 10m; **strategy is the blocker, not infra.** No full soak, no engine gating, no artifacts. **MULTI-STRATEGY SWEEP DONE 2026-06-28 (Barış "do all options"):** all 15 distinct engine strategies × SPY/QQQ/AAPL on native bundle. Exploratory best-of-grid flagged DONCHIAN/VWAP/GOLDEN_CROSS; honest engine walk-forward+DSR on top 3 × 3 symbols (9 cells) = only 1 PASS (DONCHIAN/AAPL +2.18% OOS, not DSR-robust p=0.215), 0 robust_final. Stage-A survivors = multiple-testing noise. **No promotable strategy on SPY/QQQ/AAPL 10m — crypto-era library does not transfer.** Report `11_TRIAGE/US_EQUITIES_10M_MULTI_STRATEGY_SWEEP_2026-06-28.md`. **Infra blocker FULLY CLOSED** (pipeline proven end-to-end on native US-equities 10m). Created discoverable data inventory `03_QUANTLENS/data/README.md` (native bundles + crypto locations + `MEGA_BUNDLE_MANIFEST` reuse contract). **Next human decision:** pursue NEW strategy logic and/or more symbols+longer history; adjustment policy + equity-session gating moot until a real edge exists. **UPGRADE 2026-06-28 (Alpaca):** Barış gave Alpaca paper key → wrote `03_QUANTLENS/tools/alpaca_download_us_equities_10m.py`, pulled 7 symbols (SPY/QQQ/AAPL/MSFT/NVDA/AMZN/TSLA) ~57.7k bars each (~6yr, adjusted, with volume) → bundle `native_us_equities_10m_alpaca_2026-06-28`. Full engine sweep (140 cells): **15 PASS (was 1), still 0 DSR-robust.** **GEN_DONCHIAN_BREAKOUT = lead: +OOS on 5/7 symbols, beats buy&hold on AAPL+TSLA.** Report `11_TRIAGE/US_EQUITIES_10M_ALPACA_6YR_SWEEP_2026-06-28.md`. Still NOT PROMOTABLE (no cell DSR-robust; best DSR confidence 0.46, need ≥0.95 — DSR is higher=better, earlier "≤0.05" wording was backwards, corrected). **DONCHIAN cross-sectional DSR DONE → LEAD CLOSED:** one shared config on all 7 symbols, 488 pooled OOS trades, mean R +0.03, PF 1.06, bootstrap p=0.27, DSR conf 0.22 → not significant, not robust; "5/7 positive" was per-symbol cherry-picking (only QQQ/AAPL positive under shared config). Report `11_TRIAGE/DONCHIAN_CROSS_SECTIONAL_DSR_2026-06-28.md`. **No existing strategy has a robust edge on native US-equities 10m even with 6yr×7sym.** Infra fully done + reusable; productive path = NEW strategy logic. 24MB CSVs + run outputs git-ignored; manifest/script/reports committed. **COMPLETE DATASET BUILT 2026-06-29 (Barış request, ran overnight):** `tools/alpaca_download_dataset.py` → bundle `native_multiasset_alpaca_2026-06-28`: **51 symbols × 7 TF (10m..1d) = 357 datasets, 357/357 PASS, ~11.86M bars, 711MB.** Indices+stocks+commodity/bond/sector ETF proxies+VXX+intl+12 crypto. Adjusted, with volume. NO forex/futures (Alpaca limit — deferred to other providers). 711MB CSVs git-ignored; manifest+script+README committed. **This is now the PRIMARY research substrate.** Next: test NEW strategy logic across asset classes/TFs on it (no existing strategy is DSR-robust). Still open after data decision: (c) top_results.json only once a real same-bucket multi-row set exists; (d) keep converter as only sanctioned path. DONE 2026-06-28: (e) converter/read-model now expose `provenance.universe_mismatch` as a strict boolean and carry text in `universe_mismatch_reason`, with legacy string artifacts normalized at read time.
12. DONE 2026-06-16: Launcher single-instance follow-up (audit nits). `-StatusOnly` now truly non-mutating (moved before `Limit-LogSize`, prints via `Write-Output` not the launcher log) — verified log size/mtime unchanged across 2 runs. Startup auto-start CORRECTED: one per-user Startup VBS `MTC_Command_Center_Dashboard.vbs` exists and points to the guarded `run_dashboard_server.ps1` (prior "no auto-start found" was stale); no duplicate VBS; nothing created/deleted. Re-verified: 2 launches skip, count=1, `POST`→405, `/healthz`+snapshot=200, 69 tests OK, PARSE_OK. Report: `11_TRIAGE/DASHBOARD_LAUNCHER_SINGLE_INSTANCE_FOLLOWUP_REPORT_2026-06-15.md`.
13. AUDITED 2026-06-16 (impl pending): `/api/snapshot` perf. Measured **115.56 MB** (121,172,209 B), warm fetch 10.2s / cold ~60s. Root cause = scorecard data embedded 3-4×. Biggest: `scorecards.by_strategy` 31.6MB (**UI never reads it**), `scorecards.cards` 30MB (used; gates1/1B/2/3 sub_scores ~26MB), `candidate_audit` 8.4MB (**UI-unused**, CLI/tests only), `candidate_pipeline.rows[].scorecard_v2_cases` 7.1MB (**UI uses count only**, app.js:400 already accepts a number). Full analysis + UI dependency map: `11_TRIAGE/SNAPSHOT_PAYLOAD_PERFORMANCE_AUDIT_2026-06-16.md`.
   - DONE 2026-06-16 (L1+L2+L3): snapshot slimmed **115.56MB → 44.64MB (−61%)**. `read_model._slim_http_snapshot()` drops `scorecards.by_strategy`, omits top-level `candidate_audit` (reader/CLI/tests intact), collapses `candidate_pipeline.rows[].scorecard_v2_cases` arrays → int count. Zero frontend change. 69 API tests OK; `node --check` OK; `/healthz`=200 read_only; `POST`→405. Report: `11_TRIAGE/SNAPSHOT_PAYLOAD_SLIM_LOW_RISK_PATCH_REPORT_2026-06-16.md`.
   - DONE 2026-06-16 (M1): snapshot **44.64MB → 4.45MB** (−90%; vs original 115.56MB = −96%). `read_model._slim_http_snapshot` strips per-card gate `sub_scores` + collapses `notes`→count/preview (all 837 cards) and strips pipeline `scorecard_v2` gate sub_scores; scores+statuses+gate_summary kept inline. Full cards retained in `_FULL_SCORECARDS_CACHE`; new read-only `GET /api/scorecard-detail?strategy_id=` (server.py, param-validated, no path read, 400/404/200, POST→405) + `build_scorecard_detail`. app.js: `state.detailCards`, `loadStrategyDetail`/`detailBestCard`, fetch-on-open in renderIntelligence, subscoreList loading/summary-only states, advancedSection uses loaded detail. 69 API tests OK; `node --check` OK; `/healthz`=200; `POST` both endpoints 405; detail GEN_ATR_PULLBACK_TREND→11 cards/565KB/has_sub. Report: `11_TRIAGE/SNAPSHOT_GATE_DETAIL_LAZY_LOAD_PATCH_REPORT_2026-06-16.md`.
   - ▶ OPTIONAL (polish, not bloat): gzip JSON responses (transport-only); cache detail-by-id across views. Snapshot size goal achieved.
Report: `11_TRIAGE/BACKTEST_ARTIFACT_READER_INTEGRATION_REPORT_2026-06-15.md`.

## ARCHIVED / HISTORICAL - night_3M_2026-06-08 run notes (launched 2026-06-08 23:29)

Launched by DeepSeek v4 Pro. 59 strategies, 20 workers, ~210K evals/iter, target 15+ iters = 3M+ cases. Post-loop validation auto-runs after 8h deadline (~07:29).

### Morning tasks [AI: Any|DeepSeek]:
1. **Verify completion:** read heartbeat + log
   - `cat tools/overnight_runs/night_3M_2026-06-08.log`
   - `cat tools/overnight_runs/_heartbeat_night_3M_2026-06-08.json`
   - Check for `=== ALL DONE ===` marker
2. **Read morning report:** `05_BACKTEST_RESULTS/night_3M_2026-06-08/MORNING_REPORT.md`
3. **MCC visibility:** Run `mcc_night_tail.sh` on the best iter if scorecards need enrichment (D009: use `run_python_clean.py`). Verify `/api/snapshot?refresh=1` shows new run.
4. **Write lessons:** `11_TRIAGE/lessons_archive/OVERNIGHT_LESSONS_2026-06-08.md`
5. **No promotion:** All results are research-only per deterministic soak nature (A19). Gates must prove edge independently.

## ▶ CODEX PICKUP 2026-06-08 — 5 open items (full detail: `_AI_MEMORY/CODEX_PICKUP_2026-06-08.md`)

1. **Night-runs → MCC** `[AI: Codex]` — DONE 2026-06-08 by Codex GPT-5. `full_sweep_2026-06-07` (122), `batch023_034_2026-06-07` (111), and final validation iter `night_1m_2026-06-07/iter_05` (122) are enriched into `scorecard_v2`. MCC scorecard reader now scans nested scorecard runs and sees 715 total cards / 46 distinct strategies. No promotion: all three 2026-06-07 batches have 0 promotable cards.
2. **UI Round-2 remainder** `[AI: Codex]` — DONE 2026-06-08 by Codex GPT-5 except Barış screenshot re-check. R2-04/05 fixed as a compact verdict/badge ladder tooltip. R2-13-deep fixed: every scorecard sub-score now carries `max_points` and a short `deduction_reason`, and the gate detail table shows the reason. R2-31 fixed: Strategy Detail now surfaces the selected scorecard file timestamp, falling back to snapshot timestamp only when no scorecard is linked. R2-36 closed as a no-code audit: Gate2 tooltip references real emitted `metrics.wfo_pass`, not a ghost requirement. Plan: `_AI_MEMORY/UI Reviev/ROUND2_PLAN.md`.
3. **QuantLens = Claude/Codex verdict** `[AI: Codex|Barış]` — DONE 2026-06-08 by Codex GPT-5 as opinion-only metadata. Added `05_REGISTRY/AI_QUANTLENS_VERDICT_REGISTRY.json`, read-only `expert_quantlens` snapshot key, row/scorecard attachment, and a Strategy Detail `QuantLens Expert Verdict` section. Current verdicts: 141 NEEDS_CLARIFICATION, 46 RESEARCH_ONLY, 25 SALVAGE, 0 PASS. Scorecard remains the only scoring authority.
4. **AI strategy naming** `[AI: Codex|Barış]` — DONE 2026-06-08 by Codex GPT-5 as display-only metadata. Added `05_REGISTRY/AI_STRATEGY_NAME_REGISTRY.json` and read-only API attachment; current snapshot applies names to 176/176 pipeline rows and 715/715 scorecards. Barış can still rename individual entries later if desired.
5. **Backlog** — UI-30 producer_spec field-fill (needs approval), Gate3 builder (no scorer; binding decisions in memory mcc-gate3-promotion-decisions), W1 parity-in-night-flow. W2 auto-backtest-selector closed 2026-06-08 by Codex GPT-5: `03_QUANTLENS/tools/build_needs_backtest_selector.py` writes `NEEDS_BACKTEST_SELECTOR.{json,md}`; current output has 89 objective candidates. Dead `renderDecisionPanel()` cleanup closed 2026-06-08 by Codex GPT-5. Stray hung python PID cleanup checked 2026-06-08 by Codex GPT-5: PIDs 18480/57724/21200 were already absent, no kill needed.

## Dashboard UI architecture (2026-06-07)

### UI-36-CANONICAL-ROW | DONE 2026-06-07 (Codex GPT-5) | API canonical display row [AI: Codex]
- `scorecard_reader.py` now attaches `canonical` to every scorecard-merged row.
- `read_model.py` now scorecard-merges `candidate_pipeline.rows` as well as audit rows.
- Summary/schema written to `_AI_MEMORY/UI Reviev/RESULT_UI36_codex.md`.
- Validation: py_compile PASS; API unittest discovery 35 passed; live snapshot smoke PASS.
- Follow-up [AI: Claude|Codex]: migrate frontend panels to read `row.canonical` instead of raw stage/legacy fields.

## Strategy coding sprint (2026-06-07 — autonomous)

### N5-AUDIT | DONE 2026-06-07 (Claude) | 63-strateji kodlanabilirlik audit
- Kayıt: `_AI_MEMORY/N5_CODABILITY_AUDIT.md`
- 34 ALREADY_IN_ENGINE · 16 CODEABLE · 9 PRE_REG_NEEDED · 4 DISCRETIONARY · 6 PARKED_NO_DATA
- STG061+STG063: N5 agent CODEABLE dedi ama kendi spec'leri "thresholds unknown" → PRE_REG_NEEDED düzeltildi

### A1-PRODUCER-SPEC | DONE 2026-06-07 (Claude) | 41 producer_spec.json üretildi
- Script: `03_QUANTLENS/tools/generate_producer_specs.py`
- 63/63 strateji artık producer_spec.json'a sahip (41 yeni, 22 mevcut)
- 41 gerçek MEGA metrik; 22 dürüst placeholder (hiç uydurulmuş sayı yok)

### FULL-59-SWEEP | DONE 2026-06-07 (Claude + DeepSeek) | full_sweep_2026-06-07.sh dispatch [AI: Claude]
- Script: `03_QUANTLENS/tools/full_sweep_2026-06-07.sh`.
- 59 strategies via strat_batch_remaining.py chain, 18 workers.
- Result: 5015 cells, 122 evaluation artifacts, report written to `03_QUANTLENS/05_BACKTEST_RESULTS/full_sweep_2026-06-07/REPORT_full-2026-06-07.md`.
- Alpha summary: passes=122, beat_buyhold=55, premium=0, down_market_alpha=0.
- D009 shim confirmed working; scipy.stats intercepted, no BLAS hang.

### NIGHT-1M-QUIET-2026-06-07 | ARCHIVED / HISTORICAL 2026-06-07 (Codex GPT-5) | 1M quiet overnight sweep [AI: Codex|Any]
- User requested no questions, max 10 workers, quiet machine, about 1,000,000 cases after UI-audit work.
- Launcher: `03_QUANTLENS/tools/night_1m_2026-06-07.sh`; keep-awake wrapper: `03_QUANTLENS/tools/start_night_1m_2026-06-07_keepawake.ps1`.
- Output root: `03_QUANTLENS/05_BACKTEST_RESULTS/night_1m_2026-06-07/`.
- Live heartbeat: `03_QUANTLENS/tools/overnight_runs/_heartbeat_night_1m_2026-06-07.json` and dashboard-facing `_heartbeat.json`.
- Plan: 5 full MEGA passes at 10 workers, about 215,645 estimated configs/pass, target about 1,078,225, then validation tail on final successful pass.
- Morning action [AI: Any]: verify heartbeat/logs, read `SUMMARY_night_1m_2026-06-07.md`, validate artifacts from the final successful iter, and keep the conclusion research-only unless gates prove otherwise. Repeated passes are deterministic soak/current-code evidence, not independent statistical proof.

### STG028-034-046-053-CODING | DONE 2026-06-07 (DeepSeek v4 Pro recovery) | 5 strategies swept + validated
- File: `03_QUANTLENS/tools/strat_batch_remaining.py`
- QL_CANSLIM_SHAKEOUT_v1 (STG028) · QL_ANTI_CHASE_CRABEL_v1 (STG033)
  QL_EMA_RETEST_v1 (STG034) · QL_VWAP_TREND_CONT_v1 (STG046) · QL_HARRIS_50DMA_v1 (STG053)
- Recovery sweep: 425 jobs, 4 workers, 109.3s → 11 PASS candidates
- Gate2: 4 OK/PASS, 7 FAIL. Promotable: 0/11 (Gate3 INCOMPLETE).
- D009 fixed (scipy shim). STG061/063 remain PRE_REG_NEEDED.
- Run: `remaining_2026-06-07-recovery/`

### PRE_REG_NEEDED — Barış threshold tanımlamalı (9 strateji):
| STG | İhtiyaç |
|---|---|
| STG007 | Stage2 EMA/MA eşiği |
| STG021 | VCP kontraksiyon % eşiği |
| STG027 | RSI diverjans + CHoCH bölge genişliği |
| STG037 | 7-mum pattern geometri |
| STG054 | Fishhook derinlik/hız eşiği |
| STG058 | Parabolic SAR çarpan + "champion" filtresi |
| STG061 | Pierpont extension eşiği + danger-zone sınırı |
| STG062 | Weinstein Stage2 MA eğim + hacim eşiği |
| STG063 | Tito RS eşiği + crossback trigger |

## Overnight spec sprint (2026-06-06 — autonomous)

### SPEC-SPRINT-ALL-35 | DONE 2026-06-06 (Claude, autonomous) | 35 deterministic spec files [AI: Claude]
- Barış approved: "Tüm 35 strateji için spec yaz / Gate3: başla / ben uyuyorum sen başla"
- Written: 35 × `07_deterministic_spec.md` for STG001-022 (method reconstruction), STG023-034 (translated from run_batch.py Python functions), STG046 (parsed from Pine review script)
- All existing specs (STG035-045, STG047-063) already present → **63/63 strategies now have spec files**
- Committed as `915611f` (62 files, 2333 insertions)
- Registry regenerated: review_needed 1447 → 1251 (−196 placeholders)
- Known limit: STG001-034 and STG046 have no `01_candidate_metadata.yaml` → `known_strengths`/`known_weaknesses` registry fields remain review_needed until those files are created

### GATE3-LIFECYCLE-INVEST | DONE 2026-06-06 (Claude, autonomous) | Gate3 lifecycle test investigation [AI: Claude]
- Investigated "5 failing lifecycle tests" from prior context
- Result: **286 tests pass, 0 failures** across all test suites (35 + 251)
- The prior "lifecycle failures" were scorecard-level blockers, NOT pytest failures
- MEV-004 still open: `pending_queue`, EOD/EOW time-stop, consecutive-loss reset, max-pyramid guard = real test failures in the MTC engine lifecycle test suite (not the pytest suite)
- Gate3 score: 97.0/100 INCOMPLETE for `QL_FAM_MOMENTUM_CONTINUATION|TRXUSDT|4h`
- No code changes made; no tests broken

### PINE-BACKTEST-CHECK | DONE 2026-06-06 (Claude, autonomous) | Pine code availability check [AI: Claude]
- Checked all Pine files in pinets/ — 3 found, none are strategies ready for overnight backtest without additional setup
- No new backtests started (insufficient setup for autonomous execution)

## S6 worker monitor UI (2026-06-06)

### S6-D3B-WORKER-MONITOR | DONE 2026-06-06 (Codex GPT-5) | Overnight runner heartbeat widget [AI: Codex]
- Added embedded Worker Monitor card to Backtest Summary, using `snapshot.overnight_heartbeat`; no new top-level tab.
- Current source snapshot renders offline state with reason `overnight_runs dir not found`.
- Files changed: `08_DASHBOARD_APP/apps/web/app.js`, `08_DASHBOARD_APP/apps/web/index.html`, `08_DASHBOARD_APP/apps/web/styles.css`, `_AI_MEMORY/PARALLEL_AGENT_REPORTS/S6_D3B_WORKER_MONITOR_REPORT.md`.
- Validation: D3a prerequisite PASS; `node --check app.js` PASS; clean dashboard server health PASS; browser verification PASS on `http://127.0.0.1:8766/dashboard`; API pytest blocked by missing `pytest`; DeepSeek review blocked by missing `openai`.

## S5 dashboard acceptance panel (2026-06-06)

### S5-CODEX-A8 | DONE 2026-06-06 (Codex GPT-5) | Global acceptance criterion panel [AI: Codex]
- Added global `MCC System Status` panel at the top of the main dashboard content, visible on the default Pipeline screen without opening a strategy.
- Panel derives from `snapshot.scorecards.cards`: best candidate, blocked count/reason, scorecard totals, Gate2 PASS, Gate3 OK, and next action.
- Live values verified: 349 scorecards, 1 promotable, 125 Gate2 PASS, 1 Gate3 OK, 348 blocked; best `QL_FAM_MOMENTUM_CONTINUATION|TRXUSDT|4h`.
- Validation: `node --check app.js` PASS; dashboard health PASS; browser verification PASS; API pytest blocked by missing `pytest`; DeepSeek review blocked by missing `openai`.

## S2 dashboard UI components (2026-06-06)

### S2-CODEX-UI | DONE 2026-06-06 (Codex GPT-5) | A5/A6/A7/D4 dashboard components [AI: Codex]
- Implemented detail-page Gate2 Backtest Evidence renderer from `scorecard_v2.gate2.metrics`, Not Promotable blockers panel, Pipeline gate-status filters, and Backtest run detail panel.
- Files changed: `08_DASHBOARD_APP/apps/web/app.js`, `08_DASHBOARD_APP/apps/web/index.html`, `08_DASHBOARD_APP/apps/web/styles.css`, `_AI_MEMORY/PARALLEL_AGENT_REPORTS/S2_CODEX_UI_REPORT.md`.
- Validation: `node --check app.js` PASS; dashboard health PASS; browser verification PASS for A6, A7, D4, and A5 no-data state. API pytest blocked by missing `pytest`; DeepSeek adversarial review blocked by missing `openai`.
- Caveat: current live snapshot scorecards have empty `gate2.metrics`, so positive metric-card rendering remains data-dependent. No metrics were fabricated.

> **MASTER PLAN (2026-06-06):** MCC mimarisini tamamen bitirme + tüm stratejileri ilerletme iş planı → [[MCC_COMPLETION_MASTER_PLAN]] (`_AI_MEMORY/MCC_COMPLETION_MASTER_PLAN.md`). Workstream A (UI), B (pipeline), C (Gate3 — asıl blocker, builder yok), D (gece-veri→UI), E (promosyon hattı). Barış kararı bekleyen: C0 (production tanımı), B3 (confirmation grid), C2/C3 (entegrasyon onayı).

## Codex continuation closure (2026-06-06)

### C3-DRY-RUN-GATE3 | DONE 2026-06-06 (Codex GPT-5) | Dry-run adapter evidence, no live path [AI: Codex]
- Added `07_ADAPTERS/liveops/dry_run_adapter.py`, tests, and README. Generated C3 evidence for the 9 `fam_templates_2026-06-06` all-gate artifacts under `03_STATUS/dry_run_evidence_2026-06-06/`.
- `LIVEOPS_STATUS.json` now records dry-run mode only: live trading false, webhook sending false, broker integration false, 9 simulated-signal events, 0 live orders, 0 webhook sends.
- Gate3 moved from 46.0 to 91.0 for the family-template readiness artifacts, but remains **INCOMPLETE** and `promotable=0` because MTC risk-engine compatibility and backtest-to-live matching are still unproven.
- Validation: py_compile PASS, dry-run tests 4 PASS, 9/9 readiness artifacts schema-valid, clean score_gate3 pass=0, score_all_gates promotable=0.

### B2-REMAINING-SHORT-MR | PARKED 2026-06-06 (Codex GPT-5) | STG047/STG054/STG055 not safe on crypto data [AI: Baris|Codex]
- STG047 Brian Lee small-cap gap MR short requires US-equity gap-up scanner, low-float context, prior resistance, borrow/short frictions, and session/EOD behavior.
- STG054 fishhook EP day-1 retake requires equity episodic-pivot gap+run/day-after retake and session semantics.
- STG055 Gon low-float momentum requires low-float scanner, halt/resume events, premarket momentum, and float/volume filters.
- Decision: do **not** code crypto proxy variants. They are parked until a US-equity data source with session/float/halt fields exists.

### A3-GAP-MATRIX-DEEPSEEK-DISPATCH | DONE 2026-06-06 (Codex GPT-5) [AI: Codex|DeepSeek]
- Added `_AI_MEMORY/A3_GAP_MATRIX.md`.
- Added `_AI_MEMORY/DEEPSEEK_DISPATCH.md` with five read-only/skeptical review prompts: family mapping, no-lookahead safety, C3 adapter safety, documentation cleanup, and MOMENTUM_CONTINUATION 4h skeptical review.

## New-strategy coding (2026-06-06)

### NEWSTRAT-STG056 | DONE 2026-06-06 (Claude) | Oliver Kell price cycle coded + swept [AI: Claude]
- Registry had 63 strategies but engine GRIDS only 43 → coded one genuinely-missing backtestable candidate. Picked **STG056 Oliver Kell** (clean objective spec, pure-EMA, crypto/daily fit). STG052 (CANSLIM — needs fundamentals, no data), STG047/STG054 (equity gap plays, weak crypto fit), STG057 (LBR — needs threshold/pattern judgment, pre-register first) deliberately NOT auto-coded.
- New file `03_QUANTLENS/tools/strat_extra_runner.py` (monkey-patch layered on overnight_v2_runner, **no edit to mega_walk_forward.py or v2**). Faithful long-side mapping of `07_deterministic_spec.md`: 10/20-EMA green-light + snapback (was-below-slow within snap_lb) + wedge-pop crossback above fast EMA + higher-low; swing-low stop. All `.shift(1)` — no lookahead. Grid 36 configs.
- Smoke PASS (non-degenerate: 40-50 trades/fold). Full sweep: 68 cells (17 sym × {1h,2h,4h,1D}), **2 PASS** (TRX 4h/2h), DSR 0.031/0.041. CPCV (extra-runner loaded): both TRX **15/15 splits pass** (120/158 trades). Gate2 80.4/83.5 **INCOMPLETE** (single/few-candidate PBO insufficient — not FAIL). Output: `05_BACKTEST_RESULTS/new_strategies_2026-06-06/` (+ top-level `_results.json`, dashboard COMPLETED).
- **Verdict: works + CPCV-robust on TRX but DSR-floored + likely TRX bull-beta → NO promotion, no Pine/MTC/parity/live.** Same night-wide pattern (deeper validation can't beat DSR). Strategy reusable in engine via `strat_extra_runner.py`.
- **Carry-forward:** STG057 LBR (ROC2-reversal / 3-bar-breakout / coil-expansion) + STG054 fishhook + STG047 smallcap-gap-short are codeable the same way once Barış pre-registers the threshold/pattern definitions (avoids me inventing params → keeps DSR valid). STG056 not registered in generated registries (AGENTS.md: generator-produced); logged here + handoff only.

## Confirmation Run Follow-up (2026-06-04)

### NIGHT-CONFIRM-2026-06-04 | DONE | Quiet pre-registered confirmation run + validation tail [AI: Codex GPT-5]
- Resumed Claude's interrupted Option B path and launched the quiet confirmation run with 4 workers.
- Output: `03_QUANTLENS/05_BACKTEST_RESULTS/confirm_2026-06-04/MORNING_REPORT_confirm_2026-06-04.md`.
- Result: 306 cells / ~3,672 configs / 16 PASS / 1 BH-FDR survivor / 0 DSR-robust / 0 final robust.
- A18 fixed in output: down-market alpha count/table now matches canonical `alpha_summary.json` (`down_market_alpha=6`).
- Validation tail done: CPCV, PBO, 16 evaluation artifacts, 16 Gate-2 scorecards. Scorecards: all INCOMPLETE, 0 pass.
- Morning watchdog active until 2026-06-05 07:30 local: `03_QUANTLENS/tools/overnight_runs/_heartbeat_confirm_morning_watchdog.json`.
- No Pine/MTC/parity/live-trading action is authorized by these results.

### NIGHT-CONFIRM-2026-06-05-REVIEW | DONE 2026-06-05 (Claude) | Morning review of confirmation artifacts [AI: Claude|Baris]
- Reviewed report + CPCV/PBO + 16 scorecards. A18 verified (down_market_alpha=6 == ALPHA_DONE).
- DSR rose wide→narrow (0.0→0.34-0.38 best) but none ≥0.50; Gate-2 16/16 INCOMPLETE (metric gap, not FAIL).
- **Decision:** no promotion. Forward-paper observation OPTIONAL for 2 least-weak cells: 8EMA LINK 1h, Donchian ETH 2h. No Pine/MTC/parity/live action.
- Closure done: lessons C4-C6, runbook A19 + CHANGELOG, INDEX already had 06-05 line.

### NIGHT-FOLLOWUP-HEAVY-TIER | PARTIAL DONE 2026-06-05 (Claude) | Compute-filling heavy-validation tier [AI: Claude|Barış]
- **Problem (A19):** deterministic narrow confirmation finishes in minutes; machine sat idle-awake on watchdog the rest of the night. Tekrar = sıfır bilgi (seed=md5, mega:731).
- **DONE 2026-06-05 evening (Claude):** built `heavy_night_2026-06-05.sh` + `heavy_night_report.py`. Ran first **43-strategy** enriched sweep (3655 cells, 72 PASS+ vs 38 in the 20-strategy run) + **3×-deeper CPCV** (n_groups=10 → 45 splits, 24 cells ≥0.80) + PBO + 72 eval artifacts + Gate2 (53 PASS/19 FAIL) + scorecard_v2 (0 promotable, Gate3 INCOMPLETE). Output: `05_BACKTEST_RESULTS/heavy_tier_2026-06-05/` (+ top-level `heavy_tier_2026-06-05_results.json` for dashboard; verified visible, COMPLETED). Report: `heavy_tier_2026-06-05/HEAVY_TIER_MORNING_REPORT.md`. Closure: lessons C7/C8 + runbook A20/A21 + CHANGELOG.
- **Key finding (C7/A21):** deeper CPCV does NOT rescue DSR — Gate2 PASS ∧ CPCV-deep≥0.80 ∧ DSR≥0.50 = **0/72**. DSR trial count = grid size, not split count (A17). Re-confirms: go narrow (NIGHT-FOLLOWUP-002), not deeper/broader.
- **STILL OPEN (deliberately not autonomous):** multi-seed bootstrap stability is statistically trivial at n_boot=50k (MC SE ~0.002 → seed jitter negligible; "multi-seed DSR" moot under determinism). ±2-step pre-registered grid + 4h/1D neighborhood backtests = genuinely-new param-evals but need Barış design sign-off (A17: wider grids harm DSR). `probabilistic_pbo` lazy/random combo sampling fix (A20) for deep-CPCV PBO.
- **No Pine/MTC/parity/live action taken. No promotion (Gate3 blocker stands).**

## SP-004 rubric sign-off (2026-06-04)

### SP-004-SIGNOFF | DONE | D1-D6 owner decisions resolved [AI: Claude | Barış]
- Barış signed D1-D6 (DECISIONS D007). Rubric `12_STRATEGY_EVALUATION_RUBRIC.md` updated: D1 Gate 1B → /100 PASS≥75 (criteria rescaled ×2), D3 parity → advisory (PARITY_WARNING, non-blocking), D2/D4/D6 accepted, D5 deferred to Phase 1.5. **Unblocks Phase 2 scoring lock.**

### SP-004-PHASE1-EVALARTIFACT | DONE | evaluation_artifact writer [AI: DeepSeek/Claude]
- Done (2026-06-04 Batch G/H): `03_QUANTLENS/tools/build_evaluation_artifact.py`. CLI `--mega --cpcv --pbo --out-dir`; pure `build_artifact()`; status-enveloped metrics (OK only when computed, else NOT_COMPUTED/N_A, never auto-zero); hard_flags/flags bare per schema; version 'v1'. Claude-audited on real 5MB MEGA: 149 artifacts, 0 schema errors (Draft2020-12+$ref), 0 fabricated numbers.
- Known limits (intentional): per-fold arrays dropped from metrics (scalars only); repaint_status=null (no repaint stage), parity_status='N_A', has_benchmark=false — fill when those stages exist.

### SP-004-PHASE2-SCORINGREADER | DONE | gate2 scoring reader [AI: DeepSeek/Claude]
- Done (2026-06-04 Batch I/J): `03_QUANTLENS/tools/score_gate2.py` (`score_gate2(artifact)->dict`, CLI `--in-dir --out-dir`). 25 criteria /100 per rubric §5.1-5.7; status-gated (non-OK metric → not scored → gate INCOMPLETE, never auto-zero); REJECT_REPAINT→FAIL; PBO≥0.5→OVERFIT_SUSPECT advisory; parity advisory; pass=(OK and ≥75). Batch J reconciled Phase-1 writer to emit schema metric vocabulary. Claude-audited real 5MB: 149 artifacts 0 schema-err, 149 scorecards all INCOMPLETE (22-43, 0 pass, 0 fabricated).

### SP-004-PHASE3-GATESCORERS | DONE | Gate1/1B/3 + unified composer [AI: Grok/Claude]
- Done (2026-06-05, dispatched to Grok grok-4 via `ds_agent.py`, Claude-audited on real data; DeepSeek was 402 Insufficient Balance).
- New files under `03_QUANTLENS/tools/`: `score_gate1.py` (intake /100, 35 criteria, `intake.*` envelopes), `score_gate1b.py` (MTC feasibility /100 PASS≥75, `feasibility.*`, D1 verdict PASS/CONDITIONAL/FAIL), `score_gate3.py` (production-readiness /100, reads `production_readiness_artifact_v1` groups per D4, 37 criteria), `score_all_gates.py` (unified composer → one `scorecard_v2`, no top-level number; `gate_summary.promotable` honest = all four OK+pass).
- All mirror `score_gate2.py`: pure `score_gateX(artifact)->dict` + CLI `--in-dir --out-dir`; status-envelope (only OK scores, non-OK → `points_awarded=None` → gate INCOMPLETE, never auto-zero); `REJECT_REPAINT`→FAIL; parity advisory; utf-8 stdout.
- Claude audit (real 16 confirm-2026-06-04 eval artifacts + synthetic): py_compile PASS ×4; full-OK→100/OK/pass; empty→INCOMPLETE; gate1 MEDIUM-repaint→98; REJECT_REPAINT→FAIL; composer all-OK→promotable. **Real 16/16 = all gates INCOMPLETE, 0 pass, 0 promotable** — correct honest status (intake/feasibility/readiness artifacts not emitted yet). Inline fix: gate1b verdict PASS-under-REJECT_REPAINT → hard-fail override.
- Carry-forward: these gates stay INCOMPLETE until writer artifacts exist (intake/feasibility for Gate1/1B; `production_readiness_artifact_v1` for Gate3; Gate2 metric-enrichment below). Scorers ready to score the moment those are emitted. Nothing committed.

### SP-004-METRIC-ENRICHMENT | DONE + COMMITTED (88a79e0) | enrich builder + engine output [AI: Claude/DeepSeek | Barış approved 2026-06-05]
- Barış approved 2026-06-05 (touches MTC strategy OUTPUT, not signal/Pine/parity logic). Done via DeepSeek dispatch + Claude audit.
- **Builder (`build_evaluation_artifact.py`, Task A):** replaced the blanket-N_A block with honest per-metric derivation from data MEGA already emits — `return_pct_compound`, `recovery_factor`, `calendar_days` (from data_start/end), `multi_window_pass` (folds_positive==n_folds), `net_after_fees_pct` (cost already in net), `avg_trade_vs_cost` — plus forward-compatible passthrough for engine-emitted fields. **Integrity call (Claude): `sharpe`/`sortino` kept N_A** because MEGA's lockbox `sharpe` is a t-stat-like per-trade scaled value, NOT the annualized Sharpe the rubric scores — mapping it would inflate the gate. `param_stability_score`, `regime.*`, `long_short_ratio`, `net_after_slippage_pct` honestly N_A. Audit: rebuilt real 16 confirm artifacts, **0 schema errors** (Draft2020-12+$ref), values hand-verified; gate2 scores moved **22–43 → 42–60** (still INCOMPLETE, 0 pass, 0 fabricated — correct).
- **Engine (`mega_walk_forward.py`, Task B):** additive OUTPUT only — added `max_consecutive_losses`, `top_trade_concentration`, `equity_curve_health` to `SliceStats`/`simulate_slice` (computed from the existing per-trade `arr`/`eq`; `asdict` auto-propagates into `lockbox_oos`). No existing field/value/trade-logic changed (verified: diff additive, formulas hand-checked mcl=1/conc=0.3333/health=0.6, import-failure is pre-existing/environmental on HEAD too). Builder passthrough will surface these on the **next** MEGA run.
- **Still N_A until further work:** sharpe/sortino (need annualized definition or time-series equity), regime.* (no regime stage), benchmark.excess_alpha/beats_ema (needs B&H-on-same-window stage), worst_window_drawdown_pct, param_stability_score. Full Gate-2 PASS also needs a **fresh sweep** under the enriched engine (Barış OPS — not run here; existing artifacts built from old MEGA JSON so the 3 new engine metrics are still N_A in them).
- **NOT COMMITTED (deliberate):** `mega_walk_forward.py` carries ~245/-50 of pre-existing uncommitted Batch A–J engine work; `build_evaluation_artifact.py` is untracked Batch G/H/J. Per the standing "leave Batch edits for Barış" rule, my enrichment rides on top uncommitted — Barış decides when to commit the combined engine/builder state.

### SP-004-METRIC-ENRICHMENT-RUN | DONE | fresh sweep under enriched engine [AI: Claude, Barış go-ahead 2026-06-05]
- Ran 2026-06-05 (Claude): full MEGA sweep under enriched engine (commit 88a79e0). 1700 cells / 14m43s / 8 workers; 38 PASS+STRONG_PASS. Validation tail: CPCV (v2 patch) + PBO. Built 38 enriched artifacts + 38 Gate-2 scorecards.
- **Result (regeneration, NOT promotion):** new engine metrics (max_consecutive_losses/top_trade_concentration/equity_curve_health) + builder-derived (recovery/calendar_days/multi_window_pass/net_after_fees/avg_trade_vs_cost) + cpcv/pbo now OK 38/38. Gate-2 scores **22–43 → 39–64 (mean 51.8, top 63.6)**. Still all INCOMPLETE / 0 pass / 0 fabricated / 0 schema errors — sharpe/sortino/regime/benchmark honestly N_A.
- Output (on disk, untracked like other run dirs): `05_BACKTEST_RESULTS/enriched_metrics_2026-06-05/` (results json, cpcv, pbo, evaluation_artifacts, scorecards, ENRICHED_RUN_SUMMARY.md). No Pine/MTC/parity/live action authorized.
- **Remaining for full Gate-2 PASS (genuine future work, not fakeable):** annualized Sharpe/Sortino (needs time-series equity, not per-trade R), a regime-split stage, and a same-window Buy&Hold benchmark stage. These are the only blockers between INCOMPLETE and a scorable PASS.
- **Finding:** all 149 cells score INCOMPLETE because MEGA/CPCV/PBO don't produce: sharpe, sortino, recovery_factor, worst_window_drawdown_pct, max_consecutive_losses, calendar_days, regime_coverage_count, top_trade_concentration, long_short_ratio, param_stability_score, multi_window_pass, net_after_fees_pct, net_after_slippage_pct, avg_trade_vs_cost, equity_curve_health, return_pct_compound, benchmark.excess_alpha_pct/beats_ema, regime.* (and CPCV only ran on a few cells → cpcv_pass_ratio mostly N_A).
- To make Gate 2 fully scorable: enrich the backtest engine (mega_walk_forward) to emit these per-cell (OOS sharpe/sortino/recovery/regime split/benchmark), and run CPCV across all PASS cells. Backtest-side work — needs design + Barış. Until then INCOMPLETE is the correct honest status.

### SP-004-GATE2-BENCHMARK | DONE + COMMITTED (7175ff6) | same-window Buy&Hold benchmark [AI: DeepSeek/Codex GPT-5]
- Done 2026-06-05 via DeepSeek dispatch + Codex audit. `mega_walk_forward.py` now emits `summary.buy_hold_lockbox` for the exact lockbox window: buy at first lockbox open, hold to final lockbox close, with return, positive max drawdown, and finite return/DD ratio.
- Codex audit fixes applied: entry baseline included in the B&H equity curve so immediate drawdown is counted; helper returns JSON-native floats.
- `build_evaluation_artifact.py` now sets `benchmark.excess_alpha_pct` and `benchmark.beats_bh_risk_adjusted` to OK when real B&H inputs exist, and marks `completeness.has_benchmark` dynamically. `beats_ema_benchmark` remains N_A until a separate EMA benchmark stage exists.
- Validation PASS: py_compile, synthetic helper smoke, synthetic builder smoke, and real one-cell audit `QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL LINKUSDT 1h`. Real artifact benchmark OK (`excess_alpha_pct=97.989`, `beats_bh_risk_adjusted=true`), Gate2 score 56 but still INCOMPLETE due remaining N_A fields.
- Fresh sweep DONE 2026-06-05: `05_BACKTEST_RESULTS/bh_benchmark_2026-06-05_7175ff6/`. MEGA 1700 cells / 38 PASS+STRONG_PASS; CPCV+PBO+38 eval artifacts+38 Gate2+38 scorecard_v2 rebuilt. Audit: 38/38 artifacts B&H benchmark OK, `has_benchmark=true`, 0 schema errors. Gate2 scores 38.59-69.0 mean 52.1; still 38/38 INCOMPLETE, 0 pass, 0 promotable.
- Remaining blockers after B&H closure: annualized Sharpe/Sortino, worst-window drawdown, param stability, slippage, EMA benchmark, and regime split.

### SP-004-GATE2-WORST-WINDOW | DONE + COMMITTED (283d198) | worst-window drawdown metric [AI: DeepSeek/Codex GPT-5]
- Done 2026-06-05 via DeepSeek dispatch + Codex audit. `mega_walk_forward.py` now emits `summary.worst_window_drawdown_pct` as max absolute fold-test drawdown for the selected config; `build_evaluation_artifact.py` maps `metrics.worst_window_drawdown_pct` from that summary field first and does not fabricate it from lockbox max drawdown.
- Validation PASS: py_compile, diff-check, synthetic builder primary/fallback/missing checks, and real one-cell audit `QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL LINKUSDT 1h` emitted `worst_window_drawdown_pct=19.452`; artifact metric OK; Gate2 worst-window criterion scored 4/4; schema errors 0.
- Fresh sweep DONE 2026-06-05: `05_BACKTEST_RESULTS/worst_window_2026-06-05_283d198/`. MEGA 1700 cells / 38 PASS+STRONG_PASS; CPCV+PBO+38 eval artifacts+38 Gate2+38 scorecard_v2 rebuilt. Audit: 38/38 artifacts B&H benchmark OK and worst-window OK, 0 schema errors. Gate2 scores 42.59-73.0 mean 56.04; still 38/38 INCOMPLETE, 0 pass, 0 promotable.
- Remaining blockers after worst-window closure: annualized Sharpe/Sortino, param stability, slippage, EMA benchmark, and regime split.

### SP-004-GATE2-ANNUALIZED-RISK | DONE + COMMITTED (15e8d47) | annualized Sharpe/Sortino [AI: DeepSeek/Codex GPT-5]
- Done 2026-06-05 via DeepSeek investigation + implementation dispatch, Codex audited. MEGA now emits `lockbox_oos.annualized_sharpe` and `lockbox_oos.annualized_sortino` from a daily strategy equity curve; old MEGA `sharpe`/`sharpe_pt` are preserved and not reused for Gate2 annualized Sharpe.
- `build_evaluation_artifact.py` maps Gate2 `metrics.sharpe` and `metrics.sortino` only from the new annualized lockbox fields. Backward rebuild of pre-annualized 38 artifacts kept Sharpe/Sortino N_A 38/38.
- Validation PASS: py_compile, diff-check, real one-cell audit, existing lockbox fields unchanged, one-cell annualized_sharpe=1.307 and annualized_sortino=2.6959, Gate2 Sharpe 5/5 and Sortino 4/4, schema errors 0.
- Fresh sweep DONE 2026-06-05: `05_BACKTEST_RESULTS/annualized_risk_2026-06-05_15e8d47/`. MEGA 1700 cells / 38 PASS+STRONG_PASS; CPCV+PBO+38 eval artifacts+38 Gate2+38 scorecard_v2 rebuilt. Audit: 38/38 artifacts Sharpe/Sortino/B&H/worst-window OK, 0 schema errors. Gate2 scores 46.25-82.0 mean 61.88; still 38/38 INCOMPLETE, 0 pass, 0 promotable because param stability/slippage/EMA/regime remain N_A.
- Remaining blockers after annualized-risk closure: param stability, slippage, EMA benchmark, and regime split.

### SP-004-GATE2-SLIPPAGE | DONE + COMMITTED (5c68419) | post-hoc slippage stress [AI: DeepSeek/Codex GPT-5]
- Done 2026-06-05 via DeepSeek dispatch + Codex audit. MEGA now emits `lockbox_oos.net_after_slippage_pct` using `SLIPPAGE_BPS_PER_SIDE=2.0` (4 bps round trip) subtracted from each existing per-trade net return before compounding; existing `COST_BPS` and `net_return_pct` are unchanged.
- `build_evaluation_artifact.py` maps Gate2 `metrics.net_after_slippage_pct` only from the new lockbox field. Backward rebuild of pre-slippage 38 artifacts kept slippage N_A 38/38.
- Validation PASS: py_compile, diff-check, real one-cell audit, existing lockbox fields unchanged, one-cell net_return_pct=75.374 / net_after_slippage_pct=67.119, Gate2 slippage 2/2, schema errors 0.
- Fresh sweep DONE 2026-06-05: `05_BACKTEST_RESULTS/slippage_2026-06-05_5c68419/`. MEGA 1700 cells, 8 workers, 1212.3s, 31 PASS + 7 STRONG_PASS = 38 candidate cells; CPCV `--v2`, PBO, 38 evaluation artifacts, 38 Gate-2 scorecards, 38 scorecard_v2. Audit: 38/38 artifacts have annualized_sharpe, annualized_sortino, net_after_slippage_pct, B&H benchmark, and worst_window_drawdown_pct OK; 38/38 schema-valid (0 errors). Gate2 scores 48.25–84.0, mean 63.69; all 38 INCOMPLETE, 0 Gate2 pass, 0 promotable. Top cell 8EMA LINK 1h score 84.0 INCOMPLETE.
- Carry-forward: slippage is no longer a Gate2 blocker. Remaining blockers: param stability, EMA benchmark, and regime split.

### SP-004-GATE2-FINAL-METRICS | DONE + COMMITTED (39b51db) | param stability, EMA benchmark, regime split [AI: DeepSeek/Codex GPT-5]
- Baris approved APPROVE GATE2 DEFINITIONS. Done 2026-06-05 via DeepSeek dispatch + Codex audit.
- Implemented output-only definitions: `param_stability_score` from per-fold selected best params with numeric-closeness fallback; EMA50/EMA200 same-window long-flat benchmark mapped to `benchmark.beats_ema_benchmark`; regime split trend/range/high_vol/low_vol using EMA200, ADX14, ATR percentile buckets mapped to regime fields and `regime_coverage_count`.
- Codex audit fixes: preserved `simulate_slice` `return_trades` two-value compatibility via `return_trade_events` flag; removed EMA lookahead by acting on previous-close cross at next open; schema-null regime safeguards.
- Validation before commit: py_compile, diff-check, real one-cell MEGA LINK 8EMA 1h, existing lockbox fields unchanged vs prior slippage audit, one-cell new fields OK (`param_stability_score` 0.899, EMA benchmark present, `regime_coverage_count` 4, schema errors 0); one-cell Gate2 score 95/INCOMPLETE only because single-candidate PBO is insufficient.
- **Fresh sweep DONE 2026-06-05:** `05_BACKTEST_RESULTS/final_gate2_2026-06-05_39b51db/`. MEGA full sweep: 1700 cells, 8 workers, 1517.4s, 31 PASS + 7 STRONG_PASS = 38 candidate cells; CPCV rerun with `--max-candidates 9999` (default 20 was corrected), CPCV 38/38 OK, PBO status OK pbo=0.014569; 38 evaluation artifacts, 38 Gate2 scorecards, 38 scorecard_v2.
- **Gate2 result: 25 OK/pass, 13 FAIL, 0 INCOMPLETE.** Top scores: 100.0 8EMA LINK 1h; 100.0 GEN_ATR_PULLBACK_TREND DOGE 4h; 99.18 GEN_RSI_OVERSOLD_REVERSAL LINK 2h; 96.06 GEN_KELTNER_BREAKOUT LINK 15m; 92.31 GEN_ZSCORE_MEAN_REVERSION DOT 15m.
- **Original scorecard_v2 still promotable=0** because Gate1/Gate1B/Gate3 envelopes were absent at sweep time.
- **Gate2 metric blockers are now fully cleared.** Subsequent all-gate evidence work below fills Gate1/Gate1B from coded MEGA evidence; Gate3 remains the real blocker.

### SP-004-ALL-GATE-EVIDENCE | DONE | Gate1/Gate1B evidence + dashboard scorecard refresh [AI: DeepSeek/Codex GPT-5]
- Done 2026-06-05 after user requested all possible remaining work. DeepSeek was delegated the bounded helper; it timed out and left partial output, then Codex audited/fixed it.
- New helper: `03_QUANTLENS/tools/build_all_gate_evidence.py`. It reads final Gate2 eval artifacts plus `MEGA_walk_forward_results.json` and emits combined all-gate artifacts with `intake`, `feasibility`, production-readiness groups, and reproducibility envelopes.
- Evidence rule: Gate1/Gate1B are scored only from coded MEGA/backtest evidence. Gate3 production readiness is not fabricated; alert adapter/state sync/fail-safe and unproven MTC risk compatibility stay N_A/NOT_COMPUTED.
- CPCV safety fix: `cpcv_validator.py --max-candidates` default is now `0` = no cap; rows are sliced only when an explicit positive cap is passed.
- Real output: `05_BACKTEST_RESULTS/final_gate2_2026-06-05_39b51db/all_gate_artifacts/` (38/38 artifacts, all MEGA-matched), plus `gate1_scorecards/`, `gate1b_scorecards/`, `gate3_scorecards/`, `scorecard_v2_all_gate/`, and refreshed dashboard-visible `scorecard_v2/`.
- Validation: py_compile PASS; 38/38 all-gate artifacts validate against both `evaluation_artifact_v1` and `production_readiness_artifact_v1`; Gate1 38 OK/pass (93-96), Gate1B 38 OK/pass (80), Gate2 25 OK/pass + 13 FAIL, Gate3 38 INCOMPLETE/0 pass, promotable 0/38.
- Dashboard/API: `http://127.0.0.1:8765/api/snapshot?refresh=1` sees the final run with 38 cards: 25 `OK/OK/OK/INCOMPLETE`, 13 `OK/OK/FAIL/INCOMPLETE`.
- Remaining blocker: Gate3 production-readiness evidence source. Needs real alert/adapter/state-sync/fail-safe/live-integration artifacts before any production OK envelopes or promotion claim. [AI: Claude|Baris]

### SP-004-SCHEMA-PARITY | DONE | Move parity to advisory in schema [AI: DeepSeek/Claude]
- Done (2026-06-04 Batch F): `06_SCHEMAS/evaluation_artifact_v1.schema.json` — `parity_gate` removed from `hard_flags`; new advisory `flags.parity_status` ∈ {PASS, WARN, N_A, null}. Claude-audited: json.load VALID, Draft2020-12 check_schema VALID, parity_gate gone everywhere, completeness intact.
- **Reader carry-forward (Phase 2):** the future scoring reader must read `flags.parity_status` (NOT `hard_flags.parity_gate`) and treat WARN as non-blocking. Captured for the Phase-2 build.

## Local YouTube Transcript Collector (2026-06-04)

### YT-TRANSCRIPT-001 | DONE | Local transcript collector utility [AI: Codex GPT-5]
- Added isolated Python tool under `YT_TRANSCRIPT_COLLECTOR/`.
- Reads `urls.txt`, extracts YouTube video IDs, fetches transcripts with `youtube-transcript-api`, prefers `tr` then `en` then any available transcript, writes Markdown under `transcripts/`, and writes `reports/transcript_index.csv` plus `reports/failed_videos.csv`.
- Safety boundary: no YouTube login, no password request, no video/audio download, no browser automation, and no account actions.
- Validation: py_compile PASS, 2 offline URL extraction tests PASS from tool folder and repo root, CLI help PASS.
- Run update 2026-06-04: fetched `2NuvYsXMehw` successfully; output `YT_TRANSCRIPT_COLLECTOR/transcripts/2NuvYsXMehw.md`; metadata `Turkish (auto-generated) (tr)`. Added UTF-8 BOM URL-file regression fix/test after PowerShell input exposed it.
- Organization update 2026-06-04: moved Hermes-related transcript files into `YT_TRANSCRIPT_COLLECTOR/transcripts/hermes/`; moved contents of `Temp/HERMES/` there and deleted the old empty folder.
- No open follow-up unless Baris explicitly requests Playwright/browser fallback after transcript-api failures.

## Hermes Agent Layer (2026-06-04)

### HERMES-001 | DONE | Install Hermes and create MTC profiles [AI: Codex GPT-5]
- Installed Hermes Agent `0.15.2` in `%LOCALAPPDATA%/hermes/hermes-pypi-venv` after the official git installer clone timed out.
- Created profiles: `mtc-steward`, `quantlens-research`, `dashboard-qa`, `backtest-monitor`, `repo-hygiene`.
- Wrote profile-specific `SOUL.md` plus shared `memories/USER.md`, `memories/MEMORY.md`, and `MTC_WORKSPACE.md` guardrails.
- PATH updated for new terminals; current shells may need restart.
- Model/provider setup intentionally not selected to avoid unapproved paid/remote model routing.

### HERMES-002 | OPEN | Configure model/provider per profile [AI: Baris]
- Run one of: `<profile> setup`, `hermes -p <profile> model`, or `hermes -p <profile> config set model <provider/model>`.
- Desktop path is now also available: open Hermes Desktop, click Settings, and choose a provider/model there. Do this only when remote/paid routing is approved.

### HERMES-003 | DONE | Install Hermes Desktop app [AI: Codex GPT-5]
- Installed official Hermes Desktop under `%LOCALAPPDATA%/hermes/hermes-agent/apps/desktop/release/win-unpacked/Hermes.exe`.
- Created Desktop and Start Menu shortcuts.
- Verified normal app launch after fixing the bootstrap marker.
- Screenshot: `C:\tmp\hermes_desktop_final.png`.
- Choose cost/routing policy before using Hermes for live agent sessions.

### HERMES-004 | CLOSED 2026-08-09 (superseded) | Install proposed MTC memory package into Hermes core memory
- Package path moved to archive: `C:\LAB\MTC_LOCAL_ONLY_ARCHIVE\2026-06-21\_HERMES_MEMORY_IMPORT\`
- Closure reason (Claude Fable 5, verified on disk): live Hermes memory already exists at
  `%LOCALAPPDATA%\hermes\memories\USER.md` + `MEMORY.md` (written 2026-06-05..07) and is NEWER and richer
  than the proposed package (adds token discipline / ds_agent rules, Telegram gateway watchdog runbook,
  multi-agent landscape). Installing the June package would be a downgrade. No copy performed.
- Residual: live MEMORY.md still tells Hermes to update SESSION_LOG.md (retired 2026-07-05) — fix when
  Hermes is next actively used.

### HERMES-005 | OPEN 2026-08-09 | openai-codex token invalidated → re-auth [AI: Baris]
- Diagnosis (request dump 2026-08-09): HTTP 401 `token_invalidated` from `chatgpt.com/backend-api/codex` —
  not quota. `auth reset` + desktop restart did not help; OAuth device token itself is dead.
- Fix: `hermes auth add openai-codex --type oauth` → complete device-code sign-in in browser with the
  ChatGPT Pro account. DeepSeek provider verified working meanwhile (`-m deepseek-v4-pro --provider deepseek`).

## SP-005 Wave A status update (2026-06-04)

### SP-005 | DONE WAVE A | Strategy Detail Page Redesign [AI: Codex GPT-5]
- Status: **SP-005 Wave A implemented; Wave B/C pending.**
- Files changed: `08_DASHBOARD_APP/apps/web/app.js`, `08_DASHBOARD_APP/apps/web/styles.css`, `08_DASHBOARD_APP/apps/api/mcc_readonly/pipeline_reader.py`.
- Implemented live Strategy Detail Page Wave A: terminal single-scroll layout, human title fallback, merged Verdict & Decision block, Scorecard placeholder directly below verdict, Strategy Taxonomy shell, Review Journey, expanded Trading Rules with visible "Not defined yet", honest Backtest Evidence unavailable state/checklist, Salvageable Ideas placeholder, de-emphasized Source Material, and collapsed Technical Details carrying raw IDs/legacy composite/debug data.
- Intentionally not implemented: SP-004 scoring math, `scorecard_v2`, QuantLens structured reader, backtest-case visualizations, source-claim-vs-reproduced visuals, filter migration to gate status, Pine/MTC/parity/backtest behavior changes, audit-data deletion.
- Validation: `node --check app.js` PASS; `py_compile pipeline_reader.py` PASS; dashboard API tests PASS (`35 passed` with `PYTHONPATH` set); browser check on `http://127.0.0.1:8765/dashboard` confirms all Wave A sections render, first tested title is not raw ID, Technical Details collapsed, missing fields visible, no desktop horizontal overflow after CSS containment.
- Data caveat: current snapshot has no row with real `metrics`, so metrics-present Backtest Evidence could not be visually verified. Missing-rules, legacy-score-only, and no-QuantLens states were verified from snapshot data.

### SP-005 | DONE WAVE B | QuantLens structured reader + detail-page card [AI: Claude]
- Reader DONE (2026-06-05, dispatched to Grok grok-4, Claude-audited): read-only `08_DASHBOARD_APP/apps/api/mcc_readonly/quantlens_reader.py` parses `03_SALVAGE_IDEAS/<candidate>/01_candidate_metadata.yaml` (PyYAML, guarded import). Emits per-candidate `quantlens_verdict` (decision label, commercial-value band §8.6, complexity, testability §8.7, risks — commentary/labels, NO computed score), structured `salvageable_ideas[]` from `candidate_kind` flags, derived `stop_state` (CLOSED_SOURCE_STOP from closed_source_risk HIGH / COMPLEXITY_OVERLOAD from complexity≥8 / GARBAGE), `reference_files` repo-relative links, JSON-safe `raw`. Wired `quantlens` key into `read_model.py`. Fixed 2 audit bugs (ref-files→dir; date→str coercion). Dashboard API tests 35 passed.
- UI DONE (2026-06-05, Claude): `apps/web/app.js` — `findQuantlensCandidate` (joins by candidate_id===row.id, confirmed all 3 match pipeline/audit rows), new `renderQuantlensVerdict` card (decision badge, stop-state banner, commercial/complexity/testability/instrument facts, risk chips, recommended next step), real `renderSalvageableIdeas` from `salvageable_ideas[]`, `buildWaveADecision` now surfaces the real QuantLens label. Section order Verdict→Scorecard→QuantLens Verdict→Taxonomy. `styles.css` adds `.quantlens-stop`. Verified live in the running dashboard (preview): QL strategy renders full card (Equilibrium: SALVAGE, 4/10, 4 components), non-QL strategy shows clean "Not in QuantLens" fallback, no JS error, `node --check` PASS. Not committed.
- Carry-forward: stop-state banner code path (CLOSED_SOURCE_STOP/COMPLEXITY_OVERLOAD) is wired but unverified live (no on-disk candidate currently has a stop_state; all 3 are SALVAGE/no-stop).

### SP-005 | DONE WAVE C | scorecard_v2 gate render [AI: Codex GPT-5]
- Implemented 2026-06-05 as read-only dashboard consumption of real `scorecard_v2` artifacts.
- Added `mcc_readonly/scorecard_reader.py`; `read_model.py` now exposes top-level `scorecards` and attaches `scorecard_v2` / `scorecard_v2_cases` to matching audit/pipeline rows by base strategy id.
- Generated 38 real all-gate scorecard_v2 files for `05_BACKTEST_RESULTS/enriched_metrics_2026-06-05/scorecard_v2`; snapshot currently links 10 audit rows.
- `app.js` renders Gate 1 Intake, Gate 1B MTC Feasibility, Gate 2 Backtest Evidence, and Gate 3 Production Readiness separately; no blended score; null/non-OK scores display as `N/A`; missing/not-scored fields are visible; missing artifacts have a clean fallback.
- Validation: API py_compile PASS, API tests PASS (`35 passed, 1 subtest`), `node --check app.js` PASS, browser check PASS for one linked scorecard row and one missing-artifact fallback row with no JS console errors.
- Honest state: 38/38 scorecard_v2 are still non-promotable/INCOMPLETE because intake, feasibility, production-readiness, annualized sharpe/sortino, regime, and same-window benchmark fields are not available yet. This is expected and not a UI failure.
