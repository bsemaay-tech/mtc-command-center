# PIPELINE_STATE — B1 envanteri (2026-06-06, Claude)

> Kaynak: `build_dashboard_snapshot().candidate_pipeline` (176 row) + `scorecards` (300 card).
> DeepSeek'in "196 row / 22 backtested / 22 promoted" sayıları **yanlış** — gerçek altta.

## Özet (gerçek)

| Metrik | Değer |
|---|---|
| Pipeline candidate row | **176** |
| current_stage = classified (erken) | 165 |
| current_stage = backtested | **11** |
| **promotable (Gate3 OK)** | **0 / 300 scorecard** |
| scorecard card (tüm run'lar) | 300 |

## 3 katman (next_action'a göre)

### Katman 1 — Backtested → "Build promotion packet" (11) — EN İLERİ
Gate2 evidence'ı var, promotion packet bekliyor (Gate1/1B/Gate3 eksik). QL_2026-05-01
ailesi — engine GRIDS'te + heavy_tier'de swept:
- Stg071 RSI 5-setup (1h) · Stg072 Bollinger 20/2 (ANY) · Stg073 7-candlestick (ANY)
- Stg075 VWAP pullback (5m) · Stg077 Dual-RSI 60/40 (1h) · Stg079 Multi-EMA channel
- Stg084 8EMA purple (10m) · Stg085 7-year pattern · Stg086 Purple Profits · + 2 exit/2-candle
- **Aksiyon:** Gate1/1B evidence + Gate3 artifact (C1) → scorecard_v2 → promotion packet.
  Çoğu DSR-floored → gerçek promotion değil, FORWARD_PAPER adayı (karar 3).

### Katman 2 — "Run walk-forward / OOS / alpha test" (86) — TEST EDİLEBİLİR, KOŞULMAMIŞ
Spec var ama engine'de değil / swept değil. Çoğu QL_NICK_* (weekly character change,
sell-decision, earnings cushion...) + QL_GON_* + diğerleri.
- **Aksiyon (B2):** mekanik/objektif olanları `strat_extra_runner.py` pattern'iyle kodla
  → sweep → Gate2. STG056 Oliver Kell bu şekilde yapıldı (örnek).
- **DİKKAT:** çoğu QL_NICK_* haftalık/diskresyoner (character change, sell framework,
  earnings) → **mekanik kodlanamaz**. Önce objektif-codeable alt kümeyi ayır (N5 audit).
  Threshold/pattern judgment gerektirenler Barış pre-register etmeli.

### Katman 3 — "Wiki/rejected → park" (76) — İLERLEYEMEZ (dürüst)
Wiki-only / module-branch / rejected-source / closed-source. Gerçek backtestable
strateji değil. **Aksiyon:** UI'da dürüstçe "parked + neden" göster (A6 why-not-promotable).

### Diğer (3): formula/source audit (2), split-into-cases (1)

### N5 audit — Katman 2'nin (86) codeable ayrımı (2026-06-06)
- **35 NET-CODEABLE** (mekanik indikatör): QL_GON_* (EMA touch/fader/halt-momentum),
  QL_KELL_EMA_CROSSBACK (≈STG056 yapıldı), QL_CHARLES_*_PULLBACK (50DMA/21EMA/base-top),
  QL_RYAN_TIGHT_BREAKOUT, QL_LBR_* (coil/3-bar/ATR-exit = STG057), QL_STAN_STAGE_2A_*,
  QL_TITO_RS_MOMENTUM, QL_SLINGSHOT_4EMA... → `strat_extra_runner.py` pattern ile kodlanabilir.
- **40 UNCLEAR** (manuel review): çoğu codeable (QL_GON_OG_BULL_FLAG, short-squeeze) ama
  threshold/pattern judgment ister → Barış pre-reg veya dikkatli implement.
- **11 DISCRETIONARY** (kodlanamaz): QL_NICK_WEEKLY_* (character change, sell-decision,
  earnings cushion, universe scan) → diskresyoner/haftalık. UI'da "parked + neden" göster.
- **B2 gece batch hedefi: ~40-50 codeable.** Her biri yeni hücreler = genuinely-new compute.
  DSR duvarı beklenir ama envanter dürüst ilerler.

## Gate dağılımı (300 scorecard)
- Gate2: ~en iyi run'da 53/72 PASS (heavy_tier). Genel: çoğu cell var.
- Gate1/1B: coded MEGA evidence'tan OK (intake/feasibility artifact'leri kısmi).
- **Gate3: 0 OK** — builder yok (C1 blocker). → **promotable 0**.

## Sıradaki aksiyonlar (bu plana göre)
1. **C1** — Gate3 artifact builder (spec-derivable) → 11 backtested + 53 Gate2-PASS cell'in
   Gate3 kısmi puanı çıkar, "ne eksik" netleşir.
2. **N5 audit** — Katman 2'nin 86'sından **objektif-codeable** alt kümeyi ayır (weekly/
   diskresyoner olanları ele). B2 night batch'i bunları kodlar.
3. **A1** — spec→metadata (165 classified'in UI "Not defined yet"i çözülür).
4. **B4** — DSR-floored ama CPCV-robust 11 backtested → FORWARD_PAPER işaretle (karar 3).

> Not: "İlerlet" = her katmanı dürüst en-ileri noktasına taşı. 76 park ilerlemez (normal).
> 11 backtested + objektif-codeable Katman-2 alt kümesi = gerçek aktif iş havuzu (~50-90).
