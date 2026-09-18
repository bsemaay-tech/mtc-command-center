# T0 exact-Opus read — WP-P0-29 DD-06 testnet falsification probe — attempt 6

Reviewer: exact `claude-opus-5`, xhigh, fresh session, no delegation, no sub-agents.
Round 4 read of `a46da0aa` (owner `OD-20260918-DD06-R4-A-1`, arm order B `OD-20260918-DD06-ORDER-B-1`).
Safety rule of the 2026-09-17 addendum observed throughout: every mutation in a scratch copy, the
fixture suite only, `main()` never with a real SDK object or a venue URL, no network call of any kind.

---

## 0. Verified identities

| What | Value |
|---|---|
| COMPUTED HEAD (`git -c safe.directory=* -C C:/tmp/P029_DD06_20260915 rev-parse HEAD`) | `a46da0aa7a4ea3a58fb00c5e293e10b60307687d` |
| sha256 `IBKR_PAPER_BRIDGE/tools/dd06_agent_withdraw_probe.py` | `66125F5DBDF4CD1442E6991E70F7EAA0C2DF25C7149349DFBE55D19006293C0B` |
| sha256 `IBKR_PAPER_BRIDGE/tests/test_dd06_agent_withdraw_probe.py` | `D667762961E66E89BB41099CC1E54FEED96A227BB84A31E213DAB96A2E61F89A` |
| Scope (`git diff --stat acd79b52 a46da0aa`) | exactly two files, `+92 −29` — matches the addendum's claim |

**The launch brief contradicts itself and I did not BLOCK on it.** `opus/BRIEF.md:1` re-pins the candidate
to `a46da0aa`, and `REVIEW_BRIEF.md:11` (Subject) pins `a46da0aa`; but `opus/BRIEF.md:3` still carries
*"if … HEAD is not 2128352b348902a8b4755d2566e133c55094af8b, your verdict must be BLOCK"* — the **round-2**
sha, now two rounds stale. The observed HEAD equals the two agreeing sources, so I proceeded and filed the
residue as **N-12 (re-reopened)**. This is the third consecutive round in which the BRIEF title was
re-pinned and its body was not.

---

## 1. Suite re-run (brief item 6)

```
cwd C:/tmp/P029_DD06_20260915
C:/tmp/P012_FUNDING_PY312_20260911/Scripts/python.exe -m pytest \
  IBKR_PAPER_BRIDGE/tests/test_dd06_agent_withdraw_probe.py -q -p no:cacheprovider --basetemp C:/bt_opus_dd06
................................                                         [100%]
32 passed in 1.14s
```

My pristine scratch copy (`C:/tmp/OPUS_DD06_SCRATCH/A6/base`, `bridge/` + `tools/` + the two test files)
reproduces it exactly: `32 passed in 0.51s`. Every mutant below is measured against that baseline.

Full Bridge suite (my own run, item 6): see §6 — `FULL_BRIDGE_SUITE_A6.txt`.

---

## 2. The four checks this round was authorized for

| # | Check | Result |
|---|---|---|
| (a) | `INCONCLUSIVE` dropped from the branch condition → the unclassifiable test must fail | **KILLED** — `M-A` → `1 failed`, exactly `test_unclassifiable_response_on_fund_arm_is_measured_and_stops` |
| (b) | the stop (`return`) removed after the re-read → both undetermined-outcome tests must fail | **KILLED** — `M-B` → `2 failed`: `test_transport_error_is_inconclusive_not_a_refusal` **and** `test_unclassifiable_response_on_fund_arm_is_measured_and_stops` |
| (c) | withdraw3 moved back to first → the order-pinning tests must fail | **KILLED** — `M-C` → `4 failed` (all-refused order pin, not-refused stop, transport error, unclassifiable) |
| (d) | an `INCONCLUSIVE` on `approveAgent` still ends in the ordinary end-of-run `DD06_INCONCLUSIVE`; `_paid` / `_attribute` / gates / offline fixture byte-unchanged from `acd79b52` | **CONFIRMED**, both halves — see below |

**(d) first half**, my own probe (`tests/test_a6_reviewer_probe.py`, scratch only), an unparsable
`approveAgent` response on an otherwise all-refused run:

```
RESULT: DD06_INCONCLUSIVE FINDING: None
exchange.calls == ['order','cancel:60109082440','usdSend','spotSend','withdraw3','approveAgent']
no post_approveAgent_* step; no SKIPPED_AFTER_UNCLASSIFIED marker
```
The `and name in FUND_MOVING_ARMS` guard (`tools:702`) holds: a non-fund arm does not take the
re-read/stop path, every fund arm was still tried, and the run ends on the ordinary
`record.result == "RUNNING"` path (`tools:738-747`). An `ERROR` on `approveAgent` behaves identically.
`finding` is `None` there — Gemini's round-4 NIT, which I confirm and carry as **N-24**.

**(d) second half** — I parsed both revisions with `ast` and sha256'd each function body
(`C:/tmp/OPUS_DD06_SCRATCH/A6/tool_acd79b52.py` from `git show acd79b52:…` vs the candidate):

```
SAME  _paid  _attribute  _reread_both_wallets  _balances  _attempt  redact
SAME  refuse_unless_testnet  refuse_without_run_token  refuse_master_key  write_record
SAME  classify_response  classify_exception  classify_refusal_text  per_status_errors
SAME  control_order_size  main
SAME  test:offline  test:_NeverDial
```
18 of 18 byte-identical. The whole round-4 delta is the docstring, `FUND_MOVING_ARMS`' order, the arm-list
order, the undetermined-outcome branch, and `plan_text` — confirmed against the diff itself.

---

## 3. Per-item findings (brief items 1–6)

### Item 1 — no mainnet path, no key leak

