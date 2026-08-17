# WP-I SUCCESSOR PREREGISTRATION — SKELETON (Lead, 2026-08-10)

Prepared while the T0 audit cycles run, so finalization is a fill-in exercise, not an
authoring task. This skeleton mints NOTHING: every identifier remains
`<ALLOCATE-AT-DISPATCH>`, every unfrozen hash `<PIN-AT-FREEZE>`. The successor document
is produced from this skeleton + the accepted draft (round 1.7) once all three T0
artifacts (RP6-P0, RP7-WPI-RO, transport set) hold accepting verdicts from both
flagships. Committing the successor BEFORE any invocation is mandatory (draft §0).

## 1. Values already resolvable — filled at finalization from committed records

| Variable | Value | Source |
|---|---|---|
| `WPI_UNIT_FRAGMENT_SHA256` | `538c1c6038b475e87fb0e9b9c35fd4ebd8451b40ff93538f8fea5aa0b49279bd` | `LEAD_PIN_RESOLUTION_2026-08-10.md` (R1) |
| `WPI_LOG_DIR` | `/var/log/mtc-bridge` | same (R2); already literal in draft round 1.6+ |
| `WPI_EXPECTED_DROPIN_SET` | **empty set** (zero drop-ins for `mtc-bridge-first-start.service`) | GLM advisory + Lead verification: `install.sh` at the candidate creates none; a non-empty observed set is FAIL (deviant state), inability to enumerate is STOP |
| `P0_STATE_UID` / `P0_STATE_GID` | `999` / `988` | recorded getent preflight (draft §2) |
| `P0_EXPECT_UID` | numeric uid of the `gatea` login | pinned at dispatch from the recorded login identity |
| All host paths, lock digest/bytes/packages, endpoint, sweep budget | as draft §2 | unchanged |

## 2. Placeholders that ONLY Stage-1 freeze may fill

- Block hashes: `RP6-P0.sh`, `RP7-WPI-RO.sh` (accepted final bytes), reused
  `RP0-LIB.sh` `4a404d7b…` (18968 B) + `RP0-BOOTSTRAP.sh` `e7d748f6…` (1937 B)
  byte-verified at freeze.
- Transport hashes: `run_p0.sh`, `run_ro.sh`, `transport_runner.ps1`,
  `TRANSPORT_PLAN.tsv`, `remote_setup_wpi.sh`, `remote_extract_verify_wpi.sh`,
  reused `remote_close_tree.sh` `87157f0e…` (7470 B).
- `runkit.tar` bytes + digest (deterministic build, same builder discipline as
  Stage 1B).
- `WPI_FIXED_ATTESTED_MOUNT_PROJECTION_SHA256` (projection v2) and the row-8
  execution-domain attestation constants — see §5 OPEN DECISION.
- Extractor archive-constants block (member digests/bytes) — filled from the frozen
  member set.

## 3. Identifier allocation (at dispatch, per draft §1)

1. Mint `WPI-<UTCSTAMP>Z-<8hex>` base; stage RUNIDs `<base>-P0`, `<base>-RO`;
   `REMOTE_BASE=/home/gatea/wpi_staging_<component>`.
2. Test every component against accepted `rp0_require_safe_component`
   (rc 0) and demonstrate the refusal set (`../escaped`, `a/b`, `.`, `..`, `-lead`,
   empty, `bad name` → rc 1) — transcript into the successor self-QA.
3. Collision checks: operator-side vs the two recorded roots
   (`C:\WPI_ARTIFACTS\WPLP2_TRANSPORT_…` and `…-R45B`); host-side `/home/gatea/`
   check rides op 01's create-once semantics (a pre-existing tree is FAIL, spent
   RUNID).
4. A failed allocation burns the RUNID; no retry pool.

## 4. Freeze-gate checklist (ordered; each item blocks the next)

1. All three artifacts hold accepting verdicts from BOTH flagships (T0 floor).
2. Fill attestation constants (§5) → run the deferred accepting-input QA arms:
   `wpi_validate_inputs` GREEN (RP7 F2c freeze-gate item) and the RP6-P0 row-8
   equivalent.
3. §10.2 path-scope proof over every frozen block: parsed closed-set expansion (NOT
   literal scan), rejection of dynamic construction, allowlist comparison after
   expansion, computed-forbidden-path RED/GREEN — exact commands + real output in the
   Stage-1 record.
4. Deterministic `runkit.tar` build; member list = RP0-LIB, RP0-BOOTSTRAP, RP6-P0,
   RP7-WPI-RO, run_p0.sh, run_ro.sh (RP1-B3.sh excluded); fill extractor constants;
   re-hash everything into the successor §3/§4 tables.
5. Successor document completed (this skeleton + draft) and COMMITTED. Only then
   op 01.

## 5. RESOLVED — owner granted option (a), 2026-08-10 ~16:45 ("Seçenek a")

Gr

The projection-v2 digest and the row-8 namespace/root-mount identities must be
produced OUTSIDE the ssh login domain they attest (Pattern 2). Grant #3 covers running
`RPD-VERIFY.sh` as root — its accepted bytes (`3b9e78e8…`) predate projection v2 and do
not emit these values, and editing it voids its acceptance.

Options:
- **(a) RECOMMENDED:** owner extends grant #3 to ONE additional preregistered
  read-only root command set in the same root session (capture
  `/proc/self/mountinfo` + `readlink /proc/1/ns/{user,mnt,pid,net}` + root-mount
  identity, output hashed at production). Smallest new surface; same session, same
  read-only class.
- **(b)** Derive attestation from committed install-time deploy records only — no new
  host contact, but weaker: records predate today's host state, and a mount added
  since install would be invisible until the run STOPs on mismatch (fail-closed, but
  burns a RUNID).
- **(c)** Run WP-I without row-8/projection attestation — NOT acceptable: reverts the
  catalogue C04 repair; listed only for completeness.

**OWNER CHOSE (a) 2026-08-10 ~16:45** ("Seçenek a"). Recorded as authorization #6 in
`../NEW_SESSION_KICKOFF_PROMPT_2026-08-09_NIGHT.md`. Action: preregister the read-only
attestation command set (`/proc/self/mountinfo` capture + `readlink /proc/1/ns/{user,
mnt,pid,net}` + canonical root-mount identity, hashed at production) as part of the
successor document; it runs inside the grant-#3 root session before the RO stage
interprets any mount/namespace claim. Freeze-gate item 2 is now unblocked pending that
preregistration.

## 6. Op list

The successor reproduces `TRANSPORT_PLAN.tsv` (round-2 repaired) §5 semantics: ops
01–12, first-FAIL with `always` retention, evidence closed by separate invocations
(07/08), operator-side binding local-only (11/12), row-24 probe op 06 operator-side.

## 7. Post-run

Evidence retrieval (op 09/10) → digest-set binding → WP-I closure record (unit ledger,
hour booking) → Audit 2 dispatch (`AUDIT2_READINESS_PACKAGE`, resolve the GLM
supplemental-vs-omitted flag) → RPD-VERIFY root execution (grant #3) closes the three
B3-deferred checks + `bridge.env` naming question.
