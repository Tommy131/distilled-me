# Motion & Animation

> Motion-on-purpose, shared timings, reduced-motion fallbacks, transform/opacity first.

## Principles

1. **Purpose** — draw attention, guide focus, or communicate state change.
2. **Consistency** — same interaction → same duration and easing tokens.
3. **Reduced motion** — every animation has a `prefers-reduced-motion` path.
4. **Accessibility** — motion must not steal focus, reorder tab stops, or replace required text status.
5. **Performance** — prefer `transform` and `opacity`; avoid animating layout properties (`top`, `left`, `width`, `height`) when possible.
6. **Optional** — the product remains usable with motion disabled.

## Timing tokens

| Token | Value | Use |
|-------|-------|-----|
| `--duration-fast` | 120ms | Press, icon color, small feedback |
| `--duration-normal` | 200ms | Hover, tooltip, short fade |
| `--duration-slow` | 300ms | Dialog, panel, accordion |
| `--duration-deliberate` | 450ms | Full-view transitions |

## Easing tokens

| Token | Value | Use |
|-------|-------|-----|
| `--easing-standard` | `cubic-bezier(0.2, 0, 0, 1)` | Default UI |
| `--easing-emphasized` | `cubic-bezier(0.3, 0, 0, 1)` | Stronger emphasis |
| `--easing-entrance` | `cubic-bezier(0, 0, 0, 1)` | Elements entering |
| `--easing-exit` | `cubic-bezier(0.3, 0, 1, 1)` | Elements leaving |
| `--easing-linear` | `linear` | Spinners / indeterminate progress |

## Examples

### Press feedback

```css
.button {
  transition: transform var(--duration-fast) var(--easing-standard);
}

.button:active {
  transform: scale(0.98);
}

@media (prefers-reduced-motion: reduce) {
  .button {
    transition: none;
  }
  .button:active {
    transform: none;
  }
}
```

### Tooltip

```css
.tooltip {
  opacity: 0;
  transform: translateY(4px);
  transition:
    opacity var(--duration-normal) var(--easing-exit),
    transform var(--duration-normal) var(--easing-entrance);
}

.tooltip[data-open="true"] {
  opacity: 1;
  transform: translateY(0);
}
```

### Dialog

```css
.overlay {
  opacity: 0;
  pointer-events: none;
  transition: opacity var(--duration-slow) var(--easing-standard);
}

.overlay[data-open="true"] {
  opacity: 1;
  pointer-events: auto;
}

.dialog {
  transform: translateY(8px) scale(0.98);
  transition: transform var(--duration-slow) var(--easing-emphasized);
}

.overlay[data-open="true"] .dialog {
  transform: translateY(0) scale(1);
}
```

### Spinner

```css
.spinner {
  width: 24px;
  height: 24px;
  border: 3px solid rgb(255 255 255 / 0.25);
  border-top-color: currentColor;
  border-radius: 50%;
  animation: spin var(--duration-deliberate) linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (prefers-reduced-motion: reduce) {
  .spinner {
    animation: none;
    border-top-color: currentColor;
    opacity: 0.8;
  }
}
```

### Skeleton shimmer

```css
.skeleton {
  background: linear-gradient(
    90deg,
    var(--color-bg-elevation-2) 0%,
    var(--color-bg-elevation-1) 50%,
    var(--color-bg-elevation-2) 100%
  );
  background-size: 200% 100%;
  animation: shimmer var(--duration-deliberate) linear infinite;
}

@keyframes shimmer {
  to {
    background-position: -200% 0;
  }
}

@media (prefers-reduced-motion: reduce) {
  .skeleton {
    animation: none;
  }
}
```

## Reduced motion (global fallback)

Also provided in `assets/tokens.css`:

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

Prefer component-level fallbacks when a reduced alternative (instant state swap, opacity-only) is better than disabling everything.

```js
const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
```

## Performance

**Good:** animate `transform`, `opacity`.

**Avoid when possible:** `top` / `left` / `width` / `height` for continuous animation.

**`will-change`:** set sparingly on elements about to animate, then remove — do **not** write `transition: will-change …`.

```css
.dialog-entering {
  will-change: transform, opacity;
}
.dialog-settled {
  will-change: auto;
}
```

JS-driven motion: use `requestAnimationFrame`; prefer Web Animations API or CSS when sufficient.

## Patterns to prefer / avoid

| Prefer | Avoid |
|--------|--------|
| Short feedback on press | Multi-second blocking intros |
| Opacity + transform page enter | Parallax that breaks reduced-motion users |
| Accordion with `grid-template-rows` / measured height | Huge fixed `max-height` jumps that feel laggy |
| Toast slide with reduced-motion = fade/appear | Motion as the only way to notice an error |

Accordion note: animating `max-height` to a large constant works but is imprecise; measuring content height or using modern grid 0fr/1fr patterns is better when browser support allows.

## Accessibility matrix

| Requirement | Motion rule |
|-------------|-------------|
| Tab order | Unchanged by animation |
| Focus | Do not move focus solely for decoration |
| Screen reader | Status text / live regions carry the meaning |
| Reduced motion | Fallback required |
| Zoom | Motion still usable at 200% zoom |
