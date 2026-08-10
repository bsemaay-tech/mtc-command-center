All verification complete. Here is the full report.

---

# RE-AUDIT REPORT — `RP6-P0.sh` round 3 (final T0 round), Claude flagship T0 slot (`claude-opus-5`, xhigh)

## VERDICT: PASS-WITH-NITS

**All three round-2 residuals and both nits are CLOSED**, each verified by execution against the committed bytes `2d9b166e…` / 71743 B at `bbb40ab6`, and — for F1 and F3 — by fixtures I built myself rather than the repair's own.

- **F1** — the fabricated `rc=126` is gone, the resolved path is restored, and §8.1 row 1 was amended to a grammar the block can satisfy honestly. The only two surviving `126` literals in the block sit inside `case "$rc" in 126)` arms of probes that really do invoke something.
- **F2** — the fence's RED side is pinned to the immutable `0bbc3591`; I re-ran the fence twice and all four other recorded outputs. **Five for five reproduce**: four `cmp`-identical, the fence identical after normalizing only its `mktemp` root.
- **F3** — row 8 now discriminates a crafted `/proc` by namespace-link device vs root device, and it is load-bearing by execution. I drove a crafted fixture built from **real regular files on the real root filesystem, adjudicated by real GNU `stat` 8.32**: refused at rc 3. The comparison-only mutant admits the identical fixture at rc 0 and prints the false sentence. The residual is disclosed in the evidence line *and* the terminal claim.
- **Nits 1–2** — the `(os error 2)` alternative was dropped (not just re-attributed), its provenance corrected in both documents, and the GNU-producer assumption is stated in the block header.

**Scope note.** Windows Git Bash, GNU bash 5.2.37, GNU coreutils 8.32. My RP6 targets were byte-stable throughout: `RP6-P0.sh` re-derives to `2d9b166e…` / 71743 B before and after this session, and all five RP6 targets plus the prereg draft show clean in `git status`. `RP7-WPI-RO.sh` is dirty under a concurrent session — not read for edit, not touched, not part of this basis. All fixtures were written under `/tmp` and the session scratchpad; no repository file was modified, no host contacted, no network command run, no commit made.

---

## Section 1 — Mechanical gates and re-derivation

| Item | Claimed | Observed | Verdict |
|---|---|---|---|
| SHA-256 | `2d9b166eacfc39ebe0d8d89edb5860876ccc4d9f0ff97f9e10a228dbcf96289e` | identical | **PASS** |
| Bytes | 71743 | 71743 | **PASS** |
| `bash -n` | PASS | rc 0 | **PASS** |
| Byte form | `cr=0 lf=1328 bom=false non_ascii=0 trailing_ws=0` | 0 CR, 1328 LF, no BOM (`# =` at offset 0), 0 non-ASCII lines, 0 trailing-WS lines | **PASS** |
| Post-audit integrity | — | hash + bytes unchanged; all RP6 targets clean | **PASS** |

---

## Section 2 — V-rows: the three residuals and two nits

