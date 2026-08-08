#!/usr/bin/env python3
"""Local D026 regression test for the Gate A A-5 post-start readiness repair (revision E).

Usage:
    python test_gatea_A5_readiness.py --script <path/to/gatea_A5.sh>

What this proves
----------------
DEFECT 1 - the readiness race (run-kit D).  D's ``gatea_A5.sh`` gated its post-start
assertions on systemd ``ActiveState=active`` alone (``retry 30 wait_active``), so the post
listener assertion could fire before the application had bound ``127.0.0.1:8790``.  That is
the reproduced 2026-08-09 A-5 FAIL (``listener_count=0`` -> ``A5_FAIL reason=post listener
not loopback-only``, trap ``rc=1``) on a service that was in fact healthy moments later.

DEFECT 2 - the false wall-clock bound (first E draft, Lead finding 2026-08-09, repair round
1).  The first repair used ``retry 30 post_start_ready`` and described it as a 30 s ceiling.
``retry`` counts ATTEMPTS, not seconds: ``check_api``'s
``urllib.request.urlopen(..., timeout=10)`` can block ten seconds inside one attempt and
``retry`` then sleeps another second, so a listener-present / API-stalled service could keep
that wait running for roughly 330 seconds while the marker asserted a 30 s ceiling.  The
original regression stubs returned immediately, so they could not see it.

Revision E must therefore wait, after the single explicit ``systemctl start`` and before the
final post assertions, on a REAL MONOTONIC WALL-CLOCK DEADLINE that

    * is satisfied only when all three of these hold in the SAME attempt --
        1. systemd ``ActiveState=active``                              (``wait_active``)
        2. a nonempty loopback-only ``:8790`` listener set             (``check_listener_loopback_only``)
        3. ``GET /api/status`` HTTP 200 + exact credential-free DISARMED (``check_api``)
    * charges probe duration AND inter-attempt backoff against one budget read from a
      monotonic clock, and
    * hard-bounds every attempt by the REMAINING budget, so a blocked probe is terminated at
      the deadline instead of extending it.

This test verifies that contract STRUCTURALLY and, decisively, BEHAVIOURALLY.  It extracts
the script's REAL readiness constants and REAL shell function definitions and executes them
against local stubs, including a stub readiness probe that blocks far longer than the test
deadline.  Two scenarios form the D026 falsification pair, run on every invocation with
identical stubs and an identical nominal bound:

    mutation_pre_repair_attempt_count_wait_violates_deadline
        the VERBATIM pre-repair wait (the script's own ``retry`` helper driving the old
        ``post_start_ready``) blows straight through its nominal bound, and

    behaviour_repaired_deadline_beats_pre_repair_on_same_stub
        the repaired wait, same stubs, same nominal bound, returns nonzero at the deadline
        in a fraction of that time.

A third scenario blocks a probe for far longer than any test deadline and then proves the
probe process is GONE afterwards - the deadline terminates the probe, it does not wait it out.

Safety
------
Local-only test artifact.  It is NEVER executed on gatea-staging and it never executes the
Gate-A script -- ``bash -n`` parses without running, and the behavioural harness runs only
the extracted function definitions.  It never invokes ``systemctl``, ``sudo``, ``ss``,
``journalctl``, ``ssh``, ``scp``, the installed Bridge venv Python, any network call, or any
staging action: those names are shadowed BOTH by exported harness functions AND by executable
shims placed first on ``PATH`` (so even a process that does not inherit shell functions cannot
reach the real command).  Every shim appends to a private log file that the harness reports,
so a forbidden call cannot be swallowed by the readiness path's diagnostics suppression.  All
harness state lives in a private temporary directory that is removed afterwards.

Environment guard (repair round 2)
----------------------------------
The script under test resolves its own deadline guard with ``TIMEOUT_BIN="$(command -v timeout
|| true)"`` and proves it in step1 with a BASH child -- a Bash PATH lookup on the machine that
runs the script.  This test therefore asks the SAME question of the SAME shell: the guard is
resolved and exercised INSIDE the selected Bash, over the same ``bash -s`` transport the
behavioural harness uses.  Asking Python instead (``shutil.which("timeout")``) asked WINDOWS
where ``timeout`` is, and on a canonical Windows workstation Windows answers
``C:\\Windows\\system32\\timeout.EXE`` -- an unrelated console-pause command that cannot bound
a child -- so the environment check failed while the mechanism it was checking worked, and the
documented default command could only be made to pass by prepending a directory to ``PATH`` by
hand (Lead finding, 2026-08-09).  No ``PATH`` override is required, requested or accepted, and
a Windows ``timeout.EXE`` is never accepted as the guard.

Exit code
---------
0 = every check passed (GREEN).  Nonzero = at least one check failed (RED).
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

# Names of the existing run-kit checks the readiness wait must reuse.
ACTIVE_FN = "wait_active"
LISTENER_FN = "check_listener_loopback_only"
API_FN = "check_api"
REQUIRED_READY_CHECKS = (ACTIVE_FN, LISTENER_FN, API_FN)

# The wall-clock deadline the preregistration requires, in seconds.
REQUIRED_READY_DEADLINE_S = 30

# Sentinels around the script's readiness constants; the block is lifted VERBATIM into the
# behavioural harness so the test cannot drift from the real values.
CONSTS_BEGIN = "E READINESS DEADLINE CONSTANTS (BEGIN"
CONSTS_END = "E READINESS DEADLINE CONSTANTS (END"

# Embedded Python heredoc marker used by every run-kit script.
HEREDOC_MARKER = "PYEOF"

FORBIDDEN_MARKER = "GATEA_TEST_FORBIDDEN"

# Claims retired by repair round 1.  Any of these surviving anywhere in the script means the
# source still asserts the attempt-count bound the Lead falsified.
RETIRED_FALSE_CLAIMS = (
    "ready_max_wait_s",
    "30 s maximum",
    "30-second maximum",
    "30 attempts",
)

FUNC_OPEN_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*\(\)\s*\{\s*$")
START_CMD_RE = re.compile(r"^\s*sudo\s+systemctl\s+start\s")
RETRY_CALL_RE = re.compile(r"(?:^|[^\w.])retry\s+(\d+)\s+([A-Za-z_][A-Za-z0-9_]*)")
SLEEP_LITERAL_RE = re.compile(r"^\s*sleep\s+[0-9.]+\s*$")
WORD_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
RUN_BOUNDED_CALL_RE = re.compile(r"run_bounded\s+\"\$(\w+)\"\s+(\w+)")

# --------------------------------------------------------------------------------------
# behavioural scenario constants
# --------------------------------------------------------------------------------------
# All deadlines below are TEST-ONLY values handed to the real wait function; the production
# value (REQUIRED_READY_DEADLINE_S) is asserted structurally instead, so the test never has
# to sit through a 30 s wait.
TEST_DEADLINE_S = 3          # short deadline for the timeout/termination scenarios
TEST_LONG_DEADLINE_S = 12    # comfortable deadline for the delayed-success case
READY_AT_ATTEMPT = 3         # attempt on which the delayed-success stubs become ready
SLOW_PROBE_S = 45            # a readiness probe that blocks far beyond any test deadline

# The D026 falsification pair: identical stubs, identical nominal bound, one run driven by
# the verbatim pre-repair attempt-count wait and one by the repaired deadline wait.
AB_BOUND = 2                 # seconds for the repaired wait / attempts for the old wait
AB_SLOW_PROBE_S = 8          # per-attempt block; > AB_BOUND so the old wait must overrun

# Tolerance budget for every "at or below the deadline" assertion.  Named sources only:
#   + 2 s  KILL_GRACE_S - the bounded SIGTERM -> SIGKILL escalation a probe that ignores
#          SIGTERM is allowed to add.  This is the script's own honest tolerance.
#   + 1 s  coarse-clock rounding: on a host without /proc/uptime the script's mono_now_ds()
#          falls back to $SECONDS, whose resolution is one second.
#   + 3 s  python subprocess spawn, bash startup/teardown, one child shell per attempt, and
#          ordinary process-scheduling slop.
# Nothing else is absorbed here: the pre-repair overrun this pair detects is ~8x the bound.
DEADLINE_TOLERANCE_S = 6

# The VERBATIM pre-repair readiness function (first E draft / Lead-audited source).  It is
# kept here, not read from disk, so the falsification survives the repair that deleted it.
PRE_REPAIR_POST_START_READY = """post_start_ready() {
    wait_active || return 1
    check_listener_loopback_only >/dev/null 2>&1 || return 1
    check_api >/dev/null 2>&1 || return 1
    return 0
}"""

# Fallback only: the script under test normally still defines this attempt-count helper (D
# uses it for the cheap dead-window wait), and the real one is preferred for fidelity.
PRE_REPAIR_RETRY_FALLBACK = """retry() {
    local tries="$1" fn="$2"; shift 2
    local i=0
    while (( i < tries )); do
        if "$fn" "$@"; then return 0; fi
        i=$((i+1)); sleep 1
    done
    return 1
}"""

# Negative control: the SAME real deadline wait driving an active-only probe. The probe's
# real name is substituted in, so the control overrides whatever the script actually calls.
SYNTHETIC_ACTIVE_ONLY_PROBE_TMPL = """%s() {
    wait_active || return 1
    return 0
}"""


# --------------------------------------------------------------------------------------
# script parsing
# --------------------------------------------------------------------------------------
def read_script_lines(path):
    """Return the script as a list of LF-normalised lines.

    The shipped kit member is LF-only, but a Windows checkout of this repo can present
    tracked ``.sh`` files with CRLF; normalising here keeps both the structural checks and
    the behavioural extraction correct in either case.
    """
    with open(path, "rb") as handle:
        raw = handle.read()
    text = raw.decode("utf-8")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text.split("\n")


def parse_functions(lines):
    """Map top-level shell function name -> {start, end, body}."""
    funcs = {}
    index = 0
    total = len(lines)
    while index < total:
        match = FUNC_OPEN_RE.match(lines[index])
        if match:
            for end in range(index + 1, total):
                if lines[end] == "}":
                    funcs[match.group(1)] = {
                        "start": index,
                        "end": end,
                        "body": lines[index:end + 1],
                    }
                    index = end
                    break
        index += 1
    return funcs


def extract_heredocs(lines, marker=HEREDOC_MARKER):
    """Return [(open_line_index, close_line_index, text)] for each <<'MARKER' block."""
    open_re = re.compile(r"<<'%s'\s*$" % re.escape(marker))
    blocks = []
    index = 0
    total = len(lines)
    while index < total:
        if open_re.search(lines[index]):
            for end in range(index + 1, total):
                if lines[end].strip() == marker:
                    blocks.append((index, end, "\n".join(lines[index + 1:end])))
                    index = end
                    break
        index += 1
    return blocks


def extract_constants_block(lines):
    """Return (text, error) for the verbatim readiness-constants block."""
    begin = end = None
    for i, line in enumerate(lines):
        if begin is None and CONSTS_BEGIN in line:
            begin = i
        elif begin is not None and CONSTS_END in line:
            end = i
            break
    if begin is None or end is None:
        return None, ("no readiness-constants block delimited by `%s` / `%s` -- the test "
                      "cannot lift the real deadline values" % (CONSTS_BEGIN, CONSTS_END))
    return "\n".join(lines[begin + 1:end]), None


def is_code(line):
    stripped = line.strip()
    return bool(stripped) and not stripped.startswith("#")


def code_body(func):
    return "\n".join(line for line in func["body"] if is_code(line))


def find_explicit_starts(lines):
    return [i for i, line in enumerate(lines) if START_CMD_RE.match(line)]


def find_retry_calls(lines, funcs):
    """Top-level (non-comment, outside the retry definition) `retry <n> <fn>` call sites."""
    retry_def = funcs.get("retry")
    def_range = range(retry_def["start"], retry_def["end"] + 1) if retry_def else range(0)
    calls = []
    for i, line in enumerate(lines):
        if i in def_range or not is_code(line):
            continue
        match = RETRY_CALL_RE.search(line)
        if match:
            calls.append({"line": i, "tries": int(match.group(1)), "fn": match.group(2)})
    return calls


def transitive_refs(funcs, name, depth=5):
    """Every identifier reachable from `name`'s code body, following called functions."""
    seen = set()
    names = set()
    pending = [(name, depth)]
    while pending:
        current, left = pending.pop()
        if current in seen or left < 0:
            continue
        seen.add(current)
        func = funcs.get(current)
        if func is None:
            continue
        for word in WORD_RE.findall(code_body(func)):
            names.add(word)
            if word in funcs and word not in seen:
                pending.append((word, left - 1))
    return names


