# Split packet — 2026-05-30

## `QLR_NwgJQyoUAaI` — Pro Swing Trading Setups For Consistent Gains (Ultimate Trading Guide Ep 2)

**Source:** 31k-word multi-host webinar (Episode 2 of a 7-part series). Hosts: Ryan, Richard Moglen.
**Title:** "Pro Swing Trading Setups For Consistent Gains — Ultimate Trading Guide Ep 2"
**URL:** https://www.youtube.com/watch?v=NwgJQyoUAaI
**Heuristic flag:** SPLIT_RECOMMENDED (5 indicators + enumeration markers)

Grep over the full transcript surfaces **6 distinct setups/edges** that the hosts walk through in their own sections. Three of them are unique to this video and worth promoting as new candidates; three are cross-references to setups already in the audit.

---

## Identified setups

### 1. Launchpad setup (Ross / Ryan's specialty) **— PROMOTE**

> "So the launchpad setup Ross is huge on this one. ... it comes from studying a lot of charts"

- **What it is**: Tight base after a strong move up the right side, very low volatility in the contraction zone, RS line acting well, expansion-then-contraction-then-expansion pattern.
- **Entry signal**: Break out of the tight contraction zone with volume.
- **Stop**: Below the contraction (tight zone allows tight risk).
- **Why it's distinct**: Not the standard cup/handle or VCP — the hosts position it as Ross's own variant; the contraction comes after an "up the right side" move (not from a deep correction).
- **Recommended id**: `QL_LAUNCHPAD_PROSWING_1D`

### 2. HV edge — Highest Volume signals **— PROMOTE**

> "highest volume in a year and highest volume since last earnings ... highest volume ever ... highest volumes IPO ... all of those are configured in DPU already"

- **What it is**: A volume-based signal family using bar-by-bar volume rank: (a) highest volume bar ever in stock's history, (b) highest volume bar since last earnings, (c) highest volume bar of an IPO's history, (d) highest volume in past N days (typically 1 year).
- **Entry signal**: When the HV bar occurs on a setup bar (e.g., gap up on earnings, breakout from base), it confirms institutional accumulation.
- **Stop**: Low of HV bar.
- **Why it's distinct**: This is a quantifiable volume edge — not just "high volume", but RANK-based ("ever", "since last earnings", "since IPO"). Directly testable with rolling-window highest-volume conditions.
- **Recommended id**: `QL_HIGHEST_VOLUME_EDGE_PROSWING_1D`

### 3. Relative Strength edge — RS line / RS phase / RS days **— PROMOTE**

> "we did a recent webinar kind of completely about this ... relative strength, new high before price"
> "over 61% of days, that's what you're kind of looking for. We. See the 63%, if a stock is exhibiting relative strength"
> "RS zone. RS phase. ... in a relative strength phase on a 21 day basis"

- **What it is**: Three-part RS framework with quantified thresholds:
  - **RS line new highs before price** — the canonical signal
  - **RS phase**: 21-day basis, stock outperforms index (shaded zone in the screenshot)
  - **RS days**: Stock outperforms market on ≥61-63% of recent days
- **Entry signal**: When all 3 conditions present + price setup (HV / launchpad / etc.).
- **Why it's distinct**: The 21-day phase + 61-63% day count are crisp empirical thresholds backtest-able as a stand-alone filter; the hosts even say they have prebuilt scans for "relative strength 1, 3, 6, 9, and 12 month".
- **Recommended id**: `QL_RS_PHASE_DAYS_PROSWING_OVERLAY` (filter overlay, not standalone entry)

### 4. Cup and Handle / VCP **— CROSS-REFERENCE**

> "stocks that technically form cup and handles seem"
> "Miner venous built a whole system on Vcps, right? ... it's more vcp ss it's declining on below average volume"

- These are mentioned but not freshly specified — the hosts assume audience knowledge. Already covered by #4 (Minervini canonical VCP — `QLR_M_tD6X0CSOI`) and #1 (Richard's VCP tutorial — `QLR_Tm0dkf8_giA`) in the earlier promotion packet.
- **Action**: Don't create new candidate. Just mark this episode's VCP discussion as a cross-reference / alternate explanation of `QL_VCP_MINERVINI_1D`.

### 5. Stage Analysis (Weinstein 4-stage) **— CROSS-REFERENCE**

> "stocks have the stage 1, 2, 3, and four"

- Same situation — Stage 2 filter is part of the underlying methodology used by many candidates (notably `QL_DEEPAK_153_FILTER_1D` from packet #6, which explicitly codifies "50 MA > 200 MA"). Mentioned here but not re-derived.
- **Action**: Cross-reference, no new candidate.

### 6. Earnings catalyst breakouts **— BORDERLINE**

> "what is the earning surprise on this? What it has a company done that's causing this gap up?"
> "highest volume since last earnings"

- Discussed mostly in the context of HV edge (#2). The hosts treat the earnings gap as a *trigger event* for the HV / RS setups rather than a standalone setup.
- **Action**: Treat as a feature/condition inside `QL_HIGHEST_VOLUME_EDGE_PROSWING_1D` rather than a separate candidate.

---

## Proposed split summary

| sub-candidate | promote? | parent | notes |
|---|---|---|---|
| Launchpad setup | YES | QLR_NwgJQyoUAaI | new candidate, Ross's variant |
| Highest-Volume edge | YES | QLR_NwgJQyoUAaI | testable rank-based volume rule |
| RS phase/days overlay | YES | QLR_NwgJQyoUAaI | filter overlay with 61-63% day threshold |
| Cup and Handle / VCP | NO | — | cross-ref to `QL_VCP_MINERVINI_1D` |
| Stage analysis | NO | — | cross-ref to `QL_DEEPAK_153_FILTER_1D` |
| Earnings catalyst | NO | — | merged into Highest-Volume edge |

**Net result:** 1 parent video → 3 new candidate cases.

This is more than the Codex heuristic suggested (which found only 1 split candidate in the whole 67-transcript corpus) but less than a naive "1 indicator = 1 case" split would yield. The 3 are the ones with **distinct, codifiable rules** that the hosts walk through with their own language and quantified thresholds.

---

## Next decisions for you

- Approve / reject each of the 3 new candidate proposals (Launchpad / Highest-Volume / RS-overlay)
- Decide whether to do the same split exercise on **Episodes 1, 3, 4, 5, 6, 7** of the series if the rest of the transcripts are accessible — likely many more distinct setups across the series
- For RS-overlay: do you want this as a filter inside each strategy's spec, or as a separate measurable overlay candidate?
