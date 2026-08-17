# KICKOFF — Codex T2: Audit-2 readiness-package refresh round 1 (close the 20 NEEDS-UPDATE items)

You are Codex `gpt-5.6-sol` xhigh, EDITOR (T2 documentation coherence). Working dir
`C:\LAB\Tradingview_LAB_CLEAN`. Your own coherence review
`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_COHERENCE_CODEX_2026-08-10.md` returned
`NEEDS-UPDATE: 20 items` (9 stale claim groups + 11 missing-material packets). This round
updates the package IN PLACE to the 2026-08-12 midday state. Edit ONLY files inside
`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/`. No git mutation (the Lead
commits), no host, no network, no execution of any block or harness. Do not touch block
files, SELF_QA files, STATUS files, prereg drafts, or anything outside the package dir.

## Current truth to normalize the package against (2026-08-12 ~11:00, Lead-supplied)

- **Codex flagship acceptances: 3/5.** RP6-P0 (`RP6_CODEX_T0_AUDIT_R16`, PASS-WITH-NITS —
  exact-byte-span census fixpoint; `RP6-P0.sh` UNCHANGED since r10a, 110817 B, SHA-256
  `5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330`), RP7-WPI-RO
  (`RP7_CODEX_T0_AUDIT_R9`, PASS — descriptor-bound status body, `wpi_alloc_leaf` deleted),
  transport (`TRANSPORT_CODEX_R6B_CONFIRM`, PASS).
- **Second flagship (Claude Pro, fresh non-implementer) audits are scheduled tonight
  2026-08-12 23:00+** for transport, RP7, RP6, plus the pathscope EXECUTION-audit. Until
  those verdicts exist, NONE of the three executable sets has dual-flagship acceptance —
  the package must say so and must reference the four pre-written kickoffs
  (`KICKOFF_CLAUDEPRO_{TRANSPORT,RP7,RP6}_2NDFLAGSHIP_AUDIT.md` in `WPI_BLOCKS_DRAFT/`,
  `KICKOFF_CLAUDEPRO_PATHSCOPE_EXECUTION_AUDIT.md` in `WPI_PREREG_DRAFT_ROUND1/`).
- **SEC102 composite pathproof:** both original CRITICALs closed + Codex-verified;
  command-word WHITELIST inversion confirmed a fixpoint (r7); r8 closed the child-completion
  finding; ONE MEDIUM remains (r8 audit: §13 wrapper LF→CRLF text-mode write vs byte-for-byte
  claim), r9 repair in flight today; then Codex r9 audit closes the Codex slot; GLM-5.2
  second opinion (T1, >300 lines) follows. Interpreter-vocabulary residual is OWNER-RATIFIED
  2026-08-12 as a disclosed production-gate item (do not present as open defect).
- **Pathscope prover r2:** `pathscope_prover.py` 122446 B, SHA-256 `890016f0…`; 9+5
  silent-sink classes closed; finding-6 = honest `ALLOW-LEXICAL` disclosure + residual R1.
  Codex is FILTER-BLOCKED on the source (tooling blocker, on record); GLM read-audit
  favorable but SUPPLEMENTAL; Claude Pro execution-audit tonight.
- **Successor prereg:** R3 merged (`WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md`), 34/34
  conserved. MC-01..03 RESOLVED by owner ratification 2026-08-12 (FAM-01 twelve exact P0
  tool pins no PATH fallback; FAM-02 exact venv root; FAM-03 frozen-composite evidence-root
  derivation) — adjudication `LEAD_MC_ADJUDICATION_2026-08-11.md`. Implementation in the
  frozen composite remains a freeze gate. Transport F1 (outer SSH account-shell boundary)
  OWNER-RATIFIED accept-with-disclosure: honestly OPEN, NOT a freeze blocker.
- **Rows 1–9:** owner decision stands — BUILD ALL NINE, applied only AFTER RP7 dual
  flagship acceptance.
- **Ledger:** ~40 h used of 50 (ESTIMATE, needs owner ratification; owner waived the
  10h-remaining stop gate 2026-08-11 with honest booking). Replace the stale 26.9 h figure.
- **Audit-tier policy stands:** Audit 2 is T0, exactly `claude-opus-5` + `gpt-5.6-sol`,
  both fresh + xhigh; GLM never silently added → close OPEN_QUESTIONS question 1.
- Audit 2 still cannot precede WP-I closure; the honest-start condition of the coherence
  review is unchanged. The ordering corrections in that review (§Ordering) must be applied
  verbatim: Audit 2 audits an already frozen SHA; the WP-I segment shows the blockers and
  the separate Stage-1 freeze.

## Contract
1. Work through all 9 stale claim groups: replace each quoted stale sentence with current
   truth (above), keeping every honest limitation. For item 7, replace the obsolete
   `UNLOCATED` rows in `AUDIT2_D026_RED_LOCATIONS.md` with the corrected per-case locations
   from the file's own Lead correction; genuinely unlocated rows stay supplemental.
2. For the 11 missing-material packets: where material now EXISTS (per-artifact acceptance
   matrix data above, §10.1 delta now in prereg R3, prereg review state, MC resolutions),
   write the packet or a stub that points to the exact current artifact + what is still
   missing. Where material genuinely cannot exist yet (WP-I execution evidence, frozen-SHA
   bundle, freeze-input ledger), keep an explicit NOT-YET-AVAILABLE packet — do not
   fabricate.
3. Every updated claim carries the date tag `[refreshed 2026-08-12]`.
4. Add one new file `AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md` in the package dir: per
   artifact (RP6, RP7, transport, SEC102, pathscope, prereg) — exact bytes/identity, latest
   verdict per auditor, what acceptance is still missing. Tonight's Claude verdicts will be
   appended by the Lead; leave a clearly marked PENDING row per artifact.
5. Finish with a short changelog section at the top of `AUDIT2_HANDOFF_PACKAGE.md` listing
   which of the 20 items are CLOSED by this refresh and which remain OPEN (with reason).
   Do NOT claim the package is dispatchable — it is not, until WP-I closes.

Print a summary of files changed + items closed/open when done.
