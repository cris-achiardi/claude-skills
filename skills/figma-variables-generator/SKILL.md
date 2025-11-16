---
name: figma-variables-generator
description: Generate JSON files for creating Figma variable collections from text descriptions or design token data. Use when designers need to create or convert design tokens (colors, spacing, typography, etc.) into Figma variables format. Supports multiple modes (Light/Dark), code syntax definitions, variable references/aliases, and hierarchical organization. Triggers include requests to "create Figma variables", "generate variables JSON", "convert design tokens", or working with design system tokens.
---

# Figma Variables Generator

Generate properly formatted JSON files for creating Figma variable collections from text descriptions, existing design token data, or images showing design systems.

## Core Capabilities

This skill helps designers create Figma variable collections by generating the JSON format required by Figma variable import/export plugins. The output can be directly imported into Figma using plugins like "Variables Import Export" or similar tools.

### Supported Variable Types

- **Color** (`$type: "color"`) - RGB hex values or variable references
- **Number** (`$type: "number"`) - Numeric values for sizes, spacing
- **String** (`$type: "string"`) - Text values for font families, etc.
- **Boolean** (`$type: "boolean"`) - True/false values
- **Spacing** (`$type: "spacing"`) - Spacing scale values
- **Border Radius** (`$type: "borderRadius"`) - Corner radius values
- **Font Size** (`$type: "fontSize"`) - Typography size values
- **Font Weight** (`$type: "fontWeight"`) - Typography weight values

### Key Features

1. **Multiple Modes**: Support for different modes (e.g., Light/Dark themes)
2. **Variable References**: Use `{collection.subcategory.variableName}` syntax to reference other variables
3. **Code Syntax**: Optional platform-specific naming conventions (WEB, iOS, ANDROID)
4. **Hierarchical Organization**: Group variables into collections, categories, and subcategories
5. **Flexible Input**: Accept design tokens from text, structured data, or images

## Workflow

### Step 1: Gather Information

Before generating the JSON, ask the user:

1. **Collection Name**: What should the variable collection be named?
2. **Variable Content**: What variables need to be created? (Accept text descriptions, existing JSON, or analyze uploaded images)
3. **Modes**: Does this collection need multiple modes (e.g., Light/Dark)? What should they be named?
4. **Code Syntax**: Should code syntax be included? If yes:
   - Which platforms? (WEB, iOS, ANDROID)
   - What naming convention? (camelCase, snake_case, kebab-case, PascalCase)
5. **Organization**: How should variables be organized? (category/subcategory structure)

### Step 2: Generate JSON Structure

Create a JSON file following this structure:

```json
{
  "Collection Name": {
    "category": {
      "subcategory": {
        "variableName": {
          "$type": "color",
          "$value": {
            "Light": "#ffffff",
            "Dark": "#000000"
          },
          "$extensions": {
            "codeSyntax": {
              "WEB": "categorySubcategoryVariableName"
            }
          }
        }
      }
    }
  }
}
```

### Step 3: Apply Naming Conventions

When code syntax is requested:

**camelCase** (default for WEB):
- `foreground.base` → `foregroundBase`
- `background.interactive.primary` → `backgroundInteractivePrimary`

**snake_case** (common for Python, some backend systems):
- `foreground.base` → `foreground_base`
- `background.interactive.primary` → `background_interactive_primary`

**kebab-case** (common for CSS):
- `foreground.base` → `foreground-base`
- `background.interactive.primary` → `background-interactive-primary`

**PascalCase** (common for some component systems):
- `foreground.base` → `ForegroundBase`
- `background.interactive.primary` → `BackgroundInteractivePrimary`

### Step 4: Convert Units to Pixels

**CRITICAL**: Figma only works with pixel values. Always convert relative units to pixels:

**Common Conversions** (assuming 16px base font size):
- `1rem` → `16` (pixels)
- `2rem` → `32` (pixels)
- `0.875rem` → `14` (pixels)
- `1em` → `16` (pixels, context-dependent)
- `1.5em` → `24` (pixels, context-dependent)

**Percentage/Viewport Units** (ask user for context if needed):
- `100%` → ask for parent container size
- `50vw` → ask for viewport width or use common breakpoint
- `10vh` → ask for viewport height or use common breakpoint

**Other Units**:
- `1pt` → `1.333` (pixels)
- `1pc` → `16` (pixels, 1 pica = 12 points)

When encountering unit-based values, automatically convert to pixels without units in the JSON output.

**Example**:
- Input: `font-size: 1.5rem` → Output: `"$value": 24`
- Input: `spacing: 2rem` → Output: `"$value": 32`
- Input: `line-height: 1.5em` → Output: `"$value": 24`

### Step 5: Handle Variable References

For variables that reference other variables (aliases), use the reference syntax:

```json
{
  "Semantic Colors": {
    "text": {
      "primary": {
        "$type": "color",
        "$value": {
          "Light": "{Color Primitives.gray.gray900}",
          "Dark": "{Color Primitives.gray.gray100}"
        }
      }
    }
  }
}
```

The reference format is: `{CollectionName.category.subcategory.variableName}`

## Examples

### Example 1: Simple Color Tokens

**Input**: "Create a collection called 'Brand Colors' with primary (#389fba), secondary (#c9a0dc), and white (#ffffff) colors for light and dark modes"

