# T0 exact-Opus review (round 3) — WP-P0-29 DD-06 testnet falsification probe, candidate `2128352b`

Reviewer: exact `claude-opus-5`, xhigh effort — the THIRD exact-Opus read of this candidate
(T0 repair round 2 of 3). Brief: `C:/tmp/OPUS_QUEUE_20260916/DD06/REVIEW_BRIEF.md`, executing the
ADDENDUM of 2026-09-17 22:0x. Launch instruction: `C:/tmp/OPUS_QUEUE_20260916/DD06/opus/BRIEF.md`.

---

## 0. Safety-rule compliance and incident disclosure

**No incident. No network call of any kind was made by me.**

The lane safety rule (addendum of 2026-09-17 21:5x) was observed literally:

- Every mutation was applied to a **scratch copy** at `C:/tmp/OPUS_DD06_SCRATCH/mutroot3/`. The subject
  worktree was never written to; I verified after all work that both source blob OIDs are unchanged
  (§1). The only worktree side effect is CPython bytecode caches
  (`IBKR_PAPER_BRIDGE/{tools,tests}/__pycache__`), created by the very pytest command the brief
  prescribes. No source byte moved.
- I never ran `main()` or `run_probe` against real SDK objects, never set `HL_*` or
  `DD06_PROBE_RUN_TOKEN`, and never removed or bypassed the `offline` fixture.
- Every mutant run's complete output was scanned for network signs
  (`ConnectionError|Max retries|urllib3|ReadTimeout|getaddrinfo|hyperliquid-testnet|requests.exceptions|NewConnectionError`).
  Two runs matched on `hyperliquid-testnet`; **I opened both and confirmed neither is a dial**:
  - `M-Q` (the `refuse_master_key` call removed from `main`): the match is pytest printing the
    **tripwire's own arguments** — `self = <_NeverDial object>`, `args = ('https://api.hyperliquid-testnet.xyz',)`.
    The URL reached `_NeverDial.__call__`, which raised instead of constructing an `Info`. This is the
    tripwire working exactly as designed, and it is the strongest single piece of evidence in this review.
  - `M-K` (`TESTNET_URL` → mainnet): the match is the assertion source line of
    `test_plan_names_the_testnet_host_and_the_gates` (`tests:522`).
- Two reviewer probe files were written **into the scratch tree only**
  (`mutroot3/tests/test_reviewer_probes3.py`, `mutroot3/tests/test_reviewer_partial3.py`). They are not
  part of the candidate and are not proposed for it.

---

## 1. Verified identities

| Item | Value |
|---|---|
| **COMPUTED HEAD** (`git -c safe.directory=* -C C:/tmp/P029_DD06_20260915 rev-parse HEAD`) | `2128352b348902a8b4755d2566e133c55094af8b` ✅ matches the pin |
| sha256 `IBKR_PAPER_BRIDGE/tools/dd06_agent_withdraw_probe.py` | `8C62DD1B8396CE47737D87BA2679396146DB09C5DA3F5576A0A6EA9C585FC191` |
| sha256 `IBKR_PAPER_BRIDGE/tests/test_dd06_agent_withdraw_probe.py` | `B1813E453DDDAF3D9151EDD0F9CD221C82651B8154279F533ABC68E53492B934` |
| git blob OID, tool — committed / on disk | `c4f55256038ee8aac0e1c82d43dae3c3c3b6ce4d` / `c4f55256038ee8aac0e1c82d43dae3c3c3b6ce4d` ✅ identical |
| git blob OID, test — committed / on disk | `2291d5aa437c4f0fd06b4bd7f59b8afc95a7a4ad` / `2291d5aa437c4f0fd06b4bd7f59b8afc95a7a4ad` ✅ identical |
| Scope, `git diff --name-status fcac0ac6 2128352b` | `A` on exactly those two paths, nothing else ✅ |
| Round-2 delta, `git diff --numstat a46b2a9d 2128352b` | `121/28` test + `141/54` tool = **+262 / −82**, matching the addendum's claim ✅ |

The blob-OID comparison is the point that matters: the bytes I read, tested and mutated are the bytes
that are committed at the pinned HEAD, not a dirty working tree.

Git commands used, and only these: `rev-parse`, `show`, `hash-object`, `diff <sha> <sha>`.
No `status`, no diff against the working tree, no `add`/`commit`/`checkout`/`push`.

