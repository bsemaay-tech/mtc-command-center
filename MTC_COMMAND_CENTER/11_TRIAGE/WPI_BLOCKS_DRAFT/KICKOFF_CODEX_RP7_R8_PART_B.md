# KICKOFF — RP7 round-8 review: rows 20–24, the evidence contract, and the restored control

Fresh `gpt-5.6-sol` session, effort xhigh. Report only; edit nothing except your output
file. Working dir `C:\LAB\Tradingview_LAB_CLEAN`. No host contact, no network, no commit.

`RP7-WPI-RO.sh` is a read-only environment preflight block for a maintenance job: it looks
at an already-provisioned host, records what it finds, and prints one machine-readable line
per checked row. It changes nothing. Confirm **each branch reports an honest result** — an
accepting line only when the observation established it, an inability to observe reported as
STOP rather than as a completed negative observation, and no printed wording stronger than
the code supports.

**Scope: rows 20–24, the evidence/QA contract, and the four round-7 findings.** Rows 10–19
and the earlier repairs are out of scope and are covered only by carried fences.

## Subject

`WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh` — **round-8 bytes**, SHA-256
`11621044d0adc21af93e1cfc7b88ef88de8aca4683a69ab16cbc542a124141a4`, 99903 B, commit
`bb8546e6`. Re-derive hash, byte count, CR bytes and `bash -n` first. Round-7 predecessor:
`e695a67b4b621558ef13879fad3f8a868f6eb9ac6ffeb97babc8776081e07f32`, 92853 B, commit
`c708511f` — materialise with `git cat-file blob`, never `git checkout`.

## Your four round-7 findings, and what round 8 claims

1. **The changed carried fence accepted an unrelated regression.** Claimed repaired: the
   exact two-outcome status pin is restored while keeping the subshell, a `return 7` mutant
   is added as a RED arm in two fences, and both the old and new assertions were run against
   the same three outputs. **Verify the restored assertion actually rejects the mutant**, and
   that keeping the subshell did not reintroduce any other looseness.
2. **Status and namespace child observations replaceable by name.** Claimed repaired: both
   capture streams descriptor-bound, with the row-20 status code, row-21 parser result, both
   row-22 namespace records and the diagnostic-stream emptiness all read through them, no
   name fallback. **The implementer discloses that readers outside rows 20–22 — rows 10–19's
   tree/metadata/interpreter/verifier and the read-diagnostic leaves — are still name-opened,
   and names that as the next likely finding.** Judge whether the in-band repair is complete
   and whether the disclosure is accurate; the out-of-band readers are out of scope here.
3. **The evidence command overclaimed rc-137 provenance and a whole-command aggregate.**
   Claimed repaired: wrappers instrumented with `--verbose` so a 137 is attributed from the
   wrapper's own diagnostic; the enforcement claim **withdrawn** rather than reworded; the
   mislabelled reader-arm field renamed. The result line now reads
   `fence_timeout_budget_s=4650 whole_command_bound=none prelude_bounded=no`. **Judge whether
   that is now truthful and complete** — in particular whether `prelude_bounded=no` is an
   honest admission or a gap that should be closed.
4. **The listener bind-inability branch could not emit its declared STOP.** Claimed repaired
   **by making the branch reachable**, not by editing the draft. Verify the branch is genuinely
   reachable and that the emitted line matches the declared form exactly.

## What the Lead verified — extend it

The Lead ran the published command verbatim on these bytes:

```text
R8_FENCE_RC=0 R7_FENCE_RC=0 R6_FENCE_RC=0 R5_FENCE_RC=0 R4_FENCE_RC=0
PUBLISHED_COMMAND_RESULT=pass fences=5 per_fence_bound_s=900 kill_grace_s=30
  fence_timeout_budget_s=4650 whole_command_bound=none prelude_bounded=no
```

and the in-fence failure arm yields `PUBLISHED_COMMAND_RESULT=fence_failed fence=r6 rc=7`.

**Two things the Lead did not check, which are yours.** First, whether each published
command runs the thing it names — in the parallel RP6 work a documented command piped a
harness into `bash --noprofile --norc "$mutant"`, so Bash ran the mutant file and ignored
stdin, producing confident output from the wrong program. Check every published command in
`SELF_QA_RP7.md` for that class of error. Second, whether any carried fence changed in a way
that reduces discriminating power — that is what produced finding 1 last round, so give a
per-changed-arm verdict.

## Rows 20–24 and the draft

Conformance at the exact FAIL/STOP wording in
`WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` §8.2. Round 8 made draft edits for the
rows 20/21/22 namespace half as a consequence of finding 2 — verify block and draft agree and
that no edit widened what the block may claim.

## Known freeze-gate items — not findings

The `<PIN-AT-FREEZE>` constants and the accepting `wpi_validate_inputs` branch. §8.2 rows 1–9
are implemented by no block and are a separate owner decision.

## Patterns

`DESIGN_DEFECT_PATTERNS_2026-08-10.md`, thirteen patterns. This band has now produced five
instances of evidence that looks conclusive and establishes nothing. Assume a sixth exists.

## Output

Write **only** `WPI_BLOCKS_DRAFT/RP7_CODEX_T0_AUDIT_R8_PART_B_2026-08-11.md`: verdict for
your band first, then a row table with evidence, then findings most severe first with
command, rc and output, then a section on published-command integrity and one on any changed
carried arms. State plainly which bands were out of scope.
