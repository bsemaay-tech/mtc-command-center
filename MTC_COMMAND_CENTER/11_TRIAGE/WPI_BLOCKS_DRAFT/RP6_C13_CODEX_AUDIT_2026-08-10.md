BLOCK: 3 findings

# Findings

## 1. HIGH — rc 2 plus diagnostic bytes is falsely classified as a valid no-match

`RP6-P0.sh:656-660` merges stdout and stderr, but the rc-2 branch returns
`P0_PW_OUTCOME=nomatch` without requiring the capture to be empty. The
`mtc-bridge` caller at `RP6-P0.sh:733-734` consequently turns any such outcome
into `state_account_resolution_unexpected ... observed_numeric=absent`, even
though non-empty error/diagnostic bytes mean positive absence was not
established. This violates round-1.5 section 8.1 rows 2-3, the explicit
valid-no-match-versus-lookup-error requirement, Pattern 1, and the block's own
status-before-output rule at lines 24-29.

Executed equivalent status/output falsification against the real extracted
parser:

```text
CONTROL_TOOL_RC=2 raw=[/usr/bin/grep: definitely_missing_c13_fixture: No such file or directory]
PARSER_OUTCOME=nomatch diag=[/usr/bin/grep: definitely_missing_c13_fixture: No such file or directory]
EXPECTED_ERROR_ASSERTION_RC=1
```

Required repair: rc 2 may become `nomatch` only when the complete merged capture
has the exact valid no-match shape (empty for this interface). Any diagnostic,
partial record, or other byte at rc 2 must become `error`, and the caller must
emit `identity_unresolvable` rc 3. Record D026 RED/GREEN output for this case.

## 2. MEDIUM — the C13 QA is not D026 closure evidence

`SELF_QA_RP6.md:301-385` extracts the repaired functions and manually calls
`p0_resolve_accounts`; it never runs the test against `cbaf3ec8^` or an
equivalent implementation mutation. Its cases labelled RED are deviant-input
cases against repaired code, not D026 RED. In particular, deleting the
production integration call at `RP6-P0.sh:743` would leave this harness green,
because it extracts the function at `SELF_QA_RP6.md:343` and invokes it itself
at line 358. The backstop section mutates away each rc-3 pre-check, but records
no run with the new `:?` backstop itself removed; the retained as-drafted RED is
a missing-stdin harness failure, not a falsification of the implementation fix.

Required repair: add real RED output against the exact pre-C13 behavior or an
equivalent mutation that removes/bypasses both the production arm integration
and each claimed backstop, then run the same assertions GREEN on repaired bytes.
Until then these tests are supplemental under D026.

## 3. MEDIUM — the block header still claims that no name is queried

`RP6-P0.sh:31-35` says that no name is looked up or captured anywhere and that
the block asks the resolver database nothing. The new arm explicitly queries
`gatea` and `mtc-bridge`, captures the returned name field, and prints it as a
diagnostic (`RP6-P0.sh:656`, `700-704`, `722-726`). The terminal claim was
updated, but this earlier design claim is now false (Pattern 9).

Required repair: narrow the header to the truth already expressed by the arm
and terminal claim: names are queried and recorded diagnostically, admission is
numeric only, and NSS source identity is not established.

# Verification matrix

| Item | Result | One-line evidence |
|---|---|---|
| V1 — diff isolation | PASS | `git diff cbaf3ec8^ -- RP6-P0.sh` is 164 insertions/4 deletions and is confined to the two new inputs, the 12th-tool inventory entry, the account-resolution section/call, and claim replacements; every pre-existing executable arm is byte-untouched. |
| V2 — spec conformance | FAIL | Numeric equality and `999:988`/group plumbing are present, but finding 1 fails the binding distinction between a valid no-match and a lookup/error result. |
| V3 — truthfulness/parser | FAIL | The rc-0 path rejects multiline, wrong-field-count, and nonnumeric uid/gid records, but finding 1 proves a false positive-absence class and finding 3 is a false design claim. |
| V4 — execution environment/read-only | PASS | `getent` is the 12th inventory tool, is resolved/stored as absolute `P0_GETENT`, participates in the preregistered pin check, and the new production arm performs only `id`, `getent`, builtin parsing, comparisons, and diagnostic output; it adds no write. |
| V5 — QA integrity | FAIL | The exact C13 arm fence reran in Git Bash with process rc 0 and the recorded rc vector `0,3,3,3,3`; the corrected backstop fence reran with process rc 0 and both named backstops, and its additional header line is covered by the recorded trimming disclosure. The as-drafted missing-input and ungated-summary reasoning is consistent with its retained RED transcript, but finding 2 prevents D026 acceptance. |
| V6 — hash/bytes | PASS | Git Bash re-derived current `cfdb23b8834a783638723c54cf632973c1cc20c5fb676cb6d310a9d43b9acf1c`, 54109 B; baseline `6c5b89456b4b4072969f7c928328d2d0ecb51e8476a15c5a7401f2988c9766f7`, 44979 B; `bash -n` rc 0. |

# Commands independently executed

```text
git diff --no-ext-diff --unified=8 "cbaf3ec8^" -- "MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6-P0.sh"
sed -n '308,385p' SELF_QA_RP6.md | bash --noprofile --norc
sed -n '439,513p' SELF_QA_RP6.md | bash --noprofile --norc
sha256sum RP6-P0.sh
wc -c < RP6-P0.sh
git show 'cbaf3ec8^:MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6-P0.sh' | sha256sum
git show 'cbaf3ec8^:MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6-P0.sh' | wc -c
bash -n RP6-P0.sh
```

No host was contacted. No production or preregistration file was modified.
