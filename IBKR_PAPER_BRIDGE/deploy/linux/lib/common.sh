# shellcheck shell=bash
# Shared, fail-closed helpers for the MTC bridge Linux deployment assets.
#
# Sourced by install.sh / verify.sh / rollback.sh. Contains no action that
# starts, enables or arms a service, provisions a secret, or mutates the
# firewall. Every function either asserts or reports.

# --- canonical, non-negotiable layout --------------------------------------
MTC_USER="mtc-bridge"
MTC_GROUP="mtc-bridge"
MTC_OPT_ROOT="/opt/mtc-bridge"
MTC_RELEASES_ROOT="${MTC_OPT_ROOT}/releases"
MTC_VENVS_ROOT="${MTC_OPT_ROOT}/venvs"
MTC_STATE_DIR="/var/lib/mtc-bridge"
MTC_STATE_DB="${MTC_STATE_DIR}/bridge.db"
MTC_LOG_DIR="/var/log/mtc-bridge"
MTC_CONF_DIR="/etc/mtc-bridge"
MTC_ENV_FILE="${MTC_CONF_DIR}/mtc-bridge.env"
MTC_INSTALL_MANIFEST="${MTC_CONF_DIR}/install_manifest.json"

# Real unit files live in /usr/local/lib so that `systemctl mask` can place its
# /dev/null symlink in /etc/systemd/system without destroying them.
MTC_UNIT_DIR="/usr/local/lib/systemd/system"
MTC_MASK_DIR="/etc/systemd/system"
MTC_FIRST_START_UNIT="mtc-bridge-first-start.service"
MTC_STEADY_UNIT="mtc-bridge-steady.service"

MTC_LOGROTATE_FILE="/etc/logrotate.d/mtc-bridge"
MTC_BIND_HOST="127.0.0.1"
MTC_BIND_PORT="8790"
MTC_PYTHON="python3.12"

MTC_DRY_RUN="${MTC_DRY_RUN:-0}"

# --- output ----------------------------------------------------------------
log()  { printf '[mtc-bridge] %s\n' "$*"; }
pass() { printf 'PASS  %s\n' "$*"; }
fail() { printf 'FAIL  %s\n' "$*" >&2; MTC_FAILURES=$((${MTC_FAILURES:-0} + 1)); }
die()  { printf '[mtc-bridge] FATAL: %s\n' "$*" >&2; exit 1; }

# Every mutating call goes through run() so --dry-run is honoured everywhere.
run() {
  if [ "${MTC_DRY_RUN}" = "1" ]; then
    printf '[dry-run] %s\n' "$*"
    return 0
  fi
  "$@"
}

# --- preconditions ---------------------------------------------------------
require_root() {
  [ "$(id -u)" -eq 0 ] || die "must run as root"
}

require_cmd() {
  for c in "$@"; do
    command -v "$c" >/dev/null 2>&1 || die "required command missing: $c"
  done
}

require_release_sha() {
  [[ "$1" =~ ^[0-9a-f]{40}$ ]] || die "release sha must be exactly 40 lowercase hex characters"
}

release_dir() { printf '%s/%s' "${MTC_RELEASES_ROOT}" "$1"; }
venv_dir() { printf '%s/%s' "${MTC_VENVS_ROOT}" "$1"; }

require_sha256() {
  [[ "$1" =~ ^[0-9a-f]{64}$ ]] || die "sha256 must be exactly 64 lowercase hex characters"
}

assert_not_symlink() {
  local path="$1"
  if [ -L "$path" ]; then
    die "canonical deployment path must not be a symlink: $path"
  fi
}

# --- verification primitives ----------------------------------------------
assert_mode_owner() {
  # assert_mode_owner <path> <expected mode> <expected owner:group>
  local path="$1" want_mode="${2#0}" want_own="$3" got_mode got_own
  if [ ! -e "$path" ]; then fail "missing: $path"; return 1; fi
  got_mode="$(stat -c '%a' "$path")"
  got_own="$(stat -c '%U:%G' "$path")"
  if [ "$got_mode" != "$want_mode" ]; then
    fail "$path mode $got_mode, expected $want_mode"; return 1
  fi
  if [ "$got_own" != "$want_own" ]; then
    fail "$path owner $got_own, expected $want_own"; return 1
  fi
  pass "$path mode $want_mode owner $want_own"
}

assert_no_writable_paths() {
  # The release tree must carry no write bit for anyone.
  local root="$1" offenders
  offenders="$(find "$root" -perm /222 -print -quit 2>/dev/null || true)"
  if [ -n "$offenders" ]; then
    fail "writable path inside immutable release: $offenders"; return 1
  fi
  pass "immutable tree carries no write bit ($root)"
}

assert_regular_directory_tree() {
  # Accepted payloads and installed releases may contain only ordinary
  # directories and regular files. In particular, never let `cp -a` preserve a
  # symlink, device, socket, FIFO or other special entry into a release.
  local root="$1" offender
  if [ ! -d "${root}" ] || [ -L "${root}" ]; then
    fail "payload root is not an ordinary directory: ${root}"; return 1
  fi
  if ! offender="$(find "${root}" -mindepth 1 ! -type d ! -type f -print -quit 2>/dev/null)"; then
    fail "cannot inventory filesystem entry types under ${root}"; return 1
  fi
  if [ -n "${offender}" ]; then
    fail "non-regular filesystem entry inside payload tree: ${offender}"; return 1
  fi
  pass "payload tree contains ordinary directories and regular files only"
}

