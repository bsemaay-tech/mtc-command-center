# WP-P0-13 `TrialRecord` catalog writer — DESIGN DRAFT v2.3

**[SUPERSEDED IN v2.2 — W296; retained v2.1 title follows.]**

# WP-P0-13 `TrialRecord` catalog writer — DESIGN DRAFT v2.1

**[SUPERSEDED IN v2.1 — W287; retained v2.0 title follows.]**

# WP-P0-13 `TrialRecord` catalog writer — DESIGN DRAFT v2.0

## v2.3 change log — FOLD-P013 T330 F01 (addendum 32 "for example")

T330 cross-family census triage confirmed finding F01: the strategy TYPE list `day` / `swing` /
`position` was stated as a closed, exhaustive list at two sites (the v2.2 change-log owner quotation
and the NEW-BY-ADDENDUM-32 design item), while owner addendum 32 uses "for example", making the
list illustrative. Two AMENDMENT-CHOICE paragraphs are inserted after the cited sites, quoting the
owner's "for example" phrase from `ADDENDUM_32.md:38`. The retained wording is superseded: the three
types are examples of the owned strategy TYPE policy categories, the list is not closed, and any
type the owner names later is admitted under the same rule. No line is deleted; the header version
is bumped v2.2 → v2.3. (`T330_EXTRACT.md`; `ADDENDUM_32.md:38`)

## v2.2 change log — W296 owner addendum 32 decision 128

Owner addendum 32 supersedes only the row-6 selection ruling applied in v2.1; decision 88 and B-12's
settings-retention disposition are untouched. The controlling owner words for decision 128 are:

> "Do not choose winners using one score alone. Require all safety and quality checks first, then rank
> by overall robustness.
>
> Keep the best 20 candidates separately for each strategy type—for example, day trading, swing
> trading, and position trading—so one type does not crowd out another.
>
> Keep any tied candidates at the cut-off as well."

**AMENDMENT-CHOICE (FOLD-P013, owner addendum 32 "for example", 2026-09-03).** The retained wording above is superseded: the three types `day`, `swing`, and `position` are examples of the owned strategy TYPE policy categories, the list is not closed, and any strategy type the owner names later is admitted under the same rule. Owner addendum 32, verbatim: "for example, day trading, swing trading, and position trading" (`ADDENDUM_32.md:38`).

The v2.1 decision-87 text and every consequence it introduced are retained. The B-07 primary site now
tags that decision as superseded and makes the current selected universe the best 20 separately for
strategy TYPE `day`, `swing`, and `position`, after all safety and quality checks, ranked by overall
robustness, with every cut-off tie retained. The old market/timeframe partition and the old automatic
keep union of risk-versus-return, promoted, robust, and pinned groups are no longer current selection
authority. Their existing row flags remain independently produced facts; none is deleted or silently
repurposed. B-07 remains open for the P0-13 build owner to encode the versioned policy, owned
strategy-type binding, robustness comparison, cut-off-tie semantics, policy-version/evidence binding,
and the still-required lifecycle/pin flag authorities. No number, identity, field, or producer is
minted. (`C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:837-876,900-912`;
§2.1 stage 4; §3.2; §7 B-07)

**Cross-draft echo.** The rev-2 census assigns no X-group to row 6; P0-13's existing X-1 participation
belongs to B-12 and is unchanged by decision 128. Addendum 32 nevertheless introduces a structural
echo across the sibling designs: P0-20 carries versioned policy settings and fresh relevant evidence
on change under decision 127; P0-21 carries strategy-type-specific, versioned minimum/forward-evidence
rules under decisions 129-130; P0-13 consumes the same strategy TYPE and policy-version/evidence
structure when applying decision 128. The unset sibling values remain `OWNER-ANSWERED-SHAPE, VALUE
PENDING (addendum 32)`: per-type leverage caps; swing/position minimum trade counts; day forward
period and trade count; swing/position calendar period; “meaningful number”; and the count of “normal
market conditions”. P0-13 also appears in X-10 with its identity-without-a-recipe engineering items and
their sibling drafts; decision 128 supplies no identity recipe and changes none of those sites. No
sibling draft is edited here. (`C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:856-898,902-928`;
`C:\tmp\LANE_PROMPTS_20260828\W269_PHASE0_OWNER_QUESTIONS.md:622-695`)

This change log records design only. Nothing in W296 or addendum 32 authorizes live trading, a build,
or a code change.

## v2.1 change log — W287 owner addendum 31 decisions 87–88

The owner answered the two P0-13 halves on the Phase-0 page. This fold applies each answer once at its
named blocker, retains the prior blocker text, and leaves the engineering half open where the answer
does not supply a contract or producer. The 11 blocker headings and three discrepancy headings do not
change, so open items remain **14**. No code, schema, identity preimage, producer, repository byte, build,
fixture, run, or artifact is produced here.

| Decision | Owner's verbatim words | v2.1 disposition |
|---|---|---|
| **Owner addendum 31 decision 87 (2026-09-02), row 6** | "Use a combined quality rule, not one score. Keep the top 20 per strategy, market, and timeframe; also keep the best risk-versus-return group, promoted items, robust items, and anything I pin." | **B-07 OWNER HALF CLOSED.** The keep-rule shape and exact top count are fixed. B-07 remains open only for the engineering-owned versioned policy encoding and delivery/binding of the authoritative lifecycle and pin records; this decision supplies no scalar score, comparison formula, policy version, or new identity. (`C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:737-745`; §7 B-07) |
| **Owner addendum 31 decision 88 (2026-09-02), row 7** | "Keep settings for every saved trial." | **B-12 OWNER HALF CLOSED.** The keep-all-settings storage direction is ratified for conserved rows, selected and unselected. B-12 remains open on its engineering half: the WP-P0-04 contract owner must ratify the exact canonical `preregistered_space_hash` preimage and sole identity function; the answer supplies neither. (`C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:737-745`; §7 B-12) |

**Cross-draft echo — X-1.** B-12 is the P0-13 site in X-1. The same engineering preimage contract is
carried by `P014_DESIGN_DRAFT_V1.md` DS52-B02 (and its mapping) and `P022_DESIGN_DRAFT_V1.md` OQ-4.
Decision 88 closes only P0-13's split-out storage-versus-proof owner limb; it does not close or narrow
the shared canonical-byte question in any of the three drafts. Decision 87 has no X-group in the rev-2
census. (`C:\tmp\LANE_PROMPTS_20260828\W269_PHASE0_OWNER_QUESTIONS.md:112-122,624-629,690-695,834-835`)

## v2.0 change log — W241 partial apply of the GM66 census

The GM66 census returned four findings. Three exact-anchor hunks applied and one stopped. GM66-F01's
supplied CURRENT block does not match the draft byte-for-byte: the patch wraps after “six”, while the
draft wraps after `ContractModel` and carries the start of the sentence after earlier text on the same
line. The hunk was not hand-adjusted, so **B-16 was not opened** and the inheritance/member-count
ambiguity remains for the next patch author. GM66-F02 opens **B-17** because the reader has no committed
expected-coordinate operand; GM66-F03 corrects the stale gate cell; GM66-F04 puts the prose-only Hive
routing gate into the table. Open blockers move **10 → 11**, open discrepancies stay **3**, and total
open items move **13 → 14**. B-12 and B-15 remain open and unchanged.
(`C:\tmp\LANE_PROMPTS_20260828\DS79_P013_PATCH.md:47-75`;
`C:\tmp\LANE_PROMPTS_20260828\DETECT_GM66_P013.md:12-85`)

| Finding | Severity | Disposition | v2.0 result |
|---|---:|---|---|
| **GM66-F01** — view-preimage inheritance and exact member count are ambiguous | HIGH | **STOPPED — supplied CURRENT bytes do not match** | No source text was hand-adjusted, no B-16 was opened, and the ambiguity remains live. (§4.2.1; `C:\tmp\LANE_PROMPTS_20260828\DS79_P013_PATCH.md:47-72`) |
| **GM66-F02** — R-8 lacks a committed expected-coordinate operand | HIGH | **APPLIED — B-17 OPENED** | R-8 now says the check cannot be performed from committed bytes, retains the superseded promise, and asks where the independent committed operand lives. (§5.4; §7 B-17) |
| **GM66-F03** — gate-table cell contradicts §6 controlling text | MEDIUM | **APPLIED** | The v1.8 clause is retained and tagged; the live v2.0 clause agrees that F-6 runs no R arm while B-15 is open. (§6) |
| **GM66-F04** — Hive routing gate is missing from the table | LOW | **APPLIED** | The existing prose remains and the same gate now has a table row. (§6) |

**What v2.0 does not claim.** The stopped F01 hunk is not a repair. This design still does not choose a
base class or member count for either view preimage type. B-17 does not invent committed storage; it
opens the missing-storage question. No code, schema, writer, build, fixture, run, artifact, repository,
or Git state was produced by this lane.

## v1.9 change log — W215 residual sweep of the v1.8 fold

The G104 verification of the W203 fold returned one finding: the v1.8 change-log bullet counts **five**
relabelled while its own disposition table lists **six**. This lane fixes that side of the disagreement
and then sweeps the classes that finding belongs to across the whole of v1.8, because a verifier
enumerates what it saw and the next lane must sweep the class. Two further defects were found by that
sweep and are recorded below. **No blocker is opened and none is closed; open items stay at 13.**
(`C:\tmp\LANE_PROMPTS_20260828\DETECT_G104_P013_FOLD.md:1-20`;
`C:\tmp\LANE_PROMPTS_20260828\LANE_W215_P013_RESIDUAL.md:1-56`)

| Finding | Severity | Disposition | v1.9 repair |
|---|---:|---|---|
| **G104-F01** — the v1.8 change-log bullet says five relabelled while its own disposition table lists six | MEDIUM | **FIXED — the bullet was the wrong side** | Counted from the v1.8 table's own Disposition column: **G102-F01, F02, F03, F05, F06, and F07 read RELABELLED** and **G102-F04 reads WITHDRAWN** — six and one. Two other sites already said six: the fold report's verdict, and §9's v1.8 entry condition, which names “the six v1.8 repairs”. The change-log bullet was the only site carrying five, so the bullet is the wrong side; its v1.8 wording is retained and tagged beside the correction rather than deleted. (Change log, v1.8 bullet) |
| **W215-F02** — B-15's consequence was applied to F-13 and R-8 only, but its open channel blocks every arm that begins from a committed package | MEDIUM | **RECORDED — the consequence is widened; no new blocker, nothing assembled** | §4.1's layout puts `strategy=`, `symbol=`, and `timeframe=` in **every** part path, and §4.1's own v1.8 status says “no path containing them may be derived”, so while B-15 is open no committed package exists at all. v1.8's “F-4, F-10, R-1, and R-3 are unaffected” (§5.3) and “R-1..R-7 are unaffected by B-15” (§5.4) are therefore too narrow, as are §6's “runs R-1..R-7 today” and §4.2.2's live v1.7 sentence that the path/receipt cell check “remains separately specified”. §§4.2.2, 5.3, 5.4, and 6 now state the rule — an arm is blocked by B-15 wherever its input is a staged or committed Parquet part, a commit receipt, or the candidate/published view — and apply it: **F-1, F-4, F-5, F-6, F-7, F-10, F-11, F-12, F-13 and R-1..R-8** are blocked; the writer-boundary probes **F-2, F-3, and F-8**, which refuse before any part is staged, are not; **F-9** is recorded as undecided and handed to the reviewer rather than counted either way, because its committed bytes are the artifact tree, which carries no routing segment. B-15's question is unchanged, no blocker is opened, and no channel is named to make this go away. (§4.1; §4.2.2; §5.3; §5.4; §6; §7 B-15) |
| **W215-F03** — “the 0-hit contracts grep for every coined name” was measured over five names | LOW | **MEASURED — the grep is completed and the claim holds** | The v1.8 change-log cell for G102-F07 claims a 0-hit contracts grep for **every** coined name. §8 item 10 recorded a grep of five names, only three of which are in its own coined list, and the fold report records the same five. This session greps every name in that coined list — `document_version`, `publication_version`, `CatalogCommitPreimageV1`, `PublishedViewSchemaDocumentV1`, `ViewPublicationPreimageV1`, `RunCellDimensionsFactory`, `CommittedPathCellInspector`, `PathReceiptCellComparer`, `COMMIT_PREIMAGE_MEMBER_MISSING`, `PATH_RECEIPT_CELL_MISMATCH` — plus `CompletedRunInput`, `DuckDBViewPublisher`, `RunCellDimensionsReceipt`, `CatalogCommitIdentity`, `TrialCatalogViewSchemaProjector`, `CommittedDuckDBSchemaInspector`, and `DuckDBSchemaFingerprintComparer`, under `MTC_COMMAND_CENTER/`: **0 hits each**. The claim was true; it is now the measured one. (§8 item 10) |

**Retention completed, not a finding of its own.** §4.2.1's SQL-whitespace matrix row is tagged
“retained v1.7 cell” but retained only the v1.7 **Outcome** word; the v1.7 **Why** sentence was
rewritten in place with no struck-through retention. It is restored beside the v1.8 text, quoted from
the verification that recorded it (`C:\tmp\LANE_PROMPTS_20260828\DETECT_G102_P013_CLOSURES.md:101`).
No other retained span was found shortened, tidied, or missing: the whole file was compared byte for
byte against `C:\tmp\LANE_PROMPTS_20260828\SNAPSHOTS\20260902_0120\P013_DESIGN_DRAFT_V1.md`, which is
identical to the pre-W215 draft, and every v1.8 retention was compared against the verification that
quoted the superseded wording.

**What v1.9 does not claim.** Three defects were not treated as a quota and neither was finding fault:
the v1.8 body repairs were re-read and left standing, and every count in the document was recomputed
from its own rows. **B-12 is still open and untouched** — this lane wrote nothing in §7 B-12, proposed
no recipe, and named no candidate field set anywhere. **B-15 is still stated as a question**, not
answered: v1.9 widens what its open channel blocks and does **not** name the member that would close
it. Correcting a count and widening a consequence does not make the writer buildable: **B-04** and
**B-12** still leave two required non-null `TrialRecord` identities with no emittable value, **B-01**
still gates build, and **B-15** is still open. No repository byte was written by this lane.

## v1.8 change log — W203 fold of the G102 closure verification

A different family verified the four v1.7 blocker closures and returned seven findings — five HIGH,
two MEDIUM. Five of the seven say a version of one thing: the closures **assembled** member sets, a
type vocabulary and a producer input, and presented them as already-written. That is the
manufactured-preimage defect the closures existed to prevent, reappearing inside the closures. This
fold does not answer any finding by assembling a better set. Where something was assembled, v1.8 says
so; where an input was assembled, v1.8 withdraws it and opens a blocker.
(`C:\tmp\LANE_PROMPTS_20260828\DETECT_G102_P013_CLOSURES.md:12,18-123`)

| Finding | Severity | Disposition | v1.8 repair |
|---|---:|---|---|
| **G102-F01** — B-13 type vocabulary is not “exactly the distinct spellings already present” | HIGH | **RELABELLED — the vocabulary is defined here** | The eight-word list is unchanged and no new dialect word is added, but the claim that it was already present was false: §3.2 also spells `dictionary VARCHAR`, `canonical-JSON VARCHAR`, and `canonical decimal VARCHAR`. §4.2.1 item 5 now states the collapse rule P0-13 applies (physical type word only; annotation and length qualifier dropped), names what is already-written versus what this design adds, and adds a matrix row making the annotation class **ACCEPTED, not DETECTED**. (§4.2.1) |
| **G102-F02** — `document_version` / `publication_version` are new preimage members with no value, type, or producer | HIGH | **RELABELLED — both coined here, now fully specified** | Neither member is withdrawn and no member list is replaced. Each is labelled a v1.8 design act inherited from nothing, and given a type (`NonEmptyStr`), a sole producer, the fixed literal `"1"`, and a change rule that a different member set needs a new type name. Both are listed for re-audit. (§4.2.1; §9) |
| **G102-F03** — `ContractModel` injects a seventh member; the cited lock does not detect omission | HIGH | **RELABELLED — repository opened and the finding confirmed** | `base.py:59-67` is the class statement and `ConfigDict`; `base.py:69` declares defaulted `contract_version`; `canonical_json` serializes via `model_dump` (`identity.py:16-17`). The member contract is corrected to *six declared members plus the inherited `contract_version`, and no others*, the cite is re-pointed, and the fact that the inherited member's omission is **filled, not refused** is stated as an ACCEPTED-not-DETECTED limit instead of being left to R-7 to imply. (§4.1.3; §7 B-10) |
| **G102-F04** — B-14's sole producer reads fields `CompletedRunInput` does not declare | HIGH | **WITHDRAWN — blocker B-15 opened** | Confirmed by opening the files: `CompletedRunInput` has **0 repository hits**, and the draft's own §2.1 field list declares no cell coordinate while §4.1.3 marks all three routing values absent by design. v1.8 refuses to add three members to `CompletedRunInput` to close it. The sentence is withdrawn and **B-15 `RUN-CELL-COORDINATE-CHANNEL`** asks: *through which declared member of the closed `CompletedRunInput` do the run's `strategy`, `symbol`, and `timeframe` cell coordinates reach `RunCellDimensionsFactory`?* B-14's authority answer is not re-opened. (§3.4.3; §7 B-14; §7 B-15) |
| **G102-F05** — live v1.6 controlling text still asserts B-10/B-14 block; D-03 still exposes routing values from a run envelope | HIGH | **RELABELLED — both sites tagged, plus one more found by this fold's own sweep** | §3.4.2's untagged v1.6 disposition and D-03's v1.5 channel sentence are retained, tagged, and given v1.8 controlling text. A third site the G102 report scored elsewhere is now tagged too: §2.1's “the run envelope” collides in name with §4.1.3's closed `run_envelope`, and the collision is recorded rather than resolved by assembly. (§2.1; §3.4.2; D-03) |
| **G102-F06** — SQL-whitespace DETECTED, but the SQL producer is also the hash producer | MEDIUM | **RELABELLED — the check does not exist, so the matrix now says so** | The cell is changed from DETECTED to **NOT DETECTED by any named check**, with the reason stated: `DuckDBViewPublisher` produces both operands, §4.2.2's reader does not recompute `view_publication_hash`, and no arm changes only whitespace. A note separates the matrix rows that have an independent comparer from those that do not. No reader-side recompute is promised: a prose promise of a check is not a check. (§4.2.1; §5.3) |
| **G102-F07** — the change log presents assembled v1.7 member sets as already-written artefacts | MEDIUM | **RELABELLED — the banner is replaced by an explicit split** | “No preimage, field, dialect, owner, or storage location was invented” and “v1.7 still invents nothing” are retained, tagged, and replaced by §8 item 10, which lists already-written artefacts with the file and line each was verified at, and lists what this design assembles or coins — including the 0-hit contracts grep for every coined name. The change-log bullet below says the same thing. **[v1.9 — W215-F03:]** the grep behind that phrase covered five names, three of which are in the coined list; §8 item 10 now records the grep of every name in that list, all **0 hits**. **[v1.9 — G104-F01:]** the change-log bullet below said five relabelled where this table says six, and is corrected there. (§8 item 10) |

**What v1.8 does not claim.** Seven findings were not treated as a quota, and neither was finding
fault: **B-12 is still open and untouched** — no recipe, no narrowing, no candidate field set appears
anywhere in this fold — and B-11's storage answer, B-13's recipe *pick*, B-14's authority frame, and
the R-7/R-8/F-13 failing inputs were re-read and left standing, because the verification confirmed
them. No finding was refuted: all seven were checked against the draft or the repository and all seven
held, though F04's shape needed the repository to settle. Correcting four closures does not make the
writer buildable: **B-04** and **B-12** still leave two required non-null `TrialRecord` identities with
no emittable value, **B-01** still gates build, and **B-15** is new. No repository byte was written by
this fold.

## v1.7 change log — W198 blocker close (G99 unfenced audit)

The G93 fold opened B-10 through B-14 from inside a two-file fence. An unfenced audit read the
places that fence excluded — the contracts package, the canonical plan, the architecture brief, the
WP-P0-08 writer inventory, and `P012_FRESH_DESIGN_V1.md` v1.9 — and found four of the five closable
by a P0-13 design lane and one genuinely the owner's. This lane closes the four and leaves the fifth
untouched. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_G99_BLOCKERS.md:11-21,87-89`)

| Blocker | v1.6 state | v1.7 disposition | What closes it |
|---|---|---|---|
| **B-10** `CATALOG-COMMIT-PREIMAGE-MEMBERSHIP` | OPEN | **CLOSED in v1.7; corrected in v1.8 (G102-F03) — the member contract is six declared members plus the inherited `contract_version`, and the `base.py:59-67` cite is re-pointed** | §4.1.3 gives item 2 of `CatalogCommitPreimageV1` a typed closed run-envelope field list — every member marked required or absent-by-design — built from the six already-written `compute_evaluation_run_hash` members and the already-written v1.5 candidate list, serialized by the already-written repository `canonical_json`. Sole envelope producer `EvaluationIdentityFactory`; sole digest producer `CatalogCommitIdentity`. No new field and no new dialect is minted. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:31-44,76-95`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G99_BLOCKERS.md:31-33`) |
| **B-11** `EVALUATION-PREIMAGE-COMMITTED-STORAGE` | OPEN | **CLOSED in v1.7** | The same §4.1.3 envelope is the committed home: all six members are required members of the run envelope inside the preimage, and the receipt already committed at `commits/<catalog_commit_hash>.json` already stores the exact preimage, so the bytes exist for every conserved trial, selected or not. No `TrialRecord` column is added, `ArtifactManifest` is not used, and no third JSON is invented. R-3 is re-pointed at the stored members. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:76-95`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G99_BLOCKERS.md:41-43`) |
| **B-12** `PREREGISTERED-SPACE-HASH-PREIMAGE` | OPEN | **REMAINS OPEN — UNTOUCHED IN v1.7 AND IN v1.8** | The unfenced audit reached the same verdict the fold did: nothing outside the fence supplies a closed field set or a sole identity function, and a lane that minted one would commit the manufactured-preimage defect the blocker exists to prevent. B-12's text, its `TrialRecord` producer cell, and every claim gated on it are unchanged in v1.7. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_G99_BLOCKERS.md:51-55,81`) |
| **B-13** `VIEW-SCHEMA-AND-PUBLICATION-PREIMAGE` | OPEN | **CLOSED in v1.7; corrected in v1.8 (G102-F01/F02/F06) — the type vocabulary is defined here rather than inherited, `document_version` and `publication_version` are coined here and now specified, and the SQL-whitespace cell reads NOT DETECTED** | §4.2.1 picks **one** of the two already-written digest recipes — repository `canonical_json` plus SHA-256 — cites why the other was not picked, closes `PublishedViewSchemaDocumentV1` over the already-frozen §3.2/§3.3/§3.4.1 column list in table order with the nested struct kept nested, closes the `view_publication_hash` preimage, names `DuckDBViewPublisher` as sole producer of the published SQL bytes, and states the DETECTED-versus-accepted outcome for whitespace and for type spelling. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:31-44`; `MTC_COMMAND_CENTER/contracts/README.md:48-55`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G99_BLOCKERS.md:61-63`) |
| **B-14** `ROUTING-VALUE-SOLE-PRODUCER` | OPEN | **CLOSED in v1.7 on the authority question; successor blocker B-15 opened in v1.8 (G102-F04) — the factory's declared input is withdrawn, so the three Hive segments and F-13/R-8 are blocked design targets again** | §3.4.3 names `RunCellDimensionsFactory` as sole producer of a typed three-value receipt whose authority is the completed run's own cell coordinates — the strategy × symbol × timeframe cell the sole canonical emitter already writes one result per — plus `CommittedPathCellInspector`, `PathReceiptCellComparer`, typed `PATH_RECEIPT_CELL_MISMATCH`, F-13, and R-8: the same producer/observer/comparer shape already used for `run_id` without a blocker. P0-13 does **not** name itself the authority. `TrialRecord` gains no field; B-03/D-03 are untouched. (`MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_08_WRITER_INVENTORY_2026-08-25/WRITER_INVENTORY.md:35,102`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G99_BLOCKERS.md:71-73`) |

**What v1.7 does not claim.** Closing four blockers does not make the writer buildable. `TrialRecordAssembler`
still cannot construct a row while **B-04** (`param_hash` preimage) and **B-12** (`preregistered_space_hash`
preimage) leave two required non-null `TrialRecord` identities with no emittable value, so no commit,
no publication, and no fixture arm downstream of row assembly can execute; **B-01** still gates build on
WP-P0-20 acceptance. What v1.7 changes is that the commit preimage, the committed evaluation-preimage
home, the two schema fingerprints, `view_publication_hash`, and the three routing values are now
*specified* rather than *unspecified* — the arms that were blocked design targets for want of a byte
formula or a value authority are now specified design targets blocked only by the identity blockers
above. **[v1.8 amendment, G102-F04:]** the three routing values are the exception — they are a blocked
design target again under **B-15**, because §3.4.3's factory has no declared input, so F-13 and R-8
join `preregistered_space_hash` and `param_hash` among the arms that may not be constructed.
Self-references in this change log use stable section anchors, not line numbers, because a
fold moves them. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:24,28`; §2.1 private stage 3
v1.6 controlling design; §7 B-01, B-04, B-12)

## v1.6 change log — G93 fold

| Review finding | Severity | Disposition | v1.6 repair |
|---|---:|---|---|
| G93-F01 — `CatalogCommitPreimageV1` was not a closed byte preimage | HIGH | **REPAIRED — B-10 OPENED; B-10 CLOSED IN v1.7 (§4.1.3); MEMBER CONTRACT CORRECTED IN v1.8 (G102-F03)** | Retained and tagged the v1.5 formula as superseded, withdrew the claim that the run-envelope member set is closed, and made `catalog_commit_hash` unavailable until the exact required/absent-by-design envelope membership is ratified. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:52-86`) |
| G93-F02 — read-side `evaluation_run_hash` recompute had no committed preimage | HIGH | **REPAIRED — B-11 OPENED; B-11 CLOSED IN v1.7 (§4.1.3)** | Retained and tagged the out-of-band read-side claim, pinned the six repository formula members, and blocked the reader plus R-3 until an owned committed home exists for every member for every trial. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:88-120`) |
| G93-F03 — `preregistered_space_hash` had no preimage and no blocker | HIGH | **REPAIRED — B-12 OPENED; B-12 STILL OPEN AND UNTOUCHED IN v1.7** | Withdrew `SearchFamilyRegistry` as a sufficient hash producer and prohibited emission until the search-family owner ratifies the exact canonical preimage and sole identity function. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:122-142`) |
| G93-F04 — one module declared the universe and proved conservation | MEDIUM | **REPAIRED** | Replaced the self-comparison with an expected-universe projector, a committed-row inventory, and a comparer in neither module; F-11 makes a missing member and a deleted comparison independently RED. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:144-171`) |
| G93-F05 — path/row `run_id` agreement had no comparer or failing input | MEDIUM | **REPAIRED** | Added independent row/path producers, `PathRowRunIdComparer`, typed `PATH_ROW_RUN_ID_MISMATCH`, F-12, and R-6. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:173-202`) |
| G93-F06 — schema fingerprints and `view_publication_hash` had no byte formula | MEDIUM | **REPAIRED — B-13 OPENED; B-13 CLOSED IN v1.7 (§4.2.1); CORRECTED IN v1.8 (G102-F01/F02/F06)** | Retained and tagged the v1.5 identities as superseded and prohibited either digest until the exact schema-document and SQL byte preimages, serialization, storage, and SQL-normalization producer are ratified. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:204-233`) |
| G93-F07 — P0-20 citations had drifted | MEDIUM | **REPAIRED** | Retained and tagged every stale pointer, re-pointed supported claims to the current battery/build-design v1.5 spans, and removed battery authority where the current document does not define the field. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:235-266`) |
| G93-F08 — `strategy`/`symbol`/`timeframe` had no sole value producer | MEDIUM | **REPAIRED — B-14 OPENED; B-14 CLOSED IN v1.7 (§3.4.3); SUCCESSOR B-15 OPENED IN v1.8** | Kept the Hive path as a physical channel but withdrew the run envelope as an unnamed value authority; publication is blocked until an owner-produced typed receipt and equality check are ratified. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:268-291`) |

## v1.5 change log — G61 fold

| Review finding | Severity | Disposition | v1.5 repair |
|---|---:|---|---|
| G61-F01 — expected DuckDB view schema differed from the published SQL projection | MEDIUM | **FOLDED** | Froze the published-view contract to the columns the §4.2 SQL actually produces: the `TrialRecord` row/nested fields, Hive `lineage`/`strategy`/`symbol`/`timeframe`, and the filename-derived `catalog_commit_hash`. The path `run_id` must agree with the row's single logical `run_id`; receipt-only metadata is explicitly excluded from the view fingerprint. The observed producer now inspects only the candidate view projection, and F-10 starts from the production SQL template and changes only that projection. **v1.6 note:** this row's self-cite carried v1.5 line numbers that the v1.6 fold moved, so it is re-pointed to stable section anchors — §2.1 private stage 9, §3.4 through §3.4.2, §4.2, and fixture F-10 in §5.3. The G61-F01 producer separation survives v1.6; only the digest emission is now blocked on B-13. |

## v1.4 change log — G42 fold

| Review finding | Severity | Disposition | v1.4 repair |
|---|---:|---|---|
| G42-F01 — DuckDB schema-fingerprint comparison did not name both producers | MEDIUM | **FIXED** | Named `TrialCatalogViewSchemaProjector` as the sole expected-fingerprint producer, `CommittedDuckDBSchemaInspector` as the sole observed-fingerprint producer, and `DuckDBSchemaFingerprintComparer` as the comparer that emits neither operand. The design explicitly refuses deriving the expected fingerprint from the committed parts or view being inspected, and F-10 supplies the discriminating changed-projection input plus a deleted/degenerate-check RED arm. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_G42_P013_V13.md:54-91`) |
| G42-F02 — `has_full_artifacts=false` had no named producer or failing input | MEDIUM | **FIXED** | `ArtifactCommitVerifier` now emits exactly one flag for every conserved `trial_id`: `true` only for a selected, identity-matched committed artifact set and `false` only for an unselected trial with no committed selected-artifact address. The Pydantic default cannot supply the value; every inconsistent combination is refused. F-9(e) and F-9(f) respectively refuse an unselected row changed to `true` and a selected identity-matched row changed to `false`. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_G42_P013_V13.md:93-133`) |

## N81 round-3 fold disposition

| Review finding | Severity | Disposition | v1.3 repair |
|---|---:|---|---|
| N81-F01 — selected-artifact `trial_id` disappears before committed-byte verification | MEDIUM | **FIXED** | Added blocker **B-09** and discrepancy **D-04**; the selected-artifact address is now per trial (`artifacts/<package_hash>/<trial_id>/`), the committed `manifest.json` carries `trial_id` plus dependent identities under a WP-P0-04 schema-owner binding, and `ArtifactCommitVerifier` compares the committed address and manifest identity against the independent row identity from `IdentityValidator`, never against the upstream `SelectedArtifactPayloadReceipt`. Fixture **F-9** proves two selected trials sharing a `package_hash` commit to distinct addresses and that an overwrite, address/manifest swap, missing committed identity, or duplicate address is refused. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_N81_P013_V12.md:7-12`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:67,77-87`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:54-73,132-135`)

## W77 round-2 fold dispositions

| Review finding | Disposition | v1.2 repair |
|---|---|---|
| P34-N1 — stale companion cite `PLAN:503` | **FIXED** | The screening permission now cites only `PLAN:509-511`. (`C:\tmp\LANE_PROMPTS_20260828\AUDIT_P34_P013_V11.md:183-193`)
| P34-N2 — writer-inventory cite landed early | **FIXED** | The no-current-catalog-writer statement now cites the verified `WRITER_INVENTORY.md:98-105` range. (`C:\tmp\LANE_PROMPTS_20260828\AUDIT_P34_P013_V11.md:195-201`)
| P34-N3 — `family_size` cite low bound off by one | **FIXED** | The BLOCK-context citation now begins at line 299. (`C:\tmp\LANE_PROMPTS_20260828\AUDIT_P34_P013_V11.md:203-209`)
| P34-N4 — header finding count was ambiguous | **FIXED** | The header now says `Open items` and, after the N70-F04 status correction, reports 7 blockers plus 2 open discrepancies; it does not call them draft defects. (`C:\tmp\LANE_PROMPTS_20260828\AUDIT_P34_P013_V11.md:211-218`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_N70_P013_V11.md:28-33`)
| N70-F01 — no discriminating typed fixture for the acceptance reader | **FIXED** | `AcceptanceEvidenceReader` now emits one closed five-reason refusal taxonomy and R-1..R-5 make each check individually load-bearing with all other conditions valid; R-3 is the committed preimage mismatch, while writer-boundary F-8 stays separate. **v1.6 note:** the taxonomy is now six reasons and the reader fixtures are R-1..R-6; see §5.2 and §5.4. **v1.7 note:** the taxonomy is now eight reasons and the reader fixtures are R-1..R-8; `COMMIT_PREIMAGE_MEMBER_MISSING` and `PATH_RECEIPT_CELL_MISMATCH` were added with R-7 and R-8, and no previously blocked R arm remains blocked on B-10, B-11, or B-13. **v1.8 note:** the taxonomy count is unchanged at eight, but `PATH_RECEIPT_CELL_MISMATCH` is an unavailable reason and R-8 is a blocked design target while **B-15** leaves `PathReceiptCellComparer` without one of its two operands. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_N70_P013_V11.md:7-12`; §7 B-15)
| N70-F02 — self-referential `catalog_commit_hash` | **FIXED** | The hash now covers a canonical `CatalogCommitPreimage` that excludes the hash and hash-bearing final paths; staged part bytes contain no commit hash. Final paths and receipt fields are derived and independently checked, and the DuckDB view projects the hash from the filename. **v1.6 note:** the non-self-referential *shape* survives, but G93-F01 showed the preimage was not in fact closed — the envelope member set was permissive — so the hash, the derived final paths, and this row's “now covers” claim are withdrawn until B-10 and B-13 close; see §4.1.2. **v1.7 note:** B-10 and B-13 are closed, so the hash, the derived final paths, and the “now covers” claim are restored on the closed member set in §4.1.3; the non-self-referential shape is unchanged and the DuckDB view still projects the hash from the filename. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_N70_P013_V11.md:14-19`)
| N70-F03 — missing/ambiguous output producers | **FIXED** | Typed selected-artifact payload receipts, a manifest builder, a byte-only committer, a separate verifier, and one idempotent `DuckDBViewPublisher` now have explicit inputs/outputs and modified-copy probes. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_N70_P013_V11.md:21-26`)
| N70-F04 — historical implementer status treated as current | **FIXED** | B-02 and open discrepancy D-01 are closed: repository merge records show WP-P0-04 PASS with zero findings and WP-P0-08 T2 PASS-WITH-NITS with zero required findings. (`git-object:fead492b0b87f207aa6e7a259372b9767d4301f9:7,17-19`; `git-object:88eab9c93b7c285b990d07502ea1ec476034e8d5:7,9-14`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_N70_P013_V11.md:28-33`)

