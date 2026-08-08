#!/usr/bin/env bash
# Gate A - A-6 empty-startup reconcile dry-run (run-kit D, 2026-08-08)
# Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b (credential-free DISARMED)
#
# AUTHORIZED ONLY FOR THE OWNER-APPROVED PREREGISTERED GATE A RERUN on gatea-staging.
# Builds a throwaway in-process app against a TEMP database with an injected MockBroker
# (bars=[]) so no credential resolver and no network/broker/exchange path is exercised.
# Proves empty startup raises nothing, does not hang, and leaves no leftover queued events.
#
# INSTALLED-CANDIDATE GROUNDING (Lead-verified; Lead audit is authoritative):
#   * The ACCEPTED installed candidate at the release path below supports
#     create_app(..., start_mode=None) and the exact create_app(..., start_mode='credentialed')
#     call used here. An older records-branch working tree that appeared to lack the kwarg is
#     NON-authoritative for this gate; the installed candidate wins.
#   * start_mode='credentialed' is passed explicitly. The injected broker=MockBroker(bars=[])
#     prevents _build_broker from running, so there is no credential resolver, no
#     HyperliquidBroker, and no network/broker/exchange path. dry_run=True is honored literally.
#   * The installed candidate's engine.status() exposes the deferred_event_queue_depth key;
#     it is required == 0 AND len(order_manager._queued_events) == 0 (both are checked).
#   * Outbound hardening: before importing bridge.app (and before create_app),
#     HL_ACCOUNT_ADDRESS / HL_API_WALLET_KEY / TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID /
#     MTC_BRIDGE_START_MODE / MTC_BRIDGE_STATE_DB are popped from the isolated process env
#     (os.environ.pop removes and discards the process-local value; no value is printed,
#     copied, persisted, or retained — it is not claimed the values are "never read"; Gate-A
#     preconditions already established the keys absent, so clearing is defense in depth; the
#     env FILE is not opened by A6). The optional Telegram notifier is required absent or
#     disabled (engine.notifier is None or its .enabled is False); that notifier_disabled
#     boolean is printed and bound into the PASS assertion so no unrelated outbound path can
#     be created.
#
# This script does NOT POST /api/arm and does NOT read /etc/mtc-bridge/mtc-bridge.env.
# It writes only under /home/gatea (the evidence log and a temp dir it creates and removes).
# Hard exclusions: no credential value, broker/exchange access, successful ARM, order,
# TESTNET/mainnet, wallet, master merge, or economic action. First genuine FAIL stops.
set -Eeuo pipefail

UNIT="mtc-bridge-first-start.service"
PY="/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b/bin/python"
RELEASE="/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b/IBKR_PAPER_BRIDGE"
LOG="/home/gatea/gatea-A6-20260808D.log"
TMP=""

# --- refuse to overwrite an existing evidence log (no clobber) -------------------
if [[ -e "$LOG" ]]; then
    printf 'ERROR: evidence log already exists (%s); refusing to overwrite\n' "$LOG" >&2
    exit 2
fi

exec > "$LOG" 2>&1

finish() {
    local rc=$?
    if [[ -n "$TMP" ]]; then
        # Safety: never rm -rf. Require the exact mktemp shape (prefix + EXACTLY six
        # alphanumeric chars), a real directory, and NOT a symlink; then delete only
        # maxdepth-1 REGULAR files whose exact basenames are bridge.db / bridge.db-wal /
        # bridge.db-shm (the SQLite main DB plus its WAL/SHM sidecars). Require no entries
        # remain, then rmdir. Any invalid target or leftover residue forces a nonzero exit.
        if [[ "$TMP" =~ ^/home/gatea/gatea-A6-temp[.][A-Za-z0-9]{6}$ && -d "$TMP" && ! -L "$TMP" ]]; then
            local clean_ok=0
            find "$TMP" -maxdepth 1 -type f \( \
                -name bridge.db -o -name bridge.db-wal -o -name bridge.db-shm \) -delete || clean_ok=1
            if [[ -n "$(find "$TMP" -mindepth 1 -maxdepth 1 -print -quit 2>/dev/null)" ]]; then
                echo "A6_temp_cleanup_residue=$TMP"
                clean_ok=1
            fi
            rmdir "$TMP" || clean_ok=1
            if (( clean_ok == 0 )); then
                echo "A6_temp_cleaned=$TMP"
            else
                echo "A6_temp_cleanup_failed=$TMP"
                rc=1
            fi
        else
            echo "A6_temp_cleanup_skipped_invalid=$TMP"
            rc=1
        fi
    fi
    printf '\nA6_TRAP_EXIT rc=%s\n' "$rc"
    exit "$rc"
}
trap finish EXIT

