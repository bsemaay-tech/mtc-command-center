# FORWARD_PAPER Observation Queue

> Karar 3 (2026-06-06): DSR<0.50 ama CPCV-robust + alpha-pozitif adaylar
> `PROMOTE_TO_FORWARD_PAPER_TRADE` — live-bar OOS gözlem. **Pine/MTC/live YOK,
> promotion YOK.** Sadece ileri veride takip kaydı; yeni veride tutarsa gerçek kanıt.

## Cohort 1 — Family templates (2026-06-06, fam_templates run)

En güçlü mekanik edge bu seansta. Dar grid (16 config) → DSR gücü korundu (A17).

| Strateji | Sym | TF | CPCV | DSR | Gate2 | Neden forward-paper |
|---|---|---|---|---|---|---|
| **MOMENTUM_CONTINUATION** | TRX | 4h | **15/15** | **0.492** | 78 | En yüksek DSR + tam CPCV |
| **MOMENTUM_CONTINUATION** | LINK | 4h | **15/15** | 0.403 | 80 | Cross-symbol teyit |
| **CONSOLIDATION_BREAKOUT** | TRX | 4h | **15/15** | 0.393 | 82 | Tam CPCV + en yüksek Gate2 |
| MOMENTUM_CONTINUATION | BTC | 4h | 13/15 | 0.266 | — | Cross-symbol (major) |
| PULLBACK_TO_MA | LTC | 4h | 14/15 | 0.264 | 81.9 | Robust |
| CONSOLIDATION_BREAKOUT | TRX | 2h | 14/15 | 0.101 | — | Robust |

**Ana sinyal:** MOMENTUM_CONTINUATION **4h cross-symbol** (TRX 15/15, LINK 15/15,
BTC 13/15) — tek hücre değil, 3 sembolde tutarlı. Runbook §3.2: cross-symbol consistency
= asıl sinyal. DSR 0.49 eşiğe en yakın (tüm seans).

**Caveat:** TRX bull-outlier riski (TRX birçok hücrede güçlü). LINK+BTC teyidi bu riski
azaltıyor ama down-market alpha ayrı doğrulanmalı.

## Sonraki adım (Barış onayı)
- B3 confirmation: MOMENTUM 4h için **dar pre-registered grid** (±1-2 step) → DSR'ı 0.50+
  geçirmeye çalış. Şu an 0.49 → küçük family daraltması eşiği geçirebilir.
- Forward-paper gözlem: live-bar OOS topla (kod yok, sadece kayıt).
- Implementasyon: `strat_extra_runner.py` QL_FAM_MOMENTUM_CONTINUATION.

## Aile-template kapsamı (N5 codeable pool)
- QL_FAM_PULLBACK_TO_MA ← CHARLES 50DMA/21EMA/base-top, SLINGSHOT 4EMA
- QL_FAM_CONSOLIDATION_BREAKOUT ← RYAN tight, GON high-tight flag, STAN 1B→2A
- QL_FAM_MOMENTUM_CONTINUATION ← TITO RS momentum, GON halt-momentum
- + QL_OLIVER_KELL (STG056), QL_LBR_COIL (STG057)
