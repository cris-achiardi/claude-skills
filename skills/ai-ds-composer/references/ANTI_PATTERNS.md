# ANTI_PATTERNS.md - What NOT to Do

Anti-patterns are violations of design system philosophy. They exist in component metadata for a reason. Understand them, respect them, and only override with explicit user acknowledgment.

---

## How to Handle Anti-Patterns

When you identify that your suggestion would violate an anti-pattern:

1. **Don't suggest it** (default)
2. **Flag it** - Explain the anti-pattern from metadata
3. **Offer alternative** - Show the recommended approach
4. **Ask for override** - Only if user explicitly wants it anyway (rare)

**Example:**
```
User: "Make a button that goes to my dashboard"

Your response:
"Navigation (going to dashboard) + Button is an anti-pattern.

Anti-pattern: 'Using button for plain navigation'
Reason: 'Buttons indicate actions, not navigation'

Alternative: Use Link component instead.

Unless you specifically want a prominent action button for dashboard access,
I recommend <Link href="/dashboard">Dashboard</Link>"
```

---

## Common Anti-Patterns by Component

### Button Anti-Patterns

#### 1. Button for Navigation
```jsx
// ❌ ANTI-PATTERN
<Button href="/dashboard">Go to Dashboard</Button>

// ✅ CORRECT
<Link href="/dashboard">Go to Dashboard</Link>

// ✅ ACCEPTABLE IF PRIMARY ACTION
// (But even then, consider Link first)
<Button href="/dashboard" variant="primary">
  Access Dashboard
  <Icon name="ExternalLink" size={16} />
</Button>
```

**Reason:** Buttons signal "action" (submit, delete, toggle), not navigation. Links signal "navigation."

**When to override:** If the dashboard access is the primary call-to-action on the page (rare).

---

#### 2. Multiple Primary Buttons
```jsx
// ❌ ANTI-PATTERN
<div style="display: flex; gap: 1rem">
  <Button variant="primary">Save</Button>
  <Button variant="primary">Publish</Button>
  <Button variant="primary">Schedule</Button>
</div>

// ✅ CORRECT
<div style="display: flex; gap: 1rem">
  <Button variant="primary">Save</Button>
  <Button variant="secondary">Publish</Button>
  <Button variant="ghost">Schedule</Button>
</div>
```

**Reason:** Multiple primary buttons confuse visual hierarchy. Only one action should be primary.

**When to override:** Never. This is a design principle.

---

#### 3. Very Long Button Labels
```jsx
// ❌ ANTI-PATTERN
<Button>Click here to submit the form and continue to the next step</Button>

// ✅ CORRECT
<Button>Next Step</Button>

// ✅ IF CONTEXT UNCLEAR
<Button>Continue to Checkout</Button>
```

**Reason:** Buttons should be concise and action-oriented (2-3 words max).

**When to override:** If the action truly needs explanation, use a label outside the button instead.

---

### Heading Anti-Patterns

#### 1. Skipping Heading Levels
```jsx
// ❌ ANTI-PATTERN
<h1>Main Title</h1>
<h3>Subsection</h3>  {/* Skipped h2 */}
<h4>Sub-subsection</h4>

// ✅ CORRECT
<h1>Main Title</h1>
<h2>Section</h2>
<h3>Subsection</h3>
<h4>Sub-subsection</h4>
```

**Reason:** Screen readers and document structure depend on sequential heading levels.

**When to override:** Never. Use `size` prop to override visual appearance if needed:
```jsx
<h3>Subsection</h3>  {/* Semantic h3 */}
<Heading as="h3" size="h2">Looks like h2, structured as h3</Heading>
```

---

#### 2. Multiple h1 on Same Page
```jsx
// ❌ ANTI-PATTERN
<h1>Page Title</h1>
<section>
  <h1>Section Title</h1>  {/* Wrong: Second h1 */}
</section>

// ✅ CORRECT
<h1>Page Title</h1>
<section>
  <h2>Section Title</h2>
</section>
```

