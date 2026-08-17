#!/usr/bin/env bash
# Gate A - A-9 content-redacted secret scan (run-kit D, 2026-08-08)
# Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b (credential-free DISARMED)
#
# AUTHORIZED ONLY FOR THE OWNER-APPROVED PREREGISTERED GATE A RERUN on gatea-staging.
# Recursively scans EXACTLY /opt/mtc-bridge/releases/<SHA> and /etc/mtc-bridge for nine
# pre-registered secret patterns. It does NOT scan the venv or /home/gatea.
#
# Uses `sudo grep -RIlE --binary-files=without-match` so only file PATHS are ever printed
# (never matched text). For each category the grep rc is captured separately: rc 0/1 are
# allowed (0 = match found, 1 = no match); rc > 1 (grep error) fails this script. Any match
# (count > 0) is a FAIL/BLOCK and is never auto-dismissed - the Lead must adjudicate it.
#
# This script does NOT POST /api/arm. It scans bytes under /opt/mtc-bridge/releases/<SHA>
# and /etc/mtc-bridge (which necessarily includes the root-readable env file), but `grep -l`
# prints file PATHS only; no value or matched text is ever printed, copied, or persisted.
# Output is category counts + matched paths only. It writes only the evidence log under /home/gatea.
# Hard exclusions: no credential value, broker/exchange access, successful ARM, order,
# TESTNET/mainnet, wallet, master merge, or economic action. First genuine FAIL stops.
set -Eeuo pipefail

REL="/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b"
ETC="/etc/mtc-bridge"
LOG="/home/gatea/gatea-A9-20260808D.log"
ERRFILE=""

if [[ -e "$LOG" ]]; then
    printf 'ERROR: evidence log already exists (%s); refusing to overwrite\n' "$LOG" >&2
    exit 2
fi

exec > "$LOG" 2>&1

finish() {
    local rc=$?
    if [[ -n "$ERRFILE" && -f "$ERRFILE" ]]; then rm -f "$ERRFILE" || true; fi
    printf '\nA9_TRAP_EXIT rc=%s\n' "$rc"
}
trap finish EXIT

fail() {
    printf 'A9_FAIL reason=%s\n' "$*"
    exit 1
}

echo "A9_SECTION header"
echo "A9_candidate=2ce41e34bceb599d80af24c5c33d835820ec321b"
echo "A9_scan_release=$REL"
echo "A9_scan_etc=$ETC"
echo "A9_scan_excluded=venv and /home/gatea are NOT scanned"
echo "A9_note=content redacted: scans bytes incl. the root-readable env file but grep -l prints PATHS only; no value/matched text printed/copied/persisted; only category counts + paths emitted"

NAMES=(private_key_block aws_access_key github_token slack_token openai_token anthropic_token xai_token telegram_bot_token ethereum_private_key)
ERES=(
'-----BEGIN (RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----'
'AKIA[0-9A-Z]{16}'
'(gh[pousr]_[A-Za-z0-9]{36,255}|github_pat_[A-Za-z0-9_]{50,255})'
'xox[baprs]-[A-Za-z0-9-]{20,}'
'sk-(proj|svcacct)-[A-Za-z0-9_-]{20,}'
'sk-ant-[A-Za-z0-9_-]{20,}'
'xai-[A-Za-z0-9_-]{20,}'
'[0-9]{8,10}:[A-Za-z0-9_-]{35}'
'0x[0-9a-fA-F]{64}'
)

ERRFILE=$(mktemp /home/gatea/gatea-A9-err.XXXXXX) || fail "mktemp failed"
HIT=0

echo "A9_SECTION scan"
i=0
for name in "${NAMES[@]}"; do
    ere="${ERES[$i]}"
    out=""
    rc=0
    # -e marks the ERE as a pattern and -- ends options before the paths, so a pattern
    # that begins with '-' (the private-key block ERE) cannot be parsed as an option.
    if out=$(sudo grep -RIlE --binary-files=without-match -e "$ere" -- "$REL" "$ETC" 2>"$ERRFILE"); then
        rc=0
    else
        rc=$?
    fi
    if [[ -n "$out" ]]; then
        count=$(printf '%s\n' "$out" | wc -l)
    else
        count=0
    fi
    echo "A9_category=$name rc=$rc matches=$count"
    if (( rc > 1 )); then
        echo "A9_grep_error_stderr_begin"
        cat "$ERRFILE" || true
        echo "A9_grep_error_stderr_end"
        fail "grep error for category $name (rc=$rc)"
    fi
    if (( count > 0 )); then
        echo "A9_paths_begin"
        printf '%s\n' "$out"
        echo "A9_paths_end"
        HIT=1
    fi
    i=$((i+1))
done

echo "A9_any_hit=$HIT"
if (( HIT != 0 )); then
    fail "secret-pattern hit(s) detected - FAIL/BLOCK, requires Lead adjudication"
fi

echo "A9_SECTION done"
echo "A-9 PASS"
