# SELF QA - B3-GAP-ENV Option 1 design repair, round 2

Subjects: `round2/RP1-B3.sh` (489 lines), `round2/RPD-VERIFY.sh` (518 lines).

```
88ff0f23851b544e956a013c095b34180c0db04def85f04612b704348a1c2248  RP1-B3.sh
8e6edeeb232f4ed8a728810cfb4b3c5c7a9a21c0549d1d1f5a157e0d678650a9  RPD-VERIFY.sh
```

No remote host was contacted. Nothing outside `round2/` was written inside the
repository; the harness, its stubs and its JSON fixtures live in a session
scratch directory outside the repository tree and are reproduced verbatim in
section 3. Neither block was run against `/etc/mtc-bridge`, `/opt/mtc-bridge` or
any other target path: the QA host is Windows/MSYS and has none of them.

## 1. Environment

```
$ bash --version | head -1
GNU bash, version 5.2.37(1)-release (x86_64-pc-msys)
$ python3 --version
Python 3.13.14
$ command -v shellcheck
(not installed - shellcheck was NOT run; see section 8)
```

## 2. `bash -n` and encoding evidence

```
$ cd round2
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
```

Re-run after the final edit of each file; both still rc=0.

## 3. Method, and the three counts N1 asked for

Every arm below was driven through a harness that does **not** retype any
predicate: each function is extracted from the delivered file mechanically

```
awk -v fn="$1" 'index($0, fn "() {")==1 {f=1} f{print} f && /^\}$/{exit}' "$SRC"
```

and `eval`ed under `set -Eeuo pipefail` with the delivered `..._on_err` trap, the
delivered `..._sanitize`, the delivered constants, and the real
`b3_stop`/`b3_fail` (resp. `rpd_*`) definitions, so the bytes exercised are the
delivered bytes.

**The three counts, for both files together:**

| Category | Count |
|---|---:|
| A. Delivered-code arms run with NO stubbed command (real tools, real files) | **43** |
| B. Delivered-code arms run with at least one stubbed command or repointed path literal | **82** |
| C. Inherited RP0-LIB arms NOT re-run (not driven, not claimed as driven) | **3** |

Per file: `RP1-B3.sh` = 15 in A, 48 in B (63 runs). `RPD-VERIFY.sh` = 28 in A,
34 in B (62 runs). Total driven: 125 runs, 125 matched the designed outcome,
**0 mismatches**.

Category C in full, so it is not a vague remainder: the three internal paths of
`rp0_monotonic_ms` (RP0-LIB:18-22) - its success path, its
`/proc/uptime`-unreadable STOP, and an `awk` failure. This block reaches them
only through `t0="$(rp0_monotonic_ms)" || b3_stop "monotonic_clock_unevaluable"`,
and that adjudication IS driven (arm `W6`) with a stub returning 3; the library
function's own three paths were not re-run here and are not claimed as driven.
`RPD-VERIFY.sh` calls no library function at all, so it inherits nothing.

Round 1's `[accepted]` category has no members in round 2: the two predicates
that were byte-identical to the accepted block were modified for F3/F4/F6 (see
DESIGN_NOTES section 3.1) and are therefore driven here, not inherited.

Two QA substitutions are used, and only these two:

1. `/proc/self/uid_map` is a literal in the delivered code and does not exist on
   the QA host. For arms `NSU_*`, `NSM`, `NSOK` and `NSUNR` the extracted
   function body had exactly that one literal replaced with a fixture path by a
   single `sed` substitution; every other byte is delivered. Arm `NS1` uses the
   unmodified literal and drives the unreadable STOP for real.
2. The QA host's `python3` is Windows Python, which renders file metadata as mode
   `0666`, uid `0`, gid `0`. The manifest arms therefore pass `0666` where the
   deploy-time call passes `0640`; the mode and owner mismatch arms are driven by
   passing values the fixture does not have.

One harness defect is disclosed rather than hidden: the first budget-exceeded
stub referenced an unset counter variable under `set -u`, so it drove
`monotonic_clock_unevaluable` instead of the intended arm. It was rebuilt with a
file-backed counter (`W5b`) and then produced the intended
`sweep_budget_exceeded`. The defective run is not counted.

## 4. `RP1-B3.sh` arm walk (63 runs)

