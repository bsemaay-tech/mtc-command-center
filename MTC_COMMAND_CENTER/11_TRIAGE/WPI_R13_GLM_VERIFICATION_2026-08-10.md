I have read all four input files in full. Below is my read-only verification report. (Per audit-mode rules I have created, modified, and deleted zero files; this text is the report.)

---

# WP-I round 1.3 closure verification — report

## Verdict

- **F3 (B2/B4 system-manager access failure misread as host drift): CLOSED**
- **F4 (B3 partial `find` output inspected before adjudicating walk failure): CLOSED**

Both closure targets are genuinely closed as written. No regression to F1/F2/F5/F6. The two residual items at the end of this report are nits, not defects.

---

## Answer 1 — F3 closed?

**Yes.** Walking B2/B4 with the audit's three access-failure shapes (D-Bus/polkit denial, `systemctl` absent, or the login in a PID/mount namespace without the system manager):

**At P0 (section 8.1), the stage now stops before any unit-state/property probe exists:**
- Row 6 (`WPI_PREREGISTRATION_DRAFT.md:367`): `command -v systemctl` must resolve, else `P0_STOP reason=missing_tool tool=systemctl`. An absent `systemctl` never reaches B2/B4.
- Row 7 (`:368`): a *separate* readiness gate that `systemctl` "can execute, reach the intended system manager over its system bus from the login's PID/mount namespace, pass D-Bus/polkit authorization, and return a parseable manager response", else `P0_STOP reason=system_manager_unreachable`. Lines 377-380 make explicit that tool presence is insufficient and that a namespace/auth/parse failure routes manager-backed B2/B4 to RPD-VERIFY rather than accusing the host.

**Per-row, a could-not-evaluate arm is reached before every comparison:**
- Row 1 active (`:386`): `B2_STOP reason=system_manager_unreachable operation=is-active` for invocation/bus/namespace/auth/parse failure **first**; only after reachability is proven may a *valid* `inactive` become `B2_FAIL reason=unit_not_active` — and this is explicitly decoupled from numeric rc (lines 455-458). An empty/error `is-active` result has no valid state, so it is STOP, not FAIL.
- Row 2 NRestarts (`:387`), Row 3 Restart (`:388`), Row 4 MainPID (`:389`): `B2_STOP reason=unit_property_unreadable prop=... before comparison`; "only a successfully read value may become B2_FAIL".
- Row 5 candidate binding (`:390`): `B2_STOP reason=unit_definition_unreadable operation=cat ... before stdout interpretation on any ... incomplete-output or parse error`; only a complete rendering may FAIL.
- Row 8 sandboxing (`:393`): `B4_STOP reason=unit_property_unreadable prop=<P> ... before comparison`.
- Row 9 start mode (`:394`): `B4_STOP reason=unit_property_unreadable prop=Environment ... before stdout interpretation`.

**General-list gap closed.** The audit's specific complaint — "the general STOP list at lines 405-407 does not include `systemctl`" — is fixed: the list at `:521-524` now names `systemctl` and "system-bus query", and the System-manager adjudication rule (`:450-460`) restates the precedence in full.

**Row that can still yield a FAIL on an access failure: none.** I checked every manager-backed row (1-5, 8-9); each gates its FAIL behind a STOP, and an incomplete/error result is routed to STOP/DEFER-ROOT-SIDE, not FAIL. Rows 6-7 (B2 fragment) are direct file reads, not manager probes; their access errors are F5 hash/read STOPs and are also intact.

## Answer 2 — F4 closed?

**Yes.** With the audit's scenario (world-writable path emitted early by `find -perm /222`, then EACCES and nonzero exit later):

