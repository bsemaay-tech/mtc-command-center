# KICKOFF — RP6-P0 round 8: repair the two failing legacy fences (evidence only)

You are the IMPLEMENTER. Narrow round. Working dir `C:\LAB\Tradingview_LAB_CLEAN`.
No host contact, no network, no commit. UNIX LF only, zero CR bytes.

**Do not modify `RP6-P0.sh`.** Its round-7 bytes are
`fa852d7e0a984f977a489bd565834c1ced32eab4fd81221388a25a6bad6483cd`, 103071 B, commit
`d9d7420f`, and they must come out of this round byte-identical. This round repairs
**evidence only**. If you believe the block itself must change, say so in the report and
stop rather than changing it.

If your session cannot execute commands, write the repairs and mark QA
`PENDING-LEAD-EXECUTION`. Do not fabricate transcripts.

## What happened

The Lead ran every fence by anchored marker after round 7. Record:
`RP6_R7_LEAD_QA_EXECUTION_2026-08-10.md`. Three round-7 harnesses PASS (4/4, 4/4, 8/8).
`C13_R3_BACKSTOP`, `F2_FREEZE_GATE` and `C13_R4B` PASS. Two fail:

```text
RP6_FULLBLOCK_D026   rc 1, 7 s,  no summary emitted
RP6_R4_D026          rc 1, 41 s, findings=4
```

Both from the same cause, in the fences themselves:

```text
/tmp/.../pin-3487.sh: line 17: P0_FIXED_STAT: unbound variable
/tmp/.../f4-post.sh:  line 15: P0_FIXED_STAT: unbound variable
```

These fences synthesise a test arm by `sed`-slicing `RP6-P0.sh` between two source
landmarks. Round 7 added ten frozen `P0_FIXED_*` constants — `P0_FIXED_STAT` is at
`RP6-P0.sh:289` — which fall outside those slices. The arm references a constant it never
defines, `set -u` aborts it, and it exits **rc 1**.

## Writable file list (write nothing else)

- `WPI_BLOCKS_DRAFT/SELF_QA_RP6.md`
- `WPI_BLOCKS_DRAFT/STATUS_RP6_P0.md`
- `WPI_BLOCKS_DRAFT/RP6_REPAIR_R8_REPORT.md` (new)

**Owned by other live sessions — never write them:** `RP6-P0.sh` (frozen this round),
`RP7-*`, `SELF_QA_RP7.md`, `STATUS_RP7.md`, `transport_runner.ps1`, `TRANSPORT_*`,
`remote_*.sh`, `run_p0.sh`, `run_ro.sh`, `WPI_PREREGISTRATION_DRAFT.md`,
`pathscope_prover.py`, `PATHSCOPE_*`, `SEC101_*`, `ROWS_1_9_*`.

## The two repairs

1. **Make each fence's arm construction survive block growth.** A fence that slices the
   block by source landmarks breaks every time the block grows — which is the same defect
   correction 5 was written to remove, one level down. Anchored extraction of the *fence*
   does not help if the *fence* then line-slices the *block*. Fix it properly: either have
   the arm source the whole block with the entry point suppressed (the pattern the round-7
   harnesses and the Codex fixtures use successfully — `source <(sed '/^p0_main "$@"$/d' …)`
   or the block's equivalent), or define every constant the arm depends on explicitly and
   assert at arm-build time that none is missing. Do **not** simply widen the slice by hand;
   that just moves the next break.
2. **Then re-run every fence from a clean shell** and record, per fence, the exact anchored
   command, its rc, its summary line and its stderr. `RP6_R4_D026` now returns in 41 s,
   inside its bound — confirm that holds.

## One item you must NOT silently resolve

`RP6_FULLBLOCK_D026` also reports:

```text
ASSERT_UNMET label=F7_TOOL_POST
  token=[tool_not_evaluable tool=getent path=/tmp/.../nonexec-tool rc=na
         detail=access_builtin_x_denied mechanism=access_builtin_x]
```

Round 7 changed tool resolution (twelve mandatory exact pins, unpinned fallback deleted),
so this path may legitimately report differently now. Determine which it is and **state your
reasoning explicitly**: either the block's new token is correct and the fence's expectation
is stale — in which case update the expectation and justify it against the preregistered
row-1 grammar in `WPI_PREREGISTRATION_DRAFT.md` — or the round-7 repair changed a
not-evaluable classification it should not have, in which case **do not fix it here**;
report it as a block defect for round 9. Changing an expectation to make a test pass,
without establishing which side is wrong, is the one thing this round must not do.

## Deliverables

Updated `SELF_QA_RP6.md` (all fences passing, or a truthful record of any that still do not)
+ `STATUS_RP6_P0.md` + `RP6_REPAIR_R8_REPORT.md`. Confirm `RP6-P0.sh` is unchanged by
re-deriving its SHA-256 and byte count and quoting them. State the disposition of both
repairs and of the `F7_TOOL_POST` question explicitly.
