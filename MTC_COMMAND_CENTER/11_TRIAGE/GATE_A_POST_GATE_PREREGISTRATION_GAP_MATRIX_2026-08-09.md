# Gate A — Post-Gate Preregistration & Gap Matrix (WP-L Phase 2 → WP-I staging → Audit 2 → WP-A)

- **Date:** 2026-08-09.
- **Model / route:** GLM-5.2 via the Z.AI Coding Plan route (owner-requested exact model).
- **Session type:** Bounded documentation unit, **read-only / local**. Starting documentation HEAD
  `52b8f496`; frozen product candidate `2ce41e34bceb599d80af24c5c33d835820ec321b` (unchanged).
- **Worker scope:** GLM-5.2 edited only the four task-named files — this new record,
  `_AI_MEMORY/NEXT_STEPS.md`, `_AI_MEMORY/GLOBAL_HANDOFF.md`, and
  `11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md` (the latter three prepended; all prior text
  preserved). GLM-5.2 ran **no** SSH, Gate-A script, sudo, systemctl, reboot, test, package/install,
  network/broker/exchange, credential-read, Git, staging-host, or mutation command. Targeted reads
  and `rg` only; no broad repo scan. **No command block in this document was executed.** No evidence
  directory is claimed to exist unless an existing path is cited.

- **Lead acceptance corrections:** Codex independently checked the four-file diff against real source
  and corrected three GLM drafting errors before integration: the test map contains **10 existing
  symbols plus 1 stale/absent symbol**; reboot does **not** create a mask (the currently running unit is
  unmasked, so its post-reboot mask state must be preregistered rather than assumed); and credentialed
  TESTNET egress observation does **not** require ARM. ARM remains forbidden. Codex also re-derived the
  candidate lock blob SHA-256 as
  `40873556a7f4586d77f165b985863138c9fc95b095da64ac52456b8c49098ec3` (56 entries, 1345 hashes).

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
5. **56-entry hash-locked closure confirmed at the candidate checkout** this unit:
   `requirements.lock` has **56** `==`-pinned entries and **1345** `--hash=sha256:` lines (≥1 hash
   per entry); `verify_lock.py` rejects URLs/VCS/index-overrides and requires exact `==` + ≥1 hash.

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
- **Canonical source:** `GATE_A_A9_PASS_FINAL_2026-08-09D.md`; `deploy/linux/README.md`.
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
- **Canonical source:** `IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md`.
- **Existing evidence:** 56-entry exact+hashed lock; secret scan zero category/path hits at the
  *frozen* tree; egress inventory (TESTNET runtime-required, optional Telegram, install-time index,
  loopback listener, forbidden mainnet, unused Anthropic/xAI).
- **Remaining evidence:** this is **PRE-GATE-A / STATIC ONLY** — it is not a runtime egress capture,
  not an Ubuntu install result, and not destination-egress control. Runtime egress / TESTNET-only /
  no-mainnet remain owed (see C5).
- **⚠ Lock-identity precision:** the lock blob/SHA-256 recorded in SECURITY_BASELINE is for frozen
  source `637307e8` / candidate `1adf9ae5…`. The current candidate is `2ce41e34…321b`. The
  *property* (56 exact+hashed entries; `verify_lock.py` contract) is source-invariant and was
  re-confirmed at the candidate checkout this unit (56 entries, 1345 hashes), but the exact lock
  **blob SHA-256 was re-derived by the Lead at `2ce41e34…321b` as
  `40873556a7f4586d77f165b985863138c9fc95b095da64ac52456b8c49098ec3`.** Do not cite the
  `1adf9ae5` blob hash as the current candidate's.
- **Mutation class:** `local-static`. **Authority/budget:** none.
- **Output artifact:** the re-derived candidate lock blob SHA-256 (to be recorded when computed; NOT
  YET recorded here). **PASS:** 56 entries, every entry exact+hashed, no URL/VCS/index override.
  **Failure disposition:** a non-hashed or count-drifting lock is a product-SHA change (STOP; not a
  documentation unit). **D026:** n/a (inventory, not a regression test).

### A4 — Unit-template static invariants (design facts)
- **Predicate:** the installed unit declares the safety-critical directives.
- **Canonical source:** `deploy/linux/systemd/mtc-bridge-first-start.service.template`;
  `deploy/linux/verify.sh` (needles, lines 155–165); `deploy/linux/lib/common.sh` (constants).
