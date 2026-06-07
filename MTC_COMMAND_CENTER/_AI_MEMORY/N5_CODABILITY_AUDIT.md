# N5 — Katman-2 Strateji Kodlanabilirlik Audit
_2026-06-07, Claude Sonnet 4.6_

> Kaynak: 63 stratejinin `07_deterministic_spec.md` + MEGA GRIDS incelemesi.
> Amaç: Hangi Katman-2 adayları Barış onayı olmadan autonomous kodlanabilir?

## Özet

| Sınıf | Sayı | Oran |
|---|---|---|
| ALREADY_IN_ENGINE | 35 | 56% |
| CODEABLE | 16 | 25% |
| PRE_REG_NEEDED | 8 | 13% |
| DISCRETIONARY | 4 | 6% |
| PARKED_NO_DATA | 6 | 9% |
| **Toplam** | **63** | |

> **Revizyon 2026-06-07a:** STG061 ve STG063 CODEABLE → PRE_REG_NEEDED olarak düzeltildi.
> **Revizyon 2026-06-07b:** STG027 PRE_REG_NEEDED → ALREADY_IN_ENGINE olarak düzeltildi.
> STG027 (BigBeluga RSI CHoCH) `strat_extra_batch_023_034.py`'de `QL_BIGBELUGA_RSI_v1` olarak kodlanmış.

**B2 gece batch hedefi:** 16 CODEABLE → 11'i zaten engine'de (batch023_034 + strat_extra),
5 yeni (STG028/033/034/046/053) `strat_batch_remaining.py` olarak kodlandı (2026-06-07).
**Recovery sweep 2026-06-07 (DeepSeek v4 Pro):** 425 jobs, 4 workers, 109.3s.
11 PASS → Gate2: 4 OK, 7 FAIL. Gate3: 11 INCOMPLETE. Promotable: 0/11.
Top: QL_VWAP_TREND_CONT_v1 ARBUSDT 1h (91.87), QL_EMA_RETEST_v1 BNBUSDT 4h (90.0).
D009 fixed: `_scipy_shim.py` (pure-Python norm, no scipy C extension needed).
9 PRE_REG: Barış threshold tanımladıktan sonra.

---

## Tam Tablo

