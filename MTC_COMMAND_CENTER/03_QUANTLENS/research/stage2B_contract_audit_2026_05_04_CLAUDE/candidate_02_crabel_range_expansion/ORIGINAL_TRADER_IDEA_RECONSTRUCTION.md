# ORIGINAL_TRADER_IDEA_RECONSTRUCTION — Crabel Range Expansion (canonical)

## Plain English
Crabel observed that low-volatility days (NR4/NR7 — narrowest range of the last 4 or 7 days) tend to be followed by a directional expansion **the next day**, and that the best entries are stop orders placed just outside today's open in the direction of that expansion. The signal is *intraday*: it triggers when price travels a small distance from the open, before the day has decided its direction.

## Decomposition
- **Core edge:** mean-reversion of volatility — low-vol clusters precede high-vol expansion. The first decisive move out of the open is more likely to follow through than fade.
- **Setup context:** prior day was NR4 or NR7 (or ID/NR4 = inside-day AND NR4). Some Crabel variants additionally require an opening gap inside prior day's range, or a 2-bar pattern (2BH/2BL).
- **Trigger:** at session open, place a buy-stop at `O + Stretch * mult` and a sell-stop at `O − Stretch * mult`. `Stretch = mean_10d(min(O−L, H−O))`. Multiplier typically 0.5–1.0.
- **Invalidation:** opposite stop hit (then optional reverse-and-go) OR end-of-session.
- **Exit:** end-of-day exit (Crabel's classical rule) OR previous-day high/low as target OR 1×Stretch profit target.
- **Risk:** stop-distance defines size; per-trade risk usually ≤1%.
- **Universe:** liquid futures (ES, NQ, ZB, CL) and large-cap US equities; also applied to FX. Crabel is **session-based**.
- **Discretionary judgement:** which pattern stack to require (NR7 vs NR4 vs ID/NR4); multiplier; whether to allow reversal entries.
- **Non-essential commentary:** Crabel's specific examples in book (1980s/90s data) are illustrative.

## What an honest mechanical proxy must include
A. Real **Stretch** calculation (10-day mean of min(O-L, H-O)), not previous range × constant.
B. Stop entries placed from **today's open**, not yesterday's close.
C. NR-pattern qualifier (NR4, NR7, or ID/NR4).
D. Session-based exit (EOD).
E. Tested on instruments with a real session open (futures, equities) — NOT 24/7 crypto where "open" is arbitrary.

## What proxy must NOT do
- Use `prior_close ± prior_range * mult` on daily bars and call it Crabel.
- Apply to 24/7 crypto without redefining "open" (usually 00:00 UTC, but then the strategy is no longer Crabel — it is a daily-anchored breakout).
- Skip the NR-pattern setup filter.
