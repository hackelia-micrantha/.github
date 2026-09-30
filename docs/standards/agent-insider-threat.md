# AI Agent Insider-Threat and Cumulative Exposure Standard

This standard defines how Micrantha projects should reason about AI-assisted and autonomous agents that can accumulate sensitive organizational context over time.

It complements the general [security engineering standard](security.md). It does not assume that ordinary agent access is malicious, and it does not create a second authorization engine.

## Core threat model

A capable agent can resemble a long-lived insider because it may be intentionally given:

- broad repository access;
- issue, document, email, chat, and file context;
- durable memory;
- credentials and connectors;
- execution tools;
- network access;
- cross-project visibility.

The important security failure may emerge from **composition** rather than one obviously prohibited call.

Conceptually:

```text
read confidential source A      -> individually allowed
read infrastructure detail B    -> individually allowed
read customer/project data C    -> individually allowed
persist summary                 -> individually allowed
send external message           -> independently allowed

combined history
  -> prohibited disclosure
```

Per-call authorization alone is insufficient when policy depends on what the run, principal, workspace, or durable context has already observed.

## Security objective

Treat an AI/agent runtime as a powerful **untrusted principal operating inside the trust perimeter**.

Reasoning access must not imply:

- unrestricted cross-domain aggregation;
- durable access to every credential it can use indirectly;
- unrestricted persistence;
- unrestricted egress;
- authority to declassify information;
- authority to erase its own attribution;
- authority to decide that accumulated exposure no longer matters.

The system should preserve enough externally maintained state to determine whether a proposed consequential action remains compatible with prior material exposure.

## Exposure state is not transcript state

Where policy depends on accumulated information exposure, represent that state using bounded structured facts.

Candidate facts include:

- sensitivity/classification classes observed;
- project, tenant, workspace, or customer scopes crossed;
- credential/security/topology metadata exposure;
- regulated/personal/customer data exposure;
- source trust/taint classes;
- whether plaintext was materialized;
- whether protected data was persisted to Memory, cache, artifact, or workspace;
- approved purpose;
- allowed destination classes;
- time/expiry or exposure budget where policy uses one.

Do not make raw model transcripts, summaries, or model narration authoritative exposure state.

A model may say:

> I did not retain anything sensitive.

That statement is evidence at most. It does not clear exposure state.

## Composition-aware authorization

A consequential action should be evaluated against both:

1. the action's ordinary authority; and
2. the policy-relevant accumulated exposure/composition state.

Examples include:

- confidential read followed by external message;
- private-source read followed by public repository publication;
- tenant-A data access followed by tenant-B write;
- regulated-data retrieval followed by an external model-provider call;
- secret-bearing task context followed by durable Memory promotion;
- privileged repository inspection followed by artifact export.

Where a rule depends on prior exposure, the authorization decision must bind the exact current exposure/composition-state identity so a decision made against an earlier state cannot be replayed after additional protected reads.

## Scope and reset semantics

Exposure state must follow the actual trust/persistence boundary.

A new:

- chat;
- model invocation;
- process;
- agent persona;
- worker;
- retry;

does not necessarily reset exposure risk.

Do not reset merely because the conversational session changed when any of the following survive:

- durable Memory;
- persistent workspace artifacts;
- cached summaries;
- reusable credentials;
- tool state;
- exported intermediate files;
- persistent delegated authority;
- retained outputs containing protected data.

Conversely, do not retain exposure state forever by default. Scope and expiry should follow the relevant policy boundary, purpose, and persistence model.

## Purpose limitation

Sensitive access should be purpose-bound where practical.

A capability to retrieve protected information should identify enough context to constrain its use, for example:

```text
principal
purpose
resource/scope
sensitivity ceiling
lifetime
allowed downstream destination classes
```

Purpose metadata is not sufficient by itself. Runtime and effect boundaries must still enforce the relevant controls.

## Egress

External egress is a high-value composition boundary.

Applicable egress includes:

- outbound HTTP/network calls;
- email/chat/message sends;
- public or cross-trust repository writes;
- uploads or artifact publication;
- external model-provider calls;
- clipboard/desktop bridging;
- cross-tenant writes;
- durable exports.

Prefer explicit destination classes and fail closed when required current exposure state is unavailable or indeterminate.

Do not grant a lower-trust model or agent unrestricted network access merely because each individual destination has a legitimate use.

## Credentials and indirect authority

Agents should normally receive the narrow ability to perform a requested operation, not reusable underlying credentials.

Prefer:

```text
agent
  -> typed bounded request
  -> gateway / provider
  -> short-lived scoped authority
  -> exact effect
```

over:

```text
agent
  -> reusable GitHub / cloud / KMS / messaging token
```

A secret that never appears in the model context can still be dangerously broad if the agent can drive a generic credentialed proxy. The semantic effect and destination must remain bounded.

## Memory and persistence

Durable Memory increases insider-threat blast radius because exposure can survive the originating task.

Memory systems should preserve:

- classification;
- provenance;
- scope;
- purpose where material;
- retention;
- retrieval authorization;
- deletion/forgetting state.

