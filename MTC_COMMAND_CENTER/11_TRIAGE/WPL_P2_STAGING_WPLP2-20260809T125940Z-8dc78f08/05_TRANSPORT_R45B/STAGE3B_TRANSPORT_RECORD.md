# WP-L Phase 2 — Stage 3B transport record (R4-5 re-attempt)

Unit: `WPLP2-20260809T125940Z-8dc78f08` · Lead session (Claude Fable 5), 2026-08-09 evening
Preregistration: `../04_PREREG_R45B/PREREGISTRATION_R45B.md` (written and hash-frozen
**before** any R45B remote invocation; dry run verified the 4-op plan first).

Result: **TR_RUN PASS — all 4 ops rc=0 — R4-5 PASS, both arms exactly as preregistered.**

## Execution (`-Execute -Confirm WPLP2-20260809T125940Z-8dc78f08-R45B-EXECUTE`)

| op | kind | rc | outcome |
|---|---|---|---|
| 01 | ssh run_r45b.sh | 0 | all four remote artifacts hash-verified byte-for-byte, evidence leaf allocated create-once, runner rc 0 |
| 02 | ssh remote_close_tree.sh | 0 | `CLOSE PASS files=1 wrote_into_evidence_tree=0`, digest set stable across 2 passes |
| 03 | scp evidence down | 0 | `r45b.log` retrieved |
| 04 | local_bind | 0 | **TR_BIND_PASS files=1**; `CLOSE_DIGEST_SET_SHA256 1f74d69af7da8fd5cd5cfad7ba698ce0637fe34401606426d3f2d805ff1baf7f` reproduced bit-identical locally; `r45b.log` = `00078e7e…`, 4521 bytes |

## What R4-5 proved (from the bound `r45b.log`)

Falsification target: the two-line `dst_path.is_symlink()` `Fail` guard in `RP4-C3
restore_into` (D026 Arm 1, guard-scope only — no C3 verdict claimed, C3 stays BLOCKED).

- Mutation discipline held: mutant differs from the accepted `RP4-C3.py` (`0520cc90…`,
  12770 bytes, 295 lines) by **exactly** lines 124–125; the two removed lines and the
  full unified diff are in the evidence log (`R45_mutant_diff_sha256 a776d1b9…`).
- **RED arm (guard deleted): the harm is real.** `restore_into` returned without
  exception through a dangling symlink `red/dest/restored.db → red/outside/target.db`;
  post-state: a real SQLite database (`target_magic=b'SQLite format 3\x00'`, 8192 bytes,
  3 rows readable) written **outside the restore root**.
- **GREEN arm (accepted bytes): the guard stops it.** Exception raised with exactly the
  predicted message `restore destination is a symlink: /tmp/r45.p3adetdb/green/dest/restored.db`;
  target absent afterwards, symlink unchanged; classified to RP4-C3's FAIL_RC mapping.
- Verdict: the guard is **load-bearing** — its deletion converts a refused restore into
  a silent write outside the restore root. `R45 PASS arms=red,green
  both_expected_outcomes=observed`, `R45_RC=0`.
- Remote fixture root `/tmp/r45.p3adetdb` preserved (`cleanup=never`), per first-FAIL /
  no-clobber discipline even on PASS.

This closes the one Stage-2 item that could not close on Windows (real symlink
semantics required). Predicted outcomes #6 and #7 of the Stage 2 preregistration §8 —
re-preregistered unchanged as R45B expectations #1–#2 — both **held**.

## Committed-copy note and ledger

`operator_record/` is a bit-identical copy of the create-once record root
`C:\WPI_ARTIFACTS\WPLP2_TRANSPORT_WPLP2-20260809T125940Z-8dc78f08-R45B` (which remains
untouched). `operator_record/evidence/…-R45B/r45b.log` is excluded from git by the repo
guard's log-file rule; its identity is bound above and in
`operator_record/TRANSPORT_SHA256SUMS.txt`.

Ledger (prospective, per unit): Stage 3 + Stage 3B together booked **0.4 h** against the
ratified balance (~28.7 h remaining at WP-L P2 Stage-1+2 booking → ~28.3 h). No
retroactive reconstruction.

## Safety state after Stage 3B

Zero service mutation, zero ARM, zero credential contact — unchanged. Remote writes:
the create-once evidence leaf and the preserved `/tmp` fixture only. RUNID `…-R45B`
consumed (stage completed). C1, C2, C3, C4, C5 not touched; B3 remains blocked on
`B3-GAP-ENV` pending owner decision.
