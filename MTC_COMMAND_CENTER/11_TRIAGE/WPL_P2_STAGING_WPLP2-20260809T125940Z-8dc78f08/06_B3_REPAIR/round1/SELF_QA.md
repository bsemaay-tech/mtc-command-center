# SELF QA - B3-GAP-ENV Option 1 design repair, round 1

Subjects: `round1/RP1-B3.sh` (226 lines), `round1/RPD-VERIFY.sh` (169 lines).

```
03152789e7cc3deb5adff113f6a81bff3cdaf04ff4311730ab82d02d5d9622a7  RP1-B3.sh
610996deec81dc25ef7252b77a6a585779df16acb0ce9258a634e54bd08a98ba  RPD-VERIFY.sh
```

No remote host was contacted. Nothing outside `round1/` was written. Neither
block was run against `/etc/mtc-bridge`, `/opt/mtc-bridge` or any other target
path: the QA host is Windows/MSYS and has none of them, which is why the one
end-to-end run below FAILs at the release tree.

## 1. Environment

```
$ bash --version | head -1
GNU bash, version 5.2.37(1)-release (x86_64-pc-msys)
$ command -v shellcheck
(not installed - shellcheck was NOT run; see section 8)
```

## 2. `bash -n` evidence (required by the kickoff)

```
$ cd round1
$ bash -n RP1-B3.sh    ; echo "rc=$?"
rc=0
$ bash -n RPD-VERIFY.sh; echo "rc=$?"
rc=0
```

Re-run after the final edit of each file; both still rc=0. Encoding checks:

```
$ iconv -f ASCII -t ASCII <RP1-B3.sh    >/dev/null && echo ASCII_OK
ASCII_OK
$ iconv -f ASCII -t ASCII <RPD-VERIFY.sh >/dev/null && echo ASCII_OK
ASCII_OK
$ LC_ALL=C grep -c $'\r' RP1-B3.sh RPD-VERIFY.sh
RP1-B3.sh:0
RPD-VERIFY.sh:0
```

## 3. Method for the arm walk

Every arm below was driven through a harness that does **not** retype any
predicate: each function is extracted from the delivered file mechanically
(`awk 'index($0, fn "() {")==1 {f=1} f{print} f && /^\}/{exit}'`) and `eval`ed
under `set -Eeuo pipefail` with the real `b3_stop`/`b3_fail` (resp. `rpd_*`)
definitions, so the bytes exercised are the delivered bytes. Only `stat`, `grep`,
`id`, `mktemp` and `rp0_probe_path` are stubbed, which is what makes each error
class reachable on a host that has none of the real paths.

Result: **43 arms driven, 43 matched the expected rc, 0 mismatches.** Arms marked
`[real]` were produced by running the delivered file itself with no stubs. Arms
marked `[accepted]` are byte-identical to the adversarially accepted block and
were not re-driven here; they were verified identical by extraction and `diff`.

## 4. `RP1-B3.sh` - every FAIL and STOP arm

### 4.1 STOP arms (rc 3)

