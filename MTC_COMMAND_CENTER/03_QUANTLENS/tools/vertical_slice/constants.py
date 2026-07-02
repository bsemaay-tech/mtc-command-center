"""Immutable constants for the STG002 SYSTEM_TEST_ONLY vertical slice."""

from pathlib import Path


BANNER = "SYSTEM_TEST_ONLY / NOT STRATEGY_APPROVED / NO REAL MONEY"

CANDIDATE_ID = "QL_ALPHA_LINK_8EMA_1H"
ENGINE_STRATEGY_ID = "QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL"
SYMBOL = "LINKUSDT"
TIMEFRAME = "1h"
EXCHANGE = "BINANCE"

SCHEMA_ID = "mtc.signal/v1"
STRATEGY_VERSION = "system-test-stg002-v1"
QTY_MODEL = "none"
RISK_REF = "system_test_replay"

ALLOWED_ENVIRONMENTS = ("paper",)
FORBIDDEN_LABELS = ("live", "testnet", "broker", "TradingView", "WunderTrading")

TOOLS_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[4]
STG002_STRATEGY_DIR = (
    REPO_ROOT
    / "MTC_COMMAND_CENTER"
    / "03_QUANTLENS"
    / "strategies"
    / "STG002_ql_alpha_link_8ema_1h"
)
STG002_TRADES_CSV = STG002_STRATEGY_DIR / "QL_ALPHA_LINK_8EMA_1H_trades.csv"
STG002_SIGNALS_CSV = STG002_STRATEGY_DIR / "QL_ALPHA_LINK_8EMA_1H_signals.csv"
STG002_PRODUCER_SPEC = STG002_STRATEGY_DIR / "producer_spec.json"
