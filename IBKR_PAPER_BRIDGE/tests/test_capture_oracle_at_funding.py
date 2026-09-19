"""P012 O-1 Phase A — the oracle-at-funding verifier, against the real captured bytes.

Every rejection class is exercised on a **modified copy** of the vendored fixture bytes
(`tests/fixtures/p012_oracle_reads_20260919/`, itself a byte-exact copy of the Lead-owned
reader's completed 2026-09-19 15:00Z/16:00Z brackets). One change per copy. The fixture
directory is never mutated in place, and no test performs a network read, instantiates an
SDK client, touches a credential or runs the collector's live mode.

Contract: `ADMISSION_G2_R3_LEAD_DECISIONS.md` (which tightens G2 r3 §5.6) and `G2_PLAN.md` r3.
"""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path

import pytest

from tools import capture_oracle_at_funding as oracle

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "p012_oracle_reads_20260919"
MANIFEST = "ORACLE_READS_MANIFEST.jsonl"

HOUR_15 = "2026-09-19T15:00:00Z"
HOUR_16 = "2026-09-19T16:00:00Z"
EVENT_15 = datetime(2026, 9, 19, 15, 0, 0, 41000, tzinfo=UTC)
EVENT_16 = datetime(2026, 9, 19, 16, 0, 0, 60000, tzinfo=UTC)

PRE_15 = "H20260919T150000Z_pre_metaAndAssetCtxs.json"
POST_15 = "H20260919T150000Z_post_metaAndAssetCtxs.json"

# the real observed values (from the vendored bytes, not re-derived by the tool under test)
PRE_15_PX = Decimal("81581.4")
POST_15_PX = Decimal("81581.4")
PRE_16_PX = Decimal("81628.0")
POST_16_PX = Decimal("81636.0")


