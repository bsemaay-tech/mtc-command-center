# Deterministic Spec — Anthony Layered Leadership Swing System

> Source: YouTube `_QewlGLBaeA` ("Trading Millions: How I Finally Became a
> Profitable Swing Trader"). Re-triaged 2026-06-04 from `11_TRIAGE` cluster
> Stg088-094 (7 candidate angles = sub-setups of ONE system; shared transcript).
> **Discretionary swing system** — this captures the systematizable skeleton.

## Core idea: layered margin of safety (stack edges)
A trade should pass as many layers as possible; more layers = bigger size/conviction.

1. **Relative strength (stock)** — only trade stocks materially stronger than the
   market/peers (leaders that keep reappearing in scans).
2. **Theme / sector overlay** — the leader must sit in a hot sector/theme (rotation
   awareness; can also express via 3x leveraged sector ETFs). "The more you focus on
   theme/sector, the less the exact pattern matters."
3. **Market environment / timing** — cycle stage gates exposure (press early-cycle,
   reduce in chop/topping).
4. **Pattern / entry tactic** — chosen by cycle stage (see setups).

## Sub-setups (the 7 angles)
- **EP_EARNINGS_THEME_BREAKOUT** — episodic pivot: earnings/news/theme catalyst gap
  out of a base; buy the breakout. Strongest early in a cycle (goes straight, may not
  retest entry).
- **OUTLIER_LEADER_BREAKOUT** — trade the biggest movers / true market leaders
  breaking out of bases.
- **BREAKOUT_PULLBACK_RS** — for established names: enter on the pullback after a
  base breakout (later-cycle tactic), in RS leaders.
- **UNDERCUT_RECLAIM_LEADER** — shakeout reversal: price undercuts a base low then
  reclaims it → entry (weak hands flushed).
- **THEME_LEADERSHIP_ENGINE** — selection layer: rank sectors/themes, pick the
  leading stock within the leading theme.
- **BACKWATCH_BREAKOUT_HEALTH_ENGINE** — daily routine: collate biggest movers into a
  "backwatch" list, Mon-Fri template; use breadth of breakouts as a market-health
  gauge.
- **CYCLE_AWARE_EXPOSURE_CONTROL** — money management: progressive exposure scaled to
  cycle stage and how breakouts are behaving (health engine). Reduce/flatten in chop.

## Entry / risk / exit (common skeleton)
- **Entry:** breakout from base / EP gap / undercut-reclaim, in an RS leader inside a
  strong theme, when market environment is favorable.
- **Extension check:** measure price vs **low-of-day** before entry ("am I too
  extended → only a tiny position?").
- **Stop:** initial stop at **low of day** (Kamagi-simple), then **trail**.
- **Exit:** trail under rising MAs / structure; sell into climax/extension; cut
  laggards. Asymmetric R:R, comfortable with ~30% win rate if winners are large.
- **Sizing:** risk-first; progressive exposure by cycle stage (CYCLE_AWARE module).

## Reusable components for MTC
- RELATIVE_STRENGTH ranking filter, THEME/sector leadership filter (new), EP/gap
  detector, base-breakout entry, undercut-reclaim entry, low-of-day stop + trail,
  cycle-aware exposure controller (money management).

## Risks for backtesting
- Heavy discretion in theme/cycle reading; market-environment gating is subjective.
- Lookahead risk in "leader/theme" selection (must rank on closed data only).
- Survivorship: leaders are obvious in hindsight.

## Disposition
CANDIDATE (system, partial/discretionary). Not prototyped, not promoted, research-only.
