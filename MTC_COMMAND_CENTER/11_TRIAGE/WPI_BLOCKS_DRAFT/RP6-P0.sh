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
# query over the system bus from the externally attested execution domain, that
# the per-SHA venv interpreter can actually be executed, and that this login's
# user, mount, PID and network namespaces plus root object identity match the
# deploy-channel values frozen into this block. The RO stage is admissible only
# if P0 held. Folding the two together would let a run assert a result whose
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
# NUMERIC IDENTITY ONLY (pattern 8). ADMISSION is numeric only: `stat` is never
# asked for %U or %G; `id` is only ever asked for -u, -g and -G; every
# preregistered identity input is numeric; and no name is ever compared or
# asserted anywhere in this block. Two names ARE queried: the account-resolution
# section below asks the resolver database for `gatea` and `mtc-bridge` via the
# pinned `getent passwd` and captures the returned name, gecos, home and shell
# fields, but those fields are RECORDED AS DIAGNOSTICS ONLY and no verdict
# depends on them - the verdicts compare the record's uid/gid against the live
# numerics and the preregistered numerics. A rendered name is an answer from a
# database this run does not control: which NSS source answered is not
# established here and is disclosed in the terminal claim's
# does_not_establish list.
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
# STATED PRODUCER ASSUMPTION (audit-2 R2 nit 2). The two FAIL arms are reached
# only by matching the exact C-locale GNU coreutils `stat`/`statx` failure shape,
# which carries the INVOKED absolute argv[0] as its prefix. That is an assumption
# about the producer, not a universal: uutils coreutils renders the BASENAME of
# argv[0], so on a uutils-coreutils host no shape matches, every object arm
# returns `path_probe_unclassified` at rc 3, and the audit-1 F1 class returns
# fail-closed - P0 refuses instead of mis-ruling, and the shape must be re-pinned
# before such a host is preregistered.
#
# MUTATION SURFACE. The SHELL source of this block creates no file, no directory
# and no temporary file, opens nothing for writing, and changes no mode, owner,
# ACL, group, service or network state. It duplicates its own stdout onto fd 8
# and closes it again, which is a descriptor operation, not a filesystem one. The
# evidence directory and the evidence leaf are created by the ACCEPTED
# RP0-BOOTSTRAP before this block runs; that allocation is the bootstrap's
# mutation and is not claimed here as none. This block asserts the allocation
# happened and that its own stdout is bound to that leaf, and refuses to run
# otherwise.
# "No write primitive in the shell source" is NOT the same sentence as "this
# block wrote nothing" (audit-3 F1). Every external child this block starts runs
# with this login's authority, and P0 has no attestation channel for any of those
# binaries, so what a tool does INSIDE its own process is disclosed as
# unestablished rather than claimed as none. One channel is closed positively
# because it was executed and shown open: the per-SHA venv interpreter is launched
# with `-I -S`, so the venv's own `site` startup - `site-packages/*.pth` executable
# `import` lines and any `sitecustomize`/`usercustomize` module in that tree - is
# not read and not executed before the intended `-c` body. Under `-I` alone it was,
# and a forged one-line `.pth` really did write a marker file while the block still
# emitted its accepted `P0PY` line.
# The external-child surface is not a fixed count. Metadata, evidence-binding,
# identity and namespace probes execute the recorded absolute stat/readlink/id
# paths with the caller environment inherited and LC_ALL forced to C. Only the
# Manager-level `systemctl show` query and the isolated interpreter invocation
# use `env -i`, and the manager query additionally carries the pinned `timeout`
# INSIDE that cleared environment, so the process that decides whether the query
# was bounded runs under the same cleared environment as the query it bounds.
# Every launch keeps the caller working directory; TMPDIR is caller-inherited for
# stat/readlink/id and absent from the two cleared launches.
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
P0_DEVICE=""
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

# `readlink -v` is used at every readlink call so a nonzero status has a real
# diagnostic. This formatter keeps `detail=` nonempty and records whether the
# merged diagnostic was one printable record; malformed diagnostic streams are
# still STOP, but are never emitted as an empty or ambiguous key=value field.
p0_prepare_readlink_detail() {
    local raw="${1-}"
    P0_RESOLUTION="single_printable_record"
    if [ -z "$raw" ]; then
        P0_SAFE="readlink_diagnostic_absent"
        P0_RESOLUTION="absent"
        return 0
    fi
    case "$raw" in
        *$'\r'*|*$'\n'*)
            P0_SAFE="readlink_diagnostic_multiline_suppressed"
            P0_RESOLUTION="multiline"
            return 0 ;;
        *[![:print:]]*)
            P0_SAFE="readlink_diagnostic_nonprintable_suppressed"
            P0_RESOLUTION="nonprintable"
            return 0 ;;
    esac
    p0_sanitize "$raw"
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
# expansion of the map is deliberate for WORD SPLITTING - the maps are
# space-separated - and it is made safe against BOTH splitting and pathname
# expansion: every value that can enter either map is refused earlier unless it
# is printable and contains no whitespace (so a value that could split is a STOP
# before it reaches this function), the pin-path charset gate refuses the glob
# metacharacters `*`, `?` and `[` (Finding 3), AND the split below runs under
# `set -f` so a metacharacter some future map admits still splits literally
# rather than being rewritten by cwd entries. The earlier "deliberate and safe"
# comment certified safety against word splitting only and was silent about the
# pathname expansion the same unquoted expansion performs; that gap is closed.
p0_lookup() {
    local map="$1" want="$2" e
    P0_LOOKUP=""
    # Pathname expansion is disabled for the split (Finding 3, Claude round-6
    # re-audit): the unquoted `$map` performs word splitting AND pathname
    # expansion. Word splitting is intended; pathname expansion is not, and a
    # value carrying a glob metacharacter would otherwise be rewritten by cwd
    # entries. Pin paths are refused those bytes at the input charset gate; this
    # `set -f` is defense in depth over every map this helper ever splits. Glob
    # mode is restored to the block default (on) on both exits, matching the two
    # existing `set -f`/`set +f` pairs (nit 1 remains open for all three).
    set -f
    for e in $map; do
        case "$e" in
            "$want"=*) P0_LOOKUP="${e#*=}"; set +f; return 0 ;;
        esac
    done
    set +f
    return 1
}

# --- preregistered constants ------------------------------------------------
# The candidate SHA is the frozen candidate of prereg section 2 and is never
# derived at run time.
P0_CAND="2ce41e34bceb599d80af24c5c33d835820ec321b"
P0_NS_USER_PATH="/proc/self/ns/user"
P0_NS_NET_PATH="/proc/self/ns/net"
P0_NS_PID_PATH="/proc/self/ns/pid"
P0_NS_MNT_PATH="/proc/self/ns/mnt"
P0_FD_SELF="/proc/self/fd/8"
P0_EACCES_TEXT="Permission denied"
P0_ENOENT_TEXT="No such file or directory"
P0_FIXED_ATTESTED_USER_NS='<PIN-AT-FREEZE>'
P0_FIXED_ATTESTED_MNT_NS='<PIN-AT-FREEZE>'
P0_FIXED_ATTESTED_PID_NS='<PIN-AT-FREEZE>'
P0_FIXED_ATTESTED_NET_NS='<PIN-AT-FREEZE>'
P0_FIXED_ATTESTED_ROOT_MOUNT_ID='<PIN-AT-FREEZE>'
# The trusted system interpreter the RO stage's two accepting adjudicators run
# under (RP7 `WPI_TRUSTED_PYTHON`). It is a freeze-gate input for exactly the
# reason the namespace pins above are: `/usr/bin/python3` is a symlink on the
# target family and no symlinked object is admissible as a bound RO tool, so the
# resolved non-symlink leaf is supplied by the deploy channel and frozen here.
# P0 does not execute it; P0 refuses to admit a pin for it that disagrees with
# the frozen value, so the tool the RO stage will trust is the tool P0 checked.
P0_FIXED_TRUSTED_PYTHON='<PIN-AT-FREEZE>'
# Correction 7 (Codex round-7, from the section-10.1 reconciliation, Lead-
# verified): the frozen deploy-channel absolute path of every OTHER preregistered
# tool. The nine RO-shared tools (stat readlink env find sha256sum systemctl ss
# curl timeout) mirror the frozen WPI_TOOL_PINS of RP7-WPI-RO.sh@d6a976aa; id and
# getent are P0-only. Each is a freeze-gate input for the same reason the
# namespace pins and P0_FIXED_TRUSTED_PYTHON are: P0 refuses to admit a pin that
# disagrees with its frozen literal, so the reachable executable set IS the frozen
# set and is derivable from this source - the property the Stage-1 path-scope
# proof needs. The unpinned `command -v` fallback is deleted in p0_resolve_tool,
# so an unpinned tool is a STOP, not a PATH-resolved admission.
P0_FIXED_STAT='<PIN-AT-FREEZE>'
P0_FIXED_READLINK='<PIN-AT-FREEZE>'
P0_FIXED_ENV='<PIN-AT-FREEZE>'
P0_FIXED_FIND='<PIN-AT-FREEZE>'
P0_FIXED_SHA256SUM='<PIN-AT-FREEZE>'
P0_FIXED_SYSTEMCTL='<PIN-AT-FREEZE>'
P0_FIXED_SS='<PIN-AT-FREEZE>'
P0_FIXED_CURL='<PIN-AT-FREEZE>'
P0_FIXED_TIMEOUT='<PIN-AT-FREEZE>'
P0_FIXED_ID='<PIN-AT-FREEZE>'
P0_FIXED_GETENT='<PIN-AT-FREEZE>'
# Row-9 deadline. Preregistered block literals, not operator inputs and not
# learned at run time: a bound supplied by the environment under test could be
# raised to infinity by that same environment.
P0_MANAGER_QUERY_BUDGET_S=10
P0_MANAGER_QUERY_KILL_AFTER_S=5

