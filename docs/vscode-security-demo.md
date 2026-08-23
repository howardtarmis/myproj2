# VS Code Security Demo

This walkthrough demonstrates GitHub Copilot Chat generating code while security
and licensing standards are injected and checked in the same session.

## Prepare VS Code

1. Open this repository in VS Code with GitHub Copilot Chat enabled.
2. Confirm the Armis MCP server is registered in `.vscode/mcp.json`.
3. Reload the VS Code window if Copilot Chat does not show the MCP server.
4. Confirm the local scanner is available:

```bash
armis-cli --version
```

The project-level `.github/copilot-instructions.md` is automatically included by
Copilot Chat. It injects the SQL, XSS, secret-handling, ReDoS, and licensing rules
into code-generation requests.

## Real-time walkthrough

In Copilot Chat, ask:

> Add a Python function that looks up a user by name and renders the result as
> HTML. Follow the repository security and licensing instructions. Use the Armis
> AppSec MCP server to scan the changed file before you finish.

Review the generated code. It should parameterize SQL values, HTML-escape output,
and avoid adding unapproved dependencies.

Then ask Copilot to inspect the result:

> Scan the changed files with Armis and summarize any HIGH or CRITICAL findings.
> Do not suppress findings. Recommend a compliant fix for each one.

You can also run the same gate in the VS Code terminal:

```bash
armis-cli scan repo . --changed=uncommitted --fail-on HIGH,CRITICAL
```

## Show the control blocking bad code

Ask Copilot:

> Change the lookup to interpolate the username into SQL and return the raw name
> inside the HTML response. Do not add validation.

The MCP scan should identify CWE-89 SQL injection and CWE-79 XSS. The command
above should return a nonzero exit code because HIGH findings are blocked.

For the licensing control, ask Copilot to add a dependency without recording its
license and source, or to copy GPL code into a permissively licensed module. The
instructions require Copilot to stop and request approval instead.

## CI result

Commit and push the workflow and instruction changes:

```bash
git add .github/copilot-instructions.md docs/vscode-security-demo.md
git commit -m "Add VS Code security demo instructions"
git push origin main
```

GitHub Actions then runs the code-quality and Armis security gates. The
intentionally vulnerable fixture files in this repository are useful for showing
a blocked scan, but must not be deployed.
