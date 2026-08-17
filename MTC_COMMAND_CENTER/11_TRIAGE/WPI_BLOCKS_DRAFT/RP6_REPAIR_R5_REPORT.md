# RP6-P0 round-5 repair report — three Codex final-audit findings (F1–F3)

Date: 2026-08-10
Implementer: GLM-5.2 (fresh session)
Auditor of this block: Codex `gpt-5.6-sol`, `xhigh` (final-audit
`RP6_CODEX_FINAL_AUDIT_2026-08-10.md`). GLM-5.2 did not audit this block, so
implementer/auditor separation holds.
Tier: **T0** — defensive staging preflight / host execution-domain surface.
Authority: DRAFT. Not frozen, not hashed into any kit, not dispatchable, carrying
NO host-contact authority. No host, SSH, network, deployment, broker, backtest,
Pine, parity, MTC, or trading action was performed. No commit was made.

## Inputs

- `RP6_CODEX_FINAL_AUDIT_2026-08-10.md` — findings F1–F3 with executed
  falsifications and "Required repair" text. That text BINDS.
- `RP6-P0.sh` — target. Baseline (verified BEFORE the first edit):
  SHA-256 `e93d07adcc9ae03ad15e0b0f10c76be54517251ab461c8fe789d160072d253c6`,
  85540 B, commit `945e20f5`.
- `KICKOFF_RP6_REPAIR_R5.md` — the bounded round-5 contract.
- `DESIGN_DEFECT_PATTERNS_2026-08-10.md` — binding pre-read.

## Artefact (real, computed in-session by read-only tools)

- Repaired `RP6-P0.sh` SHA-256:
  `490e3e4edfec811dee3dc90c6693e8ebeb865eb946a431ff017de58e66f0ce5f`
- Repaired `RP6-P0.sh` byte count: `89029` (was `85540`; +3489 B = the three
  gates plus their comments). LF-only, no BOM; the edits introduced no CR.
- `bash -n RP6-P0.sh`: **PENDING** — the GLM-5.2 session gates `bash -n` and
  script execution (identical to the C13 GLM-5.2 round's recorded blocker).
- The three edits are grep-confirmed at their expected sites; no other arm was
  changed. `shellcheck` is not installed and was not run.

## The three fixes

### F1 (HIGH) — the python3 freeze gate was optional when the `python3` pin was omitted

**Root cause.** `P0_TOOL_PINS` is optional. The only check of
`P0_FIXED_TRUSTED_PYTHON` sat inside `if [ "$p0_pin_name" = python3 ]` in the
pin-parse loop, so supplying a `python3` pin ENGAGED the check while OMITTING it
left `P0_TRUSTED_PYTHON_BOUND=no` and skipped the check entirely. The polarity
was backwards: the security-relevant pin engaged the gate; omitting it disabled
the gate. After the other five placeholders are filled, this sixth
`<PIN-AT-FREEZE>` literal would not be load-bearing. (Auditor falsification:
`PIN_NONE rc=0`, `PIN_NO_PYTHON rc=0`, `PIN_WITH_PYTHON rc=3` only because the
placeholder was still unfilled.)

**Repair.** Immediately after the pin-parse loop (repaired bytes ~line 523), add:

```bash
[ "$P0_TRUSTED_PYTHON_BOUND" = yes ] \
    || p0_stop "input_pin_freeze_unfilled tool=python3 name=P0_FIXED_TRUSTED_PYTHON detail=trusted_python_pin_omitted_freeze_gate_load_bearing"
```

The `detail=` distinguishes omission (this post-loop gate) from a still-unfilled
deploy-channel placeholder (the in-loop gate, `detail=deploy_channel_value_never_derived_here`,
unchanged). Both are rc 3 under the same freeze-gate reason. Now every
missing-python3 prelude STOPs the same way; the complete pin set (with the
deploy-channel value filled) stays GREEN.

**Evidence (D026, PENDING execution).** `SELF_QA_RP6.md` §R5-F1 harness drives
the auditor's exact three fixtures for both variants (the D026 mutation is
"delete the post-loop gate"): `PIN_NONE`/`PIN_NO_PYTHON` go `rc=0` (omit
admitted) on pre-fix bytes and `rc=3` (omission STOP) on repaired bytes;
`PIN_WITH_PYTHON` with the freeze filled stays `rc=0`; with the placeholder
still unfilled the in-loop gate still fires `rc=3`.

