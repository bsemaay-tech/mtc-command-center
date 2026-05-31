# Promotion packets — 2026-05-30

Per-candidate rule extraction + draft `producer_spec.json` skeleton for the 7 LIKELY_MISCLASSIFIED rows from `reclassification_decisions_2026-05-30.md`. These are **proposals**, not promotions — each one needs your approval before becoming a real candidate spec. The QuantLens-lab `06_PROMOTED_TO_PARITY/` is git-ignored, so accepting a packet means dropping the spec into the lab and re-running audit + parity work separately.

Rule confidence levels: **HIGH** = quoted nearly verbatim from transcript; **MEDIUM** = clear in context but speaker hedges; **LOW** = inferred from examples.

---

## 1. `QLR_Tm0dkf8_giA` — VCP Breakouts (Richard Moglen, +50% in 20 Days)

**Source:** ~3k word focused tutorial. Self-contained, not an interview.
**Title:** "How to Trade Breakouts with The Volatility Contraction Pattern (VCP)"
**Why misclassified:** Audit marked `manual visual review only`. VCP is a deterministic pattern (Minervini's framework). The tutorial gives explicit entry/exit/stop rules.

### Rules
| Rule | Confidence | Source |
|---|---|---|
| Pattern: 2+ successive lower-amplitude contractions within a base, tightening left-to-right | HIGH | "carbon handle ... two contraction VCP, this is the pivot point right here" |
| Volume: declining volume on each contraction, surge on breakout | HIGH | "volume to dry up on the declines and increase on the rallies" |
| Entry: BUY at pivot-point breakout (prior resistance, often weekly/all-time high) | HIGH | "alerts right at the pivot point ... breakout" |
| Stop: Low of consolidation (loose) OR low of breakout day (tight) | HIGH | "stop loss basically at the low of this consolidation or even at the low of the day" |
| Hold confirmation: stays above 21 EMA along base low | MEDIUM | "I like how it held the 21 ema as well along the base low" |
| Manage: move stop to breakeven on +5-10% gain, then trail under 10-day SMA | HIGH | "move up stops to break even initially and even as the stock continues to work" |

### Suggested cases
- 1H + 1D — VCP base detection on multiple timeframes
- ~~5m~~ — intraday probably noisy; primary is daily

### Draft producer_spec skeleton
```json
{
  "candidate_id": "QL_VCP_BREAKOUT_RICHARD_1D",
  "source_url": "https://www.youtube.com/watch?v=Tm0dkf8_giA",
  "direction": "long_only",
  "filters": {
    "pattern": "VCP_2_PLUS_CONTRACTIONS",
    "min_contractions": 2,
    "each_contraction_lower_amplitude": true,
    "volume_dry_up_on_contraction": true
  },
  "entry": {"trigger": "PRICE_BREAKOUT_OVER_PIVOT_WITH_VOLUME_SURGE"},
  "stop": {"type": "LOW_OF_BREAKOUT_DAY", "alt": "LOW_OF_BASE"},
  "scale_out": {"to_breakeven_at_pct": 5, "trail_indicator": "SMA_10"},
  "fidelity_to_original_youtube_source": "DERIVED_TUTORIAL"
}
```

---

## 2. `QLR_UmLa9FAlMgw` — Brian Shannon AVWAP setups (CMT)

**Source:** 20k-word interview with the author of the AVWAP book.
**Title:** "The AVWAP Trading Indicator Secrets and Setups"
**Why misclassified:** Title says "setups" plural; transcript names ~4 concrete AVWAP setups with entry/stop rules. **Note:** strong split candidate too — could become 4 separate cases.

### Setups identified
| # | Setup | Entry | Stop |
|---|---|---|---|
| 2a | Daily VWAP gap reclaim | Stock gaps up, settles, reclaims daily VWAP from below | Below low of day |
| 2b | Multi-timeframe stage-2 emerging momentum | After 20MA > 50MA > 200MA structure forms, buy on first higher-low pullback | Below higher-low |
| 2c | Intraday opening range + AVWAP | Break of opening range, pullback to VWAP holds as support | Below the VWAP-touch swing-low |
| 2d | Anchored to earnings day | Anchor VWAP at earnings bar, buy pullbacks to AVWAP, scale out at extension | Below AVWAP swing-low |

Scale-out: 1/3 at breakout, 1/3 at next pivot, ride remainder with trailing stop under last swing-low.

### Recommended action
**Promote as one parent candidate with 4 sub-cases.** Brian's "5-day MA still declining but touching 50-day or 21 EMA" is a confluence rule that applies across all setups. The parent producer_spec defines the AVWAP anchor logic; each sub-spec defines entry/stop variant.

Draft parent spec only here; sub-spec drafts upon your approval.

---

## 3. `QLR_Lot25-2fb-4` — Christian Flanders (433%, Poker→Trader)

**Source:** 34k-word interview, 32 section headings, very content-rich.
**Title:** "433% Return in 1 Year — From Poker Player to Full Time Trader"
**Why misclassified:** Names multiple **fully specified** setups with explicit entry/stop wording. **Heavy split candidate.**

### Setups identified
| # | Setup | Entry | Stop | Confidence |
|---|---|---|---|---|
| 3a | **Episodic pivots** (his favorite) | News/earnings catalyst → massive premarket volume → BUY at first 5-min opening range high | LOW OF DAY | HIGH (verbatim) |
| 3b | VCP entries (Minervini-style) | Early entry on contractions OR breakout of standard pivot | Below pivot / base low | HIGH |
| 3c | Power plays | High-tight-flag continuation | Below flag low | MEDIUM (named only) |
| 3d | "Just use opening range + 5-6% stop" | Buy at open OR on 5-min opening range high | 5-6% below entry | HIGH |

### Trailing rule library (worth its own case)
Christian backtested his own trades with three trailing rules:
| Trail | Total R | Avg gain | Avg hold | P&L vs baseline |
|---|---|---|---|---|
| 10-day MA close | 290R | — | 16d | baseline |
| 20-day MA close | 590R | 24% | 34d | +145% |
| 50-day MA close | 600R | 27% | 50d | +170% |

→ **Tradeable insight**: 20-day MA trail outperforms 10-day for episodic pivots. This is empirically validated by his own data.

### Recommended action
Promote as **4 separate cases** sharing the same `source_url`:
1. `QL_EPISODIC_PIVOT_CHRISTIAN_5M` — opening range high entry, 5-min timeframe
2. `QL_TRAILING_RULE_20MA_CHRISTIAN_1D` — exit-rule overlay (20-day MA close)
3. `QL_VCP_EARLY_ENTRY_CHRISTIAN_1D` — early-contraction entry
4. `QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M` — fixed-stop variant (baseline test)

This is where the user's Task-4 ("split candidates") interest pays off.

---

## 4. `QLR_M_tD6X0CSOI` — The Perfect VCP (Mark Minervini himself)

**Source:** ~10k-word direct interview with Mark Minervini.
**Title:** "The Perfect VCP Trading Setup with Mark Minervini"
**Why misclassified:** Mark Minervini's VCP is the **industry-standard** version of the pattern. The other VCP candidate (Richard Moglen tutorial #1) is a derivative; this is the source.

### Rules
| Rule | Confidence |
|---|---|
| Coming off market lows: stocks first into new high ground are the leaders | HIGH |
| Confirmation: follow-through day in market | HIGH |
| RS line: making new highs **before** price | HIGH |
| Stage-2 only (Weinstein 4-stage): price above and 50MA above 200MA | HIGH |
| Breadth filter: track % of stocks above 50 and 200-day MAs as participation gauge | MEDIUM |
| Pattern: VCP with progressively tighter contractions | HIGH |
| Entry: at the pivot breakout from VCP base | HIGH |
| Position sizing: progressive exposure — start 5-10-15-20%, add as trades work | HIGH |
| Stop: below pivot | HIGH |

### Recommended action
Promote as `QL_VCP_MINERVINI_1D` — the **canonical** VCP candidate. The Richard Moglen tutorial (#1) becomes either a duplicate or a "Richard's interpretation" variant. Recommend keeping just Minervini as primary, marking Richard's tutorial as `DUPLICATE_OF_QL_VCP_MINERVINI_1D` in the audit.

---

## 5. `QLR_kao-hhaQnig` — Andrew Connell event-driven (103%)

**Source:** 19k-word interview.
**Title:** "The Simple Event Driven Trading Setup"
**Why misclassified:** Title names a setup; transcript has a concrete entry rule.

### Rules
| Rule | Confidence |
|---|---|
| Setup: Stage-4 stock has waterfall → likely cycle low → forms base → pops through declining 50 SMA | HIGH |
| Entry: Above prior day's high (above-the-day entry) **OR** breakout from monthly Volume Profile value area | HIGH |
| Stop: Below prior swing low | MEDIUM |
| Catalyst confirmation: News/earnings/guidance helps for trend reversal | MEDIUM |
| Variant for uptrend continuation: "for continuation it's got to be the go-to" — different exit timing | LOW |

**Honest assessment:** This is the weakest of the 7. The entry rule is concrete but the exit and trade management are not crisply specified in the sampled context. **Recommendation: REVIEW further before promoting** — a full transcript read could either solidify or weaken the case. Demote to "needs deeper read" rather than promote immediately.

---

## 6. `QLR_lpjTNygfnzM` — Deepak Uppal 153% Simple Swing

**Source:** 22k-word interview.
**Title:** "Simple Swing Trading Strategies for Achieving Triple Digit Returns"
**Why misclassified:** Speaker explicitly states "non-negotiable rules" — strongest extractable filter set in the entire 18-row review.

### Rules (quoted nearly verbatim)
| Rule | Confidence |
|---|---|
| **Non-negotiable**: always use stop losses | HIGH (his words) |
| Price > 200-day MA | HIGH |
| Price > 50-day MA | HIGH |
| 50-day MA > 200-day MA (Stage 2 confirmation) | HIGH |
| Stocks > $75 only (~90% of below-$75 filtered out) | HIGH |
| Concentration: top-10 names produce ~65% of yearly gains | HIGH (his empirical claim) |
| VIX caution: don't enter on VIX spike-and-close-high; wait for spike-and-close-low | MEDIUM |

### Recommended action
Promote as `QL_DEEPAK_153_FILTER_1D` — **filter overlay, not a standalone entry rule.** Deepak doesn't specify an entry trigger beyond "stocks setting up in uptrend"; the value is the filter set. This should ride on top of a separate entry methodology (e.g., a VCP or O'Neil follow-through entry).

Pair with #4 (Minervini VCP) or #3a (Christian episodic pivot) as the entry trigger.

---

## 7. `QLR_UD7gipBWnuY` — When To Take Profits — Market Wizards compilation

**Source:** 11k-word multi-wizard compilation video.
**Title:** "When To Take Trading Profits - Market Wizards Share Their Sell Rules"
**Why misclassified:** Compiles concrete sell rules from multiple wizards. Even without one entry signal, the sell rules can become a **modular exit-rule library**.

### Sell rules library
| # | Rule | Source | Confidence |
|---|---|---|---|
| 7a | Trim on first close below 50-day MA (modern: full exit on clean close below) | Stan Weinstein | HIGH |
| 7b | 8% extension from 50-day MA = ~90th percentile → consider trimming | Stan Weinstein | HIGH |
| 7c | Won't trade stocks below 20-week EMA (~100-day MA) | Speaker B | HIGH |
| 7d | Ride 10 or 20-period MA after trade works; want 3+ touches to confirm respect | Speaker B | HIGH |
| 7e | Monthly loss cap: 5% normally; cascading reduction (5/3/2/1) after consecutive losing months | Speaker B | HIGH |

### Recommended action
Promote as `QL_SELL_RULES_MARKET_WIZARDS_OVERLAY` — not a strategy, an **exit-rule module library** that any long-side strategy can adopt. Particularly 7a (50-MA exit), 7c (20-week EMA filter), and 7e (monthly DD cap) are immediately codifiable.

---

## Summary action table

| # | candidate_id | recommended action | est. complexity |
|---|---|---|---|
| 1 | QLR_Tm0dkf8_giA | Promote as `QL_VCP_BREAKOUT_RICHARD_1D` OR mark duplicate-of #4 | low |
| 2 | QLR_UmLa9FAlMgw | Promote parent `QL_AVWAP_BRIAN_SHANNON_PARENT` + 4 sub-cases | high |
| 3 | QLR_Lot25-2fb-4 | Split into 4 cases (episodic pivot, trail-rule, VCP early, fixed-stop) | high |
| 4 | QLR_M_tD6X0CSOI | Promote as canonical `QL_VCP_MINERVINI_1D` | medium |
| 5 | QLR_kao-hhaQnig | REVIEW further — entry concrete, exit underspecified | low |
| 6 | QLR_lpjTNygfnzM | Promote as `QL_DEEPAK_153_FILTER_1D` (filter overlay) | low |
| 7 | QLR_UD7gipBWnuY | Promote as `QL_SELL_RULES_MARKET_WIZARDS_OVERLAY` (exit library) | medium |

**Next decisions for you:**
- Approve / reject each row's recommended action
- For SPLIT candidates (#2, #3), confirm sub-case names before I generate per-sub-case spec drafts
- For #1 vs #4 duplicate question: keep one, mark the other
- For #5: do you want me to do a deeper transcript read, or leave it for your manual review?
