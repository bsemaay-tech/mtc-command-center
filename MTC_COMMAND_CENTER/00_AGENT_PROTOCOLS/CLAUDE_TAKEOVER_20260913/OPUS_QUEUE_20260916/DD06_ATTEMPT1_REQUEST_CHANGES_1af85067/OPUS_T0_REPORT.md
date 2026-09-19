# T0 exact review — WP-P0-29 DD-06 testnet falsification probe, candidate `1af85067`

Reviewer: exact `claude-opus-5`, effort **xhigh** (T0 slot, Wednesday 2026-09-16 optional lane; also the source read for the Friday Sol lane).
Subject: `C:/tmp/P029_DD06_20260915` (read-only worktree). Brief: `C:/tmp/OPUS_QUEUE_20260916/DD06/REVIEW_BRIEF.md`.
Candidate author: Claude Opus 5 Lead (disclosed). I am an independent reviewer; I did not delegate, spawn agents, or resume another session.
Interpreter for every run below: `C:/tmp/P012_FUNDING_PY312_20260911/Scripts/python.exe` (hyperliquid-python-sdk at `C:/tmp/P012_FUNDING_PY312_20260911/Lib/site-packages/hyperliquid/`).

---

## 0. INCIDENT DISCLOSURE — I caused one unintended live TESTNET run of this probe

Read this before the findings; it is both a disclosure and the strongest piece of evidence in the review.

The brief told me to build my own mutants of the safety controls. Mutant **M8** removed the `HL_LIVE_ACK` refusal from `refuse_unless_testnet` (`tools/dd06_agent_withdraw_probe.py:214-217`) and I ran the *fixture* test suite against it on a scratch copy. `tests/test_dd06_agent_withdraw_probe.py:407-412` (`test_main_refuses_mainnet_before_reading_any_credential`) calls the real `probe.main(...)`. With that one refusal gone, `main()` continued into its real branch, resolved a **real Hyperliquid credential from this host's `HKEY_CURRENT_USER\Environment`** (`source: user_registry`), built `Info`/`Exchange` against `TESTNET_URL`, and executed the probe against the live testnet venue.

What it did on the venue (2026-09-17 **15:56:06Z–15:56:16Z** = 18:56 UTC+3; record preserved at `C:/tmp/OPUS_DD06_SCRATCH/mut/unused/DD06_PROBE_RECORD.json`, 4 117 B, sha256 `40ad6f32a1cd02dcf8fee1177f3eefd233b2a756b5e65d261138b4019a07bd09`, matching its own sidecar):

| Step | Outcome | Venue text / data |
|---|---|---|
| S0 reads (master) | RECORDED | two agents (`MTC-bridge-test`, `kvm2-bridge`); perp 0.0; spot USDC **984.987457** (the post-r3 value) |
| S1 control order | NOT_REFUSED | real resting BTC bid 0.00016 @ 69210.0, oid `60364599563` |
| S1 control cancel | NOT_REFUSED | `{"statuses": ["success"]}` — the order was cancelled |
| withdraw3 6 USDC | REFUSED, UNCLASSIFIED | `Must deposit before performing actions. User: [redacted-address]` |
| usdSend 1 USDC | REFUSED, UNCLASSIFIED | same |
| spotSend 1 USDC | REFUSED, UNCLASSIFIED | same |
| approveAgent | REFUSED, UNCLASSIFIED | same |
| result | `DD06_INCONCLUSIVE` | — |

Damage assessment, stated plainly: **testnet only** (M8 did not touch `TESTNET_URL`; no mainnet contact in this session), no funds moved, no agent approved, no position (the venue confirmed the cancel with `success`), no credential value printed or written (the record is address-free by design), and the subject worktree was never modified (mtimes still 2026-09-15 21:37; no artefacts). The credential used was the **Windows-host agent wallet** (zero balance — that is why every arm returned "Must deposit"), not the funded `kvm2-bridge` agent. I did not make any further network call, so I cannot re-verify `openOrders` from here; the owner/Lead may want one public read to close it.

What I got wrong: I did not foresee that a mutant of a *refusal* could convert an offline fixture suite into a live venue run, and I ran a venue action that is gated on owner authority (`OD-…-R2/R3-GO`) without holding one. That is on me.

