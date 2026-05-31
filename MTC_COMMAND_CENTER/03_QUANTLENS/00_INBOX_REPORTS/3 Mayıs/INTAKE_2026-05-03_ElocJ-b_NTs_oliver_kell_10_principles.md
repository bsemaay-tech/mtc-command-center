# QuantLens Transcript Intake Report — Oliver Kell / 10 Principles of Trading

## 1. Metadata

- **Source URL:** https://youtu.be/ElocJ-b_NTs?si=5HoHV7QnhLAqXNM1
- **Normalized URL:** https://www.youtube.com/watch?v=ElocJ-b_NTs
- **Video ID:** `ElocJ-b_NTs`
- **Title:** `The 10 Principles of Trading with Investing Champion Oliver Kell`
- **Channel:** `UNKNOWN_CHANNEL`
- **Transcript file:** `The 10 Principles of Trading with Investing Champion Oliver Kell.md`
- **Transcript SHA256:** `b443225f836ace82eae32800d6c3c3b590a010e7258a841e0951f113792a0e53`
- **Approx. word count:** `16,719`
- **Intake date:** 2026-05-03
- **Duplicate status:** `NOT_DUPLICATE_IN_CURRENT_SESSION`
- **Repo registry duplicate check:** `NOT_VERIFIED_REPO_NOT_AVAILABLE`
- **Channel blacklist check:** `NOT_VERIFIED_REPO_NOT_AVAILABLE`
- **Final classification:** `CANDIDATE`
- **Codex status suggestion:** `READY_FOR_PYTHON_PROTOTYPE`
- **Candidate ID suggestion:** `QL_CAND_2026-05-03_ElocJ-b_NTs_KELL_10P`

---

## 2. Executive Summary

Bu transcript, Oliver Kell'in swing trading yaklaşımını iki katmanda veriyor:

1. **Market regime / market health layer:** Nasdaq, S&P, Russell, semiconductors, mega-cap leaders, breadth expansion, bear trap, breakaway gap, runaway gap, weekly/daily buy signal, 20-week reclaim/backtest gibi piyasa bağlamı.
2. **Trade execution + risk layer:** 10 prensip üzerinden stop, pozisyon boyutu, plan, P&L ile agresiflik ayarı, extended alım yapmama, earnings gambling kaçınma, strength'e satış ve failed-move hızlı hareket uyarısı.

Bu nedenle video tek bir basit indikatör stratejisi değil; **MTC_V2 için market-regime gate + high-beta liquid growth swing producer + risk/exit management modülü** olarak ayrıştırılmalıdır.

---

## 3. Decision

### Final Verdict: `CANDIDATE`

Bu dosya `CANDIDATE` olarak işlenmeli çünkü:

- Net kodlanabilir market regime kuralları var.
- Net kodlanabilir risk kuralları var.
- Wedge pop, EMA crossback, bull flag, bear trap, higher-low shelf, stage/base breakout gibi teknik setup aileleri var.
- Sistematik prototype'a dönüştürülebilecek entry, gate, sizing ve exit bileşenleri içeriyor.

### Neden doğrudan Pine'a geçilmemeli?

- Terimlerin çoğu discretionary: `wedge pop`, `scum`, `bear trap`, `kicker candle`, `first extension`, `second extension`, `sell into strength`.
- Bu tanımlar önce Python'da kesinleştirilmeli.
- Piyasa rejimi ve çoklu sembol/index kontrolü Pine tarafında request/security ve performans yükü yaratabilir.
- Earnings calendar gibi bazı parçalar OHLCV dışında veri ister.

---

## 4. Extracted Strategy Components

## 4.1 Market Regime Gate — `KELL_MARKET_REGIME_V1`

### Amaç

Sadece piyasa rüzgarı arkadayken long swing trade almak.

### Kaynak Fikirler

- Nasdaq daily + weekly buy signal en iyi ortam.
- S&P ve Russell da daily/weekly buy signal veriyorsa breadth genişliyor.
- Semiconductors market direction için öncü kabul ediliyor.
- Mega-cap leaders, özellikle Apple/Microsoft/Amazon/Nvidia/AVGO/AMD gibi büyük liderlerin yapısı index sağlığı için referans.
- Bear trap + breakaway gap + runaway gap kombinasyonu güçlü regime sinyali.

### Kodlanabilir Proxy

**Index universe:**

- `QQQ` veya Nasdaq proxy
- `SPY` veya S&P 500 proxy
- `IWM` veya Russell 2000 proxy
- `SMH` veya semiconductor proxy

**Daily buy signal proxy:**

- Close > EMA20
- EMA10 > EMA20 veya close EMA10/EMA20 üzerinde güçlü reclaim
- Son N bar içinde pivot / downtrend breakout
- Son N bar içinde unfilled gap veya breakaway gap opsiyonel

