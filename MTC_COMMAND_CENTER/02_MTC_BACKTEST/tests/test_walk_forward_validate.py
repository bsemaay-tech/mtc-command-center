import json
from argparse import Namespace
from pathlib import Path

from scripts.walk_forward_validate import build_commands, build_walkforward_reports, export_candidates_from_train_csv


def test_build_commands_wires_expected_subcommands(tmp_path: Path):
    args = Namespace(
        train_case="configs/cases/aug2025_parity.json",
        target_case_1="configs/cases/target_sep2025_dec2025.json",
        target_case_2="configs/cases/target_jan2026.json",
        iters=200,
        seed=42,
        workers=1,
        min_trades=10,
        max_dd=40.0,
        outdir=str(tmp_path),
    )

    commands, _ = build_commands(args, tmp_path)

    assert len(commands) == 4
    assert commands[0][3] == "run"
    assert commands[1][3] == "export-candidates"
    assert commands[2][3] == "replay-candidates"
    assert commands[3][3] == "replay-candidates"
    assert "--iters" in commands[0]
    assert "--seed" in commands[0]
    assert "--workers" in commands[0]


def test_build_commands_respects_threshold_args(tmp_path: Path):
    args = Namespace(
        train_case="configs/cases/aug2025_parity.json",
        target_case_1="configs/cases/target_sep2025_dec2025.json",
        target_case_2="configs/cases/target_jan2026.json",
        iters=50,
        seed=7,
        workers=1,
        min_trades=12,
        max_dd=35.0,
        outdir=str(tmp_path),
    )
    commands, _ = build_commands(args, tmp_path)
    assert "--min-trades" in commands[0] and "12" in commands[0]
    assert "--max-dd" in commands[0] and "35.0" in commands[0]
    assert "--min-trades" in commands[2] and "12" in commands[2]
    assert "--max-dd" in commands[2] and "35.0" in commands[2]


def test_build_commands_passes_mode_space_file_and_top_k(tmp_path: Path):
    args = Namespace(
        train_case="configs/cases/supertrend_wf_train_20260308.json",
        target_case_1="configs/cases/supertrend_wf_target1_20260308.json",
        target_case_2="configs/cases/supertrend_wf_target2_20260308.json",
        mode="grid",
        iters=45,
        seed=42,
        workers=2,
        min_trades=10,
        max_dd=80.0,
        space_file="configs/spaces/supertrend_walkforward_high_atr_20260308.json",
        objectives="net_profit,max_dd_pct,profit_factor",
        top_k=5,
        candidate_source="pareto",
        outdir=str(tmp_path),
    )

    commands, _ = build_commands(args, tmp_path)

    assert "--mode" in commands[0] and "grid" in commands[0]
    assert "--space-file" in commands[0]
    assert "configs/spaces/supertrend_walkforward_high_atr_20260308.json" in commands[0]
    assert "--objectives" in commands[0]
    assert "net_profit,max_dd_pct,profit_factor" in commands[0]
    assert "--top-k" in commands[1] and "5" in commands[1]


def test_build_walkforward_reports_writes_ranking_and_summary(tmp_path: Path):
    (tmp_path / "replay_target1.csv").write_text(
        "candidate_file,status,net_profit,max_dd_pct\n"
        "a.json,OK,100,10\n"
        "b.json,OK,80,8\n",
        encoding="utf-8",
    )
    (tmp_path / "replay_target2.csv").write_text(
        "candidate_file,status,net_profit,max_dd_pct\n"
        "a.json,OK,50,12\n"
        "b.json,OK,70,9\n",
        encoding="utf-8",
    )

    ranking, summary = build_walkforward_reports(tmp_path)
    assert ranking.exists()
    assert summary.exists()
    payload = json.loads(summary.read_text(encoding="utf-8"))
    assert payload["status"] == "OK"
    assert payload["best_candidate_file"] in {"a.json", "b.json"}


def test_build_walkforward_reports_handles_missing_replay_csv(tmp_path: Path):
    ranking, summary = build_walkforward_reports(tmp_path)
    assert ranking.exists()
    assert summary.exists()
    payload = json.loads(summary.read_text(encoding="utf-8"))
    assert payload["status"] == "EMPTY"
    assert payload["reason"] == "missing_replay_csv"


def test_export_candidates_from_train_csv_selects_top_score(tmp_path: Path):
    trials = tmp_path / "train_trials.csv"
    trials.write_text(
        "idx,score,net_profit,max_dd_pct,total_trades,win_rate,profit_factor,runtime_s,status,prune_reason,min_trades_threshold,max_dd_threshold_pct,pruned_metric_value,stop_loss.percent,risk.risk_long_percent\n"
        "0,10,100,5,20,50,1.2,1.0,OK,,10,80,0,0.2,0.1\n"
        "1,20,90,4,20,55,1.3,1.0,OK,,10,80,0,0.3,0.2\n"
        "2,30,80,3,20,60,1.4,1.0,PRUNED,MAX_DD_PCT,10,80,81,0.4,0.3\n",
        encoding="utf-8",
    )
    outdir = tmp_path / "candidates"
    written = export_candidates_from_train_csv(trials, outdir, top_k=1, overwrite=True)
    assert len(written) == 1
    payload = json.loads(written[0].read_text(encoding="utf-8"))
    assert payload["params"]["stop_loss.percent"] == 0.3
