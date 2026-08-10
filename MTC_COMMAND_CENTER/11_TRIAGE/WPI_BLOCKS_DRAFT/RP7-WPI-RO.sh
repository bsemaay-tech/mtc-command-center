#!/usr/bin/env bash
# ===== BLOCK-ID: RP7-WPI-RO ===== [EXECUTABLE PROPOSAL BLOCK]
# WP-I read-only rows 10-24 (PROPOSED DESIGN, DRAFT).
# Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b.
#
# AUTHORITY: authoring only. These bytes grant no host contact, transport,
# RUNID, budget, service, credential, trading, or deployment authority.
#
# Runtime mutation is confined to create-once capture leaves inside EV_DIR,
# which RP0-BOOTSTRAP allocated before this block. No host object is changed.
# File content is never printed: result lines contain paths, metadata, counts,
# classifications, and digests only.
#
# rc contract:
#   0 = PASS   1 = FAIL (completed probe established deviant state)
#   3 = STOP (the predicate could not be evaluated)
#
# Required same-shell order:
#   . RP0-LIB.sh ; . RP0-BOOTSTRAP.sh ; . RP7-WPI-RO.sh
set -Eeuo pipefail
export LC_ALL=C

WPI_SAFE=""
WPI_LINE=""
WPI_CAP_OUT=""
WPI_CAP_ERR=""
WPI_CAP_RC=0
WPI_CAP_ELAPSED_MS=0
WPI_READ_DIAG=""
WPI_META_KIND=""
WPI_META_MODE=""
WPI_META_OWNER=""
WPI_META_ID=""
WPI_META_SIZE=""
WPI_PROBE_SEQ=0
WPI_MOUNT_BEFORE=""
WPI_VENV_WALK_COMPLETE=no
WPI_INTERPRETER_RAN=no
WPI_METADATA_READABLE=no

wpi_stop() { printf '%s_STOP reason=%s\n' "$1" "${*:2}"; exit 3; }
wpi_fail() { printf '%s_FAIL reason=%s\n' "$1" "${*:2}"; exit 1; }

wpi_on_err() {
    local rc=$?
    printf 'RP7_STOP reason=unadjudicated_command_status rc=%s line=%s cmd=[%s]\n' \
        "$rc" "${BASH_LINENO[0]}" "$BASH_COMMAND"
    exit 3
}
trap 'wpi_on_err' ERR

wpi_sanitize() {
    local s="${1-}"
    s="${s//$'\r'/ }"
    s="${s//$'\n'/ }"
    case "$s" in *[![:print:]]*) s="[non_printable_detail_suppressed]" ;; esac
    WPI_SAFE="${s:0:300}"
}

wpi_require_set() {
    local name="$1" value="${2-}"
    [ -n "$value" ] || wpi_stop RP7 "prereg_input_missing name=$name"
}

wpi_require_uint() {
    local name="$1" value="${2-}" minimum="$3"
    wpi_require_set "$name" "$value"
    case "$value" in *[!0-9]*) wpi_stop RP7 "prereg_input_malformed name=$name expected=decimal_digits" ;; esac
    [ "$value" -ge "$minimum" ] || wpi_stop RP7 "prereg_input_malformed name=$name value=$value expected_min=$minimum"
}

wpi_require_sha256() {
    local name="$1" value="${2-}"
    wpi_require_set "$name" "$value"
    [ "${#value}" -eq 64 ] || wpi_stop RP7 "prereg_input_malformed name=$name expected=64_lower_hex"
    case "$value" in *[!0-9a-f]*) wpi_stop RP7 "prereg_input_malformed name=$name expected=64_lower_hex" ;; esac
}

