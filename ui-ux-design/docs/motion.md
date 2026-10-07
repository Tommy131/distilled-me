# Motion — OwO

> Default interaction duration is **300ms** (`--anim-duration`), matching Flutter `AppThemeData.animationDuration` and Flight web. Keep motion optional and purposeful.

## Principles

1. Purpose: attention, focus guidance, or state change.
2. Same interaction → same duration/easing.
3. Always provide `prefers-reduced-motion` fallbacks.
4. Prefer `transform` / `opacity`.
5. Motion must not steal focus or replace required text status.

## Timing

| Token | Value | Use |
|-------|-------|-----|
| `--duration-fast` | 150ms | Press scale, icon color |
| `--duration-normal` | 220ms | Sidebar collapse micro-interactions |
| `--duration-slow` / `--anim-duration` | **300ms** | Default UI, theme transitions, nav selection |
| `--duration-deliberate` | 450ms | Large page / hero |

Curves: `--easing-standard` (Material-like ease), `--easing-emphasized` for stronger state changes. Flutter often uses `easeInOut` / `easeOutCubic`.

## Patterns

### Press

```css
.button {
  transition: transform var(--duration-fast) var(--easing-standard);
}
.button:active {
  transform: scale(0.98);
}
```

### Nav selection

Selected bottom-nav / sidebar icon: animate scale to ~1.1 and color to primary over `--anim-duration`.

### Sidebar width

Animate width between `--sidebar-expanded` and `--sidebar-collapsed` (~220–300ms). Content reflow should not jump focus.

### Theme switch

Token swap may be instant; if fading chrome, keep ≤300ms and respect reduced motion.

## Reduced motion

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

Flight web also keeps a `.motion-essential` escape for tiny opacity cues when fully disabling motion would hide state — prefer explicit state text over relying on that.

## Performance

- Animate transform/opacity; avoid layout thrash.
- `will-change` only while animating, then reset — never `transition: will-change`.
