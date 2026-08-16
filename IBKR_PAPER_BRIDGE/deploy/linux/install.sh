#!/usr/bin/env bash
#
# install.sh — bounded, non-interactive, fail-closed installation of ONE exact
# bridge release onto an Ubuntu 24.04 host.
#
# WHAT THIS SCRIPT DOES
#   * verifies the payload against RELEASE_SHA + RELEASE_SHA256SUMS;
#   * creates the dedicated non-login `mtc-bridge` identity;
#   * materialises the immutable release at /opt/mtc-bridge/releases/<sha>,
#     root-owned and read-only;
#   * builds a per-SHA Python 3.12 venv under /opt/mtc-bridge/venvs and installs
#     ONLY binary wheels from `requirements.lock` with `--require-hashes` (no
#     global pip, floating version, unhashed artifact, or unpinned build env);
#   * creates /var/lib/mtc-bridge, /var/log/mtc-bridge, /etc/mtc-bridge;
#   * creates the root-owned 0600 env file with NO values in it;
#   * installs the first-start unit MASKED and installs the logrotate policy;
#   * asserts UFW is active/default-deny, SSH remains allowed, and 8790 is not.
#
# WHAT THIS SCRIPT NEVER DOES
#   * start, enable or arm any service;
#   * install or enable the restart-enabled steady profile;
#   * write, read, prompt for, or transfer any secret value;
#   * add, remove or modify a firewall rule;
#   * touch the Windows writer, perform a cutover, or migrate state;
#   * contact a broker, an exchange or any network endpoint other than the
#     package index (and not even that when --wheelhouse is used).
#
# Running it requires the separate KVM2-P4-01 installation authorization and is
# bounded to exactly one attempt (KVM2-P4-02). It grants no later authority.
#
# Usage:
#   sudo bash ./install.sh --release-sha <40-hex> \
#        --manifest-sha256 <64-hex> --source <payload dir> \
#        [--wheelhouse <dir>] [--dry-run]
#
# Exit codes: 0 installed/idempotent no-op; 1 any precondition or check failure.

set -Eeuo pipefail
IFS=$'\n\t'

RELEASE_SHA=""
MANIFEST_SHA256=""
SOURCE_DIR=""
WHEELHOUSE=""
MTC_DRY_RUN="${MTC_DRY_RUN:-0}"

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
EXECUTING_INSTALLER="${SCRIPT_DIR}/$(basename -- "${BASH_SOURCE[0]}")"

bootstrap_die() {
  printf '[mtc-bridge] FATAL: %s\n' "$*" >&2
  exit 1
}

usage() {
  sed -n '2,40p' "${BASH_SOURCE[0]}"
  exit 1
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --release-sha) RELEASE_SHA="${2:-}"; shift 2 ;;
    --manifest-sha256) MANIFEST_SHA256="${2:-}"; shift 2 ;;
    --source)      SOURCE_DIR="${2:-}";  shift 2 ;;
    --wheelhouse)  WHEELHOUSE="${2:-}";  shift 2 ;;
    --dry-run)     MTC_DRY_RUN=1;        shift ;;
    -h|--help)     usage ;;
    *)             bootstrap_die "unknown argument: $1" ;;
  esac
done

[ -n "${RELEASE_SHA}" ] || bootstrap_die "--release-sha is required"
[ -n "${MANIFEST_SHA256}" ] || bootstrap_die "--manifest-sha256 is required"
[ -n "${SOURCE_DIR}" ] || bootstrap_die "--source is required"
[[ "${RELEASE_SHA}" =~ ^[0-9a-f]{40}$ ]] \
  || bootstrap_die "release sha must be exactly 40 lowercase hex characters"
[[ "${MANIFEST_SHA256}" =~ ^[0-9a-f]{64}$ ]] \
  || bootstrap_die "sha256 must be exactly 64 lowercase hex characters"
for command_name in realpath sha256sum find sort sed cmp tr awk; do
  command -v "${command_name}" >/dev/null 2>&1 \
    || bootstrap_die "required bootstrap command missing: ${command_name}"
done

