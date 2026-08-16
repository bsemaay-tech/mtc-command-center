# T0 round-2 Codex verdict — Plan V4 + launcher v2 + replacement candidate `be689537`

| Field | Value |
|---|---|
| Model identity reported by runtime/route | **OpenAI Codex `gpt-5.6-sol`** |
| Effort | **xhigh** |
| Audit slot | **T0 Codex flagship slot, round 2 of the un-reset Plan-V3 cap (3)** |
| Session | **Fresh, independent, adversarial**; no state from the quota-failed attempt was available or used |
| Working directory | `C:\AUD62B` |
| Start (UTC+3) | **2026-08-16 14:14:43 +03:00** |
| Stop (UTC+3) | **2026-08-16 14:30:58 +03:00** |
| **VERDICT** | **REQUEST_CHANGES — 7 REQUIRED, 1 NIT** |

## Execution boundary

Read-only everywhere except this verdict and disposable scratch under
`C:\tmp\codex_t0_v4_d026_20260816_1421`. I did not execute the launcher or any
deployment script, contact KVM2 or any other host, open SSH/network/browser
sessions, mutate Git state, read an existing credential/private key, or
sub-delegate. The only SSH invocation was local `ssh -G`, which evaluates
configuration without connecting. A disposable audit-only key was generated in
the scratch directory solely to test whether `ssh-keygen -lf` accepts private
material stored under a `.pub` name.

## Subject pins — start and end

All three subjects matched at start and end. No pin STOP occurred.

| Subject | Start | End |
|---|---|---|
| Plan V4: `C:\R7FINAL\MTC_COMMAND_CENTER\11_TRIAGE\KVM2_DEPLOYMENT_PLAN_V4_2026-08-16.md` | 7676 B; SHA-256 `c2339ea0d41f921e3174b9f82bbbe07554649e69453447decf307999c9796ae0` | identical |
| Launcher v2: `C:\R7FINAL\MTC_COMMAND_CENTER\11_TRIAGE\KVM2_RUNKIT\Open-BridgeDashboard.ps1` | 9008 B; SHA-256 `e6e8bfa4217b05b0b134018175c082186b6fcbcb5c66d0cfbfa7ed84c2e1675c` | identical |
| Candidate in `C:\AUD62B` | HEAD `be68953787c299bdaf30f83f301aa66a8ec0ea1f`; tree `4ff9a5cfb744ba0440b8580d2d7f9dc70b81a69f`; parent `62bf661b065dec5b5d9895d83575581fe369252d`; local `integration/bridge-release-20260815` ref at HEAD; clean | identical; clean |

## REQUIRED findings

### REQUIRED-1 — `assert_ufw_bridge_safe` still admits an inbound ALLOW that exposes 8790

The repaired predicate recognizes an exposed Bridge port only when UFW's first
column equals `8790` or begins `8790/`
(`IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh:157-185`, specifically
`:179-181`). A valid range rule is rendered as `8790:8800/tcp`; it contains the
Bridge port but matches neither branch.

I sourced the real candidate function in disposable scratch and supplied this
UFW status fixture:

```text
Status: active
Default: deny (incoming), allow (outgoing), disabled (routed)
22/tcp ALLOW IN Anywhere
8790:8800/tcp ALLOW IN Anywhere
```

Real result:

```text
PASS  ufw active, default-deny incoming; SSH port 22 allowed; Bridge port 8790 not exposed
RC=0
```

The new parametrized regression covers exact `8790/tcp`, future 80/443, and
missing SSH only (`tests/test_linux_deployment.py:273-334`). It does not cover
range/application-profile/unmodelled ALLOW grammar. Codex round-1 R5 is
**NOT-CLOSED**. Repair must fail closed over every UFW ALLOW representation that
can include 8790, including ranges; unmodelled rule grammar must STOP/FAIL, not
disappear.

### REQUIRED-2 — V4 retires the old candidate but still incorporates executable commands pinned to it

V4 incorporates V2 sections 0-8 as binding (`KVM2_DEPLOYMENT_PLAN_V4_2026-08-16.md:3-5`), declares all identities re-pinned (`:12-22`), and says the
`62bf661b` payload/pins must not be installed (`:22`). But incorporated V2 still
contains the only exact transfer/install/verify commands, all naming
`C:\tmp\payload-62bf661b`, release `62bf661b...`, and manifest
`1078ac22...` (`KVM2_DEPLOYMENT_PLAN_62BF661B_V2_2026-08-16.md:82-100`).

