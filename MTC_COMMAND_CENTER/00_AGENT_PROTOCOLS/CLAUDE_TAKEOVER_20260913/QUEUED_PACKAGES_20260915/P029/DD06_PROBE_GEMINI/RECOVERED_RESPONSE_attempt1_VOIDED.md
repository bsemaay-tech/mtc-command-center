# SUPPLEMENTAL DETECTION REVIEW: WP-P0-29 DD-06 TESTNET PROBE

**Reviewer Role:** Supplemental Read-Only Detection Reviewer (`SUPPLEMENTAL_UNEXECUTED`)  
**Target Commit:** `71cde24e0c712da3be2a4c442d9e7fdb65b20094`  
**Packet Root:** `_gemini_packets_20260913/DD06_PROBE_20260915`  
**Authority Reference:** `OD-20260915-P029-DD06-TESTNET-PROBE-PREP-1` (Preparation only; execution requires explicit owner approval)

---

## 1. Findings

### Finding 1 (REQUIRED) — Inaccurate Fund Movement Claim for `withdraw3`
- **Location:** `subject/dd06_agent_withdraw_probe.py:15-18`
- **Description:** The docstring claims: *"Destinations are the account's own master address: usdSend/spotSend would be self-transfers; withdraw3 would be a bridge withdrawal to the SAME address on the bridge chain (owner-controlled, testnet faucet money)..."*. Per the SDK source (`SDK_0_24_0_SIGNATURES.txt:46-55`), `withdraw_from_bridge` executes a bridge withdrawal (`type: "withdraw3"`) sending funds from the Hyperliquid venue account to Arbitrum. If this arm were accepted by the venue, funds **would leave the venue account**. Even though the recipient address on Arbitrum is owner-controlled and holds faucet money, conflating bridge withdrawal with zero-movement self-transfers is technically inaccurate in the script's docstring. The step packet (`subject/DD06_TESTNET_PROBE_STEP_PACKET_20260915.md:22`) correctly acknowledges *"if NOT refused, 6 test-USDC leave the venue to an address you control"*, but the script docstring must be aligned to explicitly state that funds leave the exchange account if not refused.

### Finding 2 (REQUIRED) — Classification Overclaims on Validation Errors / Self-Transfers
- **Location:** `subject/dd06_agent_withdraw_probe.py:125-133`, `136-144`, `358-360`
- **Description:** `classify_response` maps any dict with `status == "err"` to `"REFUSED"`, and `classify_exception` maps any `ClientError` to `"REFUSED"`. For `usd_transfer` and `spot_transfer`, the destination is `account_address` (a self-transfer). If the venue rejects the transfer for validation/ledger rules (e.g. `"cannot transfer to self"`, invalid transfer recipient, or nonce issue) rather than agent authorization restrictions, the probe increments `refused += 1` and concludes `DD06_REFUSALS_OBSERVED` (exit code 0). While packet §4 requires the Lead to manually inspect refusal text post-run, the automated classification and exit code 0 overclaim success. The classifier should distinguish authorization refusals (matching messages such as `"must be user"`, `"does not exist"`, or agent/permission wording) from validation errors, or flag generic error envelopes as unverified/inconclusive.

