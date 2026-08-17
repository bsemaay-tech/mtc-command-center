# KICKOFF — B3 repair round 6 (DOCUMENTATION ONLY, last mechanical layer)

Audit 5 confirmed the code is frozen and closed, and closed the command-level
placeholders. One survivor remains: the section-4 shared DECLARATION block in
`SELF_QA.md` is not copy-paste runnable, so the section-5 commands that source it are
technically not self-executing. This round makes that block literally runnable and
changes nothing else. Write into `round6/`. ASCII only. English only.

## Absolute code-freeze constraint (verify by hash before finishing)

`round6/RP1-B3.sh`, `round6/RPD-VERIFY.sh`, `round6/DESIGN_NOTES.md` MUST be
byte-identical copies of `round5/` (which equal round4). Required SHA-256:

- `RP1-B3.sh` = `6f3ea022b68d80a552c4ebcb771bbb2a707bdab46a383d605ffc5b88b884becc`
- `RPD-VERIFY.sh` = `3b9e78e87cecdc10ab1a10d14e79dbff530968e4075277117743c88976fa813c`
- `DESIGN_NOTES.md` = `103ffe3811dfd7764bf1b4d9bc47489fbe3cb2d72bca7c5c32e461a82440f23b`

They are pre-copied for you. Do NOT edit them. No code license this round.

## Inputs (read these, nothing else)

- This file; `audit5/AUDIT5_REPORT.md` (the single required finding); `round5/SELF_QA.md`
  (the file to repair — the defect is its section 4, lines ~346-385, plus any command
  block that silently depends on that setup).

## The only permitted change — make `round6/SELF_QA.md` section 4 copy-paste runnable

The exact-command standard means: a reader can paste section 4, then any section-5
command block, into a fresh MSYS/Git-Bash shell and reproduce the recorded output with
zero edits. Fix precisely these, and re-verify the whole file still satisfies it:

1. **`QA=<the scratch directory rendered as $QA above>` (line ~354) is invalid Bash.**
   Replace with a literal establishing command: `QA="$(mktemp -d)"`. Then ensure every
   fixture/`arm.sh`/subtree that any section-5 command sources is BUILT by literal
   commands that appear in section 4 (or at the top of that command's own block)
   against `$QA`, so a paste-and-run genuinely recreates them. If some section-5 blocks
   already build their own fixtures, keep that; only add what is missing. Nothing may
   assume a pre-existing populated `$QA`.
2. **`B="<repo>/..."` (line ~352) uses a disallowed placeholder.** Replace `<repo>`
   with the literal absolute MSYS path of this checkout:
   `B="/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/06_B3_REPAIR"`.
   A literal absolute path is exact, not a placeholder. Keep `R2/R3/R4` derived from it.
   Remove the now-obsolete "fourth path normalization" justification prose for `<repo>`.
3. **The shared capture recipe `out="$(<the run line> 2>&1)" ...` (line ~381)** stands
   in for real commands. Either (a) give each direct-run arm its own literal, complete
   capture command inside that arm's block, or (b) define a single literal helper
   `run_capture() { local out rc=0; out="$(eval "$1" 2>&1)" || rc=$?; emit "$out"; printf 'RC=%s\n' "$rc"; }`
   in section 4 and show each arm calling it with its literal command string. No
   `<the run line>` placeholder may remain.
4. Re-scan the WHOLE file: no command block anywhere may contain `<...>` angle-bracket
   placeholders except the two explicitly-declared output normalizations the auditor
   already accepted (`<QA>` for scratch-root in RECORDED OUTPUT, and the machine-local
   python path token) — and those appear only in OUTPUT transcripts, never in a command
   you are telling the reader to run.

Do not touch section 0 hashes, the code files, the arithmetic (43 A / 119 B / 3 C, PASS),
or the narrowed nit-2 wording (PASS). Do not remove any truthful caveat.

## Deliverable

`round6/` with exactly four files: the three byte-identical code/doc files and the
repaired `SELF_QA.md`. No hidden files. Print DONE plus the four SHA-256s.
