#!/usr/bin/env bash
# Gate A - A-8 loopback binding proof (REMOTE side) (run-kit D, 2026-08-08)
# Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b (credential-free DISARMED)
#
# AUTHORIZED ONLY FOR THE OWNER-APPROVED PREREGISTERED GATE A RERUN on gatea-staging.
# Read-only: enumerates the LOCAL-ADDRESS column of every `ss -H -ltn 'sport = :8790'`
# entry and requires a nonempty set in which EVERY address is loopback
# (127.0.0.1:8790 or the IPv6 loopback form). Any wildcard (0.0.0.0/[::]/*), the VM IP,
# or any non-loopback address is a FAIL. Records `ip -brief address` and
# `ufw status verbose` as read-only evidence.
#
# This script does NOT POST /api/arm and does NOT read /etc/mtc-bridge/mtc-bridge.env.
# It writes only the evidence log under /home/gatea and performs no service mutation.
# Hard exclusions: no credential value, broker/exchange access, successful ARM, order,
# TESTNET/mainnet, wallet, master merge, or economic action. First genuine FAIL stops.
#
# NOTE: A-8 PASS requires BOTH this remote script ending `A-8 PASS` AND the Windows host
# script gatea_A8_host.ps1 showing port22_ok=true and port8790_ok=false. Neither alone
# passes the gate (assembled by the Lead from both logs).
set -Eeuo pipefail

UNIT="mtc-bridge-first-start.service"
VM_IP="172.24.55.233"
PY="/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b/bin/python"
LOG="/home/gatea/gatea-A8-20260808D.log"

if [[ -e "$LOG" ]]; then
    printf 'ERROR: evidence log already exists (%s); refusing to overwrite\n' "$LOG" >&2
    exit 2
fi

exec > "$LOG" 2>&1

finish() {
    local rc=$?
    printf '\nA8_TRAP_EXIT rc=%s\n' "$rc"
}
trap finish EXIT

fail() {
    printf 'A8_FAIL reason=%s\n' "$*"
    exit 1
}

echo "A8_SECTION header"
echo "A8_unit=$UNIT"
echo "A8_candidate=2ce41e34bceb599d80af24c5c33d835820ec321b"
echo "A8_vm_ip=$VM_IP"
echo "A8_py=$PY"
echo "A8_note=no POST /api/arm; env file contents not read; companion host script required for gate PASS"

# ---- step 1: enumerate local-address column; require all loopback --------------
echo "A8_SECTION step1_binding"
if ! "$PY" - "$VM_IP" <<'PYEOF'
import subprocess, sys
vm_ip = sys.argv[1]
out = subprocess.run(["ss", "-H", "-ltn", "sport = :8790"], capture_output=True, text=True)
print("ss_rc=%s" % out.returncode)
if out.returncode != 0:
    print("RESULT=FAIL ss_nonzero"); sys.exit(1)
# `ss -H -ltn` columns: [0]=state [1]=Recv-Q [2]=Send-Q [3]=LOCAL addr:port
# [4]=PEER addr:port. We collect the LOCAL column at index 3. Index 4 (peer) is
# the listener's peer, which is always *:* for a listener — appending p[4] is
# FORBIDDEN (it repeats the A-4 peer-column false negative). Require >= 5 fields
# so the LOCAL column is present.
addrs = []
for line in out.stdout.splitlines():
    p = line.split()
    if len(p) >= 5:
        addrs.append(p[3])
print("listener_count=%d" % len(addrs))
print("local_addresses=%s" % (",".join(addrs) if addrs else ""))
def host_of(a):
    return a.rsplit(":", 1)[0].strip("[]")
def is_loopback(a):
    h = host_of(a)
    return h == "::1" or h == "127.0.0.1" or h.startswith("127.")
bad = [a for a in addrs if not is_loopback(a)]
wildcard = [a for a in addrs if host_of(a) in ("0.0.0.0", "::", "*", "*:*")]
on_vm = [a for a in addrs if host_of(a) == vm_ip]
print("nonloopback_addrs=%s" % (",".join(bad) if bad else ""))
print("wildcard_addrs=%s" % (",".join(wildcard) if wildcard else ""))
print("vm_ip_addrs=%s" % (",".join(on_vm) if on_vm else ""))
ok = len(addrs) > 0 and len(bad) == 0
print("RESULT=%s" % ("PASS" if ok else "FAIL"))
if not ok:
    sys.exit(1)
PYEOF
then
    fail ":8790 binding is not loopback-only (empty / wildcard / VM IP / non-loopback)"
fi

# ---- step 2: record ip -brief address (read-only) ------------------------------
echo "A8_SECTION step2_ip"
echo "A8_ip_brief_begin"
ip -brief address || true
echo "A8_ip_brief_end"

# ---- step 3: record ufw status verbose (read-only) -----------------------------
echo "A8_SECTION step3_ufw"
echo "A8_ufw_begin"
ufw_rc=0
sudo ufw status verbose || ufw_rc=$?
echo "A8_ufw_rc=$ufw_rc"
echo "A8_ufw_end"

echo "A8_SECTION done"
echo "A-8 PASS"
