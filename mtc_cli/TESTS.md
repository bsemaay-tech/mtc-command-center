# MTC CLI verification

- Execute the real CLI entrypoint for happy path and at least one failure path.
- Show RED/GREEN for defect closure; direct function calls are supplemental when the CLI wrapper is
  part of the contract.
- Validate UTF-8, Windows paths, exit codes, stdout/stderr contract, schema, backups, atomicity, lock,
  and event output as applicable.
- Confirm fixtures/logs contain no secrets and no frozen-legacy, host, broker, deploy, or live path is
  reached outside explicit authorization.
