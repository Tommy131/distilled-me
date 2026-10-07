---
name: ui-ux-design
description: >
  Design, implement, and review UI/UX with a token-driven design system, WCAG 2.2 AA
  accessibility, responsive/adaptive layout, and motion-on-purpose. Covers design tokens,
  component state machines, focus/keyboard/screen-reader requirements, breakpoints, theming,
  and design-to-code workflow. Use when designing components or screens, writing CSS/Tailwind,
  establishing or extending a design system, reviewing UI for a11y/responsiveness/theming, or
  when the user mentions accessibility, WCAG, design tokens, focus rings, or reduced motion.
  Prefer this skill for systemized UI/a11y work; use a general frontend-design skill for one-off
  visual styling without a design-system workflow.
---

# Design System & UX Specification

Token-driven UI system inspired by Apple HIG and Microsoft Fluent ideas: semantic tokens, WCAG 2.2 AA, responsive layout, motion-on-purpose, and a prototype → system → production workflow.

**Never apply component changes ad hoc.** Go through the design process (`docs/design-process.md`) unless the user explicitly asks for a quick one-off tweak.

## Workflow Overview

| Phase | Load |
|-------|------|
| Design tokens & theming | `docs/design-system.md` + `assets/tokens.css` |
| Layout & breakpoints | `docs/layout.md` |
| Component states & patterns | `docs/components.md` |
| Accessibility (WCAG 2.2 AA) | `docs/accessibility.md` |
| Motion & animation | `docs/motion.md` |
| Design process & iteration | `docs/design-process.md` |
| Testing & QA | `docs/testing.md` |

Load only the docs needed for the current task.

## Guardrails

### Always (non-negotiable)

1. **No accessibility bypass** — focusable controls have visible `:focus-visible` styles, logical tab order, correct names/roles; aim for zero critical `axe-core` violations.
2. **No layout shift on load** — reserve space (skeleton/placeholder) before late content arrives.
3. **Motion is optional** — every animation has a `prefers-reduced-motion` fallback; motion must not break focus, tab order, or screen-reader announcements.
4. **Tokens are source of truth** — no raw hex/spacing/type values in component code; use semantic CSS variables (see `assets/tokens.css`).

### Defaults (may trim — declare in project docs)

5. **Breakpoints** — default set: 320 / 480 / 768 / 1024 / 1280 / 1440. Desktop “comfortable” target is ≥1024px. Mobile-only or embedded UIs MAY drop unused breakpoints in `DESIGN` / design-system docs.
6. **Theme control** — support `prefers-color-scheme` and light/dark semantic tokens. An explicit in-app theme toggle is the **default for multi-page apps**; landing pages, emails, or OS-native shells MAY omit the toggle if system scheme is enough — document the choice.

## Quick Reference: Tokens

Use semantic tokens in components. Full list: `docs/design-system.md` and `assets/tokens.css`.

```css
/* Color */
--color-text-primary, --color-text-secondary, --color-text-tertiary
--color-bg-surface, --color-bg-elevation-1, --color-bg-elevation-2
--color-border-subtle, --color-border-default, --color-border-strong
--color-focus-ring

/* Spacing (4px base grid; 2px only for hairline tweaks) */
--space-0 … --space-10  /* 0, 2, 4, 8, 12, 16, 24, 32, 40, 48, 64 */

/* Typography roles (use longhands, not fake font shorthand) */
--font-family-sans
--font-size-display, --font-size-heading, --font-size-body, --font-size-label, --font-size-caption
--line-height-display, --line-height-heading, --line-height-body, …
--font-weight-regular (400), --font-weight-semibold (600), --font-weight-bold (700)

/* Motion */
--duration-fast (120ms), --duration-normal (200ms), --duration-slow (300ms), --duration-deliberate (450ms)
--easing-standard, --easing-emphasized, --easing-entrance, --easing-exit
```

## Quick Reference: WCAG 2.2 AA

| Area | Requirement |
|------|-------------|
| Keyboard | All actions reachable and operable by keyboard |
| Focus visible | `:focus-visible` indicator on every focusable control |
| Focus order | Matches visual/reading order; no tabindex > 0 |
| Name, Role, Value | Correct accessible name; native elements preferred over ARIA |
| Contrast | Text ≥ 4.5:1 (normal), ≥ 3:1 (large); UI components/graphics ≥ 3:1 |
| Images | Informative images have `alt`; decorative use `alt=""` |
| Headings | One `<h1>` per page; hierarchical headings |
| Language | `lang` on `<html>` (and on foreign phrases when needed) |
| Target size | Interactive targets meet WCAG 2.2 minimum target size (AA) |
| Status | Errors and updates exposed via text and/or polite/assertive live regions |

Full criteria and patterns: `docs/accessibility.md`.

## Quick Reference: Breakpoints

| Breakpoint | Role |
|------------|------|
| 320px | Narrow mobile floor |
| 480px | Phone |
| 768px | Tablet |
| 1024px | Desktop default |
| 1280px | Large desktop / max content width often starts |
| 1440px | Wide display |

Details: `docs/layout.md`.

## Quick Reference: Motion

| Principle | Guideline |
|-----------|-----------|
| Purpose | Attention, focus guidance, or state change — no decorative-only motion that blocks tasks |
| Consistency | Same interaction → same duration/easing |
| Reduced motion | `@media (prefers-reduced-motion: reduce)` |
| Performance | Prefer `transform` and `opacity` |

Details: `docs/motion.md`.

## Additional Resources

- [design-system.md](docs/design-system.md) — token architecture
- [assets/tokens.css](assets/tokens.css) — copy-ready CSS variables
- [layout.md](docs/layout.md) — grid and responsive rules
- [components.md](docs/components.md) — state machines and patterns
- [accessibility.md](docs/accessibility.md) — WCAG 2.2 AA
- [motion.md](docs/motion.md) — motion guidelines
- [design-process.md](docs/design-process.md) — workflow
- [testing.md](docs/testing.md) — visual / a11y / responsive QA
