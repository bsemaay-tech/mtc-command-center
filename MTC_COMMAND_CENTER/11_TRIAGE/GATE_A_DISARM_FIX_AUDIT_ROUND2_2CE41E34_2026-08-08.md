# Gate 5 audit round 2 — A-4 repair `2ce41e34` (2026-08-08)

## VERDICT: **`2ce41e34` IS ACCEPTED under D025.** Repair candidate accepted; Gate A not rerun.

Companion to round 1: `GATE_A_DISARM_FIX_AUDIT_ROUND1_ED3D0534_2026-08-08.md` (the parent
`ed3d0534` was **NOT ACCEPTED**, one Lead-reproduced required finding). Round 2 is the agreed minimum
repair, and both flagships now accept it. **This accepts the repair candidate only — not the host Gate A
result. Gate A has not rerun; A-4 remains historically failed until the new artifact passes on staging.**

| D025 slot | Auditor | Verdict | Suite executed |
|---|---|---|---|
| Flagship 1 | `gpt-5.6-sol` xhigh | **PASS** — 0 required | yes, full `1360 passed, 1 warning in 116.05s` |
| Flagship 2 | `claude-opus-5` xhigh | **PASS-WITH-NITS** — 0 required, nits only | yes, full `1360 passed, 1 warning in 145.53s` |
| Auditor 4 | `GLM-5.2` (Z.AI Coding Plan) | **PASS** — 0 required | yes, full `1360 passed, 1 warning` |
| Auditor 3 | `cline-pass/deepseek-v4-flash` via Cline | **BLOCK** — non-execution | no — CLI returned `No access to ClinePass subscription models yet.` |

D025 rule 3 requires **both** flagships accepting plus no unresolved reproduced required finding.
Both flagships accept; the GLM auditor also accepts and executed the suite. The DeepSeek slot could not
execute (subscription access not yet available) and returned BLOCK per D025 rule 1 — a non-execution
BLOCK that is supplemental/no detection coverage and **does not veto acceptance** when both flagships are
accepting and no required finding is reproduced. **Acceptance stands.**

Auditor worktrees (all detached clean, audited at `2ce41e34`):

| Auditor | Worktree | Status at end |
|---|---|---|
| Codex `gpt-5.6-sol` xhigh | `C:\GAAUD_DISARM_CDX_R2` | clean — edited nothing |
| Claude `claude-opus-5` xhigh | `C:\GAAUD_DISARM_CLA_R2` | clean — edited nothing |
| GLM-5.2 | `C:\GAAUD_DISARM_GLM_R2` | clean — edited nothing |
| DeepSeek V4 Flash (Cline) | `C:\GAAUD_DISARM_DS_R2` | clean — no execution |

---

## 0. The candidate and the repair

- **Repair parent:** `ed3d053432fb496123ac43bcb7d40cfb64edbb8b` (round 1, NOT ACCEPTED).
- **Accepted candidate:** `2ce41e34bceb599d80af24c5c33d835820ec321b`.
- **Branch / worktree:** `codex/gate-a-disarmed-start-mode`, `C:\GADISARM`.
- **Commit message:** `fix(deploy): reject start-mode env override`.
- **Diff:** exactly **4 files, 59 insertions** — verify guard, behavior test, README, env template. No
  fifth file; no product-runtime file touched.

The round-1 required finding was that `EnvironmentFile=` overrides `Environment=` in systemd, so the
unit's `MTC_BRIDGE_START_MODE=credential_free_disarmed` pin was defeatable by a root-written
`MTC_BRIDGE_START_MODE=` in `/etc/mtc-bridge/mtc-bridge.env`, and `verify.sh` rejected only `HL_LIVE_ACK=`
so it reported PASS while the override won. Round 2 closes that channel: `verify.sh` now rejects any
`MTC_BRIDGE_START_MODE=` definition in `${MTC_ENV_FILE}`, a regression test proves the rejection, and the
README/env template document that the variable is set by the unit and must not be defined in the env file.

---

## 1. Lead evidence at `2ce41e34`

- **Targeted test (the new behavior test):** `1 passed in 0.81s`.
- **Deployment test file:** `48 passed in 12.57s`.
- **Full suite:** `1360 passed, 1 warning in 122.86s` — the Windows floor moves from `1359` to `1360`
  because exactly one new test function was added.

### D026 falsification — Lead-run, both mutations independently RED

The new behavior test was falsified two ways before being accepted as evidence:

- **RED-A (require-export mutation):** the `verify.sh` env-file guard was mutated to require an
  `export` prefix, so a bare `MTC_BRIDGE_START_MODE=credentialed` assignment was no longer rejected.
  Expected `FAIL_BRANCH`; **actual `PASS_BRANCH`** — the test correctly failed on the broken guard.