| V | R2 finding | Verdict | Executed evidence on the committed bytes |
|---|---|---|---|
| **V1** | **F1 MED** — fabricated `rc=126`, resolved path deleted from the STOP | **CLOSED** | `RP6-P0.sh:548-549`. My own harness, same non-executable fixture on both revisions: `PRE rc=3 tool_not_executable tool=getent path=<W>/nonexec mechanism=access_builtin_x` → `POST rc=3 tool_not_evaluable tool=getent path=<W>/nonexec rc=na detail=access_builtin_x_denied mechanism=access_builtin_x`. Field set and **order** match amended §8.1 row 1 exactly (`tool_not_evaluable,tool,path,rc,detail,mechanism` both sides). An executable fixture is still admitted (`ADMITTED resolved=[ getent=…] mode=[ getent=path_resolved_absolute]`, rc 0) — no regression on the accepting arm. Block-wide: `tool_not_evaluable` has exactly 1 arm; the two remaining `126` literals (`:1096`, `:1273`) are `case "$rc" in 126)` branches of the `systemctl` and interpreter probes, which genuinely execute. `path=$resolved` is safe in the key=value grammar because `:528-532` already refuses any resolved path containing whitespace or non-printables. |
| **V2** | **F2 MED** — four D026 transcripts stale or un-runnable | **CLOSED** | Every RED side is pinned to an immutable commit: fence `pre_rev=0bbc3591`, R3 arm `pre_rev=cbaf3ec8`, R4 arm `pre_rev=cbaf3ec8` + `r3_rev=8d2f25a5`; **no `HEAD:` reference survives in any harness**. All four resolve to real commits. See the reproduction table below. |
| **V3** | **F3 LOW/MED** — `binding=deploy_attested_exact` printed without disclosing the procfs assumption | **CLOSED** | Both halves of the remedy applied. See the F3 table below. |
| **V4** | **Nit 1** — `(os error 2)` dead alternative with false GNU provenance | **CLOSED** | The alternative is deleted from `p0_classify_stat_shape` (`:1149-1153`); `os error` now appears exactly once in the block, in the comment recording why it is gone and that it came from `RP7-WPI-RO.sh`. `RP6_FULLBLOCK_REPAIR_REPORT.md:40` and `STATUS_RP6_P0.md:51,61-66` both name uutils/Rust `std::io::Error` and the basename-prefix reason. Deletion is behaviour-preserving on GNU: the F1 ENOENT arms still flip to `venv_root_absent` / `interpreter_absent` at rc 1 on real absent objects. |
| **V5** | **Nit 2** — producer assumption unstated | **CLOSED** | `RP6-P0.sh:59-66`, `STATED PRODUCER ASSUMPTION`. Names the C-locale GNU shape, the absolute-`argv[0]` dependency, the uutils basename divergence, and the fail-closed consequence (`path_probe_unclassified` at rc 3, re-pin before preregistering such a host). Accurate as written. |

### F2 — transcript reproduction, executed by me from the line ranges the document itself cites

| Section | Extraction | Process rc | Summary | Transcript |
|---|---|---|---|---|
| Full-block D026 fence | `sed -n '1678,2068p'` | **0** (twice) | `RP6_FULLBLOCK_D026_SUMMARY findings=7 round3_residuals=3 real_lstat_arms=2 execution_domain_cases=9 readlink_stop_arms=3 result=PASS` | 156/156 lines, **`NORMALIZED_TRANSCRIPT_MATCH=True`** — the only delta is the random `mktemp` root; the two runs are byte-identical to each other |
| C13 R3 arm | `sed -n '664,787p'` | 0 | `C13_R3_ARM_QA_SUMMARY cases=16 result=PASS` (16 `CASE_OK`, 0 `CASE_BAD`) | **`cmp` clean**, 116 lines |
| C13 R3 `:?` backstop | `sed -n '952,1035p'` | 0 | `C13_R3_BACKSTOP_QA_SUMMARY inputs=2 mutations=2 cases=4 result=PASS` | **`cmp` clean**, 37 lines |
| C13 R4 arm | `sed -n '1181,1346p'` | 0 | `C13_R4_ARM_QA_SUMMARY cases=27 result=PASS` (25 `CASE_OK` + 2 `PROBE_OK`, 0 bad) | **`cmp` clean**, 201 lines |
| F2 freeze-literal gate | `sed -n '2286,2319p'` | 0 | `F2_FREEZE_GATE_QA_SUMMARY placeholder_rc=3 filled_fixture_rc=0 result=PASS` | **`cmp` clean**, 7 lines |

The fence prints its own RED identity — `RED_SOURCE rev=0bbc3591 sha256=bff3c86e…bac85b7cf bytes=57441` — so the pin is verifiable from the transcript without trusting the variable. 39 `ASSERT_MET`, 0 `ASSERT_UNMET`, 34 labelled arms. In round 2 this fence died at line 52 of 143 and never printed a summary; it now runs to completion and is re-runnable at any future HEAD.

