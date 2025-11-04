# COMPONENT_SELECTION.md - Decision Examples

Real-world examples of applying the component selection algorithm to different user intents.

## Example 1: Vague Request → Clarification → Selection

**User Says:** "Add a button like on the homepage"

### Step 1: Parse Intent (Clarify)
Too vague. You need:
- What action does this button trigger?
- Where is it positioned (hero, card, form)?
- Is it primary or secondary?
- Any specific styling?

**Follow-up:** "I see the homepage has several buttons. Are you referring to the 'Get Started' button in the hero, or something else? What action should this new button trigger?"

### Step 2: After Clarification
"It should trigger signup, positioned in a form, same style as the hero button"

**Clear intent:** Primary call-to-action button for form submission in a hero-like context.

### Step 3: Consult Metadata

**Read:** `atoms/index.metadata.ts`
```
SelectionGuide.actions['user-action'] → Button
```

**Read:** `Button.metadata.ts`
```
selectionCriteria: {
  usePrimary: "Main action user should take on the page/section"
}

variants: {
  variant: {
    primary: "Main call-to-action, high visual prominence"
  },
  size: {
    lg: "Prominent CTAs, hero sections"
  }
}
```

**Check:** `antiPatterns` → No violations for this use case

### Step 4: Suggest
```typescript
<Button 
  type="submit" 
  variant="primary" 
  size="lg"
>
  Sign Up
  <Icon name="ArrowRight" size={16} />
</Button>
```

**Why:** Selection criterion "Main action user should take" matches signup form. Variant `primary` and size `lg` align with hero prominence. `type="submit"` follows form composition pattern.

---

## Example 2: CSS vs Component Decision

**User Says:** "Need spacing between these items in a grid"

### Step 1: Check System Philosophy

**Read:** `design-system.metadata.ts`
```
philosophies: {
  cssFirst: "CSS utilities for layout/spacing"
}
```

### Step 2: Check CSS Metadata

**Read:** `styles/index.metadata.ts`
```
conventions: {
  spacing: "use var(--spacing-step-3) not hard values",
  layout: "CSS Grid for complex, flexbox for simple"
}
```

### Step 3: Suggest CSS, Not Component

**Suggest:**
```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-step-3);
}
```

**Why:** Philosophy says "CSS first." No component needed here. Spacer component exists but is marked `low` priority in atoms index. CSS is the right tool.

---

## Example 3: Composition Pattern From Metadata

**User Says:** "Create a blog post card"

### Step 1: Look for Existing Pattern

**Read:** `molecules/index.metadata.ts`
```
CommonCompositions: {
  cardWithImage: ["Image", "Heading", "Text", "Link"]
}
```

Great! Pattern already exists.

### Step 2: Map Components to Their Metadata

**For each component in the pattern:**

**Image:**
- Read: `Image.metadata.ts`
- Variant: default (no special variants needed)
- Props: `src`, `alt`, `width`, `height`

**Heading:**
- Read: `Heading.metadata.ts`
- Philosophy says: "Prefer native <h3> when possible, use component for size override if needed"
- Suggest: Native `<h3>` for semantic HTML unless special size needed

**Text:**
- Read: `Text.metadata.ts`
- Philosophy says: "Avoid Text component, use native <p>"
- Suggest: Native `<p>` instead

**Link:**
- Read: `Link.metadata.ts` or use Link variant of Button
- This is for "Read More" → should use Button with `variant="ghost"` or Link component
- Check: Metadata shows Link vs Button preference

### Step 3: Compose

**Suggested structure:**
```tsx
<article>
  <Image src="..." alt="post cover" />
  <h3>Post Title</h3>
  <p>Brief excerpt...</p>
  <time>Published date</time>
  <Link href="/post-slug">Read Article</Link>
</article>
```

**Why:** Respects philosophy of preferring native HTML. Only uses components where they add value (Image for lazy loading, Link for navigation). No unnecessary wrapper components.

---

## Example 4: Anti-Pattern Detection

**User Says:** "Make a button that navigates to the dashboard"

### Step 1: Recognize the Intent
"Navigation" + "button" = potential anti-pattern

### Step 2: Check Metadata

**Read:** `Button.metadata.ts`
```
antiPatterns: [
  {
    scenario: "Using button for plain navigation",
    reason: "Buttons indicate actions, not navigation",
    alternative: "Use Link component for navigation"
  }
]
```

### Step 3: Flag and Redirect

**Output:**
> "You want navigation to the dashboard. However, Button's anti-pattern says: 'Using button for plain navigation' because buttons indicate actions, not navigation.
>
> **Instead, use Link component:**
> ```jsx
> <Link href="/dashboard">Dashboard</Link>
> ```
>
> If the dashboard link is the main CTA (primary action), you could use Button with `href`:
> ```jsx
> <Button href="/dashboard" variant="primary">Go to Dashboard</Button>
> ```
>
> Which is your use case—navigation or primary action?"

