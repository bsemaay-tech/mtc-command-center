# BLOCK: 5 findings

Auditor: Codex `gpt-5.6-sol`, xhigh, second flagship T0 slot. Direct audit under
owner amendments A2/A2a; no delegation or sub-delegation.

Audited executable: `RP7-WPI-RO.sh` at commit `1c1c9ed1`, 58,012 bytes,
SHA-256 `1d118d1581534f5d16b3730efbe642e80e5232fbf8a245d238574907166a7f4e`.
The working-tree executable is byte-identical to that commit. Concurrent transport
work changed unrelated portions of `WPI_PREREGISTRATION_DRAFT.md`; a zero-context
diff scan found no change to projection v2, rows 10-24, or the binding/execution
paragraphs, and those binding surfaces were audited from commit `1c1c9ed1`.

No staging/live host was contacted, no SSH/SCP or external TCP probe ran, no RUNID
was minted, and no source or transport file was changed. Local falsification fixtures
were confined to checked temporary paths and removed. Official Python documentation
was consulted for the target Python 3.12 semantics.

The six round-3 repair subjects reproduce, and the independent projection-v2 attacks
below pass. Acceptance is nevertheless blocked. The venv used to adjudicate rows 19
and 21 executes unbound site-startup code before the intended verifier/parser; the
listener parser can emit FAIL before proving its input is complete; the metadata
preflight does not cover the full discovery universe of its own verifier; the B5/B6
semantic row order is inverted beyond the one preregistered preflight exception; and
several exact row grammars remain unimplemented.

## V-item results

| V | Result | Evidence |
|---|---|---|
| **V1 - frozen-byte identity and syntax** | **PASS** | Worktree and commit `1c1c9ed1` compare byte-identical. Independently re-derived: 58,012 bytes and `1d118d15...6a7f4e`. Git Bash `bash -n` returned 0. |
| **V2 - published QA and D026 evidence** | **PASS for the claimed round-3 repairs; not acceptance** | The exact fenced body from `SELF_QA_RP7.md` ran in Git Bash 5.2.37 / GNU coreutils 8.32, returned 0, and ended `QA_PASS all_assertions=yes`. Its v1/v2 projection, pre-fix/production `wpi_fail`, timeout-order, tool-attestation, kind-token, and ENOENT discriminators all ran. The fence has no arms for findings 1-4 below. |
| **V3 - rows 10-24 and exact grammar** | **FAIL** | Row 24 is correctly operator-side only, and the principal row 10-23 outcomes are present. Caller-specific unreadable reasons for rows 17-19a collapse to generic `path_not_evaluable`, and two raw multi-word `%F` values remain (finding 5). |
| **V4 - ordering rules** | **FAIL** | Timeout/rc/diagnostics precede `find` stdout, and the service-netns preflight precedes both network probes. But listener semantics run before rows 20-21 (finding 4), and row 22 can FAIL on an early socket before a later malformed socket is parsed (finding 2). |
| **V5 - path-object binding and projection v2** | **PASS for the mount projection; FAIL for executed-code binding** | Independent synthetic tables proved root-prefix boundaries, escaped mountinfo fields, last-record tie-breaking, stack counts, and subtree sensitivity. But rows 19 and 21 execute venv site-startup code that is neither enumerated nor bound as an adjudicator (finding 1). |
| **V6 - STOP-vs-FAIL truthfulness** | **FAIL** | Reversing the same two listener records changes rc 1 to rc 3. The case containing a malformed record is not evaluable in either order, so the wildcard-first rc 1 is false (finding 2). |
| **V7 - probe execution environment and read-only scope** | **FAIL** | `env -i -> timeout` is correctly inverted and bounded. However, `-I` does not disable Python's `site` startup; a `.pth` line executed and wrote an unallocated file before the child body (finding 1). |
| **V8 - structured parsing and complete readers** | **FAIL** | JSON itself is strict, mount readers distinguish the exercised completion cases, and `ss` is captured unfiltered. The listener semantic comparison precedes complete table parsing (finding 2), while `importlib.metadata` consumes `egg-info` objects omitted by the preflight (finding 3). |
| **V9 - local/read-only declared scope** | **PASS except finding 1** | Static scan found no row-16 forbidden descendant prefix and no SSH/SCP/operator-side row-24 implementation. All ordinary block writes target evidence leaves. Python startup breaks the claim because code from the subject venv can perform arbitrary process-authority writes before adjudication. |

