# Phase 5 — Backtest Watchdog (ops)

**Date:** 2026-06-22 · **By:** Claude Opus 4.8 · **Status:** Phase 5 COMPLETE (watchdog shipped;
n8n wiring is config the operator activates).

Closes Phase 5 of the AI tool integration roadmap: a finished/failed/stalled overnight run pushes
a notification **without an AI agent staying open**. Built on the Phase-5-prerequisite emitter
contract (`RUN_PROGRESS_EMITTER_DESIGN_2026-06-22.md`).

## How it works
1. A run is launched under the **supervisor** (`run_emitter_supervisor.py`) so the canonical
   contract is written to `03_QUANTLENS/tools/overnight_runs/progress/<run_id>/`
   (`heartbeat.json` · `events.jsonl` · `status.json` · `_latest.json`).
2. An external scheduler polls the **one-shot watchdog** every few minutes:
   ```
   python 03_QUANTLENS/tools/run_watchdog.py 03_QUANTLENS/tools/overnight_runs/progress
   ```
   It derives the state (`running` / `stalled` / `dead` / `done` / `failed`) and, on the first poll
   that enters an **alert state** (`done`/`failed`/`stalled`/`dead`), fires **one** notification.
   De-dupe state lives in `progress/_watchdog_state.json`, so frequent polling never re-notifies.
3. Notifications always append to `progress/_watchdog_notifications.log` (local, safe). An **opt-in**
   webhook is sent only when `--webhook-url URL` is supplied — no outward action without that URL.

## Wiring options (pick one)

### A. n8n (repo-external, preferred)
Import `03_QUANTLENS/tools/n8n/mtc_backtest_watchdog.workflow.json`:
Schedule (5 min) → Execute Command (`run_watchdog.py …`) → IF stdout ∈ {done,failed,stalled,dead}
→ **replace the `Notify` Set node with a Telegram / Email / Slack node**. Fix the two absolute
paths in the Execute Command node for the host. Toggle the workflow `active`.

### B. Windows Task Scheduler (no n8n)
Register one task that runs every 5 min:
```
python <repo>\MTC_COMMAND_CENTER\03_QUANTLENS\tools\run_watchdog.py <repo>\MTC_COMMAND_CENTER\03_QUANTLENS\tools\overnight_runs\progress --webhook-url <your-n8n-or-telegram-webhook>
```
The watchdog handles state + de-dupe; the webhook delivers the alert.

## Launch a run under the supervisor (so the contract exists)
```
python 03_QUANTLENS/tools/run_emitter_supervisor.py \
    03_QUANTLENS/tools/overnight_runs/progress <run_id> \
    --status-file <out_root>/detached/run_status.json --status-total <N> -- \
    python 03_QUANTLENS/tools/run_quantlens_overnight_research.py <runner args…>
```
The supervisor observes the runner's existing `run_status.json` → engine code is **not modified**.

## Safety
- Read-only w.r.t. the run; no backtest is launched by the watchdog.
- No outward notification unless an operator supplies a webhook URL.
- Emitter/watchdog outputs live under the already-git-ignored `overnight_runs/`.
- No engine / parity / MTC_V2 / schema / broker touch.

## Tests
`03_QUANTLENS/tools/tests/` — 22 passed (emitter, supervisor, watchdog, state machine).
Dashboard API suite — 86 passed (no regression). CLI smokes verified ok/crash/dedupe paths.