**Why:** Metadata explicitly flags this scenario. Respect the anti-pattern; help the user understand it.

---

## Example 5: Gap Identification (No Solution Exists)

**User Says:** "I need a multi-level dropdown menu with keyboard navigation"

### Step 1: Search Metadata

**Read:** `atoms/index.metadata.ts` → No Dropdown
**Read:** `molecules/index.metadata.ts` → No Menu
**Read:** `organisms/index.metadata.ts` → No Navigation menu

### Step 2: Identify the Gap

Gap exists: No existing component for multi-level dropdown.

### Step 3: Don't Auto-Generate, Flag It

**Output:**
> "Your requirement (multi-level dropdown menu with keyboard nav) doesn't exist in the design system. You have a few options:
>
> **Option A: Workaround with existing components**
> - Compose a custom solution using Button + hidden overlay
> - Trade-off: Limited nesting, manual keyboard handling
>
> **Option B: Create new Menu component**
> - Requires new component development
> - Trade-off: More work upfront, but reusable going forward
>
> Which approach works for your timeline and requirements?"

**Why:** You identified the gap but didn't invent a solution. Human decides next step.

---

## Example 6: Project-Specific Decision

**Scenario:** Two similar projects with different philosophies

### Project A: React SPA (Next.js)
**Philosophy:** "Use components for everything interactive"

**For "add heading":**
- Suggest: `<Heading size="h1">Title</Heading>`
- Reason: Component-first approach

### Project B: Astro SSG
**Philosophy:** "Prefer native HTML + CSS"

**For "add heading":**
- Suggest: `<h1 class="text-xl font-semibold">Title</h1>`
- Reason: Native HTML respected

**Lesson:** The same request gets different answers based on top-level system metadata. Read system philosophy first.

---

## Example 7: Variant Selection Logic

**User Says:** "I need three buttons in a card—action, alternative, and delete"

### Step 1: Map to Variants

**Read:** `Button.metadata.ts` → `variants.variant.purpose`

- Action (main) → `variant="primary"`
- Alternative (secondary) → `variant="secondary"`
- Delete (destructive) → `variant="danger"`

### Step 2: Suggest with Size Context

**Card context:** Smaller space, so use `size="sm"` instead of default `md`

### Step 3: Output

```jsx
<div style="display: flex; gap: var(--spacing-step-2)">
  <Button variant="primary" size="sm">Save</Button>
  <Button variant="secondary" size="sm">Cancel</Button>
  <Button variant="danger" size="sm">Delete</Button>
</div>
```

**Why:** Variants matched to intent. Size adjusted for context. Spacing from CSS metadata.

---

## Example 8: Icon Composition

**User Says:** "Add a download button"

### Step 1: Check Button Composition

**Read:** `Button.metadata.ts`
```
composition: {
  nestedComponents: ["Icon"],
  commonPartners: ["Icon"]
}
```

Icons can nest in Button.

### Step 2: Check Icon Metadata

**Read:** `Icon.metadata.ts` → What icon libraries available? (Lucide, etc.)

### Step 3: Check Project Stack

**Read:** `design-system.metadata.ts`
```
icons: "Lucide React"
```

### Step 4: Suggest

```jsx
<Button variant="primary">
  Download
  <Icon name="Download" size={16} />
</Button>
```

**Why:** Button composition allows Icon. Lucide is available. Icon placed after text (following metadata pattern).

---

## Decision Tree Reference

Use this quick lookup when unsure:

| User Intent | Check Metadata | Common Decision |
|---|---|---|
| "I need to do X" (action) | Button.selectionCriteria | Pick variant based on action hierarchy |
| "Navigate to Y" (nav) | Link or Button.antiPatterns | Prefer Link, warn against Button |
| "Space these items" (layout) | CSS metadata + philosophy | Suggest utilities, not Spacer |
| "Add heading" | Heading vs native | Prefer native if possible |
| "Show a list of X" | Layer index → atoms/molecules | Usually compose existing atoms |
| "I need [component name] like Z" | Search layer index → component metadata | Find similar usage in codebase for reference |
| "This doesn't exist" | Full metadata search → gap check | Flag gap, don't auto-generate |

---

## Debugging Your Selection

If you're uncertain about a suggestion, ask:

1. **Is this in metadata?** If not, you're guessing—ask the user
2. **Does metadata have an anti-pattern?** If yes, don't suggest it
3. **Does the selection criterion match the intent?** If no, try another component
4. **Am I respecting system philosophy?** If no, adjust
5. **Can I cite where this came from in metadata?** If no, rethink

Your suggestion should always trace back to metadata—not intuition.
