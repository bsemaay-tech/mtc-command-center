# Candidate Card — CAND_027

- **Source intake:** `3 Mayıs/INTAKE_2026-05-03_6tnREqUJ1WY_trading_backtests_misleading.md`
- **Source URL:** https://www.youtube.com/watch?v=6tnREqUJ1WY
- **Video ID:** 6tnREqUJ1WY
- **Title:** Trading Backtests Are Misleading - Here's what to do instead
- **Existing candidate id (if any):** -
- **Codex status (intake):** WIKI_ONLY

## Thesis (one sentence)

Extracted from intake (auto-summary). Verify against source before promotion.

## Classification

- **Strategy family:** STRATEGY
- **Asset class:** US_EQUITY
- **Native timeframe:** UNKNOWN
- **MTC relevance:** PRODUCER_CANDIDATE
- **Testability:** TEST_WITH_1D_CRYPTO_PROXY

## Required data
- Native: see asset_class / primary_tf above.
- Local availability for crypto 5m: 17 symbols (BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT, ADAUSDT, DOGEUSDT, AVAXUSDT, LINKUSDT, DOTUSDT, LTCUSDT, TRXUSDT, POLUSDT, APTUSDT, ARBUSDT, NEARUSDT, OPUSDT) — research-only manifest.
- US equity / microcap: NOT available locally → blocked or proxied.

## Entry logic (raw extract)
## Setup Variables
- Fresh material news? yes/no
- All-time high / major level breakout? yes/no
- Prior consolidation? yes/no
- Relative volume:
- Short interest / float:
- Similar names moving? yes/no
- Market context supportive? yes/no

## Exit logic (raw extract)
_(see source intake)_

## Stop logic (raw extract)
## Riskli veya Supheli Iddialar

1. **Discretionary edge genellenebilir olmayabilir**
   - Lance'in hizli yorumlama becerisi herkese aktarilamaz. Bu nedenle systematize edilirken explicit feature set gerekir.

2. **News catalyst verisi yoksa yanlis backtest riski yuksek**
   - OHLCV-only test, haberli ve habersiz hareketleri karistirabilir.

3. **Level 2 / tape-reading Pine tarafinda dogrudan yok**
   - Bu bilgiler ancak proxy ile veya ayri veri pipeline ile modele eklenebilir.

4. **Meme/squeeze rejimleri nadir ve degiskendir**
   - Bu rejimler icin tarihsel data az oldugundan position sizing dusuk tutulmali.

5. **Forward testing daha hizli ama daha az kesinliklidir**
   - Forward testing, erken adaptasyon saglar; fakat az orneklem yuzunden false confidence yaratabilir.

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
