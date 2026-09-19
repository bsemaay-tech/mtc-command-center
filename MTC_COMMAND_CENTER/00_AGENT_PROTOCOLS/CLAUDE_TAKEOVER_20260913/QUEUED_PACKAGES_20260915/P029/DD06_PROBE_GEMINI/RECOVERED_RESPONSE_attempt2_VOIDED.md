# SUPPLEMENTAL DETECTION REVIEW: WP-P0-29 DD-06 TESTNET PROBE (SLICE 2)

**Reviewer Role:** Supplemental Read-Only Detection Reviewer (`SUPPLEMENTAL_UNEXECUTED`)  
**Target Commit:** `69377d6b9b3322266c1716c78d82cc68d62ac8ef` (HEAD, slice 2)  
**Packet Root:** [`C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915)  
**Authority Reference:** `OD-20260915-P029-DD06-TESTNET-PROBE-PREP-1` (Preparation only; execution strictly requires separate owner authorization: "probe steps approved")

---

## 1. Findings (Slice 2)

The two REQUIRED findings and two NITs reported in the voided attempt 1 on `71cde24e` have been closed in `69377d6b`:
- **F-1 (Closed):** The docstring in [`subject/dd06_agent_withdraw_probe.py:15-20`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/dd06_agent_withdraw_probe.py#L15-L20) and packet [§3 line 26](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/DD06_TESTNET_PROBE_STEP_PACKET_20260915.md#L26) explicitly state that a non-refused `withdraw3` would cause funds to **leave the venue account** to the owner's Arbitrum bridge-chain address.
- **F-2 (Closed):** [`classify_refusal_text()`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/dd06_agent_withdraw_probe.py#L179-L190) classifies venue error messages into `AUTHORIZATION`, `VALIDATION`, or `UNCLASSIFIED`. Lines 421–429 mandate that **only** `AUTHORIZATION` refusals allow `DD06_REFUSALS_OBSERVED`; any validation-shaped rejection (e.g. self-send, minimum amount) makes the outcome `DD06_INCONCLUSIVE` (exit code 2).
- **F-3 (Closed):** Step packet [§3 line 25](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/DD06_TESTNET_PROBE_STEP_PACKET_20260915.md#L25) abort conditions now explicitly instruct the owner to inspect the testnet UI and flatten any position by hand if the control order fills.
- **F-4 (Closed):** [`write_record()`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/dd06_agent_withdraw_probe.py#L465-L468) enforces a fail-closed check raising `ProbeRefused` if any `0x`-prefixed 40-hex address survives redaction in the serialized JSON.

Two non-blocking observational NITs remain in slice 2:

### Finding 1 (NIT) — Unprefixed 40-Hex Address Boundary
- **Location:** [`subject/dd06_agent_withdraw_probe.py:57`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/dd06_agent_withdraw_probe.py#L57), [`subject/dd06_agent_withdraw_probe.py:465-468`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/dd06_agent_withdraw_probe.py#L465-L468)
- **Description:** `_HEX40 = re.compile(r"(?i)0x[0-9a-f]{40}")` strictly matches `0x`-prefixed addresses. While EVM addresses almost universally include `0x`, any unprefixed 40-hex address returned by an atypical venue error body would not be scrubbed by `_HEX40` nor tripped by the write guard (which enforces `_HEX40`). Standard 40-hex git SHAs or hashes preclude removing the prefix requirement without false positives, so retaining `0x` is defensible, but the boundary assumption is noted.

### Finding 2 (NIT) — Order ID Regex Parsing Dependency
- **Location:** [`subject/dd06_agent_withdraw_probe.py:433-440`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/dd06_agent_withdraw_probe.py#L433-L440)
- **Description:** `_resting_oid` extracts the resting order ID using regex `re.search(r'"oid":\s*(\d+)', text)` against the stringified response. If the SDK response structure or key naming for resting orders varies across environments, `_resting_oid` returns `None`, which triggers fail-closed abort `ABORTED_CONTROL_ARM_NOT_ACCEPTED` (line 327) rather than leaving an untracked order. The fail-closed behavior is safe, but parsing the dictionary structure directly before redaction would be slightly cleaner.

---

## 2. Task Assessment & Verdict Table

| # | Task Area | Verdict | Summary Assessment |
|---|---|---|---|
| 1 | Mainnet / Real-Money Reachability | **PASS** | `TESTNET_URL` is hard-coded (`https://api.hyperliquid-testnet.xyz`) and passed explicitly to both `Info` and `Exchange` (preventing the SDK default of `MAINNET_API_URL`). `refuse_unless_testnet` rejects any `--network` other than `"testnet"` and aborts if `HL_LIVE_ACK` is present. `refuse_master_key` ensures agent address ≠ account master address. No mainnet credentials are read. |
| 2 | Key Custody | **PASS** | Key is resolved via `resolve_hyperliquid_credentials()`, converted to `LocalAccount`, and `del api_key` executes immediately. The `approve_agent` return tuple `(response, agent_key)` drops index `[1]` immediately. Private keys (32 bytes = 64 hex) cannot survive `_HEX64` redaction. `write_record` validates serialized JSON against both `_HEX64` and `_HEX40` before writing; mutant `m2` confirms fail-closed behavior. |
| 3 | Funds Cannot Leave | **PASS** | Task 3(a) docstring critique is **moot**: docstring and step packet explicitly acknowledge that a non-refused `withdraw3` would move 6 test-USDC off the venue account to the bridge chain. 6 USDC clears bridge minimum (5 USDC) + fee (1 USDC) to eliminate amount refusals. Task 3(b) self-transfers (`usdSend`, `spotSend`) cannot yield false positives: `classify_refusal_text` requires `AUTHORIZATION` text; any self-send validation refusal yields `DD06_INCONCLUSIVE`. |
| 4 | Classification Honesty | **PASS** | Both HTTP 200 `status: err` envelopes and HTTP 4xx `ClientError` (e.g. 422 user/wallet not found) map to `REFUSED` and have their message text classified by `classify_refusal_text`. Transport errors (5xx, network drops) map to `ERROR`, yielding `DD06_INCONCLUSIVE`. Full redacted error strings are stored in `data["error"]` / `data["response"]`. |
| 5 | State Left Behind | **PASS** | Resting control order placed at 90% of mid, >= $10.5 notional. If filled during resting period, probe does not trade or flatten; step packet §3 line 25 abort condition instructs owner to inspect UI and flatten by hand. Cancel failure aborts loudly with `ABORTED_CONTROL_CANCEL_FAILED`. An unrefused `approveAgent` drops the generated key and packet §3 step 4 directs the owner to prune `dd06-probe-candidate` from the testnet UI. |
| 6 | Stop Rule and Tests | **PASS** | `STOP_ON_NOT_REFUSED = True` halts sequence upon first non-refusal. Red mutants confirm test sensitivity: `LEAD_RED_ARM_m1.txt` proves stop-rule test fails when disabled; `LEAD_RED_ARM_m2.txt` proves write-record guard halts surviving keys; `LEAD_RED_ARM_m3.txt` proves classification tests fail when classifier is stubbed to return `AUTHORIZATION`. All 14 tests assert exact behaviors. |
| 7 | Packet Honesty | **PASS** | Step packet §3 precisely documents arms, amounts, destinations, exit codes (0 for `DD06_REFUSALS_OBSERVED`, 2 for finding/inconclusive/aborted, 3 for refusal to start), sub-account skipping, and explicit non-claim of mainnet parity. Abort conditions are complete. |
| 8 | Scope | **PASS** | `DIFF_STAT` confirms exactly 2 new files (`tools/dd06_agent_withdraw_probe.py` and `tests/test_dd06_agent_withdraw_probe.py`), +905 lines. Zero protected paths touched. Full bridge suite passes (1612 passed, 1 skipped, 1 warning). Ruff is clean; repo guard PASS. |

---

## 3. Exact Read Coverage

All file inspections were performed exclusively within [`C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915):

1. [`PACKET_SHA256SUMS.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/PACKET_SHA256SUMS.txt): lines 1–19 (complete)
2. [`subject/dd06_agent_withdraw_probe.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/dd06_agent_withdraw_probe.py): (559 lines total, complete in 4 ranges)
   - Lines 1–150
   - Lines 151–300 (continuation 1)
   - Lines 301–450 (continuation 2)
   - Lines 451–559 (continuation 3)
3. [`subject/test_dd06_agent_withdraw_probe.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/test_dd06_agent_withdraw_probe.py): (348 lines total, complete in 3 ranges)
   - Lines 1–150
   - Lines 151–300 (continuation 1)
   - Lines 301–348 (continuation 2)
4. [`subject/DD06_TESTNET_PROBE_STEP_PACKET_20260915.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/DD06_TESTNET_PROBE_STEP_PACKET_20260915.md): lines 1–45 (complete)
5. [`subject/COMMIT_HEAD.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/COMMIT_HEAD.txt): lines 1–32 (complete)
6. [`subject/DIFF_STAT_fcac0ac6_HEAD.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/DIFF_STAT_fcac0ac6_HEAD.txt): lines 1–4 (complete)
7. [`sources/SDK_0_24_0_SIGNATURES.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/sources/SDK_0_24_0_SIGNATURES.txt): lines 1–73 (complete)
8. [`sources/bridge_settings_fcac0ac6.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/sources/bridge_settings_fcac0ac6.py): lines 50–135 (covers required lines 60–120)
9. [`sources/smoke_p0_fcac0ac6.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/sources/smoke_p0_fcac0ac6.py): lines 1–80 and lines 235–344 (complete required ranges)
10. [`sources/SMOKE_P0_LEAD_NOTE_20260914.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/sources/SMOKE_P0_LEAD_NOTE_20260914.md): lines 1–35 (complete)
11. [`sources/DECISIONS_rows_DD06.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/sources/DECISIONS_rows_DD06.md): lines 1–5 (complete)
12. [`sources/LEAD_PYTEST_focused_slice2.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/sources/LEAD_PYTEST_focused_slice2.txt): lines 1–3 (complete)
13. [`sources/LEAD_PYTEST_full_bridge_slice2.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/sources/LEAD_PYTEST_full_bridge_slice2.txt): lines 1–4 (complete)
14. [`sources/LEAD_RUFF_slice2.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/sources/LEAD_RUFF_slice2.txt): lines 1–2 (complete)
15. [`sources/LEAD_RED_ARM_m1.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/sources/LEAD_RED_ARM_m1.txt): lines 1–25 (complete)
16. [`sources/LEAD_RED_ARM_m2.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/sources/LEAD_RED_ARM_m2.txt): lines 1–40 (complete; inspected via native ripgrep search matching all lines due to non-ASCII Windows path sequence in traceback)
17. [`sources/LEAD_RED_ARM_m3.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/sources/LEAD_RED_ARM_m3.txt): lines 1–4 (complete)
18. [`sources/LEAD_GUARD_slice2.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/sources/LEAD_GUARD_slice2.txt): lines 1–5 (complete)
19. [`sources/RECOVERED_RESPONSE_attempt1_VOIDED.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/sources/RECOVERED_RESPONSE_attempt1_VOIDED.md): lines 1–121 (complete)

---

## 4. Not Verified

1. **No Live Execution:** No script was executed; no live Python interpreter or testnet runner was run by this reviewer.
2. **No Venue Access:** No HTTP requests or WebSocket connections were made to Hyperliquid testnet or mainnet.
3. **No Host Access:** No connection to host KVM2 (`srv1856225`), `/etc/mtc-bridge/mtc-bridge.env`, or host systemd services.
4. **Live Venue Error Strings:** The exact literal error strings returned live by Hyperliquid testnet for `withdraw_from_bridge` and self-transfers were not observed live; verification relies on SDK signatures and precedent fixture traces.

---

```json
{
  "part": "DD06_PROBE_GEMINI",
  "verdict": "PASS-WITH-NITS",
  "evidence_class": "SUPPLEMENTAL_UNEXECUTED",
  "findings": [
    {
      "id": "FINDING-1",
      "severity": "NIT",
      "path": "subject/dd06_agent_withdraw_probe.py:57",
      "summary": "_HEX40 regex requires 0x prefix; unprefixed 40-hex addresses would not be matched or blocked by write_record assertion."
    },
    {
      "id": "FINDING-2",
      "severity": "NIT",
      "path": "subject/dd06_agent_withdraw_probe.py:438",
      "summary": "_resting_oid relies on regex searching stringified response for oid; returns None and fails closed if response formatting changes."
    }
  ],
  "required_scope_unread": []
}
```

GEMINI_READ_ONLY_OK
