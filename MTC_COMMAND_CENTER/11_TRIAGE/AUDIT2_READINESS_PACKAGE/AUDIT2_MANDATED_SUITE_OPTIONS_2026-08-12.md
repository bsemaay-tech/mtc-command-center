# AUDIT-2 MANDATED SUITE — OPTIONS FOR THE OWNER (2026-08-12)

**Author:** Claude Opus 5, counterpart IMPLEMENTER. **Acceptance owner:** Codex Lead.
**Status of this file:** options only. **P10-10 remains unwritten** — this document does not
create it, does not choose a command, and does not state any count.

**Executed in this session:** nothing. No test, no collection, no lint, no compile, no Git, no
host, no network action. Tools used were Read and Write only; a later bounded repair pass used
Read and Edit only. Every number appearing below is quoted from a dated record, is a static
filename count, or is arithmetic over those; none was produced by a run today.

**Citation-rule carve-out, stated up front.** The kickoff requires every claim to carry a
`file:line` (`KICKOFF_CODEX_MANDATED_SUITE_OPTIONS.md:28-33`). The `[STATIC]` filename totals in
§3 and every figure derived from them do **not** meet that rule and are not presented as if they
did — see `[STATIC-UNCITED]` below and the note opening §3.

**Label key used throughout.**
`[MEASURED-ELSEWHERE]` a value quoted from a dated record, with its source.
`[STATIC]` a count of filenames or a configuration fact read from bytes without execution.
`[JUDGMENT]` a planning estimate by this author, not a measurement.
`[STATIC-UNCITED]` a filename total, or arithmetic over such totals, produced by a bounded path
inventory rather than read from a citable line. It carries **no `file:line`** and therefore does
not satisfy the kickoff's universal citation rule; it is not independently checkable from this
document and must be re-derived before any freeze. Every `[STATIC]` total in §3 is also
`[STATIC-UNCITED]`.
`[STATIC-ABSENCE]` a path that a static inventory did not find; no file is cited, because
citing a `file:line` for a file that does not exist would itself be the Pattern-10 defect
(`DESIGN_DEFECT_PATTERNS_2026-08-10.md:617-621`).

---

## 1. What P10-10 must contain, and why it blocks two other components

The auditor contract requires all of the following to be filled and frozen **from one
authoritative source before dispatch**: `MANDATED_COMMAND`, `EXPECTED_EXIT_CODE`,
`EXPECTED_PASS_COUNT`, `EXPECTED_FAIL_COUNT`, `EXPECTED_FAILURE_1`, `EXPECTED_FAILURE_2`,
`EXPECTED_SKIP_XFAIL_COUNTS`, `BASELINE_SOURCE` at the frozen SHA.
`AUDIT2_AUDITOR_SESSION_INPUTS.md:89-100`

The same section is an explicit dispatch blocker: "the authoritative command, test IDs, exact
counts, output signatures, and frozen-SHA baseline are wholly unresolved."
`AUDIT2_AUDITOR_SESSION_INPUTS.md:84-87`

No auditor may substitute a command or infer the anomaly set; each required auditor must execute
the mandated suite, and inability to execute requires BLOCK — non-execution is not acceptance.
`AUDIT2_AUDITOR_SESSION_INPUTS.md:102-104`

The scope study records the cascade: P10-10 has no producing step, P10-11 (the frozen-SHA
execution record) cannot be specified while the command is unchosen, and P10-12 (the accepted
anomaly register) cannot be adjudicated without a baseline.
`AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:62-64`, `AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:71`

The handoff package restates that none of these may be inferred from a pre-freeze tree.
`AUDIT2_HANDOFF_PACKAGE.md:163-168`; and the readiness matrix row S3 marks the suite and anomaly
baseline `NOT-YET-AVAILABLE` with the instruction "do not infer two gc-referent failures."
`AUDIT2_HANDOFF_PACKAGE.md:78`

**Ordering constraint.** The mandated suite is defined and executed at step 13 of the combined
production order, after the pre-WP-A freeze at step 12 and before Audit-2 dispatch at step 15.
`AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:119-122`

### Which defect patterns this decision is exposed to

- **Pattern 10, "evidence that cannot fail."** Self-produced counts and templated command
  records offered as closure when nothing about them could have come out wrong; "A count is not
  a fixture — it has no red state." `DESIGN_DEFECT_PATTERNS_2026-08-10.md:617-628` A hardcoded
  `EXPECTED_FAIL_COUNT` or a copied anomaly list is exactly this.
- **Pattern 9, "the sentence outruns the probe."** The recorded claim is broader than the
  executed predicate can establish. `DESIGN_DEFECT_PATTERNS_2026-08-10.md:547-551` A
  `MANDATED_COMMAND` covering one product while the prose says "the repository suite" is this
  defect.
- **Pattern 1, "STOP is not a result."** A condition under which a check could not be evaluated
  emitted as a verdict, or an evaluable observation emitted as an inability to evaluate.
  `DESIGN_DEFECT_PATTERNS_2026-08-10.md:48-52` For the suite this means: a collection error, an
  ACL `PermissionError`, or a missing dependency is **not** a pass and **not** an accepted
  failure — it is STOP.
