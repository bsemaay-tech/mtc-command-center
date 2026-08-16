#!/usr/bin/env bash
#
# verify.sh — read-only verification of an installed bridge release.
#
# Every check is an assertion. This script starts nothing, enables nothing,
# unmasks nothing, provisions nothing, reads no secret value, and changes no
# firewall rule. It is safe to run at any time and prints one PASS/FAIL line per
# check, then exits non-zero if any check failed (fail closed).
#
# Usage:
#   sudo bash ./verify.sh --release-sha <40-hex> --manifest-sha256 <64-hex>
#
# Exit codes: 0 all checks passed; 1 at least one check failed or bad usage.

set -Eeuo pipefail
IFS=$'\n\t'

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/common.sh
. "${SCRIPT_DIR}/lib/common.sh"

RELEASE_SHA=""
MANIFEST_SHA256=""
while [ "$#" -gt 0 ]; do
  case "$1" in
    --release-sha) RELEASE_SHA="${2:-}"; shift 2 ;;
    --manifest-sha256) MANIFEST_SHA256="${2:-}"; shift 2 ;;
    -h|--help)     sed -n '2,16p' "${BASH_SOURCE[0]}"; exit 1 ;;
    *)             die "unknown argument: $1" ;;
  esac
done
[ -n "${RELEASE_SHA}" ] || die "--release-sha is required"
[ -n "${MANIFEST_SHA256}" ] || die "--manifest-sha256 is required"
require_release_sha "${RELEASE_SHA}"
require_sha256 "${MANIFEST_SHA256}"
require_root
require_cmd stat find systemctl sha256sum sed cmp sort awk getent id pgrep

DEST="$(release_dir "${RELEASE_SHA}")"
VENV="$(venv_dir "${RELEASE_SHA}")"
MTC_FAILURES=0

log "verifying release ${RELEASE_SHA} (read-only)"

for canonical_path in \
    "${MTC_OPT_ROOT}" "${MTC_RELEASES_ROOT}" "${MTC_VENVS_ROOT}" \
    "${DEST}" "${VENV}" "${MTC_STATE_DIR}" "${MTC_LOG_DIR}" \
    "${MTC_CONF_DIR}" "${MTC_ENV_FILE}" "${MTC_INSTALL_MANIFEST}" \
    "${MTC_UNIT_DIR}" "${MTC_UNIT_DIR}/${MTC_FIRST_START_UNIT}" \
    "${MTC_LOGROTATE_FILE}"; do
  assert_not_symlink "${canonical_path}"
done

# --- 1. service identity ---------------------------------------------------
if getent passwd "${MTC_USER}" >/dev/null; then
  shell="$(getent passwd "${MTC_USER}" | awk -F: '{print $7}')"
  user_gid="$(getent passwd "${MTC_USER}" | awk -F: '{print $4}')"
  group_gid="$(getent group "${MTC_GROUP}" | awk -F: '{print $3}')"
  case "${shell}" in
    */nologin|*/false) pass "service user ${MTC_USER} is non-login (${shell})" ;;
    *)                 fail "service user ${MTC_USER} has a login shell: ${shell}" ;;
  esac
  if [ -n "${group_gid}" ] && [ "${user_gid}" = "${group_gid}" ]; then
    pass "service user primary group is ${MTC_GROUP}"
  else
    fail "service user primary group is not ${MTC_GROUP}"
  fi
  if id -nG "${MTC_USER}" | tr ' ' '\n' | grep -qxE 'sudo|admin|docker|adm|systemd-journal'; then
    fail "service user is in a privileged group"
  else
    pass "service user holds no privileged group membership"
  fi
else
  fail "service user ${MTC_USER} does not exist"
fi

# --- 2. immutable release tree --------------------------------------------
if [ -d "${DEST}" ]; then
  assert_mode_owner "${DEST}" 0555 root:root || true
  assert_no_writable_paths "${DEST}" || true
  assert_exact_payload_tree "${DEST}" || true
  actual_manifest_sha="$(sha256_of "${DEST}/RELEASE_SHA256SUMS")"
  if [ "${actual_manifest_sha}" = "${MANIFEST_SHA256}" ]; then
    pass "release manifest matches accepted sha256"
  else
    fail "release manifest does not match accepted sha256"
  fi
  if ( cd "${DEST}" && sha256sum --strict --quiet -c RELEASE_SHA256SUMS ); then
    pass "release payload matches RELEASE_SHA256SUMS"
  else
    fail "release payload does not match RELEASE_SHA256SUMS"
  fi
  marker="$(tr -d '[:space:]' < "${DEST}/RELEASE_SHA" 2>/dev/null || true)"
  if [ "${marker}" = "${RELEASE_SHA}" ]; then
    pass "release marker matches ${RELEASE_SHA}"
  else
    fail "release marker mismatch"
  fi
