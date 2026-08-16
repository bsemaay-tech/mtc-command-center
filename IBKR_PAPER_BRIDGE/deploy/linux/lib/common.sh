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
MTC_LOGROTATE_CRON="/etc/cron.hourly/mtc-bridge-logrotate"
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

preflight_venv_capability() {
  if ! PYTHONDONTWRITEBYTECODE=1 "${MTC_PYTHON}" -c 'import venv, ensurepip' \
      >/dev/null 2>&1; then
    die "${MTC_PYTHON} cannot import venv and ensurepip; install Ubuntu package python3.12-venv before retrying"
  fi
  pass "${MTC_PYTHON} venv/ensurepip capability available"
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
  #                   [expected numeric uid:gid] [file|directory]
  local path="$1" want_mode="${2#0}" want_own="$3"
  local want_numeric="${4:-}" want_kind="${5:-}" got_mode got_own got_numeric
  if [ ! -e "$path" ]; then fail "missing: $path"; return 1; fi
  if [ -L "$path" ]; then fail "symlink not allowed: $path"; return 1; fi
  case "${want_kind}" in
    "") : ;;
    file) [ -f "$path" ] || { fail "not a regular file: $path"; return 1; } ;;
    directory) [ -d "$path" ] || { fail "not a directory: $path"; return 1; } ;;
    *) fail "invalid metadata kind ${want_kind}: $path"; return 1 ;;
  esac
  if ! got_mode="$(stat -c '%a' "$path")"; then
    fail "cannot read mode: $path"; return 1
  fi
  if ! got_own="$(stat -c '%U:%G' "$path")"; then
    fail "cannot read owner: $path"; return 1
  fi
  if [ -n "${want_numeric}" ]; then
    if ! got_numeric="$(stat -c '%u:%g' "$path")"; then
      fail "cannot read numeric owner: $path"; return 1
    fi
  fi
  if [ "$got_mode" != "$want_mode" ]; then
    fail "$path mode $got_mode, expected $want_mode"; return 1
  fi
  if [ "$got_own" != "$want_own" ]; then
    fail "$path owner $got_own, expected $want_own"; return 1
  fi
  if [ -n "${want_numeric}" ] && [ "$got_numeric" != "$want_numeric" ]; then
    fail "$path numeric owner $got_numeric, expected $want_numeric"; return 1
  fi
  pass "$path mode $want_mode owner $want_own${want_numeric:+ numeric $want_numeric}"
}

assert_no_writable_paths() {
  # The release tree must carry no write bit for anyone.
  local root="$1" offenders
  if ! offenders="$(find "$root" ! -type l -perm /222 -print -quit 2>/dev/null)"; then
    fail "cannot inventory writable paths under $root"; return 1
  fi
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
  if ! expected="$(sed -E 's/^[0-9a-f]{64} [ *]//' \
      "${root}/RELEASE_SHA256SUMS" | sort)"; then
    fail "cannot parse RELEASE_SHA256SUMS"; return 1
  fi
  if ! actual="$(cd "${root}" \
      && find . -type f '!' -name RELEASE_SHA256SUMS -print | sort)"; then
    fail "cannot inventory release tree"; return 1
  fi
  if ! cmp -s <(printf '%s\n' "${expected}") <(printf '%s\n' "${actual}"); then
    fail "release file inventory differs from RELEASE_SHA256SUMS"; return 1
  fi
  pass "release file inventory exactly matches RELEASE_SHA256SUMS"
}

