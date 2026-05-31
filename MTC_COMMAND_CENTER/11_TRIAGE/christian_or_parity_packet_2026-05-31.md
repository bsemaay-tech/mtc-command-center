# Christian Open Range Parity Review Packet - 2026-05-31

Strategy: `QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M`

Source packet:
- Validation report: `11_TRIAGE/christian_or_validation_2026-05-31.md`
- Generator: `11_TRIAGE/block_bootstrap_christian_or.py`

## Decision

**Recommend promotion to PineTS parity review.**

The strongest case is `TRXUSDT 2h`, which passes both the block-bootstrap gate and the rolling-origin check. The other positive cells are not as clean, but they still clear the block-bootstrap threshold and show enough cross-symbol evidence to justify moving the strategy into the parity stage instead of parking it.

## Evidence summary

| Symbol | TF | Block p | Rolling pass | Read |
|---|---|---:|---:|---|
| OPUSDT | 1h | 0.07970 | 0/5 | PASS, weak rolling |
| ETHUSDT | 1h | 0.05990 | 2/5 | PASS, weak rolling |
| NEARUSDT | 4h | 0.12520 | 3/5 | WATCH |
| TRXUSDT | 2h | 0.03240 | 4/5 | PASS, best cell |
| BTCUSDT | 15m | 0.08310 | 2/5 | PASS, weak rolling |
| BTCUSDT | 4h | 0.22640 | 2/5 | WATCH |

## Why this is enough

- `4/6` cells satisfy the block-bootstrap gate.
- The strongest cell is not a one-off artifact: `TRXUSDT 2h` also has the best rolling-origin support.
- Cross-symbol coverage is broader than a narrow single-market fit, so this is worth parity review rather than immediate discard.

## Caveat

The rolling-origin evidence is mixed. This is not a green light for promotion to production; it is a gate pass into parity review with caution attached.

## Next step

Build the parity packet around:

1. `TRXUSDT 2h` as the anchor case.
2. OP/ETH/BTC as supporting but weaker confirmations.
3. A clear note that rolling-origin stability is not yet strong enough for production confidence.