## Independently executed evidence

### Frozen bytes and published fence

```text
worktree_sha256=1d118d1581534f5d16b3730efbe642e80e5232fbf8a245d238574907166a7f4e
worktree_bytes=58012
diff(1c1c9ed1)=0
bash_n_rc=0
...
BASH_N_RC=0 BYTES=58012 SHA256=1d118d1581534f5d16b3730efbe642e80e5232fbf8a245d238574907166a7f4e
QA_PASS all_assertions=yes
```

### Independent projection-v2 attack

Four mount tables used the production parser/projector: a root-only table; a mount
below the release root whose `root`, `mount_point`, and `source` contain mountinfo
escapes; an out-of-subtree prefix lookalike; and a second mount stacked at `/`.

```text
PROJECTION_ATTACK
  clean   =0ccbcd1dee9d25d387e6e3dcd5b65bf263e4c644aee2c02a81eefd3ddeb0376e
  escaped =bcf8efbf12d6a80c326f40ae7e610af8112b4a58f7de5f14cfcc786a9c7f84df
  outside =0ccbcd1dee9d25d387e6e3dcd5b65bf263e4c644aee2c02a81eefd3ddeb0376e
  stack   =28329955dae95eecbb23ecff6cff3af78107ff17325f6210d2204f18d83a5dd9
ESCAPED_SUBTREE=[... root=/x\040root ... weird\011name ... source=/dev/src\134x]
STACK_EFFECTIVE=[kind=point path=/usr/bin/stat ... source=/dev/stack shared_mount_point_records=2]
PROJECTION_ATTACK_PASS boundary=yes escaped_fields=yes last_tie=yes stack_count=yes
```

This closes the requested independent attacks on subtree visibility, boundary
matching, escaped-field preservation, equal-length tie-breaking, and stack counts.
No projection-v2 finding remains.

## Findings

### 1. Venv `site` startup executes unbound code before both adjudicators, permitting false PASS and mutation - BLOCK

**Locations:** `RP7-WPI-RO.sh:812` (`python -I verify_lock.py`) and
`RP7-WPI-RO.sh:895-919` (`python -I -c <status parser>`); preregistration probe
execution-environment rule.

