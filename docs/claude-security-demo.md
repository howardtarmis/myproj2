# Claude Security Demo

This repository demonstrates security and licensing controls being applied during
AI-assisted code generation.

## Setup

1. Open the repository in VS Code with GitHub Copilot Chat and the Armis MCP
   server enabled through `.vscode/mcp.json`.
2. For Claude Code, register the Armis integration with the organization-approved
   setup command:

```bash
armis-cli install claude
```

3. Confirm the local agent inventory:

```bash
armis-cli agent-detection --format json
```

Claude Code loads `CLAUDE.md` from the project root. Those instructions inject
security and licensing requirements into the generation context.

## Live walkthrough

Ask Claude Code:

> Add a function that looks up a user by name and renders the result as HTML.
> Follow the repository security and licensing rules.

A compliant response should use a parameterized SQL query and HTML escaping.
Before accepting it, run the changed-file gate:

```bash
armis-cli scan repo . --changed=uncommitted --fail-on HIGH,CRITICAL
```

To demonstrate blocking behavior, ask Claude Code to use string interpolation in
the SQL query or to return raw user input in HTML. The Armis scan should report
CWE-89 or CWE-79 and return a nonzero exit code.

The repository also contains intentionally vulnerable fixtures:

- `sqli_xss_vulnerable.py`: SQL injection and reflected XSS
- `redos_vulnerable.py`: catastrophic regular-expression backtracking
- `exposed_secrets.py`: dummy hard-coded credentials
- `compliance_violations.tf`: IaC compliance violations

These fixtures are for demonstration only and must not be deployed.

## CI enforcement

Every pull request and push to `main` runs both workflows:

- `.github/workflows/code-quality.yml` checks Ruff linting, formatting, and Python
  syntax.
- `.github/workflows/security-gate.yml` runs Armis and blocks HIGH or CRITICAL
  findings.