V4 gives the replacement release and manifest hashes but no replacement payload
path and no exact stage-1/stage-2 commands. Following the incorporated commands
violates V4; manually substituting values is not an exact executable plan. This
is a fresh command-fidelity blocker. Restate the complete transfer, dry-run,
install, and verify commands with the `be689537...` payload path, release SHA,
and `58705d...` manifest pin, and explicitly override the old V2 command block.

### REQUIRED-3 — D3-5/D3-6 independent side-effect evidence remains self-confirming

V4 replaces pure application-log absence with three point-in-time `ss -ntu`
captures plus `journalctl` (`KVM2_DEPLOYMENT_PLAN_V4_2026-08-16.md:26-43`). The
mechanism still cannot establish the claim:

- `ss -ntu` omits process/UID/cgroup ownership, so it cannot identify a socket as
  originating from the Bridge service;
- a short connection between the three captures leaves every capture green;
- `journalctl -u` is still the checked service's own logging surface; and
- no independent order/store observation proves the ARM attempt created no
  order-side effect.

The exact dashboard-generated confirm header, exact credential-free 409 detail,
and unchanged before/after state are good repairs (`:30-36`). The independent
side-effect leg is not. Codex R7 is **NOT-CLOSED** and Claude R6 is
**PARTIALLY-CLOSED**. Specify a continuous, host-independent observation
attributed to the service for the whole attempt window, plus an independent
before/after order/persistence check.

### REQUIRED-4 — The rollback rehearsal still has no executable input/command contract and is ordered before its prerequisite

V4 says the mandatory state-manifest input will be a hash record produced during
the V2 §5.3 backup and that the exact command will be recorded later
(`KVM2_DEPLOYMENT_PLAN_V4_2026-08-16.md:45-51`). V2, however, orders rollback as
stage-3 item 1 and backup as item 3, and its backup text defines no rollback
state-manifest file (`KVM2_DEPLOYMENT_PLAN_62BF661B_V2_2026-08-16.md:110-120`).

The actual script requires both an existing exact file and its SHA before any
rehearsal can run:

```text
--state-manifest-file <file> --state-manifest-sha256 <64-hex>
```

(`IBKR_PAPER_BRIDGE/deploy/linux/rollback.sh:24-27,54-62`). V4 supplies neither
the creation command/format/path nor the rollback command, and points to an
artifact produced two numbered steps later. Promising to record a command at
execution time is self-produced evidence, not a reviewed input contract. Codex
R8 is **NOT-CLOSED**. Reorder the steps and provide the exact manifest-generation
and rollback commands, paths, and hash handoff in the plan.

### REQUIRED-5 — The resource repair still states a false log-retention bound

The unit now genuinely contains `MemoryHigh=768M` and `MemoryMax=1G`
(`mtc-bridge-first-start.service.template:60-61`). The disk/log statement is
not honest. The policy uses daily `copytruncate`, seven generations, and
`maxsize 64M` (`deploy/linux/logrotate/mtc-bridge:8-24`). If an active log grows
past 64 MiB between invocations, the next invocation rotates the whole oversized
file; that file then remains among the seven retained generations. Therefore
V4's “policy-bounded retention ≈ 1 GiB worst case at rotation points” claim
(`KVM2_DEPLOYMENT_PLAN_V4_2026-08-16.md:69-76`) is false. The worst case remains
unbounded after a rotation, not merely until the next invocation.

Codex R6 is **PARTIALLY-CLOSED**: the RAM limit is real, but the log/disk bound
is not, and the ≤10 GiB disk budget remains monitoring rather than prevention.
Either state only a nominal threshold calculation with no worst-case bound, or
add an actual hard disk/log ceiling consistent with owner multi-tenant item 10.

### REQUIRED-6 — Three sampled regression arms fail mandatory D026 falsification

I tested four of the eleven new/extended arms in independent candidate copies
outside the repository. One positive control worked; three equivalent defect
mutations stayed green:

| Arm | Deliberate equivalent mutation | Real result | D026 result |
|---|---|---|---|
| status identity/health/timestamps (`tests/test_api.py:47-74`) | renamed produced `host_identity` to `host_identity_mutated` | `KeyError: 'host_identity'`; **1 failed**, rc 1 | **Verified RED** |
| complete dry-run mutation manifest (`tests/test_linux_deployment.py:212-263`) | added an unlisted real `run install ... /opt/hermes` mutation | **1 passed**, rc 0 | **FAILED falsification** |
| read-only verifier (`tests/test_linux_deployment.py:846-865`) | added `printf ... > /tmp/codex-verifier-mutation` to `verify.sh` | **1 passed**, rc 0 | **FAILED falsification** |
| active memory ceilings (`tests/test_linux_deployment.py:339-352`) | commented out both `MemoryHigh=768M` and `MemoryMax=1G` | **1 passed**, rc 0 | **FAILED falsification** |

The dry-run test compares the plan IDs to its own hand-maintained
`real_mutations` dictionary, so a mutation absent from both declarations is
invisible. The verifier test rejects only a small known list of writes. The unit
test searches raw substrings and therefore accepts commented-out settings.

Under D026 these tests are supplemental, not closure evidence. The implementation
report's blanket claim that every new/extended arm has valid RED/GREEN evidence
(`RIC1_IMPLEMENT_REPORT_2026-08-16.md:141-151`) does not survive mutation.
Codex R4, R6, and R9 are at best **PARTIALLY-CLOSED** until independent tests are
made to fail on these exact mutations and real RED/GREEN transcripts are
recorded.

### REQUIRED-7 — Launcher v2 has a private-key read path under its “public file only” preflight

The launcher trusts the filename `hostinger_kvm2.pub`, checks only that it is a
leaf, then passes it to `ssh-keygen -lf` (`Open-BridgeDashboard.ps1:15,107-108,132-142`). It never verifies that the content is public-key material before invoking a parser that accepts private keys.

In disposable scratch I generated an audit-only encrypted Ed25519 private key
directly at a filename ending `.pub` and ran the launcher's same fingerprint
operation. Real result:

```text
ssh-keygen -lf <private-file-named-.pub> -E sha256
RC=0
256 SHA256:... disposable-audit-key-2 (ED25519)
```

Thus a misplaced/replaced private key at the configured path is opened and read,
contrary to the launcher lines 3-5/23 and V4's “public file only” claim
(`KVM2_DEPLOYMENT_PLAN_V4_2026-08-16.md:20`). No private bytes are printed, but
the hard exclusion is “not read,” not merely “not displayed.” Codex R2 and Claude
R2 are **PARTIALLY-CLOSED**. Prefer removing this file read entirely and pinning
the expected public fingerprint literal against `ssh-add -l` output.

## NIT

### NIT-1 — Intended key presence is not intended key selection

Local non-connecting `ssh -G` reproduced the intended isolated configuration
(`-F NUL`, `IdentityFile=NUL`, global store NUL, named user store, proxy disabled,
strict checking), but also reported `identitiesonly no`. The launcher proves the
intended fingerprint is among loaded agent keys; SSH may still authenticate with
another loaded agent key. The owner requirement only requires agent-based auth,
so this is optional hardening rather than a separate required repair.

## Per-finding round-1 closure

### Codex R1-R10

| Round-1 finding | Closure | Mechanism result |
|---|---|---|
| R1 D3-4 facts absent | **CLOSED** | API fields at `routes.py:35-37,262-274`; System renderers at `app.js:129-133`/`index.html:101-105`; status mutation control went RED. |
| R2 launcher agent-only/isolation/pins | **PARTIALLY-CLOSED** | Ambient config/default identity/global trust/proxy paths are closed and intended fingerprint presence is checked; REQUIRED-7 leaves a private-key read path. |
| R3 launcher failure/cleanup | **CLOSED** | Child monitored through readiness and after wait; tunnel/browser failures caught; child owned by `try/finally` (`Open-BridgeDashboard.ps1:175-224`). AST errors = 0. |
| R4 complete dry run | **PARTIALLY-CLOSED** | Current 31-item manifest appears to enumerate current real mutations (`install.sh:219-274`), but its offered D026 test stayed green for an unlisted `/opt/hermes` mutation (REQUIRED-6). |
| R5 multi-tenant UFW predicate | **NOT-CLOSED** | Range exposure false-pass reproduced on the real candidate function (REQUIRED-1). |
| R6 resource/log protection | **PARTIALLY-CLOSED** | RAM ceilings real; log worst-case claim false and unit regression is non-falsifying (REQUIRED-5/6). |
| R7 independent no-side-effect evidence | **NOT-CLOSED** | Point-sampled unattributed sockets plus service logs remain self-confirming (REQUIRED-3). |
| R8 rollback rehearsal inputs/disposition | **NOT-CLOSED** | Write and partial-install disposition are acknowledged, but exact prerequisite generation/command is absent and ordered later (REQUIRED-4). |
| R9 verifier read-only | **PARTIALLY-CLOSED** | Current mechanism contains no identified persistent write, but mandatory regression evidence stayed green after a real `/tmp` write (REQUIRED-6). |
| R10 venv prerequisite | **CLOSED** | `import venv, ensurepip` with bytecode disabled runs before the first target mutation (`common.sh:61-68`; `install.sh:130-135,286`). |

