# Package 7 — Official Hyperliquid Documentation Quote Dump

**Collected by:** Claude (Fable) Lead, live WebFetch/WebSearch of official pages, 2026-08-17
(evening + night, two collection passes). **Method:** public documentation reads only — zero
account, API-key, wallet, login, SDK, or endpoint actions. Summaries below are the fetch tool's
extraction of each page; quoted sentences are verbatim from the official pages.

## D1. Sub-accounts — https://hyperliquid.gitbook.io/hyperliquid-docs/trading/sub-accounts

- "Up to 10 sub-accounts can be created after reaching $100,000 in volume"
- "Every additional $100M in volume enables the ability to create 1 additional sub-account, up to a maximum of 50 sub-accounts"
- "Sub-accounts share the same fee tiers as the master account, but referral discounts do not apply to sub-accounts"
- "The number of API wallets available starts at 3 for all master accounts and increases by 2 per sub-account"
- Page does NOT address: technical creation steps, transfer rules, margin/clearinghouse treatment, testnet vs mainnet differences.

## D2. Nonces and API wallets — https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/nonces-and-api-wallets

- "A master account can approve API wallets to sign on behalf of the master account or any of the sub-accounts"
- Sub-accounts do not have private keys; actions for a sub-account are signed by the master (or an approved API wallet) with the vaultAddress field set to the sub-account address.
- "Nonces are tracked per signer, which is the user address if signed with private key of the address, or the agent address if signed with an API wallet"
- "The 100 highest nonces are stored per address"; nonces must fall within (T - 2 days, T + 1 day) of block timestamp.
- "It's recommended to use separate API wallets for different subaccounts"
- Removal scenarios: unnamed wallet deregistered when a new unnamed one is approved; wallets can expire; wallets pruned when the registering account no longer has funds. "Generate a new agent wallet on future use to avoid unexpected behavior" after deregistration.
- No explicit total API-wallet limit stated ON THIS PAGE (but see D1's count rule).

## D3. Rate limits — https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/rate-limits-and-user-limits

- IP-based REST: "aggregated weight limit of 1200 per minute"; exchange request weight `1 + floor(batch_length / 40)`; info weights 2 / 20 / 60 by type; per-item surcharges ("additional rate limit weight per 20 items returned"; candleSnapshot per 60 items); explorer weight 40.
- WebSocket: max 10 connections; 30 new connections/min; 1000 subscriptions; 10 unique users across user-specific subscriptions; 2000 messages/min sent; 100 inflight posts.
- Address-based: "sub-accounts treated as separate users"; "1 request per 1 USDC traded cumulatively" with "initial buffer of 10000 requests"; throttled to one request per 10 seconds when limited; cancels `min(limit + 100000, limit * 2)`; open orders 1000 + 1 per 5M USDC volume, cap 5000.

## D4. Margining — https://hyperliquid.gitbook.io/hyperliquid-docs/trading/margining

- "Cross margin is the default, which allows for maximal capital efficiency by sharing collateral between all other cross margin positions."
- "Isolated margin is also supported, which allows an asset's collateral to be constrained to that asset."
- "Some assets are strict isolated, which functions the same as isolated margin with the additional constraint that margin cannot be removed."
- "Leverage can be set by a user to any integer between 1 and the max leverage. Max leverage depends on the asset."
- HIP-3 DEXs: "no cross" mode (isolated with margin removal enabled, no cross margin).
- Page does NOT address: cross+isolated coexistence on one asset; simultaneous long and short (hedge mode).

## D5. Perpetual assets — https://hyperliquid.gitbook.io/hyperliquid-docs/trading/perpetual-assets

- "Max leverage varies by asset, ranging from 3x to 40x. Maintenance margin is half of the initial margin at max leverage."
- Page does NOT discuss position netting, one-position-per-asset, opposing orders reducing positions, or hedge mode.

## D6. Account abstraction modes — https://hyperliquid.gitbook.io/hyperliquid-docs/trading/account-abstraction-modes

- Four modes: Unified Account ("single balance for each asset. This balance collateralizes all cross margin positions in that asset and is unified with spot balance in that asset"); Portfolio Margin ("single portfolio unifying all eligible assets, which are currently HYPE, BTC, USDC, USDT"); Manual/Standard ("separate perp and spot balances, separate DEX balances. Cross margin applies to each DEX separately"); DEX Abstraction (discontinued).
- "Builder code addresses must be in standard mode to accrue builder fees"
- "Portfolio margin and unified account are limited to 50k user actions per day. Standard mode has no such restrictions."
- API note: on unified/portfolio-margin modes "all balances and holds in the spot clearinghouse state. Individual perp dex user states are not meaningful."

## D7. Portfolio margin — https://hyperliquid.gitbook.io/hyperliquid-docs/trading/portfolio-margin

- "Under portfolio margin, a user's spot and perps trading are unified for greater capital efficiency."
- "Sub-accounts are still treated separately under portfolio margin."
- Described as "a generalization of cross margin". Does not address isolated-margin mode or same-asset position handling.
- Access constraint: ">$5M in weighted volume or account value >$10k", total account value "<$25M", plus supply/borrow caps. No explicit alpha/live designation on the page.

## D8. Testnet — faucet page https://hyperliquid.gitbook.io/hyperliquid-docs/onboarding/testnet-faucet and API docs https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api

- Testnet faucet requires a mainnet deposit on the same address; claims 1,000 mock USDC at app.hyperliquid-testnet.xyz/drip.
- API: same requests work against testnet base URL `https://api.hyperliquid-testnet.xyz` (mainnet: `https://api.hyperliquid.xyz`).
- NOT stated anywhere fetched: whether the sub-account volume gate, API-wallet counts, or rate limits differ on testnet.

## Known gaps in this dump (candidate UNKNOWNs)

1. Same-symbol netting / hedge mode: no official sentence found (third-party consensus says one-way netting per account; NEVER cite that as VERIFIED).
2. Cross+isolated coexistence on the same asset: not addressed.
3. Testnet parity of limits/gates: not addressed.
4. The actual trading account's cumulative volume / sub-account eligibility: account fact — ACCOUNT-LEVEL-ONLY by definition.
5. Sub-account margin/clearinghouse treatment details beyond D7's "treated separately": limited.
