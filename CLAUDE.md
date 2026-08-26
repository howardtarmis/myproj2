# Claude Code Project Rules

Apply these rules to every generated or modified file in this repository.

## Security

- Treat all external input as untrusted.
- Use parameterized SQL queries; never interpolate user input into SQL.
- HTML-escape untrusted output before rendering it.
- Avoid regular expressions with nested quantifiers on untrusted input.
- Never add real credentials, tokens, passwords, or private keys to source.
- Run the Armis AppSec scan on changed files before considering work complete.
- Block HIGH and CRITICAL findings. Do not suppress a finding without explicit review.

## Licensing

- Record every dependency's name, version, license, and source.
- Preserve third-party copyright and license notices.
- Obtain approval before adding GPL, AGPL, or other copyleft dependencies.
- Escalate unknown, custom, missing, or non-commercial licenses.
- Prefer MIT, BSD, or Apache-2.0 dependencies when practical.

## Verification

Before reporting a change as complete, run the narrowest applicable checks:

```bash
python3 -m compileall -q .
armis-cli scan repo . --changed=uncommitted --fail-on HIGH,CRITICAL
```
