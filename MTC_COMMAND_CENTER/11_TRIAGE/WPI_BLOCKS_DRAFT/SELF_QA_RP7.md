# SELF-QA - RP7-WPI-RO repair round 3

Status: `SELF-QA-EXECUTED-PENDING-INDEPENDENT-REAUDIT`

The exact fence below ran locally in **Git Bash (MSYS2)** on the workstation. It made no
SSH/SCP call, opened no network connection, contacted no staging host, minted no RUNID,
and changed no repository file. Fixture writes were confined to one `mktemp` directory
under `/tmp`, whose prefix was checked before recursive removal.

Round 2's fence ran under WSL2 on uutils coreutils. Re-audit finding 2(a) was that this
proved the wrong branch: uutils emits a basename-prefixed ENOENT diagnostic, while the
Debian 12 target's GNU coreutils emits the absolute `argv[0]` form, and only the latter
survives round 3's narrowed matcher. This round's environment is **GNU coreutils 8.32**,
the target's build family, so the `wpi_lstat` GREEN arm now runs against the real
diagnostic the target produces, with no wrapper at all (`REAL_GNU_DIAGNOSTIC`,
`REAL_GNU_ABSENT`). The round-2 transcript is deliberately **not** carried forward:
round-3 edits (the narrowed ENOENT set, the v2 projection, the `attestation=` field, the
`elapsed_s` rendering) change several of its recorded lines, so republishing it would be
stale evidence.

## Exact command

The fence text below was written verbatim to a file and executed as a fresh child shell
from Git Bash:

```
bash <fence-file>            # exit status 0, terminal line QA_PASS all_assertions=yes
```

It is equally paste-and-run: open `bash` from Git Bash and paste the fence into it. It
aborts with `QA_ASSERT_FAIL` and a nonzero exit on any unexpected result, so `QA_PASS`
is reachable only when every assertion below held.

## What this environment can and cannot represent (disclosed in full)

MSYS2 has no root, and its NTFS mounts are `noacl`, so `chown 0:0` and `chmod 0555` are
silent no-ops; it also cannot create a POSIX symlink or a character device at an
arbitrary path. Three fixture classes exist for exactly those gaps, and nothing else is
substituted anywhere in this suite:

| Fixture | Substitutes only | Everything else is real |
|---|---|---|
| `stat-shim` + variants | numeric ownership (rendered `0:0`), and for one named path per variant the `%F` kind | the real GNU `stat` result for the real object: mode, `dev:inode`, size, exit status, ENOENT classification, stream discipline, and the wrapper's own `argv[0]` in its diagnostic |
| `readlink-plain`, `readlink-cr` | the target string a real `readlink` would print for a symlink MSYS2 cannot create | the production symlink branch, the single-record reader and `wpi_sanitize` run unmodified |
| JSON parser child | Windows CPython's CRLF record terminator, normalised to the LF a Debian CPython emits | real CPython, the real parser source embedded in the block, real exit codes, real strict-JSON behaviour |

Production functions are replaced in only two places, both stated where they occur and
both with their subject elsewhere: `wpi_walk_components` in the write-bit arms (whose
subject is `find`-stdout classification and the FAIL-through-guard path) and
`wpi_capture` in the transport-shaped regression arms. **Both round-2 mount-guard stubs
are gone** - re-audit finding 2(d): every arm that opens a mount window now runs the
real `wpi_mount_guard_begin`/`wpi_mount_guard_end` against an attestation computed from
the live table by the real projector, and `MOUNT_WINDOW_CLOSED` is emitted by a wrapper
*around* the real guard-close rather than by a stub replacing it.

Not reproducible here, and not claimed: a real bind or overlay mount. As in the
re-audit, the mount findings are falsified by appending to a real captured `mountinfo`
table the exact record such a mount would produce.

## The fence

