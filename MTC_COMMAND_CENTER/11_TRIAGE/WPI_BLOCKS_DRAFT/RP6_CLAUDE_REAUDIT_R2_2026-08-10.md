I have everything. Here is the full audit report.

---

# RE-AUDIT REPORT — `RP6-P0.sh` full-block repair, round 2, Claude flagship T0 slot (claude-opus-5, xhigh)

## VERDICT: REQUEST_CHANGES (3)

**All seven round-1 findings are CLOSED**, each with an executed falsification that I rebuilt independently and drove against the repaired bytes. F1 and F2 — the two HIGH findings — are closed on real GNU `lstat` and a real end-to-end drive respectively; the row-8 gate is genuinely load-bearing (removing either the comparison or the call makes the manager query reachable with a mismatched namespace, executed both ways).

Three items require changes, none of them a reproduced round-1 finding and none producing a false verdict: the F7 repair introduced a fabricated `rc=` field and lost the resolved path from a STOP arm; the repair's own D026 evidence no longer reproduces (four recorded transcripts, including the new full-block fence, are stale or un-runnable post-commit); and the new row-8 evidence line asserts a binding it does not disclose the limits of.

**Scope note.** Windows Git Bash, GNU bash 5.2.37, GNU coreutils 8.32. My RP6 targets were byte-stable throughout: `RP6-P0.sh` re-derives to `041c9da9…c048db` / 66381 B before and after this session and shows clean in `git status`. Two things moved under me and neither touched my basis: `HEAD` advanced `90d8d447 → 56760955` (a parallel-dispatch docs commit), and `WPI_PREREGISTRATION_DRAFT.md` acquired working-tree edits confined to the transport-set derivation contract (§3) — **§8.1 is untouched** (verified by diff filter and by re-grepping rows 1, 3 and 8). All fixtures were written to the session scratchpad; no repository file was modified by me, no host was contacted, no network command was run.

---

## Section 1 — Mechanical gates and re-derivation (V9)

| Item | Claimed | Observed | Verdict |
|---|---|---|---|
| SHA-256 | `041c9da9769e36638c9785b54afc638fa8e7b475a6d24238fc10388916c048db` | identical | **PASS** |
| Bytes | 66381 | 66381 | **PASS** |
| `bash -n` | PASS | rc 0 | **PASS** |
| Line endings / BOM / charset | `cr_bytes=0 lf_bytes=1248 bom=false` | 0 CR, 1248 LF, no BOM, 0 non-ASCII, 0 trailing-WS lines | **PASS** |
| Diff scope vs `90d8d447^` | 5 whitelisted files | exactly those 5; prereg delta is the single row-3 field reorder | **PASS** |
| Post-audit integrity | — | hash + bytes unchanged; all five RP6 targets clean | **PASS** |

**Harness re-runs on the new bytes.**

- C13 R4 arm harness (`SELF_QA_RP6.md:1159-1324`) → rc 0, `C13_R4_ARM_QA_SUMMARY cases=27 result=PASS`, 25 `CASE_OK` + 2 `PROBE_OK`, 0 `CASE_BAD`/`PROBE_BAD`. **Summary green.** Its recorded transcript no longer matches — see finding 2.
- C13 R3 backstop harness (`:942-1025`) → rc 0, `C13_R3_BACKSTOP_QA_SUMMARY inputs=2 mutations=2 cases=4 result=PASS`. **Summary green**, transcript stale — finding 2.
- C13 R3 arm harness (`:664-787`) → rc 0, `C13_R3_ARM_QA_SUMMARY cases=16 result=PASS`. Transcript stale — finding 2.
- New full-block D026 fence (`:1636-1956`) → **rc 1, aborts**; the recorded `result=PASS` summary is unreachable on the committed tree — finding 2.

---

## Section 2 — V-rows: closure of the seven round-1 findings

