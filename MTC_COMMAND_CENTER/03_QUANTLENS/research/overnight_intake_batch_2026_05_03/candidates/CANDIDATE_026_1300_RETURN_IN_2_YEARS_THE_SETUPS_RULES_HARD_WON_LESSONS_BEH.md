# Candidate Card — CAND_026

- **Source intake:** `3 Mayıs/INTAKE_2026-05-03_6aOnCK1gv2w_chris_flanders_edge.md`
- **Source URL:** https://www.youtube.com/watch?v=6aOnCK1gv2w
- **Video ID:** 6aOnCK1gv2w
- **Title:** +1300% Return in 2 Years The Setups Rules Hard Won Lessons Behind Chris Flander's Edge
- **Existing candidate id (if any):** QL_CAND_20260503_EP_ORB_001
- **Codex status (intake):** i

## Thesis (one sentence)

Extracted from intake (auto-summary). Verify against source before promotion.

## Classification

- **Strategy family:** PROCESS_ONLY
- **Asset class:** US_EQUITY
- **Native timeframe:** monthly
- **MTC relevance:** PROCESS_ONLY
- **Testability:** REJECT_NOT_TESTABLE_AS_PRODUCER

## Required data
- Native: see asset_class / primary_tf above.
- Local availability for crypto 5m: 17 symbols (BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT, ADAUSDT, DOGEUSDT, AVAXUSDT, LINKUSDT, DOTUSDT, LTCUSDT, TRXUSDT, POLUSDT, APTUSDT, ARBUSDT, NEARUSDT, OPUSDT) — research-only manifest.
- US equity / microcap: NOT available locally → blocked or proxied.

## Entry logic (raw extract)
### Entry Logic

1. Önceden EP günü oluşmuş olmalı.
2. EP sonrası dar range / flag / consolidation oluşmalı.
3. Pullback hacmi düşük veya range sıkı olmalı.
4. Breakout günü yeni high veya flag high üstü kapanış/taşma olmalı.
5. Mevcut pozisyon varsa add-on yapılır; yoksa secondary entry yapılabilir.

## Exit logic (raw extract)
### Exit Logic

- Initial stop asla genişletilmez.
- Trade hızlı şekilde profit cushion üretmezse erken çıkış / stop.
- Büyük kazanan haline gelirse stop gevşetilebilir; ancak sadece winner için.
- Persistent trender olursa 21 EMA / 50 DMA bazlı takip yapılabilir.
- Climax / blowoff karakteri gösterirse strength içine kademeli satış yapılabilir.

## Stop logic (raw extract)
### Risk

Bu candidate EP/ORB kadar net kurallı değil. Theme detection objektifleştirilmeden overfit riski yüksek.

---

## Sizing (raw extract)
_(see source intake)_

## Ambiguities
- Crypto-proxy applicability for US-equity-native setups (catalyst, gap, session).
- Discretionary "support/resistance" or "candle confirmation" rules require deterministic formalization before backtest.

## Conservative formalization for Python prototype
- Replace any discretionary subjective check with a single deterministic rule.
- If the strategy depends on US session, gap, or earnings catalyst, mark DATA_BLOCKED unless an explicit numeric proxy is documented in this card.

## Critical caveats
- Tonight's run is Python-only research; no Pine, no parity, no live alerts.
- A weak or rejected result is acceptable if evidence-based.
