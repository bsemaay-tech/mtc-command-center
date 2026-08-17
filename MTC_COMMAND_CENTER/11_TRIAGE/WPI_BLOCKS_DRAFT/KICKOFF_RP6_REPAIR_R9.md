# KICKOFF — RP6-P0 round 9: one grammar drift, two emit sites

You are the IMPLEMENTER. Narrow round. Codex is the auditor of record and re-audits your
bytes. Working dir `C:\LAB\Tradingview_LAB_CLEAN`. No host contact, no network, no commit.
UNIX LF only, zero CR bytes. Never `git checkout` a block file — use
`git cat-file blob <sha>:<path> > <path>`.

If your session cannot execute commands, write the repair and the arms, mark QA
`PENDING-LEAD-EXECUTION`, and the Lead will run them. Do not fabricate transcripts. That has
worked well for two rounds running.

## Input bytes

`WPI_BLOCKS_DRAFT/RP6-P0.sh`: SHA-256
`fa852d7e0a984f977a489bd565834c1ced32eab4fd81221388a25a6bad6483cd`, 103071 B, commit
`a01cb018`. The block **unfreezes for this round** — round 8 was evidence-only and correctly
left it untouched.

## The defect

Evidence: `RP6_R8_LEAD_QA_EXECUTION_2026-08-11.md`. The Lead ran the repaired
`RP6_R4_D026` fence; its one remaining unmet assert is a genuine block defect.

One reason token is emitted in two shapes, and **neither matches the preregistered shape**:

```text
:612   p0_stop "input_pin_freeze_unfilled tool=$p0_pin_name detail=deploy_channel_value_never_derived_here"
:651   p0_stop "input_pin_freeze_unfilled tool=python3 name=P0_FIXED_TRUSTED_PYTHON detail=trusted_python_pin_omitted_freeze_gate_load_bearing"

draft  P0_STOP reason=input_pin_freeze_unfilled tool=python3 name=P0_FIXED_TRUSTED_PYTHON detail=deploy_channel_value_never_derived_here
```

`:612` lost the `name=` field when round 7 generalised that site over the twelve-pin table.
`:651` keeps `name=` but emits a `detail=` value the draft does not declare.
`WPI_PREREGISTRATION_DRAFT.md` row 1 declares exactly one form.

## The repair

Every emit site must carry the `name=` of the frozen constant it is actually talking about,
and every `detail=` value must be one the draft declares. Since `:612` is now generic over
twelve tools, `name=` must resolve to that tool's own frozen constant
(`P0_FIXED_STAT`, `P0_FIXED_READLINK`, … `P0_FIXED_TRUSTED_PYTHON`) rather than being
hard-coded.

Then decide, and justify, one of two closures — do not do both silently:

- **Either** the two sites are genuinely distinct conditions, in which case the draft must
  declare both, with a distinct `detail=` for each and a sentence saying when each fires;
- **or** they are the same condition reached twice, in which case they must emit the same
  line and one site should probably call the other.

Say which, and why, in the report. A grammar that exists in two shapes because nobody
noticed is not a design.

## Sweep the rest

This defect was invisible to review three times and surfaced only when an executable fence
was finally able to run. **Assume it is not the only one.** Enumerate every `p0_stop` /
`p0_fail` emit site in the block, and compare each against the reason grammar the draft
declares. Report any other site whose emitted fields differ from the declared form — field
present that is not declared, declared field absent, or a `detail=` value the draft never
names. Fix the ones that are clearly the block's error; report the ones where the draft
looks wrong instead, and do not change the draft to match the code without saying so
explicitly.

## Writable file list

- `WPI_BLOCKS_DRAFT/RP6-P0.sh`
- `WPI_BLOCKS_DRAFT/SELF_QA_RP6.md`
- `WPI_BLOCKS_DRAFT/STATUS_RP6_P0.md`
- `WPI_BLOCKS_DRAFT/RP6_REPAIR_R9_REPORT.md` (new)
- `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` — narrow, only if the adjudication
  above requires it, and list every edit

**Owned by other sessions — never write:** `RP7-*`, `SELF_QA_RP7.md`, `STATUS_RP7.md`,
`transport_runner.ps1`, `TRANSPORT_*`, `remote_*.sh`, `run_p0.sh`, `run_ro.sh`,
`pathscope_prover.py`, `PATHSCOPE_*`, `SEC101_*`, `SEC102_*`, `ROWS_1_9_*`, `RUNID_*`.

## Deliverables

Repaired `RP6-P0.sh` + `SELF_QA_RP6.md` with a RED/GREEN arm proving the emitted line now
matches the declared grammar exactly (and that the previously passing fences still pass) +
`STATUS_RP6_P0.md` + `RP6_REPAIR_R9_REPORT.md` with the emit-site sweep table. `bash -n`
rc 0; re-derive SHA-256 and byte count; zero CR bytes via `tr -cd '\r' < file | wc -c`.