`[A]` = no stubbed command. `[B]` = stubbed command or repointed literal.

### 4.1 Input guards and preconditions, delivered file executed as a file `[A]`

| Arm | Command | Output | Rc |
|---|---|---|---:|
| R1 | `env -u B3_SWEEP_BUDGET_S bash RP1-B3.sh` | `B3_STOP reason=input_missing name=B3_SWEEP_BUDGET_S detail=preregistered per-tree sweep budget in seconds, positive integer, never derived here` | 3 |
| R2 | `B3_SWEEP_BUDGET_S=abc` | `B3_STOP reason=input_charset name=B3_SWEEP_BUDGET_S expected=decimal_digits` | 3 |
| R3 | `B3_SWEEP_BUDGET_S=0` | `B3_STOP reason=input_range name=B3_SWEEP_BUDGET_S value=0 expected=positive_integer` | 3 |
| R4 | `B3_SWEEP_BUDGET_S=120`, RP0-LIB not sourced | `B3_STOP reason=rp0_lib_not_sourced predicate=rp0_monotonic_ms` | 3 |
| R5 | `. RP0-LIB.sh; . RP1-B3.sh` end to end | `B3_SECTION header candidate=2ce41e34...321b` / `B3_identity uid=4096 gids=[4096]` / `B3_STOP reason=namespace_unreadable ns=user path=/proc/self/ns/user` | 3 |

R1-R3 are the O2 fix: a missing or malformed operator input is now rc 3 with a
reason string, where round 1 exited 1 through the bare `:?` guard. R5 stops at
the namespace disclosure because MSYS has no `/proc/self/ns` at all
(`ls: cannot access '/proc/self/ns/': No such file or directory`); on Linux this
line records the two identities and continues. That is a real new dependency and
it is stated in DESIGN_NOTES section 8.

### 4.2 `b3_sanitize` `[A]`

| Arm | Input | `B3_SAFE` |
|---|---|---|
| S1 | `a<LF>b` | `[a b]` |
| S2 | `x<BEL>y` | `[[non_printable_detail_suppressed]]` |
| S3 | 500 `a` bytes | `len=400` |

### 4.3 `b3_probe_kind`, stubbed `stat` `[B]`

| Arm | Stub | Result | Rc |
|---|---|---|---:|
| K1 | `regular file` | `kind=regular` | 0 |
| K2 | `regular empty file` | `kind=regular` | 0 |
| K3 | `directory` | `kind=dir` | 0 |
| K4 | `fifo` | `kind=other` | 0 |
| K5 | `symbolic link` + live target | `kind=link_live` | 0 |
| K6 | `symbolic link` + ENOENT target | `kind=link_dangling` | 0 |
| K7 | `symbolic link` + EIO target | `B3_STOP reason=link_target_probe_error path=/p rc=1 detail=stat: cannot statx '/p': Input/output error` | 3 |
| K8 | rc 1, ENOENT | `kind=absent` | 0 |
| K9 | rc 1, EACCES | `B3_STOP reason=path_probe_error path=/p rc=1 detail=stat: cannot statx '/p': Permission denied` | 3 |
| K10 | rc 0, empty output | `B3_STOP reason=path_probe_empty path=/p rc=0` | 3 |

K9 and K10 are the two arms that make the no-temp classifier equivalent in
strength to `rp0_probe_path`: a probe error is never `absent`, and silence is
never success.

### 4.4 `b3_assert_mode_owner`, stubbed `stat` `[B]`

| Arm | Scenario | Output | Rc |
|---|---|---|---:|
| M1 | `0555 0:0` expected, matches | `B3_stat path=/p owner_numeric=0:0 owner_name=root:root mode=555` | 0 |
| M2 | uid 1000 rendered as `root:root` (F3 scenario 1) | `B3_FAIL reason=path=/p owner_numeric=1000:1000 expected=0:0` | 1 |
| M3 | mode drift | `B3_FAIL reason=path=/p mode=755 expected=555` | 1 |
| M4 | `mtc-bridge:mtc-bridge`, uid 1500 | `B3_stat path=/p owner_numeric=1500:1500 owner_name=mtc-bridge:mtc-bridge mode=750` | 0 |
| M5 | `mtc-bridge` name over uid 0 | `B3_FAIL reason=path=/p owner_numeric=0:1500 expected=nonzero_service_account name=mtc-bridge:mtc-bridge` | 1 |
| M6 | wrong service account name | `B3_FAIL reason=path=/p owner_name=other:other expected=mtc-bridge:mtc-bridge` | 1 |
| M7 | path absent | `B3_FAIL reason=missing path=/p` | 1 |
| M8 | symlink at a canonical path | `B3_FAIL reason=canonical deployment path is a symlink kind=link_live path=/p` | 1 |
| M9 | socket/fifo/device | `B3_FAIL reason=unexpected object kind=other path=/p` | 1 |
| M10 | `stat %a` fails | `B3_STOP reason=mode_probe_failed path=/p` | 3 |

