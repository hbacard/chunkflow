# Security Policy

ChunkFlow takes security seriously. This document describes how to report
vulnerabilities and what you can expect.

## Reporting a vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

Please report vulnerabilities privately by email to the maintainer:

- **Maintainer:** Hugo Bacard
- **Email:** `hugo.bacard@ijclab.in2p3.fr`
- **GPG / PGP key:** _optional — request one by email before sending sensitive details_

Please include as much of the following as possible:

- The affected version / commit
- A description of the vulnerability and its impact
- Steps to reproduce
- Any suggested fix

Sensitive information is kept confidential until a fix is released.

## Response expectations

- **Acknowledgement:** within 5 business days of receipt
- **Status update:** we will share a timeline for the fix
- **Disclosure:** coordinated public disclosure after a fix is released

## Scope

The core `chunkflow` package, the MCP server (`mcp/`), and the Docker deployment
configuration. Third-party dependencies are tracked via Dependabot; for
vulnerabilities in dependencies, follow the respective upstream advisory
process.