def find_readiness(lines, funcs):
    """Locate the post-start readiness wait.

    Returns (info, error).  ``error`` is a human-readable reason when the combined-readiness
    contract is absent -- this is the run-kit D case the RED demonstration relies on.
    """
    starts = find_explicit_starts(lines)
    if len(starts) != 1:
        return None, (
            "expected exactly one explicit `sudo systemctl start` command, found %d"
            % len(starts)
        )
    start_line = starts[0]

    # A readiness wait is any function that transitively reaches all three checks.
    candidates = sorted(
        name for name in funcs
        if all(check in transitive_refs(funcs, name) for check in REQUIRED_READY_CHECKS)
    )
    if not candidates:
        return None, (
            "no shell function reaches all three readiness checks (%s) -- systemd-active "
            "alone would satisfy any post-start wait, which is exactly the run-kit D "
            "readiness race" % ", ".join(REQUIRED_READY_CHECKS)
        )

    call = None
    for i in range(start_line + 1, len(lines)):
        if not is_code(lines[i]):
            continue
        words = set(WORD_RE.findall(lines[i]))
        hit = [c for c in candidates if c in words]
        if hit:
            call = {"line": i, "fn": hit[0]}
            break
    if call is None:
        return None, (
            "the explicit start on line %d is not followed by a call to any "
            "combined-readiness function (candidates: %s)"
            % (start_line + 1, ", ".join(candidates))
        )

    return {
        "start_line": start_line,
        "call_line": call["line"],
        "name": call["fn"],
        "body": funcs[call["fn"]]["body"],
    }, None


