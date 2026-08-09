#!/usr/bin/env bash
# Gate A - A-5 unclean SIGKILL / manual-restart consistency (run-kit E, 2026-08-09)
# Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b (credential-free DISARMED)
#
# REVISION E - A-5-ONLY REPAIR KIT. Supersedes run-kit D for the A-5 rerun ONLY.
# A-6..A-9 remain NOT RUN and remain governed by the already-accepted run-kit D source
# (MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RUN_KIT_D_2026-08-08/) until A-5 PASSES and
# _AI_MEMORY is updated. The frozen run-kit D and its evidence are preserved unchanged;
# /home/gatea/gatea-A5-20260808D.log is NEVER overwritten or reused.
#
# This file is a copy of the frozen run-kit D gatea_A5.sh and differs ONLY in:
#   (1) revision / date / header / path wording for E;
#   (2) the new no-clobber evidence log /home/gatea/gatea-A5-20260809E.log;
#   (3) the post-start application-readiness repair - the readiness deadline constants,
#       mono_now_ds(), run_bounded(), ready_probe_once(), wait_ready_deadline(), the
#       export -f transport line, the step1 deadline-guard preconditions, and the single
#       structured readiness marker;
#   (4) one comment-only truthfulness fix on the D retry() helper (it is attempt-count
#       bounded, not second bounded) - its behaviour is byte-for-byte unchanged.
# No D assertion, dead-window proof, DB/API/listener condition, hard exclusion, fail
# behaviour, no-clobber behaviour, authorized SIGKILL, Restart=no requirement, or
# exactly-one-explicit-start contract is weakened or removed.
#
# REPAIR ROUND 1 (2026-08-09) - THE CORRECTED TIMING CONTRACT.
# The first E draft used `retry 30 post_start_ready` and described that as a hard 30 s
# ceiling. It was not one. `retry` counts ATTEMPTS, not seconds: check_api's
# urllib.request.urlopen(..., timeout=10) can block for ten seconds inside a single
# attempt and `retry` then sleeps one more second, so a listener-present / API-stalled
# service could keep that wait running for roughly 330 seconds while the readiness marker
# still declared a 30 s ceiling. That claim was false; it and every wording of it have
# been removed from this script, and the regression test fails the script if one returns.
# The wait below is a REAL MONOTONIC WALL-CLOCK DEADLINE: probe duration (active +
# listener + API) and the backoff between attempts are all charged against one 30 s
# budget read from a monotonic clock, and every attempt runs under a hard guard bounded
# by the REMAINING budget, so a blocked probe cannot extend it. wait_ready_deadline()
# states the exact contract and its honest, bounded termination tolerance.
#
# REPAIR ROUND 3 (2026-08-09, FINAL) - THE DEADLINE BOUNDARY ON THE SUCCESS PATH.
# Round 1 checked the deadline before every attempt and before every backoff sleep, but the
# SUCCESSFUL-probe branch of wait_ready_deadline() took its post-probe monotonic reading,
# recorded the elapsed time, and returned 0 WITHOUT comparing that reading to the deadline.
# A probe that reported success only after the deadline had already passed was therefore
# accepted as readiness, so the script could emit the positive readiness marker with an
# elapsed time larger than its own hard bound - contradicting the preregistered contract. There
# is still exactly ONE line in this script that prints that marker. The Lead reproduced the
# exact committed function with a one-second budget and the monotonic sequence 0, 0, 11:
# result SUCCESS, elapsed 11 deciseconds, rc 0. That finding is accepted without qualification.
# The success branch now re-checks the deadline with the SAME rule the other two guards use -
# see THE EQUALITY BOUNDARY in wait_ready_deadline() - and returns failure if the post-probe
# reading is at or past the deadline. Nothing else changed: the bounded termination guarantee,
# the exactly-one-explicit-start contract, the three-condition readiness definition, the final
# full unsuppressed checks and the no-clobber behaviour are all exactly as round 1 left them.
#
# AUTHORIZED ONLY FOR THE OWNER-APPROVED PREREGISTERED GATE A RERUN on gatea-staging.
# Proves: with Restart=no, SIGKILL of the main process does NOT auto-restart; after one
# explicit start the service returns to the identical credential-free DISARMED state and
# the persisted store is byte-for-byte logically unchanged.
#
# This script does NOT POST /api/arm and does NOT read /etc/mtc-bridge/mtc-bridge.env.
# Hard exclusions: no credential value, broker/exchange access, successful ARM, order,
# TESTNET/mainnet, wallet, master merge, or economic action.
# First genuine FAIL stops; on failure NO auto-restart/mask - the Lead handles the safe
# first-FAIL response.
set -Eeuo pipefail

