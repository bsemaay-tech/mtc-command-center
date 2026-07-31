# 01 — Current System Baseline

Baseline timestamp: 2026-07-17, Europe/Chisinau. This document separates source verification from documentation claims. No test suite, bridge process, exchange request, or database query was run for this baseline.

## Identity and working state

| Item | Status | Verified value | Evidence / qualification |
| --- | --- | --- | --- |
| Repository root | Verified | `C:\LAB\Tradingview_LAB_CLEAN` with command center under `MTC_COMMAND_CENTER` | Git and filesystem inspection |
| Active branch | Verified | `feature/donchian-crypto-ladder` | `git branch --show-current` |
| Active commit | Verified | `70586cf5e023c74ac77d4cda503979c01531c36b` | `git rev-parse HEAD` |
| Working tree | Verified | Dirty before this task; pre-existing modified memory files and unrelated untracked artifacts | `git status --short`; nothing was reset, stashed, or removed |
| Documented runtime path | Verified | `C:\P2RT` | Runtime worktree exists and is a clean detached checkout |
| Runtime commit | Verified | `74e0990b1d0722a301d8385f7833d4903baeeb8f` | Read-only `git -C C:\P2RT` inspection |
| Repository/runtime equality | Verified | **No**; bridge trees differ materially | `git diff --stat 74e0990b..HEAD -- IBKR_PAPER_BRIDGE` showed 20 changed/deleted bridge files and 1,499 deletions relative to deployed runtime |
| Runtime process | Verified | Bridge not running/listening during inspection | Port 8790 had no listener; `/api/status` timed out; Task Scheduler state was `Ready` |
| Monitoring period | Partially verified | Day 0 v5 was documented as starting 2026-07-16T13:41:26.908952Z, but it is not currently observable and cannot count as uninterrupted | `_AI_MEMORY\GLOBAL_HANDOFF.md`; current read-only process/port check |
| Release status | Verified | Hyperliquid testnet/paper validation only; no mainnet release | `IBKR_PAPER_BRIDGE\README.md`, deployed config, unsigned live gate |

## Operational modes

| Environment | Status | Current capability | Evidence / limitation |
| --- | --- | --- | --- |
| Research | Verified | QuantLens registries, datasets, MEGA walk-forward, CPCV/PBO, bootstrap/BH-FDR, DSR, multi-window, benchmark reporting | Source tools and canonical rules; no run executed now |
| Backtest/validation | Verified | Existing fast/event-style Python tooling and parity infrastructure; VectorBT approximation POC exists | `03_QUANTLENS`, `01_MTC_PROJECT`, protected `02_MTC_BACKTEST`; VectorBT is not an execution-fidelity oracle |
| Local system test | Verified | Fake-money vertical slice with expected/received/filled ledgers and reconciler | `03_QUANTLENS\tools\vertical_slice`; historical completed evidence only |
| Testnet | Partially verified | Official Hyperliquid SDK connector and deployed testnet config exist; historical real testnet evidence exists | Source and tests verified; no exchange call made now |
| Paper | Partially verified | Bridge treats Hyperliquid testnet as paper and has a prior monitored P2 run | Runtime is currently unavailable; active soak not verified |
| Live/mainnet | Verified blocked | Mainnet is not authorized; no signed gate | `_AI_MEMORY\LIVE_TRADING_GATE.md`, ADR-0004, ADR-0029 Proposed |

## Capability baseline

