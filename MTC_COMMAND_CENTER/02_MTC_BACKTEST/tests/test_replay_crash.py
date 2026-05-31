import pytest
from pathlib import Path
import json
import pandas as pd
from src.optimizer_v0 import replay_candidates
from src.config.schema import TradeRecord

# Ensure we use a real case that exists
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CASE_PATH = PROJECT_ROOT / "mtc_backtest" / "configs" / "cases" / "full_jul2025_jan2026_parity.json"

def test_load_data_for_replay_crash():
    """Regression test for NameError: timezone not defined."""
    if not CASE_PATH.exists():
        pytest.skip(f"Case file not found: {CASE_PATH}")
        
    try:
        # This triggers load_data_for_replay -> _parse_dt -> timezone.utc
        replay_candidates.load_data_for_replay(CASE_PATH)
    except NameError as e:
        pytest.fail(f"Caught expected NameError (regression): {e}")
    except FileNotFoundError:
        # If dataset missing, that's fine for this test, as long as it didn't crash on NameError first
        # But load_data_for_replay checks dataset existence.
        # We just want to ensure it passes the timezone usage.
        pass
    except Exception as e:
        # Other errors (like missing dataset) are fine, as long as it's not NameError
        if "timezone" in str(e):
             pytest.fail(f"Caught timezone error: {e}")
        print(f"Caught other error: {e}")


def test_load_data_for_replay_uses_end_of_day_for_date_only_end(tmp_path):
    csv_path = tmp_path / "sample.csv"
    case_path = tmp_path / "case.json"

    # Bar on end date at noon UTC should be included when end_date is date-only.
    df = pd.DataFrame(
        [
            {"timestamp": "2025-01-01T00:00:00Z", "open": 1, "high": 1, "low": 1, "close": 1, "volume": 1},
            {"timestamp": "2025-01-02T12:00:00Z", "open": 1, "high": 1, "low": 1, "close": 1, "volume": 1},
            {"timestamp": "2025-01-03T00:00:00Z", "open": 1, "high": 1, "low": 1, "close": 1, "volume": 1},
        ]
    )
    df.to_csv(csv_path, index=False)

    case_payload = {
        "dataset": str(csv_path),
        "start_date": "2025-01-01",
        "end_date": "2025-01-02",
        "preroll_days": 0,
        "warmup_bars": 0,
        "config": {},
    }
    case_path.write_text(json.dumps(case_payload), encoding="utf-8")

    filtered, _, _, _, eval_end = replay_candidates.load_data_for_replay(case_path)
    assert len(filtered) == 2
    assert eval_end.hour == 23 and eval_end.minute == 59


def test_trade_record_accepts_engine_exit_reasons():
    row = dict(
        trade_id=1,
        direction="long",
        entry_bar=0,
        entry_time="2025-01-01T00:00:00Z",
        entry_price=100.0,
        exit_bar=1,
        exit_time="2025-01-01T00:15:00Z",
        exit_price=101.0,
        quantity=1.0,
        pnl=1.0,
        pnl_pct=1.0,
    )
    TradeRecord(**{**row, "exit_reason": "BE"})
    TradeRecord(**{**row, "exit_reason": "EVAL_START_FLATTEN"})
