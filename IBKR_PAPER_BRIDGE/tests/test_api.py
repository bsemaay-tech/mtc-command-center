from __future__ import annotations

from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient

from bridge.app import create_app
from bridge.broker.mock import MockBroker, ScriptedOutcome
from bridge.engine.engine import BridgeEngine
from bridge.engine.risk import RiskConfig, RiskEngine
from bridge.engine.strategies.keltner_trail_ema8 import KeltnerTrailEma8
from bridge.engine.types import ActionOutcome
from bridge.store.db import Store


class _BroadcastSpy:
    def __init__(self):
        self.messages = []

    async def broadcast(self, topic, data):
        self.messages.append((topic, data))


def _runtime_api(tmp_path, *, schema_version: int = 4):
    db_path = tmp_path / f"runtime-v{schema_version}.db"
    if schema_version != 4:
        store = Store(db_path)
        store.initialize(target_schema_version=schema_version)
        store.close()
    app = create_app(
        start_runtime=True,
        store_path=db_path,
        broker=MockBroker(bars=[]),
    )
    app.state.ws_hub = _BroadcastSpy()
    return TestClient(app), app


def test_api_status_config_state_and_snapshot_roundtrip():
    client = TestClient(create_app())

    status = client.get("/api/status").json()
    assert status["state"] == "DISARMED"
    assert status["network"] == "testnet"
    state_version = status["state_version"]

    config = client.get("/api/config")
    assert config.status_code == 503
    assert config.json()["detail"] == "CONFIG_NOT_RUNTIME_VALIDATED"

    stale = client.post("/api/arm", headers={"X-Confirm": str(state_version + 1)})
    assert stale.status_code == 409

    armed = client.post("/api/arm", headers={"X-Confirm": str(state_version)})
    assert armed.status_code == 200
    assert armed.json()["state"] == "ARMED"

    disarmed = client.post("/api/disarm")
    assert disarmed.status_code == 200
    assert disarmed.json()["state"] == "DISARMED"

    killed = client.post("/api/kill?flatten=false")
    assert killed.status_code == 200
    assert killed.json()["state"] == "KILLED"

    snapshot = client.get("/api/snapshot").json()
    assert snapshot["status"]["state"] == "KILLED"
    assert snapshot["config"] == {}
    assert snapshot["config_status"] == "CONFIG_NOT_RUNTIME_VALIDATED"
    assert snapshot["bars"]["bars"] == []


def test_ws_pushes_snapshot_on_connect():
    client = TestClient(create_app())

    with client.websocket_connect("/ws") as ws:
        message = ws.receive_json()

    assert message["topic"] == "snapshot"
    assert message["data"]["status"]["mode"] == "paper"


def test_runtime_config_view_is_validated_and_restart_only_put_has_no_side_effect(
    tmp_path,
):
    client, app = _runtime_api(tmp_path)
    try:
        assert not hasattr(app.state, "bridge_config")
        before_view = client.get("/api/config")
        assert before_view.status_code == 200
        assert before_view.json()["broker"]["reconnect_attempts"] == {
            "value": 9,
            "provenance": "explicit",
            "apply_mode": "restart_only",
            "capability": "always",
        }
        before_version = client.get("/api/status").json()["state_version"]
        before_events = app.state.bridge_store.get_events()
        before_engine_value = app.state.bridge_engine.bar_reconnect_attempts

        refused = client.put(
            "/api/config",
            headers={"X-Confirm": str(before_version)},
            json={"broker": {"reconnect_attempts": 10}},
        )

        assert refused.status_code == 422
        assert refused.json()["detail"] == {
            "errors": [
                {
                    "class": "RESTART_ONLY",
                    "setting": "broker.reconnect_attempts",
                    "reason": "managed_candidate_restart_required",
                }
            ]
        }
        assert client.get("/api/config").json() == before_view.json()
        assert app.state.bridge_engine.bar_reconnect_attempts == before_engine_value
        assert app.state.bridge_store.get_events() == before_events
        assert client.get("/api/status").json()["state_version"] == before_version
        assert app.state.ws_hub.messages == []
    finally:
        app.state.bridge_store.close()


def test_unknown_and_schema_inert_puts_are_typed_and_side_effect_free(tmp_path):
    client, app = _runtime_api(tmp_path)
    try:
        before_view = client.get("/api/config").json()
        before_version = client.get("/api/status").json()["state_version"]
        before_events = app.state.bridge_store.get_events()

        typo = client.put(
            "/api/config",
            headers={"X-Confirm": str(before_version)},
            json={"risk": {"max_daily_los_pct": 0.01}},
        )
        network = client.put(
            "/api/config",
            headers={"X-Confirm": str(before_version)},
            json={"broker": {"network": "testnet"}},
        )
        inert = client.put(
            "/api/config",
            headers={"X-Confirm": str(before_version)},
            json={"risk": {"max_symbol_gross_pct": 0.2}},
        )

        assert typo.status_code == 422
        assert typo.json()["detail"]["errors"] == [
            {
                "class": "UNKNOWN_KEY",
                "setting": "risk.max_daily_los_pct",
                "reason": "no_bound_runtime_field",
                "suggestion": "risk.max_daily_loss_pct",
            }
        ]
        assert network.status_code == 422
        assert network.json()["detail"]["errors"] == [
            {
                "class": "UNKNOWN_KEY",
                "setting": "broker.network",
                "reason": "no_bound_runtime_field",
            }
        ]
        assert "restart-only" not in network.text
        assert inert.status_code == 422
        assert inert.json()["detail"]["errors"] == [
            {
                "class": "KNOWN_INERT_SCHEMA",
                "setting": "risk.max_symbol_gross_pct",
                "actual_schema": 4,
                "requires": "schema>=8",
            }
        ]
        assert client.get("/api/config").json() == before_view
        assert app.state.bridge_store.get_events() == before_events
        assert client.get("/api/status").json()["state_version"] == before_version
        assert app.state.ws_hub.messages == []
    finally:
        app.state.bridge_store.close()


