# GATE A — INDEPENDENT AUDIT OF THE LEAD'S FINDINGS (2026-08-02)

Auditor: **`gpt-5.6-sol`, effort `xhigh`**, fresh session, read-only sandbox.
Target: `9b3d27c1` on `feature/donchian-crypto-ladder`.
Verdict: **REQUEST_CHANGES.**

## Why this audit was commissioned

The Lead's Gate A finding kills the WP-I candidate artifact and forces a rebuild. That is a
consequential call to hand the owner, so the audit prompt **published the Lead's own reasoning and
asked the auditor to falsify it** — the programme's own lesson 3, applied deliberately.

It worked. The auditor refuted the Lead's central root-cause attribution.

## Findings, and what the Lead did about each

| Claim | Auditor | Lead's action |
|---|---|---|
| 1 — CRLF is in the committed blobs, present on `origin/master` | **REFUTED** | Already self-corrected at `63f9413b`, before the verdict landed, by an independent size/`od` measurement. Both arrived at the same corrected cause: `package.sh:73` bare `git archive` under `core.autocrlf=true`. |
| 2 — the venv seal assertion can never pass on any venv | **REFUTED as written; CONFIRMED for this installer** | Accepted and corrected. Reproduced on the host: `--copies` removes the three `bin/*` symlinks but `lib64 -> lib` remains, so the assertion still fires; and `install.sh:290` never passes `--copies`. Universal phrasing withdrawn; operational conclusion stands. |
| 3 — the recorded floor was measured on the wrong Python | **CONFIRMED** for the recorded baseline; mechanism **UNVERIFIED** by the auditor (it could not run 3.12) | Accepted. The mechanism *was* verified empirically by the Lead on the staging host, where the tests genuinely fail under 3.12.3. Also accepted: "never measured" is a statement about the programme's *recorded* baseline, not proof no undocumented private 3.12 run ever happened. |
| 4 — the service needs credentials Gate A forbids | **CONFIRMED**, with a qualification | Accepted and corrected. The fail-closed DISARMED write is **not** unconditional: `app.py:109` preserves an existing `KILLED` state. Correct behaviour, but the Lead's wording implied otherwise. |
| 5 — the ledger failure is defect 1 | **REFUTED as stated** | Same root-cause inversion as claim 1; corrected. The substance survives and was then *proved* rather than inferred: normalising `ledger_schema.json` moves it 903 → 867 bytes and `b6580e31…` → `f4cdece5…`, the exact value the ledger records, and the test passes. |

## The defect the Lead under-framed

> *"The most important missed defect is build reproducibility: the same `RELEASE_SHA` can produce
> different payload bytes and manifest hashes depending on archive conversion settings."*

Correct, and now recorded as **defect 5** in `GATE_A_RECON_DEFECT_LIST_2026-08-02.md`. The Lead had
treated CRLF as the disease; it is a symptom. If a commit does not determine the payload bytes, then
`--release-sha` + `--manifest-sha256` do not actually bind a payload to a commit, and the artifact
model the programme rests on is unsound. The repair must pin export behaviour and ideally assert it,
so a misconfigured builder fails loudly rather than shipping a subtly different payload.

The auditor also caught a scope trap: an `eol=lf` rule covering only
`IBKR_PAPER_BRIDGE/deploy/linux/**` would fix the installer but leave the ledger failing, because
`ledger_schema.json` lives under `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/`.

## What the auditor endorsed

- Stopping the official gate at A-2 was correct — the runbook says stop at the first FAIL.
- Running the further work as separately labelled reconnaissance on a normalised **copy** is
  procedurally sound and does not contaminate the official evidence. The commit chronology keeps the
  A-2 result before the reconnaissance report.
- Not repairing the artifact during the gate was correct, **not** a missed obligation.
- At the audited target, the three Gate A commits changed only report documents — no source, no
  artifact.

## Limits of this audit, stated by the auditor

- No test suite was executed; all checks were read-only except a small Python 3.14 `gc` probe. Under
  the AGENTS.md four-auditor rule this audit is therefore **supplemental for suite-dependent claims**;
  it is authoritative on the repository-inspection claims, which is what it was commissioned for.
- It could not verify from the repository that the pristine host payload was left untouched — that
  remains a host-side claim.
- The branch advanced during the audit to `ca98ce93` (documentation corrections only). **Those
  post-target commits were not audited and need a delta audit.** No deployment source or artifact
  rebuild occurred in them.

## Consequence

Gate A's A-2 **FAIL stands**, unaffected by any of the corrections. The artifact must still be
rebuilt. What changed is the repair: from a repo-wide content renormalisation (wrong, invasive) to
pinning deterministic export behaviour (correct, small) plus the `common.sh` type-filter fix.

Acceptance of the eventual *repair* still requires the canonical floor — both flagship auditors
accepting — and this audit does not pre-empt it.
