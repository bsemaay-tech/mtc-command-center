#!/usr/bin/env bash
#
# package.sh — build the immutable install payload for ONE exact release SHA.
#
# Runs on a trusted build host (never on KVM2, never against a dirty worktree).
# Produces a directory that install.sh can verify without needing git:
#
#   <out>/RELEASE_SHA           the exact 40-hex commit
#   <out>/RELEASE_SHA256SUMS    sha256sum manifest of every payload file
#   <out>/...                   the tree as recorded at that commit
#
# The payload is built from `git archive <sha>`, so an uncommitted or modified
# working file can never leak into a release — the dirty-main-worktree ban is
# structural here, not a convention.
#
# WHAT THIS SCRIPT NEVER DOES
#   * touch a VPS, a service, a secret, the firewall or the exchange;
#   * commit, push, merge, check out, reset or otherwise mutate the repository;
#   * install anything.
#
# Usage:
#   bash ./package.sh --release-sha <40-hex> --repo <repo root> --out <empty dir>
#
# Exit codes: 0 payload built; 1 any precondition failure.

set -Eeuo pipefail
IFS=$'\n\t'

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/common.sh
. "${SCRIPT_DIR}/lib/common.sh"

RELEASE_SHA=""
REPO=""
OUT=""
while [ "$#" -gt 0 ]; do
  case "$1" in
    --release-sha) RELEASE_SHA="${2:-}"; shift 2 ;;
    --repo)        REPO="${2:-}";        shift 2 ;;
    --out)         OUT="${2:-}";         shift 2 ;;
    -h|--help)     sed -n '2,26p' "${BASH_SOURCE[0]}"; exit 1 ;;
    *)             die "unknown argument: $1" ;;
  esac
done

[ -n "${RELEASE_SHA}" ] || die "--release-sha is required"
[ -n "${REPO}" ]        || die "--repo is required"
[ -n "${OUT}" ]         || die "--out is required"
require_release_sha "${RELEASE_SHA}"
require_cmd git tar sha256sum sort realpath cmp mktemp find grep xargs
for gnu_cmd in find sort grep realpath xargs; do
  gnu_version="$("${gnu_cmd}" --version 2>/dev/null)" \
    || die "GNU ${gnu_cmd} is required"
  [[ "${gnu_version}" = *GNU* ]] || die "GNU ${gnu_cmd} is required"
done

git -C "${REPO}" rev-parse --is-inside-work-tree >/dev/null 2>&1 \
  || die "--repo is not a git worktree"
REPO="$(realpath "${REPO}")"
OUT="$(realpath -m "${OUT}")"
case "${OUT}/" in
  "${REPO}/"*) die "--out must be outside the repository worktree" ;;
esac

HEAD_SHA="$(git -C "${REPO}" rev-parse HEAD)"
[ "${HEAD_SHA}" = "${RELEASE_SHA}" ] || die "repo HEAD is not the requested release sha"
git -C "${REPO}" cat-file -e "${RELEASE_SHA}^{commit}" \
  || die "release sha is not a local commit object"
if [ -n "$(git -C "${REPO}" status --porcelain --untracked-files=all)" ]; then
  die "worktree is dirty; a dirty worktree is never a deployment source"
fi

if [ -d "${OUT}" ] && [ -n "$(ls -A "${OUT}" 2>/dev/null)" ]; then
  die "--out must be an empty or non-existent directory"
fi
mkdir -p "${OUT}"

log "exporting ${RELEASE_SHA} via git archive"
# Both line-ending pins are required: the repository's `* text=auto`
# attribute makes core.eol load-bearing.  On Windows, its native default would
# emit CRLF even with core.autocrlf=false.
git -c core.autocrlf=false -c core.eol=lf -c tar.umask=0022 -C "${REPO}" \
  archive --format=tar "${RELEASE_SHA}" | tar -x -C "${OUT}"

