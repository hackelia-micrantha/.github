# Micrantha Telemetry and Observability Architecture

Status: draft

Tracks: #60

Related:

- `ryjen/dubnium#766` — Dubnium events/observability/telemetry program
- `ryjen/dubnium#772` — Dubnium OpenTelemetry/Grafana integration
- `hackelia-micrantha/dubnium-community#54` — public CloudEvents Event Contract v1
- `ryjen/eyespie#304` — first mobile/backendless implementation
- `hackelia-micrantha/bluebell#5` — later KMP extraction

## Purpose

Define the small, reusable observability contract shared across Micrantha projects while preserving project ownership, local-first operation, privacy boundaries, and independent deployment choices.

The goal is interoperability and consistent semantics, not one telemetry backend.

## Core separation

Keep these planes distinct:

```text
canonical domain state / operation
        |
        +--> domain event
        |      CloudEvents 1.0 when durable/interoperable event evidence is useful
        |
        +--> operational telemetry
        |      OpenTelemetry traces / metrics / bounded diagnostic signals
        |
        +--> security / audit evidence
        |      domain-owned governed evidence where stronger semantics are required
        |
        +--> product analytics
        |      separate typed product vocabulary / consent / retention policy
        |
        +--> user-exportable diagnostics
               bounded local support artifact
```

These concerns may correlate but they are not interchangeable:

- a trace is not canonical state;
- an event is not automatically an alert;
- product analytics is not operational telemetry;
- audit evidence is not a general-purpose metrics/log stream;
- diagnostics do not grant authority.

## Adopted standards

Micrantha reuses established standards rather than defining parallel protocols.

- **CloudEvents 1.0** is the preferred outer envelope for interoperable domain events.
- **OpenTelemetry** is the canonical telemetry/correlation model.
- **W3C Trace Context** is the preferred cross-boundary correlation mechanism.
- Prefer upstream **OpenTelemetry Semantic Conventions** where an exact semantic match exists.
- Project adapters should be thin wrappers around established SDKs and own only project-specific naming, privacy, bounded values, and application seams.

Projects may expose no-op/local-only telemetry while still conforming to the common model.

## Authority and source-of-truth invariants

Observability is observational.

```text
configuration intent        -> project/configuration owner
runtime/domain state        -> owning project/service/store
security authorization      -> policy/capability owner
telemetry                   -> observation/correlation only
event projection            -> evidence/query projection only
alerts/notifications        -> derived/operator presentation only
```

Common rules:

1. Telemetry never silently becomes authorization or canonical domain state.
2. Correlation IDs never confer authority.
3. Collector/exporter failure must not change a successful source operation unless a domain explicitly documents stronger delivery semantics.
4. Backpressure is bounded; observability may drop/coalesce according to explicit policy rather than stall core work indefinitely.
5. Local diagnosis should remain useful without a remote collector or service.

## Common resource and release identity

Operational signals should be attributable to concrete software/runtime identity where available.

Candidate common fields:

```text
project
component / service
release version
build number / build identity
source revision
telemetry schema/profile revision
platform/runtime identity
model/runtime revision where materially relevant
```

Not every project needs every field.

Identity fields must be bounded and intentionally exposed. Do not use:

- private filesystem paths;
- arbitrary URLs;
- unrestricted environment values;
- advertising/device-fingerprint identifiers;
- arbitrary user-generated identifiers;
- high-cardinality opaque IDs as metric labels.

## Diagnostic vocabulary

Prefer stable machine-readable values over prose.

Conceptual shape:

```text
operation
stage?
result = success | cancelled | degraded | failed
code = project-owned stable diagnostic code
measurement = bounded duration/count/size where useful
trace/correlation context?
release/runtime identity
occurredAt
```

Human messages may evolve independently. Portable/queryable diagnostics should not rely on exception strings.

Material semantic changes to a diagnostic code require a new code/version rather than silently redefining historical meaning.

## Trace / event / metric guidance

Use this default mapping:

```text
operation/run          -> trace
nested operation       -> span
lifecycle/domain fact  -> CloudEvent and/or span event
aggregate quantity     -> metric
bounded failure detail -> diagnostic record / structured log-like signal
```

Do not create CloudEvents for every UI action or method call.

Do not turn ephemeral object identifiers into metric dimensions.

## Privacy profile

Telemetry contracts should make sensitive data difficult to represent by default.

### Excluded from generic operational telemetry by default

- secrets, tokens, credentials, signing material;
- unrestricted environment values;
- arbitrary log or exception bodies;
- raw prompts/completions;
- raw memory content;
- raw capability request bodies;
- raw images/frames/files;
- embeddings;
- exact location/address/history;
- private filesystem paths;
- arbitrary user-generated text/content;
- advertising IDs and device fingerprints.

A project may deliberately define a separate governed contract for a field class when a real requirement exists. That exception must define purpose, visibility, retention, and access.

### Preferred data classes

Projects should document at least:

- public/non-sensitive operational metadata;
- pseudonymous/correlation metadata;
- private operational metadata;
- user content;
- secrets/credentials;
- security-sensitive evidence.

Remote export policy may be stricter than local retention policy.

## Boundedness and cardinality

Every telemetry implementation should document bounds for:

- event/record payload size;
- local queue/ring-buffer record count and/or byte budget;
- retention age;
- exporter retry/backoff;
- attribute value size;
- metric label cardinality.

Avoid labels/attributes such as:

- filenames;
- bundle/game/run IDs unless a bounded diagnostic context explicitly requires them;
- arbitrary URLs;
- full exception messages;
- user-entered text;
- raw model/prompt content;
- unbounded repository/workflow metadata.

## Local diagnostics

Local diagnostics are a first-class part of the common strategy.

A project should be able to answer:

> What version/runtime was running, what operation failed, at which stage, and what should be inspected next?

without requiring remote collection.

A common diagnostic export profile should contain only bounded support-safe data, such as:

```text
diagnostic schema/profile revision
release/source identity
platform/runtime/model identity where relevant
recent stable operation/result/code records
aggregate timing/count summaries
telemetry degradation/drop counters
```

Project-specific export UX and persistence are not standardized here.

## Remote telemetry

Remote collection is optional and policy-controlled.

The common contract does not require a hosted Micrantha backend.

When a project enables remote ingestion:

- ingestion credentials/authority remain outside untrusted clients where possible;
- clients are treated as untrusted producers;
- schemas/field allowlists are validated server-side;
- rate/byte limits apply;
- replay/idempotency policy is explicit where relevant;
- retention/access is defined per signal class;
- collection failure remains observational degradation unless explicitly documented otherwise.

## Product analytics boundary

Product analytics is intentionally separate.

A product may reuse common release/correlation values, but should use its own typed vocabulary, purpose, consent/disclosure, aggregation, and retention rules.

Avoid a universal application API such as:

```text
record(name, Map<String, Any>)
```

when a closed typed event hierarchy can enforce privacy and semantics structurally.

For Eyespie, `ryjen/eyespie#117` owns the product-analytics track separately from `#304` operational telemetry.

## Security and audit evidence boundary

Some events require stronger evidence semantics than ordinary telemetry.

Examples:

- authorization decisions;
- approval state;
- capability dispatch;
- signed provenance;
- high-value security transitions.

Those records remain owned by the relevant domain/governance system. Telemetry may reference or correlate with them, but a trace/span/log must not replace exact authorization/evidence state.

## Project profiles

### Dubnium

Dubnium is the current reference implementation for the architecture semantics.

Reusable decisions:

- CloudEvents for domain events;
- OpenTelemetry for telemetry/correlation;
- W3C trace propagation;
- bounded allowlisted fields;
- local-first diagnosis;
- observational failure semantics;
- event/telemetry never becomes authority.

Dubnium-specific deployment remains project-owned:

- systemd/journald and `dubctl`;
- PostgreSQL event projection and LISTEN/NOTIFY;
- Grafana Alloy/Beyla/Tempo/Loki/Prometheus/Alertmanager/Grafana;
- Mako/ntfy notification routing.

Do not require those components for other Micrantha projects merely because Dubnium uses them.

### Eyespie

Eyespie is the first mobile/backendless consumer.

Release telemetry should cover production operation boundaries such as:

```text
startup
camera/capture
MediaPipe initialization
embedding generation
match evaluation
SQLDelight persistence
.eyespie import/export validation
share/open handoff
lifecycle/cancellation
```

Eyespie diagnostics must exclude raw images, embeddings, clues/answers, bundle bytes, private paths/keys/tokens, exact location, recipients, and arbitrary exception/environment content.

Core gameplay remains local-authoritative and functional with telemetry disabled and offline.

### Bluebell

Bluebell is the later reusable KMP extraction target, not the place to invent the first API.

After Eyespie proves the seam, candidates for extraction include:

- release/runtime identity values;
- trace/correlation facade;
- stable diagnostic result types;
- NoOp/Fake sinks;
- bounded local sink abstractions;
- diagnostic export envelope;
- privacy-safe bounded value helpers;
- optional OTel adapter boundary.

Project vocabularies remain with their projects.

## Public contract relationship

`hackelia-micrantha/dubnium-community#54` remains the existing public CloudEvents contract work.

Do not destabilize that work solely to rename it Micrantha-wide.

Prefer a layered approach:

```text
Micrantha common semantics
   |
   +--> Dubnium public event profile
   +--> Eyespie operational diagnostics profile
   +--> future project profiles
```

If later experience shows the public event profile is truly generic, extract/rename only the stable common portion with compatibility preserved.

## Adoption checklist

A project adopting this strategy should answer:

- What domain state remains authoritative?
- Which operations deserve traces?
- Which facts deserve durable/interoperable events?
- What stable diagnostic codes are needed?
- Which metrics are actually actionable?
- Which fields are prohibited?
- What cardinality/payload/retention bounds apply?
- Does local diagnosis work without a collector?
- What happens when telemetry storage/export fails?
- Is remote export enabled, and under what consent/policy?
- Are product analytics and audit evidence kept separate?

## Non-goals

- one mandatory hosted telemetry provider;
- one mandatory collector/storage stack;
- centralizing every project's domain event catalog;
- event-sourcing all domains;
- session replay;
- advertising attribution/fingerprinting;
- unrestricted log shipping;
- making observability a prerequisite for application correctness.