The backstop's changed kill mechanism is stated honestly at `SELF_QA_RP6.md:1092-1108`, and my re-run confirms the description: `precheck_only` → rc 1 with the named message at line 330; `precheck_and_backstop` → rc 3 `execution_domain_unattested field=user_namespace detail=preregistered_value_missing`, assertion unmet on both message and rc, mutant killed. The decision not to fabricate freeze literals to restore the older `unbound variable` mechanism is correct under D026.

### F3 — row-8 procfs discrimination, driven on **real GNU `stat` against real objects**

Git Bash has no `/proc/self/ns` and refuses native symlinks, so my `readlink` shim supplies the link *text* only. Everything the discrimination turns on — the device — came from real `/usr/bin/stat` 8.32 against real filesystem objects. Root: `606877205:37154696925843707`.

| Case | Fixture | Result | Verdict |
|---|---|---|---|
| Honest | four distinct real objects on `/proc` (device `255`, a genuine non-root superblock) | rc **0**, `binding=deploy_attested_exact … procfs_identity=not_established ns_link_devices=255,255,255,255 root_device=606877205 ns_link_devices_distinct_from_root=yes` | admitted, and the disclosure is on the line |
| **Crafted** | four **real regular files allocated on the real root filesystem** — what a bind-mounted fabricated `/proc` exposes; real `stat -L -c '%d'` returns `606877205` | rc **3**, `execution_domain_unattested field=user_namespace detail=namespace_link_on_root_filesystem device=606877205 root_device=606877205` | **refused** |
| **Comparison-only mutant** | identical crafted fixture; only the `[ "$P0_DEVICE" != "$root_dev" ]` comparison deleted (`MUTANT_COMPARISONS_REMAINING=0`, `MUTANT_DEVICE_READS_REMAINING=1`) | rc **0**, admits, and prints `ns_link_devices=606877205,606877205,606877205,606877205 root_device=606877205 ns_link_devices_distinct_from_root=yes` | **load-bearing by execution** — the mutant emits exactly the false sentence the comparison prevents |
| Absent object | grammatically perfect link text, target does not exist | rc **3**, `subject=namespace_link_device rc=1 detail=[/usr/bin/stat: cannot stat '…': No such file or directory]` | fail-closed |

Ordering verified from the file, not from a stub: `p0_assert_execution_domain` at `:1066`, `p0_assert_system_manager_ready` at `:1123`, `P0_STAT` resolved at `:599`. The four `p0_assert_ns_link_off_root` calls sit at `:1051-1054`, after the equality comparisons (so a genuine divergence still reports as `execution_domain_mismatch`) and before both the evidence line and row 9. The four `P0_NS_*_PATH` values are hardcoded literals at `:227-230`, not caller-injectable. `p0_sanitize` collapses CR/LF and truncates at 400, so the new STOP arm cannot break the leaf grammar.

---

## Section 3 — Regression