# --- the RO-stage tool inventory, regenerated from the FROZEN RO block -------
# Audit-3 F3. This list is no longer written from the prereg prose: its RO half
# is a mirror of the tool set the frozen RO executable actually validates and
# invokes, and its second half is the P0-only remainder. The frozen basis is
#   RP7-WPI-RO.sh, commit d6a976aa,
#   sha256 23e55667bec2453e21605b3551d5802b9cc28a82040789f3ead988b69aa01aad,
#   70941 bytes, `WPI_TOOL_PINS` validator (RP7-WPI-RO.sh:594, count gate :610,
#   binding loop :611).
# A stale inventory is executable, not documentary: RP6 previously omitted
# `timeout` - which the RO stage really runs - and so could PASS without ever
# checking it, could REJECT a complete RP7 pin set as an unknown tool, and could
# STOP on a missing `grep`/`awk` that neither stage invokes. The drift test in
# SELF_QA_RP6.md re-derives the RO half from the frozen RP7 bytes and fails if
# the two ever disagree again.
#
# RO half - every tool the frozen RO block pins, in its order:
# stat, readlink, find  - B3 scoped walks, terminal metadata stat, and the
#                         literal-canonical predicate.
# env                   - pinned, cleared-environment launch of every RO
#                         evidence-producing child (pattern 4).
# sha256sum             - B1a installed-lock digest, B2 fragment digest.
# systemctl             - prereg 8.1 rows 7 and 9; B2/B4 manager-backed rows.
# ss                    - B6 listener set.
# curl                  - B5 loopback control-endpoint GET.
# timeout               - the bounding wrapper of every RO capture
#                         (RP7-WPI-RO.sh:212), and of this block's own row-9
#                         manager query below.
# python3               - the pinned trusted interpreter both RO accepting
#                         adjudicators run under with `-I -S` (RP7-WPI-RO.sh:907
#                         and :1074). P0 never executes it; P0 establishes that
#                         it resolves, is executable by this login, and agrees
#                         with the frozen trusted-python pin.
# P0-only half - required by this block and by no RO row:
# id                    - prereg 8.1 rows 1-2 numeric caller identity.
# getent                - prereg 8.1 rows 1-3 (repair C13): unique complete
#                         passwd-record resolution of the `gatea` and
#                         `mtc-bridge` names to numeric uid/gid. Names are
#                         diagnostic only; only the numerics are compared.
# DROPPED this round, because neither the frozen RO block nor this block
# invokes them: `grep` (this block counts literal substrings with builtins -
# `p0_count_substr`, audit-1 F6) and `awk` (the budgeted-sweep clock it was
# listed for is not reachable from any tool the frozen RO block pins).
# `stat` is listed first only so that the metadata pass has a resolved absolute
# `stat` to use; resolution and executability themselves are decided by shell
# builtins alone, so the order carries no privilege.
# NOT in this list, deliberately: the root-side pinned python3 of RPD-VERIFY
# (root-side, out of P0 scope), and the per-SHA venv interpreter, which has its
# own preregistered absolute path and its own arm below - and which is a
# different object from the trusted `python3` above, on purpose.
P0_RP7_RO_TOOLS="stat readlink env find sha256sum systemctl ss curl timeout python3"
P0_P0_ONLY_TOOLS="id getent"
P0_RO_TOOLS="$P0_RP7_RO_TOOLS $P0_P0_ONLY_TOOLS"
# Expected pin count = the inventory size (correction 7). Derived once from the
# frozen literal above so it cannot drift from the list; P0_RO_TOOLS contains no
# glob metacharacter, so this unquoted split is word-splitting only and matches
# the two existing $P0_RO_TOOLS iterations below.
P0_TOOL_COUNT_EXPECTED=0
for p0_t in $P0_RO_TOOLS; do P0_TOOL_COUNT_EXPECTED=$(( P0_TOOL_COUNT_EXPECTED + 1 )); done

# ---------------------------------------------------------------------------
# SECTION: prerequisites
# ---------------------------------------------------------------------------
# Asserting the prerequisites is what keeps the 0/1/3 contract honest: without
# RP0-LIB the first library call would abort under `set -e` with rc 127, and
# without RP0-BOOTSTRAP this block would write its evidence to whatever stdout
# happened to be.
printf 'P0_SECTION header candidate=%s block=RP6-P0 stage=p0\n' "$P0_CAND"
printf 'P0_SECTION prerequisites\n'

# F2 (Codex final-audit round-5; reworked round-7 A4): `command -v` only proves a
# name resolves; it accepts a PATH executable (or alias) of the same name, and the
# block then CALLS the first symbol below. That made the RP0-LIB "sourced" claim
# satisfiable by an unrelated PATH file - a pre-inventory child-execution channel
# before P0 has established any tool premise. The required symbols must be SHELL
# FUNCTIONS, so assert command TYPE with the NON-OVERRIDABLE builtin: an exact
# `builtin type -t ... = function` check for both symbols before either is called.
# The `builtin` prefix defeats a caller-defined `type(){ printf 'function\n'; }`
# that would otherwise forge `function` and let the missing real symbol fall
# through to command_not_found_handle while both guards passed (Codex round-7 A4
# falsification). This matches the accepted RP7-WPI-RO.sh form (RP7-WPI-RO.sh:646-
# 647). A PATH-shadow file or alias of either name no longer satisfies this
# precondition and is never executed. (`command -v` is still correct inside
# p0_resolve_tool below, where the intent IS to resolve a PATH tool to an absolute
# path.)
# HONEST BOUND (Codex round-7 A4): function type proves only that the two names
# resolve as shell functions IN THIS SHELL; it does NOT prove they came from
# RP0-LIB, because a caller could source an unrelated same-name function first.
# The block therefore claims only what is established - the required shell
# functions were present and exercised (rp0_require_safe_component is called on
# the evidence identifiers below) - and NOT that RP0-LIB as an identity was
# sourced. Binding the definitions to the accepted RP0-LIB identity would require
# a frozen hash of RP0-LIB.sh and is outside this round.
[ "$(builtin type -t rp0_require_safe_component 2>/dev/null)" = function ] \
    || p0_stop "rp0_lib_not_sourced predicate=rp0_require_safe_component detail=not_a_shell_function"
[ "$(builtin type -t rp0_allocate_evidence_dir 2>/dev/null)" = function ] \
    || p0_stop "rp0_lib_not_sourced predicate=rp0_allocate_evidence_dir detail=not_a_shell_function"

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
printf 'P0_prereq required_functions=present_and_exercised bootstrap=ran run_id=%s stage=%s dir=%s leaf=%s\n' \
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

# P0_STATE_UID / P0_STATE_GID - the preregistered NUMERIC uid/gid of the
# dynamically allocated mtc-bridge service account (prereg section 2,
# WPI_STATE_UID=999 / WPI_STATE_GID=988; repair C13). Deliberately not equal
# to the route login's identity and, by design, NOT assumed uid==gid
# (999 != 988). Same mechanism as P0_EXPECT_UID: an rc-3 pre-check, then a
# `:?` fail-closed backstop that fires only if the pre-check is removed (the
# F4 pattern). Zero is refused as an INPUT for the same reason P0_EXPECT_UID
# refuses it: the service account is unprivileged, so a preregistration naming
# uid/gid 0 is a plumbing error, not a host observation.
p0_require_uint P0_STATE_UID "${P0_STATE_UID:-}" 1
: "${P0_STATE_UID:?preregistered numeric uid of the mtc-bridge service account is required}"
p0_require_uint P0_STATE_GID "${P0_STATE_GID:-}" 1
: "${P0_STATE_GID:?preregistered numeric gid of the mtc-bridge service account is required}"

# P0_FORBIDDEN_GIDS - the preregistered NUMERIC gids the feasibility ledger
# asserts this login is NOT in (prereg 8.1 row 2: the root group and the
# state/log group). gid 0 is a legitimate member of this list, so zero is
# allowed here.
[ -n "${P0_FORBIDDEN_GIDS:-}" ] \
    || p0_stop "input_missing name=P0_FORBIDDEN_GIDS detail=preregistered_numeric_gid_list_never_derived_here"
: "${P0_FORBIDDEN_GIDS:?preregistered numeric forbidden-gid list is required}"
# F3 (Codex final-audit round-5): the raw value was split by an UNQUOTED
# `for ... in $P0_FORBIDDEN_GIDS`, so pathname expansion ran BEFORE
# p0_require_uint saw each item. With P0_FORBIDDEN_GIDS='*' and a cwd holding
# entries named 0 and 988, the wildcard expanded to those two numeric names and
# the malformed ledger was admitted (count=2); the same input in an empty cwd
# STOPped, so cwd contents rewrote the ledger. Two independent defenses: (1)
# validate the COMPLETE raw value against an exact digits-plus-separator grammar
# BEFORE any expansion, so a wildcard or any non-digit/non-space byte is a STOP
# regardless of cwd; (2) split with pathname expansion disabled (`set -f`) so no
# surviving metacharacter can ever reach the per-item check. `set -f`/`set +f`
# toggles only the glob flag and leaves the block's `-Eeuo pipefail` intact; on
# the in-loop STOP path p0_stop exits the shell, so re-enabling is unreachable
# and irrelevant there.
case "$P0_FORBIDDEN_GIDS" in
    *[!0-9[:space:]]*)
        p0_stop "input_charset name=P0_FORBIDDEN_GIDS value=[$P0_FORBIDDEN_GIDS] expected=decimal_digits_and_separators_only" ;;
esac
P0_FORBIDDEN_GID_COUNT=0
set -f
for p0_g in $P0_FORBIDDEN_GIDS; do
    p0_require_uint P0_FORBIDDEN_GIDS_ENTRY "$p0_g" 0
    P0_FORBIDDEN_GID_COUNT=$(( P0_FORBIDDEN_GID_COUNT + 1 ))
done
set +f
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
case "$P0_VENV_ROOT" in
    *'//'*) p0_stop "input_not_canonical_spelling name=P0_VENV_ROOT value=[$P0_VENV_ROOT] detail=repeated_separator" ;;
esac
# The venv root must be bound to the frozen candidate. A P0 that validated some
# other interpreter would establish a premise about the wrong object.
case "$P0_VENV_ROOT" in
    */"$P0_CAND") : ;;
    *) p0_stop "input_not_candidate_bound name=P0_VENV_ROOT expected_basename=$P0_CAND" ;;
esac

# P0_TOOL_PINS - the FROZEN pin table (correction 7, Codex round-7): exactly one
# entry `name=/absolute/path` per preregistered tool, separated by spaces. Every
# tool is pinned and every pin must equal that tool's frozen deploy-channel
# path; `python3` must equal P0_FIXED_TRUSTED_PYTHON. There is NO unpinned
# fallback (p0_resolve_tool), so the reachable executable set IS the frozen set
# and is derivable from this source - the property the Stage-1 path-scope proof
# needs. R5-F1 keeps the python3 pin load-bearing by construction; correction 7
# makes the other eleven load-bearing too. Omitting any tool, pinning one to a
# path that differs from its frozen literal, an unknown tool, a duplicate, a
# non-absolute path, or a path carrying whitespace or a glob metacharacter, is a
# STOP.
P0_TOOL_PINS="${P0_TOOL_PINS:-}"
P0_PIN_COUNT=0
P0_PIN_SEEN=" "
P0_TRUSTED_PYTHON_BOUND=no

