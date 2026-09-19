# Supplemental Read-Only Detection Review: WP-P0-29 DD-06 Testnet Probe (T0 Repair Round 3, Commit `acd79b52`)

**Reviewer Role:** `gemini-3.8-flash-high` (Independent Detection Reviewer, `SUPPLEMENTAL_UNEXECUTED`)  
**Repository Working Copy:** `C:\LAB\Tradingview_LAB_CLEAN`  
**Packet Under Review:** `_gemini_packets_20260913/DD06_R3_20260918`  
**Commit Inspected:** `acd79b52efbbf8847621cabe1797cc6fc0567f17` (`+94/-18`, 2 files)

---

## 1. Traces

### 1.1 Parametrized Cases in [`test_dd06_agent_withdraw_probe.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R3_20260918/subject/test_dd06_agent_withdraw_probe_HEAD_complete.py#L619-L681)

#### (a) `agent-pays-master-spot-unreadable`
- **S0 Readings:**
  - Account: `{"accountValue": "0.0", "usdc_total": "983.987457"}`
  - Agent: `{"accountValue": "0.0", "usdc_total": "14.0"}`
- **Post-Arm (`spotSend`, amount 1.0, threshold 0.5):**
  - Account: `info.usdc[ACCOUNT] = None` (transient 503), `account_value` remains `"0.0"`. `account_after = {"accountValue": "0.0", "usdc_total": None}`.
  - Agent: `info.usdc[AGENT] = "13.0"`. `agent_after = {"accountValue": "0.0", "usdc_total": "13.0"}`.
- **`_paid` Evaluation:**
  - **Account:** For `accountValue`, $\Delta = 0.0 - 0.0 = 0.0$ (not $\le -0.5$). For `usdc_total`, `second is None` triggers `unreadable += 1`. Loop ends; since `unreadable == 1` and no key decreased by threshold, `_paid(account_before, account_after, 1.0) -> None`.
  - **Agent:** For `accountValue`, $\Delta = 0.0$. For `usdc_total`, $\Delta = 13.0 - 14.0 = -1.0 \le -0.5$ (exceeds threshold 0.5). Returns `True` immediately.
- **`_attribute` Outcome:**
  - `master_paid = None`, `own_paid = True`, `agent_read = True`.
  - `master_text = "UNREADABLE"`, `own_text = "paid"`. Readings string: `[account UNREADABLE, agent wallet paid]`.
  - Enters `if own_paid and master_paid is None:` branch.
  - **Label:** `DD06_FINDING_OWN_FUNDS_MOVED_MASTER_UNREADABLE`.
  - **Finding Text:** `"spotSend was NOT refused and the AGENT wallet's own balance DECREASED; the ACCOUNT was NOT measured (a balance read failed), so nothing is concluded about the master's funds [account UNREADABLE, agent wallet paid] - re-read the account by hand before drawing any DD-06 conclusion"`.
  - **Exclusion & Honesty Check:** Neither `"did not pay"` (for the account) nor `"not the DD-06 breach"` appears anywhere in the finding.

#### (b) `master-pays-perp-unreadable`
- **Post-Arm:** `info.usdc[ACCOUNT] = "977.987457"` (decreased by 6.0), `info.account_value[ACCOUNT] = None`.
- **`_paid` Evaluation:**
  - **Account:** For `accountValue`, `second is None` increments `unreadable += 1`. For `usdc_total`, $\Delta = 977.987457 - 983.987457 = -6.0 \le -0.5$. A measured decrease is a fact even beside an unreadable key; returns `True` immediately.
  - **Agent:** No balance changed ($\Delta = 0.0$); returns `False`.
- **`_attribute` Outcome:** `master_paid = True` triggers the breach branch.
  - **Label:** `DD06_FINDING_MASTER_FUNDS_MOVED`.
  - **Finding Text:** `"spotSend was NOT refused and the ACCOUNT's balance DECREASED by at least half the arm amount: the agent key moved the master's funds (DD-06 falsified on testnet) [account paid, agent wallet did not pay]"`.

#### (c) `nothing-moves-master-spot-unreadable`
- **Post-Arm:** `info.usdc[ACCOUNT] = None`, `info.account_value[ACCOUNT] = "0.0"`. Agent balances untouched (`"14.0"`, `"0.0"`).
- **`_paid` Evaluation:**
  - **Account:** `accountValue` unchanged ($\Delta = 0.0$), `usdc_total` unreadable (`None`). Returns `None`.
  - **Agent:** Both keys readable and unchanged. Returns `False`.