fail() {
    printf 'A6_FAIL reason=%s\n' "$*"
    exit 1
}

echo "A6_SECTION header"
echo "A6_unit=$UNIT"
echo "A6_candidate=2ce41e34bceb599d80af24c5c33d835820ec321b"
echo "A6_release=$RELEASE"
echo "A6_py=$PY"
echo "A6_note=no POST /api/arm; env FILE not opened by A6; injected MockBroker(bars=[]), no network; six env keys popped before import (no value printed/copied/persisted/retained; defense in depth)"
echo "A6_grounding=installed candidate authoritative; create_app(start_mode='credentialed') supported; MockBroker blocks _build_broker/credentials/network; six env keys popped BEFORE importing bridge.app (removes/discards process-local values; no value printed/copied/persisted/retained; defense in depth) + notifier absent/disabled bound into assertion; engine.status()['deferred_event_queue_depth'] required ==0"

getprop() { systemctl show -p "$1" --value "$UNIT" 2>/dev/null || true; }

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
}

# ---- step 1: production service DISARMED before --------------------------------
echo "A6_SECTION step1_pre"
pre_act=$(getprop ActiveState); pre_pid=$(getprop MainPID)
echo "A6_pre_active=$pre_act"; echo "A6_pre_mainpid=$pre_pid"
[[ "$pre_act" == "active" ]] || fail "precondition ActiveState=active (got $pre_act)"
[[ "$pre_pid" =~ ^[0-9]+$ ]] || fail "precondition MainPID numeric ($pre_pid)"
(( pre_pid > 0 )) || fail "precondition MainPID>0 ($pre_pid)"
echo "A6_pre_api:"
if ! check_api; then fail "precondition API not credential-free DISARMED"; fi

# ---- step 2: temp dir + in-process dry run -------------------------------------
echo "A6_SECTION step2_temp"
cd "$RELEASE" || fail "cannot cd to release"
TMP=$(mktemp -d /home/gatea/gatea-A6-temp.XXXXXX) || fail "mktemp failed"
echo "A6_temp=$TMP"

echo "A6_SECTION step3_dryrun"
if ! "$PY" - "$RELEASE" "$TMP" <<'PYEOF'
import asyncio, os, sys
from pathlib import Path
release = Path(sys.argv[1]); tmp = Path(sys.argv[2])
sys.path.insert(0, str(release))

# Outbound hardening: pop the six credential/notifier/start-mode/state-DB keys from this
# isolated process BEFORE importing bridge.app or any module that could construct an app,
# so even module-level default app construction cannot see the parent process values.
# os.environ.pop removes and discards the process-local value; no value is printed, copied,
# persisted, or retained. (It is not claimed the values are "never read"; Gate-A
# preconditions already established the keys absent, so clearing is defense in depth. The
# env FILE is not opened by A6.) Removing the TELEGRAM_* keys keeps the optional notifier
# from arming an outbound path; the explicit kwargs below (start_mode, store_path, broker)
# make create_app independent of any env residue.
for _k in ("HL_ACCOUNT_ADDRESS", "HL_API_WALLET_KEY", "TELEGRAM_BOT_TOKEN",
           "TELEGRAM_CHAT_ID", "MTC_BRIDGE_START_MODE", "MTC_BRIDGE_STATE_DB"):
    os.environ.pop(_k, None)

from bridge.app import create_app
from bridge.broker.mock import MockBroker

store_path = tmp / "bridge.db"
# start_mode='credentialed' is supported by the installed candidate; the injected
# MockBroker(bars=[]) prevents _build_broker, so no credential resolver / network runs.
app = create_app(dry_run=True, store_path=store_path, start_runtime=True,
                 start_mode='credentialed', broker=MockBroker(bars=[]))
engine = app.state.bridge_engine
print("engine_present=%s" % (engine is not None))
if engine is None:
    print("RESULT=FAIL no_engine"); sys.exit(1)

# Notifier/outbound: the optional Telegram notifier must be absent or disabled so it
# cannot create an unrelated outbound path. Print only the boolean; never an env value.
notifier_disabled = engine.notifier is None or engine.notifier.enabled is False
print("notifier_disabled=%s" % ("true" if notifier_disabled else "false"))

