# Dashboard verification

- Run the affected API/read-model and frontend tests, lint/typecheck if configured.
- Visually verify the real rendered route at desktop and phone widths; do not accept source review as
  visual evidence.
- Confirm missing/stale/malformed/unevaluable fixtures fail closed and are never shown as ready/PASS.
- Verify `/dashboard` and existing read-only endpoints remain compatible.
- Confirm no network target, credential, command execution, write action, broker/paper/live control,
  or unrelated generated asset entered the diff.
