from __future__ import annotations

import hashlib
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys

import pytest

from bridge.app import create_app
from bridge.broker.mock import MockBroker
from bridge.config_contract import ConfigContractAstCensus
from bridge.store.db import Store


SHIPPED_CONFIG = Path(__file__).parents[1] / "config" / "bridge.yaml"
SHIPPED_CONFIG_BYTES = 324
SHIPPED_CONFIG_SHA256 = "a96fecd10d6966c3e93a829ec4d75869a0851f0136a06e85ab45c255ee0f5842"


def _write_yaml(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def _candidate_with_risk_leaf(tmp_path: Path, name: str, value: str) -> Path:
    text = SHIPPED_CONFIG.read_text(encoding="utf-8")
    return _write_yaml(
        tmp_path / f"{name}.yaml",
        text.replace("risk:\n", f"risk:\n  {name}: {value}\n", 1),
    )


def _initialize_schema(path: Path, version: int) -> None:
    store = Store(path)
    try:
        store.initialize(target_schema_version=version)
    finally:
        store.close()


def _source(relative: str) -> str:
    return (Path(__file__).parents[1] / relative).read_text(encoding="utf-8")


def test_startup_refuses_unknown_leaf_before_app_state_mutation(tmp_path):
    config_path = _write_yaml(
        tmp_path / "bridge.yaml",
        "risk:\n  max_daily_los_pct: 0.01\n",
    )
    store_path = tmp_path / "bridge.db"

    with pytest.raises(RuntimeError) as caught:
        create_app(
            start_runtime=True,
            config_path=config_path,
            store_path=store_path,
            broker=MockBroker(bars=[]),
        )

    assert str(caught.value).splitlines() == [
        "STARTUP_FAIL class=UNKNOWN_KEY setting=risk.max_daily_los_pct "
        "reason=no_bound_runtime_field suggestion=risk.max_daily_loss_pct "
        "action=remove_or_implement_under_separate_approval",
        "STARTUP_FAIL summary refused=1",
    ]
    store = Store(store_path)
    try:
        assert store.get_meta("app_state") is None
    finally:
        store.close()


def test_shipped_v2_schema4_paper_is_read_once_and_reaches_every_consumer(
    tmp_path, monkeypatch
):
    raw = SHIPPED_CONFIG.read_bytes()
    assert len(raw) == SHIPPED_CONFIG_BYTES
    assert hashlib.sha256(raw).hexdigest() == SHIPPED_CONFIG_SHA256

    original_read_text = Path.read_text

    def refuse_second_whole_document_reader(path: Path, *args, **kwargs):
        if path.resolve() == SHIPPED_CONFIG.resolve():
            raise AssertionError("accepted config was read a second time")
        return original_read_text(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", refuse_second_whole_document_reader)
    app = create_app(
        start_runtime=True,
        config_path=SHIPPED_CONFIG,
        store_path=tmp_path / "bridge.db",
        broker=MockBroker(bars=[]),
    )
    try:
        validated = app.state.validated_runtime_settings
        assert validated.schema_version == 4
        assert validated.mode == "paper"
        assert validated.config_sha256 == SHIPPED_CONFIG_SHA256
        assert validated.declared_leaf_paths == (
            "broker.data_restore_timeout_s",
            "broker.reconnect_attempts",
            "broker.reconnect_base_delay_s",
            "risk.max_consecutive_losses",
            "risk.max_daily_loss_pct",
            "risk.max_leverage",
            "risk.max_position_notional_pct",
            "risk.min_order_usd",
            "risk.min_stop_distance_pct",
            "risk.reconcile_max_consecutive_failures",
            "risk.risk_pct_per_trade",
        )
        assert set(validated.declared_leaf_paths) < set(validated.bound_setting_paths)
        assert set(validated.bound_setting_paths) - set(validated.declared_leaf_paths) == {
            "risk.app_armed",
            "risk.coin_enabled",
            "risk.direction",
            "risk.feed_stale",
            "risk.size_decimals",
        }
        assert {row.producer for row in validated.configured_rows} == {"YamlLeafWalker"}
        assert {setting.producer for setting in validated.settings.values()} == {
            "BoundFieldWalker"
        }

        engine = app.state.bridge_engine
        assert engine is not None
        assert engine.state == "DISARMED"
        expected_risk = {
            "risk_pct_per_trade": 0.005,
            "max_daily_loss_pct": 0.02,
            "max_position_notional_pct": 0.20,
            "min_stop_distance_pct": 0.001,
            "min_order_usd": 10.0,
            "max_leverage": 1,
            "max_consecutive_losses": 3,
        }
        for field_name, expected in expected_risk.items():
            assert getattr(engine.risk_engine.config, field_name) == expected
        assert engine.reconcile_max_consecutive_failures == 3
        assert engine.bar_reconnect_attempts == 9
        assert engine.bar_reconnect_base_delay_s == 5.0
        assert engine.bar_data_restore_timeout_s == 300.0
        assert app.state.bridge_store.get_meta("app_state") == "DISARMED"
    finally:
        app.state.bridge_store.close()


def test_source_census_independently_matches_bound_fields_to_consumer_gates():
    package_root = Path(__file__).parents[1]

    census = ConfigContractAstCensus.run(package_root)

    assert census.status == "PASS", census.findings
    assert census.findings == ()
    assert len(census.rows) == 25
    assert census.source_sha256
    assert census.candidate_bytes == SHIPPED_CONFIG_BYTES
    assert census.candidate_sha256 == SHIPPED_CONFIG_SHA256
    assert census.package_sha256
    for required in ConfigContractAstCensus.REQUIRED_SOURCES:
        assert required in census.source_identities
    rows = {row.setting_path: row for row in census.rows}
    assert {row.producer for row in census.rows} == {"ConfigContractAstCensus"}
    assert rows["risk.risk_pct_per_trade"].expected_path == "risk.risk_pct_per_trade"
    assert rows["risk.risk_pct_per_trade"].field_source_line != rows[
        "risk.risk_pct_per_trade"
    ].take_source_line
    assert rows["risk.risk_pct_per_trade"].consumer_capability == "always"
    assert rows["risk.equity_floor_usdc"].consumer_capability == "durable_risk"
    assert rows["risk.equity_floor_usdc"].read_site_capability == "durable_risk"
    assert rows["risk.max_symbol_gross_pct"].consumer_capability == "exposure_controls"
    assert rows["risk.max_symbol_gross_pct"].read_site_capability == "exposure_controls"
    assert rows["broker.reconnect_attempts"].target_field == "bar_reconnect_attempts"
    assert (
        rows["risk.reconcile_max_consecutive_failures"].target_field
        == "reconcile_max_consecutive_failures"
    )


def test_non_default_values_reach_each_settings_bearing_target(tmp_path):
    candidate = SHIPPED_CONFIG.read_text(encoding="utf-8")
    candidate = candidate.replace("  reconnect_attempts: 9\n", "  reconnect_attempts: 7\n", 1)
    candidate = candidate.replace(
        "  risk_pct_per_trade: 0.005\n", "  risk_pct_per_trade: 0.006\n", 1
    )
    candidate = candidate.replace(
        "  reconcile_max_consecutive_failures: 3\n",
        "  reconcile_max_consecutive_failures: 4\n",
        1,
    )

    app = create_app(
        start_runtime=True,
        config_path=_write_yaml(tmp_path / "non-defaults.yaml", candidate),
        store_path=tmp_path / "non-defaults.db",
        broker=MockBroker(bars=[]),
    )
    try:
        engine = app.state.bridge_engine
        assert engine.risk_engine.config.risk_pct_per_trade == 0.006
        assert engine.bar_reconnect_attempts == 7
        assert engine.reconcile_max_consecutive_failures == 4
    finally:
        app.state.bridge_store.close()


def test_schema_capability_matrix_refuses_inert_and_accepts_exact_boundaries(tmp_path):
    exposure_config = _candidate_with_risk_leaf(
        tmp_path, "max_symbol_gross_pct", "0.19"
    )
    for schema_version in (4, 7):
        db_path = tmp_path / f"exposure-v{schema_version}.db"
        _initialize_schema(db_path, schema_version)
        with pytest.raises(RuntimeError) as caught:
            create_app(
                start_runtime=True,
                config_path=exposure_config,
                store_path=db_path,
                broker=MockBroker(bars=[]),
            )
        assert str(caught.value).splitlines() == [
            "STARTUP_FAIL class=KNOWN_INERT_SCHEMA "
            f"setting=risk.max_symbol_gross_pct actual_schema={schema_version} "
            "requires=schema>=8 "
            "action=remove_or_obtain_separate_schema_and_config_approval",
            "STARTUP_FAIL summary refused=1",
        ]

    schema8_path = tmp_path / "exposure-v8.db"
    _initialize_schema(schema8_path, 8)
    schema8_app = create_app(
        start_runtime=True,
        config_path=exposure_config,
        store_path=schema8_path,
        broker=MockBroker(bars=[]),
    )
    try:
        assert schema8_app.state.validated_runtime_settings.schema_version == 8
        assert schema8_app.state.bridge_engine.risk_engine.config.max_symbol_gross_pct == 0.19
    finally:
        schema8_app.state.bridge_store.close()

    durable_config = _candidate_with_risk_leaf(tmp_path, "equity_floor_usdc", "600")
    schema4_path = tmp_path / "durable-v4.db"
    _initialize_schema(schema4_path, 4)
    with pytest.raises(RuntimeError) as caught:
        create_app(
            start_runtime=True,
            config_path=durable_config,
            store_path=schema4_path,
            broker=MockBroker(bars=[]),
        )
    assert "class=KNOWN_INERT_SCHEMA setting=risk.equity_floor_usdc actual_schema=4" in str(
        caught.value
    )

    schema7_path = tmp_path / "durable-v7.db"
    _initialize_schema(schema7_path, 7)
    schema7_app = create_app(
        start_runtime=True,
        config_path=durable_config,
        store_path=schema7_path,
        broker=MockBroker(bars=[]),
    )
    try:
        assert schema7_app.state.validated_runtime_settings.schema_version == 7
        assert schema7_app.state.bridge_engine.risk_engine.config.equity_floor_usdc == 600.0
    finally:
        schema7_app.state.bridge_store.close()


def test_broker_network_is_unknown_at_startup_not_restart_only(tmp_path):
    text = SHIPPED_CONFIG.read_text(encoding="utf-8").replace(
        "broker:\n", "broker:\n  network: testnet\n", 1
    )
    config_path = _write_yaml(tmp_path / "network.yaml", text)

    with pytest.raises(RuntimeError) as caught:
        create_app(
            start_runtime=True,
            config_path=config_path,
            store_path=tmp_path / "network.db",
            broker=MockBroker(bars=[]),
        )

    assert "class=UNKNOWN_KEY setting=broker.network" in str(caught.value)
    assert "restart-only" not in str(caught.value)


def test_dry_run_refuses_explicit_replaced_value_and_uses_internal_override(tmp_path):
    with pytest.raises(RuntimeError) as caught:
        create_app(
            dry_run=True,
            start_runtime=True,
            config_path=SHIPPED_CONFIG,
            store_path=tmp_path / "explicit-dry-run.db",
            broker=MockBroker(bars=[]),
        )
    assert "class=KNOWN_INERT_MODE setting=risk.max_position_notional_pct" in str(
        caught.value
    )
    assert "actual_mode=dry_run" in str(caught.value)

    without_explicit = SHIPPED_CONFIG.read_text(encoding="utf-8").replace(
        "  max_position_notional_pct: 0.20\n", "", 1
    )
    app = create_app(
        dry_run=True,
        start_runtime=True,
        config_path=_write_yaml(tmp_path / "dry-run.yaml", without_explicit),
        store_path=tmp_path / "internal-dry-run.db",
        broker=MockBroker(bars=[]),
    )
    try:
        assert app.state.bridge_engine.risk_engine.config.max_position_notional_pct == 0.5
        assert app.state.validated_runtime_settings.effective_view()["risk"][
            "max_position_notional_pct"
        ] == {
            "value": 0.5,
            "provenance": "internal_mode_override",
            "apply_mode": "restart_only",
            "capability": "always",
        }
    finally:
        app.state.bridge_store.close()


def test_config_read_inability_stops_before_leaf_classification_or_state(tmp_path, monkeypatch):
    config_path = tmp_path / "unreadable.yaml"
    config_path.write_bytes(SHIPPED_CONFIG.read_bytes())
    original_read_bytes = Path.read_bytes

    def unreadable(path: Path):
        if path == config_path:
            raise PermissionError("probe")
        return original_read_bytes(path)

    monkeypatch.setattr(Path, "read_bytes", unreadable)
    store_path = tmp_path / "file-stop.db"
    with pytest.raises(RuntimeError) as caught:
        create_app(
            start_runtime=True,
            config_path=config_path,
            store_path=store_path,
            broker=MockBroker(bars=[]),
        )
    assert str(caught.value).splitlines() == [
        "STARTUP_STOP subject=config reason=file_unreadable "
        "action=repair_config_read_and_retry",
        "STARTUP_STOP summary refused=1",
    ]
    assert "STARTUP_FAIL" not in str(caught.value)
    store = Store(store_path)
    try:
        assert store.get_meta("app_state") is None
    finally:
        store.close()


def test_database_open_and_unsupported_schema_are_reasoned_stops(tmp_path):
    regular_parent = tmp_path / "not-a-directory"
    regular_parent.write_text("blocking parent", encoding="utf-8")
    with pytest.raises(RuntimeError) as open_caught:
        create_app(
            start_runtime=True,
            config_path=SHIPPED_CONFIG,
            store_path=regular_parent / "bridge.db",
            broker=MockBroker(bars=[]),
        )
    assert str(open_caught.value).splitlines() == [
        "STARTUP_STOP subject=schema_capabilities reason=store_initialize_failed "
        "action=repair_store_evaluation_and_retry",
        "STARTUP_STOP summary refused=1",
    ]

    unsupported_path = tmp_path / "unsupported.db"
    connection = sqlite3.connect(unsupported_path)
    connection.execute("CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT)")
    connection.execute(
        "INSERT INTO meta(key, value) VALUES ('schema_version', '999')"
    )
    connection.commit()
    connection.close()
    with pytest.raises(RuntimeError) as schema_caught:
        create_app(
            start_runtime=True,
            config_path=SHIPPED_CONFIG,
            store_path=unsupported_path,
            broker=MockBroker(bars=[]),
        )
    assert str(schema_caught.value) == str(open_caught.value)

    missing_meta_path = tmp_path / "missing-meta.db"
    sqlite3.connect(missing_meta_path).close()
    control = create_app(
        start_runtime=True,
        config_path=SHIPPED_CONFIG,
        store_path=missing_meta_path,
        broker=MockBroker(bars=[]),
    )
    try:
        assert control.state.validated_runtime_settings.schema_version == 4
        assert control.state.bridge_store.get_meta("app_state") == "DISARMED"
    finally:
        control.state.bridge_store.close()


def test_capability_read_failure_is_stop_never_inert_fail(tmp_path, monkeypatch):
    def not_evaluated(_store):
        raise sqlite3.OperationalError("probe")

    monkeypatch.setattr(Store, "durable_risk_controls_enabled", not_evaluated)
    store_path = tmp_path / "schema-read-stop.db"
    with pytest.raises(RuntimeError) as caught:
        create_app(
            start_runtime=True,
            config_path=SHIPPED_CONFIG,
            store_path=store_path,
            broker=MockBroker(bars=[]),
        )
    assert str(caught.value).splitlines() == [
        "STARTUP_STOP subject=schema_capabilities reason=not_evaluated "
        "action=repair_store_evaluation_and_retry",
        "STARTUP_STOP summary refused=1",
    ]
    assert "KNOWN_INERT_SCHEMA" not in str(caught.value)
    store = Store(store_path)
    try:
        assert store.get_meta("app_state") is None
    finally:
        store.close()


def test_complete_census_detects_duplicate_yaml_and_source_boundary_changes(tmp_path):
    duplicate_yaml = SHIPPED_CONFIG.read_text(encoding="utf-8").replace(
        "  risk_pct_per_trade: 0.005\n",
        "  risk_pct_per_trade: 0.005\n  risk_pct_per_trade: 0.006\n",
        1,
    )
    with pytest.raises(RuntimeError) as duplicate_caught:
        create_app(
            start_runtime=True,
            config_path=_write_yaml(tmp_path / "duplicate.yaml", duplicate_yaml),
            store_path=tmp_path / "duplicate.db",
            broker=MockBroker(bars=[]),
        )
    assert "class=INVALID_DOCUMENT" in str(duplicate_caught.value)
    assert "reason=duplicate_key:risk_pct_per_trade" in str(duplicate_caught.value)

    package_root = Path(__file__).parents[1]
    contract_source = _source("bridge/config_contract.py")
    removed_field = contract_source.replace(
        "    max_leverage: TakenValue[int]\n", "", 1
    )
    removed = ConfigContractAstCensus.run(
        package_root,
        source_overrides={"bridge/config_contract.py": removed_field},
    )
    assert removed.status == "DETECTED"
    assert "BOUND_FIELD_SET_MISMATCH" in {finding.code for finding in removed.findings}

    duplicate_path = contract_source.replace(
        '"risk.max_leverage", int, default=1, validator=at_least_one',
        '"risk.max_consecutive_losses", int, default=1, validator=at_least_one',
        1,
    )
    duplicate = ConfigContractAstCensus.run(
        package_root,
        source_overrides={"bridge/config_contract.py": duplicate_path},
    )
    assert duplicate.status == "DETECTED"
    duplicate_codes = {finding.code for finding in duplicate.findings}
    assert {"FIELD_PATH_MISMATCH", "DUPLICATE_TAKE_PATH"} <= duplicate_codes

    engine_source = _source("bridge/engine/engine.py")
    renamed_target = engine_source.replace(
        "    bar_reconnect_attempts: int = 9\n",
        "    bar_reconnect_attempt_count: int = 9\n",
        1,
    )
    renamed = ConfigContractAstCensus.run(
        package_root,
        source_overrides={"bridge/engine/engine.py": renamed_target},
    )
    assert renamed.status == "DETECTED"
    assert "ENGINE_TARGET_FIELD_MISSING" in {
        finding.code for finding in renamed.findings
    }


def test_source_census_detects_decorative_reads_gate_mismatch_and_raw_access():
    package_root = Path(__file__).parents[1]
    contract_source = _source("bridge/config_contract.py")
    reader_line = "    reader = SettingsReader(leaves, capabilities, mode=mode)\n"

    for statement in (
        '    reader.take("risk.unused_guard", float, default=0.1)\n',
        '    unused_guard = reader.take("risk.unused_guard", float, default=0.1)\n',
    ):
        modified = contract_source.replace(reader_line, reader_line + statement, 1)
        result = ConfigContractAstCensus.run(
            package_root,
            source_overrides={"bridge/config_contract.py": modified},
        )
        assert result.status == "DETECTED"
        assert "DECORATIVE_TAKE" in {finding.code for finding in result.findings}

    wrong_read_gate = contract_source.replace(
        "            capability=EXPOSURE_CONTROLS,\n            validator=positive_fraction,\n",
        "            capability=DURABLE_RISK,\n            validator=positive_fraction,\n",
        1,
    )
    read_gate_result = ConfigContractAstCensus.run(
        package_root,
        source_overrides={"bridge/config_contract.py": wrong_read_gate},
    )
    assert read_gate_result.status == "DETECTED"
    assert "CAPABILITY_GATE_MISMATCH" in {
        finding.code for finding in read_gate_result.findings
    }

    wrong_read_identity = contract_source.replace(
        '    "durable_risk", "durable_risk_controls_enabled", min_schema=7\n',
        '    "exposure_controls", "durable_risk_controls_enabled", min_schema=7\n',
        1,
    )
    identity_result = ConfigContractAstCensus.run(
        package_root,
        source_overrides={"bridge/config_contract.py": wrong_read_identity},
    )
    assert identity_result.status == "DETECTED"
    assert "CAPABILITY_IDENTITY_MISMATCH" in {
        finding.code for finding in identity_result.findings
    }

    reconcile_source = _source("bridge/engine/reconcile.py")
    wrong_consumer_gate = reconcile_source.replace(
        "exposure_controls_enabled", "durable_risk_controls_enabled"
    )
    consumer_gate_result = ConfigContractAstCensus.run(
        package_root,
        source_overrides={"bridge/engine/reconcile.py": wrong_consumer_gate},
    )
    assert consumer_gate_result.status == "DETECTED"
    assert "CAPABILITY_GATE_MISMATCH" in {
        finding.code for finding in consumer_gate_result.findings
    }

    app_source = _source("bridge/app.py")
    raw_access = app_source + '\nimport yaml as modified_yaml\nmodified_yaml.safe_load("{}")\n'
    raw_result = ConfigContractAstCensus.run(
        package_root, source_overrides={"bridge/app.py": raw_access}
    )
    assert raw_result.status == "DETECTED"
    assert "RAW_YAML_ACCESS" in {finding.code for finding in raw_result.findings}

    unsupported = app_source + '\neval("1")\n'
    unsupported_result = ConfigContractAstCensus.run(
        package_root, source_overrides={"bridge/app.py": unsupported}
    )
    assert unsupported_result.status == "SOURCE_CENSUS_STOP"
    assert "UNMODELED_DYNAMIC_EXECUTION" in {
        finding.code for finding in unsupported_result.findings
    }


def test_package_gate_detects_one_leaf_and_hash_changes_independently(tmp_path):
    package_root = Path(__file__).parents[1]
    raw = SHIPPED_CONFIG.read_bytes()
    modified = raw.replace(b"risk:\n", b"risk:\n  inserted_probe: 1\n", 1)

    result = ConfigContractAstCensus.run(package_root, candidate_bytes=modified)

    assert result.status == "DETECTED"
    assert result.candidate_sha256 != SHIPPED_CONFIG_SHA256
    assert result.candidate_bytes > SHIPPED_CONFIG_BYTES
    assert "CANDIDATE_HASH_MISMATCH" in {
        finding.code for finding in result.findings
    }
    modified_path = tmp_path / "inserted-leaf.yaml"
    modified_path.write_bytes(modified)
    with pytest.raises(RuntimeError) as caught:
        create_app(
            start_runtime=True,
            config_path=modified_path,
            store_path=tmp_path / "inserted-leaf.db",
            broker=MockBroker(bars=[]),
        )
    assert "class=UNKNOWN_KEY setting=risk.inserted_probe" in str(caught.value)


def test_same_typed_path_swap_is_detected_by_runtime_and_source_producers(tmp_path):
    package_root = Path(__file__).parents[1]
    source = _source("bridge/config_contract.py")
    placeholder = '"risk.__w62_swap_placeholder__", float'
    swapped = source.replace('"risk.risk_pct_per_trade", float', placeholder, 1)
    swapped = swapped.replace(
        '"risk.min_stop_distance_pct", float',
        '"risk.risk_pct_per_trade", float',
        1,
    )
    swapped = swapped.replace(
        placeholder, '"risk.min_stop_distance_pct", float', 1
    )
    assert swapped != source

    census = ConfigContractAstCensus.run(
        package_root,
        source_overrides={"bridge/config_contract.py": swapped},
    )
    assert census.status == "DETECTED"
    assert [
        finding.code for finding in census.findings if finding.code == "FIELD_PATH_MISMATCH"
    ] == ["FIELD_PATH_MISMATCH", "FIELD_PATH_MISMATCH"]

    variant_root = tmp_path / "field-swap"
    shutil.copytree(package_root / "bridge", variant_root / "bridge")
    shutil.copytree(package_root / "config", variant_root / "config")
    (variant_root / "bridge" / "config_contract.py").write_text(
        swapped, encoding="utf-8", newline="\n"
    )
    probe = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "from pathlib import Path\n"
                "from bridge.app import create_app\n"
                "from bridge.broker.mock import MockBroker\n"
                "from bridge.config_contract import StartupConfigRefusal\n"
                "try:\n"
                "    create_app(start_runtime=True, "
                "config_path=Path('config/bridge.yaml'), "
                "store_path=Path('variant.db'), broker=MockBroker(bars=[]))\n"
                "except StartupConfigRefusal as exc:\n"
                "    print(str(exc))\n"
                "    raise SystemExit(0)\n"
                "print('T-FIELD-DERIVED-PATH result=NOT_DETECTED')\n"
                "raise SystemExit(1)\n"
            ),
        ],
        cwd=variant_root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=120,
        check=False,
    )
    assert probe.returncode == 0, probe.stdout + probe.stderr
    assert probe.stderr == ""
    assert probe.stdout.splitlines() == [
        "STARTUP_STOP subject=config_binding setting=risk.min_stop_distance_pct "
        "reason=field_path_mismatch action=repair_source_binding_and_retry",
        "STARTUP_STOP subject=config_binding setting=risk.risk_pct_per_trade "
        "reason=field_path_mismatch action=repair_source_binding_and_retry",
        "STARTUP_STOP summary refused=2",
    ]


