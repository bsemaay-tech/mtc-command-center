# RP6-P0 round-7 repair report — five Codex round-6 audit required corrections

Date: 2026-08-10
Implementer: Claude (fresh session).
Auditor of this block: Codex (`gpt-5.6-sol`, xhigh) is the auditor of record for
these corrections (`RP6_CODEX_AUDIT_R6_2026-08-10.md`, REQUEST_CHANGES, rows
A4/A8/A9/A10/A11), so implementer/auditor separation holds.
Tier: **T0** — defensive staging preflight / host execution-domain surface.
Authority: owner grant #7 (2026-08-10) lifts the T0 round cap for this block set
— rounds continue until both flagships accept; the acceptance standard is
unchanged. DRAFT. Not frozen, not hashed into any kit, not dispatchable, carrying
NO host-contact authority. No host, SSH, network, deployment, broker, backtest,
Pine, parity, MTC, or trading action was performed. No commit was made.

## Inputs

- `RP6_CODEX_AUDIT_R6_2026-08-10.md` — REQUEST_CHANGES, five required corrections
  (rows A4, A8, A9, A10, A11) with executed falsifications. That text BINDS.
- `RP6-P0.sh` — target. Baseline (verified BEFORE the first edit): SHA-256
  `75db028e76438bc88caba19b9c3b6411e5f573f7b6c2bd13c3883d24e4389570`, 93421 B,
  commit `8fcab4d4`.
- `SELF_QA_RP6.md`, `STATUS_RP6_P0.md`, `RP6_REPAIR_R6_REPORT.md`,
  `RP6_REPAIR_R4_REPORT.md`.
- `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` — edited narrowly
  (two §8.1 rows: row 1 for correction 7, row 9 for correction 4d).
- `DESIGN_DEFECT_PATTERNS_2026-08-10.md` — binding pre-read (patterns 1, 5, 6,
  9, 10).

## Artefact (identity real; `bash -n` PENDING-LEAD-EXECUTION)

- Repaired `RP6-P0.sh` SHA-256: `fa852d7e0a984f977a489bd565834c1ced32eab4fd81221388a25a6bad6483cd`
  (computed in-session via `sha256sum < RP6-P0.sh`; the path-arg form is sandbox-
  blocked, the stdin-redirect form runs).
- Repaired `RP6-P0.sh` byte count: `103071` (was `93421`; +9650 B — the eleven
  freeze literals and their comment, the `p0_frozen_tool_path` helper, the
  per-tool frozen binding + omission/count gates, the caller-noglob wrapper, the
  C3 shape-adjudication blocks, and the C4 comment/token changes).
- CR bytes: `tr -cd '\r' < RP6-P0.sh | wc -c` → `0`; every edit is LF-only by
  construction. LF-only, no BOM.
- `bash -n RP6-P0.sh`: **PENDING-LEAD-EXECUTION** — this session gates
  `bash -n`/`bash -c` (execution approval). The Lead must run it in an unhindered
  Git Bash and record the rc.
- Baseline before the first edit: SHA-256
  `75db028e76438bc88caba19b9c3b6411e5f573f7b6c2bd13c3883d24e4389570`, 93421 B.
- The freeze-gate literal count changes from **six** to **seventeen**: the five
  namespace/root literals, `P0_FIXED_TRUSTED_PYTHON`, and the eleven new per-tool
  path literals added by correction 7. No end-to-end `P0 PASS` is possible until
  all seventeen deploy-channel values are filled.

## The five corrections

### C1 / A4 — R5-F2 prerequisite check: real builtin + honest claim

**Root cause.** The two prerequisite guards used the overridable `type -t`, so a
caller-defined `type(){ printf 'function\n'; }` forged `function` for both
symbols; the missing real `rp0_require_safe_component` then fell through to
`command_not_found_handle` and the case ended `PREREQ_GATE_ACCEPTED` (Codex
falsification). Separately, the comment and `P0_prereq lib=sourced` claimed
RP0-LIB provenance that function type cannot establish.

