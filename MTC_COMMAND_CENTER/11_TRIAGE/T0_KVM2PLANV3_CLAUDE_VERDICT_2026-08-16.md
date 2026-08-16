# T0 verdict — KVM2 deployment plan V3 + dashboard launcher — candidate `62bf661b` — Claude slot

| Field | Value |
|---|---|
| Reviewer slot | Claude (one of two independent T0 flagships) |
| Model identity (runtime-reported) | `claude-opus-5` — "Opus 5", Claude 5 family |
| Effort | `xhigh` as configured by the dispatching route. **In-session introspection of the effort setting is not possible**; I applied no lower-effort override. Same caveat of record as `BRIDGE_RELEASE_T0_ACCEPTANCE_2026-08-16.md` lines 40–45. |
| Session | Fresh, adversarial, no V1/V2 review context |
| Working directory | `C:\AUD62A` (candidate worktree) |
| Start (UTC+3) | 2026-08-16 13:11:47 |
| Stop (UTC+3) | 2026-08-16 13:22:36 |
| **VERDICT** | **REQUEST_CHANGES** — 7 REQUIRED, 13 NIT |

## Subject pins — start and end

| File | Expected | Start | End |
|---|---|---|---|
| `KVM2_DEPLOYMENT_PLAN_62BF661B_V3_2026-08-16.md` | 6770 B / `065da2d5…4769fff` | 6770 B / `065da2d513ad6c821e78a0977df5787be3b8d7550a87deadeb8f7afb34769fff` ✅ | identical ✅ |
| `KVM2_RUNKIT/Open-BridgeDashboard.ps1` | 4859 B / `9c9beaeb…3d96c2972` | 4859 B / `9c9beaebcf73374588e3a1594760b613bbca5f04b66af75bf6329a13d96c2972` ✅ | identical ✅ |

Both pins matched at start and at end. No STOP condition.

### Exclusions honoured

Read-only everywhere except this file. **No host contact, no network contact, the
launcher was never executed, no ssh connection was opened, no git write, no
credential read, no sub-delegation.** `C:\LAB\Tradingview_LAB_CLEAN` untouched.

Three local probes were run; none touches a host or a network:
- `Get-FileHash` on the two pinned files (start + end);
- three PowerShell language-semantics probes against a `cmd.exe` stub and
  `ssh.exe` **invoked with no hostname** (prints usage, exits — no connection);
- `ssh-keygen -F` against the local `known_hosts` file (pure file read).

### Independence disclosure

While grepping `11_TRIAGE` for the string "item 12", one line of the counterpart
file `T0_KVM2PLANV3_CODEX_VERDICT_2026-08-16.md` appeared in the results (a
section heading only: `### 1. Owner dashboard requirements 1–11 plus item 12`).
I did not open that file and read no part of its analysis or verdict. Every
finding below was derived from the subject bytes and the candidate source.

---

## Check 1 — Owner dashboard requirements: cite or MISSING

**Record discrepancy up front:** the kickoff scopes this check as "requirements
1–11 + item 12". The binding record
`OWNER_REQUIREMENT_DASHBOARD_2026-08-16.md` contains **eight** numbered items
(lines 20–50). There is no item 9, 10, 11 or 12 in it, and the 12-item list in
`OWNER_INSTRUCTIONS_KVM2_MULTITENANT_2026-08-16.md` is the multi-tenant set
(check 2), whose item 12 (lines 56–57) is the future-upgrade section. Items 9–12
of a "dashboard requirement set" are therefore **unverifiable — no record
exists**. See REQUIRED-5. Below I check the eight recorded items plus the
kickoff's item-12 substance (NEXT_STEPS queuing), which does exist and is
satisfied.

