# Figma Icon Library Reference

> **PROJECT-SPECIFIC (OPTIONAL)**: Only needed if your Figma file has an icon component set.
> Delete this file if you don't have one -- the skill will fall back to the figma-cli's built-in SVG rendering.

## Discovering Your Icon Component Set

Run this to find icon component sets in your Figma file:
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

## Configuration

Replace these values with your icon set's details:

- **Component Set ID**: `YOUR_SET_ID_HERE`
- **Component Set Name**: `Your Icon Set Name`
- **Total variants**: (discovered from command above)

### Properties

| Property | Type | Default | Options |
|----------|------|---------|---------|
| Icon Name | VARIANT | (varies) | Your icon names |
| Size | VARIANT | (varies) | Your size options |

### Variant Naming Format

```
Icon Name=<icon-name>, Size=<size>
```

## Creating an Icon Instance

```javascript
const iconSet = await figma.getNodeByIdAsync('YOUR_SET_ID_HERE');
const variant = iconSet.children.find(
  c => c.name === 'Icon Name=star, Size=20px'
);
if (variant) {
  const instance = variant.createInstance();
  parentFrame.appendChild(instance);
}
```

## Semantic Icon Mappings

Map semantic meanings to your icon names:

| Semantic | Icon Name | Usage |
|----------|----------|-------|
| close | `x` | Close buttons |
| search | `search` | Search inputs |
| loading | `loader-2` | Loading spinners |
| chevron-down | `chevron-down` | Dropdowns |
| check | `check` | Checkboxes |
| error | `alert-circle` | Error states |
| success | `check-circle-2` | Success states |
| warning | `alert-triangle` | Warning states |
| info | `info` | Info states |

Add more mappings specific to your project.

## Size Selection Guide

| Context | Recommended Size |
|---------|-----------------|
| Inside small components (Badge, Chip) | Smallest available |
| Default components (Alert, Button) | Medium |
| Large or standalone icons | Largest available |
