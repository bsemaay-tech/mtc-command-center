# ADR-0006 - single-writer and lockfile before database

Status: Accepted

Context: Multiple AI agents can corrupt JSON if they write concurrently.

Decision: Use one writer, resource lockfiles, backups, validation, and atomic replace before considering a database.

Consequences: Controlled writes are deferred to MVP-2.