| Owner item (source) | Plan V3 | Result |
|---|---|---|
| 1. 8790 never public; UFW never opens it; reverse proxy never proxies dashboard or any control endpoint (owner req 20–23) | V3 D1 lines 34–38; §9 line 95 "no public exposure of port 8790 ever" | **CITED** (see NIT-9 on the enumeration) |
| 2. Completion = owner can securely open the dashboard after the separate first DISARMED start (owner req 24–26) | V3 D3 header lines 57–59; D3-3 line 65 | **CITED** |
| 3. One-click launcher, T0-audited with the package: pinned tunnel, opens browser, no password/passphrase stored, agent key, strict host-key, clear failure on auth/forward/local-port (owner req 27–30) | V3 lines 11–12 (package), D2 lines 43–55; artifact `Open-BridgeDashboard.ps1` | **CITED but NOT SATISFIED** — the artifact aborts on its first executable statement (REQUIRED-1) and one claimed preflight does not exist (REQUIRED-3) |
| 4. Verification proves: loopback-only; unreachable from internet; tunnel works; dashboard shows correct **host, candidate SHA, service health, last update time, DISARMED**; live capability disabled; no button can ARM (owner req 31–36) | D3-1 line 63 ✓; D3-2 line 64 ✓; D3-3 line 65 ✓; D3-4 line 66 **unprovable**; D3-5 line 67 ✓; D3-6 line 68 ✓ (weak spec) | **PARTIAL** — host / SHA / last-update legs are **MISSING from the candidate's API and UI** (REQUIRED-4) |
| 5. No redesign delay — verify the EXISTING dashboard first (owner req 37–38) | D1 lines 30–31 | **CITED** — but mutually unsatisfiable with item 4 as written (REQUIRED-4) |
| 6. Dashboard V2 package, separately scoped, immediately after stable DISARMED deploy; ten named views; read-only/control split; public hosting never exposes control endpoints; public/authenticated access = separate scope + authorization (owner req 39–46) | D4 lines 75–84 — all ten views present (health, DISARMED/ARMED, SHA+host, active strategy, positions+working orders, equity+P&L, risk gates, decision stream+errors, backup health, last update); hard split line 79–81; public-hosting bar line 81–82; separate authorization line 82–83 | **CITED, complete** |
| 7. Multi-tenant protections of V2 retained unchanged (owner req 47) | V3 lines 14–24 | **CITED** (see check 2 and REQUIRED-7) |
| 8. Authorizes no install/config/start/firewall/deployment; reviews first, then the single sentence (owner req 48–50) | V3 status line 3 "PLAN — NOT AUTHORIZED TO EXECUTE"; §9 framed as an ask, line 87 "present AFTER the fresh T0 pair accepts these bytes" | **CITED** |
| kickoff item 12 — NEXT_STEPS queuing of D4 | `_AI_MEMORY/NEXT_STEPS.md` top block, "Update 2026-08-16 evening" entry 4: **[AI: Claude]** Dashboard V2 work package, ten views, hard split, tier split T1/T0, "Spec anchor: plan V3 §D4" | **PRESENT** |

## Check 2 — Multi-tenant requirements 1–12 (V2 §0/§7 by reference)

All twelve remain satisfied through the carried V2 text. Mapping:

| Owner multi-tenant item | Carrier |
|---|---|
| 1 no Hermes/websites now | V2 §0 table lines 18–19 "FUTURE — nothing installed now" |
| 2 Bridge self-contained | V2 §0 line 17 (four paths, own user), §7 lines 143–150 |
| 3 no global Python packages / shared dirs | V2 §0 lines 28–30 |
| 4 reserved future locations + identities | V2 §0 lines 18–19, 24–27 |
| 5 loopback-only 8790, never behind the reverse proxy | V2 §0 line 17; **strengthened** by V3 D1 lines 34–38 |
| 6 80/443 reserved; SSH-only is present state not requirement | V2 §0 lines 19, 31–33 |
| 7 no host-wide security change | V2 §0 lines 31–33 |
| 8 service-specific backups/monitoring/logrotate/rollback | V2 §0 lines 34–36; §5 lines 112–123 |
| 9 rollback never touches future-tenant anything | V2 §7 lines 147–150 |
| 10 resource headroom recorded | V2 §0 lines 44–53 (≤1 GiB / ≤10 G vs measured 46.9 MiB) |
| 11 isolation | V2 §0 lines 37–42 |
| 12 future-upgrade section, bootstrap never repeated | V2 §2 lines 74–80; §8 lines 152–176 |

Independently corroborated against the candidate's own deploy assets (see check
6): `install.sh` never touches the firewall (`assert_ufw_ssh_only` is read-only,
lines 237/390), installs the unit **masked** and asserts not-active/not-enabled
(lines 365–378), and `rollback.sh` is stop+mask+preserve with an explicit bar on
deleting `/var/lib/mtc-bridge` (header lines 17–20). Claims match code.

