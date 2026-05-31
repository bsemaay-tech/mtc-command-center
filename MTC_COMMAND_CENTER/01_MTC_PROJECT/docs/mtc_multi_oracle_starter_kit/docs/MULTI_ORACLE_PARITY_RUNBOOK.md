# MTC v2 Multi-Oracle Parity Runbook

## Purpose

This runbook defines how to use multiple tools to validate MTC v2 parity without trusting a single engine.

## Oracle roles

| Oracle | Role |
|---|---|
| TradingView export | Final external Pine reference |
| Existing Python engine | Main local optimization/backtest engine |
| PineTS | Indicator/signal oracle |
| PyneCore | Experimental independent strategy execution oracle |
| vectorbt | Fast signal-array / parameter-sweep oracle |
| backtesting.py | Optional small sanity-check runner |

## Parity levels

| Level | Meaning |
|---|---|
| L0 | Data parity |
| L1 | Indicator parity |
| L2 | Raw signal parity |
| L3 | Transformed signal parity |
| L4 | Entry decision parity |
| L5 | Trade execution parity |
| L6 | Equity/statistics parity |

## FAST_SUITE

Use after every code change.

- 3 small cases.
- PineTS: L0/L1/L2 only.
- Python engine: L0-L6 if fast enough.
- PyneCore: only if POC stable.
- Goal: catch obvious regressions in seconds/minutes.

## CORE_SUITE

Use before meaningful patch.

- 20 representative cases.
- Include long-only, short-only, flip, SL/TP, BE, trailing, time stop, filter block.
- Compare Python vs PineTS at L1/L2/L3.
- Compare Python vs PyneCore at L1-L6 when available.

## NIGHTLY_SUITE

Use overnight.

- 100+ cases.
- Include parameter sweeps.
- Include vectorbt signal-level approximations.
- Generate summary report.

## RELEASE_SUITE

Use before declaring parity-safe release.

- Includes TradingView export reference.
- Must include exact Pine settings.
- Must include strategy tester exported trades/stats.
- Any L5/L6 divergence must be explained before release.

## Standard command examples

```powershell
python tools/mtc_runtime_compat_scan.py --pine path\to\MASTER_TEMPLATE_CORE.pine --out-dir reports

python parity_oracles/compare/parity_compare.py `
  --baseline-dir path\to\baseline `
  --candidate-dir path\to\candidate `
  --level L2 `
  --out-md reports\case001_L2.md `
  --out-json reports\case001_L2.json
```

## Divergence diagnosis guide

| Divergence starts at | Likely area |
|---|---|
| L0 | Data source, timezone, missing bars, duplicate bars, warmup |
| L1 | Indicator seeding, RMA/ATR, HTF alignment, precision |
| L2 | Signal producer, conflict normalization |
| L3 | Confirmation/retest pipeline, persistent state |
| L4 | Entry gates, position manager, cooldown, max entries |
| L5 | Fill model, exit-first order, SL/TP/BE/trailing, partial exits |
| L6 | Commission, slippage, sizing, equity accounting |
