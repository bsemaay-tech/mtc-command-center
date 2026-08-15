# RP7 R1-R4 Codex T0 audit — 2026-08-15

## Verdict

**PASS**

No required repair and no optional nit were found in the frozen candidate.
This is the independent Codex T0 verdict only; repository acceptance still
requires the separately mandated fresh Claude flagship verdict. I did not read
that verdict or its kickoff for this round.

## Auditor, scope, and safety

- Auditor: fresh independent `gpt-5.6-sol`, effort `xhigh`, T0.
- Candidate commit: `80cbed461d0b0371e6eabbfff0e732e5001affaf`.
- Audit checkout: `C:\R7T0CDX` only.
- The required rules, repair authority, prior cap-override verdicts, owner
  boundary, Lead verification, defect-pattern catalogue, and all four frozen
  artifacts were read in full.
- Frozen Git-object bytes were materialized in run-owned Linux scratch. No
  candidate artifact was executed from mutable worktree bytes.
- No network, host/service mutation, deployment, credentials, broker/exchange,
  ARM, order, TESTNET/mainnet, Pine, parity, MTC, or trading action occurred.

## Frozen identity

All four objects re-derived from candidate Git objects matched the kickoff
freeze before and after execution:

| artifact | bytes | SHA-256 |
|---|---:|---|
| `RP7-WPI-RO.sh` | 137981 | `4caed4aecc91cada3b8b99f8ff06d7ba0d7376b2bc07e92c298f4a7b7ca0900c` |
| `SELF_QA_RP7.md` | 585132 | `b1031cc5e71f2a19e05a400a0d3754b9cf37b5917848868e61ae0764a5b1c8ae` |
| `STATUS_RP7.md` | 19165 | `f1fbe2e1d8381b2c5d762e6c69fff2718b7f90ae8d09e8b32d1947fab8ea5a46` |
| `RP7_ROWS_1_9_REPORT_2026-08-13.md` | 54481 | `0a434a98393a6c8ecf41a01d6696326c814c44bf69a5d51734f1b44cbe738c46` |

The extracted rows-1-9 fence was 115657 bytes with SHA-256
`b64c23ebcc85dece217a2128c069b7d4074cc763533319edb8a25ecf2dc06fbb`;
`bash --noprofile --norc -n` returned rc 0. The production script was LF-only,
had zero CR bytes, and remained byte-identical after the audit runs.

## Mandatory independent execution

Environment: WSL Ubuntu, Bash `5.3.9`, Python `3.14.4`, and real systemd
`259 (259.5-0ubuntu3)`.

I ran the complete frozen rows-1-9 fence twice, sequentially, with separate
run-owned scratch and retained raw evidence:

| run | rc | elapsed | published bytes / lines | published SHA-256 | stderr |
|---|---:|---:|---:|---|---:|
| 1 | 0 | 198 s | 54284 / 250 | `d0788122c132e43c25aea52315d53b3596c40c57598e2bbded9b2efa11cae8ab` | 0 B |
| 2 | 0 | 198 s | 54284 / 250 | `d0788122c132e43c25aea52315d53b3596c40c57598e2bbded9b2efa11cae8ab` | 0 B |

Raw `cmp` of the two published stdout files returned rc 0. No external edit,
replacement, normalization, or exclusion was applied. Both runs reported:

- 43 RED/GREEN pairs and 12 single-subject controls;
- 23 multi-subject RED, 15 multi-subject GREEN, and 65 multi-subject controls;
- seven actual named subjects, 14 systemd oracle fixtures, and 11 environment
  oracle fixtures;
- `result=PASS`, extracted production functions, and
  `block_logic_reimplemented=no`;
- no harness abort, case/subject failure, unexpected stderr, capture collision,
  unadjudicated arm, ERR-trap contamination, or before/after identity drift.

The identical publication did not reuse or conceal runtime identities:

| identity | run 1 | run 2 |
|---|---|---|
| scratch root | `/tmp/rp7_rows_1_9_rebuild_evidence.6iWnh8CH` | `/tmp/rp7_rows_1_9_rebuild_evidence.fDMbweqm` |
| live mount projection | `9e75f7c42499f18680c5ffeb216f7b6202c72301d131a6f94153ef445a494082` | `6f3cd25e26173e9499adbd77d9bae356d2ee7cf717051099b6c6b45b8fcba481` |
| decoy mount projection | `aad3551bb8b61152dd7db840263dd59da3c381f2451cb3608c750fdad2ce72df` | `e5545f98d728756931816f68e424a5cff9c27aa5ff18d272a5213e11618dc9a5` |
| raw transcript SHA-256 | `0caba166edc2276f1bc5c540e8252fb1a68e73b7d1214e71b06a26fa1d55d88c` | `a1901b3e826cd83114d79bf617dea145394417a4cb3683406a504ab9ac98d6ca` |

The retained raw transcripts were 58645 bytes each, compared unequal as
expected, and differed on 262 lines (131 line pairs).

## R1-R4 adjudication

### R1 — production normalization boundary

