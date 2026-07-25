# Security Policy

## Reporting a vulnerability

Please do not disclose security vulnerabilities in public issues. Contact the repository owner privately through GitHub and include a minimal reproduction, affected version, and impact.

## Scope

The bridge deliberately limits commands, validates envelopes, uses local filesystem queues, and requires future write commands to be explicitly confirmed. Reports involving command validation, path escape, unsafe logging, queue tampering, or unexpected model modification are in scope.
