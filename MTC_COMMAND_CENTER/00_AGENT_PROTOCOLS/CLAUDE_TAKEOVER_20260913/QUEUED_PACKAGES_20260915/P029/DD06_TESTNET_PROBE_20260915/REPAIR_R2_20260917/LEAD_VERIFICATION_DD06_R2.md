# LEAD_VERIFICATION — DD-06 testnet probe, T0 repair round 2 (`2128352b`) after the second exact-Opus read of `a46b2a9d` returned REQUEST_CHANGES — 2026-09-17 21:3x-21:4x UTC+3

**Trigger:** lane 7 attempt 2 (21:15-21:32 UTC+3, launcher exit 0, 100 turns, 453-line report `OPUS_QUEUE_20260916/DD06/ATTEMPT2_REQUEST_CHANGES_a46b2a9d/OPUS_T0_REPORT.md`; the binding safety rule held — no incident, its mutants ran on scratch copies under the tripwires) → **REQUEST_CHANGES**, two REQUIRED, twelve NITs. The reviewer confirmed round 1's gates and offline suite (§1-§2, §7a-§7d) and then replayed the venue's own r3 readings through the round-1 attribution.
**R-1:** `_moved` answered "changed?", not "did funds leave?", and `master_moved` was consulted first — so the r3 shape (agent 14.0 → 13.0 paid; master 983.987457 → 984.987457 RECEIVED) produced `DD06_FINDING_MASTER_FUNDS_MOVED` and "DD-06 falsified on testnet" — the maximum-severity sentence for an event in which the agent spent its own dollar. Sub-cases: an unreadable master (`_moved → None`, falsy) sent the run to the OWN branch which printed "the master's are unchanged" (unmeasured); a 0.01 mark-to-market tick on `accountValue` satisfied the MASTER branch. The Lead's round-1 fixtures changed one wallet at a time and never modelled a receipt — the r3 lesson was written into the docstring and not into the arithmetic.
**R-2:** a fund-moving arm ending in `ERROR` (timeout / 5xx — the signed request may have executed) was neither re-measured nor stopped; the run proceeded to the next fund-moving arm with a stale pre-arm balance.
**Role:** Lead = disclosed builder; T0 cap 3 rounds — round 2 (a third REQUEST_CHANGES ends the Lead's repair authority on this candidate).

## Repair (`2128352b`, +262/−82, two files)
- `ARM_AMOUNT_USDC` per fund-moving arm (withdraw3 6, usdSend/spotSend/usdClassTransfer 1, subAccountTransfer 1).
- `_paid(before, after, amount)`: True only when a readable balance (spot USDC total or perp accountValue, compared as `Decimal(str(x))`) DECREASED by at least half the amount; False when every readable balance stayed inside that band (an increase or a tick is not a payment); None when nothing was readable; malformed strings skipped (`InvalidOperation`).
- `_attribute(name, master_paid, own_paid, agent_read)`: `DD06_FINDING_MASTER_FUNDS_MOVED` only on a measured master decrease (the breach; the sentence names the decrease), `DD06_FINDING_OWN_FUNDS_MOVED` on the agent's decrease with no master decrease (r3 shape), else `DD06_FINDING_NOT_REFUSED` with the readings; each side rendered `paid` / `did not pay` / `UNREADABLE` / `NOT READ (no agent address supplied)` — never "unchanged".
- `_reread_both_wallets(...)` shared by the `NOT_REFUSED` branch and the new `ERROR` branch: on `ERROR` for a name in `FUND_MOVING_ARMS` → re-read both, `DD06_INCONCLUSIVE_FUND_ARM_ERROR` (or the measured label), finding "the signed request may have executed … sequence stopped", later arms `SKIPPED_AFTER_ERROR`, return. An `ERROR` on `approveAgent` (not fund-moving) still proceeds as before.
- Docstring rewritten for the attribution rule; N-11 (the dry-run test under `offline`); N-12 (the lane's agent brief pin) and N-8 (the brief's "ran once") fixed in the lane files.
- Tests: `_BalancesInfo` with per-address balances and unreadable (`None`) sides; parametrized `test_not_refused_fund_arm_names_whose_funds_left` — `r3-replay` (must read OWN and never say "falsified"), `master-pays`, `mark-to-market-tick`, `nothing-moves`, `agent-pays-master-unreadable` ("account UNREADABLE", never "unchanged"); `test_paid_is_directional_amount_aware_and_unreadable_honest`; the transport-error test asserts the stop + re-read.
Ruff: 7 findings (all pre-existing; one fewer than HEAD after formatting); both files ruff-formatted.

## Evidence
| Arm | Result | File |
|---|---|---|
| RED R1a — `_paid` back to "changed" (`delta != 0`) | **3 failed** (r3-replay, mark-to-market-tick, the `_paid` unit) | `LEAD_RED_DD06_R2_R1a_paid_means_changed_not_decreased.txt` |
| RED R1b — `None` rendered as "did not pay" | **1 failed** (agent-pays-master-unreadable) | `LEAD_RED_DD06_R2_R1b_unreadable_reads_as_did_not_pay.txt` |
| RED R1c — threshold ignored (any decrease counts) | **6 failed** (the amount-aware cases) | `LEAD_RED_DD06_R2_R1c_threshold_ignored.txt` |
| RED R2 — the ERROR branch removed | **1 failed** (`test_transport_error_is_inconclusive_not_a_refusal`) | `LEAD_RED_DD06_R2_R2_error_branch_removed.txt` |
| RED — the eight round-1 mutants (M2/M3/M4/M5/M8/R3/N2 + the classification) re-run on the round-2 bytes | each fails exactly its fence; M3/M5 **tripwire hit** (no network) | `LEAD_RED_DD06_R2_M*.txt`, `…_R3_…`, `…_N2_…` |
| GREEN — the fixture suite, `HL_*` removed, ASCII basetemp | **28 passed** (25 → 28) | `LEAD_PYTEST_GREEN_R2.txt` |
| Full Bridge suite (same env hygiene) | **1626 passed, 1 skipped, 0 failed** | `LEAD_FULL_BRIDGE_SUITE_R2.txt` |
| Guard | `RESULT: PASS`; staged exactly the two files | `LEAD_GUARD_R2.txt` |
| Gemini delta (`DD06_R2_GEMINI`, packet `DD06_R2_20260917`, 21 files) | COUNTED **PASS**, R-1/R-2 CLOSED, `master_increase_can_yield_breach_label: false`, 0 findings; 37 reads / 0 outside / 0 mismatches; 186 s | `GEMINI/` (+ `LEAD_ADJUDICATION.md` there) |
No network call was made by any Lead arm; every mutant ran as a file swap with the tripwires in place.

## Carried
N-3 (`_resting_oid` must require `resting`), N-4 (`_HEX40` bare 40-hex), N-5 (min-notional margin), N-6 (host binding — narrowed by the token gate), N-7 (`usd_class_transfer` in the protocol + a test; the `# type: ignore` placement), N-9 (arm order → owner `DD06-ORDER A|B`), N-10 (`len(digits) <= 5` is not an invariant — the venue's integer exemption; sweep-based test). The open venue question stays open: withdraw3 from an agent with a FUNDED perp balance has never been exercised.

## Roster
Lane 7 re-pinned to `2128352b` (launcher, brief Subject + addendum 3, agent brief, queue row, log); attempt 2 archived. Third exact-Opus read on the next Pro window (round 2 of the cap 3 — the last the Lead may repair); Sol (Sat) under the safety rule. The Lead never accepts its own code.

Recorded by Claude Opus 5 Lead (session 6, `4a8233`).
