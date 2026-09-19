# T0 exact-Opus read — WP-P0-29 DD-06 testnet falsification probe — attempt 5

**Candidate `acd79b52`** (T0 repair round 3, the owner-authorized extra round `OD-20260918-DD06-CAP-A-1`).
Reviewer: exact `claude-opus-5`, xhigh. Fixture tests + code reading only — **the probe was not run**.
The safety rule of the 2026-09-17 addendum was honoured throughout: every mutation lived in a scratch
copy, only the fixture suite was ever run against a mutant, `main()` was never executed with a real SDK
object or a credential, and no command of mine could reach a venue (§7).

---

## 0. Verified identities

| Item | Value |
|---|---|
| COMPUTED HEAD (`git -c safe.directory=* -C C:/tmp/P029_DD06_20260915 rev-parse HEAD`) | `acd79b52efbbf8847621cabe1797cc6fc0567f17` ✅ matches the Subject pin |
| sha256 `IBKR_PAPER_BRIDGE/tools/dd06_agent_withdraw_probe.py` | `D0574D6CD4F6C32E8033F453670592FDFABBA0D3849E460ADF97EB25560D3E37` |
| sha256 `IBKR_PAPER_BRIDGE/tests/test_dd06_agent_withdraw_probe.py` | `7C79997DD7C642221CA1475E059A44448276EF8E2898AD5979B457DE32D4A03D` |
| Scope, base → candidate (`git diff --stat fcac0ac6 acd79b52`) | `2 files changed, 1608 insertions(+)` — exactly the two files ✅ |
| Scope, round-3 delta (`git diff --stat 2128352b acd79b52`) | `2 files changed, 94 insertions(+), 18 deletions(-)` — matches the claimed +94/−18 ✅ |
| Subject after my work | both hashes unchanged; HEAD unchanged; worktree never written to ✅ |

Git commands used: `rev-parse`, `show <sha>:<path>`, `diff --stat <sha> <sha>` only. No status, no
working-tree diff, no add/commit/checkout/push, in any repository.

In this report `tools:N` = `IBKR_PAPER_BRIDGE/tools/dd06_agent_withdraw_probe.py` line N at `acd79b52`,
`tests:N` the test file. Every line number below was re-grepped against the candidate's own bytes; none
is copied from an earlier report.

---

## 1. Suite re-run (brief item 6)

```
cwd C:/tmp/P029_DD06_20260915
C:/tmp/P012_FUNDING_PY312_20260911/Scripts/python.exe -m pytest \
  IBKR_PAPER_BRIDGE/tests/test_dd06_agent_withdraw_probe.py -q -p no:cacheprovider --basetemp C:/bt_opus_dd06
-> 31 passed in 0.59s
```

31, matching the claimed GREEN (28 → 31). No `HL_*` variable was present in my environment (checked
before the run: the `Get-ChildItem Env: | Where-Object Name -like 'HL_*'` filter printed nothing), and
`DD06_PROBE_RUN_TOKEN` was never set. Scope is exactly the two files (§0). I did not re-run the full
Bridge suite; the Lead's `LEAD_FULL_BRIDGE_SUITE_R3.txt` claim (1629/1) is recorded, not re-measured by
me → NOT VERIFIED (§7).

---

## 2. The four checks this round was authorized for (addendum of 2026-09-18)

All four pass. **The round-3 repair is correct and complete**; my REQUIRED finding in §6 is a
pre-existing hole elsewhere in the same function's caller, not a regression introduced by it.