**One formal defect** in how V2 is carried → REQUIRED-7.

## Check 3 — Launcher line-by-line security review (T0 heart)

Walked every line of `Open-BridgeDashboard.ps1` (4859 B, 97 lines).

### What is correct

- **No secret handling.** No password, no passphrase, no key file passed for
  authentication — the ssh invocation (lines 60–69) carries no `-i` and no
  `IdentityFile`. `$agentList` (line 49) is captured and never printed. The two
  Fail messages that mention `~/.ssh/hostinger_kvm2` (lines 46, 51) are
  single-quoted instructional text; `$env:USERPROFILE` is not even expanded.
  **No secret is ever printed.** ✅
- **Strict host-key policy.** `StrictHostKeyChecking=yes` + explicit
  `UserKnownHostsFile=$KnownHosts` + `BatchMode=yes` (lines 63–65) — a changed
  host key is a hard failure and can never be auto-accepted. ✅ The explicit
  `UserKnownHostsFile` is the right fit for the recorded operator fact that the
  Turkish character in `%USERPROFILE%` breaks default resolution
  (`KVM2_READONLY_INVENTORY` line 17). I confirmed locally that OpenSSH reads
  that non-ASCII path correctly (`ssh-keygen -F 152.239.123.231` → rc 0, three
  key types matched — the pin genuinely exists).
- **`ExitOnForwardFailure=yes`** (line 66) present, plus the local-port-free
  preflight (lines 55–56) and the `HasExited` check (lines 74–76). ✅
- **Forward binds loopback explicitly** — `-L 127.0.0.1:18790:127.0.0.1:8790`
  (line 62), four-field form, no `0.0.0.0`, `GatewayPorts` left at default no.
  The tunnel cannot be reached from the LAN. ✅
- **No other network contact.** One `ssh` to the pinned host, one
  `Invoke-WebRequest` to `127.0.0.1:18790`, one `Start-Process` of a loopback
  URL. Nothing else. ✅ (NIT-13 on proxy edge case.)
- **Host/user fidelity** — `152.239.123.231` / `baris` match
  `KVM2_READONLY_INVENTORY` lines 12–16. ✅
- **`exit 1` inside `Fail()`** correctly terminates the whole script, not just
  the function. ✅
- **`ssh-add -l` exit-code logic is sound in principle** (asked explicitly by the
  kickoff): Windows OpenSSH `ssh-add -l` returns 0 = identities listed, 1 = agent
  reachable but empty, 2 = cannot connect. `if ($LASTEXITCODE -ne 0)` (line 50)
  correctly catches both failure codes, and line 48's warmup cannot poison
  `$LASTEXITCODE` because `ssh-add.exe` resets it. The logic is right; the
  **statement that carries it is not** — see REQUIRED-2.

### REQUIRED-1 — the launcher aborts on every run, at its first executable statement

`Open-BridgeDashboard.ps1:48`
```powershell
& $SshExe -o BatchMode=yes 2>$null | Out-Null   # no-op warmup; ignore
```
with `$ErrorActionPreference = 'Stop'` at line 20.

In **Windows PowerShell 5.1**, redirecting a native executable's stderr wraps
each stderr line in a `NativeCommandError` ErrorRecord; with `EAP = 'Stop'` that
becomes a **terminating** error. `ssh.exe` with no hostname writes its usage
block to stderr. There is no `try`/`catch`.

Empirically confirmed on this machine, with the real binary at the real path:

```
psver = 5.1.26100.9168
CASE-A  & cmd.exe /c "echo x 1>&2"                2>$null | Out-Null  -> THREW NativeCommandError
CASE-B  & C:\Windows\System32\OpenSSH\ssh.exe -o BatchMode=yes 2>$null | Out-Null
                                                                      -> THREW NativeCommandError
CASE-C  $x = & cmd.exe /c "echo x 1>&2"           2>&1                -> THREW NativeCommandError
```

`pwsh` is **not installed** on this PC (checked: `Get-Command pwsh` → not found),
and `.ps1` has no file association, so the only way the owner can run this is
`powershell.exe` 5.1 — i.e. the case that throws. `2>$null` does not save it
(CASE-A).

