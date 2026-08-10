# WP-I transport set self-QA — round 2

Status: **REPAIRED-PENDING-REAUDIT**

Date: 2026-08-10. Round 2 of the T0 cap 3, closing the union of the Codex xhigh
audit (`TRANSPORT_CODEX_AUDIT_2026-08-10.md`, 10 required findings) and the
Claude xhigh audit (`TRANSPORT_CLAUDE_T0_AUDIT_2026-08-10.md`, 6 required + 5
nits).

Scope was local authoring and local fixtures only. **No SSH, SCP, host IP,
remote host, credential, service, unit, broker, exchange, or trading operation
was contacted or executed.** The only sockets opened were `127.0.0.1`
listener/connect fixtures for the section-8 row-24 classification arms. No RUNID
was allocated; `C:\WPI_ARTIFACTS` contains no `WPI_TRANSPORT_*` entry.

## 0. How to re-execute every claim in this document

Everything below is produced by exactly two scripts. They are reproduced here
**verbatim**, they take no arguments, they declare no shell state, and they are
the literal files that produced the transcripts recorded beneath them. Run them
in this order:

```
wsl.exe -e bash /mnt/c/<path>/wpi_r2_shell_qa.sh        # fixture set 1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File <path>\wpi_r2_runner_qa.ps1
```

Set 1 leaves the real `remote_close_tree.sh` transcripts under
`C:\Users\Public\wpi_r2_qa\close`, which set 2 consumes and then removes.

**RED is not a narration.** Every shell RED arm executes the *exact audited
round-1 bytes*, read straight out of commit `1c1c9ed1` — the commit both
auditors examined — and the script prints their digests so the baseline is
provable. Every runner RED arm executes the *current* file with precisely the
repair reverted, and the mutation anchor is asserted present before it is
applied, so a silently-missed anchor throws instead of manufacturing a false RED.

### Declared substitutions (there are five, and no others)

| # | Substitution | Why it is required | Where it shows up |
|---|---|---|---|
| S1 | Scratch roots rendered `<QA>` | random/absolute fixture paths | every transcript |
| S2 | Sandbox constants in a fixture copy (`EXPECT_PREFIX`, `EXPECT_PARENT`, `EXPECT_UID/GID`, `BASE_RUN`, `EXTRACT_DIR`, block digests, plan digest, record root) | a fixture cannot allocate the real host paths | both scripts, by `sed`/line rewrite |
| S3 | Tool pins retargeted at regular root-owned `0755` copies under `<QA>/bin` | this QA host ships coreutils as **symlinks** into a multicall binary, and the repaired scripts refuse a symlinked tool by design | shell set, `QA_TOOLCOPY` line |
| S4 | `ssh`/`scp` program pins retargeted at `C:\Windows\System32\cmd.exe` at its real digest | the process-launch path (8 of 12 ops) must be driven with **no host contact** | runner set, `QA_PROGRAM_PIN_SUBSTITUTION` line |
| S5 | `remote_close_tree.sh` `EXPECT_OWNER='gatea:gatea'` → `'root:root'` | the sandbox tree is root-owned; printed as a diff | shell set, `CLOSE_TRANSCRIPTS` |

S3 and S4 are the only substitutions that touch a *predicate*; both are printed
by the scripts themselves, and both are argued in §6. S5 is identical to the
substitution the round-1 Claude audit made and recorded.

The QA copy of `transport_runner.ps1` is written with a UTF-8 BOM because the
operator profile path on this host is non-ASCII and Windows PowerShell 5.1 would
otherwise decode the copy as ANSI. **The delivered file is ASCII-only with no
BOM** (§8). The `HOMEPATH`/`USERPROFILE` values inside a child's `set` output are
rendered in the console OEM codepage; that is a display property of `cmd`, not of
the value passed.

## 1. Finding → closing arm

| Finding | Repair | Arm that fails without it |
|---|---|---|
| Codex F2 / Claude F1 — `$Matches` clobber, ops 11/12 can never bind | latch every capture on the line after its own match | runner `A1` (PASS, rc 0) vs `A2` (RED: `digest_differs` ×3 on byte-identical files, rc 1) |
| Codex F1 / Claude F2 — child STOP rolled into FAIL | classify the mismatch: rc 3 → `TR_RUN STOP` exit 3 | runner `C1` (STOP, rc 3) vs `C2` (RED: FAIL, rc 1) |
| — precedence when both occur | deviant observation outranks later not-evaluable, both counted | runner `C3` (`deviant=1 not_evaluable=1` → FAIL) |
| — first-FAIL ordering unchanged | unchanged predicate | runner `C5` (skips 02, runs both `always`) vs `C4` (RED runs 02) |
| Codex F3 — inherited PATH selects the transport chain | pinned absolute programs + digest + trusted-SID chain + constructed environment | runner `D2` (`PINNED_PROGRAM_RAN`) vs `D1` (RED: `FAKE_SSH_EXECUTED`, rc 0 PASS); shell `P0/RO_HIJACK_*` |
| Codex F3 (wrappers, remote scripts) | pinned `sha256sum`/`stat`/`tar`/… with numeric ownership | shell `P0_HIJACK_GREEN` (`block_sha256_mismatch`, rc 3) vs `P0_HIJACK_RED` (`P0W_HIJACKED_BLOCK_EXECUTED`, rc 0) |
| Codex F4 — ambiguous diagnostic read as absence | calibrated whole-string template + kernel cross-check | shell `A2_GREEN` (STOP, 0 dirs) vs `A2_RED` (PASS, 4 dirs); `A3_GREEN` one-line two-class → STOP |
| Codex F5 — mutation before the path is bound; resolver names as identity | full parent chain bound before the first `mkdir`; numeric `%u:%g` | shell `A4_GREEN` (0 dirs) vs `A4_RED` (4 dirs through the symlink); `A5_GREEN` (`owner_numeric=1000:1000`) vs `A5_RED` (PASS) |
| Codex F6 — listing stdout consumed before status/diagnostics/completion | sentinel capture, two-pass diagnostic equality, termination check, re-hash after listing | shell `B2_GREEN` / `B3_GREEN` (STOP) vs `B2_RED` / `B3_RED` (PASS) |
| Codex F7 / Claude F5 — derivation exceeds §4 | counts derived from `MEMBERS`; §4 amended and the amendment declared | shell `B4_GREEN` (derived 5 → PASS) vs `B4_RED` (literal 6 → FAIL) |
| Codex F8 / Claude F3 — op 02 cwd, kit location | `01_RUNKIT` pinned as a distinct directory | runner `F1` (kit selected) / `F2` (decoy digest refused) |
| Codex F9 / Claude F3 — ops 07/08 name an absent artifact | `ACCEPTED:` root token resolving to the frozen Stage-2 directory | runner `F3` (`87157f0e…` at the accepted path) / `F4` / `F5` (both STOP) |
| Claude F6 — no fail-closed guard for `<ALLOCATE-AT-DISPATCH>` | marker gate + top-level trap | runner `E1` (`unfilled_marker field=RECORD_ROOT`, rc 3) vs `E2` (RED: localized `Test-Path` crash, rc 1) |
| Codex F10 / Claude F4 — evidence is not literal, arms undriven | this document | §6 coverage accounting |
| Claude N1 | `WPI_LOG_DIR='/var/log/mtc-bridge'` per §2 | §8 grep |
| Claude N3 | kind↔program, kind↔stdin, cwd allowlist | runner `F6`–`F9` |
| Claude N4 | record root created before the rest of preflight | every runner arm shows `TR_RECORD_ROOT` before `TR_PLAN_READ` |

## 2. Accepted-source identity precondition

```powershell
$b='MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08'
$p=@("$b\02_PREREG\remote_setup.sh","$b\02_PREREG\remote_extract_verify.sh","$b\02_PREREG\remote_close_tree.sh")
foreach($f in $p){$i=Get-Item -LiteralPath $f; "$(Split-Path $f -Leaf)`t$($i.Length)`t$((Get-FileHash -Algorithm SHA256 -LiteralPath $f).Hash.ToLowerInvariant())"}
```

```text
remote_setup.sh          4976   faee3725325d7155a6309e2371b85a4facba1980f0169c8268e47a75902821b5
remote_extract_verify.sh 8270   ba0bef0ef6ceb91c445e1d74e2c8d3b6fa7ac01e7e4e10216139b96b28c93db3
remote_close_tree.sh     7470   87157f0ea454df7c1f826a8c76a38f3045dd38efdd8fa347644f79251d3f3f0e
```

Verdict: PASS, and unchanged from round 1.

## 3. Fixture set 1 — shell side (verbatim)

`wpi_r2_shell_qa.sh`:

```bash
#!/usr/bin/env bash
# WP-I transport round 2 - shell-side RED/GREEN fixture set (standalone).
#
#   RED  = the exact audited round-1 bytes, read from commit 1c1c9ed1.
#   GREEN= the current repaired bytes in the working tree.
#
# Run it as root under WSL/Linux:
#   wsl.exe -e bash /mnt/c/.../wpi_r2_shell_qa.sh
# It creates only /wpi_r2_qa (removed at the end) and
# /mnt/c/Users/Public/wpi_r2_qa/close, which fixture set 2 consumes.
# It contacts no host and touches no repository file.
set -u
exec 2>&1          # one ordered stream, so the recorded transcript is faithful
REPO=/mnt/c/LAB/Tradingview_LAB_CLEAN
BASE=1c1c9ed1
D=MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT
ACC=$REPO/MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/02_PREREG
Q=/wpi_r2_qa
OUT=/mnt/c/Users/Public/wpi_r2_qa

rm -rf "$Q"; mkdir -m 0755 -p "$Q/bin" "$Q/shim" "$Q/head"
rm -rf "$OUT"; mkdir -p "$OUT/close"
for f in remote_setup_wpi.sh remote_extract_verify_wpi.sh run_p0.sh run_ro.sh; do
    git -C "$REPO" show "$BASE:$D/$f" >"$Q/head/$f"
done
# Pinned tool copies: this QA host ships coreutils as symlinks into a multicall
# binary, and the repaired scripts refuse a symlinked tool by design, so the
# pins are retargeted at regular root-owned 0755 copies. This is the ONLY
# substitution the tool-identity arms make.
for t in stat mkdir readlink sha256sum tar find chmod; do
    cp -L "/usr/bin/$t" "$Q/bin/$t"; chown 0:0 "$Q/bin/$t"; chmod 0755 "$Q/bin/$t"
done
echo "QA_TOOLCOPY $($Q/bin/stat --version | head -1)"
echo "QA_BASE_COMMIT $BASE"
for f in remote_setup_wpi.sh remote_extract_verify_wpi.sh run_p0.sh run_ro.sh; do
    printf 'RED_BASELINE %-30s %s\n' "$f" "$($Q/bin/sha256sum "$Q/head/$f" | cut -c1-64)"
done

dirs()  { find "$1" -mindepth 1 -type d 2>/dev/null | wc -l; }
run()   { local rc=0 pfx=""; [ $# -ge 4 ] && pfx="$4:"
          echo "=== $1 ==="; set +e; PATH="${pfx}${PATH}" bash "$2" $3 2>&1; rc=$?
          echo "RC=$rc"; }

############################################################ A. remote_setup_wpi.sh
mk_green() { # $1=out $2=parent $3=uid $4=gid [$5=stat pin]
    sed -e "s|^EXPECT_PREFIX=.*|EXPECT_PREFIX='$2/wpi_staging_'|" \
        -e "s|^EXPECT_PARENT=.*|EXPECT_PARENT='$2'|" \
        -e "s|^EXPECT_UID=.*|EXPECT_UID='$3'|" -e "s|^EXPECT_GID=.*|EXPECT_GID='$4'|" \
        -e "s|^TOOL_STAT=.*|TOOL_STAT='${5:-$Q/bin/stat}'|" \
        -e "s|^TOOL_MKDIR=.*|TOOL_MKDIR='$Q/bin/mkdir'|" \
        -e "s|^TOOL_READLINK=.*|TOOL_READLINK='$Q/bin/readlink'|" \
        "$REPO/$D/remote_setup_wpi.sh" >"$1"
}
mk_red() { # $1=out $2=parent   (round-1 bytes; sandbox prefix + owner name only)
    sed -e "s|^EXPECT_PREFIX=.*|EXPECT_PREFIX='$2/wpi_staging_'|" \
        -e "s|^EXPECT_OWNER=.*|EXPECT_OWNER='root:root'|" "$Q/head/remote_setup_wpi.sh" >"$1"
}
shim_stat() { # $1=out $2=target $3=mode(multi|oneline|alias)
    { echo '#!/bin/bash'; echo 'p="${@: -1}"'
      case "$3" in
        multi)   printf 'if [ "$p" = "%s" ] && [ ! -e "$p" ]; then\n  printf "stat: cannot stat '"'"'%%s'"'"': Permission denied\\n" "$p" >&2\n  printf "stat: cannot stat '"'"'%%s'"'"': No such file or directory\\n" "$p" >&2\n  exit 1\nfi\n' "$2" ;;
        oneline) printf 'if [ "$p" = "%s" ] && [ ! -e "$p" ]; then\n  printf "stat: cannot stat '"'"'%%s'"'"': Permission denied stat: cannot stat '"'"'%%s'"'"': No such file or directory\\n" "$p" "$p" >&2\n  exit 1\nfi\n' "$2" ;;
        alias)   printf 'if [ "$p" = "%s" ] && [ "$1" = "-c" ]; then\n  case "$2" in\n    %%u:%%g) printf "1000:1000\\n"; exit 0 ;;\n    %%U:%%G) printf "root:root\\n";  exit 0 ;;\n  esac\nfi\n' "$2" ;;
      esac
      printf 'exec %s/bin/stat "$@"\n' "$Q"
    } >"$1"; chown 0:0 "$1"; chmod 0755 "$1"
}

mkdir -m 0755 -p "$Q/a1/home/gatea"; mk_green "$Q/a1.sh" "$Q/a1/home/gatea" 0 0
run A1_GREEN_HAPPY_PATH "$Q/a1.sh" "$Q/a1/home/gatea/wpi_staging_SAFE"
echo "DIRS_CREATED=$(dirs "$Q/a1/home/gatea")"

mkdir -m 0755 -p "$Q/a2red/home/gatea" "$Q/a2green/home/gatea"
shim_stat "$Q/shim/stat" "$Q/a2red/home/gatea/wpi_staging_SAFE" multi
shim_stat "$Q/bin/stat_multi" "$Q/a2green/home/gatea/wpi_staging_SAFE" multi
mk_red "$Q/a2red.sh" "$Q/a2red/home/gatea"
run A2_RED_MIXED_DIAGNOSTIC_ROUND1_BYTES "$Q/a2red.sh" "$Q/a2red/home/gatea/wpi_staging_SAFE" "$Q/shim"
echo "DIRS_CREATED=$(dirs "$Q/a2red/home/gatea")"
mk_green "$Q/a2green.sh" "$Q/a2green/home/gatea" 0 0 "$Q/bin/stat_multi"
run A2_GREEN_MIXED_DIAGNOSTIC "$Q/a2green.sh" "$Q/a2green/home/gatea/wpi_staging_SAFE"
echo "DIRS_CREATED=$(dirs "$Q/a2green/home/gatea")"

mkdir -m 0755 -p "$Q/a3/home/gatea"
shim_stat "$Q/bin/stat_oneline" "$Q/a3/home/gatea/wpi_staging_SAFE" oneline
mk_green "$Q/a3.sh" "$Q/a3/home/gatea" 0 0 "$Q/bin/stat_oneline"
run A3_GREEN_ONE_LINE_TWO_CLASSES "$Q/a3.sh" "$Q/a3/home/gatea/wpi_staging_SAFE"
echo "DIRS_CREATED=$(dirs "$Q/a3/home/gatea")"

for v in red green; do mkdir -m 0755 -p "$Q/a4$v/home/real"; ln -s "$Q/a4$v/home/real" "$Q/a4$v/home/link"; done
mk_red "$Q/a4red.sh" "$Q/a4red/home/link"
run A4_RED_PARENT_SYMLINK_ROUND1_BYTES "$Q/a4red.sh" "$Q/a4red/home/link/wpi_staging_SAFE"
echo "DIRS_CREATED_THROUGH_LINK=$(dirs "$Q/a4red/home/real")"
mk_green "$Q/a4green.sh" "$Q/a4green/home/link" 0 0
run A4_GREEN_PARENT_SYMLINK "$Q/a4green.sh" "$Q/a4green/home/link/wpi_staging_SAFE"
echo "DIRS_CREATED_THROUGH_LINK=$(dirs "$Q/a4green/home/real")"

mkdir -m 0755 -p "$Q/a5red/home/gatea" "$Q/a5green/home/gatea"
shim_stat "$Q/shim/stat" "$Q/a5red/home/gatea/wpi_staging_SAFE" alias
shim_stat "$Q/bin/stat_alias" "$Q/a5green/home/gatea/wpi_staging_SAFE" alias
mk_red "$Q/a5red.sh" "$Q/a5red/home/gatea"
run A5_RED_NSS_ALIAS_ROUND1_BYTES "$Q/a5red.sh" "$Q/a5red/home/gatea/wpi_staging_SAFE" "$Q/shim"
mk_green "$Q/a5green.sh" "$Q/a5green/home/gatea" 0 0 "$Q/bin/stat_alias"
run A5_GREEN_NSS_ALIAS "$Q/a5green.sh" "$Q/a5green/home/gatea/wpi_staging_SAFE"

mkdir -m 0755 -p "$Q/a6/home/gatea"
sed -e "s|^EXPECT_PREFIX=.*|EXPECT_PREFIX='$Q/a6/home/gatea/wpi_staging_'|" \
    -e "s|^EXPECT_PARENT=.*|EXPECT_PARENT='$Q/a6/home/gatea'|" \
    -e "s|^TOOL_STAT=.*|TOOL_STAT='$Q/bin/stat'|" -e "s|^TOOL_MKDIR=.*|TOOL_MKDIR='$Q/bin/mkdir'|" \
    -e "s|^TOOL_READLINK=.*|TOOL_READLINK='$Q/bin/readlink'|" "$REPO/$D/remote_setup_wpi.sh" >"$Q/a6.sh"
run A6_GREEN_IDENTITY_PIN_UNFILLED "$Q/a6.sh" "$Q/a6/home/gatea/wpi_staging_SAFE"
echo "DIRS_CREATED=$(dirs "$Q/a6/home/gatea")"

mkdir -m 0755 -p "$Q/a7/home/gatea"; chmod 0777 "$Q/a7/home"
mk_green "$Q/a7.sh" "$Q/a7/home/gatea" 0 0
run A7_GREEN_WORLD_WRITABLE_ANCESTOR "$Q/a7.sh" "$Q/a7/home/gatea/wpi_staging_SAFE"
echo "DIRS_CREATED=$(dirs "$Q/a7/home/gatea")"

##################################################### B. remote_extract_verify_wpi.sh
set_block() { awk -v name="$3" -v blk="$4" '
    BEGIN{skip=0} skip==1{ if ($0 ~ /\047$/) skip=0; next }
    index($0, name "=\047")==1 { print name "=\047" blk "\047"; if ($0 !~ /\047$/) skip=1; next } {print}' "$1" >"$2"; }
mk_archive() { local d="$1"; shift; mkdir -m 0755 -p "$d/src" "$d/kit"
    local m; for m in "$@"; do printf 'fixture body for %s\n' "$m" >"$d/src/$m"; done
    ( cd "$d/src" && "$Q/bin/tar" -cf "$d/kit/runkit.tar" "$@" )
    ( cd "$d/src" && "$Q/bin/sha256sum" "$@" ) >"$d/hashes.txt"
    "$Q/bin/stat" -c '%s' "$d/kit/runkit.tar" >"$d/bytes.txt"
    "$Q/bin/sha256sum" "$d/kit/runkit.tar" | cut -d' ' -f1 >"$d/sha.txt"; }
mk_ecase() { local n="$1" v="$2" mb="$3" tv="$4"; shift 4; local d="$Q/$n$v" base
    mk_archive "$d" "$@"
    if [ "$v" = red ]; then base="$Q/head/remote_extract_verify_wpi.sh"; else base="$REPO/$D/remote_extract_verify_wpi.sh"; fi
    set_block "$base" "$d/s1.sh" MEMBERS "$mb"; set_block "$d/s1.sh" "$d/run.sh" HASHES "$(cat "$d/hashes.txt")"
    sed -i -e "s|^EXPECT_ARCHIVE_BYTES=.*|EXPECT_ARCHIVE_BYTES='$(cat "$d/bytes.txt")'|" "$d/run.sh"
    if [ "$v" = green ]; then sed -i \
        -e "s|^TOOL_STAT=.*|TOOL_STAT='$Q/bin/stat'|" -e "s|^TOOL_SHA256SUM=.*|TOOL_SHA256SUM='$Q/bin/sha256sum'|" \
        -e "s|^TOOL_TAR=.*|TOOL_TAR='${tv:-$Q/bin/tar}'|" -e "s|^TOOL_MKDIR=.*|TOOL_MKDIR='$Q/bin/mkdir'|" \
        -e "s|^TOOL_READLINK=.*|TOOL_READLINK='$Q/bin/readlink'|" -e "s|^TOOL_FIND=.*|TOOL_FIND='$Q/bin/find'|" \
        -e "s|^TOOL_CHMOD=.*|TOOL_CHMOD='$Q/bin/chmod'|" "$d/run.sh"; fi
    printf '%s\n' "$d"; }
run_ecase() { local rc=0 pfx=""; [ $# -ge 3 ] && pfx="$3:"
    echo "=== $1 ==="; set +e
    PATH="${pfx}${PATH}" bash "$2/run.sh" "$2/kit/runkit.tar" "$2/kit/extracted" "$(cat "$2/sha.txt")" 2>&1; rc=$?
    echo "RC=$rc"; }
shim_tar() { { echo '#!/bin/bash'
    case "$2" in
      warn)   echo 'case "$1" in -t*) printf "FAKE_TAR_WARNING: listing incomplete is possible\n" >&2 ;; esac' ;;
      unterm) echo 'if [ "$1" = "-tf" ]; then printf "RP0-LIB.sh\nRP0-BOOTSTRAP.sh\nRP6-P0.sh\nRP7-WPI-RO.sh\nrun_p0.sh\nrun_ro.sh"; exit 0; fi' ;;
      fail)   echo 'case "$1" in -t*) printf "tar: fixture listing failure\n" >&2; exit 2 ;; esac' ;;
    esac
    printf 'exec %s/bin/tar "$@"\n' "$Q"; } >"$1"; chown 0:0 "$1"; chmod 0755 "$1"; }
SIX='RP0-LIB.sh
RP0-BOOTSTRAP.sh
RP6-P0.sh
RP7-WPI-RO.sh
run_p0.sh
run_ro.sh'
FIVE='RP0-LIB.sh
RP0-BOOTSTRAP.sh
RP6-P0.sh
RP7-WPI-RO.sh
run_p0.sh'
M6="RP0-LIB.sh RP0-BOOTSTRAP.sh RP6-P0.sh RP7-WPI-RO.sh run_p0.sh run_ro.sh"
M5="RP0-LIB.sh RP0-BOOTSTRAP.sh RP6-P0.sh RP7-WPI-RO.sh run_p0.sh"

run_ecase B1_GREEN_HAPPY_PATH "$(mk_ecase b1 green "$SIX" "" $M6)"
shim_tar "$Q/bin/tar_warn" warn; cp "$Q/bin/tar_warn" "$Q/shim/tar"; chmod 0755 "$Q/shim/tar"
run_ecase B2_RED_LISTING_WARNING_ROUND1_BYTES "$(mk_ecase b2 red "$SIX" "" $M6)" "$Q/shim"
run_ecase B2_GREEN_LISTING_WARNING "$(mk_ecase b2 green "$SIX" "$Q/bin/tar_warn" $M6)"
shim_tar "$Q/bin/tar_unterm" unterm; cp "$Q/bin/tar_unterm" "$Q/shim/tar"; chmod 0755 "$Q/shim/tar"
run_ecase B3_RED_UNTERMINATED_LISTING_ROUND1_BYTES "$(mk_ecase b3 red "$SIX" "" $M6)" "$Q/shim"
run_ecase B3_GREEN_UNTERMINATED_LISTING "$(mk_ecase b3 green "$SIX" "$Q/bin/tar_unterm" $M6)"
run_ecase B4_RED_FIVE_MEMBERS_AGAINST_LITERAL_SIX "$(mk_ecase b4 red "$FIVE" "" $M5)"
run_ecase B4_GREEN_FIVE_MEMBERS_DERIVED_COUNT "$(mk_ecase b4 green "$FIVE" "" $M5)"
shim_tar "$Q/shim/tar" warn
run_ecase B5_GREEN_PLANTED_PATH_TAR_IGNORED "$(mk_ecase b5 green "$SIX" "" $M6)" "$Q/shim"
shim_tar "$Q/bin/tar_fail" fail
run_ecase B6_GREEN_LISTING_HARD_FAILURE "$(mk_ecase b6 green "$SIX" "$Q/bin/tar_fail" $M6)"

################################################################ C. the two wrappers
mk_wcase() { local c="$Q/$1" k="$2" v="$3" E T P W L B H src
    E="$c/extracted"; mkdir -p "$E" "$c/evidence/runkit"
    printf 'rp0_require_safe_component(){ return 0; }\nrp0_allocate_evidence_dir(){ return 0; }\n' >"$E/RP0-LIB.sh"
    printf 'EV_DIR="$EV_RUNKIT/$RUNID"\nmkdir -m 0700 -- "$EV_DIR"\nEV_LOG="$EV_DIR/${EV_STAGE_ID}.log"\n: >"$EV_LOG"\nexec >>"$EV_LOG" 2>&1\n' >"$E/RP0-BOOTSTRAP.sh"
    if [ "$k" = p0 ]; then T=RP6-P0.sh; P=P0W; W=run_p0.sh; else T=RP7-WPI-RO.sh; P=ROW; W=run_ro.sh; fi
    printf 'if IFS= read -r stolen; then printf %s_FIXTURE" stdin=stolen\\n"; exit 1; fi\nprintf %s_FIXTURE" stdin=eof\\n"\n' "$P" "$P" >"$E/$T"
    L=$("$Q/bin/sha256sum" "$E/RP0-LIB.sh"); L=${L%% *}
    B=$("$Q/bin/sha256sum" "$E/RP0-BOOTSTRAP.sh"); B=${B%% *}
    H=$("$Q/bin/sha256sum" "$E/$T"); H=${H%% *}
    if [ "$v" = red ]; then src="$Q/head/$W"; else src="$REPO/$D/$W"; fi
    sed -e "s|^BASE_RUN=.*|BASE_RUN='QA'|" -e "s|^REMOTE_BASE=.*|REMOTE_BASE='$c'|" \
        -e "s|^EXTRACT_DIR=.*|EXTRACT_DIR='$E'|" -e "s|^RUNID=.*|RUNID='QA-$k'|" \
        -e "s|^EV_PARENT=.*|EV_PARENT='$c/evidence'|" -e "s|^EV_RUNKIT=.*|EV_RUNKIT='$c/evidence/runkit'|" \
        -e "s|^RP0_LIB_SHA=.*|RP0_LIB_SHA='$L'|" -e "s|^RP0_BOOTSTRAP_SHA=.*|RP0_BOOTSTRAP_SHA='$B'|" \
        -e "s|^RP6_P0_SHA=.*|RP6_P0_SHA='$H'|" -e "s|^RP7_WPI_RO_SHA=.*|RP7_WPI_RO_SHA='$H'|" \
        -e "s|^TOOL_STAT=.*|TOOL_STAT='$Q/bin/stat'|" -e "s|^TOOL_SHA256SUM=.*|TOOL_SHA256SUM='$Q/bin/sha256sum'|" \
        "$src" >"$c/wrapper.sh"
    printf '%s|%s|%s|%s\n' "$c" "$E" "$T" "$P"; }
stream() { { cat "$1"; printf "printf 'TAIL_EXECUTED\\n'\\n"; } | bash --noprofile --norc -s; }
runw()  { local rc=0 pfx=""; [ $# -ge 5 ] && pfx="$5:"
    echo "=== $1 ==="; set +e; PATH="${pfx}${PATH}" stream "$2"; rc=$?
    [ -f "$3/evidence/runkit/QA-$4/$4.log" ] && cat "$3/evidence/runkit/QA-$4/$4.log"
    echo "RC=$rc"; }

for k in p0 ro; do
    U=$(echo "$k" | tr a-z A-Z)
    IFS='|' read -r C E T P < <(mk_wcase "${k}lr" "$k" red)
    mv "$E/$T" "$E/$T.real"; ln -s "$T.real" "$E/$T"
    sed '/\[ ! -L "\$path" \] ||/d' "$C/wrapper.sh" >"$C/red.sh"
    runw "${U}_LINK_RED_NO_SYMLINK_REFUSAL" "$C/red.sh" "$C" "$k"
    IFS='|' read -r C E T P < <(mk_wcase "${k}lg" "$k" green)
    mv "$E/$T" "$E/$T.real"; ln -s "$T.real" "$E/$T"
    runw "${U}_LINK_GREEN" "$C/wrapper.sh" "$C" "$k"
    IFS='|' read -r C E T P < <(mk_wcase "${k}sr" "$k" red)
    sed "s|\. \"\$EXTRACT_DIR/$T\" </dev/null|. \"\$EXTRACT_DIR/$T\"|" "$C/wrapper.sh" >"$C/red.sh"
    runw "${U}_STDIN_RED_NO_DEV_NULL" "$C/red.sh" "$C" "$k"
    IFS='|' read -r C E T P < <(mk_wcase "${k}sg" "$k" green)
    runw "${U}_STDIN_GREEN" "$C/wrapper.sh" "$C" "$k"
    IFS='|' read -r C E T P < <(mk_wcase "${k}hr" "$k" red)
    printf 'printf %s_HIJACKED_BLOCK_EXECUTED"\\n"\n' "$P" >"$E/$T"
    FROZEN=$(grep -oE "SHA='[0-9a-f]{64}'" "$C/wrapper.sh" | tail -1 | grep -oE '[0-9a-f]{64}')
    { echo '#!/bin/bash'
      printf 'for a in "$@"; do case "$a" in */%s) printf "%s  %%s\\n" "$a"; exit 0 ;; esac; done\n' "$T" "$FROZEN"
      printf 'exec %s/bin/sha256sum "$@"\n' "$Q"; } >"$Q/shim/sha256sum"; chmod 0755 "$Q/shim/sha256sum"
    runw "${U}_HIJACK_RED_PATH_RESOLVED_DIGEST_TOOL" "$C/wrapper.sh" "$C" "$k" "$Q/shim"
    IFS='|' read -r C E T P < <(mk_wcase "${k}hg" "$k" green)
    printf 'printf %s_HIJACKED_BLOCK_EXECUTED"\\n"\n' "$P" >"$E/$T"
    runw "${U}_HIJACK_GREEN_PINNED_DIGEST_TOOL" "$C/wrapper.sh" "$C" "$k" "$Q/shim"
done
IFS='|' read -r C E T P < <(mk_wcase p0ts p0 green)
ln -s "$Q/bin/sha256sum" "$Q/bin/sha256sum_link"
sed -i "s|^TOOL_SHA256SUM=.*|TOOL_SHA256SUM='$Q/bin/sha256sum_link'|" "$C/wrapper.sh"
runw P0_TOOL_IS_SYMLINK "$C/wrapper.sh" "$C" p0
IFS='|' read -r C E T P < <(mk_wcase p0tw p0 green)
cp "$Q/bin/sha256sum" "$Q/bin/sha256sum_ww"; chown 0:0 "$Q/bin/sha256sum_ww"; chmod 0757 "$Q/bin/sha256sum_ww"
sed -i "s|^TOOL_SHA256SUM=.*|TOOL_SHA256SUM='$Q/bin/sha256sum_ww'|" "$C/wrapper.sh"
runw P0_TOOL_OTHER_WRITABLE "$C/wrapper.sh" "$C" p0

######################################## D. real remote_close_tree.sh transcripts
echo "=== CLOSE_TRANSCRIPTS ==="
echo "ACCEPTED_SOURCE $("$Q/bin/sha256sum" "$ACC/remote_close_tree.sh" | cut -d' ' -f1) bytes=$("$Q/bin/stat" -c %s "$ACC/remote_close_tree.sh")"
sed "s|^EXPECT_OWNER='gatea:gatea'|EXPECT_OWNER='root:root'|" "$ACC/remote_close_tree.sh" >"$Q/close.sh"
echo "--- the only substitution ---"; diff "$ACC/remote_close_tree.sh" "$Q/close.sh" || true; echo "--- end diff ---"
for R in QA-P0 QA-RO; do
    EV="$Q/ev/runkit/$R"; mkdir -m 0700 -p "$Q/ev/runkit"; mkdir -m 0700 "$EV"; mkdir -m 0700 "$EV/sub"
    printf 'alpha evidence line for %s\n' "$R" >"$EV/aaa.txt"
    printf 'stage log for %s\nsecond line\n' "$R" >"$EV/stage.log"
    printf 'nested evidence for %s\n' "$R" >"$EV/sub/nested.txt"
    chmod 0600 "$EV/aaa.txt" "$EV/stage.log" "$EV/sub/nested.txt"
    rc=0; bash "$Q/close.sh" "$EV" "$R" >"$OUT/close/$R.stdout" 2>"$OUT/close/$R.stderr" || rc=$?
    echo "--- CLOSE $R rc=$rc ---"; cat "$OUT/close/$R.stdout"
    [ -s "$OUT/close/$R.stderr" ] && { echo "--stderr--"; cat "$OUT/close/$R.stderr"; }
    mkdir -p "$OUT/close/tree/$R"; cp -a "$EV/." "$OUT/close/tree/$R/"
done
rm -rf "$Q"
echo "=== WPI_R2_SHELL_QA_COMPLETE (fixture root removed; only $OUT/close remains) ==="
```

