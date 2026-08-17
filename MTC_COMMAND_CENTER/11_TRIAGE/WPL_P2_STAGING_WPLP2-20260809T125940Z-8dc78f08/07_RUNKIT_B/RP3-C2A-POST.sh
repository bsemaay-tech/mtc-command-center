# ===== BLOCK-ID: RP3-C2A-POST ===== [EXECUTABLE PROPOSAL BLOCK]
# WP-L Phase 2 — C2 Scenario A post-reboot assertion (PROPOSED DESIGN).
# Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b. NOT host-authorized.
# Read-only: no service mutation, no reboot, no start, no unmask, no credential
# read, no POST /api/arm. Requires RP0-LIB and RP0-BOOTSTRAP. The scenario is
# preregistered; this block NEVER selects a branch from what it observes.
set -Eeuo pipefail

UNIT="mtc-bridge-first-start.service"
FRAGMENT="/usr/local/lib/systemd/system/$UNIT"
MASK_PATH="/etc/systemd/system/$UNIT"
PORT="8790"

: "${C2_SCENARIO:?preregistered scenario identifier is required}"
: "${C2_BASELINE_INVARIANTS_SHA256:?preregistered pre-reboot protected-invariant hash is required}"
: "${C2_BASELINE_INVARIANTS_JSON:?preregistered pre-reboot protected-invariant document is required}"
: "${C2_POST_INVARIANTS_SHA256:?post-reboot invariant hash, produced by the accepted quiescent capture, is required}"
: "${C2_POST_INVARIANTS_JSON:?post-reboot protected-invariant document is required}"
: "${PY:?candidate venv interpreter path is required}"

c2a_stop() { printf 'C2A_STOP reason=%s\n' "$*"; exit 3; }
c2a_fail() { printf 'C2A_FAIL reason=%s\n' "$*"; exit 1; }

[ "$C2_SCENARIO" = "A_plain_reboot_expect_static_unmasked" ] \
    || c2a_fail "wrong preregistered scenario: $C2_SCENARIO"

# The baseline is an INPUT. Its absence is STOP, never "compare post against post".
for f in "$C2_BASELINE_INVARIANTS_JSON" "$C2_POST_INVARIANTS_JSON"; do
    kind="$(rp0_probe_path "$f")" || exit 3
    [ "$kind" = "regular" ] || c2a_stop "invariant_document_kind=$kind path=$f"
done

printf 'C2A_SECTION step1_active_state\n'
active="$(rp0_show_property "$UNIT" ActiveState)" || exit 3
printf 'C2A_active=%s\n' "$active"
[ "$active" = "inactive" ] || c2a_fail "ActiveState=$active expected inactive (unexpected auto-start)"

printf 'C2A_SECTION step2_enablement_and_mask\n'
enabled="$(rp0_is_enabled_token "$UNIT")" || exit 3
printf 'C2A_is_enabled=%s\n' "$enabled"
[ "$enabled" = "static" ] || c2a_fail "is-enabled=$enabled expected exactly static"

frag_kind="$(rp0_probe_path "$FRAGMENT")" || exit 3
[ "$frag_kind" = "regular" ] || c2a_fail "canonical fragment kind=$frag_kind path=$FRAGMENT"

mask_kind="$(rp0_probe_path "$MASK_PATH")" || exit 3
printf 'C2A_mask_path_kind=%s\n' "$mask_kind"
[ "$mask_kind" = "absent" ] || c2a_fail "mask path must be absent as object AND link, found $mask_kind"

printf 'C2A_SECTION step3_no_writer_no_listener\n'
procs=""; prc=0
procs="$(rp0_pgrep_status 'bridge\.app')" || prc=$?
case "$prc" in
    0) printf 'C2A_dangling_procs_begin\n%s\nC2A_dangling_procs_end\n' "$procs"
       c2a_fail "a bridge.app process is running after reboot with no authorised start" ;;
    1) printf 'C2A_writers=0\n' ;;
    *) exit 3 ;;
esac
listeners="$(rp0_listener_count "$PORT")" || exit 3
printf 'C2A_listener_count=%s\n' "$listeners"
[ "$listeners" -eq 0 ] || c2a_fail "control port $PORT has a listener after reboot"

# A cgroup survivor is a THIRD, independent way the unit can still hold a
# process: it need not match the writer pattern and need not hold the port.
# Omitting this check was the gap; the predicate is fail-closed (STOP on any
# unevaluable property, walk or read).
cgsurv="$(rp0_cgroup_survivors "$UNIT")" || exit 3
printf 'C2A_cgroup_survivors=%s\n' "$cgsurv"
[ "$cgsurv" -eq 0 ] || c2a_fail "the unit cgroup still holds $cgsurv process(es) after reboot"

printf 'C2A_SECTION step4_app_state_not_armed\n'
# ABSOLUTE assertion, not a comment and not implied by equality: equality alone
# would happily accept "ARMED before the reboot and ARMED after it".
app_state=""; asrc=0
app_state="$("$PY" - "$C2_POST_INVARIANTS_JSON" <<'PYEOF'
import json, sys
try:
    with open(sys.argv[1], "r", encoding="utf-8") as handle:
        doc = json.load(handle)
except Exception as exc:
    print(f"app_state_document_unreadable: {exc.__class__.__name__}: {exc}", file=sys.stderr)
    raise SystemExit(3)
if not isinstance(doc, dict) or "app_state" not in doc:
    print("app_state_field_missing", file=sys.stderr)
    raise SystemExit(3)
print("" if doc["app_state"] is None else str(doc["app_state"]))
PYEOF
)" || asrc=$?
[ "$asrc" -eq 0 ] || c2a_stop "app_state_unevaluable path=$C2_POST_INVARIANTS_JSON rc=$asrc"
printf 'C2A_app_state=%s\n' "$app_state"
[ "$app_state" != "ARMED" ] || c2a_fail "app_state=ARMED after reboot; the unit must not return armed"

printf 'C2A_SECTION step5_protected_invariant_equality\n'
# EXACT equality of both the candidate invariants hash and the invariant document.
# Presence, size or "recorded" are NOT this predicate; `app_state != ARMED` is a
# separate REQUIRED assertion (step 4) and never a substitute for equality.
[ "$C2_POST_INVARIANTS_SHA256" = "$C2_BASELINE_INVARIANTS_SHA256" ] \
    || c2a_fail "protected invariants hash differs across reboot (baseline=$C2_BASELINE_INVARIANTS_SHA256 post=$C2_POST_INVARIANTS_SHA256)"
cmp -s -- "$C2_BASELINE_INVARIANTS_JSON" "$C2_POST_INVARIANTS_JSON" \
    || c2a_fail "protected invariant documents differ across reboot"
printf 'C2A_invariants_equal=yes sha256=%s\n' "$C2_POST_INVARIANTS_SHA256"

printf 'C2A_SECTION done\n'
printf 'C2A PASS (terminal branch: no recovery start is authorised by this result)\n'