else
  fail "release directory missing: ${DEST}"
fi

# --- 3. hash-locked virtual environment -----------------------------------
if [ -x "${VENV}/bin/python" ]; then
  assert_mode_owner "${VENV}" 0555 root:root || true
  assert_no_writable_paths "${VENV}" || true
  pyver="$("${VENV}/bin/python" -c 'import sys; print("%d.%d" % sys.version_info[:2])')"
  if [ "${pyver}" = "3.12" ]; then
    pass "venv interpreter is Python ${pyver}"
  else
    fail "venv interpreter is Python ${pyver}, expected 3.12"
  fi
else
  fail "venv interpreter missing"
fi
if "${VENV}/bin/python" "${DEST}/IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py" \
    --lock "${DEST}/IBKR_PAPER_BRIDGE/requirements.lock" --check-installed; then
  pass "venv distributions exactly match the hash-locked requirements"
else
  fail "venv distributions do not exactly match the hash-locked requirements"
fi

# --- 4. writable state / log / config paths -------------------------------
assert_mode_owner "${MTC_STATE_DIR}" 0750 "${MTC_USER}:${MTC_GROUP}" || true
assert_mode_owner "${MTC_LOG_DIR}"   0750 "${MTC_USER}:${MTC_GROUP}" || true
assert_mode_owner "${MTC_CONF_DIR}"  0750 root:root || true
assert_mode_owner "${MTC_ENV_FILE}"  0600 root:root || true
assert_mode_owner "${MTC_INSTALL_MANIFEST}" 0640 root:root || true
if grep -qF "\"release_sha\": \"${RELEASE_SHA}\"" "${MTC_INSTALL_MANIFEST}" 2>/dev/null \
   && grep -qF "\"release_manifest_sha256\": \"${MANIFEST_SHA256}\"" \
      "${MTC_INSTALL_MANIFEST}" 2>/dev/null; then
  pass "install manifest binds release and payload manifest hashes"
else
  fail "install manifest does not bind the expected release hashes"
fi

# --- 5. secret hygiene (names only; no value is ever read or printed) -----
if [ -f "${MTC_ENV_FILE}" ] && grep -qE '^[[:space:]]*(export[[:space:]]+)?HL_LIVE_ACK=' "${MTC_ENV_FILE}"; then
  fail "HL_LIVE_ACK is defined in the env file"
else
  pass "HL_LIVE_ACK absent from env file"
fi
if [ -f "${MTC_ENV_FILE}" ] && grep -qE '^[[:space:]]*(export[[:space:]]+)?MTC_BRIDGE_START_MODE=' "${MTC_ENV_FILE}"; then
  fail "MTC_BRIDGE_START_MODE is defined in the env file"
else
  pass "MTC_BRIDGE_START_MODE absent from env file"
fi
if grep -rqE '^[[:space:]]*Environment=.*HL_(API_WALLET_KEY|ACCOUNT_ADDRESS|LIVE_ACK)' \
     "${MTC_UNIT_DIR}/${MTC_FIRST_START_UNIT}" 2>/dev/null; then
  fail "unit carries credential material in Environment="
else
  pass "unit carries no credential material"
fi

