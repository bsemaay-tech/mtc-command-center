# ===== BLOCK-ID: RP0-LIB ===== [EXECUTABLE PROPOSAL BLOCK]
# WP-L Phase 2 — shared evidence + predicate bootstrap library (PROPOSED DESIGN).
# Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b (credential-free DISARMED).
# NOT host-authorized. Definitions only: sourcing this block performs no filesystem,
# service, network, credential or economic action.
#
# rc contract for every predicate defined here:
#   0 = TRUE   1 = FALSE   3 = COULD NOT EVALUATE (always STOP)
RP0_STOP_RC=3

rp0_stop() { printf 'RP0_STOP reason=%s\n' "$*" >&2; return "$RP0_STOP_RC"; }
rp0_fail() { printf 'RP0_FAIL reason=%s\n' "$*" >&2; return 1; }
rp0_note() { printf 'RP0_NOTE %s\n' "$*"; }

# --- monotonic clock -------------------------------------------------------
# Wall-clock seconds are not a bound. /proc/uptime is monotonic; if it cannot be
# read, elapsed time COULD NOT BE EVALUATED and the caller must STOP.
rp0_monotonic_ms() {
    local up rest
    read -r up rest < /proc/uptime || { rp0_stop "monotonic_clock_unreadable"; return 3; }
    LC_ALL=C awk -v u="$up" 'BEGIN { printf "%.0f\n", u * 1000 }'
}

# --- three-outcome path classification -------------------------------------
# Prints exactly one of: absent regular dir link_live link_dangling other
# rc 0 = classified, rc 3 = COULD NOT EVALUATE. A probe error is NEVER "absent",
# and a dangling link is NEVER "absent" — that conflation was defect F1.
# `stat` without -L does not dereference, so a dangling link is still classified.
rp0_probe_path() {
    local p="$1" kind rc=0 err detail
    err="$(mktemp)" || { rp0_stop "probe_tempfile_failed path=$p"; return 3; }
    kind="$(LC_ALL=C stat -c '%F' -- "$p" 2>"$err")" || rc=$?
    if [ "$rc" -eq 0 ]; then
        case "$kind" in
            "symbolic link")
                rc=0
                LC_ALL=C stat -L -c '%F' -- "$p" >/dev/null 2>"$err" || rc=$?
                if [ "$rc" -eq 0 ]; then printf 'link_live\n'; rm -f "$err"; return 0; fi
                detail="$(tr -d '\r\n' <"$err")"; rm -f "$err"
                case "$detail" in
                    *"No such file or directory"*) printf 'link_dangling\n'; return 0 ;;
                esac
                rp0_stop "link_target_probe_error path=$p rc=$rc detail=$detail"; return 3 ;;
            "regular file"|"regular empty file") printf 'regular\n'; rm -f "$err"; return 0 ;;
            "directory")                         printf 'dir\n';     rm -f "$err"; return 0 ;;
            *)                                   printf 'other\n';   rm -f "$err"; return 0 ;;
        esac
    fi
    detail="$(tr -d '\r\n' <"$err")"; rm -f "$err"
    case "$detail" in
        *"No such file or directory"*) printf 'absent\n'; return 0 ;;
    esac
    rp0_stop "path_probe_error path=$p rc=$rc detail=$detail"
    return 3
}

# --- canonical non-link parent with preregistered owner/mode ---------------
# args: <path> <expected owner:group> <expected octal mode>
rp0_require_canonical_dir() {
    local p="$1" want_own="$2" want_mode="${3#0}" kind canon own mode
    kind="$(rp0_probe_path "$p")" || return 3
    case "$kind" in
        dir) : ;;
        absent)                  rp0_fail "evidence_parent_absent path=$p"; return 1 ;;
        link_live|link_dangling) rp0_fail "evidence_parent_is_symlink kind=$kind path=$p"; return 1 ;;
        *)                       rp0_fail "evidence_parent_kind=$kind path=$p"; return 1 ;;
    esac
    canon="$(readlink -f -- "$p")" || { rp0_stop "canonicalization_failed path=$p"; return 3; }
    [ "$canon" = "$p" ] || { rp0_fail "evidence_parent_not_canonical path=$p canonical=$canon"; return 1; }
    own="$(LC_ALL=C stat -c '%U:%G' -- "$p")" || { rp0_stop "owner_probe_failed path=$p"; return 3; }
    mode="$(LC_ALL=C stat -c '%a' -- "$p")"   || { rp0_stop "mode_probe_failed path=$p"; return 3; }
    [ "$own" = "$want_own" ]   || { rp0_fail "evidence_parent_owner=$own expected=$want_own path=$p"; return 1; }
    [ "$mode" = "$want_mode" ] || { rp0_fail "evidence_parent_mode=$mode expected=$want_mode path=$p"; return 1; }
    rp0_note "evidence_parent_ok path=$p owner=$own mode=$mode"
    return 0
}