| Check | Verdict | Evidence |
|---|---|---|
| `RP6-P0.sh` unchanged between my R2 basis and `bbb40ab6^` | **PASS** | `git diff 90d8d447 bbb40ab6^ -- RP6-P0.sh` empty — the parent *is* the `041c9da9…` bytes I audited in round 2 |
| Block diff confined to the 3 residuals + 2 nits | **PASS** | 8 hunks, each mapping 1:1: producer-assumption header (nit 2), `P0_DEVICE` global (F3), `p0_resolve_tool` STOP + comment (F1), execution-domain comment (F3), `p0_read_object_device` + `p0_assert_ns_link_off_root` (F3), evidence-line + four calls (F3), `(os error 2)` deletion + comment (nit 1), `does_not_establish` addition (F3). Nothing outside |
| Prereg §8.1 confined to row 1 | **PASS** | Section extracted and diffed in isolation: 28 lines both sides, **exactly 2 changed lines = row 1 only**. Rows 2–9 byte-identical |
| No round-1/2 closure reopened | **PASS** | All 7 round-1 findings re-driven through the fence on the current bytes: 39/39 assertions met, 0 unmet. Plus 16 + 4 + 27 recorded harness cases green |
| Read-only scope holds | **PASS** | No `mktemp`, `rm`, `mv`, `cp`, `mkdir`, `chmod`, `chown`, `touch`, `tee`, `ln`, `dd`, `truncate` anywhere in the block. Only redirections: `>/dev/null 2>&1` on two `command -v` probes, `2>&1` captures, and `exec 8>&1`/`8>&-` |
| fd-8 discipline intact | **PASS** | fd 8 is opened and closed entirely inside `p0_assert_evidence_leaf_bound` (`:637-653`, top-level call at `:676`), which completes long before the new execution-domain code — the four new STOP arms cannot leak it |
| Draft standing preserved | **PASS** | 12 `<PIN-AT-FREEZE>` occurrences; the freeze gate still refuses at rc 3 `freeze_pin_unfilled`. The block still cannot GREEN end-to-end |
| Evidence-package integrity (the R2 FAIL) | **PASS** | 5/5 recorded outputs reproduce; all RED sides on immutable pins |

---

## Findings

**None requiring repair.** No REQUEST_CHANGES item, no reproduced defect, no false claim surviving in the evidence leaf or the documents.

---

## Nits (not counted in the verdict)

1. **The device test is a partial mitigation, and two concrete bypasses go unnamed.** The generic disclosure `procfs_identity=not_established` is correct and covers them, but neither is stated: (a) an actor who already has the mount authority the threat model assumes will normally mount a *tmpfs* over `/proc` rather than bind-mounting a root-filesystem directory — a different superblock, so a different `st_dev`, so admitted; (b) `readlink` and `stat -L` are separate probes on the same path, so a `/proc` swap between the two (crafted during the readlinks, real during the stats) also passes. What the round-3 change genuinely buys is refusal of the bind-mount-from-rootfs variant, and honesty about the rest. The `stat -f -c '%t'` nsfs-magic successor option is recorded with a correct D026 justification for deferring it; that is the fix that would close (a), and re-reading the device inside the same probe would narrow (b).
2. **A new fail-closed dependency, undisclosed.** Row 8 now requires `stat -L` to succeed on all four namespace links. A host where `readlink` succeeds but `stat -L` fails previously passed row 8 and now STOPs at rc 3. For `/proc/self/ns/*` on a modern kernel this is effectively unreachable, and the direction is right for a preflight — but it is a new refusal surface that the header does not name.
3. **`ns_link_devices_distinct_from_root=yes` is a `printf` literal, not a derived value.** True whenever printed on shipped bytes, and the four raw devices plus `root_device` are on the same line so a leaf reader can check it — which is why this is a nit and not a finding. The `local root_dev="" dev_user="" …` initialisation at `:1019` exists partly so the D026 mutant reaches that line and visibly admits; that is the right call for the mutation (a `set -u` death would have been an inconclusive kill), but it does remove `set -u` as a backstop on the evidence line for a future partial edit.
4. **`p0_read_object_device`'s error arm carries no `diagnostic_shape=`.** It uses `p0_sanitize` directly, matching the sibling `stat` arm for `root_mount_identity` at `:1034` and differing from the `readlink` arms, which use `p0_prepare_readlink_detail`. Consistent within its own class; cosmetically inconsistent across the function.
5. **Commit scope, for the Lead — not an RP6 defect.** `bbb40ab6` is not confined to RP6 round 3: `WPI_PREREGISTRATION_DRAFT.md` also carries the transport round-2 four-class derivation contract (§3 plus the op-table rows 01/02/03). These are the concurrent-session working-tree edits I recorded as already present in my round-2 report; the commit message and `RP6_REPAIR_R3_REPORT.md:29-32,284-288` both disclose them as preserved-not-authored. §8.1 itself changed exactly one line. Recorded so the RP6 acceptance is not read as acceptance of the transport contract.
6. **Carried unchanged from round 2, deliberately deferred and on the record for freeze work** (R2 nits 3–9, correctly outside the round-3 contract): bash ≥ 4.4 floor undeclared; `P0_RESOLUTION` carrying two unrelated meanings; frozen `root_mount_identity` embedding a reboot-unstable anonymous `st_dev` on btrfs/overlay/zfs roots; evidence reduction on the domain STOP path; `P0_identity_admitted` / `P0_account_admitted` printed before the domain gate; the tautological `readlink -v -f -- /` comparison; and the three round-1 carry-overs (`kind=regular file` breaking key=value on the 12 tool lines, `detail=…_parent_search_succeeded` overstating what an ENOENT establishes, `evidence_stdout_bound_to_create_once_leaf` proving same-object-now rather than create-onceness).

