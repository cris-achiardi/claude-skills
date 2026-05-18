# Figma Typography Reference

How to apply text styles, load fonts, and map CSS typography tokens to Figma text styles when generating components via the Plugin API. The font family, weight set, and text-style names are project-specific — consuming skills should encode those in their own config and pass values into the patterns below.

## Discovering Text Styles

List all text styles in the open Figma file:
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

Use the returned list to build the project's CSS-token → Figma-style mapping.

## Applying a Text Style

```javascript
const textStyles = await figma.getLocalTextStylesAsync();
const style = textStyles.find(s => s.name === 'Body/Md/Regular');

// Apply BEFORE setting characters
if (style) textNode.textStyleId = style.id;
textNode.characters = 'Hello';
```

**CRITICAL**: Apply `textStyleId` BEFORE `.characters`. Setting characters first forces Figma to use its default font (Inter); applying a style afterward triggers font-loading errors on text nodes whose font hasn't been loaded yet.

## Font Loading

Even when using text styles, the underlying fonts must be loaded before creating text nodes:
```javascript
await figma.loadFontAsync({ family: 'Outfit', style: 'Regular' });
await figma.loadFontAsync({ family: 'Outfit', style: 'Medium' });
await figma.loadFontAsync({ family: 'Outfit', style: 'SemiBold' });
```

Load every weight the design system uses up-front in the eval script. Missing weight loads cause silent failures (text nodes keep Inter instead of the requested family).

## CSS Token → Figma Text Style Mapping

Most design systems express text styles as CSS custom properties like `--text-{category}-{size}-{weight}`. The corresponding Figma style name is the same path with `/` separators and TitleCase segments.

Conversion pattern:

```
--text-body-md-regular        →  Body/Md/Regular
--text-title-lg-semibold      →  Title/Lg/Semibold
--text-caption-sm-medium      →  Caption/Sm/Medium
```

The exact category/size/weight enum is project-specific. Build the mapping once per project and store it in the skill's config.

## Handling Weight Overrides

When a component uses a base text style but locally overrides the weight (e.g., a Body/Md style rendered SemiBold for emphasis), set `textStyleId` first, then override `fontName`. The override detaches the node from the style for that property only — this is the correct Figma idiom for weight overrides:

```javascript
textNode.textStyleId = baseStyle.id;
// Override weight (detaches from style for fontName, acceptable for overrides)
textNode.fontName = { family: 'Outfit', style: 'SemiBold' };
```

The base text style's font size, line height, and letter spacing are preserved; only the weight changes.

## Font Weight → Style Name

Most modern variable/static fonts use these conventional style names:

| Weight Value | Style Name |
|---|---|
| 300 | Light |
| 400 | Regular |
| 500 | Medium |
| 600 | SemiBold |
| 700 | Bold |

Some fonts use non-standard names (`Demi` instead of `Medium`, `Heavy` instead of `Bold`). When in doubt, run the discovery script above and use the exact `style` string Figma returns.

## Common pitfalls

- **Setting `.characters` before `textStyleId`** — forces Inter font loading, produces a font-load error on the next operation.
- **Forgetting to load all weights** — text nodes silently fall back to Inter for the missing weight; the visual diff is subtle.
- **Assuming the style mapping** — always verify against the actual Figma file via the discovery script. Mismatches between CSS and Figma style names are the most common cause of "unmapped text style" failures.
