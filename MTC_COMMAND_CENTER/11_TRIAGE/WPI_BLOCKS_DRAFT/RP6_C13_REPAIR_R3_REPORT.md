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


# Round 4 — disposition of `RP6_C13_REAUDIT_CODEX_2026-08-10.md`

Implementer: Claude Opus 5, bounded FINAL round under the T0 cap
(`KICKOFF_C13_REPAIR_R4.md`). Same session type as round 3: local Git Bash only, no
host contacted, no network command run, nothing committed.

## Findings and what was done

| Re-audit finding | Severity | Disposition |
|---|---|---|
| 1 — newline-only rc-2 capture falsely admitted as a valid no-match (`RP6-P0.sh:673`) | HIGH | **REPAIRED IN THE BLOCK** + RED/GREEN fixture added to harness 1 |
| 2 — R3 package exceeds the four-file whitelist (extra provenance log) | MEDIUM | **NO REPAIR** — Lead adjudicated it as an accepted Lead-side deviation added at commit time; file untouched |

## Finding 1 — the repair

The defect was in the capture, not in the test. `raw="$(… 2>&1)"` deletes trailing
newlines, so `[ -n "$raw" ]` at rc 2 could not distinguish an empty capture from one
whose only bytes were newlines, and the newline-only case fell through to
`P0_PW_OUTCOME="nomatch"` — contrary to the closure contract that ANY byte at rc 2
means positive absence was not established.

Repaired shape:

```bash
raw="$(LC_ALL=C "$P0_GETENT" passwd "$acct" 2>&1 || getent_rc=$?; printf x; exit "${getent_rc:-0}")" || rc=$?
case "$raw" in
    *x) raw="${raw%x}" ;;
    *)  P0_PW_DIAG="capture_sentinel_lost"; P0_PW_OUTCOME="error"; return 0 ;;
esac
[ -z "$raw" ] || had_bytes=yes
while [ "${raw%$'\n'}" != "$raw" ]; do raw="${raw%$'\n'}"; done
```

Four decisions behind that shape, each of which an auditor should be able to attack
directly:

1. **Sentinel inside the substitution.** `printf x` runs in the same subshell, so the
   capture's last byte is always `x` and every byte getent emitted — trailing
   newlines included — survives the substitution. Stripping the sentinel afterwards
   restores the real stream.
2. **rc semantics.** The kickoff warned about this. A bare `…; printf x` would make
   the substitution exit with `printf`'s status, so `|| rc=$?` would never fire and
   every rc-2 no-match would be misread as rc 0. getent's own rc is captured into
   `getent_rc` and the subshell re-exits with it.
3. **`set -e` safety.** getent is placed on the LEFT of `||`, where errexit is
   guaranteed ignored, so an inherited `set -e` cannot kill the subshell at the
   failing getent before the sentinel is written. This matters because that failure
   mode would be silent and fail-OPEN — the capture would lose its trailing newlines
   again and the defect would return. Verified empirically in this session under
   `set -Eeuo pipefail` with an external rc-2 fixture; both the guarded and unguarded
   forms produced the full 2-byte capture in Git Bash 5.2, and the guarded form is
   the one kept because it does not depend on that behaviour.
4. **Fail closed if the sentinel is lost.** If `raw` does not end in `x`, the capture
   was truncated by something other than getent, its trailing bytes are unknown, and
   no emptiness claim can be drawn from it. That is `error` /
   `capture_sentinel_lost`, never a no-match (Pattern 1).

Then `had_bytes` is decided on the preserved capture, and `raw` is normalized back to
exactly what plain command substitution used to produce, so the rc-0 full-record
parse and every diagnostic string are byte-identical to the R3-audited behaviour.
A newline-only rc-2 capture normalizes to empty, so it gets its own honest diagnostic
`newline_only_capture_at_rc2` rather than an empty `detail=[]`.

## Same-pattern sweep (the kickoff's "list them")

