# Implementation Notes — QL_ALPHA_LINK_8EMA_1H

## Files that MAY be changed in a later implementation task
- New files **inside this candidate folder** (REVIEW_ONLY / SANDBOX_ONLY): a standalone Python reference producer and a Pine v6 REVIEW wrapper.
- A sandbox Pine script under an existing sandbox/strategy_sandboxes location (clearly marked REVIEW_ONLY).

## Files that MUST NOT be changed now
- `01_PINE/MTC_V2.pine` (production Pine) — do not touch.
- Production alerts / webhook / order automation — none to be added.
- `tools/mega_walk_forward.py` and overnight result artifacts — treat as read-only source of truth.

## Integration risks
- **Producer/exit coupling:** the `8EMA_EXIT_TRAIL` family bundles entry (8EMA pullback) with an exit (EMA8 trailing). MTC_v2 requires producer/filter/exit/risk separation — the trailing exit must become an MTC_v2 exit module, not part of the producer.
- **Exit fidelity sensitivity:** win rate 35.5% with PF 2.04 depends on large winners captured by the trail; a different exit will change the edge.
- **Statistical caution:** fails BH-FDR/DSR — do not size as a proven edge.

## MTC_v2 producer/filter/exit/risk separation
- **Producer:** 8EMA pullback + impulse long entry (the part to expose as a producer signal).
- **Filter:** none currently (could later add a regime filter).
- **Exit:** EMA8 trailing close, hard stop (3-bar low), max-hold — map to MTC_v2 exit-first modules.
- **Risk:** 2R-equivalent sizing not used in exit-trail; risk = entry−stop. Define position sizing at integration.

## Exit-first compatibility
- Exit logic is already explicit and deterministic → compatible with exit-first design. Must be implemented/validated before entries are trusted.

## Token-efficiency notes
- Raw metrics referenced by path (no large tables duplicated). Full results: `05_BACKTEST_RESULTS/MEGA_walk_forward_results.json`.

## Missing information
- Original YouTube "8EMA" producer exact rules → `NEEDS_SOURCE_CONFIRMATION` (engine logic verified, source fidelity not).
- No forward (post-2026-04-27) data yet → forward paper-trade pending.
