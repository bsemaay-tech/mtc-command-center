# 06 — Hyperliquid Setup Checklist (testnet = paper)

**Audience:** Barış (one-time manual setup) + the build-day agent (P0 depends on this).
**Goal:** get a Hyperliquid **testnet** account + an **API wallet** ready so the bridge can connect,
read the account, and place a bracket (entry + native SL/TP trigger orders) — all with fake money.

Replaces the old IBKR/TWS setup. Hyperliquid is a pure API (no desktop terminal, no ports, no
socket-client toggles) — setup is much shorter than IBKR.

---

## 0. Testnet vs mainnet

| | Testnet (paper) | Mainnet (real money) |
|---|---|---|
| Money | Fake (faucet USDC) | Real |
| Bridge default | hardcoded `network="testnet"` (`bridge/app.py:203`) | triple-lock (`hyperliquid.py:2165-2169`) never evaluates unless that word is first changed to `mainnet` |
| URL | `app.hyperliquid-testnet.xyz` | `app.hyperliquid.xyz` |
| Use for | ALL of v1 (P0-P3) | never in v1 |

Do everything below on **testnet**.

---

## 1. Wallet + testnet account

1. You need an EVM wallet (e.g. MetaMask / Rabby) — Hyperliquid logs in by connecting a wallet.
2. Go to **`https://app.hyperliquid-testnet.xyz`** and connect your wallet.
3. Get testnet USDC from the faucet (the testnet UI has a faucet; if not, the Hyperliquid Discord
   testnet-faucet channel). You want a few hundred (fake) USDC to trade with.
4. Confirm you can see a balance on the testnet UI. This is your paper account.

---

## 2. Create an API wallet (agent wallet) — the safety-critical step

Do NOT put your main wallet private key in the bridge. Hyperliquid supports **API wallets**
(a.k.a. agent wallets): a delegated key that can place/cancel orders **but cannot withdraw funds**.

1. On the testnet site, open **More → API** (or the "API Wallets" / "Agent Wallets" section).
2. Create/authorize a new API wallet. This gives you an **API wallet private key**.
3. Note two values:
   - your **main account address** (the wallet you funded) → env `HL_ACCOUNT_ADDRESS`
   - the **API wallet private key** → env `HL_API_WALLET_KEY`
4. The bridge signs orders with the API wallet key and references the main account address. Because
   the API wallet cannot withdraw, even a fully compromised bridge cannot move your funds. **This is
   the single most important safety property — never use the main wallet key.**

> When you later go to mainnet (out of v1 scope), repeat this on the mainnet site with a mainnet API
> wallet — and only ever fund it with an amount you accept losing.

---

## 3. Environment variables the bridge reads

```
HL_ACCOUNT_ADDRESS = 0x...        # your funded (testnet) main account address
HL_API_WALLET_KEY  = 0x...        # the API/agent wallet private key (trade-only, no withdraw)
ANTHROPIC_API_KEY  = ...          # optional (LLM veto; v1 default OFF anyway)
XAI_API_KEY        = ...          # optional (Grok market-sentiment regime)
TELEGRAM_BOT_TOKEN = ...          # optional (notifications)
TELEGRAM_CHAT_ID   = ...          # optional
# HL_LIVE_ACK is intentionally NOT set — it is only for mainnet, and not in v1.
```

Set these in your shell / a local `.env` the bridge loads (git-ignored). Never commit them.

---

## 4. Config sanity (config/bridge.yaml)

Confirm before P0:
```
mode: paper
broker: { network: testnet, coin: BTC, leverage: 1, margin_mode: isolated }
```
`leverage: 1` = no leverage (safest for the plumbing phase). Raising it is a deliberate change and
trips the `max_leverage` cap unless you also raise that.

---

## 5. Verify — the P0 smoke test (build-day agent runs this, with your approval)

Once the bridge code exists, `tools/smoke_p0.py` will, against testnet:

1. Connect with the API wallet (Info + Exchange, `TESTNET_API_URL`).
2. Pull the account summary (equity, available margin) and a live BTC 1h candle.
3. Place a small **entry + SL/TP trigger group** (`grouping="positionTpsl"`), confirm the SL trigger
   is resting on the book, then cancel/flatten.
4. Write every step to the JSON decision log.

**Pass = all steps succeed on testnet and the SL trigger appears as a real resting order.**

> Per repo rules, the agent runs this **only with your explicit in-session approval** — it is an
> exchange action (even though it is testnet/fake money).

---

## 6. Quick reference card

```
Site:     app.hyperliquid-testnet.xyz   (testnet = paper; mainnet is out of v1 scope)
Fund:     faucet USDC (fake)
Key:      API / agent wallet ONLY (cannot withdraw) — never the main wallet key
Env:      HL_ACCOUNT_ADDRESS (main addr) + HL_API_WALLET_KEY (agent key)
Config:   network: testnet, coin: BTC, leverage: 1, margin_mode: isolated
Safety:   native SL/TP trigger orders rest on the book (survive a bridge crash)
Proof:    P0 places entry + SL/TP trigger group on testnet, SL resting, then cancels
```

If any step is unclear when you get there, ask and I'll walk you through the exact Hyperliquid UI
path for the current version.