# --- 6. unit state: installed, masked, never started, never enabled -------
if [ -f "${MTC_UNIT_DIR}/${MTC_FIRST_START_UNIT}" ]; then
  unit="${MTC_UNIT_DIR}/${MTC_FIRST_START_UNIT}"
  pass "first-start unit installed at ${unit}"
  log  "first-start unit sha256=$(sha256_of "${unit}")"
  for needle in \
      'Restart=no' \
      'User=mtc-bridge' \
      'PrivateTmp=yes' \
      'ProtectSystem=strict' \
      'NoNewPrivileges=yes' \
      'KillSignal=SIGTERM' \
      'TimeoutStopSec=45' \
      'StartLimitBurst=3' \
      'MemoryHigh=768M' \
      'MemoryMax=1G' \
      "ReadWritePaths=${MTC_STATE_DIR} ${MTC_LOG_DIR}" \
      "MTC_BRIDGE_STATE_DB=${MTC_STATE_DB}" \
      'MTC_BRIDGE_START_MODE=credential_free_disarmed' \
      "MTC_BRIDGE_RELEASE_SHA=${RELEASE_SHA}" ; do
    if grep -qF "${needle}" "${unit}"; then
      pass "unit declares ${needle}"
    else
      fail "unit is missing ${needle}"
    fi
  done
  if grep -q "releases/${RELEASE_SHA}/" "${unit}"; then
    pass "unit is bound to the exact release sha"
  else
    fail "unit does not reference releases/${RELEASE_SHA}"
  fi
  if grep -q "venvs/${RELEASE_SHA}/bin/python" "${unit}"; then
    pass "unit uses the exact per-SHA venv"
  else
    fail "unit does not use the exact per-SHA venv"
  fi
  if cmp -s \
      <(sed "s/@RELEASE_SHA@/${RELEASE_SHA}/g" \
        "${DEST}/IBKR_PAPER_BRIDGE/deploy/linux/systemd/${MTC_FIRST_START_UNIT}.template") \
      "${unit}"; then
    pass "installed unit exactly matches the accepted release template"
  else
    fail "installed unit differs from the accepted release template"
  fi
  if grep -q '^\[Install\]' "${unit}"; then
    fail "unit has an [Install] section and could be enabled at boot"
  else
    pass "unit has no [Install] section and cannot be enabled"
  fi
else
  fail "first-start unit not installed"
fi

if [ -L "${MTC_MASK_DIR}/${MTC_FIRST_START_UNIT}" ] \
   && [ "$(readlink -f "${MTC_MASK_DIR}/${MTC_FIRST_START_UNIT}")" = "/dev/null" ]; then
  pass "first-start unit is masked"
else
  fail "first-start unit is not masked"
fi
if systemctl is-active --quiet "${MTC_FIRST_START_UNIT}"; then
  fail "first-start unit is ACTIVE; it must not be running before KVM2-P4-07"
else
  pass "first-start unit is not active"
fi
case "$(systemctl is-enabled "${MTC_FIRST_START_UNIT}" 2>&1 || true)" in
  masked|disabled|static) pass "first-start unit is not enabled" ;;
  *)                      fail "first-start unit reports an enabled state" ;;
esac

# --- 7. restart-enabled steady profile must be absent ---------------------
if [ -e "${MTC_UNIT_DIR}/${MTC_STEADY_UNIT}" ] \
   || [ -L "${MTC_UNIT_DIR}/${MTC_STEADY_UNIT}" ] \
   || [ -e "${MTC_MASK_DIR}/${MTC_STEADY_UNIT}" ] \
   || [ -L "${MTC_MASK_DIR}/${MTC_STEADY_UNIT}" ]; then
  fail "restart-enabled steady unit is installed; it needs its own gate"
else
  pass "restart-enabled steady unit absent"
fi

# --- 8. logs, rotation, control plane -------------------------------------
if [ -f "${MTC_LOGROTATE_FILE}" ]; then
  pass "logrotate policy installed"
else
  fail "logrotate policy missing"
fi
assert_loopback_only_source "${DEST}/IBKR_PAPER_BRIDGE/bridge/app.py" || true
# This verifier is specifically the masked/unstarted mode. A future explicit
# running/steady verifier may allow one bound writer, but this mode requires
# both zero writer processes and a completely closed port, including loopback.
if pgrep -f '[b]ridge\.app' >/dev/null 2>&1; then
  fail "orphan bridge.app writer exists while service must be unstarted"
else
  pass "no bridge.app writer process exists"
fi
assert_control_port_closed || true
assert_no_public_control_listener || true
assert_ufw_bridge_safe || true

# --- 9. summary ------------------------------------------------------------
if [ "${MTC_FAILURES}" -eq 0 ]; then
  log "VERIFY PASS — release ${RELEASE_SHA} installed, masked, unstarted, unarmed"
  exit 0
fi
log "VERIFY FAIL — ${MTC_FAILURES} check(s) failed"
exit 1