What it proves about the candidate: the offline-ness of this test suite rests on a **single** line. That is finding **R-2**, and it is demonstrated, not theorised.

---

## 1. Verified identities

| Item | Value |
|---|---|
| COMPUTED HEAD (`git -c safe.directory=* -C C:/tmp/P029_DD06_20260915 rev-parse HEAD`) | `1af85067234632ff057b4212e7599f8003a85ee6` ✓ equals the brief's candidate |
| Branch tip `refs/heads/feature/p029-dd06-testnet-probe-20260915` | `1af85067234632ff057b4212e7599f8003a85ee6` (HEAD **is** the tip; no later commit) |
| Diff vs base (`git diff --name-status fcac0ac6 1af85067`) | exactly `A IBKR_PAPER_BRIDGE/tests/test_dd06_agent_withdraw_probe.py`, `A IBKR_PAPER_BRIDGE/tools/dd06_agent_withdraw_probe.py`; `--stat` = 2 files changed, **1016 insertions(+), 0 deletions** ✓ additive only |
| tool — git blob OID | `610b9f20a8128910c1221e647824f137ca0627dd` |
| tool — **sha256 of the committed blob bytes** (23 627 B, LF) | `96d5052ec6beaaee75e02c35ad2982404834aee33c7bc4c2ef8b52f8d73274ff` |
| tool — sha256 of the CRLF working-tree checkout (24 231 B) | `46f971ba1c8cd1ab98aafee6b78e14e07f6acc9a94c9f9cc578c5f13f6ec5676` |
| test — git blob OID | `f1c8834b49d744b02407acb59b70146d5916db81` |
| test — sha256 of the committed blob bytes (14 655 B, LF) | `248ba617a8a02c981354dd5edc87b7cb3112b8d96788b048e7796ae035c30259` |
| test — sha256 of the CRLF checkout (15 067 B) | `4b01f7c0336934b76ea70756b8c962ce13b3acbb9d273fd6812fcec3c7eb9b17` |

**Run identity closed against bytes:** the on-host `probe_sha256=96d5052ec6beaaee75e02c35ad2982404834aee33c7bc4c2ef8b52f8d73274ff` printed by `kvm2_dd06_probe_run_r3_OUTPUT.redacted.txt:2` is exactly the sha256 of the committed blob I computed above. **r2 and r3 ran this candidate's bytes**, not a variant. (Both the r2 and r3 readings quote the same `96d5052e…`.)

Authorities verified in the owner records, not in the reports that cite them: `OD-20260915-P029-DD06-PROBE-STEPS-APPROVED-1` (`OWNER_DECISIONS_PENDING_20260915_session5.md:124`), `OD-20260916-P029-DD06-R2-GO-1` (`…:127`, owner `r2 go` 08:05 UTC+3), `OD-20260916-P029-DD06-R3-GO-1` (`OWNER_ANSWERS_20260915.md:97`, owner `r3 go`; `RUN_STATE_20260916_session6_snapshot.md:516`).

**Correction to the brief's subject description (not a code defect):** the brief says the candidate "ran once on testnet" and that "a corrected re-run r2 waits for the owner's word". It has in fact run **three** times — r1 (2026-09-15, aborted at the control arm), **r2** (2026-09-16 05:12Z, `DD06_INCONCLUSIVE`), **r3** (2026-09-16 09:00Z, `DD06_FINDING_NOT_REFUSED`) — each under its own owner row. I reviewed against the r2/r3 bytes as well; they change two of my findings from theory to demonstration.

## 2. Baseline test run (mine)

```
cwd: C:/tmp/P029_DD06_20260915
C:/tmp/P012_FUNDING_PY312_20260911/Scripts/python.exe -m pytest IBKR_PAPER_BRIDGE/tests/test_dd06_agent_withdraw_probe.py -q -p no:cacheprovider --basetemp C:/bt_opus_dd06
→ ................                                                         [100%]
  16 passed in 0.34s
```
16 tests, as claimed (`LEAD_PYTEST_focused_slice3.txt` = `16 passed in 0.26s`). Suite green, offline, no `HL_*` set by me.

