# KICKOFF — B3 repair round 4 (PREPARED, NOT DISPATCHED)

**STATUS: NOT AUTHORIZED. This file is prepared prep only.** The ≤3-round audit
contract was spent at round 3 (BLOCK, `audit3/AUDIT3_REPORT.md`). Round 4 runs ONLY if
Barış authorizes the bounded extra round (Option A in
`B3_REPAIR_CYCLE_RECORD.md`). Until then this file activates nothing. It exists so the
fix can start with zero design latency the moment authorization arrives. No delegate has
been dispatched against it.

Scope is deliberately minimal: the TWO surviving audit-3 REQUIRED findings, nothing
else. This is not a fresh repair round; it is a bounded closure of two named defects.

## Inputs (read these, nothing else)

- This file; `audit3/AUDIT3_REPORT.md` (findings 1 and 2 are the entire scope);
  `round3/` (the baseline — copy forward byte-identical except the two fixes).

## The only two changes permitted

1. **Audit-3 finding 1 — mount-reader read-error arm** (`round3/RP1-B3.sh:430-462`
   and `round3/RPD-VERIFY.sh:430-462`). Currently an empty nonzero `read` (e.g.
   `read error: Is a directory` on the mounts source, zero records consumed) is
   classified as ordinary EOF and returns a false `no_mount_boundary` rc 0. Fix:
   distinguish "nonzero read AND zero fields populated AND zero records seen" from a
   clean EOF, and route it to STOP with a dedicated reason
   (`mount_table_read_error`). Apply the SAME fix to both copies. The populated
   unterminated-final-record case already STOPs correctly — do not disturb it.
2. **Audit-3 finding 2 — QA D026 documentation** (`round3/SELF_QA.md`). For every
   item 1–6 closure test, record the EXACT executable RED command (round-3-minus-fix
   or round-2 code) and the EXACT GREEN command (round-4 code) plus their real output
   — not prose descriptions. Add the missing read-error arm test from fix 1 (RED:
   round-3 code returns rc 0 false pass; GREEN: round-4 code STOPs rc 3). Fix the
   section-6.13 subcount label (9 → the real count) so every displayed count is exact.

## Hard constraints

- Change ONLY what findings 1 and 2 require. Everything audit 3 verified CLOSED must
  stay byte-identical (diff round3 → round4 must show only the two fixes + their QA).
- Deliver exactly four files into `round4/`: `RP1-B3.sh`, `RPD-VERIFY.sh`,
  `DESIGN_NOTES.md` (add a "round 4" section naming the two closures), `SELF_QA.md`.
  No hidden files or caches.
- ASCII only, English only, `bash -n` clean, no host contact, nothing outside
  `round4/`.

## Closure audit after round 4

A single narrow Codex closure audit confined to the two findings + a regression sweep
of the round3→round4 diff. Verdict PASS / PASS-WITH-NITS accepts and unblocks Stage 1B
runkit re-freeze; anything else escalates to owner (no round 5).
