# MTC Python Backtest & Optimization System

**Version:** 1.0.0 | **Status:** MVP Ready

A local-only Windows 11 application that ports the TradingView MASTER_TEMPLATE_CORE (MTC) Pine Script v6 strategy to Python for backtesting and parameter optimization.

## 🚀 Quick Start

### Windows (Double-click)
```batch
run_app.bat
```

### Manual
```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

The app will open at **http://localhost:8501**

---

## 📁 Project Structure

```
mtc_backtest/
├── app.py                  # Streamlit entry point
├── run_app.bat             # Windows launcher
├── requirements.txt        # Dependencies
├── src/
│   ├── config/             # Configuration & defaults
│   ├── data/               # Data download & caching
│   ├── engine/             # Backtest engine & indicators
│   ├── modules/
│   │   ├── signals/        # Signal plugins (Supertrend)
│   │   ├── filters/        # Filters (MA, Volume, ATR)
│   │   └── risk/           # Risk (SL, TP, Sizing)
│   ├── optimize/           # Optuna optimization
│   └── ui/                 # Streamlit UI pages
├── data/                   # Downloaded datasets
├── exports/                # Backtest results
└── logs/                   # Application logs
```

---

## 🔧 Features

### ✅ Implemented (MVP)
- **Data Layer**: Download OHLCV from Binance USDT-M Futures via ccxt
- **Signal Modules**: Supertrend with Heikin Ashi support
- **Filter Modules**: MA Filter, Volume Filter, ATR Volatility Floor
- **Risk Engine**: All SL modes (ATR, %, Swing), Multi-TP, Break-Even, Trailing
- **Backtest Engine**: Bar-by-bar simulation matching MTC logic
- **Metrics**: 25+ performance metrics (Sharpe, Sortino, Profit Factor, etc.)
- **Optimization**: Optuna TPE sampler with configurable objectives
- **UI**: Streamlit dashboard with download, backtest, optimize pages

### 🔜 Coming Soon
- Range Filter Hybrid signal module
- HTF Trend Filter
- Full parity export tools
- Pine debug script generator

---

## 📊 Usage

### 1. Download Data
1. Go to "📥 Data Download"
2. Enter symbol (e.g., `BTCUSDT`), timeframe (e.g., `15m`)
3. Select date range
4. Click "Download"

### 2. Run Backtest
1. Go to "🔬 Backtest"
2. Select dataset
3. Configure parameters (or use defaults)
4. Click "Run Backtest"
5. View equity curve, metrics, and trades

### 3. Optimize Parameters
1. Go to "⚡ Optimize"
2. Select parameters to optimize
3. Set ranges and number of trials
4. Click "Run Optimization"
5. Copy the Pine Script preset to TradingView

---

## ⚙️ Configuration

Default parameters match `MASTER_TEMPLATE_CORE.pine` v2.2.0:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `signal_mode` | Supertrend | Signal generation method |
| `st_atr_len` | 21 | Supertrend ATR length |
| `st_factor` | 4.0 | Supertrend factor |
| `risk_long_pct` | 4.0% | Risk per long trade |
| `fallback_qty_pct` | 5.0% | Fallback position size when SL is OFF |
| `risk_equity_mode` | Initial | Risk sizing equity source (Initial/Realized) |
| `use_notional_hard_assert` | False | Hard skip entry if total notional still exceeds cap |
| `signal_mode_max_entries` | 1 | Max entries in Signal mode |
| `max_pyramid_positions` | 1 | Max same-direction pyramid positions |
| `use_volume_filter` | False | Volume participation filter default |
| `use_atr_vol_filter` | False | ATR volatility floor default |
| `use_eq_curve_guard` | False | Equity curve guard default |
| `sl_mode` | ATR | Stop loss mode |
| `sl_atr_mult` | 4.0 | SL ATR multiplier |
| `use_multi_tp` | True | Enable TP1/TP2 |
| `use_trailing` | True | Enable trailing stop |

---

## 📋 Requirements

- Python 3.11+
- Windows 11 (tested)
- Dependencies: ccxt, pandas, numpy, streamlit, optuna, plotly

---

## 📝 License

For personal/educational use only. Not for redistribution.

---

## 🔗 Related

- [MASTER_TEMPLATE_CORE.pine](../00_MASTER_TEMPLATE/)
- [Pine Module Pack v2](../20_MODULES_REUSABLE/)