## Prior G18 fold dispositions (retained)

| G18 finding | Disposition | v1.1 repair retained/extended in v1.2 |
|---|---|---|
| G18-F01 — the structural stamp omitted the `evaluation_run_hash.simulator_class` preimage | **FIXED** | `LineageClassifier` locks the class before identity work; `EvaluationIdentityFactory` consumes that locked value; the writer refuses a legacy receipt pre-bound to another class in F-8, while reader fixtures R-3/R-4 independently discriminate the committed evaluation and dependent-trial checks. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_G18_P013_DRAFT.md:15-54`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_N70_P013_V11.md:7-12`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:76-95,132-135`)
| G18-F02 — caller-label probe relied on `extra="forbid"` against a known `TrialRecord` field | **FIXED** | The public seam now accepts a closed `CompletedRunInput` that omits and explicitly reserves lineage/routing keys; F-2 targets that boundary, not `TrialRecord`. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_G18_P013_DRAFT.md:56-84`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:57`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/base.py:59-67`)
| G18-F03 — module-count comparison had both operands from one producer | **FIXED** | The table now flags `modules_enabled_count == len(modules_enabled)` as **LIMITATION—SAME-PRODUCER CONSISTENCY ONLY**, never independent completeness proof; a second source remains P0-04-owned. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_G18_P013_DRAFT.md:86-103`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:70-74`)
| G18-F04 — P0-20 paper pointers had drifted | **FIXED** | All six affected field/boundary citations were re-pointed to the then-current v1.1 paper or the still-BLOCK audit; the paper remains context, not accepted authority. **v1.6 note:** that battery paper is now **v1.5**, so `P020_STATISTICAL_BATTERY_DEFINITION_V1.md:1-4` no longer reads as v1.1; G93-F07 re-pointed the affected cites a second time and they are listed in the v1.6 change log above. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_G18_P013_DRAFT.md:105-138`; `C:\tmp\LANE_PROMPTS_20260828\P020_STATISTICAL_BATTERY_DEFINITION_V1.md:1-4`; `C:\tmp\LANE_PROMPTS_20260828\AUDIT_P19_P020_PAPERS.md:1-4`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:235-266`)
| G18-F05 — producer-separation lesson cited a rotating handoff | **FIXED** | Normative citations now point to durable Pattern 10; the handoff is no longer the authority for this rule. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_G18_P013_DRAFT.md:140-156`; `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:617-628,681-687`)

## Change log

- **v2.2 (2026-09-03, W296 amendment fold).** Layered owner addendum 32 **decision 128** over the
  retained addendum-31 decision 87 at B-07. The current rule requires all safety and quality checks
  before robustness ranking, then keeps the best 20 separately for strategy TYPE `day`, `swing`, and
  `position`, including every cut-off tie. The v2.1 market/timeframe partition and automatic keep union
  of risk-versus-return, promoted, robust, and pinned groups are retained as superseded history; the
  corresponding row flags remain independent facts. B-07's owner half stays closed, while the P0-13
  build owner still owes the versioned policy/type/evidence encoding and the lifecycle/pin flag
  authorities. `NEW-BY-ADDENDUM-32` records the shared P0-20/P0-13/P0-21 strategy-type and versioned
  policy/evidence structure; P0-20 carries decision 127 and P0-21 carries decisions 129-130. X-1 and
  decision 88 are unchanged. Open items remain **14**. (`C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:837-928`;
  §2.1 stage 4; §7 B-07; §7 B-12)
- **v2.1 (2026-09-02, W287 owner-answer fold).** Applied owner addendum 31 **decision 87** at B-07
  and **decision 88** at B-12. Decision 87 closes only the owner keep-rule shape: combined rather than
  one score, top 20 per strategy/market/timeframe, plus the best risk-versus-return group, promoted,
  robust, and pinned items. The engineering-owned versioned policy encoding and authoritative
  lifecycle/pin-record delivery remain open under B-07. Decision 88 ratifies settings retention for
  every saved trial, while the WP-P0-04-owned canonical preimage bytes and sole identity function
  remain open under B-12. X-1 siblings P0-14 DS52-B02 and P0-22 OQ-4 continue to carry that same
  engineering preimage dependency; neither decision closes them. Open items remain **14**. No code,
  schema, identity preimage, producer, repository byte, build, fixture, run, or artifact was produced.
  (`C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:737-745`;
  `C:\tmp\LANE_PROMPTS_20260828\W269_PHASE0_OWNER_QUESTIONS.md:112-122,624-629,834-835`; §7 B-07;
  §7 B-12)
- **v2.0 (2026-09-02, W241 GM66 patch apply).** Applied GM66-F02, GM66-F03, and GM66-F04: opened
  B-17 for the missing committed expected-coordinate operand; retained and corrected the stale v1.8
  acceptance-gate clause; and added the Hive-routing gate to the §6 table. GM66-F01 **stopped** because
  the patch's CURRENT block did not match the draft byte-for-byte; it was not hand-adjusted, so no B-16
  was opened and the view-preimage base-class/member-count ambiguity remains. Open blockers **10 →
  11**, open discrepancies stay **3**, total open items **13 → 14**. B-12 and B-15 remain open and
  unchanged. No repository byte, code, schema, writer, build, fixture, run, or artifact was produced.
  (`C:\tmp\LANE_PROMPTS_20260828\DS79_P013_PATCH.md:47-116`;
  `C:\tmp\LANE_PROMPTS_20260828\DETECT_GM66_P013.md:12-85`)
- **v1.8 (2026-09-02, W203 G102 closure fold).** Folded all seven G102 findings on the v1.7 closures: **[SUPERSEDED IN v1.9 — G104-F01; retained v1.8 count:]** “five relabelled honestly, one withdrawn to a new blocker, none refuted.” **v1.9 correction:** the disposition table at the head of this change log records **six relabelled** — G102-F01, F02, F03, F05, F06, F07 — **one withdrawn to a new blocker** (G102-F04), and **none refuted**; five plus one plus zero was six of seven, and the bullet, not the table, was the wrong side. **What this design defines rather than inherits is now said at each site and here:** the §4.2.1 type vocabulary and the collapse rule that produces it; `document_version` and `publication_version`, both coined here and now given a type, a sole producer, the literal `"1"`, and a change rule; the six-member run envelope, whose contract is corrected to *six declared members plus the inherited `contract_version`* after opening `base.py` and finding the defaulted field at `base.py:69` that the cited `base.py:59-67` span does not mention. **Withdrawn:** §3.4.3's claim that `RunCellDimensionsFactory` reads cell coordinates “carried on the closed `CompletedRunInput`” — §2.1 declares no such member and v1.7 had emptied the envelope they previously rode in — opening **B-15 `RUN-CELL-COORDINATE-CHANNEL`** rather than adding three members to the boundary type. **Withdrawn checks:** SQL-whitespace “DETECTED” becomes NOT DETECTED, because the SQL producer is also the hash producer and no reader recomputes `view_publication_hash`; the annotation-collapse class is recorded as ACCEPTED; omission of the inherited `contract_version` is recorded as filled rather than refused. **Residual sweep:** §3.4.2's untagged v1.6 “B-10 blocks / B-14 separately blocks” paragraph and D-03's “exposes them from a run envelope” sentence are retained, tagged, and superseded; §2.1's run-envelope name collision is recorded. Every superseded sentence is retained with its version and finding id. Open items 12 → **13**; open blockers 9 → **10**. B-12 remains open and untouched. No repository byte, code, schema, writer, build, fixture, or run was produced. (`C:\tmp\LANE_PROMPTS_20260828\LANE_W203_P013_CLOSURE_FOLD.md:1-46`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G102_P013_CLOSURES.md:12,18-123`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/base.py:12,62-67,69,71-78`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:16-17,76-95`)
- **v1.7 (2026-09-02, W198 blocker close).** Closed **B-10**, **B-11**, **B-13**, and **B-14** using recipes, formulae, column tables, receipts, and cell dimensions that were already written outside the two-file fence the G93 fold worked inside; left **B-12** open and untouched because nothing supplies a closed field set or a sole identity function for it. Added §3.4.3 (routing-value factory, inspector, comparer, typed reason), §4.1.3 (closed commit-envelope member table and its committed home), and §4.2.1 (one chosen digest recipe, closed schema document, closed publication preimage, sole SQL producer, DETECTED/accepted matrix). Extended the closed acceptance-reader taxonomy from six reasons to eight and added F-13, R-7, and R-8. Every superseded v1.6 blocking note is retained and tagged, not deleted. **[SUPERSEDED IN v1.8 — G102-F07; retained v1.7 sentence:]** “No preimage, field, dialect, owner, or storage location was invented: each closure names an already-written artefact and its sole producer.” **v1.8:** that sentence was not accurate. The closures assembled a member set, a type vocabulary, two version members, and a producer input; §8 item 10 lists what is already-written with the line each was verified at, and what this design assembles or coins. Open items 16 → 12 in v1.7, then 12 → 13 in v1.8. Build remains blocked on B-01, and row assembly remains blocked on B-04 and B-12. No repository byte, code, schema, writer, build, fixture, or run was produced. (`C:\tmp\LANE_PROMPTS_20260828\LANE_W198_P013_BLOCKER_CLOSE.md:1-40`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G99_BLOCKERS.md:11-21,31-33,41-43,51-55,61-63,71-73`)
- **v1.6 (2026-09-01, W191 + W194 G93 fold).** Provenance: lane W191 began this fold and halted inside §5 when its provider returned a usage-limit error, leaving §§1–4 folded and §§5–9 at their v1.5 text; no W191 report was written and v1.6 was never emitted as a completed state. Lane W194 re-read the census and the partially folded body and completed §§5–9 — the six-reason reader taxonomy, F-11, F-12, R-6, the blocked-arm and blocked-gate notes, the §6 conservation and path/row `run_id` rows, blockers B-10 through B-14, the retirement of “presently BLOCK” in B-01, the open-item count, and the §8/§9 version and blocker-range text. Repaired all eight G93 findings: **G93-F01**, **G93-F02**, **G93-F03**, **G93-F04**, **G93-F05**, **G93-F06**, **G93-F07**, and **G93-F08**. Five repairs open honest blockers B-10 through B-14 rather than inventing missing preimages, committed storage, or routing-value authority; G93-F04 and G93-F05 now have independent producers/comparers and discriminating modified copies; G93-F07 now points to the current P0-20 battery/build-design v1.5 state. The proposed cross-document digest convention was not cited as authority. No repository byte, code, schema, writer, build, fixture, or run was produced. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:38-46,52-291`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_GM43_ROOT_CAUSE.md:18-92`)
- **v1.5 (2026-08-31, W158 G61 fold).** Folded G61-F01. The frozen published-view schema now matches the actual §4.2 SQL channels; commit-receipt-only metadata is no longer projected as expected view columns, Hive `lineage` is explicit, path/row `run_id` coexistence is defined, the observed fingerprint comes only from the candidate view visible to queries, and F-10's GREEN baseline is the production SQL template. The independent producers and same-producer-degenerate refusal remain. No schema, API, or physical join was invented. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_G61_P013_V14.md:50-163`)
- **v1.4 (2026-08-31, W124 G42 fold).** Folded both G42 MEDIUM findings. The DuckDB schema check now has independent expected and observed fingerprint producers plus a comparer that produces neither operand, explicitly refuses the same-producer-degenerate design, and has discriminating fixture F-10. `ArtifactCommitVerifier` now emits `has_full_artifacts` for every conserved trial on both the selected/`true` and unselected/`false` paths; F-9(e) and F-9(f) make both flag directions load-bearing and forbid reliance on the Pydantic default. Open items remain 11 (8 blockers, 3 discrepancies); no owner-gated value changed and every **PROVISIONAL-ON-P020** label remains. Build remains gated on WP-P0-20 acceptance. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_G42_P013_V13.md:41-48,54-133`)
- **v1.3 (2026-08-30, W94 N81 round-3 fold).** Folded the one N81 MEDIUM. Gave each selected trial one collision-free committed address (`artifacts/<package_hash>/<trial_id>/`) and one committed identity operand (`trial_id` plus dependent identities in `manifest.json`) so `ArtifactCommitVerifier` compares committed bytes against the independent row identity rather than reusing the upstream payload receipt as both operands; added blocker B-09 for the required WP-P0-04 schema-owner manifest/path binding, discrepancy D-04, and fixture F-9 (two selected trials with the same `package_hash`). Open items 9 → 11 (8 blockers, 3 discrepancies). No P0-20 choice changed; every **PROVISIONAL-ON-P020** label is retained and B-09 is not itself P0-20-gated. Build remains gated on WP-P0-20 acceptance. (`C:\tmp\LANE_PROMPTS_20260828\LANE_W94_P013_FOLD3.md:1-16`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_N81_P013_V12.md:7-12,37-41`)
- **v1.2 (2026-08-30, W77 round-2 fold).** Closed all four P34 citation/wording nits and all four N70 findings: added typed one-check reader fixtures, defined a non-self-referential commit preimage and filename projection, named the DuckDB and selected-artifact producers, and replaced stale implementer snapshots with the repository merge acceptance records. DS7 was not folded because `C:\tmp\LANE_PROMPTS_20260828\DS7_RUN.log` was absent when W77 started. Every P0-20-dependent choice remains **PROVISIONAL-ON-P020**; build remains gated on WP-P0-20 acceptance. (`C:\tmp\LANE_PROMPTS_20260828\LANE_W77_P013_FOLD2.md:1-12`; `C:\tmp\LANE_PROMPTS_20260828\AUDIT_P34_P013_V11.md:181-218`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_N70_P013_V11.md:3-33`)
- **v1.1 (2026-08-30, W64 G18 fold).** Folded all five G18 findings without claiming acceptance or build authority: locked lineage before identity formation, closed the caller input, added a mismatched-preimage fixture, flagged the same-producer module-count limitation, corrected P0-20 pointers, and replaced rotating handoff citations with durable Pattern 10 citations. Every P0-20-dependent choice remains **PROVISIONAL-ON-P020**; build remains gated on WP-P0-20 acceptance. (`C:\tmp\LANE_PROMPTS_20260828\LANE_W64_P013_DRAFT_FOLD.md:1-12`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G18_P013_DRAFT.md:3-9`)

**[SUPERSEDED IN v1.6 — retained v1.5 verdict text:]** **Verdict:** **DESIGN DRAFT COMPLETE; BUILD BLOCKED.** This is design only: it authorizes no code, schema, writer, repository, Git, run, or artifact-generation change. WP-P0-13 build remains after WP-P0-20 acceptance and this draft must be re-audited after that acceptance. (`C:\tmp\LANE_PROMPTS_20260828\LANE_W51_P013_DESIGN.md:8-12,43-46`)

**[SUPERSEDED IN v1.7 — retained v1.6 verdict text:]** **Verdict:** **DESIGN DRAFT REPAIRED; BUILD BLOCKED.** This is design only: it authorizes no code, schema, writer, repository, Git, build, fixture execution, run, or artifact-generation change. WP-P0-13 still depends on WP-P0-20, and B-10 through B-14 additionally prevent implementation from inventing the missing identities, storage, or routing authority. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:409-417,483-510`; `C:\tmp\LANE_PROMPTS_20260828\P020_BUILD_DESIGN_V1.md:1-10`)

**[SUPERSEDED IN v1.8 — W203 G102 fold; retained v1.7 verdict text:]** **Verdict:** **DESIGN DRAFT REPAIRED; BUILD BLOCKED.** This is design only: it authorizes no code, schema, writer, repository, Git, build, fixture execution, run, or artifact-generation change. WP-P0-13 still depends on WP-P0-20 through B-01. B-10, B-11, B-13, and B-14 are closed in v1.7 by naming already-written recipes and producers; **B-12 remains open and untouched**, and together with B-04 it still leaves two required non-null `TrialRecord` identities with no emittable value, so no row may be assembled and no commit or publication may occur. The remaining open blockers continue to prevent implementation from inventing the missing identities. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:409-417,483-510`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:24,28`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G99_BLOCKERS.md:51-55,87-89`)

**[SUPERSEDED IN v1.9 — W215 residual sweep; retained v1.8 verdict text:]** **Verdict:** **DESIGN DRAFT REPAIRED; BUILD BLOCKED.** This is design only: it authorizes no code, schema, writer, repository, Git, build, fixture execution, run, or artifact-generation change. WP-P0-13 still depends on WP-P0-20 through B-01. B-10, B-11, and B-13 remain closed with their v1.8 corrections; B-14's authority answer stands, but its successor **B-15** is open and the three Hive routing values are a blocked design target again. **B-12 remains open and untouched**, and together with B-04 it still leaves two required non-null `TrialRecord` identities with no emittable value, so no row may be assembled and no commit or publication may occur. Four corrected closures are not four stronger ones: a closure is a design act, and §9 requires the reviewer to re-audit both the closures and these corrections. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:409-417,483-510`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:24,28`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/base.py:12,69`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G102_P013_CLOSURES.md:12`)

**Verdict:** **DESIGN DRAFT REPAIRED; BUILD BLOCKED.** The verdict is unchanged in substance: v1.9 corrected a count, widened one consequence, and completed one measurement; it closed nothing and opened nothing. This is design only: it authorizes no code, schema, writer, repository, Git, build, fixture execution, run, or artifact-generation change. WP-P0-13 still depends on WP-P0-20 through B-01. B-10, B-11, and B-13 remain closed with their v1.8 corrections; B-14's authority answer stands, but its successor **B-15** is open — and v1.9 records that while B-15 is open **no part path may be derived at all**, so every fixture arm whose input is a staged or committed part, a commit receipt, or the published view is a blocked design target — not only F-13 and R-8 — leaving only the writer-boundary probes F-2, F-3, and F-8, with F-9 recorded as undecided. **B-12 remains open and untouched**, and together with B-04 it still leaves two required non-null `TrialRecord` identities with no emittable value, so no row may be assembled and no commit or publication may occur. A corrected count is not a stronger closure: §9 still requires the reviewer to re-audit the four v1.7 closures, the six v1.8 repairs, and these v1.9 corrections. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:409-417,483-510`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:24,28`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/base.py:12,69`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G104_P013_FOLD.md:1-20`; §7 B-15)

**[SUPERSEDED IN v1.6 — retained v1.5 count:]** **Open items:** **11** — 8 named blockers and 3 open repository/contract discrepancies; these are not claimed as defects in v1.5. No accepting audit verdict is claimed. The package tier remains T1. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:415-417`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_N70_P013_V11.md:28-33`)

**[SUPERSEDED IN v1.7 — retained v1.6 count:]** **Open items:** **16** — 13 named blockers and 3 open repository/contract discrepancies; these are not claimed as defects in v1.6. No accepting audit verdict is claimed. The package tier remains T1. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:415-417`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:38-46,52-291`)

**[SUPERSEDED IN v1.8 — W203 G102 fold; retained v1.7 count:]** **Open items:** **12** — 9 named blockers and 3 open repository/contract discrepancies; these are not claimed as defects in v1.7. The 9 open blockers are **B-01, B-03, B-04, B-05, B-06, B-07, B-08, B-09, B-12**; **B-10, B-11, B-13, and B-14 closed in v1.7** and their sections are retained, tagged, and marked CLOSED rather than deleted. The 3 discrepancies are **D-02, D-03, D-04**, all unchanged. No accepting audit verdict is claimed. The package tier remains T1. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:415-417`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G99_BLOCKERS.md:19-21,87-89`)

**[SUPERSEDED IN v1.9 — W215 residual sweep; retained v1.8 count, which v1.9 recounted from the same rows and did not move:]** **Open items:** **13** — 10 named blockers and 3 open repository/contract discrepancies; these are not claimed as defects in v1.8. The 10 open blockers are **B-01, B-03, B-04, B-05, B-06, B-07, B-08, B-09, B-12, B-15**, where **B-15 `RUN-CELL-COORDINATE-CHANNEL` is opened in v1.8** by the withdrawal of §3.4.3's factory input. **B-10, B-11, and B-13 remain closed** with the v1.8 corrections recorded in their sections; **B-14 remains closed** on the authority question it asked, with B-15 as its successor. Every closed section is retained, tagged, and marked CLOSED rather than deleted. The 3 discrepancies are **D-02, D-03, D-04**; D-03's channel sentence is corrected in v1.8 and the discrepancy itself is unchanged and still open. No accepting audit verdict is claimed. The package tier remains T1. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:415-417`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G102_P013_CLOSURES.md:12,60-72`; §7 B-15)

**Open items:** **13** — 10 named blockers and 3 open repository/contract discrepancies; these are not claimed as defects in v1.9. **The count did not move in v1.9 and was recounted from the section headings themselves rather than carried forward:** the 10 open blockers are **B-01, B-03, B-04, B-05, B-06, B-07, B-08, B-09, B-12, B-15** (§7 headings) and the 3 discrepancies are **D-02, D-03, D-04** (§ Discrepancies headings); former B-02 and D-01 remain closed and excluded. **B-10, B-11, and B-13 remain closed** with their v1.8 corrections; **B-14 remains closed** on the authority question it asked, with B-15 as its successor. Every closed section is retained, tagged, and marked CLOSED rather than deleted. v1.9 opened no blocker, closed no blocker, and resolved no discrepancy. No accepting audit verdict is claimed. The package tier remains T1. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:415-417`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G104_P013_FOLD.md:1-20`; §7 B-12; §7 B-15)

**[SUPERSEDED IN v2.0 — W241; retained v1.9 verdict paragraph beginning “DESIGN DRAFT REPAIRED; BUILD BLOCKED.” character-for-character in the preceding v1.9 banner.]**

**[SUPERSEDED IN v2.1 — W287; retained v2.0 verdict follows.]**

**Verdict:** **DESIGN DRAFT PARTIALLY REPAIRED; BUILD BLOCKED.** GM66-F02, F03, and F04 are repaired;
GM66-F01 remains unresolved because its supplied verbatim hunk stopped. WP-P0-13 still depends on
WP-P0-20 through B-01; B-04 and B-12 still prevent row assembly; B-15 still prevents derivation of the
Hive routing paths; and new B-17 prevents R-8 from being performed from committed bytes even after a
factory input channel exists. B-12 and B-15 remain open and unchanged. No repository byte, code,
schema, writer, build, fixture, run, or artifact was produced. (§7 B-12; §7 B-15; §7 B-17;
`C:\tmp\LANE_PROMPTS_20260828\DS79_P013_PATCH.md:47-116`)

**v2.1 verdict:** **OWNER HALVES FOLDED; DESIGN AND BUILD REMAIN BLOCKED.** Decision 87 settles B-07's
keep-rule shape and decision 88 settles B-12's keep-all-settings choice. Neither answer supplies the
engineering contracts still required: B-07 needs the versioned policy encoding and authoritative
lifecycle/pin-record bindings, while B-12 needs the WP-P0-04-owned canonical preimage and sole identity
function. B-04 and the engineering half of B-12 still prevent row assembly; B-01, B-15, and B-17 keep
their prior consequences. No repository byte, code, schema, writer, build, fixture, run, or artifact is
produced. (`C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:744-745`;
§7 B-07; §7 B-12)

**[SUPERSEDED IN v2.2 — W296; retained v2.1 verdict above.]**

**v2.2 verdict:** **AMENDMENT FOLDED; DESIGN AND BUILD REMAIN BLOCKED.** Decision 128 supersedes
decision 87 and supplies the current selection shape, exact per-type count, and cut-off-tie rule. It
does not supply the engineering-owned policy/type/evidence encoding, exact robustness comparison, or
the authoritative lifecycle/pin records still needed to populate their independent row flags. B-07
therefore remains open only on that engineering half. Decision 88 and B-12 are unchanged; B-04 and
B-12 still prevent row assembly, and B-01, B-15, and B-17 keep their prior consequences.
(`C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:870-876,900-912`; §7 B-07; §7 B-12)

**[SUPERSEDED IN v2.0 — W241; retained v1.9 open-items paragraph beginning “Open items: 13” character-for-character in the preceding v1.9 count banner.]**

**[SUPERSEDED IN v2.1 — W287; retained v2.0 open-items paragraph follows.]**

**Open items:** **14** — **11** named blockers and **3** open repository/contract discrepancies. The
11 open blockers are **B-01, B-03, B-04, B-05, B-06, B-07, B-08, B-09, B-12, B-15, B-17** (§7
headings); the 3 discrepancies are **D-02, D-03, D-04** (§ Discrepancies headings). B-16 is absent
because GM66-F01 stopped. **B-10, B-11, and B-13 remain closed** with their recorded corrections;
**B-14 remains closed** on its authority question. No accepting audit verdict is claimed. The package
tier remains T1.

**v2.1 open items:** **14** — the same 11 named blocker headings and three discrepancy headings. B-07
and B-12 remain in that list only because their engineering halves remain open; their owner halves are
**DECIDED** and must not be returned to the owner. The other nine blockers and all three discrepancies
are unchanged. No accepting audit verdict is claimed. The package tier remains T1. (§7 B-07; §7 B-12;
§ Discrepancies)

**[SUPERSEDED IN v2.2 — W296; retained v2.1 open-items paragraph above.]**

**v2.2 open items:** **14** — the same 11 named blocker headings and three discrepancy headings. B-07
remains listed only for its engineering half under current decision 128; B-12 remains listed only for
its engineering half under unchanged decision 88. The other nine blockers and all three discrepancies
are unchanged. No accepting audit verdict is claimed. The package tier remains T1. (§7 B-07; §7 B-12;
§ Discrepancies)

## 1. Binding boundaries

1. WP-P0-04 owns the `TrialRecord` schema; WP-P0-13 consumes it and may not redefine it. The present repository model and its inherited base field are therefore the logical row contract in §3. WP-P0-04 is accepted on the current repository line: its merge record says T1 PASS with zero findings. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:255,317-332`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:14-68`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/base.py:59-89`; `git-object:fead492b0b87f207aa6e7a259372b9767d4301f9:7,17-19`)
2. The required catalog result is one Parquet row per trial, optimizer-independent and DuckDB-queryable; it must carry the six fields named in the lane prompt, selected trials must have full artifacts, and no row may lack a lineage class. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:409-417`; `C:\tmp\LANE_PROMPTS_20260828\LANE_W51_P013_DESIGN.md:29-41`)
3. WP-P0-08 identifies the post-migration `mega_walk_forward.py` path as the single direct emitter, treats CPCV/PBO/robustness/gate scoring as identity-keyed producers or consumers, and assigns useful legacy detail to selected-trial artifacts rather than parallel catalogs. Its repository merge record is T2 PASS-WITH-NITS with zero required findings. (`MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_08_WRITER_INVENTORY_2026-08-25/WRITER_INVENTORY.md:98-105`; `git-object:88eab9c93b7c285b990d07502ea1ec476034e8d5:7,9-14`)
4. **PROVISIONAL-ON-P020:** every choice about `FULL_KERNEL_SIMULATION`, canonical-path receipts, shared-allocator identity, the computed unsimulated-control manifest, and the final statistical/rejection producer remains provisional. **[SUPERSEDED IN v1.6 — retained status wording:]** “the two supplied P0-20 papers are both BLOCK.” P19 records that historical BLOCK for the v1 papers; the current P0-20 build-input design is v1.5, explicitly **DESIGN ONLY**, and no WP-P0-20 package acceptance is claimed here. B-01 remains the controlling P0-13 gate. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:483-510`; `C:\tmp\LANE_PROMPTS_20260828\AUDIT_P19_P020_PAPERS.md:1-16`; `C:\tmp\LANE_PROMPTS_20260828\P020_BUILD_DESIGN_V1.md:1-10`)
5. **[SUPERSEDED IN v1.6 — retained stale pointer:]** The v1.5 draft pointed this rule to `P020_STATISTICAL_BATTERY_DEFINITION_V1.md:59-66`. **Current:** inability to evaluate is BLOCKED/STOP, not a candidate FAIL; a tool error, missing data, unset threshold, or unreadable input never becomes PASS or FAIL. (`MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:48-107`; `C:\tmp\LANE_PROMPTS_20260828\P020_STATISTICAL_BATTERY_DEFINITION_V1.md:116-123`; `C:\tmp\LANE_PROMPTS_20260828\P020_BUILD_DESIGN_V1.md:700-705`)

## 2. Module, interface, and seam

### 2.1 Deep module

**DESIGN DECISION:** create one deep module, `TrialCatalogWriter`, with one external interface:

```text
write_completed_run(completed_run: CompletedRunInput) -> CatalogCommitReceipt
```

`CompletedRunInput` is a P0-13-owned closed boundary type, not an amendment to `TrialRecord`. Its declared fields are every terminal trial receipt, family-level statistical outputs, selection decisions, the run envelope, exactly one opaque adapter-issued lineage-origin receipt, and a closed set of typed `SelectedArtifactPayloadReceipt` objects keyed by `trial_id` and artifact kind. It deliberately has no `simulator_class`, `lineage`, sink-selection, output-path, flag-default, or ready-made-`TrialRecord` field. Boundary parsing explicitly refuses any such reserved key before conversion, even if the same spelling is a valid field on a later `TrialRecord`. This makes a caller label unrepresentable at the writer seam instead of hoping a known `TrialRecord` field is treated as an unknown extra. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:57`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/base.py:59-67`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_N70_P013_V11.md:21-26`)

**v1.8 note on this field list (G102-F04/G102-F05).** Two things about the sentence above are recorded
rather than repaired. First, the phrase "the run envelope" here is the v1.5 caller-supplied structure;
it is **not** `CatalogCommitPreimageV1.run_envelope`, the P0-13-owned typed model whose six members
§4.1.3 closes and whose sole producer is `EvaluationIdentityFactory` inside the module. The two names
collide and this draft does not decide which caller-supplied bytes populate the closed envelope; that
was never asked and is not answered here. Second, this list declares no `strategy`, `symbol`,
`timeframe`, or cell coordinate, which is why §3.4.3's factory input is withdrawn to **B-15**. v1.8
deliberately does not add members to this list to make that finding go away. (§3.4.3; §4.1.3; §7 B-15)

**[SUPERSEDED IN v1.6 — G93-F01/G93-F06; retained v1.5 return-payload text:]** The interface returns the committed row count, unique-trial count, catalog commit hash, Parquet part paths, selected-artifact manifests, and the versioned DuckDB view-publication receipt. Lineage, identities, flags, and paths are assembled and validated inside the module. This concentrates one-row conservation, lineage locking, identity validation, Parquet lowering, selection, and atomic commit behind one interface. The one-row-per-trial, DuckDB-queryability, and selected-artifact obligations come from the package output and brief artifact model. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:412,416`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2050-2089`)

