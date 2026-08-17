# KICKOFF — RUNID minting: are the proposed identifiers actually accepted, and is the refusal demonstration real?

Fresh `gpt-5.6-sol` session, effort high. Reading, reasoning and small text-level checks
only. Do not modify any block, wrapper, prover or preregistration file. Working dir
`C:\LAB\Tradingview_LAB_CLEAN`. No host contact, no network, no commit.

## Why

Before anything runs, Stage 1 must mint one-use run identifiers and commit them. A RUNID
that the run's own component-safety predicate would refuse is a stop-the-world problem
discovered at the worst moment — after the preregistration is committed and frozen. The
skeleton also promises a demonstration of the predicate's *refusal* set, and a gestural
demonstration is worse than none: it creates the appearance of a check.

## Inputs (relative to `MTC_COMMAND_CENTER\11_TRIAGE\`)

1. `WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_SKELETON_2026-08-10.md` — the minting rules
   and the promised demonstration.
2. `WPI_PREREG_DRAFT_ROUND1/SKELETON_REVIEW_CODEX_2026-08-10.md` — gap 4 raised this;
   build on it rather than repeating it.
3. `rp0_require_safe_component` — **locate the authoritative definition yourself** (RP0-LIB;
   the wrappers `run_p0.sh` / `run_ro.sh` source it). Record the file path, byte count and
   SHA-256 of the source you read. If you cannot locate it, say so plainly and stop — do not
   reason from a copy of unknown provenance.
4. `WPI_BLOCKS_DRAFT/RP6-P0.sh` and `RP7-WPI-RO.sh` — both consume RUNID-derived paths;
   `RP6-P0.sh` additionally treats `RUNID` and `EV_STAGE_ID` as opaque unpinned values
   (recorded in `PATHSCOPE_LEAD_RERUN_2026-08-10.md`).
5. `WPI_BLOCKS_DRAFT/TRANSPORT_PLAN.tsv` and `transport_runner.ps1` — where RUNIDs travel.

## Questions

1. **Derive the accepted character set and shape** from the predicate's actual code, not
   from prose describing it. Quote the code. State exactly what is accepted and what is
   refused, including empty input, leading `-`, `.` and `..`, path separators, whitespace,
   control characters, non-ASCII, glob metacharacters, and length limits if any.
2. **Test the proposed RUNIDs against that.** For each identifier form the skeleton proposes
   or implies, say whether it is accepted, and show the reasoning against the quoted code. A
   form that is accepted only by luck — e.g. because a timestamp happens to avoid a
   metacharacter — should be called out as fragile.
3. **Assess the refusal demonstration.** Is each refusal case specific and executable, or is
   it a list of adjectives? Propose the minimal set of cases that would actually establish
   the predicate refuses what it claims to refuse — one case per refusal class, each with the
   exact input and the expected refusal.
4. **Follow the RUNID through the composition.** From minting, through the wrapper, into
   `EV_DIR`/`EV_LOG`, into the transport plan's arguments, into the remote scripts. At every
   boundary: is it re-validated, or trusted because an earlier stage validated it? Name any
   boundary where a value crosses without re-validation, and say whether that matters.
5. **One-use discipline.** What in the design prevents a RUNID being reused, and what would
   happen if one were? Is reuse detectable after the fact from the evidence alone?

## Output

Write **only** `WPI_PREREG_DRAFT_ROUND1/RUNID_MINTING_REVIEW_CODEX_2026-08-11.md`: the
located predicate's identity, the derived accept/refuse specification quoted from code, the
verdict on each proposed identifier, the proposed minimal refusal-demonstration set, the
boundary-crossing table, and the one-use assessment. End with a short list of anything Stage 1
must change before minting.
