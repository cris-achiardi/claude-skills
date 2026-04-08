# Figma Typography Reference

> **PROJECT-SPECIFIC**: Customize this file for your design system.

## Font Family

Replace with your project's font family:

- Font family: `'Your Font', sans-serif`
- All text in generated components must use this font

## Discovering Your Text Styles

Run this to list all text styles in your Figma file:
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

## Applying a Text Style

```javascript
const textStyles = await figma.getLocalTextStylesAsync();
const style = textStyles.find(s => s.name === 'Body/Md/Regular');

// Apply BEFORE setting characters
if (style) textNode.textStyleId = style.id;
textNode.characters = 'Hello';
```

**IMPORTANT**: Apply text style BEFORE `.characters` to avoid font loading issues.

## Font Loading

Even when using text styles, fonts must be loaded before creating text:
```javascript
await figma.loadFontAsync({ family: 'YourFont', style: 'Regular' });
await figma.loadFontAsync({ family: 'YourFont', style: 'Medium' });
```

## CSS Token to Figma Text Style Mapping

Map your CSS tokens to Figma style names. Example:

| CSS Token | Figma Style |
|---|---|
| `--text-body-md-regular` | `Body/Md/Regular` |
| `--text-title-lg-semibold` | `Title/Lg/Semibold` |

Conversion pattern: `--text-{category}-{size}-{weight}` becomes `{Category}/{Size}/{Weight}`

## Handling Weight Overrides

When a component uses a base text style but overrides weight:
```javascript
textNode.textStyleId = baseStyle.id;
// Override weight (detaches from style, acceptable for overrides)
textNode.fontName = { family: 'YourFont', style: 'SemiBold' };
```

## Font Weight to Style Name

Map your font's weight values to style names:

| Weight Value | Style Name |
|---|---|
| 300 | Light |
| 400 | Regular |
| 500 | Medium |
| 600 | SemiBold |
| 700 | Bold |
