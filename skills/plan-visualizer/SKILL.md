
---
name: plan-visualizer
description: Visualize agent plans, task lists, and project workflows as beautiful interactive HTML pages. Use this skill whenever the user wants to visualize a plan, see a plan as a diagram, render a task breakdown, turn a plan file into a flowchart or timeline, or display project steps and dependencies graphically. Also trigger when the user says things like "show me the plan", "visualize this workflow", "make a diagram of these steps", "render my plan as HTML", or has a plan.md / TODO file they want to see visually.
---

# Plan Visualizer

Transform agent-generated plans, task lists, and workflow documents into rich, interactive HTML visualizations.

## Input Sources

Identify the plan content from one of these sources:

1. **Claude Code plan mode output** — the structured plan from the current conversation (steps, sub-steps, notes)
2. **Existing plan files** in the project — look for files like `plan.md`, `TODO.md`, `PLAN.md`, `tasks.md`, or any file the user points to
3. **User-provided plan text** — pasted directly in the conversation

## Step 1: Parse the Plan

Extract the following structure from the plan content:

```
Plan {
  title: string
  description?: string
  phases: Phase[]
  dependencies?: Dependency[]
}

Phase {
  id: string
  name: string
  description?: string
  steps: Step[]
  status?: "pending" | "in_progress" | "completed"
}

Step {
  id: string
  text: string
  substeps?: string[]
  status?: "pending" | "in_progress" | "completed"
  dependsOn?: string[]       // IDs of steps this depends on
  resources?: string[]        // files, tools, APIs involved
  notes?: string
  estimatedEffort?: string    // "small" | "medium" | "large"
}

Dependency {
  from: string   // step or resource ID
  to: string     // step or resource ID
  type: "blocks" | "uses" | "produces" | "reads" | "writes"
}
```

When parsing markdown plans:
- `#` / `##` headings → phases
- Numbered lists / `- [ ]` checkboxes → steps
- Indented items → substeps
- `[x]` → completed, `[ ]` → pending
- Look for keywords like "depends on", "requires", "after", "blocks" to infer dependencies
- Look for file paths, tool names, API references to extract resources

## Step 2: Generate the HTML Visualization

Read the HTML template at `assets/template.html` (relative to this skill's directory). This template provides the full interactive visualization framework.

Populate the template by replacing the `__PLAN_DATA__` placeholder with the parsed plan data as a JSON object.

The template renders two complementary views:

### Timeline View (for SOP / workflow steps)
- Vertical timeline with phase groupings
- Each step is an interactive card showing status, description, and substeps
- Progress indicators per phase
- Animated transitions and hover effects
- Color-coded status (pending/in-progress/completed)

### Dependency Tree View (for resource relationships)
- Interactive tree/graph showing how steps and resources connect
- Nodes for steps, files, tools, and APIs
- Directed edges showing dependency types (blocks, uses, produces)
- Expandable/collapsible nodes
- Highlight dependency chains on hover

### Shared Features
- Tab navigation between Timeline and Dependency views
- Search/filter to find specific steps
- Click a step in Timeline to highlight it in the Dependency tree
- Dark/light theme toggle
- Export as PNG option
- Responsive layout
- Keyboard navigation (arrow keys to move between steps, Enter to expand)

## Step 3: Write and Open

1. Write the populated HTML to a temp file: `/tmp/plan-viz-{timestamp}.html`
2. Open it in the browser: `open /tmp/plan-viz-{timestamp}.html` (macOS) or `xdg-open` (Linux)
3. Tell the user the file path in case they want to keep it

## Design Guidelines

The visualization should feel polished and delightful:

- **Default Light Theme**: The template defaults to a clean, bright light theme. Users can toggle to dark mode manually.
- **Chinese-first UI**: All UI labels, status text, and placeholders are in Chinese (中文). When parsing plans, prefer translating phase/step names to Chinese if the source is in Chinese or the user communicates in Chinese. Keep technical terms (API, CLI, etc.) in English.
- **Typography**: Use a modern sans-serif stack. Headings in a display font (loaded from Google Fonts), body in a clean readable font.
- **Colors**: Use a carefully curated palette — not the usual blue/gray defaults. Use CSS custom properties for easy theming.
- **Motion**: Subtle entrance animations for cards (staggered fade-in), smooth transitions on hover/expand, animated progress bars.
- **Layout**: Clean whitespace, clear visual hierarchy, responsive grid. Timeline should feel like a narrative flow, not a boring list.
- **Icons**: Use inline SVG icons for status indicators, step types, and navigation. No external icon dependencies.
- **Interactivity**: Everything should feel responsive — hover states, click feedback, smooth scrolling to sections.
- **Dependency Graph**: Uses layered (Sugiyama-style) topological layout for dependency views — upstream dependencies appear above downstream steps, avoiding the chaotic overlapping of pure force-directed layouts. The layout computes topological layers first, then applies gentle force refinement for aesthetics.

Avoid: generic Bootstrap aesthetics, harsh solid colors, cramped layouts, static uninteractive pages.