Sensitive operational context should not silently become durable knowledge.

Promotion should not erase sensitivity labels merely because the data was summarized or embedded.

Derived indexes, summaries, caches, and embeddings remain part of the exposure lifecycle when they can reproduce protected information.

## Repository and supply-chain content

Repository content is untrusted input to an agent.

Potentially hostile content includes:

- README/instruction files;
- issues and pull-request text;
- source comments;
- generated code;
- build scripts;
- dependencies;
- test fixtures;
- tool configuration;
- retrieved remote documentation.

Such content may influence reasoning but cannot itself:

- become trusted policy;
- grant credentials;
- widen filesystem/network access;
- change protected destinations;
- satisfy approval;
- override higher-priority trusted instructions.

External repositories or generated code entering higher-trust workflows may warrant quarantine, inspection, isolated execution, or explicit provenance checks.

This standard does not require a universal Git man-in-the-middle proxy.

## Observation and detection

Useful signals may include:

- unexpectedly broad source fan-in;
- many unrelated sensitive reads within one purpose scope;
- access to credential/topology metadata without task need;
- cross-project or cross-tenant traversal;
- sensitive reads followed by new external destination attempts;
- unusual archive/export/publication behavior;
- repeated Memory promotion of sensitive context;
- repeated denied egress attempts;
- unusual destination or provider changes;
- anomalous persistent-context growth.

These are **signals**, not proof of malicious intent.

An anomaly detector may trigger:

- increased verification;
- narrower capabilities;
- quarantine;
- human review;
- temporary egress suspension;
- investigation.

It must not silently become the sole authorization authority unless a separately reviewed policy explicitly defines that deterministic effect.

## Attribution and provenance

Do not scrub agent identity merely to minimize retained data.

Preserve bounded, privacy-aware attribution sufficient to answer:

- which principal/runtime/model role accessed a protected class;
- under which purpose/capability;
- which trusted/untrusted source class was involved;
- what persistence occurred;
- what consequential action or destination was attempted;
- which policy decision governed it;
- what effect was actually verified.

Minimize:

- plaintext;
- secrets;
- unnecessary prompts/transcripts;
- raw personal data.

Preserve:

- opaque identities;
- hashes/references;
- classifications;
- policy/effect lineage;
- non-secret audit evidence.

## AI classification boundary

AI may assist with:

- sensitivity classification;
- source/destination categorization;
- explaining suspicious access patterns;
- correlating distributed evidence;
- recommending narrower scopes.

Where security can depend on mechanically known facts, prefer deterministic labels and enforcement.

Model classification alone should not authorize declassification, cross-tenant movement, or protected external release.

When semantic classification is unavoidable, record its uncertainty and apply a policy-appropriate fail-closed or review path.

## Containment and recovery

A suspected compromised agent should be containable without broad system shutdown where practical.

Controls may include:

- revoke short-lived capabilities;
- suspend egress;
- invalidate delegated credentials;
- quarantine workspace/run state;
- stop Memory promotion;
- preserve bounded forensic evidence;
- rotate exposed credentials according to actual exposure;
- reconcile potentially in-flight effects;
- re-establish a clean context/runtime.

Do not treat "new session" as containment if the compromised persistence/authority remains.

## Defensive scenarios

Projects implementing agentic systems should cover applicable scenarios such as:

1. confidential read + external send is denied by composition policy;
2. private repository read + public commit is denied unless explicitly reviewed;
3. tenant-A read + tenant-B write cannot cross scope;
4. durable Memory promotion preserves source sensitivity and scope;
5. agent restart does not reset exposure state while persistent workspace/Memory survives;
6. explicit clean run boundary resets only the exposure state policy says is scoped to that run;
7. false model claim that sensitive data was not read cannot clear authoritative state;
8. prompt-injected repository content cannot widen credentials or destinations;
9. lower-trust worker cannot access raw reusable credentials;
10. anomaly signal causes review/quarantine but does not fabricate evidence of malicious intent;
11. denied consequential action produces no external effect;
12. stale authorization bound to exposure state S1 cannot commit after state advances to S2.

## Relationship to project ownership

### Anthesis

Owns:

- composition-aware policy;
- exact current state binding;
- approval;
- evidence sufficiency;
- containment policy;
- governance interpretation.

### Dubnium

Owns:

- runtime observation;
- execution-authority enforcement;
- data/tool/network isolation;
- durable run state;
- Memory integration;
- bounded credential/provider adapters;
- egress enforcement;
- runtime evidence.

### Capability and Operator/Supervisor Gateways

Own bounded request/transport/effect mediation within their assigned contracts.

They do not become policy authorities merely because they enforce or transport a decision.

### Memory

Memory is persistent context, not authority. Memory sensitivity/provenance/lifecycle must survive transformations that remain retrievable.

## Non-goals

This standard does not:

- assume all AI agents are malicious;
- infer human or model intent from access patterns;
- require complete transcript surveillance;
- build a general enterprise DLP product;
- introduce a second policy engine;
- require a general temporal-logic language;
- make anomaly detection authoritative by default;
- require a universal Git proxy;
- erase agent attribution in the name of privacy.