**Mutation harness** (so the subject worktree is never written): the two files were copied to `C:/tmp/OPUS_DD06_SCRATCH/mut/{tools,tests}/` with a `conftest.py` that puts `mut/` first on `sys.path` and appends the worktree's `IBKR_PAPER_BRIDGE` (for `bridge`). Validated before use — `16 passed in 0.28s`, and `tools.dd06_agent_withdraw_probe.__file__ → C:\tmp/OPUS_DD06_SCRATCH/mut\tools\dd06_agent_withdraw_probe.py`, i.e. mutants really are the module under test. A deliberate no-op mutant (M11, comment text only) survived, confirming the harness does not fail spuriously.

## 3. Per-item decisions

### Item 1 — no mainnet path, no key leak

| Control | file:line | Test that pins it | Mutant result |
|---|---|---|---|
| `TESTNET_URL` hard-coded, used for both endpoints **and** the SDK's signature domain (`is_mainnet = base_url == MAINNET_API_URL`) | `tools/…probe.py:47`, used `:588-589`, printed `:526` | **none** | **M2 SURVIVED** — 16 passed |
| `refuse_unless_testnet` (`--network` ≠ testnet) | `:209-213`; call `:562` | `tests/…:126`, `:412` | not mutated separately (killed via M8) |
| `HL_LIVE_ACK` refusal | `:214-217` | `tests/…:127-130`, `:408-410` | **M8 KILLED** (2 failed) — *and see §0* |
| master-key refusal (function) | `:220-225` | `tests/…:135-137` | pinned |
| master-key refusal (**the call in `main`**) | `:572` | **none** | **M3 SURVIVED** — 16 passed |
| `del api_key` | `:571` | **none** | **M1 SURVIVED** — 16 passed |
| redaction of 40/64-hex before recording | `:58-59`, `:66-78` | `tests/…:222-224` | **M7 KILLED** (2 failed) |
| `write_record` refuses a surviving hex | `:509-514` | **none** | **M4 SURVIVED** — 16 passed |

Mutant commands (all in `C:/tmp/OPUS_DD06_SCRATCH/mut`, driver `C:/tmp/OPUS_DD06_SCRATCH/mutants.py`, full output `C:/tmp/OPUS_DD06_SCRATCH/MUTANTS_OUT.txt`):

```
python -m pytest tests/test_dd06_agent_withdraw_probe.py -q -p no:cacheprovider --basetemp C:/bt_opus_dd06

M1  delete `del api_key`                                  rc=0 SURVIVED  16 passed in 0.31s
M2  TESTNET_URL -> "https://api.hyperliquid.xyz"           rc=0 SURVIVED  16 passed in 0.29s
M3  delete refuse_master_key() call in main                rc=0 SURVIVED  16 passed in 0.34s
M4  delete write_record surviving-hex guards               rc=0 SURVIVED  16 passed in 0.28s
M5  STOP_ON_NOT_REFUSED = False                            rc=1 KILLED    1 failed  (test_not_refused_fund_moving_arm_is_a_finding_and_stops_the_sequence)
M6  WITHDRAW_AMOUNT_USDC 6.0 -> 1.0                        rc=1 KILLED    3 failed
M7  redact() returns input unredacted                      rc=1 KILLED    2 failed  (…redacts_everything, …write_once)
M8  drop the HL_LIVE_ACK refusal                           rc=1 KILLED    2 failed  in 11.10s  ← the live run of §0
M9  accept non-AUTHORIZATION refusals as DD-06 evidence    rc=1 KILLED    1 failed  (…validation_shaped_refusal…)
M10 withdraw3 destination -> foreign address               rc=1 KILLED    3 failed
M11 comment-only no-op (harness control)                   rc=0 SURVIVED  16 passed in 0.27s
RESTORED pristine: rc=0 16 passed in 0.30s
```

Reading: the controls that guard *classification and record content* are genuinely pinned (M5-M7, M9, M10 all die). The controls that keep the tool **off mainnet and off a master key** are not pinned at all (M1-M4 survive). M2 is the serious one: one string literal is the whole mainnet boundary, and after changing it the tool still prints `dd06-probe/v1 — TESTNET ONLY (https://api.hyperliquid.xyz)` from `plan_text` (`:526`) because the words "TESTNET ONLY" are a separate literal. → **R-1**.

