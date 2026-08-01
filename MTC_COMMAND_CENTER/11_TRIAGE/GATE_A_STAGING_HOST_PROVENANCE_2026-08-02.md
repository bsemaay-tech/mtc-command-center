# GATE A — STAGING HOST PROVENANCE RECORD (2026-08-02)

Companion to `GATE_A_PREREGISTRATION_AND_STAGING_RUNBOOK_2026-08-01.md` (`af071882`) and
`GATE_A_PREREGISTRATION_ADDENDUM_A_2026-08-02.md` (`27a3a9d7`).

Records where the Gate A staging host came from, because "clean host" is a claim that has to be
provable rather than asserted. Written before Gate A's checks were executed.

## 1. Hyper-V access — resolved

`NEXT_SESSION_HANDOFF_2026-08-02.md` §1 stated the owner had signed out and back in. He had not, at
that point: the newest interactive logon was **2026-08-01 16:59:13** with `explorer.exe` running
unbroken since 16:59:14, and no logon session existed from 2026-08-02. `AzureAD\BarışSemaay` **was**
already a member of `S-1-5-32-578`, so the group add had landed — only the logon token was stale, and
with `HiberbootEnabled=1` a lock/unlock or sleep-resume never rebuilds it.

Owner restarted 2026-08-02 01:23:28. Verified after: token carries `S-1-5-32-578`, `Get-VM` succeeds.

## 2. Undocumented prior effort found on the host

`Get-VM` immediately returned a VM the handoff did not mention:

| Property | Value |
|---|---|
| Name | `KVM2-Ubuntu-2404-Staging` |
| Created | **2026-07-27 11:15:22** |
| State | Off (Gen 2, 4 vCPU, 4 GB, autocheckpoints off) |
| VHDX | `7.75 GB` written — an OS is installed |
| Attached | `kvm2-staging-autoinstall-seed.iso` |

`C:\HyperV\KVM2-Staging\` holds ~50 scripts and result files from 2026-07-26/27. Nothing under
`MTC_COMMAND_CENTER/` references any of it — the effort is **unrecorded in the repo**.

What its own result files show:

- `failed-azure-vm-retirement.json` — an Azure cloud-image attempt, retired.
- `missing-sudo-vm-retirement.json` — a second VM retired: *"Authorized key user lacked the intended
  validated sudoers rule."* Its 8.9 GB VHDX was archived to `evidence/…/failed_missing_sudoers/`.
- The surviving VM is the **third** attempt, built from a **patched** installer ISO.
- `vm-validate-result.json` / `vm-rehearsal-result.json` / `vm-restart-result.json` — all `PASS`.

## 3. Safety conclusion — the handoff's boundary claim holds

`vm-rehearsal-result.json` records, in the prior session's own words:

```
"bridge_rehearsal": "NOT_RUN",
"classification":   "local infrastructure-only"
```

Its passing items are OS hardening, root-login negative, storage fsync/hash, a **dummy** install
start, dummy rollback absence, and a boot-id-verified restart. No bridge, broker, order, ARM,
TESTNET, mainnet, wallet or credential action appears anywhere in that directory.

**So the handoff's safety statement is correct** — nothing on Linux touched the bridge. What was
wrong was its *host inventory*: "Hyper-V command available but access denied" was read as "no host
exists", when in fact a host had been built six days earlier and the denial merely hid it.

## 4. Decision — the 2026-07-27 VM is NOT used as the Gate A host

It is Ubuntu 24.04, validated and restart-tested, and reusing it would have saved roughly fifteen
minutes. It is still the wrong host:

- It ran `dummy_install_start` and `dummy_rollback_absence` rehearsals — install residue of
  unquantified extent.
- It survived a period of hand-repair attempts (`repair-vm-sudo.ps1`) whose full effect is not
  recorded.
- Its VHDX was written as recently as 2026-08-02 01:23, immediately before the host restart.

The programme's own rule decides it: *"a lab snapshot or agent uninstall is never clean-host
evidence,"* and *"after several half-finished attempts nobody can prove whether the working system is
a clean install or a survivor of leftovers."* A host that cannot be shown clean cannot produce
clean-host evidence, and saving fifteen minutes is not worth an A-1 result nobody can trust later.

**`KVM2-Ubuntu-2404-Staging` was left untouched** — not started, not modified, not deleted. It is
prior evidence and its disposal is the owner's call, not the Lead's.

## 5. Installation media — provenance proven, not assumed

The prior session's official ISO was already on disk and was re-verified independently here:

```
C:\HyperV\KVM2-Staging\Images\ubuntu-24.04.4-live-server-amd64.iso
3,405,469,696 bytes
sha256 e907d92eeec9df64163a7e454cbc8d7755e8ddc7ed42f99dbc80c40f1a138433
       == Canonical's published releases.ubuntu.com/24.04/SHA256SUMS
