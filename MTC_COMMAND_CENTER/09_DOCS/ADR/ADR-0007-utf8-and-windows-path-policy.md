# ADR-0007 - UTF-8 and Windows path policy

Status: Accepted

Context: The local Windows environment can include Turkish characters and long paths.

Decision: Require explicit UTF-8 and canonicalize paths before optional long-path prefixing.

Consequences: MVP-0 includes path validation.
