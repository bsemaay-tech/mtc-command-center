# DISCRETIONARY_ELEMENTS — Crabel Range Expansion

Crabel is one of the *least* discretionary classical strategies in this set — most rules are fully mechanical.

| Element | Mechanical? | Notes | Previous LLM choice |
|---|---|---|---|
| Stretch formula | Fully mechanical | mean(min(O−L,H−O),10) | WRONG (used prior-day range) |
| NR4 / NR7 detection | Fully mechanical | smallest range of last N | MISSING |
| Multiplier choice | Param sweep | 0.5–1.0 | Reasonable (0.9) but on wrong base |
| Reversal entry | Choice; mechanical | Test both | Default = both, OK |
| Profit target | Choice | None / 1×Stretch / PD-HL | Used reward = none + N/A; OK |
| News blackout | Mechanical with calendar | Easy if data available | Missing |
| Session definition | Mechanical for futures/equities; *requires explicit choice for crypto* | Adapt and re-label | Hidden: silently ran daily |

Producer / filter / process classification:
- **Producer candidate** — but only as intraday-session module.
- Cannot be honestly tested on current crypto-daily bundle.
