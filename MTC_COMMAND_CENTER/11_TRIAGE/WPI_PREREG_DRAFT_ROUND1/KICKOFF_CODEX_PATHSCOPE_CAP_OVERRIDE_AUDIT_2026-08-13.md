# Pathscope cap-override T1 execution audit - Codex

Dispatch only after every `PENDING-FILL-AFTER-REPAIR` field below is replaced
from the frozen committed bytes. Any unfilled field is a dispatch BLOCK.

Auditor: fresh independent `gpt-5.6-sol`, effort `high`, T1. Read-only except
one new verdict file. No resume/continue, sub-delegation, Git mutation, host or
network contact, deployment, credentials, ARM, orders, TESTNET, mainnet, Pine,
parity, or trading action.

Owner authority: `WPI_OWNER_DECISIONS_2026-08-13.md` section 4 authorizes this
single extra repair/audit cycle; it waives no acceptance standard.

Frozen subject commit: `2fb3eac05f8da716609549179a7961aa692eae6b`

| artifact | bytes | SHA-256 |
|---|---:|---|
| `pathscope_prover.py` | `131599` | `553A97E932A190B4967B8F1F39C546D7558D9066ABD30B3AECA1913FED27E2EB` |
| `SELF_QA_PATHSCOPE.md` | `240907` | `3EFEA7F34521BC02D2FADAB102A7A59AE25D1C6A6BEC8E1D93A6AF47510A92FB` |
| `STATUS_PATHSCOPE.md` | `6981` | `85E6C03CEC42F306B6D001E90EC919AC77304EF5226AB6C1C6B7A25D6B783D4A` |
| `PATHSCOPE_CAP_OVERRIDE_REPAIR_REPORT_2026-08-13.md` | `19739` | `389D7688295BD3637292D660A908DE7B97B331173FADDF4C63585DAEFFD88D28` |

Read the r3 Codex verdict, the cap-override Lead finding, the supplemental
findings, the repair report, and all four frozen artifacts. Re-derive every
identity before execution.

Mandatory audit:

1. Extract and run the published PowerShell harness verbatim. Require clean
   outer completion, no stderr, exact recorded transcript/hash reproduction,
   deterministic pairs, and unchanged identities afterward.
2. Independently reproduce C-2 at prefix, `env`, and `export` sites and verify
   later absolute members, allowlisted-first lists, empty-plus-path lists,
   whitespace command text, and ordinary relative paths never disappear.
3. Verify quoted/escaped whitespace remains one pathname: the Lead case
   `X="$ROOT dir/escape"` must remain rejected, not split into allowed pieces.
4. Inspect the complete member grammar for adjacent silent sinks, URI/endpoint
   ambiguity, provenance loss, and any value that produces zero terminal
   accounting despite carrying a pathname or executable command text.
5. For every claimed regression closure, require literal execution against the
   actual committed pre-fix blob and repaired bytes. Current-only RED labels or
   narrated predictions are supplemental, not D026 evidence.
6. Verify no out-of-scope tracked or untracked delta attributable to the audit.

Write only
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_CAP_OVERRIDE_CODEX_T1_AUDIT_2026-08-13.md`.

Verdict must be exactly PASS, PASS-WITH-NITS, REQUEST_CHANGES, or BLOCK.
PASS-WITH-NITS may contain no required repair. This is the authorized final T1
audit cycle; any required finding returns the lane to the owner boundary.
