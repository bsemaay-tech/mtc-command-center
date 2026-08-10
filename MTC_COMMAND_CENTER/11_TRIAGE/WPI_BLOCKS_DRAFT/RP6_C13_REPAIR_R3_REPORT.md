# RP6-P0 C13 — bounded repair round 3, implementer report

**Implementer:** Claude Opus 5, acting as bounded-round IMPLEMENTER under
`KICKOFF_C13_REPAIR_R3.md`. GLM-5.2 (the C13 implementer) is quota-blocked. This
implementer neither authored nor audited the C13 arm; the C13 auditor is Codex,
who re-audits this repair.
**Date:** 2026-08-10. **Working directory:** `C:\LAB\Tradingview_LAB_CLEAN`.
**Repair contract:** `RP6_C13_CODEX_AUDIT_2026-08-10.md` (BLOCK, 3 findings).

**Status of the block: REPAIRED-PENDING-RE-AUDIT.** Not frozen, not accepted, not
dispatchable, not authorised for host execution. Nothing committed.

## Artefact

| Item | Value |
|---|---|
| Pre-R3 bytes (audited by Codex; commit `cbaf3ec8`) | SHA-256 `cfdb23b8834a783638723c54cf632973c1cc20c5fb676cb6d310a9d43b9acf1c`, 54109 B |
| R3-repaired bytes | SHA-256 `ef205e2064caa0cb1493abf037ce9d435f2bf8f6259c5bb3fc4964d1abb2b4b9`, 55467 B |
| `bash -n RP6-P0.sh` | rc 0, `BASH_N=PASS` |
| `git diff --numstat` (block) | 34 insertions, 12 deletions, one file |
| Executable lines changed | one `case` arm in `p0_resolve_passwd`; the other three hunks are comment/claim text |
| Files touched | `RP6-P0.sh`, `SELF_QA_RP6.md`, `STATUS_RP6_P0.md`, this report — exactly the four kickoff deliverables |

## Finding → disposition → evidence

### F1 (HIGH) — rc 2 plus diagnostic bytes falsely classified as a valid no-match

**Disposition: REPAIRED IN THE BLOCK.**

`p0_resolve_passwd`'s rc-2 arm now requires the complete merged capture to be
empty — this interface's exact valid no-match shape — before it may return
`nomatch`. Any diagnostic, partial record or other byte at rc 2 sets
`P0_PW_OUTCOME=error`, and the existing `error` arms of both callers emit
`identity_unresolvable … rc 3`. No caller change was needed or made. The
surviving no-match path records `P0_PW_DIAG=empty_capture_at_rc2` — the reason the
no-match was admitted — instead of a sanitized empty string.

```diff
-        2) P0_PW_OUTCOME="nomatch"; p0_sanitize "$raw"; P0_PW_DIAG="$P0_SAFE"; return 0 ;;
+        2)
+            if [ -n "$raw" ]; then
+                p0_sanitize "$raw"; P0_PW_DIAG="$P0_SAFE"
+                P0_PW_OUTCOME="error"; return 0
+            fi
+            P0_PW_OUTCOME="nomatch"; P0_PW_DIAG="empty_capture_at_rc2"; return 0 ;;
```

The rc-0 arm, the `*)` error arm, the multiline/colon-count/nonnumeric checks and
both caller `case` statements are byte-identical to the audited bytes. The
parser-function docblock and the section preamble were narrowed to match
(rc 2 is a valid no-match only with an empty capture; rc 2 with bytes is an
inability to evaluate).

**Evidence** — `SELF_QA_RP6.md` § "C13 R3 — D026 harness 1", block C, real
captured output. Three rc-2-plus-bytes fixtures (NSS timeout on stderr, partial
record `mtc-bridge:x:999`, and an `SERVBUSY` diagnostic for `gatea`):

- repaired bytes → `P0_STOP reason=identity_unresolvable account=mtc-bridge detail=[getent: sss_nss: connection to the name service timed out]`, rc 3 — assertion MET (GREEN);
- pre-repair bytes, same fixtures, same assertions → `ASSERT_UNMET` on all three (RED);
- the defect recorded positively: pre-repair bytes emit `P0_STOP reason=state_account_resolution_unexpected account=mtc-bridge observed_numeric=absent expected_numeric=999:988 detail=getent_valid_no_match`;
- `gatea` under pre-repair bytes emits the right verdict for the wrong reason
  (`identity_unresolvable account=gatea rc=2 detail=getent_valid_no_match_for_route_login`), which the assertion on `detail=[…]` distinguishes.

**Regression** — block D: the genuine valid no-match (rc 2, empty capture) still
produces the exact preregistered line
`state_account_resolution_unexpected … observed_numeric=absent … detail=getent_valid_no_match`
at rc 3. The narrowing did not collapse the row-3 arm.

### F2 (MEDIUM) — the C13 QA is not D026 closure evidence

**Disposition: REPAIRED IN THE QA.** The two earlier C13 fences are re-labelled
SUPPLEMENTAL in place (with a pointer to the round-3 sections and a statement of
exactly why each is supplemental), and two new harnesses were written and
executed locally in Git Bash.

