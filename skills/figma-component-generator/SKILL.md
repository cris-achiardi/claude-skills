---
name: figma-component-generator
version: 1.0.0
description: "Generate Figma component sets from source code using the figma-cli tool. This skill should be used when the user wants to create or update Figma components by reading React/CSS source files and generating matching component sets with variants, properties, and variable bindings. Invoked as a slash command with a Figma page URL or component name."
---

# Figma Component Generator

Generate Figma component sets from source code (TSX, CSS Modules, metadata files) using the `figma-cli` eval command. Reads component logic, styles, and optional metadata to produce a properly structured Figma component set with variants, sizes, colors, and boolean properties -- all bound to Figma variables.

## Prerequisites

- The `figma-cli` repo must be cloned locally
- Figma Desktop must be running with CDP enabled (port 9222)
- The target Figma file must be open
- The daemon should be running (`node src/index.js daemon start`)

To verify the connection:
```bash
curl -s http://localhost:9222/json
```

## Usage

```
/figma-component-generator <figma-page-url> [component-path]
```

- `figma-page-url`: URL of the Figma page where the component should be created (required)
- `component-path`: Path to the component folder (if not provided, ask the user)

## Workflow

### Step 1: Resolve inputs

Parse the Figma page URL to extract the file and page context. If `component-path` is not provided, ask the user for it.

Locate the `figma-cli` repo. Check common locations:
- Look for a `figma-cli` directory in the current working directory or its parent
- Check `~/figma-cli` or `~/Projects/figma-cli`
- Or ask the user for the path if not found

Store the CLI path for use in all subsequent eval commands:
```
CLI_PATH=<path-to-figma-cli>
```

### Step 2: Analyze the component source

Read the component files. At minimum, look for:

1. **Component logic** (`.tsx`, `.jsx`, `.vue`, `.svelte`): Extract props, variants, types, default values
2. **Styles** (`.module.css`, `.css`, `.scss`): Extract sizing, colors, spacing, border radius, token usage
3. **Metadata** (`.metadata.ts`, `.metadata.json`): If available, extract structured variant definitions, sizes, colors, descriptions

From these files, build a **component spec**:

- **Variant dimensions**: Identify the props that create visual variants (e.g., `variant: solid|soft|outline`, `color: primary|danger|...`, `size: sm|md|lg`)
- **Sizing tokens**: Map size variants to pixel values (height, padding, font-size, gap)
- **Color tokens**: Map each variant+color combination to CSS custom properties (e.g., `var(--background-interactive-primary)`)
- **Boolean features**: Identify optional visual elements (dots, icons, close buttons) that should become boolean component properties
- **Shape properties**: Border radius, stroke width, stroke alignment

### Step 3: Query Figma variables

Before generating, fetch all available Figma variables to build a mapping:

```bash
cd $CLI_PATH && node src/index.js eval "
(async () => {
  const allVars = await figma.variables.getLocalVariablesAsync();
  return JSON.stringify(allVars.map(v => v.name));
})()"
```

**Token-to-variable mapping**: Convert CSS token names to Figma variable paths:
- `var(--background-interactive-primary)` maps to `background/interactive/primary`
- Strip `var(--` and `)`, replace `-` with `/` for path segments

For each token used by the component, check if a matching Figma variable exists. Track any **unmapped tokens** for the final report.

For detailed mapping rules and patterns, read `references/figma-plugin-api-patterns.md`.

### Step 4: Navigate to the target page

Parse the `node-id` from the Figma URL (URL-encoded, e.g., `2001-2` means `2001:2`).

```bash
cd $CLI_PATH && node src/index.js eval "
(async () => {
  const targetId = '<decoded-node-id>';
  const page = figma.root.children.find(p => p.id === targetId);
  if (!page) {
    // Fallback: find by name
    const page2 = figma.root.children.find(p => p.name.trim() === '> <ComponentName>');
    if (page2) { figma.currentPage = page2; return 'Navigated by name'; }
    return 'Page not found';
  }
  figma.currentPage = page;
  return 'Navigated to: ' + page.name;
})()"
```

