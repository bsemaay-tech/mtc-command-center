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
require_cmd git tar sha256sum sort realpath

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
git -C "${REPO}" archive --format=tar "${RELEASE_SHA}" | tar -x -C "${OUT}"

printf '%s\n' "${RELEASE_SHA}" > "${OUT}/RELEASE_SHA"

MTC_FAILURES=0
assert_regular_directory_tree "${OUT}" || true
[ "${MTC_FAILURES}" -eq 0 ] \
  || die "archive contains a symlink or special filesystem entry"

log "generating RELEASE_SHA256SUMS"
( cd "${OUT}" \
  && find . -type f '!' -name RELEASE_SHA256SUMS -print0 \
     | sort -z \
     | xargs -0 sha256sum > RELEASE_SHA256SUMS )

PAYLOAD_HASH="$(sha256_of "${OUT}/RELEASE_SHA256SUMS")"
log "payload built for ${RELEASE_SHA}"
log "RELEASE_SHA256SUMS sha256=${PAYLOAD_HASH}"
log "Record this hash in the release-candidate manifest before any install attempt."
