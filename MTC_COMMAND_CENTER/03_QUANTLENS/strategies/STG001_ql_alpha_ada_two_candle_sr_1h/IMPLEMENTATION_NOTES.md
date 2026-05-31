# Implementation Notes — QL_ALPHA_ADA_TWO_CANDLE_SR_1H

## Files that MAY be changed in a later implementation task
- New REVIEW_ONLY / SANDBOX_ONLY files inside this candidate folder (Python reference producer, Pine v6 review wrapper).
- A clearly-marked sandbox Pine script under an existing sandbox location.

## Files that MUST NOT be changed now
- `01_PINE/MTC_V2.pine` (production) — do not touch.
- Production alerts / webhook / order automation — none to be added.
- `tools/mega_walk_forward.py` + overnight result artifacts — read-only source of truth.

## Integration risks
- **Low sample (53 trades):** do not size or trust until the forward window grows the sample. Highest-priority risk for this candidate.
- **Rare signals:** 200-bar resistance lookback yields infrequent entries; forward validation may be slow.
- **Statistical caution:** fails BH-FDR/DSR — candidate, not edge.

## MTC_v2 producer/filter/exit/risk separation
- **Producer:** breakout-with-strong-close long entry.
- **Filter:** the 200-bar resistance break and `pos>=0.6` act as confirmation filters; keep them attached to the producer or expose as filter module.
- **Exit:** 2R target + 2-bar-low stop + max-hold → MTC_v2 exit modules.
- **Risk:** risk = entry−stop; define sizing at integration.

## Exit-first compatibility
- Exit (fixed 2R + stop + time) is explicit and deterministic → exit-first compatible.

## Token-efficiency notes
- Metrics referenced by path; no large tables duplicated. Full data: `05_BACKTEST_RESULTS/MEGA_walk_forward_results.json`.

## Missing information
- Original "Two-Candle SR" video exact rules → `NEEDS_SOURCE_CONFIRMATION`.
- Whether the original intends reversal vs breakout → engine uses breakout-with-strong-close; confirm against source before parity hardening.
- No forward (post-2026-04-27) data yet.
