# ===== BLOCK-ID: RP6-P0 ===== [EXECUTABLE PROPOSAL BLOCK]
# WP-I P0 preflight - the premises every later WP-I claim rests on (PROPOSED
# DESIGN, DRAFT). Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b.
#
# AUTHORITY. DRAFT. Not frozen, not hashed into any kit, and carrying NO
# authority to run against any host. WP-I holds no host-contact authority and no
# budget lift, so nothing here may be dispatched on the strength of this file.
#
# WHAT P0 IS FOR. P0 establishes, from the login the run actually gets: who the
# process is numerically, that every tool the RO stage will invoke resolves and
# is executable by this login, that the system manager answers a Manager-level
# query over the system bus from this login's PID and mount namespaces, that the
# per-SHA venv interpreter can actually be executed, and what this login's net,
# pid and mnt namespace identities are. The RO stage is admissible only if P0
# held. Folding the two together would let a run assert a result whose
# precondition it never checked.
#
# rc contract, identical to the accepted blocks:
#   0 = PASS   1 = FAIL (a probe ran and observed deviant state)   3 = STOP
# No raw tool status may escape as this block's exit code: every capture is
# adjudicated at its call site, and the ERR trap below converts anything still
# unadjudicated into a reasoned STOP.
#
# ORDER OF ADJUDICATION (pattern 6). Every producer runs under LC_ALL=C, has its
# stdout and stderr captured together, and has its status and its diagnostics
# adjudicated BEFORE any byte of its output is interpreted. Streams are merged
# on purpose: with no temp file available (pattern 4 / audit-1 F4), a merged
# capture that must equal an exact expected shape is strictly stronger than
# "rc 0 and stdout looks right", because any stderr text destroys the shape.
#
# NUMERIC IDENTITY ONLY (pattern 8). No name is looked up, captured or compared
# anywhere in this block. `stat` is never asked for %U or %G; `id` is only ever
# asked for -u, -g and -G; every preregistered identity input is numeric. A
# rendered name is an answer from a database this run does not control, so this
# block asks that database nothing.
#
# STOP IS NOT A RESULT (pattern 1). Each branch below was written by first
# writing the sentence it emits and then asking which of three things it
# witnessed. The two classes that are FAIL here are the venv-root and venv
# interpreter object arms: an exact-shape ENOENT on a PREREGISTERED absolute
# path positively proves that directory search succeeded and observes a missing
# preregistered object, which is the ruling of audit-1 F5/O1 and is deviant host
# state, not an inability to evaluate. Everything else P0 can observe - a tool
# that does not resolve, a manager that does not answer, an exec denial, an
# unreadable namespace link - is an inability to evaluate and is STOP. The
# kickoff's tool rule ("a missing tool is a STOP naming the tool, never a silent
# skip and never a FAIL") is binding and deliberately NOT generalised from the
# audit-1 F5 ruling: a PATH-resolved tool has no preregistered path, so its
# absence is not an observation about a named host object.
#
# MUTATION SURFACE. This block creates no file, no directory and no temporary
# file, opens nothing for writing, and changes no mode, owner, ACL, group,
# service or network state. It duplicates its own stdout onto fd 8 and closes it
# again, which is a descriptor operation, not a filesystem one. The evidence
# directory and the evidence leaf are created by the ACCEPTED RP0-BOOTSTRAP
# before this block runs; that allocation is the bootstrap's mutation and is not
# claimed here as none. This block asserts the allocation happened and that its
# own stdout is bound to that leaf, and refuses to run otherwise.
# The external-child surface is not a fixed count. Metadata, evidence-binding,
# identity and namespace probes execute the recorded absolute stat/readlink/id
# paths with the caller environment inherited and LC_ALL forced to C. Only the
# Manager-level `systemctl show` query and the isolated interpreter invocation
# use `env -i`. Every launch keeps the caller working directory; TMPDIR is
# caller-inherited for stat/readlink/id and absent from the two cleared launches.
# This is an honest record of the current bounded P0 block, not compliance with
# round 1.4's stronger probe-execution-environment rule; satisfying that rule
# needs preregistered cwd/TMPDIR and helper target chains before a future freeze.
#
# RP0-LIB helpers deliberately NOT used here, and why:
#   - `rp0_probe_path` (RP0-LIB:29-55) allocates a temp file at RP0-LIB:31 and
#     sanitizes captured stderr with an UNADJUDICATED `tr` at RP0-LIB:39 and
#     RP0-LIB:49 - audit-1 F4 and F6. `p0_probe_kind` below is a local,
#     temp-free, fully adjudicated replacement emitting the same six tokens, and
#     it additionally requires a failure diagnostic to be exactly ONE recognised
#     C-locale shape naming the probed path (audit-2 A2-F6), which the library
#     helper does not do.
#   - `rp0_show_property` (RP0-LIB:183-189) and `rp0_is_enabled_token`
#     (RP0-LIB:169-180) discard stderr with `2>/dev/null`, so their diagnostics
#     can never be adjudicated, and both are UNIT queries resolved through PATH.
#     P0 needs a MANAGER readiness query, run from a pinned absolute path with a
#     cleared environment and with its stderr inside the evidence, so
#     `p0_assert_system_manager_ready` is a local replacement.
#   - `rp0_monotonic_ms`, `rp0_listener_count`, `rp0_listener_inventory`,
#     `rp0_writer_inventory`, `rp0_cgroup_survivors`, `rp0_cgroup_inventory`
#     serve RO-stage predicates and budgeted walks. P0 performs no walk and no
#     RO row, so none of them is called.
#   - `rp0_require_safe_component` (RP0-LIB:85-94) IS used, on the identifiers
#     the accepted bootstrap allocated, as proof that RP0-LIB is genuinely
#     sourced and functional rather than merely present by name.
#
# PREREQUISITES, in this order, in the SAME shell:
#   . RP0-LIB.sh        (predicate library; definitions only)
#   . RP0-BOOTSTRAP.sh  (create-once evidence dir + leaf; redirects stdout)
#   . RP6-P0.sh         (this block)
# The bootstrap redirects the shell's stdout into the create-once leaf, so this
# block must run in that same shell. Sourcing order is asserted, not assumed.
set -Eeuo pipefail
export LC_ALL=C

