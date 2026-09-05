# Community UI design directive

Phyllotaxis is the shared design-system and UI substrate for Micrantha projects.

For public and community-facing user interfaces, the default visual direction is intentionally minimal and utilitarian, using late-1990s web interfaces and Craigslist as reference points for restraint, information density, and obvious interaction affordances.

The governing rule is:

> **1990s in visual character, not in capability.**

Community UI should look plain, direct, lightweight, and content-first while retaining modern semantics, accessibility, responsiveness, security, and interaction quality.

## Prefer

- system and browser-native typography;
- obvious text links and familiar browser affordances;
- restrained colour use with strong link and state distinction;
- compact, readable information density;
- simple borders and separators where structure needs reinforcement;
- natural document flow and intrinsic layout;
- small amounts of reusable spacing rather than large decorative whitespace;
- controls whose purpose is visible without ornamental styling;
- interfaces that remain understandable when CSS is reduced or partially unavailable.

## Avoid by default

- decorative gradients;
- glass, blur, glow, and elevation effects;
- rounded-card layouts as a general composition pattern;
- oversized hero sections;
- ornamental animation or motion;
- bespoke typography when system fonts are sufficient;
- hidden navigation or icon-only controls when obvious text works;
- visual complexity introduced only to make an interface appear contemporary.

These are defaults, not absolute prohibitions. A deviation should correspond to a concrete semantic, usability, accessibility, or product requirement.

## Modern capability remains required

The visual direction does not reproduce historical browser limitations or inaccessible 1990s markup. Community interfaces should still use or support, as applicable:

- semantic HTML;
- keyboard navigation and visible focus states;
- WCAG-appropriate contrast and interaction targets;
- responsive and container-aware layout;
- reduced-motion preferences;
- internationalization and text scaling;
- modern form semantics and validation;
- progressive enhancement.

## Review heuristic

When two designs satisfy the same product and accessibility requirements, prefer the one with:

1. fewer visual concepts;
2. fewer custom values;
3. fewer wrappers;
4. fewer effects;
5. more obvious browser-native semantics;
6. higher information density without harming readability.

A community surface should feel closer to a well-maintained document, utility, or classified listing than to a contemporary marketing site.

## Scope

This directive applies by default to UI introduced or materially redesigned in `hackelia-micrantha` community repositories. Repository-specific requirements may justify a documented exception, but should not silently replace the shared visual direction.