`-I` is not `-S`. Python 3.12 documents `-I` as implying `-E`, `-P`, and `-s`,
not `-S`. The `site` module is therefore still imported, and executable `import`
lines in venv `site-packages/*.pth` run during startup. See the official
[Python 3.12 command-line documentation](https://docs.python.org/3.12/using/cmdline.html#cmdoption-I)
and [`site` startup documentation](https://docs.python.org/3.12/library/site.html).

The block uses the venv being judged as the interpreter for two accepting
adjudicators. A `.pth` or `sitecustomize.py` in that same tree runs before the embedded
strict-JSON source and before the digest-bound `verify_lock.py`. It can silently
replace imported modules, print the exact accepted one-line result and exit 0, alter
the evidence directory, or perform any other operation available to `gatea`. The
cleared environment, fixed cwd, mount projection, and `-I` do not prevent it.

**Executed falsification.** A temporary venv contained one `.pth` line that wrote
`pth.marker`. The child body was harmless and identical in both runs:

```text
CHILD_BODY
CHILD_BODY
PTH_MUTATION I_rc=0 I_marker=True I_S_rc=0 I_S_marker=False
```

Thus the production option (`-I`) executed code and mutated state before the intended
child, while adding `-S` prevented that startup code. A malicious one-line startup
hook can instead emit `OK fields=8` or
`verify_lock: PASS: lock+installed; packages=56` and terminate before the intended
adjudicator runs. This is simultaneously Pattern 4 (untrusted child startup), Pattern
9 (the claimed parser is not necessarily the process that produced the line), a
false-PASS route, and a violation of the read-only/create-once mutation claim.

**Required repair.** Do not let the subject venv arbitrate its own status or package
state. Run the status parser under a separately pinned/bound trusted interpreter with
site disabled. Redesign parity so a trusted interpreter inspects an explicit venv
metadata path without importing venv startup configuration, or use `-I -S` plus an
explicit, complete discovery implementation. Add D026 fixtures in which `.pth` and
`sitecustomize.py` forge accepted output and attempt a write: RED now, GREEN only when
neither executes.

### 2. Row 22 can emit a semantic FAIL before the complete `ss` table is parsed - HIGH

**Locations:** `RP7-WPI-RO.sh:853-880`, especially the in-loop FAILs at `:876-877`;
preregistration row 22 and the general probe-output precedence rule.

The draft requires the unfiltered table to be captured whole, **every** socket row to
be structurally parsed, and only then the port-8790 semantics to be applied. The code
does capture the whole child stdout, but it calls `wpi_fail` immediately when an early
row is wildcard or non-preregistered. A malformed or unterminated later record is
never read, so an inability to evaluate the table becomes a host-state FAIL.

**Executed falsification.** The same two records were supplied in opposite order:

```text
B6_FAIL reason=nonloopback_listener addr=0.0.0.0
B6_STOP reason=listener_inventory_unreadable_or_unparseable rc=0 detail=table_grammar
LISTENER_ORDER wildcard_first_rc=1 malformed_first_rc=3 expected_both_stop=3
LISTENER_ORDER_FALSIFIED early_semantic_fail_precedes_complete_parse=yes
```

Both files contain a malformed record; complete structural parsing cannot hold in
either order. This is the exact Pattern-6 partial-interpretation defect the binding
rule forbids.

**Required repair.** Parse and validate all rows to clean EOF first, recording only
sanitised semantic counters/flags during the loop. Apply wildcard, unexpected-address,
and count FAILs only after reader diagnostics, record termination, and grammar all
hold. The two order permutations above must both be D026 RED/GREEN evidence.

### 3. Row 19's readability preflight omits metadata formats its verifier consumes - HIGH

**Locations:** `RP7-WPI-RO.sh:746` (`find ... -name '*.dist-info'`) and the candidate
`IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py:43-49`
(`importlib.metadata.distributions()`).

The preregistration says the preflight proves every metadata object the verifier
consumes readable, then equates that universe with `*.dist-info/METADATA` and
`RECORD`. Python 3.12's `importlib.metadata` explicitly discovers both `dist-info`
and `egg-info`, may discover metadata in zip entries on `sys.path`, and supports
extended finders. See the official
[`importlib.metadata` documentation](https://docs.python.org/3.12/library/importlib.metadata.html).

**Executed falsification.** A directory containing only
`ghost.egg-info/PKG-INFO` was passed to the real standard-library discovery API:

```text
[('ghost', '1.0', 'PathDistribution')]
PY_RC=0
```

Production row-19 preflight cannot enumerate that object because its `find` predicate
admits only `*.dist-info`. Therefore it has not established complete readability of
the verifier's input universe, and neither a named mismatch FAIL nor a PASS is
admissible under the binding paragraph. Finding 1 makes this worse because `.pth`
can add more search locations and custom finders before discovery starts.

**Required repair.** Define one explicit discovery universe shared by preflight and
verifier. Either enumerate and validate every format/location the verifier accepts
(`dist-info`, `egg-info`, zip/extension routes as applicable), or make the trusted
verifier reject every non-preregistered format/location before comparing versions.
Add readable, unreadable, malformed, and unexpected `egg-info` D026 cases.

### 4. The implementation inverts the semantic B5/B6 row order, not only the authorised row-22 preflight - MEDIUM

**Location:** `RP7-WPI-RO.sh:981-986`; preregistration rows 20-23 and namespace-binding
paragraph.

The draft explicitly authorises one display-order inversion: the **service-netns
preflight** from row 22 must run before rows 20-21 and before the `ss` interpretation.
After that preflight, the predicted-first-divergence table still places B5 endpoint
and flags (20-21) before B6 listener semantics (22-23). The implementation does:

```text
wpi_assert_netns_binding
wpi_assert_listener_set
wpi_assert_status
```

Consequently a listener FAIL is recorded before an independently present row-20/21
deviation. The comment says the binding order is intentional, but the call order
also moves the whole listener adjudication; that additional inversion is not
preregistered.

**Required repair.** Preserve the authorised preflight inversion only:
`netns binding -> status rows 20-21 -> listener rows 22-23`, or amend and independently
approve the preregistered first-divergence order before executable bytes change. Add a
two-deviation fixture proving which result is first.

### 5. Exact row/result grammar still has caller-reason and token-shape gaps - LOW

**Locations:** generic `wpi_lstat` STOPs at `RP7-WPI-RO.sh:248-266`, regular-digest
callers at `:685-694` and `:807-812`, and raw metadata-kind renderings at `:762` and
`:768`; preregistration rows 17-19a.

Required exact-grammar mismatches remain:

1. A stat/access/diagnostic failure while binding `requirements.lock` is emitted as
   `B1a_STOP reason=path_not_evaluable`, while row 17 requires
   `installed_lock_unreadable`. The same generic helper output replaces row 19a's
   `verifier_unreadable` and row 19's `metadata_unreadable` on their lstat paths.
2. A regular lock/verifier leaf with wrong numeric ownership reaches generic
   `path_metadata_mismatch`; rows 17 and 19a do not preregister that form.
3. The row-17 object-kind implementation adds `path=<p>` to
   `installed_lock_object_unexpected`, while the exact table records only `kind=<k>`.
4. `dist_info_kind_$WPI_META_KIND` and `kind_$WPI_META_KIND` interpolate raw GNU `%F`;
   values such as `character special file` split the space-delimited evidence grammar.
   Round 3 added `wpi_kind_token` for two identical sites but left these two reachable.

These are not false-PASS routes by themselves; the rc class remains STOP or FAIL.
They are nevertheless required repairs because the kickoff makes the row grammar
exact and the draft calls the `binding=`/result tokens preregistered evidence.

**Required repair.** Carry a caller-specific unreadable reason through lstat/component
walks, reconcile every regular-digest metadata-deviation form with rows 17/19a, and
route all `%F` values through `wpi_kind_token`. Falsify each emitted line against an
erroring stat and a multi-word object kind.

## Freeze-gate items acknowledged, not findings

1. `WPI_FIXED_ATTESTED_MOUNT_PROJECTION_SHA256='<PIN-AT-FREEZE>'` deliberately prevents
   an accepting `wpi_validate_inputs` arm. I did not reclassify the absent GREEN as a
   QA defect. The accepting arm remains mandatory after the deploy channel supplies
   the v2 digest and before dispatch.
2. The attestation placeholder itself is deliberate. No end-to-end RP7 PASS can or
   should exist before it is pinned.
3. Row 24 remains correctly operator-side and is not evaluated by RP7.

## Limits of this audit

- No staging execution was attempted or authorised.
- No real bind/overlay mount was created. Projection attacks used exact synthetic
  mountinfo records with the production parser/projector, matching the established QA
  method.
- The `.pth` mutation was executed on local Python 3.14; the relevant behavior is
  explicitly documented for target Python 3.12 in the primary sources linked above.
- `shellcheck` is not installed; no ShellCheck result is claimed.

This is the second flagship T0 verdict. Because it is non-accepting and round 3 is the
recorded T0 cap, RP7 cannot freeze or dispatch under the current contract; the blocker
returns to Barış rather than silently opening a fourth repair round.
