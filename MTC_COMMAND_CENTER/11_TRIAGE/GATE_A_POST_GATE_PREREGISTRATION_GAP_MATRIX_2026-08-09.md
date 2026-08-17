# Gate A — Post-Gate Preregistration & Gap Matrix (WP-L Phase 2 → WP-I staging → Audit 2 → WP-A)

> # ⛔ SUPERSEDING PROVENANCE CORRECTION — 2026-08-09
>
> **Applied by:** `claude-opus-5` (xhigh), documentation-only repair unit.
> **Full evidence:** `GATE_A_POST_GATE_PROVENANCE_REPAIR_2026-08-09.md` (same directory).
> **Where this block and the original text conflict, this block governs.**
>
> **The defect.** This matrix was originally authored by reading **product** files (tests,
> `verify.sh`, `bridge/app.py`, `tools/wal_state_bundle.py`, `deploy/linux/README.md`) out of the
> **documentation/governance checkout**, and attributing those readings to the **frozen, deployed
> product candidate**. The two refs are **divergent** — neither is an ancestor of the other:
>
> ```
> documentation / governance HEAD : 851d2aa5   (roadmap, authority, audit roster, handoffs, evidence index)
> frozen / deployed candidate     : 2ce41e34bceb599d80af24c5c33d835820ec321b   (product, deploy, runtime, tests, tools)
> merge base                      : 4d2228cf8985ce755c398cceff23f777a99d5404
> git merge-base --is-ancestor 2ce41e34… 851d2aa5   → exit 1
> git merge-base --is-ancestor 851d2aa5 2ce41e34…   → exit 1
> git diff --stat 2ce41e34… 851d2aa5 -- IBKR_PAPER_BRIDGE
>     → 33 files changed, 624 insertions(+), 14372 deletions(-)
> ```
>
> **Binding source-of-truth split.**
>
> | Fact class | Authoritative source |
> |---|---|
> | Roadmap, sequencing, authority envelope, audit roster (D025/D026), handoffs, evidence index | documentation branch `851d2aa5` |
> | Gate-A A0–A9 evidence, installed-host inventory | immutable captured evidence, explicitly tied to `2ce41e34…321b` |
> | **Product, deploy, runtime, start-mode, test symbols, tool behaviour** | **`git show` / `git grep` at `2ce41e34…321b`** — or installed-host / Gate-A evidence explicitly tied to it |
>
> **Never infer candidate source behaviour from the documentation checkout when the blobs differ.**
> Where blobs differ, product citations must be written commit-qualified as
> `2ce41e34…321b:<path>:<line>`. A bare `<path>:<line>` in this document is doc-derived unless
> corrected below.
>
> **Blob status of the files this matrix relies on** (`git rev-parse <ref>:<path>`, under
> `IBKR_PAPER_BRIDGE/`):
>
> | Path | Candidate `2ce41e34…321b` | Documentation `851d2aa5` | Effect |
> |---|---|---|---|
> | `requirements.lock` | `47f53fa227bf0f18b9bf9bd77e060d8856961728` | *same* | ref-invariant |
> | `deploy/linux/verify_lock.py` | `8ccd6f329154422a85b8e7663e6a079dbd47b4fd` | *same* | ref-invariant |
> | `deploy/linux/rollback.sh` | `4b36674dcb1baa7c3b119cac98f8e6017b1f1566` | *same* | ref-invariant |
> | `deploy/linux/COMMANDS.md` | `3deeefc8da2984d5220482f065e569b74874847a` | *same* | ref-invariant |
> | `deploy/linux/verify.sh` | `5cfefd709202ff504ae7b7fc3504b8c0b00900b6` | `bce1f0e23e63f9a8d168c751aec99ac84d1334c7` | **candidate only** |
> | `deploy/linux/systemd/mtc-bridge-first-start.service.template` | `c18232549d96aa200d8c7f796e64de743288940c` | `b175ced7f36df52ad2e55532264f36f49fdc8281` | **candidate only** |
> | `tools/wal_state_bundle.py` | `26c077e650ab88ba2086efa3a80790769bc055b1` | `aaa2918229a1367ebf1fb6a458a4e65673dc180e` | **candidate only** |
> | `bridge/app.py` | `572c4178fe804da17601eefd898027e9261492e6` | `6d0abc6351a0d20aef324fb00b936c0f189d036f` | **candidate only** |
> | `deploy/linux/README.md`, `env/mtc-bridge.env.template`, `lib/common.sh`, and the cited tests | differ | differ | **candidate only** |
> | `deploy/linux/SECURITY_BASELINE.md` | **ABSENT** | `8db2e6dd7e782c96f585f6672c4489c4ce5c1488` | governance artifact, **not** candidate payload |
> | `tests/test_credential_free_disarmed.py` | `ce0ae7c24f795dc8e5d56bf7cca82e1a75351402` | **ABSENT** | **candidate only** |
>
> **What this corrects in the text below.**
>
> 1. **All 11 target test symbols EXIST at the frozen candidate.** The claim that
>    `test_kill_restart_after_request_commit_keeps_killed_and_resumes_once` is absent/stale is
>    **FALSE** for the deployed candidate — it is at
>    `2ce41e34…321b:IBKR_PAPER_BRIDGE/tests/test_partial_fill_protection.py:2765`. It is absent only
>    from the divergent documentation checkout. **Gap G4 is WITHDRAWN.** The proposed WP0 deletion is
>    **CANCELLED**; `WP0_SCOPE_BASELINE_RECORD_2026-07-31.md` lines 308 and 364 are **correct as
>    written** and must not be edited. No replacement symbol is needed.
> 2. **Every `verify.sh`, `README.md`, and test line number originally in this document is a
>    documentation-checkout offset.** Corrected candidate anchors are given inline below and in §4a.
> 3. **Credential-free DISARMED start mode is a candidate-only protection that this matrix
>    originally omitted entirely** (it does not exist in the documentation-branch deploy tree —
>    `git grep MTC_BRIDGE_START_MODE 851d2aa5 -- IBKR_PAPER_BRIDGE/deploy/linux` returns nothing).
>    See the new §0.6 and B5.
> 4. **`SECURITY_BASELINE.md` is not candidate payload** and is reclassified wherever it was cited as
>    a canonical product source (A3, C5).
> 5. **The C5 egress premise is corrected**: at the candidate, the deployed start mode constructs
>    **no broker at all**, so no runtime egress can be captured from the current staging runtime.
>
> **What this does NOT change.** No product defect was found. The candidate is unchanged. No staging
> action, test execution, or Git mutation occurred. The budget/authority blockers (§1, G7) stand
> unchanged, and all substantive gap conclusions (G1, G2, G3, G5, G6, G7) survive — only their
> citations were repaired.

> # ⛔ ROUND-2 SUPERSEDING CORRECTION — 2026-08-09 (lock byte provenance)
>
> **Applied by:** a second, fresh `claude-opus-5` (xhigh) documentation-only repair session, same
> two-file scope, at documentation HEAD `f8a6bc0f1a7fa00fcd1637297e05424732386da7`.
> **Full evidence:** `GATE_A_POST_GATE_PROVENANCE_REPAIR_2026-08-09.md` §2.7 (reproduction), §4.1,
> §5.1, §6.7, §10.
> **Where this block conflicts with anything below — including the round-1 block above — this block
> governs.**
>
> **The defect.** Three different values were collapsed into one "candidate lock hash":
>
> | Value | What it actually is | Status |
> |---|---|---|
> | `47f53fa227bf0f18b9bf9bd77e060d8856961728` | **Git blob object ID (SHA-1)** of `requirements.lock` — hashes `"blob 117762\0" + content`, *not* the content | ✅ correct, and ref-invariant at `2ce41e34…321b`, `851d2aa5`, `f8a6bc0f` **and** frozen source `637307e8` |
> | `a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e` | **SHA-256 of the raw blob content** (LF, **117 762 B**) — the candidate lock's real content identity, and the **expected** byte value of the deployed LF payload | ✅ **use this** — as the *expected* value; see the round-3 block for what has and has not been observed on the host |
> | `40873556a7f4586d77f165b985863138c9fc95b095da64ac52456b8c49098ec3` | **SHA-256 of a Windows CRLF worktree checkout** (**119 274 B**), produced by `core.autocrlf=true` + `* text=auto` on the documentation machine | ⛔ **not a candidate or host value — do not cite** |
>
> `119 274 − 117 762 = 1 512` = exactly the blob's line count: one `\r` per line, nothing else.
>
> **Why this matters here.** It is not a labelling nicety — it is a live host predicate this matrix
> was about to preregister. At the candidate:
> `…/deploy/linux/package.sh:78-83` builds the payload with
> `git -c core.autocrlf=false -c core.eol=lf … archive` (its comment at `:79-81` names the Windows
> CRLF hazard by name); `…/deploy/linux/install.sh:401,416` hashes the **installed** lock and writes
> it to `/etc/mtc-bridge/install_manifest.json` as `requirements_lock_sha256`;
> `…/deploy/linux/verify.sh:82-91` re-verifies every release file against `RELEASE_SHA256SUMS`.
> The installed lock is therefore **expected** to hash to `a1881296…` (⛔ round-3 precision:
> expected **by construction**; no observed host read of that value exists in the located evidence —
> see the round-3 block above). **A3's "Output artifact" line invited a run-kit author to preregister
> `40873556…` as the expected value — a hash of no byte stream the candidate contains, so against a
> host that does match the payload it fails and raises a fabricated lock-drift STOP on a protected
> surface.**
>
> **This was already right before it was broken.** `SECURITY_BASELINE.md:28-29` records "Git blob"
> and "Raw Git-blob SHA-256" as two separate rows with exactly these values, and its own snippet at
> `:155-174` derives them the same way (`git cat-file blob` → `hashlib.sha256` at `:172-174`);
> `WPI_READINESS_RECORD_2026-08-01.md:52` records both.
> `40873556…` exists in no product file and in no record predating 2026-08-08.
>
> **Also corrected in round 2:**
>
> 1. **A3's "lock-identity precision" caveat is withdrawn.** The lock blob at `637307e8` is *also*
>    `47f53fa2…`, so `SECURITY_BASELINE.md`'s lock identity **is** the current candidate's. There is
>    no separate "`1adf9ae5` lock blob hash" to avoid citing.
> 2. **The remaining bare product/deploy citations are now qualified** — the ones round 1 corrected
>    were qualified, but the ones it did not dispute were left as bare `<path>` references, which
>    G8's own rule classes as unverified. See the new §4b and repair-record §6.7.
> 3. **"Line numbers coincide" ≠ "blob is ref-invariant."** Three of the seven cited test files are
>    byte-identical on both refs; a fourth agreed by luck. See §4 and repair-record §5.1.
> 4. **The gated steady profile carries no start-mode pin** (§0.6 applies to the first-start unit
>    only). Recorded in A4 as a preregistration prerequisite — **not** as a defect.
>
> **What round 2 does NOT change.** No product defect. Candidate unchanged. No staging action, test
> execution, or Git mutation. The 56-entry / 1345-hash counts stand (re-derived again). Every
> round-1 conclusion other than the lock-hash label stands, G4 stays withdrawn, and WP0 stays
> uneditable.

> # ⛔ ROUND-3 SUPERSEDING CORRECTION — 2026-08-09 (expected payload bytes vs observed host bytes)
>
> **Applied by:** a third, fresh `claude-opus-5` (xhigh) documentation-only repair session, same
> two-file scope, at documentation HEAD `f8a6bc0f1a7fa00fcd1637297e05424732386da7` (rounds 1–2 present
> as uncommitted changes to these two files; nothing committed, no Git mutation).
> **Full evidence:** `GATE_A_POST_GATE_PROVENANCE_REPAIR_2026-08-09.md` §2.7(e), §2.7(g), §3, §11.
> **Where this block conflicts with anything below — including both blocks above — this block
> governs.**
>
> **What stands.** `a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e` remains the
> correct **expected source/payload byte hash** of `requirements.lock` — SHA-256 of the raw **LF**
> Git-blob content, re-derived a third time this round (`git cat-file blob 47f53fa2… | sha256sum`;
> `git cat-file -s` → `117762`), and the byte stream the LF-pinned `git archive` ships
> (`2ce41e34…321b:…/deploy/linux/package.sh:78-83`). `40873556…` stays withdrawn — that conclusion is
> byte arithmetic over the blob and depends on nothing corrected here.
>
> **What is corrected.** Rounds 1–2 stated as **fact** that the lock installed on `GATEA-STAGING`
> hashes to `a1881296…` and that `/etc/mtc-bridge/install_manifest.json` → `requirements_lock_sha256`
> carries it. That is a **derivation from source and packaging mechanics, not an observation.**
> **No Gate-A evidence located in this repair records the observed SHA-256 of
> `/opt/mtc-bridge/releases/2ce41e34…321b/IBKR_PAPER_BRIDGE/requirements.lock`, nor the observed
> `requirements_lock_sha256` on the host.** What the evidence actually holds (repair-record §2.7g):
> the transition inventory's read of that manifest records **boolean/schema fields only, no hash of
> any kind**; `install.sh` writes `LOCK_SHA` into the manifest (`:416`) but never logs it (`:431-433`),
> so it is not expected in the A-2 capture either; and the only local `verify_lock` /
> `RELEASE_SHA256SUMS` PASS records belong to the **superseded** `ebada020` and `1adf9ae5` releases and
> carry package **counts**, never a lock hash.
>
> | Value class | Status in this matrix |
> |---|---|
> | Expected source/payload byte hash (LF, 117 762 B) `a1881296…` | ✅ **Established.** Preregister as the *expected* value. |
> | Observed installed-host value — `sha256sum` of the installed lock / manifest `requirements_lock_sha256` | ⛔ **NOT IN EVIDENCE.** An open read-only host predicate, blocked by §1. Never write it as known. |
> | Windows worktree checkout SHA-256 (CRLF, 119 274 B) `40873556…` | ⛔ **Never cite** (unchanged). |
>
> **Effect on preregistration (A3, B1).** The lock comparison is a predicate **to be tested**, not a
> restatement of a verified fact. On a mismatch against `a1881296…` the disposition is **investigate
> read-only**, weighing a wrong expected value *and* genuine drift — do not auto-classify either way.
> Round 2's "documentation error, not lock drift" disposition is specific to the withdrawn
> `40873556…` and does not transfer.
>
> **What round 3 does NOT change.** No product defect. Candidate unchanged. No staging action, no host
> read, no test execution, no Git mutation, no commit. Counts 56 / 1345 stand. G4 stays withdrawn,
> WP0 stays uneditable, and every other round-1 and round-2 conclusion stands.

- **Date:** 2026-08-09.
- **Model / route:** GLM-5.2 via the Z.AI Coding Plan route (owner-requested exact model).
- **Session type:** Bounded documentation unit, **read-only / local**. Starting documentation HEAD
  `52b8f496`; frozen product candidate `2ce41e34bceb599d80af24c5c33d835820ec321b` (unchanged).
  **⛔ Provenance defect (see correction block above):** the authoring session read *product* files
  from the documentation checkout rather than from the frozen candidate. The two refs are divergent,
  so every product/deploy/test/tool fact originally recorded here was doc-derived and has been
  re-verified at `2ce41e34…321b` by the 2026-08-09 repair unit.
- **Worker scope:** GLM-5.2 edited only the four task-named files — this new record,
  `_AI_MEMORY/NEXT_STEPS.md`, `_AI_MEMORY/GLOBAL_HANDOFF.md`, and
  `11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md` (the latter three prepended; all prior text
  preserved). GLM-5.2 ran **no** SSH, Gate-A script, sudo, systemctl, reboot, test, package/install,
  network/broker/exchange, credential-read, Git, staging-host, or mutation command. Targeted reads
  and `rg` only; no broad repo scan. **No command block in this document was executed.** No evidence
  directory is claimed to exist unless an existing path is cited.

