# KICKOFF — RP7-WPI-RO.sh round 7: four findings from the round-6 part-B re-audit

You are Claude Opus 5, effort xhigh, **IMPLEMENTER**. Codex is the auditor of record and
re-audits your bytes, so separation holds. Authorised under owner grant #7. Working dir
`C:\LAB\Tradingview_LAB_CLEAN`. No host contact, no network, no commit. UNIX LF only, zero
CR bytes. Never `git checkout` a block file — use `git cat-file blob <sha>:<path> > <path>`.

## Input bytes

`WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh` round-6 bytes: SHA-256
`6586698c707601c70a3e99903dc789ee2ee71fd2bae1bc1763adc52f72a40709`, 88460 B, commit
`3e2a976a`.

Round 6's repairs were confirmed by the auditor — the four round-5 findings are
substantially closed, the padded-listener / wildcard / `500` / `401` controls hold, and
`wpi_open_leaf` genuinely binds the shell-side write to the object its create-once open
created. **Build on that; do not re-litigate it.**

## Binding scope

`WPI_BLOCKS_DRAFT/RP7_CODEX_T0_AUDIT_R6_PART_B_2026-08-11.md` — **BLOCK: 4**. That text
binds, including its executed evidence. Reproduce each RED on the round-6 bytes first.

1. **F1 (HIGH) — the common single-record reader normalises NUL-bearing records into
   accepting observations.** Make every use of `wpi_single_record` byte-preserving *before*
   Bash can delete NUL, and account for every captured byte. A NUL or any other
   unrepresentable record must STOP before status, parser-result or namespace semantics are
   applied. Add real predecessor/current RED/GREEN arms for all three affected records.
2. **F2 (HIGH) — nonnumeric listener queue fields reach a complete accepting listener
   set.** `:1260-1266`, especially `:1265`: the parser validates the *combined* string
   `"$recvq:$sendq"` against a class that permits the separator, so a field can be empty or
   itself contain a colon. Validate `recvq` and `sendq` **separately** as nonempty
   decimal-digit fields before any inventory-complete line. Keep the published
   column-padding and wildcard controls.
3. **F3 (HIGH) — draft row 22 claims a byte identity the disclosed reader residual does not
   establish.** The draft says the inventory is read as one string "so that the byte string
   adjudicated is the byte string captured", but the child closes its descriptors and the
   reader re-opens the path at `:1246`. Two honest options — pick one and say why: keep and
   read the capture descriptor so the read is bound to the created object, **or** narrow row
   22 and the `bytes=` description to the re-opened evidence object actually adjudicated.
   **Do not state captured/adjudicated equality while residual 2 stands.** This is the
   round-6 residual coming back as a finding because the draft overclaimed it — the right
   move is to make the claim match what the code establishes.
4. **F4 (MEDIUM) — the evidence command propagates assertion failure but misclassifies
   kill-after timeout and does not enforce its claimed aggregate.** Round 6 fixed rc
   propagation — the Lead verified that independently — but a fence killed after the grace
   period exits **137**, not 124, and lands in the generic failure branch; and the "2700 s
   aggregate" is a documented claim no code enforces, and it does not include the three
   30-second graces. Classify kill-after outcomes distinctly, and either enforce a real
   outer aggregate bound or document a truthful one that includes every grace. Add a
   TERM-ignoring fence to the published failure evidence so the kill-after path is proven,
   not asserted.

## The through-line

F1, F2 and F3 are all the same shape: **a value is admitted, transformed, or re-read, and
the claim made about it is stronger than what survived the transformation.** F1 loses bytes
to Bash's NUL handling; F2 validates a concatenation instead of its fields; F3 claims
identity across a close-and-reopen. Pattern 13 in the amended
`DESIGN_DEFECT_PATTERNS_2026-08-10.md` (thirteen patterns now) names this directly: every
admitted member needs exactly one terminal disposition, and identity must be carried
unchanged across every boundary — or the claim must be narrowed to what survives.

## Deliverables

Repaired `RP7-WPI-RO.sh` + `SELF_QA_RP7.md` with real RED/GREEN per finding, each with its
no-weakening control + `STATUS_RP7.md` + narrow draft edits + `RP7_REPAIR_R7_REPORT.md`
(finding → disposition → evidence, draft-edit list, freeze-gate inputs). Carry the existing
fences unchanged where possible and say which were carried byte-identical. `bash -n` rc 0;
re-derive SHA-256 and byte count; zero CR bytes via `tr -cd '\r' < file | wc -c`. State the
disposition of every finding explicitly, including anything you do not repair and why. Do
not commit — the Lead verifies and commits.
