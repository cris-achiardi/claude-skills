---
name: enara-figma-ds
version: 1.0.0
description: "Generate Enara design system Figma component sets from React/CSS source files using the figma-cli tool. This skill should be used when the user wants to create or update Enara DS components in Figma — reads agnostic Figma generation patterns from https://www.giorris.dev/figma/refs/ via WebFetch (with local fallback copies bundled in references/) and applies Enara-specific configuration from enara-config.md. Invoked as a slash command with a Figma page URL or component name."
---

# Enara Figma DS Component Generator

Generate Enara design system Figma component sets from source code (TSX, CSS Modules, metadata) using the `figma-cli` eval command. Reads agnostic Figma generation patterns from the public references library at `https://www.giorris.dev/figma/refs/` and applies Enara-specific values (Outfit font, Lucide Icon set, semantic token namespace, figma-map at `C:\Users\crmor\.claude\data\figma-map.json`) from the local `enara-config.md`.

## Reference resolution

This skill loads reference material from two sources:

- **`enara-config.md`** (local, always read first) — Enara identity: font, icon set IDs, text style naming, token namespace, figma-map path, variant conventions.
- **Public references library** at `https://www.giorris.dev/figma/refs/` — Agnostic patterns and rules, organized by topic. Map index: `https://www.giorris.dev/figma/refs/refs-map.md`.

### Fetch strategy for external references

When loading any agnostic ref, use **WebFetch with a verbatim-preserving prompt**:

> "Return the full content of this file verbatim. Preserve all code examples, ordering rules, and tables exactly. Do not summarize, do not paraphrase."

Battle-tested rules encode failure modes line-by-line — a summary loses the nuance.

**Fallback**: if WebFetch fails or returns obviously truncated content, fall back to `Read references/<file>` — the skill bundles local fallback copies of every public ref under `references/` for resilience. The local copies are byte-identical to the canonical URLs; behavior is the same.

### Reference URLs (canonical) and local fallbacks

| Ref | Canonical URL | Local fallback |
|---|---|---|
| Refs map | `https://www.giorris.dev/figma/refs/refs-map.md` | — (no local fallback needed) |
| Plugin API patterns | `https://www.giorris.dev/figma/refs/figma-plugin-api-patterns.md` | `references/figma-plugin-api-patterns.md` |
| Typography | `https://www.giorris.dev/figma/refs/figma-typography.md` | `references/figma-typography.md` |
| Icon library | `https://www.giorris.dev/figma/refs/figma-icon-library.md` | `references/figma-icon-library.md` |
| Map lookup | `https://www.giorris.dev/figma/refs/figma-map-lookup.md` | `references/figma-map-lookup.md` |
| Sizing modes | `https://www.giorris.dev/figma/refs/rules/sizing-modes.md` | `references/rules/sizing-modes.md` |
| Slots | `https://www.giorris.dev/figma/refs/rules/slots.md` | `references/rules/slots.md` |
| Nested components | `https://www.giorris.dev/figma/refs/rules/nested-components.md` | `references/rules/nested-components.md` |
| Floating overlays | `https://www.giorris.dev/figma/refs/rules/floating-overlays.md` | `references/rules/floating-overlays.md` |
| Atomic dependencies | `https://www.giorris.dev/figma/refs/rules/atomic-dependencies.md` | `references/rules/atomic-dependencies.md` |
| Icon recoloring | `https://www.giorris.dev/figma/refs/rules/icon-recoloring.md` | `references/rules/icon-recoloring.md` |

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
/enara-figma-ds <figma-page-url> [component-path]
```

- `figma-page-url`: URL of the Figma page where the component should be created (required)
- `component-path`: Path to the component folder under `libs/ui-react/src/components/...` (if not provided, ask the user)

## Workflow

### Step 0: Load Enara identity and figma-map (always, up-front)

Before any work:

1. **Read `enara-config.md`** (local, in this skill's directory). Capture: font family, weights to load, icon set keys, figma-map path, token namespace, variant conventions.
2. **Read the figma-map** at the path defined in `enara-config.md` (default: `C:\Users\crmor\.claude\data\figma-map.json`). Parse `sources`, `components`, `icons`.
3. **Validate file key**: parse the file key from the Figma URL provided by the user. Compare to `sources.foundations.key`. If they don't match, warn the user — the map's `componentSetId` values won't be valid in a different file (only `componentKey` values are cross-file). Use `importComponentSetByKeyAsync(componentKey)` for cross-file generation.

### Step 1: Resolve inputs

Parse the Figma page URL to extract the file key and page node-id. If `component-path` is not provided, ask the user — Enara components live under `libs/ui-react/src/components/{atoms|molecules|organisms|templates}/<Name>/`.

Locate the `figma-cli` repo. Check common locations:
- Look for a `figma-cli` directory in the current working directory or its parent
- Check `~/figma-cli` or `~/Projects/figma-cli`
- Or ask the user for the path if not found

Store the CLI path:
```
CLI_PATH=<path-to-figma-cli>
```

### Step 2: Analyze the component source

Read the component files:

1. **Component logic** (`.tsx`): Extract props, variants, types, default values
2. **Styles** (`.module.css`): Extract sizing, colors, spacing, border radius, token usage. Map CSS tokens to Enara's `foreground/...`, `background/...`, `border/...` namespace per `enara-config.md`.
3. **Metadata** (`.metadata.ts`): Extract structured variant definitions, sizes, colors, descriptions, `composition.nestedComponents`, `composition.commonPartners`

Build a **component spec**:
- Variant dimensions (e.g., `Variant=solid|soft|outline`, `Color=primary|danger|...`, `Size=sm|md|lg`)
- Sizing tokens (height, padding, font-size, gap)
- Color tokens mapped to Enara semantic variables
- Boolean features (dots, icons, close buttons) → boolean component properties
- Shape properties (border radius, stroke width, alignment)

Apply Enara's variant naming conventions from `enara-config.md` — `Variant`, `Color`, `Size`, `State`, `Role`, `Show <Element>`.

### Step 3: Classify component and resolve dependencies

**Fetch** `https://www.giorris.dev/figma/refs/rules/atomic-dependencies.md` (verbatim) and follow the classification + resolution workflow:

1. **Classify** as Visual, Layout Wrapper, or Compositional using CSS and metadata signals
2. **If Layout Wrapper**: present the clarity checkpoint to the user and wait — do NOT generate a component set unless they explicitly choose to
3. **If Visual or Compositional**: extract dependency names from metadata and source imports
4. **Resolve dependencies via the figma-map first**:
   - For each dependency, check `components.<name>.componentKey` and `components.<name>.componentSetId`
   - If generating into the source file (key matches `sources.foundations.key`), use `figma.getNodeByIdAsync(componentSetId)` for fast direct lookup
   - If generating into a different file, use `figma.importComponentSetByKeyAsync(componentKey)`
   - If the dependency isn't in the map or has `componentKey: null`, fall back to `figma.root.findAll(...)`
5. **Build a dependency map** with each found dependency's set ID + available variants. Warn the user about missing dependencies (per the agnostic rule).

For full schema, see `https://www.giorris.dev/figma/refs/figma-map-lookup.md` (fetch verbatim if details are needed).

### Step 4: Query Figma variables

Before generating, fetch all available Figma variables:

```bash
cd $CLI_PATH && node src/index.js eval "
(async () => {
  const allVars = await figma.variables.getLocalVariablesAsync();
  return JSON.stringify(allVars.map(v => v.name));
})()"
```

**Token-to-variable mapping** (per `enara-config.md` token namespace):
- `var(--foreground-interactive-primary)` → `foreground/interactive/primary`
- `var(--background-system-danger)` → `background/system/danger`
- Strip `var(--` and `)`, replace `-` with `/` for path segments

For each token used, check for a matching Figma variable. Track **unmapped tokens** for the final report.

For Plugin API binding details, fetch `https://www.giorris.dev/figma/refs/figma-plugin-api-patterns.md` (verbatim).

### Step 5: Navigate to the target page

Parse the `node-id` from the Figma URL (URL-encoded, e.g., `2001-2` means `2001:2`).

```bash
cd $CLI_PATH && node src/index.js eval "
(async () => {
  const targetId = '<decoded-node-id>';
  const page = figma.root.children.find(p => p.id === targetId);
  if (!page) {
    const page2 = figma.root.children.find(p => p.name.trim() === '> <ComponentName>');
    if (page2) { figma.currentPage = page2; return 'Navigated by name'; }
    return 'Page not found';
  }
  figma.currentPage = page;
  return 'Navigated to: ' + page.name;
})()"
```

### Step 6: Generate the component set

Build a single eval script that creates all variant combinations. The script must:

1. **Load fonts** — load every Outfit weight from `enara-config.md` (Regular, Medium, SemiBold, Bold at minimum)
2. **Fetch variables** and create a lookup helper
3. **Create component variants** by iterating over all dimension combinations:
   - For each combination (e.g., `solid + primary + md`), create `figma.createComponent()`
   - Name using `Variant=solid, Color=primary, Size=md` syntax
   - Set auto-layout, sizing, padding, gap, corner radius (consult sizing-modes ref)
   - Set placeholder fills/strokes, then bind to Figma variables
   - Create child elements (text labels, dots, icons) with proper bindings
   - For children that map to resolved dependencies (from Step 3), use `componentNode.createInstance()` instead of raw frames
   - Add boolean component properties for optional elements
4. **Combine variants** using `figma.combineAsVariants(components, figma.currentPage)`
5. **Arrange in a grid** for readability (remove auto-layout from set, position manually)
6. **Return a structured report** including the new `componentSetId` (and `componentKey` if available) for the figma-map update in Step 7

