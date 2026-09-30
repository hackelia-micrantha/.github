# Observability standard

This standard defines Micrantha's organization-wide expectations for operational telemetry, domain events, product/usage measurement, diagnostics, and their relationship to security and governance evidence.

The goal is interoperable, privacy-conscious observability without creating a Micrantha-specific observability platform. Micrantha defines policy and bounded domain semantics; established standards and implementations provide telemetry plumbing, transport, collection, storage, and analysis wherever they fit.

## Principles

1. **Standards first.** Prefer OpenTelemetry, OTLP, W3C Trace Context, CloudEvents, and existing semantic conventions over Micrantha-specific protocols or attribute vocabularies.
2. **Thin customization.** A `micrantha.*` convention or shared adapter is justified only when an applicable upstream convention does not express the required meaning or when a cross-project policy boundary must be enforced consistently.
3. **Observation is not authority.** Telemetry, analytics, events, predictions, dashboards, and alerts describe behavior; they do not themselves authorize effects or become canonical domain state.
4. **Optional observability must remain optional.** A project must be able to operate correctly with optional telemetry disabled, without a remote collector, and with a no-op/local-only sink unless observability is itself part of the declared product contract.
5. **Required governance evidence is separate.** Disabling optional telemetry must not silently suppress evidence required to authorize, verify, or audit a governed operation.
6. **Collect to answer questions.** Usage/product measurement starts from a declared question or decision need and collects the minimum data, detail, frequency, and retention required to answer it.
7. **Preserve composability.** Instrumentation must not corrupt CLI stdout/stderr contracts, machine-readable output, deterministic behavior, or stable transport/domain semantics.
8. **Bound cost and blast radius.** Cardinality, payload size, queues, retries, retention, local storage, and exporter failure must be bounded.
9. **Local-first capable.** Local diagnosis and analysis should remain useful without a hosted service; the architecture must remain compatible with future intentional offline/store-and-forward operation.
10. **Backend neutral.** No organization-wide standard requires Grafana, Prometheus, Loki, Tempo, Mixpanel, Matomo, or another particular storage/analysis vendor.

## Normative standards baseline

Operational telemetry SHOULD use OpenTelemetry APIs/data model and OTLP where supported.

Implementations SHOULD:

- use upstream OpenTelemetry semantic conventions when they have the exact intended meaning;
- use W3C Trace Context for cross-boundary trace propagation where tracing is supported;
- preserve upstream stability/version considerations for semantic conventions that are not yet stable;
- keep instrumentation APIs separate from SDK/exporter ownership so libraries do not force a backend onto applications;
- honor applicable native OpenTelemetry configuration rather than replacing it with an incompatible Micrantha-only configuration model.

Durable or externally interoperable domain events SHOULD use CloudEvents 1.0-compatible envelopes where the event model benefits from a standard event envelope. A project must not create a durable event merely because a trace or log event exists.

Project-specific event profiles, such as Dubnium event contracts, layer on this standard and remain owned by the relevant domain.

## Signal taxonomy

Projects MUST distinguish the following concepts when they are present:

| Plane | Purpose | Canonical authority |
| --- | --- | --- |
| Operational telemetry | Explain runtime behavior and performance through traces, metrics, logs, and bounded events | Observational only |
| Domain events | Represent meaningful domain occurrences that may cross process/system boundaries | Domain contract decides |
| Product/usage measurement | Answer declared questions about product or feature use | Analytical only |
| Security/audit evidence | Establish attributable facts required by a security/governance contract | Domain/governance contract |
| Diagnostics | Support bounded local/operator troubleshooting | Observational only |
| Alerts/notifications | Draw attention to derived conditions | Never authority by themselves |

A metric is not a domain event. A trace is not canonical state. Product analytics is not audit evidence. An alert is not approval.

## Resource and release identity

Signals SHOULD be attributable to the concrete software/runtime identity necessary to interpret them, using upstream semantic conventions where available.

Relevant identity can include:

- service/component/project identity;
- release/version/build identity;
- source revision;
- schema/profile revision;
- deployment/environment class;
- runtime/platform/model revision where material.

Identity fields must be bounded and typed. Raw paths, arbitrary URLs, prompts, user-generated strings, and other unbounded values MUST NOT be promoted into metric dimensions merely because they are available.

## Operation and diagnostic vocabulary

Projects SHOULD expose stable machine-readable operation/result/error semantics separately from human-readable diagnostic prose.

Where upstream semantics are insufficient, the common profile defines a small extension vocabulary for:

- bounded operation result;
- stable project-owned diagnostic code;
- optional project/domain operation name.