| Emitted string | Trigger | Evidence |
|---|---|---|
| `B3_STOP reason=rp0_lib_not_sourced predicate=rp0_probe_path` | RP0-LIB not sourced | `[real]` G4 |
| `B3_STOP reason=rp0_lib_not_sourced predicate=rp0_monotonic_ms` | RP0-LIB partially sourced | same construct, line 55 |
| `B3_STOP reason=uid_probe_failed` | `id -u` non-zero | B3 |
| `B3_STOP reason=group_probe_failed` | `id -G` non-zero (either call site) | B4, B11 |
| `B3_STOP reason=must_run_unprivileged uid=0` | caller is root | B1 |
| `B3_STOP reason=dir_gid_probe_failed path=/etc/mtc-bridge` | `stat -c '%g'` on CONF_DIR fails | B10 |
| `B3_STOP reason=caller_in_conf_dir_group path=/etc/mtc-bridge gid=0 caller_gids=[1000 0 27]` | caller is in CONF_DIR's group | B5, B8 (gid 10), B9 (gid 8001) |
| `B3_STOP reason=boundary_tempfile_failed path=/etc/mtc-bridge/mtc-bridge.env` | `mktemp` fails | A7 |
| `B3_STOP reason=conf_dir_search_permitted_name_absent path=/etc/mtc-bridge/mtc-bridge.env rc=1 expected=EACCES` | ENOENT, i.e. the search succeeded | A4 |
| `B3_STOP reason=boundary_probe_unclassified path=/etc/mtc-bridge/mtc-bridge.env rc=1 detail=stat: cannot statx '/etc/mtc-bridge/mtc-bridge.env': Input/output error` | any other error class | A5 |
| `B3_STOP reason=boundary_probe_unclassified path=/etc/mtc-bridge/mtc-bridge.env rc=4 detail=` | non-zero rc with EMPTY stderr - the "silence is not success" arm | A6 |
| `B3_STOP reason=mode_probe_failed path=<p>` | `stat %a` fails | `[accepted]` |
| `B3_STOP reason=owner_probe_failed path=<p>` | `stat %U:%G` fails | `[accepted]` |
| `B3_STOP reason=sweep_tempfile_failed root=<r>` | `mktemp` fails in the sweep | `[accepted]` |
| `B3_STOP reason=writable_inventory_failed root=<r> rc=<n> detail=<...> partial=[<...>]` | `find` non-zero | `[accepted]` |
| `B3_STOP reason=sweep_budget_exceeded root=<r> elapsed_s=<n> budget_s=120` | sweep over budget | `[accepted]` |
| `RP0_STOP reason=path_probe_error path=<p> rc=<n> detail=<...>` then rc 3 | propagated from `rp0_probe_path` via `|| exit 3` | library-emitted; this is the exact string the accepted block produced on the target |

### 4.2 FAIL arms (rc 1)

| Emitted string | Trigger | Evidence |
|---|---|---|
| `B3_FAIL reason=conf_dir_entry_permitted path=/etc/mtc-bridge/mtc-bridge.env stat=[regular file\|600\|root:root] expected=EACCES` | the boundary probe SUCCEEDED - directory more open than the accepted state | A1 |
| `B3_FAIL reason=missing path=/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b` | asserted path absent | `[real]` I1 |
| `B3_FAIL reason=canonical deployment path is a symlink kind=<k> path=<p>` | symlink at a canonical path | `[accepted]` |
| `B3_FAIL reason=unexpected object kind=<k> path=<p>` | socket/fifo/device etc. | `[accepted]` |
| `B3_FAIL reason=path=<p> mode=<m> expected=<want>` | mode drift | `[accepted]` |
| `B3_FAIL reason=path=<p> owner=<o> expected=<want>` | owner drift | `[accepted]` |
| `B3_FAIL reason=writable path inside immutable tree: <path>` | any write bit in either tree | `[accepted]` |

### 4.3 The one non-0/1/3 exit

`: "${B3_SWEEP_BUDGET_S:?...}"` (line 44) aborts with **rc 1** and writes its
message to stderr, not through `b3_fail`:

```
$ env -u B3_SWEEP_BUDGET_S bash RP1-B3.sh; echo rc=$?
RP1-B3.sh: line 44: B3_SWEEP_BUDGET_S: preregistered per-tree sweep budget in seconds is required
rc=1
```

This is the accepted block's own behaviour, preserved verbatim as the kickoff
requires. Disclosed as open item O2 in DESIGN_NOTES.md: a missing operator input
is arguably COULD-NOT-EVALUATE (rc 3), not deviant host state (rc 1). Note the
RP0-BOOTSTRAP `exec > "$leaf" 2>&1` means the message does still reach the
evidence leaf; only the rc classification is at issue.

### 4.4 Pass-arm output, for completeness

