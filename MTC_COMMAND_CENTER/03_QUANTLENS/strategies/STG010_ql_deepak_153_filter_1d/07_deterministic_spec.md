# Deterministic Spec — Deepak Singhania 1-5-3 Filter 1D (QL_DEEPAK_153_FILTER_1D)

> Source: Deepak Singhania 153% return strategy intake. Promoted to parity candidate in prior system.
> No active producer_spec.json. Spec reconstructed from strategy name and Deepak's published method.

## Universe
- US equities (growth stocks), 1D bars.
- Focus: stocks outperforming the market on relative strength.

## Concept
Deepak Singhania's "1-5-3 filter": a multi-timeframe momentum filter for selecting entry
timing into trending stocks. The numbers refer to periods used in a multi-timeframe momentum
or MA system (interpretation: 1-week momentum above 5-week above 3-month trend).

## Indicators (reconstructed)
```
momentum_1w  = close / close[5] - 1         # 1-week (5-day) momentum
momentum_5w  = close / close[25] - 1        # 5-week (25-day) momentum
momentum_3m  = close / close[63] - 1        # 3-month (63-day) momentum
rs_vs_spy    = close/close[63] vs SPY/SPY[63]  # relative strength vs benchmark
```

## Signal definition (filter-only, reconstructed)
```
# 1-5-3 alignment: short-term > medium-term > long-term momentum
momentum_aligned = (momentum_1w > 0)
                 AND (momentum_5w > 0)
                 AND (momentum_3m > 0)

rs_positive = rs_vs_spy > 1.0               # outperforming benchmark

filter_pass = momentum_aligned AND rs_positive
```

Used as a universe filter: only trade stocks that pass the 1-5-3 filter on the day of entry.

## Use as entry gate
Apply as a filter before any entry signal from a producer strategy:
```
final_entry = producer_signal AND filter_pass
```

## Data requirements
- 1D OHLCV, minimum 63 bars warmup (3-month momentum)
- Benchmark comparison (SPY or index) for RS calculation

## Known risks
- Momentum filters have inherent look-ahead if not applied on closed bars.
- Short-term momentum (1-week) can oscillate rapidly — adds noise.
- Market-relative RS requires benchmark feed.

## Disposition
Parity candidate. Use as a universe filter / entry gate rather than standalone entry signal.
Not approved for live trading.
