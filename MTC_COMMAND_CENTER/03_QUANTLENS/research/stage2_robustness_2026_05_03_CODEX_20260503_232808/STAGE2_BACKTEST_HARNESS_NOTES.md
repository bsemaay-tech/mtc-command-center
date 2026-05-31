# Stage-2 Backtest Harness Notes

No lookahead by construction: indicators use rolling/past values; entries use next bar open where applicable; same-bar ambiguity skipped or conservative stop-first exits. Failed assets are logged.
