# SELF QA - B3-GAP-ENV Option 1 design repair, round 4 (BOUNDED CLOSURE)

Subjects: `round4/RP1-B3.sh` (662 lines), `round4/RPD-VERIFY.sh` (775 lines).

```
6f3ea022b68d80a552c4ebcb771bbb2a707bdab46a383d605ffc5b88b884becc  RP1-B3.sh
3b9e78e87cecdc10ab1a10d14e79dbff530968e4075277117743c88976fa813c  RPD-VERIFY.sh
```

Round 4 is a bounded closure of the TWO surviving REQUIRED findings of
`audit3/AUDIT3_REPORT.md`. It changes exactly two things: the mount-reader
read-error arm in both blocks (finding 1), and this file (finding 2). Everything
audit 3 verified CLOSED is byte-identical to round 3; the executable diff
`round3` -> `round4` is confined to `b3_assert_no_mount_at_or_under` and
`rpd_assert_no_mount_at_or_under`, plus the comment block above each.

No remote host was contacted. Nothing outside `round4/` was written inside the
repository; the harness, its stubs and its fixtures live in a session scratch
directory outside the repository tree. Neither block was run against
`/etc/mtc-bridge`, `/opt/mtc-bridge` or any other target path: the QA host is
Windows/MSYS and has none of them.

**Three textual substitutions are applied to every transcript in this file, and
only these three. Nothing else in any recorded output is altered.**

| Rendered as | Actual string |
|---|---|
| `$QA` | `/c/Users/BARSEM~1/AppData/Local/Temp/claude/C--LAB-Tradingview-LAB-CLEAN/351bc794-7e80-44b9-b3cf-bfe25dca1adc/scratchpad/r4` |
| `$QAW` | the same directory in the Windows spelling `cygpath -m` produces, `C:/Users/BARSEM~1/...`, which is the form the QA host's python3 can open |
| `$QA_PY` | the QA host's `python3` absolute path. It contains a non-ASCII user-directory component, so it is NOT reproduced here; this file is required to be ASCII. It is used only as a repointed value of the delivered `PYTHON_BIN` literal, and every arm that uses it is counted in category B. |

The substitution is mechanical, not editorial: every arm below is run through

```
emit() { local s="$1"; s="${s//$QA_PY/\$QA_PY}"; s="${s//$QAW/\$QAW}"; s="${s//$QA/\$QA}"; printf '%s\n' "$s"; }
```

so the transcripts are the process output with those three strings replaced and
nothing else touched.

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

Same host as round 3. The last line matters twice. It is why the delivered
`PYTHON_BIN` literal has to be repointed for the functional manifest arms, and it
is also why the `manifest_tool_absent` STOP can be driven for real, with no
substitution at all (arm `TP1`).

## 2. `bash -n`, encoding and deliverable-set evidence

```
$ cd round4
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
6f3ea022b68d80a552c4ebcb771bbb2a707bdab46a383d605ffc5b88b884becc *RP1-B3.sh
3b9e78e87cecdc10ab1a10d14e79dbff530968e4075277117743c88976fa813c *RPD-VERIFY.sh
$ wc -l RP1-B3.sh RPD-VERIFY.sh
  662 RP1-B3.sh
  775 RPD-VERIFY.sh
```

The two hashes above are the hashes of the bytes every round-4 arm below was
extracted from.

The deliverable set is exactly four files. `find round4 -mindepth 1` was checked
after the last write and lists only `DESIGN_NOTES.md`, `RP1-B3.sh`,
`RPD-VERIFY.sh` and `SELF_QA.md` - no dot-directory, no cache, no editor or tool
artifact. Nothing in this round created one.

### 2.1 The whole executable delta, round 3 to round 4

Both files carry the same change. `diff -u round3 round4`, executable hunk only
(the comment hunk above each function is shown in DESIGN_NOTES section 10):

```
@@ -434,7 +453,13 @@
         f1=""; f2=""; f3=""; f4=""; f5=""; f6=""; extra=""; rrc=0
         IFS=' ' read -r f1 f2 f3 f4 f5 f6 extra <&9 || rrc=$?
         if [ "$rrc" -ne 0 ]; then
-            if [ -z "$f1$f2$f3$f4$f5$f6$extra" ]; then break; fi
+            if [ -z "$f1$f2$f3$f4$f5$f6$extra" ]; then
+                if [ "$records" -eq 0 ]; then
+                    exec 9<&-
+                    b3_stop "mount_table_read_error path=$MOUNTS records=$records read_rc=$rrc detail=nonzero_read_populated_no_field_and_consumed_no_record"
+                fi
+                break
+            fi
             truncated=1
         fi
         records=$(( records + 1 ))
```

`RPD-VERIFY.sh` is the identical hunk with `rpd_stop` in place of `b3_stop`. No
other executable line in either file differs from round 3.

## 3. Method, and the three exact counts (A2-F7 / audit-3 finding 2)

Every arm is driven against DELIVERED BYTES. No predicate is retyped: each
function is extracted mechanically from the delivered file and `eval`ed under
`set -Eeuo pipefail` together with the delivered `..._stop`, `..._fail`,
`..._on_err` + `ERR` trap and `..._sanitize`.

```
exfn() { awk -v fn="$2" 'index($0, fn "() {")==1 {f=1} f{print} f && /^\}$/{exit}' "$1"; }
ex1()  { LC_ALL=C grep -m1 "^$2() {" "$1"; }   # one-line definitions
exc()  { LC_ALL=C grep -m1 "^$2="    "$1"; }   # constants
```

The six preludes, used verbatim throughout, exactly as executed:

```
pre2b() { printf 'set -Eeuo pipefail\nexport LC_ALL=C\nB3_KIND=""\nB3_SAFE=""\n'
          ex1 "$R2/RP1-B3.sh" b3_stop; ex1 "$R2/RP1-B3.sh" b3_fail
          exfn "$R2/RP1-B3.sh" b3_on_err; printf "trap 'b3_on_err' ERR\n"
          exfn "$R2/RP1-B3.sh" b3_sanitize; }
pre2r() { printf 'set -Eeuo pipefail\nexport LC_ALL=C\nRPD_KIND=""\nRPD_SAFE=""\n'
          ex1 "$R2/RPD-VERIFY.sh" rpd_stop; ex1 "$R2/RPD-VERIFY.sh" rpd_fail
          exfn "$R2/RPD-VERIFY.sh" rpd_on_err; printf "trap 'rpd_on_err' ERR\n"
          exfn "$R2/RPD-VERIFY.sh" rpd_sanitize; }
pre3b() { printf 'set -Eeuo pipefail\nexport LC_ALL=C\nB3_KIND=""\nB3_SAFE=""\nB3_COUNT=0\nB3_SHAPE=""\n'
          ex1 "$R3/RP1-B3.sh" b3_stop; ex1 "$R3/RP1-B3.sh" b3_fail
          exfn "$R3/RP1-B3.sh" b3_on_err; printf "trap 'b3_on_err' ERR\n"
          exfn "$R3/RP1-B3.sh" b3_sanitize; }
pre3r() { printf 'set -Eeuo pipefail\nexport LC_ALL=C\nunset CDPATH\nRPD_KIND=""\nRPD_SAFE=""\n'
          ex1 "$R3/RPD-VERIFY.sh" rpd_stop; ex1 "$R3/RPD-VERIFY.sh" rpd_fail
          exfn "$R3/RPD-VERIFY.sh" rpd_on_err; printf "trap 'rpd_on_err' ERR\n"
          exfn "$R3/RPD-VERIFY.sh" rpd_sanitize; }
pre4b() { printf 'set -Eeuo pipefail\nexport LC_ALL=C\nB3_KIND=""\nB3_SAFE=""\nB3_COUNT=0\nB3_SHAPE=""\n'
          ex1 "$R4/RP1-B3.sh" b3_stop; ex1 "$R4/RP1-B3.sh" b3_fail
          exfn "$R4/RP1-B3.sh" b3_on_err; printf "trap 'b3_on_err' ERR\n"
          exfn "$R4/RP1-B3.sh" b3_sanitize; }
pre4r() { printf 'set -Eeuo pipefail\nexport LC_ALL=C\nunset CDPATH\nRPD_KIND=""\nRPD_SAFE=""\n'
          ex1 "$R4/RPD-VERIFY.sh" rpd_stop; ex1 "$R4/RPD-VERIFY.sh" rpd_fail
          exfn "$R4/RPD-VERIFY.sh" rpd_on_err; printf "trap 'rpd_on_err' ERR\n"
          exfn "$R4/RPD-VERIFY.sh" rpd_sanitize; }
```

### The three counts

Counted by the audit's own rule: **category B is any arm with a stubbed command
OR a repointed path literal**, with no exceptions - including both mount
sections.

