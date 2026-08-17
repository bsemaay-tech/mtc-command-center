# KICKOFF — Codex T1 review: §10.2 path-scope prover (`pathscope_prover.py`)

You are the single T1 reviewer for a local static-analysis tool. Fresh session,
`gpt-5.6-sol`, effort high. Report only — edit nothing except your own output file.
Working dir `C:\LAB\Tradingview_LAB_CLEAN`. No host contact, no network.

## What the tool is for

Before a maintenance block is frozen, we must be able to state — and prove — the complete
set of host paths that block can reach. `pathscope_prover.py` parses the block's shell
source, expands the pinned constants, extracts every filesystem/network argument, and
reports each resolved path as inside or outside a declared allowlist. It executes nothing.

The tool's value depends entirely on one property: **it must not report a path as
resolved-and-allowed unless it genuinely established that.** Anything it cannot analyse
must come back as an explicit unresolved/rc-3 outcome, never as a silent pass. It was
deliberately not tuned to make the blocks pass — the current output is RP6 1 resolved /
37 unresolved and RP7 4 resolved / 65 unresolved, which is an expected shape, not a bug.

Author: Claude Opus 5 (high). You are independent of it.

## Inputs (relative to `MTC_COMMAND_CENTER\11_TRIAGE\`)

1. `WPI_PREREG_DRAFT_ROUND1/pathscope_prover.py` — 49820 B. Re-derive size + SHA-256.
2. `WPI_PREREG_DRAFT_ROUND1/KICKOFF_PATHSCOPE_PROVER.md` — the contract it was built to.
3. `WPI_PREREG_DRAFT_ROUND1/SELF_QA_PATHSCOPE.md` — its published QA and fixtures.
4. `WPI_PREREG_DRAFT_ROUND1/STATUS_PATHSCOPE.md` — status (`AUTHORED-PENDING-AUDIT`).
5. `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` §10.1 (the allowlist) and §10.2
   (what Stage 1 must emit). The tool must satisfy §10.2 as written.
6. `DESIGN_DEFECT_PATTERNS_2026-08-10.md` — check the tool against all ten patterns.
7. Real inputs to run it against: `WPI_BLOCKS_DRAFT/RP6-P0.sh` and
   `WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh` (read-only; do not modify them).

## Review contract

Attack the lexer and the resolver with executed fixtures, not code-reading alone:

- **Quote and expansion handling** — single/double quotes, `$'...'`, backslash-newline
  continuations, here-documents and here-strings, `$(...)` and backtick nesting, arrays,
  `${var:-default}`, `${var/x/y}`, arithmetic contexts, brace expansion, tilde.
- **Under-reporting is the fatal class.** Construct a block fragment that reaches a real
  filesystem or network primitive by a route the tool does not model, and show the tool
  reporting neither the path nor an unresolved marker. That is the highest-severity
  finding available and outranks everything else.
- **Sink coverage** — redirections (`>`, `>>`, `<`, `<>`, `&>`, fd duplication), `exec`,
  `source`/`.`, `cd`/`pushd`, command substitution feeding a path argument, `find -exec`,
  `xargs`, `tar`/`cp`/`install` style multi-path argv, `/dev/tcp`, `ssh`, `curl`, `getent`.
- **Verdict grammar** — exact/tree/terminal allowlist decisions, lexical normalization
  (`..`, `.`, repeated slashes, trailing slash), symlink-unaware claims stated as such.
- **Fail-closed discipline** — every unsupported construction must be rc 3 with a reason;
  find any path where an unsupported construction silently degrades to a resolved verdict.
- **Determinism** — same input, same output, stable ordering.
- Re-run its published QA yourself and confirm each published assertion actually holds;
  report any published evidence command that is not literally re-runnable.

## Output

Write **only** `WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_CODEX_T1_AUDIT_2026-08-10.md`:
verdict first (`PASS` / `PASS-WITH-NITS` / `REQUEST_CHANGES` / `BLOCK: <n>`), then findings
most severe first, each with the exact command run, its rc, and observed output. State
explicitly whether the current RP6/RP7 resolved-vs-unresolved counts are trustworthy
outputs of a sound tool. Do not commit.
