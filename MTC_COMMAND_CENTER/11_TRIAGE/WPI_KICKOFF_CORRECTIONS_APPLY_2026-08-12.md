# WP-I Claude Pro kickoff corrections — application report

Date: 2026-08-12  
Gate: T2 documentation/evidence edit  
Writable scope: the six paths authorized by `KICKOFF_CODEX_KICKOFF_CORRECTIONS_2026-08-12.md`

## Result

Every current-state finding in
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_CLAUDEPRO_KICKOFF_PREFLIGHT_2026-08-12.md` is applied. The four
kickoffs changed. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/STATUS_TRANSPORT.md` already
contained the separately requested minimal correction in the current checkout, so it was
verified against both round-6 verdicts and preserved byte-for-byte.

Before the first kickoff edit, all referenced sizes and SHA-256 values were independently
re-derived from current files with `Get-FileHash -Algorithm SHA256` and file length. The historical
r16 `SELF_QA_RP6.md` identity was re-derived from the `753894ba` blob in memory; the pre-repair
Transport blob `61696132a5f2fce97aad4054d41a780297ff21a1` was likewise read and hashed in memory.
There was no disagreement with the preflight values, so no identity item was stopped.

## Transport findings

1. `TRANSPORT_CODEX_R6B_CONFIRM` shorthand → **APPLIED**. It is now
   `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_CODEX_R6B_CONFIRM_2026-08-11.md` in the
   opening role paragraph.
2. Missing audited-byte identity → **APPLIED**. The `Bytes under audit` section now contains the
   exact seven-row table from the preflight for `run_p0.sh`, `run_ro.sh`, `transport_runner.ps1`,
   `TRANSPORT_PLAN.tsv`, `remote_setup_wpi.sh`, `remote_extract_verify_wpi.sh`, and
   `remote_close_tree_wpi.sh`, with full repo-relative paths, byte sizes, and full SHA-256 values.
3. Claim-audit source shorthand → **APPLIED**. The documentary-defect section cites
   `MTC_COMMAND_CENTER/11_TRIAGE/WPI_SELFQA_CLAIM_AUDIT_TRANSPORT_PATHSCOPE_2026-08-12.md`.
4. “Five claims” count → **APPLIED**. The prompt now says the source raised **four Transport
   findings — `F-1`, `F-2`, `U-1`, `U-2`** and separates the Pathscope findings.
5. Incomplete harness invocation → **APPLIED**. Audit-contract item 1 identifies checked-in
   `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/_r5_wsl_fixtures.sh` as 21221 B with SHA-256
   `a2bb6f6e3c0022aa001db7adb58189649acab9b23b522dc0544b018f9ce7971b`, instructs the auditor to
   materialize blob `61696132a5f2fce97aad4054d41a780297ff21a1` as
   `<scratch>/r6/pre/remote_close_tree_wpi.sh`, and then says: **“Then pass that directory as the
   harness's second argument.”** The instruction cites
   `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_R6_REPORT_2026-08-11.md:269-272`.
6. Working-directory path precision → **APPLIED**. The status, self-QA, source audit, harness,
   report, seven target, and prose references use full repo-relative paths. The pre-repair blob's
   28756 B/full SHA-256 identity is tied to
   `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_TRANSPORT.md:2329`.

The Transport delta gate was not touched; its suffix is byte-identical to HEAD.

## RP7 findings

1. Codex verdict shorthand → **APPLIED**. It is now
   `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_CODEX_T0_AUDIT_R9_2026-08-11.md`.
2. Missing current identity and nonexistent report → **APPLIED**. The prompt pins
   `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh` at 108301 B / SHA-256
   `0e93f90de7fcefe86fee4137f3ba11ea34b69b120d6a06c304fdde0e9b921e62`, and the reading order
   now names the existing
   `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_REPAIR_R9_REPORT.md`.
3. Claim-audit source shorthand → **APPLIED**. It now cites
   `MTC_COMMAND_CENTER/11_TRIAGE/WPI_SELFQA_CLAIM_AUDIT_RP7_2026-08-12.md`.