**Consequence:** the one-click launcher never opens a tunnel, never reaches the
agent check, and never reaches any `Fail()`. The owner gets a red
`RemoteException` / `NativeCommandError` blob — the exact opposite of D2's
"clear plain-language failure" (V3 line 51) and owner requirement 3. **D3-3 can
never pass**, so operational completion as defined in D3 is unreachable.

**Fix:** delete line 48. Its own comment says it is a no-op; it is, in fact, the
single fatal statement in the file.

### REQUIRED-2 — the agent-failure `Fail()` branch is unreachable in the case it exists for

`Open-BridgeDashboard.ps1:49–52`
```powershell
$agentList = & 'C:\Windows\System32\OpenSSH\ssh-add.exe' -l 2>&1
if ($LASTEXITCODE -ne 0) { Fail 'No key is loaded in ssh-agent. ...' }
```

Same mechanism (CASE-C above). `ssh-add` writes *connection* failures
(`Error connecting to agent: ...`, rc 2) to **stderr** — so in the "agent
running as a service but not usable" case the script dies with a raw exception
instead of calling the friendly `Fail()` two lines below. The `Get-Service`
preflight (lines 44–47) does not cover this: a Running service is not the same
as a reachable agent pipe.

Compounding: `ssh-add.exe` is invoked from a hard-coded literal path that is
**never preflighted**, while `ssh.exe` is (line 40). If it is absent,
`CommandNotFoundException` under `EAP = 'Stop'` produces the same raw crash.

**Fix:**
```powershell
$SshAdd = 'C:\Windows\System32\OpenSSH\ssh-add.exe'
if (-not (Test-Path -LiteralPath $SshAdd)) { Fail "Windows OpenSSH ssh-add not found at $SshAdd." }
$prevEAP = $ErrorActionPreference; $ErrorActionPreference = 'Continue'
$agentOut = & $SshAdd -l 2>&1
$agentRc  = $LASTEXITCODE
$ErrorActionPreference = $prevEAP
if ($agentRc -eq 2) { Fail 'The ssh-agent is running but cannot be reached. ...' }
if ($agentRc -ne 0) { Fail 'No key is loaded in ssh-agent. ...' }
```

### REQUIRED-3 — D2 claims a known_hosts **pin** preflight that the launcher does not perform

Plan V3 lines 51–52 claim the launcher preflights "known_hosts pin present".
`Open-BridgeDashboard.ps1:41` only tests that the **file exists**:

```powershell
if (-not (Test-Path -LiteralPath $KnownHosts)) { Fail "known_hosts not found ... the host key pin is missing." }
```

A `known_hosts` that exists but holds no entry for `152.239.123.231` passes this
check while the property it names is false — the self-confirming pattern exactly
(`SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md`, question: *what would make this
check fail?* Answer today: only deleting the whole file). The subsequent failure
surfaces as the generic line 75 message whose "usual causes" list does **not**
include "this host is not pinned", so the owner is pointed at the wrong problem
in the one scenario that must never be shrugged off.

**Fix** (verified working on this machine, non-ASCII profile path included —
`rc 0`, 3 key types matched):
```powershell
& 'C:\Windows\System32\OpenSSH\ssh-keygen.exe' -F $HostAddr -f $KnownHosts | Out-Null
if ($LASTEXITCODE -ne 0) { Fail "No pinned host key for $HostAddr in $KnownHosts. STOP and report - do not accept a new key." }
```
(guard it with the same `EAP` handling as REQUIRED-2).

### `Start-Process -NoNewWindow -PassThru` + `Wait-Process` — does it behave as claimed?

Partly. `-NoNewWindow` attaches `ssh.exe` to the same console, so a console close
(`CTRL_CLOSE_EVENT`) or `Ctrl+C` (`CTRL_C_EVENT`) reaches it and the default
handler terminates it — the common paths of "closing the window closes the
tunnel" (D2 line 55) do hold. `-PassThru` gives the real `ssh.exe` PID, so
`Stop-Process -Id $tunnel.Id` (line 87) and `Wait-Process -Id $tunnel.Id`
(line 97) target the right process.

But the binding is **by console signal only**: `Start-Process` creates no job
object, and there is no `try`/`finally`. Any termination of the PowerShell
process that does not deliver a console signal leaves `ssh.exe` orphaned with the
tunnel open. Asserted, not enforced → NIT-4 with the fix.

