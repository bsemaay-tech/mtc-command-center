# A missing artifact the plan never defined — 2026-08-16

Recorded separately because it was found inside a third-draft procedure document
and would otherwise be lost there. This is a gap in the programme, not in the
document that found it.

## What is missing

Nothing in this project publishes the **identity of the artifact WP-A actually
tested**, independently of whoever later performs the freeze.

The freeze procedures needed that identity to prove continuity: the artifact
being frozen must be the same one WP-A validated. Three drafts tried to satisfy
that requirement and all three failed the same way, because there is no
independent thing to compare against. The final freeze therefore compared the
artifact to a byte count and SHA-256 **supplied by the freezer**, which matches by
construction and proves nothing.

`FREEZE_PROCEDURES_V3_2026-08-16.md` takes the honest option rather than
attempting a fourth variation, marking F5:

> `CANNOT BE CLOSED UNTIL WP_A_TESTED_ARTIFACT_AUTHORITY_V1 EXISTS`

The programme plan requires WP-A and requires captured evidence, but never names a
machine-readable producer or an immutable identity publication for what WP-A
tested.

## Why it went unnoticed

Because the natural way to write the check hides it. "Compare the artifact against
its expected identity" reads as rigorous, and the question *where does the expected
identity come from* is one document away. This is the pattern in
`SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md`, and this instance survived three
drafts precisely because each draft rearranged the comparison instead of asking
where its input came from.

## What the missing artifact must be

Whatever creates it, it has to satisfy four properties, or the check is decorative
again:

1. **Produced by WP-A, not by the freezer.** If the later party can influence it,
   there is no check.
2. **Create-once and immutable** after WP-A closes, with its own recorded identity.
3. **Machine-readable, with a unique-row selector** — and explicit rejection of
   both zero matching rows and multiple matching rows. A lookup that silently picks
   the first match reintroduces the defect.
4. **Independently verifiable**: an auditor who was not present must be able to
   recompute the published identity from the artifact.

## Consequences

- The final-freeze continuity check cannot be honestly closed until this exists.
  Any freeze performed before then carries an unproved continuity claim, and that
  should be disclosed rather than papered over.
- It must be defined **before WP-A runs**, not after. WP-A is the only party that
  can publish what it tested; once WP-A closes without producing it, the identity
  is unrecoverable except by trusting someone's later recollection.
- This is cheap now and expensive later. Defining a small publication contract
  today costs little; discovering at freeze time that nothing published the
  identity means either re-running WP-A or accepting a disclosed gap in the chain.

## Status

Not a decision for the owner yet — it is a design task with a clear shape. It
belongs in the work catalogue as its own row, before WP-A, and it should be named
in the WP-I closure template so WP-A cannot close without it.

No host, deployment, credential, service, broker/exchange, ARM, order,
TESTNET/mainnet, Pine, parity, MTC, trading, or economic action relates to this
record.