**[SUPERSEDED IN v1.7 — B-10/B-13 closed; retained v1.6 text:]** **v1.6 controlling return payload:** the committed row count, unique-trial count, Parquet part paths, and selected-artifact manifests remain in `CatalogCommitReceipt`. The `catalog_commit_hash` member is unavailable while B-10 or B-13 is open, and the versioned DuckDB view-publication receipt is unavailable while B-13 is open, so `write_completed_run` cannot return a complete receipt and the module cannot reach commit or publication until those blockers close. The conservation, lineage-locking, identity-validation, lowering, and selection stages below remain the design; only the digest-bearing and publication members are withdrawn. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:52-86,204-233`)

**v1.7 controlling return payload:** the full v1.5 member list is restored to `CatalogCommitReceipt` — committed row count, unique-trial count, `catalog_commit_hash`, Parquet part paths, selected-artifact manifests, and the versioned DuckDB view-publication receipt — because §4.1.3 closes the commit preimage and §4.2.1 closes both schema fingerprints and `view_publication_hash`. The receipt additionally stores the exact typed preimage, which is where the six `evaluation_run_hash` members now live (§4.1.3, closing B-11). The module still cannot *reach* commit or publication: stage 3 below halts at B-04 and B-12, so no row is assembled, nothing is staged, and no receipt is produced. The withdrawal in v1.6 was for want of a byte formula; the remaining halt is for want of two row identities, which is a different and still-open condition. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:31-44,76-95`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:24,28`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G99_BLOCKERS.md:31-33,41-43,61-63`)

Internally, the module has these private stages, in order:

1. **[SUPERSEDED IN v1.6 — G93-F04; retained v1.5 text:]** `TerminalTrialConserver` declares the input universe once and proves `terminal receipts = emitted rows = unique trial_id values`; a missing, duplicate, overwritten, or unexplained terminal trial refuses the commit. This applies the one-terminal-disposition rule rather than trusting a final count.

   **v1.6 controlling design:** the conservation seam has three private modules with disjoint interfaces. `CompletedRunTrialUniverseProjector` is the sole expected-universe producer: before writer filtering, it projects the ordered `trial_id` multiset from the closed `CompletedRunInput` terminal receipts and cannot read assembled rows, staged parts, or committed parts. `CommittedTrialRowInventory` is the sole observed-universe producer: after serialization, it reads the staged hash-free Parquet parts and projects their ordered `trial_id` multiset and per-part row counts; it cannot read the expected-universe receipt. `TrialConservationComparer` belongs to neither producer, emits neither operand, and refuses a missing receipt, producer-identity alias, duplicate identity, unequal multiset, unexplained count, or overwrite. Only its typed success receipt permits commit. F-11 keeps the expected receipt fixed while one staged row is omitted, and a one-check-deleted comparer that accepts that modified copy is RED. This makes the required one-row-per-trial result a comparison across the writer seam, not one module agreeing with its own declaration. (`MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:933-967`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:409-417`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:144-171`)
2. `LineageClassifier` consumes only the adapter-issued capability and canonical-path receipt, derives one locked `simulator_class`, and fixes the physical sink class before any evaluation or trial identity is formed or accepted. Callers never pass a lineage label. **PROVISIONAL-ON-P020** for the acceptance-bearing receipt and full-kernel branch. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:498-510`)
3. `IdentityValidator` recomputes or validates every identity through its sole identity producer and refuses a mismatch. **PROVISIONAL-ON-P020** for the accepted evaluation and deployment preimages. It passes the locked class to `EvaluationIdentityFactory`, recomputes `evaluation_run_hash`, then recomputes every dependent `trial_id`; a receipt carrying a hash formed with another class is refused rather than rewritten only on the row. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:76-95,132-135`)

   **v1.6 controlling design:** “every identity” is now bounded. Two required non-null `TrialRecord` identities have no emittable value: `param_hash` has a named producer but no ratified preimage (B-04) and `preregistered_space_hash` has neither (B-12). `IdentityValidator` therefore cannot validate a complete identity set, and stage 7's `TrialRecordAssembler` cannot construct a row, until B-04 and B-12 close. Neither this stage nor the assembler may substitute a default, a sentinel, or a locally invented formula for a blocked identity; a row assembled with one is refused. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:24,28`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:1-154`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:122-142`)
4. `ArtifactSelector` applies the selected-trial rule and declares the selected `trial_id` universe before any artifact byte is committed. The brief selects top-K, Pareto, robust, promoted, and user-pinned trials. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2075-2089`)

   **v2.1 selection cascade — decision 87.** The selected universe's owner-decided shape is the union
   of the `TopKSelector` top **20** group per strategy, market, and timeframe; the
   `ParetoSelector` best risk-versus-return group; robust items; lifecycle-promoted items; and
   user-pinned items. The rule is combined rather than reduced to one score. `ArtifactSelector` may
   apply this only after B-07's engineering owner supplies the versioned policy encoding and the named
   lifecycle/pin-record bindings. The encoding must bind the owner's word “market” to an existing owned
   market dimension (the draft currently routes by `symbol`) rather than minting another identity; no
   scalar score, tie rule, or comparison formula is invented here. (`C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:744`; §7 B-07)

   **v2.2 amendment cascade — decision 128 supersedes decision 87.** `ArtifactSelector` first requires
   every applicable safety and quality check to pass, then consumes the engineering-owned overall-
   robustness order. `TopKSelector` marks the best **20** separately within strategy TYPE `day`,
   `swing`, and `position`, plus every candidate tied at the cut-off. Market and timeframe no longer
   partition this owner-decided top group. `ParetoSelector`, `RobustnessGate`,
   `LifecycleDecisionProjector`, and `UserPinProjector` continue to produce their row facts, but those
   facts no longer add a trial automatically to the selected universe. The exact check inputs,
   robustness comparison, type binding, and executable tie handling remain B-07 engineering work; no
   scalar score or new identity is introduced. (`C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:870-876,900-912`; §7 B-07)

   **NEW-BY-ADDENDUM-32 — strategy-type and versioned-policy design item.** Before selection can run,
   the P0-13 seam must consume an owned strategy TYPE with exactly the policy categories `day`,
   `swing`, or `position`, versioned selection-policy settings, the applied policy version, and the
   relevant evidence provenance for that version. A policy-version change requires fresh relevant
   evidence before selection is recomputed. This is a cross-draft compatibility requirement: P0-20
   owns the versioned risk/leverage policy-and-fresh-evidence side, P0-21 owns the per-type versioned
   minimum/forward-evidence rules, and the P0-13 build owner must bind their accepted receipts to the
   selection policy. This item does not add a `TrialRecord` field, choose a receipt identity, or supply
   any still-pending evidence value. Those sibling values remain `OWNER-ANSWERED-SHAPE, VALUE PENDING
   (addendum 32)`. (`C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:856-898,902-928`;
   `C:\tmp\LANE_PROMPTS_20260828\LANE_W296_P013_AMEND_FOLD.md:45-47`; §7 B-07)

   **AMENDMENT-CHOICE (FOLD-P013, owner addendum 32 "for example", 2026-09-03).** The retained wording above is superseded: the three types `day`, `swing`, and `position` are examples of the owned strategy TYPE policy categories, the list is not closed, and any strategy type the owner names later is admitted under the same rule. Owner addendum 32, verbatim: "for example, day trading, swing trading, and position trading" (`ADDENDUM_32.md:38`).

5. `SelectedArtifactManifestBuilder` consumes the four typed payload receipts for each selected trial and produces canonical `manifest.json` bytes that carry the selected `trial_id` and its dependent identities (`package_hash`, `evaluation_run_hash`, `param_hash`) under the WP-P0-04 schema-owner binding required by blocker B-09; `SelectedArtifactCommitter` alone writes those five prepared payloads under one per-trial address `artifacts/<package_hash>/<trial_id>/` and refuses a second write to an already-committed address. The committer neither creates payload content nor decides completeness. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2075-2085`; `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_08_WRITER_INVENTORY_2026-08-25/WRITER_INVENTORY.md:102-104`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:132-135`)
6. `ArtifactCommitVerifier`, a separate reader of committed bytes, consumes the conserved `trial_id` universe from `CompletedRunTrialUniverseProjector` through the successful `TrialConservationComparer` receipt, the selected `trial_id` universe from `ArtifactSelector`, and the committed-address inventory. **[SUPERSEDED IN v1.6 — retained source name:]** the v1.5 text named `TerminalTrialConserver` as the universe source. For each selected trial the verifier checks the closed member set, byte length, digest, committed directory address, and committed `manifest.json` identities, and compares the committed `trial_id` and dependent identities against the independent row identity produced by `IdentityValidator`/`TrialIdentityFactory` in stage 3 — never against the upstream `SelectedArtifactPayloadReceipt`, so no producer receipt is both operands of the comparison. It emits exactly one `has_full_artifacts` value for every conserved `trial_id`: `true` iff the trial is selected and the committed address/manifest identities match that independent row identity; `false` iff the trial is unselected and no selected-artifact address was committed for it. Any other combination — including `true` for an unselected trial, `false` for a selected identity-matched trial, or a selected trial without a valid verifier receipt — is refused before assembly. The repository model's default `false` never supplies this value. A missing committed identity, an address/manifest/row mismatch, or a duplicate address is also refused. The verifier cannot write or synthesize an artifact. The later catalog-commit `{trial_id, manifest_sha256, members}` association in §4.1 is a second check and does not substitute for this one. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:67,77-88`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:132-135`; `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:933-967`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:144-171`)
7. `TrialRecordAssembler` accepts values only from the sole producers in §3, including the independent artifact-verification receipt, constructs the repository `TrialRecord` normally, and never uses `model_construct()` or validation-bypass copying. (`MTC_COMMAND_CENTER/contracts/README.md:18-35`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:14-74`)
8. **[SUPERSEDED IN v1.6 — G93-F01/G93-F06; retained v1.5 text:]** `ParquetCommitter` lowers and stages hash-free Parquet parts outside the query glob, validates them, asks sole producer `CatalogCommitIdentity` to hash the non-self-referential preimage in §4.1, atomically moves them to the derived hash-bearing paths, and writes the closed receipt. The same preimage is idempotent; the same `trial_id` with different bytes refuses.

   **[SUPERSEDED IN v1.7 — B-10/B-13 closed; retained v1.6 text:]** **v1.6 controlling design:** `ParquetCommitter` may lower and validate hash-free staged parts, but it must halt before identity formation, final-path derivation, or publication while B-10 or B-13 is open. The desired non-self-referential and idempotent properties remain acceptance requirements after the preimages close; they are not current computable claims. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:31-44`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:52-86,204-233`)

   **v1.7 controlling design:** the v1.5 stage-8 sequence is restored and is now computable: `ParquetCommitter` lowers and stages hash-free parts outside the query glob, validates them, asks sole producer `CatalogCommitIdentity` to hash the closed §4.1.3 preimage, atomically moves each staged slot to the derived hash-bearing path, and writes the closed receipt. Non-self-reference is preserved by construction — item 2's envelope excludes `catalog_commit_hash` and item 3's `path_slot` ends at the partition directory plus ordinal (§4.1.3). Idempotence is now a computable identity because every member is a stored byte sequence: the same closed preimage yields the same digest, and the same `trial_id` with different bytes changes item 3 and therefore the digest, so it refuses. This stage is unreachable in practice while stage 3 halts on B-04/B-12; it is a specified stage, not an executed one. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:31-44`; §4.1.3)
9. **[SUPERSEDED IN v1.6 — G93-F06; retained v1.5 text:]** `DuckDBViewPublisher` is the sole producer of the versioned `trial_catalog` view. Before publication, sole expected-fingerprint producer `TrialCatalogViewSchemaProjector` projects exactly the frozen published-view contract in §3.4.1, without reading committed parts or the candidate view. Sole observed-fingerprint producer `CommittedDuckDBSchemaInspector` derives the logical schema only from the candidate view projection that queries will see; it does not merge a separate Parquet-parts schema into that operand. `DuckDBSchemaFingerprintComparer`, which produces neither operand and belongs to neither producer, compares them and refuses any mismatch. Deriving the expected operand from the same committed parts or view being inspected is explicitly refused as a same-producer-degenerate implementation; it is not independent schema proof. After that comparison, `DuckDBViewPublisher` consumes only validated committed receipts and parts, refuses a wrong glob, and publishes the §4.2 SQL template after injecting the sorted validated receipt hashes.

   **[SUPERSEDED IN v1.7 — B-10/B-13 closed; retained v1.6 text:]** **v1.6 controlling design:** these producer-separation constraints remain, but the fingerprint and publication interfaces are blocked on B-13 and the validated commit receipts are blocked on B-10/B-13. No view publication occurs until those blockers close. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:412,416`; `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:617-628,681-687`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:52-86,204-233`)

   **v1.7 controlling design:** the producer-separation constraints are unchanged and the fingerprint and publication interfaces are now specified: both fingerprints are `SHA256(canonical_json(PublishedViewSchemaDocumentV1))` over the ordered column document in §4.2.1, and `DuckDBViewPublisher` is the sole producer of the published SQL bytes that `view_publication_hash` binds. The expected producer still may not inspect committed parts or the candidate view, and the comparer still emits neither operand. Publication remains unreachable while stage 3 halts on B-04/B-12, and it remains gated on WP-P0-20 acceptance through B-01. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:412,416`; `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:617-628,681-687`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:31-44`; §4.2.1)

Each `SelectedArtifactPayloadReceipt` is closed and immutable: `{trial_id, artifact_kind, producer_id, staged_handle, byte_length, sha256}`. Exactly one receipt is required for each of `trades.parquet`, `equity.parquet`, `intents.jsonl`, and `levels.parquet` for every selected trial; unselected trials supply none. Sole payload producers are respectively `TradeLedgerArtifactProducer`, `EquityCurveArtifactProducer`, `IntentTraceArtifactProducer`, and `LevelTraceArtifactProducer`. The manifest builder is the sole `manifest.json` byte producer, and the committer consumes prepared bytes from all five producers without changing them. Missing, duplicate, wrong-kind, identity-drifted, or unexplained receipts refuse before commit. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2075-2085`; `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_08_WRITER_INVENTORY_2026-08-25/WRITER_INVENTORY.md:102-104`; `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:933-967`)

### 2.2 Real adapters at the lineage seam

There are exactly two adapters:

- `MigratedCanonicalRunAdapter` supplies a verified canonical-path receipt and can obtain the private acceptance-bearing sink capability. **PROVISIONAL-ON-P020:** the receipt shape, issuer, and verification rule are frozen only after WP-P0-20 accepts. WP-P0-20 requires import identity for the exact shared allocator plus kernel, not an assertion or stand-in stamp. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:497-509`)
- `LegacySignalScreenRunAdapter` has no parameter or method that can request the acceptance-bearing capability. Its private capability maps unconditionally to `SIGNAL_SCREEN_ONLY` and the physical screening root. The plan explicitly permits cheap screening but makes its numbers non-acceptance-bearing. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:509-511`)

The seam is the completed-run receipt, not an optimizer hook. Grid, TPE, and random search can vary upstream while the same terminal receipt and writer interface remain fixed; choosing a primary optimizer is a later decision. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:27-33`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2037-2048`)

### 2.3 Mapping to the WP-P0-08 writer inventory

| Inventory writer/class | WP-P0-13 design disposition | Emission point |
|---|---|---|
| Post-migration `mega_walk_forward.py` | Sole direct caller of `TrialCatalogWriter`; no best-only JSON remains authoritative after verified migration. **PROVISIONAL-ON-P020** because the direct caller is the migrated canonical path. | Once, at completed-run finalization, after every terminal trial and family statistic is available. (`MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_08_WRITER_INVENTORY_2026-08-25/WRITER_INVENTORY.md:35,102`)
| CPCV, PBO, robustness, BH/DSR, and gate scoring | Identity-keyed value producers feeding the completed-run receipt; never independent catalog writers or in-place row mutators. **PROVISIONAL-ON-P020** for final producer identities and STOP semantics. | Before run finalization; each returns values keyed by `evaluation_run_hash`, `family_id`, and/or `trial_id`. (`MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_08_WRITER_INVENTORY_2026-08-25/WRITER_INVENTORY.md:42-56,103`; `C:\tmp\LANE_PROMPTS_20260828\AUDIT_P19_P020_PAPERS.md:53-83`)
| `reference_producer.py`, prototype/STG046 debug writers, batch/Stage-2 traces | Useful trade/equity/intent/level columns move to Tier-2 selected artifacts; they do not write catalog rows. | Typed payload producers feed `SelectedArtifactManifestBuilder` and the byte-only `SelectedArtifactCommitter`; the separate `ArtifactCommitVerifier` only reads the committed result. (`MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_08_WRITER_INVENTORY_2026-08-25/WRITER_INVENTORY.md:38,65-85,104`)
| `run_quantlens_overnight_research.py` and any explicitly retained unmigrated tool | Route through `LegacySignalScreenRunAdapter`; no second CSV catalog authority. | Completed legacy run, always into the screening root. (`MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_08_WRITER_INVENTORY_2026-08-25/WRITER_INVENTORY.md:36`)
| Run plans and progress emitters | Remain operational manifests/status only; never evidence rows. | No `TrialRecord` emission. (`MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_08_WRITER_INVENTORY_2026-08-25/WRITER_INVENTORY.md:58-59`)
| All other independent JSON/CSV result authorities | Retire only after migration and verification; this design authorizes no deletion. | No direct emission after cutover. (`MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_08_WRITER_INVENTORY_2026-08-25/WRITER_INVENTORY.md:29,100-105`)

No Parquet, DuckDB, or SQLite `TrialRecord` writer exists in the inventory today, so this is a new writer module rather than a wrapper around an existing catalog sink. (`MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_08_WRITER_INVENTORY_2026-08-25/WRITER_INVENTORY.md:98-105`)

## 3. `TrialRecord` row contract

### 3.1 Encoding rules

- Logical types and nullability below are exactly the repository model. `NonEmptyStr` is a stripped string with length at least one; `Sha256` is 64 lowercase hexadecimal characters; unknown fields are refused; every model is frozen. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/base.py:12-16,59-89`)
- Parquet `LIST` represents contract tuples. `parameters` is physically stored in the column named `parameters` as canonical UTF-8 JSON `VARCHAR`; the writer refuses non-canonical/non-JSON values. This preserves the logical `dict[str, Any]` without inventing TrialRecord fields. `fee_bps_used` is a canonical decimal-string `VARCHAR` to avoid a silent precision/scale choice. Canonical JSON already defines sorted keys, compact separators, decimal strings, and refusal of NaN. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:31,54`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:15-44`)
- Required list fields may be empty but never NULL. An early rejected trial therefore carries empty fold lists plus a non-empty rejection reason; it is still one terminal trial row. Required-vs-nullable follows the present model. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:35-60`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:412,416`)
- The assembler does not compute values. It accepts each field from exactly the sole producer named below, validates it, and refuses conflicting second values.

### 3.2 Top-level fields (48)

| Field | Logical type → Parquet | Nullable? | Sole producer | Authority / note |
|---|---|---:|---|---|
| `contract_version` | string matching `0.1.0` → `VARCHAR` | No | `ContractRuntime` | Inherited required-on-disk default; mismatches refused. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/base.py:12,59-78`)
| `run_id` | non-empty string → `VARCHAR` | No | `RunIdentityFactory` | `deployment_identity_hash.environment.sequence`. **PROVISIONAL-ON-P020** for the accepted deployment identity input. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:17`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:138-141`)
| `candidate_id` | non-empty string → `VARCHAR` | No | `CandidateIdentityFactory` | Frozen date plus source-provenance hash. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:18`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:47-51`)
| `package_hash` | SHA-256 → `VARCHAR(64)` | No | `PackageIdentityFactory` | Computed from frozen strategy semantics. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:19`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:54-73`)
| `deployment_identity_hash` | SHA-256 → `VARCHAR(64)` | No | `DeploymentIdentityFactory` | **PROVISIONAL-ON-P020:** includes accepted allocator/cost/protection lineage. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:20`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:98-129`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:487-499`)
| `evaluation_run_hash` | SHA-256 → `VARCHAR(64)` | No | `EvaluationIdentityFactory` | **PROVISIONAL-ON-P020:** the factory receives the class already locked by `LineageClassifier` and binds package, dataset manifest, cost model, simulator class/version, and evaluation config; a caller/receipt hash is comparison input only. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:21`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:76-95`)
| `family_id` | non-empty string → `VARCHAR` | No | `FamilyIdentityFactory` | Source provenance, producer, parameter neighbourhood. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:22`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:144-154`)
| `trial_id` | non-empty string → `VARCHAR` | No | `TrialIdentityFactory` | Evaluation hash, parameter hash, non-negative sequence. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:23`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:132-135`)
| `param_hash` | SHA-256 → `VARCHAR(64)` | No | `ParameterSetCanonicalizer` | Producer is fixed here; exact preimage is blocker B-04. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:24`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:31-44`)
| `exit_mode` | non-empty string → `VARCHAR` | No | `StrategyPackageProjector` | Frozen exact trial configuration. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:25`)
| `search_regime` | enum `grid|tpe|random` → dictionary `VARCHAR` | No | `SearchFamilyRegistry` | Contract precedes optimizer choice. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:27`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2037-2048`)
| `preregistered_space_hash` | SHA-256 → `VARCHAR(64)` | No | **BLOCKED — B-12; no producer may emit it** | **[SUPERSEDED IN v1.6 — retained v1.5 producer/note:]** `SearchFamilyRegistry`; “One registered family space.” The repository requires the field but supplies no canonical preimage or identity function; P0-13 will not invent either. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:28`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:1-154`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:122-142`)
| `trial_index_in_family` | integer ≥0 → `BIGINT` | No | `SearchFamilyRegistry` | Stable sequence within family. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:29`)
| `family_size` | integer >0 → `BIGINT` | No | `SearchFamilyRegistry` | **PROVISIONAL-ON-P020:** P0-13 must carry the field, while its final family semantics remain behind B-01. **[SUPERSEDED IN v1.6 — retained stale pointer:]** `P020_STATISTICAL_BATTERY_DEFINITION_V1.md:299-301`; the current v1.5 battery does not define `family_size`, so it is not cited as authority for this field. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:30`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:409-417`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:235-266`)
| `parameters` | `dict[str, Any]` → canonical-JSON `VARCHAR` | No | `ParameterSetCanonicalizer` | Present schema is one mapping, not sparse typed columns; see discrepancy D-02. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:31`)
| `modules_enabled` | tuple of non-empty strings → `LIST<VARCHAR>` | No | `StrategyPackageProjector` | Immutable module set projection. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:32`)
| `modules_enabled_count` | integer ≥0 → `BIGINT` | No | `StrategyPackageProjector` | **LIMITATION—SAME-PRODUCER CONSISTENCY ONLY:** the model validates equality with `len(modules_enabled)`, but both operands come from this producer, so this is not independent module-set completeness proof. If independent proof is required, P0-04 must define a second authoritative source, such as the package-hash preimage, and a comparer that emits neither operand. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:33,70-74`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:54-70`)
| `fold_test_returns` | tuple of float → `LIST<DOUBLE>` | No | `WalkForwardEvaluator` | **PROVISIONAL-ON-P020:** migrated canonical evaluator. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:35`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:485,498-510`)
| `fold_test_sharpes` | tuple of float → `LIST<DOUBLE>` | No | `WalkForwardEvaluator` | **PROVISIONAL-ON-P020.** (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:36`; `C:\tmp\LANE_PROMPTS_20260828\AUDIT_P19_P020_PAPERS.md:60-71`)
| `fold_test_trades` | tuple of integer → `LIST<BIGINT>` | No | `WalkForwardEvaluator` | **PROVISIONAL-ON-P020.** (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:37`; `C:\tmp\LANE_PROMPTS_20260828\AUDIT_P19_P020_PAPERS.md:60-71`)
| `lockbox_return_pct` | float → `DOUBLE` | Yes | `LockboxEvaluator` | **PROVISIONAL-ON-P020;** the repository field is nullable; when the lockbox element is required, missing registration or an unset minimum-data threshold is BLOCKED rather than FAIL. **[SUPERSEDED IN v1.6 — retained stale pointer:]** `P020_STATISTICAL_BATTERY_DEFINITION_V1.md:74-101`. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:39`; `C:\tmp\LANE_PROMPTS_20260828\P020_STATISTICAL_BATTERY_DEFINITION_V1.md:220-249`)
| `lockbox_sharpe` | float → `DOUBLE` | Yes | `LockboxEvaluator` | **PROVISIONAL-ON-P020.** (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:40`)
| `lockbox_maxdd` | float → `DOUBLE` | Yes | `LockboxEvaluator` | **PROVISIONAL-ON-P020.** (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:41`)
| `lockbox_trades` | integer → `BIGINT` | Yes | `LockboxEvaluator` | **PROVISIONAL-ON-P020.** (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:42`)
| `lockbox_pf` | float → `DOUBLE` | Yes | `LockboxEvaluator` | **PROVISIONAL-ON-P020.** (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:43`)
| `lockbox_expectancy_R` | float → `DOUBLE` | Yes | `LockboxEvaluator` | **PROVISIONAL-ON-P020.** (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:44`)
| `lockbox_win_rate` | float → `DOUBLE` | Yes | `LockboxEvaluator` | **PROVISIONAL-ON-P020.** (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:45`)
| `bh_return_pct` | float → `DOUBLE` | Yes | `BenchmarkEvaluator` | **PROVISIONAL-ON-P020.** (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:46`)
| `excess_alpha` | float → `DOUBLE` | Yes | `BenchmarkEvaluator` | **PROVISIONAL-ON-P020.** (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:47`)
| `dsr_p_value` | float → `DOUBLE` | Yes | `DSREvaluator` | **PROVISIONAL-ON-P020:** inability to evaluate remains NULL/BLOCKED, not false. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:48`; `C:\tmp\LANE_PROMPTS_20260828\AUDIT_P19_P020_PAPERS.md:341-351`)
| `dsr_robust` | bool → `BOOLEAN` | Yes | `DSREvaluator` | **PROVISIONAL-ON-P020:** NULL/not-produced is not evaluable; false is a valid evaluated failure only after the threshold authority exists. **[SUPERSEDED IN v1.6 — retained stale pointer:]** `P020_STATISTICAL_BATTERY_DEFINITION_V1.md:281-289`. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:49`; `C:\tmp\LANE_PROMPTS_20260828\P020_STATISTICAL_BATTERY_DEFINITION_V1.md:394-430`)
| `bh_fdr_survivor` | bool → `BOOLEAN` | Yes | `BHFDRFamilyEvaluator` | **PROVISIONAL-ON-P020:** the complete family definition awaits acceptance. **[SUPERSEDED IN v1.6 — retained stale pointer:]** `P020_STATISTICAL_BATTERY_DEFINITION_V1.md:217-249`. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:50`; `C:\tmp\LANE_PROMPTS_20260828\P020_STATISTICAL_BATTERY_DEFINITION_V1.md:340-392`)
| `cpcv_pass_ratio` | float → `DOUBLE` | Yes | `CPCVEvaluator` | **PROVISIONAL-ON-P020:** inline producer and STOP mapping await acceptance. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:51`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:485`; `C:\tmp\LANE_PROMPTS_20260828\AUDIT_P19_P020_PAPERS.md:366-371`)
| `pbo` | float → `DOUBLE` | Yes | `PBOEvaluator` | **PROVISIONAL-ON-P020:** inline producer and threshold semantics await acceptance. **[SUPERSEDED IN v1.6 — retained stale pointer:]** `P020_STATISTICAL_BATTERY_DEFINITION_V1.md:187-215`. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:52`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:483-510`; `C:\tmp\LANE_PROMPTS_20260828\P020_STATISTICAL_BATTERY_DEFINITION_V1.md:303-338`)
| `net_after_slippage_pct` | float → `DOUBLE` | Yes | `CostedFillEvaluator` | **PROVISIONAL-ON-P020:** must come from accepted in-path economics, not a side column. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:53`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:485-487`)
| `fee_bps_used` | Decimal → canonical decimal `VARCHAR` | Yes | `CostedFillEvaluator` | **PROVISIONAL-ON-P020:** versioned cost registry. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:54`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:487`)
| `slippage_model_id` | non-empty string → `VARCHAR` | Yes | `CostedFillEvaluator` | **PROVISIONAL-ON-P020:** versioned cost registry. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:55`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:487`)
| `simulator_class` | non-empty string → dictionary `VARCHAR` | No | `LineageClassifier` | Locked before evaluation/trial identity work; legacy adapter always yields `SIGNAL_SCREEN_ONLY`; full class is **PROVISIONAL-ON-P020** and requires the sealed receipt. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:57`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:76-95`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:499,509-510`)
| `unsimulated_controls_hash` | SHA-256 → `VARCHAR(64)` | No | `ControlManifestHasher` | **PROVISIONAL-ON-P020:** hashes the computed manifest, never a caller declaration. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:58`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:500-503,509`)
| `classification` | non-empty string → dictionary `VARCHAR` | No | `TrialGateAggregator` | **PROVISIONAL-ON-P020:** sole row-level terminal classification producer. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:59`; `C:\tmp\LANE_PROMPTS_20260828\AUDIT_P19_P020_PAPERS.md:53-83`)
| `rejection_reasons` | tuple of non-empty strings → `LIST<VARCHAR>` | No | `TrialGateAggregator` | **PROVISIONAL-ON-P020:** sole normalized reason producer; taxonomy is blocker B-06. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:60`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:416`)
| `is_pareto` | bool → `BOOLEAN` | No | `ParetoSelector` | Default false is emitted by this producer, not inferred by Parquet. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:62`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2087`)
| `is_top_k` | bool → `BOOLEAN` | No | `TopKSelector` | Exact objective/K is blocker B-07. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:63`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2087`)
| `is_robust` | bool → `BOOLEAN` | No | `RobustnessGate` | **PROVISIONAL-ON-P020:** P0-13 does not infer “not evaluable” from false; final mapping remains behind B-01 because the current P0-20 v1.5 battery does not define `is_robust`. **[SUPERSEDED IN v1.6 — retained stale pointer:]** `P020_STATISTICAL_BATTERY_DEFINITION_V1.md:381-392`. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:64`; `C:\tmp\LANE_PROMPTS_20260828\P020_STATISTICAL_BATTERY_DEFINITION_V1.md:116-123`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:235-266`)
| `is_promoted` | bool → `BOOLEAN` | No | `LifecycleDecisionProjector` | True only from the future authoritative lifecycle decision; writer/gate scoring cannot mint it. Authority is blocker B-07. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:65`; `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_08_WRITER_INVENTORY_2026-08-25/WRITER_INVENTORY.md:55`)
| `is_pinned` | bool → `BOOLEAN` | No | `UserPinProjector` | True only from an explicit user pin record; authority is blocker B-07. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:66`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2087`)
| `has_full_artifacts` | bool → `BOOLEAN` | No | `ArtifactCommitVerifier` | This producer emits one value per conserved `trial_id`: `true` only for a selected trial whose committed artifacts and manifest are present and identity-matched; `false` only for an unselected trial with no committed selected-artifact address. Default `false` is emitted by this producer, not inferred from the repository model or Parquet. Every inconsistent selection/artifact/flag combination is refused before assembly. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:67,77-88`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2075-2087`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G42_P013_V13.md:93-133`)
| `environment_lineage` | `EnvironmentLineage` → non-null `STRUCT` | No | `EnvironmentLineageRecorder` | Environment is outside identity hashes but required beside evidence. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:68`; `MTC_COMMAND_CENTER/contracts/README.md:39-42`)

**v2.1 field cascade — decisions 87 and 88.** `is_top_k` now means membership in the owner-decided
top-20-per-strategy/market/timeframe group; `is_pareto`, `is_robust`, `is_promoted`, and `is_pinned`
remain the other independently produced keep groups, and no one-score field is introduced. The
required `parameters` value is retained for every conserved trial row, selected and unselected, which
implements the owner-decided settings-retention scope once the engineering blockers permit rows to be
assembled. This does not widen `has_full_artifacts`: full Tier-2 artifacts remain selected-only, while
settings remain in every saved catalog row. B-07's policy/record half and B-12's preimage half remain
open. (`C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:744-745`;
§3.2 rows `parameters`, `is_pareto`, `is_top_k`, `is_robust`, `is_promoted`, `is_pinned`,
`has_full_artifacts`; §7 B-07; §7 B-12)

**v2.2 field cascade — decision 128 supersedes decision 87.** The retained v2.1 meanings above are
historical where they define selection membership. Under the current rule, `is_top_k` means membership
in the best-20-per-strategy-TYPE group plus all cut-off ties, after safety and quality checks and the
overall-robustness ranking. The existing `is_pareto`, `is_robust`, `is_promoted`, and `is_pinned` fields
remain independently produced row facts, but none automatically selects a trial. `has_full_artifacts`
continues to follow the current selected universe. Decision 88 still requires `parameters` on every
saved row and is unchanged by addendum 32. The contract has no strategy-type or selection-policy-
version field, so the `NEW-BY-ADDENDUM-32` design item remains an owned boundary-binding task under
B-07 rather than a schema amendment here. (`C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:870-876,900-912`; §2.1 stage 4; §7 B-07; §7 B-12)

### 3.3 Nested `environment_lineage` fields (7)

| Nested field | Logical type → Parquet | Nullable? | Sole producer | Authority / note |
|---|---|---:|---|---|
| `contract_version` | string matching `0.1.0` → `VARCHAR` | No | `ContractRuntime` | Inherited by the nested contract. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/base.py:59-78`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/lineage.py:18-26`)
| `python_version` | non-empty string → `VARCHAR` | No | `EnvironmentLineageRecorder` | Required environment fact. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/lineage.py:21`)
| `dependency_lockfile_hash` | SHA-256 → `VARCHAR(64)` | No | `EnvironmentLineageRecorder` | Required environment fact. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/lineage.py:22`)
| `os_name` | non-empty string → `VARCHAR` | No | `EnvironmentLineageRecorder` | Required environment fact. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/lineage.py:23`)
| `os_version` | non-empty string → `VARCHAR` | No | `EnvironmentLineageRecorder` | Required environment fact. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/lineage.py:24`)
| `golden_suite_hash` | SHA-256 → `VARCHAR(64)` | No | `EnvironmentLineageRecorder` | Required golden-suite identity. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/lineage.py:25`)
| `golden_suite_bit_identical` | bool → `BOOLEAN` | No | `EnvironmentLineageRecorder` | Required result of the environment-change golden comparison. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/lineage.py:26`; `MTC_COMMAND_CENTER/contracts/README.md:39-42`)

### 3.4 Published-view contract without redefining `TrialRecord`

The brief requires Hive-style path/query dimensions `run_id`, `strategy`, `symbol`, and `timeframe`, while the present `TrialRecord` contains only `run_id`. The frozen logical schema for the §4.2 published view is exactly: all §3.2 top-level fields (including the §3.3 nested struct), plus the five view-only columns below. `TrialCatalogViewSchemaProjector` projects exactly this set. No commit-receipt field is silently expected from SQL that does not read the receipt. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2050-2071`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:14-68`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G61_P013_V14.md:99-149`)