| Subsystem | Status | Verified current capability | Evidence and limits |
| --- | --- | --- | --- |
| Language/runtime | Verified | Python; FastAPI/asyncio bridge; Windows-first operations | `IBKR_PAPER_BRIDGE\bridge\app.py`, deployment script |
| Exchange | Verified | Hyperliquid testnet using `hyperliquid-python-sdk`; signing via agent/API wallet | `bridge\broker\hyperliquid.py`, `bridge\settings.py`, deployed config |
| CCXT | Partially verified | CCXT exists in other repository data-provider paths, not in the Hyperliquid execution bridge | No CCXT bridge adapter or tested native override policy found |
| Strategy interface | Partially verified | A small `Strategy` protocol with `on_bar` and `trail_level` exists | Engine type annotation and construction are concrete `KeltnerTrailEma8`; one symbol/timeframe/strategy in v1 |
| Strategy configuration | Partially verified | YAML names a strategy file and risk config | App constructs strategy directly; no verified strategy-version/config-hash contract |
| Signal/execution separation | Partially verified | Strategy emits `Signal`; risk and order manager are separate modules | Shared reusable strategy core across research/backtest/bridge is not established |
| Market data REST | Verified | Historical candle warm-up through broker abstraction | `Broker.historical_bars`, `BarFeed.start` |
| Market data WebSocket | Verified | Candle subscription, exactly-once bar finalization, reconnect/resubscribe, stale detection | Deployed `bars.py`; timestamp dedupe exists, but no exchange sequence-gap ledger |
| Data restoration | Verified in deployed code | `DISCONNECT`, `RECONNECT`, `DATA_RESTORED`, 300-second configured restoration window | Deployed `C:\P2RT` code/tests; current shared branch lacks these latest changes |
| Funding/OI/liquidations/L2 | Not found | No maintained research collector/persistence contract in the bridge | Account/fill types include limited funding fields, not the required feed stack |
| Broker abstraction | Verified | Project-owned `Broker` protocol, MockBroker, HyperliquidBroker | Protocol covers account, positions, orders, bars, bracket, cancel, flatten, reprotect |
| Testnet/mainnet isolation | Partially verified | Testnet is hardcoded in app and deployed config; credential resolver is separate | Architecture documents describe triple lock, but current app path does not expose a mainnet mode to verify that contract |
| Agent wallet | Partially verified | Runtime loads account address plus API-wallet key; docs require non-withdrawal agent wallet | Wallet permissions/rotation were not queried |
| Subaccounts/vaults | Not found | No implementation in bridge adapter contract | Required feature qualification remains open |
| Trigger/reduce-only orders | Verified | Native bracket and protective trigger paths are present | `HyperliquidBroker.place_bracket`, `reprotect_position`; historical testnet evidence |
| Rate/nonce/time policy | Partially verified | SDK supplies signing; reconnect retry budget exists | No explicit rate-limit budget, nonce ownership monitor, or clock-skew control found |
| Deterministic order ID | Verified | Deterministic 128-bit `cloid` from decision identity and role | `HyperliquidBroker.compute_cloids`/`_raw_cloid` |
| Duplicate prevention | Partially verified | In-memory submitted set plus SQLite fingerprint uniqueness within `run_id` | Cross-run/restart semantic identity and unknown submission recovery are incomplete |
| Order states | Partially verified | OPEN/SUBMITTED/PENDING plus fill/update ingestion and matching cascade | No canonical exhaustive state machine; unknown submission, cancel-pending, expired, and partial protection invariants are incomplete |
| Partial fills | Partially verified | Fill events and `filled_qty` exist; documentation identifies protection requirement | No complete tested partial-entry-to-protected/flattened state machine found |
| Reconciliation | Partially verified | Periodic positions/open-orders/account reconcile; protective-order recovery; foreign positions ignored; ambiguous matches fail closed | Fill history, balances/margin diffs, pending cancels, unknown quarantine, and a durable reconciliation checkpoint are incomplete |
| Reconcile health | Verified in deployed code | Freshness timestamp/error, bounded tolerated failures, stale ARM rejection | Deployed code only; runtime is down, so current freshness is unavailable |
| Risk sizing | Verified | Stop-distance sizing, min order, notional/margin/leverage caps, direction/feed/state gates | `bridge\engine\risk.py` |
| Daily loss | Verified inert (2026-07-18) | Gate code exists in `RiskEngine` but is inert by construction in the operational path | `engine.py` calls `evaluate()` without `realized_today`/`consecutive_losses` (defaults 0.0/0, so DAILY_LOSS and CONSECUTIVE_LOSS can never trigger); `orders.py` persists `realized_today=0.0`; `db.py::upsert_risk_day` has no callers; `test_risk.py` passes only via direct parameter injection. Confirmed in shared branch and deployed `74e0990b` |
| Drawdown/portfolio/wallet exposure | Not found | No complete max-drawdown, aggregate exposure, or portfolio policy in bridge | Single-position notional cap is not equivalent |
| Liquidation/funding stress | Not found | Position model exposes liquidation price but risk engine does not veto on distance/funding | Target control missing |
| Kill/disarm | Verified | Persistent KILLED state, cancel-all, optional flatten, stale-data auto-disarm, post-await state checks | Local API exposes mutation endpoints; remote/authenticated design is not approved |
| Persistence | Verified | SQLite WAL; tables for runs, bars, decisions, orders, fills, trades, equity, risk days, directives, events, fingerprints | `bridge\store\db.py` |
| Schema management | Partially verified | Inline `CREATE TABLE IF NOT EXISTS`, meta schema version `2` | No ordered migration framework, rollback, compatibility test, or migration ledger |
| Backup/restore/corruption | Not found | No verified automated backup, restore drill, or corruption recovery | Roadmap must add evidence before migration decisions |
| Audit log | Partially verified | Decision chain and event rows are durable | Not tamper-evident; event detail may be free-form; no retention/export integrity contract |
| Monitoring | Partially verified | Structured DB events, status/snapshot/equity APIs, reconcile and feed events | Runtime unavailable; no metrics backend/SLO; freshness semantics incomplete |
| Telegram | Verified | Fail-silent outbound alerts and heartbeat | No delivery receipt, escalation/dedup policy, or outbound allowlist evidence |
| Bridge dashboard | Verified | Local static dashboard with REST/WS status plus ARM/DISARM/KILL/config writes | Localhost only, but it is not read-only and has no authentication beyond state-version confirmation |
| MTC dashboard | Verified | Separate read-only command-center shell/API | Project memory and dashboard source/tests; it must not import execution authority |
| Deployment | Partially verified | Isolated `C:\P2RT` worktree and Windows Task Scheduler supervisor pattern | Deployed wrapper is path-derived; active shared branch contains older hardcoded wrapper; no release manifest, lock file, health gate, or tested rollback automation |
| Dependency security | Not found | `requirements.txt` is unpinned | No lock/hashes, SCA, SBOM, container scan, or reproducible build evidence found |
| Secret handling | Partially verified | Environment/HKCU lookup, format validation, redacted errors, agent-wallet policy | No vault, permission audit, rotation drill, repository-wide automated secret gate evidence in bridge release flow |
| LLM boundary | Partially verified | LLM gate is veto-only and disabled in P2 profile; post-await state check exists | Fail-open policy exists in config; imported model providers remain outbound/security surfaces; ADR-0026 requires advisory-only future state |
| Tests | Verified | Unit/integration/failure/drill tests cover API, store, risk, strategy, broker, reconnect, duplicate bars, kill-mid-await, reconciliation, dashboard, and smoke tooling | 132-pass result is documented for deployed commit; not rerun in this planning task |
| Known incidents | Verified from records | Reconnect/user-event subscription issue, reconnect/reconciler race, testnet outages, stale-data disarms, shared-worktree runtime drift risk | Incident/status docs and `_AI_MEMORY\GLOBAL_HANDOFF.md` |

## Current release conclusion

The system is a real, non-blank Python testnet/paper bridge with meaningful safety controls. It is not a live-ready platform. The highest immediate risk is not missing framework sophistication; it is the lack of one mechanically verified release identity between the active repository, the isolated runtime, its config, and its monitoring evidence. That is why TS-P0-001 precedes all feature work.

