Audit complete. Full report follows.

---

# INDEPENDENT AUDIT — `RP7-WPI-RO.sh` (auditor 2, Claude Opus 5, 2026-08-10)

## BLOCK: 13 findings

Auditor: Claude Opus 5, standing in for GLM (quota window exhausted). Read-only. No host contacted, no socket opened, no network call, no RUNID minted, no repository file created, modified, or deleted. All fixtures ran locally under `/tmp/rp7-audit*.` and the session scratchpad.

**Execution environment for every transcript below:** `GNU bash 5.2.37(1)-release (x86_64-pc-msys)`, `stat (GNU coreutils) 8.32`. Where a conclusion depends on the target host's coreutils build rather than on this one, it is marked as such in the finding.

---

## V-item results

| V | Result | Evidence |
|---|---|---|
| **V1** Row coverage 10–23, exact FAIL/STOP grammar; row 24 operator-side | **FAIL** | Row 24 is correctly left operator-side (`wpi_record_external_probe_boundary`, no probe). But every `*_absent` FAIL in rows 10/11/15/17/18/19 is unreachable (finding 1); row 13's `walk_permission_error` appears 0 times in the file; row 12 emits `elapsed_ms=` where the row names `elapsed_s=`; row 19 emits four reason tokens the row never preregistered (finding 8) |
| **V2** Ordering | **PASS** | Adjudication order verified at all 13 `wpi_capture` consumers: rc → complete diagnostic stream → stdout, with no exception. `wpi_run_find` adjudicates elapsed → rc → stderr before `wpi_assert_tree` opens stdout. Parity is gated behind `WPI_VENV_WALK_COMPLETE`, `WPI_INTERPRETER_RAN`, `WPI_METADATA_READABLE` (`:521`, `:522`, `:587`), all set in the correct order by `wpi_main`. `wpi_assert_netns_binding` precedes both `ss` and `curl` (`:747`). Caveat: the budget half of row 12 is detection, not enforcement — finding 6 |
| **V3** Path-object binding rule | **FAIL** | Component-wise non-following walk, numeric ownership and `.`/`..` rejection are correctly implemented in `wpi_walk_components`. But the walk's absent-leaf arm is dead (finding 1), mount attestation is not established before the first filesystem or exec probe, and no FAIL path closes its mount window, so no FAIL is a mount-bound atomic observation (finding 4) |
| **V4** STOP-vs-FAIL truthfulness | **FAIL** | Three classes misclassified, each with executed falsification: findings 1, 2, 3. Finding 10 is a fourth, arguable case |
| **V5** Structured parsing / line-reader completion | **FAIL** | Strict JSON is genuinely strict — I falsified duplicate key, `NaN`, wrong type and top-level array; all four return rc 3, and the `flag_mismatch` FAIL arm returns rc 1. Both line readers distinguish clean EOF, unterminated populated final record, and hard read error; I re-ran both. The failure is row 22: the block runs `ss -H -ltn 'sport = :8790'` — a tool-side filter — where the row preregisters a complete table "structurally parsed into all socket rows", and R5 requires the full listener inventory as evidence (finding 9). Residual glob-active field splitting (finding 13) |
| **V6** Probe execution-environment rule; read-only scope | **PASS** | `wpi_capture` runs every child as `cd "$EV_DIR"; exec "$WPI_ENV" -i LC_ALL=C PATH=/usr/bin:/bin HOME=/nonexistent TMPDIR="$EV_DIR" <absolute argv[0]>`; both Python children use `-I`. `wpi_alloc_leaf` refuses any leaf outside `$EV_DIR` and is create-once under `noclobber`. No branch prints file content — diagnostics are referenced by path, JSON mismatches by digest, parity mismatches by a fixed token. Two qualifications below under "observations" |
| **V7** Self-QA re-runnable, RED cases falsify | **FAIL** | Reproducibility is **PASS**: I extracted the fence bytes verbatim (`sed -n '37,174p'`) and piped them to a fresh `bash --noprofile --norc`. Exit 0, **stderr empty**, output identical to the recorded transcript line-for-line except the `mktemp` suffix. The stated `RP0-LIB.sh` bytes/sha are correct (independently re-derived: 18968, `4a404d7b…`). The failure is coverage: the binding rule, the mount guard, tool binding, row 18 and the row-19 preflight have zero executed evidence (finding 5) |
| **V8** Byte identity | **PASS** | `sha256sum` → `81a292418d78a2fb6ed94435fb05d1e2b70124af0a469f73611b7a259cdc6c3c`; `wc -c` → `44198`. Both equal the kickoff's claims. `bash -n` clean |

