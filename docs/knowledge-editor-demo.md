# Organization Standards with Knowledge Editor

The Knowledge Editor is the control plane for teaching the AI assistant how this
organization builds software. Security teams and platform owners can turn local
practice into searchable guidance that agents retrieve during code generation.

## What to capture

Create a knowledge entry for each standard that needs consistent enforcement.
Include:

- **Rule:** the required behavior.
- **Context:** the repositories, teams, or frameworks where it applies.
- **Good example:** a compliant implementation.
- **Bad example:** a recognizable anti-pattern and why it is rejected.
- **Verification:** the test, scanner, or review step that proves compliance.
- **Owner and revision:** who approves changes and when the rule was last reviewed.

For example, an SSO entry might specify that applications must use the approved
OIDC provider, validate issuer and audience claims, require PKCE for public
clients, and never implement a second password store. An API-format entry might
require versioned `/v1` routes, a standard error envelope, ISO-8601 timestamps,
and documented pagination fields.

Do not place client secrets, signing keys, passwords, or personal data in the
knowledge base. Describe secret locations and rotation procedures instead.

## Publish and retrieve

1. In the Armis platform, open **Knowledge Editor**.
2. Create or update the organization standard and add its scope, examples,
   verification criteria, and owner.
3. Submit it through the organization review and approval process.
4. Publish the approved revision to the organization knowledge base.
5. Install the Knowledge integration for the assistant. For Claude Code:

```bash
armis-cli install knowledge
```

The CLI documentation states that this adds `/knowledge`, `/cwe-fix`,
`/cwe-fix-report`, `/framework-guidance`, and `/tech-guidance`. The agent can
also call the knowledge integration while generating code. Credentials use
`ARMIS_CLIENT_ID` and `ARMIS_CLIENT_SECRET`; the tenant is resolved server-side.

## Live VS Code demonstration

In Copilot Chat, ask:

> Retrieve the organization standards for SSO and API response formats. Create a
> new endpoint that authenticates through the approved OIDC provider and returns
> a paginated response using the required error envelope. Cite the applicable
> standards and propose verification checks before editing files.

The assistant should retrieve the published guidance, apply the organization’s
specific rules, and identify any missing implementation detail rather than
inventing a local convention.

Then ask:

> Review the endpoint against the retrieved organization standards and the Armis
> security rules. Scan the changed files, report HIGH or CRITICAL findings, and
> recommend a compliant fix for every finding. Do not suppress findings.

Run the local gate as an independent check:

```bash
armis-cli scan repo . --changed=uncommitted --fail-on HIGH,CRITICAL
```

## Demonstrate a policy update

Change the API standard in Knowledge Editor, for example by requiring a new
`trace_id` field in every error response. Publish the reviewed revision, then
ask the assistant to review the endpoint again. The next response should identify
the newly required field and update the implementation or tests accordingly.

This demonstrates the lifecycle: an owner authors a rule, reviewers approve it,
the platform publishes it, the assistant retrieves it during generation, and the
scanner and CI gate verify the resulting code.
