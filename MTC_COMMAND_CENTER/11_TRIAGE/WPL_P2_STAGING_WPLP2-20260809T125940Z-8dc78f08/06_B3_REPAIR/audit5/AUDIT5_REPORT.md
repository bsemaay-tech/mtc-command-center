BLOCK

# Required finding

## 1. D026 exact-command recording is still not closed

`round5/SELF_QA.md` does not provide a literally executable prerequisite for
the section 5 closure commands:

- Line 352 records `B="<repo>/..."`. The kickoff permits normalization of the
  scratch root only, not a repository-root placeholder. Line 365 itself calls
  this a fourth path normalization.
- Line 354 records `QA=<the scratch directory rendered as $QA above>`. This is
  not valid Bash. Running the section 4 declaration block exactly as written
  stops before any closure command can run:

```
bash: line 3: syntax error near unexpected token `newline'
bash: line 3: `QA=<the scratch directory rendered as $QA above>'
RC=2
```

Every section 5 command depends on `R2`, `R3`, `R4`, `QA`, and related values
from that block. Therefore the commands require edits or external replacement
before they run, contrary to lines 348 and 507-520 and to the kickoff rule that
a command needing an edit is not closed.

There is a second residual parameterized command in the same prerequisite
record. Line 381 uses `out="$(<the run line> 2>&1)" ...` instead of recording
the concrete capture command actually used for each direct run. Those direct
commands do not themselves print the documented `RC=` line. This is still a
recipe standing in for literal executed command text.

The named round-4 placeholders `<FIX>`, `<CASE>`, `<PRE>`, `<SRC>`, `<FILE>`,
`<FN>`, and `<FX>` do not remain in section 5 command blocks, and all item-6
`STUB_CASE` values are literal. That partial repair does not cure the executable
prerequisite and capture placeholders above. Per the kickoff, the residual
placeholder/non-runnable command is REQUIRED.

# Code freeze

PASS. The three round-5 non-QA files are byte-identical to round 4:

```
RP1-B3.sh      6f3ea022b68d80a552c4ebcb771bbb2a707bdab46a383d605ffc5b88b884becc
RPD-VERIFY.sh  3b9e78e87cecdc10ab1a10d14e79dbff530968e4075277117743c88976fa813c
DESIGN_NOTES.md 103ffe3811dfd7764bf1b4d9bc47489fbe3cb2d72bca7c5c32e461a82440f23b
```

`round5/` contains exactly the required four files and no hidden entry. No code
delta exists, so no audit-4 code path was re-litigated.

# Exact-command samples

Five unchanged section 5 command bodies were run under the recorded MSYS/Git
Bash environment after resolving the defective shared `B` and `QA` declarations
externally. All five then reproduced the stated normalized output and status:

1. Item 1 cwd RED: `RPD_manifest_binding ... bound=both ...`, rc 0.
2. Item 4 `nan.json` RED: `RPD_manifest_binding ... bound=both ...`, rc 0.
3. Item 4 `nan.json` GREEN: `install_manifest_non_json_constant`, rc 3.
4. Item 6 GREEN with literal `STUB_CASE=twoline`:
   `boundary_diagnostic_multiline`, rc 3.
5. Item 5 RPD `adir` GREEN: `mount_table_read_error`, records 0, rc 3.

The item-1 cwd RED block rebuilds the round-2 `arm.sh` before copying it, so the
specific overwritten-arm state defect from audit 4 is repaired. The successful
samples show that the section 5 bodies work after external setup repair; they do
not make the recorded shared setup literal or executable.

# Nit 2 and arithmetic

PASS. The limitation is narrowed to a mid-table read failure that populates no
field after at least one complete record. The document separately states that a
partially populated record reaches the `truncated=1` STOP arm.

The totals and subcounts reconcile exactly:

```
RP1 = 21 A / 64 B
RPD = 22 A / 55 B
Total = 43 A / 119 B / 3 C
```

Section 6.13 is labelled 11, and the driven/carried table reconciles to
162 / 71 / 91.

Final verdict: BLOCK.
