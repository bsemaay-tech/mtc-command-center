# STAGE2 FINAL RECOMMENDATION

## Direct Answers
- Pine'a geçecek strateji var mı? `NO`.
- MTC producer adayı var mı? `NO_DIRECT_PROMOTION`.
- Sadece filter/gate olarak değerli model var mı? `NONE`.
- Reject edilmeli mi? `NONE`.
- Daha fazla data isteyen model var mı? `NONE_FOR_CRYPTO_DAILY_4H`; equity/session-specific fikirler bu Stage 2 kapsamı dışında.

## Largest Risks
- Crabel: drawdown and holdout sensitivity.
- Linda 5SMA: asset concentration and high drawdown on weak assets.
- BigBeluga: timeframe/regime sensitivity and parameter stability risk if neighbors weaken.

## Next Step
- Pine/parity değil; önce Stage 2 weak modeller için daha sıkı OOS + regime filter/gate deneyleri yapılmalı.

## Model Decisions
- `QL_CRABEL_RANGE_EXPANSION_STAGE2_v0`: `STAGE2_WEAK`; holdout PF is below pass threshold, despite strong aggregate and fee stress.
- `QL_LINDA_5SMA_RS_PULLBACK_v0`: `STAGE2_WEAK`; aggregate is positive, but parameter stability is `OVERFIT_RISK`.
- `QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0`: `STAGE2_WEAK`; metrics are promising, but not promoted because Stage 2 remains research-only and requires stricter OOS/regime validation before Pine.
