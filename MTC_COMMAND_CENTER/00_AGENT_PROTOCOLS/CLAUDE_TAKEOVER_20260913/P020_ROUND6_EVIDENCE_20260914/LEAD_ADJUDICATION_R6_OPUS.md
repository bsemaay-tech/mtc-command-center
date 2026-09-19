# LEAD_ADJUDICATION_R6_OPUS — exact claude-opus-5 xhigh round-6 review of WP-P0-20 preselection V1.6 — 2026-09-14 17:03Z

Slot: Claude Pro (`--print`, xhigh, max 100 turns), authorized by `OD-20260914-P020-OPUS6-1` (the week's last Pro slot). Run 16:37:12Z-16:59:02Z (21.8 min), exit 0, 76 user turns; Pro seven-day utilization moved 0.81 → 0.85 (reset 2026-09-16 20:00Z). Report `opus/OPUS_T0_REPORT.md` (535 lines), session 1cd9bb40… in `opus/stream.jsonl`.

**Verdict as returned: PASS-WITH-NITS — 0 REQUIRED, 9 NITs.** Identities COMPUTED and matching (HEAD b9b72f85…, frozen cb756020…, procedure/tests/records); freeze reproduced byte-for-byte; 106 tests; every prior finding (R1-R6, N-1..N-5, S1-S5, NIT-1, NIT-4, T1-T4, N4-1..N4-4, Sol-4, interval check, D5, derivation tool) CLOSED against bytes except documentation residuals; item 7 real-stack arm 40/40 with a working negative control; item 10 (D9-A): V3 differs from V2 in three fields, plan/driver moved four and one line, no owner-policy value changed, no selection rule/window/prefix/family order changed; twelve RED arms fail-closed (frozen-file swap, three commit-failure paths, hostile trade container, tampered procedure byte, out-of-interval window, sizing-record dependency probe, …).

## NITs (Lead disposition; none blocks the shot — the reviewer says so and the Lead agrees)
| ID | Finding | Disposition |
|---|---|---|
| N6-1 | driver line citation `:459-493` stale in the FROZEN artifact/prereg/procedure annotations (D5 shifted the driver 11 lines); equivalence pinned mechanically | residual (documentation); recompute + re-freeze in the NEXT reviewed change, not before this shot |
| N6-2 | `abort` swallows `first_error` (zero-byte reserved file on persistent I/O failure, no ABORTED record) | residual carried from R5; the launcher records the run and the package dir is inspected after every shot |
| N6-3 | cost and funding records still declare `end_exclusive = 2025-09-22T08:00Z` (before the 15m calibration window); inert at the pinned HEAD (no interval enforcement in `economics.py`), same declared-but-unchecked class as the V1.4 abort | **owner lever, after the shot**: ratify extending both intervals to 2026-05-01 with the same word as D6/D9 (record V2 of cost/funding), or declare them documentation-only; the Lead's real-cell smoke already proves the stack accepts the real windows today |
| N6-4 | `_validate_plan` one message for four failures | diagnosability residual |
| N6-5 | `REPORT.md` banner one report behind | documentation residual |
| N6-6 | dead `base_plan` parameter in `derive_trials` | residual |
| N6-7 | two live prereg self-citations drifted (`verify_frozen_identity`, `dataset_lines`) | documentation residual; fold into N6-1's re-freeze |
| N6-8 | derivation tool does not re-derive the matching from the recorded binary matrix (a consistently rewritten output PAIR would pass; exclusive-create + never-delete are the only defence) | **fix BEFORE deriving the measurement plan**: ~10-line addition + RED test in `derive_benchmark_plan.py` (builder lane after the shot, reviewed with the derived plan) |
| N6-9 | record drift is indistinguishable from a non-trade-bearing cell (uniform BLOCKED) | observability residual; the Lead's disclosed pre-shot smoke (records accepted on real windows) excludes drift for THIS shot; a per-cell refusal-class counter is a candidate for the next reviewed change |

Roster after this adjudication: Lead REPRODUCED, Gemini 3.7 PASS (SATISFIED), Opus PASS-WITH-NITS; **Sol R6 pending** (Codex Plus reset 20:09Z, queue-r6). Grok slot vacant (weekly cap). The V1.6 token stays unused until Sol accepts. Adjudicated by Claude Opus 5 Lead (b9df29).
