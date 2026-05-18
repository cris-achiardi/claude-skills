# Figma Map Lookup Table

## What it is

A JSON file that maps code components to their Figma node IDs (page IDs and component set IDs). This lets a generation skill use direct ID lookups (`figma.getNodeByIdAsync`) instead of full-file traversal (`figma.root.findAll`) when resolving dependencies.

## Why it exists

`figma.root.findAll()` traverses all pages synchronously. This can fail silently in certain conditions (e.g., special characters in page names, lazy-loaded pages). Direct ID lookup is faster and more reliable.

## File location

The map file location is **implementation-defined** — consuming skills decide where it lives. The map file is **external to this reference**: this document describes only the schema and resolution algorithm. Common conventions:

- A user data directory (e.g., `~/.claude/data/figma-map.json` for Claude Code workflows)
- A project-local file (e.g., `.figma-map.json` at the repo root)
- A shared team location

The map is **optional**. If absent, the skill must fall back to `findAll` for dependency resolution.

> A formal JSON schema for this map may be published alongside this ref in a future iteration. Until then, treat the schema below as the spec.

## Schema

```json
{
  "figmaFileKey": "<figma-file-key-from-url>",
  "figmaFileName": "<human-readable-file-name>",
  "lastScanned": "<YYYY-MM-DD>",
  "components": {
    "<ComponentName>": {
      "code": "<relative-path-from-repo-root>",
      "category": "atoms | molecules | organisms | templates",
      "pageId": "<figma-page-node-id>",
      "componentSetId": "<figma-component-set-id> | null"
    }
  },
  "icons": {
    "<IconSetName>": {
      "pageId": "<page-id>",
      "componentSetId": "<component-set-id>",
      "variantCount": 1234
    }
  }
}
```

### Field descriptions

| Field | Type | Description |
|---|---|---|
| `figmaFileKey` | string | The file key from the Figma URL (used as sanity check) |
| `figmaFileName` | string | Human-readable name for reference |
| `lastScanned` | string | ISO date of last bootstrap scan |
| `components.<Name>.code` | string | Relative path to component directory in the codebase |
| `components.<Name>.category` | string | Atomic design category |
| `components.<Name>.pageId` | string | Figma page node ID (always present) |
| `components.<Name>.componentSetId` | string or null | Figma component set ID, null if not yet generated |
| `icons.<Name>.componentSetId` | string | Icon library component set ID |

## How to generate it

### Bootstrap scan (recommended)

Connect to Figma via the CLI, then run this eval to scan all existing component sets:

```javascript
(async () => {
  const results = [];
  for (const page of figma.root.children) {
    const sets = page.findAll(n => n.type === 'COMPONENT_SET');
    for (const set of sets) {
      results.push({
        name: set.name,
        componentSetId: set.id,
        pageId: page.id,
        pageName: page.name.trim(),
        variantCount: set.children.length
      });
    }
  }
  return JSON.stringify(results, null, 2);
})()
```

Then match the results against the codebase component directories to build the JSON. Components with a Figma page but no component set yet get `"componentSetId": null`.

### Manual updates

After generating a new component, the consuming skill should add or update its `componentSetId` in the JSON. The component set ID is returned in the generation report.

## How the skill uses it

During dependency resolution, when the skill needs to find a component set:

1. **Check the map first**: Look up the dependency name in `components`. If `componentSetId` is non-null, use `figma.getNodeByIdAsync(id)` for a direct lookup.
2. **Validate the file key**: Compare the URL's file key against `figmaFileKey`. If they don't match, skip the map (IDs are file-specific).
3. **Fall back to findAll**: If the component isn't in the map or has `null` componentSetId, fall back to `figma.root.findAll()`.

```javascript
// Pseudocode for dependency resolution with map
const map = loadFigmaMap(); // read from the path defined by the consuming skill
const fileKey = parseFileKeyFromUrl(figmaUrl);

if (map && map.figmaFileKey === fileKey) {
  const entry = map.components[dependencyName];
  if (entry && entry.componentSetId) {
    // Fast path: direct ID lookup
    const node = await figma.getNodeByIdAsync(entry.componentSetId);
    if (node && node.type === 'COMPONENT_SET') {
      return node; // found via map
    }
  }
}

// Slow path: full traversal fallback
const matches = figma.root.findAll(n =>
  n.type === 'COMPONENT_SET' && n.name === dependencyName
);
```
