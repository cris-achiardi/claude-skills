# Spec Ideation Examples

Practical examples of the framework applied across different domains.

## Table of Contents

1. Research & Data Processing
2. Product Design
3. Feature Development
4. Content Creation
5. Complex Multi-Domain Example

---

## 1. Research & Data Processing

### Scenario: Normalizing Movement Data

**Phase: Expansion**

User: "As a researcher processing movement data, I need to automate dataset normalization to save time and reduce manual errors."

Claude: "Let's expand on this. What formats are your datasets in? CSV, Excel, JSON? What kind of normalization are we talking about—data types, value ranges, naming conventions? Are there any existing validation rules? What about missing data or outliers?"

User: "Mostly CSV. I need to standardize column names, convert timestamps to a unified format, and handle missing values."

Claude: "Got it. A few more things to consider: Do you have datasets from different sources with different timestamp formats? How do you want to handle missing values—drop them, fill with defaults, interpolate? What about data validation—should the tool flag suspicious values or automatically correct them? And finally, do you need this to run once, or repeatedly on new data?"

**Phase: Contraction**

User: "Good questions. I get data from three different motion capture systems, each with slightly different timestamp formats. For missing values, I'd prefer flagging them rather than auto-filling. And yes, this needs to run repeatedly."

Claude: "Okay, so we're looking at a repeatable pipeline rather than a one-off script. That changes the architecture. Would you rather have a Python script you run manually, or something more automated like a watch folder that processes new files automatically? The trade-off: manual script is simpler to maintain but requires you to remember to run it; automated solution is more convenient but adds complexity in error handling and logging."

User: "Manual script is fine—I want control over when it runs."

Claude: "Makes sense. Last thing: How do you want to handle errors? If one file fails, should the entire batch stop, or should it continue with the others and log the failures?"

**Phase: Documentation**

Once clarity is reached, Claude would help create a specification document including the data pipeline architecture, input/output formats, error handling strategy, and validation rules with justifications for each decision made during contraction.

---

## 2. Product Design

### Scenario: Onboarding Flow

**Phase: Expansion**

User: "I need to design an accessible onboarding flow for our app."

Claude: "Let's unpack this. Who are your users—are we talking about a general audience or specific user types with different needs? What devices do they use? What's the goal of onboarding—feature education, data collection, account setup? And what does 'accessible' mean in your context—WCAG compliance, multiple languages, low-bandwidth support?"

User: "Primary users are healthcare providers using tablets. Goal is account setup and basic feature introduction. Accessible meaning WCAG 2.1 AA compliant."

Claude: "Healthcare context is important. Are there HIPAA considerations for the data you collect during onboarding? What about users with varying levels of tech comfort—do you need different paths for power users vs novices? And given tablet use, are we talking portrait, landscape, or both orientations?"

**Phase: Contraction**

User: "HIPAA definitely applies. Most users are tech-comfortable, but we should have help available. Both orientations need to work."

Claude: "Here's a key decision: Do you want a linear flow where everyone sees the same steps, or an adaptive flow that shortcuts based on user responses? Linear is simpler to build and test, but adaptive provides better UX for experienced users. What's more important for your first version—speed to market or optimal experience?"

User: "Speed to market. We can iterate on adaptive later."

Claude: "Smart. That means we can design a single linear flow with optional 'skip' actions rather than building branching logic. This also simplifies analytics. One more thing: How many steps are you thinking? Research suggests 3-5 is optimal for completion rates, but if you have compliance requirements, that might not be flexible."

**Phase: Documentation**

The resulting product brief would detail the user flow, screen specifications, WCAG compliance checklist, data handling requirements, and the rationale for choosing linear over adaptive (speed to market, simpler analytics).

---

## 3. Feature Development

### Scenario: Contact Import Feature

**Phase: Expansion (EARS format)**

User: "Given a CSV file with contacts in mixed formats, when I run the import, then each contact should be normalized with separate first name and last name columns in title case."

Claude: "This is clearer than a vague request. Let's expand on edge cases: What about names with prefixes like 'Dr.' or 'Mr.'? What about hyphenated last names or compound first names? Should the tool handle international names that don't follow Western first/last name conventions? And what happens if the CSV has unexpected columns or malformed data?"

User: "I didn't think about international names. We do have some users from non-Western countries."

Claude: "This is actually a significant consideration. Western name parsing logic won't work for many cultures. Do you want to detect name format and apply appropriate parsing, or provide a manual review step for ambiguous cases? The first is complex but user-friendly; the second is simpler but requires more user time."

**Phase: Contraction**

User: "Manual review for now—we can improve automation later."

Claude: "Good call. That changes the architecture from a fully automated importer to a two-step process: automated parsing with confidence scoring, then manual review for low-confidence matches. This actually makes the system more robust because users catch edge cases we didn't anticipate. Should the review interface show the original data alongside the parsed data?"

User: "Yes, definitely."

Claude: "That adds a UI component but is essential for informed decisions. One last trade-off: Do you want to save the parsing logic as reusable rules that improve over time, or keep each import independent? Reusable rules mean building a rule engine; independent imports mean simpler code but no learning."

**Phase: Documentation**

The implementation plan would include the two-phase architecture (automated parsing + manual review), UI mockups for the review interface, parsing confidence thresholds, and the decision to defer rule learning to a future iteration with clear justification.

---

## 4. Content Creation

### Scenario: Technical Documentation

**Phase: Expansion**

User: "I need to write technical documentation for our API."

Claude: "Let's define the scope. What's the audience—are these internal developers, external partners, or public developers? What stage is the API—existing and needs docs, or being designed alongside documentation? What format are you thinking—single page, multi-page site, interactive playground? And do you have existing code that could generate API references automatically?"

