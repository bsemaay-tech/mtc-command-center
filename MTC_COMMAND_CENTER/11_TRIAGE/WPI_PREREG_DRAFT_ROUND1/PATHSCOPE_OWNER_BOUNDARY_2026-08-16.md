# Pathscope owner boundary — after Option C — 2026-08-16

Status: **REQUEST_CHANGES. The authorized Option C cycle is consumed. The lane is
stopped.** No further Pathscope repair or audit is authorized.

Subject: `codex/pathscope-accounting-redesign-20260815`, implementation `ec98cbd4`.
Verdict: `PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md`, fresh `claude-opus-5`,
cross-model against the Codex implementer, executed in isolated worktree
`C:\PSCAUD`.

## What Barış authorized and what happened

D1 authorized one accounting-layer redesign plus one fresh flagship execution
audit, with a required finding returning the lane to the owner boundary rather
than opening another round. All of that happened, in order, and the cycle is now
spent.

The redesign was designed, independently attacked before implementation (which
caught an admission-boundary hole and saved the cycle from an obvious failure),
amended against that review, implemented, and audited.

## What the redesign genuinely achieved

The audit is explicit that this was not a wasted round, and the Lead agrees:

- The original R5 defects are **dead**. Pool text dedupe, the single-empty
  Boolean, the RHS-wide source union, and the missing dispositions are gone — and
  the checks that would catch their return use **independent inputs**, which is
  the property that was missing everywhere before.
- **F1, F2 and F3 as filed are closed** and stay closed under the auditor's own
  re-measurement, not merely under the implementer's.
- All fifteen mutation arms reproduce: post-hoc corruption of the ledger faults
  every time.
- The regression contract is honest to the row — 109 cases, exactly two authorized
  rc changes, and the 60 declared byte-identical blocks are exactly the 60 that
  are identical.

## Why it still failed

Two REQUIRED findings, both of which the auditor reproduced with A/B output.

**REQUIRED-1 — the admission guard is bypassable inside its own route.**
`${LD_PRELOAD:=/etc/evil.so}` reaches `PASS rc=0` with zero coverage issues
through any data-role option operand on 33 of 92 registered specs plus the wrapper
specs, through a subscripted target on the exact carrier named in the design's own
falsification plan, and through `for`-lists, `case` subjects, heredoc bodies,
here-strings and test brackets. The composite passes them through. In one case a
reassuring `ALLOW-LEXICAL` row is attached. The design's closing claim that
unmodeled assignment-effect argv cannot silently cross the boundary is falsified.

**REQUIRED-2 — the independent cardinality check is not independent.**
`expected_counts` is `len()` of the very lists the member-emission loops iterate.
The design demanded an independent count and named the formula; neither was
implemented. Three splitter mutations each produce a false `PASS rc=0` with zero
accounting faults, one of them reinstating F1.

The auditor is honest about its own uncertainty on the second: it attacked
REQUIRED-2 hard and could not reach it from input alone, so a reasonable reader
could call it a documentation defect plus a defence-in-depth gap rather than a live
hole. It kept it REQUIRED because the design made it an explicit acceptance item
and the report claims it runs. That reasoning is sound and the Lead does not
overturn it.

## The fact that should drive the next decision

This is the **fifth** cycle in which the named findings were closed and the same
class was found one step further out.

Option C was chosen specifically to end that pattern by replacing shape-recognition
with conservation. It did not, and the audit explains why in one sentence:
conservation quantifies over **admitted** values, so an admission boundary with
open doors defeats it no matter how sound the accounting behind that boundary is.
The guard added for this was itself bypassable through ordinary shell constructs.

That is now strong evidence about the problem rather than about any one attempt.
The lexical surface of shell assignment is large, and each cycle has closed the
doors it knew about.

## What is not being decided here

No option is exercised. The Lead is not proposing a sixth cycle, and will not
start one. The options remain what they were, with one now much better informed:

- accept Pathscope with disclosure as a supplemental aid and take it off the
  critical path, recording precisely what is not proved;
- authorize a further bounded cycle against REQUIRED-1 and REQUIRED-2, knowing
  the base rate;
- drop it from WP-I and record the gap;
- or something new — for instance, restricting the prover's accepted input
  grammar so that anything outside a small provable subset is rejected outright
  rather than analysed, which trades usability for a boundary that can actually
  be closed.

The fourth is the Lead's instinct after five cycles, but it is a design proposal
requiring its own scoping, not a recommendation ready to be acted on tonight.

## Downstream

Unchanged: Stage-1 freeze, Audit 2 and WP-A remain blocked behind this lane and
behind the two decisions recorded elsewhere — the privileged staging channel and
the Step 8/10 dependency cycle. RP7 rows 1-9 remain accepted at `80cbed46` and are
unaffected.

No host, network, deployment, service, credential, broker/exchange, ARM, order,
TESTNET/mainnet, Pine, parity, MTC, trading, or economic action was authorized or
performed.
