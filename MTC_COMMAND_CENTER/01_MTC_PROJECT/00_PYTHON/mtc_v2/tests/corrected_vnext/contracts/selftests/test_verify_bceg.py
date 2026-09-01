from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from mtc_v2.tests.corrected_vnext.verify_bceg import (
    GateRefusal,
    build_projection_results,
    compare_documents,
    compare_scoped_expected,
    decode_stop_price_f64,
    execute_corrected_scenario,
    load_json_exact,
    resolve_record_references,
    validate_corrected_event_surface,
    validate_input_envelope,
    validate_legacy_unpadded,
)


FIXTURES = Path(__file__).parent
MTC_V2_ROOT = FIXTURES.parents[3]


def refusal(check_id: str, action) -> None:
    with pytest.raises(GateRefusal) as caught:
        action()
    assert caught.value.check_id == check_id


def test_identical_pair_compares_equal_on_every_node() -> None:
    left = load_json_exact(FIXTURES / "node_equal_left.json")
    right = load_json_exact(FIXTURES / "node_equal_right.json")
    assert compare_documents(left, right) is None


def test_one_node_difference_is_predetected_exactly() -> None:
    left = load_json_exact(FIXTURES / "node_equal_left.json")
    right = load_json_exact(FIXTURES / "node_one_diff.json")
    difference = compare_documents(left, right)
    assert difference is not None
    assert difference[0] == "/a/1"


def test_corrected_expectation_compares_only_the_two_design_surfaces() -> None:
    expected = {
        "EVENT_SURFACE": {"events": []},
        "RESULT_SURFACE": {"value": 1},
        "provenance": {"author": "tables"},
        "blocked_cells": ["authoring-only"],
    }
    observed = {
        "EVENT_SURFACE": {"events": []},
        "RESULT_SURFACE": {"value": 1},
        "provenance": {"author": "kernel"},
    }

    assert compare_scoped_expected(expected, observed) is None

    observed["RESULT_SURFACE"]["value"] = 2
    difference = compare_scoped_expected(expected, observed)
    assert difference is not None
    assert difference[0] == "/RESULT_SURFACE/value"


@pytest.mark.parametrize(
    ("fixture", "check_id"),
    [("duplicate_key.json", "JSON_DUPLICATE_KEY"), ("nonfinite.json", "JSON_NON_FINITE")],
)
def test_strict_json_refusals(fixture: str, check_id: str) -> None:
    refusal(check_id, lambda: load_json_exact(FIXTURES / fixture))


def test_version_shaped_surface_refusals() -> None:
    padded = load_json_exact(FIXTURES / "padded_legacy.json")
    refusal("LEGACY_SCHEMA_PADDED", lambda: validate_legacy_unpadded(padded))
    sequenced = load_json_exact(FIXTURES / "wrong_sequence.json")
    refusal("CORRECTED_SEQUENCE_INVALID", lambda: validate_corrected_event_surface(sequenced))


@pytest.mark.parametrize(
    ("fixture", "check_id"),
    [
        ("input_unknown_top.json", "INPUT_UNKNOWN_TOP_LEVEL_MEMBER"),
        ("input_missing_corrected_only.json", "INPUT_MISSING_TOP_LEVEL_MEMBER"),
        ("input_corrected_in_legacy.json", "INPUT_CORRECTED_ONLY_IN_LEGACY_ARM"),
        ("input_f64_wrong_case.json", "INPUT_F64BITS_INVALID"),
        ("input_f64_short.json", "INPUT_F64BITS_INVALID"),
        ("input_f64_nonquiet.json", "INPUT_F64BITS_INVALID"),
        ("input_f64_infinity.json", "INPUT_F64BITS_INVALID"),
        ("input_f64_outside.json", "INPUT_F64BITS_OUTSIDE_SELECTOR"),
    ],
)
def test_section_22_input_refusals(fixture: str, check_id: str) -> None:
    document = load_json_exact(FIXTURES / fixture)
    refusal(check_id, lambda: validate_input_envelope(document))


def test_input_digest_mismatch_refusal() -> None:
    path = FIXTURES / "input_valid.json"
    document = load_json_exact(path)
    wrong_digest = "0" * 64
    assert hashlib.sha256(path.read_bytes()).hexdigest() != wrong_digest
    refusal(
        "INPUT_DIGEST_MISMATCH",
        lambda: validate_input_envelope(document, path=path, expected_digest=wrong_digest),
    )


