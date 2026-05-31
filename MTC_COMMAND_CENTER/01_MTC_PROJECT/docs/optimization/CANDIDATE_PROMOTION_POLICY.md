# Candidate Promotion Policy

## Research Candidate

A research candidate is any ranked optimizer row with enough metadata to inspect. It may be useful for diagnostics but has no robustness or production meaning.

## Medium Robust Candidate

A medium robust candidate passes the current coverage-aware medium threshold in the optimizer output. It may be used to seed a second-pass optimization.

Medium candidates cannot be written into Pine defaults and cannot be described as release-ready.

## Strict Robust Candidate

A strict robust candidate must satisfy all of the following:

- Train, validation, and test performance are positive.
- `walkforward_consistency >= 0.70`.
- `positive_symbol_count >= 3`.
- `positive_timeframe_count >= 3`.
- Regime breakdown must not collapse in CHOPPY or CONSOLIDATING regimes.
- Duplicate conflicts must be 0.
- Dataset hashes must be valid.
- No live, production, or TradingView release claim is allowed without final TradingView audit.

## Promotion Candidate

A promotion candidate is a strict robust candidate selected for final release-audit preparation. It must be packaged with exact params, datasets, hashes, code version, report paths, and a TradingView final audit plan.

## Candidate Promotion Requires Complete/Stable Run Context

A candidate should not be promoted if it comes from an interrupted or unverified run, if resume/de-dup status is not clean, if worker conflicts exist, if the benchmarked worker policy was not followed, if data source/hash/manifest evidence is missing, or if the run was executed only inside the Codex terminal and may have aborted without a clean checkpoint.

## Non-Negotiables

- Medium candidates may seed second-pass optimization only.
- Production promotion requires TradingView release audit.
- Optimization output alone never changes Pine defaults.
- Optimization output alone never claims TradingView release parity.

## Search-Space Reduction Promotion Boundary

- Parameter library entries are research seeds only.
- Medium candidates may seed staged refinement but cannot become Pine defaults.
- A candidate found through smart sampling still requires strict robust status and final TradingView audit before promotion.
