# AUDIT REPORT — `RP6-P0.sh`, Claude flagship T0 slot (claude-opus-5, xhigh)

## VERDICT: BLOCK: 7

Seven required findings. Two are HIGH: the block's filesystem-object classifier **cannot match on any host**, which makes its entire rc-1 FAIL contract for the two arms the header names unreachable and reinstates `[AUDIT1 F5]`; and **§8.1 row 8 is not implemented and not disclosed** in the block's own out-of-scope enumeration. Both were missed by all five prior rounds. All findings below carry executed falsifications.

Scope note: audit performed on Windows Git Bash, GNU coreutils 8.32, bash 5.x. `RP6-P0.sh` and every other repository file I read are byte-identical to their pre-session state (re-derived below); all fixtures were written to the session scratchpad only. `RP7-WPI-RO.sh` shows as modified in `git status` — that is a concurrent RP7 R3 session, not this one; I read only its committed HEAD bytes.

---

## Section 1 — Re-derivation and mechanical gates

| Item | Claimed | Observed | Verdict |
|---|---|---|---|
| SHA-256 | `bff3c86e6e9b565c55da34580284f22c80253d9e931d879fd749459bac85b7cf` | identical | **PASS** |
| Bytes | 57441 | 57441 | **PASS** |
| `bash -n` | PASS | rc 0 | **PASS** |
| Line endings / BOM | — | LF only (0 CR), no BOM, ASCII | **PASS** |
| Post-audit integrity | — | hash + bytes unchanged; `SELF_QA_RP6.md`, `STATUS_RP6_P0.md`, prereg, pattern catalogue all clean in `git status` | **PASS** |

**Harness re-runs, verbatim from the document.**

- Harness 1 — `sed -n '1159,1324p' SELF_QA_RP6.md | bash --noprofile --norc` → process rc 0, `C13_R4_ARM_QA_SUMMARY cases=27 result=PASS`, 25 `CASE_OK` + 2 `PROBE_OK`, 0 `CASE_BAD`/`PROBE_BAD`. `diff` against the 201 recorded output lines (1335–1535): **byte-identical**.
- Harness 2 — `sed -n '942,1025p' SELF_QA_RP6.md | bash --noprofile --norc` → process rc 0, `C13_R3_BACKSTOP_QA_SUMMARY inputs=2 mutations=2 cases=4 result=PASS`. `diff` against recorded lines 1033–1074: **byte-identical**.

Both harnesses are genuine D026 evidence: polarity-checked, mutation-killed, block-driven, and reproducible without an edit. Pattern 10 is not instantiated by the QA.

**End-to-end drive (new — no prior round did this).** I built a full fixture (stubbed `rp0_*` predicates, real create-once leaf with `exec >`, shimmed `getent`/`systemctl`/`ss`, fixture venv + interpreter, `readlink` shim for `/proc/self/ns/*` which this platform lacks) and drove the **whole block** to `P0 PASS` rc 0, then ran 20 falsification cases against it. Three constants (`P0_NS_*_PATH`) were repointed **in a scratchpad copy**; the repository file was never written.

---

## Section 2 — §8.1 row-by-row conformance

