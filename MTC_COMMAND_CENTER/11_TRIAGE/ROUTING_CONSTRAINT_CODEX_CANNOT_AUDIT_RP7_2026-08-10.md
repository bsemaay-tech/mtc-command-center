# ROUTING CONSTRAINT — the Codex flagship slot cannot complete an RP7 review

Date 2026-08-10, ~22:00. Recorded because it changes how the two-flagship T0 contract can
be satisfied for this artifact, and the next session must not rediscover it by burning two
more dispatches.

## What happened, twice

| Attempt | Scope | Tokens at death | Outcome |
|---|---|---:|---|
| RP7 round-5 full T0 review | rows 10–24 + five repairs + evidence contract | ~261k | killed by the provider content filter, no report written |
| RP7 round-5 **Part A** | five repairs + rows 10–19 only | ~275k | killed the same way, no report written |

Both ended with:

```text
ERROR: This content was flagged for possible cybersecurity risk.
```

## Why narrowing the prompt did not help

The handoff's documented workaround is neutral operational framing, and both dispatches used
it — "read-only environment preflight block", "confirm each branch reports honest results",
no attack/exploit/adversarial vocabulary. Part A additionally cut the scope roughly in half.

It still died, **later** in the run and at a higher token count. That is the signal: the
flagged material is not the prompt. It is the work product. A competent review of this block
necessarily constructs namespace, symlink, interpreter-replacement and capture-redirection
fixtures, and reasons about them in text. The last thing in the Part A transcript before the
kill was a symlink-escape probe (`/root/run -> /outside`, `OUTSIDE=no`) — a correct,
read-only, negative result, and exactly the kind of content that trips the classifier.

Narrower bands do not fix this. They just move the death later.

## What this means for the T0 contract

The two-flagship contract exists because the two families have different blind spots — the
venv-interpreter hole survived three Claude rounds and was found by Codex. Satisfying it
with **two Claude-family sessions is not equivalent** and must not be presented as if it
were. Claude Pro and Claude Max are the same model family; using Max to fill the Codex slot
would spend scarce emergency credit to buy a weaker guarantee. **That is why Max was not
used here**, even though the emergency policy's literal conditions were met
(acceptance-critical, Claude Pro exhausted, Codex unable to fill the slot).

## The routes that remain, in order of preference

1. **Codex on work that needs no constructed fixtures.** Delta verification, diff
   classification, grammar-table conformance, evidence-contract text checks. Dispatched
   tonight as `KICKOFF_CODEX_RP7_R5_DELTA_ONLY.md` — reading and diffing only, explicitly
   forbidden from building fixtures. If that completes, Codex still contributes real
   independent scrutiny to this artifact, just not behavioural falsification.
2. **Claude flagship for the behavioural half**, on its own slot, at full xhigh.
3. **A third family** for genuine independence on the behavioural half. None is currently
   available at flagship quality: GLM is a repair lane, Cline has no capacity, DeepSeek and
   NIM are not flagships. **This is the gap the owner should know about.**
4. Claude Max — only if an acceptance genuinely turns on it, and always recorded as a
   same-family second opinion rather than an independent flagship.

## Owner-facing summary

One of our two independent reviewers can no longer finish the job on this particular file.
Its provider stops it partway through, because doing the review properly means writing out
exactly the kind of probing that the provider's safety filter blocks. We tried a smaller
slice; it died later in the same way.

The other reviewer still works. But two reviews from the same family are worth less than one
from each — the biggest find of the whole project came from the disagreement between the two
families. If this file needs a genuinely independent second opinion, that is a gap worth
knowing about before freeze, not after.