M2 is the F3 fix reproduced directly: round 1 would have PASSed this file.

### 4.5 `b3_assert_no_writable_paths`, stubbed `find` and clock `[B]`

| Arm | Scenario | Output | Rc |
|---|---|---|---:|
| W1 | clean tree | `B3_sweep root=/opt/tree elapsed_s=0 budget_s=120` / `B3_no_write_bit root=/opt/tree` | 0 |
| W2 | offender found | `B3_FAIL reason=writable path inside immutable tree: /opt/tree/bad` | 1 |
| W3 | `find` rc 1 with stderr | `B3_STOP reason=writable_inventory_failed root=/opt/tree rc=1 detail=/opt/tree/xfind: permission denied` | 3 |
| W4 | rc 0, output not under root | `B3_STOP reason=writable_inventory_unparsable root=/opt/tree rc=0 out=surprise-not-a-path` | 3 |
| W5b | elapsed 200s over a 120s budget | `B3_STOP reason=sweep_budget_exceeded root=/opt/tree elapsed_s=200 budget_s=120` | 3 |
| W6 | clock predicate returns 3 | `B3_STOP reason=monotonic_clock_unevaluable root=/opt/tree phase=start` | 3 |
| W7 | clock predicate returns non-numeric | `B3_STOP reason=monotonic_clock_unparsable root=/opt/tree t0=[notanumber] t1=[notanumber]` | 3 |

W3 shows the disclosed merge: `detail=` now carries the partial stdout
(`/opt/tree/x`) followed by the stderr text, where round 1 had two fields. No
predicate reads it.

### 4.6 Identity, namespaces, group `[B]`

| Arm | Scenario | Output | Rc |
|---|---|---|---:|
| I1 | uid 1000 | `B3_identity uid=1000 gids=[1000 4 27]` | 0 |
| I2 | uid 0 | `B3_STOP reason=must_run_unprivileged uid=0` | 3 |
| I3 | `id -u` fails | `B3_STOP reason=uid_probe_failed` | 3 |
| I4 | `id -G` fails | `B3_STOP reason=group_probe_failed` | 3 |
| N1 | both namespaces readable | `B3_namespace user=user:[4026531837] mnt=user:[4026531837] scope=self_only note=initial_ns_comparison_needs_root` | 0 |
| N2 | `readlink` fails | `B3_STOP reason=namespace_unreadable ns=user path=/proc/self/ns/user` | 3 |
| N3 | `readlink` rc 0, empty | `B3_STOP reason=namespace_identity_empty user=[] mnt=[]` | 3 |
| G1 | gid 0, caller `1000 4 27` | `B3_not_in_conf_dir_group path=/etc/mtc-bridge gid=0` | 0 |
| G2 | gid 0, caller `1000 0 27` | `B3_STOP reason=caller_in_conf_dir_group path=/etc/mtc-bridge gid=0 caller_gids=[1000 0 27]` | 3 |
| G3 | gid 10 vs caller gid 0 (whole-word match) | `B3_not_in_conf_dir_group path=/etc/mtc-bridge gid=10` | 0 |
| G4 | `stat %g` fails | `B3_STOP reason=dir_gid_probe_failed path=/etc/mtc-bridge` | 3 |

### 4.7 CONF_DIR identity: canonical path `[B]` and mount boundary `[A]`

