# LEAD_ADJUDICATION_R5_OPUS — exact claude-opus-5 xhigh T0 round 5 of P020 preselection V1.5 — 2026-09-14 08:15Z

Lane P20O5P on Claude Pro (OD-20260914-P020-RECORD-V2-1 authorizes one slot), 07:39:50Z-08:01:34Z, 76 turns, exit 0, report `opus/OPUS_T0_REPORT.md` (767 lines). Pro seven-day utilization 0.81 at the end.

**VERDICT: PASS-WITH-NITS. 0 REQUIRED, 6 NITs.** Identities COMPUTED and MATCH (frozen b7548984…, 200 independent recomputations of selection-controlling values agree); 96 tests; deterministic freeze reproduced byte-for-byte; closure of T1-T4 / S1-S5 / R1-R6 / N-1..N-5 / NIT-1/4 / N4-1..N4-4 / Sol-4 verified against bytes (N4-1, N4-3 repaired with residuals raised as N5-1/N5-2). **Item 7 (the round-4 miss) done as mandated:** real pinned records loaded, `for_evaluation` 40/40 at both bounds of all 20 windows/prefixes, bar monotonicity per window, the V1.4-aborting timestamp accepted under V2, out-of-range refusals both directions; the new `PRESELECT_REFUSED_RECORD_INTERVAL` check refuses both ways. Item 8 (D5): current plan validates unchanged; derived plans with `derivation.family_order` validate; outside/duplicate/wrong-size refuse; acyclic. Item 9 (derivation tool): single read, digests describe parsed bytes, re-pin, `family_order` emitted.

| NIT | Claim | Lead check | Disposition |
|---|---|---|---|
| N5-1 | frozen artifact / procedure source / prereg carry driver line citations (`:459-493`) invalidated by the D5 edit (gate now `:460-504`) | CONFIRMED (Grok NIT 4 same) — the equivalence itself is pinned mechanically | documentation residual → next batch |
| N5-2 | `abort` swallows its own error: a persistent I/O failure leaves a zero-byte reserved file with no ABORTED record and no signal | narrower successor of N4-3; both paths still exist (re-run refused) | residual → next batch (surface the abort error in the exit message) |
| N5-3 | cost and funding records (and the plan/runbook text) still end 2025-09-22T08:00Z; inert at this HEAD (only `instrument.py` enforces an interval) but the three records disagree; suggested: extend both under the same ratification or declare documentation-only | CONFIRMED inert: Lead END-TO-END smoke (real driver + engine + records on a synthetic in-range frame) PASSED past `_profile` through `simulate_slice` — exactly the part Opus could not exercise. Grok NIT 2 same. | residual; owner may ratify extending cost/funding intervals to 2026-05-01 in the next batch (same word as D6) |
| N5-4 | `_validate_plan` reports every family-set failure as a size error (message wording) | message-quality NIT | next batch |
| N5-5 | `REPORT.md` banner omits `REPORT_R6.md` | trivial | next batch |
| N5-6 | dead parameter in the derivation tool | trivial | next batch |

Roster for V1.5 after this record: Lead REPRODUCED (+ end-to-end smoke); Grok NITS; Gemini PASS (SATISFIED); **Opus round 5 PASS-WITH-NITS**; Sol round 5 queued for the Codex Plus reset (10:06Z). None of the six NITs changes an execution outcome; none blocks the shot (Opus §Summary). Adjudicated by Claude Opus 5 Lead (session 2c48d1).
