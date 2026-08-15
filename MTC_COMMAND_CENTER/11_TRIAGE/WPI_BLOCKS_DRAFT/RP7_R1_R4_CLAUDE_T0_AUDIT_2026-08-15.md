# RP7 R1-R4 - Claude T0 flagship audit

**Verdict: PASS-WITH-NITS** (0 required repairs, 6 optional nits)

Auditor: Claude, fresh independent non-implementer session, no `--resume` /
`--continue`, no sub-delegation, no other model invoked. Exact model
`claude-opus-5`; effort `xhigh` per the dispatch contract of
`KICKOFF_CLAUDE_RP7_R1_R4_T0_AUDIT_2026-08-15.md` (the effort setting is supplied
by the launcher and is not introspectable from inside the session; it is stated
as contracted, not as measured). Tier T0. Date 2026-08-15. Worktree `C:\R7T0CLA`.

Frozen candidate commit `80cbed461d0b0371e6eabbfff0e732e5001affaf`.

I did not read `RP7_R1_R4_CODEX_T0_AUDIT_2026-08-15.md` or any other same-round
Codex verdict; no such file exists in this tree. The prior-round cap-override
verdicts and the Codex Lead adjudication were read because the kickoff requires
them. This verdict alone cannot accept T0: both mandatory flagship verdicts are
required.

Summary of what was executed and what it showed: the four frozen identities
re-derive exactly from Git object bytes; the complete rows-1-9 fence ran twice
sequentially in a run-owned Linux scratch tree materialised from those bytes,
rc 0 both times, and the two published transcripts are **raw byte-for-byte
identical to each other and to the transcript embedded in `SELF_QA_RP7.md`**,
with no external editing, path replacement, normalisation or exclusion; the real
internal scratch roots and mount-projection digests differed between the runs and
remained bound; R1, R2, R3 and R4 all reproduce closed on independent evidence;
and a wider terminator sweep than the package's own found no surviving false PASS
or false FAIL in the row-6 or row-9 predicates.

---

## 1. Identity - re-derived from Git object bytes

`C:\R7T0CLA` is a Windows linked worktree with `core.autocrlf=true` and
`.gitattributes` `* text=auto`, so its working-tree copies carry CRLF. Those
transport-converted bytes are **not** the frozen subject and are not reported as
drift. Every identity below was re-derived by walking `commit -> tree -> path ->
blob` and materialising the blob bytes into a run-owned Linux scratch tree
preserving the repository-relative layout.

```text
$ git cat-file -t 80cbed461d0b0371e6eabbfff0e732e5001affaf   -> commit

RP7-WPI-RO.sh                     blob=0e145424b5cf1cadec06838963d7187584aaa2f5
  bytes=137981 sha256=4caed4aecc91cada3b8b99f8ff06d7ba0d7376b2bc07e92c298f4a7b7ca0900c cr_bytes=0
SELF_QA_RP7.md                    blob=d20fe06395cc053c2f9c315b8805e90a43d6fb16
  bytes=585132 sha256=b1031cc5e71f2a19e05a400a0d3754b9cf37b5917848868e61ae0764a5b1c8ae cr_bytes=0
STATUS_RP7.md                     blob=de3a4dd6bcdc98e4968c6c6131c4392f65e110bc
  bytes=19165  sha256=f1fbe2e1d8381b2c5d762e6c69fff2718b7f90ae8d09e8b32d1947fab8ea5a46 cr_bytes=0
RP7_ROWS_1_9_REPORT_2026-08-13.md blob=36d49845cf04e2c95589e51c0363cb9913251390
  bytes=54481  sha256=0a434a98393a6c8ecf41a01d6696326c814c44bf69a5d51734f1b44cbe738c46 cr_bytes=0
```

All four equal the kickoff freeze table exactly. No dispatch BLOCK on identity.

Historical subjects the fence names, re-derived through the same object store:
`90cbeac4` = 127491 B / `5b00207a...b9b3dbe3`; `8ec89675` = 127655 B /
`beacf85b...4f52d809a8`; `2d0f24d0` = 132886 B / `a4af307c...49670b243`. All three
match the fence's own assertions.

Independent syntax and extraction checks on the materialised bytes:

```text
bash --noprofile --norc -n RP7-WPI-RO.sh                       rc=0
bash --noprofile --norc -n <extracted fence>                   rc=0
bash --noprofile --norc -n <block minus terminal wpi_main>     rc=0
extracted fence  bytes=115657 lines=1215
                 sha256=b64c23ebcc85dece217a2128c069b7d4074cc763533319edb8a25ecf2dc06fbb
terminal line of RP7-WPI-RO.sh: wpi_main "$@"
```

The extracted-fence SHA-256 equals the value recorded in
`RP7_R1_R4_LEAD_VERIFICATION_2026-08-15.md`.

## 2. Mandatory execution - the complete rows-1-9 fence, twice, sequentially

