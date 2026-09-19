# Gemini read-only wrapper repair — 2026-09-14 (owner decision OD-20260914-GEMINI-WRAPPER-2, "D10 Yes")

File: `C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-GeminiProReadOnly.ps1`
- before: sha256 `66c749a08b2559d1b275bd458920dd03ed5eaf581ff13ccc777c6f801e8de5e2` (backup `C:\tmp\Invoke-GeminiProReadOnly.ps1.BAK_20260914_preEnvelopeFix`)
- after:  sha256 `eff6a7273a6b94e27dee84f06f6aa7956dd7b9b7e9057a2bbcb24103398a4dda`

## Trigger
`P012_RISK_PACKET_GEMINI_B` (12:35-12:41Z): the model completed a PASS review; the CLI recorded five transient `INTERNAL (code 500)` retries as ERROR_MESSAGE steps; the print-mode `result` object then had a member the wrapper's exact six-member pin did not allow → `Gemini payload contains missing or unexpected members.` and the raw stdout was discarded with the throw (CT13 `P012_RISK_PACKET_20260914/GEMINI_AUDIT_B/LEAD_TERMINAL_ATTEMPT1.md`).

## Change 1 — `Assert-AgentPayload`
The six required members (`conversation_id, status, response, duration_seconds, num_turns, usage`) must all be present, case-exact (missing → `Gemini payload is missing the required member: <name>`). Additional members no longer throw; each is written to stderr as `GEMINI_RESULT_EXTRA_MEMBER name=<n> value=<json, 500 chars max>`. The `usage` object stays exact (five members). The status == `SUCCESS`, non-empty response and `GEMINI_READ_ONLY_OK` sentinel checks are unchanged — a run that did not succeed still throws.

## Change 2 — tail of the script
`ConvertFrom-SingleTurnStream` + `Assert-AgentPayload` now run inside try/catch; on a refusal after the model run the raw stdout and stderr are written to `%TEMP%\gemini_wrapper_failures\<UTC stamp>_<pid>.stdout.jsonl` / `.stderr.txt` (UTF-8, outside every repository) and the thrown message gains `Raw stdout/stderr kept at: <path>`. Nothing is retried.

Untouched: sandbox, deny rules, filesystem-change watcher, repository snapshot comparison, project-config hash check, stream-event schema (`Stream init/step/result`), exit-code check, preflight.

## Evidence
- `test_assert_agent_payload.ps1` (7 cases, functions extracted from the wrapper file; strict-JSON guard stubbed): ORIGINAL → case 2 (seven members, SUCCESS, sentinel) THROWS the production message = RED; PATCHED → 7/7 as expected (extra member tolerated with the stderr line; status ERROR / missing sentinel / missing usage / extra usage member / wrong-case name still THROW) = GREEN. Outputs in this directory (`test_original.txt`, `test_patched.txt`).
- Real probe through the patched wrapper 13:06Z: conversation `c3d8b631-0be4-4ac6-9e4c-5b88675790b8`, `status: SUCCESS`, sentinel present, rc 0.
- Pins updated (old hash → new hash), backups `*.BAK_20260914_prePinUpdate`: `C:\tmp\GEMINI_LANES_20260907_2035\Invoke-GeminiPacketReview.ps1`, `C:\tmp\GEMINI_R30_20260908\Invoke-GeminiPacketReview.ps1`. `gemini_chain.py` only records the hash in LEAD_START.json (no assertion).

## Not verified
The exact member the CLI added on 2026-09-14 is unknown (raw bytes were lost by the old wrapper). The next occurrence will be captured by change 2 and named on stderr by change 1.