**Output**:
```json
{
  "Brand Colors": {
    "primary": {
      "$type": "color",
      "$value": {
        "Light": "#389fba",
        "Dark": "#389fba"
      }
    },
    "secondary": {
      "$type": "color",
      "$value": {
        "Light": "#c9a0dc",
        "Dark": "#c9a0dc"
      }
    },
    "white": {
      "$type": "color",
      "$value": {
        "Light": "#ffffff",
        "Dark": "#ffffff"
      }
    }
  }
}
```

### Example 2: Spacing Scale with Code Syntax

**Input**: "Create a spacing scale collection with values 0, 8, 16, 24, 32px. Use camelCase for web."

**Output**:
```json
{
  "Spacing": {
    "space": {
      "0": {
        "$type": "spacing",
        "$value": 0,
        "$extensions": {
          "codeSyntax": {
            "WEB": "space0"
          }
        }
      },
      "1": {
        "$type": "spacing",
        "$value": 8,
        "$extensions": {
          "codeSyntax": {
            "WEB": "space1"
          }
        }
      },
      "2": {
        "$type": "spacing",
        "$value": 16,
        "$extensions": {
          "codeSyntax": {
            "WEB": "space2"
          }
        }
      },
      "3": {
        "$type": "spacing",
        "$value": 24,
        "$extensions": {
          "codeSyntax": {
            "WEB": "space3"
          }
        }
      },
      "4": {
        "$type": "spacing",
        "$value": 32,
        "$extensions": {
          "codeSyntax": {
            "WEB": "space4"
          }
        }
      }
    }
  }
}
```

### Example 3: Unit Conversion from rem to pixels

**Input**: "Create typography tokens: body is 1rem, heading-sm is 1.25rem, heading-md is 1.5rem, heading-lg is 2rem"

**Output**:
```json
{
  "Typography": {
    "fontSize": {
      "body": {
        "$type": "fontSize",
        "$value": 16,
        "$extensions": {
          "codeSyntax": {
            "WEB": "fontSizeBody"
          }
        }
      },
      "headingSm": {
        "$type": "fontSize",
        "$value": 20,
        "$extensions": {
          "codeSyntax": {
            "WEB": "fontSizeHeadingSm"
          }
        }
      },
      "headingMd": {
        "$type": "fontSize",
        "$value": 24,
        "$extensions": {
          "codeSyntax": {
            "WEB": "fontSizeHeadingMd"
          }
        }
      },
      "headingLg": {
        "$type": "fontSize",
        "$value": 32,
        "$extensions": {
          "codeSyntax": {
            "WEB": "fontSizeHeadingLg"
          }
        }
      }
    }
  }
}
```

### Example 4: Semantic Colors with References

**Input**: "Create semantic colors that reference primitives. Text primary should use gray900 in light mode and gray100 in dark mode."

**Output**:
```json
{
  "Semantic Colors": {
    "text": {
      "primary": {
        "$type": "color",
        "$value": {
          "Light": "{Primitives.gray.gray900}",
          "Dark": "{Primitives.gray.gray100}"
        },
        "$extensions": {
          "codeSyntax": {
            "WEB": "textPrimary"
          }
        }
      }
    }
  }
}
```

## Important Notes

1. **Pixel Values Only**: Figma only accepts pixel values for numeric types. Always convert rem, em, %, vw, vh, pt, and other units to pixels:
   - 1rem = 16px (standard base)
   - 1em = 16px (context-dependent)
   - 1pt = 1.333px
   - Ask user for context if percentage or viewport units are present

2. **Single Mode Collections**: If only one mode is needed, omit the mode structure and use direct values:
   ```json
   {
     "Collection": {
       "variable": {
         "$type": "color",
         "$value": "#ffffff"
       }
     }
   }
   ```

2. **Single Mode Collections**: If only one mode is needed, omit the mode structure and use direct values:
   ```json
   {
     "Collection": {
       "variable": {
         "$type": "color",
         "$value": "#ffffff"
       }
     }
   }
   ```

3. **Code Syntax is Optional**: Only include `$extensions.codeSyntax` when explicitly requested by the user

4. **Consistent Hierarchy**: Maintain consistent depth in variable paths (e.g., all variables at same nesting level within a category)

5. **Valid Color Formats**:
   - Hex: `#ffffff`, `#fff`
   - RGB object: `{r: 1, g: 1, b: 1}` (values 0-1)
   - RGBA: `rgba(255, 255, 255, 0.5)`
   - Variable reference: `{collection.path.to.variable}`

6. **File Naming**: Use descriptive names like `brand-colors.json`, `spacing-tokens.json`, `semantic-colors.json`

## Common Patterns

### Pattern 1: Primitive + Semantic Collections

Create two collections: one for primitives (base colors, raw values) and one for semantic tokens (purpose-based references).

### Pattern 2: Multi-Platform Syntax

When supporting multiple platforms, include all in the same variable:

```json
{
  "$extensions": {
    "codeSyntax": {
      "WEB": "backgroundPrimary",
      "iOS": "backgroundColor.primary",
      "ANDROID": "background_color_primary"
    }
  }
}
```

### Pattern 3: Complex Hierarchies

For design systems with deep organization:

```json
{
  "Design System": {
    "component": {
      "button": {
        "background": {
          "primary": {
            "default": { ... },
            "hover": { ... },
            "pressed": { ... }
          }
        }
      }
    }
  }
}
```

## Deliverable

Always create the JSON file and provide it to the user in `/mnt/user-data/outputs/` with a clear, descriptive filename. Include a brief summary of what was generated and how to import it into Figma.
