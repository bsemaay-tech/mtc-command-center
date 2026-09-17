"""Minimal scheduled oracle reader for WP-P0-12 step D-4 (owner O-3 "now", O-2 0.05 %, O-1 wait).

Read-only, public Hyperliquid Info API (no key, no credential surface, no writes to the venue).
At every full hour H inside the window it performs two bracketing reads of `metaAndAssetCtxs`
(H - 2 s and H + 2 s, host wall clock) and one `clearinghouseState` read for the owner's address
(H + 3 s) so the position size at the funding instant is witnessed beside the oracle price.
Every response is stored write-once (`xb`) as the original HTTP bytes with a `.sha256` sidecar, and one
JSON line per read is appended to `ORACLE_READS_MANIFEST.jsonl` (host clock, http status, sha256,
bytes, the coin's oraclePx/markPx if parseable). Nothing here is the reviewed tool of design note §3;
this is the capture action only. Stop early by creating `STOP` in the output directory.
Usage: python oracle_bracket_reader.py <out_dir> <hours> <coin>
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import pathlib
import sys
import time

import requests

INFO_URL = "https://api.hyperliquid.xyz/info"
ADDRESS = "0x1E265F5E39957E08ed02A120ceFA33A9bd46AC49"
TOLERANCE = "0.05%"  # owner O-2, recorded for the later adapter


def utcnow() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def write_once(path: pathlib.Path, data: bytes) -> None:
    with open(path, "xb") as fh:
        fh.write(data)
        fh.flush()
    with open(str(path) + ".sha256", "x", encoding="ascii") as fh:
        fh.write(sha256(data) + "\n")


def read(out: pathlib.Path, kind: str, payload: dict, label: str, coin: str) -> None:
    started = utcnow()
    try:
        resp = requests.post(INFO_URL, json=payload, timeout=20)
        raw = resp.content
        status = resp.status_code
    except Exception as exc:  # noqa: BLE001 - the failure itself is recorded
        raw = f"REQUEST_FAILED: {type(exc).__name__}: {exc}".encode()
        status = -1
    ended = utcnow()
    name = f"{label}_{kind}.json" if status == 200 else f"{label}_{kind}_ERROR.txt"
    write_once(out / name, raw)
    row = {
        "label": label,
        "kind": kind,
        "request": payload,
        "started_utc": started.isoformat(timespec="milliseconds"),
        "ended_utc": ended.isoformat(timespec="milliseconds"),
        "http_status": status,
        "file": name,
        "bytes": len(raw),
        "sha256": sha256(raw),
        "clock": "host wall clock (Windows), not the venue's",
        "tolerance_owner_O2": TOLERANCE,
    }
    if status == 200:
        try:
            parsed = json.loads(raw)
            if kind == "metaAndAssetCtxs":
                universe = parsed[0]["universe"]
                ctxs = parsed[1]
                for i, asset in enumerate(universe):
                    if asset.get("name") == coin:
                        ctx = ctxs[i]
                        row["coin"] = coin
                        row["json_pointer_oraclePx"] = f"/1/{i}/oraclePx"
                        row["oraclePx"] = ctx.get("oraclePx")
                        row["markPx"] = ctx.get("markPx")
                        row["funding"] = ctx.get("funding")
                        break
            elif kind == "clearinghouseState":
                row["assetPositions"] = [
                    {"coin": ap["position"].get("coin"), "szi": ap["position"].get("szi")}
                    for ap in parsed.get("assetPositions", [])
                ]
                row["venue_time_ms"] = parsed.get("time")
        except Exception as exc:  # noqa: BLE001
            row["parse_note"] = f"{type(exc).__name__}: {exc}"
    with open(out / "ORACLE_READS_MANIFEST.jsonl", "a", encoding="ascii") as fh:
        fh.write(json.dumps(row, sort_keys=True) + "\n")
    print(row.get("label"), kind, status, row.get("oraclePx", row.get("assetPositions", "")), flush=True)


def sleep_until(target: dt.datetime, out: pathlib.Path) -> bool:
    while True:
        if (out / "STOP").exists():
            return False
        remaining = (target - utcnow()).total_seconds()
        if remaining <= 0:
            return True
        time.sleep(min(remaining, 20.0))


def main() -> int:
    out = pathlib.Path(sys.argv[1])
    hours = int(sys.argv[2])
    coin = sys.argv[3] if len(sys.argv) > 3 else "BTC"
    out.mkdir(parents=True, exist_ok=True)
    now = utcnow()
    next_hour = (now + dt.timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    if (next_hour - now).total_seconds() > 3600 - 5:
        next_hour = now.replace(minute=0, second=0, microsecond=0)
    print(f"start {now.isoformat(timespec='seconds')} first hour {next_hour.isoformat()} hours {hours} coin {coin}", flush=True)
    for n in range(hours):
        hour = next_hour + dt.timedelta(hours=n)
        label = hour.strftime("H%Y%m%dT%H%M%SZ")
        if not sleep_until(hour - dt.timedelta(seconds=2), out):
            print("STOP file seen; exiting", flush=True)
            return 0
        read(out, "metaAndAssetCtxs", {"type": "metaAndAssetCtxs"}, label + "_pre", coin)
        sleep_until(hour + dt.timedelta(seconds=2), out)
        read(out, "metaAndAssetCtxs", {"type": "metaAndAssetCtxs"}, label + "_post", coin)
        sleep_until(hour + dt.timedelta(seconds=3), out)
        read(out, "clearinghouseState", {"type": "clearinghouseState", "user": ADDRESS}, label + "_state", coin)
    print("window complete", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