P0_SAFE=""
P0_COUNT=0
P0_KIND=""
P0_FKIND=""
P0_SHAPE=""
P0_LOOKUP=""
P0_CAPTURE=""
P0_RESOLUTION=""
P0_TOOLS_RESOLVED=""
P0_TOOLS_RESOLUTION=""
P0_NS_VALUE=""
P0_META_KIND=""
P0_META_MODE=""
P0_META_OWNER=""

p0_stop() { printf 'P0_STOP reason=%s\n' "$*"; exit 3; }
p0_fail() { printf 'P0_FAIL reason=%s\n' "$*"; exit 1; }

# --- fail-closed backstop for unadjudicated statuses ------------------------
# `set -e` alone exits with the failing tool's own status: 1 (misreadable as a
# host-state FAIL), 126, or 127. This trap guarantees that every path out of the
# block is 0, 1 or 3 and that a non-zero exit always carries a reason string. It
# is a backstop, not the mechanism: every capture below is adjudicated
# explicitly and this trap should be unreachable.
p0_on_err() {
    local rc=$?
    printf 'P0_STOP reason=unadjudicated_command_status rc=%s line=%s cmd=[%s]\n' \
        "$rc" "${BASH_LINENO[0]}" "$BASH_COMMAND"
    exit 3
}
trap 'p0_on_err' ERR

# --- diagnostic sanitization, builtins only ---------------------------------
# Parameter expansion only: no external tool, no subshell, no exit status to
# adjudicate (audit-1 F6). This is an OUTPUT filter that bounds what a
# diagnostic can push into the evidence leaf. It is never a classifier input:
# folding CR/LF into spaces before matching is exactly what let a two-line
# diagnostic select an arm by substring (audit-2 A2-F6). Classifiers below
# inspect the RAW capture first and sanitize only for printing.
p0_sanitize() {
    local s="${1-}"
    s="${s//$'\r'/ }"
    s="${s//$'\n'/ }"
    case "$s" in
        *[![:print:]]*) s="[non_printable_detail_suppressed]" ;;
    esac
    P0_SAFE="${s:0:400}"
}

# --- literal substring counter, builtins only (A2-F6) -----------------------
# Sets P0_COUNT to the number of non-overlapping occurrences of a LITERAL
# needle. No `grep -c`, no pipeline, no subshell: nothing here has an exit
# status that could escape while an ambiguity is being adjudicated. The needle
# is always a block literal, never captured text, so the empty-needle
# non-termination case is unreachable by construction.
p0_count_substr() {
    local needle="$2" n=0 rest="$1"
    while [ "${rest#*"$needle"}" != "$rest" ]; do
        rest="${rest#*"$needle"}"
        n=$(( n + 1 ))
    done
    P0_COUNT="$n"
}

# --- name=value lookup over a space-separated map, builtins only ------------
# Used for the tool pin table and for resolved tool paths. The unquoted
# expansion of the map is deliberate and safe: every value that can enter either
# map is refused earlier unless it is printable and contains no whitespace, so a
# path that could split is a STOP before it ever reaches this function.
p0_lookup() {
    local map="$1" want="$2" e
    P0_LOOKUP=""
    for e in $map; do
        case "$e" in
            "$want"=*) P0_LOOKUP="${e#*=}"; return 0 ;;
        esac
    done
    return 1
}

# --- preregistered constants ------------------------------------------------
# The candidate SHA is the frozen candidate of prereg section 2 and is never
# derived at run time.
P0_CAND="2ce41e34bceb599d80af24c5c33d835820ec321b"
P0_NS_NET_PATH="/proc/self/ns/net"
P0_NS_PID_PATH="/proc/self/ns/pid"
P0_NS_MNT_PATH="/proc/self/ns/mnt"
P0_FD_SELF="/proc/self/fd/8"
P0_EACCES_TEXT="Permission denied"
P0_ENOENT_TEXT="No such file or directory"

# --- the RO-stage tool inventory, derived ONLY from the prereg and the
# --- feasibility ledger -----------------------------------------------------
# stat, readlink, find  - B3 scoped walks, terminal metadata stat, and the
#                         literal-canonical predicate (feasibility B3; the
#                         accepted RP1-B3 uses exactly these three).
# id                    - prereg 8.1 rows 1-2, and the caller-identity and
#                         group predicates of RP1-B3.
# grep                  - B2 direct fragment half ("Grep rc outside {0,1} ...
#                         STOP before stdout comparison").
# sha256sum             - B1a installed-lock digest, B2 fragment digest.
# awk                   - the monotonic clock of the budgeted B3 sweep
#                         (RP0-LIB:21), which every walk row depends on.
# env                   - pinned, cleared-environment launch of the B1 verifier
#                         interpreter and of manager queries (pattern 4).
# systemctl             - prereg 8.1 rows 6-7; B2/B4 manager-backed rows.
# ss                    - prereg 8.1 row 3; B6 listener set.
# curl                  - prereg 8.1 row 4; B5 loopback control-endpoint GET.
# `stat` is listed first only so that the metadata pass has a resolved absolute
# `stat` to use; resolution and executability themselves are decided by shell
# builtins alone, so the order carries no privilege.
# NOT in this list, deliberately: the root-side pinned python3 of RPD-VERIFY
# (root-side, out of P0 scope), and the per-SHA venv interpreter, which has its
# own preregistered absolute path and its own arm below.
P0_RO_TOOLS="stat readlink id env find grep sha256sum awk systemctl ss curl"

# ---------------------------------------------------------------------------
# SECTION: prerequisites
# ---------------------------------------------------------------------------
# Asserting the prerequisites is what keeps the 0/1/3 contract honest: without
# RP0-LIB the first library call would abort under `set -e` with rc 127, and
# without RP0-BOOTSTRAP this block would write its evidence to whatever stdout
# happened to be.
printf 'P0_SECTION header candidate=%s block=RP6-P0 stage=p0\n' "$P0_CAND"
printf 'P0_SECTION prerequisites\n'

command -v rp0_require_safe_component >/dev/null 2>&1 \
    || p0_stop "rp0_lib_not_sourced predicate=rp0_require_safe_component"
command -v rp0_allocate_evidence_dir >/dev/null 2>&1 \
    || p0_stop "rp0_lib_not_sourced predicate=rp0_allocate_evidence_dir"

[ -n "${RUNID:-}" ]       || p0_stop "rp0_bootstrap_not_run detail=RUNID_unset"
[ -n "${EV_STAGE_ID:-}" ] || p0_stop "rp0_bootstrap_not_run detail=EV_STAGE_ID_unset"
[ -n "${EV_DIR:-}" ]      || p0_stop "rp0_bootstrap_not_run detail=EV_DIR_unset"
[ -n "${EV_LOG:-}" ]      || p0_stop "rp0_bootstrap_not_run detail=EV_LOG_unset"

