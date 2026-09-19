# T0 exact-Opus read #2 (repair round 1 of 3) — WP-P0-29 DD-06 testnet falsification probe, candidate `a46b2a9d`

Reviewer: exact `claude-opus-5`, effort xhigh, launched from `C:/tmp/OPUS_QUEUE_20260916/DD06/opus/BRIEF.md`.
No delegation, no sub-agents, no resumed session. One report file; scratch under `C:/tmp/OPUS_DD06_SCRATCH/` only.
Read performed 2026-09-17, ~21:2x–22:1x UTC+3. Lead is the disclosed author of the candidate and is not a reviewer here.

**Safety rule observed.** No network call of any kind was made. The worktree files were never modified.
Every mutant lived in a scratch copy; only the fixture suite was ever run against a mutant; `main()` was
never invoked outside pytest, never with a venue URL, never with `HL_*` or `DD06_PROBE_RUN_TOKEN` set.

---

## 0. Verified identities

| Item | Value |
|---|---|
| COMPUTED HEAD (`git -c safe.directory=* -C C:/tmp/P029_DD06_20260915 rev-parse HEAD`) | `a46b2a9db861433e1128dba21fc18362867b5d7f` ✅ matches the candidate |
| `tools/dd06_agent_withdraw_probe.py` sha256 (working tree, CRLF) | `47C70E6882E674E2D22D2B2FC8337731402C691387C5651432D827DB6A6DF84B` (31 256 B) |
| `tests/test_dd06_agent_withdraw_probe.py` sha256 (working tree, CRLF) | `C3A0DA6104403A536056008E9BE019B7A8BEBF65FCEEB00ED9702842C670AF33` (22 846 B) |
| tool — git blob OID at HEAD | `2c8d071810d2dcc3219e89d67b325783991e5bb7` |
| test — git blob OID at HEAD | `0982253bfdb7c66a72cdf9fa902a7b15834a1e7e` |
| Working tree == HEAD? | **Yes.** The checkout is CRLF (745 CRLF / 745 LF in the tool); LF-normalising the working bytes reproduces both HEAD blob OIDs exactly. Verified without `git status` or any diff-with-working-tree. |
| Scope vs base (`git diff --name-status fcac0ac6 a46b2a9d`) | `A IBKR_PAPER_BRIDGE/tests/test_dd06_agent_withdraw_probe.py`, `A IBKR_PAPER_BRIDGE/tools/dd06_agent_withdraw_probe.py` — **exactly two files, both ADDED, nothing modified** ✅ |
| Repair slice (`git diff --stat 1af85067 a46b2a9d`) | `2 files changed, 349 insertions(+), 13 deletions(-)` ✅ matches the addendum's `+349/−13, two files` |

Git commands used: `rev-parse HEAD`, `rev-parse HEAD:<path>`, `diff --name-status <sha> <sha>`,
`diff --stat <sha> <sha>`, `show HEAD:<path>` (byte comparison, stated as required). No status, no
diff-with-working-tree, no add/commit/checkout/push, in any repository.

### Pin discrepancy in my own launch brief — recorded, not fatal
`opus/BRIEF.md:3` says *"If … HEAD is not `1af85067234632ff057b4212e7599f8003a85ee6`, your verdict must be
BLOCK."* That sentence contradicts **its own title line** (`BRIEF.md:1`: *"RE-PINNED 2026-09-17 21:5x to
`a46b2a9d` (T0 repair round 1)"*), the `REVIEW_BRIEF.md:1` title, and the whole 2026-09-17 addendum, all of
which name `a46b2a9d`. Observed HEAD is `a46b2a9d`, the repair candidate. I read the stale sha as an
un-updated sentence, not as the pin, and reviewed `a46b2a9d`. Filed as **N-12** so the Friday Sol lane is not
handed a brief whose literal reading forces BLOCK on the correct subject.

### Baseline suite (re-run by me, as the brief requires)

```
cwd: C:\tmp\P029_DD06_20260915
C:/tmp/P012_FUNDING_PY312_20260911/Scripts/python.exe -m pytest IBKR_PAPER_BRIDGE/tests/test_dd06_agent_withdraw_probe.py -q -p no:cacheprovider --basetemp C:/bt_opus_dd06
.........................                                                [100%]
25 passed in 0.56s
```
✅ 25 passed, matching `REPAIR_R1_20260917/LEAD_PYTEST_GREEN_R1.txt` (`25 passed in 0.61s`, exit 0).

---

## 1. No mainnet path, no key leak

