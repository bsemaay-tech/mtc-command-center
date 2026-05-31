# MTC Mapping

## Candidate Role

`QLR_R215f4fj7V8` is treated as an isolated signal producer candidate for manual visual review.

## Later Pipeline Mapping

- Producer: raw long/short pulse producer.
- Filter: VWAP guard and range/no-man's-land guard.
- Exit: prior-bar trailing stop as candidate-specific exit idea.
- Sizing: source mentions setup quality/risk tiers, but this sandbox does not implement A/B/C sizing.

## MTC Money Management Reuse

Reusable later through an external shared harness:

- direction enable/disable
- fixed quantity or risk percentage mode
- stop mode
- take-profit mode
- time exit
- exit-first behavior
- no-repaint signal discipline

## Intentionally Not Used Yet

- Production `MTC_V2.pine`
- Production Python runners
- Portfolio-level optimizer
- Stage robustness runner
- Any real alert/trade automation

## Required Before Integration

1. Manual visual review pass.
2. Source-faithful rule clarification for catalyst/news context.
3. Python/Pine raw signal parity.
4. No-repaint checks.
5. Golden case expansion from real chart examples.
6. Stage robustness after visual/parity approval.
7. Explicit owner approval.
