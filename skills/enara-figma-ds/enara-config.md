# Enara Design System — Skill Configuration

Enara-locked values consumed by `enara-figma-ds` SKILL.md. Loaded once at the start of every invocation. Do NOT externalize these — they only apply when generating into Enara's Figma file.

## Typography

- **Font family**: `Outfit` (Google Fonts, sans-serif fallback)
- **Weights available**: 100 (Thin), 200 (ExtraLight), 300 (Light), 400 (Regular), 500 (Medium), 600 (SemiBold), 700 (Bold), 800 (ExtraBold), 900 (Black)
- **Weights commonly used in components**: Regular (400), Medium (500), SemiBold (600), Bold (700) — always load these at the top of every eval script

### Text style naming convention

CSS token path → Figma style name follows TitleCase with `/` separators:

```
text.{category}.{size}.{weight}  →  {Category}/{Size}/{Weight}
```

Categories observed in `libs/tokens/tokens/text-styles.json`: `display`, `heading`, `title`, `body`, `caption`. Sizes: `xl`, `lg`, `md`, `sm`, `xs` (varies per category). Weights: `regular`, `semibold`, `bold`.

Example mappings:

| CSS token | Figma style |
|---|---|
| `text.display.xl.regular` | `Display/Xl/Regular` |
| `text.heading.lg.semibold` | `Heading/Lg/Semibold` |
| `text.body.md.regular` | `Body/Md/Regular` |
| `text.caption.sm.medium` | `Caption/Sm/Medium` |

Always verify against actual `figma.getLocalTextStylesAsync()` output — text style names may have drifted from the token source.

## Icon library

- **Name in Figma**: `Lucide Icon`
- **Source file**: `00_Foundations`
- **componentKey** (publish-time stable, use across files): `404f8e56e9d089b86f3104afe3554d0b3ef31356`
- **componentSetId** (only valid in source file `00_Foundations`): `2292:1737`
- **pageId** (in source file): `2107:5763`
- **Variant count**: ~4,104 (Lucide full set, multiple sizes)
- **Variant naming**: `Icon Name=<lucide-name>, Size=<size>` — exact size enum varies, run discovery in target file before generation

Import pattern for cross-file generation (use `componentKey`, not `componentSetId`):

```javascript
const iconSet = await figma.importComponentSetByKeyAsync('404f8e56e9d089b86f3104afe3554d0b3ef31356');
const variant = iconSet.children.find(c => c.name === 'Icon Name=search, Size=20px');
const instance = variant.createInstance();
```

## Figma map lookup table

- **Path**: `C:\Users\crmor\.claude\data\figma-map.json`
- **Schema version**: `2.0` (see `_schema` field in the file)
- **Already populated** with all current Enara components (atoms, molecules, organisms, templates) and their componentSetIds + componentKeys

Read at the start of every invocation. Update at the end after any new component is generated — add or update the entry for the generated component with its new `componentSetId` and (if published) `componentKey`.

### Map schema essentials

- `sources.<sourceName>.key` — Figma file key for that source file
- `sources.<sourceName>.libraryKey` — Library key for cross-file imports
- `components.<Name>` — entry per code component, with `pageId`, `componentSetId`, `componentKey`, `dependsOn`, `assetType`
- `icons.<Name>` — same shape for icon sets

When generating into the source file (`36EGuGS3ziQPIWELiphSDO` / `00_Foundations`), `componentSetId` is usable directly. When generating into a different file (a product app file, for example), use `importComponentSetByKeyAsync(componentKey)` instead.

For full schema and resolution algorithm, see the agnostic ref: https://www.giorris.dev/figma/refs/figma-map-lookup.md

## Source files

| Source name | Figma file key | Figma name | Purpose |
|---|---|---|---|
| `foundations` | `36EGuGS3ziQPIWELiphSDO` | `00_Foundations` | Master design system file — variables, styles, all DS component sets live here |

The `libraryKey` for foundations is in the figma-map's `sources.foundations.libraryKey`.

## Token namespace (semantic colors)

Enara's semantic color tokens follow this hierarchy (in `libs/tokens/tokens/semantic-colors.json`):

```
foreground/
  base
  interactive/{primary, white}
  subtle
  muted
  disabled
  inverted
  system/{success, warning, danger, info}
  brand/{logo}
  utility/{moonstone, wisteria, green, ...}

background/
  (analogous hierarchy)

border/
  (analogous hierarchy)
```

CSS → Figma variable name conversion (same as agnostic pattern):

```
var(--foreground-interactive-primary)   →  foreground/interactive/primary
var(--background-system-danger)          →  background/system/danger
var(--border-default)                    →  border/default
```

## Code path convention

Components live in the `@enara-health/ui-react` workspace at:

```
libs/ui-react/src/components/{atoms|molecules|organisms|templates}/<ComponentName>/
```

Each component directory contains:
- `<ComponentName>.tsx` — React source with props/variants
- `<ComponentName>.module.css` — CSS Module with sizing, colors, spacing
- `<ComponentName>.metadata.ts` — AI-ready metadata
- `index.ts` — barrel export

When the user provides a component name (not a path), resolve to `libs/ui-react/src/components/**/<Name>/` and detect category from the path.

## Variant property conventions

Enara component sets use these property names (TitleCase) across the library:

- `Variant` — visual style (`solid`, `soft`, `outline`, `ghost`)
- `Color` — semantic color (`neutral`, `primary`, `success`, `warning`, `danger`, `info`)
- `Size` — sizing token (`sm`, `md`, `lg`)
- `State` — interaction state (`default`, `hover`, `pressed`, `disabled`, `focused`)
- `Role` — for buttons (`primary`, `secondary`, `ghost`, `danger`)
- `Show <Element>` — boolean for optional elements (`Show Dot`, `Show Icon`, `Show Close`)

Lowercase values, hyphenated when multi-word (`chevron-down`, not `ChevronDown`).

Verify against existing Enara component sets in the figma-map when picking variants for instance creation — values are stable across the library.

## Commit conventions (when shipping new components)

When this skill produces commits (in a separate workflow), follow Enara's git rules:

- Format: `<type>(<scope>): <description>`
- Scope for component changes: `ui-react`
- Scope for token changes: `tokens`
- Scope for repo-wide changes: `repo`

Example: `feat(ui-react): add AlertDialog component`

## Skill behavior summary

When invoked, the skill should:

1. Read this file (`enara-config.md`) for Enara identity
2. Read the figma-map at the path above
3. Fetch agnostic refs from `https://www.giorris.dev/figma/refs/` (verbatim) as the workflow demands them
4. Execute the 7-step workflow from SKILL.md
5. Update the figma-map with any newly-generated component IDs before reporting back
