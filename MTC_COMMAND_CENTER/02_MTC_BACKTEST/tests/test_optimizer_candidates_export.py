import pytest
import json
from pathlib import Path
from src.optimizer_v0 import candidates

def test_select_candidates_ok_only():
    payload = {
        "items": [
            {"status": "OK", "net_profit": 100, "dd_pct": 5, "param_key": "A"},
            {"status": "PRUNED", "net_profit": 50, "dd_pct": 2, "param_key": "B"},
            {"status": "OK", "net_profit": 80, "dd_pct": 10, "param_key": "C"},
        ]
    }
    
    # OK only
    sel = candidates.select_candidates(payload, top_k=10, include_pruned=False)
    assert len(sel) == 2
    assert sel[0]["param_key"] == "A" # Sort: (5, -100) < (10, -80)
    
    # Include Pruned
    sel_all = candidates.select_candidates(payload, top_k=10, include_pruned=True)
    assert len(sel_all) == 3
    # Sort order:
    # B: (2, -50, B)
    # A: (5, -100, A)
    # C: (10, -80, C)
    assert sel_all[0]["param_key"] == "B"
    assert sel_all[1]["param_key"] == "A"

def test_export_candidates_writes_files_deterministic(tmp_path):
    outdir = tmp_path / "cands"
    payload_meta = {"run_id": "test-run"}
    
    cands = [
        {"param_key": "p1", "net_profit": 100, "dd_pct": 5, "params": {"a": 1}},
        {"param_key": "p2", "net_profit": 200, "dd_pct": 10, "params": {"a": 2}},
    ]
    
    written = candidates.write_candidates(cands, payload_meta, outdir, "testcand", overwrite=False)
    
    assert len(written) == 2
    assert outdir.exists()
    
    # Check file 1
    # Rank 1: p1 (dd 5)
    f1 = written[0]
    content1 = json.loads(f1.read_text("utf-8"))
    assert content1["meta"]["rank"] == 1
    assert content1["meta"]["param_key"] == "p1"
    assert content1["params"]["a"] == 1
    assert "testcand_001" in f1.name

def test_overwrite_guardrail(tmp_path):
    outdir = tmp_path / "guard"
    outdir.mkdir()
    
    cands = [{"param_key": "p1", "net_profit": 10, "dd_pct": 1}]
    payload_meta = {}
    
    # Write once
    candidates.write_candidates(cands, payload_meta, outdir, "g", False)
    
    # Write again - fail
    with pytest.raises(FileExistsError):
        candidates.write_candidates(cands, payload_meta, outdir, "g", False)
        
    # Write again with overwrite - OK
    candidates.write_candidates(cands, payload_meta, outdir, "g", True)