def find_probe(funcs, ready):
    """The single-attempt probe the deadline wait drives, via its `run_bounded` call."""
    match = RUN_BOUNDED_CALL_RE.search("\n".join(ready["body"]))
    if match and match.group(2) in funcs:
        return match.group(2), match.group(1)
    # No bounded runner: the wait itself is the probe (pre-repair / D shapes).
    return ready["name"], None


# --------------------------------------------------------------------------------------
# behavioural harness
# --------------------------------------------------------------------------------------
HARNESS_TEMPLATE = r"""#!/usr/bin/env bash
# Generated by test_gatea_A5_readiness.py. Exercises the REAL extracted readiness constants
# and function definitions against local stubs. No staging, no network, no systemctl/sudo/ss,
# no Bridge Python.
set -Eeuo pipefail

WORK="$PWD"
ATTEMPTS="$WORK/attempts";                 : > "$ATTEMPTS"
GATEA_FORBIDDEN_LOG="$WORK/forbidden.log"; : > "$GATEA_FORBIDDEN_LOG"
PROBE_PID_FILE="$WORK/probe_pid";          : > "$PROBE_PID_FILE"
export ATTEMPTS GATEA_FORBIDDEN_LOG PROBE_PID_FILE

STUB_ACTIVE_RC=__ACTIVE_RC__
STUB_LISTENER_READY_AT=__LISTENER_READY_AT__
STUB_API_READY_AT=__API_READY_AT__
STUB_API_SLOW_S=__API_SLOW_S__
export STUB_ACTIVE_RC STUB_LISTENER_READY_AT STUB_API_READY_AT STUB_API_SLOW_S

# --- real commands are shadowed twice over --------------------------------------------
# (a) exported shell functions, inherited by every child bash;
# (b) executable shims first on PATH, reached even by a process that inherits no functions.
# Both append to $GATEA_FORBIDDEN_LOG, which the harness reports, so a forbidden call cannot
# be swallowed by the readiness path's per-attempt diagnostics suppression.
_forbid() { printf '__MARKER__ %s\n' "$1" >> "$GATEA_FORBIDDEN_LOG"; exit 97; }
sudo()       { _forbid sudo; }
systemctl()  { _forbid systemctl; }
ss()         { _forbid ss; }
journalctl() { _forbid journalctl; }
curl()       { _forbid curl; }
wget()       { _forbid wget; }
nc()         { _forbid nc; }
sqlite3()    { _forbid sqlite3; }
ssh()        { _forbid ssh; }
scp()        { _forbid scp; }
export -f _forbid sudo systemctl ss journalctl curl wget nc sqlite3 ssh scp

SHIMDIR="$WORK/forbidden-bin"
mkdir -p "$SHIMDIR"
for _c in sudo systemctl ss journalctl curl wget nc sqlite3 ssh scp; do
    cat > "$SHIMDIR/$_c" <<SHIMEOF
#!/bin/sh
printf '__MARKER__ %s\n' "$_c" >> "\$GATEA_FORBIDDEN_LOG"
exit 97
SHIMEOF
    chmod +x "$SHIMDIR/$_c"
done
PATH="$SHIMDIR:$PATH"
export PATH

PY="$WORK/forbidden-bridge-python"
DB="$WORK/forbidden-state-db"
UNIT="gatea-test-not-a-real-unit"
export PY DB UNIT

_bump()     { printf 'x\n' >> "$ATTEMPTS"; }
_attempts() { wc -l < "$ATTEMPTS" | tr -d ' '; }
export -f _bump _attempts

# stub 1: systemd ActiveState -- silent, like the real wait_active. Counts the attempt,
# because the readiness probe calls it first on every attempt. The counter is a FILE, so it
# is shared with the bounded child shell the repaired wait spawns per attempt.
wait_active() { _bump; return "$STUB_ACTIVE_RC"; }
# safety net only: the enforced contract is that readiness delegates its active check to
# wait_active, so this is not the counted seam.
getprop() {
    case "$1" in
        ActiveState) if [[ "$STUB_ACTIVE_RC" == "0" ]]; then printf 'active\n'; else printf 'activating\n'; fi ;;
        *) printf '\n' ;;
    esac
}

# stub 2: :8790 loopback listener -- absent until attempt STUB_LISTENER_READY_AT (0 = never)
check_listener_loopback_only() {
    local n; n=$(_attempts)
    if (( STUB_LISTENER_READY_AT > 0 )) && (( n >= STUB_LISTENER_READY_AT )); then
        printf 'ss_rc=0\nlistener_count=1\nnonloopback_addrs=\nRESULT=PASS\n'
        return 0
    fi
    printf 'ss_rc=0\nlistener_count=0\nnonloopback_addrs=\nRESULT=FAIL\n'
    return 1
}

# stub 3: the API probe.
# STUB_API_SLOW_S > 0 models the defect the Lead found: a reachable listener with a stalled
# application, where the real check_api sits in urllib.request.urlopen(..., timeout=10). The
# blocking child's PID is recorded so the harness can prove afterwards that the deadline
# TERMINATED it rather than waiting it out.
check_api() {
    local n sp
    n=$(_attempts)
    if (( STUB_API_SLOW_S > 0 )); then
        sleep "$STUB_API_SLOW_S" &
        sp=$!
        printf '%s\n' "$sp" > "$PROBE_PID_FILE"
        wait "$sp" 2>/dev/null || true
        printf 'RESULT=FAIL api_read_error: stub_slow_probe\n'
        return 1
    fi
    if (( STUB_API_READY_AT > 0 )) && (( n >= STUB_API_READY_AT )); then
        printf 'api_http_status=200\napi_state=DISARMED\napi_mode=credential_free_disarmed\nRESULT=PASS\n'
        return 0
    fi
    printf 'RESULT=FAIL api_read_error: stub_not_ready\n'
    return 1
}
export -f wait_active getprop check_listener_loopback_only check_api

# --- readiness constants, extracted VERBATIM from the script under test ----------------
__CONSTS__
# --- function definitions, extracted VERBATIM from the script under test ---------------
__FUNCS__
# --- optional control override ---------------------------------------------------------
__OVERRIDE__
# ---------------------------------------------------------------------------------------
__EXPORTS__

_t0=$SECONDS
if __TARGET_CALL__; then _rc=0; else _rc=1; fi
_t1=$SECONDS
sleep 1   # let any signalled probe child finish dying before the survivor test
printf 'HARNESS_rc=%s\n' "$_rc"
printf 'HARNESS_attempts=%s\n' "$(_attempts)"
printf 'HARNESS_elapsed=%s\n' "$(( _t1 - _t0 ))"
printf 'HARNESS_forbidden=%s\n' "$(wc -l < "$GATEA_FORBIDDEN_LOG" | tr -d ' ')"
if [[ -s "$PROBE_PID_FILE" ]]; then
    _pp=$(cat "$PROBE_PID_FILE")
    printf 'HARNESS_probe_pid=%s\n' "$_pp"
    if kill -0 "$_pp" 2>/dev/null; then
        printf 'HARNESS_probe_survivor=yes\n'
        kill -KILL "$_pp" 2>/dev/null || true
    else
        printf 'HARNESS_probe_survivor=no\n'
    fi
else
    printf 'HARNESS_probe_pid=none\n'
    printf 'HARNESS_probe_survivor=none\n'
fi
exit 0
"""


