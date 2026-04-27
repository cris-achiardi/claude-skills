# Changelog

All notable changes to the Giorris Claude Skills marketplace will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.8.0] - 2026-04-26

### Changed

#### figma-component-generator (v1.0.0 → v1.1.0)
- **New Step**: Component classification and dependency resolution (Step 3)
  - Classifies components as Visual, Layout Wrapper, or Compositional based on CSS and metadata signals
  - Layout wrappers trigger a clarity checkpoint (docs-only / wrapper-with-slot / skip) before any generation
  - Compositional components extract dependencies from metadata `nestedComponents`/`commonPartners` and source imports, then reuse existing component sets via `createInstance()` instead of redrawing them as raw frames
- **New Reference**: `references/figma-map-lookup.md`
  - Optional `figma-map.json` schema for direct ID lookups
  - Bootstrap script that scans every page and emits component-set IDs
  - Resolution order: lookup table → fallback to `figma.root.findAll`
- **New Rule**: `references/rules/atomic-dependencies.md`
  - Visual/Layout/Compositional classification with explicit code signals
  - Dependency extraction, Figma traversal, and missing-dependency placeholder behavior
  - Variant selection heuristics (mapping React props like `role`, `color`, `size` to Figma variants) and instance text overrides
- **New Rule**: `references/rules/floating-overlays.md`
  - Detection signals for popovers, dropdowns, tooltips (Floating UI, Radix, Headless UI, cmdk, portals, absolute/fixed positioning)
  - Shape A (split into trigger + floating component sets) vs. Shape B (single component with `State=open`) decision guide
  - Common-component recommendations table (Select, DatePicker, Tooltip, Modal, Toast, etc.)
- **Updated Pattern Detection Table**:
  - Sharper Dynamic-item-count signals (positive vs. negative; OTP, rating, single-child wrappers, render-props excluded)
  - New rows for Floating overlays and Atomic dependencies
  - Cross-dependency note for components that fire both Nested-components and Dynamic-item-count rules
- **Updated `slots.md`**:
  - Pattern A (instance-filled, homogeneous items) vs. Pattern B (frame-filled, heterogeneous items)
  - Selection-persistence pitfall for `slot convert` (must chain in one bash call)
  - `--name` flag may be ignored; new slot ID is printed by the CLI and replaces the original frame ID
- **Updated `nested-components.md`**: Added cross-reference to `atomic-dependencies.md` to disambiguate "create new sub-component set" from "reuse existing component set as instance"
- **Updated Generation Report**: Now includes a Dependencies-resolved line so users see which atoms were wired vs. placeholdered

## [1.7.0] - 2026-04-08

### Added

#### figma-component-generator (v1.0.0)
- **New Skill**: Generate Figma component sets from source code using the figma-cli tool
  - Reads React/CSS/metadata source files and produces Figma components with variants and variable bindings
  - Automatic Figma variable mapping from CSS custom properties
  - Lucide icon library integration with per-variant recoloring
  - Text style application via Figma's local text styles
  - Modular rules system for sizing modes, nested components, slots, and icon recoloring
  - Project-specific configuration via template reference files (typography, icon library)
  - Cross-platform support (macOS and Windows)
  - Comprehensive README with setup guide for new projects

## [1.6.0] - 2025-12-21

### Changed

#### codebase-index (v1.1.0 → v1.2.0)
- **New Feature**: React component support for Astro projects
  - Added `.tsx` and `.jsx` extensions to Astro framework configuration
  - Now correctly detects and indexes React components in hybrid Astro+React projects
  - Impact: +10 components discovered in test project (47 → 57 components)
- **Improved**: Windows compatibility
  - Removed all emoji characters from console output
  - Prevents UnicodeEncodeError on Windows systems with cp1252 encoding
  - Cleaner, more professional terminal output across all platforms
- **Fixed**: Metadata count accuracy
  - React component metadata files (.metadata.tsx) now correctly detected
  - Metadata coverage tracking now 100% accurate for hybrid projects

## [1.5.0] - 2025-11-21

### Changed