**First, the fact that decides how much the fences matter.** `bridge/settings.py :: resolve_hyperliquid_credentials`
resolves the process environment *and then falls back to* `HKEY_CURRENT_USER\Environment`. On this
workstation that fallback is live — presence check, values never printed:

```
HL_ACCOUNT_ADDRESS: PRESENT (len=42)
HL_API_WALLET_KEY:  PRESENT (len=66)
HL_LIVE_ACK:        absent
DD06_PROBE_RUN_TOKEN: absent
```

So `monkeypatch.delenv("HL_API_WALLET_KEY")` does **not** make a test offline — the resolver would still
return a valid agent key from the registry. Only the `offline` fixture's tripwire on the resolver
(`tests:445-446`) does. The Lead's fixture design is therefore correct and load-bearing, and the
2026-09-17 incident shape is genuinely closed. My M-A and M-F mutants below prove both halves of that.

| Control | Code | Test that pins it | My mutant | Result |
|---|---|---|---|---|
| `TESTNET_URL` hard-coded, the only host the tool can dial | `tools:56`, used at `tools:728-729`, printed in the plan `tools:661` | `tests:511-516` | **M-E** `TESTNET_URL` → `https://api.hyperliquid.xyz` | ✅ killed — `test_plan_names_the_testnet_host_and_the_gates` fails |
| `refuse_unless_testnet` (mainnet refused) | `tools:235-239`, called `tools:701` | `tests:124-131`, `tests:459-465` | covered by M-B below | ✅ |
| `HL_LIVE_ACK` refusal | `tools:240-243` | `tests:127-131` | **M-B** block deleted | ✅ killed — `test_refuses_mainnet_and_live_ack` → `Failed: DID NOT RAISE ProbeRefused`. **No test reached the resolver** (see §7b for which line stopped it) |
| Second gate: `DD06_PROBE_RUN_TOKEN == --run-id` | `tools:246-255`, called `tools:702` | `tests:467-477` (via `main`), `tests:480-489` (unit) | **M-A** call at `:702` deleted | ✅ killed — and it fails on the **resolver tripwire**, not a network error (§7a) |
| Master-key refusal | `tools:258-263`, called `tools:712` | `tests:134-137`, `tests:492-508` | **M-F** call at `:712` deleted | ✅ killed — fails on the **`Info` tripwire**, i.e. without that line `main` would have built an SDK object |
| `del api_key` | `tools:711` | *(none)* | **M-H** line deleted | ❌ **survives — 25 passed, no test fails** |
| Redaction of 64-hex before any record | `tools:74`, `tools:92` | `tests:222-224` | **M-P** `_HEX64.sub` removed | ✅ killed |
| `write_record` refuses a surviving hex | `tools:644-649` | `tests:519-530` | **M-G** both guards deleted | ✅ killed |

**`del api_key` (M-H): confirmed to be a gesture, not a control.** Deleting `tools:711` leaves the suite
fully green. It also cannot do what a reader might assume: `Account.from_key(api_key)` at `tools:710`
has already copied the key material into the wallet object, and `resolve_hyperliquid_credentials`'s
return tuple is gone in any case. The Lead disclosed this and kept the line "without a claim", and the
docstring/plan make no claim about it — so this is **not** a finding. It is recorded here because the
brief asked for the mutant, and the honest answer is "no test pins it, and no test should".

**Verdict on item 1:** no mainnet path. Two independent gates sit ahead of every credential read and every
SDK construction (`tools:701` then `tools:702`, both before `tools:709`), and each is separately fenced by a
test that dies on a tripwire rather than on the network. No key leak: the key is never printed, never
recorded, and two independent redaction layers plus a refuse-to-write guard stand between the record and
any 64-hex string.

---

## 2. Funds cannot leave silently

| Claim | Where | Status |
|---|---|---|
| `STOP_ON_NOT_REFUSED` stops the sequence after a NOT_REFUSED arm | `tools:72`, `tools:597-600` | ✅ fenced — **M-I** (`= False`) kills 4 tests |
| withdraw3 amount = 6 USDC, above the documented 5 USDC minimum + 1 USDC fee | `tools:62`, arm at `tools:481-487` | ✅ fenced — **M-J** (`= 0.5`) kills 3 tests via `tests:95` |
| withdraw3 destination = the account's own master address | `tools:484-486` | ✅ fenced — **M-O** (destination → a foreign address) kills 3 tests via `tests:99` |
| The packet says plainly that a non-refused withdraw3 takes test-USDC **off the venue** | `DD06_TESTNET_PROBE_STEP_PACKET_20260915.md` L22 and L26 | ✅ verified against bytes: *"A NOT-refused `withdraw3` means 6 test-USDC **leave the venue** to the owner's own address on the bridge chain — stated plainly, not hidden behind 'own address'."* |
| A NOT_REFUSED **fund-moving** arm re-reads both wallets before concluding | `tools:555-596` | ⚠️ present, but the conclusion it draws is wrong — **R-1** |
| An **ERROR'd** fund-moving arm is measured and stops the sequence | `tools:545-600` | ❌ **it is neither — R-2** |