### Claude R1-R7

| Round-1 finding | Closure | Mechanism result |
|---|---|---|
| R1 EAP/native warmup fatal | **CLOSED** | Warmup removed; native calls use `Invoke-NativeCapture` with real rc capture (`Open-BridgeDashboard.ps1:28-55`). |
| R2 agent error branch/binary/intended key | **PARTIALLY-CLOSED** | rc 1/2 split and binary preflight are real (`:99-125`); intended fingerprint is checked, but REQUIRED-7 violates the public-only premise. |
| R3 known_hosts file-only check | **CLOSED** | Real `ssh-keygen -F <host> -f <store>` preflight at `:127-130`; isolated trust options parse successfully. |
| R4 D3-4 capability absent | **CLOSED** | Same status/UI mechanism as Codex R1. |
| R5 citation mismatch | **CLOSED** | V4 correctly separates dashboard owner items 1-8 from multi-tenant §2 items 1-12 (`KVM2_DEPLOYMENT_PLAN_V4_2026-08-16.md:58-63`), verified against both named owner records. |
| R6 stale-confirm refusal can pass | **PARTIALLY-CLOSED** | Exact current-confirm 409 plus unchanged state is fixed; independent side-effect evidence is still inadequate (REQUIRED-3). |
| R7 authority delegated to superseded V2 | **CLOSED** | V4 formalizes incorporation/no independent authority and §9 enumerates its action scope (`KVM2_DEPLOYMENT_PLAN_V4_2026-08-16.md:3-5,65-67,82-96`). REQUIRED-2 is a separate stale-command fidelity defect. |

## Candidate delta scope and protected surfaces

`git diff --stat 62bf661b..be689537` matched exactly:

```text
11 files changed, 350 insertions(+), 77 deletions(-)
```

The exact changed-file list is the eleven files claimed in
`RIC1_IMPLEMENT_REPORT_2026-08-16.md:190-212`; no unlisted file changed.
Explicit directory diffs confirmed engine, store, and broker byte-identical.
No Pine, parity, `MTC_V2`, trading strategy, order, risk, or broker implementation
byte changed. The dashboard delta is limited to the owner-approved status facts
and rendering; the other eight production/test files correspond to reproduced
non-dashboard deployment repairs. Scope check: **PASS**.

## Full suite — independently executed

Command from `C:\AUD62B`:

```powershell
$env:PYTHONUTF8='1'; $env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest -q -p no:cacheprovider IBKR_PAPER_BRIDGE/tests
```

Real final line:

```text
1367 passed, 1 warning in 175.75s (0:02:55)
```

The warning was the existing Starlette/httpx deprecation warning. Exit code 0.
`git status --porcelain` was empty immediately afterward and at the final pin.

## Plan §2 six-item repair result

| V4 item | Result |
|---|---|
| 2.1 D3-5/D3-6 independent evidence | **NOT REPAIRED** — REQUIRED-3 |
| 2.2 rollback inputs/write/partial-install disposition | **PARTIAL** — write/disposition honest; exact executable input and ordering absent (REQUIRED-4) |
| 2.3 citation hygiene | **REPAIRED** |
| 2.4 authority structure / self-contained §9 scope | **REPAIRED**; stale incorporated commands are a separate REQUIRED-2 |
| 2.5 honest resource wording | **NOT REPAIRED** — REQUIRED-5 |
| 2.6 D3-4 capability on new bytes | **REPAIRED** |

## Final acceptance statement

**REQUEST_CHANGES.** The candidate suite and scope checks pass, but the package
has reproduced host-safety, evidence, command-fidelity, and launcher-secret
findings. Do not run the launcher, do not present §9 for authorization, and do
not contact KVM2 on these bytes. This is round 2 of the T0 cap; one round remains.
