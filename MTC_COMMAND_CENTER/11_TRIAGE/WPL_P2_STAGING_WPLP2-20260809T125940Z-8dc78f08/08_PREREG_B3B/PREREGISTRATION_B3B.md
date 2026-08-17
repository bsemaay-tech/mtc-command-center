# WP-L Phase 2 - Stage 2B immutable B3B preregistration

Status: **PREREGISTERED TEMPLATE - no remote invocation has occurred**

This document covers one read-only execution of the repaired `RP1-B3.sh` only.
Writing it is not transport or execution authorization. The Lead performs any
later transport. The allocation token and numeric service identity are explicit
dispatch-time placeholders; the runner refuses execution while any placeholder
remains. Dispatch must bind them from the approved allocation and recorded host
inventory, update all dependent hashes, and re-freeze the package before any
host contact.

## 1. Run identifiers and evidence tree

The one-use unit is `WPLP2B-20260809T210610Z-834380c5`. Its one-use RUNID is
`WPLP2B-20260809T210610Z-834380c5-B3B`. A failed allocation burns the bound RUNID.

| Field | Preregistered value | Expected owner | Expected mode |
|---|---|---|---|
| `UNIT` | `WPLP2B-20260809T210610Z-834380c5` | - | safe component after binding |
| `RUNID` | `<unit>-B3B` | - | safe component after binding |
| `EV_STAGE_ID` | `b3b` | - | safe component |
| `REMOTE_BASE` | `/home/gatea/wpl_p2b_staging_<unit>` | `gatea:gatea` | `0700` |
| `EV_PARENT` | `<REMOTE_BASE>/evidence` | `gatea:gatea` | `0700` |
| `EV_RUNKIT` | `<REMOTE_BASE>/evidence/runkit` | `gatea:gatea` | `0700` |
| `REMOTE_KIT` | `<REMOTE_BASE>/kit` | `gatea:gatea` | `0700` |
| remote archive | `<REMOTE_BASE>/kit/runkit_b.tar` | - | - |
| `EXTRACT_DIR` | `<REMOTE_BASE>/kit/extracted` | `gatea:gatea` | directory `0700`, files `0444` |
| `EV_DIR` | `<EV_RUNKIT>/<unit>-B3B` | `gatea:gatea` | `0700` |
| `EV_LOG` | `<EV_DIR>/b3b.log` | - | create-once |
| operator record | `C:\WPI_ARTIFACTS\WPLP2B_TRANSPORT_<unit>` | local operator | create-once |

The `wpl_p2b_staging_` and `WPLP2B_TRANSPORT_` namespaces are distinct from
the existing `wpl_p2_staging_WPLP2-20260809T125940Z-8dc78f08` remote tree and
the two existing `WPLP2_TRANSPORT_` record roots.

## 2. Preregistered inputs consumed by the repaired block

| Variable | Value now | Binding rule |
|---|---|---|
| `B3_SWEEP_BUDGET_S` | `120` | Positive decimal seconds, per tree. Exceeding it is STOP. |
| `B3_SVC_UID` | `999` | Lead replaces it with the nonzero numeric service uid from the recorded host inventory before execution. |
| `B3_SVC_GID` | `999` | Lead replaces it with the nonzero numeric service gid from the recorded host inventory before execution. |

These are exactly the three inputs required by repaired `RP1-B3.sh`.
`B3_RELEASE_MANIFEST_SHA256` is deliberately absent because the repaired block
does not consume it. A wrong service uid or gid would create a false
`B3_FAIL reason=path=... owner_numeric=... expected=...` result. Therefore the
Lead must use the recorded numeric inventory, never an NSS name lookup or a
value derived during this check. Unresolved placeholders cause local refusal
before any process or connection starts.

## 3. Expected SHA-256 of every block carried

Archive: `../07_RUNKIT_B/runkit_b.tar`, 184320 bytes, 10 members, sha256
`888bec17cbea99a781368b7c3747d6a9085840005a686000bedaadcacb44246b`.