# Bootstrap the trust boundary without sourcing any helper. The only helper we
# execute is common.sh from the externally hash-bound payload, and only after
# the entire payload has proved to contain regular files and match its exact
# manifest. This must happen before any target-host mutation.
[ -d "${SOURCE_DIR}" ] || bootstrap_die "payload directory not found"
[ ! -L "${SOURCE_DIR}" ] || bootstrap_die "payload directory must not be a symlink"
SOURCE_DIR="$(realpath -e -- "${SOURCE_DIR}")" \
  || bootstrap_die "cannot resolve payload directory"
PAYLOAD_DEPLOY_DIR="${SOURCE_DIR}/IBKR_PAPER_BRIDGE/deploy/linux"
PAYLOAD_INSTALLER="${PAYLOAD_DEPLOY_DIR}/install.sh"
PAYLOAD_COMMON="${PAYLOAD_DEPLOY_DIR}/lib/common.sh"
[ "${EXECUTING_INSTALLER}" = "${PAYLOAD_INSTALLER}" ] \
  || bootstrap_die "executing installer is not the installer inside the accepted payload"
[ ! -L "${BASH_SOURCE[0]}" ] \
  || bootstrap_die "executing installer path must not be a symlink"

if ! BOOTSTRAP_OFFENDER="$(
    find "${SOURCE_DIR}" -mindepth 1 ! -type d ! -type f -print -quit 2>/dev/null
  )"; then
  bootstrap_die "cannot inventory payload filesystem entry types"
fi
[ -z "${BOOTSTRAP_OFFENDER}" ] \
  || bootstrap_die "payload contains a symlink or special filesystem entry"
[ -f "${SOURCE_DIR}/RELEASE_SHA" ] \
  || bootstrap_die "payload has no regular RELEASE_SHA marker"
[ -f "${SOURCE_DIR}/RELEASE_SHA256SUMS" ] \
  || bootstrap_die "payload has no regular RELEASE_SHA256SUMS manifest"

ACTUAL_MANIFEST_SHA="$(sha256sum "${SOURCE_DIR}/RELEASE_SHA256SUMS" | awk '{print $1}')"
[ "${ACTUAL_MANIFEST_SHA}" = "${MANIFEST_SHA256}" ] \
  || bootstrap_die "payload manifest hash does not match --manifest-sha256"
if ! cmp -s \
    <(sed -E 's/^[0-9a-f]{64} [ *]//' "${SOURCE_DIR}/RELEASE_SHA256SUMS" | sort) \
    <(cd "${SOURCE_DIR}" && find . -type f '!' -name RELEASE_SHA256SUMS -print | sort); then
  bootstrap_die "payload file inventory differs from RELEASE_SHA256SUMS"
fi
( cd "${SOURCE_DIR}" && sha256sum --strict --quiet -c RELEASE_SHA256SUMS ) \
  || bootstrap_die "payload checksum verification failed"

[ -f "${PAYLOAD_INSTALLER}" ] \
  || bootstrap_die "accepted payload installer is not a regular file"
[ -f "${PAYLOAD_COMMON}" ] \
  || bootstrap_die "accepted payload common helper is not a regular file"
# shellcheck source=lib/common.sh
. "${PAYLOAD_COMMON}"

require_release_sha "${RELEASE_SHA}"
require_sha256 "${MANIFEST_SHA256}"
require_root
require_cmd sha256sum install find chmod chown stat systemctl sed grep tr cp cmp \
            sort awk date getent groupadd useradd id pgrep readlink realpath "${MTC_PYTHON}"
preflight_venv_capability

DEST="$(release_dir "${RELEASE_SHA}")"
VENV="$(venv_dir "${RELEASE_SHA}")"

# --------------------------------------------------------------------------
# 0. refuse to run in a state that would make the install unsafe
# --------------------------------------------------------------------------
if [ -n "${HL_LIVE_ACK:-}" ]; then
  die "HL_LIVE_ACK is set in this shell; mainnet acknowledgement must never be present"
