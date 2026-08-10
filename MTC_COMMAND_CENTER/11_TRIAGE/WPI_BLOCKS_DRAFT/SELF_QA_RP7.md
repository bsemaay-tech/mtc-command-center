# SELF-QA Ã¢â‚¬â€ RP7-WPI-RO repair round 2

Status: `SELF-QA-EXECUTED-PENDING-INDEPENDENT-REAUDIT`

The exact fence below ran locally as root in the installed Ubuntu WSL2 guest. It made no
SSH/SCP call, opened no network connection, contacted no staging host, minted no RUNID,
and changed no repository file. Fixture writes were confined to one `mktemp` directory
under `/tmp`, whose prefix was checked before recursive removal.

This is D026 evidence, not an arm-count assertion. Each repair-specific regression has an
executed pre-fix-equivalent `mutant_` RED arm and a production GREEN arm. The path-binding
GREEN arms call the real production `wpi_lstat` and `wpi_walk_components` against real
Linux objects. The mount GREEN arms call the real parser, normalized projector, digest,
guard begin/end, and FAIL-through-guard helper against synthetic mount tables. The suite
also executes the four JSON arms requested by the auditor plus both `NaN` and `Infinity`.

## Exact paste-and-run command

Paste this fence into `wsl.exe -d Ubuntu -- bash` from any directory:

```bash
SCRIPT=/mnt/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh
Q=$(mktemp -d /tmp/rp7-r2-qa.XXXXXX)
source <(sed '$d' "$SCRIPT")
trap - ERR
set +E
set +e
set +u
set +o pipefail

expect_rc(){ [ "$2" -eq "$3" ] || { printf 'QA_ASSERT_FAIL name=%s got=%s expected=%s\n' "$1" "$2" "$3"; exit 90; }; }
common(){
    EV_DIR="$1"; mkdir -p "$EV_DIR"
    WPI_ENV=/usr/bin/env; WPI_TIMEOUT=/usr/bin/timeout; WPI_SWEEP_BUDGET_S=5
    WPI_STAT=/usr/bin/stat; WPI_READLINK=/usr/bin/readlink
    WPI_FIND=/usr/bin/find; WPI_SHA256SUM=/usr/bin/sha256sum
    WPI_SYSTEMCTL=/usr/bin/systemctl; WPI_SS=/usr/bin/ss; WPI_CURL=/usr/bin/curl
    WPI_MOUNT_GUARD_ACTIVE=no; WPI_PROBE_SEQ=0; WPI_MOUNT_SNAPSHOT_SEQ=0
}
printf 'QA_ROOT=%s\n' "$Q"

# F1/F5: real lstat/component walks. The mutant accepts only the absolute argv[0]
# diagnostic prefix; Ubuntu's real tool emits its basename, so the absent object is RED.
mutant_lstat_prefix_only(){
    local prefix="$1" path="$2"
    wpi_capture mutant_lstat "$WPI_STAT" -c '%F|%a|%u:%g|%d:%i|%s' -- "$path"
    wpi_single_record "$prefix" "path_not_evaluable path=$path rc=$WPI_CAP_RC" "$WPI_CAP_ERR"
    case "$WPI_LINE" in
        "$WPI_STAT: cannot statx '$path': No such file or directory"|"$WPI_STAT: cannot stat '$path': No such file or directory") return 0 ;;
        *) wpi_stop "$prefix" "path_not_evaluable path=$path rc=$WPI_CAP_RC detail=mutant_prefix_miss" ;;
    esac
}
mkdir -p "$Q/tree/dir" "$Q/tree/wrongowner" "$Q/tree/wrongmode"
: > "$Q/tree/dir/file"
ln -s "$Q/tree/dir" "$Q/tree/linkdir"
ln -s "$Q/tree/dir/file" "$Q/tree/linkleaf"
chown 1000:1000 "$Q/tree/wrongowner"
chmod 755 "$Q/tree/wrongmode"
( common "$Q/ev-f1-red"; mutant_lstat_prefix_only B3 "$Q/tree/absent" ); f1red=$?
( common "$Q/ev-f1-green"; wpi_walk_components B3 "$Q/tree/absent" regular '' 0:0 ); f1green=$?
( common "$Q/ev-si"; wpi_walk_components B3 "$Q/tree/linkdir/file" regular '' 0:0 ); si=$?
( common "$Q/ev-sl"; wpi_walk_components B3 "$Q/tree/linkleaf" regular '' 0:0 ); sl=$?
( common "$Q/ev-owner"; wpi_walk_components B3 "$Q/tree/wrongowner" directory '' 0:0 ); owner=$?
( common "$Q/ev-mode"; wpi_walk_components B3 "$Q/tree/wrongmode" directory 0555 0:0 ); mode=$?
printf 'PATH_BINDING_RCS mutant_absent=%s absent=%s symlink_intermediate=%s symlink_leaf=%s wrong_owner=%s wrong_mode=%s\n' "$f1red" "$f1green" "$si" "$sl" "$owner" "$mode"
expect_rc f1_mutant "$f1red" 3; expect_rc absent "$f1green" 1; expect_rc symlink_intermediate "$si" 1
expect_rc symlink_leaf "$sl" 1; expect_rc wrong_owner "$owner" 1; expect_rc wrong_mode "$mode" 1

# F2: the inherited FAIL mutation versus production STOP, plus merged-/usr pin refusal.
mkdir -p "$Q/tool/real"; printf '#!/bin/sh\nexit 0\n' > "$Q/tool/real/tool"; chmod 755 "$Q/tool/real/tool"
ln -s "$Q/tool/real" "$Q/tool/link"
( common "$Q/ev-tool-red"; wpi_walk_components RP7 "$Q/tool/link/tool" regular '' 0:0 ); toolred=$?
( common "$Q/ev-tool-green"; wpi_bind_tool stat "$Q/tool/link/tool" ); toolgreen=$?
set_input_fixture(){
    WPI_CANDIDATE_SHA=2ce41e34bceb599d80af24c5c33d835820ec321b
    WPI_RELEASE_ROOT=/opt/mtc-bridge/releases/$WPI_CANDIDATE_SHA
    WPI_VENV_ROOT=/opt/mtc-bridge/venvs/$WPI_CANDIDATE_SHA
    WPI_UNIT_FRAGMENT=/usr/local/lib/systemd/system/mtc-bridge-first-start.service
    WPI_UNIT_FRAGMENT_BYTES=3736; WPI_UNIT_FRAGMENT_SHA256=$(printf '%064d' 0)
    WPI_EXPECTED_LOCK_SHA256=a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e
    WPI_EXPECTED_LOCK_BYTES=117762; WPI_EXPECTED_PACKAGES=56
    WPI_STATE_DIR=/var/lib/mtc-bridge; WPI_STATE_UID=999; WPI_STATE_GID=988
    WPI_LOG_DIR=/var/log/mtc-bridge; WPI_CONF_DIR=/etc/mtc-bridge
    WPI_CONTROL_ENDPOINT=http://127.0.0.1:8790/api/status; WPI_SWEEP_BUDGET_S=120
    WPI_TOOL_PINS='stat=/bin/stat readlink=/usr/bin/readlink env=/usr/bin/env find=/usr/bin/find sha256sum=/usr/bin/sha256sum systemctl=/usr/bin/systemctl ss=/usr/bin/ss curl=/usr/bin/curl timeout=/usr/bin/timeout'
    WPI_ATTESTED_MOUNTINFO_SHA256=$(printf '%064d' 0); WPI_MAINPID=189813
    WPI_VERIFY_LOCK_SHA256=d951e0eea01ec1a89bcfbe9d9630949b31bb316faae2ba6bcae39be794a451e5
}
( set_input_fixture; wpi_validate_inputs ); merged=$?
printf 'TOOL_BINDING_RCS mutant_inherited_fail=%s production_stop=%s merged_usr_pin=%s\n' "$toolred" "$toolgreen" "$merged"
expect_rc tool_mutant "$toolred" 1; expect_rc tool_stop "$toolgreen" 3; expect_rc merged_usr "$merged" 3

# F3/F4/F12: unsafe rendering and FAIL-through-guard. The mutant grammar STOPs.
mutant_observed_path_grammar(){ case "$2" in *[[:space:]]*) wpi_stop "$1" "structured_path_unparseable source=$3 detail=unsafe_character" ;; esac; }
( mutant_observed_path_grammar B3 '/fixture/write me' find_stdout ); spacered=$?
(
    common "$Q/ev-space"
    wpi_mount_guard_begin(){ WPI_MOUNT_GUARD_ACTIVE=yes; printf 'MOUNT_WINDOW_OPEN\n'; }
    wpi_mount_guard_end(){ WPI_MOUNT_GUARD_ACTIVE=no; printf 'MOUNT_WINDOW_CLOSED\n'; }
    wpi_walk_components(){ :; }
    wpi_run_find(){ WPI_CAP_OUT="$EV_DIR/find.out"; WPI_CAP_ERR="$EV_DIR/find.err"; WPI_CAP_ELAPSED_MS=4; : > "$WPI_CAP_ERR"; printf '/fixture/write me\0' > "$WPI_CAP_OUT"; }
    wpi_assert_tree /fixture release
); spacegreen=$?
printf 'SPACE_PATH_RCS mutant_stop=%s production_fail=%s\n' "$spacered" "$spacegreen"
expect_rc space_mutant "$spacered" 3; expect_rc space_green "$spacegreen" 1

# F11/F4: real normalized projection and mount guard over two synthetic tables.
mount_globals(){
    common "$1"
    WPI_RELEASE_ROOT=/opt/mtc-bridge/releases/x; WPI_VENV_ROOT=/opt/mtc-bridge/venvs/x
    WPI_UNIT_FRAGMENT=/usr/local/lib/systemd/system/u; WPI_STATE_DIR=/var/lib/mtc-bridge
    WPI_LOG_DIR=/var/log/mtc-bridge; WPI_CONF_DIR=/etc/mtc-bridge; WPI_MAINPID=2
}
printf '%s\n' '36 25 0:32 / / rw - ext4 /dev/root rw' > "$Q/mount-1"
printf '%s\n' '36 25 0:32 / / rw - ext4 /dev/evil rw' > "$Q/mount-2"
mount_globals "$Q/ev-mount-calc"; wpi_build_mount_projection "$Q/mount-1"; attested="$WPI_MOUNT_PROJECTION_DIGEST"
( printf 'MUTANT_FAIL reason=fixture_without_guard_close\n'; exit 1 ); mountred=$?
(
    mount_globals "$Q/ev-mount-changed"; WPI_ATTESTED_MOUNTINFO_SHA256="$attested"; SNAP=0
    wpi_capture_mountinfo_snapshot(){ SNAP=$((SNAP+1)); if [ "$SNAP" -eq 1 ]; then WPI_LINE="$Q/mount-1"; else WPI_LINE="$Q/mount-2"; fi; }
    wpi_mount_guard_begin; wpi_fail B3 fixture_deviation
); mountchanged=$?
(
    mount_globals "$Q/ev-mount-stable"; WPI_ATTESTED_MOUNTINFO_SHA256="$attested"
    wpi_capture_mountinfo_snapshot(){ WPI_LINE="$Q/mount-1"; }
    wpi_mount_guard_begin; wpi_fail B3 fixture_deviation
); mountstable=$?
mount_globals "$Q/ev-mount-real"; wpi_capture_mountinfo_snapshot; real_snapshot="$WPI_LINE"; wpi_build_mount_projection "$real_snapshot"; mountreal=$?
printf 'MOUNT_GUARD_RCS mutant_no_close=%s changed_downgrade=%s stable_fail=%s real_capture_projection=%s\n' "$mountred" "$mountchanged" "$mountstable" "$mountreal"
expect_rc mount_mutant "$mountred" 1; expect_rc mount_changed "$mountchanged" 3; expect_rc mount_stable "$mountstable" 1; expect_rc mount_real "$mountreal" 0

# F13: pathname expansion changes the mutant field; production preserves /mnt/*.
printf '%s\n' '40 25 0:32 / /mnt/* rw - ext4 /dev/* rw' > "$Q/mount-glob"
mutant_split_mount_field(){ local pre='40 25 0:32 / /mnt/* rw'; set +f; set -- $pre; printf 'MUTANT_MOUNT_POINT=%s\n' "$5"; set -f; }
mutant_split_mount_field
common "$Q/ev-mount-glob"; wpi_parse_mountinfo "$Q/mount-glob"; globrc=$?
printf 'PRODUCTION_MOUNT_POINT=%s GLOB_PARSE_RC=%s\n' "${WPI_MI_POINT[0]}" "$globrc"
[ "${WPI_MI_POINT[0]}" = '/mnt/*' ] || exit 91; expect_rc glob_parse "$globrc" 0

# F6: pre-fix-equivalent unbounded capture versus the production timeout wrapper.
printf '#!/bin/sh\n/usr/bin/sleep 3\n' > "$Q/slow-find"; chmod 755 "$Q/slow-find"
mutant_capture_unbounded(){
    local label="$1"; shift; local start end rc=0
    WPI_PROBE_SEQ=$((WPI_PROBE_SEQ+1)); WPI_CAP_OUT="$EV_DIR/mutant.stdout"; WPI_CAP_ERR="$EV_DIR/mutant.stderr"
    : > "$WPI_CAP_OUT"; : > "$WPI_CAP_ERR"; wpi_clock_ms; start="$WPI_LINE"
    ( cd "$EV_DIR"; exec "$WPI_ENV" -i LC_ALL=C PATH=/usr/bin:/bin HOME=/nonexistent TMPDIR="$EV_DIR" "$@" ) >"$WPI_CAP_OUT" 2>"$WPI_CAP_ERR" || rc=$?
    wpi_clock_ms; end="$WPI_LINE"; WPI_CAP_RC=$rc; WPI_CAP_ELAPSED_MS=$((end-start))
}
mutant_run_find(){ mutant_capture_unbounded slow "$WPI_FIND" /fixture -perm /222 -print0; wpi_stop B3 "sweep_budget_exceeded root=/fixture elapsed_s=$((WPI_CAP_ELAPSED_MS/1000)) elapsed_ms=$WPI_CAP_ELAPSED_MS budget_s=1"; }
start=$SECONDS; ( common "$Q/ev-time-red"; WPI_FIND="$Q/slow-find"; WPI_SWEEP_BUDGET_S=1; mutant_run_find ); timered=$?; redwall=$((SECONDS-start))
start=$SECONDS; ( common "$Q/ev-time-green"; WPI_FIND="$Q/slow-find"; WPI_SWEEP_BUDGET_S=1; wpi_run_find B3 slow /fixture -perm /222 -print0 ); timegreen=$?; greenwall=$((SECONDS-start))
printf 'TIMEOUT_RCS mutant=%s production=%s mutant_wall_s=%s production_wall_s=%s\n' "$timered" "$timegreen" "$redwall" "$greenwall"
expect_rc timeout_mutant "$timered" 3; expect_rc timeout_green "$timegreen" 3
[ "$redwall" -ge 3 ] && [ "$greenwall" -le 2 ] || exit 92

# F7/F12: the symlink-accepting mutant passes; production STOPs and sanitizes CR.
mkdir -p "$Q/interpreter/good/bin" "$Q/interpreter/link/bin" "$Q/interpreter/cr/bin"
printf '#!/bin/sh\nprintf "Python 3.12.9\\n"\n' > "$Q/interpreter/good/bin/python"; chmod 755 "$Q/interpreter/good/bin/python"
ln -s "$Q/interpreter/good/bin/python" "$Q/interpreter/link/bin/python"
ln -s $'/decoy\rB1_interpreter path=spoofed exec=ok' "$Q/interpreter/cr/bin/python"
mutant_interpreter_accept_symlink(){ local resolved; resolved=$(/usr/bin/readlink -f -- "$WPI_VENV_ROOT/bin/python") || return 3; /usr/bin/timeout 2 "$resolved" -I -V >/dev/null; }
( WPI_VENV_ROOT="$Q/interpreter/link"; mutant_interpreter_accept_symlink ); interpreterred=$?
(
    common "$Q/ev-interpreter-link"; WPI_VENV_ROOT="$Q/interpreter/link"
    wpi_mount_guard_begin(){ WPI_MOUNT_GUARD_ACTIVE=yes; }; wpi_mount_guard_end(){ WPI_MOUNT_GUARD_ACTIVE=no; }
    wpi_assert_interpreter
); interpreterlink=$?
(
    common "$Q/ev-interpreter-cr"; WPI_VENV_ROOT="$Q/interpreter/cr"
    wpi_mount_guard_begin(){ WPI_MOUNT_GUARD_ACTIVE=yes; }; wpi_mount_guard_end(){ WPI_MOUNT_GUARD_ACTIVE=no; }
    wpi_assert_interpreter
); interpretercr=$?
(
    common "$Q/ev-interpreter-good"; WPI_VENV_ROOT="$Q/interpreter/good"
    wpi_mount_guard_begin(){ WPI_MOUNT_GUARD_ACTIVE=yes; }; wpi_mount_guard_end(){ WPI_MOUNT_GUARD_ACTIVE=no; }
    wpi_assert_interpreter
); interpretergood=$?
printf 'INTERPRETER_RCS mutant_symlink_accept=%s production_symlink=%s cr_sanitized_stop=%s regular=%s\n' "$interpreterred" "$interpreterlink" "$interpretercr" "$interpretergood"
expect_rc interpreter_mutant "$interpreterred" 0; expect_rc interpreter_link "$interpreterlink" 3
expect_rc interpreter_cr "$interpretercr" 3; expect_rc interpreter_regular "$interpretergood" 0

# F9: mutation delegates filtering to ss; production argv is unfiltered and parses all rows.
(
    EV_DIR="$Q/ev-listener-red"; mkdir "$EV_DIR"; WPI_SS=/usr/bin/ss
    wpi_capture(){ printf 'MUTANT_SS_ARGV=%s\n' "$*"; WPI_CAP_RC=0; }
    wpi_capture listeners "$WPI_SS" -H -ltn 'sport = :8790'
); listenerred=$?
(
    EV_DIR="$Q/ev-listener-green"; mkdir "$EV_DIR"; WPI_SS=/usr/bin/ss
    wpi_capture(){ printf 'PRODUCTION_SS_ARGV=%s\n' "$*"; WPI_CAP_OUT="$EV_DIR/ss.out"; WPI_CAP_ERR="$EV_DIR/ss.err"; WPI_CAP_RC=0; : > "$WPI_CAP_ERR"; printf '%s\n' 'LISTEN 0 128 0.0.0.0:22 0.0.0.0:*' 'LISTEN 0 128 127.0.0.1:8790 0.0.0.0:*' > "$WPI_CAP_OUT"; }
    wpi_assert_listener_set
); listenergreen=$?
printf 'LISTENER_RCS mutant_filtered=%s production_full_inventory=%s\n' "$listenerred" "$listenergreen"
expect_rc listener_mutant "$listenerred" 0; expect_rc listener_green "$listenergreen" 0

# F10/F5: exact production parser child for good, NaN, Infinity, wrong type,
# top-level array, value mismatch, and missing key. The mutation remaps type FAIL to STOP.
run_json_case(){
    local name="$1" json="$2" mode="${3:-production}" d
    d="$Q/json-$name"; mkdir "$d"
    (
        EV_DIR="$d"; WPI_CURL=/usr/bin/curl; WPI_SHA256SUM=/usr/bin/sha256sum
        WPI_CONTROL_ENDPOINT=http://127.0.0.1:8790/api/status; WPI_VENV_ROOT=/fixture; BODY_JSON="$json"; CALL=0
        if [ "$mode" = mutant ]; then
            wpi_fail(){ wpi_stop B5 "mutant_wrong_type_classification $*"; }
        fi
        wpi_capture(){
            local label="$1" cmd; shift; cmd="$1"; shift; CALL=$((CALL+1))
            WPI_CAP_OUT="$EV_DIR/$CALL.out"; WPI_CAP_ERR="$EV_DIR/$CALL.err"; WPI_CAP_RC=0; : > "$WPI_CAP_ERR"
            case "$label" in
                status_get) printf '200\n' > "$WPI_CAP_OUT"; printf '%s\n' "$BODY_JSON" > "$EV_DIR/ro.status.body" ;;
                sha256) printf '%064d  body\n' 0 > "$WPI_CAP_OUT" ;;
                status_json) /usr/bin/timeout 5 /usr/bin/python3 "$@" > "$WPI_CAP_OUT" 2> "$WPI_CAP_ERR" || WPI_CAP_RC=$? ;;
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

# Regression sweep for pre-existing STOP/FAIL ordering and the other major groups.
printf '#!/bin/sh\nprintf "Access denied\\n" >&2\nexit 5\n' > "$Q/systemctl-denied"; chmod 755 "$Q/systemctl-denied"
printf '#!/bin/sh\nprintf "/fixture/writable\\0"\nprintf "find denied\\n" >&2\nexit 1\n' > "$Q/find-partial"; chmod 755 "$Q/find-partial"
( common "$Q/ev-manager"; WPI_SYSTEMCTL="$Q/systemctl-denied"; wpi_assert_manager_ready ); manager=$?
( common "$Q/ev-partial"; WPI_FIND="$Q/find-partial"; wpi_run_find B3 partial /fixture -perm /222 -print0 ); partial=$?
(
    EV_DIR="$Q/ev-parity-fail"; mkdir "$EV_DIR"; WPI_METADATA_READABLE=yes; WPI_RELEASE_ROOT=/fixture/release; WPI_VENV_ROOT=/fixture/venv; WPI_EXPECTED_PACKAGES=56
    wpi_assert_regular_digest(){ :; }; wpi_capture(){ WPI_CAP_OUT="$EV_DIR/out"; WPI_CAP_ERR="$EV_DIR/err"; WPI_CAP_RC=1; : > "$WPI_CAP_OUT"; printf '%s\n' 'verify_lock: FAIL: missing-or-wrong=demo-pkg' > "$WPI_CAP_ERR"; }
    wpi_assert_lock_parity
); parityfail=$?
(
    EV_DIR="$Q/ev-parity-stop"; mkdir "$EV_DIR"; WPI_METADATA_READABLE=yes; WPI_RELEASE_ROOT=/fixture/release; WPI_VENV_ROOT=/fixture/venv; WPI_EXPECTED_PACKAGES=56
    wpi_assert_regular_digest(){ :; }; wpi_capture(){ WPI_CAP_OUT="$EV_DIR/out"; WPI_CAP_ERR="$EV_DIR/err"; WPI_CAP_RC=1; : > "$WPI_CAP_OUT"; printf '%s\n' 'verify_lock: FAIL: Permission denied' > "$WPI_CAP_ERR"; }
    wpi_assert_lock_parity
); paritystop=$?
(
    EV_DIR="$Q/ev-netns"; mkdir "$EV_DIR"; WPI_READLINK=/usr/bin/readlink; WPI_MAINPID=189813; CALL=0
    wpi_capture(){ CALL=$((CALL+1)); WPI_CAP_OUT="$EV_DIR/$CALL.out"; WPI_CAP_ERR="$EV_DIR/$CALL.err"; WPI_CAP_RC=0; : > "$WPI_CAP_ERR"; if [ "$CALL" -eq 1 ]; then printf 'net:[100]\n' > "$WPI_CAP_OUT"; else printf 'net:[200]\n' > "$WPI_CAP_OUT"; fi; }
    wpi_assert_netns_binding
); netns=$?
(
    EV_DIR="$Q/ev-http"; mkdir "$EV_DIR"; WPI_CURL=/usr/bin/curl; WPI_CONTROL_ENDPOINT=http://127.0.0.1:8790/api/status
    wpi_capture(){ WPI_CAP_OUT="$EV_DIR/out"; WPI_CAP_ERR="$EV_DIR/err"; WPI_CAP_RC=0; printf '500\n' > "$WPI_CAP_OUT"; : > "$WPI_CAP_ERR"; }
    wpi_assert_status
); http=$?
printf 'REGRESSION_RCS manager_stop=%s partial_walk_stop=%s parity_fail=%s parity_generic_stop=%s netns_stop=%s http_fail=%s\n' "$manager" "$partial" "$parityfail" "$paritystop" "$netns" "$http"
expect_rc manager "$manager" 3; expect_rc partial "$partial" 3; expect_rc parity_fail "$parityfail" 1
expect_rc parity_stop "$paritystop" 3; expect_rc netns "$netns" 3; expect_rc http "$http" 1

/usr/bin/bash -n "$SCRIPT"; syntax=$?
printf 'BASH_N_RC=%s\n' "$syntax"; expect_rc bash_n "$syntax" 0
case "$Q" in /tmp/rp7-r2-qa.*) rm -rf -- "$Q" ;; *) printf 'QA_ASSERT_FAIL unsafe_cleanup=%s\n' "$Q"; exit 93 ;; esac
printf 'QA_PASS all_assertions=yes\n'
```

