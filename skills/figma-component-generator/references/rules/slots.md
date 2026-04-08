# Rule: Figma Slots for Dynamic Item Count

## When to apply

A component can have a **variable number of children** (N tabs, N menu items, N list rows). Without slots, the component is locked to a fixed count — designers can hide items but cannot add more.

## Why

Slots let designers **add, remove, and reorder** content inside component instances without detaching. This is the proper Figma solution for dynamic lists.

## How slots work

A slot is a special frame inside a component that allows instance-level content editing. In the Figma Plugin API, slots are created by setting `isSlot = true` on a frame — but this **does NOT work via eval**.

## Workaround: `slot convert` CLI command

The figma-cli `slot convert` command works, but it cannot target nodes by ID inside component set variants. The workaround:

1. **Create the frame** inside the component via eval (as a normal frame with auto-layout)
2. **Add default children** (component instances) inside the frame
3. **Select the frame** via eval: `figma.currentPage.selection = [frameNode]`
4. **Run `slot convert`** without a node ID (operates on selection)

```bash
# Step 3: Select the frame
node src/index.js eval "(async () => {
  const node = await figma.getNodeByIdAsync('<frame-id>');
  if (node) figma.currentPage.selection = [node];
  return 'Selected';
})()"

# Step 4: Convert to slot (operates on selection)
node src/index.js slot convert --name "SlotName"
```

## Important notes

- `node.isSlot = true` in eval **silently fails** — the property is not set, no error thrown
- `slot convert <nodeId>` **fails for nodes inside component set variants** — returns "Cannot read properties of null"
- The selection + headless `slot convert` approach is the only reliable method
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
