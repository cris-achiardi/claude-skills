# Changelog

All notable changes to the Giorris Claude Skills marketplace will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