Environment: WSL Ubuntu, kernel `6.18.33.2-microsoft-standard-WSL2`,
`systemd 259 (259.5-0ubuntu3)`, `GNU bash 5.3.9(1)`, `Python 3.14.4`,
`git 2.53.0`, root.

The frozen blobs were materialised into `/var/tmp/r7t0cla_audit/repo/...` (a
run-owned Linux scratch tree, outside every repository). The fence needs
`git -C "$REPO" cat-file blob 90cbeac4|8ec89675|2d0f24d0:...`, so the scratch tree
was made a run-owned repository with `git init` and an
`objects/info/alternates` entry pointing read-only at the audited object store.
Nothing was written to that store and no Git state in `C:\R7T0CLA` or
`C:\LAB\Tradingview_LAB_CLEAN` was mutated.

**The published extraction command was executed verbatim, unedited.** The frozen
fence derives `REPO` from the directory the command cds into, so no `RP7_REPO`
override and no fence edit was needed - which is itself the R3 sub-claim that the
published body runs unedited in any checkout:

```text
cd <run-owned materialisation>/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT
sed -n '/^# RP7_ROWS_1_9_REBUILD_FENCE_BEGIN$/,/^# RP7_ROWS_1_9_REBUILD_FENCE_END$/p' SELF_QA_RP7.md | bash --noprofile --norc
```

Results, strictly sequential, one after the other:

| run | rc | elapsed | stdout bytes | lines | stdout SHA-256 | stderr |
|---|---:|---:|---:|---:|---|---:|
| A | 0 | 197.6 s | 54284 | 250 | `d0788122c132e43c25aea52315d53b3596c40c57598e2bbded9b2efa11cae8ab` | 0 B |
| B | 0 | 199.0 s | 54284 | 250 | `d0788122c132e43c25aea52315d53b3596c40c57598e2bbded9b2efa11cae8ab` | 0 B |

```text
cmp runA.stdout runB.stdout                        -> rc 0, identical
cmp <SELF_QA_RP7.md:1354-1603> runA.stdout         -> rc 0, identical
```

The transcript embedded in the frozen `SELF_QA_RP7.md` is **byte-for-byte the
same 54284 bytes** as both of my fresh runs. No `sed`, no substitution, no
excluded field, no tolerated line. The prior round's "155 of 156 lines after an
external `sed`" exception is genuinely gone, not restated.

Contamination and abort census, measured on my own run:

```text
HARNESS_ABORT 0   HARNESS_CASE_FAIL 0    HARNESS_SUBJECT_FAIL 0
HARNESS_CASE_STDERR 0   HARNESS_SUBJECT_STDERR 0   RP7_STOP 0
HARNESS_COUNT_MISMATCH 0  HARNESS_BLOCK_ID_MISMATCH 0
HARNESS_ORACLE_FAIL 0   HARNESS_ENV_ORACLE_FAIL 0   stderr bytes 0

HARNESS_BLOCK_ID stage=before bytes=137981 sha256=4caed4ae...7ca0900c cr_bytes=0 bash_n=0
HARNESS_BLOCK_ID stage=after  bytes=137981 sha256=4caed4ae...7ca0900c cr_bytes=0 bash_n=0

single subject   RED=43  GREEN=43  CONTROL=12          (98 D026 lines)
multi subject    RED=23  GREEN=15  CONTROL=65          (103 D026_SUBJECT lines)
per subject      repaired 25, round4 19, capoverride 16, current 16,
                 mut_broad 9, mut_nocr 9, mut_splitlines 9
HARNESS_SUBJECT 7   HARNESS_MUTANT 3
ORACLE 14 (live systemd-analyze verify)   ENV_ORACLE 11 (live)
D026_SUMMARY ... result=PASS extracted_block_functions=yes block_logic_reimplemented=no
```

All fourteen `ORACLE` arms and all eleven `ENV_ORACLE` arms executed live against
`systemd-analyze verify` on this machine; none was skipped, and the fence's
`systemd_version_below_rule_of_record` / `systemd_oracle_unavailable` aborts did
not fire.

### Real internal identities differed and remained bound

Retained through the fence's documented `RP7_RAW_EVIDENCE_DIR` export:

| internal identity | run A | run B |
|---|---|---|
| scratch root | `/tmp/rp7_rows_1_9_rebuild_evidence.8VSwFMhe` | `/tmp/rp7_rows_1_9_rebuild_evidence.dCCrhGNz` |
| live mount projection | `fd6cce3b1466d3d02ac3b72f5c8b0f64b0879c547b1f6d8e33b550e7efcb2351` | `23e94f38e63203736dfc3981f116ef6cf233c80909fe8cf71ba2eddad617cc20` |
| decoy projection | `71245099336cca0b4b686193c52f7ef93b25984c03b1dc8c9df5723d70ec4ccb` | `363bde6a427007780e999977692945223dab0b3db5276767a4a1829e2459e8a2` |
| re-derived projection (2nd build, same run) | equals the attested value | equals the attested value |
| raw transcript SHA-256 | `781fcf0868227435fbc1fb4bfad5e204b647ac2c8a53ae64c9ce59da965c8e68` | `e4da6fbca94bcb47b8569d9bc17d4cea182c8a83efa1437efeb9a27c05901883` |
| realised root occurrences, raw / published | 131 lines / **0** | 131 lines / **0** |

