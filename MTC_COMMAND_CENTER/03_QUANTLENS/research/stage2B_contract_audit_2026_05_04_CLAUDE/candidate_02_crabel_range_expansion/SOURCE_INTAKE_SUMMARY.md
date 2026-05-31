# SOURCE_INTAKE_SUMMARY — Crabel Range Expansion

## Source files Codex pointed to
- `06_QUANTLENS_LAB/00_INBOX_REPORTS/3 Mayıs/2026-05-03_Ne3X-l6W4CQ_quantlens_process_strategy_intake.md` (Linda Raschke / TraderLion process video — Crabel mentioned only briefly as one example).

## What the *real* Crabel framework is (from Toby Crabel "Day Trading with Short-Term Price Patterns and Opening Range Breakout", 1990)
- Crabel is an **intraday opening range breakout** trader, NOT a daily previous-range breakout system.
- Core construct is the **Stretch**: average over last 10 days of `min(open−low, high−open)`.
- Trigger: place buy stop at `today's open + Stretch × multiplier` and sell stop at `today's open − Stretch × multiplier` (multiplier typically 0.5–1.0).
- Best setups stack additional patterns: NR4/NR7, ID/NR4, opening-gap context, 2BH/2BL.
- Time stop: end of session if both stops missed.

## What the Linda Raschke Ne3X intake actually says about Crabel
- Linda mentions Crabel in passing as one of several "process" examples for low-frequency edge.
- The intake does **not** define Crabel's stretch math, does not specify timeframe, and does not give an opening-range trigger.

## Intake-stated rule (Codex's quoted "audited rule")
- "Break prior close ± prior range × multiplier; next close / time exit proxy." — this is an LLM paraphrase, not Crabel's actual rule, and not even close to what Crabel published.

## Mismatch summary
- Codex sourced Crabel to a video that does not contain Crabel's mechanical rules.
- Codex's resulting Python implementation diverges materially from Crabel's actual published method.