```bash
SCRIPT=/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh
Q=$(mktemp -d /tmp/rp7-r3-qa.XXXXXX)
PYEXE=/c/Python314/python.exe
CR=$'\r'
source <(sed '$d' "$SCRIPT")
trap - ERR
set +E
set +e
set +u
set +o pipefail

expect_rc(){ [ "$2" -eq "$3" ] || { printf 'QA_ASSERT_FAIL name=%s got=%s expected=%s\n' "$1" "$2" "$3"; exit 90; }; }
expect_eq(){ [ "$2" = "$3" ] || { printf 'QA_ASSERT_FAIL name=%s got=[%s] expected=[%s]\n' "$1" "$2" "$3"; exit 90; }; }
expect_ne(){ [ "$2" != "$3" ] || { printf 'QA_ASSERT_FAIL name=%s got=[%s] expected_not=[%s]\n' "$1" "$2" "$3"; exit 90; }; }
common(){
    EV_DIR="$1"; mkdir -p "$EV_DIR"
    WPI_ENV=/usr/bin/env; WPI_TIMEOUT=/usr/bin/timeout; WPI_SWEEP_BUDGET_S=5
    WPI_STAT=/usr/bin/stat; WPI_READLINK=/usr/bin/readlink
    WPI_FIND=/usr/bin/find; WPI_SHA256SUM=/usr/bin/sha256sum
    WPI_SYSTEMCTL=/usr/bin/systemctl; WPI_SS=/usr/bin/ss; WPI_CURL=/usr/bin/curl
    WPI_MOUNT_GUARD_ACTIVE=no; WPI_PROBE_SEQ=0; WPI_MOUNT_SNAPSHOT_SEQ=0
}
proj_globals(){
    common "$1"
    WPI_RELEASE_ROOT=/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b
    WPI_VENV_ROOT=/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b
    WPI_UNIT_FRAGMENT=/usr/local/lib/systemd/system/mtc-bridge-first-start.service
    WPI_STATE_DIR=/var/lib/mtc-bridge; WPI_LOG_DIR=/var/log/mtc-bridge
    WPI_CONF_DIR=/etc/mtc-bridge; WPI_MAINPID=189813
}
printf 'QA_ROOT=%s\n' "$Q"
printf 'QA_ENV bash=%s coreutils_stat=%s uid_gid=%s:%s live_mountinfo_records=%s symlinks=%s\n' \
    "$BASH_VERSION" "$(/usr/bin/stat --version | head -1 | sed 's/.* //')" "$(id -u)" "$(id -g)" \
    "$(wc -l < /proc/self/mountinfo)" "not_representable_msys2"

# ---------------------------------------------------------------------------
# Fixture 1 - metadata shim. Renders the REAL metadata of the REAL object as
# reported by the real GNU coreutils stat, substituting only what MSYS2 cannot
# express: numeric ownership (this filesystem has no root) and, where a fixture
# demands it, the object kind. Mode, dev:inode, size, ENOENT classification,
# exit status and stream discipline are the unmodified real results.
# ---------------------------------------------------------------------------
make_stat_shim(){
    local w="$1"; shift
    cat > "$w" <<'SHIM_EOF'
#!/bin/sh
target=""
for a in "$@"; do target=$a; done
e="${TMPDIR:-/tmp}/.stat_shim.$$"
out=$(/usr/bin/stat "$@" 2>"$e"); rc=$?
if [ "$rc" -ne 0 ]; then
    msg=$(cat "$e"); rm -f "$e"
    case "$msg" in
        *"No such file or directory"*)
            printf "%s: cannot stat '%s': No such file or directory\n" "$0" "$target" >&2 ;;
        *) printf '%s\n' "$msg" >&2 ;;
    esac
    exit "$rc"
fi
rm -f "$e"
kind=${out%%|*}; rest=${out#*|}
mode=${rest%%|*}; rest=${rest#*|}
rest=${rest#*|}
ident=${rest%%|*}; size=${rest#*|}
owner=0:0
SHIM_EOF
    while [ "$#" -ge 3 ]; do
        printf 'if [ "$target" = %s ]; then %s=%s; fi\n' "'$1'" "$2" "'$3'" >> "$w"
        shift 3
    done
    printf '%s\n' 'printf "%s|%s|%s|%s|%s\n" "$kind" "$mode" "$owner" "$ident" "$size"' >> "$w"
    chmod 755 "$w"
}
make_stat_shim "$Q/stat-shim"

# ---------------------------------------------------------------------------
# F2(a) + F4 - ENOENT diagnostic acceptance. The primary GREEN arm uses the
# REAL GNU coreutils stat on a REAL absent object: that is the exact absolute
# argv[0] form the Debian 12 target produces and the form the round-2 uutils
# fence could never emit. The wrapper matrix then falsifies every other form,
# including the three basename spellings this round removed.
# ---------------------------------------------------------------------------
ABSENT="$Q/absent-leaf"
printf 'REAL_GNU_DIAGNOSTIC=[%s]\n' "$(/usr/bin/stat -c '%F' -- "$ABSENT" 2>&1 >/dev/null)"
( common "$Q/ev-diag-real"; wpi_lstat B3 "$ABSENT"; printf 'REAL_GNU_ABSENT kind=%s child_rc=%s\n' "$WPI_META_KIND" "$WPI_CAP_RC"; [ "$WPI_META_KIND" = absent ] || exit 95 ); realabsent=$?

make_stat_diag(){
    local w="$1" msg="$2"
    { printf '%s\n' '#!/bin/sh'
      printf "cat >&2 <<'DIAG_EOF'\n"
      printf '%s\n' "$msg"
      printf '%s\n' 'DIAG_EOF' 'exit 1'
    } > "$w"
    chmod 755 "$w"
}
diag_case(){
    local id="$1" w="$Q/stat-diag-$1" base="stat-diag-$1" msg
    case "$id" in
        abs_statx)  msg="$w: cannot statx '$ABSENT': No such file or directory" ;;
        abs_stat)   msg="$w: cannot stat '$ABSENT': No such file or directory" ;;
        abs_oserr)  msg="$w: cannot stat '$ABSENT': No such file or directory (os error 2)" ;;
        base_statx) msg="$base: cannot statx '$ABSENT': No such file or directory" ;;
        base_stat)  msg="$base: cannot stat '$ABSENT': No such file or directory" ;;
        base_oserr) msg="$base: cannot stat '$ABSENT': No such file or directory (os error 2)" ;;
        foreign)    msg="$w: cannot stat '$ABSENT': Permission denied" ;;
    esac
    make_stat_diag "$w" "$msg"
    ( common "$Q/ev-diag-$id"; WPI_STAT="$w"; wpi_lstat B3 "$ABSENT"; printf 'DIAG_ACCEPTED id=%s kind=%s\n' "$id" "$WPI_META_KIND" )
}
diag_case abs_statx; d1=$?
diag_case abs_stat; d2=$?
diag_case abs_oserr; d3=$?
diag_case base_statx; d4=$?
diag_case base_stat; d5=$?
diag_case base_oserr; d6=$?
diag_case foreign; d7=$?
printf 'STAT_DIAGNOSTIC_RCS real_gnu_absent=%s abs_statx=%s abs_stat=%s abs_oserr=%s base_statx=%s base_stat=%s base_oserr=%s foreign=%s\n' \
    "$realabsent" "$d1" "$d2" "$d3" "$d4" "$d5" "$d6" "$d7"
expect_rc diag_real "$realabsent" 0
expect_rc diag_abs_statx "$d1" 0; expect_rc diag_abs_stat "$d2" 0; expect_rc diag_abs_oserr "$d3" 0
expect_rc diag_base_statx "$d4" 3; expect_rc diag_base_stat "$d5" 3; expect_rc diag_base_oserr "$d6" 3
expect_rc diag_foreign "$d7" 3

# ---------------------------------------------------------------------------
# F1 - normalised_path_projection_v2 versus the round-2 v1 body, verbatim.
# N1 (bind/overlay inside a trusted subtree) and N2 (mount stacked on an
# existing mount point) are the auditor's two falsifications; both must now
# flip, and the v1 body must still be blind to both.
# ---------------------------------------------------------------------------
mutant_build_mount_projection_v1(){
    local snapshot="$1" projection path mp best=-1 best_len=-1 i len
    local -a paths=(
        "$WPI_STAT" "$WPI_READLINK" "$WPI_ENV" "$WPI_FIND" "$WPI_SHA256SUM"
        "$WPI_SYSTEMCTL" "$WPI_SS" "$WPI_CURL" "$WPI_TIMEOUT"
        "$WPI_RELEASE_ROOT" "$WPI_VENV_ROOT" "$WPI_UNIT_FRAGMENT"
        "$WPI_STATE_DIR" "$WPI_LOG_DIR" "$WPI_CONF_DIR"
        /proc/self/mountinfo /proc/self/ns/net "/proc/$WPI_MAINPID/ns/net"
    )
    wpi_parse_mountinfo "$snapshot"
    WPI_PROBE_SEQ=$(( WPI_PROBE_SEQ + 1 ))
    projection="$EV_DIR/ro.$(printf '%04d' "$WPI_PROBE_SEQ").mount_projection_v1.tsv"
    wpi_alloc_leaf "$projection"
    for path in "${paths[@]}"; do
        best=-1; best_len=-1
        for ((i=0; i<${#WPI_MI_POINT[@]}; i++)); do
            mp="${WPI_MI_POINT[$i]}"
            if [ "$mp" = / ] || [ "$path" = "$mp" ] || [[ "$path" == "$mp/"* ]]; then
                len=${#mp}
                if [ "$len" -gt "$best_len" ]; then best="$i"; best_len="$len"; fi
            fi
        done
        [ "$best" -ge 0 ] || wpi_stop RP7 "mount_projection_unbound path=$path"
        printf 'path=%s\tdevice=%s\troot=%s\tmount_point=%s\tfstype=%s\tsource=%s\n' \
            "$path" "${WPI_MI_DEVICE[$best]}" "${WPI_MI_ROOT[$best]}" \
            "${WPI_MI_POINT[$best]}" "${WPI_MI_FSTYPE[$best]}" "${WPI_MI_SOURCE[$best]}" \
            >>"$projection" || wpi_stop RP7 "mount_projection_write_failed path=$projection"
    done
    wpi_sha_file RP7 mount_projection_unreadable "$projection"
    WPI_MOUNT_PROJECTION_DIGEST_V1="$WPI_LINE"
}
v2_digest(){ ( proj_globals "$Q/ev-$2" >/dev/null; wpi_build_mount_projection "$1" >/dev/null; printf '%s' "$WPI_MOUNT_PROJECTION_DIGEST" ); }
v1_digest(){ ( proj_globals "$Q/ev-$2" >/dev/null; mutant_build_mount_projection_v1 "$1" >/dev/null; printf '%s' "$WPI_MOUNT_PROJECTION_DIGEST_V1" ); }

proj_globals "$Q/ev-snapshot"
wpi_capture_mountinfo_snapshot; REAL_SNAP="$WPI_LINE"
cp "$REAL_SNAP" "$Q/n1-clean"
cp "$REAL_SNAP" "$Q/n1-decoy"
printf '%s\n' "900 0 0:99 / $WPI_RELEASE_ROOT/IBKR_PAPER_BRIDGE rw - tmpfs decoy_bind rw" >> "$Q/n1-decoy"
cp "$REAL_SNAP" "$Q/n1-venv-decoy"
printf '%s\n' "901 0 0:98 / $WPI_VENV_ROOT/lib/python3.12/site-packages rw - tmpfs decoy_overlay rw" >> "$Q/n1-venv-decoy"
n1_clean_v2=$(v2_digest "$Q/n1-clean" n1a)
n1_decoy_v2=$(v2_digest "$Q/n1-decoy" n1b)
n1_venv_v2=$(v2_digest "$Q/n1-venv-decoy" n1c)
n1_repeat_v2=$(v2_digest "$Q/n1-clean" n1d)
n1_clean_v1=$(v1_digest "$Q/n1-clean" n1e)
n1_decoy_v1=$(v1_digest "$Q/n1-decoy" n1f)
n1_venv_v1=$(v1_digest "$Q/n1-venv-decoy" n1g)
printf 'N1_REAL_MOUNTINFO records=%s captured_by=wpi_capture_mountinfo_snapshot\n' "$(wc -l < "$REAL_SNAP")"
printf 'N1_V2 clean=%s decoy_bind_under_release=%s decoy_overlay_under_venv=%s repeat_clean=%s\n' \
    "$n1_clean_v2" "$n1_decoy_v2" "$n1_venv_v2" "$n1_repeat_v2"
printf 'N1_V1_ROUND2 clean=%s decoy_bind_under_release=%s decoy_overlay_under_venv=%s\n' \
    "$n1_clean_v1" "$n1_decoy_v1" "$n1_venv_v1"
expect_ne n1_v2_bind_detected "$n1_decoy_v2" "$n1_clean_v2"
expect_ne n1_v2_overlay_detected "$n1_venv_v2" "$n1_clean_v2"
expect_eq n1_v2_deterministic "$n1_repeat_v2" "$n1_clean_v2"
expect_eq n1_v1_bind_blind "$n1_decoy_v1" "$n1_clean_v1"
expect_eq n1_v1_overlay_blind "$n1_venv_v1" "$n1_clean_v1"

printf '%s\n' '36 25 0:32 / / rw - ext4 /dev/root rw' > "$Q/n2-clean"
{ printf '%s\n' '36 25 0:32 / / rw - ext4 /dev/root rw'
  printf '%s\n' '37 36 0:99 / / rw - tmpfs /dev/decoy rw'; } > "$Q/n2-stacked"
{ printf '%s\n' '36 25 0:32 / / rw - ext4 /dev/root rw'
  printf '%s\n' '38 36 0:32 / /usr/bin rw - ext4 /dev/root rw'
  printf '%s\n' '39 36 0:97 / /usr/bin rw - tmpfs /dev/decoytools rw'; } > "$Q/n2-tool-stacked"
{ printf '%s\n' '36 25 0:32 / / rw - ext4 /dev/root rw'
  printf '%s\n' '38 36 0:32 / /usr/bin rw - ext4 /dev/root rw'; } > "$Q/n2-tool-clean"
n2_clean_v2=$(v2_digest "$Q/n2-clean" n2a)
n2_stacked_v2=$(v2_digest "$Q/n2-stacked" n2b)
n2_tool_clean_v2=$(v2_digest "$Q/n2-tool-clean" n2c)
n2_tool_stacked_v2=$(v2_digest "$Q/n2-tool-stacked" n2d)
n2_clean_v1=$(v1_digest "$Q/n2-clean" n2e)
n2_stacked_v1=$(v1_digest "$Q/n2-stacked" n2f)
n2_tool_clean_v1=$(v1_digest "$Q/n2-tool-clean" n2g)
n2_tool_stacked_v1=$(v1_digest "$Q/n2-tool-stacked" n2h)
printf 'N2_V2 clean_root=%s stacked_on_root=%s clean_usr_bin=%s stacked_on_usr_bin=%s\n' \
    "$n2_clean_v2" "$n2_stacked_v2" "$n2_tool_clean_v2" "$n2_tool_stacked_v2"
printf 'N2_V1_ROUND2 clean_root=%s stacked_on_root=%s clean_usr_bin=%s stacked_on_usr_bin=%s\n' \
    "$n2_clean_v1" "$n2_stacked_v1" "$n2_tool_clean_v1" "$n2_tool_stacked_v1"
expect_ne n2_v2_stacked_detected "$n2_stacked_v2" "$n2_clean_v2"
expect_ne n2_v2_tool_stacked_detected "$n2_tool_stacked_v2" "$n2_tool_clean_v2"
expect_eq n2_v1_stacked_blind "$n2_stacked_v1" "$n2_clean_v1"
expect_eq n2_v1_tool_stacked_blind "$n2_tool_stacked_v1" "$n2_tool_clean_v1"

v2_digest "$Q/n2-tool-stacked" shape >/dev/null
SHAPE="$Q/ev-shape/ro.0002.mount_projection.tsv"
printf 'V2_RECORD_SHAPE points=%s subtree=%s subtree_count=%s\n' \
    "$(grep -c '^kind=point' "$SHAPE")" "$(grep -c '^kind=subtree	' "$SHAPE")" "$(grep -c '^kind=subtree_count' "$SHAPE")"
printf 'V2_EFFECTIVE_MOUNT %s\n' "$(grep -m1 '^kind=point	path=/usr/bin/stat	' "$SHAPE" | tr '\t' ' ')"
printf 'V2_SUBTREE_USR_BIN %s\n' "$(grep '^kind=subtree_count	subtree_root=/usr/bin	' "$SHAPE" | tr '\t' ' ')"
expect_rc v2_points "$(grep -c '^kind=point' "$SHAPE")" 20
expect_rc v2_subtree_counts "$(grep -c '^kind=subtree_count' "$SHAPE")" 6

# ---------------------------------------------------------------------------
# F2(b) - the real pre-fix wpi_fail body versus production. MOUNT_WINDOW_CLOSED
# is emitted by a wrapper AROUND the real guard-close, not by a stub replacing
# it, so its absence proves the window really was left open.
# ---------------------------------------------------------------------------
eval "$(declare -f wpi_mount_guard_end | sed '1s/^wpi_mount_guard_end/wpi_real_mount_guard_end/')"
mark_guard_end(){ wpi_mount_guard_end(){ wpi_real_mount_guard_end; printf 'MOUNT_WINDOW_CLOSED\n'; }; }
# The projection covers the tool pins themselves, so an arm that pins a fixture
# tool has a legitimately different topology. Each such arm computes its own
# attestation from the live table with its own pin set - computed, never stubbed.
compute_attestation(){ wpi_capture_mountinfo_snapshot >/dev/null; wpi_build_mount_projection "$WPI_LINE" >/dev/null; WPI_ATTESTED_MOUNTINFO_SHA256="$WPI_MOUNT_PROJECTION_DIGEST"; }
proj_globals "$Q/ev-guard-attest"
wpi_capture_mountinfo_snapshot >/dev/null; GSNAP="$WPI_LINE"
ATTESTED=$(v2_digest "$GSNAP" attest)
printf 'COMPUTED_ATTESTATION sha256=%s format=normalised_path_projection_v2\n' "$ATTESTED"
(
    proj_globals "$Q/ev-fail-mutant"; WPI_ATTESTED_MOUNTINFO_SHA256="$ATTESTED"; mark_guard_end
    wpi_fail(){ printf '%s_FAIL reason=%s\n' "$1" "${*:2}"; exit 1; }
    wpi_mount_guard_begin; wpi_fail B3 fixture_deviation
) > "$Q/fail-mutant.log" 2>&1; failmutant=$?
(
    proj_globals "$Q/ev-fail-green"; WPI_ATTESTED_MOUNTINFO_SHA256="$ATTESTED"; mark_guard_end
    wpi_mount_guard_begin; wpi_fail B3 fixture_deviation
) > "$Q/fail-green.log" 2>&1; failgreen=$?
cat "$Q/fail-mutant.log" "$Q/fail-green.log"
mutclosed=$(grep -c '^MOUNT_WINDOW_CLOSED$' "$Q/fail-mutant.log")
greenclosed=$(grep -c '^MOUNT_WINDOW_CLOSED$' "$Q/fail-green.log")
printf 'FAIL_GUARD_CLOSE mutant_rc=%s mutant_window_closed=%s production_rc=%s production_window_closed=%s\n' \
    "$failmutant" "$mutclosed" "$failgreen" "$greenclosed"
expect_rc fail_mutant_rc "$failmutant" 1; expect_rc fail_mutant_closed "$mutclosed" 0
expect_rc fail_green_rc "$failgreen" 1; expect_rc fail_green_closed "$greenclosed" 1

(
    proj_globals "$Q/ev-guard-changed"; WPI_ATTESTED_MOUNTINFO_SHA256="$ATTESTED"; SNAP=0
    wpi_capture_mountinfo_snapshot(){ SNAP=$((SNAP+1)); if [ "$SNAP" -eq 1 ]; then WPI_LINE="$GSNAP"; else WPI_LINE="$Q/n1-decoy"; fi; }
    wpi_mount_guard_begin; wpi_fail B3 fixture_deviation
); guardchanged=$?
(
    proj_globals "$Q/ev-guard-mismatch"; WPI_ATTESTED_MOUNTINFO_SHA256=$(printf '%064d' 0)
    wpi_mount_guard_begin
); guardmismatch=$?
printf 'MOUNT_GUARD_RCS changed_downgrade=%s attestation_mismatch=%s\n' "$guardchanged" "$guardmismatch"
expect_rc guard_changed "$guardchanged" 3; expect_rc guard_mismatch "$guardmismatch" 3

# ---------------------------------------------------------------------------
# F2(d) - the unsafe-pathname and interpreter arms now run the REAL mount guard
# against a computed attestation. No guard stub remains anywhere in this file.
# ---------------------------------------------------------------------------
mutant_observed_path_grammar(){ case "$2" in *[[:space:]]*) wpi_stop "$1" "structured_path_unparseable source=$3 detail=unsafe_character" ;; esac; }
( mutant_observed_path_grammar B3 '/fixture/write me' find_stdout ); spacered=$?
(
    proj_globals "$Q/ev-space"; WPI_ATTESTED_MOUNTINFO_SHA256="$ATTESTED"
    wpi_walk_components(){ :; }
    wpi_run_find(){ WPI_CAP_OUT="$EV_DIR/find.out"; WPI_CAP_ERR="$EV_DIR/find.err"; WPI_CAP_ELAPSED_MS=4; : > "$WPI_CAP_ERR"; printf '/fixture/write me\0' > "$WPI_CAP_OUT"; }
    wpi_assert_tree /fixture release
); spacegreen=$?
mkdir -p "$Q/imm/sub"; : > "$Q/imm/sub/write me"
(
    proj_globals "$Q/ev-realfind"; WPI_ATTESTED_MOUNTINFO_SHA256="$ATTESTED"
    wpi_walk_components(){ :; }
    wpi_assert_tree "$Q/imm/sub" release
); realfind=$?
printf 'UNSAFE_PATH_RCS mutant_stop=%s suppressed_render_fail=%s real_find_fail=%s\n' "$spacered" "$spacegreen" "$realfind"
expect_rc space_mutant "$spacered" 3; expect_rc space_green "$spacegreen" 1; expect_rc real_find "$realfind" 1

# ---------------------------------------------------------------------------
# F3 - attestation disclosure on all nine tool bindings.
# ---------------------------------------------------------------------------
mkdir -p "$Q/tools"
for t in stat readlink env find sha256sum systemctl ss curl timeout; do
    printf '#!/bin/sh\nexit 0\n' > "$Q/tools/$t"; chmod 755 "$Q/tools/$t"
done
mutant_bind_tool_no_attestation(){
    local name="$1" path="$2"
    wpi_require_absolute "WPI_TOOL_PINS.$name" "$path"
    [ -x "$path" ] || wpi_stop RP7 "tool_not_evaluable tool=$name path=$path detail=not_executable"
    wpi_walk_components RP7 "$path" regular "" 0:0 path_absent path_metadata_mismatch stop "tool_not_evaluable tool=$name"
    printf 'MUTANT_RP7_tool name=%s path=%s owner_numeric=0:0 mode=%s kind=regular resolution=pinned_absolute\n' "$name" "$path" "$WPI_META_MODE"
}
( common "$Q/ev-bind-mutant"; WPI_STAT="$Q/stat-shim"; mutant_bind_tool_no_attestation stat "$Q/tools/stat" ) > "$Q/bind-mutant.log" 2>&1; bindmutant=$?
(
    common "$Q/ev-bind"; WPI_STAT="$Q/stat-shim"
    for t in stat readlink env find sha256sum systemctl ss curl timeout; do
        wpi_bind_tool "$t" "$Q/tools/$t"
    done
) > "$Q/bind.log" 2>&1; bindrc=$?
cat "$Q/bind-mutant.log" "$Q/bind.log"
mutattest=$(grep -c 'attestation=' "$Q/bind-mutant.log")
selfcount=$(grep -c 'attestation=self$' "$Q/bind.log")
boundcount=$(grep -c 'attestation=bound_instrument$' "$Q/bind.log")
selfnames=$(grep 'attestation=self$' "$Q/bind.log" | sed 's/^RP7_tool name=\([a-z0-9]*\) .*/\1/' | tr '\n' ',')
printf 'TOOL_ATTESTATION mutant_rc=%s mutant_attestation_fields=%s production_rc=%s self=%s bound_instrument=%s self_names=%s\n' \
    "$bindmutant" "$mutattest" "$bindrc" "$selfcount" "$boundcount" "$selfnames"
expect_rc bind_mutant_rc "$bindmutant" 0; expect_rc bind_mutant_attest "$mutattest" 0
expect_rc bind_rc "$bindrc" 0; expect_rc bind_self "$selfcount" 4; expect_rc bind_bound "$boundcount" 5
expect_eq bind_self_names "$selfnames" "stat,env,sha256sum,timeout,"

# ---------------------------------------------------------------------------
# F5 - multi-word %F values are routed through wpi_kind_token at both sites.
# ---------------------------------------------------------------------------
( common "$Q/ev-devnull"; wpi_lstat B1 /dev/null; wpi_kind_token "$WPI_META_KIND"; printf 'REAL_CHARDEV raw=[%s] token=[%s]\n' "$WPI_META_KIND" "$WPI_LINE"; [ "$WPI_LINE" = other ] || exit 96 ); devnull=$?
make_stat_shim "$Q/stat-rootchar" / kind 'character special file'
mkdir -p "$Q/venv/bin"
printf '#!/bin/sh\nprintf "Python 3.12.9\\n"\n' > "$Q/venv/bin/python"; chmod 755 "$Q/venv/bin/python"
make_stat_shim "$Q/stat-pychar" "$Q/venv/bin/python" kind 'character special file'
printf 'MUTANT_B3_STOP reason=path_not_evaluable path=/ detail=root_kind_%s\n' 'character special file'
printf 'MUTANT_B1_STOP reason=interpreter_object_unbound kind=%s target=none\n' 'character special file'
( common "$Q/ev-rootchar"; WPI_STAT="$Q/stat-rootchar"; wpi_walk_components B3 "$Q/imm" directory '' 0:0 ) > "$Q/rootchar.log" 2>&1; rootchar=$?
(
    proj_globals "$Q/ev-pychar"
    WPI_STAT="$Q/stat-pychar"; WPI_VENV_ROOT="$Q/venv"; compute_attestation
    wpi_assert_interpreter
) > "$Q/pychar.log" 2>&1; pychar=$?
grep '_STOP' "$Q/rootchar.log" "$Q/pychar.log" | sed 's/^[^:]*://'
printf 'KIND_TOKEN_RCS real_chardev=%s root_kind_stop=%s interpreter_kind_stop=%s root_token_ok=%s interpreter_token_ok=%s\n' \
    "$devnull" "$rootchar" "$pychar" \
    "$(grep -c 'detail=root_kind_other$' "$Q/rootchar.log")" \
    "$(grep -c 'kind=other target=none$' "$Q/pychar.log")"
expect_rc kind_devnull "$devnull" 0; expect_rc kind_root "$rootchar" 3; expect_rc kind_py "$pychar" 3
expect_rc kind_root_token "$(grep -c 'detail=root_kind_other$' "$Q/rootchar.log")" 1
expect_rc kind_py_token "$(grep -c 'kind=other target=none$' "$Q/pychar.log")" 1

# ---------------------------------------------------------------------------
# F6 - the bounding wrapper now runs INSIDE the cleared environment, and still
# bounds. RED is the round-2 ordering, verbatim.
# ---------------------------------------------------------------------------
export WPI_QA_ENV_MARKER=present
mutant_capture_timeout_outside_env(){
    local label="$1"; shift
    local start end rc=0
    WPI_PROBE_SEQ=$(( WPI_PROBE_SEQ + 1 ))
    WPI_CAP_OUT="$EV_DIR/ro.$(printf '%04d' "$WPI_PROBE_SEQ").$label.stdout"
    WPI_CAP_ERR="$EV_DIR/ro.$(printf '%04d' "$WPI_PROBE_SEQ").$label.stderr"
    wpi_alloc_leaf "$WPI_CAP_OUT"; wpi_alloc_leaf "$WPI_CAP_ERR"
    wpi_clock_ms; start="$WPI_LINE"
    (
        cd "$EV_DIR" || exit 125
        exec "$WPI_TIMEOUT" --signal=TERM --kill-after=5s "${WPI_SWEEP_BUDGET_S}s" \
            "$WPI_ENV" -i LC_ALL=C PATH=/usr/bin:/bin HOME=/nonexistent TMPDIR="$EV_DIR" "$@"
    ) >"$WPI_CAP_OUT" 2>"$WPI_CAP_ERR" || rc=$?
    wpi_clock_ms; end="$WPI_LINE"
    WPI_CAP_RC="$rc"; WPI_CAP_ELAPSED_MS=$(( end - start ))
}
make_timeout_probe(){
    local w="$1" out="$2"
    { printf '%s\n' '#!/bin/sh'; printf "/usr/bin/env > '%s'\n" "$out"; printf '%s\n' 'exec /usr/bin/timeout "$@"'; } > "$w"
    chmod 755 "$w"
}
make_timeout_probe "$Q/timeout-probe-red" "$Q/timeout-env-red.txt"
make_timeout_probe "$Q/timeout-probe-green" "$Q/timeout-env-green.txt"
( common "$Q/ev-env-red"; WPI_TIMEOUT="$Q/timeout-probe-red"; mutant_capture_timeout_outside_env envprobe /usr/bin/true ) >/dev/null 2>&1
( common "$Q/ev-env-green"; WPI_TIMEOUT="$Q/timeout-probe-green"; wpi_capture envprobe /usr/bin/true ) >/dev/null 2>&1
redmarker=$(grep -c '^WPI_QA_ENV_MARKER=present$' "$Q/timeout-env-red.txt")
greenmarker=$(grep -c '^WPI_QA_ENV_MARKER=present$' "$Q/timeout-env-green.txt")
printf 'TIMEOUT_ENV mutant_marker=%s mutant_vars=%s production_marker=%s production_vars=%s production_env=[%s]\n' \
    "$redmarker" "$(wc -l < "$Q/timeout-env-red.txt")" "$greenmarker" "$(wc -l < "$Q/timeout-env-green.txt")" \
    "$(sort "$Q/timeout-env-green.txt" | tr '\n' ' ')"
expect_rc timeout_env_red "$redmarker" 1; expect_rc timeout_env_green "$greenmarker" 0

printf '#!/bin/sh\n/usr/bin/sleep 8\n' > "$Q/slow-find"; chmod 755 "$Q/slow-find"
mutant_capture_unbounded(){
    local label="$1"; shift; local start end rc=0
    WPI_PROBE_SEQ=$((WPI_PROBE_SEQ+1)); WPI_CAP_OUT="$EV_DIR/mutant.stdout"; WPI_CAP_ERR="$EV_DIR/mutant.stderr"
    : > "$WPI_CAP_OUT"; : > "$WPI_CAP_ERR"; wpi_clock_ms; start="$WPI_LINE"
    ( cd "$EV_DIR"; exec "$WPI_ENV" -i LC_ALL=C PATH=/usr/bin:/bin HOME=/nonexistent TMPDIR="$EV_DIR" "$@" ) >"$WPI_CAP_OUT" 2>"$WPI_CAP_ERR" || rc=$?
    wpi_clock_ms; end="$WPI_LINE"; WPI_CAP_RC=$rc; WPI_CAP_ELAPSED_MS=$((end-start))
}
mutant_run_find(){ mutant_capture_unbounded slow "$WPI_FIND" /fixture -perm /222 -print0; wpi_stop B3 "sweep_budget_exceeded root=/fixture elapsed_s=$((WPI_CAP_ELAPSED_MS/1000)) elapsed_ms=$WPI_CAP_ELAPSED_MS budget_s=2"; }
start=$SECONDS; ( common "$Q/ev-time-red"; WPI_FIND="$Q/slow-find"; WPI_SWEEP_BUDGET_S=2; mutant_run_find ); timered=$?; redwall=$((SECONDS-start))
start=$SECONDS; ( common "$Q/ev-time-green"; WPI_FIND="$Q/slow-find"; WPI_SWEEP_BUDGET_S=2; wpi_run_find B3 slow /fixture -perm /222 -print0 ); timegreen=$?; greenwall=$((SECONDS-start))
printf 'TIMEOUT_RCS mutant=%s production=%s mutant_wall_s=%s production_wall_s=%s budget_s=2 child_sleep_s=8\n' "$timered" "$timegreen" "$redwall" "$greenwall"
expect_rc timeout_mutant "$timered" 3; expect_rc timeout_green "$timegreen" 3
[ "$redwall" -ge 8 ] && [ "$greenwall" -le 4 ] || { printf 'QA_ASSERT_FAIL name=timeout_wall red=%s green=%s\n' "$redwall" "$greenwall"; exit 92; }

# ---------------------------------------------------------------------------
# Interpreter arms with the REAL guard and the computed attestation.
# ---------------------------------------------------------------------------
mkdir -p "$Q/venvlink/bin"; printf '#!/bin/sh\nexit 0\n' > "$Q/venvlink/bin/python"; chmod 755 "$Q/venvlink/bin/python"
make_stat_shim "$Q/stat-pylink" "$Q/venvlink/bin/python" kind 'symbolic link'
# The CR is produced by the fixture's own printf at run time, not embedded as a
# raw byte in the fixture source, because the MSYS2 shell strips a lone CR when
# it reads a script file.
make_readlink_shim(){ local w="$1" t="$2"; printf '#!/bin/sh\n' > "$w"; printf "printf '%s\\\\n'\n" "$t" >> "$w"; chmod 755 "$w"; }
make_readlink_shim "$Q/readlink-plain" '/decoy/target'
make_readlink_shim "$Q/readlink-cr" '/decoy\rB1_interpreter path=spoofed exec=ok'
(
    proj_globals "$Q/ev-py-good"
    WPI_STAT="$Q/stat-shim"; WPI_VENV_ROOT="$Q/venv"; compute_attestation
    wpi_assert_interpreter
) > "$Q/py-good.log" 2>&1; pygood=$?
(
    proj_globals "$Q/ev-py-link"
    WPI_STAT="$Q/stat-pylink"; WPI_READLINK="$Q/readlink-plain"; WPI_VENV_ROOT="$Q/venvlink"; compute_attestation
    wpi_assert_interpreter
) > "$Q/py-link.log" 2>&1; pylink=$?
(
    proj_globals "$Q/ev-py-cr"
    WPI_STAT="$Q/stat-pylink"; WPI_READLINK="$Q/readlink-cr"; WPI_VENV_ROOT="$Q/venvlink"; compute_attestation
    wpi_assert_interpreter
) > "$Q/py-cr.log" 2>&1; pycr=$?
grep -h -E '^(B1_interpreter|B1_STOP)' "$Q/py-good.log" "$Q/py-link.log" "$Q/py-cr.log"
crforged=$(grep -c '^B1_interpreter' "$Q/py-cr.log")
crstop=$(grep -c '^B1_STOP reason=interpreter_object_unbound kind=symlink target=/decoy B1_interpreter path=spoofed exec=ok$' "$Q/py-cr.log")
printf 'INTERPRETER_RCS regular_pass=%s symlink_stop=%s cr_stop=%s cr_forged_lines=%s cr_single_sanitised_line=%s\n' \
    "$pygood" "$pylink" "$pycr" "$crforged" "$crstop"
expect_rc interpreter_good "$pygood" 0; expect_rc interpreter_link "$pylink" 3; expect_rc interpreter_cr "$pycr" 3
expect_rc interpreter_cr_forged "$crforged" 0; expect_rc interpreter_cr_single "$crstop" 1

# ---------------------------------------------------------------------------
# Regression sweep.
# ---------------------------------------------------------------------------
printf '%s\n' '40 25 0:32 / /mnt/* rw - ext4 /dev/* rw' > "$Q/mount-glob"
mutant_split_mount_field(){ local pre='40 25 0:32 / /mnt/* rw'; set +f; set -- $pre; printf 'MUTANT_MOUNT_POINT=%s\n' "$5"; set -f; }
mutant_split_mount_field
common "$Q/ev-mount-glob"; wpi_parse_mountinfo "$Q/mount-glob"; globrc=$?
printf 'PRODUCTION_MOUNT_POINT=%s GLOB_PARSE_RC=%s\n' "${WPI_MI_POINT[0]}" "$globrc"
[ "${WPI_MI_POINT[0]}" = '/mnt/*' ] || exit 91; expect_rc glob_parse "$globrc" 0

run_json_case(){
    local name="$1" json="$2" mode="${3:-production}" d
    d="$Q/json-$name"; mkdir -p "$d"
    (
        EV_DIR="$d"; WPI_CURL=/usr/bin/curl; WPI_SHA256SUM=/usr/bin/sha256sum
        WPI_CONTROL_ENDPOINT=http://127.0.0.1:8790/api/status; WPI_VENV_ROOT=/fixture; BODY_JSON="$json"; CALL=0
        if [ "$mode" = mutant ]; then wpi_fail(){ wpi_stop B5 "mutant_wrong_type_classification $*"; }; fi
        wpi_capture(){
            local label="$1"; shift; local -a a=("$@"); local n=$(( ${#a[@]} - 1 )); CALL=$((CALL+1))
            WPI_CAP_OUT="$EV_DIR/$CALL.out"; WPI_CAP_ERR="$EV_DIR/$CALL.err"; WPI_CAP_RC=0; : > "$WPI_CAP_ERR"
            case "$label" in
                status_get) printf '200\n' > "$WPI_CAP_OUT"; printf '%s\n' "$BODY_JSON" > "$EV_DIR/ro.status.body" ;;
                sha256) printf '%064d  body\n' 0 > "$WPI_CAP_OUT" ;;
                status_json) a[$n]="$(cygpath -w "${a[$n]}")"
                    # Real CPython, real parser source. Windows CPython terminates
                    # lines CRLF; the fixture normalises to the LF a Debian CPython
                    # emits. The block's own readers are untouched.
                    /usr/bin/timeout 20 "$PYEXE" "${a[@]:1}" > "$EV_DIR/py.raw" 2> "$EV_DIR/py.raw.err" || WPI_CAP_RC=$?
                    tr -d '\r' < "$EV_DIR/py.raw" > "$WPI_CAP_OUT"
                    tr -d '\r' < "$EV_DIR/py.raw.err" > "$WPI_CAP_ERR" ;;
            esac
        }
        wpi_assert_status
    )
    return $?
}
base='"state":"DISARMED","state_version":1,"mode":"credential_free_disarmed","network":"disabled","exchange_conn":"disabled","exchange_enabled":false,"credential_lookup":"disabled","arm_enabled":false'
wrong_type='{ "state":"DISARMED","state_version":"1","mode":"credential_free_disarmed","network":"disabled","exchange_conn":"disabled","exchange_enabled":false,"credential_lookup":"disabled","arm_enabled":false }'
run_json_case type-red "$wrong_type" mutant; typered=$?
run_json_case good "{$base}"; jgood=$?
run_json_case nan "{$base,\"extra\":NaN}"; jnan=$?
run_json_case infinity "{$base,\"extra\":Infinity}"; jinf=$?
run_json_case wrong-type "$wrong_type"; jtype=$?
run_json_case top-array '[]'; jtop=$?
run_json_case mismatch '{"state":"ARMED","state_version":1,"mode":"credential_free_disarmed","network":"disabled","exchange_conn":"disabled","exchange_enabled":false,"credential_lookup":"disabled","arm_enabled":false}'; jmis=$?
run_json_case missing '{"state":"DISARMED"}'; jmissing=$?
printf 'JSON_RCS mutant_wrong_type=%s good=%s nan=%s infinity=%s wrong_type=%s top_array=%s mismatch=%s missing=%s\n' "$typered" "$jgood" "$jnan" "$jinf" "$jtype" "$jtop" "$jmis" "$jmissing"
expect_rc type_mutant "$typered" 3; expect_rc json_good "$jgood" 0; expect_rc json_nan "$jnan" 3; expect_rc json_inf "$jinf" 3
expect_rc json_type "$jtype" 1; expect_rc json_top "$jtop" 3; expect_rc json_mismatch "$jmis" 1; expect_rc json_missing "$jmissing" 3

(
    EV_DIR="$Q/ev-listener-red"; mkdir -p "$EV_DIR"; WPI_SS=/usr/bin/ss
    wpi_capture(){ printf 'MUTANT_SS_ARGV=%s\n' "$*"; WPI_CAP_RC=0; }
    wpi_capture listeners "$WPI_SS" -H -ltn 'sport = :8790'
); listenerred=$?
(
    EV_DIR="$Q/ev-listener-green"; mkdir -p "$EV_DIR"; WPI_SS=/usr/bin/ss
    wpi_capture(){ printf 'PRODUCTION_SS_ARGV=%s\n' "$*"; WPI_CAP_OUT="$EV_DIR/ss.out"; WPI_CAP_ERR="$EV_DIR/ss.err"; WPI_CAP_RC=0; : > "$WPI_CAP_ERR"; printf '%s\n' 'LISTEN 0 128 0.0.0.0:22 0.0.0.0:*' 'LISTEN 0 128 127.0.0.1:8790 0.0.0.0:*' > "$WPI_CAP_OUT"; }
    wpi_assert_listener_set
); listenergreen=$?
(
    EV_DIR="$Q/ev-listener-addr"; mkdir -p "$EV_DIR"; WPI_SS=/usr/bin/ss
    wpi_capture(){ WPI_CAP_OUT="$EV_DIR/ss.out"; WPI_CAP_ERR="$EV_DIR/ss.err"; WPI_CAP_RC=0; : > "$WPI_CAP_ERR"; printf '%s\n' 'LISTEN 0 128 10.0.0.5:8790 0.0.0.0:*' > "$WPI_CAP_OUT"; }
    wpi_assert_listener_set
); listeneraddr=$?
printf 'LISTENER_RCS mutant_filtered=%s production_full_inventory=%s non_preregistered_address=%s\n' "$listenerred" "$listenergreen" "$listeneraddr"
expect_rc listener_mutant "$listenerred" 0; expect_rc listener_green "$listenergreen" 0; expect_rc listener_addr "$listeneraddr" 1

printf '#!/bin/sh\nprintf "Access denied\\n" >&2\nexit 5\n' > "$Q/systemctl-denied"; chmod 755 "$Q/systemctl-denied"
printf '#!/bin/sh\nprintf "/fixture/writable\\0"\nprintf "find denied\\n" >&2\nexit 1\n' > "$Q/find-partial"; chmod 755 "$Q/find-partial"
( common "$Q/ev-manager"; WPI_SYSTEMCTL="$Q/systemctl-denied"; wpi_assert_manager_ready ); manager=$?
( common "$Q/ev-partial"; WPI_FIND="$Q/find-partial"; wpi_run_find B3 partial /fixture -perm /222 -print0 ); partial=$?
(
    EV_DIR="$Q/ev-parity-fail"; mkdir -p "$EV_DIR"; WPI_METADATA_READABLE=yes; WPI_RELEASE_ROOT=/fixture/release; WPI_VENV_ROOT=/fixture/venv; WPI_EXPECTED_PACKAGES=56
    wpi_assert_regular_digest(){ :; }; wpi_capture(){ WPI_CAP_OUT="$EV_DIR/out"; WPI_CAP_ERR="$EV_DIR/err"; WPI_CAP_RC=1; : > "$WPI_CAP_OUT"; printf '%s\n' 'verify_lock: FAIL: missing-or-wrong=demo-pkg' > "$WPI_CAP_ERR"; }
    wpi_assert_lock_parity
); parityfail=$?
(
    EV_DIR="$Q/ev-parity-stop"; mkdir -p "$EV_DIR"; WPI_METADATA_READABLE=yes; WPI_RELEASE_ROOT=/fixture/release; WPI_VENV_ROOT=/fixture/venv; WPI_EXPECTED_PACKAGES=56
    wpi_assert_regular_digest(){ :; }; wpi_capture(){ WPI_CAP_OUT="$EV_DIR/out"; WPI_CAP_ERR="$EV_DIR/err"; WPI_CAP_RC=1; : > "$WPI_CAP_OUT"; printf '%s\n' 'verify_lock: FAIL: Permission denied' > "$WPI_CAP_ERR"; }
    wpi_assert_lock_parity
); paritystop=$?
(
    EV_DIR="$Q/ev-netns"; mkdir -p "$EV_DIR"; WPI_READLINK=/usr/bin/readlink; WPI_MAINPID=189813; CALL=0
    wpi_capture(){ CALL=$((CALL+1)); WPI_CAP_OUT="$EV_DIR/$CALL.out"; WPI_CAP_ERR="$EV_DIR/$CALL.err"; WPI_CAP_RC=0; : > "$WPI_CAP_ERR"; if [ "$CALL" -eq 1 ]; then printf 'net:[100]\n' > "$WPI_CAP_OUT"; else printf 'net:[200]\n' > "$WPI_CAP_OUT"; fi; }
    wpi_assert_netns_binding
); netns=$?
(
    EV_DIR="$Q/ev-http"; mkdir -p "$EV_DIR"; WPI_CURL=/usr/bin/curl; WPI_CONTROL_ENDPOINT=http://127.0.0.1:8790/api/status
    wpi_capture(){ WPI_CAP_OUT="$EV_DIR/out"; WPI_CAP_ERR="$EV_DIR/err"; WPI_CAP_RC=0; printf '500\n' > "$WPI_CAP_OUT"; : > "$WPI_CAP_ERR"; }
    wpi_assert_status
); http=$?
printf 'REGRESSION_RCS manager_stop=%s partial_walk_stop=%s parity_fail=%s parity_generic_stop=%s netns_stop=%s http_fail=%s\n' "$manager" "$partial" "$parityfail" "$paritystop" "$netns" "$http"
expect_rc manager "$manager" 3; expect_rc partial "$partial" 3; expect_rc parity_fail "$parityfail" 1
expect_rc parity_stop "$paritystop" 3; expect_rc netns "$netns" 3; expect_rc http "$http" 1

/usr/bin/bash -n "$SCRIPT"; syntax=$?
printf 'BASH_N_RC=%s BYTES=%s SHA256=%s\n' "$syntax" "$(wc -c < "$SCRIPT")" "$(sha256sum "$SCRIPT" | cut -d' ' -f1)"
expect_rc bash_n "$syntax" 0
case "$Q" in /tmp/rp7-r3-qa.*) rm -rf -- "$Q" ;; *) printf 'QA_ASSERT_FAIL unsafe_cleanup=%s\n' "$Q"; exit 93 ;; esac
printf 'QA_PASS all_assertions=yes\n'
```

