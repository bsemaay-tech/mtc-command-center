================================================================================
GATE A RUN KIT D - A-5 .. A-9 (credential-free DISARMED) - 2026-08-08
Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b
================================================================================

AUTHORIZED ONLY FOR THE OWNER-APPROVED PREREGISTERED GATE A RERUN on gatea-staging.
This kit exercises a DISARMED staging service. It does not change product code.
Hard exclusions (unchanged): no credential value, broker/exchange access, successful ARM,
order, TESTNET/mainnet, wallet, master merge, or economic action. First genuine FAIL stops.

STATUS: LEAD-ACCEPTED FROZEN SOURCE / PREREGISTRATION ONLY. This kit has NOT been packaged,
transferred, or executed. A-5..A-9 are NOT RUN. No gate result is claimed. Final Lead checks:
five Bash scripts syntax PASS; PowerShell parser PASS; every Python heredoc compiles; diff/CR/scope
checks PASS. Package/transfer is the next bounded unit, followed by an AI-memory checkpoint.

LEAD-AUDIT REPAIR ROUND 1 (2026-08-08): the Lead's real source review found and repaired
binding defects in the first patch (Lead verification authoritative over the implementer's
older records-branch read): A-5/A-8 collect the `ss -H -ltn` LOCAL column at index 3 (not the
peer column 4); A-6 restores `start_mode='credentialed'` (installed candidate supports it),
fixes the false PASS (nonzero on timeout / start exception / failed assertion / stop
exception; `try/finally` always stops), and replaces unguarded `rm -rf` with validated temp
cleanup; A-8 host exits nonzero (`A8_HOST_FAIL`) when the probe fails; A-9 uses
`-e <ERE> -- <paths>`, canonical nine category names, and a truthful content statement (reads
bytes incl. the env file but emits counts + paths only). Lead evidence already supplied: `bash
-n` all 5 rc 0; PowerShell parser 0 errors; CR-byte count 0 on every new kit/preregistration
file. These are syntax/byte checks only; the repaired bindings await the Lead's re-audit. See
GATE_A_A5_A9_PREREGISTRATION_2026-08-08D.md §9.

LEAD-AUDIT REPAIR ROUND 2 (2026-08-08): a focused follow-up repaired exactly the three remaining
REQUIRED A-6 defects in gatea_A6.sh ONLY (A5/A7/A8/A8_host/A9 unchanged):
(1) Partial-start cleanup -- `stop_required` is set immediately BEFORE `engine.start()` so the
    `finally` always attempts `await engine.stop()` whenever start was invoked (including after a
    timeout or start exception). A stop exception stays nonzero; if start already failed, the
    original start exception is preserved while the stop failure is still recorded (no false PASS).
(2) SQLite sidecar cleanup -- strict target validation (exact `/home/gatea/gatea-A6-temp.` prefix
    + EXACTLY six alphanumeric mktemp chars, a real directory, not a symlink), then delete only
    maxdepth-1 REGULAR files whose exact basenames are `bridge.db` / `bridge.db-wal` / `bridge.db-shm`,
    require no entries remain, then `rmdir`. Never recursive; an invalid target or leftover residue
    forces a nonzero exit. A valid run no longer falsely fails on leftover WAL/SHM sidecars.