# --- preregistered identifier must be ONE safe path component --------------
# args: <variable name> <value>
# A run ID or stage ID that carries a separator, `.`, `..`, a leading `-`, or
# any character outside [A-Za-z0-9._-] can place the ACTIVE evidence leaf beside
# or above the directory §1.5 later hashes. Non-empty is not the predicate:
# `EV_STAGE_ID=../escaped` is non-empty and escapes the closed tree, which
# silently defeats the remote/local binding while the run still reports success.
rp0_require_safe_component() {
    local name="$1" val="$2"
    case "$val" in
        ""|"."|"..")       rp0_fail "component_reserved name=$name value=[$val]";     return 1 ;;
        -*)                rp0_fail "component_leading_dash name=$name value=[$val]"; return 1 ;;
        *[!A-Za-z0-9._-]*) rp0_fail "component_charset name=$name value=[$val]";      return 1 ;;
    esac
    rp0_note "component_ok name=$name value=$val"
    return 0
}

# --- prove a derived path is a DIRECT child of the allocated directory -----
# args: <allocated dir> <derived leaf>
# Independent of the string check above, and applied after allocation: the leaf
# must be spelled exactly `<dir>/<basename>`, and its canonical parent must be
# the canonical allocated directory. A symlinked intermediate is therefore
# refused too, even when every literal component looked safe.
rp0_require_leaf_inside() {
    local dir="$1" leaf="$2" base parent canon_dir canon_parent
    base="${leaf##*/}"
    parent="${leaf%/*}"
    [ "$leaf" = "$dir/$base" ] || { rp0_fail "leaf_not_direct_child dir=$dir leaf=$leaf"; return 1; }
    canon_dir="$(readlink -f -- "$dir")"       || { rp0_stop "canonicalization_failed path=$dir";    return 3; }
    canon_parent="$(readlink -f -- "$parent")" || { rp0_stop "canonicalization_failed path=$parent"; return 3; }
    [ "$canon_parent" = "$canon_dir" ] \
        || { rp0_fail "leaf_parent_escapes dir=$canon_dir parent=$canon_parent leaf=$leaf"; return 1; }
    rp0_note "leaf_contained dir=$canon_dir name=$base"
    return 0
}

# --- create-once evidence directory ----------------------------------------
# ONE plain `mkdir -m 0700`. Never `mkdir -p`: a missing intermediate must fail,
# not be silently manufactured. Any non-zero rc is STOP and burns the run ID.
rp0_allocate_evidence_dir() {
    local evdir="$1" out rc=0
    out="$(mkdir -m 0700 -- "$evdir" 2>&1)" || rc=$?
    if [ "$rc" -ne 0 ]; then
        rp0_stop "evidence_allocation_failed dir=$evdir rc=$rc detail=$out run_id_burned=yes"
        return 3
    fi
    rp0_note "evidence_dir_allocated dir=$evdir"
    return 0
}

# --- create-once evidence leaf ---------------------------------------------
# `noclobber` makes the shell open with O_CREAT|O_EXCL, so an existing regular
# file, a LIVE symlink and a DANGLING symlink are all refused with EEXIST. This
# is the exact predicate the rejected `[[ -e "$LOG" ]]` guard did not provide.
# No append, no truncation of an existing path, no rename-aside, no retry.
rp0_open_evidence_leaf() {
    local leaf="$1" rc=0 kind size
    set -o noclobber
    : > "$leaf" || rc=$?
    set +o noclobber
    if [ "$rc" -ne 0 ]; then
        rp0_stop "evidence_leaf_not_creatable leaf=$leaf rc=$rc"; return 3
    fi
    kind="$(rp0_probe_path "$leaf")" || return 3
    [ "$kind" = "regular" ] || { rp0_stop "evidence_leaf_kind=$kind leaf=$leaf"; return 3; }
    size="$(LC_ALL=C stat -c '%s' -- "$leaf")" || { rp0_stop "evidence_leaf_stat_failed leaf=$leaf"; return 3; }
    [ "$size" = "0" ] || { rp0_stop "evidence_leaf_not_empty leaf=$leaf size=$size"; return 3; }
    exec > "$leaf" 2>&1
    return 0
}