---

## 2. Baseline suite (re-run by me, twice)

```
cwd: C:\tmp\P029_DD06_20260915
C:/tmp/P012_FUNDING_PY312_20260911/Scripts/python.exe -m pytest \
  IBKR_PAPER_BRIDGE/tests/test_dd06_agent_withdraw_probe.py -q -p no:cacheprovider --basetemp C:/bt_opus_dd06
............................                                             [100%]
28 passed in 0.56s
EXIT=0
```

28 passed (25 → 28 as claimed). The Lead's evidence bytes agree:
`REPAIR_R2_20260917/LEAD_PYTEST_GREEN_R2.txt` ends `28 passed in 0.53s / exit=0`;
`LEAD_FULL_BRIDGE_SUITE_R2.txt` ends `1626 passed, 1 skipped, 1 warning in 172.97s / exit=0`;
`LEAD_GUARD_R2.txt` ends `[protected] none … RESULT: PASS` naming exactly the two files.
I read those tails as bytes; I did not re-derive the full-suite number (see NOT VERIFIED).

My scratch harness reproduces the suite faithfully: `28 passed`, and the imported module resolves to
`C:\tmp\OPUS_DD06_SCRATCH\mutroot3\tools\dd06_agent_withdraw_probe.py` — the scratch copy, not the
worktree. `PYTHONPATH` is empty on this host, so there is no cross-contamination path.

---

## 3. The brief's six items

| # | Item | Verdict | Evidence (file:line) |
|---|---|---|---|
| 1 | **No mainnet path, no key leak** | ✅ each guard fenced except the disclosed gesture | `TESTNET_URL` `tools:63` (M-K kills); `refuse_unless_testnet` `tools:249-257` (M-I kills); `refuse_without_run_token` `tools:260-269`, called at `tools:789` (M-H kills, **on the resolver tripwire**); `refuse_master_key` `tools:272-277`, called at `tools:799` (M-Q kills, **on the `Info` tripwire**); `del api_key` `tools:798` (**M-L survives — disclosed by the Lead as a gesture, not a control**); redaction `tools:88-89, 96-108`; `write_record` hex guards `tools:731-736` (M-P kills) |
| 2 | **Funds cannot leave silently** | ✅ | `STOP_ON_NOT_REFUSED` `tools:86` (M-J kills, 6 failures); withdraw3 `6.0` USDC `tools:69` (M-M kills, 8 failures); destination is the account's own address `tools:575-579`; the packet's plain statement that a non-refused withdraw3 leaves the venue is in the module docstring `tools:16-19` and in `plan_text` `tools:751` |
| 3 | **Classification honesty** | ✅ a VALIDATION refusal can never become DD-06 evidence | `classify_response` `tools:180-189`; `classify_exception` `tools:192-199`; `classify_refusal_text` `tools:234-246` with `"does not exist"` in VALIDATION `tools:228` and the signer sentence in AUTHORIZATION `tools:204` (M-D kills). The INCONCLUSIVE path is `tools:688-697`: `DD06_REFUSALS_OBSERVED` requires `authorization_refusals == len(arms)`, so one VALIDATION-class refusal forces `DD06_INCONCLUSIVE` |
| 4 | **Control arm** | ✅ the r1 rejection cannot recur | `control_order_size` `tools:280-288` via `round_hl_price` (`bridge/broker/hyperliquid.py:72-89`). **My sweep of 2 900 001 mids from 10 000.0 to 300 000.0 step 0.1: 0 tick violations, 0 non-integer prices above 5 significant figures, 0 prices above 90 % of mid.** `control_order_size(76974.0, 5) == (69270.0, 0.00016)` ✅ and the r1 price `69276.6` is unreachable. M-R (restore `round(mid*0.9, 1)`) kills `tests:147` |
| 5 | **Fixture tests vs reality** | ❌ **one gap makes the next run misreport — R-1** | see §5 and §6 |
| 6 | **Scope and suite** | ✅ | §1 and §2 |

---

## 4. My own mutants

