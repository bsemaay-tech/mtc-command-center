# Deterministic Spec — Ariel Market-Timed Momentum Swing

> Source: YouTube `Nq-p7Bu1YT0` (Ariel, super-performance swing trader).
> Re-triaged 2026-06-04 from `11_TRIAGE` Stg103. Same momentum school as STG048
> (Anthony) / STG049 — cross-check before prototyping. Discretionary.

## Core idea
Trade relative-strength leaders in leading groups, **but gate it by market state**:
- Market pushing higher → trade RS leaders long (breakout buy / earnings gap up /
  flatbed breakout).
- Market pulling back / weak → **don't trade RS, just track it**; focus only on the
  strongest names; be willing to **short on distribution**.

## Entry tactics (the "setups")
- **Breakout buy** — leader breaks out of a base.
- **Earnings gap up** — buy strong reaction to earnings.
- **Flatbed breakout** — long, tight, flat base breaking out.
- **Short side** — when the market starts distributing, short the weakest names.

## Selection
- "Don't trade your favorite stocks — make the stocks in leading groups your
  favorites." Rank by RS vs market; trade leaders of leading sectors.

## Risk / exit
- Risk-first; stop below the breakout/base low; trail with the trend; cut on failure.
- Reduce/avoid longs when market breadth deteriorates (market-state gate).

## Reusable components for MTC
- Market-state gate (trade-RS on/off), RS leader ranking, flatbed-base breakout
  detector, earnings-gap entry, distribution-based short trigger.

## Lessons (keep)
- The setup is timeless; the *market environment* decides whether it works now.
- In a down market, tracking RS beats trading it — wait for the turn.
- Leaders rotate by group; follow the leading groups, not personal favorites.

## Risks for backtesting
- Market-state read is discretionary → encode an objective breadth/index filter.
- Heavy overlap with other momentum systems → guard against redundant variants.

## Disposition
CANDIDATE (methodology). Not prototyped, not promoted, research-only.
