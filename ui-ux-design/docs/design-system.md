# Design System — Tokens & Architecture

> Tokens over magic values. Components use **semantic** tokens; themes remap primitives. Start from `assets/tokens.css`.

## Token layers

```
Primitives (palette, raw sizes)
    → Semantic tokens (intent: text, surface, border, focus)
        → Component tokens (optional: --button-primary-bg)
            → Themes (light / dark / system)
```

### Layer 1 — Primitives

Raw palette and scales. Prefer not to reference these in components.

### Layer 2 — Semantic tokens (required in components)

```css
color: var(--color-text-primary);
background: var(--color-bg-surface);
border-color: var(--color-border-default);
box-shadow: 0 0 0 2px var(--color-focus-ring);
padding: var(--space-3) var(--space-4);
font-family: var(--font-family-sans);
font-size: var(--font-size-body);
line-height: var(--line-height-body);
font-weight: var(--font-weight-regular);
transition: opacity var(--duration-normal) var(--easing-standard);
```

### Layer 3 — Component tokens (optional)

Use when the same control needs many states:

```css
--button-primary-bg: var(--color-bg-primary);
--button-primary-bg-hover: var(--palette-primary-800);
--button-primary-fg: var(--color-text-on-primary);
```

### Layer 4 — Themes

- Default light values on `:root`.
- Dark via `[data-theme="dark"]` (and optional system preference when no explicit `data-theme="light"`).
- Every semantic color MUST resolve in both themes with sufficient contrast.

**Default product rule:** honor `prefers-color-scheme`, allow user override via `data-theme`. In-app toggle is default for multi-page apps; omit only when documented (marketing page, OS-native chrome, etc.).

## Typography (correct CSS)

Do **not** cram family/size/weight into one invalid `font-family` string. Use longhands:

```css
.heading {
  font-family: var(--font-family-sans);
  font-size: var(--font-size-heading);
  line-height: var(--line-height-heading);
  font-weight: var(--font-weight-bold);
}
```

| Role | Size token | Weight | Typical use |
|------|------------|--------|-------------|
| Display | `--font-size-display` | bold | Hero / marketing |
| Heading | `--font-size-heading` | bold / semibold | Page/section titles |
| Body | `--font-size-body` | regular | Paragraphs |
| Label | `--font-size-label` | semibold | Controls, forms |
| Caption | `--font-size-caption` | regular | Hints, metadata |

Scale sizes per breakpoint in `docs/layout.md` with `clamp()` or media queries.

## Spacing

4px grid. `--space-1` (2px) is only for hairlines/alignment tweaks.

| Token | Value |
|-------|-------|
| `--space-0` … `--space-10` | 0, 2, 4, 8, 12, 16, 24, 32, 40, 48, 64 px |

## Motion tokens

| Token | Default | Use |
|-------|---------|-----|
| `--duration-fast` | 120ms | Press feedback, small color changes |
| `--duration-normal` | 200ms | Hover, tooltips, short fades |
| `--duration-slow` | 300ms | Panels, dialogs |
| `--duration-deliberate` | 450ms | Large page transitions |
| `--easing-standard` | `cubic-bezier(0.2, 0, 0, 1)` | Most UI |
| `--easing-emphasized` | `cubic-bezier(0.3, 0, 0, 1)` | Important state changes |
| `--easing-entrance` | `cubic-bezier(0, 0, 0, 1)` | Entering elements |
| `--easing-exit` | `cubic-bezier(0.3, 0, 1, 1)` | Exiting elements |

## Token rules

1. No magic values in component styles — colors, spacing, radii, durations via tokens.
2. Components use semantic (or component) tokens, not raw palette — unless building the theme layer itself.
3. Names encode intent: `--color-text-secondary`, not `--gray-2`.
4. Dark variants required for every semantic color used in UI.
5. Changing a primitive should cascade through semantics; document breaking token renames.
6. Ship `assets/tokens.css` (or generated equivalent) as the single source in the repo.

## Minimal JSON schema (optional tooling)

```json
{
  "color": {
    "text": {
      "primary": { "light": "#1D1D1D", "dark": "#F2F2F2" }
    }
  },
  "space": { "3": "8px", "5": "16px" },
  "fontSize": { "body": "1rem", "heading": "1.5rem" },
  "duration": { "normal": "200ms" }
}
```

Keep CSS variables as the runtime source of truth unless the project already uses Style Dictionary / Tokens Studio — then generate `tokens.css` in CI.

## Summary

1. User or system sets theme → `data-theme` / `color-scheme` updates.
2. Semantic tokens resolve to theme-specific primitives.
3. Components read semantics only — no per-component hard-coded theme forks.