# The accepted predicate is exercised, not merely name-checked. A refusal here
# is could-not-evaluate for P0's own evidence discipline, never host state.
rp0_require_safe_component RUNID "$RUNID" \
    || p0_stop "evidence_identifier_refused name=RUNID"
rp0_require_safe_component EV_STAGE_ID "$EV_STAGE_ID" \
    || p0_stop "evidence_identifier_refused name=EV_STAGE_ID"
printf 'P0_prereq lib=sourced bootstrap=ran run_id=%s stage=%s dir=%s leaf=%s\n' \
    "$RUNID" "$EV_STAGE_ID" "$EV_DIR" "$EV_LOG"

# ---------------------------------------------------------------------------
# SECTION: preregistered inputs
# ---------------------------------------------------------------------------
# A missing or malformed operator input is COULD NOT EVALUATE, not deviant host
# state. Every input is numeric or a preregistered absolute path; none is
# derived here, and none is a name.
p0_require_uint() {
    local name="$1" val="$2" min="$3"
    [ -n "$val" ] \
        || p0_stop "input_missing name=$name detail=preregistered_numeric_value_never_derived_here"
    case "$val" in
        *[!0-9]*) p0_stop "input_charset name=$name expected=decimal_digits" ;;
    esac
    [ "$val" -ge "$min" ] \
        || p0_stop "input_range name=$name value=$val expected_min=$min"
}

# P0_EXPECT_UID - the preregistered NUMERIC uid of the route login. Zero is
# refused as an INPUT, not merely as an observation: the accepted execution
# model is unprivileged, so a preregistration naming uid 0 is a plumbing error.
p0_require_uint P0_EXPECT_UID "${P0_EXPECT_UID:-}" 1
: "${P0_EXPECT_UID:?preregistered numeric uid of the route login is required}"

# P0_FORBIDDEN_GIDS - the preregistered NUMERIC gids the feasibility ledger
# asserts this login is NOT in (prereg 8.1 row 2: the root group and the
# state/log group). gid 0 is a legitimate member of this list, so zero is
# allowed here.
[ -n "${P0_FORBIDDEN_GIDS:-}" ] \
    || p0_stop "input_missing name=P0_FORBIDDEN_GIDS detail=preregistered_numeric_gid_list_never_derived_here"
: "${P0_FORBIDDEN_GIDS:?preregistered numeric forbidden-gid list is required}"
P0_FORBIDDEN_GID_COUNT=0
for p0_g in $P0_FORBIDDEN_GIDS; do
    p0_require_uint P0_FORBIDDEN_GIDS_ENTRY "$p0_g" 0
    P0_FORBIDDEN_GID_COUNT=$(( P0_FORBIDDEN_GID_COUNT + 1 ))
done
[ "$P0_FORBIDDEN_GID_COUNT" -ge 1 ] \
    || p0_stop "input_range name=P0_FORBIDDEN_GIDS value=[$P0_FORBIDDEN_GIDS] expected=at_least_one_numeric_gid"

# P0_VENV_ROOT - the preregistered per-SHA venv root (prereg section 2,
# WPI_VENV_ROOT). Shape only is checked here, with builtins; the filesystem
# object is adjudicated in the interpreter section, after the tools that would
# probe it have been resolved.
[ -n "${P0_VENV_ROOT:-}" ] \
    || p0_stop "input_missing name=P0_VENV_ROOT detail=preregistered_per_sha_venv_root_never_derived_here"
: "${P0_VENV_ROOT:?preregistered per-SHA venv root is required}"
case "$P0_VENV_ROOT" in
    *[![:print:]]*|*[[:space:]]*)
        p0_stop "input_charset name=P0_VENV_ROOT expected=printable_without_whitespace" ;;
esac
case "$P0_VENV_ROOT" in
    /*) : ;;
    *)  p0_stop "input_not_absolute name=P0_VENV_ROOT value=[$P0_VENV_ROOT]" ;;
esac
case "/$P0_VENV_ROOT/" in
    *"/../"*|*"/./"*)
        p0_stop "input_path_traversal name=P0_VENV_ROOT value=[$P0_VENV_ROOT]" ;;
esac
# The venv root must be bound to the frozen candidate. A P0 that validated some
# other interpreter would establish a premise about the wrong object.
case "$P0_VENV_ROOT" in
    */"$P0_CAND") : ;;
    *) p0_stop "input_not_candidate_bound name=P0_VENV_ROOT expected_basename=$P0_CAND" ;;
esac

