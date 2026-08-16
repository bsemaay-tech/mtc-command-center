# T0 round-2 verdict — plan V4 + launcher v2 + replacement candidate `be689537` — Claude slot

| Field | Value |
|---|---|
| Reviewer slot | Claude (one of two independent T0 flagships), round 2 of the un-reset Plan-V3 T0 cap (3) |
| Model identity (runtime-reported) | `claude-opus-5` — "Opus 5", Claude 5 family |
| Effort | `xhigh` as configured by the dispatching route. **In-session introspection of the effort setting is not possible**; I applied no lower-effort override. Same caveat of record as round 1. |
| Session | Fresh, adversarial |
| Working directory | `C:\AUD62B` (candidate worktree) |
| Start (UTC+3) | 2026-08-16 14:01:06 |
| Stop (UTC+3) | 2026-08-16 14:14:50 |
| **VERDICT** | **REQUEST_CHANGES** — 3 REQUIRED, 12 NIT |

## Subject pins — start and end

| # | Subject | Expected | Start | End |
|---|---|---|---|---|
| 1 | `KVM2_DEPLOYMENT_PLAN_V4_2026-08-16.md` | 7676 B / `c2339ea0…9796ae0` | 7676 B / `c2339ea0d41f921e3174b9f82bbbe07554649e69453447decf307999c9796ae0` ✅ | identical ✅ |
| 2 | `KVM2_RUNKIT/Open-BridgeDashboard.ps1` | 9008 B / `e6e8bfa4…2c4e1675c` | 9008 B / `e6e8bfa4217b05b0b134018175c082186b6fcbcb5c66d0cfbfa7ed84c2e1675c` ✅ | identical ✅ |
| 3 | Candidate commit | `be689537…` | HEAD `be68953787c299bdaf30f83f301aa66a8ec0ea1f`, parent `62bf661b065dec5b5d9895d83575581fe369252d` ✅, tree `4ff9a5cf…`, tip of `integration/bridge-release-20260815` (local + `origin/`), `git status --porcelain` empty ✅ | identical, still clean ✅ |

All three pins matched at start and at end. No STOP condition.

### Exclusions honoured

Read-only everywhere except this file plus disposable scratch **outside** the repo
(`…\scratchpad\d026`, `C:\tmp\_ufwprobe`, `C:\tmp\_bk_*`). **No host contact, no
network contact, the launcher was never executed, no ssh connection was opened,
no git mutation anywhere, no credential read, no sub-delegation.**
`C:\LAB\Tradingview_LAB_CLEAN` untouched; `C:\R7FINAL` read only.

Local probes run (none touches a host or network):

- `Get-FileHash`/`sha256sum` on the pinned files and the payload;
- the full pytest suite from the candidate root;
- mutation runs of individual tests against a **copy** of `IBKR_PAPER_BRIDGE` in scratch;
- `bash` fixture runs of `assert_ufw_bridge_safe` sourced from the scratch copy;
- **`ssh -G`** — local configuration evaluation only, opens no socket. I used the
  placeholder host `t0-review-placeholder.invalid`, not the real KVM2 address, so
  the probe is unambiguously non-contacting. Option parsing is host-independent.

---

## Required check 3 — full suite, executed by me

```
PYTHONUTF8=1 python -m pytest -q -p no:cacheprovider IBKR_PAPER_BRIDGE/tests
```
run from `C:\AUD62B` at HEAD `be689537`. Exact final line:

```
1367 passed, 1 warning in 174.80s (0:02:54)
```

**Required `1367 passed, 1 warning` — MET.** `git status --porcelain` empty after
the run; HEAD unchanged. (Third independent timing: implementer 183.59 s, Lead
163.40 s, this run 174.80 s.)

## Required check 2 — candidate delta scope

`git diff --stat 62bf661b..be689537` = **exactly the 11 claimed files**, +350/−77,
all `M` (no adds, no deletes, no renames). Byte-for-byte match with the stat block
in `RIC1_IMPLEMENT_REPORT_2026-08-16.md:201-212`.

Trading logic untouched — verified by tree OID, not by inspection:

| Path | `62bf661b` tree | `be689537` tree | |
|---|---|---|---|
| `bridge/engine` | `ce762510…` | `ce762510…` | IDENTICAL |
| `bridge/store` | `c305201f…` | `c305201f…` | IDENTICAL |
| `bridge/broker` | `14a18b1c…` | `14a18b1c…` | IDENTICAL |
| `bridge/app.py`, `config/` | — | — | 0 changed files |

Every changed file falls inside the owner-approved scope of
`OWNER_DECISION_STATUS_PATCH_2026-08-16.md:9-16` (status fields + display) or the
"repair ALL reproduced T0 findings" clause at `:17`. **Nothing outside scope.**

### Extra: the pinned payload verified (beyond the required checks)

The plan pins `RELEASE_SHA256SUMS` at `58705d92…891a8a24` (V4 `:19`). I found the
built payload at `C:\tmp\payload-be689537` and verified it:

- `sha256sum RELEASE_SHA256SUMS` = `58705d925c0a2488347f0b6206bb0e75cc130ae704c5cb52ffc4f945891a8a24` ✅ matches the pin;
- `sha256sum -c RELEASE_SHA256SUMS` → rc 0, self-consistent;
- **134 payload files compared byte-for-byte against the commit blobs: 0 diffs, 0 missing in either direction**;
- **CR count = 0** in `install.sh`, `verify.sh`, `rollback.sh`, `common.sh`, the
  unit template and the logrotate policy.

That last point matters and I checked it deliberately. This repo carries
`* text=auto`, so the Windows working tree holds CRLF (I measured 98 CRLF in the
unit template as checked out) while the blobs are LF. A payload built from a
Windows checkout would ship `#!/usr/bin/env bash\r` and fail on Ubuntu. It did
not happen — the payload is LF. The bytes/SHA ambiguity that has produced three
defects on this project is **not** present here.

---

## Required check 1 — per-finding closure, verified on mechanism

### Codex round-1 REQUIRED (R1–R10)

