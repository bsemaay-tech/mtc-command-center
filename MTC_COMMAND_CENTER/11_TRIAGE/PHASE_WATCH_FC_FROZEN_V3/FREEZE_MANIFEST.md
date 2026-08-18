# FREEZE MANIFEST — forced-command V3 artifact set (owner freeze approval 2026-08-18)

**Frozen for the pre-application T0 review. HELD: no T0 dispatch until the owner
releases it; no KVM2 contact or mutation under any circumstances until the owner's
separate exact application approval.** `WATCH_ACTIVE: NO`.

Because this repo uses `* text=auto`, every text file has TWO canonical byte forms
(see the recorded-hash-form-ambiguity rule). Both are pinned here; the **git blob
OID is the authoritative identity**:

| File | Git blob OID (repo LF form, authoritative) | SHA-256 (as-authored working-tree bytes, LF) |
|---|---|---|
| `mtc-watch-collect` | `b92e49fd6defe4a62bb2ea62b6f658b425bcd34b` | `764ba932198fed0a6602e3b222fce6413c0cbecddcb60530b0d4f0ec812669d7` |
| `70-mtc-watch.conf` | `816aff73aeffd3ef08fe60afe31a9704fda0ea30` | `c7d0e123257809806ab60dcaca47d045981289e4f1b35b37bdfdeab16f14be61` |
| `authorized_keys.mtc-watch.template` | `f95a8ca33482d96ba04b470b9add5d586deaf27c` | `b11fd6df5247f8114e7d6c4e39b5d0b25d54910b68e598b1cf8ff2908b1c8dc0` |
| `mtc-bridge-backup` | `842a410ff07cd2047523d9e88d54ebe49bbf0081` | `1508e93d17d61a508fdb49a288e6afa617a74542320b8d819df53450319724ec` |
| `mtc-bridge-backup.service` | `e236e331a98f5f8a20f28e3e2dc80e4dd837f1b1` | `421ce6860bdd063f30d55614ed49a176605bb061280abbba127d1c234859882b` |
| `mtc-bridge-backup.timer` | `7c1e61cdd94c71bba0f3e90a511228e90edaab65` | `2feed4c1d89326a40e6823459551ef2ec8995907ba537119d272bd42da18057e` |
| `provisioning-commands.sh` | `1702225ecd2a3ba8756ca562bea82a8eebd0e42e` | `a64cff983851e6039ff87e3e6252ecbb239478bc08ba177dc3c2b1b11d6831e0` |
| `collect_kvm2_evidence_v3.ps1` | `8a9275670d85bccca6c6c9fef1227e552f2397e8` | `1600e585f3eab23984ca2343f506cf6e12639ca58fe3187a364856b9ed37fce8` |
| `tests_T_ssh_lockdown.ps1` | `03eb629d07a82ad3fe2f4700fbc982fdc1e66937` | `8102cc4028df21f1f292e33c765e2fe2212704e5f1a1a0d9bffe00864ba92197` |
| `tests_B_backup_failures.sh` | `125be3f628bf3ef42ccc7104394967b056fb6bac` | `b6b72c4e8d9fca5d8ac2255f69afd8f4fc08a47a13e446249f49f9322b42846b` |
| `tests_W_agent.ps1` | `49766b44cca96b4f4e72fcbc7063a1744bd6c2aa` | `c00d559d145b32bb813cd20cee119ab7fd2f2f9795a8c502991ba11fcbda5ed1` |

## Owner-required hardening, where it lives

| Requirement | Location |
|---|---|
| Absolute executable paths | every command in `mtc-watch-collect`, `mtc-bridge-backup`, `provisioning-commands.sh` |
| Sanitized `env -i` | every menu entry in `mtc-watch-collect`; both `runuser` invocations in `mtc-bridge-backup` |
| Restrictive `umask` | `umask 077` at the top of both shell executables; `UMask=0077` in the service unit; `umask 022` for provisioning installs |
| Overlap prevention | `flock -n` on `/run/mtc-bridge-backup.lock` (orchestrator single-instance); systemd oneshot prevents timer overlap |
| Atomic manifest replacement preserving watcher ACL | `status.json.tmp` gets `chmod 0644` + `setfacl u:mtc-watch:r--` BEFORE the atomic `mv` — rename keeps the inode's ACL; done identically on success and failure paths |
| T/B/W falsification scripts | `tests_T_ssh_lockdown.ps1` (T1–T10), `tests_B_backup_failures.sh` (B1–B6 binding contract), `tests_W_agent.ps1` (W1–W4) |

## Placeholders resolved only at application (each re-hashed then)

- `<OWNER-PUBKEY>` in the authorized_keys template — owner-generated ed25519 public key.
- `PASTE-MTC-WATCH-KEY-FINGERPRINT-AT-APPLICATION` in the client and `tests_W` — the new key's SHA256 fingerprint.
- `/opt/mtc-bridge/current` release symlink — if the deployment does not maintain
  this symlink, the orchestrator's `RELEASE_LINK` line is amended at review to the
  exact release path; flagged for the T0 reviewers.

## Change control

Any byte change to any file above voids the freeze: re-freeze + re-review. The
gate chain from the V3 design doc governs; the pre-application T0 pair (exact
`claude-opus-5` xhigh + `gpt-5.6-sol` xhigh) is dispatched only on the owner's
release of the hold.
