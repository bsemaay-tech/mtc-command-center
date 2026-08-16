# GATEA-STAGING Privileged-Channel Configuration Question Sheet

This is a **documentation request only**. Please do not run, change, or install anything, and do not probe the live host. Answer only from existing authoritative configuration records. If those records do not establish an item, write `UNKNOWN` and identify the missing or insufficient record; do not infer a value. Completing this sheet does not approve or authorize host access or any other action.

## Part 1 — Three administrator choices

| Choice | What is being chosen | A complete answer |
|---|---|---|
| **1. Exact privileged account** | Name the account intended to provide the approved privileged channel. | The exact principal and host/address, whether the approved pinned identity is intended for that principal, and the authoritative account/key-to-principal mapping record. |
| **2. Direct or indirect route** | Choose direct login to that account, or an exact escalation/forced-command route. | State `DIRECT`, or list the entire ordered chain from login account through the account shell and every forced-command, wrapper, or escalation step to the privileged process. Include the byte-exact command/arguments and authoritative mapping record for every enforced step. |
| **3. Enforced read-only control** | Choose the configuration control that independently prevents target mutation before and during the capture, including failure paths. | Give the exact control name, policy/configuration identity and location, enforcement owner, point in the process chain where it applies, and the write scope it denies while evidence output remains available. |

## Part 2 — Five facts from configuration records

| Fact | Configuration records that typically hold it | Required answer form |
|---|---|---|
| **1. Account shell** | Authoritative account/provisioning record and executable identity record. | Exact absolute shell path and executable identity, bound to the selected principal. |
| **2. Forced command** | Effective server access configuration and the selected identity’s key-to-command mapping; any applicable wrapper configuration. | The byte-exact forced-command command/arguments, or the literal `NONE`, plus the record name and revision that establishes it. |
| **3. Environment before cleanup** | Applicable server-session, authentication-stack, account, shell-startup, and forced-command/wrapper configuration records. | A byte-preserved, complete `NAME=VALUE` inventory for the first target process immediately before environment cleanup. Explicitly record presence or absence of `BASH_ENV`, `ENV`, loader variables, exported functions, and startup hooks. |
| **4. Starting directory** | Account/provisioning, session-launch, and forced-command/wrapper configuration records. | Exact absolute working-directory path for the first target process, before shell startup, interpreter import, or any directory change; name the configuration that sets it. |
| **5. Inherited file connections** | Session-launch and forced-command/wrapper process configuration records. | A complete table of every inherited file descriptor: number, connected target, read/write mode, and close-on-exec state. Include descriptors 0, 1, and 2 and state explicitly whether any other inherited writable descriptor exists. |

## Fill-in checklist

- [ ] Privileged account/principal and host/address: ______________________________
- [ ] Direct route or complete ordered escalation/forced-command chain: ___________
- [ ] Independently enforced read-only control: __________________________________
- [ ] Account shell path and executable identity: _________________________________
- [ ] Forced command (byte-exact) or `NONE`: ______________________________________
- [ ] Complete environment before cleanup: _______________________________________
- [ ] Starting directory before startup/import/directory change: __________________
- [ ] Complete inherited file-connection table: __________________________________

**Independence note:** Read-only must be enforced by configuration, not promised by a person or merely stated by the program being constrained. Please identify the authoritative records behind every answer. Copies or screenshots of those records are welcome. If the records leave an item open, report it as `UNKNOWN` rather than filling the gap by assumption.

## Source appendix

- Documentation-only authority and requested deliverable: `MTC_COMMAND_CENTER/11_TRIAGE/OWNER_DECISIONS_2026-08-16_MORNING.md:10-25`.
- Three decisions versus five record-based facts: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/ROOT_CHANNEL_RECORD_GAP_2026-08-15.md:10-12`.
- Required facts, record types, and answer detail: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/ROOT_CHANNEL_RECORD_GAP_2026-08-15.md:172-185`.
- Exact owner/administrator question and no-authority boundary: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/ROOT_CHANNEL_RECORD_GAP_2026-08-15.md:216-236`.