---

## Findings

### 1. `wpi_lstat` cannot classify ENOENT under its own invocation contract — every preregistered `*_absent` FAIL is dead code — BLOCK

**Location** `RP7-WPI-RO.sh:196-200`

**Defect.** `wpi_lstat` recognises an absent path by exact-matching the captured diagnostic against two literals:

```
"stat: cannot statx '$path': No such file or directory"|"stat: cannot stat '$path': No such file or directory"
```

But `wpi_capture` (`:153`) execs the child as `exec "$WPI_ENV" -i … "$@"`, where `"$@"` begins with `$WPI_STAT` — an **absolute** path, enforced by `wpi_require_absolute` at `:311` and `:350`. GNU coreutils sets its error prefix from `argv[0]` verbatim, so the diagnostic is `/usr/bin/stat: cannot stat…`, never `stat: cannot stat…`. Neither literal can match. Every ENOENT therefore falls to the `*)` arm and becomes `path_not_evaluable … detail=unclassified_diagnostic`, rc 3.

This is `[AUDIT1 F5]` reconstructed exactly: a result that positively proves directory search succeeded and observes a missing preregistered path, emitted as an inability to evaluate. Pattern 1.

**Consequence.** Four preregistered FAIL outcomes become unreachable: `path_absent` (rows 10, 11, 15), `installed_lock_absent` (row 17), `interpreter_absent` (row 18), `distribution_metadata_absent` (row 19). A staging host with the release root deleted returns rc 3 "could not evaluate" instead of rc 1, burns its RUNID, and files a positively-observed host deviation as a tooling problem.

**Falsification (executed).** Real `wpi_lstat`, real `/usr/bin/env` and `/usr/bin/stat`, production invocation shape:

```
B3_STOP reason=path_not_evaluable path=/opt/mtc-bridge/releases/absent-leaf rc=1 detail=unclassified_diagnostic diagnostic_file=/tmp/rp7-audit.6hTsJD/f1/ro.0001.lstat.stderr
F1_LSTAT_ENOENT_RC=3 expected_for_absent_leaf=return0_then_FAIL_rc1
F1_STDERR_CAPTURED=[/usr/bin/stat: cannot stat '/opt/mtc-bridge/releases/absent-leaf': No such file or directory]
```

Same walk with the classification repaired (stub returning `absent`) reaches the truthful outcome:

```
B3_FAIL reason=path_absent path=/opt/mtc-bridge/releases/2ce41e34
F1b_WALK_ABSENT_LEAF_RC_WITH_REPAIRED_LSTAT=1
```

The prefix behaviour was confirmed here on coreutils 8.32; the target host's build (Debian 12 ships 9.1, which uses the `statx` wording) is not in reach of this audit. The conclusion is wording-independent: the block matches both wordings and **both** are prefixed with `argv[0]`.

**Minimal fix.** The block already knows the exact prefix it supplied. Keep exact matching, parameterise it:

```bash
"$WPI_STAT: cannot statx '$path': No such file or directory"|"$WPI_STAT: cannot stat '$path': No such file or directory")
```

Then add a self-QA arm that drives the real `wpi_lstat` against a genuinely absent path and asserts rc 1.

---

### 2. `wpi_bind_tool` emits `RP7_FAIL` rc 1 for tool-binding preconditions — an unpreregistered outcome class — BLOCK

**Location** `RP7-WPI-RO.sh:313` (`wpi_walk_components RP7 "$path" regular "" 0:0`)

**Defect.** `wpi_bind_tool`'s own explicit arms all STOP: `tool_not_evaluable … detail=not_executable` (`:312`), `detail=mode_grammar` (`:314`), `detail=group_or_world_writable` (`:315`). But the walk it delegates to inherits the default FAIL grammar, so a tool pin whose parent component is a symlink, whose leaf is a symlink, or whose leaf is not numerically root-owned exits rc 1 as `RP7_FAIL`.