| Arm | Scenario | Output | Rc |
|---|---|---|---:|
| C1 | dir, canonical | `B3_conf_dir_canonical path=/etc/mtc-bridge` | 0 |
| C2 | canonicalizes elsewhere (F2 decoy) | `B3_FAIL reason=conf_dir_not_literal_canonical path=/etc/mtc-bridge canonical=/srv/decoy` | 1 |
| C3 | final component is a symlink | `B3_FAIL reason=conf_dir_kind=link_live path=/etc/mtc-bridge expected=dir` | 1 |
| C4 | `readlink -f` fails | `B3_STOP reason=canonicalization_failed path=/etc/mtc-bridge` | 3 |
| MB1 | mounts contain `/etc/mtc-bridgeX` only | `B3_conf_dir_no_mount_boundary path=/etc/mtc-bridge source=<fixture>` | 0 |
| MB2 | mount AT the directory | `B3_STOP reason=mount_boundary_at_or_under_conf_dir path=/etc/mtc-bridge mounts=1 first_target=/etc/mtc-bridge` | 3 |
| MB3 | mount UNDER the directory | `B3_STOP reason=mount_boundary_at_or_under_conf_dir path=/etc/mtc-bridge mounts=1 first_target=/etc/mtc-bridge/sub` | 3 |
| MB4 | mounts file unreadable | `B3_STOP reason=mounts_unreadable path=<fixture>` | 3 |

MB1 also proves the prefix match does not fire on the sibling name
`/etc/mtc-bridgeX`.

### 4.8 access(2) predicate `[A]`

| Arm | Scenario | Output | Rc |
|---|---|---|---:|
| D1 | path on which `-x` and `-r` are both false | `B3_conf_dir_search_denied path=<dir> mechanism=access_builtin` | 0 |
| D2 | real openable directory | `B3_FAIL reason=conf_dir_search_permitted path=<dir> mechanism=access_builtin_x expected=denied` | 1 |

Honest limit of arm D1: MSYS cannot make a real directory refuse search, so the
pass arm was driven against a path where both tests are false for the wrong
reason. It exercises the delivered code path, not the kernel semantics. The
`conf_dir_read_permitted` FAIL arm (`-x` false, `-r` true) is NOT reachable on
this host and was NOT driven; it is verified by inspection only, and is counted
in neither A nor B.

### 4.9 Boundary probe, stubbed `stat` `[B]`

| Arm | Scenario | Output | Rc |
|---|---|---|---:|
| O1 | `stat` SUCCEEDS | `B3_FAIL reason=conf_dir_entry_permitted path=/etc/mtc-bridge/mtc-bridge.env stat=[regular file\|600\|0:0] expected=EACCES` | 1 |
| O2 | EACCES | `B3_conf_dir_opaque_to_operator path=/etc/mtc-bridge/mtc-bridge.env outcome=EACCES rc=1 mechanism=message_lc_all_c` | 0 |
| O3 | ENOENT | `B3_FAIL reason=conf_dir_search_permitted_name_absent path=/etc/mtc-bridge/mtc-bridge.env rc=1 expected=EACCES` | **1** |
| O4 | EIO | `B3_STOP reason=boundary_probe_unclassified path=... rc=1 detail=stat: cannot statx '...': Input/output error` | 3 |
| O5 | rc 4, EMPTY stderr | `B3_STOP reason=boundary_probe_unclassified path=... rc=4 detail=` | 3 |
| O6 | diagnostic carrying a non-printable byte | `B3_STOP reason=boundary_probe_unclassified path=... rc=1 detail=[non_printable_detail_suppressed]` | 3 |

O3 is the F5/O1 fix: round 1 emitted rc 3 here with the same reason string; the
class is now FAIL. O6 shows that suppression is fail-closed - a diagnostic that
contains `Permission denied` next to a non-printable byte does NOT reach the
pass arm.

### 4.10 ERR trap backstop `[A]`

| Arm | Scenario | Output | Rc |
|---|---|---|---:|
| T1 | unadjudicated `tr` failure (the exact F6 mechanism) | `B3_STOP reason=unadjudicated_command_status rc=1 line=23 cmd=[tr -d x < /no-such-file-zz]` | 3 |

Round 1 exited here with `tr`'s own status and no reason string.

## 5. `RPD-VERIFY.sh` arm walk (62 runs)

### 5.1 Delivered file executed as a file `[A]`

