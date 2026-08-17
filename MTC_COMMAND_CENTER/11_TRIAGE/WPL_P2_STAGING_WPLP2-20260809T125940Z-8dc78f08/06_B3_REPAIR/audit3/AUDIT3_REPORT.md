BLOCK

# Findings

## 1. REQUIRED - MEDIUM - A2-F5 is not closed for read errors

Locations: `round3/RP1-B3.sh:430-462` and
`round3/RPD-VERIFY.sh:430-462`.

The round-3 loops close the populated unterminated-record case, but they still
classify an empty nonzero `read` as ordinary EOF without distinguishing a read
error. On Linux, opening a directory for input succeeds and the first Bash
`read` reports `Is a directory`, returns nonzero, and populates no fields. Both
delivered loops take the `break` at line 437, print a no-mount admission with
`records=0`, and return 0. This directly violates final-list item 5, which
requires STOP on read-error input.

Independent delivered-function fixture output:

```
bash: read: read error: Is a directory
RPD_conf_dir_no_mount_boundary path=/etc/mtc-bridge source=/tmp/audit3-codex-rerun.QcHg0a records=0
RC=0

bash: read: read error: Is a directory
B3_conf_dir_no_mount_boundary path=/etc/mtc-bridge source=/tmp/audit3-codex-rerun.QcHg0a records=0
RC=0
```

This is not a new finding. It is the surviving read-error arm explicitly named
by item 5 of the final list. `DESIGN_NOTES.md:187-189` says that read errors were
driven RED/GREEN, while `SELF_QA.md:146` correctly says the mid-read error arm
was not driven at all.

## 2. REQUIRED - MEDIUM - A2-F7 is not closed under D026

Locations: `round3/SELF_QA.md:202-580` and
`round3/SELF_QA.md:761-779`.

The QA contains actual RED/GREEN outputs, but it does not record exact executable
commands for every item 1-6 closure test as required:

- Item 1 records the RED command, but the GREEN command is only described as
  "identical, with R3 in place of R2"; the cwd GREEN command is also omitted.
- Item 4 says only "the section 5.1 manifest arm with the fixture swapped" and
  gives a results table. No exact RED or GREEN command is recorded.
- Item 5 gives the exact RPD command and says the B3 form "differs only"; the
  exact B3 command is absent. The required read-error arm is not tested at all.
- Item 6 gives the exact RED command, but describes the GREEN construction in
  prose instead of recording its exact command.

Those tests are supplemental, not D026 closure evidence. Items 2 and 3 do have
exact RED and GREEN commands plus real output.

The main three-way totals can be reconciled as 43 A / 115 B / 3 C, but one
subcount is internally wrong: section 6.13 is headed `Manifest binding ... (9)`;
its own text enumerates 3 item-4 arms, 2 item-1 arms, and 6 table arms, which is
11. The stated RPD B subtotal of 53 is reachable only with 11. This does not
change the overall arithmetic, but it defeats the claim that every displayed
count is exact.

# 1. Final-list closure and refutation fixtures

| Item | Status | Round-3 evidence or surviving failure |
|---|---|---|
| 1 | CLOSED | `RPD-VERIFY.sh:146-149,493-531,599-613` pins `/usr/bin/env` and `/usr/bin/python3`, checks the targets, launches with `env -i`, `-I -S -E`, and cwd `/`. Independent PYTHONPATH and cwd shadows both returned `install_manifest_unparsable`, rc 3. |
| 2 | CLOSED | `RPD-VERIFY.sh:176-190,232-320` requires, validates, and compares all three deploy-channel attestation values. An actual matching Linux run printed `bound=attested` and rc 0; each mismatch has a reasoned rc-3 arm. No local `bound=initial` inference remains. |
| 3 | CLOSED | `RP1-B3.sh:177-202,274-295,610-611` requires nonzero numeric service ids and compares `%u:%g` only. The name-mapped 999:999 fixture failed against preregistered 1500:1500 with rc 1. |
| 4 | CLOSED | `RPD-VERIFY.sh:619-631,675-680,710` supplies a raising `parse_constant` callback and maps it to rc 3. The NaN fixture returned `install_manifest_non_json_constant`, rc 3. The same callback covers Infinity and -Infinity. |
| 5 | NOT CLOSED | The populated unterminated-record case now STOPs in both copies, but an empty nonzero read is treated as EOF and returns a false no-mount rc 0. See finding 1. |
| 6 | CLOSED | `RP1-B3.sh:546-589` rejects raw CR/LF, counts error classes, and requires a whole-string C-locale shape. The two-line EACCES+ENOENT fixture returned `boundary_diagnostic_multiline`, rc 3. |
| 7 | NOT CLOSED | The overall category totals reconcile, but exact D026 commands are absent for several item 1-6 GREEN/RED tests, the item-5 read-error arm is untested, and section 6.13 mislabels 11 manifest arms as 9. See finding 2. |
| 8 | CLOSED | A force-inclusive recursive listing of `round3/` contains exactly `DESIGN_NOTES.md`, `RP1-B3.sh`, `RPD-VERIFY.sh`, and `SELF_QA.md`; there are no hidden files, caches, or directories. |