- **Lead acceptance corrections:** Codex independently checked the four-file diff against real source
  and corrected three GLM drafting errors before integration: ~~the test map contains **10 existing
  symbols plus 1 stale/absent symbol**~~ (**SUPERSEDED 2026-08-09 — see below**); reboot does **not**
  create a mask (the currently running unit is unmasked, so its post-reboot mask state must be
  preregistered rather than assumed); and credentialed TESTNET egress observation does **not** require
  ARM. ARM remains forbidden. ~~Codex also re-derived the candidate lock blob SHA-256 as
  `40873556a7f4586d77f165b985863138c9fc95b095da64ac52456b8c49098ec3` (56 entries, 1345 hashes).~~
  **⛔ SUPERSEDED 2026-08-09 (round 2) — see the next two bullets.**
- **⛔ Superseding correction to the first Lead item:** the test map contains **11 existing symbols
  and zero stale symbols** at the frozen candidate. The "10 + 1 stale" reading inherited the
  authoring session's wrong ref; it is a fact about `851d2aa5`, not about `2ce41e34…321b`. The other
  two Lead corrections stand.
- **⛔ Superseding correction to the fourth Lead item (round 2) — the lock hash.** The counts are
  right (**56** `==`-pinned entries, **1345** `--hash=sha256:` lines, re-derived at the candidate
  twice), and the blob **is** byte-identical across refs
  (`47f53fa227bf0f18b9bf9bd77e060d8856961728`) — but the value `40873556…` is **not** a candidate
  lock hash and round 1 was wrong to bless it. It is the SHA-256 of a **Windows CRLF worktree
  checkout** (119 274 B). The lock's content SHA-256 is
  **`a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e`** (LF, 117 762 B), and *that*
  is what blob identity makes ref-invariant. Note also that `47f53fa2…` is a **blob object ID**, not
  a content hash — calling it "the lock blob SHA-256" conflated two different hashes of two
  different inputs. Reproduction: repair-record §2.7.
  ⛔ **Round-3 scope on this same value:** `a1881296…` is the **expected** source/payload byte hash.
  The staging host's own value — installed lock, and manifest `requirements_lock_sha256` — has never
  been read in any located evidence (round-3 block; §4b; repair-record §2.7g).

> **Reader contract.** This is a *preregistration* matrix: it records what each obligation is, what
> evidence already exists, and the exact method that *would* close it — but it executes nothing on the
> host. Every proposed host command is explicitly marked **NOT EXECUTED** and is safe-by-construction
> (read-only, or a documented mutation that requires its own authority). Where an exact safe command
> cannot yet be specified, the cell reads **COMMAND GAP** rather than improvising one.

---

## 0. Headline (facts, verified from source this unit)

1. **Correct sequence after Gate A is `WP-L Phase 2 → WP-I staging verification → Audit 2 → WP-A`.**
   Source: `TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md` §23a steps 3–5 (lines 972–973)
   and §"Audit 2" (lines 863, 1195–1199); confirmed one-line by
   `GATE_A_PREREGISTRATION_AND_STAGING_RUNBOOK_2026-08-01.md:137`
   (`Gate A verification → WP-L Phase 2 → WP-I staging → Audit 2 → WP-A`, all DISARMED). **Do not
   start WP-V** (§23a step 10 is gated behind Gate B / deployment approval).
2. **Reuse immutable Gate-A evidence where predicates overlap, but do not call Gate A itself
   WP-L/WP-I/WP-A completion, and do not rerun Gate A.** Gate A A-0..A-9 PASS is *staging acceptance
   only* (`GATE_A_A9_PASS_FINAL_2026-08-09D.md`); it authorises no ARM, credential, broker, order,
   TESTNET/mainnet, master merge, or promotion.
3. **The staging host `GATEA-STAGING` remains safe and retained:** active, `Restart=no`,
   `NRestarts=0`, MainPID 189813, exactly one loopback listener `127.0.0.1:8790`, credential-free
   DISARMED `state_version=1`, all credential/network/exchange/ARM flags off; only candidate
   `2ce41e34…321b` installed (`GATE_A_POST_GATE_TRANSITION_INVENTORY_2026-08-09.md`).
4. **Exact 50-hour balance is NOT REPRODUCIBLE** (`GATE_A_50H_LEDGER_RECONSTRUCTION_2026-08-09.md`,
   state 5). Therefore **no host execution may be authorised or performed in this unit**; local /
   read-only preparation continues.
5. **56-entry hash-locked closure confirmed at the candidate** (re-verified at
   `2ce41e34…321b` by both repair rounds):
   `2ce41e34…321b:IBKR_PAPER_BRIDGE/requirements.lock` has **56** `==`-pinned entries and
   **1345** `--hash=sha256:` lines (≥1 hash per entry);
   `2ce41e34…321b:IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py` (blob `8ccd6f32…`) rejects
   URLs/VCS/index-overrides and requires exact `==` + ≥1 hash (`parse_lock` at `:28`), and prints
   the count it actually parsed rather than a constant (`:97`). Both blobs are **identical on the
   documentation and candidate refs**, so this pair of facts is ref-invariant and was the one class
   of product claim the original provenance defect could not corrupt.
   **⛔ Round-2 precision — the lock's three identities, none interchangeable:**
   - **Git blob object ID (SHA-1):** `47f53fa227bf0f18b9bf9bd77e060d8856961728` — ref-invariant at
     `2ce41e34…321b`, `851d2aa5`, `f8a6bc0f` and frozen source `637307e8`.
   - **Raw blob content SHA-256 (LF, 117 762 B):**
     `a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e` — **the value to
     preregister, as the *expected* one**; it is what the LF-pinned `git archive` ships, and therefore
     what `install.sh` is expected to record as `requirements_lock_sha256` and what
     `RELEASE_SHA256SUMS` is expected to re-verify.
   - **Windows worktree CRLF checkout SHA-256 (119 274 B):** `40873556…` — a local artifact of this
     documentation machine. **Never a candidate or host value.**
   - **⛔ Observed installed-host value (round 3): NOT IN EVIDENCE.** Neither a `sha256sum` of
     `/opt/mtc-bridge/releases/2ce41e34…321b/IBKR_PAPER_BRIDGE/requirements.lock` nor the host's
     `/etc/mtc-bridge/install_manifest.json` → `requirements_lock_sha256` has been captured in any
     record located by the repair unit. This is a **fourth, distinct identity** — an open read-only
     host predicate — and `a1881296…` is its *expected*, not its confirmed, value.

   Derive the content hash as `git cat-file blob 47f53fa2… | sha256sum`. Do **not** hash the file
   from a Windows checkout, and do **not** write the derived value as though the host had been read.
6. **⛔ NEW (candidate-only; omitted by the original authoring session) — the deployed candidate
   enforces credential-free DISARMED start mode at three layers.** None of this exists in the
   documentation-branch deploy tree (`git grep MTC_BRIDGE_START_MODE 851d2aa5 --
   IBKR_PAPER_BRIDGE/deploy/linux` → no output), which is why the original matrix never recorded it:
   - **Unit pins the mode:**
     `2ce41e34…321b:IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template:42`
     → `Environment=MTC_BRIDGE_START_MODE=credential_free_disarmed`.
   - **Verifier requires it and blocks override:** `2ce41e34…321b:…/deploy/linux/verify.sh:171`
     carries `MTC_BRIDGE_START_MODE=credential_free_disarmed` in the required unit-needle list;
     `…/verify.sh:143-146` **fails** on any `MTC_BRIDGE_START_MODE=` assignment (bare or `export`) in
     `/etc/mtc-bridge/mtc-bridge.env`, so the env file cannot override the unit;
     `…/deploy/linux/env/mtc-bridge.env.template:40-42` documents that the key must stay absent.
   - **Application implements it:** `2ce41e34…321b:IBKR_PAPER_BRIDGE/bridge/app.py:32` defines the
     mode; `:113` rejects `--dry-run` with it; `:115` rejects being handed a broker; `:138-147`
     forces `network="disabled"`, `exchange_conn="disabled"`, `exchange_enabled=False`,
     `credential_lookup="disabled"`, **`arm_enabled=False`**; and `:149`
     (`if start_runtime and not credential_free_disarmed:`) means the broker build — which resolves
     credentials at `:244` and selects `network="testnet"` at `:246` — is **never reached** in this
     mode. **No broker is constructed; ARM and orders are unavailable.**
   Cite this only as candidate-qualified source or as installed-host / Gate-A evidence tied to
   `2ce41e34…321b`. **Never** from the documentation checkout.

---

## 1. Authority & budget envelope (what controls this matrix)

- **Broad standing programme authorisation** exists (`OWNER_AUTH_50H_EXECUTION_PROMPT_2026-07-31.md`)
  covering WP-L/WP-I/WP-A/WP-R/WP-V, the named expendable staging host, and even pre-granting the
  WP-V / ARM / first-TESTNET approvals — **but only subject to every objective prerequisite passing**
  (`GATE_A_POST_GATE_ROADMAP_AUTHORITY_DISCOVERY_2026-08-09.md` §2.1).
- **Two narrower later constraints control the current transition and were not lifted by name:**
  `CODEX_TAKEOVER_HANDOFF_2026-08-02.md:261-263` and
  `NEXT_SESSION_HANDOFF_2026-08-08.md` hard-stop (merge to master, WP-V/deployment, KVM2, credentials,
  broker/exchange, ARM, orders, TESTNET/mainnet, Pine/parity/MTC/trading, any economic action).
- **Conservative result:** read-only / local preparation and evidence reconstruction are authorised
  now; WP-V / KVM2 / master merge / credentials / broker / ARM / orders / TESTNET-mainnet / economic
  action / old-payload deletion are **NOT** authorised now.
- **Budget blocker:** the exact used/remaining balance against the hard 50 h ceiling is not
  reproducible, so budget compliance for any *server-executed* post-Gate work cannot be proven. This
  bounds what may be *committed to*, not what may be *prepared*. A human re-plan or explicit ceiling
  extension is required before any host execution.

---

## 2. Obligation matrix — column legend

Each obligation below carries these fields: **Predicate · Canonical source · Existing evidence ·
Remaining evidence · Proposed command/method (NOT EXECUTED) · Mutation class · Authority/budget
prerequisite · Output artifact · PASS condition · Failure disposition · D026 note.**

Mutation classes: `read-only-host` (asserts only), `mutating-host` (stops/masks/reboots/restores —
needs its own authority), `audit` (canonical Gate-5/Gate-6 contract), `local-static` (no host at all).

---

## Group A — Reusable immutable Gate-A evidence (NO new host action)

These are *already-captured, immutable* facts. They satisfy part or all of a downstream predicate and
must be **reused, not re-run**. None of them is, by itself, WP-L/WP-I/WP-A completion.

### A1 — Frozen product candidate identity
- **Predicate:** the deployed artifact equals the accepted frozen candidate.
- **Canonical source:** `GATE_A_A9_PASS_FINAL_2026-08-09D.md`;
  `2ce41e34…321b:IBKR_PAPER_BRIDGE/deploy/linux/README.md` (⛔ round-2 qualification — candidate blob
  `f3f1d75e7e…`, **differs** from the documentation blob `666b79d834…`; cite the candidate, and cite
  its "never been executed" lines only as historical — G6).
- **Existing evidence:** candidate `2ce41e34bceb599d80af24c5c33d835820ec321b`; A-0..A-9 ran against
  exactly this SHA; transition inventory confirms only this release is installed at
  `/opt/mtc-bridge/releases/2ce41e34…321b`.
- **Remaining evidence:** none for identity.
- **Proposed method:** none — identity is immutable. Cite the SHA in every downstream artifact.
- **Mutation class:** `local-static`. **Authority/budget:** none.
- **Output artifact:** cited inline. **PASS:** SHA matches. **Failure disposition:** a different SHA
  is a hard STOP (candidate drift).

