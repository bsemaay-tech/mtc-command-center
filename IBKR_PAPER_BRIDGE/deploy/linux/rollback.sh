#!/usr/bin/env bash
#
# rollback.sh — return the host to a recorded, stopped, unarmed state.
#
# Rollback here means exactly what KVM2-P4-08 defines it to mean:
#   service stopped and masked, state and risk artifacts preserved, writer
#   count zero, no Windows authority re-enabled.
#
# WHAT THIS SCRIPT DOES
#   * gracefully stops the first-start unit if (and only if) it is running;
#   * masks it so it cannot be started again without an explicit unmask;
#   * optionally re-binds the first-start unit to a previously installed
#     rollback release SHA, verifying that release's checksums first;
#   * records a rollback manifest with both SHAs and the unit hash.
#
# WHAT THIS SCRIPT NEVER DOES
#   * start, enable, unmask or arm any service — the post-rollback recovery
#     start is a separate authorization (KVM2-P4-08A) and a separate bounded
#     execution (KVM2-P4-08B);
#   * delete, move, reset or migrate /var/lib/mtc-bridge — risk-state evidence
#     is preserved, never cleaned;
#   * touch the firewall, any secret, the Windows writer, or the exchange.
#
# Usage:
#   sudo bash ./rollback.sh --state-manifest-file <file> \
#        --state-manifest-sha256 <64-hex> \
#        [--to-release-sha <40-hex> --to-manifest-sha256 <64-hex>] [--dry-run]
#
# Exit codes: 0 rollback recorded; 1 any precondition or check failure.

set -Eeuo pipefail
IFS=$'\n\t'

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/common.sh
. "${SCRIPT_DIR}/lib/common.sh"

TARGET_SHA=""
TARGET_MANIFEST_SHA256=""
STATE_MANIFEST_FILE=""
STATE_MANIFEST_SHA256=""
while [ "$#" -gt 0 ]; do
  case "$1" in
    --to-release-sha) TARGET_SHA="${2:-}"; shift 2 ;;
    --to-manifest-sha256) TARGET_MANIFEST_SHA256="${2:-}"; shift 2 ;;
    --state-manifest-file) STATE_MANIFEST_FILE="${2:-}"; shift 2 ;;
    --state-manifest-sha256) STATE_MANIFEST_SHA256="${2:-}"; shift 2 ;;
    --dry-run)        MTC_DRY_RUN=1;       shift ;;
    -h|--help)        sed -n '2,26p' "${BASH_SOURCE[0]}"; exit 1 ;;
    *)                die "unknown argument: $1" ;;
  esac
done

require_root
require_cmd systemctl sha256sum sed install grep cmp sort awk find mktemp date \
            basename pgrep ss
[ -n "${STATE_MANIFEST_FILE}" ] || die "--state-manifest-file is required"
[ -n "${STATE_MANIFEST_SHA256}" ] || die "--state-manifest-sha256 is required"
require_sha256 "${STATE_MANIFEST_SHA256}"
[ -f "${STATE_MANIFEST_FILE}" ] || die "state manifest file is missing"
[ "$(sha256_of "${STATE_MANIFEST_FILE}")" = "${STATE_MANIFEST_SHA256}" ] \
  || die "state manifest file hash does not match accepted sha256"
if [ -n "${TARGET_SHA}" ] || [ -n "${TARGET_MANIFEST_SHA256}" ]; then
  [ -n "${TARGET_SHA}" ] && [ -n "${TARGET_MANIFEST_SHA256}" ] \
    || die "--to-release-sha and --to-manifest-sha256 must be supplied together"
  require_release_sha "${TARGET_SHA}"
  require_sha256 "${TARGET_MANIFEST_SHA256}"
fi

MTC_ROLLBACK_MANIFEST="${MTC_CONF_DIR}/rollback_manifest.json"
assert_not_symlink "${MTC_ROLLBACK_MANIFEST}"
if [ -e "${MTC_UNIT_DIR}/${MTC_STEADY_UNIT}" ] \
   || [ -L "${MTC_UNIT_DIR}/${MTC_STEADY_UNIT}" ] \
   || [ -e "${MTC_MASK_DIR}/${MTC_STEADY_UNIT}" ] \
   || [ -L "${MTC_MASK_DIR}/${MTC_STEADY_UNIT}" ]; then
  die "unexpected steady unit is installed; preserve evidence and stop"
fi

# --- 1. stop, never start --------------------------------------------------
if systemctl is-active --quiet "${MTC_FIRST_START_UNIT}"; then
  log "stopping ${MTC_FIRST_START_UNIT} (SIGTERM, 45s grace per unit)"
  run systemctl stop "${MTC_FIRST_START_UNIT}"
else
  log "${MTC_FIRST_START_UNIT} already inactive"
fi
run systemctl mask "${MTC_FIRST_START_UNIT}"

if [ "${MTC_DRY_RUN}" != "1" ] && systemctl is-active --quiet "${MTC_FIRST_START_UNIT}"; then
  die "unit is still active after stop; escalate, do not retry blindly"
