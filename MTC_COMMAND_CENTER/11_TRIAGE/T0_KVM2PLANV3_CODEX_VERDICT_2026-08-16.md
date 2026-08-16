# T0 Codex verdict — KVM2 deployment plan V3 + dashboard launcher

- Model identity reported by runtime/route: **OpenAI Codex `gpt-5.6-sol`**
- Effort: **xhigh**
- Review start (UTC+3): **2026-08-16 13:03:08 +03:00**
- Review stop (UTC+3): **2026-08-16 13:12:50 +03:00**
- Audit tier/slot: **T0, Codex flagship slot, fresh independent review**
- Execution boundary: read-only except this verdict. The launcher was not run. No SSH, host, browser, application server, or other network contact occurred. No credential was read. The only launcher execution-adjacent check was a local PowerShell AST parse, which returned zero syntax errors.

## Subject pins

Both subjects matched at review start and review end.

| Subject | Start | End |
|---|---|---|
| `C:\R7FINAL\MTC_COMMAND_CENTER\11_TRIAGE\KVM2_DEPLOYMENT_PLAN_62BF661B_V3_2026-08-16.md` | 6770 bytes; SHA-256 `065da2d513ad6c821e78a0977df5787be3b8d7550a87deadeb8f7afb34769fff` | 6770 bytes; SHA-256 `065da2d513ad6c821e78a0977df5787be3b8d7550a87deadeb8f7afb34769fff` |
| `C:\R7FINAL\MTC_COMMAND_CENTER\11_TRIAGE\KVM2_RUNKIT\Open-BridgeDashboard.ps1` | 4859 bytes; SHA-256 `9c9beaebcf73374588e3a1594760b613bbca5f04b66af75bf6329a13d96c2972` | 4859 bytes; SHA-256 `9c9beaebcf73374588e3a1594760b613bbca5f04b66af75bf6329a13d96c2972` |

## Verdict

**REQUEST_CHANGES**

There are **10 REQUIRED findings** and **0 NITs**. The package must not be presented for the §9 authorization sentence in its current form.

## REQUIRED findings

### REQUIRED-1 — The shipped dashboard cannot pass D3-4

V3 makes the existing dashboard completion-critical, forbids a pre-deployment redesign, and requires it to render host identity, candidate SHA, service health, last-update time, and DISARMED state (`KVM2_DEPLOYMENT_PLAN_62BF661B_V3_2026-08-16.md:28-31`, `:57-68`). The candidate does not expose or render most of those facts:

- Initial status contains state/mode/network/exchange/window facts but no host identity, deployed SHA, service-health field, or dashboard last-update timestamp (`bridge/api/routes.py:21-48`).
- Credential-free setup adds disabled-capability fields only (`bridge/app.py:135-148`), and `/api/status` returns that dictionary unchanged (`bridge/api/routes.py:62-67`).
- The existing System view renders only Network, DB, and State Version (`bridge/static/index.html:95-105`; `bridge/static/app.js:125-130`).

Therefore the required screenshot plus `/api/status` JSON cannot contain the asserted host/SHA/health/update facts. This is a deterministic completion blocker, not a future polish item. Repair requires a newly accepted candidate/dashboard surface or a revised owner-approved completion mechanism; the current exact candidate and “use as-is” plan cannot both satisfy the requirement.

### REQUIRED-2 — The launcher does not enforce agent-only authentication, an isolated target route, or the named pin store

The SSH command uses no explicit `-i`, which is good, but it does not disable the normal OpenSSH identity-file or configuration paths (`Open-BridgeDashboard.ps1:60-69`). OpenSSH can still consult default identity files and user/system configuration; configuration can add `IdentityFile`, `ProxyJump`, or `ProxyCommand`. Consequently:

- authentication is not proven to come **only** from the agent;
- a configured proxy/jump can contact a host other than the pinned destination, contrary to `Open-BridgeDashboard.ps1:15`; and
- system/global known-hosts sources can participate, so success is not restricted to the named user pin file.

