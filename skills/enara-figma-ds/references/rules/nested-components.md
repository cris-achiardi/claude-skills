# Rule: Nested Component Architecture

## When to apply

A component contains **repeated elements that have their own visual states** (active/inactive, enabled/disabled, selected/unselected, hover). This is detected by:
- Multiple elements rendered from a `.map()` or loop in the source code
- Conditional className/styling based on a per-item prop (e.g., `isActive`, `isSelected`, `isDisabled`)
- Items that share the same structure but differ in state

## Why

Without nested components, designers cannot toggle individual element states from the Figma properties panel. A flat component treats all children as plain frames with no variant controls.

## Pattern

1. **Create the sub-component set first** (e.g., "Tab Item")
   - Variant properties: `State` (active/inactive/disabled), plus any shared dimensions like `Size`
   - Boolean properties for optional elements (icons, badges, etc.)
   - Each variant has proper fills, text styles, and variable bindings for its state

2. **Create the parent component** (e.g., "Tabs")
   - Uses **instances** of the sub-component, not plain frames
   - Set default states on instances (e.g., first item active, rest inactive)
   - Consider combining with slots (see `rules/slots.md`) for dynamic item count

3. **Both component sets live on the same page**
   - Sub-component positioned above the parent component
   - Both are published as part of the library

## Common examples

| Parent Component | Sub-Component | Sub-Component States |
|---|---|---|
| Tabs | Tab Item | active, inactive, disabled |
| Pagination | Nav Button | enabled, disabled |
| Select / Dropdown | Option Item | default, selected, highlighted |
| Table | Row | default, selected, hover |
| ActionMenu | Menu Item | default, active, disabled |
| NavigationDrawer | Nav Item | default, active, collapsed |
| Breadcrumb | Breadcrumb Item | default, current |

## Code example

```javascript
// 1. Create sub-component variants
const subComps = [];
for (const state of ['active', 'inactive', 'disabled']) {
  const comp = figma.createComponent();
  comp.name = 'State=' + state;
  // ... set up layout, fills, text for this state
  subComps.push(comp);
}
const subSet = figma.combineAsVariants(subComps, figma.currentPage);
subSet.name = 'Tab Item';

// 2. Create parent using instances of sub-component
const parent = figma.createComponent();
const activeVariant = subSet.children.find(c => c.name.includes('State=active'));
const inactiveVariant = subSet.children.find(c => c.name.includes('State=inactive'));

const tab1 = activeVariant.createInstance();
const tab2 = inactiveVariant.createInstance();
const tab3 = inactiveVariant.createInstance();
parent.appendChild(tab1);
parent.appendChild(tab2);
parent.appendChild(tab3);
```

## Relationship to atomic dependencies

This rule covers creating **new** sub-component sets that live alongside the parent (e.g., Tab Item created together with Tabs). For reusing **existing** component sets that were generated separately (e.g., using a Button component set that already exists in the file), see `rules/atomic-dependencies.md`.