#### 3.4.1 Columns added by the published view

| View-only field | Type | Nullable? | Physical production channel | Use |
|---|---|---:|---|---|
| `lineage` | non-empty string | No | Hive `lineage=*` path partition | Filter and independent agreement with row `simulator_class`. |
| `strategy` | non-empty string | No | Hive `strategy=*` path partition | Filter. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2052-2056`)
| `symbol` | non-empty string | No | Hive `symbol=*` path partition | Filter. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2052-2056`)
| `timeframe` | non-empty string | No | Hive `timeframe=*` path partition | Filter. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2052-2056`)
| `catalog_commit_hash` | SHA-256 | No | §4.2 filename `regexp_extract` over the final hash-bearing part name | Join to the publisher-injected validated receipt hashes; the value is not stored in the Parquet bytes it covers. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_N70_P013_V11.md:14-19`)

**[SUPERSEDED IN v1.7 — B-14 closed; retained v1.6 text:]** The table names physical channels, not value authorities. The current sources require non-empty `strategy`, `symbol`, and `timeframe` path/query dimensions but do not name the producer of their values. Until B-14 closes, no caller or committer may mint them, the three partitions are a blocked design target, and path/envelope equality cannot be claimed. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2050-2071`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:14-68`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:268-291`)

**[SUPERSEDED IN v1.8 — G102-F04; retained v1.7 text:]** **v1.7 controlling disposition:** the table still names physical channels, not value authorities — that sentence survives, and it is precisely why §3.4.3 now names the authority separately. The three values are produced by `RunCellDimensionsFactory` from the completed run's own cell coordinates, the committed Hive path bytes must equal that typed receipt, and `PathReceiptCellComparer` proves the agreement with typed `PATH_RECEIPT_CELL_MISMATCH`. The three partitions are therefore a specified design target, not a blocked one; no caller and no committer mints the values. (§3.4.3; `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_08_WRITER_INVENTORY_2026-08-25/WRITER_INVENTORY.md:35,102`)

**v1.8 controlling disposition:** the table names physical channels, not value authorities — that sentence still survives. The **authority** for the three values is settled and not re-opened: it is the completed run's own strategy × symbol × timeframe cell, produced by `RunCellDimensionsFactory`, observed by `CommittedPathCellInspector`, and compared by `PathReceiptCellComparer` with typed `PATH_RECEIPT_CELL_MISMATCH`. What is **not** settled is the declared channel by which those coordinates reach the factory: §2.1's closed `CompletedRunInput` declares none, so the factory cannot emit a receipt and the three partitions are a **blocked design target again** under **B-15**. No caller and no committer may mint the values, and no path/receipt equality may be claimed until B-15 closes. (§3.4.3; §7 B-15; `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_08_WRITER_INVENTORY_2026-08-25/WRITER_INVENTORY.md:35,102`)

**[SUPERSEDED IN v1.7 — B-10/B-13 closed; retained v1.6 text:]** The `catalog_commit_hash` view column is likewise a blocked design target: it is projected from the final hash-bearing part filename, and that filename cannot be derived while B-10 or B-13 is open. Its non-null requirement above therefore describes the intended post-blocker view, not a column the current design can produce. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:52-86,204-233`)

**v1.7 controlling disposition:** the final hash-bearing part filename is derivable, because §4.1.3 closes the preimage `CatalogCommitIdentity` hashes and §4.2.1 closes the expected fingerprint that preimage embeds. The `catalog_commit_hash` view column is a specified non-null column projected from that filename by the §4.2 `regexp_extract`, and its value is still not stored in the Parquet bytes it covers. (§4.1.3; §4.2.1; `C:\tmp\LANE_PROMPTS_20260828\DETECT_N70_P013_V11.md:14-19`)

**[SUPERSEDED IN v1.6 — G93-F05; retained v1.5 text:]** `run_id` is one logical §3.2 row column, not an extra view-only column. The Hive `run_id=*` path segment is an independently checked routing copy and must equal the Parquet row value for every part. A missing, conflicting, or separately surfaced duplicate path value refuses publication; the expected fingerprint contains `run_id` exactly once.

**v1.6 controlling design:** `RunIdentityFactory` is the sole expected-value producer for each row `run_id`. `CommittedPathRunIdInspector` is the sole observed-value producer and reads only the Hive `run_id=*` segment for each candidate part. `PathRowRunIdComparer` belongs to neither producer, emits neither operand, consumes both typed receipts, and refuses a missing receipt, producer-identity alias, missing path value, separately surfaced duplicate column, unequal path/row value, or mixed row values within a part with `REFUSED(reason=PATH_ROW_RUN_ID_MISMATCH)`. F-12/R-6 changes only the Hive segment, rebuilds the catalog receipt so every commit predicate remains valid, and requires that exact reason; a one-check-deleted comparer accepts and is RED. The expected schema still contains `run_id` exactly once, but column count is not treated as value comparison. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:17`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:138-141`; `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:617-687`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:173-202`)

`canonical_path_receipt_hash` is absent by design for screening, so it is not a nullable-or-conditional view column invented by `union_by_name`. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_G61_P013_V14.md:119-139`)

#### 3.4.2 Commit-receipt metadata, not published-view columns

**[SUPERSEDED IN v1.6 — G93-F01/G93-F08; retained v1.5 text:]** The run envelope retained in `CatalogCommitPreimageV1` may bind `dataset_manifest_sha`, `simulator_version`, `battery_version`, `objective_id`, and conditional `canonical_path_receipt_hash`. The §4.2 SQL reads neither that receipt nor an extra Parquet column for those values, so they are explicitly excluded from the published-view contract and both schema fingerprints. Making any of them queryable requires a separately owned physical column or explicit receipt join; this draft invents neither. `strategy`, `symbol`, and `timeframe` remain in that commit envelope as well as being physically produced by Hive paths.

**[SUPERSEDED IN v1.8 — G102-F05; retained v1.6 text, untagged until this fold:]** **v1.6 controlling disposition:** “may bind” is not a member contract. B-10 blocks `CatalogCommitPreimageV1` until the complete required/absent-by-design run-envelope field set is ratified, and B-14 separately blocks the three routing values until their owner-produced typed receipt is named. Their exclusion from the published view remains a query-shape statement only; it supplies neither a hash preimage nor a value producer. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:76-95`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:498-510`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:52-86,268-291`)

**v1.8 controlling disposition for §3.4.2.** This paragraph was the one place in the draft where a v1.6 blocking claim survived the v1.7 fold untagged, and W198's residual sweep missed it because its pattern did not include `B-10 blocks` or `B-14 separately blocks`. The current state: **B-10 is closed** — “may bind” is replaced by the closed six-member table in §4.1.3, so the sentence that B-10 blocks `CatalogCommitPreimageV1` is superseded. **B-14 is closed** on the question it asked — the authority is named in §3.4.3 — but the three routing values are blocked again on the narrower **B-15**, which asks for the declared channel, not the authority. `battery_version` and `objective_id` are now marked absent by design (§4.1.3), `canonical_path_receipt_hash` remains absent by design, and `strategy`/`symbol`/`timeframe` are absent from item 2 and carried once in item 3's `path_slot`. Their exclusion from the published view remains a query-shape statement only. (§3.4.3; §4.1.3; §7 B-10; §7 B-14; §7 B-15)

Adding any view or receipt field as an actual `TrialRecord` model field is a WP-P0-04 schema-owner action, not a WP-P0-13 default. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:255,267`)

#### 3.4.3 Routing-value producer and path agreement (v1.7 — closes B-14; v1.8 — factory input withdrawn to B-15)

**Where the authority lives.** It is not P0-13, and it is not the Hive path. The authority is the
completed run's own cell coordinates. WP-P0-08 records the sole canonical emitter as
`mega_walk_forward.py`, whose persistence unit is already "One JSON result per strategy × symbol ×
timeframe cell", and whose "TrialRecord fields already present" column already begins with
"Dimensions"; the consolidated disposition makes that same emitter, after WP-P0-20 migration, the
single direct `TrialRecord` emitter and hence the sole direct caller of `TrialCatalogWriter`. A
completed run that has no strategy × symbol × timeframe cell coordinates cannot have been executed
as a cell, so the values are a property of the completed run, not an invention of the writer.
(`MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_08_WRITER_INVENTORY_2026-08-25/WRITER_INVENTORY.md:35,102`;
`C:\tmp\LANE_PROMPTS_20260828\DETECT_G99_BLOCKERS.md:71-73`)

**The three modules, with disjoint interfaces.** This is the same producer/observer/comparer shape
§3.4.1 already uses for `run_id` — `RunIdentityFactory`, `CommittedPathRunIdInspector`,
`PathRowRunIdComparer` — which the G93 fold repaired without needing a blocker.

1. **`RunCellDimensionsFactory` — sole value producer.**

   **[SUPERSEDED IN v1.8 — G102-F04; retained v1.7 text:]** "It consumes only the completed run's cell
   coordinates carried on the closed `CompletedRunInput` and emits exactly one immutable typed
   `RunCellDimensionsReceipt` of `{strategy, symbol, timeframe}`, each `NonEmptyStr` under the
   repository primitive."

   **v1.8 controlling text — the input is withdrawn, not replaced.** That sentence named an input this
   document does not declare. §2.1's closed `CompletedRunInput` field list contains no `strategy`,
   `symbol`, `timeframe`, or cell-coordinate member, and v1.7 marked all three **absent by design**
   from item 2's run envelope, so the factory has no declared typed input anywhere in this draft.
   WP-P0-08's "One JSON result per strategy × symbol × timeframe cell" is the persistence unit of the
   emitter, not a declared member of the writer's boundary type. v1.8 does **not** repair this by
   adding three members to `CompletedRunInput`: assembling an input list is the same act B-14 was
   opened to prevent, and a second assembled list that has survived a verification round is worse than
   the first. The channel is therefore withdrawn and opened as **B-15**. While B-15 is open,
   `RunCellDimensionsFactory` may not emit a receipt, the three Hive routing segments are again a
   blocked design target, and F-13 and R-8 may not be constructed. What survives unchanged and is not
   re-opened: the authority frame above, the three-module producer/observer/comparer shape, the
   factory's refusal rules below, and typed `PATH_RECEIPT_CELL_MISMATCH`. (§7 B-15;
   `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_08_WRITER_INVENTORY_2026-08-25/WRITER_INVENTORY.md:35`)

   The factory's refusal rules, unchanged from v1.7 and effective once B-15 names the channel: it
   emits exactly one immutable typed `RunCellDimensionsReceipt` of `{strategy, symbol, timeframe}`,
   each `NonEmptyStr` under the repository primitive, and refuses a missing coordinate, an empty or whitespace-only coordinate, a
   second differing value for the same coordinate within one completed run, and any attempt to
   default or derive a coordinate from a path, a filename, or a caller label. It cannot read staged
   parts, committed parts, or the candidate view. No other component may emit these three values.
   (`MTC_COMMAND_CENTER/contracts/mtc_contracts/base.py:16,59-67`)
2. **`CommittedPathCellInspector` — sole observed-value producer.** After staging, it reads only the
   Hive `strategy=`, `symbol=`, and `timeframe=` segments of each candidate part path and emits one
   typed observed receipt per part. It cannot read the factory receipt, the run envelope, or the
   Parquet row bytes.
3. **`PathReceiptCellComparer` — comparer that owns neither operand.** It belongs to neither
   producer, emits neither operand, and must receive both typed receipts. It refuses a missing
   receipt, a producer-identity alias, a missing path segment, an unequal value for any of the three
   dimensions, and differing values for the same dimension across parts of one commit, with
   `REFUSED(reason=PATH_RECEIPT_CELL_MISMATCH)`. Only its typed success receipt permits commit.
   Deriving the expected operand from the same path bytes being inspected is a refused
   same-producer-degenerate implementation even when the two values match.
   (`MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:617-628,681-687`)

**Corroboration, and its honest limit.** `symbol` has a second repository source: the run's
`StrategyPackage.instrument_metadata.symbol`, and P012's `InstrumentRecord` likewise carries `symbol`
in its closed member set. `RunCellDimensionsFactory` must refuse when its `symbol` differs from the
package's `InstrumentMetadata.symbol` for the same run. `strategy` and `timeframe` have **no** second
source: `StrategyPackage` has no strategy-name field and no timeframe, and P012's `InstrumentRecord`
member set contains neither. Their agreement is therefore proved only across the writer seam by
`PathReceiptCellComparer`, not against an independent catalogue; this is recorded as a limitation, not
as independent value proof. Citing P012 does not ratify WP-P0-12, which is DESIGN ONLY.
(`MTC_COMMAND_CENTER/contracts/mtc_contracts/package.py:18-24,27-45`;
`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:1-3,147-149,770-773`)

**Where the values are carried, once.** The three values are carried in the commit preimage exactly
once, through item 3's hash-free `path_slot`, which is the partition directory (§4.1.3). They are
therefore marked **absent by design** from item 2's run envelope: binding them twice would let two
honest implementations disagree about which copy the digest covers. The v1.5 sentence that they
"remain in that commit envelope as well as being physically produced by Hive paths" is superseded
above and is not restored.

**Falsification.** F-13 (writer arm) and R-8 (reader arm) in §§5.3-5.4 change exactly one Hive
dimension and require `PATH_RECEIPT_CELL_MISMATCH`; a one-check-deleted comparer accepts and is RED.
**v1.8 amendment (G102-F04):** both arms begin from "a valid committed package whose
`RunCellDimensionsFactory` receipt is fixed". No such receipt can be produced while **B-15** leaves
the factory with no declared input, so F-13 and R-8 are blocked design targets again — specified, not
constructible. Naming them here remains a build requirement, never closure evidence. (§7 B-15)

**v2.0 reader-side limit (GM66-F02).** F-13 is a writer-side arm: after B-15 closes, the live factory
receipt can be compared with the staged path before commit. R-8 is different. The committed package
stores the three coordinates only in item 3's path-derived `path_slot`; it does not commit the factory
receipt or another independent expected operand. A post-commit reader that derives both operands from
that path performs the same-source comparison §3.4.3 already refuses. R-8 therefore remains a blocked
design target under new **B-17** even after B-15 closes. B-17 does not close, narrow, or answer B-15.
(§4.1.3; §5.4; §7 B-15; §7 B-17;
`C:\tmp\LANE_PROMPTS_20260828\DETECT_GM66_P013.md:32-59`)

**What this does not decide.** Whether `strategy`, `symbol`, and `timeframe` become `TrialRecord`
columns remains the separate WP-P0-04 schema question in **B-03** and discrepancy **D-03**, both
unchanged by v1.7. This subsection adds no model field and no manifest field.
(`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:14-68`;
`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:255`)

## 4. Parquet layout and DuckDB queryability

### 4.1 Layout

```text
trial_catalog_v0/
  lineage=SIGNAL_SCREEN_ONLY/
    run_id=<run_id>/strategy=<strategy>/symbol=<symbol>/timeframe=<timeframe>/
      part-<catalog_commit_hash>-00000.parquet
  lineage=FULL_KERNEL_SIMULATION/                    # PROVISIONAL-ON-P020
    run_id=<run_id>/strategy=<strategy>/symbol=<symbol>/timeframe=<timeframe>/
      part-<catalog_commit_hash>-00000.parquet
  commits/<catalog_commit_hash>.json

artifacts/<package_hash>/<trial_id>/                 # per-trial address; manifest/path binding gated on B-09
  trades.parquet
  equity.parquet
  intents.jsonl
  levels.parquet
  manifest.json                                     # + trial_id, package_hash, evaluation_run_hash, param_hash
```

**[SUPERSEDED IN v1.7 — B-10/B-13/B-14 closed; retained v1.6 text:]** **v1.6 status of this layout.** Three of its elements are blocked design targets, not current design output: the `part-<catalog_commit_hash>-00000.parquet` names and the `commits/<catalog_commit_hash>.json` receipt depend on B-10 and B-13, and the `strategy=`, `symbol=`, and `timeframe=` segments depend on B-14. The `lineage=` and `run_id=` segments and the artifact tree are unaffected, and the artifact address remains gated on B-09 as before. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:52-86,204-233,268-291`)

**[SUPERSEDED IN v1.8 — G102-F04; retained v1.7 text:]** **v1.7 status of this layout.** Every element of the layout is now specified: the hash-bearing part names and the `commits/<catalog_commit_hash>.json` receipt are derivable from the closed §4.1.3 preimage, and the `strategy=`, `symbol=`, and `timeframe=` segments carry the §3.4.3 factory receipt under comparer agreement. The artifact address remains gated on **B-09** exactly as before, and nothing in this layout can be written while stage 3 halts on B-04/B-12. "Specified" here means the bytes and producers are named; it does not mean any path was created. (§3.4.3; §4.1.3; §4.2.1)

**v1.8 status of this layout.** Most of the layout is specified: the hash-bearing part names and the `commits/<catalog_commit_hash>.json` receipt are derivable from the closed §4.1.3 preimage, and the `lineage=` and `run_id=` segments have named producers and comparers. **One element is a blocked design target again:** the `strategy=`, `symbol=`, and `timeframe=` segments, whose value channel is open under **B-15** — the factory that owns those bytes has no declared input, so no path containing them may be derived. The artifact address remains gated on **B-09** exactly as before, and nothing in this layout can be written while stage 3 halts on B-04/B-12. "Specified" here means the bytes and producers are named; it does not mean any path was created. (§3.4.3; §4.1.3; §4.2.1; §7 B-15)

The row retains `run_id` and `simulator_class` inside Parquet; the path repeats them as routing facts. The structural lineage stamp has three required agreements: Hive `lineage`, row `simulator_class`, and the `simulator_class` value in the `evaluation_run_hash` preimage. The separate path/row `run_id` agreement is produced and checked only through `RunIdentityFactory`, `CommittedPathRunIdInspector`, and `PathRowRunIdComparer` in §3.4.1; it is not inferred from the lineage comparison or schema fingerprint. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:76-95,138-141`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:173-202`)

**[SUPERSEDED IN v1.6 — G93-F02; retained v1.5 text:]** The acceptance reader requires path/row equality, recomputes `evaluation_run_hash` from receipt preimage inputs plus the committed row class, re-validates dependent `trial_id`, checks the commit receipt, and — for the full partition — verifies `canonical_path_receipt_hash`. A mismatch is refused; no component rewrites only the row label.

**[SUPERSEDED IN v1.7 — B-11 closed; retained v1.6 text:]** **v1.6 controlling disposition:** the write-time formula remains the repository `compute_evaluation_run_hash(package_hash, dataset_manifest_sha, cost_model_json, simulator_class, simulator_version, evaluation_config_json)`, serialized by the repository identity module. The reader may not claim an independent recompute until B-11 names an owned committed home for all six members for every conserved trial, including unselected trials. Out-of-band writer state is forbidden. Path/row `run_id`, commit, dependent `trial_id`, and canonical-receipt checks remain separate, but no `EVALUATION_PREIMAGE_MISMATCH` acceptance claim or R-3 execution is available while B-11 is open. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:31-44,76-95`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:19,21,57`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:88-120`)

**v1.7 controlling disposition:** the write-time formula is unchanged — it is repository code, not a P0-13 choice. The committed home is now named: all six members are required members of the run envelope inside `CatalogCommitPreimageV1` (§4.1.3), and the receipt at `commits/<catalog_commit_hash>.json` already stores the exact typed preimage, so the reader recomputes `compute_evaluation_run_hash` from committed bytes alone. Because the receipt is run-level and stage 3 recomputes one `evaluation_run_hash` per completed run and then every dependent `trial_id`, the stored members cover every conserved trial in that run — selected and unselected alike — which is what `ArtifactManifest` could never do, since unselected trials have none and its `dataset_hash` is not `dataset_manifest_sha`. Out-of-band writer state remains forbidden: a builder who supplies `cost_model_json` or `evaluation_config_json` from write-time state rather than from the committed receipt is not reading committed evidence and the recompute is refused. `EVALUATION_PREIMAGE_MISMATCH` and R-3 are consequently available as specified arms. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:31-44,76-95,132-135`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:19,21,57,77-87`; §4.1.3; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G99_BLOCKERS.md:41-43`)

Selected-artifact addressing is per trial: `compute_package_hash` carries no trial sequence while `make_trial_id` does, so two selected trials can share a `package_hash`; each therefore commits under `artifacts/<package_hash>/<trial_id>/`, and its `manifest.json` carries `trial_id` plus the dependent identities (`package_hash`, `evaluation_run_hash`, `param_hash`) so `ArtifactCommitVerifier` has an independent committed operand. Adding `trial_id` and those identities to the manifest, and the per-trial address itself, are the WP-P0-04 schema-owner action in blocker **B-09**; the brief's Tier-2 layout shows only `artifacts/<package_hash>/` and the current `ArtifactManifest` carries neither `trial_id` nor `param_hash`, recorded as discrepancy **D-04**. The remaining manifest lineage — package, deployment, evaluation, dataset, kernel, simulator, control, allocation, and environment — follows the brief. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:54-73,76-95,132-135`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2050-2087`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:19,23-24,77-88`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_N81_P013_V12.md:7-12`)

#### 4.1.1 Retained superseded v1.5 commit-identity text

**[SUPERSEDED IN v1.6 — G93-F01/G93-F06; retained for provenance, not a computable contract:]** `CatalogCommitIdentity` is the sole hash producer. It computes `SHA256(canonical_json(CatalogCommitPreimageV1))`, where the closed preimage contains only:

1. preimage/contract versions and the expected DuckDB view schema fingerprint produced solely by `TrialCatalogViewSchemaProjector` from the frozen §3.4.1 published-view contract, without inspecting committed parts or the candidate view;
2. the run envelope **excluding** `catalog_commit_hash`;
3. an ordered part set of `{ordinal, hash-free path_slot, staged_byte_length, staged_sha256, row_count, ordered_trial_ids}`; and
4. an ordered selected-artifact set of `{trial_id, manifest_sha256, members:[{artifact_kind, byte_length, sha256}]}`.

**[SUPERSEDED IN v1.6 — retained continuation:]** The staged Parquet bytes contain no `catalog_commit_hash`, and `path_slot` ends at the partition directory plus part ordinal; neither includes a placeholder or final hash-bearing name. After hashing, `ParquetCommitter` deterministically maps each slot to `part-<catalog_commit_hash>-<ordinal:05d>.parquet` and the receipt to `commits/<catalog_commit_hash>.json`. The closed receipt stores the hash, exact preimage, and derived final-path mapping. `AcceptanceEvidenceReader` rehashes the preimage, re-derives every final path, verifies each committed part and selected-manifest digest/membership, and refuses unknown receipt fields. Thus a changed part byte, preimage/receipt field, final-path mapping, or selected-manifest member is DETECTED without any hash depending on itself. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_N70_P013_V11.md:14-19`; `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:617-687`)

#### 4.1.2 v1.6 controlling commit-identity disposition

**[SUPERSEDED IN v1.7 — B-10/B-13 closed; retained v1.6 text. The requirements it states — reject missing as well as unknown members, and expose an internally self-consistent omit-one modified copy that a mere rehash accepts — are carried forward verbatim into §4.1.3 and R-7, not dropped:]** The non-self-referential shape remains a required design property, but the v1.5 text is not executable: the run-envelope membership is open and the schema-fingerprint bytes are open. `CatalogCommitPreimageV1`, `CatalogCommitIdentity`, `catalog_commit_hash`, the hash-bearing final-path derivation, and R-1 are therefore blocked design targets until both B-10 and B-13 close. No implementation may hash the fields it happens to receive, omit a candidate envelope member, source an expected fingerprint from observed parts, or treat the stored receipt as proof that required members were present. Once the blockers close, the receipt must store the exact typed preimage, reject missing as well as unknown members, and expose a modified copy that omits one required member while all stored bytes are internally self-consistent; acceptance by a reader that merely rehashes the stored receipt is RED. The repository canonical serializer is UTF-8 JSON with sorted keys, compact separators, non-ASCII retained, decimals rendered with `format(..., "f")`, and NaN refused; this serializer does not decide the still-open member set. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:15-44`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:52-86,204-233`)

#### 4.1.3 v1.7 closed commit-identity preimage (closes B-10 and B-11)

**Recipe — cited, not invented.** `CatalogCommitIdentity` remains the sole hash producer and computes
`SHA256(canonical_json(CatalogCommitPreimageV1).encode("utf-8"))`. That is the repository's own
accepted identity encoding — UTF-8 JSON, lexicographically sorted keys, compact separators, non-ASCII
retained, `Decimal` rendered with `format(..., "f")`, enums and timestamps rendered as strings, NaN
refused — the same serializer every shipped identity formula already uses. v1.6 already named this
serializer for the commit preimage; v1.7 adds only the member set it serializes.
(`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:15-44`; `MTC_COMMAND_CENTER/contracts/README.md:48-55`)

**The four items are unchanged from the retained v1.5 shape in §4.1.1.** Item 1 is preimage/contract
versions plus the expected view-schema fingerprint, now closed by §4.2.1. Item 3 is the ordered part
set `{ordinal, hash-free path_slot, staged_byte_length, staged_sha256, row_count, ordered_trial_ids}`.
Item 4 is the ordered selected-artifact set `{trial_id, manifest_sha256, members:[{artifact_kind,
byte_length, sha256}]}`. What v1.6 withdrew, and what follows, is item 2.

**Item 2 — the run envelope, closed.**

**[SUPERSEDED IN v1.8 — G102-F03; retained v1.7 text:]** "`CatalogCommitPreimageV1.run_envelope` is a
P0-13-owned typed model with exactly these six members and no others. "Required" means the model has
no default and parsing refuses the member's absence; "absent by design" means the member is not
declared, so `extra="forbid"` refuses it if supplied. Both directions are enforced by the repository
contract base, which forbids extras and freezes the model.
(`MTC_COMMAND_CENTER/contracts/mtc_contracts/base.py:59-67`)"

**v1.8 controlling text — what the cited base actually contains, read this session.**
`MTC_COMMAND_CENTER/contracts/mtc_contracts/base.py:59-67` is the `ContractModel` class statement, its
docstring, and `ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True,
validate_default=True)`. It contains **no** required-member logic: refusal of an absent member comes
from declaring a field with no default in the envelope model itself, not from that span. Immediately
after it, at `base.py:69`, the same base declares `contract_version: str =
Field(default=CONTRACT_VERSION, pattern=r"^0\.1\.0$")` with `CONTRACT_VERSION = "0.1.0"` at
`base.py:12` and a validator refusing any other value at `base.py:71-78`. `canonical_json` serializes a
`BaseModel` through `model_dump(mode="python")`
(`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:16-17`), so every field the model declares —
inherited ones included — is in the digest.

**Consequence, stated plainly rather than argued away.** `CatalogCommitPreimageV1.run_envelope` is a
`ContractModel` subclass, so `canonical_json` serializes **seven** members: the six declared below plus
the inherited `contract_version`. The v1.7 sentence "exactly these six members and no others" was
false of the base it cited, and two honest implementations — one hashing a plain six-field model, one
hashing a `ContractModel` subclass — would produce different `catalog_commit_hash` values for the same
six evaluation members. The corrected member contract is: **the six P0-13-declared members below, plus
the inherited `contract_version`, and no others.** `contract_version` is already-written repository
state, not a v1.8 addition; §3.2 already lists it as a serialized row field with producer
`ContractRuntime`. No new member, type, or producer is introduced here.

**Honest limit on omission detection for the inherited member.** Because `contract_version` carries a
default, its absence from a stored receipt is **filled, not refused**: the typed parse supplies
`"0.1.0"`, the rehash then matches, and `COMMIT_PREIMAGE_MEMBER_MISSING` does not fire. R-7's omit-one
arm therefore covers the six declared members only, and this document does not claim otherwise. That
gap is bounded, not unchecked: `base.py:69`'s pattern and `base.py:71-78`'s validator admit exactly one
value, so a filled default can only ever be the value an honest implementation would have hashed. This
is an **ACCEPTED, not DETECTED** class, recorded here and in §9's re-audit list.
(`MTC_COMMAND_CENTER/contracts/mtc_contracts/base.py:12,62-67,69,71-78`;
`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:16-17,31-44`)

| Envelope member | Status | Type | Sole producer | Why |
|---|---|---|---|---|
| `package_hash` | **REQUIRED** | `Sha256` | `EvaluationIdentityFactory` | Member 1 of `compute_evaluation_run_hash`. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:78,89`) |
| `dataset_manifest_sha` | **REQUIRED** | `Sha256` | `EvaluationIdentityFactory` | Member 2 of the formula, and already the first name in the retained v1.5 "may bind" list. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:79,90`) |
| `cost_model_json` | **REQUIRED** | canonical-JSON `VARCHAR` | `EvaluationIdentityFactory` | Member 3. v1.6 recorded it as having no committed home anywhere; this row is that home. Not a new JSON document — it is the existing named function argument, stored. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:80,91`) |
| `simulator_class` | **REQUIRED** | `NonEmptyStr` | `EvaluationIdentityFactory`, receiving the value already locked by `LineageClassifier` | Member 4, and the operand of the structural lineage stamp. The factory may not accept a caller value. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:81,92`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:57`) |
| `simulator_version` | **REQUIRED** | `NonEmptyStr` | `EvaluationIdentityFactory` | Member 5, and the second name in the retained v1.5 "may bind" list. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:82,93`) |
| `evaluation_config_json` | **REQUIRED** | canonical-JSON `VARCHAR` | `EvaluationIdentityFactory` | Member 6. Like `cost_model_json`, v1.6 recorded no committed home; this row is that home. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:83,94`) |

| Candidate deliberately excluded | Status | Why it is absent by design |
|---|---|---|
| `catalog_commit_hash` | **ABSENT BY DESIGN** | Self-reference. The retained v1.5 shape already excluded it and v1.7 does not restore it. |
| `evaluation_run_hash` | **ABSENT BY DESIGN** | It is the digest of the six members above. Storing both the digest and its own preimage members inside one preimage would let a receipt be internally consistent while the six members disagree with the row value; instead the reader recomputes it from the six stored members and compares against the row, which is exactly R-3. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:76-95`) |
| `strategy`, `symbol`, `timeframe` | **ABSENT BY DESIGN** | Already carried once, in item 3's hash-free `path_slot`, which is the Hive partition directory; their value authority is the §3.4.3 factory receipt and their agreement is proved by `PathReceiptCellComparer`. Binding them twice would leave two honest implementations disagreeing about which copy the digest covers. (§3.4.3) |
| `run_id`, `lineage` | **ABSENT BY DESIGN** | Same reason: both are Hive path segments inside item 3's `path_slot`, and their agreement with the row is proved by `PathRowRunIdComparer` and by the structural lineage stamp respectively. (§3.4.1) |
| `canonical_path_receipt_hash` | **ABSENT BY DESIGN** | The draft already states it is absent by design for screening; a conditional member would make the closed set depend on lineage and would reappear as a nullable-or-conditional view column through `union_by_name`. Full-lineage runs prove the receipt through `P020CanonicalPathReceiptVerifier` and `CANONICAL_RECEIPT_MISSING_OR_INVALID`, not through the commit digest. (§3.4.1; §5.2) |
| `battery_version` | **ABSENT BY DESIGN (v1.7)** | Promoting it into the commit identity would freeze a P0-20 value while **B-01** is open. The current P0-20 battery definition is v1.5 and owner-gated, and no acceptance is claimed here. (`C:\tmp\LANE_PROMPTS_20260828\P020_STATISTICAL_BATTERY_DEFINITION_V1.md:1-4`) |
| `objective_id` | **ABSENT BY DESIGN (v1.7)** | Same reason against **B-07**: the objective and K are not fixed, and no approximate value becomes a default. (§7 B-07) |

**v2.1 qualification of the retained `objective_id` premise.** The owner premise in that v1.7 cell is
superseded: decision 87 fixes K at 20 per strategy/market/timeframe and expressly chooses a combined
rule rather than one score. `objective_id` nevertheless remains **ABSENT BY DESIGN** because the owner
did not name a scalar objective or authorize a new objective identity. B-07's engineering owner must
encode the combined rule as a versioned policy without manufacturing either; that engineering half
remains open. (`C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:744`; §7 B-07)