| Block | File | Lines | SHA-256 | Provenance | Execution |
|---|---|---:|---|---|---|
| RP0-LIB | `RP0-LIB.sh` | 370 | `4a404d7b90d83aef47b3593757f86e3699b3bc2dd772f51df63ead4f10d9ab48` | `accepted_blob` | sourced after hash gate |
| RP0-BOOTSTRAP | `RP0-BOOTSTRAP.sh` | 36 | `e7d748f6b41c6156de4d5c5e2d93c2b08729b1f85377b132660424024815bb33` | `accepted_blob` | sourced after hash gate |
| RP1-B3 | `RP1-B3.sh` | 662 | `6f3ea022b68d80a552c4ebcb771bbb2a707bdab46a383d605ffc5b88b884becc` | `repair_round6`; supersedes `f40411b053779b28ec9d970d7e5610fe5f363acbc48ee487d07ebce2638a69af` | executed |
| RP3-C2A-POST | `RP3-C2A-POST.sh` | 104 | `e233d29b005964e84cd6cbc2af50deccd83bb281dac39696e47de1c8890b5a27` | `accepted_blob` | not executed |
| RP3-C2B-POST | `RP3-C2B-POST.sh` | 74 | `26a1010cd9380289c5b90c08845b2af6ec31074fc5145241978a714b930bb412` | `accepted_blob` | not executed |
| RP4-C3 | `RP4-C3.py` | 295 | `0520cc901e56a66fe61e0df9edc0ed33fa4b05c09d62ba8f7471ef9ff688e4a5` | `accepted_blob` | not executed |
| RP5-C4A | `RP5-C4A.sh` | 374 | `a5b1b2e4d4e5227b3bb1f0ea31e9e547040231913445970efe1046f4eba9e0f2` | `accepted_blob` | not executed |
| RP5-C4B | `RP5-C4B.sh` | 249 | `10c4b3231042101ed9049dbf57ec3123ce902e9b18136769728a1a2e92f4037e` | `accepted_blob` | not executed |
| RP5-C4C | `RP5-C4C.sh` | 228 | `de7301f1deb752bcc63d818348c2fdc33372a6b7d7d4f377b62bdf27d313e3a8` | `accepted_blob` | not executed |
| RPD-VERIFY | `RPD-VERIFY.sh` | 775 | `3b9e78e87cecdc10ab1a10d14e79dbff530968e4075277117743c88976fa813c` | `repair_round6` | not executed; root-side design only |

The remote extractor hashes the archive before parsing any tar header, accepts
exactly these ten regular basenames in this order, extracts into a create-once
directory, makes each file `0444`, and verifies every digest. Only the three
files named as executed above are later sourced.

## 4. Support-script hashes

| File | Bytes | SHA-256 | Role |
|---|---:|---|---|
| `remote_setup_b3b.sh` | 3244 | `242b14ce848607ed1ae58a50d2effe03fcb13549867629578cf74d0e0a3b3866` | op 01 stdin, create-once allocation |
| `remote_extract_verify_b3b.sh` | 6155 | `68007732d8088f076575bd71a59e987e6f677602e272a4f36b19215e31d39750` | op 03 stdin, archive/member verification |
| `run_b3b.sh` | 2295 | `ae56c4a962ba28b1114b280823ae5c4661237c77085e67c443f780d6a7bd37b0` | op 04 stdin, repaired B3 wrapper |
| `remote_close_tree_b3b.sh` | 4305 | `5a9cfd5e8cec5960670fd46339f8fb15c355e2de23a34d878c0dc0e69cc50dcb` | op 05 stdin, closed-tree hash |
| `TRANSPORT_PLAN_B3B.tsv` | 3486 | `2f50feae6a91d519bf824208907dbc2ab6153729dd57e90ade9156fb72f99f4a` | exact seven-op plan pinned by runner |
| `transport_runner_b3b.ps1` | 14343 | `a94e91146b6c9091b38895f78d1379661b33ada5177176d9ede2da372ea39791` | local dry-run-first recorder |

The four new shell files preserve the accepted scripts' operational predicates
where applicable. Byte identity was not possible because this kickoff requires
ASCII-only deliverables and the accepted shell files contain non-ASCII comment
bytes. The B3B files use ASCII comments and preserve or narrow behavior as
described here; no host-facing capability was added.

## 5. Exact remote argv per operation