| Row | Requirement | Implementation | Executed evidence | Verdict |
|---|---|---|---|---|
| 1 | `getent` present; `missing_tool tool=getent`, or `tool_not_evaluable tool=getent rc=<n> detail=<d>` | resolved as 12th inventory tool; `missing_tool` token exact | `P0_STOP reason=missing_tool tool=getent rc=1 detail=[]` | **PARTIAL** — `tool_not_evaluable` absent from the block (finding 7) |
| 2 | complete unique `getent passwd gatea`; numeric `id -u`/`-g` equal record; `identity_unresolvable` / `identity_unexpected observed_numeric=… expected_numeric=… account=gatea` | implemented, numeric-only, full 7-field parse | harness 1 cases 4,5,12; `identity_unexpected account=gatea` rc 3 | **PARTIAL** — token correct; identity-section emits the same token with an incompatible field grammar (finding 7) |
| 3 | `getent passwd mtc-bridge` → `999:988`; `id -G` excludes 0 and 988; `group_query_not_evaluable`; `capability_wider_than_ledger gid=<g>` | numeric compare vs `P0_STATE_UID/GID`; whole-word forbidden-gid scan | `P0_STOP reason=capability_wider_than_ledger gid=4096 caller_gids=[4096]` rc 3; harness 1 cases 1–3 | **PARTIAL** — `group_query_not_evaluable` absent (finding 7) |
| 4 | `ss` present | in inventory | `P0_tool name=ss … resolution=path_resolved_absolute` | **PASS** |
| 5 | `curl` present | in inventory | `P0_tool name=curl …` | **PASS** |
| 6 | `sha256sum` present | in inventory | `P0_tool name=sha256sum …` | **PASS** |
| 7 | `systemctl` present | in inventory | `P0_tool name=systemctl …` | **PASS** |
| 8 | **execution-domain binding** vs frozen external attestation; `execution_domain_unattested` / `execution_domain_mismatch` | **not implemented anywhere**; namespaces are record-only | `grep -n 'execution_domain\|attest'` → zero matches in executable code | **FAIL — finding 2** |
| 9 | manager readiness, **"only after row 8"** | implemented well (Manager `show --property=Version`, `env -i`, absolute binary, fail-closed) — but runs with row 8 absent | `P0_system_manager_ready …` rc 0; `system_manager_unreachable rc=127 detail=invocation_command_not_found` | **PARTIAL** — the arm itself is sound; its stated precondition is unmet (finding 2) |

---

## Section 3 — V-item evidence

| V | Item | Verdict | Evidence |
|---|---|---|---|
| V1 | Hash / bytes / syntax | PASS | Section 1 |
| V2 | §8.1 rows 1–9 at exact grammar | **FAIL** | Section 2; findings 2, 7 |
| V3 | STOP-vs-FAIL truthfulness on every branch | **FAIL** | findings 1, 3 |
| V4 | Numeric-identity rule (Pattern 8) | PASS | no `%U`/`%G`/`id -un`/`-gn` anywhere; `id` asked only `-u`,`-g`,`-G` (5 sites); names captured but never compared |
| V5 | Capability ledger (forbidden gids) | PASS | whole-word match on space-padded list; gid 0 does not match gid 10; executed RED above |
| V6 | getent arm incl. R4 sentinel | PASS with residual | harness 1 re-run byte-identical; newline-only rc-2 → `error`/`newline_only_capture_at_rc2` reproduced independently; residual = finding 6 |
| V7 | `:?` backstops | PASS | harness 2 re-run byte-identical; mutant killed (`precheck_and_backstop` → `unbound variable`, assertion correctly UNMET) |
| V8 | Tool inventory (12 tools) | PASS | `P0_tool_inventory count=12`; superset of every pinned tool variable in the committed RO block (`WPI_STAT/READLINK/ENV/FIND/SHA256SUM/SS/SYSTEMCTL/CURL/INTERPRETER`) |
| V9 | Namespace / manager arms | PASS (arms) | both driven GREEN and RED; namespace claim is honestly `record_only binding=not_established` — Pattern 2 is *not* instantiated by the token, only by the missing row-8 gate |
| V10 | Evidence-leaf binding | PASS | dev:inode identity via fd 8 verified on a real leaf; `evidence_leaf_not_bound` RED reproduced; fd 8 closed on all three exit paths (GLM F6 is genuinely closed) |
| V11 | Read-only scope | PASS | no redirection, `mktemp`, `rm`, `mv`, `cp`, `chmod`, `touch`, or `tee` in the block; only `exec 8>&1`/`8>&-`, disclosed |
| V12 | Harness re-runs (27 + 4) | PASS | Section 1 |

**Same-family adversarial pass on R3/R4 (Claude-implemented), as instructed.** The sentinel construction is correct, not merely plausible: `getent` is on the left of `||` so an inherited `set -e`/ERR trap cannot kill the subshell before `printf x`; `exit "${getent_rc:-0}"` genuinely carries the tool's rc out (a bare `; printf x` would mask it); `getent_rc` is assigned only inside the substitution subshell so it cannot leak between calls; `had_bytes` is decided **before** the trailing-newline normalization; and the normalization genuinely restores the R3-audited value, which the 16 verbatim R3 regression cases confirm. I found one surviving hole (finding 6) and one harness-fidelity limitation (nit 4). I did not find the R3/R4 work to be self-serving.

