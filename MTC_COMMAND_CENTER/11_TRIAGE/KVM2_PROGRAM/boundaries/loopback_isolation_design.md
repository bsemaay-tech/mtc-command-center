# Same-host loopback/control-plane isolation design

- Status: **DEFERRED / BLOCKED — P5-10 NOT IMPLEMENTED**

This placeholder exists at the canonical path so no later task can silently
invent a second location. Loopback binding protects against remote exposure but
does not prevent another local identity from connecting. No AI-lab workload may
be admitted until a separately authorized design selects and implements an
OS-enforced mechanism, runs the complete negative-test suite from the final lab
identity and child processes, preserves the owner SSH tunnel, and receives fresh
Gate 5/Gate 6 acceptance.

The future design must cover IPv4/IPv6 loopback, alternate host routes, proxy
variables, inherited descriptors, service-control buses, bridge paths,
process/ptrace access, agent/private-key sockets, root/container sockets, host
metadata, shared temporary memory, journal access, abstract Unix sockets,
kernel keyrings, and unapproved egress. No architecture is selected here.
