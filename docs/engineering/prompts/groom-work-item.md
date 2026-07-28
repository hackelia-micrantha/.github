# Prompt: groom an engineering work item

```text
Review and rewrite the supplied material as a well-groomed engineering work item.

The source may describe a bug, feature, design, plan, specification, investigation, infrastructure change, security improvement, RFC, or epic. Do not force every item into a user-story format.

First provide a concise grooming assessment:

- Primary work-item type
- Readiness: Draft / Needs discovery / Needs decisions / Needs decomposition / Ready for implementation
- Intended outcome
- Missing information or evidence
- Hidden dependencies
- Primary risks
- Recommended priority and labels
- Whether the work should be split
- Whether QART, RFC, ADR, specification, or investigation artifacts are required

Then rewrite the item using only sections that add value:

- Title
- Executive summary
- Context
- Problem or opportunity
- Goals
- Non-goals
- Stakeholders and actors
- Current state
- Desired state
- Requirements
- Constraints and quality attributes
- Proposed approach
- Alternatives and trade-offs
- Architecture and data flow
- Interfaces and contracts
- Security and governance
- Operational design
- Migration and compatibility
- Validation strategy
- Acceptance criteria
- Delivery slices or workstreams
- Dependencies
- Risks and mitigations
- Open questions
- Documentation outputs
- Definition of done
- Epic success measures and exit criteria

Rules:

- Make the artifact understandable without chat history.
- Preserve evidence, constraints, and accepted decisions.
- Separate facts, assumptions, recommendations, and unresolved questions.
- Separate the problem from the proposed implementation.
- Use an outcome-oriented title.
- Define explicit goals and non-goals.
- Convert vague claims into observable or verifiable properties.
- Do not invent missing requirements or claim unverified system behaviour.
- Include happy, failure, and adversarial paths when material.
- Include security, privacy, governance, trust boundaries, operability, compatibility, migration, rollout, and rollback when material.
- Prefer independently reviewable and mergeable delivery slices.
- Recommend an ADR only for a decision that has actually been accepted.
- Recommend QART when alternatives remain unresolved.
- Recommend an RFC when the change crosses important boundaries, affects public contracts, requires broad review, or is expensive to reverse.
- Avoid ceremonial sections that do not improve decisions or delivery.

Source material:
<PASTE ISSUE, PLAN, DESIGN, SPECIFICATION, OR NOTES HERE>
```
