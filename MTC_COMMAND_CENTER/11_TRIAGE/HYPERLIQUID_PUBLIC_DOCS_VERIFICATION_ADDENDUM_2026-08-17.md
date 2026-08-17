# Hyperliquid Public-Docs Verification Addendum — 2026-08-17 (overnight)

**Artifact class:** unaccepted supplemental research draft; documentation only
**Method:** live fetches of official Hyperliquid GitBook documentation pages on 2026-08-17
(evening), performed by the Claude Lead session. **Zero account, API-key, wallet, login, or
exchange actions.** No SDK calls, no endpoints touched.
**Authority:** none. This addendum informs Package 7 (official exchange reverification) and the
conditioning of Package 1; it does NOT replace Package 7 and does not authorize any architecture
freeze, implementation, or account action.

## 1. Why this exists

The consumed T2 review of the Bridge V2 deferral backlog required (finding 2) that official
exchange verification precede or explicitly condition exchange-dependent Package 1 decisions
(subaccount eligibility, agent-wallet behavior, same-symbol netting, margin mode, API limits).
This addendum captures what the **public official documentation** states today, clearly separated
from what it does NOT state.

## 2. Facts from official documentation (with source pages)

### 2.1 Sub-accounts — VOLUME-GATED (high-impact fact)

Source: `https://hyperliquid.gitbook.io/hyperliquid-docs/trading/sub-accounts`

- "Up to 10 sub-accounts can be created after reaching $100,000 in volume."
- "Every additional $100M in volume enables the ability to create 1 additional sub-account, up to
  a maximum of 50 sub-accounts."
- "Sub-accounts share the same fee tiers as the master account, but referral discounts do not
  apply to sub-accounts."
- "The number of API wallets available starts at 3 for all master accounts and increases by 2 per
  sub-account."

**Implication for the backlog (not a decision):** the preferred one-risk-bucket-per-subaccount
model in `docs/30` assumes subaccounts are available. A fresh or low-volume account has **zero**
sub-accounts until $100,000 cumulative volume. Package 1 worker-isolation design must treat
subaccount availability as **conditional**, with an explicit fallback (e.g. virtual books under
one account) until the volume gate is confirmed passed for the actual account in use. Whether the
volume gate applies identically on TESTNET is **UNKNOWN** from public docs.

### 2.2 API wallets (agent wallets)

Source: `https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/nonces-and-api-wallets`

- A master account can approve API wallets to sign on behalf of the master account or any of its
  sub-accounts; sub-accounts do not have private keys.
- Nonces are tracked **per signer** (user address or agent address); "The 100 highest nonces are
  stored per address"; nonces must fall within (T − 2 days, T + 1 day) of block time.
- "It's recommended to use separate API wallets for different sub-accounts" (nonce collision
  avoidance).
- Deregistration/expiry: an unnamed API wallet is deregistered when a new unnamed one is approved;
  wallets can expire; wallets are pruned if the registering account no longer has funds. After
  deregistration, generate a new agent wallet on future use.

**Implication:** per-worker API-wallet assignment is the documented pattern; wallet lifecycle
(expiry/pruning) must be part of any worker-identity contract.

### 2.3 Margin modes

Source: `https://hyperliquid.gitbook.io/hyperliquid-docs/trading/margining`

- "Cross margin is the default…"; isolated margin is supported; some assets are "strict isolated"
  (margin cannot be removed).
- Leverage is any integer from 1 to the asset's max; max leverage varies by asset (3x–40x per the
  perpetual-assets page); maintenance margin is half of initial margin at max leverage.
- HIP-3 DEXs support a "no cross" mode.
- Whether cross and isolated positions can coexist on the same asset, and hedge-mode questions,
  are **not addressed** on this page.

### 2.4 API rate limits

Source: `https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/rate-limits-and-user-limits`

- IP-based: aggregated weight limit **1200 per minute**; exchange requests weigh
  `1 + floor(batch_length / 40)`; info requests weigh 2 / 20 / 60 by type, with per-item
  surcharges on list endpoints; explorer requests weigh 40.
- WebSocket: max 10 connections, 30 new connections/min, 1000 subscriptions, 10 unique users
  across user-specific subscriptions, 2000 messages/min sent, 100 inflight posts.
- Address-based: **"sub-accounts treated as separate users"**; accrual of 1 request per 1 USDC
  traded cumulatively with an initial buffer of 10,000 requests; when throttled, one request per
  10 seconds still allowed; cancels get `min(limit + 100000, limit * 2)`; open-order cap 1000
  plus 1 per 5M USDC volume, capped at 5000.

**Implication:** multi-worker designs get per-subaccount address-based budgets (good), but share
the IP-based 1200/min weight and the 10-connection WebSocket cap on one VPS (a real shared
constraint for worker topology).

## 3. NOT established by official documentation (UNKNOWN — preserve)

1. **Same-symbol netting / hedge mode:** the fetched official pages (margining, perpetual assets,
   sub-accounts) do not state whether one account can hold simultaneous long and short positions
   on the same asset. Third-party sources consistently describe one-way netting per account with
   sub-accounts as the workaround, but **no official sentence was found**; treat as UNKNOWN until
   Package 7 verifies (documentation dig or supervised account-level check under its own gate).
2. **TESTNET parity:** whether the sub-account volume gate, API-wallet counts, and rate limits
   apply identically on testnet is not stated in the fetched pages.
3. **Cross+isolated coexistence on one asset:** not stated.
4. **Current account's own eligibility:** cumulative volume of the actual account in use is an
   account fact, not a docs fact — only Package 7 (separately gated) may establish it.

## 4. Boundary

This addendum is background material for Package 7 and for conditioning Package 1. It is
unaccepted, grants no authority, froze no architecture decision, and involved no account or
network action beyond public documentation reads.
