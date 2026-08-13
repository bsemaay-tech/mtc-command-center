# RP7 status

Status: **rows-1-9-EXTENDED-PENDING-REAUDIT**

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
- Round-4 repair also carries row-6 systemd continuation state across ignored
  comment/blank lines and makes row 9 fail closed on environment tokens without
  a valid `NAME=` assignment before target semantics.

Documentary state:

- `SELF_QA_RP7.md` replaces the rejected simulated rows 1-9 matrix with an
  embedded `sed | bash` rebuild fence and its executed transcript. The fence
  extracts the delivered `RP7-WPI-RO.sh` bytes, asserts identity before and
  after, and drives the block's own B2/B4 functions. It produced 24 RED/GREEN
  pairs and 4 controls after round-3 repair, then 29 RED/GREEN pairs and 5
  controls after round-4 repair.
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
bytes=127491
sha256=5b00207aff17a9a9f29e056b9f93fb46b2cf640376659bf75b9f33b9b9b3dbe3
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
