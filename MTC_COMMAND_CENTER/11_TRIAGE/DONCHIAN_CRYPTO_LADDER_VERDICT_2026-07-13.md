# GEN_DONCHIAN_BREAKOUT — Crypto Evidence Ladder Verdict (2026-07-13)

> **What changed:** GEN_DONCHIAN_BREAKOUT (the open US-equities-10m research lead) was taken
> through the full canonical evidence ladder on crypto: BTCUSD + ETHUSD × 1h + 4h,
> primary Alpaca multi-asset bundle, one pre-registered 4-cell run.
> **What matters:** **VERDICT = NULL.** 0/4 cells PASS walk-forward. 3 REJECTED (negative
> lockbox, PF < 1), 1 INSUFFICIENT_TRADES. 0 BH-FDR survivors, 0 DSR-robust, 0 robust_final.
> No FORWARD_PAPER mapping applies (nothing was WF-PASS, CPCV had zero eligible candidates).
> **Next action:** none for this lead on this universe. Crypto Paper Bridge export: **NOT READY —
> no candidate exists**; bridge untouched per session scope.

## Executive Summary

The Donchian breakout lead does **not** transfer to BTC/ETH at 1h/4h. All four cells failed the
first gate (rolling walk-forward + lockbox): three lost money outright on the 25% lockbox
(−16.8% to −22.4%, PF 0.70–0.95), and the only positive cell (ETHUSD 4h, +30.8%) produced just
9 lockbox trades — below the 30-trade guardrail, hence `INSUFFICIENT_TRADES`, never PASS.
Downstream statistical gates confirm: bootstrap family m=3, BH-FDR survivors 0; DSR confidence
0.0001 / 0.0 / 0.0 / 0.24 — all far below even the pragmatic crypto research bar (≥ 0.50).
This is consistent with the 4-night finding (63 archetypes, 0 robust_final): the ceiling is
methodological, not strategy selection. **NULL is the honest verdict.**

## Key Decisions

- Pre-registered scope: 1 strategy × {BTCUSD, ETHUSD} × {1h, 4h}, base grid, default
  `fixed_2R` exit (swept exits are Faz 3b and need their own pre-registration).
- All 4 cells ran in **one engine invocation** so BH-FDR multiplicity is corrected across the
  whole family, not per-cell.
- A22 compliance: newest lessons read pre-launch; smoke = 2.8 s/cell → full run ≈ 5 s; run-progress
  supervisor deliberately **not** used (reserved for long runs), machine released immediately.
- A23 compliance: explicit `--symbol/--tf` passed (flags override the hardcoded legacy universe;
  manifest alone only binds data).

## Tested Universe & Data Coverage (verified on disk, rules §3)

Bundle: `native_multiasset_alpaca_2026-06-28` (PRIMARY), `MEGA_BUNDLE_MANIFEST` set explicitly.

| Dataset | Bars | First (UTC) | Last (UTC) |
|---|---|---|---|
| BTCUSD 1h | 48,077 | 2021-01-01 06:00 | 2026-06-28 00:00 |
| BTCUSD 4h | 12,023 | 2021-01-01 04:00 | 2026-06-28 00:00 |
| ETHUSD 1h | 48,075 | 2021-01-01 06:00 | 2026-06-28 00:00 |
| ETHUSD 4h | 12,023 | 2021-01-01 04:00 | 2026-06-28 00:00 |

All ≥ MIN_BARS_REQUIRED (1500). NO_DATA: 0. Lockbox (last 25%) = **2025-02-12 → 2026-06-28**,
a sustained down market (BTC −37%, ETH −40%) — a favorable window for detecting genuine alpha.

## Strategy Family & Parameter Search Space

`GEN_DONCHIAN_BREAKOUT` — long-only breakout above prior N-bar high (`shift(1)`, no repaint,
confirmed bars) + ATR buffer; stop = rolling low. Grid **60** combos: `channel_len`
{10,20,40,80,150} × `atr_buf` {0, .10, .25, .50} × `stop_lookback` {5,10,20}. DSR trial count = 60.
Exit: `fixed_2R`, 96-bar holding cap. Costs: 8 bps round-trip + 2 bps/side slippage stress.
Engine: `mega_walk_forward.py` (read-only, `faz3b-exit-mode-v1`), untouched.

## Runtime & Workers

Smoke: 1 cell / 2 workers / 2.8 s (scratchpad, JSON write proven — Gate 3.2). Full run:
4 jobs / 4 workers / **5.0 s**, thread-pinned. In-day scenario; no supervisor, no idle-awake.

## Walk-Forward / OOS Method & Statistical Corrections

The engine was configured for 3 rolling folds (60/20), but the disjoint-OOS geometry yields
**2 feasible non-overlapping folds** per dataset (`summary.n_folds=2`); the third configured fold
cannot fit before the 25% terminal lockbox and is not emitted. MIN_TRADES_FOR_PASS 30.
Bootstrap 2000 resamples (+ 50k hi-res pass — 0 PASS candidates to refine) → BH-FDR q=0.10 over
m=3 testable lockboxes → Bailey-LdP DSR (trials = 60). CPCV (6 groups, 2 test, 1% embargo) ran
for the record: **0 eligible candidates** (nothing PASS/STRONG_PASS). PBO: N/A (no CPCV splits).
Multi-window Q1–Q4 + parameter neighborhood: **0 candidates** (tool consumes PASS set only).

## Strategy vs Buy-and-Hold (identical lockbox slice, ALL cells — `buyhold_all_cells.json`)