- **The RP6 literal-zero analogy.** The kickoff states the governing analogy directly: an empty
  anomaly set must be an observed and adjudicated result, never a hardcoded count — "the same
  defect class as RP6's `dynamic_targets=0` literal found today."
  `KICKOFF_CODEX_MANDATED_SUITE_OPTIONS.md:39-42`

---

## 2. Historical baseline claims, located and dated

The kickoff requires each such claim to be located, sourced, dated, and adjudicated as history
rather than treated as the answer. `KICKOFF_CODEX_MANDATED_SUITE_OPTIONS.md:28-33`

| # | Claim, verbatim in substance | Source `file:line` | Date | Adjudication |
|---|---|---|---|---|
| H1 | Windows full suite `1359 passed, 1 warning`, Lead-reproduced, original run `136.91s`, independent rerun in fresh detached worktree `C:\GAAUD_INT_GLM` `130.09s` | `GATE_A_INTEGRATION_RECORD_EBADA020_2026-08-03.md:136` | 2026-08-03 | `[MEASURED-ELSEWHERE]` at SHA `ebada020`. **Superseded** — see H8/H9. |
| H2 | Locked Linux full suite `2 failed, 1357 passed, 1 warning`, CLOSED 2026-08-03 | `GATE_A_INTEGRATION_RECORD_EBADA020_2026-08-03.md:137` | 2026-08-03 | `[MEASURED-ELSEWHERE]` at `ebada020` on `gatea-staging`, Ubuntu 24.04.4, Python 3.12.3, SQLite 3.45.1 (`:142-143`). **Superseded** — see H7. |
| H3 | Lead reproduction: `cd C:\GAAUD_INT_GLM\IBKR_PAPER_BRIDGE` then `python -m pytest -q` → `1359 passed, 1 warning in 130.09s` | `GATE_A_INTEGRATION_AUDIT_ROUND1_EBADA020_2026-08-03.md:84-88` | 2026-08-03 | `[MEASURED-ELSEWHERE]`. The record itself says "It is Lead evidence, not auditor evidence" (`:90-92`). This is the **only fully written-out invocation with its CWD** in the historical set. |
| H4 | Round-2 auditor: Windows full suite `1359 passed, 1 warning in 136.00s`, exit 0 | `GATE_A_INTEGRATION_AUDIT_ROUND1_EBADA020_2026-08-03.md:116-121` | 2026-08-03 | `[MEASURED-ELSEWHERE]`. A **retelling of the same `ebada020` baseline**, independently produced — not a separate baseline. |
| H5 | Round-3 auditor invocation `$env:PYTEST_ADDOPTS='-p no:cacheprovider'; python -m pytest -q` in `C:\GAAUD_INT_GLM\IBKR_PAPER_BRIDGE`, result `1359 passed, 1 warning in 222.05s` | `GATE_A_INTEGRATION_FLAGSHIP_AUDITS_EBADA020_2026-08-08.md:68-74` | 2026-08-08 (run), same `ebada020` artefact | `[MEASURED-ELSEWHERE]`. Again a **retelling of the `ebada020` floor**, not a new baseline. Notable for carrying an explicit plugin control (`-p no:cacheprovider`) and for a 222.05s runtime against the same count. |
| H6 | Preregistered Linux expectation `2 failed, 1357 passed, 1 warning`, with **exactly** two permitted failures: `tests/test_order_state.py::test_gc_referents_of_transitions_contain_no_mutable_container` and `tests/test_order_state.py::test_gc_referents_of_raw_aliases_contain_no_mutable_container`; both CPython-version-dependent, both fail identically on parent `637307e8`, both pass on Windows CPython 3.14; "any third failure, or any failure whose node ID is not one of those two" is FAIL | `GATE_A_PREREGISTRATION_ADDENDUM_B_2026-08-08.md:51-67` | 2026-08-08 | `[MEASURED-ELSEWHERE]`, measured twice (Lead 2026-08-03; `claude-opus-5` xhigh 2026-08-08) per `:62-64`. **Exact dated history for a specific Linux runtime at a specific SHA. Not current.** |
| H7 | Addendum C keeps A-3 at `2 failed, 1357 passed, 1 warning` because the round-1 repair `ed3d0534` added two assertions **inside existing test functions**, so the count does not move; Windows floor stays `1359 passed, 1 warning`, Lead-reproduced at `ed3d0534` in `198.90s` | `GATE_A_PREREGISTRATION_ADDENDUM_C_2026-08-08.md:55-59` | 2026-08-08 | `[MEASURED-ELSEWHERE]`. Explains **why** the numbers held: no new test function. |
| H8 | Addendum D **rebaselines**: round-2 candidate `2ce41e34` adds **one new test function**, so expected Linux becomes `2 failed, 1358 passed, 1 warning` with exactly the same two pre-registered `test_order_state.py` node IDs, and the Windows floor moves `1359` → `1360` | `GATE_A_PREREGISTRATION_ADDENDUM_D_2026-08-08.md:56-66` | 2026-08-08 | `[MEASURED-ELSEWHERE]` for Windows; the Linux figure is explicitly stated as "the expected count and must be checked on the host; it is not asserted from Windows" (`:63-64`). |
| H9 | At `2ce41e34`: Lead full suite `1360 passed, 1 warning in 122.86s`; flagship `gpt-5.6-sol` `1360 passed, 1 warning in 116.05s`; flagship `claude-opus-5` `1360 passed, 1 warning in 145.53s`; `GLM-5.2` `1360 passed, 1 warning`; DeepSeek slot BLOCK, non-execution | `GATE_A_DISARM_FIX_AUDIT_ROUND2_2CE41E34_2026-08-08.md:12-15`, `GATE_A_DISARM_FIX_AUDIT_ROUND2_2CE41E34_2026-08-08.md:54-57` | 2026-08-08 | `[MEASURED-ELSEWHERE]`. The **last Windows figure of record** for the Bridge product. |
| H10 | Handoff retelling of H8/H9: full suite `1360 passed, 1 warning in 122.86s` ("floor +1 — one new test function"); Gate A inputs rebaselined in Addendum D with Linux A-3 expected `2 failed, 1358 passed, 1 warning`, same two pre-registered failures | `MTC_COMMAND_CENTER\_AI_MEMORY\GLOBAL_HANDOFF.md:1844-1852` | 2026-08-08 | **Retelling, not a separate baseline.** It quotes the Addendum-D and round-2 records above. |
| H11 | Old checklist: mandated command plus "expected baseline (current accepted anomaly set, e.g. the two permitted `test_order_state.py` gc-referent failures, stated explicitly)" | `AUDIT2_EVIDENCE_CHECKLIST_DRAFT_2026-08-09.md:103-106` | 2026-08-09 | **Superseded.** This is the sentence the refreshed package forbids repeating as current. |
| H12 | Coherence finding 9: the package "provides no authoritative command, test IDs, output signatures, or frozen-SHA baseline that establishes this as the current accepted anomaly set … The quoted sentence must not be presented as a current baseline." | `AUDIT2_COHERENCE_CODEX_2026-08-10.md:28` | 2026-08-10 | Governing adjudication of H11. |
| H13 | A **different, later** two-failure set: "Frozen test floor at `678e8b94`: `2 failed, 1113 passed` (`--ignore=TSP1009B.pytest_tmp_s1r1`, Python 3.14.2 / pytest 9.0.2). Both failures pre-existing … the stale KVM2 ledger hash and the stale `schema_version == "2"` expectation against default v4." | `MTC_COMMAND_CENTER\_AI_MEMORY\GLOBAL_HANDOFF.md:2531` | current-memory entry, WP-S | `[MEASURED-ELSEWHERE]`. **This is not the gc-referent pair.** Different SHA, different interpreter, different ignore flag, different failure identities, different pass count. |
| H14 | Product memory names the same later pair: "Two suite failures are **pre-existing and out of scope** on every branch: the stale KVM2 evidence ledger hash, and `test_invariants_preserve_risk_and_history` asserting `schema_version == "2"` against the current default v4." | `MTC_COMMAND_CENTER\_AI_MEMORY\PROJECT_MEMORY.md:73-75` | current | `[MEASURED-ELSEWHERE]` as a standing description. Corroborates H13 and **contradicts any assumption that the gc-referent pair is the live anomaly set.** |

