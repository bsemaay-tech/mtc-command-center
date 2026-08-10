# RP6-P0 — status: REPAIRED-PENDING-AUDIT, do not treat as accepted

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
`ef205e20…` (55467 B) against `RP6_C13_CODEX_AUDIT_2026-08-10.md`.