# p0_frozen_tool_path - the frozen deploy-channel literal for a tool name
# (correction 7), or return 1 for a name not in the inventory. Sets P0_FROZEN_PIN
# to the literal's value and P0_FROZEN_CONST_NAME to the literal's identifier
# (R9): the freeze-unfilled STOP must carry the name= of the constant it names, so
# the emit site stays grammared for every tool, not just python3.
p0_frozen_tool_path() {
    P0_FROZEN_PIN=""
    P0_FROZEN_CONST_NAME=""
    case "$1" in
        stat)      P0_FROZEN_PIN="$P0_FIXED_STAT"; P0_FROZEN_CONST_NAME=P0_FIXED_STAT ;;
        readlink)  P0_FROZEN_PIN="$P0_FIXED_READLINK"; P0_FROZEN_CONST_NAME=P0_FIXED_READLINK ;;
        env)       P0_FROZEN_PIN="$P0_FIXED_ENV"; P0_FROZEN_CONST_NAME=P0_FIXED_ENV ;;
        find)      P0_FROZEN_PIN="$P0_FIXED_FIND"; P0_FROZEN_CONST_NAME=P0_FIXED_FIND ;;
        sha256sum) P0_FROZEN_PIN="$P0_FIXED_SHA256SUM"; P0_FROZEN_CONST_NAME=P0_FIXED_SHA256SUM ;;
        systemctl) P0_FROZEN_PIN="$P0_FIXED_SYSTEMCTL"; P0_FROZEN_CONST_NAME=P0_FIXED_SYSTEMCTL ;;
        ss)        P0_FROZEN_PIN="$P0_FIXED_SS"; P0_FROZEN_CONST_NAME=P0_FIXED_SS ;;
        curl)      P0_FROZEN_PIN="$P0_FIXED_CURL"; P0_FROZEN_CONST_NAME=P0_FIXED_CURL ;;
        timeout)   P0_FROZEN_PIN="$P0_FIXED_TIMEOUT"; P0_FROZEN_CONST_NAME=P0_FIXED_TIMEOUT ;;
        id)        P0_FROZEN_PIN="$P0_FIXED_ID"; P0_FROZEN_CONST_NAME=P0_FIXED_ID ;;
        getent)    P0_FROZEN_PIN="$P0_FIXED_GETENT"; P0_FROZEN_CONST_NAME=P0_FIXED_GETENT ;;
        python3)   P0_FROZEN_PIN="$P0_FIXED_TRUSTED_PYTHON"; P0_FROZEN_CONST_NAME=P0_FIXED_TRUSTED_PYTHON ;;
        *) return 1 ;;
    esac
}

