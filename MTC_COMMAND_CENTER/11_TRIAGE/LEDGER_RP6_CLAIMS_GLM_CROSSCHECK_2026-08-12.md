Done. Verdict written to `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6_LEDGER_GLM_CROSSCHECK_2026-08-12.md` (new file — the sibling `RP6_GLM_ADVANCE_READ_AUDIT_2026-08-12.md` was a *different* audit's verdict, the prior RP6-11 `eval` read, so I left it untouched).

## Verdict: ADVANCE-SUPPLEMENTAL, PASS-WITH-NITS — zero required repairs

The RP6 half of the gpt-5.5 freeze-input ledger is **substantively accurate**. Every RP6 claim re-derived from current bytes.

**The consequential claim (Blocker 7) — CONFIRMED.** "RP6 cannot produce an end-to-end P0 PASS with the freeze literals outstanding, so the Codex r16 acceptance was a source/audit acceptance, not a host PASS." Proven as three byte-verified premises:
- **A.** Exactly **17 distinct `P0_FIXED_*` definitions** are set to `<PIN-AT-FREEZE>` (`:266-270` 5 attested + `:278` python + `:289-299` 11 tools). Triple-reconciled: raw count, the status text `freeze_gate_literal_count=17`, and the 12+5 decomposition.
- **B.** The fence refuses markers — `p0_stop` at `:709`, `:724`, `:733-742`. RP6 STOPs (exit 3) before any PASS line.
- **C.** The wrapper hands RP6 exactly those markers (`run_p0.sh:151-155` defines, `:237-240` exports, `:245` sources).

**The 17-vs-27 "discrepancy" — RESOLVED, not a defect.** 17 = distinct freeze-input *definitions*; 27 = total raw *occurrences* = 17 definitions + **10 fence/guard occurrences** (`:607, :615, :645, :709, :724, :733, :735, :737, :739, :741`). The 10 are the load-bearing guard itself. Both counts correct; different referents.

**r16 characterization — CONFIRMED.** r16 was a static census/grammar QA (`PASS-WITH-NITS`, harness summaries `:23-26`) that explicitly made "no host observation" (`:159-161`) and "grants no host/deployment authority" (`:183-185`). The ledger classifies it correctly; r16 never claimed to be a host PASS.

**All RP6-P0.sh consumer line citations verified** (hash unchanged since r16, so stable): `:691-700, :707-724, :733-752, :1390-1393, :1394-1414, :617-623, :632-639, :355-357, :488-515, :759, :1871-1872`.

**The one genuine defect — stale citation (NIT).** The ledger cites `STATUS_RP6_P0.md:311-312`, but that line no longer holds the claim — round 17 + the Lead's status correction shifted it. The claim is now at `:396-397` (recurs ~9×; count field at `:274`). Claim content true; line number stale — exactly the drift the kickoff flagged as likely. Optional fix: repoint to `:396-397`.

Read-only observed: no git mutation, no host/network, no block-byte edit, no acceptance slot closed.