TREE_RAW=""
EXPECTED_INVENTORY=""
ACTUAL_INVENTORY=""
CR_INVENTORY=""
cleanup_package_temps() {
  local package_temp
  for package_temp in "${TREE_RAW}" "${EXPECTED_INVENTORY}" \
    "${ACTUAL_INVENTORY}" "${CR_INVENTORY}"; do
    [ -z "${package_temp}" ] || rm -f -- "${package_temp}"
  done
}
trap cleanup_package_temps EXIT
TREE_RAW="$(mktemp)"
EXPECTED_INVENTORY="$(mktemp)"
ACTUAL_INVENTORY="$(mktemp)"
CR_INVENTORY="$(mktemp)"

log "verifying exported inventory and sizes match the release commit"
if ! git -C "${REPO}" ls-tree -rz --long "${RELEASE_SHA}" > "${TREE_RAW}"; then
  die "cannot inventory release commit tree"
fi
: > "${EXPECTED_INVENTORY}"
while IFS= read -r -d '' tree_entry; do
  tree_metadata="${tree_entry%%$'\t'*}"
  tree_path="${tree_entry#*$'\t'}"
  tree_size="${tree_metadata##* }"
  printf '%s\t%s\0' "${tree_size}" "${tree_path}" >> "${EXPECTED_INVENTORY}"
done < "${TREE_RAW}"
if ! (cd "${OUT}" && find . -type f -printf '%s\t%P\0') > "${ACTUAL_INVENTORY}"; then
  die "cannot inventory exported payload files"
fi
LC_ALL=C sort -z -o "${EXPECTED_INVENTORY}" "${EXPECTED_INVENTORY}"
LC_ALL=C sort -z -o "${ACTUAL_INVENTORY}" "${ACTUAL_INVENTORY}"
cmp -s "${EXPECTED_INVENTORY}" "${ACTUAL_INVENTORY}" \
  || die "exported file inventory or sizes differ from release commit tree"

printf '%s\n' "${RELEASE_SHA}" > "${OUT}/RELEASE_SHA"

MTC_FAILURES=0
assert_regular_directory_tree "${OUT}" || true
[ "${MTC_FAILURES}" -eq 0 ] \
  || die "archive contains a symlink or special filesystem entry"

log "verifying LF-only payload files contain no CR bytes"
if ! (
  cd "${OUT}"
  find . -type f -path './IBKR_PAPER_BRIDGE/deploy/linux/*' -print0
) > "${CR_INVENTORY}"; then
  die "cannot inventory LF-required payload files"
fi
DEPLOY_LF_REQUIRED_COUNT=0
while IFS= read -r -d '' payload_file; do
  DEPLOY_LF_REQUIRED_COUNT=$((DEPLOY_LF_REQUIRED_COUNT + 1))
done < "${CR_INVENTORY}"
if ! (
  cd "${OUT}"
  find . -type f -name '*.sh' \
    ! -path './IBKR_PAPER_BRIDGE/deploy/linux/*' -print0
) >> "${CR_INVENTORY}"; then
  die "cannot inventory LF-required payload files"
fi
LF_REQUIRED_COUNT=0
while IFS= read -r -d '' payload_file; do
  LF_REQUIRED_COUNT=$((LF_REQUIRED_COUNT + 1))
  if LC_ALL=C grep -qU $'\r' "${OUT}/${payload_file#./}"; then
    die "archive contains CR byte in LF-required file: ${payload_file#./}"
  else
    grep_status="$?"
    [ "${grep_status}" -eq 1 ] \
      || die "cannot inspect LF-required file for CR bytes: ${payload_file#./}"
  fi
done < "${CR_INVENTORY}"
[ "${DEPLOY_LF_REQUIRED_COUNT}" -gt 0 ] \
  || die "no deployment LF-required payload files were found to inspect"
[ "${LF_REQUIRED_COUNT}" -gt 0 ] \
  || die "no LF-required payload files were found to inspect"

log "generating RELEASE_SHA256SUMS"
( export LC_ALL=C
  cd "${OUT}"
  find . -type f '!' -name RELEASE_SHA256SUMS -print0 \
     | sort -z \
     | xargs -0 sha256sum > RELEASE_SHA256SUMS )

PAYLOAD_HASH="$(sha256_of "${OUT}/RELEASE_SHA256SUMS")"
log "payload built for ${RELEASE_SHA}"
log "RELEASE_SHA256SUMS sha256=${PAYLOAD_HASH}"
log "Record this hash in the release-candidate manifest before any install attempt."
