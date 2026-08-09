# WP-L P2 proposal repair — frozen candidate anchor map (2026-08-09)

## 0. Status and authority

Lead-owned read-only evidence map for future verification of the one-file proposal repair. It does not
edit candidate source, execute proposed scripts, contact a host, or accept the rejected proposal.

Exact candidate: `2ce41e34bceb599d80af24c5c33d835820ec321b`.

| Candidate path | Git blob |
|---|---|
| `IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py` | `26c077e650ab88ba2086efa3a80790769bc055b1` |
| `IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh` | `db11010a24edfbb96ba80ec1fbe1db3ff29193c9` |
| `IBKR_PAPER_BRIDGE/deploy/linux/verify.sh` | `5cfefd709202ff504ae7b7fc3504b8c0b00900b6` |
| `IBKR_PAPER_BRIDGE/deploy/linux/rollback.sh` | `4b36674dcb1baa7c3b119cac98f8e6017b1f1566` |
| `IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template` | `c18232549d96aa200d8c7f796e64de743288940c` |

All lines below are candidate-qualified, not live-branch line claims.

## 1. `wal_state_bundle.py`

- `:212-213` — canonical JSON is `json.dumps(..., sort_keys=True, separators=(",", ":"))`.
- `:342-381` — `_connect_readonly(path)` uses a `mode=ro` URI and returns `sqlite3.Connection`.
- `:405-411` — candidate integrity and FK helpers operate on a connection.
- `:417` — public `collect_invariants(conn: sqlite3.Connection)`; passing a string/path is invalid.
- `:561-562` — public `invariants_hash(invariants)` hashes candidate canonical JSON.
- `:568-569` — bundle sidecar paths derive from the forbidden suffix set.
- `:780-795` — source capture runs integrity/FK and collects source invariants before writing output.
- `:797-806` — candidate consistent-copy primitive is exactly `src.backup(dst)` with SQLite destination.
- `:814-827` — candidate rejects bundle sidecars, then runs integrity/FK and collects bundle invariants.

Proposal implications: C3 must use connections, SQLite backup, candidate invariant canonicalization,
protected-field equality, sidecar/identity checks, and preserved failure evidence. A path argument,
file-copy substitute, or custom JSON hash is not candidate fidelity.

## 2. `deploy/linux/lib/common.sh`

- `:41-48` — mutating candidate commands pass through `run()`; `MTC_DRY_RUN=1` prints and returns without
  executing the command.
- `:95-105` — `assert_no_writable_paths`; exact predicate is
  `find "$root" ! -type l -perm /222 -print -quit`, and `find` failure is a candidate failure.

The old checklist pointer `deploy/linux/common.sh` is absent at the candidate. The exact path includes
`lib/`; this was independently reproduced during checklist audit round 1.

## 3. `deploy/linux/verify.sh`

- `:79-81` — release root requires exact `0555 root:root`, `/222` scan, and exact payload tree.
- `:82-98` — release manifest file hash, payload `sha256sum`, and exact release marker are separate checks.
- `:105-106` — venv root requires exact `0555 root:root` and `/222` scan.
- `:124-128` — exact state/log/config/env/install-manifest modes and owners.
- `:129-135` — install manifest must bind both candidate release SHA and release/payload manifest SHA.
- `:138-146` — candidate fails if env file defines `HL_LIVE_ACK` or `MTC_BRIDGE_START_MODE`.
- `:155-205` — installed unit path/content, exact release and venv bindings, and unit contract checks.

Proposal implications: B3 cannot call a full post-start `verify.sh`, but its bounded substitute must not
weaken these relevant predicates or collapse read/tool errors into PASS.

## 4. `deploy/linux/rollback.sh`

- `:42-52` — parses paired rebind arguments, required state-manifest arguments, and `--dry-run`.
- `:57-68` — state manifest/hash required; rebind SHA arguments must be supplied together when either is
  present.
- `:70-78` — rollback-manifest guard calls `assert_not_symlink` only; it does not reject an existing
  regular file. Steady unit presence is rejected.
- `:79-101` — stop/mask behavior and candidate post-stop local checks; dry-run goes through `run()`.
- `:113-116` — `UNIT_SHA` is populated from the currently installed first-start unit when present,
  independently of the later rebind branch.
- `:148-155` — rebind-only unit installation/daemon-reload/mask path.
- `:157-180` — when not dry-run, rollback manifest is unconditionally written with `cat >`, then
  `root:root` and `0640`. In no-rebind mode, `rollback_release_sha` and
  `rollback_release_manifest_sha256` are empty; `first_start_unit_sha256` equals the installed unit hash
  when present and is empty only when that unit file is absent.

Proposal implications: C4 must prove manifest object-and-link absence immediately before use, validate a
mutation-free dry run, invoke candidate rollback once without rebind arguments, require the two empty
target-release fields plus the exact preregistered installed-unit hash/absence result, and prove protected
invariant equality. The candidate's symlink-only guard does not supply regular-file no-clobber protection.

Stop/mask at `:79-86` is unconditional. A no-rebind invocation deliberately omits both target SHA
arguments, so the additional rebind install/daemon-reload/remask branch at `:117-155` is skipped.

## 5. First-start unit template

- blob has 93 lines and no actual `^[Install]$` section; comment `:11-12` states enable is structurally
  unavailable.
- `:29-45` — exact service identity/path, credential-free DISARMED start mode, and env file.
- `:47-55` — `KillSignal=SIGTERM`, `KillMode=mixed`, `TimeoutStopSec=45`, `FinalKillSignal=SIGKILL`,
  `Restart=no`.
- `:63-93` — sandbox and writable-surface restrictions.

Proposal implications: C1 cannot pin a successful shutdown tuple from these directives alone; the exact
locked runtime/systemd result remains an open prerequisite. C2-A expects a preregistered unmasked/static
post-reboot branch because there is no `[Install]` section, while C2-B requires exact mask persistence.

## 6. Lead verification commands

Read only; substitute no branch alias for the candidate SHA:

```powershell
git ls-tree 2ce41e34 -- <exact-candidate-path>
git show 2ce41e34:<exact-candidate-path>
git cat-file -e 2ce41e34:<exact-candidate-path>
```

Line claims must be re-derived from the candidate object if any future source claim expands beyond this
map. A live-branch match is not candidate evidence.

## 7. Next steps

1. Do not dispatch until the repaired package commit has fresh `claude-opus-5` xhigh and
   `gpt-5.6-sol` xhigh accepting verdicts plus no unresolved Lead-reproduced required finding from any
   canonical auditor.
2. Freeze the resulting one-file proposal commit.
3. Use this map plus the repaired checklist from that same accepted package commit. Historical checklist
   `456968bb` is superseded and MUST NOT be used.
4. Preserve genuine local RED/GREEN commands and outputs; text assertions are not D026 evidence.
5. No host/script transfer/trading/deployment authority follows from this map.
