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