- **Existing evidence:** `Restart=no`; no `[Install]` section; `KillSignal=SIGTERM`,
  `KillMode=mixed`, `TimeoutStopSec=45`, `FinalKillSignal=SIGKILL`; `MTC_BRIDGE_STATE_DB`,
  `ReadWritePaths`, sandboxing directives (`NoNewPrivileges`, `ProtectSystem=strict`,
  `RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX`, etc.); loopback bind asserted in code.
- **Remaining evidence:** the *template* is static; the *rendered/installed* unit on the host is
  verified by A4-staging (B2). The **steady** profile (`mtc-bridge-steady.service.template`,
  `Restart=on-failure`) is a **gated artifact** — never installed/enabled; itself has no `[Install]`.
- **Mutation class:** `local-static`. **Authority/budget:** none.
- **Output artifact:** cited inline. **PASS:** template matches the accepted release template byte-for
  byte (`verify.sh` lines 182–190 `cmp`). **Failure disposition:** template drift = candidate change.

### A5 — Local source-map: target test symbols (10 exist, 1 stale)
- **Predicate:** the regression tests named as evidence in the readiness baseline still exist in the
  candidate source.
- **Canonical source:** `WP0_SCOPE_BASELINE_RECORD_2026-07-31.md` (evidence map); `IBKR_PAPER_BRIDGE/tests/`.
- **Existing evidence (verified this unit by `rg`):** the ten requested target symbols resolve as
  listed in §4 below. In addition, the older WP0 map names
  `test_kill_restart_after_request_commit_keeps_killed_and_resumes_once`, which is **absent** from
  current source (see Gap G4). Two valid symbols anchor WP0 I-R2
  (`test_kill_persists_across_restart`, `test_killed_alive_is_interrupted`).
- **Mutation class:** `local-static`. **Authority/budget:** none.
- **Output artifact:** the test-map table (§4). **PASS:** cited symbols exist at the cited paths.
  **Failure disposition:** an absent cited symbol is a stale evidence-map node (refresh the map), not a
  product-defect inference. **D026:** existence ≠ closure; see §5.

### A6 — Lock / `verify_lock.py` contract
- **Predicate:** an offline, network-free verifier proves every lock entry is exact+hashed and (with
  `--check-installed`) that the installed venv distribution set equals the lock.
- **Canonical source:** `deploy/linux/verify_lock.py`.
- **Existing evidence:** `parse_lock` rejects URLs/VCS/index overrides, requires exact `==` + ≥1
  `--hash=sha256:` per entry; `--check-installed` compares installed vs expected, allowing only the
  `pip`/`setuptools` bootstrap set; prints `packages=<n>`. Re-confirmed this unit: 56 entries.
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
  equals the 56-entry lock"); `verify.sh` §3 (lines 104–121); `verify_lock.py`.
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

### B2 — systemd runtime identity (active, `Restart=no`, bound to exact SHA/venv)
- **Predicate:** the running unit is the accepted first-start unit, active, `Restart=no`,
  `NRestarts=0`, bound to the exact release SHA and per-SHA venv, with no `[Install]`.
- **Canonical source:** `verify.sh` §6 (lines 150–199); transition inventory (current unit fragment
  SHA-256 `538c1c60…279bd`, 3736 B).
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
- **Canonical source:** `verify.sh` §2/§4 (lines 78–135); `deploy/linux/README.md` target layout.
- **Existing evidence:** transition inventory (release root mode 555; env 600; manifest 640).
- **Proposed command (NOT EXECUTED):** read-only `stat`/`find` (mirror `verify.sh` assertions without
  the mask/active/port-closed preconditions). **COMMAND GAP:** a single bounded post-start
  permissions-subcheck command is not yet authored as a run-kit step; design it in the local run-kit
  unit (do not run `verify.sh` wholesale — see G2).
- **Mutation class:** `read-only-host`. **Authority/budget:** blocked. **Output artifact:** stat output
  (NOT YET CREATED). **PASS:** modes/owners match. **Failure disposition:** mode/owner drift = STOP.