**R-2 (REQUIRED), demonstrated offline.** `run_probe`'s arm loop branches only on `REFUSED` (`tools:548-551`)
and `NOT_REFUSED` (`tools:552-600`). An `ERROR` — which `classify_exception` (`tools:178-185`) returns for a
timeout, a 5xx, or any non-`ClientError` exception, i.e. precisely the cases where a signed request may
already have reached the venue — falls through both branches and the loop continues to the next fund-moving
arm, with no balance re-read at all. The shipped suite pins today's behaviour at `tests:329-343` but only
asserts the outcome label, not the exposure. My demonstration (`test_DEMO_A`, §7e) has withdraw3 execute at
the venue and *then* time out:

```
result  : DD06_INCONCLUSIVE
finding : None
calls   : ['order', 'cancel:60109082440', 'withdraw3', 'usdSend', 'spotSend', 'approveAgent']
  withdraw3   ERROR        <- 6 USDC left the venue here
  usdSend     REFUSED      <- the probe kept firing fund-moving arms anyway
  spotSend    REFUSED
  approveAgent REFUSED
'994.0'  in record: False   <- the post-withdrawal truth is never read
'1000.0' in record: True    <- only the stale S0 reading survives
```

So the written record of a run in which 6 test-USDC left the venue is `"result": "DD06_INCONCLUSIVE"`,
`"finding": null`, and a pre-arm balance that is silently stale. That is the literal failure mode item 2
is meant to exclude. Remedy is small and symmetric with the R-4 repair: treat `ERROR` on a name in
`FUND_MOVING_ARMS` the way `NOT_REFUSED` is treated — re-read both wallets, record before/after, and stop.

---

## 3. Classification honesty

| Path | Code | Behaviour |
|---|---|---|
| err envelope | `tools:170-171` | `REFUSED` |
| ok envelope with `statuses[].error` (the r1 tick rejection) | `tools:153-163`, `tools:172-174` | `REFUSED` — fenced; **M-K** (ignore per-status errors) kills 2 tests |
| clean ok envelope | `tools:174` | `NOT_REFUSED` |
| anything else | `tools:175` | `INCONCLUSIVE` |
| exceptions | `tools:178-185` | `ClientError` → `REFUSED`; everything else → `ERROR` |

**Can a VALIDATION refusal be counted as DD-06 evidence? No.** The path is explicit: `_attempt` stamps
`data["refusal_class"]` from `classify_refusal_text` (`tools:292-293`, `tools:302-308`); the loop only
increments `authorization_refusals` when that class is exactly `AUTHORIZATION` (`tools:549-550`); and the
success label `DD06_REFUSALS_OBSERVED` requires `refused == len(arms) **and** authorization_refusals ==
len(arms)` (`tools:602-603`). Any VALIDATION or UNCLASSIFIED refusal therefore drops the run to
`DD06_INCONCLUSIVE` (`tools:605`) with a finding telling the reader to go read the venue texts
(`tools:606-610`). Pinned at `tests:308-326`. This is the correct, conservative shape.

**R-3 of the first read is properly repaired.** `"does not exist"` now sits in `VALIDATION_MARKERS`
(`tools:214`) while the venue's signer sentence `"user or api wallet"` sits in `AUTHORIZATION_MARKERS`
(`tools:190`), and authorization wins when both appear (`tools:228-231`). Two failing inputs are pinned at
`tests:295-302`. **M-D** (move `"does not exist"` back into `AUTHORIZATION_MARKERS`) kills
`test_refusal_text_classes`. ✅

One honest caveat, not a finding: `AUTHORIZATION_MARKERS` contains the bare substring `"agent"`
(`tools:195`), so any venue text containing the word — including, say, an `approveAgent` amount complaint —
classifies as AUTHORIZATION. The direction of that error is *toward* claiming DD-06 evidence. It is
mitigated because the Lead re-reads every recorded text by hand (packet L26) and because r3 shows the venue's
real texts are short and unambiguous. Worth knowing; not worth a repair round.