async def run():
    # Any timeout, start exception, failed assertion, or stop exception MUST exit nonzero.
    # (The first patch printed RESULT=FAIL then returned 0, letting Bash reach A-6 PASS.)
    # stop_required is set BEFORE engine.start is invoked, so finally always attempts
    # engine.stop() once start has begun -- including after a timeout or start exception.
    # If start already failed, the original start exception is preserved (a stop exception
    # raised in finally is recorded but does not replace the start error or make a success).
    stop_required = False
    started = False
    passed = False
    try:
        try:
            stop_required = True
            await asyncio.wait_for(engine.start(lookback=0), timeout=30)
            started = True
        except asyncio.TimeoutError:
            print("RESULT=FAIL engine_start_timeout"); raise
        except Exception as e:
            print("RESULT=FAIL engine_start_error: %r" % (e,)); raise
        om = engine.order_manager
        queued = len(om._queued_events)
        status = engine.status()
        depth = status['deferred_event_queue_depth']
        print("engine_state=%s" % engine.state)
        print("engine_mode=%s" % engine.mode)
        print("reconcile_ready=%s" % engine.reconcile_ready)
        print("reconcile_error=%s" % engine.reconcile_error)
        print("status_deferred_event_queue_depth=%s" % depth)
        print("queued_events_len=%d" % queued)
        print("mock_connected=%s" % engine.broker.connected)
        print("broker_orders=%d" % len(engine.broker.orders))
        print("broker_fills=%d" % len(engine.broker.fills))
        print("broker_position=%s" % engine.broker.position)
        ok = (engine.state == "DISARMED"
              and engine.reconcile_ready is True
              and engine.reconcile_error is None
              and depth == 0
              and queued == 0
              and engine.broker.connected is True
              and len(engine.broker.orders) == 0
              and len(engine.broker.fills) == 0
              and engine.broker.position is None
              and notifier_disabled)
        if not ok:
            print("RESULT=FAIL reconcile_assertion")
            raise AssertionError("empty-startup reconcile assertions not met")
        passed = True
    finally:
        if stop_required:
            try:
                await engine.stop()
                print("engine_stopped=yes")
            except Exception as e:
                # A stop failure is always nonzero. When start completed (started), the
                # stop exception governs and is re-raised. When start already failed, the
                # original start exception is still in flight; record the stop failure but
                # do not raise (preserves the start error; never synthesize success).
                print("RESULT=FAIL engine_stop_error: %r" % (e,))
                if started:
                    raise
        if passed:
            print("RESULT=PASS")

asyncio.run(run())
PYEOF
then
    fail "in-process dry run / assertions failed"
fi

# ---- step 4: temp DB persisted state -------------------------------------------
echo "A6_SECTION step4_tempdb"
if ! "$PY" - "$TMP/bridge.db" <<'PYEOF'
import sqlite3, sys
db = sys.argv[1]
con = sqlite3.connect("file:%s?mode=ro" % db, uri=True)
qc = con.execute("PRAGMA quick_check").fetchall()[0][0]
meta = dict(con.execute("SELECT key, value FROM meta").fetchall())
app_state = meta.get("app_state"); schema = meta.get("schema_version")
print("tempdb_quick_check=%s" % qc)
print("tempdb_app_state=%s" % app_state)
print("tempdb_schema_version=%s" % schema)
con.close()
if qc != "ok" or app_state != "DISARMED" or str(schema) != "4":
    print("RESULT=FAIL"); sys.exit(1)
print("RESULT=PASS")
PYEOF
then
    fail "temp DB state check failed"
fi

echo "A6_tempdb_scope=empty-broker startup proves no raise/hang/leftover queue on empty startup; NOT queue-drain-under-load; no full-reconcile requirement (baseline schema 4 disables it)"

# ---- step 5: production service unchanged after --------------------------------
echo "A6_SECTION step5_post"
post_act=$(getprop ActiveState); post_pid=$(getprop MainPID)
echo "A6_post_active=$post_act"; echo "A6_post_mainpid=$post_pid"
[[ "$post_act" == "active" ]] || fail "post ActiveState!=active ($post_act)"
[[ "$post_pid" == "$pre_pid" ]] || fail "production MainPID changed ($pre_pid -> $post_pid)"
echo "A6_post_api:"
if ! check_api; then fail "post API not credential-free DISARMED"; fi

echo "A6_SECTION done"
echo "A-6 PASS"
