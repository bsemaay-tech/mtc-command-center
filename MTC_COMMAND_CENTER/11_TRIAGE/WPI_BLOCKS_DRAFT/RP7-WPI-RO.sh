#!/usr/bin/env bash
# ===== BLOCK-ID: RP7-WPI-RO ===== [EXECUTABLE PROPOSAL BLOCK]
# WP-I read-only rows 10-24 (PROPOSED DESIGN, DRAFT).
# Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b.
#
# AUTHORITY: authoring only. These bytes grant no host contact, transport,
# RUNID, budget, service, credential, trading, or deployment authority.
#
# Runtime mutation is confined to create-once capture leaves inside EV_DIR,
# which RP0-BOOTSTRAP allocated before this block. EV_DIR is itself proven, at
# the first predicate and before any leaf is allocated, to be a strict
# descendant of the frozen evidence root below <REMOTE_BASE>; every leaf is then
# proven to be inside EV_DIR. No host object outside that tree is changed, and
# no path outside it is opened for writing - including /dev/null.
# Every shell-side write goes to a descriptor returned by the O_CREAT|O_EXCL
# open that created the leaf, and never to a re-resolved name: `noclobber`
# proves only that the name did not exist at allocation, which is not the same
# fact as "the object written is the object allocated". The one write this
# block cannot bind that way is curl's `--output <path>` for the status body,
# because curl is given a name, not a descriptor; that leaf is create-once
# allocated and re-opened by name by curl. On the READ side, the one reader
# whose bytes a preregistered row claims identity for - the row-22 listener
# inventory - reads through a descriptor re-derived from the capture's own
# descriptor rather than from the leaf name, so the byte string adjudicated is
# the byte string the child wrote into the object the create-once open created.
# Every other reader opens by name and claims nothing beyond what its record
# grammar establishes; no row states captured/adjudicated identity for those.
# Both residuals are stated in SELF_QA_RP7.md rather than covered by the
# sentence above.
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
set -f
export LC_ALL=C

WPI_SAFE=""
WPI_LINE=""
WPI_CAP_OUT=""
WPI_CAP_ERR=""
WPI_CAP_OUT_FD=""
WPI_CAP_RC=0
WPI_CAP_ELAPSED_MS=0
WPI_READ_DIAG=""
WPI_READ_DIAG_FD=""
WPI_LEAF_FD=""
WPI_EP_ADDR=""
WPI_EP_PORT=""
WPI_META_KIND=""
WPI_META_MODE=""
WPI_META_OWNER=""
WPI_META_ID=""
WPI_META_SIZE=""
WPI_PROBE_SEQ=0
WPI_MOUNT_BEFORE=""
WPI_MOUNT_GUARD_ACTIVE=no
WPI_PATH_FIELD=""
WPI_PATH_RENDERABLE=yes
WPI_MOUNT_SNAPSHOT_SEQ=0
WPI_FIXED_ATTESTED_MOUNT_PROJECTION_SHA256='<PIN-AT-FREEZE>'
# The trusted adjudicating interpreter. Neither accepting adjudicator (the status
# JSON parser, the lock-parity verifier) may run under the venv being judged: on
# the target Python 3.12, -I implies -E/-P/-s but NOT -S, so site still imports and
# an executable line in <venv>/lib/python3.12/site-packages/*.pth, or a
# sitecustomize/usercustomize module in that same tree, runs with this process's
# authority before the intended child body. Both adjudicators therefore run under
# this pinned system interpreter with -I -S. /usr/bin/python3 is a symlink on the
# target family and no symlinked object is admissible as a bound tool, so the
# resolved non-symlink leaf is a freeze-gate input, exactly like the mount
# attestation below it.
WPI_FIXED_TRUSTED_PYTHON='<PIN-AT-FREEZE>'
# The only tree this block may write into. RP0-BOOTSTRAP allocates EV_DIR as
# <REMOTE_BASE>/evidence/runkit/<RUNID>, and the block proved EV_LOG below EV_DIR
# and every capture leaf below EV_DIR - but nothing proved EV_DIR itself descends
# from the run's own base, so the whole create-once chain hung from an unattested
# root supplied by the same channel it was meant to bound. The frozen prefix below
# closes that, and is a freeze-gate input exactly like the two pins above it:
# <REMOTE_BASE> is allocated, so Stage 1 must allocate it BEFORE it freezes these
# bytes. Until the pin is filled the block STOPs rather than claiming provenance.
WPI_FIXED_EVIDENCE_ROOT='<PIN-AT-FREEZE>'
WPI_VENV_WALK_COMPLETE=no
WPI_INTERPRETER_RAN=no
WPI_METADATA_READABLE=no
# The row-21 response schema, declared exactly once. The parent needs it to
# decide whether a result record its own child could have produced is being
# adjudicated, and the child needs it to answer at all; declaring it twice would
# let the two drift, so it is passed to the child as argv[2] and the child
# refuses to answer unless its own table is equal to it (pattern 11). Round 5's
# parent checked only that the record contained no disallowed characters, so a
# truncated `TYPE state str` - a record naming no expected type, which the child
# cannot emit - became an rc-1 host-state FAIL with an empty `expected_type=`
# field (Codex round-5 part B finding 2).
WPI_STATUS_SCHEMA='state:str state_version:int mode:str network:str exchange_conn:str exchange_enabled:bool credential_lookup:str arm_enabled:bool'

wpi_stop() { printf '%s_STOP reason=%s\n' "$1" "${*:2}"; exit 3; }
wpi_fail() {
    local prefix="$1"; shift
    if [ "$WPI_MOUNT_GUARD_ACTIVE" = yes ]; then
        wpi_mount_guard_end
    fi
    printf '%s_FAIL reason=%s\n' "$prefix" "$*"
    exit 1
}

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

