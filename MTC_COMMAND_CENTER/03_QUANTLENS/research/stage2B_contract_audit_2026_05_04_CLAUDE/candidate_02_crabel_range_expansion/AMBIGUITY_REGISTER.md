# AMBIGUITY_REGISTER — Crabel Range Expansion

| ID | Ambiguity | Safe default | Dangerous default |
|---|---|---|---|
| A1 | Stretch period | 10 days (canonical) | Anything else without justification |
| A2 | Multiplier | 0.5–1.0 grid | <0.3 (overfits noise) or >1.5 (misses moves) |
| A3 | NR pattern | NR7 (most selective) | None |
| A4 | Allow reversal entries | Test both | Always reverse without filter |
| A5 | Profit target | Test {none, 1×Stretch, prior-day HL} | Aggressive multi-R targets unrelated to Stretch |
| A6 | "Session" definition for crypto | Explicit 00:00 UTC + relabel as adapted | Pretend daily bars = session |
| A7 | Position direction in trend | EMA200-filter optional gate | Force long-only or short-only without test |
