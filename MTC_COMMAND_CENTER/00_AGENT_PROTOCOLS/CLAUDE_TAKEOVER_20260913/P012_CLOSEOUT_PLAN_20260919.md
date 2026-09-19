# WP-P0-12 — what is left to close the package (written Sat 2026-09-19 09:5x UTC+3 by the P0 Claude Lead, session 7) — **SUPERSEDED 13:53: Layer A CLOSED, see `P012_CLOSEOUT_RECORD_20260919.md`** (T1-T7 done; T8 `CT13-MERGE` still the owner's call)

Plain English for the owner. Times UTC+3. Sources: `HANDOFF_20260919_SESSION7.md`, `OWNER_DECISIONS_PENDING.md`, CT13 `DECISIONS.md` (17 `OD-…-P012-…` rows), `P012_ACCEPTANCE_AMENDMENT_20260913.md`, the lane records in `OPUS_QUEUE_20260916/` and the capture/intake record folders in this run root. Verified this morning: the CT13 records branch is 194 commits ahead of `master` and contains every P0-12 decision; `master` holds none of them yet.

## 1. What "done" means (two layers — you ruled this on 2026-09-13)
- **Layer A — research/engineering scope** (`OD-20260913-P012-SCOPE-1`): the funding/position evidence capture tool, the intake adapter (D-1..D-6), the validator chain, and their reviews. Label when finished: *"P0-12 research/engineering scope complete; production admission pending."*
- **Layer B — production admission** (explicitly OUT of the current closure): OPEN-01..OPEN-10, the qualified-human review, KVM2 gate order, MERGE-AUTH for money-exposed release. Nothing in this plan touches Layer B except to name it.

## 2. Where each piece stands today
| Piece | Bytes | Exact-Opus | Gemini | Sol (2nd flagship) | Merged? |
|---|---|---|---|---|---|
| Capture tool (`capture_own_account_evidence.py`) | branch `feature/p012-path1-capture-20260914` @ `af921d75` (worktree `C:/tmp/P1CAP_20260914`) | PASS-WITH-NITS (7 NITs) | PASS | **not yet** (Codex reset tonight 18:47) | no |
| Intake adapter, accepting half (D-1..D-6) | branch `feature/p012-funding-intake-adapter-20260915` @ `a871e429` (worktree `C:/tmp/P012_INTAKE_20260915`) | PASS-WITH-NITS ×2 (NITs 1-9 + NIT-A) | PASS | **not yet** | no |
| Real capture r1 (2026-09-15) | evidence only | — | — | — | refused D-4 by design (no oracle read existed) |
| Real capture r2 (2026-09-17, your BTC trade 10:28-13:23) | evidence only, signed by you, tool-verified | — | — | — | first real D-1..D-6 candidate, but D-4 hand-filled → NON-accepting by design |
| Oracle capture (O-1 auto-fill of D-4) | not built | — | — | — | you ruled `O-1 wait` (2026-09-18) |
| Validator / gate chain (re-seals #36-#39) | ratified 2026-09-14 on CT13 | (older T0 rounds) | — | — | records on CT13, not on master |
| CT13 records branch | `feature/claude-takeover-20260913` @ `881702d8` (+ today's wave) | — | — | — | not merged to master |

## 3. Smallest tasks to close Layer A, in order (who can do it; what blocks it)
| # | Task | Who | Blocked by |
|---|---|---|---|
| T1 | Sol read of the capture tool `af921d75` (documentary, one Codex lane) | AI (Lead) | Codex Plus weekly reset **tonight 18:47** |
| T2 | Sol read of the intake half `a871e429` | AI | same reset; one lane at a time |
| T3 | Apply the DRAFTED capture-tool NIT slice (7 NITs, `P1CAP_NIT_SLICE_PREP_20260918/`), RED/GREEN on the PINNED Python 3.12, Gemini delta, exact-Opus re-read, Sol on the final bytes | AI | nothing (after T1 so Sol reads the base first — or skip T1 and Sol-read the final bytes only: the Lead's call, saves one Sol lane) |
| T4 | Build the intake NIT slice (NITs 1-9, NIT-A) **with `D6-START B`** (window start exclusive — already ruled), same roster as T3 | AI | nothing (after T2, same note) |
| T5 | Open + merge the capture-tool PR to `master` (PR-only, Bridge suite green) | AI mechanics | **your word**: the 2026-09-13 amendment's `MERGE-AUTH` row says a P0-12 merge needs an explicit owner release act (one line: `P012-MERGE capture go`) |
| T6 | Open + merge the intake-adapter PR | AI mechanics | **your word** (`P012-MERGE intake go`) |
| T7 | Write the Layer-A close-out record (label above; roster table; hashes) and the register row; push CT13 | AI | T5, T6 |
| T8 | Records PR: CT13 branch → `master` (194 commits of records; T2/T3 class; PR-only serial merge) | AI mechanics | **your decision**: merge the whole takeover branch now, or keep it open until the P0 campaign ends (one line: `CT13-MERGE now|later`) |

## 4. Beyond Layer A — things only you can do, or that need a decision (none urgent today)
- **`O-1 build`** (oracle-capture tool + automatic D-4 fill). Without it every real capture stays NON-accepting (r2 shape). Your standing answer is `wait`; say `O-1 build` when you want it. AI builds it; same review roster.
- **A new real capture (r3) with tool-filled D-4** after O-1: you open a small mainnet BTC perp position spanning at least two funding hours (e.g. 10:00→13:00), then sign the ownership message; the AI runs the capture and intake. **Live Hyperliquid action = yours only.** (Testnet cannot produce real funding evidence for this package.)
- **Qualified/experienced human review before any money-exposed release** (Layer B `SPECIALIST` row): you named yourself as self-attestation; the act itself is yours.
- **KVM2 gate order** (secret provisioning → DISARMED start → rollback proofs → ARM): each step is a separate sentence from you; Bridge Toolkit buttons exist for the read-only checks.
- **Registry-key hygiene**: `HL_API_WALLET_KEY` sits in `HKCU\Environment`, readable by any process. Recommendation stands: move it; your machine, your call.
- **External research still open** (not blocking Layer A): Hyperliquid's funding cadence / fee-tier documentation for the real account is "not established in the sources used" (`P012_RISK_PACKET_OWNER_PRESENTATION_DRAFT.md`). Needs venue docs + an authenticated own-account read (yours). Suggested route: CodeBuddy hy4-preview or Cline Pass documentary lane, then you confirm on the venue UI.
- **Route limits that pace the AI work**: Codex Plus weekly (Sol) resets tonight; Claude Pro 5-hour windows for exact-Opus reads; Gemini serialised; Grok weekly (Fri).

## 5. Open owner one-liners right now
- `P26-EVID A|B` (P0-26, not P0-12; default B).
- Nothing else is open. New ones proposed above: `P012-MERGE capture go` / `P012-MERGE intake go` (when T3/T4 rosters are complete), `CT13-MERGE now|later`, `O-1 build` (whenever you want it).