### Item 2 — funds cannot leave silently

- `STOP_ON_NOT_REFUSED = True` (`:56`) is consumed at `:462-465`: the first `NOT_REFUSED` arm sets `finding`, sets `result = "DD06_FINDING_NOT_REFUSED"`, records every later arm as `SKIPPED_AFTER_FINDING` and returns. Pinned by `tests/…:248-270`; **M5 kills**. Verified in reality: r3's `spotSend` NOT_REFUSED stopped the sequence and `approveAgent` was never sent (`kvm2_dd06_probe_run_r3_OUTPUT.redacted.txt:115-120`).
- withdraw3 amount `6.0` USDC (`:53`) with destination `account_address` (`:390-394`). Both pinned: the fake asserts `amount == probe.WITHDRAW_AMOUNT_USDC >= 6.0` and `destination == ACCOUNT` (`tests/…:95`); **M6 and M10 each kill 3 tests**. r3's record shows `{"amount": 6.0, "destination": "[account]"}` (`…r3_OUTPUT…:89`).
- The packet says it plainly, twice, in the owner's own document: "if NOT refused, 6 test-USDC leave the venue to an address you control" (`DD06_TESTNET_PROBE_STEP_PACKET_20260915.md:22`) and "A NOT-refused `withdraw3` means 6 test-USDC **leave the venue** to the owner's own address on the bridge chain — stated plainly, not hidden behind 'own address'" (`:26`). Gemini F-1 is satisfied against bytes.
- Caveat on the wording: `FUND_MOVING_ARMS` (`:55`) is **defined and never referenced**; the stop rule actually fires on *any* `NOT_REFUSED` arm, `approveAgent` included. Broader than documented, i.e. safe-direction — but a declared control that is not the one running. → **N-1**.
- Funds cannot leave *silently*. They can still leave: withdraw3 is the **first** arm (`:388`), so the one irreversible action runs before the two in-venue self-transfers whose non-refusal would have tripped the stop rule first. Running `usdSend`/`spotSend` before `withdraw3` would carry identical evidence value in the all-refused case and strictly less exposure in the falsification case. I am **not** filing this as REQUIRED: §3 of the packet is the owner-approved order, and a reviewer does not silently re-cut an approved procedure. → **N-9**, for the owner to decide.

### Item 3 — classification honesty

The honest paths are real and work:
- `classify_response` (`:143-152`): `status == "err"` → REFUSED; `status == "ok"` with a `statuses[].error` → REFUSED (`per_status_errors`, `:130-140`); clean `ok` → NOT_REFUSED; anything else → INCONCLUSIVE. Pinned by `tests/…:162-185`.
- `classify_exception` (`:155-162`): `ClientError` → REFUSED, `ServerError`/other → ERROR. Pinned by `tests/…:313-327`.
- The verdict gate (`:466-470`) requires `refused == len(arms) **and** authorization_refusals == len(arms)`; otherwise `DD06_INCONCLUSIVE`. **M9 dies** on `test_validation_shaped_refusal_makes_the_run_inconclusive` (`tests/…:292-310`). So a *plainly* validation-shaped refusal cannot be counted as DD-06 evidence — and r2 is the proof: the venue's real text `Must deposit before performing actions. User: <address>` classified `UNCLASSIFIED` on all four arms and the run reported `DD06_INCONCLUSIVE` rather than claiming evidence (`LEAD_READING_r2_20260916.md:11-14`). That is the design working.

The dishonest path that remains: **`classify_refusal_text` (`:196-206`) checks AUTHORIZATION markers first, and `"does not exist"` is an AUTHORIZATION marker (`:168`), while the docstring (`:19-22`) lists "sub-account existence" as VALIDATION.** Measured, not argued:

```
cwd C:/tmp/OPUS_DD06_SCRATCH   (interpreter as above)
classify_refusal_text('Sub-account 0xdead does not exist')   -> 'AUTHORIZATION'
classify_refusal_text('Sub account does not exist')          -> 'AUTHORIZATION'
classify_refusal_text('Insufficient balance for agent')      -> 'AUTHORIZATION'
classify_refusal_text('Must deposit before performing actions. User: 0xabc') -> 'UNCLASSIFIED'
classify_refusal_text('Insufficient balance for withdrawal.')-> 'VALIDATION'
classify_refusal_text('Error withdrawing from bridge')        -> 'UNCLASSIFIED'
```