- **`_attribute` Outcome:**
  - `master_paid = None`, `own_paid = False`, `agent_read = True`.
  - Neither `master_paid` nor `own_paid` is True. Fall-through to final branch.
  - `unmeasured = master_paid is None or (agent_read and own_paid is None)` evaluates to `True` (since `master_paid is None`).
  - **Label:** `DD06_FINDING_NOT_REFUSED`.
  - **Finding Text:** Appends `" - a wallet was NOT measured (UNREADABLE): re-read it by hand"` before concluding. Readings read `[account UNREADABLE, agent wallet did not pay]`.
  - `"account did not pay"` is absent.

---

### 1.2 The Reviewer's Probe ([`sources/reviewer_test_reviewer_partial3_on_2128352b.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R3_20260918/sources/reviewer_test_reviewer_partial3_on_2128352b.py)) on Commit `acd79b52`

The probe asserts the pre-repair behavior on `2128352b`. When executed against `acd79b52`:
1. `test_partially_unreadable_master_is_reported_as_did_not_pay`:
   - **First Failing Assertion:** Line 46: `assert record.result == "DD06_FINDING_OWN_FUNDS_MOVED"`.
   - **Why:** `record.result` is now correctly `DD06_FINDING_OWN_FUNDS_MOVED_MASTER_UNREADABLE`. (Subsequent assertions expecting `"account did not pay"` and `"not the DD-06 breach"` also fail).
2. `test_paid_unit_the_decoy_key_alone_produces_a_definite_False`:
   - **First Failing Assertion:** Line 59: `assert probe._paid(before, after, 1.0) is False`.
   - **Why:** `after` has `usdc_total: None`. Under the new `_paid`, any unreadable key without a qualifying decrease returns `None` (`AssertionError: assert None is False`).
3. `test_master_spot_unreadable_and_a_real_master_decrease_is_missed`:
   - **First Failing Assertion:** Line 84: `assert record.result == "DD06_FINDING_OWN_FUNDS_MOVED"`.
   - **Why:** With `info.usdc[ACCOUNT] = None`, `master_paid` is `None` rather than `False`. The result is `DD06_FINDING_OWN_FUNDS_MOVED_MASTER_UNREADABLE`, not `OWN_FUNDS_MOVED`.

