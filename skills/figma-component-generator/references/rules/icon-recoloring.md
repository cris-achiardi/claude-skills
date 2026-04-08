# Rule: Icon Recoloring

## When to apply

Lucide icon instances are placed inside component variants that have **different foreground colors** (e.g., solid buttons with white icons vs outline buttons with colored icons).

## Why

Figma has **no `currentColor` inheritance**. In CSS, icons inherit color from their parent via `color: currentColor`. In Figma, icon instances keep their default fill/stroke from the library (typically `foreground-base` / dark). They must be explicitly recolored per variant.

## Recoloring pattern

Lucide icons use **strokes** (not fills) for their vector paths. To recolor, traverse the instance tree recursively and rebind all vector strokes and fills:

```javascript
const recolorIcon = (node, fgVariable) => {
  if (node.strokes && node.strokes.length > 0) {
    const paint = figma.variables.setBoundVariableForPaint(
      node.strokes[0], 'color', fgVariable
    );
    node.strokes = [paint];
  }
  if (node.fills && node.fills.length > 0 && node.fills[0].type === 'SOLID') {
    const paint = figma.variables.setBoundVariableForPaint(
      node.fills[0], 'color', fgVariable
    );
    node.fills = [paint];
  }
  if ('children' in node && node.children) {
    for (const child of node.children) {
      recolorIcon(child, fgVariable);
    }
  }
};
```

## Color source strategy

**Best practice:** Match the icon color to the **sibling text node's fill variable**. This ensures icons and text always use the same foreground color.

```javascript
// Find the label text to get its variable
const labelNode = variant.children.find(c => c.type === 'TEXT');
let labelVarId = null;
if (labelNode?.boundVariables?.fills?.[0]) {
  labelVarId = labelNode.boundVariables.fills[0].id;
}
const labelVar = allVars.find(v => v.id === labelVarId);

// Apply same variable to icon
if (labelVar) recolorIcon(iconInstance, labelVar);
```

**Fallback:** When there's no sibling text (e.g., IconButton), use the variant's designated foreground variable from the color map.

## When NOT to recolor

- Icons in the Lucide Icon component set itself (library source) — leave as-is
- Icons that should always be a fixed color regardless of variant (rare)

## Common pitfalls

- Forgetting to recolor after `createInstance()` — icons default to dark
- Only recoloring fills but not strokes (Lucide uses strokes)
- Not traversing recursively — some icons have nested groups/vectors
