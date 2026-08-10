# RP6-P0 round 8 — repair report (evidence only)

Implementer: Claude (fresh session, 2026-08-11). Role: IMPLEMENTER. Audit tier
unchanged: **T0** (host/execution-domain preflight). Round 8 is an **evidence-only**
round: it repairs the two legacy fences that failed the Lead's round-7 QA
execution and writes **no byte of `RP6-P0.sh`**. No host contact, no network, no
commit. UNIX LF only, zero CR bytes.

Authorised under owner grant #7 (2026-08-10), which lifts the T0 round cap for
this block set. The block remains a draft: not frozen, accepted, dispatchable, or
authorised for host execution.

## Scope and writable surface

Written this round (and nothing else):

- `WPI_BLOCKS_DRAFT/SELF_QA_RP6.md` — the four fence edits + a ROUND 8 section.
- `WPI_BLOCKS_DRAFT/STATUS_RP6_P0.md` — a round-8 status layer.
- `WPI_BLOCKS_DRAFT/RP6_REPAIR_R8_REPORT.md` — this file (new).

**Frozen this round (not written):** `RP6-P0.sh`. The other live-session-owned
files (`RP7-*`, `SELF_QA_RP7.md`, `STATUS_RP7.md`, `transport_runner.ps1`,
`TRANSPORT_*`, `remote_*.sh`, `run_p0.sh`, `run_ro.sh`,
`WPI_PREREGISTRATION_DRAFT.md`, `pathscope_prover.py`, `PATHSCOPE_*`, `SEC101_*`,
`ROWS_1_9_*`) were not written.

## Block identity — UNCHANGED (round-8 confirmation)

Round 8 writes nothing to `RP6-P0.sh`. Re-derived this session by read-only tools
(`sha256sum`, `wc -c`, `tr -cd '\r' … | wc -c`):

```text
sha256   fa852d7e0a984f977a489bd565834c1ced32eab4fd81221388a25a6bad6483cd
bytes    103071
cr_bytes 0
```

These are byte-identical to the round-7 bytes (commit `d9d7420f`,
`RP6_R7_LEAD_QA_EXECUTION_2026-08-10.md`). `bash -n` was not re-run this session
(the session gates `bash`), but no block byte was touched, so the round-7
`bash -n` rc 0 stands. **No belief that the block itself must change arose**; this
round repaired evidence only, as scoped.

## What round 7 left open

The Lead ran every fence by anchored marker after round 7
(`RP6_R7_LEAD_QA_EXECUTION_2026-08-10.md`):

| fence | rc | elapsed | result |
|---|---:|---:|---|
| R7_F2 / R7_F3 / R7_C3 harnesses | 0 | — | PASS (4/4, 4/4, 8/8) |
| `C13_R3_BACKSTOP` | 0 | 1 s | PASS |
| `F2_FREEZE_GATE` | 0 | 0 s | PASS |
| `C13_R4B` | 0 | 9 s | PASS |
| `RP6_FULLBLOCK_D026` | **1** | 7 s | **FAIL** — no summary emitted |
| `RP6_R4_D026` | **1** | 41 s | **FAIL** — `findings=4` |

Both failures share one root cause, in the fences' own arm construction:

```text
…/pin-$$$.sh: line 17: P0_FIXED_STAT: unbound variable   (RP6_R4_D026, build_pin_arm)
…/f4-post.sh: line 15: P0_FIXED_STAT: unbound variable   (RP6_FULLBLOCK_D026, build_f4_arm)
```

`build_f4_arm` and `build_pin_arm` synthesise a test arm by `sed`-slicing
`RP6-P0.sh` between two source landmarks. Correction 7 (round 7) added twelve
frozen `P0_FIXED_*` deploy-channel literals at `RP6-P0.sh:266-299`, which fall
OUTSIDE those slices. The extracted pin loop calls `p0_frozen_tool_path`
(`RP6-P0.sh:535-552`), which reads `$P0_FIXED_STAT` (etc.) under `set -u`; the
literal is unset in the arm, so the arm aborts rc 1.

This session cannot execute `bash` (see QA status), so the analysis is by reading
the source. It localises the defect to exactly the two landmark-slice arms and
surfaces two further consequences the unbound abort had masked.

### Why only the two landmark-slice arms break