### F2 (MEDIUM) — PATH executables were accepted and reported as sourced RP0 functions

**Root cause.** The prerequisite checks used `command -v`, which only proves a
name resolves — it accepts an executable file (or alias) from PATH, not just a
sourced function. The block then CALLED the first symbol, so a PATH-shadow file
of the right name satisfied the "RP0-LIB sourced" claim and ran arbitrary child
behaviour before P0 had established any tool premise. (Auditor falsification: two
executable files of those names first in PATH; `P0_prereq lib=sourced
bootstrap=ran` printed and the first file wrote a marker.)

**Repair.** Replace both `command -v <symbol>` checks with an exact builtin type
assertion (repaired bytes ~lines 342–345):

```bash
[ "$(type -t rp0_require_safe_component 2>/dev/null)" = function ] \
    || p0_stop "rp0_lib_not_sourced predicate=rp0_require_safe_component detail=not_a_shell_function"
[ "$(type -t rp0_allocate_evidence_dir 2>/dev/null)" = function ] \
    || p0_stop "rp0_lib_not_sourced predicate=rp0_allocate_evidence_dir detail=not_a_shell_function"
```

`type -t` returns `function` only for a sourced shell function; a PATH file
returns `file`, an alias returns `alias`, and a missing name returns nothing —
all fail the `= function` test and STOP before either symbol is called. A
genuinely sourced function still resolves to `function`. (`command -v` remains
correct inside `p0_resolve_tool`, where the intent IS to resolve a PATH tool to
an absolute path; that site is unchanged.)

**Evidence (D026, PENDING execution).** `SELF_QA_RP6.md` §R5-F2 harness installs
PATH-shadow executable files of both names (no functions defined) and detects
execution via an on-disk marker: on pre-fix bytes the shadow is accepted (`rc=0`)
AND the file executes (marker written); on repaired bytes it is rejected at
`rc=3` (`not_a_shell_function`) and the marker is ABSENT (rejected and never
run). A second case defines genuine functions (with the shadow files still
present but shadowed) and confirms `type -t` returns `function` and the check
passes on both variants.

### F3 (MEDIUM) — malformed forbidden-GID input was pathname-expanded and could be admitted

**Root cause.** The raw `P0_FORBIDDEN_GIDS` value was never grammar-checked
before the unquoted split `for p0_g in $P0_FORBIDDEN_GIDS`; Bash therefore
pathname-expanded it before `p0_require_uint` saw each item. With
`P0_FORBIDDEN_GIDS='*'` and a cwd holding entries named `0` and `988`, the
wildcard expanded to those two numeric names and the malformed ledger was
admitted (`count=2`); the same input in an empty cwd STOPped. So cwd contents
rewrote the ledger. The capability intersection loop later in the block repeated
the same unquoted expansion.

**Repair.** Two independent defenses at the input gate (repaired bytes
~lines 418–428):

```bash
case "$P0_FORBIDDEN_GIDS" in
    *[!0-9[:space:]]*)
        p0_stop "input_charset name=P0_FORBIDDEN_GIDS value=[$P0_FORBIDDEN_GIDS] expected=decimal_digits_and_separators_only" ;;
esac
...
set -f
for p0_g in $P0_FORBIDDEN_GIDS; do
    p0_require_uint P0_FORBIDDEN_GIDS_ENTRY "$p0_g" 0
    P0_FORBIDDEN_GID_COUNT=$(( P0_FORBIDDEN_GID_COUNT + 1 ))
done
set +f
```

