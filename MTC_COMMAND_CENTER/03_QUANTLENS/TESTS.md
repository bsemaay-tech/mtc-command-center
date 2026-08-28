# QuantLens verification

- Execute all four canonical gates and buy-and-hold comparison; record commands and real output.
- Verify `MEGA_BUNDLE_MANIFEST`, symbol, timeframe, bars, asset class, timezone/session semantics,
  seeds, and output identity before interpreting numbers.
- Show D026 RED/GREEN for every new regression claim; do not recapture goldens to hide drift.
- Run strategy safety review for repaint/lookahead/data leakage and preserve Pine/parity behavior.
- Validate generated registries and confirm the run appears in Strategy Research Lab.
- For CPCV, `--max-candidates 0` means all PASS/STRONG_PASS candidates; a positive cap must be
  labelled smoke/sample. For PBO, use the bounded generation contract from D008.
- Long runs use supervisor heartbeat/events/status and watchdog; a stalled or unevaluable gate
  stops, never silently passes or becomes a generic strategy failure.
