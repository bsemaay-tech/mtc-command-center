# WP-L Phase 2 — R4-5 closure attempt (2026-08-09) — RESULT: STILL BLOCKED, NOT CLOSED

## Verdict

**R4-5 (dangling restore-destination symlink fixture, Python level) remains BLOCKED. No RED/GREEN
run was performed. Closure is NOT claimed.** The round-2 blocker recorded in
`WPL_P2_COMMAND_GAP_PROPOSALS_2026-08-09.md` §8.4 row R4-5 at commit `75ee8912` — `os.symlink`
refused with `WinError 1314` (SeCreateSymbolicLinkPrivilege not held) — was reproduced identically
today with three independent probes. The equivalent shell-level predicate remains closed by §8.2
R0-2; that standing is unchanged by this attempt.

## Task provenance and boundary

Owner-directed bounded local attempt (2026-08-09, Claude Fable session). Boundary respected: no
host/staging contact, no model dispatch, no existing file edited, no fixture or harness file
created or modified, no Developer Mode or privilege change made. This new file is the only
repository change from this unit.

## Evidence — why the fixture still cannot be built (all probes 2026-08-09)

### (a) Token privilege — ABSENT

`whoami /priv` on the working (non-elevated) token lists **no `SeCreateSymbolicLinkPrivilege`**
(pattern match over the full privilege listing returned nothing). The session shell is not
elevated (`WindowsPrincipal.IsInRole(Administrator)` → `False`).

### (b) Windows Developer Mode — OFF (checked read-only, NOT enabled)

`reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock"` returned no
`AllowDevelopmentWithoutDevLicense` value (key/value absent). With Developer Mode off, CPython's
`SYMBOLIC_LINK_FLAG_ALLOW_UNPRIVILEGED_CREATE` path (used automatically by `os.symlink` on
Python ≥3.8) is unavailable, so unprivileged symlink creation cannot succeed. Per the task
boundary, Developer Mode was only inspected, not changed.

### (c) Empirical reproduction — exact same failure as round 2

```
python -c "import os; os.symlink(r'C:\nonexistent_target_R45_probe', <scratchpad>\dangling_probe_link)"
→ OSError: [WinError 1314] Gereken ayrıcalık istemci tarafından sağlanmıyor
```

A dangling symlink (the precise artifact the R4-5 fixture requires) cannot be created by CPython
in this environment. Junction/`.lnk` workarounds remain invalid for the same reasons already
recorded in the round-2 table (a junction is not `Path.is_symlink()`; MSYS `.lnk` emulation is
invisible to CPython) — they would not exercise the predicate honestly.

## Harness state (verified present, untouched)

Both protected D026 roots exist and were left unmodified:

- `%LOCALAPPDATA%\Temp\D026.mR6q2g` — `blocks, fx_r0_1, fx_r0_1b, fx_r0_2, fx_r0_3, fx_r0_4,
  fx_r0_7, redtmp, release, rp4`
- `%LOCALAPPDATA%\Temp\D026R2.87imLE` — `blocks, blocks_check, blocks_final, fx_r1, fx_r2,
  red_blocks, release, rp4, rp5, stubs`

Target block confirmed at the frozen commit: `RP4-C3` in
`11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_2026-08-09.md` @ `75ee8912` (round-2 blob digest
`0520cc901e56a66fe61e0df9edc0ed33fa4b05c09d62ba8f7471ef9ff688e4a5`, 295 lines, `py_compile` OK per
§8.1). It was read, not executed.

## What would close R4-5 (for a future authorized unit — any ONE unblock path)

1. **Enable Windows Developer Mode** (Settings → System → For developers). CPython then creates
   symlinks unprivileged. Owner action; this unit deliberately did not enable it.
2. **Run the fixture step from an elevated shell** whose token holds
   `SeCreateSymbolicLinkPrivilege`.
3. **Grant the privilege** to the working user via security policy (`SeCreateSymbolicLinkPrivilege`
   user-rights assignment) + re-logon.

After unblock, the closure run is exactly the §8.4 R4-5 fixture against frozen `RP4-C3`
(`0520cc90…`): create the dangling restore-destination symlink in a fresh temporary root, run the
block, and record honestly — expected GREEN behaviour is fail-closed rejection (`C3_FAIL`, or
`C3_STOP` with artifacts preserved), with the RED side demonstrated per D026 (falsification or
equivalent mutation), commands and real output recorded. Until that run exists, R4-5 stays
**BLOCKED — not closed** everywhere it is referenced.

## Exclusions

No SSH, host, staging, or `systemctl` contact; no service, credential, broker/exchange, ARM,
TESTNET/mainnet, or economic action; DISARMED state untouched; no model dispatch (no Codex, no
Claude Max, no GLM, no Cline); no existing repository file modified; no Git action beyond adding
exactly this new file on `feature/donchian-crypto-ladder`.
