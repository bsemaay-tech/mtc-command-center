# LEAD_ADJUDICATION — lane 7 (optional): exact `claude-opus-5` xhigh T0 read of the DD-06 testnet probe `1af85067` — 2026-09-17 19:0x-22:1x UTC+3

**Lane:** `OPUS_QUEUE_20260916/DD06/opus/run.ps1`, Claude PRO profile, launched by hand 18:5x UTC+3 after lane 6; 18:47-19:04 (15:47:15-16:04:11Z), launcher exit 0, 81 turns, no 429; report `ATTEMPT1_REQUEST_CHANGES_1af85067/OPUS_T0_REPORT.md`, 229 lines.
**Verdict as returned:** `VERDICT: REQUEST_CHANGES` — **4 REQUIRED** (R-1 four unfenced safety guards; R-2 the suite's offline-ness rests on one refusal, the real `main()` is exercised with nothing stubbed; R-3 `"does not exist"` as AUTHORIZATION evidence; R-4 the `NOT_REFUSED` finding text unsupported by any agent-balance read) + 9 NITs + **§0 INCIDENT DISCLOSURE**: the reviewer's mutant M8 caused one live TESTNET run (control order placed and cancelled; fund arms refused; `DD06_INCONCLUSIVE`; testnet only; nothing moved). Also sound per the reviewer: redaction + write-once real and pinned, the stop rule real, the refusal-class gate honest, the control-arm arithmetic correct across 1.14 M mids, scope exactly two files.

## Lead handling
1. **Incident** (`INCIDENT_20260917_LANE7_DD06/INCIDENT_20260917_LANE7_DD06_UNINTENDED_TESTNET_RUN.md`): public testnet reads at 19:05 — `openOrders []`, perp 0.0 / no positions, spot USDC 984.987457 unchanged, no fills since 15:00Z, same two agents → venue clean; no key material in the reviewer's stream/report (scanned); disclosed to the owner in chat 19:0x with the damage assessment and the recommendation about the process-readable registry credential; rule breach stated plainly (a testnet action without an owner word, through a lane the Lead launched with a mutant brief on a credential-holding host).
2. **Citations** (`:47`, `:55`, `:59`, `:168`, `:196-206`, `:214-217`, `:245`, `:283-333`, `:388`, `:434-441`, `:459-465`, `:479-485`, `:509-514`, `:550`, `:571-572`; tests `:273-289`, `:407-412`): read against the `1af85067` bytes while building the repair — all EXACT.
3. **Repair round 1 as the disclosed builder → `a46b2a9d`** (`DD06_TESTNET_PROBE_20260915/REPAIR_R1_20260917/LEAD_VERIFICATION_DD06_R1.md`): second execution gate + offline fixture suite (R-2), the four fences (R-1), marker narrowing (R-3), whose-funds-moved attribution (R-4), N-1/N-2; eight mutants RED (the two removed-gate mutants hit tripwires, no dial); GREEN 25; full Bridge 1623; Gemini `DD06_R1_GEMINI` PASS-WITH-NITS (R-1..R-4 CLOSED; `suite_can_dial_after_two_gates_removed: false`).
4. **Lane rule** (binding, in the DD06 brief addendum, the queue file, the Sol README, the memory): no lane mutates a venue-facing tool's refusals and runs `main()`/real-SDK tests against the mutant on this workstation; scratch copies and fixture suites only.

## NITs — disposition
| # | Finding | Disposition |
|---|---|---|
| N-1 | `FUND_MOVING_ARMS` unused | **fixed** (`a46b2a9d`: used for the balance attribution; `usdClassTransfer` added) |
| N-2 | `BaseException` swallows the operator's abort | **fixed** (re-raised) |
| N-3 | `_resting_oid` matches a filled status → wrong remedy text | carried (require the `resting` key) |
| N-4 | `_HEX40` requires the `0x` prefix | carried (hygiene) |
| N-5 | min-notional float edge | carried (`* 1.01` margin) |
| N-6 | nothing binds execution to KVM2 | **closed by the token gate** (an owner-worded run sets the token where it runs) |
| N-7 | `--include-usd-class-transfer` untested / not in the protocol | carried |
| N-8 | brief said "ran once" (three runs) | **fixed in the lane addendum** |
| N-9 | arm order (withdraw3 first) | **owner one-liner `DD06-ORDER A|B`** (rec. B: in-venue self-transfers first) |
| Gemini NIT | duplicate assertion in `test_refusal_text_classes` | carried (remove with the next slice) |

## Standing
Lane 7 re-pinned to `a46b2a9d`; attempt 1 archived; the second exact-Opus read under the safety rule when the Pro window allows; Sol (Sat) reads the pin that stands. DD-06 itself: the register row stays AMENDED-BY-OWNER-AUTHORITY on the r3 evidence (`LEAD_PUBLIC_READS_after_r3.txt`, which the reviewer verified supports the Lead's conclusion); no probe record closes DD-06 on its own until the R-4 attribution has run on the venue (owner-worded run only). The Lead accepts nothing.

Recorded by Claude Opus 5 Lead (session 6, `4a8233`).