fi
if [ -e "${MTC_MASK_DIR}/${MTC_STEADY_UNIT}" ] \
   || [ -L "${MTC_MASK_DIR}/${MTC_STEADY_UNIT}" ] \
   || [ -e "${MTC_UNIT_DIR}/${MTC_STEADY_UNIT}" ] \
   || [ -L "${MTC_UNIT_DIR}/${MTC_STEADY_UNIT}" ]; then
  die "restart-enabled steady unit is present; it must be admitted through its own gate, not here"
fi

# --------------------------------------------------------------------------
# 1. payload verification — exact SHA binding + checksum manifest
# --------------------------------------------------------------------------
PAYLOAD_SHA="$(tr -d '[:space:]' < "${SOURCE_DIR}/RELEASE_SHA")"
[ "${PAYLOAD_SHA}" = "${RELEASE_SHA}" ] || die "payload RELEASE_SHA does not match --release-sha"
[ "$(sha256_of "${SOURCE_DIR}/RELEASE_SHA256SUMS")" = "${ACTUAL_MANIFEST_SHA}" ] \
  || die "payload manifest changed after bootstrap verification"
[ "${ACTUAL_MANIFEST_SHA}" = "${MANIFEST_SHA256}" ] \
  || die "payload manifest hash does not match --manifest-sha256"

log "verifying payload checksums"
( cd "${SOURCE_DIR}" && sha256sum --strict --quiet -c RELEASE_SHA256SUMS ) \
  || die "payload checksum verification failed"
MTC_FAILURES=0
assert_exact_payload_tree "${SOURCE_DIR}" || true
[ "${MTC_FAILURES}" -eq 0 ] || die "payload file inventory verification failed"

LOCKFILE="${SOURCE_DIR}/IBKR_PAPER_BRIDGE/requirements.lock"
[ -f "${LOCKFILE}" ] || die "payload has no IBKR_PAPER_BRIDGE/requirements.lock"
[ -f "${SOURCE_DIR}/IBKR_PAPER_BRIDGE/bridge/app.py" ] || die "payload has no bridge/app.py"
LOCK_VERIFY="${SOURCE_DIR}/IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py"
[ -f "${LOCK_VERIFY}" ] || die "payload has no offline lock verifier"
"${MTC_PYTHON}" "${LOCK_VERIFY}" --lock "${LOCKFILE}" \
  || die "requirements.lock is not exact and fully hashed"
ENV_TEMPLATE="${PAYLOAD_DEPLOY_DIR}/env/mtc-bridge.env.template"
FIRST_START_TEMPLATE="${PAYLOAD_DEPLOY_DIR}/systemd/${MTC_FIRST_START_UNIT}.template"
LOGROTATE_TEMPLATE="${PAYLOAD_DEPLOY_DIR}/logrotate/mtc-bridge"
[ -f "${ENV_TEMPLATE}" ] || die "payload has no env contract template"
[ -f "${FIRST_START_TEMPLATE}" ] || die "payload has no first-start unit template"
[ -f "${LOGROTATE_TEMPLATE}" ] || die "payload has no logrotate template"
if grep -qE '^[[:space:]]*(export[[:space:]]+)?[A-Za-z_][A-Za-z0-9_]*=' "${ENV_TEMPLATE}"; then
  die "payload env template contains a definition"
fi

for canonical_path in \
    "${MTC_OPT_ROOT}" "${MTC_RELEASES_ROOT}" "${MTC_VENVS_ROOT}" \
    "${MTC_STATE_DIR}" "${MTC_LOG_DIR}" "${MTC_CONF_DIR}" \
    "${MTC_ENV_FILE}" "${MTC_INSTALL_MANIFEST}" "${MTC_UNIT_DIR}" \
    "${MTC_UNIT_DIR}/${MTC_FIRST_START_UNIT}" "${MTC_LOGROTATE_FILE}" \
    "${DEST}" "$(venv_dir "${RELEASE_SHA}")"; do
  assert_not_symlink "${canonical_path}"
done
if [ -f "${MTC_ENV_FILE}" ] \
   && grep -qE '^[[:space:]]*(export[[:space:]]+)?[A-Za-z_][A-Za-z0-9_]*=' "${MTC_ENV_FILE}"; then
  die "env file already contains definitions; installation/configuration gate forbids secrets"