## Real captured output

The fence above was run verbatim. Its complete stdout/stderr transcript is recorded
below from the final run; no line is reconstructed from prose.

```text
QA_ROOT=/tmp/rp7-r3-qa.A5Ueex
QA_ENV bash=5.2.37(1)-release coreutils_stat=8.32 uid_gid=4096:4096 live_mountinfo_records=4 symlinks=not_representable_msys2
REAL_GNU_DIAGNOSTIC=[/usr/bin/stat: cannot stat '/tmp/rp7-r3-qa.A5Ueex/absent-leaf': No such file or directory]
REAL_GNU_ABSENT kind=absent child_rc=1
DIAG_ACCEPTED id=abs_statx kind=absent
DIAG_ACCEPTED id=abs_stat kind=absent
DIAG_ACCEPTED id=abs_oserr kind=absent
B3_STOP reason=path_not_evaluable path=/tmp/rp7-r3-qa.A5Ueex/absent-leaf rc=1 detail=unclassified_diagnostic diagnostic_file=/tmp/rp7-r3-qa.A5Ueex/ev-diag-base_statx/ro.0001.lstat.stderr
B3_STOP reason=path_not_evaluable path=/tmp/rp7-r3-qa.A5Ueex/absent-leaf rc=1 detail=unclassified_diagnostic diagnostic_file=/tmp/rp7-r3-qa.A5Ueex/ev-diag-base_stat/ro.0001.lstat.stderr
B3_STOP reason=path_not_evaluable path=/tmp/rp7-r3-qa.A5Ueex/absent-leaf rc=1 detail=unclassified_diagnostic diagnostic_file=/tmp/rp7-r3-qa.A5Ueex/ev-diag-base_oserr/ro.0001.lstat.stderr
B3_STOP reason=path_not_evaluable path=/tmp/rp7-r3-qa.A5Ueex/absent-leaf rc=1 detail=unclassified_diagnostic diagnostic_file=/tmp/rp7-r3-qa.A5Ueex/ev-diag-foreign/ro.0001.lstat.stderr
STAT_DIAGNOSTIC_RCS real_gnu_absent=0 abs_statx=0 abs_stat=0 abs_oserr=0 base_statx=3 base_stat=3 base_oserr=3 foreign=3
N1_REAL_MOUNTINFO records=4 captured_by=wpi_capture_mountinfo_snapshot
N1_V2 clean=0d38de2c7789dc17bf0d247a76a43ccfaf7eeba498ba9673acf1794c70460809 decoy_bind_under_release=48e028dc046561bb4eaf670d4b09b03564b5d50015a3909b4c164ad55fc9ebac decoy_overlay_under_venv=b2e860b298153b7d0126c50793f90a2c6bee51569d1a4ff38ce48d95ddfc7555 repeat_clean=0d38de2c7789dc17bf0d247a76a43ccfaf7eeba498ba9673acf1794c70460809
N1_V1_ROUND2 clean=226bfa6e97eeff8342967f18c0bf6da46e4abcf5afb21a3ca15bed675673bacf decoy_bind_under_release=226bfa6e97eeff8342967f18c0bf6da46e4abcf5afb21a3ca15bed675673bacf decoy_overlay_under_venv=226bfa6e97eeff8342967f18c0bf6da46e4abcf5afb21a3ca15bed675673bacf
N2_V2 clean_root=bef3c8a769a1c5f135913586a57b28d05847d170b7d046780da3b6e5ba6cbd35 stacked_on_root=62c610475998244fb2c0e760efea64aa68f2a9b70a7760694d76957f613dc911 clean_usr_bin=6a99b695cc57832e0ee71196b9f551ff4c49d028c9138e2632c2f2d08e68a06e stacked_on_usr_bin=7cefa0fbe20d1670204b973917b5f5cc23376d9e42959409dddcc17fd682f7fb
N2_V1_ROUND2 clean_root=309e1645500547dc8b370dc621e9bc1ba984ea6f36b1debcd4ccf6c3473ea2bc stacked_on_root=309e1645500547dc8b370dc621e9bc1ba984ea6f36b1debcd4ccf6c3473ea2bc clean_usr_bin=8b4f25af2e3c8977afee2f1844e10e1a0d1849959a7736f0d73b364ffb3a8638 stacked_on_usr_bin=8b4f25af2e3c8977afee2f1844e10e1a0d1849959a7736f0d73b364ffb3a8638
V2_RECORD_SHAPE points=20 subtree=2 subtree_count=6
V2_EFFECTIVE_MOUNT kind=point path=/usr/bin/stat device=0:97 root=/ mount_point=/usr/bin fstype=tmpfs source=/dev/decoytools shared_mount_point_records=2
V2_SUBTREE_USR_BIN kind=subtree_count subtree_root=/usr/bin records=2
COMPUTED_ATTESTATION sha256=0d38de2c7789dc17bf0d247a76a43ccfaf7eeba498ba9673acf1794c70460809 format=normalised_path_projection_v2
RP7_mount_table parsed=yes records=4 content=not_printed
RP7_mount_projection format=normalised_path_projection_v2 points=20 roots=6 mount_records=4 raw_snapshot=/tmp/rp7-r3-qa.A5Ueex/ev-fail-mutant/ro.mountinfo.0001.snapshot projection=/tmp/rp7-r3-qa.A5Ueex/ev-fail-mutant/ro.0003.mount_projection.tsv sha256=0d38de2c7789dc17bf0d247a76a43ccfaf7eeba498ba9673acf1794c70460809 content=not_printed
B3_FAIL reason=fixture_deviation
RP7_mount_table parsed=yes records=4 content=not_printed
RP7_mount_projection format=normalised_path_projection_v2 points=20 roots=6 mount_records=4 raw_snapshot=/tmp/rp7-r3-qa.A5Ueex/ev-fail-green/ro.mountinfo.0001.snapshot projection=/tmp/rp7-r3-qa.A5Ueex/ev-fail-green/ro.0003.mount_projection.tsv sha256=0d38de2c7789dc17bf0d247a76a43ccfaf7eeba498ba9673acf1794c70460809 content=not_printed
RP7_mount_table parsed=yes records=4 content=not_printed
RP7_mount_projection format=normalised_path_projection_v2 points=20 roots=6 mount_records=4 raw_snapshot=/tmp/rp7-r3-qa.A5Ueex/ev-fail-green/ro.mountinfo.0002.snapshot projection=/tmp/rp7-r3-qa.A5Ueex/ev-fail-green/ro.0008.mount_projection.tsv sha256=0d38de2c7789dc17bf0d247a76a43ccfaf7eeba498ba9673acf1794c70460809 content=not_printed
MOUNT_WINDOW_CLOSED
B3_FAIL reason=fixture_deviation
FAIL_GUARD_CLOSE mutant_rc=1 mutant_window_closed=0 production_rc=1 production_window_closed=1
RP7_mount_table parsed=yes records=4 content=not_printed
RP7_mount_projection format=normalised_path_projection_v2 points=20 roots=6 mount_records=4 raw_snapshot=/tmp/rp7-r3-qa.A5Ueex/ev-guard-attest/ro.mountinfo.0001.snapshot projection=/tmp/rp7-r3-qa.A5Ueex/ev-guard-changed/ro.0002.mount_projection.tsv sha256=0d38de2c7789dc17bf0d247a76a43ccfaf7eeba498ba9673acf1794c70460809 content=not_printed
RP7_mount_table parsed=yes records=5 content=not_printed
RP7_mount_projection format=normalised_path_projection_v2 points=20 roots=6 mount_records=5 raw_snapshot=/tmp/rp7-r3-qa.A5Ueex/n1-decoy projection=/tmp/rp7-r3-qa.A5Ueex/ev-guard-changed/ro.0006.mount_projection.tsv sha256=48e028dc046561bb4eaf670d4b09b03564b5d50015a3909b4c164ad55fc9ebac content=not_printed
RP7_STOP reason=mount_topology_changed before=0d38de2c7789dc17bf0d247a76a43ccfaf7eeba498ba9673acf1794c70460809 after=48e028dc046561bb4eaf670d4b09b03564b5d50015a3909b4c164ad55fc9ebac format=normalised_path_projection_v2
RP7_mount_table parsed=yes records=4 content=not_printed
RP7_mount_projection format=normalised_path_projection_v2 points=20 roots=6 mount_records=4 raw_snapshot=/tmp/rp7-r3-qa.A5Ueex/ev-guard-mismatch/ro.mountinfo.0001.snapshot projection=/tmp/rp7-r3-qa.A5Ueex/ev-guard-mismatch/ro.0003.mount_projection.tsv sha256=0d38de2c7789dc17bf0d247a76a43ccfaf7eeba498ba9673acf1794c70460809 content=not_printed
RP7_STOP reason=mount_topology_mismatch observed=0d38de2c7789dc17bf0d247a76a43ccfaf7eeba498ba9673acf1794c70460809 attested=0000000000000000000000000000000000000000000000000000000000000000 format=normalised_path_projection_v2
MOUNT_GUARD_RCS changed_downgrade=3 attestation_mismatch=3
B3_STOP reason=structured_path_unparseable source=find_stdout detail=unsafe_character
RP7_mount_table parsed=yes records=4 content=not_printed
RP7_mount_projection format=normalised_path_projection_v2 points=20 roots=6 mount_records=4 raw_snapshot=/tmp/rp7-r3-qa.A5Ueex/ev-space/ro.mountinfo.0001.snapshot projection=/tmp/rp7-r3-qa.A5Ueex/ev-space/ro.0003.mount_projection.tsv sha256=0d38de2c7789dc17bf0d247a76a43ccfaf7eeba498ba9673acf1794c70460809 content=not_printed
RP7_mount_table parsed=yes records=4 content=not_printed
RP7_mount_projection format=normalised_path_projection_v2 points=20 roots=6 mount_records=4 raw_snapshot=/tmp/rp7-r3-qa.A5Ueex/ev-space/ro.mountinfo.0002.snapshot projection=/tmp/rp7-r3-qa.A5Ueex/ev-space/ro.0012.mount_projection.tsv sha256=0d38de2c7789dc17bf0d247a76a43ccfaf7eeba498ba9673acf1794c70460809 content=not_printed
B3_FAIL reason=writable_path_inside_immutable_tree path=[unrenderable] path_sha256=565603d319c5019948e7655e2da5b2f006639a9ad9d087d2ed6cba5a41948f2e count=1
RP7_mount_table parsed=yes records=4 content=not_printed
RP7_mount_projection format=normalised_path_projection_v2 points=20 roots=6 mount_records=4 raw_snapshot=/tmp/rp7-r3-qa.A5Ueex/ev-realfind/ro.mountinfo.0001.snapshot projection=/tmp/rp7-r3-qa.A5Ueex/ev-realfind/ro.0003.mount_projection.tsv sha256=0d38de2c7789dc17bf0d247a76a43ccfaf7eeba498ba9673acf1794c70460809 content=not_printed
RP7_mount_table parsed=yes records=4 content=not_printed
RP7_mount_projection format=normalised_path_projection_v2 points=20 roots=6 mount_records=4 raw_snapshot=/tmp/rp7-r3-qa.A5Ueex/ev-realfind/ro.mountinfo.0002.snapshot projection=/tmp/rp7-r3-qa.A5Ueex/ev-realfind/ro.0013.mount_projection.tsv sha256=0d38de2c7789dc17bf0d247a76a43ccfaf7eeba498ba9673acf1794c70460809 content=not_printed
B3_FAIL reason=writable_path_inside_immutable_tree path=/tmp/rp7-r3-qa.A5Ueex/imm/sub count=2
UNSAFE_PATH_RCS mutant_stop=3 suppressed_render_fail=1 real_find_fail=1
MUTANT_RP7_tool name=stat path=/tmp/rp7-r3-qa.A5Ueex/tools/stat owner_numeric=0:0 mode=755 kind=regular resolution=pinned_absolute
RP7_tool name=stat path=/tmp/rp7-r3-qa.A5Ueex/tools/stat owner_numeric=0:0 mode=755 kind=regular resolution=pinned_absolute attestation=self
RP7_tool name=readlink path=/tmp/rp7-r3-qa.A5Ueex/tools/readlink owner_numeric=0:0 mode=755 kind=regular resolution=pinned_absolute attestation=bound_instrument
RP7_tool name=env path=/tmp/rp7-r3-qa.A5Ueex/tools/env owner_numeric=0:0 mode=755 kind=regular resolution=pinned_absolute attestation=self
RP7_tool name=find path=/tmp/rp7-r3-qa.A5Ueex/tools/find owner_numeric=0:0 mode=755 kind=regular resolution=pinned_absolute attestation=bound_instrument
RP7_tool name=sha256sum path=/tmp/rp7-r3-qa.A5Ueex/tools/sha256sum owner_numeric=0:0 mode=755 kind=regular resolution=pinned_absolute attestation=self
RP7_tool name=systemctl path=/tmp/rp7-r3-qa.A5Ueex/tools/systemctl owner_numeric=0:0 mode=755 kind=regular resolution=pinned_absolute attestation=bound_instrument
RP7_tool name=ss path=/tmp/rp7-r3-qa.A5Ueex/tools/ss owner_numeric=0:0 mode=755 kind=regular resolution=pinned_absolute attestation=bound_instrument
RP7_tool name=curl path=/tmp/rp7-r3-qa.A5Ueex/tools/curl owner_numeric=0:0 mode=755 kind=regular resolution=pinned_absolute attestation=bound_instrument
RP7_tool name=timeout path=/tmp/rp7-r3-qa.A5Ueex/tools/timeout owner_numeric=0:0 mode=755 kind=regular resolution=pinned_absolute attestation=self
TOOL_ATTESTATION mutant_rc=0 mutant_attestation_fields=0 production_rc=0 self=4 bound_instrument=5 self_names=stat,env,sha256sum,timeout,
REAL_CHARDEV raw=[character special file] token=[other]
MUTANT_B3_STOP reason=path_not_evaluable path=/ detail=root_kind_character special file
MUTANT_B1_STOP reason=interpreter_object_unbound kind=character special file target=none
B3_STOP reason=path_not_evaluable path=/ detail=root_kind_other
B1_STOP reason=interpreter_object_unbound kind=other target=none
KIND_TOKEN_RCS real_chardev=0 root_kind_stop=3 interpreter_kind_stop=3 root_token_ok=1 interpreter_token_ok=1
TIMEOUT_ENV mutant_marker=1 mutant_vars=104 production_marker=0 production_vars=10 production_env=[HOME=/nonexistent LC_ALL=C MSYSTEM=MINGW64 PATH=/usr/bin:/bin PWD=/c/Users/BarışSemaay/AppData/Local/Temp/rp7-r3-qa.A5Ueex/ev-env-green SHLVL=1 SYSTEMROOT=C:\WINDOWS TMPDIR=/tmp/rp7-r3-qa.A5Ueex/ev-env-green WINDIR=C:\WINDOWS _=/usr/bin/env ]
B3_STOP reason=sweep_budget_exceeded root=/fixture elapsed_s=8 elapsed_ms=8080 budget_s=2
B3_STOP reason=sweep_budget_exceeded root=/fixture elapsed_s=2 elapsed_ms=2200 budget_s=2
TIMEOUT_RCS mutant=3 production=3 mutant_wall_s=8 production_wall_s=2 budget_s=2 child_sleep_s=8
B1_interpreter path=/tmp/rp7-r3-qa.A5Ueex/venv/bin/python object=non_symlink_regular preexec_binding=component_and_mount_window_closed exec_binding=separate_bounded_exec version_family=3.12 env=cleared isolated=yes
B1_STOP reason=interpreter_object_unbound kind=symlink target=/decoy/target
B1_STOP reason=interpreter_object_unbound kind=symlink target=/decoy B1_interpreter path=spoofed exec=ok
INTERPRETER_RCS regular_pass=0 symlink_stop=3 cr_stop=3 cr_forged_lines=0 cr_single_sanitised_line=1
MUTANT_MOUNT_POINT=/mnt/*
RP7_mount_table parsed=yes records=1 content=not_printed
PRODUCTION_MOUNT_POINT=/mnt/* GLOB_PARSE_RC=0
B5_STOP reason=mutant_wrong_type_classification B5 flag_mismatch field=state_version observed_type=str expected_type=int
B5_status http=200 json=strict required_fields=8 flags=expected body_sha256=0000000000000000000000000000000000000000000000000000000000000000 content=not_printed
B5_STOP reason=status_body_unreadable_or_unparseable detail=strict_json_or_parser_failure parser_rc=3 body_sha256=0000000000000000000000000000000000000000000000000000000000000000
B5_STOP reason=status_body_unreadable_or_unparseable detail=strict_json_or_parser_failure parser_rc=3 body_sha256=0000000000000000000000000000000000000000000000000000000000000000
B5_FAIL reason=flag_mismatch field=state_version observed_type=str expected_type=int
B5_STOP reason=status_body_unreadable_or_unparseable detail=strict_json_or_parser_failure parser_rc=3 body_sha256=0000000000000000000000000000000000000000000000000000000000000000
B5_FAIL reason=flag_mismatch field=state observed_sha256=b30c3a9662f46e65f2b937b628583be2bff0e37e7466aa3b4bd988740310a913 expected=preregistered_typed_value
B5_STOP reason=schema_unexpected field=state_version
JSON_RCS mutant_wrong_type=3 good=0 nan=3 infinity=3 wrong_type=1 top_array=3 mismatch=1 missing=3
MUTANT_SS_ARGV=listeners /usr/bin/ss -H -ltn sport = :8790
PRODUCTION_SS_ARGV=listeners /usr/bin/ss -H -ltn
B6_listener_inventory rows=2 evidence_file=/tmp/rp7-r3-qa.A5Ueex/ev-listener-green/ss.out content=not_printed table=complete scope_applied_in_block=yes
B6_listener_set port=8790 count=1 local=127.0.0.1 wildcard=none table=complete
B6_FAIL reason=listener_set_unexpected observed=non_preregistered_address expected=1x127.0.0.1:8790
LISTENER_RCS mutant_filtered=0 production_full_inventory=0 non_preregistered_address=1
RP7_STOP reason=system_manager_unreachable rc=5 detail=manager_query_nonzero diagnostic_file=/tmp/rp7-r3-qa.A5Ueex/ev-manager/ro.0001.system_manager.stderr
B3_STOP reason=walk_incomplete root=/fixture rc=1 detail=diagnostic_captured diagnostic_file=/tmp/rp7-r3-qa.A5Ueex/ev-partial/ro.0001.partial.stderr partial_stdout_discarded=/tmp/rp7-r3-qa.A5Ueex/ev-partial/ro.0001.partial.stdout
B1_FAIL reason=lock_installed_parity observed=positively_distinguished_named_set_mismatch
B1_STOP reason=verifier_not_evaluable rc=1 detail=unclassified_verifier_result diagnostic_file=/tmp/rp7-r3-qa.A5Ueex/ev-parity-stop/err
B6_STOP reason=netns_mismatch caller=net:[100] service=net:[200]
B5_FAIL reason=status_endpoint_unexpected_http code=500
REGRESSION_RCS manager_stop=3 partial_walk_stop=3 parity_fail=1 parity_generic_stop=3 netns_stop=3 http_fail=1
BASH_N_RC=0 BYTES=58012 SHA256=1d118d1581534f5d16b3730efbe642e80e5232fbf8a245d238574907166a7f4e
QA_PASS all_assertions=yes
```