**Reason:** One `h1` per page for document hierarchy.

**When to override:** Never. This is accessibility-critical.

---

#### 3. Using Headings for Non-Heading Content
```jsx
// ❌ ANTI-PATTERN
<h2>Important notice</h2>  {/* Just emphasizing, not heading */}

// ✅ CORRECT
<p><strong>Important notice</strong></p>

// OR
<div role="alert" className="notice">Important notice</div>
```

**Reason:** Headings structure content. For emphasis, use `<strong>` or CSS.

**When to override:** Never. Use correct semantic element.

---

### Text Component Anti-Patterns

#### 1. Using Text Component for Body Copy
```jsx
// ❌ ANTI-PATTERN
<Text>This is a paragraph of body text</Text>

// ✅ CORRECT
<p>This is a paragraph of body text</p>
```

**Reason:** Global CSS provides consistent typography for native `<p>`. Text component is unnecessary.

**When to override:** Only if Text provides special styling that `<p>` + class cannot.

---

#### 2. Using Text Component for Inline Text
```jsx
// ❌ ANTI-PATTERN
<div>
  <Text>Some text</Text> and <Text>more text</Text>
</div>

// ✅ CORRECT
<div>
  <p>Some text and more text</p>
</div>

// OR
<div>Some text and <span>more text</span></div>
```

**Reason:** Inline text doesn't need a component. Use native elements + CSS classes.

**When to override:** Only if you need component-level state or interactivity.

---

### Spacer Component Anti-Patterns

#### 1. Using Spacer for Layout Spacing
```jsx
// ❌ ANTI-PATTERN
<div>
  <Button>First</Button>
  <Spacer size="medium" />
  <Button>Second</Button>
</div>

// ✅ CORRECT
<div style="display: flex; gap: var(--spacing-step-2)">
  <Button>First</Button>
  <Button>Second</Button>
</div>
```

**Reason:** CSS `gap` is more flexible and semantic. Spacer creates empty DOM nodes.

**When to override:** Never. Use CSS utilities.

---

#### 2. Using Spacer Instead of Margin
```jsx
// ❌ ANTI-PATTERN
<div>
  <Spacer size="large" />
  <Heading>Title</Heading>
</div>

// ✅ CORRECT
<div>
  <Heading className="mt-large">Title</Heading>
</div>

// OR
<div style="margin-top: var(--spacing-step-3)">
  <Heading>Title</Heading>
</div>
```

**Reason:** Margin is cleaner. Spacer component adds unnecessary elements.

**When to override:** Never. Use CSS.

---

### Container Anti-Patterns

#### 1. Using Container Instead of CSS
```jsx
// ❌ ANTI-PATTERN
<Container maxWidth="1200px" centerContent>
  Content here
</Container>

// ✅ CORRECT
<div style="max-width: 1200px; margin-inline: auto">
  Content here
</div>

// OR WITH CLASS
<div className="container">
  Content here
</div>
```

**Reason:** CSS max-width pattern is simpler and more standard.

**When to override:** If Container provides special responsive behavior or resets documented in metadata.

---

### Avatar Anti-Patterns

#### 1. Using Avatar for Non-User Content
```jsx
// ❌ ANTI-PATTERN
<Avatar src="logo.png" alt="Company logo" />

// ✅ CORRECT
<Image src="logo.png" alt="Company logo" />

// OR NATIVE
<img src="logo.png" alt="Company logo" />
```

**Reason:** Avatar is for user profiles. Logo is content—use Image or `<img>`.

**When to override:** Never. Semantic correctness matters for accessibility.

---

### Badge vs Tag Anti-Patterns

#### 1. Using Badge for Categories
```jsx
// ❌ ANTI-PATTERN
<Badge>React</Badge>
<Badge>Design</Badge>

// ✅ CORRECT
<Tag>React</Tag>
<Tag>Design</Tag>
```

