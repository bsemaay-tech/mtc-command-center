# Wiring the validator into the gate is not free — and I told the owner it was

**Author:** Lead (claude-opus-5) · **Date:** 2026-09-10 · **Status:** built, measured, **not landed**
**Authorises the change:** `HIST-2026-0030` (task `WP-P012-VALIDATOR-REPORT-ONLY`)
**Blocks the change:** the Section-16 receipt certifies the harness bytes

---

## What I told the owner when he chose this

Presenting "report-only first" as the safe option, I wrote:

> The gate runs it and records every refusal in the receipt, but does not refuse the build. You get
> the full list in writing each run, **with no risk of blocking work**, and we see whether it stays
> quiet before giving it teeth.

**The last clause is false.** He chose the option on it.

## What actually happens

The wiring works exactly as specified. Built, tested, and measured:

| property | measured |
|---|---|
| `declared_field_validation` block in the receipt | present |
| `enforced` | `false` |
| validator refusals reaching `acceptance_blockers` | **0** |
| validator refusals reaching `claim_label` | **none** |
| contract self-tests | **494 passed, 0 failed** |
| what the validator reports on the real record | **5** — 4 `CHAIN_UNVERIFIABLE`, 1 owner-overruled nit |

**And the gate refuses anyway:**

```
claim_label: BOUNDED_NON_BLOCKED_CORRECTION_EVIDENCE_REFUSED
refusals:    SEMANTIC_COVERAGE_REVIEW_INVALID
             reviewed_identities.harness_sha256: does not match measured identity
acceptance_blockers: 0
```

Making the gate run the validator means **editing `verify_bceg.py`** — the harness. The Section-16
receipt certifies the harness by digest as one of its content identity keys
(`verify_bceg.py:66-74`, refusal at `:650-654`):

| | digest |
|---|---|
| receipt certifies | `53b4ff48973bdf6dda8485f4c34de43d320fdb07da43fc523eaa17366e2817cf` |
| harness now measures | `d3c01ace1abe2f37cd3d96a5d53a307d38cf3d60732c6fce64ee56e98c3e34d4` |

So report-only does not refuse **on validator findings** — that part is true and tested. But it cannot
be switched on at all without invalidating the review that acceptance depends on.

## The cost, measured

**Not a re-seal.** The harness is not one of the 19 sealed members, and the seal is unchanged at
`b6ac5a46…` through all of this.

| | measured |
|---|---|
| harness change | **71 insertions, 0 deletions, 1 file** |
| seal | unchanged, no re-seal #31 |
| what is needed | a **Section-16 delta review** re-certifying the harness digest |
| who may perform it | not the claude family (authored the tables) and not the codex family — the standing route is `gemini-3.8-flash-high` under OD-20260906-3 |

## This is the third time today, and it is one pattern

| I checked | I missed | 
|---|---|
| the seal (repair 6) | the record feeds self-tests **inside** the gate suite |
| `refused_missing_fields` semantics (Decision 1) | the standing `KEEP_REFUSED` ruling on the same fields, **which I had written down myself** |
| that report-only cannot refuse on findings | that switching it on edits a **certified** file |

Each time I verified the mechanism I was thinking about and missed the one beside it. The seal, the
blocker list, and the finding channel are three of the routes into a verdict; **the harness digest and
the self-test suite are two more.** A cost claim is only as good as the enumeration behind it, and
mine has now been incomplete three times in one day.

**What would have caught all three:** before claiming any change is free, list every artefact that
digests, certifies, or asserts against the thing being edited — and check each. For this repository
that list is at least: the 19 sealed members, the anchor sidecar, the Section-16 receipt's eight
content identity keys, and the contract self-test suite.

## Options, and what each costs

1. **Keep the validator standalone.** Revert these 71 lines. Costs nothing, changes no verdict — and
   returns the defect class to depending on someone remembering to run it, which is the option the
   owner explicitly rejected.
2. **Land it and commission the Section-16 delta review.** Honest and complete. Costs one review round
   over 71 added lines, through the route that has had quota and wrapper problems before.
3. **Land it on an owner overrule of the receipt mismatch.** Fastest. **The Lead advises against it:**
   whether acceptance recorded on an overrule satisfies the strict clause requiring "required
   independent reviews and Lead acceptance complete" is *already* an open question flagged under
   `HIST-2026-0026`, and this would add a second instance to it.

**Lead recommendation: option 2.** The change is 71 lines and mechanically trivial to review, the
owner has already said he wants the validator wired, and paying a small review now avoids compounding
the overrule question that final acceptance already has to answer.

**Nothing is landed.** The wiring is held on its own branch; the policy correction
(`HIST-2026-0032`) and repair 7 (`HIST-2026-0031`) are independent of it and proceed separately.