- The rows were **reordered**: row 12 budget (`:397`) -> row 13 walk completeness (`:398`) -> row 14 write bits (`:399`). Row 13 fires `B3_STOP reason=walk_permission_error` (ACL/LSM/permission) or `walk_incomplete` (any other nonzero rc / mount / traversal / diagnostic error) on the EACCES + nonzero exit, and row 13 states this "disqualifies rows 14 and 19".
- Row 14 admits `B3_FAIL reason=writable_path_inside_immutable_tree` **only** "from stdout of a sweep already proven complete"; "partial stdout is discarded as result evidence and can produce only the row-12/13 STOP". So the early writable pathname cannot accuse a correct host.
- The binding order is stated generically in the Atomic-walk adjudication rule (`:424-432`): capture stdout/stderr/rc/elapsed without streaming stdout to a parser; adjudicate (1) timeout/budget, (2) exit status + complete diagnostic stream, (3) only then stdout. Any LSM/ACL/mount/permission/traversal diagnostic or nonzero rc is STOP.

**Generality.** The rule is not limited to the cited row. The Atomic rule covers "every filesystem walk, including the immutable-tree write-bit sweeps **and any metadata enumeration feeding row 19**", and the General probe-output precedence rule (`:462-469`) extends the same capture-then-adjudicate order to every interpreted stdout (`stat`, `find`, `grep`, `ss`, `curl`, `sha256sum`, `readlink`, `systemctl`, `mktemp`, verifier). Stage-1 block acceptance (`:218-228`) now requires an adversarial transcript: a writable-pathname-then-traversal-error fixture must yield `B3_STOP`, never `B3_FAIL`.

**Places that still interpret stdout without first adjudicating status: none left uncovered.** The only rows that interpret a command's stdout without restating the status-first order *inline* are B5 rows 20-21 (`:405-406`, curl). They are covered by the binding General rule (`:462-469`), which explicitly names `curl` and "invocation/access errors". See nit #2.

## Answer 3 — Regression check

**No regression. No truthful caveat dropped.**
- **F1** intact: row 19 preflight readability precondition (`:404`), Metadata-readability adjudication rule (`:435-448`), binding ordering rule (`:411-422`), TSV B1 row (`WPI_CHECK_FEASIBILITY.tsv:13`).
- **F2** intact: row 22 namespace-binding preflight (`:407`), Namespace-binding rule (`:479-497`), TSV B6 row (`:19`).
- **F5** intact: row 7 `fragment_unreadable` with rc-0-before-compare (`:392`); row 17 `installed_lock_unreadable` (`:402`); TSV B2/B1a notes (`:14-15`).
- **F6** intact and the specific caveat the question names is preserved verbatim in spirit: the three pre-dispatch items are "necessary but not sufficient" with the two added gates — **explicit written host-contact/transport authority** and **the required budget lift** — and `-Execute`/`-Confirm` are called out as technical interlocks, not authority (`:34-43`, restated `:310-316`). `SELF_QA.md:497-499` reaffirms this remains necessary before any successor is dispatchable.
- The B2/B4 class changes are a **tightening** (INCLUDE-READ-ONLY only after P0 readiness, else DEFER-ROOT-SIDE), not a weakening; the direct-fragment half of B2 stays unprivileged.

## Answer 4 — Honesty check

`SELF_QA.md` round 1.3 (`:458-505`) is accurate. I verified every substantive change-claim against the draft and TSV:
- systemctl presence + query readiness added to P0 -> draft `:367-368`. ✓
- Readiness covers invocation/bus/namespace/auth/parse; tool presence insufficient -> `:368`, `:377-380`. ✓
- Per-row STOP tokens (`system_manager_unreachable`/`unit_property_unreadable`/`unit_definition_unreadable`) before each FAIL -> `:386-394`. ✓
- inactive-as-evaluable-FAIL decoupled from numeric rc -> `:386`, `:455-458`. ✓
- General STOP list now names systemctl + system bus -> `:521-524`. ✓
- B2/B4 reclassified `partial` with the split, direct fragment half stays unprivileged -> TSV `:15,17`; DEFER-ROOT-SIDE list `:587-590`. ✓
- F4: atomic capture, three-step order, row reordering (12-13 before 14), row-14 "proven complete rc-0" gate, generalization to metadata enumeration + all interpreted stdout, Stage-1 adversarial-transcript requirement -> `:397-399`, `:424-432`, `:462-469`, `:218-228`. ✓

