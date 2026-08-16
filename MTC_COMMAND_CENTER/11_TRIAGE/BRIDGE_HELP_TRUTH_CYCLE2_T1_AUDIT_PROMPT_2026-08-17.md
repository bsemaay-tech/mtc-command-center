# Bridge Help truth cycle 2 — fresh T1 audit prompt

You are the single fresh flagship auditor for a T1 non-economic product/docs
repair. Use exact `gpt-5.6-sol` at `high` effort. Work read-only in
`C:\BRIDGE_HELP_IMPL`. Do not edit, commit, reset, stash, clean, or contact any
host.

Read:

- `C:\LAB\Tradingview_LAB_CLEAN\AGENTS.md`
- `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\BRIDGE_HELP_TRUTH_CYCLE2_GATE1_2026-08-17.md`
- the actual six-file uncommitted Help/System Map diff in `C:\BRIDGE_HELP_IMPL`
- the relevant runtime/config sources cited by `help_map.json`

Audit the complete Help feature, with special attention to the two fresh-cycle
repairs:

1. The LLM gate must be described as dormant/unwired scaffolding. Runtime uses
   `NullLLMGate`; toggling the YAML flags does not activate it. Store/logging and
   risk/dashboard connections are planned. Preserve the future narrowing-only
   economic boundary.
2. Dashboard V1 must be described as six original pages plus Help, a next-bar
   UTC time rather than a countdown, a snapshot on connection, and no automatic
   client reconnect handler. Readiness gaps must not be duplicated.

Independently inspect source truth; do not trust the implementer report. Execute:

```text
python -m pytest IBKR_PAPER_BRIDGE/tests/test_dashboard_static.py -q
node --check IBKR_PAPER_BRIDGE/bridge/static/app.js
git diff --check
```

Also execute the complete Bridge suite if feasible. The known baseline is two
unrelated failures: the canonical deployment-ledger fixture hash and the WAL
schema-version expectation (`4 != 2`). Classify any additional failure.

Check that the new D026 tests genuinely discriminate the named wrong wording,
that `planned_v2` plus `status_detail` does not misleadingly say the source class
is absent, that no control/economic authority leaked into AI or Help, that the
frontend stays dependency-free/private/text-only, and that the AI-facing index
does not duplicate the JSON knowledge base.

Return exactly one verdict: `PASS`, `PASS-WITH-NITS`, `REQUEST_CHANGES`, or
`BLOCK`. List required findings separately from optional nits. Do not claim
deployment or acceptance authority.