fi

verify_service_identity() {
  local group_gid user_record user_gid user_home user_shell
  group_gid="$(getent group "${MTC_GROUP}" | awk -F: '{print $3}')"
  user_record="$(getent passwd "${MTC_USER}")"
  [ -n "${group_gid}" ] && [ -n "${user_record}" ] || die "service identity is incomplete"
  user_gid="$(printf '%s\n' "${user_record}" | awk -F: '{print $4}')"
  user_home="$(printf '%s\n' "${user_record}" | awk -F: '{print $6}')"
  user_shell="$(printf '%s\n' "${user_record}" | awk -F: '{print $7}')"
  [ "${user_gid}" = "${group_gid}" ] || die "existing service user has the wrong primary group"
  [ "${user_home}" = "${MTC_STATE_DIR}" ] || die "existing service user has the wrong home"
  case "${user_shell}" in
    */nologin|*/false) : ;;
    *) die "existing service user has a login shell" ;;
  esac
  if id -nG "${MTC_USER}" | tr ' ' '\n' | grep -qxE 'sudo|admin|docker|adm|systemd-journal'; then
    die "existing service user belongs to a privileged group"
  fi
}

dry_run_action() {
  printf '[dry-run] ACTION %-20s %s\n' "$1" "$2"
}

print_dry_run_manifest() {
  dry_run_action "identity-group" "ensure system group ${MTC_GROUP}"
  dry_run_action "identity-user" "ensure nologin user ${MTC_USER} with home ${MTC_STATE_DIR}"
  dry_run_action "dir-state" "ensure ${MTC_STATE_DIR} owner ${MTC_USER}:${MTC_GROUP} mode 0750"
  dry_run_action "dir-log" "ensure ${MTC_LOG_DIR} owner ${MTC_USER}:${MTC_GROUP} mode 0750"
  dry_run_action "dir-config" "ensure ${MTC_CONF_DIR} owner root:root mode 0750"
  dry_run_action "dir-opt" "ensure ${MTC_OPT_ROOT} owner root:root mode 0755"
  dry_run_action "dir-releases" "ensure ${MTC_RELEASES_ROOT} owner root:root mode 0755"
  dry_run_action "dir-venvs" "ensure ${MTC_VENVS_ROOT} owner root:root mode 0755"
  dry_run_action "release-dir" "create ${DEST} owner root:root mode 0755 if absent"
  dry_run_action "release-copy" "copy accepted payload ${SOURCE_DIR}/. to ${DEST}/ if absent"
  dry_run_action "venv-create" "create Python 3.12 venv ${VENV} if absent"
  if [ -n "${WHEELHOUSE}" ]; then
    dry_run_action "venv-install" "install hash-locked wheels into ${VENV} from ${WHEELHOUSE}"
  else
    dry_run_action "venv-install" "install hash-locked binary wheels into ${VENV} from package index"
  fi
  dry_run_action "seal-release-owner" "recursively set ${DEST} owner root:root"
  dry_run_action "seal-release-dirs" "recursively set directories under ${DEST} mode 0555"
  dry_run_action "seal-release-exec" "recursively set executable files under ${DEST} mode 0555"
  dry_run_action "seal-release-files" "recursively set non-executable files under ${DEST} mode 0444"
  dry_run_action "seal-venv-owner" "recursively set ${VENV} owner root:root"
  dry_run_action "seal-venv-dirs" "recursively set directories under ${VENV} mode 0555"
  dry_run_action "seal-venv-exec" "recursively set executable files under ${VENV} mode 0555"
  dry_run_action "seal-venv-files" "recursively set non-executable files under ${VENV} mode 0444"
  dry_run_action "env-install" "create ${MTC_ENV_FILE} from names-only template if absent, root:root mode 0600"
  dry_run_action "env-owner" "set ${MTC_ENV_FILE} owner root:root"
  dry_run_action "env-mode" "set ${MTC_ENV_FILE} mode 0600"
  dry_run_action "unit-dir" "ensure ${MTC_UNIT_DIR} owner root:root mode 0755"
  dry_run_action "unit-install" "render release ${RELEASE_SHA} and install ${MTC_UNIT_DIR}/${MTC_FIRST_START_UNIT} root:root mode 0644"
  dry_run_action "systemd-reload" "run systemctl daemon-reload"
  dry_run_action "unit-mask" "mask ${MTC_FIRST_START_UNIT} via ${MTC_MASK_DIR}/${MTC_FIRST_START_UNIT}"
  dry_run_action "logrotate-install" "install ${MTC_LOGROTATE_FILE} root:root mode 0644"
  dry_run_action "manifest-write" "write hash-only install manifest ${MTC_INSTALL_MANIFEST}"
  dry_run_action "manifest-owner" "set ${MTC_INSTALL_MANIFEST} owner root:root"
  dry_run_action "manifest-mode" "set ${MTC_INSTALL_MANIFEST} mode 0640"
}