wpi_require_path_structure() {
    local prefix="$1" path="$2" source="$3"
    case "$path" in
        /*) : ;;
        *) wpi_stop "$prefix" "structured_path_unparseable source=$source detail=not_absolute" ;;
    esac
    case "$path" in *'//'*) wpi_stop "$prefix" "structured_path_unparseable source=$source detail=empty_component" ;; esac
    case "/$path/" in *'/../'*|*'/./'*) wpi_stop "$prefix" "structured_path_unparseable source=$source detail=dot_component" ;; esac
}

wpi_write_text_leaf() {
    local value="$1" leaf fd
    WPI_PROBE_SEQ=$(( WPI_PROBE_SEQ + 1 ))
    leaf="$EV_DIR/ro.$(printf '%04d' "$WPI_PROBE_SEQ").suppressed_value.bin"
    wpi_open_leaf "$leaf"; fd="$WPI_LEAF_FD"
    printf '%s' "$value" >&"$fd" || wpi_stop RP7 "capture_leaf_write_failed leaf=$leaf"
    exec {fd}>&-
    wpi_sha_file RP7 suppressed_value_unreadable "$leaf"
}

wpi_render_path() {
    local path="$1"
    case "$path" in
        *[![:print:]]*|*[[:space:]]*)
            wpi_write_text_leaf "$path"
            WPI_PATH_FIELD="path=[unrenderable] path_sha256=$WPI_LINE"
            WPI_PATH_RENDERABLE=no
            ;;
        *)
            WPI_PATH_FIELD="path=$path"
            WPI_PATH_RENDERABLE=yes
            ;;
    esac
}

wpi_require_observed_path_grammar() {
    local prefix="$1" path="$2" source="$3"
    wpi_require_path_structure "$prefix" "$path" "$source"
    # Bash variables cannot contain NUL. Any absolute NUL-delimited record that
    # reached this point is a path; unsafe display bytes are content-suppressed.
    wpi_render_path "$path"
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
    # stderr is CLOSED, not redirected to /dev/null: /dev/null is outside both the
    # run evidence tree and the section-10.1 allowlist, so opening it for writing
    # would be an unpreregistered write open. Closing fd 2 discards the noclobber
    # diagnostic with no open at all and leaves the noclobber test itself intact.
    if ! ( set -o noclobber; : > "$leaf" ) 2>&-; then
        wpi_stop RP7 "capture_leaf_not_create_once leaf=$leaf"
    fi
}

# Allocate a leaf and KEEP the descriptor the creating open returned. The
# create-once test is the same `noclobber` test as above and STOPs with the same
# reason, but the object is not let go of between the create and the write: the
# recovered round-5 fixture replaced a freshly allocated leaf with a hard link to
# a file outside the evidence tree in exactly that window, and the capture then
# wrote its payload through the substituted name at rc 0 with no STOP. A name is
# not an object. Every shell-side write in this block goes through the descriptor
# this function returns, so the object written is the object created.
# The redirection is guarded by `|| rc=$?` because a failed `exec` redirection is
# a shell error, not a command failure, and would otherwise reach the ERR trap
# as an unadjudicated status instead of this reason.
wpi_open_leaf() {
    local leaf="$1" rc=0
    case "$leaf" in "$EV_DIR"/*) : ;; *) wpi_stop RP7 "capture_path_outside_evidence leaf=$leaf ev_dir=$EV_DIR" ;; esac
    WPI_LEAF_FD=""
    # stderr is CLOSED, not redirected to /dev/null, for the reason above.
    set -o noclobber
    { exec {WPI_LEAF_FD}>"$leaf"; } 2>&- || rc=$?
    set +o noclobber
    [ "$rc" -eq 0 ] && [ -n "$WPI_LEAF_FD" ] || wpi_stop RP7 "capture_leaf_not_create_once leaf=$leaf"
}

wpi_alloc_read_diag() {
    local label="$1"
    WPI_PROBE_SEQ=$(( WPI_PROBE_SEQ + 1 ))
    WPI_READ_DIAG="$EV_DIR/ro.$(printf '%04d' "$WPI_PROBE_SEQ").$label.read.stderr"
    wpi_open_leaf "$WPI_READ_DIAG"; WPI_READ_DIAG_FD="$WPI_LEAF_FD"
}

# Run one evidence-producing child from EV_DIR, with a cleared environment,
# fixed locale/PATH/TMPDIR, absolute argv[0], and separate create-once streams.
# The bounding wrapper is inside the cleared environment, not outside it: env is
# the first exec, so timeout - the process that decides whether a probe was
# bounded - runs under the same cleared environment as the probe it bounds.
wpi_capture() {
    local label="$1"; shift
    local start end rc=0 ofd efd brc=0
    if [ -n "$WPI_CAP_OUT_FD" ]; then exec {WPI_CAP_OUT_FD}<&-; WPI_CAP_OUT_FD=""; fi
    WPI_PROBE_SEQ=$(( WPI_PROBE_SEQ + 1 ))
    WPI_CAP_OUT="$EV_DIR/ro.$(printf '%04d' "$WPI_PROBE_SEQ").$label.stdout"
    WPI_CAP_ERR="$EV_DIR/ro.$(printf '%04d' "$WPI_PROBE_SEQ").$label.stderr"
    wpi_open_leaf "$WPI_CAP_OUT"; ofd="$WPI_LEAF_FD"
    wpi_open_leaf "$WPI_CAP_ERR"; efd="$WPI_LEAF_FD"
    wpi_clock_ms; start="$WPI_LINE"
    (
        cd "$EV_DIR" || exit 125
        exec "$WPI_ENV" -i LC_ALL=C PATH=/usr/bin:/bin HOME=/nonexistent TMPDIR="$EV_DIR" \
            "$WPI_TIMEOUT" --signal=TERM --kill-after=5s "${WPI_SWEEP_BUDGET_S}s" "$@"
    ) >&"$ofd" 2>&"$efd" || rc=$?
    # A reader that opens the leaf NAME again adjudicates whatever object that
    # name resolves to at read time, which is not necessarily the object the
    # child wrote (Codex round-6 part B finding 3). The read side is therefore
    # bound the same way the write side already is: while the creating write
    # descriptor is still open, `/dev/fd/<n>` is opened for reading, which
    # resolves THROUGH that descriptor instead of through the evidence
    # directory, so no name lookup happens after the child ran and a later
    # replacement of the leaf name cannot change the bytes read. The descriptor
    # is opened after the child exits, so the child never inherits it. It is
    # closed at the next capture, which is also why exactly one capture's
    # streams are bound at a time.
    { exec {WPI_CAP_OUT_FD}</dev/fd/"$ofd"; } 2>&- || brc=$?
    [ "$brc" -eq 0 ] && [ -n "$WPI_CAP_OUT_FD" ] \
        || wpi_stop RP7 "capture_stream_not_bindable label=$label leaf=$WPI_CAP_OUT"
    exec {ofd}>&-
    exec {efd}>&-
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

# Builtin-only exact single-record reader.
#
# Round 6 read this record with `IFS= read -r`, which SILENTLY DISCARDS NUL, so
# `2<NUL>00` was consumed as the completed HTTP status `200`, `O<NUL>K fields=8`
# as the parser's accepting result, and `ne<NUL>t:[100]` as a valid namespace
# identity - three malformed records normalised into accepting observations
# (Codex round-6 part B finding 1). The listener reader had already been
# rewritten for exactly this reason; this reader now uses the same discipline,
# so no caller of it can lose a byte before grammar.
#
# The whole stream is taken in ONE NUL-delimited read. That read returns 0 only
# when it actually found a NUL - the single byte class this reader cannot
# represent - and otherwise returns EOF with EVERY captured byte in `whole`.
# The record is then split out of that one string in memory, and
# `${#first} + 1 == ${#whole}` is the conservation equation that accounts for
# every captured byte against the one record and its terminator. LC_ALL=C is
# pinned at the top of this block, so `${#...}` is a byte count.
#
# There is deliberately no additional charset gate here, unlike the listener
# inventory reader: with `-r`, an empty IFS and a NUL delimiter, NUL is the only
# class `read` can drop, and every caller of this function already adjudicates
# the record against an exact grammar of its own. A gate that STOPped on, say,
# CR would silently change the accepted row-18 symlink-target disposition,
# which no finding asks for.
#
# The source is already a regular create-once evidence leaf.
wpi_single_record() {
    local prefix="$1" reason="$2" file="$3" fd whole="" first="" extra="" rc=0 diag dfd
    wpi_alloc_read_diag single_record; diag="$WPI_READ_DIAG"; dfd="$WPI_READ_DIAG_FD"
    exec {fd}<"$file" || wpi_stop "$prefix" "$reason detail=open_failed source=$file"
    IFS= read -r -d '' -u "$fd" whole 2>&"$dfd" || rc=$?
    exec {fd}<&-; exec {dfd}>&-
    wpi_require_empty_file "$prefix" "$reason detail=hard_read_error source=$file" "$diag"
    [ "$rc" -ne 0 ] || wpi_stop "$prefix" "$reason detail=nul_byte_in_record source=$file"
    [ -n "$whole" ] || wpi_stop "$prefix" "$reason detail=empty_or_read_error source=$file read_rc=$rc"
    case "$whole" in
        *$'\n'*) first="${whole%%$'\n'*}"; extra="${whole#*$'\n'}" ;;
        *) wpi_stop "$prefix" "$reason detail=unterminated_final_record source=$file read_rc=$rc" ;;
    esac
    if [ -n "$extra" ]; then
        case "$extra" in
            *$'\n'*) wpi_stop "$prefix" "$reason detail=multiple_records source=$file" ;;
            *) wpi_stop "$prefix" "$reason detail=unterminated_extra_record source=$file" ;;
        esac
    fi
    [ $(( ${#first} + 1 )) -eq "${#whole}" ] \
        || wpi_stop "$prefix" "$reason detail=record_bytes_unaccounted source=$file consumed=$(( ${#first} + 1 )) captured=${#whole}"
    WPI_LINE="$first"
}

# The third argument is the CALLER's row-specific inability-to-evaluate reason.
# Rows 17, 19 and 19a preregister `installed_lock_unreadable`, `metadata_unreadable`
# and `verifier_unreadable` respectively; only callers with no row-specific token of
# their own fall back to the generic `path_not_evaluable`.
wpi_lstat() {
    local prefix="$1" path="$2" unreadable="${3:-path_not_evaluable}" raw rest path_field
    wpi_render_path "$path"; path_field="$WPI_PATH_FIELD"
    wpi_capture lstat "$WPI_STAT" -c '%F|%a|%u:%g|%d:%i|%s' -- "$path"
    if [ "$WPI_CAP_RC" -ne 0 ]; then
        wpi_require_empty_file "$prefix" "$unreadable $path_field rc=$WPI_CAP_RC" "$WPI_CAP_OUT"
        wpi_single_record "$prefix" "$unreadable $path_field rc=$WPI_CAP_RC" "$WPI_CAP_ERR"
        # Only the diagnostic forms the pinned absolute argv[0] can itself produce
        # are accepted as proof of absence. A basename-prefixed diagnostic did not
        # come from the invocation this block controls.
        case "$WPI_LINE" in
            "$WPI_STAT: cannot statx '$path': No such file or directory"|"$WPI_STAT: cannot stat '$path': No such file or directory"|\
            "$WPI_STAT: cannot stat '$path': No such file or directory (os error 2)")
                WPI_META_KIND=absent; WPI_META_MODE=""; WPI_META_OWNER=""; WPI_META_ID=""; WPI_META_SIZE=""; return 0 ;;
            *) wpi_stop "$prefix" "$unreadable $path_field rc=$WPI_CAP_RC detail=unclassified_diagnostic diagnostic_file=$WPI_CAP_ERR" ;;
        esac
    fi
    wpi_require_empty_file "$prefix" "$unreadable $path_field rc=0" "$WPI_CAP_ERR"
    wpi_single_record "$prefix" "$unreadable $path_field rc=0" "$WPI_CAP_OUT"
    raw="$WPI_LINE"
    case "$raw" in *'|'*'|'*'|'*'|'*) : ;; *) wpi_stop "$prefix" "$unreadable $path_field rc=0 detail=metadata_grammar" ;; esac
    WPI_META_KIND="${raw%%|*}"; rest="${raw#*|}"
    WPI_META_MODE="${rest%%|*}"; rest="${rest#*|}"
    WPI_META_OWNER="${rest%%|*}"; rest="${rest#*|}"
    WPI_META_ID="${rest%%|*}"; WPI_META_SIZE="${rest#*|}"
    case "$WPI_META_MODE" in ''|*[!0-7]*) wpi_stop "$prefix" "$unreadable $path_field rc=0 detail=mode_grammar" ;; esac
    case "$WPI_META_OWNER" in *[!0-9:]*|*:*:*|:*|*:|'') wpi_stop "$prefix" "$unreadable $path_field rc=0 detail=owner_grammar" ;; *:*) : ;; *) wpi_stop "$prefix" "$unreadable $path_field rc=0 detail=owner_grammar" ;; esac
    case "$WPI_META_ID" in *[!0-9:]*|*:*:*|:*|*:|'') wpi_stop "$prefix" "$unreadable $path_field rc=0 detail=object_id_grammar" ;; *:*) : ;; *) wpi_stop "$prefix" "$unreadable $path_field rc=0 detail=object_id_grammar" ;; esac
    case "$WPI_META_SIZE" in ''|*[!0-9]*) wpi_stop "$prefix" "$unreadable $path_field rc=0 detail=size_grammar" ;; esac
}

wpi_kind_token() {
    case "$1" in
        directory) WPI_LINE=directory ;;
        'regular file'|'regular empty file') WPI_LINE=regular ;;
        'symbolic link') WPI_LINE=symlink ;;
        absent) WPI_LINE=absent ;;
        *) WPI_LINE=other ;;
    esac
}

wpi_walk_deviation() {
    local outcome="$1" prefix="$2" message="$3"
    if [ "$outcome" = stop ]; then wpi_stop "$prefix" "$message"; fi
    wpi_fail "$prefix" "$message"
}

# Arguments 10-12 carry the row-specific evidence grammar of the caller:
#   10 unreadable_reason  - the row's inability-to-evaluate token (see wpi_lstat)
#   11 leaf_owner_reason  - the row's own numeric-ownership deviation FAIL for the
#                           bound LEAF; empty keeps the generic path_metadata_mismatch
#   12 leaf_field_style   - `kind_only` emits the leaf object/owner deviation without
#                           a path= field (row 17 records `kind=<k>` only); the
#                           default `with_path` keeps it (row 19a records path=<p>).
wpi_walk_components() {
    local prefix="$1" path="$2" leaf_kind="$3" leaf_mode="$4" leaf_owner="$5"
    local leaf_absent_reason="${6:-path_absent}" leaf_object_reason="${7:-path_metadata_mismatch}"
    local outcome="${8:-fail}" stop_context="${9:-path_binding_not_evaluable}"
    local unreadable="${10:-path_not_evaluable}" leaf_owner_reason="${11:-}" leaf_field_style="${12:-with_path}"
    local rest component current="" expected_kind expected_owner expected_mode kind_token deviation_reason walk_path_field leaf_fields
    wpi_require_path_structure "$prefix" "$path" component_walk
    wpi_render_path "$path"; walk_path_field="$WPI_PATH_FIELD"
    wpi_lstat "$prefix" / "$unreadable"
    if [ "$WPI_META_KIND" != directory ]; then
        wpi_kind_token "$WPI_META_KIND"
        wpi_stop "$prefix" "$unreadable path=/ detail=root_kind_$WPI_LINE"
    fi
    [ "$WPI_META_OWNER" = 0:0 ] || wpi_stop "$prefix" "$unreadable path=/ owner_numeric=$WPI_META_OWNER expected=0:0"
    rest="${path#/}"
    IFS='/' read -r -a WPI_COMPONENTS <<< "$rest"
    [ "${#WPI_COMPONENTS[@]}" -ge 1 ] || wpi_stop "$prefix" "$unreadable $walk_path_field detail=no_components"
    for component in "${WPI_COMPONENTS[@]}"; do
        [ -n "$component" ] || wpi_stop "$prefix" "$unreadable $walk_path_field detail=empty_component"
        [ "$component" != "." ] && [ "$component" != ".." ] || wpi_stop "$prefix" "$unreadable $walk_path_field detail=dot_component"
        current="$current/$component"
        expected_kind="directory"; expected_owner="0:0"; expected_mode=any
        if [ "$current" = "$path" ]; then
            expected_kind="$leaf_kind"; expected_owner="$leaf_owner"
            [ -n "$leaf_mode" ] && expected_mode="${leaf_mode#0}"
        fi
        wpi_lstat "$prefix" "$current" "$unreadable"
        if [ "$leaf_field_style" = kind_only ]; then leaf_fields=""; else leaf_fields=" $WPI_PATH_FIELD"; fi
        if [ "$WPI_META_KIND" = absent ]; then
            if [ "$outcome" = stop ]; then
                wpi_stop "$prefix" "$stop_context detail=path_absent $WPI_PATH_FIELD"
            elif [ "$current" = "$path" ]; then wpi_fail "$prefix" "$leaf_absent_reason $WPI_PATH_FIELD"
            else wpi_fail "$prefix" "path_absent $WPI_PATH_FIELD"; fi
        fi
        wpi_kind_token "$WPI_META_KIND"; kind_token="$WPI_LINE"
        case "$expected_kind:$WPI_META_KIND" in
            directory:directory|regular:'regular file'|regular:'regular empty file') : ;;
            *) if [ "$outcome" = stop ]; then
                   wpi_stop "$prefix" "$stop_context detail=path_metadata_mismatch $WPI_PATH_FIELD kind=$kind_token mode=$WPI_META_MODE owner_numeric=$WPI_META_OWNER expected=$expected_kind,$expected_mode,$expected_owner"
               elif [ "$current" = "$path" ] && [ "$leaf_object_reason" != path_metadata_mismatch ]; then
                   wpi_fail "$prefix" "$leaf_object_reason$leaf_fields kind=$kind_token"
               else
                   wpi_fail "$prefix" "path_metadata_mismatch $WPI_PATH_FIELD kind=$kind_token mode=$WPI_META_MODE owner_numeric=$WPI_META_OWNER expected=$expected_kind,$expected_mode,$expected_owner"
               fi ;;
        esac
        if [ "$WPI_META_OWNER" != "$expected_owner" ]; then
            if [ "$outcome" != stop ] && [ "$current" = "$path" ] && [ -n "$leaf_owner_reason" ]; then
                wpi_fail "$prefix" "$leaf_owner_reason$leaf_fields owner_numeric=$WPI_META_OWNER expected=$expected_owner"
            fi
            if [ "$outcome" = stop ]; then deviation_reason="$stop_context detail=path_metadata_mismatch"
            else deviation_reason=path_metadata_mismatch; fi
            wpi_walk_deviation "$outcome" "$prefix" "$deviation_reason $WPI_PATH_FIELD kind=$kind_token mode=$WPI_META_MODE owner_numeric=$WPI_META_OWNER expected=$expected_kind,$expected_mode,$expected_owner"
        fi
        if [ "$current" = "$path" ] && [ -n "$leaf_mode" ]; then
            if [ "$WPI_META_MODE" != "${leaf_mode#0}" ]; then
                if [ "$outcome" = stop ]; then deviation_reason="$stop_context detail=path_metadata_mismatch"
                else deviation_reason=path_metadata_mismatch; fi
                wpi_walk_deviation "$outcome" "$prefix" "$deviation_reason $WPI_PATH_FIELD kind=$kind_token mode=$WPI_META_MODE owner_numeric=$WPI_META_OWNER expected=$expected_kind,$expected_mode,$expected_owner"
            fi
        fi
    done
}

wpi_parse_mountinfo() {
    local file="$1" fd line="" rc=0 records=0 pre post diag dfd seen_ids=" "
    local device root mount_point fstype source
    WPI_MI_DEVICE=(); WPI_MI_ROOT=(); WPI_MI_POINT=(); WPI_MI_FSTYPE=(); WPI_MI_SOURCE=()
    wpi_alloc_read_diag mount_table; diag="$WPI_READ_DIAG"; dfd="$WPI_READ_DIAG_FD"
    exec {fd}<"$file" || wpi_stop RP7 "mount_table_unreadable path=$file detail=open_failed"
    while true; do
        line=""; rc=0; IFS= read -r -u "$fd" line 2>&"$dfd" || rc=$?
        if [ "$rc" -ne 0 ]; then
            exec {fd}<&-; exec {dfd}>&-
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
        device="$3"; root="$4"; mount_point="$5"
        set -- $post
        [ "$#" -ge 3 ] || wpi_stop RP7 "mount_table_malformed path=$file record=$((records+1)) detail=post_fields"
        fstype="$1"; source="$2"
        case "$fstype:$source" in *[[:space:]]*) wpi_stop RP7 "mount_table_malformed path=$file record=$((records+1)) detail=post_field_whitespace" ;; esac
        WPI_MI_DEVICE+=("$device"); WPI_MI_ROOT+=("$root"); WPI_MI_POINT+=("$mount_point")
        WPI_MI_FSTYPE+=("$fstype"); WPI_MI_SOURCE+=("$source")
        records=$(( records + 1 ))
    done
    [ "$records" -ge 1 ] || wpi_stop RP7 "mount_table_unreadable path=$file detail=no_records"
    printf 'RP7_mount_table parsed=yes records=%s content=not_printed\n' "$records"
}

wpi_capture_mountinfo_snapshot() {
    local snapshot infd outfd line="" rc=0 diag dfd
    WPI_MOUNT_SNAPSHOT_SEQ=$(( WPI_MOUNT_SNAPSHOT_SEQ + 1 ))
    snapshot="$EV_DIR/ro.mountinfo.$(printf '%04d' "$WPI_MOUNT_SNAPSHOT_SEQ").snapshot"
    wpi_open_leaf "$snapshot"; outfd="$WPI_LEAF_FD"
    wpi_alloc_read_diag mountinfo_snapshot; diag="$WPI_READ_DIAG"; dfd="$WPI_READ_DIAG_FD"
    exec {infd}</proc/self/mountinfo || { exec {outfd}>&-; exec {dfd}>&-; wpi_stop RP7 "mount_table_unreadable path=/proc/self/mountinfo detail=open_failed"; }
    while true; do
        line=""; rc=0; IFS= read -r -u "$infd" line 2>&"$dfd" || rc=$?
        if [ "$rc" -ne 0 ]; then
            exec {infd}<&-; exec {outfd}>&-; exec {dfd}>&-
            wpi_require_empty_file RP7 "mount_table_read_error path=/proc/self/mountinfo" "$diag"
            [ -z "$line" ] || wpi_stop RP7 "mount_table_unterminated_final_record path=/proc/self/mountinfo"
            break
        fi
        printf '%s\n' "$line" >&"$outfd" || { exec {infd}<&-; exec {outfd}>&-; exec {dfd}>&-; wpi_stop RP7 "mount_table_unreadable path=$snapshot detail=evidence_write_failed"; }
    done
    WPI_LINE="$snapshot"
}

# normalised_path_projection_v2. Three record types, emitted in this fixed order:
#   kind=point         one per preregistered point path, its EFFECTIVE covering
#                      mount (longest mount point, last such record in mountinfo
#                      order) plus the number of records sharing that mount point,
#                      so a mount stacked on an existing mount point is visible
#                      instead of silently collapsed;
#   kind=subtree       every mountinfo record at or below a preregistered root, in
#                      mountinfo order, so a bind or overlay mount anywhere inside a
#                      trusted subtree changes the digest even though the root's own
#                      covering mount is unchanged;
#   kind=subtree_count one per root, the number of its subtree records.
# v1 projected 18 point paths only and was therefore blind to both cases.
wpi_build_mount_projection() {
    local snapshot="$1" projection pfd path mp best=-1 best_len=-1 i len shared
    local r rprefix subtree_records seen_roots=" "
    local -a points=(
        "$WPI_STAT" "$WPI_READLINK" "$WPI_ENV" "$WPI_FIND" "$WPI_SHA256SUM"
        "$WPI_SYSTEMCTL" "$WPI_SS" "$WPI_CURL" "$WPI_TIMEOUT" "$WPI_PYTHON3"
        "$WPI_RELEASE_ROOT" "$WPI_VENV_ROOT" "$WPI_UNIT_FRAGMENT"
        "$WPI_STATE_DIR" "$WPI_LOG_DIR" "$WPI_CONF_DIR"
        "$WPI_RELEASE_ROOT/IBKR_PAPER_BRIDGE/requirements.lock"
        "$WPI_RELEASE_ROOT/IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py"
        /proc/self/mountinfo /proc/self/ns/net "/proc/$WPI_MAINPID/ns/net"
    )
    local -a root_candidates=(
        "$WPI_RELEASE_ROOT" "$WPI_VENV_ROOT" "$WPI_CONF_DIR" "$WPI_STATE_DIR" "$WPI_LOG_DIR"
        "${WPI_STAT%/*}" "${WPI_READLINK%/*}" "${WPI_ENV%/*}" "${WPI_FIND%/*}"
        "${WPI_SHA256SUM%/*}" "${WPI_SYSTEMCTL%/*}" "${WPI_SS%/*}" "${WPI_CURL%/*}"
        "${WPI_TIMEOUT%/*}" "${WPI_PYTHON3%/*}"
    )
    local -a roots=()
    for r in "${root_candidates[@]}"; do
        [ -n "$r" ] || r=/
        case "$seen_roots" in *" $r "*) continue ;; esac
        seen_roots="$seen_roots$r "
        roots+=("$r")
    done
    wpi_parse_mountinfo "$snapshot"
    WPI_PROBE_SEQ=$(( WPI_PROBE_SEQ + 1 ))
    projection="$EV_DIR/ro.$(printf '%04d' "$WPI_PROBE_SEQ").mount_projection.tsv"
    wpi_open_leaf "$projection"; pfd="$WPI_LEAF_FD"
    for path in "${points[@]}"; do
        best=-1; best_len=-1
        for ((i=0; i<${#WPI_MI_POINT[@]}; i++)); do
            mp="${WPI_MI_POINT[$i]}"
            if [ "$mp" = / ] || [ "$path" = "$mp" ] || [[ "$path" == "$mp/"* ]]; then
                len=${#mp}
                # -ge, not -gt: a later record at the same mount point shadows the
                # earlier one, so the last match is the effective mount.
                if [ "$len" -ge "$best_len" ]; then best="$i"; best_len="$len"; fi
            fi
        done
        [ "$best" -ge 0 ] || wpi_stop RP7 "mount_projection_unbound path=$path"
        shared=0
        for ((i=0; i<${#WPI_MI_POINT[@]}; i++)); do
            [ "${WPI_MI_POINT[$i]}" = "${WPI_MI_POINT[$best]}" ] || continue
            shared=$(( shared + 1 ))
        done
        printf 'kind=point\tpath=%s\tdevice=%s\troot=%s\tmount_point=%s\tfstype=%s\tsource=%s\tshared_mount_point_records=%s\n' \
            "$path" "${WPI_MI_DEVICE[$best]}" "${WPI_MI_ROOT[$best]}" \
            "${WPI_MI_POINT[$best]}" "${WPI_MI_FSTYPE[$best]}" "${WPI_MI_SOURCE[$best]}" "$shared" \
            >&"$pfd" || wpi_stop RP7 "mount_projection_write_failed path=$projection"
    done
    for r in "${roots[@]}"; do
        subtree_records=0
        rprefix="${r%/}/"
        for ((i=0; i<${#WPI_MI_POINT[@]}; i++)); do
            mp="${WPI_MI_POINT[$i]}"
            [ "$mp" = "$r" ] || [[ "$mp" == "$rprefix"* ]] || continue
            subtree_records=$(( subtree_records + 1 ))
            printf 'kind=subtree\tsubtree_root=%s\tseq=%s\tdevice=%s\troot=%s\tmount_point=%s\tfstype=%s\tsource=%s\n' \
                "$r" "$subtree_records" "${WPI_MI_DEVICE[$i]}" "${WPI_MI_ROOT[$i]}" \
                "$mp" "${WPI_MI_FSTYPE[$i]}" "${WPI_MI_SOURCE[$i]}" \
                >&"$pfd" || wpi_stop RP7 "mount_projection_write_failed path=$projection"
        done
        printf 'kind=subtree_count\tsubtree_root=%s\trecords=%s\n' "$r" "$subtree_records" \
            >&"$pfd" || wpi_stop RP7 "mount_projection_write_failed path=$projection"
    done
    exec {pfd}>&-
    wpi_sha_file RP7 mount_projection_unreadable "$projection"
    WPI_MOUNT_PROJECTION_DIGEST="$WPI_LINE"
    printf 'RP7_mount_projection format=normalised_path_projection_v2 points=%s roots=%s mount_records=%s raw_snapshot=%s projection=%s sha256=%s content=not_printed\n' \
        "${#points[@]}" "${#roots[@]}" "${#WPI_MI_POINT[@]}" "$snapshot" "$projection" "$WPI_MOUNT_PROJECTION_DIGEST"
}

wpi_sha_file() {
    local prefix="$1" reason="$2" path="$3" digest rendered path_field
    case "$path" in *[![:print:]]*|*[[:space:]]*) path_field='path=[unrenderable]' ;; *) path_field="path=$path" ;; esac
    wpi_capture sha256 "$WPI_SHA256SUM" -- "$path"
    [ "$WPI_CAP_RC" -eq 0 ] || wpi_stop "$prefix" "$reason $path_field rc=$WPI_CAP_RC detail=sha256sum_failed diagnostic_file=$WPI_CAP_ERR"
    wpi_require_empty_file "$prefix" "$reason $path_field rc=0" "$WPI_CAP_ERR"
    wpi_single_record "$prefix" "$reason $path_field rc=0" "$WPI_CAP_OUT"
    rendered="$WPI_LINE"; digest="${rendered%% *}"
    [ "${#digest}" -eq 64 ] || wpi_stop "$prefix" "$reason $path_field rc=0 detail=digest_grammar"
    case "$digest" in *[!0-9a-f]*) wpi_stop "$prefix" "$reason $path_field rc=0 detail=digest_grammar" ;; esac
    WPI_LINE="$digest"
}

wpi_mount_guard_begin() {
    local snapshot
    [ "$WPI_MOUNT_GUARD_ACTIVE" = no ] || wpi_stop RP7 "mount_guard_nested"
    wpi_capture_mountinfo_snapshot; snapshot="$WPI_LINE"
    wpi_build_mount_projection "$snapshot"
    [ "$WPI_MOUNT_PROJECTION_DIGEST" = "$WPI_ATTESTED_MOUNTINFO_SHA256" ] || \
        wpi_stop RP7 "mount_topology_mismatch observed=$WPI_MOUNT_PROJECTION_DIGEST attested=$WPI_ATTESTED_MOUNTINFO_SHA256 format=normalised_path_projection_v2"
    WPI_MOUNT_BEFORE="$WPI_MOUNT_PROJECTION_DIGEST"
    WPI_MOUNT_GUARD_ACTIVE=yes
}

wpi_mount_guard_end() {
    local snapshot before="$WPI_MOUNT_BEFORE"
    [ "$WPI_MOUNT_GUARD_ACTIVE" = yes ] || wpi_stop RP7 "mount_guard_not_open"
    wpi_capture_mountinfo_snapshot; snapshot="$WPI_LINE"
    wpi_build_mount_projection "$snapshot"
    WPI_MOUNT_GUARD_ACTIVE=no
    [ "$WPI_MOUNT_PROJECTION_DIGEST" = "$before" ] || \
        wpi_stop RP7 "mount_topology_changed before=$before after=$WPI_MOUNT_PROJECTION_DIGEST format=normalised_path_projection_v2"
}

wpi_bind_tool() {
    local name="$1" path="$2" attestation
    wpi_require_absolute "WPI_TOOL_PINS.$name" "$path"
    [ -x "$path" ] || wpi_stop RP7 "tool_not_evaluable tool=$name path=$path detail=not_executable"
    wpi_walk_components RP7 "$path" regular "" 0:0 path_absent path_metadata_mismatch stop "tool_not_evaluable tool=$name"
    case "$WPI_META_MODE" in ???) : ;; *) wpi_stop RP7 "tool_not_evaluable tool=$name path=$path detail=mode_grammar" ;; esac
    [ $(( 8#$WPI_META_MODE & 8#022 )) -eq 0 ] || wpi_stop RP7 "tool_not_evaluable tool=$name path=$path mode=$WPI_META_MODE detail=group_or_world_writable"
    # Truthfulness of the binding claim: stat, env, sha256sum and timeout are the
    # instruments the mount projection and this very binding are built from, so
    # they are exercised before any RP7_tool line exists. They attest themselves;
    # the remaining six - including the trusted adjudicating python3 - are bound by
    # already-attested instruments.
    case "$name" in
        stat|env|sha256sum|timeout) attestation=self ;;
        *) attestation=bound_instrument ;;
    esac
    printf 'RP7_tool name=%s path=%s owner_numeric=0:0 mode=%s kind=regular resolution=pinned_absolute attestation=%s\n' "$name" "$path" "$WPI_META_MODE" "$attestation"
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
    wpi_expect_literal WPI_LOG_DIR "$WPI_LOG_DIR" /var/log/mtc-bridge
    wpi_expect_literal WPI_CONF_DIR "$WPI_CONF_DIR" /etc/mtc-bridge
    wpi_expect_literal WPI_CONTROL_ENDPOINT "$WPI_CONTROL_ENDPOINT" http://127.0.0.1:8790/api/status
    wpi_expect_literal WPI_SWEEP_BUDGET_S "$WPI_SWEEP_BUDGET_S" 120

    wpi_require_set WPI_TOOL_PINS "${WPI_TOOL_PINS:-}"
    for entry in $WPI_TOOL_PINS; do
        case "$entry" in *=*) pin_name="${entry%%=*}"; pin_path="${entry#*=}" ;; *) wpi_stop RP7 "prereg_input_malformed name=WPI_TOOL_PINS entry=missing_equals" ;; esac
        case "$pin_name" in stat|readlink|env|find|sha256sum|systemctl|ss|curl|timeout|python3) : ;; *) wpi_stop RP7 "prereg_input_malformed name=WPI_TOOL_PINS unknown_tool=$pin_name" ;; esac
        case "$pin_seen" in *" $pin_name "*) wpi_stop RP7 "prereg_input_malformed name=WPI_TOOL_PINS duplicate=$pin_name" ;; esac
        wpi_require_absolute "WPI_TOOL_PINS.$pin_name" "$pin_path"
        if [ "$pin_name" = python3 ]; then
            # The one pin whose leaf name is a freeze-gate input. /usr/bin/python3 is
            # a symlink on the target family and wpi_bind_tool admits no symlinked
            # object, so the resolved /usr/bin/python3.<minor> is pinned at freeze.
            case "$pin_path" in /usr/bin/python3|/usr/bin/python3.[0-9]|/usr/bin/python3.[0-9][0-9]) : ;;
                *) wpi_stop RP7 "prereg_input_malformed name=WPI_TOOL_PINS.python3 expected=/usr/bin/python3_or_python3.MINOR" ;;
            esac
            wpi_expect_literal WPI_TOOL_PINS.python3 "$pin_path" "$WPI_FIXED_TRUSTED_PYTHON"
        else
            [ "$pin_path" = "/usr/bin/$pin_name" ] || wpi_stop RP7 "prereg_input_malformed name=WPI_TOOL_PINS.$pin_name expected=/usr/bin/$pin_name"
        fi
        pin_seen="$pin_seen$pin_name "; pin_count=$(( pin_count + 1 ))
    done
    [ "$pin_count" -eq 10 ] || wpi_stop RP7 "prereg_input_malformed name=WPI_TOOL_PINS observed_count=$pin_count expected_count=10"
    for name in stat readlink env find sha256sum systemctl ss curl timeout python3; do
        wpi_map_get "$WPI_TOOL_PINS" "$name"; path="$WPI_LINE"
        printf -v "WPI_${name^^}" '%s' "$path"
    done
    wpi_require_sha256 WPI_ATTESTED_MOUNTINFO_SHA256 "${WPI_ATTESTED_MOUNTINFO_SHA256:-}"
    wpi_expect_literal WPI_ATTESTED_MOUNTINFO_SHA256 "$WPI_ATTESTED_MOUNTINFO_SHA256" "$WPI_FIXED_ATTESTED_MOUNT_PROJECTION_SHA256"
    wpi_require_uint WPI_MAINPID "${WPI_MAINPID:-}" 2
    wpi_expect_literal WPI_MAINPID "$WPI_MAINPID" 189813
    wpi_require_set WPI_VERIFY_LOCK_SHA256 "${WPI_VERIFY_LOCK_SHA256:-}"
    wpi_expect_literal WPI_VERIFY_LOCK_SHA256 "${WPI_VERIFY_LOCK_SHA256:-}" d951e0eea01ec1a89bcfbe9d9630949b31bb316faae2ba6bcae39be794a451e5
}

wpi_assert_prerequisites() {
    # `builtin type -t` is the non-overridable form and needs no redirection: with
    # -t an undefined name prints nothing on either stream and returns 1, so no
    # /dev/null write open is required to silence it, and `builtin` bypasses any
    # function named `type`. It is also strictly narrower than `command -v`, which
    # would have been satisfied by an executable of the same name on PATH.
    [ "$(builtin type -t rp0_require_safe_component)" = function ] || wpi_stop RP7 "rp0_lib_not_sourced predicate=rp0_require_safe_component"
    [ "$(builtin type -t rp0_allocate_evidence_dir)" = function ] || wpi_stop RP7 "rp0_lib_not_sourced predicate=rp0_allocate_evidence_dir"
    wpi_require_set RUNID "${RUNID:-}"; wpi_require_set EV_STAGE_ID "${EV_STAGE_ID:-}"
    wpi_require_set EV_DIR "${EV_DIR:-}"; wpi_require_set EV_LOG "${EV_LOG:-}"
    rp0_require_safe_component RUNID "$RUNID" || wpi_stop RP7 "evidence_identifier_refused name=RUNID"
    rp0_require_safe_component EV_STAGE_ID "$EV_STAGE_ID" || wpi_stop RP7 "evidence_identifier_refused name=EV_STAGE_ID"
    [ "$EV_STAGE_ID" = ro ] || wpi_stop RP7 "prereg_input_malformed name=EV_STAGE_ID expected=ro"
    # Evidence-root provenance, established BEFORE any leaf can be allocated. The
    # two existing containments (EV_LOG below EV_DIR, every capture leaf below
    # EV_DIR) are relative; this is the absolute one they hang from.
    wpi_require_absolute EV_DIR "$EV_DIR"
    [ "$WPI_FIXED_EVIDENCE_ROOT" != '<PIN-AT-FREEZE>' ] || \
        wpi_stop RP7 "evidence_root_unattested detail=freeze_gate_pin_unfilled name=WPI_FIXED_EVIDENCE_ROOT"
    wpi_require_absolute WPI_FIXED_EVIDENCE_ROOT "$WPI_FIXED_EVIDENCE_ROOT"
    case "$EV_DIR" in
        "$WPI_FIXED_EVIDENCE_ROOT"/*) : ;;
        *) wpi_stop RP7 "evidence_root_unattested ev_dir=$EV_DIR expected_root=$WPI_FIXED_EVIDENCE_ROOT" ;;
    esac
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
    printf 'RP7_evidence_bound leaf=%s object_id=%s stdout_path=[%s] mechanism=dev_inode_identity evidence_root=%s root_binding=frozen_prefix_descent\n' "$EV_LOG" "$logid" "$WPI_SAFE" "$WPI_FIXED_EVIDENCE_ROOT"
}

wpi_run_find() {
    local prefix="$1" label="$2" root="$3" elapsed_s; shift 3
    wpi_capture "$label" "$WPI_FIND" "$root" "$@"
    # Whole seconds actually elapsed (truncated), so elapsed_s never disagrees
    # with the elapsed_ms it renders. Enforcement below is on milliseconds.
    elapsed_s=$(( WPI_CAP_ELAPSED_MS / 1000 ))
    if [ "$WPI_CAP_RC" -eq 124 ] || [ "$WPI_CAP_ELAPSED_MS" -gt $(( WPI_SWEEP_BUDGET_S * 1000 )) ]; then
        wpi_stop "$prefix" "sweep_budget_exceeded root=$root elapsed_s=$elapsed_s elapsed_ms=$WPI_CAP_ELAPSED_MS budget_s=$WPI_SWEEP_BUDGET_S"
    fi
    if [ "$WPI_CAP_RC" -ne 0 ]; then
        wpi_stop "$prefix" "walk_incomplete root=$root rc=$WPI_CAP_RC detail=diagnostic_captured diagnostic_file=$WPI_CAP_ERR partial_stdout_discarded=$WPI_CAP_OUT"
    fi
    wpi_require_empty_file "$prefix" "walk_incomplete root=$root rc=0" "$WPI_CAP_ERR"
}

wpi_assert_tree() {
    local root="$1" label="$2" out fd path="" rc=0 writable_count=0 find_elapsed find_elapsed_s
    local diag dfd
    wpi_mount_guard_begin
    wpi_walk_components B3 "$root" directory 0555 0:0
    wpi_run_find B3 "${label}_writable" "$root" -perm /222 -print0
    out="$WPI_CAP_OUT"; find_elapsed="$WPI_CAP_ELAPSED_MS"; find_elapsed_s=$(( find_elapsed / 1000 ))
    [ -r "$out" ] && [ -f "$out" ] || wpi_stop B3 "walk_incomplete root=$root detail=stdout_not_readable_regular"
    if [ -s "$out" ]; then
        wpi_alloc_read_diag writable_paths; diag="$WPI_READ_DIAG"; dfd="$WPI_READ_DIAG_FD"
        exec {fd}<"$out" || wpi_stop B3 "walk_incomplete root=$root detail=stdout_open_failed"
        while true; do
            path=""; rc=0; IFS= read -r -d '' -u "$fd" path 2>&"$dfd" || rc=$?
            if [ "$rc" -ne 0 ]; then
                exec {fd}<&-; exec {dfd}>&-
                wpi_require_empty_file B3 "walk_incomplete root=$root detail=stdout_read_error" "$diag"
                [ -z "$path" ] || wpi_stop B3 "walk_incomplete root=$root detail=unterminated_nul_record"
                break
            fi
            wpi_require_observed_path_grammar B3 "$path" find_stdout
            writable_count=$(( writable_count + 1 ))
            [ "$writable_count" -eq 1 ] || continue
            WPI_FIRST_WRITABLE_FIELD="$WPI_PATH_FIELD"
        done
        [ "$writable_count" -ge 1 ] || wpi_stop B3 "walk_incomplete root=$root detail=nonempty_unparseable_stdout"
        wpi_fail B3 "writable_path_inside_immutable_tree $WPI_FIRST_WRITABLE_FIELD count=$writable_count"
    fi
    wpi_mount_guard_end
    printf 'B3_path path=%s kind=directory mode=555 owner_numeric=0:0 binding=component_and_mount_window_closed\n' "$root"
    printf 'B3_sweep root=%s complete=yes elapsed_s=%s elapsed_ms=%s writable_paths=0\n' "$root" "$find_elapsed_s" "$find_elapsed"
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

# The unreadable and numeric-ownership deviation tokens are derived from the row's
# own label, so every form this helper can emit for rows 17 and 19a is one the row
# preregisters: <label>_unreadable for an inability to evaluate any component or the
# leaf, and <label>_owner_unexpected for a bound leaf whose numeric ownership
# deviates. `field_style` selects row 17's `kind=<k>`-only rendering against row 19a's
# `path=<p> kind=<k>`.
wpi_assert_regular_digest() {
    local prefix="$1" absent_reason="$2" mismatch_reason="$3" path="$4" bytes="$5" digest="$6" label="$7" object_reason="${8:-path_metadata_mismatch}" field_style="${9:-with_path}" observed_size
    wpi_mount_guard_begin
    wpi_walk_components "$prefix" "$path" regular "" 0:0 "$absent_reason" "$object_reason" fail path_binding_not_evaluable \
        "${label}_unreadable" "${label}_owner_unexpected" "$field_style"
    observed_size="$WPI_META_SIZE"
    wpi_sha_file "$prefix" "${label}_unreadable" "$path"
    WPI_OBSERVED_DIGEST="$WPI_LINE"
    wpi_mount_guard_end
    [ "$observed_size" = "$bytes" ] || wpi_fail "$prefix" "$mismatch_reason observed_bytes=$observed_size expected_bytes=$bytes"
    [ "$WPI_OBSERVED_DIGEST" = "$digest" ] || wpi_fail "$prefix" "$mismatch_reason observed=$WPI_OBSERVED_DIGEST expected=$digest"
    printf '%s_digest path=%s bytes=%s sha256=%s binding=component_and_mount\n' "$prefix" "$path" "$observed_size" "$WPI_OBSERVED_DIGEST"
}

wpi_assert_interpreter() {
    local py="$WPI_VENV_ROOT/bin/python" resolved
    wpi_mount_guard_begin
    wpi_walk_components B1 "$WPI_VENV_ROOT/bin" directory "" 0:0
    wpi_lstat B1 "$py"
    [ "$WPI_META_KIND" != absent ] || wpi_fail B1 "interpreter_absent path=$py"
    case "$WPI_META_KIND" in
        'symbolic link')
            wpi_capture interpreter_target "$WPI_READLINK" -- "$py"
            [ "$WPI_CAP_RC" -eq 0 ] || wpi_stop B1 "interpreter_object_unbound kind=symlink target=unreadable"
            wpi_require_empty_file B1 "interpreter_object_unbound kind=symlink" "$WPI_CAP_ERR"
            wpi_single_record B1 "interpreter_object_unbound kind=symlink" "$WPI_CAP_OUT"; resolved="$WPI_LINE"
            wpi_sanitize "$resolved"
            wpi_stop B1 "interpreter_object_unbound kind=symlink target=$WPI_SAFE" ;;
        'regular file'|'regular empty file')
            [ "$WPI_META_OWNER" = 0:0 ] || wpi_stop B1 "interpreter_object_unbound kind=regular owner_numeric=$WPI_META_OWNER expected=0:0"
            : ;;
        *) wpi_kind_token "$WPI_META_KIND"
           wpi_stop B1 "interpreter_object_unbound kind=$WPI_LINE target=none" ;;
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
    printf 'B1_interpreter path=%s object=non_symlink_regular preexec_binding=component_and_mount_window_closed exec_binding=separate_bounded_exec version_family=3.12 env=cleared isolated=yes\n' "$py"
}

# ONE explicit discovery universe, shared verbatim with the trusted verifier driver
# in wpi_assert_lock_parity (Codex F1 + F3). The round-3 enumeration filtered on
# `-name '*.dist-info'` and therefore could not observe the other formats and
# locations importlib.metadata accepts, so it never established complete readability
# of the verifier's input universe. The enumeration is now UNFILTERED: every direct
# child of site-packages is classified, the only admissible metadata object is a
# `*.dist-info` DIRECTORY carrying METADATA and RECORD, and every other discovery
# format or location the verifier would accept - egg-info, egg-link, egg, zip/whl
# archive routes - plus the `.pth` and sitecustomize/usercustomize startup hooks that
# can ADD locations or execute, is a STOP rather than a silently unenumerated object.
# The trusted driver re-derives the same universe from its own scan and rejects the
# same set, so no accepting result can rest on a format only one side enumerated.
wpi_assert_metadata_readable() {
    local site="$WPI_VENV_ROOT/lib/python3.12/site-packages" out fd path="" rc=0 count=0 member diag dfd
    local entries=0 ignored=0 base fmt
    [ "$WPI_VENV_WALK_COMPLETE" = yes ] || wpi_stop B1 "verifier_not_evaluable rc=3 detail=venv_walk_not_complete"
    [ "$WPI_INTERPRETER_RAN" = yes ] || wpi_stop B1 "verifier_not_evaluable rc=3 detail=interpreter_not_run"
    wpi_mount_guard_begin
    wpi_walk_components B1 "$site" directory "" 0:0 path_absent path_metadata_mismatch fail path_binding_not_evaluable metadata_unreadable
    wpi_run_find B1 metadata_enumeration "$site" -mindepth 1 -maxdepth 1 -print0
    out="$WPI_CAP_OUT"
    wpi_alloc_read_diag metadata_paths; diag="$WPI_READ_DIAG"; dfd="$WPI_READ_DIAG_FD"
    exec {fd}<"$out" || wpi_stop B1 "metadata_unreadable path=$site detail=enumeration_open_failed"
    while true; do
        path=""; rc=0; IFS= read -r -d '' -u "$fd" path 2>&"$dfd" || rc=$?
        if [ "$rc" -ne 0 ]; then
            exec {fd}<&-; exec {dfd}>&-
            wpi_require_empty_file B1 "metadata_unreadable path=$site detail=enumeration_read_error" "$diag"
            [ -z "$path" ] || wpi_stop B1 "metadata_unreadable path=$site detail=unterminated_nul_record"
            break
        fi
        entries=$(( entries + 1 ))
        wpi_require_observed_path_grammar B1 "$path" metadata_enumeration
        base="${path##*/}"; fmt=""
        case "$base" in
            *.dist-info) fmt=dist_info ;;
            *.egg-info) fmt=egg_info ;;
            *.egg-link) fmt=egg_link ;;
            *.egg) fmt=egg ;;
            *.pth) fmt=pth ;;
            *.zip) fmt=zip ;;
            *.whl) fmt=whl ;;
            sitecustomize.py|usercustomize.py) fmt=startup_hook ;;
        esac
        if [ -z "$fmt" ]; then ignored=$(( ignored + 1 )); continue; fi
        [ "$fmt" = dist_info ] || wpi_stop B1 "metadata_universe_unexpected stage=preflight $WPI_PATH_FIELD format=$fmt"
        wpi_lstat B1 "$path" metadata_unreadable
        [ "$WPI_META_KIND" != absent ] || wpi_stop B1 "metadata_unreadable $WPI_PATH_FIELD detail=object_disappeared_after_complete_enumeration"
        if [ "$WPI_META_KIND" != directory ]; then
            wpi_kind_token "$WPI_META_KIND"
            wpi_stop B1 "metadata_universe_unexpected stage=preflight $WPI_PATH_FIELD format=dist_info_kind_$WPI_LINE"
        fi
        [ "$WPI_META_OWNER" = 0:0 ] || wpi_stop B1 "metadata_unreadable $WPI_PATH_FIELD owner_numeric=$WPI_META_OWNER expected=0:0"
        count=$(( count + 1 ))
        wpi_walk_components B1 "$path" directory "" 0:0 path_absent path_metadata_mismatch fail path_binding_not_evaluable metadata_unreadable
        for member in METADATA RECORD; do
            wpi_lstat B1 "$path/$member" metadata_unreadable
            [ "$WPI_META_KIND" != absent ] || wpi_fail B1 "distribution_metadata_absent $WPI_PATH_FIELD"
            case "$WPI_META_KIND" in
                'regular file'|'regular empty file') : ;;
                *) wpi_kind_token "$WPI_META_KIND"; wpi_stop B1 "metadata_unreadable $WPI_PATH_FIELD detail=kind_$WPI_LINE" ;;
            esac
            [ "$WPI_META_OWNER" = 0:0 ] || wpi_stop B1 "metadata_unreadable $WPI_PATH_FIELD owner_numeric=$WPI_META_OWNER expected=0:0"
            wpi_sha_file B1 metadata_unreadable "$path/$member"
            WPI_MEMBER_DIGEST="$WPI_LINE"
            wpi_render_path "$path/$member"
            printf 'B1_metadata_readable %s bytes_digest=sha256:%s content=not_printed binding=window_open_pending_close\n' "$WPI_PATH_FIELD" "$WPI_MEMBER_DIGEST"
        done
    done
    wpi_mount_guard_end
    [ "$count" -ge 1 ] || wpi_stop B1 "metadata_unreadable path=$site detail=no_dist_info_directories"
    WPI_METADATA_READABLE=yes
    printf 'B1_metadata_universe root=%s entries=%s dist_info_dirs=%s non_metadata_entries=%s enumeration=unfiltered_maxdepth_1 universe=explicit_dist_info_only\n' \
        "$site" "$entries" "$count" "$ignored"
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

