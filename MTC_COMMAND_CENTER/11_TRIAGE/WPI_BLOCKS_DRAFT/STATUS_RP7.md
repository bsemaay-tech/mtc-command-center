# RP7 status

Status: **rows-1-9-EXTENDED-PENDING-FRESH-SAME-BYTE-T0-AUDITS**

Current block identity is `132886` /
`a4af307c34cbc6092676b0838e17090dcadeb1116703773f1dbd42749670b243`. The Lead
independently reproduced the complete published fence against these exact bytes
on 2026-08-15 (rc 0, 124.8 s, all 9 systemd oracle arms and final D026 summary
matched). No auditor has accepted these bytes. Both required T0 auditor slots
are PENDING and must run fresh **against this same byte identity**. Commit `90cbeac4` is a recorded implementer repair
against the superseded `127491` bytes, not an acceptance, and it does not carry
forward. No acceptance is claimed here.

These bytes are the product of the single owner-authorized cap-override repair
round (`WPI_OWNER_DECISIONS_2026-08-13.md` §4). That authorization covers one
repair plus the two fresh mandatory T0 flagship audits; it waives no finding, no
acceptance standard, and no safety gate, and grants no host, deployment,
credential, service, broker, ARM, order, TESTNET or mainnet authority.

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
- **Run-owned scratch root (new).** The fixed `/tmp/rp7_rows_1_9_rebuild_evidence`
  root was a collision hazard and is replaced by a `mktemp -d` root created per
  run, with the recursive-removal guard kept and matched to the run-owned shape.

Documentary state:

- `SELF_QA_RP7.md` replaces the rejected simulated rows 1-9 matrix with an
  embedded `sed | bash` rebuild fence and its executed transcript. The fence
  extracts the delivered `RP7-WPI-RO.sh` bytes, asserts identity before and
  after, and drives the block's own B2/B4 functions. Count history: 24 RED/GREEN
  pairs and 4 controls after round-3 repair; 29 pairs and 5 controls after
  round-4 repair; 35 pairs and 7 controls for the `127655` bytes. **Current count
  for the `132886` bytes: 36 single-subject RED/GREEN pairs and 9 controls, plus
  48 multi-subject arms over 5 named subjects (11 RED / 10 GREEN / 27 CONTROL),
  plus 9 executed `ORACLE` arms**, `result=PASS`, rc 0, 0 stderr bytes, 156
  stdout lines, 125 s.
- The `SELF_QA_RP7.md` transcript is the verbatim stdout of a real fence run
  against the `132886` bytes. The fence was run three times on this workstation.
  Because the scratch root is now run-owned, transcripts are compared after
  substituting each run's own `HARNESS_SCRATCH_ROOT` path; so normalised, a fresh
  run of the published fence reproduces the pasted transcript on **155 of 156
  lines**. The single differing line is `HARNESS_ATTESTED_MOUNTINFO sha256=`, a
  mount-namespace projection digest that is not evidence for or against any row
  predicate. Its per-run variation is no longer unexplained: the projection
  includes a `kind=point path=$WPI_UNIT_FRAGMENT` record, that path lives under
  the run-owned root, so the digest must differ per run. The block requires only
  intra-run consistency of that value, which `wpi_mount_guard_begin` re-checks and
  which held on every arm of every run.
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
bytes=132886
sha256=a4af307c34cbc6092676b0838e17090dcadeb1116703773f1dbd42749670b243
cr_bytes=0
bash_n=0
red_green_pairs=36
controls=9
multi_subject_arms=48
multi_subject_red_green_control=11/10/27
multi_subject_subjects=5
systemd_oracle_arms=9
fence_stdout_lines=156
fence_rc=0
fence_stderr_bytes=0
auditor_acceptance=none_yet_both_T0_slots_pending_same_bytes
independent_lead_run=pass_2026-08-15_rc0_elapsed_124.8s_oracle9_summary_matched
previous_capoverride_bytes=127655
previous_capoverride_sha256=beacf85b628e419d911416dc1ee51a382f742d90cbabe29602e60c4f52d809a8
previous_capoverride_superseded_reason=REQUIRED_1_row6_CR_normalisation_missing_false_FAIL
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
round.