## Coverage interpretation - round-3 findings

**Finding 1 (BLOCK) - projection blind to subtrees and to stacked mounts.** The two
falsifications the auditor ran now flip, and the round-2 body is carried in the fence as
`mutant_build_mount_projection_v1` (its verbatim pre-fix text) so both directions are
executed side by side against the *same* tables:

| Table | v2 (repaired) | v1 (round 2) |
|---|---|---|
| real 4-record `mountinfo`, clean | `0d38de2c…` | `226bfa6e…` |
| + bind mount at `<release>/IBKR_PAPER_BRIDGE` | `48e028dc…` **differs** | `226bfa6e…` **identical - blind** |
| + overlay at `<venv>/lib/python3.12/site-packages` | `b2e860b2…` **differs** | `226bfa6e…` **identical - blind** |
| synthetic, second mount stacked on `/` | `62c61047…` **differs** from `bef3c8a7…` | `309e1645…` **identical - blind** |
| synthetic, second mount stacked on `/usr/bin` | `7cefa0fb…` **differs** from `6a99b695…` | `8b4f25af…` **identical - blind** |

`repeat_clean` re-derives the clean digest bit-for-bit, so the difference is the decoy,
not nondeterminism. `V2_EFFECTIVE_MOUNT` shows the `-ge` tie-break selecting the *last*
record at `/usr/bin` (`source=/dev/decoytools`) with `shared_mount_point_records=2`, and
`V2_SUBTREE_USR_BIN` shows the subtree count that makes the stack visible.
`V2_RECORD_SHAPE` confirms the declared shape: 20 point records, 6 subtree-count records
(five preregistered roots plus the deduplicated `/usr/bin` tool directory).