The preflight only proves that `known_hosts` exists (`Open-BridgeDashboard.ps1:40-42`), not that it contains the expected host/fingerprint, and `ssh-add -l` proves only that at least one identity is loaded (`Open-BridgeDashboard.ps1:43-52`), not the intended KVM2 identity.

Use an audited Windows-compatible way to suppress ambient SSH configuration, disable identity-file authentication while retaining the agent, disable proxy/jump routing, disable alternate known-host stores, verify the exact public host-key pin, and—without reading a private key—verify the intended public agent fingerprint.

### REQUIRED-3 — Several promised launcher failure paths and tunnel cleanup paths are not reliable

The happy-path mechanics are sound: `Start-Process -NoNewWindow -PassThru` returns the SSH process and `Wait-Process` keeps the script attached on success (`Open-BridgeDashboard.ps1:70`, `:91-97`). `ExitOnForwardFailure=yes` is also present (`:66`). The failure contract is not sound:

- SSH has a 10-second connect timeout, but the script checks `HasExited` once after only three seconds (`Open-BridgeDashboard.ps1:67`, `:72-76`). A later authentication, host-key, connection, or forward failure falls into the HTTP loop and is mislabeled as “tunnel is up but dashboard did not answer” (`:78-89`).
- Failure to invoke `ssh-add.exe`, `Start-Process` for SSH, or `Start-Process` for the browser is a terminating PowerShell error under `$ErrorActionPreference = 'Stop'`, not a reachable `Fail()` branch (`:20`, `:49`, `:70`, `:93`).
- Tunnel cleanup exists only in the HTTP-failure branch (`:86-88`). There is no enclosing `try/finally` or equivalent lifetime owner, so an exception after SSH starts—most visibly browser-launch failure—can strand the child when the script is invoked from an existing PowerShell/Terminal window.

Windows OpenSSH `ssh-add -l` is fail-closed for the basic predicate: zero means identities were listed and nonzero means no usable list. But status 1 (no identities) and an agent communication/error status are collapsed into the same inaccurate “No key is loaded” diagnosis, and the command does not prove the intended key. The implementation must monitor SSH through the readiness loop, report its real exit/failure class, route all promised failures through a clear handler, and guarantee child cleanup on every exit path.

### REQUIRED-4 — The dry run does not print the complete mutating plan that V2 tells the operator to approve

V2 directs the operator to read the complete dry-run plan and confirm every mutation is inside the tenancy boundary (`KVM2_DEPLOYMENT_PLAN_62BF661B_V2_2026-08-16.md:82-93`). `COMMANDS.md:44-59` makes the same claim. In reality, `install.sh` reaches a special dry-run exit at `install.sh:235-247`, before the directory creation, release copy, venv creation/package installation, sealing, env-file installation, unit installation/mask, logrotate installation, and install-manifest write at `install.sh:252-429`.

Only prospective group/user calls and a summary are printed. The plan's pre-mutation inspection gate therefore cannot inspect most mutations it claims to cover. The dry-run path must traverse/emit every mutating action, or the plan needs a complete independently pinned action manifest that the operator can actually inspect before the one attempt.

### REQUIRED-5 — The deployment assets turn “SSH-only” into a permanent upgrade prerequisite and conflict with the multi-tenant requirement

V2 correctly says SSH-only is merely the present state and that 80/443 must remain available to the future website tenant (`KVM2_DEPLOYMENT_PLAN_62BF661B_V2_2026-08-16.md:29-33`). But `assert_ufw_ssh_only` fails on every non-SSH inbound ALLOW rule (`deploy/linux/lib/common.sh:155-180`), and both install and verification invoke it (`install.sh:235-243`, `:387-396`; `verify.sh:239-250`).

