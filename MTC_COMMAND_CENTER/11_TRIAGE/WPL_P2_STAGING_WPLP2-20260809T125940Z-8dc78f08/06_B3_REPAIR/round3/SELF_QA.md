# SELF QA - B3-GAP-ENV Option 1 design repair, round 3 (FINAL)

Subjects: `round3/RP1-B3.sh` (637 lines), `round3/RPD-VERIFY.sh` (750 lines).

```
e561e8b4cf5444bebf2293046a3ea649712d3b229bd380e1c69364ab552397dd  RP1-B3.sh
f4c5d61de7e55bd7f2fc9f6a73754a093cb114b1c8316b85a683a78f833e63a2  RPD-VERIFY.sh
```

No remote host was contacted. Nothing outside `round3/` was written inside the
repository; the harness, its stubs and its fixtures live in a session scratch
directory outside the repository tree. Neither block was run against
`/etc/mtc-bridge`, `/opt/mtc-bridge` or any other target path: the QA host is
Windows/MSYS and has none of them.

**Two textual substitutions are applied to every transcript in this file, and
only these two. Nothing else in any recorded output is altered.**

| Rendered as | Actual string |
|---|---|
| `$QA` | `/c/Users/BARSEM~1/AppData/Local/Temp/claude/C--LAB-Tradingview-LAB-CLEAN/1f65c7cb-69bb-48cd-ba00-ed3aaa793ce4/scratchpad/r3` |
| `$QAW` | the same directory in the Windows spelling `cygpath -m` produces, `C:/Users/BARSEM~1/...` , which is the form the QA host's python3 can open |
| `$QA_PY` | the QA host's `python3` absolute path. It contains a non-ASCII user-directory component, so it is NOT reproduced here; this file is required to be ASCII. It is used only as a repointed value of the delivered `PYTHON_BIN` literal, and every arm that uses it is counted in category B. |

## 1. Environment

```
$ bash --version | head -1
GNU bash, version 5.2.37(1)-release (x86_64-pc-msys)
$ python3 --version
Python 3.13.14
$ uname -a
MINGW64_NT-10.0-26200 DESKTOP-K223CHV 3.6.5-22c95533.x86_64 2025-10-10 12:02 UTC x86_64 Msys
$ env --version | head -1
env (GNU coreutils) 8.32
$ command -v shellcheck
(not installed - shellcheck was NOT run; see section 8)
$ ls /usr/bin/python3
ls: cannot access '/usr/bin/python3': No such file or directory
```

The last line matters twice. It is why the delivered `PYTHON_BIN` literal has to
be repointed for the functional manifest arms, and it is also why the
`manifest_tool_absent` STOP could be driven for real, with no substitution at all
(arm `I1-GREEN-pin-absent`).

## 2. `bash -n`, encoding and deliverable-set evidence

```
$ cd round3
$ bash -n RP1-B3.sh    ; echo "rc=$?"
rc=0
$ bash -n RPD-VERIFY.sh; echo "rc=$?"
rc=0
$ iconv -f ASCII -t ASCII <RP1-B3.sh     >/dev/null && echo ASCII_OK
ASCII_OK
$ iconv -f ASCII -t ASCII <RPD-VERIFY.sh >/dev/null && echo ASCII_OK
ASCII_OK
$ LC_ALL=C grep -c $'\r' RP1-B3.sh RPD-VERIFY.sh
RP1-B3.sh:0
RPD-VERIFY.sh:0
$ sha256sum RP1-B3.sh RPD-VERIFY.sh
e561e8b4cf5444bebf2293046a3ea649712d3b229bd380e1c69364ab552397dd *RP1-B3.sh
f4c5d61de7e55bd7f2fc9f6a73754a093cb114b1c8316b85a683a78f833e63a2 *RPD-VERIFY.sh
$ wc -l RP1-B3.sh RPD-VERIFY.sh
  637 RP1-B3.sh
  750 RPD-VERIFY.sh
```

Re-run after the final edit of each file; both still rc=0, and the two hashes
above are the hashes of the bytes every arm below was extracted from.

A2-F8: the deliverable set is exactly four files. `find round3 -mindepth 1` was
checked after the last write and lists only `DESIGN_NOTES.md`, `RP1-B3.sh`,
`RPD-VERIFY.sh` and `SELF_QA.md` - no dot-directory, no cache, no editor or tool
artifact. Nothing in this round created one.

## 3. Method, and the three exact counts (A2-F7)

Every arm is driven against DELIVERED BYTES. No predicate is retyped: each
function is extracted mechanically from the delivered file and `eval`ed under
`set -Eeuo pipefail` together with the delivered `..._stop`, `..._fail`,
`..._on_err` + `ERR` trap and `..._sanitize`.

```
exfn() { awk -v fn="$2" 'index($0, fn "() {")==1 {f=1} f{print} f && /^\}$/{exit}' "$1"; }
ex1()  { LC_ALL=C grep -m1 "^$2() {" "$1"; }   # one-line definitions
exc()  { LC_ALL=C grep -m1 "^$2="    "$1"; }   # constants
```

The four preludes, used verbatim throughout:

```
pre3b() {   # round-3 RP1-B3
    printf 'set -Eeuo pipefail\nexport LC_ALL=C\nB3_KIND=""\nB3_SAFE=""\nB3_COUNT=0\nB3_SHAPE=""\n'
    ex1 "$R3/RP1-B3.sh" b3_stop; ex1 "$R3/RP1-B3.sh" b3_fail
    exfn "$R3/RP1-B3.sh" b3_on_err; printf "trap 'b3_on_err' ERR\n"
    exfn "$R3/RP1-B3.sh" b3_sanitize
}
pre3r() {   # round-3 RPD-VERIFY
    printf 'set -Eeuo pipefail\nexport LC_ALL=C\nunset CDPATH\nRPD_KIND=""\nRPD_SAFE=""\n'
    ex1 "$R3/RPD-VERIFY.sh" rpd_stop; ex1 "$R3/RPD-VERIFY.sh" rpd_fail
    exfn "$R3/RPD-VERIFY.sh" rpd_on_err; printf "trap 'rpd_on_err' ERR\n"
    exfn "$R3/RPD-VERIFY.sh" rpd_sanitize
}
pre2b() / pre2r()   # identical, with $R2 in place of $R3, for every RED baseline
```

### The three counts

Counted by the audit's own rule: **category B is any arm with a stubbed command
OR a repointed path literal**, with no exceptions - including both mount
sections, which the audit named specifically.

| Category | Count |
|---|---:|
| A. Delivered-code arms run with NO stubbed command and NO repointed literal | **43** |
| B. Delivered-code arms run with at least one stubbed command or repointed path literal | **115** |
| C. Inherited RP0-LIB arms NOT re-run (not driven, not claimed as driven) | **3** |

Per file: `RP1-B3.sh` = **21 A / 62 B** (83 runs). `RPD-VERIFY.sh` =
**22 A / 53 B** (75 runs). Total driven: **158 runs**, 158 matched the designed
outcome after the one delivered-code defect in section 3.1 was fixed,
**0 remaining mismatches**.

Reported separately, because they are ROUND-2 code and belong in no round-3
category: **25 RED baseline runs** against `round2/`, listed in section 5.

Category C in full, so it is not a vague remainder: the three internal paths of
`rp0_monotonic_ms` (RP0-LIB:18-22) - its success path, its `/proc/uptime`
unreadable STOP, and an `awk` failure. `RP1-B3` reaches them only through
`t0="$(rp0_monotonic_ms)" || b3_stop "monotonic_clock_unevaluable"`, and that
adjudication IS driven (arms `W6`, `W7`) with a stub; the library function's own
three paths were not re-run here and are not claimed as driven. `RPD-VERIFY.sh`
calls no library function at all, so it inherits nothing.

