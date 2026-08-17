# Lead adjudication — B3 STOP at op 05 (2026-08-09)

## Finding

`RP1-B3.sh` stopped with rc 3:

```
RP0_STOP reason=path_probe_error path=/etc/mtc-bridge/mtc-bridge.env rc=1 detail=stat: cannot statx '/etc/mtc-bridge/mtc-bridge.env': Permission denied
```

Root cause: `/etc/mtc-bridge` is `root:root` mode `750` (B3's own earlier probe, in the
bound evidence). The run executes as the unprivileged login user `gatea`, who is not in
the `root` group, so the directory is not searchable for it: `stat` on **any** name under
`/etc/mtc-bridge/` returns `EACCES` regardless of whether the file exists. The env-file
check (§8 #4) and the manifest-binding check (§8 #5, which must read
`/etc/mtc-bridge/install_manifest.json`, mode `640 root:root`) are **structurally
impossible for an unprivileged operator on this host** — not merely inconvenient.

## Classification

- This is a **STOP (rc 3, could-not-evaluate)**, not a B3 FAIL: no probe that ran found
  deviant host state. Checks #1–#3 (release tree, venv tree, write-bit sweeps) all held.
- The preregistered named risk for this line (§8 #4: `bridge.env` vs `mtc-bridge.env`
  naming) is **unresolved, not triggered** — permission denial precedes the existence
  question, and the name cannot be adjudicated from this run's evidence.
- Per PREREGISTRATION.md: a STOP is never re-read as a PASS. RUNID
  `WPLP2-20260809T125940Z-8dc78f08-B3` is burned.

## Design gap (new): `B3-GAP-ENV`

The **accepted** B3 design (RP1-B3.sh, frozen `f40411b0…`) assumes the operator can
`stat` root-protected paths under `/etc/mtc-bridge/`. The accepted execution model
(unprivileged `gatea`, no sudo, zero host mutation) contradicts that assumption. One of
the two must change, and both changes are outside tonight's authority:

1. **Design repair** — restrict B3's admission claim to what an unprivileged operator can
   verify (trees + ancillary dir modes), and move env-file/manifest-binding verification
   to a privileged channel (e.g. a root-side check at deploy time, or a narrowly scoped
   `sudo -n stat` allowlist). Changes a frozen, adversarially accepted block → requires a
   new repair/re-audit cycle and re-freeze (new block hash, new runkit, new Stage 1).
2. **Host-side change** — group membership or ACL letting `gatea` read the metadata dir.
   Host mutation/reprovisioning → explicitly forbidden tonight.

**Escalation: owner decision required.** No improvised closure was attempted. B3 is
treated as blocked-by-gap alongside C1-GAP-A/C1-GAP-B until Barış rules.

## Disposition of R4-5

R4-5's skip is **collateral only** (first-FAIL sequencing), not an R4-5 defect. It needs
no privileged path: it verifies four hashes it carries, allocates its own evidence leaf
under `~gatea`, and runs a local-temp symlink-guard falsification. Every artifact it
depends on is already on the host **and hash-gated at run time** (`run_r45*.sh` re-verifies
RP0-LIB, RP0-BOOTSTRAP, RP4-C3 and the runner byte-for-byte before sourcing anything).

Owner authorization for tonight explicitly covered R4-5 execution. Re-attempting it
under a fresh preregistration (new one-use RUNID `…-R45B`, new create-once record root,
same frozen blocks, same route, same fail-closed argv discipline) stays inside that
authorization and inside §11's retry rule. Prepared as Stage 3B in `04_PREREG_R45B/`;
executed only after its own dry run verifies the new preregistration.
