# CODEX PROMPT — P2 Outage-Tolerance Policy Fix + Notify-Threshold + PR Merges (2026-07-15)

Author: Claude Fable 5 (auditor). Executor: Codex GPT-5 (builder).
Barış decisions 2026-07-15: (1) outage-tolerance policy = **option (a)**; (2) merge PRs #16→#19;
(3) PC uptime schedule below governs ARM timing.
Incident: GLOBAL_HANDOFF `[Claude Fable 5] 2026-07-15 — P2 INCIDENT #2` (commit `30a3d01f`).

## WHY (Fable-verified on live event store — do not re-derive)

P2 Day 0 v3 died 2026-07-15T08:40:06Z on a REAL Hyperliquid testnet outage (2nd in ~26h):
`ServerError` on reconnect ×5 AND on the reconcile REST call. The race fix HELD (zero
`RECONCILE_DEFERRED`, zero `HyperliquidNotConfigured`) — this is NOT a code defect. TWO
independent safety triggers fired on the same ~2-min outage: (a) reconcile single-strike at
`08:40:06Z`; (b) `DATA_STALE ws_dead_reconnect_failed` at `08:41:19Z` after the 5-attempt
reconnect budget (~75s) exhausted. Because HL testnet has ~daily ~2-min outages, **both
triggers must become outage-tolerant or every window dies.** Bounded-risk justification for a
PAPER testnet: the native stop-loss rests server-side on the exchange (positionTpsl), so a
short blind window with no local reconcile is acceptable.

## SCOPE — this is a fail-closed SAFETY change; minimal, auditable, reversible

Two files carry logic (`bridge/engine/engine.py`, `bridge/engine/bars.py`) + notifier gating
(`bridge/engine/engine.py _notify_bg` or the notify call sites) + tests. Nothing else.
Fail-closed PRINCIPLE stays; only the false-positive TIMING of two triggers changes.

## HARD RAILS

1. Branch `feature/ibkr-bridge-final` in a DEDICATED worktree:
   `git -C C:/LAB/Tradingview_LAB_CLEAN worktree add C:/BTOL feature/ibkr-bridge-final`.
   Do ALL build work there. Never `--ignore-other-worktrees`.
2. **`C:\P2RT` untouched during build** (it is DISARMED, safe). Deploy is Task 5, locked.
3. TESTNET only; `HL_LIVE_ACK` unset; never print `HL_API_WALLET_KEY`; secret grep
   `[0-9a-fA-F]{64,}` on staged diff = 0 before every commit.
4. Inline commits (hook flips HEAD): `git checkout feature/ibkr-bridge-final && git add <paths> && git commit`. Explicit paths only.
5. `PYTHONUTF8=1`; both suites (repo root + `IBKR_PAPER_BRIDGE/`) green before "done". Base =
   127 passed at `8e53439e`.
6. Report failures as failures. Fable re-runs everything on real code.

## TASK 1 — Reconcile consecutive-failure tolerance (`engine.py _run_reconcile_cycle`)

Current: ANY reconcile exception → `reconcile_ready=False` + `RECONCILE_FAILED` event +
single-strike disarm. Keep the existing `RECONCILE_DEFERRED` branch (race fix) exactly as is.

Change: add `self._consecutive_reconcile_failures: int` (init 0 in `__init__`). On a
reconcile exception that is NOT the deferred-rebuild case:
- increment the counter;
- set `reconcile_error`, and set `reconcile_ready=False` (honest — we do not know state);
- **disarm ONLY when `self._consecutive_reconcile_failures >= 3`** (config
  `reconcile_max_consecutive_failures: int = 3`, read from `bridge.yaml` risk block if present,
  default 3). On the disarming failure emit `RECONCILE_FAILED` (ERROR) exactly as today
  (event + notify + disarm), with the consecutive count in `detail`.
- For failures 1 and 2 (below threshold) emit a NEW distinct event
  `RECONCILE_FAILED_TOLERATED` (WARN) with `detail="consecutive=<n>/3; error=<type>"`, do NOT
  disarm, do NOT flip state. reconcile_ready stays False until a success.
- On ANY successful reconcile: reset `_consecutive_reconcile_failures = 0`, `reconcile_ready
  = True`, and keep the existing `RECONCILE_RECOVERED` emission when recovering from a
  not-ready state.

Invariant to assert in tests: 3rd CONSECUTIVE failure disarms; a success between failures
resets the count (2 fails → success → 2 fails must NOT disarm).

## TASK 2 — Reconnect budget extension (`bars.py`)

Current `reconnect(attempts=5, base_delay=5.0)` → ~75s before `DATA_STALE
ws_dead_reconnect_failed`. Extend the budget so a ~2-3 min outage is survived, DATA_STALE
(→disarm) only after ~5 min of continuous failed reconnect. Keep exponential backoff with the
60s cap. Make the budget config-driven (constructor args already exist; thread new defaults
from the engine/config, do not hardcode magic numbers deep in the loop):
- raise `attempts` so cumulative backoff ≈ 5 min (e.g. attempts=9 → 0+5+10+20+40+60+60+60+60 ≈
  315s); state the exact arithmetic in the report.
- leave `data_restore_timeout_s` (post-reconnect fresh-bar wait) as is UNLESS the report shows
  it needs raising to avoid a spurious `reconnect_no_fresh_data` stale; if raised, justify.
