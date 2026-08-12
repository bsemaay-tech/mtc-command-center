# KICKOFF — Claude Pro T0 audit: RP7-WPI-RO.sh round 9, SECOND FLAGSHIP (dual-acceptance gate)

You are `claude-opus-5` xhigh via the default Claude Pro account, AUDITOR — the second
flagship. Codex `gpt-5.6-sol` already holds flagship PASS on these bytes
(`RP7_CODEX_T0_AUDIT_R9`: all five r8 findings closed, including the F1 `ro.status.body`
BLOCK — the fetched body is now bound to the created leaf by descriptor, `wpi_alloc_leaf`
deleted). Claude MAX implemented r9, so YOU (a fresh Claude Pro session that implemented
nothing on this block) are the required independent second flagship. Working dir
`C:\LAB\Tradingview_LAB_CLEAN`. Read-only on the repo: edit nothing except your verdict
file, no git mutation, no remote host, no network. Local fixture execution exactly as the
published harness does it is permitted.

## Bytes under audit
`RP7-WPI-RO.sh` as committed on `feature/donchian-crypto-ladder`. Start from
`STATUS_RP7.md` (this directory), then `SELF_QA_RP7.md` (§ROUND 9) and
`RP7_R9_REPORT` for the published harness and evidence, then the Codex r9 verdict.
Verify the narrative against the bytes — do not inherit Codex's conclusions.

## The r9 headline you must independently re-establish
The round-6 residual that came due: `ro.status.body` was create-once allocated then
addressed BY NAME by curl, digest, and parser — a hard link or name swap could overwrite
outside the evidence tree or flip an ARMED body to an accepting DISARMED result. r9 binds
the leaf by DESCRIPTOR end to end (curl `--output /dev/fd/3` dup'd from the `O_CREAT|O_EXCL`
open; parser reads the same descriptor as stdin and digests exactly what it parses;
`wpi_alloc_leaf` deleted). Also: descriptor-bind STOP reports measured child rc, not a
caller literal; row-22 `detail` field emitted on both nonzero namespace-read branches.

## Audit contract
1. Run the published SELF-QA harness VERBATIM (record real rc/summary lines). No
   extract-and-run.
2. Adversarially attack the descriptor binding: is there ANY remaining site where an
   evidence leaf is created and later addressed by a rebindable name? Any second reader of
   a name? Any caller-declared rc literal surviving?
3. Confirm rows 10–23 read-only claims now hold inside rows 20–21 (the class the r6
   disclosure admitted), and row 24 stays operator-side only.
4. Thirteen-pattern adjudication table. Verdict: PASS / PASS-WITH-NITS / REQUEST_CHANGES /
   BLOCK. If accepting, state that RP7 reaches DUAL FLAGSHIP ACCEPTANCE — which also
   unlocks the owner-decided rows 1–9 build (BUILD ALL NINE, applied only after this
   acceptance).

Write ONE new file: `RP7_CLAUDE_T0_2NDFLAG_AUDIT_2026-08-12.md` (this directory).
Prove `git status --porcelain` shows only that file at the end.
