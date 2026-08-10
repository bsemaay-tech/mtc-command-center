# RP7 status

Status: **REPAIRED-R4-PENDING-INDEPENDENT-REAUDIT**

Scope: `RP7-WPI-RO.sh` implements remote RO-stage rows 10-23 and records row
24 as operator-side only. Repair round 4 was authorized by the owner in-session
on 2026-08-10 past the recorded T0 cap, after the second-flagship Codex xhigh
audit (`RP7_CODEX_T0_AUDIT_2026-08-10.md`) returned BLOCK on five findings, one
of them a security-relevant false-PASS hole. Recorded as a standing-authority
§1 escalation resolved to CONTINUE by explicit owner grant. Acceptance belongs
to the fresh cross-model re-audit.

Material repair state added this round:

- **the subject venv no longer arbitrates its own status or package state.**
  On the target Python 3.12, `-I` implies `-E`/`-P`/`-s` but **not** `-S`, so
  `site` still imported and an executable `import` line in the judged venv's own
  `site-packages/*.pth` - or a `sitecustomize.py` beside it - ran with this
  block's authority before either adjudicator's source was compiled. It could
  print the exact accepted result and exit 0, and could write anywhere `gatea`
  can write. Both accepting adjudicators now run under a separately pinned
  system interpreter with `-I -S`, and each refuses to produce a result unless
  `sys.flags.isolated` and `sys.flags.no_site` are set and no
  `site`/`sitecustomize`/`usercustomize` module is loaded;
- **one explicit discovery universe** shared by the row-19 preflight and the
  trusted verifier. The preflight enumeration is unfiltered to depth 1, the only
  admissible metadata object is a `*.dist-info` directory holding `METADATA` and
  `RECORD`, and every other format or location `importlib.metadata` accepts -
  `egg-info`, `egg-link`, `egg`, `zip`, `whl`, and the `.pth`/`sitecustomize`
  startup hooks - is a STOP on both sides. The trusted driver replaces the
  implicit `sys.path` discovery with exactly that enumerated list, so the zip and
  extension-finder routes are structurally unreachable, and the venv's
  `site-packages` is never placed on `sys.path`;
- **row 22 parses the whole `ss` table before any semantic verdict.** Wildcard,
  unexpected-address and count FAILs are applied only after reader diagnostics,
  record termination and grammar have held for every record. Reversing the two
  records the auditor used no longer changes rc 1 to rc 3: both orders reach
  STOP rc 3, because both tables contain a record that is not evaluable;
- **the preregistered B5/B6 order is restored.** Only the row-22 service-netns
  preflight inversion is authorized; the round-3 whole-listener move is reverted,
  so the executed order is `netns binding -> status rows 20-21 -> listener rows
  22-23`;
- **row grammar.** Rows 17, 19 and 19a carry their own unreadable tokens
  (`installed_lock_unreadable`, `metadata_unreadable`, `verifier_unreadable`)
  through every `lstat` and component walk instead of the generic
  `path_not_evaluable`; a bound leaf with deviant numeric ownership emits the
  row's own `installed_lock_owner_unexpected` / `verifier_owner_unexpected`;
  `installed_lock_object_unexpected` no longer carries the extra `path=`; and the
  last two raw `%F` sites are routed through `wpi_kind_token`.

Local validation: literal Git Bash (MSYS2, GNU coreutils 8.32, CPython 3.14.2)
QA fence PASS (`QA_PASS all_assertions=yes`), with a REAL RED/GREEN pair for
every one of the five findings and every round-3 arm carried forward. The
finding-1 arms are the load-bearing ones and they were **executed**: two real
`python -m venv` environments, one carrying an executable `*.pth` and one a
`sitecustomize.py`, each writing a marker file and printing the exact accepted
result line. Against the round-3 bytes both produce a PASS on a deviant host
plus a mutation; against the round-4 bytes the marker is absent and the truthful
FAIL is emitted. A third arm in each pair pins the SAME venv interpreter under
the repaired flags, so the isolated variable is `-S` alone. The published fence
was re-extracted from `SELF_QA_RP7.md` and re-run byte-identically to green.
`bash -n` PASS.

**FREEZE-GATE ITEMS (two, both carried deliberately).**

1. `WPI_FIXED_ATTESTED_MOUNT_PROJECTION_SHA256` is still `<PIN-AT-FREEZE>`, so
   there is no executed arm in which `wpi_validate_inputs` *accepts* a correct
   input set, and there cannot be one before freeze. The
   `normalised_path_projection_v2` digest the deploy channel must supply now
   covers **21** point paths, not 20: the trusted interpreter is a projection
   point.
2. `WPI_FIXED_TRUSTED_PYTHON` is new and also `<PIN-AT-FREEZE>`.
   `/usr/bin/python3` is a symlink on the target family and `wpi_bind_tool`
   admits no symlinked object, so the deploy channel must pin the resolved
   `/usr/bin/python3.<minor>`. The QA records the executed proof that an
   unresolved pin is refused (`tool_not_evaluable tool=python3 ... kind=symlink`,
   rc 3) rather than silently followed.

The first action after the deploy channel supplies both values, and before
dispatch, is to execute the accepting-input arm and record it. The block cannot
be frozen on the strength of this QA alone.

Final executable identity:

```text
bytes=70941
sha256=23e55667bec2453e21605b3551d5802b9cc28a82040789f3ead988b69aa01aad
```

No host contact, network probe, SSH/SCP, RUNID minting, commit, deployment, or
change outside the round-4 authorized deliverables occurred.
