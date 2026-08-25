# MTC backtest inputs

- Exact CLI/profile/config, data source and version, symbols/timeframes, seed, and expected artifact.
- Relevant module contract and the smallest fixture/case set.
- For MTC-Engine Validation: `src/config/profiles/light_risk.py`, selected manual producer adapters,
  `MTCRunner`, and its current CLI tests.
- Root `DECISIONS.md`, especially D003; open full decision text only when needed.
- Any Pine/TradingView oracle must include version, export date, tolerance, and comparability status.

Do not use the QuantLens hard-coded legacy data default as an implicit source for this stage.
