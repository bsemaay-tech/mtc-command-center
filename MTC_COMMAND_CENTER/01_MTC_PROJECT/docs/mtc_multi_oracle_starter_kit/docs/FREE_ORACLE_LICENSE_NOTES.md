# Free Oracle License Notes

This document is not legal advice. It is a practical engineering risk note for local research/POC use.

| Tool | Reported license profile | Local POC risk | Deep integration risk | Action |
|---|---|---:|---:|---|
| PineTS | AGPL-3.0 + commercial license | Low for private/internal research | Medium/high if distributed or offered as service | Use as external CLI/oracle; avoid embedding into proprietary app without review |
| pinets-cli | AGPL-3.0 | Low for private/internal research | Medium/high if distributed | Use as local CLI tool |
| PyneCore | Apache 2.0 core | Low | Low for core runtime | Good POC candidate |
| PyneComp compiler | Separate closed-source/SaaS | Not free | Not compatible with “fully free” requirement | Do not use in this project |
| vectorbt | Open-source community edition; package/license terms should be checked in repo | Low for local research | Medium until exact license constraints verified | Use as optional oracle; document version/license |
| backtesting.py | AGPL-3.0 | Low for local research | Medium/high for distribution/service | Optional sanity runner only |
| backtrader | GPL-3.0 | Low for local research | Medium/high for distribution | Lower priority fallback only |

## Engineering policy

1. Do not embed AGPL/GPL engines into core proprietary code without review.
2. Prefer running restrictive tools as isolated CLI/process or optional experiment.
3. Keep generated normalized CSV/JSON outputs separate from tool source code.
4. Document exact package version and license in every oracle report.