# P0_TOOL_PINS - optional preregistered pin table, entries `name=/absolute/path`
# separated by spaces. Where the design requires a pinned absolute path, the pin
# is supplied here and PATH resolution must agree with it; a disagreement is a
# shadowing signal and STOPs. Where no pin is preregistered the resolved
# absolute path is RECORDED so the successor preregistration can pin it, and the
# claim line says so.
P0_TOOL_PINS="${P0_TOOL_PINS:-}"
P0_PIN_COUNT=0
for p0_pin in $P0_TOOL_PINS; do
    case "$p0_pin" in
        *=*) : ;;
        *) p0_stop "input_pin_malformed name=P0_TOOL_PINS entry=[$p0_pin] expected=tool=absolute_path" ;;
    esac
    p0_pin_name="${p0_pin%%=*}"
    p0_pin_path="${p0_pin#*=}"
    p0_lookup_hit=no
    for p0_t in $P0_RO_TOOLS; do
        if [ "$p0_t" = "$p0_pin_name" ]; then p0_lookup_hit=yes; fi
    done
    [ "$p0_lookup_hit" = "yes" ] \
        || p0_stop "input_pin_unknown_tool name=P0_TOOL_PINS tool=$p0_pin_name inventory=[$P0_RO_TOOLS]"
    case "$p0_pin_path" in
        /*) : ;;
        *) p0_stop "input_pin_not_absolute tool=$p0_pin_name path=[$p0_pin_path]" ;;
    esac
    case "$p0_pin_path" in
        *[![:print:]]*|*[[:space:]]*)
            p0_stop "input_pin_charset tool=$p0_pin_name expected=printable_without_whitespace" ;;
    esac
    P0_PIN_COUNT=$(( P0_PIN_COUNT + 1 ))
done

# This derives the literal leaf name only. P0 has no preregistered value for a
# resolved `bin` component or interpreter-symlink target chain, so it cannot
# truthfully bind either one here; that residual is disclosed in the terminal
# `does_not_establish` claim instead of learning and accepting a target at run
# time contrary to prereg row 18.
P0_PY="$P0_VENV_ROOT/bin/python"

printf 'P0_SECTION preregistered_inputs\n'
printf 'P0_input name=P0_EXPECT_UID value=%s\n' "$P0_EXPECT_UID"
printf 'P0_input name=P0_FORBIDDEN_GIDS value=[%s] count=%s\n' \
    "$P0_FORBIDDEN_GIDS" "$P0_FORBIDDEN_GID_COUNT"
printf 'P0_input name=P0_VENV_ROOT value=%s\n' "$P0_VENV_ROOT"
printf 'P0_input name=P0_TOOL_PINS value=[%s] count=%s\n' "$P0_TOOL_PINS" "$P0_PIN_COUNT"
printf 'P0_input name=P0_INTERPRETER value=%s derived_from=P0_VENV_ROOT\n' "$P0_PY"

# ---------------------------------------------------------------------------
# SECTION: tool inventory
# ---------------------------------------------------------------------------
# Resolution and executability are decided by shell builtins only - `command -v`
# and the access(2) predicate `[ -x ]` - so no external tool has to be trusted
# before the inventory that establishes it. `stat` is used afterwards, for the
# RECORD only; a failure there is could-not-evaluate, never a silent skip.
# What this section establishes: the named tool resolves to an absolute path
# that this login may execute, and that path's kind, mode and numeric owner are
# recorded. What it does NOT establish: that the resolved object is the
# distribution's tool. P0 has no attestation channel and does not pretend to
# one; unpinned entries are recorded as `path_resolved_absolute` precisely so
# the successor can pin them.
p0_resolve_tool() {
    local t="$1" resolved rc=0 pin
    resolved="$(command -v "$t" 2>&1)" || rc=$?
    if [ "$rc" -ne 0 ] || [ -z "$resolved" ]; then
        p0_sanitize "$resolved"
        p0_stop "missing_tool tool=$t rc=$rc detail=[$P0_SAFE]"
    fi
    case "$resolved" in
        /*) : ;;
        *)  p0_sanitize "$resolved"
            p0_stop "tool_resolution_unparsable tool=$t resolved=[$P0_SAFE] expected=absolute_path" ;;
    esac
    case "$resolved" in
        *[![:print:]]*|*[[:space:]]*)
            p0_sanitize "$resolved"
            p0_stop "tool_resolution_unparsable tool=$t resolved=[$P0_SAFE] expected=printable_without_whitespace" ;;
    esac
    if p0_lookup "$P0_TOOL_PINS" "$t"; then
        pin="$P0_LOOKUP"
        [ "$resolved" = "$pin" ] \
            || p0_stop "tool_pin_mismatch tool=$t pinned=$pin resolved=$resolved"
        P0_RESOLUTION="pinned_absolute"
    else
        P0_RESOLUTION="path_resolved_absolute"
    fi
    [ -x "$resolved" ] \
        || p0_stop "tool_not_executable tool=$t path=$resolved mechanism=access_builtin_x"
    P0_TOOLS_RESOLVED="$P0_TOOLS_RESOLVED $t=$resolved"
    P0_TOOLS_RESOLUTION="$P0_TOOLS_RESOLUTION $t=$P0_RESOLUTION"
}

# Metadata record for one already-resolved tool. Status first, then shape, then
# fields; nothing here decides anything, and an unreadable or unparsable record
# is a STOP rather than a blank column.
p0_record_metadata() {
    local label="$1" p="$2" raw rc=0 rest
    P0_META_KIND=""; P0_META_MODE=""; P0_META_OWNER=""
    raw="$(LC_ALL=C "$P0_STAT" -c '%F|%a|%u:%g' -- "$p" 2>&1)" || rc=$?
    if [ "$rc" -ne 0 ]; then
        p0_sanitize "$raw"
        p0_stop "metadata_unreadable subject=$label path=$p rc=$rc detail=$P0_SAFE"
    fi
    case "$raw" in
        *$'\r'*|*$'\n'*)
            p0_sanitize "$raw"
            p0_stop "metadata_multiline subject=$label path=$p detail=$P0_SAFE" ;;
    esac
    case "$raw" in
        *"|"*"|"*) : ;;
        *) p0_sanitize "$raw"
           p0_stop "metadata_unparsable subject=$label path=$p detail=[$P0_SAFE] expected=kind|mode|uid:gid" ;;
    esac
    P0_META_KIND="${raw%%|*}"
    rest="${raw#*|}"
    P0_META_MODE="${rest%%|*}"
    P0_META_OWNER="${rest#*|}"
    case "$P0_META_KIND" in
        ""|*[![:print:]]*) p0_stop "metadata_unparsable subject=$label path=$p field=kind" ;;
    esac
    case "$P0_META_MODE" in
        ""|*[!0-7]*) p0_stop "metadata_unparsable subject=$label path=$p field=mode value=[$P0_META_MODE]" ;;
    esac
    case "$P0_META_OWNER" in
        *[!0-9:]*|*:*:*|:*|*:|"")
            p0_stop "metadata_unparsable subject=$label path=$p field=owner_numeric value=[$P0_META_OWNER]" ;;
        *:*) : ;;
        *) p0_stop "metadata_unparsable subject=$label path=$p field=owner_numeric value=[$P0_META_OWNER]" ;;
    esac
}

printf 'P0_SECTION tool_inventory\n'
for p0_t in $P0_RO_TOOLS; do
    p0_resolve_tool "$p0_t"
done

p0_lookup "$P0_TOOLS_RESOLVED" stat      || p0_stop "missing_tool tool=stat detail=absent_from_resolved_map"
P0_STAT="$P0_LOOKUP"
p0_lookup "$P0_TOOLS_RESOLVED" readlink  || p0_stop "missing_tool tool=readlink detail=absent_from_resolved_map"
P0_READLINK="$P0_LOOKUP"
p0_lookup "$P0_TOOLS_RESOLVED" id        || p0_stop "missing_tool tool=id detail=absent_from_resolved_map"
P0_ID="$P0_LOOKUP"
p0_lookup "$P0_TOOLS_RESOLVED" env       || p0_stop "missing_tool tool=env detail=absent_from_resolved_map"
P0_ENV="$P0_LOOKUP"
p0_lookup "$P0_TOOLS_RESOLVED" systemctl || p0_stop "missing_tool tool=systemctl detail=absent_from_resolved_map"
P0_SYSTEMCTL="$P0_LOOKUP"

P0_TOOL_COUNT=0
for p0_t in $P0_RO_TOOLS; do
    p0_lookup "$P0_TOOLS_RESOLVED" "$p0_t" || p0_stop "missing_tool tool=$p0_t detail=absent_from_resolved_map"
    p0_path="$P0_LOOKUP"
    p0_lookup "$P0_TOOLS_RESOLUTION" "$p0_t" || p0_stop "tool_resolution_unparsable tool=$p0_t detail=resolution_mode_lost"
    p0_res="$P0_LOOKUP"
    p0_record_metadata "tool:$p0_t" "$p0_path"
    printf 'P0_tool name=%s path=%s kind=%s mode=%s owner_numeric=%s resolution=%s\n' \
        "$p0_t" "$p0_path" "$P0_META_KIND" "$P0_META_MODE" "$P0_META_OWNER" "$p0_res"
    P0_TOOL_COUNT=$(( P0_TOOL_COUNT + 1 ))
done
printf 'P0_tool_inventory count=%s pinned=%s provenance=not_established\n' \
    "$P0_TOOL_COUNT" "$P0_PIN_COUNT"

# ---------------------------------------------------------------------------
# SECTION: evidence binding
# ---------------------------------------------------------------------------
# The bootstrap redirected this shell's stdout into the create-once leaf. That
# is asserted here rather than assumed, and it is asserted by OBJECT IDENTITY
# (device and inode), not by a path string: a path comparison inside a command
# substitution would compare the substitution's pipe, and a path can be renamed
# under a still-open descriptor. fd 8 is a dup of the real stdout, so the
# identity survives the subshell the capture runs in. The resolved path is
# recorded as a diagnostic only.
p0_assert_evidence_leaf_bound() {
    local rawpath fdid logid rc=0
    exec 8>&1
    rawpath="$(LC_ALL=C "$P0_READLINK" -- "$P0_FD_SELF" 2>&1)" || rc=$?
    if [ "$rc" -ne 0 ]; then
        p0_sanitize "$rawpath"
        exec 8>&-
        p0_stop "evidence_binding_unprobeable path=$P0_FD_SELF rc=$rc detail=$P0_SAFE"
    fi
    rc=0
    fdid="$(LC_ALL=C "$P0_STAT" -L -c '%d:%i' -- "$P0_FD_SELF" 2>&1)" || rc=$?
    if [ "$rc" -ne 0 ]; then
        p0_sanitize "$fdid"
        exec 8>&-
        p0_stop "evidence_binding_unprobeable path=$P0_FD_SELF rc=$rc detail=$P0_SAFE"
    fi
    rc=0
    logid="$(LC_ALL=C "$P0_STAT" -c '%d:%i' -- "$EV_LOG" 2>&1)" || rc=$?
    exec 8>&-
    if [ "$rc" -ne 0 ]; then
        p0_sanitize "$logid"
        p0_stop "evidence_binding_unprobeable path=$EV_LOG rc=$rc detail=$P0_SAFE"
    fi
    case "$fdid" in
        *[!0-9:]*|*:*:*|:*|*:|"") p0_stop "evidence_binding_unparsable subject=fd8 value=[$fdid]" ;;
        *:*) : ;;
        *) p0_stop "evidence_binding_unparsable subject=fd8 value=[$fdid]" ;;
    esac
    case "$logid" in
        *[!0-9:]*|*:*:*|:*|*:|"") p0_stop "evidence_binding_unparsable subject=ev_log value=[$logid]" ;;
        *:*) : ;;
        *) p0_stop "evidence_binding_unparsable subject=ev_log value=[$logid]" ;;
    esac
    p0_sanitize "$rawpath"
    [ "$fdid" = "$logid" ] \
        || p0_stop "evidence_leaf_not_bound ev_log=$EV_LOG ev_log_id=$logid stdout_id=$fdid stdout_path=[$P0_SAFE]"
    printf 'P0_evidence_bound leaf=%s object_id=%s stdout_path=[%s] mechanism=dev_inode_identity\n' \
        "$EV_LOG" "$logid" "$P0_SAFE"
}

printf 'P0_SECTION evidence_binding\n'
p0_assert_evidence_leaf_bound

# ---------------------------------------------------------------------------
# SECTION: executing identity (prereg 8.1 rows 1-2)
# ---------------------------------------------------------------------------
# Numeric only. `id -un` and every other name form is deliberately not called:
# it would ask a name service this run does not control, and audit-2 A2-F3
# showed a rendered name accepting the wrong numeric identity.
# Row 1 divergence keeps the prereg reason token `identity_unexpected`, with the
# name fields replaced by numeric ones. Row 2 keeps `capability_wider_than_
# ledger`, likewise numeric: MORE privilege than the ledger assumed is a STOP,
# because several DEFER-ROOT-SIDE calls would then rest on a false premise and
# the correct response is re-adjudication of the scope, not a run that quietly
# reaches further than the document it was preregistered under.
p0_capture_numeric() {
    local label="$1" flag="$2" raw rc=0
    raw="$(LC_ALL=C "$P0_ID" "$flag" 2>&1)" || rc=$?
    if [ "$rc" -ne 0 ]; then
        p0_sanitize "$raw"
        p0_stop "identity_probe_failed field=$label flag=$flag rc=$rc detail=$P0_SAFE"
    fi
    case "$raw" in
        *$'\r'*|*$'\n'*)
            p0_sanitize "$raw"
            p0_stop "identity_probe_multiline field=$label flag=$flag detail=$P0_SAFE" ;;
    esac
    [ -n "$raw" ] || p0_stop "identity_probe_empty field=$label flag=$flag"
    P0_CAPTURE="$raw"
}

p0_record_identity() {
    local uid gid gids g count=0 f
    p0_capture_numeric uid -u; uid="$P0_CAPTURE"
    case "$uid" in
        *[!0-9]*) p0_stop "identity_probe_unparsable field=uid value=[$uid] expected=decimal_digits" ;;
    esac
    p0_capture_numeric gid -g; gid="$P0_CAPTURE"
    case "$gid" in
        *[!0-9]*) p0_stop "identity_probe_unparsable field=gid value=[$gid] expected=decimal_digits" ;;
    esac
    p0_capture_numeric gids -G; gids="$P0_CAPTURE"
    for g in $gids; do
        case "$g" in
            *[!0-9]*) p0_stop "identity_probe_unparsable field=gids value=[$gids] expected=decimal_digits" ;;
        esac
        count=$(( count + 1 ))
    done
    [ "$count" -ge 1 ] || p0_stop "identity_probe_empty field=gids value=[$gids]"
    printf 'P0_identity uid=%s gid=%s gids=[%s] gid_count=%s form=numeric_only\n' \
        "$uid" "$gid" "$gids" "$count"
    [ "$uid" = "$P0_EXPECT_UID" ] \
        || p0_stop "identity_unexpected uid=$uid expected=$P0_EXPECT_UID"
    # Whole-word match on the space-padded list, so gid 0 does not match gid 10.
    for f in $P0_FORBIDDEN_GIDS; do
        case " $gids " in
            *" $f "*) p0_stop "capability_wider_than_ledger gid=$f caller_gids=[$gids]" ;;
        esac
    done
    printf 'P0_identity_admitted uid=%s forbidden_gids=[%s] intersection=empty\n' \
        "$uid" "$P0_FORBIDDEN_GIDS"
}

printf 'P0_SECTION identity\n'
p0_record_identity

# ---------------------------------------------------------------------------
# SECTION: namespace identity (WP-I audit F2)
# ---------------------------------------------------------------------------
# RECORD ONLY. This block observes the net, pid and mount namespace identities
# of ITS OWN process and prints them. It does not compare them with any
# service's, does not read /proc/1/ns/* and does not claim that they are the
# host's initial namespaces - labelling a local observation `bound=initial` was
# exactly audit-2 A2-F2. The value of the record is that a later listener or
# unit claim can be shown to have been made from these namespaces, or shown not
# to have been. Unreadable is STOP, never a silent omission.
p0_read_ns() {
    local label="$1" path="$2" raw rc=0
    raw="$(LC_ALL=C "$P0_READLINK" -- "$path" 2>&1)" || rc=$?
    if [ "$rc" -ne 0 ]; then
        p0_sanitize "$raw"
        p0_stop "namespace_unreadable ns=$label path=$path rc=$rc detail=$P0_SAFE"
    fi
    [ -n "$raw" ] || p0_stop "namespace_identity_empty ns=$label path=$path"
    case "$raw" in
        *[![:print:]]*|*[[:space:]]*)
            p0_stop "namespace_identity_unprintable ns=$label path=$path" ;;
    esac
    P0_NS_VALUE="$raw"
}

p0_record_namespaces() {
    local net pid mnt
    p0_read_ns net "$P0_NS_NET_PATH"; net="$P0_NS_VALUE"
    p0_read_ns pid "$P0_NS_PID_PATH"; pid="$P0_NS_VALUE"
    p0_read_ns mnt "$P0_NS_MNT_PATH"; mnt="$P0_NS_VALUE"
    printf 'P0_namespace net=%s pid=%s mnt=%s scope=self_only claim=record_only binding=not_established\n' \
        "$net" "$pid" "$mnt"
}

printf 'P0_SECTION namespaces\n'
p0_record_namespaces

# ---------------------------------------------------------------------------
# SECTION: system-manager readiness (prereg 8.1 row 7)
# ---------------------------------------------------------------------------
# Presence of `systemctl` proves nothing about the manager: a denied bus, an
# isolated PID or mount namespace, or a polkit refusal all make the query fail
# BEFORE any unit state is returned, and a later run would then read "could not
# ask" as "unit not active" - WP-I audit F3 and pattern 1.
# The query is `show --property=Version` against the SYSTEM manager. It is
# read-only, it takes no unit, and it is answered by the manager itself over the
# system bus. `systemctl --version` is deliberately NOT used: it prints the
# client's own version without contacting any manager, so it could satisfy a
# readiness check while the bus was unreachable - the sentence would outrun the
# probe (pattern 9).
# The environment is CLEARED for the child (pattern 4): sd-bus honours
# environment variables that redirect the system bus address, so a query run
# with the caller's environment could be answered by an operator-controlled
# decoy. `env -i` with an explicit LC_ALL=C removes that channel and pins the
# locale of the response in the same step. The binary is the absolute path from
# the inventory, never a fresh PATH search.
# Everything short of a complete, single-line, exactly-shaped `Version=` answer
# is `system_manager_unreachable`, the prereg row-7 token, with rc and a detail
# class. Fail closed in every direction.
p0_assert_system_manager_ready() {
    local raw rc=0 value detail
    raw="$(LC_ALL=C "$P0_ENV" -i LC_ALL=C "$P0_SYSTEMCTL" --system --no-pager show --property=Version 2>&1)" || rc=$?
    if [ "$rc" -ne 0 ]; then
        case "$rc" in
            126) detail="invocation_found_but_not_executable" ;;
            127) detail="invocation_command_not_found" ;;
            *)   detail="manager_query_nonzero_status" ;;
        esac
        p0_sanitize "$raw"
        p0_stop "system_manager_unreachable rc=$rc detail=$detail text=[$P0_SAFE]"
    fi
    case "$raw" in
        *$'\r'*|*$'\n'*)
            p0_sanitize "$raw"
            p0_stop "system_manager_unreachable rc=$rc detail=response_multiline text=[$P0_SAFE]" ;;
    esac
    case "$raw" in
        "Version="?*) value="${raw#Version=}" ;;
        *) p0_sanitize "$raw"
           p0_stop "system_manager_unreachable rc=$rc detail=response_unparseable text=[$P0_SAFE]" ;;
    esac
    case "$value" in
        *[![:print:]]*)
            p0_stop "system_manager_unreachable rc=$rc detail=response_unprintable_value" ;;
    esac
    p0_sanitize "$value"
    printf 'P0_system_manager_ready bus=system query=show_property_Version response_key=Version response_value=[%s] env=cleared binary=%s scope=this_login_pid_and_mount_namespaces manager_identity=not_established\n' \
        "$P0_SAFE" "$P0_SYSTEMCTL"
}

printf 'P0_SECTION system_manager\n'
p0_assert_system_manager_ready

# ---------------------------------------------------------------------------
# SECTION: interpreter executability (WP-I audit F1)
# ---------------------------------------------------------------------------
# The per-SHA venv interpreter must be provably executable by THIS login before
# any parity or version claim depends on running it. An exec denial gets its own
# STOP reason and is never a version or package-parity FAIL: an unprivileged
# process that could not run the verifier has not observed package drift.
# Object arms are FAIL, execution arms are STOP, and the boundary between them
# is the audit-1 F5 ruling: an exact-shape ENOENT on a preregistered absolute
# path proves the parent chain was searchable and observes a missing
# preregistered object.

# Local, temp-free path classifier. Same six tokens as `rp0_probe_path`, plus a
# stricter failure branch: the raw diagnostic must contain no CR or LF, must
# name exactly one errno class, and must match the exact C-locale GNU coreutils
# shape for the probed path. `statx` and `stat` spellings are both accepted
# because coreutils changed producers; nothing else is. Sets globals rather than
# printing, so that a STOP raised inside it cannot be captured into a caller's
# variable by a command substitution.
p0_classify_stat_shape() {
    local p="$1" raw="$2"
    P0_SHAPE=""
    case "$raw" in
        "stat: cannot statx '$p': $P0_EACCES_TEXT"|"stat: cannot stat '$p': $P0_EACCES_TEXT")
            P0_SHAPE="eacces" ;;
        "stat: cannot statx '$p': $P0_ENOENT_TEXT"|"stat: cannot stat '$p': $P0_ENOENT_TEXT")
            P0_SHAPE="enoent" ;;
    esac
}

p0_probe_kind() {
    local p="$1" raw rc=0 sub subrc=0 n_eacces n_enoent classes
    P0_KIND=""; P0_FKIND=""
    raw="$(LC_ALL=C "$P0_STAT" -c '%F' -- "$p" 2>&1)" || rc=$?
    if [ "$rc" -eq 0 ]; then
        p0_sanitize "$raw"
        case "$P0_SAFE" in
            "symbolic link")
                sub="$(LC_ALL=C "$P0_STAT" -L -c '%F' -- "$p" 2>&1)" || subrc=$?
                if [ "$subrc" -eq 0 ]; then
                    p0_sanitize "$sub"
                    case "$P0_SAFE" in
                        "regular file"|"regular empty file") P0_FKIND="regular" ;;
                        "directory")                        P0_FKIND="dir" ;;
                        "")  p0_stop "link_target_probe_empty path=$p rc=0" ;;
                        *)   P0_FKIND="other" ;;
                    esac
                    P0_KIND="link_live"
                    return 0
                fi
                p0_classify_stat_shape "$p" "$sub"
                p0_sanitize "$sub"
                case "$P0_SHAPE" in
                    enoent) P0_KIND="link_dangling"; P0_FKIND="absent"; return 0 ;;
                esac
                p0_stop "link_target_probe_error path=$p rc=$subrc detail=$P0_SAFE" ;;
            "regular file"|"regular empty file") P0_KIND="regular"; P0_FKIND="regular"; return 0 ;;
            "directory")                         P0_KIND="dir";     P0_FKIND="dir";     return 0 ;;
            "")                                  p0_stop "path_probe_empty path=$p rc=0" ;;
            *)                                   P0_KIND="other";   P0_FKIND="other";   return 0 ;;
        esac
    fi
    case "$raw" in
        *$'\r'*|*$'\n'*)
            p0_sanitize "$raw"
            p0_stop "path_probe_multiline path=$p rc=$rc detail=$P0_SAFE" ;;
    esac
    p0_count_substr "$raw" "$P0_EACCES_TEXT"; n_eacces="$P0_COUNT"
    p0_count_substr "$raw" "$P0_ENOENT_TEXT"; n_enoent="$P0_COUNT"
    classes=$(( n_eacces + n_enoent ))
    if [ "$classes" -gt 1 ]; then
        p0_sanitize "$raw"
        p0_stop "path_probe_ambiguous path=$p rc=$rc classes=$classes eacces=$n_eacces enoent=$n_enoent detail=$P0_SAFE"
    fi
    p0_classify_stat_shape "$p" "$raw"
    p0_sanitize "$raw"
    case "$P0_SHAPE" in
        enoent) P0_KIND="absent"; P0_FKIND="absent"; return 0 ;;
        eacces) p0_stop "path_probe_denied path=$p rc=$rc detail=$P0_SAFE" ;;
    esac
    p0_stop "path_probe_unclassified path=$p rc=$rc detail=$P0_SAFE"
}

# The venv root itself, before the interpreter inside it. Verifying the
# container before the contents is pattern 3: a symlinked or non-canonical root
# would put the interpreter claim on an object the accepted state never named.
p0_assert_venv_root() {
    local d="$1" canon rc=0
    p0_probe_kind "$d"
    case "$P0_KIND" in
        dir) : ;;
        absent) p0_fail "venv_root_absent path=$d detail=preregistered_path_observed_missing" ;;
        link_live|link_dangling)
            p0_fail "venv_root_is_symlink kind=$P0_KIND path=$d" ;;
        *) p0_fail "venv_root_kind_unexpected kind=$P0_KIND path=$d expected=dir" ;;
    esac
    canon="$(LC_ALL=C "$P0_READLINK" -f -- "$d" 2>&1)" || rc=$?
    if [ "$rc" -ne 0 ]; then
        p0_sanitize "$canon"
        p0_stop "venv_root_canonicalization_failed path=$d rc=$rc detail=$P0_SAFE"
    fi
    p0_sanitize "$canon"
    [ "$canon" = "$d" ] \
        || p0_fail "venv_root_not_literal_canonical path=$d canonical=$P0_SAFE"
    p0_record_metadata "venv_root" "$d"
    printf 'P0_venv_root path=%s kind=dir mode=%s owner_numeric=%s canonical=literal\n' \
        "$d" "$P0_META_MODE" "$P0_META_OWNER"
}

p0_assert_interpreter_executable() {
    local py="$1" raw rc=0 version major minor rest
    p0_probe_kind "$py"
    case "$P0_KIND" in
        regular) : ;;
        link_live)
            # A venv interpreter is normally a symlink; the link itself is not
            # deviant, but a link whose target is not a regular file is.
            [ "$P0_FKIND" = "regular" ] \
                || p0_fail "interpreter_target_kind_unexpected kind=$P0_FKIND path=$py expected=regular" ;;
        absent)
            p0_fail "interpreter_absent path=$py detail=preregistered_path_observed_missing_parent_search_succeeded" ;;
        link_dangling)
            p0_fail "interpreter_symlink_dangling path=$py" ;;
        *)
            p0_fail "interpreter_kind_unexpected kind=$P0_KIND path=$py expected=regular_or_live_symlink" ;;
    esac
    p0_record_metadata "interpreter" "$py"
    printf 'P0_interpreter_object path=%s kind=%s target_kind=%s mode=%s owner_numeric=%s\n' \
        "$py" "$P0_KIND" "$P0_FKIND" "$P0_META_MODE" "$P0_META_OWNER"
    # access(2) first: the kernel answers the execute question for THIS caller,
    # including ACLs and LSM policy, with no diagnostic string involved.
    [ -x "$py" ] \
        || p0_stop "interpreter_not_executable path=$py mechanism=access_builtin_x detail=exec_permission_denied_to_this_login"
    # Then a real execution, with the environment cleared and the interpreter in
    # isolated mode: PYTHONPATH, PYTHONSTARTUP, PYTHONHOME and a current-working
    # -directory shadow are all removed as channels (pattern 4, audit-2 A2-F1).
    # `-I` also implies -E and -s. Only `sys` is imported and only two integers
    # are printed; nothing is written and nothing is installed.
    raw="$(LC_ALL=C "$P0_ENV" -i LC_ALL=C "$py" -I -c 'import sys; print("P0PY %d.%d" % sys.version_info[:2])' 2>&1)" || rc=$?
    if [ "$rc" -ne 0 ]; then
        p0_sanitize "$raw"
        case "$rc" in
            126) p0_stop "interpreter_exec_denied path=$py rc=126 detail=found_but_could_not_be_executed_by_this_login text=[$P0_SAFE]" ;;
            127) p0_stop "interpreter_exec_failed path=$py rc=127 detail=interpreter_or_its_loader_not_found text=[$P0_SAFE]" ;;
            *)   p0_stop "interpreter_exec_failed path=$py rc=$rc detail=nonzero_interpreter_status text=[$P0_SAFE]" ;;
        esac
    fi
    case "$raw" in
        *$'\r'*|*$'\n'*)
            p0_sanitize "$raw"
            p0_stop "interpreter_probe_multiline path=$py detail=$P0_SAFE" ;;
    esac
    case "$raw" in
        "P0PY "?*) version="${raw#P0PY }" ;;
        *) p0_sanitize "$raw"
           p0_stop "interpreter_probe_unparsable path=$py detail=[$P0_SAFE] expected=P0PY_major.minor" ;;
    esac
    case "$version" in
        *.*) major="${version%%.*}"; rest="${version#*.}"; minor="$rest" ;;
        *)   p0_stop "interpreter_probe_unparsable path=$py detail=[$version] expected=P0PY_major.minor" ;;
    esac
    case "$major" in ""|*[!0-9]*) p0_stop "interpreter_probe_unparsable path=$py field=major value=[$major]" ;; esac
    case "$minor" in ""|*[!0-9]*) p0_stop "interpreter_probe_unparsable path=$py field=minor value=[$minor]" ;; esac
    # The version is RECORDED, never compared. The 3.12 predicate and the
    # 56-entry lock parity are RO-stage rows (feasibility B1); asserting either
    # here would be a parity claim resting on a premise this section exists to
    # establish.
    printf 'P0_interpreter path=%s exec=ok env=cleared isolated=yes reported_version=%s.%s adjudication=recorded_not_compared\n' \
        "$py" "$major" "$minor"
}

printf 'P0_SECTION interpreter\n'
p0_assert_venv_root "$P0_VENV_ROOT"
p0_assert_interpreter_executable "$P0_PY"

# ---------------------------------------------------------------------------
# SECTION: out of scope, stated in the evidence
# ---------------------------------------------------------------------------
# Silence about an excluded check is how a scope reduction becomes an unnoticed
# coverage loss. Everything P0 does not implement is named here.
printf 'P0_SECTION out_of_scope\n'
printf 'P0_out_of_scope class=BLOCKED-UPSTREAM group=C checks=C1,C2,C3,C4,C5 reason=mutating_host_or_credential_and_network_authority_absent implemented=no\n'
printf 'P0_out_of_scope class=DEFER-ROOT-SIDE item=B1a_install_manifest_field channel=RPD-VERIFY implemented=no\n'
printf 'P0_out_of_scope class=DEFER-ROOT-SIDE item=B3_any_path_inside_protected_metadata_dirs channel=RPD-VERIFY implemented=no\n'
printf 'P0_out_of_scope class=DEFER-ROOT-SIDE item=B4_manager_properties_if_readiness_absent channel=RPD-VERIFY implemented=no\n'
printf 'P0_out_of_scope class=DEFER-ROOT-SIDE item=B6_ufw_status_and_service_netns_binding channel=RPD-VERIFY implemented=no\n'
printf 'P0_out_of_scope class=RO_STAGE item=every_prereg_8.2_row stage=ro implemented=no\n'

# ---------------------------------------------------------------------------
# SECTION: terminal claim
# ---------------------------------------------------------------------------
# Written by stating the claim and then deleting every word the executed
# predicates cannot establish. What survives is the log line.
printf 'P0_SECTION done\n'
printf 'P0_claim establishes=executing_numeric_identity_of_this_login,forbidden_gid_non_membership,resolution_and_executability_of_the_11_listed_RO_tools,evidence_stdout_bound_to_create_once_leaf,system_manager_answered_a_Manager_property_query_over_the_system_bus_from_this_login_namespaces,venv_interpreter_leaf_kind_and_executability,self_namespace_identities_recorded\n'
printf 'P0_claim does_not_establish=any_RO_row_host_state,tool_provenance_or_distribution_identity,round1_4_probe_execution_environment_binding,identity_of_the_manager_that_answered,binding_of_these_namespaces_to_any_service_or_to_the_host_initial_namespaces,interpreter_intermediate_component_or_symlink_target_binding,interpreter_version_or_package_parity,anything_under_the_protected_metadata_directories,anything_about_group_C\n'
printf 'P0_claim scope=this_login_only identity=numeric_only mutation=none_in_this_block evidence_leaf=allocated_by_RP0-BOOTSTRAP child_env=mixed coreutils_launch=recorded_absolute_after_PATH_resolution inherited_env=stat_readlink_id cleared_env=systemctl_and_interpreter_only cwd=caller_inherited tmpdir=caller_inherited_or_unset\n'
printf 'P0 PASS\n'
