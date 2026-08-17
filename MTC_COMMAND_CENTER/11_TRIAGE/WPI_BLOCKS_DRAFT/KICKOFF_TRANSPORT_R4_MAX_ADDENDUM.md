# ADDENDUM — Transport round 4 rebuild, Claude Max dispatch 2026-08-11

Read and execute `KICKOFF_TRANSPORT_REPAIR_R4.md` (same directory) with the following
binding additions from the Lead. You are `claude-opus-5` xhigh via the Max account.

1. **The concurrent session's partial edit is SUPERSEDED.** Commit `cf049b6b` edited
   `remote_close_tree_wpi.sh` in a non-operational way: it requires a third `WORK_ROOT`
   argument no plan byte passes, and its clean launch self-STOPs, making the new STOP path
   unreachable. Do not build on that edit. Start from the round-3 bytes of all nine files
   (commit `78173bfd`) and re-apply what is worth keeping only if you can show its STOP
   path reachable from a plan-passed invocation.
2. **Follow the ordered resumption list** in `TRANSPORT_STATE_ASSESSMENT_2026-08-11.md`
   (same directory). That assessment is the current state authority: F4/T5/T7/T8 not
   started; F1/F2/T6 partial; F3 unreachable as written.
3. **T5 is load-bearing:** `run_p0.sh` currently exports NONE of the five `P0_ATTESTED_*`
   values `RP6-P0.sh` requires, so the composition STOPs before any host observation.
   Prove the repaired composition passes them by executing the launch path locally with
   the connection stubbed, not by asserting it.
4. Reminders that have burned prior rounds: never credit an item as done on the strength
   of a comment claiming it; a disclosure is not a control; every fixture RED before
   GREEN (D026); LF-only shell bytes (write via bash heredoc or byte-checked writes,
   `tr -cd '\r' < f | wc -c` must be 0); `transport_runner.ps1` stays PowerShell
   5.1-compatible; no commit, the Lead commits.
5. Output: repaired file set + `TRANSPORT_R4_REPORT_2026-08-11.md` with per-item
   dispositions for F1–F4, T5–T8, and every kept/dropped piece of the superseded edit,
   plus executed self-QA transcripts (`PENDING-LEAD-EXECUTION` only where your session
   truly cannot execute).
