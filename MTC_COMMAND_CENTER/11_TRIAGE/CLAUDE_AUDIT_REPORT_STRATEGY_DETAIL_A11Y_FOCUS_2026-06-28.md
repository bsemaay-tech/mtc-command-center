# Claude Audit Report — Strategy Detail P1 A11y Focus

**Auditor:** Claude Opus 4.8
**Date:** 2026-06-28
**Scope:** Codex patch for the Impeccable Strategy Detail P1 a11y-focus follow-up — making the
four STAGE workflow cards native keyboard-focusable controls, adding a global `:focus-visible`
ring, a focused workflow-card state, and `prefers-reduced-motion` handling for the amber pulse.

---

## Verdict

**PASS WITH NITS**

The a11y change is correct, minimal, and meets every requirement of NEXT_STEPS item P1
"a11y focus." All validation passes (2 a11y tests OK, 89 full-suite OK, `node --check` OK,
`git diff --check` clean). Nits are working-tree hygiene and one optional reduced-motion gap —
no regression and no code fix required.

---

## Questions — answers

1. **Four workflow/STAGE cards now keyboard-focusable native controls?** YES.
   `workflowCard()` emits `<button type="button" class="workflow-card ...">` instead of a
   clickable `<div>` (`app.js:987-989`). Native `<button>` is focusable and Enter/Space
   activates the `onclick` handler by default — no manual `tabindex`/`role`/keydown needed.
   `type="button"` correctly prevents any implicit form submission.

2. **Existing scroll behavior + visual layout preserved?** YES. The `onclick="scrollToSection('${section}')"`
   handler is unchanged. `.workflow-card` gains a full button reset
   (`display:block; width:100%; color:inherit; font-family:var(--sans); text-align:left`,
   `styles.css:609-621`) so the native button matches the prior div's box, typography, and
   left alignment inside the `repeat(4,1fr)` grid. `padding:13px 14px` and `cursor:pointer`
   retained; child `.stg/.ttl/.st` rules unchanged.

3. **Global `:focus-visible` ring visible without layout shift?** YES.
   `:focus-visible { outline: 2px solid var(--teal); outline-offset: 3px; }`
   (`styles.css:63-66`). `outline` does not participate in layout (unlike `border`), and
   `outline-offset` only pushes the ring outward — no reflow/shift. Teal on dark panels is
   clearly visible.

4. **`.workflow-card:focus-visible` clear focused state?** YES.
   `styles.css:623-626` sets `background: var(--panel-hover)` + `border-color: rgba(45,212,191,0.65)`,
   combining with the global teal outline for an unambiguous focused look distinct from
   hover-only.

5. **`prefers-reduced-motion: reduce` disables the amber pulse?** YES.
   `.dot.amber { animation: pulse 2s infinite; }` (`styles.css:197`) is overridden by
   `@media (prefers-reduced-motion: reduce) { .dot.amber { animation: none; } }`
   (`styles.css:203-205`). Equal specificity, later source order → the `none` wins. Verified.

6. **New static test meaningful, not overbroad?** YES.
   `test_strategy_detail_a11y_static.py` asserts (a) the workflow card is a
   `<button type="button" class="workflow-card`, (b) no `div.workflow-card[onclick]` remains,
   (c) `:focus-visible {`, `.workflow-card:focus-visible`, and
   `@media (prefers-reduced-motion: reduce)` exist, and (d) `.dot.amber { ... animation: none }`.
   Scoped to the exact contract; regex anchors are specific enough not to be trivially
   satisfied by unrelated CSS.

7. **Codex stayed inside UI/a11y scope?** YES for the a11y change itself — only the
   `workflowCard` markup and the four a11y CSS additions. No Pine/MTC_V2/parity/backtest/
   schemas/broker/scorecard/trading logic touched. (See NIT-1 on co-resident unrelated edits.)

8. **Handoff/NEXT_STEPS accurate?** YES.
   `GLOBAL_HANDOFF.md` "Codex GPT-5 2026-06-28 — Strategy Detail P1 a11y focus" accurately
   describes the div→button swap, focus ring, focused state, reduced-motion, the new test, the
   UI-only scope, and validation (2 a11y tests, 89 full, node --check, diff --check) — all
   matching my reruns. `NEXT_STEPS.md` marks item 2 "[P1] a11y focus" DONE with "Claude audit
   pending" — correct status at audit time.

---

## Findings

### NIT-1 — Working tree mixes three independent uncommitted UI tasks
`app.js` and `styles.css` currently carry three unrelated uncommitted changes at once:
(1) **this** a11y-focus patch, (2) the artifact-universe-mismatch boolean work
(`app.js` `profileRowFlags`, audited separately — PASS WITH NITS), and (3) DeepSeek's
empty-state contrast fix (the `var(--faint)`/`var(--faintest)` → `var(--muted)` swaps across
~10 selectors, documented in GLOBAL_HANDOFF). The a11y diff is cleanly separable from the
other two, but per `AGENTS.md` PARALLEL AGENT SAFETY these should be committed as distinct
commits so an agent re-reading the file does not treat co-resident uncommitted edits as
corruption. Hygiene only — no defect in the a11y change.

### NIT-2 — Reduced-motion covers only the amber pulse, not all animation
`@media (prefers-reduced-motion: reduce)` disables `.dot.amber` pulse but does not gate the
toast/modal `animation: slidein .25s ease` (`styles.css:881`) or other transitions. This
matches the *letter* of the NEXT_STEPS item (which named only the pulse dot), so it is in
scope — but a fully complete reduced-motion implementation would also neutralize `slidein`.
Optional future polish, not required for this item.

---

## Commands run and results

```
node --check app.js                          -> NODE_OK
git diff --check (app.js, styles.css, test)  -> clean (only LF->CRLF warnings)
PYTHONPATH=. python -m unittest tests.test_strategy_detail_a11y_static
                                             -> Ran 2 tests ... OK
PYTHONPATH=. python -m unittest discover tests
                                             -> Ran 89 tests in 49.786s ... OK
```

Manual verification:
- `.dot.amber` pulse at `styles.css:197`, disabled at `styles.css:203-205` (later, equal
  specificity → wins).
- `.workflow-card` button reset confirmed complete (`styles.css:609-621`): display/width/
  color/font-family/text-align/background/border/border-radius/padding/cursor/transition.
- `:focus-visible` uses `outline` (no layout impact).

---

## Fixes applied

None. Read-only audit. No staging, commits, branches, or destructive git operations.

---

## Protected-scope confirmation

CONFIRMED. The a11y patch does not touch Pine, MTC_V2, parity, backtest, schemas,
broker/execution, scorecard math, artifact semantics, or trading logic. Changes limited to
the `workflowCard` DOM element and four a11y CSS rules, plus a static guard test. The
unrelated edits sharing the working tree (artifact-universe boolean, DeepSeek contrast swap)
are documented sibling tasks and are out of scope for this item (NIT-1).
