# MTC Data Validation Report
Generated: 2026-03-08T17:07:33Z

## Summary

| Symbol | TF | Bars | Status |
|--------|----|------|--------|
| BTCUSDT | 1d | 2,808 | [WARN] WARN |
| BTCUSDT | 4h | 16,840 | [WARN] WARN |
| BTCUSDT | 2h | 33,663 | [WARN] WARN |
| BTCUSDT | 1h | 67,309 | [WARN] WARN |
| BTCUSDT | 15m | 269,199 | [WARN] WARN |
| BTCUSDT | 5m | 807,586 | [WARN] WARN |
| ETHUSDT | 1d | 2,624 | [WARN] WARN |
| ETHUSDT | 15m | 251,607 | [WARN] WARN |
| ETHUSDT | 1h | 62,910 | [WARN] WARN |
| ETHUSDT | 4h | 15,738 | [WARN] WARN |
| BTCUSDT.P | 15m | 3,072 | [OK] OK |

---
## BTCUSDT / 1d
- **Path**: `C:/LAB/tradingview-lab/110_/data/processed/binance/BTCUSDT/1d.parquet`
- **Bars**: 2,808
- **Range**: 2018-07-01 00:00:00+00:00 → 2026-03-08 00:00:00+00:00
- **Monotonic**: [OK] OK — Index is monotonically increasing.
- **Duplicates**: [OK] OK — No duplicate timestamps.
- **UTC**: [OK] OK — Timezone confirmed UTC (UTC).
- **Gaps**: [WARN] WARN — 2807 gap(s) between 1h-24h. Largest: 1 days 00:00:00 (expected 1 days 00:00:00). Likely exchange maintenance (Binance can have ~10-12h downtime).
- **OHLC Sanity**: [OK] OK — OHLC sanity: high>=max(O,C), low<=min(O,C), volume>=0.

**Overall Status: [WARN] WARN**

---
## BTCUSDT / 4h
- **Path**: `C:/LAB/tradingview-lab/110_/data/processed/binance/BTCUSDT/4h.parquet`
- **Bars**: 16,840
- **Range**: 2018-07-01 00:00:00+00:00 → 2026-03-08 16:00:00+00:00
- **Monotonic**: [OK] OK — Index is monotonically increasing.
- **Duplicates**: [OK] OK — No duplicate timestamps.
- **UTC**: [OK] OK — Timezone confirmed UTC (UTC).
- **Gaps**: [WARN] WARN — 16839 gap(s) between 1h-24h. Largest: 0 days 12:00:00 (expected 0 days 04:00:00). Likely exchange maintenance (Binance can have ~10-12h downtime).
- **OHLC Sanity**: [OK] OK — OHLC sanity: high>=max(O,C), low<=min(O,C), volume>=0.

**Overall Status: [WARN] WARN**

---
## BTCUSDT / 2h
- **Path**: `C:/LAB/tradingview-lab/110_/data/processed/binance/BTCUSDT/2h.parquet`
- **Bars**: 33,663
- **Range**: 2018-07-01 00:00:00+00:00 → 2026-03-08 16:00:00+00:00
- **Monotonic**: [OK] OK — Index is monotonically increasing.
- **Duplicates**: [OK] OK — No duplicate timestamps.
- **UTC**: [OK] OK — Timezone confirmed UTC (UTC).
- **Gaps**: [WARN] WARN — 33662 gap(s) between 1h-24h. Largest: 0 days 10:00:00 (expected 0 days 02:00:00). Likely exchange maintenance (Binance can have ~10-12h downtime).
- **OHLC Sanity**: [OK] OK — OHLC sanity: high>=max(O,C), low<=min(O,C), volume>=0.

**Overall Status: [WARN] WARN**

---
## BTCUSDT / 1h
- **Path**: `C:/LAB/tradingview-lab/110_/data/processed/binance/BTCUSDT/1h.parquet`
- **Bars**: 67,309
- **Range**: 2018-07-01 00:00:00+00:00 → 2026-03-08 17:00:00+00:00
- **Monotonic**: [OK] OK — Index is monotonically increasing.
- **Duplicates**: [OK] OK — No duplicate timestamps.
- **UTC**: [OK] OK — Timezone confirmed UTC (UTC).
- **Gaps**: [WARN] WARN — 23 gap(s) between 1h-24h. Largest: 0 days 11:00:00 (expected 0 days 01:00:00). Likely exchange maintenance (Binance can have ~10-12h downtime).
- **OHLC Sanity**: [OK] OK — OHLC sanity: high>=max(O,C), low<=min(O,C), volume>=0.

**Overall Status: [WARN] WARN**

---
## BTCUSDT / 15m
- **Path**: `C:/LAB/tradingview-lab/110_/data/processed/binance/BTCUSDT/15m.parquet`
- **Bars**: 269,199
- **Range**: 2018-07-01 00:00:00+00:00 → 2026-03-08 17:00:00+00:00
- **Monotonic**: [OK] OK — Index is monotonically increasing.
- **Duplicates**: [OK] OK — No duplicate timestamps.
- **UTC**: [OK] OK — Timezone confirmed UTC (UTC).
- **Gaps**: [WARN] WARN — 24 gap(s) between 1h-24h. Largest: 0 days 10:15:00 (expected 0 days 00:15:00). Likely exchange maintenance (Binance can have ~10-12h downtime).
- **OHLC Sanity**: [OK] OK — OHLC sanity: high>=max(O,C), low<=min(O,C), volume>=0.

