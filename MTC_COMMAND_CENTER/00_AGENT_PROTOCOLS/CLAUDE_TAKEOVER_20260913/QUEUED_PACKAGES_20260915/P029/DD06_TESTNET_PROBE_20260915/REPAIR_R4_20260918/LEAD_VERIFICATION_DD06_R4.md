# LEAD_VERIFICATION - DD-06 testnet probe, round 4 (`a46da0aa`) - the named round the owner authorized (`OD-20260918-DD06-R4-A-1`) + arm order B (`OD-20260918-DD06-ORDER-B-1`), owner one line `N-16 B  D6-START B  DD06-ORDER B  P26-N2 doc  O-1 wait  DD06-R4 A` (2026-09-18 10:4x UTC+3)

**Trigger:** the fourth exact-Opus read of `acd79b52` (attempt 5, 08:25-08:44 UTC+3; `OPUS_QUEUE_20260916/DD06/ATTEMPT5_REQUEST_CHANGES_acd79b52/`; no incident) CONFIRMED the round-3 repair and returned REQUEST_CHANGES on one pre-existing REQUIRED, R-1, reproduced by the Lead offline (`ADJUDICATION_R4_20260918/`): `classify_response` returns `INCONCLUSIVE` for a response that is neither a refusal nor an acceptance envelope - the installed SDK (0.24.0) returns `{"error": "Could not parse JSON: ..."}` for any 2xx non-JSON body without raising - and the arm loop handled REFUSED / NOT_REFUSED / ERROR only, so an INCONCLUSIVE fund-moving arm was neither re-read nor stopped, the later signed fund-moving requests were sent, and the run ended `DD06_INCONCLUSIVE` with `finding None`. Round 2's R-2 had closed the exception channel only. Mine, since slice 3.
**Role:** Lead = disclosed builder. Scope: exactly the two files.

## Change (`a46da0aa`, +92/-29; tool blob `5747868e`, tests blob `5a0b8146`)
- Undetermined branch: `if outcome in ("ERROR", "INCONCLUSIVE") and name in FUND_MOVING_ARMS:` -> `_reread_both_wallets`; result `DD06_INCONCLUSIVE_FUND_ARM_ERROR` (ERROR) or the new `DD06_INCONCLUSIVE_FUND_ARM_UNCLASSIFIED` (INCONCLUSIVE), replaced by the measured attribution label when `_attribute` sees a decrease; finding `"{name} ended in ERROR (transport or server)"` / `"{name} returned a response the probe could not classify (neither a refusal nor an acceptance envelope)"` + "the signed request may have executed; balances re-read and the sequence stopped: {text}"; later arms `SKIPPED_AFTER_ERROR` / `SKIPPED_AFTER_UNCLASSIFIED`; return. `classify_response` unchanged. An INCONCLUSIVE on `approveAgent` (not fund-moving) still reaches the end-of-run `DD06_INCONCLUSIVE` handling as before.
- Arm order B: `arms` built as usdSend, spotSend, [subAccountTransfer], [usdClassTransfer], withdraw3, approveAgent; `FUND_MOVING_ARMS` reordered to the execution order (membership identical); docstring S2 list and the plan text (`S2 arms ..., in this order:` + `withdraw3 ... (LAST fund-moving arm)`) agree; the plan text's stop rule now reads "a fund-moving arm that is NOT refused, ends in ERROR, or returns a response the probe cannot classify stops the sequence, re-reads BOTH wallets and records a FINDING".
- Tests: new `test_unclassifiable_response_on_fund_arm_is_measured_and_stops`; `test_transport_error_is_inconclusive_not_a_refusal` now errors on usdSend and asserts spotSend/withdraw3/approveAgent `SKIPPED_AFTER_ERROR` and withdraw3 never called; the all-refused test pins the order-B call sequence; the not-refused stop test asserts withdraw3 skipped and never called. Ruff 7 (pre-existing); both files ruff-formatted; CRLF preserved.

## Evidence (`REPAIR_R4_20260918/`; mutants on the scratch copy `C:/tmp/LEAD_DD06_SCRATCH_R4_RED/`, fixture suite only, `HL_*`/`DD06_PROBE_RUN_TOKEN` removed, basetemps `C:/bt_s4/dd06r4*`; no network, `main()` never run)
| Arm | Result | File |
|---|---|---|
| CONTROL - the fourth reader's own probe `test_r4_reviewer.py::test_R1_inconclusive_fund_arm_neither_stops_nor_measures` (asserts the OLD fall-through; passed on `acd79b52`) on the patched code | **1 failed** | `LEAD_RED_DD06_R4_CONTROL_reviewer_r4_R1_probe_now_fails.txt` |
| R1a - INCONCLUSIVE dropped from the condition (fall-through restored) | **1 failed** (the unclassifiable test) | `LEAD_RED_DD06_R4_R1a_inconclusive_falls_through_again.txt` |
| R1b - UNCLASSIFIED labelled as ERROR | **1 failed** | `LEAD_RED_DD06_R4_R1b_unclassified_labelled_as_error.txt` |
| R1c - the stop removed after the re-read (`continue` instead of `return`) | **2 failed** (transport-error + unclassifiable) | `LEAD_RED_DD06_R4_R1c_no_stop_after_reread.txt` |
| ORDER - withdraw3 moved back to first | **4 failed** (all-refused sequence, not-refused stop, transport-error, unclassifiable) | `LEAD_RED_DD06_R4_ORDER_withdraw3_first_again.txt` |
| Baseline scratch, unmutated | 32 passed | `LEAD_RED_DD06_R4_BASELINE_scratch_unmutated.txt` |
| GREEN - the fixture suite in the worktree | **32 passed** (31 -> 32) | `LEAD_PYTEST_GREEN_R4.txt` |
| Full Bridge suite | **1630 passed, 1 skipped, 0 failed** | `LEAD_FULL_BRIDGE_SUITE_R4.txt` |
| Guard | `RESULT: PASS`; staged exactly the two files | `LEAD_GUARD_R4.txt` |
| Gemini delta `DD06_R4_GEMINI` (packet `DD06_R4_20260918`, 18 files; runner `run_dd06_r4_g38.ps1`) | see `GEMINI/` and the queue log | `GEMINI/` |

## Carried (unchanged this round)
N-3, N-4, N-5, N-6, N-7, N-8, N-10, N-13, N-14, N-16, N-17 (`del api_key` unpinned), N-18, N-20; N-9 closed by order B; N-15's second half disposed of by the channel-naming finding text (first half - the embedded `_attribute` sentence - still carried). The open venue question stays open; the probe runs only on a separate owner word.

## Roster
Lane 7 re-pinned to `a46da0aa` (launcher HEAD pin, agent brief, REVIEW_BRIEF HEAD + addendum 5, queue row); attempt 5 archived. Fifth exact-Opus read right after the Gemini delta; Sol (Sat) on these bytes under the safety rule. A REQUEST_CHANGES goes back to the owner. The Lead never accepts its own code.

Recorded by Claude Opus 5 Lead (session 6, `4a8233`), 10:5x UTC+3 (QUEUE_LOG stamps authoritative).
