# Rule: Figma Slots for Dynamic Item Count

## When to apply

A component can have a **variable number of children** (N tabs, N menu items, N list rows). Without slots, the component is locked to a fixed count — designers can hide items but cannot add more.

## Why

Slots let designers **add, remove, and reorder** content inside component instances without detaching. This is the proper Figma solution for dynamic lists.

## Two slot-filling patterns

Before generating the slot's default content, decide which pattern fits the component:

### Pattern A — Instance-filled slot (homogeneous items)

Slot contains **instances of a separate sub-component set**. Every child has the same schema; variety comes from the sub-component's own variants (e.g., `State=active` vs `State=inactive`).

**When to use:**
- Every item in code has the same shape (same props, same structure). Examples: `<Tab>`, `<BreadcrumbItem>`, `<StepperStep>`, `<ListRow>`.
- A natural sub-component exists — either exported in code, or one you're generating alongside as its own component set.
- Items have internal variants (active/inactive, selected/default) that are worth exposing via the sub-component's property panel.

**Example — Tabs:**
- Slot contains 3 instances of the `Tab Item` component set (itself variants of `Size × State`).
- Designers add tabs by duplicating an instance and swapping variants via the property panel.

**Generation:** Create the sub-component set first, then populate the parent's slot with `createInstance()` calls from the sub-component's variants. Follow `rules/atomic-dependencies.md` for instance creation patterns.

### Pattern B — Frame-filled slot (heterogeneous items)

Slot contains **raw styled frames** — no sub-component. Each child is styled inline and can differ structurally from siblings.

**When to use:**
- Items in code have **different shapes or roles** (e.g., menu items AND dividers; or default items, danger items, disabled items all styled inline).
- No sub-component exists in code. Creating a Figma-only sub-component would break 1:1 parity.
- Children aren't meant to be swapped as variants — designers edit them inline.

**Example — ActionMenu:**
- Slot contains 4 item frames + 1 divider frame. Items have different label/icon/color combinations inline.
- Designers add items by duplicating an existing frame inside the instance and editing text/icon/color.

**Generation:** Build each default child as a styled `figma.createFrame()` with its own fills/strokes/text. No `createInstance()`.

### Choosing between A and B

Ask: **"Does the code export a sub-component, or does the item schema vary per row?"**

| Signal | Pattern |
|---|---|
| Code has `<TabItem>`, `<ListRow>`, `<StepperStep>` as exports | A (instance-filled) |
| Items loop over an array of the same shape, no inline variation | A (instance-filled) |
| Items include mixed kinds in one array (items + dividers + variants) | B (frame-filled) |
| Code renders items inline inside the parent, no sub-component | B (frame-filled) |
| Component is a molecule whose one exported component IS the parent | B (frame-filled) |

Do NOT default to pattern A just because "items" sounds repeatable — pick based on code structure.

## How slots work

A slot is a special frame inside a component that allows instance-level content editing. In the Figma Plugin API, slots are created by setting `isSlot = true` on a frame — but this **does NOT work via eval**.

## Workaround: `slot convert` CLI command

The figma-cli `slot convert` command works, but it cannot target nodes by ID inside component set variants. The workaround:

1. **Create the frame** inside the component via eval (as a normal frame with auto-layout)
2. **Add default children** (component instances) inside the frame
3. **Select the frame** via eval: `figma.currentPage.selection = [frameNode]`
4. **Run `slot convert`** without a node ID (operates on selection)

```bash
# Chain select + convert in ONE bash call (selection does NOT persist across
# separate CLI invocations — a second `node src/index.js ...` call loses it).
node src/index.js eval "(async () => {
  const node = await figma.getNodeByIdAsync('<frame-id>');
  if (node) figma.currentPage.selection = [node];
  return 'Selected';
})()" && node src/index.js slot convert --name "SlotName"
```

## Important notes

- `node.isSlot = true` in eval **silently fails** — the property is not set, no error thrown
- `slot convert <nodeId>` **fails for nodes inside component set variants** — returns "Cannot read properties of null"
- The selection + headless `slot convert` approach is the only reliable method
- **Selection does NOT persist between separate CLI invocations.** Chain the select eval and `slot convert` with `&&` in a single bash command. Running them as two separate tool calls will produce "✗ No frame selected".
- **The `--name` flag may be ignored** — the converted slot is often named `Slot` regardless of what you pass. Rename in a follow-up eval:
  ```javascript
  const slot = await figma.getNodeByIdAsync('<new-slot-id>');
  slot.name = 'Items';
  ```
- **The slot ID changes on conversion.** The original frame ID is no longer valid; the CLI prints the new slot ID (`Slot ID: <id>`) in stdout — capture it from there, or query the component's children after conversion to find the new SLOT node.
- After conversion, the node type changes from `FRAME` to `SLOT`
- Process each variant's slot frame separately (one select + convert per frame)

## Full workflow for component sets

When creating a component set where each variant needs a slot:

```javascript
// In the eval script: create frames (NOT slots) with default content
for (const variant of variants) {
  const container = figma.createComponent();
  // ... set up container

  const slotFrame = figma.createFrame();
  slotFrame.name = 'Items';
  slotFrame.layoutMode = 'HORIZONTAL';
  slotFrame.fills = [];
  // ... add default instances
  container.appendChild(slotFrame);
}

// After combining as variants, return the slot frame IDs
```

Then in sequential bash calls:
```bash
# For each slot frame ID returned:
node src/index.js eval "(async () => { ... select frame ... })()"
node src/index.js slot convert --name "Items"
```

## Verification

After conversion, verify with:
```javascript
const node = await figma.getNodeByIdAsync('<slot-id>');
console.log(node.type); // Should be "SLOT", not "FRAME"
```

## Combining with atomic dependencies

When a slot contains instances of existing component sets (e.g., a FilterBar slot containing Button and Select instances), the slot's default children should use `createInstance()` from the resolved dependency map rather than raw frames. See `rules/atomic-dependencies.md` for the resolution workflow.
