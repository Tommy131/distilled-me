---
name: ui-ux-design
description: >
  Design, implement, and review UI/UX with the OwO token-driven design system (Flutter
  AppThemeData / Flight web CSS vars), WCAG 2.2 AA, responsive shells (sidebar 200/60,
  mobile bottom nav), and motion-on-purpose. Use when designing components or screens,
  writing CSS/Tailwind/Flutter themes, establishing a design system, reviewing a11y or
  theming, or working on OwO apps (dashboard, flight assistant, bahnklar, middleware web,
  ai-studio, exam-trainer, win-deploy). Prefer this for systemized UI/a11y; use a general
  frontend-design skill for one-off visual styling without design-system workflow.
---

# OwO Design System & UX Specification

Token-driven UI distilled from OwO products (Flutter shells + Flight web port + Studio/Exam/WinDeploy variants). WCAG 2.2 AA, flat bordered surfaces, primary triad theming, sidebar/bottom-nav shells.

**Never apply component changes ad hoc.** Follow `docs/design-process.md` unless the user asks for a quick one-off tweak. Provenance: `docs/owo-sources.md`.

## Workflow Overview

| Phase | Load |
|-------|------|
| OwO tokens & theming | `docs/design-system.md` + `assets/tokens.css` |
| Layout shells & breakpoints | `docs/layout.md` |
| Component recipes | `docs/components.md` |
| Accessibility (WCAG 2.2 AA) | `docs/accessibility.md` |
| Motion | `docs/motion.md` |
| Design process | `docs/design-process.md` |
| Testing & QA | `docs/testing.md` |
| Source map | `docs/owo-sources.md` |

Load only what the task needs.

## Guardrails

### Always

1. **No accessibility bypass** — visible `:focus-visible`, logical tab order, correct names/roles; zero critical `axe-core` issues on changed UI.
2. **No layout shift on load** — reserve space before late content.
3. **Motion optional** — `prefers-reduced-motion` fallbacks; motion must not break focus or SR announcements.
4. **Tokens only** — no raw hex/spacing/type in components; use `assets/tokens.css` or Flutter `AppThemeData` helpers.

### OwO defaults (trim only if documented)

5. **Shell breakpoints** — mobile `<650`, desktop `≥1242`; desktop min content ~1000px; sidebar 200/60.
6. **Theme** — system/light/dark + primary triad presets for shell apps; dark-only tools (Studio/Exam) set `[data-product]` and document it.
7. **Surfaces** — flat cards (elevation 0 + 1px border + radius 12).

## Quick Reference: OwO tokens

```css
/* Brand triad (默认紫) */
--color-primary: #6C5CE7;
--color-secondary: #A29BFE;
--color-accent: #00B894;

/* Surfaces light → dark */
--color-background: #F5F6FA; /* dark #1A1A2E */
--color-surface: #FFFFFF;    /* dark #16213E */
--color-text-primary / --color-text-secondary
--color-border

/* Space / radius / motion */
--space-sm: 8px; --space-md: 16px; --space-lg: 24px; --space-xl: 32px;
--radius-sm: 8px; --radius-md: 12px; --radius-lg: 16px;
--anim-duration: 300ms;

/* Chrome */
--sidebar-expanded: 200px; --sidebar-collapsed: 60px;
--bp-mobile-max: 649px; --bp-desktop-min: 1242px;
```

Product accents: `[data-product="studio"|"exam"|"win-deploy"]`. Full file: `assets/tokens.css`.

## Quick Reference: Type

| Role | Size | Notes |
|------|------|-------|
| Display | 32 / 28 / 24 | Noto Sans SC, bold/semibold |
| Headline / AppBar | 20 | Often Microsoft YaHei |
| Body | 16 / 14 | Default UI 14, lh 1.5 |
| Label / caption | 12 / 11 | |
| Mono | JetBrains / Cascadia | Telemetry & code |

## Quick Reference: WCAG 2.2 AA

Keyboard operable · focus visible · order matches reading · name/role/value · contrast 4.5:1 text · images `alt` · one `h1` · `lang` · target size · status messages. Details: `docs/accessibility.md`.

## Quick Reference: Shells

| Viewport | Pattern |
|----------|---------|
| Mobile | AppBar + content + bottom nav (≤5) + optional drawer |
| Desktop | Collapsible sidebar 200/60 + AppBar + content |
| Tools | Sticky topbar + max-width content (Exam/Studio) |

## Additional Resources

- [owo-sources.md](docs/owo-sources.md) — distillation sources & presets
- [design-system.md](docs/design-system.md) — token architecture
- [assets/tokens.css](assets/tokens.css) — copy-ready CSS
- [layout.md](docs/layout.md) · [components.md](docs/components.md) · [motion.md](docs/motion.md)
- [accessibility.md](docs/accessibility.md) · [design-process.md](docs/design-process.md) · [testing.md](docs/testing.md)
