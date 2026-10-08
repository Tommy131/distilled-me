---
name: ui-ux-design
description: >
  Design, implement, and review OwO UI with token-driven Flutter, React, and WPF
  systems, responsive shells, WCAG 2.2 AA, and purposeful motion. Use for visual
  redesigns, component/layout/theme work, accessibility reviews, and existing OwO
  Recorder Signal pages; preserve current behavior unless the user explicitly changes it.
metadata:
  short-description: Design and review OwO interfaces safely
---

# OwO UI/UX design

Use this skill to turn an interface brief or an existing OwO screen into a coherent, accessible, responsive product surface. The default system comes from the OwO Flutter `AppThemeData` and Flight web tokens. For the existing OwO Recorder web app, load [recorder-signal-patterns.md](docs/recorder-signal-patterns.md) when the task touches its Signal visual language, user quota pages, or administration screens.

## Non-negotiable product contract

1. **Preserve behavior by default.** A visual redesign keeps routes, API calls, request bodies, permissions, business rules, submit timing, content order, and existing workflows intact. Inspect handlers and tests before changing markup. If a behavior change is requested, isolate and state it.
2. **Use semantic tokens.** Feature code consumes the project's existing color, spacing, radius, type, shadow, and motion variables. Never introduce a raw color or ad-hoc spacing value in a component when a token exists. When an app has a local token namespace, map the design to it instead of forcing the generic OwO names.
3. **Make states first-class.** Loading, empty, error, success, disabled, partial, and long-content states need an intentional layout and an accurate accessible announcement. Do not invent metrics, fake records, or synthetic operational status to fill empty space.
4. **Avoid duplicate communication.** If several records produce the same user-facing warning, deduplicate it at the presentation boundary. Keep distinct guidance, merge action lists in stable order, and show one heading for the group. Do not hide a genuinely different issue merely because it appears in the same panel.

## Default design direction

- Use whitespace and a responsive grid to make information scannable. Bento groupings are appropriate for independent metrics or actions; do not turn every row into a decorative card.
- Prefer flat bordered surfaces with restrained shadows. Use 16px, 24px, or 32px radii deliberately by hierarchy; keep controls smaller than primary panels.
- Use a strong display/title weight against a quiet readable body weight. Use a mono face for IDs, timestamps, quantities, scores, and other data where alignment matters.
- Keep one accent for the primary action and status emphasis. Semantic success, warning, and danger colors must remain distinct and readable in both themes.
- Use gradients, blur, and glow only when they explain grouping or hierarchy. Dark mode uses a deep tinted surface rather than pure black.

## Workflow

### 1. Reconnaissance

Identify the route, shell, component entry point, existing tokens, data contract, interaction handlers, tests, and current responsive rules. Read only the relevant references below. Write down the single job of the page and the information that must remain in its original order.

### 2. Plan before styling

Create a small layout model: page header, primary action, summary or filters, main content, and state surfaces. Choose a desktop and mobile arrangement before editing CSS. Decide which information is a metric, a filter, a record, a status, or an irreversible action; the semantic category should determine the component shape.

### 3. Implement in layers

1. Apply tokens and page geometry.
2. Establish hierarchy and responsive reflow.
3. Style component states and interaction feedback.
4. Add only the minimum markup needed for accessible names, regions, status messages, and focus behavior.
5. Keep page-specific rules scoped. Shared CSS changes must be justified by more than one consumer.

### 4. Validate behavior and presentation

Run the smallest meaningful unit tests first, then the project's build and lint checks. Use Playwright or the available browser harness for changed routes. Check light/dark themes, Chinese/English when localization exists, 320/390/768/1024/1440px or the product's agreed widths, no document-level horizontal overflow, and axe WCAG 2/2.1/2.2 AA checks. Exercise at least one success, failure, empty, loading, long-content, and destructive-confirmation path when those states exist.

Do not claim that a complete test suite passed when it is known to be incomplete, OOM-prone, or blocked by pre-existing failures. Report the exact targeted checks and their limits.

## System defaults

The canonical OwO defaults remain in [design-system.md](docs/design-system.md), [layout.md](docs/layout.md), [components.md](docs/components.md), and [assets/tokens.css](assets/tokens.css):

- 8pt spacing; common 8/12/16px radius; 300ms motion with reduced-motion fallback.
- Light/dark/system themes with semantic surface, text, border, focus, and status tokens.
- Desktop sidebar 200px/60px collapsed, mobile shell below 650px, and a 56px app bar unless a product-specific shell says otherwise.
- Native controls and table semantics where appropriate; visible `:focus-visible`; one logical `h1`; status updates via `role="status"` or `role="alert"`.
- Modal focus moves inside, stays contained, closes with Escape when safe, and returns to the trigger.

## Reference routing

| Need | Read |
| --- | --- |
| OwO tokens, themes, and product provenance | `docs/design-system.md`, `assets/tokens.css`, `docs/owo-sources.md` |
| Shell and breakpoint decisions | `docs/layout.md` |
| Component recipes | `docs/components.md` |
| WCAG, semantics, and focus | `docs/accessibility.md` |
| Motion | `docs/motion.md` |
| Design process and decision records | `docs/design-process.md` |
| Test and browser QA patterns | `docs/testing.md` |
| OwO Recorder Signal visual language, admin patterns, state deduplication, and validation matrix | `docs/recorder-signal-patterns.md` |

Load only the references that materially affect the current request. The Recorder reference is an implementation overlay, not a replacement for canonical OwO tokens or for product-specific requirements.