# --- pgrep: 0 matched / 1 none / anything else STOP ------------------------
# Defect F9 was `pgrep ... || true` plus "empty temp file means no process".
# rc 2 (syntax/fatal) with empty output then read as "no writer survived".
rp0_pgrep_status() {
    local pat="$1" out rc=0
    out="$(pgrep -af "$pat" 2>&1)" || rc=$?
    case "$rc" in
        0) printf '%s\n' "$out"; return 0 ;;
        1) if [ -n "$out" ]; then rp0_stop "pgrep_rc1_with_output pattern=$pat out=$out"; return 3; fi
           return 1 ;;
        *) rp0_stop "pgrep_status pattern=$pat rc=$rc out=$out"; return 3 ;;
    esac
}

# --- systemctl is-enabled: token and status adjudicated TOGETHER -----------
# Defect F4/F9 was `systemctl is-enabled ... || true`, after which empty or
# error output satisfied `!= masked`. A preregistered token may only PASS when
# the command status is one of the documented token-producing statuses.
# Blank or unparsable output is STOP.
rp0_is_enabled_token() {
    local unit="$1" out rc=0
    out="$(systemctl is-enabled -- "$unit" 2>/dev/null)" || rc=$?
    case "$rc:$out" in
        0:enabled|0:enabled-runtime|0:alias|0:linked|0:linked-runtime|0:generated)
            printf '%s\n' "$out"; return 0 ;;
        1:static|1:masked|1:masked-runtime|1:disabled|1:indirect|1:transient)
            printf '%s\n' "$out"; return 0 ;;
    esac
    rp0_stop "is_enabled_unadjudicable unit=$unit rc=$rc token=[$out]"
    return 3
}

# --- systemctl show: one property, status adjudicated ----------------------
rp0_show_property() {
    local unit="$1" prop="$2" out rc=0
    out="$(systemctl show -p "$prop" --value -- "$unit" 2>/dev/null)" || rc=$?
    if [ "$rc" -ne 0 ]; then rp0_stop "systemctl_show_failed unit=$unit prop=$prop rc=$rc"; return 3; fi
    if [ -z "$out" ]; then rp0_stop "systemctl_show_blank unit=$unit prop=$prop"; return 3; fi
    printf '%s\n' "$out"; return 0
}