- **RED-B (invert branches):** the guard's accept/reject branches were inverted. Same mismatch —
  expected `FAIL_BRANCH`, actual `PASS_BRANCH`.
- **GREEN:** both mutations restored, the real guard in place, the test passes.

Both mutations went RED against the real source; the test discriminates the defect. (Round 1's RED-A was
a `require-export` shape mismatch; round 2's mutation matched the documented `FAIL_BRANCH`/`PASS_BRANCH`
wording and reproduced the same conclusion independently.)

## 2. Artifact — rebuilt and verified at `2ce41e34`

- **Path:** `C:\WPI_ARTIFACTS\2ce41e34bceb599d80af24c5c33d835820ec321b`.
- **Manifest SHA-256:** `EDB0FD34E3D976B872868CC3DFBF745CBC4B08F6C4C5D21B8D6CDA47A3E20D26`.
- **Size:** 7,059 manifest entries, 7,060 files, 1,033,362,481 bytes.
- **Deploy scripts:** **zero CR bytes in all five `deploy/linux/*.sh`**.
- **Property counts in the built payload:** first-start pin **1**, steady pin **0**, env guard **1**,
  behavioral test **1** — all four expected, none missing, none doubled.

## 3. Auditor evidence

### Codex flagship — `gpt-5.6-sol` xhigh — PASS

- Targeted test `1 passed in 1.09s`; deployment file `48 passed in 12.50s`; full suite
  `1360 passed, 1 warning in 116.05s`.
- Both D026 mutations independently RED; **GREEN with the fix in place**.
- Artifact and bash syntax verified (the env-file guard parses and rejects as intended).
- Worktree `C:\GAAUD_DISARM_CDX_R2` clean at end.
- **Zero required findings.**

### Claude flagship — `claude-opus-5` xhigh — PASS-WITH-NITS

- Targeted test `1 passed in 1.03s`; deployment file `48 passed in 12.42s`; full suite
  `1360 passed, 1 warning in 145.53s`.
- **Required two plus four extra mutants all killed** — the falsification was checked harder than the
  minimum and still held.
- Artifact and bash verified.
- Worktree `C:\GAAUD_DISARM_CLA_R2` clean at end.
- **Zero required findings.** Nits are optional and queued, not repaired here (§4).

### GLM-5.2 (auditor 4) — PASS

- Targeted `1 passed`; deployment `48 passed`; full `1360 passed, 1 warning`.
- Both D026 mutations independently RED.
- Artifact verified.
- Worktree `C:\GAAUD_DISARM_GLM_R2` clean at end.
- **Zero required findings.** GLM executed the suite this round (unlike its round-1 non-execution event),
  so its accepting verdict carries detection coverage, not a read-only opinion.

### DeepSeek V4 Flash (auditor 3, Cline) — non-execution BLOCK

- CLI returned `No access to ClinePass subscription models yet.` **No audit opinion/findings and no test
  execution.** Worktree `C:\GAAUD_DISARM_DS_R2` remained clean.
- Per D025 rule 1 this is a non-execution BLOCK. Per D025 rule 3, an unexecuted slot is supplemental/no
  detection coverage and does not veto acceptance: both flagships are accepting and no reproduced required
  finding remains. Recorded honestly, not silently dropped.

## 4. Claude optional nits — queued, not repaired here

Queued for a future scoped follow-up; explicitly **not** repaired in this record (no product edits).

1. The verifier does not inspect **systemd drop-ins** (`*.conf` under the unit's `*.service.d/`), only the
   env file and the rendered unit. A drop-in is a third override channel. Future scoped follow-up.
2. The **steady profile carries no start-mode pin** (correctly — steady is the future credentialed profile),
   so the property is currently first-start only. Address at the steady profile's future gate, not here.
3. Remaining cosmetic / over-strict / test-structure notes are non-blocking and need not be expanded in
   every record.

## 5. Acceptance and what does NOT follow

- **`2ce41e34` is ACCEPTED under D025** as the repair candidate. `ebada020` remains the last
  accepted *Gate A* candidate; `2ce41e34` supersedes `ed3d0534` as the repair to attempt on staging.
- **Gate A has not rerun.** A-4 is still historically failed. Acceptance of the candidate is not a Gate A
  PASS; the new artifact must pass on staging (A-0 through A-9, first-FAIL rule) under Addendum D.
- **No transfer, install, teardown, or Gate A action is authorized by this acceptance.** Those await
  explicit staging authorization from Barış.
- Repair round 2 of a maximum 3 was the accepting round.
- **No product code was changed by this record** — it is acceptance evidence only. The 4-file repair was
  authorized and built in its own session.