**Finding 2(a) - the GNU branch had no executed coverage.** `REAL_GNU_DIAGNOSTIC` records
the real GNU coreutils 8.32 message for a real absent object, and `REAL_GNU_ABSENT`
records production `wpi_lstat` classifying it `absent` at child rc 1 - the branch the
Debian target takes, executed, with no fixture in the path. `STAT_DIAGNOSTIC_RCS` then
drives seven wrapper fixtures through the same production code: the three accepted
absolute-`argv[0]` forms all classify `absent` (rc 0), and the three basename forms plus
a foreign `Permission denied` all STOP `detail=unclassified_diagnostic` (rc 3).

**Finding 2(b) - the RED arm was a placebo.** `wpi_fail`'s verbatim pre-fix body (print,
then exit, with no guard close) is now the mutant. `FAIL_GUARD_CLOSE` records
`mutant_window_closed=0` against `production_window_closed=1` at the same rc 1: the
pre-fix body really does leave the mount window open, and the repaired one really does
close it before printing. The marker comes from a wrapper around the real
`wpi_mount_guard_end`, so a stub cannot manufacture it.

**Finding 2(c) - no accepting `wpi_validate_inputs` arm.** Not faked. It is impossible
before freeze: `WPI_FIXED_ATTESTED_MOUNT_PROJECTION_SHA256` is still `<PIN-AT-FREEZE>`,
so `wpi_validate_inputs` necessarily STOPs. Recorded as a **freeze-gate item** in
`STATUS_RP7.md`: the first act after the deploy channel supplies the v2 digest is an
executed accepting-input arm, before dispatch.