| Category | Count |
|---|---:|
| A. Delivered-code arms run with NO stubbed command and NO repointed literal | **43** |
| B. Delivered-code arms run with at least one stubbed command or repointed path literal | **119** |
| C. Inherited RP0-LIB arms NOT re-run (not driven, not claimed as driven) | **3** |

Per file: `RP1-B3.sh` = **21 A / 64 B** (85 runs). `RPD-VERIFY.sh` =
**22 A / 55 B** (77 runs). Total driven: **162 runs**, 162 matched the designed
outcome, **0 mismatches**.

Round 3 was 43 A / 115 B. The delta is exactly **+4 B**: the new read-error arm,
two fixtures (a directory and a zero-byte source) times two blocks. No other arm
count changed, because no other predicate changed.

Every displayed subcount below is exact and reconciles to these totals:

```
RP1 A = 6.1 (5) + 6.2 (5) + 6.3 (7) + 6.7 (3) + 6.8 real-coreutils (1)      = 21
RP1 B = 6.4 (10) + 6.5 (18) + 6.6 (15) + 6.8 (11) + 6.9 (10)                = 64
RPD A = item-2 input/missing arms (11) + 6.10 A arms (11)                   = 22
RPD B = attestation (5) + 6.9 mount (10) + pinned-tool (4) + 6.11 (10)
        + 6.12 (15) + 6.13 (11)                                             = 55
```

The section 6.13 label is `(11)` in round 4. Audit-3 finding 2 was right: round 3
headed that section `(9)` while its own text enumerates 3 item-4 arms, 2 item-1
arms and 6 table arms. 11 is the number the RPD B subtotal was always computed
with; only the label was wrong, and it is now the real count.

### What was driven against ROUND-4 bytes in this round, and what was not

This is the honesty statement audit-3 finding 2 exists to force. **71 of the 162
arms were re-driven in this round against round-4 bytes.** The other **91 were
driven in round 3 and are carried forward, not re-run and not re-claimed as
freshly driven.** That is sound only because it is checkable: section 2.1 shows
that the entire executable delta is inside `*_assert_no_mount_at_or_under`, so
every carried-forward arm executes bytes that are identical to the bytes round 3
drove. Any arm that touches the changed function was re-run.

| Section | Arms | Driven vs round-4 bytes this round | Carried forward |
|---|---:|---:|---:|
| 6.1 `RP1-B3.sh` whole file | 5 | 4 (`R1`-`R4`) | 1 (`R5`) |
| 6.2 new-input guards | 5 | 5 | 0 |
| 6.3 sanitize / count_substr | 7 | 0 | 7 |
| 6.4 `b3_probe_kind` | 10 | 0 | 10 |
| 6.5 mode_owner + sweep | 18 | 4 (the section 5.3 arms) | 14 |
| 6.6 identity/ns/group/canonical | 15 | 0 | 15 |
| 6.7 access(2) + ERR trap | 3 | 0 | 3 |
| 6.8 boundary probe | 12 | 12 | 0 |
| 6.9 mount reader, both blocks | 20 | 20 | 0 |
| 6.10 RPD whole file / hex / pins | 16 | 4 (`RD1`, `RD3`, `TP1`, `TP2`) | 12 |
| 6.11 `rpd_probe_kind` | 10 | 0 | 10 |
| 6.12 conf_dir + regular_mode_owner | 15 | 0 | 15 |
| 6.13 manifest binding | 11 | 6 | 5 |
| attestation + item-2 input arms | 16 | 16 | 0 |
| **Total** | **162** | **71** | **91** |

Reported separately, because they are ROUND-2 or ROUND-3 code and belong in no
round-4 category: **29 RED baseline runs** - 25 against `round2/` (items 1-6, the
same 25 round 3 reported) and **4 against `round3/`**, which are the new
read-error arm's RED side. All 29 are in section 5.

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
3. `open_kind_not_regular` (RPD-VERIFY manifest reader) - needs a non-regular
   object that `open` succeeds on.
4. A `read_error` raised mid-read rather than at open (RPD-VERIFY manifest
   reader).
5. NEW, and named rather than hidden: a read(2) failure raised MID-TABLE by the
   MOUNT reader, after at least one well-formed record. Section 8 gap 10 states
   why no arm can exist for it in a shell: `read` returns 1 for both end of input
   and a read error, so that case is indistinguishable from a clean EOF at the
   shell level. The round-4 fix closes the case that IS distinguishable - a
   nonzero read that populated nothing and consumed no record - and claims
   nothing about the other.

### 3.1 Delivered-code defects found by this round's QA

None. The two round-4 code hunks passed every arm on the first run. The one
round-3 defect this QA process found (`rpd_require_ns_token`, a `local` that
expanded `$kind` before assigning it) was fixed in round 3 and is unchanged here;
its re-run is arm `I2-G1` in section 5.2.

### 3.2 Harness defects, disclosed rather than hidden

1. The first attempt at the section 5.3 missing-input arms was written
   `env B3_SWEEP_BUDGET_S=120 -u B3_SVC_UID ... bash RP1-B3.sh`. GNU `env` takes
   options only BEFORE the first assignment, so `-u` was parsed as the command
   name and the runs returned `env: '-u': No such file or directory`, rc 127,
   with no B3 output at all. Rebuilt as
   `env -u B3_SVC_UID B3_SWEEP_BUDGET_S=120 ...`. The defective runs are not
   counted; the rebuilt runs are the ones recorded in 5.3.

## 4. QA substitutions, in full

Every command in section 5 is executable as written after these declarations,
which are the ones the harness used:

```
B="<repo>/MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/06_B3_REPAIR"
R2="$B/round2"; R3="$B/round3"; R4="$B/round4"
QA=<the scratch directory rendered as $QA above>
QAW="$(cygpath -m "$QA")"
QA_PY="$(command -v python3)"
GOODREL="2ce41e34bceb599d80af24c5c33d835820ec321b"
GOODMAN="edb0fd34e3d976b872868cc3dfbf745cbc4b08f6c4c5d21b8d6cda47a3e20d26"
arm() { local out rc=0; out="$(bash "$QA/arm.sh" 2>&1)" || rc=$?; emit "$out"; printf 'RC=%s\n' "$rc"; }
```

Only these four kinds of substitution are used, and every arm that uses one is
category B.

1. **`/proc/self/uid_map`** is a literal in the delivered attestation function and
   does not exist on MSYS. For the item-2 arms the extracted function body had
   exactly that one literal replaced with a fixture path by a single `sed`
   substitution; every other byte is delivered.
2. **`MOUNTS`** is repointed to a fixture path for every mount arm (both blocks).
   The function bodies are delivered bytes.
3. **`PYTHON_BIN`** is repointed to `$QA_PY` for the functional manifest arms, and
   `rpd_require_pinned_tool` is replaced by this one-line stub in those arms
   only, because the QA host cannot present a `0:0`-owned interpreter:

   ```
   pinstub() { printf '%s\n' 'rpd_require_pinned_tool() { printf '"'"'RPD_tool name=%s path=%s mode=755 owner_numeric=0:0 resolution=pinned_absolute\n'"'"' "$1" "$2"; }'; }
   ```

   The pinned-tool predicate itself is driven separately, unsubstituted, in
   section 5.1.
4. **Stubbed producers** (`stat`, `readlink`) on a PATH-prepended directory, for
   arms whose outcome depends on a value the QA host cannot produce. The three
   stubs are listed in 4.1.

Two QA-host facts shape the manifest arms and are stated so no reader mistakes
them for delivered behaviour: the QA `python3` renders POSIX metadata as mode
`0666`, uid `0`, gid `0`, so those arms pass `0666` where the deploy-time call
passes `0640`; and it opens Windows-form paths, so fixture paths are given as
`$QAW/...`.

### 4.1 The three stubs and the fixtures, verbatim

`$QA/fix3/stub/stat` (item 3):

```
#!/bin/sh
fmt=""
while [ $# -gt 0 ]; do
  case "$1" in
    -c) fmt="$2"; shift 2 ;;
    -L) shift ;;
    --) shift; break ;;
    *)  break ;;
  esac
done
case "$fmt" in
  '%F')     echo "${STUB_KIND:-directory}" ;;
  '%a')     echo "${STUB_MODE:-750}" ;;
  '%u:%g')  echo "${STUB_OWN:-999:999}" ;;
  '%U:%G')  echo "${STUB_NAME:-mtc-bridge:mtc-bridge}" ;;
  *) echo "stub-stat: unhandled format [$fmt]" >&2; exit 1 ;;
esac
exit 0
```

`$QA/fix3/stubdir/stat` (item 6) emits one diagnostic shape per `STUB_CASE` on
stderr and exits 1, except `empty` (exit 4, no stderr) and `ok` (prints
`regular file|600|0:0`, exit 0):

