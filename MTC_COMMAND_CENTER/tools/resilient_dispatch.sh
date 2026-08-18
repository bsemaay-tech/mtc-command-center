#!/usr/bin/env bash
# resilient_dispatch.sh — network-resilient wrapper for Codex/Claude CLI dispatches.
#
# Why this exists: on 2026-07-31 a mains->generator switchover dropped DNS mid-run.
# A `codex exec` implementer dispatch burned 120k tokens, exhausted 5 WebSocket and
# 5 HTTPS reconnects, and returned nothing. Power transitions on this site are
# expected to keep doing that.
#
# What it does:
#   1. Waits for real connectivity before starting (not just an interface being up).
#   2. Runs the dispatch.
#   3. On a network-class failure that produced NO output, waits and retries with
#      backoff, up to MAX_ATTEMPTS.
#   4. On a CONFIRMED Codex account quota / rate-limit exhaustion, switches once —
#      one way — to the secondary Codex profile and re-runs the identical argv and
#      prompt with CODEX_HOME pointed at it. See "Account failover" below.
#
# What it deliberately REFUSES to do:
#   - It never retries if the target worktree became dirty. A partially-applied
#     implementer edit must be inspected by the Lead, never re-run blindly: a second
#     pass over already-edited files can double-apply a change and silently corrupt
#     the artifact that a Gate-5 audit is about to freeze.
#   - It never touches Git. All commits/pushes/merges stay with the Lead.
#   - It never reads, copies, or logs credential contents. The secondary profile is
#     validated by existence/readability of <home>/auth.json only.
#   - It never migrates an already-running dispatch. A switch can only affect the
#     NEXT attempt.
#
# Account failover (conservative, one-way, at most once per run):
#   Triggered only when ALL of these hold for one attempt:
#     - the dispatched command is `codex` (argv[0] basename),
#     - it exited nonzero,
#     - it produced NO final-message output,
#     - the worktree is still clean,
#     - the log matches CODEX_QUOTA_PATTERN,
#     - the log does NOT match CODEX_NET_PATTERN (a network-class failure always
#       wins: generic connectivity errors keep the existing same-account backoff),
#     - no failover has happened yet in this run,
#     - the caller is not already running on the secondary profile.
#   Secondary profile: CODEX_SECONDARY_HOME, default ~/.codex-hesap2.
#   If it is missing or unusable the wrapper FAILS CLOSED (exit 5) rather than
#   hammering the exhausted account.
#
# Usage:
#   resilient_dispatch.sh <worktree> <prompt_file> <out_file> <log_file> <cmd...>
#
# Example:
#   resilient_dispatch.sh C:/WPS prompt.md last.md full.log \
#     codex exec -C C:/WPS -s workspace-write -m gpt-5.6-sol \
#       -c model_reasoning_effort=xhigh -c 'approval_policy="never"'
#
# Exit codes: 0 success · 2 dirty worktree, manual inspection required
#             3 attempts exhausted · 4 bad usage
#             5 quota exhaustion confirmed but secondary Codex profile unusable

set -uo pipefail

MAX_ATTEMPTS="${MAX_ATTEMPTS:-5}"
NET_WAIT_MAX_S="${NET_WAIT_MAX_S:-1800}"   # give a generator/mains transition 30 min
PROBE_URL="${PROBE_URL:-https://chatgpt.com}"

# Secondary Codex subscription. Account 1 stays the default; this is only ever used
# after a confirmed quota/rate-limit exhaustion of the account the caller started on.
CODEX_SECONDARY_HOME="${CODEX_SECONDARY_HOME:-$HOME/.codex-hesap2}"

# Deliberately narrow. A pattern that is merely "an error happened" must NOT be here:
# a false positive burns the reserve account for free.
CODEX_QUOTA_PATTERN="${CODEX_QUOTA_PATTERN:-usage limit reached|(hit|reached) (your|the) usage limit|usage limit for|quota (exceeded|exhausted)|insufficient_quota|exceeded your current quota|out of (credits|quota)|(hit|reached|exceeded) (your|the) rate limit|rate[ _-]?limit(ed)? (exceeded|reached)|too many requests|(http|https|status|code|error)[^0-9]{0,12}429}"

# Network-class failures veto a failover: they are what the backoff loop already
# exists for, and switching accounts would not help.
CODEX_NET_PATTERN="${CODEX_NET_PATTERN:-getaddrinfo|enotfound|econnreset|econnrefused|etimedout|ehostunreach|enetunreach|epipe|socket hang up|connection (reset|refused|timed out|closed)|network is unreachable|temporary failure in name resolution|name resolution|tls handshake|handshake fail|stream (disconnected|closed) before|websocket|proxy error|ssl}"

if [ "$#" -lt 5 ]; then
  echo "usage: $0 <worktree> <prompt_file> <out_file> <log_file> <cmd...>" >&2
  exit 4
fi

WORKTREE="$1"; PROMPT="$2"; OUT="$3"; LOG="$4"; shift 4

log() { printf '[%s] %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*" | tee -a "$LOG.dispatch"; }

# Real connectivity, not just a link light. Any HTTP status means DNS + TCP + TLS work.
net_up() { curl -s -o /dev/null --max-time 15 "$PROBE_URL" 2>/dev/null; }

wait_for_net() {
  local waited=0 backoff=10
  while ! net_up; do
    if [ "$waited" -ge "$NET_WAIT_MAX_S" ]; then
      log "network still down after ${waited}s; giving up"
      return 1
    fi
    log "network down; sleeping ${backoff}s (waited ${waited}s)"
    sleep "$backoff"; waited=$((waited + backoff))
    [ "$backoff" -lt 120 ] && backoff=$((backoff * 2))
  done
  [ "$waited" -gt 0 ] && log "network back after ${waited}s"
  return 0
}

worktree_dirty() {
  [ -n "$(git -C "$WORKTREE" status --porcelain -uno 2>/dev/null)" ]
}

# A dispatch counts as productive if it wrote a non-empty final-message file.
produced_output() { [ -s "$OUT" ]; }

if worktree_dirty; then
  log "REFUSING TO START: $WORKTREE already has uncommitted changes."
  log "Commit or inspect them first — this wrapper must never run on top of an unreviewed edit."
  exit 2
fi

for attempt in $(seq 1 "$MAX_ATTEMPTS"); do
  wait_for_net || exit 3
  log "attempt $attempt/$MAX_ATTEMPTS: $*"
  rm -f "$OUT"
  "$@" < "$PROMPT" > "$LOG" 2>&1
  rc=$?

  if produced_output; then
    log "attempt $attempt produced output (rc=$rc); done"
    exit 0
  fi

  if worktree_dirty; then
    log "attempt $attempt produced NO output but LEFT THE WORKTREE DIRTY (rc=$rc)."
    log "STOPPING for Lead inspection — a blind retry could double-apply a partial edit."
    exit 2
  fi

  log "attempt $attempt produced no output and no edits (rc=$rc); treating as a lost run"
  tail -c 600 "$LOG" | tr -d '\000' | sed 's/^/    | /' | tee -a "$LOG.dispatch"
  sleep $((attempt * 30))
done

log "all $MAX_ATTEMPTS attempts exhausted with no output"
exit 3
