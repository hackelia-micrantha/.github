# CLI interoperability standard

Micrantha command-line tools are expected to behave as composable Unix programs and to expose the same canonical domain semantics used by orchestrators, services, CI integrations, and other adapters.

This standard applies to repositories that ship a CLI or expose stable machine-consumable operations through both a CLI and another transport.

## Principles

1. **Do one bounded job well.** Prefer narrow commands and explicit composition over large hidden workflows.
2. **stdin, stdout, and stderr are APIs.** stdout carries primary data; diagnostics, progress, warnings, and usage belong on stderr.
3. **Human output is not the machine contract.** Stable machine modes must exist for supported automation and composition.
4. **Pipes transport data, not authority.** Piped input never implies approval, authenticated identity, capability grant, or permission to mutate.
5. **One semantic contract, many transports.** CLI, Supervisor/orchestrator, RPC/service, CI, and library adapters reuse the same canonical versioned domain semantics.
6. **Packaged documentation is part of the interface.** Every shipped CLI includes a section-1 man page through its supported install and release paths.

## Unix process contract

### stdin

Commands that logically consume a document, record stream, or path list SHOULD support stdin. Prefer `-` as the conventional stdin operand where it is unambiguous and safe.

Input handling MUST:

- treat piped data as untrusted;
- enforce applicable size, record-count, parser, recursion, and resource bounds;
- avoid reading secrets from command-line arguments merely for convenience;
- avoid implicit prompting when stdin or stdout is not a TTY;
- distinguish data input from approval, authentication, and authorization.

### stdout

stdout MUST contain only the command's primary result in machine mode. Diagnostics, progress, warnings, prompts, usage, and debug logging MUST NOT corrupt a machine-readable stdout stream.

Commands with structured output SHOULD converge on:

```text
--format text|json|jsonl
```

`jsonl`/NDJSON is preferred when records can naturally be processed independently or streamed.

Structured output SHOULD preserve stable ordering where determinism is expected and SHOULD carry a schema or contract version where compatibility matters.

### stderr

stderr is for diagnostics, progress, warnings, human-facing usage, and debug information.

stderr MUST NOT disclose credentials, tokens, private keys, sensitive prompt bodies, approval material, or private filesystem contents beyond the command's documented diagnostic contract.

### exit status

Commands MUST document stable exit-status semantics for supported command families. Distinguish successful execution from invalid input, policy denial, unavailable dependency, stale state, verification failure, and internal failure where those distinctions are meaningful to callers.

### broken pipes and signals

A downstream consumer exiting normally, for example:

```sh
tool --format jsonl | head -n1
```

MUST NOT be reported as an application failure solely because stdout was closed. CLIs SHOULD handle SIGPIPE/broken-pipe behavior according to normal Unix expectations.

### TTY and color

- do not emit ANSI/color when stdout is not a TTY unless explicitly requested;
- support `NO_COLOR` where color is otherwise used;
- effectful commands MUST NOT block on an implicit prompt in non-interactive execution;
- non-interactive mutation MUST require an explicit, documented authority mode.

## Path and record interoperability

For path-producing or path-consuming commands:

- newline-delimited paths are acceptable only when the domain guarantees they are safe;
- support NUL-delimited input/output (`-0`, `--null`, or an established equivalent) where arbitrary filesystem paths are in scope;
- interoperation with `find`, `xargs`, `jq`, `sort`, `grep`, `sed`, `awk`, and shell redirection SHOULD be natural.

## Configuration precedence

Where configuration exists, document precedence explicitly. Prefer:

```text
CLI > environment > repository/user config > defaults
```

A repository MAY use a different model when required by the domain, but the behavior must be deterministic and documented.

## Canonical semantic contracts across transports

A Micrantha tool MUST define one canonical, versioned domain contract for each stable operation and reuse that contract across CLI composition, Supervisor/orchestrator integration, RPC/service adapters, CI integrations, and library APIs where applicable.

A transport MAY add transport-specific metadata or behavior such as:

- stdin/stdout framing;
- exit status;
- request or correlation IDs;
- deadlines and cancellation;
- trace context;
- authenticated session/principal context;
- wire envelopes or protocol headers.