```
#!/bin/sh
for a in "$@"; do p="$a"; done
case "${STUB_CASE:-}" in
  twoline)   printf "stat: cannot stat '%s': Permission denied\nstat: cannot stat '%s': No such file or directory\n" "$p" "$p" >&2; exit 1 ;;
  oneline2)  printf "stat: cannot stat '%s': Permission denied (No such file or directory)\n" "$p" >&2; exit 1 ;;
  wrapper)   printf "mtcwrap: stat failed on %s: Permission denied\n" "$p" >&2; exit 1 ;;
  wrongpath) printf "stat: cannot stat '/some/other/path': Permission denied\n" >&2; exit 1 ;;
  eacces)    printf "stat: cannot stat '%s': Permission denied\n" "$p" >&2; exit 1 ;;
  statx)     printf "stat: cannot statx '%s': Permission denied\n" "$p" >&2; exit 1 ;;
  enoent)    printf "stat: cannot stat '%s': No such file or directory\n" "$p" >&2; exit 1 ;;
  eio)       printf "stat: cannot stat '%s': Input/output error\n" "$p" >&2; exit 1 ;;
  empty)     exit 4 ;;
  nonprint)  printf "stat: cannot stat '%s': Permission denied\a\n" "$p" >&2; exit 1 ;;
  ok)        printf 'regular file|600|0:0\n'; exit 0 ;;
esac
exit 9
```

`$QA/fix2/stub/readlink` answers `/proc/self/ns/*` and `/proc/1/ns/*` from
`STUB_SELF_U`, `STUB_SELF_M`, `STUB_INIT_U`, `STUB_INIT_M`; `$QA/fix2/stub/stat`
answers `-c '%d:%i'` from `STUB_ROOTFS`. Both exit 1 / 1 on anything else.

The mount fixtures, exactly as built:

```
M="$QA/fix2/mounts"; mkdir -p "$M/adir"
printf 'sysfs /sys sysfs rw 0 0\nproc /proc proc rw 0 0\ntmpfs /run tmpfs rw 0 0\n' >"$M/clean"
printf 'sysfs /sys sysfs rw 0 0\ntmpfs /etc/mtc-bridgeX tmpfs rw 0 0\n'            >"$M/sibling"
printf 'tmpfs /etc/mtc-bridge tmpfs rw 0 0\n'                                      >"$M/at"
printf 'tmpfs /etc/mtc-bridge/sub tmpfs rw 0 0\n'                                  >"$M/under"
printf 'src /etc/mtc-bridge ext4 rw 0 0'                                           >"$M/nonl"
printf 'sysfs /sys sysfs rw 0 0\nsrc /etc/mtc-bri\n'                               >"$M/short"
printf 'sysfs /sys sysfs rw 0 0\nsrc /etc/mtc-bridge ext4 rw 0 0 extra\n'          >"$M/wide"
: >"$M/empty"
```

`$M/nonl` is written with no terminating newline, deliberately. `$M/adir` is a
DIRECTORY - the audit's own read-error fixture. `$M/empty` is a zero-byte file.

The manifest fixtures:

```
printf '%s\n' 'THIS IS NOT JSON AND BINDS NOTHING' >"$QA/fix1/wrong.json"
printf '{"release_sha": "%s", "release_manifest_sha256": "%s"}\n' "$GOODREL" "$GOODMAN" >"$QA/fix1/good.json"
printf '{"release_sha": "%s", "release_manifest_sha256": "%s", "extra": NaN}\n'       "$GOODREL" "$GOODMAN" >"$QA/fix1/nan.json"
printf '{"release_sha": "%s", "release_manifest_sha256": "%s", "extra": Infinity}\n'  "$GOODREL" "$GOODMAN" >"$QA/fix1/inf.json"
printf '{"release_sha": "%s", "release_manifest_sha256": "%s", "extra": -Infinity}\n' "$GOODREL" "$GOODMAN" >"$QA/fix1/neginf.json"
cat >"$QA/fix1/shadow/json.py" <<EOF
def loads(*a, **k):
    return {"release_sha": "$GOODREL",
            "release_manifest_sha256": "$GOODMAN"}
EOF
cp "$QA/fix1/shadow/json.py" "$QA/fix1/cwdshadow/json.py"
```

## 5. D026 closure evidence: exact command, real RED, real GREEN

For every final-list item 1-6. RED is ROUND-2 delivered code (or ROUND-3 code
where the defect is the one round 4 closes); GREEN is ROUND-4 delivered code.
Both sides of every pair were run on this host in this round, against the same
fixture, in the same shell session. **Every command below is the exact command
that was executed** - no prose stands in for one, and no GREEN is described as
"the RED command with X swapped".

### 5.1 Item 1 (A2-F1) - interpreter isolation

**Command (RED), PYTHONPATH shadow:**

```
{ pre2r
  exc "$R2/RPD-VERIFY.sh" ROOT_OWNER; exc "$R2/RPD-VERIFY.sh" MANIFEST_MAX_BYTES
  exfn "$R2/RPD-VERIFY.sh" rpd_assert_manifest_binding
  printf 'rpd_assert_manifest_binding "%s" "%s" "%s" 0666\n' \
      "$QAW/fix1/wrong.json" "$GOODREL" "$GOODMAN"; } >"$QA/arm.sh"
PYTHONPATH="$QAW/fix1/shadow" bash "$QA/arm.sh"
```

```
RPD_manifest_binding path=$QAW/fix1/wrong.json bound=both parser=python3_json_structural keys=top_level_exact
RC=0
```

**Command (GREEN), PYTHONPATH shadow:**

```
{ pre4r
  exc "$R4/RPD-VERIFY.sh" ROOT_OWNER; exc "$R4/RPD-VERIFY.sh" MANIFEST_MAX_BYTES
  exc "$R4/RPD-VERIFY.sh" ENV_BIN; exc "$R4/RPD-VERIFY.sh" CHILD_PATH
  exc "$R4/RPD-VERIFY.sh" CHILD_CWD
  printf 'PYTHON_BIN="%s"\n' "$QA_PY"
  pinstub
  exfn "$R4/RPD-VERIFY.sh" rpd_assert_manifest_binding
  printf 'rpd_assert_manifest_binding "%s" "%s" "%s" 0666\n' \
      "$QAW/fix1/wrong.json" "$GOODREL" "$GOODMAN"; } >"$QA/arm.sh"
PYTHONPATH="$QAW/fix1/shadow" bash "$QA/arm.sh"
```

```
RPD_tool name=env path=/usr/bin/env mode=755 owner_numeric=0:0 resolution=pinned_absolute
RPD_tool name=python3 path=$QA_PY mode=755 owner_numeric=0:0 resolution=pinned_absolute
RPD_STOP reason=install_manifest_unparsable path=$QAW/fix1/wrong.json
RC=3
```

**Command (RED), cwd shadow** - the round-2 arm script, executed from the
poisoned directory:

```
cp "$QA/arm.sh" "$QA/fix1/cwdshadow/arm.sh"
( cd "$QA/fix1/cwdshadow" && bash ./arm.sh )
```

```
RPD_manifest_binding path=$QAW/fix1/wrong.json bound=both parser=python3_json_structural keys=top_level_exact
RC=0
```

**Command (GREEN), cwd shadow** - the round-4 arm script built exactly as in the
GREEN command above, then:

```
cp "$QA/arm.sh" "$QA/fix1/cwdshadow/arm.sh"
( cd "$QA/fix1/cwdshadow" && bash ./arm.sh )
```

```
RPD_tool name=env path=/usr/bin/env mode=755 owner_numeric=0:0 resolution=pinned_absolute
RPD_tool name=python3 path=$QA_PY mode=755 owner_numeric=0:0 resolution=pinned_absolute
RPD_STOP reason=install_manifest_unparsable path=$QAW/fix1/wrong.json
RC=3
```

Both hijack shapes are closed, and the GREEN result is the truth about the file:
it is not JSON.

**The pinned-tool predicate itself, unsubstituted** (category A). Command:

```
{ pre4r; exfn "$R4/RPD-VERIFY.sh" rpd_probe_kind; exc "$R4/RPD-VERIFY.sh" ROOT_OWNER
  exc "$R4/RPD-VERIFY.sh" PYTHON_BIN; exc "$R4/RPD-VERIFY.sh" ENV_BIN
  exfn "$R4/RPD-VERIFY.sh" rpd_require_pinned_tool
  printf 'rpd_require_pinned_tool python3 "$PYTHON_BIN"\n'; } >"$QA/arm.sh"
arm
```

```
RPD_STOP reason=manifest_tool_absent name=python3 path=/usr/bin/python3 detail=pinned absolute interpreter toolchain is required and has no PATH fallback
RC=3
```

Same command with the last line `printf 'rpd_require_pinned_tool env "$ENV_BIN"\n'`:

```
RPD_STOP reason=manifest_tool_not_root_owned name=env path=/usr/bin/env owner_numeric=4096:4096 expected=0:0
RC=3
```

