# RP7 cap-override Lead continuation — 2026-08-14

Role: binding Lead handoff for the still-authorized RP7 T0 repair. This is not an
audit verdict and claims no acceptance.

## Live state

- Repository HEAD when recorded: `4070ef3623b65b87a10584144944d1310405bd9c`.
- The 2026-08-14 Claude Pro `claude-opus-5` xhigh session hit its session limit
  before completion; Pro reported reset at 13:50 Europe/Chisinau.
- The separate Claude Max route reported its weekly limit exhausted.
- Only `RP7-WPI-RO.sh` was modified. The partial working-tree identity is
  130788 bytes, SHA-256
  `7126AD78737C481C56149D87B41A089D23279C7E1EDFEDF403311702CF883A50`.
- `SELF_QA_RP7.md`, `STATUS_RP7.md`, and
  `RP7_ROWS_1_9_REPORT_2026-08-13.md` remain at committed bytes.
- Do not discard, stash, reset, or overwrite the partial diff. Independently
  inspect it and continue the same authorized repair in a fresh exact
  `claude-opus-5` xhigh session.

## Binding Lead finding — REQUIRED-1 remains open

The partial diff added a comment saying that CR blocks continuation and that no
`rstrip` should be added, but it left the rejected parser logic unchanged. The
Lead reproduced the real behavior locally on systemd 259:

```text
/tmp/.../crlf.service:4: Unknown key 'WantedBy' in section [Unit], ignoring.
CURRENT_CONTINUES=False
REPAIRED_CONTINUES=True
```

The diagnostic proves that systemd absorbs `[Install]` after a value line ending
in backslash plus CRLF. Therefore the current parser's `physical.lstrip(WS)` is
wrong for this case. Apply the audit-prescribed surgical CR removal before the
continuation test (for example `physical.rstrip("\r").lstrip(WS)`). Do not use
broad `rstrip()` or `rstrip(WS)`: the trailing-space-after-backslash control must
retain the systemd disposition.

Remove or correct the false comment. Add and execute the `crlf_install` and
`trailing_space_after_backslash` cases as literal D026 evidence.

## Supplemental review — Lead adjudication

A read-only GLM-5.2 review was used only to find counterexamples while Opus was
quota-blocked. The Lead accepted the CRLF finding above after direct systemd 259
reproduction. The Lead also inspected the partial row-9 changes:

- mid-name quote rejection is directionally correct;
- the explicit single-occurrence invariant is documentation of existing
  fail-closed behavior;
- the dual-lexer count disagreement fails closed.

These row-9 changes still require the kickoff's literal D026 fixtures and the
complete published fence. The supplemental review fills no flagship slot.

## Remaining mandatory work

Read and obey
`KICKOFF_CLAUDE_RP7_CAP_OVERRIDE_REPAIR_2026-08-13.md` and its binding prior
audit in full, with this continuation as an additional repair input.

1. Close REQUIRED-1 as above and execute its RED/GREEN plus control evidence.
2. Close REQUIRED-2 by running all six row-6 pairs against both the materialized
   round-4 blob and repaired bytes in separate processes, preserving each case's
   real polarity and terminal line.
3. Complete the row-9 D026 evidence for mid-name quoting, fully quoted valid
   token, and same-value duplicate refusal.
4. Run the complete rows-1–9 fence verbatim, re-derive every byte/SHA identity,
   and make the pasted transcript reproduce exactly.
5. Update only the four files owned by the original kickoff. Run shell syntax and
   `git diff --check`. Do not commit, stash, reset, checkout, deploy, contact a
   host, use credentials, or touch ARM/orders/trading surfaces.

Stop only after all four owned files are internally complete and report exact
commands and real outputs. The Lead will independently reproduce the evidence,
pin the candidate, and dispatch the two mandatory fresh T0 flagship audits.

## 2026-08-14 14:53 Europe/Chisinau continuation update

A fresh exact `claude-opus-5` xhigh continuation was launched at 14:47 after
the earlier Pro reset. It hit the session limit at 14:53 and reported the next
reset as 18:50 Europe/Chisinau. The session changed no bytes.

The isolated partial remains exactly:

- `RP7-WPI-RO.sh`: 130788 bytes; SHA-256
  `7126AD78737C481C56149D87B41A089D23279C7E1EDFEDF403311702CF883A50`.
- `SELF_QA_RP7.md`: 445965 bytes; SHA-256
  `54B115D0BFE25B45B52FBA50DC8C2893EB99007D4021F07B310F50E83A3419FA`.
- `STATUS_RP7.md`: 7725 bytes; SHA-256
  `4CF27CA778BB7D056648CC9880733285589B2E3814EFBEB50ADD138E7357A054`.
- `RP7_ROWS_1_9_REPORT_2026-08-13.md`: 31982 bytes; SHA-256
  `2A6CFF5CDEC28DF1174AA8E62EEC491C001CB10227F5FFF5BBD5BE69A20A0284`.

Only `RP7-WPI-RO.sh` differs from Git, still at 53 insertions and 5 deletions.
No Claude or Codex CLI writer remained after the quota stop. Resume only in a
fresh exact `claude-opus-5` xhigh session after the reset; do not discard,
stash, reset, checkout, or overwrite this partial diff.

## 2026-08-14 owner-approved compact-context launch

The next fresh exact `claude-opus-5` xhigh session must use the new
`RP7_OPUS_COMPACT_CONTINUATION_PACKET_2026-08-14.md` as its staged read order and
evidence map. This is an owner-approved quota optimization only: it changes the
read order, not any acceptance standard, finding, D026 requirement, fence
requirement, identity assertion, or safety gate.
`KICKOFF_CLAUDE_RP7_CAP_OVERRIDE_REPAIR_2026-08-13.md` now points to that read
order instead of a startup full-read of all four current files. The repair is
**not complete**: REQUIRED-1 (CRLF continuation), REQUIRED-2 (two-subject
six-pair fence), and the row-9 literal D026 fixtures remain open. No acceptance
is claimed here or in the packet.