All 3 tests fail on `acd79b52`, matching [`sources/LEAD_RED_DD06_R3_CONTROL_reviewer_partial_probe_now_fails.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R3_20260918/sources/LEAD_RED_DD06_R3_CONTROL_reviewer_partial_probe_now_fails.txt).

---

### 1.3 Adversarial Analysis

- **Case 1: Both keys readable, one decreased by a tick, the other by full amount.**
  - *Trace:* Key 1 ($\Delta = -0.01 > -threshold$) does not trigger return. Key 2 ($\Delta = -1.0 \le -threshold$) returns `True` immediately.
  - *Result:* Returns `True`. Consistent and sound: any readable decrease exceeding the threshold indicates fund movement.
- **Case 2: Agent wallet partially unreadable while master wallet paid.**
  - *Trace:* `master_paid = True`, `own_paid = None`. In `_attribute`, `if master_paid:` fires first.
  - *Result:* Returns `DD06_FINDING_MASTER_FUNDS_MOVED` with readings `[account paid, agent wallet UNREADABLE]`.
  - *DD-06 Significance:* Sound. Master funds leaving on an agent-signed action is the definition of the breach/falsification; the agent's balance readability cannot exonerate or alter the master breach.
- **Case 3: `after` missing a key that `before` has.**
  - *Trace:* `_paid` iterates `for key in before:`. If `key` is missing in `after`, `after.get(key)` returns `None`, which triggers `if first is None or second is None: unreadable += 1; continue`. If no other key decreased, it returns `None`.
  - *Result:* Safely treats missing keys as unreadable (`None`), never `False`. Note that `_balances` structurally guarantees fixed keys `{"accountValue", "usdc_total"}`.
- **Case 4: `own_paid is None` with `master_paid is False`.**
  - *Trace:* Neither `master_paid` nor `own_paid` is True. In `_attribute`, `unmeasured = master_paid is None or (agent_read and own_paid is None)` evaluates to `True`.
  - *Result:* Label `DD06_FINDING_NOT_REFUSED`; text includes `[account did not pay, agent wallet UNREADABLE]` and appends `" - a wallet was NOT measured (UNREADABLE): re-read it by hand"`.
  - *DD-06 Significance:* Sound. Because the agent was unmeasured, it does not draw conclusions about agent funds, does not emit `OWN_FUNDS_MOVED`, leaves DD-06 in `BLOCK`, and instructs hand re-reading.

---

### 1.4 Preservation and Honesty

1. **Gate Architecture:** Both the network gate (`refuse_unless_testnet`, rejecting `HL_LIVE_ACK`) and the token gate (`refuse_without_run_token`, requiring `DD06_PROBE_RUN_TOKEN == run_id`) remain strictly before any credential resolution or SDK initialization.
2. **Safety & Redaction:** Hex pattern regexes (`_HEX64`, `_HEX40`), tripwired fixtures, and write-once output directory semantics are untouched.
3. **Execution Semantics:** `STOP_ON_NOT_REFUSED = True` (remaining arms marked `SKIPPED_AFTER_FINDING`), `outcome == "ERROR"` on fund-moving arms (`DD06_INCONCLUSIVE_FUND_ARM_ERROR` and `SKIPPED_AFTER_ERROR`), and round-2 attribution rules for fully readable readings are preserved.
4. **Scope Integrity:** Exactly two files modified (`test_dd06_agent_withdraw_probe.py` and `dd06_agent_withdraw_probe.py`; `+94/-18`).
5. **Mutation & Test Record:**
   - Mutant R1a (readable-per-key restored): 4 failed ([`sources/LEAD_RED_DD06_R3_R1a_readable_per_key_restored.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R3_20260918/sources/LEAD_RED_DD06_R3_R1a_readable_per_key_restored.txt)).
   - Mutant R1b (master unreadable branch removed): 2 failed ([`sources/LEAD_RED_DD06_R3_R1b_master_unreadable_branch_removed.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R3_20260918/sources/LEAD_RED_DD06_R3_R1b_master_unreadable_branch_removed.txt)).
   - Mutant R1c (unparsable counted as readable): 1 failed ([`sources/LEAD_RED_DD06_R3_R1c_unparsable_counts_as_readable.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R3_20260918/sources/LEAD_RED_DD06_R3_R1c_unparsable_counts_as_readable.txt)).
   - Mutant R1d (unmeasured note removed): 1 failed ([`sources/LEAD_RED_DD06_R3_R1d_not_refused_unmeasured_note_removed.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R3_20260918/sources/LEAD_RED_DD06_R3_R1d_not_refused_unmeasured_note_removed.txt)).
   - Reviewer probe control: 3 failed ([`sources/LEAD_RED_DD06_R3_CONTROL_reviewer_partial_probe_now_fails.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R3_20260918/sources/LEAD_RED_DD06_R3_CONTROL_reviewer_partial_probe_now_fails.txt)).
   - Full suite: 31 passed in focused probe suite; 1629 passed, 1 skipped in Bridge suite; MTC Repo Guard: PASS.

---

### 1.5 Carried NITs

The carried design notes (N-3..N-10, N-13..N-16) from the third exact-Opus review remain non-blocking design observations. None represent a safety hazard, a false positive, or an incorrect attribution on testnet. None are REQUIRED.

---

## 2. Findings

- **No REQUIRED findings.** R-1 is completely resolved and closed.
- **No new NIT findings.** Implementation is minimal, honest, and robustly pinned by tests.

---

## 3. Exact Read Coverage