| Addendum check | Result |
|---|---|
| **(a)** `_paid` back to readable-per-key | **KILLED.** My M-1 (hand-written round-2 body) → 3 failed; my exact splice of the *verbatim* round-2 `_paid` taken from `git show 2128352b:…` → the same 3 failed: `…[agent-pays-master-spot-unreadable]`, `…[nothing-moves-master-spot-unreadable]`, `test_paid_is_directional_amount_aware_and_unreadable_honest`. The spot-unreadable cases and the `_paid` unit are exactly the tests the addendum predicted. (The Lead's own row claims **4**; see **N-18** — the extra case is pinned by a different mutant, so the guard is covered either way.) |
| **(b)** MASTER_UNREADABLE branch removed | **KILLED.** M-2 → 2 failed: `…[agent-pays-master-unreadable]`, `…[agent-pays-master-spot-unreadable]` — both on the reappearance of "not the DD-06 breach". M-13 (the same branch disabled by `and False`) kills the same two. |
| **(c)** the decoy shape yields `None` for any amount | **CONFIRMED** by my own parametrized probe: `before {"accountValue": "0.0", "usdc_total": "983.987457"}` → `after {"accountValue": "0.0", "usdc_total": None}` returns `None` for 6.0, 1.0, 0.5, 0.01 and 1 000 000.0. One boundary exception exists at `amount = 0`, unreachable through the shipped table → **N-20**. |
| **(d)** round-2 complete-reading semantics unchanged; a master INCREASE can never be the breach | **CONFIRMED.** `_attribute(False, True)` → `DD06_FINDING_OWN_FUNDS_MOVED`; `(True, False)` → `MASTER_FUNDS_MOVED`; `(False, False)` → `NOT_REFUSED`; `(None, True)` → `MASTER_UNREADABLE`. Thresholds are half the arm amount and `set(ARM_AMOUNT_USDC) == set(FUND_MOVING_ARMS)`: withdraw3 6 → 3 (97.01 `False` / 97.0 `True` from 100.0), the 1 USDC arms → 0.5 (99.51 `False` / 99.5 `True`). Every master increase I tried (`983.987457 → 984.987457`, `→1000.0`, `→983.987458`, unchanged) returns `False`, and `False` cannot reach the breach label. |

---

## 3. Per-item findings (brief items 1–3, 6)

### Item 1 — no mainnet path, no key leak

| Guard | Where | Test that pins it | My mutant → result |
|---|---|---|---|
| `TESTNET_URL` hard-coded, and it is the only host `main` can dial | `tools:67`, used at `tools:842-843`, printed in the plan `tools:775` | `test_plan_names_the_testnet_host_and_the_gates` (`tests:519`) | **M-3** → `1 failed` ✅ |
| `refuse_unless_testnet` (mainnet + `HL_LIVE_ACK`) | `tools:253-261`, called `tools:815` | `test_refuses_mainnet_and_live_ack` (`tests:124`), `test_main_refuses_mainnet_before_reading_any_credential` (`tests:467`) | **M-5** (ack refusal deleted) → `1 failed` ✅, **and no test reached the resolver**: the `main()` test is stopped one line later by the token gate at `tools:816`, so the fence holds even with this refusal gone |
| `refuse_without_run_token` — second, independent gate | `tools:264-273`, called `tools:816` **before** any credential read or SDK object | `test_main_refuses_without_the_execution_token…` (`tests:475`), `test_run_token_gate_is_a_unit_of_its_own` (`tests:488`) | **M-6** → `1 failed`, and it fails on the **resolver tripwire** (`_NeverDial`, `tests:431-441`), never on a network error ✅ |
| `refuse_master_key` called in `main` | `tools:276-281`, called `tools:826` | `test_main_refuses_a_master_key_after_the_gates_and_before_any_sdk_object` (`tests:500`) | **M-4** → `1 failed`, again on a **tripwire** (`Info`), no network ✅ |
| `write_record` refuses a surviving hex | `tools:758-763` | `test_write_record_refuses_surviving_hex` (`tests:527`) | **M-7** → `1 failed` ✅ |
| redaction of 40/64-hex before any record | `tools:100-112`, applied in `_attempt` `tools:306-326` and `redact_map` `tools:160-164` | `test_all_arms_refused_…redacts_everything` (`tests:188`) asserts the key and both addresses are absent from the written bytes | not separately mutated; covered by M-7 and the assertion above |
| `del api_key` | `tools:825` | — | **M-8 → SURVIVED (31 passed).** Nothing pins it. This matches round 1's reading: it is a gesture, not a control. The code makes **no claim** for it (no comment asserts protection), so I do not file it; I record it so no later reader cites it as a guard |

No mainnet URL exists anywhere in the tool; `main` cannot be pointed at one (`--network` only gates,
`tools:796`; the URL is the constant). The credential is read exactly once (`tools:823`) after both gates.

### Item 2 — funds cannot leave silently

| Element | Where | Verdict |
|---|---|---|
| `STOP_ON_NOT_REFUSED` | `tools:90`, enforced `tools:688-691` | **M-10** (`= False`) → `9 failed` ✅ well pinned |
| withdraw3 amount 6 USDC, above the 5 USDC bridge minimum + 1 USDC fee | `tools:73`, asserted in the fake venue `tests:95` (`amount == probe.WITHDRAW_AMOUNT_USDC >= 6.0`) | **M-11** (`6.0 → 1.0`) → `11 failed` ✅ the floor is genuinely pinned |
| destination is the account's own master address | `tools:603-606` | own-address destination asserted `tests:95, 99, 103` ✅ |
| the packet says plainly that a non-refused withdraw3 leaves the venue | `tools:16-19` ("funds WOULD LEAVE the venue account … testnet faucet money") and the plan the owner reads, `tools:778` | present and unambiguous ✅ |
| the stop rule as stated to the owner | `tools:780` "Stop rule: a NOT_REFUSED fund-moving arm stops the sequence and records a FINDING" | **the stop rule has a third, unhandled outcome → R-1, §6** ❌ |

### Item 3 — classification honesty

`classify_response` (`tools:184-193`) grades an `err` envelope REFUSED, an `ok` envelope REFUSED when
`per_status_errors` (`tools:171-181`) finds a `statuses[].error`, a clean `ok` NOT_REFUSED, and
**anything else INCONCLUSIVE** (`tools:193`). `classify_exception` (`tools:196-203`) maps `ClientError`
→ REFUSED and everything else → ERROR.

**Can a VALIDATION refusal be counted as DD-06 evidence?** Not through the path round 1 closed. A bare
`"does not exist"` is VALIDATION (`tools:232`) and only the venue's signer sentence is AUTHORIZATION
(`tools:208`); **M-12** (moving `"does not exist"` back into the authorization list) → `1 failed` ✅.
The run only reaches `DD06_REFUSALS_OBSERVED` when every arm was refused **and** every refusal graded
AUTHORIZATION (`tools:715-717`); otherwise `DD06_INCONCLUSIVE` (`tools:719`). That is the code path the
brief asks for, and it is correct.

Two residues remain, both verified by me against the current bytes:
* the bare markers `"permission"` / `"agent"` / `"api wallet"` (`tools:213-215`) still catch
  validation-shaped texts, and authorization wins over validation by construction (`tools:246-249`):
  `"Extra agent already exists"`, `"Agent name too long"` and `"API Wallet limit reached"` all grade
  **AUTHORIZATION** → **N-17**. The real refusal texts recorded on testnet are not of this shape
  (r3: `"Error withdrawing from bridge"` → UNCLASSIFIED, `"Insufficient balance for withdrawal."` →
  VALIDATION), which is why this is a NIT and not a defect.
* a **wrong-key run cannot manufacture a clean verdict**: an agent key unknown to testnet would be
  refused at the control arm and the run aborts before any S2 arm (`tools:585-587`), pinned by
  `test_control_arm_rejection_aborts_before_any_transfer_arm` (`tests:355`). The control arm does the
  job it exists for. ✅

---

## 4. Item 4 — the control price, on my own sweep

```
cwd C:/tmp/OPUS_DD06_SCRATCH   python r4_price_sweep.py   (no network)
mids swept                                : 1,200,001 (10 000.0 .. 130 000.0 step 0.1, szDecimals=5)
price above 90 % of mid (could fill)      : 0
decimals > 1 (wire-invalid)               : 0
>5 significant figures, NON-integer       : 0        <- the r1 defect shape
>5 significant figures, integer (exempt)  : 1,700
worst notional                            : 10.499999999999998 at mid 10416.7 (px 9375.0, sz 0.00112)
r1 rejected price 69276.6 ever produced   : False
control_order_size(76974.0, 5)            : (69270.0, 0.00016)
control_order_size(60000.0, 5)            : (54000.0, 0.0002)
```

**Item 4 is satisfied.** The r1 rejection (`Price must be divisible by tick size`, 69276.6 from mid
76974.0) cannot recur for any mid ≥ 10 000: not one swept mid produces a non-integer price above five
significant figures, and 76974.0 now yields 69270.0 exactly as required. `control_order_size`
(`tools:284-292`) delegates the rounding to the Bridge's own `round_hl_price`
(`bridge/broker/hyperliquid.py:72-89`), which rounds DOWN, so the bid stays at or below 90 % of mid and
cannot fill. Two residues: 1 700 mids yield an integer price above five significant figures via the
early integral return (`bridge/broker/hyperliquid.py:79-80`), wire-valid only under the venue's integer
exemption → **N-10**; and the worst exact notional is 2e-15 below the `10.5` constant → **N-5**. Neither
is a venue risk (the venue floor is $10).

---

## 5. Item 5 — what the fixtures still do not carry

| Venue-shaped fact | Could it make the next run misreport? |
|---|---|
| **A 2xx whose body is not JSON** | **Yes — this is R-1.** The installed SDK turns it into a *return value*, not an exception (`hyperliquid/api.py:25-28`), and the probe has no branch for the resulting outcome. Demonstrated against the unmodified candidate |
| A balance endpoint failing on one wallet, or on one of a wallet's two endpoints | **Now handled** — this was the third read's R-1 and the round-3 repair closes it (§2 a/b). Both partial shapes are pinned (`tests:601-616`, cases `agent-pays-master-spot-unreadable`, `master-pays-perp-unreadable`, `nothing-moves-master-spot-unreadable`) |
| A wallet that simply holds **no USDC row** (the ordinary agent wallet) | Reads `usdc_total = None` (`tools:354-355`), so it can never be graded "did not pay" — it is always named UNREADABLE. Safe direction, but the record will call a wallet unmeasured that was read perfectly well → **N-21** |
| `marginSummary` or `balances` present but JSON `null` | `_balances` raises (`AttributeError` at `tools:341`, `TypeError` at `tools:350`) — uncaught, and `run_probe`/`write_record` are not wrapped in `main` (`tools:844-853`), so **the whole record is lost** at the worst possible moment → **N-19** |
| A venue balance string of `"NaN"` | `Decimal("NaN") - Decimal(x)` succeeds *inside* the try, and `delta <= -threshold` at `tools:385` — **outside** it — raises `InvalidOperation`; same lost-record consequence → **N-19** |
| Venue settlement latency on withdraw3 | Safe direction: a real breach would most likely land as `DD06_FINDING_NOT_REFUSED`, which still stops the run and forbids a conclusion (`tools:437`) → **N-14** |
| A funded perp position during the probe window | A mark-to-market drift ≥ half the arm amount is counted as a payment (`tools:385` accepts any key). Not reachable on this account (perp `accountValue` structurally `0.0`, verified in the r3 record; the 90 %-of-mid bid cannot fill) → **N-13** |
| A filled control order | `_resting_oid` (`tools:728-734`) matches a `filled` status's oid too (verified: returns 77 for a filled response), giving "cancel it by hand" — the wrong remedy for an open position → **N-3** |
| `--include-usd-class-transfer` | Still untested, and `usd_class_transfer` is absent from `ExchangeLike` (`tools:123-140`) though `usdClassTransfer` is in `FUND_MOVING_ARMS` (`tools:80`) and `ARM_AMOUNT_USDC` (`tools:88`) → **N-7** |
| withdraw3 against a **funded perp** balance | Still never exercised — r3's withdraw3 died on the agent's 0 perp balance with the opaque `"Error withdrawing from bridge"`. A fact about the package, not a defect in this candidate |

---

## 6. Findings

### REQUIRED

#### R-1 — a fund-moving arm whose outcome the tool cannot determine is neither measured nor stopped, and two further fund-moving requests are sent after it

**Where.** The arm loop `tools:665-714` branches on `REFUSED` (`tools:667`), `NOT_REFUSED`
(`tools:672`) and `ERROR` (`tools:692`). `classify_response` has a **fourth** return value,
`"INCONCLUSIVE"` (`tools:193`), and nothing in the loop handles it: execution falls through to the next
arm. The terminal label is then set at `tools:715-724` to `DD06_INCONCLUSIVE` with `finding = None`.

**Why it is reachable — the SDK's own documented behaviour, not a hypothetical.** Every fund-moving arm
returns whatever `Exchange._post_action` → `API.post` returns (`hyperliquid/exchange.py:101-110`), and
`API.post` does this (`hyperliquid/api.py:20-28`, SDK 0.24.0, the version installed in the Bridge
interpreter):

```python
        response = self.session.post(url, json=payload, timeout=self.timeout)
        self._handle_exception(response)          # raises only for status >= 400
        try:
            return response.json()
        except ValueError:
            return {"error": f"Could not parse JSON: {response.text}"}
```

A **2xx with a body that is not JSON** — a proxy or CDN interstitial, a truncated body, an empty body —
therefore never raises. It arrives as `{"error": "Could not parse JSON: …"}`, a dict with no `status`
key, which `classify_response` grades `INCONCLUSIVE`. Verified directly:

```
returned: {'error': 'Could not parse JSON: <html>502 Bad Gateway</html>'}
classify_response(that value) -> INCONCLUSIVE
JSONDecodeError is a ValueError: True
```

**Demonstrated** against the **unmodified** candidate (`C:/tmp/OPUS_DD06_SCRATCH/mutroot4`, fake venue
objects only, no network, no `main()`; `tests/test_r4_reviewer.py::test_R1_inconclusive_fund_arm_neither_stops_nor_measures`):

```
OUTCOME(withdraw3) : INCONCLUSIVE
RESULT             : DD06_INCONCLUSIVE
FINDING            : None
EXCHANGE CALLS     : ['order', 'cancel:60109082440', 'withdraw3', 'usdSend', 'spotSend', 'approveAgent']
POST-ARM RE-READS  : []
```

The venue was asked to move **6 USDC**; the tool cannot say whether it did; **neither wallet is
re-read**; and it then sends **two more signed fund-moving requests** (usdSend, spotSend) plus
approveAgent. The record ends with `finding: null` and a label indistinguishable from a benign run — my
second probe shows an ordinary "one refusal was not authorization-shaped" run producing the same
`DD06_INCONCLUSIVE`, the difference being that the benign one at least explains itself (`tools:721-724`).

**Why this is REQUIRED and not a NIT.**
1. It is the **same defect the owner already paid a round for**. Round 2's R-2 — "a fund-moving arm
   ending in ERROR was neither measured nor stopped" — was accepted as REQUIRED on exactly this
   reasoning, and the repair closed the **exception** channel only (`tools:692`). The **response**
   channel carries the identical risk, and the SDK routes unparseable 2xx bodies there by design. My
   third probe shows the two channels side by side: the same uncertainty reached through
   `ServerError` gives `DD06_INCONCLUSIVE_FUND_ARM_ERROR`, a re-read of both wallets and
   `SKIPPED_AFTER_ERROR` on every later arm; reached through the response it gives silence.
2. It breaks a guarantee stated to the owner in the plan he reads before authorizing the run
   (`tools:780`) and in the module docstring (`tools:19-20, 28-30`), which say a fund-moving arm that
   is not refused, or whose signed request may have executed, stops the sequence and re-reads both
   wallets.
3. The probe runs **once**, on a single owner word, against a funded testnet account, with a live
   agent credential. "We asked the venue to move money and cannot say what happened" is the one
   outcome the record must never pass over in silence.

**Remedy (one line plus its text).** Treat the undetermined response like the undetermined exception:

```python
        if outcome in ("ERROR", "INCONCLUSIVE") and name in FUND_MOVING_ARMS:
```

at `tools:692`, with the finding text distinguishing the two ("ended in ERROR" vs "returned a response
the probe could not classify — the signed request may have executed"), and a test that feeds
`{"error": "Could not parse JSON: …"}` to a fund-moving arm and asserts both the re-read and
`SKIPPED_AFTER_…` on the later arms. This also disposes of N-15's second half.

**What R-1 is not.** It is **not** a regression from round 3, and it does not touch the round-3 repair,
which is correct and complete on all four checks the owner authorized (§2). If the owner prefers, the
round-3 repair stands on its own merits and R-1 can be handled as a separate, named, one-line change —
that is his call, not mine.

### NIT

Carried from earlier reads, each **re-verified by me against the current bytes** (not copied):

- **N-3** *(re-raised, verified)* `_resting_oid` (`tools:728-734`) matches any `"oid": N`, a `filled`
  status included — I fed it a filled response and got `77`. A filled control order then yields
  `ABORTED_CONTROL_CANCEL_FAILED` and *"cancel it by hand"*, the wrong remedy for an open position.
  Second face of the same weakness: an order the venue **accepted** whose oid cannot be parsed yields
  `ABORTED_CONTROL_ARM_NOT_ACCEPTED` (`tools:585-587`) with `finding = None` — the record says "not
  accepted" about an order that was accepted, and nothing is cancelled (demonstrated in my
  `test_NIT_accepted_control_order_with_an_unparseable_oid_is_called_not_accepted`). Require the
  `resting` key, and say "an order may be resting" whenever the order was accepted.
- **N-4** *(re-raised, verified)* `_HEX40` (`tools:93`) requires the `0x` prefix, so a bare 40-hex string
  passes both `redact` and the `write_record` guard — `redact({"leak": "a1"*20})` returns it verbatim.
  `_HEX64` (`tools:92`) correctly makes the prefix optional. Addresses are public; hygiene only.
- **N-5** *(re-raised, re-measured)* worst exact notional over my 1.2 M-mid sweep is
  `10.499999999999998` at mid 10 416.7, 2e-15 below `CONTROL_MIN_NOTIONAL_USD`, which would break the
  suite's own `>=` at `tests:158` for unsampled mids. No venue impact (floor $10).
- **N-6** *(re-raised, reduced)* nothing binds execution to KVM2-P4-03 although §3 of the packet does;
  the run token is host-agnostic. I found no host check anywhere in the tool.
- **N-7** *(re-raised, verified)* `usd_class_transfer` is absent from `ExchangeLike` (`tools:123-140`)
  though `usdClassTransfer` is in `FUND_MOVING_ARMS` (`tools:80`) and `ARM_AMOUNT_USDC` (`tools:88`);
  the arm has no test; the `# type: ignore[attr-defined]` sits on the `arms.append(...)` close paren
  (`tools:654`) rather than on the attribute access (`tools:652`).
- **N-8** *(re-raised; residue unchanged)* `REVIEW_BRIEF.md:6` still describes the two files as
  "16 tests" (they are 31) and `REVIEW_BRIEF.md:7` still says "a corrected re-run r2 waits for the
  owner's word" although r2 and r3 have both run. The Friday Sol lane reads that body.
- **N-9** *(the owner's call, unchanged)* arm order: withdraw3, the only arm that moves funds **off** the
  venue, still runs first (`tools:600-607`). §3 of the packet is the owner-approved order. r3 is
  evidence for reordering — spotSend was the arm that was not refused.
- **N-10** *(re-raised, re-measured)* `tests:154` asserts `len(digits) <= 5` as though it were an
  invariant of `control_order_size`. It is not: 1 700 of my 1 200 001 swept mids give an integer price
  above five significant figures (mid 111 120.0 → 100 008.0), wire-valid only under the venue's integer
  exemption, which `round_hl_price`'s own comment (`bridge/broker/hyperliquid.py:84-87`) declines to
  rely on for values ≥ 10 000 and which the early integral return (`:79-80`) bypasses. The test passes
  because it samples five mids.
- **N-13** *(re-raised)* a mark-to-market drift ≥ half the arm amount is still counted as a payment:
  `tools:385` accepts a decrease in **either** key, and the threshold for the 1 USDC arms is 0.50.
  Not reachable on the account this probe runs against (the r3 record shows `accountValue "0.0"` with
  every dollar in `usdc_total "983.987457"`, and the 90 %-of-mid bid cannot fill), which is why it stays
  a NIT — it becomes REQUIRED the day the probe is pointed at an account holding a position.
- **N-14** *(re-raised)* a single post-arm snapshot (`tools:454`, `tools:464`) with no allowance for
  settlement latency; safe direction, but a real breach could be understated as `NOT_REFUSED`.
- **N-15** *(re-raised)* the ERROR branch embeds `_attribute`'s sentence verbatim (`tools:705-711`), so
  an errored arm's record reads "… was NOT refused; no readable balance decreased …", which is not what
  happened. The remedy for R-1 should fix this wording at the same time.
- **N-16** *(re-raised — still open)* the per-arm amount table is unpinned. **M-9** replaces the lookup
  at `tools:453` with a flat `TRANSFER_AMOUNT_USDC` and the suite still reports **31 passed**: nothing
  asserts that withdraw3 is measured against 6 USDC rather than 1. The values are correct today (§2 d),
  so this is coverage, not behaviour; both producers are `ARM_AMOUNT_USDC` (`tools:83-89`) and the
  lookup (`tools:453`), and the failing input is M-9 itself.
- **N-12** *(reopened)* `opus/BRIEF.md:3` still makes `2128352b` — the **round-2** sha — the BLOCK
  trigger ("if … HEAD is not 2128352b…, your verdict must be BLOCK"), while its own title line and
  `REVIEW_BRIEF.md:11` pin `acd79b52`. The same defect that was closed last round, re-created by the
  re-pin: the title was updated and the body was not. I proceeded on the two agreeing sources.

New this read:

- **N-17** *(new)* the bare markers `"permission"`, `"agent"`, `"api wallet"` (`tools:213-215`) grade
  validation-shaped texts as AUTHORIZATION, and authorization wins over validation (`tools:246-249`).
  Verified inputs: `"Extra agent already exists"`, `"Agent name too long"`, `"API Wallet limit reached"`
  → all **AUTHORIZATION**. Because `DD06_REFUSALS_OBSERVED` requires *every* refusal to be
  authorization-graded (`tools:716`), an over-grade on the approveAgent arm makes the run look cleaner
  than the evidence is. None of the venue texts actually recorded on testnet has this shape, which is
  why it is a NIT. Remedy: require a co-occurring signer/authority phrase, as `"user or api wallet"`
  (`tools:208`) already does.
- **N-18** *(new; the record, not the code)* the round-3 evidence row `R1a` claims **4 failed** and lists
  `…[agent-pays-master-unreadable]` among them. Restoring the **verbatim** round-2 `_paid` (spliced from
  `git show 2128352b:…`) into the candidate gives **3 failed**, without that case — round 2 already
  returned `None` when every key was unreadable on one side, so that case is pinned by the R1b mutant
  instead (my M-2 kills it). The fence is covered; the attribution in the table is off by one row.
- **N-19** *(new)* two uncaught paths in the post-arm measurement lose the **entire record** at the worst
  moment, because `run_probe` and `write_record` are not wrapped in `main` (`tools:844-853`):
  `_balances` raises `AttributeError` when `marginSummary` is JSON `null` (`tools:341`) and `TypeError`
  when `balances` is `null` (`tools:350`); `_paid` raises `InvalidOperation` on a `"NaN"` reading because
  the comparison at `tools:385` sits outside the try at `tools:380-383`. All three verified by
  `pytest.raises` in my probe file. Both triggers are unlikely from this venue, which is why they are a
  NIT — but the consequence (a `NOT_REFUSED` fund arm whose finding is never written) is severe enough
  to deserve a `try/except` around the measurement, or a `write_record` in a `finally`.
- **N-20** *(new, latent)* `delta <= -threshold` (`tools:385`) accepts `delta == 0` when the threshold is
  0, so `_paid(same, same, 0.0)` returns **True** — an unchanged, fully readable wallet "paid", and the
  master branch would print "DD-06 falsified on testnet". Not reachable through the shipped table
  (every `ARM_AMOUNT_USDC` value ≥ 1.0 and the lookup default is 1.0), so it is latent — but it is
  exactly the kind of change N-16's missing coverage would not catch. Require a strict decrease.
- **N-21** *(new)* a wallet holding no USDC row at all — the ordinary agent wallet — reads
  `usdc_total = None` (`tools:354-355`) and so can never be graded "did not pay"; it is reported as
  `UNREADABLE` with "re-read it by hand" although the read succeeded. The direction is the safe one
  (this is the conservatism round 3 asked for), but the record will send the operator after a
  non-existent failure. Distinguishing "absent" from "unreadable" would fix it.

---

## 7. NOT VERIFIED

- **I did not run the probe.** No credential was read; no `HL_*` variable and no `DD06_PROBE_RUN_TOKEN`
  was ever set by me; `main()` was never executed except through the candidate's own `offline` fixture
  (`tests:444-464`), whose tripwires replace the resolver and both SDK constructors; no SDK object was
  constructed against a venue URL; no network call of any kind was made. The two mutants that remove a
  gate (M-4, M-6) were confirmed to fail **on a tripwire**, and my driver additionally scanned every
  mutant run for network-shaped errors (`ConnectionError`, `Max retries`, `getaddrinfo`, `Timeout`) —
  **none appeared in any of the 14 runs**. The one place I exercised SDK code (`API.post`) used a
  hand-built fake response object with no session and an `example.invalid` base URL.
- **Everything DD-06 itself asks is still open.** Whether an agent wallet can withdraw from a **funded**
  perp balance was not established by r1–r3 and is not established here; r3's withdraw3 returned the
  opaque `"Error withdrawing from bridge"`, graded UNCLASSIFIED. DD-06 stays BLOCK.
- **Mainnet parity is not claimed** by the candidate or by me.
- **Not re-measured by me:** the full Bridge suite (1629 passed / 1 skipped), Ruff (7 pre-existing), the
  guard PASS, and the Gemini `DD06_R3_GEMINI` delta — all recorded in
  `REPAIR_R3_20260918/` and taken as the Lead's claims, not as my measurements. I re-ran only the
  focused suite (§1) and my own probes and mutants.
- **The r1/r2/r3 testnet runs** are read from the redacted records under
  `QUEUED_PACKAGES_20260915/P029/DD06_TESTNET_PROBE_20260915/`; I verified the r3 balances and venue
  texts against those bytes, not against any report's description of them.

---

## 8. Reproduction

All of my artifacts are under `C:/tmp/OPUS_DD06_SCRATCH/` (nothing outside my report directory and the
scratch root was written):

| File | What it does |
|---|---|
| `mutroot4/` | byte-identical copy of the candidate's two files (hashes match §0) + `bridge/` + my `conftest.py` |
| `mutroot4/tests/test_r4_reviewer.py` | my 17 probes against the **unmodified** candidate — `48 passed` together with the candidate's 31 |
| `mutate4.py` → `R4_MUTANTS_OUT.txt` | the 13-mutant battery (baseline `31 passed`; pristine restored and re-verified afterwards) |
| `r4_m1_exact.py` | splices the verbatim round-2 `_paid` from `git show 2128352b:…` — the N-18 measurement |
| `r4_price_sweep.py` | the 1 200 001-mid item-4 sweep |
| `r4_residues.py` | N-3/N-4/N-7/N-17/N-20 checks against the current bytes |
| `r4_decimal_probe.py` | the `Decimal` NaN check and the SDK `API.post` non-JSON 2xx check |

---

## 9. Summary

The repair this round was authorized for is **sound**: all four addendum checks pass, the partial-read
defect the third read found is properly closed, the complete-reading semantics of round 2 are intact,
the scope is exactly the two files, and every safety fence I mutated was killed by a test — with the
removed-gate mutants stopping on tripwires rather than on the network. Item 4 is satisfied on a sweep of
my own. Item 1 holds with one honest caveat (`del api_key` is unpinned and unclaimed).

It fails on one pre-existing hole that no earlier read covered: `classify_response` has three outcomes
and the arm loop handles two, so a fund-moving arm whose result the tool cannot determine — the shape
the installed SDK produces for any 2xx with a non-JSON body — is passed over in silence while two more
signed fund-moving requests follow it. That is the guarantee the owner is shown before he authorizes the
run, and it is one line from being kept.

VERDICT: REQUEST_CHANGES