### B4 — Environment isolation / sandboxing directives present
- **Predicate:** hardening directives are present and effective on the running unit.
- **Canonical source:** unit template; `verify.sh` needles (lines 155–165).
- **Existing evidence:** template declares them (A4).
- **Proposed command (NOT EXECUTED):** `systemctl show` the effective security properties
  (`PrivateTmp`, `ProtectSystem`, `NoNewPrivileges`, `CapabilityBoundingSet`, etc.).
- **Mutation class:** `read-only-host`. **Authority/budget:** blocked. **Output artifact:** show output
  (NOT YET CREATED). **PASS:** effective values match template. **Failure disposition:** drift = STOP.

### B5 — Current credential-free DISARMED runtime (no secret value read)
- **Predicate:** API reports DISARMED, `state_version=1`, mode `credential_free_disarmed`, all
  network/exchange/credential/ARM flags off; **no credential value is read.**
- **Canonical source:** A-5/A-7/A-8/A-9 postchecks; transition inventory.
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
- **Canonical source:** `verify.sh` §8 (lines 233–244); A-8 PASS evidence.
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
- **Canonical source:** `WP0_SCOPE_BASELINE_RECORD_2026-07-31.md` I-R4 (line 366); unit template
  `KillSignal=SIGTERM`/`TimeoutStopSec=45`/`FinalKillSignal=SIGKILL`.
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
- **Canonical source:** `WPI_READINESS_RECORD_2026-08-01.md` §6 ("reboot DISARMED"); first-start +
  steady templates; roadmap line 773 ("survives reboot DISARMED").
- **Existing evidence:** template facts (A4); A-5 did **not** reboot the host.
- **Proposed method (NOT EXECUTED):** first preregister one of two distinct scenarios: (A) plain
  reboot from the current unmasked state, expecting inactive+unmasked; or (B) separately authorised
  stop+mask followed by reboot, expecting inactive+masked. On return, read-only assert the expected
  mask state plus no `bridge.app` writer, closed control port, and persisted DB state not ARMED.
  **COMMAND GAP:**
  `verify.sh` is a pre-start masked verifier and is **not** the post-reboot instrument; a bounded
  post-reboot read-only subcheck procedure must be designed first.
- **Mutation class:** `mutating-host` (reboot). **Authority/budget:** requires explicit named lift +
  budget; **blocked**. **Output artifact:** post-reboot evidence log (NOT YET CREATED). **PASS:** unit
  expected preregistered mask state + no writer/listener + DB state not ARMED after reboot. **Failure
  disposition:** any writer, listener, ARMED state, or mask-state mismatch after reboot = STOP.

### C3 — SQLite WAL-consistent backup / verify / restore on a TEMPORARY COPY (never the active DB)
- **Predicate:** a WAL-consistent bundle is captured, verified, and **restored into a temporary copy**
  that re-derives the same invariants; the **active database is never destructively tested.**
- **Canonical source:** `IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py`; `deploy/linux/COMMANDS.md`
  Stage E; roadmap line 773; WPI §6 ("SQLite backup/restore and risk/history continuity").
- **Existing evidence:** `wal_state_bundle.py` exists, is offline/read-only against source, uses the
  SQLite online-backup API (never copies the db/wal/shm trio), runs `integrity_check` +
  `foreign_key_check` on both ends, re-derives sanitised invariants, and fails closed on sidecar
  presence, drift, or hash mismatch. Test coverage: `test_bundle_never_contains_a_wal_shm_trio`,
  `test_invariants_preserve_risk_and_history` (exist; A5).
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
  copy. **COMMAND GAP:** the exact "restore into temp DB + re-verify" wrapper script is not yet
  authored; design it locally (next unit).
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
- **Canonical source:** `deploy/linux/rollback.sh`; `COMMANDS.md` Stage G; roadmap/WPI §6.
- **Existing evidence:** `rollback.sh` requires `--state-manifest-file` + `--state-manifest-sha256`
  (the accepted state-bundle manifest hash), stops (SIGTERM, 45 s) then masks, asserts no
  `bridge.app` writer and a closed control port, preserves state, and writes
  `/etc/mtc-bridge/rollback_manifest.json`. The `--to-release-sha`/`--to-manifest-sha256` pair is
  **optional** — stop+mask works without a target.
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
- **Canonical source:** `SECURITY_BASELINE.md` §3 (egress inventory); WPI §6.
- **Existing evidence:** **static inventory only** (A3): code selects `network="testnet"`
  (`bridge/app.py`); SDK `constants.TESTNET_API_URL`; notifier gated on both Telegram names resolving.
  A-8 proved the listener is loopback-only. A-9 proved zero secret-signature hits.