(1) validate the COMPLETE raw value against an exact digits-plus-separator
grammar BEFORE any expansion, so a wildcard or any non-digit/non-space byte is a
STOP regardless of cwd; (2) split with pathname expansion disabled (`set -f`) so
no surviving metacharacter can ever reach the per-item check. The secondary
capability-intersection loop (~lines 891–897) is wrapped in `set -f`/`set +f`
too as defense in depth, although the upstream grammar gate already guarantees
the value is digits-plus-separators by the time it runs. `set -f`/`set +f`
toggle only the glob flag and leave the block's `-Eeuo pipefail` intact; on the
in-loop STOP path `p0_stop` exits the shell, so re-enabling is unreachable and
irrelevant there.

**Evidence (D026, PENDING execution).** `SELF_QA_RP6.md` §R5-F3 harness drives
the auditor's wildcard fixture in BOTH an empty cwd and a cwd containing entries
named `0` and `988`: on pre-fix bytes `*` is admitted (`count=2`) in the numeric
cwd but STOPs in the empty cwd (the cwd-dependence IS the defect); on repaired
bytes `*` STOPs via the grammar gate (`decimal_digits_and_separators_only`)
IDENTICALLY in both cwds, and a valid `0 988` list is still admitted (`count=2`,
no regression).

## What is preserved

- rc 0/1/3 contract, STOP-vs-FAIL truthfulness, numeric-only identity,
  read-only scope, and every pre-existing arm are unchanged. The six edits are
  strictly additive at three sites; no existing STOP/FAIL token was altered.
- The freeze gate still has exactly six `<PIN-AT-FREEZE>` literals; F1 makes the
  sixth (`P0_FIXED_TRUSTED_PYTHON`) load-bearing by construction rather than by
  operator choice — the count is unchanged.
- `P0_FORBIDDEN_GIDS` is still emitted on `P0_input`/`P0_tool_inventory` lines
  via quoted expansion (those sites were never vulnerable); only the two unquoted
  split loops changed.
- The `P0_TRUSTED_PYTHON_BOUND` inventory print now always shows `yes` at that
  point (a `no` would have STOPped at the new gate), which is more truthful, not
  less.

## QA execution status: PENDING (Lead to execute)

The GLM-5.2 session gates `bash -n` and script execution. Per the kickoff
(lines 51–53), this is reported rather than papered over with fabricated output.
The Lead must run, in an unhindered Git Bash:

```text
bash -n MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6-P0.sh
sed -n '/R5_F1_HARNESS_BEGIN/,/R5_F1_HARNESS_END/p' SELF_QA_RP6.md | bash --noprofile --norc
sed -n '/R5_F2_HARNESS_BEGIN/,/R5_F2_HARNESS_END/p' SELF_QA_RP6.md | bash --noprofile --norc
sed -n '/R5_F3_HARNESS_BEGIN/,/R5_F3_HARNESS_END/p' SELF_QA_RP6.md | bash --noprofile --norc
# plus the five prior mandated fences, re-run against the round-5 bytes:
sed -n '952,1035p'   SELF_QA_RP6.md | bash --noprofile --norc   # backstop, 4 cases
sed -n '1678,2068p'  SELF_QA_RP6.md | bash --noprofile --norc   # full-block D026, 39 assertions
sed -n '2286,2319p'  SELF_QA_RP6.md | bash --noprofile --norc   # freeze-literal gate
sed -n '2545,2989p'  SELF_QA_RP6.md | bash --noprofile --norc   # R4 D026, 102 assertions
sed -n '3353,3518p'  SELF_QA_RP6.md | bash --noprofile --norc   # R4b C13 arm, 27 cases
```

Expected (design intent): each R5 harness prints
`R5_FX_QA_SUMMARY cases=N pass=N fail=0 result=PASS`; the three auditor fixtures
flip polarity as tabulated in `SELF_QA_RP6.md` §R5. The five prior fences should
remain green (no changed arm touches their assertions); the full-block and R4
D026 fences also re-grep the prereg draft, which this round did not edit.

## Scope

Four files touched only — `RP6-P0.sh`, `SELF_QA_RP6.md`, `STATUS_RP6_P0.md`, and
this file. Nothing committed. No host contacted, no network command run, no host
file content printed. The block remains draft: not frozen, not accepted, not
dispatchable, and not authorised for host execution.
