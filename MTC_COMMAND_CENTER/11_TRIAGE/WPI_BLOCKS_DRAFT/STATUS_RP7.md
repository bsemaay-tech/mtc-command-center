# RP7 status

Status: **rows-1-9-EXTENDED-PENDING-FRESH-SAME-BYTE-T0-AUDITS**

Current block identity is `137981` /
`4caed4aecc91cada3b8b99f8ff06d7ba0d7376b2bc07e92c298f4a7b7ca0900c`.

## Provenance of record - one chronology

This table is the single provenance statement for RP7 rows 1-9. It is reproduced
identically in `SELF_QA_RP7.md` and `RP7_ROWS_1_9_REPORT_2026-08-13.md`. Any
statement elsewhere is scoped to the byte identity it names and does not carry
forward.

| byte identity | implementer self-QA | independent Lead run | flagship auditor verdicts |
|---|---|---|---|
| `108301` (round 9) | yes | yes | two accepting verdicts - superseded, does not carry forward |
| `127491` (round 4, `90cbeac4`) | yes | yes, recorded at the time | none |
| `127655` (post-round-4, `8ec89675`) | yes | yes, recorded at the time, against a different fence | none |
| `132886` (cap-override, `2d0f24d0`) | yes | yes - complete fence, 2026-08-15, rc 0, 124.8 s | Codex `gpt-5.6-sol` **BLOCK**, Claude `claude-opus-5` **REQUEST_CHANGES** |
| `137981` (R1-R4 repair) | yes | yes - two complete retained fence runs, 2026-08-15, rc 0, raw `cmp` identical | **not yet - both T0 slots PENDING** |

Neither T0 flagship accepted `132886`; between them they left four REQUIRED
findings, R1 through R4, and the bytes that close those findings are new. After
the implementer self-QA, the Lead independently ran the complete fence twice
against `137981`: both runs returned rc 0 with zero stderr and raw published
stdout compared identical. No auditor has seen these bytes yet, and no
acceptance is claimed here. Commit `90cbeac4` is a recorded implementer repair
against the superseded `127491` bytes, not an acceptance, and it does not carry
forward to `127655`, `132886` or `137981`.

These bytes are the product of the owner-authorized R1-R4 repair round dispatched
by `KICKOFF_CLAUDE_RP7_R1_R4_REPAIR_2026-08-15.md`, opened after
`RP7_CAP_OVERRIDE_FINAL_OWNER_BOUNDARY_2026-08-15.md` returned RP7 to the owner
boundary. That authorization covers one repair plus the two fresh mandatory T0
flagship audits; it waives no finding, no acceptance standard, and no safety
gate, and grants no host, deployment, credential, service, broker, ARM, order,
TESTNET or mainnet authority.

Scope: `RP7-WPI-RO.sh` now implements the remote RO-stage predicates for rows
1-23 and still records row 24 as operator-side only. This is the owner-decided
rows 1-9 extension over the previously accepted round-9 bytes. The extension
re-opens RP7 acceptance: the changed bytes need fresh independent acceptance,
and the Audit-2 matrix row for RP7 is PENDING for both required auditors.

Material state added in this extension:

- `RP7_SECTION B2_rows_1_7` is inserted before `RP7_SECTION B3_rows_10_15`.
  It performs one bounded `systemctl show` capture for rows 1-5, proves every
  property record present before interpreting its value, then checks row 6 with
  a trusted `python3 -I -S` unit-file line parser and row 7 with the existing
  fragment digest predicate.
- `RP7_SECTION B4_rows_8_9` is inserted after B2 and before B3. It performs one
  bounded `systemctl show` capture for the ten row-8 sandbox properties plus
  `Environment`, compares the rendered sandbox pins, and tokenizes row 9 rather
  than substring-matching it.
- The new pin class is: ten rendered row-8 sandbox values, the expected
  `FragmentPath`, and the expected-empty `DropInPaths` set for row 5.