Section 8.2 contains no `RP7` row and no `RP7_FAIL` grammar. Under the outcome contract, rc 1 means "a probe that ran observed deviant host state" and any FAIL is "a STOP requiring Lead adjudication — a candidate-repair question". An untrustworthy instrument is not a candidate defect; P0 rows 1 and 4–7 classify every tool problem as STOP. Pattern 1.

**Consequence, and why it is live.** `WPI_TOOL_PINS` is `<PIN-AT-FREEZE>` in `run_ro.sh:42` and nothing constrains it to `/usr/bin`. On a merged-`/usr` distribution — Debian 12 is one — `/bin` and `/sbin` are symlinks to `usr/bin` and `usr/sbin`. A Stage-1 pin table recording `ss` at `/sbin/ss` or any tool at `/bin/…` makes the RO stage exit rc 1 accusing the host of drift, on the first tool bound, before any row runs.

**Falsification (executed).**

```
RP7_FAIL reason=path_metadata_mismatch path=/usr kind=symlink expected=directory
G1_TOOL_PARENT_SYMLINK_RC=1 expected=3_STOP_tool_not_evaluable

RP7_FAIL reason=path_metadata_mismatch path=/usr/bin/stat owner_numeric=1000:1000 expected_owner_numeric=0:0
G2_TOOL_OWNED_BY_1000_RC=1 expected=3_STOP_tool_not_evaluable
```

A reason-token inventory over the frozen bytes shows no explicit `wpi_fail RP7` call anywhere — confirming the FAIL is unintended inheritance rather than a design decision.

**Minimal fix.** Give `wpi_walk_components` an outcome-class parameter, or call it from `wpi_bind_tool` with absent/object reasons that route to `wpi_stop`. Add the merged-`/usr` pin as a self-QA arm, and constrain `WPI_TOOL_PINS` at freeze to canonical non-symlinked directories.

---

### 3. A writable pathname containing a space STOPs instead of FAILing — row 14's FAIL is evadable — BLOCK

**Location** `RP7-WPI-RO.sh:442` and `:538`, via `wpi_require_observed_path_grammar:100`

**Defect.** `find … -perm /222 -print0` emits raw pathnames; a space is a legal filename byte. `wpi_require_observed_path_grammar` STOPs on `*[[:space:]]*`, so a writable file named with a space inside the release or venv tree produces `structured_path_unparseable`, rc 3, rather than row 14's `B3_FAIL reason=writable_path_inside_immutable_tree`. The sweep was complete, rc 0, diagnostics empty — the deviant state was positively observed and is reported as an inability to evaluate. Pattern 1. The same grammar sits on the row-19 metadata enumeration.

**Falsification (executed).** Author's own accepted RED harness, one byte changed in the fixture pathname:

```
B3_path path=/fixture kind=directory mode=555 owner_numeric=0:0 binding=component_and_mount
B3_STOP reason=structured_path_unparseable source=find_stdout detail=unsafe_character
F2_WRITABLE_PATH_WITH_SPACE_RC=3 expected=1_FAIL
```

and for row 19:

```
B1_STOP reason=structured_path_unparseable source=metadata_enumeration detail=unsafe_character
G5_DISTINFO_SPACE_RC=3
```

**Minimal fix.** Do not conflate rendering safety with evaluability. Count and classify the record, then render it suppressed: `wpi_fail B3 "writable_path_inside_immutable_tree path=[unrenderable] path_sha256=<h> count=<n>"`. Reserve `structured_path_unparseable` for a record that is not a path at all (non-absolute, embedded NUL).

---

### 4. Mount attestation is not established before the first probe, and no FAIL path closes its mount window — HIGH

**Location** `wpi_main:716-725` vs first `wpi_mount_guard_begin` at `:425`; `wpi_assert_tree:448`, `wpi_assert_metadata_dir`, `wpi_assert_regular_digest`, `wpi_assert_metadata_readable`

**Defect, part A — ordering.** Call-site order in the frozen bytes: `wpi_bind_tool` ×8 (`:718`), `wpi_assert_evidence_leaf_bound` (`:721`), `wpi_assert_manager_ready` (`:725`), and only then the first `wpi_mount_guard_begin` at `:425`. Every tool is bound, every tool is first executed, the evidence leaf is bound, and the system manager is queried, all before the mount topology has been compared to the deploy-channel attestation once. The binding rule requires the attested-topology comparison so "an overlay or bind mount cannot substitute a decoy object"; a bind mount over `/usr/bin` substitutes the entire instrument set and is detected only afterwards.

