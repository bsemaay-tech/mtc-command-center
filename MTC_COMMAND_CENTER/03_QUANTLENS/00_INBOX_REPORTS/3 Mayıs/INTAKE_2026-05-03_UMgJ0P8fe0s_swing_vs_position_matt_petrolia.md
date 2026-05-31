# QuantLens Transcript Intake Report

## Metadata

- Intake ID: `INTAKE_2026-05-03_UMgJ0P8fe0s`
- Source URL: https://www.youtube.com/watch?v=UMgJ0P8fe0s
- Original URL: https://youtu.be/UMgJ0P8fe0s?si=eKWvqv-TW7Z9oeTt
- Video ID: `UMgJ0P8fe0s`
- Title: `Swing Trading Vs. Position Trading`
- Speaker / Guest: Matt Petrolia / Matt Petrallia
- Channel: TraderLion / UNKNOWN_CHANNEL in file metadata
- Intake Date: 2026-05-03
- Transcript Archive Path: `/mnt/data/Swing Trading Vs.md`
- Transcript Hash SHA256: `3503ca634d4002a28d6275c59c8d119f92052d7cf5f58be0c7dfa56f4376da63`
- Duplicate Check: `NOT_VERIFIED` — repo registry erişimi yok; yalnızca bu oturumdaki dosya adı ve URL bazında yeni dosya olarak ele alındı.
- Channel Quality Check: `NOT_VERIFIED` — `channel_blacklist.yaml` ve `channel_quality_registry.csv` erişimi yok.
- MTC_V2 Files Modified: `NO`
- Production Python Runner Modified: `NO`
- Backtest / Optimization Run: `NO`

## Final Classification

- Classification: `SALVAGE`
- Codex Status Suggestion: `SALVAGE_ONLY`
- Confidence: `HIGH`
- Reason: Transcript güçlü bir entry producer vermez; ancak swing/position ayrımı, trade-management routing, partial profit, break-even stop, environment-aware exit policy ve position-trade SMA trailing mantığı açısından çok değerli bir risk/position-management modülü sağlar.

## Executive Summary

Bu video doğrudan “al/sat sinyali” üreten tek başına bir strateji değildir. Ana değeri, aynı entry sinyalinin farklı yönetim rejimlerine ayrılmasıdır:

1. **Swing trade**: Günlük chart sinyali, kısa süre, hızlı kâr realizasyonu, 1–1.5R ilk partial, break-even koruması, hedef / direnç civarında çoğunluğu satma.
2. **Position trade**: Haftalık chart setup’ı, daha uzun duration, daha büyük R potansiyeli, trendin devamı için pullback tolere etme, key SMA üzerinde soft trailing stop.
3. **Environment-aware management**: Piyasa koşulu kötü ise swing duration kısalır, partial daha erken alınır, position trade kapatılır veya hiç açılmaz.
4. **Plan-first execution**: Trade’e girmeden önce veya hemen sonra bu trade’in swing mi position mı yönetileceği belirlenir. Böylece sonradan “let winners run” ile “base hit al çık” mantığı birbirine karışmaz.

Bu nedenle video, QuantLens / MTC_V2 için **Signal Producer** değil, **Exit Rules + Position Manager + PortfolioState policy** katmanına aday bilgi sağlar.

## Key Ideas Extracted

### 1. Trade Management Router

Ana fikir:

```text
Entry signal geldikten sonra trade_type belirlenir:
- SWING
- POSITION
```

Bu ayrım, aynı pozisyona uygulanacak exit ve partial kurallarını değiştirir.

#### SWING mode

- Signal timeframe: Daily
- Beklenen duration: 1 gün – birkaç hafta
- Beklenen hedef: çoğunlukla 3R–5R arası; zayıf piyasa ortamında 1R–2R kabul edilebilir
- İlk partial: yaklaşık 1R–1.5R
- İlk partial sonrası stop: break-even veya çok yakın koruma
- Çoğunluk çıkışı: direnç, target zone, momentum zayıflaması, önceki swing high, high-range candle sonrası
- Amaç: anlamlı pullback başlamadan önce çoğunu veya tamamını satmak

#### POSITION mode

- Signal timeframe: Weekly setup + daily execution olabilir
- Beklenen duration: haftalar / aylar
- Beklenen hedef: büyük R multiple, trend continuation
- İlk partial yine alınabilir: yaklaşık 1R–1.5R
- Stop yönetimi: key SMA altında anlamlı kapanış, örnek 10SMA / 20SMA / 21EMA / 50SMA gibi sembolün karakterine göre
- Soft stop: key SMA + tolerans filtresi
- Hard stop: flash-crash veya beklenmedik gap riskine karşı daha aşağıda koruyucu stop
- Amaç: trendin etini almak; her küçük pullback’te çıkmamak

