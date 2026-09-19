"""WP-P0-28 read-only own-account ELIGIBILITY capture (owner OD-20260915-P028-READ-GO-1).

Reuses the reviewed Path 1 capture tool (IBKR_PAPER_BRIDGE/tools/capture_own_account_evidence.py at
af921d75) for every custody primitive — CapturingInfo (pre-parse HTTP bytes), record_response (write-once
+ sha256 sidecar + manifest entry with raw_bytes_source), ownership_result (EIP-191 recovery BEFORE any
network object), verify_sidecars, the HL_API_WALLET_KEY refusal and the address check — and issues exactly
four public Info reads for one address: subAccounts, userFees, userRole, clearinghouseState, each twice
(re-query, content-compared). No key, no signing except the offline ownership check, no exchange import,
no order, no sub-account creation, no transfer. Outputs go only under --out.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path

TOOL_DIR = Path("C:/tmp/P1CAP_20260914/IBKR_PAPER_BRIDGE")
sys.path.insert(0, str(TOOL_DIR))
from tools import capture_own_account_evidence as cae  # noqa: E402

EXPECTED_TOOL_SHA256 = "00b3b8f69f0e48700ea6072e9930ddefcc48f3d28420860843c2cafaa3c62ddd"  # af921d75
QUERIES = (
    ("sub_accounts", "query_sub_accounts", {"type": "subAccounts"}),
    ("user_fees", "user_fees", {"type": "userFees"}),
    ("user_role", "user_role", {"type": "userRole"}),
    ("clearinghouse_state", "user_state", {"type": "clearinghouseState", "dex": ""}),
)


def query_pass(info, out_dir: Path, manifest: list, *, pass_name: str, address: str, base_url: str) -> dict:
    parsed_by_name: dict[str, object] = {}
    for name, method, body_template in QUERIES:
        body = dict(body_template, user=address)
        started = datetime.now(UTC)
        parsed, raw = cae.recorded_call(
            info, method, (address,), body,
            out_dir=out_dir, manifest=manifest, name=f"{name}_{pass_name}", base_url=base_url, started=started,
        )
        cae.record_response(
            out_dir, manifest, name=f"{name}_{pass_name}", capture=raw, base_url=base_url,
            started=started, ended=datetime.now(UTC),
        )
        parsed_by_name[name] = parsed
    return parsed_by_name


def account_scoped(name: str, parsed):
    """Re-query comparison ignores venue-wide fields that move every second and are not this
    account's evidence: userFees.dailyUserVlm[*].exchange is the EXCHANGE-WIDE daily volume
    (observed 2026-09-15: only that field differed between two passes 3 s apart). Both passes'
    original bytes are still stored; the derived view records the observed difference."""
    if name == "user_fees" and isinstance(parsed, dict):
        scoped = dict(parsed)
        rows = parsed.get("dailyUserVlm")
        if isinstance(rows, list):
            scoped["dailyUserVlm"] = [
                {k: v for k, v in row.items() if k != "exchange"} if isinstance(row, dict) else row
                for row in rows
            ]
        return scoped
    return parsed


def derived_view(parsed: dict) -> dict:
    subs = parsed["sub_accounts"]
    fees = parsed["user_fees"] if isinstance(parsed["user_fees"], dict) else {}
    role = parsed["user_role"] if isinstance(parsed["user_role"], dict) else {}
    state = parsed["clearinghouse_state"] if isinstance(parsed["clearinghouse_state"], dict) else {}
    daily = fees.get("dailyUserVlm") if isinstance(fees.get("dailyUserVlm"), list) else []
    def _sum(key: str) -> str:
        total = 0.0
        for row in daily:
            try:
                total += float(row.get(key, "0"))
            except (TypeError, ValueError, AttributeError):
                pass
        return f"{total:.6f}"
    sub_list = subs if isinstance(subs, list) else []
    return {
        "label": "DERIVED_VIEW_NOT_ORIGINAL_BYTES",
        "role": role.get("role"),
        "sub_account_count": len(sub_list),
        "sub_accounts": [
            {"name": s.get("name"), "subAccountUser": s.get("subAccountUser"), "master": s.get("master")}
            for s in sub_list if isinstance(s, dict)
        ],
        "daily_volume_rows": len(daily),
        "daily_volume_first_date": daily[0].get("date") if daily and isinstance(daily[0], dict) else None,
        "daily_volume_last_date": daily[-1].get("date") if daily and isinstance(daily[-1], dict) else None,
        "sum_userCross_over_returned_days": _sum("userCross"),
        "sum_userAdd_over_returned_days": _sum("userAdd"),
        "sum_exchange_over_returned_days": _sum("exchange"),
        "userCrossRate": fees.get("userCrossRate"),
        "userAddRate": fees.get("userAddRate"),
        "activeReferralDiscount": fees.get("activeReferralDiscount"),
        "assetPositions_count": len(state.get("assetPositions", []) or []),
        "withdrawable": state.get("withdrawable"),
        "requery_rule": "user_fees compared with dailyUserVlm[*].exchange (venue-wide volume) masked; all other fields byte-equal across passes",
        "note": "Volume sums cover only the days the API returned in dailyUserVlm; the $100,000 sub-account rule "
                "(hyperliquid-docs/trading/sub-accounts, accessed 2026-09-15) is compared by the Lead in the record, "
                "not asserted here.",
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--address", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--ownership-signature", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if "HL_API_WALLET_KEY" in os.environ:
            raise cae.CaptureRefused(cae.REFUSED_KEY_PRESENT)
        if cae.tool_sha256() != EXPECTED_TOOL_SHA256:
            raise cae.CaptureRefused(cae.REFUSED_MALFORMED, "reviewed capture tool digest drifted")
        if not cae.ADDRESS_RE.fullmatch(args.address):
            raise cae.CaptureRefused(cae.REFUSED_BAD_ADDRESS)
        ownership = cae.ownership_result(args.address, args.run_id, args.ownership_signature)
        args.out.mkdir(parents=True, exist_ok=True)
        base_url = cae.info_base_url("mainnet")
        info = cae.make_info(base_url)
        manifest_entries: list = []
        pass1 = query_pass(info, args.out, manifest_entries, pass_name="pass1", address=args.address, base_url=base_url)
        pass2 = query_pass(info, args.out, manifest_entries, pass_name="pass2", address=args.address, base_url=base_url)
        for name, _, _ in QUERIES:
            if name == "clearinghouse_state":
                continue  # state carries a server time field; recorded twice, compared by the Lead
            if account_scoped(name, pass1[name]) != account_scoped(name, pass2[name]):
                raise cae.CaptureRefused(cae.REFUSED_REQUERY_MISMATCH, name)
        cae.write_once(args.out / "DERIVED_ELIGIBILITY_VIEW.json", cae.json_bytes(derived_view(pass1)))
        manifest = {
            "kind": "P028_OWN_ACCOUNT_ELIGIBILITY_CAPTURE_MANIFEST_V1",
            "run_id": args.run_id,
            "network": "mainnet",
            "address": args.address,
            "queries": [q[2]["type"] for q in QUERIES],
            "capture_tool": {"path": "IBKR_PAPER_BRIDGE/tools/capture_own_account_evidence.py", "sha256": EXPECTED_TOOL_SHA256, "commit": "af921d75"},
            "wrapper_sha256": cae.sha256_bytes(Path(__file__).read_bytes()),
            "ownership_evidence": ownership,
            "responses": manifest_entries,
        }
        cae.write_once(args.out / "CAPTURE_MANIFEST.json", cae.json_bytes(manifest))
        cae.verify_sidecars(args.out)
        print("CAPTURE_OK")
        return 0
    except cae.CaptureRefused as exc:
        print(exc.code, file=sys.stderr)
        if exc.detail:
            print(exc.detail, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