def _rows(directory: Path) -> list[dict]:
    text = (directory / MANIFEST).read_text(encoding="utf-8")
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def _write_rows(directory: Path, rows: list[dict]) -> None:
    (directory / MANIFEST).write_text(
        "".join(
            json.dumps(row, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"
            for row in rows
        ),
        encoding="utf-8",
    )


def _reads(tmp_path: Path, name: str = "reads") -> Path:
    """A private copy of the fixture bytes. The fixture itself is never written."""
    target = tmp_path / name
    target.mkdir(parents=True)
    for source in FIXTURE.iterdir():
        if source.is_file():
            (target / source.name).write_bytes(source.read_bytes())
    return target


def _patch_row(directory: Path, index: int, **changes) -> None:
    """Edit exactly one manifest row. Raw bytes, sidecars and hashes stay untouched —
    this is the *lying summary* technique."""
    rows = _rows(directory)
    rows[index].update(changes)
    _write_rows(directory, rows)


def _reprice(directory: Path, filename: str, new_px: str) -> None:
    """Rewrite the raw oraclePx and re-sign everything consistently (sidecar, manifest
    sha256/bytes/oraclePx). This constructs a *valid* read with a different price; it is
    not a tamper test."""
    raw = (directory / filename).read_bytes()
    payload = json.loads(raw.decode("utf-8"))
    old = payload[1][0]["oraclePx"]
    needle = f'"oraclePx":"{old}"'.encode()
    assert raw.count(needle) == 1, "expected exactly one oraclePx for asset 0"
    patched = raw.replace(needle, f'"oraclePx":"{new_px}"'.encode())
    (directory / filename).write_bytes(patched)
    digest = hashlib.sha256(patched).hexdigest()
    (directory / (filename + ".sha256")).write_text(digest + "\n", encoding="ascii")
    rows = _rows(directory)
    for row in rows:
        if row["file"] == filename:
            row["sha256"] = digest
            row["bytes"] = len(patched)
            row["oraclePx"] = new_px
    _write_rows(directory, rows)


def _resolve(directory: Path, hour: str = HOUR_15, event: datetime = EVENT_15):
    return oracle.load_reads(directory).resolve(hour, event)


# --------------------------------------------------------------------------- policy


def test_the_shipped_tolerance_is_the_owner_constant_and_nothing_can_relax_it():
    assert oracle.O2_RELATIVE_TOLERANCE == Decimal("0.0005")
    assert str(oracle.O2_RELATIVE_TOLERANCE) == "0.0005"
    assert oracle.FRESHNESS_WINDOW == timedelta(seconds=5)

    source = Path(oracle.__file__).read_text(encoding="utf-8")
    assert "os.environ" not in source and "getenv" not in source
    # no CLI knob may exist for the owner's policy or for the comparison bound
    help_text = oracle.build_parser().format_help()
    for forbidden in (
        "--tolerance",
        "--o2",
        "--corroboration-bound",
        "--bound",
        "--freshness",
        "--allow-stale",
    ):
        assert forbidden not in help_text


def test_the_module_carries_no_network_or_sdk_capability():
    source = Path(oracle.__file__).read_text(encoding="utf-8")
    for forbidden in (
        "urllib",
        "requests",
        "httpx",
        "socket",
        "hyperliquid",
        "eth_account",
    ):
        assert forbidden not in source, (
            f"{forbidden} must not appear in a fixture-only tool"
        )


# --------------------------------------------------------------------- happy path


def test_real_reads_verify_and_resolve_the_closest_observation_at_or_before_the_event(
    tmp_path: Path,
):
    resolution = _resolve(_reads(tmp_path))

    assert resolution.admitted_price == PRE_15_PX
    assert resolution.admitted_read.file == PRE_15
    assert resolution.admitted_read.label.endswith("pre")
    # the locator the exporter's D-4 validator demands
    sidecar = (FIXTURE / (PRE_15 + ".sha256")).read_text(encoding="ascii").strip()
    assert resolution.locator == f"{sidecar}#/1/0/oraclePx"
    assert oracle.LOCATOR_PATTERN.fullmatch(resolution.locator)
    # the admitted value is never an average of the bracket
    assert resolution.relative_agreement == Decimal(0)
    assert resolution.tolerance == Decimal("0.0005")
    assert resolution.position_witness["szi"] == "0.0006"

    evidence = resolution.evidence()
    assert evidence["host_clock_limitation"] == oracle.HOST_CLOCK_LIMITATION
    assert "host wall clock" in evidence["host_clock_limitation"]
    assert "settlement" in evidence["host_clock_limitation"]
    assert evidence["admitted_price"] == "81581.4"


def test_the_second_real_hour_agrees_inside_the_fixed_tolerance_without_averaging(
    tmp_path: Path,
):
    resolution = _resolve(_reads(tmp_path), HOUR_16, EVENT_16)

    assert resolution.admitted_price == PRE_16_PX
    assert resolution.admitted_price != (PRE_16_PX + POST_16_PX) / 2
    expected = abs(PRE_16_PX - POST_16_PX) / min(PRE_16_PX, POST_16_PX)
    assert resolution.relative_agreement == expected
    assert resolution.relative_agreement < oracle.O2_RELATIVE_TOLERANCE


# ------------------------------------------------------------------ raw integrity


def test_a_single_changed_raw_byte_is_rejected(tmp_path: Path):
    reads = _reads(tmp_path)
    raw = (reads / PRE_15).read_bytes()
    (reads / PRE_15).write_bytes(
        raw.replace(b'"oraclePx":"81581.4"', b'"oraclePx":"81581.5"')
    )

    with pytest.raises(oracle.OracleRefused) as excinfo:
        oracle.load_reads(reads)
    assert excinfo.value.code == "ORACLE_RAW_BYTES_MISMATCH"


def test_a_sidecar_that_disagrees_with_the_manifest_is_rejected(tmp_path: Path):
    reads = _reads(tmp_path)
    (reads / (PRE_15 + ".sha256")).write_text("0" * 64 + "\n", encoding="ascii")

    with pytest.raises(oracle.OracleRefused) as excinfo:
        oracle.load_reads(reads)
    assert excinfo.value.code in {
        "ORACLE_RAW_BYTES_MISMATCH",
        "ORACLE_SIDECAR_MISMATCH",
    }


def test_a_manifest_byte_length_that_disagrees_is_rejected(tmp_path: Path):
    reads = _reads(tmp_path)
    _patch_row(reads, 0, bytes=1)

    with pytest.raises(oracle.OracleRefused) as excinfo:
        oracle.load_reads(reads)
    assert excinfo.value.code == "ORACLE_RAW_LENGTH_MISMATCH"


def test_a_missing_raw_file_is_rejected(tmp_path: Path):
    reads = _reads(tmp_path)
    (reads / PRE_15).unlink()

    with pytest.raises(oracle.OracleRefused) as excinfo:
        oracle.load_reads(reads)
    assert excinfo.value.code == "ORACLE_RAW_MISSING"


def test_a_non_200_status_is_rejected(tmp_path: Path):
    reads = _reads(tmp_path)
    _patch_row(reads, 0, http_status=503)

    with pytest.raises(oracle.OracleRefused) as excinfo:
        oracle.load_reads(reads)
    assert excinfo.value.code == "ORACLE_HTTP_STATUS_NOT_200"


def test_an_unparsable_raw_body_is_rejected(tmp_path: Path):
    reads = _reads(tmp_path)
    broken = b"{not json"
    (reads / PRE_15).write_bytes(broken)
    digest = hashlib.sha256(broken).hexdigest()
    (reads / (PRE_15 + ".sha256")).write_text(digest + "\n", encoding="ascii")
    _patch_row(reads, 0, sha256=digest, bytes=len(broken))

    with pytest.raises(oracle.OracleRefused) as excinfo:
        oracle.load_reads(reads)
    assert excinfo.value.code == "ORACLE_RAW_UNPARSABLE"


# ---------------------------------------------------------------- lying summaries


def test_a_lying_summary_oracle_px_is_rejected_although_every_hash_stays_valid(
    tmp_path: Path,
):
    reads = _reads(tmp_path)
    _patch_row(reads, 0, oraclePx="99999.0")

    # the raw file and both digests are still perfectly valid — only the convenience copy lies
    assert (
        hashlib.sha256((reads / PRE_15).read_bytes()).hexdigest()
        == _rows(reads)[0]["sha256"]
    )

    with pytest.raises(oracle.OracleRefused) as excinfo:
        oracle.load_reads(reads)
    assert excinfo.value.code == "ORACLE_SUMMARY_DISAGREES_WITH_RAW"
    assert "99999.0" in str(excinfo.value) and "81581.4" in str(excinfo.value)


def test_a_lying_summary_coin_is_rejected_although_every_hash_stays_valid(
    tmp_path: Path,
):
    reads = _reads(tmp_path)
    _patch_row(reads, 0, coin="ETH")

    assert (
        hashlib.sha256((reads / PRE_15).read_bytes()).hexdigest()
        == _rows(reads)[0]["sha256"]
    )

    with pytest.raises(oracle.OracleRefused) as excinfo:
        oracle.load_reads(reads)
    assert excinfo.value.code == "ORACLE_SUMMARY_DISAGREES_WITH_RAW"
    assert "ETH" in str(excinfo.value)


@pytest.mark.parametrize("field,value", [("markPx", "70000.0"), ("funding", "0.9")])
def test_a_lying_summary_mark_or_funding_is_rejected(tmp_path: Path, field, value):
    reads = _reads(tmp_path)
    _patch_row(reads, 0, **{field: value})

    with pytest.raises(oracle.OracleRefused) as excinfo:
        oracle.load_reads(reads)
    assert excinfo.value.code == "ORACLE_SUMMARY_DISAGREES_WITH_RAW"


def test_a_manifest_pointer_that_names_another_coin_is_rejected(tmp_path: Path):
    """The manifest must never be able to redirect the tool to a different asset."""
    reads = _reads(tmp_path)
    _patch_row(reads, 0, json_pointer_oraclePx="/1/1/oraclePx")

    with pytest.raises(oracle.OracleRefused) as excinfo:
        oracle.load_reads(reads)
    assert excinfo.value.code in {
        "ORACLE_SUMMARY_DISAGREES_WITH_RAW",
        "ORACLE_COIN_NOT_ADMITTED",
    }


def test_an_unresolvable_pointer_is_rejected(tmp_path: Path):
    reads = _reads(tmp_path)
    _patch_row(reads, 0, json_pointer_oraclePx="/1/99999/oraclePx")

    with pytest.raises(oracle.OracleRefused) as excinfo:
        oracle.load_reads(reads)
    assert excinfo.value.code == "ORACLE_POINTER_UNRESOLVED"


@pytest.mark.parametrize("px", ["0", "-1.0", "", "abc"])
def test_a_nonpositive_or_unparsable_price_is_rejected(tmp_path: Path, px):
    reads = _reads(tmp_path)
    _reprice(reads, PRE_15, px)

    with pytest.raises(oracle.OracleRefused) as excinfo:
        oracle.load_reads(reads)
    assert excinfo.value.code == "ORACLE_VALUE_INVALID"


def test_a_nonfinite_manifest_constant_is_rejected(tmp_path: Path):
    reads = _reads(tmp_path)
    text = (reads / MANIFEST).read_text(encoding="utf-8").splitlines()
    text[0] = text[0].replace('"bytes": 72350', '"bytes": NaN')
    (reads / MANIFEST).write_text("\n".join(text) + "\n", encoding="utf-8")

    with pytest.raises(oracle.OracleRefused) as excinfo:
        oracle.load_reads(reads)
    assert excinfo.value.code == "ORACLE_MANIFEST_INVALID"


def test_a_duplicate_manifest_member_is_rejected(tmp_path: Path):
    reads = _reads(tmp_path)
    lines = (reads / MANIFEST).read_text(encoding="utf-8").splitlines()
    lines[0] = lines[0].replace('"coin": "BTC"', '"coin": "BTC", "coin": "ETH"', 1)
    (reads / MANIFEST).write_text("\n".join(lines) + "\n", encoding="utf-8")

    with pytest.raises(oracle.OracleRefused) as excinfo:
        oracle.load_reads(reads)
    assert excinfo.value.code == "ORACLE_MANIFEST_INVALID"


# --------------------------------------------------------------------- pairing


def test_a_duplicated_pre_row_is_ambiguous_and_refuses(tmp_path: Path):
    reads = _reads(tmp_path)
    rows = _rows(reads)
    rows.append(dict(rows[0]))
    _write_rows(reads, rows)

    with pytest.raises(oracle.OracleRefused) as excinfo:
        _resolve(reads)
    assert excinfo.value.code == "ORACLE_PAIR_AMBIGUOUS"


def test_a_missing_post_row_refuses(tmp_path: Path):
    reads = _reads(tmp_path)
    rows = [row for row in _rows(reads) if row["file"] != POST_15]
    _write_rows(reads, rows)

    with pytest.raises(oracle.OracleRefused) as excinfo:
        _resolve(reads)
    assert excinfo.value.code == "ORACLE_PAIR_AMBIGUOUS"


def test_an_hour_with_no_rows_at_all_refuses(tmp_path: Path):
    with pytest.raises(oracle.OracleRefused) as excinfo:
        _resolve(
            _reads(tmp_path),
            "2026-09-19T20:00:00Z",
            datetime(2026, 9, 19, 20, 0, tzinfo=UTC),
        )
    assert excinfo.value.code == "ORACLE_PAIR_AMBIGUOUS"


# ------------------------------------------------------- timestamps and bracketing


def test_a_timestamp_without_an_explicit_offset_is_rejected(tmp_path: Path):
    reads = _reads(tmp_path)
    _patch_row(reads, 0, started_utc="2026-09-19T14:59:58.000")

    with pytest.raises(oracle.OracleRefused) as excinfo:
        oracle.load_reads(reads)
    assert excinfo.value.code == "ORACLE_TIMESTAMP_INVALID"


def test_an_out_of_order_interval_is_rejected(tmp_path: Path):
    reads = _reads(tmp_path)
    _patch_row(reads, 0, started_utc="2026-09-19T14:59:59.900+00:00")

    with pytest.raises(oracle.OracleRefused) as excinfo:
        oracle.load_reads(reads)
    assert excinfo.value.code == "ORACLE_TIMESTAMP_INVALID"


def test_the_label_alone_is_never_timing_proof(tmp_path: Path):
    """A row labelled `pre` whose recorded interval sits after the hour still refuses."""
    reads = _reads(tmp_path)
    _patch_row(
        reads,
        0,
        started_utc="2026-09-19T15:00:01.000+00:00",
        ended_utc="2026-09-19T15:00:01.500+00:00",
    )

    with pytest.raises(oracle.OracleRefused) as excinfo:
        _resolve(reads)
    assert excinfo.value.code == "ORACLE_BRACKET_STALE"


@pytest.mark.parametrize(
    "index,changes,expected",
    [
        # pre must lie ENTIRELY within [H-5s, H]
        (0, {"started_utc": "2026-09-19T14:59:55.000+00:00"}, None),
        (0, {"started_utc": "2026-09-19T14:59:54.999+00:00"}, "ORACLE_BRACKET_STALE"),
        (
            0,
            {
                "started_utc": "2026-09-19T15:00:00.000+00:00",
                "ended_utc": "2026-09-19T15:00:00.001+00:00",
            },
            "ORACLE_BRACKET_STALE",
        ),
        # post must lie ENTIRELY within (H, H+5s]
        (1, {"ended_utc": "2026-09-19T15:00:05.000+00:00"}, None),
        (1, {"ended_utc": "2026-09-19T15:00:05.001+00:00"}, "ORACLE_BRACKET_STALE"),
        (
            1,
            {
                "started_utc": "2026-09-19T15:00:00.000+00:00",
                "ended_utc": "2026-09-19T15:00:00.500+00:00",
            },
            "ORACLE_BRACKET_STALE",
        ),
    ],
)
def test_the_freshness_cutoffs_are_exact_and_cover_entire_intervals(
    tmp_path: Path, index, changes, expected
):
    reads = _reads(tmp_path)
    _patch_row(reads, index, **changes)

    if expected is None:
        assert _resolve(reads).admitted_price == PRE_15_PX
    else:
        with pytest.raises(oracle.OracleRefused) as excinfo:
            _resolve(reads)
        assert excinfo.value.code == expected


def test_the_reads_must_straddle_the_validated_event_not_merely_the_hour(
    tmp_path: Path,
):
    """`post.started` must not precede the event: the bracket has to contain E itself."""
    with pytest.raises(oracle.OracleRefused) as excinfo:
        _resolve(
            _reads(tmp_path),
            HOUR_15,
            datetime(2026, 9, 19, 15, 0, 2, 500000, tzinfo=UTC),
        )
    assert excinfo.value.code == "ORACLE_BRACKET_DOES_NOT_STRADDLE_EVENT"


def test_an_event_before_the_pre_read_cannot_belong_to_this_hour_and_refuses(
    tmp_path: Path,
):
    """The `pre.ended <= E` clause is retained as a guard but is implied here: the freshness
    rule puts `pre.ended` at or before H, and hour identity puts E at or after H. An event
    earlier than the pre read therefore belongs to a different hour, and that is the refusal."""
    with pytest.raises(oracle.OracleRefused) as excinfo:
        _resolve(
            _reads(tmp_path),
            HOUR_15,
            datetime(2026, 9, 19, 14, 59, 58, 500000, tzinfo=UTC),
        )
    assert excinfo.value.code == "ORACLE_HOUR_IDENTITY_MISMATCH"


def test_an_event_belonging_to_another_hour_refuses(tmp_path: Path):
    with pytest.raises(oracle.OracleRefused) as excinfo:
        _resolve(_reads(tmp_path), HOUR_15, EVENT_16)
    assert excinfo.value.code == "ORACLE_HOUR_IDENTITY_MISMATCH"


def test_a_naive_event_timestamp_refuses(tmp_path: Path):
    with pytest.raises(oracle.OracleRefused) as excinfo:
        # a naive stamp is exactly what this test requires the tool to refuse
        _resolve(_reads(tmp_path), HOUR_15, datetime(2026, 9, 19, 15, 0, 0, 41000))  # noqa: DTZ001
    assert excinfo.value.code == "ORACLE_TIMESTAMP_INVALID"


# --------------------------------------------------------------------- tolerance


@pytest.mark.parametrize(
    "post_px,admitted",
    [
        ("81622.1906", True),  # just below 0.0005 against pre 81581.4
        ("81622.1907", True),  # exactly 0.0005 — admitted, the comparison is <=
        ("81622.19071", False),  # just above
        ("82000.0", False),
    ],
)
def test_the_fixed_tolerance_boundary(tmp_path: Path, post_px, admitted):
    reads = _reads(tmp_path)
    _reprice(reads, POST_15, post_px)

    pre, post = PRE_15_PX, Decimal(post_px)
    rel = abs(pre - post) / min(pre, post)
    assert (rel <= oracle.O2_RELATIVE_TOLERANCE) is admitted, "fixture arithmetic check"

    if admitted:
        assert _resolve(reads).admitted_price == PRE_15_PX
    else:
        with pytest.raises(oracle.OracleRefused) as excinfo:
            _resolve(reads)
        assert excinfo.value.code == "ORACLE_TOLERANCE_EXCEEDED"


def test_the_agreement_denominator_is_the_smaller_of_the_two_reads(tmp_path: Path):
    reads = _reads(tmp_path)
    _reprice(reads, POST_15, "81600.0")
    resolution = _resolve(reads)

    assert (
        resolution.relative_agreement == (Decimal("81600.0") - PRE_15_PX) / PRE_15_PX
    )  # min(pre, post) = pre, strictly harsher than a mean-based variant


def test_selection_prefers_the_closest_eligible_observation_at_or_before_the_event(
    tmp_path: Path,
):
    reads = _reads(tmp_path)
    _reprice(reads, POST_15, "81581.5")
    resolution = _resolve(reads)

    # pre is the only observation at-or-before E; post is never selected and never averaged
    assert resolution.admitted_price == PRE_15_PX
    assert resolution.admitted_read.file == PRE_15
    assert resolution.admitted_price != Decimal("81581.45")


# ----------------------------------------------------- payment-derived corroboration


REAL_USDC, REAL_SZI, REAL_RATE = "-0.000612", "0.0006", "0.0000125"


def test_corroboration_is_unavailable_without_a_supported_bound_and_fails_closed():
    result = oracle.corroborate(PRE_15_PX, REAL_USDC, REAL_SZI, REAL_RATE)

    assert result["status"] == oracle.CORROBORATION_UNAVAILABLE_NO_SUPPORTED_BOUND
    assert result["corroborated"] is False
    assert result["bound"] is None
    # the exact diagnostic arithmetic is still performed and recorded
    expected = abs(Decimal(REAL_USDC)) / (
        abs(Decimal(REAL_SZI)) * abs(Decimal(REAL_RATE))
    )
    assert Decimal(result["derived_price"]) == expected
    assert Decimal(result["absolute_difference"]) == abs(expected - PRE_15_PX)
    assert (
        Decimal(result["relative_difference"]) == abs(expected - PRE_15_PX) / PRE_15_PX
    )
    assert result["sign_consistent"] is True


def test_the_derived_price_is_never_the_oracle_price(tmp_path: Path):
    result = oracle.corroborate(PRE_15_PX, REAL_USDC, REAL_SZI, REAL_RATE)
    assert "oracle_price" not in result
    assert result["statement"].startswith("RESEARCH_EVIDENCE_ONLY")


def test_the_owner_tolerance_is_never_silently_reused_as_the_payment_bound():
    """O-2 governs the agreement of two oracle reads; it is not a payment-rounding bound."""
    result = oracle.corroborate(PRE_15_PX, REAL_USDC, REAL_SZI, REAL_RATE)
    assert result["bound"] is None
    assert str(oracle.O2_RELATIVE_TOLERANCE) not in json.dumps(result)


@pytest.mark.parametrize("szi,rate", [("0", "0.0000125"), ("0.0006", "0")])
def test_a_zero_denominator_on_an_inventoried_event_fails_closed(szi, rate):
    result = oracle.corroborate(PRE_15_PX, REAL_USDC, szi, rate)

    assert result["status"] == oracle.CORROBORATION_UNAVAILABLE_ZERO_DENOMINATOR
    assert result["corroborated"] is False
    assert result["derived_price"] is None


def test_a_zero_payment_is_unavailable_evidence_and_never_a_proved_contradiction():
    result = oracle.corroborate(PRE_15_PX, "0", REAL_SZI, REAL_RATE)

    assert result["status"] == oracle.CORROBORATION_UNAVAILABLE_ZERO_PAYMENT
    assert result["corroborated"] is False
    assert "CONTRADICTION" not in result["status"]


def test_a_sign_inconsistency_on_nonzero_values_is_a_material_contradiction():
    # LONG position, positive rate ⇒ the account pays ⇒ usdc must be negative
    result = oracle.corroborate(PRE_15_PX, "+0.000612", REAL_SZI, REAL_RATE)

    assert result["status"] == oracle.CORROBORATION_CONTRADICTION_SIGN
    assert result["corroborated"] is False
    assert result["sign_consistent"] is False


def test_the_sign_check_is_not_skipped_when_the_magnitude_test_is_unavailable():
    result = oracle.corroborate(PRE_15_PX, "+0.000612", REAL_SZI, REAL_RATE)
    assert result["sign_consistent"] is False
    assert result["status"] == oracle.CORROBORATION_CONTRADICTION_SIGN


def test_an_explicit_synthetic_bound_adjudicates_both_ways():
    """The only way the comparison can be adjudicated. `corroboration_bound` is a keyword
    argument with no CLI flag, no environment variable and no configuration file behind it;
    production always leaves it None (the test above proves the unavailable default)."""
    derived = abs(Decimal(REAL_USDC)) / (
        abs(Decimal(REAL_SZI)) * abs(Decimal(REAL_RATE))
    )
    rel = abs(derived - PRE_15_PX) / PRE_15_PX

    inside = oracle.corroborate(
        PRE_15_PX, REAL_USDC, REAL_SZI, REAL_RATE, corroboration_bound=rel
    )
    assert inside["status"] == oracle.CORROBORATED
    assert inside["corroborated"] is True
    assert Decimal(inside["bound"]) == rel

    outside = oracle.corroborate(
        PRE_15_PX,
        REAL_USDC,
        REAL_SZI,
        REAL_RATE,
        corroboration_bound=rel / 2,
    )
    assert outside["status"] == oracle.CORROBORATION_CONTRADICTION_MAGNITUDE
    assert outside["corroborated"] is False


@pytest.mark.parametrize("value", ["nan", "inf", "-inf", "", "1e"])
def test_nonfinite_or_unparsable_payment_inputs_refuse(value):
    with pytest.raises(oracle.OracleRefused) as excinfo:
        oracle.corroborate(PRE_15_PX, value, REAL_SZI, REAL_RATE)
    assert excinfo.value.code == "ORACLE_PAYMENT_INPUT_INVALID"


# --------------------------------------------------------- collector (never live here)


def test_the_scheduled_collector_plans_the_design_note_instants():
    plan = oracle.plan_bracket(datetime(2026, 9, 19, 15, 0, tzinfo=UTC))

    assert [step["label"] for step in plan] == ["pre", "post", "state"]
    assert plan[0]["at"] < datetime(2026, 9, 19, 15, 0, tzinfo=UTC) < plan[1]["at"]
    for step in plan:
        assert (
            abs(step["at"] - datetime(2026, 9, 19, 15, 0, tzinfo=UTC))
            <= oracle.FRESHNESS_WINDOW
        )


def test_the_collector_has_no_default_transport_and_cannot_reach_a_venue(
    tmp_path: Path,
):
    """Phase A ships no network transport at all: the collector must be handed one."""
    with pytest.raises(TypeError):
        oracle.collect_bracket(  # type: ignore[call-arg]
            datetime(2026, 9, 19, 15, 0, tzinfo=UTC), out_dir=tmp_path / "out"
        )


def test_the_collector_writes_the_readers_exact_shape_with_an_injected_transport(
    tmp_path: Path,
):
    pre = (FIXTURE / PRE_15).read_bytes()
    post = (FIXTURE / POST_15).read_bytes()
    state = (FIXTURE / "H20260919T150000Z_state_clearinghouseState.json").read_bytes()
    canned = {"pre": pre, "post": post, "state": state}
    stamps = {
        "pre": ("2026-09-19T14:59:58.000+00:00", "2026-09-19T14:59:58.589+00:00"),
        "post": ("2026-09-19T15:00:02.001+00:00", "2026-09-19T15:00:02.907+00:00"),
        "state": ("2026-09-19T15:00:03.001+00:00", "2026-09-19T15:00:03.385+00:00"),
    }

    def transport(label, request):
        assert "user" not in request or request["type"] == "clearinghouseState"
        return 200, canned[label], stamps[label][0], stamps[label][1]

    out = tmp_path / "collected"
    oracle.collect_bracket(
        datetime(2026, 9, 19, 15, 0, tzinfo=UTC),
        out_dir=out,
        transport=transport,
        address="0x1E265F5E39957E08ed02A120ceFA33A9bd46AC49",
    )

    # what it wrote is exactly what the verifier accepts
    resolution = oracle.load_reads(out).resolve(HOUR_15, EVENT_15)
    assert resolution.admitted_price == PRE_15_PX
    assert (out / (PRE_15 + ".sha256")).read_text(
        encoding="ascii"
    ).strip() == hashlib.sha256(pre).hexdigest()


def test_the_collector_never_writes_into_an_existing_directory(tmp_path: Path):
    out = tmp_path / "existing"
    out.mkdir()
    with pytest.raises(oracle.OracleRefused) as excinfo:
        oracle.collect_bracket(
            datetime(2026, 9, 19, 15, 0, tzinfo=UTC),
            out_dir=out,
            transport=lambda label, request: (200, b"[]", "", ""),
        )
    assert excinfo.value.code == "ORACLE_OUTPUT_EXISTS"


# --------------------------------------------------------------------------- CLI


def test_the_cli_verifies_without_writing_into_the_reads_directory(
    tmp_path: Path, capsys
):
    reads = _reads(tmp_path)
    before = {p.name: p.read_bytes() for p in reads.iterdir()}

    code = oracle.main(
        [
            "--verify-existing",
            str(reads),
            "--hour",
            HOUR_15,
            "--event-timestamp",
            "2026-09-19T15:00:00.041+00:00",
        ]
    )

    assert code == 0
    report = json.loads(capsys.readouterr().out)
    assert report["admitted_price"] == "81581.4"
    assert report["host_clock_limitation"] == oracle.HOST_CLOCK_LIMITATION
    assert {p.name: p.read_bytes() for p in reads.iterdir()} == before


def test_the_cli_refuses_and_reports_the_code_on_a_rejected_bracket(
    tmp_path: Path, capsys
):
    reads = _reads(tmp_path)
    _patch_row(reads, 0, oraclePx="99999.0")

    code = oracle.main(
        [
            "--verify-existing",
            str(reads),
            "--hour",
            HOUR_15,
            "--event-timestamp",
            "2026-09-19T15:00:00.041+00:00",
        ]
    )

    assert code == 3
    assert "ORACLE_SUMMARY_DISAGREES_WITH_RAW" in capsys.readouterr().err


# ------------------------------------------------- gaps found by the source mutants


def _repoint_to_asset(directory: Path, filename: str, index: int) -> str:
    """Point the manifest row at another asset and make EVERY summary field agree with that
    asset's raw values. Integrity and the cross-check both pass, so only the admitted-asset
    rule can refuse. Raw bytes and both digests are untouched."""
    payload = json.loads((directory / filename).read_bytes().decode("utf-8"))
    name = payload[0]["universe"][index]["name"]
    context = payload[1][index]
    rows = _rows(directory)
    for row in rows:
        if row["file"] == filename:
            row["json_pointer_oraclePx"] = f"/1/{index}/oraclePx"
            row["coin"] = name
            row["oraclePx"] = context["oraclePx"]
            row["markPx"] = context["markPx"]
            row["funding"] = context["funding"]
    _write_rows(directory, rows)
    return name


def test_a_self_consistent_row_for_another_asset_is_still_not_admitted(tmp_path: Path):
    reads = _reads(tmp_path)
    name = _repoint_to_asset(reads, PRE_15, 1)
    assert name != "BTC"

    with pytest.raises(oracle.OracleRefused) as excinfo:
        oracle.load_reads(reads)
    assert excinfo.value.code == "ORACLE_COIN_NOT_ADMITTED"
    assert name in str(excinfo.value)


def _synthetic(name: str, ended: datetime, price: str) -> oracle.VerifiedRead:
    return oracle.VerifiedRead(
        file=name,
        label=name,
        kind="metaAndAssetCtxs",
        role="pre",
        hour_utc=HOUR_15,
        coin="BTC",
        sha256="0" * 64,
        byte_length=1,
        started=ended - timedelta(milliseconds=500),
        ended=ended,
        pointer="/1/0/oraclePx",
        oracle_price=Decimal(price),
    )


def test_selection_takes_the_latest_of_several_observations_at_or_before_the_event():
    """The rule is `closest at or before`, not `first`, `last written` or an average."""
    early = _synthetic(
        "early", datetime(2026, 9, 19, 14, 59, 50, tzinfo=UTC), "81000.0"
    )
    closest = _synthetic(
        "closest", datetime(2026, 9, 19, 14, 59, 58, tzinfo=UTC), "81581.4"
    )
    after = _synthetic("after", datetime(2026, 9, 19, 15, 0, 2, tzinfo=UTC), "82000.0")

    chosen = oracle.select_at_or_before([early, closest, after], EVENT_15)

    assert chosen is closest
    assert chosen.oracle_price == PRE_15_PX
    # not the earliest eligible, not the later observation, not their mean
    assert chosen is not early and chosen is not after
    assert chosen.oracle_price != (early.oracle_price + closest.oracle_price) / 2


def test_selection_refuses_when_nothing_ended_at_or_before_the_event():
    after = _synthetic("after", datetime(2026, 9, 19, 15, 0, 2, tzinfo=UTC), "82000.0")

    with pytest.raises(oracle.OracleRefused) as excinfo:
        oracle.select_at_or_before([after], EVENT_15)
    assert excinfo.value.code == "ORACLE_BRACKET_DOES_NOT_STRADDLE_EVENT"
