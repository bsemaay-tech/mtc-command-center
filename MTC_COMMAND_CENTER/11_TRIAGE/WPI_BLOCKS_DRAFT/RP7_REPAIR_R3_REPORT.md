# RP7-WPI-RO repair round 3 report

Date: 2026-08-10
Implementer: Claude Opus 5 (xhigh), direct under owner amendments A2/A2a - no
sub-delegation, no counterpart implementer, no sub-agent.
Input audit: `RP7_CLAUDEPRO_REAUDIT_R2_2026-08-10.md` (BLOCK, 6 findings, baseline
`ed9aa6b3c1caab1360bdde499ebc893eb431084a15b643a019fb98c4d8837cfa`, 54001 B - both
re-derived at session start and matched before any edit).
Round: **3 of 3** under the T0 cap. Disposition: **6/6 implemented; pending fresh
independent cross-model re-audit.**

No staging host was contacted, no network connection opened, no SSH/SCP call made, no
RUNID minted, and no commit created. QA executed locally in Git Bash.

## Finding dispositions

| Finding | Disposition | Executable change | Evidence |
|---|---|---|---|
| **F1** (BLOCK) - projection blind to subtrees and to stacked mounts | Closed | `wpi_build_mount_projection` rewritten as `normalised_path_projection_v2`. Three record kinds: `kind=point` (20 paths - the previous 18 plus `<release>/IBKR_PAPER_BRIDGE/requirements.lock` and `…/deploy/linux/verify_lock.py`) carrying the **effective** covering mount and `shared_mount_point_records=<n>`; `kind=subtree` (every mountinfo record at or below each preregistered root, in mountinfo order); `kind=subtree_count` per root. Roots: `WPI_RELEASE_ROOT`, `WPI_VENV_ROOT`, `WPI_CONF_DIR`, `WPI_STATE_DIR`, `WPI_LOG_DIR`, then each tool's directory, deduplicated on first appearance (6 under the pinned `/usr/bin` set). Tie-break `-gt` → `-ge`, so the **last** longest match wins - the record that is actually serving the path. Guard messages carry `format=normalised_path_projection_v2`. | `SELF_QA_RP7.md` → `N1_V2` / `N1_V1_ROUND2`, `N2_V2` / `N2_V1_ROUND2`, `V2_RECORD_SHAPE`, `V2_EFFECTIVE_MOUNT`, `V2_SUBTREE_USR_BIN`. Both auditor falsifications flip; the verbatim round-2 body, executed on the same tables, stays blind to all four decoys. |
| **F2(a)** - GNU-prefix branch had no executed coverage | Closed | none (QA defect) | QA moved from WSL2/uutils to **Git Bash / GNU coreutils 8.32**. `REAL_GNU_DIAGNOSTIC` + `REAL_GNU_ABSENT`: production `wpi_lstat` classifies a real absent object `absent` from the real absolute-`argv[0]` diagnostic, no fixture in the path. `STAT_DIAGNOSTIC_RCS` then drives seven wrapper fixtures: three accepted forms → rc 0 `absent`; three basename forms + one foreign diagnostic → rc 3 `unclassified_diagnostic`. |
| **F2(b)** - RED arm was a placebo `printf` | Closed | none (QA defect) | The mutant is now `wpi_fail`'s verbatim pre-fix body. `FAIL_GUARD_CLOSE mutant_rc=1 mutant_window_closed=0 production_rc=1 production_window_closed=1`. The marker is emitted by a wrapper *around* the real `wpi_mount_guard_end` (installed via `declare -f` rename), so no stub can manufacture it. |
| **F2(c)** - no accepting `wpi_validate_inputs` arm | **Recorded as freeze-gate item, not faked** | none | Impossible before freeze by design: `WPI_FIXED_ATTESTED_MOUNT_PROJECTION_SHA256` is `<PIN-AT-FREEZE>`, so validation necessarily STOPs. Recorded in `STATUS_RP7.md` as the first action after the deploy channel supplies the v2 digest and before dispatch. |
| **F2(d)** - two real guards still stubbed | Closed | none (QA defect) | Every guard stub deleted. The unsafe-pathname arm, a new real-`find` arm, and all four interpreter arms run the real `wpi_mount_guard_begin`/`end` against a computed attestation (`COMPUTED_ATTESTATION`; per-arm `compute_attestation` where the arm pins fixture tools, since the projection covers the tool pins). `MOUNT_GUARD_RCS changed_downgrade=3 attestation_mismatch=3`. |
| **F3** (MEDIUM) - undisclosed self-attestation | Closed | `wpi_bind_tool` emits `attestation=self` for `stat`, `env`, `sha256sum`, `timeout` and `attestation=bound_instrument` for the other five, on the existing `RP7_tool` line. Disclosed in the draft's binding section. | `TOOL_ATTESTATION … self=4 bound_instrument=5 self_names=stat,env,sha256sum,timeout,`; the executed pre-fix line `MUTANT_RP7_tool` carries no `attestation=` field. |
| **F4** (LOW) - ENOENT match widened | Closed | `wpi_lstat` accepts only `"$WPI_STAT: cannot statx …"`, `"$WPI_STAT: cannot stat …"` and `"$WPI_STAT: cannot stat … (os error 2)"`. The three basename spellings are removed. | `STAT_DIAGNOSTIC_RCS base_statx=3 base_stat=3 base_oserr=3` against `abs_*=0`. |
| **F5** (LOW) - residual row grammar | Closed | Code: `:287` and `:646` (now `:294` / `:715`) route `$WPI_META_KIND` through `wpi_kind_token`, which gains an explicit `absent` case so the root-kind STOP keeps that distinction. Draft: `binding=` vocabulary declared, row 17 byte-count FAIL form, row 22 `observed=non_preregistered_address`, row 19 component-walk FAIL grammar. | `REAL_CHARDEV raw=[character special file] token=[other]`; production `detail=root_kind_other` and `kind=other target=none` against the executed `MUTANT_B3_STOP` / `MUTANT_B1_STOP` multi-word renderings; `LISTENER_RCS non_preregistered_address=1`. |
| **F6** (LOW) - `timeout` outside the cleared environment | Closed by **inversion** (the finding's preferred option) | `wpi_capture` now execs `"$WPI_ENV" -i … "$WPI_TIMEOUT" … "$@"`. | `TIMEOUT_ENV mutant_marker=1 mutant_vars=104 production_marker=0 production_vars=10` - the bounding process records its own environment, and the round-2 ordering (carried verbatim as `mutant_capture_timeout_outside_env`) leaks the block's environment including the `WPI_QA_ENV_MARKER` sentinel. Bound preserved: `TIMEOUT_RCS … production_wall_s=2 budget_s=2 child_sleep_s=8`, rc 124 → `sweep_budget_exceeded`. |
| **Observation 4** - `elapsed_s` ceiling reads oddly | Applied | `(ms+999)/1000` → `ms/1000` at both sites, so `elapsed_s` is the truncated rendering of the `elapsed_ms` printed beside it. Enforcement unchanged (milliseconds). | Transcript: `elapsed_s=2 elapsed_ms=2200 budget_s=2` and `elapsed_s=8 elapsed_ms=8080`. |
| **Observation 1** - late-bound globals | Honoured | No conditional assignment of a late-bound global added. The single new local (`attestation`) is assigned on every branch of its `case`, default included. | Code review of the diff; `bash -n` rc 0. |

### One deliberate deviation from the finding text, stated plainly

F2(a) asked for a wrapper emitting **each of the six accepted literals**, asserting
`absent` for all six and RED on a seventh. F4, in the same round, removes three of those
six. The arm therefore drives **all seven** forms and asserts `absent` for the three that
survive F4 and STOP for the four that do not - which is the same test with the two
findings composed, and it is what makes F4 falsifiable rather than merely asserted.

F4's minimal fix also left the `statx` + `(os error 2)` combination out of the accepted
set. That asymmetry is retained on purpose: uutils emits the `stat` wording with that
suffix and GNU emits neither, so no build produces the missing combination, and adding
it would widen the accepted set without a producer - the opposite of the finding.

## D026 RED/GREEN record

Every round-3 repair has an executed pre-fix RED arm and a repaired GREEN arm in the same
environment, and in three cases the RED arm is the round-2 source text carried verbatim
into the fence: `mutant_build_mount_projection_v1` (F1), the pre-fix `wpi_fail` body
(F2b), and `mutant_capture_timeout_outside_env` (F6). Every mutation is named `mutant_`
and exists only inside the QA fence; the repaired code was never reverted in the
worktree. Key vectors from the final run:

```text
STAT_DIAGNOSTIC_RCS real_gnu_absent=0 abs_statx=0 abs_stat=0 abs_oserr=0 base_statx=3 base_stat=3 base_oserr=3 foreign=3
N1_V2 clean=0d38de2c… decoy_bind_under_release=48e028dc… decoy_overlay_under_venv=b2e860b2… repeat_clean=0d38de2c…
N1_V1_ROUND2 clean=226bfa6e… decoy_bind_under_release=226bfa6e… decoy_overlay_under_venv=226bfa6e…
N2_V2 clean_root=bef3c8a7… stacked_on_root=62c61047… clean_usr_bin=6a99b695… stacked_on_usr_bin=7cefa0fb…
N2_V1_ROUND2 clean_root=309e1645… stacked_on_root=309e1645… clean_usr_bin=8b4f25af… stacked_on_usr_bin=8b4f25af…
V2_RECORD_SHAPE points=20 subtree=2 subtree_count=6
V2_EFFECTIVE_MOUNT kind=point path=/usr/bin/stat device=0:97 root=/ mount_point=/usr/bin fstype=tmpfs source=/dev/decoytools shared_mount_point_records=2
FAIL_GUARD_CLOSE mutant_rc=1 mutant_window_closed=0 production_rc=1 production_window_closed=1
MOUNT_GUARD_RCS changed_downgrade=3 attestation_mismatch=3
UNSAFE_PATH_RCS mutant_stop=3 suppressed_render_fail=1 real_find_fail=1
TOOL_ATTESTATION mutant_rc=0 mutant_attestation_fields=0 production_rc=0 self=4 bound_instrument=5 self_names=stat,env,sha256sum,timeout,
KIND_TOKEN_RCS real_chardev=0 root_kind_stop=3 interpreter_kind_stop=3 root_token_ok=1 interpreter_token_ok=1
TIMEOUT_ENV mutant_marker=1 mutant_vars=104 production_marker=0 production_vars=10
TIMEOUT_RCS mutant=3 production=3 mutant_wall_s=8 production_wall_s=2 budget_s=2 child_sleep_s=8
INTERPRETER_RCS regular_pass=0 symlink_stop=3 cr_stop=3 cr_forged_lines=0 cr_single_sanitised_line=1
JSON_RCS mutant_wrong_type=3 good=0 nan=3 infinity=3 wrong_type=1 top_array=3 mismatch=1 missing=3
LISTENER_RCS mutant_filtered=0 production_full_inventory=0 non_preregistered_address=1
REGRESSION_RCS manager_stop=3 partial_walk_stop=3 parity_fail=1 parity_generic_stop=3 netns_stop=3 http_fail=1
QA_PASS all_assertions=yes
```

## QA environment change, and what it costs

The kickoff required local Git Bash execution, which is also the fix for F2(a): MSYS2
ships **GNU coreutils 8.32**, the target's build family, so the absolute-`argv[0]`
diagnostic branch is now executed rather than reasoned about. The cost is that MSYS2 has
no root, mounts NTFS `noacl` (so `chown 0:0` and `chmod 0555` are no-ops), and cannot
create a POSIX symlink or a character device at an arbitrary path. Three fixture classes
close exactly those gaps and nothing else - a `stat` shim that substitutes only numeric
ownership and, per named variant, one path's `%F` kind; a `readlink` shim that supplies
the target string; and CRLF→LF normalisation of the Windows CPython child. Each is
tabulated in `SELF_QA_RP7.md` with what stays real. The round-2 WSL2 transcript is **not**
republished: round-3 edits change several of its recorded lines, so carrying it forward
would be stale evidence rather than extra coverage.

## Draft edits - exhaustive list

Six hunks, +78/−16 lines, all within the subjects a finding's fix names:

1. §4 deploy-channel attestation paragraph - `normalised_path_projection_v1` replaced by
   the full `normalised_path_projection_v2` definition: three record kinds, the twenty
   point paths in order, the effective-mount and `shared_mount_point_records` rule, the
   six-root subtree closure and per-root counts, why the closure is load-bearing, and the
   explicit statement that the deploy channel must attest the complete v2 record set (F1).
2. §8.2 row 17 - byte-count FAIL form
   `observed_bytes=<n> expected_bytes=117762`, adjudicated before the digest form (F5).
3. §8.2 row 19 - the component-walk FAIL grammar for `site-packages` and each
   `*.dist-info` directory (`path_absent`, `path_metadata_mismatch`) (F5).
4. §8.2 row 22 - `observed=non_preregistered_address` recorded as an accepted
   content-suppressed rendering beside `observed_count=<n>` (F5).
5. Path-object binding rule - points at the v2 record set; adds the **preregistered
   `binding=` vocabulary** (all seven spellings, each defined) and the
   **instrument-attestation disclosure** (which four tools are `attestation=self` and
   why) (F5, F3).
6. Probe execution-environment rule - states that the bounding wrapper is inside the
   cleared environment, `env` execing `timeout` and not the reverse (F6).

No other row or paragraph was edited. All 19 `<PIN-AT-STAGE-1>` / `<PIN-BEFORE-DISPATCH>`
placeholders are byte-identical to HEAD; `<PIN-AT-FREEZE>` remains intact at
`RP7-WPI-RO.sh:42`.

## Final validation and executable identity

```text
bash -n RP7-WPI-RO.sh   → rc 0
bytes                   → 58012
sha256                  → 1d118d1581534f5d16b3730efbe642e80e5232fbf8a245d238574907166a7f4e
```

Block diff versus the audited baseline: +90/−20 lines, confined to `wpi_capture`,
`wpi_lstat`, `wpi_kind_token`, `wpi_walk_components` (root-kind rendering only),
`wpi_build_mount_projection`, `wpi_mount_guard_begin`/`end` (format token only),
`wpi_bind_tool`, `wpi_run_find`, `wpi_assert_tree` and `wpi_assert_interpreter` (the `*)`
kind rendering only). No row logic, adjudication order, or STOP/FAIL classification was
changed anywhere else. `shellcheck` is not installed; no ShellCheck result is claimed.

## Deliverable boundary

Exactly the five kickoff-authorized files were touched:

1. `WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh`
2. `WPI_BLOCKS_DRAFT/SELF_QA_RP7.md`
3. `WPI_BLOCKS_DRAFT/STATUS_RP7.md`
4. `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md`
5. `WPI_BLOCKS_DRAFT/RP7_REPAIR_R3_REPORT.md`

No commit was created. This is the final round of the T0 cap: the next gate is a fresh
independent re-audit against these exact bytes and this literal QA fence, and if it does
not accept, the blocker goes to Barış rather than a fourth round.
