# KICKOFF — Author the §10.2 path-scope prover (Stage-1 freeze tooling)

You are Claude Opus 5 (high), implementer. Working directory:
C:\LAB\Tradingview_LAB_CLEAN. Authoring only — no host contact, no network, no commit.

## Contract (draft round 1.6+ §10.2, `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md`)

Stage 1 must emit, per frozen block, the sorted set of every host path that can reach a
filesystem or network primitive after constant and variable expansion, and show every
entry inside the §10.1 allowlist. A literal-string scan is supplemental only. The
accepted proof parses the complete shell input, rejects unresolved/dynamic path
construction, proves every path-bearing argument derives only from preregistered
constants, expands those constants, checks the closed set against §10.1, and falsifies
a forbidden path assembled from separately harmless tokens (must reject it).

## Deliverables (all in `WPI_PREREG_DRAND_ROUND1` is a typo guard — use `WPI_PREREG_DRAFT_ROUND1/`)

1. `WPI_PREREG_DRAFT_ROUND1/pathscope_prover.py` — Python 3.12, stdlib only. Input: a
   shell file + a constants table (the §2 `WPI_*`/`P0_*` values as KEY=VALUE lines) +
   an allowlist file (§10.1 patterns). Output: the sorted expanded path set, per-path
   allowlist verdict, and rc 0 only when the set is closed and fully allowlisted;
   rc 1 on any forbidden/unresolvable path; rc 3 on parse failure. Conservative by
   design: any construct it cannot statically resolve (command substitution into a
   path, unpinned variable, eval) is rc 3 REJECT, never a guess — an inability to
   evaluate is a STOP, never a pass.
2. `WPI_PREREG_DRAFT_ROUND1/SELF_QA_PATHSCOPE.md` — real RED/GREEN runs: GREEN on a
   small fixture using only preregistered constants; RED on (a) a forbidden literal
   path, (b) a forbidden path assembled from separately harmless tokens
   (`p="/etc"; q="mtc-bridge"; cat "$p/$q/x"`), (c) an unresolvable dynamic path →
   rc 3. Then run it against the REAL committed `RP6-P0.sh` and `RP7-WPI-RO.sh` with
   the real §2 constants and §10.1 allowlist, and record the honest result — expected
   outcome is a finding list, not necessarily a clean pass; do NOT tune the tool to
   make the blocks pass. Real output only.
3. `WPI_PREREG_DRAFT_ROUND1/STATUS_PATHSCOPE.md` — `AUTHORED-PENDING-AUDIT` (T1: this
   is local-only Stage-1 tooling), one-line design notes.

Touch ONLY those three files.
