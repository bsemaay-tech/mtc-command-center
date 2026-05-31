import json
from pathlib import Path

from src.optimizer_v0.search import TrialResult
from src.optimizer_v0.store_sqlite import SQLiteStore
from src.ui.run_history import (
    compare_runs,
    list_result_artifacts,
    load_run_history,
    read_artifact_preview,
    resolve_db_path,
    summarize_run,
)


def _mk_trial(idx: int, score: float, status: str = "OK", params_key_val: float = 1.0) -> TrialResult:
    return TrialResult(
        idx=idx,
        params={"x": params_key_val},
        score=score,
        net_profit=10.0,
        max_dd_pct=5.0,
        total_trades=20,
        win_rate=40.0,
        profit_factor=1.2,
        runtime_s=0.1,
        status=status,
    )


def test_run_history_summary_and_compare(tmp_path: Path):
    db = tmp_path / "results.db"
    store = SQLiteStore(db)
    run_a = store.create_run("case_a.json", "random", 42, 5, 1, 10, 40.0)
    run_b = store.create_run("case_b.json", "random", 43, 5, 1, 10, 40.0)
    store.upsert_trial(run_a, _mk_trial(0, 1.0, params_key_val=1.0))
    store.upsert_trial(run_a, _mk_trial(1, 2.0, params_key_val=2.0))
    store.upsert_trial(run_b, _mk_trial(0, 0.5, params_key_val=2.0))

    runs = load_run_history(db, limit=10)
    assert len(runs) == 2

    summary = summarize_run(db, run_a)
    assert summary["counts"]["total"] == 2
    assert summary["best_score"] == 2.0

    cmp = compare_runs(db, run_a, run_b)
    assert cmp["overlap_params_key"] == 1
    assert cmp["best_score_a"] == 2.0
    assert cmp["best_score_b"] == 0.5


def test_artifact_listing_and_preview(tmp_path: Path):
    results = tmp_path / "results"
    results.mkdir()
    (results / "a.txt").write_text("hello", encoding="utf-8")
    (results / "b.json").write_text(json.dumps({"k": 1}), encoding="utf-8")

    files = list_result_artifacts(results)
    assert len(files) == 2
    txt_preview = read_artifact_preview(results / "a.txt")
    json_preview = read_artifact_preview(results / "b.json")
    assert "hello" in txt_preview
    assert '"k": 1' in json_preview


def test_resolve_db_path_prefers_existing(tmp_path: Path):
    p1 = tmp_path / "missing.db"
    p2 = tmp_path / "existing.db"
    p2.write_text("", encoding="utf-8")
    picked = resolve_db_path([str(p1), str(p2)])
    assert picked == p2