### Arms NOT driven at all - excluded from every count above

1. `conf_dir_read_permitted` (RP1-B3, `-x` false and `-r` true). MSYS cannot
   produce a directory with that permission shape.
2. `manifest_tool_not_executable` (RPD-VERIFY). MSYS reports `[ -x ]` TRUE for a
   mode-0644 regular file, so the arm cannot be reached here. Verified by
   inspection only.
3. `open_kind_not_regular` (RPD-VERIFY reader) - needs a non-regular object that
   `open` succeeds on.
4. A `read_error` raised mid-read rather than at open (RPD-VERIFY reader).

### 3.1 One delivered-code defect found by this QA, and fixed

`rpd_require_ns_token` was first written with `pfx="$kind:["` inside the same
`local` declaration that introduces `kind`. Bash expands every word of a `local`
command before assigning any of them, so the function aborted under `set -u`:

```
$ bash arm.sh
arm.sh: line 25: kind: unbound variable
RC=1
```

That is a raw exit with no reason string and rc 1 - the code this contract
reserves for "the host is deviant" - i.e. exactly the failure class F6/O5 exists
to prevent. Fixed by hoisting `pfx` onto its own line, with a comment in the file
saying why the two lines are not folded. Every other `local` declaration in both
blocks was then audited for the same pattern (`grep -n '^ *local .*=.*\$'`); there
are no others. The re-run is arm `I2-G1` in section 5.2.

### 3.2 Harness defects, disclosed rather than hidden

1. A first attempt at the missing-attestation-input arms used
   `env -u VAR ... VAR=value`, which re-set the variable it had just removed; the
   runs reached `must_run_as_root` instead of the intended guard. Rebuilt with an
   explicit `unset` inside the subshell. The defective runs are not counted.
2. The `rp0_monotonic_ms` stub used `$STUB_CLOCK` unquoted under `set -u`, so
   arms `W1`-`W4` first drove `monotonic_clock_unevaluable` instead of their
   intended arms. Rebuilt with `${STUB_CLOCK:-}`. The defective runs are not
   counted; the rebuilt runs are in section 6.5.

## 4. QA substitutions, in full

Only these four kinds are used, and every arm that uses one is category B.

1. **`/proc/self/uid_map`** is a literal in the delivered attestation function and
   does not exist on MSYS. For the `I2-GREEN-*` arms the extracted function body
   had exactly that one literal replaced with a fixture path by a single `sed`
   substitution; every other byte is delivered.
2. **`MOUNTS`** is repointed to a fixture file for every mount arm (both blocks).
   The function bodies are delivered bytes.
3. **`PYTHON_BIN`** is repointed to `$QA_PY` for the functional manifest arms, and
   `rpd_require_pinned_tool` is replaced by a one-line stub in those arms only,
   because the QA host cannot present a `0:0`-owned interpreter. The pinned-tool
   predicate itself is driven separately, unsubstituted, in section 5.1.
4. **Stubbed producers** (`stat`, `readlink`, `id`, `find`, and a stub interpreter)
   on a PATH-prepended directory, for arms whose outcome depends on a value the QA
   host cannot produce.

Two QA-host facts shape the manifest arms and are stated so no reader mistakes
them for delivered behaviour: the QA `python3` renders POSIX metadata as mode
`0666`, uid `0`, gid `0`, so those arms pass `0666` where the deploy-time call
passes `0640`; and it opens Windows-form paths, so fixture paths are given as
`$QAW/...`.

## 5. D026 closure evidence: exact command, real RED, real GREEN

For every audit-2 item 1-6. RED is the ROUND-2 delivered code; GREEN is the
ROUND-3 delivered code; both were run on this host in this round, against the same
fixture, in the same shell session.

### 5.1 Item 1 (A2-F1) - interpreter isolation

Fixtures: `$QA/fix1/wrong.json` contains exactly
`THIS IS NOT JSON AND BINDS NOTHING`; `$QA/fix1/shadow/json.py` and
`$QA/fix1/cwdshadow/json.py` are

```python
def loads(*a, **k):
    return {"release_sha": "2ce41e34bceb599d80af24c5c33d835820ec321b",
            "release_manifest_sha256": "edb0fd34e3d976b872868cc3dfbf745cbc4b08f6c4c5d21b8d6cda47a3e20d26"}
```

**Command (RED)** - round-2 prelude plus the round-2 function, nothing else:

```
{ pre2r; exfn "$R2/RPD-VERIFY.sh" rpd_assert_manifest_binding
  printf 'rpd_assert_manifest_binding "%s" "%s" "%s" 0666\n' \
      "$QAW/fix1/wrong.json" "$GOODREL" "$GOODMAN"; } >arm.sh
PYTHONPATH="$QAW/fix1/shadow" bash arm.sh
```

```
RPD_manifest_binding path=$QAW/fix1/wrong.json bound=both parser=python3_json_structural keys=top_level_exact
RC=0
```

**Command (GREEN)** - identical, with `$R3` in place of `$R2` and `PYTHON_BIN`
repointed to `$QA_PY`:

```
RPD_tool name=env path=/usr/bin/env mode=755 owner_numeric=0:0 resolution=pinned_absolute
RPD_tool name=python3 path=$QA_PY mode=755 owner_numeric=0:0 resolution=pinned_absolute
RPD_STOP reason=install_manifest_unparsable path=$QAW/fix1/wrong.json
RC=3
```

**Command (RED, cwd variant)** - same arm script, executed from the poisoned
directory:

```
cp arm.sh "$QA/fix1/cwdshadow/arm.sh"
( cd "$QA/fix1/cwdshadow" && bash ./arm.sh )
```

```
RPD_manifest_binding path=$QAW/fix1/wrong.json bound=both parser=python3_json_structural keys=top_level_exact
RC=0
```

**GREEN, cwd variant** - same command, round-3 arm script:

```
RPD_tool name=env path=/usr/bin/env mode=755 owner_numeric=0:0 resolution=pinned_absolute
RPD_tool name=python3 path=$QA_PY mode=755 owner_numeric=0:0 resolution=pinned_absolute
RPD_STOP reason=install_manifest_unparsable path=$QAW/fix1/wrong.json
RC=3
```

Both hijack shapes are closed, and the GREEN result is the truth about the file:
it is not JSON.

**The pinned-tool predicate itself, unsubstituted.** These use the delivered
literals `PYTHON_BIN=/usr/bin/python3` and `ENV_BIN=/usr/bin/env` and the
delivered `rpd_require_pinned_tool`; no stub, no repointed value (category A):

```
{ pre3r; exfn "$R3/RPD-VERIFY.sh" rpd_probe_kind; exc "$R3/RPD-VERIFY.sh" ROOT_OWNER
  exc "$R3/RPD-VERIFY.sh" PYTHON_BIN; exc "$R3/RPD-VERIFY.sh" ENV_BIN
  exfn "$R3/RPD-VERIFY.sh" rpd_require_pinned_tool
  printf 'rpd_require_pinned_tool python3 "$PYTHON_BIN"\n'; } >arm.sh
bash arm.sh
```

```
RPD_STOP reason=manifest_tool_absent name=python3 path=/usr/bin/python3 detail=pinned absolute interpreter toolchain is required and has no PATH fallback
RC=3
```

```
... printf 'rpd_require_pinned_tool env "$ENV_BIN"\n' ...
RPD_STOP reason=manifest_tool_not_root_owned name=env path=/usr/bin/env owner_numeric=4096:4096 expected=0:0
RC=3
```

