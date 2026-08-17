# RP7-WPI-RO repair round 2 report

Date: 2026-08-10
Implementer: Codex, direct under owner amendments A2/A2a
Input audit: `RP7_CLAUDEPRO_AUDIT_2026-08-10.md`
Disposition: **13/13 implemented; pending fresh independent cross-model re-audit**

No sub-agent or counterpart implementer was used. No staging host was contacted, no
network probe or SSH/SCP ran, no RUNID was minted, and no commit was created.

## Finding dispositions

| Finding | Disposition | Executable change | Evidence pointer |
|---|---|---|---|
| F1 — dead ENOENT arms | Closed | `wpi_lstat` exact-matches the supplied absolute `WPI_STAT` prefix and the exact basename forms observed across GNU/uutils builds, including the known `os error 2` suffix. | `SELF_QA_RP7.md` → `PATH_BINDING_RCS`: prefix-only mutant rc 3; real absent walk rc 1. |
| F2 — tool-binding FAIL class | Closed | `wpi_walk_components` has an explicit STOP outcome for tool binding; all nine pins must be exact `/usr/bin/<tool>` paths, preventing merged-`/usr` aliases. | `TOOL_BINDING_RCS`: inherited mutant rc 1; production rc 3; `/bin/stat` pin rc 3. |
| F3 — space pathname false STOP | Closed | Complete NUL records are classified first. Unsafe display bytes are written to a create-once evidence leaf, hashed, and rendered as `path=[unrenderable] path_sha256=<h> count=<n>`. Only non-absolute/structurally invalid records STOP. | `SPACE_PATH_RCS`: old grammar rc 3; repaired complete sweep rc 1 with digest and count. |
| F4 — mount ordering/atomicity | Closed | Initial guard begins before tool binding and remains open through tool/evidence/manager preflight. `wpi_fail` closes any active guard first; topology movement becomes `mount_topology_changed` STOP. Binding text now distinguishes pre-exec binding from the separately bounded exec. | `MOUNT_WINDOW_OPEN/CLOSED`; `MOUNT_GUARD_RCS`: changed projection rc 3, stable projection rc 1. |
| F5 — QA coverage | Closed | Replaced the stub-heavy suite with a literal WSL2/Linux fence covering real absent leaf, symlinked intermediate/leaf, wrong owner, wrong mode, tool binding, merged-`/usr`, real mount snapshot/projection, mount RED/GREEN, interpreter rows, and all requested JSON arms. | Complete executable fence and transcript in `SELF_QA_RP7.md`; terminal line `QA_PASS all_assertions=yes`. |
| F6 — post-hoc-only budget | Closed | `/usr/bin/timeout` is the ninth pinned/bound tool and wraps every `wpi_capture` child. The post-hoc monotonic gate remains. Both `elapsed_s` and `elapsed_ms` are emitted. | `TIMEOUT_RCS`: unbounded mutant wall 3 s; production wall 1 s at a 1 s budget, both classified STOP. |
| F7 — unbound inputs/interpreter | Closed for repair draft | `WPI_LOG_DIR` is literal `/var/log/mtc-bridge`; the block contains its own freeze-time literal projection-digest pin and rejects wrapper divergence; interpreter symlinks are never accepted or followed for execution. | Draft §2 pin; `WPI_FIXED_ATTESTED_MOUNT_PROJECTION_SHA256`; `INTERPRETER_RCS` (mutant symlink pass 0, production STOP 3, regular 0). The `<PIN-AT-FREEZE>` token must be replaced by the deploy-channel digest before freeze/dispatch, as designed. |
| F8 — row grammar drift | Closed | Unified `path_metadata_mismatch` fields; added `elapsed_s` beside `elapsed_ms`; deleted nonexistent `walk_permission_error`; added row 19a verifier identity; documented all three suppression renderings. | Draft §8.2 rows 10, 12–14, 18, 19/19a, 21–22; emitted lines throughout final QA transcript. |
| F9 — filtered listener inventory | Closed | Runs only unfiltered `ss -H -ltn`, retains the whole evidence leaf, parses every row, then scopes to port 8790 in block code. | `MUTANT_SS_ARGV` contains filter; `PRODUCTION_SS_ARGV` does not; production parses two rows and passes. |
| F10 — wrong type STOP | Closed | Missing key remains `schema_unexpected` STOP. Present wrong type is `flag_mismatch` FAIL with `observed_type` and `expected_type`. | `JSON_RCS`: wrong-type mutant 3, production 1; missing 3; mismatch 1; good 0. |
| F11 — mount object/projection | Closed | Each observation copies `/proc/self/mountinfo` once into a create-once leaf, parses and hashes that same leaf, builds a deterministic per-path covering-mount projection (`device`, `root`, `mount_point`, `fstype`, `source`), and compares its SHA-256. | `real_capture_projection=0` over real WSL `/proc`; synthetic changed/stable projection evidence in `MOUNT_GUARD_RCS`. |
| F12 — log injection | Closed | Interpreter symlink targets pass through `wpi_sanitize`; unsafe observed paths use digest suppression; other host-derived result fields are either grammar-constrained or sanitized. | `cr_sanitized_stop=3`; transcript contains one physical STOP line with CR replaced by a space. |
| F13 — active globbing | Closed | `set -f` is issued with the strict-mode prologue and remains active for both field-splitting parsers. | Mutant expands `/mnt/*` to `/mnt/c`; production preserves literal `/mnt/*`, rc 0. |

