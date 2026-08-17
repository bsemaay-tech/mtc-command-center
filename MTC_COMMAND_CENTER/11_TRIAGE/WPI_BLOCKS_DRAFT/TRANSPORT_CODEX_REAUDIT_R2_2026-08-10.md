# REQUEST_CHANGES — 4 required findings

**Tier and slot:** T0, fresh Codex flagship `gpt-5.6-sol`, xhigh, round-2
re-audit. Owner amendment A2/A2a was observed: this audit was performed directly,
with no sub-delegation.

**Scope and source identity:** the eight transport targets were audited at commit
`9ef4437d1391065b5e5485db963d1f62dc4ea67d`. Their blobs are unchanged through
the audit-time `HEAD` (`4f58e650f8ef57b23cc03c50df051a3f377f59fe`). The ratified
preregistration input was the current tracked blob
`19e4c969889da61838f2759cb539bc27f58ffed9`, which contains the amended four-class
section-4 contract. Concurrent `RP6-P0.sh` / `RP7-WPI-RO.sh` work and the other
flagship's report were not used or modified.

This was local-only verification. No staging host, SSH/SCP connection, credential,
service, broker, exchange, or trading action was performed. Network activity was
limited to the self-QA's loopback sockets. The only repository file written by this
audit is this report.

The repaired binder itself is sound: an equal remote/local pair now binds at rc 0,
and unequal pairs discriminate. The set is nevertheless not safe to freeze or
dispatch. Raw OpenSSH/SCP failures and cleanup failures are still classified as
deviant host observations; the constructed environment makes the real pinned
OpenSSH program exit 255 before a connection; the byte-identical accepted close
script still executes evidence-producing helpers from inherited `PATH`; and the
setup repair omitted the accepted mount-object bind required by round-1 Codex F5.

## V1–V16 — original required-finding closure ledger

