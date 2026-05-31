# Bug and Repair Report

## Missing Input Files
No material first-run/audited inventory path mismatch after clean-folder audit.

## Candidate Extraction Bugs
- First run used a narrow fixed candidate set, so many valid intakes were pooled rather than explicitly mapped one-to-one.
- Audited output creates coverage rows and audited cards with source traceability.

## Dedupe Bugs
- First-run clean inventory classified fewer duplicates than the earlier base folder; audited duplicate logic separates URL/video/strategy duplicates.

## Data Usage Bugs
- No evidence of microcap strategy being wrongly crypto-tested.
- 5m crypto proxy was used for intraday candidates, but audited reports downgrade those claims.

## Backtest Logic Bugs
- No direct lookahead proof found from exported trades, but first-pass fills are simplified proxies and high drawdowns make promotion unsafe.

## Metric Bugs
No material mismatch between first-run clean trade exports and audited recomputation.

## Fee Stress Bugs
No monotonic fee stress bug found.

## Classification / Overclaiming Bugs
- Huge net returns were unsafe to present as opportunity because drawdowns were extreme.
- Audited classifications reject Pine/MTC producer promotion.