---

## 4. Control arm

`control_order_size` (`tools:266-274`) routes the price through the Bridge's own `round_hl_price`
(`bridge/broker/hyperliquid.py`), which rounds **down** to `max(10^-(6-szDecimals), 10^(adjusted-4))`, with an
extra guard digit for values ≥ 10 000.

I did not take the suite's five sampled mids on trust. I swept **285 723** mids from 10 000 to 210 000 at
szDecimals 5 (`C:/tmp/OPUS_DD06_SCRATCH/price_sweep.py`):

```
r1 pin 76974.0 -> (69270.0, 0.00016)          <- matches tests:159 exactly
mids checked                        : 285723
price above 90% of mid (could fill) : 0
decimals > 6-szDecimals             : 0
>5 sig figs AND NOT an integer      : 0
>5 sig figs but integer (HL-legal)  : 1273   e.g. mid 111150.0 -> 100035.0
```

**The r1 rejection (`Price must be divisible by tick size`, 69276.6) cannot recur for any mid ≥ 10 000.**
Every produced price is at or below 90 % of mid (so it cannot fill), carries at most `6 - szDecimals`
decimals, and carries at most 5 significant figures unless it is an integer — and integer prices are
accepted regardless of significant figures. **M-L** (restore the r1 `round(mid*0.9, 1)`) kills
`test_control_price_is_wire_valid_for_a_real_btc_mid`. ✅

Two measured caveats, both NITs:
- 1 273 of the 285 723 mids (0.45 %) yield a >5-significant-figure **integer** price. That is wire-valid only
  under the venue's integer exemption — the same exemption `round_hl_price`'s own comment says it does not
  want to rely on for values ≥ 10 000. The suite's `len(digits) <= 5` assertion (`tests:154`) is therefore not
  a property of the code; it passes only because five mids are sampled. → **N-10**.
- N-5 re-measured: the worst **exact** notional across the sweep is exactly `$10.50` (mid 11 111.6 →
  10 000.0 × 0.00105); the float product dips to `10.499999999999998` for some mids, which breaks the suite's
  own `>=` assertion (`tests:158`) for unsampled mids. No venue impact — the real floor is $10 and the
  constant carries $0.50 of margin. → **N-5**, unchanged.

---

## 5. Fixture tests vs reality — and yes, one of these makes the next run misreport

This is the item that decides the verdict, because the answer is no longer hypothetical: **r2 and r3 have
already run on testnet**, and r3 took the NOT_REFUSED branch that this repair was written for.

From `LEAD_READING_r3_20260916.md` and `LEAD_PUBLIC_READS_after_r3.txt` (2026-09-16 09:01:19Z), verified
against bytes:

- agent `0xfa06…8504` spot USDC **14.0 → 13.0**, perp 0.0 — the agent paid
- master `0x1E26…AC49` spot USDC **983.987457 → 984.987457**, perp 0.0 — **the master received**
- venue ledger: `spotTransfer` `user = agent`, `destination = master`, 1.0 USDC
- arm outcomes: withdraw3 REFUSED/UNCLASSIFIED, usdSend REFUSED/VALIDATION, **spotSend NOT_REFUSED**

### R-1 (REQUIRED) — replaying the venue's own r3 readings through the repaired attribution prints the opposite of the truth

`_moved` (`tools:341-351`) answers *"did any readable balance change?"* — not *"did funds leave?"* — and
`run_probe` consults `master_moved` first (`tools:578`) and `own_moved` only in the `elif` (`tools:584`). A
self-transfer from the agent to the master **increases** the master's balance, so `master_moved` is `True`
and the master branch wins. Demonstrated with r3's exact numbers
(`C:/tmp/OPUS_DD06_SCRATCH/mutroot/tests/test_reviewer_r3_replay.py`, **passes** against the unmodified
candidate):

```
record.result  == "DD06_FINDING_MASTER_FUNDS_MOVED"
record.finding contains "moved the master's funds (DD-06 falsified on testnet)"
record.finding does NOT contain "AGENT wallet's own balance changed"
(while the recorded readings are correct: master 983.987457 -> 984.987457, agent 14.0 -> 13.0)
```

