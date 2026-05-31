# Status Schema Notes

Status JSON files are the dashboard-facing data contracts for MCC. They should remain valid JSON at all times and should be updated only by assigned tasks.

## Rules

- Use `null` when a value is unknown or not generated yet.
- Use `not_connected_yet` when a reader or integration has not been implemented.
- Use `WAITING_FOR_USER` inside task or case status fields when required source data is missing.
- Do not store secrets in any status file.
- Prefer append-only report artifacts for detailed diagnostics; keep status JSON concise.

## Dashboard Expectations

The future dashboard should treat these files as read-only inputs. It should display missing data clearly instead of assuming success.