## D026 RED/GREEN record

The QA fence is self-contained and aborts on any unexpected rc. It was extracted without
editing from the first `bash` fence in `SELF_QA_RP7.md` and executed by Ubuntu WSL2 Bash.
Every mutation is named `mutant_` and exists only inside the QA fence. The final output is
recorded verbatim in the same document. The repaired code was not reverted in the worktree.

Key vectors from the final run:

```text
PATH_BINDING_RCS mutant_absent=3 absent=1 symlink_intermediate=1 symlink_leaf=1 wrong_owner=1 wrong_mode=1
TOOL_BINDING_RCS mutant_inherited_fail=1 production_stop=3 merged_usr_pin=3
SPACE_PATH_RCS mutant_stop=3 production_fail=1
MOUNT_GUARD_RCS mutant_no_close=1 changed_downgrade=3 stable_fail=1 real_capture_projection=0
TIMEOUT_RCS mutant=3 production=3 mutant_wall_s=3 production_wall_s=1
INTERPRETER_RCS mutant_symlink_accept=0 production_symlink=3 cr_sanitized_stop=3 regular=0
LISTENER_RCS mutant_filtered=0 production_full_inventory=0
JSON_RCS mutant_wrong_type=3 good=0 nan=3 infinity=3 wrong_type=1 top_array=3 mismatch=1 missing=3
REGRESSION_RCS manager_stop=3 partial_walk_stop=3 parity_fail=1 parity_generic_stop=3 netns_stop=3 http_fail=1
QA_PASS all_assertions=yes
```

## Draft edits — exhaustive list

Only Lead-adjudicated design text was changed:

1. §2 `WPI_LOG_DIR` input row — literal `/var/log/mtc-bridge` and Lead-pin origin.
2. External deploy-channel attestation paragraph — `normalised_path_projection_v1`
   record format and same-leaf capture/parse/hash rule.
3. §8.2 row 10 — exact unified metadata field spelling.
4. §8.2 row 12 — ninth `timeout` tool and dual elapsed fields.
5. §8.2 row 13 — removed `walk_permission_error`, recording the Pattern-5 reason.
6. §8.2 row 14 — unsafe valid pathname suppression grammar plus count.
7. §8.2 row 18 — non-symlink interpreter, symlink STOP, suppressed version rendering,
   and separate bounded-exec disclosure.
8. §8.2 row 19 — metadata path suppression and enumeration STOP routing.
9. §8.2 new row 19a — verifier identity/digest outcomes.
10. §8.2 row 21 — absent-key STOP versus wrong-type FAIL and digest suppression.
11. §8.2 row 22 — full unfiltered inventory evidence and `observed_count` suppression.
12. Path-object binding/attestation paragraph below §8.2 — non-symlink interpreter and
    exact normalized projection fields.

No other draft row or paragraph was edited.

## Final validation and executable identity

Commands:

```powershell
& 'C:\Program Files\Git\bin\bash.exe' -n 'MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh'
$i = Get-Item -LiteralPath 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_BLOCKS_DRAFT\RP7-WPI-RO.sh'
$i.Length
(Get-FileHash -Algorithm SHA256 -LiteralPath $i.FullName).Hash.ToLowerInvariant()
```

Output:

```text
bash_n_rc=0
bytes=54001
sha256=ed9aa6b3c1caab1360bdde499ebc893eb431084a15b643a019fb98c4d8837cfa
```

`shellcheck` was not installed in the Ubuntu guest, so no ShellCheck result is claimed.
The literal QA fence and `bash -n` are the executable validation evidence for this round.

## Deliverable boundary

Exactly the five kickoff-authorized files were touched:

1. `WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh`
2. `WPI_BLOCKS_DRAFT/SELF_QA_RP7.md`
3. `WPI_BLOCKS_DRAFT/STATUS_RP7.md`
4. `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md`
5. `WPI_BLOCKS_DRAFT/RP7_REPAIR_R2_REPORT.md`

No commit was created. Next gate: fresh independent cross-model re-audit against these
exact executable bytes and the literal QA fence.