- The terminal claim moved from `rows_10_23...` to `rows_1_23...`, while the
  disclaimer still stays about the manager that answered in the attested
  execution domain and does not claim host authority.
- The rows 1-9 evidence rebuild exposed and fixed one real B2 row-6 defect:
  `wpi_assert_fragment_has_no_install_section` preserved the parser rc and now
  consumes the parser capture before `wpi_mount_guard_end` overwrites the active
  capture descriptors.
- Round-2 repair hardens `ExecStart` parsing for richer started-unit
  `systemctl show` renderings: semicolons inside bracketed runtime fields no
  longer split top-level fields, unknown keyed runtime fields are ignored, and
  `path`, `argv[]`, and `ignore_errors` are still presence-checked and matched
  exactly.
- Round-3 repair reverts row 6 to exact-case `Install` matching. Lowercase
  `[install]` is again a CONTROL because systemd ignores it as an unknown
  section rather than treating it as an install section. The round-2
  case-insensitive change was a verify-before-fix failure based on a false
  systemd-section parsing claim.
- Round-4 repair implements the full row-1 amended STOP domain: B2
  manager/query/table-parse failures, absent `ActiveState`, and empty or
  unrecognized `ActiveState` values all stop as
  `system_manager_unreachable operation=show` before the first state
  comparison. The row-5 truncated-show fixture was moved to row 1 because this
  is now the first divergence.
- Round-4 repair also made row 9 fail closed on environment tokens without a
  valid `NAME=` assignment before target semantics. That row-9 repair stands.
- Round-4 additionally claimed to carry "row-6 systemd continuation state across
  ignored comment/blank lines". **That claim was false and is superseded.** Blank
  lines were bridged as well as comments, which let a real `[Install]` section be
  swallowed as continuation text and reported `install_section=absent` — a false
  PASS on a row-6 safety predicate. See the post-round-4 regression repair below.
- Post-round-4 regression repair (bytes `127655`): the row-6 rule of
  record is now exactly — a **comment** line (`#` or `;` after leading
  whitespace) **bridges** an open continuation; a **blank** line **terminates**
  it, and the accumulated logical line is classified immediately. Continuation is
  decided by an **odd** count of trailing backslashes; a continuation still open
  at EOF is flushed and classified; a section header carrying a trailing comment
  is a `section_header_grammar` STOP rather than a silently accepted header. The
  repair adds a `blank_no_bridge` RED/GREEN regression guard plus five further
  pairs, and two no-weakening CONTROL arms (`multi_comment_bridge`,
  `odd_backslash_three`) proving comment bridging was not deleted to make the
  blank-line case pass. This is a repair record, not an acceptance.
- **Cap-override repair, REQUIRED-1 (current bytes `132886`).** The post-round-4
  regression repair also silently dropped round 4's `physical.rstrip("\r")`
  normalisation, leaving `physical.lstrip(WS)`. That is a **false FAIL** on the
  row-6 safety predicate: systemd reads a value line ending in backslash + CRLF
  as continuing, so the `[Install]` after it is continuation text, but the block
  reported `install_section_present` at rc 1. The repair restores exactly
  `line=physical.rstrip("\r").lstrip(WS)`. The strip is CR-only on purpose: a
  broad `rstrip()` would also eat trailing spaces, fabricate a continuation
  systemd does not perform and swallow a **real** `[Install]` — the false PASS
  direction. Both errors now run as executed mutants (`mut_nocr`, `mut_broad`)
  beside the two real committed blobs.
- **Cap-override repair, REQUIRED-2.** The fence now executes every row-6 pair
  against named other byte sets, not only against the delivered bytes: five
  subjects (`round4` `127491`, `current` `127655`, `repaired`, `mut_nocr`,
  `mut_broad`), each in a **separate process** with a scratch namespace unique to
  (subject, arm), asserting each subject's exact rc and exact terminal line.
  48 multi-subject arms: 11 RED, 10 GREEN, 27 CONTROL.