So on the run the venue has *already produced once*, the repaired tool writes the package's maximum-severity
sentence — **"the agent key moved the master's funds (DD-06 falsified on testnet)"** — for an event in which
the agent spent its own dollar and the master got richer. R-4 asked the Lead to stop asserting a breach it
never measured; the readings are now taken, but the inference drawn from them still is not measured. The
`elif` ordering means the wrong branch wins in exactly the observed case.

**R-1(b), same root, separate trigger.** When the master's balances are unreadable, `_moved` returns `None`
(`tools:349-350`), `None` is falsy at `tools:578`, and a readable agent change sends the run to the OWN
branch, which prints *"the master's are unchanged"* (`tools:588-589`) — a statement nothing measured.
Demonstrated by `test_DEMO_B` (§7f): every master reading in that record is `None` while the finding claims
the master is unchanged.

**Remedy (minimal, deterministic, testable).** Make the attribution directional and amount-aware, using
readings the record already carries: `master_moved` should mean *the master's readable balance decreased*;
`own_moved` should mean *the agent's decreased*; the sentence "DD-06 falsified on testnet" should require a
master **decrease** consistent with the arm's amount; and an unreadable side must produce
"unreadable", never "unchanged". Three failing inputs are already written and can be lifted from
`test_reviewer_r3_replay.py` and `test_DEMO_B`/`test_DEMO_C`.

### Other venue-shaped facts the fixtures still do not carry

| Fact | Could it make the next run misreport? |
|---|---|
| **`--include-usd-class-transfer`**: zero tests; `usd_class_transfer` is still absent from the `ExchangeLike` protocol (`tools:105-122`) although `usdClassTransfer` is now declared fund-moving (`tools:69`) and the `# type: ignore` sits on `tools:534` rather than on the attribute access at `tools:532` | Only if the owner passes the flag — but then an entirely unexercised arm meets the venue, which is the r1 failure shape. → **N-7**, re-raised |
| A **filled** control order: `_resting_oid` (`tools:614-620`) regex-matches any `"oid": N`, including a `filled` status | Yields `ABORTED_CONTROL_CANCEL_FAILED` with *"rests on the book … cancel it by hand"* — the wrong remedy for an open position. → **N-3**, re-raised |
| withdraw3 with a **funded perp** balance | Still never exercised; r3's withdraw3 died on the agent's 0 perp balance with the opaque `Error withdrawing from bridge` (UNCLASSIFIED). "The agent cannot withdraw when funds are present" remains untested — the probe's central question is still open on its most important arm |
| `statuses` payloads for a *successful* withdraw3/usdSend | Low risk: r3 returned `{"type":"default"}`, exactly what the fixtures return |
| Rate-limit / 429 `ClientError` | REFUSED + UNCLASSIFIED → INCONCLUSIVE. Safe direction |
| Unified vs classic account balances | `_balances` (`tools:313-338`) reads perp `accountValue` + spot USDC and `_moved` treats **any** change as movement, so on an account with an open position a mark-to-market tick alone satisfies the master branch. Demonstrated by `test_DEMO_C` (§7g): a 0.01 `accountValue` drift with USDC untouched prints "DD-06 falsified on testnet". Same root as R-1 |
| Mainnet parity | Correctly not claimed anywhere |

---

## 6. Scope and suite

- **Exactly two files**, both added, nothing else touched — `git diff --name-status fcac0ac6 a46b2a9d` (§0). ✅
- **Focused suite re-run by me: 25 passed** (§0), matching the Lead's `LEAD_PYTEST_GREEN_R1.txt`. ✅
- **Full Bridge suite: NOT re-run by me** — see NOT VERIFIED. The Lead's evidence bytes
  (`REPAIR_R1_20260917/LEAD_FULL_BRIDGE_SUITE_R1.txt`) end `1623 passed, 1 skipped, 1 warning in 173.73s`,
  exit 0. The regression risk it covers is structurally near-zero anyway: the diff **adds** two files and
  modifies none, so the only way the candidate could disturb the existing suite is an import side effect at
  collection, and the tool's module level does nothing but import `bridge.broker.hyperliquid`.

---

## 7. My own mutants

Harness: an isolated scratch copy, `C:/tmp/OPUS_DD06_SCRATCH/mutroot/` (`bridge/` copied from the worktree,
`tools/dd06_agent_withdraw_probe.py` = the mutation target, `tests/` = verbatim copies of the shipped test
and `tests/conftest.py`). The worktree was never written to. Driver: `C:/tmp/OPUS_DD06_SCRATCH/mutate.py`.
Command for every run below, `cwd = C:\tmp\OPUS_DD06_SCRATCH\mutroot`:

