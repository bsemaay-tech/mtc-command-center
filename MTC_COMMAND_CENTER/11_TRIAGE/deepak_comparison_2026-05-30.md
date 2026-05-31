# Deepak Uppal 3-transcript comparison — 2026-05-30

For the still-ambiguous `QLR_q43pkYBo1hU` (REVIEW_HUMAN #16) — is it a duplicate of `QLR_lpjTNygfnzM` (LIKELY_MISCLASSIFIED #6) or `QLR_oPeTkxTnooA` (KEEP_REJECTED #15)?

## Side-by-side

| | A: lpjTNygfnzM (153%) | B: oPeTkxTnooA (259% Risk) | C: q43pkYBo1hU (259% Perf) |
|---|---|---|---|
| **Title** | Simple Swing Strategies — Triple Digit | Risk Management Strategy — Consistent Returns | Swing Trading Performance Strategy |
| **Length** | 22k words / 1765 lines | 19k / 1621 | **34k / 2754 — longest** |
| **Year referenced** | 153% year | 259% year (says "2023: 29%, 2024: top contender") | 259% year |
| **Format** | Interview | Conference presentation with slides | Conference presentation (extended) |
| **Example trades / stocks** | Broadcom (chip theme), Nvidia, Netflix, SMCI, PLTR | NVDA, Tesla, Bitcoin gap, specific dollar stops ($789.73, $100.73, $20) | Meta, Netflix, Tesla, SMCI, snapback examples |
| **Primary topic** | **Filter rules** + top-10 concentration | **Stop-loss math / position sizing** | **Performance / process / mindset + intraday entry timing** |

## Content overlap analysis

### What's unique to A (lpjTNygfnzM, 153%)
- The "**non-negotiable** rule" framing — explicit filter set:
  - price > 200 MA AND > 50 MA
  - 50 MA > 200 MA (Stage 2)
  - stocks > $75
- Top-10 concentration claim ("65% of gains from 10 stocks")
- VIX-spike-and-close-low entry trigger
- 153% year — a **different** trading year than B/C

### What's unique to B (oPeTkxTnooA, 259% Risk)
- Per-trade position sizing math (1% portfolio risk → calculated stop distance → calculated share count)
- Comparison of 8% generic stop vs technical stop with concrete dollar examples
- Stop types taxonomy: 8% generic, technical, percentage, time-based, etc.
- Quote of Larry's "the rule" book — risk management framing
- 259% year (2023)

### What's unique to C (q43pkYBo1hU, 259% Perf)
- 8%-stop backtest on his own losing year — showed +50% instead of −15% if he had used 8% stop universally (his "aha moment")
- Snapback-on-indexes setup with 50 SMA as resistance/key level
- Intraday entry timing rules: "buy in morning if good setup; buy end-of-day for half-position if closing strong; full position next morning if continues"
- Use of margin/concentration in good market environments
- Same 259% year as B but different lens

## Verdict

**They are NOT duplicates** — three distinct talks by the same speaker at different events:
- A covers his **filter framework** (one year, different from B/C)
- B covers his **risk management math** (the 259% year, from a position-sizing angle)
- C covers his **full year's process** (same 259% year as B, but from a process/mindset/intraday-timing angle)

The overlap (stop loss, concentration, similar example stocks) is the standard frame of any "how I did this year" trading talk — the meat of each is different.

## Reclassification

| candidate | previous verdict | new verdict | reasoning |
|---|---|---|---|
| A: lpjTNygfnzM (153%) | LIKELY_MISCLASSIFIED | **LIKELY_MISCLASSIFIED** (unchanged) | Filter rules already promoted as `QL_DEEPAK_153_FILTER_1D` in packets #6 |
| B: oPeTkxTnooA (259% Risk) | KEEP_REJECTED | **PROMOTE as risk overlay** (was misclassified) | The position-sizing math is concrete and testable — should be a `QL_DEEPAK_RISK_OVERLAY_259` candidate, similar role to the Market Wizards sell-rule overlay (packet #7) |
| C: q43pkYBo1hU (259% Perf) | REVIEW_HUMAN | **REVIEW_HUMAN → LIKELY_MISCLASSIFIED** | Adds the intraday entry timing rules + snapback-at-50-SMA setup that A/B don't cover; promotable as `QL_DEEPAK_SNAPBACK_50SMA_INTRADAY` |

## Net effect on the overall triage

Previously:
- LIKELY_MISCLASSIFIED: 24 (includes A)
- KEEP_REJECTED: 23 (includes B)
- REVIEW_HUMAN: 18 (includes C)

After this comparison:
- LIKELY_MISCLASSIFIED: 25 (added C)
- KEEP_REJECTED: 22 (removed B → now overlay candidate)
- REVIEW_HUMAN: 17 (removed C)
- + 1 new overlay candidate (B as `QL_DEEPAK_RISK_OVERLAY_259`)

The Deepak corpus yields **3 distinct promotable candidates**:
1. Filter framework (A) — `QL_DEEPAK_153_FILTER_1D`
2. Position-sizing math overlay (B) — `QL_DEEPAK_RISK_OVERLAY_259`
3. Intraday timing + snapback setup (C) — `QL_DEEPAK_SNAPBACK_50SMA_INTRADAY`

All share `source` cluster but are different specs. Recommend treating them as a "Deepak Uppal corpus" — 3 candidates sharing common ancestry but each with its own testable rules.

## Next decisions for you

- Approve treating Deepak as a 3-candidate corpus (vs. de-duplicating to one)
- Approve promotion of B from KEEP_REJECTED to overlay-candidate (changes the overall tally)
- For the long term: consider whether the user-side workflow needs a **"speaker cluster"** field in the audit so multi-talk speakers (Deepak, Brian Shannon, Christian Flanders, Mark Minervini) are visible as related rather than just separate candidates
