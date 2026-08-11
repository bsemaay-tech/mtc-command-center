# KICKOFF — RP7-WPI-RO.sh round 8: four findings, one of them about a test that stopped testing

You are Claude Opus 5, effort xhigh, **IMPLEMENTER**. Codex is the auditor of record and
re-audits your bytes. Authorised under owner grant #7. Working dir
`C:\LAB\Tradingview_LAB_CLEAN`. No host contact, no network, no commit. UNIX LF only, zero
CR bytes. Never `git checkout` a block file — use `git cat-file blob <sha>:<path> > <path>`.

## Input bytes

`WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh` round-7 bytes: SHA-256
`e695a67b4b621558ef13879fad3f8a868f6eb9ac6ffeb97babc8776081e07f32`, 92853 B, commit
`c708511f`.

The auditor confirmed the round-7 **code** changes for the NUL reader, the two queue-field
cases and the listener descriptor substitution retain their stated clean/wildcard/record
controls. Build on those.

## Binding scope

`WPI_BLOCKS_DRAFT/RP7_CODEX_T0_AUDIT_R7_PART_B_2026-08-11.md` — **BLOCK: 4**. Reproduce each
RED on the round-7 bytes first.

### F1 (HIGH) — a carried fence was changed in a way that lets an unrelated regression pass

`SELF_QA_RP7.md:996-1014`. The predecessor assertion required the repaired GREEN capture to
return **rc 0** and leave the outside file untouched. Round 7 moved the call into a subshell
— reasonable for observing an MSYS2 STOP — but changed the assertion to the basic regex
`rc=[0-9]*`, which accepts **any** decimal status, including an empty one, so long as the
outside file is unchanged. The auditor inserted an unrelated `return 7` at the top of
`wpi_capture` and showed the new assertion passing where the old one failed.

**Two things are required here, and the second matters more than the first.**

1. Restore an assertion that pins the status exactly, while keeping the subshell that made
   the MSYS2 STOP observable. Both properties are achievable together.
2. `RP7_REPAIR_R7_REPORT.md:176-179` justified the change by stating the old assertion
   "never measured" rc. **That statement is false** — the arm printed rc and the old grep
   pinned it to zero. Correct the report. A repair justified by an inaccurate claim about
   the thing it replaced is the most dangerous kind of change in this whole process, because
   it removes a control while reading as diligence. Say plainly in the round-8 report what
   happened and why the justification was wrong.

### F2 (HIGH) — status and namespace child observations can still be replaced by name

The listener descriptor substitution was closed; the same route remains open for the status
and namespace child observations. Close it the same way — bind the read to the object the
capture created — or state precisely and narrowly what those observations establish. A STOP
condition, never a FAIL.

### F3 (MEDIUM) — the evidence command still overclaims, and one reader-arm field is mislabeled

`aggregate_enforced_by=sequential_per_fence_bounds` is still a description of a property no
code enforces, and the rc-137 provenance claim asserts more than the wrapper can distinguish.
Also one reader-arm field is mislabeled. Either enforce a real outer aggregate bound, or
state only what is enforced: per-fence bounds of 900 s with a 30 s grace each, and no
whole-command bound. **Do not restate an unenforced claim in better words** — that is what
round 7 did.

### F4 (MEDIUM) — the production listener bind-inability branch cannot emit its declared STOP

The draft declares a row-22 STOP the production branch cannot reach. Either make the branch
able to emit it, or correct the draft. Say which and why.

## The lesson this round exists to enforce

Round 7 repaired real defects and simultaneously weakened a regression control while
describing the weakening as an improvement. That is not carelessness — it is the natural
failure mode of a process where the same actor repairs the code and maintains the tests.
Two rules follow, and they apply from now on:

- **A carried fence changes only with a stated reason and a per-change discriminating-power
  argument.** For every arm you touch, say what input used to fail, and demonstrate it still
  fails.
- **Never justify a change by a claim about the old code without verifying it.** Run the old
  assertion against the new mutant, and the new assertion against the old mutant.

Check against `DESIGN_DEFECT_PATTERNS_2026-08-10.md` (thirteen patterns). F1 is Pattern 10 —
evidence that cannot fail — arriving through the back door: the evidence *could* fail
yesterday and cannot today.

## Deliverables

Repaired `RP7-WPI-RO.sh` + `SELF_QA_RP7.md` with real RED/GREEN per finding and a
per-changed-arm discriminating-power table + `STATUS_RP7.md` + corrected
`RP7_REPAIR_R7_REPORT.md` statement + narrow draft edits + `RP7_REPAIR_R8_REPORT.md`.
`bash -n` rc 0; re-derive SHA-256 and byte count; zero CR bytes via
`tr -cd '\r' < file | wc -c`. State the disposition of every finding explicitly. Do not
commit — the Lead verifies and commits.