- **⚠ Hard blocker:** observing *actual runtime* egress requires credentials and broker/TESTNET network
  authority, all explicitly unavailable now (§1). It does **not** require ARM: source constructs the
  TESTNET broker before any human ARM transition, and an authorised future capture must remain
  DISARMED with ARM forbidden.
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

### E1 — DISARMED restart invariant (I-R1)
- **Predicate:** restart while flat + DISARMED → starts DISARMED, no order submitted.
- **Canonical source:** `WP0_SCOPE_BASELINE_RECORD_2026-07-31.md` I-R1 (line 363); `bridge/app.py`
  forces DISARMED unless KILLED.
- **Existing evidence:** code+test COVERED statically; A-6 empty-broker startup. **Remaining:** Ubuntu
  execution.
- **Test symbol (source-verified):** `tests/test_interim_risk_wiring.py::test_gates_persist_across_restart`.
- **Proposed method (NOT EXECUTED):** authorised single restart on the retained host; assert DISARMED
  + no order via `/api/status`. **Mutation class:** `mutating-host`. **Authority/budget:** blocked.
  **PASS:** DISARMED, zero orders. **Failure:** armed state or any order = STOP (candidate repair).
  **D026:** existing test; not new closure evidence.

### E2 — killed/disarmed persistence across restart (I-R2; note stale node)
- **Predicate:** killed/disarmed state persists across restart.
- **Canonical source:** WP0 I-R2 (line 364).
- **Existing evidence:** code+test COVERED statically. **⚠ Stale node (Gap G4):** I-R2 cites
  `test_kill_restart_after_request_commit_keeps_killed_and_resumes_once`, **absent** from current
  source; the other two cited symbols exist. Refresh the evidence map; do not assume a defect.
- **Test symbols (source-verified):** `tests/test_api.py::test_kill_persists_across_restart`,
  `tests/test_window_state.py::test_killed_alive_is_interrupted`.
- **Proposed method (NOT EXECUTED):** restart under a killed/disarmed state; assert persistence.
  **Mutation class:** `mutating-host`. **Authority/budget:** blocked. **PASS:** state persists.
  **Failure:** state reset = STOP. **D026:** existing tests; not new closure evidence.

### E3 — DB state-file integrity across restart (I-R3)
- **Predicate:** the SQLite state file remains integrity-clean and risk/history-invariant across
  restart.
- **Canonical source:** WP0 I-R3 (line 365); `wal_state_bundle.py`.
- **Test symbols (source-verified):** `tests/test_wal_state_bundle.py::test_bundle_never_contains_a_wal_shm_trio`,
  `tests/test_wal_state_bundle.py::test_invariants_preserve_risk_and_history`.
- **Proposed method (NOT EXECUTED):** restart, then `wal_state_bundle` capture+verify on a temp copy
  (C3 method). **Mutation class:** `mutating-host`. **Authority/budget:** blocked. **PASS:** integrity
  ok + invariants stable. **Failure:** drift = STOP.

### E4 — Reconnect dedupes to one order
- **Predicate:** a disconnect/reconnect does not duplicate an in-flight order.
- **Canonical source:** WP0 reconciliation map; A-6 boundary.
- **Test symbol (source-verified):** `tests/test_p1_failure_drills.py::test_drill_disconnect_reconnect_dedupes_to_one_order`.
- **⚠ A-6 boundary (Gap G5):** A-6 asserted empty-broker startup only; it does **not** prove
  queue-drain-under-load or full reconcile (schema-4 disables full reconcile). WP-A must exercise real
  reconnect/queue/full-reconcile predicates.
- **Proposed method (NOT EXECUTED):** authorised reconnect drill; assert exactly one order. **Mutation
  class:** `mutating-host`. **Authority/budget:** blocked. **PASS:** one order. **Failure:** duplicate =
  STOP.

### E5 — Stale-data auto-disarm
- **Predicate:** stale market data triggers exactly one auto-disarm.
- **Canonical source:** WP0 map.
- **Test symbols (source-verified):** `tests/test_p1_failure_drills.py::test_drill_data_stale_auto_disarms`,
  `tests/test_bars.py::test_data_stale_emits_and_disarms_once`.