Real output (S1 applied; nothing else altered):

```text
QA_TOOLCOPY stat (uutils coreutils) 0.8.0
QA_BASE_COMMIT 1c1c9ed1
RED_BASELINE remote_setup_wpi.sh            5b2598184b228eef5d93c7f4ef7a5aa8a627ffbdea8c71e6cc093b416ebb0a34
RED_BASELINE remote_extract_verify_wpi.sh   17ed8f3f8d80a79fc1b132ff1ef55cf0677da13c551da30e0db7531935c1f6f2
RED_BASELINE run_p0.sh                      8b2c520aa342f3f49fc9f0ad543b6c8a918c995b66e1cae8a1dd1c543b9dbfe9
RED_BASELINE run_ro.sh                      88f9f736e68c4978cc15d29621082d0395dc49de97a4c8efc79893fc536ad3e0
=== A1_GREEN_HAPPY_PATH ===
SETUP_NOTE tool name=stat path=<QA>/bin/stat owner_numeric=0:0 mode=755 resolution=pinned_absolute
SETUP_NOTE tool name=mkdir path=<QA>/bin/mkdir owner_numeric=0:0 mode=755 resolution=pinned_absolute
SETUP_NOTE tool name=readlink path=<QA>/bin/readlink owner_numeric=0:0 mode=755 resolution=pinned_absolute
SETUP_NOTE identity euid=0 expected_numeric=0:0 name_diagnostic=gatea:gatea
SETUP_NOTE base_component_ok value=SAFE
SETUP_NOTE parent_bound path=/ owner_numeric=0:0 owner_name=root:root mode=755
SETUP_NOTE parent_bound path=<QA> owner_numeric=0:0 owner_name=root:root mode=755
SETUP_NOTE parent_bound path=<QA>/a1 owner_numeric=0:0 owner_name=root:root mode=755
SETUP_NOTE parent_bound path=<QA>/a1/home owner_numeric=0:0 owner_name=root:root mode=755
SETUP_NOTE parent_bound path=<QA>/a1/home/gatea owner_numeric=0:0 owner_name=root:root mode=755
SETUP_NOTE enoent_calibration rc=1 template=stat: cannot stat '@PATH@': No such file or directory (os error 2)
SETUP_NOTE base_absent path=<QA>/a1/home/gatea/wpi_staging_SAFE
SETUP_NOTE allocated path=<QA>/a1/home/gatea/wpi_staging_SAFE
SETUP_NOTE dir_ok path=<QA>/a1/home/gatea/wpi_staging_SAFE owner_numeric=0:0 owner_name=root:root mode=700
SETUP_NOTE allocated path=<QA>/a1/home/gatea/wpi_staging_SAFE/evidence
SETUP_NOTE dir_ok path=<QA>/a1/home/gatea/wpi_staging_SAFE/evidence owner_numeric=0:0 owner_name=root:root mode=700
SETUP_NOTE allocated path=<QA>/a1/home/gatea/wpi_staging_SAFE/evidence/runkit
SETUP_NOTE dir_ok path=<QA>/a1/home/gatea/wpi_staging_SAFE/evidence/runkit owner_numeric=0:0 owner_name=root:root mode=700
SETUP_NOTE allocated path=<QA>/a1/home/gatea/wpi_staging_SAFE/kit
SETUP_NOTE dir_ok path=<QA>/a1/home/gatea/wpi_staging_SAFE/kit owner_numeric=0:0 owner_name=root:root mode=700
SETUP PASS base=<QA>/a1/home/gatea/wpi_staging_SAFE evidence=<QA>/a1/home/gatea/wpi_staging_SAFE/evidence runkit=<QA>/a1/home/gatea/wpi_staging_SAFE/evidence/runkit kit=<QA>/a1/home/gatea/wpi_staging_SAFE/kit owner_numeric=0:0 owner_name=gatea:gatea mode=700
RC=0
DIRS_CREATED=4
=== A2_RED_MIXED_DIAGNOSTIC_ROUND1_BYTES ===
SETUP_NOTE base_component_ok value=SAFE
SETUP_NOTE base_absent path=<QA>/a2red/home/gatea/wpi_staging_SAFE
SETUP_NOTE allocated path=<QA>/a2red/home/gatea/wpi_staging_SAFE
SETUP_NOTE allocated path=<QA>/a2red/home/gatea/wpi_staging_SAFE/evidence
SETUP_NOTE allocated path=<QA>/a2red/home/gatea/wpi_staging_SAFE/evidence/runkit
SETUP_NOTE allocated path=<QA>/a2red/home/gatea/wpi_staging_SAFE/kit
SETUP_NOTE dir_ok path=<QA>/a2red/home/gatea/wpi_staging_SAFE owner=root:root mode=700
SETUP_NOTE dir_ok path=<QA>/a2red/home/gatea/wpi_staging_SAFE/evidence owner=root:root mode=700
SETUP_NOTE dir_ok path=<QA>/a2red/home/gatea/wpi_staging_SAFE/evidence/runkit owner=root:root mode=700
SETUP_NOTE dir_ok path=<QA>/a2red/home/gatea/wpi_staging_SAFE/kit owner=root:root mode=700
SETUP PASS base=<QA>/a2red/home/gatea/wpi_staging_SAFE evidence=<QA>/a2red/home/gatea/wpi_staging_SAFE/evidence runkit=<QA>/a2red/home/gatea/wpi_staging_SAFE/evidence/runkit kit=<QA>/a2red/home/gatea/wpi_staging_SAFE/kit owner=root:root mode=700
RC=0
DIRS_CREATED=4
=== A2_GREEN_MIXED_DIAGNOSTIC ===
SETUP_NOTE tool name=stat_multi path=<QA>/bin/stat_multi owner_numeric=0:0 mode=755 resolution=pinned_absolute
SETUP_NOTE tool name=mkdir path=<QA>/bin/mkdir owner_numeric=0:0 mode=755 resolution=pinned_absolute
SETUP_NOTE tool name=readlink path=<QA>/bin/readlink owner_numeric=0:0 mode=755 resolution=pinned_absolute
SETUP_NOTE identity euid=0 expected_numeric=0:0 name_diagnostic=gatea:gatea
SETUP_NOTE base_component_ok value=SAFE
SETUP_NOTE parent_bound path=/ owner_numeric=0:0 owner_name=root:root mode=755
SETUP_NOTE parent_bound path=<QA> owner_numeric=0:0 owner_name=root:root mode=755
SETUP_NOTE parent_bound path=<QA>/a2green owner_numeric=0:0 owner_name=root:root mode=755
SETUP_NOTE parent_bound path=<QA>/a2green/home owner_numeric=0:0 owner_name=root:root mode=755
SETUP_NOTE parent_bound path=<QA>/a2green/home/gatea owner_numeric=0:0 owner_name=root:root mode=755
SETUP_NOTE enoent_calibration rc=1 template=stat: cannot stat '@PATH@': No such file or directory (os error 2)
SETUP_STOP reason=path_probe_multiline path=<QA>/a2green/home/gatea/wpi_staging_SAFE rc=1
RC=3
DIRS_CREATED=0
=== A3_GREEN_ONE_LINE_TWO_CLASSES ===
SETUP_NOTE tool name=stat_oneline path=<QA>/bin/stat_oneline owner_numeric=0:0 mode=755 resolution=pinned_absolute
SETUP_NOTE tool name=mkdir path=<QA>/bin/mkdir owner_numeric=0:0 mode=755 resolution=pinned_absolute
SETUP_NOTE tool name=readlink path=<QA>/bin/readlink owner_numeric=0:0 mode=755 resolution=pinned_absolute
SETUP_NOTE identity euid=0 expected_numeric=0:0 name_diagnostic=gatea:gatea
SETUP_NOTE base_component_ok value=SAFE
SETUP_NOTE parent_bound path=/ owner_numeric=0:0 owner_name=root:root mode=755
SETUP_NOTE parent_bound path=<QA> owner_numeric=0:0 owner_name=root:root mode=755
SETUP_NOTE parent_bound path=<QA>/a3 owner_numeric=0:0 owner_name=root:root mode=755
SETUP_NOTE parent_bound path=<QA>/a3/home owner_numeric=0:0 owner_name=root:root mode=755
SETUP_NOTE parent_bound path=<QA>/a3/home/gatea owner_numeric=0:0 owner_name=root:root mode=755
SETUP_NOTE enoent_calibration rc=1 template=stat: cannot stat '@PATH@': No such file or directory (os error 2)
SETUP_STOP reason=path_probe_unclassified path=<QA>/a3/home/gatea/wpi_staging_SAFE rc=1 detail=stat: cannot stat '<QA>/a3/home/gatea/wpi_staging_SAFE': Permission denied stat: cannot stat '<QA>/a3/home/gatea/wpi_staging_SAFE': No such file or directory
RC=3
DIRS_CREATED=0
=== A4_RED_PARENT_SYMLINK_ROUND1_BYTES ===
SETUP_NOTE base_component_ok value=SAFE
SETUP_NOTE base_absent path=<QA>/a4red/home/link/wpi_staging_SAFE
SETUP_NOTE allocated path=<QA>/a4red/home/link/wpi_staging_SAFE
SETUP_NOTE allocated path=<QA>/a4red/home/link/wpi_staging_SAFE/evidence
SETUP_NOTE allocated path=<QA>/a4red/home/link/wpi_staging_SAFE/evidence/runkit
SETUP_NOTE allocated path=<QA>/a4red/home/link/wpi_staging_SAFE/kit
SETUP_FAIL reason=path_not_canonical path=<QA>/a4red/home/link/wpi_staging_SAFE canonical=<QA>/a4red/home/real/wpi_staging_SAFE
RC=1
DIRS_CREATED_THROUGH_LINK=4
=== A4_GREEN_PARENT_SYMLINK ===
SETUP_NOTE tool name=stat path=<QA>/bin/stat owner_numeric=0:0 mode=755 resolution=pinned_absolute
SETUP_NOTE tool name=mkdir path=<QA>/bin/mkdir owner_numeric=0:0 mode=755 resolution=pinned_absolute
SETUP_NOTE tool name=readlink path=<QA>/bin/readlink owner_numeric=0:0 mode=755 resolution=pinned_absolute
SETUP_NOTE identity euid=0 expected_numeric=0:0 name_diagnostic=gatea:gatea
SETUP_NOTE base_component_ok value=SAFE
SETUP_FAIL reason=parent_not_canonical path=<QA>/a4green/home/link canonical=<QA>/a4green/home/real
RC=1
DIRS_CREATED_THROUGH_LINK=0
=== A5_RED_NSS_ALIAS_ROUND1_BYTES ===
SETUP_NOTE base_component_ok value=SAFE
SETUP_NOTE base_absent path=<QA>/a5red/home/gatea/wpi_staging_SAFE
SETUP_NOTE allocated path=<QA>/a5red/home/gatea/wpi_staging_SAFE
SETUP_NOTE allocated path=<QA>/a5red/home/gatea/wpi_staging_SAFE/evidence
SETUP_NOTE allocated path=<QA>/a5red/home/gatea/wpi_staging_SAFE/evidence/runkit
SETUP_NOTE allocated path=<QA>/a5red/home/gatea/wpi_staging_SAFE/kit
SETUP_NOTE dir_ok path=<QA>/a5red/home/gatea/wpi_staging_SAFE owner=root:root mode=700
SETUP_NOTE dir_ok path=<QA>/a5red/home/gatea/wpi_staging_SAFE/evidence owner=root:root mode=700
SETUP_NOTE dir_ok path=<QA>/a5red/home/gatea/wpi_staging_SAFE/evidence/runkit owner=root:root mode=700
SETUP_NOTE dir_ok path=<QA>/a5red/home/gatea/wpi_staging_SAFE/kit owner=root:root mode=700
SETUP PASS base=<QA>/a5red/home/gatea/wpi_staging_SAFE evidence=<QA>/a5red/home/gatea/wpi_staging_SAFE/evidence runkit=<QA>/a5red/home/gatea/wpi_staging_SAFE/evidence/runkit kit=<QA>/a5red/home/gatea/wpi_staging_SAFE/kit owner=root:root mode=700
RC=0
=== A5_GREEN_NSS_ALIAS ===
SETUP_NOTE tool name=stat_alias path=<QA>/bin/stat_alias owner_numeric=0:0 mode=755 resolution=pinned_absolute
SETUP_NOTE tool name=mkdir path=<QA>/bin/mkdir owner_numeric=0:0 mode=755 resolution=pinned_absolute
SETUP_NOTE tool name=readlink path=<QA>/bin/readlink owner_numeric=0:0 mode=755 resolution=pinned_absolute
SETUP_NOTE identity euid=0 expected_numeric=0:0 name_diagnostic=gatea:gatea
SETUP_NOTE base_component_ok value=SAFE
SETUP_NOTE parent_bound path=/ owner_numeric=0:0 owner_name=root:root mode=755
SETUP_NOTE parent_bound path=<QA> owner_numeric=0:0 owner_name=root:root mode=755
SETUP_NOTE parent_bound path=<QA>/a5green owner_numeric=0:0 owner_name=root:root mode=755
SETUP_NOTE parent_bound path=<QA>/a5green/home owner_numeric=0:0 owner_name=root:root mode=755
SETUP_NOTE parent_bound path=<QA>/a5green/home/gatea owner_numeric=0:0 owner_name=root:root mode=755
SETUP_NOTE enoent_calibration rc=1 template=stat: cannot stat '@PATH@': No such file or directory (os error 2)
SETUP_NOTE base_absent path=<QA>/a5green/home/gatea/wpi_staging_SAFE
SETUP_NOTE allocated path=<QA>/a5green/home/gatea/wpi_staging_SAFE
SETUP_FAIL reason=owner_numeric=1000:1000 expected=0:0 path=<QA>/a5green/home/gatea/wpi_staging_SAFE owner_name=root:root
RC=1
=== A6_GREEN_IDENTITY_PIN_UNFILLED ===
SETUP_NOTE tool name=stat path=<QA>/bin/stat owner_numeric=0:0 mode=755 resolution=pinned_absolute
SETUP_NOTE tool name=mkdir path=<QA>/bin/mkdir owner_numeric=0:0 mode=755 resolution=pinned_absolute
SETUP_NOTE tool name=readlink path=<QA>/bin/readlink owner_numeric=0:0 mode=755 resolution=pinned_absolute
SETUP_STOP reason=identity_pin_unfilled field=EXPECT_UID
RC=3
DIRS_CREATED=0
=== A7_GREEN_WORLD_WRITABLE_ANCESTOR ===
SETUP_NOTE tool name=stat path=<QA>/bin/stat owner_numeric=0:0 mode=755 resolution=pinned_absolute
SETUP_NOTE tool name=mkdir path=<QA>/bin/mkdir owner_numeric=0:0 mode=755 resolution=pinned_absolute
SETUP_NOTE tool name=readlink path=<QA>/bin/readlink owner_numeric=0:0 mode=755 resolution=pinned_absolute
SETUP_NOTE identity euid=0 expected_numeric=0:0 name_diagnostic=gatea:gatea
SETUP_NOTE base_component_ok value=SAFE
SETUP_NOTE parent_bound path=/ owner_numeric=0:0 owner_name=root:root mode=755
SETUP_NOTE parent_bound path=<QA> owner_numeric=0:0 owner_name=root:root mode=755
SETUP_NOTE parent_bound path=<QA>/a7 owner_numeric=0:0 owner_name=root:root mode=755
SETUP_FAIL reason=parent_other_writable mode=777 path=<QA>/a7/home
RC=1
DIRS_CREATED=0
=== B1_GREEN_HAPPY_PATH ===
EXTRACT_NOTE tool name=stat path=<QA>/bin/stat owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE tool name=sha256sum path=<QA>/bin/sha256sum owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE tool name=tar path=<QA>/bin/tar owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE tool name=mkdir path=<QA>/bin/mkdir owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE tool name=readlink path=<QA>/bin/readlink owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE tool name=find path=<QA>/bin/find owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE tool name=chmod path=<QA>/bin/chmod owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE member_constant count=6 source=MEMBERS
EXTRACT_NOTE parent_bound path=<QA>/b1green/kit owner_uid=0 mode=755
EXTRACT_NOTE enoent_calibration rc=1 template=stat: cannot stat '@PATH@': No such file or directory (os error 2)
EXTRACT_archive path=<QA>/b1green/kit/runkit.tar bytes=10240
EXTRACT_archive_sha256 actual=cb0bbbaf36b4f16956ea2faacd818f0bb43aa83d99c3784a8d1b0599363f697e expected=cb0bbbaf36b4f16956ea2faacd818f0bb43aa83d99c3784a8d1b0599363f697e
EXTRACT_NOTE members_exact count=6 order=stage1
EXTRACT_NOTE extract_dir_allocated path=<QA>/b1green/kit/extracted
EXTRACT_NOTE extracted_files_readonly mode=0444
EXTRACT_block name=RP0-LIB.sh sha256=cdb08f04ae0e78e18be2ac75fab6c56e0410345fa7846b8a399849a9d46007d5
EXTRACT_block name=RP0-BOOTSTRAP.sh sha256=9014464ca51250132ac02b0406eb9d3cc9fba2ce5c214f25b790a22749386d2b
EXTRACT_block name=RP6-P0.sh sha256=60b632bc0f914309c5451e928e81cd7a2fd8c2faceaa61a0f3f65151bd8a8cf0
EXTRACT_block name=RP7-WPI-RO.sh sha256=05754d3bc0e44cce897bb7c47de2993cbb32077920296fbe321595c3fd304958
EXTRACT_block name=run_p0.sh sha256=7b4d63257cdf3576b16a8124b68844a2d6284294eb870f590c306dc2c8c6b200
EXTRACT_block name=run_ro.sh sha256=e58c4c5b619f684169973224e37e7e6594e56644a81c31bf7d2b23ce7bfb6b1a
EXTRACT PASS archive=<QA>/b1green/kit/runkit.tar archive_sha256=cb0bbbaf36b4f16956ea2faacd818f0bb43aa83d99c3784a8d1b0599363f697e dir=<QA>/b1green/kit/extracted members=6 verified=6 executed=0
RC=0
=== B2_RED_LISTING_WARNING_ROUND1_BYTES ===
EXTRACT_archive path=<QA>/b2red/kit/runkit.tar bytes=10240
EXTRACT_archive_sha256 actual=cb0bbbaf36b4f16956ea2faacd818f0bb43aa83d99c3784a8d1b0599363f697e expected=cb0bbbaf36b4f16956ea2faacd818f0bb43aa83d99c3784a8d1b0599363f697e
FAKE_TAR_WARNING: listing incomplete is possible
FAKE_TAR_WARNING: listing incomplete is possible
EXTRACT_NOTE members_exact count=6 order=stage1
EXTRACT_NOTE extract_dir_allocated path=<QA>/b2red/kit/extracted
EXTRACT_NOTE extracted_files_readonly mode=0444
RP0-LIB.sh: OK
RP0-BOOTSTRAP.sh: OK
RP6-P0.sh: OK
RP7-WPI-RO.sh: OK
run_p0.sh: OK
run_ro.sh: OK
EXTRACT_block name=RP0-LIB.sh sha256=cdb08f04ae0e78e18be2ac75fab6c56e0410345fa7846b8a399849a9d46007d5
EXTRACT_block name=RP0-BOOTSTRAP.sh sha256=9014464ca51250132ac02b0406eb9d3cc9fba2ce5c214f25b790a22749386d2b
EXTRACT_block name=RP6-P0.sh sha256=60b632bc0f914309c5451e928e81cd7a2fd8c2faceaa61a0f3f65151bd8a8cf0
EXTRACT_block name=RP7-WPI-RO.sh sha256=05754d3bc0e44cce897bb7c47de2993cbb32077920296fbe321595c3fd304958
EXTRACT_block name=run_p0.sh sha256=7b4d63257cdf3576b16a8124b68844a2d6284294eb870f590c306dc2c8c6b200
EXTRACT_block name=run_ro.sh sha256=e58c4c5b619f684169973224e37e7e6594e56644a81c31bf7d2b23ce7bfb6b1a
EXTRACT PASS archive=<QA>/b2red/kit/runkit.tar archive_sha256=cb0bbbaf36b4f16956ea2faacd818f0bb43aa83d99c3784a8d1b0599363f697e dir=<QA>/b2red/kit/extracted members=6 verified=6 executed=0
RC=0
=== B2_GREEN_LISTING_WARNING ===
EXTRACT_NOTE tool name=stat path=<QA>/bin/stat owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE tool name=sha256sum path=<QA>/bin/sha256sum owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE tool name=tar_warn path=<QA>/bin/tar_warn owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE tool name=mkdir path=<QA>/bin/mkdir owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE tool name=readlink path=<QA>/bin/readlink owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE tool name=find path=<QA>/bin/find owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE tool name=chmod path=<QA>/bin/chmod owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE member_constant count=6 source=MEMBERS
EXTRACT_NOTE parent_bound path=<QA>/b2green/kit owner_uid=0 mode=755
EXTRACT_NOTE enoent_calibration rc=1 template=stat: cannot stat '@PATH@': No such file or directory (os error 2)
EXTRACT_archive path=<QA>/b2green/kit/runkit.tar bytes=10240
EXTRACT_archive_sha256 actual=cb0bbbaf36b4f16956ea2faacd818f0bb43aa83d99c3784a8d1b0599363f697e expected=cb0bbbaf36b4f16956ea2faacd818f0bb43aa83d99c3784a8d1b0599363f697e
EXTRACT_STOP reason=tar_type_listing_diagnostics detail=FAKE_TAR_WARNING: listing incomplete is possible
-rw-r--r-- root/root        28 2026-08-10 13:36 RP0-LIB.sh
-rw-r--r-- root/root        34 2026-08-10 13:36 RP0-BOOTSTRAP.sh
-rw-r--r-- root/root        27 2026-08-10 13:36 RP6-P0.sh
-rw-r--r-- root/root        31 2026-08-10 13:36 RP7-WPI-RO.sh
-rw-r--r-- root/root        27 2026-08-10 13:36 run_p0.sh
-rw-r--r-- root/root        27 2026-08-10 13:36 run_ro.sh

RC=3
=== B3_RED_UNTERMINATED_LISTING_ROUND1_BYTES ===
EXTRACT_archive path=<QA>/b3red/kit/runkit.tar bytes=10240
EXTRACT_archive_sha256 actual=cb0bbbaf36b4f16956ea2faacd818f0bb43aa83d99c3784a8d1b0599363f697e expected=cb0bbbaf36b4f16956ea2faacd818f0bb43aa83d99c3784a8d1b0599363f697e
EXTRACT_NOTE members_exact count=6 order=stage1
EXTRACT_NOTE extract_dir_allocated path=<QA>/b3red/kit/extracted
EXTRACT_NOTE extracted_files_readonly mode=0444
RP0-LIB.sh: OK
RP0-BOOTSTRAP.sh: OK
RP6-P0.sh: OK
RP7-WPI-RO.sh: OK
run_p0.sh: OK
run_ro.sh: OK
EXTRACT_block name=RP0-LIB.sh sha256=cdb08f04ae0e78e18be2ac75fab6c56e0410345fa7846b8a399849a9d46007d5
EXTRACT_block name=RP0-BOOTSTRAP.sh sha256=9014464ca51250132ac02b0406eb9d3cc9fba2ce5c214f25b790a22749386d2b
EXTRACT_block name=RP6-P0.sh sha256=60b632bc0f914309c5451e928e81cd7a2fd8c2faceaa61a0f3f65151bd8a8cf0
EXTRACT_block name=RP7-WPI-RO.sh sha256=05754d3bc0e44cce897bb7c47de2993cbb32077920296fbe321595c3fd304958
EXTRACT_block name=run_p0.sh sha256=7b4d63257cdf3576b16a8124b68844a2d6284294eb870f590c306dc2c8c6b200
EXTRACT_block name=run_ro.sh sha256=e58c4c5b619f684169973224e37e7e6594e56644a81c31bf7d2b23ce7bfb6b1a
EXTRACT PASS archive=<QA>/b3red/kit/runkit.tar archive_sha256=cb0bbbaf36b4f16956ea2faacd818f0bb43aa83d99c3784a8d1b0599363f697e dir=<QA>/b3red/kit/extracted members=6 verified=6 executed=0
RC=0
=== B3_GREEN_UNTERMINATED_LISTING ===
EXTRACT_NOTE tool name=stat path=<QA>/bin/stat owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE tool name=sha256sum path=<QA>/bin/sha256sum owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE tool name=tar_unterm path=<QA>/bin/tar_unterm owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE tool name=mkdir path=<QA>/bin/mkdir owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE tool name=readlink path=<QA>/bin/readlink owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE tool name=find path=<QA>/bin/find owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE tool name=chmod path=<QA>/bin/chmod owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE member_constant count=6 source=MEMBERS
EXTRACT_NOTE parent_bound path=<QA>/b3green/kit owner_uid=0 mode=755
EXTRACT_NOTE enoent_calibration rc=1 template=stat: cannot stat '@PATH@': No such file or directory (os error 2)
EXTRACT_archive path=<QA>/b3green/kit/runkit.tar bytes=10240
EXTRACT_archive_sha256 actual=cb0bbbaf36b4f16956ea2faacd818f0bb43aa83d99c3784a8d1b0599363f697e expected=cb0bbbaf36b4f16956ea2faacd818f0bb43aa83d99c3784a8d1b0599363f697e
EXTRACT_STOP reason=tar_name_listing_unterminated_final_record
RC=3
=== B4_RED_FIVE_MEMBERS_AGAINST_LITERAL_SIX ===
EXTRACT_archive path=<QA>/b4red/kit/runkit.tar bytes=10240
EXTRACT_archive_sha256 actual=509dd1ac27362d1fc46ebf89af11801a466b85b6e0becee907d813de6bb4fa9a expected=509dd1ac27362d1fc46ebf89af11801a466b85b6e0becee907d813de6bb4fa9a
EXTRACT_FAIL reason=tar_member_count=5 expected=6
RC=1
=== B4_GREEN_FIVE_MEMBERS_DERIVED_COUNT ===
EXTRACT_NOTE tool name=stat path=<QA>/bin/stat owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE tool name=sha256sum path=<QA>/bin/sha256sum owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE tool name=tar path=<QA>/bin/tar owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE tool name=mkdir path=<QA>/bin/mkdir owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE tool name=readlink path=<QA>/bin/readlink owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE tool name=find path=<QA>/bin/find owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE tool name=chmod path=<QA>/bin/chmod owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE member_constant count=5 source=MEMBERS
EXTRACT_NOTE parent_bound path=<QA>/b4green/kit owner_uid=0 mode=755
EXTRACT_NOTE enoent_calibration rc=1 template=stat: cannot stat '@PATH@': No such file or directory (os error 2)
EXTRACT_archive path=<QA>/b4green/kit/runkit.tar bytes=10240
EXTRACT_archive_sha256 actual=509dd1ac27362d1fc46ebf89af11801a466b85b6e0becee907d813de6bb4fa9a expected=509dd1ac27362d1fc46ebf89af11801a466b85b6e0becee907d813de6bb4fa9a
EXTRACT_NOTE members_exact count=5 order=stage1
EXTRACT_NOTE extract_dir_allocated path=<QA>/b4green/kit/extracted
EXTRACT_NOTE extracted_files_readonly mode=0444
EXTRACT_block name=RP0-LIB.sh sha256=cdb08f04ae0e78e18be2ac75fab6c56e0410345fa7846b8a399849a9d46007d5
EXTRACT_block name=RP0-BOOTSTRAP.sh sha256=9014464ca51250132ac02b0406eb9d3cc9fba2ce5c214f25b790a22749386d2b
EXTRACT_block name=RP6-P0.sh sha256=60b632bc0f914309c5451e928e81cd7a2fd8c2faceaa61a0f3f65151bd8a8cf0
EXTRACT_block name=RP7-WPI-RO.sh sha256=05754d3bc0e44cce897bb7c47de2993cbb32077920296fbe321595c3fd304958
EXTRACT_block name=run_p0.sh sha256=7b4d63257cdf3576b16a8124b68844a2d6284294eb870f590c306dc2c8c6b200
EXTRACT PASS archive=<QA>/b4green/kit/runkit.tar archive_sha256=509dd1ac27362d1fc46ebf89af11801a466b85b6e0becee907d813de6bb4fa9a dir=<QA>/b4green/kit/extracted members=5 verified=5 executed=0
RC=0
=== B5_GREEN_PLANTED_PATH_TAR_IGNORED ===
EXTRACT_NOTE tool name=stat path=<QA>/bin/stat owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE tool name=sha256sum path=<QA>/bin/sha256sum owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE tool name=tar path=<QA>/bin/tar owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE tool name=mkdir path=<QA>/bin/mkdir owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE tool name=readlink path=<QA>/bin/readlink owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE tool name=find path=<QA>/bin/find owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE tool name=chmod path=<QA>/bin/chmod owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE member_constant count=6 source=MEMBERS
EXTRACT_NOTE parent_bound path=<QA>/b5green/kit owner_uid=0 mode=755
EXTRACT_NOTE enoent_calibration rc=1 template=stat: cannot stat '@PATH@': No such file or directory (os error 2)
EXTRACT_archive path=<QA>/b5green/kit/runkit.tar bytes=10240
EXTRACT_archive_sha256 actual=fb503db79b512ee82d89f77f01f37b34cdf728f57d8a45f5edd1ff1398e94f6d expected=fb503db79b512ee82d89f77f01f37b34cdf728f57d8a45f5edd1ff1398e94f6d
EXTRACT_NOTE members_exact count=6 order=stage1
EXTRACT_NOTE extract_dir_allocated path=<QA>/b5green/kit/extracted
EXTRACT_NOTE extracted_files_readonly mode=0444
EXTRACT_block name=RP0-LIB.sh sha256=cdb08f04ae0e78e18be2ac75fab6c56e0410345fa7846b8a399849a9d46007d5
EXTRACT_block name=RP0-BOOTSTRAP.sh sha256=9014464ca51250132ac02b0406eb9d3cc9fba2ce5c214f25b790a22749386d2b
EXTRACT_block name=RP6-P0.sh sha256=60b632bc0f914309c5451e928e81cd7a2fd8c2faceaa61a0f3f65151bd8a8cf0
EXTRACT_block name=RP7-WPI-RO.sh sha256=05754d3bc0e44cce897bb7c47de2993cbb32077920296fbe321595c3fd304958
EXTRACT_block name=run_p0.sh sha256=7b4d63257cdf3576b16a8124b68844a2d6284294eb870f590c306dc2c8c6b200
EXTRACT_block name=run_ro.sh sha256=e58c4c5b619f684169973224e37e7e6594e56644a81c31bf7d2b23ce7bfb6b1a
EXTRACT PASS archive=<QA>/b5green/kit/runkit.tar archive_sha256=fb503db79b512ee82d89f77f01f37b34cdf728f57d8a45f5edd1ff1398e94f6d dir=<QA>/b5green/kit/extracted members=6 verified=6 executed=0
RC=0
=== B6_GREEN_LISTING_HARD_FAILURE ===
EXTRACT_NOTE tool name=stat path=<QA>/bin/stat owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE tool name=sha256sum path=<QA>/bin/sha256sum owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE tool name=tar_fail path=<QA>/bin/tar_fail owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE tool name=mkdir path=<QA>/bin/mkdir owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE tool name=readlink path=<QA>/bin/readlink owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE tool name=find path=<QA>/bin/find owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE tool name=chmod path=<QA>/bin/chmod owner_numeric=0:0 mode=755 resolution=pinned_absolute
EXTRACT_NOTE member_constant count=6 source=MEMBERS
EXTRACT_NOTE parent_bound path=<QA>/b6green/kit owner_uid=0 mode=755
EXTRACT_NOTE enoent_calibration rc=1 template=stat: cannot stat '@PATH@': No such file or directory (os error 2)
EXTRACT_archive path=<QA>/b6green/kit/runkit.tar bytes=10240
EXTRACT_archive_sha256 actual=fb503db79b512ee82d89f77f01f37b34cdf728f57d8a45f5edd1ff1398e94f6d expected=fb503db79b512ee82d89f77f01f37b34cdf728f57d8a45f5edd1ff1398e94f6d
EXTRACT_STOP reason=tar_type_listing_failed rc=2 detail=tar: fixture listing failure

RC=3
=== P0_LINK_RED_NO_SYMLINK_REFUSAL ===
P0W_header base_run=QA runid=QA-p0 stage=p0
P0W_block path=<QA>/p0lr/extracted/RP0-LIB.sh sha256=c40ac28f736f4a3d7749d1b878287e6a50fe8d5d8c4c083302b47470c1440da0
P0W_block path=<QA>/p0lr/extracted/RP0-BOOTSTRAP.sh sha256=6cbb07150259415307765ebaefb92d2ca0cf9838bf12749bff93446dde30ddef
P0W_block path=<QA>/p0lr/extracted/RP6-P0.sh sha256=01f706a17dc6787df311f7f6b04aa8577427c63e56f688d3406531a46664aeae
P0W_evidence_open runid=QA-p0 stage=p0 dir=<QA>/p0lr/evidence/runkit/QA-p0 leaf=<QA>/p0lr/evidence/runkit/QA-p0/p0.log
P0W_FIXTURE stdin=eof
P0W done runid=QA-p0
TAIL_EXECUTED
RC=0
=== P0_LINK_GREEN ===
P0W_tool name=stat path=<QA>/bin/stat owner_numeric=0:0 mode=755 resolution=pinned_absolute
P0W_tool name=sha256sum path=<QA>/bin/sha256sum owner_numeric=0:0 mode=755 resolution=pinned_absolute
P0W_header base_run=QA runid=QA-p0 stage=p0
P0W_block path=<QA>/p0lg/extracted/RP0-LIB.sh sha256=c40ac28f736f4a3d7749d1b878287e6a50fe8d5d8c4c083302b47470c1440da0
P0W_block path=<QA>/p0lg/extracted/RP0-BOOTSTRAP.sh sha256=6cbb07150259415307765ebaefb92d2ca0cf9838bf12749bff93446dde30ddef
P0W_STOP reason=block_is_symlink path=<QA>/p0lg/extracted/RP6-P0.sh
RC=3
=== P0_STDIN_RED_NO_DEV_NULL ===
P0W_header base_run=QA runid=QA-p0 stage=p0
P0W_block path=<QA>/p0sr/extracted/RP0-LIB.sh sha256=c40ac28f736f4a3d7749d1b878287e6a50fe8d5d8c4c083302b47470c1440da0
P0W_block path=<QA>/p0sr/extracted/RP0-BOOTSTRAP.sh sha256=6cbb07150259415307765ebaefb92d2ca0cf9838bf12749bff93446dde30ddef
P0W_block path=<QA>/p0sr/extracted/RP6-P0.sh sha256=01f706a17dc6787df311f7f6b04aa8577427c63e56f688d3406531a46664aeae
P0W_evidence_open runid=QA-p0 stage=p0 dir=<QA>/p0sr/evidence/runkit/QA-p0 leaf=<QA>/p0sr/evidence/runkit/QA-p0/p0.log
P0W_FIXTURE stdin=stolen
RC=1
=== P0_STDIN_GREEN ===
P0W_tool name=stat path=<QA>/bin/stat owner_numeric=0:0 mode=755 resolution=pinned_absolute
P0W_tool name=sha256sum path=<QA>/bin/sha256sum owner_numeric=0:0 mode=755 resolution=pinned_absolute
P0W_header base_run=QA runid=QA-p0 stage=p0
P0W_block path=<QA>/p0sg/extracted/RP0-LIB.sh sha256=c40ac28f736f4a3d7749d1b878287e6a50fe8d5d8c4c083302b47470c1440da0
P0W_block path=<QA>/p0sg/extracted/RP0-BOOTSTRAP.sh sha256=6cbb07150259415307765ebaefb92d2ca0cf9838bf12749bff93446dde30ddef
P0W_block path=<QA>/p0sg/extracted/RP6-P0.sh sha256=01f706a17dc6787df311f7f6b04aa8577427c63e56f688d3406531a46664aeae
P0W_evidence_open runid=QA-p0 stage=p0 dir=<QA>/p0sg/evidence/runkit/QA-p0 leaf=<QA>/p0sg/evidence/runkit/QA-p0/p0.log
P0W_FIXTURE stdin=eof
P0W done runid=QA-p0
TAIL_EXECUTED
RC=0
=== P0_HIJACK_RED_PATH_RESOLVED_DIGEST_TOOL ===
P0W_header base_run=QA runid=QA-p0 stage=p0
P0W_block path=<QA>/p0hr/extracted/RP0-LIB.sh sha256=c40ac28f736f4a3d7749d1b878287e6a50fe8d5d8c4c083302b47470c1440da0
P0W_block path=<QA>/p0hr/extracted/RP0-BOOTSTRAP.sh sha256=6cbb07150259415307765ebaefb92d2ca0cf9838bf12749bff93446dde30ddef
P0W_block path=<QA>/p0hr/extracted/RP6-P0.sh sha256=01f706a17dc6787df311f7f6b04aa8577427c63e56f688d3406531a46664aeae
P0W_evidence_open runid=QA-p0 stage=p0 dir=<QA>/p0hr/evidence/runkit/QA-p0 leaf=<QA>/p0hr/evidence/runkit/QA-p0/p0.log
P0W_HIJACKED_BLOCK_EXECUTED
P0W done runid=QA-p0
TAIL_EXECUTED
RC=0
=== P0_HIJACK_GREEN_PINNED_DIGEST_TOOL ===
P0W_tool name=stat path=<QA>/bin/stat owner_numeric=0:0 mode=755 resolution=pinned_absolute
P0W_tool name=sha256sum path=<QA>/bin/sha256sum owner_numeric=0:0 mode=755 resolution=pinned_absolute
P0W_header base_run=QA runid=QA-p0 stage=p0
P0W_block path=<QA>/p0hg/extracted/RP0-LIB.sh sha256=c40ac28f736f4a3d7749d1b878287e6a50fe8d5d8c4c083302b47470c1440da0
P0W_block path=<QA>/p0hg/extracted/RP0-BOOTSTRAP.sh sha256=6cbb07150259415307765ebaefb92d2ca0cf9838bf12749bff93446dde30ddef
P0W_block path=<QA>/p0hg/extracted/RP6-P0.sh sha256=cdcd673443e627b7182fd0e2d6c7383a2882f16d86b7b4026bb3502241b45a61
P0W_STOP reason=block_sha256_mismatch path=<QA>/p0hg/extracted/RP6-P0.sh actual=cdcd673443e627b7182fd0e2d6c7383a2882f16d86b7b4026bb3502241b45a61 expected=01f706a17dc6787df311f7f6b04aa8577427c63e56f688d3406531a46664aeae
RC=3
=== RO_LINK_RED_NO_SYMLINK_REFUSAL ===
ROW_header base_run=QA runid=QA-ro stage=ro
ROW_block path=<QA>/rolr/extracted/RP0-LIB.sh sha256=c40ac28f736f4a3d7749d1b878287e6a50fe8d5d8c4c083302b47470c1440da0
ROW_block path=<QA>/rolr/extracted/RP0-BOOTSTRAP.sh sha256=6cbb07150259415307765ebaefb92d2ca0cf9838bf12749bff93446dde30ddef
ROW_block path=<QA>/rolr/extracted/RP7-WPI-RO.sh sha256=6fa4e6b8674cf754b71ad2a9f791d1337fd643fe7479343d5ef7bb274999fdd9
ROW_evidence_open runid=QA-ro stage=ro dir=<QA>/rolr/evidence/runkit/QA-ro leaf=<QA>/rolr/evidence/runkit/QA-ro/ro.log
ROW_FIXTURE stdin=eof
ROW done runid=QA-ro
TAIL_EXECUTED
RC=0
=== RO_LINK_GREEN ===
ROW_tool name=stat path=<QA>/bin/stat owner_numeric=0:0 mode=755 resolution=pinned_absolute
ROW_tool name=sha256sum path=<QA>/bin/sha256sum owner_numeric=0:0 mode=755 resolution=pinned_absolute
ROW_header base_run=QA runid=QA-ro stage=ro
ROW_block path=<QA>/rolg/extracted/RP0-LIB.sh sha256=c40ac28f736f4a3d7749d1b878287e6a50fe8d5d8c4c083302b47470c1440da0
ROW_block path=<QA>/rolg/extracted/RP0-BOOTSTRAP.sh sha256=6cbb07150259415307765ebaefb92d2ca0cf9838bf12749bff93446dde30ddef
ROW_STOP reason=block_is_symlink path=<QA>/rolg/extracted/RP7-WPI-RO.sh
RC=3
=== RO_STDIN_RED_NO_DEV_NULL ===
ROW_header base_run=QA runid=QA-ro stage=ro
ROW_block path=<QA>/rosr/extracted/RP0-LIB.sh sha256=c40ac28f736f4a3d7749d1b878287e6a50fe8d5d8c4c083302b47470c1440da0
ROW_block path=<QA>/rosr/extracted/RP0-BOOTSTRAP.sh sha256=6cbb07150259415307765ebaefb92d2ca0cf9838bf12749bff93446dde30ddef
ROW_block path=<QA>/rosr/extracted/RP7-WPI-RO.sh sha256=6fa4e6b8674cf754b71ad2a9f791d1337fd643fe7479343d5ef7bb274999fdd9
ROW_evidence_open runid=QA-ro stage=ro dir=<QA>/rosr/evidence/runkit/QA-ro leaf=<QA>/rosr/evidence/runkit/QA-ro/ro.log
ROW_FIXTURE stdin=stolen
RC=1
=== RO_STDIN_GREEN ===
ROW_tool name=stat path=<QA>/bin/stat owner_numeric=0:0 mode=755 resolution=pinned_absolute
ROW_tool name=sha256sum path=<QA>/bin/sha256sum owner_numeric=0:0 mode=755 resolution=pinned_absolute
ROW_header base_run=QA runid=QA-ro stage=ro
ROW_block path=<QA>/rosg/extracted/RP0-LIB.sh sha256=c40ac28f736f4a3d7749d1b878287e6a50fe8d5d8c4c083302b47470c1440da0
ROW_block path=<QA>/rosg/extracted/RP0-BOOTSTRAP.sh sha256=6cbb07150259415307765ebaefb92d2ca0cf9838bf12749bff93446dde30ddef
ROW_block path=<QA>/rosg/extracted/RP7-WPI-RO.sh sha256=6fa4e6b8674cf754b71ad2a9f791d1337fd643fe7479343d5ef7bb274999fdd9
ROW_evidence_open runid=QA-ro stage=ro dir=<QA>/rosg/evidence/runkit/QA-ro leaf=<QA>/rosg/evidence/runkit/QA-ro/ro.log
ROW_FIXTURE stdin=eof
ROW done runid=QA-ro
TAIL_EXECUTED
RC=0
=== RO_HIJACK_RED_PATH_RESOLVED_DIGEST_TOOL ===
ROW_header base_run=QA runid=QA-ro stage=ro
ROW_block path=<QA>/rohr/extracted/RP0-LIB.sh sha256=c40ac28f736f4a3d7749d1b878287e6a50fe8d5d8c4c083302b47470c1440da0
ROW_block path=<QA>/rohr/extracted/RP0-BOOTSTRAP.sh sha256=6cbb07150259415307765ebaefb92d2ca0cf9838bf12749bff93446dde30ddef
ROW_block path=<QA>/rohr/extracted/RP7-WPI-RO.sh sha256=6fa4e6b8674cf754b71ad2a9f791d1337fd643fe7479343d5ef7bb274999fdd9
ROW_evidence_open runid=QA-ro stage=ro dir=<QA>/rohr/evidence/runkit/QA-ro leaf=<QA>/rohr/evidence/runkit/QA-ro/ro.log
ROW_HIJACKED_BLOCK_EXECUTED
ROW done runid=QA-ro
TAIL_EXECUTED
RC=0
=== RO_HIJACK_GREEN_PINNED_DIGEST_TOOL ===
ROW_tool name=stat path=<QA>/bin/stat owner_numeric=0:0 mode=755 resolution=pinned_absolute
ROW_tool name=sha256sum path=<QA>/bin/sha256sum owner_numeric=0:0 mode=755 resolution=pinned_absolute
ROW_header base_run=QA runid=QA-ro stage=ro
ROW_block path=<QA>/rohg/extracted/RP0-LIB.sh sha256=c40ac28f736f4a3d7749d1b878287e6a50fe8d5d8c4c083302b47470c1440da0
ROW_block path=<QA>/rohg/extracted/RP0-BOOTSTRAP.sh sha256=6cbb07150259415307765ebaefb92d2ca0cf9838bf12749bff93446dde30ddef
ROW_block path=<QA>/rohg/extracted/RP7-WPI-RO.sh sha256=33f8c345a2163ff289c8f9e05c9817be79b6cbb937f10708c339db8c14e4416d
ROW_STOP reason=block_sha256_mismatch path=<QA>/rohg/extracted/RP7-WPI-RO.sh actual=33f8c345a2163ff289c8f9e05c9817be79b6cbb937f10708c339db8c14e4416d expected=6fa4e6b8674cf754b71ad2a9f791d1337fd643fe7479343d5ef7bb274999fdd9
RC=3
=== P0_TOOL_IS_SYMLINK ===
P0W_tool name=stat path=<QA>/bin/stat owner_numeric=0:0 mode=755 resolution=pinned_absolute
P0W_STOP reason=tool_is_symlink path=<QA>/bin/sha256sum_link
RC=3
=== P0_TOOL_OTHER_WRITABLE ===
P0W_tool name=stat path=<QA>/bin/stat owner_numeric=0:0 mode=755 resolution=pinned_absolute
P0W_STOP reason=tool_other_writable mode=757 path=<QA>/bin/sha256sum_ww
RC=3
=== CLOSE_TRANSCRIPTS ===
ACCEPTED_SOURCE 87157f0ea454df7c1f826a8c76a38f3045dd38efdd8fa347644f79251d3f3f0e bytes=7470
--- the only substitution ---
31c31
< EXPECT_OWNER='gatea:gatea'
---
> EXPECT_OWNER='root:root'
--- end diff ---
--- CLOSE QA-P0 rc=0 ---
CLOSE_NOTE evidence_dir_ok path=<QA>/ev/runkit/QA-P0 owner=root:root mode=700
CLOSE_NOTE evidence_files count=3
CLOSE_NOTE digest_set_stable passes=2
CLOSE_BINDING runid=QA-P0 dir=<QA>/ev/runkit/QA-P0 files=3
CLOSE_DIGEST_BEGIN runid=QA-P0
CLOSE_DIGEST 07de973f6ae7b2a66fd2a15a7e0ebe8dc4bb12017e0244b455b1265c5ae4ad88  aaa.txt
CLOSE_DIGEST 015c5fc8b0edea0bc16e1fe3419a9708c50bc707867bb7732a2fb51e287c9c8d  stage.log
CLOSE_DIGEST c64f78ba4ccc75d4f32040c685f54ef2dae741cc011d3d890226ae469f50d823  sub/nested.txt
CLOSE_DIGEST_END runid=QA-P0
CLOSE_SIZE_BEGIN runid=QA-P0
CLOSE_SIZE aaa.txt 30
CLOSE_SIZE stage.log 32
CLOSE_SIZE sub/nested.txt 26
CLOSE_SIZE_END runid=QA-P0
CLOSE_DIGEST_SET_SHA256 runid=QA-P0 b769956db7ad98dddf850b0291c6296c1040aaa3a1a4a835dd2d8351537093b6
CLOSE PASS runid=QA-P0 dir=<QA>/ev/runkit/QA-P0 files=3 wrote_into_evidence_tree=0
--- CLOSE QA-RO rc=0 ---
CLOSE_NOTE evidence_dir_ok path=<QA>/ev/runkit/QA-RO owner=root:root mode=700
CLOSE_NOTE evidence_files count=3
CLOSE_NOTE digest_set_stable passes=2
CLOSE_BINDING runid=QA-RO dir=<QA>/ev/runkit/QA-RO files=3
CLOSE_DIGEST_BEGIN runid=QA-RO
CLOSE_DIGEST ddd722d5d1f8555bd270d293a4c93a48fbb9f020fc15cbc872e5c1afe877df0a  aaa.txt
CLOSE_DIGEST 805e75943934221f79e0dffa3a261f10698052eb9c71a4feee1edb1ff54f7e8c  stage.log
CLOSE_DIGEST d083afb3e182712cdd4d99dd57f9d7504f133568d2216a0dc09d4c2738889f09  sub/nested.txt
CLOSE_DIGEST_END runid=QA-RO
CLOSE_SIZE_BEGIN runid=QA-RO
CLOSE_SIZE aaa.txt 30
CLOSE_SIZE stage.log 32
CLOSE_SIZE sub/nested.txt 26
CLOSE_SIZE_END runid=QA-RO
CLOSE_DIGEST_SET_SHA256 runid=QA-RO 2e384eab0b2b417cf27678a352e59053aa2d86f5ecd1b0d81929f1980fba86a3
CLOSE PASS runid=QA-RO dir=<QA>/ev/runkit/QA-RO files=3 wrote_into_evidence_tree=0
=== WPI_R2_SHELL_QA_COMPLETE (fixture root removed; only <QAOUT>/close remains) ===
```

