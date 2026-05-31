# candidate_contract_verdict — BigBeluga

## Verdict
**PREVIOUS_BACKTEST_NOT_FAIR** + **CONTRACT_READY_FOR_CODEX_RETEST**

## Rationale
- Codex's implementation has look-ahead bias, wrong pivot length, wrong divergence definition, no direction-latching, no trailing stop, and no ladder TPs. Stage-2 numbers measure a fundamentally different strategy.
- The actual indicator is well-defined Pine source (visible in intake) — easy to replicate faithfully.
- Crypto data is sufficient for the rerun → unique among the six in being immediately retestable.
- AUDITED + CLEAN cards both misattributed the source video; only the indicator-audit intake (`XNZ4f-b3ED8`) is authoritative.

## Recommended next action
1. Fork BigBeluga Pine source directly into Python prototype (preserve every default).
2. Validate non-repaint on small known-pivot examples.
3. Walk-forward 4h and 1D crypto majors with FULL exit framework (trail + ladder + opp-CHoCH).
4. Promote/reject only after faithful implementation tested.

## Killshot conditions
After fair test, reject if:
- Trail-included strategy is still negative after fees.
- Sensitivity to ms_len is knife-edge.
- Edge concentrated in one asset / one regime.