**Repair.** `type -t` → `builtin type -t` at both guards (`RP6-P0.sh` ~398-400),
matching the accepted RP7-WPI-RO.sh form (RP7-WPI-RO.sh:646-647); the `builtin`
prefix defeats a caller-defined `type` function. The comment (~376-396) and the
`P0_prereq` line are narrowed to what is established — *required shell functions
present and exercised* (`required_functions=present_and_exercised`) — NOT that
RP0-LIB as an identity was sourced. Binding the definitions to RP0-LIB would
require a frozen hash of RP0-LIB.sh and is outside this round. The reason token
`rp0_lib_not_sourced` is kept for consistency with the accepted RP7 sibling.

**Evidence.** `SELF_QA_RP6.md` §R7 carries the `R7_F2_HARNESS` D026 fence
(execution PENDING-LEAD-EXECUTION): RED = bare `type` + override + missing symbol
→ guard falsely PASSes; GREEN = `builtin type -t` + same override → guard STOPs;
plus an HONEST-BOUND case showing an unrelated same-name function still resolves
as `function` (presence, not provenance).

### C2 / A8 — R6-F3: close pathname expansion before the first split

**Root cause.** The outer parse `for p0_pin in $P0_TOOL_PINS` ran with globbing
ON, so pathname expansion happened BEFORE the new charset gate. A cwd crafted to
hold a directory tree matching `stat=/usr/bin/sta*` rewrote the token to
`stat=/usr/bin/stat` and the loop accepted it (`PIN_PARSE_ACCEPTED count=2
trusted=yes`). The round-6 R6-F3 harness used a cwd with no whole-token match,
so its 7/7 PASS did not falsify this.

**Repair.** The outer parse now runs with pathname expansion DISABLED, saving
and RESTORING the caller's prior noglob state (`RP6-P0.sh` ~554-624): `case $-`
captures prior state, `set -f` for the parse, restored on exit. The charset gate
and `p0_lookup`'s `set -f` remain as defense in depth. A crafted cwd can no
longer rewrite a token before the gate.

**Evidence.** `SELF_QA_RP6.md` §R7 carries the `R7_F3_HARNESS` D026 fence
(execution PENDING): the exact whole-token crafted-cwd case — a directory tree
`<cwd>/stat=/usr/bin/stat`. Pre-fix (no wrapper): clean cwd → STOP on the glob,
crafted cwd → `PIN_PARSE_ACCEPTED` (RED). Repaired: STOP identically in clean and
crafted cwds (GREEN).

### C3 / A9 — adjudicate producer shape before any rc-1 object verdict

**Root cause.** `p0_probe_kind` sanitized the rc-0 `stat -c %F` response before
checking its shape, so `directory\nwarning_from_probe\n` was folded to a token
that classified as `kind=other` and produced an rc-1 `venv_root_kind_unexpected`
FAIL on an unevaluable probe. `p0_assert_venv_root` likewise compared a successful
`readlink -f` response without validating it; an rc-0 empty response produced an
rc-1 `canonical=[]` FAIL.

**Repair (pattern 1 / pattern 6 — status good, shape not, so STOP).**
- `p0_probe_kind` (~1537-1556): on rc 0, reject empty / CR-LF multiline /
  non-printable shapes as reasoned rc 3 (`path_probe_empty` / `path_probe_multiline`
  / `path_probe_nonprintable`) BEFORE sanitising or classifying.
- `p0_assert_venv_root` (~1604-1623): on rc 0, reject empty / multiline /
  non-printable / non-absolute `readlink -f` output as rc 3
  (`venv_root_canonicalization_unparsable`); only a valid complete canonical path
  that differs from the preregistered literal may be a FAIL.

