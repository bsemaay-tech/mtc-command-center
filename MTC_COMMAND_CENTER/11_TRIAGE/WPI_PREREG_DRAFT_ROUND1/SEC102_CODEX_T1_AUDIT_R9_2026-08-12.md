# VERDICT: REQUEST_CHANGES

**TIER:** T1  
**APPLIED AUDITOR CONTRACT:** Codex `gpt-5.6-sol`, xhigh per the explicit R9 kickoff; independent flagship audit; T1 round cap 2.  
**AUDIT SUBJECT:** commit `ba929abc`, SEC102 composite pathproof round 9.  
**GIT MUTATION:** none.

## Required finding

1. `SELF_QA_SEC102_R9.md:1749-1755,2084-2110` — **MEDIUM — Pattern 11, with Pattern 9 overlay:** the pre-launch comparison is not bound to the object PowerShell later opens. The wrapper creates a named temporary file, closes the creation handle, writes it, closes the read-back observation after `script.read_bytes()`, and then launches `powershell.exe -File <pathname>`. PowerShell resolves and opens that pathname only after the equality decision. A concurrent process with the same principal's access can replace or modify the file in that interval; the child can therefore execute bytes that were never compared with the fence while `same`, `SCRIPT_BYTES_IDENTICAL=1`, and the published SHA-256 still describe the earlier bytes. If that child returns status 0, empty stderr, and the published subset, the wrapper accepts it. This contradicts the unconditional claims that there is “no path through the wrapper on which unproven bytes are executed” and that the comparison proves what “the interpreter is handed.” Status item 43 admits that M1 cannot show that no other defeating write path exists, but it neither identifies this temporal rebinding nor narrows those claims.

   **Minimum required repair:** bind the byte sequence checked by the parent to the byte sequence consumed for execution, with no replace/modify window between verification and interpreter consumption, and add D026 RED/GREEN evidence for that binding. A pre-launch read followed by a pathname reopen is insufficient. If the implementation deliberately retains name-based reopening, the executed-byte-identity claim is not closed and must not be presented as such.

## Independent verification

### Scope and identity

- Commit `ba929abc` changes exactly three permitted R9 files: `SELF_QA_SEC102_R9.md`, `SEC102_R9_REPORT_2026-08-12.md`, and `STATUS_SEC102.md`. It changes no protected, Pine, parity, MTC, trading, host, network, or production surface. `git diff --check ba929abc^ ba929abc` returned 0.
- The current three R9 files are identical to their `ba929abc` versions.
- `composite_pathproof.py` is byte-identical to the R8 input commit `3f2c22ca`: Git blob `0e00db0ef3324765118f4e313f8e1964d451bd70` on both sides, 129658 bytes, SHA-256 `adbf27fd908439e1d48e6c95a4eecba956c0607c42ae5a3bfa9cb210b636c05a`. R9 is harness-only.

### Verbatim execution evidence

All detailed fixture output was redirected to temporary files outside the repository. No new attack fixture was authored. Fixtures are referenced only by class.

1. The exact section-3 PowerShell fence was extracted as bytes and run from outside the repository. Process status was 0 and stderr was empty:

   ```text
   CASES=58 FAILED_COUNT=0
   ```

2. Section 13b was run verbatim. The line-ending-sensitive sentinel flipped in both required directions; the four R8 status/stderr/subset controls conserved; M1 restored the R8 text write path and exercised the pre-launch byte gate:

   ```text
   D026_CASES=6 FALSE_ACCEPT_UNDER_R8=1 FALSE_REJECT_UNDER_R8=1 CONSERVED_R8_GATES=4 M1_GATE_FIRED=1 D026_OFF_EXPECTATION=0
   ```

   The real-artifact write-path measurement also reproduced the R8 110-LF/110-CRLF non-identity and the R9 110-LF/zero-CRLF identity. These new tests satisfy D026 for the deterministic newline-translation defect: both RED directions and the load-bearing M1 mutation were independently observed.

3. The sole section-13c Python fence was extracted as bytes, written outside the repository, and run there over the final document. The wrapper returned 0 with zero stderr. All eleven blocks passed byte, process-status, stderr, and published-subset gates:

   ```text
   BLOCKS=11 SCRIPT_BYTES_IDENTICAL_ALL=11 REJECTED_ON_BYTES=0 STATUS_PROVED_COMPLETE=11 REJECTED_ON_STATUS=0 REJECTED_ON_STDERR=0 COMPARED=11 MISMATCHED=0 REJECTED=0 CWD=<outside-repository-temp>
   OUTER_WRAPPER_RC=0
   ```

   All 24 logical transcript lines matched section 13d in order after normalizing only the environment-specific outside-directory value and the leading capture BOM in the published text fence. Every per-block byte count, LF/CRLF/non-ASCII count, SHA-256, status, stderr count, and comparison result matched. Static inspection also confirmed the byte gate precedes the sole `subprocess.run` call and that the R8 status/stderr gate text is byte-identical in R9.

## Residual and 13-pattern adjudication

- **Disclosed residual 41 is honest.** The gate compares against the document as materialized on disk, not a pinned checkout. A CRLF-materialized fresh clone changes the published LF/CRLF/SHA cross-check and makes block 11 fail loudly rather than silently. No `.gitattributes` change is required inside this R9 scope.
- **Patterns 1-8:** no new regression. The 58-case rc/reason matrix passed; no host, namespace, deployed-object, interpreter-decoding, or production claim was added. The carried interpreter-vocabulary production-gate decision remains owner-ratified and is not reopened here.
- **Pattern 9:** required finding above. The “interpreter is handed” and “no path” sentences outrun a pre-launch pathname observation.
- **Pattern 10:** the deterministic R8 text-I/O false acceptance is closed by byte-mode extraction/write/read-back and independently reproduced D026 evidence. That does not cure the separate pathname-reopen gap.
- **Pattern 11:** required finding above. The verified named file is not atomically the instrument later opened by the production caller.
- **Pattern 12:** M1 proves the new mismatch branch is exercised and terminal; no silent internal wrapper-owned translation path was found.
- **Pattern 13:** all eleven declared blocks reached exactly one terminal disposition in the clean run, and all counters conserved.

## Acceptance consequence

Round 9 closes the deterministic LF-to-CRLF rewrite found in R8, but it does not yet prove the stronger executed-instrument identity claimed by the document. This verdict does **not** close the SEC102 Codex flagship slot. The owner-ratified interpreter-vocabulary production-gate decision and the Lead's later GLM-5.2 T1 second opinion remain outside this non-accepting verdict.

## Repository-delta proof

The pre-audit dirty worktree was preserved. The final status comparison against that baseline contains exactly one additional repository path: this verdict file. No tracked file was modified by the audit, and no Git command mutated repository state.
