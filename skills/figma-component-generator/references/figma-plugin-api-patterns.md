# Figma Plugin API Patterns for Component Generation

## Execution Environment

All Figma operations run via the figma-cli `eval` command:
```bash
cd <figma-cli-repo-path> && node src/index.js eval "<javascript-code>"
```

The code executes inside Figma's Plugin API context. The `figma` global is available.

## Connection Prerequisites

Before running any eval, verify the connection:
```bash
curl -s http://localhost:9222/json
```
If this returns empty or errors, the daemon/CDP connection is down. Run:
```bash
node src/index.js connect
```

## Page Navigation

To switch to a target page by name:
```javascript
const page = figma.root.children.find(p => p.name.trim() === '> PageName');
if (page) figma.currentPage = page;
```

To find a page from a Figma URL (the node-id parameter maps to the page):
```javascript
// URL format: https://www.figma.com/design/<fileKey>/<fileName>?node-id=<pageId>&...
// node-id is URL-encoded, e.g., "2001-2" means "2001:2"
const targetId = '2001:2'; // decoded from URL
const page = figma.root.children.find(p => p.id === targetId);
```

## Font Loading

**CRITICAL**: Always load fonts before creating text nodes. Otherwise text operations will fail silently.
```javascript
await figma.loadFontAsync({ family: 'Inter', style: 'Medium' });
await figma.loadFontAsync({ family: 'Inter', style: 'Regular' });
await figma.loadFontAsync({ family: 'Inter', style: 'Bold' });
```

## Creating a Component Variant

Each variant in a component set is a `ComponentNode`:
```javascript
const comp = figma.createComponent();
comp.name = 'Variant=solid, Color=primary, Size=md';

// IMPORTANT: Call resize() FIRST, then set sizing modes.
// resize() implicitly sets both axes to FIXED, overriding any prior AUTO setting.
comp.layoutMode = 'HORIZONTAL';
comp.resize(1, 24);  // call resize BEFORE sizing modes
comp.primaryAxisSizingMode = 'AUTO';   // hug width (overrides the FIXED from resize)
comp.counterAxisSizingMode = 'FIXED';  // fixed height at 24px
comp.counterAxisAlignItems = 'CENTER';
comp.primaryAxisAlignItems = 'CENTER';
comp.paddingLeft = 10;
comp.paddingRight = 10;
comp.itemSpacing = 4;
comp.cornerRadius = 9999; // pill shape
```

**CRITICAL: resize() overrides sizing modes.** `resize()` implicitly sets both axes to `FIXED`. Always call `resize()` BEFORE setting `primaryAxisSizingMode` or `counterAxisSizingMode`. If you call `resize()` after, it will reset your `AUTO` (hug) setting back to `FIXED`, causing 1px collapsed dimensions.

**IMPORTANT**: Figma API uses `'AUTO'` for hug contents, NOT `'HUG'`. Using `'HUG'` will throw an error.

## Sizing Modes

- `primaryAxisSizingMode: 'AUTO'` = hug contents along primary axis
- `primaryAxisSizingMode: 'FIXED'` = fixed size along primary axis
- `counterAxisSizingMode: 'AUTO'` = hug contents along counter axis
- `counterAxisSizingMode: 'FIXED'` = fixed size along counter axis

**CRITICAL**: Which axis is "primary" depends on `layoutMode`:
- `layoutMode = 'HORIZONTAL'`: primary = width, counter = height
- `layoutMode = 'VERTICAL'`: primary = height, counter = width

This means the same goal ("fixed width, hug height") requires DIFFERENT settings depending on layout direction:

| Goal | HORIZONTAL layout | VERTICAL layout |
|---|---|---|
| Fixed width, hug height | primary=FIXED, counter=AUTO | primary=AUTO, counter=FIXED |
| Hug width, fixed height | primary=AUTO, counter=FIXED | primary=FIXED, counter=AUTO |
| Hug both | primary=AUTO, counter=AUTO | primary=AUTO, counter=AUTO |

Common patterns:
- Badge/chip/tag (horizontal): HUG width (`primary=AUTO`), FIXED height (`counter=FIXED`)
- Card (vertical): FIXED width (`counter=FIXED`), HUG height (`primary=AUTO`)
- FormField vertical: FIXED width (`counter=FIXED`), HUG height (`primary=AUTO`)
- FormField horizontal: FIXED width (`primary=FIXED`), HUG height (`counter=AUTO`)
- Button (horizontal): HUG or FIXED width, FIXED height

## Fills and Strokes

```javascript
// Solid fill
comp.fills = [{ type: 'SOLID', color: { r: 0.5, g: 0.5, b: 0.5 } }];

// No fill (transparent)
comp.fills = [];

// Stroke (for outline variants)
comp.strokes = [{ type: 'SOLID', color: { r: 0.5, g: 0.5, b: 0.5 } }];
comp.strokeWeight = 1;
comp.strokeAlign = 'INSIDE';  // 'INSIDE', 'OUTSIDE', 'CENTER'
```

