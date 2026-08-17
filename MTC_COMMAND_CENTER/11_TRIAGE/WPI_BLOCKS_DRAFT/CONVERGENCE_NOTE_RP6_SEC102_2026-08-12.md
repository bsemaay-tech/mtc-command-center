# Convergence note — RP6 census & SEC102 command-word (owner visibility)

Date: 2026-08-12 ~00:25. Author: Lead (Fable overnight session). For the owner's morning review.

## What this is

Two verification TOOLS have each taken many adversarial rounds tonight, each round genuinely
closing a real evasion class but the cross-model auditor then finding one subtler class. Both
are QA/proof harnesses, NOT the economic blocks. **The economic blocks are sound and unchanged
throughout:** `RP6-P0.sh` is byte-identical since round 10a (`5132bacd…`); `RP7-WPI-RO.sh` is
Codex-accepted; the transport set is Codex-accepted.

## RP6 census (proves the block's result-grammar admits no smuggled emitter)

Rounds r10 → r15 (6 rounds tonight). Each closed a real class:
cmdquote/expand/continuation → alias/function-shadow/tool-shadow/prefix → function-def shapes,
empty/partial inventory → definition-identity, append-assignment, multiplicity → (r15 audit)
intra-body emitter + same-line decoy. Every round the auditor found a subtler line-granularity
edge. **Root cause (now explicit):** the census is physical-LINE granular; the residuals are all
"line granularity loses column/byte information." **r16 (running now) is a structural fixpoint:**
move the census to exact-byte-span granularity, which closes the whole line-granularity class at
once (the same fail-closed-by-construction move that ended the SEC102 regress). If r16's audit is
clean, RP6 is done. If it still finds a residual, we are at a genuine static-analysis asymptote.

## SEC102 command-word (composite prover; proves no member reaches a sink unanalyzed)

Rounds r1 → r7. Both original CRITICALs (basename member-binding, allocation/constants
reconciliation) closed and Codex-verified. Then command-word coverage took r4→r6 closing one
prefix/expansion class at a time, until r6-audit ACCEPTED the interpreter-vocabulary residual +
conservative false-stops and named ONE structural gap (a blacklist of expansion operators missed
the extglob family). **r7 (running now) inverts to a WHITELIST** — a command word is static only
if every character is in a proven-safe set; any other char → STOP. That closes every operator,
known or future, at once. If r7's audit is clean, SEC102's command-word policy is a fixpoint; the
only remaining disclosed item is the interpreter-VOCABULARY (a recognized name set, a production-
gate decision, not a static-tool defect).

## The decision, if you want to make one

Both tools are now on their **structural fixpoint rounds** (r16 byte-span, r7 whitelist), which
should end the one-class-at-a-time regress. My plan is to let those two rounds + their audits
complete. **If either STILL reopens with a genuinely new admission gap** (not a disclosed
vocabulary/false-stop nit), my recommendation is: **accept the block on "economic block sound +
tool closes every realistic class + remaining residuals disclosed and theoretical," rather than
continue an open-ended grind** — and bring it to you. You can also say "stop now and accept with
disclosure" at any point; nothing here is a hard gate, and the blocks themselves are sound.

No autonomous acceptance of a block will happen without both flagship audits; this note is about
when to stop hardening the PROOF TOOLS, which is a judgment call I'm surfacing rather than making
silently.
