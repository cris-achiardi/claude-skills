# COMPOSITION_PATTERNS.md - Combining Components

Guide for composing multiple components into layouts and patterns while respecting hierarchy and metadata rules.

## Core Principle

Components compose bottom-up: atoms combine into molecules, molecules into organisms. Respect this hierarchy—don't force components to nest where they don't belong.

---

## Pattern Categories

### 1. Action Patterns (Button-Based)

#### Single Action
```jsx
<Button variant="primary">Click Me</Button>
```

#### Action Pair (CTA + Alternative)
```jsx
<div style="display: flex; gap: var(--spacing-step-2)">
  <Button variant="primary">Confirm</Button>
  <Button variant="secondary">Cancel</Button>
</div>
```

**Rule:** Primary first (draws attention), secondary second (offers exit).

#### Action Trio (Primary + Secondary + Destructive)
```jsx
<div style="display: flex; gap: var(--spacing-step-2); justify-content: space-between">
  <Button variant="danger" size="sm">Delete</Button>
  <div style="display: flex; gap: var(--spacing-step-1)">
    <Button variant="secondary" size="sm">Cancel</Button>
    <Button variant="primary" size="sm">Save</Button>
  </div>
</div>
```

**Rule:** Destructive on left (warning), primary on right (draws final attention), alternatives in middle.

#### Button with Icon
```jsx
<Button variant="primary">
  Get Started
  <Icon name="ArrowRight" size={16} />
</Button>
```

**Rules:**
- Icon nests inside Button (from `Button.metadata.ts → composition.nestedComponents`)
- Icon placed after text (visual flow left-to-right)
- Icon size matches button text (usually `size={16}` for default buttons)

#### Button with Icon Left
```jsx
<Button variant="primary">
  <Icon name="Download" size={16} />
  Download
</Button>
```

**Use when:** Icon provides visual metaphor that should lead (download icon before text).

---

### 2. Text + Hierarchy Patterns

#### Heading with Subheading
```jsx
<>
  <h1>Main Page Title</h1>
  <p className="text-muted">Brief subtitle or description</p>
</>
```

**Rules:**
- Prefer native `<h1>` over Heading component (per system philosophy)
- Subtitle is `<p>`, not `<h2>` (not part of hierarchy, just supporting text)
- Use class for styling, not Text component

#### Heading with Action Button
```jsx
<div style="display: flex; justify-content: space-between; align-items: baseline">
  <h2>Section Title</h2>
  <Button variant="ghost" size="sm" href="/all-items">See All →</Button>
</div>
```

**Rules:**
- Heading and button align baseline (not vertically centered)
- Button uses `ghost` variant (minimal visual weight)
- Arrow in text signals navigation

#### Heading + Tags
```jsx
<div>
  <h3>Article Title</h3>
  <div style="display: flex; gap: var(--spacing-step-1)">
    <Tag>React</Tag>
    <Tag>Design Systems</Tag>
  </div>
</div>
```

**Rules:**
- Tags below heading, not nested inside
- Tags use flexbox for spacing
- Each tag is separate component

---

### 3. Card Patterns

#### Card with Image + Text
```jsx
<article>
  <Image src="cover.jpg" alt="Article cover" />
  <h3>Article Title</h3>
  <p>Brief excerpt or description</p>
  <Link href="/article">Read More →</Link>
</article>
```

**Composition atoms:**
- Image (no component needed for simple images, use `<img>` unless special handling)
- Heading (use native `<h3>`, not component)
- Text (use native `<p>`, not Text component)
- Link (use native `<a>` or Link component)

**Rules:**
- Image first (visual hierarchy)
- Heading next (what is it?)
- Body text (context)
- Link last (call to action)
- No wrapper components unless necessary

#### Skill Card (Project-Specific Example)
```jsx
<article className="skill-card">
  <Image src="icon.svg" alt="Skill icon" />
  <h3>Skill Name</h3>
  <p>Brief description of skill</p>
  <div className="tags">
    <Tag>Label</Tag>
    <Tag>Label</Tag>
  </div>
  <time>Updated date</time>
</article>
```

**Pattern from molecules metadata:** Card layout with optional metadata.

#### Card with Badge (Status Indicator)
```jsx
<article>
  <div style="display: flex; justify-content: space-between; align-items: start">
    <h3>Item Title</h3>
    <Badge>Status</Badge>
  </div>
  <p>Description</p>
</article>
```

**Rules:**
- Badge in top-right (status indicator position)
- Heading left-aligned, Badge right-aligned
- Badge provides immediate status context

---

### 4. Form Patterns

#### Simple Form Field
```jsx
<label>
  <span>Field Label</span>
  <input type="text" placeholder="Enter value" />
</label>
```

**Rules:**
- Use native `<input>` or component if available
- Label wraps input (implicit association)
- Placeholder guides user

#### Form Field with Helper Text
```jsx
<div>
  <label htmlFor="email">Email Address</label>
  <input id="email" type="email" />
  <small>We'll never share your email</small>
</div>
```

**Rules:**
- `id` and `htmlFor` for explicit label association
- Helper text below input, `<small>` or muted class
- Semantic structure for accessibility

#### Form with Submit Button
```jsx
<form onSubmit={handleSubmit}>
  <div>
    <label htmlFor="name">Name</label>
    <input id="name" type="text" />
  </div>
  <div>
    <label htmlFor="email">Email</label>
    <input id="email" type="email" />
  </div>
  <Button type="submit" variant="primary">Send</Button>
</form>
```

**Rules:**
- Form wraps fields and submit button
- Button has `type="submit"` (from Button metadata)
- Fields grouped with consistent spacing

---

### 5. List Patterns