**Defect, part B — atomicity.** Every `wpi_fail` reached inside a mount window exits without `wpi_mount_guard_end`. The rule states parent, mount and leaf checks are "one atomic observation". A FAIL emitted without the closing comparison is not mount-bound — and FAIL is the outcome that goes to the Lead as a candidate-repair question.

**Falsification (executed).** Instrumented guards, row-14 FAIL path and row-10 metadata FAIL path:

```
MOUNT_WINDOW_OPEN
B3_path path=/fixture kind=directory mode=555 owner_numeric=0:0 binding=component_and_mount
B3_FAIL reason=writable_path_inside_immutable_tree path=/fixture/writable
G3_TREE_FAIL_PATH_RC=1

MOUNT_WINDOW_OPEN
B3_FAIL reason=path_metadata_mismatch path=/opt/mtc-bridge/releases mode=775 expected_mode=555
G3b_MODE_MISMATCH_RC=1
```

`MOUNT_WINDOW_CLOSED` never appears. Note the FAIL lines nonetheless carry `binding=component_and_mount` — the token claims a binding the branch did not complete (Pattern 9).

**Minimal fix.** Hoist one `wpi_mount_guard_begin` to immediately before the tool-binding loop. Route FAILs through a helper that runs `wpi_mount_guard_end` first and downgrades to `mount_topology_changed` STOP if the topology moved.

---

### 5. Self-QA has zero executed coverage of the path-object binding rule, the mount guard, tool binding, row 18 and the row-19 preflight — HIGH

**Location** `SELF_QA_RP7.md:80-140`

**Defect.** The fence is literally re-runnable — I confirmed that. Its coverage is the problem. Every B3, B1a and B1 fixture neutralises the code under audit:

```bash
wpi_mount_guard_begin(){ :; }; wpi_mount_guard_end(){ :; }; wpi_walk_components(){ :; }
wpi_sha_file(){ WPI_LINE=…; }
wpi_assert_regular_digest(){ :; }
```

Functions with **no executed arm anywhere in the QA**: `wpi_lstat`, `wpi_walk_components`, `wpi_bind_tool`, `wpi_validate_inputs` beyond its first missing-input STOP, `wpi_mount_guard_begin/end`, `wpi_sha_file`, `wpi_assert_evidence_leaf_bound`, `wpi_assert_metadata_dir`, `wpi_assert_interpreter`, `wpi_assert_metadata_readable`, `wpi_require_observed_path_grammar`.

That set is the entire Pattern-3 repair — the largest and highest-risk part of the design — plus rows 15, 18 and the row-19 preflight. Findings 1, 2 and 3 all live inside it, and all three were found by the first fixture that drove those functions for real. The coverage interpretation section claims "one deliberate deviant fixture each produces rc 1 for B3s, B1a, B1, B5 and B6", which is true of the reachable arms and silent about the unreached ones. A stub cannot fail. Pattern 10.

Secondary gap: strict JSON is tested for exactly two of six arms (good, duplicate key). Untested were `NaN`/`Infinity` — the Pattern-9 regression that cost the B3 cycle an audit round — plus wrong type, top-level non-object, and the `flag_mismatch` FAIL. I ran all four; the code is correct in every case, so this is a QA gap and not a code defect:

```
F4_JSON_RCS nan=3 wrong_type=3 flag_mismatch=1 top_level_array=3
```

**Minimal fix.** Add fixtures that drive the real `wpi_lstat`/`wpi_walk_components` against a constructed tree: absent leaf, symlinked intermediate, symlinked leaf, wrong numeric owner, wrong leaf mode, and one mount-guard RED/GREEN pair. Add the four JSON arms above.

---

### 6. The sweep budget is post-hoc detection, not enforcement; no probe but `curl` is time-bounded — HIGH

**Location** `wpi_run_find:413-415`