`cmp` on the two raw transcripts returns rc 1 and they differ on 262 lines
(131 line pairs) - the number the package and the Lead both state. The canon map
retained from each run contains exactly the five declared presentation values and
nothing else; `%REPO%` resolved to my run-owned materialisation path and had 0
hits, so no repository path leaked into the published bytes.

I rebuilt a mount projection myself with the production
`wpi_build_mount_projection` and confirmed the binding record is real and the
digest is the file's actual hash:

```text
BOUND kind=point  path=<run-owned>/unit/mtc-bridge-first-start.service
      device=8:48 root=/ mount_point=/ fstype=ext4 source=/dev/sdd shared_mount_point_records=1
independently_rehashed=7939df024a76512ff2cd07524d1047080fa2a86977ae8a5daf737e88d738fb4e
fence_reported       =7939df024a76512ff2cd07524d1047080fa2a86977ae8a5daf737e88d738fb4e
```

## 3. R1 - the production normalisation boundary, reproduced

### 3.1 The manager boundary, executed independently

I did not reuse the fence's `ENV_ORACLE` arms. I built my own unit fixtures and
asked systemd 259 which token it actually validated. Under a name that is invalid
even after quote removal, systemd echoes the token **with the quotes already
gone**; under a valid name the same spelling draws no diagnostic at all:

```text
ctrl_bad_name       'Environment=1BAD=value'                              -> echoed [1BAD=value]
hyphen_plain        'MTC-BRIDGE_START_MODE=credential_free_disarmed'      -> echoed [MTC-BRIDGE_START_MODE=credential_free_disarmed]
hyphen_midname_dq   'MTC-BRIDGE"_START_MODE=credential_free_disarmed"'    -> echoed [MTC-BRIDGE_START_MODE=credential_free_disarmed]
hyphen_midname_sq   "MTC-BRIDGE'_START_MODE=credential_free_disarmed'"    -> echoed [MTC-BRIDGE_START_MODE=credential_free_disarmed]
hyphen_split_quotes 'MTC-BRIDGE_START"_MO"DE=credential_free_disarmed'    -> echoed [MTC-BRIDGE_START_MODE=credential_free_disarmed]
hyphen_whole_quoted '"MTC-BRIDGE_START_MODE=credential_free_disarmed"'    -> echoed [MTC-BRIDGE_START_MODE=credential_free_disarmed]
hyphen_empty_quotes '""MTC-BRIDGE_START_MODE=credential_free_disarmed'    -> echoed [MTC-BRIDGE_START_MODE=credential_free_disarmed]
valid_midname_dq    'MTC_BRIDGE"_START_MODE=credential_free_disarmed"'    -> (none, accepted silently)
valid_split_quotes  'MTC_BRIDGE_START"_MO"DE=credential_free_disarmed'    -> (none, accepted silently)
dup_same / dup_diff                                                       -> (none, accepted silently)
```

`hyphen_split_quotes` is the decisive addition of my own: a quote pair in the
**middle** of the name disappears before validation. Quote removal therefore
precedes validation, and what the manager stores - and renders back through
`systemctl show` - is the clean protected assignment. The raw mid-name spelling
cannot reach the row-9 input. The package's withdrawal of the old "the tokenizer
refuses the unit-source attack" claim is correct, and its replacement claim is the
one that is true.

### 3.2 The real refusal, driven through the full production caller

The fence's `source_binding` pair drives `wpi_assert_regular_digest` directly. I
went one level higher and drove the actual production sequence -
`wpi_assert_b2_rows_1_7` then `wpi_assert_b4_rows_8_9`, in `wpi_main`'s order, in
a separate process per arm, using the fence's own verbatim `write_b2_show` /
`write_b4_show` helpers extracted from the frozen `SELF_QA_RP7.md` bytes:

```text
[GREEN clean unit source, clean pin]        subject=repaired
  source 3736 B sha256=fde19b8b...6241260   pin 3736 B sha256=fde19b8b...6241260
  rc=0  child_stderr=0
  B4_environment target=MTC_BRIDGE_START_MODE value=credential_free_disarmed
    parser=systemd_environment_tokenizer occurrences=1
    source_binding=unit_fragment_digest_attested_dropins_empty

[RED  unit source carries MTC_BRIDGE"_START_MODE=..."]   subject=repaired
  source 3736 B sha256=3770f311...6f8a947a   pin 3736 B sha256=fde19b8b...6241260
  rc=1  child_stderr=0
  B2_FAIL reason=unit_fragment_digest_mismatch observed=3770f311... expected=fde19b8b...
  row-9 line emitted: NONE
```

