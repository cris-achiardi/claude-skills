# Rule: Atomic Dependency Resolution

## When to apply

The component being generated is a **molecule or organism** that composes other components. This is detected by:
- Metadata `component.category` is `molecules`, `organisms`, or `templates`
- Metadata `composition.nestedComponents` array is non-empty
- Metadata `composition.commonPartners` references components that appear in the source as imports or children
- Source file imports other design-system components (e.g., `import { Button } from '...'`)
- Source JSX renders design-system components as children (e.g., `<Button>`, `<SearchInput>`)

## Why

Without this rule, the skill creates raw frames (rectangles, text nodes) to represent children that **already exist as component sets** in the Figma file. This produces:
- Designers cannot swap variants or change properties of the child
- No link between the composed component and its atoms
- Double maintenance when the atom changes (the raw frame copy is stale)

Using instances (`componentNode.createInstance()`) preserves Figma's component system: designers get property panels, variant swapping, and automatic updates when the source atom changes.

## Step 1: Classify the component

Before generating, classify the component into one of three categories based on its source code and CSS:

| Category | Signals | Action |
|---|---|---|
| **Visual component** | Has own fills, strokes, borders, color variants, size variants in CSS | Proceed with generation |
| **Layout wrapper** | No fill, no border, no stroke in CSS; only spacing/layout props (`gap`, `padding`, `flex`, `grid`); accepts `children` as primary prop; metadata `component.type` is `'layout'` | **STOP — ask the user** (see Clarity Checkpoint below) |
| **Compositional** | Has visual identity (fills, borders, shadows) AND composes other components | Generate, but use instances for composed children |

### Clarity checkpoint (layout wrappers)

When a component is classified as a **layout wrapper**, present the user with options before proceeding:

> This component is a layout wrapper — it has no visual identity of its own (no fill, no border), only spacing and layout. In Figma, this may not need to be a component set.
>
> Options:
> 1. **Documentation only** — generate a docs frame using the `/docs-to-figma` skill instead
> 2. **Wrapper with slot** — create a minimal component set with variants and a slot for children (see `rules/slots.md`)
> 3. **Skip** — do not generate anything for this component
>
> Which approach would you like?

Do NOT proceed with generation until the user chooses.

### Classification code signals

To classify, check the component's CSS module for visual identity:

**Visual signals** (any one = visual identity present):
- `background-color` / `background` (not transparent/none)
- `border` / `border-color` / `border-width` (not 0/none)
- `box-shadow`
- Color variants that change fills (multiple `background-*` tokens)

**Layout-only signals** (ALL must be true):
- No `background-color` (or only transparent)
- No `border` (or only 0/none)
- No `box-shadow`
- Primary CSS is: `display`, `flex`/`grid`, `gap`, `padding`, `align-items`, `justify-content`
- Component accepts `children` as its main content prop

## Step 2: Extract dependencies

From the component spec built in Step 2 of the main workflow, collect all dependency names:

1. **From metadata**: `composition.nestedComponents` array (e.g., `['SearchInput', 'Select', 'Button']`)
2. **From metadata**: `composition.commonPartners` array — but only include entries that are also imported or rendered in the source code
3. **From source imports**: Any import of a design-system component (e.g., `import { Button } from '../atoms/Button'`)
4. **From source JSX**: Component tags that match known design-system components

Deduplicate into a single list of dependency names.

## Step 3: Query Figma for existing component sets

Search all pages for component sets matching each dependency name:

```javascript
(async () => {
  const dependencyNames = ['Button', 'SearchInput', 'Select'];
  const results = {};

  for (const name of dependencyNames) {
    const matches = figma.root.findAll(node =>
      node.type === 'COMPONENT_SET' && node.name === name
    );
    if (matches.length > 0) {
      const set = matches[0];
      results[name] = {
        id: set.id,
        page: set.parent?.name || 'unknown',
        variants: set.children.map(c => c.name),
        variantCount: set.children.length,
      };
    } else {
      results[name] = null;
    }
  }

  return JSON.stringify(results, null, 2);
})()
```

If multiple component sets share the same name, warn the user and let them pick.

## Step 4: Build dependency map and handle missing

For each dependency:

| Status | Action |
|---|---|
| **Found** | Record the component set ID, default variant, and available variant properties. Use instances during generation. |
| **Not found** | Warn the user: "Component set `X` not found in the Figma file. Consider generating it first with `/figma-component-generator`. Proceeding with a placeholder frame." |

When a dependency is missing, do NOT silently create a raw frame that mimics the component. Instead:
1. Create a placeholder frame with a dashed stroke (`dashPattern = [6, 4]`) and the component name as a text label
2. Add a comment in the generation report listing all missing dependencies

## Step 5: Use instances during generation

When building the parent component's eval script, replace raw frame creation with instance creation for each found dependency:

```javascript
// --- Finding a component set by ID (from dependency map) ---
const buttonSet = await figma.getNodeByIdAsync('<button-set-id>');

// --- Picking the right variant ---
// Choose the variant that matches the context
// e.g., AlertDialog confirm button: Role=primary, Size=md
const confirmVariant = buttonSet.children.find(c =>
  c.name.includes('Role=primary') &&
  c.name.includes('Size=md')
);
// Fallback to default variant (first child)
const variant = confirmVariant || buttonSet.defaultVariant || buttonSet.children[0];

// --- Creating the instance ---
const confirmBtn = variant.createInstance();
parent.appendChild(confirmBtn);

// --- Overriding instance text ---
const labelNode = confirmBtn.findOne(n => n.type === 'TEXT' && n.name === 'Label');
if (labelNode) {
  await figma.loadFontAsync(labelNode.fontName);
  labelNode.characters = 'Delete';
}
```

### Variant selection heuristics

When the source code specifies props for a child component, map those to Figma variant properties:

| Source prop | Figma variant property | Example |
|---|---|---|
| `role="primary"` / `role="ghost"` | `Role=primary` / `Role=ghost` | `<Button role="ghost">Cancel</Button>` |
| `color="danger"` | `Color=danger` | `<Button color="danger">Delete</Button>` |
| `size="md"` | `Size=md` | Inherit from parent's size context |

If the source code does not specify a prop, use the default variant value from the dependency's metadata.

## Cross-references

- For **repeated instances with per-item state** (e.g., tab items inside tabs), see `rules/nested-components.md` — that rule covers creating new sub-component sets. This rule covers reusing **existing** component sets.
- For **dynamic item count** in layout wrappers or compositional components, combine with `rules/slots.md` — create a slot and populate it with instances as default content.
- For **icon instances** inside composed children, the icon is already handled by the child component's own generation. Do not recolor icons inside instances — the instance inherits its variant's icon colors.