### The adjudication the owner needs in one paragraph

`1359` was **old-SHA Windows evidence** at `ebada020` (H1, H3, H4, H5), later **superseded by
`1360`** after exactly one test function was added in `2ce41e34` (H8 `:56-66`, H9 `:56-57`). The
**two gc-referent Linux failures were exact dated history** — a real, twice-measured, correctly
preregistered expectation for a specific Linux runtime at a specific SHA (H6 `:51-67`) — and
they are **not a statement about current state**. Current memory names a **different later
two-failure set** entirely: the stale KVM2 ledger hash and the stale `schema_version == "2"`
expectation, on Windows, at `678e8b94` (H13, H14). The refreshed package prohibits inferring
either as the current baseline (`AUDIT2_AUDITOR_SESSION_INPUTS.md:84-87`,
`AUDIT2_HANDOFF_PACKAGE.md:78`). **Therefore no historical record can serve as `BASELINE_SOURCE`
today.** `BASELINE_SOURCE` must be a path at the *frozen SHA*
(`AUDIT2_AUDITOR_SESSION_INPUTS.md:99`), and every SHA above predates the pre-WP-A checkpoint,
which does not yet exist (`AUDIT2_HANDOFF_PACKAGE.md:165-168`). The history is useful for exactly
two things: sizing the run `[JUDGMENT]`, and proving that this suite's counts move for
understandable, auditable reasons (H7 explains a non-move; H8 explains a +1 move).

---

## 3. Test surfaces that exist in this repository

All counts in this section are `[STATIC]` filename counts of `test_*.py`, taken from a bounded
path inventory. **They are not collected counts and not pass counts.** A collected count can
differ from a file count for many reasons (parametrization, skips, collection errors), and
asserting otherwise would be a Pattern-9 overclaim
(`DESIGN_DEFECT_PATTERNS_2026-08-10.md:547-551`). Dependency tests inside `.venv`/`site-packages`
are excluded from every figure.