assert_exact_payload_tree() {
  # Prove that the immutable release contains exactly the files named by the
  # externally hash-bound manifest: no missing files and no injected extras.
  local root="$1" expected actual
  assert_regular_directory_tree "${root}" || return 1
  if [ ! -f "${root}/RELEASE_SHA256SUMS" ]; then
    fail "missing regular RELEASE_SHA256SUMS"; return 1
  fi
  expected="$(mktemp)"
  actual="$(mktemp)"
  if ! sed -E 's/^[0-9a-f]{64} [ *]//' \
      "${root}/RELEASE_SHA256SUMS" | sort > "${expected}"; then
    rm -f "${expected}" "${actual}"
    fail "cannot parse RELEASE_SHA256SUMS"; return 1
  fi
  if ! (cd "${root}" && find . -type f '!' -name RELEASE_SHA256SUMS -print | sort) \
      > "${actual}"; then
    rm -f "${expected}" "${actual}"
    fail "cannot inventory release tree"; return 1
  fi
  if ! cmp -s "${expected}" "${actual}"; then
    rm -f "${expected}" "${actual}"
    fail "release file inventory differs from RELEASE_SHA256SUMS"; return 1
  fi
  rm -f "${expected}" "${actual}"
  pass "release file inventory exactly matches RELEASE_SHA256SUMS"
}

# Read-only UFW assertion. This function NEVER changes a firewall rule; a
# firewall change is a separately scoped, separately audited, owner-approved
# action (KVM2 invariant 8).
assert_ufw_ssh_only() {
  if ! command -v ufw >/dev/null 2>&1; then
    fail "ufw not installed; SSH-only inbound policy cannot be asserted"; return 1
  fi
  local status
  status="$(ufw status verbose 2>/dev/null || true)"
  case "$status" in
    *"Status: active"*) : ;;
    *) fail "ufw is not active"; return 1 ;;
  esac
  case "$status" in
    *"Default: deny (incoming)"*) : ;;
    *) fail "ufw default incoming policy is not deny"; return 1 ;;
  esac
  # Any ALLOW IN rule for a port other than 22 fails closed.
  local bad
  bad="$(printf '%s\n' "$status" \
    | awk '/ALLOW IN/ { print $1 }' \
    | grep -Ev '^(22|22/tcp|22/udp|OpenSSH)$' || true)"
  if [ -n "$bad" ]; then
    fail "ufw allows non-SSH inbound: $(printf '%s' "$bad" | tr '\n' ' ')"; return 1
  fi
  case "$status" in
    *"${MTC_BIND_PORT}"*) fail "ufw mentions port ${MTC_BIND_PORT}; control plane must stay loopback-only"; return 1 ;;
  esac
  pass "ufw active, default-deny inbound, SSH-only"
}

# Static proof that the shipped application binds loopback only.
assert_loopback_only_source() {
  local app_py="$1"
  [ -f "$app_py" ] || { fail "missing application entrypoint"; return 1; }
  if ! grep -q "host=\"${MTC_BIND_HOST}\", port=${MTC_BIND_PORT}" "$app_py"; then
    fail "entrypoint does not bind ${MTC_BIND_HOST}:${MTC_BIND_PORT}"; return 1
  fi
  if grep -qE '0\.0\.0\.0|host="::"' "$app_py"; then
    fail "entrypoint contains a non-loopback bind address"; return 1
  fi
  pass "entrypoint binds ${MTC_BIND_HOST}:${MTC_BIND_PORT} only"
}

# If anything is listening on the control port it must be loopback-only.
assert_no_public_control_listener() {
  if ! command -v ss >/dev/null 2>&1; then
    fail "ss not available; listener state cannot be asserted"; return 1
  fi
  local bad
  bad="$(ss -H -ltn 2>/dev/null | awk -v p=":${MTC_BIND_PORT}" \
        '$4 ~ p && $4 !~ /^127\.0\.0\.1:/ && $4 !~ /^\[::1\]:/ { print $4 }' || true)"
  if [ -n "$bad" ]; then
    fail "non-loopback listener on control port: $bad"; return 1
  fi
  pass "no non-loopback listener on ${MTC_BIND_PORT}"
}

assert_control_port_closed() {
  if ! command -v ss >/dev/null 2>&1; then
    fail "ss not available; closed control port cannot be asserted"; return 1
  fi
  local listeners
  listeners="$(ss -H -ltn 2>/dev/null | awk -v p=":${MTC_BIND_PORT}" '$4 ~ p { print $4 }' || true)"
  if [ -n "${listeners}" ]; then
    fail "control port ${MTC_BIND_PORT} still has a listener"; return 1
  fi
  pass "control port ${MTC_BIND_PORT} is closed"
}

sha256_of() { sha256sum "$1" | awk '{print $1}'; }
