# Design — MTC Run Progress Emitter (Phase 5 prerequisite)

**Date:** 2026-06-22 · **By:** Claude Opus 4.8 · **Status:** approved by Barış (design + implement) ·
**Branch:** `feature/run-progress-emitter`

## Goal
Give long backtest runs a **stable, machine-readable progress/heartbeat/event contract** so an
external watchdog (Phase 5 = n8n) can detect *finished / failed / stalled* and report *% progress*
**without keeping an AI agent open** — and without touching parity-sensitive engine code.

## Why now
Today every overnight runner writes ad-hoc `_heartbeat_<run>.json`, and the dashboard
`heartbeat_reader.py` *guesses* the schema (tries 3 timestamp keys, 3 stage keys, globs files,
mtime-picks latest). That looseness is the symptom: there is **no contract**. n8n needs one.

## Non-goals
- The n8n flow / notifications themselves (that is Phase 5 proper; this only guarantees the files).
- Any change to trading logic, signals, `mega_walk_forward.py`, parity, MTC_V2, or schemas (06).
- Running any backtest (design + code + fake-run tests only).

## Architecture — 3 parts, engine untouched
```
[supervisor]  ── launches ──>  [runner main() bookkeeping]  ──calls──> [trading fns: signals_for/
   │ liveness tick                 │ env-gated emit()                    evaluate_one]  (UNTOUCHED)
   │ + terminal status             ▼
   └──────────────────────>  progress_emitter.py  (single source: schema + atomic writes)
                                    ▼
   03_QUANTLENS/tools/overnight_runs/progress/<run_id>/
       heartbeat.json · events.jsonl · status.json     +  progress/_latest.json  (stable pointer)
```

### A. `progress_emitter.py` — shared lib + CLI
- `Emitter` class: `run_started(...)`, `phase(name)`, `progress(current,total)`, `event(type,data)`,
  `finished(result, summary, exit_code)`. Writes `heartbeat.json` (overwrite, atomic) +
  appends `events.jsonl` + maintains `progress/_latest.json` pointer.
- **Atomic writes:** write `*.tmp` then `os.replace()` (Windows-safe, no torn reads).
- **CLI** (for shell/PowerShell runners): `python progress_emitter.py <run_id> event --type X --data '{...}'`,
  `... progress --current N --total M`, `... finished --result ok`.
- **Env-gated:** `Emitter.from_env(run_id, runner)` returns a real emitter only when
  `MTC_RUN_EMITTER=1`; otherwise a `NullEmitter` (all methods no-op). → runs that don't opt in are
  byte-identical to today. Parity-safe by construction.

### B. `run_emitter_supervisor.py` — observer + liveness + terminal guarantee
- Launches the target command with `MTC_RUN_EMITTER=1` set, generates/forwards the `run_id`.
- Every `tick_seconds` (default 30) refreshes `heartbeat.json` `updated_at` (proves the *process*
  is alive even if the runner itself is mid-compute and not emitting).
- On child exit: writes `status.json` with `result=ok|fail` + `exit_code`. **Guarantees a terminal
  state even if the runner crashes/gets killed** — the in-runner emit alone cannot do this.

### C. `heartbeat_reader.py` (dashboard, read-only) — strict + fallback
- Prefer `progress/_latest.json` → load that run's `heartbeat.json`/`status.json` under the strict
  `mtc.run_progress/v1` schema.
- **Liveness uses two timestamps:** `updated_at` (process alive) and `last_progress_at` (real
  forward progress). Derived state: `updated_at` stale → **dead**; alive but `last_progress_at`
  old → **stalled**; else **running**; `status.json` present → **done/failed**.
- Keep the existing loose `_heartbeat*.json` glob as a **fallback** for old runs (back-compat).
- Stays read-only / no-execution; dashboard `overnight_heartbeat` surfaces the richer fields.

## Contract (schemas)

**`heartbeat.json`** — `mtc.run_progress/v1` (overwritten each update):
```json
{ "schema":"mtc.run_progress/v1", "run_id":"...", "runner":"...", "pid":1234,
  "started_at":"…Z", "updated_at":"…Z", "last_progress_at":"…Z",
  "phase":"sweep",
  "progress":{"current":820,"total":1700,"pct":48.2,"eta_seconds":540},
  "counters":{"completed":820,"failed":0},
  "last_event_seq":842 }
```
**`events.jsonl`** — append-only, one JSON object per line:
```json
{"seq":1,"ts":"…Z","type":"run_started|phase_started|progress|error|run_finished","data":{}}
```
**`status.json`** — `mtc.run_status/v1`, written once at terminal:
```json
{"schema":"mtc.run_status/v1","run_id":"...","result":"ok|fail","exit_code":0,
 "finished_at":"…Z","summary":{...},"report_path":"…|null"}
```

## In-runner integration (`run_quantlens_overnight_research.py`, additive + env-gated)
Emit only in `main()`'s existing bookkeeping seam (never in `signals_for`/`backtest_fixed_r`/
`evaluate_one`):
- after initial `write_json(status_path, status)` → `emit.run_started()` + `emit.phase("sweep")`;
  `total` estimated as `len(selected) × candidates × max_params`.
- in the 60s flush block → `emit.progress(completed, total)`.
- final block → `emit.finished("ok", summary)`; `except` → `emit.finished("fail")`.
All wrapped by `Emitter.from_env(...)` → no-op unless `MTC_RUN_EMITTER=1`.

## Testing (no real backtest needed — the decoupling payoff)
- **Emitter unit:** atomic write leaves no `.tmp`; `heartbeat.json` schema/fields; `events.jsonl`
  is append-only with monotonic `seq`; `_latest.json` points to current run; `NullEmitter` writes
  nothing when env off.
- **Supervisor integration:** run a scripted fake child that emits a known event sequence then
  exits 0 (and a variant exiting 1 / killed) → assert `status.json` result + terminal heartbeat.
- **Reader:** strict parse of v1; stall vs dead vs running derivation from the two timestamps;
  old `_heartbeat*.json` fallback still works.

## Files touched
- NEW `03_QUANTLENS/tools/progress_emitter.py`
- NEW `03_QUANTLENS/tools/run_emitter_supervisor.py`
- NEW `03_QUANTLENS/tools/tests/test_progress_emitter.py`, `test_run_emitter_supervisor.py`
- EDIT `08_DASHBOARD_APP/apps/api/mcc_readonly/heartbeat_reader.py` (+ test in api tests dir)
- EDIT `03_QUANTLENS/tools/run_quantlens_overnight_research.py` (additive, env-gated emit only)
- EDIT `.gitignore` (ignore `overnight_runs/progress/`)
- NO touch: `mega_walk_forward.py`, parity, MTC_V2, 06_SCHEMAS, broker/live.

## Repo-guard
Branch-isolated; exact-staged files; emitter outputs git-ignored (artifacts); no backtest executed;
no protected-scope/engine/parity change. n8n consumption deferred to Phase 5.
