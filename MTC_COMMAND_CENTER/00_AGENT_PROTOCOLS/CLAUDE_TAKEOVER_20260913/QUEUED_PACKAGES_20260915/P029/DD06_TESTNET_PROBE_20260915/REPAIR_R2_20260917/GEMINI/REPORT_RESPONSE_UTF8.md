### Review Assessment: WP-P0-29 DD-06 Testnet Probe T0 Repair Round 2 (`2128352b`)

This is an independent read-only detection review (`SUPPLEMENTAL_UNEXECUTED`) of commit `2128352b` (+262/−82 across two files) on branch `feature/p029-dd06-testnet-probe-20260915`.

---

### (a) Execution Traces and Analyses

#### 1. Trace: `test_not_refused_fund_arm_names_whose_funds_left[r3-replay]`
- **S0 Initial Readings**:
  - Master (`ACCOUNT`): `accountValue="0.0"`, `usdc_total="983.987457"`.
  - Agent (`AGENT`): `accountValue="0.0"`, `usdc_total="14.0"`.
- **Arm Sequence**:
  - `withdraw3` (6.0 USDC) is REFUSED (`AUTHORIZATION`).
  - `usdSend` (1.0 USDC) is REFUSED (`AUTHORIZATION`).
  - `spotSend` (1.0 USDC) invokes `_leaky_exchange` with `_r3_replay`. The venue responds `status: "ok"`, classified as `NOT_REFUSED`.
- **Post-Arm Re-reads (`_reread_both_wallets`)**:
  - Master (`ACCOUNT`): `accountValue="0.0"`, `usdc_total="984.987457"`.
  - Agent (`AGENT`): `accountValue="0.0"`, `usdc_total="13.0"`.
- **Evaluation in `_paid` (`amount=1.0`, `threshold=Decimal('0.5')`)**:
  - Master:
    - `accountValue`: $\Delta = 0.0 - 0.0 = 0.0$ ($> -0.5$).
    - `usdc_total`: $\Delta = 984.987457 - 983.987457 = +1.0$ ($> -0.5$).
    - Readable balances checked $= 2$, neither decreased $\le -0.5 \implies$ `master_paid = False`.
  - Agent:
    - `accountValue`: $\Delta = 0.0$.
    - `usdc_total`: $\Delta = 13.0 - 14.0 = -1.0 \le -0.5 \implies$ `own_paid = True`.
- **Attribution & Finding**:
  - In `_attribute("spotSend", master_paid=False, own_paid=True, agent_read=True)`:
    - `master_text = "did not pay"`, `own_text = "paid"`.
    - `readings = "account did not pay, agent wallet paid"`.
    - Result label: `DD06_FINDING_OWN_FUNDS_MOVED`.
    - Finding text: `"spotSend was NOT refused and the AGENT wallet's own balance DECREASED while the account's readable balances did not: the agent moved its own funds (r3 shape; not the DD-06 breach) [account did not pay, agent wallet paid]"`.
  - Later arm `approveAgent` marked `SKIPPED_AFTER_FINDING`. Probe stops immediately.
  - **Confirmation**: `"falsified"` cannot appear.

#### Additional Parametrized Cases:
- **`[mark-to-market-tick]`**:
  - Master `accountValue` drifts $0.0 \to 0.01$ ($\Delta = +0.01$). `usdc_total` unchanged.
  - `_paid` master: $\Delta = +0.01 > -0.5 \implies False$.
  - `_paid` agent: $\Delta = 0.0 > -0.5 \implies False$.
  - Result: `DD06_FINDING_NOT_REFUSED`.
  - Finding: `"no readable balance decreased by half the arm amount on either wallet [account did not pay, agent wallet did not pay]..."`. `"falsified"` is absent.
- **`[agent-pays-master-unreadable]`**:
  - Master reads fail with 503 (`accountValue=None`, `usdc_total=None`). Agent pays 1 USDC (`14.0 -> 13.0`).
  - `_paid` master: readable balances $= 0 \implies None$.
  - `_paid` agent: $\Delta = -1.0 \le -0.5 \implies True$.
  - Result: `DD06_FINDING_OWN_FUNDS_MOVED`.
  - Finding: `"...[account UNREADABLE, agent wallet paid]"`. Notice `"UNREADABLE"` is rendered; `"unchanged"` is strictly absent.
- **`[master-pays]`**:
  - Master `usdc_total` drops $983.987457 \to 982.987457$ ($\Delta = -1.0 \le -0.5$). Agent unchanged.
  - `_paid` master $= True$, `_paid` agent $= False$.
  - Result: `DD06_FINDING_MASTER_FUNDS_MOVED`.
  - Finding: `"spotSend was NOT refused and the ACCOUNT's balance DECREASED by at least half the arm amount: the agent key moved the master's funds (DD-06 falsified on testnet) [account paid, agent wallet did not pay]"`.

