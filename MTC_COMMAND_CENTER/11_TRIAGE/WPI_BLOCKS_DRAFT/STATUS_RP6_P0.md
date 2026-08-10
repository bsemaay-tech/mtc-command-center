# RP6-P0 — status: ROUND-3-REPAIRED-PENDING-T0-REAUDIT

Updated 2026-08-10 by the round-3 implementer (`claude-opus-5` xhigh, fresh
session). Audit tier: **T0** (host/execution-domain preflight). Round 2's Claude
flagship re-audit (`RP6_CLAUDE_REAUDIT_R2_2026-08-10.md`) confirmed all seven
original findings CLOSED and returned REQUEST_CHANGES on three residuals; those
three plus both nits are repaired here. **This is round 3 of 3 — the T0 cap is
now exhausted**, so the next verdict is terminal for this cycle: an accepting
verdict finishes the loop, and a non-accepting one must be reported to Barış
rather than opening a fourth round. Acceptance still requires fresh independent
`claude-opus-5` xhigh and `gpt-5.6-sol` xhigh verdicts. The block remains a draft:
not frozen, accepted, dispatchable, or authorised for host execution.

Current executable identity:

```text
sha256=2d9b166eacfc39ebe0d8d89edb5860876ccc4d9f0ff97f9e10a228dbcf96289e
bytes=71743
bash_n=PASS
line_endings=LF_only
bom=none
superseded_round2_sha256=041c9da9769e36638c9785b54afc638fa8e7b475a6d24238fc10388916c048db
superseded_round2_bytes=66381
```

Round-3 disposition (re-audit R2 findings 1-3, nits 1-2) — full record in
`RP6_REPAIR_R3_REPORT.md`:

- **R2-F1 (MEDIUM):** the non-executable-tool STOP no longer asserts an
  invocation status it never observed. It now emits
  `tool_not_evaluable tool=<t> path=<resolved> rc=na
  detail=access_builtin_x_denied mechanism=access_builtin_x` — required token
  kept, resolved path restored, fabricated `rc=126` gone. Prereg §8.1 row 1 was
  amended to `rc=<n|na>` because P0 decides executability with shell builtins
  only and never invokes an inventory tool, so no arm of this block can carry an
  honest invocation status.
- **R2-F2 (MEDIUM):** the repair's own D026 evidence reproduces again. The
  full-block fence's RED side is pinned to the immutable `0bbc3591`
  (`= 90d8d447^`) instead of the moving `HEAD`, for both the block and the prereg
  draft, and all four recorded transcripts were re-executed and replaced. Three
  reproduce byte-identically; the fence matches after normalizing only its random
  `mktemp` root.
- **R2-F3 (LOW/MED):** row 8 now discriminates a crafted `/proc`. Each namespace
  link's followed device is compared against the root object's device — a
  namespace inode lives on the anonymous `nsfs` superblock, so a fabrication
  allocated on the root filesystem is refused as
  `namespace_link_on_root_filesystem`. Because a fabrication on any *other*
  filesystem would still pass, the evidence line states
  `procfs_identity=not_established` and the terminal claim carries
  `procfs_mount_identity_of_the_namespace_links` in `does_not_establish`.
- **Nit 1:** the `(os error 2)` classifier alternative was **dropped**, not kept,
  and its provenance corrected (see F1 below).
- **Nit 2:** the block header now names the GNU-producer assumption explicitly.

Full-block repair disposition:

- F1: the filesystem diagnostic classifier now accepts only the exact absolute
  `$P0_STAT` argv[0] prefix and the controlled C-locale GNU coreutils
  `stat`/`statx` forms. Both real-lstat missing-object arms flip from unclassified
  STOP rc 3 to the required host FAIL rc 1. **Corrected in round 3 (R2 nit 1):**
  the `(os error 2)` alternative this bullet used to call "the observed ENOENT
  form" was never observed here. `(os error N)` is a Rust `std::io::Error`
  rendering from uutils coreutils, and uutils prefixes its messages with the
  *basename* of `argv[0]`, so an absolute prefix combined with that suffix is
  unreachable. Round 3 deleted the alternative. The residual is stated in the
  block header: on a uutils host the whole class returns fail-closed at rc 3
  `path_probe_unclassified` rather than FAIL, and the shape must be re-pinned
  before such a host is preregistered.