# The subject venv never arbitrates its own package state (Codex F1). Round 3 ran
# `<venv>/bin/python -I verify_lock.py`; -I does not imply -S, so `site` still
# imported and one executable line in that venv's own site-packages/*.pth - or a
# sitecustomize.py beside it - ran with this process's authority, could print
# `verify_lock: PASS: lock+installed; packages=56` and exit 0 before the digest-bound
# verifier was ever compiled, and could write anywhere `gatea` can write.
#
# The adjudicator is now the pinned system interpreter under -I -S. The venv
# contributes exactly one thing: an explicit metadata DIRECTORY passed as argv. It is
# never on sys.path, so no venv module is importable and no venv startup
# configuration is read. The driver refuses to proceed unless its own startup is
# provably isolated and site-free, replaces importlib.metadata's implicit sys.path
# discovery with the one explicit universe defined by the row-19 preflight, and only
# then compiles and runs the digest-bound verifier source under __main__.
#
# Admission is not adjudication (Codex round-4 finding 2). The row-19 preflight and
# the driver's own scan prove object kind, ownership, byte readability and format -
# none of which is the object's package IDENTITY. verify_lock.py:68-74 skips every
# distribution whose METADATA carries no Name and overwrites duplicate canonical
# names in a dict, so an admitted-but-malformed object silently leaves the universe
# it was admitted into and parity can print the accepting line for a set it never
# adjudicated. The driver therefore establishes exactly one grammar-valid Name and
# Version per admitted object, and a unique canonical name across them, BEFORE any
# distribution object is handed to the verifier. Absent, ambiguous, unparseable or
# duplicate identity is an inability to evaluate: rc 6, STOP - never a silent
# omission and never a named-mismatch FAIL.
wpi_assert_lock_parity() {
    local verifier="$WPI_RELEASE_ROOT/IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py"
    local lock="$WPI_RELEASE_ROOT/IBKR_PAPER_BRIDGE/requirements.lock"
    local site="$WPI_VENV_ROOT/lib/python3.12/site-packages" err fields ufmt udigest
    [ "$WPI_METADATA_READABLE" = yes ] || wpi_stop B1 "verifier_not_evaluable rc=3 detail=metadata_preflight_not_complete"
    wpi_assert_regular_digest B1 verifier_absent verifier_digest_mismatch "$verifier" 3735 "$WPI_VERIFY_LOCK_SHA256" verifier verifier_object_unexpected with_path
    wpi_capture lock_parity "$WPI_PYTHON3" -I -S -c '
import email,hashlib,os,re,sys
def die(code,token,extra=""):
 sys.stderr.write("verify_lock_driver: "+token+extra+chr(10)); sys.exit(code)
if not (sys.flags.isolated and sys.flags.no_site): die(4,"trusted_startup_unproven")
for m in ("site","sitecustomize","usercustomize"):
 if m in sys.modules: die(4,"trusted_startup_unproven")
site_dir=sys.argv[1]; verifier=sys.argv[2]; lock=sys.argv[3]
import importlib.metadata as M
import importlib.machinery as MM
from pathlib import Path
REJECT=((".egg-info","egg_info"),(".egg-link","egg_link"),(".egg","egg"),(".pth","pth"),(".zip","zip"),(".whl","whl"))
accepted=[]
try:
 names=sorted(os.listdir(site_dir))
except OSError:
 die(4,"universe_unreadable")
for n in names:
 h=hashlib.sha256(n.encode("utf-8","surrogateescape")).hexdigest()
 if n in ("sitecustomize.py","usercustomize.py"): die(5,"universe_unexpected"," format=startup_hook name_sha256="+h)
 if n.endswith(".dist-info"):
  p=os.path.join(site_dir,n)
  if os.path.islink(p) or not os.path.isdir(p): die(5,"universe_unexpected"," format=dist_info_not_directory name_sha256="+h)
  accepted.append(Path(p)); continue
 for suf,tok in REJECT:
  if n.endswith(suf): die(5,"universe_unexpected"," format="+tok+" name_sha256="+h)
if not accepted: die(4,"universe_empty")
NAME_RE=re.compile("[A-Za-z0-9]([A-Za-z0-9._-]*[A-Za-z0-9])?")
VER_RE=re.compile("[0-9][0-9A-Za-z.!+_-]*")
canon={}
for p in accepted:
 h=hashlib.sha256(p.name.encode("utf-8","surrogateescape")).hexdigest()
 t=" name_sha256="+h
 try:
  raw=(p/"METADATA").read_bytes()
 except OSError:
  die(6,"distribution_identity_unestablished"," detail=metadata_unreadable"+t)
 msg=email.message_from_string(raw.decode("utf-8","surrogateescape"))
 nm=msg.get_all("Name") or []
 vs=msg.get_all("Version") or []
 if len(nm)!=1: die(6,"distribution_identity_unestablished"," detail=name_"+("absent" if not nm else "ambiguous")+t)
 if len(vs)!=1: die(6,"distribution_identity_unestablished"," detail=version_"+("absent" if not vs else "ambiguous")+t)
 nv=str(nm[0]).strip(); vv=str(vs[0]).strip()
 if not NAME_RE.fullmatch(nv): die(6,"distribution_identity_unestablished"," detail=name_grammar"+t)
 if not VER_RE.fullmatch(vv): die(6,"distribution_identity_unestablished"," detail=version_grammar"+t)
 c=re.sub("[-_.]+","-",nv).lower()
 if c in canon: die(6,"distribution_identity_unestablished"," detail=canonical_name_duplicate"+t)
 canon[c]=h
D=[M.PathDistribution(p) for p in accepted]
M.distributions=lambda **kw: iter(list(D))
M.Distribution.discover=staticmethod(lambda **kw: iter(list(D)))
MM.PathFinder.find_distributions=staticmethod(lambda *a,**k: iter(()))
with open(verifier,"rb") as f: src=f.read()
sys.argv=[verifier,"--lock",lock,"--check-installed"]
exec(compile(src,verifier,"exec"),{"__name__":"__main__","__file__":verifier})
' "$site" "$verifier" "$lock"
    if [ "$WPI_CAP_RC" -eq 0 ]; then
        wpi_require_empty_file B1 "verifier_not_evaluable rc=0" "$WPI_CAP_ERR"
        wpi_single_record B1 "verifier_not_evaluable rc=0" "$WPI_CAP_OUT"
        [ "$WPI_LINE" = "verify_lock: PASS: lock+installed; packages=$WPI_EXPECTED_PACKAGES" ] \
            || wpi_stop B1 "verifier_not_evaluable rc=0 detail=pass_grammar"
        printf 'B1_lock_parity result=pass packages=%s output=structurally_parsed verifier_preexec_binding=component_mount_digest_window_closed exec_binding=separate_bounded_exec adjudicator=pinned_system_interpreter isolation=isolated_no_site discovery=explicit_dist_info_universe\n' "$WPI_EXPECTED_PACKAGES"
        return 0
    fi
    wpi_require_empty_file B1 "verifier_not_evaluable rc=$WPI_CAP_RC detail=unexpected_stdout" "$WPI_CAP_OUT"
    wpi_single_record B1 "verifier_not_evaluable rc=$WPI_CAP_RC" "$WPI_CAP_ERR"
    err="$WPI_LINE"
    if [ "$WPI_CAP_RC" -eq 5 ]; then
        case "$err" in
            'verify_lock_driver: universe_unexpected format='*' name_sha256='*)
                # The driver is trusted, but its two rendered fields are still parsed
                # under their exact grammar before they enter an evidence line.
                fields="${err#verify_lock_driver: universe_unexpected }"
                ufmt="${fields%% *}"; udigest="${fields#* }"
                case "$ufmt" in format=[a-z][a-z_0-9]*) : ;; *) wpi_stop B1 "verifier_not_evaluable rc=5 detail=driver_grammar diagnostic_file=$WPI_CAP_ERR" ;; esac
                case "$udigest" in name_sha256=?*) : ;; *) wpi_stop B1 "verifier_not_evaluable rc=5 detail=driver_grammar diagnostic_file=$WPI_CAP_ERR" ;; esac
                case "${udigest#name_sha256=}" in ''|*[!0-9a-f]*) wpi_stop B1 "verifier_not_evaluable rc=5 detail=driver_grammar diagnostic_file=$WPI_CAP_ERR" ;; esac
                [ "${#udigest}" -eq 76 ] || wpi_stop B1 "verifier_not_evaluable rc=5 detail=driver_grammar diagnostic_file=$WPI_CAP_ERR"
                wpi_stop B1 "metadata_universe_unexpected stage=verifier $ufmt $udigest" ;;
            *) wpi_stop B1 "verifier_not_evaluable rc=5 detail=driver_grammar diagnostic_file=$WPI_CAP_ERR" ;;
        esac
    fi
    if [ "$WPI_CAP_RC" -eq 6 ]; then
        case "$err" in
            'verify_lock_driver: distribution_identity_unestablished detail='*' name_sha256='*)
                fields="${err#verify_lock_driver: distribution_identity_unestablished }"
                ufmt="${fields%% *}"; udigest="${fields#* }"
                case "$ufmt" in detail=[a-z][a-z_0-9]*) : ;; *) wpi_stop B1 "verifier_not_evaluable rc=6 detail=driver_grammar diagnostic_file=$WPI_CAP_ERR" ;; esac
                case "$udigest" in name_sha256=?*) : ;; *) wpi_stop B1 "verifier_not_evaluable rc=6 detail=driver_grammar diagnostic_file=$WPI_CAP_ERR" ;; esac
                case "${udigest#name_sha256=}" in ''|*[!0-9a-f]*) wpi_stop B1 "verifier_not_evaluable rc=6 detail=driver_grammar diagnostic_file=$WPI_CAP_ERR" ;; esac
                [ "${#udigest}" -eq 76 ] || wpi_stop B1 "verifier_not_evaluable rc=6 detail=driver_grammar diagnostic_file=$WPI_CAP_ERR"
                wpi_stop B1 "metadata_identity_unestablished stage=verifier $ufmt $udigest" ;;
            *) wpi_stop B1 "verifier_not_evaluable rc=6 detail=driver_grammar diagnostic_file=$WPI_CAP_ERR" ;;
        esac
    fi
    if [ "$WPI_CAP_RC" -eq 4 ]; then
        case "$err" in
            'verify_lock_driver: trusted_startup_unproven'|'verify_lock_driver: universe_unreadable'|'verify_lock_driver: universe_empty')
                wpi_stop B1 "verifier_not_evaluable rc=4 detail=${err#verify_lock_driver: }" ;;
            *) wpi_stop B1 "verifier_not_evaluable rc=4 detail=driver_grammar diagnostic_file=$WPI_CAP_ERR" ;;
        esac
    fi
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

