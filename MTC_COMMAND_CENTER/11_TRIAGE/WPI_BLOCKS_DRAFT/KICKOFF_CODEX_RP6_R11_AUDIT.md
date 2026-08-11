# KICKOFF — Codex T0 audit: RP6-P0 round 11 bytes

Date: 2026-08-11. Codex `gpt-5.6-sol` xhigh, AUDITOR of record, fresh session. Read-only:
edit nothing except your verdict file, no git mutation, no host, no network. T0 surface.

## Bytes under audit — commit `2d033fa6`

`RP6-P0.sh` SHA-256 `5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330`
(was `a090ae73…`). `SELF_QA_RP6.md`, `STATUS_RP6_P0.md`, `RP6_R11_REPORT_2026-08-11.md`.

## Your round-10 findings (REQUEST_CHANGES ×4)

`RP6_CODEX_T0_AUDIT_R10_2026-08-11.md` — (1) grammar normalizer lossy / not fail-closed;
(2) F3 unknown stat-kind → host FAIL rc 1 (should STOP); (3) R9 RED-twin recipe masks status
via trailing `rm` (recipe rc 0 while harness failed) + guard falsification prose-only;
(4) F4 evidence prose outruns predicate.

## Round-11 dispositions to verify

The Lead ran the R11 harnesses VERBATIM from the block dir (rc 0):
- `R11_GRAMMAR` 15/15 — now 149 tuples/163 sites, census `emitter_lines=163 unmodeled=0`,
  `correlation_preserved_one_value_per_field`, mutant `alt_quoting killed_by=census(164!=163)`,
  mutant `correlated_relabel killed_by=grammar_closed`.
- `R11_F3` 85/85 — unknown stat-kind → `P0_STOP reason=link_target_kind_unrecognized rc 3`;
  every recognized POSIX special-file kind still `P0_FAIL ... kind=other` rc 1; regular rc 0.
- `R11_F4` rc 0; `R11_F1_RED` 17/17 (falsification: r10 grammar blind to alt-quoting +
  correlated relabel; r11 census/tuples catch them; parser-alone still blind is asserted).
- The R9 RED-twin recipe (`R11_R9RED`) now returns real rc 1.

## Audit contract

- Re-run each published R11 command VERBATIM; confirm summaries + statuses. The round-10
  finding 3 was exactly a recipe whose exit status disagreed with its verdict — re-verify the
  R9 RED-twin recipe returns rc 1 now, and that the guard-falsification is now an executable
  fence, not prose (D026). State which you executed; non-execution ≠ acceptance (D025 r1).
- Finding 1: independently attempt an unmodeled emitter syntax (a novel valid quoting form)
  and a correlation-preserving relabel; confirm the census fails closed on the first and the
  tuple comparison catches the second. Try to find a syntax the census still misses.
- Finding 2: confirm no successful-producer + unrecognized-token path still reaches host FAIL;
  confirm the recognized-kind grammar is complete for GNU `stat %F`.
- Finding 4: confirm the F4 prose now matches the executed predicate.
- 13 defect patterns. Verdict: PASS / PASS-WITH-NITS / REQUEST_CHANGES / BLOCK.
- Note in passing (not a finding for you to fix): `RP6_R10_REPORT_2026-08-11.md:362-364`
  still carries an "every input class" overclaim that r11 corrected in the r11 report/SELF_QA/
  STATUS instead of editing the r10 report in place (scope fence). Confirm the correction is
  adequate or call it.

Write ONE new file: `RP6_CODEX_T0_AUDIT_R11_2026-08-11.md`.