UNIT="mtc-bridge-first-start.service"
PY="/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b/bin/python"
DB="/var/lib/mtc-bridge/bridge.db"
LOG="/home/gatea/gatea-A5-20260809E.log"

# --- E READINESS DEADLINE CONSTANTS (BEGIN; extracted verbatim by test_gatea_A5_readiness.py) ---
# READY_MAX_S is a WALL-CLOCK budget, not an attempt count.
READY_MAX_S=30
# Backoff between readiness attempts. wait_ready_deadline() never sleeps past the deadline.
READY_POLL_S=1
# Bounded SIGTERM -> SIGKILL escalation for a probe that ignores SIGTERM. This is the only
# way the readiness operation can outlive READY_MAX_S, and by at most this many seconds.
KILL_GRACE_S=2
# GNU coreutils deadline guard. Presence AND real behaviour are validated in step1 before
# anything depends on it; an absent or non-functional guard is a precondition FAIL, never a
# silent fall back to an unbounded probe.
TIMEOUT_BIN="$(command -v timeout || true)"
# /proc/uptime is Linux CLOCK_BOOTTIME: it never steps backwards and never jumps when NTP or
# an operator moves the wall clock, which $SECONDS and `date +%s` both do. step1 REQUIRES it
# on the run target; the $SECONDS fallback exists only so the local regression harness can
# exercise this identical deadline arithmetic on a host without /proc/uptime.
MONO_CLOCK=bash_seconds
if [[ -r /proc/uptime ]]; then MONO_CLOCK=proc_uptime; fi
# --- E READINESS DEADLINE CONSTANTS (END) ---

# Set by wait_ready_deadline() for the readiness marker / failure reason.
READY_ATTEMPTS=0
READY_ELAPSED_DS=0

# --- refuse to overwrite an existing evidence log (no clobber) -------------------
if [[ -e "$LOG" ]]; then
    printf 'ERROR: evidence log already exists (%s); refusing to overwrite\n' "$LOG" >&2
    exit 2
fi

# --- redirect all stdout+stderr to the evidence log ------------------------------
exec > "$LOG" 2>&1

finish() {
    local rc=$?
    printf '\nA5_TRAP_EXIT rc=%s\n' "$rc"
}
trap finish EXIT

fail() {
    printf 'A5_FAIL reason=%s\n' "$*"
    exit 1
}

echo "A5_SECTION header"
echo "A5_unit=$UNIT"
echo "A5_candidate=2ce41e34bceb599d80af24c5c33d835820ec321b"
echo "A5_db=$DB"
echo "A5_py=$PY"
echo "A5_kit_revision=E"
echo "A5_kit_repair_round=3"
echo "A5_readiness=monotonic_wall_clock_deadline ready_deadline_s=$READY_MAX_S ready_poll_s=$READY_POLL_S ready_kill_grace_s=$KILL_GRACE_S"
echo "A5_supersedes=run-kit D for the A-5 rerun only; A-6..A-9 remain NOT RUN under run-kit D"
echo "A5_note=no POST /api/arm; env file contents not read"
echo "A5_action_authority=runbook-authorized SIGKILL of main + one explicit start (Restart=no)"

getprop() { systemctl show -p "$1" --value "$UNIT" 2>/dev/null || true; }