# Two phases, and the boundary between them is the finding (Codex F2). Round 3 called
# wpi_fail from inside the read loop, so an early wildcard row produced a host-state
# FAIL while a later malformed row was never read: reversing two records changed rc 1
# to rc 3 although neither ordering was evaluable. Phase 1 now reads to clean EOF and
# records only sanitised counters and flags; a grammar, read or termination failure is
# still an immediate STOP, because that is an inability to evaluate rather than an
# observation. Phase 2 applies the wildcard, unexpected-address and count FAILs only
# after reader diagnostics, record termination and table grammar have all held.
# One dotted quad, every octet complete and in range, no leading zeros. `ss -n`
# emits canonical decimal, so a token that is not exactly that did not come from
# the instrument this row claims to have read.
wpi_ipv4_ok() {
    local rest="$1" o n=0
    case "$1" in ''|*[!0-9.]*|.*|*.|*..*) return 1 ;; esac
    while : ; do
        case "$rest" in *.*) o="${rest%%.*}"; rest="${rest#*.}" ;; *) o="$rest"; rest="" ;; esac
        n=$(( n + 1 ))
        [ "${#o}" -le 3 ] || return 1
        case "$o" in 0|[1-9]*) : ;; *) return 1 ;; esac
        [ "$o" -le 255 ] || return 1
        [ "$n" -le 4 ] || return 1
        [ -n "$rest" ] || break
    done
    [ "$n" -eq 4 ]
}

