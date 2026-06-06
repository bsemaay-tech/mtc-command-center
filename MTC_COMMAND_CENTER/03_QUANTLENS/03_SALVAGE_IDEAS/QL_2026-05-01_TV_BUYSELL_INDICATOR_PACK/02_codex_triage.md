# Codex Triage

## Executive Triage
Status: SALVAGE_ONLY → Q Trend: FILTER_OVERLAY (2026-06-01 DeepSeek V4 Pro)

The transcript is a curated list of five TradingView buy/sell label indicators. It does not provide a complete codable trading strategy. The only safe output is a salvage note for future research.

## 2026-06-01 — Q Trend Backtest Evidence (DeepSeek V4 Pro)

Q Trend (Tosenko) Pine kodu ve 2 transcript ile split edildi, Python implementasyonu yapıldı, multi-symbol backtest çalıştırıldı.

### Backtest Sonuçları

| Varyant | Sembol | Lockbox | PF | DD | Trades | Sonuç |
|---------|--------|---------|-----|------|--------|-------|
| Long (tüm) | ETHUSDT | +110.7% | 1.28 | -50.8% | 180 | FAIL |
| Long (tüm) | BTCUSDT | -27.4% | 0.78 | -37.9% | 91 | FAIL |
| Short | SOLUSDT | +70.8% | 1.19 | -63.6% | 215 | FAIL |
| Short | BTCUSDT | +25.4% | 1.27 | -26.1% | 67 | FAIL |
| Strong+ADX | SOLUSDT | +9.2% | 1.24 | -14.1% | 23 | INSUF |
| Strong+ADX | LINKUSDT | +4.6% | 1.31 | -14.5% | 9 | INSUF |

### Karar: FILTER_OVERLAY
- Q Trend standalone strateji olarak kullanılamaz — cross-fold/cross-symbol tutarlılık yok
- **Rol: confirmation / guard filter** — mevcut stratejilere ek filtre olarak bağlanabilir
- Q Trend `change_up` sinyali trend yönü filtresi, `strong_buy` kalite filtresi olarak kullanılabilir
- Pine kodu: `00_INBOX_REPORTS/1 Haziran/Stg Q Trend/Q Trend.pine`
- Python implementasyonu: `overnight_v2_runner.py` → `_qtrend_signal()` + `_compute_adx()`

## STOP Condition Check
- Closed source dependency: medium risk because the workflow depends on external TradingView community indicators.
- Repaint/lookahead: unknown because each script must be audited separately.
- Strategy completeness: insufficient.
- MTC_V2 compatibility: not directly actionable.
- Marketing risk: high, due "most accurate buy sell signals ever" framing.

## Strategy Completeness Check
- Entry: indicator labels only, no full setup definition.
- Exit: absent.
- Stop: absent.
- Target: absent.
- Risk: generic 1% rule mention only.
- Market/timeframe: absent.

## MTC_V2 Compatibility
No direct integration recommended. Individual ideas could later be mapped as confirmations or guards if their formulas are open and reproducible.

## Salvageable Ideas
- Q Trend strong signals → **FILTER_OVERLAY** (backtest: standalone edge yok, confirmation/guard rolüne uygun)
- QQE/RSI smoothing as a momentum filter concept.
- UT Bot ATR trailing logic as a known research family.
- Pivot Point SuperTrend as a reversal/swing confirmation concept.
- Lorentzian classifier as a watchlist-only ML-style signal source, not parity-ready.
- Trading journal and 1% risk reminder as process notes.

## Final Status
SALVAGE_ONLY. Q Trend → FILTER_OVERLAY.

## Next Action
Do not create prototype code for standalone strategy. Q Trend: mevcut stratejilere confirmation/guard filter olarak entegre edilebilir. Diğer 4 indikatör için aynı süreç tekrarlanmadıkça FILTER_OVERLAY sınıflandırması yapılmaz.
