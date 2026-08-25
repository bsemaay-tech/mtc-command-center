# MTC backtest application stage rules

This stage owns the Python MTC backtester, validation CLI, local data/configuration, and its tests.
It does not own QuantLens strategy-research runs; route those to `03_QUANTLENS`.

- Pine, parity, MTC strategy behavior, scoring thresholds, and trading semantics are protected.
  Require explicit owner approval for any behavioral change.
- Preserve the existing engine as the source; do not create a parallel engine or silently redirect
  the MTC-Engine Validation funnel.
- MTC-Engine Validation remains shortlist-only, uses `MTCRunner`, `light_risk.py`, manual producer
  adapters, and `python -m src.cli.mtc_engine_validate`; it is not live trading or controller
  integration.
- Data/provider/config changes must pin identity and avoid hidden defaults. Generated outputs stay
  out of source unless an evidence refresh explicitly includes them.
- Treat parity as sacred in QA. Any regression closure uses real RED/GREEN evidence and exact cases.
- Local-only non-economic code is normally T1; any broker/host/live/security surface escalates T0.
