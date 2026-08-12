Sweep complete. Verdict written to `MTC_COMMAND_CENTER/11_TRIAGE/WPI_STATUS_VS_BYTES_SWEEP_GLM_2026-08-12.md` (read-only; no status file edited, no git mutation, no host, no network).

## Result

**Files swept: 4** — STATUS_RP6_P0, STATUS_RP7, STATUS_TRANSPORT, STATUS_SEC102.
**Findings by class: stale = 1 · wrong = 0.** No false byte identity, no false attribution, no broken cross-reference survived verification.

**14 identities independently re-derived, all match** — the 5 kickoff-anchored current artifacts (RP6-P0.sh 110817/5132bacd…, RP7-WPI-RO.sh 108301/0e93f90d…, composite_pathproof.py 129658/adbf27fd…, pathscope_prover.py 122446/890016f0…, SELF_QA_RP6.md 1038848/07cf843d…), all 7 transport targets, and 2 historical pinned git-blobs (frozen_ro_basis @d6a976aa = 70941/23e55667…, round-8 basis @bb8546e6 = 99903/11621044…). My derivation matches the kickoff's anchors exactly, so the tooling is sound.

**The motivating r17 attribution defect is already corrected** — STATUS_RP6_P0.md, RP6_R17_REPORT, and the run log (`model: gpt-5.5`) all agree.

**Most consequential finding (stale):** `STATUS_TRANSPORT.md` does not reflect the round-6 Codex audit cycle. On disk, `TRANSPORT_CODEX_R6_AUDIT` = REQUEST_CHANGES on a false *"nine-file unchanged"* byte-identity claim at SELF_QA_TRANSPORT.md:2665, and `TRANSPORT_CODEX_R6B_CONFIRM` = PASS (commit `7e4b5e9f`, closing the Codex slot). The header still reads `REPAIRED-PENDING-REAUDIT` and the body never mentions it — the status was edited 2026-08-12 (owner ratification) without incorporating the audit. The false claim itself is already repaired in the bytes (now correctly scoped to "seven targets"). The remaining-pending item is genuinely the Claude flagship slot, so this is stale (understated), not wrong.

Two verified reconciliations worth noting: `freeze_gate_literal_count=17` is correct (17 distinct pinned inputs; the Lead's "27" is raw string occurrences incl. 10 guards — both right, different counts), and the R15:180 line citation is accurate (the `@@REPORT_EXEC_BLOCK@@` placeholder is exactly there).

One observation, not a defect: `RP6_R16_MAX_RUN_2026-08-12.log` is 0 bytes, so the r16 implementer attribution can't be machine-verified from its log — and Claude/Max run logs generally lack model headers, so the attribution cross-check is cleanly executable only on the Codex side.