| # | Status | Mechanism verified |
|---|---|---|
| **R1** dashboard cannot pass D3-4 | **CLOSED** | `routes.py:35-37` adds `host_identity` (`socket.gethostname()`), `release_sha` (`MTC_BRIDGE_RELEASE_SHA`, default `unknown`), `service_start_ts`; `_status_payload` (`:262-274`) derives `service_health` and stamps `status_ts`; all three read paths (`/api/status`, `make_snapshot`, `_bump_and_broadcast`) routed through it. `index.html:101-105` adds five cards, `app.js:129-133` binds them. Falsified by mutation — see D026 below. |
| **R2** no agent-only auth / isolated route / named pin store | **CLOSED** | Verified by my own `ssh -G` parse, rc **0**, on the exact v2 option set: `identityfile NUL` — **and nothing else**, so the OpenSSH default identity files are never added; `identitiesonly no`, so agent keys remain the only usable source; `globalknownhostsfile NUL`; `userknownhostsfile C:\Users\BarışSemaay\.ssh\known_hosts` (quotes stripped correctly, non-ASCII intact); `stricthostkeychecking true`. `ProxyCommand=none`/`ProxyJump=none` accepted (`ssh -G` omits disabled proxies from its dump). Pin presence is now a real `ssh-keygen -F` (`:127-130`) and the intended **public** key fingerprint must be in the agent (`:132-146`) — public file only, no private key read. |
| **R3** unreliable failure/cleanup paths | **CLOSED** | `HasExited` is polled **before and after every readiness probe** across 10 attempts (`:187-194`), so the ~10–25 s loop outlives `ConnectTimeout=10` — the round-1 "one check at 3 s" gap is gone. `Get-SshExitMessage` (`:65-74`) reports the real `ExitCode` with a failure class. `Start-Process` and browser launch are wrapped (`:179-184`, `:200-205`). `try/finally` (`:178-224`) force-kills and reaps the child on every exit path the process survives. |
| **R4** dry run does not print the mutating plan | **CLOSED** | 31 ID-keyed `dry_run_action` lines (`install.sh:220-256`), emitted at `:274` before any mutation. **The dry-run block also moved ahead of identity creation** — the old one ran `groupadd`/`useradd` *first*, so `--dry-run` used to mutate the host. That is a real unreported improvement. Parity test falsified by mutation. |
| **R5** SSH-only predicate breaks multi-tenancy | **PARTIALLY-CLOSED** | Tenancy leg genuinely fixed: `assert_ufw_bridge_safe` accepts 80/443 and requires an SSH ALLOW rule; reverting to the old semantics turns the test red (proved). **The 8790-exposure leg has proven holes → REQUIRED-1 below.** |
| **R6** resource protection asserted not enforced; false 64 MiB cap | **CLOSED** | Unit gains `MemoryHigh=768M` + `MemoryMax=1G` (`template:59-61`), asserted by `verify.sh:169-170`. Logrotate becomes `rotate 7` + `maxsize 64M` on two explicitly named logs, and its own comment states the 1 GiB threshold budget **and** that it is not a hard quota. `size`→`maxsize` is the correct change: with `daily`, `size` rotates on size only, `maxsize` rotates daily *and* early. Plan §2.5 retracts the 64 MiB claim in terms. |
| **R7** log-absence used as no-side-effect proof | **CLOSED** | Plan §2.1 replaces it with host-side `ss -ntu` before/during/after plus `journalctl`, "observed by the operator session, not asserted by the application", with an explicit disclosure of what it does not cover. That is a second party the checked application cannot reach. (Residual sampling limit → NIT-5.) |
| **R8** rollback rehearsal has no executable input contract | **PARTIALLY-CLOSED** | The "not a no-op" half is fully repaired (§2.2 states the `rollback_manifest.json` write and §9 authorises it), and partial-install disposition is now enumerated. **The input contract is still not executable → REQUIRED-3 below.** |
| **R9** `verify.sh` not read-only | **CLOSED** | `mktemp` removed from `require_cmd` and from both comparison sites; `common.sh:132-153` and `verify.sh:191-201` use command substitution and process substitution. I grepped the whole script for write forms: only `2>/dev/null`, `>/dev/null` and read redirections remain. Falsified by mutation. |
| **R10** venv prerequisite unproved | **CLOSED** | `preflight_venv_capability` (`common.sh:61-68`) runs `python3.12 -c 'import venv, ensurepip'` under `PYTHONDONTWRITEBYTECODE=1` — non-mutating, and `ensurepip` is exactly the module Ubuntu withholds until `python3.12-venv` is installed, so it tests the real failure mode. Called at `install.sh:135`, before every mutation and on the dry-run path. Falsified by mutation. |

### Claude round-1 REQUIRED (R1–R7)