```
C:/tmp/P012_FUNDING_PY312_20260911/Scripts/python.exe -m pytest tests/test_dd06_agent_withdraw_probe.py -q -p no:cacheprovider --basetemp C:/bt_opus_dd06_mut
```

Harness baseline `25 passed`; after the driver restored the pristine bytes, `25 passed` again.
`network sign` = a scan of each run's full output for `ConnectionError|Max retries|urllib3|Timeout|getaddrinfo`.

| Mutant | Fence removed | Outcome | Tripwire | Network sign |
|---|---|---|---|---|
| **M-A** | token gate call `tools:702` | 1 failed, 24 passed — `test_main_refuses_without_the_execution_token_before_reading_any_credential` | ✅ `resolve_hyperliquid_credentials` | none |
| **M-B** | `HL_LIVE_ACK` refusal `tools:240-243` | 1 failed, 24 passed — `test_refuses_mainnet_and_live_ack` | none reached | none |
| **M-C** | `_moved` → always `False` | 2 failed — exactly the `[agent-…]` and `[master-…]` attribution cases | none | none |
| **M-D** | `"does not exist"` → AUTHORIZATION | 1 failed — `test_refusal_text_classes` | none | none |
| **M-E** | `TESTNET_URL` → mainnet | 1 failed — `test_plan_names_the_testnet_host_and_the_gates` | none | none |
| **M-F** | `refuse_master_key` call `tools:712` | 1 failed — `test_main_refuses_a_master_key_after_the_gates_and_before_any_sdk_object` | ✅ `Info` | none |
| **M-G** | `write_record` hex guards `tools:644-649` | 1 failed — `test_write_record_refuses_surviving_hex` | none | none |
| **M-H** | `del api_key` `tools:711` | **0 failed — 25 passed** | none | none |
| **M-I** | `STOP_ON_NOT_REFUSED` → `False` | 4 failed | none | none |
| **M-J** | withdraw amount `6.0` → `0.5` | 3 failed | none | none |
| **M-K** | ignore `statuses[].error` | 2 failed | none | none |
| **M-L** | restore the r1 `round(mid*0.9, 1)` | 1 failed — `test_control_price_is_wire_valid_for_a_real_btc_mid` | none | none |
| **M-M** | `FUND_MOVING_ARMS` → `()` | 4 failed | none | none |
| **M-N** | dry-run early return `tools:697-699` | 1 failed — `test_dry_run_needs_no_credentials_and_no_network` (`assert 3 == 0`) | none | none |
| **M-O** | withdraw3 destination → foreign address | 3 failed | none | none |
| **M-P** | `_HEX64` redaction removed | 1 failed | none | none |

**15 of 16 killed; the single survivor is M-H, which the Lead disclosed in advance as a gesture rather than a control.**

### 7a. M-A — the addendum's required check (a)

```
>       assert probe.main(["--run-id", "x", "--out", "unused", "--network", "testnet"]) == 3
E       AssertionError: resolve_hyperliquid_credentials must never be reached from the fixture suite
tests\test_dd06_agent_withdraw_probe.py:431: AssertionError
1 failed, 24 passed in 0.74s
```
✅ The token test fails **on the resolver tripwire**, never on a network error. Given the live registry
credential documented in §1, this is the difference between a failing test and a live testnet dial.

### 7b. M-B — the addendum's required check (b), and which line stopped it

`test_refuses_mainnet_and_live_ack` fails with `Failed: DID NOT RAISE ProbeRefused`, and **no test reached
the resolver, the SDK constructors, or the network.** The line that stopped `main` is
**`tools/dd06_agent_withdraw_probe.py:702` — `refuse_without_run_token(args.run_id, dict(os.environ))`**.
Proof that it is that line and not something later: the two `main()` gate tests still passed, i.e. `main`
still returned 3; `DD06_PROBE_RUN_TOKEN` is cleared by the `offline` fixture (`tests:449-455`); and M-A shows
that deleting exactly `:702` is what lets execution reach the resolver tripwire. Defence in depth confirmed —
losing the `HL_LIVE_ACK` refusal no longer arms anything.

### 7c. M-C / 7d. M-D — the addendum's required checks (c) and (d)
`_moved` → always `False` fails exactly the two attribution cases
(`…[agent-DD06_FINDING_OWN_FUNDS_MOVED-…]` and `…[master-DD06_FINDING_MASTER_FUNDS_MOVED-…]`), and nothing
else. `"does not exist"` back in `AUTHORIZATION_MARKERS` fails `test_refusal_text_classes`. ✅ both.