retry() {
    # retry <max_attempts> <fn_name> [args...]
    # ATTEMPT-COUNT bounded (this is NOT a seconds bound - each attempt costs whatever the
    # probe costs, plus the 1 s sleep after a failure). Preserved verbatim from run-kit D and
    # used ONLY for the cheap systemd-property dead-window wait in step3, whose probe is a
    # single `systemctl show` and a /proc test. The post-start application-readiness wait,
    # which calls the heavyweight listener/API probes, uses wait_ready_deadline() instead -
    # see REPAIR ROUND 1 in the header.
    local tries="$1" fn="$2"; shift 2
    local i=0
    while (( i < tries )); do
        if "$fn" "$@"; then return 0; fi
        i=$((i+1)); sleep 1
    done
    return 1
}

# GET /api/status, assert exact credential-free DISARMED, print key=value evidence
check_api() {
    "$PY" - <<'PYEOF'
import json, sys, urllib.request
try:
    with urllib.request.urlopen("http://127.0.0.1:8790/api/status", timeout=10) as r:
        body = r.read().decode(); code = r.status
    j = json.loads(body)
except Exception as e:
    print("RESULT=FAIL api_read_error: %r" % (e,)); sys.exit(1)
def off(v):
    if v is False: return True
    return isinstance(v, str) and v.strip().lower() in ("false", "0", "no", "disabled", "none", "off", "null", "")
print("api_http_status=%s" % code)
print("api_state=%s" % j.get("state"))
print("api_mode=%s" % j.get("mode"))
print("api_state_version=%s" % j.get("state_version"))
print("api_network=%s" % j.get("network"))
print("api_exchange_conn=%s" % j.get("exchange_conn"))
print("api_credential_lookup=%s" % j.get("credential_lookup"))
print("api_exchange_enabled=%s" % j.get("exchange_enabled"))
print("api_arm_enabled=%s" % j.get("arm_enabled"))
ok = (code == 200
      and j.get("state") == "DISARMED"
      and j.get("mode") == "credential_free_disarmed"
      and j.get("state_version") == 1
      and off(j.get("network"))
      and off(j.get("exchange_conn"))
      and off(j.get("credential_lookup"))
      and off(j.get("exchange_enabled"))
      and off(j.get("arm_enabled")))
print("RESULT=%s" % ("PASS" if ok else "FAIL"))
if not ok:
    sys.exit(1)
PYEOF
}

# require :8790 listener set nonempty AND every local address is loopback
check_listener_loopback_only() {
    "$PY" - <<'PYEOF'
import subprocess, sys
out = subprocess.run(["ss", "-H", "-ltn", "sport = :8790"], capture_output=True, text=True)
print("ss_rc=%s" % out.returncode)
if out.returncode != 0:
    print("RESULT=FAIL ss_nonzero"); sys.exit(1)
# `ss -H -ltn` columns: [0]=state [1]=Recv-Q [2]=Send-Q [3]=LOCAL addr:port
# [4]=PEER addr:port. We collect the LOCAL column at index 3. Index 4 (peer) is
# the listener's peer, which is always *:* for a listener — appending p[4] is
# FORBIDDEN (it repeats the A-4 peer-column false negative: counts *:* not the
# real binding). Require >= 5 fields so the LOCAL column is present.
addrs = []
for line in out.stdout.splitlines():
    p = line.split()
    if len(p) >= 5:
        addrs.append(p[3])
print("listener_count=%d" % len(addrs))
def is_loopback(a):
    host = a.rsplit(":", 1)[0].strip("[]")
    return host == "::1" or host == "127.0.0.1" or host.startswith("127.")
bad = [a for a in addrs if not is_loopback(a)]
print("nonloopback_addrs=%s" % (",".join(bad) if bad else ""))
ok = len(addrs) > 0 and len(bad) == 0
print("RESULT=%s" % ("PASS" if ok else "FAIL"))
if not ok:
    sys.exit(1)
PYEOF
}

