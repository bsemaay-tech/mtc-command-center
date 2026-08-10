# KICKOFF — RP6-P0.sh round 7: five Codex required corrections

You are the IMPLEMENTER for round 7. Codex is the auditor of record for these corrections
and will re-audit your bytes, so it must not be you. Round 7 is authorised under owner
grant #7 (T0 round cap lifted for this block set until both flagships accept).
Working dir `C:\LAB\Tradingview_LAB_CLEAN`. No host contact, no network, no commit.
UNIX LF only, zero CR bytes. Never `git checkout` a block file (autocrlf rewrites it); to
restore, use `git cat-file blob HEAD:<path> > <path>`.

If your session cannot execute shell commands, **do not fabricate transcripts** — write
the harnesses, mark each QA entry `PENDING-LEAD-EXECUTION`, and the Lead will run them and
replace the placeholders with real output. That is the expected and accepted behaviour.

## Inputs (relative to `MTC_COMMAND_CENTER\11_TRIAGE\`)

1. `WPI_BLOCKS_DRAFT/RP6_CODEX_AUDIT_R6_2026-08-10.md` — **REQUEST_CHANGES**, five required
   corrections with executed falsifications (rows A4, A8, A9, A10, A11). That text BINDS.
2. `WPI_BLOCKS_DRAFT/RP6-P0.sh` — round-6 bytes, 93421 B, SHA-256
   `75db028e76438bc88caba19b9c3b6411e5f573f7b6c2bd13c3883d24e4389570`, commit `8fcab4d4`.
3. `WPI_BLOCKS_DRAFT/SELF_QA_RP6.md`, `STATUS_RP6_P0.md`, `RP6_REPAIR_R6_REPORT.md`.
4. `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` — edit narrowly only where a
   correction requires it; list every draft edit in your report.
5. `DESIGN_DEFECT_PATTERNS_2026-08-10.md` — binding.

## Writable file list (write nothing else)

- `WPI_BLOCKS_DRAFT/RP6-P0.sh`
- `WPI_BLOCKS_DRAFT/SELF_QA_RP6.md`
- `WPI_BLOCKS_DRAFT/STATUS_RP6_P0.md`
- `WPI_BLOCKS_DRAFT/RP6_REPAIR_R7_REPORT.md` (new)
- `WPI_BLOCKS_DRAFT/RP6_REPAIR_R4_REPORT.md` — **for correction 6 only**
- `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` — narrow edits only

**Owned by other live sessions — never write them:** `RP7-WPI-RO.sh`, `SELF_QA_RP7.md`,
`STATUS_RP7.md`, `RP7_*`, `transport_runner.ps1`, `TRANSPORT_*`, `remote_*.sh`,
`run_p0.sh`, `run_ro.sh`, `pathscope_prover.py`, `SEC101_*`, `PATHSCOPE_*`.

## The corrections

1. **Make the R5-F2 prerequisite check a real builtin, and make its claim honest.** Use
   `builtin type -t` (or an equivalently non-overridable builtin) so a caller-defined
   `type()` cannot forge the result — Codex defined `type(){ printf 'function\n'; }` and
   both guards passed while the missing `rp0_require_safe_component` fell through to
   `command_not_found_handle`, ending `PREREQ_GATE_ACCEPTED`. Separately: function type
   alone cannot prove a function came from RP0-LIB. Either bind the definitions to the
   accepted RP0-LIB identity, or narrow `P0_prereq lib=sourced` (line ~375) and the
   comments at ~354 to what is actually established — *required shell functions were
   present and exercised*. D026 RED/GREEN for an overridden `type` and for an unrelated
   same-name shell function.

2. **Close R6-F3 before the first split.** The outer parse is still
   `for p0_pin in $P0_TOOL_PINS` (line ~488) with globbing enabled, so pathname expansion
   happens *before* the new charset gate. Disable pathname expansion around that outer
   parse — preserving and restoring the caller's prior noglob state — or parse without
   unquoted expansion. Keep the charset gate and the `p0_lookup` defence as depth. Extend
   the R6-F3 harness with the exact whole-token crafted-cwd case: a tree matching
   `stat=/usr/bin/sta*`. Current bytes must be **RED** (crafted cwd → rc 0,
   `PIN_PARSE_ACCEPTED count=2 … trusted=yes`); repaired bytes must **STOP identically in
   clean and crafted cwds**.

3. **Adjudicate producer SHAPE before any rc-1 object verdict.** In `p0_probe_kind`
   (~1428-1454), reject CR/LF, non-printable, empty and otherwise invalid rc-0 producer
   shapes as a reasoned **rc 3** *before* sanitising or classifying — Codex turned
   `directory\nwarning_from_probe\n` into `kind=other` and an rc-1 `venv_root_kind_unexpected`
   FAIL on an unevaluable probe. Apply the same status-then-shape rule to a successful
   `readlink -f` in `p0_assert_venv_root` (~1491-1498): empty, multiline, non-printable or
   unparseable output is **STOP**; only a valid, complete canonical path that differs from
   the preregistered literal may be FAIL. D026 for both arms.

4. **Narrow or enforce every printed claim.** At minimum: document that `P0_TOOL_PINS`
   requires `python3` (it is called optional at ~478 while R5-F1 makes it mandatory); do
   not call the prerequisite check builtin- or provenance-bound unless it is; either
   require the timeout pin before printing `pinned_timeout` (~1381, ~1636) or print its
   real resolution mode; do not label rc 124 uniquely as a deadline unless the wrapper can
   distinguish a child's own rc 124 (`timeout 10s bash -c 'exit 124'` returns 124 at
   `elapsed_s=0`); and express interpreter isolation as *requested flags plus
   child-reported state* (~1607, ~1636) unless the interpreter's provenance is
   independently bound.

5. **Make every evidence command literal and bounded.** Replace **all** line ranges with
   unique anchored marker pairs whose own invocation text cannot reopen the range — e.g.
   `^# R6_F1_HARNESS_BEGIN$` / `^# R6_F1_HARNESS_END$`. The recorded unanchored
   `/BEGIN/,/END/` commands all returned rc 2 because `sed` re-entered the range at the
   later Markdown line containing both markers. **Give the five legacy fences the same
   marker treatment** — this is also the Lead's own finding: they are addressed by
   absolute line ranges, the file grows every round, and two of them now run into prose
   and look like regressions. Repair the R4 fence so all descendants close and the command
   returns within its documented bound (it retained an open handle and blew a 60 s bound).
   Then re-run every exact command from a clean Git Bash and record command, rc, summary
   and stderr. Existing PASS summaries are supplemental until their recorded commands exit
   cleanly.

6. **Fix the one stale site left by round 6** (outside R6's allowlist, inside yours):
   `RP6_REPAIR_R4_REPORT.md:88` still carries the retracted claim that `-S` cannot be
   silently deleted. The truthful statement is the R6 one: the self-check catches only
   ACCIDENTAL loss, a hostile `.pth` defeats it, and `-S` is the load-bearing control.

## Deliverables

Repaired `RP6-P0.sh` + updated `SELF_QA_RP6.md` (RED/GREEN per correction, anchored
commands only) + `STATUS_RP6_P0.md` + narrow draft edits + `RP6_REPAIR_R7_REPORT.md`
(finding → disposition → evidence, draft-edit list, freeze-gate inputs). `bash -n` rc 0;
re-derive SHA-256 + byte count; zero CR bytes measured with `tr -cd '\r' < file | wc -c`
(never `grep -c $'\r'` — inside a loop it matches every line and cries wolf). State the
disposition of every correction explicitly, including anything you do not repair and why.
Do not commit; the Lead verifies the hash and commits.