**Every total in this section is `[STATIC-UNCITED]`.** The totals below — **29**, **13**, the
`2/1/5/1` group, **80**, the QuantLens figures, **26**, the small-surface figures, and the
`~145`-outside figure derived from them — come from a bounded path inventory performed for this
task, not from any line of any file. No `file:line` is or can be given for them, and inventing
one would be the Pattern-10 defect at `DESIGN_DEFECT_PATTERNS_2026-08-10.md:645-653`. They are
therefore **unsupported under the kickoff's universal citation rule**
(`KICKOFF_CODEX_MANDATED_SUITE_OPTIONS.md:28-33`): usable for sizing and comparison
`[JUDGMENT]`, not usable as evidence, and each must be re-counted and recorded with its
inventory method before it enters `MANDATED_COMMAND` or any frozen field. The `pyproject.toml`
configuration facts quoted alongside them **do** carry `file:line` and are unaffected. The
exclusion of `.venv`/`site-packages` is itself a property of that uncited inventory.

### S-A. `IBKR_PAPER_BRIDGE` — the Audit-2 product

- **Where:** `IBKR_PAPER_BRIDGE/tests`, **29** `test_*.py` files `[STATIC]`. Representative
  coverage across API, dry-run engine, risk, store, order state and lifecycle, broker and
  reconcile, Linux deploy and wrappers, release evidence, and WAL bundles `[STATIC]`.
- **Documented product command** (`IBKR_PAPER_BRIDGE\README.md:38-49`), verbatim:

  ```powershell
  cd C:\LAB\Tradingview_LAB_CLEAN
  $env:PYTHONUTF8 = "1"
  python -m pip install -r IBKR_PAPER_BRIDGE\requirements.txt
  python -m pytest IBKR_PAPER_BRIDGE\tests -q
  ```

- **Product memory states a different invocation contract:** the suite "must be run with CWD
  `IBKR_PAPER_BRIDGE` and `--ignore=TSP1009B.pytest_tmp_s1r1` — that directory is ACL-locked and
  plain `pytest` aborts collection with `PermissionError`."
  `MTC_COMMAND_CENTER\_AI_MEMORY\PROJECT_MEMORY.md:70-72`
- **Product layout for scope:** `bridge/{api,broker,engine,store}/`, `config/`, `deploy/linux/`,
  `docs/`, `tests/`, `requirements.{in,lock,txt}`; runtime entry `bridge/app.py`, FastAPI+uvicorn
  on loopback `127.0.0.1:8790`; startup fail-closed to DISARMED.
  `MTC_COMMAND_CENTER\_AI_MEMORY\PROJECT_MEMORY.md:56-60`
- **Historical invocations actually used** were `python -m pytest -q` with CWD
  `...\IBKR_PAPER_BRIDGE` (`GATE_A_INTEGRATION_AUDIT_ROUND1_EBADA020_2026-08-03.md:84-88`), and
  the same with `PYTEST_ADDOPTS='-p no:cacheprovider'`
  (`GATE_A_INTEGRATION_FLAGSHIP_AUDITS_EBADA020_2026-08-08.md:68-70`).

> **Reconciliation defect, stated now, to be resolved statically before any freeze.** Three
> descriptions of "the Bridge suite" disagree: README runs from the repository root with a path
> argument and no ignore flag (`README.md:46`); memory requires CWD `IBKR_PAPER_BRIDGE` plus
> `--ignore=TSP1009B.pytest_tmp_s1r1` and warns that the plain form aborts collection with
> `PermissionError` (`PROJECT_MEMORY.md:70-72`); the historical audit runs used CWD
> `IBKR_PAPER_BRIDGE` with no ignore flag and succeeded
> (`GATE_A_INTEGRATION_AUDIT_ROUND1_EBADA020_2026-08-03.md:84-88`). `[JUDGMENT]` The most likely
> explanation is that the ACL-locked directory appeared after 2026-08-03 and that CWD choice
> changes whether it is under the rootdir at all — but that is a hypothesis, not a measurement,
> and the reconciliation is a **no-test preflight** item, not an assumption.

### S-B. `01_MTC_PROJECT` — MTC V2

- `MTC_COMMAND_CENTER\01_MTC_PROJECT\00_PYTHON\pyproject.toml:1-8`: project `mtc-v2`,
  `requires-python = ">=3.11"`, `[tool.pytest.ini_options] testpaths = ["mtc_v2/tests"]`.
  **13** `test_*.py` files `[STATIC]`.
- Other `01_MTC_PROJECT` surfaces `[STATIC]`: root tests **2**; starter-kit tests **1**;
  `parity_oracles` tests **5**; tools tests **1**.

### S-C. `02_MTC_BACKTEST`

- `MTC_COMMAND_CENTER\02_MTC_BACKTEST\pyproject.toml:47-60`: `testpaths = ["tests"]`,
  `python_files = ["test_*.py"]`, `addopts = ["-v", "--tb=short", "--strict-markers"]`, and two
  declared markers — `slow` ("deselect with `-m \"not slow\"`") and `parity`
  ("marks tests that check TV↔PY parity"). **80** `test_*.py` files `[STATIC]`.