| # | Status | Mechanism verified |
|---|---|---|
| **R1** launcher aborts on its first executable statement | **CLOSED — re-attacked empirically** | The fatal warmup is deleted, and I re-ran my original attack against the v2 mechanism on the owner's actual PowerShell (**5.1.26100.9168**): `Invoke-NativeCapture` calling `ssh.exe` with a stderr-producing argument returned `rc=255` with 7 captured lines and **did not throw**. The local-scope `$ErrorActionPreference='Continue'` genuinely defuses `NativeCommandError`, and `$LASTEXITCODE` is captured before any caller decision. The one defect that made D3-3 unreachable is gone. |
| **R2** agent-failure branch unreachable; `ssh-add` never preflighted | **CLOSED** | All three binaries preflighted at `:99-103`. rc 2 (agent unreachable), rc 1 (no identities) and any other nonzero now have three distinct plain-language messages (`:117-125`). Fail-closed throughout: a catch leaves `ExitCode = -1`, which falls to the `-ne 0` branch. |
| **R3** claimed known_hosts *pin* preflight did not exist | **CLOSED** | `ssh-keygen -F $HostAddr -f $KnownHosts` at `:127-130`; nonzero says STOP/report and never accept a new key. The v1 check that only proved the file existed is gone. (Residual → NIT-3.) |
| **R4** D3-4 asserts a capability the candidate lacks | **CLOSED** | Same mechanism as Codex R1. D1/D3-4 are no longer mutually unsatisfiable: the facts are added to the existing System panel, not a redesign, so "use the existing dashboard first" survives. Plan §2.6 correctly notes no D3-4 relaxation was needed. |
| **R5** dashboard-requirement citation/count mismatch | **CLOSED — checked against the records** | `OWNER_REQUIREMENT_DASHBOARD_2026-08-16.md` has exactly **8** numbered items (`:21-48`); `OWNER_INSTRUCTIONS_KVM2_MULTITENANT_2026-08-16.md` **§2** has items **1–12** (`:38-57`). Plan §2.3 cites both exactly that way. The phantom "dashboard items 9–12" are gone. |
| **R6** D3-6 evidence spec admits a false pass | **CLOSED — verified in code** | `routes.py:94` `_require_confirm` still runs first, but §2.1 now requires the request to come from the dashboard's own ARM control (`app.js` sends `X-Confirm = state_version`, well-formed by construction), so the stale-confirm 409 is excluded by construction. The required detail string matches the runtime bytes exactly: `routes.py:97-101` concatenates to `ARM unavailable in credential-free DISARMED start mode; exchange access is disabled`. And I confirmed the 409 path raises **before** `_bump_and_broadcast` (`:112`), so "unchanged `state_version`" is a real, checkable postcondition. |
| **R7** §9 delegates scope to a superseded document | **CLOSED** | V4 `:3-5` — "**incorporates** V2 §0–§8 and V3 §D1–§D4 by reference as amended below; neither V2 nor V3 has independent authority". §9 now enumerates its own actions inline (`:87-92`). The owner can read the sentence and see what he is signing. (Residual → NIT-10.) |

**17 of 17 round-1 REQUIRED addressed on mechanism; 15 CLOSED, 2 PARTIALLY-CLOSED.
None REGRESSED.**

---

## Required check 4 — D026 spot-check (independent falsification)

Method: `IBKR_PAPER_BRIDGE` copied to scratch **outside the repo**; each fix
mutated in the copy; the arm re-run. Baseline in the copy: 9 passed. Repo never
touched — `git status --porcelain` empty at start and end.

I did not rely on the recorded RED transcripts. 12 mutations across 7 arms:

| Arm | Mutation | Result | |
|---|---|---|---|
| `test_ufw_bridge_safe_…` | disable the 8790 exposure leg | RED (`bridge_port_exposed` fails) | ✅ |
| `test_ufw_bridge_safe_…` | restore old SSH-only semantics | RED (`future_web_tenant` fails) | ✅ genuinely detects the R5 regression |
| `test_dry_run_manifest_…` | delete the `unit-mask` manifest line | RED | ✅ manifest↔code parity is real, not a line count |
| `test_installer_preflights_venv_…` | delete the `preflight_venv_capability` call | RED | ✅ |
| `test_status_exposes_…` | delete `host_identity` | RED | ✅ |
| `test_status_exposes_…` | make `KILLED` never map to `halted` | RED | ✅ |
| `test_status_exposes_…` | `/api/status` bypasses `_status_payload` | RED | ✅ |
| `test_status_exposes_…` | recompute `service_start_ts` per response | RED | ✅ start-time semantics genuinely pinned |
| `test_status_exposes_…` | **freeze `status_ts` to a 2020 constant** | **GREEN** | ❌ **→ REQUIRED-2** |
| `test_status_release_sha_defaults…` | remove the `or "unknown"` default | RED | ✅ |
| `test_dashboard_core_static_contract` | delete the `releaseSha` renderer | RED | ✅ |
| `test_dashboard_core_static_contract` | delete the Service Health card | RED | ✅ |
| `test_verifier_is_read_only_…` | reintroduce an `mktemp` write | RED | ✅ |
| `test_first_start_unit_…` | delete `MemoryMax=1G` | RED | ✅ |

All mutations reverted; the arms return 17 passed in the scratch copy.