- **Proposed method (NOT EXECUTED):** authorised stale-data drill; assert one disarm. **Mutation
  class:** `mutating-host`. **Authority/budget:** blocked. **PASS:** one disarm. **Failure:** none or
  many = STOP.

### E6 — WebSocket death triggers auto-reconnect
- **Predicate:** a feed/WebSocket death triggers auto-reconnect (not silent failure).
- **Canonical source:** WP0 map.
- **Test symbol (source-verified):** `tests/test_p1_failure_drills.py::test_drill_ws_death_triggers_auto_reconnect`.
- **Proposed method (NOT EXECUTED):** authorised ws-death drill; assert reconnect. **Mutation class:**
  `mutating-host`. **Authority/budget:** blocked. **PASS:** reconnect observed. **Failure:** no
  reconnect = STOP.

### E7 — Active recovery suppresses ordinary reconcile repair
- **Predicate:** while an active partial-fill recovery is in progress, ordinary reconcile repair is
  suppressed.
- **Canonical source:** WP0 map.
- **Test symbol (source-verified):** `tests/test_partial_fill_protection.py::test_active_recovery_suppresses_ordinary_reconcile_repair`.
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
- **G2 — full `verify.sh` is a pre-start verifier and will fail post-start.** `verify.sh` §6/§8 fails
  if the unit is ACTIVE ("must not be running before KVM2-P4-07", lines 207–211), fails if any
  `bridge.app` writer exists (lines 237–241), and asserts the control port **closed** (line 242); its
  own comment (lines 234–236) states it is the *masked/unstarted* mode only. After Gate A unmasked and
  started the service, a full `verify.sh` run will **intentionally fail**. **Do not prescribe it in the
  current state.** Use the bounded read-only subchecks of Group B (or design a missing post-start
  verifier) — `COMMANDS.md` Stage F states the mask assertion is intentionally no longer applicable
  post-start.
- **G3 — rollback rebind has an unmet prerequisite.** `rollback.sh` can stop+mask without a target
  (requires the accepted state-manifest hash) but **mutates service state**; a meaningful release-rebind
  additionally requires an **already-installed previous immutable release**, and only candidate
  `2ce41e34…321b` is installed (old `ebada020…` install + venv already absent). A prior-release rollback
  proof has an **unmet prerequisite**. Do not invent a target or run rollback.
- **G4 — stale evidence-map node.** `WP0_SCOPE_BASELINE_RECORD_2026-07-31.md` references
  `test_kill_restart_after_request_commit_keeps_killed_and_resumes_once` (lines 308, 364/I-R2), but
  that symbol is **absent** from current source (verified this unit). Mark it a **stale evidence-map
  node requiring source-map refresh**; do **not** assume a product defect and do not invent a
  replacement. The two sibling symbols in I-R2 do exist.
- **G5 — A-5/A-6 scope limits.** A-5 proved SIGKILL + restart + state integrity + DISARMED, **not**
  graceful SIGTERM and **not** host reboot (I-R4 OPEN). A-6 asserted empty-broker startup only; it does
  **not** prove queue-drain-under-load or full reconcile (schema-4 disables full reconcile).
- **G6 — README historical "never executed" text is stale after Gate A.** `deploy/linux/README.md`
  states these assets "have never been executed" (lines 4, 118–120). After Gate A A-0..A-9, the
  candidate **has** been installed and started on the staging host. **Cite that README line only as
  historical**, not as current status.
- **G7 — exact 50-hour balance NOT REPRODUCIBLE; all host execution blocked.** The current exact
  used/remaining balance is not reproducible (`GATE_A_50H_LEDGER_RECONSTRUCTION_2026-08-09.md`,
  state 5). The broader standing authorisation does **not** override the narrower current
  budget/safety hold and does **not** authorise credentials, broker, ARM/orders, TESTNET/mainnet, or
  economic action. No host execution may be authorised or performed in this unit.

---

## 4. Existing target tests — exact map (verified this unit by `rg`)