**(a) Production arm integration call.** Harness 1 no longer calls
`p0_resolve_accounts`. It extracts the helper and arm definitions as before, then
appends the block's own top-level driver lines — selected from the source bytes by
exact whole-line match — so the block, not the harness, decides whether the arm
runs. Mutation `nocall` deletes the production integration call. Captured output:
`DRIVER_LINES repaired=1 prerepair=1 nocall=0`, and all three arm assertions go
`ASSERT_UNMET` with the arm producing nothing but its section header at rc 0. The
mutation the auditor named now kills the harness.

**(b) The `:?` backstops themselves.** Harness 2 runs one assertion (rc 1 plus the
named input message) against two mutations per new input:
`precheck_only` (rc-3 pre-check deleted, backstop kept) → `ASSERT_MET`, the
backstop fires at the block's own line; `precheck_and_backstop` (both deleted) →
`ASSERT_UNMET`, the block runs on through two further sections and dies at the
first *use* of the variable with `P0_STATE_UID: unbound variable` — an unnamed
`set -u` error carrying no `P0_STOP reason=` and no adjudicated rc 3.
Stated exactly: the mutant is killed on the message, not on rc (rc is 1 in both
cases). `MUTATION_LINES_REMOVED … n=1` / `n=2` proves each mutation removed the
lines it claims to.

**(c) The F1 fix.** Covered under F1 above — same assertions, GREEN on repaired
bytes and RED on the pre-repair bytes obtained from `git show cbaf3ec8:<path>`.

**Harness integrity.** Both harnesses check assertion POLARITY: a case declared
`RED` fails the run if its assertion is met, so a surviving mutant is a harness
failure rather than a silent pass, and the summary line is gated by an explicit
if/else with `exit 1` on failure (Pattern 10). Results: harness 1 process rc 0,
`C13_R3_ARM_QA_SUMMARY cases=16 result=PASS`; harness 2 process rc 0,
`C13_R3_BACKSTOP_QA_SUMMARY inputs=2 mutations=2 cases=4 result=PASS`.

**Transcription check.** Both fenced commands were extracted back out of
`SELF_QA_RP6.md` after writing, re-run from the document itself, and diffed
byte-for-byte against the executed scripts and against the pasted output — command
fences identical, output fences identical. One line of the first pasted output was
a copy slip in the initial write-up (a duplicated `ASSERT_MET` substring) and was
replaced mechanically from the captured run, then re-diffed clean. Recorded here
because the audit is entitled to know the paste was machine-verified rather than
eyeballed.

### F3 (MEDIUM) — the block header still claims that no name is queried

**Disposition: REPAIRED IN THE BLOCK.** The "NUMERIC IDENTITY ONLY (pattern 8)"
header no longer says that no name is looked up or captured anywhere and that the
block asks the resolver database nothing. It now says: ADMISSION is numeric only;
no name is ever compared or asserted; two names ARE queried by the
account-resolution section via the pinned `getent passwd`; the returned name,
gecos, home and shell fields are RECORDED AS DIAGNOSTICS ONLY and no verdict
depends on them; and which NSS source answered is not established here, as
already disclosed in the terminal claim's `does_not_establish` list. This matches
the arm at `RP6-P0.sh:656`/`700-704`/`722-726` (pre-repair line numbers) and the
terminal claim, closing the Pattern 9 contradiction.

## Preserved, and how it was checked

- **Read-only scope.** The only executable change is one `case` arm in a parser
  that runs comparisons and string builtins. No file, directory, temp file, mode,
  owner, ACL, group, service or network state is created or changed; no new tool
  is invoked; the 12-tool inventory is untouched.
- **rc 0/1/3 contract.** Unchanged. The F1 repair moves outcomes between two
  existing rc-3 reasons; it introduces no new exit path and no FAIL.
- **All pre-existing arms.** `git diff -U2` is four hunks: three comment/claim
  hunks and the one rc-2 arm. Every other executable line in the block is
  byte-identical to the audited bytes.
- **`bash -n`** rc 0 on the repaired bytes, re-run after the final edit.

## Limits, stated plainly

- The complete P0 block still was not run. It needs the accepted RP0
  library/bootstrap, Linux `/proc` namespace objects, the preregistered per-SHA
  venv, `getent`/`systemctl` on PATH and a reachable system manager — none of
  which exist in this Git Bash environment. Harness 1 sources the extracted arm
  plus the block's own driver lines; harness 2 sources the whole block but dies
  inside input validation before any external P0 probe.
- The `getent` used in QA is a local fixture. Production pins an absolute `getent`
  from the inventory. The fixture exercises the arm's adjudication, not any host
  NSS, and asserts no name.
- Both harnesses write QA-only files under `/tmp` (the fixture and the extracted
  source variants) — outside the repository, and not files the block creates.
- No host was contacted, no network command was run, and no host file content was
  printed. Nothing was committed.

## Note for the Lead (outside this round's scope)

While this round ran, `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh`
appeared as modified in the working tree (271 changed lines, mtime moving during
this session). This implementer did not touch that file and made no change to it;
another session appears to be editing it concurrently. Flagged so the Lead does
not attribute it to this repair when staging.
