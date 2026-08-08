#!/usr/bin/env bash
# Gate A - A-7 read-only status / persisted-state / log evidence (run-kit D, 2026-08-08)
# Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b (credential-free DISARMED)
#
# AUTHORIZED ONLY FOR THE OWNER-APPROVED PREREGISTERED GATE A RERUN on gatea-staging.
# Read-only: asserts /api/status is exact credential-free DISARMED and that the reported
# state equals the persisted DB app_state; records the documented log files as regular and
# nonempty with size/mode/owner/group/SHA-256; records a bounded journal line count + tail
# with NO credential grep. /api/health is NOT probed (route absent). reconcile_ready is NOT
# required true (a credential-free service correctly reports it false).
#
# This script does NOT POST /api/arm and does NOT read /etc/mtc-bridge/mtc-bridge.env.
# It writes only the evidence log under /home/gatea and performs no service mutation.
# Hard exclusions: no credential value, broker/exchange access, successful ARM, order,
# TESTNET/mainnet, wallet, master merge, or economic action. First genuine FAIL stops.
set -Eeuo pipefail

UNIT="mtc-bridge-first-start.service"
PY="/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b/bin/python"
DB="/var/lib/mtc-bridge/bridge.db"
LOGDIR="/var/log/mtc-bridge"
LOG="/home/gatea/gatea-A7-20260808D.log"

if [[ -e "$LOG" ]]; then
    printf 'ERROR: evidence log already exists (%s); refusing to overwrite\n' "$LOG" >&2
    exit 2
fi

exec > "$LOG" 2>&1

finish() {
    local rc=$?
    printf '\nA7_TRAP_EXIT rc=%s\n' "$rc"
}
trap finish EXIT

fail() {
    printf 'A7_FAIL reason=%s\n' "$*"
    exit 1
}

echo "A7_SECTION header"
echo "A7_unit=$UNIT"
echo "A7_candidate=2ce41e34bceb599d80af24c5c33d835820ec321b"
echo "A7_db=$DB"
echo "A7_logdir=$LOGDIR"
echo "A7_py=$PY"
echo "A7_note=no POST /api/arm; env file contents not read; no /api/health probe; reconcile_ready NOT required true"

getprop() { systemctl show -p "$1" --value "$UNIT" 2>/dev/null || true; }

# ---- step 1: /api/status exact credential-free DISARMED ------------------------
echo "A7_SECTION step1_api"
api_out=$("$PY" - <<'PYEOF'
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
print("api_reconcile_ready=%s" % j.get("reconcile_ready"))
print("api_reconcile_error=%s" % j.get("reconcile_error"))
ok = (code == 200
      and j.get("state") == "DISARMED"
      and j.get("mode") == "credential_free_disarmed"
      and j.get("state_version") == 1
      and off(j.get("network")) and off(j.get("exchange_conn")) and off(j.get("credential_lookup"))
      and off(j.get("exchange_enabled")) and off(j.get("arm_enabled")))
print("RESULT=%s" % ("PASS" if ok else "FAIL"))
if not ok:
    sys.exit(1)
PYEOF
) || fail "/api/status not credential-free DISARMED"
printf '%s\n' "$api_out"
api_state=$(printf '%s\n' "$api_out" | sed -n 's/^api_state=//p')
[[ -n "$api_state" ]] || fail "could not parse api_state"

# ---- step 2: persisted DB state must equal API state ---------------------------
echo "A7_SECTION step2_db"
db_out=$(sudo "$PY" - "$DB" <<'PYEOF'
import sqlite3, sys
db = sys.argv[1]
con = sqlite3.connect("file:%s?mode=ro" % db, uri=True)
qc = con.execute("PRAGMA quick_check").fetchall()[0][0]
meta = dict(con.execute("SELECT key, value FROM meta").fetchall())
con.close()
print("db_quick_check=%s" % qc)
print("db_app_state=%s" % meta.get("app_state"))
print("db_schema_version=%s" % meta.get("schema_version"))
PYEOF
) || fail "DB read failed"
printf '%s\n' "$db_out"
db_qc=$(printf '%s\n' "$db_out" | sed -n 's/^db_quick_check=//p')
db_app=$(printf '%s\n' "$db_out" | sed -n 's/^db_app_state=//p')
db_schema=$(printf '%s\n' "$db_out" | sed -n 's/^db_schema_version=//p')
[[ "$db_qc" == "ok" ]] || fail "DB quick_check not ok ($db_qc)"
[[ "$db_schema" == "4" ]] || fail "DB schema_version not 4 ($db_schema)"
[[ -n "$db_app" ]] || fail "DB app_state empty"
echo "A7_state_consistency=api_state=${api_state} db_app_state=${db_app}"
[[ "$db_app" == "DISARMED" ]] || fail "DB app_state not DISARMED ($db_app)"
# Explicit cross-source equality: after separately validating the API state and the DB
# app_state above, assert and record that the persisted DB app_state equals the API state
# (an explicit equality check, not merely the logically-equivalent two DISARMED checks).
# On mismatch exit nonzero. All existing checks above are preserved.
echo "A7_db_app_eq_api_state=${db_app}==${api_state}"
[[ "$db_app" == "$api_state" ]] || fail "DB app_state != api_state (${db_app} != ${api_state})"

# ---- step 3: documented log files regular and nonempty ------------------------
echo "A7_SECTION step3_logs"
for f in bridge.log bridge.err.log; do
    p="$LOGDIR/$f"
    if sudo test -f "$p"; then :; else fail "$p not a regular file"; fi
    meta=$(sudo stat -c '%s %a %U %G' "$p")
    bytes=$(printf '%s' "$meta" | awk '{print $1}')
    [[ "$bytes" =~ ^[0-9]+$ && "$bytes" -gt 0 ]] || fail "$p empty or size unreadable ($meta)"
    sum=$(sudo sha256sum "$p" | awk '{print $1}')
    echo "A7_log name=$f bytes=$bytes mode=$(printf '%s' "$meta" | awk '{print $2}') owner=$(printf '%s' "$meta" | awk '{print $3}') group=$(printf '%s' "$meta" | awk '{print $4}') sha256=$sum"
done

# ---- step 4: journal query succeeds; bounded line count + tail (no cred grep) ---
echo "A7_SECTION step4_journal"
jout=$(sudo journalctl -u "$UNIT" --no-pager -n 200 2>&1) || fail "journalctl query failed (rc=$?)"
jcount=$(printf '%s\n' "$jout" | wc -l)
echo "A7_journal_tail_lines=$jcount"
echo "A7_journal_tail_begin"
printf '%s\n' "$jout"
echo "A7_journal_tail_end"
echo "A7_journal_credgrep=not performed (forbidden by contract)"

echo "A7_SECTION done"
echo "A-7 PASS"
