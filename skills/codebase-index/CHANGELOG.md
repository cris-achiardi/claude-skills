# Codebase Index - Changelog

## [1.1.0] - 2025-11-14

### Fixed
- **Critical**: Fixed filename collision bug causing data loss
  - Root cause: Using `file_path.stem` as dictionary keys caused collisions when multiple files had the same name (e.g., `index.astro`, `[slug].astro` in different directories)
  - Solution: Changed to use full relative paths as component keys
  - Impact: Previously lost 4 pages (index.astro files in subdirectories), now correctly captures all 46 components (was 42)

- **Critical**: Fixed component name resolution in `usedBy` relationships
  - Root cause: Import names like `"ThoughtsSection"` couldn't match full path keys like `"src/components/ui/ThoughtsSection.astro"`
  - Solution: Added name-to-path mapping in `_populate_used_by()` function
  - Impact: `usedBy` arrays now correctly populated (were previously empty or incomplete)

### Added
- Collision detection warnings for debugging
- Schema detection and tracking (`schemaDependencies` field)
- Multi-format metadata file detection (.metadata.json, .metadata.ts, .metadata.tsx)
- Support for both `Component.astro.metadata.ts` and `Component.metadata.ts` patterns

### Changed
- Component keys now use full relative paths instead of stem names
- Statistics now include `schemas_found` count
- Dependencies now include `schemas` category

### Testing
- Verified on Astro codebase (astro-giorris)
- Before: 42 components, incomplete relationships
- After: 46 components, 100% accurate relationships

## [1.0.0] - 2025-11-13

### Added
- Initial release
- Framework auto-detection (React, Vue, Svelte, Astro, Next.js, Angular, Solid)
- TOON format support (30-60% token savings)
- Component relationship mapping (uses/usedBy)
- NPM dependency tracking
- Utility and CSS detection
- Data query pattern extraction
