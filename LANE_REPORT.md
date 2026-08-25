# Lane Y report - CRLF ledger-hash repair

## Result

The owner-authorized T1 repair is implemented on `fix/crlf-ledger-attr-20260825`.

- The exact identity-bearing schema path is pinned to LF in the root `.gitattributes`.
- The canonical ledger hash and every evidence Git blob are unchanged.
- The local schema checkout now has LF bytes and hashes to the ledger's recorded identity.
- A new regression test proves a forced-`core.autocrlf=true` fresh checkout preserves that
  identity.
- D026 is satisfied: the test failed with the diagnosed CRLF hash when the pin was absent in a
  scratch clone and passed when only the pin was applied.
- Full Bridge suite: `1382 passed, 1 warning in 142.64s`.
- No push, merge, deployment, host contact, credential access, or trading action occurred.

## Candidate files

1. `.gitattributes`
2. `IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py`
3. `MTC_COMMAND_CENTER/11_TRIAGE/CRLF_LEDGER_FIX_2026-08-25/FIX_EVIDENCE.md`
4. `LANE_REPORT.md`

Detailed commands, hashes, all evidence blob OIDs, and verbatim RED/GREEN output are in
`MTC_COMMAND_CENTER/11_TRIAGE/CRLF_LEDGER_FIX_2026-08-25/FIX_EVIDENCE.md`.

## T1 independent acceptance

Audit tier: **T1**. Round 1 returned `BLOCK` solely because the Claude harness denied Python
execution; it reported zero required repairs. The second and final fresh round used the same exact
`claude-opus-5` model at high effort with a constrained Python permission and returned
`PASS-WITH-NITS` with zero required repairs.

The accepting auditor independently ran:

- Full suite: `1382 passed, 1 warning in 112.87s`.
- Focused canonical and fresh-checkout tests: `2 passed in 0.78s`.
- `git diff --cached --check`: clean.

It independently reconfirmed the candidate scope, attribute precedence, all seven unchanged
evidence blob OIDs, and the D026 LF/CRLF hash discriminator. Its four low/very-low nits were
explicitly optional: git-less export handling, ambient Git config hermeticity, an additional
scratch-index OID assertion, and the expected suite-duration difference. No security Gate 6 was
required because no auth, secret, network, host, deployment, broker, or economic surface changed.
