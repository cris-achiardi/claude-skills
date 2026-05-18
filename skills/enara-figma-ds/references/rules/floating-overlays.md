# Rule: Floating Overlays — Recognize and Treat as Their Own Entity

## When to apply

A component has content that, in real product use, **renders outside the parent's layout flow** — overlapping or floating above other UI rather than pushing siblings. Detected by:

- Source uses a floating-UI library (`@floating-ui/react`, `floating-ui`, `react-aria` Popover, `@radix-ui/react-popover`, `@radix-ui/react-dropdown-menu`, `@radix-ui/react-tooltip`, `cmdk`, `@headlessui/react`)
- Source uses React portals (`createPortal`, `<Portal>`, Radix `Portal` primitives)
- CSS uses `position: fixed` or `position: absolute` for the expanded part with high `z-index`
- Conditional rendering tied to an open/closed state (`{open && <Menu .../>}`)
- Component's expanded state visually overlaps siblings in the live product but doesn't push them

## Why recognition matters

Figma doesn't enforce the floating relationship — it's a designer-tooling concern, not a Figma-engine concern. But two things go wrong if the floating part is *only* a hidden child of the trigger gated by a `State=open` variant:

1. **Mockup composition is awkward.** When designers drop the trigger into a page mockup and switch it to `State=open`, Figma's auto-layout pushes everything below it down — which never happens at runtime. Designers end up with mockups that don't reflect production.
2. **The floating part isn't reusable.** It can't be dropped independently into other mockups (e.g., to show a Toast somewhere unrelated to a trigger), and Figma's prototyping `Open Overlay` action can't target it as its own entity.

The goal is to make the floating element a **first-class, independently usable entity** in the Figma library. Whether that's a separate component set or a variant of the parent that designers can detach and use floats in prototypes is a judgment call — both produce reusable floating UI as long as the entity is recognized and treated deliberately.

## Two valid shapes — designer's choice

### Shape A — Split into sibling component sets (recommended for complex overlays)

Generate two component sets on the same page:

1. **`<Component>`** (trigger) — variants for resting states (`HasValue`, `Disabled`, `Focused`)
2. **`<Component>/<Floating>`** (overlay) — variants for the floating part's own states (`State=open|loading|empty|error`, or `Placement=top|bottom|...`)

Slash naming makes the relationship discoverable in the library. Designers compose mockups by placing both instances near each other; Figma prototyping wires them via `Open Overlay`/`Close Overlay` actions on the trigger.

**Use this shape when:**
- The floating part has its own non-trivial state space (loading/empty/error states)
- The floating part is reused across multiple triggers (e.g., a generic `Menu` used by `Dropdown`, `ContextMenu`, `Select`)
- The trigger's resting variants and the overlay's states feel orthogonal

### Shape B — Single component with `State=open` variant

Keep one component set with `State=closed|open|...` as a variant axis. The "open" variant contains the floating part as a child.

**Use this shape when:**
- The floating part is small and tightly coupled to one trigger (e.g., a simple Tooltip)
- The "open" state has no internal state space worth exposing (no loading/empty/error)
- Designers prefer clicking through variant states in the property panel to wiring overlays

If you go with Shape B, **still treat the floating part as a recognizable subtree** — give it a clear named frame (e.g., `Dropdown`, `Popover Content`) so designers can detach the instance and use that subtree independently when needed. Don't bury it in unnamed wrapper frames.

## Figma prototyping context

Figma natively supports floating overlays via prototyping interactions:

- `Open Overlay` action — triggers display a target frame as a modal/positioned overlay
- Overlay positions: Center, Top Left, Manual (relative to trigger), etc.
- Overlay can have `Close when clicking outside`, swap behavior, etc.

Either Shape A or Shape B can be wired this way. Shape A makes the wiring more obvious (the overlay frame is a separate publishable thing), but Shape B's `State=open` variant can also serve as an overlay target in prototypes if the open variant is well-named.

## Common examples

| Component | Recommended shape | Notes |
|---|---|---|
| Select / Combobox / Autocomplete | A — `Select` + `Select/Dropdown` | Dropdown has open/loading/empty/error states |
| DatePicker | A — `DatePicker` + `DatePicker/Calendar` | Calendar has month/year navigation states |
| Popover (generic) | A — `Popover/Trigger` + `Popover/Content` | Content is reused by many features |
| Tooltip | B usually — `Tooltip` only | No separate trigger; wraps any element. Single component with `Placement` variants |
| ContextMenu / Dropdown | A — `Dropdown/Trigger` + `Dropdown/Menu` | Menu often slot-fills with `Menu Item` instances |
| Dialog / Modal | A — `Dialog/Trigger` (optional) + `Dialog/Content` | Content has Size variants |
| Drawer | A — `Drawer/Trigger` (optional) + `Drawer/Panel` | Panel has Side variants |
| Toast | A — `Toast` standalone | No trigger — programmatic. Single floating set with Variant=info\|success\|error |
| Disclosure (inline expand) | NEITHER — single component with `State=open\|closed` | Genuinely inline, no portal, no float |

