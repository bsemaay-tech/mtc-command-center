# FINAL T0 round-3 Codex verdict — Plan V5 + launcher v3 + candidate `a7460784`

| Field | Value |
|---|---|
| Model identity reported by runtime/route | **OpenAI Codex `gpt-5.6-sol`** |
| Effort | **xhigh** |
| Audit slot | **T0 Codex flagship slot, round 3 (FINAL) of the un-reset Plan-V3 cap** |
| Session | **Fresh, independent, adversarial; no sub-delegation** |
| Working directory | `C:\AUD62C` |
| Start (UTC+3) | **2026-08-16 15:10:20 +03:00** |
| Stop (UTC+3) | **2026-08-16 15:25:42 +03:00** |
| **VERDICT** | **REQUEST_CHANGES — 8 REQUIRED, 0 NIT** |

## Execution boundary

Read-only everywhere except this verdict and disposable scratch under
`C:\tmp\codex_t0_v5_20260816_1510` plus `/tmp/codex-cron-metadata.QKWi6D`.
I did not execute the launcher, installer, verifier, rollback script, service,
firewall, or any host-side plan command; did not contact KVM2 or any other host;
did not open any SSH connection; did not read an identity key; did not mutate
Git state; and did not sub-delegate. The sole SSH invocation was local
configuration evaluation with `ssh -G` against
`t0-v5-placeholder.invalid`, which opens no connection.

## Subject pins — start and end

All three subjects matched their required pins at both observations.

| Subject | Start | End |
|---|---|---|
| Plan V5: `C:\R7FINAL\MTC_COMMAND_CENTER\11_TRIAGE\KVM2_DEPLOYMENT_PLAN_V5_2026-08-16.md` | 9785 B; SHA-256 `269da78155a233d23f290f5a07a13647495d065e45dd947cb4cd2be68ecc30a4` | identical |
| Launcher v3: `C:\R7FINAL\MTC_COMMAND_CENTER\11_TRIAGE\KVM2_RUNKIT\Open-BridgeDashboard.ps1` | 8651 B; SHA-256 `533f29db75ebfa12d1bb1ecbe7f40d241d94364c4f41d74d293268b0f053adca` | identical |
| Candidate in `C:\AUD62C` | HEAD `a7460784c1563c140ee7c75197aeab2b0170da8a`; parent `be68953787c299bdaf30f83f301aa66a8ec0ea1f`; tree `d14d3d372c74a73fc2dc804e50472013d56e1844`; local and `origin/` integration refs at HEAD; clean | identical; clean |

The payload identity cited by the plan also exists locally: release marker
`a7460784c1563c140ee7c75197aeab2b0170da8a` and
`RELEASE_SHA256SUMS` SHA-256
`2581ed3fbb020c03bb4e0dc41f35d60a54ee949d892164c705a34050abd9b8c0`.

## REQUIRED findings

### REQUIRED-1 — two rebuilt D026 arms still accept new equivalent defects

The exact round-2 mutations are now RED, but the rebuilt tests are still
denylist/self-confirming checks rather than evidence of their broad claims.
I copied the candidate outside the repository, confirmed each new mutation was
present, and ran the named real arm:

| Rebuilt arm | New independent mutation | Real result |
|---|---|---|
| Complete dry-run mutation manifest (`tests/test_linux_deployment.py:217-250`) | Added the direct mutating command `install -d -o root -g root -m 0755 /opt/codex-unlisted-direct`, without `run`/`run_action` or a manifest row | **1 passed**, rc 0 |
| Read-only verifier (`tests/test_linux_deployment.py:879-915`) | Added `python3.12 -c '...Path("/tmp/codex-verifier-python").write_text("mutation")'` to `verify.sh` | **1 passed**, rc 0 |

The dry-run arm only inventories `run_action` and rejects raw calls spelled
`run ...`; it never proves that every mutating statement is routed through
that wrapper. The verifier arm recognizes a finite list of shell writes and
redirections but cannot adjudicate a child interpreter's filesystem effect.
Both mutations preserve the named defects: an unlisted host mutation and a
persistent verifier write. Under D026 these arms remain supplemental, not
closure evidence. Codex round-2 R6 is **NOT CLOSED**. Repair the mechanism so
unclassified executable/mutating forms STOP, then record these two REDs and
final GREEN output.