**Overall Status: [WARN] WARN**

---
## BTCUSDT / 5m
- **Path**: `C:/LAB/tradingview-lab/110_/data/processed/binance/BTCUSDT/5m.parquet`
- **Bars**: 807,586
- **Range**: 2018-07-01 00:00:00+00:00 → 2026-03-08 17:00:00+00:00
- **Monotonic**: [OK] OK — Index is monotonically increasing.
- **Duplicates**: [OK] OK — No duplicate timestamps.
- **UTC**: [OK] OK — Timezone confirmed UTC (UTC).
- **Gaps**: [WARN] WARN — 24 gap(s) between 1h-24h. Largest: 0 days 10:05:00 (expected 0 days 00:05:00). Likely exchange maintenance (Binance can have ~10-12h downtime).
- **OHLC Sanity**: [OK] OK — OHLC sanity: high>=max(O,C), low<=min(O,C), volume>=0.

**Overall Status: [WARN] WARN**

---
## ETHUSDT / 1d
- **Path**: `C:/LAB/tradingview-lab/110_/data/processed/binance/ETHUSDT/1d.parquet`
- **Bars**: 2,624
- **Range**: 2019-01-01 00:00:00+00:00 → 2026-03-08 00:00:00+00:00
- **Monotonic**: [OK] OK — Index is monotonically increasing.
- **Duplicates**: [OK] OK — No duplicate timestamps.
- **UTC**: [OK] OK — Timezone confirmed UTC (UTC).
- **Gaps**: [WARN] WARN — 2623 gap(s) between 1h-24h. Largest: 1 days 00:00:00 (expected 1 days 00:00:00). Likely exchange maintenance (Binance can have ~10-12h downtime).
- **OHLC Sanity**: [OK] OK — OHLC sanity: high>=max(O,C), low<=min(O,C), volume>=0.

**Overall Status: [WARN] WARN**

---
## ETHUSDT / 15m
- **Path**: `C:/LAB/tradingview-lab/110_/data/processed/binance/ETHUSDT/15m.parquet`
- **Bars**: 251,607
- **Range**: 2019-01-01 00:00:00+00:00 → 2026-03-08 17:00:00+00:00
- **Monotonic**: [OK] OK — Index is monotonically increasing.
- **Duplicates**: [OK] OK — No duplicate timestamps.
- **UTC**: [OK] OK — Timezone confirmed UTC (UTC).
- **Gaps**: [WARN] WARN — 21 gap(s) between 1h-24h. Largest: 0 days 10:15:00 (expected 0 days 00:15:00). Likely exchange maintenance (Binance can have ~10-12h downtime).
- **OHLC Sanity**: [OK] OK — OHLC sanity: high>=max(O,C), low<=min(O,C), volume>=0.

**Overall Status: [WARN] WARN**

---
## ETHUSDT / 1h
- **Path**: `C:/LAB/tradingview-lab/110_/data/processed/binance/ETHUSDT/1h.parquet`
- **Bars**: 62,910
- **Range**: 2019-01-01 00:00:00+00:00 → 2026-03-08 17:00:00+00:00
- **Monotonic**: [OK] OK — Index is monotonically increasing.
- **Duplicates**: [OK] OK — No duplicate timestamps.
- **UTC**: [OK] OK — Timezone confirmed UTC (UTC).
- **Gaps**: [WARN] WARN — 20 gap(s) between 1h-24h. Largest: 0 days 11:00:00 (expected 0 days 01:00:00). Likely exchange maintenance (Binance can have ~10-12h downtime).
- **OHLC Sanity**: [OK] OK — OHLC sanity: high>=max(O,C), low<=min(O,C), volume>=0.

**Overall Status: [WARN] WARN**

---
## ETHUSDT / 4h
- **Path**: `C:/LAB/tradingview-lab/110_/data/processed/binance/ETHUSDT/4h.parquet`
- **Bars**: 15,738
- **Range**: 2019-01-01 00:00:00+00:00 → 2026-03-08 16:00:00+00:00
- **Monotonic**: [OK] OK — Index is monotonically increasing.
- **Duplicates**: [OK] OK — No duplicate timestamps.
- **UTC**: [OK] OK — Timezone confirmed UTC (UTC).
- **Gaps**: [WARN] WARN — 15737 gap(s) between 1h-24h. Largest: 0 days 12:00:00 (expected 0 days 04:00:00). Likely exchange maintenance (Binance can have ~10-12h downtime).
- **OHLC Sanity**: [OK] OK — OHLC sanity: high>=max(O,C), low<=min(O,C), volume>=0.

**Overall Status: [WARN] WARN**

---
## BTCUSDT.P / 15m
- **Path**: `C:/LAB/tradingview-lab/110_/data/processed/binance_usdm/BTCUSDT.P/15m.parquet`
- **Bars**: 3,072
- **Range**: 2025-12-01 00:00:00+00:00 → 2026-01-01 23:45:00+00:00
- **Monotonic**: [OK] OK — Index is monotonically increasing.
- **Duplicates**: [OK] OK — No duplicate timestamps.
- **UTC**: [OK] OK — Timezone confirmed UTC (UTC).
- **Gaps**: [OK] OK — No significant gaps (expected interval: 0 days 00:15:00).
- **OHLC Sanity**: [OK] OK — OHLC sanity: high>=max(O,C), low<=min(O,C), volume>=0.

**Overall Status: [OK] OK**
