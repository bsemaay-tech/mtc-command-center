# QL_2026-05-01_SWING_1H_DUAL_RSI_60_40_PULLBACK — Deterministic Spec

- **Status**: PROMOTED TO PROTOTYPE
- **Author**: Antigravity Technical Architect

## 1. Core Concept & Formula
Multi-timeframe trend-following pullback strategy using Daily RSI as trend filter and 1-Hour RSI as local pullback execution gate.

## 2. Strict Mechanical Rules

### A. Higher Timeframe (HTF) Daily Trend Filter
* **Calculation**: `RSI(7)` calculated on Daily completed closes.
* **Alignment Rule**: To prevent lookahead bias, any 1-Hour bar on calendar day $D$ can ONLY reference the completed Daily `RSI(7)` value of day $D-1$ (fully closed at UTC 00:00).
* **Regime Definition**:
  * **Bull Regime (Long Only)**: Daily `RSI(7) > 60`
  * **Bear Regime (Short Only)**: Daily `RSI(7) < 40`
  * **Sideways (No-Trade)**: Daily `RSI(7)` is between `40` and `60` inclusive.

### B. Lower Timeframe (LTF) 1-Hour Entry Logic
* **Calculation**: `RSI(7)` on the 1-Hour chart.
* **Long Entry Trigger**:
  1. HTF Trend Filter must be in a **Bull Regime**.
  2. 1-Hour `RSI(7)` must fall below `40` (Entering the pullback state).
  3. **Pullback Memory**: The pullback state remains active for a maximum of **12 bars (12 hours)**. If the recovery cross does not occur within 12 hours, the setup is discarded.
  4. **Trigger**: 1-Hour `RSI(7)` crosses back above `40`.
  5. **Execution**: Buy on the **open** of the next 1-Hour bar immediately following the crossing bar.
* **Short Entry Trigger**:
  1. HTF Trend Filter must be in a **Bear Regime**.
  2. 1-Hour `RSI(7)` must rise above `60`.
  3. **Pullback Memory**: Pullback state active for max **12 bars (12 hours)**.
  4. **Trigger**: 1-Hour `RSI(7)` crosses back below `60`.
  5. **Execution**: Sell short on the **open** of the next 1-Hour bar.

### C. Stop Loss & Take Profit (Risk Management)
* **Long Stop Loss**: Minimum `low` of the last 10 closed 1-Hour bars preceding the entry bar (Lookahead-free swing stop).
* **Short Stop Loss**: Maximum `high` of the last 10 closed 1-Hour bars preceding the entry bar.
* **Take Profit**: Fixed `2.0R` (Take Profit distance is exactly $2.0 \times$ Stop Loss distance).
* **Large-Candle Filter**: If the Stop Loss distance (Entry - Stop Loss) is greater than $2.5 \times ATR(14)$, discard the trade (Avoids chasing momentum on volatile breakout candles).

## 3. Pilot Sandbox Parameters
* **Target Universe**: `BTCUSDT`, `ETHUSDT`, `SOLUSDT` (Binance Futures OHLCV).
* **Timeframes**: 1-Hour entries with Daily trend filter.
* **Trading Costs**: 8.0 BPS round trip (slippage + fees).