| Arm | Scenario | Output | Rc |
|---|---|---|---:|
| RD1 | no inputs | `RPD_STOP reason=input_missing name=RPD_CANDIDATE_SHA detail=preregistered candidate release sha, 40 lowercase hex, never derived here` | 3 |
| RD2 | candidate only | `RPD_STOP reason=input_missing name=RPD_RELEASE_MANIFEST_SHA256 detail=preregistered accepted RELEASE_SHA256SUMS sha256, 64 lowercase hex, never derived here` | 3 |
| RD3 | both inputs, non-root caller | `RPD_SECTION identity` / `RPD_STOP reason=must_run_as_root uid=4096` | 3 |
| RD4 | candidate set to the empty string | `RPD_STOP reason=input_missing name=RPD_CANDIDATE_SHA ...` | 3 |
| RD5 | RP0-LIB sourced first (it is no longer needed) | `RPD_SECTION identity` / `RPD_STOP reason=must_run_as_root uid=4096` | 3 |

RD5 confirms the block behaves identically with and without RP0-LIB sourced.

### 5.2 `rpd_require_hex` `[A]`

| Arm | Input | Output | Rc |
|---|---|---|---:|
| H1 | 40 lowercase hex | `RPD_input name=RPD_CANDIDATE_SHA value=2ce41e34bceb599d80af24c5c33d835820ec321b` | 0 |
| H2 | uppercase | `RPD_STOP reason=input_charset name=RPD_CANDIDATE_SHA expected=lowercase_hex` | 3 |
| H3 | 8 hex chars | `RPD_STOP reason=input_length name=RPD_CANDIDATE_SHA len=8 expected=40` | 3 |
| H4 | 40 hex in the 64 slot | `RPD_STOP reason=input_length name=RPD_RELEASE_MANIFEST_SHA256 len=40 expected=64` | 3 |

Neither STOP arm prints the rejected value.

### 5.3 `rpd_probe_kind`, stubbed `stat` `[B]`

`PK1` regular, `PK2` dir, `PK3` other (socket), `PK4` link_live, `PK5`
link_dangling, all rc 0; `PK6` `RPD_STOP reason=link_target_probe_error path=/p
rc=1 detail=stat: cannot statx '/p': Input/output error` rc 3; `PK7` absent rc 0;
`PK8` `RPD_STOP reason=path_probe_error ... Permission denied` rc 3; `PK9`
`RPD_STOP reason=path_probe_empty path=/p rc=0` rc 3.

### 5.4 `rpd_assert_initial_namespaces` `[B]`

| Arm | Scenario | Output | Rc |
|---|---|---|---:|
| NS1 | real `/proc/self/uid_map`, absent on MSYS | `RPD_STOP reason=uid_map_unreadable path=/proc/self/uid_map` | 3 |
| NSU_ok | identity map `0 0 4294967295` | `RPD_namespace user=ns:[1] mnt=ns:[1] bound=initial uid_map=identity` | 0 |
| NSU_rootless | map `0 1000 1` (F3 scenario 2) | `RPD_STOP reason=user_namespace_not_initial reason=uid_map_not_identity map=[0 1000 1]` | 3 |
| NSU_multi | two mapping lines | `RPD_STOP reason=user_namespace_not_initial reason=multiple_uid_map_lines lines=2` | 3 |
| NSU_empty | empty uid_map | `RPD_STOP reason=user_namespace_not_initial reason=empty_uid_map lines=0` | 3 |
| NSM | self user ns != pid 1 user ns | `RPD_STOP reason=namespace_not_initial ns=user self=user:[4026531837] init=user:[4026999999]` | 3 |
| NSOK | self == pid 1 for both namespaces | `RPD_namespace user=user:[4026531837] mnt=mnt:[4026531840] bound=initial uid_map=identity` | 0 |
| NSUNR | `readlink` on the ns links fails | `RPD_STOP reason=namespace_unreadable ns=user path=/proc/self/ns/user` | 3 |

`NSU_rootless` is the F3 scenario-2 refutation: a rootless namespace that maps
host uid 1000 to namespace uid 0 cannot pass, even though `id -u` prints 0 there.

### 5.5 `rpd_assert_conf_dir` `[B]` and `rpd_assert_no_mount_at_or_under` `[A]`