- F2: P0 now requires frozen deploy-channel pins for user/mount/PID/network
  namespaces plus `stat -c '%d:%i' /`, validates the prelude values with reasoned
  rc-3 pre-checks and `:?` backstops, compares every live identity, and gates the
  manager query behind the comparison. Missing/unreadable input is
  `execution_domain_unattested`; mismatch is `execution_domain_mismatch`.
- F3: repeated separators in `P0_VENV_ROOT` STOP as
  `input_not_canonical_spelling` before any host object verdict.
- F4: duplicate/conflicting tool pins STOP as
  `prereg_input_malformed name=P0_TOOL_PINS duplicate=<tool>`; the count is now
  the count of distinct accepted tools.
- F5: every readlink producer uses `-v`; failed captures have nonempty bracketed
  `detail=` plus an explicit diagnostic-shape token.
- F6: getent capture uses NUL-delimited `mapfile` records with an out-of-band rc
  record; NUL emitted by the producer creates an extra record and becomes
  `identity_unresolvable` via `nul_byte_in_merged_capture`, never no-match.
- F7: `tool_not_evaluable` and `group_query_not_evaluable` are executable reason
  tokens. Every `identity_unexpected` line now uses
  `observed_numeric=<u:g> expected_numeric=<u:g> account=<a>`; §8.1 row 3 was
  aligned without changing row 9.

**Freeze gate — mandatory, same class as RP7.** The following embedded literals
remain `<PIN-AT-FREEZE>` and deliberately prevent an end-to-end `P0 PASS`:

- `P0_FIXED_ATTESTED_USER_NS`
- `P0_FIXED_ATTESTED_MNT_NS`
- `P0_FIXED_ATTESTED_PID_NS`
- `P0_FIXED_ATTESTED_NET_NS`
- `P0_FIXED_ATTESTED_ROOT_MOUNT_ID`

Before freeze/dispatch, the root-authorised deploy channel must mint the four exact
`readlink /proc/<attested-host-pid>/ns/<kind>` tokens and the exact
`stat -c '%d:%i' /` identity, embed each literal, supply identical prelude values,
and re-run the whole block on the intended guest. No value may be learned or
re-pinned from the login session being tested.

Local evidence, all re-executed in round 3 against `2d9b166e…` / 71743 B: the
literal full-block fence in `SELF_QA_RP6.md` ends
`RP6_FULLBLOCK_D026_SUMMARY findings=7 round3_residuals=3 real_lstat_arms=2
execution_domain_cases=9 readlink_stop_arms=3 result=PASS` at process rc 0, and its
normalized re-run transcript matches the recorded output. The separate
freeze-literal fence passes with placeholder rc 3 and filled-fixture rc 0. The
16-case C13 R3 arm harness, the 27-case C13 R4 arm harness and the four-case
backstop harness all pass at rc 0, and each of those three recorded transcripts is
now byte-identical to a fresh re-run (`cmp` clean) from the line range the document
cites. No host, SSH, network, deployment, backtest, broker, or trading action
occurred, and no commit was made.

---

# Prior status history — REPAIRED-PENDING-AUDIT, do not treat as accepted

Updated by the Codex implementer on 2026-08-10 under owner amendment A2/A2a. The
repair and its local falsification evidence are ready for independent Lead review;
the block is not frozen, accepted, dispatchable, or authorised for host execution.

- **F1 — REPAIRED BY HONEST DISCLOSURE.** The false fixed child count was removed.
  The header and terminal evidence now state the mixed environment, PATH-resolution,
  inherited-cwd and inherited-or-unset-TMPDIR surface, and explicitly do not claim
  round-1.4 probe-execution-environment binding. Full binding needs new preregistered
  inputs and is outside this bounded repair.
- **F2 — CLOSED BY LEAD ADJUDICATION; NO BLOCK CHANGE.** The existing STOP polarity
  remains correct under draft round 1.4's numeric-identity rows.
- **F3 — REPAIRED BY EXPLICIT RESIDUAL DISCLOSURE.** The terminal evidence now says
  P0 does not establish interpreter intermediate-component or symlink-target binding.
  Learning a target at runtime would violate row 18; accepting one requires a future
  preregistered target chain.
- **F4 — REPAIRED.** `:?` fail-closed backstops now follow the rc-3 pre-checks for
  `P0_EXPECT_UID`, `P0_FORBIDDEN_GIDS`, and `P0_VENV_ROOT`.

`SELF_QA_RP6.md` records literal local commands and real RED/GREEN output. No host
was contacted; no ssh, network, backtest, deployment, or trading action was run.