# The group count of one colon-separated IPv6 run, or rc 1 if any group is not
# 1-4 hex digits (or, as the FINAL group only, a complete dotted quad worth two).
wpi_ipv6_groups() {
    local rest="$1" piece n=0
    WPI_LINE=0
    [ -n "$rest" ] || return 0
    while : ; do
        case "$rest" in *:*) piece="${rest%%:*}"; rest="${rest#*:}" ;; *) piece="$rest"; rest="" ;; esac
        [ -n "$piece" ] || return 1
        case "$piece" in
            *.*) wpi_ipv4_ok "$piece" || return 1; n=$(( n + 2 )); [ -z "$rest" ] || return 1 ;;
            *)   [ "${#piece}" -le 4 ] || return 1
                 case "$piece" in *[!0-9A-Fa-f]*) return 1 ;; esac
                 n=$(( n + 1 )) ;;
        esac
        [ "$n" -le 8 ] || return 1
        [ -n "$rest" ] || break
    done
    WPI_LINE="$n"
}

# One IPv6 literal: at most one `::`, eight groups without it, fewer than eight
# with it, an optional interface zone.
wpi_ipv6_ok() {
    local s="$1" zone head tail hn
    case "$s" in
        *%*) zone="${s##*%}"; s="${s%%%*}"
             [ -n "$zone" ] || return 1
             case "$zone" in *[!A-Za-z0-9_.-]*) return 1 ;; esac ;;
    esac
    case "$s" in *:*) : ;; *) return 1 ;; esac
    case "$s" in *[!0-9A-Fa-f:.]*) return 1 ;; esac
    case "$s" in *::*::*) return 1 ;; esac
    case "$s" in
        *::*)
            head="${s%%::*}"; tail="${s#*::}"
            wpi_ipv6_groups "$head" || return 1; hn="$WPI_LINE"
            wpi_ipv6_groups "$tail" || return 1
            [ $(( hn + WPI_LINE )) -le 7 ] || return 1 ;;
        *)
            wpi_ipv6_groups "$s" || return 1
            [ "$WPI_LINE" -eq 8 ] || return 1 ;;
    esac
    return 0
}