| STG_ID | Strateji | Sınıf | Neden |
|---|---|---|---|
| STG001 | ADA Two-Candle S/R | ALREADY_IN_ENGINE | overnight_v2_runner patch |
| STG002 | LINK 8EMA Pullback | ALREADY_IN_ENGINE | overnight_v2_runner patch |
| STG003 | LTC RSI Oversold Recovery | ALREADY_IN_ENGINE | overnight_v2_runner patch |
| STG004 | Brian Shannon AVWAP Earnings | ALREADY_IN_ENGINE | overnight_v2_runner patch |
| STG005 | Brian Shannon AVWAP Gap Reclaim | ALREADY_IN_ENGINE | overnight_v2_runner patch |
| STG006 | Brian Shannon AVWAP Intraday OR | ALREADY_IN_ENGINE | overnight_v2_runner patch |
| STG007 | Brian Shannon AVWAP Stage2 | PRE_REG_NEEDED | Subjective stage gate — threshold gerekli |
| STG008 | Andrew Connell Gap 1D | ALREADY_IN_ENGINE | overnight_v2_runner patch |
| STG009 | Andrew Connell Gap 5m | ALREADY_IN_ENGINE | overnight_v2_runner patch |
| STG010 | Deepak Singhania 1-5-3 Filter | ALREADY_IN_ENGINE | overnight_v2_runner patch |
| STG011 | Deepak Singhania 259% Risk | ALREADY_IN_ENGINE | overnight_v2_runner patch |
| STG012 | Deepak Singhania Snapback 50SMA | ALREADY_IN_ENGINE | overnight_v2_runner patch |
| STG013 | Christian Flanders Episodic Pivot | ALREADY_IN_ENGINE | overnight_v2_runner patch |
| STG014 | Highest Volume Edge ProSwing | ALREADY_IN_ENGINE | overnight_v2_runner patch |
| STG015 | Launchpad ProSwing 1D | ALREADY_IN_ENGINE | overnight_v2_runner patch |
| STG016 | Christian Flanders Open Range | ALREADY_IN_ENGINE | overnight_v2_runner patch |
| STG017 | RS Phase Days ProSwing | ALREADY_IN_ENGINE | overnight_v2_runner patch |
| STG018 | Market Wizards Sell Rules | ALREADY_IN_ENGINE | overnight_v2_runner patch |
| STG019 | Christian Flanders Trail 20MA | ALREADY_IN_ENGINE | overnight_v2_runner patch |
| STG020 | Christian Flanders VCP Early | ALREADY_IN_ENGINE | overnight_v2_runner patch |
| STG021 | Minervini VCP Pivot Breakout | PRE_REG_NEEDED | Stage2 kontraksiyon threshold gerekli |
| STG022 | Richard Moglen VCP 1D | ALREADY_IN_ENGINE | overnight_v2_runner patch |
| STG023 | Kell Wedge Pop / Crossback | CODEABLE | EMA zone + range % + higher-low mekanik |
| STG024 | Martin/Luke Pullback AVWAP | CODEABLE | AVWAP + EMA destek + dönüş mekanik |
| STG025 | Slingshot 4EMA High Pullback | CODEABLE | EMA overlap + pullback + kırılım mekanik |
| STG026 | Crabel Range Expansion Stage2 | CODEABLE | Coil + range-expansion + ATR mekanik |
| STG027 | BigBeluga RSI CHoCH ATR | ALREADY_IN_ENGINE | strat_extra_batch_023_034 (QL_BIGBELUGA_RSI_v1) |
| STG028 | CANSLIM Shakeout Plus3 | CODEABLE | Baz + shakeout + 3-bar giriş mekanik |
| STG029 | Linda 5SMA RS Pullback | CODEABLE | 5SMA + RS rank + pullback + dönüş mekanik |
| STG030 | Linda 8am ET Opening Range | PARKED_NO_DATA | US market session open marker gerekli |
| STG031 | High-Beta Opening Bar Gap | PARKED_NO_DATA | US session-specific; kripto açılış yok |
| STG032 | Ty Rajnus Microcap Liquid Short | PARKED_NO_DATA | Microcap float + likidite tarayıcı gerekli |
| STG033 | Daily Extension Anti-Chase Filter | CODEABLE | Extension % + rejim kapısı mekanik |
| STG034 | EMA20/50 Two-Retests Baseline | CODEABLE | EMA çapraz + yeniden test mekanik |
| STG035 | QL 1H RSI Confluence | ALREADY_IN_ENGINE | MEGA orijinal GRIDS |
| STG036 | QL Bollinger Bands 20/2 | ALREADY_IN_ENGINE | MEGA orijinal GRIDS |
| STG037 | QL 7-Candlestick Pattern | PRE_REG_NEEDED | Mum geometri threshold gerekli |
| STG038 | QL VWAP Pullback Reversal | ALREADY_IN_ENGINE | MEGA orijinal GRIDS |
| STG039 | QL Two-Candle Sentiment SR | ALREADY_IN_ENGINE | MEGA orijinal GRIDS |
| STG040 | QL Dual-RSI 60/40 Pullback | ALREADY_IN_ENGINE | MEGA orijinal GRIDS |
| STG041 | QL Multi-EMA Channel | ALREADY_IN_ENGINE | MEGA orijinal GRIDS |
| STG042 | QL US Equities 8EMA 10m | ALREADY_IN_ENGINE | MEGA orijinal GRIDS |
| STG043 | QL US Equities 8EMA Exit Trail | ALREADY_IN_ENGINE | MEGA orijinal GRIDS |
| STG044 | QL Bull Flag LE Model | ALREADY_IN_ENGINE | MEGA orijinal GRIDS |
| STG045 | QL Purple Profits | ALREADY_IN_ENGINE | MEGA orijinal GRIDS |
| STG046 | QLR VWAP Multi-Anchor | CODEABLE | VWAP anchor + kırılım mekanik |
| STG047 | Brian Lee Small-cap Gap MR | PARKED_NO_DATA | Pre-market gap tarayıcı; microcap veri yok |
| STG048 | Anthony Layered Leadership | DISCRETIONARY | Tema/sektör rotasyon + piyasa döngüsü |
| STG049 | Brian Shannon AVWAP Method | DISCRETIONARY | Hot sektör tarama + piyasa farkındalığı |
| STG050 | Ariel Market-Timed Momentum | DISCRETIONARY | Piyasa durum kapısı + RS lider sıralaması |
| STG051 | David Ryan Price/Volume Stage | DISCRETIONARY | Stage tanımı öznel |
| STG052 | CANSLIM O'Neil Growth | PARKED_NO_DATA | Temel veri gerekli (çeyrek kazanç) |
| STG053 | Charles Harris Pullback Core | CODEABLE | 50DMA/21EMA + core zone mekanik |
| STG054 | Fishhook EP Day1 Retake | PRE_REG_NEEDED | Fishhook pattern threshold gerekli |
| STG055 | Gon Low-Float Momentum | PARKED_NO_DATA | Halt dedektör + float tarayıcı (US) |
| STG056 | Oliver Kell Price Cycle | ALREADY_IN_ENGINE | strat_extra_runner (kodlandı) |
| STG057 | Linda Raschke LBR Toolkit | ALREADY_IN_ENGINE | strat_extra_runner (coil variant) |
| STG058 | Martin Parabolic Pullback | PRE_REG_NEEDED | Parabolic SAR threshold + champion filtresi |
| STG059 | Nick Weekly Stage | DISCRETIONARY | Karakter değişimi + kazanç zamanlaması |
| STG060 | Roppel Leadership Position | DISCRETIONARY | RS "hendek" + pozisyon büyüklüğü kararı |
| STG061 | Ryan Pierpont Breakout | PRE_REG_NEEDED | Spec: "thresholds unknown — formalize first" |
| STG062 | Stan Weinstein Stage | PRE_REG_NEEDED | Stage threshold (destek/direnç) gerekli |
| STG063 | Tito Options-Aware RS | PRE_REG_NEEDED | Spec: "options rules unknown; Low readiness" |