## C13 round — getent resolution arm (GLM-5.2 implementer, 2026-08-10)

Added by GLM-5.2 as IMPLEMENTER under the bounded C13 kickoff (round-1.4
section 8.1 rows 1–3, repair C13; Lead-adjudicated real conformance gap). Status
stays **REPAIRED-PENDING-AUDIT** — the Codex (G5) audit is outstanding, so the
block remains not frozen, not accepted, not dispatchable, and not authorised for
host execution.

- **C13 — IMPLEMENTED; QA EXECUTION PENDING.** Added one arm to `RP6-P0.sh`: a
  pinned-absolute `getent` (added to the inventory as the 12th RO tool) resolves
  `gatea` and `mtc-bridge`, each record parsed whole under the passwd grammar
  (Pattern 5; duplicate/multiline/malformed → ambiguous → STOP), admitting on
  NUMERIC uid/gid only (Pattern 8) with names as diagnostics. rc contract per
  the kickoff and the F2 polarity: getent missing/error/unparsable/duplicate →
  `identity_unresolvable` rc 3; `gatea` numeric mismatch → `identity_unexpected`
  rc 3; `mtc-bridge` valid no-match (rc 2) or numeric mismatch →
  `state_account_resolution_unexpected` rc 3. Two new preregistered inputs
  `P0_STATE_UID` (999) / `P0_STATE_GID` (988) use the same `p0_require_uint`
  rc-3 pre-check + `:?` backstop as `P0_EXPECT_UID` (F4 pattern). Claim lines
  updated honestly (11→12 tools; adds
  `name_to_numeric_resolution_of_gatea_and_mtc_bridge_via_getent`; discloses
  `nss_source_identity_of_getent_resolution`; `getent` joins the inherited-env
  set). Read-only scope, the 0/1/3 contract, STOP-vs-FAIL truthfulness, and all
  existing arms are preserved.
- **QA NOT YET EXECUTED — concrete harness blocker.** The GLM-5.2 implementer
  session's Bash tool gates interpreter/script execution (every `bash -n`,
  `bash -c`, path-script run, process substitution, brace heredoc, and
  off-tree write returned *requires approval* and was not approved this turn).
  `SELF_QA_RP6.md` therefore contains the paste-and-run RED/GREEN + backstop
  commands and the real final SHA-256/byte count, but the RED/GREEN real output
  and `bash -n` are marked **PENDING**, not fabricated. Per AGENTS.md the
  implementer reports this blocker rather than silently substituting fake
  evidence (D026 / Pattern 10; the GLM known-failure-mode of AGENTS.md rule 4).
- **Artefact (real, computed in-session).** Repaired `RP6-P0.sh` SHA-256
  `cfdb23b8834a783638723c54cf632973c1cc20c5fb676cb6d310a9d43b9acf1c`, 54109
  bytes (baseline `6c5b8945…766f7`, 44979 bytes). Three files touched only
  (`RP6-P0.sh`, `SELF_QA_RP6.md`, this file); nothing committed.

**Required to close C13:** run the C13 commands in `SELF_QA_RP6.md` in an
unhindered Git Bash process (or have Codex run them at G5), paste the real
RED/GREEN output, and confirm `bash -n` PASS — then the Codex G5 audit.

**Lead QA execution, 2026-08-10 — the blocker above is CLEARED.** The Lead ran
the full C13 QA in an unhindered Git Bash: arm RED/GREEN 5/5 CASE_OK (GREEN
rc 0; four REDs rc 3 with the exact preregistered reason tokens); backstop
2/2 GREEN after a Lead harness correction (the drafted C13 backstop caller fed
`sed` no input and its summary was ungated — both defects recorded with the
as-drafted failing run in `SELF_QA_RP6.md`, then fixed); `bash -n` PASS; hash
and byte count re-verified identical to the implementer's record
(`cfdb23b8…`, 54109 B). Real outputs pasted into `SELF_QA_RP6.md`. Remaining
to close: the independent Codex G5 audit of the C13 arm.

## C13 round 3 — Codex audit repair (Claude Opus 5 implementer, 2026-08-10)

The Codex G5 audit of the C13 arm returned **BLOCK, 3 findings**
(`RP6_C13_CODEX_AUDIT_2026-08-10.md`: V2/V3/V5 FAIL, V1/V4/V6 PASS). GLM-5.2, the
C13 implementer, is quota-blocked, so Claude Opus 5 executed this bounded repair
round as implementer; it neither authored nor audited the C13 arm. Status stays
**REPAIRED-PENDING-AUDIT** — the block is not frozen, not accepted, not
dispatchable, and not authorised for host execution, and the Codex re-audit is
outstanding.

