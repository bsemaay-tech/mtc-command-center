# Hyperliquid Account Structure — Subaccounts, Agent Wallets, Netting

Wayfinder research ticket: [#51](https://github.com/bsemaay-tech/mtc-command-center/issues/51)
Date: 2026-08-23
Scope: read-only research against primary sources only. No authenticated calls, no
testnet interaction, no order-shaped requests were made. One harmless unauthenticated
public read (`POST https://api.hyperliquid.xyz/info {"type":"meta"}`) was performed as
explicitly owner-approved in the ticket.

Sources consulted (all primary):
- Official Hyperliquid docs at `hyperliquid.gitbook.io/hyperliquid-docs` (GitBook)
- Official `hyperliquid-python-sdk` source on GitHub (`hyperliquid-dex/hyperliquid-python-sdk`, `master` branch)
- Local broker adapter: `IBKR_PAPER_BRIDGE/bridge/broker/hyperliquid.py` (this repo)
- Public unauthenticated `info` endpoint (`type: meta`), one call, read-only

This document states facts only. It does not recommend a design (subaccounts vs.
vaults vs. single account for per-strategy isolation) — that decision belongs to
tickets #40 and #42. Where the primary sources were silent, the fact is marked
**UNKNOWN** rather than inferred or guessed; where a conclusion is *derived* by
combining two cited primary facts (not stated verbatim in one place), it is labeled
**derived**.

---

## 1. Subaccounts

1.1. A master account can create **up to 10 sub-accounts after reaching $100,000 in
cumulative trading volume**. Every additional $100M of volume unlocks 1 more
sub-account, up to a hard cap of **50 sub-accounts**.
Source: [Sub-accounts — Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/sub-accounts)

1.2. Sub-accounts **share the same fee tier** as the master account, but **referral
discounts do not apply to sub-accounts**.
Source: [Sub-accounts — Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/sub-accounts)

1.3. A sub-account has **no private key of its own**. To act on behalf of a
sub-account, the signature is produced by the master account's key (or an API/agent
wallet approved by the master — see §2), and the request carries a `vaultAddress`
field set to the sub-account's own onchain address:
> "To perform actions on behalf of a subaccount or vault signing should be done by
> the master account and the vaultAddress field should be set to the address of the
> subaccount or vault."
`vaultAddress` is documented as: "If trading on behalf of a vault or subaccount, its
Onchain address in 42-character hexadecimal format." It appears on the `order`,
`cancel`, `cancelByCloid`, `scheduleCancel`, `modify`, `batchModify`,
`updateLeverage`, `updateIsolatedMargin`, `twapOrder` and `twapCancel` actions.
Source: [Exchange endpoint — Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint)

1.4. Each sub-account **has its own onchain address**, distinct from the master's
(fact 1.3) and from every other sub-account's. Hyperliquid's Info endpoints
(`user_state` / `clearinghouseState`, etc.) return positions, margin and balances
**for the address that is queried** — this is how every read in this codebase's
broker adapter works today (`self.info.user_state(self.account_address)`,
`IBKR_PAPER_BRIDGE/bridge/broker/hyperliquid.py:223, 240, 1023-1025`). Combining
these two facts: **a sub-account's positions/margin/balances are held and reported
separately (isolated) from the master account and from other sub-accounts** — this
is a **derived** conclusion; no single doc page states "sub-account margin is
isolated" in those words, and the dedicated sub-accounts page is explicitly silent
on the isolation question when asked directly.
Sources: [Exchange endpoint](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint) · `hyperliquid.py:223,240,1023-1025` (this repo)

1.5. **The number of API (agent) wallets available starts at 3 for the master
account and increases by 2 per sub-account** (verbatim from the sub-accounts page).
Source: [Sub-accounts — Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/sub-accounts)
— See also §2.5 for a partially-overlapping secondary-source figure that could not
be verified verbatim in the primary doc text and should not be relied on.