All views performed natively via `view_file` in ranges $\le 150$ lines:
1. [`PACKET_SHA256SUMS.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R3_20260918/PACKET_SHA256SUMS.txt): lines 1–19 (complete)
2. [`subject/DIFF_STAT_2128352b_acd79b52.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R3_20260918/subject/DIFF_STAT_2128352b_acd79b52.txt): lines 1–4 (complete)
3. [`subject/COMMIT_acd79b52.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R3_20260918/subject/COMMIT_acd79b52.txt): lines 1–47 (complete)
4. [`subject/DIFF_2128352b_acd79b52.patch`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R3_20260918/subject/DIFF_2128352b_acd79b52.patch): lines 1–150; lines 151–209 (complete)
5. [`sources/OPUS_T0_REPORT_attempt4_2128352b.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R3_20260918/sources/OPUS_T0_REPORT_attempt4_2128352b.md): lines 227–304 (R-1); lines 366–423 (NOT VERIFIED & verdict)
6. [`sources/reviewer_test_reviewer_partial3_on_2128352b.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R3_20260918/sources/reviewer_test_reviewer_partial3_on_2128352b.py): lines 1–86 (complete)
7. [`sources/LEAD_FULL_BRIDGE_SUITE_R3.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R3_20260918/sources/LEAD_FULL_BRIDGE_SUITE_R3.txt): lines 1–31 (complete)
8. [`sources/LEAD_GUARD_R3.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R3_20260918/sources/LEAD_GUARD_R3.txt): lines 1–17 (complete)
9. [`sources/LEAD_PYTEST_GREEN_R3.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R3_20260918/sources/LEAD_PYTEST_GREEN_R3.txt): lines 1–3 (complete)
10. [`sources/LEAD_RED_DD06_R3_BASELINE_scratch_unmutated.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R3_20260918/sources/LEAD_RED_DD06_R3_BASELINE_scratch_unmutated.txt): lines 1–4 (complete)
11. [`sources/LEAD_RED_DD06_R3_CONTROL_reviewer_partial_probe_now_fails.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R3_20260918/sources/LEAD_RED_DD06_R3_CONTROL_reviewer_partial_probe_now_fails.txt): lines 1–97 (complete)
12. [`sources/LEAD_RED_DD06_R3_R1a_readable_per_key_restored.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R3_20260918/sources/LEAD_RED_DD06_R3_R1a_readable_per_key_restored.txt): lines 1–150; lines 151–301 (complete)
13. [`sources/LEAD_RED_DD06_R3_R1b_master_unreadable_branch_removed.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R3_20260918/sources/LEAD_RED_DD06_R3_R1b_master_unreadable_branch_removed.txt): lines 1–150; lines 151–192 (complete)
14. [`sources/LEAD_RED_DD06_R3_R1c_unparsable_counts_as_readable.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R3_20260918/sources/LEAD_RED_DD06_R3_R1c_unparsable_counts_as_readable.txt): lines 1–39 (complete)
15. [`sources/LEAD_RED_DD06_R3_R1d_not_refused_unmeasured_note_removed.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R3_20260918/sources/LEAD_RED_DD06_R3_R1d_not_refused_unmeasured_note_removed.txt): lines 1–98 (complete)
16. [`sources/LEAD_REPRO_R3_R1_reviewer_partial_probe_on_unmodified_2128352b.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R3_20260918/sources/LEAD_REPRO_R3_R1_reviewer_partial_probe_on_unmodified_2128352b.txt): lines 1–8 (complete)
17. [`subject/dd06_agent_withdraw_probe_HEAD_complete.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R3_20260918/subject/dd06_agent_withdraw_probe_HEAD_complete.py): lines 1–150; lines 151–300; lines 301–450; lines 451–600; lines 601–750; lines 751–860 (complete)
18. [`subject/test_dd06_agent_withdraw_probe_HEAD_complete.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R3_20260918/subject/test_dd06_agent_withdraw_probe_HEAD_complete.py): lines 520–660; lines 661–750 (complete coverage of `_BalancesInfo` through `test_paid_is_directional_amount_aware_and_unreadable_honest` to EOF)

---

## 4. NOT VERIFIED

- **No live or testnet probe execution:** As a read-only unexecuted reviewer (`SUPPLEMENTAL_UNEXECUTED`), I executed no tests, contacted no network endpoints, and read no credentials.
- **Full test suite execution:** Full bridge suite count (`1629 passed, 1 skipped`) and focused test count (`31 passed`) are verified from the Lead's recorded test logs in the packet, not independently re-executed.
- **Git working tree mutation:** No Git operations or filesystem writes were executed.

---

## 5. Review Verdict

```json
{
  "part": "DD06_R3_GEMINI",
  "verdict": "PASS",
  "evidence_class": "SUPPLEMENTAL_UNEXECUTED",
  "r1": "CLOSED",
  "partial_unreadable_master_can_read_as_did_not_pay": false,
  "exclusion_possible_without_complete_master_reading": false,
  "findings": [],
  "required_scope_unread": []
}
```

GEMINI_READ_ONLY_OK