- **Row-9 D026 completion.** Literal fixtures added for mid-name quote rejection
  (`environment_token_name_not_literal`), the fully quoted and value-quoted valid
  controls, and the same-value duplicate refused under the explicitly declared
  stronger-than-systemd single-occurrence invariant.
- **Row-6 systemd oracle (new).** The one row-6 claim that is about *systemd*
  rather than about this block is now executed in the published fence: nine
  `ORACLE` arms run `systemd-analyze verify` on fixtures whose unknown key names
  the section it landed in, with three controls first. Established: trailing CR
  is part of the line terminator and **continues**; trailing spaces are line
  content and **do not**; an even backslash count does not. The fence aborts
  loudly if `systemd-analyze` is unavailable rather than skipping the arms.
- **Fixture terminator census (new).** This rule was reproduced wrongly twice
  during the repair, once in each direction, both times from a fixture that had
  silently lost a byte through one shell layer too many. `fixture_terms` /
  `fixture_expect_terms` now assert a per-line terminator census for every
  CR/space-sensitive fixture before any parser or oracle sees it, and the census
  is printed on each `ORACLE` line.
- **Run-owned scratch root.** The fixed `/tmp/rp7_rows_1_9_rebuild_evidence`
  root was a collision hazard and is replaced by a `mktemp -d` root created per
  run, with the recursive-removal guard kept and matched to the run-owned shape.
- **R4 repair — systemd line terminator modelled (current bytes `137981`).** The
  cap-override parser split on `text.split("\n")` and then stripped a *run* of
  trailing CRs. That models only `LF` as a terminator. Executed against systemd
  259: a bare `CR` ends a line, `CR CR LF` is a terminator plus a blank line that
  terminates a continuation, and a CR-only file parses normally. Two fragments
  systemd loads **with** a real `[Install]` section were reported
  `install_section=absent` at rc 0 — a **false PASS** on the row-6 safety
  predicate — and a third could not be evaluated at all. The repair replaces two
  lines with `for physical in re.split("\r\n|\r|\n",text)` plus a plain
  `lstrip(WS)`. A plain revert to `str.splitlines()` is **not** equivalent and is
  executed as the mutant `mut_splitlines`: it also breaks at `VT`, `FF`, `FS`,
  `GS`, `RS`, `NEL`, `U+2028` and `U+2029`, which systemd treats as content, and
  produces the opposite false FAIL.
- **R4 evidence.** Five new `ORACLE` arms vary the terminator identity itself —
  the dimension the previous nine arms never varied. New production-path D026
  pairs for `bare_cr_install`, `multi_cr_install` and `cr_only_file` run against
  the real committed `132886` blob (new named subject `capoverride`) plus
  `127655`, `127491` and three mutants. `bs_cr_then_header` and
  `vt_after_backslash` are the no-weakening controls that stop "model the CR"
  becoming "split on everything".
- **R1 repair — row 9 bound to the production normalisation boundary.** The row-9
  D026 arm injected a raw mid-name-quote spelling directly into fake `systemctl
  show` output; production reads the manager's *effective* rendering instead.
  Eleven new `ENV_ORACLE` arms execute that boundary: systemd prints the token it
  validated with the quotes already removed, so quote removal precedes validation
  and the manager renders the clean protected assignment. The claim that the
  tokenizer refuses the unit-source attack is **withdrawn as an overclaim**; the
  guard's true scope is rendering attribution and it is unchanged. What refuses
  the attacked source is the row-7 fragment digest plus row-5 empty drop-ins, now
  executed as a same-size differing-SHA D026 pair through the real digest
  predicate.
- **R1 repair — unattested source is now a STOP.** `wpi_assert_b2_rows_1_7` sets
  `WPI_UNIT_SOURCE_ATTESTED` only after rows 1-7 complete, and
  `wpi_assert_environment_start_mode` refuses to emit an accepting line without
  it (`unit_source_not_attested`, `unit_source_attestation_mismatch`, both rc 3).
  The accepting line now carries the earned token
  `source_binding=unit_fragment_digest_attested_dropins_empty`. RED against
  `132886`, `127655` and `127491`, GREEN against `137981`.