---

#### 2. Trace: `test_transport_error_is_inconclusive_not_a_refusal`
- **Arm Execution**:
  - `withdraw3` raises `_ServerError(503, "no capacity")`.
  - `classify_exception` classifies `_ServerError` as `"ERROR"`.
- **Handling in `run_probe` (`outcome == "ERROR" and name in FUND_MOVING_ARMS`)**:
  - `_reread_both_wallets` triggers:
    - Master balances recorded in step `post_withdraw3_account_balances`.
    - Master balances unchanged $\implies \Delta = 0.0 > -3.0$ (`amount=6.0`, `threshold=3.0`) $\implies master\_paid = False$.
    - Agent address not supplied $\implies agent\_read = False, own\_paid = None$.
  - `_attribute("withdraw3", False, None, False)` produces label `DD06_FINDING_NOT_REFUSED`.
  - `record.result` set to `DD06_INCONCLUSIVE_FUND_ARM_ERROR` (retained because label is `DD06_FINDING_NOT_REFUSED`).
  - `record.finding` explicitly states `"withdraw3 ended in ERROR (transport or server) - the signed request may have executed; balances re-read and the sequence stopped: withdraw3 was NOT refused; no readable balance decreased..."`.
  - Arms `usdSend`, `spotSend`, `approveAgent` marked `SKIPPED_AFTER_ERROR`.
  - Sequence terminates and returns `record`.
- **Behavior on `approveAgent` ERROR**:
  - `approveAgent` is **not** in `FUND_MOVING_ARMS`.
  - If `approveAgent` errors, it records `outcome: "ERROR"`, but does **not** enter the fund-moving error branch. It does not stop earlier arms or re-read balances. The loop finishes, `refused == len(arms)` is false, and `record.result` becomes `DD06_INCONCLUSIVE` with `finding = None`. This is correct because `approveAgent` does not move funds.

---

#### 3. Adversarial Analysis of `_paid`
1. **Decrease Exactly at Threshold**:
   - `delta <= -threshold`: For `amount=1.0`, `threshold=0.5`. If $\Delta = -0.5$, $-0.5 \le -0.5$ evaluates to `True`. This matches the requirement: "decreased by at least half the amount".
2. **Scientific Notation Strings**:
   - Python `Decimal(str("1e-3"))` parses valid exponential notation into `Decimal('0.001')`. `delta` calculation succeeds without exception. Non-numeric strings raise `InvalidOperation` or `ValueError`, both caught by `except (InvalidOperation, ValueError): continue`, correctly skipping invalid readings.
3. **Perp Drift vs Spot USDC on Dual-Balance Wallets**:
   - If spot USDC is unreadable or 0, but an open perp position experiences marked volatility such that perp `accountValue` decreases by $\ge 0.5$ during the probe call, `_paid` will return `True`. While theoretical on accounts with active leveraged perp positions, testnet probe preconditions prescribe flat accounts. The $0.5$ threshold effectively filters normal mark-to-market noise (such as $0.01$ ticks).

---

#### 4. Preservation and Honesty Verification
- **Scope**: Exactly 2 files modified: [test_dd06_agent_withdraw_probe.py](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R2_20260917/subject/test_dd06_agent_withdraw_probe_HEAD_complete.py) (+149/−24) and [dd06_agent_withdraw_probe.py](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R2_20260917/subject/dd06_agent_withdraw_probe_HEAD_complete.py) (+195/−58). Net: +262/−82.
- **Safety Gates & Tripwires**:
  - Gate 1 (`refuse_unless_testnet` checking testnet and `HL_LIVE_ACK`) and Gate 2 (`refuse_without_run_token` checking `DD06_PROBE_RUN_TOKEN == run_id`) remain at `main()` lines 788-789 before credentials or SDK objects are constructed.
  - All `main()` tests, now explicitly including `test_dry_run_needs_no_credentials_and_no_network`, execute under the `offline` fixture with `_NeverDial` tripwires.
- **Lead Records Audit**:
  - 11 RED mutants checked: M2, M3, M4, M5, M8, N2, R1a, R1b, R1c, R2, R3.
  - `tripwire_hit=True` occurs **only** for M3 and M5 (the two removed-gate mutants), proving that without the gates, the offline tripwire catches execution.
  - `LEAD_PYTEST_GREEN_R2.txt`: 28 passed.
  - `LEAD_FULL_BRIDGE_SUITE_R2.txt`: 1626 passed, 1 skipped.
  - `LEAD_GUARD_R2.txt`: RESULT: PASS.
- **Venue r3 Replay Fidelity**:
  - Initial: master 983.987457, agent 14.0.
  - After: master 984.987457, agent 13.0.
  - The test fixture values exactly match testnet r3 ledger readings.

