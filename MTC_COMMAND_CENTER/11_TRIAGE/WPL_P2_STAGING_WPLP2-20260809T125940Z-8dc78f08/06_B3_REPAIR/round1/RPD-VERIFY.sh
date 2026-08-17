# ===== BLOCK-ID: RPD-VERIFY ===== [EXECUTABLE PROPOSAL BLOCK]
# WP-L Phase 2 - root-side deploy-time admission verify (PROPOSED DESIGN, NEW in
# the B3-GAP-ENV repair, Option 1, round 1). NOT host-authorized.
# DESIGN ONLY IN THIS UNIT: no execution path exists for this block tonight. It
# enters the runkit as a frozen, NON-EXECUTED block exactly like RP3/RP5, and it
# is intended to run as root at install/deploy time through the deploy channel.
# Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b (identifier arrives as an
# input, see below; it is never derived on the host).
#
# It carries the two admissions an unprivileged operator cannot evaluate on this
# host (03_TRANSPORT/B3_STOP_ADJUDICATION.md): the env file's mode/owner, and the
# install manifest's mode/owner plus BOTH of its bindings. Those checks are moved
# here unweakened - identical predicate strength, identical three-outcome rc
# handling - not relaxed.
#
# Read-only `stat` and silent `grep -qsF` only. No mutation of any kind, no
# sudo, no group/ACL change, no service action, no network, no POST /api/arm, no
# broker/exchange/order/TESTNET/mainnet/economic action. No file content is
# printed and no credential value is read: the env file's METADATA is probed and
# the file itself is never opened. Requires RP0-LIB sourced.
#
# rc contract, unchanged from RP0-LIB: 0 = admitted, 1 = FAIL (deviant state),
# 3 = STOP (could not evaluate). A STOP is never re-read as a PASS.
set -Eeuo pipefail

ENV_FILE="/etc/mtc-bridge/mtc-bridge.env"
INSTALL_MANIFEST="/etc/mtc-bridge/install_manifest.json"

rpd_stop() { printf 'RPD_STOP reason=%s\n' "$*"; exit 3; }
rpd_fail() { printf 'RPD_FAIL reason=%s\n' "$*"; exit 1; }

# Preregistered, never derived here. The candidate release SHA and the accepted
# RELEASE_SHA256SUMS sha256 arrive as required environment variables from the
# operator's preregistration. Deriving either from the host would let the host
# attest to its own acceptance; PREREGISTRATION.md sec. 2 states the rule for the
# second value directly - a manifest cannot attest to its own acceptance - and it
# applies with equal force to the release SHA the manifest is tested against.
#
# The accepted `:?` guard form of RP1-B3 is kept verbatim below, but it is
# PRECEDED by an explicit rc-3 check, and the two are not redundant. A bare
# `: "${VAR:?msg}"` aborts a non-interactive shell with rc 1, i.e. exactly the
# code this contract reserves for "the host state is deviant". A missing
# deploy-time input is not deviant host state, it is COULD NOT EVALUATE, and a
# deploy harness that reads rc 1 as a host verdict would draw the wrong
# conclusion from an operator plumbing error. The pre-check classifies it as
# STOP and puts a reason string on stdout; the `:?` line is retained so the
# accepted guard form still fails closed if the pre-check is ever edited out.
[ -n "${RPD_CANDIDATE_SHA:-}" ] \
    || rpd_stop "input_missing name=RPD_CANDIDATE_SHA detail=preregistered candidate release sha, 40 lowercase hex, never derived here"
[ -n "${RPD_RELEASE_MANIFEST_SHA256:-}" ] \
    || rpd_stop "input_missing name=RPD_RELEASE_MANIFEST_SHA256 detail=preregistered accepted RELEASE_SHA256SUMS sha256, 64 lowercase hex, never derived here"
: "${RPD_CANDIDATE_SHA:?preregistered candidate release sha is required, 40 lowercase hex, never derived here}"
: "${RPD_RELEASE_MANIFEST_SHA256:?preregistered accepted RELEASE_SHA256SUMS sha256 is required, 64 lowercase hex, never derived here}"

# --- RP0-LIB precondition ---------------------------------------------------
# Same reason as in RP1-B3: unsourced, the first predicate call would abort under
# `set -e` with rc 127 and no reason string, which is neither a FAIL nor a STOP.
command -v rp0_probe_path >/dev/null 2>&1 || rpd_stop "rp0_lib_not_sourced predicate=rp0_probe_path"

# --- root precondition ------------------------------------------------------
# Every check in this block is exactly the set an unprivileged caller cannot
# evaluate on this host. Running unprivileged is therefore COULD NOT EVALUATE and
# it must never degrade into a silent skip or a partial pass: that degradation is
# what would let a deploy believe the env file had been admitted when nothing
# looked at it. Non-root is STOP.
# Identity is read NUMERICALLY, for the same reason as in RP1-B3: `id -un` needs
# a name-service lookup that can fail on a healthy host, and on hosts whose
# account names are not ASCII it would also put non-ASCII bytes into an evidence
# log that is required to be ASCII. uid 0 is the predicate; a name adds nothing.
rpd_require_root() {
    local uid
    uid="$(id -u)"   || rpd_stop "uid_probe_failed"
    [ "$uid" = "0" ] || rpd_stop "must_run_as_root uid=$uid"
    printf 'RPD_identity uid=%s\n' "$uid"
}

