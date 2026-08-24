# Incident Retrospective Prompt

Use this prompt after an incident has been contained and the goal is to produce a blameless retrospective that identifies contributing factors, validates remediation, and converts learning into durable controls.

Do **not** use this prompt during active containment — the priority is stopping the incident, not documenting it. Do **not** use it for routine bug triage — use [issue grooming](issues/issue-grooming.md) or [merge-gate review](pull-requests/merge-gate-review.md).

```markdown
# Incident retrospective

Produce a blameless retrospective for **[INCIDENT / SYSTEM / TIME PERIOD]** in **[REPOSITORY / PROJECT / ECOSYSTEM]**.

## Context

- **Incident summary:** [ONE SENTENCE]
- **Time window:** [START] to [RESOLVED]
- **Affected systems or repositories:** [SCOPE]
- **Severity and impact:** [USERS / DATA / SECURITY / OPERABILITY / DELIVERY]
- **Mutation authorization:** [READ ONLY / CREATE FOLLOW-UP ISSUES]

## Execution boundary

Begin read-only. Treat incident timelines, logs, monitoring data, post-incident communications, and participant recollections as evidence. Do not assign blame to individuals. Focus on system properties, controls, and contributing factors.

## Retrospective principles

- **Blameless.** People act with available information and incentives. Fix the system, not the person.
- **Evidence over narrative.** Distinguish verified timeline events from assumptions and reconstruction.
- **Contributing factors, not root cause.** Incidents rarely have a single cause. Identify the conditions that combined.
- **Durable controls.** Prefer detection, automation, and architecture changes over process reminders.

## Evidence to inspect

Inspect applicable:
- incident timeline, alerts, and monitoring data;
- logs, traces, and deployment records;
- pull requests, configuration changes, and infrastructure changes during the window;
- prior related incidents, near-misses, and known limitations;
- runbooks, on-call procedures, and escalation paths;
- communication channels (incident channels, status pages, external reports).

## Retrospective dimensions

### 1. Timeline

Reconstruct the verified sequence: detection, acknowledgment, containment, mitigation, resolution. Note where the timeline is uncertain or reconstructed.

### 2. Impact

Describe the observable effect on users, operators, data, security, or delivery. Distinguish direct impact from cascading effects.

### 3. Contributing factors

Identify the conditions that allowed the incident. Common categories:
- detection gap (no alert, slow alert, alert fatigue);
- architecture or boundary weakness (missing isolation, fail-open, shared state);
- process or review gap (missing check, skipped validation, stale runbook);
- knowledge or communication gap (undocumented assumption, unclear ownership);
- change or deployment risk (untested path, missing rollback, partial migration);
- dependency or infrastructure failure (external service, resource exhaustion, drift).

### 4. What worked well

Identify the controls, decisions, and responses that limited impact or accelerated recovery. Preserve these.

### 5. Remediation and follow-up

Separate:
- **Containment** — already done to stop the incident.
- **Corrective** — fixes the immediate defect or gap.
- **Preventive** — reduces the probability or impact of similar incidents (detection, architecture, automation, runbooks, tests).
- **Observability** — improves detection, diagnosis, or evidence for future incidents.

### 6. Durable controls

For each follow-up item, identify:
- the control type (detection, prevention, mitigation, recovery);
- the owning repository and accountable owner;
- the smallest bounded implementation slice;
- the evidence that proves the control works;
- priority (P0–P3) and the incident severity that justifies it.

## Required output

### A. Incident summary

State the incident, time window, severity, affected systems, and current status.

### B. Timeline

Present the verified sequence. Mark uncertain or reconstructed entries explicitly.

### C. Impact assessment

Describe the observable effect and the population affected.

### D. Contributing factors

List the conditions that combined. Do not reduce to a single root cause.

### E. What worked

Identify effective controls and responses to preserve.

### F. Follow-up items

| Priority | Control type | Description | Owner | Repository | Evidence | Outcome |
| --- | --- | --- | --- | --- | --- | --- |

Group related items into coherent, independently verifiable outcomes. Do not create one issue per minor observation.

### G. Recommendations

Recommend the smallest set of durable controls that materially reduce the probability or impact of similar incidents. Prefer detection and automation over process.

## Authorized follow-up mode

When issue creation is explicitly authorized:

1. Create bounded follow-up issues in the owning repositories.
2. Link each issue to the retrospective.
3. Preserve unique findings before consolidating duplicates.
4. Do not mark preventive work as lower priority merely because the incident is resolved.
5. Report the created issues and any remaining untracked work.
```

Compact invocation:

> Produce a blameless retrospective for **[INCIDENT]**: reconstruct the timeline, identify contributing factors (not blame), separate containment from corrective and preventive work, and return bounded follow-up issues with accountable owners.
