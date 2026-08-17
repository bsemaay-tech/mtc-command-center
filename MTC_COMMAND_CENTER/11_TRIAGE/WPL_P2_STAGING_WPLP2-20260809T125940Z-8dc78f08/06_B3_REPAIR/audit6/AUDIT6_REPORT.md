PASS

# Findings

No required finding and no optional nit.

No failure scenario reproduced. A hash drift would have blocked before command
execution. An invalid shared declaration, a missing fixture, an unresolved
reader-supplied value, or output/status drift would have made the literal command
record non-reproducible. None occurred in the valid MSYS/Git-Bash run.

# 1. Code freeze

PASS. SHA-256 was computed before the paste-and-run test:

```
RP1-B3.sh       6f3ea022b68d80a552c4ebcb771bbb2a707bdab46a383d605ffc5b88b884becc
RPD-VERIFY.sh   3b9e78e87cecdc10ab1a10d14e79dbff530968e4075277117743c88976fa813c
DESIGN_NOTES.md 103ffe3811dfd7764bf1b4d9bc47489fbe3cb2d72bca7c5c32e461a82440f23b
```

All three equal the kickoff values. `round6/` contains exactly the four expected
files and no hidden entry.

# 2. Literal paste-and-run

PASS. The fenced bodies of sections 4.0 and 4.1 and the four named section-5
command blocks were extracted from `round6/SELF_QA.md` without changing any
character. `printf '%s'` sent those ASCII characters to the standard input of a
fresh `bash --noprofile --norc` process from
`C:\Program Files\Git\bin\bash.exe` (Git Bash/MSYS Bash 5.2.37). Audit-only block
status markers were appended after, not inserted into, each fenced body. The
fresh shell process returned rc 0 and its stderr was empty.

Section 4.0 actual output and status:

```
(no output)
BLOCK_RC=0
```

Section 4.1 actual output and status:

```
(no output)
BLOCK_RC=0
```

Item 1 cwd RED actual output and status:

```
RPD_manifest_binding path=$QAW/fix1/wrong.json bound=both parser=python3_json_structural keys=top_level_exact
RC=0
BLOCK_RC=0
```

This exactly reproduces the recorded two-line transcript.

Item 4 `nan.json` GREEN actual output and status:

```
RPD_tool name=env path=/usr/bin/env mode=755 owner_numeric=0:0 resolution=pinned_absolute
RPD_tool name=python3 path=$QA_PY mode=755 owner_numeric=0:0 resolution=pinned_absolute
RPD_STOP reason=install_manifest_non_json_constant path=$QAW/fix1/nan.json detail=NaN_Infinity_-Infinity_are_not_JSON_values
RC=3
BLOCK_RC=0
```

This exactly reproduces the recorded four-line transcript.

Item 5 RPD directory-source GREEN actual output and status:

```
$QA/arm.sh: line 30: read: read error: 0: Is a directory
RPD_STOP reason=mount_table_read_error path=$QA/fix2/mounts/adir records=0 read_rc=1 detail=nonzero_read_populated_no_field_and_consumed_no_record
RC=3
BLOCK_RC=0
```

This exactly reproduces the recorded three-line transcript.

Item 6 GREEN `STUB_CASE` command block actual output, in its literal run-line
order (`twoline`, `oneline2`, `wrapper`, `wrongpath`, `eacces`, `statx`,
`enoent`, `eio`, `empty`, `nonprint`, `ok`):

```
B3_STOP reason=boundary_diagnostic_multiline path=/etc/mtc-bridge/mtc-bridge.env rc=1 detail=stat: cannot stat '/etc/mtc-bridge/mtc-bridge.env': Permission denied stat: cannot stat '/etc/mtc-bridge/mtc-bridge.env': No such file or directory
RC=3
B3_STOP reason=boundary_diagnostic_ambiguous path=/etc/mtc-bridge/mtc-bridge.env rc=1 classes=2 eacces=1 enoent=1 detail=stat: cannot stat '/etc/mtc-bridge/mtc-bridge.env': Permission denied (No such file or directory)
RC=3
B3_STOP reason=boundary_probe_unclassified path=/etc/mtc-bridge/mtc-bridge.env rc=1 detail=mtcwrap: stat failed on /etc/mtc-bridge/mtc-bridge.env: Permission denied
RC=3
B3_STOP reason=boundary_probe_unclassified path=/etc/mtc-bridge/mtc-bridge.env rc=1 detail=stat: cannot stat '/some/other/path': Permission denied
RC=3
B3_conf_dir_opaque_to_operator path=/etc/mtc-bridge/mtc-bridge.env outcome=EACCES rc=1 mechanism=message_lc_all_c_exact_shape
RC=0
B3_conf_dir_opaque_to_operator path=/etc/mtc-bridge/mtc-bridge.env outcome=EACCES rc=1 mechanism=message_lc_all_c_exact_shape
RC=0
B3_FAIL reason=conf_dir_search_permitted_name_absent path=/etc/mtc-bridge/mtc-bridge.env rc=1 expected=EACCES
RC=1
B3_STOP reason=boundary_probe_unclassified path=/etc/mtc-bridge/mtc-bridge.env rc=1 detail=stat: cannot stat '/etc/mtc-bridge/mtc-bridge.env': Input/output error
RC=3
B3_STOP reason=boundary_probe_unclassified path=/etc/mtc-bridge/mtc-bridge.env rc=4 detail=
RC=3
B3_STOP reason=boundary_probe_unclassified path=/etc/mtc-bridge/mtc-bridge.env rc=1 detail=[non_printable_detail_suppressed]
RC=3
B3_FAIL reason=conf_dir_entry_permitted path=/etc/mtc-bridge/mtc-bridge.env stat=[regular file|600|0:0] expected=EACCES
RC=1
BLOCK_RC=0
```

The result rc vector is `3,3,3,3,0,0,1,3,3,3,1`, exactly matching the section
5.6 table. No tested fence required an edit.

# 3. Placeholder sweep

PASS. A whole-file scan found no angle-bracket placeholder in any command block
that a reader is instructed to run, and no TODO, TBD, FIXME, XXX, fill-in, or
insert-here marker.

The repaired round-5 strings `<repo>`,
`<the scratch directory rendered as $QA above>`, and `<the run line>` remain only
where prose names the old defects. They are not runnable text. The subject's
literal output-shape tokens `<decimal_inode>`, `<decimal_dev>`, `<inode>`, and
`<uid>:<gid>` occur only in recorded output. `<LF>` and `<BEL>` label inputs in a
carried-forward table with no command line. `<read-only file>` is explanatory
prose about an input descriptor, outside every runnable block. The declared
`$QA`, `$QAW`, and `$QA_PY` normalizations occur in recorded output as intended.
None asks the reader to supply or edit a value.

# 4. Nit 2 and arithmetic

PASS. The section-3 item-5 paragraph and section-8 gap-10 paragraph are
text-identical to round 5. The limitation remains narrowly stated as a no-field
mid-table read failure after at least one complete record. The separate partially
populated case is still stated to reach `truncated=1` and STOP with
`mount_table_unterminated_final_record`.

The arithmetic independently reconciles:

```
RP1 A = 5 + 5 + 7 + 3 + 1 = 21
RP1 B = 10 + 18 + 15 + 11 + 10 = 64
RPD A = 11 + 11 = 22
RPD B = 5 + 10 + 4 + 10 + 15 + 11 = 55
Total A = 21 + 22 = 43
Total B = 64 + 55 = 119
Total C = 3
Driven = 43 + 119 = 162
Driven/carried = 71 + 91 = 162
```

Final verdict: PASS.
