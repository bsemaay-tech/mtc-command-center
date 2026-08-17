Report file write blocked (`EPERM` — the pre-created placeholder is locked by another process). The kickoff's deliverable is the printed report, so here it is in full.

---

# RE-AUDIT — `RP7-WPI-RO.sh` round 2 (auditor 2, Claude Opus 5, 2026-08-10)

## BLOCK: 6 findings

Returning auditor, same instance that produced the round-1 BLOCK. Read-only: no host contacted, no socket opened, no network call, no RUNID minted, no repository file created, modified or deleted. All fixtures ran locally under `/tmp` in two environments and cleaned up after themselves.

**Execution environments.** (a) `GNU bash 5.2.37(1)-release (x86_64-pc-msys)`, `stat (GNU coreutils) 8.32` — the build whose `argv[0]`-prefixed diagnostic finding 1 was about. (b) Ubuntu WSL2, kernel `6.18.33.2-microsoft-standard-WSL2`, running as uid 0, `stat (uutils coreutils) 0.8.0` — the environment the repair's own QA used. Where a conclusion depends on the target host's coreutils build rather than on these, it is marked as such.

**13 of 13 round-1 findings are closed.** Every round-1 falsification fixture was re-run against the repaired bytes and every one now lands on the repaired outcome. The BLOCK is not a regression on the contract; it is one new defect that the adjudicated F11 fix introduced, plus five lower-severity residuals.

---

## V-item results