| Arm | Scenario | Output | Rc |
|---|---|---|---:|
| CD1 | dir, canonical, 750, 0:0 | `RPD_stat path=/etc/mtc-bridge owner_numeric=0:0 owner_name=root:root mode=750` / `RPD_conf_dir_canonical path=/etc/mtc-bridge` | 0 |
| CD2 | mode 755 | `RPD_FAIL reason=path=/etc/mtc-bridge mode=755 expected=750` | 1 |
| CD3 | uid 1000 rendered `root:root` | `RPD_FAIL reason=path=/etc/mtc-bridge owner_numeric=1000:1000 expected=0:0` | 1 |
| CD4 | canonicalizes to `/srv/decoy` (the F2 attack) | `RPD_FAIL reason=conf_dir_not_literal_canonical path=/etc/mtc-bridge canonical=/srv/decoy` | 1 |
| CD5 | absent | `RPD_FAIL reason=conf_dir_missing path=/etc/mtc-bridge` | 1 |
| CD6 | `/etc/mtc-bridge` IS a symlink to a decoy dir (the F2 attack) | `RPD_FAIL reason=conf_dir_is_symlink kind=link_live path=/etc/mtc-bridge` | 1 |
| CD7 | socket | `RPD_FAIL reason=conf_dir_kind=other path=/etc/mtc-bridge expected=dir` | 1 |
| CD8 | `readlink -f` fails | `RPD_STOP reason=canonicalization_failed path=/etc/mtc-bridge` | 3 |
| MB1 | clean mount table | `RPD_conf_dir_no_mount_boundary path=/etc/mtc-bridge source=<fixture>` | 0 |
| MB2 | mount AT the directory | `RPD_STOP reason=mount_boundary_at_or_under_conf_dir path=/etc/mtc-bridge mounts=1 first_target=/etc/mtc-bridge` | 3 |
| MB3 | mount UNDER the directory | `RPD_STOP reason=mount_boundary_at_or_under_conf_dir path=/etc/mtc-bridge mounts=1 first_target=/etc/mtc-bridge/sub` | 3 |
| MB4 | mounts file unreadable | `RPD_STOP reason=mounts_unreadable path=<fixture>` | 3 |

CD4 and CD6 are the two shapes of the F2 attack; round 1 admitted both.

### 5.6 `rpd_assert_regular_mode_owner` `[B]`