User: "External developers, API is mostly built, thinking multi-page site. We have OpenAPI specs."

Claude: "Great, OpenAPI specs mean you can auto-generate the reference section. That leaves you focusing on conceptual docs, quickstarts, and examples. Do you need versioning support from day one, or can that come later? And what's the hosting plan—are you using something like ReadTheDocs, GitHub Pages, or custom infrastructure?"

**Phase: Contraction**

User: "Versioning can wait. We'll use GitHub Pages since our code is already there."

Claude: "Makes sense—keeps everything in one place. Now, a structural decision: Do you want a 'cookbook' approach with lots of specific examples, or a 'concepts' approach that explains the architecture deeply with fewer examples? Cookbook is faster to produce and great for getting started, but concepts help developers understand *why* things work that way. Most docs need both, but what's your priority for version 1?"

User: "Cookbook—we need developers up and running fast."

Claude: "Perfect. That means your structure could be: Installation → Authentication → Top 5 Use Cases (with code) → API Reference (auto-generated). This gets developers productive quickly and you can add conceptual depth in future versions. Should the examples be in multiple languages, or just one?"

**Phase: Documentation**

The resulting documentation plan would specify the structure (cookbook approach), content sections with priorities, auto-generation setup for API reference, example code language choices, and the rationale for deferring versioning and deep conceptual docs.

---

## 5. Complex Multi-Domain Example

### Scenario: Internal Research Platform

This example demonstrates how the framework scales to complex, ambiguous problems.

**Phase: Expansion**

User: "We need a better way to manage our research projects. Right now everything is scattered across emails, Drive folders, and spreadsheets."

Claude: "This touches multiple domains—project management, data storage, collaboration. Let's expand systematically. First, what defines a 'research project' in your organization? Is it time-bound, team-based, both? What kind of assets are we talking about—just documents, or also data files, code, analysis results? Who needs access—just the project team, or others for review or replication?"

User: "Projects vary from 3 months to 2 years, teams of 2-6 people. Assets include documents, datasets, analysis scripts, and visualizations. Project teams need full access, but leadership needs read access for reviews."

Claude: "Got it. Now let's talk about the pain points specifically. When you say 'scattered,' what's the actual problem—is it finding things, is it version control, is it knowing who's working on what, or all of the above? And what about collaboration—do people need to work on the same files simultaneously, or is it more about sharing completed work?"

User: "Mostly finding things and version control. We've lost data before because someone worked on an outdated version."

**Phase: Contraction (Multiple Iterations)**

Claude: "Okay, so search and version control are the core problems. Here's a key architectural question: Do you want a full project management system with tasks, timelines, and dependencies, or primarily a well-organized file repository with good search and versioning? The first solves more problems but is a bigger lift; the second addresses your immediate pain with less complexity."

User: "Honestly, the file repository sounds like what we need right now. We use other tools for task management."

Claude: "Smart to keep scope contained. That said, even a 'simple' file repository has decisions. Should it integrate with your existing tools—like syncing from Google Drive, or pulling code from GitHub—or be a standalone hub where everything lives? Integration is convenient but fragile; standalone is reliable but requires migration."

User: "Integration makes sense so we don't have to change workflows drastically."

Claude: "Fair, though integration has trade-offs. If Google Drive or GitHub change their API, your system breaks. Are you okay accepting that risk for the convenience, or would you rather have the stability of a standalone system even if it means more upfront migration work?"

User: "We can accept the risk. Our workflows are too entrenched to change overnight."

Claude: "Understood. Now, about search—do you need full-text search inside documents and code, or just searching by filename, project name, tags, etc.? Full-text is powerful but means indexing everything, which has performance and storage implications."

User: "Filename and metadata search is probably enough for now."

Claude: "That simplifies things significantly. One more thing: You mentioned version control. Do you need Git-style versioning with branches and merges, or just 'snapshots in time' that you can restore? The first is overkill for most document work but necessary for code; the second is simpler but less powerful."

User: "Snapshots are fine for documents. The code is already in GitHub."

**Phase: Documentation**

At this point, enough decisions have been made to document:

1. **Product Brief**: Internal research file repository with metadata search and snapshot versioning, integrating with Google Drive and GitHub, with role-based access for team members and leadership.

2. **Technical Architecture**: Integration points (Drive API, GitHub API), metadata schema, snapshot storage strategy, search indexing approach, authentication/authorization model.

3. **Roadmap**: Phase 1 focuses on Drive/GitHub integration and basic search. Phase 2 adds advanced search filters. Phase 3 considers full-text search if needed. Each phase is scoped based on decisions made during contraction.

4. **Trade-off Log**: Documents decisions made (integration vs standalone, snapshot vs Git-style versioning, metadata vs full-text search) with rationales. This is crucial because when requirements change later, the team can revisit these decisions with full context.

---

## Key Patterns Across Examples

Notice how the framework works similarly across domains:

1. **Expansion always reveals hidden complexity**: Whether it's name parsing rules, WCAG requirements, or API versioning, the expansion phase surfaces considerations the user hadn't thought about.

2. **Contraction is iterative and trade-off-focused**: Claude doesn't just answer questions—it presents options with explicit trade-offs, helping the user make informed decisions.

3. **Documentation captures not just decisions, but reasoning**: This makes the documentation valuable beyond the immediate implementation, serving as a record for future iterations.

4. **The framework scales**: Whether it's a simple script or a complex platform, the three phases work the same way. The difference is just how many iterations happen in each phase.

5. **User maintains control**: At no point does Claude make decisions for the user. It expands possibilities, clarifies trade-offs, and structures thinking, but the user decides.

This is Spec Design: structured thinking that produces specifications, not vibes.