| V | Result | Evidence |
|---|---|---|
| **V1** F1 `wpi_lstat` ENOENT | **CLOSED** (executed) | Real repaired `wpi_lstat`, GNU 8.32, production invocation shape, genuinely absent leaf: rc 0, `F1a_KIND=absent`. Round-1 matcher restored as a mutant in the same environment: `B3_STOP … detail=unclassified_diagnostic`, rc 3 — the fixture still discriminates. Real `wpi_walk_components` over a real root-owned `0555` tree with an absent leaf: `B3_FAIL reason=path_absent`, rc 1 |
| **V2** F2 tool-binding outcome class | **CLOSED** (executed) | `wpi_bind_tool stat <symlinked-parent>` → `RP7_STOP reason=tool_not_evaluable tool=stat detail=path_metadata_mismatch … kind=symlink`, rc **3** (round 1: rc 1 `RP7_FAIL`). Tool owned `1000:1000` → rc **3** (round 1: rc 1). `WPI_TOOL_PINS` carrying `stat=/bin/stat` → `RP7_STOP reason=prereg_input_malformed name=WPI_TOOL_PINS.stat expected=/usr/bin/stat`, rc 3. Merged-`/usr` aliasing is now unreachable by construction: `:502` forces every pin to the literal `/usr/bin/<name>` |
| **V3** F3 unsafe pathname | **CLOSED** (executed) | Real `wpi_assert_tree` over a real `0555 0:0` tree containing a real regular file named with a space, real `find -perm /222 -print0`, real mount guard against a real 37-record `/proc/self/mountinfo`: `B3_FAIL reason=writable_path_inside_immutable_tree path=[unrenderable] path_sha256=0e959ec6…c5b7e2ad count=1`, rc **1** (round 1: rc 3 `structured_path_unparseable`) |
| **V4** F4 mount ordering + atomicity | **CLOSED** (executed) | Part A: `wpi_mount_guard_begin` is `wpi_main:881`, the `wpi_bind_tool` loop `:882-885`, evidence leaf `:887`, manager `:891`, `wpi_mount_guard_end` `:892` — the window now spans the whole preflight. Part B: in the V3 transcript `RP7_mount_projection` appears **twice** before `B3_FAIL`, i.e. `wpi_fail:50-52` ran `wpi_mount_guard_end` first; the FAIL line no longer carries a `binding=` claim at all. Downgrade proven with the real guard: moving one projected path's covering mount between begin and end gives `RP7_STOP reason=mount_topology_changed before=42976f30… after=24eefde1… format=normalised_path_projection_v1`, rc 3 |
| **V5** F5 QA coverage | **PARTIALLY CLOSED** | The stub-heavy suite is gone; `wpi_lstat`, `wpi_walk_components`, `wpi_bind_tool`, `wpi_parse_mountinfo`, `wpi_build_mount_projection`, `wpi_mount_guard_begin/end`, `wpi_sha_file`, `wpi_assert_interpreter`, `wpi_capture` and all four JSON arms now have executed arms. Four residual gaps remain — finding 2 |
| **V6** F6 budget enforcement | **CLOSED** (executed) | `/usr/bin/timeout` is the ninth pinned tool and wraps **every** child at `wpi_capture:197`. Real 8 s child against a 2 s budget: `B3_STOP reason=sweep_budget_exceeded root=/fixture elapsed_s=3 elapsed_ms=2190 budget_s=2`, rc 3, **wall clock 2 s**. Round 1's shape returned only after the child finished. Post-hoc gate retained at `:565`; `elapsed_s` emitted alongside `elapsed_ms` |
| **V7** F7 unbound inputs | **CLOSED** (code+diff) | `WPI_LOG_DIR` literal-pinned `/var/log/mtc-bridge` (`:491`) and draft §2 row filled with the Lead-pin origin. `WPI_INTERPRETER_TARGET` occurs **0 times** in the frozen bytes; `wpi_assert_interpreter` derives `<venv>/bin/python` from the pinned venv root and STOPs on any observed symlink (`:636-642`). `WPI_ATTESTED_MOUNTINFO_SHA256` is now literal-checked in-block against `WPI_FIXED_ATTESTED_MOUNT_PROJECTION_SHA256` (`:42`, `:511`) |
| **V8** F8 row grammar | **PARTIALLY CLOSED** | `walk_permission_error` deleted from row 13 with the Pattern-5 reason recorded; `elapsed_s`/`elapsed_ms` both emitted and both in row 12; `path_metadata_mismatch` unified to one field set at `:312/:316/:322/:328` and row 10 aligned to `expected=directory,555,0:0`; row 19a added for verifier identity; the three content-suppression renderings recorded. Five smaller deltas survive — finding 5 |
| **V9** F9 listener inventory | **CLOSED** (code + QA argv) | `wpi_assert_listener_set:778` runs `"$WPI_SS" -H -ltn` with no filter (`sport =` occurs 0 times in the file), retains the whole capture leaf as evidence (`:811` `evidence_file=… table=complete`), parses every row (`:783-809`), and applies the 8790 scope in-block at `:805`. QA records both argvs: `MUTANT_SS_ARGV=… sport = :8790` vs `PRODUCTION_SS_ARGV=listeners /usr/bin/ss -H -ltn` |
| **V10** F10 wrong-typed flag | **CLOSED** (executed) | Parser exit 5 → `B5_FAIL reason=flag_mismatch field=state_version observed_type=str expected_type=int`, rc 1; absent key → `B5_STOP reason=schema_unexpected field=state_version`, rc 3. Draft row 21 split to match. Re-run in my own execution of the QA fence: `JSON_RCS … wrong_type=1 … missing=3` |
| **V11** F11 mount object/projection | **CLOSED AS SPECIFIED — superseded by finding 1** | `/proc/self/mountinfo` is copied once into a create-once leaf (`:371-390`); that leaf is parsed and the derived projection is what gets hashed, so parse and digest share one object. The volatile whole-file digest is gone. But the projection that replaced it does not detect the substitution the binding exists to prevent — finding 1 |
| **V12** F12 log injection | **CLOSED** (executed) | `wpi_sanitize` now called 3× (`:557`, `:641`, plus its definition); QA transcript carries one physical line `B1_STOP reason=interpreter_object_unbound kind=symlink target=/decoy B1_interpreter path=spoofed exec=ok` — CR replaced by a space, no forged second line. Every other host-derived field reaching `printf` is grammar-constrained or digest-suppressed; one cosmetic exception in finding 5 |
| **V13** F13 field splitting | **CLOSED** (executed) | `set -f` at `:21`; `set -o` inside a sourced fixture reports `noglob on`; `wpi_parse_mountinfo` over a record with mount point `/mnt/*` and source `/dev/*` yields `F13_MOUNT_POINT=[/mnt/*] F13_SOURCE=[/dev/*]`, rc 0 |
| **V14** Regression | **PASS** | Round-1 V2 (ordering) re-verified at all 15 `wpi_capture` consumers: rc → complete diagnostic stream → stdout, no exception; `wpi_run_find` still adjudicates timeout → rc → stderr before `wpi_assert_tree` opens stdout; parity still gated behind `WPI_VENV_WALK_COMPLETE`/`WPI_INTERPRETER_RAN`/`WPI_METADATA_READABLE`; `wpi_assert_netns_binding` still precedes both `ss` and `curl`. Round-1 V6 holds with one new qualification — finding 6. Round-1 V8 re-derived below. QA fence re-run verbatim by me in WSL2: reproduces the recorded transcript line-for-line except the `mktemp` suffix and one 3010/3000 ms sample, terminating `QA_PASS all_assertions=yes`. `verify_lock.py` re-derived independently at the candidate: 3735 bytes, `d951e0ee…a451e5` — matches row 19a and the block's pin |
| **V15** Draft round 1.6 | **PASS** | 4 hunks, +22/−14 lines, confined to the five adjudicated subjects: §2 `WPI_LOG_DIR` row, the deploy-channel attestation paragraph, §8.2 rows 10/12/13/14/18/19/19a/21/22, and the path-object binding paragraph. No other row or paragraph touched. No weakening found: every edit narrows or adds obligation. `<PIN-AT-FREEZE>` intact at `RP7-WPI-RO.sh:42`; all 24 `<PIN-AT-STAGE-1>` / `<PIN-BEFORE-DISPATCH>` placeholders in the draft intact. One draft↔block disagreement in finding 1 |
| **V16** Byte identity | **PASS** | `sha256sum` → `ed9aa6b3c1caab1360bdde499ebc893eb431084a15b643a019fb98c4d8837cfa`; `wc -c` → `54001`. Both equal the kickoff's claims. `bash -n` rc 0. Round-1 baseline independently re-derived at `f503af55^`: `81a29241…`, 44198 B. Commit `f503af55` touches exactly the five authorised files |

