# CLI design, UX, and implementation guidance

This document extends the [CLI interoperability standard](cli-interoperability.md) with consistent human-facing presentation, discoverability, language-specific implementation choices, and cross-project adoption. It does not redefine the underlying domain semantics, Unix transport contract, authority model, or release gates.

**Authority map:** [CLI interoperability](cli-interoperability.md) owns stdin/stdout/stderr, format negotiation, machine contracts, exit semantics, safe non-interactive behavior, man-page minimums, and cross-transport equivalence. [Releases](releases.md) owns versioning, exact-artifact release evidence, packaging, SBOM/provenance/signatures, and rollback. [Source exposure and distribution](source-exposure-and-distribution.md) owns private/public implementation and distribution topology. [Security](security.md) owns secrets, execution authority, and supply-chain risk. [Documentation](documentation.md) owns general documentation lifecycle; [testing](testing.md) owns the evidence pyramid. This page specifies CLI-specific UX details and points to those authorities rather than copying them.

## Applicability and compatibility

- A **supported CLI** follows applicable MUST requirements in the CLI interoperability standard and documents intentionally unsupported features. An experimental command may defer optional presentation/extension features if it does not claim them as supported.
- Existing released commands must not silently change command names, default output format, flag meaning, field types, or exit meanings merely to adopt a convention here. Record an inventory, compatibility decision, migration notice, and regression tests first.
- Requirements below marked MUST are normative for **new supported command surfaces**; existing stable surfaces require a deliberate compatible migration. SHOULD indicates a recommended default with a documented project-level alternative.
- Keep the public CLI contract implementation-language-neutral. A common UX contract does not require an organization-specific shared runtime.

## Human-facing output

New human-oriented list/status commands SHOULD display a concise table when stdout is an interactive terminal. Table formatting is presentation, never a machine contract. Columns SHOULD have explicit headings, aligned widths, bounded display length, meaningful empty-state text, and clear units. Offer a detail command or an explicit wider presentation for information omitted by the table. Do not silently truncate identifiers, security-relevant data, or values when a reader could mistake a display abbreviation for the full value.

Respect terminal width, `NO_COLOR`, `TERM=dumb`, redirected stdout, and accessibility. Color and Unicode MAY enhance output but MUST NOT be the only means of conveying a state. Disable progress animation and ANSI escapes on non-TTY output unless explicitly requested.