- **F1 (HIGH) — REPAIRED IN THE BLOCK.** `p0_resolve_passwd` accepts getent
  `rc 2` as `nomatch` only when the complete merged capture is empty, this
  interface's exact valid-no-match shape. `rc 2` carrying any byte (NSS
  diagnostic, partial record, module warning) is now `error`, so the caller emits
  `identity_unresolvable … rc 3` instead of asserting a positive absence it never
  observed. `P0_PW_DIAG` on the surviving no-match path records
  `empty_capture_at_rc2`. All other parser arms and both caller `case` statements
  are byte-identical, and the genuine `mtc-bridge` valid no-match still yields
  `state_account_resolution_unexpected observed_numeric=absent` (regression-tested).
- **F2 (MEDIUM) — REPAIRED IN THE QA.** The two earlier C13 fences are re-labelled
  SUPPLEMENTAL in place, and two D026 harnesses were added and executed locally.
  Harness 1 (16 cases) no longer calls the arm: it appends the block's own
  top-level driver lines, matched as exact whole lines out of the source bytes, so
  the block decides whether the arm runs; it then runs one assertion set across
  three variants — R3-repaired bytes, pre-R3 bytes (`cbaf3ec8`, `cfdb23b8…`), and
  bytes with the production integration call deleted. Deleting that call takes all
  three arm assertions to `ASSERT_UNMET`; the pre-repair bytes fail every F1
  assertion and are separately recorded emitting the defective
  `observed_numeric=absent` verdict. Harness 2 (4 cases) adds the mutation that
  removes each new `:?` backstop itself. Both harnesses check assertion POLARITY,
  so a surviving mutant fails the run.
- **F3 (MEDIUM) — REPAIRED IN THE BLOCK.** The "NUMERIC IDENTITY ONLY" header no
  longer claims that no name is looked up or captured and that the block asks the
  resolver database nothing. It states the truth: admission is numeric only and no
  name is ever compared or asserted; two names ARE queried via the pinned
  `getent passwd`; the returned name/gecos/home/shell fields are diagnostics no
  verdict depends on; NSS source identity is not established.
- **Artefact (real, computed in-session, Git Bash).** Repaired `RP6-P0.sh`
  SHA-256 `ef205e2064caa0cb1493abf037ce9d435f2bf8f6259c5bb3fc4964d1abb2b4b9`,
  55467 bytes (pre-R3 `cfdb23b8…`, 54109 bytes; diff 34 insertions / 12
  deletions, one file). `bash -n` rc 0, `BASH_N=PASS`. Harness 1 process rc 0,
  `C13_R3_ARM_QA_SUMMARY cases=16 result=PASS`; harness 2 process rc 0,
  `C13_R3_BACKSTOP_QA_SUMMARY … cases=4 result=PASS`. Both fenced commands in
  `SELF_QA_RP6.md` were re-run from the document itself and diffed byte-for-byte
  against the pasted output.
- **Scope.** Four files touched (`RP6-P0.sh`, `SELF_QA_RP6.md`, this file,
  `RP6_C13_REPAIR_R3_REPORT.md`); nothing committed; no host contacted and no
  network command run. Read-only scope, the rc 0/1/3 contract, and every
  pre-existing arm are preserved.

**Required to close C13:** the independent Codex re-audit of the R3 bytes
`ef205e20…` (55467 B) against `RP6_C13_CODEX_AUDIT_2026-08-10.md`. — DONE: that
re-audit ran and returned BLOCK with 2 findings; see the round-4 section below,
which supersedes this requirement.

## C13 round 4 — Codex re-audit repair (Claude Opus 5 implementer, 2026-08-10)

The Codex re-audit of the R3 bytes returned **BLOCK, 2 findings**
(`RP6_C13_REAUDIT_CODEX_2026-08-10.md`: V1 and V4 FAIL, V2/V3/V5 PASS). This is the
last bounded round under the T0 cap. Claude Opus 5 executed it as implementer; it
neither authored nor audited the C13 arm. Status stays **REPAIRED-PENDING-AUDIT** —
the block is not frozen, not accepted, not dispatchable, and not authorised for host
execution.