| Control | Where | Test that pins it | My mutant |
|---|---|---|---|
| `TESTNET_URL` hard-coded, no mainnet URL anywhere | `tools:73`, used `tools:866-867` | `test_plan_names_the_testnet_host_and_the_gates` (`tests:558`) | — (killed by attempt 5's M-3; unchanged bytes) |
| `refuse_unless_testnet` | `tools:259-267`, called `tools:839` | `test_refuses_mainnet_and_live_ack` (`tests:124`) | **M-I** (HL_LIVE_ACK refusal deleted) → `1 failed`, that unit only |
| `HL_LIVE_ACK` refusal | `tools:264-267` | same | **M-I**: with it gone, the `main()` test that sets `HL_LIVE_ACK` still returns 3 — stopped by the **token gate** (`tools:840` → `refuse_without_run_token`, `tools:270-279`) before any credential read. Tripwire not reached, **no network-shaped error** |
| `DD06_PROBE_RUN_TOKEN` second gate | `tools:270-279`, called `tools:840` | `test_main_refuses_without_the_execution_token…` (`tests:514`), `test_run_token_gate_is_a_unit_of_its_own` (`tests:527`) | **M-H** (gate deleted from `main`) → `1 failed` **on the resolver tripwire** (`resolve_hyperliquid_credentials must never be reached from the fixture suite`), not on the venue |
| master-key refusal | `tools:282-288`, called `tools:850` | `test_main_refuses_a_master_key_after_the_gates_and_before_any_sdk_object` (`tests:539`) | unchanged bytes; attempt 5's mutant died on the `Info` tripwire |
| redaction before any record | `tools:98-99`, `106-118`, applied in `_attempt` (`tools:313-332`) and `redact_map` (`tools:166-170`) | `test_all_arms_refused_…redacts_everything` (`tests:188`) asserts the key and both addresses are absent from the written bytes | — |
| `write_record` refuses a surviving hex | `tools:781-786` | `test_write_record_refuses_surviving_hex` (`tests:566`) | — |
| `del api_key` | `tools:849` | **none** | **M-L** (line deleted) → **SURVIVED, 32 passed.** Nothing pins it. The code makes no claim for it (no comment calls it a control), so I file no finding — I record it so no later reader cites it as a guard. This matches rounds 1 and 5. |

Two independent gates sit before the credential read (`tools:839-840`, resolver at `tools:847`), so no
single-line change reaches a venue from the suite — the property the 2026-09-17 incident cost. Both
removed-gate mutants confirmed that by hand.

### Item 2 — funds cannot leave silently

- `STOP_ON_NOT_REFUSED` (`tools:96`) is honoured at `tools:698-701`; later arms are marked
  `SKIPPED_AFTER_FINDING` and the function returns. **M-J** (skip marks removed) → `2 failed`.
- withdraw3 amount **6.0 USDC** (`tools:79`) and destination = the account's own address
  (`tools:660-662`). **M-O** (amount → 1.0) → `2 failed`; **M-P** (destination → a foreign address) →
  `2 failed`. Both fenced.
- The packet states it plainly: *"if NOT refused, 6 test-USDC leave the venue to an address you control"*
  (`DD06_TESTNET_PROBE_STEP_PACKET_20260915.md:22`) and again at `:26`.
- **Order B strictly improves this property.** withdraw3 — the only arm that moves funds *off* the venue —
  now runs last (`tools:656-664`), after the self-transfer arms, so any earlier non-refusal stops the run
  before the off-venue request is ever signed. Verified for the full optional-arm configuration too
  (no shipped test covers it): `usdSend, spotSend, subAccountTransfer, usdClassTransfer, withdraw3,
  approveAgent`. This closes **N-9**, which was the owner's to decide.

### Item 3 — classification honesty

`classify_response` (`tools:190-199`) has three outcomes; `classify_exception` (`tools:202-209`) adds
`ERROR`. For a name in `FUND_MOVING_ARMS` **all four are now handled**: `REFUSED` → continue
(`tools:677-681`), `NOT_REFUSED` → measure + stop (`tools:682-701`), `ERROR`/`INCONCLUSIVE` → measure +
stop (`tools:702-737`). That is the exhaustiveness attempt 5's R-1 was about, and it is complete.

A VALIDATION refusal can never be counted as DD-06 evidence: `DD06_REFUSALS_OBSERVED` needs
`refused == len(arms) and authorization_refusals == len(arms)` (`tools:739`), and
`authorization_refusals` only increments on `refusal_class == "AUTHORIZATION"` (`tools:679-680`);
anything else falls to `DD06_INCONCLUSIVE` (`tools:742`). `test_validation_shaped_refusal_makes_the_run_inconclusive`
(`tests:312`) pins it. R-3's narrowing survives: `"Sub-account 0xabc does not exist"` → VALIDATION,
`"User or API Wallet 0xabc does not exist."` → AUTHORIZATION (`tests:297-306`, re-run by me).

### Item 4 — the control price, on my own sweep

`control_order_size` (`tools:290-298`) via `round_hl_price`. I swept **every mid from 10 000.0 to
500 000.0 in 0.1 steps (4.9 M prices)**, szDecimals 5:

```
non-integer prices above 5 significant figures : 0
prices with more than one decimal place        : 0
prices above 90 % of mid                       : 0
orders below the venue's $10 floor             : 0
worst notional shortfall vs CONTROL_MIN_NOTIONAL_USD (10.5): 1.78e-15 at mid 10416.7
```

**The r1 rejection (`Price must be divisible by tick size`, 69276.6) cannot recur for any mid ≥ 10 000.**
Mechanism: for `mid*0.9 ≥ 10 000` the guard digit at `bridge/broker/hyperliquid.py:86-87` quantises to
tens or coarser, so the result is an integer; for `9 000 ≤ mid*0.9 < 10 000` the quantum is 0.1 on a
four-digit integer part, i.e. exactly five significant figures. `76974.0 → 69270.0` reproduced.

### Item 5 — what the fixtures still do not carry

Re-checked against the **installed** SDK (`hyperliquid` 0.24-shape, `…/site-packages/hyperliquid`):

- **Confirmed faithful:** `ClientError` is raised only for 4xx and `ServerError` for ≥ 5xx
  (`api.py:30-43`), so `classify_exception`'s name test is sound; and the round-4 premise is real —
  `api.py:25-28` returns `{"error": f"Could not parse JSON: {response.text}"}` for a 2xx non-JSON body
  **without raising**. All six exchange methods the arms call exist with matching signatures
  (`usd_transfer:579`, `spot_transfer:590`, `withdraw_from_bridge:624`, `sub_account_transfer:518`,
  `usd_class_transfer:474`, `approve_agent:635`).
- **Still not carried by the fixtures:** the real `statuses` shapes for withdraw3/usdSend/spotSend (the
  fakes return `{"type": "default"}` or a bare `status: err` string — no venue capture of a *successful*
  transfer envelope exists in the records); a unified-account `spot_user_state` with several tokens; a
  wallet with **no** USDC row (see N-21); `marginSummary` present but `null` (see N-19); and the
  `usdClassTransfer` arm, which no test exercises at all (N-7).
- **Could any of them make the next run misreport?** The one that could is N-19's shape
  (`marginSummary: null` / `balances: null`): it raises out of the post-arm measurement and, because
  `write_record` runs only after `run_probe` returns (`tools:868-877`), the **entire record is lost** at
  the exact moment a fund arm was not refused. Low probability, high consequence — see N-19/N-26.

### Item 6 — scope and suite

Exactly two files (§0). Focused suite 32/32 from the worktree and from my scratch copy. Full Bridge
suite: §6.

---

## 4. My own mutants

All runs: `cwd C:/tmp/OPUS_DD06_SCRATCH/A6/mut_<id>`, driver
`C:/tmp/OPUS_DD06_SCRATCH/A6/run_mutants.py` / `run_mutants2.py`, command

```
C:/tmp/P012_FUNDING_PY312_20260911/Scripts/python.exe -m pytest \
  tests/test_dd06_agent_withdraw_probe.py -q -p no:cacheprovider --basetemp C:/bt_opus_dd06_a6
```

The driver scans every run for the tripwire string and for network-shaped errors
(`ConnectionError`, `Max retries`, `getaddrinfo`, `requests.exceptions`, `api.hyperliquid`, …).
Baseline `32 passed`. Raw output per mutant in `C:/tmp/OPUS_DD06_SCRATCH/A6/out_*.txt`.

| id | mutation (tool file only; never the tests, never the `offline` fixture) | result | network-shaped? |
|---|---|---|---|
| M-A | `outcome in ("ERROR","INCONCLUSIVE")` → `outcome == "ERROR"` | KILLED 1 | no |
| M-B | the `return record` after the re-read removed | KILLED 2 | no |
| M-C | withdraw3 restored as the first arm | KILLED 4 | no |
| M-D | `spotSend` removed from `FUND_MOVING_ARMS` | KILLED 9 | no |
| M-E | the UNCLASSIFIED channel relabelled `…_FUND_ARM_ERROR` | KILLED 1 | no |
| M-F | `_paid` back to readable-per-key (round-3 repair undone) | KILLED 4 | no |
| M-G | the `MASTER_UNREADABLE` branch disabled | KILLED 2 | no |
| M-H | the run-token gate deleted from `main` | KILLED 1 — **on the resolver tripwire** | no |
| M-I | the `HL_LIVE_ACK` refusal deleted | KILLED 1 — the token gate stops `main` first | no |
| M-J | later arms no longer marked skipped on the stop path | KILLED 2 | no |
| M-K | `ARM_AMOUNT_USDC` lookup → flat `TRANSFER_AMOUNT_USDC` | **SURVIVED 32** → N-16 | no |
| M-L | `del api_key` deleted | **SURVIVED 32** → recorded, not filed | no |
| M-N | `and name in FUND_MOVING_ARMS` dropped from the undetermined branch | **SURVIVED 32** → N-23 | no |
| M-O | `WITHDRAW_AMOUNT_USDC` 6.0 → 1.0 | KILLED 2 | no |
| M-P | withdraw3 destination → a foreign address | KILLED 2 | no |

Round-3's repairs are still fenced on the round-4 bytes (M-F, M-G), and the two gate-removal mutants die
on tripwires rather than on a dial-out (M-H, M-I) — the property the incident of 2026-09-17 made binding.

---

## 5. Findings

### REQUIRED

**None.** The round-4 repair does what the addendum says, the fences hold, the scope is two files, and I
found no defect this round that makes the probe's output wrong or lets funds move unrecorded.

### Blocking for the next EXECUTION (not defects in this candidate)

- **N-22 (new) — the owner-approved step packet is two rounds stale, and executing it verbatim now fails.**
  `DD06_TESTNET_PROBE_STEP_PACKET_20260915.md:22` still lists the S2 arms as
  *"`withdraw3` …, `usdSend`, `spotSend`, `approveAgent`"* — the pre-order-B sequence the tool no longer
  runs. Worse, the step-2 command line there (and in the newest runner,
  `kvm2_dd06_probe_run_r3.sh:15`) sets **no `DD06_PROBE_RUN_TOKEN`**, because the token gate was added in
  round 1 *after* the packet and all three runs were written. Run as written, the probe exits 3 with
  `PROBE_REFUSED: DD06_PROBE_RUN_TOKEN must equal the run id (…)` and nothing is probed. The token must
  equal `--run-id`, which carries a UTC stamp, so it cannot be pre-baked into `/etc/mtc-bridge/…env`.
  Remedy: an addendum row to the packet naming order B and adding
  `DD06_PROBE_RUN_TOKEN="$RUN_ID"` to the runner, before step 2 is executed. The tool is correct here;
  the documents are behind it. (`--dry-run`, step 1 of the packet, does print the correct order and the
  gate list — `tools:796-812` — so the operator has one in-band authority.)
- **N-25 (new; records)** the addendum cites Lead evidence at
  `P029/DD06_TESTNET_PROBE_20260915/REPAIR_R4_20260918/`. **That directory does not exist** in CT13
  (rounds 1–3 each have theirs; round 4 has only `ADJUDICATION_R4_20260918/`, holding the *fourth
  reader's* probe file and a repro note). The round-4 mutant evidence, the GREEN 32, the 1630/1 and the
  ruff/guard rows are therefore unverifiable at the cited path. I re-derived all of the code claims
  myself (§2, §4), so this does not change my verdict — but the record should be filed where the brief
  says it is.

### NIT

Carried items, each **re-verified by me against the current bytes** (printed output in
`C:/tmp/OPUS_DD06_SCRATCH/A6/base/tests/test_a6_carried_nits.py`), never copied from an earlier report:

- **N-3** *(re-raised)* `_resting_oid` (`tools:751-757`) matches any `"oid": N` — I fed it a **filled**
  status and got `77`. A filled control order then reports `ABORTED_CONTROL_CANCEL_FAILED` / "cancel it by
  hand", the wrong remedy for an open position; and an accepted order whose oid will not parse reports
  `ABORTED_CONTROL_ARM_NOT_ACCEPTED` (`tools:591-593`) with `finding = None`. Require the `resting` key.
- **N-4** *(re-raised)* `_HEX40` (`tools:99`) requires the `0x` prefix: `redact({"leak": "a1"*20})`
  returns the bare address verbatim, and the `write_record` guard (`tools:783`) misses it too. `_HEX64`
  correctly makes the prefix optional. Addresses are public; hygiene only.
- **N-5** *(re-raised, re-measured)* worst exact notional over my 4.9 M-mid sweep is `10.499999999999998`
  at mid 10 416.7 — 1.8e-15 under `CONTROL_MIN_NOTIONAL_USD`, which would break the suite's own `>=`
  (`tests:158`) for unsampled mids. No venue impact: never below the $10 floor.
- **N-6** *(re-raised)* nothing binds execution to KVM2-P4-03 although §3 of the packet does; the run
  token is host-agnostic. No host check exists in the tool.
- **N-7** *(re-raised)* `usd_class_transfer` is absent from `ExchangeLike` (`tools:129-147`, members
  printed) though `usdClassTransfer` is in `FUND_MOVING_ARMS` (`tools:85`) and `ARM_AMOUNT_USDC`
  (`tools:94`); the `# type: ignore[attr-defined]` still sits on the `arms.append(...)` close paren
  (`tools:655`) rather than on the attribute access (`tools:654`); **no test enables the arm.** Under
  order B this now matters more than it did: `usdClassTransfer` runs *before* withdraw3, and any
  pre-send local failure there (an SDK without the method → `AttributeError`) is graded `ERROR`, which
  stops the run and records *"the signed request may have executed"* for a request that was never signed.
  The installed SDK has the method, so this is latent.
- **N-10** *(re-raised, re-measured)* `tests:154` asserts `len(digits) <= 5` as if it were an invariant of
  `control_order_size`. It is not: **12 500 counterexamples** in a 10 000→250 000 step-10 sweep, e.g.
  mid `111120.0 → 100008.0`, mid `123460.0 → 111114.0` — six significant figures. They are wire-valid
  only under the venue's integer exemption, which `round_hl_price` reaches by its early integral return
  (`bridge/broker/hyperliquid.py:79-80`, pinned by the Bridge's own contract test
  `tests/test_hyperliquid_broker.py:187`). The test passes because it samples five mids.
- **N-13** *(re-raised)* a mark-to-market drift ≥ half the arm amount still counts as a payment:
  `_paid(100.0→99.4 accountValue, USDC untouched, arm 1.0)` returns **True**. Unreachable on this account
  (perp `accountValue` is structurally `"0.0"`, every dollar in spot) — it becomes REQUIRED the day the
  probe is pointed at an account holding a position.
- **N-14** *(re-raised, extended)* a single post-arm snapshot (`tools:460`, `tools:470`) with no allowance
  for settlement latency; and the *before* snapshot (`tools:545-546`) is taken before the control arm, so
  anything the control order did sits inside the measurement window. Safe direction (understates).
- **N-15** *(re-raised, now on two channels)* both undetermined branches embed `_attribute`'s sentence
  verbatim, so the record reads *"spotSend returned a response the probe could not classify … : spotSend
  **was NOT refused**; no readable balance decreased …"* — a self-contradicting finding. Verified on both
  the ERROR and the UNCLASSIFIED path. `_attribute` (`tools:396-445`) should take the channel, or the
  caller should strip the clause.
- **N-16** *(re-raised — still open)* the per-arm amount table is unpinned: **M-K** replaces the lookup
  (`tools:459`) with a flat `TRANSFER_AMOUNT_USDC` and the suite still reports **32 passed**. Nothing
  asserts that withdraw3 is measured against 6 USDC rather than 1. Values are correct today; this is
  coverage, not behaviour.
- **N-17** *(re-raised)* the bare markers `"permission"`, `"agent"`, `"api wallet"` (`tools:219-221`)
  grade validation-shaped texts as AUTHORIZATION, and authorization wins over validation
  (`tools:252-255`). Verified: `"Extra agent already exists"`, `"Agent name too long"`,
  `"API Wallet limit reached"`, `"Insufficient permission balance"` → **all AUTHORIZATION**. Since
  `DD06_REFUSALS_OBSERVED` — the one outcome that moves the register row — needs *every* refusal
  authorization-graded (`tools:739`), an over-grade makes the run look cleaner than the evidence is. It
  stays a NIT because the packet (`:31`) makes the Lead re-read every recorded text by hand.
- **N-19** *(re-raised)* uncaught paths in the post-arm measurement: `_balances` raises `AttributeError`
  on `marginSummary: null` (assigned `tools:347`, dereferenced `tools:348`) and `TypeError` on
  `balances: null` (assigned `tools:356`, iterated `tools:357-359`); `_paid`
  raises `InvalidOperation` on a `"NaN"` reading because the comparison (`tools:391`) sits outside the try
  (`tools:386-390`). All three verified with `pytest.raises`. Consequence below.
- **N-20** *(re-raised)* `delta <= -threshold` (`tools:391`) accepts `delta == 0` when the threshold is 0:
  `_paid(same, same, 0.0)` → **True**, i.e. an unchanged, fully readable wallet "paid" and the master
  branch would print *"DD-06 falsified on testnet"*. Latent (every shipped amount ≥ 1.0), and exactly the
  change N-16's missing coverage would not catch. Require a strict decrease.
- **N-21** *(re-raised)* a wallet holding **no USDC row** — the ordinary shape of an agent wallet — reads
  `{'accountValue': '0.0', 'usdc_total': None}` (`tools:357-361`) and can therefore never be graded "did
  not pay": it is reported `UNREADABLE` with "re-read it by hand" although the read succeeded. Safe
  direction; the record sends the operator after a failure that did not happen.

New this read:

- **N-23** *(new; coverage)* the guard that keeps non-fund arms off the re-read/stop path is unfenced:
  **M-N** drops `and name in FUND_MOVING_ARMS` from `tools:702` and the suite still reports **32 passed**.
  The behaviour is correct today (I pinned it in my own probe), but check (d) of this round's addendum
  rests on a line no shipped test defends. One test — an unclassifiable `approveAgent` asserting
  `DD06_INCONCLUSIVE` and no `post_approveAgent_*` step — closes it.
- **N-24** *(new; Gemini's round-4 NIT, confirmed)* an `ERROR` or `INCONCLUSIVE` on `approveAgent` ends
  the run as `DD06_INCONCLUSIVE` with **`finding = None`** (`tools:738-747`), indistinguishable in the
  `result` field from a validation-graded refusal run, which *does* get a finding (`tools:744-747`). The
  per-step record still carries the outcome and the redacted response, so nothing is hidden — but the
  operator's one-line summary says nothing. Give the `RUNNING`-fallthrough an else-branch naming the arm
  and its outcome.
- **N-26** *(new; generalises N-19)* `run_probe` accumulates the whole record in memory and `write_record`
  runs **only if `run_probe` returns normally** (`tools:868-877`); nothing is printed during the run
  (`main` prints once, `tools:878`). So *every* abort path discards the complete record of arms already
  sent: the uncaught exceptions of N-19, the operator's `KeyboardInterrupt` (deliberately re-raised at
  `tools:307-308` under N-2), and the packet's `timeout 300` kill (`kvm2_dd06_probe_run_r3.sh:15`). The
  case that matters: a fund-moving arm is not refused, the re-read throws, and the run leaves **no
  record file at all** at precisely the moment the evidence is most valuable. Remedy: `write_record` in a
  `finally`, or flush each step as it is appended. With N-19 this is the strongest remaining item and the
  one I would fix first if the owner grants another round.

Residue in this lane's own documents (unchanged from attempt 5, so not re-argued):

- **N-8** `REVIEW_BRIEF.md:6` still says the two files are "16 tests" (they are 32) and `:7` still says
  "a corrected re-run r2 waits for the owner's word" though r2 and r3 have both run. The Friday Sol lane
  reads that body.
- **N-12** *(re-reopened)* `opus/BRIEF.md:3` — see §0. Third round running.
- One correction to the addendum's own summary of attempt 5 (`REVIEW_BRIEF.md:47`): it lists
  "N-17 (`del api_key` unpinned)". Attempt 5's N-17 is the over-broad AUTHORIZATION markers; it recorded
  `del api_key` as unpinned-and-unclaimed and deliberately filed **no** finding for it. I reach the same
  place independently (M-L).

---

## 6. Full Bridge suite (item 6)

```
cwd C:/tmp/P029_DD06_20260915
C:/tmp/P012_FUNDING_PY312_20260911/Scripts/python.exe -m pytest IBKR_PAPER_BRIDGE/tests \
  -q -p no:cacheprovider --basetemp C:/bt_opus_dd06_a6full
```
```
1630 passed, 1 skipped, 1 warning in 202.19s (0:03:22)
```

Matches the addendum's claim exactly (`1630/1`). The one warning is a pre-existing
`StarletteDeprecationWarning` from `fastapi/testclient.py`, unrelated to these two files. Full output in
`C:/tmp/OPUS_DD06_SCRATCH/A6/FULL_BRIDGE_SUITE_A6.txt`.

---

## 7. NOT VERIFIED

- **I did not run the probe.** No credential was read. I never set `HL_API_WALLET_KEY`,
  `HL_ACCOUNT_ADDRESS`, `HL_LIVE_ACK` or `DD06_PROBE_RUN_TOKEN`. `main()` executed only through the
  candidate's own `offline` fixture (`tests:483-503`), whose tripwires replace
  `resolve_hyperliquid_credentials` and both SDK constructors; I neither removed nor weakened that
  fixture in any mutant. No SDK object was ever constructed against a venue URL. **No network call of any
  kind was made** — the two gate-removal mutants died on tripwires, and my driver scanned all 15 mutant
  runs for network-shaped errors: none. No incident to disclose.
- **Venue behaviour is unproven.** Nothing here says what Hyperliquid testnet will actually answer; the
  fixtures are the Lead's model of it (item 5 lists what they still do not carry). DD-06 remains BLOCK.
- **The Lead's round-4 evidence rows were not verified at the cited path** (N-25) — I re-derived the code
  claims with my own mutants instead. Ruff and the protected-paths guard I did not run.
- **`git` use:** `rev-parse HEAD`, `show <rev>:<path>`, `diff <sha> <sha> -- <paths>` and `diff --stat`
  only. No `status`, no diff against a working tree, no `add`/`commit`/`checkout`/`push`, in any
  repository.
- I wrote nothing outside `C:/tmp/OPUS_QUEUE_20260916/DD06/opus/` except scratch under
  `C:/tmp/OPUS_DD06_SCRATCH/A6/` (my own subdirectory; earlier attempts' files left untouched).

---

## 8. Reproduction

```
git -c safe.directory=* -C C:/tmp/P029_DD06_20260915 rev-parse HEAD          # a46da0aa…
git -c safe.directory=* -C C:/tmp/P029_DD06_20260915 diff --stat acd79b52 a46da0aa
cd C:/tmp/P029_DD06_20260915 && C:/tmp/P012_FUNDING_PY312_20260911/Scripts/python.exe -m pytest \
  IBKR_PAPER_BRIDGE/tests/test_dd06_agent_withdraw_probe.py -q -p no:cacheprovider --basetemp C:/bt_opus_dd06
C:/tmp/P012_FUNDING_PY312_20260911/Scripts/python.exe C:/tmp/OPUS_DD06_SCRATCH/A6/run_mutants.py
C:/tmp/P012_FUNDING_PY312_20260911/Scripts/python.exe C:/tmp/OPUS_DD06_SCRATCH/A6/run_mutants2.py
cd C:/tmp/OPUS_DD06_SCRATCH/A6/base && …/python.exe -m pytest tests/test_a6_reviewer_probe.py \
  tests/test_a6_carried_nits.py -q -p no:cacheprovider --basetemp C:/bt_opus_dd06_a6 -s
```
Artifacts: `MUTANTS_A6.txt`, `MUTANTS_A6_PASS2.txt`, `out_*.txt`, `FULL_BRIDGE_SUITE_A6.txt`,
`tool_acd79b52.py` / `test_acd79b52.py` (from `git show`), all under `C:/tmp/OPUS_DD06_SCRATCH/A6/`.

---

## 9. Summary

The round-4 repair is **sound and minimal**. `classify_response`'s third outcome is now handled exactly
where the fourth read said it must be: a fund-moving arm whose response the probe cannot classify is
measured on both wallets, labelled `DD06_INCONCLUSIVE_FUND_ARM_UNCLASSIFIED` with the channel named and
"the signed request may have executed" stated, and the sequence stops with the later arms marked
`SKIPPED_AFTER_UNCLASSIFIED`. All three authorized mutants (a)–(c) are killed by the shipped tests, check
(d) holds on both halves, and `_paid`, `_attribute`, the gates and the `offline` fixture are byte-identical
to `acd79b52` — round 3's repair is untouched and still fenced under my own mutants. Arm order B is
applied, pinned for the default configuration, and verified by me for the full one; it makes the
"funds cannot leave silently" property strictly stronger, and it closes N-9.

I found no REQUIRED defect. What is left is a long NIT tail, most of it pre-existing and most of it in the
safe direction; the two I would fix first are **N-26/N-19** (every abort path discards the whole record,
including after a fund arm that was not refused) and **N-16/N-20** (the amount table is unpinned and a
zero threshold makes an unchanged wallet "pay"). Two items outside the candidate need the owner's hand
before the next execution: the step packet and the runner still carry the pre-order-B arm list and set no
`DD06_PROBE_RUN_TOKEN`, so the run as documented would exit 3 (**N-22**); and the round-4 evidence is not
filed where the brief cites it (**N-25**).

VERDICT: PASS-WITH-NITS
