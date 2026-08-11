# Transport round 5 — draft edits NOT applied by this session (2026-08-11)

## Why these are not applied

`KICKOFF_TRANSPORT_REPAIR_R5.md` requires the F1 wording and the BA-3 narrowing to be
aligned in the preregistration drafts as well as in the block directory. Those two files
live under `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/`, and this session was
instructed at dispatch:

> A parallel Max session owns `pathscope_prover.py` in `WPI_PREREG_DRAFT_ROUND1` — do not
> touch that directory.

That is the `AGENTS.md` **PARALLEL AGENT SAFETY** case: those files carry uncommitted work
from other sessions, and a concurrent writer plus an uncommitted tree is exactly how prior
work gets destroyed. This session therefore **read** the target lines and did not write to
that directory. Nothing was staged, reverted, checked out, reset or stashed anywhere.

**Status: BA-3 is NOT fully closed, and F1's draft mirror is NOT yet aligned, until the
four edits below are applied.** They are stated here as exact old → new text so the Lead
(or whichever session owns that directory next) can apply them mechanically and a
re-auditor can verify them without re-deriving the wording.

Line numbers are as of the bytes read at 2026-08-11 and are advisory; the **anchor text**
is authoritative.

---

## Edit 1 — BA-3, main draft

**File:** `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md`
**Anchor:** §6, lines 688–691.

**OLD (exact):**

```text
a kind's grammar, and an `ssh` rc whose capture carries no marker **from that
operation's own family** are all not-evaluable. An `always` failure caused by an
earlier break on **its own branch** is not-evaluable rather than a new host FAIL,
and it names which of the two cases it is —
`cleanup_after_unestablished_prerequisite` or `cleanup_after_earlier_deviation`;
a failure on an unrelated branch does not demote it.
```

**NEW (exact):**

```text
a kind's grammar, and an `ssh` rc whose capture carries no marker **from that
operation's own family** are all not-evaluable. An `always` failure caused by an
earlier break on **its own branch** is not-evaluable rather than a new host FAIL;
a failure on an unrelated branch does not demote it. The reason recorded is the
**first** one that applies, so an operation whose own kind or status already
explains the inability reports that: a nonzero `scp` reports
`scp_transfer_did_not_complete` and an rc 3 reports `operation_reported_stop`,
whatever its prerequisites. Only an **rc-1** `always` failure reaches
prerequisite adjudication, and only there does the record name which of the two
prerequisite cases applies —
`cleanup_after_unestablished_prerequisite` or `cleanup_after_earlier_deviation`.
Every `always` operation still emits `TR_OP_PREREQ_STATE` with the resolved
class of each edge, so the prerequisite state is auditable from the record in
all cases, including the ones whose reason token is not a prerequisite token.
```

**Why:** `transport_runner.ps1` `Get-OpOutcomeClass` returns
`scp_transfer_did_not_complete` (line 1103) and `operation_reported_stop` (line 1108)
before the prerequisite branch (lines 1116–1120) is reachable. Codex's round-4 Fixture B
execution showed ops 09/10 and 11/12 doing exactly that with prerequisites genuinely
unestablished. The old sentence claims every broken-branch `always` failure names one of
the two tokens; the classifier does not, and should not.

---

## Edits 2 and 3 — BA-3, successor draft (two occurrences, keep byte-identical)

**File:** `WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md`
**Anchors:** §6 (line ~570) and Gap 10 (line ~678). Band A requires the two copies to stay
byte-semantically identical, so apply the **same** replacement to both.

**OLD (exact, the clause inside each occurrence):**

```text
and an `always` failure caused by an earlier broken sequence **on its own branch** is not-evaluable rather than a new host FAIL, and it names which case it is (`cleanup_after_unestablished_prerequisite` or `cleanup_after_earlier_deviation`).
```

**NEW (exact):**

```text
and an `always` failure caused by an earlier broken sequence **on its own branch** is not-evaluable rather than a new host FAIL, with the first applicable reason recorded — a nonzero scp reports `scp_transfer_did_not_complete` and an rc 3 reports `operation_reported_stop` whatever its prerequisites, and only an rc-1 `always` failure reaches prerequisite adjudication and names which case it is (`cleanup_after_unestablished_prerequisite` or `cleanup_after_earlier_deviation`); every `always` operation emits `TR_OP_PREREQ_STATE` with each edge's resolved class regardless.
```

**Verification after applying:** the two occurrences must remain identical —
`grep -c 'first applicable reason recorded'` returns 2, and diffing the two paragraphs
shows no difference.

---

## Edit 4 — BA-1, main draft

**File:** `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md`
**Anchor:** §4 derivation class 6, lines 357–360.

**OLD (exact):**

```text
   points `TMPDIR` at that proven directory, and removes it on every exit path with
   the removal's own status adjudicated rather than ignored.
```

**NEW (exact):**

```text
   points `TMPDIR` at that proven directory, and removes it on every exit path taken
   after the create returned 0, with the removal's own status adjudicated rather than
   ignored. The coverage is stated at that width deliberately: a **nonzero** `mkdir`
   result is not covered, because a nonzero status is no evidence that the object at
   that path is the one this run created, and removing an object the run cannot prove
   it created is the wrong answer. That arm STOPs and records whether an object is
   present (`object_after_failed_create=present|absent`) instead of claiming coverage.
```

**Why:** round-4 bytes armed the cleanup trap after a post-creation STOP branch and left
residue (`SCRIPT_RC=3 … RESIDUE_PRESENT=yes`). The code is repaired in round 5; this is
the mirrored prose. RED/GREEN: `SELF_QA_TRANSPORT.md` §R5-1.

---

## Also to check in that directory when it is next owned (F1 alignment)

The F1 status wording — **"inner child closed; outer SSH account-shell boundary open"** —
must replace any draft text that says F1 is closed on the composition, that the `BASH_ENV`
residual is unreachable, or that the remote login/account shell "cannot select or influence
what runs". This session could not sweep those files for such text without reading and
potentially editing them, so the sweep is listed rather than performed. Suggested check:

```text
grep -n -i "unreachable\|closed on the composition\|cannot select or influence\|login shell" \
  WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md \
  WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md
```

Any hit that asserts closure or unreachability for F1 is in scope for the same correction
already applied to `TRANSPORT_R4_REPORT_2026-08-11.md`, `STATUS_TRANSPORT.md`,
`SELF_QA_TRANSPORT.md`, `transport_runner.ps1` and all five delivered shell scripts.

This file grants no host, freeze, allocation, execution, dispatch, or Git authority.
