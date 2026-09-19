"""Independent reproduction of Sol's REQUIRED R-1 finding against 1029d6e9's committed bytes
(worktree C:/tmp/P1CAP_20260914, unmodified). Drives paged_query directly through run_capture
with a hand-built fake Info double: page1 is FULL (2 rows, limit=2) ending at cursor t1; page2 is
SHORT (1 row) but its row's time is BEFORE the new cursor t1 (while still >= the original window
start) — the claim is that :362 checks only the constant start_ms, never the advancing cursor, so
this should be silently accepted instead of refused. Both passes return the identical sequence so
requery agrees (the "hidden" shape Sol described)."""
import sys, tempfile, argparse
sys.path.insert(0, r"C:\tmp\P1CAP_20260914\IBKR_PAPER_BRIDGE")
from tools import capture_own_account_evidence as cae

START_MS = 1789210800000
END_MS = 1789214400000
T0 = START_MS + 1000   # inside window, will become the "stale" page-2 row's time
T1 = START_MS + 5000   # inside window, later than T0; becomes cursor after page 1

def fill_row(tid, t):
    return {
        "coin": "BTC", "fee": "0.01", "feeToken": "USDC", "time": t, "tid": tid,
        "hash": f"0xfill{tid}", "oid": 1000 + tid, "closedPnl": "0.00",
        "crossed": True, "side": "B", "px": "60000", "sz": "0.001",
    }

PAGE1 = [fill_row(1, T0), fill_row(2, T1)]   # full page, 2 rows == limit
PAGE2 = [fill_row(3, T0)]                     # short page, but its row's time (T0) < cursor (T1)
SEQUENCE = [PAGE1, PAGE2, PAGE1, PAGE2]        # pass1: page1,page2 ; pass2 (requery): page1,page2 again

class FakeInfo:
    def __init__(self):
        self.calls = 0
    def user_fills_by_time(self, address, start_ms, end_ms):
        row = SEQUENCE[min(self.calls, len(SEQUENCE) - 1)]
        self.calls += 1
        return row
    def user_funding_history(self, address, start_ms, end_ms):
        return []
    def user_state(self, address):
        return {"assetPositions": []}

cae.HL_FILLS_PAGE_LIMIT = 2
cae.make_info = lambda base_url: FakeInfo()
cae.constants.TESTNET_API_URL = "https://testnet.example"

with tempfile.TemporaryDirectory() as td:
    ns = argparse.Namespace(
        network="testnet", address="0x1111111111111111111111111111111111111111",
        coin="BTC", start="2026-09-12T11:00:00Z", end="2026-09-12T12:00:00Z",
        out=td + "/out", ownership_signature=None, run_id="run-r1-repro",
    )
    try:
        manifest = cae.run_capture(ns)
        fills = [e for e in manifest.get("derived", {}).get("fills", [])] if "derived" in manifest else None
        print("NO REFUSAL RAISED -- capture SUCCEEDED (this is the bug Sol reported if true)")
        print("manifest ownership_evidence:", manifest.get("ownership_evidence", {}).get("status"))
        import json
        print(json.dumps(manifest.get("fills_derived", manifest.get("derived")), indent=2)[:1000])
    except cae.CaptureRefused as exc:
        print("REFUSED (bug NOT reproduced / already fixed):", exc.code, exc.detail)
