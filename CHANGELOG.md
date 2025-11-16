# Changelog

All notable changes to the Giorris Claude Skills marketplace will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
