# WP-I Stage 2 — remote base allocation (PREREGISTERED, create-once).
#
# Transport op 01. Delivered on ssh stdin to the frozen remote launch domain,
# which `transport_runner.ps1` holds as a constant and every plan row must carry
# verbatim:
#   /usr/bin/env -i PATH=/usr/bin:/bin LC_ALL=C HOME=/home/gatea \
#     /usr/bin/bash --noprofile --norc -s -- <REMOTE_BASE>
#
# Creates exactly five directories and nothing else — the base, the evidence
# parent, the evidence runkit directory, the kit directory, and `<BASE>/work`,
# the run-owned scratch root that ops 07/08 receive as their third argument so
# the close script never inherits a TMPDIR location (Codex final audit F2,
# derivation class 6). It never deletes, never
# renames, never chmods an existing object, never uses `mkdir -p`, never
# creates a temporary file, never touches a service, a unit, a credential, the
# network or the bridge. It runs BEFORE the runkit exists on the host, so it
# deliberately depends on nothing from the runkit: no proposal block is sourced
# or executed here.
#
# Round 2 repairs (Codex F3/F4/F5):
#   * every executable is a verified absolute pin - nothing is selected by the
#     inherited PATH, and no `mktemp`/`TMPDIR` object is created at all;
#   * the ENTIRE parent chain is bound - non-symlink, canonical, searchable,
#     numerically owned, not group/other writable - BEFORE the first mkdir;
#   * identity is numeric (`%u:%g`); the rendered `%U:%G` name is diagnostic
#     only;
#   * a path probe that cannot be classified - multiline, mixed, unexpected
#     prose, or a kernel answer that contradicts the diagnostic - is STOP, and
#     STOP happens before any mutation.
#
# Round 3 repair (Codex round-2 re-audit F4): the round-2 chain binding covered
# the symlink half of "the leaf is not the path" and not the mount half. A bind
# or overlay mount at the same literal canonical path presents the expected
# owner, mode and canonicalisation, so every component predicate passed and all
# four directories were created inside the substituted object. The allocation
# parent's COVERING MOUNT is therefore projected from `/proc/self/mountinfo` and
# compared, before the first mkdir, against an identity a root-authorised deploy
# channel attested outside this login session (owner grant #6). It is never
# learned from the session being tested; an unfilled pin or a mismatch is STOP.
#
# Round 4 repairs (Codex final audit F1, derivation classes 5 and 6): the remote
# interpreter and its startup environment are now inside the pinned program
# domain rather than selected by the login shell's PATH, and this script attests
# that domain before its first external program; and it allocates the run-owned
# scratch root that removes the close script's inherited-TMPDIR channel.
#
# rc contract: 0 = allocated, 1 = FAIL (predicate refused), 3 = STOP (could not
# evaluate — never re-read as "absent" or as success).
set -Eeuo pipefail

# --- class 5: launch-domain attestation --------------------------------------
# This block runs BEFORE the first external program, so a plant that replaced
# the interpreter or injected a startup file is refused rather than measured. A
# launch-domain violation is an inability to evaluate, never a host finding:
# every arm here is rc 3.
EXPECT_INTERPRETER='/usr/bin/bash'
EXPECT_LAUNCH_PATH='/usr/bin:/bin'
EXPECT_LAUNCH_LC_ALL='C'
EXPECT_LAUNCH_HOME='/home/gatea'
LD_ENVIRON='/proc/self/environ'

# The inherited-function sweep runs BEFORE this script defines a function of its
# own, so `declare -F` describes only what the launch domain delivered rather
# than this program's own names. `declare -F` exits 1 when there is nothing to
# list, which under `set -e` would end the run with no marker at all, so its
# status is consumed deliberately and the emptiness is tested afterwards.
LD_FUNCS="$(declare -F 2>/dev/null || :)"
if [ -n "$LD_FUNCS" ]; then
    printf 'SETUP_STOP reason=launch_domain_inherited_shell_function detail=[%s]\n' "$LD_FUNCS" >&2
    exit 3
fi