### A2 — Immutable Gate-A evidence set (A0–A9 + reports)
- **Predicate:** staging evidence is captured, hashed, and locally preserved.
- **Canonical source:** `GATE_A_POST_GATE_TRANSITION_INVENTORY_2026-08-09.md` ("Canonical Gate-A
  evidence index").
- **Existing evidence:** A0–A9 logs with recorded SHA-256/bytes; canonical PASS reports
  `GATE_A_LOCAL_RUN_KIT_2026-08-08C.md`, `GATE_A_A4_PASS_…`, `GATE_A_A5_PASS_2026-08-09E.md`,
  `GATE_A_A6_PASS_2026-08-09D.md`, `GATE_A_A7_PASS_…`, `GATE_A_A8_PASS_…`, `GATE_A_A9_PASS_FINAL_…`.
- **Remaining evidence:** none — do not rerun.
- **Proposed method:** reference by path + hash; never re-execute.
- **Mutation class:** `local-static`. **Authority/budget:** none.
- **Output artifact:** cited inline. **PASS:** hashes match the recorded values. **Failure
  disposition:** a hash mismatch in preserved evidence is a STOP for the chain that depends on it.

### A3 — WP-I static minimum-security / secret-scan / egress *inventory* (static only)
- **Predicate:** pinned dependency inventory, content-redacted secret scan (zero hits), and outbound
  network *inventory* exist as local artifacts.
- **Canonical source:** `SECURITY_BASELINE.md` — **⛔ reclassified.** This file is **ABSENT from the
  frozen candidate** (`git rev-parse 2ce41e34…321b:IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md`
  → `fatal: … exists on disk, but not in '2ce41e34…'`). It is a **later governance/evidence
  artifact** on the documentation branch (blob `8db2e6dd…`), **not** a member of the deployed
  candidate payload. It may legitimately *describe* analysis of the candidate, but it must be cited
  as governance evidence with that distinction stated — never as candidate source. Candidate-side
  sources for this predicate are `2ce41e34…321b:IBKR_PAPER_BRIDGE/requirements.lock` and
  `…/deploy/linux/verify_lock.py` (both ref-invariant blobs).
- **Existing evidence:** 56-entry exact+hashed lock; secret scan zero category/path hits at the
  *frozen* tree; egress inventory (TESTNET runtime-required, optional Telegram, install-time index,
  loopback listener, forbidden mainnet, unused Anthropic/xAI). **⛔ Scope note:** the egress
  inventory is a *static reading of what the code could reach*. It does **not** describe the
  deployed start mode, which constructs no broker at all (§0.6, C5).
- **Remaining evidence:** this is **PRE-GATE-A / STATIC ONLY** — it is not a runtime egress capture,
  not an Ubuntu install result, and not destination-egress control. Runtime egress / TESTNET-only /
  no-mainnet remain owed (see C5).
- **~~⚠ Lock-identity precision:~~ ⛔ WITHDRAWN AND REPLACED (round 2).** The withdrawn text read:
  *"the lock blob/SHA-256 recorded in SECURITY_BASELINE is for frozen source `637307e8` / candidate
  `1adf9ae5…` … the exact lock blob SHA-256 re-derived by the Lead at `2ce41e34…321b` is
  `40873556…`. Do not cite the `1adf9ae5` blob hash as the current candidate's."* Both halves are
  wrong:
  - `git rev-parse 637307e8:IBKR_PAPER_BRIDGE/requirements.lock` → `47f53fa2…` — the **same blob**
    as the candidate's. SECURITY_BASELINE's lock identity therefore **is** the current candidate's,
    and there is no distinct "`1adf9ae5` lock blob hash" to avoid citing.
  - The value to cite is the one SECURITY_BASELINE already records at `:29`:
    **`a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e`** (raw blob content, LF,
    117 762 B). `40873556…` is a Windows CRLF worktree checkout hash (119 274 B) and is **not** a
    candidate or host value.
  The *property* (56 exact+hashed entries; `verify_lock.py` contract) is source-invariant and was
  re-confirmed at the candidate in both rounds (56 entries, 1345 hashes).
- **✅ Provenance-safe:** `2ce41e34…321b:IBKR_PAPER_BRIDGE/requirements.lock` (`47f53fa2…`) and
  `2ce41e34…321b:IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py` (`8ccd6f32…`) are **byte-identical
  on the documentation and candidate refs**, so this A3 lock claim is unaffected by the *provenance*
  defect. ⛔ **Round-2 caveat:** ref-invariance protects the **blob**, not the number attached to it.
  The wrong hash was recorded *despite* the blob being identical, because it was taken from a
  Windows checkout instead of from the blob. "Ref-invariant" is not a licence to skip re-derivation.
- **Mutation class:** `local-static`. **Authority/budget:** none.
- **Output artifact (⛔ RECORDED round 2; ⛔ scoped round 3):** lock **blob object ID**
  `47f53fa227bf0f18b9bf9bd77e060d8856961728`; lock **raw content SHA-256 (LF, 117 762 B)**
  `a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e`, derived by
  `git cat-file blob 47f53fa2… | sha256sum`. **This is the value a run-kit step must preregister as
  the *expected* one** when comparing against `/etc/mtc-bridge/install_manifest.json` →
  `requirements_lock_sha256` (written by `2ce41e34…321b:…/deploy/linux/install.sh:401,416`) or against
  `RELEASE_SHA256SUMS` (re-verified by `…/verify.sh:82-91`).
  ⛔ **Round-3 boundary — the host side of this comparison is still open.** Both values above are
  **source-derived**. No located Gate-A evidence records the **observed** installed-lock SHA-256 or
  the host manifest's `requirements_lock_sha256` (repair-record §2.7g): the transition inventory read
  that manifest for boolean/schema fields only, `install.sh` never logs `LOCK_SHA`, and the local
  `verify_lock`/`RELEASE_SHA256SUMS` PASS records belong to the superseded `ebada020` / `1adf9ae5`
  releases and carry counts, not hashes. So this A3 artifact closes the **static/local** predicate
  only; the host comparison remains a preregistered, unexecuted read-only step (B1), blocked by §1.
  **PASS (static, satisfied):** 56 entries, every entry exact+hashed, no URL/VCS/index override.
  **Failure disposition:** a non-hashed or count-drifting lock in **source** is a product-SHA change
  (STOP; not a documentation unit). A **host** mismatch against `a1881296…`, whenever that comparison
  is first authorised and run, is **investigate read-only** — weigh a wrong expected value *and*
  genuine drift before escalating or dismissing; do not auto-classify. **D026:** n/a (inventory, not a
  regression test).

### A4 — Unit-template static invariants (design facts)
- **Predicate:** the installed unit declares the safety-critical directives.
- **Canonical source (candidate-qualified):**
  `2ce41e34…321b:IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template`
  (blob `c18232549d…`, **differs** from the doc branch);
  `2ce41e34…321b:IBKR_PAPER_BRIDGE/deploy/linux/verify.sh` **needle list at lines 160–171**
  (⛔ was cited as "lines 155–165" — a documentation-checkout offset);
  `2ce41e34…321b:IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh` (constants; also differs).
- **Existing evidence:** `Restart=no`; no `[Install]` section; `KillSignal=SIGTERM`,
  `KillMode=mixed`, `TimeoutStopSec=45`, `FinalKillSignal=SIGKILL`; `MTC_BRIDGE_STATE_DB`,
  `ReadWritePaths`, sandboxing directives (`NoNewPrivileges`, `ProtectSystem=strict`,
  `RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX`, etc.); loopback bind asserted in code;
  **⛔ and — omitted originally — `Environment=MTC_BRIDGE_START_MODE=credential_free_disarmed` at
  template line 42, which `verify.sh:171` requires as a needle** (§0.6). The candidate's full
  required needle set at `verify.sh:160-171` is: `Restart=no`, `User=mtc-bridge`, `PrivateTmp=yes`,
  `ProtectSystem=strict`, `NoNewPrivileges=yes`, `KillSignal=SIGTERM`, `TimeoutStopSec=45`,
  `StartLimitBurst=3`, `ReadWritePaths=<state> <log>`, `MTC_BRIDGE_STATE_DB=<db>`, and
  `MTC_BRIDGE_START_MODE=credential_free_disarmed`.
- **⛔ Candidate line anchors (round 2 — the directives above were previously asserted without
  them).** At `2ce41e34…321b:IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template`
  (blob `c1823254…`): `Environment=MTC_BRIDGE_STATE_DB=…` **:40**;
  `Environment=MTC_BRIDGE_START_MODE=credential_free_disarmed` **:42**; `KillSignal=SIGTERM` **:48**;
  `KillMode=mixed` **:49**; `TimeoutStopSec=45` **:51**; `FinalKillSignal=SIGKILL` **:52**;
  `Restart=no` **:55**. The only `[Install]` match in the file is the explanatory comment at **:11**
  — there is **no** `[Install]` section.
- **Remaining evidence:** the *template* is static; the *rendered/installed* unit on the host is
  verified by A4-staging (B2). The **steady** profile
  (`2ce41e34…321b:IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-steady.service.template`,
  blob `121229ea5b…` — ⛔ round-2 finding: **ref-invariant**, byte-identical on both refs, so this
  one sub-claim was never at provenance risk) is a **gated artifact** — never installed/enabled;
  `Restart=on-failure` at **:52**; itself has no `[Install]` (only the comment at **:19**).
- **⛔ Start-mode asymmetry (round 2, NEW — preregistration prerequisite, NOT a defect claim).** The
  steady template carries **no** `Environment=MTC_BRIDGE_START_MODE=` line; its `Environment=` set is
  **:39-41** only (`PYTHONUTF8`, `PYTHONDONTWRITEBYTECODE`, `MTC_BRIDGE_STATE_DB`). The three-layer
  credential-free DISARMED enforcement of §0.6 is therefore a property of the **first-start unit**,
  not of the candidate in general. This is **not** a product defect — the steady profile is gated,
  never installed, never enabled, and its admission is a separately authorised Gate-B / WP-V step.
  It is recorded so that no future admission preregistration assumes the pin carries over: it does
  not, and §0.6 as written could invite that assumption.
- **Mutation class:** `local-static`. **Authority/budget:** none.
- **Output artifact:** cited inline. **PASS:** template matches the accepted release template byte-for
  byte (`2ce41e34…321b:…/verify.sh:186-195` `cmp`; ⛔ was cited as "lines 182–190"). **Failure
  disposition:** template drift = candidate change.

### A5 — Candidate source-map: target test symbols (**all 11 exist**)
- **Predicate:** the regression tests named as evidence in the readiness baseline still exist in the
  candidate source.
- **Canonical source:** `WP0_SCOPE_BASELINE_RECORD_2026-07-31.md` (evidence map, documentation
  branch); **test symbols read from `2ce41e34…321b:IBKR_PAPER_BRIDGE/tests/`** — never from the
  documentation checkout.
- **⛔ CORRECTED. Existing evidence (re-verified by `git grep` at the frozen candidate):** **all 11**
  target symbols resolve, as listed in §4 below. The earlier statement that
  `test_kill_restart_after_request_commit_keeps_killed_and_resumes_once` is **absent** was **FALSE
  for the deployed candidate** — it exists at
  `2ce41e34…321b:IBKR_PAPER_BRIDGE/tests/test_partial_fill_protection.py:2765`. It is absent only
  from the divergent documentation checkout, which is what the original `rg` scanned.
  **Therefore all three symbols anchoring WP0 I-R2 exist** (`test_kill_persists_across_restart`,
  `test_killed_alive_is_interrupted`, and
  `test_kill_restart_after_request_commit_keeps_killed_and_resumes_once`). **Gap G4 is withdrawn;
  the proposed WP0 deletion is cancelled; no replacement symbol is needed.**
- **Mutation class:** `local-static`. **Authority/budget:** none.
- **Output artifact:** the corrected test-map table (§4). **PASS:** cited symbols exist at the cited
  **candidate-qualified** paths. **Failure disposition:** before declaring any cited symbol absent,
  re-grep at `2ce41e34…321b`; an absence in the documentation checkout is a **provenance error**,
  not a stale evidence-map node and not a product defect. **D026:** existence ≠ closure; and
  existence proven by `git grep` is not execution — see §5.

### A6 — Lock / `verify_lock.py` contract
- **Predicate:** an offline, network-free verifier proves every lock entry is exact+hashed and (with
  `--check-installed`) that the installed venv distribution set equals the lock.
- **Canonical source (⛔ round-2 qualification):**
  `2ce41e34…321b:IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py`, blob `8ccd6f329154422a85b8e7663e6a079dbd47b4fd`
  — **ref-invariant** (byte-identical on both refs), so either checkout would have given the same
  answer here; it is written candidate-qualified anyway, per G8.
- **Existing evidence (with candidate anchors, round 2):** `parse_lock` (**:28**) rejects
  URLs/VCS/index overrides and requires exact `==` + ≥1 `--hash=sha256:` per entry;
  `--check-installed` (**:78**, parsed in `main` at **:75**) compares installed vs expected, allowing
  only the `pip`/`setuptools` bootstrap set; the PASS line at **:97** is
  `print(f"verify_lock: PASS: {mode}; packages={len(expected)}")` — i.e. B1's expected `packages=56`
  is emitted from the count actually parsed out of the lock, **not** a hard-coded constant, so the
  number is evidence rather than an echo. Re-confirmed in both rounds: 56 entries.
- **Mutation class:** `local-static` (the tool) / `read-only-host` (the `--check-installed` run).
- **Authority/budget:** the *local* parse needs none; the *host* `--check-installed` run is a B1 host
  check (preregistered, not run).
- **Output artifact:** `verify_lock: PASS: lock+installed; packages=56`. **PASS:** exit 0 and the
  printed count is 56. **Failure disposition:** exit 1 = missing/extra/unpinned distro.

---

## Group B — Proposed read-only post-start host checks (PREREGISTER ONLY; do NOT run)

These assert the *currently-running, accepted* staging state without mutating it. They are the
bounded subchecks that replace a full `verify.sh` run (see Gap G2 — full `verify.sh` intentionally
fails post-start). All **NOT EXECUTED**.

### B1 — Ubuntu Python 3.12 venv + exact 56-entry installed lock parity
- **Predicate:** the per-SHA venv interpreter is Python 3.12 and its installed distribution set
  exactly equals the 56-entry lock.
- **Canonical source:** `WPI_READINESS_RECORD_2026-08-01.md` §6 ("installed distribution set exactly
  equals the 56-entry lock"); `2ce41e34…321b:…/deploy/linux/verify.sh` **§3 lines 103–122**
  (⛔ was "lines 104–121"); `2ce41e34…321b:…/deploy/linux/verify_lock.py` (blob `8ccd6f32…`,
  ref-invariant; contract anchors in A6).
- **⛔ Hash-preregistration warning (round 2).** If this step is ever extended to also assert the
  *lock file's* identity on the host — e.g. against `/etc/mtc-bridge/install_manifest.json` →
  `requirements_lock_sha256` (written by `2ce41e34…321b:…/deploy/linux/install.sh:401,416`) or
  against `RELEASE_SHA256SUMS` (re-verified by `…/verify.sh:82-91`) — the expected value is the raw
  blob content SHA-256 **`a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e`**, not
  `40873556…`. The payload is built LF-pinned (`…/package.sh:78-83`). A mismatch caused by using the
  Windows worktree hash is a **documentation error, not lock drift**, and must not be escalated.
  ⛔ **Round-3 addition:** that extension is a **new capture**, not a re-check of something already
  known — the host value has never been read. It is specified separately as **B1a** below.
- **Existing evidence:** static lock is 56 exact+hashed (A3/A6); venv path is
  `/opt/mtc-bridge/venvs/2ce41e34…321b`. **Not yet proven on Ubuntu at the candidate.**
- **Remaining evidence:** the runtime `--check-installed` PASS against the live venv.
- **Proposed command (NOT EXECUTED):**
  ```bash
  # Run from the per-SHA venv interpreter; read-only; no network.
  /opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b/bin/python \
      /opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b/IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py \
      --lock /opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b/IBKR_PAPER_BRIDGE/requirements.lock \
      --check-installed
  # expect stdout: verify_lock: PASS: lock+installed; packages=56
  ```
- **Mutation class:** `read-only-host`. **Authority/budget:** host access + budget lift required
  (blocked, §1). **Output artifact:** the command's stdout (no-clobber capture path assigned at
  execution; NOT YET CREATED). **PASS:** exit 0, `packages=56`. **Failure disposition:** missing/extra
  distro = STOP (product/install drift). **D026:** n/a (parity proof, not a regression test).

### ⛔ B1a — installed `requirements.lock` byte identity on the host (NEW, round 3 — OPEN capture)
- **Predicate:** the `requirements.lock` **installed** at
  `/opt/mtc-bridge/releases/2ce41e34…321b/IBKR_PAPER_BRIDGE/` is byte-identical to the frozen
  candidate's LF payload, and the host manifest's `requirements_lock_sha256` agrees.
- **Canonical source (expected value, source-derived):** `git cat-file blob 47f53fa2… | sha256sum`
  → `a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e` (LF, 117 762 B), shipped by the
  LF-pinned export at `2ce41e34…321b:…/deploy/linux/package.sh:78-83`, hashed and recorded at
  `…/install.sh:401,416`, re-verified against `RELEASE_SHA256SUMS` at `…/verify.sh:82-91`.
- **⛔ Existing evidence: NONE.** This is why B1a exists. No located Gate-A evidence records either the
  observed installed-lock SHA-256 or the host's `requirements_lock_sha256`: the transition inventory
  read `/etc/mtc-bridge/install_manifest.json` for boolean/schema fields only; `install.sh` writes
  `LOCK_SHA` into the manifest but never logs it (`:431-433` print the release and **unit** hashes); and
  the only local `verify_lock` / `RELEASE_SHA256SUMS` PASS records belong to the superseded `ebada020`
  and `1adf9ae5` releases and carry package **counts**, not hashes. Enumeration: repair-record §2.7g.
- **Remaining evidence:** one read-only host read, captured with its command and output.
- **Proposed command (NOT EXECUTED), read-only:**
  ```bash
  sha256sum /opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b/IBKR_PAPER_BRIDGE/requirements.lock
  # expect: a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e
  # optional corroboration (root read; the manifest is 0640 root:root):
  #   grep -o '"requirements_lock_sha256": *"[0-9a-f]\{64\}"' /etc/mtc-bridge/install_manifest.json
  ```
- **Mutation class:** `read-only-host`. **Authority/budget:** host access + budget lift required
  (blocked, §1). **Output artifact:** captured stdout, no-clobber path (NOT YET CREATED).
  **PASS:** observed value equals `a1881296…`. **Failure disposition:** **investigate read-only** —
  weigh a wrong expected value *and* genuine drift; re-check the derivation chain (blob → LF-pinned
  export → manifest-verified install) before escalating a STOP or dismissing one. **D026:** n/a
  (capture, not a regression test).

### B2 — systemd runtime identity (active, `Restart=no`, bound to exact SHA/venv)
- **Predicate:** the running unit is the accepted first-start unit, active, `Restart=no`,
  `NRestarts=0`, bound to the exact release SHA and per-SHA venv, with no `[Install]`.
- **Canonical source:** `2ce41e34…321b:…/deploy/linux/verify.sh` **§6 lines 155–222**
  (⛔ was "lines 150–199"); transition inventory (current unit fragment SHA-256 `538c1c60…279bd`,
  3736 B — installed-host evidence tied to the candidate, unaffected by the provenance defect).
- **Existing evidence:** transition inventory recorded MainPID 189813, `Restart=no`, `NRestarts=0`;
  A-5 post-state; A-7/A-8/A-9 postchecks.
- **Proposed commands (NOT EXECUTED), all read-only:**
  ```bash
  systemctl is-active  mtc-bridge-first-start.service            # expect: active
  systemctl show -p NRestarts --value mtc-bridge-first-start.service   # expect: 0
  systemctl show -p Restart  --value mtc-bridge-first-start.service    # expect: no
  systemctl cat mtc-bridge-first-start.service | grep -E 'releases/2ce41e34|venvs/2ce41e34'  # bound
  grep -q '^\[Install\]' /usr/local/lib/systemd/system/mtc-bridge-first-start.service && echo BAD || echo OK
  sha256sum /usr/local/lib/systemd/system/mtc-bridge-first-start.service   # expect 538c1c60…279bd
  ```
- **Mutation class:** `read-only-host`. **Authority/budget:** host access + budget lift (blocked).
  **Output artifact:** captured stdout (NOT YET CREATED). **PASS:** active / NRestarts=0 / Restart=no
  / SHA-bound / no `[Install]` / unit hash = `538c1c60…279bd`. **Failure disposition:** any mismatch =
  STOP (service drift).

### B3 — Paths / ownership / permissions
- **Predicate:** release read-only `0555 root:root`; state+log `0750 mtc-bridge:mtc-bridge`; conf
  `0750 root:root`; env `0600 root:root`; install manifest `0640 root:root`.
- **Canonical source:** `2ce41e34…321b:…/deploy/linux/verify.sh` **§2 lines 77–102 and §4 lines
  123–136** (⛔ was "lines 78–135"); `2ce41e34…321b:…/deploy/linux/README.md` target layout.
- **Existing evidence:** transition inventory (release root mode 555; env 600; manifest 640).
- **Proposed command (NOT EXECUTED):** read-only `stat`/`find` (mirror `verify.sh` assertions without
  the mask/active/port-closed preconditions). **COMMAND GAP:** a single bounded post-start
  permissions-subcheck command is not yet authored as a run-kit step; design it in the local run-kit
  unit (do not run `verify.sh` wholesale — see G2).
- **Mutation class:** `read-only-host`. **Authority/budget:** blocked. **Output artifact:** stat output
  (NOT YET CREATED). **PASS:** modes/owners match. **Failure disposition:** mode/owner drift = STOP.

### B4 — Environment isolation / sandboxing directives present
- **Predicate:** hardening directives are present and effective on the running unit.
- **Canonical source:** `2ce41e34…321b:…/systemd/mtc-bridge-first-start.service.template`;
  `2ce41e34…321b:…/deploy/linux/verify.sh` **needles at lines 160–171** (⛔ was "lines 155–165").
- **Existing evidence:** template declares them (A4), **including
  `MTC_BRIDGE_START_MODE=credential_free_disarmed` at template line 42** (§0.6).
- **Proposed command (NOT EXECUTED):** `systemctl show` the effective security properties
  (`PrivateTmp`, `ProtectSystem`, `NoNewPrivileges`, `CapabilityBoundingSet`, etc.).
- **Mutation class:** `read-only-host`. **Authority/budget:** blocked. **Output artifact:** show output
  (NOT YET CREATED). **PASS:** effective values match template. **Failure disposition:** drift = STOP.

### B5 — Current credential-free DISARMED runtime (no secret value read)
- **Predicate:** API reports DISARMED, `state_version=1`, mode `credential_free_disarmed`, all
  network/exchange/credential/ARM flags off; **no credential value is read.**
- **Canonical source:** A-5/A-7/A-8/A-9 postchecks; transition inventory (installed-host evidence
  tied to `2ce41e34…321b`). **⛔ Candidate-qualified source basis (added):** the reported flags are
  not incidental — they are *set by the deployed start mode*. At
  `2ce41e34…321b:IBKR_PAPER_BRIDGE/bridge/app.py:138-147` the credential-free DISARMED branch pins
  `mode="credential_free_disarmed"`, `network="disabled"`, `exchange_conn="disabled"`,
  `exchange_enabled=False`, `credential_lookup="disabled"`, `arm_enabled=False`; and `:149` skips
  broker construction entirely. The unit pins the mode (template line 42) and `verify.sh:143-146`
  blocks any env-file override (§0.6). **This basis exists only at the candidate** — do not
  re-derive it from the documentation checkout, whose `bridge/app.py` blob (`6d0abc63…`) does not
  contain it.
- **Proposed command (NOT EXECUTED):**
  ```bash
  curl -s http://127.0.0.1:8790/api/status   # via SSH tunnel; inspect state/flags only
  ```
- **Mutation class:** `read-only-host`. **Authority/budget:** blocked. **Output artifact:** redacted
  status JSON (NOT YET CREATED). **PASS:** DISARMED + all flags off. **Failure disposition:** any flag
  on, or state ≠ DISARMED, = STOP and investigate read-only.

### B6 — Loopback-only listener + UFW SSH-only + host-unreachable (re-capture, read-only)
- **Predicate:** exactly one listener, `127.0.0.1:8790` only; no non-loopback/wildcard/VM-IP listener;
  UFW SSH-only; external host cannot reach 8790.
- **Canonical source:** `2ce41e34…321b:…/deploy/linux/verify.sh` **§8 lines 233–251**
  (⛔ was "lines 233–244"); A-8 PASS evidence.
- **Existing evidence:** A-8 already captured `listener_count=1`, `127.0.0.1:8790` only, UFW `rc=0`,
  host `port8790_ok=False`.
- **Proposed command (NOT EXECUTED):** `ss -ltn` filter + `ufw status` (read-only) + host-side
  `TcpClient` reprobe — exactly the A-8 method.
- **Mutation class:** `read-only-host`. **Authority/budget:** blocked. **Output artifact:** socket/UFW
  capture (NOT YET CREATED). **PASS:** single loopback listener, UFW SSH-only, host 8790 closed.
  **Failure disposition:** extra/non-loopback listener or UFW rule = STOP.

---

## Group C — Proposed mutating host checks (PREREGISTER ONLY; do NOT run)

These mutate service/host/database state. Each **requires its own explicit authority + budget lift**
beyond this unit. None is authorised now. Each is marked **NOT EXECUTED**.

### C1 — Graceful SIGTERM clean shutdown (OPEN predicate I-R4)
- **Predicate:** `systemctl stop` delivers SIGTERM; the process exits within `TimeoutStopSec=45`
  (then `FinalKillSignal=SIGKILL`); `NRestarts` stays 0; the DB is consistent afterward; no dangling
  state. (WP0 I-R4, **explicitly OPEN**: "No test asserts SIGTERM/lifespan shutdown leaves no dangling
  state.")
- **Canonical source:** `WP0_SCOPE_BASELINE_RECORD_2026-07-31.md` I-R4 (line 366, documentation
  branch); ⛔ **round-2 qualification of the unit-template half** —
  `2ce41e34…321b:IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template`
  (blob `c1823254…`, **candidate-only**): `KillSignal=SIGTERM` **:48**, `KillMode=mixed` **:49**,
  `TimeoutStopSec=45` **:51**, `FinalKillSignal=SIGKILL` **:52**. Round 1 left this as a bare "unit
  template" reference even though the template blob differs between refs.
- **Existing evidence:** the unit *configures* SIGTERM (template). A-5 proved **SIGKILL** + restart +
  state integrity + DISARMED — **not** graceful SIGTERM, **not** host reboot (Gap G5).
- **Proposed method (NOT EXECUTED):** `systemctl stop` once; capture exit timing, `NRestarts`,
  post-stop DB `PRAGMA quick_check` + `wal_state_bundle` invariants on a read-only copy; then the
  separate recovery start (KVM2-P4-08A/B). **COMMAND GAP:** there is no existing verifier that asserts
  "no dangling state after SIGTERM" — a bounded post-stop evidence procedure must be *designed* (local,
  next unit) before any execution. Do not improvise.
- **Mutation class:** `mutating-host`. **Authority/budget:** requires explicit named lift (stop +
  recovery start) + budget; **blocked**. **Output artifact:** post-stop evidence log (NOT YET CREATED).
  **PASS:** clean exit ≤45 s, `NRestarts`=0, DB quick_check ok, invariants unchanged. **Failure
  disposition:** timeout-to-SIGKILL, dangling writer, or invariant drift = STOP; treat as a candidate
  repair need (re-audit picture), not a documentation outcome. **D026:** if a new SIGTERM-shutdown
  regression test is offered as closure, it must be shown RED (e.g., against reverted shutdown
  behaviour) then GREEN — see §5.

### C2 — Reboot DISARMED (define precisely; COMMAND GAP)
- **Predicate ("reboot DISARMED"):** after a host reboot, the bridge is **not** armed and submits **no**
  order. Because the first-start unit has `Restart=no` and **no `[Install]`** (it cannot auto-start at
  boot) and the steady profile is gated/inert/not-installed, the bridge cannot auto-start. A reboot
  also does **not** change mask state: from the current accepted state (active and unmasked), a plain
  reboot should leave the unit inactive and unmasked; a masked post-reboot state is valid only if a
  separately authorised pre-reboot step masks it first. In either case the safety predicate is
  **DISARMED-by-absence** (no process/listener/order), NOT an auto-restarted DISARMED service. Do **not**
  infer an auto-restart promise; do **not** yet label the absence of `[Install]`/auto-start as a
  product defect (Gap G1).
- **Canonical source:** `WPI_READINESS_RECORD_2026-08-01.md` §6 ("reboot DISARMED"); roadmap line 773
  ("survives reboot DISARMED"); ⛔ **round-2 qualification of the template half** — first-start
  template `2ce41e34…321b:…/systemd/mtc-bridge-first-start.service.template` (blob `c1823254…`,
  candidate-only; `Restart=no` **:55**, no `[Install]` section) and steady template
  `2ce41e34…321b:…/systemd/mtc-bridge-steady.service.template` (blob `121229ea…`, **ref-invariant**;
  `Restart=on-failure` **:52**, no `[Install]`). Both anchors underwrite G1's "cannot auto-start at
  boot" premise, which round 1 asserted from bare "templates".
- **Existing evidence:** template facts (A4); A-5 did **not** reboot the host.
- **Proposed method (NOT EXECUTED):** first preregister one of two distinct scenarios: (A) plain
  reboot from the current unmasked state, expecting inactive+unmasked; or (B) separately authorised
  stop+mask followed by reboot, expecting inactive+masked. On return, read-only assert the expected
  mask state plus no `bridge.app` writer, closed control port, and persisted DB state not ARMED.
  **COMMAND GAP:**
  `2ce41e34…321b:…/deploy/linux/verify.sh` is a pre-start **masked/unstarted-mode** verifier (its own
  comment at `…:240-242`) and is **not** the post-reboot instrument; a bounded post-reboot read-only
  subcheck procedure must be designed first. Note also that a post-reboot DISARMED assertion may
  additionally rely on the candidate's pinned start mode (§0.6): even if the unit were started, the
  template pin + `verify.sh:143-146` env-override rejection + `bridge/app.py:149` no-broker gate mean
  it would come up credential-free DISARMED with `arm_enabled=False`. That is candidate-only
  behaviour and must be cited as such.
- **Mutation class:** `mutating-host` (reboot). **Authority/budget:** requires explicit named lift +
  budget; **blocked**. **Output artifact:** post-reboot evidence log (NOT YET CREATED). **PASS:** unit
  expected preregistered mask state + no writer/listener + DB state not ARMED after reboot. **Failure
  disposition:** any writer, listener, ARMED state, or mask-state mismatch after reboot = STOP.

### C3 — SQLite WAL-consistent backup / verify / restore on a TEMPORARY COPY (never the active DB)
- **Predicate:** a WAL-consistent bundle is captured, verified, and **restored into a temporary copy**
  that re-derives the same invariants; the **active database is never destructively tested.**
- **Canonical source:** `2ce41e34…321b:IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py`
  (blob `26c077e650…` — **differs** from the documentation blob `aaa29182…`; the doc blob must not be
  used for line references); `2ce41e34…321b:IBKR_PAPER_BRIDGE/deploy/linux/COMMANDS.md` **Stage E at
  :116** (blob `3deeefc8…`, ref-invariant — ⛔ round-2: stage heading anchors are A :20, B :44,
  C :63, D :96, E :116, F :205, G :240); roadmap line 773; WPI §6 ("SQLite backup/restore and
  risk/history continuity").
- **Existing evidence (re-verified at the candidate):** `wal_state_bundle.py` is offline/read-only
  against source, uses the SQLite online-backup API `src.backup(dst)` (`…:801`) rather than copying
  the db/wal/shm trio, runs `PRAGMA integrity_check` / `PRAGMA foreign_key_check` on both ends
  (`…:405-411`, `:786-788`, `:821-823`, `:1116-1118`), re-derives sanitised invariants via public
  `collect_invariants` (`…:417`), and fails closed on sidecar presence (`…:814-816`, `:1157-1159`,
  `:1120-1121`), drift, or hash mismatch. **⛔ Subcommand surface (candidate-verified):** the CLI
  exposes exactly **two** subcommands under a required subparser (`…:1216`) — `create` (`…:1218`)
  and `verify` (`…:1232`). `--allow-live-source` is a `create` flag (`…:1223`; usage banner
  `…:48`). **There is no `restore` subcommand**, which is precisely why the restore-into-temp
  COMMAND GAP below is real. Test coverage: `test_bundle_never_contains_a_wal_shm_trio`
  (`2ce41e34…321b:tests/test_wal_state_bundle.py:856`), `test_invariants_preserve_risk_and_history`
  (`…:882`) — both exist at the candidate (A5, §4).
- **Proposed method (NOT EXECUTED):**
  1. Capture from a **quiesced/temp copy** (not the live trio): `wal_state_bundle.py create --source
     <temp-copy-of-bridge.db> --out-dir <bundle> > capture-report.json` (**never** `--allow-live-source`
     for a cutover/restore proof).
  2. Record `bundle_db_sha256` + `invariants_sha256` into a separately-held hash record.
  3. `wal_state_bundle.py verify --bundle-dir <bundle> --expect-bundle-sha256 <h>
     --expect-invariants-sha256 <h>`.
  4. Restore into a **second temp DB** and re-run `collect_invariants` to prove risk/history continuity
     (daily-loss, consecutive-loss, `risk_days`) — all on temporary copies; the production
     `/var/lib/mtc-bridge/bridge.db` is never overwritten by a test.
- **⚠ Prerequisite precision:** the cleanest capture is from a quiesced writer. Capturing from the
  **live running** bridge without `--allow-live-source` will (correctly) fail closed on drift. A
  live-source capture is a *warning*, not a cutover proof. The restore-validation must target a temp
  copy. **COMMAND GAP (confirmed at the candidate):** the tool exposes only `create` and `verify`, so
  the "restore into temp DB + re-verify" wrapper does not exist and must be authored locally (next
  unit). Step 4 below is therefore a *wrapper* around the public `collect_invariants`
  (`2ce41e34…321b:tools/wal_state_bundle.py:417`), not an existing subcommand.
- **Mutation class:** `mutating-host` (it touches the host DB path to obtain the temp copy; even a
  read-only online backup reads the live file under SQLite locking). **Authority/budget:** requires
  explicit named lift + budget; **blocked**. **Output artifact:** capture report + bundle + verify
  report + restore-into-temp report (NOT YET CREATED). **PASS:** `verdict=VALID`, invariants match the
  preregistered hashes, no sidecar. **Failure disposition:** drift/corruption/hash mismatch = exit 2 =
  STOP. **D026:** the existing `wal_state_bundle` tests are *existing* coverage, not new closure
  evidence for a *newly named* defect (§5).

### C4 — Rollback: stop+mask+zero-writers (no target) vs release-rebind (unmet prerequisite)
- **Predicate:** rollback stops and masks the service, preserves `/var/lib/mtc-bridge` state, and proves
  zero local writers; an optional release-rebind re-points the unit to a previously installed immutable
  release.
- **Canonical source (⛔ round-2 qualification — round 1 left both of these bare):**
  `2ce41e34…321b:IBKR_PAPER_BRIDGE/deploy/linux/rollback.sh`, blob
  `4b36674dcb1baa7c3b119cac98f8e6017b1f1566` (**ref-invariant**);
  `2ce41e34…321b:IBKR_PAPER_BRIDGE/deploy/linux/COMMANDS.md` **Stage G at :240** (blob `3deeefc8…`,
  ref-invariant); roadmap/WPI §6.
- **Existing evidence (with candidate anchors, round 2):** `rollback.sh` usage banner **:25-27**;
  flag parsing `--to-release-sha` **:44**, `--to-manifest-sha256` **:45**, `--state-manifest-file`
  **:46**, `--state-manifest-sha256` **:47**; the two hard requirements at **:57-58**
  (`"--state-manifest-file is required"`, `"--state-manifest-sha256 is required"`) — i.e. the
  accepted state-bundle manifest hash is mandatory; `systemctl stop` **:82** then `systemctl mask`
  **:86** (and **:153** on the rebind path); target-release manifest verification **:122-124**;
  `/etc/mtc-bridge/rollback_manifest.json` written from the path set at **:70**. It asserts no
  `bridge.app` writer and a closed control port and preserves state. The
  `--to-release-sha`/`--to-manifest-sha256` pair is **optional but paired** — the guard at **:65**
  (`"--to-release-sha and --to-manifest-sha256 must be supplied together"`) rejects one without the
  other; stop+mask works with neither.
- **⚠ Unmet prerequisite (Gap G3):** a meaningful **release-rebind** additionally requires an
  **already-installed previous immutable release**. The transition inventory shows **only** candidate
  `2ce41e34…321b` is installed (the old `ebada020…` install + venv are already absent). Therefore a
  prior-release rollback rebind **cannot be proven now** — its prerequisite is unmet. **Do not invent a
  target release or run rollback.**
- **Proposed method (NOT EXECUTED):**
  - *Stop+mask+zero-writers proof* (feasible once authorised): `rollback.sh --state-manifest-file <M>
    --state-manifest-sha256 <H>` with **no** `--to-*` flags; then read-only assert masked + no writer +
    state preserved. Requires the accepted state-bundle manifest hash (from C3) as a prerequisite.
  - *Release-rebind proof* (NOT feasible now): would need a second installed immutable release — absent.
- **Mutation class:** `mutating-host`. **Authority/budget:** requires KVM2-P4-08 authorisation +
  budget; **blocked**. **Output artifact:** rollback evidence log + `rollback_manifest.json` (NOT YET
  CREATED). **PASS (stop+mask):** masked, no `bridge.app` writer, port closed, state dir preserved,
  manifest recorded. **Failure disposition:** a surviving writer or state loss = STOP. **D026:** n/a
  (operational proof). **COMMAND GAP:** the stop+mask-only run-kit step (with the C3 manifest hash
  wired in) is not yet authored.

### C5 — Actual egress / TESTNET-only destinations / no mainnet / Telegram disposition (needs credentials/network authority → blocked)
- **Predicate:** observed runtime egress goes only to `api.hyperliquid-testnet.xyz` (and optionally
  `api.telegram.org`); **no** `api.hyperliquid.xyz` (mainnet) traffic; loopback-only `127.0.0.1:8790`.
- **Canonical source:** `SECURITY_BASELINE.md` §3 (egress inventory) — **⛔ governance/evidence
  artifact, ABSENT from the candidate** (§A3); it describes candidate analysis but is not candidate
  payload and must not be cited as candidate source. WPI §6.
- **Existing evidence:** **static inventory only** (A3): code selects `network="testnet"`
  (`2ce41e34…321b:IBKR_PAPER_BRIDGE/bridge/app.py:246`, inside `_build_broker`, which resolves
  credentials at `:244`); SDK `constants.TESTNET_API_URL`; notifier gated on both Telegram names
  resolving. A-8 proved the listener is loopback-only. A-9 proved zero secret-signature hits.
- **⛔ CORRECTED premise — the deployed start mode constructs NO broker at all.** The original text
  read: *"source constructs the TESTNET broker before any human ARM transition."* At the candidate
  that holds **only** for a non-credential-free `start_runtime` launch. In the mode the staging host
  actually runs, `2ce41e34…321b:IBKR_PAPER_BRIDGE/bridge/app.py:149`
  (`if start_runtime and not credential_free_disarmed:`) gates broker construction off entirely:
  **no credential resolution, no `network="testnet"` selection, no exchange connection,
  `arm_enabled=False`** (`:138-147`). This behaviour is **absent from the documentation-branch
  `bridge/app.py` blob** and so was invisible to the authoring session.
- **⚠ Hard blocker (tightened, not relaxed):** a runtime egress capture **cannot be obtained from the
  current staging runtime at any authority level** — not because ARM is missing, but because the
  deployed start mode builds no broker and therefore emits no broker egress. An authorised future
  capture would require a **different, separately authorised start mode** *plus* credential and
  broker/TESTNET network authority — none of which exists now (§1). The Lead's standing correction
  that such a capture **does not require ARM** remains valid; ARM remains forbidden, and any future
  capture must remain DISARMED.
- **Proposed method (NOT EXECUTED; blocked on credential + broker/TESTNET network authority that is
  itself out of scope here):** authorised **DISARMED-only** TESTNET capture of DNS/HTTPS/WebSocket
  destinations + certificate inspection + explicit no-mainnet/no-order assertion; separately confirm
  Telegram enabled/disabled disposition without recording secret values. **COMMAND GAP** until the
  separate credential/network authority exists — this is not a current-unit item.
- **Mutation class:** would be `mutating-host`/network and requires credentials. **Authority/budget:**
  **not authorised** (credentials/ARM/TESTNET). **Output artifact:** egress capture (NOT YET CREATED,
  not currently authorisable). **PASS:** TESTNET-only + no-mainnet + loopback-only + Telegram
  disposition recorded. **Failure disposition:** any mainnet attempt = hard BLOCK.

---

## Group D — Audit 2 (canonical four-auditor contract from current `AGENTS.md`)

### D1 — Four-auditor contract (NOT the older plan wording)
- **Predicate:** Audit 2 is a Gate-5 audit conducted under the **current canonical audit roster**
  (`AGENTS.md` §CANONICAL AUDIT ROSTER), **not** the older plan §1020 Codex-only wording
  ("Codex `gpt-5.6-sol` xhigh, independent session").
- **Canonical source:** `AGENTS.md` §CANONICAL AUDIT ROSTER + §"Four-auditor acceptance rule (D025)".
- **Contract (exact):**
  - **Auditor 1 — Claude:** `claude-opus-5`, effort `xhigh`, always; fresh independent session.
  - **Auditor 2 — Codex:** `gpt-5.6-sol`, effort `high` (ordinary G5) or `xhigh` (protected/re-audit);
    fresh independent session.
  - **Auditor 3 — DeepSeek V4 Flash:** `cline-pass/deepseek-v4-flash` via Cline CLI (D025-authorised);
    read-only worktree + cleanliness proof.
  - **Auditor 4 — GLM-5.2:** GLM-5.2 via Z.AI Coding Plan (D025-authorised); same isolation.
  - **Acceptance floor (D025 rule 3):** accepting verdicts from **both flagships**
    (`claude-opus-5` xhigh **and** `gpt-5.6-sol` xhigh) **plus no unresolved reproduced required
    finding from any auditor.** Auditors 3–4 add detection, not an unexecuted-read veto.
  - **Non-execution → BLOCK (rule 1):** an auditor that cannot execute the mandated test suite must
    return BLOCK; non-execution is never acceptance (known GLM-5.2 failure mode recorded).
  - **Binding findings (rule 2):** a required finding from any auditor is binding *after the Lead
    reproduces it on real source*; unreproduced findings are recorded with evidence, not dropped.
  - **Repair bound:** maximum 3 repair/re-audit rounds; then STOP and report.
- **Existing evidence:** roster is live in `AGENTS.md`; D025 ratified 2026-08-01.
- **Remaining evidence:** the actual Audit-2 round on the frozen WP-L/WP-I checkpoint artifact.
- **Proposed method (NOT EXECUTED):** freeze the exact checkpoint SHA/artifact after WP-L Phase 2 +
  WP-I staging verification; run the four-auditor Gate-5 on it; Lead reproduces any required finding;
  accept only on the D025 floor.
- **Mutation class:** `audit`. **Authority/budget:** host execution for WP-L/WP-I is a prerequisite and
  is budget-blocked; the audit itself draws on WP-R (§20). **Output artifact:** four independent audit
  verdicts + Lead reproduction notes (NOT YET CREATED). **PASS:** D025 floor met, no unresolved
  reproduced required finding. **Failure disposition:** REQUEST_CHANGES/BLOCK → repair loop (≤3), else
  STOP. **D026:** auditors must verify each new test's RED-then-GREEN, not accept the claim (§5).

### D2 — Timing / sequence / scope
- **Predicate:** Audit 2 runs **immediately after** WP-L Phase 2 + WP-I staging verification and
  **before** WP-A; scope = Linux-port + staging acceptance of the frozen artifact.
- **Canonical source:** roadmap §23a step 4 (line 973), §"Audit 2" (lines 863, 1199); runbook :137.
- **Existing evidence:** sequence documented (§0.1). **Remaining:** WP-L Phase 2 + WP-I staging evidence
  not yet captured (host execution blocked).
- **Proposed method:** none until the prerequisite evidence exists.
- **Mutation class:** `audit`. **Authority/budget:** blocked upstream. **Output artifact:** as D1.
  **PASS:** ordered correctly, accepting verdict before WP-A begins. **Failure disposition:** starting
  WP-A before an accepting Audit 2 = sequence violation (STOP).

---

## Group E — WP-A targeted Ubuntu verification (on the retained host, before discard)

WP-A executes the DISARMED restart / reconnect / stale-data / persistence invariants on the retained
staging host and captures evidence **before** the host is discarded (roadmap §23a step 5–6). Each item
below is a **mutating host action** (it stops/starts the service) and is **NOT EXECUTED**. The test
symbols are *existing source coverage* that WP-A must exercise on Ubuntu — they are **not** new closure
evidence for a newly named defect (§5).

> **⛔ Provenance note for all of Group E.** Every "(source-verified)" test citation below was
> originally resolved against the documentation checkout and is corrected here to the **frozen
> candidate** `2ce41e34…321b`. All 11 symbols exist at the candidate; see the corrected §4 table for
> the authoritative `path:line` values.

### E1 — DISARMED restart invariant (I-R1)
- **Predicate:** restart while flat + DISARMED → starts DISARMED, no order submitted.
- **Canonical source:** `WP0_SCOPE_BASELINE_RECORD_2026-07-31.md` I-R1 (line 363);
  `2ce41e34…321b:IBKR_PAPER_BRIDGE/bridge/app.py` forces DISARMED unless KILLED (candidate blob
  `572c4178…`).
- **Existing evidence:** code+test COVERED statically; A-6 empty-broker startup. **Remaining:** Ubuntu
  execution. **⛔ Reinforcement (candidate-only):** the deployed start mode makes "starts DISARMED"
  structural rather than incidental — `bridge/app.py:138-147` pins `arm_enabled=False` and `:149`
  builds no broker (§0.6).
- **Test symbol (candidate-verified):**
  `2ce41e34…321b:IBKR_PAPER_BRIDGE/tests/test_interim_risk_wiring.py:333::test_gates_persist_across_restart`.
- **Proposed method (NOT EXECUTED):** authorised single restart on the retained host; assert DISARMED
  + no order via `/api/status`. **Mutation class:** `mutating-host`. **Authority/budget:** blocked.
  **PASS:** DISARMED, zero orders. **Failure:** armed state or any order = STOP (candidate repair).
  **D026:** existing test; not new closure evidence.

### E2 — killed/disarmed persistence across restart (I-R2; **all three symbols exist**)
- **Predicate:** killed/disarmed state persists across restart.
- **Canonical source:** WP0 I-R2 (line 364).
- **Existing evidence:** code+test COVERED statically. **⛔ CORRECTED — the former "stale node"
  warning is WITHDRAWN.** I-R2 cites three symbols and **all three exist at the frozen candidate**,
  including `test_kill_restart_after_request_commit_keeps_killed_and_resumes_once` at
  `2ce41e34…321b:IBKR_PAPER_BRIDGE/tests/test_partial_fill_protection.py:2765`. The earlier "absent"
  reading came from the divergent documentation checkout. **WP0 line 364 is correct as written; do
  not edit it, and do not refresh or delete the citation.** Gap G4 is withdrawn.
- **Test symbols (candidate-verified — all three):**
  `2ce41e34…321b:IBKR_PAPER_BRIDGE/tests/test_api.py:69::test_kill_persists_across_restart`,
  `2ce41e34…321b:IBKR_PAPER_BRIDGE/tests/test_window_state.py:82::test_killed_alive_is_interrupted`,
  `2ce41e34…321b:IBKR_PAPER_BRIDGE/tests/test_partial_fill_protection.py:2765::test_kill_restart_after_request_commit_keeps_killed_and_resumes_once`.
- **Proposed method (NOT EXECUTED):** restart under a killed/disarmed state; assert persistence.
  **Mutation class:** `mutating-host`. **Authority/budget:** blocked. **PASS:** state persists.
  **Failure:** state reset = STOP. **D026:** existing tests; not new closure evidence.

### E3 — DB state-file integrity across restart (I-R3)
- **Predicate:** the SQLite state file remains integrity-clean and risk/history-invariant across
  restart.
- **Canonical source:** WP0 I-R3 (line 365);
  `2ce41e34…321b:IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py` (blob `26c077e650…`).
- **Test symbols (candidate-verified):**
  `2ce41e34…321b:IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py:856::test_bundle_never_contains_a_wal_shm_trio`,
  `2ce41e34…321b:IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py:882::test_invariants_preserve_risk_and_history`.
- **Proposed method (NOT EXECUTED):** restart, then `wal_state_bundle` capture+verify on a temp copy
  (C3 method). **Mutation class:** `mutating-host`. **Authority/budget:** blocked. **PASS:** integrity
  ok + invariants stable. **Failure:** drift = STOP.

### E4 — Reconnect dedupes to one order
- **Predicate:** a disconnect/reconnect does not duplicate an in-flight order.
- **Canonical source:** WP0 reconciliation map; A-6 boundary.
- **Test symbol (candidate-verified):**
  `2ce41e34…321b:IBKR_PAPER_BRIDGE/tests/test_p1_failure_drills.py:16::test_drill_disconnect_reconnect_dedupes_to_one_order`.
- **⚠ A-6 boundary (Gap G5):** A-6 asserted empty-broker startup only; it does **not** prove
  queue-drain-under-load or full reconcile (schema-4 disables full reconcile). WP-A must exercise real
  reconnect/queue/full-reconcile predicates.
- **Proposed method (NOT EXECUTED):** authorised reconnect drill; assert exactly one order. **Mutation
  class:** `mutating-host`. **Authority/budget:** blocked. **PASS:** one order. **Failure:** duplicate =
  STOP.

### E5 — Stale-data auto-disarm
- **Predicate:** stale market data triggers exactly one auto-disarm.
- **Canonical source:** WP0 map.
- **Test symbols (candidate-verified):**
  `2ce41e34…321b:IBKR_PAPER_BRIDGE/tests/test_p1_failure_drills.py:87::test_drill_data_stale_auto_disarms`,
  `2ce41e34…321b:IBKR_PAPER_BRIDGE/tests/test_bars.py:27::test_data_stale_emits_and_disarms_once`.
- **Proposed method (NOT EXECUTED):** authorised stale-data drill; assert one disarm. **Mutation
  class:** `mutating-host`. **Authority/budget:** blocked. **PASS:** one disarm. **Failure:** none or
  many = STOP.

### E6 — WebSocket death triggers auto-reconnect
- **Predicate:** a feed/WebSocket death triggers auto-reconnect (not silent failure).
- **Canonical source:** WP0 map.
- **Test symbol (candidate-verified):**
  `2ce41e34…321b:IBKR_PAPER_BRIDGE/tests/test_p1_failure_drills.py:319::test_drill_ws_death_triggers_auto_reconnect`.
- **Proposed method (NOT EXECUTED):** authorised ws-death drill; assert reconnect. **Mutation class:**
  `mutating-host`. **Authority/budget:** blocked. **PASS:** reconnect observed. **Failure:** no
  reconnect = STOP.

### E7 — Active recovery suppresses ordinary reconcile repair
- **Predicate:** while an active partial-fill recovery is in progress, ordinary reconcile repair is
  suppressed.
- **Canonical source:** WP0 map.
- **Test symbol (candidate-verified):**
  `2ce41e34…321b:IBKR_PAPER_BRIDGE/tests/test_partial_fill_protection.py:1871::test_active_recovery_suppresses_ordinary_reconcile_repair`.
- **Proposed method (NOT EXECUTED):** authorised recovery drill; assert suppression. **Mutation class:**
  `mutating-host`. **Authority/budget:** blocked. **PASS:** reconcile repair suppressed during active
  recovery. **Failure:** spurious repair = STOP.

### E8 — SIGTERM clean shutdown (overlaps C1 / I-R4)
- **Predicate / status:** as C1 — OPEN predicate. WP-A must capture SIGTERM evidence alongside the
  restart invariants. **COMMAND GAP** for the post-stop "no dangling state" verifier.

---

## 3. Gaps & contradictions (explicitly recorded)

- **G1 — reboot/auto-start is not a promise; no product defect yet.** The first-start unit is active
  and unmasked now but has `Restart=no` and **no `[Install]`** (cannot auto-start at boot); the steady
  profile is gated, inert, not installed, and **itself has no `[Install]`**. Reboot preserves rather
  than creates mask state. Therefore "reboot DISARMED" must be **defined precisely** before execution
  (C2): plain reboot from the current state expects inactive+unmasked, whereas inactive+masked requires
  a separately authorised pre-reboot mask step. Both are DISARMED-by-absence only if no
  process/listener/order exists and persisted DB state is not ARMED. Do not infer an auto-restart
  promise, and do not yet label the missing `[Install]`/auto-start as a product defect.
- **G2 — full `verify.sh` is a pre-start verifier and will fail post-start.** ✅ **Conclusion stands;
  line citations corrected to the candidate.** At
  `2ce41e34…321b:IBKR_PAPER_BRIDGE/deploy/linux/verify.sh` (blob `5cfefd7092…`), §6/§8 fails if the
  unit is ACTIVE ("first-start unit is ACTIVE; it must not be running before KVM2-P4-07",
  **lines 213–214**; ⛔ was "207–211"), fails if any `bridge.app` writer exists (**lines 243–247**;
  ⛔ was "237–241"), and asserts the control port **closed** (**line 248**; ⛔ was "242"); its own
  comment (**lines 240–242**; ⛔ was "234–236") states it is the *masked/unstarted* mode only —
  *"this mode requires both zero writer processes and a completely closed port, including
  loopback."* It also asserts the unit is **masked** (**lines 206–211**), which post-Gate-A it is
  not. After Gate A unmasked and started the service, a full `verify.sh` run will **intentionally
  fail**. **Do not prescribe it in the current state.** Use the bounded read-only subchecks of
  Group B (or design a missing post-start verifier) — `COMMANDS.md` Stage F (blob `3deeefc8…`,
  ref-invariant) states the mask assertion is intentionally no longer applicable post-start.
- **G3 — rollback rebind has an unmet prerequisite.** ✅ **Conclusion stands; citation qualified in
  round 2.** `2ce41e34…321b:IBKR_PAPER_BRIDGE/deploy/linux/rollback.sh` (blob `4b36674d…`,
  **ref-invariant**) can stop+mask without a target
  (requires the accepted state-manifest hash, **:57-58**) but **mutates service state** (`systemctl
  stop` **:82**, `systemctl mask` **:86**); a meaningful release-rebind
  additionally requires an **already-installed previous immutable release**, and only candidate
  `2ce41e34…321b` is installed (old `ebada020…` install + venv already absent). A prior-release rollback
  proof has an **unmet prerequisite**. Do not invent a target or run rollback.
- **~~G4 — stale evidence-map node.~~ ⛔ WITHDRAWN 2026-08-09 — the gap does not exist.** The
  original claim was: *`WP0_SCOPE_BASELINE_RECORD_2026-07-31.md` references
  `test_kill_restart_after_request_commit_keeps_killed_and_resumes_once` (lines 308, 364/I-R2), but
  that symbol is absent from current source.* **That is false for the frozen, deployed candidate.**
  The symbol exists at
  `2ce41e34…321b:IBKR_PAPER_BRIDGE/tests/test_partial_fill_protection.py:2765`:
  ```
  $ git grep -n test_kill_restart_after_request_commit_keeps_killed_and_resumes_once \
        2ce41e34bceb599d80af24c5c33d835820ec321b -- IBKR_PAPER_BRIDGE/tests
  2ce41e34…321b:IBKR_PAPER_BRIDGE/tests/test_partial_fill_protection.py:2765:def test_kill_restart_after_request_commit_keeps_killed_and_resumes_once(
  ```
  It is absent **only** from the divergent documentation checkout `851d2aa5`, which is what the
  authoring session searched. **Consequences:**
  - **WP0 lines 308 and 364 are CORRECT as written. The proposed WP0 deletion is CANCELLED.
    `WP0_SCOPE_BASELINE_RECORD_2026-07-31.md` must not be edited on the strength of this claim.**
  - No replacement symbol is needed; nothing is to be invented.
  - There is **no** source-map refresh item, and **no** product defect. All three I-R2 symbols exist.
  - **G4 is replaced by a new gap, G8 (below):** the real defect was documentation provenance.
- **G5 — A-5/A-6 scope limits.** A-5 proved SIGKILL + restart + state integrity + DISARMED, **not**
  graceful SIGTERM and **not** host reboot (I-R4 OPEN). A-6 asserted empty-broker startup only; it does
  **not** prove queue-drain-under-load or full reconcile (schema-4 disables full reconcile).
- **G6 — README historical "never executed" text is stale after Gate A.** ✅ **Conclusion stands;
  line citations corrected.** `2ce41e34…321b:IBKR_PAPER_BRIDGE/deploy/linux/README.md` states
  `Status: **PREPARATION ONLY — nothing here has been executed on any host.**` (**line 4**) and
  `These assets have **never been executed**, on KVM2 or anywhere else…` (**lines 123–125**;
  ⛔ was cited as "118–120", a documentation-checkout offset). After Gate A A-0..A-9, the candidate
  **has** been installed and started on the staging host. **Cite those README lines only as
  historical**, not as current status.
- **G7 — exact 50-hour balance NOT REPRODUCIBLE; all host execution blocked.** The current exact
  used/remaining balance is not reproducible (`GATE_A_50H_LEDGER_RECONSTRUCTION_2026-08-09.md`,
  state 5). The broader standing authorisation does **not** override the narrower current
  budget/safety hold and does **not** authorise credentials, broker, ARM/orders, TESTNET/mainnet, or
  economic action. No host execution may be authorised or performed in this unit.
- **⛔ G8 (NEW, replaces G4) — documentation/candidate provenance split is not enforced by the
  workflow.** The documentation/governance branch and the frozen candidate are **divergent**
  (merge base `4d2228cf…`; `git diff --stat` shows the doc tree missing ~14.4k lines of product and
  test code relative to the candidate, including all of `tests/test_credential_free_disarmed.py`).
  Nothing in the post-Gate workflow prevented an author from reading product files out of the
  documentation checkout and recording them as candidate facts — which is exactly what produced the
  false G4, the wrong line anchors throughout, and the complete omission of the credential-free
  DISARMED start-mode protections (§0.6). **Mitigation (binding from now on):** post-Gate records
  must cite product/deploy/runtime/test/tool facts as `2ce41e34…321b:<path>:<line>`, obtained by
  `git show`/`git grep` at the candidate or from installed-host / Gate-A evidence explicitly tied to
  it. A bare `<path>:<line>` in a post-Gate record is to be treated as **unverified**. Full analysis:
  `GATE_A_POST_GATE_PROVENANCE_REPAIR_2026-08-09.md`.
- **⛔ G9 (NEW, round 2) — hash provenance is not stated, and the working tree is not the payload.**
  The G8 mitigation fixed *path* provenance but said nothing about *hash* provenance, and the same
  class of error immediately recurred one level down: a hash of the Windows worktree file
  (`40873556…`, CRLF, 119 274 B) was recorded as the frozen candidate's lock hash and declared
  exempt from re-derivation on the strength of blob identity. This repo is `core.autocrlf=true` with
  `* text=auto` (`git ls-files --eol` → `i/lf  w/crlf`), and **this `requirements.lock` checkout
  differs from the committed and deployed bytes because line-ending conversion is proven for it;
  other text files subject to that conversion may differ too, so candidate content hashes must be
  derived from Git blob/archive bytes rather than assumed from a converted worktree**. The
  candidate's own packager knows this — it pins
  `-c core.autocrlf=false -c core.eol=lf` for `git archive`
  (`2ce41e34…321b:…/deploy/linux/package.sh:78-83`, comment at `:79-81`). The error was live, not
  cosmetic: `install.sh:401,416` records the installed lock hash in
  `/etc/mtc-bridge/install_manifest.json` and `verify.sh:82-91` re-verifies the release tree against
  `RELEASE_SHA256SUMS`, so preregistering the CRLF value would have raised a **fabricated lock-drift
  STOP against a host that matches the payload**. **Mitigation (binding from now on):** every hash in
  a post-Gate record must name its input using exactly one of *Git blob object ID (SHA-1)* / *raw blob
  content SHA-256 (LF)* / *worktree checkout SHA-256*; content hashes are derived with
  `git cat-file blob <id> | sha256sum`, never by hashing a Windows checkout; and "the blob is
  ref-invariant" licences reuse of the **blob ID**, never of an unverified number attached to it.
  Values: §4b. Full analysis: `GATE_A_POST_GATE_PROVENANCE_REPAIR_2026-08-09.md` §2.7.
- **⛔ G10 (NEW, round 3) — a derived expectation was recorded as an observed host fact.** G8 fixed
  *path* provenance and G9 fixed *hash-input* provenance; neither constrained **epistemic** provenance,
  and the same error recurred one level further out. Rounds 1–2 wrote that the lock installed on
  `GATEA-STAGING` "therefore hashes to `a1881296…`" and that
  `/etc/mtc-bridge/install_manifest.json` → `requirements_lock_sha256` carries that value. The
  derivation is sound — LF-pinned export (`package.sh:78-83`) → hashed at install (`install.sh:401`) →
  recorded (`:416`) → re-verified against `RELEASE_SHA256SUMS` (`verify.sh:82-91`) — but **no located
  Gate-A evidence records either observed value** (repair-record §2.7g). Recording it as settled turns
  an untested predicate into apparent evidence, and pre-commits the diagnosis of any future mismatch.
  **Mitigation (binding from now on):** every hash in a post-Gate record carries **two** labels —
  *what was hashed* (G9) **and** *expected-from-source* vs *observed-on-host*. An expectation is
  written as "expected …, to be compared against"; an observation requires a captured command and its
  output. Where the observation has not been made, the record says so and carries it as an open
  predicate (B1a). Full analysis: `GATE_A_POST_GATE_PROVENANCE_REPAIR_2026-08-09.md` §2.7(g), §3.

---

## 4. Target tests — exact map (⛔ CORRECTED: verified at the frozen candidate; **all 11 exist**)

> The original table was resolved against the documentation checkout `851d2aa5`. Every line number
> in it — and its "ABSENT" row 11 — was a fact about the wrong tree. The table below is
> re-derived by `git grep` at `2ce41e34bceb599d80af24c5c33d835820ec321b`. Paths are relative to
> `IBKR_PAPER_BRIDGE/`. The final column preserves the superseded doc-ref value so the contamination
> signature stays auditable.

| # | Symbol | Candidate `2ce41e34…321b` path:line | Status | Superseded doc-ref value |
|---|---|---|---|---|
| 1 | `test_gates_persist_across_restart` | `tests/test_interim_risk_wiring.py:333` | **EXISTS** → WP-A E1/I-R1 | 333 (coincides) |
| 2 | `test_kill_persists_across_restart` | `tests/test_api.py:69` | **EXISTS** → WP-A E2/I-R2 | ~~61~~ |
| 3 | `test_killed_alive_is_interrupted` | `tests/test_window_state.py:82` | **EXISTS** → WP-A E2/I-R2 | 82 (coincides) |
| 4 | `test_bundle_never_contains_a_wal_shm_trio` | `tests/test_wal_state_bundle.py:856` | **EXISTS** → WP-A E3/I-R3, C3 | ~~289~~ |
| 5 | `test_invariants_preserve_risk_and_history` | `tests/test_wal_state_bundle.py:882` | **EXISTS** → WP-A E3/I-R3, C3 | ~~315~~ |
| 6 | `test_drill_disconnect_reconnect_dedupes_to_one_order` | `tests/test_p1_failure_drills.py:16` | **EXISTS** → WP-A E4 | 16 (coincides) |
| 7 | `test_drill_data_stale_auto_disarms` | `tests/test_p1_failure_drills.py:87` | **EXISTS** → WP-A E5 | ~~40~~ |
| 8 | `test_drill_ws_death_triggers_auto_reconnect` | `tests/test_p1_failure_drills.py:319` | **EXISTS** → WP-A E6 | ~~272~~ |
| 9 | `test_data_stale_emits_and_disarms_once` | `tests/test_bars.py:27` | **EXISTS** → WP-A E5 | 27 (coincides) |
| 10 | `test_active_recovery_suppresses_ordinary_reconcile_repair` | `tests/test_partial_fill_protection.py:1871` | **EXISTS** → WP-A E7 | ~~1867~~ |
| 11 | `test_kill_restart_after_request_commit_keeps_killed_and_resumes_once` | `tests/test_partial_fill_protection.py:2765` | **EXISTS** → WP-A E2/I-R2 | ~~"— ABSENT (stale node)"~~ |

**11 / 11 EXIST at the frozen, deployed candidate. There is no stale evidence-map node and no
missing symbol. `WP0_SCOPE_BASELINE_RECORD_2026-07-31.md` lines 308 and 364 are correct and must not
be edited.**

**D026 caveat.** These rows prove *existence* by `git grep`, not execution. No test was run in the
authoring unit or in either repair unit. Existence is not closure — see §5.

**⛔ Round-2 precision — "(coincides)" is two different things.** Four rows show the same line number
on both refs, but only three of them are *structurally* safe: their **files** are byte-identical
across the refs. The fourth agreed by luck.

| # | File | Blob status | Why the numbers agree |
|---|---|---|---|
| 1 | `tests/test_interim_risk_wiring.py` | **ref-invariant** `29214adae7…` | Structural — same bytes on both refs; `:333` cannot disagree |
| 3 | `tests/test_window_state.py` | **ref-invariant** `e9d3912958…` | Structural (`:82`) |
| 9 | `tests/test_bars.py` | **ref-invariant** `17453080ed…` | Structural (`:27`) |
| 6 | `tests/test_p1_failure_drills.py` | **differs** (`9e50c1b51c…` vs `f2e3a32171…`) | **Coincidence only** — divergence in this file starts after line 16; rows 7 and 8 in the *same file* shift by 47 |

Do not generalise from a matching line number to a matching file. Rows 1, 3 and 9 were harmless to
read from the documentation checkout; row 6 must still be treated as candidate-sourced.

### 4a. Corrected `verify.sh` section map (candidate `2ce41e34…321b`, blob `5cfefd7092…`)

Every `verify.sh` line number originally in this document was a documentation-checkout offset.
Use only the candidate column below.

| Region | **Candidate lines (use these)** | ~~Superseded doc lines~~ |
|---|---|---|
| §1 service identity | 54–76 | — |
| §2 immutable release tree | 77–102 | ~~78–135 (as "§2/§4")~~ |
| §3 hash-locked venv | 103–122 | ~~104–121~~ |
| §4 writable state / log / config | 123–136 | ~~(folded into 78–135)~~ |
| §5 secret hygiene | 137–154 | — |
| — start-mode env-override rejection | **143–146** | *(omitted originally)* |
| §6 unit state | 155–222 | ~~150–199~~ |
| — required unit needle list | 160–171 | ~~155–165~~ |
| — start-mode needle | **171** | *(omitted originally)* |
| — template byte-compare (`cmp`) | 186–195 | ~~182–190~~ |
| — `[Install]` absent check | 197–201 | — |
| — masked assertion | 206–211 | — |
| — ACTIVE ⇒ fail | 213–214 | ~~207–211~~ |
| §7 steady profile must be absent | 223–232 | — |
| §8 logs / rotation / control plane | 233–251 | ~~233–244~~ |
| — masked/unstarted-mode comment | 240–242 | ~~234–236~~ |
| — zero `bridge.app` writer | 243–247 | ~~237–241~~ |
| — control port closed | 248 | ~~242~~ |
| §9 summary | 252– | — |

### 4b. Blob ledger and lock identity (⛔ NEW, round 2)

Every product/deploy/tool path this matrix cites, with its blob on both sides. Round 1's superseding
block left six of these as an unresolved "differ / differ"; they are resolved here so the table is
checkable rather than asserted. Documentation column verified identical at `851d2aa5` **and** the
current HEAD `f8a6bc0f` (the intervening commits are documentation-only).

**Ref-invariant (nine) — either citation valid; the provenance defect could not have corrupted these:**

| Path (under `IBKR_PAPER_BRIDGE/`) | Blob (both refs) |
|---|---|
| `requirements.lock` | `47f53fa227bf0f18b9bf9bd77e060d8856961728` |
| `deploy/linux/verify_lock.py` | `8ccd6f329154422a85b8e7663e6a079dbd47b4fd` |
| `deploy/linux/rollback.sh` | `4b36674dcb1baa7c3b119cac98f8e6017b1f1566` |
| `deploy/linux/COMMANDS.md` | `3deeefc8da2984d5220482f065e569b74874847a` |
| `deploy/linux/install.sh` | `40983e5a675728dbdefe68e46dfe6d055d2841a1` |
| `deploy/linux/systemd/mtc-bridge-steady.service.template` | `121229ea5b0fc8c67c8bc5e49d4ffcc3f25f4fba` |
| `tests/test_bars.py` | `17453080ed330ed2f4cc72bbe5e245164420a2ad` |
| `tests/test_interim_risk_wiring.py` | `29214adae7006ac6b60bf53240b2e507f3ad858d` |
| `tests/test_window_state.py` | `e9d39129587f7d8e2b26e2f3d5221b7a02d4b106` |

**Candidate-only (twelve) — cite `2ce41e34…321b` and nothing else:**

| Path (under `IBKR_PAPER_BRIDGE/`) | Candidate `2ce41e34…321b` | Documentation |
|---|---|---|
| `deploy/linux/verify.sh` | `5cfefd709202ff504ae7b7fc3504b8c0b00900b6` | `bce1f0e23e63f9a8d168c751aec99ac84d1334c7` |
| `deploy/linux/systemd/mtc-bridge-first-start.service.template` | `c18232549d96aa200d8c7f796e64de743288940c` | `b175ced7f36df52ad2e55532264f36f49fdc8281` |
| `deploy/linux/README.md` | `f3f1d75e7e4369609cd0eb299466b2ceb62a0a16` | `666b79d834f50433cd0cba7c88224fb674fdbb56` |
| `deploy/linux/env/mtc-bridge.env.template` | `c03d6e47ab57c00ef95f4122607fc7ba88119e35` | `fbf8cb833c58a30c8262f14027512bbfdedae3e8` |
| `deploy/linux/lib/common.sh` | `db11010a24edfbb96ba80ec1fbe1db3ff29193c9` | `7d5aa166ac2f3b703e9543a42d49564c66e34002` |
| `deploy/linux/package.sh` | `add6478d33cce8d929d58f895407abe01d51da20` | `150c18c36447ecc122332a992581ca6d9bba4007` |
| `tools/wal_state_bundle.py` | `26c077e650ab88ba2086efa3a80790769bc055b1` | `aaa2918229a1367ebf1fb6a458a4e65673dc180e` |
| `bridge/app.py` | `572c4178fe804da17601eefd898027e9261492e6` | `6d0abc6351a0d20aef324fb00b936c0f189d036f` |
| `tests/test_partial_fill_protection.py` | `7b0b9ea36dd8b15108f6befcbcb00015ed2f51fb` | `42c55c09afc93edb4d7364008da4b702176721c3` |
| `tests/test_api.py` | `40d31925ac93c4bfe13a877f060b5abaf6c0cd6e` | `d9da63e7f66afd6db7e24eef774296dce9487c16` |
| `tests/test_wal_state_bundle.py` | `07de7b206f56c7442c3ea07ec160dc7ef2497415` | `edc02108c9829aa7b2409fd3eca774d00cb1b5b2` |
| `tests/test_p1_failure_drills.py` | `9e50c1b51cd6d60967f5481adfeda9779815efd9` | `f2e3a32171c12c53bd31bba35dbcc691417b53b6` |

**Presence asymmetry:** `deploy/linux/SECURITY_BASELINE.md` — **ABSENT** at the candidate, present on
the documentation branch (`8db2e6dd7e782c96f585f6672c4489c4ce5c1488`, unchanged at `f8a6bc0f`);
`tests/test_credential_free_disarmed.py` — present at the candidate
(`ce0ae7c24f795dc8e5d56bf7cca82e1a75351402`), **ABSENT** on the documentation branch.

**Lock identity — the one value the whole matrix depends on:**

| Kind | Value | Use |
|---|---|---|
| Git blob object ID (SHA-1) | `47f53fa227bf0f18b9bf9bd77e060d8856961728` | Ref identity. Same at `2ce41e34…321b`, `851d2aa5`, `f8a6bc0f`, `637307e8`. **Not** a content hash |
| Raw blob content SHA-256 (LF, 117 762 B) | `a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e` | ✅ **Preregister this — as the *expected* value.** Source-derived: the committed bytes, hence the bytes the LF-pinned archive ships, hence the value `RELEASE_SHA256SUMS` and `install_manifest.json` → `requirements_lock_sha256` are **expected** to carry |
| Worktree checkout SHA-256 (CRLF, 119 274 B) | `40873556a7f4586d77f165b985863138c9fc95b095da64ac52456b8c49098ec3` | ⛔ **Never cite.** Local Windows artifact; `119 274 − 117 762 = 1 512` = the blob's line count |
| ⛔ **Observed installed-host value** (round 3) — `sha256sum` of the installed lock, and the host manifest's `requirements_lock_sha256` | **NOT IN EVIDENCE** | ⛔ **Open predicate, not a fact.** Never captured in any located record (repair-record §2.7g). Closable by one authorised read-only host read (B1a); blocked by §1 |

Derivation of the expected value: `git cat-file blob 47f53fa227bf0f18b9bf9bd77e060d8856961728 |
sha256sum`. Full reproduction, the operational chain (`package.sh:78-83` → `install.sh:401,416` →
`verify.sh:82-91`), and the enumeration of what the Gate-A evidence does **not** contain are in
`GATE_A_POST_GATE_PROVENANCE_REPAIR_2026-08-09.md` §2.7 and §2.7(g).

---

## 5. D026 — falsified-test rule (binds this matrix)

A regression test offered as proof that a **specifically named** defect is closed is **not closure
evidence** until it has been shown **RED** against the exact pre-fix/reverted behaviour (or an
equivalent deliberate falsification) **and GREEN** with the fix in place, with the commands and real
output recorded (`AGENTS.md` §D026, owner-ratified 2026-08-03).

- **Existing tests are not automatically new D026 evidence** for a newly named defect. The **eleven**
  symbols in §4 (⛔ was "ten") are *existing coverage*; citing them does not close a new defect.
- **⛔ Existence ≠ execution.** The §4 map was produced by `git grep` at the candidate. **No test was
  run** in the authoring unit or in the repair unit. A `git grep` hit is weaker than a D026 RED-then-
  GREEN demonstration and weaker even than a passing run; it proves only that the symbol is present
  in the deployed candidate's source.
- **Any new regression test proposed as closure** for a post-Gate finding (e.g., a SIGTERM-shutdown
  test for I-R4) must be demonstrated RED-then-GREEN. If safe reversion is impractical, an independent
  mutation/falsification is required; otherwise the test is classified **supplemental — not closure**.
- **Binds implementers and auditors.** Applies with particular force to protected Bridge /
  persistence / concurrency / safety surfaces.
- Does **not** require mutating every unrelated legacy test.

---

## 6. Command-block safety contract

- Every command block above is **NOT EXECUTED** and is safe-by-construction (read-only, or a
  documented mutation gated behind its own authority).
- **No secret value** is embedded or printed; the env file is referenced by mode/owner only.
- **No evidence directory is claimed to exist** unless an existing path is cited (the local preserved
  copies under `C:\WPI_ARTIFACTS\…` and the remote `/home/gatea/…` logs already exist and are cited by
  hash). Proposed outputs are marked **NOT YET CREATED**.
- **No-clobber timestamped output paths** and **preregistered hashes** are the standard: capture to a
  path that does not overwrite prior evidence; record the expected `bundle_db_sha256` /
  `invariants_sha256` into a separately-held hash record at creation time (COMMANDS.md Stage E
  pattern), then verify against it. Hashes for not-yet-created outputs are **not** invented here.
- Where an exact safe command cannot yet be specified, the cell reads **COMMAND GAP** (C1 post-stop
  verifier, C2 post-reboot subcheck, C3 restore-into-temp wrapper, C4 stop+mask-only run-kit step, C5
  egress capture). These are **local run-kit design items**, not execution items.

---

## 7. Factual verdict & blockers

- **Verdict:** the post-Gate chain `WP-L Phase 2 → WP-I staging verification → Audit 2 → WP-A` is
  correctly sequenced; its obligations, reusable evidence, and unresolved command gaps are explicitly
  mapped. It is **not execution-ready** while those gaps and the budget/authority blockers remain.
  Gate-A immutable evidence is
  identified and reusable (Group A). No host execution occurred and none is authorised.
- **Blocker 1 — budget (binding):** the exact 50 h balance is NOT REPRODUCIBLE (G7); no server-executed
  post-Gate work may be committed against the unknown hard ceiling. Requires a human re-plan or
  explicit ceiling extension.
- **Blocker 2 — authority:** WP-V/KVM2/master/credentials/broker/ARM/orders/TESTNET-mainnet/economic
  action each need a new explicit named lift (§1).
- **Open method gaps (not blockers — local design work):** a post-start read-only verifier (G2), a
  post-SIGTERM "no dangling state" procedure (C1/E8/I-R4), a post-reboot read-only subcheck (C2), a
  restore-into-temp wrapper (C3), and a stop+mask-only rollback run-kit step (C4). Each is a **COMMAND
  GAP** to be resolved in local run-kit design, not by improvising a host command.
- **~~Stale node to refresh (local): the absent symbol in WP0 I-R2 (G4).~~ ⛔ WITHDRAWN** — all 11
  symbols exist at the frozen candidate; WP0 is correct; there is no refresh item and no edit to
  make. See the withdrawn G4 and the corrected §4.
- **⛔ Open evidence item (round 3, B1a):** the **observed** installed-lock hash on `GATEA-STAGING` —
  `sha256sum` of `/opt/mtc-bridge/releases/2ce41e34…321b/IBKR_PAPER_BRIDGE/requirements.lock`, or the
  host manifest's `requirements_lock_sha256` — is **not in any located Gate-A evidence**. The expected
  value `a1881296…` is established from source; the comparison is not yet made. This is a **capture
  gap**, not a defect and not a drift signal: one bounded read-only host read closes it, and that read
  is blocked with all other host action under §1.
- **⛔ Provenance defects (G8 + G9 + G10, documentation-only):** this matrix originally sourced product
  facts from the divergent documentation checkout (**G8**, repaired round 1); the round-1 repair then
  recorded a Windows worktree hash as the candidate's lock hash (**G9**, repaired round 2); and rounds
  1–2 recorded a source-derived expectation as an observed host fact (**G10**, repaired round 3).
  **No product defect, no candidate change, no staging action, no test run in any round.**
  Residual propagation survives in three files outside this document's scope, each carrying **both**
  errors — the withdrawn G4 symbol claim and the wrong lock hash:
  `NEXT_SESSION_HANDOFF_2026-08-08.md:27` and `:46`; `_AI_MEMORY/GLOBAL_HANDOFF.md:28` and `:49`;
  `_AI_MEMORY/NEXT_STEPS.md:23` and `:37`. Handed to the Lead.
- **⛔ Round-2 note on what the repairs did *not* reach:** both rounds corrected *citations*. No
  obligation, gap conclusion, blocker, or authority statement in this matrix changed in either
  round, and the two blockers below still bind.

## Next steps (execution order)

1. **[AI: Any]** Local run-kit design/validation only: author the bounded **post-start read-only
   subcheck** set (Group B) and the four **COMMAND GAP** procedures (C1 post-stop verifier, C2
   post-reboot subcheck, C3 restore-into-temp wrapper, C4 stop+mask-only rollback step) as *designs*,
   with exact commands, no-clobber output paths, preregistered predicates, and stop conditions. **No
   staging execution.** ⛔ **Take every product/deploy/tool line anchor from §4/§4a/§4b or re-derive
   it at `2ce41e34…321b`; do not read product facts from the documentation checkout (G8).**
   ⛔ **Take every hash from §4b, labelled by kind; never hash a file out of this Windows worktree
   (G9). Where a run-kit step compares the lock on the host, the expected value is the raw blob
   content SHA-256 `a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e` — not
   `40873556…`.**
   ⛔ **Write that comparison as a predicate, not a restatement (G10): the host value has never been
   read (§4b, B1a). The step reads "expected `a1881296…`, to be compared against
   `install_manifest.json` → `requirements_lock_sha256` / `sha256sum` of the installed lock", with a
   captured-output artifact and an investigate-read-only failure disposition — never "confirms the
   installed lock hash".**
   ⛔ **The former instruction to "refresh the stale WP0 I-R2 evidence-map node (G4)" is CANCELLED —
   G4 is withdrawn, WP0 is correct, and `WP0_SCOPE_BASELINE_RECORD_2026-07-31.md` must not be
   edited.**
1a. **[Lead]** Propagate **both** corrections to the three files outside this document's write scope.
   Each carries the withdrawn G4 symbol claim **and** the wrong lock hash — symbol lines
   `NEXT_SESSION_HANDOFF_2026-08-08.md:27`, `GLOBAL_HANDOFF.md:28`, `NEXT_STEPS.md:23`; hash lines
   `NEXT_SESSION_HANDOFF_2026-08-08.md:46`, `GLOBAL_HANDOFF.md:49`, `NEXT_STEPS.md:37`. For the hash
   lines, replace `40873556…` with content SHA-256 `a1881296…` (blob ID `47f53fa2…`), or drop the
   value and cite §4b. Original G4 propagation list: `NEXT_SESSION_HANDOFF_2026-08-08.md:27`,
   `_AI_MEMORY/GLOBAL_HANDOFF.md:28`, `_AI_MEMORY/NEXT_STEPS.md:23`.
2. **[AI: Any]** Keep `GATEA-STAGING` retained, active, credential-free DISARMED; take no service,
   package, credential, or network action against it. Do not discard it (needed through WP-A).
3. **[AI: Barış]** Re-plan the remaining hours against the hard 50 h ceiling, or issue an explicit
   ceiling extension, before any server-executed WP-L Phase 2 / WP-I / WP-A work.
4. **[AI: Barış]** A named explicit lift is required before WP-V, KVM2, master merge, credential load,
   broker/exchange access, ARM, orders, TESTNET/mainnet, economic action, or old-payload deletion.

**Next autonomous safe unit:** local run-kit design/validation **only** (step 1), with **no staging
execution**. ⛔ **Round-3 amendment to the former "it does not" claim:** the matrix now names one
read-only host fact that is **not** yet captured — the installed `requirements.lock` byte identity
(**B1a**). That does not change the next unit: B1a is a *host* read and stays blocked on Blockers 1–2
like every other host action; it is preregistered here, not performed. Every **other** read-only host
fact the matrix depends on is already captured by the post-Gate transition inventory, so the matrix
still adds its value through *run-kit / evidence-method design*, which is local. Server execution
remains blocked on Blockers 1–2.

## Stop conditions

- Any request to execute WP-V/KVM2/master/ARM/credentials/broker/orders/economic action without an
  explicit named lift.
- Any required WP-L Phase 2 / WP-I / WP-A evidence that would need a **product repair** (changes the
  frozen SHA → re-audit picture) — that is not a documentation unit.
- Any budget/hour claim that cannot be evidenced against the ledger's §2 anchors.
- Any attempt to invent/round/retroactively book hours, invent a rollback target, run `verify.sh`
  wholesale post-start, or destructively test the active database.
- ⛔ Any edit to `WP0_SCOPE_BASELINE_RECORD_2026-07-31.md` on the strength of the **withdrawn** G4
  claim. WP0 lines 308 and 364 are correct at the frozen candidate.
- ⛔ Any citation of documentation-checkout product blobs as candidate behaviour, or any bare
  `<path>:<line>` product citation in a post-Gate record (G8).
- ⛔ **(round 2, G9)** Any use of `40873556a7f4586d77f165b985863138c9fc95b095da64ac52456b8c49098ec3`
  as a candidate, payload, or host lock value — in particular as a preregistered PASS predicate
  against `/etc/mtc-bridge/install_manifest.json` → `requirements_lock_sha256` or against
  `RELEASE_SHA256SUMS`. A mismatch produced that way is a **documentation error, not lock drift**,
  and must not be escalated as a STOP or treated as candidate/host drift.
- ⛔ **(round 2, G9)** Any hash recorded without stating what was hashed (Git blob object ID vs raw
  blob content vs worktree checkout), or derived by hashing a file out of this Windows worktree.
- ⛔ **(round 2)** Any assumption that the gated steady profile inherits the first-start unit's
  `MTC_BRIDGE_START_MODE=credential_free_disarmed` pin — it does not (A4).
- ⛔ **(round 3, G10)** Any statement that the installed `/opt/mtc-bridge/…/requirements.lock`, or the
  host's `install_manifest.json` → `requirements_lock_sha256`, **is** `a1881296…` as an observed fact,
  absent a captured read-only host read recorded with its command and output. The accurate status is
  **expected `a1881296…`, unobserved** (§4b, B1a).
- ⛔ **(round 3, G10)** Any automatic disposition of a host mismatch **against `a1881296…`** — neither
  "documentation error" nor "lock drift" may be assumed. Investigate read-only, check both the
  expected-value derivation and the host, then escalate or dismiss. Round 2's automatic
  documentation-error ruling applies only to the withdrawn `40873556…`.
- ⛔ **(round 3)** Any execution of the B1a read-only host read — or any other host contact — without
  the named authority/budget lift required by §1.
- Any service drift on `GATEA-STAGING` (more than one listener, non-loopback bind, ARM enabled,
  credentials present, or an unexpected second release).

---

## Routing record

```
Classification      : Tier 4, difficult protected Bridge safety/evidence preregistration; exact-model owner request.
Protected           : yes — Bridge deployment/runtime/persistence/restart/rollback/egress evidence surface; documentation only.
Model + provider    : GLM-5.2 via Z.AI Coding Plan.
Cheaper-model rationale : exact-model user request and adversarial protected-surface synthesis; cheap sidecars separately map bounded requirements.
Exact paths         : writes — MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_POST_GATE_PREREGISTRATION_GAP_MATRIX_2026-08-09.md (new),
                       MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md (prepend),
                       MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md (prepend),
                       MTC_COMMAND_CENTER/11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md (prepend).
                     reads — AGENTS.md; roadmap §23a/§Audit 2; WPL_PHASE1/WPI_READINESS/WP0_SCOPE_BASELINE/GATE_A_STAGING_HOST_PROVENANCE;
                       A-0..A-9 PASS reports; GATE_A_POST_GATE_TRANSITION_INVENTORY / GATE_A_POST_GATE_ROADMAP_AUTHORITY_DISCOVERY /
                       GATE_A_50H_LEDGER_RECONSTRUCTION (2026-08-09); deploy/linux/{README,COMMANDS,SECURITY_BASELINE,verify.sh,
                       verify_lock.py,rollback.sh,lib/common.sh,systemd/*.template}; tools/wal_state_bundle.py; targeted tests/ via rg.
Context/tool budget : targeted reads/rg only, no broad repo scan; four-file write ceiling.
Fallback            : none; if the exact route is unavailable, stop without edits.
External API credits: no paid API; subscription route only.
```

### Repair addendum — 2026-08-09 (provenance correction)

```
Repair unit         : claude-opus-5, effort xhigh, fresh independent implementer session.
Defect              : product facts sourced from the divergent documentation checkout and recorded
                      as frozen-candidate facts (new gap G8).
Refs                : documentation HEAD 851d2aa5 (detached, clean tree);
                      frozen candidate 2ce41e34bceb599d80af24c5c33d835820ec321b (UNCHANGED);
                      merge base 4d2228cf8985ce755c398cceff23f777a99d5404;
                      divergence proven — both `git merge-base --is-ancestor` tests exit 1.
Corrections applied : superseding provenance block (top); §0 Lead-correction item 1 superseded;
                      new §0.6 start-mode facts; A3 SECURITY_BASELINE reclassified; A4/B1/B2/B3/B4/B6
                      verify.sh anchors; A5 rewritten (all 11 exist); B5 candidate basis added;
                      C2/C3 candidate-qualified; C5 egress premise corrected; Group E symbols
                      candidate-qualified; G2/G6 anchors; G4 WITHDRAWN; G8 added; §4 table rebuilt;
                      §4a verify.sh section map added; §5 ten→eleven + existence≠execution;
                      §7 and Next-steps corrected; stop conditions extended.
Full evidence       : GATE_A_POST_GATE_PROVENANCE_REPAIR_2026-08-09.md (same directory).
Product change      : none. No candidate change. No product/deploy/test file written.
Commands            : read-only Git only (rev-parse, merge-base, cat-file, grep, show, diff --stat,
                      status). No SSH/sudo/systemctl/reboot/service/test/package/network/broker/
                      exchange/credential/ARM/order/staging-host command. No Git mutation.
WP0                 : NOT edited; proposed deletion cancelled.
Memory/handoff      : none in this unit; Gate-7 write-back belongs to the Lead after acceptance.
```

### Repair addendum 2 — 2026-08-09 (lock byte provenance + remaining candidate qualification)

```
Repair unit         : claude-opus-5, effort xhigh, fresh independent implementer session (round 2).
Repaired commit     : f8a6bc0f1a7fa00fcd1637297e05424732386da7, clean worktree C:\PGR.
Defects             : G9 (new) — a Windows CRLF worktree hash (40873556…, 119 274 B) was recorded as
                      the frozen candidate's lock blob SHA-256 and declared exempt from
                      re-derivation; the correct raw-blob content SHA-256 is a1881296… (LF,
                      117 762 B) and the blob object ID is 47f53fa2… . Also: product/deploy/tool
                      citations round 1 did not dispute were left bare, contrary to G8's own rule.
Refs                : documentation HEAD f8a6bc0f (detached, clean; round-1 HEAD 851d2aa5 — no
                      product-blob drift between them, all §4b paths re-resolved and identical);
                      frozen candidate 2ce41e34bceb599d80af24c5c33d835820ec321b (UNCHANGED);
                      merge base 4d2228cf…, divergence re-proven (both --is-ancestor tests exit 1).
Corrections applied : round-2 superseding block (top); Lead-corrections item 4 superseded; §0.5 lock
                      identity triple; A1 README qualified; A3 lock-identity caveat withdrawn and
                      replaced, Output artifact now recorded; A4 first-start anchors + steady-profile
                      blob and start-mode asymmetry; A6 verify_lock.py qualified with anchors;
                      B1 hash-preregistration warning; C1/C2 template anchors; C3/C4 COMMANDS.md +
                      rollback.sh qualified with anchors; G3 qualified; §4 coincidence-vs-ref-
                      invariance table; §4b blob ledger and lock identity (NEW); G9 added; §7 verdict;
                      Next steps 1 and 1a; stop conditions extended.
Values of record    : lock blob object ID  47f53fa227bf0f18b9bf9bd77e060d8856961728 (ref-invariant
                                           at 2ce41e34…321b, 851d2aa5, f8a6bc0f, 637307e8);
                      lock content SHA-256 a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e
                                           (LF, 117 762 B) — the value to preregister;
                      worktree artifact    40873556a7f4586d77f165b985863138c9fc95b095da64ac52456b8c49098ec3
                                           (CRLF, 119 274 B) — never cite;
                      counts               56 ==-pinned entries, 1345 --hash=sha256: lines.
Full evidence       : GATE_A_POST_GATE_PROVENANCE_REPAIR_2026-08-09.md §2.7, §2.8, §4.1, §4.2, §5.1,
                      §6.7, §10.
Product change      : none. No candidate change. No product/deploy/test file written.
Commands            : read-only Git only (rev-parse, merge-base, cat-file, ls-files --eol, grep,
                      config --get, status) plus local sha256sum/wc over the worktree lock file.
                      No SSH/sudo/systemctl/reboot/service/test/package-install/network/broker/
                      exchange/credential/ARM/order/staging-host command. No Git mutation. No commit.
WP0                 : NOT edited; G4 stays withdrawn; proposed deletion stays cancelled.
Out of scope        : NEXT_SESSION_HANDOFF_2026-08-08.md, _AI_MEMORY/GLOBAL_HANDOFF.md,
                      _AI_MEMORY/NEXT_STEPS.md — each carries both errors; handed to the Lead.
Memory/handoff      : none in this unit; Gate-7 write-back belongs to the Lead after acceptance.
```

### Repair addendum 3 — 2026-08-09 (expected payload bytes vs observed installed-host bytes)

```
Repair unit         : claude-opus-5, effort xhigh, fresh independent implementer session (round 3).
Repaired at         : documentation HEAD f8a6bc0f1a7fa00fcd1637297e05424732386da7, worktree C:\PGR,
                      with rounds 1-2 present as uncommitted changes to these two files only.
                      Nothing committed or staged; no Git mutation of any kind.
Defect              : G10 (new) — rounds 1-2 recorded a source-derived expectation as an observed
                      host fact: "the installed lock therefore hashes to a1881296…", attributed to
                      /etc/mtc-bridge/install_manifest.json → requirements_lock_sha256. No Gate-A
                      evidence located in this repair records the observed installed-lock SHA-256 or
                      the host manifest value.
Retained            : a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e as the correct
                      EXPECTED source/payload byte hash for the LF archive (re-derived this round;
                      git cat-file -s → 117762). 40873556… stays withdrawn (byte arithmetic over the
                      blob, independent of any host claim); blob ID 47f53fa2… stays ref-invariant;
                      counts 56 / 1345 stand; G4 stays withdrawn; WP0 stays uneditable.
Now open            : B1a — observed installed-host lock hash NOT IN EVIDENCE; closable by one
                      authorised read-only host read; blocked by §1.
Evidence of absence : transition inventory's install_manifest read records boolean/schema fields
                      only, no hash field; install.sh writes LOCK_SHA to the manifest (:416) but
                      never logs it (:431-433); the only local verify_lock / RELEASE_SHA256SUMS PASS
                      records belong to the superseded ebada020 and 1adf9ae5 releases and carry
                      package counts, not hashes. The Lead has read C:\WPI_ARTIFACTS\ locally:
                      ...\2ce41e34…321b\RELEASE_SHA256SUMS:99 records the EXPECTED package-member
                      hash a1881296… for ./IBKR_PAPER_BRIDGE/requirements.lock, and
                      post_gate_transition_inventory_detail_20260809.out records
                      requirements_lock_sha256 only as a manifest_top_keys entry without printing
                      its value. No targeted local-artifact hit supplies the observed installed-host
                      lock hash or manifest field value. /home/gatea/ remains uninspected; no host
                      was contacted.
Corrections applied : round-3 superseding block (top); round-2 block sentences qualified; Lead-
                      corrections round-2 bullet scoped; §0.5 lock identities 3→4 with the observed
                      value marked NOT IN EVIDENCE; A3 Output artifact scoped to static/local with an
                      investigate-read-only host disposition; B1 warning cross-referenced and new
                      Group-B item B1a added (proposed read-only command, NOT EXECUTED, blocked);
                      G9 wording; G10 added; §4b lock-identity table row added; §7 open evidence
                      item, G8+G9+G10 summary and the "next autonomous safe unit" claim amended;
                      Next steps 1; stop conditions; this addendum.
Product change      : none. No candidate change. No product/deploy/test file written.
Commands            : read-only Git only (rev-parse, cat-file blob/-s) plus local read-only content
                      search and one read of the ref-invariant install.sh. No SSH/sudo/systemctl/
                      reboot/service/test/package-install/network/broker/exchange/credential/ARM/
                      order/staging-host command. No host contacted. No Git mutation. No commit.
WP0                 : NOT edited; G4 stays withdrawn; proposed deletion stays cancelled.
Out of scope        : NEXT_SESSION_HANDOFF_2026-08-08.md, _AI_MEMORY/GLOBAL_HANDOFF.md,
                      _AI_MEMORY/NEXT_STEPS.md — when the Lead replaces 40873556… there, label the
                      replacement "expected raw blob content SHA-256 (LF), source-derived"; do not
                      restate it as the installed-host value.
Memory/handoff      : none in this unit; Gate-7 write-back belongs to the Lead after acceptance.
```