Every other arm in both fences extracts whole FUNCTIONS via `exfn`
(`sed -n "/^name() {$/,/^}$/p"`). The functions it extracts — `p0_resolve_tool`,
`p0_assert_execution_domain`, `p0_resolve_accounts`, `p0_resolve_passwd`,
`p0_capture_numeric`, `p0_record_metadata`, `p0_assert_venv_root`,
`p0_assert_interpreter_executable`, `p0_classify_stat_shape`, `p0_probe_kind`,
`p0_assert_evidence_leaf_bound`, `p0_read_domain_ns`, `p0_read_object_device`,
`p0_assert_ns_link_off_root`, `p0_assert_system_manager_ready`, `p0_sanitize`,
`p0_lookup`, `p0_prepare_readlink_detail`, `p0_count_substr` — read ENV inputs
(`P0_ATTESTED_*`, `P0_TOOL_PINS`, `P0_EXPECT_UID`, …) or the `P0_TOOL_PINS` map.
**None reads a `P0_FIXED_*` literal.** The `P0_FIXED_*` literals are referenced
only by top-level code: `p0_frozen_tool_path` and the python3 gate inside the pin
loop, and the top-level execution-domain frozen-pin checks (`:700-718`). So only
the landmark slices that carry that top-level code break. (The FULLBLOCK F3 arm
slices `:492-516`, before the pin section, so it is unaffected; verified by
locating its end anchor `# P0_TOOL_PINS` at `:517`.)

## Repair 1 — arm construction that survives block growth

The fix prescribed by the kickoff's option 2: **define every constant the arm
depends on, and assert at arm-build time that none is missing.**

### `build_f4_arm` (FULLBLOCK, `SELF_QA_RP6.md`)

The F4 arm tests duplicate-pin rejection. It supplies
`P0_TOOL_PINS="stat=/usr/bin/stat stat=/decoy/stat"`. The first `stat` pin reaches
`p0_frozen_tool_path` (`:609`) before the second `stat` pin hits the duplicate
check (`:578`), so the abort is on the first pin.

- The slice is `RP6-P0.sh:528-720` (anchors `P0_TOOL_PINS="${P0_TOOL_PINS:-}"` →
  `# This derives the literal leaf name only`).
