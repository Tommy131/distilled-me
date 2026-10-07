---
name: ui-ux-design
description: Design, code, and review UI/UX following Apple Human Guidelines / Fluent Design System principles: token-driven theming, WCAG 2025 accessibility compliance, responsive/adaptive layouts, motion-on-purpose, and a strict design-to-code workflow. Use when designing components, writing CSS/Tailwind, building screens, reviewing UI code for a11y/accessibility/responsiveness, or establishing a design system.
disable-model-invocation: true
---

# Design System & UX Specification

A language-agnostic design system modeled on Apple Human Guidelines and Microsoft Fluent — token-driven theming, WCAG 2025 compliance, responsive/adaptive, motion-on-purpose, and a strict workflow from prototype to production.

**Never apply component changes ad hoc.** Always go through the design process.

## Workflow Overview

| Phase | Loading |
|-------|---------|
| Design tokens & layout | `docs/design-system.md` + `docs/layout.md` |
| Component states & patterns | `docs/components.md` |
| Accessibility & a11y | `docs/accessibility.md` |
| Motion & animation | `docs/motion.md` |
| Design process & iteration | `docs/design-process.md` |
| Testing & QA | `docs/testing.md` |

## Non-Negotiable Guardrails (any phase)

1. **No accessibility bypass** — every focusable element has visible focus style, logical tab order, correct `aria-*` attributes, and passes `axe` scans with zero critical errors.
2. **No layout shift on load** — content must be laid out (skeleton if needed) before network requests resolve.
3. **Motion is optional, never required** — every motion has a reduced-motion media query; motion cannot affect accessibility or functionality.
4. **Design tokens are the source of truth** — never hardcode colors, spacing, or typography values in component code.
5. **Responsive ≥1000px breakpoints** — all components must function and be tested at ≥1000px (desktop minimum), ≥768px (tablet), ≥320px (narrow mobile).
6. **Dark/light mode toggle always present** — system-prepared, user-preferred, explicit toggle for non-system themes (OS-level color scheme applies first; user toggle is additive).

## Quick Reference: Token Usage

```css
/* Color tokens */
--color-text-primary, --color-text-secondary, --color-text-tertiary
--color-bg-surface, --color-bg-elevation-1, --color-bg-elevation-2
--color-border-subtle, --color-border-default, --color-border-strong

/* Spacing tokens */
--space-0 (0px), --space-1 (2px), --space-2 (4px), --space-3 (8px)
--space-4 (12px), --space-5 (16px), --space-6 (24px), --space-7 (32px)
--space-8 (40px), --space-9 (48px), --space-10 (64px)

/* Typography tokens */
--font-display, --font-heading, --font-body, --font-label, --font-caption
--font-weight-regular (400), --font-weight-semibold (600), --font-weight-bold (700)

/* Motion tokens */
--duration-fast (48ms), --duration-normal (100ms), --duration-slow (200ms)
--duration-very-slow (320ms)
--easing-ease-in, --easing-ease-out, --easing-ease-in-out, --easing-linear
--easing-bezier-fast, --easing-bezier-spring, --easing-bezier-easy-out
```

## Quick Reference: WCAG 2025 Compliance

| Category | Required |
|-----------|-----------|
| Tab order logical | All interactive elements in logical tab order |
| Focus visible | Focus ring on all focusable elements |
| Keyboard | All actions keyboard accessible, no exclusive mouse |
| ARIA roles | Correct use of `role`, `aria-label`, `aria-live`, `aria-expanded`, `aria-modal` |
| Language | `lang` attribute on all content, `<meta name="description">` |
| Alt images | All images have `alt`; decorative images `alt=""` |
| Headings | One `<h1>` per page, proper heading hierarchy |
| Screen reader | All content announced to screen readers |

For the full WCAG 2025 criteria checklist, see `docs/accessibility.md`.

## Quick Reference: Responsive Breakpoints

| Breakpoint | Device | Notes |
|------------|--------|-------|
| 320px | Narrow mobile | Minimum safe width; horizontal padding ≤ `space-4` |
| 480px | Standard mobile | Small screens |
| 768px | Tablet | Medium screens |
| 1000px | Desktop | Desktop minimum |
| 1280px | Large desktop | Max width container |
| 1440px | Large display | No max-width |

For grid system details, see `docs/layout.md`.

## Quick Reference: Motion Principles

| Principle | Guideline |
|-----------|-----------|
| **Motion-on-purpose** | Every animation has a semantic purpose: draw attention, guide focus, or communicate state change |
| **Consistency** | Same interaction pattern = same motion timing and easing |
| **Reduced motion** | Always include `@media (prefers-reduced-motion: reduce)` fallback |
| **Accessibility** | Motion cannot affect tab order, focus management, or screen reader announcements |

For complete motion guidelines, see `docs/motion.md`.

## Additional Resources

- For complete design system tokens and token architecture, see [design-system.md](docs/design-system.md)
- For layout, grid, and responsive system, see [layout.md](docs/layout.md)
- For component patterns and state machines, see [components.md](docs/components.md)
- For accessibility criteria and tooling, see [accessibility.md](docs/accessibility.md)
- For motion guidelines, see [motion.md](docs/motion.md)
- For design workflow and iteration, see [design-process.md](docs/design-process.md)
- For testing and QA workflows, see [testing.md](docs/testing.md)