# MEASURED SCOPE LIMIT (round 4, recorded rather than implied). `bash` reads
# `$BASH_ENV` before the first byte of a stdin-delivered script, and
# `--norc`/`--noprofile` do not disable that channel, so a startup plant that
# EXITS forges the record before anything here runs. No in-script attestation
# can close that. It is closed on the operator side, by the frozen `env -i`
# launch domain with an explicit complete variable list that
# `transport_runner.ps1` enforces verbatim on every plan row, so no plan row can
# introduce `BASH_ENV` at all - which is why the domain is stated on both sides.
# A plant that lets the script RUN, the only kind that could forge a
# real-looking record, is refused by the sweep below: `BASH_ENV` is still in the
# exec environment the kernel recorded. Both cases are executed in self-QA.
ld_stop() { printf 'SETUP_STOP reason=%s\n' "$*" >&2; exit 3; }

[ "${BASH:-}" = "$EXPECT_INTERPRETER" ] \
    || ld_stop "launch_domain_interpreter=${BASH:-unset} expected=$EXPECT_INTERPRETER"
if shopt -q login_shell; then ld_stop "launch_domain_login_shell_startup_files_were_read"; fi

# The exec environment is read from the kernel's own copy rather than from the
# shell's exported-name list: `/proc/self/environ` is what `execve` received, so
# names the shell adds for its children (PWD, SHLVL, _) cannot mask an entry the
# launch domain actually delivered. Each expected entry is matched as a WHOLE
# `name=value` string and must appear exactly once; anything else — BASH_ENV,
# ENV, LD_PRELOAD, a BASH_FUNC_x%% exported function, an inherited TMPDIR — is a
# name this sweep does not recognise, and it STOPs naming the offender. The read
# is a redirection, not an external program.
[ ! -L "$LD_ENVIRON" ] || ld_stop "launch_domain_environ_is_symlink path=$LD_ENVIRON"
[ -r "$LD_ENVIRON" ]   || ld_stop "launch_domain_environ_unreadable path=$LD_ENVIRON"
LD_SEEN_PATH=0; LD_SEEN_LC_ALL=0; LD_SEEN_HOME=0; LD_ENTRIES=0
LD_ENTRY=''
while IFS= read -r -d '' LD_ENTRY || [ -n "$LD_ENTRY" ]; do
    [ -n "$LD_ENTRY" ] || continue
    LD_ENTRIES=$((LD_ENTRIES + 1))
    case "$LD_ENTRY" in
        "PATH=$EXPECT_LAUNCH_PATH")     LD_SEEN_PATH=$((LD_SEEN_PATH + 1)) ;;
        "LC_ALL=$EXPECT_LAUNCH_LC_ALL") LD_SEEN_LC_ALL=$((LD_SEEN_LC_ALL + 1)) ;;
        "HOME=$EXPECT_LAUNCH_HOME")     LD_SEEN_HOME=$((LD_SEEN_HOME + 1)) ;;
        *) ld_stop "launch_domain_unexpected_environment_entry name=[${LD_ENTRY%%=*}]" ;;
    esac
    LD_ENTRY=''
done < "$LD_ENVIRON"
[ "$LD_ENTRIES" -eq 3 ]     || ld_stop "launch_domain_environment_size=$LD_ENTRIES expected=3"
[ "$LD_SEEN_PATH" -eq 1 ]   || ld_stop "launch_domain_path_entries=$LD_SEEN_PATH expected=1 value=$EXPECT_LAUNCH_PATH"
[ "$LD_SEEN_LC_ALL" -eq 1 ] || ld_stop "launch_domain_lc_all_entries=$LD_SEEN_LC_ALL expected=1 value=$EXPECT_LAUNCH_LC_ALL"
[ "$LD_SEEN_HOME" -eq 1 ]   || ld_stop "launch_domain_home_entries=$LD_SEEN_HOME expected=1 value=$EXPECT_LAUNCH_HOME"

export LC_ALL=C

EXPECT_PREFIX='/home/gatea/wpi_staging_'
EXPECT_PARENT='/home/gatea'
EXPECT_UID='<PIN-AT-FREEZE>'
EXPECT_GID='<PIN-AT-FREEZE>'
EXPECT_OWNER_NAME='gatea:gatea'
EXPECT_MODE='700'
# The covering-mount identity of EXPECT_PARENT, attested by the deploy channel
# before op 01 runs (owner grant #6). Rendered exactly as the projection below
# renders it, one line, space-separated key=value fields in this fixed order.
EXPECT_PARENT_MOUNT='<PIN-AT-FREEZE>'
MOUNTINFO='/proc/self/mountinfo'