| Arm | Scenario | Output | Rc |
|---|---|---|---:|
| LF1 | regular, 600, 0:0 | `RPD_stat path=/etc/mtc-bridge/mtc-bridge.env owner_numeric=0:0 owner_name=root:root mode=600` | 0 |
| LF2 | mode 640 | `RPD_FAIL reason=path=... mode=640 expected=600` | 1 |
| LF3 | uid 1000 rendered `root:root` | `RPD_FAIL reason=path=... owner_numeric=1000:1000 expected=0:0` | 1 |
| LF4 | absent (the sec. 8 #4 naming risk becomes answerable here) | `RPD_FAIL reason=missing path=...` | 1 |
| LF5 | directory | `RPD_FAIL reason=expected a regular file kind=dir path=...` | 1 |
| LF6 | symlink | `RPD_FAIL reason=canonical deployment path is a symlink kind=link_live path=...` | 1 |
| LF7 | socket | `RPD_FAIL reason=unexpected object kind=other path=...` | 1 |

### 5.7 `rpd_assert_manifest_binding`, real `python3`, real fixtures `[A]` except where noted

| Arm | Fixture | Output | Rc |
|---|---|---|---:|
| BD_mf_good | valid manifest, both bindings correct | `RPD_manifest_binding path=... bound=both parser=python3_json_structural keys=top_level_exact` | 0 |
| BD_mf_decoy | **the audit's F1 fixture**: correct values nested in `decoy`, both top-level values wrong | `RPD_FAIL reason=install manifest binds a different release_sha` | **1** |
| BD_mf_dup | duplicate `release_sha`, accepted value first | `RPD_STOP reason=install_manifest_ambiguous_duplicate_key path=...` | **3** |
| BD_mf_absent | `release_sha` absent | `RPD_FAIL reason=install manifest does not bind release_sha` | 1 |
| BD_mf_wrong | wrong `release_sha` | `RPD_FAIL reason=install manifest binds a different release_sha` | 1 |
| BD_mf_array | top level is an array | `RPD_STOP reason=install_manifest_not_single_top_level_object path=...` | 3 |
| BD_mf_bad | truncated JSON | `RPD_STOP reason=install_manifest_unparsable path=...` | 3 |
| BD_mf_num | `release_sha` is a number, not a string | `RPD_FAIL reason=install manifest binds a different release_sha` | 1 |
| BD_mf_trailing | valid object followed by trailing data | `RPD_STOP reason=install_manifest_unparsable path=...` | 3 |
| BD_gone | file absent | `RPD_STOP reason=install_manifest_unreadable path=...` | 3 |
| BD_mode | expected mode differs from the open descriptor's | `RPD_STOP reason=install_manifest_mode_changed_between_stat_and_read path=...` | 3 |
| BD_owner | expected owner differs from the open descriptor's | `RPD_STOP reason=install_manifest_owner_changed_between_stat_and_read path=...` | 3 |
| BD_size | 10-byte bound | `RPD_STOP reason=install_manifest_oversize path=... limit_bytes=10` | 3 |
| BD_nopy | empty `PATH`, no `python3` | `RPD_STOP reason=manifest_parser_absent tool=python3 path=... detail=structural JSON verification is required and has no weaker fallback` | 3 |
| BD_junk `[B]` | stub `python3` prints `WEIRD OUTPUT!`, rc 0 | `RPD_STOP reason=manifest_parser_unadjudicable path=... rc=0 token=[unexpected_reader_output]` | 3 |
| BD_rc9 `[B]` | stub `python3` exits 9 with no output | `RPD_STOP reason=manifest_parser_unadjudicable path=... rc=9 token=[unexpected_reader_output]` | 3 |

`BD_junk` also proves the token charset guard: a reader that emits anything
outside `[a-z0-9_]` has its output replaced by a fixed literal before it can
reach the evidence log, so no manifest bytes can be smuggled out through the
STOP reason.

Not driven: `open_kind_not_regular` (it needs a non-regular object that `open`
succeeds on, which the QA host cannot produce), and `read_error` raised mid-read
rather than at open. Both are counted in neither A nor B.

### 5.8 ERR trap backstop `[A]`

`T1`: `RPD_STOP reason=unadjudicated_command_status rc=1 line=32 cmd=[tr -d x < /no-such-file-zz]`, rc 3.

## 6. The F1 refutation, reproduced end to end

The audit's fixture, byte for byte:

```json
{"decoy": {"release_sha": "2ce41e34bceb599d80af24c5c33d835820ec321b", "release_manifest_sha256": "edb0fd34e3d976b872868cc3dfbf745cbc4b08f6c4c5d21b8d6cda47a3e20d26"}, "release_sha": "0000000000000000000000000000000000000000", "release_manifest_sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
```

Round 1 (`grep -qsF`): `GREP_RELEASE_RC=0`, `GREP_MANIFEST_RC=0`, i.e. `RPD PASS`.
Round 2 (`rpd_assert_manifest_binding`, delivered bytes):

```
RPD_FAIL reason=install manifest binds a different release_sha
rc=1
```

Duplicate-key fixture (accepted value first, wrong value second), which the
round-1 grep also admitted:

```
RPD_STOP reason=install_manifest_ambiguous_duplicate_key path=<fixture>
rc=3
```

The parser was additionally exercised standalone across nine JSON shapes before
being wired in; the wired results above are the ones that count.

## 7. No file content is printed and no credential value is read

Audited line by line, both blocks, after the round 2 changes.

1. **Every output statement is a `printf` with a fixed ASCII format string.**
   There is no `cat`, `head`, `tail`, `sed`, `awk`, `od`, `strings`, no `echo` of
   a file, and no command substitution whose value comes from a file's CONTENT.
   The values interpolated into output are: a path literal from the block, a
   `stat` metadata field (`%F`, `%a`, `%u:%g`, `%U:%G`, `%g`), a numeric id from
   `id -u`/`id -G`, a namespace identity from `readlink /proc/*/ns/*`, a
   canonical path from `readlink -f`, a mount TARGET path from
   `/proc/self/mounts`, a `find` PATH (never file bytes), an elapsed-seconds
   integer, an rc, a preregistered input, a fixed reader token, and a sanitized
   `stat`/`find` STDERR string.
2. **The env file is never opened.** In `RP1-B3.sh` the only reference to
   `ENV_FILE` is as an argument to `b3_assert_conf_dir_opaque`, which runs
   exactly one `stat` on it - a metadata syscall the design EXPECTS to be
   refused. In `RPD-VERIFY.sh` the only references are `stat -c` calls. There is
   no read and no redirection from it in either block.
3. **The manifest is read only by the structural reader**, which writes one token
   from the closed set `bound absent_* mismatch_* duplicate_key
   top_level_not_object parse_error read_error too_large open_kind_not_regular
   open_mode_mismatch open_owner_mismatch`, has its stderr sent to `/dev/null` so
   that not even a parser diagnostic carrying a line and column is logged, and is
   further filtered by the `[a-z0-9_]` token guard before any STOP reason is
   composed. Driven: `BD_junk`.
4. **The two values printed verbatim are operator inputs, not host reads.**
   `RPD_input` prints `RPD_CANDIDATE_SHA` and `RPD_RELEASE_MANIFEST_SHA256`, both
   supplied from preregistration and both format-proven lowercase hex of the
   preregistered width BEFORE printing. On the two rejection arms the value is
   deliberately NOT printed (only its name and length).
5. **Nothing reads a credential.** Neither block references a token, key,
   password, `Authorization`, `/api/arm`, an exchange, an order, TESTNET or
   mainnet. Command inventory across both files: `stat`, `find`, `id`,
   `readlink`, `command -v`, `printf`, and `python3` (RPD only). Removed since
   round 1: `mktemp`, `tr`, `rm`, `grep`. Scanned for and confirmed absent:
   `chmod`, `chown`, `chgrp`, `setfacl`, `sudo`, `mv`, `cp`, `ln`, `mkdir`,
   `touch`, `tee`, `dd`, `truncate`, `sed`, `systemctl`, `curl`, `wget`, `ssh`,
   `scp`, `nc`, `openssl`, `pip`.
6. **There is no file-writing redirection in either block.** The only
   redirections are `2>&1` into a variable capture, `2>/dev/null` (discard),
   `>/dev/null` on `command -v`, and `exec 9< <read-only file>` plus its close.
   No `>` or `>>` targets any path. This is the O3/F4 claim, and it is why both
   headers can now state the mutation surface as none.
7. **`RPD-VERIFY.sh` mutates nothing.** No write to `ENV_FILE`,
   `INSTALL_MANIFEST` or `CONF_DIR`, no mode/owner change, no service or network
   call, no `sudo`, no group or ACL change. Its root requirement is used solely
   for metadata probes and one read-only open.

## 8. Known gaps in this QA

Stated so the re-audit does not have to find them.

1. **No Linux host.** The genuine EACCES pass arm, the access(2) denial, the
   namespace predicates against a real kernel, the mount table and the numeric
   `0:0` ownership of real files could not be produced here. They were driven
   through stubs and fixtures whose shapes are the real `coreutils` and kernel
   shapes. A different `stat` implementation or a translated locale would land in
   `boundary_probe_unclassified` - fail-closed, but a real first-run risk;
   `LC_ALL=C` is exported and pinned, which is what makes the message shape
   predictable.
2. **MSYS has no `/proc/self/ns`, `/proc/self/uid_map` or `/proc/self/mounts`.**
   Every arm that consumes them used a fixture path or a stub, except `NS1` and
   `R5`, which drove the unreadable STOPs for real. On Linux these are the paths
   the block will actually read.
3. **`shellcheck` was not run** (not installed on this host). Only `bash -n`
   evidence is provided, as the kickoff required.
4. **`python3` on the QA host is Windows Python 3.13**, not the target's 3.12,
   and it renders POSIX file metadata as `0666 0:0`. The JSON semantics
   exercised (duplicate keys, top-level typing, exact string comparison, trailing
   data) are standard-library behaviour and are stable across both; the fstat
   arms were driven with QA-host values as disclosed in section 3.
5. **Three arms were not driven at all** and are excluded from both counts:
   `conf_dir_read_permitted` (section 4.8), `open_kind_not_regular` and a
   mid-read `read_error` (section 5.7).
6. **`RPD-VERIFY.sh` has never run as root** anywhere, and round 2 added four
   Linux-only dependencies to it. Its PASS path is fixture-exercised only. Treat
   the first deploy-time run as a first run (open item O7).
7. **The section 8 #4 naming risk remains unresolved** and cannot be resolved by
   any unprivileged block, by construction of the EACCES denial.
