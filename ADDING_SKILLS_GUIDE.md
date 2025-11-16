# Adding Skills Guide

This guide walks through the complete process of adding a new skill to the Giorris Claude Skills marketplace.

## Overview

Each skill requires:
1. Skill files in `skills/` directory
2. Entry in `.claude-plugin/marketplace.json`
3. Documentation in `README.md`
4. Changelog entry in `CHANGELOG.md`
5. Version bump in `package.json`

## Step-by-Step Process

### 1. Create Skill Directory Structure

Create the following directory structure for your new skill:

```
skills/
└── your-skill-name/
    ├── SKILL.md              # Main skill file (REQUIRED)
    ├── LICENSE.txt           # MIT License (REQUIRED)
    ├── references/           # Additional documentation (OPTIONAL)
    │   ├── quick-reference.md
    │   └── examples.md
    ├── assets/               # Templates, examples (OPTIONAL)
    │   └── template.tsx
    └── scripts/              # Utility scripts (OPTIONAL)
        └── helper.py
```

**Required files:**
- `SKILL.md` - Main skill prompt and documentation
- `LICENSE.txt` - MIT License file

**Optional directories:**
- `references/` - Additional reference documentation
- `assets/` - Templates, examples, or other assets
- `scripts/` - Utility scripts (e.g., Python scripts for automation)

### 2. Create SKILL.md File

The `SKILL.md` file must include frontmatter with metadata:

```markdown
---
name: your-skill-name
description: Brief description of what the skill does. Triggers include "keyword1", "keyword2", or when user needs specific functionality.
---

# Your Skill Name

Detailed description of the skill and its capabilities.

## Core Capabilities

- Feature 1
- Feature 2
- Feature 3

## Workflow

### Step 1: Initial Setup
Instructions...

### Step 2: Main Process
Instructions...

## Examples

### Example 1: Use Case Name
**Input**: "User request"
**Output**: Expected result

## Important Notes

1. Key consideration 1
2. Key consideration 2
```

**Frontmatter fields:**
- `name` - Skill ID (lowercase, hyphenated)
- `description` - Brief description (1-2 sentences) that includes trigger keywords

### 3. Create LICENSE.txt

Use the standard MIT License template:

```
MIT License

Copyright (c) 2025 Your Skill Name Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### 4. Update marketplace.json

Add your skill entry to `.claude-plugin/marketplace.json`:

```json
{
  "name": "your-skill-name",
  "source": "./skills/your-skill-name",
  "description": "Brief description matching SKILL.md frontmatter",
  "version": "1.0.0",
  "category": "design-system|workflow|development",
  "author": {
    "name": "Cristian Morales",
    "email": "crmorales.achiardi@gmail.com"
  },
  "license": "MIT"
}
```

**Categories:**
- `design-system` - Design system and component-related skills
- `workflow` - Process and methodology skills
- `development` - Development tools and automation skills

**Version format:** Use semantic versioning (X.Y.Z)
- Start new skills at `1.0.0`
- Patch updates (bug fixes): increment Z
- Minor updates (new features): increment Y
- Major updates (breaking changes): increment X

### 5. Update README.md

Add a new section for your skill in `README.md` under the "Available Skills" section. Follow the existing format:

```markdown
### Your Skill Name
**Category:** Design System|Workflow|Development
**Version:** 1.0.0