if [ "${MTC_DRY_RUN}" = "1" ]; then
  MTC_FAILURES=0
  if getent group "${MTC_GROUP}" >/dev/null \
     || getent passwd "${MTC_USER}" >/dev/null; then
    verify_service_identity
  fi
  assert_ufw_bridge_safe || true
  assert_control_port_closed || true
  assert_loopback_only_source "${SOURCE_DIR}/IBKR_PAPER_BRIDGE/bridge/app.py" || true
  if pgrep -f '[b]ridge\.app' >/dev/null 2>&1; then
    fail "a bridge.app process already exists on the target host"
  fi
  [ "${MTC_FAILURES}" -eq 0 ] || die "${MTC_FAILURES} dry-run boundary assertion(s) failed"
  print_dry_run_manifest
  log "dry-run PASS for ${RELEASE_SHA}; complete mutation manifest printed above"
  log "NOT started, NOT enabled, NO secret provisioned, NO firewall change."
  exit 0
fi

# --------------------------------------------------------------------------
# 2. dedicated non-login service identity (idempotent)
# --------------------------------------------------------------------------
if getent group "${MTC_GROUP}" >/dev/null; then
  log "group ${MTC_GROUP} already present"
else
  run groupadd --system "${MTC_GROUP}"
fi
if getent passwd "${MTC_USER}" >/dev/null; then
  log "user ${MTC_USER} already present"
  verify_service_identity
else
  run useradd --system --gid "${MTC_GROUP}" \
      --home-dir "${MTC_STATE_DIR}" --no-create-home \
      --shell /usr/sbin/nologin \
      --comment "MTC Crypto Paper Bridge service account" "${MTC_USER}"
fi

verify_service_identity

# --------------------------------------------------------------------------
# 3. writable state / log / config directories
# --------------------------------------------------------------------------
run install -d -o "${MTC_USER}" -g "${MTC_GROUP}" -m 0750 "${MTC_STATE_DIR}"
run install -d -o "${MTC_USER}" -g "${MTC_GROUP}" -m 0750 "${MTC_LOG_DIR}"
run install -d -o root -g root -m 0750 "${MTC_CONF_DIR}"
run install -d -o root -g root -m 0755 "${MTC_OPT_ROOT}"
run install -d -o root -g root -m 0755 "${MTC_RELEASES_ROOT}"
run install -d -o root -g root -m 0755 "${MTC_VENVS_ROOT}"

# --------------------------------------------------------------------------
# 4. immutable release tree
# --------------------------------------------------------------------------
if [ -d "${DEST}" ]; then
  log "release ${RELEASE_SHA} already materialised; re-verifying in place"
  [ "$(sha256_of "${DEST}/RELEASE_SHA256SUMS")" = "${MANIFEST_SHA256}" ] \
    || die "installed release manifest hash differs from the accepted artifact"
  ( cd "${DEST}" && sha256sum --strict --quiet -c RELEASE_SHA256SUMS ) \
    || die "installed release failed checksum verification; refusing to continue"
else
  log "materialising release ${RELEASE_SHA}"
  run install -d -o root -g root -m 0755 "${DEST}"
  run cp -a "${SOURCE_DIR}/." "${DEST}/"