def find_bash(explicit=None):
    if explicit:
        return explicit
    found = shutil.which("bash")
    if found:
        return found
    for candidate in (
        r"C:\Program Files\Git\bin\bash.exe",
        r"C:\Program Files\Git\usr\bin\bash.exe",
        "/bin/bash",
        "/usr/bin/bash",
    ):
        if os.path.exists(candidate):
            return candidate
    return None


# --------------------------------------------------------------------------------------
# deadline guard probe -- resolved and exercised INSIDE the selected bash
# --------------------------------------------------------------------------------------
# The script under test resolves its own guard as `TIMEOUT_BIN="$(command -v timeout || true)"`
# and proves it in step1 with
#     "$TIMEOUT_BIN" --signal=TERM --kill-after="$KILL_GRACE_S" 0.5 "${BASH:-bash}" -c 'sleep 30'
# -- a BASH PATH lookup driving a BASH child, on the machine that runs the script. This probe
# asks exactly that question of exactly that shell.
#
# Repair round 2 (Lead finding, 2026-08-09). Asking Python instead -- shutil.which("timeout") --
# asked WINDOWS where `timeout` is, and on a canonical Windows workstation Windows answers
# C:/Windows/system32/timeout.EXE: an unrelated console-pause command that cannot bound a child
# and exits 1. Meanwhile the behavioural scenarios were running GNU coreutils `timeout` happily
# through the selected Bash's own PATH, so the environment check failed while the mechanism it
# was checking worked, and the documented default command could be made to pass only by
# prepending a directory to PATH by hand. No PATH override is required, requested or accepted.
#
# The probe deliberately uses the SAME transport as run_harness(): `bash -s` with the script fed
# on stdin, non-login and non-interactive. A login shell could source a profile that adds
# directories the harness's own child shells never see, which would certify a PATH the test does
# not actually run under.
GUARD_SCRIPT = r"""
set -u
_bin=$(command -v timeout 2>/dev/null || true)
printf 'GUARD_bin=%s\n' "${_bin:-none}"
if [[ -z "${_bin:-}" ]]; then
    printf 'GUARD_version=none\n'
    printf 'GUARD_version_rc=127\n'
    printf 'GUARD_kill_rc=127\n'
    exit 0
fi
# </dev/null on every child: this shell is reading its own script from stdin, so no child may
# be left able to consume it.
_vout=$("$_bin" --version </dev/null 2>&1)
_vrc=$?
printf 'GUARD_version_rc=%s\n' "$_vrc"
printf 'GUARD_version=%s\n' "$(printf '%s\n' "$_vout" | head -1 | tr -d '\r')"
"$_bin" --signal=TERM --kill-after=2 0.5 "${BASH:-bash}" -c 'sleep 30' </dev/null >/dev/null 2>&1
printf 'GUARD_kill_rc=%s\n' "$?"
exit 0
"""

# GNU coreutils identifies itself: `timeout --version` -> "timeout (GNU coreutils) 8.32".
GNU_GUARD_TOKEN = "coreutils"

# Windows ships an unrelated console-pause `timeout.EXE` in its system directory. It is never a
# valid deadline guard and is rejected explicitly, whatever a PATH lookup returned. Both spellings
# are matched: the native `C:\Windows\system32\...` and the MSYS `/c/Windows/system32/...` form.
WINDOWS_TIMEOUT_RE = re.compile(r"[\\/](?:[A-Za-z][\\/])?windows[\\/]system32[\\/]", re.I)


def probe_deadline_guard(bash_exe):
    """Resolve and exercise the GNU coreutils deadline guard inside `bash_exe`.

    Returns ``(metrics, error)``: the ``GUARD_*`` key=value lines the probe printed, and a
    human-readable reason when the probe could not be executed at all.  Nothing is swallowed --
    a probe that cannot run is reported and the check goes RED (D025 rule 1).
    """
    try:
        proc = subprocess.run(
            [bash_exe, "-s"],
            input=GUARD_SCRIPT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=120,
        )
    except Exception as exc:  # noqa: BLE001 - reported, never swallowed
        return {}, "the deadline-guard probe could not be executed under %s: %r" % (
            bash_exe, exc)
    metrics = {}
    for line in (proc.stdout or "").splitlines():
        if line.startswith("GUARD_"):
            key, _, value = line.partition("=")
            metrics[key] = value.strip()
    if "GUARD_bin" not in metrics:
        return metrics, (
            "the deadline-guard probe produced no GUARD_bin line under %s (rc=%s stderr=%r)"
            % (bash_exe, proc.returncode, (proc.stderr or "").strip()[:200]))
    return metrics, None