**Disclosure of my own error:** my first attempt at the `KILLED`→`halted` mutation
used a `\n`-anchored pattern against a CRLF working tree, so it silently did not
apply and reported a false GREEN. I caught it by checking that the mutation had
landed, redid it CRLF-safe, and it went RED. The `status_ts` result below was
produced by a mutation I confirmed had landed (`grep -c` = 1) and is real.

`RIC1_IMPLEMENT_REPORT`'s RED/GREEN claims are consistent with what I measured,
including its honest disclosure at `:139` that the first combined RED run had a
harness fault in the status arm.

---

## REQUIRED findings

### REQUIRED-1 — `assert_ufw_bridge_safe` reports "Bridge port 8790 not exposed" while UFW exposes it

`common.sh:178-183` decides exposure from **field 1 only**:

```bash
bridge_allow="$(printf '%s\n' "${status}" | awk -v port="${MTC_BIND_PORT}" '
  /ALLOW IN/ && ($1 == port || index($1, port "/") == 1) { print }
')"
```

`ufw status verbose` puts the destination address in field 1 whenever a rule
names one, pushing the port to field 2. I ran the real function against fixtures:

| Fixture rule | Result |
|---|---|
| `8790/tcp ALLOW IN Anywhere` | rc 1 — FAIL ✅ |
| `8790/tcp on eth0 ALLOW IN Anywhere` | rc 1 — FAIL ✅ |
| **`152.239.123.231 8790/tcp ALLOW IN Anywhere`** | **rc 0 — PASS, printing "…Bridge port 8790 not exposed"** ❌ |
| **`8000:9000/tcp ALLOW IN Anywhere`** | **rc 0 — PASS, same message** ❌ |

The destination-address form is a **regression**: the deleted
`assert_ufw_ssh_only` carried a catch-all `case "$status" in *"${MTC_BIND_PORT}"*)`
that would have caught it on substring. The port-range form was missed before too.

The new D026 arm cannot detect either — its three fixtures use only the canonical
first-field form, so the test passes in both worlds. Self-confirming-check test:
*what would make this fail?* Only a rule whose **first token** is exactly the
port. That trigger is far narrower than the sentence the function prints.

Not unsafe today: the inventory records UFW with 22/tcp only, and the
`ss`-based `assert_control_port_closed` / `assert_no_public_control_listener`
(`common.sh`, called at `verify.sh:248-249`) are independent of UFW and do check
real listeners. But R5's whole point was the **reusable** path after the web
tenant opens rules, and that is exactly when non-canonical rule forms appear.

**Fix:** scan all fields, not `$1` — e.g. match `ALLOW IN` lines where any field
equals the port or starts `port/`, and restore a substring catch-all as a second
leg. Add both fixtures above to the parametrised arm.

### REQUIRED-2 — the "fresh timestamp" arm passes with a frozen 2020 constant

`tests/test_api.py` — `test_status_exposes_deployment_identity_health_and_fresh_timestamp`
asserts freshness with:

```python
assert datetime.fromisoformat(second["status_ts"]) >= datetime.fromisoformat(first["status_ts"])
```

I replaced `_status_payload`'s per-response stamp with
`status.setdefault("status_ts", "2020-01-01T00:00:00+00:00")` — a value that never
changes and is six years stale — and **the arm stayed GREEN**. `>=` is satisfied by
equality, and the constant parses with `tzinfo == UTC`.

This is the arm covering the **"Last Update"** tile, which is owner requirement 4's
last-update leg and part of D3-4's evidence. D3-4 records what the dashboard
*displays*, so a frozen timestamp would satisfy the suite and the D3 matrix
simultaneously while telling the owner nothing about whether his dashboard is
live. That is the self-confirming pattern, in a new check offered as closure
evidence — the exact thing required check 7 asks me to test.

The shipped implementation is correct; the check is not. I verified a real
assertion is achievable on the current bytes: strict `second > first` holds, and
`status_ts` is within 0.0005 s of `datetime.now(UTC)`.

**Fix:** assert bounded freshness against the clock —
`(datetime.now(UTC) - datetime.fromisoformat(payload["status_ts"])).total_seconds() < 5`
— plus strict `>` between the two calls. A frozen constant then fails.

