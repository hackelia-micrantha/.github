# Micrantha observability profile v1

Status: **organization profile v1**

This profile is the minimal cross-project interoperability contract implementing the [observability standard](observability.md). It intentionally defines only the semantics Micrantha projects need to share.

It is not a telemetry SDK, collector, storage format, analytics backend, dashboard framework, or project-wide event registry.

## 1. Compatibility baseline

Implementations SHOULD use:

- OpenTelemetry APIs and data model for operational traces, metrics, and logs;
- OTLP for operational telemetry transport where an exporter/collector boundary exists;
- W3C Trace Context for supported distributed trace propagation;
- upstream OpenTelemetry semantic conventions whenever their meaning matches;
- CloudEvents 1.0-compatible envelopes for durable/interoperable domain events where such an envelope is warranted.

An implementation using an OpenTelemetry semantic convention whose stability is not Stable MUST pin/document the convention version or otherwise isolate the unstable naming behind an adapter.

The `otel.*` namespace is reserved by OpenTelemetry and MUST NOT be used for Micrantha-specific attributes.

## 2. Planes

An implementation MUST classify emitted data into one of these planes:

```text
operational telemetry
domain event
product/usage measurement
security/audit evidence
diagnostic artifact
alert/notification
```

One physical backend may store multiple planes, but their semantics, authority, retention, and access policies remain distinguishable.

## 3. Common operational identity

Operational observations SHOULD carry enough resource identity to establish:

```text
software/service/component
release/version
deployment/environment class
source revision when needed for diagnosis
schema/profile revision when needed for compatibility
```

Use upstream resource attributes first.

Project-specific identity values MUST be bounded and MUST NOT be blindly copied into metric dimensions.

## 4. Common result semantics

When a domain requires a result finer than OpenTelemetry span status, the following bounded vocabulary MAY be used:

```text
micrantha.operation.result =
  success
  cancelled
  degraded
  failed
```

Projects MAY define a stable diagnostic code:

```text
micrantha.diagnostic.code = <project-owned bounded identifier>
```

Examples:

```text
runner.memory_budget_exhausted
config.schema_invalid
policy.denied
dependency.unavailable
```

Rules:

- diagnostic codes are stable identifiers, not human prose;
- codes SHOULD remain low/bounded cardinality within a component;
- human-readable messages are separate;
- use upstream `error.type` and domain-specific upstream conventions where they accurately apply;
- do not duplicate an upstream semantic convention under `micrantha.*`.

Additional `micrantha.*` attributes require a demonstrated cross-project semantic gap. Project-specific attributes SHOULD normally use the project's own namespace.

## 5. Cardinality classes

Attributes used for metric dimensions MUST normally be drawn from bounded sets.

### Bounded

Typical metric-safe candidates:

```text
operation class
result
error class
component
runtime/platform class
workflow/job class
feature/config mode with a bounded enum
```

### Correlation/high-cardinality

Normally trace/event/log-only:

```text
trace/request/run/worker IDs
source revisions
repository/branch identifiers
filenames/paths
URLs
user/account identifiers
session identifiers
```

### Content

Excluded from generic telemetry unless explicitly permitted:

```text
stdin/stdout/stderr bodies
prompts/completions
memory contents
user-generated text
images/media
embeddings
arbitrary request/response bodies
environment maps
```

## 6. Configuration semantics

The profile does not mandate one Micrantha configuration file.

OpenTelemetry-native controls SHOULD remain authoritative for the OTel SDK/exporter layer where supported.

At minimum, implementations SHOULD support the semantic equivalents of:

```text
instrumentation: enabled | disabled
local_collection: enabled | disabled
remote_export: enabled | disabled
```

These controls are independent.

`OTEL_SDK_DISABLED=true` MUST be honored by an OTel-based implementation as disabling optional OTel SDK signal production according to the upstream SDK specification.

Project convenience surfaces MAY include, for example:

```text
--telemetry=off
--telemetry=local
--telemetry=export
```

but they MUST document their mapping to native configuration and MUST NOT alter the command's domain semantics.

Configuration precedence follows the [CLI interoperability standard](cli-interoperability.md) for CLI surfaces unless a repository documents a justified alternative.

## 7. Export modes

The common semantic modes are:

| Mode | Instrument | Keep/process locally | Remote export |
| --- | --- | --- | --- |
| `off` | no | no | no |
| `local` | yes | yes | no |
| `export` | yes | implementation-defined | yes |

A repository MAY expose different names or additional modes.

The common standard does not require remote export and does not require a collector to be running. Any optional remote export MUST have a documented disable/opt-out control at the appropriate operator, deployment, or end-user scope.

Optional telemetry exporter failure does not change the source operation's result.

## 8. CLI profile

For a CLI operation:

- telemetry is out-of-band from stdout/stderr;
- machine stdout remains valid according to the CLI contract;
- no implicit prompt is introduced by telemetry;
- arguments and content are excluded by default;
- short-lived export/flush work is bounded;
- a downstream broken pipe is not converted into telemetry failure;
- explicit trace context may be propagated when an orchestrator/process contract supports it;
- baggage/trace context is metadata, not identity or authority.

OpenTelemetry CLI semantic conventions MAY be used, but because their stability can evolve, projects SHOULD isolate them behind a small adapter rather than copy unstable attribute names throughout domain code.

## 9. Product measurement plan

A product/usage measurement SHOULD have a declaration equivalent to:

```yaml
measurement:
  id: runner-drain-adoption

question:
  What proportion of apply workflows use an explicit drain step?

decision:
  Decide whether drain should become the normal apply workflow.

events:
  - runner.drain.requested
  - runner.apply.requested

properties:
  - outcome

privacy:
  identity: none
  aggregate_locally: true
  generalize: true

retention: 30d

export:
  mode: local
  consent: not-applicable
```

Required semantics:

- `id`: stable measurement identifier;
- `question`: the question the measurement exists to answer;
- `decision`: optional decision/learning use;
- `events`: minimal event set;
- `properties`: explicit allowlist;
- `identity`: `none`, `pseudonymous`, or an explicitly justified identified mode;
- `aggregate_locally`: whether raw events can be reduced before export;
- `retention`: bounded retention;
- `export.mode`: no export, local-only, or policy-controlled remote export;
- `consent`: applicable consent/disclosure contract for user-facing measurement.

Projects MAY represent this declaration in YAML, JSON, code, documentation, or another validated form. V1 does not require a universal schema registry.

Analysis MAY use concepts such as funnels, flows, cohorts, retention, and segmentation. Those are analysis semantics, not a mandate for a specific vendor or custom analytics service.

## 10. Domain events

When a durable/interoperable domain event uses CloudEvents:

- the project/domain owns the event type vocabulary;
- event identity/correlation is not authority;
- payloads remain bounded and classified;
- trace context may be preserved when present;
- replaying an event does not grant permission to repeat an effect;
- operational trace/log events MUST NOT automatically become durable domain events.

Project profiles MAY further constrain CloudEvents source/type/versioning conventions.

## 11. Governance and audit evidence

Security/audit evidence is not disabled by optional telemetry controls when the governing contract requires that evidence.

Governed evidence MAY reference an operational trace, event, diagnostic, or measurement, but the governing domain owns:

- admissibility;
- integrity requirements;
- actor/authority binding;
- retention;
- verification;
- acceptance/rejection/indeterminate semantics.

Telemetry cannot promote itself into authoritative evidence.

## 12. Diagnostic bundle profile

A bounded diagnostic bundle MAY contain:

```text
generated_at
software/release/runtime identity
telemetry configuration state
recent stable diagnostic-code counts
bounded timing/counter summaries
dependency-health summaries
explicit exclusions/redaction metadata
```

It MUST NOT be a generic archive of logs, environment variables, prompts, user content, private files, or process memory.

## 13. Offline/store-and-forward compatibility

V1 defines compatibility requirements, not a custom storage implementation.

For temporary remote outages, reuse standard collector/exporter retry and persistent queue mechanisms when they solve the requirement.

A future intentional offline store MUST be able to enforce:

```text
bounded quota + retention
classification/redaction before persistence
encryption at rest where required
origin identity
schema/profile version
observed_at != stored_at != synchronized_at
idempotent sync/deduplication
expiry/deletion
export policy/consent at sync time
optional local aggregation/generalization
```

Operational telemetry SHOULD remain synchronizable as standard OTLP where practical.

Product measurement MAY synchronize aggregate summaries instead of raw events when the declared question does not require raw history.

No custom offline wire protocol is defined in v1.

## 14. Conformance checklist

A project claiming this profile should verify the applicable subset:

- [ ] upstream semantic conventions are used before custom ones;
- [ ] custom attributes are documented and bounded;
- [ ] optional instrumentation can be disabled;
- [ ] local-only/no-remote operation works;
- [ ] exporter failure cannot change an independent source operation result;
- [ ] metric dimensions meet cardinality policy;
- [ ] secrets/content are excluded by default;
- [ ] CLI stdout/stderr and machine output remain composable;
- [ ] product measurements have declared questions and bounded retention/export policy;
- [ ] domain events remain distinct from traces/log events;
- [ ] governed evidence is distinct from optional telemetry;
- [ ] queues/retries/storage are bounded;
- [ ] implementation choices do not preclude a later policy-controlled offline sink.

## 15. Explicit non-requirements

Conformance does not require:

- a Grafana stack;
- Mixpanel or Matomo;
- Clean Insights SDKs;
- a hosted collector;
- a central identity graph;
- session replay;
- one shared project event vocabulary;
- a Micrantha collector;
- a Micrantha telemetry database;
- a Micrantha analytics query engine.
