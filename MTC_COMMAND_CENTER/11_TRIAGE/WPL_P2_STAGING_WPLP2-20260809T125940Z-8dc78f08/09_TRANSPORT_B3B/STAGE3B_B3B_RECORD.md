# Stage 3B-B3B — repaired B3 executed on the host (2026-08-09 night)

Result: **TR_RUN PASS — 7/7 ops rc=0 — `B3 PASS`.** The design gap `B3-GAP-ENV`, which
stopped the original block on first host contact, is closed on the real host.

Unit `WPLP2B-20260809T210610Z-834380c5`, RUNID `…-B3B` (one-use, now consumed).
Authority: owner authorization given in-session 2026-08-09 (`STANDING_AUTONOMY_AUTHORITY_2026-08-09.md`
§A1). Preregistration `../08_PREREG_B3B/` committed at `bf395dab` **before** any B3B
invocation — the ordering is provable from git history.

## Ops

| op | kind | rc | outcome |
|---|---|---|---|
| 01 | ssh remote_setup | 0 | four create-once dirs allocated |
| 02 | scp runkit_b.tar up | 0 | re-frozen archive uploaded |
| 03 | ssh remote_extract_verify | 0 | `EXTRACT PASS … members=10 verified=10 executed=0`; archive re-hashed `888bec17…` remotely; all ten block digests bit-identical, including the repaired `RP1-B3.sh` and the new `RPD-VERIFY.sh` |
| 04 | ssh run_b3b | 0 | **B3 PASS** |
| 05 | ssh remote_close_tree | 0 | evidence closed, digest set stable across two passes |
| 06 | scp evidence down | 0 | `b3b.log` retrieved |
| 07 | local_bind | 0 | **TR_BIND_PASS**; remote set `d572afe7…` reproduced bit-identical locally |

## What B3 proved (from the bound `b3b.log`)

- **Release and venv trees**: `owner_numeric=0:0` mode `555`; both `-perm /222` sweeps
  clean inside the 120 s budget. No write bit anywhere in either immutable tree.
- **Ancillary paths, numeric ownership**: `/var/lib/mtc-bridge` and `/var/log/mtc-bridge`
  are `999:988` mode `750`; `/etc/mtc-bridge` is `0:0` mode `750`; the unit fragment is
  `0:0` mode `644`. Ownership is compared numerically only — the rendered names are
  diagnostic, which is what audit 2 required after showing an NSS mapping can spoof
  `root:root`.
- **Conf-dir boundary (the repaired core)**: `/etc/mtc-bridge` is canonical and
  non-symlinked, has no mount at or under it (23 mount records read), the caller is not
  in its group, and search is denied — with EACCES observed for **both** probe names
  (the existing env file and a name that does not exist). Under the repaired design that
  is the pass arm; a successful stat would have been a FAIL, and ENOENT would have been a
  FAIL too (it would prove search succeeded, i.e. the host is more open than accepted).
- **Deferred, declared not skipped**: env-file mode/owner, install-manifest mode/owner,
  and install-manifest binding each emit an explicit `B3_deferred … to=RPD-VERIFY`
  line. The claim line is honest about the reduced scope:
  `B3_claim scope=unprivileged_only deferred=3 conf_dir=opaque_to_operator ownership=numeric_only mutation=none`.

## How the numeric service identity was preregistered without circularity

The repaired block requires numeric `B3_SVC_UID`/`B3_SVC_GID`. `deploy/linux/install.sh`
creates the account with `groupadd --system` / `useradd --system` and pins no id, so no
design-time numeric value exists anywhere in the repository, and reading a number off the
host only to assert the host matches it would be vacuous.

Resolution: the deployment contract is the **name** — the unit template declares
`User=mtc-bridge` / `Group=mtc-bridge`. A recorded read-only preflight probe
(`../08_PREREG_B3B/preflight_probe.sh`, output committed alongside) resolved that name via
`getent`: uid **999**, gid **988**. Note the two differ, so the plausible-looking guess
`999:999` would have been wrong — which is exactly why this had to be resolved rather than
assumed. B3 then proves the state and log directories are owned by the same account
systemd runs the unit as. That is falsifiable: a stale directory from a reinstall, or a
chown to any other identity, fails it.

Epistemic limit, stated rather than hidden: this binds the directories to the
*currently resolvable* `mtc-bridge` account, not to a value fixed at design time. No such
fixed value exists while the deployment allocates system ids dynamically.

## Safety state

Zero service mutation, zero ARM, zero credential contact, no reboot, no rollback, no unit
write. Remote writes confined to the run's own create-once tree under `/home/gatea/`.
`RPD-VERIFY.sh` travelled in the archive and was hash-verified but **never executed** — it
is root-side and remains design-only; no root, sudo, group or ACL change was used or
requested. C1, C2, C3, C4, C5 untouched. The old unit tree and both earlier record roots
were not modified.