def run_harness(bash_exe, consts, funcs_text, exports, target_call, active_rc,
                listener_ready_at, api_ready_at, api_slow_s, override="",
                proc_timeout=180):
    """Execute the harness in a private temp dir; return (proc, metrics, wall_seconds)."""
    script = (HARNESS_TEMPLATE
              .replace("__ACTIVE_RC__", str(active_rc))
              .replace("__LISTENER_READY_AT__", str(listener_ready_at))
              .replace("__API_READY_AT__", str(api_ready_at))
              .replace("__API_SLOW_S__", str(api_slow_s))
              .replace("__CONSTS__", consts)
              .replace("__FUNCS__", funcs_text)
              .replace("__OVERRIDE__", override)
              .replace("__EXPORTS__", exports)
              .replace("__TARGET_CALL__", target_call)
              .replace("__MARKER__", FORBIDDEN_MARKER))
    work = tempfile.mkdtemp(prefix="gatea_a5_readiness_")
    started = time.monotonic()
    timed_out = False
    try:
        # bash reads the harness from stdin (`-s`) with cwd = the temp dir, so no host
        # path is ever interpolated into the shell text.
        proc = subprocess.run(
            [bash_exe, "-s"],
            input=script,
            cwd=work,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=proc_timeout,
        )
    except subprocess.TimeoutExpired as exc:
        # A harness that never returns is itself a failure signal: the deadline scenarios
        # exist precisely to bound this. Surface it as a failed run, never as a pass.
        timed_out = True
        out = exc.stdout
        if isinstance(out, bytes):
            out = out.decode("utf-8", "replace")
        proc = subprocess.CompletedProcess(
            args=[bash_exe, "-s"], returncode=-9, stdout=out or "",
            stderr="HARNESS EXCEEDED THE PYTHON-LEVEL TIMEOUT OF %ss" % proc_timeout)
    finally:
        wall = time.monotonic() - started
        shutil.rmtree(work, ignore_errors=True)
    metrics = {}
    for line in (proc.stdout or "").splitlines():
        if line.startswith("HARNESS_"):
            key, _, value = line.partition("=")
            metrics[key] = value.strip()
    # The harness sleeps one second before the survivor test; charge that back so the
    # deadline assertions measure the wait, not the harness's own settling delay.
    if not timed_out:
        wall = max(0.0, wall - 1.0)
    metrics["_timed_out"] = "yes" if timed_out else "no"
    return proc, metrics, wall


def describe(proc, metrics, wall):
    return "exit=%s wall=%.1fs %s stderr=%r" % (
        proc.returncode,
        wall,
        " ".join("%s=%s" % (k, v) for k, v in sorted(metrics.items()) if k != "_timed_out")
        or "<no metrics>",
        (proc.stderr or "").strip()[:300],
    )


