# KICKOFF — path-scope prover round 2: nine T1 findings, four CRITICAL

You are the IMPLEMENTER. Codex is the auditor of record and will re-audit your bytes, so it
must not be you. Working dir `C:\LAB\Tradingview_LAB_CLEAN`. No host contact, no network,
no commit. Do not modify either block, the preregistration draft, or `verify_lock.py`.

If your session cannot execute commands, write the code and the fixtures, mark every QA
entry `PENDING-LEAD-EXECUTION`, and the Lead will run them. Do not fabricate transcripts.

## The finding that defines this round

The tool's whole value is that it cannot quietly miss a sink. Codex demonstrated four
classes of complete Bash fragment that reach a filesystem or network primitive while the
prover emits **no path, no `UNRESOLVED` marker, and `PATHSCOPE verdict=PASS rc=0`**. Until
that is impossible, the §10.2 Stage-1 gate does not exist and no block can be frozen.

## Inputs (relative to `MTC_COMMAND_CENTER\11_TRIAGE\`)

1. `WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_CODEX_T1_AUDIT_2026-08-10.md` — **REQUEST_CHANGES: 9**
   with executed fixtures. That text BINDS. Reproduce each fixture RED before repairing.
2. `WPI_PREREG_DRAFT_ROUND1/pathscope_prover.py` — 49820 B. Re-derive size + SHA-256.
3. `WPI_PREREG_DRAFT_ROUND1/KICKOFF_PATHSCOPE_PROVER.md` — the original contract.
4. `WPI_PREREG_DRAFT_ROUND1/SELF_QA_PATHSCOPE.md`, `STATUS_PATHSCOPE.md`.
5. `WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_LEAD_RERUN_2026-08-10.md` — the Lead's reproducible
   run and the trust amendment.
6. `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` §10.1/§10.2.
7. `DESIGN_DEFECT_PATTERNS_2026-08-10.md`.

## The nine findings

**CRITICAL — silent sink loss (1–4).** Each must become a specific rc-3 unresolved marker:
1. The `NO_PATH_COMMANDS` / control shortcut discards real sinks.
2. Ordinary SSH and NSS host grammar disappears entirely.
3. `find -exec` hides a nested forbidden primitive.
4. `--option=PATH` forms are discarded by the registered sink adapters.

**HIGH (5–7).**
5. Tilde is reported as a resolved-and-**allowed** path — a false ALLOW, the worst possible
   direction of error.
6. Lexical tree membership is presented as unconditional host-path `ALLOW`. Disclose the
   lexical-vs-host semantics explicitly, including the symlink and mount limits, and label
   the verdict accordingly.
7. The `<>` redirection is not tokenised and the real target disappears.

**MEDIUM (8–9).**
8. `unresolved_count` counts heterogeneous issue records, not unresolved paths. Separate
   unresolved-path cardinality from general parser/coverage issues; both may be printed,
   but they must be distinct fields with distinct names.
9. The real-input diagnostic evidence is not literally re-runnable.

## The governing rule

**Unmodeled grammar must fail closed.** Any command, option form, redirection, expansion or
construct the tool does not model produces a specific `UNRESOLVED` record naming what it
could not resolve — never silence, and never a `PASS`. When in doubt the tool STOPs. It is
allowed to be conservative and noisy; it is not allowed to be quietly wrong.

Do **not** tune the tool so the blocks pass. Its current honest outputs (RP6 rc 3, RP7 rc 3,
and rc 3 on the unfilled `<REMOTE_BASE>` placeholder) are correct behaviour and must stay
correct after repair.

## Coverage the re-audit will exercise

Tilde, brace expansion, arithmetic contexts, arrays, `${var:-default}` and `${var/x/y}`,
`$'...'`, backslash-newline continuation, here-documents and here-strings, `$(...)` and
backtick nesting, every redirection grammar including `<>`, `&>`, `>|` and fd duplication,
`exec`, `source`/`.`, `cd`/`pushd`, command substitution feeding a path argument,
`find -exec`, `xargs`, multi-path argv (`cp`/`tar`/`install`), `/dev/tcp`, `ssh`, `curl`,
`getent`. Build a fixture per class.

## Deliverables

Repaired `pathscope_prover.py` + `SELF_QA_PATHSCOPE.md` with a D026-style RED/GREEN pair for
every silent-pass fixture (RED on the current implementation, GREEN after repair) +
`STATUS_PATHSCOPE.md` + `PATHSCOPE_REPAIR_R2_REPORT.md` (finding → disposition → evidence).
Re-derive size and SHA-256. Publish the real-block diagnostic commands so they are
**literally re-runnable**, with complete output, using content anchors rather than line
ranges. Determinism check: same input, same output, stable ordering. State the disposition
of every finding explicitly, including anything you do not repair and why.