## Check 4 — D3 matrix soundness (what would make each row fail?)

| Row | Falsifiable? | What makes it go red | Assessment |
|---|---|---|---|
| D3-1 loopback-only listener | **Yes** | `ss -tln` shows `0.0.0.0:8790` or `[::]:8790` | Sound. Independently corroborated: `common.sh:30` pins `MTC_BIND_PORT=8790`, `app.py:288` binds `host="127.0.0.1"`, and `assert_loopback_only_source` (`common.sh:184–193`) statically greps the installed `app.py` for that exact bind. The unit's `ExecStart=python -m bridge.app` (first-start template line 34) reaches that `__main__` branch, so the claim holds for the deployed path, not just the repo. |
| D3-2 unreachable from the internet | **Yes**, weakly | a successful TCP connect from the operator PC, or a UFW rule naming 8790 | Sound but order-dependent → NIT-7 |
| D3-3 tunnel works | **Yes** | launcher fails | Sound as a row; **the artifact cannot pass it today** (REQUIRED-1) |
| D3-4 dashboard shows correct facts | **No — unprovable** | nothing; the fields do not exist | **REQUIRED-4** |
| D3-5 no live capability | **Weak** (absence of evidence) | a broker/exchange socket or `HL_LIVE_ACK` present | Strengthen → NIT-8 |
| D3-6 no button can ARM | **Yes**, but the spec admits a false pass | ARM succeeds / state leaves DISARMED | **REQUIRED-6** on the evidence spec; framing is correct → see below |