**v2.2 qualification of the retained v2.1 premise.** Decision 128 supersedes the market/timeframe
partition and the combined keep-group union. It requires an overall-robustness ranking inside each
strategy TYPE, but still does not name a scalar score or authorize an `objective_id`; that field
therefore remains **ABSENT BY DESIGN**. The policy version and evidence provenance required by the
`NEW-BY-ADDENDUM-32` item must be bound through an owned engineering contract, not inserted into this
closed preimage or manufactured as an objective identity. (`C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:870-876,900-912`; §2.1 stage 4; §7 B-07)

**One value per member.** The envelope carries exactly one value for each required member because
stage 3 recomputes one `evaluation_run_hash` for the completed run and then every dependent
`trial_id`. A completed run whose conserved rows would require a second distinct value for any
envelope member is refused before staging; the envelope is never widened to a set to accommodate one.
This is a stated refusal, not an assumption that the case cannot arise. (§2.1 private stage 3;
`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:132-135`)

**Omission is DETECTED without rehashing.** The defect B-10 named is that a reader which merely
rehashes the stored receipt cannot see an omitted required member, because the omitted member is
absent from the bytes it rehashes. `AcceptanceEvidenceReader` therefore parses the stored receipt
through the typed closed model **before** any digest work: a missing required member is refused with
`REFUSED(reason=COMMIT_PREIMAGE_MEMBER_MISSING)`, and an undeclared extra member is refused by
`extra="forbid"`. Only a receipt that parses completely is then rehashed and compared, yielding
`COMMIT_HASH_MISMATCH` for a changed byte. R-7 is the modified copy that omits exactly one required
member while every stored byte is internally self-consistent; a reader that only rehashes accepts it
and is RED. **v1.8 correction (G102-F03):** the cite for this paragraph was `base.py:59-67`, which is
the `ConfigDict` span and supplies only `extra="forbid"`; absence-refusal comes from the envelope
model declaring each of the six members without a default, and the arm covers those six only — the
inherited `contract_version` is defaulted and its absence is filled, as recorded under item 2 above.
(`MTC_COMMAND_CENTER/contracts/mtc_contracts/base.py:62-67,69,71-78`;
`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:14-68`)

**Scope of this closure.** This closes a P0-13-owned type. It is not a WP-P0-04 schema amendment: no
`TrialRecord` column, no `ArtifactManifest` field, and no identity function is added, and WP-P0-04's
own output list contains no catalog-commit envelope. If a later owner wants `battery_version`,
`objective_id`, or any other member inside `catalog_commit_hash`, that is a new question and a new
version of this preimage; nothing in the named sources requires it today.
(`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:255,320`;
`C:\tmp\LANE_PROMPTS_20260828\DETECT_G99_BLOCKERS.md:31-33,112`)

One completed run may write multiple Parquet parts for bounded memory, but no part becomes query-visible until the run’s conservation and identity checks pass. Each `trial_id` occurs exactly once across the commit. This preserves “one row per trial” without requiring one file per trial. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:412`; `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:963-967`)

### 4.2 DuckDB view and required query

The build must publish a read-only view equivalent to:

```sql
CREATE VIEW trial_catalog AS
WITH projected AS (
  SELECT * EXCLUDE (filename),
         regexp_extract(
           filename,
           'part-([0-9a-f]{64})-[0-9]{5}[.]parquet$',
           1
         ) AS catalog_commit_hash
  FROM read_parquet(
    'trial_catalog_v0/lineage=*/run_id=*/strategy=*/symbol=*/timeframe=*/part-*.parquet',
    hive_partitioning = true,
    union_by_name = true,
    filename = true
  )
  WHERE regexp_full_match(
          filename,
          '.*part-[0-9a-f]{64}-[0-9]{5}[.]parquet'
        )
),
covered_commits(catalog_commit_hash) AS (
  VALUES <publisher-injected validated receipt hashes in sorted order>
)
SELECT projected.*
FROM projected
JOIN covered_commits USING (catalog_commit_hash)
WHERE lineage = simulator_class;
```

The acceptance query for a rejected trial is:

```sql
SELECT trial_id, candidate_id, classification, rejection_reasons,
       simulator_class, deployment_identity_hash
FROM trial_catalog
WHERE list_contains(rejection_reasons, $reason);
```

`parameters` remains queryable through DuckDB JSON extraction from its canonical JSON column, while fixed fields and lists retain native Parquet types. The plan requires rejection-reason lookup, and the brief requires every trial to be locatable/filterable through the DuckDB layer. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:416`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2101-2123`)

**[SUPERSEDED IN v1.6 — G93-F06; retained v1.5 fingerprint text:]** `TrialCatalogViewSchemaProjector` is the sole producer of the expected logical-schema fingerprint. It projects exactly the frozen §3.4.1 published-view contract; it cannot read committed parts, inspect the candidate view, or accept a fingerprint supplied by `ParquetCommitter` or `DuckDBViewPublisher`. `CommittedDuckDBSchemaInspector` is the sole producer of the observed fingerprint and derives it only from the candidate view projection visible to queries, not from an unspecified merge with the underlying parts schema. `DuckDBSchemaFingerprintComparer` produces neither operand, belongs to neither producer, and must receive both typed receipts; it refuses a missing receipt, producer-identity alias, or unequal fingerprint. An implementation that derives “expected” from the same committed parts or candidate view used for “observed” is a refused same-producer-degenerate implementation, even when the two values match.

**[SUPERSEDED IN v1.7 — B-13 closed; retained v1.6 text:]** **v1.6 controlling fingerprint disposition:** the producer separation remains required, but none of the three modules may emit or compare a fingerprint while B-13 is open. The frozen published-view field set does not supply ordered schema-document bytes: logical type spelling, column order, nullability representation, nested `STRUCT` field representation, canonical serialization, and committed receipt storage remain unset. B-13 must close those bytes for both expected and observed receipts without allowing the expected producer to inspect the candidate view. Until then F-10 is a blocked design target, not closure evidence. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:31-44`; `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:617-628,681-687`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:204-233`)

**[SUPERSEDED IN v1.6 — G93-F06; retained v1.5 publication text:]** Only after that independent comparison does `DuckDBViewPublisher` consume the validated committed-receipt set, inject its sorted hashes into `covered_commits`, and check the exact glob. Its output is one read-only view plus a publication receipt whose `view_publication_hash` binds normalized SQL, both schema-fingerprint receipts, their comparison receipt, and the covered commit set. Re-publishing the same hash is a no-op. A new hash may atomically replace the view only when the new covered set is a strict superset and every prior hash remains; a changed SQL/schema for the same covered set or any dropped/unknown commit refuses. Build probes must show: absent publication makes the required query unavailable; a wrong glob omits a known committed `trial_id` and refuses coverage; F-10's changed projected schema is refused by the independent comparer; a wrong covered set refuses conservation; and a modified filename-extraction expression fails to join the receipt hashes.

**[SUPERSEDED IN v1.7 — B-13 closed; retained v1.6 text:]** **v1.6 controlling publication disposition:** `DuckDBViewPublisher` must not emit `view_publication_hash`, claim idempotence, or publish a hash-addressed view while B-13 is open. The phrase “normalized SQL” names neither bytes nor a producer. B-13 must ratify the closed `view_publication_hash` preimage, exact SQL serialization/normalization behavior, the sole producer of those bytes, and committed storage for every member. The eventual modified-copy matrix must distinguish a semantic schema/type change from a representation-only SQL change and state which is DETECTED and which is accepted; v1.6 does not invent that outcome. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:412,416`; `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:617-628,681-687`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:204-233`)

#### 4.2.1 v1.7 closed fingerprint and publication preimages (closes B-13)

**One recipe, chosen and cited.** Two already-written digest recipes were available and B-13 required
picking one:

- **(a) Repository canonical JSON.** `SHA256(canonical_json(value).encode("utf-8"))` — UTF-8 JSON,
  sorted keys, compact separators, non-ASCII retained, decimals via `format(..., "f")`, NaN refused,
  documented as the identity encoding for every `SHA256(A ‖ B …)` formula in the package.
  (`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:31-44`; `MTC_COMMAND_CENTER/contracts/README.md:48-55`)
- **(b) P012 §5.1 exact-file bytes.** A UTF-8 JSON file with no BOM, LF endings, a required final LF,
  and a detached `<file>.sha256` holding the lower-case SHA-256 of those exact file bytes, never
  embedded in the bytes it hashes. (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:132-134`)

**v1.7 picks (a), and here is why.** First, the schema fingerprint has no file: the expected document
is projected in memory by `TrialCatalogViewSchemaProjector` from the §3.4.1 contract and the observed
document in memory by `CommittedDuckDBSchemaInspector` from the candidate view, so recipe (b) would
require inventing a file, a writer for it, and a sidecar — the manufacture B-13 exists to prevent.
Second, the expected fingerprint is item 1 of `CatalogCommitPreimageV1`, which §4.1.3 already
serializes with `canonical_json`; using a second dialect inside one digest would put two
serializations in one preimage. Third, recipe (a) is shipped, accepted repository code under WP-P0-04's
T1 PASS record, while `P012_FRESH_DESIGN_V1.md` is explicitly DESIGN ONLY and citing it here would not
ratify it. Fourth, (a) leaves the implementer no layout choice at all: key order and separators are
fixed by the serializer, so two honest implementations cannot disagree. No third recipe is invented.
(`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:31-44`; `C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:1-3`;
`git-object:fead492b0b87f207aa6e7a259372b9767d4301f9:7,17-19`)

**`PublishedViewSchemaDocumentV1` — the closed schema document, defined here.** A typed model with
exactly two members: `document_version` and `columns`. `columns` is an **ordered array**;
`canonical_json` sorts object keys but preserves array order, so column order is part of the digest.
(`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:34-40`)

**v1.8 statement about `document_version` (G102-F02).** This member is **coined by this design**. It
appears in no already-frozen column table, in neither cited digest recipe, and in no prior version of
this draft; v1.7 introduced it inside a set described as closed while naming no value, no type, and no
producer for it, which would let two honest implementations put `"1"`, `"v1.7"`, or `"0.1.0"` into the
same otherwise-identical document and derive different fingerprints for the identical production
template — the exact defect B-13 was opened to prevent. v1.8 does not withdraw the member and does not
assemble a different member list; it states what a member needs:

- **Type:** `NonEmptyStr` under the repository primitive (`MTC_COMMAND_CENTER/contracts/mtc_contracts/base.py:16`).
- **Value:** the literal `"1"`, matching the `V1` in the type name. It is a design constant, not a
  runtime or environment value, and no producer may compute it.
- **Sole producers:** `TrialCatalogViewSchemaProjector` on the expected side and
  `CommittedDuckDBSchemaInspector` on the observed side each emit the same constant, because both
  serialize the same closed document shape; an unequal `document_version` between the two operands is
  a `SCHEMA_FINGERPRINT_MISMATCH` like any other member difference.
- **Change rule:** altering the member set or the ordering rules of this document requires a new type
  name and a new literal. That is a new version of this design, not a runtime choice.

This is a v1.8 design act, plainly labelled. It is listed in §9 for re-audit.

1. **Order.** Exactly the §3.2 top-level fields in §3.2 table order (48 entries), followed by the five
   §3.4.1 view-only columns in §3.4.1 table order. No other column may appear.
2. **Each entry** is `{name, type, nullable}`, plus `fields` for the one nested entry.
3. **`nullable`** is `false` for a §3.2/§3.3/§3.4.1 "Nullable?" cell of `No` and `true` for `Yes`.
4. **Nested struct stays nested.** `environment_lineage` carries `type: "STRUCT"` and a `fields` array
   holding the seven §3.3 nested fields in §3.3 table order, each `{name, type, nullable}`. It is
   never flattened; §3.4.1 already requires the nested struct in the frozen contract.
5. **Type vocabulary.**

   **[SUPERSEDED IN v1.8 — G102-F01; retained v1.7 text:]** "**Type vocabulary** is exactly the
   distinct spellings already present in the §3.2/§3.3 Parquet-type cells, with the design-intent
   length qualifier removed so both producers can emit the same string: `VARCHAR`, `BIGINT`, `DOUBLE`,
   `BOOLEAN`, `LIST<VARCHAR>`, `LIST<DOUBLE>`, `LIST<BIGINT>`, `STRUCT`. The two §3.4.1 columns whose
   Type cell is prose take the §3.2 spelling for the same logical type — `non-empty string` →
   `VARCHAR`, `SHA-256` → `VARCHAR`. No new dialect word is introduced."

   **v1.8 controlling text — the vocabulary is defined here, and this says so.** The eight-word list is
   unchanged and no new dialect word is introduced, but the sentence "exactly the distinct spellings
   already present" was not true of the tables it cited. The §3.2 Parquet-type cells also contain
   `dictionary VARCHAR` (`search_regime`, `simulator_class`, `classification`), `canonical-JSON
   VARCHAR` (`parameters`), and `canonical decimal VARCHAR` (`fee_bps_used`) — three spellings that
   are neither in the eight-word list nor the disclosed `VARCHAR(64)` qualifier. **P0-13 defines this
   vocabulary here**, by one stated rule applied to the already-written cells:

   > Each Parquet-type cell is read as a physical type word optionally preceded by a design-intent
   > annotation (`dictionary`, `canonical-JSON`, `canonical decimal`) or followed by a contract-level
   > length qualifier (`(64)`). The **physical type word alone** is the vocabulary entry. `dictionary
   > VARCHAR`, `canonical-JSON VARCHAR`, `canonical decimal VARCHAR`, and `VARCHAR(64)` therefore all
   > collapse to `VARCHAR`.

   **Already-written:** the eight physical type words themselves, and every cell the rule is applied
   to. **Added by this design:** the rule that collapses annotation and qualifier, and the resulting
   closed eight-word set. An implementer who copies the §3.2 cells verbatim and an implementer who
   copies the eight-word list would otherwise mint different `PublishedViewSchemaDocumentV1` bytes for
   the same production view, so the honest GREEN baseline B-13 demanded would not be one baseline; the
   rule above is what makes it one. The consequence of the collapse is stated in the DETECTED/accepted
   matrix below and is not hidden: a dictionary-encoded versus plain `VARCHAR` column and a
   `VARCHAR(64)` versus `VARCHAR` column are **ACCEPTED, not DETECTED** by this fingerprint.
   (`draft` §3.2 rows `search_regime`, `parameters`, `fee_bps_used`, `simulator_class`,
   `classification`; §9 re-audit list)

**Why the length qualifier is dropped, stated plainly.** §3.2 spells `Sha256` columns `VARCHAR(64)`
and `NonEmptyStr` columns `VARCHAR`. That distinction is a contract-level one — it comes from
`Sha256` versus `NonEmptyStr` in the repository base module, not from a Parquet physical type. The
observed producer may derive its operand **only** from the candidate view projection and is forbidden
to merge the Parquet parts schema into it, so it cannot be required to reproduce a qualifier the
contract, not the view, supplies. Keeping `VARCHAR(64)` on the expected side alone would make the
honest baseline permanently unequal. v1.7 therefore uses the unqualified spelling on both sides and
records the consequence below rather than hiding it. Whether a DuckDB candidate view can report a
length qualifier at all is **NOT VERIFIED** by this lane: no execution occurred.
(`MTC_COMMAND_CENTER/contracts/mtc_contracts/base.py:15-16`; §2.1 private stage 9)

**Both fingerprints.** `expected_schema_fingerprint = SHA256(canonical_json(document))` produced solely
by `TrialCatalogViewSchemaProjector` from §3.4.1, which may not read committed parts or the candidate
view. `observed_schema_fingerprint = SHA256(canonical_json(document))` over the same closed document
shape, produced solely by `CommittedDuckDBSchemaInspector` from the query-visible candidate view
projection. `DuckDBSchemaFingerprintComparer` produces neither, must receive both typed receipts, and
refuses a missing receipt, a producer-identity alias, or unequal fingerprints with
`SCHEMA_FINGERPRINT_MISMATCH`. Deriving both from the same view remains a refused
same-producer-degenerate implementation even on matching inputs.

**Committed storage for every member.** The expected fingerprint is item 1 of the commit preimage and
is therefore stored in `commits/<catalog_commit_hash>.json` (§4.1.3). The observed fingerprint, the
comparison receipt, and the full `view_publication_hash` preimage are stored in the publication
receipt that `DuckDBViewPublisher` emits alongside the view.

**`ViewPublicationPreimageV1` — the closed publication preimage, defined here.** Exactly five members,
hashed by the same recipe: `{publication_version, published_sql_text, expected_schema_fingerprint,
observed_schema_fingerprint, covered_commit_hashes}`.

**v1.8 statement about `publication_version` (G102-F02).** Like `document_version`, this member is
**coined by this design**. v1.5 bound `view_publication_hash` to "normalized SQL, both
schema-fingerprint receipts, their comparison receipt, and the covered commit set" — that list has no
`publication_version` — and v1.7 added the member to a set it called closed without naming a value, a
type, or a producer. The same repair applies and nothing is re-assembled around it: **type**
`NonEmptyStr` (`MTC_COMMAND_CENTER/contracts/mtc_contracts/base.py:16`); **value** the literal `"1"`,
matching the `V1` in the type name; **sole producer** `DuckDBViewPublisher`, which emits it as the
design constant it is and may not compute it; **change rule** altering this member set requires a new
type name and a new literal. Listed in §9 for re-audit. If this preimage is also a `ContractModel`
subclass, the inherited `contract_version` is a sixth serialized member on the same terms recorded in
§4.1.3 item 2, and the same ACCEPTED-not-DETECTED limit on its omission applies. `covered_commit_hashes` is the ordered sorted
array the §4.2 template injects into `covered_commits`. `published_sql_text` is the exact character
sequence `DuckDBViewPublisher` emits — the §4.2 template with the sorted validated receipt hashes
injected — carried as a single JSON string member, so its content survives serialization verbatim.
`DuckDBViewPublisher` is the **sole producer** of those bytes; no other component may emit, rewrite,
or re-indent them. Re-publishing an identical preimage yields an identical digest, so "re-publishing
the same hash is a no-op" is now a computable identity rather than a claim.

**The word "normalized" is retired.** v1.5 said `view_publication_hash` binds "normalized SQL". That
phrase named neither bytes nor a producer, which is half of what B-13 asked. v1.7 replaces it with
`published_sql_text` and applies **no** normalization transform: the member is the emitted text as
emitted. The comparison receipt is not a member because both fingerprints it compares are already
members; binding its identifier as well would add a member no reader could independently recompute.

**DETECTED versus accepted — the matrix B-13 required.**

| Modified copy, one operand changed | Outcome | Why |
|---|---|---|
| A projected column added to or dropped from the candidate view (F-10) | **DETECTED** | The `columns` array differs, so the observed digest differs. |
| Two columns reordered in the candidate view projection | **DETECTED** | `canonical_json` preserves array order. |
| A column's nullability changed | **DETECTED** | `nullable` is a member value. |
| A column's logical type changed across the vocabulary, e.g. `BIGINT` → `DOUBLE`, or `LIST<VARCHAR>` → `VARCHAR` | **DETECTED** | `type` is a member value. |
| `environment_lineage` flattened into seven top-level columns | **DETECTED** | Both the `columns` array and the nested `fields` array change. |
| Type spelling changed only between `VARCHAR(64)` and `VARCHAR` for a `Sha256` column | **ACCEPTED — not DETECTED here** | The qualifier is dropped from the vocabulary, for the reason stated above. This class is caught instead by the `Sha256` pattern on the row contract, which refuses a value that is not 64 lower-case hex, and by `IdentityValidator`. It is **not** silently unchecked, but it is not this fingerprint's check. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/base.py:13,15`) |
| **(v1.8 row, G102-F01)** A column's design-intent annotation changed — `dictionary VARCHAR` → plain `VARCHAR`, `canonical-JSON VARCHAR` → plain `VARCHAR`, or `canonical decimal VARCHAR` → plain `VARCHAR` | **ACCEPTED — not DETECTED** | The v1.8 collapse rule in item 5 reduces every such cell to the physical word `VARCHAR`, so the `type` member does not change. This class is caught instead where the annotation is actually enforced: canonical-JSON and canonical-decimal lowering are refused at write time by §3.1's encoding rules, and dictionary encoding is a physical storage choice this fingerprint never claimed to cover. Stated so a later reader does not treat the collapse as free. (§3.1) |
| Whitespace, indentation, or key order changed in a schema-document *representation* | **ACCEPTED — not DETECTED** | The document is re-serialized by `canonical_json` before hashing, so layout is not part of the preimage. This is the deliberate consequence of choosing recipe (a) over recipe (b), which would have DETECTED it. |
| Whitespace or indentation changed in the published SQL | **[SUPERSEDED IN v1.8 — G102-F06; retained v1.7 cell:]** "**DETECTED**" — **v1.8: NOT DETECTED by any named check in this design** | **[RETENTION COMPLETED IN v1.9 — W215; the v1.8 tag retained only the Outcome word, so the v1.7 “Why” cell is restored here, quoted from the verification that recorded it (`C:\tmp\LANE_PROMPTS_20260828\DETECT_G102_P013_CLOSURES.md:101`):]** “`published_sql_text` is the exact emitted character sequence inside a JSON string member; no normalization runs. A representation-only SQL edit therefore changes `view_publication_hash`.” **v1.8 controlling text, unchanged:** `published_sql_text` is the exact emitted character sequence inside a JSON string member and no normalization runs, so a representation-only SQL edit does change the *digest value*. But changing a digest is not detecting a change. `DuckDBViewPublisher` is the sole producer of the SQL bytes **and** the producer of `view_publication_hash` over them, so a publisher that re-indents and re-hashes is internally consistent and nothing named would fail. Unlike the two schema fingerprints, which have `DuckDBSchemaFingerprintComparer` producing neither operand, `view_publication_hash` has no independent comparer: §4.2.2's reader recomputes the commit digest and the evaluation digest and **does not** recompute the publication hash, and no R- or F-arm changes only SQL whitespace. v1.8 does not repair this by promising a reader-side recompute — a prose promise of a check is not a check. The gap is recorded here and in §9. |
| The `regexp_extract` filename expression changed | **DETECTED** | It is inside `published_sql_text`, and separately the changed extraction fails to join the injected receipt hashes. |
| A commit hash added to or removed from the covered set | **DETECTED** | `covered_commit_hashes` is a member. |

**v1.8 note — which rows of this matrix have an independent check, and which do not (G102-F06).** The
first five rows turn on the two schema fingerprints, and those have a named comparer that produces
neither operand (`DuckDBSchemaFingerprintComparer`, with `TrialCatalogViewSchemaProjector` and
`CommittedDuckDBSchemaInspector` as the two independent producers), so "DETECTED" there names a check
that can fail. The last three rows turn on `view_publication_hash`, whose preimage bytes and whose
digest are both produced by `DuckDBViewPublisher`. For those rows "DETECTED" may only be read as "the
digest value changes", never as "a named component would refuse", with one exception: the
`regexp_extract` row has a second and genuinely independent failure path — a changed extraction fails
to join the publisher-injected receipt hashes, so the required query returns no rows — and it is that
second path, not the digest, which makes the row a check. This limit is stated rather than repaired:
supplying an independent recompute of `view_publication_hash` would mean naming a reader-side operand
producer, and this fold does not assemble one to make a finding go away.

**v1.7 controlling publication disposition:** `DuckDBViewPublisher` emits `view_publication_hash` over
`ViewPublicationPreimageV1`, publishes only after the independent fingerprint comparison succeeds, and
retains the v1.5 replacement rule — a new hash may atomically replace the view only when the new
covered set is a strict superset and every prior hash remains; a changed SQL or schema for the same
covered set, or any dropped or unknown commit, refuses. None of this is reachable while stage 3 halts
on B-04/B-12, and build remains gated on B-01.
(`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:412,416`;
`MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:617-628,681-687`;
`C:\tmp\LANE_PROMPTS_20260828\DETECT_G99_BLOCKERS.md:61-63`)

#### 4.2.2 Acceptance-bearing reader separation

**[SUPERSEDED IN v1.6 — G93-F01/G93-F02/G93-F06; retained v1.5 reader text:]** The acceptance-bearing reader is a separate module from `TrialCatalogWriter`. It reads commit receipts and full-lineage Parquet, independently recomputes the commit, evaluation, and trial identities from committed preimage inputs, and does not import the writer’s classifier or accept a caller-provided `simulator_class`.

**[SUPERSEDED IN v1.7 — B-10/B-11/B-13 closed; retained v1.6 text:]** **v1.6 controlling reader disposition:** separation from `TrialCatalogWriter` and refusal of caller-provided `simulator_class` remain required, but independent commit recompute is blocked on B-10/B-13 and independent evaluation recompute is blocked on B-11. The reader may not import out-of-band write-time state to bypass either blocker. Dependent `trial_id`, lineage, canonical-receipt, and path/row `run_id` checks remain separately specified. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:76-95,132-141`; `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:617-628,681-687`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:52-120,173-233`)

**v1.7 controlling reader disposition:** separation from `TrialCatalogWriter` and refusal of caller-provided `simulator_class` are unchanged. Independent commit recompute is now specified: the reader parses the stored receipt through the closed §4.1.3 model, refuses a missing member before any digest work, then rehashes the exact preimage with `canonical_json` and re-derives every final path. Independent evaluation recompute is now specified: the reader calls `compute_evaluation_run_hash` over the six committed envelope members and compares against the row value. The reader still may not import out-of-band write-time state for any operand — that prohibition is what makes the committed home load-bearing, and it survives the closure. Dependent `trial_id`, lineage, canonical-receipt, path/row `run_id`, and path/receipt cell checks remain separately specified. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:31-44,76-95,132-141`; §3.4.3; §4.1.3; §4.2.1)

**v1.9 amendment to the reader disposition (W215-F02).** One clause of the v1.7 sentence above is
narrowed, and the rest stands. **[SUPERSEDED IN v1.9 — W215-F02; retained v1.7 clause:]** “path/receipt
cell checks remain separately specified.” **v1.9:** the check is specified but **unavailable** while
**B-15** leaves `RunCellDimensionsFactory` without a declared input, so `PathReceiptCellComparer` can
receive only one of its two operands and can neither succeed nor refuse (§5.2's taxonomy already
records `PATH_RECEIPT_CELL_MISMATCH` as an unavailable reason). More than that: because §4.1's layout
puts `strategy=`, `symbol=`, and `timeframe=` in every part path and §4.1's v1.8 status of that layout
already says “no path containing them may be derived”, **the reader has no committed package to read at
all** while B-15 is open. The commit, evaluation, dependent-`trial_id`, lineage, canonical-receipt, and path/row `run_id`
checks are unchanged as specifications; what v1.9 withdraws is any suggestion that a reader arm can be
constructed while B-15 stands. (§4.1; §5.2; §5.3; §5.4; §7 B-15)

**v2.0 amendment to the reader disposition (GM66-F02).** The v1.9 B-15 block remains, but it is not the
only reason the cell check is unavailable. After B-15 supplies a declared factory input, the reader
still cannot perform R-8 from committed bytes because the expected factory receipt is not committed.
The path is the observed operand and cannot also supply the expected operand. B-17 asks for the missing
committed home; until it closes, no reader-side `PATH_RECEIPT_CELL_MISMATCH` verification is claimed.
(§3.4.3; §4.1.3; §5.4; §7 B-17)

## 5. Structural lineage enforcement and D026 fixture

### 5.1 Structural rule

`LegacySignalScreenRunAdapter` possesses only a `ScreenSinkCapability`; that opaque capability selects `lineage=SIGNAL_SCREEN_ONLY` and causes `LineageClassifier` to lock the row/preimage class to the same constant before `EvaluationIdentityFactory` runs. Its interface has no lineage argument and no full-sink path. `MigratedCanonicalRunAdapter` can obtain `FullEvidenceSinkCapability` only from a successful `P020CanonicalPathReceiptVerifier`. **PROVISIONAL-ON-P020:** the full capability, receipt issuer/shape, and full-kernel preimage remain undefined until P0-20 accepts. The stand-in/unmigrated path can never obtain the full capability through a manifest label, and a receipt already bound to a different class is refused. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:76-95`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:498-510`)

The present WP-P0-04 field is only `NonEmptyStr`, so the writer seal, physical sink capability, and independent acceptance receipt are all required; trusting the field string alone would be convention, not structure. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:57`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/base.py:15-16`)

### 5.2 Two proof producers

The D026 proof deliberately has two producers:

1. **Observed-row producer:** production `LegacySignalScreenRunAdapter → TrialCatalogWriter`, which produces the committed screening row and commit receipt.
2. **Admissibility-verdict producer:** separate `AcceptanceEvidenceReader → P020CanonicalPathReceiptVerifier`, which produces `ACCEPTED` or typed `REFUSED(reason=...)` from the committed location, path lineage, row class, recomputed identities, commit receipt, and canonical-path receipt. It is forbidden to import `TrialCatalogWriter` or `LineageClassifier` and does not reuse the row producer’s decision. **PROVISIONAL-ON-P020** for the canonical receipt verifier. Durable Pattern 10 requires a check that can fail; §§5.3-5.4 name the modified copy for each structural operand. (`MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:617-628,681-687`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_N70_P013_V11.md:7-12`)

**[SUPERSEDED IN v1.6 — G93-F05; retained v1.5 taxonomy text:]** The acceptance-reader refusal taxonomy is a closed P0-13 system taxonomy, distinct from the still-**PROVISIONAL-ON-P020** trial-rejection taxonomy in B-06. Bare `REFUSED` is forbidden. Exactly these five reasons exist: `COMMIT_HASH_MISMATCH`, `PATH_ROW_LINEAGE_MISMATCH`, `EVALUATION_PREIMAGE_MISMATCH`, `TRIAL_ID_MISMATCH`, and `CANONICAL_RECEIPT_MISSING_OR_INVALID`. Each reason names the independently recomputed predicate that failed; no reason is inferred from another check’s output.

**[SUPERSEDED IN v1.7 — taxonomy extended to eight; retained v1.6 text:]** **v1.6 controlling taxonomy:** the taxonomy is closed and contains exactly **six** reasons: `COMMIT_HASH_MISMATCH`, `PATH_ROW_LINEAGE_MISMATCH`, `PATH_ROW_RUN_ID_MISMATCH`, `EVALUATION_PREIMAGE_MISMATCH`, `TRIAL_ID_MISMATCH`, and `CANONICAL_RECEIPT_MISSING_OR_INVALID`. `PATH_ROW_RUN_ID_MISMATCH` is emitted only by `PathRowRunIdComparer` (§3.4.1) and is never inferred from, folded into, or masked by `PATH_ROW_LINEAGE_MISMATCH`; the two operands are produced by `RunIdentityFactory` and `CommittedPathRunIdInspector` respectively. Bare `REFUSED` remains forbidden and each reason still names the independently produced predicate that failed. Two of the six are not available while their blockers are open: `COMMIT_HASH_MISMATCH` requires the closed commit preimage (B-10) and schema-fingerprint bytes (B-13), and `EVALUATION_PREIMAGE_MISMATCH` requires committed storage for all six evaluation-preimage members (B-11). Until those close, §5.2's second producer may recompute and refuse only on path lineage, path/row `run_id`, dependent `trial_id`, and the canonical-path receipt; it may not substitute out-of-band write-time state for a committed operand, and no `ACCEPTED` verdict from it is acceptance evidence. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_N70_P013_V11.md:7-12`; `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:617-687`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:76-95,132-141`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:88-120,173-202`)

**v1.7 controlling taxonomy:** the taxonomy remains a closed P0-13 system taxonomy, distinct from the
still-**PROVISIONAL-ON-P020** trial-rejection taxonomy in B-06, and now contains exactly **eight**
reasons: `COMMIT_PREIMAGE_MEMBER_MISSING`, `COMMIT_HASH_MISMATCH`, `PATH_ROW_LINEAGE_MISMATCH`,
`PATH_ROW_RUN_ID_MISMATCH`, `PATH_RECEIPT_CELL_MISMATCH`, `EVALUATION_PREIMAGE_MISMATCH`,
`TRIAL_ID_MISMATCH`, and `CANONICAL_RECEIPT_MISSING_OR_INVALID`. Bare `REFUSED` remains forbidden and
each reason still names the independently produced predicate that failed; no reason is inferred from,
folded into, or masked by another.

- `COMMIT_PREIMAGE_MEMBER_MISSING` is emitted only by the reader's typed parse of the stored receipt
  against the closed §4.1.3 model, strictly **before** any rehash, and is never emitted by
  `CatalogCommitIdentity`. It is what makes an omitted required member DETECTED at all: the digest
  cannot see it, because the omitted member is absent from the bytes the digest covers.
- `PATH_RECEIPT_CELL_MISMATCH` is emitted only by `PathReceiptCellComparer` (§3.4.3), whose operands
  come from `RunCellDimensionsFactory` and `CommittedPathCellInspector`. It is never folded into
  `PATH_ROW_LINEAGE_MISMATCH` or `PATH_ROW_RUN_ID_MISMATCH`. **v1.8 (G102-F04):** the reason stays in
  the closed taxonomy, but it is unavailable while **B-15** leaves `RunCellDimensionsFactory` without a
  declared input — the comparer cannot receive one of its two required operands, so it can neither
  succeed nor refuse. The taxonomy count is unchanged at eight. (§7 B-15)