# --- preregistered input format guard ---------------------------------------
# args: <variable name> <value> <expected length>
# Not cosmetic. `grep -F` treats a MULTI-LINE pattern as a SET of alternatives,
# so a value carrying a newline or a CR (a mis-plumbed deploy variable, a value
# read from a CRLF file) would silently turn each binding test into a match
# against an unrelated manifest line and could manufacture a PASS. Constraining
# the charset to lowercase hex and the length to the preregistered width removes
# that whole class, plus every quoting surprise, before either grep runs.
# Over-constraint is deliberate and fail-closed: an identifier of a different
# width STOPs and forces a new preregistration instead of matching silently.
# The value is NOT printed on either STOP arm - a mis-plumbed variable may hold
# something that must not reach an evidence log. It is printed only after it has
# been proven to be pure lowercase hex of the preregistered width.
rpd_require_hex() {
    local name="$1" val="$2" want_len="$3"
    case "$val" in
        *[!0-9a-f]*) rpd_stop "input_charset name=$name expected=lowercase_hex" ;;
    esac
    [ "${#val}" = "$want_len" ] || rpd_stop "input_length name=$name len=${#val} expected=$want_len"
    printf 'RPD_input name=%s value=%s\n' "$name" "$val"
}

# --- exact mode + owner on a REGULAR file, candidate strength ---------------
# Reproduces candidate common.sh assert_mode_owner (:80-93) with one deliberate
# tightening: both paths here are files, so `dir` is NOT an accepted kind (the
# shared helper in RP1-B3 accepts `regular|dir` because it also guards trees).
# `stat` is not given -L, so a symlink at either canonical path is classified
# link_live/link_dangling by rp0_probe_path and FAILs instead of being followed.
# Exact octal mode and exact owner:group; there is no accepted alternative mode.
rpd_assert_regular_mode_owner() {
    local p="$1" want_mode="${2#0}" want_own="$3" kind mode own
    kind="$(rp0_probe_path "$p")" || exit 3
    case "$kind" in
        regular) : ;;
        absent)                  rpd_fail "missing path=$p" ;;
        dir)                     rpd_fail "expected a regular file kind=dir path=$p" ;;
        link_live|link_dangling) rpd_fail "canonical deployment path is a symlink kind=$kind path=$p" ;;
        *)                       rpd_fail "unexpected object kind=$kind path=$p" ;;
    esac
    mode="$(LC_ALL=C stat -c '%a' -- "$p")"   || rpd_stop "mode_probe_failed path=$p"
    own="$(LC_ALL=C stat -c '%U:%G' -- "$p")" || rpd_stop "owner_probe_failed path=$p"
    printf 'RPD_stat path=%s owner=%s mode=%s\n' "$p" "$own" "$mode"
    [ "$mode" = "$want_mode" ] || rpd_fail "path=$p mode=$mode expected=$want_mode"
    [ "$own"  = "$want_own"  ] || rpd_fail "path=$p owner=$own expected=$want_own"
}

# --- install-manifest binding, silent, three-outcome ----------------------
# Candidate verify.sh:129-135 binds BOTH the candidate release SHA and the
# release/payload manifest SHA. `grep -qsF` prints nothing, so no unrelated
# manifest content reaches the evidence log. rc 0 = bound, rc 1 = not bound,
# any other rc = read/tool error = STOP (never "not bound").
rpd_assert_manifest_binding() {
    local manifest="$1" release_sha="$2" manifest_sha="$3" kind rc=0
    kind="$(rp0_probe_path "$manifest")" || exit 3
    [ "$kind" = "regular" ] || rpd_fail "install manifest kind=$kind path=$manifest"
    LC_ALL=C grep -qsF -- "\"release_sha\": \"$release_sha\"" "$manifest" || rc=$?
    case "$rc" in
        0) : ;;
        1) rpd_fail "install manifest does not bind release_sha" ;;
        *) rpd_stop "install_manifest_unreadable path=$manifest grep_rc=$rc" ;;
    esac
    rc=0
    LC_ALL=C grep -qsF -- "\"release_manifest_sha256\": \"$manifest_sha\"" "$manifest" || rc=$?
    case "$rc" in
        0) : ;;
        1) rpd_fail "install manifest does not bind release_manifest_sha256" ;;
        *) rpd_stop "install_manifest_unreadable path=$manifest grep_rc=$rc" ;;
    esac
    printf 'RPD_manifest_binding path=%s bound=both\n' "$manifest"
}

printf 'RPD_SECTION identity\n'
rpd_require_root

# Guarded BEFORE anything prints either value.
printf 'RPD_SECTION preregistered_inputs\n'
rpd_require_hex RPD_CANDIDATE_SHA           "$RPD_CANDIDATE_SHA"           40
rpd_require_hex RPD_RELEASE_MANIFEST_SHA256 "$RPD_RELEASE_MANIFEST_SHA256" 64

printf 'RPD_SECTION header candidate=%s\n' "$RPD_CANDIDATE_SHA"

# Metadata only. The env file is stat'ed and never opened: its mode and owner are
# the admission, its content is out of scope for every block in this unit.
printf 'RPD_SECTION conf_metadata\n'
rpd_assert_regular_mode_owner "$ENV_FILE"         0600 root:root
rpd_assert_regular_mode_owner "$INSTALL_MANIFEST" 0640 root:root

printf 'RPD_SECTION manifest_binding\n'
rpd_assert_manifest_binding "$INSTALL_MANIFEST" "$RPD_CANDIDATE_SHA" "$RPD_RELEASE_MANIFEST_SHA256"

printf 'RPD_SECTION done\n'
printf 'RPD_claim scope=root_side_deploy_time checks=env_mode_owner,manifest_mode_owner,manifest_binding\n'
printf 'RPD PASS\n'
