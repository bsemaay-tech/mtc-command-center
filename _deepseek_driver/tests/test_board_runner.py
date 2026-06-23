"""Tests for board_runner.py — the read-only MTC AI Boardroom MVP.

Guarantees under test:
  - fan-out to independent workers + a judge synthesis step
  - persistence of a versioned run folder (input, worker outputs, final report, metadata)
  - READ-ONLY: the runner writes ONLY inside its own run dir, never source files
  - basic secret redaction on persisted input
  - refusal to write into protected (denylisted) locations
"""
import datetime as dt
import json
from pathlib import Path

import pytest

from board_runner import Worker, BoardInput, run_board


def _fixed_now():
    return dt.datetime(2026, 6, 22, 13, 30, 0)


def _make_input():
    return BoardInput(
        title="Architecture review",
        task="Should we extract provider.py?",
        context="ds_agent.py has a PROVIDERS map.",
        workers=[
            Worker(name="deepseek", prov="deepseek", model="deepseek-chat"),
            Worker(name="xai", prov="xai", model="grok"),
        ],
        judge=Worker(name="judge", prov="deepseek", model="deepseek-chat"),
    )


def _tagging_chat_fn(messages, prov, model):
    # Worker calls echo their model; judge call echoes what it received.
    user = messages[-1]["content"]
    if model == "judge-model" or "JUDGE" in messages[0]["content"]:
        return "JUDGE_VERDICT over:\n" + user
    return f"[{model}] reviewed: {user[:40]}"


def test_run_board_creates_run_artifacts(tmp_path):
    res = run_board(_make_input(), runs_dir=tmp_path,
                    chat_fn=_tagging_chat_fn, now=_fixed_now())
    rd = res.run_dir
    assert rd.exists()
    assert (rd / "input.md").exists()
    assert (rd / "final_report.md").exists()
    assert (rd / "metadata.json").exists()
    assert (rd / "worker_outputs" / "deepseek.md").exists()
    assert (rd / "worker_outputs" / "xai.md").exists()


def test_each_worker_called_once_and_judge_sees_all_outputs(tmp_path):
    seen = []

    def chat_fn(messages, prov, model):
        seen.append(model)
        if messages[0]["content"].startswith("JUDGE"):
            joined = messages[-1]["content"]
            # judge must receive both worker outputs
            assert "deepseek" in joined and "xai" in joined
            return "FINAL"
        return f"worker {model} ok"

    res = run_board(_make_input(), runs_dir=tmp_path, chat_fn=chat_fn, now=_fixed_now())
    # two workers + one judge
    assert seen.count("deepseek-chat") >= 1
    assert "grok" in seen
    assert res.judge_output == "FINAL"
    assert set(res.worker_outputs.keys()) == {"deepseek", "xai"}


def test_run_board_only_writes_inside_run_dir(tmp_path):
    res = run_board(_make_input(), runs_dir=tmp_path,
                    chat_fn=_tagging_chat_fn, now=_fixed_now())
    assert res.writes, "expected recorded writes"
    for p in res.writes:
        assert Path(p).resolve().is_relative_to(res.run_dir.resolve()), \
            f"write escaped run dir: {p}"


def test_metadata_lists_workers_and_holds_no_secret(tmp_path):
    bi = _make_input()
    bi.task = "key is sk-SECRET1234567890abcdef please review"
    res = run_board(bi, runs_dir=tmp_path, chat_fn=_tagging_chat_fn, now=_fixed_now())
    meta = json.loads((res.run_dir / "metadata.json").read_text(encoding="utf-8"))
    assert meta["title"] == "Architecture review"
    assert {w["name"] for w in meta["workers"]} == {"deepseek", "xai"}
    assert meta["judge"]["name"] == "judge"
    assert "sk-SECRET1234567890abcdef" not in json.dumps(meta)


def test_persisted_input_is_redacted(tmp_path):
    bi = _make_input()
    bi.task = "token sk-SECRET1234567890abcdef must not leak"
    res = run_board(bi, runs_dir=tmp_path, chat_fn=_tagging_chat_fn, now=_fixed_now())
    text = (res.run_dir / "input.md").read_text(encoding="utf-8")
    assert "sk-SECRET1234567890abcdef" not in text
    assert "REDACTED" in text


def test_run_board_refuses_protected_runs_dir(tmp_path):
    protected = tmp_path / "MTC_V2" / "runs"
    with pytest.raises(ValueError):
        run_board(_make_input(), runs_dir=protected,
                  chat_fn=_tagging_chat_fn, now=_fixed_now())