### REQUIRED-3 — the rollback-rehearsal input named by §2.2 is not available when the rehearsal runs

`rollback.sh:56-62` hard-requires both `--state-manifest-file` and
`--state-manifest-sha256`, verifies the file exists, and dies unless its sha256
matches. Plan §2.2 names the input as "the freshly captured hash record of the
(empty) `/var/lib/mtc-bridge` state produced during stage-3 backup (§V2-5.3)".

Three problems in the referenced text:

1. **Ordering.** V2 §5 lists the rollback rehearsal as item **1** and
   backup/restore as item **3**. §2.2 sources the consumer's mandatory input from
   an item that runs *after* it, and neither V4 nor V2 reorders the stage or says
   §5.3 must run first. Codex R8 raised this ordering problem; V4 sources the
   input without resolving it.
2. **The producer may not produce it.** V2 §5.3 tars state to "an off-host
   encrypted archive **on the operator PC**; restore to temp; hash-compare". It
   never specifies a host-resident hash-record **file** with a recorded sha256 —
   and `rollback.sh` runs as root on KVM2 and does `[ -f "${STATE_MANIFEST_FILE}" ]`
   against a host path.
3. **No command template.** §2.2 says the exact command is "recorded in the
   execution record before running". The *form* is knowable now
   (`--state-manifest-file <path> --state-manifest-sha256 <sha>`, and **no**
   `--to-release-sha`/`--to-manifest-sha256`), and R8 asked for it.

This is the one finding with a live operational cost: §9 authorises the rehearsal
inside the **one** bounded attempt, and the operator would discover the missing
input mid-stage-3.

**Fix:** in §2.2, (a) state that §V2-5.3's state capture runs before §V2-5.1's
rehearsal, (b) require §5.3 to leave a host-resident hash record at a named path
with its sha256 recorded, and (c) give the literal command template with those two
placeholders and an explicit "no `--to-*` arguments in the initial rehearsal".

---

## Required check 5 — launcher v2 line-by-line (fresh eyes)

Walked all 227 lines. No remaining crash path, secret-touching path, unpinned
trust path, or orphaned-child path rises to REQUIRED.

**Correct, and checked rather than assumed:**

- **No secret is read or printed.** Only the `.pub` file is fingerprinted
  (`ssh-keygen -lf`, `:132`); `ssh-add -l` lists fingerprints, never key material;
  `Invoke-NativeCapture` output is never echoed. The one fingerprint printed
  (`:142`) is a public-key fingerprint.
- **Trust is pinned and isolated** — see Codex R2 above; verified by `ssh -G`.
- **Fail-closed fingerprint logic.** `Get-Sha256Fingerprints` requires the public
  file to yield exactly one fingerprint (`:138`) and the agent list to contain it
  (`:141`). An rc-0 agent list with no fingerprints fails; a `.pub` whose comment
  contained a second `SHA256:` token fails. Both fail in the safe direction.
- **N-3 (round-1) closed properly.** `:156` embeds real quotes into the option
  string; PS 5.1 `Start-Process -ArgumentList` joins without quoting, so the quotes
  survive to `CommandLineToArgvW`. `ssh -G` confirmed the path resolves intact,
  non-ASCII included.
- **N-5, N-6, N-13 closed.** Body marker `<title>Crypto Paper Bridge</title>`
  (`:88`), `$request.Proxy = $null` (`:81`), unconditional 1 s sleep (`:193`).
- **N-4 closed as specified** — `try/finally` at `:178-224` kills and reaps.
- **Child lifetime.** `-NoNewWindow` keeps ssh in the console group, so Ctrl+C and
  window-close reach it directly; `finally` covers script-level exits. The only
  orphan path left is a hard kill of `powershell.exe`, which needs a Win32 Job
  Object and is not reachable from PS 5.1 without P/Invoke. Not a defect.

## Required check 6 — the six §2 repairs