Round 2 has no counterpart to either arm: it ran `command -v python3` and would
have used whatever PATH returned. The remaining pinned-tool arms (kind, mode 755
pass, 757 other-writable, 775 group-writable) are in section 6.10.

### 5.2 Item 2 (A2-F2) - deploy-channel attestation

Fixture: `uid_map_identity` contains `0 0 4294967295`. The stub `readlink`
answers `/proc/self/ns/*` and `/proc/1/ns/*` from environment variables, so the
rootful-container case can be presented exactly as the audit describes it: self
namespaces equal to VISIBLE pid 1's, identity uid map, but not the host's.

**Command (RED)**:

```
{ pre2r; exfn "$R2/RPD-VERIFY.sh" rpd_assert_initial_namespaces \
    | sed "s|/proc/self/uid_map|$QA/fix2/uid_map_identity|"
  printf 'rpd_assert_initial_namespaces\n'; } >arm.sh
PATH="$QA/fix2/stub:$PATH" \
  STUB_SELF_U='user:[4026999991]' STUB_SELF_M='mnt:[4026999992]' \
  STUB_INIT_U='user:[4026999991]' STUB_INIT_M='mnt:[4026999992]' bash arm.sh
```

```
RPD_namespace user=user:[4026999991] mnt=mnt:[4026999992] bound=initial uid_map=identity
RC=0
```

That is the overclaim: `bound=initial` printed for a namespace pair that is not
the host's.

**Command (GREEN)** - same container, attested host values supplied:

```
{ pre3r; exfn "$R3/RPD-VERIFY.sh" rpd_assert_attested_namespaces \
    | sed "s|/proc/self/uid_map|$QA/fix2/uid_map_identity|"
  exc "$R3/RPD-VERIFY.sh" ROOTFS; printf 'rpd_assert_attested_namespaces\n'; } >arm.sh
PATH="$QA/fix2/stub:$PATH" \
  STUB_SELF_U='user:[4026999991]' STUB_SELF_M='mnt:[4026999992]' STUB_ROOTFS='2049:2' \
  RPD_EXPECT_NS_USER='user:[4026531837]' RPD_EXPECT_NS_MNT='mnt:[4026531840]' \
  RPD_EXPECT_ROOTFS_ID='2049:2' bash arm.sh
```

```
RPD_STOP reason=namespace_not_attested ns=user self=user:[4026999991] attested=user:[4026531837]
RC=3
```

Same arm, self equal to every attested value:

```
RPD_namespace user=user:[4026531837] mnt=mnt:[4026531840] rootfs=2049:2 bound=attested source=deploy_channel_preregistration uid_map=identity
RC=0
```

Same arm, user namespace matching and mount namespace not:

```
RPD_STOP reason=namespace_not_attested ns=mnt self=mnt:[4026999992] attested=mnt:[4026531840]
RC=3
```

Same arm, both namespaces matching and `/` a different filesystem object - the
chroot / bind-over-root case the namespace tokens alone cannot see:

```
RPD_STOP reason=rootfs_not_attested path=/ self=64768:9999 attested=2049:2
RC=3
```

Same arm, rootless uid map `0 1000 1` - the round-2 predicate, kept:

```
RPD_STOP reason=user_namespace_not_initial reason=uid_map_not_identity map=[0 1000 1]
RC=3
```

Input guards, delivered functions, no stub and no repointed literal (category A):

| Arm | Command tail | Output | Rc |
|---|---|---|---:|
| I2-G1 | `rpd_require_ns_token RPD_EXPECT_NS_USER "user:[4026531837]" user` | `RPD_input name=RPD_EXPECT_NS_USER value=user:[4026531837]` | 0 |
| I2-G2 | `rpd_require_ns_token RPD_EXPECT_NS_MNT "4026531840" mnt` | `RPD_STOP reason=input_shape name=RPD_EXPECT_NS_MNT expected=mnt:[<decimal_inode>]` | 3 |
| I2-G3 | `rpd_require_ns_token RPD_EXPECT_NS_USER "user:[40265abc]" user` | `RPD_STOP reason=input_charset name=RPD_EXPECT_NS_USER expected=decimal_inode` | 3 |
| I2-G4 | `rpd_require_ns_token RPD_EXPECT_NS_MNT "user:[4026531840]" mnt` | `RPD_STOP reason=input_shape name=RPD_EXPECT_NS_MNT expected=mnt:[<decimal_inode>]` | 3 |
| I2-G8 | `rpd_require_ns_token RPD_EXPECT_NS_USER "user:[]" user` | `RPD_STOP reason=input_shape name=RPD_EXPECT_NS_USER expected=user:[<decimal_inode>] detail=empty_inode` | 3 |
| I2-G5 | `rpd_require_devino RPD_EXPECT_ROOTFS_ID "2049:2"` | `RPD_input name=RPD_EXPECT_ROOTFS_ID value=2049:2` | 0 |
| I2-G6 | `rpd_require_devino RPD_EXPECT_ROOTFS_ID "2049:2:3"` | `RPD_STOP reason=input_shape name=RPD_EXPECT_ROOTFS_ID expected=<decimal_dev>:<decimal_inode>` | 3 |
| I2-G7 | `rpd_require_devino RPD_EXPECT_ROOTFS_ID "dev:2"` | `RPD_STOP reason=input_charset name=RPD_EXPECT_ROOTFS_ID expected=decimal_dev_and_inode` | 3 |

Missing-input STOPs, delivered file executed as a file (category A). Command:

```
( cd round3
  export RPD_CANDIDATE_SHA=2ce41e34bceb599d80af24c5c33d835820ec321b
  export RPD_RELEASE_MANIFEST_SHA256=edb0fd34e3d976b872868cc3dfbf745cbc4b08f6c4c5d21b8d6cda47a3e20d26
  export RPD_EXPECT_NS_USER='user:[4026531837]' RPD_EXPECT_NS_MNT='mnt:[4026531840]' RPD_EXPECT_ROOTFS_ID=2049:2
  unset RPD_EXPECT_NS_USER      # then NS_MNT, then ROOTFS_ID
  bash RPD-VERIFY.sh )
```

```
RPD_STOP reason=input_missing name=RPD_EXPECT_NS_USER detail=deploy-channel attested host user namespace token, exact readlink form user:[<inode>], never derived here
RC=3
RPD_STOP reason=input_missing name=RPD_EXPECT_NS_MNT detail=deploy-channel attested host mount namespace token, exact readlink form mnt:[<inode>], never derived here
RC=3
RPD_STOP reason=input_missing name=RPD_EXPECT_ROOTFS_ID detail=deploy-channel attested host root filesystem identity, exact stat -c %d:%i form, never derived here
RC=3
```

### 5.3 Item 3 (A2-F3) - numeric service uid/gid

The audit's exact scenario: the accepted account has some preregistered nonzero
pair, the host presents `999:999`, and NSS renders `999:999` as
`mtc-bridge:mtc-bridge`.

**Command (RED)**:

```
{ pre2b; exfn "$R2/RP1-B3.sh" b3_probe_kind; exfn "$R2/RP1-B3.sh" b3_assert_mode_owner
  printf 'b3_assert_mode_owner /var/lib/mtc-bridge 0750 mtc-bridge:mtc-bridge\n'; } >arm.sh
PATH="$QA/fix3/stub:$PATH" bash arm.sh      # stub stat: %F=directory %a=750 %u:%g=999:999 %U:%G=mtc-bridge:mtc-bridge
```