Once the authorized web tenant opens 80/443, the claimed repeatable Bridge install/upgrade verification path will fail. This violates owner multi-tenant items 6 and 12 (`OWNER_INSTRUCTIONS_KVM2_MULTITENANT_2026-08-16.md:43-48`, `:56-65`) and contradicts V2's reusable-upgrade promise (`KVM2_DEPLOYMENT_PLAN_62BF661B_V2_2026-08-16.md:152-176`). The invariant should be default-deny plus no rule/public path exposing Bridge 8790, not host-wide SSH-only forever.

### REQUIRED-6 — The resource protection is asserted, not enforced, and the 64 MiB log-cap claim is false

V2 says the Bridge budget is ≤1 GiB RAM/≤10 G disk, that monitoring is current “enforcement,” and that logs are capped at 64 MiB (`KVM2_DEPLOYMENT_PLAN_62BF661B_V2_2026-08-16.md:44-53`). The accepted unit has no `MemoryMax`, `MemoryHigh`, CPU quota, or other resource ceiling (`mtc-bridge-first-start.service.template:63-93`). Monitoring can report an overrun after it occurs; it cannot prevent one.

The logrotate policy's `size 64M` is a per-file rotation threshold, not a total cap, and it retains 30 generations for both matching log files (`deploy/linux/logrotate/mtc-bridge:13-25`). Current files can exceed the threshold between runs and retained data can be far above 64 MiB. This fails the self-confirming-check question and does not establish that Bridge cannot crowd future tenants. Correct the claims and add enforceable pre-start limits/retention consistent with the owner requirement, with the required candidate/unit re-acceptance if bytes change.

### REQUIRED-7 — D3-5 and part of D3-6 use application-controlled absence-of-log evidence as proof of no side effect

D3-5 treats “no broker/exchange connection attempt (logs)” as proof, and D3-6 treats “no order/network side effect in logs” as proof (`KVM2_DEPLOYMENT_PLAN_62BF661B_V3_2026-08-16.md:67-71`). An unlogged attempt or side effect makes the property false while these checks stay green. That is the exact self-confirming pattern described at `SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:45-63`.

The ARM-refusal core is valid: credential-free mode rejects a supplied broker and never builds one (`bridge/app.py:111-149`), and the ARM route returns HTTP 409 before engine/state action (`bridge/api/routes.py:87-108`). D3-6 is also correctly labeled a one-time refusal proof, not an ARM grant (`KVM2_DEPLOYMENT_PLAN_62BF661B_V3_2026-08-16.md:70-71`). Retain the 409 plus before/after DISARMED proof, but add an independent outbound/order-side-effect observation for D3-5/D3-6 rather than relying on the checked application to log its own violation.

### REQUIRED-8 — The planned rollback rehearsal has no executable input contract and is not a no-op

V2 schedules rollback rehearsal before its backup/restore item and calls it a no-op on the never-started masked unit (`KVM2_DEPLOYMENT_PLAN_62BF661B_V2_2026-08-16.md:110-120`). `rollback.sh` cannot run without an already existing, separately hashed state-manifest file (`rollback.sh:54-62`), but the plan supplies neither the file nor the exact command/values for this initial empty-state rehearsal. Even without a target release, the script writes or replaces `/etc/mtc-bridge/rollback_manifest.json` (`rollback.sh:157-180`), so it is not a no-op.

There is a second mismatch: an install failure is directed to §7 rollback (`KVM2_DEPLOYMENT_PLAN_62BF661B_V2_2026-08-16.md:103-108`), but the rollback script preserves/deletes nothing and may lack its mandatory manifest or installed unit after a partial install. Define exact, available rehearsal inputs, describe the write honestly, and provide an exact partial-install failure disposition inside the authorized boundary.

### REQUIRED-9 — `verify.sh` is not read-only as §4/§9 claim

V2 calls verification read-only (`KVM2_DEPLOYMENT_PLAN_62BF661B_V2_2026-08-16.md:100-107`), and §9 authorizes “read-only verification” (`KVM2_DEPLOYMENT_PLAN_62BF661B_V3_2026-08-16.md:89-97`). `verify.sh` creates an expected-unit file with `mktemp`, writes it, and deletes it (`verify.sh:188-197`). That is a host filesystem write/delete, normally under `/tmp`, outside the enumerated Bridge paths.