# One `ss -n` endpoint token, split at the last colon and then validated on both
# sides. Round 5 required only that the address half contain a colon and that the
# port half be decimal digits, so `nonsense:8790` was adjudicated as an observed
# non-preregistered listener and `127.0.0.1:99999` as an observed absence of the
# preregistered one - two host-state FAILs derived from records that state no
# address and no port (Codex round-5 part B finding 1). An endpoint the block
# cannot parse is an inability to evaluate the row, never an observation.
wpi_require_endpoint() {
    local token="$1" role="$2" addr port inner
    local reason="listener_inventory_unreadable_or_unparseable rc=0"
    case "$token" in *:*) port="${token##*:}"; addr="${token%:*}" ;;
        *) wpi_stop B6 "$reason detail=${role}_endpoint_grammar" ;; esac
    case "$port" in
        '*') [ "$role" = peer ] || wpi_stop B6 "$reason detail=${role}_port_grammar" ;;
        ''|*[!0-9]*) wpi_stop B6 "$reason detail=${role}_port_grammar" ;;
        *)  [ "${#port}" -le 5 ] || wpi_stop B6 "$reason detail=${role}_port_grammar"
            case "$port" in 0|[1-9]*) : ;; *) wpi_stop B6 "$reason detail=${role}_port_grammar" ;; esac
            [ "$port" -le 65535 ] || wpi_stop B6 "$reason detail=${role}_port_range port=$port" ;;
    esac
    case "$addr" in
        '') wpi_stop B6 "$reason detail=${role}_address_grammar" ;;
        '*') : ;;
        '['*']') inner="${addr#[}"; inner="${inner%]}"
                 wpi_ipv6_ok "$inner" || wpi_stop B6 "$reason detail=${role}_address_grammar" ;;
        *:*) wpi_ipv6_ok "$addr" || wpi_stop B6 "$reason detail=${role}_address_grammar" ;;
        *) wpi_ipv4_ok "$addr" || wpi_stop B6 "$reason detail=${role}_address_grammar" ;;
    esac
    WPI_EP_ADDR="$addr"; WPI_EP_PORT="$port"
}