The attacked source is refused at row 7 and **row 9 is never reached**. Same-size,
differing-digest fixtures, so the predicate can only be discriminating on content.
`wpi_main` runs B2 before B4 unconditionally, `WPI_UNIT_SOURCE_ATTESTED` is
initialised empty at `RP7-WPI-RO.sh:130` and set only at the end of
`wpi_assert_b2_rows_1_7` after `DropInPaths`-empty and the fragment digest have
both passed, and `wpi_assert_environment_start_mode` STOPs without it. The
accepting token `source_binding=unit_fragment_digest_attested_dropins_empty` is
therefore earned by the sequence that emits it.

The cap-override bytes accept the same clean rendering with **no** source
attestation at all - their accepting line carries no `source_binding` token
(`CTRL_capoverride_clean`, rc 0) - which is exactly the R1 gap, reproduced against
real committed bytes rather than a mutant.

### 3.3 Controls and duplicate policy remain truthful

25 rendering arms driven through the full production caller on the repaired
bytes. No false PASS; every accepting arm is truthfully accepting:

```text
ACCEPT clean / whole_quoted / single_quoted_whole / value_quoted
ACCEPT value_inner_quotes  MTC_BRIDGE_START_MODE=cred"ential"_free_disarmed -> value=credential_free_disarmed
ACCEPT trailing_space_tok
STOP   midname_dq, midname_sq, name_esc_backslash        detail=environment_token_name_not_literal
STOP   outer_pair, four_quotes, empty_quotes_prefix, name_quoted_only
                                                          detail=environment_token_lexing_disagreement
STOP   unbalanced_quote (ValueError), no_assignment, digit_name
FAIL   dup_same (count=2), dup_diff (count=2), absent (count=0),
       substring_name (count=0), empty_value, dollar_expansion, value_with_equals
STOP   tab_separated / newline_in_render  - refused by the show-capture parser before row 9
```

The duplicate policy is truthful in both directions: systemd accepts both
duplicate forms with no diagnostic (my `dup_same` / `dup_diff` oracle arms above),
row 9 refuses them as an rc-1 FAIL, and the block, `STATUS_RP7.md` and the report
each state plainly that this is a **declared narrowing stronger than systemd**,
together with the disclosure that whether a real manager ever renders the
protected name twice is not established by this fixture harness.

**R1 reproduces closed.**

## 4. R2 - one exact chronology

The three chronology tables in `SELF_QA_RP7.md`, `STATUS_RP7.md` and
`RP7_ROWS_1_9_REPORT_2026-08-13.md` are **byte-identical as text**, each hashing
to `12df590d9c2a4d61c9b6aad1230c3b47414670ddff521ebb140fc789ac02b174`.

I searched all four frozen artifacts for the strings the prior round found
contradictory - `none_yet`, "no independent Lead run", "no Lead run",
`independent_lead_run=`, auditor-acceptance claims - and read every occurrence of
"Lead" in all four. The result is one coherent state:

- every surviving Lead sentence names the byte identity it is about (`108301`,
  `127491`, `127655`, `132886`, `137981`);
- `auditor_acceptance=none_yet_both_T0_slots_pending_same_bytes` and
  `independent_lead_run=pass_2026-08-15_two_retained_runs_rc0_203s_each_raw_cmp_identical`
  are consistent with the table and with each other;
- the two cap-override verdicts retain their real values (Codex **BLOCK**,
  Claude **REQUEST_CHANGES**) and are not recast as acceptances;
- no artifact claims any auditor has seen `137981`, and none claims acceptance.

Nothing in the package claims later work already occurred. The `137981` row
records "both T0 slots PENDING", which was true at freeze and is the state this
verdict now begins to fill.

**R2 reproduces closed.**

## 5. R3 - canonical presentation cannot mask a deviation

Beyond the byte-identical two-run result in §2, I adversarially broke the
publication layer and the mount binding in run-owned scratch copies of the fence.
Each mutation replaced or inserted **exactly one line**, verified unique before
execution; the repository copy was never modified.

| # | adversarial change | observed | published vs baseline |
|---|---|---|---|
| 1 | freeze the attested mount digest to a constant after the first build | rc 97 `HARNESS_ABORT mount_projection_not_rederivable` | DIFFERS |
| 2 | make the decoy rebuild reuse the real fragment path | rc 97 `HARNESS_ABORT mount_projection_not_path_sensitive` | DIFFERS |
| 3 | repoint the fragment so the `kind=point` binding record no longer matches | rc 97 `HARNESS_ABORT mount_projection_unit_fragment_record_absent` | DIFFERS |
| 4 | print the run root once more (`EXTRAROOT %s`) | rc 94 `HARNESS_CANON_FAIL count_mismatch:%RUNROOT% expected=133 observed=134` + `HARNESS_ABORT canonicalisation_failed` | DIFFERS |
| 5 | print a **foreign** realised root of the same template that is not this run's | rc 94 `HARNESS_CANON_FAIL run_owned_root_realised_name_survived` | DIFFERS |

Arm 5 is the one the declared-count gate cannot catch (the count stays 133); the
unconditional residue gate catches it instead. Arms 1-3 are three independent
ways for the hidden digest to stop being a live, re-derivable, path-sensitive
function of this namespace, and each aborts before any row runs.