def test_valid_section_22_input() -> None:
    path = FIXTURES / "input_valid.json"
    document = load_json_exact(path)
    validate_input_envelope(
        document,
        path=path,
        expected_digest=hashlib.sha256(path.read_bytes()).hexdigest(),
    )


def test_section_22_nan_decoder_preserves_the_exact_quiet_nan_bits() -> None:
    document = load_json_exact(FIXTURES / "input_valid.json")

    value = decode_stop_price_f64(document, scenario_id="RULE2-01-GREEN")

    assert value is not None
    assert value != value


def test_record_reference_digest_mismatch_refuses_before_execution() -> None:
    document = load_json_exact(FIXTURES / "input_record_digest_mismatch.json")

    refusal(
        "RECORD_DIGEST_MISMATCH",
        lambda: resolve_record_references(
            MTC_V2_ROOT, document["corrected_only"]["records"]
        ),
    )


def test_corrected_scenario_executes_real_seam_and_emits_six_containers() -> None:
    catalog = load_json_exact(MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json")
    row = next(member for member in catalog if member["scenario_id"] == "RULE2-01-RED")

    observed = execute_corrected_scenario(MTC_V2_ROOT, row)

    assert observed["producer_id"] == "KERNEL_2"
    assert observed["semantics_version"] == "2.0.0"
    assert list(observed["EVENT_SURFACE"]) == [
        "decision_events",
        "fill_events",
        "cash_events",
        "fee_events",
        "funding_events",
        "exit_events",
    ]
    assert observed["RESULT_SURFACE"]["run_manifest"]["kernel_semantics_version"] == "2.0.0"


@pytest.mark.parametrize(
    ("scenario_id", "expected_decisions"),
    [
        ("RULE2-01-RED", ["SEMANTICS_VALIDATED", "SIZING_COMPUTED", "MIN_NOTIONAL_ADMITTED"]),
        ("RULE2-01-GREEN", ["SEMANTICS_VALIDATED", "SIZING_COMPUTED", "MIN_NOTIONAL_ADMITTED"]),
        ("RULE2-02-RED", ["SEMANTICS_VALIDATED", "SIZING_COMPUTED", "REFUSED_MIN_NOTIONAL"]),
        ("RULE2-02-GREEN", ["SEMANTICS_VALIDATED", "SIZING_COMPUTED", "MIN_NOTIONAL_ADMITTED"]),
        ("RULE2-03-RED", ["SEMANTICS_VALIDATED", "REFUSED_INSTRUMENT_OVERRIDE_ON_EVALUATION"]),
        ("RULE2-03-GREEN", ["SEMANTICS_VALIDATED", "INSTRUMENT_RECORD_VALIDATED"]),
        ("RULE2-04-RED", ["SEMANTICS_VALIDATED", "PROTECTIVE_STOP_EVALUATED"]),
        ("RULE2-04-GREEN", ["SEMANTICS_VALIDATED", "PROTECTIVE_STOP_EVALUATED"]),
        ("RULE2-05-RED", ["SEMANTICS_VALIDATED", "MIN_NOTIONAL_ADMITTED"]),
        ("RULE2-05-GREEN", ["SEMANTICS_VALIDATED", "MIN_NOTIONAL_ADMITTED"]),
        ("RULE2-06-RED", ["SEMANTICS_VALIDATED", "PROTECTIVE_STOP_EVALUATED", "COLLISION_RESOLVED"]),
        ("RULE2-06-EQUAL-PRICE-RED", ["SEMANTICS_VALIDATED", "PROTECTIVE_STOP_EVALUATED", "COLLISION_RESOLVED"]),
        ("RULE2-06-GREEN", ["SEMANTICS_VALIDATED", "PROTECTIVE_STOP_EVALUATED", "COLLISION_RESOLVED"]),
        ("RULE2-07-RED", ["SEMANTICS_VALIDATED", "SIZING_COMPUTED", "MIN_NOTIONAL_ADMITTED"]),
        ("RULE2-07-GREEN", ["SEMANTICS_VALIDATED"]),
        ("RULE2-08-RED", ["SEMANTICS_VALIDATED", "FUNDING_ELIGIBILITY"]),
        ("RULE2-08-GREEN", ["SEMANTICS_VALIDATED", "FUNDING_ELIGIBILITY"]),
    ],
)
def test_section_23_decision_trail_contains_each_evaluated_closed_reason(
    scenario_id: str, expected_decisions: list[str]
) -> None:
    catalog = load_json_exact(MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json")
    row = next(member for member in catalog if member["scenario_id"] == scenario_id)

    decisions = execute_corrected_scenario(MTC_V2_ROOT, row)["EVENT_SURFACE"]["decision_events"]

    assert [member["decision"] for member in decisions] == expected_decisions
    assert [member["sequence"] for member in decisions] == list(range(len(decisions)))
    assert all(member["kernel_semantics_version"] == "2.0.0" for member in decisions)
    assert all("details" not in member for member in decisions)
    assert all("lifecycle_id" not in member for member in decisions)
    assert all("refusal_code" not in member for member in decisions)
    assert "event_timestamp" not in decisions[0]


@pytest.mark.parametrize(
    "scenario_id",
    [
        "RULE2-01-RED",
        "RULE2-01-GREEN",
        "RULE2-02-RED",
        "RULE2-02-GREEN",
        "RULE2-03-RED",
        "RULE2-03-GREEN",
        "RULE2-04-RED",
        "RULE2-04-GREEN",
        "RULE2-05-RED",
        "RULE2-05-GREEN",
        "RULE2-06-RED",
        "RULE2-06-EQUAL-PRICE-RED",
        "RULE2-06-GREEN",
        "RULE2-07-RED",
        "RULE2-07-GREEN",
        "RULE2-08-RED",
        "RULE2-08-GREEN",
    ],
)
def test_section_23_every_emitted_event_carries_kernel_identity(
    scenario_id: str,
) -> None:
    catalog = load_json_exact(MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json")
    row = next(member for member in catalog if member["scenario_id"] == scenario_id)

    event_surface = execute_corrected_scenario(MTC_V2_ROOT, row)["EVENT_SURFACE"]

    assert all(
        member["kernel_semantics_version"] == "2.0.0"
        for events in event_surface.values()
        for member in events
    )


@pytest.mark.parametrize(
    ("scenario_id", "expected_equity_curve"),
    [
        ("RULE2-04-RED", {"first": 999.955, "last": 989.9145}),
        ("RULE2-04-GREEN", {"first": 999.955, "last": 999.955}),
        ("RULE2-06-RED", {"first": 999.91, "last": 1014.81325}),
        ("RULE2-06-EQUAL-PRICE-RED", {"first": 999.91, "last": 1009.8155}),
        ("RULE2-06-GREEN", {"first": 999.91, "last": 979.829}),
    ],
)
def test_section_23_equity_endpoints_are_window_scoped_realized_equity(
    scenario_id: str, expected_equity_curve: dict[str, float]
) -> None:
    catalog = load_json_exact(MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json")
    row = next(member for member in catalog if member["scenario_id"] == scenario_id)

    equity_curve = execute_corrected_scenario(MTC_V2_ROOT, row)["RESULT_SURFACE"][
        "equity_curve"
    ]

    assert equity_curve == pytest.approx(expected_equity_curve)


@pytest.mark.parametrize(
    "scenario_id",
    [
        "RULE2-04-RED",
        "RULE2-04-GREEN",
        "RULE2-06-RED",
        "RULE2-06-EQUAL-PRICE-RED",
        "RULE2-06-GREEN",
    ],
)
def test_section_23_fill_and_exit_conditionals_are_closed(
    scenario_id: str,
) -> None:
    catalog = load_json_exact(MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json")
    row = next(member for member in catalog if member["scenario_id"] == scenario_id)
    events = execute_corrected_scenario(MTC_V2_ROOT, row)["EVENT_SURFACE"]
    common_fill = {
        "sequence",
        "kernel_semantics_version",
        "fill_id",
        "event_class",
        "side",
        "reference_price",
        "slippage_model_id",
        "slippage_bps",
        "slippage_impact",
        "slippage_application_count",
        "price_tick_alignment",
        "final_fill_price",
        "quantity",
        "liquidity_role",
    }
    common_exit = {
        "sequence",
        "kernel_semantics_version",
        "exit_id",
        "reason",
        "fill_id",
        "quantity",
        "final_fill_price",
        "gross_realized_pnl",
    }
    fill_by_id = {member["fill_id"]: member for member in events["fill_events"]}

    for fill in events["fill_events"]:
        expected = set(common_fill)
        if fill["event_class"].endswith("EXIT"):
            expected.add("exit_id")
        if fill["event_class"] == "PROTECTIVE_STOP_EXIT":
            expected.add("fill_trigger")
        if fill["event_class"] == "TARGET_EXIT":
            expected.update({"target_fraction", "reference_quantity"})
        assert set(fill) == expected
    for exit_event in events["exit_events"]:
        expected = set(common_exit)
        if fill_by_id[exit_event["fill_id"]]["event_class"] == "PROTECTIVE_STOP_EXIT":
            expected.add("fill_trigger")
        assert set(exit_event) == expected


def test_rule2_05_red_honors_explicit_quantity_after_slippage() -> None:
    catalog = load_json_exact(MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json")
    row = next(member for member in catalog if member["scenario_id"] == "RULE2-05-RED")

    observed = execute_corrected_scenario(MTC_V2_ROOT, row)

    assert [
        (member["final_fill_price"], member["quantity"])
        for member in observed["EVENT_SURFACE"]["fill_events"]
    ] == [(101, 1)]
    assert [
        (member["kind"], member["signed_delta"])
        for member in observed["EVENT_SURFACE"]["cash_events"]
    ] == [("FEE", -0.04545)]
    assert observed["EVENT_SURFACE"]["fee_events"][0]["fee_cash_delta"] == -0.04545


@pytest.mark.parametrize(
    ("scenario_id", "expected_cash", "expected_cumulative"),
    [
        ("RULE2-08-RED", [("FUNDING", -0.1)], -0.1),
        ("RULE2-08-GREEN", [], 0),
    ],
)
def test_rule2_08_null_cost_is_not_consumed_and_funding_is_projected(
    scenario_id: str,
    expected_cash: list[tuple[str, float]],
    expected_cumulative: float,
) -> None:
    catalog = load_json_exact(MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json")
    row = next(member for member in catalog if member["scenario_id"] == scenario_id)

    observed = execute_corrected_scenario(MTC_V2_ROOT, row)

    result = observed["RESULT_SURFACE"]
    event = observed["EVENT_SURFACE"]
    assert result["refusals"] == []
    assert result["run_manifest"]["cost_schedule_id"] == "NOT_CONSUMED"
    assert [(member["kind"], member["signed_delta"]) for member in event["cash_events"]] == expected_cash
    assert [member["funding_cash_delta"] for member in event["funding_events"]] == [
        delta for _kind, delta in expected_cash
    ]
    assert result["cumulative_funding"] == expected_cumulative


def test_missing_decision_projection_resolves_absent() -> None:
    scenario_id = "RULE2-02-RED"
    selector = "/EVENT_SURFACE/decision_events/3/decision"
    catalog = load_json_exact(MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json")
    row = next(member for member in catalog if member["scenario_id"] == scenario_id)
    input_document = load_json_exact(MTC_V2_ROOT / row["input"]["path"])
    legacy = load_json_exact(
        MTC_V2_ROOT / "tests/corrected_vnext/observed/1.0.0" / f"{scenario_id}.json"
    )
    corrected = execute_corrected_scenario(MTC_V2_ROOT, row)

    projections = build_projection_results(
        scenario_id,
        input_document,
        legacy["RESULT_SURFACE"],
        corrected,
    )

    selected = next(member for member in projections if member["selector"] == selector)
    assert selected["corrected"] == {"tag": "ABSENT"}


def test_all_cataloged_corrected_scenarios_are_executable() -> None:
    catalog = load_json_exact(MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json")

    observed = [
        execute_corrected_scenario(MTC_V2_ROOT, row)
        for row in catalog
        if row["role"] in {"RED", "GREEN"}
    ]

    assert [member["scenario_id"] for member in observed] == [
        row["scenario_id"] for row in catalog if row["role"] in {"RED", "GREEN"}
    ]
    assert all(member["semantics_version"] == "2.0.0" for member in observed)