- `--strict-markers` (`:55`) means an unknown marker is an error, so any matrix runner that
  invents `-m` expressions here fails loudly rather than silently `[JUDGMENT]`.

### S-D. QuantLens

`[STATIC]` `tools/tests` **8**; **12** research strategy directories with **2** scaffold tests
each; **STG023–STG034** with **2** each; **STG046** with **3**.

### S-E. Dashboard

`[STATIC]` API tests **26**. A dated command exists in the Dashboard `PROJECT_HANDOFF.md` at
lines 7-15 and 37-49 per the bounded source map supplied with this task. **Scope caveat:** this
author did not open that file in this session, so the command text is not quoted here and no
`file:line` is asserted for its content. If Dashboard enters the mandated scope, that file must
be read and quoted before any freeze.

### S-F. Small surfaces

`[STATIC]` `mtc_cli/tests` **1**; `07_ADAPTERS/liveops/tests` **1**; `_deepseek_driver/tests`
**5**.

### S-G. Runner/CI configuration — a static absence

`[STATIC-ABSENCE]` The bounded path inventory found **no `.github/workflows`** and **no root
`pytest.ini`, `tox.ini`, `noxfile.py`, `setup.cfg`, `package.json` or `Makefile`**. No file is
cited for these, because there is no file to cite; inventing a citation is the defect class in
`DESIGN_DEFECT_PATTERNS_2026-08-10.md:645-653` (templates and non-existent paths presented as
exact commands). **Consequence: no named CI option exists.** A "run the CI configuration"
choice is not available to the owner, and the kickoff's third example option
(`KICKOFF_CODEX_MANDATED_SUITE_OPTIONS.md:34-36`) is therefore struck rather than offered.

### Cross-surface consequence

There is **no single rootdir** under which every surface above resolves: `01_MTC_PROJECT` and
`02_MTC_BACKTEST` each carry their own `[tool.pytest.ini_options]` with their own `testpaths`
(`00_PYTHON\pyproject.toml:7-8`, `02_MTC_BACKTEST\pyproject.toml:47-48`), and the Bridge's
required CWD is a third location (`PROJECT_MEMORY.md:70-72`). Any repository-wide option is
therefore necessarily a **multi-command matrix**, not one command — which collides directly with
`MANDATED_COMMAND=<exact command>`, singular
(`AUDIT2_AUDITOR_SESSION_INPUTS.md:92`).

---

## 4. The three options

### Option A — full `IBKR_PAPER_BRIDGE` suite at the frozen SHA *(recommended)*

**What it is.** One command, one rootdir, the Audit-2 product only: the Bridge suite of **29**
static test files `[STATIC]`, run at the pre-WP-A frozen SHA in each auditor's isolated
worktree, after a **static, no-test preflight** that reconciles the README invocation
(`IBKR_PAPER_BRIDGE\README.md:46`) against the CWD and `--ignore=TSP1009B.pytest_tmp_s1r1`
requirement (`PROJECT_MEMORY.md:70-72`) and against the historical invocations that carried a
plugin control (`GATE_A_INTEGRATION_FLAGSHIP_AUDITS_EBADA020_2026-08-08.md:68-70`).

**The preflight is static and produces a decision, not a run.** It must settle, by reading
bytes only: (1) exact CWD; (2) whether the ignore flag is required from that CWD or a no-op;
(3) whether a `no:randomly`-class plugin control belongs in the pinned invocation — the historical
runs pinned `-p no:cacheprovider` and any order-randomizing plugin present in the environment
would make a pass **set** reproducible but a pass **order** not, which matters only if the
adjudication depends on ordering `[JUDGMENT]`; (4) `PYTHONUTF8` and any other environment pin
implied by `README.md:44`.

- **Proves.** Cohesive breadth over the actual artefact under audit: the product whose layout,
  fail-closed startup, WAL store, schema and `deploy/linux/` package are the Audit-2 subject
  (`PROJECT_MEMORY.md:56-69`), and the product every historical Gate-A floor was measured
  against (H1–H9). It is the only surface with a **documented, repeatedly executed, auditor-
  reproduced** invocation.
- **Misses.** Every unrelated surface: MTC V2 (13), MTC backtest (80), QuantLens, Dashboard (26),
  and the small surfaces — `[STATIC]`/`[STATIC-UNCITED]` counts from §3, none carrying a
  `file:line`. If WP-I or the freeze touched anything
  outside `IBKR_PAPER_BRIDGE`, Option A does not exercise it.
