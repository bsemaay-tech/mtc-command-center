# Governance stage handoff

## [Claude Opus 5 Lead] 2026-08-28 night → 2026-08-29 morning — owner approved three packages; WP-P0-10 merged, WP-P0-11 blocked at repair 3

- **Outcome:** the owner ruled on all three blocked packages at 20:56 and went offline.
  **WP-P0-10 is built, dual-flagship PASSED, and MERGED — `master` is now `7f9ef16a` (PR #135).**
  The promotion decision was recast as report-only, audited and corrected. **WP-P0-11 advanced four
  commits and is currently BLOCKED** on a detection finding. Four owner decision pages and a
  costed hours record are in `C:\tmp\LANE_PROMPTS_20260828\`.

- **WP-P0-10 — MERGED and PARKED.** A single verifier-owned SHA-256 now pins the whole declaration
  inventory: `DECLARATION_INVENTORY_SHA256 = b1d81fb1…`, 241 records (224 fixture-local, 17
  companion), 2,660 declared input paths. The demonstration that failed the package — remove one
  declaration, add another, keep the total at 2,660, update the package's own hashes — is proven
  **RED-then-refused on the same bytes**: accepted by the verifier at `9a76818f`, refused at HEAD.
  Regression `47/47 refused, 2/2 controls, baseline clean`, re-run on `master` after the merge.
  The owner's condition was met: the suite's claim is narrowed to **declaration integrity, not value
  integrity**, in `fixtures/README.md`, the module docstring, `manifest.json` and `LANE_REPORT.md`.
  **Two caveats that must travel with this:** PR #135 carried the **whole** package — 14 commits, 29
  files, ~12,859 insertions — while the two flagship audits covered only the final two commits
  against their parent; and **CI does not execute this package at all** (the required check is the
  Bridge suite), so the green tick is silent about what merged.

- **WP-P0-11 — four commits, BLOCKED.** `255e71c5` (stage 1: one scenario-binding module replacing
  two duplicated guards, plus four mechanical findings), `217feb52` (stage 2: exact-bound authority
  set, comparison rule, mutation criteria, expectation provenance), `3c606d57` and `0b94d923`
  (two repair rounds). Measured row arm moved **33 GREEN / 7 STOP → 27 GREEN / 13 STOP / 2
  not-applicable**. **That movement is the gate starting to work, not degrading** — rows lost GREEN
  because checks that had been asserted began to be performed. **Do not restore 33/7.**
  **Current blocker:** a detection review of `0b94d923` found **10 surviving self-consistency
  comparisons** in `row_arm.py` (both operands reachable from one local name; measured identical on
  33/33 executable and 7/7 unresolved bindings). Repair round 3 is dispatched.

- **The defect class, now fully characterised — this is the durable finding.** One defect dominated
  the night: *a value declared as checked that nothing actually checks*. It appeared **four times,
  three of them inside the repairs meant to remove it**, written by three different models in three
  different lanes. **It is a specification failure, not an author failure:** when the instruction is
  "make X verified", the cheapest passing implementation builds the proof out of X.
  **What worked was not more auditing.** Two rules written into the build spec — *name the producer
  and source of both sides of every comparison*, and *exhibit an input that makes each check fail* —
  found **seven** instances in one lane where three independent audits had found three, and then
  **prevented two more in a design before a line was written**. Cost per instance falls by roughly an
  order of magnitude at each step earlier in the pipeline. **Two structural fixes are the model to
  copy:** a module *forbidden to import* the generator it must disagree with, and a provenance
  `method` promoted to a **required keyword-only parameter** so no caller can stamp a label without
  declaring one.

- **WP-P0-11 stage 4 (v3 publication) — designed, and STOP.** Nine blockers must close before the
  owner signs. Two are serious in their own right: **`p011_gate.py` `row_arm_receipt()` hardcodes
  `{green 33, stop 7, not_applicable 2}` and refuses any evidence that disagrees** — a check that can
  only pass on a wrong answer, in the code that produces the receipt the owner signs; and
  **`stage1_freeze.main()` and `command_finalize_candidate()` write the external owner-signed anchor
  themselves** — code must never issue the owner's signature. Also: candidate generation is
  **circular**, and the baseline hashes `sys.executable`, the Python build string and the platform
  into its own bytes, so it is **not reproducible by a third party**.

- **Findings outside the three packages, all read-only and all owner-facing.** These matter more than
  the packages and each has a decision page:
  - **The kill switch does not flatten on the deployed store.** `engine.kill()` latches `KILLED` and
    returns unless the store is schema **v9** (`SCHEMA_VERSION_KILL_EVIDENCE = 9`); the deployed
    store is **v4**. Known since August, but it had been carried forward as a *sound* safety property.
  - **11 economic controls fully inert, one partially**, from **one line**: `bridge/app.py:108` calls
    `store.initialize()` with no argument, taking baseline schema v4 and never opting into the
    capabilities above it. The opt-in design is deliberate and correct; nothing ever opts in.
  - **The forward-paper queue is inert** — all 46 stored scorecards lack the `gate2.metrics` object
    it reads, so every candidate is rejected for missing data, not quality. **The
    `FORWARD_PAPER_CANDIDATE` labels on strategy folders never passed that queue**; they came from a
    classification or a human note.
  - **`pine-alert-guard` does not gate.** The only required status check under ruleset
    "Protect master – required CI" is `Bridge suite (Python 3.12)`. A live `alert(` could merge past
    a red guard. **`branches/master/protection` returns 404 — protection is a ruleset, not classic
    branch protection.**
  - **`config/bridge.yaml` is largely decorative** — a dozen keys have zero Python readers.
  - **Range Filter** is short-biased from a flat start, in Python *and* Pine; research-only;
    recommendation is to document, not change.

- **Governance:** WP-P0-11 must merge as **one unit after stage 4**, not stage by stage — a partial
  merge puts a package on `master` whose signed receipt does not describe its own code. Flagged to
  the owner as reversible if he disagrees.

- **Route reality corrected:** Codex `secondary` and `fourth` were recorded as capped until Aug 31.
  **Both are live.** Grok is **exhausted (402)** after 12 lanes — the owner's stated goal for that
  route. Claude Max was spent under his dated one-night authorization, recorded with the Pro
  exhaustion evidence that triggered it; **that authorization does not carry forward.**

- **Lead errors: 19 recorded**, including three safety-shaped claims corrected before the owner read
  them, four counts bounded by a search pattern rather than by the repository, and **four hours of
  idle time caused by dispatching lanes without starting the waiter that reads their results** — the
  largest single waste of the night. Full account in `N_HOURS_LEDGER.md`.

## [Claude Opus 5 Lead] 2026-08-28 evening — flagship audit round; three packages returned to the owner

- **Outcome:** the three queued flagship audits ran. **All three packages are blocked or parked and
  none was merged.** `master` remains `85c3e17f`. Three owner decisions are open; each has a
  plain-language page under `C:	mp\LANE_PROMPTS_20260828\`.
- **WP-P0-10 round 4f (`9a76818f`) — BLOCK, parked.** Two independent flagships and the third
  auditor agreed. Round 4f's completeness rule is verifier-owned and holds on its own terms, but the
  **declaration inventory it iterates is fixture data**: emptying the 24 companion PINNED
  declarations and flipping all 32 values passed with baseline-identical counts
  (`2660`/`241`/`397`). Coverage is 52 of 1327 declared `config.*` occurrences. Both flagships judged
  the fixture-local surface **not defensible for acceptance without an owner ruling**. The
  pre-committed stopping rule fired; **no round 5 dispatched**. Fixture edits were independently
  confirmed citation-only; the F-3 authority pin is genuinely closed.
- **WP-P0-11 gate v2 bump — DONE, owner-authorized, pushed `82144f01`.** Premise verified before
  rebuild (93 hunks, citations only); double build byte-identical at 96,154 observations; **full
  C01–C42 re-verified with identical dispositions — 33 GREEN / 7 STOP / 2 policy-only, and no STOP
  became GREEN**; v1 anchor retained; gate still **STOP**.
- **WP-P0-11 gate audit — BLOCK by both flagships, returned to the owner.** Fresh instances of the
  declared-but-uncompared class **in the GREEN rows**: `clean_producer_corroboration` declared
  `required: true` on all 40 rows and compared by nothing (6 GREEN rows declare two authorities and
  ran one); `comparison_rule` and `producer_mutation.required_red` present-checked only;
  `p011_gate.py:577`'s completeness guard is a strict-subset test that catches 0 of 8. **The
  receipt's `76/76` is really `68/76` with 8 fields absent and `outcome: STOP`** — the lane's own
  full-stream matrix at `ee501fe4` measured that, was deleted at `4d2581e4`, and the v2 re-pin also
  removed the sentence limiting the 76. **C32/C34/C42 are gate encoding errors, not authority
  contradictions** — only C35 is real, a `NameError` in A present since the initial commit that must
  not be preserved. Comparator itself proven sound: 134/134 leaf variants detected.
- **Promotion-gates package — stopped at the T2 cap.** Confirm audit REQUEST_CHANGES with 3 required
  findings plus a Lead-adjudicated fifth. `AGENTS.md` allows T2 one repair round; it has had one, so
  **no second round was dispatched**. Impact numbers fully re-derived and true.
- **Live condition, independent of any decision:** 17 `producer_spec.json` files carry
  `FORWARD_PAPER_CANDIDATE`, minted from classification alone; the next registry rebuild propagates
  it. Not order-reaching (promotion registry empty).
- **Git / safety:** no merge, no tag, no protected surface, no Pine execution, no host/broker/venue
  action, no setting change. Both audited worktrees ended clean at their audited SHAs. **Claude Max
  was not spent** (verified from `.claude-max` timestamps before and after the Codex lanes).
- **Rotation (G7):** the replaced 2026-08-28 documentation-pack section is appended verbatim to
  `_AI_MEMORY/history/00_AGENT_PROTOCOLS_HANDOFF.md`; nothing deleted.
- **Evidence:** `C:	mp\LANE_PROMPTS_20260828\` — `HOURS_LEDGER.md` (measured times, 15 lanes),
  `MORNING_REPORT_2026-08-29.md`, three `OWNER_DECISION_*.md`, four audit reports, three costed
  design proposals, `LEAD_VERIFICATION_2026-08-28_EVENING.md` (six Lead-executed checks).