---

#### 5. Disposition of Notes N-3..N-7, N-9, N-10
- **N-3** (control order `oid` match on `filled`): Control order placed at 90% mid; will not fill. Minor handling NIT.
- **N-4** (`_HEX40` prefix requirement): Public addresses; redaction hygiene NIT.
- **N-5** (worst-case notional float product): Margin above $10 venue floor. Mathematical NIT.
- **N-6** (token gate host binding): Addressed by run token gate requirement. NIT.
- **N-7** (`--include-usd-class-transfer` test coverage): Optional flag defaulted to False. Scope NIT.
- **N-9** (arm sequence order): Spec §3 owner-approved order. Reviewer cannot unilaterally rewrite. NIT.
- **N-10** (5 sig-fig assertion): Pertains to sampled control prices. Test invariant NIT.
- **Conclusion**: None are REQUIRED; all remain classified as design notes/NITs out of scope for round 2 repair.

---

### (b) Findings

- None. No REQUIRED or NIT defects found in commit `2128352b`.

---

### (c) Exact Read Coverage

All reads performed using native `view_file` strictly within packet `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R2_20260917/` in slices $\le 150$ lines:
1. `PACKET_SHA256SUMS.txt`: lines 1-22 (complete).
2. `subject/DIFF_STAT_a46b2a9d_2128352b.txt`: lines 1-4 (complete).
3. `subject/COMMIT_2128352b.txt`: lines 1-48 (complete).
4. `subject/DIFF_a46b2a9d_2128352b.patch`: lines 1-150, 151-300, 301-450, 451-464 (complete).
5. `subject/dd06_agent_withdraw_probe_HEAD_complete.py`: lines 1-150, 151-300, 301-450, 451-600, 601-750, 751-833 (complete).
6. `subject/test_dd06_agent_withdraw_probe_HEAD_complete.py`: lines 1-150, 151-300, 301-450, 451-600, 601-701 (complete).
7. `sources/OPUS_T0_REPORT_attempt2_a46b2a9d.md`: lines 200-262, 352-414 (complete).
8. `sources/INCIDENT_20260917_LANE7_DD06_UNINTENDED_TESTNET_RUN.md`: lines 1-22 (complete).
9. Lead txt files:
   - `sources/LEAD_FULL_BRIDGE_SUITE_R2.txt`: lines 1-32 (complete).
   - `sources/LEAD_GUARD_R2.txt`: lines 1-17 (complete).
   - `sources/LEAD_PYTEST_GREEN_R2.txt`: lines 1-5 (complete).
   - `sources/LEAD_RED_DD06_R2_M2_testnet_url_to_mainnet.txt`: lines 1-22 (complete).
   - `sources/LEAD_RED_DD06_R2_M3_master_key_call_removed.txt`: lines 1-51 (complete).
   - `sources/LEAD_RED_DD06_R2_M4_hex64_guard_removed.txt`: lines 1-29 (complete).
   - `sources/LEAD_RED_DD06_R2_M5_token_gate_removed_from_main.txt`: lines 1-41 (complete).
   - `sources/LEAD_RED_DD06_R2_M8_live_ack_refusal_removed.txt`: lines 1-21 (complete).
   - `sources/LEAD_RED_DD06_R2_N2_abort_swallowed.txt`: lines 1-24 (complete).
   - `sources/LEAD_RED_DD06_R2_R1a_paid_means_changed_not_decreased.txt`: lines 1-150, 151-164 (complete).
   - `sources/LEAD_RED_DD06_R2_R1b_unreadable_reads_as_did_not_pay.txt`: lines 1-79 (complete).
   - `sources/LEAD_RED_DD06_R2_R1c_threshold_ignored.txt`: lines 1-150, 151-283 (complete).
   - `sources/LEAD_RED_DD06_R2_R2_error_branch_removed.txt`: lines 1-35 (complete).
   - `sources/LEAD_RED_DD06_R2_R3_does_not_exist_back_in_authorization.txt`: lines 1-38 (complete).

---

### (d) Nonempty NOT VERIFIED

1. Live execution of pytest or python commands was not performed (review is strictly read-only and unexecuted).
2. Live Hyperliquid testnet venue interaction and actual network socket transport were not performed.
3. Files outside `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R2_20260917` were not opened or inspected.

---

### (e) Fenced Verdict JSON

```json
{
  "part": "DD06_R2_GEMINI",
  "verdict": "PASS",
  "evidence_class": "SUPPLEMENTAL_UNEXECUTED",
  "r1": "CLOSED",
  "r2": "CLOSED",
  "master_increase_can_yield_breach_label": false,
  "findings": [],
  "required_scope_unread": []
}
```

GEMINI_READ_ONLY_OK
