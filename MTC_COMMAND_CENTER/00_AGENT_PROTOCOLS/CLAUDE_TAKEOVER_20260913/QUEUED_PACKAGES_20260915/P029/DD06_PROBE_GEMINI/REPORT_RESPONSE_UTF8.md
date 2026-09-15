# SUPPLEMENTAL DETECTION REVIEW: WP-P0-29 DD-06 TESTNET PROBE (SLICE 3 / ATTEMPT 3)

**Reviewer Role:** Independent Read-Only Detection Reviewer (`SUPPLEMENTAL_UNEXECUTED`)  
**Target Commit:** `1af85067234632ff057b4212e7599f8003a85ee6` (HEAD, slice 3)  
**Packet Root:** [`C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915)  
**Authority Reference:** `OD-20260915-P029-DD06-TESTNET-PROBE-PREP-1` (Preparation only; execution requires explicit owner word)

---

## 1. Findings

The previous slice 1 findings (Findings 1 and 2 REQUIRED) were closed in slice 2 (`69377d6b`) and remain closed in slice 3 (`1af85067`):
- **Docstring Accuracy:** [`subject/dd06_agent_withdraw_probe.py:15-20`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/dd06_agent_withdraw_probe.py#L15-L20) explicitly states that a non-refused `withdraw3` would cause funds to **leave the venue account** to the owner's bridge-chain address.
- **Classification Honesty:** [`classify_refusal_text()`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/dd06_agent_withdraw_probe.py#L196-L207) partitions error messages into `AUTHORIZATION`, `VALIDATION`, and `UNCLASSIFIED`. Only `AUTHORIZATION` allows `DD06_REFUSALS_OBSERVED`; any validation or unclassified refusal triggers `DD06_INCONCLUSIVE` (exit code 2).
- **Control Order Fill Handling:** [`DD06_TESTNET_PROBE_STEP_PACKET_20260915.md:25`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/DD06_TESTNET_PROBE_STEP_PACKET_20260915.md#L25) abort conditions instruct the owner to inspect the testnet UI and flatten any position by hand if the control order fills.
- **Address Redaction Assertion:** [`write_record()`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/dd06_agent_withdraw_probe.py#L511-L514) enforces an explicit fail-closed guard against surviving `0x`-prefixed 40-hex addresses in the serialized record.

In slice 3 (`1af85067`), after the real testnet run `dd06-testnet-20260915T183321Z-r1` rejected the control arm with `Price must be divisible by tick size. asset=3`:
- Control pricing is routed through [`round_hl_price`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/dd06_agent_withdraw_probe.py#L45) (at most 5 significant figures, bounded decimals).
- `per_status_errors()` parses `response.data.statuses[].error` so that an `ok` envelope containing per-order errors is classified `REFUSED` for that request.
- `S0_spot_user_state` records the unifiedAccount's spot USDC balance.

Two observational NITs remain:

### Finding 1 (NIT) — Unprefixed 40-Hex Address Boundary Assumption
- **Location:** [`subject/dd06_agent_withdraw_probe.py:59`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/dd06_agent_withdraw_probe.py#L59), [`subject/dd06_agent_withdraw_probe.py:511-514`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/dd06_agent_withdraw_probe.py#L511-L514)
- **Description:** `_HEX40 = re.compile(r"(?i)0x[0-9a-f]{40}")` requires a `0x` prefix. If an unexpected venue error body produced a bare 40-hex string without `0x`, it would not be redacted by `_HEX40` and would not trigger the `write_record` address assertion (which also checks `_HEX40`). Because private keys are 64 hex (`_HEX64`, which does match with or without `0x`), private keys cannot leak through this boundary. Unprefixed 40-hex matching would cause collisions with Git SHAs, so retaining `0x` is defensible.

### Finding 2 (NIT) — Regex Parsing for Order ID
- **Location:** [`subject/dd06_agent_withdraw_probe.py:479-486`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/dd06_agent_withdraw_probe.py#L479-L486)
- **Description:** [`_resting_oid`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/dd06_agent_withdraw_probe.py#L479) parses the order ID using `re.search(r'"oid":\s*(\d+)', text)` against the stringified response text. If the envelope format changes unexpectedly, `_resting_oid` returns `None`. This triggers fail-closed abort `ABORTED_CONTROL_ARM_NOT_ACCEPTED` ([line 372-374](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/dd06_agent_withdraw_probe.py#L372-L374)), which prevents continuing with an uncancelled resting order. Parsing the dictionary before redaction would be slightly cleaner.

---

## 2. Task Assessment & Verdict Table

| # | Task Area | Verdict | Summary Assessment |
|---|---|---|---|
| 1 | Mainnet / Real-Money Reachability | **PASS** | [`TESTNET_URL`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/dd06_agent_withdraw_probe.py#L47) is explicitly passed to both [`Info`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/dd06_agent_withdraw_probe.py#L588) and [`Exchange`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/dd06_agent_withdraw_probe.py#L589), overriding SDK default `MAINNET_API_URL` ([`SDK_0_24_0_SIGNATURES.txt:4`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/sources/SDK_0_24_0_SIGNATURES.txt#L4)). [`refuse_unless_testnet`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/dd06_agent_withdraw_probe.py#L209) blocks any `--network` other than `"testnet"` and aborts if `HL_LIVE_ACK` is present. [`refuse_master_key`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/dd06_agent_withdraw_probe.py#L220) rejects master keys. No mainnet credentials or endpoints can be reached. |
| 2 | Key Custody | **PASS** | `HL_API_WALLET_KEY` is wrapped into `Account.from_key()` and immediately deleted via `del api_key` ([lines 569-571](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/dd06_agent_withdraw_probe.py#L569-L571)). Element [1] of the `approve_agent` return tuple is dropped before recording ([lines 256-258](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/dd06_agent_withdraw_probe.py#L256-L258)). `_HEX64` matches any 64-hex key with or without `0x`. [`write_record()`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/dd06_agent_withdraw_probe.py#L488) fail-closed guards against surviving `_HEX64` and `_HEX40` strings, confirmed by mutant test `LEAD_RED_ARM_m2.txt`. |
| 3 | Funds Cannot Leave | **PASS** | (a) Task 3(a) docstring critique is **moot**: docstring and packet explicitly state that a non-refused `withdraw3` would move 6 test-USDC to the bridge chain. 6 USDC clears the 5 USDC min + 1 USDC fee. (b) Self-transfers (`usdSend`, `spotSend`) cannot yield false DD-06 evidence: [`classify_refusal_text`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/dd06_agent_withdraw_probe.py#L196) requires `AUTHORIZATION` markers; any self-send validation rejection maps to `VALIDATION` -> `DD06_INCONCLUSIVE`. |
| 4 | Classification Honesty | **PASS** | HTTP 200 `status: err`, HTTP 4xx `ClientError`, and per-status `error` entries inside `status: ok` envelopes are classified as `REFUSED`. Transport failures (5xx, network drops) map to `ERROR` -> `DD06_INCONCLUSIVE`. Automated outcome `DD06_REFUSALS_OBSERVED` strictly requires `refusal_class == "AUTHORIZATION"` on every arm. |
| 5 | State Left Behind | **PASS** | Resting control order placed at 90% mid, >= $10.5 notional. If filled, the probe aborts and does not trade; packet §3 line 25 directs the owner to flatten manually on testnet UI. Cancel failure aborts with `ABORTED_CONTROL_CANCEL_FAILED`. An unrefused `approveAgent` key is discarded; packet §3 step 4 directs pruning `dd06-probe-candidate` from testnet UI. |
| 6 | Stop Rule and Tests | **PASS** | [`STOP_ON_NOT_REFUSED = True`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/dd06_agent_withdraw_probe.py#L56) halts immediately upon the first non-refusal. Red mutant tests confirm test sensitivity: `LEAD_RED_ARM_m1.txt` (stop rule disabled), `LEAD_RED_ARM_m2.txt` (redaction disabled / write guard fires), `LEAD_RED_ARM_m3.txt` (stubbed classifier), and `LEAD_RED_ARM_slice3_old_probe_new_tests.txt` (3 tests fail against slice 2 bytes). |
| 7 | Packet Honesty | **PASS** | Packet §3 precisely matches script parameters, exit codes (0 = observed, 2 = finding/inconclusive/aborted, 3 = refused to start), sub-account skipping, and explicit non-claim of mainnet parity ("mainnet parity assumed, not proven"). |
| 8 | Scope | **PASS** | [`DIFF_STAT_fcac0ac6_HEAD.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/DIFF_STAT_fcac0ac6_HEAD.txt) confirms exactly 2 new files under `IBKR_PAPER_BRIDGE/` (+1016 lines total). No protected paths touched ([`LEAD_GUARD_slice3.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/sources/LEAD_GUARD_slice3.txt)). Full bridge suite passes (1614 passed, 1 skipped, 1 warning, exit 0). Ruff clean. |
| 9 | r1 Record Verification | **PASS** | In `kvm2_dd06_probe_run_OUTPUT.redacted.txt`, run `dd06-testnet-20260915T183321Z-r1` aborted at control arm with `ABORTED_CONTROL_ARM_NOT_ACCEPTED`, exit 2. No transfer arm ran; nothing rested. This matches packet §3 step 2 and §4 semantics exactly. |
| 10 | Slice 3 Semantics & Per-Status Safety | **PASS** | [`control_order_size`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/dd06_agent_withdraw_probe.py#L228) routes price through [`round_hl_price`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/dd06_agent_withdraw_probe.py#L45) (for mid 76974.0, price rounds to 69270.0, 4 significant figures, <= 5 sig figs, wire valid). [`classify_response`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/dd06_agent_withdraw_probe.py#L143) returns `REFUSED` on `ok` envelopes only if `statuses[].error` exists; a genuine success has no `statuses[].error` and evaluates to `NOT_REFUSED`. |
| 11 | r2 Reading Soundness & Unified Account | **PASS** | S0 now records `S0_spot_user_state` (`usdc_total` and `usdc_hold`). A unifiedAccount's USDC sits in spot (perp margin shows 0.0). With spot USDC recorded, refusals cannot be attributed to zero balance. Combined with `AUTHORIZATION` classification, an r2 `DD06_REFUSALS_OBSERVED` outcome will be read soundly under packet §4. |

---

## 3. Exact Read Coverage

All 27 files in [`C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/PACKET_SHA256SUMS.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/PACKET_SHA256SUMS.txt) were read using native tools with at most 150 lines per view:

1. [`PACKET_SHA256SUMS.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/PACKET_SHA256SUMS.txt): lines 1–27 (complete)
2. [`subject/COMMIT_HEAD.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/COMMIT_HEAD.txt): lines 1–23 (complete)
3. [`subject/DIFF_STAT_fcac0ac6_HEAD.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/DIFF_STAT_fcac0ac6_HEAD.txt): lines 1–4 (complete)
4. [`subject/dd06_agent_withdraw_probe.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/dd06_agent_withdraw_probe.py): (605 lines total, complete in 5 ranges)
   - Lines 1–150
   - Lines 151–300 (continuation 1)
   - Lines 301–450 (continuation 2)
   - Lines 451–600 (continuation 3)
   - Lines 601–605 (continuation 4)
5. [`subject/test_dd06_agent_withdraw_probe.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/test_dd06_agent_withdraw_probe.py): (413 lines total, complete in 3 ranges)
   - Lines 1–150
   - Lines 151–300 (continuation 1)
   - Lines 301–413 (continuation 2)
6. [`subject/DD06_TESTNET_PROBE_STEP_PACKET_20260915.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/subject/DD06_TESTNET_PROBE_STEP_PACKET_20260915.md): lines 1–45 (complete)
7. [`sources/SDK_0_24_0_SIGNATURES.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/sources/SDK_0_24_0_SIGNATURES.txt): lines 1–73 (complete)
8. [`sources/bridge_settings_fcac0ac6.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/sources/bridge_settings_fcac0ac6.py): lines 50–130 (covers required lines 60–120)
9. [`sources/smoke_p0_fcac0ac6.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/sources/smoke_p0_fcac0ac6.py): lines 1–80 and lines 235–343 (complete required ranges)
10. [`sources/SMOKE_P0_LEAD_NOTE_20260914.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/sources/SMOKE_P0_LEAD_NOTE_20260914.md): lines 1–35 (complete)
11. [`sources/DECISIONS_rows_DD06.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/sources/DECISIONS_rows_DD06.md): lines 1–5 (complete)
12. [`sources/LEAD_PYTEST_focused_slice2.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/sources/LEAD_PYTEST_focused_slice2.txt): lines 1–3 (complete)
13. [`sources/LEAD_PYTEST_full_bridge_slice2.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/sources/LEAD_PYTEST_full_bridge_slice2.txt): lines 1–4 (complete)
14. [`sources/LEAD_RUFF_slice2.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/sources/LEAD_RUFF_slice2.txt): lines 1–2 (complete)
15. [`sources/LEAD_RED_ARM_m1.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/sources/LEAD_RED_ARM_m1.txt): lines 1–25 (complete)
16. [`sources/LEAD_RED_ARM_m2.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/sources/LEAD_RED_ARM_m2.txt): lines 1–41 (complete)
17. [`sources/LEAD_RED_ARM_m3.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/sources/LEAD_RED_ARM_m3.txt): lines 1–4 (complete)
18. [`sources/LEAD_GUARD_slice2.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/sources/LEAD_GUARD_slice2.txt): lines 1–5 (complete)
19. [`sources/RECOVERED_RESPONSE_attempt1_VOIDED.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/sources/RECOVERED_RESPONSE_attempt1_VOIDED.md): lines 1–121 (complete)
20. [`sources/RECOVERED_RESPONSE_attempt2_VOIDED.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/sources/RECOVERED_RESPONSE_attempt2_VOIDED.md): lines 1–111 (complete)
21. [`sources/kvm2_dd06_probe_run.sh`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/sources/kvm2_dd06_probe_run.sh): lines 1–29 (complete)
22. [`sources/kvm2_dd06_probe_run_OUTPUT.redacted.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/sources/kvm2_dd06_probe_run_OUTPUT.redacted.txt): lines 1–64 (complete)
23. [`sources/LEAD_GUARD_slice3.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/sources/LEAD_GUARD_slice3.txt): lines 1–15 (complete)
24. [`sources/LEAD_PYTEST_focused_slice3.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/sources/LEAD_PYTEST_focused_slice3.txt): lines 1–2 (complete)
25. [`sources/LEAD_PYTEST_full_bridge_slice3.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/sources/LEAD_PYTEST_full_bridge_slice3.txt): lines 1–32 (complete)
26. [`sources/LEAD_RED_ARM_slice3_old_probe_new_tests.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/sources/LEAD_RED_ARM_slice3_old_probe_new_tests.txt): lines 1–5 (complete)
27. [`sources/LEAD_RUFF_slice3.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915/sources/LEAD_RUFF_slice3.txt): lines 1–2 (complete)

---

## 4. Not Verified

1. **No Execution:** This reviewer did not execute any Python script, test runner, CLI command, or shell tool.
2. **No Venue Access:** No HTTP requests or WebSocket connections were made to Hyperliquid testnet or mainnet.
3. **No Host Access:** No connection to host KVM2 (`srv1856225`), `/etc/mtc-bridge/mtc-bridge.env`, or host systemd services.
4. **Unexecuted r2 Run:** The planned r2 run has not yet executed; analysis of r2 semantics is based on the deterministic code path and r1 evidence.

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
      "path": "subject/dd06_agent_withdraw_probe.py:59",
      "summary": "_HEX40 regex requires 0x prefix; an unprefixed 40-hex address would not be matched or blocked by write_record assertion."
    },
    {
      "id": "FINDING-2",
      "severity": "NIT",
      "path": "subject/dd06_agent_withdraw_probe.py:484",
      "summary": "_resting_oid parses order ID from stringified response text using regex and fails closed to ABORTED_CONTROL_ARM_NOT_ACCEPTED if structure changes."
    }
  ],
  "required_scope_unread": []
}
```

GEMINI_READ_ONLY_OK
