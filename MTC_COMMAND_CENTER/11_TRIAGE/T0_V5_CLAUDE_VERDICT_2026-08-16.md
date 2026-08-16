# T0 round-3 (FINAL) verdict — plan V5 + launcher v3 + final candidate `a7460784` — Claude slot

| Field | Value |
|---|---|
| Reviewer slot | Claude (one of two independent T0 flagships), **round 3 — the final round of the un-reset Plan-V3 T0 cap (3)** |
| Model identity (runtime-reported) | `claude-opus-5` — "Opus 5", Claude 5 family |
| Effort | `xhigh` as configured by the dispatching route. **In-session introspection of the effort setting is not possible**; I applied no lower-effort override. Same caveat of record as rounds 1 and 2. |
| Session | Fresh, independent, adversarial; no state carried from my round-1 or round-2 sessions beyond the two published verdicts I was told to verify |
| Working directory | `C:\AUD62C` |
| Start (UTC+3) | 2026-08-16 15:10:07 |
| Stop (UTC+3) | 2026-08-16 15:25:58 |
| **VERDICT** | **REQUEST_CHANGES — 2 REQUIRED, 14 NIT** |

## Subject pins — start and end

| # | Subject | Expected | Start | End |
|---|---|---|---|---|
| 1 | `KVM2_DEPLOYMENT_PLAN_V5_2026-08-16.md` | 9785 B / `269da781…be8ecc30a4` | 9785 B / `269da78155a233d23f290f5a07a13647495d065e45dd947cb4cd2be68ecc30a4` ✅ | identical ✅ |
| 2 | `KVM2_RUNKIT/Open-BridgeDashboard.ps1` | 8651 B / `533f29db…f0b8053adca` | 8651 B / `533f29db75ebfa12d1bb1ecbe7f40d241d94364c4f41d74d293268b0f053adca` ✅ | identical ✅ |
| 3 | Candidate commit | `a7460784…` | HEAD `a7460784c1563c140ee7c75197aeab2b0170da8a`, parent `be68953787c299bdaf30f83f301aa66a8ec0ea1f` ✅, tree `d14d3d372c74a73fc2dc804e50472013d56e1844`, tip of `integration/bridge-release-20260815`, `git status --porcelain` empty ✅ | identical, still clean ✅ |

All three pins matched at start and at end. **No STOP condition occurred.**

The pinned launcher is byte-identical to the implementer's produced artifact:
`C:\tmp\lane_out\Open-BridgeDashboard_v3.ps1` and
`…\KVM2_RUNKIT\Open-BridgeDashboard.ps1` both hash `533f29db…053adca`.

### Exclusions honoured