Either make the comparison genuinely read-only/in-memory or explicitly add the exact bounded temporary-write surface to the plan and authorization. The present bytes do not match the sentence's scope.

### REQUIRED-10 — The host fact record does not prove the venv prerequisite before the one mutating attempt

The inventory proves Python 3.12.3 and absence of system `pip3` (`KVM2_READONLY_INVENTORY_2026-08-16.md:42`), then says the venv bootstrap path should be confirmed (`:69-72`). Neither the inventory nor the dry run establishes that Ubuntu's `venv`/`ensurepip` support is installed. The dry run checks only that `python3.12` is a command and exits before attempting venv creation (`install.sh:133-135`, `:235-247`); the real attempt reaches `python3.12 -m venv` only after creating the identity, directories, and release tree (`install.sh:217-275`, `:280-310`).

On Ubuntu, the interpreter executable alone does not prove the separately packaged venv capability. Add a non-mutating preflight that proves the needed module/bootstrap support before any install mutation, otherwise a predictable prerequisite failure consumes the one attempt and leaves partial state.

## Required-check results

### 1. Owner dashboard requirements 1–11 plus item 12

The binding owner record groups the substance into eight numbered paragraphs; the kickoff requires twelve checks. The table below decomposes the combined paragraphs without dropping any substance.

| # | Result | Evidence |
|---|---|---|
| 1. KVM2 bind is `127.0.0.1:8790` only | PASS | V3 `:28-30`, `:35`; actual bind `bridge/app.py:281-288`. |
| 2. UFW never opens 8790 | PASS for initial plan | V3 `:33-38`; installer changes no rule and checks 8790, but REQUIRED-5 rejects the broader SSH-only predicate. |
| 3. Future reverse proxy exposes no dashboard/control endpoint | PASS as a binding plan rule | V3 `:35-39`, `:79-84`. Future implementation remains separately T0-gated. |
| 4. Operational completion waits for separate first DISARMED start and secure Windows access | PASS | V3 `:57-59`, `:89-97`. |
| 5. Use the existing dashboard first; no redesign delay | PLAN PRESENT, IMPLEMENTATION INSUFFICIENT | V3 `:28-31`; REQUIRED-1 shows the existing dashboard cannot meet the facts requirement. |
| 6. One-click pinned tunnel opens the browser | PARTIAL / REQUIRED | Intended at V3 `:41-55`; launcher `:58-97`; REQUIRED-2 and REQUIRED-3. |
| 7. No stored password/passphrase; authentication only from loaded agent | Password/passphrase storage PASS; agent-only MISSING | Launcher `:22-29`, `:43-52`, `:60-69`; REQUIRED-2. |
| 8. Strict host-key pin and clear auth/forward/local-port failures | PARTIAL / REQUIRED | Strict and forward options exist at launcher `:63-67`; pin presence and several failure paths are not established (REQUIRED-2/3). |
| 9. Prove loopback-only, internet-unreachable, and owner-PC tunnel success | PRESENT, partly dependent on launcher repair | V3 D3-1..D3-3 at `:61-65`; see D3 analysis below. |
| 10. Dashboard shows host, SHA, service health, update time, DISARMED | **MISSING in candidate** | V3 `:66`; candidate evidence in REQUIRED-1. |
| 11. Network/exchange/live order disabled; no button can ARM/create economic action | Application refusal PASS; operational proof PARTIAL / REQUIRED | V3 `:67-71`; `bridge/app.py:111-149`; `bridge/api/routes.py:87-108`; REQUIRED-7. |
| 12. Immediate Dashboard V2 work package queued with read-only/control split and tier split | PASS | `NEXT_STEPS.md:18-37`; V3 `:73-85`. |

