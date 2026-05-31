# Python Experiment Plan

## Experiment scope

## Candidate rules to prototype

## Required OHLCV inputs

## Timeframe

## Symbols

BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT ve mevcut data bundle'da uygun olan semboller.

## Commission/slippage assumptions

## Walk-forward plan

Train, validation ve OOS/test splitleri açık yazılmalıdır.

## Baseline comparison

## Pass/fail criteria

Net profit tek başına yeterli değildir; trade count, drawdown, PF, OOS ve hassasiyet birlikte değerlendirilir.

## Expected output files

```text
05_BACKTEST_RESULTS\<CandidateID>\
├─ backtest_config.yaml
├─ symbol_results.csv
├─ walk_forward_results.csv
├─ robustness_summary.md
├─ pass_fail_decision.md
└─ next_action.md
```

## Runtime limits