fail() { printf 'SETUP_FAIL reason=%s\n' "$*" >&2; exit 1; }
stop() { printf 'SETUP_STOP reason=%s\n' "$*" >&2; exit 3; }
note() { printf 'SETUP_NOTE %s\n' "$*"; }

# --- pinned program identities ----------------------------------------------
# The absolute path IS the pin; the inherited PATH selects nothing. `stat` is
# the bootstrap root of trust and is the first object verified, including
# itself. Ownership is compared numerically.
TOOL_STAT='/usr/bin/stat'
TOOL_MKDIR='/usr/bin/mkdir'
TOOL_READLINK='/usr/bin/readlink'
# The launch domain's own two programs are admitted under the same rule, so the
# interpreter this script attested above is inside the pinned program domain
# rather than beside it (derivation class 5).
TOOL_ENV='/usr/bin/env'
TOOL_BASH='/usr/bin/bash'

require_tool() {
    local t="$1" own mode g o
    case "$t" in /*) : ;; *) stop "tool_path_not_absolute path=$t" ;; esac
    [ ! -L "$t" ] || stop "tool_is_symlink path=$t"
    [ -f "$t" ]   || stop "tool_missing_or_not_regular path=$t"
    [ -x "$t" ]   || stop "tool_not_executable path=$t"
    own="$("$TOOL_STAT" -c '%u:%g' -- "$t" </dev/null 2>/dev/null)" || stop "tool_owner_probe_failed path=$t"
    mode="$("$TOOL_STAT" -c '%a' -- "$t" </dev/null 2>/dev/null)"   || stop "tool_mode_probe_failed path=$t"
    [ "$own" = '0:0' ] || stop "tool_owner_numeric=$own expected=0:0 path=$t"
    o="${mode#"${mode%?}"}"
    g="${mode%?}"; g="${g#"${g%?}"}"
    case "$o" in 2|3|6|7) stop "tool_other_writable mode=$mode path=$t" ;; esac
    case "$g" in 2|3|6|7) stop "tool_group_writable mode=$mode path=$t" ;; esac
    note "tool name=${t##*/} path=$t owner_numeric=$own mode=$mode resolution=pinned_absolute"
}

require_tool "$TOOL_STAT"
require_tool "$TOOL_MKDIR"
require_tool "$TOOL_READLINK"
require_tool "$TOOL_ENV"
require_tool "$TOOL_BASH"

# The attested interpreter must be the pinned OBJECT, not merely a path that
# spells the same characters: `$BASH` was compared as a string in the class 5
# block, and the pin admitted `/usr/bin/bash` as a non-symlink root-owned
# regular file here.
[ "$BASH" = "$TOOL_BASH" ] || stop "launch_domain_interpreter_outside_pinned_set value=$BASH"
note "launch_domain interpreter=$BASH path=$PATH lc_all=$EXPECT_LAUNCH_LC_ALL home=$HOME exec_environment_entries=$LD_ENTRIES inherited_functions=0 bash_env=absent env=absent tmpdir=absent attestation=builtins_and_proc_self_environ"

# --- the preregistered numeric identity must actually be pinned -------------
case "$EXPECT_UID" in ''|*[!0-9]*) stop "identity_pin_unfilled field=EXPECT_UID" ;; esac
case "$EXPECT_GID" in ''|*[!0-9]*) stop "identity_pin_unfilled field=EXPECT_GID" ;; esac
# The mount attestation is a missing INPUT, not a failed predicate, so an
# unfilled or malformed pin is rc 3 and is refused here - before any path is
# probed and long before any mutation.
#
# The marker is COMPOSED rather than written out, so that a Stage 1 fill which
# replaces the placeholder text globally cannot also rewrite the guard that
# detects it. A guard carrying the literal would be replaced by the real value
# and would then STOP on a correctly frozen script - fail-closed in the wrong
# place, which is still a defect.
PIN_MARKER="$(printf '<PIN-%s>' 'AT-FREEZE')"
case "$EXPECT_PARENT_MOUNT" in
    ''|"$PIN_MARKER") stop "mount_pin_unfilled field=EXPECT_PARENT_MOUNT" ;;
    device=*\ root=*\ mount_point=*\ fstype=*\ source=*\ shared_mount_point_records=*) : ;;
    *) stop "mount_pin_malformed field=EXPECT_PARENT_MOUNT value=[$EXPECT_PARENT_MOUNT]" ;;