```
B3_identity uid=1000 gids=[1000 4 27]
B3_not_in_conf_dir_group path=/etc/mtc-bridge gid=0
B3_conf_dir_opaque_to_operator path=/etc/mtc-bridge/mtc-bridge.env outcome=EACCES rc=1
B3_conf_dir_opaque_to_operator path=/etc/mtc-bridge/.b3-boundary-probe-absent-name outcome=EACCES rc=1
B3_deferred check=env_file_mode_owner path=/etc/mtc-bridge/mtc-bridge.env to=RPD-VERIFY reason=conf_dir_not_searchable_unprivileged
B3_claim scope=unprivileged_only deferred=3 conf_dir=opaque_to_operator
B3 PASS
```

`[real]` end-to-end run on the QA host, RP0-LIB sourced, `B3_SWEEP_BUDGET_S=120`:

```
rc=1
B3_SECTION header candidate=2ce41e34bceb599d80af24c5c33d835820ec321b
B3_identity uid=4096 gids=[4096]
B3_SECTION release_tree
B3_FAIL reason=missing path=/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b
```

Correct: the identity guard passed (uid != 0, not in any CONF_DIR group), then the
first asserted path is genuinely absent on this host, so the block FAILed closed
and stopped. It never reached the boundary section, and it never touched a target.

## 5. `RPD-VERIFY.sh` - every FAIL and STOP arm

### 5.1 STOP arms (rc 3)

| Emitted string | Trigger | Evidence |
|---|---|---|
| `RPD_STOP reason=input_missing name=RPD_CANDIDATE_SHA detail=preregistered candidate release sha, 40 lowercase hex, never derived here` | input unset or empty | `[real]` G2, H1, H3 |
| `RPD_STOP reason=input_missing name=RPD_RELEASE_MANIFEST_SHA256 detail=preregistered accepted RELEASE_SHA256SUMS sha256, 64 lowercase hex, never derived here` | input unset or empty | `[real]` H2 |
| `RPD_STOP reason=rp0_lib_not_sourced predicate=rp0_probe_path` | RP0-LIB not sourced | `[real]` G3, H4 |
| `RPD_STOP reason=uid_probe_failed` | `id -u` non-zero | line 72 |
| `RPD_STOP reason=must_run_as_root uid=4096` | not root - never a silent skip | `[real]` H5 |
| `RPD_STOP reason=input_charset name=RPD_CANDIDATE_SHA expected=lowercase_hex` | uppercase, newline, CR, quote, any non `[0-9a-f]` | C3, C4, C5, C6 |
| `RPD_STOP reason=input_length name=RPD_CANDIDATE_SHA len=8 expected=40` | wrong width | C7, C8 (64-in-40 slot) |
| `RPD_STOP reason=mode_probe_failed path=/etc/mtc-bridge/mtc-bridge.env` | `stat %a` fails | F8 |
| `RPD_STOP reason=owner_probe_failed path=/etc/mtc-bridge/mtc-bridge.env` | `stat %U:%G` fails | F9 |
| `RPD_STOP reason=install_manifest_unreadable path=/etc/mtc-bridge/install_manifest.json grep_rc=2` | `grep` rc > 1 on EITHER binding test - never read as "not bound" | E4 (first test), E5 (second test) |
| `RP0_STOP reason=...` then rc 3 | propagated from `rp0_probe_path` via `|| exit 3` | E7, F10 |

`[real]` non-root run with RP0-LIB actually sourced:

```
$ env RPD_CANDIDATE_SHA=2ce41e34... RPD_RELEASE_MANIFEST_SHA256=edb0fd34... \
    bash -c '. RP0-LIB.sh; . RPD-VERIFY.sh'
rc=3
RPD_SECTION identity
RPD_STOP reason=must_run_as_root uid=4096
```

### 5.2 FAIL arms (rc 1)

