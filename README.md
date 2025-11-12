# Claude Code Skills by Giorris

Curated collection of Claude Code skills for design systems, development workflows, and AI-assisted ideation.

## 🚀 Quick Start

### NPX Installation (Recommended)

The easiest way to install skills is using npx:

```bash
# Interactive mode - select skills from a menu
npx giorris-claude-skills

# Install specific skill
npx giorris-claude-skills install ai-component-metadata

# Install all skills at once
npx giorris-claude-skills --all
```

### Via Claude Code Marketplace

```bash
# Add the marketplace
/plugin marketplace add github:cris-achiardi/claude-skills

# Install by name from marketplace
/plugin install ai-component-metadata@giorris-skills

# Or install directly from GitHub
/plugin install github:cris-achiardi/claude-skills/skills/ai-component-metadata
```

## 📦 Available Skills

### AI Component Metadata
**Category:** Design System
**Version:** 1.0.0

Generate AI-ready metadata for design system components to enable intelligent UI generation. Analyzes component structure and generates structured metadata that helps AI understand when and how to use components correctly.

**Install:**
```bash
npx giorris-claude-skills install ai-component-metadata
```

**Use Cases:**
- Building AI-consumable design systems
- Enabling intelligent UI generation
- Creating component metadata for Storybook
- Integrating with Figma MCP for complete context

**Learn more:** [View Documentation](./skills/ai-component-metadata/)

---

### AI DS Composer
**Category:** Design System
**Version:** 1.0.0

Strategic guide for consuming design system metadata to compose components intelligently. Teaches AI to reason through metadata hierarchically, prioritize component reuse, apply selection criteria, and flag gaps when existing components don't fit requirements.

**Install:**
```bash
/plugin install ai-ds-composer@giorris-skills
```

**Use Cases:**
- Intelligent UI component selection and composition
- Design system component reasoning and reuse
- Understanding hierarchical metadata structures
- Applying anti-pattern rules and selection criteria
- Flagging when custom components are needed

**Learn more:** [View Documentation](./skills/ai-ds-composer/)

---

### Spec Ideation Framework
**Category:** Workflow
**Version:** 1.0.0

Structured framework for working with AI to transform vague ideas into clear, documented specifications through conscious decision-making. Uses a three-phase process: Expansion, Contraction, and Documentation.

**Install:**
```bash
npx giorris-claude-skills install spec-ideation
```

**Use Cases:**
- Planning complex features or projects
- Making design decisions with AI assistance
- Creating specifications from rough ideas
- Structured problem-solving and ideation

**Learn more:** [View Documentation](./skills/spec-ideation/)

---

### Crazy 8's (Solo Version)
**Category:** Workflow
**Version:** 1.0.0

Solo rapid ideation method based on Google Design Sprint Crazy 8's exercise. Generates 8 distinct solution ideas in 8 minutes through rapid-fire ideation or sketch documentation. Includes creativity warm-up questions, built-in timer, optional creative constraints, and generates visual HTML/CSS prototypes.

**Install:**
```bash
npx giorris-claude-skills install crazy-8s
```

**Use Cases:**
- Rapid solo ideation for design challenges
- Exploring multiple solution directions quickly
- Pushing beyond first obvious ideas
- Generating variety before converging on solutions

**Learn more:** [View Documentation](./skills/crazy-8s/)

---

### Problem Mapping
**Category:** Workflow
**Version:** 1.0.0

Foundational problem framing for design sprints and product strategy. Based on Google Design Sprint "Understand" phase methodology. Creates structured problem map documents that establish shared understanding before ideation - defining problem statements, identifying users/stakeholders, setting success criteria, and documenting constraints.

**Install:**
```bash
npx giorris-claude-skills install problem-mapping
```

**Use Cases:**
- Framing design challenges before solution generation
- Establishing shared team understanding
- Documenting goals, constraints, and assumptions
- Foundation for HMW exercises and design sprints

**Learn more:** [View Documentation](./skills/problem-mapping/)

---

## 🌐 Browse Online

Visit **coming soon** to:
- Browse skills with syntax-highlighted previews
- View detailed documentation
- See usage examples
- Copy installation commands

## 🛠️ What are Claude Code Skills?

Skills are reusable prompts and workflows that extend Claude Code's capabilities. They help you:
- Standardize common workflows
- Share best practices across projects
- Enable specialized AI behaviors
- Build domain-specific AI assistants

Learn more about [Claude Code Skills](https://docs.claude.com/en/docs/claude-code/skills).

## 📖 Skill Structure

Each skill in this marketplace follows a consistent structure:

```
skills/
└── skill-name/
    ├── SKILL.md           # Main skill documentation
    ├── LICENSE.txt        # MIT License
    ├── references/        # Additional documentation
    │   └── EXAMPLES.md
    ├── assets/            # Templates and examples
    │   └── template.tsx
    └── scripts/           # Optional utility scripts
        └── helper.py
```

## 🤝 Contributing

While these skills are primarily maintained by Cristian Morales, suggestions and improvements are welcome!

### Reporting Issues
Found a bug or have a suggestion? [Open an issue](https://github.com/cris-achiardi/claude-skills/issues)

### Proposing Improvements
Have an idea to enhance a skill? Feel free to:
1. Fork the repository
2. Make your improvements
3. Submit a pull request with a clear description

## 📜 License

All skills in this marketplace are licensed under the MIT License. See individual skill directories for specific license files.

Copyright © 2025 Cristian Morales

## 🔗 Links

- **Website:** [giorris.dev](https://giorris.dev)
- **Skills Catalog:** coming soon
- **GitHub:** [@cris-achiardi](https://github.com/cris-achiardi)

## 💬 Support

- **Documentation:** [giorris.dev/skills](https://giorris.dev/skills)
- **Issues:** [GitHub Issues](https://github.com/cris-achiardi/claude-skills/issues)
- **Contact:** crmorales.achiardi@gmail.com

---

#### ⭐ Found this useful? Give us a heart to support the project!

[![Buy Me A Coffee](https://img.buymeacoffee.com/button-api/?text=Buy%20me%20a%20coffee&emoji=&slug=giorris&button_colour=5146e6&font_colour=ffffff&font_family=Comic&outline_colour=ffffff&coffee_colour=FFDD00)](https://www.buymeacoffee.com/giorris)
