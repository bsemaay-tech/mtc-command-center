# ===== BLOCK-ID: RP3-C2B-POST ===== [EXECUTABLE PROPOSAL BLOCK]
# WP-L Phase 2 — C2 Scenario B post-reboot assertion (PROPOSED DESIGN).
# Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b. NOT host-authorized.
# Runs only in the preregistered Scenario B, after C2-B-PRE completed and the
# separately authorized reboot occurred. Read-only; no mutation of any kind.
set -Eeuo pipefail

UNIT="mtc-bridge-first-start.service"
MASK_PATH="/etc/systemd/system/$UNIT"
PORT="8790"

: "${C2_SCENARIO:?preregistered scenario identifier is required}"
: "${C2_QUIESCENT_INVARIANTS_SHA256:?post-stop/pre-reboot quiescent invariant hash is required}"
: "${C2_QUIESCENT_INVARIANTS_JSON:?post-stop/pre-reboot quiescent invariant document is required}"
: "${C2_POST_INVARIANTS_SHA256:?post-reboot invariant hash is required}"
: "${C2_POST_INVARIANTS_JSON:?post-reboot invariant document is required}"

c2b_stop() { printf 'C2B_STOP reason=%s\n' "$*"; exit 3; }
c2b_fail() { printf 'C2B_FAIL reason=%s\n' "$*"; exit 1; }

[ "$C2_SCENARIO" = "B_pre_reboot_stop_mask_expect_masked" ] \
    || c2b_fail "wrong preregistered scenario: $C2_SCENARIO"

for f in "$C2_QUIESCENT_INVARIANTS_JSON" "$C2_POST_INVARIANTS_JSON"; do
    kind="$(rp0_probe_path "$f")" || exit 3
    [ "$kind" = "regular" ] || c2b_stop "invariant_document_kind=$kind path=$f"
done

printf 'C2B_SECTION step1_active_state\n'
active="$(rp0_show_property "$UNIT" ActiveState)" || exit 3
printf 'C2B_active=%s\n' "$active"
[ "$active" = "inactive" ] || c2b_fail "ActiveState=$active expected inactive"

printf 'C2B_SECTION step2_mask_survived_reboot\n'
enabled="$(rp0_is_enabled_token "$UNIT")" || exit 3
printf 'C2B_is_enabled=%s\n' "$enabled"
[ "$enabled" = "masked" ] || c2b_fail "is-enabled=$enabled expected exactly masked"

mask_kind="$(rp0_probe_path "$MASK_PATH")" || exit 3
printf 'C2B_mask_path_kind=%s\n' "$mask_kind"
[ "$mask_kind" = "link_live" ] || c2b_fail "mask path kind=$mask_kind expected a live symlink"
raw_target="$(readlink -- "$MASK_PATH")" || c2b_stop "mask_link_read_failed path=$MASK_PATH"
printf 'C2B_mask_raw_target=%s\n' "$raw_target"
[ "$raw_target" = "/dev/null" ] || c2b_fail "mask link raw target=$raw_target expected exactly /dev/null"

printf 'C2B_SECTION step3_no_writer_no_listener\n'
procs=""; prc=0
procs="$(rp0_pgrep_status 'bridge\.app')" || prc=$?
case "$prc" in
    0) printf 'C2B_dangling_procs_begin\n%s\nC2B_dangling_procs_end\n' "$procs"
       c2b_fail "a bridge.app process is running after a masked reboot" ;;
    1) printf 'C2B_writers=0\n' ;;
    *) exit 3 ;;
esac
listeners="$(rp0_listener_count "$PORT")" || exit 3
printf 'C2B_listener_count=%s\n' "$listeners"
[ "$listeners" -eq 0 ] || c2b_fail "control port $PORT has a listener after a masked reboot"

# Third independent survivor class, fail-closed exactly as in Scenario A. A
# masked unit whose cgroup still holds a process is not a DISARMED host.
cgsurv="$(rp0_cgroup_survivors "$UNIT")" || exit 3
printf 'C2B_cgroup_survivors=%s\n' "$cgsurv"
[ "$cgsurv" -eq 0 ] || c2b_fail "the unit cgroup still holds $cgsurv process(es) after a masked reboot"

printf 'C2B_SECTION step4_protected_invariant_equality\n'
# Comparison basis is the POST-STOP / PRE-REBOOT quiescent baseline, never the pre-stop one.
[ "$C2_POST_INVARIANTS_SHA256" = "$C2_QUIESCENT_INVARIANTS_SHA256" ] \
    || c2b_fail "protected invariants hash differs across reboot (quiescent=$C2_QUIESCENT_INVARIANTS_SHA256 post=$C2_POST_INVARIANTS_SHA256)"
cmp -s -- "$C2_QUIESCENT_INVARIANTS_JSON" "$C2_POST_INVARIANTS_JSON" \
    || c2b_fail "protected invariant documents differ across reboot"
printf 'C2B_invariants_equal=yes sha256=%s\n' "$C2_POST_INVARIANTS_SHA256"

printf 'C2B_SECTION done\n'
printf 'C2B PASS (no start, unmask or recovery action is authorised by this result)\n'
