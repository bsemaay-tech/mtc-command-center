# Section-16 review packets — the standard

Derived from four measured failures during WP-P0-12 re-seal #29/#30 (2026-09-06 → 2026-09-09).
Applies to every future Section-16 review packet, including the R7 production-lineage receipt and
every re-seal after #30.

Authored by the session that caused two of the failures; adopted, corrected and extended by the Lead
session `tradingview-lab-clean-c1`. Landed in the repo 2026-09-09 after re-seal #30 merged — it was
deliberately held out of that PR to avoid widening its scope.

**Why this exists.** In one evening, three different Section-16 reviews produced, or nearly produced,
a disposition that was not backed by reading the subject. None looked wrong at the time. All were
caught by accident, not by design. A fourth mode was found the next day.

---

## The four failures, measured

### 1. The reviewer was told not to read — receipt #29

`R29_PROMPT_NOTOOLS.md` opens: *"Answer from the text below ONLY. Do not use any tools. Do not read,
list, or search any files."* It was written to work around a route that kept dying. It was
**declared, not concealed** — but #29's six dispositions were never checked against bytes, and #30 is
a delta that inherits them.

Stated precisely: the eight pinned *identities* were mechanically re-measured and the Item-2 hunk
coverage was regenerated with the gate's own parser. The *semantic* content of the six dispositions
was checked against nothing. "#29 is unverified" is too broad; "#29 is fine" is too generous.

### 2. The reviewer was told to verify, and could not — packet R30

*"Verify that claim rather than accepting it"* appeared three times in `TASK.md`. Measured at the
sandbox's pinned head `108ea066`:

| path | state |
|---|---|
| `mtc_v2/tests/corrected_vnext/` | ABSENT |
| `mtc_v2/golden/` | ABSENT |
| `mtc_v2/core/economic_records/funding/` | ABSENT |
| `mtc_v2/core/economics.py` | ABSENT |
| `mtc_v2/tests/.../verify_bceg.py` | ABSENT |
| `mtc_v2/core/types.py` | **PRESENT, STALE** |
| `mtc_v2/core/results.py` | **PRESENT, STALE** (185 lines; candidate has 1071) |
| `mtc_v2/core/runner.py` | **PRESENT, STALE** |

The first account of this listed `types.py` as ABSENT. It is not — a `grep -c` whose zero-match exit
status fired an "absent" fallback, and the fallback was recorded as a measurement. The error ran in
the direction that **understates** the danger, because present-but-stale is the worse category.

### 3. The reviewer read something, and it was stale — attempt 7

The worst of the four. `core/results.py` exists in that sandbox — 185 lines, **zero** occurrences of
`mark_price` or `oracle_price`. Attempt 7 cited `core/results.py:629-644` and `verify_bceg.py:1532`,
called a census "directly verified", and reached **PASS**. `verify_bceg.py` is not in that checkout at
all. Three of six census files differ between the stale tree and the candidate.

**Absence makes a reviewer stop. Staleness makes it confident and wrong.**

### 4. The reviewer read the right bytes and was still wrong — attempt 8

Run against a packet already rebuilt to R1–R7: candidate and prior bytes both present, all 236
byte-verified against their Git objects, outside reads forbidden. It returned `SUCCESS`, all six items
`UNCHANGED`, and its Item-6 consumer census matched an independent census. It was still rejected,
because it stated that hunks in `core/types.py` and `core/results.py` bind to census row `S18-04`.
Authoritative, from the prior receipt **inside the packet**: `types.py → S18-09`,
`results.py → S18-10`, `economics.py → S18-02`. Two of three bindings were wrong.

It inferred an identifier the packet states explicitly. Attempt 7, which read the wrong tree entirely,
named all three correctly. **A plausible, internally consistent report is not evidence of anything,
and "the verdict looks reasonable" is not a check.** It matters because reviewer reason strings are
copied verbatim into the sealed receipt: a wrong row id becomes a false statement inside a contract
artifact.

---

## The rules

### R1 — The packet contains the bytes under review
Every file the brief cites, or asks the reviewer to check, is **in the packet** — not referenced by
repository path, not assumed present. Include a file even when it did not change, if a claim depends
on its content. *Kills failures 2 and 3.*

### R2 — The brief forbids reading anything outside the packet
State it: *"Read ONLY files inside this packet. Any repository path appearing in this document is
provenance text, not a file to open."* Without this the reviewer may find a **stale** copy of the
right filename and cite it in good faith. *Kills failure 3.*