---

## Findings — most severe first

### Finding 1 — HIGH. The stat-diagnostic classifier can never match, so every filesystem-object FAIL arm is dead code and `[AUDIT1 F5]` is reinstated (Pattern 1)

`RP6-P0.sh:910-919` matches an exact shape whose program-name prefix is the literal `stat:`:

```
"stat: cannot statx '$p': $P0_ENOENT_TEXT"|"stat: cannot stat '$p': $P0_ENOENT_TEXT")
```

But the block deliberately invokes stat by the **resolved absolute path** at all five call sites (`RP6-P0.sh:433,518,525,924,929`: `LC_ALL=C "$P0_STAT" …`). GNU `error()` prints `program_invocation_name`, i.e. `argv[0]` verbatim — so the real diagnostic is `/usr/bin/stat: cannot stat '<p>': …`, which the pattern cannot match. Same binary, two `argv[0]` forms:

```
$ stat -c '%F' -- /nonexistent/xyz
stat: cannot stat '/nonexistent/xyz': No such file or directory
$ /usr/bin/stat -c '%F' -- /nonexistent/xyz
/usr/bin/stat: cannot stat '/nonexistent/xyz': No such file or directory
```

`P0_SHAPE` therefore never becomes `enoent` or `eacces`, and `p0_probe_kind` falls through to the generic `path_probe_unclassified` for **every** stat failure.

**Executed falsification.** Identical fixture, missing venv root; the only variable is whether the diagnostic carries the absolute prefix:

```
production behaviour  → BLOCK_RC=3  P0_STOP reason=path_probe_unclassified path=<W>/venvs_missing/2ce41e34…321b
argv[0] rendered bare → BLOCK_RC=1  P0_FAIL reason=venv_root_absent path=<W>/venvs_missing/2ce41e34…321b detail=preregistered_path_observed_missing
```

Same for the interpreter:

```
production behaviour  → BLOCK_RC=3  P0_STOP reason=path_probe_unclassified path=<W>/…/bin/python
argv[0] rendered bare → BLOCK_RC=1  P0_FAIL reason=interpreter_absent path=<W>/…/bin/python detail=preregistered_path_observed_missing_parent_search_succeeded
```

And for EACCES (`path_probe_denied` likewise unreachable):

```
production behaviour  → P0_STOP reason=path_probe_unclassified … detail=/usr/bin/stat: cannot statx …
argv[0] rendered bare → P0_STOP reason=path_probe_denied      … detail=stat: cannot statx …
```

**Dead arms:** `venv_root_absent` (rc 1), `interpreter_absent` (rc 1), `interpreter_symlink_dangling` (rc 1, via unreachable `link_dangling`), `venv_root_is_symlink kind=link_dangling`, and `path_probe_denied` (rc 3, correct reason). These are precisely "The two classes that are FAIL here" that `RP6-P0.sh:44-56` spends thirteen lines asserting the block gets right.

**Why five rounds missed it.** The accepted `RP1-B3.sh` carries the byte-identical classifier (`RP1-B3.sh:575-583`) but invokes stat by **bare name** (`RP1-B3.sh:236,241,587`: `LC_ALL=C stat -c …`), so it matches and six B3 audit rounds validated it. RP6-P0 inherited the classifier and hardened the invocation to a pinned absolute path — silently breaking it. This is the catalogue's own "findings that existed only because of an earlier fix" shape. It survived because no round ever executed the arm: the GLM audit was inspection-only, the C13 rounds were scoped to the accounts arm, and the SELF_QA harnesses extract only `p0_resolve_passwd`/`p0_resolve_accounts`.