### 3.1 What the set-1 transcript establishes

- **A1** — the repaired allocator completes on a clean sandbox: five parent
  components bound numerically, the ENOENT template calibrated *from the pinned
  binary in that run* (`… No such file or directory (os error 2)` — the uutils
  wording, which no hardcoded GNU sentence would have matched), four directories
  allocated and each asserted immediately after creation. `DIRS_CREATED=4`.
- **A2** — Codex F4, executed both ways. The pinned `stat` returns a mixed
  EACCES+ENOENT diagnostic for the base path. Round-1 bytes classify it `absent`,
  create **4** directories and exit 0 (`SETUP PASS`). Repaired bytes STOP with
  `path_probe_multiline` and create **0**.
- **A3** — the harder variant: one line carrying both classes. Repaired bytes
  STOP with `path_probe_unclassified` because the diagnostic is not equal, as a
  whole string, to the calibrated template. `DIRS_CREATED=0`.
- **A4** — Codex F5 first half. Round-1 bytes create **4** directories through a
  parent symlink and only then notice (`path_not_canonical`). Repaired bytes
  refuse at `parent_not_canonical` with **0** created — refusal before mutation.
- **A5** — Codex F5 second half, the `[AUDIT2 A2-F3]` shape. The pinned `stat`
  renders the created base as `root:root` while its numeric owner is `1000:1000`.
  Round-1 bytes compare the *name* and return `SETUP PASS` rc 0. Repaired bytes
  return `owner_numeric=1000:1000 expected=0:0 … owner_name=root:root` rc 1 —
  numeric identity, name diagnostic only.
