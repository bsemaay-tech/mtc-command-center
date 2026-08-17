# KICKOFF — Codex re-audit of the C13 round-3 repair (read-only)

You audited the C13 arm (BLOCK, 3 findings). Claude Opus 5 implemented the bounded
round-3 repair and claims all three closed. Verify closure. Report only.

**Owner amendment A2/A2a in force: do the audit yourself, do not sub-delegate.**

## Inputs (relative to `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/`)

1. `RP6-P0.sh` — repaired bytes (claimed SHA-256
   `ef205e2064caa0cb1493abf037ce9d435f2bf8f6259c5bb3fc4964d1abb2b4b9`, 55467 B;
   pre-R3 baseline `cfdb23b8…`, 54109 B at `8d2f25a5^`).
2. `SELF_QA_RP6.md` — extended QA (two new D026 harnesses; earlier fences relabelled
   SUPPLEMENTAL).
3. `RP6_C13_REPAIR_R3_REPORT.md` — implementer report.
4. `RP6_C13_CODEX_AUDIT_2026-08-10.md` — your findings (the closure contract).

## Verify

- **V1** F1 closed: rc 2 → nomatch only on empty merged capture; any byte at rc 2 →
  error → `identity_unresolvable` rc 3; genuine valid no-match still reaches
  `state_account_resolution_unexpected observed_numeric=absent`. Re-run the F1
  RED/GREEN yourself.
- **V2** F2 closed: harness 1 is driven by the block's own top-level driver lines (not
  extracted functions); pre-R3 bytes fail RED; integration-call-deleted mutant goes
  ASSERT_UNMET; backstop-removal mutants fail polarity. Re-run at least harness 1
  yourself.
- **V3** F3 closed: header claims now truthful.
- **V4** Diff isolation vs `8d2f25a5^`: only the F1 parser arm, QA, status, report —
  every other arm byte-identical.
- **V5** Hash + bytes re-derived; `bash -n`.

Output: write `RP6_C13_REAUDIT_CODEX_2026-08-10.md` — verdict first (`PASS` or
`BLOCK: <n>`), V-rows with evidence, findings if any. Touch ONLY that file.