- The arm now defines every `P0_FIXED_*` the slice references — the eleven tool
  literals, `P0_FIXED_TRUSTED_PYTHON`, and the five attested literals. Only
  `P0_FIXED_STAT=/usr/bin/stat` is actually reached (the arm STOPs at the second
  stat pin's duplicate check); the rest are inert. The five attested literals are
  present only because the slice text references them (the duplicate arm never
  reaches the execution-domain checks that read them); their value is irrelevant.
- A build-time assertion scans the slice for `P0_FIXED_[A-Z0-9_]+` and fails the
  build LOUDLY (`ARM_BUILD_INCOMPLETE fence=RP6_FULLBLOCK_D026(F4)
  missing_frozen_literal=…`) if any is undefined.

### `build_pin_arm` (R4, `SELF_QA_RP6.md`)

The pin arm drives the real pin validator with a complete pin set.

- The slice is `RP6-P0.sh:528-652` (anchors `P0_TOOL_PINS="${P0_TOOL_PINS:-}"` →
  `# Row 8 deploy-channel attestation inputs`).
- The slice references two outside-defined values: the `P0_FIXED_*` literals
  (via `p0_frozen_tool_path` and the python3 gate) AND `P0_TOOL_COUNT_EXPECTED`
  (the count check at `:634`, also correction 7, derived at `:362-363`). The arm
  now defines the eleven tool `P0_FIXED_*` (values mirror `$RP7PINS`) and mirrors
  the block's own `P0_TOOL_COUNT_EXPECTED` derivation (`P0_TOOL_COUNT_EXPECTED=0;
  for p0_t in $P0_RO_TOOLS; do …; done`) so it tracks the inventory. `P0_FIXED_TRUSTED_PYTHON`
  comes from the existing `trusted` argument.
- The same build-time completeness assertion (scoped to `P0_FIXED_*`).

The assertion is the robustness mechanism: a future round that adds a new
`P0_FIXED_*` reference inside either slice fails the arm build loudly, instead of
emitting a silently-broken arm that aborts rc 1 at run time — the round-7 defect
class, closed one level down.

## Repair 2 — F7_TOOL_POST: classified (block correct, fence fixture stale), fixed

`RP6_FULLBLOCK_D026` also reported `ASSERT_UNMET label=F7_TOOL_POST`. (That
assertion is the line whose `set -e` abort — `require_contains` returning 1 as the
command following the final `&&` — stops the fence before its summary; the F4
unbound one line earlier is a soft-fail, because its `[ "$f4g" -eq 3 ]` is false
and `require_contains` never runs. So "no summary emitted" is the F7_TOOL_POST
abort, and the F4 unbound is the loud stderr the Lead quoted.)

The F7 tool arm resolves `getent` against a non-executable fixture (mode 0644)
and asserts the R2-F1 token `tool_not_evaluable tool=getent path=… rc=na
detail=access_builtin_x_denied mechanism=access_builtin_x`. After correction 7 it
instead emits `tool_pin_unpinned tool=getent detail=every_tool_requires_a_frozen_pin`,
because the arm set `P0_TOOL_PINS=""` and correction 7 DELETED the unpinned
`path_resolved_absolute` fallback (`RP6-P0.sh:807-811`): an unpinned tool now
STOPs BEFORE the `[ -x "$resolved" ]` executability check (`:820-821`) that emits
`tool_not_evaluable`.

**Classification — the block's token is correct; the fence fixture is stale.**
Justified against the preregistered row-1 grammar
(`WPI_PREREGISTRATION_DRAFT.md` §8.1 row 1), which round 7 itself amended:

- Row 1 still carries `tool_not_evaluable tool=getent path=<p> rc=<n|na>
  detail=<d> mechanism=<m>` as the divergence "when the resolved object cannot be
  evaluated as executable", with "`rc=na` is mandatory for the
  `mechanism=access_builtin_x` arm". The token is still intended and the block
  still emits it (`:820-821`) for a PINNED tool that resolves to a non-executable
  path. Correction 7 did NOT change the not-evaluable classification.
- Row 1's round-7 amendment states the unpinned fallback "is deleted, so a tool
  that resolves on PATH but was not pinned is `P0_STOP reason=tool_pin_unpinned
  tool=<t>`". So `tool_pin_unpinned` is the CORRECT token for the arm's old
  fixture; the fixture simply no longer reaches the arm it was written for.

**Fix (fixture only, no block change):** `build_f7_tool_arm` now pins `getent` to
the fixture path (`P0_TOOL_PINS="getent=$Q/nonexec-tool"`), so resolution passes
the pin lookup (`:771`) and reaches `[ -x ]`, where the non-executable fixture
reproduces exactly `tool_not_evaluable … rc=na detail=access_builtin_x_denied
mechanism=access_builtin_x`. The PRE arm is unaffected: the pre-repair resolver
(`RP6-P0.sh@0bbc3591:419`) kept the unpinned fallback, so it reaches `[ -x ]` and
emits `tool_not_executable` whether getent is pinned or not (verified by reading
the pre-repair source — the FULLBLOCK `pre_rev` is `0bbc3591`).

This is not "changing an expectation to make a test pass": the block side is
correct per the prereg grammar, and the fixture is updated to exercise the SAME
preregistered token under correction 7's pin requirement. (The kickoff's
prohibited move would have been to flip the expectation to `tool_pin_unpinned`
without establishing which side is wrong; that is not what was done.)

## Repair 3 — R4 GREEN count: stale under correction 7 (block correct, fence stale), fixed

Once the unbound is fixed, the R4 pin arm's GREEN case reveals a second masked
staleness. `$RP7PINS` supplied ten pins (no `id`, no `getent`) and asserted
`P0_PINS_ACCEPTED count=10`, but correction 7's omission loop (`:628-633`) and
count check (`:634-635`, `expected=12`) require all twelve, so the GREEN case
would STOP at `input_pin_omitted tool=id`. Row 1's round-7 amendment is explicit:
"exactly one frozen pin is required for each of the twelve tools … A missing pin
is `input_pin_omitted …`; a pin count other than twelve is
`input_pin_count_unexpected count=<n> expected=12`." Block correct, fence stale.

**Fix:** `$RP7PINS` now carries the full twelve-tool set (`id=/usr/bin/id
getent=/usr/bin/getent` appended; order is irrelevant — the omission loop tests
presence, not sequence) and the GREEN assertion reads `count=12`. The other five
pin cases are unaffected: the RED pre case still STOPs at `timeout` (before
`id`/`getent`); the FREEZE case still STOPs at `python3` (before `id`/`getent`);
the WRONGPY / GREP / REGRESSION cases supply their own pin sets, not `$RP7PINS`.
The build_pin_arm `P0_FIXED_*` values mirror the new `$RP7PINS`.

## Disposition summary

| item | side wrong | action | evidence |
|---|---|---|---|
| `build_f4_arm` unbound `P0_FIXED_STAT` | fence (slice excluded correction-7 literals) | define `P0_FIXED_*` + build-time assertion | `SELF_QA_RP6.md` FULLBLOCK § |
| `build_pin_arm` unbound `P0_FIXED_*` + `P0_TOOL_COUNT_EXPECTED` | fence (same) | define both + build-time assertion | `SELF_QA_RP6.md` R4 § |
| `F7_TOOL_POST` ASSERT_UNMET | fence (fixture stale vs correction 7) | pin `getent` in `build_f7_tool_arm` | justified vs prereg §8.1 row 1 |
| R4 GREEN `count=10` | fence (stale vs correction 7) | `$RP7PINS` 12 pins + `count=12` | justified vs prereg §8.1 row 1 |
| `RP6-P0.sh` | — | **unchanged** | SHA-256/bytes re-derived above |

## QA execution status — PENDING-LEAD-EXECUTION (no fabricated transcripts)

This session gates the `bash` interpreter: every `bash <script>`, `bash -n`,
`bash -c` and `sed … | bash` returned *requires approval* and was not approved —
the same blocker the round-7 Claude and GLM sessions recorded. Per the kickoff's
PENDING-LEAD-EXECUTION clause and AGENTS.md D026, the round-8 re-run is recorded
PENDING, not fabricated. No transcript in `SELF_QA_RP6.md` was invented; the
existing FULLBLOCK/R4 transcripts are explicitly labelled as the **round-6**
captures (they predate correction 7 and still read `count=10`), retained as the
shape the round-8 repair restores.

The Lead must, in an unhindered Git Bash against the unchanged round-7 bytes,
re-run the two repaired fences by anchored marker and record, per fence, the exact
command, its rc, its summary line and its stderr:

```text
sed -n '/^# RP6_FULLBLOCK_D026_HARNESS_BEGIN$/,/^# RP6_FULLBLOCK_D026_HARNESS_END$/p' SELF_QA_RP6.md | bash --noprofile --norc
sed -n '/^# RP6_R4_D026_HARNESS_BEGIN$/,/^# RP6_R4_D026_HARNESS_END$/p' SELF_QA_RP6.md | bash --noprofile --norc
```

Expected (round 8), by static analysis:

- `RP6_FULLBLOCK_D026` — rc 0, `RP6_FULLBLOCK_D026_SUMMARY findings=7 …
  result=PASS`. F4 POST → `P0_STOP reason=prereg_input_malformed name=P0_TOOL_PINS
  duplicate=stat` at rc 3 (no longer an unbound abort). F7_TOOL_POST →
  `P0_STOP reason=tool_not_evaluable tool=getent path=… rc=na
  detail=access_builtin_x_denied mechanism=access_builtin_x` at rc 3. Neither arm
  build prints `ARM_BUILD_INCOMPLETE`.
- `RP6_R4_D026` — rc 0, `RP6_R4_D026_SUMMARY findings=4
  pth_forge=real_venv manager_bound=real_timeout inventory_basis=23e55667@d6a976aa
  result=PASS`. GREEN → `P0_PINS_ACCEPTED count=12 trusted_python_pin=yes`.
  Confirm it still returns within its ~41 s bound (the R6 "open descendant handle"
  concern, which the Lead already observed closed at 41 s in round 7).

If a re-run does not match, the most likely causes (in order) are: (a) a typo in
the new `P0_FIXED_*` literal list vs the slice's actual references — the build-time
assertion prints exactly which literal is missing; (b) the F7 fixture's `command`
override interacting with the pin — re-check that `command -v getent` returns the
same path the pin names; (c) a value mismatch between `$RP7PINS` and the pin arm's
`P0_FIXED_*`. None of these would be a block defect; all are fixture-side.

## Files touched / not touched; explicit non-actions

- **Touched:** `SELF_QA_RP6.md`, `STATUS_RP6_P0.md`, `RP6_REPAIR_R8_REPORT.md`
  (new). Three files, all in the writable set.
- **Not touched:** `RP6-P0.sh` (frozen, re-verified above) and every
  live-session-owned file listed in the kickoff.
- **Not done:** no `bash` execution, no `bash -n`, no host contact, no network,
  no commit, no fabrication of transcripts.

The block's acceptance still requires fresh independent `claude-opus-5` xhigh and
`gpt-5.6-sol` xhigh verdicts at T0; this round produces no block change for them
to audit, only the evidence a Lead re-run must confirm before the two repaired
fences count as closure for corrections 5 and 7.