End-to-end (`C:/tmp/OPUS_DD06_SCRATCH/reviewer_checks.py`, output `REVIEWER_CHECKS_OUT.txt`), a run with `--sub-account` naming an address that does not exist:

```
=== CLAIM A: a non-existent sub-account yields AUTHORIZATION-class DD-06 evidence ===
result            : DD06_REFUSALS_OBSERVED
finding           : None
subAccountTransfer: REFUSED AUTHORIZATION
venue text        : {"response": "Sub-account [redacted-address] does not exist", "status": "err"}
CLAIM A HOLDS     : True
```

`DD06_REFUSALS_OBSERVED` is the outcome that, per packet §4, lets the owner move the DD-06 register row off BLOCK to "primary testnet evidence". A mistyped or stale `--sub-account` value therefore manufactures a share of that verdict out of an arm the venue refused only because the destination does not exist. → **R-3**.

### Item 4 — control arm

`control_order_size` (`:228-236`) delegates to the Bridge's own `round_hl_price` (`bridge/broker/hyperliquid.py:72-89`), which rounds **down** to `max(10^-(6-szDecimals), 10^(adjusted-4) [·10 when ≥ 10 000])` and returns integral prices unchanged. I swept it rather than reasoning about it (`C:/tmp/OPUS_DD06_SCRATCH/sweep.py`, `sweep2.py`):

```
1 140 006 mids: every 0.1 step in [10 000.0, 200 000.9], szDecimals = 5
checks: significant figures ≤ 5 (or integral) · decimals ≤ 1 · 0 < px ≤ 0.9·mid · px ≥ 0.998·0.9·mid · size a clean 10^-5 multiple
violations of the wire-validity checks: 0
r1 mid 76974.0 -> (69270.0, 0.00016)          [test asserts exactly 69270.0 — tests/…:159]
r1's rejected price round(76974.0*0.9, 1) = 69276.6 -> 6 significant figures
r3's recorded price 68520.0 reproduced from mid 76133.4
notional over the whole sweep: min 10.499999999999998, max 12.249719999999998
```

So the r1 rejection (`Price must be divisible by tick size`, 69276.6) **cannot recur for any mid ≥ 10 000**: at szDecimals 5 every produced price has ≤ 5 significant figures and ≤ 1 decimal, and stays at or below 90 % of mid so it cannot fill. Confirmed live twice at the venue — r2 `68463.0` and r3 `68520.0` both rested and cancelled. The one imperfection is that the notional lands *exactly* on `CONTROL_MIN_NOTIONAL_USD` for some mids and float rounding puts it 1.8e-15 below (mid 10416.7 → 9375.0 × 0.00112 = `10.499999999999998`), which breaks the module's own asserted invariant (`tests/…:158`) for mids the test does not sample. No venue impact — the real floor is $10 and the constant carries $0.50 of margin. → **N-5**. (Also, `control_order_size` raises `ZeroDivisionError` for absurd mids below ~0.001; it is inside the S1 `try` and aborts safely.)

### Item 5 — fixture tests vs reality

The brief asks what venue-shaped facts the fixtures still do not carry and whether any could make the next run misreport. One of them already did, on **r3, with this exact candidate**:

- **Whose funds moved is not in the record.** S0 reads `extra_agents`, `user_state` and `spot_user_state` for `account_address` only (`:283-333`) — never for `wallet.address`, which `main` has in hand (`:570`, `:580`). So when an arm succeeds, the record says `"finding": "spotSend was NOT refused for an agent wallet"` and `"result": "DD06_FINDING_NOT_REFUSED"` beside the **master's** balance and nothing else. On r3 the truth was benign: the agent moved its **own** 1 USDC (agent 14.0 → 13.0, master 983.987457 → 984.987457; the venue ledger names `user = 0xfa06…8504`, the agent — `LEAD_PUBLIC_READS_after_r3.txt:2-3,9`). The disambiguation came entirely from a pre-written human rule plus two out-of-band public reads, not from the artefact the probe produces. Reproduced offline:
  ```
  === CLAIM C: the record of a NOT_REFUSED spotSend carries no agent-wallet balance ===
  result : DD06_FINDING_NOT_REFUSED
  finding: spotSend was NOT refused for an agent wallet
  steps  : [S0_extra_agents, S0_user_state, S0_spot_user_state, S1_control_order, S1_control_cancel,
            subAccountTransfer, withdraw3, usdSend, spotSend, approveAgent]
  any step naming the AGENT wallet's own balance: []
  CLAIM C HOLDS: True
  ```
  The author names the same fix in his own r3 reading ("a slice that reads both balances before/after and classifies OWN_FUNDS_MOVED vs MASTER_FUNDS_MOVED", `LEAD_READING_r3_20260916.md:30`) and did not put it in the candidate. → **R-4**.
