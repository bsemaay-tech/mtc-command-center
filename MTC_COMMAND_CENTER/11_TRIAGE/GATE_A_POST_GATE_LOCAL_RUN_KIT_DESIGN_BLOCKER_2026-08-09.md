# Gate A post-Gate local run-kit design — third-round blocker (2026-08-09)

## Outcome

**BLOCKED after the third non-accepting repair round.** The proposed design was not committed, was not
integrated, and was not sent to canonical audit. Repo rules forbid a silent fourth repair round.

The unaccepted draft is preserved only in the isolated worktree:

- worktree: `C:\PGRK`
- base: `4599b466def320cd4afeeb238e0e192303bd85c4`
- untracked path: `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_POST_GATE_LOCAL_RUN_KIT_DESIGN_2026-08-09.md`
- SHA-256: `d12e25fb06273b006c47342fac093d4afc99e32bda815fb5e428b8a3da584107`
- size / lines: `194207` bytes / `2332` lines

## Reproduced required finding

`RK-B0` creates an evidence bootstrap contradiction:

1. Section 2.5 requires every host command to be recorded as `.cmd/.out/.err/.rc` under `<EVROOT>`.
2. Section 2.5a says `STOP` is called only inside that recorder, so stderr and rc are preserved there.
3. But `RK-B0` runs the candidate-Python verification, timestamp allocation, parent `mkdir -p`, and
   leaf `mkdir` before `<EVROOT>` exists. Those commands cannot be recorded under `<EVROOT>`, and a
   pre-root `STOP` has no four-file recorder.
4. The same bootstrap leaves the parent-path canonical/non-symlink proof and the no-clobber transfer of
   `EXPECTATIONS.md` underspecified before the first evidence write.

This is not cosmetic: the design cannot simultaneously claim complete four-file evidence, no-clobber
path safety, and an evidence root that is created only after unrecorded prerequisites run.

## Required closure for any owner-directed new cycle

Specify and independently accept one fail-closed bootstrap channel before `<EVROOT>` exists, including:

- where the first command, stdout, stderr, and rc are recorded without clobbering prior evidence;
- how `/home/gatea/runkit` and every parent are proven canonical and non-symlink before creation/use;
- how collision, permission, interpreter, timestamp, and `mkdir` failures are preserved and halt;
- how `EXPECTATIONS.md` is transferred with a destination that is neither an existing object nor a
  live/dangling link, then hashed against the preregistered local value;
- how bootstrap evidence is atomically bound into the final `<EVROOT>` manifest without overwrite.

Only after that repair may the design be frozen and sent to the D025 four-auditor roster. The still-open
`D-GAP-C1-1` and `D-GAP-C1-3` remain blocking independently.

## Safety and scope

No host command, SSH, service action, credential access, broker/TESTNET action, ARM, order, deployment,
WP-V, KVM2, master merge, or economic action occurred. Candidate `2ce41e34…321b` and staging state were
not changed. The live branch independently advanced to `779bd038` with one separate proposed command-gap
document; this blocker record does not accept or modify that proposal.

## Next safe unit

Read-only, independently inspect commit `779bd038` and
`MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_2026-08-09.md` for candidate qualification,
scope, and whether it contains reusable bootstrap evidence. This is a separate audit unit, not a fourth
repair of the blocked `C:\PGRK` design.