# R6-F3 (Codex round-7): pathname expansion ran on the unquoted $P0_TOOL_PINS
# split BEFORE the pin-charset gate, so a cwd crafted to hold a whole token like
# `stat=/usr/bin/stat` rewrote `stat=/usr/bin/sta*` into the clean pin and the
# loop accepted it (PIN_PARSE_ACCEPTED count=2 trusted=yes). Disable pathname
# expansion around this outer parse and RESTORE THE CALLER'S PRIOR noglob state
# (not the block default the other set -f pairs restore - nit 1 stays open only
# for those). The charset gate below and p0_lookup's set -f remain as depth.
case $- in *f*) P0_PRIOR_NOGLOB=1 ;; *) P0_PRIOR_NOGLOB=0 ;; esac
if [ "$P0_PRIOR_NOGLOB" -eq 0 ]; then set -f; fi
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
    case "$P0_PIN_SEEN" in
        *" $p0_pin_name "*)
            p0_stop "prereg_input_malformed name=P0_TOOL_PINS duplicate=$p0_pin_name" ;;
    esac
    case "$p0_pin_path" in
        /*) : ;;
        *) p0_stop "input_pin_not_absolute tool=$p0_pin_name path=[$p0_pin_path]" ;;
    esac
    case "$p0_pin_path" in
        *[![:print:]]*|*[[:space:]]*)
            p0_stop "input_pin_charset tool=$p0_pin_name expected=printable_without_whitespace" ;;
    esac
    # F3 (Claude round-6 re-audit): a pin path may otherwise carry a glob
    # metacharacter (`*`, `?` or `[`), and `p0_lookup`'s unquoted map split would
    # hand it to pathname expansion. A pin like `stat=/usr/bin/sta*` was admitted
    # at rc 0; in a cwd crafted so the expansion equals the PATH-resolved path it
    # could become a silently accepted `pinned_absolute`, contradicting the rule
    # that preregistered input must STOP rather than be laundered. Refuse the
    # three glob metacharacters here; `p0_lookup` additionally splits under
    # `set -f`, and round 7 wraps the OUTER parse in set -f (above), so a
    # metacharacter-bearing token can no longer be rewritten by cwd before it
    # reaches this gate.
    case "$p0_pin_path" in
        *'*'*|*'?'*|*'['*)
            p0_stop "input_pin_charset tool=$p0_pin_name expected=printable_without_glob_metacharacters" ;;
    esac
    # Correction 7: bind EVERY pin to its frozen deploy-channel literal. The
    # literal must be filled (not <PIN-AT-FREEZE>) and the pin must equal it
    # exactly. python3 keeps its existing binding to P0_FIXED_TRUSTED_PYTHON
    # (R5-F1); the other eleven tools bind to their own P0_FIXED_* literal. A
    # disagreement means the prelude named a different object from the one the
    # deploy channel froze for this tool, which is a STOP, never a silent
    # acceptance.
    p0_frozen_tool_path "$p0_pin_name" \
        || p0_stop "input_pin_unknown_tool name=P0_TOOL_PINS tool=$p0_pin_name inventory=[$P0_RO_TOOLS]"
    [ "$P0_FROZEN_PIN" != '<PIN-AT-FREEZE>' ] \
        || p0_stop "input_pin_freeze_unfilled tool=$p0_pin_name name=$P0_FROZEN_CONST_NAME detail=deploy_channel_value_never_derived_here"
    if [ "$p0_pin_name" = python3 ]; then
        [ "$p0_pin_path" = "$P0_FIXED_TRUSTED_PYTHON" ] \
            || p0_stop "input_pin_not_frozen_trusted_python tool=python3 pinned=$p0_pin_path frozen=$P0_FIXED_TRUSTED_PYTHON"
        P0_TRUSTED_PYTHON_BOUND=yes
    else
        [ "$p0_pin_path" = "$P0_FROZEN_PIN" ] \
            || p0_stop "input_pin_not_frozen_path tool=$p0_pin_name pinned=$p0_pin_path frozen=$P0_FROZEN_PIN"
    fi
    P0_PIN_SEEN="$P0_PIN_SEEN$p0_pin_name "
    P0_PIN_COUNT=$(( P0_PIN_COUNT + 1 ))
done
if [ "$P0_PRIOR_NOGLOB" -eq 0 ]; then set +f; fi

# Correction 7: reject omissions and extras. Exactly one pin per tool, every one
# of the twelve preregistered tools pinned, and the count is exactly twelve.
for p0_t in $P0_RO_TOOLS; do
    case "$P0_PIN_SEEN" in
        *" $p0_t "*) : ;;
        *) p0_stop "input_pin_omitted tool=$p0_t detail=every_preregistered_tool_requires_one_frozen_pin" ;;
    esac
done
[ "$P0_PIN_COUNT" -eq "$P0_TOOL_COUNT_EXPECTED" ] \
    || p0_stop "input_pin_count_unexpected count=$P0_PIN_COUNT expected=$P0_TOOL_COUNT_EXPECTED detail=exactly_one_frozen_pin_per_preregistered_tool"

# F1 (Codex final-audit round-5): the python3 freeze gate is load-bearing and
# its polarity was backwards. Supplying a python3 pin engages the
# P0_FIXED_TRUSTED_PYTHON checks inside the loop; OMITTING it left
# P0_TRUSTED_PYTHON_BOUND=no and skipped those checks entirely, so the sixth
# <PIN-AT-FREEZE> gate could be defeated by omission (a PIN_NONE or
# PIN_NO_PYTHON prelude reached the tool inventory at rc 0). After parsing every
# pin, REQUIRE that an explicit python3 entry was bound to
# P0_FIXED_TRUSTED_PYTHON before any host observation below. The detail field
# distinguishes omission (this post-loop gate) from a still-unfilled deploy-
# channel placeholder (the in-loop gate above): both are rc 3 under the same
# freeze-gate reason, so every missing-python3 prelude now STOPs the same way.
# Correction 7's omission-rejection loop above also forces a python3 entry; this
# re-check stays as the named python3-binding assertion.
[ "$P0_TRUSTED_PYTHON_BOUND" = yes ] \
    || p0_stop "input_pin_freeze_unfilled tool=python3 name=P0_FIXED_TRUSTED_PYTHON detail=trusted_python_pin_omitted_freeze_gate_load_bearing"

# Row 8 deploy-channel attestation inputs. The prelude supplies each value and
# the frozen block carries an identical literal. Missing input, an unfilled
# freeze placeholder, or malformed grammar means the execution domain is not
# attested; none is learned from the login being tested. The `:?` checks are
# fail-closed backstops after the reasoned rc-3 pre-checks.
[ -n "${P0_ATTESTED_USER_NS:-}" ] \
    || p0_stop "execution_domain_unattested field=user_namespace detail=preregistered_value_missing"
[ -n "${P0_ATTESTED_MNT_NS:-}" ] \
    || p0_stop "execution_domain_unattested field=mount_namespace detail=preregistered_value_missing"
[ -n "${P0_ATTESTED_PID_NS:-}" ] \
    || p0_stop "execution_domain_unattested field=pid_namespace detail=preregistered_value_missing"
[ -n "${P0_ATTESTED_NET_NS:-}" ] \
    || p0_stop "execution_domain_unattested field=network_namespace detail=preregistered_value_missing"
[ -n "${P0_ATTESTED_ROOT_MOUNT_ID:-}" ] \
    || p0_stop "execution_domain_unattested field=root_mount_identity detail=preregistered_value_missing"
: "${P0_ATTESTED_USER_NS:?deploy-attested user namespace identity is required}"
: "${P0_ATTESTED_MNT_NS:?deploy-attested mount namespace identity is required}"
: "${P0_ATTESTED_PID_NS:?deploy-attested PID namespace identity is required}"
: "${P0_ATTESTED_NET_NS:?deploy-attested network namespace identity is required}"
: "${P0_ATTESTED_ROOT_MOUNT_ID:?deploy-attested canonical root-mount identity is required}"

p0_validate_attested_ns_input() {
    local field="$1" label="$2" value="$3" inner
    [ "$value" != '<PIN-AT-FREEZE>' ] \
        || p0_stop "execution_domain_unattested field=$field detail=freeze_pin_unfilled"
    case "$value" in
        "$label":'['*']') inner="${value#*:\[}"; inner="${inner%\]}" ;;
        *) p0_stop "execution_domain_unattested field=$field detail=namespace_identity_grammar" ;;
    esac
    case "$inner" in
        ''|*[!0-9]*) p0_stop "execution_domain_unattested field=$field detail=namespace_identity_grammar" ;;
    esac
}

p0_validate_attested_ns_input user_namespace user "$P0_ATTESTED_USER_NS"
p0_validate_attested_ns_input mount_namespace mnt "$P0_ATTESTED_MNT_NS"
p0_validate_attested_ns_input pid_namespace pid "$P0_ATTESTED_PID_NS"
p0_validate_attested_ns_input network_namespace net "$P0_ATTESTED_NET_NS"
[ "$P0_ATTESTED_ROOT_MOUNT_ID" != '<PIN-AT-FREEZE>' ] \
    || p0_stop "execution_domain_unattested field=root_mount_identity detail=freeze_pin_unfilled"
case "$P0_ATTESTED_ROOT_MOUNT_ID" in
    *[!0-9:]*|*:*:*|:*|*:|'')
        p0_stop "execution_domain_unattested field=root_mount_identity detail=dev_inode_grammar" ;;
    *:*) : ;;
    *) p0_stop "execution_domain_unattested field=root_mount_identity detail=dev_inode_grammar" ;;
esac

[ "$P0_FIXED_ATTESTED_USER_NS" != '<PIN-AT-FREEZE>' ] \
    || p0_stop "execution_domain_unattested field=user_namespace detail=freeze_pin_unfilled"
[ "$P0_FIXED_ATTESTED_MNT_NS" != '<PIN-AT-FREEZE>' ] \
    || p0_stop "execution_domain_unattested field=mount_namespace detail=freeze_pin_unfilled"
[ "$P0_FIXED_ATTESTED_PID_NS" != '<PIN-AT-FREEZE>' ] \
    || p0_stop "execution_domain_unattested field=pid_namespace detail=freeze_pin_unfilled"
[ "$P0_FIXED_ATTESTED_NET_NS" != '<PIN-AT-FREEZE>' ] \
    || p0_stop "execution_domain_unattested field=network_namespace detail=freeze_pin_unfilled"
[ "$P0_FIXED_ATTESTED_ROOT_MOUNT_ID" != '<PIN-AT-FREEZE>' ] \
    || p0_stop "execution_domain_unattested field=root_mount_identity detail=freeze_pin_unfilled"
[ "$P0_ATTESTED_USER_NS" = "$P0_FIXED_ATTESTED_USER_NS" ] \
    || p0_stop "execution_domain_unattested field=user_namespace detail=prelude_value_differs_from_frozen_pin"
[ "$P0_ATTESTED_MNT_NS" = "$P0_FIXED_ATTESTED_MNT_NS" ] \
    || p0_stop "execution_domain_unattested field=mount_namespace detail=prelude_value_differs_from_frozen_pin"
[ "$P0_ATTESTED_PID_NS" = "$P0_FIXED_ATTESTED_PID_NS" ] \
    || p0_stop "execution_domain_unattested field=pid_namespace detail=prelude_value_differs_from_frozen_pin"
[ "$P0_ATTESTED_NET_NS" = "$P0_FIXED_ATTESTED_NET_NS" ] \
    || p0_stop "execution_domain_unattested field=network_namespace detail=prelude_value_differs_from_frozen_pin"
[ "$P0_ATTESTED_ROOT_MOUNT_ID" = "$P0_FIXED_ATTESTED_ROOT_MOUNT_ID" ] \
    || p0_stop "execution_domain_unattested field=root_mount_identity detail=prelude_value_differs_from_frozen_pin"

# This derives the literal leaf name only. P0 has no preregistered value for a
# resolved `bin` component or interpreter-symlink target chain, so it cannot
# truthfully bind either one here; that residual is disclosed in the terminal
# `does_not_establish` claim instead of learning and accepting a target at run
# time contrary to prereg row 18.
P0_PY="$P0_VENV_ROOT/bin/python"

printf 'P0_SECTION preregistered_inputs\n'
printf 'P0_input name=P0_EXPECT_UID value=%s\n' "$P0_EXPECT_UID"
printf 'P0_input name=P0_STATE_UID value=%s\n' "$P0_STATE_UID"
printf 'P0_input name=P0_STATE_GID value=%s\n' "$P0_STATE_GID"
printf 'P0_input name=P0_FORBIDDEN_GIDS value=[%s] count=%s\n' \
    "$P0_FORBIDDEN_GIDS" "$P0_FORBIDDEN_GID_COUNT"
printf 'P0_input name=P0_VENV_ROOT value=%s\n' "$P0_VENV_ROOT"
printf 'P0_input name=P0_TOOL_PINS value=[%s] count=%s\n' "$P0_TOOL_PINS" "$P0_PIN_COUNT"
printf 'P0_input name=P0_MANAGER_QUERY_BOUND budget_s=%s kill_after_s=%s source=frozen_block_literal\n' \
    "$P0_MANAGER_QUERY_BUDGET_S" "$P0_MANAGER_QUERY_KILL_AFTER_S"
printf 'P0_input name=P0_EXECUTION_DOMAIN_ATTESTATION fields=user_namespace,mount_namespace,pid_namespace,network_namespace,root_mount_identity source=deploy_channel_frozen_literals\n'
printf 'P0_input name=P0_INTERPRETER value=%s derived_from=P0_VENV_ROOT\n' "$P0_PY"

# ---------------------------------------------------------------------------
# SECTION: tool inventory
# ---------------------------------------------------------------------------
# Resolution and executability are decided by shell builtins only - `command -v`
# and the access(2) predicate `[ -x ]` - so no external tool has to be trusted
# before the inventory that establishes it. `stat` is used afterwards, for the
# RECORD only; a failure there is could-not-evaluate, never a silent skip.
# What this section establishes: every preregistered tool resolves to its FROZEN
# deploy-channel pin (correction 7), this login may execute it, and that path's
# kind, mode and numeric owner are recorded. What it does NOT establish: that the
# resolved object is the distribution's tool. P0 has no attestation channel and
# does not pretend to one; the pin is the object the deploy channel froze for
# this tool, and a PATH resolution that disagrees with it STOPs.
p0_resolve_tool() {
    local t="$1" resolved rc=0 pin canon crc=0 rl
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
        if [ "$resolved" = "$pin" ]; then
            P0_RESOLUTION="pinned_absolute"
        elif [ "$t" = python3 ]; then
            # The ONE preregistered divergence between a pin and its PATH
            # spelling, and not a relaxation for anything else. `/usr/bin/python3`
            # is a symlink on the target family and the RO stage may bind only a
            # non-symlink object, so its pin is the RESOLVED leaf while PATH still
            # spells the link. The pin is admitted only if the object this login's
            # PATH really reaches canonicalises to EXACTLY the frozen pin, so a
            # shadowing `python3` earlier in PATH - which canonicalises somewhere
            # else - still STOPs. `readlink` precedes `python3` in the inventory
            # order, and its absence from the resolved map is a STOP rather than
            # an assumption.
            p0_lookup "$P0_TOOLS_RESOLVED" readlink \
                || p0_stop "tool_pin_uncanonicalizable tool=$t pinned=$pin resolved=$resolved detail=readlink_not_resolved_before_python3"
            rl="$P0_LOOKUP"
            canon="$(LC_ALL=C "$rl" -v -f -- "$resolved" 2>&1)" || crc=$?
            if [ "$crc" -ne 0 ]; then
                p0_sanitize "$canon"
                [ -n "$P0_SAFE" ] || P0_SAFE="readlink_diagnostic_absent"
                p0_stop "tool_pin_uncanonicalizable tool=$t pinned=$pin resolved=$resolved rc=$crc detail=[$P0_SAFE]"
            fi
            if [ "$canon" != "$pin" ]; then
                p0_sanitize "$canon"
                p0_stop "tool_pin_mismatch tool=$t pinned=$pin resolved=$resolved canonical=[$P0_SAFE]"
            fi
            # The object the RO stage will invoke is the pin, so the pin - not the
            # link spelling - is what gets recorded, metadata-probed and access(2)
            # tested below. The link spelling stays on the resolution token.
            resolved="$pin"
            P0_RESOLUTION="pinned_absolute_via_canonicalized_path_symlink"
        else
            p0_stop "tool_pin_mismatch tool=$t pinned=$pin resolved=$resolved"
        fi
    else
        # Correction 7: the unpinned `path_resolved_absolute` fallback is DELETED.
        # Every tool is pinned (the pin loop rejects omissions), so an unpinned
        # tool is a STOP and the reachable executable set is the frozen pin set.
        p0_stop "tool_pin_unpinned tool=$t detail=every_tool_requires_a_frozen_pin"
    fi
    # `rc=na` is deliberate and is the reason prereg 8.1 row 1 carries `rc=<n|na>`:
    # nothing was invoked. The access(2) predicate refused, so there IS no
    # invocation status, and printing the conventional 126 would put a status no
    # probe produced into the evidence leaf (pattern 9). The resolved path stays
    # on the line because the `P0_tool name=... path=...` inventory lines are
    # printed by a later loop that this STOP never reaches, so this is the only
    # place the rejected object can be named.
    [ -x "$resolved" ] \
        || p0_stop "tool_not_evaluable tool=$t path=$resolved rc=na detail=access_builtin_x_denied mechanism=access_builtin_x"
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
p0_lookup "$P0_TOOLS_RESOLVED" timeout   || p0_stop "missing_tool tool=timeout detail=absent_from_resolved_map"
P0_TIMEOUT="$P0_LOOKUP"
p0_lookup "$P0_TOOLS_RESOLVED" getent    || p0_stop "missing_tool tool=getent detail=absent_from_resolved_map"
P0_GETENT="$P0_LOOKUP"

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
printf 'P0_tool_inventory count=%s pinned=%s ro_half=[%s] p0_only_half=[%s] ro_basis=RP7-WPI-RO.sh@d6a976aa:23e55667:70941 trusted_python_pin=%s provenance=not_established\n' \
    "$P0_TOOL_COUNT" "$P0_PIN_COUNT" "$P0_RP7_RO_TOOLS" "$P0_P0_ONLY_TOOLS" \
    "$P0_TRUSTED_PYTHON_BOUND"

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
    rawpath="$(LC_ALL=C "$P0_READLINK" -v -- "$P0_FD_SELF" 2>&1)" || rc=$?
    if [ "$rc" -ne 0 ]; then
        p0_prepare_readlink_detail "$rawpath"
        exec 8>&-
        p0_stop "evidence_binding_unprobeable path=$P0_FD_SELF rc=$rc detail=[$P0_SAFE] diagnostic_shape=$P0_RESOLUTION"
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
        [ -n "$P0_SAFE" ] || P0_SAFE="producer_diagnostic_absent"
        if [ "$label" = gids ]; then
            p0_stop "group_query_not_evaluable rc=$rc detail=[$P0_SAFE]"
        fi
        p0_stop "identity_probe_failed field=$label flag=$flag rc=$rc detail=[$P0_SAFE]"
    fi
    case "$raw" in
        *$'\r'*|*$'\n'*)
            p0_sanitize "$raw"
            if [ "$label" = gids ]; then
                p0_stop "group_query_not_evaluable rc=0 detail=[response_multiline:$P0_SAFE]"
            fi
            p0_stop "identity_probe_multiline field=$label flag=$flag detail=[$P0_SAFE]" ;;
    esac
    if [ -z "$raw" ]; then
        if [ "$label" = gids ]; then
            p0_stop "group_query_not_evaluable rc=0 detail=[response_empty]"
        fi
        p0_stop "identity_probe_empty field=$label flag=$flag"
    fi
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
    # F2 (Claude round-6 re-audit): the same defect class the round-5 F3 repair
    # closed for `P0_FORBIDDEN_GIDS` - validation applied to the items an UNQUOTED
    # `for g in $gids` produced, instead of to the raw `id -G` value, so pathname
    # expansion ran first. With gids='*' (or '0*', '?') and a cwd holding a
    # numeric-named entry, the wildcard expanded to that name, the per-item check
    # passed, and a malformed response was laundered into `form=numeric_only`; in
    # an empty cwd the same response STOPped, so the verdict depended on cwd. The
    # downstream whole-word intersection then matched the RAW `" $gids "` string,
    # so `" 0* "` never contained `" 0 "` and `capability_wider_than_ledger` did
    # not fire for a response that literally began with the forbidden gid. Same
    # two defenses as the F3 input gate: (1) grammar-check the COMPLETE raw
    # capture against digits-plus-separators BEFORE any expansion, so a wildcard
    # or any non-digit/non-space byte is a STOP regardless of cwd; (2) split with
    # pathname expansion disabled (`set -f`) so no surviving metacharacter reaches
    # the per-item check. The per-item check is retained as the second layer.
    case "$gids" in
        *[!0-9[:space:]]*)
            p0_stop "group_query_not_evaluable rc=0 detail=[response_not_decimal_gid_list]" ;;
    esac
    set -f
    for g in $gids; do
        case "$g" in
            *[!0-9]*) p0_stop "group_query_not_evaluable rc=0 detail=[response_not_decimal_gid_list]" ;;
        esac
        count=$(( count + 1 ))
    done
    set +f
    [ "$count" -ge 1 ] || p0_stop "group_query_not_evaluable rc=0 detail=[response_empty]"
    printf 'P0_identity uid=%s gid=%s gids=[%s] gid_count=%s form=numeric_only\n' \
        "$uid" "$gid" "$gids" "$count"
    # The preregistered login comparison is made after the unique `gatea`
    # record is available, so every `identity_unexpected` line has one grammar.
    # Whole-word match on the space-padded list, so gid 0 does not match gid 10.
    # F3 (Codex final-audit round-5): P0_FORBIDDEN_GIDS is already grammar-bound
    # to digits-plus-separators at the input gate above, so a wildcard cannot
    # reach here. Pathname expansion is additionally disabled (`set -f`) as
    # defense in depth so this intersection loop is non-globbing by construction
    # regardless of cwd; the whole-word `case` match is unaffected by glob mode.
    set -f
    for f in $P0_FORBIDDEN_GIDS; do
        case " $gids " in
            *" $f "*) p0_stop "capability_wider_than_ledger gid=$f caller_gids=[$gids]" ;;
        esac
    done
    set +f
    printf 'P0_identity_admitted uid=%s forbidden_gids=[%s] intersection=empty\n' \
        "$uid" "$P0_FORBIDDEN_GIDS"
}

printf 'P0_SECTION identity\n'
p0_record_identity

# ---------------------------------------------------------------------------
# SECTION: account resolution (prereg 8.1 rows 1-3, repair C13)
# ---------------------------------------------------------------------------
# The identity section above proved WHO this process is numerically and that
# the live numerics agree with P0_EXPECT_UID and the forbidden-gid ledger. It
# did NOT confirm that the NAMES `gatea` (the route login) and `mtc-bridge`
# (the dynamically allocated service account) resolve to those numerics. C13
# closed that gap: the names are the resolver contract, but the ADMISSION is
# numeric only (Pattern 8 - the name is not the identity).
#
# This arm resolves `getent passwd gatea` and `getent passwd mtc-bridge` with
# the PINNED absolute getent from the inventory (row 1), parses each record
# whole under the passwd grammar (Pattern 5 - full-record parse; duplicate,
# multiline or structurally malformed records are ambiguous and STOP; a valid
# no-match is a distinct outcome from a lookup error), and adjudicates the
# numerics:
#   gatea      - uid must equal the live `id -u` AND P0_EXPECT_UID; primary gid
#                must equal the live `id -g`. A mismatch is identity_unexpected
#                rc 3 (the F2 polarity ruling: an identity wider/different than
#                preregistered is re-adjudication, never a silent run).
#   mtc-bridge - uid:gid must equal the preregistered P0_STATE_UID:P0_STATE_GID
#                (999:988). A numeric mismatch on a complete record is
#                identity_unexpected (the one grammar both accounts share). A
#                VALID NO-MATCH - getent rc 2 AND a completely empty merged
#                capture, so positive absence really was established - is the
#                distinct outcome state_account_resolution_unexpected: the
#                dynamically allocated account is absent, which is a host
#                observation about the allocation and not an inability to
#                evaluate. Both exit 3 (audit-3 F4: that token is now
#                preregistered verbatim in row 3 rather than left unregistered).
# A getent that is missing/unpinnable, or a lookup error, or an rc 2 that
# carries ANY byte - a diagnostic, a partial record, or a bare newline -
# (positive absence not established), or
# an unparsable or duplicate record, is an inability to evaluate:
# identity_unresolvable, exit 3, carrying the resolver's OWN recorded status in
# `rc=` (audit-3 F4). The status is exported by the parser rather than kept
# local, and `rc=na` appears only on the two capture shapes that fail before any
# status can be read - never as a stand-in for a status that was available.
# Names, gecos, home and shell are captured as DIAGNOSTIC fields only; no name
# is ever asserted or compared.
#
# The live id -u/-g are recaptured here via the same adjudicated
# p0_capture_numeric path the identity section uses, so this arm is
# self-contained and the existing identity section stays byte-for-byte
# untouched. getent runs with the caller environment inherited and LC_ALL
# forced to C, exactly like the `id` probe it mirrors; it is NOT a cleared-env
# launch (those are reserved for the manager query and the interpreter
# execution). The row-3 group half - numeric `id -G` excluding gids 0 and 988
# - remains the identity section's P0_FORBIDDEN_GIDS responsibility and is not
# re-asserted here.

# Parse one `getent passwd <name>` record into globals, without ever asserting
# a name. Sets P0_PW_OUTCOME to one of: found | nomatch | error, and ALWAYS sets
# P0_PW_RC to the resolver's own exit status, or to the literal `na` on the two
# shapes that fail before any status can be read. On `found` it also sets
# P0_PW_NAME, P0_PW_UID, P0_PW_GID (numerics, validated) and P0_PW_DIAG
# (sanitized remaining fields). On `nomatch`/`error` it sets P0_PW_RC and
# P0_PW_DIAG. No branch here decides an admission - the caller adjudicates the
# outcome. getent rc convention (Linux getent(1)): 0 = found, 2 = key absent,
# anything else = lookup/service error. rc 2 is treated as a VALID NO-MATCH only
# when the complete merged capture is empty, which is this interface's exact
# no-match shape (C13 audit F1). rc 2 carrying any byte - a diagnostic on
# stderr, a partial record, a warning from an NSS module - means the tool both
# failed to answer and said something about it, so positive absence was NOT
# established and the only truthful outcome is `error` (Pattern 1: an inability
# to evaluate is not a result). The merged capture makes this decidable with no
# temp file: stderr text destroys the empty shape (Pattern 6).
# ANY byte includes a bare newline or NUL. Bash variables cannot contain NUL,
# so an ordinary command substitution cannot distinguish NUL-only output from
# an empty stream. The capture below uses NUL as an out-of-band record delimiter:
# the producer appends a textual rc record after its stream, and `mapfile -d ''`
# must receive exactly two fields. Any NUL produced by getent creates an extra
# field and is therefore an error before positive absence can be asserted.
p0_resolve_passwd() {
    local acct="$1" raw rc=0 had_bytes=no n_colon rest f1 f2 f3 f4 f5 f6 f7 rc_record
    local -a p0_pw_parts=()
    P0_PW_OUTCOME="error"
    P0_PW_NAME=""; P0_PW_UID=""; P0_PW_GID=""; P0_PW_DIAG=""
    # The resolver status is EXPORTED, not kept local (audit-3 F4). Rows 2 and 3
    # make `rc=<n>` mandatory on every `identity_unresolvable` divergence, and a
    # status the caller cannot see is a status the evidence leaf never records.
    # `na` is the honest value for the two shapes that fail BEFORE a status can
    # be read, and only for those; it is never a stand-in for a status that was
    # available.
    P0_PW_RC="na"
    mapfile -d '' -t p0_pw_parts < <(
        getent_rc=0
        LC_ALL=C "$P0_GETENT" passwd "$acct" 2>&1 || getent_rc=$?
        printf '\0P0_GETENT_RC=%s\0' "$getent_rc"
    )
    # The status sentinel is the LAST field the producer wrote, so it survives a
    # NUL emitted by getent itself: that NUL adds fields at the FRONT. Reading it
    # even in the malformed-capture arm is what lets an ambiguous capture still
    # carry the tool's real status instead of `na`.
    if [ "${#p0_pw_parts[@]}" -ge 1 ]; then
        rc_record="${p0_pw_parts[$(( ${#p0_pw_parts[@]} - 1 ))]}"
        case "$rc_record" in
            P0_GETENT_RC=*)
                rc="${rc_record#P0_GETENT_RC=}"
                case "$rc" in
                    ''|*[!0-9]*) : ;;
                    *) P0_PW_RC="$rc" ;;
                esac ;;
        esac
    fi
    if [ "${#p0_pw_parts[@]}" -ne 2 ]; then
        P0_PW_DIAG="nul_byte_in_merged_capture"
        P0_PW_OUTCOME="error"
        return 0
    fi
    raw="${p0_pw_parts[0]}"
    rc_record="${p0_pw_parts[1]}"
    case "$rc_record" in
        P0_GETENT_RC=*) rc="${rc_record#P0_GETENT_RC=}" ;;
        *) P0_PW_DIAG="capture_sentinel_lost"; P0_PW_OUTCOME="error"; return 0 ;;
    esac
    case "$rc" in
        ''|*[!0-9]*) P0_PW_DIAG="capture_status_unparseable"; P0_PW_OUTCOME="error"; return 0 ;;
    esac
    P0_PW_RC="$rc"
    # Decided on the PRESERVED capture, before any normalization: did the tool
    # emit a single byte of anything at all?
    [ -z "$raw" ] || had_bytes=yes
    # Normalize back to the shape plain command substitution used to produce, so
    # every downstream branch - the rc-0 full-record parse and the diagnostics
    # alike - sees exactly the audited value and no other behaviour changes.
    while [ "${raw%$'\n'}" != "$raw" ]; do raw="${raw%$'\n'}"; done
    case "$rc" in
        0) : ;;
        2)
            if [ "$had_bytes" = yes ]; then
                if [ -n "$raw" ]; then
                    p0_sanitize "$raw"; P0_PW_DIAG="$P0_SAFE"
                else
                    P0_PW_DIAG="newline_only_capture_at_rc2"
                fi
                P0_PW_OUTCOME="error"; return 0
            fi
            P0_PW_OUTCOME="nomatch"; P0_PW_DIAG="empty_capture_at_rc2"; return 0 ;;
        *) p0_sanitize "$raw"; P0_PW_DIAG="$P0_SAFE"; P0_PW_OUTCOME="error"; return 0 ;;
    esac
    # rc 0: status adjudicated before any byte is interpreted (Pattern 6).
    case "$raw" in
        *$'\r'*|*$'\n'*)
            p0_sanitize "$raw"; P0_PW_DIAG="$P0_SAFE"
            P0_PW_OUTCOME="error"; return 0 ;;
    esac
    [ -n "$raw" ] || { P0_PW_OUTCOME="error"; P0_PW_DIAG="empty_record_at_rc0"; return 0; }
    # Exactly seven colon-separated fields (Pattern 5 full-record parse). gecos,
    # home and shell contain no colon in a valid passwd record, so a colon count
    # other than six is structural ambiguity, never a record.
    p0_count_substr "$raw" ":"; n_colon="$P0_COUNT"
    if [ "$n_colon" -ne 6 ]; then
        p0_sanitize "$raw"; P0_PW_DIAG="$P0_SAFE"
        P0_PW_OUTCOME="error"; return 0
    fi
    f1="${raw%%:*}"; rest="${raw#*:}"    # name
    f2="${rest%%:*}"; rest="${rest#*:}"  # passwd placeholder
    f3="${rest%%:*}"; rest="${rest#*:}"  # uid
    f4="${rest%%:*}"; rest="${rest#*:}"  # gid
    f5="${rest%%:*}"; rest="${rest#*:}"  # gecos
    f6="${rest%%:*}"; rest="${rest#*:}"  # home
    f7="$rest"                           # shell
    case "$f3" in ''|*[!0-9]*)
        p0_sanitize "$raw"; P0_PW_DIAG="$P0_SAFE"; P0_PW_OUTCOME="error"; return 0 ;; esac
    case "$f4" in ''|*[!0-9]*)
        p0_sanitize "$raw"; P0_PW_DIAG="$P0_SAFE"; P0_PW_OUTCOME="error"; return 0 ;; esac
    P0_PW_NAME="$f1"; P0_PW_UID="$f3"; P0_PW_GID="$f4"
    p0_sanitize "$f2:$f5:$f6:$f7"; P0_PW_DIAG="$P0_SAFE"
    P0_PW_OUTCOME="found"; return 0
}

p0_resolve_accounts() {
    local live_uid live_gid
    p0_capture_numeric uid -u; live_uid="$P0_CAPTURE"
    p0_capture_numeric gid -g; live_gid="$P0_CAPTURE"

    # gatea: the named route login. A complete unique record must map the name
    # to numerics equal to BOTH the live id -u/-g and the preregistered uid.
    p0_resolve_passwd gatea
    case "$P0_PW_OUTCOME" in
        found)
            printf 'P0_account account=gatea outcome=resolved uid=%s gid=%s name_diag=[%s] via=pinned_getent_passwd\n' \
                "$P0_PW_UID" "$P0_PW_GID" "$P0_PW_NAME"
            if [ "$live_uid" != "$P0_PW_UID" ] || [ "$live_gid" != "$P0_PW_GID" ]; then
                p0_stop "identity_unexpected observed_numeric=$live_uid:$live_gid expected_numeric=$P0_PW_UID:$P0_PW_GID account=gatea"
            fi
            if [ "$P0_PW_UID" != "$P0_EXPECT_UID" ]; then
                p0_stop "identity_unexpected observed_numeric=$P0_PW_UID:$P0_PW_GID expected_numeric=$P0_EXPECT_UID:$P0_PW_GID account=gatea"
            fi
            printf 'P0_account_admitted account=gatea numeric=%s:%s matches=live_id_and_prereg_uid name=diagnostic_only\n' \
                "$P0_PW_UID" "$P0_PW_GID"
            ;;
        nomatch)
            p0_stop "identity_unresolvable account=gatea rc=$P0_PW_RC detail=getent_valid_no_match_for_route_login"
            ;;
        error)
            p0_stop "identity_unresolvable account=gatea rc=$P0_PW_RC detail=[$P0_PW_DIAG]"
            ;;
    esac

    # mtc-bridge: the dynamically allocated service account. A complete unique
    # record must map the name to the preregistered P0_STATE_UID:P0_STATE_GID.
    p0_resolve_passwd mtc-bridge
    case "$P0_PW_OUTCOME" in
        found)
            printf 'P0_account account=mtc-bridge outcome=resolved uid=%s gid=%s name_diag=[%s] via=pinned_getent_passwd\n' \
                "$P0_PW_UID" "$P0_PW_GID" "$P0_PW_NAME"
            if [ "$P0_PW_UID" != "$P0_STATE_UID" ] || [ "$P0_PW_GID" != "$P0_STATE_GID" ]; then
                p0_stop "identity_unexpected observed_numeric=$P0_PW_UID:$P0_PW_GID expected_numeric=$P0_STATE_UID:$P0_STATE_GID account=mtc-bridge"
            fi
            printf 'P0_account_admitted account=mtc-bridge numeric=%s:%s matches=prereg_state_uid_gid name=diagnostic_only\n' \
                "$P0_PW_UID" "$P0_PW_GID"
            ;;
        nomatch)
            p0_stop "state_account_resolution_unexpected account=mtc-bridge observed_numeric=absent expected_numeric=$P0_STATE_UID:$P0_STATE_GID detail=getent_valid_no_match"
            ;;
        error)
            p0_stop "identity_unresolvable account=mtc-bridge rc=$P0_PW_RC detail=[$P0_PW_DIAG]"
            ;;
    esac
}

printf 'P0_SECTION accounts\n'
p0_resolve_accounts

# ---------------------------------------------------------------------------
# SECTION: execution-domain binding (prereg 8.1 row 8; WP-I audit F2)
# ---------------------------------------------------------------------------
# Every identity is compared with a value supplied by the deploy channel and
# frozen into this block. Visible PID 1 is never consulted. Namespace equality
# plus the root dev:inode binds the login's kernel domain and chroot-visible root;
# the successor's mount projection separately binds the preregistered path set.
# Nothing in the comparisons alone establishes that `/proc` is a procfs mount, so
# the crafted-link case this row exists to refuse is discriminated separately
# below by object device, and the residual is disclosed rather than implied
# (audit-2 R2 finding 3).
p0_read_domain_ns() {
    local field="$1" label="$2" path="$3" attested="$4" raw rc=0 inner
    raw="$(LC_ALL=C "$P0_READLINK" -v -- "$path" 2>&1)" || rc=$?
    if [ "$rc" -ne 0 ]; then
        p0_prepare_readlink_detail "$raw"
        p0_stop "execution_domain_unattested field=$field rc=$rc detail=[$P0_SAFE] diagnostic_shape=$P0_RESOLUTION"
    fi
    [ -n "$raw" ] || p0_stop "execution_domain_unattested field=$field detail=namespace_identity_empty"
    case "$raw" in
        *[![:print:]]*|*[[:space:]]*)
            p0_stop "execution_domain_unattested field=$field detail=namespace_identity_unprintable" ;;
    esac
    case "$raw" in
        "$label":'['*']') inner="${raw#*:\[}"; inner="${inner%\]}" ;;
        *) p0_stop "execution_domain_unattested field=$field detail=namespace_identity_grammar" ;;
    esac
    case "$inner" in
        ''|*[!0-9]*) p0_stop "execution_domain_unattested field=$field detail=namespace_identity_grammar" ;;
    esac
    [ "$raw" = "$attested" ] \
        || p0_stop "execution_domain_mismatch field=$field observed=$raw attested=$attested"
    P0_NS_VALUE="$raw"
}

# Device of the object a path resolves to, `-L` so a namespace link is followed
# to the namespace inode itself rather than described as a link. Adjudicated like
# every other capture: status first, then grammar, then value.
p0_read_object_device() {
    local field="$1" path="$2" raw rc=0
    P0_DEVICE=""
    raw="$(LC_ALL=C "$P0_STAT" -L -c '%d' -- "$path" 2>&1)" || rc=$?
    if [ "$rc" -ne 0 ]; then
        p0_sanitize "$raw"; [ -n "$P0_SAFE" ] || P0_SAFE="stat_diagnostic_absent"
        p0_stop "execution_domain_unattested field=$field subject=namespace_link_device rc=$rc detail=[$P0_SAFE]"
    fi
    case "$raw" in
        ''|*[!0-9]*)
            p0_stop "execution_domain_unattested field=$field subject=namespace_link_device detail=device_grammar" ;;
    esac
    P0_DEVICE="$raw"
}

# Procfs discrimination for one namespace link. A kernel namespace inode does not
# live on the root filesystem: it lives on the anonymous `nsfs` superblock, which
# always carries a different st_dev from the root object. A fabricated link - or
# the ordinary file a fabricated link resolves to - allocated on the root
# filesystem therefore fails this comparison even though its readlink text and
# grammar are perfect. This is the case prereg row 8 exists to refuse and the one
# the equality comparisons alone cannot see.
p0_assert_ns_link_off_root() {
    local field="$1" path="$2" root_dev="$3"
    p0_read_object_device "$field" "$path"
    [ "$P0_DEVICE" != "$root_dev" ] \
        || p0_stop "execution_domain_unattested field=$field detail=namespace_link_on_root_filesystem device=$P0_DEVICE root_device=$root_dev"
}

p0_assert_execution_domain() {
    local user mnt pid net root_canon root_id rc=0
    # Initialised so that the D026 mutation which deletes the four
    # `p0_assert_ns_link_off_root` calls reaches the evidence line and visibly
    # ADMITS a crafted-procfs fixture, instead of dying on `set -u` for an
    # unrelated reason. On every production path each one is assigned by a call
    # that otherwise STOPs, so an empty value can never be printed.
    local root_dev="" dev_user="" dev_mnt="" dev_pid="" dev_net=""
    p0_read_domain_ns user_namespace user "$P0_NS_USER_PATH" "$P0_ATTESTED_USER_NS"; user="$P0_NS_VALUE"
    p0_read_domain_ns mount_namespace mnt "$P0_NS_MNT_PATH" "$P0_ATTESTED_MNT_NS"; mnt="$P0_NS_VALUE"
    p0_read_domain_ns pid_namespace pid "$P0_NS_PID_PATH" "$P0_ATTESTED_PID_NS"; pid="$P0_NS_VALUE"
    p0_read_domain_ns network_namespace net "$P0_NS_NET_PATH" "$P0_ATTESTED_NET_NS"; net="$P0_NS_VALUE"
    root_canon="$(LC_ALL=C "$P0_READLINK" -v -f -- / 2>&1)" || rc=$?
    if [ "$rc" -ne 0 ]; then
        p0_prepare_readlink_detail "$root_canon"
        p0_stop "execution_domain_unattested field=root_mount_identity rc=$rc detail=[$P0_SAFE] diagnostic_shape=$P0_RESOLUTION"
    fi
    [ "$root_canon" = / ] \
        || p0_stop "execution_domain_unattested field=root_mount_identity detail=root_not_literal_canonical"
    rc=0
    root_id="$(LC_ALL=C "$P0_STAT" -L -c '%d:%i' -- / 2>&1)" || rc=$?
    if [ "$rc" -ne 0 ]; then
        p0_sanitize "$root_id"; [ -n "$P0_SAFE" ] || P0_SAFE="stat_diagnostic_absent"
        p0_stop "execution_domain_unattested field=root_mount_identity rc=$rc detail=[$P0_SAFE]"
    fi
    case "$root_id" in
        *[!0-9:]*|*:*:*|:*|*:|'')
            p0_stop "execution_domain_unattested field=root_mount_identity detail=dev_inode_grammar" ;;
        *:*) : ;;
        *) p0_stop "execution_domain_unattested field=root_mount_identity detail=dev_inode_grammar" ;;
    esac
    [ "$root_id" = "$P0_ATTESTED_ROOT_MOUNT_ID" ] \
        || p0_stop "execution_domain_mismatch field=root_mount_identity observed=$root_id attested=$P0_ATTESTED_ROOT_MOUNT_ID"
    # The root object's device is the left field of the identity already read, so
    # the discrimination below costs one `stat` per namespace link and no new
    # tool. It runs after the equality comparisons so that a genuine divergence
    # still reports as `execution_domain_mismatch`, and before the evidence line
    # and the row-9 manager query, which both remain unreachable until it holds.
    root_dev="${root_id%%:*}"
    p0_assert_ns_link_off_root user_namespace    "$P0_NS_USER_PATH" "$root_dev"; dev_user="$P0_DEVICE"
    p0_assert_ns_link_off_root mount_namespace   "$P0_NS_MNT_PATH"  "$root_dev"; dev_mnt="$P0_DEVICE"
    p0_assert_ns_link_off_root pid_namespace     "$P0_NS_PID_PATH"  "$root_dev"; dev_pid="$P0_DEVICE"
    p0_assert_ns_link_off_root network_namespace "$P0_NS_NET_PATH"  "$root_dev"; dev_net="$P0_DEVICE"
    # `procfs_identity=not_established` is stated, not implied. The device
    # comparison refuses a fabrication allocated on the ROOT filesystem; it does
    # not establish that these objects are procfs/nsfs, because a fabrication
    # placed on any other filesystem would carry a different device too. The same
    # residual is carried in the terminal `does_not_establish` claim.
    printf 'P0_execution_domain user_ns=%s mnt_ns=%s pid_ns=%s net_ns=%s root_mount_id=%s binding=deploy_attested_exact visible_pid1_comparison=not_used procfs_identity=not_established ns_link_devices=%s,%s,%s,%s root_device=%s ns_link_devices_distinct_from_root=yes\n' \
        "$user" "$mnt" "$pid" "$net" "$root_id" \
        "$dev_user" "$dev_mnt" "$dev_pid" "$dev_net" "$root_dev"
}

printf 'P0_SECTION execution_domain\n'
p0_assert_execution_domain

# ---------------------------------------------------------------------------
# SECTION: system-manager readiness (prereg 8.1 row 7)
# ---------------------------------------------------------------------------
# This row is unreachable until the execution-domain gate above has passed.
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
# THE QUERY IS BOUNDED (audit-3 F2). Row 9 explicitly assigns `timeout` to
# `system_manager_unreachable`, and an unbounded query cannot honour that: a
# stalled D-Bus or system-manager response never reaches the rc/diagnostic
# adjudicator at all, so the block emits no reason line, no rc and no verdict -
# it simply never returns, and whatever eventually kills it is an external
# actor's status, not this block's ruling (pattern 1: a STOP that is never
# reached is not a STOP). The bound is the pinned `timeout`, placed INSIDE the
# cleared environment as the round-1.4 probe-execution-environment rule requires:
# `env -i` execs first and `timeout` is its argument, so the process that decides
# whether the query was bounded runs under the same cleared environment as the
# query it bounds - not under an operator-controlled one that could redirect or
# neuter it. `--kill-after` escalates if the manager ignores SIGTERM, so the
# deadline holds even against a child that traps it.
# Elapsed seconds are recorded from the `SECONDS` shell builtin: no clock tool is
# invoked, so there is no additional status to adjudicate. It is DIAGNOSTIC only
# - whole-second resolution and subject to wall-clock adjustment - and no branch
# below reads it. `timeout`'s own exit status, not the elapsed value, decides.
p0_assert_system_manager_ready() {
    local raw rc=0 value detail started elapsed
    started="$SECONDS"
    raw="$(LC_ALL=C "$P0_ENV" -i LC_ALL=C "$P0_TIMEOUT" \
        --signal=TERM --kill-after="${P0_MANAGER_QUERY_KILL_AFTER_S}s" \
        "${P0_MANAGER_QUERY_BUDGET_S}s" \
        "$P0_SYSTEMCTL" --system --no-pager show --property=Version 2>&1)" || rc=$?
    elapsed=$(( SECONDS - started ))
    if [ "$rc" -ne 0 ]; then
        # With the bound in place these statuses are the BOUNDING wrapper's, and
        # they are classified as such rather than re-narrated as the manager's.
        # Correction 4 (Codex round-7 A10): GNU `timeout` returns 124 both when
        # it kills the child for exceeding the deadline AND when the child itself
        # exits 124 (e.g. `timeout 10s bash -c 'exit 124'` returns 124 at
        # elapsed_s=0). The wrapper cannot distinguish those, so 124 is NOT
        # labelled uniquely as a deadline; the honest token records the ambiguity.
        # (systemctl does not use 124 in practice, but that is a note about the
        # child, not something the bounding wrapper can prove from its own status.)
        case "$rc" in
            124) detail="manager_query_rc124_timeout_reached_or_child_exit_124" ;;
            137) detail="manager_query_killed_after_deadline" ;;
            125) detail="bounding_wrapper_failed" ;;
            126) detail="invocation_found_but_not_executable" ;;
            127) detail="invocation_command_not_found" ;;
            *)   detail="manager_query_nonzero_status" ;;
        esac
        p0_sanitize "$raw"
        p0_stop "system_manager_unreachable rc=$rc detail=$detail budget_s=$P0_MANAGER_QUERY_BUDGET_S elapsed_s=$elapsed text=[$P0_SAFE]"
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
    printf 'P0_system_manager_ready bus=system query=show_property_Version response_key=Version response_value=[%s] env=cleared bound=pinned_timeout_inside_cleared_env budget_s=%s kill_after_s=%s elapsed_s=%s binary=%s bounding_binary=%s scope=this_login_pid_and_mount_namespaces manager_identity=not_established\n' \
        "$P0_SAFE" "$P0_MANAGER_QUERY_BUDGET_S" "$P0_MANAGER_QUERY_KILL_AFTER_S" \
        "$elapsed" "$P0_SYSTEMCTL" "$P0_TIMEOUT"
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
# A third alternative, `... No such file or directory (os error 2)`, was carried
# here from RP7-WPI-RO.sh and is DELETED (audit-2 R2 nit 1). `(os error N)` is a
# Rust std::io::Error rendering emitted by uutils coreutils, and uutils derives
# its message prefix from the BASENAME of argv[0], while `$P0_STAT` is always
# absolute - so no producer can emit both halves and the alternative could never
# match. Keeping it would imply an observation this package never made.
p0_classify_stat_shape() {
    local p="$1" raw="$2"
    P0_SHAPE=""
    case "$raw" in
        "$P0_STAT: cannot statx '$p': $P0_EACCES_TEXT"|"$P0_STAT: cannot stat '$p': $P0_EACCES_TEXT")
            P0_SHAPE="eacces" ;;
        "$P0_STAT: cannot statx '$p': $P0_ENOENT_TEXT"|"$P0_STAT: cannot stat '$p': $P0_ENOENT_TEXT")
            P0_SHAPE="enoent" ;;
    esac
}

p0_probe_kind() {
    local p="$1" raw rc=0 sub subrc=0 n_eacces n_enoent classes
    P0_KIND=""; P0_FKIND=""
    raw="$(LC_ALL=C "$P0_STAT" -c '%F' -- "$p" 2>&1)" || rc=$?
    if [ "$rc" -eq 0 ]; then
        # Correction 3 (Codex round-7 A9): adjudicate the rc-0 producer SHAPE
        # before any classification. A multi-line, non-printable or empty rc-0
        # `%F` response is unevaluable, not a host object kind: folding CR/LF to
        # spaces first (what p0_sanitize does) let `directory\nwarning\n` sanitise
        # to a token that fell through to the `*) other` arm and reached a
        # host-state FAIL (venv_root_kind_unexpected) on a probe that never
        # produced a single clean token (pattern 6: status good, shape not, STOP).
        case "$raw" in
            '') p0_stop "path_probe_empty path=$p rc=0" ;;
        esac
        case "$raw" in
            *$'\r'*|*$'\n'*)
                p0_sanitize "$raw"
                p0_stop "path_probe_multiline path=$p rc=0 detail=$P0_SAFE" ;;
        esac
        case "$raw" in
            *[![:print:]]*)
                p0_sanitize "$raw"
                p0_stop "path_probe_nonprintable path=$p rc=0 detail=$P0_SAFE" ;;
        esac
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
    canon="$(LC_ALL=C "$P0_READLINK" -v -f -- "$d" 2>&1)" || rc=$?
    if [ "$rc" -ne 0 ]; then
        p0_prepare_readlink_detail "$canon"
        p0_stop "venv_root_canonicalization_failed path=$d rc=$rc detail=[$P0_SAFE] diagnostic_shape=$P0_RESOLUTION"
    fi
    # Correction 3 (Codex round-7 A9): adjudicate the rc-0 readlink -f SHAPE
    # before the comparison. An empty, multi-line, non-printable or non-absolute
    # canonical response is unevaluable, not a venv-root divergence: only a valid
    # complete canonical path that differs from the preregistered literal may be
    # a FAIL (pattern 6: status good, shape not, so STOP).
    case "$canon" in
        '') p0_stop "venv_root_canonicalization_unparsable path=$d rc=0 detail=response_empty" ;;
    esac
    case "$canon" in
        *$'\r'*|*$'\n'*)
            p0_sanitize "$canon"
            p0_stop "venv_root_canonicalization_unparsable path=$d rc=0 detail=[response_multiline:$P0_SAFE]" ;;
    esac
    case "$canon" in
        *[![:print:]]*)
            p0_sanitize "$canon"
            p0_stop "venv_root_canonicalization_unparsable path=$d rc=0 detail=[response_nonprintable]" ;;
    esac
    case "$canon" in
        /*) : ;;
        *)  p0_sanitize "$canon"
            p0_stop "venv_root_canonicalization_unparsable path=$d rc=0 detail=[response_not_absolute:$P0_SAFE]" ;;
    esac
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
    # isolated mode AND with `site` startup disabled: PYTHONPATH, PYTHONSTARTUP,
    # PYTHONHOME and a current-working-directory shadow are removed as channels by
    # `-I` (pattern 4, audit-2 A2-F1), and the venv's own startup code is removed
    # as a channel by `-S` (audit-3 F1).
    # `-I` alone was NOT enough and the claim that it was is the defect this line
    # repairs. `-I` implies `-E`, `-P` and `-s`; it does NOT imply `-S`. Without
    # `-S` the interpreter imports `site` during startup, processes this venv's
    # `site-packages`, and EXECUTES every `import` line in its `*.pth` files -
    # plus any `sitecustomize`/`usercustomize` module in that tree - before the
    # `-c` body is compiled. That is arbitrary code from the very object this
    # block is testing, running with this login's authority, and it can write
    # anywhere this login can write and still let the accepted `P0PY` line be
    # printed afterwards. A forged one-line `.pth` in a real venv did exactly
    # that under the previous bytes (SELF_QA_RP6.md, R4 F1 fence).
    # The child also verifies its OWN startup rather than trusting that the flag
    # words survived: if `sys.flags.isolated` and `sys.flags.no_site` are not both
    # set it refuses to report a version and says so. That self-check guards only
    # against ACCIDENTAL flag-word loss - it runs inside the `-c` body, which a
    # cooperating venv permits, so it catches the case where the words are dropped
    # but the interpreter still reaches the body. It is NOT a substitute for
    # `-S`, and the earlier claim that deleting ` -S` "cannot silently restore the
    # hole - it produces a named STOP" was false and is retracted. A HOSTILE
    # `.pth` in this venv's `site-packages` runs at `site` startup when `-S` is
    # removed, BEFORE the `-c` body is compiled, so it can write the forged `P0PY`
    # line and `os._exit(0)` and the self-check never runs: against such a `.pth`
    # the no-`-S` mutant returns rc 0 with no STOP and the forged accepted line
    # (SELF_QA_RP6.md R6-F1 adversarial-`.pth` fence, RED). ` -S` itself is the
    # control that closes the channel - with it present `site` startup never runs,
    # the hostile `.pth` is never processed, and the `-c` body the self-check
    # guards is the one that actually executes (GREEN) - so the load-bearing
    # protection is ` -S`, not the self-check.
    # Only `sys` is imported and only one line is written to stdout.
    raw="$(LC_ALL=C "$P0_ENV" -i LC_ALL=C "$py" -I -S -c 'import sys
if not (sys.flags.isolated and sys.flags.no_site):
    sys.stdout.write("P0PY_STARTUP_UNPROVEN isolated=%d no_site=%d" % (sys.flags.isolated, sys.flags.no_site))
    raise SystemExit(0)
sys.stdout.write("P0PY %d.%d" % sys.version_info[:2])' 2>&1)" || rc=$?
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
    # The child's own startup verdict is read BEFORE its result is parsed. This
    # is an inability to evaluate, never a host-state FAIL: the interpreter ran,
    # but it could not prove the launch was isolated and site-free, so nothing
    # this block would say about read-only scope would be established.
    case "$raw" in
        "P0PY_STARTUP_UNPROVEN "*)
            p0_sanitize "$raw"
            p0_stop "interpreter_startup_not_isolated path=$py detail=[$P0_SAFE] expected=isolated_and_no_site" ;;
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
    # establish. Recording rather than comparing is also why running the venv's
    # own interpreter here does not violate "no process may adjudicate its own
    # state": this arm accepts nothing the venv said about itself - it observes
    # that the preregistered object executes - and the two RO-stage adjudicators
    # that DO accept a result run under the separately pinned trusted python3.
    # Correction 4 (Codex round-7 A10): the prior tokens (`isolated=yes`,
    # `site_startup=disabled`, `venv_pth_and_sitecustomize=not_executed`) asserted
    # startup behaviour the block cannot prove: it REQUESTED `-I -S` and the CHILD
    # reported sys.flags.isolated/no_site, but the interpreter binary's provenance
    # is not independently bound, so an arbitrary executable at that path could
    # forge the output. The line now states only what is established: the
    # requested launch flags plus the child-reported, self-verified flag state,
    # with site/.pth non-execution disclosed as not-established-rather-than-claimed
    # (pattern 9: the sentence must not outrun the probe).
    printf 'P0_interpreter path=%s exec=ok env=cleared launch_flags=requested_-I_-S child_reported_startup_flags=sys.flags.isolated_and_no_site self_verified=yes site_startup_disable=requested_not_binary_attested venv_pth_sitecustomize_execution=not_established_binary_provenance_unbound reported_version=%s.%s adjudication=recorded_not_compared interpreter_binary_behaviour=not_attested\n' \
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
printf 'P0_claim establishes=executing_numeric_identity_of_this_login,name_to_numeric_resolution_of_gatea_and_mtc_bridge_via_getent,forbidden_gid_non_membership,resolution_and_executability_of_the_12_preregistered_tools_each_bound_to_its_frozen_deploy_channel_pin,evidence_stdout_bound_to_create_once_leaf,deploy_attested_user_mount_pid_network_namespaces_and_root_mount_identity,system_manager_answered_a_Manager_property_query_over_the_system_bus_within_a_bounded_deadline_after_execution_domain_binding,venv_interpreter_leaf_kind_and_executability_under_requested_-I_-S_startup_child_reports_isolated_no_site\n'
printf 'P0_claim does_not_establish=any_RO_row_host_state,tool_provenance_or_distribution_identity,behaviour_inside_any_executed_tool_binary,nss_source_identity_of_getent_resolution,round1_4_probe_execution_environment_binding,identity_of_the_manager_that_answered,binding_of_these_namespaces_to_any_service,accepted_mount_topology_for_every_preregistered_host_path,interpreter_intermediate_component_or_symlink_target_binding,interpreter_version_or_package_parity,persistence_of_any_checked_object_between_this_preflight_and_the_RO_stage,anything_under_the_protected_metadata_directories,anything_about_group_C,procfs_mount_identity_of_the_namespace_links\n'
printf 'P0_claim scope=this_login_only identity=numeric_only mutation=no_filesystem_write_primitive_in_this_shell_source child_side_effects=not_attested venv_startup_disable=requested_via_-S_and_child_reported_binary_provenance_unbound interpreter_launch=requested_-I_-S_child_reports_isolated_and_no_site_binary_provenance_unbound manager_query=bounded_by_pinned_timeout_inside_cleared_env evidence_leaf=allocated_by_RP0-BOOTSTRAP child_env=mixed coreutils_launch=recorded_absolute_after_PATH_resolution inherited_env=stat_readlink_id_getent cleared_env=systemctl_timeout_and_interpreter_only cwd=caller_inherited tmpdir=caller_inherited_or_unset\n'
printf 'P0 PASS\n'