- **Plausible duration.** `[JUDGMENT]` **about 2–4 minutes**, extrapolated from
  `[MEASURED-ELSEWHERE]` historical Windows runs: `136.91s` and `130.09s`
  (`GATE_A_INTEGRATION_RECORD_EBADA020_2026-08-03.md:136`), `136.00s`
  (`GATE_A_INTEGRATION_AUDIT_ROUND1_EBADA020_2026-08-03.md:120`), `222.05s`
  (`GATE_A_INTEGRATION_FLAGSHIP_AUDITS_EBADA020_2026-08-08.md:73`), `198.90s`
  (`GATE_A_PREREGISTRATION_ADDENDUM_C_2026-08-08.md:58-59`), `122.86s`
  (`GATE_A_DISARM_FIX_AUDIT_ROUND2_2CE41E34_2026-08-08.md:56`), `116.05s` and `145.53s`
  (`GATE_A_DISARM_FIX_AUDIT_ROUND2_2CE41E34_2026-08-08.md:12-13`). **The current runtime is
  unknown**; the spread already ranges 116–222s across machines at essentially the same count.
- **Stability of the pass set.** `[JUDGMENT]` The best of the three, and the only one with
  evidence for the judgment: the Windows runtimes listed just above, drawn from H1/H3/H4/H5/H7/H9
  across three SHAs, produced exactly two distinct counts, and the one transition (`1359`→`1360`) has a written, understood cause —
  one added test function (`GATE_A_PREREGISTRATION_ADDENDUM_D_2026-08-08.md:56-59`). A suite
  whose count changes only for reasons someone wrote down in advance is a suite whose anomaly
  set can be adjudicated.
- **How rc and the anomaly set become determinable.** Only by running §5 at the frozen SHA.
  Counts, rc and anomalies are **observed later** — this option does not supply them and this
  document does not predict them.

### Option B — frozen explicit WP-I / touched-surface subset

**What it is.** An explicitly enumerated list of test files or node IDs bound to what WP-I and
the freeze diff actually touched, frozen as `MANDATED_COMMAND`. The frozen file list and exact
base-to-freeze diff that would define "touched" are themselves Packet-10 components P10-02 and
P10-03 (`AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:54-55`), so this option **cannot even be
enumerated until the freeze exists**.

- **Proves.** That the changed surface passes. Nothing wider is claimed, which at least keeps the
  claim inside the probe (Pattern 9, `DESIGN_DEFECT_PATTERNS_2026-08-10.md:608-613`).
- **Misses.** Two distinct things. **Selection bias:** the set is chosen by the same party whose
  work is under audit, and an auditor cannot easily falsify the choice — this is Pattern 10's
  "evidence that cannot fail" applied to scope rather than to counts
  (`DESIGN_DEFECT_PATTERNS_2026-08-10.md:617-628`). **Hidden coupling:** a change in
  `bridge/store` or the schema-migration path can break a test nobody labelled as touched; the
  product's own memory records cross-cutting invariants — single `Store` per connection, one
  explicit `BEGIN IMMEDIATE` per mutating method, additive migrations with no downgrade
  (`PROJECT_MEMORY.md:61-65`) — which is precisely the kind of coupling a touched-file subset
  fails to cover.
- **Plausible duration.** `[JUDGMENT]` Fastest of the three, likely well under a minute for a
  small subset, scaling with the size of the selection. This is a planning estimate with **no
  historical measurement at all** behind it — no record in §2 measures a subset of this shape.
- **Stability.** `[JUDGMENT]` High for the selected members, precisely because it excludes
  whatever might move. That stability is bought by narrowing, not earned by coverage.
- **How rc and the anomaly set become determinable.** Same procedure as §5, but the frozen
  `MANDATED_COMMAND` must enumerate the members **literally and completely**; a command with an
  elided or descriptive selector ("the touched deploy tests") is the exact defect recorded at
  `DESIGN_DEFECT_PATTERNS_2026-08-10.md:645-653`. Additionally, P10-11's comparison would prove
  only that a chosen subset held, which the auditors must be told in the contract text.

### Option C — repository-wide ordered multi-command matrix

**What it is.** An ordered sequence of commands, one per rootdir: Bridge (29 files, own CWD),
`01_MTC_PROJECT\00_PYTHON` (`testpaths = ["mtc_v2/tests"]`, 13), `01_MTC_PROJECT` root/starter-
kit/parity-oracles/tools (2/1/5/1), `02_MTC_BACKTEST` (`testpaths = ["tests"]`, 80, with `slow`
and `parity` markers), QuantLens tools and strategy scaffolds, Dashboard API (26), and the three
small surfaces — all `[STATIC]` per §3, configuration at `00_PYTHON\pyproject.toml:7-8` and
`02_MTC_BACKTEST\pyproject.toml:47-60`.

- **Proves.** The broadest surface; nothing in the repository is silently exempt.
- **Misses / costs.**
  - **Contract mismatch.** `MANDATED_COMMAND=<exact command>` is singular
    (`AUDIT2_AUDITOR_SESSION_INPUTS.md:92`), as are `EXPECTED_EXIT_CODE`, the pass/fail counts and
    `BASELINE_SOURCE` (`:93-99`). A matrix needs per-command rc and per-command counts, so the
    contract fields must be **redefined by the owner**, not merely filled.
  - **No existing CI contract to inherit.** `[STATIC-ABSENCE]` per §S-G — there is no workflow,
    `tox.ini`, `noxfile.py` or `Makefile` encoding the intended order, so the matrix would be
    **authored for this audit** and would have no prior green run to compare against.
  - **Multi-environment instability.** `[JUDGMENT]` Surfaces differ in interpreter requirement
    (`requires-python = ">=3.11"` at `00_PYTHON\pyproject.toml:5`), dependency sets, and marker
    strictness (`--strict-markers` at `02_MTC_BACKTEST\pyproject.toml:55`). Whether every surface
    even *collects* in one environment is unmeasured, and a collection failure is a STOP, not a
    result (Pattern 1, `DESIGN_DEFECT_PATTERNS_2026-08-10.md:48-52`).
  - **Includes protected parity.** `02_MTC_BACKTEST` declares a `parity` marker for "tests that
    check TV↔PY parity" (`02_MTC_BACKTEST\pyproject.toml:59`) and a `slow` marker (`:58`).
    Parity work is a separately governed concern, and dragging it under an Audit-2 gate means an
    unrelated parity drift can BLOCK the Audit-2 dispatch.
