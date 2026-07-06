# 06 — TWS / IB Gateway Setup Checklist

**Audience:** Barış (one-time manual setup) + the build-day agent (P0 depends on this).
**Goal:** get the Interactive Brokers **paper** account into a state where the bridge can connect,
read the account, and place a bracket order **without a human clicking anything** — because P2 runs
unattended and a single hidden confirmation popup silently freezes every order behind it.

This is a paper (fake-money) setup. Nothing here touches real money. The bridge additionally
refuses any non-paper port by design (see `01_ARCHITECTURE.md §11`), but do the setup on paper.

---

## 0. Which app: TWS vs IB Gateway

| | TWS (Trader Workstation) | IB Gateway |
|---|---|---|
| Has full charts/UI | Yes | No (headless-ish, just the API bridge) |
| Best for | First setup, watching it work, debugging | Long unattended P2/P3 running (lighter, more stable) |
| Paper port | **7497** | **4002** |
| Live port (bridge REFUSES) | 7496 | 4001 |

**Recommendation:** use **TWS on port 7497** for the first setup and P0/P1 (you can see what's
happening). Switch to **IB Gateway on 4002** later for the multi-day unattended P2 run. The bridge
supports both paper ports; you only change `broker.port` in `config/bridge.yaml`.

---

## 1. Account (one-time, if not done)

1. Have an Interactive Brokers account (live or just the paper-only signup).
2. Enable the **paper trading account** from Client Portal → Settings → Paper Trading Account.
   IBKR gives you a separate paper username (usually your live username + a suffix).
3. Download **Trader Workstation** (latest/stable) and/or **IB Gateway** from IBKR's site.
4. Log in to TWS **with the paper username** (the login screen has a "Paper Trading" toggle —
   make sure it's the paper login, not live).

> Sanity check: once logged in, TWS title bar / account dropdown should clearly say the account is
> a paper/demo account. If you see your real balance, stop — you're on the live login.

---

## 2. API settings in TWS (the part that matters)

Open **File → Global Configuration → API → Settings** and set exactly these:

| Setting | Value | Why |
|---|---|---|
| **Enable ActiveX and Socket Clients** | ✅ ON | The bridge talks over the socket API. Off = no connection at all. |
| **Socket port** | **7497** (TWS paper) | Must match `broker.port` in the bridge config. |
| **Read-Only API** | ⬜ **OFF** | We send orders. Left ON, every order attempt is rejected. |
| **Bypass Order Precautions for API Orders** | ✅ **ON** | **THE critical one.** Left OFF, TWS pops a modal ("size exceeds…", "confirm stop order…") that the API cannot dismiss — the order hangs in an unknown state until a human clicks. Fatal for unattended P2. |
| **Trusted IPs** → add | `127.0.0.1` | The bridge runs on the same machine (localhost). |
| **Master API client ID** | leave blank / default | The bridge uses client ID 17 (configurable). |
| **Allow connections from localhost only** | ✅ ON | Extra safety; the bridge is localhost-only anyway. |

Click **OK / Apply**.

### 2b. Order Precautions tab (belt-and-suspenders)

Even with "Bypass Order Precautions for API Orders" ON, some TWS builds still surface a few
precaution dialogs. Go to **Global Configuration → API → Precautions** (or **Orders → Precautions**)
and make sure the API-order precautions (size cap warning, price-percentage constraint, missing
stop-loss warning, etc.) are **not set to require manual confirmation** for API orders. When in
doubt, the P0 smoke test (below) is the real proof: if a bracket transmits and you did NOT have to
click anything, the setup is correct.

---

## 3. Market data type (expected, not a bug)

A paper account without a paid market-data subscription returns **delayed (15-min) data**. This is
**normal and fine** for the 1-hour strategy. The bridge explicitly requests delayed data
(`reqMarketDataType(3)`) and treats it as expected — do **not** interpret "delayed" as an error.

If you happen to have live market-data subscriptions on the account, even better, but it is not
required for v1. The bridge logs which data type it actually received at startup.

---

## 4. Auto-restart (for unattended P2)

TWS and IB Gateway force a restart roughly once every 24 hours (around 23:45 US-Eastern). For the
unattended multi-day run you want this to be an **auto-restart**, not an auto-logout:

- **Global Configuration → Lock and Exit → Auto restart** → set to auto-restart (not "Auto logoff").
- Set the restart time to a market-closed hour.

The bridge is designed to survive this restart (reconnect + re-subscribe bars + re-protect any open
position — see `01_ARCHITECTURE.md §6.1`), but auto-restart (vs auto-logout) is what lets it come
back at all without you logging in again.

---

## 5. Verify — the P0 smoke test (build-day agent runs this, with your approval)

Once the bridge code exists, the P0 smoke script (`tools/smoke_p0.py`, build plan task 8) will,
against the **running** TWS paper session:

1. Connect on 127.0.0.1:7497.
2. Pull the account summary (equity, buying power) and a delayed AAPL quote.
3. Place a small bracket order (entry + stop + optional target) **and confirm it transmits with
   NO TWS popup**, then cancel it.
4. Write every step to the JSON decision log.

**Pass = all four steps succeed and you did not have to click a single TWS dialog.** If a dialog
appeared, revisit step 2/2b (Bypass Order Precautions).

> Per repo rules, the agent runs this **only with your explicit in-session approval** — it is a
> broker action. It is still paper, but the guardrail stands.

---

## 6. Quick reference card

```
App:        TWS (setup/P0-P1)  →  IB Gateway (unattended P2/P3)
Login:      PAPER username (not live)
Port:       7497 (TWS paper)  /  4002 (Gateway paper)     [bridge refuses 7496/4001 = live]
API:        Enable Socket Clients = ON
            Read-Only API        = OFF
            Bypass Order Precautions for API Orders = ON   ← most important
            Trusted IP           = 127.0.0.1
Data:       delayed 15-min = EXPECTED, not an error
Restart:    Auto-restart (not auto-logout), market-closed hour
Proof:      P0 smoke places+cancels a bracket with zero manual clicks
```

If any step is unclear when you get there, ask and I'll walk you through the exact TWS menu path
for your version.