Round 2 has no counterpart to either arm: it ran `command -v python3` and would
have used whatever PATH returned. The remaining pinned-tool arms (kind, mode 755
pass, 757 other-writable, 775 group-writable) are round-3 arms carried forward,
listed in section 6.10.

### 5.2 Item 2 (A2-F2) - deploy-channel attestation

Fixtures: `$QA/fix2/uid_map_identity` contains `0 0 4294967295`;
`$QA/fix2/uid_map_rootless` contains `0 1000 1`. The stub `readlink` answers
`/proc/self/ns/*` and `/proc/1/ns/*` from environment variables, so the
rootful-container case can be presented exactly as the audit describes it: self
namespaces equal to VISIBLE pid 1's, identity uid map, but not the host's.

**Command (RED):**

```
{ pre2r; exfn "$R2/RPD-VERIFY.sh" rpd_assert_initial_namespaces \
    | sed "s|/proc/self/uid_map|$QA/fix2/uid_map_identity|"
  printf 'rpd_assert_initial_namespaces\n'; } >"$QA/arm.sh"
PATH="$QA/fix2/stub:$PATH" env 'STUB_SELF_U=user:[4026999991]' 'STUB_SELF_M=mnt:[4026999992]' \
  'STUB_INIT_U=user:[4026999991]' 'STUB_INIT_M=mnt:[4026999992]' bash "$QA/arm.sh"
```

```
RPD_namespace user=user:[4026999991] mnt=mnt:[4026999992] bound=initial uid_map=identity
RC=0
```

That is the overclaim: `bound=initial` printed for a namespace pair that is not
the host's.

**Command (GREEN)** - same container, attested host values supplied:

```
{ pre4r; exfn "$R4/RPD-VERIFY.sh" rpd_assert_attested_namespaces \
    | sed "s|/proc/self/uid_map|$QA/fix2/uid_map_identity|"
  exc "$R4/RPD-VERIFY.sh" ROOTFS; exc "$R4/RPD-VERIFY.sh" ROOT_OWNER
  printf 'rpd_assert_attested_namespaces\n'; } >"$QA/arm.sh"
PATH="$QA/fix2/stub:$PATH" env 'STUB_SELF_U=user:[4026999991]' 'STUB_SELF_M=mnt:[4026999992]' \
  STUB_ROOTFS=2049:2 'RPD_EXPECT_NS_USER=user:[4026531837]' 'RPD_EXPECT_NS_MNT=mnt:[4026531840]' \
  RPD_EXPECT_ROOTFS_ID=2049:2 bash "$QA/arm.sh"
```

```
RPD_STOP reason=namespace_not_attested ns=user self=user:[4026999991] attested=user:[4026531837]
RC=3
```

Same arm script, `STUB_SELF_U=user:[4026531837] STUB_SELF_M=mnt:[4026531840]` -
self equal to every attested value:

```
RPD_namespace user=user:[4026531837] mnt=mnt:[4026531840] rootfs=2049:2 bound=attested source=deploy_channel_preregistration uid_map=identity
RC=0
```

Same arm script, `STUB_SELF_U=user:[4026531837] STUB_SELF_M=mnt:[4026999992]`:

```
RPD_STOP reason=namespace_not_attested ns=mnt self=mnt:[4026999992] attested=mnt:[4026531840]
RC=3
```

Same arm script, both namespaces matching and `STUB_ROOTFS=64768:9999` - the
chroot / bind-over-root case the namespace tokens alone cannot see:

```
RPD_STOP reason=rootfs_not_attested path=/ self=64768:9999 attested=2049:2
RC=3
```

Same GREEN command with `uid_map_rootless` in place of `uid_map_identity` in the
`sed` - the round-2 predicate, kept:

```
RPD_STOP reason=user_namespace_not_initial reason=uid_map_not_identity map=[0 1000 1]
RC=3
```

Input guards, delivered round-4 functions, no stub and no repointed literal
(category A). Command, with `<tail>` the tail column:

```
{ pre4r; exfn "$R4/RPD-VERIFY.sh" <fn>; printf '%s\n' '<tail>'; } >"$QA/arm.sh"
arm
```

| Arm | `<fn>` | `<tail>` | Output | Rc |
|---|---|---|---|---:|
| I2-G1 | `rpd_require_ns_token` | `rpd_require_ns_token RPD_EXPECT_NS_USER "user:[4026531837]" user` | `RPD_input name=RPD_EXPECT_NS_USER value=user:[4026531837]` | 0 |
| I2-G2 | `rpd_require_ns_token` | `rpd_require_ns_token RPD_EXPECT_NS_MNT "4026531840" mnt` | `RPD_STOP reason=input_shape name=RPD_EXPECT_NS_MNT expected=mnt:[<decimal_inode>]` | 3 |
| I2-G3 | `rpd_require_ns_token` | `rpd_require_ns_token RPD_EXPECT_NS_USER "user:[40265abc]" user` | `RPD_STOP reason=input_charset name=RPD_EXPECT_NS_USER expected=decimal_inode` | 3 |
| I2-G4 | `rpd_require_ns_token` | `rpd_require_ns_token RPD_EXPECT_NS_MNT "user:[4026531840]" mnt` | `RPD_STOP reason=input_shape name=RPD_EXPECT_NS_MNT expected=mnt:[<decimal_inode>]` | 3 |
| I2-G8 | `rpd_require_ns_token` | `rpd_require_ns_token RPD_EXPECT_NS_USER "user:[]" user` | `RPD_STOP reason=input_shape name=RPD_EXPECT_NS_USER expected=user:[<decimal_inode>] detail=empty_inode` | 3 |
| I2-G5 | `rpd_require_devino` | `rpd_require_devino RPD_EXPECT_ROOTFS_ID "2049:2"` | `RPD_input name=RPD_EXPECT_ROOTFS_ID value=2049:2` | 0 |
| I2-G6 | `rpd_require_devino` | `rpd_require_devino RPD_EXPECT_ROOTFS_ID "2049:2:3"` | `RPD_STOP reason=input_shape name=RPD_EXPECT_ROOTFS_ID expected=<decimal_dev>:<decimal_inode>` | 3 |
| I2-G7 | `rpd_require_devino` | `rpd_require_devino RPD_EXPECT_ROOTFS_ID "dev:2"` | `RPD_STOP reason=input_charset name=RPD_EXPECT_ROOTFS_ID expected=decimal_dev_and_inode` | 3 |

Missing-input STOPs, delivered file executed as a file (category A). Command,
with `<MISS>` each of the three attestation names in turn:

```
( cd "$R4" && \
  RPD_CANDIDATE_SHA=$GOODREL RPD_RELEASE_MANIFEST_SHA256=$GOODMAN \
  RPD_EXPECT_NS_USER='user:[4026531837]' RPD_EXPECT_NS_MNT='mnt:[4026531840]' \
  RPD_EXPECT_ROOTFS_ID=2049:2 \
  bash -c "unset <MISS>; bash RPD-VERIFY.sh" )
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

**Command (RED):**

```
{ pre2b; exfn "$R2/RP1-B3.sh" b3_probe_kind; exfn "$R2/RP1-B3.sh" b3_assert_mode_owner
  printf 'b3_assert_mode_owner /var/lib/mtc-bridge 0750 mtc-bridge:mtc-bridge\n'; } >"$QA/arm.sh"
PATH="$QA/fix3/stub:$PATH" env STUB_OWN=999:999 bash "$QA/arm.sh"
```

```
B3_stat path=/var/lib/mtc-bridge owner_numeric=999:999 owner_name=mtc-bridge:mtc-bridge mode=750
RC=0
```

**Command (GREEN)** - identical stub, round-4 function, expectation built from
the preregistered pair `B3_SVC_UID=1500 B3_SVC_GID=1500`:

```
{ pre4b; exfn "$R4/RP1-B3.sh" b3_probe_kind; exfn "$R4/RP1-B3.sh" b3_assert_mode_owner
  printf 'b3_assert_mode_owner /var/lib/mtc-bridge 0750 1500:1500\n'; } >"$QA/arm.sh"