wpi_assert_listener_set() {
    local fd rc=0 count=0 total=0 consumed=0 whole="" rest="" line
    local state recvq sendq localaddr peer addr port diag dfd
    local port_rows=0 wildcard_seen=no wildcard_addr="" unexpected_seen=no
    wpi_capture listeners "$WPI_SS" -H -ltn
    [ "$WPI_CAP_RC" -eq 0 ] || wpi_stop B6 "listener_inventory_unreadable_or_unparseable rc=$WPI_CAP_RC detail=ss_failed"
    wpi_require_empty_file B6 "listener_inventory_unreadable_or_unparseable rc=0" "$WPI_CAP_ERR"
    wpi_alloc_read_diag listener_rows; diag="$WPI_READ_DIAG"; dfd="$WPI_READ_DIAG_FD"
    # Phase 0, and it is the reason this reader was rewritten. `IFS= read -r line`
    # silently DISCARDS NUL bytes, so the record `LIS<NUL>TEN ...` was consumed as
    # `LISTEN ...`: the reader repaired a malformed record into a conformant one
    # and the block printed both `parse=complete_before_semantics` and the
    # accepting listener-set line (Codex round-5 part B finding 1). Normalising a
    # record is not parsing it. The whole inventory is therefore taken in ONE
    # NUL-delimited read: that read returns 0 only when it actually found a NUL -
    # the single byte class the record reader cannot represent - and otherwise
    # returns EOF with every captured byte in `whole`. Records are then split out
    # of that one string in memory, so there is no second open, no second pass and
    # no byte that can vanish between the capture and the grammar. The closing
    # equation `consumed == ${#whole}` is the conservation check for that claim.
    #
    # Round 6 still opened `$WPI_CAP_OUT` by NAME here, so "the byte string
    # adjudicated is the byte string captured" was false the moment anything
    # replaced that name between the child's exit and this open: an executed
    # fixture swapped a wildcard capture for a loopback one and this row PASSed
    # (Codex round-6 part B finding 3). The read is therefore bound to the
    # descriptor `wpi_capture` re-derived from its own creating write
    # descriptor, which resolved no name after the child ran. This is the one
    # reader whose bytes row 22 claims identity for, which is why it is the one
    # reader bound this way.
    fd="$WPI_CAP_OUT_FD"
    [ -n "$fd" ] || wpi_stop B6 "listener_inventory_unreadable_or_unparseable rc=0 detail=capture_stream_unbound"
    IFS= read -r -d '' -u "$fd" whole 2>&"$dfd" || rc=$?
    exec {dfd}>&-
    wpi_require_empty_file B6 "listener_inventory_unreadable_or_unparseable rc=0 detail=hard_read_error" "$diag"
    [ "$rc" -ne 0 ] || wpi_stop B6 "listener_inventory_unreadable_or_unparseable rc=0 detail=nul_byte_in_inventory"
    case "$whole" in *[![:print:]$'\t\n']*) wpi_stop B6 "listener_inventory_unreadable_or_unparseable rc=0 detail=inventory_charset" ;; esac
    rest="$whole"
    while [ -n "$rest" ]; do
        case "$rest" in
            *$'\n'*) line="${rest%%$'\n'*}"; rest="${rest#*$'\n'}" ;;
            *) wpi_stop B6 "listener_inventory_unreadable_or_unparseable rc=0 detail=unterminated_final_record" ;;
        esac
        consumed=$(( consumed + ${#line} + 1 ))
        [ -n "$line" ] || wpi_stop B6 "listener_inventory_unreadable_or_unparseable rc=0 detail=blank_record"
        set -- $line
        [ "$#" -eq 5 ] \
            || wpi_stop B6 "listener_inventory_unreadable_or_unparseable rc=0 detail=table_grammar"
        state="$1"; recvq="$2"; sendq="$3"; localaddr="$4"; peer="$5"
        [ "$state" = LISTEN ] || wpi_stop B6 "listener_inventory_unreadable_or_unparseable rc=0 detail=state_grammar"
        # Each queue field separately, and each nonempty decimal digits. Round 6
        # validated the CONCATENATION `"$recvq:$sendq"` against a class that
        # permits the separator itself, so `recvq=:` and `sendq=12:34` were both
        # admitted as structurally complete and reached the accepting listener
        # line (Codex round-6 part B finding 2). Validating a joined string is
        # not validating its fields.
        case "$recvq" in ''|*[!0-9]*) wpi_stop B6 "listener_inventory_unreadable_or_unparseable rc=0 detail=queue_grammar" ;; esac
        case "$sendq" in ''|*[!0-9]*) wpi_stop B6 "listener_inventory_unreadable_or_unparseable rc=0 detail=queue_grammar" ;; esac
        case "$localaddr:$peer" in *[![:graph:]]*) wpi_stop B6 "listener_inventory_unreadable_or_unparseable rc=0 detail=address_character_grammar" ;; esac
        wpi_require_endpoint "$localaddr" local; addr="$WPI_EP_ADDR"; port="$WPI_EP_PORT"
        wpi_require_endpoint "$peer" peer
        total=$(( total + 1 ))
        [ "$port" = 8790 ] || continue
        port_rows=$(( port_rows + 1 ))
        # Sanitised counters only. No semantic verdict may leave this loop: the table
        # is not yet proven complete, so no row seen so far is yet evidence of state.
        case "$addr" in
            '*'|0.0.0.0|'[::]'|'::'|"172.24.55.233")
                if [ "$wildcard_seen" = no ]; then wildcard_seen=yes; wildcard_addr="$addr"; fi
                continue ;;
        esac
        if [ "$addr" != 127.0.0.1 ]; then unexpected_seen=yes; continue; fi
        count=$(( count + 1 ))
    done
    [ "$consumed" -eq "${#whole}" ] || wpi_stop B6 "listener_inventory_unreadable_or_unparseable rc=0 detail=record_bytes_unaccounted consumed=$consumed captured=${#whole}"
    # Phase 2. Reader diagnostics, record termination, byte conservation and table
    # grammar have all held for every row, so the inventory is a complete
    # observation and the recorded counters may now be adjudicated.
    printf 'B6_listener_inventory rows=%s port_8790_rows=%s bytes=%s evidence_file=%s content=not_printed table=complete parse=complete_before_semantics read_binding=capture_descriptor scope_applied_in_block=yes\n' \
        "$total" "$port_rows" "$consumed" "$WPI_CAP_OUT"
    [ "$wildcard_seen" = no ] || wpi_fail B6 "nonloopback_listener addr=$wildcard_addr"
    [ "$unexpected_seen" = no ] || wpi_fail B6 "listener_set_unexpected observed=non_preregistered_address expected=1x127.0.0.1:8790"
    [ "$count" -eq 1 ] || wpi_fail B6 "listener_set_unexpected observed_count=$count expected=1x127.0.0.1:8790"
    printf 'B6_listener_set port=8790 count=1 local=127.0.0.1 wildcard=none table=complete\n'
}