| V | Original finding | Result | Independent evidence |
|---|---|---|---|
| **V1** | Codex F1 — STOP converted to transport FAIL | **NOT CLOSED** | A direct child rc 3 now reaches `TR_RUN STOP`, as self-QA `C1/C2` proves. The real classifier is still numeric-only: `transport_runner.ps1:764-789` treats every mismatch other than exact rc 3 as deviant. Independent runner arm `J2` made an `scp_down` transport process return 255: `TR_OP_DEVIANT id=09 rc=255`, `TR_RUN FAIL`, runner rc 1. Arm `J1` began with a reasoned rc-3 STOP, then an `always` cleanup transfer returned 1 because there was no evidence to retrieve; the cleanup was labelled deviant and the final result became FAIL. See required finding F1. |
| **V2** | Codex F2 — `$Matches` capture clobber | **CLOSED** | Literal runner self-QA `A1` used a real close transcript and a byte-equal three-file tree: `TR_BIND_SET` hashes equal, `TR_BIND_PASS files=3`, runner rc 0. `A2` reverted only the capture latch and produced three `digest_differs`, rc 1. `A3/A4/A5` independently failed a changed, extra, and missing file. Captures are latched immediately at `transport_runner.ps1:615-661`. |
| **V3** | Codex F3 — inherited execution environment selects the trusted chain | **NOT CLOSED** | The operator-side PATH plant is refused in recorded `D1/D2`, and both wrappers ignore a PATH-planted `sha256sum`. But those launch arms substitute `cmd.exe` for the real pinned programs. With the exact constructed environment at `transport_runner.ps1:427-455`, local non-connecting `ssh.exe -G qa-target` returned rc 255 with empty stdout/stderr; adding only `PROGRAMDATA=C:\ProgramData` returned rc 0. Separately, accepted `remote_close_tree.sh` invokes bare PATH-selected helpers; an executed PATH plant mutated a closed evidence leaf and the accepted bytes still emitted `CLOSE PASS ... wrote_into_evidence_tree=0`. See F2/F3. |
| **V4** | Codex F4 — ambiguous path failure authorizes mutation | **CLOSED** | Literal shell arms reproduced round-1 RED `A2` (`SETUP PASS`, rc 0, four directories created) and repaired GREEN (`path_probe_multiline`, rc 3, zero directories). `A3` put both error classes on one line and also STOPped before mutation. |
| **V5** | Codex F5 — parent/identity bound only after mutation | **NOT CLOSED** | Numeric ownership, parent-component symlink refusal, and bind-before-`mkdir` are real: `A4` creates four directories through the old symlinked parent but the repaired script creates zero; `A5` rejects a name-rendered `root:root` alias whose numeric identity is `1000:1000`. However, round-1 F5 also required binding the **accepted mount object before allocation**. `remote_setup_wpi.sh:96-130,218-236` checks canonical spelling, symlinks, numeric ownership, searchability, and mode only. It contains no mount/mountinfo/device predicate. A bind/overlay mounted at the same canonical path with matching metadata passes those checks and receives the four mutations. See F4. |
| **V6** | Codex F6 — extractor consumes stdout before completion/diagnostics | **CLOSED** | Literal shell arms reproduced listing-warning RED `B2` as rc-0 PASS and GREEN as `tar_type_listing_diagnostics`, rc 3; unterminated-record RED `B3` PASS and GREEN STOP; hard listing failure `B6` STOP. `run_capture` adjudicates the two statuses, diagnostic equality, CR, and final LF before assigning `CAPTURE_OUT`; the archive is re-hashed after listing. |
| **V7** | Codex F7 — extractor outside section-4 derivation | **CLOSED under the ratified D-1 text** | Current section 4 names exactly four permitted classes. Mechanical diffs remain `178 insertions / 51 deletions` for setup and `246 / 69` for extractor. Changed regions map to constants/count derivation, program-path checks, STOP-before-mutation classification, or status-before-stdout adjudication. No literal six-member count remains outside `MEMBERS`; `RP1-B3.sh` is absent. The wider contract's security completeness is separately non-accepting under V17/F3/F4. |
| **V8** | Codex F8 — op-02 cwd | **CLOSED** | Plan op 02 and `$RUNKIT_DIR` both resolve to the distinct `WPI_BLOCKS_DRAFT\01_RUNKIT`. Literal runner arms `F1/F2` select that archive and refuse a same-name decoy beside the runner. |
| **V9** | Codex F9 — ops 07/08 stdin artifact absent | **CLOSED** | Plan rows 07/08 name `ACCEPTED:remote_close_tree.sh`; runner arms `F3/F4/F5` prove the accepted root resolves to the Stage-2 file at `87157f0e…`, absence STOPs, and the wrong root token STOPs. The actual accepted file is 7470 bytes and byte-equal to the pinned identity. |
| **V10** | Codex F10 — QA not executable / broken safety path omitted | **NOT CLOSED** | Both embedded suites are now literal and executable: shell suite 254 lines / 477 output lines / rc 0; runner suite rc 0 and reached its completion marker. But the claimed 8-of-12 launch-path evidence replaces both `ssh` and `scp` with `cmd.exe`, so it cannot expose the real OpenSSH environment failure in F2. It also omits the accepted close script's inherited-PATH attack in F3. The statement that every undriven arm fails only STOP-ward is contradicted by real OpenSSH rc 255 becoming FAIL. |
| **V11** | Claude F1 — `$Matches` root cause | **CLOSED** | Same executed `A1/A2` evidence as V2. `CLOSE_SIZE` captures are latched too, and sizes are compared at `transport_runner.ps1:700-705`. |
| **V12** | Claude F2 — exit-3 rollup | **NOT CLOSED** | Same executed `J1/J2` evidence as V1. Exact rc 3 is repaired, but transport inability expressed by the invoked program's native rc is still re-labelled FAIL. The real pinned OpenSSH binary deterministically supplies such rc 255 under the delivered environment. |
| **V13** | Claude F3 — close artifact and op-02 cwd | **CLOSED** | Same `F1-F5` evidence as V8/V9. Co-location-by-token resolves byte-identically and the kit directory is distinct. |
| **V14** | Claude F4 — section-7 and external launch coverage | **NOT CLOSED** | Section-7 local binding is now genuinely executed and load-bearing. The external launch arm is not: it proves only that `ProcessStartInfo` can run the substituted `cmd.exe`. The kickoff explicitly required real, non-stub launch arms. Actual no-network OpenSSH configuration evaluation fails under the shipped child environment, while the accepted remote close program chain remains PATH-selectable. |
| **V15** | Claude F5 — extractor count literals outside derivation | **CLOSED** | `MEMBER_COUNT` is derived only from `MEMBERS`; five-member mutation `B4` fails under the old literal-six behavior and passes with the derived value. The actual member set is the six WP-I basenames and excludes `RP1-B3.sh`. |
| **V16** | Claude F6 — allocation marker lacks fail-closed guard | **CLOSED** | Literal `E1` emits `TR_STOP reason=unfilled_marker field=RECORD_ROOT`, rc 3; `E2` removes the gate/trap and reproduces the localized raw `Test-Path` failure at rc 1. Exact delivered-file arm `I` STOPs on `BASE_RUN` before path use. |