- **Finding 1 (HIGH) — REPAIRED IN THE BLOCK.** `p0_resolve_passwd` captured getent
  with a plain `$( … )`, which deletes trailing newlines, so the `[ -n "$raw" ]`
  emptiness test could not tell a truly empty rc-2 capture from a newline-only one
  and admitted the latter as a valid no-match. The capture now appends a sentinel
  byte INSIDE the substitution and strips it afterwards, so the complete merged
  stream survives; `had_bytes` is decided on those preserved bytes before any
  normalization. A newline-only rc-2 capture is now `error` with
  `P0_PW_DIAG=newline_only_capture_at_rc2`, and the caller emits
  `identity_unresolvable … rc 3` for both accounts. getent sits on the left of `||`
  inside the substitution so an inherited `set -e` cannot kill the subshell before
  the sentinel is written, and its own rc is carried out by re-exiting the subshell
  with it. If the sentinel is missing anyway, the capture was truncated by something
  other than getent and the outcome is `error` / `capture_sentinel_lost` — fail
  closed, never a no-match. After the emptiness question is answered `raw` is
  normalized back to the value plain command substitution used to produce, so the
  rc-0 record parse and every diagnostic string are byte-identical to the
  R3-audited behaviour.
- **Finding 2 (MEDIUM) — NO REPAIR, LEAD-ADJUDICATED.** The extra committed
  provenance log was added by the Lead at commit time, not by the round-3
  implementer; the Lead recorded it as an accepted Lead-side deviation. Out of this
  round's scope; the file was not touched.
- **Same-pattern sweep.** `p0_resolve_passwd` is the only site in the block that
  adjudicates rc 2 as its own outcome (one `2)` case arm in the file). Every other
  capture site treats any non-zero rc as an error, and every other emptiness test —
  e.g. `p0_capture_numeric`'s `[ -n "$raw" ] || p0_stop identity_probe_empty` —
  fails CLOSED, so newline stripping there can only cause a STOP, never a false
  admission. No other site was changed.
- **QA (real, local Git Bash, D026).** `SELF_QA_RP6.md` harness 1 was extended, not
  replaced: all sixteen R3 cases verbatim, plus a fourth source variant `prer4` (the
  committed R3 bytes `ef205e20…`), three newline-only rc-2 shim modes
  (`mtc_rc2_newline`, `mtc_rc2_newlines3`, `gatea_rc2_newline`), the `nocall`
  mutation applied to the new case as well, and a probe that prints the auditor's own
  markers. Result: `C13_R4_ARM_QA_SUMMARY cases=27 result=PASS`, process rc 0, 25
  `CASE_OK` + 2 `PROBE_OK`, zero `CASE_BAD`. The new fixture is GREEN on R4 bytes
  (`identity_unresolvable … detail=[newline_only_capture_at_rc2]` rc 3) and RED on
  the R3 bytes, which are separately recorded emitting the defect
  (`state_account_resolution_unexpected … observed_numeric=absent`). The probe
  reproduces `FALSE_NOMATCH_REPRODUCED=yes` / `REQUIRED_ERROR_OUTCOME_PRESENT=no` on
  R3 bytes and `no` / `yes` on R4 bytes. Harness 2 was re-run unchanged against the
  R4 bytes: process rc 0, `C13_R3_BACKSTOP_QA_SUMMARY … cases=4 result=PASS`.
- **Artefact (real, computed in-session, Git Bash).** Repaired `RP6-P0.sh` SHA-256
  `bff3c86e6e9b565c55da34580284f22c80253d9e931d879fd749459bac85b7cf`, 57441 bytes
  (pre-R4 `ef205e20…`, 55467 bytes; diff 36 insertions / 5 deletions, one file).
  `bash -n RP6-P0.sh` rc 0, `BASH_N=PASS`. The extended harness was re-run from the
  document itself (`sed -n '1159,1324p' SELF_QA_RP6.md | bash --noprofile --norc`)
  and its pasted output is that run.
- **Scope.** Four files touched (`RP6-P0.sh`, `SELF_QA_RP6.md`, this file,
  `RP6_C13_REPAIR_R3_REPORT.md`); nothing committed; no host contacted and no network
  command run. Read-only scope, the rc 0/1/3 contract, and every pre-existing arm are
  preserved.

**Required to close C13:** the independent Codex re-audit of the R4 bytes
`bff3c86e…` (57441 B) against `RP6_C13_REAUDIT_CODEX_2026-08-10.md`.