fi
if [ "${MTC_DRY_RUN}" != "1" ]; then
  MTC_FAILURES=0
  assert_control_port_closed || true
  if pgrep -f '[b]ridge\.app' >/dev/null 2>&1; then
    fail "a bridge.app process remains after service stop"
  else
    pass "no bridge.app process remains"
  fi
  [ "${MTC_FAILURES}" -eq 0 ] \
    || die "local writer-absence checks failed; preserve evidence and stop"
fi

# --- 2. preserve state -----------------------------------------------------
# Deliberately assertion-only: risk history is evidence, never cleanup.
if [ -e "${MTC_STATE_DB}" ]; then
  log "state preserved: $(basename "${MTC_STATE_DB}")"
  log "accepted state-bundle manifest sha256=${STATE_MANIFEST_SHA256}"
else
  log "no state database present at the canonical path"
fi

# --- 3. optionally re-bind the unit to a prior release --------------------
UNIT_SHA=""
if [ -f "${MTC_UNIT_DIR}/${MTC_FIRST_START_UNIT}" ]; then
  UNIT_SHA="$(sha256_of "${MTC_UNIT_DIR}/${MTC_FIRST_START_UNIT}")"
fi
if [ -n "${TARGET_SHA}" ]; then
  TARGET_DIR="$(release_dir "${TARGET_SHA}")"
  TARGET_VENV="$(venv_dir "${TARGET_SHA}")"
  [ -d "${TARGET_DIR}" ] || die "rollback release is not installed: ${TARGET_SHA}"
  [ -x "${TARGET_VENV}/bin/python" ] || die "rollback release venv is not installed"
  [ "$(sha256_of "${TARGET_DIR}/RELEASE_SHA256SUMS")" = "${TARGET_MANIFEST_SHA256}" ] \
    || die "rollback release manifest hash does not match accepted sha256"
  ( cd "${TARGET_DIR}" && sha256sum --strict --quiet -c RELEASE_SHA256SUMS ) \
    || die "rollback release failed checksum verification"
  MTC_FAILURES=0
  assert_exact_payload_tree "${TARGET_DIR}" || true
  assert_no_writable_paths "${TARGET_DIR}" || true
  assert_no_writable_paths "${TARGET_VENV}" || true
  [ "${MTC_FAILURES}" -eq 0 ] || die "rollback release is not immutable"
  "${TARGET_VENV}/bin/python" \
      "${TARGET_DIR}/IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py" \
      --lock "${TARGET_DIR}/IBKR_PAPER_BRIDGE/requirements.lock" --check-installed \
    || die "rollback venv does not match its exact lock"

  RENDERED="$(mktemp)"
  trap 'rm -f "${RENDERED}"' EXIT
  sed "s/@RELEASE_SHA@/${TARGET_SHA}/g" \
      "${TARGET_DIR}/IBKR_PAPER_BRIDGE/deploy/linux/systemd/${MTC_FIRST_START_UNIT}.template" \
      > "${RENDERED}"
  if grep -q '@RELEASE_SHA@' "${RENDERED}"; then
    die "unit template placeholder not substituted"
  fi
  grep -q '^Restart=no$' "${RENDERED}" || die "rendered unit is not Restart=no"
  if grep -q '^\[Install\]' "${RENDERED}"; then
    die "rendered rollback unit must have no [Install] section"
  fi

  run install -o root -g root -m 0644 "${RENDERED}" "${MTC_UNIT_DIR}/${MTC_FIRST_START_UNIT}"
  UNIT_SHA="$(sha256_of "${RENDERED}")"
  run systemctl daemon-reload
  # daemon-reload does not unmask; re-assert the mask explicitly.
  run systemctl mask "${MTC_FIRST_START_UNIT}"
  log "unit re-bound to ${TARGET_SHA} sha256=${UNIT_SHA} (still masked)"
fi

# --- 4. rollback manifest --------------------------------------------------
if [ "${MTC_DRY_RUN}" != "1" ]; then
  umask 077
  cat > "${MTC_ROLLBACK_MANIFEST}" <<EOF
{
  "schema_version": "1.0.0",
  "rolled_back_at_utc": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "rollback_release_sha": "${TARGET_SHA}",
  "rollback_release_manifest_sha256": "${TARGET_MANIFEST_SHA256}",
  "state_bundle_manifest_sha256": "${STATE_MANIFEST_SHA256}",
  "first_start_unit": "${MTC_FIRST_START_UNIT}",
  "first_start_unit_sha256": "${UNIT_SHA}",
  "first_start_unit_state": "masked",
  "service_active": false,
  "service_enabled": false,
  "service_started_by_this_script": false,
  "state_dir_preserved": true,
  "secrets_touched": false,
  "firewall_modified": false,
  "windows_writer_restored": false
}
EOF
  chown root:root "${MTC_ROLLBACK_MANIFEST}"
  chmod 0640 "${MTC_ROLLBACK_MANIFEST}"
fi

log "rollback complete: unit stopped/masked, state preserved, no local bridge.app/control listener observed."
log "Exchange authority and any other host remain separate single-writer proofs."
log "A recovery start requires KVM2-P4-08A authorization then a single KVM2-P4-08B attempt."