PATH="$QA/fix3/stub:$PATH" env STUB_OWN=999:999 bash "$QA/arm.sh"
```

```
B3_stat path=/var/lib/mtc-bridge owner_numeric=999:999 owner_name=mtc-bridge:mtc-bridge mode=750
B3_FAIL reason=path=/var/lib/mtc-bridge owner_numeric=999:999 expected=1500:1500 owner_name=mtc-bridge:mtc-bridge
RC=1
```

Same GREEN command with `0750 999:999` as the expectation - the preregistered
pair really is `999:999`, so the admission still passes and this is a
discriminating check, not a blanket rejection:

```
B3_stat path=/var/lib/mtc-bridge owner_numeric=999:999 owner_name=mtc-bridge:mtc-bridge mode=750
RC=0
```

Same GREEN command with `0750 mtc-bridge:mtc-bridge` - a NAME passed where the
numeric pair belongs, i.e. a coding error in the block:

```
B3_STOP reason=owner_expectation_malformed path=/var/lib/mtc-bridge expected=[mtc-bridge:mtc-bridge] shape=<uid>:<gid>
RC=3
```

No weakening of the one case round 2 did catch - uid 0 rendered as the service
name. The RED command above with `STUB_OWN=0:999`:

```
B3_stat path=/var/lib/mtc-bridge owner_numeric=0:999 owner_name=mtc-bridge:mtc-bridge mode=750
B3_FAIL reason=path=/var/lib/mtc-bridge owner_numeric=0:999 expected=nonzero_service_account name=mtc-bridge:mtc-bridge
RC=1
```

The GREEN command with `STUB_OWN=0:999`:

```
B3_stat path=/var/lib/mtc-bridge owner_numeric=0:999 owner_name=mtc-bridge:mtc-bridge mode=750
B3_FAIL reason=path=/var/lib/mtc-bridge owner_numeric=0:999 expected=1500:1500 owner_name=mtc-bridge:mtc-bridge
RC=1
```

Input guards, delivered file executed as a file (category A). Five exact
commands, run from `round4/`:

```
env -u B3_SVC_UID B3_SWEEP_BUDGET_S=120 B3_SVC_GID=1500 bash RP1-B3.sh
env B3_SWEEP_BUDGET_S=120 B3_SVC_UID=abc  B3_SVC_GID=1500 bash RP1-B3.sh
env B3_SWEEP_BUDGET_S=120 B3_SVC_UID=0    B3_SVC_GID=1500 bash RP1-B3.sh
env -u B3_SVC_GID B3_SWEEP_BUDGET_S=120 B3_SVC_UID=1500 bash RP1-B3.sh
env B3_SWEEP_BUDGET_S=120 B3_SVC_UID=1500 B3_SVC_GID=0    bash RP1-B3.sh
```

```
B3_STOP reason=input_missing name=B3_SVC_UID detail=preregistered numeric uid of the mtc-bridge service account, never derived here
RC=3
B3_STOP reason=input_charset name=B3_SVC_UID expected=decimal_digits
RC=3
B3_STOP reason=input_range name=B3_SVC_UID value=0 expected=nonzero_service_account_uid
RC=3
B3_STOP reason=input_missing name=B3_SVC_GID detail=preregistered numeric gid of the mtc-bridge service account, never derived here
RC=3
B3_STOP reason=input_range name=B3_SVC_GID value=0 expected=nonzero_service_account_gid
RC=3
```

### 5.4 Item 4 (A2-F4) - NaN, Infinity, -Infinity

Both bindings are CORRECT in all three fixtures, so the only thing under test is
the constant.

**Command (RED)** - the section 5.1 RED command with `<FIX>` in place of
`wrong.json`, and NO `PYTHONPATH`:

```
{ pre2r
  exc "$R2/RPD-VERIFY.sh" ROOT_OWNER; exc "$R2/RPD-VERIFY.sh" MANIFEST_MAX_BYTES
  exfn "$R2/RPD-VERIFY.sh" rpd_assert_manifest_binding
  printf 'rpd_assert_manifest_binding "%s" "%s" "%s" 0666\n' \
      "$QAW/fix1/<FIX>" "$GOODREL" "$GOODMAN"; } >"$QA/arm.sh"
bash "$QA/arm.sh"
```

**Command (GREEN)** - the section 5.1 GREEN command with `<FIX>` in place of
`wrong.json`, and NO `PYTHONPATH`:

```
{ pre4r
  exc "$R4/RPD-VERIFY.sh" ROOT_OWNER; exc "$R4/RPD-VERIFY.sh" MANIFEST_MAX_BYTES
  exc "$R4/RPD-VERIFY.sh" ENV_BIN; exc "$R4/RPD-VERIFY.sh" CHILD_PATH
  exc "$R4/RPD-VERIFY.sh" CHILD_CWD
  printf 'PYTHON_BIN="%s"\n' "$QA_PY"
  pinstub
  exfn "$R4/RPD-VERIFY.sh" rpd_assert_manifest_binding
  printf 'rpd_assert_manifest_binding "%s" "%s" "%s" 0666\n' \
      "$QAW/fix1/<FIX>" "$GOODREL" "$GOODMAN"; } >"$QA/arm.sh"
bash "$QA/arm.sh"
```

`<FIX>` = `nan.json`, RED then GREEN:

```
RPD_manifest_binding path=$QAW/fix1/nan.json bound=both parser=python3_json_structural keys=top_level_exact
RC=0
```

```
RPD_tool name=env path=/usr/bin/env mode=755 owner_numeric=0:0 resolution=pinned_absolute
RPD_tool name=python3 path=$QA_PY mode=755 owner_numeric=0:0 resolution=pinned_absolute
RPD_STOP reason=install_manifest_non_json_constant path=$QAW/fix1/nan.json detail=NaN_Infinity_-Infinity_are_not_JSON_values
RC=3
```

`<FIX>` = `inf.json`, RED then GREEN:

```
RPD_manifest_binding path=$QAW/fix1/inf.json bound=both parser=python3_json_structural keys=top_level_exact
RC=0
```

```
RPD_tool name=env path=/usr/bin/env mode=755 owner_numeric=0:0 resolution=pinned_absolute
RPD_tool name=python3 path=$QA_PY mode=755 owner_numeric=0:0 resolution=pinned_absolute
RPD_STOP reason=install_manifest_non_json_constant path=$QAW/fix1/inf.json detail=NaN_Infinity_-Infinity_are_not_JSON_values
RC=3
```

`<FIX>` = `neginf.json`, RED then GREEN:

```
RPD_manifest_binding path=$QAW/fix1/neginf.json bound=both parser=python3_json_structural keys=top_level_exact
RC=0
```

```
RPD_tool name=env path=/usr/bin/env mode=755 owner_numeric=0:0 resolution=pinned_absolute
RPD_tool name=python3 path=$QA_PY mode=755 owner_numeric=0:0 resolution=pinned_absolute
RPD_STOP reason=install_manifest_non_json_constant path=$QAW/fix1/neginf.json detail=NaN_Infinity_-Infinity_are_not_JSON_values
RC=3
```

### 5.5 Item 5 (A2-F5) - the mount readers, both blocks

This is the item audit 3 marked NOT CLOSED. It has four parts: the NEW read-error
arm (5.5.1), the round-3 closures re-driven against round-4 bytes (5.5.2), and
the no-weakening sweep (5.5.3).

**The exact command, for every mount arm below.** `<PRE>` is one of `pre2b`,
`pre2r`, `pre3b`, `pre3r`, `pre4b`, `pre4r`; `<SRC>` is `$R2`, `$R3` or `$R4`;
`<FILE>` is `RP1-B3.sh` or `RPD-VERIFY.sh`; `<FN>` is
`b3_assert_no_mount_at_or_under` or `rpd_assert_no_mount_at_or_under`; `<FX>` is
the fixture name. Nothing else varies - the B3 and RPD forms are both written
out below rather than one being described as differing from the other:

```
{ <PRE>; printf 'MOUNTS=%s\n' "$QA/fix2/mounts/<FX>"
  exfn "<SRC>/<FILE>" <FN>
  printf '%s /etc/mtc-bridge\n' <FN>; } >"$QA/arm.sh"
arm
```

#### 5.5.1 NEW - the read-error arm (audit-3 finding 1)

RED here is ROUND-3 code, because round 3 is where this defect lives.

**RPD, RED, fixture `adir` (a DIRECTORY - the audit's own fixture).** Exact
command:

```
{ pre3r; printf 'MOUNTS=%s\n' "$QA/fix2/mounts/adir"
  exfn "$R3/RPD-VERIFY.sh" rpd_assert_no_mount_at_or_under
  printf 'rpd_assert_no_mount_at_or_under /etc/mtc-bridge\n'; } >"$QA/arm.sh"
arm
```

```
$QA/arm.sh: line 30: read: read error: 0: Is a directory
RPD_conf_dir_no_mount_boundary path=/etc/mtc-bridge source=$QA/fix2/mounts/adir records=0
RC=0
```

That is the audit's finding reproduced exactly: a read error, zero records
consumed, and a `no_mount_boundary` admission at rc 0.

**RPD, GREEN, fixture `adir`.** Exact command:

```
{ pre4r; printf 'MOUNTS=%s\n' "$QA/fix2/mounts/adir"
  exfn "$R4/RPD-VERIFY.sh" rpd_assert_no_mount_at_or_under
  printf 'rpd_assert_no_mount_at_or_under /etc/mtc-bridge\n'; } >"$QA/arm.sh"