fi
MTC_FAILURES=0
assert_exact_payload_tree "${DEST}" || true
[ "${MTC_FAILURES}" -eq 0 ] || die "installed release file inventory verification failed"

# --------------------------------------------------------------------------
# 5. hash-locked Python 3.12 virtual environment
# --------------------------------------------------------------------------
if [ -x "${VENV}/bin/python" ]; then
  log "venv already present; verifying exact installed distribution set"
  "${VENV}/bin/python" "${DEST}/IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py" \
      --lock "${DEST}/IBKR_PAPER_BRIDGE/requirements.lock" --check-installed \
    || die "existing venv does not exactly match requirements.lock"
else
  log "creating venv with ${MTC_PYTHON}"
  run "${MTC_PYTHON}" -m venv "${VENV}"
  PIP_ARGS=(
    "${VENV}/bin/python" -m pip install
    --require-hashes --no-deps
    --only-binary=:all:
    --no-input --no-cache-dir --disable-pip-version-check
    -r "${DEST}/IBKR_PAPER_BRIDGE/requirements.lock"
  )
  if [ -n "${WHEELHOUSE}" ]; then
    [ -d "${WHEELHOUSE}" ] || die "wheelhouse directory not found"
    log "installing fully offline from wheelhouse"
    PIP_ARGS+=(--no-index --find-links "${WHEELHOUSE}")
  fi
  # No `pip install --upgrade pip`: that would be an unpinned, unhashed network
  # install inside the release we are trying to make reproducible.
  run "${PIP_ARGS[@]}"
  "${VENV}/bin/python" "${DEST}/IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py" \
      --lock "${DEST}/IBKR_PAPER_BRIDGE/requirements.lock" --check-installed \
    || die "new venv does not exactly match requirements.lock"
fi

# --------------------------------------------------------------------------
# 6. make the release root-owned and read-only
# --------------------------------------------------------------------------
log "sealing release tree read-only"
run chown -R root:root "${DEST}"
run find "${DEST}" -type d -exec chmod 0555 {} +
run find "${DEST}" -type f -perm /111 -exec chmod 0555 {} +
run find "${DEST}" -type f '!' -perm /111 -exec chmod 0444 {} +
log "sealing per-SHA venv read-only"
run chown -R root:root "${VENV}"
run find "${VENV}" -type d -exec chmod 0555 {} +
run find "${VENV}" -type f -perm /111 -exec chmod 0555 {} +
run find "${VENV}" -type f '!' -perm /111 -exec chmod 0444 {} +
MTC_FAILURES=0
assert_no_writable_paths "${DEST}" || true
assert_no_writable_paths "${VENV}" || true
[ "${MTC_FAILURES}" -eq 0 ] || die "sealed release or venv remains writable"

# --------------------------------------------------------------------------
# 7. env-file contract — created empty, mode 0600, root-owned, never populated
# --------------------------------------------------------------------------
if [ -f "${MTC_ENV_FILE}" ]; then
  log "env file already present; not read, not modified"
else
  log "creating empty root-owned 0600 env file (no values)"
  run install -o root -g root -m 0600 \
      "${ENV_TEMPLATE}" "${MTC_ENV_FILE}"
fi
run chown root:root "${MTC_ENV_FILE}"
run chmod 0600 "${MTC_ENV_FILE}"

# --------------------------------------------------------------------------
# 8. first-start unit — rendered for the exact SHA, installed MASKED
# --------------------------------------------------------------------------
run install -d -o root -g root -m 0755 "${MTC_UNIT_DIR}"
RENDERED_CONTENT="$(sed "s/@RELEASE_SHA@/${RELEASE_SHA}/g" "${FIRST_START_TEMPLATE}")"
if grep -q '@RELEASE_SHA@' <<< "${RENDERED_CONTENT}"; then
  die "unit template placeholder not substituted"
fi
grep -q '^Restart=no$' <<< "${RENDERED_CONTENT}" || die "rendered first-start unit is not Restart=no"
if grep -q '^\[Install\]' <<< "${RENDERED_CONTENT}"; then
  die "first-start unit must have no [Install] section"