```
B3_stat path=/var/lib/mtc-bridge owner_numeric=999:999 owner_name=mtc-bridge:mtc-bridge mode=750
RC=0
```

**Command (GREEN)** - identical stub, round-3 function, expectation built from the
preregistered pair `B3_SVC_UID=1500 B3_SVC_GID=1500`:

```
{ pre3b; exfn "$R3/RP1-B3.sh" b3_probe_kind; exfn "$R3/RP1-B3.sh" b3_assert_mode_owner
  printf 'b3_assert_mode_owner /var/lib/mtc-bridge 0750 1500:1500\n'; } >arm.sh
PATH="$QA/fix3/stub:$PATH" bash arm.sh
```

```
B3_stat path=/var/lib/mtc-bridge owner_numeric=999:999 owner_name=mtc-bridge:mtc-bridge mode=750
B3_FAIL reason=path=/var/lib/mtc-bridge owner_numeric=999:999 expected=1500:1500 owner_name=mtc-bridge:mtc-bridge
RC=1
```

Same stub, preregistered pair really is `999:999` - the admission still passes,
so this is a discriminating check and not a blanket rejection:

```
B3_stat path=/var/lib/mtc-bridge owner_numeric=999:999 owner_name=mtc-bridge:mtc-bridge mode=750
RC=0
```

A NAME passed where the numeric pair belongs (a coding error in the block):

```
B3_STOP reason=owner_expectation_malformed path=/var/lib/mtc-bridge expected=[mtc-bridge:mtc-bridge] shape=<uid>:<gid>
RC=3
```

No weakening of the one case round 2 did catch - uid 0 rendered as the service
name. Round 2:

```
B3_FAIL reason=path=/var/lib/mtc-bridge owner_numeric=0:999 expected=nonzero_service_account name=mtc-bridge:mtc-bridge
RC=1
```

Round 3, same fixture:

```
B3_FAIL reason=path=/var/lib/mtc-bridge owner_numeric=0:999 expected=1500:1500 owner_name=mtc-bridge:mtc-bridge
RC=1
```

Input guards, delivered file executed as a file (category A), command
`( cd round3 && env B3_SWEEP_BUDGET_S=120 <input under test> bash RP1-B3.sh )`:

```
B3_STOP reason=input_missing name=B3_SVC_UID detail=preregistered numeric uid of the mtc-bridge service account, never derived here          RC=3
B3_STOP reason=input_charset name=B3_SVC_UID expected=decimal_digits                                                                          RC=3
B3_STOP reason=input_range name=B3_SVC_UID value=0 expected=nonzero_service_account_uid                                                       RC=3
B3_STOP reason=input_missing name=B3_SVC_GID detail=preregistered numeric gid of the mtc-bridge service account, never derived here          RC=3
B3_STOP reason=input_range name=B3_SVC_GID value=0 expected=nonzero_service_account_gid                                                       RC=3
```

### 5.4 Item 4 (A2-F4) - NaN, Infinity, -Infinity

Fixtures: `{"release_sha": "<good>", "release_manifest_sha256": "<good>",
"extra": NaN}` and the same with `Infinity` and `-Infinity`. Both bindings are
CORRECT in all three, so the only thing under test is the constant.

**Command**: the section 5.1 manifest arm with the fixture swapped.

| Fixture | RED (round-2 code) | Rc | GREEN (round-3 code) | Rc |
|---|---|---:|---|---:|
| `nan.json` | `RPD_manifest_binding path=$QAW/fix1/nan.json bound=both parser=python3_json_structural keys=top_level_exact` | 0 | `RPD_STOP reason=install_manifest_non_json_constant path=$QAW/fix1/nan.json detail=NaN_Infinity_-Infinity_are_not_JSON_values` | 3 |
| `inf.json` | `RPD_manifest_binding path=$QAW/fix1/inf.json bound=both parser=python3_json_structural keys=top_level_exact` | 0 | `RPD_STOP reason=install_manifest_non_json_constant path=$QAW/fix1/inf.json detail=NaN_Infinity_-Infinity_are_not_JSON_values` | 3 |
| `neginf.json` | `RPD_manifest_binding path=$QAW/fix1/neginf.json bound=both parser=python3_json_structural keys=top_level_exact` | 0 | `RPD_STOP reason=install_manifest_non_json_constant path=$QAW/fix1/neginf.json detail=NaN_Infinity_-Infinity_are_not_JSON_values` | 3 |

(The two `RPD_tool` lines precede every GREEN line above and are omitted from this
table only; they are shown in full in section 5.1.)

### 5.5 Item 5 (A2-F5) - the mount readers, both blocks

Fixture `nonl` is the audit's own: the single record
`src /etc/mtc-bridge ext4 rw 0 0` with NO terminating newline. Fixture `short`
ends with the truncated record `src /etc/mtc-bri`. Fixture `wide` carries a
7-field record.

**Command** (shown for RPD; the B3 form differs only in the prelude, the file and
the function name):

```
{ pre2r; printf 'MOUNTS=%s\n' "$QA/fix2/mounts/nonl"
  exfn "$R2/RPD-VERIFY.sh" rpd_assert_no_mount_at_or_under
  printf 'rpd_assert_no_mount_at_or_under /etc/mtc-bridge\n'; } >arm.sh
bash arm.sh
```

| Arm | RED (round-2 code) | Rc | GREEN (round-3 code) | Rc |
|---|---|---:|---|---:|
| RPD, `nonl` | `RPD_conf_dir_no_mount_boundary path=/etc/mtc-bridge source=$QA/fix2/mounts/nonl` | **0** | `RPD_STOP reason=mount_table_unterminated_final_record path=$QA/fix2/mounts/nonl records=1 hits=1 first_target=/etc/mtc-bridge` | **3** |
| B3, `nonl` | `B3_conf_dir_no_mount_boundary path=/etc/mtc-bridge source=$QA/fix2/mounts/nonl` | **0** | `B3_STOP reason=mount_table_unterminated_final_record path=$QA/fix2/mounts/nonl records=1 hits=1 first_target=/etc/mtc-bridge` | **3** |
| RPD, `short` | `RPD_conf_dir_no_mount_boundary path=/etc/mtc-bridge source=$QA/fix2/mounts/short` | **0** | `RPD_STOP reason=mount_record_malformed path=$QA/fix2/mounts/short record=2 expected_fields=6 got=[src /etc/mtc-bri     ]` | **3** |
| B3, `short` | `B3_conf_dir_no_mount_boundary path=/etc/mtc-bridge source=$QA/fix2/mounts/short` | **0** | `B3_STOP reason=mount_record_malformed path=$QA/fix2/mounts/short record=2 expected_fields=6 got=[src /etc/mtc-bri     ]` | **3** |
| RPD, `wide` | `RPD_STOP reason=mount_boundary_at_or_under_conf_dir path=/etc/mtc-bridge mounts=1 first_target=/etc/mtc-bridge` | 3 | `RPD_STOP reason=mount_record_malformed path=$QA/fix2/mounts/wide record=2 expected_fields=6 got=[src /etc/mtc-bridge ext4 rw 0 0 extra]` | 3 |
| B3, `wide` | `B3_STOP reason=mount_boundary_at_or_under_conf_dir path=/etc/mtc-bridge mounts=1 first_target=/etc/mtc-bridge` | 3 | `B3_STOP reason=mount_record_malformed path=$QA/fix2/mounts/wide record=2 expected_fields=6 got=[src /etc/mtc-bridge ext4 rw 0 0 extra]` | 3 |

The first four rows are the closure: the exact false rc-0 the audit reported,
against the exact fixture, now rc 3 in both blocks. The `wide` rows are stated
honestly as an ADDED validation, not a closure: round 2 already STOPped there, for
a different reason.

