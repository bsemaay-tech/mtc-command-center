# Interim TS-P1-007 deploy + fresh monitoring window (Day 1 v1) — 2026-07-19

Operator: Claude Fable 5, executing Barış's explicit 2026-07-19 approval:
"deploy gate. Push/PR of feature/interim-daily-loss-wiring → deploy to C:\P2RT → fresh
monitoring window."

Prerequisite: round-4 independent audit PASS-WITH-NITS
(`FABLE_INTERIM_TSP1007_ROUND4_AUDIT_2026-07-19.md`).

## Git / PR

- Branch `feature/interim-daily-loss-wiring` (5 commits `6fa0c831..acb83b5b`, based on
  `abda6717` = pre-merge origin/master tip) pushed to origin.
- PR #24 created and merged (merge commit, SHAs preserved):
  https://github.com/bsemaay-tech/mtc-command-center/pull/24
- New origin/master: **`008e065e`**. Verified: `acb83b5b` is an ancestor of origin/master.
- Repo guard dry-run before merge: **PASS** (36 pre-existing dirty entries in main worktree,
  all protected/untouched; none staged).

## Deploy to C:\P2RT

Pre-deploy checks:

- `MTC-Bridge-P2` task state `Ready` (not running). Last run ended 2026-07-18 22:08 with
  0xC000013A (ctrl-c style termination — predates this session; no window was active).
- Only unrelated python process was `mcc_readonly` dashboard (left running).
- `C:\P2RT` clean, detached HEAD at `74e0990b` (field-proven prior deploy).

Deploy:

- `git -C C:\P2RT fetch origin` + `git checkout --detach 008e065e`. Post-checkout status
  clean. Bridge-tree delta vs `74e0990b` = exactly the TS-P1-007 files
  (engine.py 49±, orders.py 181±, db.py 215±, doc 20, test file; 1,489+/30−).
- Deploy verification in the deployed tree (same interpreter the supervisor uses):
  `python -m pytest tests/test_interim_risk_wiring.py -q` → **32 passed**;
  `python -m pytest tests -q` → **164 passed, 1 pre-existing warning**.

## Fresh monitoring window — Day 1 v1 OPEN

- AC power confirmed (Win32_Battery status 2); `StopIfGoingOnBatteries=False`,
  `DisallowStartIfOnBatteries=True` (unchanged, per standing decision).
- `Start-ScheduledTask MTC-Bridge-P2` at **2026-07-19T18:50:25Z** (21:50:25+03:00).
  Task `Running`; supervisor spawned `python -m bridge.app` (PID 28064).
- Log: "Application startup complete", Uvicorn on 127.0.0.1:8790.
- Run: **`paper-20260719185026`**, mode `paper`, network `testnet`, exchange `hyperliquid`,
  coin BTC, tf 1h. First reconcile 18:50:36Z clean; `risk_input_error: null`;
  `data_restore_timeout_s: 300` (field-proven fix present).
- **One ARM** at ~2026-07-19T18:52:44Z via `POST /api/arm` with state_version confirm
  (2→4), matching the approved Day 0 v5 runbook precedent. State now **ARMED**.
- Thresholds unchanged and verified in runtime config: `max_daily_loss_pct: 0.02`,
  `max_consecutive_losses: 3`, `risk_pct_per_trade: 0.005`, leverage 1 isolated.

## Evidence category for this window

This is the FIRST window in which DAILY_LOSS / CONSECUTIVE_LOSS enforcement evidence may
be counted, because the deployed runtime now contains the audited gate wiring. Keep
categories separate per standing rule: connectivity / reconnect-reconciliation /
scheduler-reliability / risk-control-enforcement. Gate enforcement claims require actual
gate-relevant events (closed losing trades, RISK_REJECT decisions, DISARM transitions)
from run `paper-20260719185026` or later on commit `008e065e`.

## Safety confirmation

- Mainnet/live: NOT touched — bridge verified `network: testnet`, `mode: paper`.
- Thresholds/strategy/schema/config: unchanged (deploy = code checkout only).
- Scheduler flags: unchanged from standing decisions.
- ARM: one paper/testnet ARM under explicit owner deploy-gate approval (precedent: Day 0
  v5 record `70586cf5`).
- `C:\P1IF`: untouched this phase, still clean at `acb83b5b`.