4. Extractor contradiction → **APPLIED** with the required exact wording: **“Use the published
   `sed|bash` extractor exactly; do not retype or invent an ad-hoc extractor.”** The exact
   published command is reproduced and cited to
   `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md:177-182`.
5. Working-directory path precision → **APPLIED**. Status, self-QA, repair report, and Codex
   verdict references are full repo-relative. The one bare `SELF_QA_RP7.md` is retained only
   inside the exact published command, whose required working directory is stated in full.

The RP7 delta gate was not touched; its suffix is byte-identical to HEAD.

## RP6 findings

1. r16/current-r17 acceptance contradiction → **APPLIED** with the required exact text:
   **“Codex r16 PASS-WITH-NITS covers the unchanged `RP6-P0.sh` and the historical r16 evidence
   only; it does not fill a current-r17 flagship slot. Claude Pro is a fresh independent auditor
   of r17, but not yet the second of two current-byte acceptances.”** The prior verdict is cited
   as
   `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6_CODEX_T0_AUDIT_R16_2026-08-12.md`.
2. Stale R16 producer citation → **APPLIED**. The current producer is cited as
   `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP6.md:17925`.
3. False presentation of six/zero as measured → **APPLIED** in the round-17 explanation and
   first-class question 4 with the required wording: **“r17 asserted six R16 literal-zero fields;
   both the six and `r17_literal_zero_measurements=0` were literals, not measurements; the current
   count is indeterminate pending a measured scan.”** The withdrawal is cited to
   `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/STATUS_RP6_P0.md:53-71`.
4. Round-report source shorthand → **APPLIED**. It is now
   `MTC_COMMAND_CENTER/11_TRIAGE/WPI_ROUND_REPORT_CLAIM_AUDIT_2026-08-12.md`.
5. Moved status placeholder → **APPLIED**. The prompt now identifies
   `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/STATUS_RP6_P0.md:299`.
6. Unfilled-slot source shorthand → **APPLIED**. It is now
   `MTC_COMMAND_CENTER/11_TRIAGE/WPI_UNFILLED_SLOT_SWEEP_2026-08-12.md`.
7. Missing S-1 known defect → **APPLIED**. The new fourth-priority section discloses the global
   every-fence/no-temp scope contradiction and cites
   `MTC_COMMAND_CENTER/11_TRIAGE/WPI_SELFQA_CLAIM_AUDIT_RP6_2026-08-12.md:75-87` plus the named
   `SELF_QA_RP6.md` evidence sites.
8. Missing U-4 known defect → **APPLIED**. The same section states that broad whole-session
   no-host/no-network/no-Git/no-write negatives are author attestations, not transcript-proved,
   and cites
   `MTC_COMMAND_CENTER/11_TRIAGE/WPI_SELFQA_CLAIM_AUDIT_RP6_2026-08-12.md:136-142` plus its
   representative evidence sites.
9. “Those three positions” after eleven positions → **APPLIED**. It now says **“those eleven
   positions.”**
10. Missing F-2 source → **APPLIED**. The third-priority section cites
    `MTC_COMMAND_CENTER/11_TRIAGE/WPI_SELFQA_CLAIM_AUDIT_RP6_2026-08-12.md:63-71`.
11. False dual-acceptance close → **APPLIED** with the required exact text: **“accepting the Claude
    verdict fills the current-r17 Claude slot only; dual acceptance still requires a fresh
    `gpt-5.6-sol` xhigh audit of the r17 evidence.”** It cites
    `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:24-26`
    and explicitly notes that the matrix's line-25/line-26 inconsistency must be reconciled.
12. Shorthand path mapping → **APPLIED**. All mapped status, self-QA, round-report, audit, sweep,
    and claim-audit references are full repo-relative. Shorthand inside the two exact replacement
    sentences remains because the preflight required that wording verbatim; the same artifacts
    are pinned with full paths immediately around those sentences.

The RP6 title and current-round text marked fixed/correct by the preflight were preserved. The
RP6 delta gate was not touched; its suffix is byte-identical to HEAD.