Required audit-2 fixture reruns against delivered round-3 function bodies:

1. PYTHONPATH `json.py` shadow over a manifest containing only
   `THIS IS NOT JSON AND BINDS NOTHING`:

   ```
   RPD_tool name=env path=/usr/bin/env mode=755 owner_numeric=0:0 resolution=pinned_absolute
   RPD_tool name=python3 path=/usr/bin/python3 mode=755 owner_numeric=0:0 resolution=pinned_absolute
   RPD_STOP reason=install_manifest_unparsable path=/tmp/audit3-codex.kUrHS5/wrong.json
   RC=3
   ```

   The cwd-shadow variant independently produced the same STOP and rc 3.

2. NaN manifest with both correct bindings:

   ```
   RPD_tool name=env path=/usr/bin/env mode=755 owner_numeric=0:0 resolution=pinned_absolute
   RPD_tool name=python3 path=/usr/bin/python3 mode=755 owner_numeric=0:0 resolution=pinned_absolute
   RPD_STOP reason=install_manifest_non_json_constant path=/tmp/audit3-codex.kUrHS5/nan.json detail=NaN_Infinity_-Infinity_are_not_JSON_values
   RC=3
   ```

3. Single matching mount record with no final newline:

   ```
   RPD_STOP reason=mount_table_unterminated_final_record path=/tmp/audit3-codex-rerun.QcHg0a/nonl records=1 hits=1 first_target=/etc/mtc-bridge
   RC=3
   B3_STOP reason=mount_table_unterminated_final_record path=/tmp/audit3-codex-rerun.QcHg0a/nonl records=1 hits=1 first_target=/etc/mtc-bridge
   RC=3
   ```

4. Two-line EACCES plus ENOENT diagnostic:

   ```
   B3_STOP reason=boundary_diagnostic_multiline path=/etc/mtc-bridge/mtc-bridge.env rc=1 detail=stat: cannot stat '/etc/mtc-bridge/mtc-bridge.env': Permission denied stat: cannot stat '/etc/mtc-bridge/mtc-bridge.env': No such file or directory
   RC=3
   ```

5. Numeric 999:999 rendered by NSS as `mtc-bridge:mtc-bridge`, with the
   preregistered service owner set to 1500:1500:

   ```
   B3_stat path=/var/lib/mtc-bridge owner_numeric=999:999 owner_name=mtc-bridge:mtc-bridge mode=750
   B3_FAIL reason=path=/var/lib/mtc-bridge owner_numeric=999:999 expected=1500:1500 owner_name=mtc-bridge:mtc-bridge
   RC=1
   ```

Both scripts passed `bash -n` with rc 0. All four round-3 deliverables are ASCII.
The independently computed script hashes match the two hashes in `SELF_QA.md`.

# 2. Round-2 to round-3 regression sweep

The executable delta of both scripts was inspected separately from comments and
documentation. No item that audit 2 marked CLOSED was weakened by the round-3
delta:

- Structural top-level manifest binding remains closed. The audit-1 nested-decoy
  fixture returned `install manifest binds a different release_sha`, rc 1.
- Numeric root ownership remains closed. A numeric 1000:1000 object rendered as
  `root:root` failed against 0:0, rc 1.
- The symlinked configuration-parent fixture still returned
  `conf_dir_is_symlink`, rc 1.
- ENOENT at the boundary remains FAIL, rc 1.
- The local no-temp path probes, writable-tree predicate, input guards, and ERR
  traps are unchanged in the executable diff.
- The new attestation success arm ran against actual Linux self namespace and
  rootfs values and returned rc 0 with `bound=attested`.

No round-3-introduced regression was reproduced. The read-error false pass is an
incomplete implementation of final-list item 5, not a weakening of a round-2
closure.

# 3. QA honesty

Independent count sample:

- RP1 A = 5 + 5 + 7 + 3 + 1 = 21, matching the stated subtotal.
- RP1 B = 10 + 18 + 15 + 11 + 8 = 62, matching the stated subtotal.
- RPD A = 11 item-2/input arms + 11 section-6.10 A arms = 22.
- RPD B = 5 attestation + 8 mount + 4 pinned-tool + 10 path-kind + 15
  metadata + 11 manifest arms = 53.

Therefore the top-level 43 A / 115 B / 3 C figures reconcile, but the section
6.13 label `(9)` must be `(11)`.

D026 presence check:

| Closure item | Exact command plus real RED and GREEN output present? | Assessment |
|---|---|---|
| 1 | NO | RED command is exact; GREEN commands are prose-only. Supplemental. |
| 2 | YES | Exact RED and GREEN commands and outputs are recorded. |
| 3 | YES | Exact RED and GREEN commands and outputs are recorded. |
| 4 | NO | Commands are referenced as a prior arm "with the fixture swapped". Supplemental. |
| 5 | NO | Exact RPD command only; B3 command omitted; read-error arm absent. Supplemental and functionally not closed. |
| 6 | NO | Exact RED command only; GREEN construction is prose-only. Supplemental. |

Final verdict: BLOCK
