# Figma Component Generator Skill

Generate Figma component sets from source code using the [figma-cli](https://github.com/silships/figma-cli) tool. Reads component logic (TSX/CSS/metadata) and produces properly structured Figma components with variants, variable bindings, and icon instances.

## Prerequisites

- [figma-cli](https://github.com/silships/figma-cli) cloned and installed locally
- Figma Desktop running with CDP enabled (port 9222)
- Claude Code CLI

## Quick Start

1. Place this skill folder at `~/.claude/skills/figma-component-generator/`
2. Customize the project-specific files (see below)
3. Use as: `/figma-component-generator <figma-page-url> <component-path>`

## Project Setup

This skill has **universal rules** that work for any design system and **project-specific references** that must be customized per project.

### Files to customize

#### `references/figma-typography.md`

Contains your project's font family, text style names, and weight mappings.

**To populate for your project**, run this in the figma-cli:
```bash
node src/index.js eval "(async () => {
  const styles = await figma.getLocalTextStylesAsync();
  return JSON.stringify(styles.map(s => ({
    name: s.name,
    fontSize: s.fontSize,
    fontName: s.fontName
  })));
})()"
```

Update the file with:
- Your font family (e.g., Inter, Outfit, Roboto)
- The CSS token to Figma text style name mapping
- Font weight to style name mapping for your specific font

#### `references/figma-icon-library.md` (optional)

Only needed if your Figma file has an icon component set (e.g., a Lucide Icon library with swappable variants). If you don't have one, delete this file -- the skill will fall back to creating icons via the figma-cli's built-in SVG rendering.

**To find your icon component set** (if you have one), run:
```bash
node src/index.js eval "(async () => {
  const sets = [];
  for (const page of figma.root.children) {
    for (const child of page.children) {
      if (child.type === 'COMPONENT_SET' && child.name.toLowerCase().includes('icon')) {
        sets.push({ name: child.name, id: child.id, variants: child.children.length });
      }
    }
  }
  return JSON.stringify(sets);
})()"
```

If found, update the file with:
- Your icon component set ID
- Variant naming format (e.g., `Icon Name=star, Size=20px`)
- Available sizes
- Semantic icon mappings for your project

#### `SKILL.md`

Update the CLI path in Step 1 to match your local figma-cli location:
```
CLI_PATH=<your-path-to-figma-cli>
```

### Files that work as-is (universal)

These contain Figma Plugin API patterns and rules that apply to any project:

| File | Purpose |
|---|---|
| `references/figma-plugin-api-patterns.md` | Core API: creating components, binding variables, positioning |
| `references/figma-map-lookup.md` | Optional JSON map for fast dependency resolution by ID |
| `references/rules/sizing-modes.md` | `resize()` ordering, axis direction table |
| `references/rules/icon-recoloring.md` | Recolor pattern for icons inside colored variants |
| `references/rules/nested-components.md` | Sub-component architecture for repeated stateful elements |
| `references/rules/slots.md` | Figma slots for dynamic item count (Pattern A vs B) |
| `references/rules/atomic-dependencies.md` | Classify Visual / Layout / Compositional and reuse existing component sets as instances |
| `references/rules/floating-overlays.md` | Recognize popovers, dropdowns, tooltips and split into trigger + floating component sets when needed |

## Source Code Conventions

The skill analyzes component source files to build a spec. It looks for:

1. **Component logic** — `.tsx`, `.jsx`, `.vue`, `.svelte`
2. **Styles** — `.module.css`, `.css`, `.scss`
3. **Metadata** — `.metadata.ts`, `.metadata.json` (optional, provides structured variant info)

Not every project will have all 3. The minimum is logic + styles. Metadata is a bonus that provides pre-structured variant definitions, making generation more accurate.

If your project uses a different structure (e.g., styled-components, Tailwind classes, Storybook stories as source), the Step 2 analysis in `SKILL.md` may need adjustment.

## Variable Naming Convention

The skill maps CSS custom properties to Figma variable names:

```
CSS:   var(--background-interactive-primary)
Figma: background/interactive/primary
```

Rule: Strip `var(--` and `)`, replace `-` with `/` for path segments.

If your Figma variables use a different naming convention, update the mapping logic in `SKILL.md` Step 4.

## Adding New Rules

As you discover new patterns, add rule files to `references/rules/`:

1. Create `references/rules/your-pattern.md` with:
   - **When to apply** — detection signal
   - **Why** — what breaks without it
   - **How** — step-by-step pattern with code examples
2. Add a row to the pattern detection checklist in `SKILL.md`

## Skill Structure

```
figma-component-generator/
  SKILL.md                              <- Workflow + decision checklist
  README.md                             <- This file
  references/
    figma-plugin-api-patterns.md        <- Core Figma API patterns (universal)
    figma-map-lookup.md                 <- Optional figma-map.json schema and bootstrap (universal)
    figma-icon-library.md               <- Icon component set config (project-specific)
    figma-typography.md                 <- Font + text style config (project-specific)
    rules/
      sizing-modes.md                   <- resize() ordering, axis directions (universal)
      icon-recoloring.md                <- Recolor icons per variant (universal)
      nested-components.md              <- Sub-components for stateful elements (universal)
      slots.md                          <- Dynamic item count with slots, Pattern A/B (universal)
      atomic-dependencies.md            <- Classify component + reuse existing atoms as instances (universal)
      floating-overlays.md              <- Trigger + overlay split for popovers/dropdowns/tooltips (universal)
```

## Optional: figma-map.json lookup table

For faster, more reliable dependency resolution in compositional components, you can provide an external JSON file that maps component names to their Figma node IDs. The file is read from `~/.claude/data/figma-map.json` (the path is configurable, and the skill works without it).

When present, the skill uses `figma.getNodeByIdAsync(id)` for direct lookups instead of traversing every page with `figma.root.findAll`. See `references/figma-map-lookup.md` for the schema and the bootstrap script that scans your Figma file and builds the map.
