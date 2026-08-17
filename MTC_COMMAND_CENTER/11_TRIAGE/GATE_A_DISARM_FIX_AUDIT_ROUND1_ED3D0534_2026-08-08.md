# Gate 5 audit round 1 — A-4 repair `ed3d0534` (2026-08-08)

## VERDICT: **`ed3d0534` IS NOT ACCEPTED.** One required finding, Lead-reproduced.

| D025 slot | Auditor | Verdict | Suite executed |
|---|---|---|---|
| Flagship 1 | `claude-opus-5` xhigh | **PASS-WITH-NITS** — 0 required, 3 nits | yes, `1359 passed, 1 warning in 220.00s` |
| Flagship 2 | `gpt-5.6-sol` xhigh | **REQUEST_CHANGES** — 1 required finding | yes, full suite |

D025 rule 3 requires **both** flagships accepting plus no unresolved reproduced required finding.
`REQUEST_CHANGES` is non-accepting, and the finding reproduces. **Gate A must not start.**

Reports: `C:\tmp\CLAUDE_AUDIT_DISARM_FIX_2026-08-08.txt`,
`C:\tmp\CODEX_AUDIT_DISARM_FIX_2026-08-08.txt` (769 288 B). Worktrees `C:\GAAUD_DISARM_CLA` and
`C:\GAAUD_DISARM`, both detached at `ed3d0534`, clean at start and end. Prompt:
`C:\tmp\gatea_disarm_fix_audit_prompt.md`.

**Both flagships found the same defect independently.** They differ only on severity — Claude filed it
as NIT 1, Codex as a required finding. That convergence is the strongest signal in this round, and the
stricter reading governs.

---

## 1. The required finding — REPRODUCED, therefore binding

**`EnvironmentFile=` overrides `Environment=` in systemd, so the "pinned" start mode is not pinned.**

`deploy/linux/systemd/mtc-bridge-first-start.service.template:42` sets
`Environment=MTC_BRIDGE_START_MODE=credential_free_disarmed`, and line 45 then declares
`EnvironmentFile=/etc/mtc-bridge/mtc-bridge.env`. Per `man systemd.exec` and the upstream
`systemd.exec.xml`, assignments read from `EnvironmentFile=` **override** those made with
`Environment=`. Textual order does not protect the unit. So a root-written
`MTC_BRIDGE_START_MODE=credentialed` in the env file silently selects credentialed startup.

And the verifier cannot see it.

**Lead reproduction, run at `ed3d0534`:**

```
deploy/linux/verify.sh:138
  if [ -f "${MTC_ENV_FILE}" ] && grep -qE '^[[:space:]]*(export[[:space:]]+)?HL_LIVE_ACK=' …
  -> the env-file hygiene check rejects HL_LIVE_ACK and nothing else

grep -n 'MTC_BRIDGE_START_MODE' deploy/linux/verify.sh
  -> exactly ONE hit, line 166, inside the *unit* needle list
  -> zero env-file rejection of the variable
```

Codex's executed probe agrees:

```
EXPLICIT_OVERRIDE      resolved_mode=credentialed  exception_type=RuntimeError
                       message=BROKER_PATH_REACHED_AFTER_CREDENTIALLED_OVERRIDE
CURRENT_VERIFY_COVERAGE unit_pin_present=True  env_override_present=True
                        verifier_rejects_env_override=False
```

`verify.sh` therefore reports PASS on the unit pin while an env-file override selects credentialed
startup. **The DISARMED property is currently conventional, not enforced.**

**Lead correction to the record.** The `ed3d0534` commit message and Addendum C §C.1 justified the
placement partly on the grounds that the unit is hashed so the setting "cannot drift silently." That is
true for *unit* drift and remains true — `verify.sh:184-190` renders the release template and
`cmp -s` byte-compares it, and `install_manifest.json` records `first_start_unit_sha256`. **It was
wrong as a general claim**, because the env file is a second, unguarded channel that outranks the unit.
The placement is still correct; its stated rationale was overstated. Addendum C §C.5 asked exactly this
question and it is now answered — against the assumption.

**Execution limit, stated plainly:** neither auditor could execute the precedence itself (no systemd,
no WSL on this workstation), so that half rests on the systemd documentation. Both independently cited
it. One command on the staging host settles it and must be captured next round:

```
systemctl show -p Environment mtc-bridge-first-start.service
```

**Minimum repair, as named by Codex and within existing scope:** make `verify.sh` reject any
`MTC_BRIDGE_START_MODE=` definition in `${MTC_ENV_FILE}`, and add a regression test proving the
rejection. Claude's NIT 2 (document the pin in the README and the env template, mirroring what
`MTC_BRIDGE_STATE_DB` already has) closes the same channel by documentation and should ride along.

## 2. What both flagships confirmed working — this is not a failed repair

The repair does what it claims **when the variable is the effective value**. Both auditors ran a real
`python -m bridge.app` process with the unit's `Environment=` values and no credentials present:

```
listener on 127.0.0.1:8790          process_alive=True
GET  /api/status  -> 200  state=DISARMED  mode=credential_free_disarmed  network=disabled
                          exchange_conn=disabled  exchange_enabled=False
                          credential_lookup=disabled  arm_enabled=False
POST /api/arm     -> 409  {"detail":"ARM unavailable in credential-free DISARMED start mode;
                                     exchange access is disabled"}
GET  /api/status  -> 200  still DISARMED, state_version unchanged
```

**That is precisely the confirmation A-4 could not obtain on 2026-08-08** — an application-level arm
refusal rather than `Errno 111 Connection refused`. Without the variable, both reproduced the original
A-4 traceback exactly (`app.py:150` → `:244` → `settings.py:113` `RuntimeError`).

Claude additionally executed a near-miss table proving the failure shape is safe:

```
'credential-free-disarmed' -> ValueError    'CREDENTIAL_FREE_DISARMED' -> ValueError
'credential_free_disarm'   -> ValueError    ''                         -> ValueError
unset -> 'credentialed'   (only None falls back)
```

A typo crashes the unit rather than silently degrading to `credentialed`. Correct fail-closed shape.

Other agreed confirmations: scope is exactly 3 files / 6 insertions / 1 deletion with no fourth file;
the unit string equals the source constants at `bridge/app.py:30-32`; `install.sh` templating touches
only `@RELEASE_SHA@`, so `verify.sh`'s `grep -qF` matches the installed unit literally; the steady
profile correctly excludes the setting and `install.sh:144-148` / `verify.sh:219-225` refuse it
outright; nothing else under `deploy/` assumes credentialed startup.

**D026 falsified in both directions** (Claude), and against the parent template (both):

```
A. first-start test vs parent ebada020 template          -> AssertionError  (test_linux_deployment.py:226)
B. steady test vs a steady template polluted with the pin -> AssertionError  (…:240)
C. both tests vs real HEAD templates                      -> pass
```

Both assertions are load-bearing.

## 3. Remaining nits, not blocking

1. **Claude NIT 2 / docs.** `grep -rln "MTC_BRIDGE_START_MODE" --include=*.md .` returns nothing
   repo-wide. `MTC_BRIDGE_STATE_DB` has both a README paragraph and a note in the env template. Mirror
   both — especially "set by the unit; defining it here would override the unit," which is now known to
   be literally true.
2. **Codex nit / Claude parity.** `install.sh:413` records `first_start_unit_sha256` but `verify.sh`
   never compares that manifest field. Its exact rendered-template `cmp -s` still detects unit drift,
   so this is not a required repair.
3. **Deferred by owner, noted only:** `create_app()` still builds the broker inside itself
   (`bridge/app.py:150`), so the credential-free property rests on one environment variable rather than
   on structure. Barış deferred this deliberately on 2026-08-08. Not a finding this round — but note
   that finding 1 is a direct consequence of that structure.

## 4. Status and what happens next

- `ed3d0534` is **NOT ACCEPTED**. `ebada020` remains the last accepted candidate.
- The rebuilt artifact `C:\WPI_ARTIFACTS\ed3d0534…` (manifest `8964CC43…`) is **not invalidated as a
  build**, but it packages an unaccepted commit. Do not transfer or install it.
- **Gate A does not start.** Addendum C §C.7 already requires both flagships accepting.
- Repair round 1 of a maximum 3 is available. The repair is small and its shape is agreed by both
  auditors, so it should fit one round.
- **No product code was changed in response to this audit.** The repair needs Barış's authorization,
  the same as the fix that preceded it.
