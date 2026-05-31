# AMBIGUITY_REGISTER — Kell Wedge Pop

| ID | Ambiguity | Source quote / origin | Safe default | Dangerous default |
|---|---|---|---|---|
| A1 | "Tight mini base" threshold | Intake §4 | range/close vs 30-bar median ratio (0.7) | Fixed 8% range cap, no context |
| A2 | "Reversal extension" magnitude | Intake §3 | 1.5×ATR or zscore <-1.5 from EMA20 | None / no flush check |
| A3 | "Higher-low" detection | Intake §3 | left2/right2 confirmed pivot above flush low | Skip (treat any uptrend) |
| A4 | "Leader" / "in-play theme" | Intake §10 | RS-rank vs SPY top-decile + sector RS | Skip universe filter entirely |
| A5 | EMA10 vs EMA20 trail switch | Intake §11 | After 3 successful EMA20 holds switch | Always EMA10 or always EMA20 |
| A6 | Blowoff exit threshold | Intake §8 | Placeholder close > EMA10×1.2 (must be researched) | None; ride forever |
| A7 | Crypto adaptation timeframe | Intake §9 | 1D + 4h | 1D only with no intraday |
| A8 | Position size table | Intake §11 | Risk-based (0.5–1%) for research | Direct copy 30–35% per name |

These ambiguities mean any "fair" Codex retest must hold contract preconditions A1–A4 invariant and only sweep parameters A5–A8.