Route: `gatea@172.24.55.233`. Identity:
`C:\HyperV\GATEA-STAGING\ssh\gatea_ed25519`. Every ssh/scp operation carries,
in this order:

```
-i C:\HyperV\GATEA-STAGING\ssh\gatea_ed25519
-o BatchMode=yes -o StrictHostKeyChecking=yes -o IdentitiesOnly=yes -o ConnectTimeout=20
```

The exact current template argv is:

| op | run_when | exact argv after program name |
|---|---|---|
| 01 | `sequence_ok` | `ssh -i C:\HyperV\GATEA-STAGING\ssh\gatea_ed25519 -o BatchMode=yes -o StrictHostKeyChecking=yes -o IdentitiesOnly=yes -o ConnectTimeout=20 gatea@172.24.55.233 bash -s -- /home/gatea/wpl_p2b_staging_WPLP2B-20260809T210610Z-834380c5` |
| 02 | `sequence_ok` | `scp -i C:\HyperV\GATEA-STAGING\ssh\gatea_ed25519 -o BatchMode=yes -o StrictHostKeyChecking=yes -o IdentitiesOnly=yes -o ConnectTimeout=20 runkit_b.tar gatea@172.24.55.233:/home/gatea/wpl_p2b_staging_WPLP2B-20260809T210610Z-834380c5/kit/runkit_b.tar` |
| 03 | `sequence_ok` | `ssh -i C:\HyperV\GATEA-STAGING\ssh\gatea_ed25519 -o BatchMode=yes -o StrictHostKeyChecking=yes -o IdentitiesOnly=yes -o ConnectTimeout=20 gatea@172.24.55.233 bash -s -- /home/gatea/wpl_p2b_staging_WPLP2B-20260809T210610Z-834380c5/kit/runkit_b.tar /home/gatea/wpl_p2b_staging_WPLP2B-20260809T210610Z-834380c5/kit/extracted 888bec17cbea99a781368b7c3747d6a9085840005a686000bedaadcacb44246b` |
| 04 | `sequence_ok` | `ssh -i C:\HyperV\GATEA-STAGING\ssh\gatea_ed25519 -o BatchMode=yes -o StrictHostKeyChecking=yes -o IdentitiesOnly=yes -o ConnectTimeout=20 gatea@172.24.55.233 bash -s --` with `run_b3b.sh` on stdin |
| 05 | `always` | `ssh -i C:\HyperV\GATEA-STAGING\ssh\gatea_ed25519 -o BatchMode=yes -o StrictHostKeyChecking=yes -o IdentitiesOnly=yes -o ConnectTimeout=20 gatea@172.24.55.233 bash -s -- /home/gatea/wpl_p2b_staging_WPLP2B-20260809T210610Z-834380c5/evidence/runkit/WPLP2B-20260809T210610Z-834380c5-B3B WPLP2B-20260809T210610Z-834380c5-B3B` |
| 06 | `always` | `scp -i C:\HyperV\GATEA-STAGING\ssh\gatea_ed25519 -o BatchMode=yes -o StrictHostKeyChecking=yes -o IdentitiesOnly=yes -o ConnectTimeout=20 -r gatea@172.24.55.233:/home/gatea/wpl_p2b_staging_WPLP2B-20260809T210610Z-834380c5/evidence/runkit/WPLP2B-20260809T210610Z-834380c5-B3B .` |
| 07 | `always`, local | `local_bind 05 06 evidence\WPLP2B-20260809T210610Z-834380c5-B3B` |

Every `expect_rc` is 0. The first mismatch prevents later `sequence_ok` ops;
all `always` ops still run. The angle-bracket markers are not executable path
characters: the local runner refuses execution until dispatch replaces them
with one safe component and re-freezes the plan and all dependent pins.

## 6. Operator-side transport evidence contract

The record root is create-once. Before each executed or skipped op, the runner
creates `ops/<id>.argv`, `ops/<id>.stdout`, `ops/<id>.stderr`, and
`ops/<id>.rc`. It records the exact argv one element per line, complete and
separate stdout/stderr, and the actual rc or `skipped`. It also writes
`TRANSPORT_RECORD.txt` and `TRANSPORT_SHA256SUMS.txt` over the captured files.
No record root is created in dry-run mode.

