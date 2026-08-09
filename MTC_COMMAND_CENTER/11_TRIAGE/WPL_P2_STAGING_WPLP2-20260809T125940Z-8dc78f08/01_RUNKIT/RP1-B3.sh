# ===== BLOCK-ID: RP1-B3 ===== [EXECUTABLE PROPOSAL BLOCK]
# WP-L Phase 2 — B3 post-start permissions/ownership subcheck (PROPOSED DESIGN).
# Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b. NOT host-authorized.
# Read-only `stat`/`find`/silent `grep` only. No file content is printed, no
# credential value is read, no POST /api/arm, no broker/exchange/order/TESTNET/
# mainnet/economic action. Requires RP0-LIB sourced and RP0-BOOTSTRAP completed.
set -Eeuo pipefail

CAND="2ce41e34bceb599d80af24c5c33d835820ec321b"
REL="/opt/mtc-bridge/releases/$CAND"
VENV="/opt/mtc-bridge/venvs/$CAND"
STATE_DIR="/var/lib/mtc-bridge"
LOG_DIR="/var/log/mtc-bridge"
CONF_DIR="/etc/mtc-bridge"
ENV_FILE="/etc/mtc-bridge/mtc-bridge.env"
INSTALL_MANIFEST="/etc/mtc-bridge/install_manifest.json"
UNIT_FILE="/usr/local/lib/systemd/system/mtc-bridge-first-start.service"

# Preregistered, never derived here:
: "${B3_RELEASE_MANIFEST_SHA256:?preregistered accepted RELEASE_SHA256SUMS sha256 is required}"
: "${B3_SWEEP_BUDGET_S:?preregistered per-tree sweep budget in seconds is required}"

b3_stop() { printf 'B3_STOP reason=%s\n' "$*"; exit 3; }
b3_fail() { printf 'B3_FAIL reason=%s\n' "$*"; exit 1; }

# --- exact mode + owner, candidate strength --------------------------------
# Reproduces candidate common.sh assert_mode_owner (:80-93): exact octal mode and
# exact owner:group. There is no accepted alternative mode.
b3_assert_mode_owner() {
    local p="$1" want_mode="${2#0}" want_own="$3" kind mode own
    kind="$(rp0_probe_path "$p")" || exit 3
    case "$kind" in
        regular|dir) : ;;
        absent)                  b3_fail "missing path=$p" ;;
        link_live|link_dangling) b3_fail "canonical deployment path is a symlink kind=$kind path=$p" ;;
        *)                       b3_fail "unexpected object kind=$kind path=$p" ;;
    esac
    mode="$(LC_ALL=C stat -c '%a' -- "$p")"   || b3_stop "mode_probe_failed path=$p"
    own="$(LC_ALL=C stat -c '%U:%G' -- "$p")" || b3_stop "owner_probe_failed path=$p"
    printf 'B3_stat path=%s owner=%s mode=%s\n' "$p" "$own" "$mode"
    [ "$mode" = "$want_mode" ] || b3_fail "path=$p mode=$mode expected=$want_mode"
    [ "$own"  = "$want_own"  ] || b3_fail "path=$p owner=$own expected=$want_own"
}