**D3-6 is correctly framed as a refusal proof, not an ARM grant.** V3 lines 70–71
say so explicitly ("executed exactly once, recorded, and is a refusal-proof — not
an ARM authorization. ARM remains forbidden"), and the row itself requires "state
remains DISARMED; no order/network side effect in logs". ✅ The framing passes.

**D3 is correctly deferred behind the separate first-start sentence.** V3 D3
header line 57 ("runs after the separately authorized first DISARMED start"),
§9 line 95–96 ("The dashboard verification matrix D3 runs only after my separate
first-start sentence"), and V2 §6 line 132–137 (first start is its own gate) are
consistent. ✅

### REQUIRED-4 — D3-4 asserts a capability the candidate bytes do not have

V3 D3-4 (line 66) proves the dashboard shows "host identity `srv1856225`,
candidate SHA `62bf661b…` (via `/api/status` fields rendered by the dashboard),
service health, last update time, **DISARMED** state".

Against the candidate at `C:\AUD62A`:

- `bridge/api/routes.py:25–48` — `/api/status` returns exactly `state`, `mode`,
  `network`, `exchange_conn`, `regime`, `state_version`, `reconcile_ready`,
  `window`. **No host identity. No release SHA. No last-update field.**
  (`window.last_alive_ts` is engine liveness, and in credential-free mode no
  engine is constructed — `app.py:149`.)
- `bridge/static/index.html:95–101` — the System page renders Network, DB,
  State Version only. `bridge/static/app.js` contains no `sha`, `release`,
  `host` or `last update` render target (grep: only `state_version` at line 127
  and `window.location.host` at line 240).
- A repo-wide grep of `routes.py` for `sha|release|host|version|uptime|build`
  returns only `state_version` lines.

So D3-4's host/SHA/last-update legs cannot be recorded from the dashboard, and
owner requirement 4 (dashboard shows correct host, candidate SHA, last update)
**cannot be met by the existing dashboard** — while D1 lines 30–31 forbid
redesign before first deployment. **D1 and D3-4/owner-req-4 are mutually
unsatisfiable as written.** This is the one finding that changes the plan's
meaning rather than its wording: "operationally complete only when every row
passes" (line 59) currently defines completion as impossible.

The DISARMED-state and part of the service-health legs **do** hold:
`app.py:138–148` sets `mode=credential_free_disarmed`, `network=disabled`,
`exchange_conn=disabled`, `exchange_enabled=false`, `credential_lookup=disabled`,
`arm_enabled=false`, and the dashboard renders state/mode/connection pills
(`index.html:22–25`).

**Fix — the plan must choose and say which:**
(a) re-scope D3-4 to what the existing dashboard can show (state, mode,
connection, network), and record host identity + release SHA + install time
out-of-band from `install_manifest.json` (written by `install.sh:412–422`) and
`hostnamectl`, flagging to the owner that requirement 4's "dashboard shows" is
being met by the deployment record rather than the UI; **or**
(b) admit a minimal `/api/status` addition (release SHA + host + start time) plus
one dashboard tile as a **candidate change**, which carries its own tier
acceptance and is therefore not a "no redesign" path. Option (a) preserves
D1 and the schedule; option (b) satisfies the owner's words literally. Either is
defensible — asserting the capability exists is not.

### REQUIRED-6 — D3-6's evidence spec admits a pass that proves nothing

In `routes.py`, `_require_confirm` (line 89) runs **before** the credential-free
guard (line 90–97). An ARM request with a missing or stale `X-Confirm` header is
refused at line 236–238 with `409 "stale state_version"` — a refusal that says
nothing about credential-free mode. D3-6 records only "application-level refusal
… recorded", which that outcome satisfies.

This matters because the guard is load-bearing: in credential-free mode the
engine is `None` (`app.py:149`), so if lines 90–97 were removed, ARM would fall
through to `routes.py:105–106` `_set_state(request, "ARMED")` and persist an
ARMED app_state. A test that cannot distinguish the two worlds is decorative.

**Fix:** require the recorded evidence to be (i) the dashboard's own ARM button
press — `app.js:272` sends `X-Confirm = state_version` (line 263), so the request
is well-formed by construction — and (ii) HTTP **409** with the exact detail
string `ARM unavailable in credential-free DISARMED start mode; exchange access
is disabled`, and (iii) `/api/status` before and after showing `state=DISARMED`
with an unchanged `state_version`.

## Check 5 — §9 sentence scope

Every exclusion the kickoff names is present in V3 §9 (lines 89–97):

| Required property | Present? |
|---|---|
| Names V3, not V2 | ✅ line 91–92 |
| V2 stages 3–5 only | ✅ line 92 "V2 stages 3–5 carried unchanged" |
| §0 tenancy boundary only | ✅ line 92 |
| No service start / no enable | ✅ line 93 |
| No secret | ✅ line 93 |
| No firewall change | ✅ line 93 |
| No TESTNET/mainnet, no broker, no ARM, no orders | ✅ lines 93–94 |
| No action on reserved Hermes/web identities | ✅ line 94 |
| **No public exposure of 8790 ever** | ✅ line 95 (new in V3) |
| D3 deferred to the separate first-start sentence | ✅ lines 95–96 |
| Failed attempt stops and reports; **retry needs a new sentence** | ✅ lines 96–97 |

Scope is exact. One structural defect:

### REQUIRED-7 — the authorization sentence delegates its own scope to a document V3 declares superseded

V3 line 3–4: "**SUPERSEDES V2**". V3 line 14: V2's sections are "carried…
(by reference, still binding)". V3 §9 line 92: authorizes "V2 stages 3–5 carried
unchanged". A superseded document is not normally live authority, so the sentence
points at text with no formal standing — and V3 never restates what stages 3–5
*are*. V2's own §9 did enumerate them ("transfer, dry run, one bounded install,
read-only verification, and Bridge-scoped operational evidence", V2 lines
183–185); V3's does not. The owner is non-technical; the single sentence he signs
is the whole authorization instrument, and as written he cannot see its scope
without opening a document V3 tells him is superseded.

**Fix:** (a) change the header to "V3 **incorporates** V2 §0–§8 by reference;
V2 has no independent authority", and (b) restore the enumeration inside the §9
sentence: "…per plan V3 (transfer, dry run, one bounded install, read-only
verification and Bridge-scoped operational evidence, as carried from V2 §3–§5)…".

## Check 6 — host-fact fit and command fidelity for what V3 changed or added

Verified against the live inventory and the candidate's own assets. Every new or
changed claim in V3 was checked against code, not prose.