## Strategy Candidate Assessment

### Is this a standalone strategy?

`NO`.

Transcript, net bir entry producer tanımlamıyor. Bazı örneklerde opportunistic entries, downtrend-line reclaim, moving-average reclaim, previous high trigger, news-volume reversal gibi parçalar var; fakat bunlar sistematik entry spec seviyesinde değil.

### Is this usable as a strategy-management component?

`YES`.

Aşağıdaki bileşenler kodlanabilir:

| Module | Candidate Value | Notes |
|---|---:|---|
| Trade Type Router | High | Entry sonrası SWING/POSITION mode ataması |
| Swing Partial Exit | High | 1R–1.5R partial + BE stop |
| Position SMA Trail | High | Key SMA altında meaningful close ile exit |
| Environment-Adaptive Exit | Medium/High | Strong trend vs chop market ayrımı |
| Account Mix Policy | Medium | %60–70 swing, %30–40 position örneği kişisel; parametreleştirilmeli |
| Volatility Suitability Filter | Medium | Çok oynak isimleri position trade dışında bırakma |
| Psychological Rule Encoding | Medium | Winner-to-loser dönüşünü engelleme |

## Proposed MTC_V2 Mapping

### Layer Mapping

| MTC_V2 Layer | Kullanım |
|---|---|
| Signal Producer | Doğrudan kullanılmaz |
| Signal Transform Pipeline | Opsiyonel: setup_quality / trade_type tag üretebilir |
| Entry Gates | Volatility suitability, weekly setup eligibility, market environment |
| Position Manager | `trade_management_mode = SWING / POSITION` |
| Position Sizing | Mode’a göre risk fraction ve exposure cap |
| Exit Rules | Partial, BE, key SMA trail, target zone, high-range candle de-risk |
| PortfolioState | Swing/position allocation mix, open risk, realized/unrealized P&L ayrımı |

### Suggested Config Sketch

```yaml
trade_management:
  mode_policy:
    enabled: true
    default_mode: SWING
    position_mode_requires_weekly_setup: true
    position_mode_requires_market_regime: STRONG_UPTREND

  swing:
    signal_timeframe: D
    first_partial_r: 1.0
    first_partial_pct: 0.25
    move_stop_to_breakeven_after_first_partial: true
    target_exit_enabled: true
    target_reference:
      - previous_swing_high
      - resistance_zone
      - range_expansion_bar
    max_holding_bars_soft: 10

  position:
    signal_timeframe: W
    first_partial_r: 1.0
    first_partial_pct: 0.20
    key_sma:
      candidates: [10, 20, 21, 50]
      selection: best_recent_respected_ma
    meaningful_close_filter_pct: 1.0
    hard_stop_enabled: true
    allow_earnings_hold_if_cushion: false

  environment:
    chop_mode_partial_r: 1.0
    trend_mode_partial_r: 1.5
    disable_position_trades_in_chop: true
```

## Python Prototype Ideas

### Prototype A — Swing Partial + BE Protection

**Goal:** Mevcut MTC_V2 entry producer’larına uygulanabilecek swing exit overlay’i test etmek.

Rules:

1. Entry açılır.
2. Initial R = `abs(entry - initial_stop)`.
3. Fiyat `entry + 1R` veya `entry + 1.5R` seviyesine ulaşırsa:
   - Pozisyonun `%25–%50` kısmı kapanır.
   - Kalan pozisyon stop’u break-even’a çekilir.
4. Target zone veya momentum zayıflaması tespit edilirse kalan pozisyonun büyük kısmı kapanır.
5. Kalan küçük lot opsiyonel runner olarak bırakılabilir.

Test dimensions:

- `first_partial_r`: 1.0 / 1.25 / 1.5 / 2.0
- `first_partial_pct`: 25% / 33% / 50%
- `be_after_partial`: true / false
- `target_exit`: previous high / ATR multiple / resistance proxy
- `runner_pct`: 0% / 10% / 25%

### Prototype B — Position Trade SMA Trail

**Goal:** Büyük trendlerde erken çıkmamak için position-mode trailing çıkışını test etmek.

Rules:

