# METADATA_STRUCTURE.md - Understanding Design System Metadata

This guide explains how to read and interpret metadata at each level of the design system hierarchy.

## Top-Level System Metadata

Located at project root or `src/design-system.metadata.ts`. Captures strategic decisions about the entire design system.

### Key Fields

```typescript
export const DesignSystemMetadata = {
  projectStack: {
    framework: "Astro" | "Next.js" | "React" | etc.,
    componentLanguages: ["Astro", "React"], // What you can generate
    styling: "Modular CSS" | "Tailwind" | "CSS-in-JS",
    icons: "Lucide" | "Material Icons" | custom,
  },
  
  philosophies: {
    // These are hard constraints—not guidelines
    preferNative: "Use native HTML when global CSS suffices",
    minimizeComponents: "Components for patterns, not every element",
    cssFirst: "CSS utilities for layout/spacing",
    semanticHTML: "Semantic HTML > presentational",
  },
  
  indexHierarchy: {
    // Shows where to find what
    atoms: "Base primitives",
    molecules: "Composed patterns",
    organisms: "Full sections",
  },
  
  whenToFlag: [ /* Gap conditions */ ]
}
```

**How to use:** Read this first in a conversation. Cache these philosophies—they inform all component decisions.

**Red flags to check:**
- `preferNative: true` → Don't suggest components for simple text/headings
- `cssFirst: true` → Suggest CSS utilities before components for layout
- `minimizeComponents: true` → Justify every component choice

---

## Layer Metadata (Atoms, Molecules, Organisms)

Located at `src/components/{atoms,molecules,organisms}/index.metadata.ts`. Maps all components at that level and provides selection guidance.

### Structure

```typescript
export const AtomsMetadata = {
  // Complete catalog of all components
  AtomsMap: {
    Button: ButtonMetadata,
    Heading: HeadingMetadata,
    Icon: IconMetadata,
    // ... all atoms
  },
  
  // Priority guidance for AI
  AtomsPriority: {
    high: ['Button', 'Link', 'Heading', 'Icon'],
    medium: ['Text', 'Badge', 'Tag'],
    low: ['Container', 'Spacer'], // Less preferred
  },
  
  // Decision tree by use case
  SelectionGuide: {
    actions: {
      'user-action': 'Button',
      'navigation': 'Link',
      'copy-text': 'CopyButton',
    },
    typography: {
      'headings': 'Heading (or native <h1>-<h6>)',
      'body-text': 'Native <p> (avoid Text component)',
    },
    visual: {
      'icons': 'Icon (React - PREFERRED)',
      'user-photos': 'Avatar',
    },
  },
  
  // System rules for this layer
  DesignSystemPrinciples: {
    preferNativeHTML: [ /* list of when */ ],
    preferCSS: [ /* list of when */ ],
    modernPatterns: [ /* preferred approaches */ ],
  }
}
```

**How to use:**
1. Check `AtomsPriority` to understand which components are main vs optional
2. Scan `SelectionGuide` for your use case
3. Use `DesignSystemPrinciples` to filter suggestions (e.g., "avoid Text component")

**At molecules level:** Look for `CommonCompositions` that show expected pairings:
```typescript
CommonCompositions: {
  cardWithImage: ["Image", "Heading", "Text", "Link"],
  formField: ["Label", "Input", "HelperText"],
}
```

---

## Component Metadata

Located at `src/components/{layer}/{ComponentName}/{ComponentName}.metadata.ts`. Detailed spec for a single component.

### Essential Fields for Decisions

#### Props
```typescript
props: {
  variant: {
    type: "'primary' | 'secondary' | 'ghost' | 'danger'",
    default: "'primary'",
    required: false,
    description: "Visual style variant"
  },
  size: {
    type: "'sm' | 'md' | 'lg'",
    default: "'md'",
    required: false,
  },
  // ... other props
}
```

**How to use:** This is your source of truth for what props exist and their valid values. Never invent props not listed here.

#### Variants
```typescript
variants: {
  variant: {
    options: ["primary", "secondary", "ghost", "danger"],
    default: "primary",
    purpose: {
      primary: "Main call-to-action, high visual prominence",
      secondary: "Alternative or cancel actions",
      ghost: "Minimal visual weight, subtle actions",
      danger: "Destructive actions requiring attention"
    }
  }
}
```

**How to use:** Match user intent to purpose. If user wants "a prominent action," `variant="primary"` matches the purpose. If user wants "subtle," use `ghost`.

#### Selection Criteria
```typescript
selectionCriteria: {
  usePrimary: "Main action user should take on the page/section",
  useSecondary: "Alternative actions, cancel buttons",
  useGhost: "Tertiary actions, minimal visual weight",
  useDanger: "Delete, remove, destructive actions",
  withIcons: "Add Icon component as child for enhanced communication",
  asLink: "Provide href prop to render as anchor tag for navigation"
}
```

**How to use:** This is the decision rule. If user wants the "main action," select `usePrimary` and use `variant="primary"`. These rules precede examples and intuition.

