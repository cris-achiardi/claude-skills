# Enara Figma DS Component Generator

Generate Enara design system Figma component sets from source code using the [figma-cli](https://github.com/silships/figma-cli) tool. This skill is the Enara-specific companion to [`figma-component-generator`](../figma-component-generator/) — it reads agnostic Figma patterns from a public references library and applies Enara identity (Outfit font, Lucide Icon set, semantic token namespace, figma-map at a known path) from a local config.

## Prerequisites

- [figma-cli](https://github.com/silships/figma-cli) cloned and installed locally
- Figma Desktop running with CDP enabled (port 9222)
- Claude Code CLI
- The Enara `00_Foundations` Figma file open (or a target file that consumes Enara's library)
- An Enara design system codebase clone (e.g., `enara-health/enara-design-system`)

## Quick Start

```
/enara-figma-ds <figma-page-url> [component-path]
```

The skill reads `enara-config.md` (Enara identity), reads the figma-map at `C:\Users\crmor\.claude\data\figma-map.json` (dependency lookup), and fetches agnostic generation rules from `https://www.giorris.dev/figma/refs/` as needed.

## Architecture

This skill separates **identity** from **patterns**:

- **Identity** (in `enara-config.md`) — Outfit font weights, Lucide Icon set keys, text style naming convention, semantic token namespace (`foreground/...`, `background/...`), figma-map path, variant property conventions (`Variant`/`Color`/`Size`/`State`/`Role`).
- **Patterns** (fetched from `https://www.giorris.dev/figma/refs/`) — Plugin API patterns, sizing modes, slots, nested components, floating overlays, atomic dependencies, icon recoloring. Battle-tested rules forged from 40+ Enara component generations, externalized so other Figma skills can share them.

### Why externalize the patterns?

So multiple Figma skills (this one, future skills for variables, screens, etc.) can point at the same canonical knowledge instead of bundling drift-prone copies. The patterns evolve via the public refs library; the skill stays lean.

### Local fallback

If `https://www.giorris.dev/figma/refs/` is unreachable, the skill falls back to local copies of every ref under `references/` — byte-identical to the canonical URLs, kept in sync via the `claude-skills` repo's update flow.

## Skill Structure

```
enara-figma-ds/
  SKILL.md                              <- Workflow + fetch strategy
  README.md                             <- This file
  enara-config.md                       <- Enara identity (font, icons, tokens, map path)
  references/                           <- Local fallbacks for the public refs library
    figma-plugin-api-patterns.md
    figma-typography.md
    figma-icon-library.md
    figma-map-lookup.md
    rules/
      sizing-modes.md
      icon-recoloring.md
      nested-components.md
      slots.md
      atomic-dependencies.md
      floating-overlays.md
```

## Relationship to `figma-component-generator`

| | `figma-component-generator` | `enara-figma-ds` |
|---|---|---|
| Scope | Any design system | Enara DS only |
| References | Bundled locally in `references/` | Fetched from `https://www.giorris.dev/figma/refs/`, local fallbacks for resilience |
| Identity | Templated placeholders the user fills in | Concrete values in `enara-config.md` |
| Figma map update | Optional | Required — reads on start, writes on finish |
| When to use | Other design systems, forks | Enara work specifically |

If you're building generation skills for a different design system, fork `figma-component-generator` (templated) rather than this one.

## Public references library

The agnostic patterns this skill fetches:

- Index: <https://www.giorris.dev/figma/refs/refs-map.md>
- Core docs: `figma-plugin-api-patterns`, `figma-typography`, `figma-icon-library`, `figma-map-lookup`
- Composition rules: `atomic-dependencies`, `nested-components`, `slots`, `floating-overlays`, `icon-recoloring`, `sizing-modes`

These are the same docs that live in `references/` as fallbacks.

## Updating

- **Enara identity changes** (new icon set, token rename, etc.) → edit `enara-config.md`
- **Pattern changes** (new rule, fix to existing) → update the public ref at the giorris.dev source, then sync the local fallback in `references/`
- **Workflow changes** → edit `SKILL.md`
