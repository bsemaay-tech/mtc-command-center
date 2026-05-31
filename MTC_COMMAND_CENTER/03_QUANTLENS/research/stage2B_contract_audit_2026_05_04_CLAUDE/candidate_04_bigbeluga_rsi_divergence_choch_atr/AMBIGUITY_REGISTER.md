# AMBIGUITY_REGISTER — BigBeluga

| ID | Ambiguity | Safe default | Dangerous default |
|---|---|---|---|
| A1 | Pivot length | 10 (indicator default) | 5 (Codex's choice — halves structural window) |
| A2 | "RSI divergence" detection | Swing-pivot vs swing-pivot per Pine source | Rolling-N min/max comparison (Codex's choice — not divergence) |
| A3 | Is divergence a hard requirement or visual hint? | Hard requirement (safer) | Skip → just CHoCH |
| A4 | Trailing stop type | ATR×4 chandelier-style from highest since entry | Static ATR×4 from entry (Codex's effective choice) |
| A5 | Ladder TPs partial exit sizing | Equal thirds | Single full exit at last TP |
| A6 | Anti-whipsaw bar count between flips | 5–10 bars | 0 (allow back-to-back flips) |
| A7 | Long+short symmetric vs trend-filtered | Trend-filtered for crypto | Pure symmetric |
