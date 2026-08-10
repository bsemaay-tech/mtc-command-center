I have everything needed. Here is the verification report.

---

```
VERIFIED-CLOSED
```

**V1 — 17 repairs present at claimed locations** — PASS. All of C01–C17 found in the round-1.4 text: C01 (rows 5/6/7/10/11/15/17/18/19 split ENOENT→FAIL vs ambiguous→STOP, LoadState=not-found→FAIL, line 427–441); C02 (row 20, line 442); C03 (row 24, line 446); C04 (§4 lines 245–252, P0 rows 8–9 lines 402–403); C05 (rows 20–23 + netns rule lines 442/444/561–583 + §9 defer list 678–681); C06 (path-object rule lines 448–459); C07 (exec-env rule 524–533 + §10.3 step 1 740–748); C08 (rows 5/6/9, lines 427/428/431); C09 (row 21, line 443); C10 (rows 22/23 + structured-input rule, lines 444/445/535–542); C11 (probe-output precedence 513–522 + §7 close/bind 352–356/366–370); C12 (line-reader rule 544–551); C13 (P0 rows 1–3, lines 395–397); C14 (§1 110–113, §2 152–153, rows 10/11/15, §10.1, §10.3); C15 (scope-of-claim 612–625); C16 (§4 236–243, §5 293–299); C17 (§0 83–88, §10.2 721–732).

**V2 — STOP-vs-FAIL contract holds everywhere; no check weakened** — PASS. rc 0/1/3 contract stated 384–388 ("a STOP never becomes a FAIL by inference"); every substantive row ties FAIL to *positively established* deviant state after successful evaluation (rows 5, 6, 7, 10, 11, 14, 15, 17, 18, 19, 20, 21, 23, 24) and routes every invocation/access/traversal/parse/ambiguous/timeout class to STOP. The two judgement calls hold: row-20 401/403→STOP is consistent with the F3 authorization-failure→STOP principle (the body can't be read), and row-8 domain mismatch→STOP is correct (wrong-domain result is not host evidence). No vacuous check introduced — precondition rows (1,4–7,12,13,16) only STOP by design, which is correct gating not weakening.

**V3 — PIN placeholders untouched; read-only scope/authority claims intact** — PASS. `WPI_UNIT_FRAGMENT_SHA256` (line 147) and `WPI_LOG_DIR` (line 154) remain `<PIN-BEFORE-DISPATCH: …>`; §1.4 note (line 34) and §11 (784–786) reaffirm no placeholder fill; §12 records 0 host contact / 0 RUNIDs / 0 frozen blocks / no git action, and repo writes confined to `WPI_PREREG_DRAFT_ROUND1` (matches git status: only `M` draft + `??` round-1 files, all unstaged).

**V4 — No regression of round 1.1–1.3 fixes** — PASS. GLM F1 interpreter-exec STOP retained (row 18 line 440 + rule 553–559); Codex F1 metadata-readability precedence retained and additive (row 19 preflight 441 + rule 484–499); Codex F2 netns binding retained and *extended* by C05 to cover `curl` as well as `ss` (rule 561–583); F3/F4 system-manager/atomic-walk STOPs retained (rules 474–482, 501–511; rows 12–14). New parsing rules (C08/C09) are additive to F1, not overriding.

**V5 — Sample-attacks (4, catalogue falsification style)** — PASS (all stopped):
- *Attack A (row 19, Pattern 1/10):* a `*.dist-info/METADATA` at mode `000` under a named ACL denying `gatea` — pre-fix `verify_lock.py` exits nonzero → false "missing distribution" FAIL. Repaired text: metadata-readability preflight must prove every METADATA/RECORD open+readable before parity; generic nonzero verifier rc → `B1_STOP reason=verifier_not_evaluable`, never parity FAIL. **Stopped.**
- *Attack B (rows 22–23, Pattern 2):* PAM lands `gatea` in a private netns holding a decoy `127.0.0.1:8790` listener while the real service (host netns) has `0.0.0.0:8790`. Repaired text: row-22 preflight requires `readlink /proc/self/ns/net == readlink /proc/<MainPID>/ns/net` before any `ss`/`curl` output is read → `B6_STOP reason=netns_mismatch` → RPD-VERIFY; decoy not admitted. **Stopped.**
- *Attack C (row 6, Pattern 5):* fragment has no real `[Install]` header but a comment `# no [Install] by design` and a Description containing "Install". Repaired text: parsed under unit-file line grammar, only an actual section header counts; comment/substring does not. **Stopped.** (A *drop-in*-added `[Install]` — see advisory below — is the one residual surface.)
- *Attack D (row 10, Pattern 3):* `/opt/…/releases/2ce41e34…` is a bind mount over a clean `0555 0:0` decoy hiding a corrupted backing object. Repaired text: path-object rule compares a structurally parsed mount table against the deploy-channel-attested topology → unattested overlay STOPs. **Stopped.**

**V6 — Per-pattern coverage (0 patterns clean) consistent** — PASS. Report's pattern→finding map sums to 17 (P1:C01–03=3, P2:C04–05=2, P3:C06=1, P4:C07=1, P5:C08–10=3, P6:C11=1, P7:C12=1, P8:C13–14=2, P9:C15=1, P10:C16–17=2); each pattern has a genuine WP-I instance (incl. P4, which legitimately applies to unprivileged evidence children and to root-side RPD-VERIFY). No double-count; no pattern manufactured.

---

**Advisory observations (do NOT falsify the `17 repaired, 0 clean` claim — forward-looking successor items):**

1. **LOW — row 5 drop-in clause is unfalsifiable until a drop-in allowlist is pinned.** Location: §8.2 row 5 (line 427) "the effective fragment/drop-in set contains no unpreregistered override," against §2 (lines 140–157) which pins only the single `WPI_UNIT_FRAGMENT_SHA256`. Defect: "unpreregistered override" has no pinned set to compare against, so the clause cannot yet fail — the residual attack is a drop-in that adds an `[Install]` section (not caught by row 6, which parses only the fragment file) or a directive not covered by an effective-property row. Note ExecStart-altering and Environment/Restart drop-ins *are* caught by rows 5/9/3 via effective-value parsing, so the gap is narrow. Minimal fix: §2 should pin the accepted drop-in set (paths+hashes) for `mtc-bridge-first-start.service` or assert zero drop-ins, and name it as a third PIN item alongside R1/R2. This is a draft-completeness task, not a catalogue-pass regression; the pass correctly *requires* structural drop-in parsing (C08) — it just needs the pinned allowlist at dispatch.

2. **INFO — row 20 (401/403→STOP) and row 24 (refused/timeout→PASS) are defensible judgement calls, not defects.** 401/403→STOP mirrors the F3 authorization-failure→STOP principle; refused/timeout both satisfy the "external cannot connect" predicate. No fix needed; recorded only because V2 invited scrutiny.

No file was modified.
