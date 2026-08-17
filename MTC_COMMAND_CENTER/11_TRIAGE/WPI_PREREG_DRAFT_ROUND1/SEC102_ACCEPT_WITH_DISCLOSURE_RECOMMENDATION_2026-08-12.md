# SEC102 — Lead recommendation: ACCEPT WITH DISCLOSURE (owner decision required)

Date: 2026-08-12 ~13:00. Author: Lead (Fable session). Status: **awaiting owner decision.**
This is a judgment call the Lead is surfacing rather than making silently, exactly as
`CONVERGENCE_NOTE_RP6_SEC102_2026-08-12.md` said it would be.

## Plain-language summary (read this part if nothing else)

SEC102 is the tool that proves the WP-I security block never lets a command reach a file or a
network without being checked. **That tool itself is finished and sound.** Its file has been
byte-for-byte unchanged for five straight rounds (`composite_pathproof.py`, 129658 bytes,
`adbf27fd…c05a`) and Codex re-confirmed that identity at every round including today.

Everything that took five rounds today was the **evidence harness** — the machinery that proves
the self-QA document's published commands really are the ones that ran. Not the security logic.
The harness got dramatically stronger each round, and each time the auditor found a subtler
version of the same question: *can anyone slip different bytes between "what we checked" and
"what actually ran?"*

Today's rounds, in order:
- **r9** — the harness was rewriting line endings before running. Fixed: it now runs the exact
  published bytes.
- **r10** — a fast attacker could swap the file between the check and the launch. Fixed: the file
  is locked open by the operating system across the whole run.
- **r11** — a fast attacker could re-point a drive letter instead. Fixed structurally: the
  interpreter is no longer given a *filename at all* — the checked bytes are handed to it
  directly through a pipe. There is nothing left to swap.

**Codex verified r11 works** (55/55 transcript lines reproduced exactly, all attack tests flip
the right way, the mutant that undoes the fix brings the flaw back — so the fix is real, not
decorative). Then it found the next layer down: the harness runs under a plain `python` command,
and someone who already controls that machine's Python environment could tamper with the harness
itself before it starts.

**Codex's own verdict says: stop here, do not build round 12, ask the owner.** The Lead agrees.

## Why stopping is the right call, not fatigue

Each round genuinely closed a real class, and each new finding is one layer further from the
thing we actually care about:

| Round | What could be attacked | Who has to already control what |
|---|---|---|
| r9 | line endings in the published bytes | nothing — a real defect |
| r10 | the file, between check and launch | a process on the same machine, same user |
| r11 | the drive-letter/volume mapping | same, plus timing precision |
| r11-F1 (new) | the Python runtime running the harness | **the machine's Python install / environment** |
| residual 51 | which `powershell.exe` is found | **the machine's PATH** |

The last two require an attacker who already owns the developer machine's runtime. At that point
they do not need to fool the harness — they can change anything. This is the classic point where
hardening stops buying safety and starts buying paperwork. Codex reached the same conclusion
independently and wrote it into its verdict.

## What is closed (Codex-verified, all still standing)

- Both original CRITICALs: basename member-binding → exact deploy-path matching; allocation ↔
  constants reconciliation.
- The command-word policy inverted to a **whitelist fixpoint** — a command word counts as a safe
  leaf only if every character is in a proven-safe set; anything else STOPs. Closes extglob and
  every future operator at once.
- R3-F2 / R3-F3.
- Harness: r7 child-completion (status + stderr before stdout is believed), r8 byte-identity,
  r9 direct-object binding, r10 transient-rebind and mixed-chain — all closed and reproduced.
- The 58-case module matrix passes verbatim at every round; the eleven published evidence blocks
  reproduce byte-identically.

## What would be disclosed, not fixed (the actual decision)

If you accept, SEC102 ships with these written down as **trusted-base assumptions**, meaning "we
did not prove these; we assume the developer machine is not already compromised":

1. **The outer Python runtime** — the `python` that runs the evidence harness, its startup mode,
   import path, and standard library (Codex R11-F1, new today).
2. **The interpreter image** — which `powershell.exe` gets found via `PATH` (residual 51).
3. **The on-disk document vs. a fresh clone** — byte identity is checked against the file as it
   exists here; a fresh Windows checkout could rewrite line endings, which would produce a **loud
   failure**, not a silent pass (residual 41).
4. **The interpreter vocabulary** — the recognized-interpreter name set, to be pinned at
   production-gate time. **You already ratified this one on 2026-08-12** (decision C).

Items 1–3 are all "someone already owns this machine" assumptions. None of them affects the
security logic that WP-I actually depends on.

## Options

**Option 1 — ACCEPT WITH DISCLOSURE (Lead recommendation).**
SEC102 is accepted on: economic block sound and byte-identical; both CRITICALs and the
command-word fixpoint closed and cross-model verified; the evidence harness closes every
realistic in-model class; residuals 1–4 above disclosed in `STATUS_SEC102.md` and carried into
the successor preregistration as trusted-base assumptions. The GLM-5.2 second opinion (running
now) is attached as the model-diverse check. WP-I freeze blocker #4 clears.

**Option 2 — Authorize a separate, scoped design round** to bind the outer executor (exact
trusted interpreter, isolated/no-site startup, no user-controlled import root). This is a
*different* piece of work with its own scope fence, not a round 12 of the harness. Costs a
further build+audit cycle and, in the Lead's view, buys protection only against an attacker who
already controls the machine.

**Option 3 — Stop and reassess later.** SEC102 stays non-accepted, WP-I freeze stays blocked on
blocker #4, and the other lanes (RP6/RP7/transport second-flagship audits tonight) continue.

## What the Lead does while waiting

No SEC102 round is dispatched. The GLM-5.2 second opinion completes and is committed as evidence
either way. The 23:00 Claude Pro second-flagship audits (transport, RP7, RP6, pathscope) run as
planned. Nothing here blocks those.
