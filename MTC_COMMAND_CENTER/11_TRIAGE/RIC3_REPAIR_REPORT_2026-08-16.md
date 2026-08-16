# RIC3 round-4 final repair report

Date: 2026-08-16  
Implementer: Codex flagship implementer  
Audit tier: T0 (deployment, verifier, firewall, launcher trust, rollback, and
host-touching plan surfaces)  
Result: **IMPLEMENTATION COMPLETE; ready for the Lead's independent T0
acceptance.** This report is not an audit verdict or deployment authority.

## Frozen subject and scope

- Working directory: `C:\BRIDGE_RELEASE_INTEGRATION_20260815`
- Branch unchanged: `integration/bridge-release-20260815`
- HEAD unchanged: `a7460784c1563c140ee7c75197aeab2b0170da8a`
- No commit, checkout, reset, stash, or push command was run.
- No host or network was contacted. No installer, verifier, launcher, SSH, SCP,
  rollback, package, systemd, UFW, or audit command was executed against a
  target host.
- No sub-delegation was used.
- No trading, broker, strategy, Pine, parity, MTC behavior, Bridge application,
  or Dashboard V2 file changed.

Worktree files changed:

1. `IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh`
2. `IBKR_PAPER_BRIDGE/deploy/linux/verify.sh`
3. `IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py`
4. `IBKR_PAPER_BRIDGE/deploy/linux/README.md`

External deliverables:

1. `C:\tmp\lane_out\Open-BridgeDashboard_v4.ps1`
2. `C:\tmp\lane_out\PLAN_V6_INPUTS.md`
3. `C:\tmp\lane_out\RIC3_REPAIR_REPORT.md`

## Finding closure

### R1 — D026 dry-run and verifier arms

Route chosen for both arms: **structural**, not narrowed.

Dry-run/installer fence:

- `tests/test_linux_deployment.py:47-84` adds a normalized statement extractor
  that excludes comments and here-document data and rejects unterminated
  continuations, arrays, or here-documents.
- `tests/test_linux_deployment.py:255-401` keeps manifest-ID parity and adds
  structural fences for direct filesystem/identity mutators, non-query
  `systemctl`, child interpreters, redirection targets, the one guarded manifest
  helper, raw `run`, and a closed set of executable heads. An unclassified head
  fails.
- The exact manifest write is allowed only inside `write_install_manifest`, and
  that helper must have exactly one `run_action "manifest-write"` caller.

Verifier fence:

- `tests/test_linux_deployment.py:1053-1122` retains the read-only command,
  redirection, and query-only-systemctl controls.
- `tests/test_linux_deployment.py:1080-1107` inventories every lower-case
  `python*`, `perl`, or `bash -c` token in executable verifier text. Four exact
  existing path/probe lines are admitted; only the two exact venv probes are
  executable interpreter calls. Any added token requires review and fails the
  test.
- `README.md:82-91` states the honest boundary: these controls are structural
  over the shipped scripts' declared/modeled shell grammar and do not claim to
  understand arbitrary future shell or child-interpreter semantics.

Verification: both exact round-3 mutations are RED and the final sources are
GREEN; see the falsification transcript below.

### R2 — UFW parser and independent substring backstop

- `common.sh:179-316` parses every status-table row after the separator.
- `ALLOW IN`, `LIMIT IN`, `ALLOW FWD`, and `LIMIT FWD` share the same numeric
  port/range exposure analysis. Other unmodeled inbound verbs fail closed.
- Explicit `DENY`/`REJECT` inbound/forward rows and explicit outbound rows are
  non-admitting and skipped.
- The `OpenSSH` exception is removed. Every named application-profile row fails
  closed with the explicit numeric-enumeration instruction.
- SSH evidence must now include an explicit numeric inbound `22/tcp` rule.
- `common.sh:297-310` performs an independent post-parser substring scan and
  fails on a non-deny, non-outbound status row containing literal `8790`, even
  if the structured parser was deliberately made blind.
- Fixtures at `tests/test_linux_deployment.py:477-491` cover `OpenSSH ALLOW IN`,
  `8790/tcp LIMIT IN`, and `8790/tcp ALLOW FWD`; all prior destination, range,
  profile, safe-rule, and missing-SSH fixtures remain.

