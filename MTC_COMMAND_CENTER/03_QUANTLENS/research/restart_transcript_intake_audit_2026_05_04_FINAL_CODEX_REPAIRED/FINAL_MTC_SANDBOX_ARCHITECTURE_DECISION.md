# Final MTC Sandbox Architecture Decision

## Decision
Do not put all candidates into MTC_V2 at once. Build standalone candidate sandboxes one by one.

## Signal Contract
Each candidate must produce raw boolean long/short pulses through an MTC-compatible signal producer contract. Candidate signal logic must stay isolated from MTC_V2 production state.

## Shared Harness
Money management and risk behavior should be represented through an external shared harness concept: direction enable/disable, sizing, stop/target, trailing/BE where applicable, time exit, exit-first behavior, and no-repaint discipline.

## Pine Visual Review
Pine visual review scripts remain standalone. They should plot raw setup state, entry pulse, exit pulse, invalidation, and simple stop/target guides. They must not modify `01_PINE/MTC_V2.pine`.

## Python Parity
Each selected candidate later needs `candidate_contract.yml`, `candidate_rules.md`, `python_signal_model.py`, `python_backtest_harness.py`, `golden_cases.csv`, `tests/`, `standalone_pine_visual_review.pine`, `MTC_mapping.md`, and `VISUAL_REVIEW_CHECKLIST.md`.

## Promotion Gate
Production MTC integration requires manual visual review approval, source-faithful rules, strict Pine/Python signal parity, repaint elimination, proxy/data availability verification, Stage robustness, and explicit owner approval.