wpi_require_absolute() {
    local name="$1" value="${2-}"
    wpi_require_set "$name" "$value"
    case "$value" in /*) : ;; *) wpi_stop RP7 "prereg_input_malformed name=$name expected=absolute_path" ;; esac
    case "$value" in *[![:print:]]*|*[[:space:]]*|*'//'*) wpi_stop RP7 "prereg_input_malformed name=$name expected=canonical_printable_path" ;; esac
    case "/$value/" in *'/../'*|*'/./'*) wpi_stop RP7 "prereg_input_malformed name=$name expected=no_dot_components" ;; esac
    [ "$value" = "/" ] || [ "${value%/}" = "$value" ] || wpi_stop RP7 "prereg_input_malformed name=$name expected=no_trailing_slash"
}

wpi_expect_literal() {
    local name="$1" observed="$2" expected="$3"
    [ "$observed" = "$expected" ] || wpi_stop RP7 "prereg_input_malformed name=$name expected=$expected"
}

wpi_require_observed_path_grammar() {
    local prefix="$1" path="$2" source="$3"
    case "$path" in
        /*) : ;;
        *) wpi_stop "$prefix" "structured_path_unparseable source=$source detail=not_absolute" ;;
    esac
    case "$path" in
        *[![:print:]]*|*[[:space:]]*) wpi_stop "$prefix" "structured_path_unparseable source=$source detail=unsafe_character" ;;
    esac
}

wpi_map_get() {
    local map="$1" wanted="$2" entry found=""
    for entry in $map; do
        case "$entry" in
            "$wanted"=*) [ -z "$found" ] || wpi_stop RP7 "prereg_input_malformed name=WPI_TOOL_PINS duplicate=$wanted"
                         found="${entry#*=}" ;;
        esac
    done
    [ -n "$found" ] || wpi_stop RP7 "prereg_input_missing name=WPI_TOOL_PINS.$wanted"
    WPI_LINE="$found"
}

wpi_clock_ms() {
    local line whole frac
    IFS= read -r line < /proc/uptime || wpi_stop RP7 "monotonic_clock_unreadable path=/proc/uptime"
    [[ "$line" =~ ^([0-9]+)\.([0-9]+)\ ([0-9]+)\.([0-9]+)$ ]] || wpi_stop RP7 "monotonic_clock_unparsable"
    whole="${BASH_REMATCH[1]}"; frac="${BASH_REMATCH[2]}"
    frac="${frac}000"; frac="${frac:0:3}"
    WPI_LINE=$(( 10#$whole * 1000 + 10#$frac ))
}

wpi_alloc_leaf() {
    local leaf="$1"
    case "$leaf" in "$EV_DIR"/*) : ;; *) wpi_stop RP7 "capture_path_outside_evidence leaf=$leaf ev_dir=$EV_DIR" ;; esac
    if ! ( set -o noclobber; : > "$leaf" ) 2>/dev/null; then
        wpi_stop RP7 "capture_leaf_not_create_once leaf=$leaf"
    fi
}

wpi_alloc_read_diag() {
    local label="$1"
    WPI_PROBE_SEQ=$(( WPI_PROBE_SEQ + 1 ))
    WPI_READ_DIAG="$EV_DIR/ro.$(printf '%04d' "$WPI_PROBE_SEQ").$label.read.stderr"
    wpi_alloc_leaf "$WPI_READ_DIAG"
}

# Run one evidence-producing child from EV_DIR, with a cleared environment,
# fixed locale/PATH/TMPDIR, absolute argv[0], and separate create-once streams.
wpi_capture() {
    local label="$1"; shift
    local start end rc=0
    WPI_PROBE_SEQ=$(( WPI_PROBE_SEQ + 1 ))
    WPI_CAP_OUT="$EV_DIR/ro.$(printf '%04d' "$WPI_PROBE_SEQ").$label.stdout"
    WPI_CAP_ERR="$EV_DIR/ro.$(printf '%04d' "$WPI_PROBE_SEQ").$label.stderr"
    wpi_alloc_leaf "$WPI_CAP_OUT"
    wpi_alloc_leaf "$WPI_CAP_ERR"
    wpi_clock_ms; start="$WPI_LINE"
    (
        cd "$EV_DIR" || exit 125
        exec "$WPI_ENV" -i LC_ALL=C PATH=/usr/bin:/bin HOME=/nonexistent TMPDIR="$EV_DIR" "$@"
    ) >"$WPI_CAP_OUT" 2>"$WPI_CAP_ERR" || rc=$?
    wpi_clock_ms; end="$WPI_LINE"
    WPI_CAP_RC="$rc"
    WPI_CAP_ELAPSED_MS=$(( end - start ))
    [ "$WPI_CAP_ELAPSED_MS" -ge 0 ] || wpi_stop RP7 "monotonic_clock_reversed label=$label"
}

wpi_require_empty_file() {
    local prefix="$1" reason="$2" file="$3"
    [ -r "$file" ] && [ -f "$file" ] || wpi_stop "$prefix" "$reason detail=diagnostic_stream_not_readable_regular"
    [ ! -s "$file" ] || wpi_stop "$prefix" "$reason detail=diagnostic_stream_nonempty diagnostic_file=$file"
}

# Builtin-only exact single-record reader. It opens once, accepts the first
# record only when newline-terminated, and requires clean EOF with no second
# populated record. The source is already a regular create-once evidence leaf.
wpi_single_record() {
    local prefix="$1" reason="$2" file="$3" fd first="" extra="" rc=0 diag
    wpi_alloc_read_diag single_record; diag="$WPI_READ_DIAG"
    exec {fd}<"$file" || wpi_stop "$prefix" "$reason detail=open_failed source=$file"
    IFS= read -r -u "$fd" first 2>>"$diag" || rc=$?
    if [ "$rc" -ne 0 ]; then
        exec {fd}<&-
        wpi_require_empty_file "$prefix" "$reason detail=hard_read_error source=$file" "$diag"
        [ -z "$first" ] && wpi_stop "$prefix" "$reason detail=empty_or_read_error source=$file read_rc=$rc"
        wpi_stop "$prefix" "$reason detail=unterminated_final_record source=$file read_rc=$rc"
    fi
    rc=0
    IFS= read -r -u "$fd" extra 2>>"$diag" || rc=$?
    exec {fd}<&-
    wpi_require_empty_file "$prefix" "$reason detail=hard_read_error source=$file" "$diag"
    [ "$rc" -ne 0 ] || wpi_stop "$prefix" "$reason detail=multiple_records source=$file"
    [ -z "$extra" ] || wpi_stop "$prefix" "$reason detail=unterminated_extra_record source=$file"
    WPI_LINE="$first"
}

wpi_lstat() {
    local prefix="$1" path="$2" raw rest
    wpi_capture lstat "$WPI_STAT" -c '%F|%a|%u:%g|%d:%i|%s' -- "$path"
    if [ "$WPI_CAP_RC" -ne 0 ]; then
        wpi_require_empty_file "$prefix" "path_not_evaluable path=$path rc=$WPI_CAP_RC" "$WPI_CAP_OUT"
        wpi_single_record "$prefix" "path_not_evaluable path=$path rc=$WPI_CAP_RC" "$WPI_CAP_ERR"
        case "$WPI_LINE" in
            "stat: cannot statx '$path': No such file or directory"|"stat: cannot stat '$path': No such file or directory")
                WPI_META_KIND=absent; WPI_META_MODE=""; WPI_META_OWNER=""; WPI_META_ID=""; WPI_META_SIZE=""; return 0 ;;
            *) wpi_stop "$prefix" "path_not_evaluable path=$path rc=$WPI_CAP_RC detail=unclassified_diagnostic diagnostic_file=$WPI_CAP_ERR" ;;
        esac
    fi
    wpi_require_empty_file "$prefix" "path_not_evaluable path=$path rc=0" "$WPI_CAP_ERR"
    wpi_single_record "$prefix" "path_not_evaluable path=$path rc=0" "$WPI_CAP_OUT"
    raw="$WPI_LINE"
    case "$raw" in *'|'*'|'*'|'*'|'*) : ;; *) wpi_stop "$prefix" "path_not_evaluable path=$path rc=0 detail=metadata_grammar" ;; esac
    WPI_META_KIND="${raw%%|*}"; rest="${raw#*|}"
    WPI_META_MODE="${rest%%|*}"; rest="${rest#*|}"
    WPI_META_OWNER="${rest%%|*}"; rest="${rest#*|}"
    WPI_META_ID="${rest%%|*}"; WPI_META_SIZE="${rest#*|}"
    case "$WPI_META_MODE" in ''|*[!0-7]*) wpi_stop "$prefix" "path_not_evaluable path=$path rc=0 detail=mode_grammar" ;; esac
    case "$WPI_META_OWNER" in *[!0-9:]*|*:*:*|:*|*:|'') wpi_stop "$prefix" "path_not_evaluable path=$path rc=0 detail=owner_grammar" ;; *:*) : ;; *) wpi_stop "$prefix" "path_not_evaluable path=$path rc=0 detail=owner_grammar" ;; esac
    case "$WPI_META_ID" in *[!0-9:]*|*:*:*|:*|*:|'') wpi_stop "$prefix" "path_not_evaluable path=$path rc=0 detail=object_id_grammar" ;; *:*) : ;; *) wpi_stop "$prefix" "path_not_evaluable path=$path rc=0 detail=object_id_grammar" ;; esac
    case "$WPI_META_SIZE" in ''|*[!0-9]*) wpi_stop "$prefix" "path_not_evaluable path=$path rc=0 detail=size_grammar" ;; esac
}

wpi_walk_components() {
    local prefix="$1" path="$2" leaf_kind="$3" leaf_mode="$4" leaf_owner="$5"
    local leaf_absent_reason="${6:-path_absent}" leaf_object_reason="${7:-path_metadata_mismatch}"
    local rest component current="" expected_kind expected_owner
    wpi_require_absolute path "$path"
    wpi_lstat "$prefix" /
    [ "$WPI_META_KIND" = directory ] || wpi_stop "$prefix" "path_not_evaluable path=/ detail=root_kind_$WPI_META_KIND"
    [ "$WPI_META_OWNER" = 0:0 ] || wpi_stop "$prefix" "path_not_evaluable path=/ owner_numeric=$WPI_META_OWNER expected=0:0"
    rest="${path#/}"
    IFS='/' read -r -a WPI_COMPONENTS <<< "$rest"
    [ "${#WPI_COMPONENTS[@]}" -ge 1 ] || wpi_stop "$prefix" "path_not_evaluable path=$path detail=no_components"
    for component in "${WPI_COMPONENTS[@]}"; do
        [ -n "$component" ] || wpi_stop "$prefix" "path_not_evaluable path=$path detail=empty_component"
        [ "$component" != "." ] && [ "$component" != ".." ] || wpi_stop "$prefix" "path_not_evaluable path=$path detail=dot_component"
        current="$current/$component"
        expected_kind="directory"; expected_owner="0:0"
        if [ "$current" = "$path" ]; then expected_kind="$leaf_kind"; expected_owner="$leaf_owner"; fi
        wpi_lstat "$prefix" "$current"
        if [ "$WPI_META_KIND" = absent ]; then
            if [ "$current" = "$path" ]; then wpi_fail "$prefix" "$leaf_absent_reason path=$current"
            else wpi_fail "$prefix" "path_absent path=$current"; fi
        fi
        case "$WPI_META_KIND" in
            'symbolic link')
                if [ "$current" = "$path" ]; then wpi_fail "$prefix" "$leaf_object_reason kind=symlink path=$current"
                else wpi_fail "$prefix" "path_metadata_mismatch path=$current kind=symlink expected=directory"; fi ;;
        esac
        case "$expected_kind:$WPI_META_KIND" in
            directory:directory|regular:'regular file'|regular:'regular empty file') : ;;
            *) if [ "$current" = "$path" ]; then wpi_fail "$prefix" "$leaf_object_reason kind=$WPI_META_KIND path=$current expected=$expected_kind"
               else wpi_fail "$prefix" "path_metadata_mismatch path=$current kind=$WPI_META_KIND expected=directory"; fi ;;
        esac
        [ "$WPI_META_OWNER" = "$expected_owner" ] || wpi_fail "$prefix" "path_metadata_mismatch path=$current owner_numeric=$WPI_META_OWNER expected_owner_numeric=$expected_owner"
        if [ "$current" = "$path" ] && [ -n "$leaf_mode" ]; then
            [ "$WPI_META_MODE" = "${leaf_mode#0}" ] || wpi_fail "$prefix" "path_metadata_mismatch path=$current mode=$WPI_META_MODE expected_mode=${leaf_mode#0}"
        fi
    done
}

wpi_parse_mountinfo() {
    local file="$1" fd line="" rc=0 records=0 pre post diag seen_ids=" "
    wpi_alloc_read_diag mount_table; diag="$WPI_READ_DIAG"
    exec {fd}<"$file" || wpi_stop RP7 "mount_table_unreadable path=$file detail=open_failed"
    while true; do
        line=""; rc=0; IFS= read -r -u "$fd" line 2>>"$diag" || rc=$?
        if [ "$rc" -ne 0 ]; then
            exec {fd}<&-
            wpi_require_empty_file RP7 "mount_table_read_error path=$file records=$records" "$diag"
            [ -z "$line" ] || wpi_stop RP7 "mount_table_unterminated_final_record path=$file records=$records"
            break
        fi
        [ -n "$line" ] || wpi_stop RP7 "mount_table_malformed path=$file record=$((records+1)) detail=blank"
        case "$line" in *' - '*) pre="${line%% - *}"; post="${line#* - }" ;; *) wpi_stop RP7 "mount_table_malformed path=$file record=$((records+1)) detail=separator" ;; esac
        set -- $pre
        [ "$#" -ge 6 ] || wpi_stop RP7 "mount_table_malformed path=$file record=$((records+1)) detail=pre_fields"
        case "$1" in ''|*[!0-9]*) wpi_stop RP7 "mount_table_malformed path=$file record=$((records+1)) detail=mount_id" ;; esac
        case "$2" in ''|*[!0-9]*) wpi_stop RP7 "mount_table_malformed path=$file record=$((records+1)) detail=parent_id" ;; esac
        case "$seen_ids" in *" $1 "*) wpi_stop RP7 "mount_table_malformed path=$file record=$((records+1)) detail=duplicate_mount_id" ;; esac
        seen_ids="$seen_ids$1 "
        [[ "$3" =~ ^[0-9]+:[0-9]+$ ]] || wpi_stop RP7 "mount_table_malformed path=$file record=$((records+1)) detail=device_id"
        case "$4:$5" in /*:/*) : ;; *) wpi_stop RP7 "mount_table_malformed path=$file record=$((records+1)) detail=root_or_mountpoint" ;; esac
        set -- $post
        [ "$#" -ge 3 ] || wpi_stop RP7 "mount_table_malformed path=$file record=$((records+1)) detail=post_fields"
        records=$(( records + 1 ))
    done
    [ "$records" -ge 1 ] || wpi_stop RP7 "mount_table_unreadable path=$file detail=no_records"
    printf 'RP7_mount_table parsed=yes records=%s content=not_printed\n' "$records"
}

wpi_sha_file() {
    local prefix="$1" reason="$2" path="$3" digest rendered
    wpi_capture sha256 "$WPI_SHA256SUM" -- "$path"
    [ "$WPI_CAP_RC" -eq 0 ] || wpi_stop "$prefix" "$reason path=$path rc=$WPI_CAP_RC detail=sha256sum_failed diagnostic_file=$WPI_CAP_ERR"
    wpi_require_empty_file "$prefix" "$reason path=$path rc=0" "$WPI_CAP_ERR"
    wpi_single_record "$prefix" "$reason path=$path rc=0" "$WPI_CAP_OUT"
    rendered="$WPI_LINE"; digest="${rendered%% *}"
    [ "${#digest}" -eq 64 ] || wpi_stop "$prefix" "$reason path=$path rc=0 detail=digest_grammar"
    case "$digest" in *[!0-9a-f]*) wpi_stop "$prefix" "$reason path=$path rc=0 detail=digest_grammar" ;; esac
    WPI_LINE="$digest"
}

wpi_mount_guard_begin() {
    wpi_parse_mountinfo /proc/self/mountinfo
    wpi_sha_file RP7 mount_table_unreadable /proc/self/mountinfo
    [ "$WPI_LINE" = "$WPI_ATTESTED_MOUNTINFO_SHA256" ] || wpi_stop RP7 "mount_topology_mismatch observed=$WPI_LINE attested=$WPI_ATTESTED_MOUNTINFO_SHA256"
    WPI_MOUNT_BEFORE="$WPI_LINE"
}

wpi_mount_guard_end() {
    wpi_sha_file RP7 mount_table_unreadable /proc/self/mountinfo
    [ "$WPI_LINE" = "$WPI_MOUNT_BEFORE" ] || wpi_stop RP7 "mount_topology_changed before=$WPI_MOUNT_BEFORE after=$WPI_LINE"
}

wpi_bind_tool() {
    local name="$1" path="$2"
    wpi_require_absolute "WPI_TOOL_PINS.$name" "$path"
    [ -x "$path" ] || wpi_stop RP7 "tool_not_evaluable tool=$name path=$path detail=not_executable"
    wpi_walk_components RP7 "$path" regular "" 0:0
    case "$WPI_META_MODE" in ???) : ;; *) wpi_stop RP7 "tool_not_evaluable tool=$name path=$path detail=mode_grammar" ;; esac
    [ $(( 8#$WPI_META_MODE & 8#022 )) -eq 0 ] || wpi_stop RP7 "tool_not_evaluable tool=$name path=$path mode=$WPI_META_MODE detail=group_or_world_writable"
    printf 'RP7_tool name=%s path=%s owner_numeric=0:0 mode=%s kind=regular resolution=pinned_absolute\n' "$name" "$path" "$WPI_META_MODE"
}

wpi_validate_inputs() {
    local fixed_sha="2ce41e34bceb599d80af24c5c33d835820ec321b"
    local name path entry pin_name pin_path pin_seen=" " pin_count=0
    for name in WPI_CANDIDATE_SHA WPI_RELEASE_ROOT WPI_VENV_ROOT WPI_UNIT_FRAGMENT \
        WPI_UNIT_FRAGMENT_BYTES WPI_UNIT_FRAGMENT_SHA256 WPI_EXPECTED_LOCK_SHA256 \
        WPI_EXPECTED_LOCK_BYTES WPI_EXPECTED_PACKAGES WPI_STATE_DIR WPI_STATE_UID \
        WPI_STATE_GID WPI_LOG_DIR WPI_CONF_DIR WPI_CONTROL_ENDPOINT WPI_SWEEP_BUDGET_S; do
        wpi_require_set "$name" "${!name-}"
    done
    wpi_expect_literal WPI_CANDIDATE_SHA "$WPI_CANDIDATE_SHA" "$fixed_sha"
    wpi_expect_literal WPI_RELEASE_ROOT "$WPI_RELEASE_ROOT" "/opt/mtc-bridge/releases/$fixed_sha"
    wpi_expect_literal WPI_VENV_ROOT "$WPI_VENV_ROOT" "/opt/mtc-bridge/venvs/$fixed_sha"
    wpi_expect_literal WPI_UNIT_FRAGMENT "$WPI_UNIT_FRAGMENT" /usr/local/lib/systemd/system/mtc-bridge-first-start.service
    wpi_expect_literal WPI_UNIT_FRAGMENT_BYTES "$WPI_UNIT_FRAGMENT_BYTES" 3736
    wpi_require_sha256 WPI_UNIT_FRAGMENT_SHA256 "$WPI_UNIT_FRAGMENT_SHA256"
    wpi_expect_literal WPI_EXPECTED_LOCK_SHA256 "$WPI_EXPECTED_LOCK_SHA256" a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e
    wpi_expect_literal WPI_EXPECTED_LOCK_BYTES "$WPI_EXPECTED_LOCK_BYTES" 117762
    wpi_expect_literal WPI_EXPECTED_PACKAGES "$WPI_EXPECTED_PACKAGES" 56
    wpi_expect_literal WPI_STATE_DIR "$WPI_STATE_DIR" /var/lib/mtc-bridge
    wpi_expect_literal WPI_STATE_UID "$WPI_STATE_UID" 999
    wpi_expect_literal WPI_STATE_GID "$WPI_STATE_GID" 988
    wpi_require_absolute WPI_LOG_DIR "$WPI_LOG_DIR"
    wpi_expect_literal WPI_CONF_DIR "$WPI_CONF_DIR" /etc/mtc-bridge
    wpi_expect_literal WPI_CONTROL_ENDPOINT "$WPI_CONTROL_ENDPOINT" http://127.0.0.1:8790/api/status
    wpi_expect_literal WPI_SWEEP_BUDGET_S "$WPI_SWEEP_BUDGET_S" 120

    wpi_require_set WPI_TOOL_PINS "${WPI_TOOL_PINS:-}"
    for entry in $WPI_TOOL_PINS; do
        case "$entry" in *=*) pin_name="${entry%%=*}"; pin_path="${entry#*=}" ;; *) wpi_stop RP7 "prereg_input_malformed name=WPI_TOOL_PINS entry=missing_equals" ;; esac
        case "$pin_name" in stat|readlink|env|find|sha256sum|systemctl|ss|curl) : ;; *) wpi_stop RP7 "prereg_input_malformed name=WPI_TOOL_PINS unknown_tool=$pin_name" ;; esac
        case "$pin_seen" in *" $pin_name "*) wpi_stop RP7 "prereg_input_malformed name=WPI_TOOL_PINS duplicate=$pin_name" ;; esac
        wpi_require_absolute "WPI_TOOL_PINS.$pin_name" "$pin_path"
        pin_seen="$pin_seen$pin_name "; pin_count=$(( pin_count + 1 ))
    done
    [ "$pin_count" -eq 8 ] || wpi_stop RP7 "prereg_input_malformed name=WPI_TOOL_PINS observed_count=$pin_count expected_count=8"
    for name in stat readlink env find sha256sum systemctl ss curl; do
        wpi_map_get "$WPI_TOOL_PINS" "$name"; path="$WPI_LINE"
        printf -v "WPI_${name^^}" '%s' "$path"
    done
    WPI_SHA256SUM="$WPI_SHA256SUM"
    wpi_require_sha256 WPI_ATTESTED_MOUNTINFO_SHA256 "${WPI_ATTESTED_MOUNTINFO_SHA256:-}"
    wpi_require_uint WPI_MAINPID "${WPI_MAINPID:-}" 2
    wpi_expect_literal WPI_MAINPID "$WPI_MAINPID" 189813
    wpi_require_absolute WPI_INTERPRETER_TARGET "${WPI_INTERPRETER_TARGET:-}"
    wpi_require_set WPI_VERIFY_LOCK_SHA256 "${WPI_VERIFY_LOCK_SHA256:-}"
    wpi_expect_literal WPI_VERIFY_LOCK_SHA256 "${WPI_VERIFY_LOCK_SHA256:-}" d951e0eea01ec1a89bcfbe9d9630949b31bb316faae2ba6bcae39be794a451e5
}

wpi_assert_prerequisites() {
    command -v rp0_require_safe_component >/dev/null 2>&1 || wpi_stop RP7 "rp0_lib_not_sourced predicate=rp0_require_safe_component"
    command -v rp0_allocate_evidence_dir >/dev/null 2>&1 || wpi_stop RP7 "rp0_lib_not_sourced predicate=rp0_allocate_evidence_dir"
    wpi_require_set RUNID "${RUNID:-}"; wpi_require_set EV_STAGE_ID "${EV_STAGE_ID:-}"
    wpi_require_set EV_DIR "${EV_DIR:-}"; wpi_require_set EV_LOG "${EV_LOG:-}"
    rp0_require_safe_component RUNID "$RUNID" || wpi_stop RP7 "evidence_identifier_refused name=RUNID"
    rp0_require_safe_component EV_STAGE_ID "$EV_STAGE_ID" || wpi_stop RP7 "evidence_identifier_refused name=EV_STAGE_ID"
    [ "$EV_STAGE_ID" = ro ] || wpi_stop RP7 "prereg_input_malformed name=EV_STAGE_ID expected=ro"
    case "$EV_LOG" in "$EV_DIR"/*) : ;; *) wpi_stop RP7 "evidence_leaf_not_bound ev_log=$EV_LOG ev_dir=$EV_DIR" ;; esac
}

wpi_assert_manager_ready() {
    wpi_capture system_manager "$WPI_SYSTEMCTL" --system --no-pager show --property=Version
    [ "$WPI_CAP_RC" -eq 0 ] || wpi_stop RP7 "system_manager_unreachable rc=$WPI_CAP_RC detail=manager_query_nonzero diagnostic_file=$WPI_CAP_ERR"
    wpi_require_empty_file RP7 "system_manager_unreachable rc=0" "$WPI_CAP_ERR"
    wpi_single_record RP7 "system_manager_unreachable rc=0" "$WPI_CAP_OUT"
    case "$WPI_LINE" in Version=?*) : ;; *) wpi_stop RP7 "system_manager_unreachable rc=0 detail=response_unparseable" ;; esac
    printf 'RP7_preflight system_manager=ready query=Manager.Version output=complete\n'
}

wpi_assert_evidence_leaf_bound() {
    local fdid logid rawpath
    exec 8>&1
    wpi_capture evidence_fd_path "$WPI_READLINK" -- /proc/self/fd/8
    [ "$WPI_CAP_RC" -eq 0 ] || { exec 8>&-; wpi_stop RP7 "evidence_binding_unprobeable subject=fd8 rc=$WPI_CAP_RC"; }
    wpi_require_empty_file RP7 "evidence_binding_unprobeable subject=fd8" "$WPI_CAP_ERR"
    wpi_single_record RP7 "evidence_binding_unprobeable subject=fd8" "$WPI_CAP_OUT"; rawpath="$WPI_LINE"
    wpi_capture evidence_fd_id "$WPI_STAT" -L -c '%d:%i' -- /proc/self/fd/8
    [ "$WPI_CAP_RC" -eq 0 ] || { exec 8>&-; wpi_stop RP7 "evidence_binding_unprobeable subject=fd8 rc=$WPI_CAP_RC"; }
    wpi_require_empty_file RP7 "evidence_binding_unprobeable subject=fd8" "$WPI_CAP_ERR"
    wpi_single_record RP7 "evidence_binding_unprobeable subject=fd8" "$WPI_CAP_OUT"; fdid="$WPI_LINE"
    wpi_capture evidence_log_id "$WPI_STAT" -c '%d:%i' -- "$EV_LOG"
    [ "$WPI_CAP_RC" -eq 0 ] || { exec 8>&-; wpi_stop RP7 "evidence_binding_unprobeable subject=ev_log rc=$WPI_CAP_RC"; }
    wpi_require_empty_file RP7 "evidence_binding_unprobeable subject=ev_log" "$WPI_CAP_ERR"
    wpi_single_record RP7 "evidence_binding_unprobeable subject=ev_log" "$WPI_CAP_OUT"; logid="$WPI_LINE"
    exec 8>&-
    case "$fdid" in *[!0-9:]*|*:*:*|:*|*:|'') wpi_stop RP7 "evidence_binding_unparsable subject=fd8" ;; *:*) : ;; *) wpi_stop RP7 "evidence_binding_unparsable subject=fd8" ;; esac
    case "$logid" in *[!0-9:]*|*:*:*|:*|*:|'') wpi_stop RP7 "evidence_binding_unparsable subject=ev_log" ;; *:*) : ;; *) wpi_stop RP7 "evidence_binding_unparsable subject=ev_log" ;; esac
    [ "$fdid" = "$logid" ] || wpi_stop RP7 "evidence_leaf_not_bound ev_log=$EV_LOG ev_log_id=$logid stdout_id=$fdid"
    wpi_sanitize "$rawpath"
    printf 'RP7_evidence_bound leaf=%s object_id=%s stdout_path=[%s] mechanism=dev_inode_identity\n' "$EV_LOG" "$logid" "$WPI_SAFE"
}

wpi_run_find() {
    local prefix="$1" label="$2" root="$3"; shift 3
    wpi_capture "$label" "$WPI_FIND" "$root" "$@"
    if [ "$WPI_CAP_ELAPSED_MS" -gt $(( WPI_SWEEP_BUDGET_S * 1000 )) ]; then
        wpi_stop "$prefix" "sweep_budget_exceeded root=$root elapsed_ms=$WPI_CAP_ELAPSED_MS budget_s=$WPI_SWEEP_BUDGET_S"
    fi
    if [ "$WPI_CAP_RC" -ne 0 ]; then
        wpi_stop "$prefix" "walk_incomplete root=$root rc=$WPI_CAP_RC detail=diagnostic_captured diagnostic_file=$WPI_CAP_ERR partial_stdout_discarded=$WPI_CAP_OUT"
    fi
    wpi_require_empty_file "$prefix" "walk_incomplete root=$root rc=0" "$WPI_CAP_ERR"
}

wpi_assert_tree() {
    local root="$1" label="$2" out fd path="" rc=0 writable_count=0 find_elapsed
    local diag
    wpi_mount_guard_begin
    wpi_walk_components B3 "$root" directory 0555 0:0
    printf 'B3_path path=%s kind=directory mode=555 owner_numeric=0:0 binding=component_and_mount\n' "$root"
    wpi_run_find B3 "${label}_writable" "$root" -perm /222 -print0
    out="$WPI_CAP_OUT"; find_elapsed="$WPI_CAP_ELAPSED_MS"
    [ -r "$out" ] && [ -f "$out" ] || wpi_stop B3 "walk_incomplete root=$root detail=stdout_not_readable_regular"
    if [ -s "$out" ]; then
        wpi_alloc_read_diag writable_paths; diag="$WPI_READ_DIAG"
        exec {fd}<"$out" || wpi_stop B3 "walk_incomplete root=$root detail=stdout_open_failed"
        while true; do
            path=""; rc=0; IFS= read -r -d '' -u "$fd" path 2>>"$diag" || rc=$?
            if [ "$rc" -ne 0 ]; then
                exec {fd}<&-
                wpi_require_empty_file B3 "walk_incomplete root=$root detail=stdout_read_error" "$diag"
                [ -z "$path" ] || wpi_stop B3 "walk_incomplete root=$root detail=unterminated_nul_record"
                break
            fi
            wpi_require_observed_path_grammar B3 "$path" find_stdout
            writable_count=$(( writable_count + 1 ))
            [ "$writable_count" -eq 1 ] || continue
            WPI_FIRST_WRITABLE="$path"
        done
        [ "$writable_count" -ge 1 ] || wpi_stop B3 "walk_incomplete root=$root detail=nonempty_unparseable_stdout"
        wpi_fail B3 "writable_path_inside_immutable_tree path=$WPI_FIRST_WRITABLE"
    fi
    wpi_mount_guard_end
    printf 'B3_sweep root=%s complete=yes elapsed_ms=%s writable_paths=0\n' "$root" "$find_elapsed"
    if [ "$label" = venv ]; then WPI_VENV_WALK_COMPLETE=yes; fi
    return 0
}

wpi_assert_metadata_dir() {
    local path="$1" owner="$2"
    wpi_mount_guard_begin
    wpi_walk_components B3 "$path" directory 0750 "$owner"
    wpi_mount_guard_end
    printf 'B3_metadata_dir path=%s kind=directory mode=750 owner_numeric=%s binding=component_and_mount\n' "$path" "$owner"
}

wpi_assert_regular_digest() {
    local prefix="$1" absent_reason="$2" mismatch_reason="$3" path="$4" bytes="$5" digest="$6" label="$7" object_reason="${8:-path_metadata_mismatch}" observed_size
    wpi_mount_guard_begin
    wpi_walk_components "$prefix" "$path" regular "" 0:0 "$absent_reason" "$object_reason"
    observed_size="$WPI_META_SIZE"
    wpi_sha_file "$prefix" "${label}_unreadable" "$path"
    WPI_OBSERVED_DIGEST="$WPI_LINE"
    wpi_mount_guard_end
    [ "$observed_size" = "$bytes" ] || wpi_fail "$prefix" "$mismatch_reason observed_bytes=$observed_size expected_bytes=$bytes"
    [ "$WPI_OBSERVED_DIGEST" = "$digest" ] || wpi_fail "$prefix" "$mismatch_reason observed=$WPI_OBSERVED_DIGEST expected=$digest"
    printf '%s_digest path=%s bytes=%s sha256=%s binding=component_and_mount\n' "$prefix" "$path" "$observed_size" "$WPI_OBSERVED_DIGEST"
}

wpi_assert_interpreter() {
    local py="$WPI_VENV_ROOT/bin/python" resolved kind
    wpi_mount_guard_begin
    wpi_walk_components B1 "$WPI_VENV_ROOT/bin" directory "" 0:0
    wpi_lstat B1 "$py"
    [ "$WPI_META_KIND" != absent ] || wpi_fail B1 "interpreter_absent path=$py"
    case "$WPI_META_KIND" in
        'symbolic link')
            [ "$WPI_META_OWNER" = 0:0 ] || wpi_stop B1 "interpreter_object_unbound kind=symlink owner_numeric=$WPI_META_OWNER expected=0:0"
            wpi_capture interpreter_target "$WPI_READLINK" -f -- "$py"
            [ "$WPI_CAP_RC" -eq 0 ] || wpi_stop B1 "interpreter_object_unbound kind=symlink target=unreadable"
            wpi_require_empty_file B1 "interpreter_object_unbound kind=symlink" "$WPI_CAP_ERR"
            wpi_single_record B1 "interpreter_object_unbound kind=symlink" "$WPI_CAP_OUT"; resolved="$WPI_LINE"
            [ "$resolved" = "$WPI_INTERPRETER_TARGET" ] || wpi_stop B1 "interpreter_object_unbound kind=symlink target=$resolved"
            wpi_walk_components B1 "$resolved" regular "" 0:0 ;;
        'regular file'|'regular empty file')
            [ "$WPI_META_OWNER" = 0:0 ] || wpi_stop B1 "interpreter_object_unbound kind=regular owner_numeric=$WPI_META_OWNER expected=0:0"
            [ "$py" = "$WPI_INTERPRETER_TARGET" ] || wpi_stop B1 "interpreter_object_unbound kind=regular target=$py expected=$WPI_INTERPRETER_TARGET" ;;
        *) wpi_stop B1 "interpreter_object_unbound kind=$WPI_META_KIND target=none" ;;
    esac
    [ -x "$py" ] || wpi_stop B1 "interpreter_not_executable path=$py mechanism=access_builtin_x"
    wpi_mount_guard_end
    wpi_capture interpreter_version "$py" -I -V
    case "$WPI_CAP_RC" in
        0) : ;;
        126) wpi_stop B1 "interpreter_not_executable path=$py rc=126" ;;
        *) wpi_stop B1 "interpreter_not_executable path=$py rc=$WPI_CAP_RC" ;;
    esac
    # Python -V may use stdout or stderr, but exactly one complete stream must
    # carry the single record.
    local out_size err_size version_file
    [ -r "$WPI_CAP_OUT" ] && [ -f "$WPI_CAP_OUT" ] || wpi_stop B1 "interpreter_not_executable path=$py detail=stdout_unreadable"
    [ -r "$WPI_CAP_ERR" ] && [ -f "$WPI_CAP_ERR" ] || wpi_stop B1 "interpreter_not_executable path=$py detail=stderr_unreadable"
    if [ -s "$WPI_CAP_OUT" ] && [ ! -s "$WPI_CAP_ERR" ]; then version_file="$WPI_CAP_OUT"
    elif [ -s "$WPI_CAP_ERR" ] && [ ! -s "$WPI_CAP_OUT" ]; then version_file="$WPI_CAP_ERR"
    else wpi_stop B1 "interpreter_not_executable path=$py detail=version_stream_ambiguity"; fi
    wpi_single_record B1 "interpreter_not_executable path=$py" "$version_file"
    [[ "$WPI_LINE" =~ ^Python\ 3\.12\.[0-9]+$ ]] || wpi_fail B1 "interpreter_version observed=unpreregistered_version expected=3.12.*"
    WPI_INTERPRETER_RAN=yes
    printf 'B1_interpreter path=%s target=%s exec=ok version_family=3.12 env=cleared isolated=yes\n' "$py" "$WPI_INTERPRETER_TARGET"
}

wpi_assert_metadata_readable() {
    local site="$WPI_VENV_ROOT/lib/python3.12/site-packages" out fd path="" rc=0 count=0 member diag
    [ "$WPI_VENV_WALK_COMPLETE" = yes ] || wpi_stop B1 "verifier_not_evaluable rc=3 detail=venv_walk_not_complete"
    [ "$WPI_INTERPRETER_RAN" = yes ] || wpi_stop B1 "verifier_not_evaluable rc=3 detail=interpreter_not_run"
    wpi_mount_guard_begin
    wpi_walk_components B1 "$site" directory "" 0:0
    wpi_run_find B1 metadata_enumeration "$site" -mindepth 1 -maxdepth 1 -name '*.dist-info' -print0
    out="$WPI_CAP_OUT"
    wpi_alloc_read_diag metadata_paths; diag="$WPI_READ_DIAG"
    exec {fd}<"$out" || wpi_stop B1 "metadata_unreadable path=$site detail=enumeration_open_failed"
    while true; do
        path=""; rc=0; IFS= read -r -d '' -u "$fd" path 2>>"$diag" || rc=$?
        if [ "$rc" -ne 0 ]; then
            exec {fd}<&-
            wpi_require_empty_file B1 "metadata_unreadable path=$site detail=enumeration_read_error" "$diag"
            [ -z "$path" ] || wpi_stop B1 "metadata_unreadable path=$site detail=unterminated_nul_record"
            break
        fi
        count=$(( count + 1 ))
        wpi_require_observed_path_grammar B1 "$path" metadata_enumeration
        wpi_lstat B1 "$path"
        [ "$WPI_META_KIND" != absent ] || wpi_stop B1 "metadata_unreadable path=$path detail=object_disappeared_after_complete_enumeration"
        [ "$WPI_META_KIND" = directory ] || wpi_stop B1 "metadata_unreadable path=$path detail=dist_info_kind_$WPI_META_KIND"
        [ "$WPI_META_OWNER" = 0:0 ] || wpi_stop B1 "metadata_unreadable path=$path owner_numeric=$WPI_META_OWNER expected=0:0"
        wpi_walk_components B1 "$path" directory "" 0:0
        for member in METADATA RECORD; do
            wpi_lstat B1 "$path/$member"
            [ "$WPI_META_KIND" != absent ] || wpi_fail B1 "distribution_metadata_absent path=$path/$member"
            case "$WPI_META_KIND" in 'regular file'|'regular empty file') : ;; *) wpi_stop B1 "metadata_unreadable path=$path/$member detail=kind_$WPI_META_KIND" ;; esac
            [ "$WPI_META_OWNER" = 0:0 ] || wpi_stop B1 "metadata_unreadable path=$path/$member owner_numeric=$WPI_META_OWNER expected=0:0"
            wpi_sha_file B1 metadata_unreadable "$path/$member"
            printf 'B1_metadata_readable path=%s bytes_digest=sha256:%s content=not_printed\n' "$path/$member" "$WPI_LINE"
        done
    done
    wpi_mount_guard_end
    [ "$count" -ge 1 ] || wpi_stop B1 "metadata_unreadable path=$site detail=no_dist_info_directories"
    WPI_METADATA_READABLE=yes
    printf 'B1_metadata_preflight root=%s dist_info_dirs=%s complete=yes readable=yes\n' "$site" "$count"
}

wpi_validate_package_list() {
    local value="$1"
    case "$value" in ''|,*|*,|*',,'*|*[!a-z0-9._,-]*) return 1 ;; esac
    return 0
}

wpi_is_structured_parity_mismatch() {
    local line="$1" detail missing extras
    case "$line" in 'verify_lock: FAIL: '*) detail="${line#verify_lock: FAIL: }" ;; *) return 1 ;; esac
    case "$detail" in
        'missing-or-wrong='*'; unexpected='*)
            missing="${detail#missing-or-wrong=}"; missing="${missing%%; unexpected=*}"
            extras="${detail#*; unexpected=}"
            wpi_validate_package_list "$missing" && wpi_validate_package_list "$extras" || return 1 ;;
        'missing-or-wrong='*)
            missing="${detail#missing-or-wrong=}"
            wpi_validate_package_list "$missing" || return 1 ;;
        'unexpected='*)
            extras="${detail#unexpected=}"
            wpi_validate_package_list "$extras" || return 1 ;;
        *) return 1 ;;
    esac
    return 0
}

wpi_assert_lock_parity() {
    local verifier="$WPI_RELEASE_ROOT/IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py"
    local lock="$WPI_RELEASE_ROOT/IBKR_PAPER_BRIDGE/requirements.lock" out err
    [ "$WPI_METADATA_READABLE" = yes ] || wpi_stop B1 "verifier_not_evaluable rc=3 detail=metadata_preflight_not_complete"
    wpi_assert_regular_digest B1 verifier_absent verifier_digest_mismatch "$verifier" 3735 "$WPI_VERIFY_LOCK_SHA256" verifier verifier_object_unexpected
    wpi_capture lock_parity "$WPI_VENV_ROOT/bin/python" -I "$verifier" --lock "$lock" --check-installed
    if [ "$WPI_CAP_RC" -eq 0 ]; then
        wpi_require_empty_file B1 "verifier_not_evaluable rc=0" "$WPI_CAP_ERR"
        wpi_single_record B1 "verifier_not_evaluable rc=0" "$WPI_CAP_OUT"
        [ "$WPI_LINE" = "verify_lock: PASS: lock+installed; packages=$WPI_EXPECTED_PACKAGES" ] \
            || wpi_stop B1 "verifier_not_evaluable rc=0 detail=pass_grammar"
        printf 'B1_lock_parity result=pass packages=%s output=structurally_parsed\n' "$WPI_EXPECTED_PACKAGES"
        return 0
    fi
    wpi_require_empty_file B1 "verifier_not_evaluable rc=$WPI_CAP_RC detail=unexpected_stdout" "$WPI_CAP_OUT"
    wpi_single_record B1 "verifier_not_evaluable rc=$WPI_CAP_RC" "$WPI_CAP_ERR"
    err="$WPI_LINE"
    if [ "$WPI_CAP_RC" -eq 1 ] && wpi_is_structured_parity_mismatch "$err"; then
        wpi_fail B1 "lock_installed_parity observed=positively_distinguished_named_set_mismatch"
    fi
    wpi_stop B1 "verifier_not_evaluable rc=$WPI_CAP_RC detail=unclassified_verifier_result diagnostic_file=$WPI_CAP_ERR"
}

wpi_assert_netns_binding() {
    local caller service service_path="/proc/$WPI_MAINPID/ns/net"
    wpi_capture caller_netns "$WPI_READLINK" -- /proc/self/ns/net
    [ "$WPI_CAP_RC" -eq 0 ] || wpi_stop B6 "service_netns_unreadable path=/proc/self/ns/net rc=$WPI_CAP_RC"
    wpi_require_empty_file B6 "service_netns_unreadable path=/proc/self/ns/net rc=0" "$WPI_CAP_ERR"
    wpi_single_record B6 "service_netns_unreadable path=/proc/self/ns/net rc=0" "$WPI_CAP_OUT"; caller="$WPI_LINE"
    wpi_capture service_netns "$WPI_READLINK" -- "$service_path"
    [ "$WPI_CAP_RC" -eq 0 ] || wpi_stop B6 "service_netns_unreadable path=$service_path rc=$WPI_CAP_RC"
    wpi_require_empty_file B6 "service_netns_unreadable path=$service_path rc=0" "$WPI_CAP_ERR"
    wpi_single_record B6 "service_netns_unreadable path=$service_path rc=0" "$WPI_CAP_OUT"; service="$WPI_LINE"
    [[ "$caller" =~ ^net:\[[0-9]+\]$ ]] || wpi_stop B6 "service_netns_unreadable path=/proc/self/ns/net rc=0 detail=identity_grammar"
    [[ "$service" =~ ^net:\[[0-9]+\]$ ]] || wpi_stop B6 "service_netns_unreadable path=$service_path rc=0 detail=identity_grammar"
    [ "$caller" = "$service" ] || wpi_stop B6 "netns_mismatch caller=$caller service=$service"
    printf 'B6_netns caller=%s service=%s mainpid=%s binding=equal\n' "$caller" "$service" "$WPI_MAINPID"
}

wpi_assert_listener_set() {
    local fd line="" rc=0 count=0 state recvq sendq localaddr peer extra addr diag
    wpi_capture listeners "$WPI_SS" -H -ltn 'sport = :8790'
    [ "$WPI_CAP_RC" -eq 0 ] || wpi_stop B6 "listener_inventory_unreadable_or_unparseable rc=$WPI_CAP_RC detail=ss_failed"
    wpi_require_empty_file B6 "listener_inventory_unreadable_or_unparseable rc=0" "$WPI_CAP_ERR"
    wpi_alloc_read_diag listener_rows; diag="$WPI_READ_DIAG"
    exec {fd}<"$WPI_CAP_OUT" || wpi_stop B6 "listener_inventory_unreadable_or_unparseable rc=0 detail=open_failed"
    while true; do
        line=""; rc=0; IFS= read -r -u "$fd" line 2>>"$diag" || rc=$?
        if [ "$rc" -ne 0 ]; then
            exec {fd}<&-
            wpi_require_empty_file B6 "listener_inventory_unreadable_or_unparseable rc=0 detail=hard_read_error" "$diag"
            [ -z "$line" ] || wpi_stop B6 "listener_inventory_unreadable_or_unparseable rc=0 detail=unterminated_final_record"
            break
        fi
        [ -n "$line" ] || wpi_stop B6 "listener_inventory_unreadable_or_unparseable rc=0 detail=blank_record"
        state=""; recvq=""; sendq=""; localaddr=""; peer=""; extra=""
        read -r state recvq sendq localaddr peer extra <<< "$line"
        [ -n "$state" ] && [ -n "$recvq" ] && [ -n "$sendq" ] && [ -n "$localaddr" ] && [ -n "$peer" ] && [ -z "$extra" ] \
            || wpi_stop B6 "listener_inventory_unreadable_or_unparseable rc=0 detail=table_grammar"
        [ "$state" = LISTEN ] || wpi_stop B6 "listener_inventory_unreadable_or_unparseable rc=0 detail=state_grammar"
        case "$recvq:$sendq" in *[!0-9:]*) wpi_stop B6 "listener_inventory_unreadable_or_unparseable rc=0 detail=queue_grammar" ;; esac
        case "$localaddr" in *:8790) addr="${localaddr%:8790}" ;; *) wpi_stop B6 "listener_inventory_unreadable_or_unparseable rc=0 detail=local_address_grammar" ;; esac
        case "$addr" in '*'|0.0.0.0|'[::]'|'::'|"172.24.55.233") wpi_fail B6 "nonloopback_listener addr=$addr" ;; esac
        [ "$addr" = 127.0.0.1 ] || wpi_fail B6 "listener_set_unexpected observed=non_preregistered_address expected=1x127.0.0.1:8790"
        count=$(( count + 1 ))
    done
    [ "$count" -eq 1 ] || wpi_fail B6 "listener_set_unexpected observed_count=$count expected=1x127.0.0.1:8790"
    printf 'B6_listener_set port=8790 count=1 local=127.0.0.1 wildcard=none table=complete\n'
}

wpi_assert_status() {
    local body="$EV_DIR/ro.status.body" code_file json_out json_err
    wpi_alloc_leaf "$body"
    wpi_capture status_get "$WPI_CURL" --silent --show-error --connect-timeout 5 --max-time 10 \
        --request GET --output "$body" --write-out '%{http_code}\n' -- "$WPI_CONTROL_ENDPOINT"
    [ "$WPI_CAP_RC" -eq 0 ] || wpi_stop B5 "status_endpoint_not_evaluable rc=$WPI_CAP_RC detail=transport_error diagnostic_file=$WPI_CAP_ERR"
    wpi_require_empty_file B5 "status_endpoint_not_evaluable rc=0" "$WPI_CAP_ERR"
    wpi_single_record B5 "status_endpoint_not_evaluable rc=0" "$WPI_CAP_OUT"
    case "$WPI_LINE" in 401|403) wpi_stop B5 "status_endpoint_access_denied code=$WPI_LINE" ;; 200) : ;; [0-9][0-9][0-9]) wpi_fail B5 "status_endpoint_unexpected_http code=$WPI_LINE" ;; *) wpi_stop B5 "status_endpoint_not_evaluable rc=0 detail=http_code_grammar" ;; esac
    wpi_sha_file B5 status_body_unreadable_or_unparseable "$body"; WPI_BODY_SHA="$WPI_LINE"
    wpi_capture status_json "$WPI_VENV_ROOT/bin/python" -I -c '
import hashlib,json,sys
class Dup(Exception): pass
def pairs(xs):
 d={}
 for k,v in xs:
  if k in d: raise Dup(k)
  d[k]=v
 return d
def bad_constant(x): raise ValueError("non_json_constant")
try:
 with open(sys.argv[1],"rb") as f: raw=f.read()
 obj=json.loads(raw.decode("utf-8"),object_pairs_hook=pairs,parse_constant=bad_constant)
 if type(obj) is not dict: print("PARSE top_level"); sys.exit(3)
 expected={"state":(str,"DISARMED"),"state_version":(int,1),"mode":(str,"credential_free_disarmed"),"network":(str,"disabled"),"exchange_conn":(str,"disabled"),"exchange_enabled":(bool,False),"credential_lookup":(str,"disabled"),"arm_enabled":(bool,False)}
 for k,(t,v) in expected.items():
  if k not in obj: print("MISSING "+k); sys.exit(4)
  if type(obj[k]) is not t: print("TYPE "+k); sys.exit(5)
  if obj[k] != v:
   h=hashlib.sha256(json.dumps(obj[k],sort_keys=True,separators=(",",":"),ensure_ascii=True).encode()).hexdigest()
   print("MISMATCH %s %s"%(k,h)); sys.exit(1)
 print("OK fields=8")
except (OSError,UnicodeError,json.JSONDecodeError,Dup,ValueError) as e:
 print("PARSE "+type(e).__name__); sys.exit(3)
' "$body"
    wpi_require_empty_file B5 "status_body_unreadable_or_unparseable detail=parser_stderr" "$WPI_CAP_ERR"
    wpi_single_record B5 "status_body_unreadable_or_unparseable" "$WPI_CAP_OUT"
    case "$WPI_CAP_RC:$WPI_LINE" in
        '0:OK fields=8') printf 'B5_status http=200 json=strict required_fields=8 flags=expected body_sha256=%s content=not_printed\n' "$WPI_BODY_SHA" ;;
        4:'MISSING '*) wpi_stop B5 "schema_unexpected field=${WPI_LINE#MISSING }" ;;
        5:'TYPE '*) wpi_stop B5 "schema_unexpected field=${WPI_LINE#TYPE } detail=type" ;;
        1:'MISMATCH '*)
            read -r _ WPI_JSON_FIELD WPI_JSON_DIGEST <<< "$WPI_LINE"
            case "$WPI_JSON_FIELD:$WPI_JSON_DIGEST" in *[!A-Za-z0-9_:.-]*) wpi_stop B5 "status_body_unreadable_or_unparseable detail=mismatch_grammar" ;; esac
            wpi_fail B5 "flag_mismatch field=$WPI_JSON_FIELD observed_sha256=$WPI_JSON_DIGEST expected=preregistered_typed_value" ;;
        *) wpi_stop B5 "status_body_unreadable_or_unparseable detail=strict_json_or_parser_failure parser_rc=$WPI_CAP_RC body_sha256=$WPI_BODY_SHA" ;;
    esac
}

wpi_record_external_probe_boundary() {
    # Row 24 is operation 06, deliberately after this remote stage. Running it
    # here would answer from the service host, not the operator network domain.
    printf 'B6_external row=24 executor=operator_side op=06 evaluated_by_RP7=no reason=network_domain_separation\n'
}

wpi_main() {
    printf 'RP7_SECTION header candidate=2ce41e34bceb599d80af24c5c33d835820ec321b block=RP7-WPI-RO stage=ro\n'
    wpi_assert_prerequisites
    wpi_validate_inputs

    # Bootstrap the tool table from the preregistered stat/env paths, then bind
    # every helper before its first evidence-producing use.
    for wpi_tool in stat readlink env find sha256sum systemctl ss curl; do
        wpi_map_get "$WPI_TOOL_PINS" "$wpi_tool"
        wpi_bind_tool "$wpi_tool" "$WPI_LINE"
    done

    wpi_assert_evidence_leaf_bound

    # STOP-first preflight: no filesystem, parity, curl, or ss comparison is
    # reachable until the intended system manager has answered.
    wpi_assert_manager_ready

    printf 'RP7_SECTION B3_rows_10_15\n'
    wpi_assert_tree "$WPI_RELEASE_ROOT" release
    wpi_assert_tree "$WPI_VENV_ROOT" venv
    wpi_assert_metadata_dir "$WPI_CONF_DIR" 0:0
    wpi_assert_metadata_dir "$WPI_STATE_DIR" "$WPI_STATE_UID:$WPI_STATE_GID"
    wpi_assert_metadata_dir "$WPI_LOG_DIR" "$WPI_STATE_UID:$WPI_STATE_GID"

    printf 'RP7_SECTION B1a_row_17\n'
    wpi_assert_regular_digest B1a installed_lock_absent installed_lock_digest_mismatch \
        "$WPI_RELEASE_ROOT/IBKR_PAPER_BRIDGE/requirements.lock" \
        "$WPI_EXPECTED_LOCK_BYTES" "$WPI_EXPECTED_LOCK_SHA256" installed_lock installed_lock_object_unexpected

    printf 'RP7_SECTION B1_rows_18_19\n'
    wpi_assert_interpreter
    wpi_assert_metadata_readable
    wpi_assert_lock_parity

    printf 'RP7_SECTION B5_B6_rows_20_24\n'
    # Binding order is intentional: row 22 preflight precedes every curl/ss
    # interpretation even though its display number is later.
    wpi_assert_netns_binding
    wpi_assert_listener_set
    wpi_assert_status
    wpi_record_external_probe_boundary

    printf 'RP7_claim establishes=rows_10_23_read_only_predicates_in_attested_mount_and_service_network_domains\n'
    printf 'RP7_claim does_not_establish=row_24_operator_side_result,ACL_or_capability_immutability,whole_tree_byte_identity,root_deferred_checks,group_C,host_authority\n'
    printf 'RP7 PASS\n'
}

wpi_main "$@"