Benchmark convention is the engine's canonical first lockbox-bar open to final lockbox-bar close,
copied from each result's `summary.buy_hold_lockbox`.

| Cell | Class | Strategy % | B&H % | Excess α % | Trades | PF | MaxDD % | Folds+ | Boot p | DSR |
|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSD 1h | FAIL | −16.80 | −37.01 | +20.20 | 36 | 0.70 | −17.0 | 1/2 | 0.878 | 0.00 |
| BTCUSD 4h | FAIL | −17.84 | −37.41 | +19.57 | 31 | 0.80 | −29.9 | 1/2 | 0.530 | 0.0001 |
| ETHUSD 1h | FAIL | −22.44 | −39.25 | +16.81 | 126 | 0.95 | −35.7 | 1/2 | 0.509 | 0.00 |
| ETHUSD 4h | INSUFFICIENT_TRADES | +30.79 | −39.97 | +70.76 | **9** | 2.13 | −19.7 | 2/2 | n/a | 0.24 |

Returns are compound (engine). "Excess α > 0" here means *lost less than holding* — absolute
returns are negative in 3/4 cells. Long-only strategy; no short leg exists to break down.

## True Alpha Candidates / Benchmark Beaters / Beta Disguised as Alpha

**None.** The only cell that made money while the asset fell (ETHUSD 4h, channel_len 150) rests on
9 trades — a small-sample lottery ticket (cf. lessons G2 2026-07-03: high-DSR/low-trade cells are
noise, and this one isn't even high-DSR at 0.24). Not classifiable as TRUE_ALPHA_CANDIDATE.

## Rejected / Insufficient Summary

- REJECTED: BTCUSD 1h, BTCUSD 4h, ETHUSD 1h (fail Benchmark-absolute, Risk, Statistical gates).
- INSUFFICIENT_TRADES: ETHUSD 4h (9 lockbox trades < 30).
- NO_DATA: 0. Configurations tested: 240 (60 grid × 4 cells); skipped: 0.

## Antigravity Error Checks

Compound returns ✓ · B&H comparison on every cell ✓ · data verified on disk ✓ · rolling WF, not
single split ✓ · trade-count guardrail enforced ✓ · BH-FDR + DSR multiplicity ✓ · commission +
slippage included ✓ · no-repaint (`shift(1)`) ✓ · regime noted (down-market lockbox) ✓ ·
long/short: long-only by design ✓ · no single-window claim made ✓ · summary-first report ✓.

## Promotion Recommendation

**REJECTED** (3 cells) / **INSUFFICIENT_TRADES** (1 cell). Overall: **NULL — nothing promotable,
nothing to forward-paper.** Barış's standing DSR-fail+CPCV-robust → FORWARD_PAPER mapping is NOT
triggered: no cell is WF-PASS and CPCV evaluated zero candidates. Export target (Crypto Paper
Bridge strategy format, `IBKR_PAPER_BRIDGE/docs/01_ARCHITECTURE.md` §6.2): **NOT READY** — no
export performed, bridge untouched.

## MTC_v2 Next Actions

None from this run. The result reinforces the 2026-07-03 pivot: methodology (exit knob, trade
floor, single-asset-class families, micro-price exclusion) over more strategy×asset scans. If a
crypto Donchian idea is ever revisited, it needs a new pre-registered design (e.g. longer-history
crypto source + multi-symbol family + swept exits under Faz 3b) — not a re-run of this grid.

## Reproducibility

```powershell
$env:PYTHONUTF8='1'; $env:OMP_NUM_THREADS='1'; $env:MKL_NUM_THREADS='1'
$env:OPENBLAS_NUM_THREADS='1'; $env:NUMEXPR_NUM_THREADS='1'
$env:MEGA_BUNDLE_MANIFEST='<MCC>\03_QUANTLENS\data\native_multiasset_alpaca_2026-06-28\manifests\dataset_manifest.json'
$env:MEGA_OUTPUT_DIR='<MCC>\03_QUANTLENS\research\donchian_crypto_ladder_2026-07-13'
$env:MEGA_WORKERS='4'
python mega_walk_forward.py --strategy GEN_DONCHIAN_BREAKOUT --symbol BTCUSD --symbol ETHUSD --tf 1h --tf 4h
python finalize_bootstrap_bh.py ; python multiwindow_oos.py ; python alpha_vs_buyhold.py
python cpcv_validator.py --input <run_dir>\MEGA_walk_forward_results.json --out-dir <run_dir>\cpcv
```
Deterministic engine (md5 seed) — re-running reproduces these numbers byte-identically (A19).

## Artifact Index

Run dir `03_QUANTLENS/research/donchian_crypto_ladder_2026-07-13/`:
- `MEGA_walk_forward_results.json` + `MEGA_walk_forward_report.md` — full WF+DSR+BH-FDR results
- `buyhold_all_cells.json` — B&H vs strategy for ALL 4 cells (incl. non-PASS)
- `multiwindow_summary.json` + `MULTIWINDOW_OOS_REPORT.md` — 0 candidates (record)
- `alpha_summary.json` — 0 PASS (record)
- `cpcv/cpcv_results.json` + `cpcv/CPCV_VALIDATION_REPORT.md` — 0 eligible candidates (record)

Registries: `05_REGISTRY/RESEARCH_RUN_REGISTRY.json` (run) +
`05_REGISTRY/VARIANT_LOG_REGISTRY.json` (variant `GEN_DONCHIAN_BREAKOUT_CRYPTO_1H4H`).
This report: `11_TRIAGE/DONCHIAN_CRYPTO_LADDER_VERDICT_2026-07-13.md`.