**Closed.** Eleven live `systemd-analyze verify` fixtures on systemd 259
reproduced quote removal before environment-name validation, including the raw
mid-name double- and single-quote spellings. The frozen `current` subject false
PASSED the normalized mid-name case. The repaired production path cannot do so:
rows 1-7 attest the exact expected unit-source digest only after empty drop-ins
and exact fragment identity are established, and row 9 refuses missing or
mismatched source attestation before parsing effective `Environment`.

The source carrying the mid-name quote produced a different same-size digest
and failed row 7; the clean attested source passed through the real production
caller. A direct raw token injected after normalization was treated only as a
tokenizer control, not as closure evidence. Fully quoted and value-quoted valid
assignments remained accepted. Systemd accepted both duplicate fixtures, while
row 9 intentionally and truthfully enforced its documented stronger policy of
exactly one protected assignment. There is no residual R1 false PASS.

### R2 — chronology and provenance

**Closed.** The chronology table text in `SELF_QA_RP7.md`, `STATUS_RP7.md`, and
the report was byte-identical, with SHA-256
`e366909cf35bd861654cc01c265dcd2e1bc2c16923ae0f9308ecdffcd70a02de`.
It accurately separates the 132886-byte baseline Lead/auditor history from the
137981-byte repair's implementer and Lead runs, and leaves both fresh auditor
slots pending. A targeted search of all four frozen artifacts found no
contradictory `no Lead run`, `none_yet`, premature acceptance, or transferred
verdict claim.

### R3 — literal reproducibility without lost binding

**Closed.** The two raw published outputs compared byte-for-byte equal while
the retained scratch roots, live/decoy mount digests, and raw transcripts were
independently different. The canonicalizer accounted for every replacement and
left no run-root residue.

Independent deliberate falsifications all failed closed:

- expected `%RUNROOT%` count 132 instead of 133: rc 94,
  `HARNESS_CANON_FAIL count_mismatch`;
- frozen mount attestation digest: rc 97,
  `mount_projection_not_rederivable`;
- decoy reusing the real fragment path: rc 97,
  `mount_projection_not_path_sensitive`;
- predicate-relevant internal fragment path changed to `.alt`: rc 96, real
  `RP7_STOP reason=mount_topology_mismatch`, still visible after canonicalization.

Thus canonical presentation neither creates reproducibility by external edits
nor masks an internal identity that a row predicate consumes.

### R4 — systemd bare-CR line termination

**Closed.** Production uses the exact `re.split("\r\n|\r|\n", text)`
terminator model. Fourteen byte-censused fixtures were checked against live
systemd 259. Bare CR, multiple CR, and CR-only files exposed real `[Install]`
sections; CRLF and the backslash/CR boundary controls retained their distinct
semantics.

The bare-CR and multiple-CR regressions ran in separate processes against the
actual frozen/cap-override/round-4/repaired subjects. Frozen subjects false
PASSED the required RED cases; repaired bytes failed them and kept the controls
GREEN. LF/CRLF, trailing-space, odd/even backslash, comment/blank, malformed
header, UTF-8/NUL, and EOF behavior remained explicitly terminal and correct.

Two additional D026 falsifications confirmed test sensitivity:

- changing the bare-CR fixture by one byte: rc 96 with exact
  `fixture_bytes ... expected ... total=88 observed ... total=89`;
- replacing the repaired splitter with a behaviorally equivalent
  CR/CRLF-normalize-then-LF-split expression: rc 96 because the declared
  `mut_nocr` RED no longer failed, proving that regression is sensitive to the
  intended mutant rather than a surrounding literal.

## Thirteen-pattern and adjacent-boundary review

All thirteen catalogue patterns were applied:

1. STOP remained distinct from FAIL and was never accepted as a result.
2. Kernel/tool provenance was explicit for mount data and systemd 259.
3. Full component and mount-bound paths, not leaf names alone, were checked.
4. Privileged-child environment and capture bindings remained constrained.
5. Rows 6 and 9 used grammar-aware parsers rather than grep acceptance.
6. Capture status was resolved before stdout could decide semantics.
7. Readers completed before EOF-dependent decisions were made.
8. Names were backed by bytes, digests, source attestation, and mount identity.
9. Claims stayed within the predicates, including the disclosed duplicate
   policy and canonical-publication limits.
10. Evidence was executable and independently falsified as recorded above.
11. The fence executed extracted production functions and the declared real
    analyzer; it did not substitute a reimplementation.
12. Analyzer omissions did not disappear: source identity, manager
    normalization, terminators, malformed inputs, and raw values were bound by
    explicit complementary checks.
13. Every admitted fixture/subject arm reached an explicit RED, GREEN, CONTROL,
    FAIL, or STOP disposition, with the aggregate counts checked.

Adjacent row-6 and row-9 inspection found no false PASS/FAIL or ambiguous STOP.
Row 6 fails a real `[Install]`, STOPs unreadable/NUL/malformed input, preserves
continuation controls, and keeps the mount window closed. Row 9 requires valid
source attestation before tokenization, STOPs capture/read/attestation/parser
uncertainty, and FAILs only a completed semantic mismatch. Exact-one assignment
counting prevents duplicate ambiguity.

## Final disposition

The frozen 137981-byte candidate satisfies the R1-R4 repair contract and the
mandatory T0 Codex audit requirements. No required repair remains.

**PASS**