- The two reasons v1.6 marked unavailable are now available as specified arms: `COMMIT_HASH_MISMATCH`
  has its closed preimage (§4.1.3) and its embedded schema fingerprint (§4.2.1), and
  `EVALUATION_PREIMAGE_MISMATCH` has committed storage for all six members (§4.1.3). "Available" means
  specified, not executed — no arm is executed in a design lane, and none can run while B-04 and B-12
  leave two required row identities unemittable.

(`MTC_COMMAND_CENTER/contracts/mtc_contracts/base.py:59-67`;
`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:31-44,76-95,132-141`;
`MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:617-687`;
`MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/TESTS.md:3-14`)

**v2.0 taxonomy limit (GM66-F02).** The eight-name taxonomy is retained as the intended closed system
taxonomy, but `PATH_RECEIPT_CELL_MISMATCH` is not an executable reader reason while either B-15 or
B-17 is open. B-15 withholds the factory receipt at write time; B-17 records that no independent
expected-coordinate operand is committed for a later reader. The writer-side F-13 comparer can become
executable when B-15 closes; the reader-side R-8 reason additionally requires B-17 to close. (§3.4.3;
§5.4; §7 B-15; §7 B-17)

### 5.3 Fixture arms to execute during build

No arm is claimed executed in this design lane. Build evidence must later record exact commands and real RED/GREEN output; prose or counts alone are supplemental. (`MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/TESTS.md:3-14`; `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:658-687`)

**[SUPERSEDED IN v1.7 — B-10/B-11/B-13 closed; retained v1.6 text:]** **v1.6 arm availability.** F-4 and R-1 depend on the commit digest and are blocked design targets while B-10 or B-13 is open; F-10 depends on the two schema-fingerprint byte formulas and is a blocked design target while B-13 is open; R-3 depends on committed evaluation-preimage storage and is a blocked design target while B-11 is open. A blocked arm may not be constructed, executed, or counted as closure evidence, and no substitute arm may be built from out-of-band write-time state. F-11 and F-12 are new v1.6 arms and are not blocker-gated. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:52-120,144-233`; `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/TESTS.md:3-14`)

**v1.7 arm availability.** F-4, F-10, R-1, and R-3 are no longer blocked design targets: their missing
byte formulas and their missing committed storage are supplied by §4.1.3 and §4.2.1. F-13, R-7, and
R-8 are new v1.7 arms. **No arm is claimed executed, and no arm can be executed yet:** every fixture
that requires an assembled `TrialRecord` — which is all of them except the boundary probes F-2 and
F-3 — still cannot be constructed while **B-04** and **B-12** leave `param_hash` and
`preregistered_space_hash` with no emittable value, and **B-01** still gates build. What changed is the
*reason* an arm cannot run: it is no longer "the design does not say what to hash or where the bytes
live", it is "two required row identities have no ratified preimage". Naming an arm here remains a
build requirement, never closure evidence. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:24,28`;
`MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/TESTS.md:3-14`; §4.1.3; §4.2.1)

**v1.8 arm availability (G102-F04/G102-F06).** Two corrections to the paragraph above. **First**, F-13
and R-8 are blocked design targets again: both begin from a fixed `RunCellDimensionsFactory` receipt,
and **B-15** leaves that factory with no declared input, so neither arm may be constructed or counted.
F-4, F-10, R-1, and R-3 are unaffected and remain specified-but-unexecutable for the B-04/B-12 reason
above. **Second**, no arm anywhere in §§5.3-5.4 changes only the whitespace of the published SQL, so
the publication-hash row of §4.2.1's matrix has no falsifying input; that is recorded as a gap, not
filled with an invented arm. (§7 B-15; §4.2.1)

**v1.9 arm availability (W215-F02) — B-15's block is wider than the two arms v1.8 named.** The v1.8
paragraph above applied B-15 to F-13 and R-8 and to nothing else. **[SUPERSEDED IN v1.9 — W215-F02;
retained v1.8 sentence:]** “F-4, F-10, R-1, and R-3 are unaffected and remain
specified-but-unexecutable for the B-04/B-12 reason above.” **v1.9:** that is too narrow, and the draft
already contains the reason. §4.1's layout puts `strategy=<strategy>/symbol=<symbol>/timeframe=<timeframe>`
in **every** part path, §3.4.1's v1.8 controlling disposition says no committer may mint those values,
and §4.1's v1.8 status of the layout says “no path containing them may be derived”. While **B-15** is
open there is therefore **no staged part, no committed part, no commit receipt, and no published view**
— so every arm whose input is one of those is additionally a blocked design target under B-15, not
only F-13 and R-8. Stated as a rule and then applied, rather than asserted arm by arm: *an arm is
blocked by B-15 if its baseline or its modified copy is a staged or committed Parquet part, a commit
receipt, or the candidate/published view*, because item 3's `path_slot` **is** the Hive partition
directory and that directory contains the three segments. Applying it: **F-1, F-4, F-5, F-7, F-10,
F-11, F-12, F-13** and **R-1 through R-8** are blocked, and **F-6** with them because it is defined
over the R arms. The exceptions are the writer-boundary probes that refuse before any part is staged
or any path is derived — **F-2**, **F-3**, and **F-8**. **F-9** is left undecided here rather than
counted either way: its committed bytes are the selected-artifact tree
`artifacts/<package_hash>/<trial_id>/`, which carries no routing segment, so whether B-15 reaches it
turns on whether its completed run must reach catalog commit at all — a question this lane does not
answer and §9 hands to the reviewer. This changes no arm's specification and adds no blocker: it
records that B-15's consequence reaches the fixture set, which is what §4.1 and §3.4.1 already imply
and what §5.3 did not say. The B-04/B-12 reason above is unchanged and independent of it.
(§3.4.1; §4.1; §4.1.3; §7 B-15; `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/TESTS.md:3-14`)

**v2.0 arm availability (GM66-F02).** The v1.9 B-15 rule stands. New B-17 adds one narrower reader-side
block: **R-8**, and therefore its F-6 sub-arm, cannot be performed from committed bytes because no
independent expected-coordinate operand is committed. F-13 remains a writer-side design target and is
not blocked by B-17; once B-15 closes, it can compare the live factory receipt against staged path
bytes before commit. (§3.4.3; §4.1.3; §5.4; §7 B-17)

| Arm | Input / modified copy | Required observation |
|---|---|---|
| F-1 baseline legacy | One completed unmigrated-path run containing one rejected and one non-rejected trial. | Both rows are under `lineage=SIGNAL_SCREEN_ONLY`, both row fields equal `SIGNAL_SCREEN_ONLY`, and `AcceptanceEvidenceReader` returns `REFUSED(reason=CANONICAL_RECEIPT_MISSING_OR_INVALID)` for both. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:509-510`)
| F-2 caller-label probe | Add `simulator_class=FULL_KERNEL_SIMULATION` to raw input for the closed `CompletedRunInput`. | The input boundary refuses the reserved field because `CompletedRunInput` has no such parameter; no `TrialRecord` construction and no file commit occur. This probe does not rely on `simulator_class` being unknown to `TrialRecord`. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:57`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/base.py:59-67`)
| F-3 legacy-classifier modified copy | Modify the legacy adapter to request the full sink while supplying no valid P0-20 receipt. | Writer refuses before commit; the probe is DETECTED. **PROVISIONAL-ON-P020** for receipt shape. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:499,509`)
| F-4 post-write token modified copy **[v1.7: UNBLOCKED — B-10/B-13 closed; specified, not executable while B-04/B-12 remain]** | Change a committed screening row’s `simulator_class` bytes to `FULL_KERNEL_SIMULATION` without rebuilding the receipt. | Commit validation returns `REFUSED(reason=COMMIT_HASH_MISMATCH)`. (`MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:617-687`)
| F-5 moved-file modified copy | Use reader fixture R-2: a commit-valid part whose row says `FULL_KERNEL_SIMULATION` is deliberately placed in the screening path while every other reader predicate, including the canonical receipt, is valid. | Reader returns `REFUSED(reason=PATH_ROW_LINEAGE_MISMATCH)`; no missing-receipt condition masks the lineage check. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_N70_P013_V11.md:7-12`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:509-510`)
| F-6 acceptance-reader modified copies | For each R-1..R-8 input below, delete exactly its named reader check and change nothing else. **[SUPERSEDED IN v1.7:]** the v1.6 text read "R-1..R-6" and added "The R-1 and R-3 sub-arms are blocked design targets while B-10/B-13 and B-11 respectively remain open." **v1.7:** R-1 and R-3 are unblocked by §4.1.3/§4.2.1, and R-7 and R-8 are added; no R sub-arm is blocker-gated on B-10/B-11/B-13, and all remain unexecutable while B-04/B-12 leave two row identities unemittable. **v1.8 (G102-F04):** R-8 is additionally a blocked design target under **B-15** — it takes an F-13 copy, which cannot be built — so this fixture covers R-1..R-7 until B-15 closes. **[SUPERSEDED IN v1.9 — W215-F02; retained v1.8 sentence:]** “this fixture covers R-1..R-7 until B-15 closes.” **v1.9:** it covers none of them until B-15 closes — every R arm starts from a committed package whose part paths carry the three Hive routing segments B-15 blocks (§5.4 v1.9 amendment). | Baseline reader returns its exact typed reason; the corresponding one-check-deleted reader returns `ACCEPTED`, making the regression RED. No multi-failure legacy input is used for this discriminating proof. (`MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/TESTS.md:7-14`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_N70_P013_V11.md:7-12`)
| F-7 canonical control | **PROVISIONAL-ON-P020:** one accepted migrated-path receipt, with every required identity, produces `FULL_KERNEL_SIMULATION` and is accepted. Remove or alter the receipt and re-run the same completed run. | Exact receipt accepted; removed/altered receipt returns `REFUSED(reason=CANONICAL_RECEIPT_MISSING_OR_INVALID)`. The control cannot be executed until P0-20 accepts. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:498-510`)
| F-8 preimage-class mismatch | An unmigrated run carries a receipt whose supplied `evaluation_run_hash` was formed with `simulator_class=FULL_KERNEL_SIMULATION`; keep all other inputs fixed. **PROVISIONAL-ON-P020** for the final receipt shape, not for the refuse-on-mismatch rule. | `LineageClassifier` locks `SIGNAL_SCREEN_ONLY`; writer recomputation differs from the supplied hash, so the run is refused before assembly/commit. A modified writer that rewrites only the row class is RED. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:76-95,132-135`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:416`)
| F-9 per-trial artifact address and flag | One completed run has two selected trials with the same `package_hash` and distinct `trial_id` values plus one unselected trial (`compute_package_hash` takes no trial sequence, `make_trial_id` does). Baseline commits both selected-artifact sets and no address for the unselected trial. Sub-arms, each changing only the stated operand: (a) commit one selected trial's payloads a second time to its own address; (b) swap the two selected trials' committed `manifest.json` bytes and directory addresses; (c) omit the committed `trial_id` from one selected manifest; (d) point both selected trials at a single `artifacts/<package_hash>/` address with no `trial_id` segment; (e) change only the unselected trial's emitted `has_full_artifacts=false` to `true`; (f) change only one selected, identity-matched trial's emitted `has_full_artifacts=true` to `false`. Not P0-20-gated; **B-09** gates the ratified manifest/path binding this fixture assumes. | Baseline: each selected trial commits under `artifacts/<package_hash>/<trial_id>/` and receives `true`; the unselected trial has no selected-artifact address and receives `false`. `ArtifactCommitVerifier` emits all three flags after matching each selected committed identity against the independent stage-3 row identity and checking absence for the unselected identity. Every sub-arm is `REFUSED` before assembly. A verifier modified to reuse the upstream `SelectedArtifactPayloadReceipt` as both operands accepts (b) and is RED; a verifier modified to omit the selection/flag comparison accepts (e) or (f) and is RED. The repository model's default `false` is never an input or fallback. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:19,23-24,67,77-88`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:54-73,132-135`; `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:617-687,933-967`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G42_P013_V13.md:93-133`)
| F-10 independent DuckDB schema fingerprint **[v1.7: UNBLOCKED — B-13 closed; both operands are now `SHA256(canonical_json(PublishedViewSchemaDocumentV1))` per §4.2.1, so the honest GREEN baseline is defined; specified, not executable while B-04/B-12 remain]** | Begin with valid committed parts and the exact production §4.2 SQL template; its candidate view projection matches the frozen §3.4.1 published-view contract. In the modified copy, change only the candidate-view SQL projection to add or drop exactly one projected column, leaving committed parts, receipt hashes, and every non-schema predicate valid, and keep the expected-fingerprint receipt independently produced from unchanged §3.4.1. | `CommittedDuckDBSchemaInspector` observes the changed query-visible view schema; `DuckDBSchemaFingerprintComparer` returns `REFUSED(reason=SCHEMA_FINGERPRINT_MISMATCH)`. A one-check-deleted comparer accepts the modified copy and is RED. A degenerate implementation that derives both fingerprints from the changed view also accepts and is RED, and the design itself refuses that producer-identity alias even on matching inputs. (`MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/TESTS.md:7-14`; `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:617-687`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G42_P013_V13.md:54-91`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G61_P013_V14.md:150-163`)
| F-11 independent trial conservation | One completed run whose terminal receipts are fixed. `CompletedRunTrialUniverseProjector` produces the expected ordered `trial_id` multiset from `CompletedRunInput` before any writer filtering. In the modified copy, change only the serialization stage so exactly one conserved `trial_id` is omitted from the staged Parquet parts; the expected receipt, the terminal receipts, and every other predicate are unchanged. Sub-arms, each changing only the stated operand: (a) omit one staged row; (b) emit one `trial_id` twice across parts; (c) overwrite one staged row with a second value for the same `trial_id`. Not P0-20-gated and not blocker-gated. | Baseline: the two receipts carry equal ordered multisets and `TrialConservationComparer` emits its typed success receipt, which alone permits commit. Each sub-arm: `CommittedTrialRowInventory` observes the changed multiset and the comparer refuses. A one-check-deleted comparer accepts the modified copy and is RED. A degenerate implementation in which one module produces both operands — including one that re-reads the staged parts to build the expected multiset — also accepts and is RED, and the design refuses that producer-identity alias even on matching inputs. (`MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:617-628,681-687,933-967`; `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/TESTS.md:7-14`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:144-171`)
| F-12 path/row `run_id` writer arm | Begin from a valid committed package. Change only the Hive `run_id=` path segment of one committed part to a second syntactically valid `run_id`, leave the Parquet row `run_id` and every other predicate unchanged, and rebuild the catalog receipt so the commit predicate stays valid. Sub-arms, each changing only the stated operand: (a) unequal path/row value; (b) missing `run_id=` segment; (c) a second separately surfaced `run_id` column in the candidate view; (d) mixed row `run_id` values inside one part. Not P0-20-gated and not blocker-gated. | `RunIdentityFactory` supplies the expected value and `CommittedPathRunIdInspector` the observed one; `PathRowRunIdComparer` refuses with `REFUSED(reason=PATH_ROW_RUN_ID_MISMATCH)` for each sub-arm, never with `PATH_ROW_LINEAGE_MISMATCH`. A one-check-deleted comparer accepts and is RED. A schema fingerprint that merely counts one `run_id` column, or a lineage comparison, accepts the modified copy and is therefore not a substitute check. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:138-141`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:17`; `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/TESTS.md:7-14`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:173-202`)
| F-13 path/receipt cell writer arm (v1.7) **[v1.8: BLOCKED DESIGN TARGET — B-15 opened; the fixed factory receipt this arm starts from cannot be produced]** | Begin from a valid committed package whose `RunCellDimensionsFactory` receipt is fixed. Change only one Hive routing segment of one committed part to a second syntactically valid value, leave the factory receipt and every other predicate unchanged, and rebuild the catalog receipt so the commit predicate stays valid. Sub-arms, each changing only the stated operand: (a) unequal `strategy=`; (b) unequal `symbol=`; (c) unequal `timeframe=`; (d) a missing routing segment; (e) differing values for one dimension across two parts of the same commit; (f) a `symbol` that disagrees with the run package's `InstrumentMetadata.symbol` while the path matches the factory receipt. Not P0-20-gated. | `RunCellDimensionsFactory` supplies the expected receipt and `CommittedPathCellInspector` the observed segments; `PathReceiptCellComparer` refuses with `REFUSED(reason=PATH_RECEIPT_CELL_MISMATCH)` for sub-arms (a)–(e), never with `PATH_ROW_LINEAGE_MISMATCH` or `PATH_ROW_RUN_ID_MISMATCH`; sub-arm (f) is refused by the factory before any path exists. A one-check-deleted comparer accepts and is RED. A comparer that re-reads the same path bytes to build both operands also accepts and is RED, and the design refuses that producer-identity alias even on matching inputs. Rebuilding the commit receipt does not mask the arm, because the three values enter the digest only through item 3's `path_slot` and the comparer's operand is the factory receipt, not the digest. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/package.py:18-24`; `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_08_WRITER_INVENTORY_2026-08-25/WRITER_INVENTORY.md:35,102`; `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:617-628,681-687`; `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/TESTS.md:7-14`)

### 5.4 Individually load-bearing acceptance-reader fixtures

Each R fixture begins from the accepted F-7 canonical control and changes only the stated operand. The fixture builder recomputes the catalog commit wherever necessary so the commit predicate remains valid unless R-1 is the target. **PROVISIONAL-ON-P020** applies to producing the accepted F-7 receipt; the isolation rule and typed outcomes are not provisional. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_N70_P013_V11.md:7-12`; `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/TESTS.md:7-14`)

**[SUPERSEDED IN v1.7 — B-10/B-11/B-13 closed; retained v1.6 text:]** **v1.6 note on the rebuild premise.** “Recomputes the catalog commit wherever necessary” presumes a computable `catalog_commit_hash`; that presumption is withdrawn while B-10 or B-13 is open, so R-1 cannot be constructed and the remaining R arms cannot claim a valid rebuilt commit predicate. R-3 additionally presumes stored receipt preimage inputs the design does not yet own a home for and is withdrawn while B-11 is open. R-2, R-4, R-5, and R-6 remain specified but are not closure evidence until the packages they start from can be built. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:52-120,204-233`)

**v1.7 note on the rebuild premise.** The rebuild premise is restored: `catalog_commit_hash` is computable from the closed §4.1.3 preimage, whose item 1 fingerprint is closed by §4.2.1, so every R arm can claim a valid rebuilt commit predicate. R-3's “keep the receipt preimage inputs at the accepted values” is re-pointed at the six committed run-envelope members in §4.1.3, which is where those bytes now live. R-7 and R-8 are added. None of R-1..R-8 is closure evidence, and none can be built while B-04 and B-12 leave `param_hash` and `preregistered_space_hash` unemittable and B-01 gates build. (§4.1.3; §4.2.1; `MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:24,28`)

**v1.8 amendment (G102-F04).** R-8 additionally cannot be constructed for a reason of its own: it takes
an F-13 modified copy as its input, and F-13 begins from a fixed `RunCellDimensionsFactory` receipt
that **B-15** makes unproducible. **[SUPERSEDED IN v1.9 — W215-F02; retained v1.8 sentence:]** “R-1..R-7
are unaffected by B-15.” (§7 B-15)

**v1.9 amendment (W215-F02).** R-1 through R-7 are **not** unaffected. Every R fixture begins from the
accepted F-7 canonical control — a committed full-lineage package — and §4.1's layout puts the three
Hive routing segments in every part path, which §4.1's v1.8 status says may not be derived while
**B-15** is open. R-3's and R-7's own cells make the dependency explicit by listing the **path/receipt
cell** check among the predicates that must remain valid, and that check is unavailable while the
comparer has one operand. So R-1..R-8 are all blocked design targets under B-15 as well as
unexecutable under B-04/B-12. The two reasons are independent and neither is a substitute for the
other: closing B-04 and B-12 would not make an R arm constructible while B-15 stands. No arm is
re-specified and no channel is named here to remove the block. (§4.1; §5.3; §7 B-15)

**v2.0 amendment (GM66-F02).** R-8 has a second, independent block under **B-17**. Closing B-15 would
make a factory receipt producible, but the committed package still contains no independent expected
coordinate operand for `AcceptanceEvidenceReader`; the only committed coordinates are in the path it
is inspecting. R-8 therefore cannot be performed from committed bytes until B-17 names a committed
home. R-1 through R-7 are unaffected by B-17. (§3.4.3; §4.1.3; §7 B-17)

| Reader fixture | Only deviant predicate; all others valid | Baseline observation | One-check-deleted modified reader |
|---|---|---|---|
| R-1 commit binding **[v1.7: UNBLOCKED — B-10/B-13 closed]** | Alter one valid Parquet metric byte without rebuilding the receipt. Companion sub-arms separately alter one preimage receipt field, one derived final-path mapping, and one selected-manifest membership entry. | `REFUSED(reason=COMMIT_HASH_MISMATCH)` for each sub-arm. | `ACCEPTED` for the matching sub-arm; the regression is RED. |
| R-2 path/row lineage | Build a commit-valid package with `lineage=SIGNAL_SCREEN_ONLY` in the path and `FULL_KERNEL_SIMULATION` in the row/evaluation preimage; keep evaluation hash, dependent `trial_id`, and canonical receipt valid. | `REFUSED(reason=PATH_ROW_LINEAGE_MISMATCH)`. | `ACCEPTED`; the regression is RED. |
| R-3 committed evaluation preimage **[v1.7: UNBLOCKED and re-pointed — B-11 closed]** | In a commit-valid full-lineage package, replace the stored row `evaluation_run_hash` with another valid SHA-256 and rebuild its dependent `trial_id`; keep the **six committed run-envelope members in the §4.1.3 receipt** — `package_hash`, `dataset_manifest_sha`, `cost_model_json`, `simulator_class`, `simulator_version`, `evaluation_config_json` — at the accepted values. **[SUPERSEDED IN v1.7:]** the v1.6 cell read "keep the receipt preimage inputs at the accepted values", which named no stored bytes. Commit, path/row, path/receipt cell, dependent-trial, and canonical-receipt checks remain valid. | `REFUSED(reason=EVALUATION_PREIMAGE_MISMATCH)`, produced by recomputing `compute_evaluation_run_hash` over the six committed members and comparing against the row value — from committed bytes alone, with no out-of-band write-time state. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:76-95`) | `ACCEPTED`; the regression is RED. |
| R-4 dependent `trial_id` | In a commit-valid full-lineage package, replace only `trial_id` with another syntactically valid value; keep the evaluation preimage/hash and every other operand valid. | `REFUSED(reason=TRIAL_ID_MISMATCH)`. | `ACCEPTED`; the regression is RED. |
| R-5 canonical receipt | Keep a commit-valid full-lineage package with matching path/row, evaluation hash, and `trial_id`, but remove or invalidate only the external P0-20 receipt. | `REFUSED(reason=CANONICAL_RECEIPT_MISSING_OR_INVALID)`. | `ACCEPTED`; the regression is RED. |
| R-6 path/row `run_id` | Take the F-12 modified copy as the reader input: only the Hive `run_id=` segment differs from the Parquet row `run_id`, the receipt was rebuilt so the commit predicate holds, and path lineage, the evaluation preimage, dependent `trial_id`, and the canonical receipt are all valid. | `REFUSED(reason=PATH_ROW_RUN_ID_MISMATCH)` — never `PATH_ROW_LINEAGE_MISMATCH`, and never masked by a missing-receipt or lineage condition. | `ACCEPTED`; the regression is RED. Deleting only the lineage check leaves R-6 refusing, and deleting only the `run_id` check leaves R-2 refusing, so the two checks are independently load-bearing. |
| R-7 commit-preimage member completeness (v1.7) | Build a commit-valid full-lineage package, then produce a modified copy in which exactly one **required** §4.1.3 run-envelope member is omitted from the stored receipt and the stored digest is recomputed over the shortened preimage, so every stored byte is internally self-consistent. Every other predicate — path/row lineage, path/row `run_id`, path/receipt cell, dependent `trial_id`, canonical receipt — is valid. Run the arm once per required member. | `REFUSED(reason=COMMIT_PREIMAGE_MEMBER_MISSING)`, emitted by the reader's typed parse of the stored receipt against the closed §4.1.3 model **before** any rehash — never `COMMIT_HASH_MISMATCH`, which cannot fire because the shortened bytes rehash correctly. | `ACCEPTED`; the regression is RED. A reader that only rehashes the stored receipt accepts every sub-arm and is RED, which is the exact defect B-10 named. Deleting only the member-completeness parse leaves R-1 refusing, and deleting only the rehash leaves R-7 refusing, so the two checks are independently load-bearing. |
| R-8 path/receipt cell (v1.7) **[v1.8: BLOCKED DESIGN TARGET — B-15; it takes an F-13 copy, which cannot be built]** | Take an F-13 modified copy as the reader input: only one Hive routing segment differs from the `RunCellDimensionsFactory` receipt, the receipt was rebuilt so the commit predicate holds, and path lineage, path/row `run_id`, the evaluation preimage, dependent `trial_id`, and the canonical receipt are all valid. | **v2.0 — GM66-F02; new blocker B-17 `CELL-COORDINATE-COMMITTED-OPERAND`.** The expected cell coordinates for this check exist only in the write-time `RunCellDimensionsFactory` receipt; they are absent by design from committed storage (§4.1.3 item 2, §3.4.3), so `AcceptanceEvidenceReader` — which may not consume write-time state (§5.2) — has no independent committed operand to give `PathReceiptCellComparer`. This check **cannot be performed from committed bytes**, and this document now says so rather than describing a verification it cannot run. **[SUPERSEDED IN v2.0 — GM66-F02; retained v1.9 cell:]** "`REFUSED(reason=PATH_RECEIPT_CELL_MISMATCH)` — never `PATH_ROW_LINEAGE_MISMATCH` and never `PATH_ROW_RUN_ID_MISMATCH`, and never masked by a missing-receipt condition." **v2.0:** B-17 asks: *where, in committed storage, do the expected strategy × symbol × timeframe cell coordinates live so a reader can independently recompute the receipt operand?* Until one is named, R-8 is a blocked design target under B-15 and, independently, under B-17; it cannot be verified from committed bytes. | **[BLOCKED IN v2.0 — GM66-F02; retained v1.9 cell:]** "`ACCEPTED`; the regression is RED. Deleting only the `run_id` check leaves R-8 refusing and deleting only the cell check leaves R-6 refusing, so the two path checks are independently load-bearing." **v2.0:** **NOT VERIFIABLE from committed bytes while B-17 is open**; the retained observation is a future build target only after an independent expected operand is committed. |

F-8 remains the separate **writer-boundary** fixture and never stands in for R-3: F-8 must refuse before a row exists, while R-3 is a committed package that reaches `AcceptanceEvidenceReader`. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_N70_P013_V11.md:7-12`)

## 6. Acceptance-gate mapping

Every falsifying probe below is a build requirement, not evidence produced in this design lane.

