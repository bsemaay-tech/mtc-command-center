# KICKOFF — Audit-2 packet 9/10/11 skeletons (Codex free lane)

Tier T2 documentation drafting. Codex `-Account free` (**gpt-5.5** — confirm your actual model
from the session header and state it in your report). No git mutation; the Lead commits.

## Mission

`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md`
scoped packets 9, 10, 11. Fallback-backlog item 2 of the night plan: **draft packet skeletons,
but ONLY for whichever packets that scoping document says can honestly carry
`<PENDING-STAGE-1>` markers.** If the scoping says a packet cannot honestly be skeletonized yet
(e.g. it depends on an owner decision such as P10-10 or P11-08, or on a run that has not
happened), do NOT draft it — record why in your report instead.

## Rules

- Read the scoping document first and follow its per-component conclusions exactly. Where it
  names five components with no producing step, the skeleton must say so explicitly rather than
  imply the content is coming.
- Every unfilled slot must be an explicit `<PENDING-STAGE-1>` (or more specific) marker under a
  heading that says PENDING — never under prose that reads as resolved (binding authoring rule).
- Any byte size, SHA, count, or absolute you write must be re-derived from disk now, or labelled
  `External evidence:` with the source file cited.
- Owner-class content (ledger ratification P11-08, mandated-suite decision P10-10) gets an
  explicit `OWNER-DECISION-REQUIRED` marker, never a drafted answer.

## Files you own (disjoint — nothing else)

- New skeleton files under `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/` named
  `AUDIT2_PACKET<n>_SKELETON_2026-08-12.md` for each packet you draft.
- Your report: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PACKET_SKELETONS_CODEXFREE_2026-08-12.md` —
  what you drafted, what you declined to draft and why, model/effort from your session header.