# read-only logical DB snapshot: quick_check, meta, sorted per-table counts
db_snapshot() {
    sudo "$PY" - "$DB" <<'PYEOF'
import sqlite3, sys
db = sys.argv[1]
con = sqlite3.connect("file:%s?mode=ro" % db, uri=True)
qc = con.execute("PRAGMA quick_check").fetchall()[0][0]
print("db_quick_check=%s" % qc)
meta = dict(con.execute("SELECT key, value FROM meta").fetchall())
app_state = meta.get("app_state"); schema = meta.get("schema_version")
print("db_app_state=%s" % app_state)
print("db_schema_version=%s" % schema)
tables = [r[0] for r in con.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name").fetchall()]
for t in tables:
    n = con.execute('SELECT COUNT(*) FROM "%s"' % t.replace('"', '""')).fetchone()[0]
    print("db_table_%s=%s" % (t, n))
con.close()
if qc != "ok":
    sys.exit(2)
if app_state != "DISARMED" or str(schema) != "4":
    sys.exit(3)
PYEOF
}

wait_dead() {
    local mp; mp=$(getprop MainPID || true)
    [[ "$mp" == "0" ]] || return 1
    [[ ! -e "/proc/$oldpid" ]] || return 1
    return 0
}

no_listener() {
    local c; c=$(ss -H -ltn 'sport = :8790' 2>/dev/null | wc -l)
    [[ "$c" == "0" ]]
}

wait_active() {
    local a; a=$(getprop ActiveState || true)
    [[ "$a" == "active" ]]
}

# --- REVISION E REPAIR: post-start application-readiness proof --------------------
# Run-kit D gated the post-start assertions on systemd ActiveState=active ALONE, so the
# post listener assertion could fire before the application had bound :8790. That is the
# reproduced 2026-08-09 A-5 FAIL (`listener_count=0` -> `A5_FAIL reason=post listener not
# loopback-only`, trap rc=1) on a service that was in fact healthy moments later.
#
# Readiness here is true ONLY when ALL THREE hold in the SAME attempt:
#   1. systemd ActiveState=active                      -> wait_active
#   2. nonempty loopback-only :8790 listener set       -> check_listener_loopback_only
#   3. GET /api/status HTTP 200 + exact credential-free DISARMED -> check_api
# ActiveState=active alone can NEVER satisfy this wait: ready_probe_once() returns nonzero
# on the first of the three checks that fails, so every attempt must satisfy all three.
#
# Per-attempt stdout/stderr from the two heavyweight checks is suppressed so the evidence
# log is not filled with expected not-ready noise. This is diagnostics suppression ONLY --
# the step5 assertions below still re-run BOTH check_listener_loopback_only and check_api
# in full, unsuppressed, and they remain the authoritative post evidence. The final
# check_api deliberately keeps its own urllib timeout=10; only the READINESS path is
# bounded by the remaining deadline.

# Monotonic "now" in tenths of a second. See MONO_CLOCK in the constants block for why
# /proc/uptime is required on the run target and what the fallback is for.
mono_now_ds() {
    local up rest
    if [[ "$MONO_CLOCK" == "proc_uptime" ]] && read -r up rest < /proc/uptime \
       && [[ "$up" =~ ^([0-9]+)\.([0-9]) ]]; then
        printf '%s\n' "$(( ${BASH_REMATCH[1]} * 10 + ${BASH_REMATCH[2]} ))"
        return 0
    fi
    printf '%s\n' "$(( SECONDS * 10 ))"
}

# run_bounded <bound_deciseconds> <fn>
# Runs <fn> as a child under the GNU coreutils deadline guard. Without --foreground,
# `timeout` puts the child in its OWN PROCESS GROUP and signals the whole group, so SIGTERM
# at the bound - and SIGKILL $KILL_GRACE_S later if the probe ignores SIGTERM - reaches the
# probe shell AND every descendant it spawned (the venv python, its `ss` subprocess, a
# stalled socket read). No probe child can outlive the bound. rc 124 = the bound expired.
# The child is a fresh shell, so the readiness functions and the two variables they read are
# carried across by `export -f` / `export` below; step1 proves that transport works before
# anything depends on it.
run_bounded() {
    local bound_ds="$1" fn="$2"
    "$TIMEOUT_BIN" --signal=TERM --kill-after="$KILL_GRACE_S" \
        "$(( bound_ds / 10 )).$(( bound_ds % 10 ))" \
        "${BASH:-bash}" -c "$fn"
}

# One readiness attempt: all three conditions, in this order, short-circuiting on the first
# failure. Identical in shape to the D-era check composition; only the transport changed.
ready_probe_once() {
    wait_active || return 1
    check_listener_loopback_only >/dev/null 2>&1 || return 1
    check_api >/dev/null 2>&1 || return 1
    return 0
}

# wait_ready_deadline <max_seconds>
# A REAL MONOTONIC WALL-CLOCK DEADLINE, not an attempt count. The deadline is fixed once,
# from mono_now_ds(), at the first line of this function - which is called immediately after
# the single explicit `systemctl start`. Everything the readiness operation does is charged
# against that one budget:
#   * each attempt is run through run_bounded with the REMAINING budget as its hard bound,
#     so a stalled active/listener/API probe is terminated at the deadline instead of
#     extending it (this is the repair-round-1 defect);
#   * the backoff after a failed attempt is clamped to the remaining budget, so it can never
#     sleep past the deadline;
#   * the deadline is re-checked before every attempt, AFTER a SUCCESSFUL attempt, and before
#     every sleep, and the loop returns nonzero the moment the remaining budget reaches zero.
# THE EQUALITY BOUNDARY (repair round 3), stated once and applied identically at all three
# guards: a monotonic reading `now` has EXPIRED the deadline when `now >= deadline`, i.e. when
# `deadline - now <= 0`. Equality is expiry. All three guards use the same predicate form -
# `(( rem_ds <= 0 ))` on a freshly computed `rem_ds=$(( deadline - now ))` - so the
# same reading can never count as expired at one guard and in time at another. Readiness is
# therefore only ever emitted for a post-probe reading STRICTLY BEFORE the deadline.
# HONEST BOUND: the readiness operation returns at <max_seconds> of monotonic time, plus at
# most KILL_GRACE_S seconds IF AND ONLY IF a probe ignores SIGTERM and must be SIGKILLed,
# plus ordinary process scheduling slop. That deadline-plus-bounded-termination statement -
# not a bare ceiling claim, and not an attempt count - is what the marker, the failure reason
# and the records all state. It is NOT a claim that a probe may never take longer than one
# second; it is a claim that no probe may push the operation past the deadline.
# Returns 0 on readiness; nonzero on deadline expiry, INCLUDING the case where the probe
# itself succeeded but only after the deadline had passed. Sets READY_ATTEMPTS and
# READY_ELAPSED_DS (tenths of a second) on every path, for the marker / failure reason.
wait_ready_deadline() {
    local max_s="$1"
    local t0 deadline now rem_ds
    t0=$(mono_now_ds)
    deadline=$(( t0 + max_s * 10 ))
    READY_ATTEMPTS=0
    READY_ELAPSED_DS=0
    while :; do
        now=$(mono_now_ds)
        rem_ds=$(( deadline - now ))
        if (( rem_ds <= 0 )); then
            READY_ELAPSED_DS=$(( now - t0 ))
            return 1
        fi
        READY_ATTEMPTS=$(( READY_ATTEMPTS + 1 ))
        if run_bounded "$rem_ds" ready_probe_once; then
            now=$(mono_now_ds)
            READY_ELAPSED_DS=$(( now - t0 ))
            rem_ds=$(( deadline - now ))
            # Repair round 3. A successful probe is NOT readiness unless the post-probe
            # monotonic reading is still strictly before the deadline. Same expiry rule as the
            # two other guards (THE EQUALITY BOUNDARY above): rem_ds <= 0 is expiry. Without
            # this the wait could emit readiness with an elapsed time past its own hard bound.
            if (( rem_ds <= 0 )); then
                return 1
            fi
            return 0
        fi
        now=$(mono_now_ds)
        rem_ds=$(( deadline - now ))
        if (( rem_ds <= 0 )); then
            READY_ELAPSED_DS=$(( now - t0 ))
            return 1
        fi
        if (( rem_ds >= READY_POLL_S * 10 )); then
            sleep "$READY_POLL_S"
        else
            sleep "$(( rem_ds / 10 )).$(( rem_ds % 10 ))"
        fi
    done
}

# The bounded attempt runs in a child shell, so the readiness functions and the two
# variables they read must cross the process boundary. Validated in step1
# (A5_ready_probe_export_rc) before the run depends on it.
export PY UNIT
export -f getprop wait_active check_listener_loopback_only check_api ready_probe_once

# ============================================================================
echo "A5_SECTION step1_preconditions"

act=$(getprop ActiveState); echo "A5_pre_active=$act"
[[ "$act" == "active" ]] || fail "precondition ActiveState=active (got $act)"

restart=$(getprop Restart); echo "A5_pre_restart=$restart"
[[ "$restart" == "no" ]] || fail "precondition Restart=no (got $restart)"

oldpid=$(getprop MainPID); echo "A5_pre_mainpid=$oldpid"
[[ "$oldpid" =~ ^[0-9]+$ ]] || fail "precondition MainPID numeric ($oldpid)"
(( oldpid > 0 )) || fail "precondition MainPID>0 ($oldpid)"

nr0=$(getprop NRestarts); echo "A5_pre_nrestarts=$nr0"
[[ "$nr0" =~ ^[0-9]+$ ]] || fail "precondition NRestarts numeric ($nr0)"

# --- readiness-deadline preconditions (revision E) --------------------------------
# The deadline is only real if the clock is monotonic, the guard exists, the guard really
# terminates a blocked child, and the readiness functions survive the process boundary. All
# four are ASSERTED here rather than assumed. Each is cheap and local, and none of them
# touches the unit, the DB, the API or any service state.
echo "A5_ready_clock=$MONO_CLOCK"
[[ "$MONO_CLOCK" == "proc_uptime" ]] || fail "precondition monotonic clock /proc/uptime unreadable (got $MONO_CLOCK); the readiness deadline would not be monotonic"
echo "A5_ready_mono_now_ds=$(mono_now_ds)"

echo "A5_timeout_bin=$TIMEOUT_BIN"
[[ -n "$TIMEOUT_BIN" ]] || fail "precondition GNU coreutils timeout (readiness deadline guard) not found on PATH"

gk=0; "$TIMEOUT_BIN" --signal=TERM --kill-after="$KILL_GRACE_S" 0.5 "${BASH:-bash}" -c 'sleep 30' || gk=$?
echo "A5_timeout_guard_rc=$gk"
[[ "$gk" == "124" ]] || fail "precondition deadline guard did not terminate a blocked child (rc $gk, expected 124)"

tp=0; "$TIMEOUT_BIN" --signal=TERM --kill-after="$KILL_GRACE_S" 5 "${BASH:-bash}" -c 'declare -F ready_probe_once wait_active check_listener_loopback_only check_api >/dev/null' || tp=$?
echo "A5_ready_probe_export_rc=$tp"
[[ "$tp" == "0" ]] || fail "precondition readiness probe functions not visible in the bounded child shell (rc $tp; export -f transport failed)"

echo "A5_pre_listener:"
if ! check_listener_loopback_only; then fail "precondition listener not loopback-only"; fi

echo "A5_pre_api:"
if ! check_api; then fail "precondition API not credential-free DISARMED"; fi

echo "A5_pre_dbsnap:"
if ! pre_snap=$(db_snapshot); then fail "precondition DB snapshot failed"; fi
printf '%s\n' "$pre_snap"

echo "A5_SECTION step2_sigkill"
echo "A5_action=sudo systemctl kill --kill-whom=main --signal=SIGKILL $UNIT"
sudo systemctl kill --kill-whom=main --signal=SIGKILL "$UNIT"

echo "A5_SECTION step3_wait_dead"
if ! retry 30 wait_dead "main process dead / MainPID=0"; then fail "timeout: process did not die / MainPID!=0"; fi
echo "A5_dead_mainpid=$(getprop MainPID)"
echo "A5_proc_oldpid_exists=$([[ -e /proc/$oldpid ]] && echo yes || echo no)"
sleep 3
echo "A5_post_3s_sleep=done"

act2=$(getprop ActiveState); echo "A5_dead_active=$act2"
[[ "$act2" == "failed" || "$act2" == "inactive" ]] || fail "post-kill ActiveState not failed/inactive ($act2)"

echo "A5_dead_listener:"
if ! no_listener; then fail "post-kill :8790 listener still present (auto-restart suspected)"; fi

nr1=$(getprop NRestarts); echo "A5_dead_nrestarts=$nr1"
[[ "$nr1" == "$nr0" ]] || fail "NRestarts changed after kill ($nr0 -> $nr1)"

res=$(getprop Result); exs=$(getprop ExecMainStatus)
echo "A5_dead_result=$res"; echo "A5_dead_execmainstatus=$exs"
[[ "$res" == "signal" ]] || fail "Result not signal ($res)"
[[ "$exs" == "9" ]] || fail "ExecMainStatus not 9 ($exs)"

echo "A5_SECTION step4_reset_start"
echo "A5_action=sudo systemctl reset-failed $UNIT"
sudo systemctl reset-failed "$UNIT"
echo "A5_action=sudo systemctl start $UNIT"
sudo systemctl start "$UNIT"
if ! wait_ready_deadline "$READY_MAX_S"; then fail "deadline: service did not become application-ready within the ${READY_MAX_S}s monotonic wall-clock deadline measured from the single explicit start (requires ActiveState=active AND nonempty loopback-only :8790 listener AND exact credential-free DISARMED /api/status in the SAME attempt; every attempt ran under a hard guard bounded by the remaining deadline, SIGTERM then SIGKILL after ${KILL_GRACE_S}s, so a blocked probe could not extend it); attempts=$READY_ATTEMPTS elapsed_s=$(( READY_ELAPSED_DS / 10 )).$(( READY_ELAPSED_DS % 10 )); no second start performed"; fi
echo "A5_READY=yes ready_requires=active+loopback_only_listener_nonempty+exact_credential_free_disarmed_api ready_bound=monotonic_wall_clock_deadline ready_deadline_s=$READY_MAX_S ready_clock=$MONO_CLOCK ready_probe_guard=timeout_TERM_then_KILL ready_kill_grace_s=$KILL_GRACE_S ready_elapsed_s=$(( READY_ELAPSED_DS / 10 )).$(( READY_ELAPSED_DS % 10 )) ready_attempts=$READY_ATTEMPTS ready_second_start=none"

echo "A5_SECTION step5_post_assert"
newpid=$(getprop MainPID); echo "A5_post_mainpid=$newpid"
[[ "$newpid" =~ ^[0-9]+$ ]] || fail "post MainPID numeric ($newpid)"
(( newpid > 0 )) || fail "post MainPID>0 ($newpid)"
[[ "$newpid" != "$oldpid" ]] || fail "post MainPID equals pre PID (no new process started)"

nr2=$(getprop NRestarts); echo "A5_post_nrestarts=$nr2"
[[ "$nr2" == "$nr0" ]] || fail "NRestarts changed across restart ($nr0 -> $nr2)"

restart2=$(getprop Restart); echo "A5_post_restart=$restart2"
[[ "$restart2" == "no" ]] || fail "post Restart!=no ($restart2)"

echo "A5_post_listener:"
if ! check_listener_loopback_only; then fail "post listener not loopback-only"; fi

echo "A5_post_api:"
if ! check_api; then fail "post API not credential-free DISARMED"; fi

echo "A5_post_dbsnap:"
if ! post_snap=$(db_snapshot); then fail "post DB snapshot failed"; fi
printf '%s\n' "$post_snap"

if [[ "$pre_snap" == "$post_snap" ]]; then
    echo "A5_dbsnap_identical=yes"
else
    echo "A5_dbsnap_identical=no"
    fail "logical DB snapshot changed across kill/restart"
fi

echo "A5_SECTION done"
echo "A-5 PASS"