Human-readable messages may change without breaking analytical contracts.

## Privacy, classification, and minimization

Instrumentation MUST use explicit field selection rather than arbitrary serialization of process state, request objects, environment maps, logs, or exception structures.

Generic telemetry MUST exclude by default:

- secrets, tokens, credentials, private keys, and approval material;
- unrestricted environment values;
- raw prompts, completions, memories, or model scratch context;
- raw capability or authorization request bodies;
- arbitrary stdin/stdout/stderr bodies;
- raw images, frames, embeddings, or media;
- exact location/history unless a product contract explicitly requires it;
- private filesystem contents or paths beyond a documented bounded diagnostic contract;
- user-generated content unless an explicit measurement contract permits it.

Collection of user/product behavior SHOULD follow privacy-preserving measurement principles:

- **data minimization** — collect only what is necessary for a declared question;
- **source aggregation** — aggregate near the source when raw event detail is not required;
- **detail generalization** — reduce temporal, geographic, identity, or categorical precision where sufficient;
- **engaged transparency** — user-facing products clearly disclose applicable collection/export behavior and provide appropriate consent/control.

These principles are informed by Clean Insights; they do not require a Clean Insights runtime or backend.

## Product and usage measurement

Product analytics is a distinct vocabulary and policy surface from operational telemetry.

A material measurement SHOULD be backed by a small `MeasurementPlan` or equivalent declaration containing:

- the question being answered;
- the decision or learning goal it supports;
- the minimum events/properties required;
- identity requirements, if any;
- aggregation/generalization policy;
- retention;
- export/consent policy.

Funnels, flows, cohorts, retention, segmentation, and similar event-oriented analysis concepts are encouraged when they answer the declared question. These concepts do not imply a requirement to build or operate a custom analytics engine.

Session replay, advertising attribution, fingerprinting, and unrestricted clickstream capture are not organization defaults and require an explicit product/privacy decision.

## Enablement, disablement, and export

Projects MUST distinguish, where applicable:

1. **instrumentation** — whether observations are produced;
2. **collection** — whether observations are retained/processed locally;
3. **export** — whether observations leave the local process/device/system.

These are separate controls.

OpenTelemetry-based implementations SHOULD honor `OTEL_SDK_DISABLED` and applicable per-signal exporter configuration supported by the language/runtime. A project-facing convenience option such as `--telemetry=off` MAY map to native OTel configuration but must not create contradictory semantics.

Remote export MUST NOT be required by the common contract.

User-facing remote product/usage telemetry MUST be policy-controlled and must follow the product's disclosure/consent requirements.

Disabling optional observability MUST NOT:

- change the source operation's domain result;
- bypass authentication, authorization, approval, or verification;
- suppress evidence that a governing policy explicitly requires before an effect may proceed.

When required evidence cannot be produced, the governing domain decides whether the operation is denied, indeterminate, or otherwise safely handled. This is not treated as an optional telemetry failure.

## Failure and backpressure semantics

Optional telemetry failure is observational degradation.

Collector/exporter/backend/network failure MUST NOT change the success/failure result of an otherwise independent source operation.

Instrumentation MUST bound:

- synchronous export latency;
- retries;
- in-memory queues;
- persistent queues;
- payload size;
- CPU/memory/storage use.

When a bound is reached, implementations MAY drop, sample, coalesce, or locally summarize optional telemetry according to documented policy rather than blocking domain work indefinitely.

Dropped or degraded telemetry SHOULD itself be observable through bounded counters/diagnostics where practical.

## Cardinality

Metric dimensions MUST be intentionally bounded.

Values such as the following generally belong in spans/events/logs rather than metric labels:

- user/account identifiers;
- request IDs and trace IDs;
- source revisions;
- arbitrary branch names;
- filenames/paths;
- URLs;
- prompts or generated text;
- exception messages;
- arbitrary diagnostic strings.

A project SHOULD document any intentionally high-cardinality analytical field and why it cannot be represented more safely or cheaply.

## CLI interoperability

The [CLI interoperability standard](cli-interoperability.md) remains authoritative for stdin/stdout/stderr, machine formats, exit statuses, and cross-transport semantics.

CLI observability MUST preserve those contracts:

- stdout remains primary command output only;
- stderr remains the documented diagnostic surface;
- telemetry export is out-of-band;
- tracing/logging MUST NOT corrupt JSON/JSONL or pipeline behavior;
- arguments, stdin, stdout, stderr, environment values, paths, and user content MUST NOT be captured by default;
- telemetry disablement MUST be available without changing command semantics;
- trace context MAY be propagated across explicit process/orchestration boundaries, but propagated context and baggage remain untrusted metadata and never confer authority.

