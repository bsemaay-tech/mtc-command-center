# 05 — Implementation Backlog

Backlog size: **43 tasks**.

**Status refresh 2026-07-29**, verified against `origin/master` at `3cccc4c2`. The original "all
implementation statuses are `Not started`" line is retired. Current split:

- **12 done and merged:** TS-P0-001..004 and TS-P1-001..008.
- **1 in progress:** TS-P1-009/009B — Gate 1 signed; slice S1 accepted, **S2 BLOCKED**, S3 unstarted.
- **30 not started:** TS-P1-010, TS-P1-011, TS-P1-012 and all of Phases 2–7.

This is implementation/integration verification against merged refs, not a fresh re-audit or test
rerun of every task. The "Recommended first implementation task" section below is historical —
TS-P0-001 is long complete. The current critical path is **TS-P1-009B S2 → S3 → P1-010 → P1-011 →
P1-012**, which closes Phase 1.

**Read `origin/master`, not a local checkout.** An earlier pass on 2026-07-29 reported TS-P1-001..008
as never started. That was wrong: it inspected a stale local `master` (`8721bce0`, 37 commits behind)
and did not check remote refs, worktrees, commit ancestry or merged PRs. Landing evidence: P1-001
ancestry from `5140e062`; P1-002 `eba350ce`; P1-003 `677c3a29`; P1-004 `7f72f71c`; P1-005 merge
`ecc7a07e` (PR #30); P1-006 merge `e56ee282` (PR #31); P1-007 merge `87a428ba` (PR #32, durable risk
controls, superseding the interim PR #24 wiring); P1-008 `3cccc4c2` (PR #33). Phase 0 tooling
(`check_runtime_baseline.py`, `release_evidence.py`, `wal_state_bundle.py`) is present under
`IBKR_PAPER_BRIDGE/tools/` on `origin/master`. Any future status claim must verify against
`origin/master` and all refs before asserting that work is missing.

**Remaining effort.** Remaining Phase 1 scope is 009B follow-up plus TS-P1-010/011/012 — not a full
P1 rebuild. Under the accelerated delivery plan (see the 50-hour plan document in this folder), a
realistic figure to reach a paper-eligibility candidate is **roughly 60–90 engineering hours**; one
week is possible but tight. Phase-by-phase totals for the *full* 43-task master roadmap are not
restated here, because the active target is the Safety MVP cutoff at TS-P4-005, not roadmap
completion. Effort figures exclude Barış gate decisions, D/M/R recordkeeping and wall-clock evidence
windows such as the paper soak.

## Record requirements used below

Every task requires: `D` = update its governing documentation; `M` = update `_AI_MEMORY\GLOBAL_HANDOFF.md`, `NEXT_STEPS.md`, and `ACTIVE_FILES.md` while leaving retired `SESSION_LOG.md` untouched; `R` = create a dated run report under `11_TRIAGE` or the task-approved report root. No row waives D/M/R.

## Critical blockers

- Runtime/repository drift and missing release identity: TS-P0-001 and TS-P0-002.
- Interrupted/unobservable monitoring claim: TS-P0-003.
- Unknown/partial/duplicate state and incomplete reconciliation: TS-P1-001 through TS-P1-006.
- Incomplete daily-loss/drawdown/exposure inputs: TS-P1-007 and TS-P1-008. **2026-07-18:** review proved the DAILY_LOSS and CONSECUTIVE_LOSS gates are inert through the operational engine path (`engine.py` calls `evaluate()` without `realized_today`/`consecutive_losses`; `orders.py` persists `realized_today=0.0`; `upsert_risk_day` has no callers). Barış directed an expedited narrow interim TS-P1-007 — see the amendment log at the end of this file.
- Unpinned dependencies and incomplete secret/outbound controls: TS-P1-011 and TS-P1-012.
- Database recovery evidence: TS-P2-006 and TS-P4-003.
- Live remains blocked by TS-P6-001 and the unsigned live gate.

## Recommended first implementation task

### TS-P0-001 — Add a read-only repository/runtime baseline manifest and drift checker

- **Status:** **Done and merged.** `IBKR_PAPER_BRIDGE/tools/check_runtime_baseline.py` is present on
  `origin/master` (`3cccc4c2`). This card is retained for historical scope reference only.
- **Governing ADRs:** ADR-0019 and ADR-0027; supports ADR-0018/0025 evidence.
- **Objective:** make it mechanically obvious whether the source being reviewed matches the isolated runtime, without touching either.
- **Exact scope:** add an offline CLI that accepts explicit `--repo-root`, `--runtime-root`, and expected release inputs; reads Git HEAD/status plus selected bridge source/config hashes; emits deterministic JSON and Markdown manifests; exits `0` for an exact clean match, `2` for drift/dirty/missing runtime, and `3` for invalid evidence input. Default operation must not call HTTP, the exchange, Task Scheduler, the database, or a process-control command.
- **Out of scope:** merging branches; changing `C:\P2RT`; starting/stopping/arming the bridge; reading credentials; exchange/testnet calls; changing config, requirements, scheduler, database, strategy/risk/order logic, Pine, parity, or protected paths.
- **Expected files:** `IBKR_PAPER_BRIDGE\tools\check_runtime_baseline.py`; `IBKR_PAPER_BRIDGE\tests\test_runtime_baseline.py`; `IBKR_PAPER_BRIDGE\docs\RUNTIME_BASELINE_CONTRACT.md`; one dated run report and normal memory updates.
- **Acceptance criteria:** output contains schema version, timestamp, repository/runtime canonical paths, both commits, dirty flags, selected tree/file hashes, config hash, and explicit match verdict; missing paths and malformed Git output fail safely; output is byte-stable except declared timestamp; current repository/runtime mismatch is reported without modifying either tree.
- **Required tests:** unit tests for clean match, commit drift, dirty repo, dirty runtime, missing runtime, changed config, invalid Git output, deterministic file ordering, secret-safe output, and no-mutation behavior; one read-only local integration invocation after code review.
- **Dependencies:** none.
- **Risk / effort:** Low / S (about one bounded implementation session).
- **Recommended AI:** Cline/DeepSeek builds the bounded script and tests; Codex or Claude audits the real diff and read-only invocation.
- **Human review:** Barış confirms the selected hash scope and that no runtime operation is included.
- **Documentation:** D required; cross-link from deployment/status docs only if approved scope includes them.
- **Memory:** M required; NEXT_STEPS must then name TS-P0-002 or the human-selected task.
- **Run report:** R required with exact command, raw exit code, before/after Git status, and proof `C:\P2RT` stayed clean at the same commit.
- **Rollback:** delete the new tool/test/doc and restore only its added links; no data migration or runtime rollback is needed.

## Phase 0 baseline

| ID | Exact scope; explicit out of scope | Expected files | Acceptance criteria and tests | Dependencies | Risk / effort | Recommended AI and human review | Records | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TS-P0-001 | See full card above; no runtime/process/network mutation | Tool, test, contract above | Deterministic offline drift verdict; unit + read-only integration | None | Low / S | DeepSeek/Cline build; Codex/Claude audit; Barış hash-scope review | D/M/R | **Done** — merged; `tools/check_runtime_baseline.py` on `origin/master` |
| TS-P0-002 | Define release/rollback manifest and artifact layout; no deploy or checkout | `IBKR_PAPER_BRIDGE/docs/RELEASE_EVIDENCE_CONTRACT.md`, manifest tool/tests, report | Commit/tree/config/lock/schema/runtime hashes and rollback commit validate; tamper/missing/old-version tests | P0-001 | Low / S | DeepSeek build, Codex audit; Barış approves release contract | D/M/R | **Done** — merged; `tools/release_evidence.py` on `origin/master` |
| TS-P0-003 | Add honest running/down/interrupted/reset monitoring-window state; no restart/ARM | Bridge status/read-model contract and tests | Down can never display as active soak; transition and stale-age tests | P0-001 | Low / S | DeepSeek build, Codex audit; Barış confirms reset policy | D/M/R | **Done** — merged; `tools/wal_state_bundle.py` on `origin/master` |
| TS-P0-004 | Update ADR-0018/0025 status only after owner decision; no code/import | ADR files/index and decision report | Decision cites gap/cost evidence and has explicit owner; link/status validation | P0-001–003 | Low / XS | Codex/Claude draft; Barış approval mandatory | D/M/R | **Done 2026-07-18 (D016)** — Barış ratified ADR-0018/0025; route = continue existing system |

## Phase 1 safety

**Status (2026-07-29), verified against `origin/master` `3cccc4c2`:**

- **TS-P1-001 … TS-P1-008 — done and merged.** Ancestry/merges: `5140e062`, `eba350ce`, `677c3a29`,
  `7f72f71c`, `ecc7a07e` (PR #30), `e56ee282` (PR #31), `87a428ba` (PR #32), `3cccc4c2` (PR #33).
  TS-P1-007 landed as full durable risk controls in PR #32, superseding the interim daily-loss wiring
  of PR #24 (`008e065e`) that was deployed to `C:\P2RT` on 2026-07-19.
- **TS-P1-009 / TS-P1-009B — in progress, not complete.** Gate 1 signed 2026-07-27 (BLOCK→PASS, D1–D5
  all=A; baseline `3cccc4c2`, scope frozen at 18 paths, opt-in schema v9 with default v4, no migration
  execution). Slice **S1 accepted; S2 BLOCKED; S3 unstarted.** S2 is the active blocker.
- **TS-P1-010, TS-P1-011, TS-P1-012 — not started.** No implementation or merge evidence found
  (`git log origin/master --grep="P1-01[012]"` returns nothing).

**Critical path to Phase 1 closure: 009B S2 → 009B S3 → P1-010 → P1-011 → P1-012.**

| ID | Exact scope; explicit out of scope | Expected files | Acceptance criteria and tests | Dependencies | Risk / effort | Recommended AI and human review | Records |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TS-P1-001 | Add canonical order states/transitions; no exchange call or strategy change | `engine/types.py`, order-state contract, tests | All legal/illegal transitions deterministic; unit/property tests | P0-002 | Medium / M | Claude/Codex design, DeepSeek edit; Barış accepts invariant contract | D/M/R |
| TS-P1-002 | Persist intent/request identity across restart; no retry-policy widening | `orders.py`, `db.py`, migration/tests | Same intent/same cloid; collision and duplicate blocked after restart; property/restart tests | P1-001 | Medium / M | Claude/Codex + DeepSeek; migration review required | D/M/R |
| TS-P1-003 | Add UNKNOWN_SUBMISSION quarantine/resolution; no blind retry or testnet run | broker/order/store/tests | Timeout cannot resubmit until absence proven; timeout/reconcile/restart tests | P1-001/002 | High / M | Claude/Codex; Barış reviews fail-closed policy | D/M/R |
| TS-P1-004 | Implement bounded partial-fill protect-or-flatten states; no live/testnet execution in code session | order manager, broker fixtures/tests | Every partial permutation ends protected or safely flat; partial/failure/restart tests | P1-001–003 | High / L | Claude/Codex; adversarial + Barış review | D/M/R |
| TS-P1-005 | Create complete reconcile snapshot/diff/checkpoint; no automatic mutation of foreign state | reconciler/order/store/types/tests | Orders/fills/positions/balances/margin/pending states diffed; incomplete fetch blocks; divergence tests | P1-001 | High / L | Claude/Codex; adversarial review | D/M/R |
| TS-P1-006 | Feed one immutable fresh reconcile snapshot to risk; no new thresholds | risk/portfolio snapshot types/tests | Stale/incomplete input vetoes; property/staleness tests | P1-005 | Medium / M | Claude/Codex; Barış reviews authority boundary | D/M/R |
| TS-P1-007 | Wire realized PnL, equity stop and drawdown; no threshold invention | risk/engine/store/config/tests | Boundary triggers exactly once and persists across restart; property/restart tests | P1-006 | High / M | Claude/Codex; Barış chooses policy values | D/M/R |
| TS-P1-008 | Add symbol/portfolio/wallet exposure, leverage and liquidation-distance gates; no multi-symbol scheduler | risk/portfolio/config/tests | Aggregate limits cannot be bypassed; scenario/property tests | P1-006 | High / L | Claude/Codex; Barış policy sign-off | D/M/R |
| TS-P1-009 | Prove local kill/disarm/cancel/optional flatten and restart semantics; no remote control | engine/order/runbook/tests | Idempotent kill, persistent killed state, owned-only action; mock/restart/failure tests | P1-005–008 | High / M | Codex/Claude; Barış approves any testnet drill separately | D/M/R |
| TS-P1-010 | Add versioned/redacted append-only audit integrity; no distributed event bus | store/audit codec/export/tests | Tamper detectable; critical transitions complete; redaction/ordering/restart tests | P1-001/005 | Medium / M | Claude/Codex; security review | D/M/R |
| TS-P1-011 | Pin/lock dependencies, license inventory, secret/SCA scan and SBOM; no package upgrade without approval | lock/security configs, SBOM script/docs/tests | Rebuild from lock; known-bad fixture fails; clean scan evidence | P0-002 | Low / M | DeepSeek/Cline mechanical; Codex security audit; Barış tool approval | D/M/R |
| TS-P1-012 | Threat-model credentials, wallet permissions, rotation/revoke, telemetry/outbound destinations; never record secret values | threat model, policy tests/scripts | Redaction/negative config/outbound inventory pass; named owner/recovery | P1-011 | Medium / M | Claude/Codex; Barış credential-owner review | D/M/R |

## Phase 2 architecture

**Status (2026-07-29).** All seven rows are `Not started`.

| ID | Exact scope; explicit out of scope | Expected files | Acceptance criteria and tests | Dependencies | Risk / effort | Recommended AI and human review | Records |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TS-P2-001 | Versioned strategy interface/factory/config; no strategy-behavior change | strategy protocol/factory/config tests | Current fixture/golden behavior unchanged; contract/config/parity tests | P1-001/006; ADR-0018/25 decision | Medium / M | Claude/Codex; protected-behavior approval | D/M/R |
| TS-P2-002 | Add market-data sequence/gap/stale/replay quality contract; no L2 collector yet | bars/types/quality ledger/tests | Deterministic gap state and replay; property/reconnect tests | P0-002 | Medium / M | Claude/Codex; review no trading logic drift | D/M/R |
| TS-P2-003 | Qualify official SDK/native vs CCXT feature boundary; no dependency before security gate | adapter matrix/interface/fixtures/tests | Unsupported features fail explicit; contract/error/rate tests | P1-011/012 | Medium / M | Codex/Claude; Barış accepts matrix | D/M/R |
| TS-P2-004 | Build durable portfolio checkpoints; no multi-strategy allocation | portfolio/store/migration/tests | Restart reproduces positions/balance/margin/exposure/PnL | P1-005–008 | High / L | Claude/Codex; migration/adversarial review | D/M/R |
| TS-P2-005 | Version domain events/failure states; no message broker | event schemas/codecs/tests | Round-trip/compatibility and unknown-version fail-safe | P1-001/010 | Medium / M | Claude/Codex; schema approval if protected path touched | D/M/R |
| TS-P2-006 | Benchmark SQLite writer/recovery and design migrations/backups; no database migration | benchmark/report/migration design/tests | Evidence-backed keep/migrate decision; load/migration/restore tests | P0-002, P1-010 | Medium / L | Claude/Codex; Barış accepts ADR-0024 outcome | D/M/R |
| TS-P2-007 | Separate mode config/state/credentials/startup guards; no live runtime creation | config loader/paths/tests/docs | Wrong environment fails closed; negative mode matrix | P0-002, P2-006 | Medium / M | Claude/Codex; security review | D/M/R |

## Phase 3 validation

**Status (2026-07-29).** All six rows are `Not started`.

| ID | Exact scope; explicit out of scope | Expected files | Acceptance criteria and tests | Dependencies | Risk / effort | Recommended AI and human review | Records |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TS-P3-001 | Define validation tiers/escalation/common metrics; no backtest run | tier contract/ADR-0020 decision/tests | Every strategy class maps to evidence tier; link/contract validation | P2-001/002 | Low / M | Codex/Claude; Barış accepts ADR-0020 | D/M/R |
| TS-P3-002 | Integrate optional VectorBT rapid triage; no fill-realism claim | research adapter/lock/tests | Same signals reproducible and clearly labeled approximation | P3-001, P1-011 | Low / M | DeepSeek build, Codex quantitative audit | D/M/R |
| TS-P3-003 | Build event-driven parity validator using strategy contract; no framework rewrite | validator/adapter/fixtures/tests | Same decisions/cost assumptions; replay/parity/no-lookahead tests | P2-001, P3-001 | Medium / L | Claude/Codex; adversarial quant review | D/M/R |
| TS-P3-004 | Audit/pilot hftbacktest fields and replay offline; no live collector | coverage report, recorded fixtures, optional adapter/tests | Required fields/timestamps/sequences known; accept or defer explicitly | P2-002, P3-001, P1-011 | Low / M | Codex/DeepSeek; license/security review | D/M/R |
| TS-P3-005 | Add versioned fee/slippage/funding model; no retroactive result rewrite | cost config/module/tests | Cost scenarios reproducible; boundary/property tests | P3-001, P2-003 | Medium / M | Claude/Codex; Barış approves assumptions | D/M/R |
| TS-P3-006 | Add unified run manifest and ranking lineage; no promotion-status change | manifest/tool/tests/docs | Frozen rerun identifies exact inputs and nondeterminism | P3-001–005 | Low / M | DeepSeek build, Codex audit | D/M/R |

## Phase 4 paper hardening

**Status (2026-07-29).** All five rows are `Not started`; these are the core of the accelerated Safety
MVP (WP-C/WP-D/WP-E). Note that prior IBKR paper-bridge soak
windows (Day 0 v1–v5, Day 1 v1/v2) are connectivity/reconcile/outage-tolerance evidence only and do
**not** count toward TS-P4-005, per the 2026-07-18 amendment below.

| ID | Exact scope; explicit out of scope | Expected files | Acceptance criteria and tests | Dependencies | Risk / effort | Recommended AI and human review | Records |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TS-P4-001 | Crash/restart every order state offline, then separately approved testnet drill; no real capital | recovery runner/tests/runbook | Starts DISARMED; no duplicate/naked exposure; restart matrix | P1-002–005, P2-006 | High / L | Claude/Codex; Barış external-run approval | D/M/R |
| TS-P4-002 | Reconnect/gap/REST fallback fixture drill, approved testnet later; no silent degradation | feed/reconcile tests/runbook | Health explicit; no trade on stale/unknown data | P2-002, P1-005 | Medium / M | Codex/DeepSeek; external approval for testnet | D/M/R |
| TS-P4-003 | SQLite backup/restore/corruption drill on copies; never overwrite active DB | backup tool/tests/runbook | Exact checkpoint restore; corruption fails closed | P2-006 | High / M | DeepSeek build, Codex audit; Barış recovery review | D/M/R |
| TS-P4-004 | Deterministic mock/recorded incident harness; no external side effects by default | failure harness/fixtures/tests | Duplicate/timeout/partial/stale/rate/DB/kill drills pass | P1 tasks, P4-001–003 | Medium / L | Claude/Codex; adversarial review | D/M/R |
| TS-P4-005 | Run pre-registered approved paper/testnet monitoring and daily evidence; no mainnet | prereg/reports/validators | Required duration/sample; zero unexplained diffs; resets honored | P4-001–004, explicit approval | High / L | Codex/Claude monitor; Barış approval/ownership | D/M/R |

## Phase 5 dashboard

**Status (2026-07-29).** All three rows are `Not started`.

| ID | Exact scope; explicit out of scope | Expected files | Acceptance criteria and tests | Dependencies | Risk / effort | Recommended AI and human review | Records |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TS-P5-001 | Export read-only operations state with source/age/mode/version; no writer sharing | read-model exporter/API/tests | Missing/stale never green; permission/freshness tests | P1-005–010, P2-005 | Low / M | DeepSeek build, Codex audit | D/M/R |
| TS-P5-002 | Add MTC read-only operations page; no ARM/DISARM/KILL/config writes | MTC API/web/tests | POST/PUT denied; required fields/visual states verified | P5-001 | Low / M | DeepSeek/Cline build, Codex visual audit; Barış UX review | D/M/R |
| TS-P5-003 | Add alert dedupe/escalation/delivery/incident links; Telegram notification-only | notifier/policy/read model/tests | Dedupe/rate/redaction/failure states observable | P4-004, P5-001 | Low / M | DeepSeek build, Codex security audit | D/M/R |

## Phase 6 limited live — blocked

**Status (2026-07-29).** Both rows are `Not started` and remain blocked; the live gate is unsigned.
ADR-0029 was ratified framework-only on 2026-07-18 (D016) — that ratification does **not** open the
live gate.

| ID | Exact scope; explicit out of scope | Expected files | Acceptance criteria and tests | Dependencies | Risk / effort | Recommended AI and human review | Records |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TS-P6-001 | Assemble and sign gate evidence only; no real-capital action | live gate/ADR/evidence index | Every item current, owned and PASS; any miss blocks | All P0–P5 gates; Barış | High / L | Claude/Codex audit; Barış sole decision | D/M/R |
| TS-P6-002 | Prepare isolated limited-release package only after explicit authorization; no auto-start/capital increase | release/runbooks/evidence | Dedicated account/limits/kill/rollback/on-call and full regressions approved | P6-001 + separate written approval | High / XL | Claude/Codex; Barış direct control | D/M/R |

## Phase 7 expansion

**Status (2026-07-29).** All four rows are `Not started`.

| ID | Exact scope; explicit out of scope | Expected files | Acceptance criteria and tests | Dependencies | Risk / effort | Recommended AI and human review | Records |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TS-P7-001 | Add bounded multi-symbol scheduler; no portfolio optimization | scheduler/state/tests | Per-symbol isolation under concurrency/restart | Stable lower phases | High / L | Claude/Codex; Barış scope approval | D/M/R |
| TS-P7-002 | Add portfolio allocation/correlation stress; no leverage increase by default | portfolio risk/config/tests | Aggregate budgets invariant under races/stress | P2-004, P7-001 | High / XL | Claude/Codex + quantitative review; Barış policy | D/M/R |
| TS-P7-003 | Add one exchange adapter through full contract; no simultaneous multi-adapter rollout | adapter/fixtures/tests | Feature/security/reconcile matrix passes | P2-003, P7-002 | High / XL | Claude/Codex; Barış venue approval | D/M/R |
| TS-P7-004 | Qualify Linux/Docker runtime; no forced migration from Windows | build/image/deploy/tests | Reproducible image, SBOM, secrets, backup, health, rollback pass | P0-002, P1-011, P4-003 | Medium / L | DeepSeek build, Codex security/deploy audit; Barış migration decision | D/M/R |

## Deferred research

- Advanced market making, L3 queue models, maker-capacity studies, portfolio optimization libraries, and multiple exchanges remain deferred until single-strategy/single-exchange safety evidence is stable.
- Vaults, subaccounts, builder-code fee policy, and hftbacktest live collection remain evidence tasks, not assumed features.
- Linux/Docker is Phase 7; the current Windows/P2RT path remains supported.

## Rejected work

- Wholesale rewrite or simultaneous dual-core migration without a superseding ADR.
- Forking LLM-agent bots, copy-trading bots, or small unverified Hyperliquid bots as production core.
- Copying Passivbot grid/martingale strategy logic.
- Direct LLM order authority, signer access, leverage/risk-limit mutation, or promotion authority.
- Remote dashboard trading controls in Phase 5.
- Blind retry after an unknown submission.
- Sharing mutable operational tables or credentials across research, paper/testnet, and any future live environment.

## Amendment log

### 2026-07-29 — Status refresh, corrected (recorded by Claude Opus 5)

Documents 04 and 05 still asserted that all 43 tasks were `Not started`, which had been false for
weeks. This pass replaced the blanket claim with per-task status.

**The first attempt at this refresh was wrong and has been corrected in place.** It reported
TS-P1-001..008 as never started and priced them at roughly 120 additional hours. That reading came
from a stale local `master` (`8721bce0`, 37 commits behind `origin/master`); it did not check remote
refs, worktrees, commit ancestry or merged PRs. Re-verification against `origin/master` `3cccc4c2`
shows TS-P0-001..004 and TS-P1-001..008 all implemented and merged, with Phase 0 tooling present under
`IBKR_PAPER_BRIDGE/tools/` and `bridge/engine/orders.py` reading realized PnL from the store rather
than hardcoding `0.0`.

Corrected status: 12 done and merged, TS-P1-009/009B in progress (S1 accepted, S2 blocked, S3
unstarted), TS-P1-010/011/012 and Phases 2–7 not started. Corrected remaining effort to a paper
eligibility candidate: roughly 60–90 engineering hours, not the ~250h/~600h figures the first attempt
produced. Process lesson recorded above the phase tables: verify against `origin/master` and all refs
before asserting that work is missing. No code, branch, or runtime was touched by this documentation
pass.

### 2026-07-18 — Expedited interim TS-P1-007 (Barış decision, recorded by Claude Fable 5)

Devil's-advocate review of this package verified that the daily-loss and consecutive-loss risk
gates cannot trigger operationally in either the shared branch or deployed commit `74e0990b`:
`bridge/engine/engine.py` calls `risk_engine.evaluate()` without `realized_today` or
`consecutive_losses` (defaults 0.0/0), `bridge/engine/orders.py` hardcodes `realized_today=0.0`
into the equity ledger, `bridge/store/db.py::upsert_risk_day` has zero callers, and
`tests/test_risk.py` proves the gate only by direct parameter injection. Barış decisions:

1. **Interim TS-P1-007 is expedited** ahead of the full P1-005/P1-006 chain: wire persisted or
   reconciled `realized_today` and `consecutive_losses` values through the operational engine
   `evaluate()` path. Required proof: engine-path (not parameter-injection) tests, boundary
   tests, and restart tests showing the gates can trigger and persist. No threshold changes, no
   strategy-behavior changes, no ARM action, no external execution. **Implementation still
   requires separate explicit approval before any session executes it.**
   **UPDATE 2026-07-18: execution APPROVED by Barış.** Build on a fresh branch off post-merge
   `master` (PR #23 merged 2026-07-18, merge commit `abda6717` — master bridge tree now equals
   deployed `74e0990b`). One bounded session; independent audit before any deploy.
2. **Inert gates are not accepted:** no risk-control monitoring window may start or be counted
   before this interim wiring lands. Soak windows remain valid only as
   connectivity/reconcile/outage-tolerance evidence.
3. Full TS-P1-007 (reconciled-snapshot version) remains in place behind P1-006 and supersedes
   the interim wiring when it lands.

TS-P0-001 remains the recommended first implementation task; the interim TS-P1-007 is the first
risk-logic task once approved.