### REQUIRED-2 — the UFW parser exempts an application profile it cannot prove safe

`IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh:174-178` says application-profile
grammar must fail closed, but `:234-236` special-cases the name `OpenSSH` as an
SSH-only rule without reading or binding that profile's port definition. The
test at `tests/test_linux_deployment.py:313-316` codifies that exception.

Against the real candidate function, the exact destination-address rule,
`8000:9000/tcp`, `8790:8800/tcp`, and `Nginx Full` fixtures all returned rc 1.
But this unexpanded profile row returned rc 0:

```text
OpenSSH ALLOW IN Anywhere
80/tcp ALLOW IN Anywhere
443/tcp ALLOW IN Anywhere
PASS  ufw active, default-deny incoming; SSH port 22 allowed; Bridge port 8790 not exposed
RC=0
```

A status row containing only a profile name carries no evidence that the
profile currently expands only to port 22; a changed profile can therefore
make the printed 8790 conclusion false. This contradicts both the code comment
and Plan V5's claim that application-profile grammar STOPs. Reject every named
profile, or independently parse and pin the effective `OpenSSH` definition
before admitting it. Codex round-2 R1 and Claude round-2 R1 are only
**PARTIALLY CLOSED**.

### REQUIRED-3 — the verifier admits unsafe metadata on root-executed logrotate assets

`verify.sh:235-246` checks only bytes for `/etc/logrotate.d/mtc-bridge` and only
`-x` plus bytes for `/etc/cron.hourly/mtc-bridge-logrotate`. It never calls
`assert_mode_owner` for either file. I copied the accepted cron bytes to
scratch, set mode `0777` and owner `1000:1000`, and ran the delivered predicate;
`-x && cmp -s` returned rc 0.

The cron file is executed as root, and the logrotate policy is consumed by a
root process. Byte-identical but service-user/world-writable files are a
root-code-execution trust hole that the verifier reports as an exact match.
Require regular non-symlink files with exact numeric root ownership and exact
modes (`0644` policy, `0755` runner) before comparing bytes, and add a RED
metadata fixture.

### REQUIRED-4 — launcher v3's literal fingerprint can be supplied by a wrong key's comment

The identity-key file read is removed, the PowerShell AST has zero errors, and
the v2 SSH isolation option set still parses locally. However,
`Open-BridgeDashboard.ps1:57-62` extracts every `SHA256:`-looking substring
from each entire `ssh-add -l` line; `:129-131` then uses `-contains`.

I applied that exact parser to a syntactically representative agent line whose
real fingerprint was different and whose comment contained the pinned literal:

```text
256 SHA256:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA wrong-key-comment-SHA256:8b6bl/srDevzQ1rycf9FcQFgZXblSMddqak/9JsHBC8 (ED25519)
```

The parser returned both tokens and `-contains` accepted the expected literal.
Thus the intended agent key is not actually enforced. Parse only the dedicated
second whitespace-delimited fingerprint field under a complete accepted
`ssh-add -l -E sha256` grammar, rejecting malformed rows. Codex round-2 R7 is
**PARTIALLY CLOSED**: no identity-key file is read, but the replacement trust
mechanism has a reproducible false pass.

### REQUIRED-5 — V5's “exact executable command set” contains incomplete and unsafe commands

Plan V5 `:3-8` says every executable command is restated in this file. The
actual command block does not satisfy that claim:

- `:30-31` gives `scp` with only two trust options, then a bare
  `ssh baris@152.239.123.231` followed by the prose comment “same pinned
  options”. Neither command carries the launcher's isolated `-F NUL`, null
  identity/global-trust paths, disabled proxy routes, or password/keyboard
  refusals. Ambient SSH configuration can therefore change the route and
  authentication surface.
- `:60` and `:77` put the Unicode ellipsis `a7460784…` in executable paths;
  those literal paths do not name the installed release.
- Stage-3 items 3-5 (`:86-93`) name backup, monitoring, and re-inventory work
  but provide no reviewed commands or failure adjudication.

This is the same command-fidelity class as Codex round-2 R2: the old pins are
gone, but the operator still has to invent/substitute security-sensitive
commands. Restate literal, complete `scp`/`ssh` commands with the isolated
option set, full 40-hex release paths, and exact stage-3 commands with rc/stderr
STOP rules. Codex round-2 R2 is **NOT CLOSED**.