### R3 — Never ask for a verification the packet cannot support
Before writing "verify this yourself", check the bytes are in the packet under R1. If not, add them or
**delete the instruction**. An unsatisfiable demand next to pressure for a verdict manufactures false
confidence. *Kills failure 2.*

### R4 — A `NOT VERIFIED` section is mandatory and must be non-empty
A review returning an empty `NOT VERIFIED` section on a large delta is **suspicious, not thorough**.

### R5 — Never disable the reviewer's tools to work around a route failure
Fix the route or split the review. Do not convert a file-checking review into a text-only one to get
an answer. That produced failure 1, and it is invisible in the resulting receipt. *Kills failure 1.*

### R6 — Grep the returned report before assembling any receipt from it
Two minutes. Check every cited path and line number against the packet's `PATH_MAP`. A citation to a
file not in the packet is a **discard**, not a nit. Mechanised — see below.

### R7 — A dry-run verdicts file must be structurally invalid
A `DRYRUN_VERDICTS.json` with six fabricated `UNCHANGED` dispositions and a label saying "NOT A
REVIEW", fed to the assembler with the ratification flag, would produce a receipt that **passes the
gate's own validator**. A label is not protection. Make the placeholder fail the assembler by
construction — an invalid `disposition` value, or a required field omitted.

### R8 — Every identifier binding must cite the packet location that states it
Any claim that a hunk, file or change binds to a ratified row must name the packet file and place
where that binding is recorded. Inference from the shape of the change, from a row's name, or from
plausibility is not permitted. *"Binding not stated in packet"* is a correct answer; a confidently
wrong identifier is not. *Kills failure 4.*

### R9 — Every digest must be labelled `COMPUTED` or `QUOTED`
`COMPUTED` requires naming the packet file that was hashed. `QUOTED` requires naming the document the
value was read from. Where a digest appears in the brief, say so in the brief, so quoting it proves
nothing and the reviewer is not tempted to call it a measurement.

### R10 — Never write to a filename the reviewer owns
Added 2026-09-09. A Lead extraction script wrote the review envelope to
`T0_OPUS_R30_R3_REPORT.md` — the filename the auditor had itself been told to write — and destroyed a
1026-word report, replacing it with a 447-word summary. Recovered only because the lane transcript at
`~/.claude-max/projects/<slug>/<session_id>.jsonl` retains the original `Write` call.

Give the reviewer's own output and any Lead-side extraction **disjoint filenames**, and treat the
transcript as the recovery path of last resort.

---

## Pre-flight checklist

Run before launching any Section-16 lane. Each line is a yes/no with evidence.

- [ ] Every file cited in the brief is present **in the packet** (R1)
- [ ] `PATH_MAP` lists every packet member with its candidate-tree path
- [ ] Brief states "read ONLY files inside this packet" (R2)
- [ ] Every "verify this" instruction has its bytes in the packet — or has been deleted (R3)
- [ ] `NOT VERIFIED` section is required by the brief (R4)
- [ ] Reviewer tools are **enabled**; no route workaround disabled them (R5)
- [ ] Brief requires every binding to cite where the packet states it (R8)
- [ ] Brief requires every digest labelled `COMPUTED` or `QUOTED` (R9)
- [ ] Lead-side output filenames are disjoint from the reviewer's (R10)
- [ ] Reviewer family bar honoured: not Codex, not Claude. Gemini 3.8 is the Section-16 reviewer;
      3.7 is the T0 corroborator — a different role, do not swap them
- [ ] Manifest digests recomputed after the last packet edit, and the launcher re-verified them
- [ ] No dry-run verdicts file exists that the assembler would accept (R7)

After the report returns, before assembling anything:

- [ ] `check_review_report.py` run against the report and the packet, and it exits 0 (R6)
- [ ] `NOT VERIFIED` section present and plausible for the size of the delta
- [ ] No item marked `UNCHANGED` without its strongest-case-for-`CHANGED` paragraph
- [ ] Owner ratification present, and honouring any condition attached to it

---

## The mechanised half — `check_review_report.py`

R6 is implemented rather than left as a habit. The checker verifies that a verdict block parses, that
no item is `CHANGED` and overall carries forward, that every cited path resolves **inside** the
packet, that no line citation exceeds its file, and that the report actually cites the packet trees.

```
python check_review_report.py --packet <packet dir> <report.md>
```

**Validated RED/GREEN, 2026-09-09**, against the two real reports:

| input | result |
|---|---|
| attempt 7 — the report that reached PASS while reading the wrong tree | **REJECTED**, exit 1: *"never cites CAND/, PRIOR/ or KERNEL_BOOKKEEPING/"* and *"10 citation(s) point at the live (stale) checkout"* |
| attempt 9 — the review actually accepted into receipt #30 | **ACCEPTED**, exit 0, 14 packet-tree citations |

### What this checker does NOT establish — read this before relying on it

An earlier draft of this section claimed the checker *"discriminates on behaviour … so rewording a
report cannot satisfy it."* **That claim is false and is withdrawn.**

It was tested by an independent auditor on 2026-09-09. Attempt 7's report was taken and **one
mechanical substitution applied to citation format only** — `file:///C:/LAB/…/` rewritten to `CAND/`,
two lines changed, every claim, verdict, line number and word of prose byte-identical. The checker
**accepted it, exit 0.**

The reason is structural, not a tuning problem:

- the packet-tree check is `re.findall(r"\b(?:CAND|PRIOR|KERNEL_BOOKKEEPING)/", text)` — **a single
  occurrence of `CAND/` anywhere in the prose satisfies it**;
- the stale-checkout check is a regex on `file:///C:/LAB/…`, which disappears when the URLs are
  rewritten;
- **the path-resolution check cannot detect a stale read by construction** — a stale tree has the
  *same paths* as a fresh one, which is what staleness is;
- the `path:line` check compares against the **packet** copy, not the tree the reviewer read, so
  attempt 7's `results.py:629-644` passes against the 1071-line packet copy even though the 185-line
  tree it actually read makes that citation impossible.

**So the checker detects the citation *pattern* attempt 7 used. It does not establish that a reviewer
read the packet.** Treat a pass as "no disqualifying citation pattern found", never as evidence of a
real read. R6 is **assisted**, not mechanised, and the human check it describes still has to happen.

What it does catch, and is worth keeping for: the `file:///` stale-checkout habit, unparseable verdict
blocks, `CHANGED` items, and genuinely **invented** paths that resolve nowhere in the packet.

### Two ways to mechanise this were tested and both failed — do not retry them

Measured 2026-09-09 against the real reports, so the next session does not spend the time again.

**Candidate 1 — require verbatim quotes that resolve inside the packet.** Extract every fenced-block
line and inline-backtick span of ≥12 chars, and check it appears somewhere in the packet's 254 files.

| report | spans | resolve in packet | rate |
|---|---|---|---|
| attempt 7 (**read the wrong tree**) | 47 | 28 | **60%** |
| attempt 9 (genuine review) | 58 | 29 | 50% |

**The bad review scores higher.** Both reports' resolving spans are overwhelmingly verdict-template
boilerplate (`"reviewed_head"`, `"prior_head"`, `"new_unresolved_items": []`) copied from
`VERDICT_TEMPLATE.json` **inside the packet**. Quote resolution measures copying the template, not
reading the subject.

**Candidate 2 — require every `path:line` citation to carry a quote verified *at that line*.**

| report | citations | resolvable | carrying a verified positional quote |
|---|---|---|---|
| attempt 7 | 12 | 12 | **0** |
| attempt 9 | 2 | 2 | **0** |

**Neither report quotes positionally at all**, so this rule rejects the genuine review too. Unusable
as a gate.

**Why no report-only check can work here.** The failure mode is a reviewer reading a **stale copy of
the same paths**. A stale tree is path-identical to a fresh one — that is what staleness *is* — so
nothing about the *shape* of a citation distinguishes them. Detection has to come from the packet
side: R1 (the bytes are in the packet) and R2 (outside reads forbidden) are what actually prevent
this. **The checker is a backstop for sloppiness, not a detector for staleness.** Rely on R1 and R2.

Note also that attempt 7's *line numbers were correct*, because they came from the diff's hunk headers
rather than from reading any file. "The numbers are right" proves nothing — and this checker's
`path:line` check should not be read as proving it either.

---

## The general lesson, for things that are not review packets

All four failures share one shape: **a check that did not run, reported as a check that passed.**

The same shape as a gate refusal that hid `OBSERVED_ARTIFACT_STALE` because the pipeline aborted
before that check executed, so twelve unexamined checks read as "two known problems". The same shape
as a validator asserting an exact-millisecond alignment that never held. And the same shape as a D026
predicate that "passed" on 2026-09-09 while matching a single literal substring — reword the defect
and it goes green with the contradiction intact.

**When something reports success, ask what it actually executed. When it reports failure, ask what it
skipped. Neither answer is in the summary line.**
