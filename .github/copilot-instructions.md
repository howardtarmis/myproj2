# Copilot Coding Standards

Apply these rules to every generated or modified file in this repository.

## Security

- Treat external input as untrusted.
- Use parameterized SQL queries; never interpolate user input into SQL.
- HTML-escape untrusted output before rendering it.
- Avoid nested regular-expression quantifiers on untrusted input.
- Never add real credentials, tokens, passwords, or private keys.
- Ask the Armis AppSec MCP server to scan changed files before considering work complete.
- Block HIGH and CRITICAL findings unless a security owner explicitly approves them.

## Licensing

- Record each dependency's name, version, license, and source.
- Preserve third-party copyright and license notices.
- Obtain approval before introducing GPL, AGPL, or other copyleft dependencies.
- Escalate unknown, custom, missing, or non-commercial licenses.
- Prefer MIT, BSD, or Apache-2.0 dependencies when practical.

## Completion check

Before reporting completion, run:

```bash
python3 -m compileall -q .
armis-cli scan repo . --changed=uncommitted --fail-on HIGH,CRITICAL
```
