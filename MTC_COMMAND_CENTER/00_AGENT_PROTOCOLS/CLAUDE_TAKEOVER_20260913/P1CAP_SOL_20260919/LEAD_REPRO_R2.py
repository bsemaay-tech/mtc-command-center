"""Independent reproduction of Sol's REQUIRED R-2 finding against 1029d6e9's committed bytes.
Drives account_state_query directly with a real CapturingInfo whose .session is a fake that
returns a 2xx response with a body that is not valid JSON. CapturingInfo.post's ValueError
fallback returns {"error": "..."}  -- a dict -- and account_state_query's isinstance(parsed, dict)
check accepts any dict, so the claim is this should succeed instead of refusing."""
import sys, tempfile, pathlib
sys.path.insert(0, r"C:\tmp\P1CAP_20260914\IBKR_PAPER_BRIDGE")
from tools import capture_own_account_evidence as cae


class FakeResponse:
    def __init__(self, content: bytes, status_code: int = 200):
        self.content = content
        self.status_code = status_code
        self.text = content.decode("utf-8", errors="replace")
        self.headers = {}


class FakeSession:
    def __init__(self, response):
        self.response = response

    def post(self, url, json=None, timeout=None):
        return self.response


info = cae.CapturingInfo("https://testnet.example")
# A 2xx response whose body is not valid JSON -- e.g. an upstream proxy/error page.
info.session = FakeSession(FakeResponse(b"<html>502 Bad Gateway</html>", status_code=200))

with tempfile.TemporaryDirectory() as td:
    out_dir = pathlib.Path(td) / "out"
    out_dir.mkdir()
    manifest: list = []
    try:
        cae.account_state_query(
            info, out_dir, manifest,
            address="0x1111111111111111111111111111111111111111",
            base_url="https://testnet.example",
        )
        print("NO REFUSAL RAISED -- account_state_query ACCEPTED the parse-error sentinel as valid state (bug reproduced)")
        print("account_state.json contents:", (out_dir / "account_state.json").read_bytes())
        print("manifest entries:", manifest)
    except cae.CaptureRefused as exc:
        print("REFUSED (bug NOT reproduced / already fixed):", exc.code, exc.detail)
