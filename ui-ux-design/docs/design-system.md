# Design System — OwO tokens

> Distilled from OwO Flutter `AppThemeData` and Flight Middleware web `generateThemeTokens`. Copy `assets/tokens.css`. Provenance: `docs/owo-sources.md`.

## Token layers

```
Brand triad (primary / secondary / accent)
  → Surfaces + text + border (light/dark)
    → Semantic status (success / warning / danger / delay buckets)
      → Component recipes (cards, buttons, nav)
```

Components use **semantic** CSS variables (or Flutter `Theme.of` / `AppThemeData` helpers). Never hardcode hex in feature widgets.

## Brand triad

Every OwO shell theme is a **primary + secondary + accent** triad. Default product brand is **默认紫**:

| Token | Default |
|-------|---------|
| `--color-primary` | `#6C5CE7` |
| `--color-secondary` | `#A29BFE` |
| `--color-accent` | `#00B894` (also success) |
| `--color-on-primary` | luminance-based contrast (white on purple) |

Presets and custom themes only swap the triad; surfaces/text stay shared. See `docs/owo-sources.md` for the six Flutter presets.

Product overrides: `[data-product="studio"|"exam"|"win-deploy"]` in `assets/tokens.css`.

## Surfaces and text

| Role | Light | Dark (Flight night) |
|------|-------|---------------------|
| Background | `#F5F6FA` | `#1A1A2E` |
| Surface / card | `#FFFFFF` | `#16213E` |
| Text primary | `#2D3436` | `#DFE6E9` |
| Text secondary | `#636E72` | `#B2BEC3` |
| Border | `#DFE6E9` | `#2D3436` |

Theme modes: **system / light / dark**. Optional contrast slider lerps light surfaces toward black and dark surfaces toward `#050505` / `#0A0A15` (Flutter + Web Flight).

## Semantic / status

| Token | Value | Use |
|-------|-------|-----|
| `--color-success` / accent | `#00B894` | Success snackbars, positive accent |
| `--color-warning` | `#FF9800` | Warnings |
| `--color-danger` / error | `#E53935` / `#F44336` | Errors, destructive |
| `--color-status-ok` | `#2DB87A` | On-time / healthy (BahnKlar) |
| `--color-status-caution` | `#F5A623` | Minor delay / degraded |
| `--color-status-critical` | `#E53935` | Major delay / failed |
| `--color-status-neutral` | `#9E9E9E` | Unknown / cancelled |

Prefer status tokens over ad hoc `Colors.orange` in domain modules.

## Spacing (8-pt)

| Token | px | Typical use |
|-------|-----|-------------|
| `--space-xs` | 4 | Hair gaps, chip pad |
| `--space-sm` | 8 | Compact gaps |
| `--space-md` | 16 | **Default page / card padding** |
| `--space-lg` | 24 | Section gaps, button horizontal pad |
| `--space-xl` | 32 | Hero / page outer |

## Radius

| Token | px | Use |
|-------|-----|-----|
| `--radius-sm` | 8 | Elevated buttons, icon wells, inputs |
| `--radius-md` | 12 | **Cards**, popups |
| `--radius-lg` | 16 | Drawers, outlined buttons, hero cards |
| `--radius-pill` | 999 | Chips / pills |

## Typography

**Stack:** Noto Sans SC (UI) + Microsoft YaHei (titles / AppBar) + system UI. Mono: JetBrains / Cascadia / SF Mono for data.

| Role | Size | Weight | Notes |
|------|------|--------|-------|
| Display LG | 32 | 700 | |
| Display MD | 28 | 700 | |
| Display SM | 24 | 600 | |
| Headline | 20 | 600 | AppBar title often YaHei 20/600 |
| Title | 14 | 600 | YaHei for titleSmall |
| Body LG | 16 | 400 | Primary text |
| Body | 14 | 400 | Default UI; secondary color for body MD |
| Label | 12 | 400 | |
| Caption | 11 | 400 | |

Body line-height ≈ **1.5**. Use longhands (`font-family`, `font-size`, `line-height`, `font-weight`) — never fake `font-family` shorthand bags.

CSS utility names in Flight web: `.text-display-lg` … `.text-caption`, `.text-mono`.

## Elevation philosophy

- Cards / lists: **elevation 0** + 1px `--color-border` + `--radius-md`
- Soft shadow only for chrome, drawers, hero gradients
- Prefer border over Material elevation for density and theme stability

## Theming rules

1. No magic hex in components — tokens or theme helpers only.
2. Light and dark must both resolve every semantic color used.
3. `on-primary` from luminance (`> 0.5` → dark text).
4. Persist theme mode + selected preset (and custom triad) like Flutter `theme_provider` / web `theme-store`.
5. In-app theme settings page is default for shell apps; dark-only tools (Studio/Exam) document that choice.

## Flutter ↔ Web parity

| Flutter | Web CSS |
|---------|---------|
| `AppThemeData.primaryColor` | `--color-primary` |
| `spacingMedium` | `--space-md` |
| `borderRadiusMedium` | `--radius-md` |
| `animationDuration` | `--anim-duration` (300ms) |
| `getBorderColor(theme)` | `--color-border` |
| `getTextColor(theme)` | `--color-text-primary` / secondary |
| `sidebarExpandedWidth` | `--sidebar-expanded` |
