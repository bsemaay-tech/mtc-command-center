# Next Action

## Recommended Next Step
Write a deterministic prototype spec for the LE model bull flag setup before any code or backtest.

## Minimum Spec Items
- Required breakout level set.
- Previous day and pre-market level calculations.
- EMA/level retest selection rule.
- Retest distance threshold.
- Flag-quality threshold.
- Session time guard.
- Candle stop execution rule.
- HOD/LOD partial target without lookahead.
- EMA runner exit rule.

## Stop Condition
Do not promote to MTC_V2 or Pine until a research prototype shows useful behavior across multiple sessions and not only the cited lockout rally examples.