Execution requires both `-Execute` and exactly
`-Confirm <unit>-B3B-EXECUTE`. The current token is deliberately unresolved,
and execution is refused locally before record creation or process start.

## 7. Closing and binding the evidence tree

Op 05 is a separate ssh invocation after op 04 has returned. It writes nothing
inside `EV_DIR`, permits only directories and regular files, hashes the file set
twice, refuses a changing set, and emits `CLOSE_DIGEST`, `CLOSE_SIZE`, and
`CLOSE_DIGEST_SET_SHA256` records on stdout. Op 06 retrieves the closed tree.
Op 07 independently hashes the local copy, compares names and digests both ways,
and reconstructs the exact remote digest-set rendering. Remote-only or
local-only hashing is not acceptance.

## 8. Preregistered expectations and predicted first divergence

The predicted result is `B3 PASS`, limited to the repaired block's explicit
`scope=unprivileged_only`. The table follows execution order. Text shown after
`reason=` is taken from the repaired block; values in angle brackets are the
runtime observations substituted into that exact reason shape.

| Check | Predicted arm | Exact predicted first divergence |
|---|---|---|
| sweep input | `120` accepted | `B3_STOP reason=input_missing name=B3_SWEEP_BUDGET_S detail=preregistered per-tree sweep budget in seconds, positive integer, never derived here`; `B3_STOP reason=input_charset name=B3_SWEEP_BUDGET_S expected=decimal_digits`; or `B3_STOP reason=input_range name=B3_SWEEP_BUDGET_S value=<value> expected=positive_integer` |
| numeric service uid/gid inputs | nonzero decimals from recorded inventory | `B3_STOP reason=input_missing name=B3_SVC_UID detail=preregistered numeric uid of the mtc-bridge service account, never derived here`; `B3_STOP reason=input_charset name=B3_SVC_UID expected=decimal_digits`; `B3_STOP reason=input_range name=B3_SVC_UID value=<value> expected=nonzero_service_account_uid`; and the same exact three shapes with `B3_SVC_GID`, `gid`, and `nonzero_service_account_gid` |
| unprivileged caller | nonzero uid | `B3_STOP reason=must_run_unprivileged uid=<uid>` |
| namespace record | both self namespace identities printable | `B3_STOP reason=namespace_unreadable ns=user path=/proc/self/ns/user`; `B3_STOP reason=namespace_unreadable ns=mnt path=/proc/self/ns/mnt`; `B3_STOP reason=namespace_identity_empty user=[<value>] mnt=[<value>]`; or `B3_STOP reason=namespace_identity_unprintable` |
| release root `/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b` | `0555`, numeric `0:0` | `B3_FAIL reason=path=<path> mode=<mode> expected=555`; or `B3_FAIL reason=path=<path> owner_numeric=<uid:gid> expected=0:0 owner_name=<name>` |
| release write-bit sweep | no non-link path with any `222` bit; within 120 s | `B3_FAIL reason=writable path inside immutable tree: <path>`; `B3_STOP reason=sweep_budget_exceeded root=<root> elapsed_s=<n> budget_s=120`; `B3_STOP reason=writable_inventory_failed root=<root> rc=<rc> detail=<detail>`; or `B3_STOP reason=writable_inventory_unparsable root=<root> rc=0 out=<detail>` |
| venv root `/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b` | `0555`, numeric `0:0` | same exact `path=... mode=...`, `owner_numeric=...`, writable-path, sweep-budget, and inventory reason shapes as the release root |
| state directory `/var/lib/mtc-bridge` | `0750`, numeric `<B3_SVC_UID>:<B3_SVC_GID>` | `B3_FAIL reason=path=/var/lib/mtc-bridge mode=<mode> expected=750`; or `B3_FAIL reason=path=/var/lib/mtc-bridge owner_numeric=<uid:gid> expected=<pinned-uid:pinned-gid> owner_name=<name>` |
| log directory `/var/log/mtc-bridge` | `0750`, same numeric service owner | same exact mode/owner reason shapes with `path=/var/log/mtc-bridge` |
| config directory `/etc/mtc-bridge` | directory, `0750`, numeric `0:0` | `B3_FAIL reason=missing path=/etc/mtc-bridge`; `B3_FAIL reason=canonical deployment path is a symlink kind=<link_live-or-link_dangling> path=/etc/mtc-bridge`; `B3_FAIL reason=unexpected object kind=<kind> path=/etc/mtc-bridge`; `B3_FAIL reason=path=/etc/mtc-bridge mode=<mode> expected=750`; or the exact numeric-owner shape |
| first-start unit file | regular, `0644`, numeric `0:0` | the same exact `missing`, `canonical deployment path is a symlink`, `unexpected object kind`, mode, or numeric-owner shapes with `path=/usr/local/lib/systemd/system/mtc-bridge-first-start.service` and `expected=644` / `expected=0:0` |
| config canonicality | literal `/etc/mtc-bridge` | `B3_FAIL reason=conf_dir_kind=<kind> path=/etc/mtc-bridge expected=dir`; `B3_STOP reason=canonicalization_failed path=/etc/mtc-bridge`; or `B3_FAIL reason=conf_dir_not_literal_canonical path=/etc/mtc-bridge canonical=<path>` |
| mount boundary | none at or under config dir | `B3_STOP reason=mounts_unreadable path=/proc/self/mounts`; `B3_STOP reason=mount_table_read_error path=/proc/self/mounts records=0 read_rc=<rc> detail=nonzero_read_populated_no_field_and_consumed_no_record`; `B3_STOP reason=mount_record_malformed path=/proc/self/mounts record=<n> expected_fields=6 got=[<fields>]`; `B3_STOP reason=mount_table_unterminated_final_record path=/proc/self/mounts records=<n> hits=<n> first_target=<target>`; or `B3_STOP reason=mount_boundary_at_or_under_conf_dir path=/etc/mtc-bridge mounts=<n> first_target=<target>` |
| caller group | caller not in config directory gid | `B3_STOP reason=caller_in_conf_dir_group path=/etc/mtc-bridge gid=<gid> caller_gids=[<gids>]` |
| access builtins | config search and read denied | `B3_FAIL reason=conf_dir_search_permitted path=/etc/mtc-bridge mechanism=access_builtin_x expected=denied`; or `B3_FAIL reason=conf_dir_read_permitted path=/etc/mtc-bridge mechanism=access_builtin_r expected=denied` |
| env boundary EACCES arm | `B3_conf_dir_opaque_to_operator path=/etc/mtc-bridge/mtc-bridge.env outcome=EACCES rc=1 mechanism=message_lc_all_c_exact_shape` | A visible env file is FAIL: `B3_FAIL reason=conf_dir_entry_permitted path=/etc/mtc-bridge/mtc-bridge.env stat=[<stat>] expected=EACCES` |
| env boundary ENOENT arm | not expected; search must not reach the name | `B3_FAIL reason=conf_dir_search_permitted_name_absent path=/etc/mtc-bridge/mtc-bridge.env rc=1 expected=EACCES` |
| env boundary multiline arm | not expected | `B3_STOP reason=boundary_diagnostic_multiline path=/etc/mtc-bridge/mtc-bridge.env rc=<rc> detail=<sanitized-detail>` |
| env boundary ambiguous arm | not expected | `B3_STOP reason=boundary_diagnostic_ambiguous path=/etc/mtc-bridge/mtc-bridge.env rc=<rc> classes=<n> eacces=<n> enoent=<n> detail=<detail>` |
| env boundary unclassified arm | not expected | `B3_STOP reason=boundary_probe_unclassified path=/etc/mtc-bridge/mtc-bridge.env rc=<rc> detail=<detail>` |
| absent-name falsification | exact EACCES PASS arm for `/etc/mtc-bridge/.b3-boundary-probe-absent-name` | the same `conf_dir_entry_permitted`, `conf_dir_search_permitted_name_absent`, `boundary_diagnostic_multiline`, `boundary_diagnostic_ambiguous`, or `boundary_probe_unclassified` reason with this exact path |
| deferred env metadata check | emits exactly `B3_deferred check=env_file_mode_owner path=/etc/mtc-bridge/mtc-bridge.env to=RPD-VERIFY reason=conf_dir_not_searchable_unprivileged` | missing or changed line means the pinned block bytes did not execute; wrapper hash gate must first STOP |
| deferred manifest metadata check | emits exactly `B3_deferred check=install_manifest_mode_owner path=/etc/mtc-bridge/install_manifest.json to=RPD-VERIFY reason=conf_dir_not_searchable_unprivileged` | missing or changed line means the pinned block bytes did not execute; wrapper hash gate must first STOP |
| deferred manifest binding check | emits exactly `B3_deferred check=install_manifest_binding path=/etc/mtc-bridge/install_manifest.json to=RPD-VERIFY reason=conf_dir_not_readable_unprivileged` | missing or changed line means the pinned block bytes did not execute; wrapper hash gate must first STOP |