### Finding 3 (NIT) — Unhandled Control Order Fill Scenario
- **Location:** `subject/dd06_agent_withdraw_probe.py:276-289`; `subject/DD06_TESTNET_PROBE_STEP_PACKET_20260915.md:24-25`
- **Description:** The S1 control order places a limit bid at 90% of mid. While unfillable in stable conditions, extreme testnet volatility or a flash move could execute or partially fill the order before cancellation. The probe contains no position query or flattening routine (unlike `smoke_p0.py`'s `_flatten_if_changed`). If filled, the cancel attempt will fail or report an order status of filled, aborting with `ABORTED_CONTROL_ARM_NOT_ACCEPTED` or `ABORTED_CONTROL_CANCEL_FAILED`. Step packet §3 step 4 and §3 abort conditions mention cancelling resting orders by hand, but omit instructing the owner to check for and flatten any executed BTC position on the testnet UI.

### Finding 4 (NIT) — Address Redaction Format Assumption
- **Location:** `subject/dd06_agent_withdraw_probe.py:55`, `404-405`
- **Description:** `_HEX40 = re.compile(r"(?i)0x[0-9a-f]{40}")` strictly requires a `0x` prefix. If any raw address without `0x` were returned in an error payload, it would not be redacted by `_HEX40`. Furthermore, `write_record` enforces a fail-closed guard solely on surviving 64-hex strings (`_HEX64`), with no safety assertion against surviving 40-hex addresses (relying solely on the preceding regex replacement).

---

## 2. Task Assessment & Verdict Table

| # | Task Area | Verdict | Summary Assessment |
|---|---|---|---|
| 1 | Mainnet / Real-Money Reachability | **PASS** | `TESTNET_URL` is explicitly passed to both `Info` and `Exchange`; `refuse_unless_testnet` rejects any `--network` other than `"testnet"` and rejects if `HL_LIVE_ACK` is present; `refuse_master_key` ensures the key does not match the master address. |
| 2 | Key Custody | **PASS** | Key is read via `resolve_hyperliquid_credentials()`, converted to `LocalAccount`, and immediately deleted (`del api_key`). Element [1] of `approve_agent` return tuple is dropped before recording. `write_record` fail-closed guard on `_HEX64` verified sound by red arm `m2`. |
| 3 | Funds Cannot Leave Venue | **REQUEST_CHANGES** | `withdraw_from_bridge` removes funds from the venue account to Arbitrum; docstring claims destinations mean no funds leave, which is technically inaccurate. `usd_transfer`/`spot_transfer` to self risk false-positive refusals on validation errors (Findings 1 & 2). |
| 4 | Classification Honesty | **PASS-WITH-NITS** | Full redacted responses and error strings are preserved in the step records, enabling Lead post-run differentiation. However, automated classification treats all `status: err` / `ClientError` as `REFUSED` without inspecting message content (Finding 2). |
| 5 | State Left Behind | **PASS-WITH-NITS** | Order cancellation failure aborts loudly (`ABORTED_CONTROL_CANCEL_FAILED`). If `approve_agent` were accepted, the key was dropped, requiring owner pruning via UI (packet covers this). If control order fills, manual position flattening is needed (Finding 3). |
| 6 | Stop Rule and Tests | **PASS** | `STOP_ON_NOT_REFUSED` halts immediately upon finding non-refusal. Red mutant tests in `LEAD_RED_ARM_m1.txt` (stop rule disabled) and `LEAD_RED_ARM_m2.txt` (redaction disabled / write_record guard triggered) confirm test sensitivity. |
| 7 | Packet Honesty | **PASS-WITH-NITS** | Step packet accurately captures parameters, scope, exit codes, and explicitly states mainnet parity is assumed, not proven. Needs explicit instruction to flatten position if control order fills. |
| 8 | Scope | **PASS** | Exactly two files modified (`tools/dd06_agent_withdraw_probe.py` and `tests/test_dd06_agent_withdraw_probe.py`). Repo guard PASS; full bridge suite 1610 passed, Ruff clean. |

---

## 3. Exact Read Coverage

All reads performed inside `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915`:

1. `PACKET_SHA256SUMS.txt`: lines 1–17 (complete)
2. `subject/dd06_agent_withdraw_probe.py`: (495 lines total)
   - Lines 1–150
   - Lines 151–300 (continuation 1)
   - Lines 301–450 (continuation 2)
   - Lines 451–495 (continuation 3; complete)
3. `subject/test_dd06_agent_withdraw_probe.py`: (304 lines total)
   - Lines 1–150
   - Lines 151–300 (continuation 1)
   - Lines 301–304 (continuation 2; complete)
4. `subject/DD06_TESTNET_PROBE_STEP_PACKET_20260915.md`: lines 1–44 (complete)
5. `subject/COMMIT_HEAD.txt`: lines 1–31 (complete)
6. `subject/DIFF_STAT_fcac0ac6_HEAD.txt`: lines 1–4 (complete)
7. `sources/SDK_0_24_0_SIGNATURES.txt`: lines 1–73 (complete)
8. `sources/bridge_settings_fcac0ac6.py`: lines 60–120
9. `sources/smoke_p0_fcac0ac6.py`: lines 1–80 and lines 235–343
10. `sources/SMOKE_P0_LEAD_NOTE_20260914.md`: lines 1–35 (complete)
11. `sources/DECISIONS_rows_DD06.md`: lines 1–5 (complete)
12. `sources/LEAD_PYTEST_focused.txt`: lines 1–2 (complete)
13. `sources/LEAD_PYTEST_full_bridge.txt`: lines 1–5 (complete)
14. `sources/LEAD_RUFF.txt`: lines 1–2 (complete)
15. `sources/LEAD_RED_ARM_m1.txt`: lines 1–25 (complete)
16. `sources/LEAD_RED_ARM_m2.txt`: lines 1–40 (complete; inspected via native ripgrep regex due to non-ASCII Windows path sequence in pytest trace)
17. `sources/LEAD_GUARD.txt`: lines 1–9 (complete)

---

## 4. Not Verified

1. **No Live Execution:** No script was executed; no Python interpreter was invoked by this reviewer.
2. **No Venue Access:** No HTTP requests or WebSocket connections were made to Hyperliquid testnet or mainnet.
3. **No Host Access:** No access to host KVM2 (`srv1856225`), `/etc/mtc-bridge/mtc-bridge.env`, or live systemd services.
4. **Live Error Messages:** Actual Hyperliquid testnet response envelopes for self-transfers (`usd_transfer` to self) and `withdraw_from_bridge` were not observed live.

---

```json
{
  "part": "DD06_PROBE_GEMINI",
  "verdict": "REQUEST_CHANGES",
  "evidence_class": "SUPPLEMENTAL_UNEXECUTED",
  "findings": [
    {
      "id": "FINDING-1",
      "severity": "REQUIRED",
      "path": "subject/dd06_agent_withdraw_probe.py:15-18",
      "summary": "withdraw_from_bridge moves funds off the venue exchange to Arbitrum; docstring claim that destinations being own address means funds do not leave is technically inaccurate and must be corrected."
    },
    {
      "id": "FINDING-2",
      "severity": "REQUIRED",
      "path": "subject/dd06_agent_withdraw_probe.py:125-133",
      "summary": "classify_response and classify_exception overclaim by classifying any status: err or ClientError as REFUSED, which would falsely treat self-transfer validation rejections as agent authorization refusals."
    },
    {
      "id": "FINDING-3",
      "severity": "NIT",
      "path": "subject/DD06_TESTNET_PROBE_STEP_PACKET_20260915.md:24-25",
      "summary": "Packet abort conditions do not instruct owner to manually inspect and flatten positions on the testnet UI if the control order fills."
    },
    {
      "id": "FINDING-4",
      "severity": "NIT",
      "path": "subject/dd06_agent_withdraw_probe.py:55",
      "summary": "_HEX40 regex requires 0x prefix and write_record lacks an explicit assertion against surviving 40-hex addresses."
    }
  ],
  "required_scope_unread": []
}
```

GEMINI_READ_ONLY_OK
