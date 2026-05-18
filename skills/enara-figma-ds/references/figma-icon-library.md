# Figma Icon Library Reference

How to discover, instance, and use an existing icon component set in a Figma file when generating components. Icon set IDs, variant naming, and the semantic-name → icon-name mapping are project-specific — consuming skills should encode those in their own config. The patterns below are agnostic.

## When this applies

A component being generated needs to render an icon (search input, alert, button, badge). The design system already publishes its icons as a Figma component set (e.g., Lucide-mirrored, Phosphor-mirrored, or a custom set).

If the design system has no icon set, the generation falls back to the figma-cli's built-in SVG rendering — but the result is detached from the library and won't update when icon definitions change. Prefer instancing from a real set when one exists.

## Discovering the Icon Set

Find icon-like component sets in the current Figma file:
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

Record the resulting component set ID and store it in the consuming skill's config.

## Typical icon-set variant shape

Icon sets generally expose two variant properties:

| Property | Type | Examples |
|----------|------|----------|
| Icon Name | VARIANT | `search`, `x`, `check`, `chevron-down`, `loader-2` |
| Size | VARIANT | `16px`, `20px`, `24px` (or `sm`, `md`, `lg`) |

Variant naming follows the standard `Property=value` convention:

```
Icon Name=search, Size=20px
```

The exact icon names and size values are project-specific — confirm them with the discovery script before generating.

## Creating an Icon Instance

```javascript
const iconSet = await figma.getNodeByIdAsync('<icon-set-id>');
const variant = iconSet.children.find(
  c => c.name === 'Icon Name=star, Size=20px'
);
if (variant) {
  const instance = variant.createInstance();
  parentFrame.appendChild(instance);
}
```

Always use `getNodeByIdAsync` with the cached set ID rather than searching by name on every generation — it's faster and more reliable, especially when the icon set lives on a different page.

## Semantic Icon Mappings

Components often reference icons by their semantic role rather than their library name (a Button's loading state needs *a* spinner, not specifically `loader-2`). Build a mapping table that translates roles to library names:

| Semantic role | Common icon name | Where it appears |
|---|---|---|
| close | `x` | Close buttons, dismissible toasts/alerts |
| search | `search` | Search inputs |
| loading | `loader-2` | Spinners on async buttons |
| chevron-down | `chevron-down` | Dropdowns, select triggers |
| chevron-up | `chevron-up` | Disclosure expanders |
| check | `check` | Checkboxes, selected menu items |
| error | `alert-circle` | Error states on form fields and alerts |
| success | `check-circle-2` | Success toasts and inline confirmations |
| warning | `alert-triangle` | Warning alerts |
| info | `info` | Info tooltips and alerts |

The table above is a starting set — the consuming skill's config should extend it with project-specific mappings.

## Size Selection Guide

Pick an icon size based on the parent component's footprint:

| Context | Recommended icon size |
|---------|----------------------|
| Inside small components (Badge, Chip, Tag) | Smallest available (e.g., 12px or 14px) |
| Default components (Alert, Button, Input) | Medium (e.g., 16px or 20px) |
| Large or standalone icons (Empty states, Hero) | Largest available (e.g., 24px or 32px) |

When generating, infer the size from CSS context (icon-size token, parent font-size) and pick the closest available variant.

## After instancing: recoloring

Icon instances inherit the library's default fills/strokes (typically `foreground-base`). When placed inside a colored variant (e.g., a solid-primary button with white text), the icon must be recolored to match — Figma has no `currentColor` inheritance. See `rules/icon-recoloring.md` for the recoloring pattern.

## Common pitfalls

- **Searching the icon set by name on every generation** — slow and fragile; cache the set ID in the project config.
- **Skipping recoloring** — icons render in the default library color instead of inheriting the variant's foreground.
- **Hardcoding icon sizes** — always pick from the icon set's available sizes; arbitrary values produce 1:1-scaled SVGs that don't match the rest of the system.