# The preregistered type of one row-21 field, from the single schema declaration
# the child is also held to. rc 1 for any name that is not a member: a result
# record naming a field outside the declared universe was produced by something
# other than this block's own parser over this block's own schema.
wpi_status_expected_type() {
    local field="$1" entry
    for entry in $WPI_STATUS_SCHEMA; do
        case "$entry" in "$field":*) WPI_LINE="${entry#*:}"; return 0 ;; esac
    done
    return 1
}

wpi_assert_status() {
    local body="$EV_DIR/ro.status.body" code_file json_out json_err record
    wpi_alloc_leaf "$body"
    wpi_capture status_get "$WPI_CURL" --silent --show-error --connect-timeout 5 --max-time 10 \
        --request GET --output "$body" --write-out '%{http_code}\n' -- "$WPI_CONTROL_ENDPOINT"
    [ "$WPI_CAP_RC" -eq 0 ] || wpi_stop B5 "status_endpoint_not_evaluable rc=$WPI_CAP_RC detail=transport_error diagnostic_file=$WPI_CAP_ERR"
    wpi_require_empty_file B5 "status_endpoint_not_evaluable rc=0" "$WPI_CAP_ERR"
    wpi_single_record B5 "status_endpoint_not_evaluable rc=0" "$WPI_CAP_OUT"
    # Round 5 read every three-digit string as a completed HTTP response, so
    # curl's no-response sentinel `000` and the out-of-range `600` were both
    # reported as observed endpoint deviations at rc 1 (Codex round-5 part B
    # finding 3). Section 8.2 permits FAIL only for a complete, valid non-200
    # response; a token outside 100-599 is not a status line the endpoint sent,
    # it is the absence of one.
    case "$WPI_LINE" in
        401|403) wpi_stop B5 "status_endpoint_access_denied code=$WPI_LINE" ;;
        200) : ;;
        000) wpi_stop B5 "status_endpoint_not_evaluable rc=0 detail=http_code_no_response code=000" ;;
        [1-5][0-9][0-9]) wpi_fail B5 "status_endpoint_unexpected_http code=$WPI_LINE" ;;
        *) wpi_stop B5 "status_endpoint_not_evaluable rc=0 detail=http_code_grammar" ;;
    esac
    wpi_sha_file B5 status_body_unreadable_or_unparseable "$body"; WPI_BODY_SHA="$WPI_LINE"
    # The status parser needs no venv context whatever - it opens one file and parses
    # JSON with the standard library - so it runs under the pinned system interpreter
    # with -I -S. Under round 3's `<venv>/bin/python -I`, `site` still imported and a
    # single executable line in that venv's site-packages/*.pth could print exactly
    # `OK fields=8` and exit 0 before this source was compiled. The guard below makes
    # the isolation a checked precondition of the parse rather than a claim.
    wpi_capture status_json "$WPI_PYTHON3" -I -S -c '
import hashlib,json,sys
if not (sys.flags.isolated and sys.flags.no_site): print("PARSE startup_not_isolated"); sys.exit(3)
for _m in ("site","sitecustomize","usercustomize"):
 if _m in sys.modules: print("PARSE startup_hook_present"); sys.exit(3)
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
 if dict(p.split(":",1) for p in sys.argv[2].split()) != dict((k,t.__name__) for k,(t,v) in expected.items()): print("PARSE schema_declaration_mismatch"); sys.exit(3)
 for k,(t,v) in expected.items():
  if k not in obj: print("MISSING "+k); sys.exit(4)
  if type(obj[k]) is not t: print("TYPE %s %s %s"%(k,type(obj[k]).__name__,t.__name__)); sys.exit(5)
  if obj[k] != v:
   h=hashlib.sha256(json.dumps(obj[k],sort_keys=True,separators=(",",":"),ensure_ascii=True).encode()).hexdigest()
   print("MISMATCH %s %s"%(k,h)); sys.exit(1)
 print("OK fields=8")
except (OSError,UnicodeError,json.JSONDecodeError,Dup,ValueError,IndexError) as e:
 print("PARSE "+type(e).__name__); sys.exit(3)
' "$body" "$WPI_STATUS_SCHEMA"
    wpi_require_empty_file B5 "status_body_unreadable_or_unparseable detail=parser_stderr" "$WPI_CAP_ERR"
    wpi_single_record B5 "status_body_unreadable_or_unparseable" "$WPI_CAP_OUT"
    record="$WPI_LINE"
    # Every result record is reconstructed from its own tokens and compared to the
    # bytes the child actually emitted, so a record is admitted only in the exact
    # shape one of the four `print` statements above can produce. Round 5 checked
    # the character class and nothing else: `TYPE state str` - three tokens, no
    # expected type - was classified as a completed flag deviation and returned
    # rc 1 with `expected_type=` empty, and `MISMATCH state abc` did the same with
    # a three-character digest (Codex round-5 part B finding 2). rc 1 means a
    # completed probe established deviant host state; it must not be reachable
    # from a producer result the producer could not have produced.
    case "$WPI_CAP_RC:$record" in
        '0:OK fields=8') printf 'B5_status http=200 json=strict required_fields=8 flags=expected body_sha256=%s content=not_printed parser=pinned_system_interpreter isolation=isolated_no_site\n' "$WPI_BODY_SHA" ;;
        4:'MISSING '*)
            set -- $record
            [ "$#" -eq 2 ] || wpi_stop B5 "status_body_unreadable_or_unparseable detail=missing_record_grammar tokens=$#"
            [ "MISSING $2" = "$record" ] || wpi_stop B5 "status_body_unreadable_or_unparseable detail=missing_record_grammar"
            wpi_status_expected_type "$2" || wpi_stop B5 "status_body_unreadable_or_unparseable detail=missing_record_field"
            wpi_stop B5 "schema_unexpected field=$2" ;;
        5:'TYPE '*)
            set -- $record
            [ "$#" -eq 4 ] || wpi_stop B5 "status_body_unreadable_or_unparseable detail=type_record_grammar tokens=$#"
            [ "TYPE $2 $3 $4" = "$record" ] || wpi_stop B5 "status_body_unreadable_or_unparseable detail=type_record_grammar"
            wpi_status_expected_type "$2" || wpi_stop B5 "status_body_unreadable_or_unparseable detail=type_record_field"
            [ "$4" = "$WPI_LINE" ] || wpi_stop B5 "status_body_unreadable_or_unparseable detail=type_record_expected_type field=$2"
            case "$3" in str|int|float|bool|list|dict|NoneType) : ;; *) wpi_stop B5 "status_body_unreadable_or_unparseable detail=type_record_observed_type" ;; esac
            [ "$3" != "$4" ] || wpi_stop B5 "status_body_unreadable_or_unparseable detail=type_record_not_a_deviation field=$2"
            wpi_fail B5 "flag_mismatch field=$2 observed_type=$3 expected_type=$4" ;;
        1:'MISMATCH '*)
            set -- $record
            [ "$#" -eq 3 ] || wpi_stop B5 "status_body_unreadable_or_unparseable detail=mismatch_record_grammar tokens=$#"
            [ "MISMATCH $2 $3" = "$record" ] || wpi_stop B5 "status_body_unreadable_or_unparseable detail=mismatch_record_grammar"
            wpi_status_expected_type "$2" || wpi_stop B5 "status_body_unreadable_or_unparseable detail=mismatch_record_field"
            [ "${#3}" -eq 64 ] || wpi_stop B5 "status_body_unreadable_or_unparseable detail=mismatch_record_digest"
            case "$3" in *[!0-9a-f]*) wpi_stop B5 "status_body_unreadable_or_unparseable detail=mismatch_record_digest" ;; esac
            wpi_fail B5 "flag_mismatch field=$2 observed_sha256=$3 expected=preregistered_typed_value" ;;
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

    # Establish the deploy-attested projection before the first tool/object
    # probe. Keep the window open through tool, evidence-leaf and manager
    # preflight binding; any FAIL closes it through wpi_fail first.
    wpi_mount_guard_begin
    # ALL TEN pins are bound here, inside that window, and the tenth is the
    # trusted adjudicating python3. Round 4 accepted the tenth pin, added it to
    # projection v2 and defined its binding, but never passed it through this
    # loop: the executable ran at both adjudicators while `-I -S`, the startup
    # guards and every `pinned_system_interpreter` token rested on an object no
    # production line had ever bound (Codex round-4 finding 1). Those flags are
    # only meaningful once the program that interprets them is the bound one.
    for wpi_tool in stat readlink env find sha256sum systemctl ss curl timeout python3; do
        wpi_map_get "$WPI_TOOL_PINS" "$wpi_tool"
        wpi_bind_tool "$wpi_tool" "$WPI_LINE"
    done

    wpi_assert_evidence_leaf_bound

    # STOP-first preflight: no filesystem, parity, curl, or ss comparison is
    # reachable until the intended system manager has answered.
    wpi_assert_manager_ready
    wpi_mount_guard_end

    printf 'RP7_SECTION B3_rows_10_15\n'
    wpi_assert_tree "$WPI_RELEASE_ROOT" release
    wpi_assert_tree "$WPI_VENV_ROOT" venv
    wpi_assert_metadata_dir "$WPI_CONF_DIR" 0:0
    wpi_assert_metadata_dir "$WPI_STATE_DIR" "$WPI_STATE_UID:$WPI_STATE_GID"
    wpi_assert_metadata_dir "$WPI_LOG_DIR" "$WPI_STATE_UID:$WPI_STATE_GID"

    printf 'RP7_SECTION B1a_row_17\n'
    wpi_assert_regular_digest B1a installed_lock_absent installed_lock_digest_mismatch \
        "$WPI_RELEASE_ROOT/IBKR_PAPER_BRIDGE/requirements.lock" \
        "$WPI_EXPECTED_LOCK_BYTES" "$WPI_EXPECTED_LOCK_SHA256" installed_lock installed_lock_object_unexpected kind_only

    printf 'RP7_SECTION B1_rows_18_19\n'
    wpi_assert_interpreter
    wpi_assert_metadata_readable
    wpi_assert_lock_parity

    printf 'RP7_SECTION B5_B6_rows_20_24\n'
    # ONE inversion is preregistered and it is only the row-22 service-netns
    # PREFLIGHT: that binding precedes every curl and ss interpretation even though
    # its display number is later. Round 3 also moved the whole listener adjudication
    # ahead of rows 20-21, which is not preregistered and made a listener FAIL
    # pre-empt an independently present endpoint or flag deviation (Codex F4). The
    # preregistered first-divergence order is restored below: netns binding, then
    # B5 rows 20-21, then B6 rows 22-23.
    wpi_assert_netns_binding
    wpi_assert_status
    wpi_assert_listener_set
    wpi_record_external_probe_boundary

    printf 'RP7_claim establishes=rows_10_23_read_only_predicates_with_attested_preexec_objects_and_service_network_domain;executed_objects_use_separate_bounded_exec_after_preexec_mount_window\n'
    printf 'RP7_claim does_not_establish=row_24_operator_side_result,ACL_or_capability_immutability,whole_tree_byte_identity,root_deferred_checks,group_C,host_authority\n'
    printf 'RP7 PASS\n'
}

wpi_main "$@"