### REQUIRED-6 — the reordered rollback rehearsal still has no executable initial-state branch

The ordering is repaired, but Plan V5 `:56-80` cannot run on the state produced
by stages 1-2:

- `install.sh` creates `/var/lib/mtc-bridge` but never initializes
  `bridge.db`; the service remains masked and never started.
- `wal_state_bundle.py create` requires an existing regular `--source` and
  raises `source database not found` otherwise
  (`tools/wal_state_bundle.py:679-687`).
- Plan `:67-71` nevertheless says the installer creates an initialized DB.
  Its fallback then says the input is the tar's SHA while `rollback.sh` is
  exercised with “the manifest the installer wrote”; those are different
  files and hashes, and no literal fallback command is supplied.
- The only rollback command (`:77-79`) still passes the nonexistent
  `bridge-state-manifest/bundle_manifest.json`.

The operator would discover the missing required input inside the one bounded
attempt. Define one deterministic branch for the actual never-started empty
state (exact artifact creation, exact file/hash handoff, exact rollback
command), and separately define the existing-DB branch if it is genuinely
reachable. Codex round-2 R4 and Claude round-2 R3 are **NOT CLOSED**.

### REQUIRED-7 — §3 still permits self-confirming “zero side effects” evidence

Plan V5 `:105-124` names better instruments, but not an executable,
fail-closed evidence contract:

- The persistence leg supplies no exact SQLite query, URI, snapshot/hash
  commands, expected table identity, absent-WAL treatment, or rule that rc and
  stderr are adjudicated before equality. Empty/unread output is not separated
  from a real zero/equal observation.
- The network leg contains the shell metasyntax placeholder
  `<mtc-bridge uid>` and no exact commands for rule installation, activation
  proof, window delimiters, event extraction/attribution, loss-counter checks,
  query-error adjudication, or rule removal. An empty audit query or dropped
  audit records can therefore be read as “zero connects”. Proving that a rule
  appears active is not proof that the whole window was captured without loss.

Under the repository's self-confirming test, each leg needs an observation that
distinguishes genuine zero/equality from inability or incomplete capture.
Provide literal commands; capture stdout/stderr/rc before comparison; STOP on
missing DB/table/tool/WAL state that is not explicitly modeled; bind the audit
rule to the resolved numeric UID; prove the exact rule, audit daemon/query, and
zero lost records across the delimited window; attribute every result; and
remove the exact rule afterward. Codex round-2 R3 is **NOT CLOSED**.

### REQUIRED-8 — the authorization/removal boundary is not self-contained and omits the new cron asset

The §4 owner sentence (`:128-143`) still delegates the filesystem scope to
“the V2 §0 Bridge tenancy boundary” instead of naming it, despite the round-3
contract requiring a self-contained sentence. More concretely, the
partial-install disposition at `:95-99` says V2 §7 “now includes”
`/etc/cron.hourly/mtc-bridge-logrotate`. The incorporated V2 §7 does not: it
lists the old `~/payload-62bf661b` and ends its service assets at
`/etc/logrotate.d/mtc-bridge`.

No exact rollback/removal enumeration in V5 removes the new cron runner or the
current `~/payload-a7460784`; the audit rule/package disposition also has no
literal cleanup command. Therefore “restore the clean baseline” is not an
executable or exact boundary. Restate inside V5 the complete allowed tenancy
objects and the exact removal list/commands, including the cron runner, current
payload, audit rule, and recorded package disposition; then put that complete
scope in the §4 sentence itself.

## Exact round-2 attack replay and closure map

The exact recorded D026 attacks produced the required RED results:

| Recorded attack | Real candidate result |
|---|---|
| Frozen `2020-01-01` `status_ts` | 1 failed, rc 1 |
| Raw unlisted `run install ... /opt/hermes` | 1 failed, rc 1 |
| `printf ... > /tmp/codex-verifier-mutation` | 1 failed, rc 1 |
| Commented-out `MemoryHigh`/`MemoryMax` | 1 failed, rc 1 |

Per-finding closure after the fresh attacks:

| Round-2 finding | Closure |
|---|---|
| Codex R1 — UFW destination/range grammar | **PARTIALLY CLOSED** — exact fixtures reject; `OpenSSH` profile exception false-passes (REQUIRED-2). |
| Codex R2 — exact command restatement | **NOT CLOSED** — incomplete/ambient SSH commands and ellipsis paths remain (REQUIRED-5). |
| Codex R3 — independent side-effect evidence | **NOT CLOSED** — §3 is not executable or fail-closed against empty/lost evidence (REQUIRED-7). |
| Codex R4 — rehearsal inputs/order | **NOT CLOSED** — order fixed, actual never-started input branch cannot run (REQUIRED-6). |
| Codex R5 — log/disk honesty | **CLOSED on the named claim** — policy now calls 1 GiB nominal and worst case unbounded; fresh cron metadata defect is REQUIRED-3. |
| Codex R6 — non-falsifying regressions | **NOT CLOSED** — exact attacks RED, two new equivalent mutations GREEN (REQUIRED-1). |
| Codex R7 — identity-key file read | **PARTIALLY CLOSED** — file read removed; comment-spoofed fingerprint passes (REQUIRED-4). |
| Claude R1 — UFW destination/range false passes | **PARTIALLY CLOSED** — exact fixtures reject; profile exception remains (REQUIRED-2). |
| Claude R2 — frozen timestamp accepted | **CLOSED** — strict order plus bounded clock freshness; exact 2020 mutation RED. |
| Claude R3 — rollback prerequisite/order | **NOT CLOSED** — REQUIRED-6. |

## Candidate delta scope

`be689537..a7460784` is exactly the claimed eight files:

```text
M IBKR_PAPER_BRIDGE/deploy/linux/README.md
A IBKR_PAPER_BRIDGE/deploy/linux/cron/mtc-bridge-logrotate
M IBKR_PAPER_BRIDGE/deploy/linux/install.sh
M IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh
M IBKR_PAPER_BRIDGE/deploy/linux/logrotate/mtc-bridge
M IBKR_PAPER_BRIDGE/deploy/linux/verify.sh
M IBKR_PAPER_BRIDGE/tests/test_api.py
M IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py
```

Stat: **8 files, 301 insertions, 107 deletions**. `git diff --check` returned
0. `bridge/engine`, `bridge/store`, and `bridge/broker` tree OIDs are identical
at base and head; no `bridge/`, config, app, Pine, parity, MTC, schema, backtest,
strategy, broker, order, risk, store, or product-code byte changed. Scope:
**PASS**.

## Full suite — independently executed

Command from `C:\AUD62C`:

```powershell
$env:PYTHONUTF8='1'; $env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest -q -p no:cacheprovider IBKR_PAPER_BRIDGE/tests
```

Real final line:

```text
1373 passed, 1 warning in 165.63s (0:02:45)
```

Exit code 0. The warning is the existing Starlette/httpx deprecation warning.
HEAD remained `a7460784...` and `git status --porcelain` remained empty after
the run and at the end pin. Changed shell files and `rollback.sh` also returned
0 under `bash -n`; launcher AST errors = 0. Suite execution requirement:
**MET**.

## Launcher preservation check

No identity-key file reference, public-key file, `ssh-keygen -lf`, or private
key read remains. Local `ssh -G` with a `.invalid` placeholder parsed rc 0 and
showed `identityfile NUL`, `globalknownhostsfile NUL`, the named user trust
store, strict host checking, password/keyboard refusal, batch mode, and the
10-second timeout. The EAP-safe native wrapper, distinct agent rc branches,
known-host lookup, child readiness checks, and `try/finally` cleanup are still
present. REQUIRED-4 is the surviving trust hole.

## Final acceptance statement

**REQUEST_CHANGES — 8 REQUIRED, 0 NIT.** This is the final round of the
Plan-V3 T0 cap. The suite and delta-scope gates pass, and several exact prior
attacks are repaired, but the package still has reproduced trust, D026,
root-execution metadata, command-fidelity, rollback-input, evidence, and owner-
scope failures. The cap is exhausted without an accepting Codex verdict.
Do not run the launcher, do not contact KVM2, and do not present §4 as an
installation-authorization sentence on these bytes; return the package to the
owner unaccepted.

## NIT findings

None.
