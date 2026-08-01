# GATE A — PRE-REGISTRATION ADDENDUM A (2026-08-02)

**Addendum to** `GATE_A_PREREGISTRATION_AND_STAGING_RUNBOOK_2026-08-01.md` (commit `af071882`).

**Written before any staging host exists and before any Ubuntu execution of any kind**, which is the
only reason it is allowed to exist. The parent runbook fixed its criteria in advance so that nobody
could adjust a criterion to match whatever a run produced. This addendum keeps that discipline: it
was produced by *reading the installer source*, not by watching a run fail.

## A.0 What this does and does not change

**Weakens nothing.** Checks A-1 … A-9 in the parent §3 are unchanged — not reworded, not relaxed,
not removed. Their FAIL conditions stand exactly as written.

**Adds** two clean-host baseline preconditions that a stock Ubuntu 24.04 live-server install does
**not** satisfy, and which would otherwise have stopped A-2 mid-run. Recording them now, in advance,
is the difference between a pre-registered precondition and a post-hoc excuse.

## A.1 Evidence — read from the artifact, not from a run

Source: `C:\WPI_ARTIFACTS\1adf9ae51b0ddfe81057860aec5c23bb842f5a84`.

| # | Finding | Citation |
|---|---|---|
| 1 | `assert_ufw_ssh_only` **fails closed** if `ufw` is absent, inactive, not default-deny-incoming, allows any non-SSH inbound, or mentions port 8790 | `IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh:153-179` |
| 2 | `install.sh` calls that assertion at the **dry-run boundary** and again after install, and `die`s if any assertion failed | `install.sh:237,243` and `install.sh:390,396` |
| 3 | Stock Ubuntu 24.04 server ships `ufw` **installed but inactive** | Canonical default; to be confirmed on the host as A-1 evidence |
| 4 | Installer creates the venv with `python3.12 -m venv`, which needs `ensurepip` from the `python3.12-venv` package (not in the default server install) | `install.sh:291`, `common.sh:31` (`MTC_PYTHON="python3.12"`) |
| 5 | Required commands are otherwise satisfied by a default server install (`coreutils`, `procps` → `pgrep`, `iproute2` → `ss`, `systemd`, `passwd`) | `install.sh:133-134` |
| 6 | Python target is **3.12**; Ubuntu 24.04 ships 3.12.3 — match | `requirements.in:19`, `requirements.lock:2` |

## A.2 Clean-host baseline — added to A-1

The host must satisfy the following **before** `install.sh` is invoked. These are *host baseline*, not
artifact modifications, so A-2's FAIL condition ("any step that requires editing a file on the host to
make it work") is **not** tripped by them. No file in the payload is touched.

1. `ufw` active, `Default: deny (incoming)`, exactly one inbound allowance (SSH/22), no rule
   mentioning 8790.
2. `python3.12-venv` present.
3. Ubuntu 24.04 LTS, `python3.12` on `PATH`.

**Boundary, stated explicitly.** Enabling `ufw` on the *disposable staging VM* is establishing the
baseline the installer demands of any host. It is **not** authorization to add, remove or change a
firewall rule on KVM2, where the programme's invariant 8 stands unchanged and such a change remains a
separately scoped, separately audited, owner-approved action.

If either baseline item is instead delivered by editing the payload, that is an A-2 **FAIL** and must
be reported as one.

## A.3 Predictions recorded in advance — each falsifiable

The parent runbook records predictions before the run so the result is evidence rather than a story
told afterwards. Three stand for this gate:

- **P1.** On a host with `ufw` inactive, `install.sh --dry-run` will `die` with `ufw is not active`
  **before performing any mutation**. **If it does not** — if the dry run proceeds past that point —
  that is itself a required finding: a fail-closed assertion did not fire.
- **P2.** Without `python3.12-venv`, `python3.12 -m venv` fails and the install dies at
  `install.sh:291` without a partially populated venv surviving.
- **P3** (restated from parent §3 A-3). The KVM2 ledger-hash test may legitimately **pass** on Linux,
  because WP-L Phase 1 diagnosed its Windows failure as a CRLF artefact. Record the result either way.

## A.4 The artifact is already a `package.sh` payload

`C:\WPI_ARTIFACTS\1adf9ae5…` carries `RELEASE_SHA` and `RELEASE_SHA256SUMS` at its root — the exact
output shape of `package.sh`. It is therefore the `--source` payload directly; no repackaging step
exists or is permitted. `install.sh` refuses to run unless it is itself the copy inside that
hash-bound payload (`install.sh:96`).

**A-0 source side, executed 2026-08-02 — PASS:**

