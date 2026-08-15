# Lead finding — the 2026-08-14 Pathscope identity table was unsatisfiable — 2026-08-15

Type: **documentation defect in an audit contract**. Not a defect in
`pathscope_prover.py` and not a change to any subject byte.

## What was wrong

`KICKOFF_CODEX_PATHSCOPE_FINAL_OVERRIDE_AUDIT_2026-08-14.md` froze four
artifacts at commit `40091b2b795be3339dc0df7014df6bfc091e4eca` with one
byte-size and one SHA-256 each. The repository sets `* text=auto` in
`.gitattributes`, so every Markdown file has two legitimate identities: the
Git-object (LF) form and the Windows working-tree (CRLF) form. The table mixed
the two.

Re-derived by the Lead on 2026-08-15 from an isolated worktree at `40091b2b`
(`C:\PSRETRY`, `git status --porcelain` empty):

| artifact | 2026-08-14 kickoff | worktree (CRLF) form | Git-object (LF) form | kickoff row matched |
|---|---|---|---|---|
| `pathscope_prover.py` | 137520 / `28848d60…` | 137520 / `28848d60…` | 137520 / `28848d60…` | both (file has no CRLF delta) |
| `SELF_QA_PATHSCOPE.md` | 311577 / `f99d972f…` | 315514 / `75e5581e…` | 311577 / `f99d972f…` | **Git-object only** |
| `STATUS_PATHSCOPE.md` | 12359 / `6c2c409a…` | 12359 / `6c2c409a…` | 12197 / `4fb9ab89…` | **worktree only** |
| `PATHSCOPE_FINAL_OVERRIDE_REPAIR_REPORT_2026-08-14.md` | 21579 / `3dae5d6d…` | 21897 / `595ff2a4…` | 21579 / `3dae5d6d…` | **Git-object only** |

No single derivation method reproduces all four rows. An auditor hashing the
checkout fails two rows; an auditor hashing Git objects fails one. The contract
was therefore impossible to satisfy as written.

## Why it matters

The instruction in that kickoff was to "re-derive every identity before any
execution and require exact equality to the table." A conscientious auditor
following it would have failed the identity phase for a reason that has nothing
to do with the code under audit, and would have been correct to record a
finding. That is a spurious blocking path built into the contract.

It also puts one sentence of the 2026-08-14 transport-block record in doubt.
`PATHSCOPE_FINAL_OVERRIDE_CODEX_T1_AUDIT_2026-08-14.md` states "All four
artifact byte sizes matched the frozen kickoff table." Under the enforced
read-only sandbox that auditor could not run Git, so any size it observed came
from the checkout — and the checkout does not match two of the four rows. The
claim is not reproducible. It is recorded here as an inaccuracy in a
non-executing BLOCK record, not as a verdict change: the verdict was `BLOCK` on
transport grounds and remains `BLOCK`.

## What was done about it

The owner-authorized 2026-08-15 retry
(`KICKOFF_CODEX_PATHSCOPE_RETRY_AUDIT_2026-08-15.md`) carries a **dual-form**
identity table: worktree bytes and SHA-256, Git blob bytes and SHA-256, and the
blob OID, for all four artifacts, with both forms required to match and the
exact derivation command given for each.

This correction adds information to the contract and removes a false-failure
path. It cannot create a false PASS: every original identity value still appears
in the table and is still required, in the derivation mode where it is correct.
No subject byte changed; the frozen commit is still `40091b2b`.

## Standing rule proposed

Any future frozen-identity table in this repository states the derivation mode
explicitly, and for text files subject to `* text=auto` states both forms or
pins the Git blob OID. A bare "bytes / SHA-256" pair on a Markdown file in this
repo is ambiguous by construction.

No host, deployment, credential, service, broker, ARM, order, TESTNET/mainnet,
Pine, parity, MTC, or trading authority is created or implied by this record.