Verification: the old parser fails the new profile/LIMIT expectations; a
deliberately blinded structured parser fails five exposure cases when the
backstop is removed and passes all five when the backstop is restored. The final
targeted set passes.

### R3 — root-executed logrotate asset metadata

- `common.sh:89-126` extends `assert_mode_owner` with optional exact numeric
  UID:GID and object kind. It rejects missing paths, symlinks, wrong kinds,
  unreadable `stat` results, wrong symbolic owner, wrong numeric owner, or wrong
  mode.
- `verify.sh:235-250` checks metadata before byte comparison:
  - `/etc/logrotate.d/mtc-bridge`: regular non-symlink, `root:root`, numeric
    `0:0`, mode `0644`;
  - `/etc/cron.hourly/mtc-bridge-logrotate`: regular non-symlink, `root:root`,
    numeric `0:0`, mode `0755`.
- `tests/test_linux_deployment.py:1125-1201` executes the real verifier section
  with byte-identical fixtures and stubbed `stat`. It separately proves mode
  `0777` rejection and numeric owner `1000:1000` rejection.

Verification: the exact old byte/executable predicates falsely accept real
local-WSL scratch files at `0777 1000:1000` (RED); the repaired test rejects the
unsafe fixture and passes (GREEN).

### R4 — strict launcher fingerprint parsing

- Output: `C:\tmp\lane_out\Open-BridgeDashboard_v4.ps1`.
- `Open-BridgeDashboard_v4.ps1:57-73` accepts only the complete row grammar
  `<positive bits> SHA256:<exactly 43 base64 characters with no padding>
  <nonempty comment> (<key type>)` and extracts only the named second-field
  fingerprint.
- A malformed row throws at line 68; lines 139-144 route that exception through
  the existing `Fail` path. Malformed input is STOP, never skipped.
- The v3-to-v4 delta is limited to the version header, fingerprint parser, and
  catch-to-`Fail` routing: 22 insertions, 7 deletions.
- V3 SHA-256 remained the published
  `533f29db75ebfa12d1bb1ecbe7f40d241d94364c4f41d74d293268b0f053adca`.
- V4 SHA-256:
  `ac68196b4ae99e12892898c0a5bfb2d7d2249fc2bb476619a4c2bdaaebf2a1b5`.

Verification: the exact wrong-key comment-injection row is a v3 false pass and
a v4 rejection; v4 accepts the correct field-2 pin and throws on a malformed
row. PowerShell AST errors: 0.

### R5 — complete literal command inputs

- `PLAN_V6_INPUTS.md:12-248` contains literal Stage 1 through Stage 3.5 command
  blocks.
- Each of the three `scp`/`ssh` invocations includes the complete isolated set:
  `-F NUL`, `IdentityFile=NUL`, both proxies disabled,
  `GlobalKnownHostsFile=NUL`, explicit user known-hosts pin store,
  `IdentitiesOnly=no`, both password methods disabled, `BatchMode=yes`,
  `StrictHostKeyChecking=yes`, `ExitOnForwardFailure=yes`, and
  `ConnectTimeout=10`.
- Every release executable path uses the full 40-hex subject SHA. The document
  contains neither a Unicode ellipsis nor three dots.
- Stage 3 includes the deterministic tar/hash branch, EFS-encrypted backup and
  EFS-encrypted restore-check directories, pinned SCP, `certutil` comparison,
  Windows built-in tar inventory/restore/diff, monitoring commands and exact
  result rules, and the complete Phase-1 re-inventory command set.
- The document header explicitly says these are inputs, not authorization, and
  requires the Lead to atomically repin release/payload/manifest identity after
  the final bytes are committed and packaged.

Verification: all 3 PowerShell code fences parse with zero errors; all 8 Bash
code fences pass `bash -n`; all 3 OpenSSH invocations contain the full option
set; forbidden ellipses: 0.

### R6 — real never-started rollback rehearsal input

- `PLAN_V6_INPUTS.md:81-112` creates one deterministic archive from the actually
  existing never-started `/var/lib/mtc-bridge` and `/etc/mtc-bridge` trees,
  records its SHA-256, validates exactly 64 lowercase hex, and supplies the tar
  path/hash to `rollback.sh`.
