# KICKOFF — Claude Pro T1 EXECUTION-audit: pathscope_prover.py round 2 (flagship slot)

You are `claude-opus-5` **high** (T1 tier — corrected 2026-08-12 ~20:35; this kickoff previously
said `xhigh`, which is the T0 setting and is not the correct value for a T1 tool audit) via the
default Claude Pro account, AUDITOR. This tool has no
Codex flagship audit and cannot get one: the Codex provider content filter terminates the
run while merely READING `pathscope_prover.py` (its sink-detection source carries attack
grammar as data — forbidden-path tables, exfil URL patterns, ssh/nss host grammar). GLM-5.2
gave a favorable READ-audit, but GLM gates execution, so that opinion is SUPPLEMENTAL. You
are the flagship EXECUTION auditor: a fresh session, non-implementer (Max implemented r2),
and you CAN run the harness. Working dir `C:\LAB\Tradingview_LAB_CLEAN`. Read-only on the
repo: edit nothing except your verdict file, no git mutation, no host, no network beyond
local execution of the published harness.

## Bytes under audit
`pathscope_prover.py` 122446 B, SHA-256
`890016f0b9a8cde4eed33f8733f69055471b07c6096f6bc07450457e6c52af1d` — re-derive and confirm
first. Context files: `SELF_QA_PATHSCOPE.md`, `STATUS_PATHSCOPE.md`,
`PATHSCOPE_REPAIR_R2_REPORT.md`, round-1 Codex findings
(`PATHSCOPE_CODEX_T1_AUDIT_2026-08-10.md`), GLM read-audit
(`PATHSCOPE_GLM_T1_AUDIT_R2_2026-08-11.md`).

## Round-2 state you must independently re-establish
9+5 silent-sink classes closed. Structural change: `NO_PATH_COMMANDS`/`nonoption_operands()`
removed; an explicit `Spec` registry declares per command every accepted option and its
value role; unlisted option or unregistered command → a specific rc-3 coverage record
(fail-closed). Finding 6 repaired as DISCLOSURE: `ALLOW-LEXICAL` +
`symlink_resolution=not_established mount_boundary=not_established`, residual R1 (symlink/
mount binding) honestly out of reach for a static reader. The Lead ran the harness verbatim:
RED 511 / GREEN 644, determinism `equal=True` (find_exec, RP6-P0, RP7-WPI-RO).

## KNOWN DOCUMENTARY DEFECTS — found 2026-08-12 evening, NOT yet repaired
A prose-vs-transcript audit (`WPI_SELFQA_CLAIM_AUDIT_TRANSPORT_PATHSCOPE_2026-08-12.md`) found
two claims in `SELF_QA_PATHSCOPE.md` its own evidence does not support. Disclosed so you do not
spend your slot rediscovering them:

- **FALSE — `:325-327` says the RED rows reading `rc 0 - (no row)` are "the four CRITICAL
  findings".** The table actually contains **sixteen** such rows — `pushd`, `pushd_forbidden`,
  `popd_stack`, `trap`, `ssh`, `ssh_command`, `getent`, `python_c`, `alias`, `hash_p`,
  `mapfile_cb`, `systemctl_link`, `jobs_x`, `fddup`, `herestring`, `nc_client` — and the
  transcript confirms the same `PASS rc=0` zero-record pattern across them
  (`:427-461`, `:505-534`, `:583-587`, `:632-636`, `:729-733`).
- **UNSUPPORTED — `:8-10`** asserts every run used CPython 3.14.2 with `-B`, that the repaired
  source parses with `ast.parse(..., feature_version=(3,12))`, and that Python 3.12 is not
  installed. The harness stdout at `:43-51` prints artefact identities, line counts and
  determinism lines — none of those three facts.

**Two questions for you, since you can execute:**
1. Does the sixteen-vs-four discrepancy mean the round-1 CRITICAL count was understated in the
   document, or is "four CRITICAL" correct and the `rc 0 — (no row)` pattern simply broader than
   the CRITICAL subset? The distinction decides whether this is a wording defect or a coverage
   claim that overstates what was closed.
2. **U-3 is directly checkable by you.** Record the actual Python version, the `ast.parse`
   result, and whether 3.12 is present — that converts three unsupported assertions into
   measured facts or into findings.

## Audit contract
1. EXECUTE the published harness VERBATIM (`SELF_QA_PATHSCOPE.md` §"How to reproduce"):
   62 fixtures + 4 real-block runs + RED-before-GREEN (D026). Record real counts. This
   execution is the point of your slot — a read-only opinion here is supplemental, and we
   already have one.
2. Adversarially construct NEW Bash fragments that reach a filesystem/network primitive
   while the prover emits no path, no coverage record, and `PASS rc=0`. Any surviving
   silent sink is CRITICAL. (Local, harmless fixtures only; keep bodies symbolic.)
3. Judge finding-6/R1 honesty: does any output still present lexical membership as an
   unconditional host ALLOW?
4. Verify fail-closed coverage-error behaviour on unmodeled syntax and determinism.
5. Thirteen-pattern adjudication table. Verdict: PASS / PASS-WITH-NITS / REQUEST_CHANGES /
   BLOCK. If accepting, state that pathscope holds a flagship EXECUTION acceptance (Codex
   unavailability on record + GLM supplemental favorable).

Write ONE new file: `PATHSCOPE_CLAUDE_T1_EXEC_AUDIT_2026-08-12.md` (this directory).
**Delta gate (corrected 2026-08-12 ~20:35 — a global clean-status gate CANNOT pass in this
worktree, which carries ~100 pre-existing untracked run logs, and would have self-blocked this
lane).** Instead:
1. **Before execution** capture `git status --porcelain` → `before`.
2. Run the lane.
3. **At the end** capture `git status --porcelain` → `after`, and prove `after` minus `before`
   contains **only** `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_CLAUDE_T1_EXEC_AUDIT_2026-08-12.md`
   and nothing else. Any other entry in the delta **fails** the gate.
4. Also run `git status --porcelain -- MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_CLAUDE_T1_EXEC_AUDIT_2026-08-12.md`
   and record its output as the path-scoped confirmation.