# --- candidate any-write-bit sweep, budgeted, fail-closed ------------------
# Candidate common.sh:95-105 predicate, reproduced verbatim:
#     find "$root" ! -type l -perm /222 -print -quit
# `/222` matches ANY write bit (owner, group OR other). `-perm -0200` is
# owner-write-only and silently passes a 0020 or 0002 offender — that was F2.
# Honest cost: `-quit` shortens only a FAILING sweep; a clean tree is a full
# walk. The operator preregisters B3_SWEEP_BUDGET_S; exceeding it is STOP.
b3_assert_no_writable_paths() {
    local root="$1" offenders errf rc=0 t0 t1 elapsed_s
    errf="$(mktemp)" || b3_stop "sweep_tempfile_failed root=$root"
    t0="$(rp0_monotonic_ms)" || exit 3
    offenders="$(find "$root" ! -type l -perm /222 -print -quit 2>"$errf")" || rc=$?
    t1="$(rp0_monotonic_ms)" || exit 3
    if [ "$rc" -ne 0 ]; then
        b3_stop "writable_inventory_failed root=$root rc=$rc detail=$(tr -d '\r\n' <"$errf") partial=[$offenders]"
    fi
    rm -f "$errf"
    elapsed_s=$(( (t1 - t0) / 1000 ))
    printf 'B3_sweep root=%s elapsed_s=%s budget_s=%s\n' "$root" "$elapsed_s" "$B3_SWEEP_BUDGET_S"
    [ "$elapsed_s" -le "$B3_SWEEP_BUDGET_S" ] \
        || b3_stop "sweep_budget_exceeded root=$root elapsed_s=$elapsed_s budget_s=$B3_SWEEP_BUDGET_S"
    [ -z "$offenders" ] || b3_fail "writable path inside immutable tree: $offenders"
    printf 'B3_no_write_bit root=%s\n' "$root"
}

# --- install-manifest binding, silent, three-outcome ----------------------
# Candidate verify.sh:129-135 binds BOTH the candidate release SHA and the
# release/payload manifest SHA. `grep -qsF` prints nothing, so no unrelated
# manifest content reaches the evidence log. rc 0 = bound, rc 1 = not bound,
# any other rc = read/tool error = STOP (never "not bound").
b3_assert_manifest_binding() {
    local manifest="$1" release_sha="$2" manifest_sha="$3" kind rc=0
    kind="$(rp0_probe_path "$manifest")" || exit 3
    [ "$kind" = "regular" ] || b3_fail "install manifest kind=$kind path=$manifest"
    LC_ALL=C grep -qsF -- "\"release_sha\": \"$release_sha\"" "$manifest" || rc=$?
    case "$rc" in
        0) : ;;
        1) b3_fail "install manifest does not bind release_sha" ;;
        *) b3_stop "install_manifest_unreadable path=$manifest grep_rc=$rc" ;;
    esac
    rc=0
    LC_ALL=C grep -qsF -- "\"release_manifest_sha256\": \"$manifest_sha\"" "$manifest" || rc=$?
    case "$rc" in
        0) : ;;
        1) b3_fail "install manifest does not bind release_manifest_sha256" ;;
        *) b3_stop "install_manifest_unreadable path=$manifest grep_rc=$rc" ;;
    esac
    printf 'B3_manifest_binding path=%s bound=both\n' "$manifest"
}

printf 'B3_SECTION header candidate=%s\n' "$CAND"

printf 'B3_SECTION release_tree\n'
b3_assert_mode_owner "$REL" 0555 root:root
b3_assert_no_writable_paths "$REL"

printf 'B3_SECTION venv_tree\n'
b3_assert_mode_owner "$VENV" 0555 root:root
b3_assert_no_writable_paths "$VENV"

printf 'B3_SECTION ancillary_paths\n'
b3_assert_mode_owner "$STATE_DIR"        0750 mtc-bridge:mtc-bridge
b3_assert_mode_owner "$LOG_DIR"          0750 mtc-bridge:mtc-bridge
b3_assert_mode_owner "$CONF_DIR"         0750 root:root
b3_assert_mode_owner "$ENV_FILE"         0600 root:root
b3_assert_mode_owner "$INSTALL_MANIFEST" 0640 root:root
b3_assert_mode_owner "$UNIT_FILE"        0644 root:root

printf 'B3_SECTION manifest_binding\n'
b3_assert_manifest_binding "$INSTALL_MANIFEST" "$CAND" "$B3_RELEASE_MANIFEST_SHA256"

printf 'B3_SECTION done\n'
printf 'B3 PASS\n'
