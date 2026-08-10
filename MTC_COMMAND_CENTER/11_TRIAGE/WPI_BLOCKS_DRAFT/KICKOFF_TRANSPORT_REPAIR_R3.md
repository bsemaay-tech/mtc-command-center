# KICKOFF — Transport set round 3: close both flagship re-audit lists (5 findings)

Dispatched by the Claude Lead, 2026-08-10. Round-2 re-audit verdicts: Codex xhigh
`REQUEST_CHANGES 4` + N1 (`TRANSPORT_CODEX_REAUDIT_R2_2026-08-10.md`), Claude xhigh
`REQUEST_CHANGES 1` (`TRANSPORT_CLAUDE_REAUDIT_R2_2026-08-10.md`). Both flagships
independently found the same rc-classification defect — that convergence makes it the
priority. All 16 round-1 findings stay closed; do not regress them.

You are Claude Opus 5 xhigh, implementer. Working dir: C:\LAB\Tradingview_LAB_CLEAN.
No host contact, no network (local configuration/argv evaluation of the real pinned
`ssh.exe`/`scp.exe` without connecting IS required and IS in scope). No commit.
Write LF for shell files; keep `transport_runner.ps1` PowerShell 5.1-compatible.

## Inputs (relative to `MTC_COMMAND_CENTER/11_TRIAGE/`)

Both re-audit reports above (the contract), the eight transport files in
`WPI_BLOCKS_DRAFT/` at commit `9ef4437d`, `TRANSPORT_REPAIR_R2_REPORT.md`,
`WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` (§4 D-1 four-class contract,
§5, §7), the accepted Stage-2 originals under
`WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/02_PREREG/`, and
`DESIGN_DEFECT_PATTERNS_2026-08-10.md`.

## Findings and Lead adjudications

- **F1 (CRITICAL, both flagships)** — an observed rc outside the preregistered
  `{0,1,3}` grammar, and any native transport/cleanup failure (ssh exit 255, host
  down, rejected key, DNS, dropped route, local spawn error), must be classified
  **not-evaluable → `TR_RUN STOP`, runner exit 3**, never a completed deviant
  observation and never `TR_RUN FAIL`. FAIL remains reserved for a block that ran and
  returned rc 1. D026: drive each failure class and show the pre-fix bytes emitting
  FAIL and the repaired bytes emitting STOP.
- **F2 (CRITICAL)** — the constructed child environment cannot run the real pinned
  OpenSSH (`DELIVERED_ENV_RC=255` with zero output; adding `PROGRAMDATA` alone gives
  rc 0). Take Codex's second branch where possible: **explicitly disable ambient
  configuration and supply every required configuration through pinned arguments/
  files**; add and independently bind any environment/config path OpenSSH genuinely
  requires, each recorded with why it is needed. Prove it with the REAL pinned
  `ssh.exe`/`scp.exe` by local configuration/argv evaluation (no connection), plus a
  separate no-network process-capture arm. `cmd.exe` is supplemental only.
- **F3 (CRITICAL) — LEAD ADJUDICATION: derive, do not edit.** `remote_close_tree.sh`
  is byte-frozen accepted input and must NOT be edited. Author a fourth derived
  script `remote_close_tree_wpi.sh` under the D-1 contract, whose ONLY semantic delta
  versus the accepted 7470 B / `87157f0e…` original is class 2 (program identity):
  every tool it invokes (`mktemp`, `stat`, `tr`, `readlink`, `find`, `sort`,
  `sha256sum`, `cmp`) resolved from the frozen absolute `/usr/bin/<tool>` pin set with
  the same non-following kind / numeric `0:0` owner / not-group-or-world-writable
  admission the other `_wpi` scripts use, and no inherited-PATH lookup anywhere.
  Amend §4 to list it as the fourth derived script with the accepted original recorded
  as its derivation basis; the accepted original stays referenced but no longer
  travels. Reproduce Codex's PATH-first `sha256sum` attack: RED on the accepted bytes
  under the delivered environment (`MUTATED=yes`, `CLOSE PASS` while mutating), GREEN
  on the derived script (attack neutralised). Runtime tool digests are captured as
  evidence, not compared to pins (they cannot be known before host contact) — state
  that limit explicitly in the script's claim lines.
- **F4 (HIGH) — LEAD ADJUDICATION: bind, do not waive.** Bind the allocation parent to
  a preregistered external mount identity before the first `mkdir`. This is available:
  owner grant #6 authorizes a read-only attestation command set in the grant-#3 root
  session, and the successor preregistration will order that attestation **before**
  op 01, so the covering-mount identity of `/home/gatea` is a preregistered constant
  the setup script compares against. Implement the comparison with a
  `<PIN-AT-FREEZE>` constant + the usual rc-3 missing-input pre-check; a mismatch is
  STOP before any mutation. Record it as a freeze-gate input and note the successor
  ordering requirement in `STATUS_TRANSPORT.md`.
- **N1 (nit)** — correct the placeholder census to the re-derived counts (36/27 for the
  six executable/plan files; 41/33 across all eight).

## Deliverables

The eight transport files as needed + new `remote_close_tree_wpi.sh` +
`SELF_QA_TRANSPORT.md` (every closure REAL RED/GREEN; F2's real-`ssh.exe` evaluation
and F3's PATH-attack pair are load-bearing — run them) + `STATUS_TRANSPORT.md` +
narrow draft edits (§4 fourth derived script, §5/§7 as the fixes name, plus the
successor-ordering note for F4) + `TRANSPORT_REPAIR_R3_REPORT.md` (finding →
disposition → evidence, plus draft-edit list and every freeze-gate input). `bash -n`
each shell file; PS 5.1 parse the runner; per-file SHA-256 + bytes. Do not commit.
