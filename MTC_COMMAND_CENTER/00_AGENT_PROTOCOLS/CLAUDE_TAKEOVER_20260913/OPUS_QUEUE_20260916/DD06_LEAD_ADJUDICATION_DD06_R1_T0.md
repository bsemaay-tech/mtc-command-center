# LEAD_ADJUDICATION — lane 7, attempt 2: second exact `claude-opus-5` xhigh T0 read of the DD-06 probe at `a46b2a9d` (T0 repair round 1) — 2026-09-17 21:4x UTC+3

**Lane:** launched by hand 21:15 UTC+3 under the binding safety rule; 21:15-21:32 (18:15:44-18:32:23Z), launcher exit 0, 100 turns, no 429, **no incident** (mutants on scratch copies; the reviewer records which line stopped each mutant and that no resolver/SDK was reached); report `ATTEMPT2_REQUEST_CHANGES_a46b2a9d/OPUS_T0_REPORT.md`, 453 lines.
**Verdict as returned:** `VERDICT: REQUEST_CHANGES` — **2 REQUIRED**: R-1 the round-1 attribution inverts the one real outcome the venue has produced (r3: the agent paid, the master received → the tool would print "DD-06 falsified"); sub-cases unreadable-master → "unchanged", mark-to-market tick → movement; R-2 a fund-moving arm ending in ERROR is neither measured nor stopped. Round 1's gates and offline suite CONFIRMED (§1-§2, §7a-§7d: the removed-gate mutants stop at the token gate / the tripwires). NITs N-3..N-12.

## Lead reproduction and repair
- The r3 replay is exactly the Lead's own evidence (`LEAD_READING_r3_20260916.md`, `LEAD_PUBLIC_READS_after_r3.txt`): the round-1 arithmetic could not tell a receipt from a payment — a defect of the Lead's fixtures, which never modelled the master receiving. Reproduced by the Lead's new parametrized test on the round-1 bytes (RED arm R1a: reverting `_paid` to "changed" fails the r3-replay case).
- Repaired as the disclosed builder → **`2128352b`** (`DD06_TESTNET_PROBE_20260915/REPAIR_R2_20260917/LEAD_VERIFICATION_DD06_R2.md`): directional, amount-aware `_paid`; `_attribute` with UNREADABLE rendering; the ERROR branch measured and stopped; N-11/N-12/N-8. Eleven mutants RED; GREEN 28; full Bridge 1626; Gemini `DD06_R2_GEMINI` PASS (`master_increase_can_yield_breach_label: false`).

## NITs — disposition
| # | Finding | Disposition |
|---|---|---|
| N-3/N-4/N-5/N-7 | re-raised (resting key; bare 40-hex; min-notional margin; `usd_class_transfer` protocol + test) | carried to the next slice |
| N-6 | host binding (narrowed by the token gate) | carried; owner-worded runs set the token where they run |
| N-8 | brief said "ran once" | **fixed** (brief Subject) |
| N-9 | arm order | owner `DD06-ORDER A|B` |
| N-10 | `len(digits) <= 5` not an invariant of `control_order_size` (integer exemption) | carried (sweep-based test) |
| N-11 | dry-run test lacked `offline` | **fixed in `2128352b`** |
| N-12 | the agent brief pinned `1af85067` | **fixed** (`opus/BRIEF.md`) |

## Standing
Lane 7 re-pinned to `2128352b`; attempt 2 archived; the third exact-Opus read (round 2 of the cap 3 — the last the Lead may repair) on the next Pro window; Sol (Sat) under the safety rule. The Lead accepts nothing.

Recorded by Claude Opus 5 Lead (session 6, `4a8233`).
