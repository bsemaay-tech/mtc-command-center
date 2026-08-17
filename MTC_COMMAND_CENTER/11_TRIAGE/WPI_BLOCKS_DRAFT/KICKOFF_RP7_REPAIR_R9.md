# KICKOFF — RP7-WPI-RO.sh round 9: the status-body residual comes due, plus four

You are the IMPLEMENTER. Codex is the auditor of record and re-audits your bytes.
Authorised under owner grant #7. Working dir `C:\LAB\Tradingview_LAB_CLEAN`. No host contact,
no network, no commit. UNIX LF only, zero CR bytes. Never `git checkout` a block file — use
`git cat-file blob <sha>:<path> > <path>`.

If your session cannot execute commands, write the repairs and arms, mark QA
`PENDING-LEAD-EXECUTION`, and the Lead will run them. Do not fabricate transcripts.

## Input bytes

`WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh` round-8 bytes: SHA-256
`11621044d0adc21af93e1cfc7b88ef88de8aca4683a69ab16cbc542a124141a4`, 99903 B, commit
`bb8546e6`.

Round 8's repairs were confirmed real by the auditor: the descriptor binding holds for the
status-code, parser-result, namespace and listener capture streams; the restored
two-outcome assertion rejects the `return 7` mutant; and the published command genuinely
extracts and runs the five files it names. Build on that.

## Binding scope

`WPI_BLOCKS_DRAFT/RP7_CODEX_T0_AUDIT_R8_PART_B_2026-08-11.md` — **BLOCK: 5**. Reproduce each
RED on the round-8 bytes first.

### F1 (BLOCK/HIGH) — `ro.status.body` is still both an outside-tree write primitive and a false-PASS primitive

This is the residual round 6 disclosed and round 8 carried forward. It is now a BLOCK, and
the auditor's reasoning is the part to absorb: **an accurate disclosure is not a safety
control.** `wpi_alloc_leaf` establishes only that the name was absent when an empty leaf was
created. Curl then receives the *name* via `--output "$body"`, and the digest and the parser
also receive the name. Nothing binds the object curl writes, the object the parser opens,
and the created leaf to each other. The disclosure at `SELF_QA_RP7.md:3663-3670` is accurate
and directly contradicts the block's own unqualified statements that no outside object is
changed and that rows 10–23 are read-only predicates. It sits **inside rows 20–21**, so the
rows 10–19 scope boundary does not excuse it.

Round 6 called closing this "a design change to the row-20 probe, not a repair." That was a
fair description then. It is now required. Bind the fetched body to the object the run
created — have curl write to an inherited descriptor, or verify the object identity after
the fetch and STOP on any mismatch — and make the digest and the parser read the same bound
object. A STOP condition, never a FAIL. If you conclude the network client genuinely cannot
be made to write to a descriptor here, say so explicitly and propose the alternative that
still binds identity; do not restate the disclosure.

### F2 (HIGH) — the row-22 bind-inability fence prevents the named child from running and emits a false rc 0

The fence stops the child it claims to test, then reports success. Make the fence exercise
the real path, and make its rc track what it measures.

### F3 (MEDIUM) — a fence body can forge the wrapper-owned rc-137 diagnostic

Round 8 attributed 137 from the wrapper's own `--verbose` output. A fence body can produce
that same text. Bind the attribution to something the body cannot emit, or narrow the claim
to what is actually distinguishable.

### F4 (MEDIUM) — a changed carried assertion accepts a command that never runs the round-8 body

Same family as last round's finding 1, in a different arm. Restore an assertion that fails
when the body does not run, and give the per-changed-arm discriminating-power argument the
standing rule requires.

### F5 (MEDIUM) — draft row 22 requires `detail=<d>` on namespace-read failure; both nonzero child-rc branches omit it

Either emit the field or correct the draft — and say which side was wrong and why.

## The standing rules, restated because they keep earning their keep

- A carried fence changes only with a per-change discriminating-power argument: name the
  input that used to fail and show it still fails.
- Never justify a change by a claim about the old code without executing that claim.
- **A disclosure is not a control.** Writing down that something is unbound does not bind it,
  and a truthful note beside an unqualified claim leaves the unqualified claim false.

Check against `DESIGN_DEFECT_PATTERNS_2026-08-10.md` — thirteen patterns. F1 is Pattern 11
(the declared instrument is not the executed instrument) applied to an *object* rather than a
program: the leaf that was created is not the leaf that is written and read.

## Deliverables

Repaired `RP7-WPI-RO.sh` + `SELF_QA_RP7.md` with real RED/GREEN per finding, each with its
no-weakening control and a per-changed-arm table + `STATUS_RP7.md` + narrow draft edits +
`RP7_REPAIR_R9_REPORT.md`. `bash -n` rc 0; re-derive SHA-256 and byte count; zero CR bytes via
`tr -cd '\r' < file | wc -c`. State the disposition of every finding explicitly, including
anything you do not repair and why. Do not commit — the Lead verifies and commits.
