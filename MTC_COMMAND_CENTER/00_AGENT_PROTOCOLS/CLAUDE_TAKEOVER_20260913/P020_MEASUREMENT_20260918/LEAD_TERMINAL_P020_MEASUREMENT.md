# LEAD_TERMINAL - WP-P0-20 bounded successor-path measurement over the DERIVED plan `d84b043a` - executed ONCE 2026-09-18 08:17:48-08:17:56 UTC+3

**Authority:** `OD-20260914-P020-MEASURE-1` ("1. B YES": once, after (a) roster, (b) PROFILE_ELIGIBLE_NOT_ACCEPTED, (c) the derived-plan review) and `OD-20260915-P020-MEASURE-GROK-1` ("no, wait for Grok (Sep 18)"). Roster for (c): exact Sol PASS-WITH-NITS (`SOL_DERIVED_REPORT.md` sha256 `96273b29`), Gemini 3.7 SATISFIED (adjudication `49877a13`), Lead trial-by-trial ALL EQUAL, **Grok pre-screen SATISFIED 2026-09-18** (`laneGKDERIV_grok/LEAD_ADJUDICATION_GROK.md` `270c48ca`; report `GROK_DERIVED_VERDICT: NITS`, 0 REQUIRED). The launcher `p020_measurement_run.ps1` checked all four before touching anything.
**Launcher defect found and fixed before any action (08:17):** the roster-gate content variables (`$sol`, `$gem`, `$lead`, `$grok`) shadowed the path variables (`$SOL`...) because PowerShell names are case-insensitive, so `Sha $SOL` hashed the report TEXT and threw at the gate's Log line - before the plan swap, before `--validate-plan`, before `--run` (benchmark dir untouched: base plan `c6f07afd` in place, no backup file, no output root; `run.log` empty). Renamed to `$solText`/`$gemText`/`$leadText`/`$grokText`; the procedure is unchanged. The shot was not spent by the failed start.

## What ran (from `run.log`, every line stamped)
- Identities before anything was touched: implementation HEAD `b9b72f85`, derived plan `d84b043a`, base plan `c6f07afd`, driver `3d4453cd`, instrument record V3 `69b6f246`; every plan-referenced source hashed `pre` and `post` (identical).
- Plan swap (Sol Q1 / Gemini Q2 procedure): base kept as `BENCHMARK_PLAN_BASE_c6f07afd.json`; derived bytes installed at `BENCHMARK_PLAN.json`; the plan line of `SHA256SUMS_V16.txt` updated for the interval (`2d7580bd` -> `463274aa`); installed plan ASSERTED `== d84b043a` after the swap, before `--validate-plan`, immediately before `--run`, after `--run`.
- `--validate-plan` in place: exit 0, `PLAN_VALID: frozen manifest, selections, hashes, and 15-trial shape verified`.
- `--run --output-root C:\tmp\CLAUDE_P0_RUN_20260913\P020_MEASUREMENT_20260915\output` (root did not exist): exit 0 in 7 s; `status: MEASUREMENT_COMPLETE_NO_ACCEPTANCE`, `semantic_equal: true`.
- Restore: `BENCHMARK_PLAN.json` back to `c6f07afd`, `SHA256SUMS_V16.txt` original bytes (`2d7580bd`), backup removed; `SHA256SUMS_V16` check 6 entries / 0 mismatches; final plan digest `c6f07afd`.

## The measurement record (`output/run_report.json`, sha256 `b19ca040`)
- `source_identity.plan_sha256 = d84b043a...` (the derived plan ran); `acceptance_verdict: NOT_EVALUATED`; `profitability_or_strategy_selection_result: NOT_PUBLISHED`.
- Interrupted-then-resumed ledger: 15 trials, completed, 0 failed, 0 duplicates, checkpoint sequence 16, executed 8 after the resume (the rest carried from the checkpoint); uninterrupted reference ledger: 15 trials, completed, 0 failed, executed 15.
- `semantic_comparison_timing_excluded`: 15 compared, `equal: true`, 0 mismatches (hash-chained journals `interrupted_resumed.jsonl` `239bfdbd`, `reference.jsonl` `86f4e70e`).
- `trade_bearing_requirement`: all trials required, fallback FORBIDDEN, `failed = 0` - every trial produced a committed-transition trade-bearing result (no `BENCHMARK_PROFILE_BLOCKED`).
- Throughput: 26.9 trials/s aggregate (reference), 24.3 trials/s (resumed); extrapolation block for 100 000 trials = 1.03 h, labelled `ESTIMATE_ONLY_NEVER_EXECUTED`; benchmark budget 8 h.
- No raw OHLC, prices, quantities, fees, funding or returns in the report (opaque semantic digests only).

## Standing
This is a MEASUREMENT record only: no acceptance, ranking, profitability, strategy selection or production authority arises (the plan's `no_profitability_or_strategy_selection_results` / `not_representative_...` fields stay true). What it establishes: the successor path executes the frozen-bound 15-trial derived plan end to end, its interrupted/resumed ledger is semantically identical to an uninterrupted run, and the throughput figure is now measured, not assumed. Carried NITs from the Grok pre-screen: driver validation depth (NIT-1), `tool_sha256` self-hash (NIT-2), `DERIVATION_RULE.md` digest drift (NIT-3) - inert for this record (the launcher's whole-file assertions and `source_identity.plan_sha256` bind what ran). Next for P0-20: the Lead's review of the record against the owner's V1.6 acceptance questions is NOT the Lead's to give - the record goes to the roster (Sol Sat, Gemini) before any acceptance discussion; the shot is spent (no re-run without a new owner word).

Recorded by Claude Opus 5 Lead (session 6, `4a8233`), 08:3x UTC+3.