esac
[ "$EUID" = "$EXPECT_UID" ] || fail "login_euid=$EUID expected=$EXPECT_UID"
note "identity euid=$EUID expected_numeric=$EXPECT_UID:$EXPECT_GID name_diagnostic=$EXPECT_OWNER_NAME"

[ "$#" -eq 1 ] || fail "usage remote_setup_wpi.sh <REMOTE_BASE> argc=$#"
BASE="$1"

# --- the base must be EXACTLY <EXPECT_PREFIX><one safe component>.
# A separator, `.`, `..`, a leading `-` or any character outside
# [A-Za-z0-9._-] in the suffix would place the whole evidence tree somewhere
# other than the preregistered path while every later check still "passed".
case "$BASE" in
    "$EXPECT_PREFIX"*) SUFFIX="${BASE#"$EXPECT_PREFIX"}" ;;
    *) fail "base_prefix base=[$BASE] expected_prefix=[$EXPECT_PREFIX]" ;;
esac
case "$SUFFIX" in
    ""|"."|"..")       fail "base_component_reserved value=[$SUFFIX]" ;;
    -*)                fail "base_component_leading_dash value=[$SUFFIX]" ;;
    *[!A-Za-z0-9._-]*) fail "base_component_charset value=[$SUFFIX]" ;;
esac
note "base_component_ok value=$SUFFIX"

# --- bind every parent component BEFORE any mutation ------------------------
# Pattern 3: the leaf is not the path. A live symlink, a non-canonical
# component, or a group/other-writable ancestor lets the whole evidence tree be
# relocated while every leaf check still passes. This runs before the first
# mkdir, so a refusal costs no created directory.
bind_component() {
    local p="$1" want="$2" own name mode g o
    [ ! -L "$p" ] || stop "parent_component_is_symlink path=$p"
    [ -d "$p" ]   || stop "parent_component_not_a_directory path=$p"
    [ -x "$p" ]   || stop "parent_component_not_searchable path=$p"
    own="$("$TOOL_STAT" -c '%u:%g' -- "$p" </dev/null 2>/dev/null)"  || stop "parent_owner_probe_failed path=$p"
    name="$("$TOOL_STAT" -c '%U:%G' -- "$p" </dev/null 2>/dev/null)" || stop "parent_owner_name_probe_failed path=$p"
    mode="$("$TOOL_STAT" -c '%a' -- "$p" </dev/null 2>/dev/null)"    || stop "parent_mode_probe_failed path=$p"
    [ "$own" = "$want" ] || fail "parent_owner_numeric=$own expected=$want path=$p owner_name=$name"
    o="${mode#"${mode%?}"}"
    g="${mode%?}"; g="${g#"${g%?}"}"
    case "$o" in 2|3|6|7) fail "parent_other_writable mode=$mode path=$p" ;; esac
    case "$g" in 2|3|6|7) fail "parent_group_writable mode=$mode path=$p" ;; esac
    note "parent_bound path=$p owner_numeric=$own owner_name=$name mode=$mode"
}

bind_parent_chain() {
    local dir="$1" rest comp acc canon
    case "$dir" in /*) : ;; *) stop "parent_not_absolute path=$dir" ;; esac
    canon="$("$TOOL_READLINK" -f -- "$dir" </dev/null 2>/dev/null)" || stop "parent_canonicalization_failed path=$dir"
    [ "$canon" = "$dir" ] || fail "parent_not_canonical path=$dir canonical=$canon"
    bind_component '/' '0:0'
    acc=''
    rest="${dir#/}"
    while [ -n "$rest" ]; do
        comp="${rest%%/*}"
        if [ "$comp" = "$rest" ]; then rest=''; else rest="${rest#*/}"; fi
        acc="$acc/$comp"
        if [ "$acc" = "$dir" ]; then
            bind_component "$acc" "$EXPECT_UID:$EXPECT_GID"
        else
            bind_component "$acc" '0:0'
        fi
    done
}