`p0_resolve_passwd` is the only site in the block that adjudicates rc 2 as a distinct
outcome — the file contains exactly one `2)` case arm. The other thirteen capture
sites treat any non-zero rc as an error, and the other emptiness tests fail CLOSED:
`p0_capture_numeric` does `[ -n "$raw" ] || p0_stop identity_probe_empty`, so a
newline-only capture there STOPs at rc 3 instead of being admitted. Newline stripping
in those places cannot manufacture a false positive result, so no other site was
changed. This is stated as a scope claim an auditor can falsify by grepping for
rc-2-specific arms and for emptiness tests that lead to an ADMISSION rather than a
STOP.

## QA (D026, real local runs)

`SELF_QA_RP6.md` harness 1 was EXTENDED, not replaced — all sixteen R3 cases are
still there verbatim and still run, against the R4 bytes:

- New source variant `prer4` = the committed R3 bytes `ef205e20…` (55467 B) that the
  re-audit falsified, alongside the existing `repaired` / `prerepair` / `nocall`.
- New shim modes `mtc_rc2_newline` (one newline on stderr, the auditor's exact
  fixture), `mtc_rc2_newlines3` (three newlines on stdout), `gatea_rc2_newline`.
- The `nocall` mutation is applied to the new case too, so the new assertion is
  killed by deleting the block's own integration call — it is evidence about the
  block, not about the harness.
- A `probe` prints the re-audit's own markers from real runs.

Result: `C13_R4_ARM_QA_SUMMARY cases=27 result=PASS`, process rc 0, 25 `CASE_OK` +
2 `PROBE_OK`, zero `CASE_BAD`.

RED/GREEN on the exact finding:

```text
--- probe variant=prer4 mode=mtc_rc2_newline
FIXTURE=mtc-bridge_rc2_stderr_single_newline_byte
P0_STOP reason=state_account_resolution_unexpected account=mtc-bridge observed_numeric=absent expected_numeric=999:988 detail=getent_valid_no_match
ARM_RC=3
FALSE_NOMATCH_REPRODUCED=yes
REQUIRED_ERROR_OUTCOME_PRESENT=no

--- probe variant=repaired mode=mtc_rc2_newline
FIXTURE=mtc-bridge_rc2_stderr_single_newline_byte
P0_STOP reason=identity_unresolvable account=mtc-bridge detail=[newline_only_capture_at_rc2]
ARM_RC=3
FALSE_NOMATCH_REPRODUCED=no
REQUIRED_ERROR_OUTCOME_PRESENT=yes
```

Harness 2 was re-run unchanged against the R4 bytes: process rc 0,
`C13_R3_BACKSTOP_QA_SUMMARY inputs=2 mutations=2 cases=4 result=PASS`.

## Measurements

- `RP6-P0.sh` after R4: SHA-256
  `bff3c86e6e9b565c55da34580284f22c80253d9e931d879fd749459bac85b7cf`, 57441 bytes.
- Pre-R4 baseline (`8d2f25a5`): `ef205e20…`, 55467 bytes — re-derived in-session and
  matched the re-audit before editing.
- `git diff --stat` for the block: 36 insertions, 5 deletions, one file.
- `bash -n RP6-P0.sh` → rc 0.
- Files touched by this round, exactly four: `RP6-P0.sh`, `SELF_QA_RP6.md`,
  `STATUS_RP6_P0.md`, this report. Nothing committed. The provenance log
  `C13_R4_CLAUDEPRO_RUN_2026-08-10.log` was created by the Lead before this round
  started and was not written to by this implementer.

## Limits, stated plainly

- The complete P0 block still was not run; the environment blockers recorded for R3
  are unchanged.
- The newline fixture is a QA shim. It proves how the block adjudicates an rc-2
  capture whose bytes are newlines; it does not establish that any real NSS module
  emits such output. The contract being enforced is "any byte at rc 2 is not a proven
  absence", which does not depend on that.
- `set -e` behaviour inside command substitution was verified in this Git Bash only.
  The repair does not rely on it (point 3 above), and the `capture_sentinel_lost` arm
  makes the failure mode fail-closed rather than silent — but no test on the target
  host's shell was run, because no host was contacted.
- QA files are written under `/tmp`, outside the repository.
