# 04 — Implementation Roadmap

Phase numbers describe dependency order, not authorization. Each implementation session may execute one task only unless Barış explicitly widens scope.

**Status refresh 2026-07-29.** The blanket "all tasks are `Not started`" claim is retired; the
`Implementation status` column below is now authoritative per task. Summary verified against
`origin/master` at `3cccc4c2`: **TS-P0-001 through TS-P0-004 and TS-P1-001 through TS-P1-008 are
implemented and merged**; TS-P1-009/009B is incomplete (S1 accepted, S2 blocked, S3 unstarted);
TS-P1-010, TS-P1-011 and TS-P1-012 have no implementation or merge evidence; Phases 2–7 are not
started. This is implementation/integration verification, not a fresh re-audit or test rerun of every
task.

**Read `origin/master`, not a local checkout.** A 2026-07-29 status pass initially reported P1-001..008
as never started; that reading came from a stale local `master` (`8721bce0`, 37 commits behind) and
was wrong. Any future status claim must check `origin/master`, all refs, worktrees and commit
ancestry before asserting that work is missing. Landing evidence: P1-001 ancestry from `5140e062`;
P1-002 `eba350ce`; P1-003 `677c3a29`; P1-004 `7f72f71c`; P1-005 merge `ecc7a07e` (PR #30); P1-006
merge `e56ee282` (PR #31); P1-007 merge `87a428ba` (PR #32); P1-008 `3cccc4c2` (PR #33). The Phase 0
tooling (`IBKR_PAPER_BRIDGE/tools/check_runtime_baseline.py`, `release_evidence.py`,
`wal_state_bundle.py`) is present on `origin/master`.

## Phase outcomes

| Phase | Outcome | Entry condition | Exit condition |
| --- | --- | --- | --- |
| 0 — Preserve and baseline | The exact deployed source/config/dependency/runtime identity is mechanically visible; monitoring-window claims are honest | Roadmap accepted for planning | Gate A for Phase 0 tasks; no runtime mutation |
| 1 — Operational safety | Unknown/partial/duplicate state, reconciliation, risk, audit and security fail closed | Phase 0 identity usable | All Critical Phase 1 invariants pass mocked/fixture integration tests |
| 2 — Core separation | Stable strategy, adapter, portfolio, event, persistence and mode contracts | Phase 1 state contracts stable | Interfaces tested without changing strategy semantics |
| 3 — Research/validation stack | Reproducible tiered validation with explicit cost/fill assumptions | ADR-0020 evidence work approved | Same-data tier comparisons and manifests pass; no promotion shortcuts |
| 4 — Paper hardening | Restart/reconnect/restore/failure drills and multi-day evidence are repeatable | Phases 0–2 complete; separate testnet/paper approval | Gate D evidence; zero unexplained divergences |
| 5 — Read-only dashboard | Operations state is visible with source/age/mode/commit and honest stale states | Authoritative read model exists | No mutation path; stale/missing contract tests pass |
| 6 — Limited live | Governance package only; no start while live gate is unsigned | All prior gates plus signed ADR-0029/live gate | Separate written Barış approval; otherwise blocked |
| 7 — Controlled expansion | Scale only after evidence justifies it | Stable limited phase if ever authorized | Per-expansion ADR/gate evidence |

## Task definition matrix

| Task ID | Phase | Title | Objective | Current evidence | ADR | Priority | Complexity | Risk | Dependencies | Implementation status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TS-P0-001 | 0 | Runtime baseline drift checker | Compare repository/runtime identity read-only and emit an evidence manifest | GAP-001; shared/runtime bridge divergence | 0019, 0027 | Critical | S | Low | None | **Done** — merged; `tools/check_runtime_baseline.py` present on `origin/master` |
| TS-P0-002 | 0 | Release and rollback evidence bundle | Define immutable release manifest, config/dependency hashes and rollback target | P2RT exists; no canonical release bundle | 0008, 0017, 0019 | Critical | S | Low | P0-001 | **Done** — merged; `tools/release_evidence.py` present on `origin/master` |
| TS-P0-003 | 0 | Monitoring-window state contract | Make running/down/interrupted/reset states explicit | Runtime unavailable; Day 0 v5 documented | 0019, 0029 | Critical | S | Low | P0-001 | **Done** — merged; `tools/wal_state_bundle.py` present on `origin/master` |
| TS-P0-004 | 0 | Resolve continuation/build ADRs | Present gap/cost evidence for Barış to accept/reject ADR-0018/0025 | Gap audit now exists | 0018, 0025 | High | XS | Low | P0-001–003 | **Done 2026-07-18 (D016)** — Barış ratified ADR-0018/0025 directly; route = continue existing system, build core internally |
| TS-P1-001 | 1 | Canonical order state machine | Define exhaustive states/transitions/invariants | Partial statuses, no authoritative contract | 0023 | Critical | M | Medium | P0-002 | **Done** — merged; ancestry from `5140e062` |
| TS-P1-002 | 1 | Durable request identity and idempotency | Persist intent/request identity across retries and restarts | Deterministic cloid; run-scoped fingerprint | 0023 | Critical | M | Medium | P1-001 | **Done** — merged; `eba350ce` |
| TS-P1-003 | 1 | Unknown-submission quarantine | Reconcile ambiguous submissions before any retry | Adapter post-check exists; no durable unknown state | 0021, 0023 | Critical | M | High | P1-001, P1-002 | **Done** — merged; `677c3a29` |
| TS-P1-004 | 1 | Partial-fill protection state machine | Protect or flatten every partial quantity within policy | Fill ingestion exists; invariant incomplete | 0022, 0023 | Critical | L | High | P1-001–003 | **Done** — merged; `7f72f71c` |
| TS-P1-005 | 1 | Full reconciliation snapshot and diff | Reconcile orders, fills, positions, balances, margin and pending actions | Current positions/orders/account reconcile | 0023, 0024 | Critical | L | High | P1-001 | **Done** — merged; `ecc7a07e` (PR #30) |
| TS-P1-006 | 1 | Authoritative risk-input snapshot | Supply risk with one fresh reconciled portfolio/exchange snapshot | Risk reads point account/position values | 0022, 0023 | Critical | M | Medium | P1-005 | **Done** — merged; `e56ee282` (PR #31) |
| TS-P1-007 | 1 | Daily loss, equity-stop and drawdown enforcement | Wire reconciled PnL/equity to independent fail-closed gates | Daily-loss gate receives unproven realized PnL | 0022 | Critical | M | High | P1-006 | **Done** — merged; `87a428ba` (PR #32, durable risk controls). Supersedes the earlier interim daily-loss wiring (PR #24, `008e065e`) that was deployed to `C:\P2RT` on 2026-07-19 |
| TS-P1-008 | 1 | Exposure, leverage and liquidation controls | Enforce symbol/portfolio/wallet limits and liquidation distance | Single-position notional/leverage only | 0022 | Critical | L | High | P1-006 | **Done** — merged; `3cccc4c2` (PR #33) |
| TS-P1-009 | 1 | Kill-switch evidence and recovery | Prove disarm/cancel/flatten/restart behavior without widening web authority | Persistent kill exists | 0022, 0023, 0029 | High | M | High | P1-005–008 | **In progress — not complete.** Gate 1 signed 2026-07-27 (BLOCK→PASS, D1–D5 all=A; baseline `3cccc4c2`, scope frozen at 18 paths, opt-in schema v9 with default v4, no migration execution). TS-P1-009B slices: **S1 accepted; S2 BLOCKED; S3 unstarted.** S2 is the current blocker for Phase 1 closure |
| TS-P1-010 | 1 | Append-only audit integrity | Version and integrity-protect critical decisions/transitions | Events/decisions are durable but mutable | 0014, 0023, 0027 | High | M | Medium | P1-001, P1-005 | Not started |
| TS-P1-011 | 1 | Dependency and supply-chain baseline | Lock dependencies, inventory licenses, scan secrets/SCA, emit SBOM | Unpinned requirements | 0027 | Critical | M | Low | P0-002 | Not started |
| TS-P1-012 | 1 | Credential and outbound-network threat model | Verify least privilege, rotation/revoke policy, telemetry/outbound destinations | Env/HKCU resolver and agent-wallet policy | 0015, 0026, 0027 | Critical | M | Medium | P1-011 | Not started |
| TS-P2-001 | 2 | Versioned strategy contract | Decouple engine from concrete strategy and identify behavior/config | Small protocol; concrete Keltner construction | 0018, 0019, 0025 | High | M | Medium | P1-001, P1-006, ADR-0018/25 decision | Not started |
| TS-P2-002 | 2 | Market-data quality contract | Add sequence/gap/stale/replay definitions and quality events | Timestamp dedupe/reconnect/stale exist | 0019, 0020 | High | M | Medium | P0-002 | Not started |
| TS-P2-003 | 2 | Exchange adapter qualification | Document/test SDK-native and CCXT boundaries plus feature matrix | Official SDK adapter only | 0021, 0027 | High | M | Medium | P1-011, P1-012 | Not started |
| TS-P2-004 | 2 | Durable portfolio state | Own positions, balances, margin, exposure and PnL checkpoints | Store fragments exist | 0022–0024 | High | L | High | P1-005–008 | Not started |
| TS-P2-005 | 2 | Event and failure-state definitions | Version domain events and recovery transitions | Free-form event codes and payloads | 0014, 0023, 0024 | High | M | Medium | P1-001, P1-010 | Not started |
| TS-P2-006 | 2 | Storage benchmark and migration design | Decide keep-SQLite vs migrate; add migrations/backups contract | SQLite WAL and inline schema version | 0002, 0006, 0017, 0024 | Critical | L | Medium | P0-002, P1-010 | Not started |
| TS-P2-007 | 2 | Mode and configuration isolation | Mechanically separate research/validation/paper/future-live config/state | Partial path/config isolation | 0011, 0019 | Critical | M | Medium | P0-002, P2-006 | Not started |
| TS-P3-001 | 3 | Validation-tier contract | Resolve ADR-0020 with escalation rules and common lineage | Strong QuantLens rules; multiple partial engines | 0008, 0020 | High | M | Low | P2-001, P2-002 | Not started |
| TS-P3-002 | 3 | VectorBT rapid-research integration | Provide fast triage without claiming fill fidelity | Approximation POC; not canonical stack | 0020, 0025 | Medium | M | Low | P3-001, P1-011 | Not started |
| TS-P3-003 | 3 | Event-driven execution-parity validation | Reuse strategy contract with explicit order lifecycle/costs | Existing engine and bridge are separate | 0018, 0020, 0025 | High | L | Medium | P2-001, P3-001 | Not started |
| TS-P3-004 | 3 | hftbacktest Hyperliquid coverage audit/pilot | Decide whether/order-book strategies can use it | Coverage unverified | 0020, 0027 | Medium | M | Low | P2-002, P3-001, P1-011 | Not started |
| TS-P3-005 | 3 | Fee, slippage and funding model | Version cost assumptions and stress scenarios | Rules require costs; operational parity incomplete | 0020, 0022 | High | M | Medium | P3-001, P2-003 | Not started |
| TS-P3-006 | 3 | Reproducibility and ranking manifest | Freeze code/config/data/engine/cost/search lineage | Many artifacts, no unified tier manifest | 0008, 0019, 0020 | High | M | Low | P3-001–005 | Not started |
| TS-P4-001 | 4 | Restart recovery drill | Recover known/unknown/partial/protective state without duplicates | Startup reconcile/reprotect exists | 0023, 0029 | Critical | L | High | P1-002–005, P2-006 | Not started |
| TS-P4-002 | 4 | Reconnect/gap/REST fallback drill | Prove stream recovery and explicit degraded-state behavior | Reconnect/DATA_RESTORED historical proof | 0021–0023 | High | M | Medium | P2-002, P1-005 | Not started |
| TS-P4-003 | 4 | Backup/restore/corruption drill | Restore operational truth or fail safely | No verified recovery drill | 0017, 0024 | Critical | M | High | P2-006 | Not started |
| TS-P4-004 | 4 | Deterministic incident injection suite | Automate duplicate, timeout, partial, stale, rate, DB and kill faults | Several failure drills exist | 0022, 0023, 0027 | High | L | Medium | P1 tasks, P4-001–003 | Not started |
| TS-P4-005 | 4 | Pre-registered paper monitoring evidence | Produce daily reconciliation/incident/parity reports over approved duration | Prior P2 windows interrupted | 0019, 0029 | Critical | L | High | P4-001–004, separate approval | Not started |
| TS-P5-001 | 5 | Operations read-model contract | Export authoritative state with age/mode/version semantics | APIs exist; sources/freshness fragmented | 0016, 0028 | High | M | Low | P1-005–010, P2-005 | Not started |
| TS-P5-002 | 5 | MTC read-only operations page | Display connectivity, reconcile, differences, risk, PnL, exposure and incidents | MTC read-only shell exists | 0003, 0028 | Medium | M | Low | P5-001 | Not started |
| TS-P5-003 | 5 | Alert and incident-quality layer | Deduplicate/escalate alerts and expose runbook links | Fail-silent Telegram and DB events exist | 0027, 0028 | High | M | Low | P4-004, P5-001 | Not started |
| TS-P6-001 | 6 | Live-gate acceptance package | Resolve/sign ADR-0029 and live gate only from complete evidence | Both are unsigned/proposed | 0004, 0029 | Critical | L | High | All P0–P5 gates, Barış | Not started |
| TS-P6-002 | 6 | Limited-live release candidate | Prepare isolated small-capital release/rollback evidence; never auto-start | No authorization | 0019, 0021–0023, 0027, 0029 | Critical | XL | High | P6-001 and separate written approval | Not started |
| TS-P7-001 | 7 | Multi-symbol scheduler | Add bounded concurrency without shared-state ambiguity | Single coin/timeframe | 0018, 0019, 0022 | Medium | L | High | Stable Phase 6 evidence if ever reached | Not started |
| TS-P7-002 | 7 | Portfolio risk allocation | Add strategy/symbol/portfolio budgets and correlation stress | No portfolio layer | 0022, 0025 | High | XL | High | P2-004, P7-001 | Not started |
| TS-P7-003 | 7 | Multi-exchange support | Add one qualified adapter at a time behind common contracts | Hyperliquid only | 0021, 0025 | Low | XL | High | P2-003, P7-002 | Not started |
| TS-P7-004 | 7 | Linux/Docker qualification | Reproduce runtime, security, backup and rollback on new platform | Windows/P2RT only; VPS planned | 0011, 0017, 0019, 0027 | Medium | L | Medium | P0-002, P1-011, P4-003 | Not started |

## Delivery contract matrix

This matrix supplies the remaining mandatory fields for every roadmap item. Exact implementation scope is expanded in the backlog.

| Task ID | Expected files/modules | Acceptance criteria | Required tests | Rollback | Reference project | Notes/constraints |
| --- | --- | --- | --- | --- | --- | --- |
| TS-P0-001 | `IBKR_PAPER_BRIDGE/tools/check_runtime_baseline.py`; new tests/docs | Offline read-only manifest detects match, drift, dirty/missing runtime; deterministic exit codes; no writes | Unit + temp-repo integration + no-mutation | Delete tool/tests/docs | Current P2RT pattern | **First task**; never query exchange or change scheduler/runtime |
| TS-P0-002 | Bridge release-manifest schema/docs/tooling outside protected schemas | Manifest carries commit, tree/config/lock/schema/runtime hashes and rollback commit | Manifest contract + tamper/rollback fixture | Retain prior manifest format/read path | SLSA concepts | No deployment |
| TS-P0-003 | Status contract docs/read model/tests | Down/interrupted/reset cannot display as running/soaking | State transition/table tests | Revert reader/contract | FreqUI status patterns | Does not restart bridge |
| TS-P0-004 | ADR-0018/0025 status decision and index if approved | Explicit owner decision with rationale; no code changes | Link/status validation | Restore Proposed status via superseding record | Freqtrade/Nautilus comparison | Barış approval required |
| TS-P1-001 | `engine/types.py`, order-state doc, tests | Exhaustive legal transitions; illegal transitions fail closed | Unit/property transition tests | Feature flag/read old states | Nautilus order model | No exchange call |
| TS-P1-002 | `orders.py`, `db.py`, migrations, tests | Same intent has same identity across restart; collision/duplicate blocked | Unit, property, restart | Migration rollback/export | Hyperliquid cloid | Schema approval/migration plan first |
| TS-P1-003 | Broker/order/store/tests | Timeout enters UNKNOWN; retry impossible until absence proof | Timeout/transport/reconcile/restart tests | Disable new path, remain DISARMED | Freqtrade/Nautilus recovery | No blind retry |
| TS-P1-004 | Order manager, broker adapter, fixtures/tests | Partial qty always protected or flattened by deadline | Partial-fill permutations, failure, restart | Disable entries; preserve old close path | Hummingbot/Nautilus patterns | Testnet later, after mocks |
| TS-P1-005 | Reconciler/store/types/tests | Full snapshot produces deterministic diff/checkpoint and blocks on incomplete fetch | Contract, divergence, stale, restart | Retain prior reconcile; DISARMED | Passivbot patterns only | Foreign state never mutated automatically |
| TS-P1-006 | Portfolio/risk snapshot types/tests | Risk consumes one fresh immutable snapshot; stale/incomplete blocks | Unit/property/stale tests | Fall back to global DISARM | Nautilus risk patterns | No strategy-specific bypass |
| TS-P1-007 | Risk/store/engine/tests | Reconciled realized PnL/drawdown triggers exactly once and persists | Boundary/property/restart tests | Disable entries; preserve audit | Freqtrade protections | Threshold decision separate |
| TS-P1-008 | Risk/portfolio/config/tests | Aggregate and liquidation constraints veto deterministically | Exposure/leverage/liquidation/funding fixture tests | Restore conservative one-position cap | Riskfolio/Passivbot patterns | No third-party strategy logic |
| TS-P1-009 | Engine/order/runbook/tests | Kill is idempotent; owned orders canceled; optional flatten confirmed; restart remains killed | Mock integration + restart + failure drill | Local/manual disarm runbook | Existing bridge | Web authority not expanded |
| TS-P1-010 | Store/audit export/tests | Critical events versioned, redacted, append-only/integrity-verifiable | Tamper, ordering, redaction, restart | Export old rows; dual-read | Event sourcing patterns | Avoid institutional event bus |
| TS-P1-011 | Lock/SBOM/license/security config and docs | Rebuild from lock; scans pass or fail explicitly; SBOM retained | Clean/known-bad fixture scans | Revert lock/tool version | pip-tools/uv, CycloneDX | Installing tools separately approved |
| TS-P1-012 | Threat model, credential/outbound inventory, tests/scripts | No secrets in logs/prompts; destinations/permissions/rotation owner explicit | Redaction, config-negative, outbound policy tests | Revoke/disable connectors | Hyperliquid agent wallets | No credential values read into reports |
| TS-P2-001 | Strategy protocol/factory/config/version tests | Engine accepts registered strategy interface; current behavior fixture unchanged | Contract/golden/parity/config tests | Factory flag to current strategy | Freqtrade/Nautilus | Protected strategy semantics require approval |
| TS-P2-002 | Market-data types/feed/quality ledger/tests | Sequence/gap/stale/replay state deterministic and observable | Property/replay/reconnect/gap tests | Keep current timestamp guard | cryptofeed patterns | L2 not required for bar strategies |
| TS-P2-003 | Adapter capability matrix, interfaces/tests | Each feature names native/CCXT path and verified behavior; unsupported fails | Contract/error/rate/testnet-plan tests | Official SDK-only | CCXT/Hummingbot | No dependency until ADR/security gate |
| TS-P2-004 | Portfolio module/store/migration/tests | Restart reproduces positions/balances/exposure/PnL checkpoint | State/reconcile/restart/property tests | Export and revert schema | Nautilus portfolio model | Single writer |
| TS-P2-005 | Event schemas/codecs/tests | Versioned events round-trip; unknown version fails safely | Schema/compatibility/property tests | Dual-read prior events | CloudEvents concepts | Do not edit protected `06_SCHEMAS` without approval |
| TS-P2-006 | Benchmark tool/report, migrations, backup docs/tests | Evidence chooses SQLite or migration; upgrade/downgrade/restore proven | Load/concurrency/migration/restore | Stay on existing SQLite | SQLite/PostgreSQL | No migration before decision |
| TS-P2-007 | Mode config loader/paths/startup guards/tests | Wrong mode/credential/state root fails startup | Negative matrix + path isolation | Keep paper disabled | Twelve-factor concepts | Live mode remains absent/blocked |
| TS-P3-001 | Validation-tier spec/ADR update/tests | Strategy class maps to required tiers and evidence labels | Contract/link/same-data plan | Retain existing canonical rules | Nautilus/hftbacktest | Barış accepts ADR-0020 |
| TS-P3-002 | Research adapter, lock, tests | Same signals/metrics reproducible; output labeled approximation | Same-data/signal/property tests | Remove optional adapter | VectorBT | License/version review first |
| TS-P3-003 | Event validator/strategy adapter/tests | Explicit order lifecycle and same strategy core; no lookahead | Replay/parity/cost/restart tests | Keep current QuantLens path | Nautilus patterns | No wholesale rewrite |
| TS-P3-004 | Coverage report/pilot adapter/fixtures | Field/sequence/timestamp gaps known; integrate only if sufficient | Recorded L2 replay/latency tests | Reject/defer tool | hftbacktest | No live collector in pilot |
| TS-P3-005 | Cost-model config/module/tests | Fees/slippage/funding are versioned and stressed | Boundary/property/same-data tests | Retain old labeled results | Freqtrade cost model | Never rewrite past evidence silently |
| TS-P3-006 | Run manifest/schema/tool/tests | Rerun identifies identical inputs/results or explains nondeterminism | Hash/round-trip/replay tests | Dual-read old artifacts | MLflow concepts | No new orchestration platform needed |
| TS-P4-001 | Recovery runner/tests/run report | Crash at each state resumes DISARMED without duplicate/naked exposure | Restart matrix, recorded fixtures, testnet later | Restore prior DB/release | Existing bridge | Testnet approval required only for final tier |
| TS-P4-002 | Feed/reconciler tests/runbook | WS gap/reconnect/REST fallback yields explicit health and no silent trade | Recorded fixture, mock, then approved testnet | DISARM and restore prior release | Hyperliquid SDK | No real capital |
| TS-P4-003 | Backup tool/runbook/tests | Consistent backup restores exact checkpoint; corruption fails closed | Backup/restore/corrupt/truncate tests | Preserve original DB, never overwrite | SQLite backup API | Use temp copies in tests |
| TS-P4-004 | Failure harness/tests | Named drills deterministic with evidence and zero external side effects by default | Full drill suite | Remove harness; keep fixtures | Jepsen-style principles | Default mock/recorded only |
| TS-P4-005 | Prereg/daily report/reconciler evidence | Approved duration/sample, zero unexplained breaks, reset rules honored | Daily artifact validators + approved observations | Stop/disarm and reset clock | Freqtrade dry-run ops | Separate approval; current window not active |
| TS-P5-001 | Read-model exporter/API/tests | Every field has source/age/mode/commit/config; stale is non-green | Contract/freshness/permission tests | Disable endpoint/export | Existing MTC read model | No DB writer sharing |
| TS-P5-002 | MTC API/web/tests | Required operations panels render read-only; POST/PUT denied | API/UI/invariant/visual tests | Remove page/route | FreqUI UX only | No bridge control buttons |
| TS-P5-003 | Alert policy/notifier/read model/tests | Dedupe, severity, escalation and delivery state observable | Failure/dedupe/rate/redaction tests | Disable new routing | PagerDuty concepts | Telegram remains notification-only |
| TS-P6-001 | Signed gate/ADR/evidence index | Every item dated/owned/current; any miss is FAIL | Evidence validator/manual review | Remain paper/disarmed | Existing live gate | Barış-only decision |
| TS-P6-002 | Isolated release/runbooks/evidence only | Dedicated account/capital/limits/rollback/kill/on-call approved | Full regression, drills, paper evidence | Revoke/stop/rollback/flatten runbook | No framework substitute | No execution without new explicit authorization |
| TS-P7-001 | Scheduler/portfolio/order tests | Per-symbol isolation and bounded concurrency preserve invariants | Concurrency/property/restart tests | Reduce universe to one | Nautilus patterns | Only after stable lower phase |
| TS-P7-002 | Portfolio risk/config/tests | Aggregate allocations cannot exceed budgets under races | Scenario/property/stress tests | Conservative global cap | Riskfolio patterns | Human policy values |
| TS-P7-003 | New adapter + contract fixtures | One adapter passes full feature/security/reconcile matrix | Contract/recorded/testnet plan | Remove adapter | CCXT/Freqtrade | One exchange at a time |
| TS-P7-004 | Build/image/deploy/backup docs/tests | Reproducible image, SBOM, secrets, health, backup and rollback verified | Cross-platform/regression/image scan | Return to Windows release | Docker | Not a Phase 0 migration |

## Roadmap-wide stop rules

- Stop on unexpected changes in `C:\P2RT`, exchange state, scheduler state, credentials, protected paths, or unrelated dirty files.
- **2026-07-18 amendment (Barış):** a narrow interim TS-P1-007 (operational wiring of persisted/reconciled `realized_today`/`consecutive_losses` into the engine's `evaluate()` call, with engine-path/boundary/restart proof) is expedited and may precede P1-005/P1-006; implementation still requires separate explicit approval. No risk-control monitoring window may be counted while the DAILY_LOSS/CONSECUTIVE_LOSS gates remain inert. See the backlog amendment log. Additionally, as of 2026-07-18 **all** of ADR-0018–0029 are Proposed (the seven previously marked Accepted were unratified); ADR-status blockers in this file should be read accordingly.
- Stop if an implementation task requires accepting a Proposed ADR without owner approval.
- Stop after one task and produce its run report.
- No Phase 4 external operation, Phase 6 work, or real-capital action is implied by this roadmap.

## ADR coverage matrix

| ADR | Roadmap representation |
| --- | --- |
| ADR-0001 | TS-P5-002 uses external dashboards as UX references only |
| ADR-0002 | TS-P2-006 preserves current file/SQLite-first evolution pending evidence |
| ADR-0003 | TS-P5-001/002 enforce read-only operations surfaces |
| ADR-0004 | TS-P6-001/002 remain blocked behind explicit live governance |
| ADR-0005 | TS-P2-001 preserves review-only Pine/strategy boundaries; no Pine implementation is scheduled |
| ADR-0006 | TS-P2-006 retains single-writer/locking requirements before any database change |
| ADR-0007 | TS-P0-001 and TS-P7-004 require Windows-safe canonical paths and UTF-8 evidence |
| ADR-0008 | TS-P0-002, TS-P3-006 and every release gate require lineage |
| ADR-0009 | TS-P3-003/006 preserve manifested TradingView/parity evidence where used |
| ADR-0010 | The phase protocol protects core paths for every task |
| ADR-0011 | TS-P2-007 and TS-P7-004 isolate subprocess/runtime environments |
| ADR-0012 | The phase protocol requires mechanical protected-path checks and exact staging |
| ADR-0013 | TS-P3-006 preserves manifested manual/user inputs in lineage |
| ADR-0014 | TS-P1-010 and TS-P2-005 harden the status/event ledger |
| ADR-0015 | TS-P1-012 and TS-P5-002 keep command/network authority gated |
| ADR-0016 | TS-P5-001 defines the validated operations read model/path contract |
| ADR-0017 | TS-P0-002, TS-P2-006 and TS-P4-003 cover atomic recovery/backup behavior |
| ADR-0018 | TS-P0-004 resolves the Proposed route; TS-P2-001 is blocked on that decision |
| ADR-0019 | Phase 0 identity and TS-P2-007 implement mode/runtime/state separation |
| ADR-0020 | TS-P3-001 through TS-P3-006 are the Proposed hybrid-validation evidence path |
| ADR-0021 | TS-P2-003 qualifies official SDK, CCXT and native overrides |
| ADR-0022 | TS-P1-006 through TS-P1-009 build independent risk authority |
| ADR-0023 | TS-P1-001 through TS-P1-005 and TS-P4-001 cover order/reconcile invariants |
| ADR-0024 | TS-P2-006 and TS-P4-003 produce the Proposed storage/recovery decision evidence |
| ADR-0025 | TS-P0-004 resolves build-versus-borrow; later tasks import only bounded tools |
| ADR-0026 | TS-P1-012 enforces advisory-only LLM authority and outbound review |
| ADR-0027 | TS-P1-011/012 and release gates cover supply chain, secrets and provenance |
| ADR-0028 | TS-P5-001 through TS-P5-003 provide read-only operations visibility |
| ADR-0029 | TS-P4-005 produces paper evidence; TS-P6-001/002 remain Proposed and blocked |
