# KICKOFF — Transport round 4: four Codex final-audit findings + the F4 adjudication

You are Claude Opus 5 xhigh, IMPLEMENTER. Codex is the auditor of record for these
findings and will re-audit your work, so separation holds. Round 4 is authorised under
owner grant #7 (T0 cap lifted for this block set until both flagships accept).
Working dir: C:\LAB\Tradingview_LAB_CLEAN. No host contact and no network connection;
local configuration/argv evaluation of the real pinned `ssh.exe`/`scp.exe` WITHOUT
connecting is in scope. Do not commit. Write shell files with UNIX LF only; keep
`transport_runner.ps1` PowerShell 5.1-compatible.

## Inputs (relative to `MTC_COMMAND_CENTER/11_TRIAGE/`)

1. `WPI_BLOCKS_DRAFT/TRANSPORT_CODEX_FINAL_AUDIT_2026-08-10.md` — F1–F4 with executed
   falsifications and required repairs. That text BINDS.
2. `WPI_BLOCKS_DRAFT/TRANSPORT_CLAUDE_FINAL_AUDIT_2026-08-10.md` — the accepting
   verdict on the same bytes, including its nits. Its reasoning on the `always` rule
   informs, but does not override, the adjudication below.
3. The nine transport files at commit `78173bfd` in `WPI_BLOCKS_DRAFT/`.
4. `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` — §4/§5/§7; edit where a fix
   requires it, and list every draft edit in your report.
5. `DESIGN_DEFECT_PATTERNS_2026-08-10.md`.

## The four repairs

- **F1 (CRITICAL)** — the remote interpreter is selected outside the pinned program
  domain, and the runner accepts an unrelated marker family. Bring the remote
  interpreter inside the pinned/bound program contract and require the correct,
  specific marker family; an unrelated marker must not satisfy the check.
- **F2 (HIGH)** — inherited `TMPDIR` lets the close script write inside the evidence
  tree while it reports read-only behaviour. Give every child a run-owned TMPDIR that
  cannot name the evidence tree or any protected path, and make the read-only claim
  true (or state precisely what it does establish).
- **F3 (HIGH)** — a mixed close-tree probe error is classified as evidence absence and
  becomes FAIL. Classify it as STOP: an ambiguous or mixed probe error is an inability
  to evaluate, never a completed observation of missing evidence.
- **F4 (HIGH) — LEAD ADJUDICATION: Codex prevails; implement per-branch prerequisites.**
  Do NOT keep the single global `$sequenceOk` snapshot. Model prerequisites per branch
  and per operation: P0 close depends on P0 stage establishment; RO close on RO stage
  establishment; each fetch on its corresponding close; each local bind on its
  corresponding close/fetch. An unrelated branch's failure must never demote a genuine
  marked rc 1 to not-evaluable. Codex's decisive fixture must go GREEN: ops 01–06 all
  match, P0 close returns `CLOSE_STOP` rc 3, independent RO close returns a genuine
  marked `CLOSE_FAIL` rc 1 → the RO deviation must be counted (`deviant>=1`, run FAIL),
  not erased. Claude's scenario must still hold: a cleanup after a genuinely
  unestablished prerequisite stays not-evaluable. This subsumes Claude's nit — emit
  distinct reasons for `cleanup_after_unestablished_prerequisite` vs
  `cleanup_after_earlier_deviation`.

Also address, from the Claude report, anything it raised as a nit that these repairs
touch anyway; list the rest as deferred with reasons.

## Deliverables

Repaired transport files + `SELF_QA_TRANSPORT.md` (REAL RED/GREEN for each fix — F4's
decisive fixture and F2's TMPDIR write are load-bearing; run them) + `STATUS_TRANSPORT.md`
+ narrow draft edits + `TRANSPORT_REPAIR_R4_REPORT.md` (finding → disposition → evidence,
draft-edit list, freeze-gate inputs). `bash -n` each shell file; PS 5.1 parse the runner;
per-file SHA-256 + bytes; zero CR BYTES (count bytes, not matching lines). State the
disposition of EVERY finding explicitly, including any you do not repair and why.
