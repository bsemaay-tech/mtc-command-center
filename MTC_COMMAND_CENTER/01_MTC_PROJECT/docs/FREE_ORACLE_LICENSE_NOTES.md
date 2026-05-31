# Free Oracle License Notes

- Command: `web search official/GitHub/PyPI license pages for PineTS, PyneCore, vectorbt, backtesting.py, backtrader`
- Data hash: not applicable
- Config hash: not applicable
- Code hash: `fbc1392b1f1065a418eabcd5149259f98087b55c`

## PineTS

- Source checked: `https://github.com/QuantForgeOrg/PineTS`, `https://www.jsdelivr.com/package/npm/pinets`
- License observed: AGPL-3.0 / commercial dual license.
- Local POC mark: Caution.
- Decision: usable as local/internal signal oracle, but avoid deep proprietary distribution or SaaS use without approval.

## PyneCore

- Source checked: `https://github.com/PyneSys/pynecore`, `https://pypi.org/project/pynesys-pynecore/`
- License observed: Apache-2.0 for open-source runtime.
- Local POC mark: Safe for local POC.
- Decision: use manual Python translations only. Do not use paid PyneComp/PyneSys compiler or API-key Pine conversion.

## vectorbt

- Source checked: `https://vectorbt.dev/terms/license/`, `https://vectorbt.dev/terms/`
- License observed: Apache-2.0 with Commons Clause.
- Local POC mark: Caution.
- Decision: safe enough for local research/POC, but avoid productizing or selling a service whose value substantially derives from vectorbt without approval.

## backtesting.py

- Source checked: `https://pypi.org/project/backtesting/`, `https://github.com/kernc/backtesting.py`
- License observed: AGPL-3.0.
- Local POC mark: Caution.
- Decision: optional sanity checker only. Avoid deep integration without approval.

## backtrader

- Source checked: `https://github.com/backtrader/backtrader-docs`, `https://www.backtrader.com/`
- License observed: GPL-3.0 for docs repository; main project should be checked again before integration.
- Local POC mark: Caution.
- Decision: lower priority fallback. Do not implement unless useful and approved.