def test_decorative_take_variants_remain_unknown_through_real_startup(tmp_path):
    package_root = Path(__file__).parents[1]
    source = _source("bridge/config_contract.py")
    reader_line = "    reader = SettingsReader(leaves, capabilities, mode=mode)\n"
    variant_root = tmp_path / "decorative-take"
    shutil.copytree(package_root / "bridge", variant_root / "bridge")
    shutil.copytree(package_root / "config", variant_root / "config")
    candidate = (variant_root / "config" / "bridge.yaml").read_text(encoding="utf-8")
    (variant_root / "config" / "bridge.yaml").write_text(
        candidate.replace("risk:\n", "risk:\n  unused_guard: 0.1\n", 1),
        encoding="utf-8",
        newline="\n",
    )

    for index, statement in enumerate(
        (
            '    reader.take("risk.unused_guard", float, default=0.1)\n',
            '    unused_guard = reader.take("risk.unused_guard", float, default=0.1)\n',
        )
    ):
        modified = source.replace(reader_line, reader_line + statement, 1)
        (variant_root / "bridge" / "config_contract.py").write_text(
            modified, encoding="utf-8", newline="\n"
        )
        db_path = f"decorative-{index}.db"
        probe = subprocess.run(
            [
                sys.executable,
                "-c",
                (
                    "from pathlib import Path\n"
                    "from bridge.app import create_app\n"
                    "from bridge.broker.mock import MockBroker\n"
                    "from bridge.config_contract import StartupConfigRefusal\n"
                    "try:\n"
                    f"    create_app(start_runtime=True, config_path=Path('config/bridge.yaml'), store_path=Path('{db_path}'), broker=MockBroker(bars=[]))\n"
                    "except StartupConfigRefusal as exc:\n"
                    "    print(str(exc))\n"
                    "    raise SystemExit(0)\n"
                    "raise SystemExit(1)\n"
                ),
            ],
            cwd=variant_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=120,
            check=False,
        )
        assert probe.returncode == 0, probe.stdout + probe.stderr
        assert "class=UNKNOWN_KEY setting=risk.unused_guard" in probe.stdout


def test_paper_start_preserves_testnet_hardcode_and_disarmed_state(tmp_path, monkeypatch):
    captured = {}
    broker_sentinel = object()

    def broker_factory(**kwargs):
        captured.update(kwargs)
        return broker_sentinel

    monkeypatch.setattr("bridge.app.HyperliquidBroker", broker_factory)
    monkeypatch.setattr(
        "bridge.settings.resolve_hyperliquid_credentials",
        lambda: ("fixture-account", "fixture-key", "fixture"),
    )
    app = create_app(
        start_runtime=True,
        config_path=SHIPPED_CONFIG,
        store_path=tmp_path / "paper-safety.db",
    )
    try:
        assert captured == {
            "network": "testnet",
            "account_address": "fixture-account",
            "api_wallet_key": "fixture-key",
            "coin": "BTC",
            "leverage": 1,
        }
        assert app.state.bridge_engine.broker is broker_sentinel
        assert app.state.bridge_engine.state == "DISARMED"
        assert app.state.bridge_store.get_meta("app_state") == "DISARMED"
    finally:
        app.state.bridge_store.close()