## Pathscope findings

1. Claim-audit source shorthand → **APPLIED**. It now cites
   `MTC_COMMAND_CENTER/11_TRIAGE/WPI_SELFQA_CLAIM_AUDIT_TRANSPORT_PATHSCOPE_2026-08-12.md`.
2. Missing historical-pin disclosure → **APPLIED** in both the round-2 state and audit-contract
   item 1. The prompt labels the four real-block runs **HISTORICAL PINNED REGRESSIONS**, states
   they are explicitly not current RP6/RP7 coverage, identifies the pinned RP6/RP7 bytes, and
   requires the verdict to preserve that scope.
3. Working-directory path precision → **APPLIED**. Self-QA, status, repair report, Codex audit,
   GLM audit, parent audit, and current artifact references use full repo-relative paths.

The Pathscope tier remains T1/high as marked fixed/correct by the preflight. The Pathscope delta
gate was not touched; its suffix is byte-identical to HEAD.

## Extra STATUS_TRANSPORT item

STATUS_TRANSPORT staleness → **APPLIED IN CURRENT BYTES; VERIFIED AND PRESERVED**. The header is
`CODEX-FLAGSHIP-ACCEPTED — PENDING SECOND FLAGSHIP`. The opening round-6/6b entry records:

- `TRANSPORT_CODEX_R6_AUDIT` = `REQUEST_CHANGES` on the false nine-file unchanged claim;
- the claim repaired to the seven executable/plan targets;
- `TRANSPORT_CODEX_R6B_CONFIRM` = `PASS` at commit `7e4b5e9f`, closing the Codex slot; and
- only the Claude flagship slot remains pending.

Those claims were checked directly against
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_CODEX_R6_AUDIT_2026-08-11.md` and
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_CODEX_R6B_CONFIRM_2026-08-11.md`.
Because the minimal requested state was already present and `STATUS_TRANSPORT.md` had no working-
tree diff, no redundant rewrite was made.

## Final identities and execution statement

| Owned existing file | Final bytes | Final SHA-256 | Working-tree result |
|---|---:|---|---|
| `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/KICKOFF_CLAUDEPRO_TRANSPORT_2NDFLAGSHIP_AUDIT.md` | 9548 | `8b0bc0aa2a51072aa22e8afc063250b94e192ba49aa70d5ee29a34b785b9b6f3` | modified |
| `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/KICKOFF_CLAUDEPRO_RP7_2NDFLAGSHIP_AUDIT.md` | 7679 | `5e6c63851415d01c998baa5c9eaa7107767c5445123327189a7212cb96e4abc7` | modified |
| `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md` | 17558 | `66ed271b6eda1d09a284592aee53e9a51d0712cfa7e6b87e86041d6ced3951ce` | modified |
| `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/KICKOFF_CLAUDEPRO_PATHSCOPE_EXECUTION_AUDIT.md` | 8459 | `19c6418b2c3cd04f419f702f4b4ee118677339f187506c3ec0c0cb638d5d11eb` | modified |
| `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/STATUS_TRANSPORT.md` | 24405 | `9b0871aff9c3c8434f7e4461d241168b9d0f66b6bad69f3eac9f4d9d46941ef3` | verified, unchanged |

This report is the sixth owned path and the hashing record; its own final byte count and SHA-256
cannot be embedded without changing that identity, so they are reported by the Lead alongside
this file at handoff.

No harness, WSL fixture, or remote-host action was run for this correction task. **Lead
attestation:** no Git state was mutated: no add, commit, checkout, reset, stash, branch change,
push, or other Git write occurred. Git use was read-only (`status`, `diff`, `show`, `log`, and
`cat-file`).

Actual Lead session header: **model `gpt-5.6-sol`; effort `xhigh`** (Codex `fourth`). Gates 3–4
were delegated under the mandatory two-tier rule to the available Claude Max reserve route with
the command requesting `claude-opus-5` / `xhigh`; the implementer output confirmed
`claude-opus-5` but did not independently echo an effort field.