fi

run install -o root -g root -m 0644 \
    <(printf '%s\n' "${RENDERED_CONTENT}") "${MTC_UNIT_DIR}/${MTC_FIRST_START_UNIT}"
UNIT_SHA="$(printf '%s\n' "${RENDERED_CONTENT}" | sha256sum | awk '{print $1}')"

run systemctl daemon-reload
# Masked, never started, never enabled. Starting it later requires an explicit
# `systemctl unmask` performed under the separate KVM2-P4-06 authorization.
run systemctl mask "${MTC_FIRST_START_UNIT}"

if [ "${MTC_DRY_RUN}" != "1" ]; then
  if [ ! -L "${MTC_MASK_DIR}/${MTC_FIRST_START_UNIT}" ] \
     || [ "$(readlink -f "${MTC_MASK_DIR}/${MTC_FIRST_START_UNIT}")" != "/dev/null" ]; then
    die "first-start unit was not masked to /dev/null"
  fi
  if systemctl is-active --quiet "${MTC_FIRST_START_UNIT}"; then
    die "service is active after install; it must never be started here"
  fi
  case "$(systemctl is-enabled "${MTC_FIRST_START_UNIT}" 2>&1 || true)" in
    masked) : ;;
    *) die "first-start unit is not reported masked" ;;
  esac
fi

# --------------------------------------------------------------------------
# 9. log rotation policy
# --------------------------------------------------------------------------
run install -o root -g root -m 0644 "${LOGROTATE_TEMPLATE}" "${MTC_LOGROTATE_FILE}"

# --------------------------------------------------------------------------
# 10. read-only network assertion (never a firewall change)
# --------------------------------------------------------------------------
MTC_FAILURES=0
assert_ufw_bridge_safe || true
assert_control_port_closed || true
assert_loopback_only_source "${DEST}/IBKR_PAPER_BRIDGE/bridge/app.py" || true
if pgrep -f '[b]ridge\.app' >/dev/null 2>&1; then
  fail "a bridge.app process exists after install"
fi
[ "${MTC_FAILURES}" -eq 0 ] || die "${MTC_FAILURES} network/boundary assertion(s) failed"

# --------------------------------------------------------------------------
# 11. install manifest (hashes only; no secret, no payload content)
# --------------------------------------------------------------------------
LOCK_SHA="$(sha256_of "${DEST}/IBKR_PAPER_BRIDGE/requirements.lock")"
if [ "${MTC_DRY_RUN}" != "1" ]; then
  umask 077
  cat > "${MTC_INSTALL_MANIFEST}" <<EOF
{
  "schema_version": "1.0.0",
  "installed_at_utc": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "release_sha": "${RELEASE_SHA}",
  "release_path": "${DEST}",
  "release_manifest_sha256": "${MANIFEST_SHA256}",
  "venv_path": "${VENV}",
  "first_start_unit": "${MTC_FIRST_START_UNIT}",
  "first_start_unit_sha256": "${UNIT_SHA}",
  "first_start_unit_state": "masked",
  "steady_unit_installed": false,
  "requirements_lock_sha256": "${LOCK_SHA}",
  "state_db": "${MTC_STATE_DB}",
  "log_dir": "${MTC_LOG_DIR}",
  "env_file": "${MTC_ENV_FILE}",
  "env_file_populated": false,
  "service_started": false,
  "service_enabled": false,
  "secrets_provisioned": false,
  "firewall_modified": false
}
EOF
  chown root:root "${MTC_INSTALL_MANIFEST}"
  chmod 0640 "${MTC_INSTALL_MANIFEST}"
fi

log "install complete for ${RELEASE_SHA}"
log "unit ${MTC_FIRST_START_UNIT} sha256=${UNIT_SHA} state=masked"
log "NOT started, NOT enabled, NO secret provisioned, NO firewall change."
log "Next gates: KVM2-P4-03 (secrets), P4-04A/P4-05 (quiesce+cutover), P4-06/P4-07 (one DISARMED start)."
