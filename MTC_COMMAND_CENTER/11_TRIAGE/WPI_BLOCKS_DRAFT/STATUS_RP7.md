# RP7 status

Status: **REPAIRED-R3-PENDING-INDEPENDENT-REAUDIT**

Scope: `RP7-WPI-RO.sh` implements remote RO-stage rows 10-23 and records row
24 as operator-side only. Repair round 3 - the last round of the T0 cap -
closes the six findings in `RP7_CLAUDEPRO_REAUDIT_R2_2026-08-10.md`, on top of
round 2's 13/13. Acceptance belongs to the fresh cross-model re-audit.

Material repair state added this round:

- the mount binding is `normalised_path_projection_v2`: per preregistered point
  path the **effective** covering mount (last longest match, not first) plus the
  count of records sharing that mount point, **plus** the full subtree closure of
  every mountinfo record at or below each preregistered root, plus per-root
  counts. `requirements.lock` and `verify_lock.py` are now point paths. v1 was
  blind to a decoy mount inside a trusted subtree and to a stacked mount; both
  falsifications now flip;
- the ENOENT matcher accepts only diagnostics the block's own pinned absolute
  `argv[0]` can produce; the three basename spellings are gone;
- every tool binding discloses `attestation=self` (`stat`, `env`, `sha256sum`,
  `timeout` - the instruments the projection and the binding are built from) or
  `attestation=bound_instrument` (the other five);
- the bounding wrapper runs **inside** the cleared environment: `env -i` execs
  `timeout`, not the reverse, and the bound is preserved;
- multi-word `%F` values are routed through `wpi_kind_token` at the two sites
  that still interpolated them raw;
- `elapsed_s` is the truncated whole-second rendering of `elapsed_ms`, so the
  emitted pair cannot contradict itself. Enforcement remains on milliseconds.

Local validation: literal Git Bash (MSYS2, GNU coreutils 8.32) QA fence PASS
(`QA_PASS all_assertions=yes`), including a D026 RED/GREEN pair for every
round-3 repair, with the round-2 code bodies carried verbatim as the RED arms.
`bash -n` PASS. No mount-guard stub remains in the suite.

**FREEZE-GATE ITEM (re-audit finding 2(c), carried deliberately).** There is no
executed arm in which `wpi_validate_inputs` *accepts* a correct input set, and
there cannot be one before freeze: `WPI_FIXED_ATTESTED_MOUNT_PROJECTION_SHA256`
is still `<PIN-AT-FREEZE>`, so validation necessarily STOPs. The first action
after the deploy channel supplies the `normalised_path_projection_v2` digest,
and before dispatch, is to execute that accepting-input arm and record it. The
block cannot be frozen on the strength of this QA alone.

Final executable identity:

```text
bytes=58012
sha256=1d118d1581534f5d16b3730efbe642e80e5232fbf8a245d238574907166a7f4e
```

No host contact, network probe, SSH/SCP, RUNID minting, commit, deployment, or
change outside the five kickoff-authorized deliverables occurred.