**Evidence.** `SELF_QA_RP6.md` §R7 carries the `R7_C3_HARNESS` D026 fence
(execution PENDING): both arms, real extracted repaired functions vs faithful
pre-fix replicas. Arm (a): multiline rc-0 `%F` → repaired STOP rc 3, replica
misclassifies `kind=other` (RED). Arm (b): empty rc-0 `readlink -f` → repaired
STOP rc 3, replica FAIL rc 1 (RED).

### C4 / A10 — narrow or enforce every printed claim

- **python3 mandatory** is now documented in the `P0_TOOL_PINS` comment
  (correction 7 makes every tool mandatory, python3 included).
- **rc 124** is relabelled `manager_query_rc124_timeout_reached_or_child_exit_124`
  (~1356). GNU `timeout` returns 124 both when it kills the child for the deadline
  and when the child itself exits 124 (`timeout 10s bash -c 'exit 124'` returns
  124 at elapsed_s=0); the wrapper cannot distinguish, so 124 is not labelled
  uniquely as a deadline. Prereg §8.1 row 9 amended to match.
- **interpreter isolation** is expressed as requested flags plus child-reported
  state (~1757-1768): the `P0_interpreter` line now says
  `launch_flags=requested_-I_-S child_reported_startup_flags=sys.flags.isolated_and_no_site
  self_verified=yes site_startup_disable=requested_not_binary_attested
  venv_pth_sitecustomize_execution=not_established_binary_provenance_unbound`, and
  the terminal claim carries
  `interpreter_launch=requested_-I_-S_child_reports_isolated_and_no_site_binary_provenance_unbound`
  and a narrowed `child_side_effects`/`venv_startup_disable` pair. Binary
  provenance is not bound, so site/`.pth` non-execution is disclosed as
  not-established rather than claimed.
- **`pinned_timeout`** is honest because correction 7 makes the `timeout` pin
  mandatory (the require-the-pin branch of A10): `timeout`'s resolution is
  `pinned_absolute` or the block STOPs, so the manager line's
  `bound=pinned_timeout_inside_cleared_env` is now truthful.

### C5 / A11 — make every evidence command literal and bounded

- All eight fences now carry UNIQUE whole-line marker pairs
  (`^# <NAME>_HARNESS_BEGIN$` / `^# <NAME>_HARNESS_END$`) whose invocation text
  cannot reopen the range: the three new R7 harnesses
  (`R7_F2`/`R7_F3`/`R7_C3`) and the five legacy fences
  (`C13_R3_BACKSTOP`/`RP6_FULLBLOCK_D026`/`F2_FREEZE_GATE`/`RP6_R4_D026`/`C13_R4B`).
  The recorded commands are marker-based `sed -n '/^# …BEGIN$/,/^# …END$/p'`.
- The R4 D026 fence's POST assertions were updated in place for the renamed
  tokens (rc 124 detail; interpreter evidence and launch tokens). PRE assertions
  (against the round-3 bytes) keep the old tokens, which is correct.
- Re-running every fence from a clean Git Bash, and confirming the R4 fence
  returns within its bound (the R6-recorded open handle), is
  **PENDING-LEAD-EXECUTION** (session gates bash). Existing PASS summaries are
  supplemental until their recorded marker-based commands exit cleanly.

### C7 — make the tool set finite (section-10.1 reconciliation, Lead-verified)

**Root cause.** `P0_TOOL_PINS` defaulted empty and only python3 was later
mandatory; every other tool could stay unpinned, non-python pins could name any
absolute path, and a missing pin fell back to `command -v` with
`resolution=path_resolved_absolute`. The reachable executable set was therefore
not derivable from the frozen source, blocking the Stage-1 path-scope proof.