No weakening, round-3 code, same functions (section 6.9 has the full table):
a clean table returns `records=3` rc 0; a sibling name `/etc/mtc-bridgeX` does not
match; a mount AT and a mount UNDER the directory both STOP with the round-2
reason string; an unreadable source STOPs.

### 5.6 Item 6 (A2-F6) - boundary diagnostics

Stubbed `stat` producing each diagnostic shape on stderr with rc 1. `twoline` is
the audit's fixture: an EACCES line and an ENOENT line.

**Command**:

```
{ pre2b; exfn "$R2/RP1-B3.sh" b3_assert_conf_dir_opaque
  printf 'b3_assert_conf_dir_opaque /etc/mtc-bridge/mtc-bridge.env\n'; } >arm.sh
PATH="$QA/fix3/stubdir:$PATH" STUB_CASE=twoline bash arm.sh
```

and for GREEN the round-3 prelude plus `B3_EACCES_TEXT`, `B3_ENOENT_TEXT`,
`b3_count_substr`, `b3_classify_boundary_shape` and the round-3
`b3_assert_conf_dir_opaque`.

| Case | RED (round-2 code) | Rc | GREEN (round-3 code) | Rc |
|---|---|---:|---|---:|
| `twoline` EACCES line + ENOENT line | `B3_conf_dir_opaque_to_operator path=... outcome=EACCES rc=1 mechanism=message_lc_all_c` | **0** | `B3_STOP reason=boundary_diagnostic_multiline path=... rc=1 detail=stat: cannot stat '...': Permission denied stat: cannot stat '...': No such file or directory` | **3** |
| `oneline2` one line naming both classes | `B3_conf_dir_opaque_to_operator ... outcome=EACCES rc=1 mechanism=message_lc_all_c` | **0** | `B3_STOP reason=boundary_diagnostic_ambiguous path=... rc=1 classes=2 eacces=1 enoent=1 detail=stat: cannot stat '...': Permission denied (No such file or directory)` | **3** |
| `wrapper` `mtcwrap: stat failed on <p>: Permission denied` | `B3_conf_dir_opaque_to_operator ... outcome=EACCES rc=1 mechanism=message_lc_all_c` | **0** | `B3_STOP reason=boundary_probe_unclassified path=... rc=1 detail=mtcwrap: stat failed on /etc/mtc-bridge/mtc-bridge.env: Permission denied` | **3** |
| `wrongpath` EACCES naming a DIFFERENT path | `B3_conf_dir_opaque_to_operator ... outcome=EACCES rc=1 mechanism=message_lc_all_c` | **0** | `B3_STOP reason=boundary_probe_unclassified path=... rc=1 detail=stat: cannot stat '/some/other/path': Permission denied` | **3** |
| `eacces` exact `stat: cannot stat '<p>': Permission denied` | `B3_conf_dir_opaque_to_operator ... mechanism=message_lc_all_c` | 0 | `B3_conf_dir_opaque_to_operator path=... outcome=EACCES rc=1 mechanism=message_lc_all_c_exact_shape` | 0 |
| `statx` exact `stat: cannot statx '<p>': Permission denied` | `B3_conf_dir_opaque_to_operator ... mechanism=message_lc_all_c` | 0 | `B3_conf_dir_opaque_to_operator path=... outcome=EACCES rc=1 mechanism=message_lc_all_c_exact_shape` | 0 |
| `enoent` exact ENOENT shape | `B3_FAIL reason=conf_dir_search_permitted_name_absent path=... rc=1 expected=EACCES` | 1 | identical | 1 |
| `eio` | `B3_STOP reason=boundary_probe_unclassified ... detail=stat: cannot stat '...': Input/output error` | 3 | identical | 3 |
| `empty` rc 4, no stderr | `B3_STOP reason=boundary_probe_unclassified path=... rc=4 detail=` | 3 | identical | 3 |
| `nonprint` EACCES plus a BEL byte | `B3_STOP reason=boundary_probe_unclassified ... detail=[non_printable_detail_suppressed]` | 3 | identical | 3 |
| `ok` stat SUCCEEDS | `B3_FAIL reason=conf_dir_entry_permitted path=... stat=[regular file\|600\|0:0] expected=EACCES` | 1 | identical | 1 |

Four false rc-0 arms closed; the four PASS/FAIL arms that were already correct are
byte-identical or differ only in the `mechanism=` field, so nothing was weakened.

**The exact-shape rule driven against REAL coreutils, no stub at all**
(category A): the round-3 function probing a genuinely absent name, so the real
`stat` emits the real C-locale ENOENT diagnostic:

```
{ pre3b; exc "$R3/RP1-B3.sh" B3_EACCES_TEXT; exc "$R3/RP1-B3.sh" B3_ENOENT_TEXT
  exfn "$R3/RP1-B3.sh" b3_count_substr; exfn "$R3/RP1-B3.sh" b3_classify_boundary_shape
  exfn "$R3/RP1-B3.sh" b3_assert_conf_dir_opaque
  printf 'b3_assert_conf_dir_opaque %s/no-such-name\n' "$QA/fix3"; } >arm.sh
bash arm.sh
```

```
B3_FAIL reason=conf_dir_search_permitted_name_absent path=$QA/fix3/no-such-name rc=1 expected=EACCES
RC=1
```

This is the arm that shows the exact-shape templates match a real GNU coreutils
8.32 diagnostic and are not a construction that only the stubs satisfy.

## 6. Full round-3 arm walk

`[A]` = no stubbed command and no repointed literal. `[B]` = at least one of
either.

### 6.1 `RP1-B3.sh`, delivered file executed as a file `[A]` (5)

| Arm | Command | Output | Rc |
|---|---|---|---:|
| R1 | `env -u B3_SWEEP_BUDGET_S B3_SVC_UID=1500 B3_SVC_GID=1500 bash RP1-B3.sh` | `B3_STOP reason=input_missing name=B3_SWEEP_BUDGET_S detail=preregistered per-tree sweep budget in seconds, positive integer, never derived here` | 3 |
| R2 | `B3_SWEEP_BUDGET_S=abc ...` | `B3_STOP reason=input_charset name=B3_SWEEP_BUDGET_S expected=decimal_digits` | 3 |
| R3 | `B3_SWEEP_BUDGET_S=0 ...` | `B3_STOP reason=input_range name=B3_SWEEP_BUDGET_S value=0 expected=positive_integer` | 3 |
| R4 | all three inputs, RP0-LIB not sourced | `B3_STOP reason=rp0_lib_not_sourced predicate=rp0_monotonic_ms` | 3 |
| R5 | `. RP0-LIB.sh; . RP1-B3.sh` end to end | `B3_SECTION header candidate=2ce41e34...321b` / `B3_identity uid=4096 gids=[4096]` / `B3_STOP reason=namespace_unreadable ns=user path=/proc/self/ns/user` | 3 |

R5 stops at the namespace disclosure because MSYS has no `/proc/self/ns` at all;
on Linux this line records the two identities and continues.

### 6.2 `RP1-B3.sh` input guards for the NEW inputs `[A]` (5)

The five runs in section 5.3, all rc 3.

### 6.3 `b3_sanitize` and `b3_count_substr` `[A]` (7)

| Arm | Input | Result |
|---|---|---|
| S1 | `a<LF>b` | `[a b]` |
| S2 | `x<BEL>y` | `[[non_printable_detail_suppressed]]` |
| S3 | 500 `a` bytes | `len=400` |
| CS1 | needle absent | `CS1=0` |
| CS2 | one occurrence | `CS2=1` |
| CS3 | two occurrences | `CS3=2` |
| CS4 | one ENOENT phrase | `CS4=1` |

