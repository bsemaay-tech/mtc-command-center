# KICKOFF — Transport second-flagship RE-AUDIT (Claude Pro, close the slot)

Tier T0. Model `claude-opus-5` xhigh, fresh session, non-implementer. Read-only except your
single verdict file: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_CLAUDE_T0_2NDFLAG_REAUDIT_2026-08-13.md`.
No git mutation. **Run everything in the foreground — do NOT background any command and do NOT
end your turn while anything is still running; a prior lane lost its verdict that way. The
harness is slow on this host; be patient.**

## State you inherit

1. The prior Claude second-flagship audit
   (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_CLAUDE_T0_2NDFLAG_AUDIT_2026-08-12.md`,
   34422 B) returned REQUEST_CHANGES on exactly two grounds: (a) a false integrity sentence in
   `SELF_QA_TRANSPORT.md` (its own rule at `:2688-2690`), and (b) the mandated WSL harness
   execution could not run in that session (permissions). Its §2–§7 found **zero required
   findings against the seven frozen targets**, with byte identity 10/10 exact.
2. The six documentary repairs were applied at commit `a0fa8271`
   (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_PROSE_REPAIR_REPORT_2026-08-12.md`);
   the seven targets were Lead-re-verified byte-identical afterwards.
3. The original kickoff
   (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/KICKOFF_CLAUDEPRO_TRANSPORT_2NDFLAGSHIP_AUDIT.md`)
   carries the frozen seven-target identity table and the audit contract, including the harness
   invocation with the blob-materialization prerequisite (materialize blob
   `61696132a5f2fce97aad4054d41a780297ff21a1` as `<scratch>/r6/pre/remote_close_tree_wpi.sh`,
   then pass that directory as argument 2).

## Your contract

1. Re-derive the seven target identities; they must match the frozen table exactly. Re-derive
   the current `SELF_QA_TRANSPORT.md` and `STATUS_TRANSPORT.md` identities — these HAVE changed
   since the prior audit (documentary repairs only); state the new values.
2. Verify each of the six repairs against the prior verdict's §8: the false integrity sentence
   corrected to what the transcript proves; the counts (eleven J banners; 17-or-10 OpenSSH
   starts); the U-2 construction argument; the F-1 non-idempotence disclosure. Judge whether any
   repair introduced a new overclaim (Rule 9b classes).
3. **Execute the mandated WSL harness per the original kickoff's contract item 1, verbatim**,
   with the blob-materialization prerequisite. `wsl.exe` is available to this session. Quote
   the summary lines and rc; redirect bulk output to your session scratchpad, not the repo.
4. You may inherit the prior verdict's §2–§7 analysis for anything whose bytes are unchanged
   (the seven targets) — cite it rather than re-deriving beyond the identity check. Everything
   that changed (the two documents) must be judged on current bytes.
5. Verdict vocabulary: PASS / PASS-WITH-NITS / REQUEST_CHANGES. If the repairs hold and the
   harness run matches the published expectations, state the second-flagship acceptance
   sentence for the transport set explicitly. Delta gate: the path-scoped confirmation on your
   verdict file is the gate; report the whole-status delta as advisory with attribution
   (concurrent lanes commit in this worktree).
6. End with your session model/effort line.