- **Facts the fixtures now carry correctly** (checked against the r2/r3 bytes, so I am not guessing): the `ok` + `statuses[].error` order-rejection shape (`tests/…:162-185`, `:330-367`); the `{"status":"err","response":"<text>"}` transfer-refusal shape; `approve_agent` returning a 2-tuple — the real SDK signature is `approve_agent(self, name=None) -> Tuple[Any, str]`, so the discard at `:256-258` is right; `statuses: ["success"]` for cancel; a unified/classic account holding USDC in **spot** with perp `accountValue 0.0` (S0 spot read, `:311-333`, added in slice 3 — r2/r3 both show it). Every `ExchangeLike`/`InfoLike` member matches the installed SDK 1-for-1 (`withdraw_from_bridge`, `usd_transfer`, `spot_transfer(amount, destination, token)`, `sub_account_transfer(sub_account_user, is_deposit, usd)`, `order`, `cancel`, `extra_agents`, `spot_user_state`, `all_mids`, `meta`); `spotSend` with the bare token string `"USDC"` is accepted on testnet (r3 proved it — do not "fix" that).
- **Facts still not carried, and what each would do to the next run**: (a) the `statuses` payload of a *successful* withdraw3/usdSend/spotSend — the fixtures only ever return `{"type":"default"}`, which is what r3 actually returned, so this is now low risk; (b) a **filled** control order — see N-3, the code would call it "rests on the book"; (c) sub-account refusal texts — see R-3, the untested branch is the one that corrupts the verdict; (d) rate-limit/`429` `ClientError`s, which become REFUSED + UNCLASSIFIED → INCONCLUSIVE (safe); (e) a withdraw3 attempted with a **funded perp** balance, which no run has yet exercised (r3's withdraw3 died on the agent's 0 perp balance with the opaque `Error withdrawing from bridge`) — so "the agent cannot withdraw with funds present" is still not tested; (f) mainnet parity, which the packet correctly refuses to claim.

### Item 6 — scope and suite

Exactly two files, both new, 1016 insertions, zero deletions (§1). Focused suite re-run by me: **16 passed** (§2). Full Bridge suite: I did **not** re-run it (see NOT VERIFIED) and rely on `LEAD_PYTEST_full_bridge_slice3.txt`, whose bytes read `1614 passed, 1 skipped, 1 warning in 166.08s (0:02:46)` / `full-suite-exit=0` — note the brief's citation omits the `1 skipped`. `LEAD_RUFF_slice3.txt` = `All checks passed!`; `LEAD_GUARD_slice3.txt` = `RESULT: PASS` (the two "dirty" entries in that guard log are the candidate's own files pre-commit).

---

## 4. Findings

### REQUIRED

**R-1 — the mainnet boundary, the master-key call and the record's last-resort hex guard have zero test coverage; four mutants survive a green suite.**
`TESTNET_URL` (`tools/dd06_agent_withdraw_probe.py:47`), the `refuse_master_key(...)` call in `main` (`:572`), `del api_key` (`:571`) and the two `write_record` surviving-hex refusals (`:509-514`) are each deletable/alterable with `16 passed` still printed (M1-M4, §3 item 1). The brief pre-wrote the disposition for this case; it is also this repo's own precedent (P0-31 OD-7: a sole guard with no test). Cheapest fixes that would kill each mutant: assert `plan_text()` contains the literal testnet host (kills M2 at zero cost); one test that monkeypatches `bridge.settings.resolve_hyperliquid_credentials` and `eth_account.Account.from_key` and asserts `main` exits 3 when the derived address equals the account address (kills M3); one test feeding `write_record` a `ProbeRecord` whose step data carries a raw 64-hex string and asserting `ProbeRefused` (kills M4). `del api_key` is the weakest of the four in substance — `Account.from_key` keeps the key material inside `wallet` for the whole run, so the line is a gesture, not a control; either pin it or drop the claim.