### 7e–7g. Reviewer demonstrations (no mutation — these run against the **unmodified** candidate)

`C:/tmp/OPUS_DD06_SCRATCH/mutroot/tests/test_reviewer_demos.py` and `…/test_reviewer_r3_replay.py`, fake venue
objects only, `3 passed` and `1 passed`. They assert today's behaviour, so each finding below is
demonstrated rather than argued:

- **7e `test_DEMO_A`** → R-2: an errored fund arm that actually landed is never measured and the sequence
  keeps firing (output quoted in §2).
- **7f `test_DEMO_B`** → R-1(b): the OWN-funds finding prints "the master's are unchanged" while every master
  reading in the record is `None`.
- **7g `test_DEMO_C`** → R-1: an unrelated 0.01 `accountValue` drift, USDC untouched, prints
  "DD-06 falsified on testnet".
- **7h `test_reviewer_r3_replay`** → R-1: the venue's own r3 numbers produce
  `DD06_FINDING_MASTER_FUNDS_MOVED`.

---

## 8. Findings

### REQUIRED

**R-1 — the repaired attribution inverts the one real outcome the venue has already produced.**
`tools:341-351` (`_moved` tests "changed", not "decreased") and `tools:578-590` (`master_moved` consulted
before `own_moved`). Replaying r3's recorded readings — agent 14.0 → 13.0, master 983.987457 → 984.987457 —
yields `DD06_FINDING_MASTER_FUNDS_MOVED` and the sentence *"the agent key moved the master's funds (DD-06
falsified on testnet)"*, when the agent spent its own dollar and the master received it. Sub-case R-1(b):
with the master unreadable (`_moved → None`, falsy at `tools:578`) the OWN branch prints *"the master's are
unchanged"* (`tools:588-589`), which nothing measured. Demonstrated: §7f, §7g, §7h.
*Remedy:* make the test directional and amount-aware — master **decrease** consistent with the arm amount for
the MASTER label, agent decrease for the OWN label, and "unreadable" wherever a reading is `None`.

**R-2 — a fund-moving arm that ends in `ERROR` is neither measured nor stopped.**
`tools:545-600` branches only on `REFUSED` and `NOT_REFUSED`; `classify_exception` (`tools:178-185`) returns
`ERROR` for timeouts and 5xx — exactly the cases where a signed request may already have executed. The probe
records `ERROR`, re-reads no balances, and proceeds to the next fund-moving arm; the run is written as
`"result": "DD06_INCONCLUSIVE"`, `"finding": null` with a stale pre-arm balance. Demonstrated: §7e.
*Remedy:* on `ERROR` for a name in `FUND_MOVING_ARMS`, re-read both wallets, record before/after, and stop —
symmetric with the `NOT_REFUSED` path.

### NIT

- **N-3** *(re-raised)* `_resting_oid` (`tools:614-620`) matches any `"oid": N`, a `filled` status included, so
  a filled control order yields "rests on the book … cancel it by hand" — the wrong remedy for an open
  position. Require the `resting` key.
- **N-4** *(re-raised)* `_HEX40` (`tools:75`) requires the `0x` prefix, so a bare 40-hex address passes both
  `redact` and the `write_record` guard. `_HEX64` (`tools:74`) correctly makes the prefix optional. Addresses
  are public; hygiene only.
- **N-5** *(re-raised, now measured)* worst exact notional across 285 723 mids is exactly `$10.50`; the float
  product dips 1.8e-15 below for some mids, breaking the suite's own `>=` (`tests:158`) for unsampled mids.
  No venue impact — the floor is $10.
- **N-6** *(re-raised, reduced)* nothing binds execution to KVM2-P4-03 although packet §3 does; the run token
  is host-agnostic, so the tool remains runnable wherever `HL_*` resolves. The token gate greatly narrows
  this but does not close it.
- **N-7** *(re-raised, and now more load-bearing)* `--include-usd-class-transfer` has no test at all, and
  `usd_class_transfer` is still absent from the `ExchangeLike` protocol (`tools:105-122`) even though
  `usdClassTransfer` was added to `FUND_MOVING_ARMS` (`tools:69`) by this repair. The `# type: ignore
  [attr-defined]` also sits on `tools:534`, not on the attribute access at `tools:532`.