arm
```

```
$QA/arm.sh: line 30: read: read error: 0: Is a directory
RPD_STOP reason=mount_table_read_error path=$QA/fix2/mounts/adir records=0 read_rc=1 detail=nonzero_read_populated_no_field_and_consumed_no_record
RC=3
```

**B3, RED, fixture `adir`.** Exact command:

```
{ pre3b; printf 'MOUNTS=%s\n' "$QA/fix2/mounts/adir"
  exfn "$R3/RP1-B3.sh" b3_assert_no_mount_at_or_under
  printf 'b3_assert_no_mount_at_or_under /etc/mtc-bridge\n'; } >"$QA/arm.sh"
arm
```

```
$QA/arm.sh: line 31: read: read error: 0: Is a directory
B3_conf_dir_no_mount_boundary path=/etc/mtc-bridge source=$QA/fix2/mounts/adir records=0
RC=0
```

**B3, GREEN, fixture `adir`.** Exact command:

```
{ pre4b; printf 'MOUNTS=%s\n' "$QA/fix2/mounts/adir"
  exfn "$R4/RP1-B3.sh" b3_assert_no_mount_at_or_under
  printf 'b3_assert_no_mount_at_or_under /etc/mtc-bridge\n'; } >"$QA/arm.sh"
arm
```

```
$QA/arm.sh: line 31: read: read error: 0: Is a directory
B3_STOP reason=mount_table_read_error path=$QA/fix2/mounts/adir records=0 read_rc=1 detail=nonzero_read_populated_no_field_and_consumed_no_record
RC=3
```

The `read: read error: 0: Is a directory` line is bash's own diagnostic on the
ARM's stderr - it is not produced by either block, and neither block can test for
it. It is the MSYS spelling of the `bash: read: read error: Is a directory` the
audit recorded on Linux. Opening a directory for input succeeds on both, which is
why the round-3 loop reached its EOF branch at record zero.

**The zero-byte source, same defect, no diagnostic at all.** Same four commands
with `<FX>` = `empty`:

| Block | Code | Output | Rc |
|---|---|---|---:|
| RPD | round 3 | `RPD_conf_dir_no_mount_boundary path=/etc/mtc-bridge source=$QA/fix2/mounts/empty records=0` | **0** |
| RPD | round 4 | `RPD_STOP reason=mount_table_read_error path=$QA/fix2/mounts/empty records=0 read_rc=1 detail=nonzero_read_populated_no_field_and_consumed_no_record` | **3** |
| B3 | round 3 | `B3_conf_dir_no_mount_boundary path=/etc/mtc-bridge source=$QA/fix2/mounts/empty records=0` | **0** |
| B3 | round 4 | `B3_STOP reason=mount_table_read_error path=$QA/fix2/mounts/empty records=0 read_rc=1 detail=nonzero_read_populated_no_field_and_consumed_no_record` | **3** |

This second fixture is included deliberately, and its status is stated rather
than blurred: an EMPTY mount table is not a read error, but it is equally not a
mount table, and the round-4 predicate refuses both under the same reason for the
same stated cause - `records=0` means the source was never read. Round 3
admitted both at rc 0.

#### 5.5.2 The round-3 closures, re-driven against round-4 bytes

RED here is ROUND-2 code, as in round 3. Commands are the section 5.5 form with
`<PRE>`=`pre2r`/`pre2b` and `<SRC>`=`$R2` for RED, `pre4r`/`pre4b` and `$R4` for
GREEN.

| Arm | RED (round-2 code) | Rc | GREEN (round-4 code) | Rc |
|---|---|---:|---|---:|
| RPD, `nonl` | `RPD_conf_dir_no_mount_boundary path=/etc/mtc-bridge source=$QA/fix2/mounts/nonl` | **0** | `RPD_STOP reason=mount_table_unterminated_final_record path=$QA/fix2/mounts/nonl records=1 hits=1 first_target=/etc/mtc-bridge` | **3** |
| B3, `nonl` | `B3_conf_dir_no_mount_boundary path=/etc/mtc-bridge source=$QA/fix2/mounts/nonl` | **0** | `B3_STOP reason=mount_table_unterminated_final_record path=$QA/fix2/mounts/nonl records=1 hits=1 first_target=/etc/mtc-bridge` | **3** |
| RPD, `short` | `RPD_conf_dir_no_mount_boundary path=/etc/mtc-bridge source=$QA/fix2/mounts/short` | **0** | `RPD_STOP reason=mount_record_malformed path=$QA/fix2/mounts/short record=2 expected_fields=6 got=[src /etc/mtc-bri     ]` | **3** |
| B3, `short` | `B3_conf_dir_no_mount_boundary path=/etc/mtc-bridge source=$QA/fix2/mounts/short` | **0** | `B3_STOP reason=mount_record_malformed path=$QA/fix2/mounts/short record=2 expected_fields=6 got=[src /etc/mtc-bri     ]` | **3** |
| RPD, `wide` | `RPD_STOP reason=mount_boundary_at_or_under_conf_dir path=/etc/mtc-bridge mounts=1 first_target=/etc/mtc-bridge` | 3 | `RPD_STOP reason=mount_record_malformed path=$QA/fix2/mounts/wide record=2 expected_fields=6 got=[src /etc/mtc-bridge ext4 rw 0 0 extra]` | 3 |
| B3, `wide` | `B3_STOP reason=mount_boundary_at_or_under_conf_dir path=/etc/mtc-bridge mounts=1 first_target=/etc/mtc-bridge` | 3 | `B3_STOP reason=mount_record_malformed path=$QA/fix2/mounts/wide record=2 expected_fields=6 got=[src /etc/mtc-bridge ext4 rw 0 0 extra]` | 3 |

The first four rows are round 3's closure, unchanged by round 4. The `wide` rows
are stated honestly as an ADDED validation, not a closure: round 2 already
STOPped there, for a different reason.

#### 5.5.3 No weakening - the full round-4 sweep, both blocks

Same command form, `<PRE>`=`pre4r`/`pre4b`, `<SRC>`=`$R4`:

| Fixture | RPD output | Rc | B3 output | Rc |
|---|---|---:|---|---:|
| `clean` (3 records, none matching) | `RPD_conf_dir_no_mount_boundary path=/etc/mtc-bridge source=$QA/fix2/mounts/clean records=3` | 0 | `B3_conf_dir_no_mount_boundary path=/etc/mtc-bridge source=$QA/fix2/mounts/clean records=3` | 0 |
| `sibling` (`/etc/mtc-bridgeX` only) | `RPD_conf_dir_no_mount_boundary path=/etc/mtc-bridge source=$QA/fix2/mounts/sibling records=2` | 0 | `B3_conf_dir_no_mount_boundary path=/etc/mtc-bridge source=$QA/fix2/mounts/sibling records=2` | 0 |
| `at` (mount AT the directory) | `RPD_STOP reason=mount_boundary_at_or_under_conf_dir path=/etc/mtc-bridge mounts=1 first_target=/etc/mtc-bridge` | 3 | `B3_STOP reason=mount_boundary_at_or_under_conf_dir path=/etc/mtc-bridge mounts=1 first_target=/etc/mtc-bridge` | 3 |
| `under` (mount UNDER it) | `RPD_STOP reason=mount_boundary_at_or_under_conf_dir path=/etc/mtc-bridge mounts=1 first_target=/etc/mtc-bridge/sub` | 3 | `B3_STOP reason=mount_boundary_at_or_under_conf_dir path=/etc/mtc-bridge mounts=1 first_target=/etc/mtc-bridge/sub` | 3 |
| `absent` (source does not exist) | `RPD_STOP reason=mounts_unreadable path=$QA/fix2/mounts/absent` | 3 | `B3_STOP reason=mounts_unreadable path=$QA/fix2/mounts/absent` | 3 |

The `clean` and `sibling` rows are what prove the new arm did not turn the
predicate into a blanket rejection: a well-formed table still returns rc 0 with
its record count, and the prefix match still does not fire on `/etc/mtc-bridgeX`.

### 5.6 Item 6 (A2-F6) - boundary diagnostics

**Command (RED)**, with `<CASE>` from the table:

```
{ pre2b; exfn "$R2/RP1-B3.sh" b3_assert_conf_dir_opaque
  printf 'b3_assert_conf_dir_opaque /etc/mtc-bridge/mtc-bridge.env\n'; } >"$QA/arm.sh"
PATH="$QA/fix3/stubdir:$PATH" STUB_CASE=<CASE> bash "$QA/arm.sh"
```

**Command (GREEN)**, same `<CASE>`:

```
{ pre4b; exc "$R4/RP1-B3.sh" B3_EACCES_TEXT; exc "$R4/RP1-B3.sh" B3_ENOENT_TEXT
  exfn "$R4/RP1-B3.sh" b3_count_substr; exfn "$R4/RP1-B3.sh" b3_classify_boundary_shape
  exfn "$R4/RP1-B3.sh" b3_assert_conf_dir_opaque
  printf 'b3_assert_conf_dir_opaque /etc/mtc-bridge/mtc-bridge.env\n'; } >"$QA/arm.sh"
