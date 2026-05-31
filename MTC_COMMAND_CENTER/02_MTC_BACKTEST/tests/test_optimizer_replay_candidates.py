import pytest
import json
import pandas as pd
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.optimizer_v0 import replay_candidates

# Mock TrialResult to avoid running full backtest engine
class MockTrialResult:
    def __init__(self, idx, status="OK"):
        self.idx = idx
        self.status = status
        self.net_profit = 100.0 * idx
        self.max_dd_pct = 5.0 * idx
        self.total_trades = 10
        self.win_rate = 0.6
        self.profit_factor = 2.0
        self.score = 50.0
        self.prune_reason = None
        self.runtime_s = 0.1
        self.min_trades_threshold = 5
        self.max_dd_threshold_pct = 20.0

def test_load_candidate_files(tmp_path):
    (tmp_path / "a.json").touch()
    (tmp_path / "b.json").touch()
    (tmp_path / "c.txt").touch()
    
    files = replay_candidates.load_candidate_files(tmp_path)
    assert len(files) == 2
    assert files[0].name == "a.json"
    assert files[1].name == "b.json"

@patch("src.optimizer_v0.replay_candidates.load_data_for_replay")
@patch("src.optimizer_v0.replay_candidates.run_single_trial")
@patch("src.optimizer_v0.replay_candidates._worker_init")
def test_run_replay_batch(mock_init, mock_run, mock_load, tmp_path):
    # Setup mocks
    # return: df, base_config, warmup_bars, eval_start, eval_end
    mock_conf = MagicMock()
    mock_conf.model_dump.return_value = {}
    mock_load.return_value = (MagicMock(), mock_conf, 100, None, None)
    
    mock_run.side_effect = [
        MockTrialResult(1, "OK"),
        MockTrialResult(2, "PRUNED")
    ]
    
    # Setup candidate files
    c1 = tmp_path / "cand_1.json"
    c2 = tmp_path / "cand_2.json"
    
    c1.write_text(json.dumps({"params": {"p": 1}}))
    c2.write_text(json.dumps({"params": {"p": 2}}))
    
    out_csv = tmp_path / "replay.csv"
    
    # Run
    replay_candidates.run_replay_batch(
        case_path=Path("dummy_case.json"),
        candidate_files=[c1, c2],
        out_csv=out_csv
    )
    
    # Verify calls
    assert mock_run.call_count == 2
    mock_conf.model_dump.assert_called_once_with(by_alias=True)
    
    # Verify CSV
    assert out_csv.exists()
    df = pd.read_csv(out_csv)
    
    assert len(df) == 2
    # Check stable sort order of candidates
    assert df.iloc[0]["candidate_file"] == "cand_1.json"
    assert df.iloc[0]["status"] == "OK"
    assert df.iloc[0]["net_profit"] == 100.0
    
    assert df.iloc[1]["candidate_file"] == "cand_2.json"
    assert df.iloc[1]["status"] == "PRUNED"
    assert df.iloc[1]["net_profit"] == 200.0