**Finding 2(d) - two real guards still stubbed.** No guard stub remains. The
unsafe-pathname arm, the real-`find` arm, and all four interpreter arms open and close
the real window against a computed attestation (`COMPUTED_ATTESTATION`, and per-arm
`compute_attestation` where the arm pins fixture tools, since the projection covers the
tool pins themselves and a fixture pin legitimately changes the topology).
`MOUNT_GUARD_RCS` adds the two guard outcomes: a table that moves between begin and end
downgrades to `mount_topology_changed … format=normalised_path_projection_v2` (rc 3),
and a wrong attestation STOPs at begin as `mount_topology_mismatch` (rc 3).

**Finding 3 - undisclosed self-attestation.** `TOOL_ATTESTATION` executes all nine
bindings: exactly four carry `attestation=self` and they are exactly
`stat,env,sha256sum,timeout`; the other five carry `attestation=bound_instrument`. The
pre-fix line is executed as `MUTANT_RP7_tool` and carries no `attestation=` field at all.

**Finding 4 - ENOENT match widened.** Covered by the same `STAT_DIAGNOSTIC_RCS` matrix:
the three basename forms that round 2 accepted are now rejected, and the three
absolute-`argv[0]` forms - the only ones the block's own invocation can produce - are
accepted. The `statx` + `(os error 2)` combination is deliberately still absent: no
build emits it (uutils uses the `stat` wording), so adding it would widen the set
without a producer, which is the opposite of the finding's intent.

