from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

import bridge.app as bridge_app
import bridge.settings as bridge_settings


_CREDENTIAL_FREE_DISARMED = "credential_free_disarmed"
_CREDENTIALED = "credentialed"
_START_MODE_ENV_VAR = "MTC_BRIDGE_START_MODE"


def _close_store(app) -> None:
    store = app.state.bridge_store
    if store is not None:
        store.close()


def test_start_mode_requires_explicit_selection() -> None:
    assert bridge_app.resolve_start_mode(env={}) == _CREDENTIALED
    assert bridge_app.resolve_start_mode(
        env={_START_MODE_ENV_VAR: _CREDENTIAL_FREE_DISARMED}
    ) == _CREDENTIAL_FREE_DISARMED
    assert bridge_app.resolve_start_mode(
        cli_value=_CREDENTIAL_FREE_DISARMED,
        env={},
    ) == _CREDENTIAL_FREE_DISARMED


def test_create_app_honors_environment_mode_before_broker_selection(
    tmp_path, monkeypatch
) -> None:
    broker_calls: list[bool] = []

    def build_broker(_root, dry_run):
        broker_calls.append(dry_run)
        return object()

    monkeypatch.setenv(_START_MODE_ENV_VAR, _CREDENTIAL_FREE_DISARMED)
    monkeypatch.setattr(bridge_app, "_build_broker", build_broker)
    app = bridge_app.create_app(
        store_path=tmp_path / "environment-mode.db",
        start_runtime=True,
    )
    try:
        assert app.state.credential_free_disarmed is True
        assert app.state.bridge_engine is None
        assert broker_calls == []
    finally:
        _close_store(app)


def test_credential_free_runtime_skips_credentials_registry_and_broker(
    tmp_path, monkeypatch
) -> None:
    calls: list[str] = []

    def forbidden(name: str):
        def fail(*_args, **_kwargs):
            calls.append(name)
            raise AssertionError(f"credential-free startup called {name}")

        return fail

    monkeypatch.setattr(bridge_app, "_build_broker", forbidden("_build_broker"))
    monkeypatch.setattr(
        bridge_settings,
        "resolve_hyperliquid_credentials",
        forbidden("resolve_hyperliquid_credentials"),
    )
    if bridge_settings.winreg is not None:
        monkeypatch.setattr(
            bridge_settings.winreg,
            "OpenKey",
            forbidden("winreg.OpenKey"),
        )

    app = bridge_app.create_app(
        store_path=tmp_path / "credential-free.db",
        start_runtime=True,
        start_mode=_CREDENTIAL_FREE_DISARMED,
    )
    try:
        assert app.state.bridge_engine is None
        assert app.state.credential_free_disarmed is True
        with TestClient(app) as client:
            assert client.get("/api/status").status_code == 200
    finally:
        _close_store(app)

    assert calls == []


def test_status_is_truthful_and_current_version_arm_is_durably_rejected(
    tmp_path, monkeypatch
) -> None:
    database = tmp_path / "credential-free-arm.db"

    def broker_must_not_be_built(*_args, **_kwargs):
        raise AssertionError("credential-free startup constructed a broker")

    monkeypatch.setattr(bridge_app, "_build_broker", broker_must_not_be_built)
    app = bridge_app.create_app(
        store_path=database,
        start_runtime=True,
        start_mode=_CREDENTIAL_FREE_DISARMED,
    )
    try:
        with TestClient(app) as client:
            before = client.get("/api/status").json()
            assert before["state"] == "DISARMED"
            assert before["mode"] == _CREDENTIAL_FREE_DISARMED
            assert before["network"] == "disabled"
            assert before["exchange_conn"] == "disabled"
            assert before["exchange_enabled"] is False
            assert before["credential_lookup"] == "disabled"
            assert before["arm_enabled"] is False

            rejected = client.post(
                "/api/arm",
                headers={"X-Confirm": str(before["state_version"])},
            )
            assert rejected.status_code == 409
            assert "credential-free DISARMED" in rejected.json()["detail"]

            after = client.get("/api/status").json()
            assert after["state"] == "DISARMED"
            assert after["state_version"] == before["state_version"]
            assert app.state.bridge_store.get_meta("app_state") == "DISARMED"
            assert client.get("/api/positions").json() == []
            assert client.get("/api/orders").json() == []
            assert client.get("/api/trades").json() == []
    finally:
        _close_store(app)

    restarted = bridge_app.create_app(
        store_path=database,
        start_runtime=True,
        start_mode=_CREDENTIAL_FREE_DISARMED,
    )
    try:
        with TestClient(restarted) as client:
            assert client.get("/api/status").json()["state"] == "DISARMED"
    finally:
        _close_store(restarted)


def test_ordinary_credentialed_runtime_still_uses_existing_broker_path(
    tmp_path, monkeypatch
) -> None:
    built: list[tuple[object, bool]] = []
    broker_marker = object()

    def build_broker(root, dry_run):
        built.append((root, dry_run))
        return broker_marker

    monkeypatch.setattr(bridge_app, "_build_broker", build_broker)
    app = bridge_app.create_app(
        store_path=tmp_path / "ordinary.db",
        start_runtime=True,
    )
    try:
        assert len(built) == 1
        assert built[0][1] is False
        assert app.state.bridge_engine.broker is broker_marker
        assert app.state.bridge_status["mode"] == "paper"
        assert app.state.bridge_status["network"] == "testnet"
        assert app.state.bridge_status["exchange_conn"] == "hyperliquid"
    finally:
        _close_store(app)


def test_invalid_explicit_start_mode_fails_before_broker_selection(
    tmp_path, monkeypatch
) -> None:
    broker_calls: list[bool] = []

    def build_broker(_root, dry_run):
        broker_calls.append(dry_run)
        return object()

    monkeypatch.setattr(bridge_app, "_build_broker", build_broker)
    with pytest.raises(ValueError, match=_START_MODE_ENV_VAR):
        bridge_app.resolve_start_mode(env={_START_MODE_ENV_VAR: "disarmed-ish"})
    with pytest.raises(ValueError, match="start mode"):
        bridge_app.create_app(
            store_path=tmp_path / "invalid.db",
            start_runtime=True,
            start_mode="disarmed-ish",
        )

    monkeypatch.setenv(_START_MODE_ENV_VAR, "disarmed-ish")
    with pytest.raises(ValueError, match=_START_MODE_ENV_VAR):
        bridge_app.create_app(
            store_path=tmp_path / "invalid-environment.db",
            start_runtime=True,
        )

    assert broker_calls == []