Brief description of the skill (1-2 paragraphs explaining what it does and why it's useful).

**Install:**
\`\`\`bash
npx giorris-claude-skills install your-skill-name
\`\`\`

**Use Cases:**
- Use case 1
- Use case 2
- Use case 3
- Use case 4

**Learn more:** [View Documentation](./skills/your-skill-name/)

---
```

**Placement:** Add new skills in this order:
1. Design System skills (alphabetically)
2. Development skills (alphabetically)
3. Workflow skills (alphabetically)

### 6. Update CHANGELOG.md

Add an entry at the top of `CHANGELOG.md`:

```markdown
## [X.Y.0] - YYYY-MM-DD

### Added
- **New Skill: your-skill-name (v1.0.0)**
  - Brief description of what the skill does
  - Key feature 1
  - Key feature 2
  - Key feature 3

### Changed
- Updated README.md with Your Skill Name documentation
- Updated marketplace.json to include new skill
```

### 7. Update package.json Version

Increment the version in `package.json`:

```json
{
  "name": "giorris-claude-skills",
  "version": "X.Y.0",
  ...
}
```

**Version increment rules:**
- New skill added: increment minor version (1.3.0 → 1.4.0)
- Skill updated: increment minor version (1.3.0 → 1.4.0)
- Bug fix only: increment patch version (1.3.0 → 1.3.1)

### 8. Update README.md Latest Release

Update the "Latest Release" section in `README.md`:

```markdown
## 📢 Latest Release

**Version X.Y.0** - Brief description of what changed

Description of the main changes in this release.
```

## Creating the .skill Package (For astro-giorris)

If you need to distribute the skill through your website (giorris.dev/skills), create a `.skill` package:

### 1. Create the package structure

```bash
cd /tmp
mkdir your-skill-name
cp -r /path/to/claude-skills/skills/your-skill-name/* your-skill-name/
```

### 2. Create the .skill archive

```bash
zip -r your-skill-name.skill your-skill-name/
```

### 3. Add to astro-giorris

```bash
# Copy the .skill file
cp your-skill-name.skill /path/to/astro-giorris/public/skills/downloadables/

# Copy the cover image (if you have one)
cp your-cover-image.webp /path/to/astro-giorris/public/skills/covers/
```

## Testing Your Skill

Before publishing, test the skill installation:

### 1. Test local installation

```bash
# From the claude-skills directory
npm test

# Try installing your skill
npx . install your-skill-name
```

### 2. Verify skill location

Check that the skill was installed to:
```
~/.claude/skills/your-skill-name/
```

### 3. Test in Claude Code

1. Open Claude Code
2. Type a trigger phrase from your skill description
3. Verify the skill is recognized and works as expected

## Publishing Checklist

Before pushing to GitHub and publishing to npm:

- [ ] Skill directory created in `skills/`
- [ ] `SKILL.md` with proper frontmatter
- [ ] `LICENSE.txt` file
- [ ] Entry added to `.claude-plugin/marketplace.json`
- [ ] README.md updated with skill documentation
- [ ] CHANGELOG.md updated with new entry
- [ ] package.json version incremented
- [ ] README.md "Latest Release" section updated
- [ ] Skill tested locally
- [ ] All files committed to git
- [ ] Ready to push to GitHub

## Publishing to npm

Once everything is ready:

```bash
# 1. Commit all changes
git add .
git commit -m "feat: add your-skill-name skill v1.0.0"

# 2. Create a git tag
git tag v1.4.0

# 3. Push to GitHub
git push origin main --tags

# 4. Publish to npm
npm publish
```

## Skill Versioning Best Practices

### Skill Version (in SKILL.md frontmatter)
- Start at `1.0.0` for new skills
- Increment for changes to the skill content

### Package Version (in package.json)
- Increment when adding/updating any skill
- Follows the main package versioning

### When to increment what:

**New skill added:**
- Skill version: `1.0.0`
- Package version: Minor increment (1.3.0 → 1.4.0)

**Skill content updated:**
- Skill version: Depends on change type
  - Bug fix in skill: 1.0.0 → 1.0.1
  - New feature in skill: 1.0.0 → 1.1.0
  - Breaking change: 1.0.0 → 2.0.0
- Package version: Minor increment (1.3.0 → 1.4.0)

**Installer/package bug fix:**
- Skill version: Unchanged
- Package version: Patch increment (1.3.0 → 1.3.1)

## Common Patterns

### Design System Skills
- Focus on component metadata, design tokens, or UI generation
- Often include TypeScript/JSON examples
- May include asset templates

### Workflow Skills
- Focus on processes and methodologies
- Step-by-step instructions
- Often include examples of deliverables

### Development Skills
- Focus on automation and tooling
- May include scripts directory
- Often have more technical documentation

## Tips

1. **Keep SKILL.md focused** - The skill prompt should be clear and actionable
2. **Use references/ for details** - Move extensive documentation to reference files
3. **Include examples** - Show concrete input/output examples
4. **Test thoroughly** - Verify the skill works in different contexts
5. **Document triggers** - Make it clear when the skill should activate
6. **Version consistently** - Follow semantic versioning strictly

## Questions?

- Check existing skills in `skills/` directory for examples
- Review [Claude Code Skills documentation](https://docs.claude.com/en/docs/claude-code/skills)
- Open an issue on GitHub for questions
