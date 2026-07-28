# Prompt: review an engineering artifact

```text
Critically review the supplied engineering artifact. It may be a QART slice, RFC, ADR, plan, epic, specification, design, investigation, or delivery issue.

Do not merely summarize or praise it. Identify defects that could cause incorrect decisions, unsafe implementation, hidden scope, operational failure, or repeated rediscovery.

## Review dimensions

### Purpose and classification
- Is the artifact the correct type for the work?
- Is it being used at the correct decision maturity?
- Is unnecessary ceremony obscuring a simpler decision?

### Problem and scope
- Is the underlying problem stated independently of the proposed solution?
- Are goals and non-goals explicit?
- Are multiple independently valuable outcomes incorrectly combined?

### Decision quality
- Are decision questions neutral and bounded?
- Are credible alternatives considered?
- Are recommendations supported by evidence?
- Are trade-offs, residual risks, and revisit triggers explicit?
- Does an ADR record a real accepted decision rather than an active proposal?

### Architecture and contracts
- Are responsibilities, state ownership, data flow, control flow, and trust boundaries clear?
- Are public interfaces, error semantics, versioning, and compatibility constraints defined?
- Are implicit dependencies or cross-repository effects missing?

### Security and governance
- Are assets, authority, threats, secrets, sensitive data, approvals, provenance, and audit evidence addressed where material?
- Is fail-open versus fail-closed behaviour explicit?
- Could the proposal create confused-deputy, privilege-escalation, bypass, replay, tampering, or supply-chain risks?

### Operations
- Are observability, deployment, capacity, recovery, rollback, incident handling, and ownership sufficient?
- Are partial failures and degraded modes defined?

### Delivery and verification
- Can the work be delivered in independently reviewable slices?
- Are acceptance criteria observable and testable?
- Do validation plans cover happy, failure, compatibility, and adversarial paths?
- Are success measures connected to the stated outcome?

### AI-generated-content risks
- Identify claims that appear invented, unsupported, overly certain, or disconnected from repository evidence.
- Identify placeholders or generic boilerplate masquerading as analysis.
- Identify requirements added without an accountable source.

## Output

### Verdict
Choose one:
- Ready
- Ready with minor fixes
- Needs decisions
- Needs evidence
- Needs decomposition
- Wrong artifact type

### Findings
Order findings by severity:
- Blocking
- Significant
- Minor

For each finding include:
- Location or topic
- Problem
- Why it matters
- Concrete correction

### Missing decisions or evidence
List only material gaps.

### Recommended artifact changes
State whether to split, merge, replace, downgrade, or promote artifacts in the QART -> RFC -> ADR -> plan -> specification -> delivery chain.

### Revised structure
Provide a corrected outline or full rewrite when enough information exists. Do not invent missing decisions.

Artifact to review:
<PASTE ARTIFACT HERE>
```
