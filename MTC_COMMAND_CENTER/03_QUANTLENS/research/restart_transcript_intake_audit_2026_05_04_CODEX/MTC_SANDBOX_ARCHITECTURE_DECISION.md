# MTC Sandbox Architecture Decision

1. Should all strategies be added to MTC_V2 at once?
No. Do not add all strategies to MTC_V2. This phase found research candidates, modules, wisdom, duplicates, and blockers; none are production-ready.

2. Should each be separate at first?
Yes. Create one isolated candidate sandbox per strategy/module first.

3. How can MTC_V2 money management be reused without polluting production MTC_V2?
Reuse it through a shared MTC-compatible sandbox harness that receives raw long/short pulses and applies direction toggles, position sizing, SL/TP, trailing/BE, time exit, exit-first behavior, and no-repaint discipline outside production MTC_V2.

4. What should the standalone Pine visual review harness look like?
One standalone Pine file per candidate that plots raw setup, long pulse, short pulse, invalidation, stop/target guides, and debug labels. It must not be merged into 01_PINE/MTC_V2.pine.

5. What should the Python parity harness look like?
candidate_contract.yml defines inputs/outputs; python_signal_model.py emits raw pulses; python_backtest_harness.py is sandbox-only; golden_cases.csv captures expected signal rows; tests verify deterministic signal behavior before broader research.

6. What files should be created later for each candidate?
candidate_contract.yml, candidate_rules.md, python_signal_model.py, python_backtest_harness.py, golden_cases.csv, tests/, standalone_pine_visual_review.pine, MTC_mapping.md, VISUAL_REVIEW_CHECKLIST.md.

7. What promotion gate is required before real MTC integration?
Manual visual review, source-faithful rule spec, Python/Pine signal parity, no-repaint checks, data availability checks, OOS/robustness research, and explicit owner approval. Only then can a candidate become an MTC producer/filter candidate.