## V17–V19 — round-2 decisions and integrity

| V | Result | Evidence |
|---|---|---|
| **V17 — D-1 and Lead adjudications** | **NOT CLOSED** | The four-class derivation map is mechanically bounded, D-2 co-location-by-token resolves to accepted bytes, and D-3 is real: both shipped `_wpi` scripts STOPped rc 3 on this WSL host's symlinked `/usr/bin/stat`, before creating their target paths. But D-1 is not coherent as an end-to-end program-identity closure: it covers the two derived scripts while the executed, accepted `remote_close_tree.sh` still resolves `mktemp`, `stat`, `tr`, `readlink`, `find`, `sort`, `sha256sum`, and `cmp` from inherited PATH. The derived scripts and wrappers also compare no frozen digest for their remote tools; their `require_tool` gates bind a locator and final-component metadata, not executable bytes. Finally, class 3 omits the accepted mount-object predicate required by original F5. |
| **V18 — placeholders / no allocation** | **PASS-WITH-NIT** | All placeholders remain literal and no concrete WP-I RUNID was minted. Actual census: six executable/plan files contain 36 `<ALLOCATE-AT-DISPATCH>` and 27 `<PIN-AT-FREEZE>` occurrences; all eight files contain 41 and 33 respectively. `SELF_QA_TRANSPORT.md:1807` claims 36 and 40, so its pin count is false (N1), but no executable pin was found silently filled or removed. |
| **V19 — bytes, hashes, syntax** | **PASS** | All eight byte counts and hashes below equal their exact `9ef4437d` blobs. Git Bash `bash -n` passed the four shell targets and accepted `remote_close_tree.sh`. Windows PowerShell 5.1.26100.8875 parsed the runner with zero errors. Accepted derivation sources re-verified at 4976/`faee3725…`, 8270/`ba0bef0e…`, and 7470/`87157f0e…`. |

## Required findings — most severe first

### F1 — CRITICAL — native transport/cleanup failures still become host-state FAIL

`transport_runner.ps1:478-522` returns the external program's raw exit code.
`transport_runner.ps1:764-789` recognizes only exact rc 3 as not-evaluable and
calls every other mismatch deviant. That is valid for completed block probes whose
contract is 0/1/3; it is invalid for the transport programs themselves.

Independent local runner arms used the delivered classifier and the same real
`Invoke-ExternalProcess`, with `cmd.exe` substituted only to produce deterministic
native transport statuses without host contact:

```text
=== J1_INITIAL_STOP_PLUS_CLEANUP_ERROR ===
TR_OP_END id=01 rc=3 expect_rc=0
TR_OP_NOT_EVALUABLE id=01 rc=3 expected=0
TR_OP_END id=09 rc=1 expect_rc=0
TR_OP_DEVIANT id=09 rc=1 expected=0
TR_RUN_CLASS deviant=1 not_evaluable=1
TR_RUN FAIL ...
RUNNER_RC=1

=== J2_RAW_TRANSPORT_RC255 ===
TR_OP_END id=09 rc=255 expect_rc=0
TR_OP_DEVIANT id=09 rc=255 expected=0
TR_RUN FAIL ...
RUNNER_RC=1
```

