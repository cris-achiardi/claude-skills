# Figma Variables Quick Reference

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
```json
{
  "variableName": {
    "$type": "number",
    "$value": 16
  }
}
```

### String Variables
```json
{
  "variableName": {
    "$type": "string",
    "$value": "Inter"
  }
}
```

### Boolean Variables
```json
{
  "variableName": {
    "$type": "boolean",
    "$value": true
  }
}
```

### Spacing Variables
```json
{
  "variableName": {
    "$type": "spacing",
    "$value": 8
  }
}
```

### Border Radius Variables
```json
{
  "variableName": {
    "$type": "borderRadius",
    "$value": 4
  }
}
```

### Font Size Variables
```json
{
  "variableName": {
    "$type": "fontSize",
    "$value": 16
  }
}
```

### Font Weight Variables
```json
{
  "variableName": {
    "$type": "fontWeight",
    "$value": 400
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
