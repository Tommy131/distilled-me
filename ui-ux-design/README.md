# UI/UX Design System (OwO)

OwO-distilled design system: Flutter `AppThemeData` + Flight Middleware web CSS variables, with Studio / Exam / WinDeploy accent variants. WCAG 2.2 AA, flat bordered cards, sidebar/bottom-nav shells.

## Usage

Invoke via `/ui-ux-design` or ask for OwO theming / design-system / a11y work. Load `SKILL.md`, then only the needed `docs/` files.

## Documentation

| Topic | Document |
|-------|----------|
| Source projects & presets | `docs/owo-sources.md` |
| Design tokens | `docs/design-system.md` |
| Copy-ready CSS | `assets/tokens.css` |
| Layout shells | `docs/layout.md` |
| Components | `docs/components.md` |
| Accessibility | `docs/accessibility.md` |
| Motion | `docs/motion.md` |
| Process | `docs/design-process.md` |
| Testing | `docs/testing.md` |

## Quick Start

1. Copy `assets/tokens.css` (or mirror Flutter `AppThemeData` / web `generateThemeTokens`).
2. Pick shell: desktop sidebar, mobile bottom nav, or topbar tool layout (`docs/layout.md`).
3. Build flat bordered components (`docs/components.md`).
4. Verify WCAG 2.2 AA (`docs/accessibility.md` + axe-core).
5. Use 300ms default motion with reduced-motion fallbacks.

## Defaults

- Brand triad: `#6C5CE7` / `#A29BFE` / `#00B894` (override per product).
- Space 8/16/24/32 · radius 8/12/16 · anim 300ms.
- Light `#F5F6FA`/`#FFFFFF` · dark `#1A1A2E`/`#16213E`.