**Harness.** `C:/tmp/OPUS_DD06_SCRATCH/mutroot3/` — `bridge/` copied from the worktree,
`tools/dd06_agent_withdraw_probe.py` = the mutation target, `tests/` = a verbatim copy of the shipped
test. Driver `C:/tmp/OPUS_DD06_SCRATCH/mutate3.py` applies one textual mutation, runs the suite,
restores the pristine bytes and **verifies the restore by sha256** (`8c62dd1b…c191` before and after
every run; the closing line of each driver session re-confirms `28 passed`). Anchors are CRLF-translated
because the worktree is checked out CRLF.

Command for every row below, `cwd = C:\tmp\OPUS_DD06_SCRATCH\mutroot3`:

```
C:/tmp/P012_FUNDING_PY312_20260911/Scripts/python.exe -m pytest \
  tests/test_dd06_agent_withdraw_probe.py -q -p no:cacheprovider --basetemp C:/bt_opus_dd06_mut3
```

| Mutant | What was removed / inverted | Result | Which test died | Tripwire | Network sign |
|---|---|---|---|---|---|
| **M-A** | addendum (a): `_paid` back to "changed" (`delta != 0`) | 3 failed | `…[r3-replay]`, `…[mark-to-market-tick]`, `test_paid_is_directional…` | — | none |
| **M-B** | addendum (b): `None` rendered as "did not pay" (`tools:388`) | 1 failed | `…[agent-pays-master-unreadable]` | — | none |
| **M-B2** | addendum (b), other half: `_paid` returns `False` instead of `None` (`tools:377`) | 2 failed | `…[agent-pays-master-unreadable]`, `test_paid_is_directional…` | — | none |
| **M-C** | addendum (c): the whole `ERROR` branch (`tools:665`) | 1 failed | `test_transport_error_is_inconclusive_not_a_refusal` | — | none |
| **M-C2** | `ERROR` branch keeps the stop, skips the **measurement** | 1 failed | same test | — | none |
| **M-O** | `ERROR` branch keeps the measurement, drops the **stop** (`tools:685-687`) | 1 failed | same test | — | none |
| **M-D** | addendum (d): `"does not exist"` back in `AUTHORIZATION_MARKERS` | 1 failed | `test_refusal_text_classes` | — | none |
| **M-E** | threshold → 0 (any decrease pays) | 6 failed | 4 attribution cases + 2 units | — | none |
| **M-F** | direction dropped (`abs(delta) >= threshold`) | 2 failed | `…[r3-replay]`, `test_paid_is_directional…` | — | none |
| **M-G** | attribution order: agent consulted before the master | 2 failed | `…[r3-replay]`, `…[agent-pays-master-unreadable]` | — | none |
| **M-H** | run-token gate call `tools:789` | 1 failed | `test_main_refuses_without_the_execution_token…` | ✅ `resolve_hyperliquid_credentials` | none |
| **M-I** | `HL_LIVE_ACK` refusal `tools:254-257` | 1 failed | `test_refuses_mainnet_and_live_ack` | **none reached** | none |
| **M-J** | `STOP_ON_NOT_REFUSED` → `False` | 6 failed | 5 attribution cases + the stop test | — | none |
| **M-K** | `TESTNET_URL` → mainnet | 1 failed | `test_plan_names_the_testnet_host_and_the_gates` | — | assertion source line only |
| **M-L** | `del api_key` `tools:798` | **28 passed — survivor** | — | — | none |
| **M-M** | withdraw3 `6.0` → `0.5` | 8 failed | broad | — | none |
| **M-N** | `ARM_AMOUNT_USDC` lookup `tools:426` → flat `TRANSFER_AMOUNT_USDC` | **28 passed — survivor** | — | — | none |
| **M-P** | `write_record` 64-hex guard `tools:731-732` | 1 failed | `test_write_record_refuses_surviving_hex` | — | none |
| **M-Q** | `refuse_master_key` call `tools:799` | 1 failed | `test_main_refuses_a_master_key…` | ✅ `Info` | tripwire args only |
| **M-R** | control price back to the r1 `round(mid*0.9, 1)` | 1 failed | `test_control_price_is_wire_valid_for_a_real_btc_mid` | — | none |

**20 mutants, 18 killed, 2 survivors.** One survivor (M-L) was disclosed in advance by the Lead;
the other (M-N) is new and is filed as N-16.

### 4a. Addendum check (a) — `_paid` back to "changed"