**Repair.** Exactly one frozen pin is required for each of the twelve tools
(`stat readlink env find sha256sum systemctl ss curl timeout python3 id getent`);
each pin must equal its frozen deploy-channel literal (eleven new
`P0_FIXED_*` path literals plus `P0_FIXED_TRUSTED_PYTHON`). Omissions are rejected
(`input_pin_omitted`), extras/miscounts are rejected
(`input_pin_count_unexpected`), a non-python pin that differs from its frozen
literal is rejected (`input_pin_not_frozen_path`), and the unpinned
`command -v` fallback is DELETED so an unpinned tool STOPs (`tool_pin_unpinned`).
`p0_resolve_tool` now requires every tool's resolved path to equal its pin
(python3 keeps its canonicalisation allowance). Prereg §8.1 row 1 amended.

### C6 — fix the one stale site left by round 6

`RP6_REPAIR_R4_REPORT.md` (~line 87-88) carried the retracted claim that `-S`
"cannot be silently undone". Replaced with the round-6 truth: the third table row
shows the child `sys.flags` self-check catches only ACCIDENTAL flag-word loss
(cooperating `.pth`); a HOSTILE `.pth` that `os._exit(0)`s at `site` startup
defeats it, so `-S` itself — not the self-check — is the load-bearing control.

## Preservation (every arm not named above keeps its contract)

- rc 0/1/3 contract, STOP-vs-FAIL truthfulness, numeric identity, read-only
  scope: unchanged. C1 strengthens a guard and narrows a claim (more STOPs for a
  forged type, identical behaviour for a real function). C2 adds a `set -f`
  wrapper (identical behaviour for clean pins, STOP for crafted-cwd laundering).
  C3 adds shape STOPs before any rc-1 (more STOPs for malformed probes, identical
  behaviour for clean probes). C4 narrows printed tokens (no behaviour change).
  C7 makes pins mandatory and deletes a fallback (more STOPs for missing/mismatched
  pins; a complete frozen pin set is admitted exactly as before).
- Interpreter arm (`-I -S -c` launch), row-8 execution-domain gate, row-9 manager
  bound, resolver, evidence binding, numeric-identity discipline: the executable
  arms are unchanged; only printed tokens and the pin-binding strength change.
- The freeze gate changes in COUNT only (6 → 17), so no end-to-end `P0 PASS` is
  possible and nothing here is dispatchable.

## Evidence (D026 — REAL RED/GREEN, PENDING Lead execution)

Per the kickoff's PENDING-LEAD-EXECUTION clause, this session's Bash tool gates
script execution, so the R7 evidence is recorded as PENDING rather than
fabricated (D026 / pattern 10). `SELF_QA_RP6.md` §R7 carries three
self-contained, marker-delimited harnesses plus the marker migration of the five
legacy fences. The Lead runs each by anchored marker from a clean Git Bash and
records command, rc, summary and stderr. Expected summaries (expected, not
executed): `R7_F2_QA_SUMMARY cases=4 … PASS`, `R7_F3_QA_SUMMARY cases=4 … PASS`,
`R7_C3_QA_SUMMARY cases=4 … PASS`, and the five legacy fences at their recorded
PASS summaries. The Lead must also record the real `RP6-P0.sh` SHA-256, byte
count and `bash -n` rc.

## Scope

Six files touched (`RP6-P0.sh`, `SELF_QA_RP6.md`, `STATUS_RP6_P0.md`, this file,
`RP6_REPAIR_R4_REPORT.md` for correction 6, and two §8.1 rows of
`WPI_PREREGISTRATION_DRAFT.md`); nothing committed; no host contacted and no
network command run. Read-only scope, the rc 0/1/3 contract, STOP-vs-FAIL
truthfulness, numeric identity, and every pre-existing arm are preserved.

## Required to close

Independent Codex (`gpt-5.6-sol`, xhigh) re-audit — and, for dispatch blockade,
Claude (`claude-opus-5`, xhigh) — of the round-7 bytes against
`RP6_CODEX_AUDIT_R6_2026-08-10.md`, after the Lead executes the PENDING
`bash -n`, the three R7 harnesses, and the five marker-migrated legacy fences.
