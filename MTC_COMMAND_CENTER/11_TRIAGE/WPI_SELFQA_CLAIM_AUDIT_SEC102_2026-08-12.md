# WPI SELF-QA claim audit - SEC102

Date: 2026-08-12
Analyst: Codex

Audited document: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/SELF_QA_SEC102_R11.md`

Method: documentary consistency only, following the RP7 prose-vs-transcript method. I did not run any harness, did not edit the audited document, and did not perform any git mutation.

Audit tier classification: T2 evidence/document audit. This file is the single requested audit artifact.

## Sections Covered

Covered the header and sections 0-13, including every pasted `text` transcript block and the prose immediately interpreting each block. No section was intentionally skipped.

Trusted-base assumptions treated as disclosed owner-accepted assumptions, not findings: outer Python runtime, PATH-resolved `powershell.exe`, on-disk-vs-clone byte identity, and interpreter vocabulary.

## Output Lines Checked For Non-Measurements

I checked 375 pasted output lines across all `text` transcript blocks: lines 394-444, 554-612, 685-710, 889-930, 1086-1094, 1247-1256, 1366-1395, 1467-1473, 1574-1592, 1628-1648, 2592-2635, 3258-3312, and 3337-3338.

I found no `dynamic_targets=0`-style hardcoded output constant masquerading as a measurement. I did not classify explicitly labelled expectation fields such as `EXPECTED=`, `EXPECTED_KILLS=`, `WANT=`, or `TOKEN=` as measurement claims.

## Findings By Class

### False

F-1 - Section 1 undercounts what the `M2` kickoff-safe-set mutation admits.

- Claim: `SELF_QA_SEC102_R11.md:213-214` says mutation `M2` "shows two round-7 REDs returning to `PASS`."
- Transcript evidence: `SELF_QA_SEC102_R11.md:912` shows `M2_kickoff_safe_set_at_r6_bounds` with `OBSERVED_KILLS=['novel', 'xg_at', 'xg_plus']`, i.e. three killed REDs.
- Classification: false.

F-2 - Section 2 explains `NEWLY_CLOSED_BY_R7=10` with a nine-item subcount.

- Claim: `SELF_QA_SEC102_R11.md:447-449` says the ten newly non-silent forms are "the three extglob classes in six spellings and the three unenumerated characters."
- Transcript evidence: `SELF_QA_SEC102_R11.md:443` reports `NEWLY_CLOSED_BY_R7=10`; the rows at `SELF_QA_SEC102_R11.md:394-408` show seven newly closed extglob-related spellings (`xg_plus`, `xg_at`, `xg_bang`, `xg_relative`, `xg_after_assign_prefix`, `xg_after_named_fd`, `xg_in_function_body`) plus three novel-character rows.
- Classification: false.

F-3 - The evidence map overstates the RED-before-GREEN result for every new RED.

- Claim: `SELF_QA_SEC102_R11.md:240` says "Each new RED was `PASS` on the audited code and is `STOP` now."
- Transcript evidence: `SELF_QA_SEC102_R11.md:701-704` shows `red_render_extglob_qmark_command_word.json` as `ROLE=CARRIED_STOP` with `EXPECT_90868b86_RC=3 GOT=3` and `EXPECT_R7_RC=3 GOT=3`; `SELF_QA_SEC102_R11.md:709` reports only `RC_LEVEL_NEW_REDS=4`.
- Classification: false.

F-4 - Section 5 says every round-7-fence-removal mutation leaves the `relative` RED intact, but `M4` kills it.

- Claim: `SELF_QA_SEC102_R11.md:933-935` says every mutation that removes a round-7 fence leaves the round-6 `param`/`substitution`/`relative` REDs intact.
- Transcript evidence: `SELF_QA_SEC102_R11.md:918-919` shows `M4_full_round6_classifier` has `OBSERVED_KILLS=['novel', 'relative', 'xg_at', 'xg_bang', 'xg_plus']` and the row includes `relative=KILLED`.
- Classification: false.

F-5 - Section 7 misstates the character universe size.

- Claim: `SELF_QA_SEC102_R11.md:1103-1104` says round 7 sweeps "all 95 printable ASCII characters plus a non-ASCII sample."
- Transcript evidence: `SELF_QA_SEC102_R11.md:1250` reports `SWEEP_CHARS=101 BASES=6 POSITIONS=4 VARIANTS=1919`, so the pasted transcript does not support a 95+1 universe.
- Classification: false.

F-6 - Section 8a says no form moved, but the transcript's own note says one did.

- Claim: `SELF_QA_SEC102_R11.md:1398-1399` says "both round-6 disclosed stops are unchanged" and "No form moved between round 6 and round 7 in this battery."
- Transcript evidence: `SELF_QA_SEC102_R11.md:1390-1393` shows one row with `NOTE MOVED: round-5 control rc 0 -> round-7 disclosed conservative stop` and one row with `NOTE CARRIED: round-5 disclosed false stop, unchanged`.
- Classification: false.

### Unsupported

U-1 - Header prior-audit verdict and reproduction claims are external-reference-only.

- Claim: `SELF_QA_SEC102_R11.md:3-6` says `SEC102_CODEX_T1_AUDIT_R10_2026-08-12.md` returned `REQUEST_CHANGES`, closed earlier items after independently reproducing every number, and conserved every earlier SEC102 verdict.
- Transcript evidence: no supporting transcript line exists in this document; the only support is the referenced external audit file name.
- Classification: unsupported.

U-2 - Cross-round byte-identity and carried-record claims are not proved by the pasted transcript here.

- Claim: `SELF_QA_SEC102_R11.md:17-22` says every sections 1-12 `powershell` block is byte-identical to `SELF_QA_SEC102_R10.md`; `SELF_QA_SEC102_R11.md:149-152` says every classification/reason/rc/transcript in sections 2-12 is the round-7 record re-run; `SELF_QA_SEC102_R11.md:1657-1659` says every byte above is the round-7 table unchanged.
- Transcript evidence: no transcript line compares the carried blocks or artifact table against R10/R7 bytes. `SELF_QA_SEC102_R11.md:3312` proves the current document's 11 blocks were executed and matched their pasted lines; it does not prove byte identity to prior documents.
- Classification: unsupported.

U-3 - Prior-round closure claims are not supported inside this document.

- Claim: `SELF_QA_SEC102_R11.md:171-172` says rounds 4, 5, and 6 closed specific earlier classes; `SELF_QA_SEC102_R11.md:1855-1860` says round-6, round-7, and round-8 findings were closed and confirmed by Codex r7/r8/r9.
- Transcript evidence: no supporting closure/confirmation transcript line exists in this document. The current pasted transcript supports current reruns and mutations, but the named Codex confirmation records are external.
- Classification: unsupported.

U-4 - Section 6 says all 77 per-form lines are reproduced, but they are not pasted.

- Claim: `SELF_QA_SEC102_R11.md:1083` says "all 77 per-form lines end `OK` and are reproduced by the command."
- Transcript evidence: the pasted output at `SELF_QA_SEC102_R11.md:1086-1094` contains only the seven `BOUNDARY` rows plus the summary `TABLE_FORMS=77 CARRIED_MOVED=6 BOUNDARY_FORMS=7 OFF_EXPECTATION=0`. The 77 per-form transcript lines are not present here.
- Classification: unsupported.

U-5 - The `pathscope_prover.py` pin claim is not present in the identity transcript.

- Claim: `SELF_QA_SEC102_R11.md:1662-1664` says `pathscope_prover.py` was not touched and its `122446 B / 890016f0...` pin is unchanged, with section 3 FREEZE GREEN transcripts as proof.
- Transcript evidence: no line in the identity output at `SELF_QA_SEC102_R11.md:1628-1648` prints `pathscope_prover.py`; the section 3 GREEN rows at `SELF_QA_SEC102_R11.md:589-590` do not print that file's bytes or SHA-256 either.
- Classification: unsupported.

U-6 - The final-byte re-derivation claim lacks a supporting transcript line.

- Claim: `SELF_QA_SEC102_R11.md:3341-3342` says the section-13d transcript was re-derived on the final bytes of the file after the last prose edit and is byte-identical to the published run.
- Transcript evidence: `SELF_QA_SEC102_R11.md:3337-3338` gives only `OUTER_WRAPPER_RC=0` and `OUTER_WRAPPER_STDERR_BYTES=0`; no transcript line records a second run identity, final-file digest, or byte-identical comparison against the earlier section-13d output.
- Classification: unsupported.

### Scope-Wrong

S-1 - The summary says every published block was run through both channels, but the transcript proves 10/11 plus one self-exclusion.

- Claim: `SELF_QA_SEC102_R11.md:138-140` says every published block's rc/stderr/stdout contract is conserved and every block is run both ways.
- Transcript evidence: `SELF_QA_SEC102_R11.md:2621-2630` lists channel-contract rows only for blocks 01-10, and `SELF_QA_SEC102_R11.md:2634` reports `CHANNEL_CONTRACT_CONSERVED=10 CHANNEL_CONTRACT_SELF_EXCLUDED=1`. The later prose at `SELF_QA_SEC102_R11.md:1952-1955` discloses the self-exclusion, but the earlier summary overstates the scope.
- Classification: scope-wrong.

## Most Consequential Finding

S-1 is the most consequential finding. The round-11 channel contract is central to the accepted SEC102 evidence, and the top-level prose says every block was run both ways while the actual transcript proves a narrower 10/11 contract plus one self-excluded block. The self-exclusion is honestly disclosed later, so this is a scope-word defect, not a hidden harness defect.