The owner instruction grants no execution authority, and V3 preserves that boundary (`OWNER_REQUIREMENT_DASHBOARD_2026-08-16.md:47-50`; V3 `:3-12`).

### 2. Multi-tenant requirements carried through V2

| Owner item | Result | Evidence |
|---|---|---|
| 1. Install no Hermes/web now | PASS | V2 `:11-20`. |
| 2. Bridge self-contained | PASS | V2 `:21-28`; installer layout `deploy/linux/lib/common.sh:8-30`. |
| 3. No global Python/shared app dirs | PASS | V2 `:27-28`; per-SHA venv `install.sh:280-310`. |
| 4. Reserve separate identities/locations | PASS | V2 `:15-20`. |
| 5. 8790 loopback; no future proxy | PASS | V2 `:17`; V3 `:33-39`. |
| 6. 80/443 stay usable; SSH-only not permanent | **FAIL** | V2 says this at `:29-33`; assets contradict it (REQUIRED-5). |
| 7. No host-wide security change blocking future services | PASS for mutation scope; compatibility caveat | No firewall/kernel/PAM/sysctl/AppArmor/Docker change at V2 `:29-33`; REQUIRED-5 still blocks later operation after 80/443 are opened. |
| 8. Service-specific backup/monitor/logrotate/rollback | PASS in declared scope | V2 `:34-36`, `:110-127`, `:141-150`; exact rehearsal is blocked by REQUIRED-8. |
| 9. Rollback/removal never touches future tenant assets | PASS as an explicit prohibition | V2 `:141-150`. |
| 10. Resource headroom protects future tenants | **FAIL** | V2 `:44-53`; REQUIRED-6. |
| 11. Compromise isolation | CONDITIONAL, not disproved here | Dedicated identity, 0750 tenant homes, strict unit, and only two writable Bridge paths are stated at V2 `:37-42`; unit `:63-93`. Future tenant permissions must be reverified as V2 requires. |
| 12. Reusable upgrade; no repeat bootstrap | **FAIL as an end-to-end procedure** | Side-by-side design exists at V2 `:152-176`, but any authorized future 80/443 rule makes its mandatory install/verify path fail (REQUIRED-5). |

The multi-tenant requirement set is therefore **not fully satisfied**.

### 3. Launcher line-by-line security/correctness result

- Agent-only auth: **FAIL** — REQUIRED-2. No explicit key is passed, but ambient config/default identity files remain possible.
- Password/passphrase storage or display: **PASS** — none is stored or printed; BatchMode prevents interactive password/passphrase prompting (`Open-BridgeDashboard.ps1:22-29`, `:60-69`).
- Strict host key / pinned store: **PARTIAL** — options are present, but exact pin presence and exclusive stores are not proven (REQUIRED-2).
- `ExitOnForwardFailure`: **PASS** (`Open-BridgeDashboard.ps1:66`).
- Local bind: **PASS** — explicit `127.0.0.1:18790` (`:27-29`, `:61-63`).
- `ssh-add -l` exit-code logic: **fail-closed but incomplete diagnosis** — REQUIRED-3.
- `Start-Process -NoNewWindow -PassThru` plus `Wait-Process`: **PASS on the normal path**; it starts the SSH child in the current console, exposes a process object, and waits. Error-path ownership is **FAIL** — REQUIRED-3.
- Clear failure paths: **FAIL** — only some branches reach `Fail()`; timing misclassifies several SSH failures (REQUIRED-3).
- No secret printed: **PASS**.
- No other network contact: **FAIL as an enforceable claim** — ambient SSH proxy/jump config is not suppressed (REQUIRED-2). The script's explicit web request itself targets loopback only (`:78-89`).
- Tunnel lifetime bound to the window: **PARTIAL** — normal same-console close is consistent with the design, but exceptions can strand the child and no cleanup owner covers every exit (REQUIRED-3).

### 4. D3 falsifiability matrix