## Variable Binding

To bind a Figma variable to a fill or stroke color:

```javascript
// Get all local variables
const allVars = await figma.variables.getLocalVariablesAsync();

// Find variable by name
const variable = allVars.find(v => v.name === 'background/interactive/primary');

// Bind to fill
const paint = figma.variables.setBoundVariableForPaint(node.fills[0], 'color', variable);
node.fills = [paint];

// Bind to stroke
const strokePaint = figma.variables.setBoundVariableForPaint(node.strokes[0], 'color', variable);
node.strokes = [strokePaint];
```

**IMPORTANT**: The node must already have at least one fill/stroke before binding. Set a placeholder fill first, then bind.

## Getting Available Variables and Collections

```javascript
const collections = await figma.variables.getLocalVariableCollectionsAsync();
const summary = collections.map(c => ({
  name: c.name,
  modes: c.modes.map(m => m.name),
  varCount: c.variableIds.length
}));

// Get all variables with their names
const allVars = await figma.variables.getLocalVariablesAsync();
const varNames = allVars.map(v => v.name);
```

## Creating Text Nodes

```javascript
const text = figma.createText();
text.name = 'Label';
text.fontName = { family: 'Inter', style: 'Medium' };
text.fontSize = 13;
text.lineHeight = { value: 100, unit: 'PERCENT' };
text.characters = 'Label Text';
text.fills = [{ type: 'SOLID', color: { r: 0.5, g: 0.5, b: 0.5 } }];

// Append to parent BEFORE setting layout properties
parentFrame.appendChild(text);
text.layoutSizingHorizontal = 'FILL'; // for text wrapping
```

## Creating Shape Nodes

```javascript
// Ellipse (for dots, avatars)
const dot = figma.createEllipse();
dot.name = 'Dot';
dot.resize(6, 6);
dot.fills = [{ type: 'SOLID', color: { r: 0.5, g: 0.5, b: 0.5 } }];

// Rectangle
const rect = figma.createRectangle();
rect.resize(100, 40);
rect.cornerRadius = 8;
```

## Boolean Component Properties

Add toggleable elements (dots, icons) as boolean component properties:
```javascript
// Add property to component
comp.addComponentProperty('Show Dot', 'BOOLEAN', false);

// Link element visibility to property
const propKey = Object.keys(comp.componentPropertyDefinitions)
  .find(k => k.startsWith('Show Dot'));
if (propKey) {
  dotNode.componentPropertyReferences = { visible: propKey };
}
```

## Combining into Component Set

After creating all individual component variants:
```javascript
const componentSet = figma.combineAsVariants(allComponents, figma.currentPage);
componentSet.name = 'ComponentName';
```

### Variant Naming Convention

Figma parses variant names from the component name using `Property=value` pairs:
```
Variant=solid, Color=primary, Size=md
```
Each unique property becomes a variant property in the component set.

## Grid Layout for Component Sets

After combining, position variants in a readable grid:
```javascript
// Remove auto-layout from set for manual positioning
componentSet.layoutMode = 'NONE';

// Position each child by parsing its variant properties
const colWidth = 120;
const rowHeight = 44;
const sectionGap = 24;
const pad = 32;

for (const child of componentSet.children) {
  const props = parseVariantName(child.name); // parse Property=value pairs
  const col = sizeIndex;    // e.g., sm=0, md=1, lg=2
  const row = colorIndex;   // e.g., neutral=0, primary=1, ...
  const section = variantIndex; // e.g., solid=0, soft=1, outline=2

  child.x = pad + col * colWidth;
  child.y = pad + section * (colorsCount * rowHeight + sectionGap) + row * rowHeight;
}

// Resize set to fit
componentSet.resize(totalWidth, totalHeight);
componentSet.fills = [{ type: 'SOLID', color: { r: 1, g: 1, b: 1 } }];
```

## CSS Token to Figma Variable Mapping

Common token patterns and their Figma variable name equivalents:

| CSS Token | Figma Variable Name Pattern |
|---|---|
| `var(--background-interactive-primary)` | `background/interactive/primary` |
| `var(--foreground-base)` | `foreground/base` |
| `var(--border-default)` | `border/default` |
| `var(--size-24)` | `size/24` |
| `var(--radius-full)` | `radius/full` |
| `var(--font-size-xs)` | `font/size/xs` |

**Conversion rule**: Strip `var(--`, `)`, replace `-` with `/` for path segments.
Exception: multi-word segments like `primary-alt` become `primaryalt` (no separator).

## Error Handling

- Always wrap eval code in `(async () => { ... })()` for async operations
- Return JSON.stringify() results for structured output
- If a variable is not found, collect it in a "missing variables" report instead of failing
- Check for node existence before manipulating: `if (!node) return 'Node not found';`

## Eval Size Limits

Large eval scripts work fine through the daemon. The daemon maintains persistent WebSocket connections and has a 60-second timeout. For very complex components, the script can be substantial (several KB of JavaScript).
