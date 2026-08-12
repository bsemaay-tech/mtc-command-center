# VERDICT: REQUEST_CHANGES

TIER: T1

APPLIED AUDITOR CONTRACT: Codex `gpt-5.6-sol`, `xhigh` per the explicit kickoff;
fresh independent read-only audit. No host or network action was performed.

Round 8 closes the round-7 child-completion finding: the wrapper rejects nonzero child
status and unadjudicated stderr before it interprets stdout, its exit reflects every rejection,
and the empty stderr contract is enforced for all eleven published blocks. The package remains
non-accepting because the same wrapper does not execute the published PowerShell bytes
verbatim, despite repeatedly claiming byte-for-byte extraction and execution.

## Required finding

`SELF_QA_SEC102_R8.md:1660`, `SELF_QA_SEC102_R8.md:1899-1900`: **MEDIUM — the
published wrapper rewrites every LF-only PowerShell block to CRLF before execution while
claiming that the extracted bytes are written and run byte-for-byte.** It reads the Markdown
through newline-translating text I/O and writes each temporary `.ps1` through
`NamedTemporaryFile(..., "w", encoding="utf-8")` without disabling newline translation.
On this Windows host, a published block containing 110 LF and zero CRLF sequences was written
with 110 CRLF sequences; the written bytes did not equal the extracted bytes.

This is Design Defect Pattern 10 overlaid by Pattern 11: the declared instrument is the
published LF byte sequence, but the executed instrument is a different CRLF byte sequence.
The current eleven blocks happen to produce the same accepted results under both encodings — I
ran all eleven again from exact extracted bytes — but the reusable verifier can still certify a
modified, line-ending-sensitive block rather than the block on the page. That makes the
document's literal/verbatim evidence claim false and leaves a future false-acceptance path.

Minimum required repair:

1. Preserve the document's fence bytes through extraction and temporary-file creation (binary
   extraction/write is the clearest route), and assert immediately before launch that the
   temporary script bytes equal the extracted fence bytes.
2. Keep the existing process-status and stderr gates ahead of stdout interpretation.
3. Under D026, demonstrate RED against the exact round-8 wrapper and GREEN after the repair with
   a harmless line-ending-sensitive sentinel or an equivalent direct byte-identity
   falsification. Record the real commands, status, and output summary; do not add an attack
   fixture or reproduce a sensitive body.
4. Re-run all eleven published blocks plus the outer wrapper from the exact published bytes.

## Round-7 finding disposition

**CLOSED.** The round-8 wrapper waits for the child, reads its real process status and stderr,
and reaches `continue` on either a nonzero status or unadjudicated stderr before the stdout
comparison is constructed. Its final exit is nonzero if any status, stderr, transcript, or
missing-transcript rejection occurs.

The verbatim harness discriminator conserved both directions. By fixture class:
`fails_after_summary` and `stderr_after_summary` are accepted by the published round-7 wrapper
and rejected by round 8 with stdout left uninterpreted; `well_behaved_child` remains accepted;
`published_line_absent` remains rejected. The word-bounded reason detector does not read
`MISMATCHED=0` as the standalone `MISMATCH` reason token.

The current empty `STDERR_CONTRACT` is sound and enforced: every one of the eleven real children
returned process status 0 with empty stderr, so no exception entry was exercised. No remaining
path was found by which a nonzero-status or stderr-writing child can have its stdout scored as
reproduced. This closes Patterns 6/7 for the round-7 finding; the required finding above is the
separate identity/reproducibility defect in Patterns 10/11.

## Reproduced evidence

Fixture stdout and stderr were redirected to files outside the repository. Only the permitted
summary and counter lines are reproduced here.

