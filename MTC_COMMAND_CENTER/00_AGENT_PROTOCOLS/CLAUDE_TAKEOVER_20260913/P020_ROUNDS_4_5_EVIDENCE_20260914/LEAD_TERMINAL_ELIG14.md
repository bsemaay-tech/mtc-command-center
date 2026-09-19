# LEAD_TERMINAL — P020 V1.4 one-shot eligibility run (ELIG14) — 2026-09-14 06:10Z

**Outcome: ABORTED at the first calibration cell, before any signal or simulation was computed. The one shot is spent (both reserved outputs exist as ABORTED records). No economic result was produced, stored or seen.**

## What happened
- 05:57:00Z gate passed: roster (Opus R4 PASS-WITH-NITS, Sol R4 PASS-WITH-NITS, Gemini SATISFIED, Lead REPRODUCED, Grok NITS), identities (HEAD b9b72f85…, frozen f839c960…, procedure c2d43525…, tests a1c9a534…), no prior outputs; 90 tests passed; `--oneshot --i-have-t0-review-authorization f839c960…` started 05:57:04Z.
- Both outputs were reserved (exclusive create) and within the same second both were rewritten as ABORTED records:
  - `PRESELECTION_CALIBRATION.json` (89 B, sha256 below): `{"error": "InstrumentRecordRefusal", "kind": "calibration", "status": "ABORTED"}`
  - `PRESELECTION_ELIGIBILITY.json` (89 B): `{"error": "InstrumentRecordRefusal", "kind": "eligibility", "status": "ABORTED"}`
- The process exited non-zero; the launcher lost the traceback (defect: `$ErrorActionPreference='Stop'` + `*>` on a native command aborts the capture on the first stderr line — `oneshot_stdout.txt` is 0 bytes; `launch.exit` was never written). The ABORTED records carry the exception class.

## Root cause (Lead diagnosis, verified with pure function calls — no simulation, nothing spent)
`InstrumentRecordRefusal` is raised by `mtc_v2/core/instrument.py` `InstrumentRecord.for_evaluation` (`REFUSED_INSTRUMENT_RECORD_OUT_OF_RANGE: evaluation timestamp is outside the record interval`) when the evaluation timestamp is not inside the record's `effective_interval`. The driver calls it at `run_bounded_benchmark.py:340` (`records.instrument.for_evaluation(frame["timestamp"].iloc[0]…)`) inside `_build_profile`, which `trade_bearing_gate` reaches at `preselect_profile.py:948` (`driver._profile`) BEFORE `build_signals`/`simulate_slice`. `trade_bearing_gate` catches only `BenchmarkProfileBlocked` (`:1094`), so the refusal propagated to `cmd_oneshot`, which aborted both reserved files (`:1067-1069`) — exactly the T3 behaviour.
The synthetic instrument record `C:/tmp/P020_LEAD_20260912/benchmark/SYNTH-P020-BOUNDED-INSTRUMENT-V1.json` has `effective_interval.start_inclusive = 2019-09-08T00:00:00Z`, `end_exclusive = 2025-09-22T08:00:00Z` — sized for the MEASUREMENT prefixes (rows 1..2048). First timestamps of the frozen CALIBRATION windows (row 2049 of each dataset, read from the manifest's normalized CSVs):

| tf | calibration first ts (row 2049) | inside record interval? | measurement row 2048 ts |
|---|---|---|---|
| 15m | 2025-09-22T08:00:00Z | **NO — equals `end_exclusive`** | 2025-09-22T07:45:00Z |
| 1h | 2024-07-02T17:00:00Z | yes | 2024-07-02T16:00:00Z |
| 2h | 2024-10-06T18:00:00Z | yes | 2024-10-06T16:00:00Z |
| 4h | 2020-08-15T00:00:00Z | yes | 2020-08-14T20:00:00Z |
| 1D | 2025-04-17T00:00:00Z | yes | 2025-04-16T00:00:00Z |

Pure reproduction with the driver's own loader (`EconomicRecords.from_record_paths` → `for_evaluation`): `2025-09-22T07:45:00Z -> OK`; `2025-09-22T08:00:00Z -> InstrumentRecordRefusal('REFUSED_INSTRUMENT_RECORD_OUT_OF_RANGE: …')`. The cell order in `_run_oneshot:1087-1088` is families × TIMEFRAMES with `15m` first, so the very first cell (family 1 × 15m) raised.

## Classification
A **preregistration precondition defect**: V1.4 pins the economic record digests (`verify_frozen_identity`, source pins) but never checks that each calibration window lies inside the instrument record's effective interval; the 15m calibration window (rows 2049..4096 = 2025-09-22T08:00Z..2025-10-13T15:45Z) lies entirely outside it, so the preregistered procedure was never executable on the frozen inputs. Every roster member had listed the real profile stack under NOT VERIFIED (Opus §8.2, Sol NOT VERIFIED, Grok "real driver/engine path has never been run", Gemini SUPPLEMENTAL_UNEXECUTED); the reviews were correct about the procedure's code and wrong to be silent about this input precondition — a declared-but-unchecked gap. Not a selection-rule change, not an economic outcome: `BENCHMARK_PROFILE_BLOCKED` was never reached.

## What this does NOT mean
- No family/timeframe was evaluated; no matrix, selection or trial result exists (both files are ABORTED records only).
- The V1.4 token is now spent by the tool's own rule (`PRESELECT_REFUSED_ALREADY_RUN` on re-run); the files must not be deleted (runbook). Any re-run needs an owner ruling (D6) and a V1.5 re-freeze because the fix touches frozen inputs.
- Owner B NO (no bounded measurement) is unaffected — nothing to measure.

## Digests
- PRESELECTION_CALIBRATION.json sha256 recorded below; PRESELECTION_ELIGIBILITY.json likewise (see the sha256sum lines appended by the Lead).
5ebbcfd8f86370959360fb9207ce0b1b06e45659345ea2fa0bc96de9c152c449 */c/tmp/P020_PRESELECT_20260913/PRESELECTION_CALIBRATION.json
7f3f8f47ca15eb6c85c7c93058c975fddfeb138fa4509d0ca784861a272f1bf4 */c/tmp/P020_PRESELECT_20260913/PRESELECTION_ELIGIBILITY.json