Read-only everywhere except this file plus disposable scratch **outside any repo**
(`…\scratchpad\{ufw,d026,wal,arch}`). **No launcher execution, no ssh invocation of
any kind (not even non-connecting `ssh -G` — this round's brief excludes ssh
outright, which is stricter than round 2's), no host or network contact, no git
mutation anywhere, no identity-key read, no sub-delegation.**
`C:\LAB\Tradingview_LAB_CLEAN` untouched; `C:\R7FINAL` read only. The repository
worktree was clean at start, after the full suite, and at the final pin.

Because I did not run `ssh -G` this round, the option-set soundness of the launcher
is established by (a) line-by-line inspection and (b) the fact that the v2→v3 diff
does not touch the option array at all, so the two independent round-2 `ssh -G`
parses of the identical array still apply. I state that as inherited evidence, not
as something I re-measured.

---

## Required check 3 — full suite, executed by me

```
PYTHONUTF8=1 PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider IBKR_PAPER_BRIDGE/tests
```

run from `C:\AUD62C` at HEAD `a7460784`. Exact final line:

```
1373 passed, 1 warning in 168.42s (0:02:48)
```

Exit code 0. The one warning is the existing Starlette/httpx deprecation warning.
**Required `1373 passed, 1 warning` — MET.** `git status --porcelain` empty
immediately afterward; HEAD unchanged. **The run mutated nothing.**
(Fourth independent timing: implementer 176.91 s, Lead 186.88 s, this run 168.42 s.)

## Required check 2 — candidate delta scope `be689537..a7460784`

`git diff --stat` = **exactly the 8 claimed files, +301/−107**, matching Plan V5 `:18`
and `RIC2_REPAIR_REPORT_2026-08-16.md:227-241`:

```
 IBKR_PAPER_BRIDGE/deploy/linux/README.md           |  15 ++-
 .../deploy/linux/cron/mtc-bridge-logrotate         |   9 ++
 IBKR_PAPER_BRIDGE/deploy/linux/install.sh          |  88 +++++++-----
 IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh       | 103 +++++++++++++-
 .../deploy/linux/logrotate/mtc-bridge              |  22 +--
 IBKR_PAPER_BRIDGE/deploy/linux/verify.sh           |  17 ++-
 IBKR_PAPER_BRIDGE/tests/test_api.py                |   6 +-
 IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py   | 148 ++++++++++++++-------
 8 files changed, 301 insertions(+), 107 deletions(-)
```

`--name-status`: 7 `M` + 1 `A` (the cron runner). No deletes, no renames, nothing
outside `IBKR_PAPER_BRIDGE/`. **The cron runner is committed, not untracked** — the
Lead staged what RIC2 left untracked, and the recorded 263 B / sha256
`2942986a…fafa47` matches the committed blob exactly.

Application code is untouched **at the whole-package level**, verified by tree OID
rather than by inspection — this round changed no Python outside `tests/`:

| Path | `be689537` tree | `a7460784` tree | |
|---|---|---|---|
| `IBKR_PAPER_BRIDGE/bridge` (whole package) | `86584046…` | `86584046…` | IDENTICAL |
| `bridge/engine` | `ce762510…` | `ce762510…` | IDENTICAL |
| `bridge/store` | `c305201f…` | `c305201f…` | IDENTICAL |
| `bridge/broker` | `14a18b1c…` | `14a18b1c…` | IDENTICAL |
| `IBKR_PAPER_BRIDGE/config` | `106fbe67…` | `106fbe67…` | IDENTICAL |

That is a stronger statement than round 2 could make: `bridge/` as a whole is
byte-identical, so no engine, store, broker, routes, app, Pine, parity, `MTC_V2`,
trading, order, risk, schema, backtest, or strategy byte moved. **Scope: PASS.**

### Extra — the pinned payload verified against the commit (beyond the required checks)

Plan V5 `:20` pins `C:\tmp\payload-a7460784` with `RELEASE_SHA256SUMS` sha256
`2581ed3f…abd9b8c0`.

- measured `sha256sum RELEASE_SHA256SUMS` = `2581ed3fbb020c03bb4e0dc41f35d60a54ee949d892164c705a34050abd9b8c0` ✅ matches the pin;
- `sha256sum -c RELEASE_SHA256SUMS` → rc 0, self-consistent, 8008 entries;
- payload path set == commit path set + the generated `RELEASE_SHA` file (contents:
  `a7460784c1563c140ee7c75197aeab2b0170da8a`), which is untracked by design;
- **every payload file re-hashed with `git hash-object` binds to the commit's blob
  OID** — 0 mismatches over the whole tree.

**Line endings — checked deliberately, because this repo carries `* text=auto`.**
`git ls-files --eol` reports `i/lf w/crlf` for the new cron runner: the Windows
working tree holds CRLF (272 B, 9 CR) while the blob is LF (263 B, 0 CR). A payload
built from the Windows checkout would ship `#!/bin/sh\r`, and `/etc/cron.hourly/`
would fail with "bad interpreter" on every invocation, silently. **It did not
happen** — the payload copy is 263 B with **CR = 0**, byte-identical to the blob, as
are `install.sh`, `verify.sh`, `rollback.sh` and `lib/common.sh`. The recorded
hash in RIC2 is the LF form and is the form that ships. The ambiguity that has
produced three defects on this project is not present here.

---

## Required check 1 — per-finding closure, verified on mechanism

I re-ran the round-2 attacks against the **real candidate bytes** rather than reading
the repair report. Every one of the six exact false-pass fixtures named in the brief
now goes RED.

### Codex round-2 R1–R7

| # | Status | Mechanism verified |
|---|---|---|
| **R1** UFW range false pass | **PARTIALLY-CLOSED** | The first-field predicate is gone, replaced by a complete ALLOW-row parser (`common.sh:158-275`) that splits destination/source around `ALLOW IN`, strips `(v6)`, handles `on <iface>`, accepts a destination address before the port, resolves inclusive `a:b` ranges, and `exit 2`s on any unmodelled grammar. I ran the real function against my own fixtures: `8000:9000/tcp` → **rc 1 FAIL** ✅, `8790:8800/tcp` → **rc 1 FAIL** ✅. **A `LIMIT IN` rule on 8790 still passes → REQUIRED-1.** |
| **R2** stale V4 commands pinned to a retired candidate | **CLOSED** | V5 `:3-11` states that every executable command an operator runs is restated in V5 and that incorporated texts "supply context and constraints, never commands"; §2 is headed "overrides every earlier command block" and carries the `a7460784` payload path, release SHA and `2581ed3f…` manifest pin throughout. `:23` explicitly retires `62bf661b`/`1078ac22…`, `be689537`/`58705d92…`, and launchers v1/v2. The command-fidelity defect itself is gone; a *different* stage-3 fidelity defect is REQUIRED-2 below. |
| **R3** self-confirming side-effect evidence | **CLOSED** | V5 §3 replaces point-sampled `ss` with three legs. Applying the self-confirming test to each: leg 1 (read-only SQLite orders census + `bridge.db`/WAL sha256, before/after, from the operator's root session) — the service cannot make the census equal while writing an order, so it is falsifiable by a party the application cannot reach ✅. Leg 3 (`auditd` + a UID-scoped `connect` audit rule started **before** the window) is kernel-side, root-owned, **continuous rather than sampled**, and **attributed by UID** — it answers all four of Codex's objections, and the row **STOPs** if the rule cannot be proven active, with sampled `ss` explicitly barred from substituting ✅. Leg 2 is the application's own response, but it is the claim under test, not the evidence of absence. This is a genuine repair. Residuals → NIT-9. |
| **R4** rollback input contract + ordering | **PARTIALLY-CLOSED** | **Ordering is genuinely fixed** — V5 §2 stage 3 is explicitly "in THIS order" with state capture as item 1 and the rehearsal as item 2, and a literal `rollback.sh` command with no `--to-*` arguments is supplied. I verified against `rollback.sh:43-59` that `--state-manifest-file` and `--state-manifest-sha256` are the only required flags and that `--to-*` are optional. **But the named input cannot be produced on this deployment → REQUIRED-2.** |
| **R5** false log-retention bound | **CLOSED** | The policy comment now calls 1 GiB "the nominal calculation", states in terms that it is "NOT a bound or quota", and that "an oversized file remains oversized after it becomes a retained generation, so policy-only worst-case disk use remains unbounded **even after rotation**" — which is exactly Codex's correction, not a paraphrase of it. `daily` is gone; `hourly` + `maxsize 64M` + `rotate 7` + seconds-precision `dateformat` are real in the shipped file. A Bridge-only `/etc/cron.hourly/mtc-bridge-logrotate` exists, is installed `-m 0755` through `run_action "logrotate-cron-install"` (`install.sh:447-448`), and `verify.sh:242-244` checks it is executable **and** `cmp -s`-identical to the release copy. The compensating monitoring control is stated and appears in plan §2 stage 3.4. Residual → NIT-8. |
| **R6** three non-falsifying regressions | **CLOSED on the exact mutations** | All three recorded false-pass mutations reproduced RED by me on the real bytes: unlisted `run install … /opt/hermes` → **1 failed**; `printf … > /tmp/codex-verifier-mutation` in `verify.sh` → **1 failed**; commented-out `MemoryHigh`/`MemoryMax` (I confirmed 2 comment lines landed) → **1 failed**. The hand-maintained `real_mutations` dictionary is gone; both inventories are parsed from `install.sh` text. Residual completeness gaps → NIT-1, NIT-2, NIT-3. |
| **R7** launcher identity-key file read | **CLOSED** | `$PublicKey`, its existence check, `ssh-keygen -lf` and all public-file fingerprint parsing are deleted — confirmed by reading all 219 lines and by the v2→v3 diff. The expected fingerprint is now the pinned literal `SHA256:8b6bl/…HBC8` at `:15`, required in `ssh-add -l -E sha256` output at `:129-132`. No identity key file of any kind is opened. |

### Claude round-2 R1–R3

| # | Status | Mechanism verified |
|---|---|---|
| **R1** UFW destination-address / range false pass | **PARTIALLY-CLOSED** | My two exact fixtures re-run against the real function: `152.239.123.231 8790/tcp ALLOW IN Anywhere` → **rc 1**, `FAIL ufw exposes Bridge port 8790: 152.239.123.231 8790/tcp ALLOW IN Anywhere` ✅ (was rc 0 "not exposed"); `8000:9000/tcp` → **rc 1 FAIL** ✅. Both are in the parametrised arm as `bridge_port_after_destination_address` and `bridge_port_inside_wide_range`. **The second leg of my recommended fix — the substring catch-all — was not implemented, and the hole it covered is still open → REQUIRED-1.** |
| **R2** frozen-2020 timestamp accepted as fresh | **CLOSED — re-attacked empirically** | `test_api.py:63-66` is now strict `second_status_ts > first_status_ts` **plus** a bounded clock check `timedelta(0) <= datetime.now(UTC) - second_status_ts < timedelta(seconds=5)`. I applied my exact round-2 mutation to the real `_status_payload` (anchor confirmed: `status["status_ts"] = datetime.now(UTC).isoformat()`), verified it landed, and the arm went **RED**. The lower bound also rejects a future-stamped clock. This is a real assertion, not a restatement. |
| **R3** rehearsal input unavailable when the rehearsal runs | **PARTIALLY-CLOSED** | My problems (1) *ordering* and (3) *no command template* are both fixed, as above. My problem (2) — "the producer may not produce it" — is **not** fixed and is now sharper than I could state in round 2 → REQUIRED-2. |

**10 of 10 round-2 REQUIRED addressed on mechanism; 7 CLOSED, 3 PARTIALLY-CLOSED.
None REGRESSED into a worse state than round 2, and none of the 17 round-1 findings
I verified closed in round 2 has re-opened.**

---

## Required check 4 — D026 spot-check with mutations of my own construction

Method: `IBKR_PAPER_BRIDGE` copied to scratch **outside the repo**; each mutation
applied to the copy, confirmed present with `grep -c` before running, then reverted.
Baseline in the copy: the three deployment arms pass, the four-arm control returns
`3 passed`. The repository was never touched — `git status --porcelain` empty at
start and end.

Beyond re-running the recorded set, I built **eleven new UFW fixtures and five new
source mutations**. Three arms failed my falsification:

| # | Arm | **New** mutation (mine, not recorded) | Real result | D026 |
|---|---|---|---|---|
| 1 | `assert_ufw_bridge_safe` | `8790/tcp LIMIT IN Anywhere` | **rc 0, `PASS … Bridge port 8790 not exposed`** | ❌ **REQUIRED-1** |
| 2 | `test_dry_run_manifest_matches_every_real_install_mutation` | bare `mkdir -p /opt/hermes` (no `run`/`run_action` wrapper) | **1 passed, rc 0** | ❌ NIT-1 |
| 3 | same arm | bare `install -d -o root -g root -m 0755 /opt/hermes` | **1 passed, rc 0** | ❌ NIT-1 |
| 4 | same arm | `eval "install -d -m 0755 /opt/hermes"` | **1 passed, rc 0** | ❌ NIT-1 |
| 5 | same arm | `run_action "hermes-dir" install -d … /opt/hermes` with no matching `dry_run_action` | **1 failed, rc 1** | ✅ |
| 6 | same arm | `run install -d … /opt/hermes` (round-2's exact fixture) | **1 failed, rc 1** | ✅ |
| 7 | `test_first_start_unit_is_separate_masked_design_and_restart_no` | move `MemoryHigh`/`MemoryMax` from `[Service]` into `[Unit]` (systemd ignores them there) | **1 passed, rc 0** | ❌ NIT-2 |
| 8 | same arm | comment out both ceilings (round-2's exact fixture) | **1 failed, rc 1** | ✅ |
| 9 | `test_verifier_is_read_only_…` | `python3 -c 'open("/tmp/claude-verifier-mutation","w").close()'` | **1 passed, rc 0** | ❌ NIT-3 |
| 10 | same arm | `printf … > /tmp/codex-verifier-mutation` (round-2's exact fixture) | **1 failed, rc 1** | ✅ |
| 11 | `test_status_exposes_…fresh_timestamp` | frozen 2020 constant (my round-2 fixture) | **1 failed, rc 1** | ✅ |

UFW fixtures I constructed that behave **correctly** (all fail closed): `8790/tcp (v6)`,
`8790/tcp on eth0`, `8790` with no protocol, `8790/tcp` allowed only from `127.0.0.1`,
`Anywhere ALLOW IN 10.0.0.0/8` (an allow-all-ports rule, correctly treated as
exposing 8790), `ALLOW FWD` (unmodelled → STOP), and an ALLOW row carrying a ufw
comment (unmodelled → STOP). The clean `22/tcp` baseline passes. That is a
substantially better predicate than v2's — the failure is confined to the one
grammar below.

**`RIC2_REPAIR_REPORT`'s RED/GREEN claims are consistent with everything I measured.**
I reproduced each of its five recorded RED transcripts independently and got the same
outcome; its `1373 passed, 1 warning` matches my own run. I found no overstatement in
that report.

---

## REQUIRED findings

### REQUIRED-1 — `assert_ufw_bridge_safe` reports "Bridge port 8790 not exposed" while a UFW `LIMIT` rule exposes it

The repaired parser only inspects rows containing the literal string `ALLOW`
(`common.sh:209`, `index($0, "ALLOW")`). UFW's `limit` verb renders its rows with the
action `LIMIT IN`, which contains no `ALLOW`, so those rows are dropped **before** any
of the new fail-closed machinery — the destination/source split, the range
resolution, and the `mark_unmodelled` → `exit 2` STOP path are all unreachable for
them.

I ran the real candidate function against this fixture:

```text
Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing), disabled (routed)
To Action From
-- ------ ----
22/tcp ALLOW IN Anywhere
8790/tcp LIMIT IN Anywhere
```

Real result:

```text
PASS  ufw active, default-deny incoming; SSH port 22 allowed; Bridge port 8790 not exposed
RC=0
```

`ufw limit` is an ACCEPT rule with rate limiting — the port is exposed. This is not
an exotic grammar: `ufw limit` is the idiom ufw's own documentation recommends for
public ports, and the repository already knows it is a rule verb —
`test_linux_deployment.py:268` enumerates `limit` alongside `allow|deny|reject` when
asserting that no deployment script mutates ufw. The safety predicate ignores the
one verb its sibling test explicitly names.

**It is a live regression, and specifically against the leg I asked for.** The
deleted `assert_ufw_ssh_only` at `62bf661b` ended with a whole-status substring
catch-all:

```bash
case "$status" in
  *"${MTC_BIND_PORT}"*) fail "ufw mentions port ${MTC_BIND_PORT}; control plane must stay loopback-only"; return 1 ;;
esac
```

That catch-all **would** have caught `8790/tcp LIMIT IN Anywhere`. My round-2
REQUIRED-1 fix had two legs — "scan all fields, not `$1`" **and** "restore a substring
catch-all as a second leg". The first leg was implemented well; the second was not,
and the residual hole is precisely what the second leg covered.

Self-confirming-check test — *what would make this assertion fail?* Only a row whose
action column reads exactly `ALLOW IN`. The sentence it prints is about the port
being exposed. Those are still not the same question, which is the same defect shape
as rounds 1 and 2, now in its third form.

**Not unsafe on the host today.** `KVM2_READONLY_INVENTORY_2026-08-16.md:29-30`
records UFW active, default-deny incoming, "the ONLY allow rule is 22/tcp (v4+v6)",
and the application binds `127.0.0.1:8790`, so no UFW rule can expose it while the
bind holds; `assert_control_port_closed` / `assert_no_public_control_listener` are
`ss`-based and independent of UFW. The cost is that the §9-authorised verification
run would print a firewall-safety sentence that is not true in a state the operator
can reach with one ordinary command, on the reusable multi-tenant path that Codex R5
exists to protect.

**Fix (contained):** match on the action column generically — treat any row whose
action is not `DENY`/`REJECT` as an exposure candidate and run it through the
existing parser, so `LIMIT IN` is resolved exactly like `ALLOW IN`; and restore the
whole-status substring catch-all as an independent second leg so an unanticipated
future rendering fails closed rather than disappearing. Add a `LIMIT IN` fixture and
a `DENY`-only control to the parametrised arm.

### REQUIRED-2 — Plan V5 stage 3.1 names a rehearsal input that cannot exist on this deployment, and asserts an installer behaviour that is false

Plan V5 §2 stage 3.1 orders state capture first (a real fix) and gives a literal
producer command:

```
sudo python3.12 /opt/mtc-bridge/releases/a7460784…/IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py create \
    --source /var/lib/mtc-bridge/bridge.db --out-dir ~/bridge-state-manifest
sha256sum ~/bridge-state-manifest/bundle_manifest.json   # record → <STATE_MANIFEST_SHA256>
```

and stage 3.2 hardcodes the consumer:

```
sudo bash …/rollback.sh \
    --state-manifest-file ~/bridge-state-manifest/bundle_manifest.json \
    --state-manifest-sha256 <STATE_MANIFEST_SHA256>
```

The tool's interface is correct — I verified `create --source/--out-dir` and
`MANIFEST_NAME = "bundle_manifest.json"` at `tools/wal_state_bundle.py:81,1218-1230`,
that `--out-dir` is created if absent (`:742`), and that `tools/` reaches the release
directory via `run_action "release-copy" cp -a`. **The problem is the input.**

**`/var/lib/mtc-bridge/bridge.db` cannot exist when stage 3.1 runs.** I searched
`install.sh` for every reference: the only occurrence of the DB is
`"state_db": "${MTC_STATE_DB}"` written into the install manifest as a *path record*
(`install.sh:481`). The installer creates the state **directory** (`dry_run_action
"dir-state"`) and nothing else; the database is created by the application at first
start, and §4 forbids any service start ("No service start, no enable"), with the D3
matrix explicitly deferred to a separate owner sentence. So at stage 3.1
`/var/lib/mtc-bridge` exists and is empty.

I ran the plan's exact producer command against that exact condition:

```text
$ python tools/wal_state_bundle.py create --source <empty-state-dir>/bridge.db --out-dir <out>
wal_state_bundle: cannot resolve source database path
REAL RC=3
bundle produced?  ls: cannot access '<out>': No such file or directory
```

**rc 3, no bundle, no `bundle_manifest.json`.** The stage-3.2 command then names a
file that does not exist, and `rollback.sh:60` dies with
`state manifest file is missing`.

Three consequences:

1. **V5 contains a false statement about the installer.** The parenthetical says
   "`wal_state_bundle.py` runs against the initialized DB the installer creates".
   The installer creates no DB. On this deployment that clause is never true.
2. **The fallback is ambiguous and, read literally, self-contradictory.** It says
   "the rehearsal input is the tar's sha256 **and** `rollback.sh` is exercised with
   the manifest the installer wrote". Those are two different artifacts —
   `~/bridge-state-initial.tar.gz` and `/etc/mtc-bridge/install_manifest.json`. But
   `rollback.sh:61-62` requires the sha to be the sha **of the file passed**:
   ```bash
   [ "$(sha256_of "${STATE_MANIFEST_FILE}")" = "${STATE_MANIFEST_SHA256}" ] \
     || die "state manifest file hash does not match accepted sha256"
   ```
   Pairing the tar's sha with the installer's manifest dies at that line. The
   operator has to guess which artifact was meant, mid-stage.
3. **The cost lands inside the single authorised attempt.** §4 authorises exactly one
   bounded attempt and the stage-3 sequence by name. The operator would run stage 3.1,
   get `rc 3` on the second command, and have to improvise the rehearsal input — which
   is the situation Codex R8, Codex R4 and my R3 were each raised to prevent. It is
   the same finding for the third round: the *ordering* half is now genuinely fixed
   and the *command template* half is now genuinely supplied, but the *producer
   actually produces it* half is still open.

This is not a criticism of the branch existing — anticipating an absent DB is right.
It is that the branch is written as the exception when it is in fact the only path
this plan can take, and the path it hands the operator is under-specified.

**Fix (contained, plan text only):** make the empty-state branch the **primary** one.
State plainly that on a fresh masked install no `bridge.db` exists, so the state
manifest is the stage-3.1 archive itself; give the two literal commands —
`sha256sum ~/bridge-state-initial.tar.gz` recorded as `<STATE_MANIFEST_SHA256>`, then
`rollback.sh --state-manifest-file ~/bridge-state-initial.tar.gz --state-manifest-sha256
<that same sha>` — and keep `wal_state_bundle.py` as the documented path for a later
rehearsal *after* first start, clearly labelled as not applicable now. One artifact,
one sha, one branch.

---

## Required check 5 — launcher v3 line-by-line

I walked all 219 lines and diffed v2→v3. **The diff is exactly the R7 repair and
nothing else**: `$PublicKey` and its existence check deleted, the `ssh-keygen -lf`
call and public-fingerprint parsing deleted, `$ExpectedFingerprint` literal added,
the comparison changed to `$agentFingerprints -notcontains $ExpectedFingerprint`,
plus header and comment text. **The entire option array, process handling,
readiness loop, `try/finally`, `Invoke-NativeCapture`, `Get-SshExitMessage`,
`Test-DashboardReady` and every `Fail` path are byte-identical to v2.** Every v2
soundness property is therefore retained by construction, including the ones round 2
verified empirically.

**No key-file read of any kind — verified precisely.** No identity key file is opened.
The one file the launcher does open is `known_hosts`, via `ssh-keygen -F $HostAddr -f
$KnownHosts` (`:124`), which is the **public host-key pin store** and whose reading is
the security property Claude R3 required. `Get-Service`, `ssh-add -l`, and
`Get-NetTCPConnection` read no files. `ssh-add -l` lists fingerprints, never key
material, and its output is never echoed. (V5's wording of this → NIT-4.)

**Pinned fingerprint literal enforced, fail-closed.** `:129-132`. I checked the
literal's form without opening any key file: 43 base64 characters decoding to 32
bytes — a well-formed SHA-256 fingerprint. Fail-closed in every direction I could
construct: rc 2 / rc 1 / any other nonzero from `ssh-add` each fail before the
comparison; an rc-0 agent list yielding no `SHA256:` token produces an empty array
and `-notcontains` is true → Fail; a catch in `Invoke-NativeCapture` leaves
`ExitCode = -1`, which falls to the `-ne 0` branch. A wrong or mistyped literal
fails closed too — the dashboard does not open. (Case-sensitivity → NIT-5;
provenance → NIT-14.)

**No new crash path, trust hole or orphan path.** Trust is pinned and isolated
(`-F NUL`, `IdentityFile=NUL`, `GlobalKnownHostsFile=NUL`, named user store,
`StrictHostKeyChecking=yes`, both proxy routes `none`, `BatchMode=yes`,
`PasswordAuthentication=no`, `KbdInteractiveAuthentication=no`,
`ExitOnForwardFailure=yes`, `ConnectTimeout=10`). `HasExited` is polled before and
after every readiness probe across 10 attempts, so the loop outlives
`ConnectTimeout=10`. `try/finally` (`:208-216`) force-kills and reaps the child on
every path the script survives; `-NoNewWindow` keeps ssh in the console group. The
only orphan path remains a hard kill of `powershell.exe`, which needs a Win32 Job
Object — unreachable from PS 5.1 without P/Invoke, and not a defect. Two round-2
NITs of mine are still open and remain NITs (NIT-6, NIT-7).

## Required check 6 — Plan V5 exactness

**Every §2 command matches the real script interfaces at `a7460784`**, checked against
the argument parsers rather than the documentation:

| V5 command | Real interface | |
|---|---|---|
| `install.sh --release-sha … --manifest-sha256 … --source … --dry-run` | `install.sh:62-66`; all three required at `:72-74`; 40-hex and 64-hex validated at `:75-78` | ✅ exact |
| `install.sh` (same, no `--dry-run`) | same | ✅ exact |
| `verify.sh --release-sha … --manifest-sha256 …` | `verify.sh:26-27`, both required `:32-33` | ✅ exact |
| `rollback.sh --state-manifest-file … --state-manifest-sha256 …`, no `--to-*` | `rollback.sh:46-47` required `:57-58`; `--to-*` optional and only paired-validated `:63-65` | ✅ exact — the "no `--to-*`" instruction is executable |
| `wal_state_bundle.py create --source … --out-dir …` → `bundle_manifest.json` | `:1218-1230`, `MANIFEST_NAME` `:81` | ✅ interface exact, **input unavailable → REQUIRED-2** |
| verify path `/opt/mtc-bridge/releases/<sha>/IBKR_PAPER_BRIDGE/deploy/linux/verify.sh` | `release-dir` + `release-copy cp -a "${SOURCE_DIR}/." "${DEST}/"` (`install.sh:337-338`) | ✅ resolves |
| SHA pins in §2 | payload manifest measured `2581ed3f…` ✅; release sha = HEAD ✅ | ✅ |

**Stage-3 ordering is coherent** — state capture → rehearsal → backup → monitoring →
re-inventory, and it is the ordering Codex R4 and my R3 asked for. **The rehearsal
branch logic is honest but not executable as written → REQUIRED-2.**

**§3 evidence mechanism — self-confirming test applied to each leg:** persistence leg
independent ✅, network leg independent, continuous and attributed ✅ with an explicit
STOP if it cannot be proven active ✅, response leg is the claim not the evidence and
is labelled as such ✅. This is the first version of this section that survives the
test. Residuals → NIT-9.

**§4 sentence.** Self-contained: it names the actions inline (transfer, dry run, one
bounded install, read-only verification, the five stage-3 items **in §2 order**,
including the rollback-manifest write), the exact release SHA, the boundary, the
auditd pre-authorisation scoped to "the later D3 evidence window only", the
exclusions, and the one-attempt/retry rule. It maps one-to-one onto §2 stages 1–3 —
I checked each item against §2 and found no action authorised that §2 does not
describe, and no §2 action unnamed. **Tenancy-boundary additions are enumerated**:
the cron file is named in §4, allowed in the stage-3.5 re-inventory diff, and
included in the V2 §7 removal enumeration referenced by the partial-install
disposition. Two scoping residuals → NIT-10, NIT-11.

## Required check 7 — fresh adversarial pass

Areas the earlier rounds had not attacked, and what I found:

- **The new cron asset end-to-end.** Name matches `run-parts`' LSB namespace
  (`^[a-zA-Z0-9_-]+$`, no extension) ✅; installed `0755` ✅; `#!/bin/sh` + `set -eu` +
  absolute `PATH` + `exec` ✅; `verify.sh` checks `-x` **and** byte-identity against the
  release copy ✅; LF in the payload ✅ (see check 2 — this was the highest-value thing
  I checked and it came back clean). Residual → NIT-8.
- **Line endings of every shipped script in the actual payload** — clean, as above.
- **The whole-package tree OID comparison** — stronger than a file list; `bridge/`
  is byte-identical, so no round-3 change can have touched application behaviour.
- **Payload↔commit blob binding over all 8007 tracked files** — 0 mismatches.
- **Whether the current `install.sh` actually has an unwrapped mutation** (the risk
  NIT-1 describes). I enumerated every non-comment line invoking a mutating verb and
  checked each against the wrapper, and independently reproduced the test's own parse:
  **32 planned IDs, 32 guarded IDs, symmetric difference empty in both directions**,
  and every mutating command routed through `run_action`. The two apparent exceptions
  are not mutations — `install.sh:356` is a `PIP_ARGS` array definition invoked at
  `:369` through `run_action "venv-install"`, and the `cat >` manifest write at `:468`
  is inside `write_install_manifest`, invoked through `run_action "manifest-write"`.
  **The dry-run manifest the operator reads at stage 1 is complete for these bytes**,
  which is what makes NIT-1 a completeness gap in the test rather than a live defect.
- **`ufw` grammar space** — eleven fixtures, one hole (REQUIRED-1).
- **Systemd section semantics** — one hole (NIT-2).
- **Non-shell write vectors in `verify.sh`** — one hole (NIT-3).

---

## NITs

1. **N-1 — the dry-run arm proves manifest↔wrapper parity, not manifest↔mutation
   completeness.** Its own comment claims the stronger property: "No hand-maintained
   action dictionary can hide a newly added mutation" and "A raw `run install …
   /opt/hermes` addition is therefore visible and RED". True only for commands
   prefixed `run`/`run_action`. A bare `mkdir -p /opt/hermes`, a bare `install -d …
   /opt/hermes`, or an `eval`-wrapped equivalent each stay **GREEN** (mutations 2–4
   above) — and the bare form is the *natural* way to write it, while the caught form
   is the unusual one. `/opt/hermes` is a reserved tenant path, so the property being
   claimed is the multi-tenant one. Graded NIT rather than REQUIRED because the exact
   round-2 fixture is genuinely RED, the `real_mutations` dictionary Codex objected to
   is genuinely gone, and I verified above that the shipped `install.sh` contains no
   unwrapped mutation — the gap is reachable only through a future source edit, which
   would itself be reviewed. **Fix:** mirror the existing `raw_run_calls == ['"$@"']`
   idiom — assert that no line outside `run_action`/`dry_run_action`/`require_cmd`
   invokes a mutating verb.
2. **N-2 — the unit-ceiling arm is section-blind.** Moving `MemoryHigh=768M` and
   `MemoryMax=1G` from `[Service]` into `[Unit]` keeps the arm **GREEN** (mutation 7),
   but systemd accepts resource-control directives only in `[Service]` and ignores
   them elsewhere with an "Unknown key name" warning, so the ceilings would be
   inert. The parser at `test_linux_deployment.py:358-364` skips `[` lines instead of
   tracking the section. This matters more than it looks: RAM is the **only enforced**
   resource protection — log/disk is explicitly nominal-only and CPU is unbounded — so
   multi-tenant item 10 rests on this one arm. `verify.sh:160-179` does not compensate:
   it uses `grep -qF 'MemoryHigh=768M'`, which is section-blind *and* comment-blind, so
   it would print "unit declares MemoryHigh=768M" in both mutated worlds. **Fix:**
   track the current section while parsing, and require both keys in `[Service]`.
3. **N-3 — the verifier read-only arm still uses a blacklist for write commands.** The
   redirection leg is now positive and complete (targets must be exactly `{/dev/null}`),
   which is the real improvement. But the command leg is
   `mktemp|rm|mv|cp|install|touch|tee|dd|truncate|ln|mkdir|rmdir|chmod|chown`, so a
   write through an unlisted interpreter — `python3 -c 'open("/tmp/…","w")'` — stays
   **GREEN** (mutation 9). Same grading logic as N-1: reachable only by editing
   `verify.sh`, and the current script has no such call. **Fix:** allow-list the
   commands `verify.sh` may invoke, the way `systemctl` verbs are already constrained
   to `{is-active, is-enabled}`.
4. **N-4 — V5 `:21` overstates the launcher property.** "No key file of any kind is
   opened" is broader than the mechanism: `ssh-keygen -F … -f $KnownHosts` opens
   `known_hosts`. The launcher's own header (`:3-5`) says it correctly — "No **identity**
   key file is opened". Use the launcher's wording in the plan; the distinction matters
   because reading the pin store is a required safety property, not an exception to one.
5. **N-5 — the pinned-fingerprint comparison is case-insensitive.** PowerShell's
   `-notcontains` compares strings case-insensitively; a SSH fingerprint is
   case-sensitive base64. The practical exposure is negligible, but the pin is now the
   *only* identity check in the launcher and `-cnotcontains` costs one character.
6. **N-6 — `:201` `Wait-Process -Id $tunnel.Id -ErrorAction Stop`** (my round-2 N-1,
   still open). If ssh dies between the readiness loop and this call — a real window,
   the browser launch sits inside it — the owner's `PROBLEM:` line becomes *"Cannot
   find a process with the process identifier 4242."*, which does not say the tunnel
   dropped. Use `$tunnel.WaitForExit()`, or `-ErrorAction SilentlyContinue` followed by
   the existing `ExitCode` check at `:203`, so `Get-SshExitMessage` produces the message.
7. **N-7 — `Fail()` ends with `Read-Host` under `$ErrorActionPreference='Stop'`** (my
   round-2 N-12, still open). With redirected stdin `Read-Host` throws and `exit 1`
   never executes. Only affects non-interactive use, which is not the design; a
   `try{}catch{}` costs nothing.
8. **N-8 — the hourly cadence is asserted but never verified.** `verify.sh` proves the
   runner file exists, is executable and matches the release copy; nothing proves the
   host actually executes `/etc/cron.hourly` — Ubuntu 24.04 drives the *system*
   logrotate from `logrotate.timer`, and `cron.hourly` fires only if the `cron` package
   is installed and running. If it is not, the policy silently reverts to the system
   run's cadence. Harmless as written, because the log bound is explicitly nominal-only
   and monitoring is the compensating control — but the plan should either add
   `systemctl is-active cron` to the stage-3.4 monitoring baseline or say the cadence
   is best-effort. (Note also that the system-wide logrotate run will process
   `/etc/logrotate.d/mtc-bridge` as well; both share the default state file, so this is
   consistent rather than double-rotating.)
9. **N-9 — §3 does not meet the exactness standard §2 sets for itself.** "prove the
   rule is active" has no literal command (`auditctl -l | grep mtcbridge_net` would do),
   and the SQLite census is described ("read-only URI") rather than written out. Also
   `-F arch=b64` scopes the rule to 64-bit syscalls, and the rule captures *all*
   connects for the UID including loopback, so the "zero connect events to non-loopback
   destinations" criterion requires the operator to filter records by hand. Graded NIT
   because §3 executes only after a *separate* first-start sentence, so it is not part
   of what §4 authorises to run now — but it will need the same treatment §2 got before
   that sentence is asked for.
10. **N-10 — §4's boundary clause does not cover three artifacts §4 itself authorises.**
    "all inside the V2 §0 Bridge tenancy boundary plus the single named cron file" —
    but the named actions also create `~/payload-a7460784` (stage 1),
    `~/bridge-state-initial.tar.gz` and `~/bridge-state-manifest/` (stage 3.1) in
    `/home/baris`, which are not Bridge-tenancy paths and are not enumerated for removal
    the way the cron file is. No other tenant is affected, so this is precision, not
    risk — but the sentence is the whole instrument for a non-technical owner. Name the
    operator-home artifacts in the same breath as the cron file, and add them to the
    cleanup enumeration.
11. **N-11 — `:31` is not an exact command.** `ssh baris@152.239.123.231  # same pinned
    options; then on the host:` elides the option set in a plan whose header states
    that *every* executable command an operator runs is restated in this file. Spell it
    out or say explicitly that the interactive login is out of scope for the exactness
    guarantee.
12. **N-12 — `OpenSSH` is special-cased as safe while every other application profile
    STOPs** (`common.sh:234-237`). The profile is Ubuntu's standard 22/tcp definition, so
    this is right in practice, but `/etc/ufw/applications.d` is editable and the code's
    own comment says application profiles "must be replaced with explicit numeric
    port/range rules before this assertion can pass". Either resolve the profile through
    `ufw app info OpenSSH` or note the assumption in the comment.
13. **N-13 — an ALLOW row carrying a ufw comment halts verification.** `22/tcp ALLOW IN
    Anywhere # admin ssh` renders the source field unmodelled and the whole assertion
    STOPs. That is the correct, fail-closed direction and I am not asking for it to be
    relaxed — but rule comments are ordinary practice, so the operator runbook should
    say that a commented rule will stop verification and how to proceed, or the parser
    should strip a trailing `#…` before the source test.
14. **N-14 — the pinned fingerprint's provenance is unverifiable inside the package.**
    V5 `:21` attributes it to the Lead, computed from the public file. I checked its
    form (valid 43-char base64 → 32 bytes) but deliberately did not open any key file to
    confirm it is the owner's key. A transcription error fails closed — the launcher
    refuses and the dashboard does not open — so this is disclosure, not a defect: the
    owner should be told that if the launcher reports the fingerprint is not loaded, the
    pin may be wrong rather than his agent.

---

## Verdict

**REQUEST_CHANGES — 2 REQUIRED, 14 NIT.**

The round-3 work is real and, on most axes, better than what I asked for. The
candidate delta is exactly the eight claimed files with `bridge/` byte-identical by
tree OID, so no application behaviour can have moved. The suite is
`1373 passed, 1 warning` under my own hand with the worktree clean before and after.
The payload binds to the commit blob-for-blob across all 8007 tracked files, and the
new cron runner ships LF — the `text=auto` trap that has produced three defects on
this project was live here and was avoided. All six exact round-2 false-pass
fixtures now go RED on the real bytes; I reproduced each rather than reading the
report, and found no overstatement in `RIC2_REPAIR_REPORT`. Launcher v3 removes the
identity-key read completely, and its diff from v2 touches nothing else, so every
property round 2 verified survives by construction. Plan V5's §2 finally restates
every command against the real script interfaces — I checked each flag against the
argument parsers — and §3 is the first version of the evidence section that survives
the self-confirming test on all three legs.

Two findings stop it, and both are the third appearance of a finding this pair has
raised twice:

- **REQUIRED-1** is a host-safety predicate that prints "Bridge port 8790 not
  exposed" for a `LIMIT IN` rule that exposes it. The parser rebuild is genuinely
  good — eleven fixtures I constructed behave correctly, including forms nobody had
  tested — but it filters on the string `ALLOW` before any of its fail-closed
  machinery runs, so an entire ufw verb never reaches the STOP path. It is a live
  regression against the substring catch-all in the function it replaced, and that
  catch-all was the second leg of the round-2 fix I recommended. Not unsafe today —
  the host has 22/tcp only and the listener is loopback-bound — but the sentence is
  false in a state one ordinary command reaches.
- **REQUIRED-2** has an operational cost inside the single authorised attempt. Stage
  3.1's producer command exits 3 with `cannot resolve source database path` on this
  deployment, because the installer creates no `bridge.db` and no service start is
  authorised; the plan's claim that it "runs against the initialized DB the installer
  creates" is false; stage 3.2 then names a file that cannot exist; and the fallback
  sentence pairs one artifact's sha with another artifact's manifest, which
  `rollback.sh` rejects by design. The ordering fix and the literal command template
  are real repairs — this is the remaining third of the same finding.

Both are contained edits: an action-column change plus a restored catch-all and two
fixtures for the first; a rewritten stage-3.1 paragraph naming one artifact, one sha
and one branch for the second. Neither requires re-opening the candidate's
application code, and neither disturbs anything verified closed above. The fourteen
NITs are genuinely optional, though N-1, N-2 and N-3 are cheap and would retire the
"test is green in both worlds" pattern that has now cost this package three rounds.

This exhausts the Plan-V3 T0 cap of 3. Per the cap rule the package goes to the owner
unaccepted, and I am not softening either finding to avoid that — the brief is
explicit that honesty outranks schedule, and REQUIRED-2 in particular would surface
as a failed command in the middle of the one attempt the owner signs for.

**The §4 sentence should not be presented on these bytes.** My recommendation to the
owner, in plain terms: the deployment package is close and the engineering is sound,
but one firewall check still prints a wrong "safe" line for a rule form he could
create by accident, and one step of the deployment script would fail partway through
because it asks for a database file that will not exist yet. Both are small text and
code fixes, not a redesign.

---

*Reviewer: Claude slot, `claude-opus-5`, round 3 of 3. Read-only outside this file
and disposable scratch; no host or network contact; launcher never executed; no ssh
invocation of any kind; no git mutation. All three subject pins verified identical at
start and at end.*