Short-lived CLIs SHOULD use bounded flush/export behavior and must not hang indefinitely waiting for telemetry delivery.

## Local diagnostics

Projects SHOULD support bounded local diagnosis appropriate to their maturity and deployment model without requiring a remote backend.

A diagnostic bundle MAY include:

- release/runtime identity;
- recent stable diagnostic codes;
- bounded aggregate timings/counters;
- dependency health summaries;
- explicit collection/export configuration state.

Diagnostic bundles MUST apply the same classification, allowlist, redaction, size, and retention rules as telemetry. A support bundle is not permission to dump process memory, arbitrary logs, environment variables, or private files.

## Offline and store-and-forward compatibility

Version 1 does not require a custom offline telemetry database.

For transient exporter/backend outages, implementations SHOULD first consider standard OpenTelemetry Collector retry/sending-queue mechanisms and persistent queue storage where appropriate.

The architecture MUST nevertheless avoid assumptions that prevent later intentional offline operation. A future durable local sync store should be able to provide, as applicable:

- bounded quota and retention;
- classification/redaction before persistence;
- encryption at rest where sensitivity requires it;
- origin and schema/profile identity;
- observed/stored/synchronized timestamps as separate concepts;
- idempotent synchronization and deduplication;
- expiry/deletion semantics;
- policy/consent checks before export;
- local aggregation/generalization before synchronization.

Where practical, standard OTLP representations SHOULD remain the synchronization format for operational telemetry. A custom wire protocol or database format requires a separate documented need.

## Security and governance boundary

Observability systems are part of the threat model.

Apply the [security standard](security.md) to telemetry collection, transport, local persistence, remote backends, dashboards, and support bundles.

In particular:

- trace/correlation identifiers are not credentials;
- receiving or replaying telemetry/events grants no capability;
- externally influenced telemetry values remain untrusted input;
- dashboards and derived predictions are evidence for investigation, not authorization;
- telemetry stores must not become shadow secret/content stores;
- access, retention, deletion, and integrity controls must match data classification;
- governed evidence may reference telemetry, but promotion into authoritative evidence is owned by the governing domain.

## Adoption profiles

Apply the smallest useful profile for the project.

### Library

Usually:

- propagate or accept context where appropriate;
- expose instrumentation hooks/APIs without requiring an SDK/backend;
- remain correct with no-op instrumentation.

### CLI

Usually:

- one bounded operation/execution span where useful;
- stable diagnostic/result codes;
- composability and no-content-capture rules;
- optional/local/no-op configuration.

### Service or daemon

Usually:

- traces for material request/work boundaries;
- RED or equivalent bounded service metrics;
- structured diagnostics/logs where useful;
- dependency/resource saturation telemetry;
- health/readiness and exporter degradation visibility.

### User-facing application

Usually adds:

- explicit privacy/export controls;
- minimal product `MeasurementPlan`s;
- local aggregation/generalization when feasible;
- lifecycle/offline behavior;
- no requirement for a hosted collector.

### Agentic or governed system

Usually adds:

- traceability for proposal/tool/execution/verification boundaries;
- bounded model/tool resource measurements;
- explicit separation of observation, recommendation, authority, and evidence;
- no raw prompt/context capture by default.

### CI/CD system

Usually adds:

- workflow/job/runner timing and outcome;
- queue/admission/resource saturation;
- exact revision/release identity;
- distinction between provider result claims and accepted verification evidence.

## Conformance and review

A repository adopting this standard SHOULD be able to answer:

- Which signal planes are present?
- Which upstream standards/semantic conventions are used?
- Which fields are custom and why?
- What is collected, retained locally, and exported remotely?
- How is optional telemetry disabled?
- What happens when collectors/backends fail?
- What cardinality/size/retention bounds apply?
- What sensitive/content fields are excluded?
- Does CLI instrumentation preserve machine composition?
- Which measurements have declared questions/retention/consent policy?
- Is required security/governance evidence separated from optional telemetry?
- Is future offline/store-and-forward operation blocked by any current assumption?

Repositories do not need identical infrastructure or identical event vocabularies.

## Non-goals

This standard does not:

- create a Micrantha telemetry protocol;
- require one hosted telemetry vendor;
- require one dashboard product;
- replace project/domain state with events;
- replace Anthesis or other governance evidence with observability;
- require product analytics for every project;
- require remote export;
- standardize every project event name centrally;
- require a custom offline telemetry database in v1.