---

## What I checked and did not find defective

- **The §8.1 row-1 amendment is the right resolution, not a grammar dodge.** The row now makes `rc=na` *mandatory* for the `mechanism=access_builtin_x` arm and reserves `rc=<n>` for an arm that actually invoked something, and records why `path=<p>` is required. That is consistent with the block's stated discipline at `:506-509` and with the fact that no P0 inventory arm ever execs.
- **The `(os error 2)` deletion is verdict-preserving on GNU.** Both surviving alternatives still match the real C-locale GNU shapes; the F1 arms still flip to rc 1 on real absent objects.
- **The row-8 grammar validators are unweakened.** `p0_read_domain_ns` still requires the label-specific shape, digits-only inner, exact-equality against the attested literal; the root identity still requires digits and exactly one colon. The device check is additive.
- **The mutation is genuinely comparison-only.** The mutant retains the device *read* (`MUTANT_DEVICE_READS_REMAINING=1`) and prints all four devices — so its admission is attributable to the missing comparison and nothing else.
- **Documents match observation.** Every executable claim in `STATUS_RP6_P0.md`, `RP6_FULLBLOCK_REPAIR_REPORT.md` and `RP6_REPAIR_R3_REPORT.md` that I could check — hash, bytes, LF count, summary strings, `cmp` results, rc values, superseded identities — matched what I measured. I found no overstated evidence claim in this round.

---

## Counts

- **Full-block D026 fence:** extracted literally by the cited line range, run **twice**, rc 0 both times, byte-identical to each other and to the recorded 156-line transcript after normalizing only the `mktemp` root. 34 arms, 39 `ASSERT_MET`, 0 `ASSERT_UNMET`.
- **Recorded harnesses re-run:** 47 cases (16 + 4 + 27) plus the freeze gate, all rc 0, all summaries `result=PASS`, all four transcripts `cmp`-identical.
- **My own fixtures, independent of the repair's:** 6 cases — 2 F1 (non-executable → exact grammar; executable → still admitted) and 4 F3 (honest / crafted / comparison-only mutant / absent object), the F3 set decided by **real GNU `stat` 8.32 on real filesystem objects**, not by a shim.
- **Fixture disclosure:** for F3, `readlink` is shimmed (Git Bash has no `/proc/self/ns` and refuses native symlinks) and `stat` is the real tool against real objects. For F1, everything is real. No `<PIN-AT-FREEZE>` literal was filled and no repository file was written.
- **Arms not driven:** real-host EACCES/ENOENT against the target Linux filesystem, real nsfs `st_dev`, and the `p0_on_err` ERR-trap backstop (still no fixture in the package). WP-I holds no host-contact authority.

**Standing unchanged:** `RP6-P0.sh` is a DRAFT — not frozen, not accepted, not dispatchable, and by construction unable to GREEN end-to-end until a root-authorised deploy channel outside the tested ssh-login domain mints and embeds the five `<PIN-AT-FREEZE>` attestation literals. This report grants no host-contact, transport, deployment, budget or trading authority, and made no repository write and no commit. The T0 round cap is now exhausted; this is my terminal verdict for the cycle, and it accepts.