Any B3 FAIL is deviant observed host state and requires Lead adjudication. Any
B3 STOP is could-not-evaluate and is never re-read as PASS. The three deferred
lines are disclosure, not execution of the deferred checks.

## 9. What is deliberately NOT preregistered

- No C1, C2, C3, C4, or C5 execution. Their blockers remain outside this check.
- No RPD-VERIFY execution. It is root/deploy-channel design only. This route has
  no root, sudo, or privilege-escalation authority.
- No env-file mode/owner, install-manifest mode/owner, or install-manifest
  binding claim. Repaired B3 defers all three to RPD-VERIFY.
- No service stop/start/enable/disable/mask/unmask, reboot, rollback, unit write,
  or chmod/chown outside this run's create-once tree.
- No credential read, ARM, orders, broker/exchange, TESTNET/mainnet, economic
  action, master merge, deployment, or Git mutation.

## 10. Disposition of the accepted operator artifacts

| Accepted artifact | B3B disposition |
|---|---|
| `remote_setup.sh` | Adapted only for the new `/home/gatea/wpl_p2b_staging_` namespace, B3B name, and ASCII comments; create-once logic retained. |
| `remote_extract_verify.sh` | Adapted for 184320 bytes, the new archive digest, exactly ten members, repaired RP1-B3, and RPD-VERIFY; it still executes no block. |
| `run_b3.sh` | Adapted to the new unit/RUNID, repaired B3 digest, and exactly the repaired input set. Symlink refusal and immediate pre-source hashes retained. |
| `remote_close_tree.sh` | Operational predicates retained; filename/header and non-ASCII comments normalized for the B3B ASCII-only deliverable. |
| `TRANSPORT_PLAN.tsv` | Reduced to the seven operations required for one B3B check; every rc remains 0 and closing/fetch/bind remain `always`. |
| `transport_runner.ps1` | Adapted to the new plan/archive/record namespace and confirm token; adds explicit per-op `.rc` files and refuses unresolved placeholders before execution. |