#### Simple List with Links
```jsx
<ul>
  <li><Link href="/item-1">Item 1</Link></li>
  <li><Link href="/item-2">Item 2</Link></li>
  <li><Link href="/item-3">Item 3</Link></li>
</ul>
```

**Rules:**
- Use semantic `<ul>` for unordered lists
- Each item is `<li>`, not standalone Link
- Link inside each list item

#### List with Icons
```jsx
<ul style="list-style: none; padding: 0">
  {items.map(item => (
    <li key={item.id} style="display: flex; gap: var(--spacing-step-2); align-items: start">
      <Icon name={item.icon} size={20} className="flex-shrink-0" />
      <div>
        <h4>{item.title}</h4>
        <p>{item.description}</p>
      </div>
    </li>
  ))}
</ul>
```

**Rules:**
- Remove default `list-style`
- Icon and text flex layout
- Icon gets `flex-shrink-0` (doesn't resize)
- Content flows naturally

#### Nested List (Hierarchy)
```jsx
<ul>
  <li>
    Parent Item
    <ul style="margin-left: var(--spacing-step-3)">
      <li>Child Item 1</li>
      <li>Child Item 2</li>
    </ul>
  </li>
</ul>
```

**Rules:**
- Nesting shows hierarchy
- Child `<ul>` indented via margin (from CSS metadata)
- No components needed for hierarchy

---

### 6. Grid / Layout Patterns

#### Responsive Grid
```jsx
<div style="
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-step-3);
">
  {items.map(item => (
    <Card key={item.id}>...</Card>
  ))}
</div>
```

**Rules:**
- `auto-fit` for responsive
- `minmax(300px, 1fr)` for minimum column width
- `gap` from CSS metadata conventions
- No Spacer component needed

#### Flex Layout (Side by Side)
```jsx
<div style="
  display: flex;
  gap: var(--spacing-step-2);
  align-items: center;
">
  <Image src="..." alt="..." style="flex-shrink: 0" />
  <div>
    <h3>Title</h3>
    <p>Description</p>
  </div>
</div>
```

**Rules:**
- Image `flex-shrink: 0` (maintains width)
- Content flows in remaining space
- Gap for spacing (not margin)

#### Three-Column to One-Column
```jsx
<div style="
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-step-3);
">
  {/* Cards automatically reflow */}
</div>
```

**No media queries needed** with `auto-fit` + `minmax`.

---

### 7. Navigation Patterns

#### Horizontal Navigation
```jsx
<nav>
  <ul style="display: flex; gap: var(--spacing-step-2); list-style: none">
    <li><Link href="/">Home</Link></li>
    <li><Link href="/about">About</Link></li>
    <li><Link href="/work">Work</Link></li>
    <li><Link href="/contact">Contact</Link></li>
  </ul>
</nav>
```

**Rules:**
- `<nav>` semantic element
- Links in flexbox
- Gap for spacing (not margin)
- No Button component (navigation intent)

#### Breadcrumb Navigation
```jsx
<nav aria-label="Breadcrumb">
  <ol style="display: flex; gap: var(--spacing-step-1); list-style: none">
    <li><Link href="/">Home</Link></li>
    <li> / </li>
    <li><Link href="/category">Category</Link></li>
    <li> / </li>
    <li aria-current="page">Current Page</li>
  </ol>
</nav>
```

**Rules:**
- `<ol>` for ordered breadcrumb
- Separators between items (` / `)
- Last item has `aria-current="page"` (not a link)

---

## Composition Rules

### Respect Metadata Constraints

Before composing, check:

1. **Can this component accept children?**
   - Read `component.metadata.composition.slots`
   - If `required: true` in slot, you must provide it
   - If component doesn't support children, don't nest

2. **What components can nest inside?**
   - Read `component.metadata.composition.nestedComponents`
   - Only nest these; don't invent new nesting

3. **What are common partners?**
   - Read `component.metadata.composition.commonPartners`
   - These are tested compositions

### Spacing Conventions

**From CSS metadata:**
```
Always use: var(--spacing-step-N)
Never use: hard px values (10px, 20px, etc.)
```

**Gap hierarchy:**
- Tight: `--spacing-step-1` (small inner gaps)
- Normal: `--spacing-step-2` (button groups, list items)
- Loose: `--spacing-step-3` (card grids, section spacing)

### Semantic HTML First

**Prefer:**
```jsx
<ul><li>Item</li></ul>  // Native list
<h2>Title</h2>          // Native heading
<a href="/">Link</a>    // Native link
<img src="..." />       // Native image
```

**Avoid:**
```jsx
<div><div>Item</div></div>  // No semantics
<Text as="h2">Title</Text>  // Unnecessary component
<Button href="/">Link</Button>  // Anti-pattern
<Picture src="..." />       // Component when not needed
```

### Visual Hierarchy Through Composition, Not Components

**Right:**
```jsx
<h1>Main Title</h1>
<p className="text-muted">Subtitle</p>
```

**Wrong:**
```jsx
<Heading>Main Title</Heading>
<Heading size="small">Subtitle</Heading>
```

---

## When NOT to Compose

Some things shouldn't be composed:

- **CSS-only spacing/layout** → Use CSS utilities directly
- **Simple text hierarchy** → Use native HTML + classes
- **Pure visual styling** → CSS, not components
- **Semantic structure** → Native HTML, not layout components

Ask: "Does this need component logic or just CSS?" If CSS, don't compose components.

---

## Testing Your Composition

Before suggesting a composition, verify:

1. ✅ Each component exists in metadata
2. ✅ Nesting rules respected (from `composition` field)
3. ✅ No anti-patterns violated
4. ✅ Semantic HTML used where appropriate
5. ✅ Spacing follows CSS conventions
6. ✅ Each component choice is justified in metadata

If you can't check all five, ask for clarification before suggesting.
