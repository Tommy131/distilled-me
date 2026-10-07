# Layout — OwO responsive shells

> Distilled from Flutter `DesktopLayout` / `MobileLayout` and Flight Middleware web sidebar + bottom nav. Tokens: `assets/tokens.css`.

## Breakpoints (OwO shell)

| Range | Role | Shell |
|-------|------|-------|
| `< 650px` (`--bp-mobile-max`) | Mobile | AppBar + content + **bottom nav** (optional module drawer) |
| `650–1241px` | Tablet | Prefer desktop shell if width allows; else mobile |
| `≥ 1242px` (`--bp-desktop-min`) | Desktop | **Collapsible sidebar** + AppBar + content |

Also honor:

- `--desktop-min-content-width: 1000px` — below this, desktop content may scroll horizontally rather than crush chrome
- Narrow phone `< 360px` — bottom nav shows fewer primary slots + “More”

General web content max: `--content-max: 1100px` (Exam/Studio centered tools). Wide workspaces (Studio) MAY use up to ~1760px — declare in product docs.

## Desktop shell

```
┌────────────┬─────────────────────────────┐
│  Sidebar   │  AppBar                     │
│  200 / 60  ├─────────────────────────────┤
│            │  Module content             │
│            │  (min content ~1000)        │
└────────────┴─────────────────────────────┘
```

| Metric | Token / value |
|--------|----------------|
| Expanded sidebar | `--sidebar-expanded` **200px** |
| Collapsed sidebar | `--sidebar-collapsed` **60px** |
| Header / AppBar row | `--header-height` **56px** |
| Nav icon | ~20px |
| Logo | ~32px |

Sidebar: module registry driven; selected item uses primary tint (`--color-primary-a10`) + primary icon/label. Collapse animation ~220–300ms.

WinDeploy uses the same **200px** left rail idea with light-first desktop chrome.

## Mobile shell

```
┌─────────────────────┐
│ AppBar (+ drawer)   │
├─────────────────────┤
│ Content             │
├─────────────────────┤
│ Bottom nav (≤5)     │
└─────────────────────┘
```

- Bottom bar: 4–5 primary destinations; overflow into “More”
- Module-specific side menus → left drawer, not extra bottom tabs
- Selected item: primary color + slight scale (~1.1); unselected: text secondary
- Optional top shadow `--shadow-chrome`

## Topbar shell (tooling apps)

Exam Trainer / parts of Studio use **sticky topbar + centered content** instead of sidebar:

- Topbar: brand + nav links + actions; `position: sticky`
- Content: `max-width: 1100px` (or product-specific), padding `--space-md`–`lg`
- Prefer **container queries** when a docked AI panel steals viewport width (Exam)

## Page padding

Default: `--space-md` (16) all around. Hero / settings sections: `--space-lg` (24).

## Grid

- Cards: CSS grid / Flutter wrap; 2-col under ~800, 4-col when wide (dashboard home pattern)
- Lists: single column with bordered group containers
- `min-width: 0` on flex children to prevent overflow
- App shell: `overflow: hidden` on body; scroll inside panes (Flight web)

## Cards and surfaces

See `docs/components.md`. Layout rule: cards sit on `--color-background` with `--color-surface` fill — never nest heavy elevation.

## Images

Reserve space with `aspect-ratio` or fixed height to avoid CLS. `max-width: 100%`.