- `PLAN_V6_INPUTS.md:249-268` records the source verification: current
  `rollback.sh:57-62` requires a regular file and its exact SHA-256, and does not
  parse the supplied state-manifest file as JSON. Its absent-database branch and
  separate rollback-record behavior are also named.
- No missing `bridge.db` is fabricated and no runtime fallback is selected.

Verification: inspected current `rollback.sh` source directly; the tar path
satisfies its real path/hash input contract.

### R7 — executable fail-closed evidence contract

- `PLAN_V6_INPUTS.md:270-379` provides exact read-only persistence commands:
  preinstalled `sqlite3` is required or STOP; DB/WAL `ls` state is captured and
  adjudicated; `mode=ro` queries record order count, maximum rowid, and
  `schema_version`; DB/WAL hashes are captured; absent WAL is admitted only as
  independently proven rc-2 absence on both sides; all stderr/rc/shape checks
  precede comparison.
- `PLAN_V6_INPUTS.md:380-544` provides the exact network leg: package baseline
  and simulation gates, numeric UID resolution, b64 `connect` audit rule,
  active-rule proof, UTC window markers, `ausearch` extraction, before/after
  numeric lost-counter equality, exact rule deletion and re-list proof, package
  simulation/purge verification, and disposition record.
- Local inspection found neither `ausearch` nor its man page, so the plan makes
  no unverified native-semantics claim. Its wrapper accepts no-match only as rc
  1 plus stdout exactly `<no matches>`, empty tool stderr, active-rule proof,
  and an unchanged lost counter; it writes a normalized explicit `NO_MATCHES`
  record. Every other shape is STOP.
- Zero connect events is required, which is stronger than filtering for only
  non-loopback connects.

Verification: all Bash evidence blocks pass syntax parsing. They were not run
because host/network contact is prohibited in this repair task.

### R8 — self-contained tenancy and removal boundary

- `PLAN_V6_INPUTS.md:545-580` enumerates the complete initial Bridge tenancy and
  later D3 additions: four Bridge roots, user/group, both unit paths/mask,
  logrotate and cron assets, current payload, state archive/hash, both encrypted
  operator directories, D3 evidence, transaction-bounded audit packages, and
  exact UID-scoped audit rule.
- `PLAN_V6_INPUTS.md:581-712` provides exact fail-closed Linux and PowerShell
  removal commands. It includes the cron asset, current payload, state files,
  evidence directory, exact audit-rule removal, baseline-gated audit package
  disposition, units/mask, all Bridge roots, user/group, and both operator-side
  directories. Destructive paths are literal and the PowerShell paths are
  full-path equality checked before removal.
- `PLAN_V6_INPUTS.md:713-742` is a self-contained owner authorization sentence
  naming the complete boundary and prohibitions, including that only the later
  D3 sentence may authorize temporary `auditd` service start/stop while Bridge
  service start and every service enable remain prohibited. It does not
  incorporate the old V2 boundary by reference.

Verification: the complete plan parses; path and ellipsis checks pass. No
removal or package command was executed.

## D026 RED/GREEN evidence

All RED work used isolated scratch copies or an extracted old predicate. No
repository source was reverted and no target host was used.

### Exact installer mutation

Mutation:

```text
install -d -o root -g root -m 0755 /opt/codex-unlisted-direct
```

Final-test RED:

```text
AssertionError: assert not ['install -d -o root -g root -m 0755 /opt/codex-unlisted-direct']
1 failed, 61 deselected
FINAL_TEST_INSTALL_MUTATION_RED_RC=1
```

GREEN: included in `14 passed, 48 deselected in 5.29s` and the final complete
suite.

### Exact verifier interpreter mutation

Mutation:

```text
python3.12 -c 'from pathlib import Path; Path("/tmp/codex-verifier-python").write_text("mutation")'
```

Final-test RED:

```text
Left contains one more item: python3.12 -c ...write_text("mutation")
1 failed, 61 deselected
FINAL_TEST_VERIFY_MUTATION_RED_RC=1
```

GREEN: included in `14 passed, 48 deselected in 5.29s` and the final complete
suite.

### UFW profile, LIMIT, forward, and backstop

Old parser RED against new expectations:

```text
known_openssh_profile: expected failure but old parser returned rc 0
bridge_port_limit_in: expected failure but old parser returned rc 0
2 failed, 9 passed
UFW_LIMIT_PROFILE_OLD_RC=1
```