A transport MUST NOT silently fork, reinterpret, weaken, or extend the underlying domain semantics.

Normative requirements:

- canonical schemas/types and version identifiers are transport-neutral where practical;
- validation, canonicalization, ordering, result/error vocabulary, provenance/evidence meaning, and security/authority semantics are shared;
- CLI JSON/JSONL SHOULD be a direct serialization or projection of the canonical contract rather than a CLI-only semantic model;
- orchestrator/service adapters SHOULD call the same core implementation or validated contract boundary used by the CLI rather than duplicate business rules;
- transport-only metadata MUST remain distinguishable from domain data;
- authenticated identity, trusted host policy, approvals, credentials, and capability grants MUST NOT become trusted merely because values crossed an internal process or API boundary;
- golden/conformance fixtures SHOULD be reusable across CLI and orchestrator/RPC tests;
- when the same deterministic input and authoritative host context are supplied, supported transports SHOULD produce semantically equivalent canonical results.

Duplicated or divergent CLI-versus-orchestrator domain models are architectural drift unless an explicit versioned compatibility decision documents why the semantics differ.

### Examples

- Modolia CLI and Supervisor integration consume the same `RouteRequest`, `RouteConstraints`, and `RouteDecision` semantics.
- Invokrum CLI and orchestrated use consume the same composition, lock, and attestation contracts.
- Anthesis CLI and Capability/Supervisor integrations consume the same capability-invocation and decision semantics. Authenticated identity and approval remain host-bound facts.
- Keylix verification semantics remain consistent between CLI conformance tooling and a long-lived verifier host. Process lifetime may add replay/nonce guarantees, but those guarantees must be explicit rather than changing the meaning of a verification result.

## Authority and effect safety

Unix composability MUST NOT weaken a component's authority boundary.

In particular:

- arbitrary piped data MUST NOT be interpreted as approval;
- a schema-valid request does not prove authenticated caller identity;
- model, repository, filesystem, verifier, or tool output remains evidence/data unless the owning domain explicitly promotes it through an authoritative mechanism;
- destructive or consequential operations require explicit authority independent of stdin framing;
- replayed evidence or prior success does not mint new authority;
- a transport adapter cannot widen the capability admitted by the canonical domain contract.

## Manual pages

Every shipped CLI MUST provide a section-1 man page installed with the supported package or release artifact.

The man page, together with `--help`, SHOULD document as applicable:

- synopsis and command structure;
- stdin/stdout/stderr behavior;
- input and output formats;
- machine contract/schema versions;
- exit statuses;
- environment variables and configuration precedence;
- non-interactive and mutation behavior;
- security and authority boundaries;
- examples, including at least one meaningful pipeline.

Significant subcommands MAY have separate section-1 pages when that improves discoverability.

Nix packages, release archives, and other supported installation channels MUST package the same documented CLI contract exercised by CI.

## Conformance checks

Repositories SHOULD reuse a small black-box conformance suite or equivalent tests covering applicable behavior:

```sh
tool ... | jq ...
producer | tool ...
tool ... | head -n1
```

Verify:

- machine stdout contains no diagnostics;
- stderr contains no secret-bearing payloads;
- non-TTY execution cannot block on an implicit prompt;
- broken-pipe behavior is clean;
- documented exit statuses are exercised;
- NUL-safe path handling works where required;
- `man <tool>` succeeds from the supported package/install path;
- canonical fixtures exercised through CLI and orchestrator/RPC adapters produce semantically equivalent results where determinism applies.

## Release readiness

For a repository that ships a CLI, the applicable requirements in this standard are release-readiness gates, not optional polish.

A supported CLI release is not ready when a material promised interface lacks required machine semantics, non-interactive safety, packaged manual documentation, or cross-transport semantic conformance.

Experimental repositories may explicitly document unavailable pre-release surfaces, but must not present an incomplete interface as supported or stable.

## Scope and exceptions

Not every command needs every format or streaming mode. Apply features when they match the command's domain.

Repository-local exceptions may be stricter or may document a justified alternative. Exceptions must identify the affected compatibility/security/support claim and must not silently weaken authority boundaries or stable-contract guarantees.