**Defect.** Elapsed time is computed after `wpi_capture` returns, so `sweep_budget_exceeded` can only be emitted once the sweep has already finished. A `find` that blocks indefinitely — a hung network filesystem, an unresponsive automount under the release tree — produces no STOP, no FAIL and no output, and the ssh stage hangs with the evidence leaf open. Row 12 preregisters a STOP for exactly this and the implementation cannot deliver it. Grepping the frozen bytes for a bounding mechanism returns one hit, `--connect-timeout 5 --max-time 10` on `curl` (`:657`); `find`, `ss`, `systemctl`, `sha256sum`, `stat`, `readlink` and both Python children are unbounded.

**Falsification (executed).** Budget 1 s against a 2 s sweep:

```
B3_STOP reason=sweep_budget_exceeded root=/fixture elapsed_ms=2070 budget_s=1
F6_BUDGET_1S_AGAINST_2S_SWEEP_RC=3
```

The STOP is correct and arrives 2.07 s in — i.e. only because the child returned. Note also `elapsed_ms=`, where row 12's grammar names `elapsed_s=<n>`.

**Minimal fix.** Bound the child. `timeout` is a ninth tool and must be pinned and bound like the other eight; the block's own mutant fixture already assumed `WPI_TIMEOUT=/usr/bin/timeout`, so the shape is known. Keep the post-hoc measurement as a second gate, and emit `elapsed_s` alongside `elapsed_ms`.

---

### 7. Two path-bearing inputs and the mount attestation are accepted shape-only; `WPI_INTERPRETER_TARGET` escapes the §10.1 allowlist — HIGH

**Location** `wpi_validate_inputs:340`, `:359`, `:362`

**Defect.** Fourteen inputs are literal-pinned with `wpi_expect_literal`. Three are not:

- `WPI_LOG_DIR` — absolute only. R2 is now resolved to `/var/log/mtc-bridge` in `LEAD_PIN_RESOLUTION_2026-08-10.md`, so it can be pinned and is not.
- `WPI_INTERPRETER_TARGET` — absolute only, and `wpi_assert_interpreter:491` runs a full component walk over whatever it names. §10.1 is exhaustive and has **no entry** covering a resolved interpreter outside the venv; a `bin/python` symlink resolving to `/usr/bin/python3.12` puts the block's `stat` calls on a path the allowlist does not admit.
- `WPI_ATTESTED_MOUNTINFO_SHA256` — 64-hex only. This single value is the sole basis of every mount binding in the block.

§10.2 requires the Stage-1 static proof to reject "unresolved/dynamic path construction" and to prove "every path-bearing argument is derived only from preregistered constants". Two path-bearing arguments in the frozen bytes are not. Row 16's claim that it "can never diverge at run time" therefore rests on a gate the block as written cannot pass.

**Minimal fix.** Pin `WPI_LOG_DIR` literally to `/var/log/mtc-bridge`. Either pin `WPI_INTERPRETER_TARGET` to a literal supplied by the deploy channel and add its allowlist row, or drop the symlink arm and require `bin/python` to be a regular file. Literal-pin the attested mountinfo digest in the block, not only in the wrapper.

---

### 8. Row-grammar deviations across rows 12, 13, 15, 18, 19, 21, 22 — MEDIUM

**Location** multiple

**Defect.** Section 8.2 calls its right-hand column the *exact* predicted first divergence. Observed deltas:

- Row 13 names two STOP tokens; `walk_permission_error` occurs **0 times** in the file. Every walk error collapses to `walk_incomplete`.
- Row 12: `elapsed_ms=` for `elapsed_s=`.
- Row 19: the block introduces `verifier_absent`, `verifier_digest_mismatch`, `verifier_object_unexpected` and `verifier_unreadable`, none preregistered, and routes enumeration errors to row-12/13 tokens (`sweep_budget_exceeded`, `walk_incomplete`) under the `B1` prefix. Digest-verifying the verifier is a genuine improvement over the draft and should be kept — but it needs a row.
- Rows 10/11/15/17: the row specifies one combined line, `path_metadata_mismatch path=<p> kind=<k> mode=<m> owner_numeric=<u:g> expected=directory,0555,0:0`. The block emits one of three partial forms with different spellings (`expected=directory`, `expected_owner_numeric=`, `expected_mode=`).
- Row 18 emits `observed=unpreregistered_version` for `observed=<v>`; row 21 emits `observed_sha256=<h>` for `observed=<v>`; row 22 emits `observed_count=<n>` for `observed=<rows>`. These three are deliberate content suppression and are defensible, but they are still deltas against a binding table.