**[SUPERSEDED IN v1.7 — B-10/B-11/B-13/B-14 closed; retained v1.6 text:]** **v1.6 gate availability.** Three gate rows below name elements that v1.6 blocks. “A real run produces a queryable catalog” depends on the commit digest (B-10), both schema-fingerprint byte formulas and `view_publication_hash` (B-13), and the three Hive routing values (B-14); its F-10 sub-probe is a blocked design target and the whole row cannot be shown GREEN until those close, while its conservation sub-probe is now F-11 and is not blocker-gated. “Fixture shows an unmigrated row unable to pass as acceptance evidence” now runs R-1..R-6, of which R-1 (B-10/B-13) and R-3 (B-11) are blocked design targets; F-1, R-2, R-4, R-5, and R-6 are not. “Every row carries a `deployment_identity_hash`” keeps its existing B-08 gate. Naming a probe here is not a claim that it can be constructed today. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:52-233,268-291`; `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/TESTS.md:3-14`)

**[SUPERSEDED IN v1.8 — G102-F04; retained v1.7 text:]** **v1.7 gate availability.** No gate row is blocked on B-10, B-11, B-13, or B-14 any more. “A real run
produces a queryable catalog” has its commit digest (§4.1.3), both schema-fingerprint byte formulas and
`view_publication_hash` (§4.2.1), and the three Hive routing values (§3.4.3); F-10 is a specified
sub-probe. “Fixture shows an unmigrated row unable to pass as acceptance evidence” now runs R-1..R-8,
none of them blocked on those four. “Every row carries a `deployment_identity_hash`” keeps its existing
**B-08** gate, unchanged. **No gate row is closable today**, for a different and still-open reason:
`TrialRecordAssembler` cannot construct a row while **B-04** and **B-12** leave `param_hash` and
`preregistered_space_hash` unemittable, and **B-01** gates build on WP-P0-20 acceptance. Naming a probe
here remains a build requirement, not a claim that it can be constructed today.
(`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:24,28`;
`MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/TESTS.md:3-14`; §3.4.3; §4.1.3; §4.2.1)

**v1.8 gate availability.** No gate row is blocked on B-10, B-11, or B-13. **One gate element is
blocked again on the new B-15:** “A real run produces a queryable catalog” needs the three Hive routing
values, and their declared channel is open, so that row's Hive-partition element and the whole
“Hive routing dimensions equal the run's cell coordinates” row below are blocked design targets whose
probes F-13/R-8 cannot be constructed. “Fixture shows an unmigrated row unable to pass as acceptance
evidence” runs R-1..R-7 today and R-8 only after B-15. B-14's own question — who produces the values —
stays answered; B-15 asks the narrower question of which declared member carries them. **No gate row
is closable today** for the standing reason as well: `TrialRecordAssembler` cannot construct a row
while **B-04** and **B-12** leave `param_hash` and `preregistered_space_hash` unemittable, and **B-01**
gates build on WP-P0-20 acceptance. (§7 B-15; §3.4.3; `MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:24,28`)

**v1.9 gate availability (W215-F02).** Two clauses of the paragraph above are widened; the rest stands.
**[SUPERSEDED IN v1.9 — W215-F02; retained v1.8 clauses:]** “that row's Hive-partition element … are
blocked design targets whose probes F-13/R-8 cannot be constructed” and “‘Fixture shows an unmigrated
row unable to pass as acceptance evidence’ runs R-1..R-7 today and R-8 only after B-15.” **v1.9:**
because every part path in §4.1's layout carries the three Hive routing segments, **B-15 blocks the
whole of the “A real run produces a queryable catalog” row**, not one element of it — no part may be
written, so no view may be published and no query may run — and the acceptance-evidence row runs **no**
R arm until B-15 closes, not R-1..R-7. The same rule §5.3 states applies to the rest of the table:
a gate row is blocked by B-15 wherever its probe reads a staged or committed part, a commit receipt,
or the published view. That reaches “A real run produces a queryable catalog” (F-10, F-11), “A rejected
trial can be found by its rejection reason” (the `list_contains` query over the published view), “One
row per trial” (F-11 over staged parts), “Path `run_id` equals row `run_id`” (F-12/R-6), and the
“Hive routing dimensions” row (F-13/R-8). It does **not** reach the probes that refuse before any part
exists: “Every row carries a `simulator_class`” keeps its F-8 arm, “An unmigrated-path row is stamped
`SIGNAL_SCREEN_ONLY`” keeps F-2/F-3/F-8, and “No row emitted without a lineage class” keeps its
refuse-before-assembly probe. “Full artifacts for selected trials” turns on the undecided F-9 question
recorded in §5.3, and “Every row carries a `deployment_identity_hash`” keeps its existing **B-08**
gate. **No gate row is closable today** for the standing B-04/B-12/B-01 reason as well, which is
unchanged and independent. Naming a probe here remains a build requirement, never closure evidence.
(§4.1; §5.3; §5.4; §7 B-08; §7 B-15)

**v2.0 gate availability (GM66-F02/F03/F04).** The v1.9 B-15 rule remains controlling. B-17 adds a
separate reader-side block: the acceptance-evidence row cannot run R-8 from committed bytes, and the
Hive-routing row's R-8 half is likewise unavailable, even after B-15 closes, until an independent
expected-coordinate operand is committed. F-13 remains the writer-side falsifying probe after B-15
closes. The stale v1.8 gate cell is superseded below, and the Hive-routing gate now appears in the
table rather than prose alone. (§3.4.3; §5.4; §7 B-15; §7 B-17)

**v1.7 gate row added — “Hive routing dimensions equal the run's cell coordinates.” [v1.8: BLOCKED DESIGN TARGET — B-15]** Design element:
`RunCellDimensionsFactory` (expected), `CommittedPathCellInspector` (observed), and
`PathReceiptCellComparer`, which produces neither operand. Falsifying probe: F-13/R-8 change exactly one
Hive routing segment and the comparer returns `REFUSED(reason=PATH_RECEIPT_CELL_MISMATCH)`; a
one-check-deleted comparer accepts and is RED, and neither the lineage comparison nor the path/row
`run_id` comparison is a substitute because both accept the modified copy. (§3.4.3;
`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2052-2056`;
`MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_08_WRITER_INVENTORY_2026-08-25/WRITER_INVENTORY.md:35,102`)

**[RETAINED IN v2.0 — GM66-F04: the v1.7/v1.8 prose gate definition above remains character-for-character; the table row below makes the gate visible to a table-only reader.]**

| Plan gate clause | Design element | Falsifying probe that must show RED on a modified copy |
|---|---|---|
| “A real run produces a queryable catalog.” | `MigratedCanonicalRunAdapter`, `TrialCatalogWriter`, committed Parquet parts, sole expected producer `TrialCatalogViewSchemaProjector` over §3.4.1, sole observed producer `CommittedDuckDBSchemaInspector` over the query-visible candidate view, separate `DuckDBSchemaFingerprintComparer`, and sole `DuckDBViewPublisher`. **PROVISIONAL-ON-P020** for the real canonical adapter. | Complete a bounded real run and query it through the published view. **[SUPERSEDED IN v1.6 — G93-F04:]** “A modified writer that skips one terminal receipt fails conservation/count” — a writer mutant alone does not falsify a conserver that declares its own universe; the v1.6 conservation sub-probe is F-11, in which the expected receipt from `CompletedRunTrialUniverseProjector` is held fixed while one staged row is omitted and `TrialConservationComparer` refuses. Separately, missing view publication, a wrong glob, F-10's independently observed schema mismatch, a same-producer-degenerate fingerprint implementation, or a wrong filename-hash projection refuses publication or omits the known commit and makes the query RED. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:412,416`; `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:617-687,957-967`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G42_P013_V13.md:54-91`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G61_P013_V14.md:150-163`)
| “A rejected trial can be found by its rejection reason.” | Non-null `rejection_reasons`, sole `TrialGateAggregator`, native Parquet list, `list_contains` query. **PROVISIONAL-ON-P020** for taxonomy. | Modified aggregator deletes or renames the fixture reason: the exact query returns zero rows and the test is RED. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:416`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:59-60`)
| “Every row carries a `simulator_class`.” | Required model field, private lineage capability, class lock before evaluation identity, and path/row/preimage agreement. | Remove/empty the field, move a screening part to the full root, or run F-8: construction, identity validation, or query acceptance refuses. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:57`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/base.py:15-16`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:76-95`)
| “Every row carries a `deployment_identity_hash`.” | Required SHA-256 field, `DeploymentIdentityFactory`, assembler identity validation. **PROVISIONAL-ON-P020** for accepted preimage inputs. | Missing, malformed, or recomputed-with-different-cost-lineage hash refuses construction/commit. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:20`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:98-129`)
| “An unmigrated-path row is stamped `SIGNAL_SCREEN_ONLY`.” | `LegacySignalScreenRunAdapter`, `ScreenSinkCapability`, `LineageClassifier`, screening physical root, and the evaluation-hash preimage. | F-2/F-3/F-5/F-8: caller label, legacy-adapter full request, moved file, and pre-bound full-class hash are each refused. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:416,499,509-510`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:76-95`)
| “Fixture shows an unmigrated row unable to pass as acceptance evidence.” | Independent `AcceptanceEvidenceReader`, closed refusal taxonomy, and canonical receipt verification; two proof producers named in §5.2. **PROVISIONAL-ON-P020** for receipt verification. | F-1 returns the typed canonical-receipt refusal. F-6 then runs R-1..R-6: deleting each single reader check changes only its isolated typed refusal to `ACCEPTED`, so every modified reader is RED. **[SUPERSEDED IN v1.7:]** “R-1 and R-3 are blocked design targets while B-10/B-13 and B-11 respectively remain open, so this gate is not closable today.” **v1.7:** R-1 and R-3 are unblocked and R-7 and R-8 are added, so F-6 runs R-1..R-8; the gate is still not closable today, because no row can be assembled while B-04 and B-12 remain. **[SUPERSEDED IN v2.0 — GM66-F03; retained v1.8 sentence:]** "**v1.8 (G102-F04):** F-6 runs R-1..R-7 today and R-8 only after **B-15**, whose open channel makes the F-13 copy R-8 starts from unbuildable." **v2.0:** F-6 runs **no** R arm until B-15 closes — every R fixture begins from a committed full-lineage package whose part paths carry the three Hive routing segments B-15 blocks (§5.3, §5.4), so this gate is not closable today. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:416`; `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/TESTS.md:7-14`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_N70_P013_V11.md:7-12`)
| **[SUPERSEDED IN v1.6 — G93-F04; retained v1.5 row:]** “One row per trial.” | `TerminalTrialConserver`, unique `trial_id`, idempotent commit. | Drop, duplicate, or overwrite one terminal receipt; conservation or uniqueness refuses the commit. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:412`; `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:957-967`)
| **v1.6 controlling row:** “One row per trial.” | Sole expected-universe producer `CompletedRunTrialUniverseProjector` over `CompletedRunInput`; sole observed-universe producer `CommittedTrialRowInventory` over the staged parts; `TrialConservationComparer`, which belongs to neither and emits neither operand; unique `trial_id`; idempotent commit. `TerminalTrialConserver` no longer exists as a single declarer-and-prover. | F-11: drop, duplicate, or overwrite one staged row while the expected receipt is unchanged — the comparer refuses the commit. A one-check-deleted comparer accepts and is RED, and a same-module implementation that derives both multisets from the staged parts also accepts and is RED. A mutated writer alone is not sufficient falsification, because the declarer would shrink with it. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:412`; `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:617-628,681-687,933-967`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:144-171`)
| “Path `run_id` equals row `run_id` for every part.” (v1.6, from the §3.4.1 routing guarantee) | `RunIdentityFactory` (expected), `CommittedPathRunIdInspector` (observed), and `PathRowRunIdComparer`, which produces neither operand. | F-12/R-6: change only the Hive `run_id=` segment and rebuild the receipt — the comparer returns `REFUSED(reason=PATH_ROW_RUN_ID_MISMATCH)` and a one-check-deleted comparer accepts and is RED. The schema fingerprint's one-`run_id`-column rule and `PATH_ROW_LINEAGE_MISMATCH` both accept this modified copy and are not substitutes. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:138-141`; `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:617-628,681-687`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:173-202`)
| “Full artifacts for selected trials per the selection rule.” | `ArtifactSelector`; four typed payload producers; `SelectedArtifactManifestBuilder`; byte-only `SelectedArtifactCommitter`; separate `ArtifactCommitVerifier` as sole producer of both `has_full_artifacts=true` and `has_full_artifacts=false` for every conserved trial; per-trial address `artifacts/<package_hash>/<trial_id>/` and per-trial manifest identity gated on **B-09**. | For each artifact kind, omit, duplicate, swap producer, change bytes, or drift `trial_id`; the committer/verifier refuses. A verifier modified to synthesize a missing member or trust the committer is RED against the same selected trial. F-9 covers two selected trials sharing a `package_hash` plus one unselected trial: distinct selected addresses and exact `true,true,false` flags are the baseline; overwrite, address/manifest swap, missing committed identity, a shared address, unselected/`true`, and selected/`false` are each refused before assembly. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:412`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2075-2087`; `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:617-687,933-967`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G42_P013_V13.md:93-133`)
| “Hive routing dimensions equal the run's cell coordinates.” **(v1.7 gate row, added to the table in v2.0 — GM66-F04) [v1.8: BLOCKED DESIGN TARGET — B-15] [v2.0: R-8 BLOCKED DESIGN TARGET — B-17]** | `RunCellDimensionsFactory` (expected), `CommittedPathCellInspector` (observed), `PathReceiptCellComparer` (produces neither operand). | F-13 changes exactly one staged Hive routing segment and, after B-15 closes, the writer-side comparer returns `REFUSED(reason=PATH_RECEIPT_CELL_MISMATCH)`; a one-check-deleted comparer accepts and is RED, and neither the lineage comparison nor the path/row `run_id` comparison is a substitute because both accept the modified copy. R-8 is the intended reader-side analogue, but it cannot be performed from committed bytes while **B-17** is open because no independent expected-coordinate operand is committed. F-13 and R-8 cannot be constructed while **B-15** is open; R-8 remains blocked after B-15 until B-17 closes. (§3.4.3; §5.4; §7 B-15; §7 B-17; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2052-2056`; `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_08_WRITER_INVENTORY_2026-08-25/WRITER_INVENTORY.md:35,102`) |
| “No row emitted without a lineage class.” | Required non-empty field plus no lineage argument at the caller seam. | Build a terminal receipt with no origin capability: writer refuses before row assembly. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:417`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:57`)

**v2.1 selection-gate cascade — decision 87.** The “Full artifacts for selected trials” row now reads
“selected” as the union named in the v2.1 `ArtifactSelector` cascade: top 20 per
strategy/market/timeframe, the best risk-versus-return group, promoted items, robust items, and pinned
items. Its B-09 manifest/path gate and the undecided B-15 reach over F-9 are unchanged. The gate still
cannot execute while B-07's versioned policy encoding and authoritative record bindings are missing.
(§2.1 stage 4; §5.3 F-9; §7 B-07; §7 B-09; §7 B-15)

**v2.2 selection-gate cascade — decision 128 supersedes decision 87.** The retained gate-table row now
reads “selected” as: passed all safety and quality checks, then ranked by overall robustness, then in
the best 20 for strategy TYPE `day`, `swing`, or `position`, including every cut-off tie. Market and
timeframe do not partition that current owner-decided group, and the Pareto, robust, promoted, and
pinned row facts do not independently enter it. The B-09 manifest/path gate and the undecided B-15
reach over F-9 remain unchanged. The gate still cannot execute while B-07's engineering policy/type/
evidence bindings are missing. (`C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:870-876,900-912`; §2.1 stage 4; §5.3 F-9; §7 B-07; §7 B-09; §7 B-15)

**v2.0 gate-table count.** The table above has **12 data rows**: 11 retained from the supplied snapshot
plus the GM66-F04 Hive-routing row. The patch's residual note says “11 rows (10 prior + 1)”, but the
snapshot's table contains 11 prior rows, including both the retained superseded conservation row and
its controlling replacement. The measured draft/snapshot count controls.
(`C:\tmp\LANE_PROMPTS_20260828\DS79_P013_PATCH.md:117-122`)

## 7. Named blockers — no defaults

### B-01 — `P020-ACCEPTANCE-AND-CANONICAL-RECEIPT`

**[SUPERSEDED IN v1.6 — G93-F07; retained v1.5 status wording:]** “its supplied checklist and battery papers are presently BLOCK”.

WP-P0-13 build cannot begin until WP-P0-20 accepts, and the canonical receipt issuer/shape is not settled. **Current status, re-read this session:** P19 recorded a 2026-08-29 flagship BLOCK of the **v1** P0-20 papers — `P020_CONTROL_PARITY_CHECKLIST_V1.md` and `P020_STATISTICAL_BATTERY_DEFINITION_V1.md` — at HEAD `d5be879e`. Those papers have since moved: the battery definition is now **v1.5**, an owner-gated versioned definition, and the P0-20 build-input design is **v1.5** and explicitly **DESIGN ONLY**. Neither current version is cited here as accepted, and no WP-P0-20 package acceptance is claimed; B-01 remains open on package acceptance itself, not on the historical paper verdicts. **PROVISIONAL-ON-P020** covers every full-kernel choice in this draft. Required resolution: accepted P0-20 artifacts plus a re-audit of this draft before build. (`C:\tmp\LANE_PROMPTS_20260828\LANE_W51_P013_DESIGN.md:8-12,21-23`; `C:\tmp\LANE_PROMPTS_20260828\AUDIT_P19_P020_PAPERS.md:1-16`; `C:\tmp\LANE_PROMPTS_20260828\P020_STATISTICAL_BATTERY_DEFINITION_V1.md:1-4`; `C:\tmp\LANE_PROMPTS_20260828\P020_BUILD_DESIGN_V1.md:1-10`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:483-510`)

### B-03 — `QUERY-DIMENSIONS-AND-PARAMETER-SHAPE`

The brief wants `strategy/symbol/timeframe` partitions and one typed nullable column per parameter, but the present `TrialRecord` has none of those dimensions and has one required `parameters: dict[str, Any]`. Required resolution: WP-P0-04 schema owner either ratifies the envelope/canonical-JSON lowering in §§3.4/4 or amends the contract; WP-P0-13 may not silently add model fields. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2052-2071`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:14-68`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:255`)

### B-04 — `PARAM-HASH-PREIMAGE`

`TrialRecord` requires `param_hash`, but the accepted identity module exposes no `compute_param_hash` formula. Required resolution: WP-P0-04 owner ratifies the exact canonical preimage and adds/identifies its sole identity function before build; P0-13 must not invent an identity formula. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:24`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:43-154`)

### B-05 — `LINEAGE-VOCABULARY-AND-SEAL`

The present schema accepts any non-empty `simulator_class` string, while the plan gives `SIGNAL_SCREEN_ONLY` special evidence semantics. Required resolution: WP-P0-04/P0-20 jointly ratify the finite vocabulary and whether it becomes a schema enum; regardless, the sealed adapter/sink design remains mandatory. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:57`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/base.py:15-16`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:499,509-510`)

### B-06 — `REJECTION-TAXONOMY-AND-STOP-MAPPING`

`rejection_reasons` is presently only a tuple of non-empty strings. The P0-20 battery paper is under repair for wrong producer/verdict details and STOP/FAIL conflation. Required resolution: accepted finite reason taxonomy, exact producer per reason, and explicit PASS/FAIL/BLOCKED mapping before the writer can guarantee reason queries are stable. **PROVISIONAL-ON-P020.** (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:59-60`; `C:\tmp\LANE_PROMPTS_20260828\AUDIT_P19_P020_PAPERS.md:53-83,170-233`)

### B-07 — `SELECTION-AND-FLAG-AUTHORITIES`

**[PARTIALLY SUPERSEDED IN v2.1 — W287; retained v2.0 blocker text follows. The owner half is decided;
the engineering half remains open.]**

The brief states `K ≈ 20` and “top-K by objective” without fixing the objective or exact K here; authoritative producers for promoted and pinned flags are also not delivered in this package. Required resolution: a versioned selection policy and named authoritative lifecycle/pin records. No approximate K becomes a default. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2075-2095`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:62-67`)

**v2.1 controlling disposition — OWNER HALF CLOSED; ENGINEERING HALF OPEN.** **DECIDED - owner
addendum 31 decision 87 (2026-09-02):** "Use a combined quality rule, not one score. Keep the top 20
per strategy, market, and timeframe; also keep the best risk-versus-return group, promoted items,
robust items, and anything I pin." The approximate K is replaced by the exact owner value **20**, and
the selected universe is the union of those keep groups rather than the output of one scalar score.
No scalar objective, ranking formula, tie rule, policy version, or new market identity is supplied by
the answer, so none is minted here. **B-07 remains OPEN only on its engineering half:** the P0-13 build
owner must encode the combined rule as a versioned selection policy and bind “market” to an existing
owned market dimension; the lifecycle/pin contract owners must deliver the authoritative records
consumed by `LifecycleDecisionProjector` and `UserPinProjector`. Those are engineering deliverables,
not owner re-asks. (`C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:744`;
`C:\tmp\LANE_PROMPTS_20260828\OWNER_PHASE0_DECISIONS_V1.md:33`;
`C:\tmp\LANE_PROMPTS_20260828\W269_PHASE0_OWNER_QUESTIONS.md:89-98,834`; §2.1 stage 4; §3.2)

**v2.2 controlling disposition — OWNER HALF CLOSED UNDER CURRENT AUTHORITY; ENGINEERING HALF OPEN.**
**SUPERSEDED - owner addendum 32 decision 128 (supersedes 87) (2026-09-02):** "Do not choose winners
using one score alone. Require all safety and quality checks first, then rank by overall robustness.

Keep the best 20 candidates separately for each strategy type—for example, day trading, swing trading,
and position trading—so one type does not crowd out another.

Keep any tied candidates at the cut-off as well." The exact owner count remains **20**, now applied
separately to strategy TYPE `day`, `swing`, and `position`, and every cut-off tie is also selected. The
market/timeframe partition and the old automatic keep union of risk-versus-return, promoted, robust,
and pinned groups are superseded, not carried forward as current selection authority. Their row flags
remain required independent facts under §3.2.

Decision 128 closes only the owner rule. **B-07 remains OPEN only on its engineering half:** the P0-13
build owner must bind the owned strategy TYPE, define the executable safety/quality gate inputs and
overall-robustness comparison, encode the best-20-plus-ties rule as a versioned selection policy, and
bind that policy version to relevant evidence under the `NEW-BY-ADDENDUM-32` item. The lifecycle/pin
contract owners still owe the authoritative records consumed by `LifecycleDecisionProjector` and
`UserPinProjector` so the independent fields can be emitted; those records no longer select a trial by
themselves. No scalar score, identity, new field, or still-pending cross-draft value is minted here.
(`C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:837-876,900-912`;
`C:\tmp\LANE_PROMPTS_20260828\OWNER_PHASE0_DECISIONS_V1.md:33`;
`C:\tmp\LANE_PROMPTS_20260828\W269_PHASE0_OWNER_QUESTIONS.md:89-98,834`; §2.1 stage 4; §3.2)

### B-08 — `LEGACY-DEPLOYMENT-IDENTITY-PREIMAGE`

Every row must carry `deployment_identity_hash`, but an unmigrated/stand-in path does not have the accepted shared allocator that the current deployment formula expects. Required resolution: WP-P0-04/P0-20 specify an honest non-accepting preimage for legacy screening rows; no sentinel may pretend the shared allocator exists. **PROVISIONAL-ON-P020.** (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:20`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:98-129`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:497-509`)

### B-09 — `SELECTED-ARTIFACT-PER-TRIAL-MANIFEST-AND-ADDRESS`

The v1.5 design retains the v1.3 per-trial binding: every selected trial has one collision-free committed address `artifacts/<package_hash>/<trial_id>/`, and its `manifest.json` carries `trial_id` plus the dependent identities (`package_hash`, `evaluation_run_hash`, `param_hash`) so `ArtifactCommitVerifier` compares committed bytes against the independent row identity rather than reusing the upstream `SelectedArtifactPayloadReceipt` as both operands. The repository does not yet support this: the current `ArtifactManifest` fields are `package_hash`, `deployment_identity_hash`, `evaluation_run_hash`, `dataset_hash`, `kernel_version`, `simulator_class`, `simulator_version`, `unsimulated_controls_hash`, `allocation_policy_version`, `environment_lineage` — no `trial_id`, no `param_hash` — and the brief's Tier-2 layout is the package-only `artifacts/<package_hash>/`. Required resolution: the WP-P0-04 schema owner ratifies the per-trial manifest/path binding — adds `trial_id` and the dependent identity fields to `ArtifactManifest` (or an owned sibling contract) and ratifies the `artifacts/<package_hash>/<trial_id>/` address — before build. WP-P0-13 may not add manifest fields or an address scheme on its own authority. This blocker is not itself P0-20-gated. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:19,23-24,77-88`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:54-73,132-135`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2075-2087`; `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:933-943,957-967`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_N81_P013_V12.md:7-12`)

### B-10 — `CATALOG-COMMIT-PREIMAGE-MEMBERSHIP` — **CLOSED IN v1.7; CLOSURE CORRECTED IN v1.8**

**v1.8 correction to the closure (G102-F03).** The closure stands, but its member contract and its cite
were both wrong and are repaired in §4.1.3 item 2. Read this session: `base.py:59-67` is the
`ContractModel` class statement and its `ConfigDict` — `extra="forbid"` and `frozen=True` live there,
required-member absence-refusal does not. `base.py:69` declares `contract_version: str =
Field(default=CONTRACT_VERSION, pattern=r"^0\.1\.0$")`, with the constant at `base.py:12` and a
validator at `base.py:71-78`, and `canonical_json` serializes a model through
`model_dump(mode="python")` (`identity.py:16-17`). A `ContractModel` subclass therefore carries a
**seventh** serialized member. The corrected contract is *six P0-13-declared members plus the inherited
`contract_version`, and no others*; the inherited member is already-written repository state, not a
v1.8 addition, and its omission from a stored receipt is **filled, not refused**, which §4.1.3 now
states as an ACCEPTED-not-DETECTED limit rather than leaving R-7's arm to imply otherwise. Everything
else in the closure below is unchanged.
(`MTC_COMMAND_CENTER/contracts/mtc_contracts/base.py:12,62-67,69,71-78`;
`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:16-17`; §4.1.3)

**v1.7 closure.** Closed by §4.1.3, which gives item 2 a typed closed run-envelope field list: six
required members — the six arguments of the shipped `compute_evaluation_run_hash` — and seven
candidates marked absent by design with the reason for each. Sole envelope producer:
`EvaluationIdentityFactory`, receiving `simulator_class` already locked by `LineageClassifier`. Sole
digest producer: `CatalogCommitIdentity`, over the shipped `canonical_json`. The "may bind" permission
is replaced by a member contract, so two honest implementations can no longer hash different
envelopes. Omission is DETECTED by a typed parse before any rehash, with
`COMMIT_PREIMAGE_MEMBER_MISSING` and fixture R-7; a reader that only rehashes the stored receipt is
RED, which is what the blocker demanded. B-13's parallel-close condition is satisfied: §4.2.1 closes
the expected fingerprint that item 1 embeds. Nominating "the WP-P0-04 schema owner" is withdrawn as
unsupported — WP-P0-04's output list contains no catalog-commit envelope, and this is a P0-13-owned
type. No `TrialRecord` column, `ArtifactManifest` field, identity function, or type dialect was added.
(`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:31-44,76-95`;
`MTC_COMMAND_CENTER/contracts/mtc_contracts/base.py:59-67`;
`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:320`;
`C:\tmp\LANE_PROMPTS_20260828\DETECT_G99_BLOCKERS.md:31-33`; §4.1.3; §4.2.1)

**[RETAINED — the v1.6 blocker text as opened, superseded by the closure above:]**

**Blocking question:** Which fields are required members of the run envelope inside `CatalogCommitPreimageV1`, and which are absent by design?

The v1.5 formula in §4.1.1 called the preimage closed while its only envelope field list said the envelope “**may bind**” five values and separately said `strategy`, `symbol`, and `timeframe` “remain in that commit envelope as well”. “May bind” is a permission, not a member contract: two honest implementations can hash different envelopes and both satisfy the sentence, and a reader that rehashes the stored receipt cannot detect an omitted required member because the omitted member is absent from the bytes it rehashes. Refusing unknown receipt fields bounds extras, not omissions. Required resolution: the WP-P0-04 schema owner, jointly with the P0-13 build owner, ratifies a typed closed field list for `CatalogCommitPreimageV1` — every member marked required or absent-by-design, including whether `strategy`, `symbol`, and `timeframe` are required — before `CatalogCommitIdentity`, `catalog_commit_hash`, the hash-bearing final-path derivation, F-4, or R-1 may be built. P0-13 may not close the set by hashing whatever the envelope happens to carry. This blocker also requires that the ratified receipt reject a missing member, proven by a modified copy that omits exactly one required member while every stored byte is internally self-consistent; acceptance by a reader that only rehashes the stored receipt is RED. B-13 must close in parallel because item 1 of the preimage embeds the still-unspecified expected schema fingerprint. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:15-44,76-95`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:255,267`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_N70_P013_V11.md:14-19`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:52-86`)

### B-11 — `EVALUATION-PREIMAGE-COMMITTED-STORAGE` — **CLOSED IN v1.7**

**v1.7 closure.** Closed by the same §4.1.3 table: all six `compute_evaluation_run_hash` members are
required members of the run envelope, and the run-level receipt already committed at
`commits/<catalog_commit_hash>.json` already stores the exact typed preimage, so `cost_model_json` and
`evaluation_config_json` — the two members v1.6 correctly said had no committed home anywhere — now
have one. Because the receipt is run-level and stage 3 recomputes one `evaluation_run_hash` per
completed run before every dependent `trial_id`, the stored bytes cover every conserved trial in that
run, selected and unselected alike. Sole producer of those members: `EvaluationIdentityFactory`. The
three prohibitions the blocker attached are all honoured: no `TrialRecord` column was added, so this is
not a WP-P0-04 schema act; `ArtifactManifest` is not the home, because unselected trials have none and
its `dataset_hash` is not `dataset_manifest_sha`; and no third JSON was invented for `cost_model_json`,
which is stored as the named function argument it already is. R-3 is re-pointed at the stored members
and `EVALUATION_PREIMAGE_MISMATCH` is available as a specified arm. WP-P0-20 freezing accepted
evaluation contents under B-01 remains a separate later question and is not a substitute for naming
where the bytes live. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:76-95,132-135`;
`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:19,21,57,77-87`;
`C:\tmp\LANE_PROMPTS_20260828\DETECT_G99_BLOCKERS.md:41-43`; §4.1.3)

**[RETAINED — the v1.6 blocker text as opened, superseded by the closure above:]**

**Blocking question:** Where is every member of the `evaluation_run_hash` preimage committed, for every conserved trial including unselected ones, so an acceptance reader can recompute the digest from committed bytes alone?

The write-time formula is settled in the repository: `compute_evaluation_run_hash` hashes `package_hash`, `dataset_manifest_sha`, `cost_model_json`, `simulator_class`, `simulator_version`, and `evaluation_config_json`. The read side is not. Parquet rows carry the hash, `package_hash`, and `simulator_class`; the commit envelope's own membership is open under B-10 and in v1.5 named at most `dataset_manifest_sha` and `simulator_version`; unselected trials have no artifact manifest at all. `cost_model_json` and `evaluation_config_json` therefore have no named committed home anywhere in this design, so §4.2's “independently recomputes … from committed preimage inputs” and R-3's “keep the receipt preimage inputs at the accepted values” are both unexecutable as written, and a builder who supplies them out of band from write-time state is not reading committed evidence. Required resolution: the WP-P0-04 schema owner names an owned committed location — a closed receipt field set, an owned extra column, or a per-trial metadata record — for all six members for every conserved trial, and R-3 is re-pointed at those stored members. P0-13 may not invent the storage location, and WP-P0-20's later formula is not a substitute for P0-13 naming where the bytes live. Until this closes, `EVALUATION_PREIMAGE_MISMATCH` is unavailable and R-3 is a blocked design target. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:76-95`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:19,21,57`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:255`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:88-120`)

### B-12 — `PREREGISTERED-SPACE-HASH-PREIMAGE` — **OPEN; UNTOUCHED IN v1.7**

**[PARTIALLY SUPERSEDED IN v2.1 — W287; retained v1.7/v2.0 blocker text follows. The split-out owner
half is decided; the engineering preimage half remains open.]**

**v1.7 status.** Not closed, not narrowed, not weakened, and no candidate recipe is proposed here. The
unfenced G99 audit read the contracts package, the canonical plan, the architecture brief, the writer
inventory, and `P012_FRESH_DESIGN_V1.md` v1.9 and reached the same verdict as the fenced fold: nothing
outside the fence supplies a closed field set or a sole identity function. Hashing
`evaluation_config_json` would collide with `evaluation_run_hash` rather than define this separate
required column; hashing “the grid JSON” would be a manufactured preimage, because module
combinations, adaptive-trial budget, and repeated-iteration membership are not a closed schema. A lane
that minted `SHA256(canonical_json(space))` would commit the exact defect B-04 exists to prevent. This
blocker belongs to WP-P0-04 or a named search-family owner. The owner question is: *what exact list of
things should count as the search space that was registered before a run, so two runs can prove they
searched the same space?* Until it is ratified, no producer may emit the field, and
`TrialRecordAssembler` cannot construct a row. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:28`;
`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:1-154`;
`MTC_COMMAND_CENTER/contracts/mtc_contracts/__init__.py:28-37`;
`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:320`;
`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:1830-1832,2061`;
`C:\tmp\LANE_PROMPTS_20260828\DETECT_G99_BLOCKERS.md:51-55,81`)

**Blocking question:** What exact canonical bytes does `preregistered_space_hash` cover, and which sole identity function produces it?

`TrialRecord` requires the field as a 64-hex SHA-256, but the accepted identity module exposes `canonical_json`, `make_candidate_id`, `compute_package_hash`, `compute_evaluation_run_hash`, `compute_deployment_identity_hash`, `make_trial_id`, `make_run_id`, and `compute_family_id` — there is no `compute_preregistered_space_hash`. The v1.5 note “One registered family space.” names a domain entity, not a byte tuple, and `SearchFamilyRegistry` was both the sole producer and the only place a check could live, so nothing named would fail if the digest covered a different space or only the space name. This is the same shape as B-04 for `param_hash`, which the draft already refuses to invent. Required resolution: WP-P0-04 or the search-family owner ratifies the exact canonical preimage and adds or identifies its sole identity function before build. Until then no producer may emit the field, and P0-13 must not invent a formula. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:28`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:1-154`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:122-142`)

**v2.1 controlling disposition — OWNER HALF CLOSED; ENGINEERING HALF OPEN.** **DECIDED - owner
addendum 31 decision 88 (2026-09-02):** "Keep settings for every saved trial." This ratifies the
draft's keep-everything direction: every conserved catalog row retains its required `parameters`
settings, selected and unselected alike; selection still controls full Tier-2 artifacts, not whether a
saved row keeps its settings. The answer names no canonical byte sequence and no identity function.
Therefore **B-12 remains OPEN, owned by the WP-P0-04 contract owner on its engineering half**: ratify
the exact canonical `preregistered_space_hash` preimage and add or identify its sole identity function.
Until that P0-04 contract exists, no producer may emit the digest and `TrialRecordAssembler` still
cannot construct a row. This decision does not close or narrow B-04. (`C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:745`;
`C:\tmp\LANE_PROMPTS_20260828\OWNER_PHASE0_DECISIONS_V1.md:34`;
`C:\tmp\LANE_PROMPTS_20260828\W269_PHASE0_OWNER_QUESTIONS.md:100-122,835`; §3.2 `parameters`)

### B-13 — `VIEW-SCHEMA-AND-PUBLICATION-PREIMAGE` — **CLOSED IN v1.7; CLOSURE CORRECTED IN v1.8**

**v1.8 corrections to the closure (G102-F01, G102-F02, G102-F06).** The recipe pick, the storage
answer, the retirement of “normalized SQL”, and the producer separation all stand. Three claims inside
the closure did not, and are repaired in §4.2.1 rather than re-assembled:

1. **The type vocabulary is defined here, not inherited.** “A type vocabulary containing only spellings
   already present in those tables” was false: the §3.2 cells also contain `dictionary VARCHAR`,
   `canonical-JSON VARCHAR`, and `canonical decimal VARCHAR`, none of which is in the eight-word list
   and none of which is the disclosed `VARCHAR(64)` qualifier. §4.2.1 item 5 keeps the same eight
   words, states the collapse rule P0-13 applies to reach them, and names the resulting
   ACCEPTED-not-DETECTED class.
2. **`document_version` and `publication_version` are coined by this design.** Both were introduced
   inside sets called closed while naming no value, no type, and no producer, which would let two
   honest implementations derive different fingerprints for the identical production template. §4.2.1
   now gives each a type, a sole producer, a fixed literal, and a change rule, and labels them v1.8
   design acts.
3. **SQL-whitespace “DETECTED” is withdrawn.** `DuckDBViewPublisher` produces both the SQL bytes and
   the digest over them, no reader recomputes `view_publication_hash`, and no arm changes only
   whitespace, so nothing named would fail. The matrix cell now reads NOT DETECTED and the gap is
   recorded rather than filled with a promised check.

(§4.2.1; §9)

**v1.7 closure.** Closed by §4.2.1. Exactly one of the two already-written digest recipes is cited —
`SHA256(canonical_json(...))` from the shipped identity module and the contracts README identity
encoding — with four stated reasons for not picking the P012 §5.1 exact-file recipe, chief among them
that neither fingerprint has a file to hash. `PublishedViewSchemaDocumentV1` closes the schema
document: ordered `columns` over the already-frozen §3.2 fields in table order followed by the five
§3.4.1 view-only columns, `nullable` from the "Nullable?" cells, `environment_lineage` kept nested with
its seven §3.3 fields, and a type vocabulary containing only spellings already present in those tables.
`ViewPublicationPreimageV1` closes `view_publication_hash` over five members, storage is named for every
member, `DuckDBViewPublisher` is named sole producer of the published SQL bytes, and the phrase
"normalized SQL" is retired for `published_sql_text` with no normalization transform. The DETECTED/
accepted matrix is stated, including the two accepted classes and where each is caught instead — this
lane does not claim a check it does not have. No third type dialect was invented. F-10 and R-1 are
unblocked, and B-10's dependency on item 1's fingerprint is satisfied.
(`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:31-44`;
`MTC_COMMAND_CENTER/contracts/README.md:48-55`;
`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:1-3,132-134`;
`C:\tmp\LANE_PROMPTS_20260828\DETECT_G99_BLOCKERS.md:61-63`; §4.2.1)

**[RETAINED — the v1.6 blocker text as opened, superseded by the closure above:]**

**Blocking question:** What exact byte sequences are hashed to produce the expected schema fingerprint, the observed schema fingerprint, and `view_publication_hash`, and who is the sole producer of the normalized SQL those bytes contain?

