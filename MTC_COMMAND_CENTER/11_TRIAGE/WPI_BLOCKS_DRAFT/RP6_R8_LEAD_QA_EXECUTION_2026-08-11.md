# Lead QA execution — RP6-P0 round 8, and one real defect it surfaced

GLM's session gates command execution, so round 8 wrote the repairs and marked QA
`PENDING-LEAD-EXECUTION`. The Lead ran the two fences. Git Bash, clean shell, `</dev/null`,
`timeout 240` per fence.

`RP6-P0.sh` is **unchanged** at SHA-256
`fa852d7e0a984f977a489bd565834c1ced32eab4fd81221388a25a6bad6483cd`, 103071 B, as round 8
required. Round 8 touched evidence only.

## Result

| Fence | Before round 8 | After round 8 |
|---|---|---|
| `RP6_FULLBLOCK_D026` | rc 1, aborted on `P0_FIXED_STAT: unbound variable`, no summary | **rc 0**, `findings=7 round3_residuals=3 real_lstat_arms=2 execution_domain_cases=9 readlink_stop_arms=3 result=PASS`, 10 s |
| `RP6_R4_D026` | rc 1, two unmet asserts, both from the same unbound variable | rc 1, 44 s, **one** unmet assert — and it is a genuine block defect, see below |

The arm-construction defect is fixed. Both fences now build arms that survive the block
growing, which is what correction 5 asked for. `RP6_FULLBLOCK_D026` is fully closed.

Round 8 also self-caught a bug before finalising: the inert attested literals it added to
`build_f4_arm` were initially unquoted `<PIN-AT-FREEZE>`, which Bash parses as redirections
and which would have aborted the arm. It single-quoted them, matching the block's own
convention at `RP6-P0.sh:289`. Worth recording — that class of bug is invisible until the
arm runs.

## The defect the surviving assert exposes — grammar drift at `RP6-P0.sh:612`

The `PIN_GREEN` case now passes: `P0_PINS_ACCEPTED count=12 trusted_python_pin=yes`, rc 0.
The freeze case STOPs at rc 3 as it should. But the line it prints does not match the
preregistered grammar:

```text
emitted   P0_STOP reason=input_pin_freeze_unfilled tool=python3 detail=deploy_channel_value_never_derived_here
declared  P0_STOP reason=input_pin_freeze_unfilled tool=python3 name=P0_FIXED_TRUSTED_PYTHON detail=deploy_channel_value_never_derived_here
```

The `name=` field is missing. `WPI_PREREGISTRATION_DRAFT.md` row 1 declares exactly one form
for this STOP, and it carries `name=P0_FIXED_TRUSTED_PYTHON`.

There are two emit sites, and they disagree with each other as well as with the draft:

- `RP6-P0.sh:612` — `p0_stop "input_pin_freeze_unfilled tool=$p0_pin_name detail=deploy_channel_value_never_derived_here"`. Round 7 generalised this site over the twelve-pin table, and in
  becoming generic it dropped the constant `name=` field.
- `RP6-P0.sh:651` — `p0_stop "input_pin_freeze_unfilled tool=python3 name=P0_FIXED_TRUSTED_PYTHON detail=trusted_python_pin_omitted_freeze_gate_load_bearing"`. This one keeps `name=` but uses a
  `detail=` value the draft does not declare.

So one reason token is emitted in two shapes, neither of which is the declared shape. This is
a **block defect, not a stale expectation** — the fence's expectation is quoted verbatim from
the preregistration.

**Disposition: round 9 scope.** Round 8 was correctly forbidden from touching the block, and
correctly did not. The fix is small — every emit site must carry the `name=` of the frozen
constant it is talking about, and every `detail=` value must be one the draft declares — but
it is a block change, so `RP6-P0.sh` unfreezes for round 9 and the resulting bytes need a
fresh T0 review.

## Why this is a good outcome

The round-7 correction that generalised the pin table was right. The grammar drift it
introduced was invisible in review and invisible to a fence that could not run. It surfaced
only because round 8 repaired the fence's arm construction and the Lead then ran it. That is
the evidence contract doing precisely the job two rounds were spent giving it.