| V3 claim | Evidence | Fit |
|---|---|---|
| Candidate "already ships the dashboard: `bridge/static/index.html`, served at `/`" (D1 lines 27–29) | `app.py:221–226` mounts `/static` and serves `index.html` at `/`; the file exists (4366 B) with `app.css` + `app.js` | ✅ |
| "all on the loopback-only listener `127.0.0.1:8790`" (D1 line 29) | `app.py:288` `uvicorn.run(..., host="127.0.0.1", port=8790)`; reached because the unit runs `python -m bridge.app` (first-start template line 34); `common.sh:30` `MTC_BIND_PORT="8790"`; `assert_loopback_only_source` (`common.sh:184–193`) greps the installed file for that exact bind | ✅ |
| Control endpoints `/api/arm`, `/api/disarm`, `/api/kill`, `/api/config` exist (D1 lines 37–38) | `routes.py:87`, `110`, `121`, `73` | ✅ (NIT-9) |
| ARM refused at application level in credential-free DISARMED mode (D3-6) | `routes.py:90–97` raises `409` when `app.state.credential_free_disarmed`; set by `app.py:137` from `resolve_start_mode` (`app.py:35–52`); pinned in the unit at `Environment=MTC_BRIDGE_START_MODE=credential_free_disarmed` (template line 42). Belt and braces: `app.py:149` never builds a broker in this mode, and `app.py:115–116` refuses a broker argument outright | ✅ |
| install.sh / verify.sh / rollback.sh semantics match the plan | `install.sh:16,20–21` (masked, never started/enabled/armed), `:365` `systemctl mask`, `:370–378` asserts masked + not active + not enabled, `:246,433` "NO firewall change"; `verify.sh:239–250` read-only assertions incl. `assert_control_port_closed`, `assert_no_public_control_listener`, `assert_ufw_ssh_only`; `rollback.sh:11,17–20` stop+mask, never unmask/start, never delete `/var/lib/mtc-bridge` | ✅ |
| verify.sh failures actually fail | Checked the `|| true` suffixes on lines 239–250 — they only defeat `set -e`; each helper calls `fail`, which increments `MTC_FAILURES`, and `verify.sh:253–258` exits 1 when non-zero. **Not** a swallowed assertion | ✅ (checked because it looked like one) |
| Launcher host/user/port facts | `152.239.123.231` / `baris` (inventory lines 12–16); 8790 loopback (above); `known_hosts` pin genuinely present, 3 key types (local `ssh-keygen -F`, rc 0) | ✅ |
| "no host-wide security change"; UFW untouched | `install.sh` calls only `assert_ufw_ssh_only` (read-only, `common.sh:155–181`); host has UFW active, default-deny, 22/tcp only (inventory lines 32–34) | ✅ |

## NITs

1. **N-1** `Open-BridgeDashboard.ps1:49` — `$agentList` is captured and never
   used; and the rc-2 case (agent unreachable) is reported with the rc-1 message
   "No key is loaded in ssh-agent", which misdirects the owner. Split the two.
2. **N-2** Agent-only authentication is asserted, not enforced. D2 line 47–48
   says "authentication ONLY from the owner-loaded ssh-agent"; the command
   (lines 60–69) passes no `-i`, but `ssh` still offers default on-disk
   identities (`~/.ssh/id_ed25519`, `id_rsa`, …) if present. No passphrase is
   ever stored either way, so the owner requirement holds in substance — but the
   stated property has no mechanism. Add `-o IdentitiesOnly=yes` (and, if the
   intent is strictly agent-only, `-o IdentityFile=none`).
3. **N-3** `Start-Process -ArgumentList` in PS 5.1 joins the array with spaces
   and does **not** quote elements. `-o "UserKnownHostsFile=$KnownHosts"`
   (line 65) survives today only because `C:\Users\BarışSemaay` has no space. One
   profile rename silently breaks the host-key pin argument. Quote the value.
4. **N-4** Tunnel lifetime is bound to the window by console signalling only
   (see check 3). Wrap the tail in `try { Wait-Process -Id $tunnel.Id } finally
   { Stop-Process -Id $tunnel.Id -Force -ErrorAction SilentlyContinue }` so
   normal script termination tears the tunnel down deterministically.
5. **N-5** Dashboard verification is status-code-only (lines 82–83): any 200 on
   `127.0.0.1:18790` satisfies it. Low risk given the port-free preflight, but
   D3-3 rests on it — assert a body marker, e.g.
   `<title>Crypto Paper Bridge</title>` (`index.html:6`).
6. **N-6** The retry loop (lines 80–85) sleeps only inside `catch`; a
   non-throwing non-200 spins five iterations with no delay. Cosmetic.
