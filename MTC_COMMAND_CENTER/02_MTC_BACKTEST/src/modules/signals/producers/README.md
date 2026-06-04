# Producer Adapter Contract

Manual producer adapters for MTC-Engine Validation live here.

Each adapter must:
- subclass `SignalPlugin`
- implement `generate(df) -> (raw_long, raw_short)`
- return boolean Series aligned to `df.index`
- emit raw entry signals only
- avoid filters, guards, SL, TP, trailing, sizing, and trade lifecycle decisions
- avoid lookahead and repaint behavior

Standalone Pine producer adapters belong under
`MTC_COMMAND_CENTER/01_MTC_PROJECT/parity_oracles/feature_adapters/pinets/`.
They are for raw-signal parity only and are not `MTC_V2.pine` integration.