```
RELEASE_SHA      : 1adf9ae51b0ddfe81057860aec5c23bb842f5a84
manifest sha256  : bfefea2f825c8ba8a4c2289cd6ed90c74b51b15bc603cd5589db8815493ced02   == expected
manifest entries : 7060        == expected
files on disk    : 7061        == expected
total bytes      : 1051904669  == expected
```

The post-transfer half of A-0 remains outstanding until a host exists.

## A.5 Pre-registered invocation

```bash
# A-2 dry run — prints every mutating action, creates nothing
sudo bash <PAYLOAD>/IBKR_PAPER_BRIDGE/deploy/linux/install.sh \
    --release-sha    1adf9ae51b0ddfe81057860aec5c23bb842f5a84 \
    --manifest-sha256 bfefea2f825c8ba8a4c2289cd6ed90c74b51b15bc603cd5589db8815493ced02 \
    --source <PAYLOAD> --dry-run

# A-2 install
sudo bash <PAYLOAD>/IBKR_PAPER_BRIDGE/deploy/linux/install.sh \
    --release-sha    1adf9ae51b0ddfe81057860aec5c23bb842f5a84 \
    --manifest-sha256 bfefea2f825c8ba8a4c2289cd6ed90c74b51b15bc603cd5589db8815493ced02 \
    --source <PAYLOAD>

# A-2 verify — read-only, repeatable
sudo bash <PAYLOAD>/IBKR_PAPER_BRIDGE/deploy/linux/verify.sh \
    --release-sha    1adf9ae51b0ddfe81057860aec5c23bb842f5a84 \
    --manifest-sha256 bfefea2f825c8ba8a4c2289cd6ed90c74b51b15bc603cd5589db8815493ced02
```

**A-4 method.** The unit installs **masked**, `Restart=no`, with no `[Install]` section
(`deploy/linux/README.md`, `install.sh:352-377`). A-4's "start the service" therefore requires
`systemctl unmask` followed by `systemctl start` on the staging host. That is the only way A-4 can be
executed at all, and it is pre-registered here rather than improvised during the run.

## A.6 Staging does not spend a KVM2 gate

`deploy/linux/COMMANDS.md` names its gates `KVM2-P4-01/-02/-03/-06/-07`. Those govern **the KVM2
target host**, including its "exactly one attempt, a retry needs a new authorization" rule.

Gate A is the rehearsal on the **disposable** host, authorized by the parent pre-registration and by
Barış's instruction of 2026-08-02. Running the Stage B / C / F equivalents on staging **does not
spend, satisfy, substitute for, or pre-approve any `KVM2-P4-xx` gate.** KVM2 still gets exactly one
clean install under its own authorizations. Anyone reading this later should not be able to mistake a
staging rehearsal for a consumed KVM2 gate.

## A.7 Staging VM specification

| Property | Value | Reason |
|---|---|---|
| Name | `GATEA-STAGING` | expendable; will be broken, wiped, redone |
| Generation | 2 (UEFI), Secure Boot template `MicrosoftUEFICertificateAuthority` | required for Ubuntu on Gen 2 |
| vCPU / RAM | 4 / 4096 MB **static** | static memory keeps the A-5 unclean-restart test deterministic |
| Disk | 40 GB dynamic VHDX | ~1 GB payload + venv + OS |
| Network | Default Switch (NAT) | outbound for the hash-pinned wheel install; A-8 still asserts loopback-only binding |
| Automatic checkpoints | **off** | a checkpoint is hidden state and would corrupt the A-5 result |
| Automatic start action | Nothing | never auto-starts with the host |
| OS | `ubuntu-24.04.4-live-server-amd64.iso`, SHA-256 `e907d92eeec9df64163a7e454cbc8d7755e8ddc7ed42f99dbc80c40f1a138433` (Canonical published) | verified against `releases.ubuntu.com/24.04/SHA256SUMS` before use |
| Access | SSH key generated on the host machine for this VM only | **no password is ever typed, requested, accepted or pasted.** Owner credentials remain owner-held |

## A.8 Blocker at time of writing

Hyper-V remains inaccessible. `AzureAD\BarışSemaay` **is** a member of `S-1-5-32-578`
("Hyper-V Yöneticileri") in the machine's local group database, but the current logon token does not
carry the group, so `Get-VM` fails with
*"Bu görevi tamamlamak için gerekli izne sahip değilsiniz."*

The newest interactive logon session is **2026-08-01 16:59:13** and `explorer.exe` has run
continuously since 16:59:14; no logon session exists from 2026-08-02. The intended sign-out/in
therefore did not occur — a lock/unlock or sleep-resume does not mint a new token. `HiberbootEnabled`
is `1`, so a full **restart** (not "shut down") is the deterministic fix. Last boot was 2026-07-27.

**The Lead does not modify group membership, policy, or elevation.** That action is the owner's.