#### Pattern detection checklist

Before generating, scan the component source for these patterns and fetch the corresponding ref (verbatim) only if the pattern fires:

| Pattern | Detection Signal | Ref to fetch |
|---|---|---|
| **Sizing & layout** | Any component (always) | `https://www.giorris.dev/figma/refs/rules/sizing-modes.md` |
| **Plugin API basics** | Any component (always) | `https://www.giorris.dev/figma/refs/figma-plugin-api-patterns.md` |
| **Icons** | lucide-react imports, icon props, SVG elements, spinners | `https://www.giorris.dev/figma/refs/figma-icon-library.md` + `https://www.giorris.dev/figma/refs/rules/icon-recoloring.md` |
| **Typography** | Text nodes, font tokens, text-style CSS properties | `https://www.giorris.dev/figma/refs/figma-typography.md` |
| **Nested components** | `.map()` loops, repeated elements with per-item state (isActive, isSelected) | `https://www.giorris.dev/figma/refs/rules/nested-components.md` |
| **Dynamic item count** | Array prop with `.map()`; runtime-determined count; no fixed upper bound. Negative: named structural children, fixed count, single-child wrapper, render-props | `https://www.giorris.dev/figma/refs/rules/slots.md` |
| **Floating overlays** | `@floating-ui/*`, `@radix-ui/react-popover`, `@radix-ui/react-dropdown-menu`, `@radix-ui/react-tooltip`, `cmdk`, `@headlessui/react`; `createPortal`; `position: absolute\|fixed` overlays | `https://www.giorris.dev/figma/refs/rules/floating-overlays.md` |
| **Atomic dependencies** | Molecule/organism; metadata `nestedComponents` non-empty; imports DS components | `https://www.giorris.dev/figma/refs/rules/atomic-dependencies.md` |

**Cross-dependency**: `Nested components` and `Dynamic item count` often fire together. When a parent maps over items AND each item has per-item state, you need BOTH: create a sub-component set per `nested-components.md`, then use slot Pattern A (instance-filled) per `slots.md`. If items are heterogeneous or have no per-item state, only `slots.md` applies (Pattern B, frame-filled).

#### Key rules for the eval script

- Wrap everything in `(async () => { ... })()`
- Always set a placeholder fill/stroke BEFORE binding a variable
- Append children to parent BEFORE setting `layoutSizingHorizontal`
- Apply text style (`textStyleId`) BEFORE setting `.characters` (avoids Inter fallback)
- Return `JSON.stringify()` for structured results
- Use `figma.variables.setBoundVariableForPaint()` for variable binding
- For complex scripts, write to a temp `.js` file and use `eval --file <path>`, then clean up
- Icons must use Enara's Lucide Icon set per `enara-config.md` — `componentKey: 404f8e56e9d089b86f3104afe3554d0b3ef31356`
- All text must use Outfit via Figma text styles per `enara-config.md`

#### Grid layout strategy

Arrange variants in a grid where:
- **Columns** = sizes (`sm`, `md`, `lg`)
- **Rows** = colors (`neutral`, `primary`, ...)
- **Sections** (separated by gap) = visual variants (`solid`, `soft`, `outline`)

### Step 7: Update the figma-map and report

After successful generation:

1. **Update the figma-map** at the path from `enara-config.md`:
   - Add or update the entry under `components.<ComponentName>` with the new `componentSetId`
   - Preserve existing fields (`code`, `category`, `pageId`, `dependsOn`, `assetType`, `_parts` if present)
   - Set `componentKey` to `null` initially — it becomes available only after Figma publishes the component to the team library; the user can update it on the next bootstrap scan
   - Update `lastScanned` to today's date

2. **Present a generation summary** to the user:

```
## Component Generated: <Name>

- **Variants created**: <count> (<dimension breakdown>)
- **Properties**: Variant, Color, Size, Show Dot (boolean)
- **Variables bound**: <fill count> fill bindings, <stroke count> stroke bindings
- **Unmapped tokens**: (none) | <list of unmapped tokens>
- **Dependencies resolved**: <found>/<total> (<found list>; <missing list> not in file)
- **figma-map updated**: added componentSetId `<new-id>` under `components.<Name>`
- **Figma node ID**: `<componentSetId>`
```

If there are unmapped tokens, suggest the user create the missing variables in Figma or check for naming mismatches.

## Important Notes

- Never delete existing content on the page. Only add new nodes.
- The figma-cli daemon has a 60-second timeout. For very large component sets (100+ variants), split into multiple eval calls.
- If the connection is lost mid-generation, run `node src/index.js daemon restart` and retry.
- The eval script can be substantial. The daemon handles large payloads.
- **Always update the figma-map on success** — future invocations rely on it for fast dependency resolution. Skipping this step leaves the map stale and forces slow `findAll` lookups.