**Do not introduce a new incompatible global output flag across existing CLIs.** The [interoperability standard](cli-interoperability.md#stdout) already recommends `--format text|json|jsonl`. New CLIs SHOULD use that convention; projects with an established `--output` option retain it and document equivalence or migration. Do not require a `--format auto` value or silently select JSON on redirected stdout for a CLI that already defaults to text. Automation MUST explicitly request a supported machine format and check the documented exit code. JSONL/NDJSON applies to independently consumable records, not arbitrary chunking of a single JSON document.

Primary results alone go to stdout in machine mode. Diagnostics, warnings, progress, and errors go to stderr even when machine mode is selected. A structured machine-error mode MAY be added by an explicit versioned contract but MUST NOT silently mix an error object into an expected successful result stream. Empty success, partial effect, cancellation, and failure MUST remain distinguishable.

## Command structure and interaction

Commands SHOULD use lowercase kebab-case names, short and discoverable noun/verb groupings, and bounded nesting. Simple tools MAY remain flat. Prefer consistent meanings for the applicable `--help`, `--version`, `--format`, `--quiet`, `--verbose`, `--no-color`, `--config`, and `--dry-run` options; do not add meaningless options to every subcommand. Keep published aliases and command spellings compatible.

Every supported command MUST offer discoverable help describing synopsis, flags, operands, stdin/output behavior, representative examples, and safety implications. A root `--version` SHOULD print the published executable version without requiring credentials or network access. An additional structured version subcommand MAY expose immutable source/build identity, CLI contract version, and available schema versions when useful.

Prompts require a TTY and an explicit interactive mode. `--yes` and `--non-interactive` MUST NOT bypass authorization, policy, identity checks, or target-bound approvals. A `--dry-run` MUST NOT commit the proposed mutation; document any reads, discovery, or other observable effects it can still perform. Display a specific target and effect before confirming irreversible operations.

Configuration precedence MUST be deterministic and documented; refer to [CLI interoperability](cli-interoperability.md#configuration-precedence). A `config explain` or `doctor` command MAY display effective *nonsecret* configuration provenance and bounded diagnostics. Diagnostic output MUST apply the [security standard](security.md).

Use stable project-owned error identifiers and documented exit meanings rather than imposing a new universal integer map on existing commands. Preserve signal and broken-pipe conventions. Subcommands that can partially mutate state must expose the actual completed/unknown/failed state and a safe reconciliation path; a process exit code is necessary but insufficient evidence of a completed effect.

## Machine contract and implementation

The canonical, versioned **domain** contract stays transport-neutral: do not create an unrelated CLI-only business model or require every project's results to fit a universal wrapper. A CLI may add versioned transport metadata, but it must not change domain state, validation, error vocabulary, evidence semantics, or authority. Document each stable JSON/JSONL record schema and its compatibility rules; consider published JSON Schema when consumers cross repository boundaries.

A breaking field-type change, field removal, reinterpreted status, or changed exit meaning requires a compatibility decision under [releases](releases.md). Additional optional fields are compatible only where consumers are required to tolerate unknown fields. Never serialize secrets or privileged internal implementation objects directly. Do not output a misleading empty result for an unavailable dependency.

A useful implementation boundary is: parser/dispatcher -> validated request and caller context -> application service and authorization -> typed domain result -> independent terminal and machine renderers. The CLI should not be the sole owner of domain logic. Reuse fixtures across CLI and service/orchestrator adapters to test semantic equivalence.

### Framework choices

Choose an actively maintained framework compatible with the project's language, build/runtime constraints, and packaging strategy; frameworks are implementation options, not organizational runtime dependencies:

| Language | Candidate framework | Relevant tradeoff |
| --- | --- | --- |
| Rust | clap; clap_complete; clap_mangen | Native executable and derived help/completions/man pages; review binary size and feature flags. |
| Go | Cobra with pflag | Good hierarchical command structure; avoid spreading global mutable state through handlers. |
| Python | Typer or Click | Ergonomic typed commands; account for interpreter/runtime packaging where standalone distribution is promised. |
| TypeScript | Commander.js or oclif | Small surface vs plugin-oriented architecture; review runtime dependencies and install script behaviour. |
| C# | System.CommandLine plus optional Spectre.Console | Keep parsing separate from rendering; validate AOT/trimming and supported platform packaging. |
| Shell | Small POSIX/shell wrapper only | Delegate nontrivial parsing, structured output, and security-sensitive domain logic to a tested implementation. |

Prefer project-owned small adapters for repeated output/help patterns. Extract an organization-wide library only after independent projects demonstrate stable reuse; do not force cross-language behaviour into a shared executable solely for consistency.

## Cross-project subcommands and extensions

Independent Micrantha tools remain independently runnable. A parent command MAY orchestrate another executable through an explicitly documented integration boundary; it must preserve the delegated program's cancellation, exit, identity, and output semantics. Do not parse another tool's human table or construct shell command strings from untrusted input. Use bounded argument arrays and document the forwarded-argument delimiter where supported.

Plugin discovery is **not** permission to execute. Any future extension manifest must declare command namespace, protocol/contract version, executable identity and provenance, input/output schemas, and required capabilities. The invoking host verifies compatibility and applies the owning authorization policy without inheriting ambient parent credentials. Registered extensions cannot silently shadow an existing command or elevate authority. Governed execution follows [security](security.md) and [tool-result trust](tool-result-trust.md).

## Help, man pages, completions, and examples

The existing [CLI interoperability man-page requirement](cli-interoperability.md#manual-pages) is a supported-release gate: ship an installed section-1 man page for the actual released executable; add section-5 configuration pages where appropriate. Generate help, references, man pages, and Bash/Zsh/Fish completions from command metadata when practical, or test authored documents against the actual CLI. Include at least one runnable pipeline and one failure/recovery example for material operations.

`--help`, `--version`, machine output, and `man <tool>` must be exercised through the supported **installed package**, not only a development checkout. Documentation and completion generation must not require production credentials.

## Binary packaging, provenance, and licensing

Packaging, source/posture constraints, source revision, release identity, checksums, signatures, SBOMs, provenance, immutable acquisition, clean consumer installation, and rollback belong to [releases](releases.md), [release readiness evidence](../architecture/release-readiness-evidence.md), and [source exposure](source-exposure-and-distribution.md). Avoid a second CLI-only release checklist with different gates.

A CLI package SHOULD contain its executable, version-matched man page, applicable completion files, installation/reference documentation, and required license/third-party notices. A distributable software artifact SHOULD have an SBOM in the format selected by its owning release pipeline and a documented integrity/provenance verification procedure. The standard does **not** impose a new mandatory CycloneDX-vs-SPDX choice or signing backend; the owning release standard and product threat model determine that profile.

Source and binary licensing decisions are project-owned. Publish the applicable license text, third-party attributions and redistribution notices, and clarify any distinct documentation/schema licenses. A public machine schema does not license private source, and private source is not a security boundary.

Symbol stripping, debug-symbol separation, and optional minification are packaging decisions; retain diagnostic and provenance capabilities commensurate with the product. Obfuscation is optional and MUST NOT be represented as credential protection, authorization, or tamper-proofing. Never embed secrets in shipped binaries. For private-canonical/public-binary projects, confirm that packaging and debug artifacts do not inadvertently disclose private implementation material; preserve the declared [source-exposure contract](source-exposure-and-distribution.md).

## Adoption and conformance

Before modifying an existing tool, capture its currently documented flags, output formats, man-page path, exit meanings, config precedence, install channels, published schemas, security boundary, and consumer scripts. Classify each proposed change as compatible presentation, additive optional interface, or breaking contract; preserve established consumers or plan a versioned migration.

The [interoperability conformance checks](cli-interoperability.md#conformance-checks) are the minimum black-box test basis. Project-owned tests SHOULD additionally exercise help and version without credentials; human table and narrow/no-colour terminal; strict stdout/stderr separation; valid JSON/JSONL and stable ordering where promised; an empty result; malformed inputs; denied and partial effects; clean non-interactive operation; safe broken-pipe handling; packed section-1 man page; and the exact installed candidate. Reuse the existing release-readiness checker and testing/Testule evidence where applicable rather than implementing a parallel release gate.

Start with one representative Rust/native CLI, one TypeScript or other managed-runtime CLI, and one effectful/infrastructure CLI. Record the actually observed differences and create repository-local adoption issues; do not claim portfolio-wide compliance from this documentation alone.