- **Plausible duration.** `[JUDGMENT]` **Unknown and slowest.** No record in §2 measures any
  non-Bridge surface. Bridge alone is 2–4 minutes; the remaining ~145 static files
  (`[STATIC-UNCITED]`, §3) include an
  explicitly `slow`-marked class (`02_MTC_BACKTEST\pyproject.toml:58`). Stating a figure here
  would be a fabricated measurement.
- **Stability.** `[JUDGMENT]` Lowest. Broadest surface, most environments, no prior green
  baseline, and each additional surface adds independent failure modes to a set that must be
  **byte-identical across two auditors and one rerun** under §5.
- **How rc and the anomaly set become determinable.** §5 must be run **per command**, and the
  two-way set equality must hold per command **and** over the union. Practically, the owner would
  be authorizing N baselines, not one.

### Comparison

| | A — Bridge full | B — touched subset | C — repo-wide matrix |
|---|---|---|---|
| Commands to freeze | 1 | 1 (explicit member list) | N, one per rootdir |
| Proves | the audited product, whole | only the changed surface | everything |
| Principal risk | unrelated surfaces unproven | selection bias + hidden coupling | instability, no CI contract, protected parity |
| Duration | ~2–4 min `[JUDGMENT]`, historical 116–222s `[MEASURED-ELSEWHERE]` | fastest, unmeasured `[JUDGMENT]` | unknown/slowest `[JUDGMENT]` |
| Prior green evidence exists | yes, multiple runs across three SHAs (§2, H1/H3/H4/H5/H7/H9) | none | none |
| Fits `MANDATED_COMMAND` singular | yes | yes | **no — requires contract change** |

---

## 5. The anomaly gate — how an anomaly set becomes *observed*

This is the procedure that makes P10-12 an observation rather than a copied number. It applies
unchanged to A, B or C. An empty anomaly set is a legal outcome **only** if it is produced by
this procedure. `AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:64`,
`KICKOFF_CODEX_MANDATED_SUITE_OPTIONS.md:39-42`

1. **Freeze the conditions before running.** The pre-WP-A SHA; the exact command string; the
   exact CWD; the exact interpreter (absolute path and version); the dependency lock actually
   installed; every environment and plugin control (`PYTHONUTF8`, `PYTEST_ADDOPTS`, any `-p
   no:` disables); and the platform. Historical practice already recorded a plugin control in
   the invocation line (`GATE_A_INTEGRATION_FLAGSHIP_AUDITS_EBADA020_2026-08-08.md:68-70`), and
   the locked Linux runs recorded interpreter and SQLite versions before use
   (`GATE_A_INTEGRATION_RECORD_EBADA020_2026-08-03.md:142-143`). Record these **before** the
   run, not reconstructed after it.
2. **Run only under authorization, in a clean isolated worktree.** The worktree contract
   requires a separate worktree per flagship, exact-HEAD equality, the resolved worktree path,
   and empty pre- and post-run `git status --porcelain`
   (`AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:65`;
   `AUDIT2_HANDOFF_PACKAGE.md:76-77`, `:79-80` — non-empty cleanliness proof returns BLOCK).
3. **Retain byte-exact output.** Full stdout, full stderr, and rc, stored with byte count and
   SHA-256 — the record contents P10-11 demands
   (`AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:63`).
4. **Capture the terminal counts *and* the exact identities.** Not just "2 failed" but every
   `FAILED`, `ERROR`, `SKIP`, `XFAIL` and `XPASS` node ID with its output signature. The
   historical preregistration already enforced identity over count: "any third failure, or any
   failure whose node ID is not one of those two … A different node ID is a FAIL even if the
   count is still two." `GATE_A_PREREGISTRATION_ADDENDUM_B_2026-08-08.md:66-67`
5. **Adjudicate each member against a source-linked authority.** For every non-passing ID, the
   record must name why it is accepted and cite the source that accepts it. An unadjudicated
   member is not an accepted anomaly.
6. **Rerun independently and require two-way set equality.** A second identical run under the
   identical frozen conditions, then set equality in **both directions** between run 1 and run 2
   — no member in one that is absent from the other. Independent reproduction is the repository's
   established habit (`GATE_A_INTEGRATION_AUDIT_ROUND1_EBADA020_2026-08-03.md:82-92`), and the
   same record warns that a pasted value is a claim to re-measure, never a measurement
   (`:96-100`).
