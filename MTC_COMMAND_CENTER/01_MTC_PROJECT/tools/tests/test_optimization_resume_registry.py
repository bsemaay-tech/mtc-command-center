from __future__ import annotations

from pathlib import Path

from tools.optimization_resume_registry import (
    EvaluationIdentity,
    ResumeRegistry,
    evaluation_key,
    metrics_hash,
)


def _identity(**overrides: object) -> EvaluationIdentity:
    data = {
        "profile_id": "profile",
        "dataset_id": "dataset",
        "dataset_hash": "datahash",
        "symbol": "BTCUSDT.P",
        "timeframe": "1h",
        "window_id": "wf1",
        "split_type": "test",
        "params": {"a": 1, "b": 2},
        "runner_version": "runner-v1",
        "optimizer_version": "optimizer-v1",
        "parameter_mapper_version": "mapper-v1",
    }
    data.update(overrides)
    return EvaluationIdentity(**data)


def test_same_identity_produces_same_evaluation_key() -> None:
    assert evaluation_key(_identity()) == evaluation_key(_identity(params={"b": 2, "a": 1}))


def test_different_params_produce_different_evaluation_key() -> None:
    assert evaluation_key(_identity()) != evaluation_key(_identity(params={"a": 2, "b": 2}))


def test_completed_evaluation_is_skipped_on_resume(tmp_path: Path) -> None:
    registry = ResumeRegistry(tmp_path / "resume_registry.sqlite")
    key = evaluation_key(_identity())

    registry.register_planned(key)
    registry.mark_running(key)
    registry.mark_completed(key, result_path="workers/w1/result.json", metrics_hash="m1")

    assert registry.is_completed(key)
    assert key in registry.load_completed_keys()


def test_skipping_completed_evaluation_preserves_completed_identity(tmp_path: Path) -> None:
    registry = ResumeRegistry(tmp_path / "resume_registry.sqlite")
    key = evaluation_key(_identity())

    registry.mark_completed(key, result_path="workers/w1/result.json", metrics_hash="m1")
    registry.mark_skipped_already_completed(key)

    assert registry.is_completed(key)
    assert key in registry.load_completed_keys()


def test_duplicate_rows_are_deduped(tmp_path: Path) -> None:
    registry = ResumeRegistry(tmp_path / "resume_registry.sqlite")
    rows = [
        {"evaluation_key": "k1", "net_profit": 1, "profit_factor": 1.2},
        {"evaluation_key": "k1", "net_profit": 1, "profit_factor": 1.2},
        {"evaluation_key": "k2", "net_profit": 2, "profit_factor": 1.4},
    ]

    unique, conflicts = registry.dedupe_results(rows)

    assert [row["evaluation_key"] for row in unique] == ["k1", "k2"]
    assert conflicts == []


def test_duplicate_conflicting_result_hash_is_detected(tmp_path: Path) -> None:
    registry = ResumeRegistry(tmp_path / "resume_registry.sqlite")
    rows = [
        {"evaluation_key": "k1", "net_profit": 1, "profit_factor": 1.2},
        {"evaluation_key": "k1", "net_profit": 9, "profit_factor": 9.9},
    ]

    unique, conflicts = registry.dedupe_results(rows)

    assert len(unique) == 1
    assert conflicts and conflicts[0]["evaluation_key"] == "k1"


def test_failed_evaluation_can_be_retried_if_policy_allows(tmp_path: Path) -> None:
    registry = ResumeRegistry(tmp_path / "resume_registry.sqlite")
    key = evaluation_key(_identity())

    registry.register_planned(key)
    registry.mark_failed(key, "boom")

    assert registry.should_retry_failed(key, retry_failed=True)
    assert not registry.should_retry_failed(key, retry_failed=False)


def test_metrics_hash_is_stable_for_key_order() -> None:
    assert metrics_hash({"b": 2, "a": 1}) == metrics_hash({"a": 1, "b": 2})