PATH="$QA/fix3/stubdir:$PATH" STUB_CASE=<CASE> bash "$QA/arm.sh"
```

`P` below abbreviates the probed path `/etc/mtc-bridge/mtc-bridge.env`, and only
that; every other byte is the real output.

| `<CASE>` | RED (round-2 code) | Rc | GREEN (round-4 code) | Rc |
|---|---|---:|---|---:|
| `twoline` | `B3_conf_dir_opaque_to_operator path=P outcome=EACCES rc=1 mechanism=message_lc_all_c` | **0** | `B3_STOP reason=boundary_diagnostic_multiline path=P rc=1 detail=stat: cannot stat 'P': Permission denied stat: cannot stat 'P': No such file or directory` | **3** |
| `oneline2` | `B3_conf_dir_opaque_to_operator path=P outcome=EACCES rc=1 mechanism=message_lc_all_c` | **0** | `B3_STOP reason=boundary_diagnostic_ambiguous path=P rc=1 classes=2 eacces=1 enoent=1 detail=stat: cannot stat 'P': Permission denied (No such file or directory)` | **3** |
| `wrapper` | `B3_conf_dir_opaque_to_operator path=P outcome=EACCES rc=1 mechanism=message_lc_all_c` | **0** | `B3_STOP reason=boundary_probe_unclassified path=P rc=1 detail=mtcwrap: stat failed on P: Permission denied` | **3** |
| `wrongpath` | `B3_conf_dir_opaque_to_operator path=P outcome=EACCES rc=1 mechanism=message_lc_all_c` | **0** | `B3_STOP reason=boundary_probe_unclassified path=P rc=1 detail=stat: cannot stat '/some/other/path': Permission denied` | **3** |
| `eacces` | `B3_conf_dir_opaque_to_operator path=P outcome=EACCES rc=1 mechanism=message_lc_all_c` | 0 | `B3_conf_dir_opaque_to_operator path=P outcome=EACCES rc=1 mechanism=message_lc_all_c_exact_shape` | 0 |
| `statx` | `B3_conf_dir_opaque_to_operator path=P outcome=EACCES rc=1 mechanism=message_lc_all_c` | 0 | `B3_conf_dir_opaque_to_operator path=P outcome=EACCES rc=1 mechanism=message_lc_all_c_exact_shape` | 0 |
| `enoent` | `B3_FAIL reason=conf_dir_search_permitted_name_absent path=P rc=1 expected=EACCES` | 1 | `B3_FAIL reason=conf_dir_search_permitted_name_absent path=P rc=1 expected=EACCES` | 1 |
| `eio` | `B3_STOP reason=boundary_probe_unclassified path=P rc=1 detail=stat: cannot stat 'P': Input/output error` | 3 | `B3_STOP reason=boundary_probe_unclassified path=P rc=1 detail=stat: cannot stat 'P': Input/output error` | 3 |
| `empty` | `B3_STOP reason=boundary_probe_unclassified path=P rc=4 detail=` | 3 | `B3_STOP reason=boundary_probe_unclassified path=P rc=4 detail=` | 3 |
| `nonprint` | `B3_STOP reason=boundary_probe_unclassified path=P rc=1 detail=[non_printable_detail_suppressed]` | 3 | `B3_STOP reason=boundary_probe_unclassified path=P rc=1 detail=[non_printable_detail_suppressed]` | 3 |
| `ok` | `B3_FAIL reason=conf_dir_entry_permitted path=P stat=[regular file\|600\|0:0] expected=EACCES` | 1 | `B3_FAIL reason=conf_dir_entry_permitted path=P stat=[regular file\|600\|0:0] expected=EACCES` | 1 |

Four false rc-0 arms closed; the seven PASS/FAIL/STOP arms that were already
correct are byte-identical or differ only in the `mechanism=` field, so nothing
was weakened.

**The exact-shape rule driven against REAL coreutils, no stub at all**
(category A): the round-4 function probing a genuinely absent name, so the real
`stat` emits the real C-locale ENOENT diagnostic. Exact command:

```
{ pre4b; exc "$R4/RP1-B3.sh" B3_EACCES_TEXT; exc "$R4/RP1-B3.sh" B3_ENOENT_TEXT
  exfn "$R4/RP1-B3.sh" b3_count_substr; exfn "$R4/RP1-B3.sh" b3_classify_boundary_shape
  exfn "$R4/RP1-B3.sh" b3_assert_conf_dir_opaque
  printf 'b3_assert_conf_dir_opaque %s/no-such-name\n' "$QA/fix3"; } >"$QA/arm.sh"
arm
```

```
B3_FAIL reason=conf_dir_search_permitted_name_absent path=$QA/fix3/no-such-name rc=1 expected=EACCES
RC=1
```

This is the arm that shows the exact-shape templates match a real GNU coreutils
8.32 diagnostic and are not a construction that only the stubs satisfy.

## 6. Full round-4 arm walk

`[A]` = no stubbed command and no repointed literal. `[B]` = at least one of
either. Sections marked **carried forward** were driven in round 3 against bytes
that round 4 does not change (section 2.1); they are reproduced here for the
count and are NOT claimed as re-run in this round.

### 6.1 `RP1-B3.sh`, delivered file executed as a file `[A]` (5)

Command: `( cd round4 && env <assignments> bash RP1-B3.sh )`.

| Arm | Command | Output | Rc |
|---|---|---|---:|
| R1 | `env -u B3_SWEEP_BUDGET_S B3_SVC_UID=1500 B3_SVC_GID=1500 bash RP1-B3.sh` | `B3_STOP reason=input_missing name=B3_SWEEP_BUDGET_S detail=preregistered per-tree sweep budget in seconds, positive integer, never derived here` | 3 |
| R2 | `env B3_SWEEP_BUDGET_S=abc B3_SVC_UID=1500 B3_SVC_GID=1500 bash RP1-B3.sh` | `B3_STOP reason=input_charset name=B3_SWEEP_BUDGET_S expected=decimal_digits` | 3 |
| R3 | `env B3_SWEEP_BUDGET_S=0 B3_SVC_UID=1500 B3_SVC_GID=1500 bash RP1-B3.sh` | `B3_STOP reason=input_range name=B3_SWEEP_BUDGET_S value=0 expected=positive_integer` | 3 |
| R4 | `env B3_SWEEP_BUDGET_S=120 B3_SVC_UID=1500 B3_SVC_GID=1500 bash RP1-B3.sh` | `B3_STOP reason=rp0_lib_not_sourced predicate=rp0_monotonic_ms` | 3 |
| R5 | `. RP0-LIB.sh; . RP1-B3.sh` end to end (**carried forward**) | `B3_SECTION header candidate=2ce41e34...321b` / `B3_identity uid=4096 gids=[4096]` / `B3_STOP reason=namespace_unreadable ns=user path=/proc/self/ns/user` | 3 |

R1-R4 were re-run against round-4 bytes and are the outputs above. R5 stops at
the namespace disclosure because MSYS has no `/proc/self/ns` at all; on Linux
this line records the two identities and continues.

### 6.2 `RP1-B3.sh` input guards for the NEW inputs `[A]` (5)

The five runs at the end of section 5.3, all rc 3, all re-run against round-4
bytes.

### 6.3 `b3_sanitize` and `b3_count_substr` `[A]` (7) - carried forward

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

### 6.4 `b3_probe_kind`, stubbed `stat` `[B]` (10) - carried forward

`PK-b3-1` regular file -> `kind=regular` rc 0; `PK-b3-2` regular empty file ->
`kind=regular` rc 0; `PK-b3-3` directory -> `kind=dir` rc 0; `PK-b3-4` fifo ->
`kind=other` rc 0; `PK-b3-5` symlink + live target -> `kind=link_live` rc 0;
`PK-b3-6` symlink + ENOENT target -> `kind=link_dangling` rc 0; `PK-b3-7` symlink
+ EIO target -> `B3_STOP reason=link_target_probe_error path=/p rc=1 detail=stat:
cannot stat '/p': Input/output error` rc 3; `PK-b3-8` rc 1 ENOENT -> `kind=absent`
rc 0; `PK-b3-9` rc 1 EACCES -> `B3_STOP reason=path_probe_error path=/p rc=1
detail=stat: cannot stat '/p': Permission denied` rc 3; `PK-b3-10` rc 0 with empty
output -> `B3_STOP reason=path_probe_empty path=/p rc=0` rc 3.

### 6.5 `b3_assert_mode_owner` and the sweep, stubbed `[B]` (7 + 7 + 4)

M1-M7 and W1-W7 are **carried forward**; the four section-5.3
`b3_assert_mode_owner` arms were re-run against round-4 bytes.

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

### 6.6 Identity, namespaces, group, canonical path, stubbed `[B]` (4+3+4+4) - carried forward

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

### 6.7 access(2) predicate and ERR trap `[A]` (2 + 1) - carried forward

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

The twelve runs in section 5.6, all re-run against round-4 bytes.

### 6.9 Mount reader, round-4 code `[B]` (10 per block)

Per block: the two NEW read-error arms (`adir`, `empty`) of section 5.5.1, the
three GREEN arms (`nonl`, `short`, `wide`) of 5.5.2, and the five sweep arms
(`clean`, `sibling`, `at`, `under`, `absent`) of 5.5.3. All 20 were driven
against round-4 bytes in this round; the full outputs are in section 5.5 and are
not duplicated here.

Round 3 had 8 arms per block. The two added per block are the closure of
audit-3 finding 1.

### 6.10 `RPD-VERIFY.sh` whole-file, hex guard, pinned tools, ERR trap

`[A]` unless marked. `RD1`, `RD3`, `TP1`, `TP2` were re-run against round-4
bytes; the rest are **carried forward**.

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
for the right reason. Its exact round-4 command:

```
( cd round4 && env RPD_CANDIDATE_SHA=$GOODREL RPD_RELEASE_MANIFEST_SHA256=$GOODMAN \
    RPD_EXPECT_NS_USER='user:[4026531837]' RPD_EXPECT_NS_MNT='mnt:[4026531840]' \
    RPD_EXPECT_ROOTFS_ID=2049:2 bash RPD-VERIFY.sh )
