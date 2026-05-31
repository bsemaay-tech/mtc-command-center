# Adapters

The adapter layer will define how MCC reads external systems without directly modifying them.

## Planned Adapters

- MTC engine adapter: read backtest summaries and engine metadata.
- PineTS adapter: read parity outputs and case summaries.
- TradingView export adapter: read user-provided export files.
- QuantLens adapter: read strategy intake and research artifacts.
- Pine Builder adapter: manage draft metadata and review state.
- LiveOps adapter: future dry-run signal sandbox only.

No adapter implementation exists in MVP-0. These folders document boundaries and future data contracts.
