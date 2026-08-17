# Lead QA execution — RP6-P0 round 9a (partial), and the first all-green fence set

## What happened

GLM was dispatched for round 9 at ~03:20 and hit its 5-hour window limit mid-run
(`reset at 2026-08-11 12:12:42` CST = 07:12 local). It left `RP6-P0.sh` **modified but
unfinished**: no report, no QA update, no status update, and the two-emit-site adjudication
not performed.

This is the "agents crash mid-write" trap the handoff warns about. The Lead did not commit
the fragment on trust and did not discard it on suspicion. It was **executed**.

## What the fragment contains

A coherent, complete fix for the grammar drift, and nothing else:

- `p0_frozen_pin_for` now also sets `P0_FROZEN_CONST_NAME` alongside `P0_FROZEN_PIN`, for all
  twelve tools.
- `RP6-P0.sh:616` now emits
  `input_pin_freeze_unfilled tool=$p0_pin_name name=$P0_FROZEN_CONST_NAME detail=deploy_channel_value_never_derived_here`,
  so a generic site carries the `name=` of the constant it is actually talking about.

`+18/−14` lines. `bash -n` rc 0.

## Lead execution — the whole fence set, clean Git Bash, `</dev/null`, `timeout 240` each

| Fence | rc | Summary |
|---|---:|---|
| `RP6_R4_D026` | 0 | `findings=4 pth_forge=real_venv manager_bound=real_timeout inventory_basis=23e55667@d6a976aa result=PASS` |
| `RP6_FULLBLOCK_D026` | 0 | PASS |
| `R7_F2` | 0 | `cases=4 pass=4 fail=0 result=PASS` |
| `R7_F3` | 0 | `cases=4 pass=4 fail=0 result=PASS` |
| `R7_C3` | 0 | `cases=8 pass=8 fail=0 result=PASS` |
| `C13_R3_BACKSTOP` | 0 | PASS |
| `F2_FREEZE_GATE` | 0 | `placeholder_rc=3 filled_fixture_rc=0 result=PASS` |
| `C13_R4B` | 0 | `cases=27 result=PASS` |

The previously failing assert now reads:

```text
ASSERT_MET label=PIN_FREEZE_EXACT exact_line=[P0_STOP reason=input_pin_freeze_unfilled
  tool=python3 name=P0_FIXED_TRUSTED_PYTHON detail=deploy_channel_value_never_derived_here]
```

which is the preregistered form, character for character.

**This is the first time RP6-P0's complete fence set has been green in one run.** Eight
fences, rc 0 each, on bytes
`e7ca9ff1e6d44b838b6d8bfddbb24bb68e2642b9f65abfc941f9482e465a0839`, 103808 B, zero CR bytes.

## Why it is committed as 9a rather than as round 9

Three parts of the round-9 kickoff were not done, and none of them is optional:

1. **The `:655` adjudication.** That site still emits
   `detail=trusted_python_pin_omitted_freeze_gate_load_bearing`, which the draft does not
   declare. The kickoff required a decision — either the two sites are distinct conditions
   and the draft declares both, or they are one condition and must emit one line. The
   fragment did neither, so one reason token still has two shapes.
2. **The emit-site sweep.** The whole point of round 9 was that this drift survived three
   reviews, so every `p0_stop` / `p0_fail` site must be compared against the declared
   grammar. Not started.
3. Report, self-QA section and status layer.

**Round 9b resumes at 07:12** when GLM's window returns, with items 1–3 as its scope and this
record as its starting evidence. The block is committed in its improved state because the fix
is verified and reverting would discard a repair proven to work — but the round is not closed
and must not be presented as closed.