| Emitted string | Trigger | Evidence |
|---|---|---|
| `RPD_FAIL reason=missing path=/etc/mtc-bridge/mtc-bridge.env` | env file absent - this is where the section 8 #4 `bridge.env` naming risk finally becomes answerable | F4 |
| `RPD_FAIL reason=expected a regular file kind=dir path=<p>` | a directory where a file is required | F5 |
| `RPD_FAIL reason=canonical deployment path is a symlink kind=link_dangling path=<p>` | symlink at either canonical path (live or dangling) | F6 |
| `RPD_FAIL reason=unexpected object kind=other path=<p>` | any other object kind | F7 |
| `RPD_FAIL reason=path=/etc/mtc-bridge/mtc-bridge.env mode=640 expected=600` | mode drift | F2 |
| `RPD_FAIL reason=path=/etc/mtc-bridge/mtc-bridge.env owner=mtc-bridge:mtc-bridge expected=root:root` | owner drift | F3 |
| `RPD_FAIL reason=install manifest kind=link_live path=/etc/mtc-bridge/install_manifest.json` | manifest is not a regular file | E6 |
| `RPD_FAIL reason=install manifest does not bind release_sha` | `grep` rc 1 on the candidate binding | E2 |
| `RPD_FAIL reason=install manifest does not bind release_manifest_sha256` | `grep` rc 1 on the manifest-sha binding | E3 |

### 5.3 Pass-arm output

```
RPD_identity uid=0
RPD_input name=RPD_CANDIDATE_SHA value=2ce41e34bceb599d80af24c5c33d835820ec321b
RPD_input name=RPD_RELEASE_MANIFEST_SHA256 value=edb0fd34e3d976b872868cc3dfbf745cbc4b08f6c4c5d21b8d6cda47a3e20d26
RPD_stat path=/etc/mtc-bridge/mtc-bridge.env owner=root:root mode=600
RPD_manifest_binding path=/etc/mtc-bridge/install_manifest.json bound=both
RPD PASS
```

## 6. Finding substantiated during QA: multi-line `grep -F` is an alternation

The `rpd_require_hex` guard exists because of this. Against a manifest-shaped
fixture:

```
{
  "release_sha": "2ce41e34bceb599d80af24c5c33d835820ec321b",
  "release_manifest_sha256": "edb0fd34...0d26"
}
```

with a value carrying an embedded newline (`deadbeef` LF `sha`), the pattern
`"release_sha": "deadbeef\nsha"` is treated by `grep -F` as the two alternatives
`"release_sha": "deadbeef` and `sha"`; the second matches `..._sha":` and:

```
$ LC_ALL=C grep -qsF -- "\"release_sha\": \"$badval\"" "$mf"; echo rc=$?
rc=0        <== a WRONG sha reported as bound
```

Control: a clean but wrong 40-hex value returns rc 1, correctly. So the hazard is
specifically a value carrying a line break, which `rpd_require_hex` rejects
(C4/C5) before either `grep` runs. The first version of this test was
mis-constructed and did NOT reproduce the hazard; it was rebuilt until the
mechanism was demonstrated rather than asserted.

## 7. No file content is printed and no credential value is read

Audited line by line, both blocks.

1. **Every output statement is a `printf` with a fixed ASCII format string.**
   There is no `cat`, `head`, `tail`, `sed`, `awk`, `od`, `strings`, no `echo` of
   a file, and no command substitution whose value comes from a file's CONTENT.
   The only values interpolated into output are: a path literal from this block,
   a `stat` metadata field (`%F`, `%a`, `%U:%G`, `%g`), a numeric id from
   `id -u`/`id -G`, a `find` PATH (never file bytes), an elapsed-seconds integer,
   an rc, a preregistered input, and a `stat`/`find` STDERR string.
2. **The env file is never opened.** In `RP1-B3.sh` the only reference to
   `ENV_FILE` is as an argument to `b3_assert_conf_dir_opaque`, which runs
   exactly one `stat` on it - a metadata syscall that the design EXPECTS to be
   refused. In `RPD-VERIFY.sh` the only references are `stat -c '%a'` and
   `stat -c '%U:%G'`. There is no `grep`, no read, no redirection from it in
   either block.
3. **The manifest is read only by silent `grep -qsF`.** `-q` suppresses all
   matched output and `-s` suppresses error messages; the only thing derived from
   the file is `grep`'s rc, and the only manifest-related output line is
   `RPD_manifest_binding path=<p> bound=both`. No manifest bytes can reach the
   evidence log. Verified: `RPD-VERIFY.sh` invokes `grep` on exactly two lines,
   132 and 139, both `LC_ALL=C grep -qsF`; its other `grep` mentions are comments
   (16, 79, 84, 125) and two `grep_rc=` reason strings (136, 143). The string
   `grep` does not appear in `RP1-B3.sh` at all (zero occurrences, comments
   included).