- **N-8** *(re-raised)* brief/record drift: `REVIEW_BRIEF.md:1` and `:6-7` still describe a probe that "ran
  once on testnet" and an r2 that "waits for the owner's word". r2 **and** r3 have run
  (`kvm2_dd06_probe_run_r2*.txt`, `..._r3*.txt`, `LEAD_READING_r2/r3`), and the candidate's own docstring
  cites "the r3 lesson" (`tools:22`). The Friday Sol lane would be briefed on a stale premise — and, given
  R-1, on the wrong idea of which branch the next run will take.
- **N-9** *(owner's call, re-raised unchanged)* arm order: `withdraw3`, the only arm that moves funds **off**
  the venue, still runs first (`tools:481-487`), ahead of the in-venue self-transfers whose non-refusal would
  trip the stop rule first. §3 of the packet is the owner-approved order, so this stays the owner's decision,
  not a reviewer's rewrite. r3 is evidence for reordering: spotSend was the arm that was not refused.
- **N-10** *(new)* `tests:154` asserts `len(digits) <= 5` as if it were an invariant of `control_order_size`.
  It is not: 1 273 of 285 723 swept mids produce a >5-significant-figure **integer** price (mid 111 150.0 →
  100 035.0), wire-valid only under the venue's integer exemption — the exemption `round_hl_price`'s own
  comment declines to rely on for values ≥ 10 000. The test passes only because it samples five mids.
- **N-11** *(new)* `test_dry_run_needs_no_credentials_and_no_network` (`tests:415-420`) is the one `main()`
  test that does **not** take the `offline` fixture. It is safe today — M-N shows the token gate catches it
  even if the dry-run early return is lost — but the lane rule reads better as "every `main()` test runs
  under `offline`", and adding the fixture costs one word.
- **N-12** *(new, process)* `opus/BRIEF.md:3` still pins `1af85067` and instructs BLOCK on any other HEAD,
  contradicting its own re-pin title, `REVIEW_BRIEF.md:1`, and the addendum. Fix before the Friday Sol lane.

---

## 9. NOT VERIFIED

- **I did not run the probe.** No credential was used, no SDK object was constructed outside a tripwired
  fixture, no venue was contacted, and no `HL_*` or `DD06_PROBE_RUN_TOKEN` variable was ever set. Everything
  in §1–§7 comes from reading the bytes, from the fixture suite, and from pure-math sweeps.
- **I did not re-run the full Bridge suite** (`1623 passed, 1 skipped` is the Lead's evidence, read as bytes
  and not re-derived). Reason, stated under the lane safety rule: this host's `HKCU\Environment` holds a live
  agent-wallet credential and `resolve_hyperliquid_credentials` falls back to it, so launching ~1 600 tests I
  have not individually audited is a venue-reachability risk I declined to take on the day a lane's mutant
  dialled the venue. §6 gives the structural argument that makes this cheap to accept.
- **Ruff was not re-run** — `ruff` is not installed in the Bridge interpreter
  (`No module named ruff`). The Lead's `LEAD_RUFF_slice3.txt` / R1 evidence was not re-derived.
- **Venue-side truth of r1/r2/r3** is taken from the recorded console, record JSON and public-read files in
  CT13. I verified those files exist and read them; I did not re-query the venue to confirm them.
- **Mainnet behaviour** is neither probed nor claimed, by the candidate or by me.
- **R-1's live consequence** is demonstrated by replaying recorded numbers through the shipped code offline.
  I did not observe the wrong sentence being printed by a real run, because I ran no run.

---

## 10. Reading

The repair is substantially good work. Every one of the first read's four REQUIRED findings is genuinely
closed, not papered over: two independent gates now stand ahead of any credential read, and — the part that
matters most — the `offline` fixture is load-bearing rather than decorative, because I confirmed that
`delenv` alone would not have stopped the resolver on this host. Fifteen of my sixteen mutants died on the
exact fence intended, and the one survivor is the one the Lead disclosed as a gesture.

It fails on the fifth thing the brief asked me to check: whether the fixtures still miss something that could
make the next run misreport. They do, and it is not hypothetical. The venue has already produced the
NOT_REFUSED branch once, and fed its own recorded numbers the repaired attribution announces the package's
most serious possible conclusion — "DD-06 falsified on testnet" — for an event in which nothing of the
master's moved. R-4 asked for a measurement instead of an assertion; the measurement is now taken and the
assertion drawn from it is still unearned. R-2 is the same shape on the other side: the one outcome class
where funds may have moved without a response is the one class that is never measured and never stops the
sequence.

Both are small, local, and already have failing inputs written. Round 1 of the T0 cap of 3.

VERDICT: REQUEST_CHANGES