- **A6** — the delivered draft state: `EXPECT_UID`/`EXPECT_GID` are
  `<PIN-AT-FREEZE>`, so the script STOPs `identity_pin_unfilled` and creates
  nothing. Fail-closed before freeze.
- **A7** — a world-writable ancestor is refused (`parent_other_writable
  mode=777`), 0 created.
- **B1** — the repaired extractor completes: seven tools admitted by pinned
  absolute path with numeric ownership, `member_constant count=6 source=MEMBERS`,
  container bound, `EXTRACT PASS … members=6 verified=6 executed=0`.
- **B2** — Codex F6, and it reproduces his transcript exactly. A listing helper
  writes a warning to stderr and returns the correct list at rc 0. Round-1 bytes
  print `FAKE_TAR_WARNING` twice and still reach `EXTRACT PASS … rc 0`. Repaired
  bytes STOP at `tar_type_listing_diagnostics` **before** any member name is
  parsed; the `detail=` field carries the complete merged stream.
- **B3** — the completion class. A listing that ends without a record separator
  is accepted by round-1 bytes (command substitution had already destroyed the
  evidence) and STOPs the repaired bytes at
  `tar_name_listing_unterminated_final_record`.
- **B4** — Codex F7 / Claude F5, the count literals. With `MEMBERS` reduced to
  five and a genuine five-member archive: round-1 bytes fail
  `tar_member_count=5 expected=6` — the literal has drifted from the constant —
  while the repaired bytes derive the count and reach
  `EXTRACT PASS … members=5 verified=5`. No count literal survives anywhere.
- **B5** — a `tar` planted earlier on `PATH` is simply not consulted; the run
  passes normally.
- **B6** — a listing that exits non-zero STOPs at `tar_type_listing_failed rc=2`.
- **P0/RO_LINK_*, P0/RO_STDIN_*** — the two round-1 wrapper guarantees still
  hold, re-executed rather than restated: deleting the `-L` refusal admits the
  symlink (rc 0, `TAIL_EXECUTED`), and dropping `</dev/null` on the target source
  lets the child eat the wrapper stream (`stdin=stolen`, rc 1, tail lost).
