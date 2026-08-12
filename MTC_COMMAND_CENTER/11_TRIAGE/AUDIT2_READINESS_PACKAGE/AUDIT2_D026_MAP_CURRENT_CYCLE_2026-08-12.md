# Audit 2 D026 map — current WP-I cycle

Date: 2026-08-12  
Audit tier: T2 documentation/evidence map  
Scope: RP6-P0 rounds 10-16, RP7-WPI-RO round 9, transport rounds 4-6b, SEC102 rounds 7-11, and pathscope prover round 2.

This map counts one row per named finding or closure-test family, not one row per control arm inside a family. An aggregate harness may therefore appear in several rows with a different load-bearing output signature. A row is fully closed only when a literal RED and GREEN are located, the pre-fix/mutant identity is explicit, and the GREEN is tied to the final bytes. Helper-only or non-literal evidence is supplemental. `Lead-run`, `auditor-reproduced`, and `author-claimed` describe the strongest execution provenance actually published; this map did not rerun the harnesses.

The final worktree identities below are unchanged from the cited accepted/audited anchors. No claim here grants freeze, host, deployment, credential, ARM, broker, order, or trading authority.

## RP6-P0

Final GREEN subject: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6-P0.sh`, 110817 B, SHA-256 `5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330`. The block bytes are unchanged throughout the r11-r17 census hardening sequence.

**Evidence-document identity — UPDATED 2026-08-12 ~15:45 (round 17).** `SELF_QA_RP6.md` is now **1038848 B, SHA-256 `07cf843d5f00bef7f980017cbe01e0dc63ddb95dce5c7253d9e9a351b0d449ac`** at commit `671d9b40`. The previously recorded round-16 identity (1024538 B, `897a5a4d92b71ca626e73a75700f60db714e5b100339205b0d40d4c36431597b`, byte-identical to the r16 audit anchor `753894ba`) is retained here as history: it is the document Codex accepted in `RP6_CODEX_T0_AUDIT_R16`, and no r16-anchored claim carries forward to the new bytes without re-audit. Round 17 added §ROUND 17 only; the block is untouched. This discrepancy was surfaced independently by `WPI_GITATTRIBUTES_DURABILITY_ANALYSIS_2026-08-12.md` while r17 was being committed.

For marker `X`, the exact invocation is `sed -n '/^# X_HARNESS_BEGIN$/,/^# X_HARNESS_END$/p' SELF_QA_RP6.md | bash --noprofile --norc`, from `WPI_BLOCKS_DRAFT`.

| ID | Closure test | Exact RED command and output signature | Exact pre-fix or mutation identity | Exact GREEN command and output signature | Final GREEN bytes | Provenance / disposition |
|---|---|---|---|---|---|---|
| RP6-01 | R10 F4 internal-binding reason | `X=R10_F4`; RED arms emit `F4_RED ... mutation=removed_rc3_precheck ...`; rc 0 for the self-checking harness | Current block with the omission loop and count check neutralized by the published `removed_rc3_precheck` substitutions | Same command; `R10_F4_QA_SUMMARY cases=16 pass=16 fail=0 result=PASS` | RP6 final subject above | Auditor-reproduced through r16; fully closed for the three executed input classes only. |
| RP6-02 | R10 alternate quoting and correlated-tuple relabel | `X=R11_F1_RED`; the harness runs the published r10 fence over the single-quoted emitter and `identity_unexpected` relabel mutants; r10 certifies them | One reachable valid single-quoted `p0_stop` spelling; separately one exact tuple relabel from `account=gatea` to `account=mtc-bridge` | Same command; `R11_F1_RED_SUMMARY cases=17 pass=17 fail=0 result=PASS` | RP6 final subject above | Auditor-reproduced; fully closed for these two mutations. |
| RP6-03 | R10 unknown printable GNU `stat -c %F` result | `X=R11_F3`; RED is the r10 catch-all mapping an unknown printable token to host-state rc 1 | Exact pre-fix classifier `*) P0_FKIND="other"` for an unrecognized successful-producer token | Same command; unknown leaf/followed tokens STOP rc 3 and `R11_F3_QA_SUMMARY cases=85 pass=85 fail=0 result=PASS` | RP6 final subject above | Auditor-reproduced; fully closed. |
| RP6-04 | R9 RED recipe status masked by cleanup | `X=R11_R9RED`; `R9_GRAMMAR_SUMMARY cases=5 pass=2 fail=3 result=FAIL`, `R9_RED_RC=1`, while the old whole recipe returned 0 | Published r9 RED recipe with `rm -f "$mutant"` as its last command | Same command; process rc 1 and `R9_RED_VERDICT status_preserved_across_cleanup exit=1` | RP6 final subject above | Auditor-reproduced; fully closed. |
| RP6-05 | Own-status guard discrimination | `X=R11_GUARDS`; each published fence is falsified by inserting `COUNTER=7` immediately before its real guard; each mutant returns nonzero | Exact marker-extracted fences, one adjacent forced-counter substitution per fence | Same command; the round-16 audit reproduced `R11_GUARDS_SUMMARY fences=25 pass=25 fail=0 result=PASS` | RP6 final subject above | Auditor-reproduced; fully closed. |
| RP6-06 | R11 fragmented command word | `X=R12_F1_RED`; the r11 fence certifies the valid reachable `p0_s""top` command word | One insertion after `p0_probe_kind() {`: `[ -z "${P0_R11_CMDQUOTE_MUTANT:-}" ] || p0_s""top "r11_cmdquote detail=quoted_command_word"` | Same command; `R12_F1_RED_SUMMARY cases=33 pass=33 fail=0 result=PASS` | RP6 final subject above | Auditor-reproduced; fully closed for this construct. |
| RP6-07 | R12 alias/function and `command`/`builtin` prefix escapes | `X=R13_F1_RED`; r12 is blind to the published `alias`, `shadow`, `cmdprefix`, and `toolshadow` mutants | Four exact published r13 mutants, mechanically extracted by the harness | Same command; r13 catches all four directions and `R13_F1_RED_SUMMARY cases=35 pass=35 fail=0 result=PASS` | RP6 final subject above | Auditor-reproduced; fully closed for the four published classes. |
| RP6-08 | R13 extractor conservation | `X=R14_F1_RED`; r13 is blind to the published `funckw`, `prefixkw`, `aliasopt`, `aliasdef`, `invpartial`, and `invempty` classes | Six exact published r14 mutants: non-parenthesized function keyword, prefix shadow, constructed alias controls, and partial/empty inventory | Same command; `R14_F1_RED_SUMMARY cases=57 pass=57 fail=0 result=PASS` | RP6 final subject above | Auditor-reproduced; fully closed for the six published classes. |
| RP6-09 | R14 definition/inventory multiplicity | `X=R15_F1_RED`; r14 is blind to `defcont`, `defmulti`, `invappend`, `invdup`, and `wrapline` | Five exact published r15 mutants: continued definition name, same-line multiplicity, append assignment, duplicate composition, and after-body append | Same command; `R15_F1_RED_SUMMARY cases=58 pass=58 fail=0 result=PASS` | RP6 final subject above | Auditor-reproduced; fully closed for these five classes. |
| RP6-10 | R15 line-granularity cancellation | `X=R16_F1_RED`; r15 returns rc 0/result PASS for `inbody` and `spandecoy` | `inbody`: an extra emitter inside the accepted one-line wrapper body. `spandecoy`: quoted false candidate and real same-name definition at columns 64/90 on one physical line | Same command; r16 rejects both and `R16_F1_RED_SUMMARY cases=52 pass=52 fail=0 result=PASS`; carried real-byte fence is `R16_GRAMMAR_SUMMARY cases=50 pass=50 fail=0 result=PASS` | RP6 final subject above | Auditor-reproduced in the r16 PASS-WITH-NITS audit; fully closed for these two classes. |
| RP6-11 | R15 dynamically resolved inventory-mutation target | `UNLOCATED — supplemental`: the r15 audit identifies the class but states that it authored/executed no new mutant | `RP6_CODEX_T0_AUDIT_R15_2026-08-12.md` F3: an admitted variable-mutating builtin whose target is resolved dynamically and contains no literal protected inventory name | No located executed RED/GREEN pair. R16 only reports the clean-byte structural assertion `inventory_variable_targets ... dynamic_targets=0`; `R16_F1_RED` explicitly offers only `inbody` and `spandecoy` as the r15-finding closures | No qualifying GREEN binding | Current audit RED without repaired D026 GREEN: **OPEN** and freeze-relevant. The later r16 structural PASS does not manufacture the missing falsification. |

RP6 disclosed residual outside the closure-test count: shell shapes outside both published detection mechanisms remain outside the r16 claim; unknown/unresolvable shapes inside the stated vocabulary fail closed. No test is offered to close the deliberately excluded universe.

## RP7-WPI-RO

Exact command for every row:

```text
sed -n '/^# RP7_EXACT_COMMAND_BEGIN$/,/^# RP7_EXACT_COMMAND_END$/p' SELF_QA_RP7.md | bash --noprofile --norc
```

RED subject: exact round-8 blob, 99903 B, SHA-256 `11621044d0adc21af93e1cfc7b88ef88de8aca4683a69ab16cbc542a124141a4`. Final GREEN subject: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh`, 108301 B, SHA-256 `0e93f90de7fcefe86fee4137f3ba11ea34b69b120d6a06c304fdde0e9b921e62`. Evidence document: `SELF_QA_RP7.md`, 367860 B, SHA-256 `f2c62cbf7421a0d395654c1642eb165f87b396af26f41cf8eaa70af7323ba672`.

| ID | Closure test | RED output signature / identity | GREEN output signature | Final GREEN bytes | Provenance / disposition |
|---|---|---|---|---|---|
| RP7-01 | Descriptor-bound status body; delete name-only `wpi_alloc_leaf` | Round-8 real caller: `BODY_BINDING mode=outside subject=red rc=0 outside_is_original=no`; reader swap: `subject=red rc=0` accepts the name-replaced body. The RED fixture carries the old `wpi_alloc_leaf` definition verbatim because production r9 deletes it. | `mode=outside subject=green rc=3 outside_is_original=yes`; `mode=reader subject=green rc=1 ... B5_FAIL reason=flag_mismatch`; clean control remains rc 0 | RP7 final subject above | Auditor-reproduced by the exact end-to-end r9 command; fully closed. |
| RP7-02 | Preserve measured child status on stream-bind STOP | Round-8 `BIND_RC mode=divert_rc7 subject=red child_rc=7 ... result=[... rc=0 detail=capture_stream_unbound]` | `subject=green child_rc=7 ... result=[... rc=7 detail=capture_stream_unbound]`; clean/undeclared controls conserved | RP7 final subject above | Auditor-reproduced; fully closed. |
| RP7-03 | Wrapper rc-137 provenance channel | `RC137_PROVENANCE body=child_spoof subject=red ... rc=137 ... kind=killed_after_grace` | `subject=green ... rc=1 ... kind=sigkill_not_from_this_wrapper ... wrapper_stream=body_cannot_write`; real kill-after control remains rc 137 | RP7 final subject above | Auditor-reproduced; fully closed. |
| RP7-04 | One-to-one published fence mapping | Same executed omit-R8/duplicate-R7 mutant: `MAPPING_ASSERTION_POWER round8_on_green=accept round8_on_mutant=accept` | `round9_on_green=accept round9_on_mutant=reject`; exact-command result remains `PUBLISHED_COMMAND_RESULT=pass fences=6` | RP7 final subject above | Auditor-reproduced; fully closed. |
| RP7-05 | Namespace-reader detail on nonzero child status | Caller/service REDs: `NETNS_DETAIL ... subject=red rc=3 detail_field_present=0` | Caller/service GREENs: `subject=green rc=3 detail_field_present=1 ... detail=identity_read_child_failed diagnostic_file=...`; equal-namespace control stays rc 0 | RP7 final subject above | Auditor-reproduced; fully closed. |

RP7 disclosed limitations outside the closure-test count: (1) MSYS2 does not reproduce target Linux `/dev/fd` semantics, so the local outside-overwrite GREEN is a fail-closed transport STOP; (2) wrapper kill attribution does not prove that no unrelated concurrent kill occurred. Both remain non-accepting-safe limitations, not missing closure tests.

## Transport set

Final nine-file identity (`TRANSPORT-FINAL-9`):

| Path under `WPI_BLOCKS_DRAFT` | Bytes | SHA-256 |
|---|---:|---|
| `run_p0.sh` | 13608 | `4f608ad546402ad9587eeac237c16c7c3c3e707ebf4e6cb589e9459f08413c0c` |
| `run_ro.sh` | 13470 | `3dea6e64b087488fda2ab9bac8b66fceac1c13e70719b3ce9d81797a50443e3c` |
| `transport_runner.ps1` | 71137 | `4db0fbd17f9b32da13564a9ce2d0786283151737d81bcee031ed2bcb7b347fd2` |
| `TRANSPORT_PLAN.tsv` | 7970 | `e3c11218a9c70ef5454d8db25c7c9965ebed3ae07bc97a766240429685c50e3c` |
| `remote_setup_wpi.sh` | 26483 | `4428a60da02415ef1b7c84561b1bba458ee7f1affcfe9d33c4b1c3f07bcb5aa5` |
| `remote_extract_verify_wpi.sh` | 23592 | `5b3c0b225fdca18fd0a074a7bcce3c7124930e62eacc9e41da236db28585a55b` |
| `remote_close_tree_wpi.sh` | 32630 | `8892574f253ab26d6d48bba270f84ef2da4458a5bca93f2b3c9723991a3732cf` |
| `SELF_QA_TRANSPORT.md` | 194204 | `0a11d035f439906972386e354fa2dfb6bac5545fcd2db298adf64019bad25175` |
| `STATUS_TRANSPORT.md` | 22791 | `0f30944c1b7a1559ac8b7867984daa5c05cb0b14b7472a68a9932027f0380890` |

The r4 evidence is helper-driven (`_r4_runner_probe.ps1`, `_r4_wsl_fixtures.sh`, `_r4_t5_compose.sh`) and the stable self-QA publishes transcripts rather than one literal self-contained fence command. The r6 BA-1 command contains an external `<scratch>` predecessor location and invokes `_r5_wsl_fixtures.sh`. Under this map's rule, all nine rows are supplemental even where Codex reproduced the helper. Also, r5 changed comments across the delivered scripts and executable cleanup ordering in `remote_close_tree_wpi.sh`; therefore an r4 GREEN does not carry byte identity to `TRANSPORT-FINAL-9`.

| ID | Closure test | RED command / output | Pre-fix or mutation identity | GREEN command / output | Final bytes | Provenance / disposition |
|---|---|---|---|---|---|---|
| TR-01 | Wrong marker family accepted | `UNLOCATED — helper-only`; r4 runner probe Fixture D on exact r3 runner SHA-256 `13a57438...0e4`: op 07 `class=match`, run PASS | Actual r3 runner blob from `78173bfd` | Helper Fixture D on r4 runner: `not_evaluable reason=no_remote_program_marker_in_capture expected_family=remote_close_tree_wpi.sh`, run STOP | GREEN measured on r4 bytes, not `TRANSPORT-FINAL-9` | Auditor-reproduced helper; supplemental. |
| TR-02 | Inherited `TMPDIR` writes into evidence | `UNLOCATED — helper-only`; `F2 RED` rc 0 with `tmp.*/raw.0` included and false `wrote_into_evidence_tree=0` | Exact round-3 close-script bytes | `F2 GREEN` rc 3 `launch_domain_unexpected_environment_entry name=[TMPDIR]`; clean/overlap controls refuse safely | GREEN measured before later byte changes | Auditor-reproduced helper; supplemental. |
| TR-03 | Mixed ENOENT+EACCES diagnostic | `UNLOCATED — helper-only`; `F3 RED` rc 1 `CLOSE_FAIL reason=evidence_dir_absent` | Exact round-3 close-script classifier | `F3 GREEN` rc 3 `CLOSE_STOP reason=path_probe_error ... No such file or directory; Permission denied` | GREEN measured before later byte changes | Auditor-reproduced helper; supplemental. |
| TR-04 | Global `always` prerequisite erased a deviation | `UNLOCATED — helper-only`; Fixture A r3: `deviant=0`, `TR_RUN STOP` | Actual r3 runner SHA-256 `13a57438...0e4` | Fixture A r4: `deviant=1`, `TR_RUN FAIL` | GREEN measured on r4 runner SHA-256 `45123de4...fed`, not final runner bytes | Auditor-reproduced helper; supplemental. |
| TR-05 | Distinguish unestablished prerequisite from earlier deviation | `UNLOCATED — helper-only`; Fixture C r3 op 08 uses `cleanup_after_unestablished_prerequisite` | Actual r3 runner | Fixture C r4 op 08 uses `cleanup_after_earlier_deviation prerequisites=[05=deviant]` | GREEN measured before final byte changes | Auditor-reproduced helper; supplemental. |
| TR-06 | T5 five `P0_ATTESTED_*` values reach RP6 gate | `UNLOCATED — helper-only`; `A-RED` exports 0; real gate `B-RED` STOPs `preregistered_value_missing` | Actual r3 wrapper SHA-256 `e4ddf87b...1f80` and old environment | `A-GREEN` exports 5; filled-equal `B-GREEN2` prints `P0_GATE_PASSED all_five_attested_inputs_accepted` rc 0 | GREEN measured on r4 wrapper SHA-256 `6646770f...9202`, not final wrapper bytes | Auditor-reproduced helper; supplemental. |
| TR-07 | T6 three-argument close contract and work-root composition | `UNLOCATED — helper-only`; superseded edit self-STOPs; two-argument old call returns `CLOSE_FAIL` rc 1 | Superseded close-script and plan shapes | Op 01 allocates `<BASE>/work`; exact plan argv closes rc 0; two-argument call now `CLOSE_STOP` rc 3 | GREEN measured before final byte changes | Author-claimed helper transcript; supplemental. |
| TR-08 | T7 inert `WPI_INTERPRETER_TARGET` removal | `UNLOCATED — static/helper-only`; r3 `run_ro.sh` defines and exports the name | Round-3 wrapper lines 45/118 | Static r4 gate: 0 assignments, 0 exports, RP7 block reads it 0 times | GREEN predicate was not rerun as a literal fence on final bytes | Author-claimed static gate; supplemental. |
| TR-09 | BA-1 cleanup after successful `mkdir` diagnostic | Published r6 driver is non-literal because predecessor path is `<scratch>`: `wsl.exe -u root -- /usr/bin/bash --noprofile --norc .../_r5_wsl_fixtures.sh ... <scratch>/r6/pre`. RED: `SCRIPT_RC=3`, `RESIDUE_PRESENT=yes` | Exact pre-repair close-script object; same subject pathname and argv; only subject bytes change | Same helper command; GREEN `SCRIPT_RC=3`, same refusal, `RESIDUE_PRESENT=no`, `REFUSAL_BYTE_IDENTICAL=yes`, `DISTINCT_SUBJECT_ARGV_LINES=1`, fixture rc 0/stderr 0 | Executable GREEN is on the final seven target bytes, but evidence remains helper-only; see `TRANSPORT-FINAL-9` | Auditor-reproduced in r6; supplemental, not D026 closure under this map's literal-fence rule. |

Transport F1 is a disclosed residual, not a missing test: the inner `env -i` child is controlled, but the earlier SSH account-shell/startup boundary remains OPEN. The owner ratified ACCEPT-WITH-DISCLOSURE; there is deliberately no GREEN and it is not a freeze blocker. T8 and the later BA-2/BA-3/R5-F1/R5-F3/r6 wording edits are documentation dispositions, not executable closure tests, and are excluded from the closure-test count.

## SEC102 composite pathproof

Final accepted module: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/composite_pathproof.py`, 129658 B, SHA-256 `adbf27fd908439e1d48e6c95a4eecba956c0607c42ae5a3bfa9cb210b636c05a`, unchanged r8-r11. Accepted evidence document: `SELF_QA_SEC102_R11.md`, 223841 B, SHA-256 `043450c665538485a50a0ffb975fa8f6a6794e2e630a38fd68afd16d0c753c3a`, byte-identical to anchor `5f87cbc2`.

For each row, the exact command is the literal section-13b PowerShell fence in the named self-QA document, ending `$d026 | python -B - $base` and `"D026_HARNESS_BLOCK_RC=$LASTEXITCODE"`. The outer current-byte GREEN is the literal section-13c Python fence run as `python -B verify_selfqa_r11.py <path-to-SELF_QA_SEC102_R11.md> <outside-directory>`.

| ID | Closure test | Exact RED source / output | Pre-fix or mutation identity | Exact GREEN source / output | Final GREEN bytes | Provenance / disposition |
|---|---|---|---|---|---|---|
| SEC-01 | R7 child status/stderr completed before stdout comparison | `SELF_QA_SEC102_R8.md` §13b: `fails_after_summary` and `stderr_after_summary` are `R7=ACCEPTED/rc0` | Exact published r7 wrapper fence SHA-256 `4ba21f81088d73cc17f5162377c42a53792f2668401be9323a3732f98b507bca` | Same literal fence: both are `R8=REJECTED/rc1`, reasons `STATUS_REJECT_NONZERO_EXIT` and `STATUS_REJECT_UNADJUDICATED_STDERR`; `D026_CASES=4 RED_UNDER_R7_GREEN_UNDER_R8=2 D026_OFF_EXPECTATION=0`, rc 0 | Final SEC module + r11 evidence above; r11 conserves these gates | Lead-run verbatim and auditor-reproduced; fully closed. |
| SEC-02 | R8 LF-to-CRLF instrument rewrite | `SELF_QA_SEC102_R9.md` §13b: `D026_WRITEPATH=R8_TEXTMODE ... WRITTEN_CRLF=110 BYTE_IDENTICAL=0`; CRLF-certified false accept and LF false reject | Exact r8 wrapper fence SHA-256 `391a8e208f16c2c53c434d5800af0fd0c24b49df4ddba39aef28cc96ed11473c`; M1 restores the r8 text write path | Same literal fence: `R9_BYTEMODE ... WRITTEN_CRLF=0 BYTE_IDENTICAL=1`; `FALSE_ACCEPT_UNDER_R8=1 FALSE_REJECT_UNDER_R8=1 ... M1_GATE_FIRED=1`, rc 0. R11 remeasures `R11_BYTEMODE ... BYTE_IDENTICAL=1` | Final SEC module + r11 evidence above | Lead-run verbatim and auditor-reproduced; fully closed. |
| SEC-03 | R9 pathname reopen between comparison and child open | `SELF_QA_SEC102_R10.md` §13b: `rebind_certified R9_HOLD=ACCEPTED/rc0` and `rebind_honest R9_HOLD=REJECTED/rc1` | Exact `R9_HOLD` mutant SHA-256 `c25f4f61d498ef97cb703862de4a55207ce295aafc187e0f9c2d98aa93f8e566` | Same literal fence: r10 reverses both correctly; `REBIND_DENIED_UNDER_R10=2`, `D026_PIN_PRECONDITION EXISTING_WRITER=1 PIN_TAKEN=0 WINERROR=32`, M2/M3 gates fire, rc 0 | Final SEC module + r11 evidence above | Lead-run verbatim and auditor-reproduced; fully closed for direct object replacement/modification. |
| SEC-04 | R10 transient drive/volume rebind restored before post-sample | `SELF_QA_SEC102_R11.md` §13b: `transient_certified R10=ACCEPTED/rc0`, `transient_honest R10=REJECTED/rc1`, `R10_TWO_SAMPLE_DETECTOR=CLEAN/1` | `R10_TRANSIENT` SHA-256 `789807812176c887f77c2643c848ff01c2a3d23947efc98affc03d4c744d78b9` | Same literal fence: r11 rejects/accepts correctly; `FALSE_ACCEPT_UNDER_R10=1 FALSE_REJECT_UNDER_R10=1 TRANSIENT_CLOSED_UNDER_R11=2`; M4 reverts only the channel and yields `FALSE_ACCEPT_UNDER_NAMED_CHANNEL=1`; summary `M4_CHANNEL_LOAD_BEARING=1`, rc 0 | Final SEC module + r11 evidence above | Lead-run verbatim and auditor-reproduced; fully closed within the accepted trusted base. |
| SEC-05 | R10 mixed historical component chain | `SELF_QA_SEC102_R11.md` §13b: `R10_HANDLES=10 R10_PATH_PIN_COMPLETE=1 R10_CHAIN_MIXED=1 R10_LIVE_LEAF_UNPINNED=1` | Published chain construction copied verbatim, with one declared swap | Same literal fence: `R11_ANCHOR=OBJECT_VOLUME_GUID/1 R11_UNAFFECTED_BY_SWAP=1`; outer wrapper reports `CHAIN_COHERENT=1`, all 11 blocks name-bound/name-less and complete | Final SEC module + r11 evidence above | Lead-run verbatim and auditor-reproduced; fully closed within the accepted trusted base. |

SEC102 has four owner-accepted disclosed assumptions with no closure test by design: the outer Python runtime/startup/import graph; the PATH-resolved PowerShell image; on-disk document identity versus a fresh clone (drift fails loudly); and the production-gate interpreter vocabulary. The owner chose ACCEPT-WITH-DISCLOSURE on 2026-08-12; GLM's second opinion is source-level PASS-WITH-NITS but supplemental on execution.

## Pathscope prover round 2

Exact aggregate command, after saving the literal `SELF_QA_PATHSCOPE.md` “The harness, verbatim” fence as `%TEMP%\pathscope_r2_harness.ps1`:

```text
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:TEMP\pathscope_r2_harness.ps1"
```

RED subject: pinned round-1 blob, 49820 B, SHA-256 `3d6af544f5cbadb0a1432d4784848f68f4bfddf22aa52c9369fd9729853d43e6`. Final GREEN subject: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/pathscope_prover.py`, 122446 B, SHA-256 `890016f0b9a8cde4eed33f8733f69055471b07c6096f6bc07450457e6c52af1d`. Evidence document: `SELF_QA_PATHSCOPE.md`, 108974 B, SHA-256 `3e8f75fba9a144ba194ab4d952bb2023c8a5d651d256d4d38a6adbb650de0362`.

The author-recorded aggregate output is `RED_R1.txt lines=511`, `GREEN_R2.txt lines=644`; determinism is `equal=True` for `find_exec`, RP6-P0, and RP7-WPI-RO. GLM performed a read audit only and explicitly could not execute; therefore the provenance is author-claimed unless stated otherwise.

| ID | Closure test | RED output signature | Exact pre-fix identity | GREEN output signature | Final GREEN bytes | Provenance / disposition |
|---|---|---|---|---|---|---|
| PS-01 | F1 no-path/control shortcut | `pushd`/`trap`: round 1 rc 0 with no row; extensions `python_c`, `alias`, `hash_p`, `mapfile_cb`, `systemctl_link`, `jobs_x` also silently pass | Pinned round-1 prover above | `pushd` becomes `/safe ALLOW-LEXICAL`, forbidden pushd/trap become rc 1 FORBID, extensions receive explicit FORBID or rc-3 coverage dispositions | Final pathscope prover above | Author-claimed literal RED/GREEN; GLM read-confirmed; fully closed as published D026, not independent audit acceptance. |
| PS-02 | F2 SSH/NSS endpoint grammar | `ssh`, `getent`, `nc_client`: round 1 rc 0 with no row | Pinned round-1 prover | `ssh`/`nc_client` report forbidden endpoints; `getent` is explicit unresolved endpoint rc 3; remote command is rc 3 | Final pathscope prover above | Author-claimed literal RED/GREEN; GLM read-confirmed; fully closed as published D026. |
| PS-03 | F3 `find -exec` hidden sink | `find_exec` round 1 rc 0, only `/safe ALLOW`; `find_unknown` also rc 0 | Pinned round-1 prover | `/etc/passwd FORBID` plus `/safe ALLOW-LEXICAL`, rc 1; unknown predicate rc 3 | Final pathscope prover above | Author-claimed literal RED/GREEN; GLM read-confirmed; fully closed as published D026. |
| PS-04 | F4 `--option=PATH` discarded | `curl_upload`, `tar_option`, `cp_option`, `cp_unknown` omit the option path and can rc 0 | Pinned round-1 prover | Exact forbidden path is reported for upload/archive/target; unknown option rc 3; controls conserved | Final pathscope prover above | Author-claimed literal RED/GREEN; GLM read-confirmed; fully closed as published D026. |
| PS-05 | F5 tilde falsely resolved under `PWD` | `tilde`/`tilde_user` print invented `/safe/~/... ALLOW`; `tilde_home` same | Pinned round-1 prover | Unknown home forms become unresolved with no false path row; pinned HOME yields real `/home/gatea/secret FORBID` rc 1 | Final pathscope prover above | Author-claimed literal RED/GREEN; GLM read-confirmed; fully closed as published D026. |
| PS-06 | F6 unconditional host-path `ALLOW` wording | `symlink_lexical`: `/safe/link/passwd verdict=ALLOW`, PASS `closed_and_allowlisted` | Pinned round-1 prover | Unconditional semantics line names lexical-only scope; token is `ALLOW-LEXICAL`; PASS reason is `closed_and_allowlisted_lexical_argv_scope` | Final pathscope prover above | Author-claimed literal RED/GREEN; GLM read-confirmed; fully closed as a disclosure repair. Host binding remains residual R1. |
| PS-07 | F7 `<>`/redirection target loss | `redir_rw` invents `/safe/> ALLOW`; `redir_clobber` omits real target | Pinned round-1 prover | Exact `/etc/x` and `/etc/y` targets are FORBID; other redirection and `/dev/tcp` controls receive explicit dispositions | Final pathscope prover above | Author-claimed literal RED/GREEN; GLM read-confirmed; fully closed as published D026. |
| PS-08 | F8 issue count mislabeled and heredoc data misread | Round 1 `heredoc unresolved_count=3`; `array unresolved_count=2`; quoted heredoc substitution is treated as program text | Pinned round-1 prover | Separate resolved/unresolved/coverage/provenance/parse fields with `kind=`; plain/quoted heredoc data rc 0; unquoted substitution still catches `/etc/shadow` | Final pathscope prover above | Author-claimed literal RED/GREEN; GLM read-confirmed; fully closed as published D026. |
| PS-09 | F9 real-input evidence was not literally rerunnable | `UNLOCATED — supplemental`: the round-1 document supplied no exact immutable extraction/setup/identity/invocation command, which is the finding itself | Round-1 self-QA prose and historical Lead rerun, without a literal one-command recipe | Current literal aggregate command above; author output `RED_R1.txt lines=511`, `GREEN_R2.txt lines=644`, three `equal=True` determinism rows | Final pathscope prover above | Author-claimed GREEN; no exact executable RED can be retroactively located. Supplemental, not D026 closure. |

Pathscope's seven disclosed residuals remain outside the closure-test count: R1 lexical-versus-host binding; R2 function positional dataflow; R3 alias expansion; R4 deliberate conservative over-reporting; R5 inline-option provenance attribution; R6 finite registry/lower-bound resolved set on STOP; and R7 renamed output fields for downstream consumers. GLM found no silent false-ALLOW by static review but could not execute, so it did not supply independent acceptance.

## Summary

- Total closure/evidence rows mapped: **39**.
- Fully closed with located RED + GREEN on the stated final bytes: **28**.
- OPEN, RED finding without a qualifying repaired GREEN: ~~**1** — `RP6-11`, dynamic inventory-mutation target.~~ **RESOLVED 2026-08-12 ~15:45 by round 17 → 0 open.** See the RP6-11 disposition note below.
- Unlocated/supplemental rows: **11 evidence-quality flags**. Ten are non-open supplemental rows (transport 9 + pathscope F9); the eleventh is the same `RP6-11` row already counted OPEN, because its RED is also unlocated. This overlap is stated so the numbers are not falsely additive.
- Disclosed residuals/limitations with no closure test by design: **15** (RP6 1, RP7 2, transport 1, SEC102 4, pathscope 7).
- Execution provenance: RP6 and RP7 closure rows are auditor-reproduced; transport rows were helper-driven even where auditor-reproduced; SEC102 rows were Lead-run verbatim and auditor-reproduced; pathscope rows are author-claimed with a non-executing GLM read audit.
- Freeze-relevant D026 result: **one open current-audit finding** remains (`RP6-11`); transport F1 is separately owner-ratified ACCEPT-WITH-DISCLOSURE and is not counted as open.

Packet 7 can now be marked CLOSED in `AUDIT2_HANDOFF_PACKAGE.md` as a completed, honest map packet; that packet closure does not upgrade any supplemental row or authorize freeze.

## RP6-11 disposition — resolved same day, with one claim corrected

This row is the map's one real catch, and its resolution is worth recording precisely because
half of the follow-up analysis was wrong.

A GLM-5.2 advance read-audit answered the open question by claiming the r16 fence *admits* a
variable-mutating `eval` with a runtime-resolved target and certifies it CLEAN. **That claim is
false for the checked-in bytes**: `SELF_QA_RP6.md:16763-16765` already refuses `eval`, `source`
and `.` as `UNMODELED kind=indirect_execution_builtin:*`. Codex found this while implementing and
said so in its own round-17 report rather than building on the bad premise. The Lead's
intermediate "confirmed by direct source read" was **partial** — it verified that `eval` appears
in `admissible_bare` and is absent from the enumerated mutating-builtin list (both true) and then
accepted the conclusion without checking whether a different branch catches it. Membership in
`admissible_bare` only suppresses the unbound-invocation check; classification happens elsewhere.

The other half was real and Lead-verified: `dynamic_targets=0` at `:17571` was a hardcoded
literal presented as a measurement, beside a genuinely measured `variable_targets=$n_vt`. Round
17's pass-format audit found **six** such literal-zero fields across three r16 success lines.

**Round 17 closes it by inversion rather than enumeration:** a closed effect model over the
tokenizer stream in which any bare word outside the modelled set is an opaque execution surface
that fails with an unmodeled record, and `dynamic_targets` becomes
`dynamic_variable_target + indirect_execution_builtin + effect_model_unmodeled`. Because the
shipped fence already refuses these constructs, the RED side uses a temporary r16 fence with
**only** the indirect-execution refusal removed — labelled explicitly rather than implied as a
live defect. Two structurally different class members were exercised (`eval` by name
concatenation; `dot_source` via a constructed runtime file).

**Lead verbatim run (evidence of record):** `R17_DYNAMIC_TARGETS_SUMMARY cases=15 pass=15 fail=0
result=PASS`, outer rc 0, carried r16 grammar `50/50` with no previously-killed mutant surviving,
`r17_literal_zero_measurements=0`, block identity unchanged.

**Still required:** the r17 bytes have no independent audit. Tonight's Claude Pro second-flagship
RP6 audit is repointed at r17 and is asked to verify the correction itself, since two models have
now disagreed about this file.