This is not hypothetical cleanup ordering. If setup or a wrapper STOPs before an
evidence directory exists, accepted `remote_close_tree.sh:76-81` returns FAIL for
the absent tree, subsequent SCP retrieval fails, and those `always` outcomes
outvote the truthful earlier STOP. Likewise SSH connection/auth/configuration rc
255 is transport inability, not an observation that staging state is deviant.

Required repair: classify by operation kind and provenance, not only integer.
At minimum, SSH's transport rc 255 and every failed SCP transfer must be STOP;
remote wrapper/block 0/1/3 results may retain their probe meaning only after the
runner has established that SSH actually ran the remote command. Cleanup whose
prerequisite evidence tree was never created must not manufacture a FAIL. Add a
whole-plan RED/GREEN with an early STOP plus all actual `always` rows.

### F2 — CRITICAL — the constructed environment cannot run the real pinned OpenSSH program

The child environment at `transport_runner.ps1:427-455` is cleared and rebuilt,
but it omits `PROGRAMDATA`, which OpenSSH for Windows needs to resolve its system
configuration. The recorded program arm substitutes `cmd.exe`, so it cannot fail
on this dependency.

A no-network configuration evaluation used the actual pinned
`C:\Windows\System32\OpenSSH\ssh.exe`, the delivered environment values, the real
operator profile values, and the runner's trusted cwd:

```text
DELIVERED_ENV_RC=255 STDOUT_BYTES=0 STDERR_BYTES=0
WITH_PROGRAMDATA_RC=0 STDOUT_BYTES=4082 STDERR_BYTES=0
```

The only mutation in the GREEN arm was adding `PROGRAMDATA=C:\ProgramData`.
Therefore the delivered plan cannot reach a remote block; it exits natively 255,
which F1 then falsely reports as host FAIL.

Required repair: either add and independently bind every OpenSSH-required
environment/config path, or explicitly disable ambient configuration and supply
all required configuration through pinned arguments/files. Exercise the real
pinned `ssh.exe` and `scp.exe` locally without connecting (configuration/argv
evaluation), then retain a separate no-network process-capture arm. `cmd.exe` is
supplemental, not closure evidence for OpenSSH.

### F3 — CRITICAL — the accepted close program chain is PATH-selected and can mutate “closed” evidence while reporting PASS

`remote_close_tree.sh` is correctly resolved at its accepted 7470-byte identity,
but its internals are not bound. It invokes bare `mktemp`, `stat`, `tr`,
`readlink`, `find`, `sort`, `sha256sum`, and `cmp`. This contradicts
`STATUS_TRANSPORT.md`'s claim that nothing on inherited PATH selects
evidence-producing code and leaves the most important evidence-binding operation
outside D-1 class 2.

An executed local falsification used the exact accepted bytes, the same recorded
owner substitution used by both flagship audits, and a PATH-first `sha256sum`
that appended to the evidence leaf once before delegating to the real tool:

```text
ATTACK_RC=0
PRE_SHA=51255217e786029054afcac9e635bd2bc6f58e31fe86a4564867d07e5109699c
POST_SHA=1335f476fe6c5977711b33e3f891a44b9746225beeb66dd1d00aa1b46beaae70
MUTATED=yes
CLOSE_DIGEST 1335f476...beaae70  a.txt
CLOSE PASS ... files=1 wrote_into_evidence_tree=0
STDERR_BYTES=0
```

The two digest passes agree because both observe the post-stage mutation, and
the later local binder would also bind those retrieved post-mutation bytes. Thus
the accepted script's `wrote_into_evidence_tree=0` sentence is false under the
delivered execution environment.

The two `_wpi` scripts and wrappers improve on this by using absolute paths, but
they still compare no frozen tool digest; `require_tool` checks only final kind,
execute bit, numeric owner, and mode, using `stat` as its own bootstrap. That does
not meet round-1 F3's required frozen program identity.

Required repair: place the close operation under the same reviewed remote
program-identity contract as every other executed support script, with no
inherited-PATH lookup. Bind executable bytes (and the relevant component/mount
chain) to Stage-1 facts rather than treating an absolute locator as identity.
Because `remote_close_tree.sh` is currently byte-frozen accepted input, any
derivation or wrapper change must be explicitly scoped and re-audited; do not
silently edit the accepted artifact.