- **R1 duplicate policy.** Retained and now executably declared: the `ENV_ORACLE`
  arms record that systemd accepts both duplicate forms without a diagnostic
  while row 9 refuses them, so the invariant is a declared narrowing. The block
  discloses that whether a real manager ever renders the protected name twice is
  not established by this fence.
- **R3 repair — the published transcript is deterministic (new).** The fence now
  separates the raw transcript from the published one: all output is written to a
  run-owned raw file and canonicalised at the publication boundary, replacing
  exactly five presentation values (`%RUNROOT%`, `%REPO%`,
  `%HOST_MOUNT_PROJECTION%`, `%SYSTEMD_ANALYZE%`, `%SYSTEMD_VERSION%`) with a
  declared hit count for each. Two fresh sequential runs produced **raw
  byte-identical** published transcripts (`cmp`, no external editing), while the
  real scratch roots and mount-projection digests differed. The layer fails
  closed: declared counts, residue detection, in-run re-derivation of the mount
  digest, a binding-record check, and a decoy rebuild that must differ. All five
  gates were falsified in run-owned scratch copies.
- **R3 repair — the published body runs unedited.** The repository root is derived
  from the directory the published extraction command cds into rather than
  hard-coded, so no reproduction needs to edit the fence first.
- **R2 repair — provenance.** The single chronology table above, reproduced
  identically in all three documents, now records the later Lead verification
  without rewriting the implementer-time evidence or claiming an auditor result.

Documentary state:

- `SELF_QA_RP7.md` replaces the rejected simulated rows 1-9 matrix with an
  embedded `sed | bash` rebuild fence and its executed transcript. The fence
  extracts the delivered `RP7-WPI-RO.sh` bytes, asserts identity before and
  after, and drives the block's own B2/B4 functions. Count history: 24 RED/GREEN
  pairs and 4 controls after round-3 repair; 29 pairs and 5 controls after
  round-4 repair; 35 pairs and 7 controls for the `127655` bytes; 36 pairs, 9
  controls, 48 multi-subject arms over 5 subjects and 9 `ORACLE` arms for the
  `132886` bytes. **Current count for the `137981` bytes: 43 single-subject
  RED/GREEN pairs and 12 controls, plus 103 multi-subject arms over 7 named
  subjects (23 RED / 15 GREEN / 65 CONTROL), plus 14 executed `ORACLE` arms and
  11 executed `ENV_ORACLE` arms**, `result=PASS`, rc 0, 0 stderr bytes, 250
  stdout lines, ~200 s.
- The `SELF_QA_RP7.md` transcript is the verbatim published stdout of a real
  fence run against the `137981` bytes. The fence was run twice back to back on
  this workstation and the two published transcripts are **raw byte-identical**,
  compared with `cmp` and with no external editing, path replacement,
  normalisation or excluded field: sha256
  `d0788122c132e43c25aea52315d53b3596c40c57598e2bbded9b2efa11cae8ab`. The
  previous "155 of 156 lines after an external sed" contract is withdrawn.
  Run-owned isolation is unchanged and is proved still real from the retained raw
  evidence: the two runs had different scratch roots
  (`...MxAGFJ3F` / `...CXTNsYx4`) and different live mount-projection digests
  (`0ba118d4...` / `90021811...`), and their raw transcripts differ on 131 line
  pairs. The mount digest is canonicalised as `%HOST_MOUNT_PROJECTION%` only
  after the fence proves in-run that it is 64-hex, re-derivable, carries the
  `kind=point` binding record for the run-owned fragment, and changes when that
  path is replaced by a decoy.
- Row-8 sandbox pins are disclosed as asserted rendered `systemctl show`
  literals. The rebuild fence proves comparator behavior against fixtures; host
  derivation of those renderings remains a freeze-time act for the flagship
  auditor and owner-visible record. `CapabilityBoundingSet=''` is called out as
  the highest-risk pin for that derivation.