---

## Findings

### 1. The normalised mount projection is blind to every mount below the 18 attested paths and to every mount stacked on an existing mount point — the decoy-substitution control it replaced is defeated — BLOCK

**Location** `wpi_build_mount_projection:392-424`, path list `:394-400`, covering-mount selection `:405-413`

**Defect, part A — subtree blindness.** The projection contains one record per path in a fixed 18-entry list: the nine tool pins, `WPI_RELEASE_ROOT`, `WPI_VENV_ROOT`, `WPI_UNIT_FRAGMENT`, `WPI_STATE_DIR`, `WPI_LOG_DIR`, `WPI_CONF_DIR`, and three `/proc` paths. The objects the block actually digests, executes and enumerates are **not** in that list:

- `<release>/IBKR_PAPER_BRIDGE/requirements.lock` (row 17)
- `<release>/IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py` (row 19a) — and the verifier the block then executes
- `<venv>/bin`, `<venv>/bin/python` (row 18) — the interpreter the block then executes
- `<venv>/lib/python3.12/site-packages` and every `*.dist-info` directory with its `METADATA` and `RECORD` (row 19)

A bind or overlay mount at any of those points changes no projected record, because the covering mount of `WPI_RELEASE_ROOT` and `WPI_VENV_ROOT` is unchanged. Round 1's whole-file `mountinfo` digest detected it — any new record changed the digest. The repair removed that detection while fixing the volatility, so the binding rule's stated purpose, "an overlay or bind mount cannot substitute a decoy object", is no longer met for the exact objects the block trusts.