- **P0/RO_HIJACK_*** — Codex F3 against the wrappers, reproducing his
  `P0_HIJACKED_BLOCK_EXECUTED`. A `sha256sum` planted on `PATH` reports the
  frozen digest for a block whose bytes were replaced. Round-1 bytes execute the
  replaced block at rc 0. Repaired bytes resolve `sha256sum` by pinned absolute
  path, compute the real digest, and STOP `block_sha256_mismatch` rc 3.
- **P0_TOOL_IS_SYMLINK / P0_TOOL_OTHER_WRITABLE** — the tool predicate itself has
  a red state: a symlinked pin and a `0757` pin are both refused at rc 3.
- **CLOSE_TRANSCRIPTS** — the accepted `remote_close_tree.sh` (7470 B,
  `87157f0e…`) run over two real evidence trees, with its one-line substitution
  printed as a diff. These transcripts are the remote half that fixture set 2
  binds against; nothing about them is synthesised.

## 4. Fixture set 2 — operator side (verbatim)

`wpi_r2_runner_qa.ps1`:

```powershell
# WP-I transport round 2 - transport_runner.ps1 RED/GREEN fixture set (standalone).
#
#   GREEN = the current repaired file.
#   RED   = the SAME file with exactly the repair reverted (a deliberate D026
#           mutation whose anchor text is asserted present before it is applied,
#           so a silently-missing anchor throws instead of producing a false RED).
#
# Prerequisite: run wpi_r2_shell_qa.sh first; it leaves the real
# remote_close_tree.sh transcripts and trees under C:\Users\Public\wpi_r2_qa\close.
# Run:  powershell.exe -NoProfile -ExecutionPolicy Bypass -File wpi_r2_runner_qa.ps1
# It contacts no host (only 127.0.0.1 probe fixtures), touches no repository
# file, allocates no RUNID, and removes its scratch root at the end.
$ErrorActionPreference = 'Stop'
$SRC   = 'C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPI_BLOCKS_DRAFT\transport_runner.ps1'
$ACCPT = 'C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\02_PREREG'
$CLOSE = 'C:\Users\Public\wpi_r2_qa\close'
$WORK  = 'C:\Users\Public\wpi_r2_qa\cases'
$CMD   = 'C:\Windows\System32\cmd.exe'
$CMDSHA= (Get-FileHash -LiteralPath $CMD -Algorithm SHA256).Hash.ToLowerInvariant()
$HDR   = "op_id`tkind`trun_when`texpect_rc`tcwd`tstdin_file`tstdin_sha256`targv`tpurpose"
if (Test-Path -LiteralPath $WORK) { Remove-Item -LiteralPath $WORK -Recurse -Force }
[void](New-Item -ItemType Directory -Path $WORK)
Write-Host ('QA_RUNNER_UNDER_TEST ' + (Get-FileHash -LiteralPath $SRC -Algorithm SHA256).Hash.ToLowerInvariant())
Write-Host ('QA_PROGRAM_PIN_SUBSTITUTION ssh,scp -> ' + $CMD + ' ' + $CMDSHA)

function Write-Lf([string]$p,[string[]]$l) { [System.IO.File]::WriteAllText($p, (($l -join "`n") + "`n"), (New-Object System.Text.UTF8Encoding($false))) }
function Sha([string]$p) { return (Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant() }
function Cut-Block([string[]]$lines,[string]$startsWith) {
    $o = New-Object System.Collections.ArrayList; $k = $false
    foreach ($l in $lines) { if ($k) { if ($l -eq ')') { $k = $false }; continue }
        if ($l.StartsWith($startsWith)) { $k = $true; continue }; [void]$o.Add($l) }
    return @($o)
}
function New-QaRunner {
    param([string]$qa,[string]$planSha,[hashtable]$mut,[hashtable]$const,[string]$pinnedBlock)
    $lines = @(Get-Content -LiteralPath $SRC)
    $lines = Cut-Block $lines '$PINNED_FILES = @('
    $lines = Cut-Block $lines '$PROGRAM_PINS = @('
    $c = @{ BASE_RUN="'QA'"; CONFIRM_TOKEN="'QA-EXECUTE'"; PREREG_DIR="'$qa'";
            RUNKIT_DIR="'$qa\01_RUNKIT'"; ACCEPTED_DIR="'$qa\accepted'";
            RECORD_ROOT="'$qa\record'"; PLAN_SHA256="'$planSha'" }
    if ($const) { foreach ($k in $const.Keys) { $c[$k] = $const[$k] } }
    $out = New-Object System.Collections.ArrayList
    foreach ($l in $lines) {
        $done = $false
        foreach ($k in @('BASE_RUN','CONFIRM_TOKEN','PREREG_DIR','RUNKIT_DIR','ACCEPTED_DIR','RECORD_ROOT','PLAN_SHA256')) {
            if ($l -match ('^\$' + $k + '\s*=')) { [void]$out.Add('$' + $k + ' = ' + $c[$k]); $done = $true; break } }
        if ($done) { continue }
        if ($l -match "^\`$STDIN_ROOTS = ") {
            [void]$out.Add("`$STDIN_ROOTS = @{ 'PREREG' = `$PREREG_DIR; 'ACCEPTED' = `$ACCEPTED_DIR }")
            if ($pinnedBlock) { [void]$out.Add($pinnedBlock) } else { [void]$out.Add("`$PINNED_FILES = @()") }
            [void]$out.Add("`$PROGRAM_PINS = @( @{ Name = 'ssh'; Path = '$CMD'; Sha = '$CMDSHA' }, @{ Name = 'scp'; Path = '$CMD'; Sha = '$CMDSHA' } )")
            continue
        }
        [void]$out.Add($l)
    }
    $text = ($out -join "`n") + "`n"
    if ($mut) { foreach ($k in $mut.Keys) {
        if (-not $text.Contains($k)) { throw ('MUTATION_ANCHOR_NOT_FOUND: ' + $k.Substring(0,[Math]::Min(60,$k.Length))) }
        $text = $text.Replace($k, $mut[$k]) } }
    # The QA copy carries the operator profile path, which is non-ASCII on this
    # host, so the COPY (never the deliverable) is written with a BOM.
    $p = Join-Path $qa 'transport_runner.ps1'
    [System.IO.File]::WriteAllText($p, $text, (New-Object System.Text.UTF8Encoding($true)))
    return $p
}
function Invoke-Runner([string]$label,[string]$runner,[string]$filter,[switch]$DryRun) {
    Write-Host ("=== " + $label + " ===")
    $prev = $ErrorActionPreference; $ErrorActionPreference = 'Continue'
    try {
        $out = if ($DryRun) { & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $runner 2>&1 }
               else { & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $runner -Execute -Confirm QA-EXECUTE 2>&1 }
        $rc = $LASTEXITCODE
        $out | ForEach-Object { "$_" } | Where-Object { -not $filter -or $_ -match $filter } | ForEach-Object { Write-Host $_ }
    } catch { Write-Host ('DRIVER_CAUGHT ' + $_.Exception.GetType().Name); $rc = $LASTEXITCODE }
    $ErrorActionPreference = $prev
    Write-Host ("RUNNER_RC=" + $rc)
}
$KEY = '^TR_(HEADER|MARKER_GATE|STOP|PLAN_READ|PLAN_ROWS|STDIN|PINNED|PROGRAM|ENV_POLICY|OP_BEGIN|OP_SKIPPED|OP_END|OP_DEVIANT|OP_NOT_EVALUABLE|FIRST_FAIL|ADDITIONAL_MISMATCH|RESULT|RUN_CLASS|RUN |DRY_RUN|RECORD_ROOT)|^  \| TR_BIND|^Test-Path|^\+|^ *\+ *Category'

# ---------------------------------------------------------- mutation anchors
$M_LATCH_OLD = @'
            $capDigest = $matches[1]; $capRel = $matches[2]
            if ($state -ne 'digests') { return [pscustomobject]@{Ok=$false;Reason='remote_digest_out_of_order'} }
            if ($capRel -notmatch '^[A-Za-z0-9._/-]+$' -or $capRel.StartsWith('/') -or $capRel -match '(^|/)\.\.?(?:/|$)') { return [pscustomobject]@{Ok=$false;Reason='remote_digest_path_unsafe'} }
            if ($digests.ContainsKey($capRel)) { return [pscustomobject]@{Ok=$false;Reason='remote_digest_duplicate'} }
            $digests.Add($capRel,$capDigest); continue
'@
$M_LATCH_NEW = @'
            if ($state -ne 'digests') { return [pscustomobject]@{Ok=$false;Reason='remote_digest_out_of_order'} }
            $rel=$matches[2]
            if ($rel -notmatch '^[A-Za-z0-9._/-]+$' -or $rel.StartsWith('/') -or $rel -match '(^|/)\.\.?(?:/|$)') { return [pscustomobject]@{Ok=$false;Reason='remote_digest_path_unsafe'} }
            if ($digests.ContainsKey($rel)) { return [pscustomobject]@{Ok=$false;Reason='remote_digest_duplicate'} }
            $digests.Add($rel,$matches[1]); continue