7. **N-7** D3-2 can pass while proving nothing if run when the service is not
   listening — a refused connection is the same observation either way. Require
   D3-2 to be executed **while D3-1's listener is confirmed live**, with both
   timestamps recorded in the same window.
8. **N-8** D3-5 rests on absence of evidence in logs. Cheap strengthening:
   assert `/api/status` shows `exchange_conn=disabled`, `exchange_enabled=false`,
   `credential_lookup=disabled`, `arm_enabled=false` (`app.py:139–148`), and that
   `ss -tnp` shows no outbound socket owned by `mtc-bridge`.
9. **N-9** D1's control-endpoint enumeration (lines 37–38) omits
   `/api/kill/ack` (`routes.py:133`) and the `/ws` WebSocket (`app.py:219`,
   `app.js:238–240`). The governing clause says "ANY Bridge endpoint", so the
   rule covers them; this is enumeration hygiene, and worth fixing because the
   list will be quoted into the future reverse-proxy work.
10. **N-10** D3 does not note that the dashboard's **DISARM** and **KILL**
    buttons stay live in credential-free mode and write persisted state
    (`routes.py:110–131` → `_set_state`), and that a KILL survives restart
    (`app.py:133` only re-asserts DISARMED when the stored state is not KILLED).
    No live economic action, so owner requirement 4 still holds — but the D3-6
    operator should be told not to press KILL, or the row should record
    `app_state` before and after.
11. **N-11** D3-6's parenthetical "(the Gate-A A-4-proven behavior)" (line 68)
    imports Gate-A language into KVM2 evidence.
    `BRIDGE_RELEASE_T0_ACCEPTANCE_2026-08-16.md` lines 54–56 bar transferring
    Gate-A A-0..A-9 off `2ce41e34`/GATEA-STAGING. The row's own proof is fresh,
    so this is wording — but this project has paid for that wording before.
    Suggest "(the behaviour Gate-A A-4 demonstrated on the *other* candidate;
    proven here independently)".
12. **N-12** D1's "the future website reverse proxy never proxies … ANY Bridge
    endpoint" has no mechanism today (nothing to enforce). Correct as a permanent
    rule; add a verify step to the future web-tenant plan so it is enforced
    rather than asserted when that tenant arrives.
13. **N-13** `Invoke-WebRequest` (line 82) honours the system proxy in PS 5.1.
    Loopback is normally bypassed, but a machine-wide proxy without a loopback
    exception would send the request off-box, contradicting "Contacts ONLY the
    pinned host" (script header line 15). Add `-Proxy $null` / an explicit
    bypass.

## Verdict

**REQUEST_CHANGES** — 7 REQUIRED, 13 NIT.

The plan's structure, tenancy boundary, gating discipline and §9 scope are sound,
and every V3 claim I could check against code checked out except the ones below.
Two of the seven REQUIRED findings are substantive rather than editorial:

- **REQUIRED-1** — the one-click launcher, one of the two pinned files under
  review, **aborts on its first executable statement on the only PowerShell
  installed on the owner's PC.** Confirmed empirically, not inferred. Owner
  requirement 3 is not met by this artifact, and D3-3 cannot pass.
- **REQUIRED-4** — D3-4 defines operational completion partly by facts the
  candidate's API and dashboard do not carry, while D1 forbids the redesign that
  would add them. As written, "complete only when every row passes" is
  unreachable.

The remainder (REQUIRED-2, 3, 6, 7) are one- to three-line repairs, and
REQUIRED-5 is a citation correction.

**Nothing found makes the §9 action unsafe.** Bootstrap stages 3–5 do not use the
launcher and do not depend on D3; the install path's safety properties (masked,
never started, never enabled, UFW untouched, Bridge-scoped rollback) are
implemented in the deploy scripts as the plan claims. The required repairs gate
*operational completion* and the *launcher*, not the installation. A plausible
disposition is to repair the launcher and the D3-4/D3-6 specs first — an hour of
work — since the §9 sentence should not be presented on bytes that a T0 pair has
just marked REQUEST_CHANGES.

---

*Reviewer: Claude slot, `claude-opus-5`. Read-only; no host or network contact;
launcher never executed. Both subject pins verified identical at start and end.*