```

Its patched sibling (`…-autoinstall.iso`) was **not** taken on trust. A full byte-level diff against
the verified official image found exactly **six** differing 2048-byte sectors, every one explained:

| Sector(s) | Structure | Difference |
|---|---|---|
| 16, 18 | Primary + Joliet volume descriptors | volume modification timestamp → `…727104834`, GMT offset `0x0c` (+3 h) — matches the recorded patch time 2026-07-27 10:48:34 local |
| 39, 544 | ISO9660 directory records | `grub.cfg` 61→73, `loopback.cfg` 52→64 — **+12 bytes each**, exactly `len(" autoinstall")` |
| 2197, 3303 | `/BOOT/GRUB/GRUB.CFG`, `/BOOT/GRUB/LOOPBACK.CFG` | one line each: `linux /casper/vmlinuz` → `linux /casper/vmlinuz autoinstall`; remaining text shifts 12 bytes into existing padding |

No byte outside those six sectors differs. The custom image is therefore provably **Canonical media
plus one kernel argument** — nothing injected. (The first pass of this check reported PASS while only
comparing the two GRUB files; that conclusion was under-evidenced and was not accepted until the
remaining four sectors were explained.)

## 6. The Gate A host as built

| Property | Value |
|---|---|
| Name | `GATEA-STAGING` |
| Location | `C:\HyperV\GATEA-STAGING\` (separate from the 2026-07-27 tree) |
| Generation | 2, Secure Boot **On**, `MicrosoftUEFICertificateAuthority` |
| vCPU / RAM | 4 / 4 GB **static** (dynamic memory disabled — keeps A-5 deterministic) |
| Disk | 40 GB dynamic VHDX, freshly created |
| Boot order | HardDisk → installer DVD → seed DVD (empty disk falls through to DVD, installed system wins afterwards; a DVD-first order reboots into the installer forever) |
| Checkpoints | disabled entirely (`-CheckpointType Disabled`) — a checkpoint is hidden state and would corrupt A-5 |
| Start / stop action | Nothing / TurnOff (no saved-state file) |
| Network | Default Switch |
| Seed | `gatea-staging-seed.iso`, sha256 `a83d6cc2e4ee2c17969975709c21d7aae8ae12034e6a964b340803c03a754af2`, CIDATA volume, LF-normalised |
| Access | ed25519 keypair generated for this VM only; **no password exists** — `password: "!"`, `passwd -l` on both accounts, `allow-pw: false`, `PasswordAuthentication no` |

The autoinstall enables `ufw` default-deny inbound with OpenSSH only, and installs `python3.12-venv`
— the two clean-host preconditions pre-registered in Addendum A §A.2. They are satisfied by the
**host build**, so no file in the payload is edited to make the install work and A-2's FAIL condition
is not tripped.

## 7. Status

Addendum A §A.8's blocker is closed. Gate A checks A-1 … A-9 have **not** been executed at the time
of writing; A-0's source half passed and its post-transfer half remains outstanding. No ARM, order,
broker, TESTNET, mainnet, wallet or credential action has occurred.