**Reason:** Badge = counts/status. Tag = categories. Different semantic meanings.

**When to override:** Never. They serve different purposes.

---

#### 2. Using Tag for Status
```jsx
// ❌ ANTI-PATTERN
<Tag>In Progress</Tag>

// ✅ CORRECT
<Badge>In Progress</Badge>

// OR WITH VARIANT
<Badge variant="warning">In Progress</Badge>
```

**Reason:** Badge conveys status/count. Tag conveys categorization.

**When to override:** Never. Use correct component.

---

### Link Anti-Patterns

#### 1. Link Without Href
```jsx
// ❌ ANTI-PATTERN
<Link>Click me</Link>

// ✅ CORRECT
<Button variant="ghost" onClick={handleClick}>Click me</Button>

// OR
<Link href="/destination">Click me</Link>
```

**Reason:** Link without `href` isn't accessible. For click actions, use Button.

**When to override:** Never. Always use semantic element.

---

### Icon Anti-Patterns

#### 1. Icon Without Alt Text
```jsx
// ❌ ANTI-PATTERN (if icon is content)
<Icon name="Download" />

// ✅ CORRECT (if icon is content)
<Icon name="Download" aria-label="Download file" />

// ✅ IF DECORATIVE
<Icon name="ArrowRight" aria-hidden="true" />
```

**Reason:** Screen readers need context. If icon communicates meaning, it needs a label.

**When to override:** Never for accessibility. Always provide context.

---

#### 2. Icon Instead of Real Content
```jsx
// ❌ ANTI-PATTERN
<Button>
  <Icon name="Save" />  {/* No text */}
</Button>

// ✅ CORRECT (if icon-only button needed)
<Button aria-label="Save">
  <Icon name="Save" aria-hidden="true" />
</Button>

// ✅ BETTER
<Button>
  Save
  <Icon name="Save" aria-hidden="true" />
</Button>
```

**Reason:** Icon alone doesn't communicate. Add text or aria-label.

**When to override:** Only if space is extremely constrained (and you add aria-label).

---

## Meta Anti-Patterns (How You Use This Skill)

### 1. Ignoring Anti-Pattern Warnings
```jsx
// ❌ YOU DO THIS
User: "Make a button that navigates"
You suggest: <Button href="/dashboard">Dashboard</Button>
// (Violates anti-pattern, not flagged)

// ✅ YOU DO THIS
User: "Make a button that navigates"
You flag: "Anti-pattern detected: Button for navigation. 
          Recommend Link instead. Override? Y/N"
```

**Why:** Anti-patterns exist for reasons. Respect them by default.

---

### 2. Suggesting Without Metadata Justification
```jsx
// ❌ YOU DO THIS
User: "Add a button"
You suggest: <Button variant="primary">Click Me</Button>
// (Why primary? Not justified)

// ✅ YOU DO THIS
User: "Add a button for signup"
You suggest: <Button variant="primary">Sign Up</Button>
// (Variant justified: "selection criteria shows primary 
//  for main call-to-action, signup is main action")
```

**Why:** Without justification, your suggestion is a guess. Always cite metadata.

---

### 3. Composing Without Checking Constraints
```jsx
// ❌ YOU DO THIS
You suggest: <Badge inside Button>Status</Badge>
// (Never checked if Badge can nest in Button)

// ✅ YOU DO THIS
You check: Button.metadata → composition.nestedComponents → ["Icon"]
// Badge NOT in list
// Flag: "Badge can't nest in Button. Consider positioning outside."
```

**Why:** Composition constraints prevent invalid nesting.

---

## General Anti-Pattern Principles

1. **Always respect semantic HTML** - Use elements for their intended purpose
2. **Always check metadata first** - Suggestions must map to documented rules
3. **Always flag anti-patterns** - Don't silently violate design system rules
4. **Always prefer native elements** - Components only when they add value
5. **Always cite your reasoning** - Suggestions trace back to metadata

If you violate these, you're not using the design system—you're working around it.