**Claim I cannot verify against the deliverables:** the provenance statement at `SELF_QA.md:501` ("Read only `KICKOFF_ROUND13_F3F4.md`, ..."). The kickoff file is not in my Inputs, so I cannot confirm what was read. This is a process statement, not a correctness claim, and none of the substantive change-claims depend on it. Not a defect.

## Answer 5 — Placeholder discipline

**Confirmed clean.** No concrete one-use RUNID, date-stamped unit id, or collision-prone record root was minted:
- RUNIDs are `<ALLOCATE-AT-DISPATCH>-P0`/`-RO` (`:92-94`); unit id `<ALLOCATE-AT-DISPATCH>` (`:5`); roots `/home/gatea/wpi_staging_<ALLOCATE-AT-DISPATCH>` (`:101`) and `C:\WPI_ARTIFACTS\WPI_TRANSPORT_<ALLOCATE-AT-DISPATCH>` (`:296`).
- The burned RUNID `WPLP2-...-B3` (`:88`) and the two Stage 2/3B record roots (`:119-121`, `:298-299`) are historical references used for burn/collision rules, exactly as the audit's own answer 4 sanctioned.
- `WPI_UNIT_FRAGMENT_SHA256` is elided as `<PIN-BEFORE-DISPATCH>` (`:138`) with an explicit never-derive-at-run-time statement (`:155-158`). Candidate/lock/reused-block hashes are inputs or pinned-from-history, not new one-use ids.

---

## Findings (ranked; both nits)

**N1 (nit) — Dangling sentence fragment in the Atomic-walk rule.**
`WPI_PREREGISTRATION_DRAFT.md:433`. After the complete rule ends at `:432` ("...exposes stdout for writable-path or metadata interpretation."), line 433 is the orphan fragment `a parity FAIL.` — an incomplete sentence, almost certainly a leftover from an edit (the intended parity-FAIL gating already exists fully at `:435-448` and row 19 `:404`). No functional impact: the rule is complete in `:424-432` and reinforced by row 14/row 19 and the Metadata-readability rule, so no implementer is misled. *No concrete failure scenario* — labeling this a nit per the task's rule. Worth a one-line cleanup so a future reader does not read the fragment as a dropped condition.

**N2 (nit) — B5 rows rely on the general rule rather than restating curl-status adjudication inline.**
`WPI_PREREGISTRATION_DRAFT.md:405-406` (rows 20-21). Row 20's named divergence `status_endpoint_http code=<c>` presupposes curl returned an HTTP code; a curl-level failure (connection refused / timeout / DNS — nonzero rc, *no* code) has no row-specific STOP token and falls back to the binding General probe-output precedence rule (`:462-469`, which names `curl` and "invocation/access errors") and the TSV's "curl probe errors are STOP" (`WPI_CHECK_FEASIBILITY.tsv:18`). The behavior is still STOP-first, so this is **not a defect** — it is an asymmetry with the F3/F4-hardened rows, which restate the order inline. *No concrete failure scenario in which a curl access error becomes a B5 FAIL* — nit. (Raising only because Answer 2 asks for any stdout-interpreting row that lacks inline status adjudication; B5 is the sole such row, and it is covered by the general rule.)

---

**Bottom line:** F3 and F4 are closed; the audit's named mislabelings (`unit_not_active`, `unit_not_bound_to_candidate`, property mismatch, and `writable_path_inside_immutable_tree` from a partial walk) are each now gated behind a STOP that fires on the access/traversal failure before any comparison or stdout interpretation. Earlier-round protections (F1/F2/F5/F6, including the authority-and-budget caveat) are intact, `SELF_QA.md` round 1.3 is accurate, and placeholder discipline holds. Only two documentation nits remain, neither of which reopens either finding.
