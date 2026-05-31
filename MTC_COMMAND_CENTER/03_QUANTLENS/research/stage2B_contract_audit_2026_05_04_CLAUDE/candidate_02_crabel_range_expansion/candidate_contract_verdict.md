# candidate_contract_verdict — Crabel Range Expansion

## Verdict
**PREVIOUS_BACKTEST_NOT_FAIR** + **CONTRACT_NEEDS_NATIVE_DATA**

(Eligible for `CONTRACT_READY_FOR_CODEX_RETEST` once intraday session data acquired.)

## Rationale
- Codex implemented a daily prior-range breakout with no NR filter and labelled it Crabel. This is not Crabel.
- The Stage-2 weak metrics measure a generic crypto-daily breakout, NOT Crabel's session-open Stretch breakout.
- Crabel's actual rules are extremely well-defined and codable; the contract is mechanically high-confidence.
- Strategy is intraday/session by design and CANNOT be fairly tested on current daily-only crypto bundle.

## Recommended next action
1. Obtain intraday OHLC for ES/NQ or US equity RTH (priority order).
2. Implement Stretch + NR{4,7,ID-NR4} producer per `CODING_REQUIREMENTS_FOR_CODEX.md`.
3. Walk-forward with NR vs no-NR side-by-side.
4. Crypto-adapted variant is allowed as a *separate*, explicitly-labelled candidate.

## Killshot conditions
After fair test, reject if:
- NR-filtered version does not improve over no-NR baseline.
- Edge disappears under realistic intraday slippage assumption.
- Multiplier sensitivity is sharp single-peak (overfit).