CS3 is the arm the ambiguity rule rests on: two occurrences of the same class on
one line are counted, not collapsed.

### 6.4 `b3_probe_kind`, stubbed `stat` `[B]` (10)

`PK-b3-1` regular file -> `kind=regular` rc 0; `PK-b3-2` regular empty file ->
`kind=regular` rc 0; `PK-b3-3` directory -> `kind=dir` rc 0; `PK-b3-4` fifo ->
`kind=other` rc 0; `PK-b3-5` symlink + live target -> `kind=link_live` rc 0;
`PK-b3-6` symlink + ENOENT target -> `kind=link_dangling` rc 0; `PK-b3-7` symlink
+ EIO target -> `B3_STOP reason=link_target_probe_error path=/p rc=1 detail=stat:
cannot stat '/p': Input/output error` rc 3; `PK-b3-8` rc 1 ENOENT -> `kind=absent`
rc 0; `PK-b3-9` rc 1 EACCES -> `B3_STOP reason=path_probe_error path=/p rc=1
detail=stat: cannot stat '/p': Permission denied` rc 3; `PK-b3-10` rc 0 with empty
output -> `B3_STOP reason=path_probe_empty path=/p rc=0` rc 3.

### 6.5 `b3_assert_mode_owner` and the sweep, stubbed `[B]` (7 + 7)

| Arm | Scenario | Output | Rc |
|---|---|---|---:|
| M1 | `0555 0:0` expected, matches | `B3_stat path=/p owner_numeric=0:0 owner_name=root:root mode=555` | 0 |
| M2 | uid 1000 rendered as `root:root` | `B3_FAIL reason=path=/p owner_numeric=1000:1000 expected=0:0 owner_name=root:root` | 1 |
| M3 | mode drift | `B3_FAIL reason=path=/p mode=755 expected=555` | 1 |
| M4 | path absent | `B3_FAIL reason=missing path=/p` | 1 |
| M5 | symlink at a canonical path | `B3_FAIL reason=canonical deployment path is a symlink kind=link_live path=/p` | 1 |
| M6 | socket/fifo/device | `B3_FAIL reason=unexpected object kind=other path=/p` | 1 |
| M7 | `stat %a` fails | `B3_STOP reason=mode_probe_failed path=/p` | 3 |
| W1 | clean tree | `B3_sweep root=/opt/tree elapsed_s=0 budget_s=120` / `B3_no_write_bit root=/opt/tree` | 0 |
| W2 | offender found | `B3_FAIL reason=writable path inside immutable tree: /opt/tree/bad` | 1 |
| W3 | `find` rc 1 with stderr | `B3_STOP reason=writable_inventory_failed root=/opt/tree rc=1 detail=/opt/tree/x find: permission denied` | 3 |
| W4 | rc 0, output not under root | `B3_STOP reason=writable_inventory_unparsable root=/opt/tree rc=0 out=surprise-not-a-path` | 3 |
| W5 | elapsed 200s over a 120s budget | `B3_sweep root=/opt/tree elapsed_s=200 budget_s=120` / `B3_STOP reason=sweep_budget_exceeded root=/opt/tree elapsed_s=200 budget_s=120` | 3 |
| W6 | clock predicate returns 3 | `B3_STOP reason=monotonic_clock_unevaluable root=/opt/tree phase=start` | 3 |
| W7 | clock predicate returns non-numeric | `B3_STOP reason=monotonic_clock_unparsable root=/opt/tree t0=[notanumber] t1=[notanumber]` | 3 |

Section 5.3 adds four more `b3_assert_mode_owner` arms (the A2-F3 pair, the
matching pair, the malformed expectation, and the uid-0 case), counted in `[B]`.

### 6.6 Identity, namespaces, group, canonical path, stubbed `[B]` (4+3+4+4)

| Arm | Scenario | Output | Rc |
|---|---|---|---:|
| I1 | uid 1000 | `B3_identity uid=1000 gids=[1000 4 27]` | 0 |
| I2 | uid 0 | `B3_STOP reason=must_run_unprivileged uid=0` | 3 |
| I3 | `id -u` fails | `B3_STOP reason=uid_probe_failed` | 3 |
| I4 | `id -G` fails | `B3_STOP reason=group_probe_failed` | 3 |
| N1 | both namespaces readable | `B3_namespace user=user:[4026531837] mnt=mnt:[4026531840] scope=self_only note=host_binding_is_attested_only_in_RPD-VERIFY` | 0 |
| N2 | `readlink` fails | `B3_STOP reason=namespace_unreadable ns=user path=/proc/self/ns/user` | 3 |
| N3 | `readlink` rc 0, empty | `B3_STOP reason=namespace_identity_empty user=[] mnt=[]` | 3 |
| G1 | dir gid 0, caller `1000 4 27` | `B3_not_in_conf_dir_group path=/etc/mtc-bridge gid=0` | 0 |
| G2 | dir gid 0, caller `1000 0 27` | `B3_STOP reason=caller_in_conf_dir_group path=/etc/mtc-bridge gid=0 caller_gids=[1000 0 27]` | 3 |
| G3 | dir gid 10 vs caller gid 0 | `B3_not_in_conf_dir_group path=/etc/mtc-bridge gid=10` | 0 |
| G4 | `stat %g` fails | `B3_STOP reason=dir_gid_probe_failed path=/etc/mtc-bridge` | 3 |
| C1 | dir, canonical | `B3_conf_dir_canonical path=/etc/mtc-bridge` | 0 |
| C2 | canonicalizes elsewhere | `B3_FAIL reason=conf_dir_not_literal_canonical path=/etc/mtc-bridge canonical=/srv/decoy` | 1 |
| C3 | final component is a symlink | `B3_FAIL reason=conf_dir_kind=link_live path=/etc/mtc-bridge expected=dir` | 1 |
| C4 | `readlink -f` fails | `B3_STOP reason=canonicalization_failed path=/etc/mtc-bridge` | 3 |

### 6.7 access(2) predicate and ERR trap `[A]` (2 + 1)

| Arm | Scenario | Output | Rc |
|---|---|---|---:|
| D1 | path on which `-x` and `-r` are both false | `B3_conf_dir_search_denied path=$QA/fix4/absent-dir mechanism=access_builtin` | 0 |
| D2 | real openable directory | `B3_FAIL reason=conf_dir_search_permitted path=$QA/fix4/dir mechanism=access_builtin_x expected=denied` | 1 |
| T1-b3 | unadjudicated `tr` failure | `B3_STOP reason=unadjudicated_command_status rc=1 line=25 cmd=[tr -d x < /no-such-file-zz]` | 3 |

Honest limit of D1, unchanged from round 2: MSYS cannot make a real directory
refuse search, so the pass arm was driven against a path where both tests are
false for the wrong reason. It exercises the delivered code path, not the kernel
semantics.

### 6.8 Boundary probe `[B]` (11) and the real-coreutils arm `[A]` (1)

The twelve runs in section 5.6.

### 6.9 Mount reader, round-3 code `[B]` (3 + 5 per block)

The `nonl`, `short` and `wide` GREEN runs of section 5.5, plus, for each block:

| Fixture | Output | Rc |
|---|---|---:|
| clean (3 records, none matching) | `..._conf_dir_no_mount_boundary path=/etc/mtc-bridge source=$QA/fix2/mounts/clean records=3` | 0 |
| sibling `/etc/mtc-bridgeX` only | `..._conf_dir_no_mount_boundary path=/etc/mtc-bridge source=$QA/fix2/mounts/sibling records=2` | 0 |
| mount AT the directory | `..._STOP reason=mount_boundary_at_or_under_conf_dir path=/etc/mtc-bridge mounts=1 first_target=/etc/mtc-bridge` | 3 |
| mount UNDER the directory | `..._STOP reason=mount_boundary_at_or_under_conf_dir path=/etc/mtc-bridge mounts=1 first_target=/etc/mtc-bridge/sub` | 3 |
| source absent | `..._STOP reason=mounts_unreadable path=$QA/fix2/mounts/absent` | 3 |

The sibling arm proves the prefix match does not fire on `/etc/mtc-bridgeX`.

### 6.10 `RPD-VERIFY.sh` whole-file, hex guard, pinned tools, ERR trap

`[A]` unless marked.

| Arm | Scenario | Output | Rc |
|---|---|---|---:|
| RD1 | no inputs | `RPD_STOP reason=input_missing name=RPD_CANDIDATE_SHA detail=preregistered candidate release sha, 40 lowercase hex, never derived here` | 3 |
| RD2 | candidate only | `RPD_STOP reason=input_missing name=RPD_RELEASE_MANIFEST_SHA256 ...` | 3 |
| RD3 | all five inputs, non-root caller | `RPD_SECTION identity` / `RPD_STOP reason=must_run_as_root uid=4096` | 3 |
| RD4 | candidate set to the empty string | `RPD_STOP reason=input_missing name=RPD_CANDIDATE_SHA ...` | 3 |
| H1 | 40 lowercase hex | `RPD_input name=RPD_CANDIDATE_SHA value=2ce41e34bceb599d80af24c5c33d835820ec321b` | 0 |
| H2 | uppercase | `RPD_STOP reason=input_charset name=RPD_CANDIDATE_SHA expected=lowercase_hex` | 3 |
| H3 | 8 hex chars | `RPD_STOP reason=input_length name=RPD_CANDIDATE_SHA len=8 expected=40` | 3 |
| H4 | 40 hex in the 64 slot | `RPD_STOP reason=input_length name=RPD_RELEASE_MANIFEST_SHA256 len=40 expected=64` | 3 |
| TP1 | delivered `PYTHON_BIN`, absent here | `RPD_STOP reason=manifest_tool_absent name=python3 path=/usr/bin/python3 detail=pinned absolute interpreter toolchain is required and has no PATH fallback` | 3 |
| TP2 | delivered `ENV_BIN`, QA-host owner | `RPD_STOP reason=manifest_tool_not_root_owned name=env path=/usr/bin/env owner_numeric=4096:4096 expected=0:0` | 3 |
| TP3 `[B]` | pinned path is a directory | `RPD_STOP reason=manifest_tool_kind name=env path=$QA/fix1/adir kind=dir expected=regular_or_live_symlink` | 3 |
| TP4 `[B]` | stubbed `stat`: regular, `0:0`, 755 | `RPD_tool name=env path=$QA/fix1/noexec mode=755 owner_numeric=0:0 resolution=pinned_absolute` | 0 |
| TP5 `[B]` | stubbed `stat`: mode 757 | `RPD_STOP reason=manifest_tool_other_writable name=env path=$QA/fix1/noexec mode=757` | 3 |
| TP6 `[B]` | stubbed `stat`: mode 775 | `RPD_STOP reason=manifest_tool_group_writable name=env path=$QA/fix1/noexec mode=775` | 3 |
| T1-rpd | unadjudicated `tr` failure | `RPD_STOP reason=unadjudicated_command_status rc=1 line=24 cmd=[tr -d x < /no-such-file-zz]` | 3 |

RD3 is the arm that shows the five-input contract is complete: with all five
present and well-formed, the block reaches the root precondition and stops there
for the right reason.

### 6.11 `rpd_probe_kind` `[B]` (10)

`PK-rpd-1` regular, `PK-rpd-2` regular empty, `PK-rpd-3` directory, `PK-rpd-4`
fifo, `PK-rpd-5` link_live, `PK-rpd-6` link_dangling, all rc 0 with the expected
token; `PK-rpd-7` `RPD_STOP reason=link_target_probe_error path=/p rc=1
detail=stat: cannot stat '/p': Input/output error` rc 3; `PK-rpd-8` absent rc 0;
`PK-rpd-9` `RPD_STOP reason=path_probe_error path=/p rc=1 detail=stat: cannot
stat '/p': Permission denied` rc 3; `PK-rpd-10` `RPD_STOP reason=path_probe_empty
path=/p rc=0` rc 3.

### 6.12 `rpd_assert_conf_dir` and `rpd_assert_regular_mode_owner` `[B]` (8 + 7)

| Arm | Scenario | Output | Rc |
|---|---|---|---:|
| CD1 | dir, canonical, 750, `0:0` | `RPD_stat path=/etc/mtc-bridge owner_numeric=0:0 owner_name=root:root mode=750` / `RPD_conf_dir_canonical path=/etc/mtc-bridge` | 0 |
| CD2 | mode 755 | `RPD_FAIL reason=path=/etc/mtc-bridge mode=755 expected=750` | 1 |
| CD3 | uid 1000 rendered `root:root` | `RPD_FAIL reason=path=/etc/mtc-bridge owner_numeric=1000:1000 expected=0:0` | 1 |
| CD4 | canonicalizes to `/srv/decoy` | `RPD_FAIL reason=conf_dir_not_literal_canonical path=/etc/mtc-bridge canonical=/srv/decoy` | 1 |
| CD5 | absent | `RPD_FAIL reason=conf_dir_missing path=/etc/mtc-bridge` | 1 |
| CD6 | the directory IS a symlink | `RPD_FAIL reason=conf_dir_is_symlink kind=link_live path=/etc/mtc-bridge` | 1 |
| CD7 | socket | `RPD_FAIL reason=conf_dir_kind=other path=/etc/mtc-bridge expected=dir` | 1 |
| CD8 | `readlink -f` fails | `RPD_STOP reason=canonicalization_failed path=/etc/mtc-bridge` | 3 |
| LF1 | regular, 600, `0:0` | `RPD_stat path=/etc/mtc-bridge/mtc-bridge.env owner_numeric=0:0 owner_name=root:root mode=600` | 0 |
| LF2 | mode 640 | `RPD_FAIL reason=path=... mode=640 expected=600` | 1 |
| LF3 | uid 1000 rendered `root:root` | `RPD_FAIL reason=path=... owner_numeric=1000:1000 expected=0:0` | 1 |
| LF4 | absent | `RPD_FAIL reason=missing path=...` | 1 |
| LF5 | directory | `RPD_FAIL reason=expected a regular file kind=dir path=...` | 1 |
| LF6 | symlink | `RPD_FAIL reason=canonical deployment path is a symlink kind=link_live path=...` | 1 |
| LF7 | socket | `RPD_FAIL reason=unexpected object kind=other path=...` | 1 |

### 6.13 Manifest binding, round-3 reader `[B]` (9)

Beyond the three item-4 arms in section 5.4 and the two item-1 arms in section
5.1:

| Arm | Fixture | Output | Rc |
|---|---|---|---:|
| NW-good | valid manifest, both bindings correct | `RPD_manifest_binding path=$QAW/fix1/good.json bound=both parser=python3_json_structural keys=top_level_exact isolation=pinned_env_i` | 0 |
| NW-decoy | audit-1 nested `decoy` fixture | `RPD_FAIL reason=install manifest binds a different release_sha` | 1 |
| NW-dup | duplicate `release_sha` | `RPD_STOP reason=install_manifest_ambiguous_duplicate_key path=$QAW/fix1/dup.json` | 3 |
| NW-gone | manifest absent | `RPD_STOP reason=install_manifest_unreadable path=$QAW/fix1/absent.json` | 3 |
| NW-size | 10-byte bound | `RPD_STOP reason=install_manifest_oversize path=$QAW/fix1/good.json limit_bytes=10` | 3 |
| NW-junk | stub interpreter prints `WEIRD OUTPUT!`, rc 0 | `RPD_STOP reason=manifest_parser_unadjudicable path=$QAW/fix1/good.json rc=0 token=[unexpected_reader_output]` | 3 |

NW-good is the arm that proves the isolation did not break the check: through
`env -i`, `-I -S -E` and `cd /`, a correct manifest still parses and still binds.
NW-decoy and NW-dup are audit-1's closures, re-driven against round-3 bytes.
NW-junk proves the token charset guard still holds, so no manifest bytes can be
smuggled out through a STOP reason.

## 7. No file content is printed and no credential value is read

Audited line by line, both blocks, after the round-3 changes.

1. **Every output statement is a `printf` with a fixed ASCII format string.**
   There is no `cat`, `head`, `tail`, `sed`, `awk`, `od`, `strings`, no `echo` of
   a file, and no command substitution whose value comes from a file's CONTENT.
   The values interpolated into output are: a path literal from the block, a
   `stat` metadata field (`%F`, `%a`, `%u:%g`, `%U:%G`, `%g`, `%d:%i`), a numeric
   id from `id -u`/`id -G`, a namespace identity from `readlink /proc/self/ns/*`,
   a canonical path from `readlink -f`, a mount TARGET path from
   `/proc/self/mounts`, a mount record count, a `find` PATH (never file bytes), an
   elapsed-seconds integer, an rc, a preregistered input, a fixed reader token, a
   pinned tool path/mode/owner, and a sanitized `stat`/`find` STDERR string.
2. **The env file is never opened.** In `RP1-B3.sh` the only reference to
   `ENV_FILE` is as an argument to `b3_assert_conf_dir_opaque`, which runs exactly
   one `stat` on it - a metadata syscall the design EXPECTS to be refused. In
   `RPD-VERIFY.sh` the only references are `stat -c` calls. There is no read and
   no redirection from it in either block.
3. **The manifest is read only by the structural reader**, which writes one token
   from the closed set `bound absent_* mismatch_* duplicate_key non_json_constant
   top_level_not_object parse_error read_error too_large open_kind_not_regular
   open_mode_mismatch open_owner_mismatch`, has its stderr sent to `/dev/null` so
   that not even a parser diagnostic carrying a line and column is logged, and is
   further filtered by the `[a-z0-9_]` token guard before any STOP reason is
   composed. Driven: `NW-junk`.
4. **The reader's environment is now an allow-list**, so nothing from the
   operator's environment reaches the child and nothing from the child's
   environment can be echoed: the eight `RPD_*` values it receives are the two
   preregistered hex inputs, the manifest path, the expected mode and the expected
   uid/gid/limit - all block constants or already-printed inputs.
5. **The five values printed verbatim are operator inputs, not host reads.**
   `RPD_input` prints the two hex values and the three attestation values;
   `B3_input` prints the three B3 inputs. All are format-proven before printing,
   and on every rejection arm the value is deliberately NOT printed (only its name
   and, for the hex guard, its length).
6. **Nothing reads a credential.** Neither block references a token, key,
   password, `Authorization`, `/api/arm`, an exchange, an order, TESTNET or
   mainnet. Command inventory across both files: `stat`, `find`, `id`, `readlink`,
   `printf`, plus `env` and `python3` (RPD only, both pinned absolute). Removed
   since round 1: `mktemp`, `tr`, `rm`, `grep`. Removed since round 2:
   `command -v python3`. Scanned for and confirmed absent: `chmod`, `chown`,
   `chgrp`, `setfacl`, `sudo`, `mv`, `cp`, `ln`, `mkdir`, `touch`, `tee`, `dd`,
   `truncate`, `sed`, `systemctl`, `curl`, `wget`, `ssh`, `scp`, `nc`, `openssl`,
   `pip`.
7. **There is no file-writing redirection in either block.** The only redirections
   are `2>&1` into a variable capture, `2>/dev/null` (discard), `>/dev/null` on
   `command -v rp0_monotonic_ms` and on the `cd`, and `exec 9< <read-only file>`
   plus its close. No `>` or `>>` targets any path.
8. **`RPD-VERIFY.sh` mutates nothing, and now that claim covers its child.** No
   write to `ENV_FILE`, `INSTALL_MANIFEST` or `CONF_DIR`, no mode/owner change, no
   service or network call, no `sudo`, no group or ACL change. Its root
   requirement is used solely for metadata probes and one read-only open. Round 2
   could make this claim only about the shell: an unisolated interpreter could
   execute imported code as root. `-I -S -E` under `env -i` from a pinned,
   root-owned binary is what restores it.

## 8. Known gaps in this QA

Stated so the re-audit does not have to find them.

1. **No Linux host.** The genuine EACCES pass arm, the access(2) denial, the
   namespace reads against a real kernel, the real mount table, `stat -c '%d:%i'`
   of a real root filesystem, and numeric `0:0` ownership of real files could not
   be produced here. They were driven through stubs and fixtures whose shapes are
   the real coreutils and kernel shapes. `LC_ALL=C` is exported and pinned, which
   is what makes the message shape predictable; the exact-shape rule was
   additionally validated against a REAL coreutils 8.32 ENOENT diagnostic
   (section 5.6, last arm).
2. **MSYS has no `/proc/self/ns`, `/proc/self/uid_map` or `/proc/self/mounts`.**
   Every arm that consumes them used a fixture path or a stub, except `R5`, which
   drove the unreadable STOP for real.
3. **The pinned interpreter could not be driven root-owned.** `/usr/bin/python3`
   does not exist here and no QA-host file is owned `0:0`, so the functional
   manifest arms repoint `PYTHON_BIN` and stub `rpd_require_pinned_tool`, while
   the predicate itself is driven separately with real absent/wrong-owner paths
   and a stubbed `stat` for the mode arms. The combination
   "pinned tool passes AND the child then parses" has therefore never run as one
   uninterrupted sequence on any host.
4. **`shellcheck` was not run** (not installed on this host). Only `bash -n`
   evidence is provided.
5. **`python3` on the QA host is Windows Python 3.13**, not the target's 3.12, and
   it renders POSIX metadata as `0666 0:0`. The JSON semantics exercised
   (duplicate keys, `parse_constant`, top-level typing, exact string comparison,
   trailing data) are standard-library behaviour and are stable across both; the
   fstat arms were driven with QA-host values as disclosed in section 4.
   `-S` was verified to leave `import json, os, stat, sys` working on this host,
   but not on a Debian-family python3.
6. **Four arms were not driven at all** and are excluded from every count; they
   are listed in section 3.
7. **`RPD-VERIFY.sh` has never run as root** anywhere, and round 3 added two more
   Linux-only dependencies plus three attestation inputs that do not exist yet.
   Its PASS path is fixture-exercised only (open item O7).
8. **The attestation itself cannot be QA'd here.** Section 5.2 proves the block
   compares correctly against attested values; nothing in this QA can prove the
   deploy channel will mint them correctly. That is the residual named in
   DESIGN_NOTES section 9.1 and it is the Lead's to close.
9. **The section 8 #4 naming risk remains unresolved** and cannot be resolved by
   any unprivileged block, by construction of the EACCES denial.