# --------------------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------------------
def main(argv=None):
    parser = argparse.ArgumentParser(
        description="D026 regression test for the Gate A A-5 post-start readiness repair")
    parser.add_argument("--script", required=True, help="path to gatea_A5.sh under test")
    parser.add_argument("--bash", default=None, help="explicit bash executable (optional)")
    args = parser.parse_args(argv)

    script_path = os.path.abspath(args.script)
    if not os.path.isfile(script_path):
        print("ERROR: script not found: %s" % script_path)
        return 2

    bash_exe = find_bash(args.bash)
    if not bash_exe:
        print("ERROR: no bash executable found; cannot run the behavioural checks")
        return 2

    lines = read_script_lines(script_path)
    funcs = parse_functions(lines)
    text = "\n".join(lines)
    consts, consts_error = extract_constants_block(lines)
    ready, ready_error = find_readiness(lines, funcs)

    results = []

    def record(name, ok, detail):
        results.append((name, bool(ok), detail))

    print("GATEA_A5_READINESS_TEST script=%s" % script_path)
    print("bash=%s" % bash_exe)
    print("script_lines=%d functions=%s" % (len(lines), ",".join(sorted(funcs))))
    print("")

    # --- environment: the deadline guard must really work here -----------------------
    # D025 rule 1: a check that cannot be executed is never acceptance. The guard is resolved
    # and exercised INSIDE the selected bash -- the same shell, the same `command -v timeout`
    # lookup and the same bash child the script under test uses in step1 -- so this certifies
    # the mechanism the real run depends on, needs no PATH override, and can never be satisfied
    # by Windows' unrelated system32 `timeout.EXE`. If GNU coreutils `timeout` is missing, is
    # not GNU, or does not terminate a blocked child, the test goes RED rather than reporting a
    # green it did not earn.
    guard, guard_error = probe_deadline_guard(bash_exe)
    guard_bin = guard.get("GUARD_bin", "none")
    guard_version = guard.get("GUARD_version", "none")
    guard_version_rc = guard.get("GUARD_version_rc", "none")
    guard_kill_rc = guard.get("GUARD_kill_rc", "none")
    guard_is_windows = bool(WINDOWS_TIMEOUT_RE.search(guard_bin))
    record(
        "env_deadline_guard_available_and_working",
        guard_error is None
        and guard_bin not in ("none", "")
        and not guard_is_windows
        and guard_version_rc == "0"
        and GNU_GUARD_TOKEN in guard_version.lower()
        and guard_kill_rc == "124",
        guard_error or (
            "resolved through the selected bash, exactly as the script's own TIMEOUT_BIN is, "
            "with no PATH override: `command -v timeout` -> %s (windows_system32=%s, never "
            "accepted as a deadline guard); `timeout --version` rc=%s -> %r (must identify GNU "
            "%s); `timeout --signal=TERM --kill-after=2 0.5 bash -c 'sleep 30'` rc=%s (124 "
            "required: the guard must terminate a blocked child)"
            % (guard_bin, guard_is_windows, guard_version_rc, guard_version, GNU_GUARD_TOKEN,
               guard_kill_rc)),
    )

    # --- static checks on the script under test --------------------------------------
    # `bash -n` PARSES ONLY; it never executes the Gate-A script.
    syntax = subprocess.run(
        [bash_exe, "-n", os.path.basename(script_path)],
        cwd=os.path.dirname(script_path),
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    record(
        "static_bash_n_syntax_ok",
        syntax.returncode == 0,
        "bash -n rc=%s stderr=%r" % (syntax.returncode, (syntax.stderr or "").strip()[:300]),
    )

    blocks = extract_heredocs(lines)
    compile_errors = []
    for open_i, _close_i, block_text in blocks:
        try:
            compile(block_text + "\n",
                    "<%s:%s@line%d>" % (os.path.basename(script_path), HEREDOC_MARKER,
                                        open_i + 1),
                    "exec")
        except SyntaxError as exc:
            compile_errors.append("line %d: %s" % (open_i + 1, exc))
    record(
        "static_embedded_python_heredocs_compile",
        len(blocks) >= 1 and not compile_errors,
        "<<'%s' blocks=%d at lines %s; compile errors=%s"
        % (HEREDOC_MARKER, len(blocks), [o + 1 for o, _c, _t in blocks],
           compile_errors or "none"),
    )

    # --- structural checks -----------------------------------------------------------
    starts = find_explicit_starts(lines)
    record(
        "structure_exactly_one_explicit_start",
        len(starts) == 1,
        "explicit `sudo systemctl start` command lines: %s"
        % ([i + 1 for i in starts] or "none"),
    )

    record(
        "structure_deadline_constants_block",
        consts is not None
        and re.search(r"^READY_MAX_S=%d$" % REQUIRED_READY_DEADLINE_S, consts or "",
                      re.M) is not None
        and re.search(r"^KILL_GRACE_S=\d+$", consts or "", re.M) is not None
        and re.search(r"^READY_POLL_S=\d+$", consts or "", re.M) is not None
        and "TIMEOUT_BIN=" in (consts or "")
        and "/proc/uptime" in (consts or ""),
        consts_error or "verbatim constants block: %r"
        % ("; ".join(l.strip() for l in (consts or "").splitlines()
                     if is_code(l))[:300],),
    )

    retry_after_start = ([] if not starts else
                         [c for c in find_retry_calls(lines, funcs) if c["line"] > starts[0]])
    record(
        "structure_no_attempt_count_retry_after_start",
        not retry_after_start,
        "attempt-count `retry <n> <fn>` call sites after the explicit start (the falsified "
        "bound; must be none): %s"
        % ([("line %d: retry %d %s" % (c["line"] + 1, c["tries"], c["fn"]))
            for c in retry_after_start] or "none"),
    )

    probe_name = probe_arg = None
    if ready is not None:
        probe_name, probe_arg = find_probe(funcs, ready)
    ready_body_text = "\n".join(ready["body"]) if ready else ""
    ready_code_lines = [l for l in (ready["body"] if ready else []) if is_code(l)]

    if ready is None:
        for name in (
            "structure_wall_clock_deadline_wait_after_start",
            "structure_readiness_requires_active_listener_and_api",
            "structure_deadline_uses_monotonic_clock",
            "structure_every_attempt_hard_bounded_by_remaining",
            "structure_backoff_never_literal_in_deadline_wait",
            "structure_final_post_assertions_after_readiness",
            "structure_no_fixed_sleep_as_readiness_proof",
        ):
            record(name, False, ready_error)
    else:
        record(
            "structure_wall_clock_deadline_wait_after_start",
            "READY_MAX_S" in lines[ready["call_line"]],
            "line %d calls `%s` after the explicit start on line %d; it must be handed the "
            "wall-clock constant READY_MAX_S, not an attempt count -- call line: %r"
            % (ready["call_line"] + 1, ready["name"], ready["start_line"] + 1,
               lines[ready["call_line"]].strip()[:200]),
        )

        probe_body = "\n".join(funcs[probe_name]["body"]) if probe_name in funcs else ""
        short_circuits = [
            any(name in line and "return 1" in line
                for line in funcs.get(probe_name, {}).get("body", []))
            for name in REQUIRED_READY_CHECKS
        ]
        record(
            "structure_readiness_requires_active_listener_and_api",
            all(short_circuits) and bool(probe_body),
            "probe `%s` short-circuits to `return 1` for: %s" % (
                probe_name,
                ", ".join("%s=%s" % (n, "yes" if ok else "NO")
                          for n, ok in zip(REQUIRED_READY_CHECKS, short_circuits))),
        )

        mono = funcs.get("mono_now_ds")
        mono_body = "\n".join(mono["body"]) if mono else ""
        record(
            "structure_deadline_uses_monotonic_clock",
            "mono_now_ds" in ready_body_text and bool(mono)
            and "/proc/uptime" in mono_body,
            "`%s` reads its clock from mono_now_ds=%s; mono_now_ds defined=%s, uses "
            "/proc/uptime=%s (CLOCK_BOOTTIME: never steps backwards on an NTP/clock change)"
            % (ready["name"], "mono_now_ds" in ready_body_text, bool(mono),
               "/proc/uptime" in mono_body),
        )

        runner = funcs.get("run_bounded")
        runner_body = "\n".join(runner["body"]) if runner else ""
        derived = bool(probe_arg) and any(
            re.match(r"\s*%s=\$\(\(.*-.*\)\)" % re.escape(probe_arg), l)
            for l in ready_code_lines)
        record(
            "structure_every_attempt_hard_bounded_by_remaining",
            bool(runner) and bool(probe_arg) and derived
            and "TIMEOUT_BIN" in runner_body and "--kill-after" in runner_body
            and "KILL_GRACE_S" in runner_body,
            "`%s` runs each attempt as `run_bounded \"$%s\" %s`; $%s is derived from a "
            "remaining-time subtraction=%s; run_bounded uses $TIMEOUT_BIN=%s "
            "--kill-after=%s $KILL_GRACE_S=%s"
            % (ready["name"], probe_arg, probe_name, probe_arg, derived,
               "TIMEOUT_BIN" in runner_body, "--kill-after" in runner_body,
               "KILL_GRACE_S" in runner_body),
        )

        literal_sleeps = [l.strip() for l in ready_code_lines if SLEEP_LITERAL_RE.match(l)]
        var_sleeps = [l.strip() for l in ready_code_lines
                      if l.strip().startswith("sleep ") and not SLEEP_LITERAL_RE.match(l)]
        record(
            "structure_backoff_never_literal_in_deadline_wait",
            not literal_sleeps and bool(var_sleeps),
            "inside `%s`: fixed-literal sleeps=%s (must be none, they cannot be clamped to "
            "the remaining deadline); remaining-derived/constant sleeps=%s"
            % (ready["name"], literal_sleeps or "none", var_sleeps or "none"),
        )

        tail_text = "\n".join(lines[i] for i in range(ready["call_line"] + 1, len(lines))
                              if is_code(lines[i]))
        final_listener = LISTENER_FN in tail_text
        final_api = API_FN in tail_text
        record(
            "structure_final_post_assertions_after_readiness",
            final_listener and final_api,
            "after the readiness wait (line %d): %s=%s %s=%s"
            % (ready["call_line"] + 1, LISTENER_FN, final_listener, API_FN, final_api),
        )

        between = lines[ready["start_line"] + 1:ready["call_line"]]
        bare_sleeps = [l.strip() for l in between if SLEEP_LITERAL_RE.match(l)]
        record(
            "structure_no_fixed_sleep_as_readiness_proof",
            not bare_sleeps,
            "bare `sleep N` lines between the explicit start and the readiness wait: %s"
            % (bare_sleeps or "none"),
        )

    marker_lines = [l for l in lines if "A5_READY=yes" in l]
    marker = marker_lines[0] if marker_lines else ""
    required_marker_tokens = (
        "ready_bound=monotonic_wall_clock_deadline",
        "ready_deadline_s=$READY_MAX_S",
        "ready_kill_grace_s=$KILL_GRACE_S",
        "ready_clock=$MONO_CLOCK",
        "ready_second_start=none",
    )
    missing_marker = [t for t in required_marker_tokens if t not in marker]
    record(
        "structure_marker_states_truthful_deadline_contract",
        len(marker_lines) == 1 and not missing_marker,
        "A5_READY marker lines=%d; missing tokens=%s"
        % (len(marker_lines), missing_marker or "none"),
    )

    surviving_claims = [c for c in RETIRED_FALSE_CLAIMS if c in text]
    record(
        "structure_no_retired_false_bound_claim",
        not surviving_claims,
        "retired attempt-count/ceiling claims still present in the source: %s"
        % (surviving_claims or "none"),
    )

    api_blocks = [t for _o, _c, t in blocks if "urllib" in t]
    record(
        "structure_final_check_api_timeout_preserved",
        any("timeout=10" in t for t in api_blocks),
        "final unsuppressed check_api keeps its own urllib timeout=10 (readiness bounding "
        "must not weaken the final evidence): urllib heredocs=%d, timeout=10 present=%s"
        % (len(api_blocks), any("timeout=10" in t for t in api_blocks)),
    )

    guard_keys = ("A5_ready_clock=", "A5_timeout_bin=", "A5_timeout_guard_rc=",
                  "A5_ready_probe_export_rc=")
    missing_keys = [k for k in guard_keys if k not in text]
    guard_fails = [l.strip() for l in lines
                   if "fail \"precondition" in l
                   and any(w in l for w in ("deadline guard", "monotonic clock",
                                            "readiness probe functions", "timeout"))]
    record(
        "structure_deadline_guard_preconditions_present",
        not missing_keys and len(guard_fails) >= 4,
        "step1 must prove the deadline is real before depending on it: missing evidence "
        "keys=%s; guard/clock/transport precondition failures=%d"
        % (missing_keys or "none", len(guard_fails)),
    )

    # --- behavioural checks ----------------------------------------------------------
    behaviour_names = (
        "behaviour_delayed_readiness_succeeds_before_deadline",
        "behaviour_deadline_wait_actually_polled",
        "behaviour_readiness_attempt_noise_suppressed",
        "behaviour_deadline_terminates_blocked_probe",
        "behaviour_no_probe_child_survives_deadline",
        "mutation_pre_repair_attempt_count_wait_violates_deadline",
        "behaviour_repaired_deadline_beats_pre_repair_on_same_stub",
        "behaviour_active_only_deadline_expires",
        "behaviour_listener_up_but_api_not_exact_deadline_expires",
        "behaviour_no_forbidden_command_invoked",
        "control_synthetic_active_only_would_have_passed",
    )
    needed = ("mono_now_ds", "run_bounded")
    missing_fns = [n for n in needed if n not in funcs]
    if ready is None or consts is None or missing_fns or probe_name not in funcs:
        reason = (ready_error if ready is None else
                  consts_error if consts is None else
                  "script does not define %s" % ", ".join(missing_fns or [str(probe_name)]))
        for name in behaviour_names:
            record(name, False, "cannot exercise the real definitions: %s" % reason)
    else:
        poll_match = re.search(r"^READY_POLL_S=(\d+)$", consts, re.M)
        poll_s = int(poll_match.group(1)) if poll_match else 1
        wanted = ["mono_now_ds", "run_bounded", probe_name, ready["name"]]
        funcs_text = "\n\n".join(
            "\n".join(funcs[n]["body"]) for n in dict.fromkeys(wanted) if n in funcs)
        exports = "export -f %s" % " ".join(dict.fromkeys(wanted))
        runs = []

        # Scenario A: active immediately; listener + exact API from attempt 3; fast probes.
        # A comfortable deadline, so this proves the wait waits and then succeeds.
        proc_a, met_a, wall_a = run_harness(
            bash_exe, consts, funcs_text, exports,
            '%s %d' % (ready["name"], TEST_LONG_DEADLINE_S),
            active_rc=0, listener_ready_at=READY_AT_ATTEMPT,
            api_ready_at=READY_AT_ATTEMPT, api_slow_s=0)
        runs.append(("delayed_readiness", proc_a, met_a))
        attempts_a = int(met_a.get("HARNESS_attempts", "-1") or -1)
        record(
            "behaviour_delayed_readiness_succeeds_before_deadline",
            proc_a.returncode == 0 and met_a.get("HARNESS_rc") == "0"
            and attempts_a == READY_AT_ATTEMPT
            and wall_a <= TEST_LONG_DEADLINE_S + DEADLINE_TOLERANCE_S,
            "listener/API ready at attempt %d, deadline %ds: %s"
            % (READY_AT_ATTEMPT, TEST_LONG_DEADLINE_S, describe(proc_a, met_a, wall_a)),
        )
        record(
            "behaviour_deadline_wait_actually_polled",
            wall_a >= (READY_AT_ATTEMPT - 1) * poll_s * 0.8 and attempts_a >= 2,
            "elapsed %.1fs over %s attempts with the script's own READY_POLL_S=%ds -- the "
            "wait must really back off between attempts (>= %.1fs of real backoff "
            "expected), not spin"
            % (wall_a, attempts_a, poll_s, (READY_AT_ATTEMPT - 1) * poll_s * 0.8),
        )
        combined_a = (proc_a.stdout or "") + (proc_a.stderr or "")
        record(
            "behaviour_readiness_attempt_noise_suppressed",
            "listener_count=0" not in combined_a and "api_read_error" not in combined_a,
            "expected not-ready per-attempt diagnostics absent from the readiness wait "
            "output: %r" % ((proc_a.stdout or "").strip()[:200],),
        )

        # Scenario B: active + listener fine, API probe blocks for SLOW_PROBE_S. THE repair.
        # The wait must return nonzero at its own deadline, far below the probe duration,
        # and the blocked probe process must be dead afterwards.
        proc_b, met_b, wall_b = run_harness(
            bash_exe, consts, funcs_text, exports,
            '%s %d' % (ready["name"], TEST_DEADLINE_S),
            active_rc=0, listener_ready_at=1, api_ready_at=0, api_slow_s=SLOW_PROBE_S,
            proc_timeout=SLOW_PROBE_S * 3)
        runs.append(("deadline_vs_blocked_probe", proc_b, met_b))
        record(
            "behaviour_deadline_terminates_blocked_probe",
            proc_b.returncode == 0 and met_b.get("HARNESS_rc") == "1"
            and met_b.get("HARNESS_probe_pid", "none") not in ("none", "")
            and wall_b <= TEST_DEADLINE_S + DEADLINE_TOLERANCE_S
            and wall_b < SLOW_PROBE_S / 2.0,
            "API probe blocks %ds, deadline %ds: must exit nonzero in <= %ds (tolerance "
            "%ds = kill-grace + coarse-clock + process slop) and far below the probe "
            "duration: %s"
            % (SLOW_PROBE_S, TEST_DEADLINE_S, TEST_DEADLINE_S + DEADLINE_TOLERANCE_S,
               DEADLINE_TOLERANCE_S, describe(proc_b, met_b, wall_b)),
        )
        record(
            "behaviour_no_probe_child_survives_deadline",
            met_b.get("HARNESS_probe_survivor") == "no",
            "the %ds probe child (pid %s) must be GONE after the deadline, not orphaned "
            "and still running: HARNESS_probe_survivor=%s"
            % (SLOW_PROBE_S, met_b.get("HARNESS_probe_pid", "?"),
               met_b.get("HARNESS_probe_survivor", "<absent>")),
        )

        # --- the D026 falsification pair: identical stubs, identical nominal bound ------
        # C: the VERBATIM pre-repair wait (the script's own attempt-count `retry` helper
        #    driving the old post_start_ready). It must overrun its nominal bound badly.
        pre_retry = ("\n".join(funcs["retry"]["body"]) if "retry" in funcs
                     else PRE_REPAIR_RETRY_FALLBACK)
        pre_funcs = pre_retry + "\n\n" + PRE_REPAIR_POST_START_READY
        proc_c, met_c, wall_c = run_harness(
            bash_exe, consts, pre_funcs, "export -f retry post_start_ready",
            'retry %d post_start_ready' % AB_BOUND,
            active_rc=0, listener_ready_at=1, api_ready_at=0, api_slow_s=AB_SLOW_PROBE_S,
            proc_timeout=AB_SLOW_PROBE_S * (AB_BOUND + 2) + 60)
        runs.append(("pre_repair_attempt_count", proc_c, met_c))
        record(
            "mutation_pre_repair_attempt_count_wait_violates_deadline",
            proc_c.returncode == 0 and met_c.get("HARNESS_rc") == "1"
            and wall_c > AB_BOUND + DEADLINE_TOLERANCE_S,
            "MUTATION (the falsified pre-repair behaviour, run verbatim): `retry %d "
            "post_start_ready` with an %ds-blocking API probe claims a %ds bound and must "
            "be shown to exceed it (> %ds) -- if this ever passes inside the bound the "
            "harness is not measuring the defect: %s"
            % (AB_BOUND, AB_SLOW_PROBE_S, AB_BOUND, AB_BOUND + DEADLINE_TOLERANCE_S,
               describe(proc_c, met_c, wall_c)),
        )

        # D: the repaired wait, SAME stubs, SAME nominal bound.
        proc_d, met_d, wall_d = run_harness(
            bash_exe, consts, funcs_text, exports,
            '%s %d' % (ready["name"], AB_BOUND),
            active_rc=0, listener_ready_at=1, api_ready_at=0, api_slow_s=AB_SLOW_PROBE_S,
            proc_timeout=AB_SLOW_PROBE_S * (AB_BOUND + 2) + 60)
        runs.append(("repaired_same_stub", proc_d, met_d))
        record(
            "behaviour_repaired_deadline_beats_pre_repair_on_same_stub",
            proc_d.returncode == 0 and met_d.get("HARNESS_rc") == "1"
            and wall_d <= AB_BOUND + DEADLINE_TOLERANCE_S
            and wall_d * 2.0 < wall_c,
            "same %ds-blocking probe, same nominal bound %ds: repaired wall %.1fs must be "
            "<= %ds AND less than half the pre-repair wall %.1fs: %s"
            % (AB_SLOW_PROBE_S, AB_BOUND, wall_d, AB_BOUND + DEADLINE_TOLERANCE_S, wall_c,
               describe(proc_d, met_d, wall_d)),
        )

        # Scenario E: systemd active on EVERY attempt, listener + API never available.
        # Proves ActiveState=active ALONE can never satisfy the readiness wait.
        proc_e, met_e, wall_e = run_harness(
            bash_exe, consts, funcs_text, exports,
            '%s %d' % (ready["name"], TEST_DEADLINE_S),
            active_rc=0, listener_ready_at=0, api_ready_at=0, api_slow_s=0)
        runs.append(("active_only", proc_e, met_e))
        record(
            "behaviour_active_only_deadline_expires",
            proc_e.returncode == 0 and met_e.get("HARNESS_rc") == "1"
            and int(met_e.get("HARNESS_attempts", "0") or 0) >= 2
            and wall_e <= TEST_DEADLINE_S + DEADLINE_TOLERANCE_S,
            "active always true, listener never bound, deadline %ds: %s"
            % (TEST_DEADLINE_S, describe(proc_e, met_e, wall_e)),
        )

        # Scenario F: active + loopback listener present, API never exactly DISARMED.
        proc_f, met_f, wall_f = run_harness(
            bash_exe, consts, funcs_text, exports,
            '%s %d' % (ready["name"], TEST_DEADLINE_S),
            active_rc=0, listener_ready_at=1, api_ready_at=0, api_slow_s=0)
        runs.append(("api_not_exact", proc_f, met_f))
        record(
            "behaviour_listener_up_but_api_not_exact_deadline_expires",
            proc_f.returncode == 0 and met_f.get("HARNESS_rc") == "1"
            and wall_f <= TEST_DEADLINE_S + DEADLINE_TOLERANCE_S,
            "active+listener true, API never exact, deadline %ds: %s"
            % (TEST_DEADLINE_S, describe(proc_f, met_f, wall_f)),
        )

        # Negative control: the SAME real deadline wait with a synthetic active-only probe
        # DOES pass scenario E's stubs. This proves E fails because of the listener/API
        # requirements, not because the harness is broken.
        proc_g, met_g, wall_g = run_harness(
            bash_exe, consts, funcs_text, exports,
            '%s %d' % (ready["name"], TEST_DEADLINE_S),
            active_rc=0, listener_ready_at=0, api_ready_at=0, api_slow_s=0,
            override=SYNTHETIC_ACTIVE_ONLY_PROBE_TMPL % probe_name)
        runs.append(("control_active_only", proc_g, met_g))
        record(
            "control_synthetic_active_only_would_have_passed",
            proc_g.returncode == 0 and met_g.get("HARNESS_rc") == "0"
            and met_g.get("HARNESS_attempts") == "1",
            "synthetic active-only probe under scenario E stubs: %s"
            % describe(proc_g, met_g, wall_g),
        )

        forbidden = [label for label, proc, met in runs
                     if FORBIDDEN_MARKER in ((proc.stdout or "") + (proc.stderr or ""))
                     or proc.returncode == 97
                     or met.get("HARNESS_forbidden", "0") not in ("0", "")]
        record(
            "behaviour_no_forbidden_command_invoked",
            not forbidden,
            "harness runs that reached for sudo/systemctl/ss/journalctl/curl/wget/nc/"
            "sqlite3/ssh/scp (function shadow + PATH shim + shim log): %s"
            % (forbidden or "none"),
        )

    # --- report ----------------------------------------------------------------------
    failed = 0
    for name, ok, detail in results:
        if not ok:
            failed += 1
        print("[%s] %s -- %s" % ("PASS" if ok else "FAIL", name, detail))
    print("")
    print("SUMMARY total=%d passed=%d failed=%d"
          % (len(results), len(results) - failed, failed))
    print("RESULT=%s" % ("GREEN" if failed == 0 else "RED"))
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