```
FAILED tests/…::test_not_refused_fund_arm_names_whose_funds_left[r3-replay]
FAILED tests/…::test_not_refused_fund_arm_names_whose_funds_left[mark-to-market-tick]
FAILED tests/…::test_paid_is_directional_amount_aware_and_unreadable_honest
3 failed, 25 passed
```
✅ The r3-replay case fails exactly as the addendum requires. The round-2 R-1 is genuinely closed for
the case that produced it: replaying the venue's own numbers (agent 14.0 → 13.0, master
983.987457 → 984.987457) now reads `DD06_FINDING_OWN_FUNDS_MOVED` and never prints "falsified".

### 4b. Addendum check (b) — `None` rendered as "did not pay"

Both halves are fenced: M-B (the rendering, `tools:388`) and M-B2 (the `_paid` return, `tools:377`) each
fail `…[agent-pays-master-unreadable]`. ✅
This check is the one that matters for R-1 below — it is fenced for the **all-or-nothing** case and
unfenced for the **partial** case.

### 4c. Addendum check (c) — the ERROR branch

Three independent mutants (M-C remove it, M-C2 keep the stop but drop the measurement, M-O keep the
measurement but drop the stop) each fail `test_transport_error_is_inconclusive_not_a_refusal`. ✅
The test pins all three properties: `DD06_INCONCLUSIVE_FUND_ARM_ERROR`, the `post_withdraw3_account_balances`
step, and `SKIPPED_AFTER_ERROR` on the later arms (`tests:330-352`).

### 4d. Addendum check (d) — `"does not exist"`

M-D fails `test_refusal_text_classes`, which pins both directions at `tests:294-303`. ✅

### 4e. Addendum check (d), second half — threshold arithmetic and the master INCREASE

Run as reviewer probes against the **unmodified** candidate
(`mutroot3/tests/test_reviewer_probes3.py`, `14 passed`):

- **Threshold arithmetic ✅.** `set(ARM_AMOUNT_USDC) == set(FUND_MOVING_ARMS)`, and for each arm the
  measured threshold is exactly half: withdraw3 `6.0 → 3.0`; usdSend, spotSend, subAccountTransfer,
  usdClassTransfer `1.0 → 0.5`. Verified behaviourally, by feeding `_paid` a decrease of exactly the
  threshold (True) and of 0.99 × the threshold (False) for each arm.
- **A master INCREASE can never produce the breach label ✅.** Swept increases of
  0.0/0.01/0.5/1.0/6.0/1000.0 against every arm amount: `_paid` is `False` in all cases. The exhaustive
  `_attribute` truth table over `(master_paid, own_paid, agent_read) ∈ {True,False,None}²×{True,False}`
  yields `DD06_FINDING_MASTER_FUNDS_MOVED` **only** when `master_paid is True`, and the word
  "unchanged" never appears in any of the 18 texts.

### 4f. Round-1 gates, re-verified by me

- **M-H** — the token gate removed: `test_main_refuses_without_the_execution_token_before_reading_any_credential`
  fails with `AssertionError: resolve_hyperliquid_credentials must never be reached from the fixture suite`.
  It fails **on the tripwire, not on a network error**. ✅
- **M-I** — the `HL_LIVE_ACK` refusal removed: only `test_refuses_mainnet_and_live_ack` fails
  (`DID NOT RAISE`), and **no test reached the resolver, either SDK constructor, or the network**.
  The line that stops `main` is **`tools:789` — `refuse_without_run_token(args.run_id, dict(os.environ))`**;
  the `offline` fixture clears `DD06_PROBE_RUN_TOKEN` (`tests:457-463`), and M-H proves that deleting
  exactly `:789` is what lets execution reach the resolver. Defence in depth confirmed: the single-line
  change that turned the suite into a live testnet run on 2026-09-17 no longer arms anything.

### 4g. Control-arm sweep (pure math, no venue)

`C:/tmp/OPUS_DD06_SCRATCH/sweep3.py`, 2 900 001 mids, 10 000.0 → 300 000.0 step 0.1, `szDecimals = 5`:

```
tick violations (more than 1 decimal):    0
>5 significant figures, NON-integer price: 0
>5 significant figures, INTEGER price:    17000      (first: mid 111120.0 -> 100008.0)
price above 90 % of mid (could fill):     0
worst notional: 10.499999999999998 at mid 10416.7    (venue floor $10.00; constant 10.5)
control_order_size(76974.0, 5) = (69270.0, 0.00016)
r1 bad price 69276.6 reproducible? False
```