# Read-only UFW assertion. This function NEVER changes a firewall rule; a
# firewall change is a separately scoped, separately audited, owner-approved
# action (KVM2 invariant 8).
assert_ufw_bridge_safe() {
  if ! command -v ufw >/dev/null 2>&1; then
    fail "ufw not installed; Bridge-safe inbound policy cannot be asserted"; return 1
  fi
  local status parsed ssh_allow bridge_allow
  if ! status="$(ufw status verbose 2>/dev/null)"; then
    fail "ufw status cannot be read"; return 1
  fi
  case "$status" in
    *"Status: active"*) : ;;
    *) fail "ufw is not active"; return 1 ;;
  esac
  case "$status" in
    *"Default: deny (incoming)"*) : ;;
    *) fail "ufw default incoming policy is not deny"; return 1 ;;
  esac
  # Parse every status-table row. ALLOW/LIMIT rules admitting inbound or
  # forwarded traffic use one exposure grammar; DENY/REJECT rules and explicit
  # outbound rules do not admit inbound traffic. A numeric port may be the first
  # field or may follow a destination address; exact ports and inclusive a:b
  # ranges are supported. Anything else is not evidence of safety: application
  # profiles and unmodelled grammar must be replaced with explicit numeric
  # port/range rules before this assertion can pass.
  if ! parsed="$(printf '%s\n' "${status}" | awk -v bridge_port="${MTC_BIND_PORT}" '
    function trim(value) {
      sub(/^[[:space:]]+/, "", value)
      sub(/[[:space:]]+$/, "", value)
      return value
    }
    function source_is_modelled(value) {
      return value == "Anywhere" || value ~ /^[0-9A-Fa-f:.]+(\/[0-9]+)?$/
    }
    function parse_port_spec(value, parts, range_parts, count) {
      count = split(value, parts, "/")
      if (count > 2 || parts[1] == "") return 0
      parsed_protocol = count == 2 ? tolower(parts[2]) : ""
      if (parsed_protocol != "" && parsed_protocol != "tcp" && parsed_protocol != "udp") return 0
      if (parts[1] ~ /^[0-9]+$/) {
        parsed_low = parts[1] + 0
        parsed_high = parsed_low
      } else if (parts[1] ~ /^[0-9]+:[0-9]+$/) {
        split(parts[1], range_parts, ":")
        parsed_low = range_parts[1] + 0
        parsed_high = range_parts[2] + 0
      } else {
        return 0
      }
      return parsed_low >= 1 && parsed_high <= 65535 && parsed_low <= parsed_high
    }
    function mark_unmodelled(reason, rule) {
      print "UNMODELLED\t" reason "\t" rule
      unmodelled = 1
    }
    /^[[:space:]]*--[[:space:]]/ { in_rules = 1; next }
    in_rules && /^[[:space:]]*$/ { next }
    in_rules {
      rule = $0
      # A single trailing rule comment ("22/tcp ... # SSH") is ordinary UFW status
      # output and is annotation, not grammar. Strip only that comment, before any
      # field handling, so the source/destination fields stay modelled.
      sub(/[[:space:]]+#[^\n]*$/, "", rule)
      if (match(rule, /[[:space:]]+(DENY|REJECT)[[:space:]]+(IN|FWD)[[:space:]]+/)) {
        next
      }
      if (match(rule, /[[:space:]]+(ALLOW|LIMIT|DENY|REJECT)[[:space:]]+OUT[[:space:]]+/)) {
        next
      }
      if (!match(rule, /[[:space:]]+(ALLOW|LIMIT)[[:space:]]+(IN|FWD)[[:space:]]+/)) {
        mark_unmodelled("rule action/direction is not a modelled inbound UFW status verb", rule)
        next
      }
      destination = trim(substr(rule, 1, RSTART - 1))
      source = trim(substr(rule, RSTART + RLENGTH))
      sub(/[[:space:]]+\(v6\)$/, "", destination)
      sub(/[[:space:]]+\(v6\)$/, "", source)
      destination = trim(destination)
      source = trim(source)
      if (!source_is_modelled(source)) {
        mark_unmodelled("source field is not an explicit address", rule)
        next
      }

      field_count = split(destination, fields, /[[:space:]]+/)
      if (field_count >= 3 && fields[field_count - 1] == "on") {
        if (fields[field_count] !~ /^[[:alnum:]_.:-]+$/) {
          mark_unmodelled("interface field is invalid", rule)
          next
        }
        field_count -= 2
      }
      if (field_count == 1 && fields[1] == "Anywhere") {
        print "BRIDGE\t" rule
        next
      }
      if (field_count == 1) {
        port_spec = fields[1]
      } else if (field_count == 2 && source_is_modelled(fields[1])) {
        port_spec = fields[2]
      } else {
        mark_unmodelled("destination is not an explicit numeric port/range", rule)
        next
      }
      if (!parse_port_spec(port_spec)) {
        mark_unmodelled("port field is not an explicit numeric port/range", rule)
        next
      }
      if (parsed_low <= bridge_port && bridge_port <= parsed_high) {
        print "BRIDGE\t" rule
      }
      if (parsed_low <= 22 && 22 <= parsed_high && (parsed_protocol == "" || parsed_protocol == "tcp")) {
        print "SSH\t" rule
      }
    }
    END { if (unmodelled) exit 2 }
  ')"; then
    fail "ufw has an unmodelled inbound rule or application profile; enumerate it as an explicit numeric port/range before Bridge verification: $(printf '%s' "${parsed}" | tr '\n' ' ')"
    return 1
  fi
  bridge_allow="$(printf '%s\n' "${parsed}" | awk -F '\t' '$1 == "BRIDGE" { print $2 }')"
  if [ -n "${bridge_allow}" ]; then
    fail "ufw exposes Bridge port ${MTC_BIND_PORT}: $(printf '%s' "${bridge_allow}" | tr '\n' ' ')"; return 1
  fi
  # Independent substring backstop: if a future parser edit silently skips an
  # inbound non-deny row containing the literal Bridge port, absence of parsed
  # BRIDGE output still cannot become a clean conclusion.
  bridge_allow="$(printf '%s\n' "${status}" | awk -v bridge_port="${MTC_BIND_PORT}" '
    /^[[:space:]]*--[[:space:]]/ { in_rules = 1; next }
    in_rules {
      # Same single trailing rule comment is stripped here, so a comment can
      # neither hide a port field nor forge a DENY/OUT skip. The scan still runs
      # over the whole remaining row, port fields included.
      rule = $0
      sub(/[[:space:]]+#[^\n]*$/, "", rule)
      if (!index(rule, bridge_port)) next
      if (rule ~ /[[:space:]]+(DENY|REJECT)[[:space:]]+(IN|FWD)[[:space:]]/) next
      if (rule ~ /[[:space:]]+(ALLOW|LIMIT|DENY|REJECT)[[:space:]]+OUT[[:space:]]/) next
      print
    }
  ')"
  if [ -n "${bridge_allow}" ]; then
    fail "ufw inbound substring backstop found Bridge port ${MTC_BIND_PORT}: $(printf '%s' "${bridge_allow}" | tr '\n' ' ')"; return 1
  fi
  ssh_allow="$(printf '%s\n' "${parsed}" | awk -F '\t' '$1 == "SSH" { print; exit }')"
  if [ -z "${ssh_allow}" ]; then
    fail "ufw has no inbound ALLOW/LIMIT rule for numeric SSH port 22/tcp"; return 1
  fi
  pass "ufw active, default-deny incoming; SSH port 22 allowed; Bridge port ${MTC_BIND_PORT} not exposed"
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