I also produced a **real** predicate-relevant mount change rather than a
simulated one. Driving the production `wpi_mount_guard_begin` /
`wpi_mount_guard_end` and creating a genuine tmpfs mount inside the tracked
scratch subtree between them:

```text
CONTROL  no mount change   rc=0  before==after  GUARD_CLOSED
MUTATE   tmpfs mounted     rc=3
  RP7_STOP reason=mount_topology_changed
    before=2dfdae43a92acbc09b25097483290ca27493145aba8cf2805e29eba551ab72fb
    after =63300692cd48678a0ee7343e166277b48905dee57e84fe9c3e8ba5e5022b1f75
    format=normalised_path_projection_v2
  (mount records 37 -> 38)
```

The deviation surfaces as a published `RP7_STOP`, not as silence. The mount was
unmounted immediately; `grep -c <scratch> /proc/self/mountinfo` returned 0
afterwards.

Canonicalisation therefore changes presentation only, is declared field by field,
is enforced by count, by residue and by three in-run binding proofs, and fails
closed on every route I could construct.

**R3 reproduces closed.**

## 6. R4 - the systemd line terminator, independently modelled

### 6.1 The two false PASSes on the frozen cap-override bytes, reproduced

Driven through the real `wpi_assert_fragment_has_no_install_section`, extracted
from each committed blob with the fence's own `sed '$d'` method and executed by
the fence's own **verbatim** `subject_child.sh` body (extracted from the frozen
`SELF_QA_RP7.md` heredoc, sha256 `abfb51a1...a1a9fe5f`), one process and one
scratch namespace per (subject, arm), child stderr empty on every arm:

```text
bare_cr_install   systemd 259: ZZZBogus landed in [Install] -> the [Install] is REAL
  round4      present rc=1     current     absent  rc=0  <- false PASS
  capoverride absent  rc=0 <- FALSE PASS   repaired    present rc=1

multi_cr_install  systemd 259: ZZZBogus landed in [Install] -> the [Install] is REAL
  round4      absent  rc=0 <- FALSE PASS   current     present rc=1
  capoverride absent  rc=0 <- FALSE PASS   repaired    present rc=1

cr_only_file      systemd 259: ZZZBogus landed in [Install] -> the [Install] is REAL
  round4      present rc=1     current     grammar rc=3
  capoverride grammar rc=3                 repaired    present rc=1
```

Both false PASSes named by the repair are real and are on the **frozen
cap-override committed bytes**, not on a mutant. `cr_only_file` is the
inability-to-evaluate case: the LF-only model STOPs on a fragment the manager
parses without difficulty. All three are `present` at rc 1 on the repaired bytes.

