# Governance stage verification

- Run the task's published command verbatim. Do not substitute extraction or simulation for the
  real artifact. If results disagree, record a finding.
- For every regression test offered as closure evidence, show RED against pre-fix behavior or a
  deliberate equivalent mutant and GREEN with the fix. If neither is practical, label it
  supplemental and do not claim closure.
- Gate-5 auditors state for every new test whether they verified its RED/GREEN evidence; identify
  each unverified test instead of implying it was reproduced.
- A carried regression fence changes only with a discriminating-power proof: old and new assertion
  against the same deviant output. Establish old behavior by execution, not reading.
- Verify persisted encoding, clock domain, hashes, sizes, and identity on disk. With text
  normalization, state both byte forms or pin the Git blob OID.
- Grep every corrected old value/claim repo-wide. Verify linked paths exist. For indexes/status
  outputs, regenerate twice and require deterministic clean output.
- Commands exceeding the 600-second foreground ceiling use a background supervisor. One overnight
  loop only; unattended multi-hour work requires verified AC/DC sleep and hibernate disabled.
- Before any commit: inspect exact diff, run scoped tests, run the repo guard/hook normally, and
  confirm no foreign edits or forbidden paths are staged. Never use `--no-verify`.
- Autonomous turns keep active delegated work or an explicit wake condition. Window-capped rounds
  record quota preflight and preserve labelled committed partial state if interrupted.