1.6. **UNKNOWN (primary docs silent):** the exact UI/API creation steps for a
sub-account beyond the volume-eligibility gate in 1.1. The page states the
eligibility threshold only, not the creation procedure.
Source: [Sub-accounts — Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/sub-accounts)

1.7. The official `hyperliquid-python-sdk` `Exchange` class exposes
`create_sub_account(name: str)` (submits a `createSubAccount` action),
`sub_account_transfer(sub_account_user, is_deposit, usd)` and
`sub_account_spot_transfer(sub_account_user, is_deposit, token, amount)` for
funding/defunding a sub-account's perp and spot balances respectively.
Source: `hyperliquid/exchange.py`, [hyperliquid-dex/hyperliquid-python-sdk](https://github.com/hyperliquid-dex/hyperliquid-python-sdk) (`master`)

1.8. **Recommended practice per the official docs: use a separate API/agent wallet
per sub-account when trading more than one in parallel.** Rationale given: nonces
are tracked per signer (see §2), so if the same agent wallet signs for two
sub-accounts, they share one nonce tracker.
Source: [Nonces and API wallets — Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/nonces-and-api-wallets)

---

## 2. Agent (API) wallets

2.1. An API wallet (== "agent wallet") is created/authorized via an
**`approveAgent`** action signed by the master account. Per the official docs:
> "A master account can approve API wallets to sign on behalf of the master account
> or any of the sub-accounts."
Source: [Nonces and API wallets — Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/nonces-and-api-wallets)

2.2. The official SDK's `approve_agent(name=None)` method generates a fresh random
private key locally (`agent_key = "0x" + secrets.token_hex(32)`), derives its
address, then has the **master wallet** sign an `approveAgent` action naming that
address as the new agent. It returns both the exchange's response and the raw new
agent private key — the agent key is generated client-side and never touches
Hyperliquid's infrastructure until its address is approved.
Source: `hyperliquid/exchange.py`, [hyperliquid-dex/hyperliquid-python-sdk](https://github.com/hyperliquid-dex/hyperliquid-python-sdk) (`master`)

2.3. **Agent wallets can sign trading actions.** This is not stated as a plain
sentence on the Exchange-endpoint doc page (queried directly, it is **silent** on
whether `order`/`cancel` require the master's own signature) — but it is
conclusively demonstrated by this repo's own production broker adapter: the *only*
key ever handed to the SDK's `Exchange` client is the agent wallet key
(`HL_API_WALLET_KEY` env var, never the master account's own key), and that
`Exchange` instance is used for every trading call the bridge makes — order
placement (`bulk_orders`), cancellation (`cancel_by_cloid`), stop modification
(`modify_order`), and position flattening (`market_close`).
Source: `IBKR_PAPER_BRIDGE/bridge/broker/hyperliquid.py:1954-1966` (`_build_sdk_clients`,
constructs `Exchange(wallet, base_url, account_address=self.account_address)` from
`api_wallet_key` only), `:440-442` (`bulk_orders`), `:1298-1301` (`cancel_by_cloid`),
`:836-846` (`modify_order`), `:885-891` (`market_close`)

2.4. **Whether agent wallets can sign fund-moving actions (withdraw, transfer,
vault transfer) or approve further agents is UNKNOWN from the primary docs
consulted.** The Exchange-endpoint doc page was queried directly and twice
confirmed **silent** on this: it documents the parameters/response shape of
`withdraw3`, `usdSend`, and `vaultTransfer` but states no signer restriction either
way. A first-pass automated read of that page produced a table claiming `order`,
`cancel`, `withdraw3`, `usdSend`, `vaultTransfer` and `approveAgent` are all
"master-only" — that table was internally contradictory (it claimed `order` itself
requires the master's own signature, which fact 2.3 disproves from this repo's own
running code) and could not be reproduced on a second, narrower query of the same
page. It is **not** relied on anywhere in this document.
Source: [Exchange endpoint — Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint) (queried twice, silent both times on this specific point)

2.5. **The official SDK does not enforce any such restriction client-side.**
Reading the SDK source directly: `withdraw_from_bridge`, `usd_transfer`,
`vault_usd_transfer` and `approve_agent` all sign with `self.wallet` — the exact
same wallet object the `Exchange` instance was constructed with — with no branch,
check, or comment distinguishing an agent-keyed instance from a master-keyed one.
If Hyperliquid restricts these actions to master-only signatures, that restriction
is enforced **server-side only**; nothing in the client SDK or the exchange-endpoint
doc page confirms or denies that server-side behavior.
Source: `hyperliquid/exchange.py`, [hyperliquid-dex/hyperliquid-python-sdk](https://github.com/hyperliquid-dex/hyperliquid-python-sdk) (`master`) —
methods `withdraw_from_bridge`, `usd_transfer`, `vault_usd_transfer`, `approve_agent`, and the `Exchange.__init__` signature: `wallet, base_url=None, meta=None, vault_address=None, account_address=None, spot_meta=None, perp_dexs=None, timeout=None`

2.6. Multiple independent secondary (non-primary) sources found during search
converge on the claim that agent wallets can trade but **cannot** withdraw or
transfer funds, framed as an intentional blast-radius-limiting design (a leaked
agent key can trade the account but not drain it). This is **plausible and
consistent** with 2.4/2.5 but could not be confirmed verbatim against the specific
primary docs and SDK source examined for this ticket. Flagged here as a secondary
claim, not a cited fact — a decision-maker relying on "agents cannot withdraw" as a
security boundary should get a primary-source confirmation (e.g. by testing on
testnet, or finding the specific doc sentence) before depending on it.

2.7. Agent wallets come in two kinds:
> "Unnamed API wallets: Deregistered when a new unnamed wallet is registered."
> "Named API wallets: Deregistered when a new ApproveAgent action uses a matching
> name."
Source: [Nonces and API wallets — Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/nonces-and-api-wallets)

2.8. Agent wallets can be **pruned** (invalidated) for three documented reasons:
> "(1) The wallet is deregistered... (2) The wallet expires. (3) The account that
> registered the agent no longer has funds."
**UNKNOWN:** the docs confirm agent wallets expire but do not state the expiry
**duration** anywhere on the page consulted.
Source: [Nonces and API wallets — Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/nonces-and-api-wallets)

2.9. Nonce scoping: nonces are **tracked per signer** — "the user address if signed
with private key ... or the agent address if signed with an API wallet." The
exchange retains "the 100 highest nonces per address," and a nonce must fall within
`(T - 2 days, T + 1 day)` of the current block timestamp. Re-registering a
previously-deregistered agent address risks replay of old signed actions once its
nonce history is pruned.
Source: [Nonces and API wallets — Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/nonces-and-api-wallets)

2.10. Per §1.5, the count of API wallets available scales with sub-accounts (3 base
+ 2 per sub-account), and per §1.3 an agent wallet can be scoped to a specific
sub-account by setting `vaultAddress` on each signed action — i.e., **one agent
wallet can be used across the master account and every sub-account** (by varying
`vaultAddress` per request), but the docs *recommend* (§1.8) giving each sub-account
its own agent wallet to avoid nonce-tracker contention when trading sub-accounts in
parallel. There is no hard technical restriction found in the primary sources
limiting a given agent wallet to a single sub-account.
Source: [Nonces and API wallets](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/nonces-and-api-wallets) · [Exchange endpoint](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint)

2.11. This repo's current bridge implementation does **not** use agent-wallet
scoping to a sub-account at all: `grep -in "vault\|subaccount\|sub_account\|sub-account"` across
`IBKR_PAPER_BRIDGE/bridge/broker/hyperliquid.py` returns **zero matches**. The
`Exchange` client is always constructed with `account_address=self.account_address`
and no `vault_address` (`hyperliquid.py:1965`); there is exactly one account context
in the code today — the master account (or whatever single address
`HL_ACCOUNT_ADDRESS` names).
Source: `IBKR_PAPER_BRIDGE/bridge/broker/hyperliquid.py:1954-1966` (this repo)

---

## 3. Position netting

3.1. The official docs' worked example response for the perpetuals account-summary
read (`clearinghouseState`) shows each entry in `assetPositions` tagged with
**`"type": "oneWay"`**:
```json
"assetPositions": [
  {
    "position": { "coin": "ETH", "szi": "0.0335", "entryPx": "2986.3", ... },
    "type": "oneWay"
  }
]
```
The docs page does not add explanatory prose defining what `"oneWay"` means beyond
its presence in the example — but the label itself, plus 3.2 and 3.3 below, are
consistent with the widely-understood behavior that Hyperliquid nets to a single
position per asset per account (no simultaneous long+short "hedge mode").
**No primary-source sentence explicitly stating "hedge mode is not supported" or
"long and short cannot coexist" was found** in the pages checked — this specific
framing is therefore **UNKNOWN** as a directly quoted doc fact, only as a
**derived** one from 3.1–3.3.
Source: [Perpetuals — Info endpoint — Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint/perpetuals)

3.2. This repo's broker adapter independently encodes the same one-position-per-coin
assumption, defensively, in two separate places:
- `portfolio_evidence()`: while building the positions map from `assetPositions`,
  if the same `coin` key appears twice it returns a `CONFLICTING` /
  `HL_POSITION_CONFLICTING` result rather than merging or summing the rows
  (`hyperliquid.py:1489-1499`).
- `symbol_snapshot()`: after filtering positions to one symbol, `len(matching) > 1`
  is treated as `HL_POSITION_CONFLICTING`, an error state, not a valid hedge
  (`hyperliquid.py:1106-1111`).
This is the bridge author's own defensive assumption, not an Hyperliquid doc
statement — cited here as corroborating internal evidence, not as a primary
Hyperliquid-side fact.
Source: `IBKR_PAPER_BRIDGE/bridge/broker/hyperliquid.py:1106-1111, 1489-1499` (this repo)

3.3. The margin mode (cross vs. isolated) is described in two places with slightly
different framing that this research did not fully reconcile:
- Margining page: **"When opening a position, a margin mode is selected"** — implies
  the choice is made per-position (i.e., different open positions on the same
  account can independently be cross or isolated).
- Contract specifications page: lists **"Account type | Per-wallet cross or
  isolated margin"** as a contract-spec parameter — implies a wallet-level setting.
Both are quoted verbatim from primary docs; this document does not attempt to
resolve the apparent tension, flagging it instead as a nuance worth a follow-up
primary-source check if the exact mechanics matter for a design decision.
Sources: [Margining — Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/margining) ·
[Contract specifications — Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/contract-specifications)

3.4. Some assets are **restricted to isolated-only margin** at the exchange level
(`"onlyIsolated": true, "marginMode": "strictIsolated"` in the asset's universe
entry) — this is a per-**asset** property, not a per-account or per-subaccount one.
Confirmed directly from the live, unauthenticated, owner-approved
`POST https://api.hyperliquid.xyz/info {"type":"meta"}` call made for this research
(HTTP 200; e.g. `CASHCAT` and several delisted assets such as `HPOS`, `RLB`,
`UNIBOT`, `OX`, `FRIEND`, `SHIA`, `PANDORA`, `NFTI` all currently carry this flag in
the live response).
Source: `POST https://api.hyperliquid.xyz/info {"type":"meta"}` (public, unauthenticated, read-only; called 2026-08-23)

---

## 4. Vaults

4.1. Vaults are described (current HyperEVM-based generation) as containers
"Builders can create and tokenize... with fully customizable accounting," enabling
"trustless read and write operations on HyperCore."
Source: [Vaults — Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/vaults)

4.2. A vault can "trade onchain via CoreWriter, or ... delegate any number of
authorized agents using CoreWriter," with "full access to Core features including
spot and HIP-3 in all quote assets."
Source: [Vaults — Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/vaults)

4.3. The current HyperEVM vault design is documented as "a strict improvement over
the 'legacy' HyperCore vaults" introduced in 2023, which "do not support HIP-3 or
spot trading" — i.e., there are two vault generations, with different capabilities.
Source: [Vaults — Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/vaults)

4.4. Hyperliquid documents a **protocol-run vault**, HLP (Hyperliquidity Provider),
which "provides liquidity to Hyperliquid through multiple market making strategies,
performs liquidations, supplies USDC in Earn, and accrues a portion of trading
fees" — distinct from user-created vaults.
Source: [Protocol vaults — Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/vaults/protocol-vaults)

4.5. The docs maintain separate guidance pages "For vault leaders" and "For vault
depositors" — i.e., the vault model is explicitly built around a **leader/depositor
relationship** (a vault can accept external depositors and share performance with
them), which is a materially different concept from a sub-account (§1), which
belongs solely to one master account with no external depositors or profit-sharing
mechanics documented anywhere in the sub-accounts page.
Sources: [For vault leaders](https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/vaults/for-vault-leaders) ·
[For vault depositors](https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/vaults/for-vault-depositors) ·
[Sub-accounts](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/sub-accounts)

4.6. Like a sub-account, a vault is acted on via the same `vaultAddress` field
mechanism described in fact 1.3 (the exchange-endpoint doc's `vaultAddress`
description explicitly covers "a vault or subaccount" together), and the SDK's
`vault_usd_transfer(vault_address, is_deposit, usd)` moves funds in/out of a vault
by address, mirroring `sub_account_transfer` (fact 1.7).
Sources: [Exchange endpoint](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint) ·
`hyperliquid/exchange.py`, [hyperliquid-dex/hyperliquid-python-sdk](https://github.com/hyperliquid-dex/hyperliquid-python-sdk)

4.7. **UNKNOWN (primary docs did not state directly):** an explicit sentence
contrasting "use a vault" vs. "use a sub-account" for pure internal per-strategy
capital isolation with no external depositors. Facts 4.1-4.6 are the closest
primary-sourced material; the leader/depositor framing (4.5) suggests vaults carry
product surface area (external depositors, profit-sharing, likely a public
leaderboard presence) that a pure internal isolation use case would not need — but
no doc page states this as a recommendation either way.

---

## 5. Rate limits

5.1. REST requests share an aggregated weight budget of **1200 per minute per IP
address**.
Source: [Rate limits and user limits — Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/rate-limits-and-user-limits)

5.2. Weight per request type (as published):
- Exchange (trading) API actions: weight `1 + floor(batch_length / 40)`
- Info requests weighted **2**: `l2Book`, `allMids`, `clearinghouseState`,
  `orderStatus`, `spotClearinghouseState`, `exchangeStatus`
- Info requests weighted **20** (default for everything else documented)
- `userRole`: weight **60**
- Additional weight per 20 returned items on: `recentTrades`, `historicalOrders`,
  `userFills`, `userFillsByTime`, `fundingHistory`, `userFunding`,
  `nonUserFundingUpdates`, `twapHistory`, `userTwapSliceFills`,
  `userTwapSliceFillsByTime`, `delegatorHistory`, `delegatorRewards`,
  `validatorStats`
- `candleSnapshot`: additional weight per 60 items returned
- Explorer API: weight **40** per request; `blockList` additionally rate-limited to
  1 per block
Source: [Rate limits and user limits — Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/rate-limits-and-user-limits)

5.3. WebSocket limits (per connection/IP as documented): max **10** connections,
max **30** new connections per minute, max **1000** subscriptions, max **10** unique
users across user-specific subscriptions, max **2000** messages sent to Hyperliquid
per minute, max **100** simultaneous in-flight `post` messages.
Source: [Rate limits and user limits — Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/rate-limits-and-user-limits)

5.4. EVM JSON-RPC (`rpc.hyperliquid.xyz/evm`): max **100 requests per minute**.
Source: [Rate limits and user limits — Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/rate-limits-and-user-limits)

5.5. A **second, per-address** limit exists independent of the per-IP one: **1
request per 1 USDC traded cumulatively since the address's inception**, with an
**initial buffer of 10,000 requests** for a brand-new address. Once exhausted, the
address is limited to **1 request per 10 seconds**. Order cancellations get a
separate, larger allowance: `min(limit + 100000, limit * 2)`.
Source: [Rate limits and user limits — Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/rate-limits-and-user-limits)

5.6. Open-order limit: **1000 resting orders by default**, plus one additional
order per **5,000,000 USDC of volume**, capped at **5000 total**. Once an address
already has 1000+ open orders, additional reduce-only or trigger orders are
rejected.
Source: [Rate limits and user limits — Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/rate-limits-and-user-limits)

5.7. Because the per-address limit (5.5) is keyed by address and a sub-account has
its own address (fact 1.4), **derived**: a sub-account accrues its own independent
per-address request buffer, separate from the master account's and from other
sub-accounts'. This was not stated verbatim on the rate-limits page (which does not
mention sub-accounts at all) — it follows from combining 1.4 and 5.5.

5.8. Unified Account and Portfolio Margin abstraction modes (fact-adjacent, from
§ account-abstraction-modes doc, cited for completeness since it is a limit, not a
rate limit per se) are capped at **50,000 user actions per day**; Standard/Manual
mode "has no such restriction" documented.
Source: [Account abstraction modes — Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/account-abstraction-modes)

---

## 6. Local codebase cross-check (facts only, no recommendation)

6.1. `IBKR_PAPER_BRIDGE/bridge/broker/hyperliquid.py` has **no subaccount or vault
support today** — confirmed by exhaustive grep (`vault|subaccount|sub_account|sub-account`,
case-insensitive) across the entire 2266-line file: **zero matches**.

6.2. The adapter detects one of the account-abstraction modes described in §
account-abstraction-modes (`_detect_account_mode`, `hyperliquid.py:1968-1978`,
calling `self.info.query_user_abstraction_state`) and branches its balance read
(`account()`, `hyperliquid.py:202-235`) between a `unifiedAccount`-specific
`spot_user_state` path and a standard `user_state` path — i.e., the code already
distinguishes "Unified Account" mode from standard mode (fact-consistent with §
account-abstraction-modes), but has no equivalent branch for sub-account or vault
addressing.

6.3. `HyperliquidBroker.__init__` takes a single `account_address` and a single
`api_wallet_key` (`hyperliquid.py:106-118`); there is exactly one credential pair
and one traded address per `HyperliquidBroker` instance in the code as it stands
today — any multi-subaccount or multi-vault usage would currently require multiple
`HyperliquidBroker` instances (one per address) rather than being handled inside a
single instance, since the class has no parameter or code path for a second
address/`vaultAddress`.

---

## Sources (all fetched/consulted 2026-08-23)

- [Sub-accounts — Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/sub-accounts)
- [Nonces and API wallets — Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/nonces-and-api-wallets)
- [Exchange endpoint — Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint)
- [Account abstraction modes — Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/account-abstraction-modes)
- [Rate limits and user limits — Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/rate-limits-and-user-limits)
- [Vaults — Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/vaults)
- [For vault leaders — Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/vaults/for-vault-leaders)
- [For vault depositors — Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/vaults/for-vault-depositors)
- [Protocol vaults — Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/vaults/protocol-vaults)
- [Margining — Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/margining)
- [Contract specifications — Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/contract-specifications)
- [Perpetuals — Info endpoint — Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint/perpetuals)
- [hyperliquid-dex/hyperliquid-python-sdk](https://github.com/hyperliquid-dex/hyperliquid-python-sdk) — `hyperliquid/exchange.py` (`master` branch, raw source read directly)
- `POST https://api.hyperliquid.xyz/info {"type":"meta"}` — public, unauthenticated, read-only call, HTTP 200, made 2026-08-23
- `IBKR_PAPER_BRIDGE/bridge/broker/hyperliquid.py` (this repo, local worktree base commit `764da27f`)