- The `DATA_STALE last_update` 2-bar staleness path (line ~176) is a separate genuine-staleness
  guard — leave it unless you can show it races the new budget; explain either way.

Alignment note: reconcile tolerance ≈3 min (Task 1) is the BINDING window; the ~5-min reconnect
budget is the outer bound. Both now exceed the observed ~2-min outages. State this in the report.

## TASK 3 — Notify-threshold (kill the ~10-min Telegram noise)

Only routine benign feed chatter is suppressed from TELEGRAM; the event store / dashboard keep
everything. Suppress Telegram dispatch for exactly these codes when routine:
`DISCONNECT`, `RECONNECT` (single successful attempt), `DATA_RESTORED`.
Continue to notify (unchanged): `RECONNECT_RETRY` (any attempt>1), `DATA_STALE`,
`RECONCILE_FAILED`, `RECONCILE_FAILED_TOLERATED`, `RECONCILE_DEFERRED`, every
`STATE_TRANSITION`, `RECONCILE_RECOVERED`, ARM/DISARM/KILL, heartbeat.
Implement as an explicit suppression set at the notify site (not by severity — DISCONNECT is
WARN and must still land in the store). Do NOT change what gets written to the DB. Add a test
asserting a routine disconnect/reconnect/restored triple produces store events but zero notifier
sends, while an escalated cycle (retry>1 / stale) DOES notify.

## TASK 4 — Tests + report → STOP for Fable audit

New tests (must fail on pre-change code where applicable):
1. reconcile 2 tolerated failures stay ARMED + `RECONCILE_FAILED_TOLERATED`; 3rd disarms.
2. failure-success-failure resets the counter (no disarm).
3. deferred-rebuild branch still defers (race-fix regression), non-configured genuine error
   still counts toward the 3-strike disarm.
4. reconnect survives a simulated ~3-min outage (mock connect failing N times then succeeding)
   without DATA_STALE; exceeding ~5 min still emits DATA_STALE + disarms.
5. notify suppression test (Task 3).
6. both full suites both CWDs; paste tails (expect ≥127 + new).

Commit to `feature/ibkr-bridge-final` in C:/BTOL (inline, secret grep). Write
`11_TRIAGE/P2_OUTAGE_TOLERANCE_REPORT_2026-07-15.md` (commands + outputs + file:line, honest
anomalies). Update `GLOBAL_HANDOFF.md` (dated section). **STOP for Fable audit. Do not deploy,
do not ARM.**

## TASK 5 — Deploy + re-ARM (LOCKED: only after Fable audit PASS + Barış go)

Single restart window, same proven sequence as 2026-07-15 Task 4 (see
`CODEX_P2_RACE_FIX_PROMPT_2026-07-14.md` §Task 4): positions/orders `[]` check → stop child →
`git -C C:/P2RT checkout --detach <audited-tip>` (P2RT is a LINKED WORKTREE, detached-HEAD
doctrine) → both-CWD suites → supervisor restart → ≥10 min observe incl. one full reconnect
cycle + clean reconciles → **exactly ONE ARM** → record new Day 0 v4 → update
03_STATUS/GLOBAL_HANDOFF/NEXT_STEPS → commit.

**ARM-TIMING per Barış PC schedule (validation-tier, NOT the definitive D3):**
- PC uptime: ON now → **2026-07-18 Sat** (then ~2h OFF) → ON → **2026-07-20** (then ~2h OFF
  morning) → **6 days uninterrupted** → pattern continues. **VPS at end of month.**
- No pre-VPS window can reach ≥10 uninterrupted days (planned PC-off on Jul 18 and Jul 20).
  Therefore a PC ARM now is **policy VALIDATION** — its purpose is to confirm the tolerance
  survives a real HL outage (≈daily) before the VPS D3. Day 0 v4 will reset at the Jul 18
  PC-off; that is expected, not a failure.
- The **definitive P2 D3 ≥10-day clock starts on the VPS** (end of month), which the VPS
  migration + this consolidated tip will seed.
- So: deploy + ARM now for validation IS worthwhile (fast real-outage evidence). Record every
  PC-off as a planned, non-incident window boundary — distinct from a safety DISARM.

## TASK 6 — Merge PRs #16→#19 (independent; after Fable audit PASS of Task 4, git-only)

Barış approved. This is NOT gated on the deploy/ARM — it is pure git housekeeping and may run
right after the Task-4 audit clears (PR #16 then already contains the policy fix).
- Order: **#16 (bridge, incl. policy fix) → #17 (UI) → #18 (faz3b prereg) → #19 (donchian).**
- #16 is clean vs master. #17/#18/#19 will conflict on `GLOBAL_HANDOFF.md` and
  `NEXT_STEPS.md` — resolve as **UNION** (keep every branch's dated sections; never drop the
  bridge/incident history). No other files should conflict — if one does, STOP and report.
- Use `gh pr merge <n> --merge` where clean; for the conflicting ones, merge locally on an
  up-to-date master with explicit union resolution, run the bridge suites once after all four
  land (still 127+ from both CWDs), then push master. Never force-push. Never rewrite master
  history.
- After merges: verify `git log --oneline master -6` shows all four, and each PR shows merged.
  Report the final master tip.

## DELIVERABLE

Both report files, dated GLOBAL_HANDOFF section, honest anomalies, explicit "no ARM / no deploy
performed" if Task 5 is still locked at your stop. STOP for Fable audit after Task 4 (+ Task 6
if you proceed to merges). Task 5 waits for Barış's go.
