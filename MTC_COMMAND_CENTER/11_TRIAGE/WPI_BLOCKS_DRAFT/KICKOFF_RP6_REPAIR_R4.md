# KICKOFF — RP6-P0 round 4 (owner intent, past T0 cap): four Codex flagship findings

Owner authorized exceeding the T0 cap for the identical venv site-startup security class
on RP7 (2026-08-10 ~17:15); the Lead extended that authorization to RP6-P0, whose Codex
flagship audit (`RP6_CODEX_T0_AUDIT_2026-08-10.md`, BLOCK 4) raised the SAME F1 hole plus
three contract fixes. Round 4. You are Claude Opus 5 xhigh, implementer. Working dir:
C:\LAB\Tradingview_LAB_CLEAN. No host/network. No commit.

**GATE: dispatch this ONLY after RP7 round 4 is committed** — F3 references RP7's final
frozen tool set (RP7 R4 adds `python3`), so it must target settled RP7 bytes, not a
moving worktree. The Lead fills the RP7 frozen basis SHA + tool set below before dispatch.

- RP7 frozen basis for F3: commit `<FILL: RP7 R4 commit>`, RO tool set `<FILL: from
  frozen RP7-WPI-RO.sh>`.

## Inputs (relative to `MTC_COMMAND_CENTER/11_TRIAGE/`)

`WPI_BLOCKS_DRAFT/RP6_CODEX_T0_AUDIT_2026-08-10.md` (findings 1–4 with executed
falsifications + required repairs = the contract), `WPI_BLOCKS_DRAFT/RP6-P0.sh` (current
`2d9b166e…`, 71743 B, `bbb40ab6`), `SELF_QA_RP6.md`, `STATUS_RP6_P0.md`, the frozen
`WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh` at the gated commit above,
`WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` (edit only §8.1 rows a fix names),
`DESIGN_DEFECT_PATTERNS_2026-08-10.md`.

## The four, exact fixes (Codex "Required repair" text binds)

- **F1 (HIGH)** — run the interpreter probe with `-I -S` (retain cleared env), so venv
  `site`/`.pth` cannot execute before the `-c` body. D026: an executable `.pth` fixture —
  current/pre-fix bytes create the marker, repaired bytes do NOT, both result shapes
  recorded. Correct the `-I means only sys imported / mutation=none_in_this_block` claims
  to state only what `-I -S` establishes.
- **F2 (MEDIUM)** — bound the row-9 `systemctl` query: cleared-env exec FIRST with the
  pinned `timeout` as its argument (`env -i … <pinned-timeout> … <pinned-systemctl> …`);
  timeout → `system_manager_unreachable` rc 3 with honest recorded status/detail. D026:
  current arm needs an external kill; repaired arm returns its own bounded STOP.
- **F3 (MEDIUM)** — regenerate the P0 RO tool inventory from the FROZEN RP7 executable
  (gated basis above) + P0-only deps: include/pin `timeout`, drop `grep`/`awk` if neither
  stage invokes them, fix the count + terminal claim. Add a drift test comparing the two
  frozen inventories. Must accept a complete RP7 pin set.
- **F4 (LOW/MED)** — `p0_resolve_passwd` must export its getent status so both error
  callers emit honest `rc=<n>` on `identity_unresolvable`. Align the valid-no-match token
  with row 3 (amend the row to preregister `state_account_resolution_unexpected`, or
  change the block to a registered token — pick one, state it, edit both sides). Add
  exact-LINE assertions (not substring) for rc0-parse-error, rc2-no-match, rc2-diagnostic,
  other-nonzero cases.

## Deliverables

Repaired `RP6-P0.sh` + `SELF_QA_RP6.md` (every fix REAL RED/GREEN; the `.pth` forge
fixture is load-bearing — run it) + `STATUS_RP6_P0.md` + `RP6_FULLBLOCK_REPAIR_REPORT.md`
+ `RP6_REPAIR_R4_REPORT.md` + any §8.1 draft edit. Write LF only. `bash -n` PASS; re-run
C13 harnesses green; new SHA-256 + bytes. If `python3`/`timeout` need `<PIN-AT-FREEZE>`
paths, mark them freeze-gate inputs. Touch ONLY those five (+draft). Do not commit.