**Residual uncertainty, stated:** my demonstration is on GNU coreutils 8.32 under MSYS. The mechanism (`error()` → `program_invocation_name` = `argv[0]`) is glibc/gnulib-generic and not platform-specific, and the same-binary two-prefix demonstration isolates it, but the target-host confirmation has not been executed because WP-I has no host-contact authority.

**Minimal fix.** Match the diagnostic as `*": cannot statx '$p': $P0_ENOENT_TEXT"` / `*": cannot stat '…"` anchored on the *suffix*, with an additional guard that the prefix equals `$P0_STAT`; or invoke via a pinned absolute path while asserting the prefix. Either way, re-drive both object arms and record RED at rc 1.

---

### Finding 2 — HIGH. §8.1 row 8 (execution-domain binding) is neither implemented nor disclosed; row 9 runs without its stated precondition (Pattern 2 + Pattern 9)

Row 8 requires the login's user/mount/PID/network namespace identities plus canonical root-mount identity to equal **externally attested values frozen into `RP6-P0.sh`**, with `execution_domain_unattested` / `execution_domain_mismatch` as the divergences, and states: "an apparently successful query from a container, chroot, private namespace or visible-PID-1 lookalike is STOP, not host evidence." Row 9 opens "**only after row 8**".

The block implements nothing of this. `grep` for `execution_domain`, `attested`, `unattested`, `root_mount` returns zero matches in executable code. The namespace section is explicitly `RECORD ONLY`.

This is not a spec-drift artefact: row 8 was introduced in the round-1.4 commit `6a8b0896` and is **byte-identical** in the current round-1.6 text, i.e. it predates every commit of `RP6-P0.sh`.

**Why this is a finding and not merely a scope decision.** The block *has* an out-of-scope section whose stated purpose is "Silence about an excluded check is how a scope reduction becomes an unnoticed coverage loss. Everything P0 does not implement is named here." (`RP6-P0.sh:1069-1077`). Row 8 is not named there. The `does_not_establish` line does disclose `binding_of_these_namespaces_to_any_service_or_to_the_host_initial_namespaces`, but that is a limitation statement, not an acknowledgement that a preregistered P0 row is unimplemented — an operator reading `P0_out_of_scope` as the exhaustive omission list is misled. This is structurally the same defect as `[WPI-AUDIT F6]` ("authority omitted from an apparently exhaustive dispatch gate").

**Concrete asymmetry making the gap load-bearing.** The successor block *does* implement an attested-domain gate. From the committed `RP7-WPI-RO.sh`:

```
444:  [ "$WPI_MOUNT_PROJECTION_DIGEST" = "$WPI_ATTESTED_MOUNTINFO_SHA256" ] || \
445:      wpi_stop RP7 "mount_topology_mismatch observed=… attested=… format=normalised_path_projection_v1"
878:  # Establish the deploy-attested projection before the first tool/object
```

So the RO stage asserts the attested binding for its own rows, while the P0 preflight whose entire purpose is "the premises every later WP-I claim rests on" does not — and P0's terminal claim nonetheless asserts `system_manager_answered_a_Manager_property_query_over_the_system_bus_from_this_login_namespaces`, an unattested-domain claim.

**Why five rounds missed it.** `RP6_P0_GLM_AUDIT_2026-08-10.md` records it directly: "The prereg 8.1 expectation table and the feasibility ledger … were **not among the five files supplied**". The GLM re-audit was bounded to F1/F3/F4; both Codex rounds were bounded to C13 rows 1–3. No round has ever checked rows 4–9 against the table.

**Minimal fix.** Either implement row 8 (preregistered attested namespace + canonical root-mount identities, with the two named tokens), or obtain a Lead adjudication reducing row 8 and record it as `P0_out_of_scope class=… item=prereg_8.1_row8_execution_domain_binding … implemented=no`, and amend row 9's "only after row 8" wording. Do not leave the omission implicit.

---

### Finding 3 — MEDIUM. A non-canonical *preregistered input* is emitted as deviant host state (rc 1 FAIL), contradicting the block's own input rule (Pattern 1)

