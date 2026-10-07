# UI/UX Design System & Workflow

Design system and UX workflow following Apple Human Guidelines and Microsoft Fluent Design System principles. Token-driven theming, WCAG 2025 accessibility compliance, responsive/adaptive layouts, motion-on-purpose.

## Usage

Load this skill via `/ui-ux-design` or `skill: ui-ux-design` when designing components, writing CSS/Tailwind, building screens, reviewing UI code for a11y/accessibility/responsiveness, or establishing a design system.

## Documentation

| Topic | Document |
|-------|----------|
| Design tokens & theming | `docs/design-system.md` |
| Layout & responsive design | `docs/layout.md` |
| Component patterns | `docs/components.md` |
| Accessibility & a11y | `docs/accessibility.md` |
| Motion & animation | `docs/motion.md` |
| Design process | `docs/design-process.md` |
| Testing & QA | `docs/testing.md` |

## Quick Start

1. Define design tokens (colors, spacing, typography, motion) in `docs/design-system.md`
2. Define breakpoints in `docs/layout.md`
3. Design components following `docs/components.md` state machine pattern
4. Verify accessibility with `docs/accessibility.md` WCAG 2025 criteria
5. Add motion per `docs/motion.md` motion-on-purpose principles
6. Iterate per `docs/design-process.md` workflow (prototype → system → production)

## Non-Negotiable Guardrails

1. No accessibility bypass — every focusable element has visible focus style, logical tab order, correct `aria-*` attributes
2. No layout shift on load — content must be laid out (skeleton if needed) before network requests resolve
3. Motion is optional, never required — every motion has a reduced-motion media query
4. Design tokens are the source of truth — never hardcode colors, spacing, or typography values
5. Responsive ≥1000px breakpoints — all components must function and be tested at ≥1000px
6. Dark/light mode toggle always present — system-prepared, user-preferred, explicit toggle