v1.5 named three separated modules — projector, inspector, and a comparer owning neither operand — and that separation survives. What it never named was a byte formula: no SHA-256, no canonical-JSON rule, no column ordering, no logical-type spelling, no nullability representation, and no nested-`STRUCT` representation for either fingerprint, and no preimage, whitespace rule, or owner for the “normalized SQL” inside `view_publication_hash`. Two honest implementations can therefore disagree on GREEN for the identical production template — `VARCHAR` versus `VARCHAR(64)`, a flattened versus nested `environment_lineage`, differing list spellings — while F-10's add-or-drop-a-column arm still fires, so F-10 does not establish the honest baseline. “Re-publishing the same hash is a no-op” is likewise not a computable identity. Required resolution: the schema owner ratifies both fingerprints as a digest over a closed canonical schema document with ordered columns, logical types, nullability, and nested fields; ratifies `view_publication_hash` as a digest over a closed preimage with a named SQL-normalization producer; names committed storage for every member; and states, for a modified copy that changes only whitespace or only type spelling, which outcome is DETECTED and which is accepted. Until then `TrialCatalogViewSchemaProjector`, `CommittedDuckDBSchemaInspector`, `DuckDBSchemaFingerprintComparer`, and `DuckDBViewPublisher` may not emit or compare a digest, F-10 and R-1 are blocked design targets, and B-10 cannot close because the commit preimage embeds the expected fingerprint. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:15-44`; `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:617-628,681-687`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:412,416`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:204-233`)

### B-14 — `ROUTING-VALUE-SOLE-PRODUCER` — **CLOSED IN v1.7; SUCCESSOR BLOCKER B-15 OPENED IN v1.8**

**v1.8 note (G102-F04).** B-14 asked *which single component produces the three values*. That question
is answered and is not re-opened: the authority is the completed run's own cell, the producer is
`RunCellDimensionsFactory`, the observer is `CommittedPathCellInspector`, and the comparer is
`PathReceiptCellComparer`. What v1.7 also asserted — that the factory “consumes only the completed
run's cell coordinates carried on the closed `CompletedRunInput`” — names an input §2.1 does not
declare, and v1.7 had simultaneously marked the three values absent by design from the run envelope
they previously rode in. The factory therefore has no declared typed input anywhere in this draft.
v1.8 does not close that by adding members to `CompletedRunInput`; it withdraws the sentence and opens
**B-15**. Consequence while B-15 is open: the factory emits no receipt, the three Hive segments are a
blocked design target, F-13 and R-8 cannot be constructed, and `PATH_RECEIPT_CELL_MISMATCH` is an
unavailable reason. (§3.4.3; §7 B-15)

**v1.7 closure.** Closed by §3.4.3. The authority is the completed run's own strategy × symbol ×
timeframe cell coordinates — the cell the sole canonical emitter already writes one result per, per the
WP-P0-08 inventory — not a path segment, not a caller, and **not P0-13**, whose v1.6 self-nomination as
"the authority" is withdrawn as the wrong frame. `RunCellDimensionsFactory` is the sole value producer
of a typed three-value receipt; `CommittedPathCellInspector` is the sole observed producer over the Hive
segments; `PathReceiptCellComparer` owns neither operand and refuses with typed
`PATH_RECEIPT_CELL_MISMATCH`. That is the same producer/observer/comparer act the draft already used for
`run_id` without opening a blocker. `symbol` is corroborated against `StrategyPackage.instrument_metadata.symbol`;
`strategy` and `timeframe` have no second repository source, which is recorded as a limitation rather
than claimed as proof. F-13 and R-8 supply the modified copy that changes exactly one Hive dimension and
must be DETECTED. No `TrialRecord` field and no `ArtifactManifest` field was added: whether the three
become columns remains **B-03** and **D-03**, both untouched.
(`MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_08_WRITER_INVENTORY_2026-08-25/WRITER_INVENTORY.md:35,102`;
`MTC_COMMAND_CENTER/contracts/mtc_contracts/package.py:18-24,27-45`;
`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2052-2056`;
`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:147-149,770-773`;
`C:\tmp\LANE_PROMPTS_20260828\DETECT_G99_BLOCKERS.md:71-73`; §3.4.3)

**[RETAINED — the v1.6 blocker text as opened, superseded by the closure above:]**

**Blocking question:** Which single component produces the `strategy`, `symbol`, and `timeframe` values that the Hive path segments and the commit envelope must both carry?

§3.2 names a sole producer for every one of the 48 row fields, but the three routing dimensions are not row fields: §3.4.1 requires them non-null from Hive path partitions and §3.4.2 says they “remain in that commit envelope as well as being physically produced by Hive paths”. A path segment is a channel, not an authority. With no named factory, a caller can supply envelope `strategy=A` while the committer writes `strategy=B` and nothing named would fail, so the brief's filterability guarantee would rest on unowned strings. B-03 and D-03 adjudicate the separate question of whether these become `TrialRecord` fields; they do not name who emits the values P0-13 writes. Required resolution: the run-envelope owner names one producer of the three values, requires the committed path bytes to equal that producer's typed receipt, and supplies a modified copy that changes exactly one Hive dimension and must be DETECTED. Until then no caller or committer may mint the values, the three partitions are a blocked design target, and no path/envelope equality may be claimed. P0-13 may not name itself the authority. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2050-2071`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:14-68`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:255`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:268-291`)

### B-15 — `RUN-CELL-COORDINATE-CHANNEL` — **OPENED IN v1.8**

**Blocking question:** Through which declared member of the closed `CompletedRunInput` do the completed
run's `strategy`, `symbol`, and `timeframe` cell coordinates reach `RunCellDimensionsFactory`?

§2.1's declared `CompletedRunInput` field list is every terminal trial receipt, family-level
statistical outputs, selection decisions, the run envelope, one opaque adapter-issued lineage-origin
receipt, and a closed set of typed `SelectedArtifactPayloadReceipt` objects — no `strategy`, no
`symbol`, no `timeframe`, and no cell-coordinate member. §4.1.3 marks all three **absent by design**
from item 2's run envelope, so the v1.5 channel is withdrawn and not restored. §3.4.3 named the factory
as sole producer, which answers B-14, but gave it an input the document does not declare. WP-P0-08's
“One JSON result per strategy × symbol × timeframe cell” is the persistence unit of the sole canonical
emitter, not a declared member of this writer's boundary type, and citing it does not make the member
exist. Two paths would follow from silence, and both are the defect this blocker exists to prevent: an
implementer invents caller fields, or re-reads the v1.5 envelope v1.7 emptied — either way routing
values are minted from an unspecified channel. **Required resolution:** the P0-13 build owner, jointly
with the WP-P0-08 migration owner for the emitter that will be the sole direct caller, ratifies the
declared member of `CompletedRunInput` that carries the cell coordinates — its name, its type, and the
rule that the factory may read no other source — before `RunCellDimensionsFactory` may emit a receipt,
before the `strategy=`, `symbol=`, and `timeframe=` Hive segments may be derived, and before F-13 or
R-8 may be constructed. This design lane will not add the member on its own authority: assembling an
input list is the act that produced this finding. This blocker is **not** P0-20-gated, and it does not
re-open B-14's authority question or touch B-03/D-03, which remain the separate schema question of
whether the three become `TrialRecord` columns. (§2.1; §3.4.3; §4.1.3;
`MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_08_WRITER_INVENTORY_2026-08-25/WRITER_INVENTORY.md:35,102`;
`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:14-68`;
`C:\tmp\LANE_PROMPTS_20260828\DETECT_G102_P013_CLOSURES.md:60-72`)

### B-17 — `CELL-COORDINATE-COMMITTED-OPERAND` — **OPENED IN v2.0**

**Blocking question:** Where, in committed storage, do the expected strategy × symbol × timeframe cell coordinates live so a reader can independently recompute the receipt operand?

`AcceptanceEvidenceReader` may use committed bytes only. The expected operand named for R-8 is the
`RunCellDimensionsFactory` receipt, but this draft commits no such receipt. Item 2's run envelope marks
all three coordinates absent by design, and item 3's `path_slot` is the Hive path being inspected — the
observed operand — so deriving the expected value from it would be the same-source comparison §3.4.3
already refuses. The existing R-8 promise therefore cannot be performed from committed bytes.
**Required resolution:** the P0-13 build owner, with the owner of the completed-run cell-coordinate
contract, ratifies an owned committed location for the independent expected receipt and re-points R-8
at those stored bytes. This section does not choose a field, type, encoding, member count, or storage
document on its own authority. B-17 is separate from and does not narrow **B-15**: B-15 asks how the
coordinates reach the factory before commit; B-17 asks where the factory's expected operand is
committed for a later reader. (§3.4.3; §4.1.3; §4.2.2; §5.2; §5.4;
`C:\tmp\LANE_PROMPTS_20260828\DETECT_GM66_P013.md:32-59`)

## 8. v1.6 limits (still binding through v2.0 except where amended below)

**v2.1 continuation.** These limits remain binding through v2.1 except where the owner-answer
qualifications below say otherwise.

1. No code, schema, writer, test, Parquet file, DuckDB database, catalog, full artifact, commit, push, PR, merge, run, optimizer, server, or repository file is produced by this lane. (`C:\tmp\LANE_PROMPTS_20260828\LANE_W51_P013_DESIGN.md:8-12,43-46`; `C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:25-36`)
2. No optimizer switch is chosen; all three existing search-regime values use the same future writer interface. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:417`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2037-2048`)
3. No statistical threshold, family definition, STOP mapping, control tier, simulator receipt, shared-allocator identity, or full-kernel lineage decision is frozen until P0-20 accepts. Every such design choice is labelled **PROVISIONAL-ON-P020** above. (`C:\tmp\LANE_PROMPTS_20260828\LANE_W51_P013_DESIGN.md:8-12,21-23`)
4. No UI or Explorer work is designed or authorized here. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:417`)
5. No legacy writer or output is deleted. Retirement occurs only after migration and verification under separate authority. (`MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_08_WRITER_INVENTORY_2026-08-25/WRITER_INVENTORY.md:29,100-105`)
6. Replay latency, artifact retention implementation, exact K/objective, and lifecycle/pin authorities remain outside this v1.6 until their named blockers close. The brief records the replay and retention direction, while this design does not invent missing numbers. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2087-2125`)

   **v2.1 qualification — decisions 87 and 88.** The retained v1.6 owner premise is superseded: the
   exact top count is 20 per strategy/market/timeframe, the other keep groups are named, and settings
   retention is “every saved trial”. Replay latency is untouched. Artifact-retention implementation,
   B-07's versioned policy/authoritative-record engineering, and B-12's WP-P0-04 preimage contract
   remain open. No scalar objective, retention implementation, identity bytes, or producer is invented
   from either answer. (`C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:744-745`;
   §7 B-07; §7 B-12)

   **v2.2 qualification — decision 128 supersedes decision 87.** The current exact selection count is
   20 separately per strategy TYPE `day`, `swing`, and `position`, with every cut-off tie retained,
   after safety/quality gates and an overall-robustness ranking. Market/timeframe partitioning and the
   other row-flag groups are no longer current automatic keep rules. Replay latency and decision 88's
   every-saved-row settings retention are untouched. Artifact-retention implementation, B-07's
   engineering policy/type/evidence binding and flag authorities, and B-12's WP-P0-04 preimage
   contract remain open. No scalar objective, identity, schema field, or pending sibling-policy value
   is supplied. (`C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:870-876,900-912`; §2.1 stage 4; §7 B-07; §7 B-12)
7. This draft deliberately does not redefine `TrialRecord`; any schema amendment returns to WP-P0-04 ownership. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:255,267`)
8. **[SUPERSEDED IN v1.7 — retained v1.6 limit:]** v1.6 invents no preimage, no committed storage location, no schema-document byte formula, no SQL-normalization rule, and no routing-value authority. Where the G93 census showed a required identity or required value with no closed source, this draft opens a named blocker (B-10 through B-14) and withdraws the affected claim rather than manufacturing bytes to look complete. `catalog_commit_hash`, `preregistered_space_hash`, both DuckDB schema fingerprints, `view_publication_hash`, and the three Hive routing values are consequently blocked design targets, and the arms that depend on them — F-4, F-10, R-1, R-3 — may not be constructed or counted. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_G93_P013.md:52-142,204-233,268-291`; `C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:29-32`)
9. **[SUPERSEDED IN v1.8 — G102-F07; retained v1.7 limit:]** **v1.7 amendment to limit 8.** v1.7 still invents nothing. Every closure cites an artefact that was already written and names its sole producer: the commit envelope is the six arguments of a shipped function serialized by a shipped serializer; the committed home is a receipt this draft already had; the fingerprint recipe is one of two already-written recipes, chosen with reasons and with the rejected one named; the schema document is the already-frozen §3.2/§3.3/§3.4.1 column list in table order with the already-decided nesting and only spellings already present in those tables; the routing authority is the completed run's own cell coordinates as already recorded by WP-P0-08. `catalog_commit_hash`, both schema fingerprints, `view_publication_hash`, and the three Hive routing values are consequently **specified** design targets rather than blocked ones, and F-4, F-10, R-1, and R-3 may be constructed once the remaining identity blockers close. **`preregistered_space_hash` is not among them**: it remains a blocked design target under B-12, which v1.7 leaves open and untouched, and B-04 leaves `param_hash` in the same state. "Specified" is not "built", "executed", or "accepted": no arm was constructed or run in this lane, and no measurement of hashing, DuckDB, or Parquet behaviour was taken. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_G99_BLOCKERS.md:19-21,87-89`; `C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:29-36`; §3.4.3; §4.1.3; §4.2.1)
10. **v1.8 replacement for limit 9 — what is already-written and what this design adds.** The v1.7
    sentence “v1.7 still invents nothing. Every closure cites an artefact that was already written”
    was not accurate, and the honest split is stated once, here, and repeated in the change log rather
    than left to a completeness banner.

    **Already-written, cited and verified by opening the file:** the `canonical_json` recipe and its
    SHA-256 wrapper (`identity.py:15-44`; `contracts/README.md:48-55`); the six hashed arguments of
    `compute_evaluation_run_hash` (`identity.py:76-95`), with the seventh parameter
    `environment_lineage` excluded from the hash (`identity.py:84`); the `ContractModel` base, its
    `extra="forbid"` / `frozen=True` config and its inherited `contract_version`
    (`base.py:12,62-67,69,71-78`); `Sha256` and `NonEmptyStr` (`base.py:15-16`);
    `InstrumentMetadata.symbol` and `StrategyPackage`'s lack of a strategy-name or timeframe field
    (`package.py:19,27-45`); `ArtifactManifest`'s field list (`trials.py:77-87`); the
    `commits/<catalog_commit_hash>.json` receipt path, already in this draft's own §4.1 layout; the
    §3.2/§3.3/§3.4.1 column tables; P012 §5.1 as the recipe explicitly *not* picked; and WP-P0-08's
    strategy × symbol × timeframe cell (`WRITER_INVENTORY.md:35,102`).

    **Assembled or coined by this design, and now labelled as such at each site:** the six-member run
    envelope (v1.7 already said “v1.7 adds only the member set it serializes”); the eight-word type
    vocabulary and the collapse rule that produces it (§4.2.1 item 5); `document_version` and
    `publication_version`, with the type, producer, literal, and change rule v1.8 supplies (§4.2.1);
    the types `CatalogCommitPreimageV1`, `PublishedViewSchemaDocumentV1`, and
    `ViewPublicationPreimageV1`; the modules `RunCellDimensionsFactory`, `CommittedPathCellInspector`,
    and `PathReceiptCellComparer`; and the reasons `COMMIT_PREIMAGE_MEMBER_MISSING` and
    `PATH_RECEIPT_CELL_MISMATCH`. None of these has a repository counterpart —
    **[SUPERSEDED IN v1.9 — W215-F03; retained v1.8 evidence sentence:]** “a contracts grep of
    `CompletedRunInput`, `RunCellDimensionsFactory`, `CatalogCommitPreimageV1`,
    `PublishedViewSchemaDocumentV1`, and `DuckDBViewPublisher` under `MTC_COMMAND_CENTER/` returned
    **0 hits** this session.”

    **v1.9 completion of that measurement (W215-F03).** That grep covered five names, only three of
    which are in the coined list above, while the change-log row for G102-F07 claimed a 0-hit grep for
    **every** coined name. A number that was not measured is not a number this draft may write, so the
    grep was completed rather than the claim softened. Greped under `MTC_COMMAND_CENTER/` this session,
    each returning **0 hits**: every name in the coined list — `document_version`,
    `publication_version`, `CatalogCommitPreimageV1`, `PublishedViewSchemaDocumentV1`,
    `ViewPublicationPreimageV1`, `RunCellDimensionsFactory`, `CommittedPathCellInspector`,
    `PathReceiptCellComparer`, `COMMIT_PREIMAGE_MEMBER_MISSING`, `PATH_RECEIPT_CELL_MISMATCH` — plus
    `CompletedRunInput`, `DuckDBViewPublisher`, `RunCellDimensionsReceipt`, `CatalogCommitIdentity`,
    `TrialCatalogViewSchemaProjector`, `CommittedDuckDBSchemaInspector`, and
    `DuckDBSchemaFingerprintComparer`. The claim held; it is now the measured one. Two entries of the
    coined list are not greppable names and are asserted from the tables themselves rather than from a
    grep: the six-member run envelope is a member set, and the eight-word type vocabulary is a set of
    physical type words that do occur in the repository as ordinary SQL words — what is coined there is
    the closed set and the collapse rule, not a new word (§4.2.1 item 5). Coining is allowed for a
    design; presenting a coined thing as already-written is what G102-F07 found and what this item ends.

    **Still blocked design targets, not specified ones:** `preregistered_space_hash` (B-12),
    `param_hash` (B-04), and — new in v1.8 — the three Hive routing values and the arms F-13/R-8,
    whose value channel is open under **B-15**. “Specified” is not “built”, “executed”, or “accepted”:
    no arm was constructed or run in this lane, and no hashing, DuckDB, or Parquet behaviour was
    measured. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_G102_P013_CLOSURES.md:112-123`;
    `C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:29-36`; §3.4.3; §4.1.3; §4.2.1; §7 B-15)
11. **v1.7 open question deliberately not answered.** Whether a DuckDB candidate view can report a `VARCHAR(64)` length qualifier is **NOT VERIFIED** — no execution occurred in this lane. §4.2.1 resolves the design around that uncertainty by using the unqualified spelling on both sides and stating the accepted-not-DETECTED consequence, rather than asserting a behaviour it did not measure.
12. A cross-document root-cause analysis of these findings and their WP-P0-21/WP-P0-22 siblings proposes a shared canonical-identity and preimage convention. That proposal is not ratified and is **not** cited anywhere in this draft as authority. Where v1.6 requires a closed preimage or a named producer, the requirement rests on the individual finding's own evidence and on the durable repository patterns, not on the proposed rule; nothing was folded that only the unratified rule would require. (`C:\tmp\LANE_PROMPTS_20260828\DETECT_GM43_ROOT_CAUSE.md:85-91,133-138`; `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:617-628,681-687`)

13. **v2.0 limits (W241).** GM66-F01 remains unresolved because its supplied verbatim hunk stopped;
    this draft still does not choose either view-preimage base class or state an exact member count.
    B-17 opens the missing committed-operand question without inventing storage. R-8 and its F-6
    sub-arm cannot be performed from committed bytes while B-17 is open; F-13 is not blocked by B-17
    because it is a writer-side comparison against the live factory receipt. The v1.9 B-15 consequence
    remains unchanged and independent. B-12 and B-15 are neither closed nor narrowed. No repository
    byte, code, schema, build, fixture, run, or artifact is produced here. (§4.2.1; §5.3; §5.4; §7
    B-12; §7 B-15; §7 B-17)

## Discrepancies

### Resolved status correction — former D-01 (not open)

The implementer lane reports were truthful historical snapshots but not the current repository status. Current merge records close the prompt/status discrepancy: WP-P0-04 records T1 PASS with zero findings, and WP-P0-08 records T2 PASS-WITH-NITS with zero required findings. The prompt’s accepted-artifact premise is therefore satisfied; former B-02 and D-01 are closed and excluded from the 16 open items. (`C:\tmp\LANE_PROMPTS_20260828\LANE_W51_P013_DESIGN.md:20`; `git-object:fead492b0b87f207aa6e7a259372b9767d4301f9:7,17-19`; `git-object:88eab9c93b7c285b990d07502ea1ec476034e8d5:7,9-14`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_N70_P013_V11.md:28-33`)

**v2.0 count note.** The historical 16-item count above is retained. Former B-02 and D-01 remain
closed and excluded; the current count is 14 open items — 11 blockers and D-02/D-03/D-04.

### D-02 — Typed sparse parameter columns vs one mapping field

The brief and writer inventory call for one typed nullable column per parameter, but the repository `TrialRecord` model contains one non-null `parameters: dict[str, Any]`. Because P0-13 may not redefine the model, this draft uses canonical JSON physical lowering and blocks finalization on B-03. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2060-2063`; `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_08_WRITER_INVENTORY_2026-08-25/WRITER_INVENTORY.md:13-16`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:27-33`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:255`)

### D-03 — Partition dimensions are not `TrialRecord` fields

**[SUPERSEDED IN v1.8 — G102-F05; retained v1.5 text, live and contradictory until this fold:]** The brief’s Parquet layout requires `strategy`, `symbol`, and `timeframe` path/query dimensions, but those fields do not exist in the repository model. “This draft exposes them from a run envelope rather than silently changing the contract”; B-03 requires schema-owner adjudication. (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2052-2056`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:14-68`)

**v1.8 controlling text for D-03.** The discrepancy itself is unchanged and still open: the brief’s Parquet layout requires the three path/query dimensions and the repository `TrialRecord` has none of them, so B-03 still requires schema-owner adjudication. What is corrected is the channel sentence, which named a v1.5 mechanism v1.7 had already withdrawn. **This draft does not expose the three values from a run envelope.** They are marked **absent by design** from item 2's run envelope and are carried exactly once, in item 3's hash-free `path_slot` — the Hive partition directory (§4.1.3). Their value authority is §3.4.3's `RunCellDimensionsFactory`, and the declared channel by which the completed run's cell coordinates reach that factory is open under **B-15**. (§3.4.3; §4.1.3; §7 B-03; §7 B-15)

### D-04 — Selected-artifact manifest and address carry no per-trial identity

The v1.5 design retains the v1.3 requirement that the committed selected-artifact `manifest.json` and directory address bind `trial_id` (plus `package_hash`, `evaluation_run_hash`, `param_hash`) so `ArtifactCommitVerifier` has an independent committed operand. The repository `ArtifactManifest` has only `package_hash`, `deployment_identity_hash`, `evaluation_run_hash`, `dataset_hash`, `kernel_version`, `simulator_class`, `simulator_version`, `unsimulated_controls_hash`, `allocation_policy_version`, `environment_lineage`, and the brief's Tier-2 layout is the package-only `artifacts/<package_hash>/` while its selection rule is per trial. Because `compute_package_hash` carries no trial sequence and `make_trial_id` does, two selected trials can share a `package_hash` and collide on the package-only address. This draft resolves the ambiguity with a per-trial address and per-trial manifest identity rather than silently amending the contract; B-09 requires schema-owner adjudication. (`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:19,23-24,77-88`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:54-73,132-135`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2075-2087`; `C:\tmp\LANE_PROMPTS_20260828\DETECT_N81_P013_V12.md:7-12`)

## 9. Re-audit entry condition

**[SUPERSEDED IN v1.7 — retained v1.6 entry condition:]** Re-audit may start only after B-01 closes with accepted P0-20 artifacts. The reviewer must then replace or affirm every **PROVISIONAL-ON-P020** item, retain the now-verified WP-P0-04/P0-08 merge acceptance records, resolve B-03 through B-14 — including the five v1.6 blockers B-10, B-11, B-12, B-13, and B-14, none of which are P0-20-gated and each of which must close before the arms it blocks can be constructed — and demand real RED/GREEN evidence for every §5/§6 probe before build acceptance. (`C:\tmp\LANE_PROMPTS_20260828\LANE_W51_P013_DESIGN.md:8-12`; `git-object:fead492b0b87f207aa6e7a259372b9767d4301f9:7,17-19`; `git-object:88eab9c93b7c285b990d07502ea1ec476034e8d5:7,9-14`; `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/TESTS.md:3-14`)

**[SUPERSEDED IN v1.8 — W203 G102 fold; retained v1.7 entry condition:]** **v1.7 entry condition.** Re-audit may start only after B-01 closes with accepted P0-20 artifacts. The
reviewer must then replace or affirm every **PROVISIONAL-ON-P020** item, retain the verified
WP-P0-04/P0-08 merge acceptance records, and resolve the nine remaining open blockers — **B-03, B-04,
B-05, B-06, B-07, B-08, B-09, B-12** alongside B-01 — of which **B-04** and **B-12** must close before
any row can be assembled and therefore before any §5 arm other than the F-2/F-3 boundary probes can be
constructed. The reviewer must additionally **re-audit the four v1.7 closures themselves**: whether
§4.1.3's required/absent-by-design split is the right one, whether §4.2.1's choice of `canonical_json`
over the P012 exact-file recipe holds and whether its two accepted-not-DETECTED classes are acceptable,
and whether §3.4.3's routing authority survives contact with the migrated emitter. A closure is a
design act, not an acceptance. Real RED/GREEN evidence remains required for every §5/§6 probe before
build acceptance. (`C:\tmp\LANE_PROMPTS_20260828\LANE_W51_P013_DESIGN.md:8-12`; `MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:24,28`; `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/TESTS.md:3-14`)

**v1.8 entry condition.** Re-audit may start only after B-01 closes with accepted P0-20 artifacts. The
reviewer must then replace or affirm every **PROVISIONAL-ON-P020** item, retain the verified
WP-P0-04/P0-08 merge acceptance records, and resolve the **ten** remaining open blockers — **B-03,
B-04, B-05, B-06, B-07, B-08, B-09, B-12, B-15** alongside B-01 — of which **B-04** and **B-12** must
close before any row can be assembled and therefore before any §5 arm other than the F-2/F-3 boundary
probes can be constructed, and **B-15** must close before the three Hive routing segments exist or
F-13/R-8 can be built. The reviewer must additionally **re-audit the four v1.7 closures and the six
v1.8 repairs**, specifically:

1. whether §4.1.3's required/absent-by-design split is the right one, and whether the corrected
   member contract — six declared members plus the inherited `contract_version` — is what an
   implementer will actually serialize;
2. whether the ACCEPTED-not-DETECTED limit on omitting the inherited `contract_version` is acceptable,
   or whether the envelope should not subclass `ContractModel` at all;
3. whether §4.2.1's choice of `canonical_json` over the P012 exact-file recipe holds;
4. whether §4.2.1 item 5's collapse rule is the right vocabulary rule, and whether the
   dictionary/canonical-annotation and `VARCHAR(64)` classes it accepts are acceptable;
5. whether the literals `"1"` fixed for `document_version` and `publication_version` are the right
   design constants, given both members are coined here and inherited from nothing;
6. whether `view_publication_hash` may remain without an independent recompute while its SQL producer
   is also its digest producer, and whether an arm that changes only SQL whitespace is required;
7. whether §3.4.3's routing authority survives contact with the migrated emitter, and what B-15's
   ratified channel turns out to be.

A closure is a design act, not an acceptance, and a corrected closure is not a stronger one. Real
RED/GREEN evidence remains required for every §5/§6 probe before build acceptance.
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W51_P013_DESIGN.md:8-12`;
`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:24,28`;
`MTC_COMMAND_CENTER/contracts/mtc_contracts/base.py:12,62-67,69`;
`MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/TESTS.md:3-14`; §7 B-15)

**v1.9 amendment to the entry condition (W215).** The v1.8 entry condition above stands in full: the
same ten open blockers, the same B-04/B-12 precondition on row assembly, and the same seven re-audit
questions. v1.9 adds an eighth and corrects one premise the seven rested on.

8. **Whether B-15's reach is now stated correctly.** v1.8 applied B-15 to F-13 and R-8 alone. v1.9
   records that while B-15 is open no part path may be derived at all, so every §5 arm whose input is
   a staged or committed part, a commit receipt, or the published view — and every §6 gate row that
   rests on one — is a blocked design target under B-15 as well, leaving only the writer-boundary
   probes F-2, F-3, and F-8 (§4.2.2, §5.3, §5.4, §6). The reviewer should decide whether that is the
   right reading of §4.1's layout; **whether F-9 is inside or outside it**, which §5.3 deliberately
   leaves undecided because the selected-artifact tree carries no routing segment; and, if the reading
   holds, whether B-15 belongs ahead of B-04 and B-12 in the closing order.

The corrected premise is **§5.4's** “R-1..R-7 are unaffected by B-15”, which the seven questions above
inherit whenever they ask what a reviewer can construct: R-1..R-8 do **not** become constructible when
B-04 and B-12 close, while B-15 stands. Open items are unchanged at **13**, recounted from the §7 and
Discrepancies headings rather than carried forward. A corrected count is not a repair of the thing
counted, and this amendment closes nothing.
(`C:\tmp\LANE_PROMPTS_20260828\DETECT_G104_P013_FOLD.md:1-20`;
`C:\tmp\LANE_PROMPTS_20260828\LANE_W215_P013_RESIDUAL.md:1-56`; §4.1; §5.3; §5.4; §7 B-15)

**v2.0 amendment to the entry condition (W241).** The reviewer now has **11** open blockers to resolve:
the v1.9 set plus **B-17**. B-15 must close before a factory receipt can exist; B-17 must then close
before R-8 can independently compare committed expected coordinates with the committed path. The two
questions are sequential and neither answers the other. GM66-F01 also remains an unresolved finding —
not a named blocker in this version, because its supplied hunk stopped — so re-audit must require a new
byte-matching patch that either cites an already-ratified base class/member count or opens the
inheritance question without defining the count here.

9. **Whether the reader has two committed coordinate operands.** The reviewer must confirm that any
   B-17 closure names an independently committed expected receipt, not a second projection of the Hive
   path, and that R-8 is re-pointed at those exact stored bytes. (§3.4.3; §4.1.3; §5.4; §7 B-17)

**v2.1 amendment to the entry condition (W287).** The same 11 blocker headings remain. For **B-07**,
the reviewer must not re-ask the keep-rule question; decision 87 is final, and review is limited to the
versioned policy encoding, the owned market-dimension binding, and authoritative lifecycle/pin-record
delivery. For **B-12**, the reviewer must not re-ask the settings-retention question; decision 88 is
final, and review is limited to the WP-P0-04-owned canonical preimage and sole identity function. The
X-1 sibling sites in P0-14 and P0-22 remain open on that same engineering contract. (§7 B-07; §7 B-12;
`C:\tmp\LANE_PROMPTS_20260828\W269_PHASE0_OWNER_QUESTIONS.md:624-629,690-695`)

**v2.2 amendment to the entry condition (W296).** The same 11 blocker headings remain. For **B-07**,
the reviewer must not re-ask row 6, but must use decision 128 rather than superseded decision 87. The
review must verify safety/quality gating before overall-robustness ranking; best 20 separately for
owned strategy TYPE `day`, `swing`, and `position`; retention of every cut-off tie; a versioned policy
and fresh-evidence binding under the `NEW-BY-ADDENDUM-32` item; and authoritative lifecycle/pin records
only as producers of their independent row facts. It must not restore market/timeframe partitioning or
automatic selection by the Pareto, robust, promoted, or pinned flags. The exact robustness comparison,
type/receipt bindings, and executable tie handling remain engineering work, not owner re-asks. B-12,
decision 88, and X-1 remain unchanged. Sibling P0-20/P0-21 values not given in addendum 32 remain
`OWNER-ANSWERED-SHAPE, VALUE PENDING (addendum 32)` and must not be defaulted here. (`C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:856-928`; §2.1 stage 4; §7 B-07; §7 B-12)

**[SUPERSEDED IN v2.1 — W287; retained v2.0 final count and verdict follow.]**

Open items are **14**: 11 open blockers and 3 open discrepancies. B-12 and B-15 remain open and
unchanged; B-16 is absent because GM66-F01 stopped. A partial patch is not acceptance.

Until then the truthful state is: **design exists; build and acceptance do not.** (`C:\tmp\LANE_PROMPTS_20260828\LANE_W51_P013_DESIGN.md:8-12`)

**v2.1 current count and verdict.** Open items remain **14**: 11 named blocker headings and three open
discrepancies. B-07 and B-12 retain their headings because only their owner halves closed; their
engineering halves remain open for the named owners and reasons above. B-15 remains open and
unchanged; B-16 remains absent because GM66-F01 stopped. The truthful state remains: **owner choices
recorded; design exists; build and acceptance do not.** (§7 B-07; §7 B-12; §7 B-15; § Discrepancies)

**[SUPERSEDED IN v2.2 — W296; retained v2.1 current count and verdict above.]**

**v2.2 current count and verdict.** Open items remain **14**: 11 named blocker headings and three open
discrepancies. B-07 retains its heading because decision 128 closes only its owner rule; the named
engineering policy/type/evidence and flag-authority work remains open. B-12 retains its heading for
the unchanged engineering preimage half under decision 88. B-15 remains open and unchanged; B-16
remains absent because GM66-F01 stopped. The truthful state remains: **current owner amendment
recorded; design exists; build and acceptance do not.** (§2.1 stage 4; §7 B-07; §7 B-12; §7 B-15;
§ Discrepancies)
