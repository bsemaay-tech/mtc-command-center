# KICKOFF — RP7 round-7 review: rows 20–24, the evidence contract, and the carried-fence question

Fresh `gpt-5.6-sol` session, effort xhigh. Report only; edit nothing except your output
file. Working dir `C:\LAB\Tradingview_LAB_CLEAN`. No host contact, no network, no commit.

`RP7-WPI-RO.sh` is a read-only environment preflight block for a maintenance job: it looks
at an already-provisioned host, records what it finds, and prints one machine-readable line
per checked row. It changes nothing. Confirm **each branch reports an honest result** — an
accepting line only when the observation established it, an inability to observe reported as
STOP rather than as a completed negative observation, and no printed wording stronger than
the code supports.

**Scope: rows 20–24, the evidence/QA contract, and the four round-6 findings.** Rows 10–19
and the round-5 repairs are out of scope and are covered only by carried fences.

## Subject

`WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh` — **round-7 bytes**, SHA-256
`e695a67b4b621558ef13879fad3f8a868f6eb9ac6ffeb97babc8776081e07f32`, 92853 B, commit
`c708511f`. Re-derive hash, byte count, CR bytes and `bash -n` first. Round-6 predecessor:
`6586698c707601c70a3e99903dc789ee2ee71fd2bae1bc1763adc52f72a40709`, 88460 B, commit
`3e2a976a` — materialise with `git cat-file blob`, never `git checkout`.

## Your four round-6 findings

From `RP7_CODEX_T0_AUDIT_R6_PART_B_2026-08-11.md` (BLOCK: 4):

1. The common single-record reader normalised NUL-bearing B5/B6 records into accepting
   observations.
2. Nonnumeric listener queue fields reached a complete accepting listener set — the parser
   validated the combined `"$recvq:$sendq"` against a class permitting the separator.
3. Draft row 22 claimed a captured/adjudicated byte identity the reader residual did not
   establish.
4. The evidence command misclassified kill-after timeout and did not enforce its claimed
   aggregate.

Confirm each repair **and its no-weakening control**.

## The item this run must not wave through

**The round-6 fence was carried but is NOT byte-identical** — the report names four changes
to it (`RP7_REPAIR_R7_REPORT.md`, fence table: round-6 body
`b080dad4315281d0447baff10dae26797ba04998bc7c9e32fb2bbbd15a570a06`, 27355 B). A carried
regression fence that changes is exactly how a repair can quietly stop testing what it used
to test. For **each** of the four named changes, determine whether it preserves the arm's
original discriminating power or weakens it, and say so per change. If any change makes a
previously failing input now pass for a reason unrelated to the repair, that is a finding
outranking everything else in this run.

The round-4 and round-5 fences are claimed carried; verify which are byte-identical.

## What the Lead already verified — extend it, do not repeat it

The Lead ran the published command exactly as written on these bytes:

```text
R7_FENCE_RC=0 R6_FENCE_RC=0 R5_FENCE_RC=0 R4_FENCE_RC=0
PUBLISHED_COMMAND_RESULT=pass fences=4 per_fence_bound_s=900 kill_grace_s=30
  aggregate_bound_s=3720 aggregate_enforced_by=sequential_per_fence_bounds
```

and the in-fence failure arm still yields `PUBLISHED_COMMAND_RESULT=fence_failed` at
`R6=7, R5=9`. So rc propagation and the happy path are established. **Your job is the parts
that were not tested:** whether a TERM-ignoring fence now classifies distinctly from an
assertion failure (rc 137 path), and whether `aggregate_enforced_by=sequential_per_fence_bounds`
is a truthful description of what the code actually enforces rather than a restatement of the
same unenforced claim in better words.

## Rows 20–24 and the draft

Conformance at the exact FAIL/STOP wording in
`WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` §8.2. Round 7 made draft edits —
verify block and draft now say the same thing, that row 22's claim matches what the reader
binding establishes, and that no edit widened what the block may claim. The round-7
reader-binding arms report `child_captured_sha256` against `adjudicated_name_sha256` with an
independent `wc -c` cross-check; judge whether that measurement is sound and whether the
`bytes=` field means what the draft now says it means.

## Method

Prefer executed tests over code reading. Self-contained `mktemp -d` trees, removed after.
Record exact command, rc and observed output for everything claimed.

## Known freeze-gate items — not findings

The `<PIN-AT-FREEZE>` constants and the accepting `wpi_validate_inputs` branch, so no
whole-block accepting run can exist before freeze. §8.2 rows 1–9 are implemented by no block
and are a separate owner decision.

## Patterns

`DESIGN_DEFECT_PATTERNS_2026-08-10.md`, thirteen patterns. Your three round-6 HIGHs were all
pattern-13 shaped — a value admitted, transformed or re-read, with a claim stronger than what
survived. Check whether that class is now closed or merely moved.

## Output

Write **only** `WPI_BLOCKS_DRAFT/RP7_CODEX_T0_AUDIT_R7_PART_B_2026-08-11.md`: verdict for
your band first, then a row table with evidence, then findings most severe first with
command, rc and output, then a dedicated section on the four carried-fence changes. State
plainly which bands were out of scope.