| §2 item | Verdict |
|---|---|
| **2.1** D3-5/D3-6 evidence independence | **REPAIRED.** Independent `ss -ntu` + `journalctl` observation by the operator session; the exact 409 detail string matches `routes.py:97-101` byte for byte; unchanged-`state_version` is a real postcondition (no bump on the 409 path). Residual sampling limit → NIT-5. |
| **2.2** rehearsal inputs + honest write + partial-install disposition | **PARTIALLY REPAIRED.** Honest write ✅ and §9 authorises it ✅; five-step partial-install disposition with "any retry needs a new owner sentence" ✅. Inputs ❌ → REQUIRED-3. |
| **2.3** citation hygiene | **REPAIRED.** Both counts verified against the records. |
| **2.4** authority structure / §9 self-contained | **REPAIRED.** Incorporation language + inline action enumeration. Residual → NIT-10. |
| **2.5** honest resource wording | **REPAIRED.** Matches the shipped unit and logrotate bytes; 2 logs × 8 files × 64 MiB = 1 GiB checks out; the false 64 MiB claim is explicitly retracted; disk is called monitored, not enforced. |
| **2.6** D3-4 provable against the new bytes | **REPAIRED.** All five legs exist and render; no D3-4 relaxation taken. |

## Required check 7 — self-confirming-check test on every new/changed check

Applied to all 14 new or changed checks. Twelve are genuinely falsifiable and I
proved it by mutation. Two fail the test: **REQUIRED-1** (a real ufw exposure the
predicate calls safe) and **REQUIRED-2** (a frozen timestamp the freshness arm
calls fresh). NIT-2 and NIT-3 are weak-but-honest checks, not false ones.

---

## NITs

1. **N-1** `:209` `Wait-Process -Id $tunnel.Id -ErrorAction Stop`. If ssh dies
   between the readiness loop and this call — a real window, the browser launch
   sits inside it — `Wait-Process` cannot resolve the exited PID and the owner's
   `PROBLEM:` line becomes *"Cannot find a process with the process identifier
   4242."*, which does not say the tunnel dropped. Use `$tunnel.WaitForExit()`, or
   `-ErrorAction SilentlyContinue` followed by the existing `ExitCode` check at
   `:211`, so `Get-SshExitMessage` produces the message instead.
2. **N-2** `service_health` is a state label, not a health probe. In
   credential-free DISARMED mode the only reachable non-`healthy` values are an
   operator KILL (`halted`) or a persisted `INTERRUPTED` window (`degraded`); no
   infrastructure condition can move it. Truthful as displayed, but the D3-4
   operator should be told the tile means "declared state", not "the process is
   well". Reachability of both non-healthy values is proven (KILL arm is RED under
   mutation), so it is not decorative — just narrow.
3. **N-3** The pin check proves an entry for `152.239.123.231` **exists** in
   `known_hosts`, not that it equals a recorded fingerprint. If the inventory
   records the host-key fingerprint, compare `ssh-keygen -F … -l` output against
   it; that is a few lines and closes the last gap between "pinned" and "pinned to
   the value we accepted".
4. **N-4** `app.py:161` — the engine's WS status publisher copies
   `bridge_status` directly instead of going through `_status_payload`, so in
   **paper** mode WS-driven updates carry a `status_ts` frozen at the last REST
   call. Not the KVM2 mode (that publisher is only installed when
   `start_runtime and not credential_free_disarmed`), so D3-4 is unaffected — but
   the "Last Update" tile will be wrong in paper mode. Route it through
   `_status_payload` for consistency.
5. **N-5** §2.1 requires `ss -ntu` at three instants. A connection opened and
   closed between captures is invisible. The disclosure covers "not every future
   instant" but not intra-window sampling. Cheap strengthening: run `ss` in a
   1-second loop for the duration of the attempt and keep the transcript, or add
   an nftables/conntrack outbound counter read before and after.
6. **N-6** V2 §5.1 still literally reads "no-op on a never-started masked unit
   (record that)". V4 §2.2 retracts it and V4's header makes the amendment
   binding, so this is formally fine — but a reader who opens the incorporated V2
   sees the false claim. Add a one-line "AMENDED BY V4 §2.2" marker, or restate
   §5.1 in V4.