(3) Notifier/outbound hardening -- before `create_app`, `HL_ACCOUNT_ADDRESS`, `HL_API_WALLET_KEY`,
    `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `MTC_BRIDGE_START_MODE`, `MTC_BRIDGE_STATE_DB` are
    popped from the isolated process env WITHOUT reading or printing any value. Explicit
    `start_mode='credentialed'`, an explicit temp `store_path`, and an injected `MockBroker(bars=[])`
    are passed. `engine.notifier is None or engine.notifier.enabled is False` is required; only
    `notifier_disabled=true/false` is printed; it is bound into the PASS assertion. No env value is
    printed. STATUS unchanged: A-5..A-9 are NOT RUN and the kit is NOT packaged/transferred/executed;
    the round-2 bindings await the Lead's final re-audit. See
    GATE_A_A5_A9_PREREGISTRATION_2026-08-08D.md §12.

LEAD-AUDIT REPAIR ROUND 3 (2026-08-08): the final focused repair round. Same worktree and unit;
only the task-named files were edited (gatea_A6.sh, gatea_A7.sh, this README, the preregistration
doc, and the three top checkpoint sections). No new files/Git/SSH/staging/execution/product edits/
credentials/ARM/orders/broker network/package/transfer. Edits:
(A) A-6 pre-import env isolation -- the six keys (HL_ACCOUNT_ADDRESS, HL_API_WALLET_KEY,
    TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, MTC_BRIDGE_START_MODE, MTC_BRIDGE_STATE_DB) are popped
    from the isolated process env via os.environ.pop BEFORE `from bridge.app import create_app`
    and `from bridge.broker.mock import MockBroker`, then explicit app construction. Order:
    stdlib imports + release sys.path; the pop loop; only then the bridge imports; then the
    create_app(...) call. This prevents even module-level default app construction from seeing
    the parent process values.
(B) A-6 wording -- os.environ.pop removes and discards process-local values; no value is
    printed, copied, persisted, or retained. It is NOT claimed the values are "never read".
    Gate-A preconditions already established the keys absent, so clearing is defense in depth.
    The env FILE (/etc/mtc-bridge/mtc-bridge.env) is not opened by A6. (A-9 keeps its separate,
    truthful statement: it scans bytes incl. the env file but emits paths/counts only.)
(C) A-7 explicit cross-source equality -- after separately validating the API state and the DB
    app_state, the script now explicitly asserts and records `db_app == api_state` (an explicit
    equality check, not merely the logically-equivalent two DISARMED checks). On mismatch it
    exits nonzero. All existing A-7 checks are preserved.
Lead re-audit after round 2 (supplied evidence; syntax/compile only -- the worker recorded it and
did NOT run it): all five Bash scripts `bash -n` rc 0; PS parser 0 errors; `git diff --check`
clean; every embedded Python heredoc compiled (A5 3 blocks, A6 3, A7 2, A8 1). Round-2 lifecycle,
sidecar-cleanup, and notifier work are accepted. STATUS unchanged: A-5..A-9 are NOT RUN and the
kit is NOT packaged/transferred/executed; the round-3 bindings await the Lead's final acceptance.
See GATE_A_A5_A9_PREREGISTRATION_2026-08-08D.md §13.

Companion preregistration: 11_TRIAGE/GATE_A_A5_A9_PREREGISTRATION_2026-08-08D.md
(exact paths, criteria, first-FAIL response, GLM routing record + report hash, Lead
correction table, explicit NOT RUN status).

--------------------------------------------------------------------------------
FROZEN FACTS
--------------------------------------------------------------------------------
- Release SHA         : 2ce41e34bceb599d80af24c5c33d835820ec321b
- Release app root    : /opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b/IBKR_PAPER_BRIDGE
- Release scan root   : /opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b  (A-9)
- venv Python (PY)    : /opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b/bin/python
- systemd unit        : mtc-bridge-first-start.service
- State DB            : /var/lib/mtc-bridge/bridge.db
- API                 : 127.0.0.1:8790  (GET /api/status only; never POST /api/arm in this kit)
- Env file            : /etc/mtc-bridge/mtc-bridge.env  (NEVER print its contents)
- Staging VM IP       : 172.24.55.233  (A-8 host probe target)
- Baseline state      : A-0..A-4 PASS; A-5..A-9 NOT RUN; service active/static,
                        credential-free DISARMED, Restart=no, no broker/credentials.

--------------------------------------------------------------------------------
KIT MEMBERS (7 files)
--------------------------------------------------------------------------------
README.txt
gatea_A5.sh          A-5 unclean SIGKILL / manual-restart consistency (Restart=no)
gatea_A6.sh          A-6 empty-startup reconcile dry-run (in-process, temp DB, MockBroker)
gatea_A7.sh          A-7 read-only status / persisted-state / log + journal evidence
gatea_A8.sh          A-8 loopback binding proof (REMOTE side, on the VM)
gatea_A8_host.ps1    A-8 host reachability probe (WINDOWS host side)
gatea_A9.sh          A-9 content-redacted secret scan (9 EREs, release + /etc/mtc-bridge only)

--------------------------------------------------------------------------------
SHARED SCRIPT CONTRACT (every Bash script)
--------------------------------------------------------------------------------
- set -Eeuo pipefail ; fixed evidence log per gate under /home/gatea ; refuses to overwrite
  an existing log (exit 2); redirects stdout+stderr to the log; EXIT trap records exact rc.
- Uses the installed venv Python for all JSON/SQLite work; NEVER assumes the sqlite3 CLI.
- No writes outside /home/gatea except the runbook-authorized service/DB state caused by the
  A-5 SIGKILL + one explicit start (Restart=no).
- Output is structured key=value evidence. Ends with exactly `A-<n> PASS` only if ALL
  assertions hold.
- A script NEVER hashes its own still-open log from inside itself; evidence-log hashes are
  captured post-run by the commands below.
- None of these scripts POST /api/arm. A-5/A-6/A-7/A-8 do not read the env file. A-9 scans
  bytes under the release + /etc/mtc-bridge (which includes the root-readable env file) via
  `grep -l`; it prints PATHS only — no value/matched text is printed, copied, or persisted
  (category counts + paths only).

--------------------------------------------------------------------------------
LOCAL VALIDATION  (Lead, BEFORE packaging/transfer/execution)
--------------------------------------------------------------------------------
Run from the kit directory.

1) Bash syntax check (each must be rc 0):
     bash -n gatea_A5.sh
     bash -n gatea_A6.sh
     bash -n gatea_A7.sh
     bash -n gatea_A8.sh
     bash -n gatea_A9.sh

2) PowerShell parser check for the host probe (must report no errors):
   Windows PowerShell:
     powershell -NoProfile -Command "$e=$null; [void][System.Management.Automation.Language.Parser]::ParseFile('gatea_A8_host.ps1',[ref]$null,[ref]$e); if($e){$e; exit 1} else {'PS_PARSE_OK'}"
   PowerShell 7 (pwsh), if available:
     pwsh -NoProfile -Command "$e=$null; [void][System.Management.Automation.Language.Parser]::ParseFile('gatea_A8_host.ps1',[ref]$null,[ref]$e); if($e){$e; exit 1} else {'PS_PARSE_OK'}"

3) CR-byte check (must be 0 for every .sh; the .ps1 is also LF in this kit):
     grep -c $'\r' gatea_A5.sh gatea_A6.sh gatea_A7.sh gatea_A8.sh gatea_A9.sh gatea_A8_host.ps1

4) Manifest + package (LATER, by Lead): generate SHA256SUMS for the 6 non-README members
   (or all 7), create the tar, and record member count + tar SHA-256 + tar bytes. This kit
   is frozen as SOURCE only; the Lead owns manifest/tar creation, transfer, and verification.

--------------------------------------------------------------------------------
TRANSFER + REMOTE VERIFICATION  (Lead)
--------------------------------------------------------------------------------
- Transfer the tar to /home/gatea on gatea-staging; verify exact tar SHA-256 and byte size
  and the exact member set; extract; run `sha256sum -c SHA256SUMS` (all OK) and re-run the
  five `bash -n` checks on the extracted files.
- Keep run-kit B and C intact; D is a sibling revision (A-5..A-9 only).

--------------------------------------------------------------------------------
EXECUTION ORDER  (on gatea-staging, as the gatea user with passwordless sudo for
systemctl/sqlite/journalctl/stat/sha256sum/ufw/grep). STOP AT FIRST FAIL.
--------------------------------------------------------------------------------
Run strictly in order. Before A-5, the Lead must have independently validated the scripts
(steps above), created the manifest/tar, and transferred + verified the kit.

  1) A-5:   bash /home/gatea/gatea_A5.sh        # SIGKILL main + one explicit start; DB unchanged
  2) A-6:   bash /home/gatea/gatea_A6.sh         # in-process empty-startup reconcile dry-run
  3) A-7:   bash /home/gatea/gatea_A7.sh         # read-only status/DB/log/journal evidence
  4) A-8 remote:   bash /home/gatea/gatea_A8.sh  # :8790 loopback binding (on the VM)
     A-8 host:     powershell -NoProfile -ExecutionPolicy Bypass -File gatea_A8_host.ps1
                   # from the Windows host; prints booleans/errors only
     A-8 PASS = remote ends `A-8 PASS` AND host shows port22_ok=True AND port8790_ok=False.
  5) A-9:   bash /home/gatea/gatea_A9.sh         # secret scan; any hit is FAIL/BLOCK

MEMORY UPDATE AFTER EACH GATE: after every gate PASS, update MTC_COMMAND_CENTER/_AI_MEMORY/
(NEXT_STEPS.md, GLOBAL_HANDOFF.md) and 11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md BEFORE
running the next gate. Do not run two gates back-to-back without the memory update.

FIRST-FAIL / SAFETY: at the first FAIL, preserve the evidence log, run only read-only
diagnostics as needed, then STOP. If the failure leaves the service in an unsafe state,
safe-stop and mask the unit (`sudo systemctl stop mtc-bridge-first-start.service`,
`sudo systemctl mask mtc-bridge-first-start.service`) and write the result + memory. Do NOT
auto-restart or mask on a script's internal failure; the Lead handles the safe first-FAIL
response.

--------------------------------------------------------------------------------
POST-RUN EVIDENCE-LOG HASH + SIZE  (run AFTER each script exits and its log is closed)
--------------------------------------------------------------------------------
On gatea-staging, for each gate that ran:
     sha256sum /home/gatea/gatea-A5-20260808D.log
     stat -c '%s' /home/gatea/gatea-A5-20260808D.log
   (likewise gatea-A6/A7/A8/A9-20260808D.log)

On the Windows host for A-8:
     Get-FileHash 'C:\WPI_ARTIFACTS\gatea-A8-host-20260808D.log' -Algorithm SHA256
     (Get-Item 'C:\WPI_ARTIFACTS\gatea-A8-host-20260808D.log').Length

These hashes/sizes are recorded in the result + memory; they are NOT produced by the scripts.
================================================================================