```

### 6.11 `rpd_probe_kind` `[B]` (10) - carried forward

`PK-rpd-1` regular, `PK-rpd-2` regular empty, `PK-rpd-3` directory, `PK-rpd-4`
fifo, `PK-rpd-5` link_live, `PK-rpd-6` link_dangling, all rc 0 with the expected
token; `PK-rpd-7` `RPD_STOP reason=link_target_probe_error path=/p rc=1
detail=stat: cannot stat '/p': Input/output error` rc 3; `PK-rpd-8` absent rc 0;
`PK-rpd-9` `RPD_STOP reason=path_probe_error path=/p rc=1 detail=stat: cannot
stat '/p': Permission denied` rc 3; `PK-rpd-10` `RPD_STOP reason=path_probe_empty
path=/p rc=0` rc 3.

### 6.12 `rpd_assert_conf_dir` and `rpd_assert_regular_mode_owner` `[B]` (8 + 7) - carried forward

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

### 6.13 Manifest binding, round-4 reader `[B]` (11)

Eleven arms, and the label is the real count: the three item-4 arms of section
5.4, the two item-1 GREEN arms of section 5.1, and the six table arms below. This
is the subcount audit-3 finding 2 reported as mislabelled `(9)` in round 3; the
RPD B subtotal was always computed with 11, and 11 is what is displayed now.

`NW-good` was re-run against round-4 bytes; the other five are **carried
forward**.

| Arm | Fixture | Output | Rc |
|---|---|---|---:|
| NW-good | valid manifest, both bindings correct | `RPD_manifest_binding path=$QAW/fix1/good.json bound=both parser=python3_json_structural keys=top_level_exact isolation=pinned_env_i` | 0 |
| NW-decoy | audit-1 nested `decoy` fixture | `RPD_FAIL reason=install manifest binds a different release_sha` | 1 |
| NW-dup | duplicate `release_sha` | `RPD_STOP reason=install_manifest_ambiguous_duplicate_key path=$QAW/fix1/dup.json` | 3 |
| NW-gone | manifest absent | `RPD_STOP reason=install_manifest_unreadable path=$QAW/fix1/absent.json` | 3 |
| NW-size | 10-byte bound | `RPD_STOP reason=install_manifest_oversize path=$QAW/fix1/good.json limit_bytes=10` | 3 |
| NW-junk | stub interpreter prints `WEIRD OUTPUT!`, rc 0 | `RPD_STOP reason=manifest_parser_unadjudicable path=$QAW/fix1/good.json rc=0 token=[unexpected_reader_output]` | 3 |

`NW-good`'s exact round-4 command is the section 5.4 GREEN command with `<FIX>` =
`good.json`. It is the arm that proves the isolation did not break the check:
through `env -i`, `-I -S -E` and `cd /`, a correct manifest still parses and
still binds. NW-decoy and NW-dup are audit-1's closures. NW-junk proves the token
charset guard still holds, so no manifest bytes can be smuggled out through a
STOP reason.

## 7. No file content is printed and no credential value is read

Audited line by line, both blocks, after the round-4 change. The round-4 hunk
adds one printf-format STOP reason and no new producer, no new redirection and no
new capture, so every statement below is the round-3 statement re-verified
against the round-4 bytes.

1. **Every output statement is a `printf` with a fixed ASCII format string.**
   There is no `cat`, `head`, `tail`, `sed`, `awk`, `od`, `strings`, no `echo` of
   a file, and no command substitution whose value comes from a file's CONTENT.
   The values interpolated into output are: a path literal from the block, a
   `stat` metadata field (`%F`, `%a`, `%u:%g`, `%U:%G`, `%g`, `%d:%i`), a numeric
   id from `id -u`/`id -G`, a namespace identity from `readlink /proc/self/ns/*`,
   a canonical path from `readlink -f`, a mount TARGET path from
   `/proc/self/mounts`, a mount record count, a `read` builtin status, a `find`
   PATH (never file bytes), an elapsed-seconds integer, an rc, a preregistered
   input, a fixed reader token, a pinned tool path/mode/owner, and a sanitized
   `stat`/`find` STDERR string. The round-4 addition is the `read` status and the
   already-present record count; no mount FIELD is added to any output.
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
4. **The reader's environment is an allow-list**, so nothing from the operator's
   environment reaches the child and nothing from the child's environment can be
   echoed: the eight `RPD_*` values it receives are the two preregistered hex
   inputs, the manifest path, the expected mode and the expected uid/gid/limit -
   all block constants or already-printed inputs.
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
   `command -v python3`. Round 4 adds no command. Scanned for and confirmed
   absent: `chmod`, `chown`, `chgrp`, `setfacl`, `sudo`, `mv`, `cp`, `ln`,
   `mkdir`, `touch`, `tee`, `dd`, `truncate`, `sed`, `systemctl`, `curl`, `wget`,
   `ssh`, `scp`, `nc`, `openssl`, `pip`.
7. **There is no file-writing redirection in either block.** The only redirections
   are `2>&1` into a variable capture, `2>/dev/null` (discard), `>/dev/null` on
   `command -v rp0_monotonic_ms` and on the `cd`, and `exec 9< <read-only file>`
   plus its close. Round 4 adds one more `exec 9<&-` close on the new STOP path
   and no new open. No `>` or `>>` targets any path.
8. **`RPD-VERIFY.sh` mutates nothing, and that claim covers its child.** No write
   to `ENV_FILE`, `INSTALL_MANIFEST` or `CONF_DIR`, no mode/owner change, no
   service or network call, no `sudo`, no group or ACL change. Its root
   requirement is used solely for metadata probes and one read-only open.

## 8. Known gaps in this QA

Stated so the closure audit does not have to find them.

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
6. **Five arms were not driven at all** and are excluded from every count; they
   are listed in section 3.
7. **`RPD-VERIFY.sh` has never run as root** anywhere, and it depends on two
   Linux-only facilities plus three attestation inputs that do not exist yet. Its
   PASS path is fixture-exercised only (open item O7).
8. **The attestation itself cannot be QA'd here.** Section 5.2 proves the block
   compares correctly against attested values; nothing in this QA can prove the
   deploy channel will mint them correctly. That is the residual named in
   DESIGN_NOTES section 9.1 and it is the Lead's to close.
9. **The section 8 #4 naming risk remains unresolved** and cannot be resolved by
   any unprivileged block, by construction of the EACCES denial.
10. **NEW, and the honest limit of the round-4 fix.** A read(2) failure raised
    MID-TABLE - after at least one well-formed record has been consumed - cannot
    be distinguished from a clean end of input by any shell-level predicate: bash
    `read` returns 1 for both, and the `read error:` diagnostic goes to the
    process's stderr rather than to a status the block can test. Round 4 closes
    the case that IS distinguishable and states the other rather than implying it
    is covered. Closing it fully would need a non-shell reader in `RP1-B3.sh`,
    which would make an interpreter-less host a new B3 STOP; that trade is named
    in DESIGN_NOTES section 10 and is the Lead's to decide, not this round's.
11. **The read-error arm was driven on MSYS, not Linux.** Opening a directory for
    input succeeds on both and the first `read` returns nonzero with no field
    populated on both, which is the condition the fix tests; the MSYS diagnostic
    text differs (`read error: 0: Is a directory` vs the Linux
    `read error: Is a directory`) and neither block reads that text. The zero-byte
    fixture drives the same branch with no diagnostic at all.
12. **91 of the 162 arms were carried forward from round 3, not re-run.** The
    table in section 3 lists exactly which, and section 2.1 shows why that is
    sound: the executable delta is confined to one function per file, and every
    arm that touches it was re-run.
