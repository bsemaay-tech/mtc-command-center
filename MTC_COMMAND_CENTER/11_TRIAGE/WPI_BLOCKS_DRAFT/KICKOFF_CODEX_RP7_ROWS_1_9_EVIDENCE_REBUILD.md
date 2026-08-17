# KICKOFF — rows 1-9 D026 evidence REBUILD (rejected: simulated harness)

Codex `-Account free`, xhigh. Working dir `C:\LAB\Tradingview_LAB_CLEAN`. You continue the
rows 1-9 build you (or a sibling session) just delivered. The Lead has NOT committed your
edits; the working tree still carries them. No git mutation.

## Why this round exists — the rejection, stated plainly

Your D026 matrix was produced by a **Python re-implementation** of the B2/B4 adjudication
logic, fed synthetic dicts (`RP7_ROWS_1_9_BUILD_CODEXFREE_RUN_2026-08-13.log:16051-16195`:
`eval_b2`, `parse_exec`, `parse_fragment`, `eval_b4` are Python rewrites; several GREEN lines
are literal tuples such as `(0,'B2_active state=active …')`). **Not one line of
`RP7-WPI-RO.sh` was executed to produce that transcript.** That is Pattern 11 — the declared
instrument is not the executed instrument — and the repo's standing lesson: a generated matrix
can pass while proving nothing. Evidence in `SELF_QA_RP7.md` that presents those lines as the
block's RED/GREEN behaviour is not acceptable and will not be committed.

The block code changes themselves (`RP7-WPI-RO.sh` B2/B4 sections) are not rejected — they
await real evidence and then flagship re-audit.

## The rebuild — binding contract

1. **Every D026 RED/GREEN/CONTROL line must be produced by executing the block's own code.**
   Use the established fence pattern in this lane: extract the B2/B4 function definitions from
   the delivered `RP7-WPI-RO.sh` bytes (bind the block identity first: re-derive bytes+SHA and
   assert them in the harness), then drive those functions under
   `bash --noprofile --norc` with fixture `systemctl show` captures (text files / here-docs
   representing each mutation). The block parses captured `show` output — it can be driven
   without a live systemd.
2. **No Python re-implementation of any block logic.** Trusted `python3 -I -S` may appear only
   where the block itself invokes it (the row-6 fragment parser), and then only by invoking
   the block's own code path.
3. **No literal result tuples.** Every GREEN is the block's executed output on the repaired /
   expected fixture; every RED is the block's executed output on the mutated fixture. If a row
   genuinely cannot be driven on this host (needs a live manager), mark that row
   `PENDING-WSL-EXECUTION` under a PENDING heading, with the exact command a WSL session must
   run — never simulate it.
4. Replace the simulated matrix in `SELF_QA_RP7.md` completely: the new section must name the
   harness (embedded, extractable via a published `sed | bash` command like the other fences),
   paste the executed transcript, and state the block identity asserted before and after.
5. Re-derive and restate all identities after your final edit (`RP7-WPI-RO.sh` should be
   UNCHANGED from 126146 B / `29832d63…` unless you must fix a defect the real execution
   exposes — if you do, say so loudly and re-derive).
6. Update `STATUS_RP7.md` and append a rebuild section to
   `RP7_ROWS_1_9_REPORT_2026-08-13.md` describing the rejection and the rebuild honestly.

## Files you own

The same four: `RP7-WPI-RO.sh` (only if a real defect surfaces), `SELF_QA_RP7.md`,
`STATUS_RP7.md`, `RP7_ROWS_1_9_REPORT_2026-08-13.md`. Nothing else. No git mutation. No
sub-delegation. State your session-header model in the report.
