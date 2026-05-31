# Audit Eligibility Jump Review - 2026-05-31

This review compares the current `mcc_readonly.audit_reader.build_candidate_audit()` snapshot with a no-merge baseline where `_merged_source_record()` is disabled.

## Snapshot delta

| Metric | Current | Baseline | Delta |
|---|---:|---:|---:|
| Total rows | 196 | 196 | 0 |
| Eligible for backtest | 167 | 178 | -11 |
| Blocked rows | 26 | 15 | +11 |
| Canonical rows | 167 | 178 | -11 |
| Source quality `REJECTED` | 70 | 0 | +70 |

## What changed

The 11 lost eligible rows are all cases where a higher-rank `quantlens_source_map.csv` record overrides the older `FINAL_LLM_KNOWLEDGE_BASE.jsonl` / `FINAL_REPAIR` style record.

That override changes the source classification from strategy-like to `REJECT_LOW_QUALITY` / `REJECT_NO_TEST`, which then propagates into:

- `blocked_reason = rejected source classification`
- `source_quality = REJECTED`
- `eligible_for_backtest = False`

## Lost rows

| Candidate ID | Title | Current reason |
|---|---|---|
| `QLR_10pHBNVi4Jc` | The Trading Setups of the Record Breaking Trading Champion | rejected source classification |
| `QLR_7UfHg8PpDZk` | The 3 Powerful Trading Setups of a Top Super-performance Trader | rejected source classification |
| `QLR_KQRuUWSZvLE` | 10 Steps to Profitable Trading in 2024 Ryan Pierpont | rejected source classification |
| `QLR_KWxhLIOchvY` | 409% Return in 1 Year Aggressive Swing Trading Tactics and Setups | rejected source classification |
| `QLR_Nq-p7Bu1YT0` | How A Day Trader Turned into a Super-Performance Swing Trader - Real Simple Ariel | rejected source classification |
| `QLR_R215f4fj7V8` | The Simple Trading Setup That Made Lance Breitstein Millions | rejected source classification |
| `QLR_ZK5cnVQ2V3Q` | The Market Wizard Trading System | rejected source classification |
| `QLR__QewlGLBaeA` | Trading Millions How I Finally Became a Profitable Swing Trader | rejected source classification |
| `QLR_kao-hhaQnig` | 103% Return in 1 Year The Simple Event Driven Trading Setup | rejected source classification |
| `QLR_oPeTkxTnooA` | 259% Return in 1 Year The Risk Management Strategy YOU Need for Consistent Returns | rejected source classification |
| `QLR_zw96qkUn9_g` | How Clement Ang Achieved 150%+ Returns in the US Investing Championship | rejected source classification |

## Assessment

This is not a data-loss regression. It is a strictness change caused by the source-map rank winning over older strategy-style classifications.

The result looks defensible if the intent is to treat `quantlens_source_map.csv` as the authoritative gatekeeper for no-test / reject decisions.

The one thing worth watching is the magnitude: the rank change moves 11 candidates out of the execution queue in one shot. That is fine if deliberate, but it is the kind of change that should stay visible in the dashboard so the queue does not feel mysteriously smaller.

## Recommendation

Keep the current merge order for now, but spot-check the 11 downgraded rows before using the audit snapshot as an execution queue. If the source map is meant to be advisory rather than authoritative, lower its precedence below the strategy-style final classifications.