---

## CODEABLE — 16 strateji (autonomous batch için öncelik)

STG023 · STG024 · STG025 · STG026 · STG028 · STG029 · STG033 · STG034 · STG046 · STG053

Not: STG023-029 ve STG033-034 **batch023_034'te swept** (ilk tarama).
STG028/033/034/046/053 **strat_batch_remaining.py**'de kodlandı (2026-06-07).
STG061/063 PRE_REG_NEEDED'a taşındı (spec "thresholds unknown" diyor).

Tüm 16 CODEABLE strateji için kod mevcut. Sweep çalışıyor.

## PRE_REG_NEEDED — 8 strateji (Barış threshold tanımlamalı)

| STG | Neye ihtiyaç var |
|---|---|
| STG007 | Stage2 EMA/MA gösterge eşiği |
| STG021 | Kontraksiyon % eşiği (Minervini VCP dar baz) |
| STG037 | 7 mum pattern geometri tanımı |
| STG054 | Fishhook pattern derinlik/hız eşiği |
| STG058 | Parabolic SAR çarpan eşiği + "champion" filtresi |
| STG061 | Pierpont extension eşiği + danger-zone sınırı |
| STG062 | Weinstein Stage2 MA eğim eşiği + hacim eşiği |
| STG063 | Tito RS eşiği + crossback trigger |
