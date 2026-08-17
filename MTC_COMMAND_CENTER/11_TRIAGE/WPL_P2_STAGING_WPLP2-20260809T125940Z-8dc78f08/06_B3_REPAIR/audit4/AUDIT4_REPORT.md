BLOCK

# Findings

## 1. REQUIRED - MEDIUM - Audit-3 finding 2 is still not closed under D026

`round4/SELF_QA.md` now contains the missing command constructions and real
outputs, but several claimed "exact executable commands" are still templates or
depend on shell state that the recorded command does not establish.

Concrete failure scenarios:

1. Item 1 cwd RED (`SELF_QA.md:453-458`) copies the current `$QA/arm.sh`.
   Following the document in order, that file was most recently overwritten by
   the round-4 GREEN construction at lines 434-442. The recorded command
   therefore runs GREEN and cannot produce the stated round-2 rc-0 output. A
   round-2 rebuild is required, but is supplied only as prose state.
2. Item 4 (`SELF_QA.md:721-746`) records commands containing the literal quoted
   path component `<FIX>`. Executed as written, those commands look for a file
   named `<FIX>` and cannot produce the listed NaN, Infinity, or -Infinity
   outputs. The required substitutions are listed later, but the exact commands
   actually executed are not recorded.
3. Item 6 (`SELF_QA.md:938-954`) records `STUB_CASE=<CASE>`. Executed literally,
   this is shell syntax, not the `twoline`, `oneline2`, `wrapper`, or `wrongpath`
   commands that produced the closure outputs. The table lists the values but
   does not record the exact GREEN command for any one of them.
4. The older item-5 closure and sweep arms similarly refer back to the generic
   `<PRE>/<SRC>/<FILE>/<FN>/<FX>` form (`SELF_QA.md:797-809,903-905,922`) rather
   than recording the concrete commands. The new directory RED/GREEN commands
   for both blocks are concrete and valid, but that does not make every item-5
   closure command exact.

This is the same evidence-contract defect as audit-3 finding 2. A parameterized
recipe plus a value table is reproducible, but it is not the exact executable
command required by the kickoff and D026. The statement at
`SELF_QA.md:409-411` that every command is the exact command executed is therefore
false. Items 2 and 3 remain adequately recorded; the new directory read-error
RED/GREEN pairs are also adequately recorded.

## 2. OPTIONAL NIT - LOW - The disclosed mid-table limitation is slightly broad

The limitation is real and openly disclosed: after at least one complete record,
an empty-buffer nonzero Bash `read` has the same status and field state as clean
EOF in this implementation. It can therefore be accepted as EOF.

The wording says a read error raised mid-table is generally indistinguishable.
That should be narrowed to a read error that populates no field after one or more
complete records. A nonzero read that leaves a partially populated record is
already distinguished by the existing `truncated=1` arm and STOPs. This wording
overstates the residual; it does not create a false admission or weaken the fix.

# Finding 1 closure - independently verified

Audit-3 finding 1 is CLOSED. The executable delta in each script adds the same
zero-record, empty-field, nonzero-read STOP and changes no other executable arm.

Directory-as-mounts-source fixture, with scratch paths normalized to `<QA>`:

```
RPD round 3 RED:
<QA>/arm.sh: line 30: read: 0: read error: Is a directory
RPD_conf_dir_no_mount_boundary path=/etc/mtc-bridge source=<QA>/fix2/mounts/adir records=0
RC=0

RPD round 4 GREEN:
<QA>/arm.sh: line 30: read: 0: read error: Is a directory
RPD_STOP reason=mount_table_read_error path=<QA>/fix2/mounts/adir records=0 read_rc=1 detail=nonzero_read_populated_no_field_and_consumed_no_record
RC=3

B3 round 3 RED:
<QA>/arm.sh: line 31: read: 0: read error: Is a directory
B3_conf_dir_no_mount_boundary path=/etc/mtc-bridge source=<QA>/fix2/mounts/adir records=0
RC=0

B3 round 4 GREEN:
<QA>/arm.sh: line 31: read: 0: read error: Is a directory
B3_STOP reason=mount_table_read_error path=<QA>/fix2/mounts/adir records=0 read_rc=1 detail=nonzero_read_populated_no_field_and_consumed_no_record
RC=3
```

Populated matching record with no final newline, against round 4:

```
RPD_STOP reason=mount_table_unterminated_final_record path=<QA>/fix2/mounts/nonl records=1 hits=1 first_target=/etc/mtc-bridge
RC=3

B3_STOP reason=mount_table_unterminated_final_record path=<QA>/fix2/mounts/nonl records=1 hits=1 first_target=/etc/mtc-bridge
RC=3
```

# D026 sampling and arithmetic

In addition to the four read-error RED/GREEN commands and the two unterminated
record commands above, these three concrete GREEN samples reproduced the stated
results:

```
Item 1, PYTHONPATH shadow:
RPD_tool name=env path=/usr/bin/env mode=755 owner_numeric=0:0 resolution=pinned_absolute
RPD_tool name=python3 path=<QA_PY> mode=755 owner_numeric=0:0 resolution=pinned_absolute
RPD_STOP reason=install_manifest_unparsable path=<QA>/fix1/wrong.json
RC=3

Item 4, NaN manifest with correct bindings:
RPD_tool name=env path=/usr/bin/env mode=755 owner_numeric=0:0 resolution=pinned_absolute
RPD_tool name=python3 path=<QA_PY> mode=755 owner_numeric=0:0 resolution=pinned_absolute
RPD_STOP reason=install_manifest_non_json_constant path=<QA>/fix1/nan.json detail=NaN_Infinity_-Infinity_are_not_JSON_values
RC=3

Item 6, two-line EACCES plus ENOENT diagnostic:
B3_STOP reason=boundary_diagnostic_multiline path=/etc/mtc-bridge/mtc-bridge.env rc=1 detail=stat: cannot stat '/etc/mtc-bridge/mtc-bridge.env': Permission denied stat: cannot stat '/etc/mtc-bridge/mtc-bridge.env': No such file or directory
RC=3
```

The corrected subcount arithmetic is exact:

```
RP1 A = 5 + 5 + 7 + 3 + 1 = 21
RP1 B = 10 + 18 + 15 + 11 + 10 = 64
RPD A = 11 + 11 = 22
RPD B = 5 + 10 + 4 + 10 + 15 + 11 = 55
Total = 43 A / 119 B / 3 C
```

Section 6.13 is correctly labelled 11.

# Round-3 to round-4 regression sweep

The round-4 directory contains exactly the required four files and all four are
ASCII with LF line endings. Both scripts pass `bash -n` with rc 0. Their hashes
match the recorded values:

```
6f3ea022b68d80a552c4ebcb771bbb2a707bdab46a383d605ffc5b88b884becc  RP1-B3.sh
3b9e78e87cecdc10ab1a10d14e79dbff530968e4075277117743c88976fa813c  RPD-VERIFY.sh
```

The executable diff of each script is confined to the intended
`*_assert_no_mount_at_or_under` branch. All other executable lines are unchanged.
The documentation delta is confined to the round-4 fix, QA evidence, corrected
counts, and associated disclosure. No audit-3 CLOSED code path was weakened and
no unrelated executable delta was found.

Final verdict: BLOCK. Audit-3 finding 1 is closed, but audit-3 finding 2 survives.
Per the kickoff, this escalates to the owner and there is no round 5.
