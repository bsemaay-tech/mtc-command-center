# Ambiguity Register

| ambiguity_id | topic | status | handling |
|---|---|---|---|
| AMB-001 | "Steadily holding above/below VWAP" exact threshold | inferred | Uses ratio of closes above/below VWAP over a lookback. |
| AMB-002 | Capitulation definition | inferred | Uses volume spike + ATR/range expansion + distance from VWAP. |
| AMB-003 | Catalyst/news quality | blocked | Not modeled. User must visually select catalyst/in-play charts. |
| AMB-004 | A/B/C setup risk tiers | blocked | Contract records concept; code uses fixed visual risk only. |
| AMB-005 | Range-bound/no-man's-land | inferred | Uses Bollinger width and recent range compression proxy. |
| AMB-006 | Exact timeframe | known/inferred | Source is intraday; first review uses 5m, 2m allowed. |
| AMB-007 | Short side | inferred | Symmetric visual proxy only; do not treat as source-complete. |