# --- bind the covering MOUNT OBJECT of the allocation parent ----------------
# Pattern 3, the half a canonical-path check cannot reach: `readlink -f` and
# every component predicate are satisfied by a bind or overlay mount presenting
# the expected metadata at the same literal path, and the four directories are
# then created inside the substituted object. A later attestation cannot make an
# earlier mutation retroactively target the accepted mount, so this runs BEFORE
# the first mkdir.
#
# The projection is the section 4 `kind=point` record restricted to the one path
# this script mutates. The effective mount is the LONGEST matching mount point;
# among equally long matches the LAST record in `mountinfo` order, because a
# later record at the same mount point shadows the earlier one.
# `shared_mount_point_records` counts them, so a stacked mount is visible in the
# projection rather than silently collapsed.
#
# The reader has three exit conditions, not one (Pattern 7): a clean
# LF-terminated end, a populated final record carrying no trailing newline, and
# a source that yields no record at all - the last of which is STOP, never an
# empty projection read as "no mount covers this path".
project_covering_mount() {
    local path="$1"
    local line records=0 best='' best_mp='' best_len=-1 shared=0
    local dev root mp fstype src mplen covers
    [ ! -L "$MOUNTINFO" ] || stop "mountinfo_is_symlink path=$MOUNTINFO"
    [ -r "$MOUNTINFO" ]   || stop "mountinfo_unreadable path=$MOUNTINFO"
    while IFS= read -r line || [ -n "$line" ]; do
        [ -n "$line" ] || continue
        records=$((records + 1))
        # mountinfo escapes space, tab, newline and backslash as octal, so the
        # fields are separator-free; noglob keeps a `*` in a source name from
        # being expanded into filenames by the split.
        set -f
        set -- $line
        set +f
        [ "$#" -ge 10 ] || stop "mountinfo_record_short fields=$# record=[$line]"
        dev="$3"; root="$4"; mp="$5"
        shift 6
        while [ "$#" -gt 0 ] && [ "$1" != '-' ]; do shift; done
        [ "$#" -ge 4 ] || stop "mountinfo_record_no_separator record=[$line]"
        fstype="$2"; src="$3"
        covers=no
        if   [ "$mp" = '/' ];     then covers=yes
        elif [ "$mp" = "$path" ]; then covers=yes
        else case "$path" in "$mp"/*) covers=yes ;; esac
        fi
        [ "$covers" = yes ] || continue
        mplen="${#mp}"
        if [ "$mplen" -gt "$best_len" ]; then
            best_len="$mplen"; best_mp="$mp"; shared=1
            best="device=$dev root=$root mount_point=$mp fstype=$fstype source=$src"
        elif [ "$mplen" -eq "$best_len" ] && [ "$mp" = "$best_mp" ]; then
            shared=$((shared + 1))
            best="device=$dev root=$root mount_point=$mp fstype=$fstype source=$src"
        fi
    done < "$MOUNTINFO"
    [ "$records" -gt 0 ]  || stop "mountinfo_no_records path=$MOUNTINFO"
    [ "$best_len" -ge 0 ] || stop "mountinfo_no_covering_mount path=$path records=$records"
    printf '%s shared_mount_point_records=%s\n' "$best" "$shared"
}

bind_parent_mount() {
    local path="$1" observed
    observed="$(project_covering_mount "$path")" || exit $?
    note "parent_mount_observed path=$path $observed"
    [ "$observed" = "$EXPECT_PARENT_MOUNT" ] \
        || stop "parent_mount_differs path=$path observed=[$observed] attested=[$EXPECT_PARENT_MOUNT]"
    note "parent_mount_bound path=$path attestation=deploy_channel_before_op_01"
}

# --- calibrate the absence diagnostic against the pinned tool itself --------
# Substring-matching `No such file or directory` is what let a mixed
# ENOENT+EACCES diagnostic be read as absence. Instead the exact sentence this
# pinned `stat` emits for an absent name under an already-bound parent is
# measured once, in this run, and turned into a template. Every later
# classification must match that template as a WHOLE string. This binds to the
# pinned binary's real grammar rather than to prose guessed at authoring time,
# and any wrapper, prefix, suffix or second diagnostic fails the comparison.
ENOENT_TEMPLATE=''
calibrate_absence() {
    local probe="$1" diag rc=0
    if [ -e "$probe" ] || [ -L "$probe" ]; then stop "enoent_calibration_path_present path=$probe" ; fi
    diag="$("$TOOL_STAT" -c '%F' -- "$probe" </dev/null 2>&1)" || rc=$?
    [ "$rc" -ne 0 ] || stop "enoent_calibration_probe_succeeded path=$probe"
    case "$diag" in *$'\n'*|*$'\r'*) stop "enoent_calibration_multiline path=$probe" ;; esac
    case "$diag" in
        *"No such file or directory"*) : ;;
        *) stop "enoent_calibration_unrecognised path=$probe rc=$rc detail=$diag" ;;
    esac
    ENOENT_TEMPLATE="${diag//"$probe"/@PATH@}"
    [ "$ENOENT_TEMPLATE" != "$diag" ] || stop "enoent_calibration_no_path_in_diagnostic detail=$diag"
    note "enoent_calibration rc=$rc template=$ENOENT_TEMPLATE"
}

# --- classify one path with the kernel, corroborated by the diagnostic -------
# Preconditions: the parent chain is already bound, so the parent is a real,
# canonical, searchable directory, and the absence template has been calibrated.
# Under those preconditions the ONLY failure a leaf probe may be classified as
# is absence, and even then three independent statements must agree: `stat`
# failed, the kernel reports neither an object nor a link, and the diagnostic
# equals the calibrated template exactly. Anything else - multiline, mixed,
# wrapped, or unrecognised - is STOP, never "absent".
probe_leaf() {
    local p="$1" diag rc=0 expected
    [ -n "$ENOENT_TEMPLATE" ] || stop "path_probe_before_calibration path=$p"
    if [ -L "$p" ]; then printf 'link\n'; return 0; fi
    diag="$("$TOOL_STAT" -c '%F' -- "$p" </dev/null 2>&1)" || rc=$?
    case "$diag" in *$'\n'*|*$'\r'*) stop "path_probe_multiline path=$p rc=$rc" ;; esac
    if [ "$rc" -eq 0 ]; then
        case "$diag" in
            "symbolic link")                    printf 'link\n' ;;
            "regular file"|"regular empty file") printf 'regular\n' ;;
            "directory")                        printf 'dir\n' ;;
            *)                                  printf 'other\n' ;;
        esac
        return 0
    fi
    if [ -e "$p" ] || [ -L "$p" ]; then
        stop "path_probe_error path=$p rc=$rc detail=$diag"
    fi
    expected="${ENOENT_TEMPLATE//@PATH@/$p}"
    [ "$diag" = "$expected" ] || stop "path_probe_unclassified path=$p rc=$rc detail=$diag"
    printf 'absent\n'
}

# --- allocate one directory with a plain, non-recursive mkdir --------------
# `mkdir -m 0700` applies the mode explicitly, so a permissive umask cannot
# widen it. No `-p`: a missing intermediate must fail loudly, never be
# manufactured. Any non-zero rc or any diagnostic at all is STOP.
allocate() {
    local p="$1" out rc=0
    out="$("$TOOL_MKDIR" -m 0700 -- "$p" </dev/null 2>&1)" || rc=$?
    [ "$rc" -eq 0 ] || stop "mkdir_failed path=$p rc=$rc detail=$out"
    [ -z "$out" ]   || stop "mkdir_diagnostics path=$p detail=$out"
    note "allocated path=$p"
}

# --- prove the created directory is canonical, non-link, numerically owned --
assert_dir() {
    local p="$1" kind canon own name mode
    kind="$(probe_leaf "$p")" || exit $?
    [ "$kind" = "dir" ] || fail "created_kind=$kind path=$p"
    canon="$("$TOOL_READLINK" -f -- "$p" </dev/null 2>/dev/null)" || stop "canonicalization_failed path=$p"
    [ "$canon" = "$p" ] || fail "path_not_canonical path=$p canonical=$canon"
    own="$("$TOOL_STAT" -c '%u:%g' -- "$p" </dev/null 2>/dev/null)"  || stop "owner_probe_failed path=$p"
    name="$("$TOOL_STAT" -c '%U:%G' -- "$p" </dev/null 2>/dev/null)" || stop "owner_name_probe_failed path=$p"
    mode="$("$TOOL_STAT" -c '%a' -- "$p" </dev/null 2>/dev/null)"    || stop "mode_probe_failed path=$p"
    [ "$own"  = "$EXPECT_UID:$EXPECT_GID" ] || fail "owner_numeric=$own expected=$EXPECT_UID:$EXPECT_GID path=$p owner_name=$name"
    [ "$mode" = "$EXPECT_MODE"  ] || fail "mode=$mode expected=$EXPECT_MODE path=$p"
    note "dir_ok path=$p owner_numeric=$own owner_name=$name mode=$mode"
}

EV_PARENT="$BASE/evidence"
EV_RUNKIT="$EV_PARENT/runkit"
REMOTE_KIT="$BASE/kit"
# Derivation class 6 (Codex final audit F2). The close script's scratch root.
# It is a sibling of the evidence parent, never a descendant of it, so the
# canonical two-way non-overlap ops 07/08 prove before creating anything under
# it is a property of this allocation rather than of an inherited TMPDIR. It is
# allocated here, by the same create-once/bind-immediately discipline as the
# other four directories, because the close script must not create its own
# scratch root: a program that allocates the root it is about to trust proves
# nothing about where that root is.
REMOTE_WORK="$BASE/work"

# The base's parent must be exactly the preregistered parent: the suffix charset
# check above already forbids a separator, so this is a second, independent
# statement of the same fact rather than a new trust assumption.
[ "${BASE%/*}" = "$EXPECT_PARENT" ] || fail "base_parent=${BASE%/*} expected=$EXPECT_PARENT"
bind_parent_chain "$EXPECT_PARENT"
bind_parent_mount "$EXPECT_PARENT"
calibrate_absence "$EXPECT_PARENT/.wpi_enoent_calibration_probe"

# --- the base must be ABSENT as an object AND as a link --------------------
# `absent` here is the classified outcome, not "the test errored".
KIND="$(probe_leaf "$BASE")" || exit $?
[ "$KIND" = "absent" ] || fail "base_already_present kind=$KIND path=$BASE"
note "base_absent path=$BASE"

# Allocate and immediately bind each directory before the next one is created,
# so no later object is ever created through an unverified parent.
allocate "$BASE";        assert_dir "$BASE"
allocate "$EV_PARENT";   assert_dir "$EV_PARENT"
allocate "$EV_RUNKIT";   assert_dir "$EV_RUNKIT"
allocate "$REMOTE_KIT";  assert_dir "$REMOTE_KIT"
allocate "$REMOTE_WORK"; assert_dir "$REMOTE_WORK"

# The work root is proven disjoint from the evidence parent here as well as in
# the close script: this side states it at allocation time, so a plan that later
# passes some other path as WORK_ROOT is contradicting a recorded fact rather
# than merely failing a downstream check.
case "$REMOTE_WORK" in
    "$EV_PARENT"|"$EV_PARENT"/*) stop "work_root_inside_evidence_parent path=$REMOTE_WORK evidence=$EV_PARENT" ;;
esac
case "$EV_PARENT" in
    "$REMOTE_WORK"/*) stop "evidence_parent_inside_work_root path=$REMOTE_WORK evidence=$EV_PARENT" ;;
esac
note "work_root_allocated path=$REMOTE_WORK consumer=ops_07_08_remote_close_tree_wpi.sh disjoint_from=$EV_PARENT"

printf 'SETUP PASS base=%s evidence=%s runkit=%s kit=%s work=%s owner_numeric=%s:%s owner_name=%s mode=%s\n' \
    "$BASE" "$EV_PARENT" "$EV_RUNKIT" "$REMOTE_KIT" "$REMOTE_WORK" \
    "$EXPECT_UID" "$EXPECT_GID" "$EXPECT_OWNER_NAME" "$EXPECT_MODE"
