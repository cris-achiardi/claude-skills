# Rule: Figma Sizing Modes

## When to apply

Every component — this rule is always relevant.

## Critical: `resize()` before sizing modes

`resize()` implicitly sets **both axes to FIXED**, overriding any prior `AUTO` (hug) setting. This causes 1px collapsed dimensions.

**Always call `resize()` BEFORE setting sizing modes:**

```javascript
// CORRECT
comp.resize(320, 1);                    // set dimensions first
comp.primaryAxisSizingMode = 'AUTO';    // then override to hug
comp.counterAxisSizingMode = 'FIXED';   // keep fixed

// WRONG — resize overrides AUTO back to FIXED
comp.primaryAxisSizingMode = 'AUTO';
comp.resize(320, 1);                    // undoes the AUTO above
```

## Axis direction depends on layout mode

Which axis is "primary" flips between HORIZONTAL and VERTICAL layouts:

- `layoutMode = 'HORIZONTAL'`: **primary = width**, counter = height
- `layoutMode = 'VERTICAL'`: **primary = height**, counter = width

The same goal requires different settings depending on direction:

| Goal | HORIZONTAL layout | VERTICAL layout |
|---|---|---|
| Fixed width, hug height | primary=FIXED, counter=AUTO | primary=AUTO, counter=FIXED |
| Hug width, fixed height | primary=AUTO, counter=FIXED | primary=FIXED, counter=AUTO |
| Hug both | primary=AUTO, counter=AUTO | primary=AUTO, counter=AUTO |

## Figma uses 'AUTO', not 'HUG'

`primaryAxisSizingMode: 'HUG'` throws an error. The correct value is `'AUTO'`.

## Common component sizing patterns

| Component Type | Layout | Width | Height |
|---|---|---|---|
| Badge, Chip, Tag | HORIZONTAL | hug (AUTO) | fixed |
| Button | HORIZONTAL | hug or fixed | fixed |
| Card | VERTICAL | fixed | hug (AUTO) |
| Alert | HORIZONTAL | fixed | hug (AUTO) |
| FormField vertical | VERTICAL | fixed (counter) | hug (primary AUTO) |
| FormField horizontal | HORIZONTAL | fixed (primary) | hug (counter AUTO) |
| Input, SearchInput | HORIZONTAL | fixed | hug (AUTO) |
| Divider horizontal | — | fixed | fixed (1px) |
| IconButton | HORIZONTAL | fixed | fixed (square) |

## Text node sizing

Text nodes inside auto-layout parents need `layoutSizingHorizontal = 'FILL'` for text wrapping. Set this **AFTER** appending the text node to its parent:

```javascript
parent.appendChild(textNode);
textNode.layoutSizingHorizontal = 'FILL'; // must be after appendChild
```
