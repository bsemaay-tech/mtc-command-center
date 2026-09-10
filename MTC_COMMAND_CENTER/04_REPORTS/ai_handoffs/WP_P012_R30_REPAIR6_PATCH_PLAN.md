# WP-P0-12 re-seal #30 — repair round 6 patch plan (NOT APPLIED)

**Author:** Lead (claude-opus-5) · **Date:** 2026-09-10 · **Status:** awaiting owner approval
**Target:** `mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json`
**Evidence:** `C:\tmp\P012_VALIDATOR_LANE_20260909\THREE_REAL_FINDINGS_MEASURED_20260910.md`

Three fields found by the fail-closed validator (PR #170), each cross-checked against a record the
validator did not author. **Nothing in this plan has been applied.**

---

## 1. The cost of this round, measured before proposing it

This is the part worth reading first, because it is the opposite of what a change to a sealed package
usually costs.

**The seal is computed over 19 members and the manifest is not one of them.** Measured from
`verify_bceg.py:2952-2965` — the seal is
`sha256("\n".join(sorted(f"{path}:{digest}")))` over `manifest["files"]`, whose 19 entries are:

| members | count |
|---|---|
| `DERIVATIONS.md` | 1 |
| `scenario_catalog.json` | 1 |
| `golden/corrected_vnext/RULE2-*.json` | 17 |

**And the manifest's own byte digest is pinned nowhere.** Measured — its sha256
`9d54f48ef4bf39d3…` appears in none of `implementation_anchor.json`,
`semantic_coverage_review.json`, or `implementation_anchor.json.sha256`. The gate loads the manifest
five times and reads it *structurally* (schema, the 19-member count, the design pin, the event-order
pin, the section-18 census). It never digests it.

Therefore all three repairs:

- **do not change `EXPECTED_SEAL_SHA` (`b6ac5a46…`)** — no re-seal #31;
- **do not invalidate the anchor sidecar** — the anchor is not being edited;
- **do not invalidate the Section-16 receipt** — `reviewed_identities` carries no manifest digest;
- **do not require a baseline re-run** — the baseline files are untouched.

Empirical corroboration: repairs 4 and 5 (`f8e73f6b`, `4eb75b44`) already edited this same manifest
and the gate stayed at zero refusals.

**Contemporaneous corroboration, written by someone else.** Commit `eda17c3f` (2026-09-03) edited this
manifest and recorded in its own note: *"EXPECTED_SEAL_SHA is computed over files[] path:sha only and is
unchanged."* That is an independent statement of §1's central claim, made ten days before I measured
it, by an actor who had just had the gate refuse them.

**This round is metadata-only.** That is the measured claim; §5 says how to falsify it.

---

## 2. Repair A — `section_16_review` contradicts the installed receipt

**Now:**

```json
"section_16_review": {
  "status": "PENDING",
  "statement": "The mandatory SEMANTIC_COVERAGE_REVIEW ... has NOT been performed and is REQUIRED
                BEFORE BUILD ACCEPTANCE. It is owner-held human review. This lane neither claims nor
                performs it, ...",
  "reviewer_independence_constraint": "..."
}
```

The sibling `semantic_coverage_review.json` is signed `2026-09-08T21:25:22+03:00` by
`Gemini 3.8 Flash High`, has 6 items, `unresolved_items: []`, and
`owner_ratification: {ratified: true, chain: [#5 … #30]}`. The gate reads `section_16_review` **zero
times** (`grep -c` = 0).

**Proposed:**

```json
"section_16_review": {
  "status": "PERFORMED_OWNER_RATIFIED",
  "status_measured_at": "2026-09-10, re-seal #30",
  "statement": "The mandatory SEMANTIC_COVERAGE_REVIEW required by Design section 16 HAS been
                performed and is installed at contracts/semantic_coverage_review.json, signed
                2026-09-08T21:25:22+03:00 by gemini-3.8-flash-high as a delta review of
                ca1a4457..d06aa741, with 6 items, unresolved_items empty, and owner ratification
                recorded through re-seal #30. The gate enforces the receipt's presence, its closed
                disposition domain and its content identities directly; it does not read this
                summary, which is descriptive only.",
  "reviewer_independence_constraint": "<unchanged>"
}
```

Two things deliberately included: the field says **when** it was measured, and it says **it is not
enforced**, so no future reader mistakes it for a check.

**Owner decision inside this repair:** `PERFORMED_OWNER_RATIFIED` is my wording. The alternative that
stays closer to the old value is `COMPLETE`. I prefer the longer one because "complete" invites the
question *complete for which re-seal*, which is the exact ambiguity that produced this finding.

---

## 3. Repair B — the baseline pin authorises the wrong run

**Now** (`legacy_event_order_map_pin.baseline_manifest`):

| field | value | status |
|---|---|---|
| `sha256` | `c5d7d91d06b26ab6…` | the re-seal-24 file |
| `EXPECTED_SEAL_SHA_consumed` | `320b432efeb9c585…` | re-seal #24's seal |
| `authorization` | "…approved 2026-09-05 20:48, re-seal24…" | correctly self-labelled |

The file at that path was rebuilt `2026-09-08T19:56:34+03:00` for the **re-seal #30 candidate**; it now
digests to `256c3593db27df56…` and consumes `b6ac5a46…`, the current seal. **The current digest appears
zero times in the manifest.**

The gate is not deceived: it re-reads the file and refuses if
`EXPECTED_SEAL_SHA_consumed != seal` (`verify_bceg.py:2980`), and it independently enforces
`baseline_manifest_sha256` as a **content identity key** of the receipt
(`verify_bceg.py:66-74`, refusal at `:650-654`) — where the receipt correctly declares `256c3593`.

So the same fact is declared twice: **enforced in the receipt and correct; unread in the manifest and
wrong.**

**Proposed** — add the current run *beside* the old one; change no historical value:

```json
"baseline_manifest": {
  "path": "C:\\tmp\\P012_BASELINE_RUN\\BASELINE_BYTES_MANIFEST.json",
  "sha256": "c5d7d91d06b26ab6b6ffee5f3a3f5e4ff00fefb5b6d236d7b2e8014e38a33242",
  "sha256_measured_at": "re-seal #24, 2026-09-05",
  "superseded": true,
  "authorization": "<unchanged>",
  "EXPECTED_SEAL_SHA_consumed": "320b432efeb9c585fbdd7b09fc4c49e6e696a01e6008ab32af24c758486edaaa",
  "current_run": {
    "sha256": "256c3593db27df5643d114beaafccb1709d32fe2e89ca147416495bff443e772",
    "EXPECTED_SEAL_SHA_consumed": "b6ac5a4616c15c416b3bac2f102e62b0f051287e767e5e8b1e6656ea19ab3eda",
    "created_at": "2026-09-08T19:56:34.134141+03:00",
    "authorization": "One full baseline execution for the re-seal #30 candidate; 17/17 VALID.",
    "measured_at": "2026-09-10",
    "enforced_by": "verify_bceg.py:2980 against the file, and reviewed_identities.baseline_manifest_sha256 as a content identity key"
  }
}
```

**The old values are not overwritten.** Re-seal #24's authorization was a real owner permission for a
real run; erasing it would destroy the record of what was approved. This is the defect repaired in
`2f1008ab`, and I am not repeating it.

**A second, separate problem this repair does not fix.** The pinned `path` is
`C:\tmp\P012_BASELINE_RUN\...` — a mutable, machine-local directory outside the repository. That is
*why* the pin went stale silently: the file was overwritten in place. No reviewer on another machine
can verify this pin at all. Fixing that means moving the baseline manifest under version control or
into a content-addressed store, which is a design change, not a repair. **Flagged, not attempted.**

---

## 4. Repair C — a dated identity written in the present tense

**Now:**

| field | declared | live | receipt |
|---|---|---|---|
| `worktree` | `C:\WFMERGE54` | `C:\P012BATCH` | — |
| `head_commit` | `108ea066a710…` | `d64d8fceabb5…` | `d06aa741c32a…` |
| `mtc_v2_core_tree_oid` | `c7f4aa1b4679…` | `9a3283ae5e2b…` | `9a3283ae5e2b…` |

`verification` ends "…**run this session**". The gate reads this field **zero times**.

**Proposed** — date the snapshot, keep the values, drop the present tense:

```json
"repository_evidence_identity": {
  "measured_at": "2026-08-30, worktree C:\\WFMERGE54",
  "historical": true,
  "worktree": "C:\\WFMERGE54",
  "head_commit": "108ea066a710ff7ef5c09246903fe3d523da1d56",
  "mtc_v2_core_tree_oid": "c7f4aa1b46792c67c171237cea62c06497aa35ea",
  "verification": "read-only git rev-parse HEAD and git rev-parse HEAD:.../mtc_v2/core, measured in
                   the session dated above and NOT re-measured since; both matched the design premise
                   at Design section 1 as of that measurement. No git mutation was performed. The
                   live identity for any given re-seal is carried by
                   semantic_coverage_review.json.reviewed_identities, which the gate enforces; this
                   block is a dated snapshot and is not read by the gate."
}
```

**The values stay.** `108ea066` is a real commit and `C:\WFMERGE54` was a real worktree; the numbers
were true when taken. Only the tense and the missing date are wrong. Overwriting them with today's
values would make the record true today and false tomorrow — the treadmill.

### The date, now measured — and it was not the date I guessed

I first wrote `measured_at: "2026-08-30"`, inferred from `108ea066` being the tip of
`root/current-20260829`. **That was the wrong kind of date** — the date a recorded commit was made, not
the date the measurement was taken. Measured:

| fact | value | source |
|---|---|---|
| `108ea066` committed | `2026-08-30T20:43:18+03:00` | `git log -1 --format=%cI 108ea066` (merge of PR #145) |
| block **introduced** | `5e8e5794`, `2026-08-31T22:50:56+03:00` | `git log -S 'WFMERGE54' -- <manifest>` |

So the correct value is **`measured_at: "2026-08-31"`** — on that day, in worktree `C:\WFMERGE54`, HEAD
was the previous day's merge. Internally coherent, which corroborates that the numbers were true when
taken.

### And the history says exactly how it went stale

`git log -S '108ea066…' -- <manifest>` returns a second commit: **`eda17c3f`, 2026-09-03T15:11:48**.
Its diff moves `seal_state.IMPLEMENTATION_BASE_SHA` **off** `108ea066` (to `5e8e5794`), with this note:

> "…the manifest seal/seal_state IMPLEMENTATION_BASE_SHA members moved 108ea066 -> 5e8e5794 to equal
> the anchor (repin_base14.py had re-pinned the anchor only; the gate refused
> IMPLEMENTATION_BASE_ANCESTRY_MISMATCH at W316B)…"

**`repository_evidence_identity.head_commit` was left at `108ea066` by that same commit.** The identical
value was corrected in the field the gate reads, because the gate refused, and left untouched in the
field the gate does not read — in one file, in one commit, on 2026-09-03.

That is not a coincidence, and it is not carelessness. It is the mechanism: **the gate's coverage is
the de-facto maintenance boundary.** Fields inside it get fixed because they fail loudly; fields
outside it rot because nothing ever asks. Repairing this one field changes three strings; wiring the
validator into the gate is what changes the mechanism.

---

## 5. How to falsify the "metadata-only" claim

Do not take §1 on my word. After applying, in a clean clone:

1. `python -m mtc_v2.tests.corrected_vnext.verify_bceg --output receipt.json`
2. Confirm `EXPECTED_SEAL_SHA` still reads `b6ac5a4616c15c41…` and `acceptance_blockers` has not grown.
3. Byte-compare `receipt.json` against the pre-repair receipt; the only permitted differences are the
   fields this plan edits and any timestamp the receipt records.

**If the seal moves, this plan is wrong and must be withdrawn**, because a moved seal means the
manifest is load-bearing in a way I failed to find, and every conclusion in §1 falls with it.

---

## 6. Governance

- **Protected path.** `contracts/` was ruled a canonical feature contract by this Lead on 2026-09-09,
  so the commit requires an `APPROVED-PATCH-PLAN: <task_id>` trailer validated against
  `TASK_HISTORY.json`. **No such task id exists for this round.** It must be created by the owner
  before any commit.
- **Not applied.** No production record has been touched. This is a plan.
- **Does not change any verdict.** All three fields are unread by the gate, so the package's
  acceptance state is exactly what it was before this document existed. Repairing them removes three
  false statements from a record humans read; it unblocks nothing.

## 7. What I recommend

Approve A and C as a single metadata commit. **Hold B** — not because the repair is wrong, but because
the `path`-outside-the-repo problem in §3 means B will go stale again on the next baseline run, and it
is worth deciding the storage question once rather than re-pinning by hand a fourth time.