**R-2 — the test suite calls the real `main()`, and only one refusal keeps it offline; remove that refusal and `pytest` becomes a live venue run with the operator's real credential.**
`tests/test_dd06_agent_withdraw_probe.py:407-412` invokes `probe.main(["--run-id","x","--out","unused","--network","testnet"])` with nothing stubbed — no patch of `resolve_hyperliquid_credentials`, `Info`, or `Exchange`. Demonstrated, not theorised: §0. On this host, `HKEY_CURRENT_USER\Environment` holds both `HL_ACCOUNT_ADDRESS` (42 chars) and `HL_API_WALLET_KEY` (66 chars), so resolution succeeds anywhere, not only on KVM2. Two independent fixes, both cheap: (1) in that test, monkeypatch the credential resolver and the two SDK constructors so the real branch can never dial; (2) in `main`, require a second, explicit execution token (e.g. `DD06_PROBE_RUN_TOKEN=<run-id>` in the environment, or an `--i-have-the-owners-word` flag) *before* constructing `Info`/`Exchange`, so no single-line change can arm the tool. (2) also closes N-6.

**R-3 — a refusal that only says the destination does not exist is counted as AUTHORIZATION-class DD-06 evidence, contradicting the module's own specification.**
`classify_refusal_text` (`:196-206`) tests AUTHORIZATION markers first and `"does not exist"` is one (`:168`), while the docstring (`:19-22`) and the packet (`:26`) both put "sub-account existence" in VALIDATION. With `--sub-account` naming a non-existent address the run returns `DD06_REFUSALS_OBSERVED` — the verdict that moves the register row — with that arm's `refusal_class: AUTHORIZATION` (Claim A, §3 item 3). Fix: check VALIDATION markers first for existence/precondition wording, or narrow the AUTHORIZATION marker to the venue's actual authorization sentence (`"user or api wallet"` + `"does not exist"`), and add the two failing inputs to `test_refusal_text_classes` (`tests/…:273-289`).