Item 4 of the brief is satisfied: the r1 `Price must be divisible by tick size` rejection cannot recur
for any mid ≥ 10 000. The two residues are test-assertion nits, not venue risks → **N-10**, **N-5**.

---

## 5. Fixture tests vs reality — what the fixtures still do not carry

| Venue-shaped fact | Could it make the next run misreport? |
|---|---|
| **A balance endpoint that fails on one wallet but not the other, or on one of a wallet's two endpoints** | **Yes — this is R-1.** `_balances` (`tools:327-352`) calls two different endpoints, `user_state` and `spot_user_state`, and swallows a failure of either into `None`. The shipped fixture only ever fails **both at once** (`_agent_pays_master_unreadable`, `tests:595-598`). The partial failure — the realistic one — is untested and is read as a measurement |
| **Venue settlement latency on withdraw3** | Yes, in the safe direction. A bridge withdrawal that the venue accepts need not be reflected in the balance the probe reads milliseconds later, so a genuine breach would most likely be recorded as `DD06_FINDING_NOT_REFUSED` rather than `…MASTER_FUNDS_MOVED`. That label still stops the run, still exits 2, and its text says "read the venue response and the ledger before drawing any DD-06 conclusion" (`tools:407-411`), so no wrong decision is invited → **N-14** |
| **A funded perp position during the probe window** | Yes, above the threshold. `accountValue` is mark-to-market; a 0.60 USD drift with USDC untouched satisfies the 0.50 threshold of a 1 USDC arm and prints "DD-06 falsified on testnet". Demonstrated (`test_DEMO_B`). Not reachable on the account this probe runs against, whose perp value is structurally 0.0 → **N-13** |
| **`--include-usd-class-transfer`** | Only if the owner passes the flag — but then an entirely unexercised arm meets the venue, which is the r1 failure shape. `usd_class_transfer` is still absent from `ExchangeLike` (`tools:119-136`) although `usdClassTransfer` is declared fund-moving (`tools:76`) and given an amount (`tools:84`) → **N-7** |
| **A filled control order** | `_resting_oid` (`tools:701-707`) matches any `"oid": N`, a `filled` status included; the run then reports "rests on the book … cancel it by hand" — the wrong remedy for an open position. Demonstrated (`test_DEMO_C`) → **N-3** |
| **withdraw3 against a funded perp balance** | Still never exercised. r3's withdraw3 died on the agent's 0 perp balance with the opaque `Error withdrawing from bridge`. The probe's central question is still open on its most important arm — a fact about the *package*, not a defect in this candidate |
| **An `ERROR` on a non-fund-moving arm** | The run ends `DD06_INCONCLUSIVE` with `finding: null` (`tools:688-697`); the error is in the steps but nothing points at it. Demonstrated (`test_DEMO_E`) → **N-15** |
| **Rate-limit / 429 `ClientError`** | REFUSED + UNCLASSIFIED → INCONCLUSIVE. Safe direction |
| **Mainnet parity** | Correctly not claimed anywhere, by the candidate or by me |

---

## 6. Findings

### REQUIRED

#### R-1 — a partially unreadable wallet is reported as a measured "did not pay", and the non-breach exclusion is printed from it

**Where.** `_paid` `tools:355-377` (the `readable` counter at `tools:374` and the
`return False if readable else None` at `tools:377`); `_attribute` `tools:380-412` (the readings at
`tools:393`, the own-funds text at `tools:400-406`).

**What happens.** `_balances` reads a wallet through **two different endpoints** and turns a failure of
either into `None` (`tools:331-336` for `user_state`, `tools:341-346` for `spot_user_state`). `_paid`
counts a key as `readable` whenever that one key parses on both sides. So a wallet counts as measured
as soon as **either** endpoint answers — and the verdict `False` is rendered by `_attribute` as the flat
words **"did not pay"**, with no unreadable marker anywhere in the sentence.

**Why that matters here specifically.** On the account this probe runs against, one of those two keys is
a decoy. The candidate's own comment says so:

> `# A unifiedAccount keeps its USDC in the spot balance (perp accountValue reads 0.0 — r1 on testnet);` — `tools:486`

