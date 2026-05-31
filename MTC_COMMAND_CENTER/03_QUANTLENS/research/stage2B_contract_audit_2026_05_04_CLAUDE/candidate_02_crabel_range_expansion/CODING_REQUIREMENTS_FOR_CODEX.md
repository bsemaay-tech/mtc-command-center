# CODING_REQUIREMENTS_FOR_CODEX — Crabel Range Expansion

## Required prototype rewrite
1. Acquire intraday OHLC for futures/equities sessions (or simulate on liquid crypto with explicit "00:00 UTC = session open" labelling).
2. Compute `Stretch = mean_10(min(O−L, H−O))` per asset, per session.
3. Compute `NR_n` flags: `range_today == min(range over last n)` for n ∈ {4,7}; `ID_NR4 = inside_day(today) AND NR4(today)`.
4. At each session open, **conditional on prior day being NR{n}**:
   - place buy-stop at `O + Stretch * mult`,
   - place sell-stop at `O − Stretch * mult`.
5. Walk the intraday bars: first stop hit fills entry. Opposite stop is initial SL. Optional profit target.
6. Force exit at session close (or 23:59 UTC for crypto-adapted).

## Variants to grid
- Stretch multiplier: [0.4, 0.6, 0.8, 1.0]
- NR pattern: [NR4, NR7, ID_NR4, none(baseline)]
- Profit target: [none, 1×Stretch, prior-day H/L]
- Direction: [both, long_only, short_only, with EMA200_daily filter]

## Hard rules
- No look-ahead: Stretch and NR computed using only data ≤ end of prior session.
- "Open" must be exactly the first traded price of the regular session.
- Track per-trade pattern label (which NR pattern + multiplier).

## Forbidden short-cuts
- Do NOT compute trigger from prior close + prior range.
- Do NOT skip NR filter.
- Do NOT report crypto-daily results as "Crabel".

## Output
- Per-session log: NR-flag, Stretch, both stop levels, fill side, fill price, intraday SL hit, intraday TP hit, EOD exit.
- Compare vs baseline "no NR filter, same multiplier" to prove the NR filter contributes edge.
