# P0-12 kernel build — owner decision package v2 (2026-08-31 morning)

Written by the Lead ~01:30, REWRITTEN ~02:00 after its own audit lane (A2, Claude) found 9
defects in v1 — all folded here; the audit record is `AUDIT_A2_DECISION_PKG.md` and this
version was re-checked against it. Plain language; claims carry evidence paths; numbered
questions at the end. You can answer with one line, but read the dependency notes first.

## Where things stand (verified facts, with honest labels)

1. The FRESH kernel design (Codex-authored per your addendum 13) went through three
   multi-family audit rounds. Terminal round-3 verdicts, quoted exactly:
   - Claude flagship: **PASS-WITH-NITS** (`AUDIT_P46_P012_V12.md:3`)
   - Grok detection: **NOT DETECTED — 0 findings** (`DETECT_G37_P012_V12.md:24`)
   - Gemini corroborator: **0 required findings, CLEAN** (`DETECT_GM17_P012_V12.md`)
   - OpenCode supplemental (4th family): **NOT CLEAN — 1 MEDIUM + 4 LOW**
     (`REVIEW_DS15_P012_V12.md:14`; the MEDIUM: one probe references a scenario case no
     catalog supplies, "needs a repair before any clean re-issue", `:71`)
   So the design is STRONG BUT NOT UNANIMOUSLY CLEAN. The grid-fitting failure class that
   killed the ten earlier design rounds was hunted by every family and reported absent in
   every round-3 report (and in the earlier rounds' reports by the lanes that ran them —
   the per-round lane IDs are in `N_TIMES.txt`; no single artifact tabulates a full 4x3
   matrix, so that stronger claim is not made here).
2. The kernel BUILD lane (W113) started and REFUSED to write any line: the accepted
   design's own precondition list is not satisfied by the repository
   (`W113_BUILD_REPORT.md`). Branch `feature/wp-p0-12-corrected-vnext-20260831` exists,
   clean, ZERO commits (verified by A2: `git log master..branch` empty). Your fail-closed
   chain worked. The build lane's evidence commands are in its report; the Lead re-ran the
   four file-existence/receipt checks with the same results (this Lead session's
   PowerShell outputs, recorded in `N_TIMES.txt` line `01:3x W113 BLOCK VERIFIED`).

## The FIVE build preconditions (design `P012_FRESH_DESIGN_V1.md:604-612`)

v1 of this package listed four; the design lists five. All five, plainly:

- **P1 (=B01) — "P0-11 accepted" AND a consumable legacy subject.** P0-11 is merged and
  owner-signed (PR #143, addendum-5 signature), but its gate record reads STOP and — the
  substantive half — P0-11 "creates no repository anchor, runs no subject"
  (`WP_P0_11_GATE_2026-08-28/LANE_REPORT.md:14-16`). Ruling "signed+merged = accepted"
  settles the WORD but not the SUBSTANCE: there is still no runnable legacy subject or
  frozen baseline bytes (that is P4 below — same root, split only because the acts differ).
- **P2 (=B02) — OPEN-01..10 terminal dispositions.** Ten owner-gated design values need
  your dispositions in `open_item_applicability.json` before any 2.0.0 build
  (`P012_FRESH_DESIGN_V1.md:576-591`). Needs your reading session, not a one-liner.
- **P3 (=B03) — independent expected-values author.** The design says `CONTRACT_TABLES`
  is authored by **"a person other than the kernel implementer"** (`:426`) and §16 review
  is **mandatory human review** by someone independent of BOTH the implementer and the
  tables author (`:527-538`). Whether an AI lane can satisfy "a person" is YOUR governance
  call — v1 of this package wrongly presented the AI-lane reading as settled. Note the
  knock-on: if Claude authors the tables, Claude is excluded from the §16 reviewer role.
- **P4 (=B04) — exact P0-11 baseline bytes.** Frozen legacy outputs do not exist as files
  (0 tracked matches). Producing them requires RUNNING the legacy kernel — execution you
  have always gated — AND it consumes the scenario catalog that P3's sealed bundle
  defines, so P4 cannot be actioned before P3 produces the catalog.
- **P5 — two further design preconditions the build lane logged and v1 omitted:**
  the design itself says the later build needs "explicit owner approval for the protected
  T0 kernel paths; this design does not supply it" (`:611`), and repository Gate 2 (an
  implementer plan accepted by the Lead, exact path list) must be in place (`:612`).
  Neither exists yet.

Also blocked pending contract rulings (from `W113_BUILD_REPORT.md:140`, not mere
ambiguities): DS15-F02 (are fee/funding arrays projections of `cash_events[]` or
additional mutations?) and DS15-F05 (legacy artifacts use `event_ordinal`; the design
demands `sequence`; an approved version-shaped validation rule is needed — legacy bytes
may not be rewritten).

## Your questions (recommended default first; dependencies stated)

1. **Design residual (DS15-F01 MEDIUM):** (a) RECOMMENDED — authorize ONE bounded design
   repair fold (fix the probe/scenario coherence + the DS15-F02/F05 contract rules as
   [OPEN]-respecting text) and ONE detection re-verify; the D028 3-round repair cap was
   consumed, so this needs your explicit word. (b) Accept the design as-is with the MEDIUM
   recorded (the build would carry it). (c) Park.
2. **P1 wording:** (a) RECOMMENDED — rule that "P0-11 accepted" means the owner-signed
   merged package; the design gets a clarification fold — while noting this does NOT by
   itself produce the legacy subject (that is Q4). (b) Treat P0-11 as not accepted; chain
   re-parks.
3. **P3 authorship:** (a) RECOMMENDED — you rule an AI lane from a non-implementer family
   may satisfy the "person other than the implementer" independence role, named in the
   ledger; §16 human review stays with YOU or a human you name. (b) Wait for a human
   co-author. (Explicitly a governance ruling — the design's word is "person".)
4. **P4 execution:** (a) RECOMMENDED — authorize ONE bounded legacy-kernel run to freeze
   baseline bytes, AFTER Q3's lane seals the scenario catalog (Q4 depends on Q3's
   output; they are sequential, not parallel). (b) Defer.
5. **P5:** (a) RECOMMENDED — grant the explicit T0 kernel-path approval as a named path
   list at build start, and the Lead submits the Gate-2 implementer plan for your visibility
   with the same message. (b) Handle at a later sitting.
6. **P2 (the ten OPEN values):** needs your reading session with
   `P012_FRESH_DESIGN_V1.md` section 19. No default exists — they are economic values.

Nothing starts without your word. The branch stays parked and clean under every answer.
