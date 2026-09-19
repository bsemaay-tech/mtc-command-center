# LEAD_TERMINAL — P020 V1.6 one-shot eligibility run (ELIG16) — 2026-09-14 20:38Z

**Outcome: the preregistered one-shot ran end-to-end and wrote `PRESELECTION_ELIGIBILITY.json` with `status = PROFILE_ELIGIBLE_NOT_ACCEPTED`.** All 45 calibration cells were evaluated, the in-memory lexicographic-first matching found a complete assignment of five distinct families to the five BTCUSDT timeframes, and all 15 locked eligibility trials (three measurement prefixes 512/1024/2048 per selected family) are trade-bearing. `one_shot: true`, `second_selection: FORBIDDEN`, `blocked: []`. Nothing was accepted by this run; the acceptance reporter, the derived measurement plan and the bounded measurement come next under their own gates.

## Run record
- Attempt 1 (20:36:07Z, `ATTEMPT1_LAUNCHER_TAB_DEFECT/`): the launcher failed BEFORE the shot — line 41 of `p020_eligibility_run_v16.ps1` carried TAB bytes (a heredoc-mangled `\t` in the tests path) so `Get-FileHash` returned null (`You cannot call a method on a null-valued expression`). No `--oneshot` call, no outputs. Fixed with the Edit tool (byte check: 0 TAB/FF bytes).
- Attempt 2 (20:38:20Z-20:38:28Z, `run.log`): roster gate passed (Opus R6 + Sol R6 PASS-WITH-NITS, Gemini SATISFIED for V1.6, Lead REPRODUCED; Grok pre-screen NOT AVAILABLE — weekly cap — supplemental slot vacant); identities OK (HEAD `b9b72f858dc830a9389517f79da5ea3c1fa6122c`, frozen = token `cb75602080850873e28dc3aa268ad1072a0f1d50148d91ad75c9896cf37fb126`, `preselect_profile.py` `c82693d4…`, `tests/test_preselect.py` `25d53fe4…`, `tests/test_sizing_floor.py` `00efdc0f…`); no prior outputs (V1.5 ABORTED files archived earlier); `pytest tests` 106 passed in 4.07 s; `--oneshot --i-have-t0-review-authorization <V1.6 digest>` exit 0 in 3 s.
- Outputs (package dir, exclusive-create, never to be deleted): `PRESELECTION_CALIBRATION.json` 1,527 B sha256 `808cbcb4ce529450e7e832baeffae00d00e64a57c456331936a75232c3299427`; `PRESELECTION_ELIGIBILITY.json` 2,003 B sha256 `fc5f8895a38147cbc76d93560b61f33cdea3b8215088acfbe6f6e8014c7bc6c2` (`calibration_sha256` inside = the calibration digest; `frozen_sha256` = V1.6). `SHA256SUMS_outputs.txt` here.

## What the tool recorded (binary only — no economic value anywhere)
| family (frozen order) | 15m | 1h | 2h | 4h | 1D |
|---|---|---|---|---|---|
| GEN_TRIPLE_EMA_STACK | 1 | 1 | 1 | 1 | 0 |
| GEN_MACD_BULL_CROSS | 1 | 1 | 1 | 1 | 0 |
| GEN_DONCHIAN_BREAKOUT | 1 | 1 | 1 | 1 | 1 |
| GEN_ATR_PULLBACK_TREND | 1 | 1 | 1 | 1 | 1 |
| GEN_GOLDEN_CROSS_PULLBACK | 1 | 1 | 1 | 1 | 1 |
| GEN_KELTNER_BREAKOUT | 1 | 1 | 1 | 1 | 0 |
| GEN_RSI_OVERSOLD_REVERSAL | 1 | 1 | 1 | 1 | 0 |
| GEN_STOCH_OVERSOLD_CROSS | 1 | 1 | 1 | 1 | 0 |
| GEN_ZSCORE_MEAN_REVERSION | 0 | 0 | 0 | 0 | 0 |
Per-timeframe trade-bearing counts 8/8/8/8/3 (V1.5 under record V2: 4/0/0/1/0 — the D8-A sizing artefact is gone). Selection by the frozen lexicographic-first rule: **15m → GEN_TRIPLE_EMA_STACK, 1h → GEN_STOCH_OVERSOLD_CROSS, 2h → GEN_KELTNER_BREAKOUT, 4h → GEN_MACD_BULL_CROSS, 1D → GEN_DONCHIAN_BREAKOUT**. 15/15 eligibility trials trade-bearing.

## What must NOT happen
No second selection, no rule change, no re-run (`second_selection: FORBIDDEN`; prereg §(g); D1 text). The selection identities are now visible: nothing about the procedure may change in response to them. The measurement plan is DERIVED from these recorded outputs by the reviewed derivation tool — after the Opus N6-8 repair (re-derive the matching from the recorded matrix; brief `laneP20DERIVFIX_build/TASK.md`) — and reviewed before the bounded measurement runs once under `OD-20260914-P020-MEASURE-1` (B YES).

## Next
1. Codex Plus: P20DERIVFIX (after the P1CAP lane) → Lead re-run of the derive tests → derive the plan from the recorded outputs (tool run by the Lead; single-read/hash rule) → derived-plan review: Lead + Gemini 3.7 + exact Sol (no Opus this week — recorded as a roster limitation for the PLAN review; the tool itself carries round-5/6 Opus acceptance).
2. Bounded measurement (15 trials) via `run_bounded_benchmark.py --run` under the owner's B YES — once, after the plan review, with its own terminal record.
3. Owner levers after the shot: Opus N6-3 (cost/funding record intervals), the 1D residual (only 3/9 families; DONCHIAN selected by rule — not a problem, information).

Recorded by Claude Opus 5 Lead (b9df29).