### Step 5: Generate the component set

Build a single eval script that creates all variant combinations. The script must:

1. **Load fonts** (always load Outfit Regular/Medium/SemiBold as needed -- see `references/figma-typography.md`)
2. **Fetch variables** and create a lookup helper
3. **Create component variants** by iterating over all dimension combinations:
   - For each combination of variant properties (e.g., `solid + primary + md`), create a `figma.createComponent()`
   - Name it using Figma's variant syntax: `Variant=solid, Color=primary, Size=md`
   - Set auto-layout, sizing, padding, gap, corner radius
   - Set fills/strokes with placeholder colors, then bind to Figma variables
   - Create child elements (text labels, dots, icons) with proper variable bindings
   - Add boolean component properties for optional elements
4. **Combine all variants** using `figma.combineAsVariants(components, figma.currentPage)`
5. **Arrange in a grid** for readability (remove auto-layout from set, position manually)
6. **Return a report** with created count and any unmapped variables

For detailed Figma Plugin API patterns and code examples, read `references/figma-plugin-api-patterns.md`.

#### Pattern detection checklist

Before generating, scan the component source for these patterns and load the relevant rule:

| Pattern | Detection Signal | Rule File |
|---|---|---|
| **Sizing & layout** | Any component | `references/rules/sizing-modes.md` (always read) |
| **Icons** | lucide-react imports, icon props, SVG elements, spinners | `references/figma-icon-library.md` + `references/rules/icon-recoloring.md` |
| **Typography** | Text nodes, font tokens, text-style CSS properties | `references/figma-typography.md` |
| **Nested components** | `.map()` loops, repeated elements with per-item state (isActive, isSelected) | `references/rules/nested-components.md` |
| **Dynamic item count** | Lists, tabs, menus where N items varies | `references/rules/slots.md` |

#### Key rules for the eval script:

- Wrap everything in `(async () => { ... })()`
- Always set a placeholder fill/stroke BEFORE binding a variable
- Append children to parent BEFORE setting `layoutSizingHorizontal`
- Apply text style (`textStyleId`) BEFORE setting `.characters` (avoids Inter font loading issues)
- Return `JSON.stringify()` for structured results
- Use `figma.variables.setBoundVariableForPaint()` for variable binding
- For complex scripts, write to a temp `.js` file and use `eval --file <path>`, then clean up after
- All icons must be Lucide instances (including spinners as `loader-2`) -- read `references/figma-icon-library.md`
- All text must use Outfit font via Figma text styles -- read `references/figma-typography.md`

#### Grid layout strategy:

Arrange variants in a grid where:
- **Columns** = sizes (sm, md, lg)
- **Rows** = colors (neutral, primary, ...)
- **Sections** (separated by gap) = visual variants (solid, soft, outline)

### Step 6: Report results

After generation, present a summary:

```
## Component Generated: Badge

- **Variants created**: 63 (3 variants x 7 colors x 3 sizes)
- **Properties**: Variant, Color, Size, Show Dot (boolean)
- **Variables bound**: 42 fill bindings, 21 stroke bindings
- **Unmapped tokens**: (none)
  OR
- **Unmapped tokens**:
  - `var(--background-utility-coral)` -- no matching Figma variable found
  - `var(--foreground-utility-coral)` -- no matching Figma variable found
```

If there are unmapped tokens, suggest the user create the missing variables in Figma or check for naming mismatches.

## Important Notes

- Never delete existing content on the page. Only add new nodes.
- The figma-cli daemon has a 60-second timeout. For very large component sets (100+ variants), consider splitting into multiple eval calls.
- If the connection is lost mid-generation, run `node src/index.js daemon restart` and retry.
- The eval script can be substantial in size. The daemon handles large payloads.
