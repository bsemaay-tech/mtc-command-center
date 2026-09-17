# SUPPLEMENTAL DETECTION REVIEW: WP-P0-29 DD-06 TESTNET PROBE (T0 REPAIR ROUND 1)
**Commit:** `a46b2a9d` | **Target:** `feature/p029-dd06-testnet-probe-20260915` (`1af85067` + repair)  
**Role:** `SUPPLEMENTAL_UNEXECUTED` (Read-only detection reviewer)

---

## (a) Traces & Adversarial Analysis

### 1. Trace of `main()` on Patched Bytes
*File:* [`subject/dd06_agent_withdraw_probe_HEAD_complete.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R1_20260917/subject/dd06_agent_withdraw_probe_HEAD_complete.py#L677-L742)

- **Scenario A: `--network testnet`, no `HL_LIVE_ACK`, no token in environment**
  1. [`main()`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R1_20260917/subject/dd06_agent_withdraw_probe_HEAD_complete.py#L677) executes arguments parsing. Line 701 calls `refuse_unless_testnet("testnet", dict(os.environ))`. Since `network == "testnet"` and `HL_LIVE_ACK` is absent/empty, line 701 succeeds without exception.
  2. Line 702 calls `refuse_without_run_token(args.run_id, dict(os.environ))`.
  3. Inside [`refuse_without_run_token`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R1_20260917/subject/dd06_agent_withdraw_probe_HEAD_complete.py#L246-L255): line 250 reads `token = environ.get(RUN_TOKEN_ENV, "").strip()`. Line 251 evaluates `if not token or token != run_id:`. Since `token` is empty, **line 252 raises `ProbeRefused`**.
  4. Exception is caught at line 713 (`except ProbeRefused as exc:`), prints to stderr at line 714, and **exits with code 3 at line 715**.
  5. **Credential & SDK Confirmation:** `resolve_hyperliquid_credentials` (line 709) and the constructors `Info(...)` (line 728) and `Exchange(...)` (line 729) are situated strictly after line 702. Neither credential resolution nor SDK instantiation is reached.

- **Scenario B: Token set (`DD06_PROBE_RUN_TOKEN == run_id`), resolver returns a master key (`wallet.address.lower() == account_address.lower()`)**
  1. Lines 701 and 702 pass.
  2. Dynamic imports at lines 703–707 execute.
  3. Line 709 calls `resolve_hyperliquid_credentials()`, returning `(account_address, master_api_key, source)`.
  4. Line 710 derives `wallet = Account.from_key(api_key)`, and line 711 executes `del api_key`.
  5. Line 712 calls `refuse_master_key(wallet.address, account_address)`.
  6. Inside [`refuse_master_key`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R1_20260917/subject/dd06_agent_withdraw_probe_HEAD_complete.py#L258-L264): line 259 detects `agent_address.lower() == account_address.lower()` and **line 260 raises `ProbeRefused`**.
  7. Caught at line 713, prints to stderr at line 714, and **exits with code 3 at line 715**. Neither `Info` (line 728) nor `Exchange` (line 729) is constructed.

---

### 2. Trace of `offline` Fixture & Structural Offline-ness
*File:* [`subject/test_dd06_agent_withdraw_probe_HEAD_complete.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R1_20260917/subject/test_dd06_agent_withdraw_probe_HEAD_complete.py#L423-L456)

- **Target Attributes Replaced:**
  - `bridge.settings.resolve_hyperliquid_credentials` replaced with `_NeverDial("resolve_hyperliquid_credentials")` (line 446).
  - `hyperliquid.exchange.Exchange` replaced with `_NeverDial("Exchange")` (line 447).
  - `hyperliquid.info.Info` replaced with `_NeverDial("Info")` (line 448).
- **Import Interception Mechanics:**
  In [`dd06_agent_withdraw_probe.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R1_20260917/subject/dd06_agent_withdraw_probe_HEAD_complete.py#L704-L707), imports are deferred inside the body of `main()`:
  ```python
  from hyperliquid.exchange import Exchange
  from hyperliquid.info import Info
  from bridge.settings import resolve_hyperliquid_credentials
  ```
  Because pytest executes the `offline` fixture before calling `main()`, the module attributes on `bridge.settings`, `hyperliquid.exchange`, and `hyperliquid.info` are already substituted with `_NeverDial` instances. The runtime `from ... import ...` statements bind directly to those tripwires.
- **Environment Scrubbing:**
  Lines 449–455 call `monkeypatch.delenv(name, raising=False)` for `HL_LIVE_ACK`, `DD06_PROBE_RUN_TOKEN`, `HL_API_WALLET_KEY`, and `HL_ACCOUNT_ADDRESS`.
- **Usage Across `main()`-Calling Tests:**
  - `test_dry_run_needs_no_credentials_and_no_network` (lines 415–421): Calls `main(["--dry-run"])`, which returns at line 699 before reaching any gate, resolver, or SDK constructor, and independently scrubs credentials.
  - `test_main_refuses_mainnet_before_reading_any_credential` (lines 459–464): Uses `offline`.
  - `test_main_refuses_without_the_execution_token_before_reading_any_credential` (lines 467–478): Uses `offline`.
  - `test_main_refuses_a_master_key_after_the_gates_and_before_any_sdk_object` (lines 492–509): Uses `offline`.
  Every test calling `main()` without `--dry-run` explicitly binds the `offline` fixture.
- **Adversarial Failure Mode Analysis:**
  If a future commit completely deletes both `refuse_without_run_token` and the `HL_LIVE_ACK` gate in `refuse_unless_testnet`, execution in any fixture test calling `main()` continues to line 709 (`resolve_hyperliquid_credentials()`).
  Because `offline` replaces `resolve_hyperliquid_credentials` with `_NeverDial`, line 709 immediately raises `AssertionError: resolve_hyperliquid_credentials must never be reached from the fixture suite` (demonstrated in `LEAD_RED_DD06_R1_M5_token_gate_removed_from_main.txt`). Even if credentials were provided by test setup (as in `test_main_refuses_a_master_key`), lines 728 and 729 hit `_NeverDial("Info")` and `_NeverDial("Exchange")` (demonstrated in `LEAD_RED_DD06_R1_M3_master_key_call_removed.txt`).
  **Conclusion:** No test in this file can reach a venue if both gates are removed. `suite_can_dial_after_two_gates_removed: false`.

---

### 3. Trace of `run_probe` on `_BalancesInfo` + `_leaky_exchange`
*File:* [`subject/dd06_agent_withdraw_probe_HEAD_complete.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R1_20260917/subject/dd06_agent_withdraw_probe_HEAD_complete.py#L354-L611), [`subject/test_dd06_agent_withdraw_probe_HEAD_complete.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R1_20260917/subject/test_dd06_agent_withdraw_probe_HEAD_complete.py#L533-L592)

- **S0 Baseline Readings:**
  - Initial balances: `ACCOUNT: 984.987457`, `AGENT: 13.0`.
  - Lines 407–414 execute `account_before = _balances(info, account_address)` and `agent_before = _balances(info, agent_address)`.
  - Step `S0_agent_balances` is recorded with `{"accountValue": "0.0", "usdc_total": "13.0"}`.
- **S1 Control & S2 Execution:**
  - S1 control order placed and cancelled successfully.
  - `withdraw3` and `usdSend` are refused with `AUTHORIZATION`.
  - `spotSend` calls `exchange.spot_transfer`. `Leaky.spot_transfer` executes, mutates balance according to `move`, and returns `{"status": "ok", ...}` (`NOT_REFUSED`).
- **Post-Arm Re-reads & Attribution (`FUND_MOVING_ARMS`):**
  - Line 556 reads `account_after = _balances(info, account_address)`. Step `post_spotSend_account_balances` recorded with before/after.
  - Line 565 computes `master_moved = _moved(account_before, account_after)`.
  - Lines 568–577 read `agent_after = _balances(info, agent_address)`. Step `post_spotSend_agent_balances` recorded with before/after.
  - Line 577 computes `own_moved = _moved(agent_before, agent_after)`.
- **Results per Parametrization:**
  - `move == "agent"`: `master_moved = False`, `own_moved = True`.  
    Line 585 sets `record.result = "DD06_FINDING_OWN_FUNDS_MOVED"`.  
    Finding text: `"spotSend was NOT refused and only the AGENT wallet's own balance changed: the agent moved its own funds, the master's are unchanged (r3 shape; not the DD-06 breach)"`.
  - `move == "master"`: `master_moved = True`, `own_moved = False`.  
    Line 579 sets `record.result = "DD06_FINDING_MASTER_FUNDS_MOVED"`.  
    Finding text: `"spotSend was NOT refused and the ACCOUNT's balance changed: the agent key moved the master's funds (DD-06 falsified on testnet)"`.
  - `move == "none"`: `master_moved = False`, `own_moved = False`.  
    Line 553/592 retains `record.result = "DD06_FINDING_NOT_REFUSED"`.  
    Finding text: `"spotSend was NOT refused; balances unchanged or unreadable on both wallets (master_moved=False, own_moved=False) - read the venue response before drawing any DD-06 conclusion"`.
- **Branch Preference When BOTH Change:**
  Line 578 evaluates `if master_moved:` first; line 584 is `elif own_moved:`. If both balances change, the logic **strictly prefers `DD06_FINDING_MASTER_FUNDS_MOVED`**.
- **Can `_moved` return `True` on Read Failure?**
  No. Lines 344–348 filter keys such that `before.get(key) is not None and after.get(key) is not None`. If nothing is readable on either side, line 349 returns `None`. Line 351 evaluates `any(before[key] != after[key] for key in readable)` only across keys successfully read on both sides.
- **Is `agent_address` Passed from `main()`?**
  Yes. Line 737 passes `agent_address=wallet.address` into `run_probe`.

---

## (b) The Four REQUIRED Closures

1. **R-1 (Unfenced Guards Fenced): CLOSED**
   - `plan_text` pins `https://api.hyperliquid-testnet.xyz`, `DD06_PROBE_RUN_TOKEN`, and `HL_LIVE_ACK` (fenced in `test_plan_names_the_testnet_host_and_the_gates`, lines 511–517; verified by mutant M2 failure).
   - `refuse_master_key` in `main()` is tested with an identical key/address, reaching exit code 3 with SDK tripwires intact (lines 492–509; verified by mutant M3 failure).
   - `write_record` surviving 64-hex and 0x40-hex guards are exercised with poisoned step data (lines 519–531; verified by mutant M4 failure).
   - `refuse_without_run_token` has an independent unit test testing valid, empty, and mismatched tokens (lines 480–490; verified by mutant M5 failure).
   - `del api_key` (line 711) is retained as local hygiene but is **not** claimed as a security control in docstrings, code, or commit notes.

2. **R-2 (Offline-ness Root Cause): CLOSED**
   - Implemented via the two-gate barrier: `refuse_unless_testnet` + `refuse_without_run_token` in `main()`.
   - Structural `offline` fixture in test suite with `_NeverDial` tripwires on resolver and SDK constructors.

3. **R-3 (Refusal Marker Classification): CLOSED**
   - `AUTHORIZATION_MARKERS` (lines 188–200) no longer contains bare `"does not exist"`. Bare `"does not exist"` is moved to `VALIDATION_MARKERS` (line 214).
   - Venue's signer error `"User or API Wallet <addr> does not exist."` matches `"user or api wallet"` in `AUTHORIZATION_MARKERS` (line 190).
   - Two new test cases added to `test_refusal_text_classes` (lines 295–298): `"Sub-account 0xabc does not exist"` -> `VALIDATION` and `"destination does not exist"` -> `VALIDATION` (verified by mutant R3 failure).

4. **R-4 (Balance Attribution & Evidence Integrity): CLOSED**
   - S0 baseline records agent balances (`S0_agent_balances`).
   - Post-arm re-read of both accounts on any `FUND_MOVING_ARMS` non-refusal.
   - Separate attribution states: `DD06_FINDING_MASTER_FUNDS_MOVED` vs `DD06_FINDING_OWN_FUNDS_MOVED` vs `DD06_FINDING_NOT_REFUSED`.
   - Verified by mutant R4 failure.

---

## (c) Behaviour Preservation

- **Redaction & Write-Once Invariants:** `redact()`, `_HEX64`, `_HEX40`, and `write_record()` write-once directory checks and sha256 sidecars are unmodified.
- **Stop Rule:** Lines 552–600 halt immediately on any `NOT_REFUSED` arm (`STOP_ON_NOT_REFUSED = True`). Subsequent arms are recorded as `SKIPPED_AFTER_FINDING`.
- **Refusal Text Handling:** Venue strings like `"Must deposit before performing actions"` contain no authorization or validation markers and remain classified as `UNCLASSIFIED`.
- **Exit Codes:** `main()` yields 0 on `DD06_REFUSALS_OBSERVED` (and dry-run), 3 on `ProbeRefused`, and 2 otherwise. Preserved.

---

## (d) Record Honesty

- **Mutant Test Fences:** All 8 Lead mutant records (`LEAD_RED_DD06_R1_*.txt`) document exact single-fence failures:
  - M2 (plan testnet URL), M3 (master key call), M4 (hex64 guard), M5 (token gate in main), M8 (live-ack refusal), N2 (abort swallowed), R3 (does not exist in auth), R4 (moved always false).
  - Mutants M3 and M5 trip the SDK / resolver tripwires (`tripwire_hit=True`). The remaining 6 fail specific assertions (`tripwire_hit=False`).
- **Test Suite Results:**
  - `LEAD_PYTEST_GREEN_R1.txt`: 25 passed in 0.61s.
  - `LEAD_FULL_BRIDGE_SUITE_R1.txt`: 1623 passed, 1 skipped in 173.73s (exit=0).
  - `LEAD_GUARD_R1.txt`: Clean dry-run guard pass.
- All artifact claims match the packet files byte-for-byte.

---

## (e) Reviewer Findings

### [NIT-1] Duplicate Assertion in `test_refusal_text_classes`
- **File & Line:** [`subject/test_dd06_agent_withdraw_probe_HEAD_complete.py:300`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R1_20260917/subject/test_dd06_agent_withdraw_probe_HEAD_complete.py#L300)
- **Severity:** NIT
- **Description:** `assert probe.classify_refusal_text("User or API Wallet 0xabc does not exist.") == "AUTHORIZATION"` is asserted at line 282 and duplicated verbatim at lines 300–302 in the same test function. Harmless redundancy.

*(Note on first-read NITs N-3..N-9: None represent safety exposures or required changes; all remain out of scope for this repair commit.)*

---

## (f) Exact Read Coverage

All views were executed natively using `view_file` strictly within packet `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R1_20260917`, capped at <= 150 lines per view call:
1. `PACKET_SHA256SUMS.txt`: lines 1–19 (complete)
2. `subject/DIFF_STAT_1af85067_a46b2a9d.txt`: lines 1–4 (complete)
3. `subject/COMMIT_a46b2a9d.txt`: lines 1–54 (complete)
4. `subject/DIFF_1af85067_a46b2a9d.patch`: lines 1–150, 151–300, 301–450, 451–498 (complete)
5. `subject/dd06_agent_withdraw_probe_HEAD_complete.py`: lines 1–150, 151–300, 301–450, 451–600, 601–746 (complete)
6. `subject/test_dd06_agent_withdraw_probe_HEAD_complete.py`: lines 1–150, 151–300, 301–450, 451–608 (complete)
7. `sources/OPUS_T0_REPORT_attempt1_1af85067.md`: lines 10–36, 185–229 (required ranges complete)
8. `sources/INCIDENT_20260917_LANE7_DD06_UNINTENDED_TESTNET_RUN.md`: lines 1–22 (complete)
9. `sources/LEAD_FULL_BRIDGE_SUITE_R1.txt`: lines 1–32 (complete)
10. `sources/LEAD_GUARD_R1.txt`: lines 1–17 (complete)
11. `sources/LEAD_PYTEST_GREEN_R1.txt`: lines 1–5 (complete)
12. `sources/LEAD_RED_DD06_R1_M2_testnet_url_to_mainnet.txt`: lines 1–22 (complete)
13. `sources/LEAD_RED_DD06_R1_M3_master_key_call_removed.txt`: lines 1–51 (complete)
14. `sources/LEAD_RED_DD06_R1_M4_hex64_guard_removed.txt`: lines 1–29 (complete)
15. `sources/LEAD_RED_DD06_R1_M5_token_gate_removed_from_main.txt`: lines 1–41 (complete)
16. `sources/LEAD_RED_DD06_R1_M8_live_ack_refusal_removed.txt`: lines 1–21 (complete)
17. `sources/LEAD_RED_DD06_R1_N2_abort_swallowed.txt`: lines 1–24 (complete)
18. `sources/LEAD_RED_DD06_R1_R3_does_not_exist_back_in_authorization.txt`: lines 1–38 (complete)
19. `sources/LEAD_RED_DD06_R1_R4_moved_always_false.txt`: lines 1–80 (complete)

---

## (g) Not Verified
- Live runtime execution or dynamic network interaction (strictly unexecuted detection review).
- Venue state, live order books, or live balance confirmations on Hyperliquid testnet or mainnet.
- Files and directories external to the assigned packet path.

---

```json
{
  "part": "DD06_R1_GEMINI",
  "verdict": "PASS-WITH-NITS",
  "evidence_class": "SUPPLEMENTAL_UNEXECUTED",
  "r1": "CLOSED",
  "r2": "CLOSED",
  "r3": "CLOSED",
  "r4": "CLOSED",
  "suite_can_dial_after_two_gates_removed": false,
  "findings": [
    {
      "id": "NIT-1",
      "severity": "NIT",
      "file": "subject/test_dd06_agent_withdraw_probe_HEAD_complete.py",
      "line": 300,
      "description": "Verbatim duplicate assertion of probe.classify_refusal_text('User or API Wallet 0xabc does not exist.') == 'AUTHORIZATION' within test_refusal_text_classes (already asserted at line 282)."
    }
  ],
  "required_scope_unread": []
}
```

GEMINI_READ_ONLY_OK