**Defect, part B — shadowed mounts.** `:411` selects the covering mount with `-gt`, so on a tie the **first** matching record wins. In `/proc/self/mountinfo` a later record at the same mount point shadows the earlier one, so the projection describes the mount that is *not* serving the path. Stacking a second mount on any existing mount point — `/`, `/usr`, `/proc` — leaves the digest unchanged. This half is also a plain correctness defect independent of any attacker: which record the projection describes is decided by list order, not by which mount is effective.

**Falsification (executed).** Against a **real** 37-record `/proc/self/mountinfo` captured by the block's own `wpi_capture_mountinfo_snapshot`, with one appended record representing a bind mount at `<release>/IBKR_PAPER_BRIDGE`:

```
N1_REAL_MOUNTINFO records=37
  clean_projection               =42976f303b66d23a8afeafe40366cbf289d334a5dac3b67438eb6e408301261c
  with_decoy_bind_under_release  =42976f303b66d23a8afeafe40366cbf289d334a5dac3b67438eb6e408301261c
  equal=YES_UNDETECTED
N1_WHOLEFILE_ROUND1 clean=f64d4d1a7480bf4b decoy=ce8edca1c91765ef equal=no
```

and on synthetic tables (GNU 8.32), part B:

```
N2_PROJECTION clean=64e7ac44581a5ddb stacked=64e7ac44581a5ddb
N2_VERDICT=PROJECTION_BLIND_TO_STACKED_MOUNT (round1 whole-file digest DID differ: yes)
```

**Why this is mine to own.** My round-1 minimal fix said "a normalised projection … for each preregistered path's covering mount". The implementation follows that text exactly; the text under-specified the path set and said nothing about tie-breaks. The draft's new attestation paragraph inherits the same gap — it promises "one ordered TSV record per preregistered path" while the block's probed-object set is far larger, so §8.2 and the implementation now disagree about what "preregistered path" means.

**Minimal fix.** Two parts, both cheap:

1. **Subtree closure, not point lookup.** For each preregistered root (`WPI_RELEASE_ROOT`, `WPI_VENV_ROOT`, `WPI_CONF_DIR`, `WPI_STATE_DIR`, `WPI_LOG_DIR`, and each tool's directory) emit, in addition to the covering-mount record, every `mountinfo` record whose mount point is at or below that root, in `mountinfo` order, plus their count. A decoy mount anywhere inside a trusted subtree then changes the digest. Add the two literal file paths (`requirements.lock`, `verify_lock.py`) to the point list as well.
2. **Effective mount, not first match.** Change `:411` to `-ge` so the last matching record wins, and emit the number of records sharing the winning mount point so a stack is visible in the projection rather than silently collapsed.

Then update the draft's attestation paragraph to define the record set as `normalised_path_projection_v2` = point records ∪ subtree closure ∪ per-root counts, and re-record what the deploy channel must attest.

---

### 2. Self-QA residuals: the repaired F1 arm the target host will actually take has zero executed coverage, F4's RED arm is a placebo, and no arm accepts a valid input set — MEDIUM

**Location** `SELF_QA_RP7.md:44-67`, `:117`, `:89`, `:96-103`, `:163-177`

**Defect.** The suite is a large improvement and I confirmed it re-runs verbatim. Four gaps remain, the first material.

**(a) The F1 GREEN arm proves the wrong branch.** The fence ran on **uutils coreutils 0.8.0**, whose diagnostic is `stat: cannot stat 'X': No such file or directory (os error 2)` — basename prefix. The repair's *primary* alternatives are the `"$WPI_STAT: …"` forms, i.e. the absolute `argv[0]` prefix, and those are the only forms a GNU coreutils host produces — which is what the Debian 12 target ships. The fence's own mutant proves the point: it accepts **only** the absolute-prefix literals and it RED-ed (`detail=mutant_prefix_miss`). So the executed evidence for finding 1's repair covers a branch the target host will never take, and the branch the target *will* take was never executed. I closed this gap myself on GNU 8.32 (`F1a_KIND=absent`, rc 0), so it is a QA-coverage defect, not a code defect — but the QA as written would pass identically if the `"$WPI_STAT: …"` alternatives had been left out.

**(b) F4's RED arm is theatre.** `:117` is `( printf 'MUTANT_FAIL reason=fixture_without_guard_close\n'; exit 1 )` — a `printf`, not the pre-fix code path. It cannot fail and it demonstrates nothing about `wpi_fail`. The `changed_downgrade` / `stable_fail` arms carry the real signal; the `mutant_no_close=1` value in the recorded vector is not evidence.

**(c) No GREEN `wpi_validate_inputs`.** `:89` is the only arm that drives it and it is RED. There is no executed proof that a *correct* input set is accepted; a block that rejected every input would pass this QA unchanged. (It is currently impossible to write that arm, because `WPI_FIXED_ATTESTED_MOUNT_PROJECTION_SHA256` is still `<PIN-AT-FREEZE>` — correct by design, but it means the gap must be closed at freeze, not deferred past it.)

**(d) Two real guards still stubbed.** `:98-100` and `:165/:170/:175` replace `wpi_mount_guard_begin/end` with no-ops, so `wpi_assert_tree`'s and `wpi_assert_interpreter`'s own guard call sites are never executed by the QA. I executed both against a real 37-record mount table (V3/V4 above), so the code is fine; the QA does not show it.

**Minimal fix.** (a) Run the F1 GREEN arm under a GNU coreutils build, or add a fixture supplying a `WPI_STAT` wrapper that emits each of the six accepted literals and asserts `absent` for all six, RED on a seventh. (b) Replace `:117` with the actual pre-fix `wpi_fail` body (print-then-exit, no guard close) and assert `MOUNT_WINDOW_CLOSED` absent. (c) Add the accepting `wpi_validate_inputs` arm as a freeze-gate item. (d) Drop the guard stubs in the two arms and supply a computed attestation, as in V3/V4.

---

### 3. The hoisted guard doubles the self-attesting tool set, and all nine bindings still print `resolution=pinned_absolute` without disclosing it — MEDIUM

**Location** `wpi_main:881-885`, `wpi_bind_tool:467`, `wpi_capture:197-198`

**Defect.** Round-1 observation 1 noted that `stat` and `env` prove their own integrity by running themselves. The adjudicated F4 hoist and the F6 `timeout` pin extend that set: `wpi_mount_guard_begin` at `:881` runs `wpi_capture_mountinfo_snapshot` and `wpi_build_mount_projection`, and the latter calls `wpi_sha_file` → `wpi_capture`, which execs `$WPI_TIMEOUT`, `$WPI_ENV` and `$WPI_SHA256SUM` — before a single `RP7_tool` line is emitted. The first `wpi_bind_tool` then execs `$WPI_STAT` to bind `$WPI_STAT`. Four of nine tools are therefore trusted before they are bound, and `:467` prints `resolution=pinned_absolute` identically for all nine.

This is a direct and unavoidable consequence of my own round-1 minimal fixes — the mount comparison needs a digest, and a digest needs `sha256sum`. It is not a repair error. It is an evidence-truthfulness gap: the printed token asserts a property four tools did not earn.

**Minimal fix.** Emit `resolution=pinned_absolute attestation=self` for `stat`, `env`, `sha256sum` and `timeout`, `attestation=bound_instrument` for the other five, and state the limitation in the draft's binding paragraph so it is disclosed in evidence rather than discovered at adjudication.

---

### 4. The ENOENT match was widened beyond the invocation the block controls — LOW

**Location** `wpi_lstat:243-245`

**Defect.** My round-1 fix said "keep exact matching, parameterise it". The repair parameterised it and additionally accepts four unparameterised forms: the bare basename with both `stat` and `statx` wordings, and two `(os error 2)` suffixed forms. The block execs an absolute `argv[0]` that `wpi_require_absolute` has already validated, so on any GNU build the basename forms are unreachable; they exist only to satisfy the uutils build the QA happened to run on. The cost is that a diagnostic which does **not** come from the pinned tool — e.g. a wrapper or a shell function shadowing it in a future refactor — is now accepted as proof of absence. Small, but it is exactly the exactness property finding 1 was written to preserve.

Asymmetry worth noting: `(os error 2)` is accepted only for the `stat` wording, not the `statx` wording. Nothing produces the missing combination today; the set is simply not closed under its own rule.

**Minimal fix.** Keep only the two `"$WPI_STAT: …"` forms plus, if uutils support is genuinely wanted, `"$WPI_STAT: … (os error 2)"`. Drop the basename alternatives, or gate them behind an explicit `WPI_TOOL_DIAGNOSTIC_STYLE` pin recorded in §2.

---

### 5. Residual row-grammar deltas after the F8 pass — LOW

**Location** multiple

**Defect.** Section 8.2 still calls its right-hand column the *exact* predicted first divergence. Remaining deltas:

- **`binding=` vocabulary is emitted but preregistered nowhere.** Six spellings across the block — `component_and_mount` (×2), `component_and_mount_window_closed` (×2), `component_mount_digest_window_closed`, `window_open_pending_close`, `separate_bounded_exec` (×2), `equal` — and §8.2 records none of them. Three were *introduced* by the observation-4 disclosure fix, so the fix added undeclared grammar.
- **Row 17 has no byte-count FAIL grammar.** `:624` emits `installed_lock_digest_mismatch observed_bytes=<n> expected_bytes=117762`; row 17 records only the `observed=<h>` digest form. Row 19a records both — row 17 was missed.
- **`observed=non_preregistered_address` is unpreregistered.** `:807` emits `B6_FAIL reason=listener_set_unexpected observed=non_preregistered_address expected=…`; row 22 records only `observed_count=<n>` as the accepted rendering.
- **Row 19 does not admit `B1_FAIL reason=path_metadata_mismatch`.** `:675` and `:694` run `wpi_walk_components` with the default FAIL outcome over `site-packages` and each `*.dist-info`, so a deviant component there emits a token row 19 never preregistered.
- **Raw `%F` reaches a `key=value` token.** `:287` and `:646` interpolate `$WPI_META_KIND` unmapped, so a device node yields `detail=root_kind_character special file` and `kind=character special file target=none` — multi-word values inside a space-delimited grammar. `wpi_kind_token` exists and is used elsewhere; these two sites skip it.

**Minimal fix.** One more reconciliation pass: declare the `binding=` token set in the draft (it is now load-bearing evidence), add the byte-count form to row 17, add `observed=non_preregistered_address` to row 22 or fold it into `observed_count`, extend row 19's grammar to the component-walk FAIL, and route `:287`/`:646` through `wpi_kind_token`.

---

### 6. `timeout` is the one child not run with a cleared environment — LOW

**Location** `wpi_capture:197-198`

**Defect.** The wrapper is `exec "$WPI_TIMEOUT" … "$WPI_ENV" -i LC_ALL=C PATH=… "$@"`, so `timeout` itself inherits the block's full environment and only the probe beneath it is env-cleared. Round-1 V6 passed on the statement that `wpi_capture` runs *every* child under `env -i`; that statement now needs a qualification. Practical exposure is small — the block exports `LC_ALL=C` at `:22` and GNU `timeout` reads little else — but the invariant is weaker than the evidence claims, and `timeout` is the process that decides whether a probe was bounded.

**Minimal fix.** Either invert to `exec "$WPI_ENV" -i … "$WPI_TIMEOUT" … "$@"` (the pin is absolute, so `env` can exec it directly), or amend the draft's execution-environment paragraph to state that the bounding wrapper runs outside the cleared environment.

---

## Additional observations — not counted as findings

1. **An unbound variable under `set -u` exits rc 1 and bypasses the ERR trap.** Executed: `UNSET_VAR_EXIT_RC=1`. rc 1 is FAIL grammar — "a completed probe established deviant host state". I found no reachable trigger in the frozen bytes (every late-bound global is assigned on all paths that read it), so this is not a finding; it is a standing hazard worth knowing before the next refactor adds a conditional assignment.
2. **Evidence volume grew again.** Each `wpi_mount_guard_begin`/`end` pair now adds a `mountinfo` snapshot leaf, a projection leaf and one `sha256sum` child; there are ten guard pairs, on top of the ~800 captures in `wpi_assert_metadata_readable`. Each guard also prints two `RP7_mount_table` / `RP7_mount_projection` lines, so the evidence log gains ~40 preflight lines before any row result.
3. **Three of the eighteen projection records are inert.** `/proc/self/mountinfo`, `/proc/self/ns/net` and `/proc/<MAINPID>/ns/net` always resolve to the `/proc` mount, so they contribute a constant to the digest and no signal.
4. **`elapsed_s` ceilings can read oddly.** `(ms+999)/1000` produced `elapsed_s=2 … budget_s=1` for an 1100 ms sweep in both the QA and my own runs. Harmless — the enforcement test is on `ms` — but the emitted pair looks self-contradictory.
5. **The block cannot execute end-to-end until `<PIN-AT-FREEZE>` is replaced.** `:511` compares the wrapper's attestation against the placeholder, so `wpi_validate_inputs` necessarily STOPs. Correct by design, and correctly disclosed in the repair report — but it means no whole-block GREEN run exists or can exist before freeze, which is why finding 2(c) has to be a freeze-gate item rather than a QA to-do.
6. **`wpi_is_structured_parity_mismatch` and the `verify_lock.py` binding remain the strongest part of the block**, unchanged and re-verified: 3735 bytes, `d951e0ee…a451e5` at the candidate, matching row 19a and `WPI_VERIFY_LOCK_SHA256`.

---

## What I could not evaluate

- Nothing was executed against the staging host, and nothing in this re-audit required it.
- Neither the QA nor I executed the `cannot statx` wording. The QA's environment is uutils (`cannot stat … (os error 2)`); mine is GNU coreutils 8.32 (`cannot stat`, absolute prefix). Debian 12 ships coreutils 9.1, which uses `statx` on a glibc that provides it. The block matches both wordings and both prefixes, and the `argv[0]` reasoning is build-independent, but the target-host transcript does not exist and I am not asserting one.
- The mount findings were falsified against a real 37-record WSL2 `mountinfo` and synthetic tables. I did not create, and had no authority to create, a real bind mount; parts A and B were demonstrated by appending the record such a mount would produce.
- `RP0-BOOTSTRAP.sh` was again not read; `EV_DIR`/`EV_LOG` assumptions were taken from `run_ro.sh` and the prereg.
- Rows 1–9 (P0, B2, B4) remain out of this block's scope.

---

## Recommended next steps

1. **Default path — dispatch repair round 3 to Codex, scoped to finding 1 only.** It is one function (`wpi_build_mount_projection`) plus one draft paragraph. Findings 2–6 fold in as the same round's secondary list. This is the shortest route to PASS.
2. Alternative: adjudicate finding 1's minimal fix first (the subtree-closure record set changes what the deploy channel must attest, so it is a Lead decision, not an implementer's), then dispatch.
3. Alternative: accept findings 3–6 as documented limitations and repair only 1 and 2. Cheapest, but leaves undeclared grammar in a table the block calls exact.
4. The report file `RP7_CLAUDEPRO_REAUDIT_R2_2026-08-10.md` is still 0 bytes — the write was refused with `EPERM` (another process holds it). Someone needs to close that handle, then the text above can be saved verbatim.

**Owner ask, plain language:** the repair fixed all thirteen problems I found last time — I re-ran every test and they all pass now. But the new mount check has a hole: it only watches 18 specific folders, and the files the script actually trusts live *below* those folders, where the check is blind. I proved it — a fake folder swapped in under the release directory is invisible to the new check, while the old check caught it. That has to be fixed before this block can be frozen.