'@
$M_GRAM_OLD = @'
if ($anyDeviant) {
    Emit ('TR_RUN FAIL base_run=' + $BASE_RUN + ' first_fail=' + $firstMismatch + ' first_not_evaluable=' + $firstNotEvaluable + ' record=' + $RECORD_ROOT)
    $exitCode = 1
} elseif ($anyNotEvaluable) {
'@
$M_GRAM_NEW = @'
if ($anyDeviant -or $anyNotEvaluable) {
    Emit ('TR_RUN FAIL base_run=' + $BASE_RUN + ' first_fail=' + $firstMismatch + ' record=' + $RECORD_ROOT)
    $exitCode = 1
} elseif ($false) {
'@
$M_SEQ_OLD  = "    if (`$op.RunWhen -eq 'sequence_ok' -and -not `$sequenceOk) {"
$M_SEQ_NEW  = "    if (`$false) {"
$M_PROG_OLD = "    `$script:ProgramByName[`$prog.Name] = `$prog.Path"
$M_PROG_NEW = "    `$script:ProgramByName[`$prog.Name] = (Get-Command `$prog.Name -ErrorAction SilentlyContinue).Source"
$M_TRAP_OLD = @'
trap {
    $detail = 'unknown'
    try { $detail = $_.Exception.GetType().FullName } catch { }
    try { Emit ('TR_STOP reason=runner_unhandled_error detail=' + $detail) }
    catch { Write-Host ('TR_STOP reason=runner_unhandled_error detail=' + $detail) }
    try { Flush-Log } catch { }
    exit 3
}
'@
$M_TRAP_NEW  = '# (top-level trap removed for this RED arm)'
$M_MARK_OLD  = "Assert-MarkerFree 'RECORD_ROOT' `$RECORD_ROOT"
$M_MARK_NEW  = '# (RECORD_ROOT marker gate removed for this RED arm)'

# ============================== A. section 7 binding over a real CLOSE record
function New-BindCase([string]$name,[hashtable]$mut,[scriptblock]$tweak) {
    $qa = Join-Path $WORK $name
    [void](New-Item -ItemType Directory -Path $qa)
    Copy-Item -LiteralPath (Join-Path $CLOSE 'tree\QA-P0') -Destination (Join-Path $qa 'tree\QA-P0') -Recurse
    Copy-Item -LiteralPath (Join-Path $CLOSE 'QA-P0.stdout') -Destination (Join-Path $qa 'close_QA-P0.txt')
    Write-Lf (Join-Path $qa 'qa_stdin.txt') @('qa stdin payload')
    if ($tweak) { & $tweak $qa }
    $rec = Join-Path $qa 'record'
    Write-Lf (Join-Path $qa 'TRANSPORT_PLAN.tsv') @(
        $HDR,
        ("07`tssh_stdin`talways`t0`t$qa`tPREREG:qa_stdin.txt`t" + (Sha (Join-Path $qa 'qa_stdin.txt')) + "`tssh /c type close_QA-P0.txt`temit the closed-tree transcript"),
        ("09`tscp_down`talways`t0`t$rec\evidence`t-`t-`tscp /c xcopy ..\..\tree\QA-P0 QA-P0\ /E /I /Q /Y`tretrieve the closed tree"),
        ("11`tlocal_bind`talways`t0`t$rec`t-`t-`tlocal_bind 07 09 evidence\QA-P0`tbind the remote and local digest sets"))
    return (New-QaRunner $qa (Sha (Join-Path $qa 'TRANSPORT_PLAN.tsv')) $mut $null $null)
}
Invoke-Runner 'A1_GREEN_BYTE_EQUAL_PAIR_BINDS'        (New-BindCase 'a1' $null $null) $KEY
Invoke-Runner 'A2_RED_MATCHES_CLOBBER_AS_DELIVERED'   (New-BindCase 'a2' @{ $M_LATCH_OLD = $M_LATCH_NEW } $null) $KEY
Invoke-Runner 'A3_GREEN_LOCAL_BYTE_CHANGED_MUST_FAIL' (New-BindCase 'a3' $null { param($qa) Add-Content -LiteralPath (Join-Path $qa 'tree\QA-P0\aaa.txt') -Value 'tamper' }) $KEY
Invoke-Runner 'A4_GREEN_EXTRA_LOCAL_FILE_MUST_FAIL'   (New-BindCase 'a4' $null { param($qa) Write-Lf (Join-Path $qa 'tree\QA-P0\extra.txt') @('extra') }) $KEY
Invoke-Runner 'A5_GREEN_MISSING_LOCAL_FILE_MUST_FAIL' (New-BindCase 'a5' $null { param($qa) Remove-Item -LiteralPath (Join-Path $qa 'tree\QA-P0\sub\nested.txt') }) $KEY
Invoke-Runner 'A6_GREEN_TAMPERED_SET_SHA_MUST_STOP'   (New-BindCase 'a6' $null {
    param($qa); $p = Join-Path $qa 'close_QA-P0.txt'
    [System.IO.File]::WriteAllText($p, ([System.IO.File]::ReadAllText($p) -replace 'CLOSE_DIGEST_SET_SHA256 runid=QA-P0 [0-9a-f]{64}', ('CLOSE_DIGEST_SET_SHA256 runid=QA-P0 ' + ('a'*64))), (New-Object System.Text.UTF8Encoding($false))) }) $KEY

# ---- close-record grammar arms (each must STOP, never FAIL, never PASS) -----
$grammar = @(
    @{ n='B1_runid_mismatch';    f={ param($t) $t -replace 'CLOSE_BINDING runid=QA-P0','CLOSE_BINDING runid=QA-XX' } },
    @{ n='B2_duplicate_digest';  f={ param($t) $t -replace '(CLOSE_DIGEST [0-9a-f]{64}  aaa\.txt\n)','$1$1' } },
    @{ n='B3_unsafe_path';       f={ param($t) $t -replace '  aaa\.txt','  ../aaa.txt' } },
    @{ n='B4_out_of_order';      f={ param($t) $t -replace 'CLOSE_DIGEST_BEGIN runid=QA-P0\n','' } },
    @{ n='B5_count_mismatch';    f={ param($t) $t -replace 'files=3','files=4' } },
    @{ n='B6_truncated_record';  f={ param($t) $t -replace 'CLOSE PASS runid=QA-P0[^\n]*\n','' } },
    @{ n='B7_unknown_record';    f={ param($t) $t + "CLOSE_SOMETHING_ELSE runid=QA-P0`n" } }
)
foreach ($g in $grammar) {
    $fn = $g.f
    Invoke-Runner ('B_' + $g.n) (New-BindCase $g.n $null {
        param($qa); $p = Join-Path $qa 'close_QA-P0.txt'
        [System.IO.File]::WriteAllText($p, (& $fn ([System.IO.File]::ReadAllText($p))), (New-Object System.Text.UTF8Encoding($false))) }) '  \| TR_BIND|^TR_RUN |^TR_OP_END id=11'
}

# ============================================ C. outcome grammar and ordering
function New-PlanCase([string]$name,[string[]]$rows,[hashtable]$mut,[hashtable]$const,[string]$pinned,[scriptblock]$prep) {
    $qa = Join-Path $WORK $name
    if (-not (Test-Path -LiteralPath $qa)) { [void](New-Item -ItemType Directory -Path $qa) }
    if ($prep) { & $prep $qa }
    Write-Lf (Join-Path $qa 'TRANSPORT_PLAN.tsv') (@($HDR) + ($rows | ForEach-Object { $_.Replace('@QA@',$qa) }))
    return (New-QaRunner $qa (Sha (Join-Path $qa 'TRANSPORT_PLAN.tsv')) $mut $const $pinned)
}
$stopRow = @("01`ttcp_probe`tsequence_ok`t0`t@QA@`t-`t-`ttcp_probe 127.0.0.1 99999 20000`ta probe with an out-of-range port")
Invoke-Runner 'C1_GREEN_CHILD_STOP_IS_RUN_STOP'          (New-PlanCase 'c1' $stopRow $null $null $null $null) $KEY
Invoke-Runner 'C2_RED_STOP_ROLLED_INTO_FAIL_AS_DELIVERED' (New-PlanCase 'c2' $stopRow @{ $M_GRAM_OLD = $M_GRAM_NEW } $null $null $null) $KEY
$listener = New-Object System.Net.Sockets.TcpListener([System.Net.IPAddress]::Loopback, 0); $listener.Start()
$open = $listener.LocalEndpoint.Port
Invoke-Runner 'C3_GREEN_DEVIANT_PLUS_LATER_STOP_IS_FAIL' (New-PlanCase 'c3' @(
    "01`ttcp_probe`tsequence_ok`t0`t@QA@`t-`t-`ttcp_probe 127.0.0.1 $open 20000`ta connected listener is observed deviant state",
    "02`ttcp_probe`talways`t0`t@QA@`t-`t-`ttcp_probe 127.0.0.1 99999 20000`ta not-evaluable cleanup probe") $null $null $null $null) $KEY
$listener.Stop()
$seqRows = @(
    "01`ttcp_probe`tsequence_ok`t1`t@QA@`t-`t-`ttcp_probe 127.0.0.1 9 20000`texpect_rc 1 while a closed port classifies rc 0",
    "02`ttcp_probe`tsequence_ok`t0`t@QA@`t-`t-`ttcp_probe 127.0.0.1 9 20000`tthis later sequence op must be skipped",
    "03`ttcp_probe`talways`t0`t@QA@`t-`t-`ttcp_probe 127.0.0.1 9 20000`tthis always op must still run",
    "04`ttcp_probe`talways`t0`t@QA@`t-`t-`ttcp_probe 127.0.0.1 9 20000`tthis always op must still run")
Invoke-Runner 'C4_RED_SKIP_PREDICATE_MUTATED' (New-PlanCase 'c4r' $seqRows @{ $M_SEQ_OLD = $M_SEQ_NEW } $null $null $null) '^TR_OP_BEGIN|^TR_OP_SKIPPED|^TR_RESULT|^TR_RUN '
Invoke-Runner 'C5_GREEN_FIRST_FAIL_ORDERING'  (New-PlanCase 'c4g' $seqRows $null $null $null $null) '^TR_OP_BEGIN|^TR_OP_SKIPPED|^TR_RESULT|^TR_RUN '

# ===================================== D. program identity and child environment
$fake = Join-Path $WORK 'fakebin'; [void](New-Item -ItemType Directory -Path $fake)
Write-Lf (Join-Path $fake 'ssh.cmd') @('@echo off','echo FAKE_SSH_EXECUTED','exit /b 0')
function New-ProgCase([string]$name,[string]$argv,[hashtable]$mut) {
    $qa = Join-Path $WORK $name; [void](New-Item -ItemType Directory -Path $qa)
    Write-Lf (Join-Path $qa 'qa_stdin.txt') @('qa stdin payload')
    Write-Lf (Join-Path $qa 'TRANSPORT_PLAN.tsv') @($HDR,
        ("01`tssh_stdin`tsequence_ok`t0`t$qa`tPREREG:qa_stdin.txt`t" + (Sha (Join-Path $qa 'qa_stdin.txt')) + "`t$argv`tprove which program the runner starts"))
    return (New-QaRunner $qa (Sha (Join-Path $qa 'TRANSPORT_PLAN.tsv')) $mut $null $null)
}
$saved = $env:PATH; $env:PATH = $fake + ';' + $env:PATH; $env:PYTHONPATH = 'C:\attacker\pythonpath'
Invoke-Runner 'D1_RED_PATH_RESOLVED_PROGRAM'      (New-ProgCase 'd1' 'ssh /c echo PINNED_PROGRAM_RAN' @{ $M_PROG_OLD = $M_PROG_NEW }) '^TR_PROGRAM|^TR_RUN '
Write-Host ('D1_op01_stdout: ' + ((Get-Content -Raw -LiteralPath (Join-Path $WORK 'd1\record\ops\01.stdout')) -replace "`r?`n",' '))
Invoke-Runner 'D2_GREEN_PINNED_ABSOLUTE_PROGRAM'  (New-ProgCase 'd2' 'ssh /c echo PINNED_PROGRAM_RAN' $null) '^TR_PROGRAM|^TR_RUN '
Write-Host ('D2_op01_stdout: ' + ((Get-Content -Raw -LiteralPath (Join-Path $WORK 'd2\record\ops\01.stdout')) -replace "`r?`n",' '))
Invoke-Runner 'D3_GREEN_CHILD_ENVIRONMENT'        (New-ProgCase 'd3' 'ssh /c set' $null) '^TR_ENV_POLICY|^TR_RUN '
Write-Host '--- the child environment, from ops/01.stdout (PYTHONPATH was set in the parent) ---'
Get-Content -LiteralPath (Join-Path $WORK 'd3\record\ops\01.stdout')
$env:PATH = $saved; Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue

# ================================================ E. marker gate and top-level trap
$anyRow = @("01`ttcp_probe`tsequence_ok`t0`t@QA@`t-`t-`ttcp_probe 127.0.0.1 9 20000`tany op")
$unf = "'C:\WPI_ARTIFACTS\WPI_TRANSPORT_<ALLOCATE-AT-DISPATCH>'"
Invoke-Runner 'E1_GREEN_UNFILLED_ALLOCATION_MARKER' (New-PlanCase 'e1' $anyRow $null @{ RECORD_ROOT = $unf } $null $null) $KEY
Invoke-Runner 'E2_RED_NO_MARKER_GATE_NO_TRAP'       (New-PlanCase 'e2' $anyRow @{ $M_MARK_OLD = $M_MARK_NEW; $M_TRAP_OLD = $M_TRAP_NEW } @{ RECORD_ROOT = $unf } $null $null) $KEY

# ======================================= F. kit location, stdin roots, plan grammar
$prepKit = { param($qa)
    [void](New-Item -ItemType Directory -Path (Join-Path $qa '01_RUNKIT') -Force)
    Write-Lf (Join-Path $qa '01_RUNKIT\runkit.tar') @('THE FROZEN KIT ARCHIVE')
    Write-Lf (Join-Path $qa 'runkit.tar') @('THE DECOY ARCHIVE BESIDE THE RUNNER') }
$probe = Join-Path $WORK '_probe'; [void](New-Item -ItemType Directory -Path $probe); & $prepKit $probe
$kitSha = Sha (Join-Path $probe '01_RUNKIT\runkit.tar'); $decoySha = Sha (Join-Path $probe 'runkit.tar')
Write-Host ("F_kit_archive_sha256=$kitSha"); Write-Host ("F_decoy_archive_sha256=$decoySha")
$kitRows = @("02`tscp_up`tsequence_ok`t0`t@QA@\01_RUNKIT`t-`t-`tscp runkit.tar host:/kit/runkit.tar`tupload the frozen kit archive")
Invoke-Runner 'F1_GREEN_KIT_ARCHIVE_RESOLVES_UNDER_01_RUNKIT' (New-PlanCase 'f1' $kitRows $null $null ("`$PINNED_FILES = @(@{ Path = (Join-Path `$RUNKIT_DIR 'runkit.tar'); Sha = '$kitSha' })") $prepKit) $KEY -DryRun
Invoke-Runner 'F2_GREEN_DECOY_BESIDE_THE_RUNNER_IS_NEVER_SELECTED' (New-PlanCase 'f2' $kitRows $null $null ("`$PINNED_FILES = @(@{ Path = (Join-Path `$RUNKIT_DIR 'runkit.tar'); Sha = '$decoySha' })") $prepKit) $KEY -DryRun
$closeSha = Sha (Join-Path $ACCPT 'remote_close_tree.sh')
Write-Host ("F_accepted_remote_close_tree_sha256=$closeSha")
$acceptedRows = @(
    "07`tssh_stdin`talways`t0`t@QA@`tACCEPTED:remote_close_tree.sh`t$closeSha`tssh /c echo op07`tclose the P0 evidence tree",
    "08`tssh_stdin`talways`t0`t@QA@`tACCEPTED:remote_close_tree.sh`t$closeSha`tssh /c echo op08`tclose the RO evidence tree")
Invoke-Runner 'F3_GREEN_ACCEPTED_ROOT_RESOLUTION'  (New-PlanCase 'f3' $acceptedRows $null @{ ACCEPTED_DIR = ("'" + $ACCPT + "'") } $null $null) $KEY -DryRun
Invoke-Runner 'F4_GREEN_ACCEPTED_FILE_ABSENT_STOPS' (New-PlanCase 'f4' $acceptedRows $null $null $null $null) $KEY -DryRun
Invoke-Runner 'F5_GREEN_WRONG_ROOT_TOKEN_STOPS'     (New-PlanCase 'f5' @("07`tssh_stdin`talways`t0`t@QA@`tPREREG:remote_close_tree.sh`t$closeSha`tssh /c echo op07`troot token points at the draft directory") $null $null $null $null) $KEY -DryRun
$zeros = '0000000000000000000000000000000000000000000000000000000000000000'
Invoke-Runner 'F6_GREEN_SSH_STDIN_WITHOUT_FILE'  (New-PlanCase 'f6' @("01`tssh_stdin`tsequence_ok`t0`t@QA@`t-`t-`tssh /c echo x`tssh_stdin with no stdin file") $null $null $null $null) '^TR_STOP' -DryRun
Invoke-Runner 'F7_GREEN_KIND_PROGRAM_MISMATCH'   (New-PlanCase 'f7' @("01`tssh_stdin`tsequence_ok`t0`t@QA@`tPREREG:x.txt`t$zeros`tscp /c echo x`tkind ssh_stdin but argv scp") $null $null $null $null) '^TR_STOP' -DryRun
Invoke-Runner 'F8_GREEN_CWD_NOT_PREREGISTERED'   (New-PlanCase 'f8' @("01`ttcp_probe`tsequence_ok`t0`tC:\Windows`t-`t-`ttcp_probe 127.0.0.1 9 20000`tcwd outside the preregistered set") $null $null $null $null) '^TR_STOP' -DryRun
Invoke-Runner 'F9_GREEN_STDIN_ON_NON_SSH_KIND'   (New-PlanCase 'f9' @("01`tscp_down`talways`t0`t@QA@`tPREREG:x.txt`t$zeros`tscp /c echo x`tstdin file on a non-ssh kind") $null $null $null $null) '^TR_STOP' -DryRun

# ===================================================== G. plan reader completion
function Run-PlanBytes([string]$label,[byte[]]$extra,[switch]$Empty,[switch]$Dir) {
    $r = New-PlanCase $label $anyRow $null $null $null $null
    $plan = Join-Path (Split-Path -Parent $r) 'TRANSPORT_PLAN.tsv'
    if ($Empty) { [System.IO.File]::WriteAllBytes($plan, @()) }
    elseif ($Dir) { Remove-Item -LiteralPath $plan; [void](New-Item -ItemType Directory -Path $plan) }
    elseif ($extra) { [System.IO.File]::WriteAllBytes($plan, ([System.IO.File]::ReadAllBytes($plan) + $extra)) }
    Invoke-Runner $label $r '^TR_PLAN_READ|^TR_STOP' -DryRun
}
Run-PlanBytes 'G1_GREEN_CLEAN_EOF' $null
Run-PlanBytes 'G2_GREEN_UNTERMINATED_FINAL_RECORD' ([byte[]](65))
Run-PlanBytes 'G3_GREEN_HARD_READ_ERROR' $null -Dir
Run-PlanBytes 'G4_GREEN_EMPTY_INPUT' $null -Empty
Run-PlanBytes 'G5_GREEN_CARRIAGE_RETURN' ([byte[]](13,10))
Run-PlanBytes 'G6_GREEN_CONTROL_BYTE' ([byte[]](7,10))
Run-PlanBytes 'G7_GREEN_NON_ASCII_BYTE' ([byte[]](200,10))

# ==================================== H. section 8 row 24 probe arms, all five
$listener = New-Object System.Net.Sockets.TcpListener([System.Net.IPAddress]::Loopback, 0); $listener.Start()
$open = $listener.LocalEndpoint.Port
$h = New-PlanCase 'h1' @(
    "01`ttcp_probe`talways`t0`t@QA@`t-`t-`ttcp_probe 127.0.0.1 9 20000`tclosed loopback port",
    "02`ttcp_probe`talways`t1`t@QA@`t-`t-`ttcp_probe 127.0.0.1 $open 20000`tlistening loopback port",
    "03`ttcp_probe`talways`t3`t@QA@`t-`t-`ttcp_probe 127.0.0.1 99999 20000`tport out of range",
    "04`ttcp_probe`talways`t3`t@QA@`t-`t-`ttcp_probe 127.0.0.1 9 60001`ttimeout out of range",
    "05`ttcp_probe`talways`t3`t@QA@`t-`t-`ttcp_probe 127.0.0.1 9`targv too short") $null $null $null $null
Invoke-Runner 'H_ROW24_ALL_FIVE_ARMS' $h '^TR_RESULT|^TR_RUN '
$listener.Stop()
foreach ($id in @('01','02','03','04','05')) {
    Write-Host ("op $id -> " + ((Get-Content -Raw -LiteralPath (Join-Path $WORK "h1\record\ops\$id.stdout")).Trim()) +
                "  [elapsed_ms=" + ((Get-Content -LiteralPath (Join-Path $WORK "h1\record\ops\$id.elapsed_ms"))).Trim() + "]")
}

# ================================ I. the real draft file, exactly as it ships
Write-Host '=== I_DRAFT_STATE_DRY_RUN_OF_THE_DELIVERED_FILE ==='
$prev = $ErrorActionPreference; $ErrorActionPreference = 'Continue'
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $SRC 2>&1 | ForEach-Object { "$_" }
Write-Host ("RUNNER_RC=" + $LASTEXITCODE)
$ErrorActionPreference = $prev

Remove-Item -LiteralPath 'C:\Users\Public\wpi_r2_qa' -Recurse -Force
Write-Host '=== WPI_R2_RUNNER_QA_COMPLETE (scratch root removed) ==='
```

Real output (S1 applied; nothing else altered):

```text
QA_RUNNER_UNDER_TEST 2f076ed9a928656fddf22969ea4bf70de895f2c84c73f13b4c64b8040e72aa9a
QA_PROGRAM_PIN_SUBSTITUTION ssh,scp -> C:\Windows\System32\cmd.exe 65ec268add3973b6dca64222985da47caeaee44a340b0ec1466782914fd743d9
=== A1_GREEN_BYTE_EQUAL_PAIR_BINDS ===
TR_HEADER base_run=QA
TR_MARKER_GATE constants=marker_free
TR_RECORD_ROOT path=<QA>\cases\a1\record
TR_PLAN_READ completion=clean_eof records=4
TR_PLAN_ROWS count=3
TR_STDIN op=07 root=PREREG path=<QA>\cases\a1\qa_stdin.txt sha256=2c74e735c85285711fe447b6af84406e73367763bcef9a71c7d24bccca3f1efd
TR_PROGRAM name=ssh path=C:\Windows\System32\cmd.exe sha256=65ec268add3973b6dca64222985da47caeaee44a340b0ec1466782914fd743d9 resolution=pinned_absolute chain=trusted
TR_PROGRAM name=scp path=C:\Windows\System32\cmd.exe sha256=65ec268add3973b6dca64222985da47caeaee44a340b0ec1466782914fd743d9 resolution=pinned_absolute chain=trusted
TR_ENV_POLICY cleared=all carried=USERPROFILE,HOMEDRIVE,HOMEPATH inherited_path=never
TR_OP_BEGIN id=07 kind=ssh_stdin cwd=<QA>\cases\a1
TR_OP_END id=07 rc=0 expect_rc=0 elapsed_ms=53 stdout_sha256=43a9217dbcf74e02a25586e8fd50244929fced1522d50d837a5f09c12e846a56 stderr_sha256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
TR_OP_BEGIN id=09 kind=scp_down cwd=<QA>\cases\a1\record\evidence
TR_OP_END id=09 rc=0 expect_rc=0 elapsed_ms=51 stdout_sha256=bf7ca40b1b35d8424c86936146683e3aa1e49115e3d7332b48fc5d4f1ed85ac1 stderr_sha256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
TR_OP_BEGIN id=11 kind=local_bind cwd=<QA>\cases\a1\record
  | TR_BIND close_op=07 fetch_op=09 local_dir=<QA>\cases\a1\record\evidence\QA-P0
  | TR_BIND_COUNTS remote=3 local=3
  | TR_BIND_SET remote_set_sha256=b769956db7ad98dddf850b0291c6296c1040aaa3a1a4a835dd2d8351537093b6 reconstructed=b769956db7ad98dddf850b0291c6296c1040aaa3a1a4a835dd2d8351537093b6
  | TR_BIND_PASS files=3
TR_OP_END id=11 rc=0 expect_rc=0 elapsed_ms=80 stdout_sha256=dc1bb11d0ddd8791a004ec4c7fd6a30dc7d4df1d39b60b9f8d4e7ad453766001 stderr_sha256=01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b
TR_RESULT id=07 rc=0 expect_rc=0 elapsed_ms=53
TR_RESULT id=09 rc=0 expect_rc=0 elapsed_ms=51
TR_RESULT id=11 rc=0 expect_rc=0 elapsed_ms=80
TR_RUN_CLASS deviant=0 not_evaluable=0 precedence=deviant_outranks_not_evaluable
TR_RUN PASS base_run=QA record=<QA>\cases\a1\record
RUNNER_RC=0
=== A2_RED_MATCHES_CLOBBER_AS_DELIVERED ===
TR_HEADER base_run=QA
TR_MARKER_GATE constants=marker_free
TR_RECORD_ROOT path=<QA>\cases\a2\record
TR_PLAN_READ completion=clean_eof records=4
TR_PLAN_ROWS count=3
TR_STDIN op=07 root=PREREG path=<QA>\cases\a2\qa_stdin.txt sha256=2c74e735c85285711fe447b6af84406e73367763bcef9a71c7d24bccca3f1efd
TR_PROGRAM name=ssh path=C:\Windows\System32\cmd.exe sha256=65ec268add3973b6dca64222985da47caeaee44a340b0ec1466782914fd743d9 resolution=pinned_absolute chain=trusted
TR_PROGRAM name=scp path=C:\Windows\System32\cmd.exe sha256=65ec268add3973b6dca64222985da47caeaee44a340b0ec1466782914fd743d9 resolution=pinned_absolute chain=trusted
TR_ENV_POLICY cleared=all carried=USERPROFILE,HOMEDRIVE,HOMEPATH inherited_path=never
TR_OP_BEGIN id=07 kind=ssh_stdin cwd=<QA>\cases\a2
TR_OP_END id=07 rc=0 expect_rc=0 elapsed_ms=85 stdout_sha256=43a9217dbcf74e02a25586e8fd50244929fced1522d50d837a5f09c12e846a56 stderr_sha256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
TR_OP_BEGIN id=09 kind=scp_down cwd=<QA>\cases\a2\record\evidence
TR_OP_END id=09 rc=0 expect_rc=0 elapsed_ms=43 stdout_sha256=bf7ca40b1b35d8424c86936146683e3aa1e49115e3d7332b48fc5d4f1ed85ac1 stderr_sha256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
TR_OP_BEGIN id=11 kind=local_bind cwd=<QA>\cases\a2\record
  | TR_BIND close_op=07 fetch_op=09 local_dir=<QA>\cases\a2\record\evidence\QA-P0
  | TR_BIND_COUNTS remote=3 local=3
  | TR_BIND_DIFF digest_differs=aaa.txt
  | TR_BIND_DIFF digest_differs=stage.log
  | TR_BIND_DIFF digest_differs=sub/nested.txt
TR_OP_END id=11 rc=1 expect_rc=0 elapsed_ms=49 stdout_sha256=afcf52cc38dc960db3973280078e187ad3c0adf6a763b7cdcf551849d434f028 stderr_sha256=01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b
TR_FIRST_FAIL id=11 rc=1 expected=0 later_sequence_ops=skip always_ops=run
TR_OP_DEVIANT id=11 rc=1 expected=0
TR_RESULT id=07 rc=0 expect_rc=0 elapsed_ms=85
TR_RESULT id=09 rc=0 expect_rc=0 elapsed_ms=43
TR_RESULT id=11 rc=1 expect_rc=0 elapsed_ms=49
TR_RUN_CLASS deviant=1 not_evaluable=0 precedence=deviant_outranks_not_evaluable
TR_RUN FAIL base_run=QA first_fail=11 first_not_evaluable= record=<QA>\cases\a2\record
RUNNER_RC=1
=== A3_GREEN_LOCAL_BYTE_CHANGED_MUST_FAIL ===
TR_HEADER base_run=QA
TR_MARKER_GATE constants=marker_free
TR_RECORD_ROOT path=<QA>\cases\a3\record
TR_PLAN_READ completion=clean_eof records=4
TR_PLAN_ROWS count=3
TR_STDIN op=07 root=PREREG path=<QA>\cases\a3\qa_stdin.txt sha256=2c74e735c85285711fe447b6af84406e73367763bcef9a71c7d24bccca3f1efd
TR_PROGRAM name=ssh path=C:\Windows\System32\cmd.exe sha256=65ec268add3973b6dca64222985da47caeaee44a340b0ec1466782914fd743d9 resolution=pinned_absolute chain=trusted
TR_PROGRAM name=scp path=C:\Windows\System32\cmd.exe sha256=65ec268add3973b6dca64222985da47caeaee44a340b0ec1466782914fd743d9 resolution=pinned_absolute chain=trusted
TR_ENV_POLICY cleared=all carried=USERPROFILE,HOMEDRIVE,HOMEPATH inherited_path=never
TR_OP_BEGIN id=07 kind=ssh_stdin cwd=<QA>\cases\a3
TR_OP_END id=07 rc=0 expect_rc=0 elapsed_ms=43 stdout_sha256=43a9217dbcf74e02a25586e8fd50244929fced1522d50d837a5f09c12e846a56 stderr_sha256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
TR_OP_BEGIN id=09 kind=scp_down cwd=<QA>\cases\a3\record\evidence
TR_OP_END id=09 rc=0 expect_rc=0 elapsed_ms=44 stdout_sha256=bf7ca40b1b35d8424c86936146683e3aa1e49115e3d7332b48fc5d4f1ed85ac1 stderr_sha256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
TR_OP_BEGIN id=11 kind=local_bind cwd=<QA>\cases\a3\record
  | TR_BIND close_op=07 fetch_op=09 local_dir=<QA>\cases\a3\record\evidence\QA-P0
  | TR_BIND_COUNTS remote=3 local=3
  | TR_BIND_DIFF digest_differs=aaa.txt
TR_OP_END id=11 rc=1 expect_rc=0 elapsed_ms=42 stdout_sha256=a4a7c213ff09435e242c4739fa0cfcbc65e50d368ed59b8bd39c8011f7acba51 stderr_sha256=01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b
TR_FIRST_FAIL id=11 rc=1 expected=0 later_sequence_ops=skip always_ops=run
TR_OP_DEVIANT id=11 rc=1 expected=0
TR_RESULT id=07 rc=0 expect_rc=0 elapsed_ms=43
TR_RESULT id=09 rc=0 expect_rc=0 elapsed_ms=44
TR_RESULT id=11 rc=1 expect_rc=0 elapsed_ms=42
TR_RUN_CLASS deviant=1 not_evaluable=0 precedence=deviant_outranks_not_evaluable
TR_RUN FAIL base_run=QA first_fail=11 first_not_evaluable= record=<QA>\cases\a3\record
RUNNER_RC=1
=== A4_GREEN_EXTRA_LOCAL_FILE_MUST_FAIL ===
TR_HEADER base_run=QA
TR_MARKER_GATE constants=marker_free
TR_RECORD_ROOT path=<QA>\cases\a4\record
TR_PLAN_READ completion=clean_eof records=4
TR_PLAN_ROWS count=3
TR_STDIN op=07 root=PREREG path=<QA>\cases\a4\qa_stdin.txt sha256=2c74e735c85285711fe447b6af84406e73367763bcef9a71c7d24bccca3f1efd
TR_PROGRAM name=ssh path=C:\Windows\System32\cmd.exe sha256=65ec268add3973b6dca64222985da47caeaee44a340b0ec1466782914fd743d9 resolution=pinned_absolute chain=trusted
TR_PROGRAM name=scp path=C:\Windows\System32\cmd.exe sha256=65ec268add3973b6dca64222985da47caeaee44a340b0ec1466782914fd743d9 resolution=pinned_absolute chain=trusted
TR_ENV_POLICY cleared=all carried=USERPROFILE,HOMEDRIVE,HOMEPATH inherited_path=never
TR_OP_BEGIN id=07 kind=ssh_stdin cwd=<QA>\cases\a4
TR_OP_END id=07 rc=0 expect_rc=0 elapsed_ms=44 stdout_sha256=43a9217dbcf74e02a25586e8fd50244929fced1522d50d837a5f09c12e846a56 stderr_sha256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
TR_OP_BEGIN id=09 kind=scp_down cwd=<QA>\cases\a4\record\evidence
TR_OP_END id=09 rc=0 expect_rc=0 elapsed_ms=43 stdout_sha256=7066a2f0ca23b9894ab5ca0c77ce84d3428dfa78117c128e393192626eaadbfc stderr_sha256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
TR_OP_BEGIN id=11 kind=local_bind cwd=<QA>\cases\a4\record
  | TR_BIND close_op=07 fetch_op=09 local_dir=<QA>\cases\a4\record\evidence\QA-P0
  | TR_BIND_COUNTS remote=3 local=4
  | TR_BIND_DIFF missing_remotely=extra.txt
TR_OP_END id=11 rc=1 expect_rc=0 elapsed_ms=45 stdout_sha256=1e4bb13d9ea5b7bd887cfa38186d7b22781db6a065eddea30ffb731788f31d67 stderr_sha256=01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b
TR_FIRST_FAIL id=11 rc=1 expected=0 later_sequence_ops=skip always_ops=run
TR_OP_DEVIANT id=11 rc=1 expected=0
TR_RESULT id=07 rc=0 expect_rc=0 elapsed_ms=44
TR_RESULT id=09 rc=0 expect_rc=0 elapsed_ms=43
TR_RESULT id=11 rc=1 expect_rc=0 elapsed_ms=45
TR_RUN_CLASS deviant=1 not_evaluable=0 precedence=deviant_outranks_not_evaluable
TR_RUN FAIL base_run=QA first_fail=11 first_not_evaluable= record=<QA>\cases\a4\record
RUNNER_RC=1
=== A5_GREEN_MISSING_LOCAL_FILE_MUST_FAIL ===
TR_HEADER base_run=QA
TR_MARKER_GATE constants=marker_free
TR_RECORD_ROOT path=<QA>\cases\a5\record
TR_PLAN_READ completion=clean_eof records=4
TR_PLAN_ROWS count=3
TR_STDIN op=07 root=PREREG path=<QA>\cases\a5\qa_stdin.txt sha256=2c74e735c85285711fe447b6af84406e73367763bcef9a71c7d24bccca3f1efd
TR_PROGRAM name=ssh path=C:\Windows\System32\cmd.exe sha256=65ec268add3973b6dca64222985da47caeaee44a340b0ec1466782914fd743d9 resolution=pinned_absolute chain=trusted
TR_PROGRAM name=scp path=C:\Windows\System32\cmd.exe sha256=65ec268add3973b6dca64222985da47caeaee44a340b0ec1466782914fd743d9 resolution=pinned_absolute chain=trusted
TR_ENV_POLICY cleared=all carried=USERPROFILE,HOMEDRIVE,HOMEPATH inherited_path=never
TR_OP_BEGIN id=07 kind=ssh_stdin cwd=<QA>\cases\a5
TR_OP_END id=07 rc=0 expect_rc=0 elapsed_ms=46 stdout_sha256=43a9217dbcf74e02a25586e8fd50244929fced1522d50d837a5f09c12e846a56 stderr_sha256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
TR_OP_BEGIN id=09 kind=scp_down cwd=<QA>\cases\a5\record\evidence
TR_OP_END id=09 rc=0 expect_rc=0 elapsed_ms=48 stdout_sha256=c2de2bf086e5fc91695ede62600ddc5f1bc2041317134243bcbcad66a198ef88 stderr_sha256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
TR_OP_BEGIN id=11 kind=local_bind cwd=<QA>\cases\a5\record
  | TR_BIND close_op=07 fetch_op=09 local_dir=<QA>\cases\a5\record\evidence\QA-P0
  | TR_BIND_COUNTS remote=3 local=2
  | TR_BIND_DIFF missing_locally=sub/nested.txt
TR_OP_END id=11 rc=1 expect_rc=0 elapsed_ms=48 stdout_sha256=905671f49dc6183f87a61bf6c6021163fcf84343bb816b1a0932e515dfb045af stderr_sha256=01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b
TR_FIRST_FAIL id=11 rc=1 expected=0 later_sequence_ops=skip always_ops=run
TR_OP_DEVIANT id=11 rc=1 expected=0
TR_RESULT id=07 rc=0 expect_rc=0 elapsed_ms=46
TR_RESULT id=09 rc=0 expect_rc=0 elapsed_ms=48
TR_RESULT id=11 rc=1 expect_rc=0 elapsed_ms=48
TR_RUN_CLASS deviant=1 not_evaluable=0 precedence=deviant_outranks_not_evaluable
TR_RUN FAIL base_run=QA first_fail=11 first_not_evaluable= record=<QA>\cases\a5\record
RUNNER_RC=1
=== A6_GREEN_TAMPERED_SET_SHA_MUST_STOP ===
TR_HEADER base_run=QA
TR_MARKER_GATE constants=marker_free
TR_RECORD_ROOT path=<QA>\cases\a6\record
TR_PLAN_READ completion=clean_eof records=4
TR_PLAN_ROWS count=3
TR_STDIN op=07 root=PREREG path=<QA>\cases\a6\qa_stdin.txt sha256=2c74e735c85285711fe447b6af84406e73367763bcef9a71c7d24bccca3f1efd
TR_PROGRAM name=ssh path=C:\Windows\System32\cmd.exe sha256=65ec268add3973b6dca64222985da47caeaee44a340b0ec1466782914fd743d9 resolution=pinned_absolute chain=trusted
TR_PROGRAM name=scp path=C:\Windows\System32\cmd.exe sha256=65ec268add3973b6dca64222985da47caeaee44a340b0ec1466782914fd743d9 resolution=pinned_absolute chain=trusted
TR_ENV_POLICY cleared=all carried=USERPROFILE,HOMEDRIVE,HOMEPATH inherited_path=never
TR_OP_BEGIN id=07 kind=ssh_stdin cwd=<QA>\cases\a6
TR_OP_END id=07 rc=0 expect_rc=0 elapsed_ms=41 stdout_sha256=50e5392d0b6d142240ecdabb86aa81d55557fbe0b6ab6bfe141ff22472a50b5d stderr_sha256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
TR_OP_BEGIN id=09 kind=scp_down cwd=<QA>\cases\a6\record\evidence
TR_OP_END id=09 rc=0 expect_rc=0 elapsed_ms=44 stdout_sha256=bf7ca40b1b35d8424c86936146683e3aa1e49115e3d7332b48fc5d4f1ed85ac1 stderr_sha256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
TR_OP_BEGIN id=11 kind=local_bind cwd=<QA>\cases\a6\record
  | TR_BIND close_op=07 fetch_op=09 local_dir=<QA>\cases\a6\record\evidence\QA-P0
  | TR_BIND_COUNTS remote=3 local=3
  | TR_BIND_SET remote_set_sha256=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa reconstructed=b769956db7ad98dddf850b0291c6296c1040aaa3a1a4a835dd2d8351537093b6
  | TR_BIND_STOP reason=digest_set_rendering_differs
TR_OP_END id=11 rc=3 expect_rc=0 elapsed_ms=58 stdout_sha256=84f62fd8a582bf878bac9d73fb702ab076696acab7f8490005dbc00c5b572703 stderr_sha256=01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b
TR_FIRST_FAIL id=11 rc=3 expected=0 later_sequence_ops=skip always_ops=run
TR_OP_NOT_EVALUABLE id=11 rc=3 expected=0
TR_RESULT id=07 rc=0 expect_rc=0 elapsed_ms=41
TR_RESULT id=09 rc=0 expect_rc=0 elapsed_ms=44
TR_RESULT id=11 rc=3 expect_rc=0 elapsed_ms=58
TR_RUN_CLASS deviant=0 not_evaluable=1 precedence=deviant_outranks_not_evaluable
TR_RUN STOP base_run=QA first_fail=11 first_not_evaluable=11 record=<QA>\cases\a6\record
RUNNER_RC=3
=== B_B1_runid_mismatch ===
  | TR_BIND close_op=07 fetch_op=09 local_dir=<QA>\cases\B1_runid_mismatch\record\evidence\QA-P0
  | TR_BIND_STOP reason=remote_close_binding_mismatch
TR_OP_END id=11 rc=3 expect_rc=0 elapsed_ms=9 stdout_sha256=88fdaa4cf9d538a3eaf17f12db89b18f51693637e46f5922d2a77fe023ae1a46 stderr_sha256=01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b
TR_RUN STOP base_run=QA first_fail=11 first_not_evaluable=11 record=<QA>\cases\B1_runid_mismatch\record
RUNNER_RC=3
=== B_B2_duplicate_digest ===
  | TR_BIND close_op=07 fetch_op=09 local_dir=<QA>\cases\B2_duplicate_digest\record\evidence\QA-P0
  | TR_BIND_STOP reason=remote_digest_duplicate
TR_OP_END id=11 rc=3 expect_rc=0 elapsed_ms=10 stdout_sha256=46fa5f82957d6e7ee6b0d4383425777e69b96893e0d9491dca50b8e1a4d0ab23 stderr_sha256=01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b
TR_RUN STOP base_run=QA first_fail=11 first_not_evaluable=11 record=<QA>\cases\B2_duplicate_digest\record
RUNNER_RC=3
=== B_B3_unsafe_path ===
  | TR_BIND close_op=07 fetch_op=09 local_dir=<QA>\cases\B3_unsafe_path\record\evidence\QA-P0
  | TR_BIND_STOP reason=remote_digest_path_unsafe
TR_OP_END id=11 rc=3 expect_rc=0 elapsed_ms=10 stdout_sha256=7605872fe57d06a38412fd1f1d6de57cc81ed89658a093789eeb6d7f91a8829d stderr_sha256=01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b
TR_RUN STOP base_run=QA first_fail=11 first_not_evaluable=11 record=<QA>\cases\B3_unsafe_path\record
RUNNER_RC=3
=== B_B4_out_of_order ===
  | TR_BIND close_op=07 fetch_op=09 local_dir=<QA>\cases\B4_out_of_order\record\evidence\QA-P0
  | TR_BIND_STOP reason=remote_digest_out_of_order
TR_OP_END id=11 rc=3 expect_rc=0 elapsed_ms=9 stdout_sha256=af37d28089f00c0a79f6054eff2c471354fe5d35b6b4fabc9bafc394b7f4dae9 stderr_sha256=01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b
TR_RUN STOP base_run=QA first_fail=11 first_not_evaluable=11 record=<QA>\cases\B4_out_of_order\record
RUNNER_RC=3
=== B_B5_count_mismatch ===
  | TR_BIND close_op=07 fetch_op=09 local_dir=<QA>\cases\B5_count_mismatch\record\evidence\QA-P0
  | TR_BIND_STOP reason=remote_close_count_mismatch
TR_OP_END id=11 rc=3 expect_rc=0 elapsed_ms=24 stdout_sha256=7191691583a7b7c56da1e70f5b51d4de7f059d42f167c9e614f43cb9e71f9c63 stderr_sha256=01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b
TR_RUN STOP base_run=QA first_fail=11 first_not_evaluable=11 record=<QA>\cases\B5_count_mismatch\record
RUNNER_RC=3
=== B_B6_truncated_record ===
  | TR_BIND close_op=07 fetch_op=09 local_dir=<QA>\cases\B6_truncated_record\record\evidence\QA-P0
  | TR_BIND_STOP reason=remote_close_incomplete
TR_OP_END id=11 rc=3 expect_rc=0 elapsed_ms=19 stdout_sha256=b382fdb9b681e147e7394076ac163abe6a63352db7c189425d974e147a8c941a stderr_sha256=01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b
TR_RUN STOP base_run=QA first_fail=11 first_not_evaluable=11 record=<QA>\cases\B6_truncated_record\record
RUNNER_RC=3
=== B_B7_unknown_record ===
  | TR_BIND close_op=07 fetch_op=09 local_dir=<QA>\cases\B7_unknown_record\record\evidence\QA-P0
  | TR_BIND_STOP reason=remote_close_unknown_or_out_of_order_record
TR_OP_END id=11 rc=3 expect_rc=0 elapsed_ms=20 stdout_sha256=f9c6446eeeb667d148a5fa51ccfae28cb920d08375264818615424e654e3a832 stderr_sha256=01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b
TR_RUN STOP base_run=QA first_fail=11 first_not_evaluable=11 record=<QA>\cases\B7_unknown_record\record
RUNNER_RC=3
=== C1_GREEN_CHILD_STOP_IS_RUN_STOP ===
TR_HEADER base_run=QA
TR_MARKER_GATE constants=marker_free
TR_RECORD_ROOT path=<QA>\cases\c1\record
TR_PLAN_READ completion=clean_eof records=2
TR_PLAN_ROWS count=1
TR_ENV_POLICY cleared=all carried=USERPROFILE,HOMEDRIVE,HOMEPATH inherited_path=never
TR_OP_BEGIN id=01 kind=tcp_probe cwd=<QA>\cases\c1
TR_OP_END id=01 rc=3 expect_rc=0 elapsed_ms=4 stdout_sha256=e3e811e68bd1fcd93f86fcd1ffb89cbb53526faabc6f657173a570339acabd0e stderr_sha256=01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b
TR_FIRST_FAIL id=01 rc=3 expected=0 later_sequence_ops=skip always_ops=run
TR_OP_NOT_EVALUABLE id=01 rc=3 expected=0
TR_RESULT id=01 rc=3 expect_rc=0 elapsed_ms=4
TR_RUN_CLASS deviant=0 not_evaluable=1 precedence=deviant_outranks_not_evaluable
TR_RUN STOP base_run=QA first_fail=01 first_not_evaluable=01 record=<QA>\cases\c1\record
RUNNER_RC=3
=== C2_RED_STOP_ROLLED_INTO_FAIL_AS_DELIVERED ===
TR_HEADER base_run=QA
TR_MARKER_GATE constants=marker_free
TR_RECORD_ROOT path=<QA>\cases\c2\record
TR_PLAN_READ completion=clean_eof records=2
TR_PLAN_ROWS count=1
TR_ENV_POLICY cleared=all carried=USERPROFILE,HOMEDRIVE,HOMEPATH inherited_path=never
TR_OP_BEGIN id=01 kind=tcp_probe cwd=<QA>\cases\c2
TR_OP_END id=01 rc=3 expect_rc=0 elapsed_ms=4 stdout_sha256=e3e811e68bd1fcd93f86fcd1ffb89cbb53526faabc6f657173a570339acabd0e stderr_sha256=01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b
TR_FIRST_FAIL id=01 rc=3 expected=0 later_sequence_ops=skip always_ops=run
TR_OP_NOT_EVALUABLE id=01 rc=3 expected=0
TR_RESULT id=01 rc=3 expect_rc=0 elapsed_ms=4
TR_RUN_CLASS deviant=0 not_evaluable=1 precedence=deviant_outranks_not_evaluable
TR_RUN FAIL base_run=QA first_fail=01 record=<QA>\cases\c2\record
RUNNER_RC=1
=== C3_GREEN_DEVIANT_PLUS_LATER_STOP_IS_FAIL ===
TR_HEADER base_run=QA
TR_MARKER_GATE constants=marker_free
TR_RECORD_ROOT path=<QA>\cases\c3\record
TR_PLAN_READ completion=clean_eof records=3
TR_PLAN_ROWS count=2
TR_ENV_POLICY cleared=all carried=USERPROFILE,HOMEDRIVE,HOMEPATH inherited_path=never
TR_OP_BEGIN id=01 kind=tcp_probe cwd=<QA>\cases\c3
TR_OP_END id=01 rc=1 expect_rc=0 elapsed_ms=18 stdout_sha256=74f47a6f377b02ade84cc66c1d446e4c858fdfa5e0ce255b7d29ba1155465cd0 stderr_sha256=01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b
TR_FIRST_FAIL id=01 rc=1 expected=0 later_sequence_ops=skip always_ops=run
TR_OP_DEVIANT id=01 rc=1 expected=0
TR_OP_BEGIN id=02 kind=tcp_probe cwd=<QA>\cases\c3
TR_OP_END id=02 rc=3 expect_rc=0 elapsed_ms=1 stdout_sha256=e3e811e68bd1fcd93f86fcd1ffb89cbb53526faabc6f657173a570339acabd0e stderr_sha256=01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b
TR_ADDITIONAL_MISMATCH id=02 first_fail=01
TR_OP_NOT_EVALUABLE id=02 rc=3 expected=0
TR_RESULT id=01 rc=1 expect_rc=0 elapsed_ms=18
TR_RESULT id=02 rc=3 expect_rc=0 elapsed_ms=1
TR_RUN_CLASS deviant=1 not_evaluable=1 precedence=deviant_outranks_not_evaluable
TR_RUN FAIL base_run=QA first_fail=01 first_not_evaluable=02 record=<QA>\cases\c3\record
RUNNER_RC=1
=== C4_RED_SKIP_PREDICATE_MUTATED ===
TR_OP_BEGIN id=01 kind=tcp_probe cwd=<QA>\cases\c4r
TR_OP_BEGIN id=02 kind=tcp_probe cwd=<QA>\cases\c4r
TR_OP_BEGIN id=03 kind=tcp_probe cwd=<QA>\cases\c4r
TR_OP_BEGIN id=04 kind=tcp_probe cwd=<QA>\cases\c4r
TR_RESULT id=01 rc=0 expect_rc=1 elapsed_ms=2043
TR_RESULT id=02 rc=0 expect_rc=0 elapsed_ms=2038
TR_RESULT id=03 rc=0 expect_rc=0 elapsed_ms=2027
TR_RESULT id=04 rc=0 expect_rc=0 elapsed_ms=2021
TR_RUN FAIL base_run=QA first_fail=01 first_not_evaluable= record=<QA>\cases\c4r\record
RUNNER_RC=1
=== C5_GREEN_FIRST_FAIL_ORDERING ===
TR_OP_BEGIN id=01 kind=tcp_probe cwd=<QA>\cases\c4g
TR_OP_SKIPPED id=02 reason=prior_sequence_mismatch
TR_OP_BEGIN id=03 kind=tcp_probe cwd=<QA>\cases\c4g
TR_OP_BEGIN id=04 kind=tcp_probe cwd=<QA>\cases\c4g
TR_RESULT id=01 rc=0 expect_rc=1 elapsed_ms=2043
TR_RESULT id=02 rc=skipped expect_rc=0 elapsed_ms=0
TR_RESULT id=03 rc=0 expect_rc=0 elapsed_ms=2026
TR_RESULT id=04 rc=0 expect_rc=0 elapsed_ms=2027
TR_RUN FAIL base_run=QA first_fail=01 first_not_evaluable= record=<QA>\cases\c4g\record
RUNNER_RC=1
=== D1_RED_PATH_RESOLVED_PROGRAM ===
TR_PROGRAM name=ssh path=C:\Windows\System32\cmd.exe sha256=65ec268add3973b6dca64222985da47caeaee44a340b0ec1466782914fd743d9 resolution=pinned_absolute chain=trusted
TR_RUN PASS base_run=QA record=<QA>\cases\d1\record
RUNNER_RC=0
D1_op01_stdout: FAKE_SSH_EXECUTED 
=== D2_GREEN_PINNED_ABSOLUTE_PROGRAM ===
TR_PROGRAM name=ssh path=C:\Windows\System32\cmd.exe sha256=65ec268add3973b6dca64222985da47caeaee44a340b0ec1466782914fd743d9 resolution=pinned_absolute chain=trusted
TR_RUN PASS base_run=QA record=<QA>\cases\d2\record
RUNNER_RC=0
D2_op01_stdout: PINNED_PROGRAM_RAN 
=== D3_GREEN_CHILD_ENVIRONMENT ===
TR_ENV_POLICY cleared=all carried=USERPROFILE,HOMEDRIVE,HOMEPATH inherited_path=never
TR_RUN PASS base_run=QA record=<QA>\cases\d3\record
RUNNER_RC=0
--- the child environment, from ops/01.stdout (PYTHONPATH was set in the parent) ---
ComSpec=C:\Windows\System32\cmd.exe
HOMEDRIVE=C:
HOMEPATH=\Users\BarŸSemaay
PATH=C:\Windows\System32;C:\Windows
PATHEXT=.COM;.EXE;.BAT;.CMD
PROMPT=$P$G
SystemRoot=C:\Windows
TEMP=<QA>\cases\d3\record\tmp
TMP=<QA>\cases\d3\record\tmp
USERPROFILE=C:\Users\BarŸSemaay
windir=C:\Windows
=== E1_GREEN_UNFILLED_ALLOCATION_MARKER ===
TR_HEADER base_run=QA
TR_STOP reason=unfilled_marker field=RECORD_ROOT
RUNNER_RC=3
=== E2_RED_NO_MARKER_GATE_NO_TRAP ===
TR_HEADER base_run=QA
TR_MARKER_GATE constants=marker_free
Test-Path : Yolda geçersiz karakterler var.
+     if (Test-Path -LiteralPath $RECORD_ROOT) { Stop-Run ('record_root ...
+         ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgument: (C:\WPI_ARTIFACT...TE-AT-DISPATCH>:String) [Test-Path], ArgumentExcepti 
RUNNER_RC=1
F_kit_archive_sha256=ebad5c95b69c04e6412b28351e8e64899bb7121cac12786b0dd0e419cc1ae6bd
F_decoy_archive_sha256=b885c44ebe6893633faa84efe4425d8f852c1fd7496ebba93b06b6ec71845ef1
=== F1_GREEN_KIT_ARCHIVE_RESOLVES_UNDER_01_RUNKIT ===
TR_HEADER base_run=QA
TR_MARKER_GATE constants=marker_free
TR_PLAN_READ completion=clean_eof records=2
TR_PLAN_ROWS count=1
TR_PINNED path=<QA>\cases\f1\01_RUNKIT\runkit.tar sha256=ebad5c95b69c04e6412b28351e8e64899bb7121cac12786b0dd0e419cc1ae6bd
TR_PROGRAM name=scp path=C:\Windows\System32\cmd.exe sha256=65ec268add3973b6dca64222985da47caeaee44a340b0ec1466782914fd743d9 resolution=pinned_absolute chain=trusted
TR_ENV_POLICY cleared=all carried=USERPROFILE,HOMEDRIVE,HOMEPATH inherited_path=never
TR_DRY_RUN no_process_was_started no_connection_was_opened
TR_DRY_RUN to_execute=-Execute_-Confirm_QA-EXECUTE
RUNNER_RC=0
=== F2_GREEN_DECOY_BESIDE_THE_RUNNER_IS_NEVER_SELECTED ===
TR_HEADER base_run=QA
TR_MARKER_GATE constants=marker_free
TR_PLAN_READ completion=clean_eof records=2
TR_PLAN_ROWS count=1
TR_PINNED path=<QA>\cases\f2\01_RUNKIT\runkit.tar sha256=ebad5c95b69c04e6412b28351e8e64899bb7121cac12786b0dd0e419cc1ae6bd
TR_STOP reason=pinned_file_sha256_mismatch path=<QA>\cases\f2\01_RUNKIT\runkit.tar actual=ebad5c95b69c04e6412b28351e8e64899bb7121cac12786b0dd0e419cc1ae6bd expected=b885c44ebe6893633faa84efe4425d8f852c1fd7496ebba93b06b6ec71845ef1
RUNNER_RC=3
F_accepted_remote_close_tree_sha256=87157f0ea454df7c1f826a8c76a38f3045dd38efdd8fa347644f79251d3f3f0e
=== F3_GREEN_ACCEPTED_ROOT_RESOLUTION ===
TR_HEADER base_run=QA
TR_MARKER_GATE constants=marker_free
TR_PLAN_READ completion=clean_eof records=3
TR_PLAN_ROWS count=2
TR_STDIN op=07 root=ACCEPTED path=C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\02_PREREG\remote_close_tree.sh sha256=87157f0ea454df7c1f826a8c76a38f3045dd38efdd8fa347644f79251d3f3f0e
TR_STDIN op=08 root=ACCEPTED path=C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\02_PREREG\remote_close_tree.sh sha256=87157f0ea454df7c1f826a8c76a38f3045dd38efdd8fa347644f79251d3f3f0e
TR_PROGRAM name=ssh path=C:\Windows\System32\cmd.exe sha256=65ec268add3973b6dca64222985da47caeaee44a340b0ec1466782914fd743d9 resolution=pinned_absolute chain=trusted
TR_ENV_POLICY cleared=all carried=USERPROFILE,HOMEDRIVE,HOMEPATH inherited_path=never
TR_DRY_RUN no_process_was_started no_connection_was_opened
TR_DRY_RUN to_execute=-Execute_-Confirm_QA-EXECUTE
RUNNER_RC=0
=== F4_GREEN_ACCEPTED_FILE_ABSENT_STOPS ===
TR_HEADER base_run=QA
TR_MARKER_GATE constants=marker_free
TR_PLAN_READ completion=clean_eof records=3
TR_PLAN_ROWS count=2
TR_STOP reason=stdin_file_missing op=07 path=<QA>\cases\f4\accepted\remote_close_tree.sh
RUNNER_RC=3
=== F5_GREEN_WRONG_ROOT_TOKEN_STOPS ===
TR_HEADER base_run=QA
TR_MARKER_GATE constants=marker_free
TR_PLAN_READ completion=clean_eof records=2
TR_PLAN_ROWS count=1
TR_STOP reason=stdin_file_missing op=07 path=<QA>\cases\f5\remote_close_tree.sh
RUNNER_RC=3
=== F6_GREEN_SSH_STDIN_WITHOUT_FILE ===
TR_STOP reason=plan_row_ssh_stdin_without_file op=01
RUNNER_RC=3
=== F7_GREEN_KIND_PROGRAM_MISMATCH ===
TR_STOP reason=plan_row_kind_program_mismatch op=01 kind=ssh_stdin program=scp
RUNNER_RC=3
=== F8_GREEN_CWD_NOT_PREREGISTERED ===
TR_STOP reason=plan_row_cwd_not_preregistered op=01 cwd=C:\Windows
RUNNER_RC=3
=== F9_GREEN_STDIN_ON_NON_SSH_KIND ===
TR_STOP reason=plan_row_stdin_file_on_non_ssh_kind op=01 kind=scp_down
RUNNER_RC=3
=== G1_GREEN_CLEAN_EOF ===
TR_PLAN_READ completion=clean_eof records=2
RUNNER_RC=0
=== G2_GREEN_UNTERMINATED_FINAL_RECORD ===
TR_STOP reason=plan_unterminated_final_record path=<QA>\cases\G2_GREEN_UNTERMINATED_FINAL_RECORD\TRANSPORT_PLAN.tsv
RUNNER_RC=3
=== G3_GREEN_HARD_READ_ERROR ===
TR_STOP reason=plan_read_error detail=System.Management.Automation.MethodInvocationException path=<QA>\cases\G3_GREEN_HARD_READ_ERROR\TRANSPORT_PLAN.tsv
RUNNER_RC=3
=== G4_GREEN_EMPTY_INPUT ===
TR_STOP reason=plan_empty_input path=<QA>\cases\G4_GREEN_EMPTY_INPUT\TRANSPORT_PLAN.tsv
RUNNER_RC=3
=== G5_GREEN_CARRIAGE_RETURN ===
TR_STOP reason=plan_carriage_return_not_allowed path=<QA>\cases\G5_GREEN_CARRIAGE_RETURN\TRANSPORT_PLAN.tsv
RUNNER_RC=3
=== G6_GREEN_CONTROL_BYTE ===
TR_STOP reason=plan_control_byte_7 path=<QA>\cases\G6_GREEN_CONTROL_BYTE\TRANSPORT_PLAN.tsv
RUNNER_RC=3
=== G7_GREEN_NON_ASCII_BYTE ===
TR_STOP reason=plan_non_ascii_byte path=<QA>\cases\G7_GREEN_NON_ASCII_BYTE\TRANSPORT_PLAN.tsv
RUNNER_RC=3
=== H_ROW24_ALL_FIVE_ARMS ===
TR_RESULT id=01 rc=0 expect_rc=0 elapsed_ms=2062
TR_RESULT id=02 rc=1 expect_rc=1 elapsed_ms=3
TR_RESULT id=03 rc=3 expect_rc=3 elapsed_ms=1
TR_RESULT id=04 rc=3 expect_rc=3 elapsed_ms=1
TR_RESULT id=05 rc=3 expect_rc=3 elapsed_ms=1
TR_RUN PASS base_run=QA record=<QA>\cases\h1\record
RUNNER_RC=0
op 01 -> B6_external row=24 outcome=connection_refused host=127.0.0.1 port=9 payload_bytes=0  [elapsed_ms=2062]
op 02 -> B6_FAIL reason=host_reachable_8790 outcome=connected host=127.0.0.1 port=60020 payload_bytes=0  [elapsed_ms=3]
op 03 -> B6_STOP reason=external_probe_not_evaluable outcome=port_invalid rc=3 detail=port_range  [elapsed_ms=1]
op 04 -> B6_STOP reason=external_probe_not_evaluable outcome=timeout_invalid rc=3 detail=timeout_range  [elapsed_ms=1]
op 05 -> B6_STOP reason=external_probe_not_evaluable outcome=argv_malformed rc=3 detail=expected_host_port_timeout  [elapsed_ms=1]
=== I_DRAFT_STATE_DRY_RUN_OF_THE_DELIVERED_FILE ===
TR_HEADER base_run=<ALLOCATE-AT-DISPATCH>
TR_MODE execute=False confirm_supplied=False
TR_STOP reason=unfilled_marker field=BASE_RUN
RUNNER_RC=3
=== WPI_R2_RUNNER_QA_COMPLETE (scratch root removed) ===
```

### 4.1 What the set-2 transcript establishes

- **A1 — the §7 binding executes and returns 0 for the first time.** A real
  `remote_close_tree.sh` transcript is fed as `ops/07.stdout`, the identical tree
  is retrieved into the record as `ops/09`, and op 11 reports
  `TR_BIND_COUNTS remote=3 local=3`,
  `TR_BIND_SET remote_set_sha256=b769956d…c208 reconstructed=b769956d…c208`,
  `TR_BIND_PASS files=3`, `TR_RUN PASS`, exit 0. `CLOSE_DIGEST_SET_SHA256` is
  compared for the first time in this artefact's life.
- **A2 — the delivered defect, reverted one hunk at a time.** The same fixture,
  with only the capture latch undone, reports `digest_differs` for all three
  byte-identical files, `TR_RUN FAIL`, exit 1 — Claude F1 and Codex F2 reproduced
  against the repaired file's own bytes.
- **A3/A4/A5 — the differing pairs must and do FAIL, each for its own reason**
  (`digest_differs=aaa.txt`, `missing_remotely=extra.txt`,
  `missing_locally=sub/nested.txt`). This is the point Claude's audit made: while
  F1 stood, every one of these produced the same rc 1 as the unmutated case and
  therefore proved nothing. They now discriminate.
- **A6 — a tampered `CLOSE_DIGEST_SET_SHA256` STOPs**, and the STOP propagates:
  `TR_BIND_STOP reason=digest_set_rendering_differs` → op rc 3 →
  `TR_RUN STOP` → exit 3.
- **B1–B7 — the close-record grammar has a red state for every clause**: runid
  mismatch, duplicate digest, `../` path, out-of-order record, declared-count
  mismatch, truncated record, unknown record. All seven return rc 3 and
  `TR_RUN STOP`, never FAIL and never PASS.
- **C1/C2 — Codex F1 / Claude F2.** One op returns a reasoned rc 3. Repaired:
  `TR_OP_NOT_EVALUABLE`, `TR_RUN_CLASS deviant=0 not_evaluable=1`,
  `TR_RUN STOP`, exit **3**. Reverted: `TR_RUN FAIL`, exit **1** — the run
  accusing the host of deviant state it never observed.
- **C3 — the precedence rule, defined and tested.** A connected listener (rc 1,
  a completed observation) followed by an `always` op that cannot be evaluated
  (rc 3) yields `TR_RUN_CLASS deviant=1 not_evaluable=1` and `TR_RUN FAIL` at
  exit 1, with `first_fail=01 first_not_evaluable=02` both recorded. A real
  deviant observation is never demoted, and the STOP is never lost.
- **C4/C5 — first-FAIL ordering is unchanged.** GREEN emits
  `TR_OP_SKIPPED id=02 reason=prior_sequence_mismatch` and still runs 03 and 04;
  the mutated skip predicate runs 02. Identical to the round-1 behaviour the
  Claude audit re-verified.
- **D1/D2 — Codex F3 on the operator side.** With a fake `ssh.cmd` first on
  `PATH`: reverting one line to `Get-Command` resolution executes it
  (`FAKE_SSH_EXECUTED`, `TR_RUN PASS`, exit 0 — a green run against an attacker's
  binary). The repaired file records
  `TR_PROGRAM name=ssh path=… sha256=… resolution=pinned_absolute chain=trusted`
  and the child prints `PINNED_PROGRAM_RAN`.
- **D3 — the child environment is constructed, not inherited.** `PYTHONPATH` was
  set to `C:\attacker\pythonpath` in the parent and a decoy directory was first
  on the parent's `PATH`; the child's own `set` output contains neither. `PATH`
  is the frozen literal, `TEMP`/`TMP` are the run-owned record subdirectory.
- **E1/E2 — Claude F6.** With the hash pins filled and `$RECORD_ROOT` still
  literal, the repaired file emits `TR_STOP reason=unfilled_marker
  field=RECORD_ROOT` and exits 3. Remove the gate and the trap and the same
  fixture reproduces the audit's finding verbatim: an unhandled, **localized**
  `Test-Path : Yolda geçersiz karakterler var.`, no `TR_STOP`, no reason token,
  exit 1.
- **F1/F2 — Codex F8.** The archive is pinned under `01_RUNKIT`; a same-named
  decoy beside the runner is never even hashed, and pinning the decoy's digest
  produces `pinned_file_sha256_mismatch` against the kit copy's digest.
- **F3/F4/F5 — Codex F9.** Op 07 and op 08 resolve
  `ACCEPTED:remote_close_tree.sh` to the frozen Stage-2 path at
  `87157f0ea454df7c1f826a8c76a38f3045dd38efdd8fa347644f79251d3f3f0e`. An absent
  file STOPs `stdin_file_missing`, and naming the same file under the wrong root
  token STOPs as well — the root is part of the pin, not a convention.
- **F6–F9 — Claude N3.** `ssh_stdin` without a stdin file, a row whose kind and
  program disagree, a cwd outside the preregistered set, and a stdin file on a
  non-ssh kind are each refused by name.
- **G1–G7 — the plan reader's seven completion classes**, all executed: clean
  EOF, unterminated final record, hard read error, empty input, CR, control byte,
  non-ASCII byte.
- **H — section 8 row 24, all five arms in one command.** `connection_refused`
  rc 0 (2062 ms, inside the 20000 ms bound), `connected` rc 1, `port_invalid`,
  `timeout_invalid` and `argv_malformed` rc 3. The exact command is the script
  above; round 1's omission of it (Codex F10) is closed.
- **I — the delivered file, exactly as it ships**, dry run, no arguments:
  `TR_STOP reason=unfilled_marker field=BASE_RUN`, exit 3. The draft is
  fail-closed at the *first* frozen constant, before it can touch a path.

## 5. Derivation boundary against the accepted originals

```powershell
$b='MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\02_PREREG'
$d='MTC_COMMAND_CENTER\11_TRIAGE\WPI_BLOCKS_DRAFT'
git diff --no-index -- "$b\remote_setup.sh" "$d\remote_setup_wpi.sh"
git diff --no-index -- "$b\remote_extract_verify.sh" "$d\remote_extract_verify_wpi.sh"
```

```text
remote_setup_wpi.sh           178 insertions(+), 51 deletions(-)   22 hunks
remote_extract_verify_wpi.sh  246 insertions(+), 69 deletions(-)   31 hunks
```

**This is a much larger derivation than round 1 permitted, and that is a
declared amendment, not an accident.** §4 of the preregistration has been amended
in this round to enumerate exactly four permitted classes; the report
(`TRANSPORT_REPAIR_R2_REPORT.md`) raises it as a Lead-visible deviation request
rather than treating it as settled. Every changed region of both files falls in
one of the four:

| Class | Regions in `remote_setup_wpi.sh` | Regions in `remote_extract_verify_wpi.sh` |
|---|---|---|
| 1 — pinned constants | `EXPECT_PREFIX`; new `EXPECT_UID`/`EXPECT_GID`/`EXPECT_PARENT`; `EXPECT_OWNER` → `EXPECT_OWNER_NAME` | archive-constants block (unchanged in shape); `MEMBER_COUNT` derived from `MEMBERS` by `count_records` |
| 2 — program identity | `TOOL_STAT`/`TOOL_MKDIR`/`TOOL_READLINK` + `require_tool`; every call site; `mktemp` and `tr` removed entirely | seven `TOOL_*` pins + `require_tool`; every call site; `mktemp` and `tr` removed entirely |
| 3 — STOP before mutation | `bind_component`, `bind_parent_chain`, `calibrate_absence`, `probe_leaf`, numeric `assert_dir`, allocate-then-assert interleaving | `bind_dir`, `calibrate_absence`, `probe_path` |
| 4 — status before stdout | `allocate` refuses any `mkdir` diagnostic | `run_capture` (sentinel rc + two-pass diagnostic equality + termination + CR refusal); re-hash after listing; `chmod`/`sha256sum` diagnostics adjudicated |

No region falls outside the four. The member set is still exactly
`RP0-LIB.sh, RP0-BOOTSTRAP.sh, RP6-P0.sh, RP7-WPI-RO.sh, run_p0.sh, run_ro.sh`,
and `RP1-B3.sh` is still excluded; all concrete archive values remain
`<PIN-AT-FREEZE>`.

## 6. Coverage accounting

Counts are bookkeeping, not closure — the closure is the transcripts above. They
are stated separately for arms actually executed in this round, arms inherited
from round 1 and re-executed here, and arms still not driven.

**Functions and arms executed in this round (all with real output above):**

| Unit | Executed |
|---|---|
| `transport_runner.ps1` | `Read-StrictAsciiLines` (7 of 7 completion classes), `Read-RemoteCloseRecord` (complete + 7 refusal clauses), `Invoke-LocalBind` (PASS, 3 diff classes, set-SHA STOP, `local_dir_absent`), `Get-Sha256OfText` (reached, and its output compared), `Invoke-ExternalProcess` (10 real child processes across the arms), `Invoke-TcpProbe` (5 of 8 arms), `Test-ReparsePoint`, `Test-TrustedProgramChain`, `Resolve-StdinPath` (both roots + both refusals), `Assert-MarkerFree`, the top-level `trap`, and the outcome classifier (PASS / FAIL / STOP / mixed precedence) |
| `remote_setup_wpi.sh` | `require_tool` (3 pins + 2 refusals), `bind_component`/`bind_parent_chain` (5 components + symlink + world-writable refusals), `calibrate_absence`, `probe_leaf` (absent / dir / 2 STOP classes), `allocate`, `assert_dir` (numeric PASS + numeric FAIL), `stop`, `fail`, `note` |
| `remote_extract_verify_wpi.sh` | `require_tool` (7 pins), `count_records`, `bind_dir`, `calibrate_absence`, `probe_path`, `run_capture` (PASS / diagnostics / unterminated / hard-fail / empty-optional), `archive_digest` ×2 with the re-hash comparison, `stop`, `fail`, `note` |
| `run_p0.sh`, `run_ro.sh` | `require_tool` (2 pins + symlink + writable refusals), `require_block` (PASS / symlink STOP / digest-mismatch STOP), `p0w_stop`/`row_stop`, and the ssh-stdin protection on all three sourced children |

`Test-Ascii` had zero call sites in round 1 and has been **deleted**, so the dead
function Claude F4 named no longer exists.

**Still not driven, and therefore supplemental — not closure evidence:**

| Arm | Why | Direction of failure |
|---|---|---|
| `Invoke-TcpProbe` `timeout` | needs a black-holed non-ASCII-route destination outside this envelope; §8 row 24 authorises `connection_refused` **or** `timeout` as rc 0, so it is a prereg classification, not a runner branch | admits a dropped SYN as a closed port — unchanged from round 1 and disclosed there too |
| `Invoke-TcpProbe` `connect_incomplete`, `local_exception`, `socket_error` | require a socket terminating in a state loopback will not produce | all three STOP at rc 3 |
| `Invoke-LocalBind` `local_reparse_point`, `local_path_outside_dir`, `local_duplicate_name`, `local_hash_error`, `local_enumeration_error` | need a reparse point or a name collision the Windows fixture cannot produce without elevation | all STOP at rc 3 |
| `Test-TrustedProgramChain` untrusted-ACE and reparse branches | require writing an ACE onto a System32 object | STOP at rc 3 |
| `program_sha256_mismatch`, `plan_sha256_mismatch`, `stdin_sha256_mismatch`, `record_root_already_exists`, `capture_hash_failed`, `record_finalize_failed` | pin-comparison and I/O branches; `pinned_file_sha256_mismatch` **is** driven (F2) and is the same comparison | STOP at rc 3 |
| `Invoke-ExternalProcess` `stdin_state=incomplete` | needs a child that closes stdin early | STOP at rc 3 |
| the six-member happy path of `remote_extract_verify_wpi.sh` against the **real** WP-I archive | the kit does not exist before Stage 1 | fail-closed on `<PIN-AT-FREEZE>` |

Every undriven arm fails in the STOP direction. None of them can turn a
not-evaluable state into a PASS.

## 7. What this round did not verify

- Real `ssh`/`scp` behaviour, host state, and the actual `remote_close_tree.sh`
  execution on `GATEA-STAGING`. `cmd.exe` stood in for the pinned programs so the
  process-launch path could be driven with no host contact; the substitution is
  declared, printed by the script, and applies to the *pin target only* — the
  pin, digest, chain and environment logic under test is the delivered logic.
- The staging host's tool inventory. The remote scripts pin `/usr/bin/<tool>` and
  refuse a symlinked, non-root-owned or group/other-writable tool. On a host that
  ships coreutils as symlinks they STOP rather than proceed — fail-closed, and
  visible as `tool_is_symlink`. §4 preregisters the `/usr/bin/<tool>` set; Stage 1
  must confirm each pin is a regular root-owned file before freeze, and that
  confirmation is not in this document.
- `RP6-P0.sh` and `RP7-WPI-RO.sh` block internals — separate T0 slots.
- The operator profile directory is *carried* into the child environment rather
  than pinned, because `ssh` reads `known_hosts` under the profile that owns the
  pinned credential. It is validated (absolute, existing container, not a reparse
  point) and recorded in `TR_ENV`, and that is the whole of the claim.
- The Windows OpenSSH digests are `<PIN-AT-FREEZE>`; Stage 1 fills them from the
  operator host. Until then the runner STOPs at `program_pin_unfilled`.

## 8. Syntax, placeholders, identities

```powershell
$d='MTC_COMMAND_CENTER\11_TRIAGE\WPI_BLOCKS_DRAFT'
$e=$null; [Management.Automation.Language.Parser]::ParseFile((Convert-Path "$d\transport_runner.ps1"),[ref]$null,[ref]$e)|Out-Null
if($e.Count){$e}else{'POWERSHELL_5_1_PARSE PASS'}
wsl.exe bash -n /mnt/c/LAB/Tradingview_LAB_CLEAN/$($d -replace '\\','/')/run_p0.sh ... run_ro.sh ... remote_setup_wpi.sh ... remote_extract_verify_wpi.sh
foreach($n in 'run_p0.sh','run_ro.sh','transport_runner.ps1','TRANSPORT_PLAN.tsv','remote_setup_wpi.sh','remote_extract_verify_wpi.sh'){
  $p=Join-Path $d $n;$i=Get-Item $p;"$n`t$($i.Length)`t$((Get-FileHash -Algorithm SHA256 $p).Hash.ToLowerInvariant())"}
```

```text
POWERSHELL_5_1_PARSE PASS            (Windows PowerShell 5.1.26100.8875)
BASH_N PASS (4 files)

run_p0.sh                     5215  e4ddf87b0869ba0fadcb9750e65f4f276c90667e788e489c5921923b0d3e1f80
run_ro.sh                     5933  cd659ee9e1edceb496a5ed08707abd283e3cf5f70a3872ab6f1fdc616ac3f4e8
transport_runner.ps1         45066  2f076ed9a928656fddf22969ea4bf70de895f2c84c73f13b4c64b8040e72aa9a
TRANSPORT_PLAN.tsv            4631  3ff967294ec0f5d592701bc63940b24f2162b38f8734e38c5343930594da7149
remote_setup_wpi.sh          12340  e91bae0827f16cbefe2091980c0a049583bd8ce4173f99e802b2d54a224c29a8
remote_extract_verify_wpi.sh 16614  8eb9c499a306c11595638d8db38b1611cdd38470ba12d2c0e019116e2139d412
```

Byte hygiene: **0 CR bytes** in all six files; `transport_runner.ps1` and
`TRANSPORT_PLAN.tsv` are pure ASCII; the two derived shell scripts carry only the
em-dashes inherited verbatim from the accepted originals. Placeholder census
across the set: 36 `<ALLOCATE-AT-DISPATCH>`, 40 `<PIN-AT-FREEZE>`, all literal;
no RUNID-shaped literal anywhere; `WPI_LOG_DIR` is now the §2-resolved
`/var/log/mtc-bridge` (Claude N1) and `WPI_UNIT_FRAGMENT_SHA256` remains the only
legitimately deferred §2 value.

These are authoring identities only. Stage 1 replaces the marked placeholders,
re-runs this QA, and pins the resulting frozen bytes. No hash in this section is
a dispatch pin, and this document grants no host, freeze, execution, or Git
authority.