Every dollar the master holds is in `usdc_total`; `accountValue` reads `0.0` before and after, always.
That permanently-readable `0.0` is enough to set `readable = 1`. Consequence: **for the master wallet on
this account, the `UNREADABLE` path the round-2 repair added can only fire if BOTH endpoints fail at
once.** A single transient failure of `spot_user_state` — the endpoint that carries the only balance
capable of paying — is reported as a measurement that it did not make.

**Demonstrated** (`C:/tmp/OPUS_DD06_SCRATCH/mutroot3/tests/test_reviewer_partial3.py`, run against the
**unmodified** candidate, fake venue objects only, `3 passed`):

```
RESULT : DD06_FINDING_OWN_FUNDS_MOVED
FINDING: spotSend was NOT refused and the AGENT wallet's own balance DECREASED while the account's
         readable balances did not: the agent moved its own funds (r3 shape; not the DD-06 breach)
         [account did not pay, agent wallet paid]
MASTER READINGS: {'before': {'accountValue': '0.0', 'usdc_total': '983.987457'},
                  'after':  {'accountValue': '0.0', 'usdc_total': None}}
```

The record says the account **did not pay**. The account's only funded balance was **never read**. The
third probe in that file shows the same output for a run in which the master really did pay 6 USDC — the
decrease is simply invisible.

**This is deliberate, not an oversight**, which is why it needs a decision rather than a patch: the
shipped unit test pins the partial case at `tests:677-684` —

```python
assert paid({"accountValue": None, "usdc_total": "10.0"},
            {"accountValue": "5.0",  "usdc_total": "10.0"}, 1.0) is False
```

— under a test named `…_unreadable_honest`. The parametrized case that does exercise unreadability
(`tests:595-598`) blanks **both** endpoints, so the partial case has no coverage at all.

**Sub-case R-1(b): the exclusion survives even when the sentence does say UNREADABLE.** With the master
fully unreadable, the finding still reads
`… the agent moved its own funds (r3 shape; not the DD-06 breach) [account UNREADABLE, agent wallet paid]`
(`test_DEMO_A`, §4e file). `"not the DD-06 breach"` (`tools:403`) is an exclusion claim; it requires a
complete, readable master measurement, and in this branch there is none. The clause
`"while the account's readable balances did not"` (`tools:402-403`) is vacuously true when there are no
readable balances, and is being used to carry the conclusion.

**Why REQUIRED and not a NIT.** This is round-2's R-1(b) surviving in the case that matters. Round 2
asked that an unreadable side be named unreadable and never treated as measured; the repair implemented
that only for the all-or-nothing failure, and on this account the all-or-nothing failure is the one shape
that essentially cannot occur, because a structurally-zero decoy balance always votes "readable". The
error direction is the flattering one — the tool tells the owner the master did not pay, about money it
did not look at — and the sentence it prints is this package's deliverable.

**Remedy (small, local, failing inputs already written).** Two lines of intent:
1. `_paid` should distinguish *measured-and-unchanged* from *not measured*: treat a wallet as measured
   only when every key parsed on both sides (or, minimally, return `None` when any key was unreadable and
   no readable key decreased). `tests:677-684` then needs its expectation flipped from `False` to `None`.
2. `_attribute` must not print `"not the DD-06 breach"` — nor the OWN label as a conclusion — unless
   `master_paid is False` with a complete reading. When the master's status is `None`, the honest label
   is an inconclusive one (`DD06_FINDING_OWN_FUNDS_MOVED_MASTER_UNREADABLE`, or reuse
   `DD06_INCONCLUSIVE_…`), with the agent's decrease reported as a fact and no exclusion drawn.

### NIT

- **N-3** *(re-raised, unchanged, demonstrated)* `_resting_oid` (`tools:701-707`) regex-matches any
  `"oid": N`, a `filled` status included, so a filled control order yields
  `ABORTED_CONTROL_CANCEL_FAILED` with *"rests on the book … cancel it by hand"* — the wrong remedy for
  an open position (`test_DEMO_C`). Require the `resting` key.
- **N-4** *(re-raised, unchanged, demonstrated)* `_HEX40` (`tools:89`) requires the `0x` prefix, so a bare
  40-hex address passes both `redact` and the `write_record` guard and is written to the record
  (`test_DEMO_D`: `"leak": "a1a1…a1"`). `_HEX64` (`tools:88`) correctly makes the prefix optional.
  Addresses are public; hygiene only.
