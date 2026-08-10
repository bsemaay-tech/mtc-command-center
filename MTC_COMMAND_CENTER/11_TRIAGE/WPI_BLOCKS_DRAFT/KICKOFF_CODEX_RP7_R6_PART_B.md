# KICKOFF — RP7 round-6 review: rows 20–24, the evidence contract, and the leaf-binding repair

Fresh `gpt-5.6-sol` session, effort xhigh. Report only; edit nothing except your output
file. Working dir `C:\LAB\Tradingview_LAB_CLEAN`. No host contact, no network, no commit.

`RP7-WPI-RO.sh` is a read-only environment preflight block for a maintenance job: it looks
at an already-provisioned host, records what it finds, and prints one machine-readable line
per checked row. It changes nothing. Confirm **each branch reports an honest result** — an
accepting line only when the observation established it, an inability to observe reported as
STOP rather than as a completed negative observation, and no printed wording stronger than
the code supports.

**Scope: rows 20–24, the evidence/QA contract, and the leaf-binding repair.** Rows 10–19 and
the round-5 repairs are out of scope for this run and are covered only by carried fences.
Stay inside the band — keeping each run narrow is deliberate and has been necessary.

## Subject

`WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh` — **round-6 bytes**, SHA-256
`6586698c707601c70a3e99903dc789ee2ee71fd2bae1bc1763adc52f72a40709`, 88460 B. Re-derive hash,
byte count, CR bytes and `bash -n` first. Round-5 predecessor for before/after work:
`393a16ce264b467bec180a2106390e6dcee4dc2605fd019871270fda11d3b0ee`, 77179 B, commit
`1143a9ff` — materialise it with `git cat-file blob`, never `git checkout`.

## What round 6 claims to close — your own four findings

From `RP7_CODEX_T0_AUDIT_R5_PART_B_2026-08-10.md` (BLOCK: 4):

1. A malformed listener record was silently normalised into a complete PASS.
2. Truncated or invented status-parser result records became semantic FAILs instead of STOPs.
3. Invalid HTTP status tokens were reported as completed endpoint deviations.
4. The published evidence command masked fence failures and was unbounded.

For each: confirm the repair, and confirm its **no-weakening control** — column-padded `ss`
output must still parse, a real wildcard listener must still be a host-state FAIL, `500` must
still be FAIL, `401` must still be STOP, and the four result records the status child really
emits must keep their round-5 dispositions.

For finding 4 specifically: **run the published command exactly as written** and confirm both
that it passes on good fences and that it **fails when a fence fails**. The repair claims each
fence now runs under a 900 s bound with a 2700 s aggregate, and that a fence killed at its
bound is reported distinctly from an assertion failure. Test the failure path, not only the
happy path.

## The leaf-binding repair, and two disclosed residuals

Round 6 replaced name-based leaf writes with `wpi_open_leaf`: the same `noclobber` create-once
test performed as `exec {fd}>`, so the descriptor returned **is** the object the open created,
and writes go through that descriptor. Assess whether that genuinely binds the write path.

The implementer disclosed two residuals rather than claiming closure. Judge whether the
disclosure is accurate and whether the narrowed claim is honest:

- **Residual 1:** `curl --output <path>` receives a name, not a descriptor, so
  `ro.status.body` is create-once allocated and then re-opened by curl — the same route, open,
  for one leaf.
- **Residual 2:** readers re-open the leaf path after the child has run; what the block
  establishes about that content is only what its record grammar establishes.

## Rows 20–24 and the draft

Conformance at the exact FAIL/STOP wording in
`WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` §8.2. Round 6 made **four draft
edits** (rows 20, 21, 22 and §10.1), including a new `bytes=<n>` field on row 22. Verify the
block and the draft now say the same thing, and that no edit widened what the block is
permitted to claim.

## Method

Prefer executed tests over code reading. Keep each test self-contained under a `mktemp -d`
tree you remove. Record the exact command, its rc and observed output for everything claimed.

## Known freeze-gate items — not findings

`WPI_FIXED_TRUSTED_PYTHON`, `WPI_FIXED_ATTESTED_MOUNT_PROJECTION_SHA256`,
`WPI_FIXED_EVIDENCE_ROOT` and the accepting `wpi_validate_inputs` branch are `<PIN-AT-FREEZE>`,
so no whole-block accepting run can exist before freeze. §8.2 rows 1–9 are implemented by no
block and are a separate owner decision.

## Patterns

Check against `DESIGN_DEFECT_PATTERNS_2026-08-10.md` — **thirteen** patterns; 11, 12 and 13
were added last night. Findings 1 and 2 were both pattern-13 shaped, so pay particular
attention to whether every admitted record now reaches exactly one terminal disposition.

## Output

Write **only** `WPI_BLOCKS_DRAFT/RP7_CODEX_T0_AUDIT_R6_PART_B_2026-08-11.md`: verdict for your
band first (`PASS` / `PASS-WITH-NITS` / `REQUEST_CHANGES` / `BLOCK: <n>`), then a row table
with evidence, then findings most severe first with command, rc and output. State plainly
which bands were out of scope.