7. **Empty only if both runs observed empty.** If and only if both runs produced a non-passing
   set of size zero may `EXPECTED_FAIL_COUNT` be recorded as `0`. Otherwise every accepted member
   is listed explicitly, by ID and signature.
8. **Inability to evaluate is STOP, never a result.** A collection error, an ACL
   `PermissionError` of the kind `PROJECT_MEMORY.md:70-72` describes, a missing dependency, or a
   worktree that fails its cleanliness proof is a STOP condition. It is not a pass, not an
   accepted failure, and not an empty anomaly set. Pattern 1,
   `DESIGN_DEFECT_PATTERNS_2026-08-10.md:48-52`; and per
   `AUDIT2_AUDITOR_SESSION_INPUTS.md:102-104`, non-execution is not acceptance.
9. **Freeze `BASELINE_SOURCE` by path, byte count and hash** at the frozen SHA
   (`AUDIT2_AUDITOR_SESSION_INPUTS.md:99`), so that what the auditors compare against is
   identified as an object, not as a remembered number.

**Then, and only then, P10-11.** Each required auditor executes the same frozen
`MANDATED_COMMAND` in its own worktree and compares its observed non-passing set against the
frozen baseline set **in both directions** — a missing expected member is as much a finding as an
unexpected new one (`AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:63`;
`GATE_A_PREREGISTRATION_ADDENDUM_B_2026-08-08.md:66-67`).

**Nothing in steps 1–9 has been performed.** This document records the gate; it does not open it.

---

## 6. Lead recommendation, and what the owner is being asked to decide

**Recommendation: Option A.** It is the only choice that is simultaneously *singular* — one
command, one CWD, one rc, one baseline, which is exactly the shape the contract's fields assume
at `AUDIT2_AUDITOR_SESSION_INPUTS.md:92-99` — and *evidenced*: multiple independent Windows runs
of this same suite across three SHAs are on record (§2, H1/H3/H4/H5/H7/H9; note that H3, H4 and
H10 partly retell runs already counted elsewhere, so no exact run tally is asserted), spanning
the recorded 116.05s to 222.05s, and the
only count transition in that entire history has a written, preregistered cause, one added test
function (`GATE_A_PREREGISTRATION_ADDENDUM_D_2026-08-08.md:56-59`). That matters more than
breadth, because what P10-10 needs is not the largest possible pass set but a set whose members
change only for reasons someone can name in advance; a baseline that drifts for unexplained
reasons cannot support the two-way set-equality comparison P10-11 requires. Option B buys speed
by letting the audited party draw its own scope, which is Pattern 10 applied to scope rather than
to counts (`DESIGN_DEFECT_PATTERNS_2026-08-10.md:617-628`) and which the product's own
cross-cutting store and migration invariants make genuinely risky
(`PROJECT_MEMORY.md:61-65`). Option C is the honest maximalist answer and it is the one I would
choose if a CI contract existed — but none does (`[STATIC-ABSENCE]`, §S-G), so its ordering,
environments and expected results would all be authored for this audit with no prior green run,
it needs the singular `MANDATED_COMMAND` field redefined, and it drags separately governed
TV↔PY parity (`02_MTC_BACKTEST\pyproject.toml:59`) inside a gate that can BLOCK the Audit-2
dispatch. Option A's real cost is stated plainly and not minimised: it proves nothing about the
other test files outside the Bridge — on the order of 145 by the `[STATIC-UNCITED]` inventory of
§3, a figure with no `file:line` behind it and one to re-derive rather than rely on — and if the
freeze diff reaches
outside `IBKR_PAPER_BRIDGE`, A must be revisited rather than quietly stretched to cover it.

### The owner ask

**Barış is asked to decide two things, and only these:**

1. **Scope: A, B, or C.** This is a decision about the *contract* — which surface the two
   flagships are bound to execute. **It is not a decision about counts**, and no count is
   requested, offered or implied here.
2. **If A: authorize freezing the exact CWD and command string after the static reconciliation
   in §4/Option A is complete.** That reconciliation resolves README (`README.md:46`) versus
   product memory (`PROJECT_MEMORY.md:70-72`) versus historical invocation
   (`GATE_A_INTEGRATION_AUDIT_ROUND1_EBADA020_2026-08-03.md:84-88`), including whether the
   `--ignore=TSP1009B.pytest_tmp_s1r1` flag and any plugin disable belong in the frozen string.
   It is a bytes-only preflight; it runs no test.

**Not being asked, and not decidable now:** `EXPECTED_EXIT_CODE`, `EXPECTED_PASS_COUNT`,
`EXPECTED_FAIL_COUNT`, `EXPECTED_FAILURE_1/2`, `EXPECTED_SKIP_XFAIL_COUNTS`. Those become
determinable only by executing §5 at the frozen SHA, under separate authorization, after the
pre-WP-A checkpoint exists (`AUDIT2_HANDOFF_PACKAGE.md:165-168`;
`AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:119-120`).

**P10-10 remains unwritten.** This file is options only. P10-11 and P10-12 remain gaps behind it.
`AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:71`
