# Lane T Report — WP-P0-28 VEN-A Documentation Half

**Date:** 2026-08-25

**Lane:** T

**Audit tier:** T2

**Status:** DOCUMENTATION HALF COMPLETE; independent T2 review PASS

**Eligibility read:** **EXCLUDED — G6-gated T0 owner action, not authorized, not started, not performed**

## Scope result

- Refreshed the old Package-7 venue record without editing it.
- Closed the current hedge-mode wording and documented the one-way signed-position surface from official primary sources.
- Verified cross/isolated coexistence within an account, while preserving same-asset dual-mode as UNKNOWN.
- Verified explicit agent-wallet custom expiry up to 180 days; no default duration is assumed.
- Preserved testnet volume-gate behavior, actual account eligibility, and venue IP allowlisting as UNKNOWN with the public primary-source searches recorded.
- Wrote the settled Q6 account-binding spec, virtual-books fallback, per-book/venue-net reconciliation, opposing-same-symbol rule, and instrument-universe consumer mapping.
- Did not reopen Q6 and did not touch Pine, parity, `MTC_V2`, Bridge, schema, account, credential, authenticated endpoint, host, testnet, mainnet, or trading surfaces.

## Primary sources

All accessed 2026-08-25:

- Hyperliquid official docs: Sub-accounts; Referrals; Nonces and API wallets; Exchange endpoint; API notation; Margining; Clearinghouse; Account abstraction modes; Portfolio margin; Perpetual assets; Rate limits and user limits; API overview; Testnet faucet; Perpetuals Info endpoint; full documentation corpus (`llms-full.txt`).
- Hyperliquid official GitHub organization: `hyperliquid-dex/hyperliquid-python-sdk`, specifically `examples/basic_sub_account.py` and `hyperliquid/info.py`.
- Local provenance inputs: old record at `887ec60fbfd9b42fb57b6c14dad8a968b1e4a713`; branch-only account-structure research at `ea6ad389e22661b329cd2910c60b06ce80141795`; settled Q6/#40 and #48 folds in the current planning set.

No blog, forum, community SDK, secondary article, authenticated page, or private account data was used to upgrade a claim.

## Exact staged paths

1. `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_28_VENUE_FACTS_2026-08-25/VENUE_VERIFICATION_RECORD_2026-08-25.md`
2. `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_28_VENUE_FACTS_2026-08-25/ACCOUNT_BINDING_AND_FALLBACK_SPEC.md`
3. `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_28_VENUE_FACTS_2026-08-25/LANE_REPORT.md`

## Commit record

- Base: `46f5bafbf82f3366c8bc7ee08f6f0eee08d46138`
- Work-package commit: `faafc19775a3047d2613812ff334abdc6bb86a34`
- Required subject: `docs(wp-p0-28): venue-fact verification + Q6 binding specs, doc half (T2, lane T 2026-08-25)`

## Verification record

- Worktree/branch/base preflight: clean `feature/wp-p0-28-venue-facts-20260825` at `46f5bafb…`.
- Public-source boundary: only unauthenticated public HTTPS documentation/source reads.
- Exact-path check: only the three files listed above are authorized for staging.
- Lead checks at the frozen work-package commit: exact three-file scope; 16 VERIFIED / 4 UNKNOWN fact dispositions; all required consumer IDs and fail-closed virtual-book terms present; `git diff --check` PASS; clean worktree.
- Independent T2 reviewer: Codex `gpt-5.6-sol`, medium effort, fresh read-only session (GLM-5.2 preferred route was unavailable for executable review through the installed wrapper).
- Independent T2 verdict: **PASS**. The reviewer reproduced the exact scope, official-source traceability, material venue claims, UNKNOWN boundaries, settled-Q6 binding, deterministic fallback rules, consumer edges, and clean worktree.
