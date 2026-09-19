"""Read-only Hyperliquid own-account evidence capture for WP-P0-12 Path 1.

This tool only uses ``hyperliquid.info.Info`` read methods. It refuses when an
API wallet key is present, imports no exchange client, and writes raw response
bytes plus SHA-256 sidecars before creating derived views.

Window semantics: the requested interval is half-open ``[start, end)`` in
milliseconds (the intake rule); the Info API's ``endTime`` is inclusive, so a row
at exactly ``end`` is stored in the original bytes but excluded from the derived
view and the identity sets. Rows outside the requested range are refused.

Ownership evidence: ``--ownership-signature`` requires ``--run-id`` (the signed
message names the run id) and is verified before any network object exists or any
file is written.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from eth_account import Account
from eth_account.messages import encode_defunct
from eth_utils.exceptions import ValidationError
from hyperliquid.info import Info
from hyperliquid.utils import constants

HL_FILLS_PAGE_LIMIT = 2000
HL_INFO_PAGE_LIMIT = 500

REFUSED_KEY_PRESENT = "CAPTURE_REFUSED_KEY_PRESENT"
REFUSED_TRUNCATED = "CAPTURE_REFUSED_TRUNCATED"
REFUSED_REQUERY_MISMATCH = "CAPTURE_REFUSED_REQUERY_MISMATCH"
REFUSED_QUERY_FAILED = "CAPTURE_REFUSED_QUERY_FAILED"
REFUSED_MALFORMED = "CAPTURE_REFUSED_MALFORMED"
REFUSED_BAD_ADDRESS = "CAPTURE_REFUSED_BAD_ADDRESS"
REFUSED_BAD_SIDECAR = "CAPTURE_REFUSED_SIDECAR_MISMATCH"
REFUSED_BAD_SIGNATURE = "CAPTURE_REFUSED_OWNERSHIP_SIGNATURE"
REFUSED_RUN_ID_REQUIRED = "CAPTURE_REFUSED_RUN_ID_REQUIRED"

# The intake declares one complete half-open interval [start_inclusive, end_exclusive);
# the Hyperliquid Info API treats endTime as inclusive, so rows at exactly end_ms are
# legitimately returned and are EXCLUDED here (never refused).
WINDOW_SEMANTICS = "half_open_start_inclusive_end_exclusive_ms"

RAW_SOURCE_HTTP = "http_response_content"
RAW_SOURCE_TEST_DOUBLE = "reserialized_parsed_json_TEST_DOUBLE_ONLY"

ADDRESS_RE = re.compile(r"^0x[0-9a-fA-F]{40}$")


class CaptureRefused(RuntimeError):
    def __init__(
        self, code: str, detail: str = "", error_capture: RawCapture | None = None
    ) -> None:
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code
        self.detail = detail
        self.error_capture = error_capture


@dataclass(frozen=True)
class RawCapture:
    endpoint: str
    body: dict[str, Any]
    raw: bytes
    source: str = RAW_SOURCE_HTTP


class CapturingInfo(Info):
    """Info client that preserves HTTP bytes before the SDK parses JSON."""

    def __init__(self, base_url: str) -> None:
        super().__init__(
            base_url,
            skip_ws=True,
            meta={"universe": []},
            spot_meta={"tokens": [], "universe": []},
        )
        self._captures: list[RawCapture] = []

    def post(self, url_path: str, payload: Any = None) -> Any:
        payload = payload or {}
        response = self.session.post(
            self.base_url + url_path, json=payload, timeout=self.timeout
        )
        raw = bytes(response.content)
        self._captures.append(RawCapture(url_path, dict(payload), raw))
        self._handle_exception(response)
        try:
            return json.loads(raw.decode("utf-8"))
        except ValueError:
            return {"error": f"Could not parse JSON: {response.text}"}

    def pop_capture(self) -> RawCapture:
        return self._captures.pop()


def ownership_message(address: str, run_id: str) -> str:
    return (
        "P012 Path 1 own-account evidence capture\n"
        f"address: {address.lower()}\n"
        f"run_id: {run_id}"
    )


def parse_utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() != UTC.utcoffset(parsed):
        raise CaptureRefused(REFUSED_MALFORMED, "timestamp must be UTC")
    return parsed.astimezone(UTC)


def ms(value: datetime) -> int:
    return int(value.timestamp() * 1000)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def write_once(path: Path, data: bytes) -> str:
    digest = sha256_bytes(data)
    try:
        with path.open("xb") as handle:
            handle.write(data)
    except FileExistsError as exc:
        raise CaptureRefused(REFUSED_MALFORMED, f"output exists: {path.name}") from exc
    sidecar = path.with_name(path.name + ".sha256")
    try:
        with sidecar.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(digest + "\n")
    except FileExistsError as exc:
        raise CaptureRefused(
            REFUSED_MALFORMED, f"output exists: {sidecar.name}"
        ) from exc
    return digest


def info_base_url(network: str) -> str:
    return (
        constants.TESTNET_API_URL if network == "testnet" else constants.MAINNET_API_URL
    )


def sdk_version() -> str:
    try:
        return importlib.metadata.version("hyperliquid-python-sdk")
    except importlib.metadata.PackageNotFoundError:
        return "UNKNOWN"


def tool_sha256() -> str:
    return sha256_bytes(Path(__file__).read_bytes())


def make_info(base_url: str) -> Info:
    return CapturingInfo(base_url)


def consume_capture(
    info: Any, parsed: Any, endpoint: str, body: dict[str, Any]
) -> RawCapture:
    """Return the pre-parse HTTP bytes captured by ``CapturingInfo``.

    The fallback (re-serialised parsed JSON) exists only for test doubles without
    ``pop_capture``; it is labelled as such in every manifest entry so a reviewer
    can never mistake it for original response bytes. ``make_info`` always returns
    a ``CapturingInfo`` on the real path.
    """
    pop = getattr(info, "pop_capture", None)
    if callable(pop):
        return pop()
    return RawCapture(endpoint, body, json_bytes(parsed), RAW_SOURCE_TEST_DOUBLE)


def call_info(
    info: Any,
    method_name: str,
    args: tuple[Any, ...],
    endpoint: str,
    body: dict[str, Any],
) -> tuple[Any, RawCapture]:
    before = len(getattr(info, "_captures", []))
    try:
        parsed = getattr(info, method_name)(*args)
    except Exception as exc:
        detail = type(exc).__name__
        status = getattr(exc, "status_code", None)
        if status is not None:
            detail = f"{detail} status={status}"
        error_capture = None
        if len(getattr(info, "_captures", [])) > before:
            # keep the error response bytes: the caller records them before refusing
            error_capture = info.pop_capture()
        raise CaptureRefused(REFUSED_QUERY_FAILED, detail, error_capture) from exc
    return parsed, consume_capture(info, parsed, endpoint, body)


def row_time(row: Any) -> int:
    if not isinstance(row, dict):
        raise CaptureRefused(REFUSED_MALFORMED, "row is not an object")
    value = row.get("time")
    if isinstance(value, bool) or not isinstance(value, int):
        raise CaptureRefused(REFUSED_MALFORMED, "row time is not an integer")
    return value


def fill_identity(row: Any) -> str:
    if not isinstance(row, dict):
        raise CaptureRefused(REFUSED_MALFORMED, "fill row is not an object")
    tid = row.get("tid")
    if tid is not None:
        if isinstance(tid, bool) or not isinstance(tid, int):
            raise CaptureRefused(REFUSED_MALFORMED, "fill tid is malformed")
        return f"tid:{tid}"
    # NIT-5 (exact-Opus read of af921d75): the former hash+oid+time fallback could merge two
    # identical partial fills of one order in one block (an undercount). Every venue fill carries
    # a tid (r1/r2 captures: all rows); a fill without one cannot be counted without ambiguity, so
    # the shape is refused rather than guessed
    raise CaptureRefused(
        REFUSED_MALFORMED, "fill without tid (identity would be ambiguous)"
    )


def funding_coin(row: dict[str, Any]) -> Any:
    delta = row.get("delta") if isinstance(row.get("delta"), dict) else {}
    return row.get("coin", delta.get("coin"))


def funding_identity(row: Any) -> str:
    if not isinstance(row, dict):
        raise CaptureRefused(REFUSED_MALFORMED, "funding row is not an object")
    h = row.get("hash")
    t = row.get("time")
    coin = funding_coin(row)
    if not isinstance(h, str) or isinstance(t, bool) or not isinstance(t, int):
        raise CaptureRefused(REFUSED_MALFORMED, "funding identity is malformed")
    if not isinstance(coin, str) or not coin:
        # two coins can settle in the same block: hash+time alone would collide
        raise CaptureRefused(REFUSED_MALFORMED, "funding identity has no coin")
    return f"hash-time-coin:{h}:{t}:{coin}"


def request_body(kind: str, address: str, start_ms: int, end_ms: int) -> dict[str, Any]:
    if kind == "fills":
        return {
            "type": "userFillsByTime",
            "user": address,
            "startTime": start_ms,
            "endTime": end_ms,
            "aggregateByTime": False,
        }
    return {
        "type": "userFunding",
        "user": address,
        "startTime": start_ms,
        "endTime": end_ms,
    }


def record_response(
    out_dir: Path,
    manifest: list[dict[str, Any]],
    *,
    name: str,
    capture: RawCapture,
    base_url: str,
    started: datetime,
    ended: datetime,
) -> str:
    rel = f"{name}.json"
    digest = write_once(out_dir / rel, capture.raw)
    manifest.append(
        {
            "file": rel,
            "request": {"endpoint": capture.endpoint, "body": capture.body},
            "response_sha256": digest,
            "raw_bytes_source": capture.source,
            "byte_length": len(capture.raw),
            "wall_clock_utc_start": started.isoformat().replace("+00:00", "Z"),
            "wall_clock_utc_end": ended.isoformat().replace("+00:00", "Z"),
            "base_url": base_url,
            "sdk_version": sdk_version(),
            "tool_sha256": tool_sha256(),
        }
    )
    return digest


def paged_query(
    info: Any,
    out_dir: Path,
    manifest: list[dict[str, Any]],
    *,
    kind: str,
    pass_name: str,
    address: str,
    start_ms: int,
    end_ms: int,
    base_url: str,
) -> list[dict[str, Any]]:
    method = "user_fills_by_time" if kind == "fills" else "user_funding_history"
    limit = HL_FILLS_PAGE_LIMIT if kind == "fills" else HL_INFO_PAGE_LIMIT
    identity = fill_identity if kind == "fills" else funding_identity
    cursor = start_ms
    page = 0
    rows_by_id: dict[str, dict[str, Any]] = {}
    while True:
        page += 1
        name = f"{kind}_{pass_name}_page{page:03d}"
        body = request_body(kind, address, cursor, end_ms)
        started = datetime.now(UTC)
        parsed, raw = recorded_call(
            info,
            method,
            (address, cursor, end_ms),
            body,
            out_dir=out_dir,
            manifest=manifest,
            name=name,
            base_url=base_url,
            started=started,
        )
        ended = datetime.now(UTC)
        digest = record_response(
            out_dir,
            manifest,
            name=name,
            capture=raw,
            base_url=base_url,
            started=started,
            ended=ended,
        )
        if not isinstance(parsed, list):
            raise CaptureRefused(REFUSED_MALFORMED, f"{kind} response is not a list")
        page_max = cursor
        previous_time: int | None = None
        for index, row in enumerate(parsed):
            ident = identity(row)
            t = row_time(row)
            if previous_time is not None and t < previous_time:
                # NIT-2: the cursor arithmetic below assumes ascending pages (the SDK's order);
                # a descending page would set the next cursor past unread rows - refuse instead
                raise CaptureRefused(
                    REFUSED_MALFORMED,
                    f"{kind} page not in ascending time order ({ident})",
                )
            previous_time = t
            # the API is asked for [cursor, end_ms] (endTime inclusive); anything outside
            # the requested range is a malformed response, never silently admitted.
            # R-1 (exact-Sol read of 1029d6e9): checking only the original start_ms let a
            # later short page repeat a row from before the CURRENT cursor - a stale or
            # duplicate-window row that requery could agree on just as easily as a real one.
            # cursor still holds this page's request floor here (it is only advanced to
            # page_max after this loop), so it is a strictly tighter, still-correct bound.
            if t < cursor:
                raise CaptureRefused(
                    REFUSED_MALFORMED, f"{kind} row before requested cursor ({ident})"
                )
            if t > end_ms:
                raise CaptureRefused(
                    REFUSED_MALFORMED, f"{kind} row after requested end ({ident})"
                )
            page_max = max(page_max, t)
            if t >= end_ms:
                # half-open window: a row at exactly end_ms is outside [start, end)
                continue
            existing = rows_by_id.get(ident)
            enriched = {
                "identity": ident,
                "row": row,
                "capture_sha256": digest,
                "json_pointer": f"/{index}",
            }
            if existing is not None:
                if existing["row"] != row:
                    raise CaptureRefused(
                        REFUSED_MALFORMED, f"{kind} identity conflict ({ident})"
                    )
                continue
            rows_by_id[ident] = enriched
        if len(parsed) < limit:
            return list(rows_by_id.values())
        if page_max <= cursor:
            raise CaptureRefused(REFUSED_TRUNCATED, f"{kind} cursor stalled")
        cursor = page_max


def recorded_call(
    info: Any,
    method_name: str,
    args: tuple[Any, ...],
    body: dict[str, Any],
    *,
    out_dir: Path,
    manifest: list[dict[str, Any]],
    name: str,
    base_url: str,
    started: datetime,
) -> tuple[Any, RawCapture]:
    """``call_info`` that stores the error response bytes (with sidecar and manifest
    entry ``<name>_ERROR``) before re-raising, so a failed query is never evidence-free."""
    try:
        return call_info(info, method_name, args, "/info", body)
    except CaptureRefused as exc:
        if exc.error_capture is not None:
            record_response(
                out_dir,
                manifest,
                name=f"{name}_ERROR",
                capture=exc.error_capture,
                base_url=base_url,
                started=started,
                ended=datetime.now(UTC),
            )
            raise CaptureRefused(
                exc.code, f"{exc.detail}; error bytes kept as {name}_ERROR.json"
            ) from exc
        raise


def account_state_query(
    info: Any,
    out_dir: Path,
    manifest: list[dict[str, Any]],
    *,
    address: str,
    base_url: str,
) -> None:
    body = {"type": "clearinghouseState", "user": address, "dex": ""}
    started = datetime.now(UTC)
    parsed, raw = recorded_call(
        info,
        "user_state",
        (address,),
        body,
        out_dir=out_dir,
        manifest=manifest,
        name="account_state",
        base_url=base_url,
        started=started,
    )
    ended = datetime.now(UTC)
    # NIT-3: the bytes are kept before the shape is judged, as paged_query does
    record_response(
        out_dir,
        manifest,
        name="account_state",
        capture=raw,
        base_url=base_url,
        started=started,
        ended=ended,
    )
    if not isinstance(parsed, dict):
        raise CaptureRefused(
            REFUSED_MALFORMED,
            "account state is not an object (bytes kept as account_state.json)",
        )
    # R-2 (exact-Sol read of 1029d6e9): CapturingInfo.post's ValueError fallback for a 2xx
    # response with a non-JSON body returns {"error": ...} - a dict, which passed the check
    # above. Every real clearinghouseState response carries assetPositions; requiring it
    # rejects that parse-failure sentinel (and any other dict that isn't real account state)
    # while every existing capture and test double already satisfies it.
    if "assetPositions" not in parsed:
        raise CaptureRefused(
            REFUSED_MALFORMED,
            "account state missing assetPositions (not a clearinghouseState object)",
        )


def fill_derived(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result = []
    for item in rows:
        row = item["row"]
        out = {
            "kind": "DERIVED_FILL",
            "coin": row.get("coin"),
            "fee": row.get("fee"),
            "feeToken": row.get("feeToken"),
            "time": row.get("time"),
            "crossed": row.get("crossed"),
            "side": row.get("side"),
            "px": row.get("px"),
            "sz": row.get("sz"),
            "capture_sha256": item["capture_sha256"],
            "json_pointer": item["json_pointer"],
        }
        if "tid" in row:
            out["tid"] = row.get("tid")
        else:
            out["hash"] = row.get("hash")
            out["oid"] = row.get("oid")
        if "closedPnl" in row:
            out["closedPnl"] = row.get("closedPnl")
        result.append(out)
    return result


def funding_derived(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result = []
    for item in rows:
        row = item["row"]
        delta = row.get("delta") if isinstance(row.get("delta"), dict) else {}
        result.append(
            {
                "kind": "DERIVED_FUNDING",
                "hash": row.get("hash"),
                "time": row.get("time"),
                "coin": row.get("coin", delta.get("coin")),
                "usdc": row.get("usdc", delta.get("usdc")),
                "fundingRate": row.get("fundingRate", delta.get("fundingRate")),
                "szi": row.get("szi", delta.get("szi")),
                "capture_sha256": item["capture_sha256"],
                "json_pointer": item["json_pointer"],
            }
        )
    return result


def read_signature(path: Path) -> str:
    # NIT-6: an unreadable or malformed signature file is a named refusal (exit 2), not a
    # raw exception (exit 1)
    try:
        raw = path.read_text(encoding="utf-8").strip()
    except (OSError, UnicodeDecodeError) as exc:
        raise CaptureRefused(
            REFUSED_BAD_SIGNATURE, f"signature file unreadable: {path.name}"
        ) from exc
    if raw.startswith("{"):
        try:
            value = json.loads(raw).get("signature")
        except (json.JSONDecodeError, AttributeError) as exc:
            raise CaptureRefused(
                REFUSED_BAD_SIGNATURE, "signature file is not a JSON object"
            ) from exc
        if not isinstance(value, str):
            raise CaptureRefused(REFUSED_BAD_SIGNATURE, "JSON missing signature")
        return value.strip()
    return raw


def ownership_result(
    address: str, run_id: str, signature_path: Path | None
) -> dict[str, Any]:
    if signature_path is None:
        return {"status": "OWNERSHIP_EVIDENCE: NOT_PROVIDED"}
    signature = read_signature(signature_path)
    message = ownership_message(address, run_id)
    try:
        recovered = Account.recover_message(
            encode_defunct(text=message), signature=signature
        )
    except (ValueError, TypeError, ValidationError) as exc:
        # NIT-6: a signature that cannot be parsed or recovered is a named refusal
        raise CaptureRefused(
            REFUSED_BAD_SIGNATURE, f"signature not recoverable: {type(exc).__name__}"
        ) from exc
    ok = recovered.lower() == address.lower()
    if not ok:
        raise CaptureRefused(REFUSED_BAD_SIGNATURE, "recovered address mismatch")
    # NIT-7: the exact signed text and the signature travel with the manifest, so the record is
    # complete without a file kept beside the tool. The message binds address + run_id only
    # (start / end / network are NOT signed) - a design change to the signed text would
    # invalidate the owner's earlier signatures and is the owner's call, not this slice's.
    return {
        "status": "OWNERSHIP_EVIDENCE: VERIFIED",
        "recovered_address": recovered,
        "message": message,
        "signature": signature,
        "binds": "address+run_id",
    }


def _sidecar_digest(path: Path) -> str:
    sidecar = path.with_name(path.name + ".sha256")
    try:
        return sidecar.read_text(encoding="utf-8").strip()
    except (OSError, UnicodeDecodeError) as exc:
        raise CaptureRefused(
            REFUSED_BAD_SIDECAR, f"sidecar unreadable: {sidecar.name}"
        ) from exc


def verify_sidecars(out_dir: Path) -> None:
    """``CAPTURE_VERIFY_OK`` means: every recorded response matches its sidecar AND the
    manifest's digest; every ``*.sha256`` in the directory (the derived view and the manifest
    included) names an existing file that hashes to it; and, when the manifest records
    ``derived_extraction_sha256`` (written from this version on), the derived view matches it.
    NIT-1 of the exact-Opus read of af921d75: the former check covered the responses only."""
    manifest_path = out_dir / "CAPTURE_MANIFEST.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        # NIT-6: a missing directory or manifest is a named refusal, not a raw exception
        raise CaptureRefused(
            REFUSED_BAD_SIDECAR, f"manifest unreadable: {manifest_path}"
        ) from exc
    if not isinstance(manifest, dict) or not isinstance(
        manifest.get("responses"), list
    ):
        raise CaptureRefused(REFUSED_BAD_SIDECAR, "manifest has no responses list")
    for entry in manifest["responses"]:
        path = out_dir / entry["file"]
        try:
            actual = sha256_bytes(path.read_bytes())
        except OSError as exc:
            raise CaptureRefused(REFUSED_BAD_SIDECAR, entry["file"]) from exc
        if actual != _sidecar_digest(path) or actual != entry["response_sha256"]:
            raise CaptureRefused(REFUSED_BAD_SIDECAR, entry["file"])
    for sidecar in sorted(out_dir.glob("*.sha256")):
        target = sidecar.with_name(sidecar.name[: -len(".sha256")])
        try:
            actual = sha256_bytes(target.read_bytes())
        except OSError as exc:
            raise CaptureRefused(
                REFUSED_BAD_SIDECAR, f"{sidecar.name} names a missing file"
            ) from exc
        if actual != _sidecar_digest(target):
            raise CaptureRefused(REFUSED_BAD_SIDECAR, target.name)
    recorded = manifest.get("derived_extraction_sha256")
    if recorded is not None:
        derived = out_dir / "DERIVED_EXTRACTION.json"
        try:
            actual = sha256_bytes(derived.read_bytes())
        except OSError as exc:
            raise CaptureRefused(REFUSED_BAD_SIDECAR, derived.name) from exc
        if actual != recorded:
            raise CaptureRefused(
                REFUSED_BAD_SIDECAR,
                "DERIVED_EXTRACTION.json differs from the manifest digest",
            )


def requery_check(
    kind: str, first: list[dict[str, Any]], second: list[dict[str, Any]]
) -> None:
    """Both passes must return the same identities AND the same row content."""
    rows_1 = {item["identity"]: item["row"] for item in first}
    rows_2 = {item["identity"]: item["row"] for item in second}
    for ident in sorted(set(rows_1) | set(rows_2)):
        if ident not in rows_1 or ident not in rows_2:
            raise CaptureRefused(
                REFUSED_REQUERY_MISMATCH, f"{kind} identity only in one pass: {ident}"
            )
        if rows_1[ident] != rows_2[ident]:
            raise CaptureRefused(
                REFUSED_REQUERY_MISMATCH, f"{kind} row content differs: {ident}"
            )


def run_capture(args: argparse.Namespace) -> dict[str, Any]:
    if "HL_API_WALLET_KEY" in os.environ:
        raise CaptureRefused(REFUSED_KEY_PRESENT)
    if not ADDRESS_RE.fullmatch(args.address):
        raise CaptureRefused(REFUSED_BAD_ADDRESS)
    start = parse_utc(args.start)
    end = parse_utc(args.end)
    if end < start:
        raise CaptureRefused(REFUSED_MALFORMED, "end before start")
    signature_path = getattr(args, "ownership_signature", None)
    run_id = getattr(args, "run_id", None)
    if signature_path is not None and not run_id:
        # the owner signs a message that names the run_id; a defaulted run_id could never verify
        raise CaptureRefused(
            REFUSED_RUN_ID_REQUIRED, "--run-id is required with --ownership-signature"
        )
    if not run_id:
        run_id = datetime.now(UTC).strftime("p012-path1-%Y%m%dT%H%M%SZ")
    # ownership evidence is verified BEFORE any network object exists and before any file
    # is written: a wrong signature leaves nothing behind
    ownership = ownership_result(args.address, run_id, signature_path)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    base_url = info_base_url(args.network)
    info = make_info(base_url)
    manifest_entries: list[dict[str, Any]] = []
    start_ms = ms(start)
    end_ms = ms(end)
    fills_1 = paged_query(
        info,
        out_dir,
        manifest_entries,
        kind="fills",
        pass_name="pass1",
        address=args.address,
        start_ms=start_ms,
        end_ms=end_ms,
        base_url=base_url,
    )
    funding_1 = paged_query(
        info,
        out_dir,
        manifest_entries,
        kind="funding",
        pass_name="pass1",
        address=args.address,
        start_ms=start_ms,
        end_ms=end_ms,
        base_url=base_url,
    )
    account_state_query(
        info, out_dir, manifest_entries, address=args.address, base_url=base_url
    )
    fills_2 = paged_query(
        info,
        out_dir,
        manifest_entries,
        kind="fills",
        pass_name="pass2",
        address=args.address,
        start_ms=start_ms,
        end_ms=end_ms,
        base_url=base_url,
    )
    funding_2 = paged_query(
        info,
        out_dir,
        manifest_entries,
        kind="funding",
        pass_name="pass2",
        address=args.address,
        start_ms=start_ms,
        end_ms=end_ms,
        base_url=base_url,
    )
    requery_check("fills", fills_1, fills_2)
    requery_check("funding", funding_1, funding_2)
    extraction = {
        "label": "DERIVED_VIEW_NOT_ORIGINAL_BYTES",
        "fills": fill_derived(fills_1),
        "funding": funding_derived(funding_1),
    }
    derived_digest = write_once(
        out_dir / "DERIVED_EXTRACTION.json", json_bytes(extraction)
    )
    manifest = {
        "kind": "P012_PATH1_OWN_ACCOUNT_CAPTURE_MANIFEST_V1",
        "run_id": run_id,
        # NIT-1: the derived view's digest is part of the manifest, so verify_sidecars binds it
        "derived_extraction_sha256": derived_digest,
        "network": args.network,
        "address": args.address,
        "coin": args.coin,
        "window": {
            "start": start.isoformat().replace("+00:00", "Z"),
            "end": end.isoformat().replace("+00:00", "Z"),
            "start_ms": start_ms,
            "end_ms": end_ms,
            "semantics": WINDOW_SEMANTICS,
        },
        "ownership_evidence": ownership,
        "responses": manifest_entries,
    }
    write_once(out_dir / "CAPTURE_MANIFEST.json", json_bytes(manifest))
    verify_sidecars(out_dir)
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--print-ownership-message")
    parser.add_argument("--run-id")
    parser.add_argument("--network", choices=("mainnet", "testnet"))
    parser.add_argument("--address")
    parser.add_argument("--coin", default="BTC")
    parser.add_argument("--start")
    parser.add_argument("--end")
    parser.add_argument("--out")
    parser.add_argument("--ownership-signature", type=Path)
    parser.add_argument("--verify-existing", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.print_ownership_message:
            if not args.address or not ADDRESS_RE.fullmatch(args.address):
                raise CaptureRefused(REFUSED_BAD_ADDRESS)
            print(ownership_message(args.address, args.print_ownership_message))
            return 0
        if args.verify_existing:
            verify_sidecars(args.verify_existing)
            print("CAPTURE_VERIFY_OK")
            return 0
        missing = [
            name
            for name in ("network", "address", "start", "end", "out")
            if getattr(args, name) is None
        ]
        if missing:
            raise CaptureRefused(REFUSED_MALFORMED, "missing " + ",".join(missing))
        run_capture(args)
        print("CAPTURE_OK")
        return 0
    except CaptureRefused as exc:
        print(exc.code, file=sys.stderr)
        if exc.detail:
            print(exc.detail, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
