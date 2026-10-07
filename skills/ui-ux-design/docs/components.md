# Component patterns — OwO

> Flat bordered surfaces, primary triad, explicit states. Align with Flutter themes and Flight web CSS modules.

## State machines

Interactive controls expose explicit states (`idle` / `loading` / `disabled` / `success` / `error`). Every user-visible state needs an accurate accessible name.

## Surface card

OwO default card = **no elevation** + border + medium radius:

```css
.card {
  background: var(--color-surface);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-md);
  box-shadow: none; /* optional: var(--shadow-card) for hero only */
}
```

**Hero / welcome card:** primary→secondary gradient, `--radius-lg`, soft primary-tinted shadow.

**Icon well:** `--color-primary-a10` fill, `--radius-sm`, icon ~24px.

**List group:** bordered container + separators using `--color-border` (1px `Divider`).

## Buttons

| Variant | Recipe |
|---------|--------|
| Primary / elevated | `--color-primary` fill, `--color-on-primary` text, pad 24×12, `--radius-sm`, elevation 0 |
| Outlined | surface fill, primary text, secondary stroke ~1.8px, **`--radius-lg`** |
| Ghost / tertiary | transparent + border `--color-border`; hover border→primary |
| Destructive | danger text/border or danger fill; confirm before irreversible actions |
| Loading | `aria-busy="true"`, disabled pointer, spinner; keep accessible name |

```css
.button--primary {
  background: var(--color-primary);
  color: var(--color-on-primary);
  border: none;
  padding: 12px 24px;
  border-radius: var(--radius-sm);
  font-weight: var(--font-weight-semibold);
  transition: background-color var(--anim-duration) var(--easing-standard),
    transform var(--duration-fast) var(--easing-standard);
}
.button--primary:active {
  transform: scale(0.98);
}
```

## Form inputs

| State | Tokens |
|-------|--------|
| Default | border `--color-border`, text primary, surface fill |
| Focus | focus ring `--color-focus-ring` / outline primary@0.3 |
| Invalid | border / text `--color-danger`; `aria-invalid` + `aria-describedby` |
| Disabled | muted text; `disabled` attribute |

Radius: `--radius-sm` (8). Padding comfortable (~8–12 vertical).

## Navigation

### Desktop sidebar

- Width 200 / 60; selected = primary + `--color-primary-a10` well
- Semantics / `aria-label` on nav region
- Collapse control in header

### Mobile bottom nav

- ≤5 slots; selected primary + scale; unselected secondary text
- “More” overflow sheet/menu for extra modules

### Topbar (Exam / Studio)

- Text links; `.active` uses elevated surface
- Sticky; wrap on narrow containers

## Feedback

| Kind | Color |
|------|-------|
| Success | `--color-success` (`#00B894`) |
| Warning | `--color-warning` |
| Error | `--color-danger` / error |
| Info | `--color-primary` |

Snackbars / toasts: short, actionable; don’t rely on color alone.

## Status chips (domain)

Prefer shared status tokens (BahnKlar delay model):

| Status | Token |
|--------|-------|
| OK / on-time | `--color-status-ok` |
| Caution / minor | `--color-status-caution` |
| Critical / major | `--color-status-critical` |
| Neutral | `--color-status-neutral` |

Chip outline: primary@0.4 light / 0.5 dark (BahnKlar `chipTheme` lesson — avoid near-black M3 defaults).

## Data views — three states

Every list/detail MUST design **loading / empty / error** (skeleton or progress; empty CTA; retry). Match software-engineering UI 三态基线.

## Tables / lists

- Mobile: stacked cards or horizontal scroll for wide tables — pick one per product
- Virtualize very large lists
- Mono + tabular nums for telemetry (`.text-mono`)

## Dialogs

Focus trap, Escape closes, restore focus, `aria-modal="true"`. Flight web often uses SweetAlert2 — still must meet focus/label rules.

## Documentation checklist

Props, states, a11y, responsive behavior, token usage, examples. Process: `docs/design-process.md`.