**Finding 5 - residual row grammar.** The two code-side items are executed:
`REAL_CHARDEV` shows the real `/dev/null` character device rendering as raw
`character special file` and mapping to token `other`, and the two production sites now
emit `detail=root_kind_other` and `kind=other target=none` where `MUTANT_B3_STOP` /
`MUTANT_B1_STOP` show the pre-fix multi-word values that broke the space-delimited
grammar. `LISTENER_RCS` adds an executed `observed=non_preregistered_address` FAIL for
the row-22 rendering. The four declaration-side items are draft edits, listed in
`RP7_REPAIR_R3_REPORT.md`.

**Finding 6 - `timeout` outside the cleared environment.** `wpi_capture` now execs `env`
first and `timeout` as its argument. `TIMEOUT_ENV` proves the inversion by having the
bounding process record its own environment: the round-2 ordering (carried verbatim as
`mutant_capture_timeout_outside_env`) leaks the block's environment to `timeout` - 104
variables including the `WPI_QA_ENV_MARKER` sentinel - while production gives it 10
variables and no sentinel. `TIMEOUT_RCS` proves the inversion did not cost the bound: a
real 8-second child against a 2-second budget is terminated at **2 s wall clock**
(rc 124 → `sweep_budget_exceeded`), where the unbounded mutant waits the full 8 s.

