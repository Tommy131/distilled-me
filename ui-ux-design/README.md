# UI/UX Design System & Workflow

Token-driven design system and UX workflow (Apple HIG / Fluent-inspired). WCAG 2.2 AA, responsive layout, motion-on-purpose.

## Usage

Invoke via `/ui-ux-design` or ask for design-system / a11y / token work. The agent should load `SKILL.md` then only the `docs/` files needed for the task.

## Documentation

| Topic | Document |
|-------|----------|
| Design tokens & theming | `docs/design-system.md` |
| Copy-ready CSS tokens | `assets/tokens.css` |
| Layout & responsive design | `docs/layout.md` |
| Component patterns | `docs/components.md` |
| Accessibility (WCAG 2.2 AA) | `docs/accessibility.md` |
| Motion & animation | `docs/motion.md` |
| Design process | `docs/design-process.md` |
| Testing & QA | `docs/testing.md` |

## Quick Start

1. Copy or adapt `assets/tokens.css`; define light/dark semantic tokens (`docs/design-system.md`).
2. Confirm breakpoints in `docs/layout.md` (trim if the product is mobile-only — document it).
3. Build components as explicit state machines (`docs/components.md`).
4. Verify WCAG 2.2 AA with `docs/accessibility.md` + `axe-core`.
5. Add motion per `docs/motion.md` with reduced-motion fallbacks.
6. Iterate with `docs/design-process.md` (prototype → system → production).

## Guardrails

**Always:** no a11y bypass; no layout shift on load; motion optional; tokens only (no magic values).

**Defaults (declarable):** breakpoint set including ≥1024px desktop target; in-app theme toggle for multi-page apps.
