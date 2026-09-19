# P012 Path 1 — first REAL own-account evidence session, executed 2026-09-14 16:03Z-18:08Z (owner's hands; Lead read-only)

Authorization: owner chat 2026-09-14 ~15:04Z "P1-1 Go … P1-5 now … P1-6 yes" on the Gemini-audited packet `P012_PATH1_REAL_CAPTURE_PACKET_20260914.md` (CT13 bbb307a4); Path D signed decision leaves Path 1 to the owner's own authority; the Bridge stays DISARMED and never touched money. Division of labour held: the owner connected his wallet, set BTC to 1x / isolated (verified on his screenshot 15:58Z), typed sizes/prices and clicked every Buy/Sell; the Lead read the trade page in its own Claude-in-Chrome tab (same wallet shown), verified every fill through the public Info API, never clicked an order control, never saw a key or password. The owner's mid-session "24 h full authorization to place and close trades" was declined (model rule; real money).

Account: the owner's own Hyperliquid **mainnet** wallet `0x1E26…AC49` (full address in the run-root records and in the owner's chat), unified account, spot USDC 102.36 before / **102.643876 after** (net +0.28 USDC). NOT the testnet wallet whose API key sits on KVM2. Mainnet history before today: 0 fills, 0 funding (clean forward slate; A1 forward-only satisfied trivially).

## Fills (public `userFills`; all BTC perp; venue fee schedule of this account 0.0432 % taker / 0.0144 % maker)
| # | UTC | side | px | sz BTC | fee USDC | maker/taker | oid | role |
|---|---|---|---|---|---|---|---|---|
| T2 | 16:03:30 | B | 78462 | 0.00016 | 0.005423 | taker (crossed) | 544824403105 | **declared: taker fill** |
| T3 | 16:05:15 | B | 78451 | 0.00013 | 0.004405 | taker | 544825781088 | **declared: near-$10 fill** (10.20 USD notional; venue minimum 10) |
| dup | 16:06:11 | B | 78438 | 0.00013 | 0.004405 | taker | 544826486048 | auxiliary (owner clicked twice) |
| T1 | 16:14:34 | B | 78410 | 0.00016 | 0.001806 | **MAKER** (crossed=false; limit ALO) | 544829071300 | **declared: maker fill** |
| T4 | 18:08:43 | A | 78993 | 0.00058 | 0.019792 | taker | 544923730764 | close (closedPnl +0.320856), auxiliary |
Total fees 0.035831 USDC (estimate in the packet: ≈ 3 cents — held).

## Funding (public `userFunding`)
| UTC | coin | usdc | rate | position |
|---|---|---|---|---|
| 17:00:00 | BTC | −0.000571 | 0.0000125 | 0.00058 |
| 18:00:00 | BTC | −0.000572 | 0.0000125 | 0.00058 |
Hourly cadence evidenced on the owner's own account (the repository sources had it NOT VERIFIED). Candidate funding interval for the intake: `[2026-09-14T16:03:30Z, 2026-09-14T18:08:43Z)` (position open) containing exactly the two settlements; the exact-once inventory and the interval declaration are the capture tool's job.

## Evidence status
- This note is the Lead's read of the public API at 18:10Z, not the capture. The immutable native bytes, SHA-256 sidecars, re-query identity check and ownership signature come from the read-only capture tool (lane P1CAP, queued on Codex Plus; owner P1-6 yes) once built and reviewed; the venue keeps the history, so the capture can run later.
- Fee package declaration: T2, T3, T1 (exactly N=3); T4 and the duplicate are not declared. Funding package: one complete interval with two events; funding M remains a separate owner decision after these observations.
- Ownership proof (P1-4): pending the local signing page (built with the capture tool); attestation-only fallback.
- Nothing here closes a Section-19 row or a signed risk; the owner's human review (Q1) and the intake validation follow. Price risk taken: ≈ $45 for two hours; outcome +0.28 USDC.

Recorded by Claude Opus 5 Lead (b9df29), 2026-09-14 18:12Z.