| V | Round-1 finding | Verdict | Executed evidence on the repaired bytes |
|---|---|---|---|
| **V1** | F1 HIGH — absolute `argv[0]` made every filesystem-object FAIL arm dead code | **CLOSED** | `p0_classify_stat_shape` is now parameterised by `$P0_STAT`. Real GNU `stat`, real absent objects, full block: `BLOCK_RC=1 P0_FAIL reason=venv_root_absent … detail=preregistered_path_observed_missing` and `BLOCK_RC=1 P0_FAIL reason=interpreter_absent …`. Both were rc 3 `path_probe_unclassified` in round 1. The EACCES arm I showed unreachable is live: `rc=3 P0_STOP reason=path_probe_denied path=/fixture/venv …`. |
| **V2** | F2 HIGH — §8.1 row 8 absent, row 9 ungated | **CLOSED** | Row 8 implemented and **executed as a gate**, not merely present. See the row-8 table below. |
| **V3** | F3 MED — non-canonical prereg *input* accused the host at rc 1 | **CLOSED** | `RP6-P0.sh:359-361`. Same healthy object, only the spelling differs: `BLOCK_RC=3 P0_STOP reason=input_not_canonical_spelling name=P0_VENV_ROOT value=[…/e2e//venvs/2ce41e34…321b] detail=repeated_separator`, raised before any filesystem probe. The canonical spelling still drives to `P0 PASS` rc 0. No other non-canonical spelling reaches rc 1: trailing `//` and trailing `/` are caught by the candidate-bound check. |
| **V4** | F4 MED — duplicate pins silently first-wins | **CLOSED** | Both orders of the same contradictory table now STOP identically: `P0_TOOL_PINS="stat=/usr/bin/stat stat=/decoy/stat"` → `rc=3 prereg_input_malformed name=P0_TOOL_PINS duplicate=stat`; decoy-first → same line. Round 1 showed rc 0 `P0 PASS` vs rc 3 depending on order. Secondary defect closed too: `pinned=` is now a distinct-tool count — 0 / 1 / 2 pins → `P0_tool_inventory count=12 pinned=0|1|2`. |
| **V5** | F5 MED — all readlink producers diagnostic-free, three STOP arms emitted empty `detail=` | **CLOSED** | `-v` at all four sites (`:621, 937, 965, 1147` — the fourth is new). Real GNU `readlink`, real ENOENT. Pre-repair: `evidence_binding_unprobeable … detail=` / `namespace_unreadable … detail=` / `venv_root_canonicalization_failed … detail=` (all empty). Repaired: all four carry `detail=[/usr/bin/readlink: <path>: No such file or directory] diagnostic_shape=single_printable_record`. |
| **V6** | F6 LOW/MED — NUL-only rc-2 admitted as valid no-match | **CLOSED** | `mapfile -d ''` + out-of-band NUL-delimited rc record. NUL-only rc 2: pre-repair `OUTCOME=nomatch DIAG=[empty_capture_at_rc2]` (plus bash's unadjudicated NUL warning); repaired `OUTCOME=error DIAG=[nul_byte_in_merged_capture]`. Bonus: an rc-0 record containing an embedded NUL was silently accepted `found` pre-repair with a truncated name — now `error`. Bash's NUL warning to unadjudicated stderr is gone. **11-case regression battery** (valid record / rc2 empty / rc2 newline-only / rc2 text / rc0 duplicate / rc0 five-field / rc0 empty / rc5 error / rc2 NUL-then-trailer …) run against both sources: **every non-NUL case byte-identical PRE vs POST**. No behaviour drift. |
| **V7** | F7 LOW/MED — two missing tokens, three `identity_unexpected` grammars | **CLOSED** (with finding 1 attached) | `tool_not_evaluable`: pre `tool_not_executable tool=getent path=… mechanism=access_builtin_x` → post `tool_not_evaluable tool=getent rc=126 detail=access_builtin_x_denied`. `group_query_not_evaluable`: all four `id -G` failure modes flipped — rc 7 → `group_query_not_evaluable rc=7 detail=[group backend unavailable]`; empty → `rc=0 detail=[response_empty]`; multiline → `rc=0 detail=[response_multiline:…]`. `identity_unexpected` now has **one** grammar, driven end to end: gatea → `observed_numeric=4096:4096 expected_numeric=4242:4096 account=gatea`; mtc-bridge → `observed_numeric=999:989 expected_numeric=999:988 account=mtc-bridge`. The second grammar (`identity_unexpected uid=… expected=…`) is deleted from `p0_record_identity`, and I verified the deletion is verdict-preserving: `live==record ∧ record==P0_EXPECT_UID ⟹ live==P0_EXPECT_UID`, with every getent non-`found` outcome still STOP. §8.1 row 3 amended to the same order (one-line diff). |

### Row-8 gate — kickoff sub-checks

| Sub-check | Verdict | Evidence |
|---|---|---|
| Gate exists | **YES** | `p0_assert_execution_domain` (`:959-988`), called at `:991`. |
| Uses `<PIN-AT-FREEZE>` constants | **YES** | Five literals `:224-228`, all still unfilled; `P0_FIXED_ATTESTED_NET_NS='<PIN-AT-FREEZE>'` restored in a copy → `rc 3 execution_domain_unattested field=network_namespace detail=freeze_pin_unfilled`. Draft bytes cannot GREEN end-to-end. |
| rc-3 pre-check + `:?` pattern | **YES** | `:412-426`. Missing prelude input → `rc 3 execution_domain_unattested field=pid_namespace detail=preregistered_value_missing`. Pre-check deleted, `:?` kept → rc 1, `P0_ATTESTED_USER_NS: deploy-attested user namespace identity is required`. **Mutant killed:** pre-check *and* `:?` both deleted → `line 438: P0_ATTESTED_USER_NS: unbound variable`, named message absent. |
| Emits the two named STOP tokens | **YES** | `execution_domain_unattested` (13 arms) and `execution_domain_mismatch` (2 arms). Driven: `execution_domain_mismatch field=network_namespace observed=net:[4026999999] attested=net:[4026531992]`; `execution_domain_mismatch field=root_mount_identity observed=606877205:37154696925843707 attested=1:2`; `execution_domain_unattested field=user_namespace rc=1 detail=[… Permission denied] diagnostic_shape=single_printable_record`. |
| **Actually gates row 9** | **YES — proved by execution, not by reading** | My fixture's `systemctl` shim appends to a marker file. **All six row-8 divergence cases: `BLOCK_RC=3 MANAGER_RAN=no`.** Two mutation kills: deleting the namespace comparison → `BLOCK_RC=0 MANAGER_RAN=yes P0 PASS` with a mismatched net ns; deleting the top-level `p0_assert_execution_domain` call → `BLOCK_RC=0 MANAGER_RAN=yes`. Both load-bearing. |
| Accepting arm recorded as a freeze-gate item | **YES**, not a finding | `STATUS_RP6_P0.md:46-60` ("Freeze gate — mandatory, same class as RP7", five literals enumerated, deploy-channel minting procedure, "No value may be learned or re-pinned from the login session being tested") and `RP6_FULLBLOCK_REPAIR_REPORT.md:70-84`. |

**Full GREEN drive.** With the five attestation literals and the four `P0_NS_*_PATH` repointed **in a scratchpad copy only**, the whole block runs to `P0 PASS` rc 0 through prerequisites, inputs, 12-tool inventory, evidence binding (real dev:inode on a real create-once leaf), identity, accounts, execution domain (`binding=deploy_attested_exact`), manager, venv root, interpreter, out-of-scope and terminal claim.

---

## Section 3 — V8 Regression

| Check | Verdict | Evidence |
|---|---|---|
| Diff confined to the seven findings' scope | **PASS** | 37 hunks, each mapping to F1–F7: header wording, `p0_prepare_readlink_detail`, attestation constants, `//` input check, pin-duplicate check, row-8 input block, `tool_not_evaluable`, `readlink -v` at four sites, group tokens, uid-compare removal, `mapfile` capture, account grammar, namespace→execution-domain replacement, classifier, terminal claim. Nothing outside. |
| Nothing that passed round 1 broke | **PASS with one regression** | V4/V5/V10/V11 (Pattern 8 numeric-only, capability ledger, fd-8 evidence binding, read-only scope) all re-verified. `exec 8>&-` still precedes every STOP path (GLM F6 stays closed). Capability ledger still whole-word: forbidden `0 4096` → `capability_wider_than_ledger gid=4096`; `0 988` → admitted. C13 arm behaviour unchanged on all 11 non-NUL cases. **Regression:** the tool-not-executable STOP lost its `path=` field — finding 1. |
| Verdict-preserving deletions | **PASS** | The removed `identity_unexpected uid=…` check and the removed record-only namespace section are both subsumed; no path admits state the old code refused. |
| Evidence-package integrity | **FAIL** | Finding 2. |

---

## Findings — most severe first

### Finding 1 — MEDIUM. The F7 repair put a fabricated invocation status into an evidence line and deleted the resolved path from it (Pattern 9)

`RP6-P0.sh:531-532`:

```bash
[ -x "$resolved" ] \
    || p0_stop "tool_not_evaluable tool=$t rc=126 detail=access_builtin_x_denied"
```

Two defects in one line.

**`rc=126` is not an observation.** No invocation happened. The block resolves and admits tools by shell builtins only — this is its stated discipline (`:496-499`: "Resolution and executability are decided by shell builtins only — `command -v` and the access(2) predicate `[ -x ]` — so no external tool has to be trusted"). §8.1 row 1 specifies `tool_not_evaluable tool=<t> rc=<n> detail=<d>` as the divergence *for invocation failure*; the repair satisfied the grammar by attaching the token to the access(2) arm and inventing the conventional shell status for "found but not executable". A reader of the evidence leaf sees `rc=126` and concludes an exec was attempted and returned 126. Nothing was executed.

**The resolved path is gone from the leaf entirely.** Pre-repair the arm emitted `tool_not_executable tool=$t path=$resolved mechanism=access_builtin_x`. The `P0_tool name=… path=…` inventory lines are printed by a *second* loop (`:595-604`) that runs only after every tool has resolved, so on this STOP no `P0_tool` line exists at all and the operator cannot tell which object was rejected.

**Executed, both sources, same non-executable fixture:**

```
PRE   rc=3  P0_STOP reason=tool_not_executable tool=getent path=<W>/b3/nonexec mechanism=access_builtin_x
POST  rc=3  P0_STOP reason=tool_not_evaluable  tool=getent rc=126 detail=access_builtin_x_denied
```

**Minimal fix.** `tool_not_evaluable tool=$t path=$resolved rc=na detail=access_builtin_x_denied mechanism=access_builtin_x` — keep the required token, restore the path, and stop asserting a status no probe produced. If §8.1 row 1's `rc=<n>` must be numeric, amend the row: P0 deliberately never invokes an inventory tool, so no arm in this block can honestly carry an invocation status.

---

### Finding 2 — MEDIUM. The repair's own D026 evidence no longer reproduces: four recorded transcripts are stale or unreachable (Pattern 10)

The repair report offers `RP6_FULLBLOCK_D026_SUMMARY … result=PASS`, `NORMALIZED_TRANSCRIPT_MATCH=True`, and three regression harness summaries as its closure evidence. The summaries are reproducible. **The transcripts are not**, and the new fence cannot be run at all on the committed tree.

**(a) The new full-block fence can only ever run once.** `SELF_QA_RP6.md:1642` takes the pre-repair RED side from a moving reference:

```bash
git show "HEAD:$target" > "$Q/pre.sh"
```

After commit `90d8d447`, `HEAD:$target` **is** the repaired block. Every "PRE" arm now executes repaired bytes. Executed:

```
=== F1 PRE root real-lstat ===
P0_FAIL reason=venv_root_absent path=/tmp/tmp.NcS3uHknpY/real-lstat-missing-root …   RC=1
```

— identical to its own POST arm, where the recorded transcript (`:1963-1964`) shows `path_probe_unclassified`. The fence then dies at `[ "$f3p" -eq 0 ]` (F3 PRE now STOPs rc 3): **process rc 1, 52 lines of 143, `result=PASS` never printed.** Line 1951 compounds it: `git show "HEAD:$draft" | grep 'identity_unexpected account=mtc-bridge observed_numeric'` returns nothing post-commit, which under `set -e` is itself fatal. The same document already knows the correct idiom — lines 697 and 1196-1197 pin `$pre_rev`/`$r3_rev` to immutable revisions.

**(b–d) Three recorded transcripts contradict their own harnesses on the repaired bytes.** The repair edited the harness assertion substrings (R3 fence at `:754-761`, R4 fence at `:1274-1281`) and changed block behaviour, but regenerated no transcript:

| Section | Harness | Recorded output | Re-run result |
|---|---|---|---|
| C13 R3 arm | `:664-787` | `:797-912` | rc 0, `cases=16 PASS`, **5 lines differ** |
| C13 R3 `:?` backstop | `:942-1025` | `:1033-1074` | rc 0, `cases=4 PASS`, **4 hunks differ** |
| C13 R4 arm — the section the document names as *current* evidence (`:1609-1613`) | `:1159-1324` | `:1335-1535` | rc 0, `cases=27 PASS`, **5 lines differ** |

In round 1 I recorded these as byte-identical and cited exactly that as proof they were "genuine D026 evidence … reproducible without an edit". That property is gone. The backstop case is the most substantive: the `precheck_and_backstop` double-mutant used to be killed by `set -u` reaching the `P0_input` printf (`unbound variable`, rc 1); on the repaired bytes it now dies earlier at the new execution-domain input pre-check (rc 3, `preregistered_value_missing`) because that harness's prelude supplies no `P0_ATTESTED_*`. The kill still holds — the named `:?` message is still absent — but the recorded mechanism is no longer the observed one. (My own fixture, which does supply the attestation prelude, still reaches the real `unbound variable` path and kills the mutant on the intended mechanism.)

**Minimal fix.** Pin the full-block fence's RED side to `90d8d447^` (or the literal `bff3c86e…` blob) instead of `HEAD`, and to a fixed prereg revision for the row-3 comparison; then re-execute and replace all four recorded transcripts. Until then, no second auditor can re-derive the repair's stated evidence.

---

### Finding 3 — LOW/MEDIUM. Row 8 prints `binding=deploy_attested_exact` without disclosing that `/proc` is never established to be procfs (Pattern 2 / Pattern 9)

The new gate reads all four identities through `readlink` on `/proc/self/ns/{user,mnt,pid,net}` and the root object through `stat -L -c '%d:%i' /`. It never establishes that `/proc` is a procfs mount. Prereg row 8's stated purpose is precisely to refuse "an apparently successful query from a container, chroot, private namespace or visible-PID-1 lookalike".

A private mount namespace that bind-mounts the real host `/` at `/` (identical `st_dev:st_ino`, so the root check passes) and over-mounts `/proc` with a directory carrying four crafted symlinks satisfies all five comparisons, and the block prints `binding=deploy_attested_exact`. That is the "private namespace" case the row exists to catch. The threat needs mount authority inside the login's namespace, which is why this is not HIGH.

The block is otherwise scrupulous about this class: the manager line carries `manager_identity=not_established`, the inventory line carries `provenance=not_established`, and `does_not_establish` names `tool_provenance_or_distribution_identity`. The row-8 line carries no such qualifier, and the procfs assumption appears nowhere in the claim block.

The fix is cheap and needs no new tool: `stat` is already pinned, so comparing `stat -L -c '%d' /proc/self/ns/user` against `stat -L -c '%d' /` (a crafted symlink lives on the root filesystem; a real namespace link lives on the anonymous `nsfs` device) distinguishes the two. Failing that, add `procfs_identity=not_established` to the `P0_execution_domain` line and the residual to `does_not_establish`.

---

## Nits (not counted in the verdict)

1. **The `(os error 2)` classifier alternative is almost certainly dead, and its provenance claim is false.** `RP6-P0.sh:1076` accepts `"$P0_STAT: cannot stat '$p': No such file or directory (os error 2)"`. `(os error N)` is a Rust `std::io::Error` rendering (uutils coreutils); uutils derives its message prefix from the *basename* of `argv[0]`, so no producer emits both an absolute prefix and that suffix. Executed all four combinations: `stat`-spelling + absolute prefix → matches (rc 1 `venv_root_absent`); `statx` + absolute → unclassified; basename + `(os error 2)` (the real uutils shape) → `path_probe_unclassified`. GNU coreutils 8.32 here emits no such suffix, and no observation of it exists anywhere in the package. `RP6_FULLBLOCK_REPAIR_REPORT.md:29` calls it "GNU's observed `os error 2` suffix" and `STATUS_RP6_P0.md:24` "the observed `(os error 2)` ENOENT form". The alternative was inherited verbatim from `RP7-WPI-RO.sh:250`; correct the attribution rather than the code.
2. **Residual, stated:** on a uutils-coreutils host the basename prefix makes every stat failure `path_probe_unclassified` again — i.e. the F1 *class* returns, fail-closed at rc 3. Worth one header sentence naming the producer assumption. (F1 is closed as found: it was a GNU-absolute-`argv[0]` defect and is fixed for GNU, verified on real bytes.)
3. **New bash floor, unstated.** `mapfile -d ''` and `local -a` require bash ≥ 4.4. The block declares no minimum; on an older bash `mapfile: -d: invalid option` lands on `p0_on_err` → `unadjudicated_command_status`, the backstop the header calls "unreachable".
4. **`P0_RESOLUTION` now carries two unrelated meanings** — tool resolution mode (`:527/529`) and readlink diagnostic shape (`:163-176`). I traced every call site: no live collision, because no readlink runs between `p0_resolve_tool`'s set and use. Hygiene only.
5. **Frozen `root_mount_identity` embeds an `st_dev`.** On btrfs/overlay/zfs roots that is an anonymous device allocated at mount time, so a correctly frozen literal invalidates on reboot. Fail-closed (rc 3 `execution_domain_mismatch`), but undisclosed. Namespace inode numbers are stable only for the kernel's *initial* namespaces.
6. **Evidence reduction on the domain STOP path.** The deleted record-only section printed all three namespace identities unconditionally; the gate records only the first diverging field. Fail-fast is right, but the surviving three observations are lost.
7. **`P0_identity_admitted` / `P0_account_admitted` are emitted before the domain gate runs.** A leaf reader who greps for them without also requiring `P0 PASS` reads pre-attestation admissions. The rc contract is unaffected.
8. **`readlink -v -f -- /` compared against `/`** (`:965-971`) is a tautology; the root canonicalization step adds nothing the `stat` identity does not.
9. **Carried unchanged from round 1, still open:** `kind=regular file` breaks key=value on the 12 tool lines; `detail=preregistered_path_observed_missing_parent_search_succeeded` overstates what an ENOENT establishes (`$P0_VENV_ROOT/bin` is never probed); `evidence_stdout_bound_to_create_once_leaf` (GLM F5) proves same-object-now, not create-onceness.

---

## What I checked and did not find defective

- **The F7 deletion of the identity-section uid comparison is verdict-preserving.** Traced every getent outcome: `found` re-derives the check in two steps in the accounts arm; `nomatch`/`error` both STOP. No path admits a wrong uid.
- **The row-8 grammar validators are tight.** `p0_read_domain_ns` requires the label-specific shape (`user:[…]` for `/proc/self/ns/user`), so a swapped or renamed link cannot pass; the `inner` extraction is digits-only; the root identity requires exactly one colon and digits; the prelude value must equal the frozen literal *and* the live value must equal the prelude.
- **The `mapfile` capture is sound.** The rc travels out-of-band in a NUL-delimited trailer, exactly two fields are required, and any producer NUL creates a third. `getent` sits on the left of `||` inside the process substitution so an inherited `set -e` cannot kill it early. The pre-normalization `had_bytes` decision and the trailing-newline re-normalization preserve the audited downstream value — confirmed on all 11 regression cases plus the 27-case R4 harness.
- **Read-only scope holds.** No redirection, `mktemp`, `rm`, `mv`, `cp`, `chmod`, `touch` or `tee` anywhere in the block; only the disclosed `exec 8>&1` / `8>&-`, closed on every exit path.
- **Pattern 4** on the two cleared launches is intact and was proved by accident again: my `systemctl` shim could not read an exported marker path through `env -i`.
- **Pattern 8** still clean: no `%U`/`%G`, `id` asked only `-u`/`-g`/`-G`, every input numeric and digit-validated, forbidden-gid matching whole-word on a space-padded list.

---

## Counts

- End-to-end drives against the real repaired bytes: **1 full GREEN `P0 PASS` rc 0** plus **21 falsification cases** (6 row-8 divergences, 4 row-8 mutation kills, 2 real-`lstat` FAIL arms, 1 input-canonicality, 4 pin-table, 4 account/ledger), each recording `BLOCK_RC` and whether the manager query executed.
- Unit-level cases on functions extracted by exact whole-function match from both sources: **51** (9 classifier prefix/suffix cases, 7 readlink producers, 22 getent capture cases across both sources, 8 group-query cases, 5 tool/inventory cases).
- Recorded harnesses re-run: **47 cases** (27 + 4 + 16), all summaries green; **1** attempted re-run of the new full-block fence (rc 1, aborted).
- Fixture disclosure: `getent`, `systemctl`, `ss`, `curl` and the `/proc/self/ns/*` half of `readlink` are shimmed; `stat`, `readlink` (all other paths), `id`, `env`, `find`, `grep`, `sha256sum`, `awk` are the real GNU tools; the venv tree, the interpreter and the evidence leaf are real objects. Nine constants — four `P0_NS_*_PATH` and the five `<PIN-AT-FREEZE>` literals — were repointed **in a scratchpad copy**; the repository file was never written.
- Arms not driven: real-host EACCES/ENOENT against the target Linux filesystem, and the `p0_on_err` ERR-trap backstop (still no fixture in the package). WP-I holds no host-contact authority.

**Standing unchanged:** `RP6-P0.sh` is a DRAFT — not frozen, not accepted, not dispatchable, and by construction unable to GREEN end-to-end until the deploy channel mints and embeds the five attestation literals. This report grants no host-contact, transport, deployment, budget or trading authority, and made no repository write and no commit.