#### Anti-Patterns
```typescript
antiPatterns: [
  {
    scenario: "Using button for plain navigation",
    reason: "Buttons indicate actions, not navigation",
    alternative: "Use Link component for navigation"
  }
]
```

**How to use:** Check anti-patterns before suggesting a component. If your suggestion matches an anti-pattern scenario, don't suggest it unless user explicitly overrides.

#### Composition
```typescript
composition: {
  slots: {
    default: {
      description: "Button text and optional icons",
      accepts: ["text", "Icon component"],
      required: true
    }
  },
  nestedComponents: ["Icon"],
  commonPartners: ["Icon", "form elements"],
}
```

**How to use:** This shows what can nest inside the component. Button accepts Icon—so you can compose Button + Icon. It doesn't accept Badge—so don't nest Badge inside Button.

#### AI-Specific Hints
```typescript
aiHints: {
  priority: "high",
  keywords: ["button", "cta", "submit", "action"],
  context: "Use for any user action or form submission",
  selectionCriteria: { /* repeated for AI */ },
}
```

**How to use:** These are secondary. The structured fields (props, variants, composition) are primary. `aiHints` are for exploration only.

---

## CSS Metadata

Located at `src/styles/index.metadata.ts` (or similar). Documents how styling works in the project.

### Structure

```typescript
export const CSSMetadata = {
  architecture: "modular - global, tokens, utilities, layout, effects, reset",
  
  approachForAI: {
    preferNativeHTML: true,
    preferUtilities: true,
    whenToUseComponent: "for complex interactive patterns only",
  },
  
  structure: {
    global: "base styles, resets, defaults",
    tokens: "CSS variables (colors, spacing, typography)",
    utilities: "utility classes (.flex, .grid, .gap-4, etc.)",
    layout: "layout patterns - flexbox, grid, container queries",
    effects: "animations, transitions, shadows",
  },
  
  conventions: {
    spacing: "use var(--spacing-step-3) not hard values",
    layout: "CSS Grid for complex, flexbox for simple",
    responsive: "mobile-first media queries",
  },
  
  examples: {
    flexCenter: "display: flex; align-items: center; justify-content: center;",
    gridResponsive: "grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));",
  }
}
```

**How to use:** When user asks for layout/spacing, suggest CSS patterns before suggesting components. Check `conventions` for project-specific patterns.

---

## Reading Metadata in Context

### Pattern 1: User says "I need a button"

1. Read: `atoms/index.metadata.ts` → `SelectionGuide.actions['user-action']` → "Button"
2. Read: `Button.metadata.ts` → `selectionCriteria` → match user intent to criterion
3. Read: `Button.metadata.ts` → `variants.variant.purpose` → pick variant
4. Check: `Button.metadata.ts` → `antiPatterns` → ensure no violations
5. Output: Suggested Button with variant, citing selection criterion

### Pattern 2: User says "Add spacing between items"

1. Read: `design-system.metadata.ts` → philosophies → "cssFirst"
2. Check: `styles/index.metadata.ts` → `structure.utilities` → CSS approach exists
3. Read: `styles/index.metadata.ts` → `conventions.spacing` → suggested pattern
4. Output: CSS utility suggestion (gap, margin, etc.), not a component

### Pattern 3: User says "I need a card"

1. Read: `molecules/index.metadata.ts` → `CommonCompositions.cardWithImage` → ["Image", "Heading", "Text", "Link"]
2. Read: Each component's metadata for their variants
3. Check: Do anti-patterns exist for this composition?
4. Output: Composition of Image + Heading + Text + Link with specific variants

---

## When Metadata Is Incomplete or Conflicting

If metadata doesn't clearly answer your question:

1. **Check the hierarchy** - A lower level (component) might clarify a higher level (layer)
2. **Lean on project philosophy** - If unclear, apply the system's stated philosophy
3. **Ask the user** - "The metadata doesn't specify X. Does your project prefer Y or Z?"
4. **Don't invent** - Never guess at an undocumented prop or pattern

Example: If Button.metadata.ts doesn't specify a `loading` prop but Button.astro supports it:
- Ask: "Does the design system document a loading state for Button? I don't see it in metadata."
- Don't assume: "I'll use loading prop anyway"

---

## Metadata Red Flags

| Flag | Meaning | Action |
|------|---------|--------|
| `antiPattern` found | Your suggestion violates design system | Don't suggest it (or flag hard override) |
| Component marked `low` priority | Discouraged usage | Prefer alternatives listed in layer index |
| `preferNativeHTML: true` | Use native elements | Don't suggest component for this use case |
| `marked as "Legacy"` | Deprecated | Don't use; prefer the suggested alternative |
| No `selectionCriteria` match | Your intent doesn't fit this component | It's the wrong component; go back and reconsider |

---

## Metadata Caching Strategy

In a conversation, read metadata once and cache:
- Top-level system metadata (read once)
- Layer index for the category you're working in (read once per layer)
- Component metadata (read as needed)

This minimizes re-reading while keeping suggestions fresh to the user's latest requirement.
