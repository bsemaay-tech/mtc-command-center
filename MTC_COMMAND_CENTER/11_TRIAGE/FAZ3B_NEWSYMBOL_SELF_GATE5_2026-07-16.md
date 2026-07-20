# FAZ 3B New-Symbol Design — Self-Adversarial Review (2026-07-16)

Reviewer: Claude Fable 5 — reviewing **my own** design. A self-review is weaker than an
independent Gate-5 by construction; this document exists so an independent reviewer starts from
the known defects rather than rediscovering them. **An independent Codex Gate-5 is still
required before approval** (pre-reg §12).

Target: `00_AGENT_PROTOCOLS/FAZ3B_STAGE2_NEWSYMBOL_CONFIRM_PREREG_2026-07-15.md`
+ tooling on branch `feature/exit-aware-gauntlet`.
**No backtest, download, smoke, gauntlet, or trading action was performed.**

## Verdict: CONDITIONALLY SOUND — 2 blocking gaps found and fixed, 3 open risks stated

## A. Symbol virginity — OK (verified, but scan scope disclosed)

Re-derived: 68 symbols have ever appeared in a `GEN_KELTNER_BREAKOUT` row across 145 MEGA result
files in `05_BACKTEST_RESULTS/` + `research/`, plus filename-encoded eval/scorecard artifacts.
None of the 16 frozen symbols appears. **Scan scope is honest but not infinite:** it covers
MEGA result/partial/iter JSONs and `*KELTNER*` filenames. A Keltner result hiding in a
differently-named artifact would be missed. Mitigation: the pre-reg mandates a launch-time
re-scan (Gate 1.1), and any hit voids that symbol.

## B. BLOCKING GAP FOUND #1 — the acquisition command was fabricated (FIXED)

My first draft's §5 command used `--bundle-id` and `--symbols`. **Neither existed.** The real
downloader had `--bundle-name` and a **hardcoded `EQUITY_UNIVERSE`** with no per-symbol override
— the step-0 command would have failed immediately, and the "executable now" claim was false.
Fixed: added additive `--symbols` / `--asset-class` flags (`build_universe()`), default path
byte-identical to the historical universe, `EQUITY_UNIVERSE` never mutated, unit-tested
(`test_downloader_default_universe_unchanged`, `test_downloader_explicit_symbols_override`).
§5 now carries the real interface. **Lesson: this is the same class of error as the Gate-5 FATAL
it replaces — asserting an interface without reading it.**

## C. BLOCKING GAP FOUND #2 — the gauntlet orchestrator is a stub (OPEN, disclosed)

`exit_aware_gauntlet.py` has tested primitives (`build_config_matrix`, `verdict`) but its
`main()` deliberately raises. **The gauntlet cannot run end-to-end today even with approval.**
The pre-reg §6 says the tooling is "built + unit-tested" — true — but a reader could infer it is
run-ready. It is not. Wiring `main()` (load cell spec → df → CPCV + matrix→PBO + strict
multiwindow → stamped verdict JSON) is a remaining task, and it must be written BEFORE approval
so the approved artifact is the thing that actually runs.

## D. Statistical framing — corrected mid-review, now defensible

My first §8 deflated every cell by the full historical N=5,795. **That was wrong**: the config is
frozen and evaluated on symbols it was never selected on, so charging the prior search again is
double-counting — the whole point of out-of-sample testing. Corrected to: PRIMARY = within-run
multiplicity only (`du_family = 1 − min(1, m(1−du_cell)) ≥ 0.95`, BH-FDR Q=0.10, ≥2 groups);
SECONDARY = the N=5,795 union-DSR as a conservatism diagnostic that can only *downgrade* an
outcome to A′, never upgrade. Both pre-registered, so neither can be renegotiated post-hoc.
**Residual objection an independent reviewer should press:** the new symbols share the 2020-2026
era, so "fresh data" is not fully independent; if a reviewer judges the era-sharing severe, the
primary should be the secondary. I state the trade-off rather than hide it.

## E. OPEN RISK #1 — trade-count feasibility (design may be underpowered)

The bar is ≥30 lockbox trades/cell and CPCV needs enough trades per 2-group test window
(~2,950 bars). Stage-1's AAPL cell got 49 lockbox trades in ~2,200 bars. **Low-volatility ETFs
in G3 (USMV, QUAL) and possibly G2 could fall short**, producing INSUFFICIENT_TRADES /
CPCV N_A → GAUNTLET_FAIL by rule. If several cells die this way the run is underpowered rather
than informative. This cannot be resolved without running. Honest options: accept the risk;
or pre-register a minimum-viable-cell count (e.g. VOID if <8 cells reach ≥30 trades) — the
pre-reg §5 already voids below 8 symbols/2 groups on acceptance, but NOT on trade count. **Recommend
adding a trade-count VOID rule before approval.**

## F. OPEN RISK #2 — the honest-limitation framing is doing heavy lifting

§4's disclosure ("new symbols, not new time") is correct but is the design's whole defence
against the correlation objection. G2 (international) is the strongest mitigation, yet EWJ/EWG/
INDA/EWZ are US-listed ETFs whose 2020-2026 drawdowns still correlate with the US macro cycle.
**A reviewer could reasonably rate this design as materially weaker than the 2028 forward window
and prefer waiting.** That is Barış's trade-off to make, explicitly, not mine to bury.

## G. OPEN RISK #3 — self-review is not independent review

I designed this and reviewed it. I found two blocking gaps in my own work within one pass, which
is evidence the design was NOT review-ready when written — and weak evidence that a third gap
does not remain. An independent adversarial pass is mandatory.

## REQUIRED BEFORE APPROVAL

1. Wire `exit_aware_gauntlet.main()` end-to-end (§C) and unit-test the wiring.
2. Add a trade-count VOID rule to the pre-reg (§E).
3. Independent Codex Gate-5 on the pre-reg + the tooling diff.
4. Then, and only then, Barış's written approval → acquisition → smoke → run.

## Execution statement

No run of any kind was performed. Nothing in this review authorises a download, a backtest, a
gauntlet, paper trading, or a promotion.
