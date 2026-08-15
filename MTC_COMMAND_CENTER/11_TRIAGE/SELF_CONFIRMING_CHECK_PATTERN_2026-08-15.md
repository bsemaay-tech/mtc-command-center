# The recurring defect this project keeps producing — 2026-08-15

Lead synthesis. Not a finding against any one document; a pattern across all of
them, written because naming it is cheaper than rediscovering it a fifth time.

## The pattern

Four independent reviews ran tonight against four unrelated documents, written by
different agents for different purposes. All four returned `NEEDS-REWORK`, and the
most serious finding in each is the **same defect wearing different clothes**:

> **A check that can pass without proving the thing it claims.**

The four instances:

| Document | The check | Why it can pass without proving anything |
|---|---|---|
| Pathscope Option C design | Conservation over admitted values | A value that is never *admitted* is never counted. `: ${LD_PRELOAD:=/etc/evil.so}` is exempted before admission, so conservation is satisfied while the danger is invisible. |
| Stage-1 allocation record | The collision check | It is real only over a declared universe nobody proved complete. It can pass by not looking. |
| Stage-1 allocation record | Append-only | Asserted, not enforced. Nothing detects or rejects an overwrite, so the property holds only while everyone behaves. |
| Freeze procedures (F5) | WP-A artifact continuity | Compares the artifact against byte count and hash values **the freezer supplies**. Set them to the current artifact and it matches — a self-consistency check presented as proof of continuity. |
| Freeze procedures (F4) | Unchanged-bits statement | Narrow enough that the overall guarantee can pass after bits changed. |
| Packet 10 suite contract | Environment reproducibility | "Linux CPython 3.12" and an integrity-checked install admit materially different runtimes. Two operators satisfy the contract and run different things. |

Add the one from earlier tonight, found by the T1 auditor rather than a review:
the implementer's own proof that the repaired assertion still had teeth
**reimplemented the comparison instead of invoking the test under audit**. It
demonstrated that the logic was sound, not that the test was discriminating.

## Why it keeps happening

Every one of these was written by someone competent, in good faith, trying to
produce a rigorous artifact. The defect is not carelessness. It is that **the
natural way to write a check is to compare a thing to what you believe about it**,
and belief is usually supplied by the same process that produced the thing.

The check then has no independent input, so it cannot fail for the reason it
exists. It fails only on typos.

This is also why the defect survives review so often: read casually, a
self-confirming check looks exactly like a real one. Both have a command, an
expected value, and a comparison. The difference is *where the expected value came
from*, and that is usually two documents away.

## The test to apply

Before accepting any check, procedure, assertion or invariant in this project, ask
one question:

> **What would have to be true for this check to fail?**

If the answer is "a typo", "an implementation bug", or "nothing I can construct",
the check is decorative. A real check has an input the checked party does not
control, and you can describe the concrete world in which it goes red.

Three follow-ups that catch most of the rest:

1. **Where does the expected value come from?** If the same process produced both
   the artifact and the expectation, there is no check.
2. **What is outside the universe?** Conservation, completeness and coverage
   properties are only as good as the set they quantify over. Ask what is exempted
   before the property applies.
3. **Is it enforced or asserted?** A property no mechanism defends is a comment.

## Where this already paid

The Pathscope design review applied question 2 and found the admission-boundary
hole before implementation, which saved the one repair cycle Barış authorized. The
T1 suite auditor applied question 1, refused the implementer's proof, and
constructed its own by wrapping the real function. Both cost under an hour and
both prevented a wasted round.

## Standing rule proposed

Every kickoff that asks for a check, an invariant or a proof carries this sentence:

> State what would make this check fail, and show it failing.

Every review of such an artifact carries:

> Try to satisfy this check while the property it claims is false.

Neither is expensive. Tonight's evidence is that both are load-bearing.

No host, deployment, credential, service, broker/exchange, ARM, order,
TESTNET/mainnet, Pine, parity, MTC, trading, or economic action relates to this
record.