## Detection signals in source

When reading the component source in Step 2, scan for:

```tsx
// Library imports — strongest signal
import { Popover } from '@radix-ui/react-popover';
import { useFloating, autoUpdate } from '@floating-ui/react';
import { Combobox } from '@headlessui/react';
import { Command } from 'cmdk';

// Portal usage
import { createPortal } from 'react-dom';
return createPortal(<Menu .../>, document.body);

// Conditional render of overlay content
{open && <DropdownContent ... />}
```

CSS signals:
```css
.dropdown {
  position: absolute;  /* or fixed */
  z-index: 50;         /* or any high value */
}
```

If any of these fire, treat the component as a floating-overlay candidate and pick a shape.

## Generation workflow

In Step 6 of `SKILL.md`, when this rule applies:

1. **Decide the shape.** Default to A for components with non-trivial overlay state spaces (loading/empty/error/multi-view). Default to B for small/single-state overlays (simple tooltips, single-state popovers).
2. **If unsure, ask the user.** Present the trade-off briefly: "This component looks like a floating overlay. Generate as a single component with a `State=open` variant, or split into a trigger and a separate floating component set?" Wait for the answer before proceeding.
3. **For Shape A:**
   - Build the trigger spec FIRST. Its variants exclude the open/expanded state.
   - Build the floating spec SECOND. Position it on the canvas next to the trigger, NOT inside it.
   - Both component sets are published. Slash-named (`<Component>` + `<Component>/<Floating>`).
4. **For Shape B:**
   - Keep one component set with the floating subtree as a clearly-named child of the open variant.
   - Make sure the floating subtree is its own auto-layout frame with a meaningful name (e.g., `Dropdown`, `Popover Content`) so it can be detached and reused.
5. **In the generation report**, note the shape:
   ```
   ## Component Generated: AutocompleteSelect (Shape A — split overlay)
   - Trigger: AutocompleteSelect (HasValue × Disabled = 4 variants)
   - Floating: AutocompleteSelect/Dropdown (State = 4 variants)
   ```
   Or:
   ```
   ## Component Generated: Tooltip (Shape B — single component)
   - Variants: Placement (4) × Size (3) = 12 variants
   - Floating subtree: `Tooltip Content` frame (detachable)
   ```

## What NOT to do

- **Don't** bury the floating part in unnamed wrapper frames. Even in Shape B, the overlay subtree needs a clear name so designers can find and detach it.
- **Don't** mix trigger states and overlay states on the same variant axis (`State=closed | open | loading | empty | disabled`). Trigger states (`disabled`, `focused`) belong on the trigger; overlay states (`loading`, `empty`) belong on the overlay. Even within Shape B, model them as two separate variant axes (`Disabled=true|false` × `State=closed|open|loading|empty`).
- **Don't** model floating placement as a meaningful design variant unless the placement materially changes the overlay's appearance (e.g., arrow position on a Tooltip). Runtime placement is the consumer's concern.

## Edge cases

- **Inline disclosures** (no portal, genuinely expand inline): NOT a floating overlay. Single component with `State=open|closed`. Detection: no portal/floating-UI imports, no `position: absolute` on the expanded part.
- **Tooltips** without a separate trigger element (wraps arbitrary children): generate only the floating set. The trigger is whatever the consumer wraps.
- **Modals over the whole viewport**: the trigger is often a regular Button (no separate trigger needed). Generate just `Dialog/Content`.
- **Bottom sheets / drawers**: same pattern as Dialog. Trigger optional, panel is the floating part.

## Relationship to other rules

- **`rules/slots.md`**: floating components often use Pattern A slots (e.g., `Dropdown/Menu` slot-fills with `Menu Item` instances). Apply both rules together.
- **`rules/nested-components.md`**: when the floating content has its own per-item state (selected option, hovered menu item), the items get their own sub-component set.
- **`rules/atomic-dependencies.md`**: the floating set may depend on existing components (e.g., `Dropdown/Menu` uses `Menu Item` instances). Resolve the floating set's dependencies the same way as any other compositional component.