#### figma-variables-generator (v1.0.0 → v1.1.0)
- **BREAKING FIX**: Corrected variable types to match Figma's actual API (only 4 types supported)
  - Removed invalid types: `spacing`, `borderRadius`, `fontSize`, `fontWeight`
  - All numeric values now use `number` type with semantic naming
  - Updated all examples to use correct types
- **New Feature**: JSON update and preservation workflow
  - Added Step 0: Check for existing JSON files before updates
  - Automatic detection of update vs. new creation
  - Preserves exact naming to prevent duplicate collections/categories
  - Documents Figma's overwrite behavior (same name = updates, different name = creates new)
- **New Feature**: JSON reformatting for readability
  - Added Step 2.5: Format and Order for Readability guidelines
  - Property ordering: `$type` → `$value` → `$description` → `$extensions`
  - Variable ordering strategies: size-based, numeric, semantic, state-based
  - Category ordering: primitives → semantic → components
  - Example 6: Before/after reformatting of messy plugin-generated JSON
- **Documentation**: Enhanced with critical warnings and best practices
  - Added prominent warnings about using only 4 core types
  - Added Example 5: Updating an existing collection
  - Updated Important Notes with 9 key guidelines
  - Enhanced quick-reference.md with formatting guidelines

### Added
- Updated CHANGELOG.md with detailed improvement notes
- Updated README.md to reflect new capabilities

## [1.4.0] - 2025-11-16

### Added
- **New Skill: figma-variables-generator (v1.0.0)**
  - Generate JSON files for creating Figma variable collections from text descriptions or design token data
  - Support for 8 variable types: color, number, string, boolean, spacing, borderRadius, fontSize, fontWeight
  - Multi-mode support (Light/Dark themes)
  - Variable references/aliases using `{collection.path.variable}` syntax
  - Code syntax generation for multiple platforms (WEB, iOS, ANDROID)
  - Multiple naming conventions: camelCase, snake_case, kebab-case, PascalCase
  - Automatic unit conversion (rem/em/pt to pixels)
  - Hierarchical organization support
  - Quick reference documentation included

### Changed
- Updated README.md with Figma Variables Generator documentation
- Updated marketplace.json to include new skill

## [1.3.0] - 2025-11-14

### Added
- **Version Comparison**: Installer now automatically detects when newer skill versions are available
- **Smart Update Messages**: Shows "Updating X: 1.0.0 → 1.1.0" when upgrading skills
- **Up-to-date Detection**: Displays "already up to date" message when same version is already installed
- **Force Reinstall Flag**: Added `--force` / `-f` flag to force reinstallation of skills
- **Version Tracking**: All SKILL.md files now include version field in frontmatter

### Changed
- Improved user experience with clearer installation status messages
- Updated help text to include `--force` flag examples
- Installer now returns status objects for better error handling

### Fixed
- Skills are no longer skipped when newer versions are available
- Version detection works with all SKILL.md frontmatter formats

## [1.2.1] - 2025-11-14

### Fixed

#### codebase-index (v1.1.0)
- **Critical Bug Fix**: Fixed filename collision bug causing data loss when multiple files had the same name in different directories
  - Changed component key from `file_path.stem` to full `relative_path` to ensure uniqueness
  - Previously, files like `src/pages/index.astro` and `src/pages/skills/index.astro` would overwrite each other
  - Impact: 4 pages were missing from indexes, 6 components incorrectly marked as unused
- **Fixed**: Component name resolution in `usedBy` relationships
  - Added name-to-path mapping to correctly resolve import names to full component paths
  - Previously, `usedBy` arrays were empty or incomplete
- **Added**: Collision detection warnings for debugging
- **Added**: Schema detection support (`schemaDependencies` tracking)
- **Added**: Multi-format metadata file detection (.json, .ts, .tsx)

## [1.2.0] - 2025-11-13

### Added
- Initial release of codebase-index skill (v1.0.0)
- AI development tools and improvements

## [1.0.0] - 2025-11-02

### Added
- Initial marketplace release
- ai-component-metadata skill (v1.0.0)
- ai-ds-composer skill (v1.0.0)
- spec-ideation skill (v1.0.0)
- crazy-8s skill (v1.0.0)
- problem-mapping skill (v1.0.0)
