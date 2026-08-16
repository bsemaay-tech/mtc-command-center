# Privileged mutation-denial channel — load-bearing decision — 2026-08-16

Lead decision under the owner-approved accelerated full-completion contract
(`OWNER_DECISION_ACCELERATED_COMPLETION_2026-08-16.md`), which requires this
question to be decided before the channel design is audited or built.

## Decision

**NOT LOAD-BEARING under the approved contract. Do not audit it; do not build
it.** The design stays committed as reference. This is the outcome the midday
handoff's honest-judgement section anticipated ("probably over-engineered now
… do not audit or build it without asking Barış whether he wants that standard
here") — and the owner has now chosen the accelerated standard.

## What the channel was for

The statically linked C account-shell gate + Landlock rulesets + seccomp
filters + private mount namespace were designed to *enforce* a privileged
read-only observation channel on GATEA-STAGING that the capturing process
could not silently lift — addressing the self-confirming-check pattern
(`SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md`): one operator configuring,
using, and certifying the same control.

## Why it is not load-bearing now

1. **The finish line changed.** The approved contract's objective is the KVM2
   deployment of the accepted current release, DISARMED and masked, with
   operational verification. The channel serves staging *evidence purity*, not
   deployment. Nothing on the KVM2 critical path consumes its output.
2. **The risk it mitigates is bounded by disposability.** GATEA-STAGING is a
   local, disposable Hyper-V VM holding no secrets and no money path. The
   recorded authorization (`HOST_CHANNEL_AUTHORIZATION_2026-08-16.md`) already
   discloses that residual continuity rests on operator integrity plus
   disposability.
3. **A cheaper mechanism with the same independence property already exists
   and is in use:** the Hyper-V checkpoint (`GATEA-STAGING-CH1-PRECHANGE-V1`),
   which no in-VM process — including in-VM root — can reach or alter. It
   provides rollback and a comparison baseline outside the observed system.
4. **Contract clause 3** forbids building extra proof systems beyond the tier
   policy for non-load-bearing surfaces. Building a custom C/Landlock/seccomp
   stack for a disarmed paper bot on a disposable VM is exactly that.

## Residual-risk disclosure (honest, carried forward)

Without the enforced channel, any future GATEA-STAGING observation is made by
the single operator over an ordinary root-capable SSH channel. Consequences:

- Observation records from GATEA-STAGING are **operator-attested, not
  mechanism-enforced**. They may inform work but should not be presented as
  independently proven read-only captures.
- The one genuinely missing channel fact (a mutation-denial control) remains
  absent by choice, not oversight. If a future gate genuinely requires an
  enforced read-only capture, the committed design V1 is the starting point
  and this decision must be explicitly revisited with the owner.
- The Hyper-V checkpoint remains the strongest available integrity mechanism:
  take a fresh checkpoint before any mutating session, compare after, retain
  it as the rollback point.
- **The money gate is untouched:** broker credentials, key handling, ARM,
  orders, TESTNET/mainnet activation keep the full T0 standard everywhere.
  This decision lowers no bar on any live-money path.

## Owner-policy amendment (narrow)

Adopted under the accelerated contract's clause 3 authority; reversible by one
owner sentence:

> The privileged mutation-denial channel design
> (`STAGING_CHANNEL_DESIGN_V1`, committed 2026-08-16) is reclassified as
> reference material, off the critical path. GATEA-STAGING observations are
> operator-attested under the recorded host authorization, with the Hyper-V
> checkpoint as the integrity mechanism. No audit, build, or repair cycle is
> spent on the channel unless the owner explicitly re-orders that standard.