**Minimal fix.** One reconciliation pass. Either implement the missing token with a non-prose mechanism or delete it from row 13 and say why (Pattern 5 forbids classifying `find`'s prose as EACCES); add the row-19 verifier-identity row; align field spellings; record the three suppressions in the table as the accepted rendering.

---

### 9. Row 22 filters at the tool instead of parsing the complete table; R5's full inventory is not captured — MEDIUM

**Location** `wpi_assert_listener_set:625`

**Defect.** The row preregisters "a complete `ss -H -ltn` result is structurally parsed into all socket rows". The block runs `ss -H -ltn 'sport = :8790'`. Two consequences: the filter grammar is delegated to the tool, so the block's structural claim covers only rows the tool chose to emit; and R5's explicit requirement — "the full listener inventory is captured as evidence rather than asserted against a count" — is unmet, since no unfiltered inventory is ever captured.

Row-23 wildcard detection is not defeated (`sport = :8790` matches any local address), so this is an evidence and contract gap rather than a false pass.

**Minimal fix.** Run the preregistered unfiltered `ss -H -ltn`, capture it whole as evidence, parse every row, and apply the port-8790 scope in the block where R5 puts it.

---

### 10. A wrong-typed preregistered flag is STOP, not FAIL — MEDIUM

**Location** `wpi_assert_status:694`

**Defect.** A body that is complete, valid, strict JSON with the correct top-level shape but reports `"arm_enabled": "false"` as a string instead of a boolean is a positively observed deviation in the exact predicate row 21 exists to test. The block maps it to `schema_unexpected … detail=type`, rc 3. Row 21 reserves `schema_unexpected` for "a preregistered key is absent under a different spelling" and says "only a complete structurally valid body may become `B5_FAIL reason=flag_mismatch`" — this body is complete and structurally valid.

**Falsification (executed).** `state_version` supplied as `"1"`:

```
B5_STOP reason=schema_unexpected field=state_version detail=type
```

The row's language is genuinely ambiguous here, which is why this is MEDIUM and not BLOCK — but the ambiguity has to be resolved in the design, not left to the code. A bridge that stringifies its ARM flag currently escapes as "could not evaluate".

**Minimal fix.** Split the row: absent key → `schema_unexpected` STOP; present key with wrong type → `flag_mismatch` FAIL with `observed_type=<t>`.

---

### 11. The mount binding hashes a different file object than it parses, over a volatile rendering — MEDIUM

**Location** `wpi_mount_guard_begin:298-301`

**Defect.** Two problems in three lines. First, `wpi_parse_mountinfo /proc/self/mountinfo` reads the file through the **shell's** `/proc/self`, while `wpi_sha_file … /proc/self/mountinfo` execs a child, whose `/proc/self` is the child's own. The parse and the digest are taken from two different kernel-generated files; the structural parse contributes nothing to the binding, since only the digest is compared. Second, comparing a whole-file SHA-256 of `mountinfo` against a deploy-channel attestation binds byte identity of a rendering that includes mount IDs, parent IDs, peer-group IDs and record order — not topology. Any unrelated mount change between attestation and run, including the `/run/user/<uid>` mount the ssh login itself can create, produces `mount_topology_mismatch` and stops the stage.

This fails closed, so it is not a false-pass route. It is a rigor defect plus a live false-STOP risk that will burn a RUNID.

**Minimal fix.** Hash and parse the same object: capture `/proc/self/mountinfo` once into a create-once evidence leaf, then parse and hash that leaf. Compare the attestation against a **normalised projection** of the parsed table (device id, root, mount point, fstype, source for each preregistered path's covering mount), not the raw digest.

---

### 12. Unsanitized host-derived symlink target reaches the evidence log — LOW

**Location** `wpi_assert_interpreter:490`

**Defect.** `wpi_sanitize` exists at `:52` and is called exactly once, at `:406`. The interpreter's resolved symlink target is printed raw in its STOP branch. `wpi_single_record` blocks LF injection (a second line becomes `multiple_records`), but CR and other control bytes pass.

**Falsification (executed).** Symlink target `/decoy\rB1_interpreter path=spoofed exec=ok`:

```
$ cat -A ev.log
B1_STOP reason=interpreter_object_unbound kind=symlink target=/decoy^MB1_interpreter path=spoofed exec=ok$

$ cat ev.log
B1_STOP reason=interpreter_object_unbound kind=symlink target=/decoyB1_interpreter path=spoofed exec=ok
```

Any CR-honouring renderer of the evidence log displays a forged `B1_interpreter` result line.

**Minimal fix.** `wpi_sanitize "$resolved"` and print `$WPI_SAFE`. Audit for other host-derived strings that reach `printf` without a grammar check.

---

### 13. Field splitting with pathname expansion active in two parsers — LOW

**Location** `wpi_parse_mountinfo:269`, `:277`; `wpi_map_get:106`

**Defect.** `set -- $pre`, `set -- $post` and `for entry in $map` split on IFS with globbing enabled; `set -f` is never issued. `mountinfo` escapes space, tab, newline and backslash as octal but does **not** escape `*`, `?` or `[`. A mount point or source containing a glob metacharacter is subject to pathname expansion against the shell's working directory, changing both field count and field values. Residual Pattern 5.

**Falsification (executed).** A record with mount point `/mnt/*` parsed and was admitted at rc 0 (no match existed in the cwd; a matching entry changes the parse):

```
RP7_mount_table parsed=yes records=1 content=not_printed
G6_MOUNTINFO_GLOB_RC=0
```

**Minimal fix.** `set -f` at the top of the block, or a local `set -f`/`set +f` pair around each split.

---

## Additional observations — not counted as findings

1. **`stat` and `env` are self-attesting.** `wpi_bind_tool stat` proves `/usr/bin/stat` is a root-owned non-writable regular file by executing `/usr/bin/stat`. The same holds for `env`. The printed `resolution=pinned_absolute` is therefore earned by the other six tools and asserted for the first two. No alternative exists under the accepted execution model — flagged so the limitation is explicit in the evidence rather than discovered later.
2. **Evidence-tree volume.** Each `wpi_lstat` costs one `env`+`stat` pair and three create-once leaves. `wpi_assert_metadata_readable` over 56 distributions runs roughly 800 captures — on the order of 2,400 evidence files and 1,600 child processes — which `remote_close_tree.sh` then hashes twice and op 10 downloads. Row 12's 120 s budget is per-sweep; there is no stage budget.
3. **Line 358, `WPI_SHA256SUM="$WPI_SHA256SUM"`,** is a no-op.
4. **`wpi_assert_interpreter` closes its mount window at `:498`, before executing the interpreter at `:499`;** `wpi_assert_lock_parity` runs the verifier with no window open at all. Defensible — a long-running child cannot sit inside a hashing window — but it means "bound object" and "executed object" are separated in time, which the `binding=` tokens do not disclose.
5. **`verify_lock.py` was independently verified at the candidate:** 3735 bytes, `d951e0ee…a451e5`, matching the block's hardcoded size and `WPI_VERIFY_LOCK_SHA256`. Its real output grammar matches the block's parser exactly — PASS on stdout as `verify_lock: PASS: lock+installed; packages=<n>`, failures on **stderr** at rc 1 as `verify_lock: FAIL: missing-or-wrong=<names>; unexpected=<names>`, with canonicalised names inside the block's accepted charset. The stream split and the structured/generic discrimination in `wpi_is_structured_parity_mismatch` are correct against the real artifact. This is the strongest part of the block.

---

## What I could not evaluate

- Nothing was executed against the staging host, and nothing in this audit required it.
- Finding 1's `argv[0]` prefix behaviour was confirmed on GNU coreutils 8.32 here, not on the target host's build. The reasoning is build-independent (gnulib `set_program_name` does not strip the directory, and the block matches both the `stat` and `statx` wordings), but the target-host transcript does not exist and I am not asserting one.
- `RP0-BOOTSTRAP.sh` was not read; the block's assumptions about `EV_DIR`/`EV_LOG` were taken from `run_ro.sh` and the prereg, not verified against bootstrap bytes.
- Rows 1–9 (P0, B2, B4) are out of this block's scope and were not audited.
