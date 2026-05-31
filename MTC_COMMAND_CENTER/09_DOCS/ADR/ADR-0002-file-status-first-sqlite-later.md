# ADR-0002 - file status first, SQLite later

Status: Accepted

Context: AI agents and the user need inspectable state before database complexity.

Decision: Use JSON/Markdown first; add SQLite later only for indexing or scaling.

Consequences: MVP-0/MVP-1 stay simple and file-based.