7. **N-7** "genuinely read-only `verify.sh` (zero temp writes)" is true on the
   target host. Bash process substitution uses `/dev/fd` on Ubuntu 24.04 and
   creates no filesystem object; on a system without `/dev/fd` bash falls back to
   named FIFOs under `/tmp`. Worth stating as host-conditional, since the
   read-only property is now load-bearing in §9.
8. **N-8** Only RAM is enforced. Multi-tenant item 10 asks that the Bridge cannot
   consume resources future tenants need; a CPU-spinning process still can.
   §2.5 does not claim otherwise, so nothing is false — but consider
   `CPUQuota=` in the unit, or say explicitly that CPU is unbounded by design.
9. **N-9** I could not positively demonstrate `-F NUL` suppressing an ambient
   config, because this PC has no `~/.ssh/config`. The parse succeeds (rc 0) and
   ssh(1) specifies that supplying `-F` on the command line makes the system-wide
   config ignored, so the mechanism is documented and the option is accepted —
   but the suppression itself is inferred, not observed. Stating the limit rather
   than claiming the proof.
10. **N-10** §9 now enumerates its actions but still says "inside the Bridge
    tenancy boundary of V2 §0" without restating that boundary. The owner is
    non-technical; the sentence is the whole instrument. One clause naming the
    four Bridge paths would finish what §2.4 started.
11. **N-11** `:107-109` hard-fails when `hostinger_kvm2.pub` is absent. An owner
    with the correct key loaded in the agent but no `.pub` on disk cannot open the
    dashboard. Correct as fail-closed; worth telling the owner in the runbook that
    the `.pub` file must be kept.
12. **N-12** `Fail()` ends with `Read-Host` under `$ErrorActionPreference='Stop'`.
    If the script is ever run with redirected stdin, `Read-Host` throws and `exit 1`
    never executes. Only affects non-interactive use, which is not the design, but
    a `try{}catch{}` around it costs nothing.

---

## Verdict

**REQUEST_CHANGES** — 3 REQUIRED, 12 NIT.

This is a substantially different package from round 1, and the difference is
real rather than editorial. The two findings that made round 1 a stop —
a launcher that aborted on its first executable statement, and a D3-4 row
defining completion by facts the candidate did not carry — are both closed on
mechanism, and I re-ran my original attacks rather than reading the report:
the EAP-safe wrapper does not throw on the owner's actual PowerShell 5.1.26100.9168,
and the five status facts exist, render, and go red when mutated. Fifteen of the
seventeen round-1 REQUIRED findings are fully closed, none regressed, the suite
is `1367 passed, 1 warning` under my own hand, the delta is exactly the eleven
approved files with the trading engine, store and broker byte-identical by tree
OID, and the pinned payload is byte-for-byte the candidate with LF endings intact.

What remains:

- **REQUIRED-1** is a safety assertion whose printed conclusion is broader than
  its mechanism, and which regressed against the version it replaced. It does not
  make the §9 action unsafe today — the host has 22/tcp only, and the `ss`-based
  listener assertions are independent of UFW — but it undermines the reusable
  upgrade path that Codex R5 existed to protect.
- **REQUIRED-2** is a check, not a behaviour: the code is right and the arm is
  wrong. It matters because this arm is offered as closure evidence for the
  dashboard requirement, and it would stay green against a dashboard frozen in
  2020.
- **REQUIRED-3** is the one with an operational cost. It sits inside the single
  authorised attempt.

All three are contained edits — an awk predicate plus two fixtures, one assertion,
and three sentences of plan text. None requires re-opening the candidate's
application code, and none disturbs the closure verified above. One round remains
under the Plan-V3 T0 cap of 3.

The §9 sentence should not be presented on bytes a T0 reviewer has marked
REQUEST_CHANGES.

---

*Reviewer: Claude slot, `claude-opus-5`. Read-only outside this file and
disposable scratch; no host or network contact; launcher never executed; no git
mutation. All three subject pins verified identical at start and at end.*