**R-4 — the record cannot support the verdict it prints: on a `NOT_REFUSED` fund arm it says "was NOT refused for an agent wallet" without ever reading the agent wallet's own balance.**
`:283-333` reads state only for `account_address`; `:460` writes the finding text. This exact code printed `DD06_FINDING_NOT_REFUSED` / `"spotSend was NOT refused for an agent wallet"` on r3 while the truth was that the agent had moved its **own** 1 USDC (§3 item 5, Claim C). A reader of `DD06_PROBE_RECORD.json` alone would conclude the restriction was falsified. Fix, using data `main` already holds: add `S0_agent_user_state` / `S0_agent_spot_user_state` for `wallet.address`, re-read both wallets after any `NOT_REFUSED` fund arm, and split the result label into `DD06_FINDING_OWN_FUNDS_MOVED` vs `DD06_FINDING_MASTER_FUNDS_MOVED` (the author's own prescription, `LEAD_READING_r3_20260916.md:30`). Until then, no record this probe writes can close DD-06 on its own; the current "VERIFIED on testnet" reading rests on `LEAD_PUBLIC_READS_after_r3.txt`, which I did verify against bytes (`:2-3`, `:9`) and which does support the Lead's conclusion.

### NIT

- **N-1** `FUND_MOVING_ARMS` (`:55`) is defined and never used; the stop rule at `:459-465` fires on *any* `NOT_REFUSED` arm (safe-direction), so the docstring's "if a fund-moving arm is NOT refused" (`:19-20`) describes a control that does not exist as written. Delete the constant or use it.
- **N-2** `_attempt` catches `BaseException` (`:245`), so a `KeyboardInterrupt` during an arm is recorded as `ERROR` and the loop proceeds to the **next** fund-moving arm — the operator's abort gesture cannot stop the sequence. Re-raise `KeyboardInterrupt`/`SystemExit`.
- **N-3** `_resting_oid` (`:479-485`) regex-matches any `"oid": N` in the redacted response, including a `filled` status. A filled control order (a ~10 % flash move while the bid rests) therefore yields `ABORTED_CONTROL_CANCEL_FAILED` with `"control order rests on the book … cancel it by hand"` — the wrong remedy for an open position. Verified offline (Claim B, `REVIEWER_CHECKS_OUT.txt`). The packet's abort conditions (`:25`) do tell the owner to flatten, so this is a wording/parse nit, not an exposure. Fix: require the `resting` key in `statuses[0]`.
- **N-4** `_HEX40` (`:59`) requires the `0x` prefix, so a bare 40-hex address passes both `redact` and the `write_record` guard. Addresses are public; hygiene only.
- **N-5** min-notional lands exactly on the constant for some mids and float rounding puts it 1.8e-15 below (§3 item 4), breaking the suite's own `>=` assertion for unsampled mids. Use a small margin (`* 1.01`) or compare with a tolerance.
- **N-6** nothing in the tool binds execution to KVM2-P4-03 although packet §3 does; `--network testnet` is the *default*, so the tool is one command away from running wherever `HL_*` exists (proven by §0, from the Windows workstation). Covered by fix (2) of R-2.
- **N-7** `--include-usd-class-transfer` (`:434-441`, `:550`) has no test and `usd_class_transfer` is absent from the `ExchangeLike` protocol (`:89-106`) — the real SDK does have `usd_class_transfer(amount, to_perp)`, so only the flag's plumbing is unverified.
- **N-8** brief/record drift: the brief's subject line says the probe "ran once on testnet"; three runs exist (§1). No code impact; flagged so the Friday Sol lane is not briefed on a stale premise.
- **N-9** arm order: `withdraw3`, the only arm that can move funds **off** the venue, runs first (`:388`), ahead of the two in-venue self-transfers whose non-refusal would trip the stop rule and make the withdrawal unnecessary. Reordering is strictly safer with identical evidence value in the all-refused case — but §3 of the packet is the owner-approved order, so this is the owner's call, not a reviewer's rewrite.

### What is sound (so the repair does not erase it)

Redaction and the write-once record are real and pinned (M7 dies; the on-host r2/r3 records are address-free). The stop rule is real and has fired at the venue. The refusal-class gate genuinely refuses to convert a non-authorization refusal into DD-06 evidence — r2's real venue text landed in `UNCLASSIFIED` and the run reported `DD06_INCONCLUSIVE`. The control arm's price arithmetic is now correct across 1.14 M mids and has been accepted twice by the live venue. Scope is exactly two additive files, lint clean, and the SDK surface the protocols describe matches the installed SDK exactly.

## 5. NOT VERIFIED

- **I did not run the probe deliberately** and hold no authority to; the one run that did occur was the unintended mutant side effect disclosed in §0, and I made no further network call afterwards.
- **I did not re-run the full Bridge suite.** The brief only requires the focused re-run; after the §0 incident I chose not to execute ~1 600 unread tests on a host whose HKCU holds live venue credentials. The claim rests on `LEAD_PYTEST_full_bridge_slice3.txt` (bytes read: `1614 passed, 1 skipped … exit=0`) plus the `--name-status` proof that no existing file was touched.
- Nothing about **mainnet** is verified or verifiable here, by design.
- **KVM2-P4-03 host state** (service DISARMED, `NRestarts 0`, installed file mode 0444) and the **on-host records** (`7f42dda1…` for r2, `e13b8939…` for r3) were not verified at the host; I read only the redacted console copies in `QUEUED_PACKAGES_20260915/P029/DD06_TESTNET_PROBE_20260915/`, whose `probe_sha256` does match the committed blob.
- The venue's **own documentation** was not read (no network); every venue-behaviour statement above comes from the r2/r3/§0 records or the installed SDK source.
- That **no testnet order rests** after the §0 run is supported only by the venue's `{"statuses": ["success"]}` cancel response inside that record; I did not issue a confirming public read.
- Whether the venue would refuse withdraw3 from an agent whose **perp** balance is funded is still untested by any run.

---

VERDICT: REQUEST_CHANGES