# --- systemd cgroup survivors: fail-closed, three outcomes -----------------
# "No writer pattern match and no listener" does NOT prove the unit is empty: a
# process that no longer matches the writer pattern, or that never opened the
# control port, still survives inside the unit's cgroup. Prints the survivor
# count for the whole cgroup SUBTREE. An unreadable property, an unparsable
# property line, a walk error, `find` stderr with rc 0, or an unreadable
# `cgroup.procs` is COULD NOT EVALUATE — never "0 survivors". Only an explicitly
# empty ControlGroup, or a cgroup directory classified absent, is zero.
rp0_cgroup_survivors() {
    local unit="$1" root="${RP0_CGROUP_ROOT:-/sys/fs/cgroup}"
    local out rc=0 cg dir kind err detail content f total=0
    local -a procfiles=() pids=()
    out="$(systemctl show -p ControlGroup -- "$unit" 2>/dev/null)" || rc=$?
    [ "$rc" -eq 0 ] || { rp0_stop "cgroup_property_failed unit=$unit rc=$rc"; return 3; }
    case "$out" in
        ControlGroup=*) cg="${out#ControlGroup=}" ;;
        *) rp0_stop "cgroup_property_unparsable unit=$unit out=[$out]"; return 3 ;;
    esac
    if [ -z "$cg" ]; then printf '0\n'; return 0; fi
    kind="$(rp0_probe_path "$root")" || return 3
    [ "$kind" = "dir" ] || { rp0_stop "cgroup_root_kind=$kind path=$root"; return 3; }
    dir="$root$cg"
    kind="$(rp0_probe_path "$dir")" || return 3
    case "$kind" in
        absent) printf '0\n'; return 0 ;;
        dir)    : ;;
        *)      rp0_stop "cgroup_dir_kind=$kind path=$dir"; return 3 ;;
    esac
    err="$(mktemp)" || { rp0_stop "cgroup_tempfile_failed unit=$unit"; return 3; }
    rc=0
    out="$(find "$dir" -type f -name cgroup.procs -print 2>"$err")" || rc=$?
    detail="$(tr -d '\r\n' <"$err")"; rm -f "$err"
    [ "$rc" -eq 0 ] || { rp0_stop "cgroup_walk_failed dir=$dir rc=$rc detail=$detail"; return 3; }
    [ -z "$detail" ] || { rp0_stop "cgroup_walk_stderr dir=$dir detail=$detail"; return 3; }
    if [ -n "$out" ]; then mapfile -t procfiles <<<"$out"; fi
    for f in "${procfiles[@]}"; do
        rc=0
        content="$(LC_ALL=C cat -- "$f" 2>/dev/null)" || rc=$?
        [ "$rc" -eq 0 ] || { rp0_stop "cgroup_procs_unreadable file=$f rc=$rc"; return 3; }
        if [ -n "$content" ]; then mapfile -t pids <<<"$content"; total=$(( total + ${#pids[@]} )); fi
    done
    printf '%s\n' "$total"
    return 0
}

# --- pipeline discipline ---------------------------------------------------
# Rule: any pipeline runs under `set -o pipefail` AND its complete component
# status vector (${PIPESTATUS[@]}) is adjudicated; empty output is never
# sufficient. Where a pipeline can be avoided it is avoided — that is strictly
# stronger than adjudicating one. The listener count below uses no pipeline.
rp0_listener_count() {
    local port="$1" raw rc=0
    local -a lines=()
    raw="$(ss -H -ltn "sport = :${port}" 2>&1)" || rc=$?
    if [ "$rc" -ne 0 ]; then rp0_stop "ss_status port=$port rc=$rc out=$raw"; return 3; fi
    if [ -n "$raw" ]; then mapfile -t lines <<<"$raw"; fi
    printf '%s\n' "${#lines[@]}"
    return 0
}

# --- identity inventories: a count is NOT an identity ----------------------
# A before/after comparison assembled from statuses and COUNTS cannot see a
# same-count replacement. Swap one bridge writer for another, one listening
# socket for another, or one cgroup member for another, and every status and
# every count stays equal while the host has in fact changed. That is exactly
# how a "nothing was mutated" claim can be satisfied by a mutated host.
# Each function below therefore emits a CANONICAL, fail-closed INVENTORY that
# identifies the objects themselves. Same three outcomes as every other
# predicate: an inventory that cannot be taken is never rendered as an empty,
# partial or defaulted value, and is never re-read as "nothing there".

# args: <pgrep pattern>
# Prints one `<pid> <full command line>` line per match, LC_ALL=C sorted, or the
# single literal `none`. rc 1 is not an outcome here: "no process matches" is a
# legitimate inventory VALUE, because callers compare inventories, not statuses.
rp0_writer_inventory() {
    local pat="$1" out rc=0 sorted
    out="$(pgrep -af "$pat" 2>&1)" || rc=$?
    case "$rc" in
        0) if [ -z "$out" ]; then rp0_stop "writer_inventory_rc0_empty pattern=$pat"; return 3; fi ;;
        1) if [ -n "$out" ]; then rp0_stop "writer_inventory_rc1_with_output pattern=$pat out=$out"; return 3; fi
           printf 'none\n'; return 0 ;;
        *) rp0_stop "writer_inventory_status pattern=$pat rc=$rc out=$out"; return 3 ;;
    esac
    sorted="$(LC_ALL=C sort <<<"$out")" || { rp0_stop "writer_inventory_sort_failed pattern=$pat"; return 3; }
    printf '%s\n' "$sorted"
    return 0
}

# args: <port>
# Prints one canonical identity line per listening socket, LC_ALL=C sorted, or
# the single literal `none`. `-p` attaches the OWNING process, so a replacement
# behind an unchanged count is visible; a socket line carrying no `users:((…))`
# field means the owner COULD NOT BE DETERMINED, which is rc 3 — never "the same
# listener as before". Recv-Q/Send-Q are deliberately dropped: they are live
# queue gauges, not identity, and comparing them would report a benign
# accept-queue movement as a mutation. No pipeline is used.
rp0_listener_inventory() {
    local port="$1" raw rc=0 line st rq sq loc peer rest ident acc sorted
    local -a lines=()
    raw="$(ss -H -ltnp "sport = :${port}" 2>&1)" || rc=$?
    if [ "$rc" -ne 0 ]; then rp0_stop "listener_inventory_status port=$port rc=$rc out=$raw"; return 3; fi
    if [ -z "$raw" ]; then printf 'none\n'; return 0; fi
    mapfile -t lines <<<"$raw"
    acc=""
    for line in "${lines[@]}"; do
        case "$line" in
            *users:*) : ;;
            *) rp0_stop "listener_owner_unresolved port=$port line=[$line]"; return 3 ;;
        esac
        st=""; rq=""; sq=""; loc=""; peer=""; rest=""
        read -r st rq sq loc peer rest <<<"$line"
        if [ -z "$st" ] || [ -z "$loc" ] || [ -z "$rest" ]; then
            rp0_stop "listener_line_incomplete port=$port line=[$line]"; return 3
        fi
        ident="state=$st local=$loc peer=$peer owner=$rest"
        acc="${acc}${ident}"$'\n'
    done
    sorted="$(LC_ALL=C sort <<<"${acc%$'\n'}")" \
        || { rp0_stop "listener_inventory_sort_failed port=$port"; return 3; }
    printf '%s\n' "$sorted"
    return 0
}

