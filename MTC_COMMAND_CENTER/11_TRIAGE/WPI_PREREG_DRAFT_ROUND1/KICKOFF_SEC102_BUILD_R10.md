# KICKOFF — SEC102 composite pathproof round 10: bind checked bytes to executed bytes (Codex r9, the last finding)

You are `claude-opus-5` xhigh via the Max account, IMPLEMENTER. Codex audits r10. Working dir
`C:\LAB\Tradingview_LAB_CLEAN`. No host, no network, no commit. Scope fence: touch ONLY
`SELF_QA_SEC102_R10.md` (new — carry forward the r9 self-QA content and fix the §13 wrapper),
`STATUS_SEC102.md`, the round-10 report `SEC102_R10_REPORT_2026-08-12.md`, and the scoped
`.gitattributes` (add r10 fixtures if any). `composite_pathproof.py` MUST stay untouched
(129658 B, SHA-256 `adbf27fd908439e1d48e6c95a4eecba956c0607c42ae5a3bfa9cb210b636c05a`).
Do NOT touch `pathscope_prover.py`, block files, RP6/RP7, prereg drafts. Never git
checkout/reset/stash any tracked file.

## Context — commit `ba929abc` audited, verdict `SEC102_CODEX_T1_AUDIT_R9_2026-08-12.md`
Codex r9 CLOSED the r8 LF/CRLF finding and independently reproduced everything (11/11 blocks,
58/58 matrix, D026 both directions, M1 gate). Residual 41 judged honest. One new MEDIUM.
This is the THIRD consecutive evidence-harness round (r7 child-status → r8 newline → r9
TOCTOU) — the structural lesson applies: close the CLASS (temporal rebinding), not the
instance. The prover, both CRITICALs, the command-word whitelist fixpoint, and the
owner-ratified vocabulary disclosure all stay closed.

## The single finding (Codex r9 — MEDIUM, Pattern 11 with Pattern 9 overlay)
`SELF_QA_SEC102_R9.md:1749-1755,2084-2110`: the pre-launch byte comparison is not bound to
the object PowerShell later opens. The wrapper writes the temp `.ps1`, reads it back, compares
— then launches `powershell.exe -File <pathname>`, which RESOLVES THE NAME AGAIN after the
equality decision. A concurrent same-principal process can replace/modify the file in that
window; the child executes bytes never compared while `SCRIPT_BYTES_IDENTICAL=1` and the
published SHA describe the earlier bytes. The document's "no path through the wrapper on
which unproven bytes are executed" / "what the interpreter is handed" claims overrun this.

## Required repair (Codex's spec: no replace/modify window between verification and
interpreter consumption; a pre-launch read + pathname reopen is insufficient)
Pick ONE structural route and implement it completely:
- **(A) Object pinning:** create the temp file via Win32 `CreateFileW` (ctypes) with share
  mode `FILE_SHARE_READ` ONLY (no write share, no delete share), write the bytes, flush,
  KEEP THE HANDLE OPEN across the child's entire lifetime, and only then launch
  `powershell.exe -File`. With write and delete sharing denied, no same-principal process can
  modify, replace, delete, or rename the object between comparison and child exit; the name
  the child resolves can only reach the pinned object. Read-back comparison stays, performed
  through the held handle or a second read handle.
- **(B) Direct consumption:** eliminate the file: feed the COMPARED BYTES themselves to the
  interpreter (`powershell.exe -NoProfile -Command -` with the byte buffer written to the
  child's stdin pipe). The executed instrument IS the compared buffer; no name, no window.
  Only choose this if you verify the rc/exit semantics of every published block are conserved
  under `-Command -` (exit codes, `$ErrorActionPreference`, stderr behavior) — if any block's
  contract changes, use route A.
State in the report WHY the chosen route closes the whole temporal-rebinding class.

## D026 evidence (required, no attack fixture, symbolic names)
1. RED against the exact r9 wrapper: a harmless concurrent rewriter that swaps the temp file's
   bytes in the check→launch window (a benign sentinel that prints a different marker line),
   showing the r9 wrapper accepts output from bytes it never compared (or, if the race cannot
   be made deterministic, demonstrate the window's existence deterministically: hold the r9
   sequence at the launch boundary and prove a write succeeds after the comparison).
2. GREEN under r10: the same rewriter attempt FAILS (route A: the write/replace is denied by
   the held handle — show the real denial; route B: there is no file to rewrite and the child
   provably consumed the compared buffer).
3. Conserve ALL r9 gates verbatim behind the new binding (byte gate, status, stderr, subset)
   and re-run the eleven published blocks + outer wrapper from exact published bytes.
4. Narrow the two overrunning sentences ONLY if a provable residual remains after the repair;
   otherwise make them true. Update STATUS item 43 to name the closed rebinding class.

## Deliverables
`SELF_QA_SEC102_R10.md` + `STATUS_SEC102.md` (r9 TOCTOU finding closed; vocabulary residual
stays disclosed per owner ratification C; residual 41 carried) +
`SEC102_R10_REPORT_2026-08-12.md`. Keep the 58-case matrix and all carried fences passing.
No commit — the Lead commits and reproduces the wrapper + D026 verbatim.
