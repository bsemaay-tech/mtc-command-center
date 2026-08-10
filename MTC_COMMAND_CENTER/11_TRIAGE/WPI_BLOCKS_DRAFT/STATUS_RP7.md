# RP7 status

Status: **REPAIRED-R5-PENDING-INDEPENDENT-REAUDIT**

Scope: `RP7-WPI-RO.sh` implements remote RO-stage rows 10-23 and records row 24
as operator-side only. Repair round 5 was authorized under owner grant #7, which
lifts the T0 round cap for this block set until both flagships accept. It
answers the second-flagship Codex T0 audit
(`RP7_CODEX_T0_AUDIT_R4_2026-08-10.md`, BLOCK on three findings, one of them a
security-relevant false-PASS hole) plus two Lead-verified items carried from the
section-10.1 reconciliation. Acceptance belongs to the fresh cross-model
re-audit; Codex is the auditor of record for findings 1-3 and re-audits these
bytes, so implementer/auditor separation holds.

Material repair state added this round:

- **the trusted adjudicating `python3` is now bound in the production main
  path.** Round 4 accepted the tenth pin, included it in projection v2 and
  defined its required binding, but the only production binding loop listed nine
  tools. The unbound executable then ran at both adjudicators while the block
  printed `adjudicator=pinned_system_interpreter` and
  `parser=pinned_system_interpreter isolation=isolated_no_site`. Codex
  demonstrated a deviant executable writing a marker, forging `OK fields=8` over
  an `ARMED` body, and still reaching `RP7 PASS`. All TEN pins now pass through
  the one production loop in `wpi_main`, inside the initial mount window and
  before it closes. `-I -S` and the startup guards are unchanged; they only
  became load-bearing once the program interpreting them is the bound one;
- **package identity is semantically adjudicated before parity.** Admission
  proved object kind, ownership, byte readability and format - none of which is
  identity. `verify_lock.py:68-74` skips every distribution whose `METADATA`
  carries no `Name` and overwrites duplicate canonical names in a dict, so an
  admitted-but-malformed object silently left the universe it was admitted into
  and row 19 could print the accepting parity line for a set it never
  adjudicated. The byte-frozen verifier is untouched; the adjudication is in the
  block's trusted driver, which now requires exactly one grammar-valid `Name`
  and one `Version` per admitted `*.dist-info` and a unique canonical name
  across them, and STOPs at rc 6 with
  `B1_STOP reason=metadata_identity_unestablished stage=verifier detail=<t>
  name_sha256=<h>` otherwise. Absent, ambiguous, unparseable or duplicate
  identity is an inability to evaluate - never a silent omission, never a named
  `lock_installed_parity` FAIL;
- **the published evidence command is real.** The round-4 document's only
  "Exact command" was the literal placeholder `bash <fence-file>`, which is a
  syntax error at rc 2. Both fences are now delimited by unique content anchors
  (`# RP7_QA_FENCE_BEGIN`/`END`, `# RP7_R4_FENCE_BEGIN`/`END`) and extracted by a
  literal command that is itself anchored and extractable. No line numbers, no
  placeholders, no undeclared shell state;
- **the three `/dev/null` write opens are gone.** Two `command -v` prerequisite
  probes became a non-overridable `builtin type -t` function-type check - which
  needs no redirection and is strictly narrower, since an executable of the
  predicate's name on `PATH` no longer satisfies it - and the `noclobber`
  create-once probe closes fd 2 instead of redirecting it. `noclobber`
  semantics are intact and no diagnostic leaks;
- **evidence-root provenance is proved.** `EV_LOG` inside `EV_DIR` and every
  capture leaf inside `EV_DIR` bind nothing while `EV_DIR` itself is unbound.
  `wpi_assert_prerequisites` now STOPs, before any leaf is allocated, unless
  `EV_DIR` is a strict descendant of the frozen `WPI_FIXED_EVIDENCE_ROOT`, and
  the file-header mutation claim is narrowed to exactly that.

Local validation: literal Git Bash (MSYS2 bash 5.2.37, GNU coreutils 8.32,
CPython 3.14.2, git 2.52.0) - **two** fences, both extracted from
`SELF_QA_RP7.md` by the published anchored command and both `QA_PASS
all_assertions=yes` at rc 0 with empty stderr:

- the round-5 fence (`0263067e...5b62f`, 20050 B) drives every arm twice, once
  against the frozen round-4 blob `git cat-file blob d6a976aa:...` re-derived to
  70941 B / `23e55667...01aad` and once against these bytes, with a real RED and
  a real GREEN for findings 1, 2, 4 and 5;
- the round-4 fence (`94101ef7...56e0`, 76710 B) is carried unchanged except for
  its two anchor comments and re-run as the no-weakening gate: every round-3 and
  round-4 arm still passes on the round-5 bytes.

`bash -n` PASS. Zero CR bytes.

**FREEZE-GATE ITEMS (three, all carried deliberately).**

1. `WPI_FIXED_ATTESTED_MOUNT_PROJECTION_SHA256` is still `<PIN-AT-FREEZE>`, so
   there is no executed arm in which `wpi_validate_inputs` *accepts* a correct
   input set, and there cannot be one before freeze. The
   `normalised_path_projection_v2` digest the deploy channel must supply covers
   **21** point paths.
2. `WPI_FIXED_TRUSTED_PYTHON` is `<PIN-AT-FREEZE>`. `/usr/bin/python3` is a
   symlink on the target family and `wpi_bind_tool` admits no symlinked object,
   so the deploy channel must pin the resolved `/usr/bin/python3.<minor>`. The
   round-4 fence records the executed proof that an unresolved pin is refused
   (`tool_not_evaluable tool=python3 ... kind=symlink`, rc 3) rather than
   silently followed - and as of this round that refusal is reachable from the
   production path.
3. `WPI_FIXED_EVIDENCE_ROOT` is new and `<PIN-AT-FREEZE>`. Its value is
   `<REMOTE_BASE>/evidence`, and `REMOTE_BASE` is allocated at dispatch, so this
   pin carries an **ordering constraint Stage 1 must close**: the base must be
   allocated before the RO block is frozen and hashed, because a block frozen
   first cannot carry a base allocated later. If Stage 1 cannot reorder that,
   the honest outcome is to record that the RO block does not claim
   evidence-root provenance for this run - not to fill the pin with anything the
   run learns about itself.

The first action after the deploy channel supplies all three values, and before
dispatch, is to execute the accepting-input arm and record it. The block cannot
be frozen on the strength of this QA alone.

Final executable identity:

```text
bytes=77179
sha256=393a16ce264b467bec180a2106390e6dcee4dc2605fd019871270fda11d3b0ee
```

No host contact, network probe, SSH/SCP, RUNID minting, commit, deployment, or
change outside the round-5 authorized deliverables occurred.
