# Reclassification decisions — 2026-05-30 — REVIEW_HUMAN 18 candidates

Per-candidate verdict after I read the sampled context (intro + threshold/enumeration neighborhoods + conclusion). Final tally:

| verdict | count |
|---|---|
| KEEP_REJECTED | 9 |
| LIKELY_MISCLASSIFIED | 7 |
| SPLIT_RECOMMENDED | 1 |
| REVIEW_HUMAN (still ambiguous) | 1 |

---

## KEEP_REJECTED (9) — rejection looks correct

These are market-wizard interviews / wisdom content / meta-discussions. Specific moving-average references appear in passing but the videos don't deliver codifiable entry/exit rules.

| # | candidate_id | title | why |
|---|---|---|---|
| 1 | `QLR_kTqKRi-j9kM` | The 5 Essential Sell Rules — Linda Bradford Raschke | Title promises rules; content is about trade-management philosophy, scalability, holding times. Single MA mention is conceptual (McClellan oscillator discussion), not a tradeable rule. Conclusion is about taking walks with friends. |
| 2 | `QLR_NGyE4YIgGpU` | 2,115% Return — Tito Adhikary (Harvard scientist) | Mindset/journey interview. Lost $33k, "revenge trading", "you are your worst enemy". Single 10-day SMA mention in IPO example. Closes with friendship/smiling. |
| 8 | `QLR_2f5VfmlU90U` | The Mind of a Trader — Charles Harris | Pure trading psychology. "Common sense, discipline, hard work." "Nothing good happens below 21-day MA" is a principle, not a rule. |
| 9 | `QLR_6tnREqUJ1WY` | Trading Backtests Are Misleading — Lance Breitstein | Meta-content about *why* backtests mislead. The "21-period MA cross" example is given to demonstrate a backtest pitfall, not as a strategy. |
| 10 | `QLR_a4uJ3rHhbfA` | Art of Position Sizing — Anish Sikri | Topic is position sizing as a meta-skill. The Market School "21-day MA throttle" is briefly noted as someone else's mechanic he doesn't fully use. |
| 11 | `QLR_jLioqyVlRkE` | $200M Hedge Fund — Jim Roppel | Career-journey interview. "50 SMA is your guard rail" is a principle. Substantial content (34k words) but not a codified system. |
| 15 | `QLR_oPeTkxTnooA` | 259% Risk Management Strategy — Deepak Uppal | Risk-management philosophy: cut losses, concentration, "always use stops". 21 EMA stop only as a passing example. |
| 17 | `QLR_ZK5cnVQ2V3Q` | The Market Wizard Trading System — David Ryan | Career interview with William O'Neill's protégé. Conclusion is "stay optimistic, work hard". 21-day MA mention in passing. |
| 18 | `QLR_SMWMraeRDXs` | ULTIMATE Risk Management — Tom Basso | Many indicators discussed (RSI/BB/Stoch/EMA/ATR) but Tom's conclusion is *explicitly* "they all give roughly the same stats, pointless to look for a better buy/sell engine — focus on risk management". Not a strategy. |

---

## LIKELY_MISCLASSIFIED (7) — testable strategy inside, rejection looks wrong

These deserve to be moved out of REJECTED. Each one names a specific, well-defined approach with concrete rules in the transcript.

| # | candidate_id | title | what is testable |
|---|---|---|---|
| 3 | `QLR_Tm0dkf8_giA` | VCP Breakouts +50% — Richard Moglen | Volatility Contraction Pattern is a well-known pattern with crisp rules (successive contractions with declining volume, breakout entry, 21 EMA support). Short focused tutorial. blocked='manual visual review only' should be challenged — VCP is codifiable. |
| 4 | `QLR_UmLa9FAlMgw` | AVWAP Secrets and Setups — Brian Shannon | About the AVWAP indicator. Title says "setups" (plural). 5 indicators referenced. Concrete pullback rule (5-day MA touching 50-day or 21 EMA = setup). Author wrote a book on it. |
| 5 | `QLR_Lot25-2fb-4` | 433% Poker Player — Christian Qwek | Names two concrete strategies: (a) *Episodic pivots* — buy at opening range high, stop at low of day; (b) 10-day MA trailing exit — close above hold / close below sell. Very testable. |
| 7 | `QLR_M_tD6X0CSOI` | The Perfect VCP — Mark Minervini | Mark Minervini's famous VCP method. 3 numeric thresholds. Explicit rules: 200-day + 50-day filter, breadth filter (% of stocks above 50/200), follow-through day, RS line at new highs. Industry-standard testable strategy. |
| 12 | `QLR_kao-hhaQnig` | Event-Driven Trading Setup — Andrew Connell | Specifically named "Event Driven Trading Setup". Concrete entry rule (near declining 50 SMA after waterfall + base + pop-through). Borderline — promote to LIKELY but recommend a careful read before promoting to a real candidate. |
| 13 | `QLR_lpjTNygfnzM` | 153% Simple Swing — Deepak Uppal | Explicit "non-negotiable rules" stated: price > 200-day MA AND > 50-day MA, 50 > 200 (Stage-2 filter), price > $75. Top-10 concentration approach. All testable. |
| 14 | `QLR_UD7gipBWnuY` | When To Take Profits — Market Wizards | Compiled sell rules from multiple wizards. 4 thresholds. Stan Weinstein: "trim on 50-day MA break". 20-week EMA rule. 10/20 period trailing once trade is working. Could be tested as a *sell-rule library* even if no single entry signal. |

---

## SPLIT_RECOMMENDED (1) — one video, multiple strategies

| # | candidate_id | title | proposed split |
|---|---|---|---|
| 6 | `QLR_NwgJQyoUAaI` | Pro Swing Trading Setups Ep 2 (webinar series) | 31k words, multi-week series, multiple named setups. Visible markers: "launchpad setup" is explicitly named. 4 distinct indicator families (EMA, MACD ×3, Bollinger, Fibonacci ×8). Suggested cases: (a) Launchpad setup, (b) MACD-based setups, (c) Bollinger pullback, (d) Fibonacci retracement. Needs a full read to extract each one cleanly. |

---

## Still REVIEW_HUMAN (1) — genuinely ambiguous

| # | candidate_id | title | ambiguity |
|---|---|---|---|
| 16 | `QLR_q43pkYBo1hU` | +259% Swing Trading Performance — Deepak Uppal | Same author as #13 (Likely-Misclassified) and #15 (Keep-Rejected). Title says "Strategy" but the threshold context shows snapback-on-indexes discussion ("50 SMA area as resistance"), and 5 ATR mentions hint at structured exits. **Recommendation**: read in tandem with #13 — if #13 captures the codable filter rules already, this one may be a duplicate-context interview and KEEP. If it contains a *different* setup, it's LIKELY_MISCLASSIFIED. Flag for the user to spot-check. |

---

## Suggested next steps (for me to do when you ask)

1. For the 7 LIKELY_MISCLASSIFIED rows, prepare per-candidate **promotion patch** spec: a draft `producer_spec.json` skeleton + concrete entry/exit rules extracted from the transcript. Doesn't auto-promote — produces a review packet so the user can approve before adding to the registry.
2. For the 1 SPLIT row, do a deep read of the full transcript and propose specific sub-cases with their own candidate IDs.
3. For row #16, do a side-by-side comparison of transcripts #13 / #15 / #16 to detect duplication.

All three would be deeper-read tasks (~5-10k tokens each). Tell me which subset to run when you're ready.
