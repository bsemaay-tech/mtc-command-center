# One authorization request — reading four public web addresses, once

**To the owner.** This is your decision to make; it is written for you.
Nothing has been fetched. Nothing will be fetched unless you say yes.

*Lead's note: this request reaches you only after the packet behind it has been audited. Nothing
below is authorized by the audit — the audit checked that the request describes what the program
actually does.*

## In one paragraph

Three of our production records (the instrument record, the fee record and the funding record) are
missing their evidence. They point at official Hyperliquid documentation pages, but we only hold
copies fetched on 31 August 2026, and some facts have no captured source at all. I am asking for
permission to read four public web addresses one time, save exactly what comes back, and take a
fingerprint (a SHA-256 digest) of each response so nobody can quietly change it later. That is the
whole request. Nothing is bought, nothing is logged into, nothing is traded, and no number is
written into any record.

## What exactly would be fetched

**4 distinct web addresses. 6 HTTP requests. That 6 is a maximum, not an estimate** — three of the
addresses are read once each, and the fourth is asked three different questions. The program cannot
issue a seventh request under any circumstance: there is no paging, no automatic retry, and it will
not follow a redirect to a different address.

Six requests, in this order, one at a time, with a one-second pause between them:

1. The public fee-schedule page — `hyperliquid.gitbook.io/.../trading/fees`
2. The public funding-rules page — `hyperliquid.gitbook.io/.../trading/funding`
3. The public liquidations page — `hyperliquid.gitbook.io/.../trading/liquidations`
4. The public market-metadata response — `api.hyperliquid.xyz/info`, asking for `meta`
5. The public asset-context response — `api.hyperliquid.xyz/info`, asking for `metaAndAssetCtxs`
6. The public funding history for BTC between the moment you authorize and the moment we fetch —
   `api.hyperliquid.xyz/info`, asking for `fundingHistory`

Requests 1–3 are ordinary documentation web pages, the same ones anyone can open in a browser.
Requests 4–6 go to Hyperliquid's public information endpoint, which is the same data any visitor to
their website receives. **No account is involved, and no password, key, wallet or signature is sent.**

**Data volume:** we expect roughly one to three megabytes in total, the same order as opening six
web pages once — but that is an estimate, so the program does not rely on it. It refuses to read
more than 4 MiB from any single response. Six responses at that limit is 24 MiB, and that is the
true hard ceiling, not the estimate.

**Where from:** Hyperliquid's own public documentation site and their own public information
endpoint. No third-party site, no data vendor, no paid archive.

**Where to:** one new folder, `C:\tmp\P012_PUBLIC_CAPTURE_V1`. That folder name is written into the
authorized scope itself, so the fingerprint you approve fixes *where* the files land as well as
*what* is fetched. The program has no option to be pointed somewhere else, and it refuses to start
if that folder already has anything in it.

## What will never be touched

- No login, no API key, no private key, no wallet address, no signature.
- No account data of any kind — not our balances, not our positions, not our order history.
- No orders, no cancels, no transfers, no trading action, on mainnet or anywhere else.
- No paid service. Hyperliquid's downloadable historical archive is deliberately excluded because
  their own page says the person downloading it pays the transfer cost — that would be a purchase.
- No live connection that stays open, no subscription, no third-party software.
- Nothing outside `C:\tmp\P012_PUBLIC_CAPTURE_V1` is written. Existing files are never overwritten.

## When: now-and-forward, not backwards

The rule is **capture-forward**: the clock starts at the moment you authorize, not earlier. This is
exactly the answer you already gave (`COST_EFFECTIVE_INTERVAL` and `FUNDING_EFFECTIVE_INTERVAL` =
capture-forward). The capture makes no claim about the past.

There is an honest consequence you should know before deciding, because it is easy to
over-expect: funding on this venue is paid **once an hour**. The window between authorizing and
fetching is minutes, so request 6 will almost certainly come back **empty**. This capture freezes the
*rules* and starts the clock; it does not by itself give the funding record its list of payment
events.

### The one option you are being asked to weigh: history