# args: <unit>
# Prints one `cgroup=<path relative to the root> pid=<pid>` line per member of
# the unit's cgroup SUBTREE, LC_ALL=C sorted, or the single literal `empty`.
# Fail-closed exactly like rp0_cgroup_survivors: an unreadable or unparsable
# property, a walk error, `find` stderr with rc 0, or an unreadable
# `cgroup.procs` is COULD NOT EVALUATE, never "no member". PID identity is the
# membership predicate; a kernel PID recycled onto a different process inside the
# compared window is not distinguished, and that residual is disclosed in §8.7.
# The counting predicate above is left byte-identical rather than refactored to
# share this walk, so its already-exercised falsifications keep standing.
rp0_cgroup_inventory() {
    local unit="$1" root="${RP0_CGROUP_ROOT:-/sys/fs/cgroup}"
    local out rc=0 cg dir kind err detail content f p rel acc sorted
    local -a procfiles=() pids=()
    out="$(systemctl show -p ControlGroup -- "$unit" 2>/dev/null)" || rc=$?
    [ "$rc" -eq 0 ] || { rp0_stop "cgroup_inventory_property_failed unit=$unit rc=$rc"; return 3; }
    case "$out" in
        ControlGroup=*) cg="${out#ControlGroup=}" ;;
        *) rp0_stop "cgroup_inventory_property_unparsable unit=$unit out=[$out]"; return 3 ;;
    esac
    if [ -z "$cg" ]; then printf 'empty\n'; return 0; fi
    kind="$(rp0_probe_path "$root")" || return 3
    [ "$kind" = "dir" ] || { rp0_stop "cgroup_inventory_root_kind=$kind path=$root"; return 3; }
    dir="$root$cg"
    kind="$(rp0_probe_path "$dir")" || return 3
    case "$kind" in
        absent) printf 'empty\n'; return 0 ;;
        dir)    : ;;
        *)      rp0_stop "cgroup_inventory_dir_kind=$kind path=$dir"; return 3 ;;
    esac
    err="$(mktemp)" || { rp0_stop "cgroup_inventory_tempfile_failed unit=$unit"; return 3; }
    rc=0
    out="$(find "$dir" -type f -name cgroup.procs -print 2>"$err")" || rc=$?
    detail="$(tr -d '\r\n' <"$err")"; rm -f "$err"
    [ "$rc" -eq 0 ] || { rp0_stop "cgroup_inventory_walk_failed dir=$dir rc=$rc detail=$detail"; return 3; }
    [ -z "$detail" ] || { rp0_stop "cgroup_inventory_walk_stderr dir=$dir detail=$detail"; return 3; }
    if [ -n "$out" ]; then mapfile -t procfiles <<<"$out"; fi
    acc=""
    for f in "${procfiles[@]}"; do
        rc=0
        content="$(LC_ALL=C cat -- "$f" 2>/dev/null)" || rc=$?
        [ "$rc" -eq 0 ] || { rp0_stop "cgroup_inventory_procs_unreadable file=$f rc=$rc"; return 3; }
        [ -n "$content" ] || continue
        mapfile -t pids <<<"$content"
        rel="${f#"$root"}"
        for p in "${pids[@]}"; do
            [ -n "$p" ] || continue
            acc="${acc}cgroup=${rel} pid=${p}"$'\n'
        done
    done
    if [ -z "$acc" ]; then printf 'empty\n'; return 0; fi
    sorted="$(LC_ALL=C sort <<<"${acc%$'\n'}")" \
        || { rp0_stop "cgroup_inventory_sort_failed unit=$unit"; return 3; }
    printf '%s\n' "$sorted"
    return 0
}
