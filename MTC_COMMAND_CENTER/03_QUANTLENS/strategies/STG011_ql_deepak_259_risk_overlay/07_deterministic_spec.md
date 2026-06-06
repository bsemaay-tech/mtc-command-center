# Deterministic Spec — Deepak Singhania 259% Risk Overlay (QL_DEEPAK_259_RISK_OVERLAY)

> Source: Deepak Singhania 259% return strategy intake. Promoted to parity candidate in prior system.
> No active producer_spec.json. Spec reconstructed from strategy name and Deepak's published method.

## Universe
- US equities (growth stocks), 1D bars.
- Overlay risk management system — not a standalone entry strategy.

## Concept
Deepak Singhania's risk overlay from his "259% in 1 year" method: a systematic position-sizing
and risk management framework applied on top of entry signals. Key rules define max position size,
account risk per trade, and scaling rules based on conviction.

## Risk overlay rules (reconstructed)
```
max_risk_per_trade = 1.0%   # of account equity per position
max_positions      = 8–10   # concurrent positions max
position_size      = max_risk_per_trade × account / (entry_price - stop_price)

# Scaling: initial entry smaller, add if confirmed
initial_size = position_size × 0.5   # start with half size
add_on_confirm = position_size × 0.5  # add full size on first 5% gain + volume
```

## Position-level stop discipline
```
initial_stop = entry × 0.92 to 0.95          # 5–8% from entry (growth stocks)
trail_stop   = MA(close, 21)                 # trail with 21-day MA
hard_exit    = close < MA(close, 50)         # always exit if 50-day MA breaks
```

## Exit discipline
```
scale_out = trim 30% at 25% gain            # reduce risk at target
full_exit = at stop, or MA50 break, or fundamental deterioration
```

## Use as risk overlay
Apply these rules on top of any producer entry signal:
```
final_size = calculate position_size using entry/stop and 1% account risk
apply trail + scale rules on existing positions
```

## Data requirements
- 1D OHLCV, minimum 50 bars
- Account equity tracking (external)

## Disposition
Overlay / risk management framework. Not an entry signal generator. Use to size and manage
positions entered from any producer strategy. Not approved for live trading.