| Option | What it means | Consequence |
|---|---|---|
| **A — no history (recommended)** | Fetch only the now-and-forward window described above. | Consistent with your existing capture-forward answer. The funding record's event list stays empty and stays refused, and would need a later, separately authorized fetch once real hours have passed. Smallest possible footprint. |
| **B — also fetch past funding history** | Walk backwards through the venue's funding history for BTC, roughly three weeks of hourly entries per request. | Gives real event bytes immediately. But their documentation never says how far back the data goes, so the depth is not guaranteed. More importantly, using those events would mean claiming the funding rules applied in the past — which is exactly the history claim your capture-forward answer refuses. Choosing B is therefore not just "more data"; it reopens a decision you already closed. It also needs more than six requests, so it changes the frozen scope, the fingerprint below, and the program itself — all three would have to be re-issued and re-approved. |

**Recommendation: Option A.** It matches the decision you already made, and it keeps this
authorization as small as it can be. If Option B is ever wanted, it deserves its own request with
its own explanation of the history claim.

## How the result is frozen and reviewed

- Every response is saved byte-for-byte, untouched, in its own file.
- Each file gets a SHA-256 fingerprint, recorded with the exact address it came from and the exact
  time it **arrived** — the clock is read after the response has been fully received, not before it
  was sent, so the recorded time is when we had the bytes.
- All the fingerprints go into one small index file whose own fingerprint is the identity of the
  whole capture. If a single byte anywhere changes later, a `verify` command detects it.
- The program refuses to run twice into the same folder and refuses to overwrite anything, so a
  capture can never be quietly replaced.
- If anything is unexpected — a page that has moved, a response bigger than the limit, or a funding
  answer large enough to have been cut short — the program **stops and reports**. It never quietly
  asks a follow-up question you did not authorize.
- **The capture writes nothing into any production record.** It produces evidence. A human reviewer,
  later, decides what — if anything — that evidence supports.

## What the capture will still NOT close

So there is no surprise afterwards:

- The **fee rounding rule**, the **fixed fee component** and the **minimum fee** stay refused. The
  official page simply does not state them, and silence is not a zero.
- The **liquidation fee class** stays refused. The official liquidation page will be captured and it
  is a genuine official source, but it does not say whether a liquidation fill counts as taker or
  maker — the fact we need is not on it.
- The **account fee-tier evidence** stays refused, because that would need an account login.
- The **funding event list** stays refused (see the hourly-funding point above).
- All **reviewer name** fields stay empty, per your standing answer.
- The **run-manifest** questions stay open; no such record exists yet.

## What stays blocked until you answer

- Refreshing the source evidence behind the instrument, fee and funding records.
- Starting a capture-forward validity window for the fee record and the funding record.
- Having any official, frozen, citable source attached to the liquidation question at all.

Everything else in WP-P0-12 continues meanwhile; nothing else waits on this.

## The exact thing you would be authorizing

A file called `FROZEN_SCOPE.json` holds the six requests, the destination folder, the timing rule,
the limits and the list of things that must never happen. Its fingerprint is:

```
4f112ccf2346fb06f2255f8e15bd194a40c57b8a496b77939f3c5901ff14a88d
```

The program refuses to fetch anything unless it is handed this exact fingerprint **and** an explicit
authorization flag. The same fingerprint is also written inside the program itself, so changing the
scope file alone is not enough — a wider scope would need a changed program too, which is a change
someone has to make and someone has to review. If a single character of the scope changes, the
fingerprint changes and the program refuses. So approving that fingerprint approves exactly that
scope and nothing wider.

An earlier draft of this request carried the fingerprint
`47785841055e12235dc425468c4adbdac1eafdeffce8ce1527058aaeecbe9f0d`. That one is superseded and
must not be approved.

## What I need from you

One line:

- `PUBLIC_CAPTURE = AUTHORIZE, OPTION A` — go ahead with the six requests, now-and-forward only; or
- `PUBLIC_CAPTURE = AUTHORIZE, OPTION B` — as above plus past funding history (re-freeze required); or
- `PUBLIC_CAPTURE = NO` — nothing is fetched; the three records keep their 31 August sources and the
  fields listed above stay refused indefinitely.

Silence means no fetch.