Independent backstop falsification: the structured classifier was deliberately
changed from `BRIDGE` to `SKIPPED`. With the substring condition removed, five
literal-8790 cases false-passed:

```text
5 failed, 6 deselected
UFW_BACKSTOP_REMOVED_RC=1
```

Restoring only the substring backstop over that still-blinded structured parser:

```text
5 passed, 57 deselected in 3.51s
UFW_BACKSTOP_GREEN_RC=0
```

Final profile/LIMIT/FWD and all retained UFW cases are included in the 14-test
GREEN group and final complete suite.

### Unsafe metadata fixture

Exact old-predicate RED demonstration in local WSL scratch:

```text
OLD_FIXTURE_POLICY=777 1000:1000
OLD_FIXTURE_CRON=777 1000:1000
RED: old byte/executable predicates falsely accepted unsafe metadata
rc=1
```

The old-source regression test also returns `1 failed`, rc 1 because the new
metadata assertions are absent. GREEN executes the real repaired verifier block
with unsafe mode and numeric ownership stubs and is included in the 14-test
GREEN group and final complete suite.

### Launcher fingerprint comment injection

Exact v3 false pass:

```text
V3_TOKENS=SHA256:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA,SHA256:8b6bl/srDevzQ1rycf9FcQFgZXblSMddqak/9JsHBC8
RED: v3 comment injection falsely accepted expected fingerprint
rc=1
```

V4 GREEN:

```text
V4_INJECTION_FIELD2=SHA256:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
V4_MALFORMED_STOP=ssh-add identity row 1 is malformed; STOP and inspect ssh-agent output manually.
GREEN: injection rejected, valid field 2 accepted, malformed row STOP
rc=0
```

## Final validation

Commands were run from the repository root unless an absolute scratch/output
path is shown.

```text
python -m pytest -q -p no:cacheprovider IBKR_PAPER_BRIDGE/tests
1376 passed, 1 warning in 189.98s (0:03:09)
```

The single warning is the existing FastAPI/Starlette `httpx` deprecation warning.

```text
Targeted repaired arms: 14 passed, 48 deselected in 5.29s
common.sh bash -n rc=0
verify.sh bash -n rc=0
Open-BridgeDashboard_v4.ps1 AST errors=0
Plan PowerShell blocks=3, parse errors=0
Plan Bash blocks=8, parse errors=0
Plan complete OpenSSH option sets=3
Plan forbidden ellipses=0
git diff --check rc=0
```

All four changed worktree files are LF-only (`CRLF=0`).

Final `git diff --stat`:

```text
 IBKR_PAPER_BRIDGE/deploy/linux/README.md         |  10 +
 IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh     |  83 +++++--
 IBKR_PAPER_BRIDGE/deploy/linux/verify.sh         |  26 +-
 IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py | 290 ++++++++++++++++++++++-
 4 files changed, 373 insertions(+), 36 deletions(-)
```

Final worktree status:

```text
 M IBKR_PAPER_BRIDGE/deploy/linux/README.md
 M IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh
 M IBKR_PAPER_BRIDGE/deploy/linux/verify.sh
 M IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py
```

Output hashes before this report was written:

```text
Open-BridgeDashboard_v4.ps1  ac68196b4ae99e12892898c0a5bfb2d7d2249fc2bb476619a4c2bdaaebf2a1b5
PLAN_V6_INPUTS.md             e6b1af409711a125c820216cf4d4fb9b9f7af72807fd9d8111f6117750c579d8
```

## Honest-claims check

- The structural-fence documentation is explicitly scoped to the current
  declared/modeled grammar.
- The launcher claim is exactly field-2 parsing under a complete accepted row
  grammar; it does not claim to validate arbitrary `ssh-add` formats.
- The plan is labeled input-only and requires post-commit/package atomic repin.
- The plan does not claim `ausearch` semantics that were unavailable locally.
- The plan does not assume `sqlite3` is installed; absence is an explicit STOP
  and installing it is expressly not authorized here.
- The plan distinguishes inspected/syntax-checked commands from commands that
  were actually run. No host-side result is claimed.
- No regression test is described as closure evidence without a recorded RED
  and GREEN result.