```text
CASES=58 FAILED_COUNT=0
CASES=6 RC_LEVEL_NEW_REDS=4 OFF_EXPECTATION=0
SUMMARY HARNESS_D026 CASES=4 RED_TO_GREEN=2 OFF_EXPECTATION=0
SUMMARY OUTER_CHILDREN CASES=11 child_rc_nonzero=0 STDERR_NONEMPTY=0
SUMMARY OUTER BLOCKS=11 STATUS_PROVED_COMPLETE=11 REJECTED_ON_STATUS=0 REJECTED_ON_STDERR=0 COMPARED=11 MISMATCHED=0 REJECTED=0
SUMMARY OUTER_PROCESS child_rc=0 STDERR_BYTES=0
SUMMARY TEXTMODE_WRITE byte_identical=0 source_lf=110 source_crlf=0 written_lf=110 written_crlf=110
SUMMARY EXACT_BYTES BLOCKS=11 child_rc_nonzero=0 STDERR_NONEMPTY=0 MISMATCHED=0 REJECTED=0
```

The 58-case matrix was executed verbatim and showed no module regression. The separate
six-case pre-feature D026 block retained four rc-level REDs and both controls. The section-13
harness D026 and the published outer wrapper also completed with status 0 and empty stderr.

## Byte and scope verification

- Frozen audit commit: `3f2c22cafdd6e564e56ced082e623615a3d0b0b3`.
- `composite_pathproof.py` has the same Git object at the R7 parent, R8 commit, and worktree:
  `0e00db0ef3324765118f4e313f8e1964d451bd70`.
- Its worktree bytes are `129658` B with SHA-256
  `adbf27fd908439e1d48e6c95a4eecba956c0607c42ae5a3bfa9cb210b636c05a`, matching the
  published round-7/R8 identity.
- The R8 commit changes only `SELF_QA_SEC102_R8.md`, `SEC102_R8_REPORT_2026-08-11.md`, and
  `STATUS_SEC102.md`; all three worktree files are byte-identical to the frozen commit.
- No Pine, parity, MTC, trading, deployment, host, network, fixture, or production-code surface
  changed in round 8 or in this audit.

## Thirteen-pattern adjudication

| Pattern | Result |
|---|---|
| 1 — STOP/PASS/FAIL ordering | PASS on the 58-case matrix and wrapper rejection order |
| 2 — Host and namespace identity | PASS within the explicit no-host scope |
| 3 — Host-object, symlink, mount identity | PASS as an unchanged explicit non-claim |
| 4 — External interpreter/environment boundary | PASS as the disclosed production-gate blocker |
| 5 — Grammar completeness | PASS on the unchanged round-7 command-word fixpoint |
| 6 — Probe status before adjudication | PASS; the R7 finding is closed |
| 7 — Incomplete-reader path | PASS; incomplete child execution cannot reach comparison |
| 8 — Deployed identity | PASS within the unchanged lexical scope |
| 9 — Claim wording vs predicate | PASS for status/stderr ordering and disclosed residuals |
| 10 — Falsifiable/reproducible evidence | **REQUEST_CHANGES: executed script bytes differ from the published bytes** |
| 11 — Declared vs executed instrument | **REQUEST_CHANGES: text-mode newline translation changes the instrument** |
| 12 — Unmodeled behavior disappearing | PASS for the unchanged module; wrapper rejects status/stderr uncertainty |
| 13 — Terminal-disposition conservation | PASS for all eleven current child dispositions |

## Residual judgments and hygiene

- The interpreter-vocabulary limitation remains the sole disclosed module production-gate
  decision. This audit neither closes nor worsens it.
- No new attack fixture was authored, and no sensitive fixture body is reproduced here.
- No git mutation was performed. This verdict is the only repository file authored by the
  audit.
- Tracked status was clean at entry and immediately before this verdict. Literal full
  `git status --porcelain` was not clean at entry: the shared worktree already contained 67
  unrelated untracked entries. Those were preserved untouched, so a repository-wide clean
  status claim would be false; the only audit-created repository delta is this verdict file.

Because the verdict is non-accepting, the SEC102 Codex flagship slot does not close in round 8.
The T1 GLM-5.2 second-opinion condition is also triggered by this finding and by the package size;
it was not dispatched here because the kickoff requires no network and assigns that dispatch to
the Lead.
