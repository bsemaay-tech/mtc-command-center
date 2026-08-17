# Bridge V2 Deferral Backlog — T2 Review Status

**Date:** 2026-08-17
**Artifact class:** T3 factual status record; no review, repair, implementation, or authorization is launched by this file
**Candidate:** `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_V2_DEFERRAL_BACKLOG_2026-08-17.md`
**Reviewed repository HEAD:** `033546fb08baad2aa606bf6cb96e08ca64a04a5d`

## Review identity and verdict

- Tier: **T2**, documentation/evidence, one reviewer and one round.
- Reviewer: fresh exact `gpt-5.6-sol` at `medium` effort.
- Verdict: **REQUEST_CHANGES**.
- Required findings: **3**.
- The reviewer worked read-only. No candidate, code, documentation, memory, lock, host, deployment, trading, credential, Pine, parity, MTC, ARM, or order state was mutated.
- The ordinary T2 round is consumed. No repair/re-review may be launched without a narrow explicit owner exception for the current corrected candidate.

## Required findings

### 1. Partial-fill recovery status is overstated or incomplete

Partial-fill recovery exists under schema **v5**, but v5 is opt-in and inactive under the default **v4** schema. Operational migration/activation evidence and final independent acceptance remain unknown. The backlog must not let “implemented offline” imply that the feature is active, accepted, or available under the default runtime schema.

### 2. Official exchange verification must precede exchange-dependent architecture decisions

Package 7's current official Hyperliquid verification must precede, or explicitly condition, Package 1 decisions that depend on exchange behavior. Subaccount eligibility, agent-wallet behavior, same-symbol netting, margin mode, and API limits must not be frozen from stale or unverified assumptions and then checked afterward.

### 3. Package 5 cannot carry a blanket T1 classification

Package 5 combines local observability work with an “offline decision-parity gauge.” Purely observational/export/mock UI mechanics may be T1, but parity semantics or protected decision-logic inspection can be T0 and separately owner-gated under highest-risk-wins. The package must be split or each sub-surface classified before work; the current blanket T1 label is too broad.

## Optional nits

1. Qualify `docs/30_V2_BACKEND_AND_DASHBOARD_DESIGN_DECISIONS.md` citations as **HEAD citations**, because the dirty B8 insertion changes later working-copy line numbers.
2. Add a direct source citation for the funding-evidence/reconciliation claim at backlog line 54.
3. Normalize hybrid classifications against the definitions in Section 2 so labels do not mix categories without an explicit explanation.

These are optional nits and are not the reason for the non-accepting verdict.

## Explicit UNKNOWNs and evidence exclusions

1. No committed acceptance record was located that resolves TS-P1-004 beyond the partial-fill contract's `PROPOSED` status.
2. Current Hyperliquid subaccount, wallet, same-symbol netting, margin-mode, and API-limit facts remain intentionally unverified.
3. The dirty `docs/30` B8 working copy and dirty AI-memory working copies were not treated as accepted authority.

UNKNOWN does not mean false. It means the reviewed evidence did not establish the claim and the backlog must preserve that uncertainty.

## Acceptance and authorization boundary

The backlog remains a useful inventory and sequencing draft, but it is **unaccepted**. It authorizes nothing, including:

- no backlog repair or additional review round;
- no architecture decision or Package 1–8 kickoff;
- no code, schema, migration, activation, merge, or release change;
- no VPS/Hostinger/KVM2/GATEA-STAGING contact or deployment;
- no credentials, provider calls, broker/exchange actions, TESTNET or MAINNET;
- no ARM/DISARM/KILL, orders, economic controls, Pine, parity, or MTC strategy changes.

The next permitted step is an owner decision: either preserve the backlog unaccepted, or authorize exactly one fresh T2 review of a corrected exact candidate. Such an exception would not reset the repository-wide cap and would grant no implementation or host/trading authority.
