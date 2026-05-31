# Candidate Card — CAND_037

- **Source intake:** `3 Mayıs/INTAKE_2026-05-03_FtAshnE3MwM_stan_weinstein_stage_analysis.md`
- **Source URL:** https://www.youtube.com/watch?v=FtAshnE3MwM
- **Video ID:** FtAshnE3MwM
- **Title:** The Simple Stage Analysis Trading System - Exclusive Interview with Stan Weinstein
- **Existing candidate id (if any):** YC_2026
- **Codex status (intake):** READY_FOR_PYTHON_PROTOTYPE

## Thesis (one sentence)

Extracted from intake (auto-summary). Verify against source before promotion.

## Classification

- **Strategy family:** STRATEGY
- **Asset class:** US_EQUITY
- **Native timeframe:** 1d
- **MTC relevance:** PRODUCER_CANDIDATE
- **Testability:** TEST_WITH_1D_CRYPTO_PROXY

## Required data
- Native: see asset_class / primary_tf above.
- Local availability for crypto 5m: 17 symbols (BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT, ADAUSDT, DOGEUSDT, AVAXUSDT, LINKUSDT, DOTUSDT, LTCUSDT, TRXUSDT, POLUSDT, APTUSDT, ARBUSDT, NEARUSDT, OPUSDT) — research-only manifest.
- US equity / microcap: NOT available locally → blocked or proxied.

## Entry logic (raw extract)
## Entry Logic Draft

## Exit logic (raw extract)
## Exit / Risk Logic Draft

## Stop logic (raw extract)
## Riskli veya Supheli Iddialar

1. **75–80% win rate iddiasi**
   - Transcriptte iyi calisma ile yuksek dogruluk orani mumkun oldugu belirtiliyor.
   - Bu iddia dogrudan alinmamali; dataset uzerinde test edilmeden strateji varsayimi yapilmamali.

2. **Stage detection subjektif olabilir**
   - Base, support, resistance ve Stage 3 tanimi insani chart reading'de kolay, algoritmik tespitte zor.
   - Prototipte explicit numeric thresholds kullanilmali.

3. **Market breadth verisi gerektirir**
   - Advance/decline line, percent stocks in bear market, buy/sell signal count gibi datalar her ortamda mevcut olmayabilir.
   - Ilk prototipte basit benchmark ve sector/group proxy ile baslanmali.

4. **200-gun MA tek basina yeterli degil**
   - Transcript 200-gun MA'yi ana yapisal arac olarak anlatsa da volume, base, group strength ve risk/reward birlikte kullaniliyor.
   - Basit `close > SMA200` sistemi bu videonun tam mantigini temsil etmez.

5. **Extension trim threshold context-sensitive**
   - 50–60% above SMA200 ornegi her volatilite rejimi ve hisse icin ayni sonucu vermeyebilir.
   - ATR-normalized extension alternatifi denenmeli.

---

## Sizing (raw extract)
## Position Sizing Draft

## Ambiguities
- Crypto-proxy applicability for US-equity-native setups (catalyst, gap, session).
- Discretionary "support/resistance" or "candle confirmation" rules require deterministic formalization before backtest.

## Conservative formalization for Python prototype
- Replace any discretionary subjective check with a single deterministic rule.
- If the strategy depends on US session, gap, or earnings catalyst, mark DATA_BLOCKED unless an explicit numeric proxy is documented in this card.

## Critical caveats
- Tonight's run is Python-only research; no Pine, no parity, no live alerts.
- A weak or rejected result is acceptable if evidence-based.
