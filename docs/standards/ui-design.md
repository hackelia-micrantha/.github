# Community UI design directive

Phyllotaxis is the shared design-system and UI substrate for Micrantha projects.

For public and community-facing user interfaces, the **default** visual direction is intentionally minimal and utilitarian, using late-1990s web interfaces and Craigslist as reference points for restraint, information density, and obvious interaction affordances.

This default is the **Utility** profile. Its governing rule is:

> **1990s in visual character, not in capability.**

Utility UI should look plain, direct, lightweight, and content-first while retaining modern semantics, accessibility, responsiveness, security, and interaction quality.

## Utility default

Prefer:

- system and browser-native typography;
- obvious text links and familiar browser affordances;
- restrained colour use with strong link and state distinction;
- compact, readable information density;
- simple borders and separators where structure needs reinforcement;
- natural document flow and intrinsic layout;
- small amounts of reusable spacing rather than large decorative whitespace;
- controls whose purpose is visible without ornamental styling;
- interfaces that remain understandable when CSS is reduced or partially unavailable.

Avoid by default:

- decorative gradients;
- glass, blur, glow, and elevation effects;
- rounded-card layouts as a general composition pattern;
- oversized hero sections;
- ornamental animation or motion;
- bespoke typography when system fonts are sufficient;
- hidden navigation or icon-only controls when obvious text works;
- visual complexity introduced only to make an interface appear contemporary.

These are defaults, not absolute prohibitions. A deviation should correspond to a concrete semantic, usability, accessibility, editorial, or product requirement.

## Editorial profile

Phyllotaxis also permits a bounded **Editorial** profile for genuine long-form, journal, article, narrative, or media surfaces.

Editorial may use a richer visual vocabulary when it materially improves reading or media comprehension, including:

- distinct display/body/monospace typography roles;
- more deliberate long-form reading rhythm;
- stronger article hierarchy;
- first-class featured and inline imagery;
- richer article metadata and taxonomy presentation;
- selective surfaces, borders, and radii;
- additional whitespace where it improves editorial pacing.

Editorial is **not** a generic “make this more modern” mode. Select it because the primary content/task is editorial or media-oriented, not because ordinary software UI needs more decoration.

Utility remains the default for project, tool, documentation, support, status, administrative, and other direct software/community surfaces.

A community project may use Editorial for a genuine journal/media section without changing its overall Utility default.

## Modern capability remains required

Neither visual profile reproduces historical browser limitations or inaccessible 1990s markup. Community interfaces should still use or support, as applicable:

- semantic HTML;
- keyboard navigation and visible focus states;
- WCAG-appropriate contrast and interaction targets;
- responsive and container-aware layout;
- reduced-motion preferences;
- internationalization and text scaling;
- modern form semantics and validation;
- progressive enhancement.

A richer profile never lowers these requirements.

## Review heuristic

For ordinary community UI, choose Utility unless a real editorial/media task justifies Editorial.

For Utility, when two designs satisfy the same product and accessibility requirements, prefer the one with:

1. fewer visual concepts;
2. fewer custom values;
3. fewer wrappers;
4. fewer effects;
5. more obvious browser-native semantics;
6. higher information density without harming readability.

For Editorial, prefer the smallest additional typography, imagery, hierarchy, and spacing vocabulary that materially improves reading or narrative comprehension.

A Utility surface should feel closer to a well-maintained document, utility, or classified listing than to a contemporary marketing site. An Editorial surface may be more expressive, but should remain semantic and restrained rather than decorative by default.

## Scope

This directive applies by default to UI introduced or materially redesigned in `hackelia-micrantha` community repositories. Repository-specific requirements may justify a documented exception, but should not silently replace the shared visual direction.

Visual profile names are semantic. Community APIs or design contracts should not encode specific sites, personal brands, or Craigslist itself as theme names.