| Row | Result | Concrete red condition / analysis |
|---|---|---|
| D3-1 | PASS as falsifiable | Red if 8790 is absent, has more than the exact loopback listener, or appears on wildcard/public IPv4/IPv6. `ss -tln` is independent of the app's status report. |
| D3-2 | PASS only in combination with D3-1 | Red if the external connection succeeds or a UFW exposure is present. One operator-PC probe alone is not global proof, but the host listener proof closes the direct-listener gap. Future reverse-proxy non-exposure remains a separately T0-gated configuration obligation. |
| D3-3 | Falsifiable but method currently defective | Red if the launcher cannot obtain HTTP 200/open the browser. REQUIRED-2/3 must be repaired before its success is accepted as secure tunnel proof. |
| D3-4 | **Cannot pass on current candidate** | REQUIRED-1. Missing host/SHA/health/update facts make the expected evidence unavailable. |
| D3-5 | **Self-confirming / REQUIRED** | It goes red on a logged attempt or present `HL_LIVE_ACK`, but stays green for an unlogged attempt. Add independent egress/connection observation (REQUIRED-7). |
| D3-6 | Refusal core PASS; side-effect clause REQUIRED | Red on anything other than application HTTP 409, any state transition away from DISARMED, or an independently observed order/egress effect. The exact-once check is explicitly not ARM authority. Application-log absence alone is not proof (REQUIRED-7). |

D3 is correctly deferred until after the separate first-start sentence (`KVM2_DEPLOYMENT_PLAN_62BF661B_V3_2026-08-16.md:57`, `:89-97`).

### 5. §9 sentence scope

**PASS on wording, subject to the findings that make the referenced procedure inaccurate.** The sentence is limited to V2 stages 3–5 inside the Bridge tenancy boundary, excludes start/enable/secrets/firewall/TESTNET/mainnet/broker/ARM/orders/reserved tenants/public 8790, defers D3 until a separate first-start sentence, and requires a new sentence after failure (`KVM2_DEPLOYMENT_PLAN_62BF661B_V3_2026-08-16.md:87-97`). It grants neither D3 nor first-start authority. REQUIRED-4, REQUIRED-8, REQUIRED-9, and REQUIRED-10 must be repaired so the referenced stages actually fit those words.

### 6. Host-fact fit and command fidelity

- Host identity/IP, clean Bridge state, UFW default-deny/SSH-only current state, resources, Python 3.12.3, and absent system pip agree between V2 and inventory (`KVM2_READONLY_INVENTORY_2026-08-16.md:12-17`, `:19-46`; V2 `:44-64`).
- Candidate acceptance is correctly identified and grants no deployment/start/economic authority (`BRIDGE_RELEASE_T0_ACCEPTANCE_2026-08-16.md:3-18`, `:47-58`).
- The application really serves `bridge/static/index.html` at `/` and binds `127.0.0.1:8790` (`bridge/app.py:218-228`, `:258-288`). D1's control routes exist (`bridge/api/routes.py:69-151`). Credential-free ARM is refused before engine action (`bridge/api/routes.py:87-108`), and credential-free creation refuses a broker and leaves network/exchange/ARM disabled (`bridge/app.py:111-149`).
- Installer no-start/no-enable/no-firewall-mutation semantics generally match, and the masked unit is installed at `install.sh:343-379`. The complete-dry-run claim does not match (REQUIRED-4), the UFW predicate does not fit future tenancy (REQUIRED-5), and the host venv prerequisite is not established (REQUIRED-10).
- `verify.sh` checks the masked/unstarted/closed-port state, but it is not literally read-only (REQUIRED-9) and permanently enforces SSH-only (REQUIRED-5).
- `rollback.sh` stops/masks and preserves state, but the initial rehearsal/failure procedure lacks its mandatory inputs and is not a no-op (REQUIRED-8).

## Final acceptance statement

**REQUEST_CHANGES.** Do not execute the launcher, do not present §9, and do not contact KVM2 on the strength of this package. The exact end pins still match the start pins, but the plan/launcher require a T0 repair and fresh review within the governing round cap.