4. **The two values printed verbatim are operator inputs, not host reads.**
   `RPD_input` prints `RPD_CANDIDATE_SHA` and `RPD_RELEASE_MANIFEST_SHA256`, both
   supplied from preregistration and both format-proven lowercase hex of the
   preregistered width BEFORE printing. Neither is derived from the host, and
   both are already recorded in `PREREGISTRATION.md` section 2. On the two
   rejection arms the value is deliberately NOT printed (only its name and
   length), so a mis-plumbed variable holding something sensitive cannot be
   echoed into an evidence log.
5. **Nothing reads a credential.** Neither block references a token, key,
   password, `Authorization`, `/api/arm`, an exchange, an order, TESTNET or
   mainnet. Command inventory across both files: `stat`, `find`, `grep -qsF`
   (RPD only), `id`, `mktemp`, `tr`, `rm -f` (temp file only), `printf`,
   `command -v`. Scanned for and confirmed absent: `chmod`, `chown`, `chgrp`,
   `setfacl`, `sudo`, `mv`, `cp`, `ln`, `mkdir`, `touch`, `tee`, `dd`,
   `truncate`, `sed -i`, `systemctl start|stop|restart|enable|disable|mask`,
   `curl`, `wget`, `ssh`, `scp`, `nc`, `openssl`, `pip`, `python`.
6. **Only two file-writing redirections exist**, both `2>"$errf"` onto a
   `mktemp` file that is `rm -f`'d: `RP1-B3.sh:87` (the accepted sweep) and
   `RP1-B3.sh:174` (the boundary probe). `RPD-VERIFY.sh` has none of its own; it
   inherits one through `rp0_probe_path`. Disclosed as open item O3 rather than
   claiming "no writes at all". No `>` or `>>` targets any verified path.
7. **`RPD-VERIFY.sh` mutates nothing.** No write to `ENV_FILE` or
   `INSTALL_MANIFEST`, no mode/owner change, no service or network call, no
   `sudo`, no group or ACL change. Its root requirement is used solely to make
   two `stat` calls and two silent `grep` calls possible.

## 8. Known gaps in this QA

Stated so the re-audit does not have to find them.

1. **No Linux host.** The genuine EACCES pass arm could not be produced by a real
   kernel here: MSYS cannot reproduce `0750 root:root` semantics. The EACCES,
   ENOENT and other-error arms were driven through a stubbed `stat` that emits
   the real `coreutils` message shapes (`stat: cannot statx '<p>': Permission
   denied`, `... : No such file or directory`). The classifier matches on those
   substrings, so a different `stat` implementation or a translated locale would
   land in the `boundary_probe_unclassified` STOP arm - fail-closed, but a real
   first-run risk. `LC_ALL=C` is set on the call, which is what makes the
   message shape predictable.
2. **`shellcheck` was not run** (not installed on this host). Only `bash -n`
   evidence is provided, as the kickoff required.
3. **Arms marked `[accepted]` were not re-driven.** They are byte-identical to
   the adversarially accepted block - verified by extraction plus `diff`
   (`b3_assert_mode_owner` 15 lines, `b3_assert_no_writable_paths` 17 lines) -
   so their falsifications stand from the accepted audit, not from this QA.
4. **`rp0_probe_path` was stubbed** in the E and F arms. Its own three-outcome
   behaviour is accepted-block property, unmodified here; arms E7/F10 show only
   that a rc-3 propagation exits 3 with no reason string of its own (the string
   comes from the library, on stderr).
5. **`RPD-VERIFY.sh` has never run as root.** Its PASS path is stub-exercised
   only. Treat the first deploy-time run as a first run (open item O7).
6. **The section 8 #4 naming risk remains unresolved** and cannot be resolved by
   any unprivileged block, by construction of the EACCES denial.
