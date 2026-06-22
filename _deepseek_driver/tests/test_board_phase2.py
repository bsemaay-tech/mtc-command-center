"""Phase-2 tests: provider fallback, worker resilience, config-driven CLI.

Still network-free: a deterministic chat_fn / mock client is injected everywhere.
"""
import datetime as dt
import json
from pathlib import Path

from board_runner import (
    Worker, BoardInput, run_board,
    board_input_from_config, main,
)


def _now():
    return dt.datetime(2026, 6, 22, 14, 0, 0)


def _judge_is(messages):
    return messages[0]["content"].startswith("JUDGE")


def test_worker_falls_back_to_next_provider_on_error(tmp_path):
    def chat_fn(messages, prov, model):
        if _judge_is(messages):
            return "VERDICT"
        if prov == "deepseek":
            raise RuntimeError("402 Insufficient Balance")
        return f"ok from {prov}"

    bi = BoardInput(
        title="T", task="review",
        workers=[Worker(name="w1", prov="deepseek", model="m", fallback=["xai"])],
        judge=Worker(name="judge", prov="deepseek", model="m"),
    )
    res = run_board(bi, runs_dir=tmp_path, chat_fn=chat_fn, now=_now())
    assert res.worker_outputs["w1"] == "ok from xai"
    wmeta = {w["name"]: w for w in res.metadata["workers"]}
    assert wmeta["w1"]["used_prov"] == "xai"
    assert wmeta["w1"]["ok"] is True


def test_worker_error_is_captured_and_run_continues(tmp_path):
    def chat_fn(messages, prov, model):
        if _judge_is(messages):
            return "VERDICT"
        if model == "broken":
            raise RuntimeError("boom")
        return "fine"

    bi = BoardInput(
        title="T", task="review",
        workers=[
            Worker(name="bad", prov="deepseek", model="broken"),
            Worker(name="good", prov="deepseek", model="ok"),
        ],
        judge=Worker(name="judge", prov="deepseek", model="m"),
    )
    res = run_board(bi, runs_dir=tmp_path, chat_fn=chat_fn, now=_now())
    assert res.worker_outputs["bad"].startswith("ERROR")
    assert res.worker_outputs["good"] == "fine"
    assert res.judge_output == "VERDICT"
    wmeta = {w["name"]: w for w in res.metadata["workers"]}
    assert wmeta["bad"]["ok"] is False
    assert wmeta["good"]["ok"] is True


def test_board_input_from_config_parses_workers_and_fallback():
    cfg = {
        "title": "Arch review",
        "task": "extract provider?",
        "context": "ds_agent has PROVIDERS",
        "workers": [
            {"name": "deepseek", "prov": "deepseek", "model": "deepseek-chat",
             "fallback": ["xai"]},
            {"name": "xai", "prov": "xai", "model": "grok"},
        ],
        "judge": {"name": "judge", "prov": "deepseek", "model": "deepseek-chat"},
    }
    bi = board_input_from_config(cfg)
    assert isinstance(bi, BoardInput)
    assert bi.title == "Arch review"
    assert bi.context == "ds_agent has PROVIDERS"
    assert bi.workers[0].fallback == ["xai"]
    assert bi.workers[1].model == "grok"
    assert bi.judge.name == "judge"


def test_cli_dry_run_executes_board_without_network(tmp_path):
    cfg = {
        "title": "CLI run",
        "task": "review this",
        "workers": [{"name": "deepseek", "prov": "deepseek", "model": "deepseek-chat"}],
        "judge": {"name": "judge", "prov": "deepseek", "model": "deepseek-chat"},
    }
    cfg_path = tmp_path / "board.json"
    cfg_path.write_text(json.dumps(cfg), encoding="utf-8")
    runs = tmp_path / "runs"

    rc = main(["--config", str(cfg_path), "--runs-dir", str(runs), "--dry-run"])
    assert rc == 0
    # exactly one run folder created, with the expected artifacts
    run_dirs = list(runs.iterdir())
    assert len(run_dirs) == 1
    rd = run_dirs[0]
    assert (rd / "final_report.md").exists()
    assert (rd / "metadata.json").exists()
    assert (rd / "worker_outputs" / "deepseek.md").exists()