**Weekly buy signal proxy:**

- Weekly close > SMA/EMA20 veya 20-week reclaim
- Weekly higher high veya descending wedge/channel breakout
- Weekly close prior resistance üzerinde

**Breadth expansion proxy:**

- QQQ + SPY aynı anda bullish
- IWM son 20 barda relative improvement gösteriyor
- Small/mid-cap growth universe'de breakout sayısı artıyor

### Output

```text
market_regime = OFF / EARLY / CONFIRMED / EXTENDED
```

### MTC_V2 Mapping

- `ENTRY GATES`
- `PortfolioState guard`
- Risk multiplier input'u: regime iyi oldukça position sizing izinleri artar.

---

## 4.2 Wedge Pop / EMA Crossback Producer — `KELL_WEDGE_POP_V1`

### Amaç

High-beta liquid growth stock içinde, geri çekilme sonrası EMA bölgesinden trend yönünde yeniden hızlanan hareketi yakalamak.

### Kodlanabilir Long Setup

**Universe gate:**

- High beta / high ATR growth names
- Sufficient dollar volume
- Theme/leader list içinde
- Fiyat aşırı düşük veya illiquid olmamalı

**Setup context:**

- Önceden güçlü uptrend veya base breakout olmalı.
- Pullback sırasında fiyat EMA10/EMA20/EMA50 çevresinde sıkışmalı.
- Lower high trendline veya mini channel oluşmalı.
- Higher low / tight flag tercih edilir.

**Trigger:**

- Close > pullback trendline
- veya high > prior 1–3 bar high
- veya close EMA10/EMA20 üstüne geri döner
- Volume expansion opsiyonel ama zorunlu değil.

**Invalidation:**

- Stop below recent swing low
- veya below EMA20/EMA50 support
- veya max 3–5% stop bandı dışında trade alma.

### MTC_V2 Mapping

- `SIGNAL PRODUCER`
- `ENTRY GATES`: non-extended, regime, liquidity, theme leader
- `EXIT RULES`: structure stop + sell-into-strength module

---

## 4.3 Bear Trap / Wyckoff Spring / 2B Reversal Module — `KELL_TRAP_REVERSAL_V1`

### Amaç

Major support altına sarkıp geri reclaim eden ve ardından güçlü hareket başlatan yapıları yakalamak.

### Kodlanabilir Long Setup

**Setup:**

- Fiyat önceki destek / range low altına iner.
- Aynı gün veya kısa süre içinde reclaim eder.
- Weekly veya daily close tekrar destek üstündedir.
- Sonrasında 3–4 günlük mini base / tight range oluşabilir.

**Trigger:**

- Mini base high breakout
- veya reclaimed level üstünde follow-through close
- veya gap/kicker candle ile güçlü devam.

**Risk:**

- Stop reclaimed support altı
- veya trap low altı
- max 3–5% stop constraint.

### Not

Bu modül özellikle market regime döndükten sonra işe yarayabilir; tek başına her spring alınmamalı.

---

## 4.4 Stage 1 / Big Base Breakout Watchlist — `KELL_STAGE1_BASE_BREAKOUT_V1`

### Amaç

Uzun süre yatay / düşüşten sonra yeni uptrend başlatabilecek büyüme hisselerini izlemek.

### Kodlanabilir Proxy

- Multi-month veya multi-year base.
- Weekly higher lows.
- Price reclaim 30-week / 40-week MA.
- Major horizontal resistance'a yaklaşma.
- Breakout volume expansion.
- Theme tailwind: AI, crypto, software, cybersecurity, semis, online betting vb.

### Kullanım

Bu modül doğrudan hızlı trade trigger'ı olmaktan çok, watchlist ve regime-aware candidate selection için uygundur.

---

## 5. 10 Trading Principles — System Mapping

| Principle | Sistem Karşılığı | MTC_V2 Katmanı |
|---|---|---|
| Put Risk First | Stop + size + max loss before entry | Position Sizing / Exit Rules |
| Fail to Plan = Plan to Fail | Pre-trade setup definition | Signal/Entry Config |
| Don't Trust Stocks, Trust Stops | Stop discipline | Exit Rules |
| Better Out & Want In | Exit early; re-entry allowed | Position Manager |
| Let P&L Guide Aggression | Progressive exposure | PortfolioState / Sizing |
| Only Price Pays | Opportunity cost guard | Position Manager |
| Sell Into Strength | Profit-taking / extension exit | Exit Rules |
| From Failed Moves Come Fast Moves | Failed breakout reversal guard | Exit Rules / Opp Signal |
| Don't Gamble on Earnings | Earnings risk filter | Entry Gate / Event Calendar |
| Don't Buy Extended Stocks | Non-extended entry gate | Entry Gate |