`RP6-P0.sh:259-261` states the rule: "A missing or malformed operator input is COULD NOT EVALUATE, not deviant host state." The input validator for `P0_VENV_ROOT` rejects non-absolute, non-printable, whitespace-bearing, `/../`, `/./` and non-candidate-bound values — but **not** a doubled separator. `p0_assert_venv_root` then compares `readlink -f` output against the literal string and calls `p0_fail` on any difference, conflating two different observations:

- the host chain contains a symlink/non-canonical component → deviant state, FAIL correct;
- the operator's preregistered *string* is non-canonical while the host object is exactly right → input defect, STOP per the block's own rule.

**Executed falsification.** Identical, healthy host object; only the spelling of the preregistered input differs:

```
P0_VENV_ROOT=<W>/venvs/2ce41e34…321b   → BLOCK_RC=0   P0 PASS
P0_VENV_ROOT=<W>//venvs/2ce41e34…321b  → BLOCK_RC=1   P0_FAIL reason=venv_root_not_literal_canonical
                                                       path=<W>//venvs/2ce41e34…321b canonical=<W>/venvs/2ce41e34…321b
```

rc 1 is the strongest verdict in the contract — it accuses the host. A plumbing error in the preregistration would produce a WP-I run reporting deviant staging state.

**Minimal fix.** Reject repeated `/` in the input validator (STOP, `input_not_canonical_spelling`), or split the arm: if `canon` differs from `d` only by separator normalization, STOP as an input defect; if it differs because a component resolved elsewhere, FAIL.

---

### Finding 4 — MEDIUM. Duplicate/conflicting tool pins are silently resolved first-wins, and `resolution=pinned_absolute` is recorded anyway (Pattern 5)

`p0_lookup` (`RP6-P0.sh:176-185`) returns the first matching entry. The `P0_TOOL_PINS` validation loop (`RP6-P0.sh:342-364`) checks each entry's shape, tool membership and absoluteness, but never checks that a tool appears **at most once**. A pin table carrying both the true pin and a stale or decoy pin therefore silently discards the disagreement the pin table exists to detect — `RP6-P0.sh:335-337`: "a disagreement is a shadowing signal and STOPs."

**Executed falsification.** The same two-entry table, differing only in order:

```
P0_TOOL_PINS="stat=/usr/bin/stat stat=/nonexistent/stat"
  → BLOCK_RC=0  P0_tool name=stat path=/usr/bin/stat … resolution=pinned_absolute
                P0_tool_inventory count=12 pinned=2 provenance=not_established
                P0 PASS

P0_TOOL_PINS="stat=/nonexistent/stat stat=/usr/bin/stat"
  → BLOCK_RC=3  P0_STOP reason=tool_pin_mismatch tool=stat pinned=/nonexistent/stat resolved=/usr/bin/stat
```

Two secondary defects in the same evidence line: `resolution=pinned_absolute` asserts the resolved path was checked against *the* pin when a contradictory pin was silently dropped, and `pinned=2` counts entries, not pinned tools (control run with one entry prints `pinned=1`, so the two are indistinguishable to a reader).

**Minimal fix.** STOP with `input_pin_duplicate tool=<t>` on any repeated tool name; count distinct pinned tools.

---

### Finding 5 — MEDIUM. All three `readlink` producers are structurally diagnostic-free, so three STOP arms record an empty `detail=` (Pattern 6 / Pattern 9)

`RP6-P0.sh:24-29` is the block's central discipline claim: "Every producer … has its stdout and stderr captured together, and has its status **and its diagnostics** adjudicated". GNU `readlink` prints **nothing** on failure unless `-v` is given, and the block passes `-v` at none of its three call sites (`:511` evidence binding, `:810` namespace, `:987` venv canonicalization).

**Executed evidence.**

```
$ out="$(readlink -- /proc/self/ns/net 2>&1)"; echo "rc=$? bytes=${#out}"
rc=1 bytes=0
$ out="$(readlink -f -- /nonexistent/a/b 2>&1)"; echo "rc=$? bytes=${#out}"
rc=1 bytes=0
$ readlink -v -- /proc/self/ns/net
readlink: /proc/self/ns/net: No such file or directory
```

Driven through the block:

```
P0_STOP reason=namespace_unreadable ns=net path=/proc/self/ns/net rc=1 detail=
```

The merged-capture argument at `RP6-P0.sh:26-29` ("any stderr text destroys the shape") buys nothing here because there is never any stderr text. Operationally this means an EACCES on `/proc/self/fd/8` and an ENOENT on it are indistinguishable in the evidence leaf — exactly the "could not ask" vs "asked and got X" distinction P0 exists to preserve. Not a false verdict (all three are correctly STOP), but a systematic evidence loss on three arms plus a `detail=` with no value in the key=value grammar.

**Minimal fix.** Add `-v` to all three `readlink` invocations, or state in the header that readlink failures carry no diagnostic by design.

---

### Finding 6 — LOW/MEDIUM. The R4 sentinel does not survive NUL bytes: a NUL-only rc-2 capture is still admitted as a valid no-match (Pattern 9; narrow survivor of C13 finding 1)

`RP6-P0.sh:669-675` claims: "**ANY byte** includes a bare newline… so the complete merged stream survives and the emptiness question is decided on the real bytes." Bash strips NUL bytes from a command substitution *before* the sentinel logic can see them, so the claim is false for NUL.

**Executed falsification** (extracted `p0_resolve_passwd`, shim exiting 2 after `printf '\000\000'`):

```
warning: command substitution: ignored null byte in input
OUTCOME=nomatch DIAG=[empty_capture_at_rc2]
```

control, single newline (the R4 fixture):

```
OUTCOME=error DIAG=[newline_only_capture_at_rc2]
```

For `mtc-bridge` this reaches `state_account_resolution_unexpected … observed_numeric=absent` — a positive-absence assertion about a resolver that actually emitted bytes, which is the class the C13 audit finding 1 and re-audit finding 1 both attacked. Realism is low and bash offers no builtin NUL-preserving substitution, so the honest repair is disclosure rather than code. Note also that bash's own warning goes to an unadjudicated stderr.

**Minimal fix.** Narrow the header claim to "any byte bash can represent in a command substitution (NUL excepted)" and record the NUL residual in `does_not_establish`.

---

### Finding 7 — LOW/MEDIUM. Two §8.1 divergence tokens are unimplemented, and `identity_unexpected` is emitted with two incompatible field grammars

The kickoff requires every P0 row at its **exact** FAIL/STOP grammar. Three deviations:

1. Row 1's invocation-failure divergence `P0_STOP reason=tool_not_evaluable tool=<t> rc=<n> detail=<d>` does not exist in the block; the nearest arm emits `tool_not_executable tool=$t path=$resolved mechanism=access_builtin_x` (`RP6-P0.sh:422`). Zero matches for `tool_not_evaluable`.
2. Row 3's pre-interpretation group divergence `P0_STOP reason=group_query_not_evaluable rc=<n> detail=<d>` does not exist; a failed `id -G` emits `identity_probe_failed field=gids flag=-G rc=… detail=…` (`RP6-P0.sh:568`).
3. Row 2's divergence is `identity_unexpected observed_numeric=<u:g> expected_numeric=<u:g> account=gatea`. The accounts arm emits it with an extra key jammed inside a value: `expected_numeric=$live_uid:$live_gid,prereg_uid=$P0_EXPECT_UID` (`RP6-P0.sh:760`). The identity arm emits the **same reason token** with an entirely different field set — executed: `P0_STOP reason=identity_unexpected uid=4096 expected=4242` — with no `account=`, `observed_numeric=` or `expected_numeric=` at all. One reason token, three grammars, none of them the table's.

**Minimal fix.** Either add the two missing tokens and unify the `identity_unexpected` field set, or amend §8.1 and record the amendment — the kickoff makes the table authoritative for reason strings.

---

## Nits (not counted in the verdict)