**Observation 4 - `elapsed_s` ceiling.** `elapsed_s` is now the truncated whole-second
rendering of `elapsed_ms`, so the emitted pair no longer contradicts itself: the
transcript shows `elapsed_s=2 elapsed_ms=2200` and `elapsed_s=8 elapsed_ms=8080`.
Enforcement is unchanged and remains on milliseconds.

**Observation 1 - late-bound globals.** No conditional assignment of a late-bound global
was added. The one new local (`attestation` in `wpi_bind_tool`) is assigned on every
branch of its `case`, including the default.

## Regression coverage carried through the round

`JSON_RCS` (eight arms, real CPython), `LISTENER_RCS` (unfiltered argv, full-table parse,
plus the new address arm), `PRODUCTION_MOUNT_POINT` (F13 glob literal preserved under
`set -f`), `INTERPRETER_RCS` (regular PASS, symlink STOP, CR-sanitised single physical
line - `cr_forged_lines=0`), `UNSAFE_PATH_RCS` (digest-suppressed rendering and a real
`find` sweep over a real tree, both FAILing through the closing guard), and
`REGRESSION_RCS` (manager STOP, partial-walk STOP, parity FAIL vs generic STOP, netns
STOP, HTTP FAIL) all hold at the round-3 bytes.

## Final-byte checks

```text
bash_n_rc=0
bytes=58012
sha256=1d118d1581534f5d16b3730efbe642e80e5232fbf8a245d238574907166a7f4e
```