| # | Symbol | Path:line | Status |
|---|---|---|---|
| 1 | `test_gates_persist_across_restart` | `tests/test_interim_risk_wiring.py:333` | EXISTS → WP-A E1/I-R1 |
| 2 | `test_kill_persists_across_restart` | `tests/test_api.py:61` | EXISTS → WP-A E2/I-R2 |
| 3 | `test_killed_alive_is_interrupted` | `tests/test_window_state.py:82` | EXISTS → WP-A E2/I-R2 |
| 4 | `test_bundle_never_contains_a_wal_shm_trio` | `tests/test_wal_state_bundle.py:289` | EXISTS → WP-A E3/I-R3, C3 |
| 5 | `test_invariants_preserve_risk_and_history` | `tests/test_wal_state_bundle.py:315` | EXISTS → WP-A E3/I-R3, C3 |
| 6 | `test_drill_disconnect_reconnect_dedupes_to_one_order` | `tests/test_p1_failure_drills.py:16` | EXISTS → WP-A E4 |
| 7 | `test_drill_data_stale_auto_disarms` | `tests/test_p1_failure_drills.py:40` | EXISTS → WP-A E5 |
| 8 | `test_drill_ws_death_triggers_auto_reconnect` | `tests/test_p1_failure_drills.py:272` | EXISTS → WP-A E6 |
| 9 | `test_data_stale_emits_and_disarms_once` | `tests/test_bars.py:27` | EXISTS → WP-A E5 |
| 10 | `test_active_recovery_suppresses_ordinary_reconcile_repair` | `tests/test_partial_fill_protection.py:1867` | EXISTS → WP-A E7 |
| 11 | `test_kill_restart_after_request_commit_keeps_killed_and_resumes_once` | — | **ABSENT** (stale node, WP0 lines 308/364) |

---

## 5. D026 — falsified-test rule (binds this matrix)

A regression test offered as proof that a **specifically named** defect is closed is **not closure
evidence** until it has been shown **RED** against the exact pre-fix/reverted behaviour (or an
equivalent deliberate falsification) **and GREEN** with the fix in place, with the commands and real
output recorded (`AGENTS.md` §D026, owner-ratified 2026-08-03).

- **Existing tests are not automatically new D026 evidence** for a newly named defect. The ten symbols
  in §4 are *existing coverage*; citing them does not close a new defect.
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
- **Stale node to refresh (local):** the absent symbol in WP0 I-R2 (G4) — refresh the evidence map; no
  defect assumed.

## Next steps (execution order)

1. **[AI: Any]** Local run-kit design/validation only: author the bounded **post-start read-only
   subcheck** set (Group B) and the four **COMMAND GAP** procedures (C1 post-stop verifier, C2
   post-reboot subcheck, C3 restore-into-temp wrapper, C4 stop+mask-only rollback step) as *designs*,
   with exact commands, no-clobber output paths, preregistered predicates, and stop conditions. **No
   staging execution.** Refresh the stale WP0 I-R2 evidence-map node (G4) locally.
2. **[AI: Any]** Keep `GATEA-STAGING` retained, active, credential-free DISARMED; take no service,
   package, credential, or network action against it. Do not discard it (needed through WP-A).
3. **[AI: Barış]** Re-plan the remaining hours against the hard 50 h ceiling, or issue an explicit
   ceiling extension, before any server-executed WP-L Phase 2 / WP-I / WP-A work.
4. **[AI: Barış]** A named explicit lift is required before WP-V, KVM2, master merge, credential load,
   broker/exchange access, ARM, orders, TESTNET/mainnet, economic action, or old-payload deletion.

**Next autonomous safe unit:** local run-kit design/validation **only** (step 1), with **no staging
execution**, unless this matrix reveals a more urgent read-only prerequisite — **it does not**: every
read-only host fact the matrix depends on is already captured by the post-Gate transition inventory,
so the matrix adds value through *run-kit / evidence-method design*, which is local. Server execution
remains blocked on Blockers 1–2.

## Stop conditions

- Any request to execute WP-V/KVM2/master/ARM/credentials/broker/orders/economic action without an
  explicit named lift.
- Any required WP-L Phase 2 / WP-I / WP-A evidence that would need a **product repair** (changes the
  frozen SHA → re-audit picture) — that is not a documentation unit.
- Any budget/hour claim that cannot be evidenced against the ledger's §2 anchors.
- Any attempt to invent/round/retroactively book hours, invent a rollback target, run `verify.sh`
  wholesale post-start, or destructively test the active database.
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