def test_ws_connection_stays_open_for_status_broadcasts():
    client = TestClient(create_app())

    with client.websocket_connect("/ws") as ws:
        assert ws.receive_json()["topic"] == "snapshot"
        client.post("/api/disarm")
        message = ws.receive_json()

    assert message["topic"] == "status"
    assert message["data"]["state"] == "DISARMED"


def test_kill_persists_across_restart(tmp_path):
    db_path = tmp_path / "bridge.db"
    first = TestClient(create_app(store_path=db_path))

    killed = first.post("/api/kill?flatten=false")
    assert killed.status_code == 200
    assert killed.json()["state"] == "KILLED"

    restarted = TestClient(create_app(store_path=db_path))
    assert restarted.get("/api/status").json()["state"] == "KILLED"

    acked = restarted.post("/api/kill/ack")
    assert acked.status_code == 409
    assert restarted.get("/api/status").json()["state"] == "KILLED"

    after_ack_restart = TestClient(create_app(store_path=db_path))
    assert after_ack_restart.get("/api/status").json()["state"] == "KILLED"


class _ApiClock:
    def __init__(self):
        self.now = datetime.now(UTC)

    def __call__(self):
        return self.now

    def advance(self, seconds: float):
        self.now += timedelta(seconds=seconds)


def _v9_api(tmp_path):
    clock = _ApiClock()
    path = tmp_path / "kill-api-v9.db"
    store = Store(path, clock=clock)
    try:
        store.initialize(target_schema_version=9)
    except RuntimeError:
        # RED baseline: exercise the predecessor behavior semantically.
        store.initialize(target_schema_version=8)
    store.create_run("kill-api", "dry_run", "testnet", {})
    clock.now = datetime.now(UTC) + timedelta(milliseconds=10)
    store.set_meta("app_state", "ARMED")
    broker = MockBroker(bars=[])
    broker.full_clock = clock
    engine = BridgeEngine(
        run_id="kill-api",
        broker=broker,
        store=store,
        strategy=KeltnerTrailEma8(),
        risk_engine=RiskEngine(RiskConfig()),
        state="ARMED",
        clock=clock,
    )
    app = create_app(store_path=path)
    app.state.bridge_engine = engine
    app.state.bridge_store = store
    app.state.bridge_status["state"] = "ARMED"
    return TestClient(app), store, engine, clock


def test_kill_ack_requires_current_x_confirm_and_rejects_unknown(tmp_path):
    client, store, _engine, _clock = _v9_api(tmp_path)
    broker = _engine.broker
    broker.orders.append({
        "cloid": "owned-entry", "oid": 1, "role": "ENTRY", "status": "OPEN",
        "qty": 0.1, "reduce_only": False, "symbol": "BTC", "direction": "LONG",
    })
    store.insert_order(
        cloid="owned-entry", oid=1, group_id="request", order_ref="owned:ENTRY",
        order_json={"symbol": "BTC", "role": "ENTRY"}, decision_uid="owned",
        trade_id=None, role="ENTRY", status="OPEN", qty=0.1,
    )
    broker.scripted_cancel.append(
        ScriptedOutcome(
            ActionOutcome.UNKNOWN, applied=False, reason_code="TIMEOUT"
        )
    )
    broker.partial_query_available = False

    killed = client.post("/api/kill?flatten=false")
    assert killed.status_code == 200
    version = killed.json()["state_version"]

    assert client.post("/api/kill/ack").status_code == 409
    assert client.post(
        "/api/kill/ack", headers={"X-Confirm": str(version - 1)}
    ).status_code == 409
    rejected = client.post(
        "/api/kill/ack", headers={"X-Confirm": str(version)}
    )
    assert rejected.status_code == 409
    assert client.get("/api/status").json()["state"] == "KILLED"


def test_kill_ack_rejects_stale_safe_checkpoint(tmp_path):
    client, _store, _engine, clock = _v9_api(tmp_path)
    killed = client.post("/api/kill?flatten=false")
    assert killed.status_code == 200
    clock.advance(_engine.full_reconcile_max_age_s() + 1)
    current = client.get("/api/status").json()["state_version"]

    acked = client.post(
        "/api/kill/ack", headers={"X-Confirm": str(current)}
    )
    assert acked.status_code == 409
    assert client.get("/api/status").json()["state"] == "KILLED"


def test_kill_ack_after_fresh_safe_proof_is_disarmed_never_armed(tmp_path):
    client, store, _engine, _clock = _v9_api(tmp_path)
    killed = client.post("/api/kill?flatten=false")
    assert killed.status_code == 200
    version = killed.json()["state_version"]

    acked = client.post(
        "/api/kill/ack", headers={"X-Confirm": str(version)}
    )
    assert acked.status_code == 200
    assert acked.json()["state"] == "DISARMED"
    assert store.get_meta("kill_request_active") is None
    assert store.get_meta("app_state") == "DISARMED"
