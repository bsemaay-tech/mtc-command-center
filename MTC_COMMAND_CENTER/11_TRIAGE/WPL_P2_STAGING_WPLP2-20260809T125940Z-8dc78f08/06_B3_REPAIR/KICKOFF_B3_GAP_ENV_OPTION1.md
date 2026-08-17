# KICKOFF — B3-GAP-ENV Option 1 design repair (round 1 implementation)

You are the counterpart implementer (Claude Max) for an authorized private-repo
test-infrastructure design repair. Self-contained brief; do not read any file outside
the "Inputs" list. Write outputs ONLY into the `round1/` subdirectory next to this file.
ASCII only in every file you produce. English only.

## Context

The accepted staging admission block `RP1-B3.sh` stopped on the target host with:

```
RP0_STOP reason=path_probe_error path=/etc/mtc-bridge/mtc-bridge.env rc=1 detail=stat: cannot statx '/etc/mtc-bridge/mtc-bridge.env': Permission denied
```

Root cause (adjudicated, `03_TRANSPORT/B3_STOP_ADJUDICATION.md`): the block runs as the
unprivileged user `gatea`; `/etc/mtc-bridge` is `750 root:root`, so `stat` on ANY name
under it returns EACCES. Two checks are therefore structurally impossible unprivileged:

- `b3_assert_mode_owner "$ENV_FILE" 0600 root:root` (line 109)
- `b3_assert_mode_owner "$INSTALL_MANIFEST" 0640 root:root` (line 110) and the whole
  `b3_assert_manifest_binding` section (lines 113-114), which must READ the manifest.

Authorized repair (Option 1, binding): keep everything an unprivileged operator CAN
verify in `RP1-B3.sh`; move the env-file and install-manifest admission into a NEW
root-side deploy-time verify block that will run as root at install/deploy time through
the deploy channel (it is NOT executed in the current staging run). No host mutation
anywhere. No sudo. No group/ACL changes.

## Inputs (read these, nothing else)

- This file.
- `../01_RUNKIT/RP1-B3.sh` — the accepted block to repair (117 lines).
- `../01_RUNKIT/RP0-LIB.sh` — for the predicates it uses (`rp0_probe_path`,
  `rp0_monotonic_ms`, logging conventions). Do not modify this file.
- `../03_TRANSPORT/B3_STOP_ADJUDICATION.md` — the adjudication you are implementing.
- `../02_PREREG/PREREGISTRATION.md` sections 2 and 8 — preregistered inputs and the
  expectation table the old design carried.

## Deliverables (write into `round1/`)

1. `RP1-B3.sh` — the repaired unprivileged block, full file. Requirements:
   - Keep unchanged in scope: release tree + venv tree exact mode/owner 0555 root:root,
     budgeted `/222` any-write-bit sweeps, `STATE_DIR`/`LOG_DIR` 0750
     mtc-bridge:mtc-bridge, `CONF_DIR` (the directory itself) 0750 root:root,
     `UNIT_FILE` 0644 root:root. Note: `stat` on `/etc/mtc-bridge` itself works
     unprivileged (needs only search on `/etc`); entering it does not.
   - Remove the `ENV_FILE` and `INSTALL_MANIFEST` stat lines and the
     `b3_assert_manifest_binding` invocation from the unprivileged path.
   - ADD an explicit unprivileged boundary probe: assert that `/etc/mtc-bridge` denies
     entry to the caller (e.g. attempting to stat a name under it yields EACCES, which
     is now an EXPECTED outcome named `B3_conf_dir_opaque_to_operator`). Rationale: the
     750 root:root claim plus a demonstrated denial is the strongest statement an
     unprivileged operator can honestly make about that directory; a SUCCESSFUL stat of
     the env file under this design would itself be a FAIL (it would mean the directory
     is more open than the accepted host state). Keep the three-outcome discipline:
     that probe returning "file visible" is FAIL, EACCES is the pass arm, any other
     error class is STOP.
   - Preserve: `set -Eeuo pipefail`, B3_/RP0_ log prefixes, no file content printed,
     rc contract 0/1/3, comment style citing candidate sources (common.sh:80-93,
     find-predicate provenance), the preregistered-inputs guard block. The
     `B3_RELEASE_MANIFEST_SHA256` requirement moves out with the manifest check;
     `B3_SWEEP_BUDGET_S` stays.
2. `RPD-VERIFY.sh` — the NEW root-side deploy-time verify block, full file. Requirements:
   - Header `# ===== BLOCK-ID: RPD-VERIFY ===== [EXECUTABLE PROPOSAL BLOCK]`, same
     conventions, same rc contract, `RPD_` log prefix.
   - Runs as root (assert `id -u` = 0 at entry; not-root is STOP, never a silent skip).
   - Read-only verification only, no mutation of any kind: env file exists, regular,
     0600 root:root; install manifest exists, regular, 0640 root:root; manifest binds
     BOTH `"release_sha": "<candidate>"` and
     `"release_manifest_sha256": "<preregistered value>"` via silent `grep -qsF` with
     the same three-outcome rc handling as the old `b3_assert_manifest_binding`
     (rc 1 = FAIL not-bound, rc >1 = STOP). No manifest content is ever printed.
   - Candidate SHA and expected manifest SHA arrive as required environment variables
     (`RPD_CANDIDATE_SHA`, `RPD_RELEASE_MANIFEST_SHA256`), guarded like the existing
     preregistered-inputs block; never derived on the host.
3. `DESIGN_NOTES.md` — for each check of the original block: where it landed
   (unprivileged / root-side) and one-sentence why; the exact-diff summary of
   `RP1-B3.sh` old vs new (list removed lines, added functions); the admission-claim
   statement each block now makes; explicit statement that RPD-VERIFY is design-only in
   this unit (no execution path exists tonight, it enters the runkit as a frozen
   non-executed block like RP3/RP5).
4. `SELF_QA.md` — evidence of `bash -n` on both scripts (run it), a walk through each
   FAIL and STOP arm with the exact reason string it emits, and confirmation that no
   line prints file content or reads a credential value.

## Hard constraints

- Do not touch any file outside `round1/`. Do not run anything against any remote host.
- Do not weaken any surviving check. Do not add network, service, credential or
  mutation logic. This is a T0-tier artifact set; it will be adversarially re-audited
  (Codex, up to 3 rounds) — write for an auditor whose job is to refute you.