**Auditor self-disclosure.** My first `multi_cr` fixture was invalid: the tooling
layer between this session and WSL collapsed one backslash, so the file carried
`\` + letter `r` + CR + LF instead of `\` + CR + CR + LF, and it produced
`present` on every subject - the opposite reading, looking entirely healthy. I
caught it because the byte census disagreed with the fence's declared
`bs=1 cr=2 lf=6 vt=0 dq=0 total=100`, discarded that arm, rebuilt the fixture from
explicit byte codes with no backslash escape sequence anywhere in the generator,
re-verified the census, and only then read the answer. This is the same failure
mode the package documents twice, and it is the reason its `fixture_terms` /
`fixture_bytes_census` pre-assertion gates are the right design rather than
ceremony. Only the rebuilt result is reported above.

### 6.2 The wider terminator sweep - no surviving unmodelled member

The repaired parser claims the terminator set is exactly `CRLF`, bare `CR`, bare
`LF`, and that **every other byte is content**. That is a universal claim, so I
tested nine candidate byte classes in two shapes each - the byte between a value
and a header, and the byte opening the line after an open continuation - against
live systemd 259 and against all four committed byte sets:

```text
fixture      systemd | round4      current     capoverride repaired
bare_cr      Install | present:1   absent:0    absent:0    present:1
bare_ff      Unit    | present:1   absent:0    absent:0    absent:0
bare_fs      Unit    | present:1   absent:0    absent:0    absent:0
bare_gs      Unit    | present:1   absent:0    absent:0    absent:0
bare_rs      Unit    | present:1   absent:0    absent:0    absent:0
bare_vt      Unit    | present:1   absent:0    absent:0    absent:0
bare_nel     Unit    | present:1   absent:0    absent:0    absent:0
bare_ls      Unit    | present:1   absent:0    absent:0    absent:0
bare_ps      Unit    | present:1   absent:0    absent:0    absent:0
cont_*       (same pattern for all nine, with cont_cr -> Install / repaired present)
```

`round4`'s `str.splitlines()` is wrong on every one of the eight non-CR classes -
the executed refutation of "just revert it" - while the repaired bytes agree with
systemd on all eighteen arms. **No unmodelled terminator survives.**

Shape arms around the header itself, all agreeing with systemd:

```text
indent_space_install / indent_tab_install   systemd Install   repaired present:1
header_trailing_space / header_trailing_tab systemd Install   repaired present:1
lower_install  [install]                    systemd "Unknown section 'install'. Ignoring."   repaired absent:0
bom_install    UTF-8 BOM then real [Install] systemd Install  repaired present:1
cr_crlf_mix    \ + CRLF then bare CR + header systemd Install repaired present:1
```

Three shapes STOP with `section_header_grammar`, and systemd's own answer shows
the STOP is the truthful disposition rather than a conservative dodge - these
fragments do not load at all:

```text
[Install] # c   -> "Invalid section header '[Install] # c'"  ... "failed to load properly ... Bad message"
[Install] ; c   -> "Invalid section header '[Install] ; c'"  ... Bad message
[Install]\ ...  -> "Invalid section header '[Install]\nZZZBogus=1'" ... Bad message
```

My reference arms reproduced the fence's already-recorded oracle answers before
any new arm was read (`ctrl_lf_bogus` Unit, `bs_lf` Unit, `bs_space_lf` Install,
`bare_cr` Install, `cr_only` Install, `vt_after_bs` Unit), which is the hard gate
that makes the new answers readable.

**R4 reproduces closed.**

## 7. D026 verification of the new tests, and the adjacent boundaries

| new test in this round | RED subject(s) | GREEN | I verified |
|---|---|---|---|
| `ORACLE bare_cr` | - | - | yes, live systemd, reproduced independently |
| `ORACLE multi_cr` | - | - | yes, reproduced independently after fixture rebuild |
| `ORACLE cr_only_file` | - | - | yes, reproduced independently |
| `ORACLE vt_after_backslash` | - | - | yes, reproduced independently |
| `ORACLE bs_cr_then_header` | - | - | executed live in both of my fence runs |
| `ENV_ORACLE` 11 arms | - | - | yes, plus four extra arms of my own (§3.1) |
| `bare_cr_install` | `capoverride` 132886, `current` 127655, `mut_nocr` | `repaired` | yes, real committed bytes, separate processes |
| `multi_cr_install` | `capoverride`, `round4` 127491 | `repaired` | yes, real committed bytes, separate processes |
| `cr_only_file` | `capoverride`, `current`, `mut_nocr` | `repaired` | yes, real committed bytes, separate processes |
| `bs_cr_then_header` | - (control, all 7 subjects) | - | executed in both fence runs |
| `vt_after_backslash` | `mut_splitlines` (mutant) | `repaired` | yes; `round4`'s real `splitlines()` shows the same class on 8 byte classes |
| row 9 `unattested_clean` | `capoverride`, `current`, `round4` | `repaired` | yes - reproduced the unbound accepting line on `capoverride` at caller level |
| row 9 `normalized_from_midname_quote` | - (control, 3 subjects) | - | yes, driven through the full production caller |
| row 9 `source_binding` (row-7 digest) | same-size differing-SHA source | clean source | yes, and driven one level higher through `wpi_main`'s real order |
| row 9 `attestation_mismatch` | synthetic attestation state | `repaired` | executed in both fence runs; the state is not reachable in production, and the package does not claim it is |
| R3 canon/mount gates | 5 falsifications | - | yes, all five re-falsified independently (§5) |

Adjacent-boundary search for a false PASS, false FAIL or ambiguous STOP:

- **Row 6, accepting direction.** 18 terminator arms + 9 header-shape arms +
  `nul`, `lower_install`, `bom`, EOF-dangling, comment-bridge, blank-terminate,
  odd/even backslash. Every accepting `install_section=absent` I could produce was
  one systemd also reads as having no `[Install]`. No false PASS found.
- **Row 6, refusing direction.** Every `present` was one systemd also loads with a
  real `[Install]`. No false FAIL found. The three `section_header_grammar` STOPs
  are on fragments systemd refuses to load at all.
- **Row 9.** 25 rendering arms (§3.3). Every accepting line is the protected
  assignment exactly once with the value systemd resolves. Malformed and
  unattributable renderings STOP; evaluable deviations FAIL. No false PASS.
- **STOP/FAIL polarity.** `unit_source_not_attested` and
  `unit_source_attestation_mismatch` are rc 3 (the observation did not happen),
  while a duplicate or altered value is rc 1 (evaluable deviation). Both are the
  truthful class.

## 8. Thirteen-pattern adjudication

| Pattern | Adjudication |
|---|---|
| 1 STOP is not a result | **Clean.** The two executed false PASSes are gone; `cr_only_file` moved from an rc-3 STOP to the truthful `present` rc 1. Remaining STOPs (`nul_byte`, `section_header_grammar`, unattested source) are genuine inabilities to evaluate; for the three grammar shapes systemd itself refuses the unit. See NIT-6 for the one conservative residue. |
| 2 Whose kernel answered? | **Clean with a nit.** The oracle domain is real and gated (`major_minimum=259 major_ok=yes`), every arm executes live, and a behavioural change on a higher version surfaces as `HARNESS_ORACLE_FAIL` rather than silence. The published transcript no longer names the exact version - see NIT-2. |
| 3 Leaf is not path | **Clean.** Component and mount binding retained; the C1 mount-projection residual is still disclosed rather than dropped. |
| 4 Child environment | **Clean.** Absolute pinned tools, `python3 -I -S`, isolation re-asserted inside both embedded parsers before any work, one process and one namespace per (subject, arm). |
| 5 Parser completeness | **Clean.** `re.split("\r\n|\r|\n", text)` is exactly systemd's terminator set, executed against nine candidate byte classes in two shapes; the alternation order (CRLF before bare CR) is stated and correct. |
| 6/7 Status before stdout | **Clean.** rc, empty child stderr, absence of non-empty captured `ro.*.stderr` leaves, absence of `RP7_STOP`, and an exact single-line record count are all adjudicated before semantics, in both `run_case` and `subject_case`. The `b4_unattested` disposition correctly declares an entitlement of **zero** parser records because it STOPs before the tokenizer runs. |
| 8 Name is not identity | **Clean.** Row 9's accepting line is now bound to the fragment's exact bytes rather than to a rendering that identifies no source. |
| 9 Sentence outruns probe | **Clean, and materially improved.** The old "the tokenizer refuses the unit-source attack" overclaim is explicitly withdrawn in the code comment, in `STATUS_RP7.md` and in the report, and replaced by the claim that is executed. The transcript exception is withdrawn rather than restated. The duplicate invariant is labelled stronger-than-systemd with the systemd half executed. The row-8 fixture-fidelity limit and the "a real manager may never render the name twice" limit are both written down. |
| 10 Evidence that can fail | **Clean.** Every count in the summary is a counter this run incremented and is compared to a declared expectation (`43/43/12`, `23/15/65`, `14`, `11`); a dropped arm aborts. Identity is asserted before and after. Fixture byte censuses are asserted before any answer is read - and that gate caught my own corrupted fixture. The canon layer's five gates were all falsified independently. |
| 11 Declared instrument not executed | **Clean.** The fence extracts and drives the delivered functions, refuses a residual `wpi_main "$@"`, and requires the named functions in every subject; `repaired.sh` is the asserted block bytes. I drove the same production functions - and `wpi_main`'s real B2-then-B4 order - for my own findings. |
| 12 Unmodelled input disappears | **Clean.** The previously unmodelled bare CR no longer disappears; a logical line starting `[` that is not a well-formed header STOPs with a coverage reason instead of being ignored; NUL and undecodable bytes STOP. |
| 13 Terminal disposition | **Clean.** Each environment token receives exactly one disposition; unconsumed/malformed tokens STOP before target semantics; the two-lex agreement check refuses a rendering that cannot be attributed token-for-token; per-subject arm counts are conserved and asserted. |

## 9. Optional nits (no required repair)

- **NIT-1 - unqualified terminal counts.** `D026_SUMMARY ... red_green_pairs=43
  controls=12` still carries no "single-subject" qualifier, although the fence
  body (`SELF_QA_RP7.md:926`) and the report both state plainly that a
  single-subject RED "is only a fixture the already-fixed code rejects". A reader
  of the terminal line alone would over-read it. This is the prior round's NIT-2,
  unchanged; the multi-subject counters beside it are the ones carrying real
  falsification weight.
- **NIT-2 - the published transcript no longer names the oracle.**
  `%SYSTEMD_ANALYZE%` and `%SYSTEMD_VERSION%` are canonicalised, so the published
  bytes record only `major_minimum=259 major_ok=yes`. That is the deliberate cost
  of host-independent determinism and is within the R3 contract, the real values
  are retained in run-owned raw evidence, and the prose names
  `systemd 259 (259.5-0ubuntu3)` - but the transcript alone cannot answer "which
  manager answered". Adding a canonical major-version token (e.g.
  `oracle_major=259`) would restore that without reintroducing per-host variance.
- **NIT-3 - asymmetric line adjudication.** `subject_case` compares the terminal
  line by exact string equality; `run_case` uses `grep -F -m1` over the whole
  stdout, so a matching line anywhere satisfies it. Exact rc equality is still
  required, so the risk is small, but the two halves of the fence hold different
  standards for the same kind of assertion.
- **NIT-4 - whose two runs.** `STATUS_RP7.md`'s documentary bullet reports scratch
  roots `...MxAGFJ3F` / `...CXTNsYx4` and mount digests `0ba118d4...` /
  `90021811...` for "the fence was run twice back to back on this workstation"
  without saying these are the **implementer's** runs; the Lead's two retained
  runs used different roots again, and mine a third pair. The chronology table
  keeps the two roles distinct, so this is ambiguity rather than contradiction,
  but one word would remove it.
- **NIT-5 - the binding record is not exported.** `RP7_RAW_EVIDENCE_DIR` retains
  `mount_projection_1/2/decoy.txt` (the summary lines) but not the
  `ro.*.mount_projection.tsv` the digest is taken over, so a reader of the
  retained evidence cannot re-check the `kind=point` binding without re-running. I
  verified the gate by falsification (§5 arm 3) and rebuilt a projection myself to
  confirm the record's shape and digest, so nothing is unproven - it is only
  unproven *from the exported evidence alone*.
- **NIT-6 - one conservative STOP.** A fragment containing a NUL byte is parsed
  normally by systemd 259, which sees a real `[Install]`; the block STOPs
  `nul_byte` at rc 3. The direction is safe (non-accepting), the fixture is
  declared in band, and row 7's digest pin would refuse such a fragment anyway -
  but it is an inability-to-evaluate on an input the manager reads without
  difficulty.

None of the six requires a code or evidence change for this candidate to be
accepted.

## 10. Scope, safety and repository state

The repair commit `80cbed46` changes exactly the four kickoff-owned artifacts,
all under `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/`
(`git show --stat`: 4 files, 1756 insertions, 427 deletions). Everything else in
the `2d0f24d0..80cbed46` range is process documentation added by the two
neighbouring commits. No Pine, parity, `MTC_V2`, schema, broker, deploy,
credential or trading surface is touched.

This session performed **no Git mutation** of the audited repository: no stage,
commit, checkout, reset, stash, branch, push, worktree or config change. HEAD
remained `4d28debbc69f35d21c022fd314309aa052e3a4aa` throughout and
`git status --porcelain` was empty (0 paths) immediately before this write. The
two pre-existing stashes (`pathscope-...-2026-08-13`, `-2026-08-14`) are untouched
and predate this session. The only path this session writes inside the repository
is:

```text
MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_R1_R4_CLAUDE_T0_AUDIT_2026-08-15.md
```

All dynamic evidence is outside every repository, under the run-owned Linux
scratch root `/var/tmp/r7t0cla_audit` plus each fence run's own `mktemp -d` root,
which the fence removed at exit. The `git init` in §2 created a repository inside
that scratch root only; it reads the audited object store through
`objects/info/alternates` and wrote nothing to it. The four materialised frozen
artifacts were re-hashed after all execution and are byte-identical to §1.

No host contact, network probe, SSH/SCP, deployment, service action, credential
handling, ARM, order, TESTNET, mainnet, Pine, parity, MTC or trading action
occurred. `systemd-analyze verify` was used read-only on local fixture files and
contacted no service manager. The single tmpfs mount in §5 was created inside my
own scratch tree, existed for the duration of one guard window, was unmounted
immediately, and left no residual mount. No sub-delegation; no other model was
invoked.

**Two environment observations, disclosed because they are visible in the
evidence and are not attributable to the candidate.** First, a stale
`/tmp/rp7_rows_1_9_rebuild_evidence.6iWnh8CH` tree from 10:46 predated my session
and was not created or removed by me. Second, a concurrent Codex process
(`/var/tmp/r7t0cdx-codex-rp7.FXGIVfZu/fence.sh`, started 10:49:57) was executing
the same fence in the same WSL distribution and overlapped the tail of my run A.
I did not read that tree or any Codex output. The overlap is in fact corroborating
rather than contaminating: it is precisely the collision the run-owned `mktemp`
root was introduced to survive, my run A and run B produced identical published
bytes across and outside that window, and both equal the transcript frozen in
`SELF_QA_RP7.md`.

## 11. Verdict

**PASS-WITH-NITS** - accepting, zero required repairs.

All four frozen identities re-derive exactly from Git object bytes. The complete
rows-1-9 fence executed twice sequentially from a run-owned Linux materialisation
of those bytes at rc 0, 250 lines, zero stderr, zero abort, capture-collision,
unexpected-stderr or ERR-trap contamination, unchanged identity before and after,
and all fourteen systemd plus eleven environment oracle arms live. The two
published transcripts are raw byte-for-byte identical to each other and to the
transcript frozen in `SELF_QA_RP7.md`, with no external editing, path replacement,
normalisation or exclusion, while the real scratch roots, mount projections, decoy
projections and raw transcripts all differed and remained bound.

R1 is closed at the production caller: the manager's quote removal precedes
validation - executed on my own fixtures, including a mid-name split-quote arm -
so the raw spelling cannot reach row 9, the attacked unit source is refused by the
row-7 digest with row 9 never reached, the accepting line now carries an earned
source-binding token, and the quoted controls and the declared duplicate policy
remain truthful. R2 is closed: three byte-identical chronology tables, every Lead
sentence scoped to its byte identity, no claim that later work already occurred.
R3 is closed: five independent falsifications of the canonicalisation and mount
gates all fail closed, and a real mount change surfaces as a published STOP. R4 is
closed: two false PASSes and one inability-to-evaluate on the frozen cap-override
committed bytes reproduced and repaired, with no unmodelled terminator surviving a
sweep of nine byte classes in two shapes and no regression in any control.

Six optional nits are recorded in §9; none is a required repair.

This verdict does not fill T0 acceptance on its own. Both mandatory flagship
verdicts are required, and the Lead owns the combined adjudication.