---

## 6. Risk & Position Management Extraction

### 6.1 Hard Stop Constraint

Transcriptte swing trading bağlamında 3–5% stop bandı vurgulanıyor.

**Prototype rule:**

```text
if abs(entry - stop) / entry > 0.05:
    reject_trade(reason="STOP_TOO_WIDE")
```

Opsiyonel daha sıkı mod:

```text
max_stop_pct = 0.03
```

### 6.2 Position Size by Max Risk

```text
shares = floor((equity * risk_pct) / abs(entry - stop))
```

Örnek:

- Risk: 50 bps = 0.50%
- Stop distance: 5%
- Position size ≈ 10% notional

### 6.3 P&L-Guided Aggression

**Idea:**

- İlk işlemler çalışıyorsa exposure artır.
- İşlemler stop oluyorsa exposure azalt.
- Market reconfirmation varsa yeni pozisyon eklenebilir.
- P&L negatifken leverage artırma.

**Prototype output:**

```text
risk_multiplier =
    0.25 if recent_pnl_bad
    0.50 if regime_early
    1.00 if regime_confirmed and open_trades_working
    1.25 if regime_confirmed and closed_pnl_positive and stops_raised
```

### 6.4 Sell Into Strength

**Candidate exit rules:**

- Weekly second extension / big extension after prior extension.
- High-volume wide-range up day.
- Extended far above EMA10/EMA20.
- Earnings ahead and stock already extended.
- Partial exit at strength; raise stop on remainder.

---

## 7. Potential Candidate Architectures

## Candidate A — `KELL_GROWTH_SWING_WEDGE_POP`

### Classification

`CANDIDATE`

### Core Thesis

High-beta liquid growth leaders, bullish market regime içinde EMA pullback / wedge pop / flag breakout sonrası kısa-orta vadeli momentum verir.

### Required Data

- Daily OHLCV
- Optional weekly OHLCV
- Index OHLCV: QQQ/SPY/IWM/SMH
- Optional earnings calendar
- Optional sector/theme mapping

### Entry Logic Draft

```text
long_setup =
    market_regime in ["EARLY", "CONFIRMED"]
    and stock_close > ema20
    and stock_close > ema50
    and ema10 >= ema20
    and recent_pullback_to_ema_zone
    and tight_range_last_3_to_10_bars
    and breakout_above_pullback_high_or_trendline
    and stop_distance_pct <= max_stop_pct
    and not_extended_from_ema20
```

### Exit Logic Draft

```text
initial_stop = min(recent_swing_low, ema20_buffer)
take_partial_if_R >= 1.5
raise_stop_to_breakeven_after_partial
sell_into_strength_if_extension_signal
exit_if_close_below_structure_stop
avoid_holding_full_size_into_earnings
```

### Expected Edge Source

- Momentum continuation in strong market regimes.
- Better R/R from buying near EMA/support rather than extension.
- Reduced losses via strict stop and exposure control.

---

## Candidate B — `KELL_BEAR_TRAP_BREAKAWAY`

### Classification

`CANDIDATE`

### Core Thesis

Support undercut + reclaim + mini base + breakaway gap/reconfirmation can start new rally legs.

### Entry Logic Draft

```text
bear_trap =
    low < prior_range_low
    and close > prior_range_low

mini_base =
    range_compression_after_trap
    and higher_low

trigger =
    close > mini_base_high
    or gap_up_above_mini_base_high
```

### Best Use

- Market turns after correction.
- Index or leader stock context.
- Works better with accumulation/gap strength confirmation.

---

## Candidate C — `KELL_POSITION_RISK_GUARD`

### Classification

`SALVAGE_MODULE` inside candidate workflow

### Purpose

Not an entry producer; used to control trade aggression and reduce account damage.

### Rules

- Do not add exposure if current positions are not working.
- If open risk is high and weak positions exist, reduce weak names before adding new ones.
- If P&L improves and stops are raised, permit additional exposure.
- If market becomes extended, avoid new buys and focus on raising stops/selling strength.

---

## 8. Backtest Prototype Plan

### Phase 1 — OHLCV-only deterministic prototype

Test only:

- Market regime gate
- Wedge pop / EMA crossback
- Stop distance filter
- Non-extended filter
- Partial at 1.5R / 2R
- Break-even stop after partial
- EMA/structure trailing stop

Avoid:

- Fundamentals
- Earnings calendar
- Theme NLP
- Real-time discretionary labels

### Phase 2 — Add market / theme context

Add:

- QQQ/SPY/IWM/SMH daily+weekly regime
- Relative strength vs QQQ/SPY
- Dollar volume filter
- ATR/beta filter

### Phase 3 — Add event risk

Add:

- Earnings calendar
- No new buys N days before earnings
- Reduce or exit before earnings unless explicit test mode allows holding.

### Phase 4 — Cross-market validation

Test on:

- US high-beta growth stocks
- Large-cap tech
- Semiconductors
- Crypto-related equities
- ETFs as baseline
- Avoid low-liquidity names initially.

---

## 9. Parameter Draft

```yaml
strategy_id: KELL_GROWTH_SWING_WEDGE_POP_V1
direction: long_only
timeframe: daily
higher_timeframe: weekly

market_regime:
  symbols: [QQQ, SPY, IWM, SMH]
  require_primary_index_bullish: true
  require_weekly_buy_signal: true
  allow_early_mode: true

entry:
  ema_fast: 10
  ema_mid: 20
  ema_slow: 50
  pullback_lookback: 3-15
  tight_range_lookback: 3-10
  breakout_lookback: 1-5
  max_extension_from_ema20_pct: 8
  max_stop_pct: 5
  preferred_stop_pct: 3

risk:
  risk_per_trade_bps: 25-50
  max_open_portfolio_risk_pct: 3-6
  pnl_aggression_enabled: true
  max_new_entries_when_regime_extended: 0

exits:
  initial_stop: recent_swing_low_or_ema20_buffer
  partial_1_R: 1.5
  partial_1_qty_pct: 25-50
  breakeven_after_partial: true
  trailing_stop: ema10_or_ema20_or_structure
  sell_into_strength_enabled: true
  earnings_exit_enabled: true
```

---

## 10. MTC_V2 Integration Notes

### Do Not Touch Yet

- `01_PINE/MTC_V2.pine`
- Production Python runner
- Existing optimization loop
- Existing parity harness

### Future Integration Candidate

**Best first integration location:**

1. Python research prototype only.
2. If robust, add as isolated producer:
   - `producer_kell_wedge_pop_v1`
3. Add regime as optional `ENTRY GATE`, not hardwired producer dependency.
4. Add P&L-guided aggression as optional `Position Sizing / PortfolioState` module.
5. Add sell-into-strength as optional exit rule.

### Parity Risk

This approach uses multi-symbol market regime and subjective structure labels. Pine parity risk is high unless every label is converted into deterministic OHLCV definitions.

---

## 11. Red Flags / Caution

- Promotional webinar content includes product/swing report section.
- Many labels are discretionary and require strict definitions before code.
- Examples are selected winners and current-market commentary, not a statistical proof.
- Earnings handling requires data outside normal OHLCV.
- Theme selection can become look-ahead biased if not implemented carefully.
- “High-beta growth” universe must be defined from data available at the time, not from future winners.

---

## 12. Trader Wiki Value

Even if strategy testing fails, this video has strong Trader Wiki value under:

- `04_SYSTEM_DEVELOPMENT`
- `05_BACKTESTING_AND_OPTIMIZATION`
- `01_RISK_MANAGEMENT`

Potential wiki note themes:

- Plan before market open.
- P&L should guide aggression.
- Price action overrides thesis.
- Strength selling reduces forced weakness selling.
- Market environment determines whether growth swing setups deserve full size.

---

## 13. Final Output Summary

### Files that would be created in repo later

```text
02_RESEARCH/YOUTUBE_STRATEGY_INTAKE/...
  intake_report.md

03_CANDIDATES/QL_CAND_2026-05-03_ElocJ-b_NTs_KELL_10P/
  candidate_summary.md
  prototype_plan.md
  parameter_draft.yaml
```

### Files not touched

```text
01_PINE/MTC_V2.pine
production Python runner files
existing backtest/optimization output
existing data bundles
existing registries
```

### Next Action

**Recommended next step:** Create isolated Python prototype for `KELL_GROWTH_SWING_WEDGE_POP_V1` using daily OHLCV + index regime data. Do not implement in Pine until Python prototype shows non-random, cross-symbol performance and the discretionary terms are fully formalized.

---

## 14. Final Classification Block

```text
classification: CANDIDATE
codex_status: READY_FOR_PYTHON_PROTOTYPE
candidate_type: MARKET_REGIME_PLUS_GROWTH_SWING_PRODUCER
primary_modules:
  - KELL_MARKET_REGIME_V1
  - KELL_WEDGE_POP_V1
  - KELL_TRAP_REVERSAL_V1
  - KELL_POSITION_RISK_GUARD
wiki_value: HIGH
duplicate: NOT_DUPLICATE_IN_CURRENT_SESSION
repo_duplicate_check: NOT_VERIFIED_REPO_NOT_AVAILABLE
channel_quality_check: NOT_VERIFIED_REPO_NOT_AVAILABLE
pine_touched: NO
python_runner_touched: NO
backtest_run: NO
optimization_run: NO
```