- **N-5** *(re-raised, re-measured)* the worst exact notional over my 2.9 M-mid sweep is
  `10.499999999999998` at mid 10 416.7 — 2e-15 below `CONTROL_MIN_NOTIONAL_USD`, which breaks the suite's
  own `>=` at `tests:158` for unsampled mids. No venue impact: the floor is $10 and the constant carries
  $0.50 of margin.
- **N-6** *(re-raised, reduced)* nothing binds execution to KVM2-P4-03 although packet §3 does; the run
  token is host-agnostic. The token gate narrows this a great deal but does not close it.
- **N-7** *(re-raised)* `--include-usd-class-transfer` still has no test, and `usd_class_transfer` is
  still absent from the `ExchangeLike` protocol (`tools:119-136`) although `usdClassTransfer` is in
  `FUND_MOVING_ARMS` (`tools:76`) and in `ARM_AMOUNT_USDC` (`tools:84`). The
  `# type: ignore[attr-defined]` also sits on `tools:627` rather than on the attribute access at
  `tools:625`.
- **N-8** *(partly fixed; residue)* `REVIEW_BRIEF.md:1` now says "ran three times on testnet" ✅, but
  `REVIEW_BRIEF.md:7` still reads "a corrected re-run r2 waits for the owner's word", and
  `REVIEW_BRIEF.md:6` still describes the two files as "16 tests". The Friday Sol lane reads that body.