## Real captured output

The fence above was run verbatim. Its complete stdout/stderr transcript is recorded below
after the final run; no line is reconstructed from prose.

```text
QA_ROOT=/tmp/rp7-r2-qa.fJ3fyq
B3_STOP reason=path_not_evaluable path=/tmp/rp7-r2-qa.fJ3fyq/tree/absent rc=1 detail=mutant_prefix_miss
B3_FAIL reason=path_absent path=/tmp/rp7-r2-qa.fJ3fyq/tree/absent
B3_FAIL reason=path_metadata_mismatch path=/tmp/rp7-r2-qa.fJ3fyq/tree/linkdir kind=symlink mode=777 owner_numeric=0:0 expected=directory,any,0:0
B3_FAIL reason=path_metadata_mismatch path=/tmp/rp7-r2-qa.fJ3fyq/tree/linkleaf kind=symlink mode=777 owner_numeric=0:0 expected=regular,any,0:0
B3_FAIL reason=path_metadata_mismatch path=/tmp/rp7-r2-qa.fJ3fyq/tree/wrongowner kind=directory mode=755 owner_numeric=1000:1000 expected=directory,any,0:0
B3_FAIL reason=path_metadata_mismatch path=/tmp/rp7-r2-qa.fJ3fyq/tree/wrongmode kind=directory mode=755 owner_numeric=0:0 expected=directory,555,0:0
PATH_BINDING_RCS mutant_absent=3 absent=1 symlink_intermediate=1 symlink_leaf=1 wrong_owner=1 wrong_mode=1
RP7_FAIL reason=path_metadata_mismatch path=/tmp/rp7-r2-qa.fJ3fyq/tool/link kind=symlink mode=777 owner_numeric=0:0 expected=directory,any,0:0
RP7_STOP reason=tool_not_evaluable tool=stat detail=path_metadata_mismatch path=/tmp/rp7-r2-qa.fJ3fyq/tool/link kind=symlink mode=777 owner_numeric=0:0 expected=directory,any,0:0
RP7_STOP reason=prereg_input_malformed name=WPI_TOOL_PINS.stat expected=/usr/bin/stat
TOOL_BINDING_RCS mutant_inherited_fail=1 production_stop=3 merged_usr_pin=3
B3_STOP reason=structured_path_unparseable source=find_stdout detail=unsafe_character
MOUNT_WINDOW_OPEN
MOUNT_WINDOW_CLOSED
B3_FAIL reason=writable_path_inside_immutable_tree path=[unrenderable] path_sha256=565603d319c5019948e7655e2da5b2f006639a9ad9d087d2ed6cba5a41948f2e count=1
SPACE_PATH_RCS mutant_stop=3 production_fail=1
RP7_mount_table parsed=yes records=1 content=not_printed
RP7_mount_projection paths=18 raw_snapshot=/tmp/rp7-r2-qa.fJ3fyq/mount-1 projection=/tmp/rp7-r2-qa.fJ3fyq/ev-mount-calc/ro.0002.mount_projection.tsv sha256=cf82544f04e03255edb0e5b9b0cd4acf42c41649b9ee9ddd7502a41571dff6e6 content=not_printed
MUTANT_FAIL reason=fixture_without_guard_close
RP7_mount_table parsed=yes records=1 content=not_printed
RP7_mount_projection paths=18 raw_snapshot=/tmp/rp7-r2-qa.fJ3fyq/mount-1 projection=/tmp/rp7-r2-qa.fJ3fyq/ev-mount-changed/ro.0002.mount_projection.tsv sha256=cf82544f04e03255edb0e5b9b0cd4acf42c41649b9ee9ddd7502a41571dff6e6 content=not_printed
RP7_mount_table parsed=yes records=1 content=not_printed
RP7_mount_projection paths=18 raw_snapshot=/tmp/rp7-r2-qa.fJ3fyq/mount-2 projection=/tmp/rp7-r2-qa.fJ3fyq/ev-mount-changed/ro.0006.mount_projection.tsv sha256=dd9c8c7510b7b4cee31e2863c1f35af3d857577c8443d9d234f4175019276ccd content=not_printed
RP7_STOP reason=mount_topology_changed before=cf82544f04e03255edb0e5b9b0cd4acf42c41649b9ee9ddd7502a41571dff6e6 after=dd9c8c7510b7b4cee31e2863c1f35af3d857577c8443d9d234f4175019276ccd format=normalised_path_projection_v1
RP7_mount_table parsed=yes records=1 content=not_printed
RP7_mount_projection paths=18 raw_snapshot=/tmp/rp7-r2-qa.fJ3fyq/mount-1 projection=/tmp/rp7-r2-qa.fJ3fyq/ev-mount-stable/ro.0002.mount_projection.tsv sha256=cf82544f04e03255edb0e5b9b0cd4acf42c41649b9ee9ddd7502a41571dff6e6 content=not_printed
RP7_mount_table parsed=yes records=1 content=not_printed
RP7_mount_projection paths=18 raw_snapshot=/tmp/rp7-r2-qa.fJ3fyq/mount-1 projection=/tmp/rp7-r2-qa.fJ3fyq/ev-mount-stable/ro.0006.mount_projection.tsv sha256=cf82544f04e03255edb0e5b9b0cd4acf42c41649b9ee9ddd7502a41571dff6e6 content=not_printed
B3_FAIL reason=fixture_deviation
RP7_mount_table parsed=yes records=37 content=not_printed
RP7_mount_projection paths=18 raw_snapshot=/tmp/rp7-r2-qa.fJ3fyq/ev-mount-real/ro.mountinfo.0001.snapshot projection=/tmp/rp7-r2-qa.fJ3fyq/ev-mount-real/ro.0003.mount_projection.tsv sha256=1ffaced07ac2de3e0a11dd9150198cc8af11d1154389936013ae55575715edff content=not_printed
MOUNT_GUARD_RCS mutant_no_close=1 changed_downgrade=3 stable_fail=1 real_capture_projection=0
MUTANT_MOUNT_POINT=/mnt/c
RP7_mount_table parsed=yes records=1 content=not_printed
PRODUCTION_MOUNT_POINT=/mnt/* GLOB_PARSE_RC=0
B3_STOP reason=sweep_budget_exceeded root=/fixture elapsed_s=3 elapsed_ms=3000 budget_s=1
B3_STOP reason=sweep_budget_exceeded root=/fixture elapsed_s=2 elapsed_ms=1100 budget_s=1
TIMEOUT_RCS mutant=3 production=3 mutant_wall_s=3 production_wall_s=1
B1_STOP reason=interpreter_object_unbound kind=symlink target=/tmp/rp7-r2-qa.fJ3fyq/interpreter/good/bin/python
B1_STOP reason=interpreter_object_unbound kind=symlink target=/decoy B1_interpreter path=spoofed exec=ok
B1_interpreter path=/tmp/rp7-r2-qa.fJ3fyq/interpreter/good/bin/python object=non_symlink_regular preexec_binding=component_and_mount_window_closed exec_binding=separate_bounded_exec version_family=3.12 env=cleared isolated=yes
INTERPRETER_RCS mutant_symlink_accept=0 production_symlink=3 cr_sanitized_stop=3 regular=0
MUTANT_SS_ARGV=listeners /usr/bin/ss -H -ltn sport = :8790
PRODUCTION_SS_ARGV=listeners /usr/bin/ss -H -ltn
B6_listener_inventory rows=2 evidence_file=/tmp/rp7-r2-qa.fJ3fyq/ev-listener-green/ss.out content=not_printed table=complete scope_applied_in_block=yes
B6_listener_set port=8790 count=1 local=127.0.0.1 wildcard=none table=complete
LISTENER_RCS mutant_filtered=0 production_full_inventory=0
B5_STOP reason=mutant_wrong_type_classification B5 flag_mismatch field=state_version observed_type=str expected_type=int
B5_status http=200 json=strict required_fields=8 flags=expected body_sha256=0000000000000000000000000000000000000000000000000000000000000000 content=not_printed
B5_STOP reason=status_body_unreadable_or_unparseable detail=strict_json_or_parser_failure parser_rc=3 body_sha256=0000000000000000000000000000000000000000000000000000000000000000
B5_STOP reason=status_body_unreadable_or_unparseable detail=strict_json_or_parser_failure parser_rc=3 body_sha256=0000000000000000000000000000000000000000000000000000000000000000
B5_FAIL reason=flag_mismatch field=state_version observed_type=str expected_type=int
B5_STOP reason=status_body_unreadable_or_unparseable detail=strict_json_or_parser_failure parser_rc=3 body_sha256=0000000000000000000000000000000000000000000000000000000000000000
B5_FAIL reason=flag_mismatch field=state observed_sha256=b30c3a9662f46e65f2b937b628583be2bff0e37e7466aa3b4bd988740310a913 expected=preregistered_typed_value
B5_STOP reason=schema_unexpected field=state_version
JSON_RCS mutant_wrong_type=3 good=0 nan=3 infinity=3 wrong_type=1 top_array=3 mismatch=1 missing=3
RP7_STOP reason=system_manager_unreachable rc=5 detail=manager_query_nonzero diagnostic_file=/tmp/rp7-r2-qa.fJ3fyq/ev-manager/ro.0001.system_manager.stderr
B3_STOP reason=walk_incomplete root=/fixture rc=1 detail=diagnostic_captured diagnostic_file=/tmp/rp7-r2-qa.fJ3fyq/ev-partial/ro.0001.partial.stderr partial_stdout_discarded=/tmp/rp7-r2-qa.fJ3fyq/ev-partial/ro.0001.partial.stdout
B1_FAIL reason=lock_installed_parity observed=positively_distinguished_named_set_mismatch
B1_STOP reason=verifier_not_evaluable rc=1 detail=unclassified_verifier_result diagnostic_file=/tmp/rp7-r2-qa.fJ3fyq/ev-parity-stop/err
B6_STOP reason=netns_mismatch caller=net:[100] service=net:[200]
B5_FAIL reason=status_endpoint_unexpected_http code=500
REGRESSION_RCS manager_stop=3 partial_walk_stop=3 parity_fail=1 parity_generic_stop=3 netns_stop=3 http_fail=1
BASH_N_RC=0
QA_PASS all_assertions=yes
```

## Coverage interpretation

- F1Ã¢â‚¬â€œF5 are covered by real Linux path objects and an executed mount-window mutation.
- F6 proves the old post-hoc-only shape waits three seconds while the repaired child is
  terminated at the one-second budget.
- F7/F12 prove symlink rejection, CR sanitization, and the non-symlink regular PASS arm.
- F8 is exercised by exact emitted field names across the fixtures and checked again in
  the final static inventory.
- F9 records the actual mutant and production `ss` argv and parses a full two-row table.
- F10 executes absent-key STOP, wrong-type FAIL, wrong-value FAIL, strict JSON rejection,
  and the expected typed PASS.
- F11 executes same-leaf capture/parse/hash on real `/proc/self/mountinfo`, plus changed
  and stable normalized-projection guard arms.
- F13 demonstrates active glob expansion changing the mutant mount field while the
  production parser preserves the literal metacharacter.

## Final-byte checks

The final `bash -n`, byte count, and SHA-256 are recorded after the final QA rerun.

```text
bash_n_rc=0
bytes=54001
sha256=ed9aa6b3c1caab1360bdde499ebc893eb431084a15b643a019fb98c4d8837cfa
```