- Preregistration amendment note for row 1: the block implements the active
  predicate by reading `ActiveState` from the bounded `systemctl show`
  property table, not by executing the preregistered verbatim
  `systemctl is-active` command. Rationale: the property-table read keeps row 1
  in the same capture contract as rows 2-5 and avoids raw tool rc becoming the
  row verdict. The labelled preregistration amendment is now present in
  `WPI_PREREGISTRATION_DRAFT.md`; the amended STOP token is `operation=show`.
- The C1 mount-projection digest residual is stated separately: that digest still
  uses a re-resolved name and is intentionally not repaired in this rows-1-9
  round.

Final executable identity:

```text
bytes=137981
sha256=4caed4aecc91cada3b8b99f8ff06d7ba0d7376b2bc07e92c298f4a7b7ca0900c
cr_bytes=0
bash_n=0
red_green_pairs=43
controls=12
multi_subject_arms=103
multi_subject_red_green_control=23/15/65
multi_subject_subjects=7
systemd_oracle_arms=14
env_oracle_arms=11
fence_stdout_lines=250
fence_rc=0
fence_stderr_bytes=0
fence_published_stdout_sha256=d0788122c132e43c25aea52315d53b3596c40c57598e2bbded9b2efa11cae8ab
fence_two_run_published_transcripts=raw_byte_identical_cmp_no_external_editing
auditor_acceptance=none_yet_both_T0_slots_pending_same_bytes
independent_lead_run=pass_2026-08-15_two_retained_runs_rc0_203s_each_raw_cmp_identical
previous_capoverride_bytes=132886
previous_capoverride_sha256=a4af307c34cbc6092676b0838e17090dcadeb1116703773f1dbd42749670b243
previous_capoverride_lead_run=pass_2026-08-15_rc0_elapsed_124.8s_oracle9_summary_matched
previous_capoverride_codex_t0_verdict=BLOCK
previous_capoverride_claude_t0_verdict=REQUEST_CHANGES
previous_capoverride_superseded_reason=R1_row9_production_boundary_R2_provenance_R3_transcript_determinism_R4_bare_CR_terminator_false_PASS
previous_postround4_bytes=127655
previous_postround4_sha256=beacf85b628e419d911416dc1ee51a382f742d90cbabe29602e60c4f52d809a8
previous_postround4_superseded_reason=REQUIRED_1_row6_CR_normalisation_missing_false_FAIL
previous_round4_bytes=127491
previous_round4_sha256=5b00207aff17a9a9f29e056b9f93fb46b2cf640376659bf75b9f33b9b9b3dbe3
previous_round4_superseded_reason=post_round4_regression_repair_row6_blank_line_false_PASS
previous_round3_rows_1_9_bytes=127038
previous_round3_rows_1_9_sha256=ac73485ff75ab6e731bf1bc137ae77f7074cab04700603ab71cba1c591141fe3
previous_rows_1_9_bytes=126182
previous_rows_1_9_sha256=8355cb00fda8af2140d99ff9e97fe458376215dbd39267b2f2958d29fb9aba85
superseded_round2_rows_1_9_bytes=127046
superseded_round2_rows_1_9_sha256=a2ec1d0c47db53a756b7abe0803e7c6e62d42dd4c6b69934332c2eb501c714ad
previous_accepted_round9_bytes=108301
previous_accepted_round9_sha256=0e93f90de7fcefe86fee4137f3ba11ea34b69b120d6a06c304fdde0e9b921e62
identity_changed=yes
```

No host contact, network probe, SSH/SCP, RUNID minting, commit, deployment, or
change outside the rows-1-9 authorized deliverables occurred in this implementer
round. No Git metadata was modified and no `checkout`, `reset`, `stash`,
`commit`, `push` or `worktree` command was run. All dynamic execution evidence
stayed in run-owned temporary trees outside the repository. The four owned files
are LF-only on disk; the Windows checkout convention is CRLF, so that difference
is transport and produces no content delta for the files this round did not
change.
