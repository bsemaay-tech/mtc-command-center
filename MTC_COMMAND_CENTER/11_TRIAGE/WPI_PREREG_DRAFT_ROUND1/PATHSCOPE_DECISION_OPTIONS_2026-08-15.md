# Pathscope — the decision Barış has to make — 2026-08-15

This document exercises no option. It states the situation, the four honest
choices, and the Lead's recommendation, so one owner sentence can unblock the
lane.

Read with `PATHSCOPE_OWNER_BOUNDARY_2026-08-15.md`.

## Plain-language situation

Pathscope is a static checker. It reads shell scripts and tries to prove that
nothing in them can load a file from outside an approved list of paths. It never
runs the scripts and never touches the VPS. Its job is to let the later WP-I
host run start from a proven-safe script set.

Four times now the same thing has happened: an auditor finds a way for a
dangerous path to slip through unnoticed, the checker is repaired, the repair
demonstrably closes exactly the reported cases — and the next fresh auditor
finds another way through, one step further out in the same shell grammar.

Today's retry is the cleanest evidence yet, because it is the first audit of
these bytes that actually executed. Everything it was asked to re-check
reproduced. It then swept the parts of the grammar nobody had named, and found
three more holes.

## Why it keeps happening

The three findings are one design fault wearing three hats.

The checker is built to **recognise dangerous shapes**. Every repair teaches it
one more shape. But shell assignment syntax is large, and anything it does not
recognise falls through silently and is reported as `PASS`. Silence means safe.

The alternative design is to **account for every member**. Split the value into
its members, and require each one to end in exactly one recorded disposition —
allowed, forbidden, or explicitly unresolved. Anything with no disposition is a
failure of the checker, not a pass for the script. Silence means stop.

Under that rule, all three of today's findings are structurally impossible:
command text with no verdict has no disposition (F1), a member can only carry
the provenance of the substring that produced it (F2), and duplicates cannot
collapse because each admitted member owns its own disposition slot (F3).

The repairs so far have all been the first kind. The audits keep proving the
first kind does not converge.

## The four options

### Option A — one more bounded repair, then one more audit

Fix F1, F2, F3 exactly as reported; re-audit with a fresh flagship.

- Cost: roughly 3-5 hours across repair, Lead verification, and one T1 audit.
- Honest odds: this is the fourth attempt at the same manoeuvre. The previous
  three each closed their named findings and each failed the next sweep. Nothing
  about this round is structurally different.
- Choose it if you want the lane to keep moving on the smallest possible step
  and you accept a real chance of a fifth cycle.

### Option B — accept with disclosure, and take Pathscope off the critical path

Declare Pathscope a **supplemental** static aid rather than a freeze gate.
Record the three findings and the design residual as accepted known limits, and
let WP-I Stage-1 proceed on the safety controls that are already accepted (RP7
rows 1-9, RP6, transport, SEC102).

- Cost: roughly 1-2 hours of documentation, no further audit.
- What you are accepting: the freeze no longer carries a proof that host scripts
  cannot load an out-of-allowlist path. The other accepted controls do not
  replace that specific proof — they cover different surfaces.
- Choose it if the unblocking matters more than that specific proof, and you are
  willing to have it written down that the proof is absent.

### Option C — redesign the accounting layer once (Lead recommendation)

Keep the parser. Replace the "recognise dangerous shapes" reporting layer with
the conservation rule above: every admitted member must reach exactly one
terminal disposition, and any member without one fails the run closed.

- Cost: realistically 6-10 hours — a design note, the implementation, Lead
  execution of the full fixture set, and one fresh flagship audit. Longer than
  Option A.
- What it buys: it retires the entire class of finding, rather than the three
  instances of it. It also makes future audits cheap, because the invariant is a
  single checkable property instead of a growing list of shapes.
- It is a rewrite of one layer, not of the prover, and the existing fixtures and
  harness stay valid as regression evidence.

### Option D — drop Pathscope from WP-I

Remove the checker from the WP-I scope entirely, record the gap in the
unresolved-risk register, and re-scope Stage 1 without it.

- Cost: roughly 2-3 hours of re-scoping documentation.
- Choose it only if you conclude the checker is not worth its cost at all. This
  is a stronger statement than Option B and harder to walk back.

## Lead recommendation

**Option C.** Three cycles of evidence say the current design does not converge,
and Option A is that same design a fourth time. Option C costs more hours in one
block but is the only choice that ends the cycle rather than extending it.

If the schedule cannot absorb 6-10 hours right now, **Option B** is the honest
fallback — it is strictly better than Option A, because it does not spend hours
buying a result the evidence says probably will not hold.

## What one sentence from you unblocks

Any one of:

> Option A: I authorize one bounded Pathscope repair limited to F1, F2 and F3,
> plus one fresh `gpt-5.6-sol` high execution audit.

> Option B: I accept Pathscope with disclosure as a supplemental aid; it is not
> a freeze gate; record the residual and proceed.

> Option C: I authorize the Pathscope accounting-layer redesign, followed by one
> fresh flagship execution audit.

> Option D: Drop Pathscope from WP-I and record the gap.

Until one of those is given, the lane stays stopped and Stage-1 freeze, Audit 2,
and WP-A stay blocked behind it.

No option in this document grants host, deployment, credential, service,
broker/exchange, ARM, order, TESTNET/mainnet, Pine, parity, MTC, trading, or
economic authority. Those remain separate gates whatever is chosen.