1. **`kind=regular file` breaks the key=value evidence grammar.** `%F` yields a multi-word value, unquoted into the log — reproduced on all 12 tool lines: `P0_tool name=stat path=/usr/bin/stat kind=regular file mode=755 …`. A whitespace-splitting reader sees a bare `file` token. Only the tool-inventory line is affected (`P0_KIND` elsewhere is a controlled token set).
2. **`detail=preregistered_path_observed_missing_parent_search_succeeded`** (`RP6-P0.sh:1011`) is not established by the probe. ENOENT names the full path whether the missing component is `python` or `bin`; `$P0_VENV_ROOT/bin` is never probed. The verdict polarity is defensible; the token is not. Same overstatement in the header at `RP6-P0.sh:47-50` ("positively proves that directory search succeeded").
3. **`evidence_stdout_bound_to_create_once_leaf`** (`RP6-P0.sh:1085`) — GLM F5, still open. The probe proves same-object *now*; create-onceness is the bootstrap's invariant. The GLM re-audit logged it as a carried nit; it remains.
4. **Harness fidelity limitation.** The extracted-function harnesses run under `set -Eeuo pipefail` with **no `ERR` trap installed**, so `p0_on_err`/`unadjudicated_command_status` cannot be exercised by them. Nothing observed is masked by this, but the backstop the header calls "a backstop, not the mechanism" has no fixture.
5. **Unquoted map expansions** (`for e in $map`, `for p0_g in $P0_FORBIDDEN_GIDS`, `for p0_pin in $P0_TOOL_PINS`, `for g in $gids`) undergo pathname expansion as well as word splitting. I traced every path: all fail closed to STOP. Hygiene only.
6. **GLM F6 is genuinely closed** — `exec 8>&-` now precedes both STOP paths and runs unconditionally (`RP6-P0.sh:514,521,526`). Recorded because the GLM re-audit listed it as still-carried.

---

## What I checked and did **not** find defective

- **Pattern 8** is cleanly honoured: no `%U`/`%G`, no `id -un`/`-gn`, every input numeric and digit-validated, names captured strictly as diagnostics, forbidden-gid matching whole-word on a space-padded list so gid 0 cannot match gid 10.
- **Pattern 6 ordering** is correct at every capture site: status adjudicated before any byte is interpreted, raw capture inspected for CR/LF **before** sanitization, sanitization used only for printing.
- **Pattern 4** on the two sensitive children is correct: `env -i LC_ALL=C` + absolute binary for the manager query, `env -i` + `-I` for the interpreter. My fixture accidentally proved the clearing works — an exported `SHIM_MGR` could not reach the systemctl child.
- **`p0_stop` is never reachable from inside a command substitution** (zero `$(p0_…` sites), so a STOP can never be captured into a caller's variable.
- **Read-only scope** holds: no redirection, temp file, or mutating tool anywhere in the block; only the disclosed fd-8 dup/close.
- **Evidence binding by dev:inode** is sound and was driven both GREEN and RED on a real leaf.
- **The C13/R3/R4 accounts arm** is well built. The sentinel, the `||` placement against an inherited `set -e`, the rc carry-out, the pre-normalization `had_bytes` decision, and the behaviour-preserving re-normalization are all correct as reasoned, and 16 verbatim R3 regression cases confirm no behaviour drift. Finding 6 is its only survivor.

---

## Counts

- Arms driven against the real block bytes, end-to-end: **1 full GREEN pass** (`P0 PASS`, rc 0) covering prerequisites, inputs, 12-tool inventory + metadata, evidence binding, identity, accounts, namespaces, manager, venv root, interpreter, out-of-scope, terminal claim.
- Falsification cases executed by me: **20** (14 mode cases + 2 argv[0] RED/GREEN pairs + 1 EACCES pair + 2 pin-order cases + 1 NUL/newline pair), plus **31** re-run harness cases (27 + 4).
- Arms driven against stubs/shims: the getent, systemctl, ss, python, `/proc/self/ns/*` and (for finding 1 only) stat producers were shimmed; disclosed at each point.
- Arms not driven: row 8 (does not exist); `p0_on_err` ERR-trap backstop (no fixture in the package, none built here); real-host EACCES/ENOENT against the target Linux filesystem (no host-contact authority).

**Standing unchanged:** `RP6-P0.sh` is a DRAFT — not frozen, not accepted, not dispatchable. No host was contacted, no network command was run, and no repository file was modified by this session.
