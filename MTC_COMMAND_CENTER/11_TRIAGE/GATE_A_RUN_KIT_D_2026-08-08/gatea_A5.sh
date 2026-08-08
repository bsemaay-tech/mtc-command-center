#!/usr/bin/env bash
# Gate A - A-5 unclean SIGKILL / manual-restart consistency (run-kit D, 2026-08-08)
# Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b (credential-free DISARMED)
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
LOG="/home/gatea/gatea-A5-20260808D.log"

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
echo "A5_note=no POST /api/arm; env file contents not read"
echo "A5_action_authority=runbook-authorized SIGKILL of main + one explicit start (Restart=no)"

getprop() { systemctl show -p "$1" --value "$UNIT" 2>/dev/null || true; }

retry() {
    # retry <max_seconds> <fn_name> [args...]
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
if ! retry 30 wait_active "service active again"; then fail "timeout: service did not return to active"; fi

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
