# Figma Variables Quick Reference

## CRITICAL: Updating Existing Collections

When adding to or updating an existing JSON file:
1. **Read the existing file first** - Load current structure
2. **Preserve exact naming** - Collection, category, subcategory, variable names must match EXACTLY
3. **Figma's behavior**: Same name = updates, different name = creates new
4. **Keep hierarchy** - Maintain the same nesting structure

Example:
- Existing: `{"Spacing": {"space": {"sm": 8}}}`
- Adding: `{"Spacing": {"space": {"md": 16}}}` ✅ Correct
- Wrong: `{"Spacing": {"spacing": {"md": 16}}}` ❌ Creates duplicate

## CRITICAL: Only 4 Variable Types

**Figma's variables API only supports 4 types:**
- `color` - for colors
- `number` - for spacing, radius, font sizes, weights, dimensions
- `string` - for font families, text values
- `boolean` - for true/false values

**DO NOT use**: `spacing`, `borderRadius`, `fontSize`, `fontWeight` - these are INVALID and will cause import errors.

**Use semantic naming instead**: `spacing.sm`, `fontSize.body`, `radius.lg` with type `number`.

## CRITICAL: Pixel Values Only

Figma only accepts pixel values. Always convert relative units:

### Common Unit Conversions (base: 16px)
- `1rem` → `16`
- `2rem` → `32`
- `0.875rem` → `14`
- `1.5rem` → `24`
- `1em` → `16` (context-dependent)
- `1pt` → `1.333`
- `1pc` → `16` (1 pica = 12 points)

### Examples
- Input: `font-size: 1.5rem` → `"$value": 24`
- Input: `spacing: 2rem` → `"$value": 32`
- Input: `line-height: 1.25em` → `"$value": 20`

## Variable Types Reference

**Figma supports only 4 core variable types:**

### Color Variables
```json
{
  "variableName": {
    "$type": "color",
    "$value": "#ffffff"  // or {r: 1, g: 1, b: 1} or "rgba(255,255,255,1)"
  }
}
```

### Number Variables
Use for: spacing, border radius, font size, font weight, dimensions, etc.

```json
{
  "spacing-sm": {
    "$type": "number",
    "$value": 8
  },
  "radius-md": {
    "$type": "number",
    "$value": 4
  },
  "fontSize-body": {
    "$type": "number",
    "$value": 16
  },
  "fontWeight-bold": {
    "$type": "number",
    "$value": 700
  }
}
```

### String Variables
Use for: font families, text content, identifiers, etc.

```json
{
  "fontFamily-sans": {
    "$type": "string",
    "$value": "Inter"
  }
}
```

### Boolean Variables
```json
{
  "featureEnabled": {
    "$type": "boolean",
    "$value": true
  }
}
```

## Multi-Mode Structure

```json
{
  "Collection Name": {
    "variableName": {
      "$type": "color",
      "$value": {
        "Light": "#ffffff",
        "Dark": "#000000"
      }
    }
  }
}
```

## Variable References (Aliases)

Reference other variables using the syntax: `{CollectionName.category.variableName}`

```json
{
  "Semantic Colors": {
    "text": {
      "primary": {
        "$type": "color",
        "$value": {
          "Light": "{Primitives.gray.900}",
          "Dark": "{Primitives.gray.100}"
        }
      }
    }
  }
}
```

## Code Syntax Extensions

### Single Platform
```json
{
  "variableName": {
    "$type": "color",
    "$value": "#ffffff",
    "$extensions": {
      "codeSyntax": {
        "WEB": "variableName"
      }
    }
  }
}
```

### Multiple Platforms
```json
{
  "variableName": {
    "$type": "color",
    "$value": "#ffffff",
    "$extensions": {
      "codeSyntax": {
        "WEB": "variableName",
        "iOS": "variable_name",
        "ANDROID": "variable_name"
      }
    }
  }
}
```

## JSON Formatting for Readability

### Property Order
1. `$type` - Type first
2. `$value` - Value second
3. `$description` - Description (if present)
4. `$extensions` - Extensions last

### Variable Ordering
- **Size-based**: xs → sm → md → lg → xl
- **Numeric**: 0 → 1 → 2 → 3 → 100 → 200...
- **Semantic**: primary → secondary → tertiary
- **State**: default → hover → active → pressed → disabled
- **Alphabetical**: Use as fallback

### Category Ordering
1. Primitives/base values (gray, blue, red)
2. Semantic/functional (text, background, border)
3. Component-specific (button, card, modal)

### Formatting
- 2-space indentation
- Each property on its own line
- No trailing commas
- Consistent spacing

## Naming Convention Examples

Given variable path: `background.interactive.primary`

- **camelCase**: `backgroundInteractivePrimary`
- **snake_case**: `background_interactive_primary`
- **kebab-case**: `background-interactive-primary`
- **PascalCase**: `BackgroundInteractivePrimary`

## Common Collection Structures

### Flat Structure
```json
{
  "Collection": {
    "variable1": {...},
    "variable2": {...}
  }
}
```

### Categorized Structure
```json
{
  "Collection": {
    "category1": {
      "variable1": {...},
      "variable2": {...}
    },
    "category2": {
      "variable3": {...}
    }
  }
}
```

### Deep Hierarchy
```json
{
  "Collection": {
    "category": {
      "subcategory": {
        "item": {
          "variable": {...}
        }
      }
    }
  }
}
```