1. Position mode sadece market regime güçlü ise aktif.
2. Weekly setup veya weekly trend filter yoksa position mode devreye girmez.
3. First partial yine 1R–1.5R civarında alınır.
4. Kalan pozisyon key SMA üzerinde taşınır.
5. Key SMA altında meaningful close varsa exit.
6. Extreme high-range / high-volume bar sonrası kısmi risk azaltma opsiyonel.

Test dimensions:

- `key_sma`: 10 / 20 / 21 / 50
- `sma_filter_pct`: 0.0 / 0.5 / 1.0
- `close_confirm_bars`: 1 / 2
- `partial_before_sma_trail`: true / false
- `high_range_de_risk`: true / false

### Prototype C — Mode Router

**Goal:** Aynı entry’nin SWING veya POSITION olarak yönetilmesi performansı nasıl değiştiriyor?

Inputs:

- Market regime score
- Weekly trend strength
- Volatility / ADR / ATR%
- Relative strength
- Thematic leader flag if available
- Price distance from key moving averages

Outputs:

```text
trade_mode = SWING | POSITION | REJECT_POSITION_USE_SWING_ONLY
```

## Suggested Rule Candidates

### Swing Mode Rule Candidate

```text
IF entry_trigger == true
AND market_regime != BEAR
AND daily_setup_quality >= threshold
THEN open SWING trade

Initial stop = setup low or ATR stop
First partial = 1.0R to 1.5R
After partial = stop to break-even
Major exit = target/resistance/range expansion/failed follow-through
```

### Position Mode Rule Candidate

```text
IF entry_trigger == true
AND weekly_setup == true
AND market_regime == STRONG_UPTREND
AND volatility_suitability == true
THEN open POSITION trade

Initial stop = setup low or weekly/daily structure
First partial = 1.0R to 1.5R
Runner stop = selected key SMA with meaningful-close filter
Hard catastrophic stop = always active
```

## Risk and Parity Notes

### Parity-sensitive areas

- Intrabar detection of R targets must be deterministic.
- If both partial target and stop touch in same bar, Python must follow MTC canonical OHLC path rules.
- Break-even stop mutation must be single-owner and monotonic after partial.
- SMA trailing stop must not repaint; only confirmed close should update trail state.
- If higher timeframe weekly setup is used, Pine must use prior-closed HTF semantics.
- Partial exit accounting must be normalized between Pine Strategy Tester and Python engine.

### Potential failure modes

| Failure Mode | Mitigation |
|---|---|
| Overfitting first partial level | Test broad R bands, not one magic value |
| Confusing swing and position exits | Store mode at entry and do not mutate without explicit rule |
| Position mode in choppy market | Require regime gate |
| Too many tiny partial rules | Keep first version simple: first partial + BE + one final exit |
| Unrealistic intrabar target fills | Use deterministic fill model and slippage assumptions |
| Taking position trades in ultra-volatile names | Add volatility suitability filter |

## Trader Wiki Value

This transcript also deserves a Trader Wiki note under:

```text
11_TRADER_WIKI/04_SYSTEM_DEVELOPMENT/
```

Suggested wiki file:

```text
TW_2026-05-03_TRADE_MANAGEMENT_swing_vs_position_trade_alignment.md
```

Topic:

- `04_SYSTEM_DEVELOPMENT`
- Secondary tags: `risk_management`, `position_sizing`, `exit_rules`, `partial_profits`, `trade_alignment`

Usefulness Score: `8/10`

## Recommended Repo Actions

Do not modify Pine or production runner yet.

Recommended next actions:

1. Save this as a SALVAGE_ONLY intake.
2. Create a research note under Trader Wiki.
3. Later, when building MTC_V2 exit/position-manager upgrades, implement:
   - `trade_management_mode`
   - `first_partial_r`
   - `move_stop_to_be_after_partial`
   - `swing_target_exit`
   - `position_key_sma_trail`
4. Compare against earlier Minervini progressive exposure report, because both belong to the same risk/position-management family.
5. Only after isolated Python tests show improvement should any Pine integration be planned.

## Final Decision

```text
STATUS: SALVAGE
CODEX_STATUS: SALVAGE_ONLY
REASON: No standalone entry strategy; high-value exit/position-management framework.
NEXT_ACTION: Add to risk/position-management research backlog; do not create standalone strategy candidate.
```

## Files Created / Touched

Created:

```text
INTAKE_2026-05-03_UMgJ0P8fe0s_swing_vs_position_matt_petrolia.md
```

Not touched:

```text
01_PINE/MTC_V2.pine
Production Python runner files
Backtest / optimization outputs
Candidate strategy registry
Large CSV / cache / data bundle files
```
