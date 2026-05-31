# Experiment Plan

## Prototype Scope
Start with the core deterministic variant:

`daily RSI(7) 60/40 regime + 1h RSI(7) pullback cross + swing stop + 2R target`

## Deterministic Rules To Define
- RSI source: close unless specified otherwise.
- Daily RSI alignment on `1h` bars without future daily close leakage.
- Cross detection for `1h RSI` above `40` and below `60`.
- Pullback memory window after RSI enters oversold/overbought zone.
- Swing low/high stop definition using past-only bars.
- Maximum signal candle or maximum stop distance filter.
- Optional support/resistance confluence algorithm.
- Optional candle pattern confirmation definitions.
- Entry execution at signal candle close or next bar open.
- Fixed `2R` target handling.

## Suggested Pilot
- Start with event extraction only.
- Test long and short events separately.
- Use one liquid market/timeframe pair before broad comparison.
- Compare core RSI-only variant against RSI plus S/R confluence only after the core event extraction is stable.

## Explicit Non-Goals
- No broad RSI playbook test.
- No discretionary candle pattern interpretation.
- No Pine patch.
- No production runner change.
- No optimization before deterministic pilot.
