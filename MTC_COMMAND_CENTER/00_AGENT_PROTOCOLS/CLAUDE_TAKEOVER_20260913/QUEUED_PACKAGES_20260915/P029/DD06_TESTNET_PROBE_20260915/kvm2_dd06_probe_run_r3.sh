# WP-P0-29 DD-06 TESTNET falsification probe — r3 under the owner word "r3 go" (2026-09-16 11:5x UTC+3; agent wallet funded by the owner with 14 USDC spot), slice 3 script,
# steps 2-3 of DD06_TESTNET_PROBE_STEP_PACKET_20260915.md. Same host-contact shape as the 2026-09-14 smoke:
# root sources the 0600 env file into the process environment only; mtc-bridge runs the probe once under timeout 300;
# every byte leaving the host passes sed redaction of 0x+64hex and 0x+40hex. Nothing else on the host is touched.
set -u
W=/tmp/smoke_p0_20260914T140527Z/IBKR_PAPER_BRIDGE
V=/opt/mtc-bridge/venvs/be007fd802bbfd2eb181d66038c374865d1562ee/bin/python
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
OUT=/tmp/dd06_$STAMP
RUN_ID=dd06-testnet-$STAMP-r3
echo "UTC_start=$(date -u +%Y-%m-%dT%H:%M:%SZ) run_id=$RUN_ID out=$OUT"
echo "probe_sha256=$(sudo -n sha256sum $W/tools/dd06_agent_withdraw_probe.py | cut -c1-64)"
echo "service_before=$(systemctl is-active mtc-bridge-first-start.service) nrestarts_before=$(systemctl show -p NRestarts --value mtc-bridge-first-start.service) api_before=$(curl -s --max-time 5 http://127.0.0.1:8790/api/status | tr -d '\n' | cut -c1-80)"
echo "--- probe start $(date -u +%H:%M:%SZ) ---"
sudo -n bash -c "set -a; . /etc/mtc-bridge/mtc-bridge.env; set +a; unset HL_LIVE_ACK; export PYTHONUTF8=1 PYTHONDONTWRITEBYTECODE=1; cd '$W' && exec timeout 300 runuser -u mtc-bridge -- '$V' tools/dd06_agent_withdraw_probe.py --run-id '$RUN_ID' --out '$OUT'" 2>&1 | sed -E 's/0x[0-9a-fA-F]{64}/0x[REDACTED_64HEX]/g; s/[0-9a-fA-F]{64}/[REDACTED_64HEX]/g; s/0x[0-9a-fA-F]{40}/0x[REDACTED_ADDRESS]/g'
echo "probe_exit=${PIPESTATUS[0]}"
echo "--- probe end $(date -u +%H:%M:%SZ) ---"
echo "service_after=$(systemctl is-active mtc-bridge-first-start.service) nrestarts_after=$(systemctl show -p NRestarts --value mtc-bridge-first-start.service) api_after=$(curl -s --max-time 5 http://127.0.0.1:8790/api/status | tr -d '\n' | cut -c1-80)"
REC="$OUT/DD06_PROBE_RECORD.json"
if sudo -n test -f "$REC"; then
  echo "record_sha256_on_host=$(sudo -n sha256sum "$REC" | cut -c1-64) record_bytes=$(sudo -n stat -c %s "$REC") sidecar=$(sudo -n cat "$REC.sha256" 2>/dev/null | cut -c1-64)"
  echo "=== RECORD (redacted again on the way out) ==="
  sudo -n cat "$REC" | sed -E 's/0x[0-9a-fA-F]{64}/0x[REDACTED_64HEX]/g; s/[0-9a-fA-F]{64}/[REDACTED_64HEX]/g; s/0x[0-9a-fA-F]{40}/0x[REDACTED_ADDRESS]/g'
  echo "=== END RECORD ==="
else
  echo "record_missing=1 out_dir_listing=$(sudo -n ls -la "$OUT" 2>&1 | tr '\n' ' ' | cut -c1-300)"
fi
echo "UTC_end=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