### F4 — HIGH — setup still does not bind the accepted mount object before mutation

Round-1 Codex F5 required the full parent chain **and accepted mount object** to
be bound before allocation. The repair implements only the first half.
`bind_parent_chain` uses `readlink`, final-component kind/searchability, numeric
ownership, and mode. There is no mount identity, device identity, mountinfo
projection, or deploy-channel value anywhere in `remote_setup_wpi.sh`.

Consequently a bind/overlay mount at the same literal canonical path, presenting
the expected owner and mode, passes `readlink -f` and every component predicate;
the script then creates all four directories in the substituted object. This is
exactly the non-symlink half of “the leaf is not the path.” The later RP6
attestation cannot make an earlier setup mutation retroactively target the
accepted mount.

Required repair: bind the allocation parent to a preregistered external mount
identity before the first `mkdir`, or explicitly re-adjudicate and waive that
part of original F5. The current D-1 wording is not such an explicit waiver and
must not be treated as silent closure.

## Optional nit

### N1 — placeholder census is inaccurate

`SELF_QA_TRANSPORT.md:1807` records 36 allocation markers and 40 freeze markers.
Re-derived counts are 36/27 for the six executable/plan files and 41/33 for all
eight files. The placeholders themselves are intact, so this is not an additional
runtime repair, but the evidence statement should be corrected under Pattern 10.

## Re-derived target identities

| File | Bytes | SHA-256 |
|---|---:|---|
| `run_p0.sh` | 5215 | `e4ddf87b0869ba0fadcb9750e65f4f276c90667e788e489c5921923b0d3e1f80` |
| `run_ro.sh` | 5933 | `cd659ee9e1edceb496a5ed08707abd283e3cf5f70a3872ab6f1fdc616ac3f4e8` |
| `transport_runner.ps1` | 45066 | `2f076ed9a928656fddf22969ea4bf70de895f2c84c73f13b4c64b8040e72aa9a` |
| `TRANSPORT_PLAN.tsv` | 4631 | `3ff967294ec0f5d592701bc63940b24f2162b38f8734e38c5343930594da7149` |
| `remote_setup_wpi.sh` | 12340 | `e91bae0827f16cbefe2091980c0a049583bd8ce4173f99e802b2d54a224c29a8` |
| `remote_extract_verify_wpi.sh` | 16614 | `8eb9c499a306c11595638d8db38b1611cdd38470ba12d2c0e019116e2139d412` |
| `SELF_QA_TRANSPORT.md` | 127570 | `586804f852b6c8f31ad55414f5d6335f06ed8f4e1fe8148c624aea7ad05e5ee7` |
| `STATUS_TRANSPORT.md` | 3562 | `4c671840f972addad3c057fc7a8d50a3339c2eaccb5e3081da2cbcc66b5c61ab` |

Accepted sources:

| File | Bytes | SHA-256 |
|---|---:|---|
| `02_PREREG/remote_setup.sh` | 4976 | `faee3725325d7155a6309e2371b85a4facba1980f0169c8268e47a75902821b5` |
| `02_PREREG/remote_extract_verify.sh` | 8270 | `ba0bef0ef6ceb91c445e1d74e2c8d3b6fa7ac01e7e4e10216139b96b28c93db3` |
| `02_PREREG/remote_close_tree.sh` | 7470 | `87157f0ea454df7c1f826a8c76a38f3045dd38efdd8fa347644f79251d3f3f0e` |

## Required next action

Do not freeze, allocate, or dispatch this set. Return F1–F4 to the same flagship
implementer for the remaining bounded T0 repair round, preserve the exact
`9ef4437d` target identity as the rejected baseline, and require literal RED/GREEN
for: the real 12-row early-STOP cleanup path; real no-network `ssh.exe` and
`scp.exe` initialization; the close-script PATH mutation; and mount-object
substitution before allocation. Then run both fresh T0 flagship slots against the
same final bytes. This report grants no host, freeze, allocation, execution, or
Git authority.
