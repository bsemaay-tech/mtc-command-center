# Implementation Notes — QL_ALPHA_LTC_RSI_OVERSOLD_1H

## Files that MAY be changed in a later implementation task
- New REVIEW_ONLY / SANDBOX_ONLY files inside this candidate folder.
- A clearly-marked sandbox Pine script (only after the candidate is un-deferred).

## Files that MUST NOT be changed now
- `01_PINE/MTC_V2.pine` (production) — do not touch.
- Production alerts / webhook / order automation — none to be added.
- `tools/mega_walk_forward.py` + overnight result artifacts — read-only source of truth.

## Integration risks
- **Thin edge (PF 1.23, expectancy 0.107R):** very sensitive to commission/slippage; small cost increases can erase it.
- **No trend filter:** mean-reversion buying dips can catch falling knives in sustained downtrends (Q3 window was −26.4%).
- **Fold inconsistency (1/3):** regime-dependent; not parity-grade yet → parity deferred.
- **Statistical:** fails BH-FDR/DSR — candidate only.

## MTC_v2 producer/filter/exit/risk separation
- **Producer:** RSI(5) oversold→recovery long entry.
- **Filter:** none today; a trend/regime filter is a likely future improvement but must be tested separately (do not silently add — it breaks parity with the recorded result).
- **Exit:** 2R target + 5-bar-low stop + max-hold → MTC_v2 exit modules.
- **Risk:** risk = entry−stop; sizing defined at integration; keep small given thin edge.

## Exit-first compatibility
- Exit is explicit/deterministic → exit-first compatible. Given the thin edge, exit quality dominates outcome.

## Token-efficiency notes
- Metrics by path; no duplicated raw tables. Full data: `05_BACKTEST_RESULTS/MEGA_walk_forward_results.json`.

## Missing information
- Original "RSI Oversold" video exact rules → `NEEDS_SOURCE_CONFIRMATION` (RSI(5)/35/45 is the grid's best, not a confirmed source rule).
- Whether the source intends a trend filter → unknown; engine uses none.
- No forward (post-2026-04-27) data yet.
