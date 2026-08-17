# Lead QA execution — RP6-P0 round 7

GLM's session gates command execution, so it wrote the harnesses and marked every QA entry
`PENDING-LEAD-EXECUTION` rather than fabricating transcripts. That is the accepted path.
The Lead ran them. This file records what actually happened, including two failures.

Subject: `RP6-P0.sh` round-7 bytes, SHA-256
`fa852d7e0a984f977a489bd565834c1ced32eab4fd81221388a25a6bad6483cd`, 103071 B, zero CR
bytes, `bash -n` rc 0. Git Bash, clean shell, `</dev/null`, each fence bounded by
`timeout 240`.

## Round-7 harnesses — all PASS

| Harness | Cases | Result | rc |
|---|---:|---|---:|
| `R7_F2` (builtin `type -t`, override defeated) | 4/4 | PASS | 0 |
| `R7_F3` (noglob before the outer pin split) | 4/4 | PASS | 0 |
| `R7_C3` (producer shape before any rc-1 verdict) | 8/8 | PASS | 0 |

These carry genuine RED/GREEN pairs: `R7_F2` shows a caller-defined `type()` letting a
missing symbol through on the old path and STOPping on the new one; `R7_F3` shows the
crafted-cwd whole-token case accepted before and STOPping identically in clean and crafted
cwds after; `R7_C3` shows an empty canonicalization producing rc 1 FAIL before and rc 3
STOP after.

## Legacy fences, re-run by anchored marker — three PASS, two FAIL

| Fence | rc | Elapsed | Result |
|---|---:|---:|---|
| `C13_R3_BACKSTOP` | 0 | 1 s | PASS, 4 cases |
| `F2_FREEZE_GATE` | 0 | 0 s | PASS |
| `C13_R4B` | 0 | 9 s | PASS, 27 cases |
| `RP6_FULLBLOCK_D026` | **1** | 7 s | **FAIL**, no summary emitted |
| `RP6_R4_D026` | **1** | 41 s | **FAIL**, `findings=4` |

The marker migration itself works: extraction by `^# <NAME>_HARNESS_BEGIN$` /
`^# <NAME>_HARNESS_END$` no longer re-enters the range at the Markdown invocation line, which
was the round-6 defect. The R4 fence also now returns in 41 s, inside its documented bound —
the "open descendant handle" half of correction 5 appears closed.

## Root cause of both failures — fixture drift, not a block regression

Both failures are the same defect in the **fences' own arm construction**:

```text
/tmp/.../pin-3487.sh: line 17: P0_FIXED_STAT: unbound variable
/tmp/.../f4-post.sh:  line 15: P0_FIXED_STAT: unbound variable
```

The legacy fences synthesise a partial test arm by `sed`-slicing the block between two
source landmarks. Correction 7 introduced ten frozen `P0_FIXED_*` constants — `P0_FIXED_STAT`
is at `RP6-P0.sh:289` — which fall outside those slices. The arm therefore references a
constant it never defined, `set -u` aborts it, and the arm exits **rc 1**.

Consequences worth stating plainly:

1. **Correction 5 is not fully closed.** Its instruction was to make evidence commands
   literal and bounded so a third party can re-run them. The markers were migrated, but the
   fences still build their arms by slicing the source, so they break exactly as the block
   grows — the same defect one level down. Anchored extraction of the *fence* does not help
   if the *fence* then line-slices the *block*.
2. **rc 1 is FAIL grammar.** An unbound variable under `set -u` exits 1, which in this
   block's vocabulary means "a completed probe established deviant host state". Here it is
   only a harness, but it is the same shape the Claude round-2 re-audit flagged as a
   standing hazard, and it is why these two failures look like regressions at a glance.

## One item that is not explained by fixture drift

`RP6_FULLBLOCK_D026` also reports:

```text
ASSERT_UNMET label=F7_TOOL_POST
  token=[tool_not_evaluable tool=getent path=/tmp/.../nonexec-tool rc=na
         detail=access_builtin_x_denied mechanism=access_builtin_x]
```

Correction 7 changed tool resolution (twelve mandatory exact pins, unpinned fallback
deleted), so the non-executable-tool path may legitimately report differently now. **This is
not classified.** It is explicit scope for the T0 re-audit: either the new token is correct
and the fence's expectation is stale, or the repair changed a not-evaluable classification
it should not have.

## Lead disposition

Round 7 is committed as a **draft round with two failing legacy fences and one unclassified
token change**, not as a clean round. The three new harnesses genuinely close corrections 1,
2 and 3. Corrections 5 and 7 need a round 8: repair the two fences to define the constants
they depend on (or build their arms without source slicing), then re-run every fence from a
clean shell and record command, rc, summary and stderr.

Nothing here is a reason to stop — a fence that fails loudly after a real change is the
system working. It is a reason not to call round 7 finished.