- **N-9** *(the owner's call, re-raised unchanged)* arm order: `withdraw3`, the only arm that moves funds
  **off** the venue, still runs first (`tools:573-579`), ahead of the in-venue self-transfers whose
  non-refusal would trip the stop rule first. §3 of the packet is the owner-approved order, so this stays
  the owner's decision. r3 is evidence for reordering: spotSend was the arm that was not refused.
- **N-10** *(re-raised, re-measured)* `tests:154` asserts `len(digits) <= 5` as if it were an invariant of
  `control_order_size`. It is not: **17 000 of my 2 900 001 swept mids** produce an integer price above
  five significant figures (mid 111 120.0 → 100 008.0), wire-valid only under the venue's integer
  exemption — which `round_hl_price`'s own comment (`bridge/broker/hyperliquid.py:84-87`) declines to
  rely on for values ≥ 10 000, and which the early integral return at `:79-80` bypasses. The test passes
  only because it samples five mids.
- **N-13** *(new)* a mark-to-market drift larger than half the arm amount is still counted as a payment.
  Threshold for the 1 USDC arms is 0.50 USD; `test_DEMO_B` shows a 0.60 `accountValue` drift with USDC
  untouched printing "DD-06 falsified on testnet". **Not reachable on the account this probe runs
  against** (perp value structurally 0.0, and the control bid cannot fill at 90 % of mid), which is why
  it is a NIT — it becomes REQUIRED the day the probe is pointed at an account holding a position.
  Remedy shares R-1's: prefer the spot USDC reading, or require the decrease in a balance that can
  actually be spent.
- **N-14** *(new)* the attribution takes a single snapshot immediately after the arm, with no allowance
  for venue settlement latency; a genuine withdraw3 breach would most likely be recorded as
  `DD06_FINDING_NOT_REFUSED`. Safe direction — that label still stops the run and its text
  (`tools:407-411`) forbids drawing a conclusion — but the record would understate a real breach. Worth
  one sentence in the record, or a second re-read after a short wait.
- **N-15** *(new)* in the `ERROR` branch the finding embeds `_attribute`'s sentence verbatim, so the
  record of an errored arm reads `… withdraw3 was NOT refused; no readable balance decreased …`
  (`test_DEMO_F`), which is not what happened. Also, an `ERROR` on a **non**-fund-moving arm
  (`approveAgent`) leaves `result = DD06_INCONCLUSIVE` with `finding = None` (`test_DEMO_E`).
- **N-16** *(new)* the per-arm amount table is the one part of the round-2 repair that no test pins.
  **M-N** replaces the lookup at `tools:426` with a flat `TRANSFER_AMOUNT_USDC` and the suite still
  reports `28 passed` — i.e. nothing asserts that withdraw3 is measured against 6 USDC rather than 1.
  The values are correct today (§4e), so this is coverage, not behaviour; both producers are
  `ARM_AMOUNT_USDC` (`tools:79-85`) and the lookup (`tools:426`), and the failing input is M-N itself.
- **N-12** *(closed)* `opus/BRIEF.md` now pins `2128352b` ✅.
- **N-11** *(closed)* `test_dry_run_needs_no_credentials_and_no_network` now takes the `offline` fixture
  (`tests:424`) ✅.

---

## 7. NOT VERIFIED

- **I did not run the probe.** No credential was read, no SDK object was constructed outside a tripwired
  fixture, no venue was contacted, no `HL_*` or `DD06_PROBE_RUN_TOKEN` was ever set. Everything above
  comes from the committed bytes, the fixture suite, offline replays with fake venue objects, and
  pure-math sweeps.
- **I did not re-run the full Bridge suite.** `1626 passed, 1 skipped` is the Lead's evidence
  (`REPAIR_R2_20260917/LEAD_FULL_BRIDGE_SUITE_R2.txt`), read as bytes, not re-derived. Reason, under the
  lane safety rule: this workstation's user registry holds a live agent-wallet credential and
  `resolve_hyperliquid_credentials` falls back to it, so launching ~1 600 tests I have not individually
  audited is a venue-reachability risk I declined. The structural argument is cheap to accept: the diff
  **adds** two files and modifies none, so the only way it could disturb the existing suite is an import
  side effect at collection, and the tool's module level does nothing but import
  `bridge.broker.hyperliquid`.
- **Ruff was not re-run** — `No module named ruff` in the Bridge interpreter. The Lead's "7 findings, all
  pre-existing" was not re-derived.
- **Venue-side truth of r1/r2/r3** is taken from the recorded console/record files in CT13. I did not
  re-query the venue.
- **R-1's live consequence** is demonstrated by driving the shipped code offline with fake venue objects.
  I did not observe the wrong sentence printed by a real run, because I ran no run.
- **The venue's integer-price exemption** (N-10) is taken from `round_hl_price`'s own comment and the r1
  rejection text; I did not confirm it against Hyperliquid documentation or the venue.
- **Mainnet behaviour** is neither probed nor claimed.

---

## 8. Reading

The round-2 repair does what the round-2 read asked for, and I could not break it. Twenty mutants;
eighteen died on exactly the fence intended. The two execution gates are independently load-bearing —
removing either one leaves the other standing, and removing the token gate fails on the resolver
tripwire rather than on a network error, which on this host is the difference between a red test and a
live testnet dial. The r3 replay now reads OWN and never says "falsified". The errored fund arm is
measured and stops the sequence, fenced three separate ways. The threshold arithmetic is right, a master
increase can never produce the breach label, and the control price cannot reproduce the r1 tick
rejection anywhere in 2.9 million mids. Scope is two files and the focused suite is green at 28 under my
own hand.

It fails on the fifth thing the brief asked me to check, and it fails there for the second time in the
same place. The round-2 remedy — *an unreadable side must be named unreadable, never treated as
measured* — was implemented for the case where both of a wallet's balance endpoints fail at once. On the
account this probe actually runs against, that case is close to unreachable, because the perp
`accountValue` the tool's own comment calls structurally zero is always readable and always votes
"measured". One transient failure of the spot endpoint — the one endpoint that reads the only money the
master has — and the record states that the account "did not pay", with no marker of any kind, while
printing "not the DD-06 breach". The safeguard was added; it cannot fire where it was needed.

I want to be plain about the consequence, because it is the owner's to weigh: this is the third
REQUEST_CHANGES under a T0 cap of three, and it ends the Lead's repair authority on this candidate. It is
not a verdict on a broken tool. Everything else in `2128352b` is verified good, the defect is one
function's readability accounting plus one sentence's claim, and the failing inputs are already written
in `C:/tmp/OPUS_DD06_SCRATCH/mutroot3/tests/test_reviewer_partial3.py`. If the owner prefers to accept
the candidate and carry R-1 as a known limitation, the cheapest sufficient mitigation is a one-line rule
in the step packet: **do not accept an attribution whose `post_*_balances` step contains a `null` on
either side — re-read by hand before recording any conclusion.** That converts the defect into an
operator check the owner is already performing.

VERDICT: REQUEST_CHANGES