## 11. Immutability and void rules

The current artifact set is an immutable non-executable preregistration
template. Dispatch creates a final frozen instance by replacing the unit token
everywhere and the uid/gid tokens in `run_b3b.sh`, then recalculating the
support hashes, plan stdin hashes, plan hash, runner plan pin, preregistration
tables, and checksum manifest. No partial substitution is allowed.

After that final freeze, any change to a block/archive/support hash, unit,
RUNID, stage id, remote/local path, route, identity, ssh option, sweep budget,
numeric service identity, plan row, confirm token, or expected rc voids the
preregistration. A failed allocation burns the bound RUNID. No retry identifier
is preregistered.

## 12. Safety state at the moment of writing

- SSH/SCP/remote invocation count: 0.
- Staging host contact: none; no socket or remote process was opened.
- Runner use: dry-run only; it printed the seven-op plan and exited 0.
- B3, RPD-VERIFY, C1, C2, C3, C4, and C5 executions: none.
- Service, unit, reboot, rollback, credential, ARM, order, broker/exchange,
  TESTNET/mainnet, deployment, and economic actions: none.
- Git add/commit/push/checkout/reset/stash/branch/worktree actions: none.
- Repository writes: only this `08_PREREG_B3B` directory.
- Archive and all ten in-archive block digests were re-verified locally without
  extraction to disk. Syntax checks and exact outputs are recorded in
  `SELF_QA_B3B.md`.
