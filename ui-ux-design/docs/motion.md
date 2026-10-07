# Motion & Animation Guidelines

> Apple Human Guidelines / Fluent Design System motion principles: motion-on-purpose, consistent timings, reduced-motion fallback, accessibility-first.

## Motion Principles

1. **Motion-on-purpose** — every animation has a semantic purpose:
   - **Draw attention** — highlight new or changed content
   - **Guide focus** — transition between related content
   - **Communicate state change** — indicate loading, completion, or failure
2. **Consistency** — same interaction pattern = same motion timing and easing across the app
3. **Reduced motion** — every animation has a `@media (prefers-reduced-motion: reduce)` fallback
4. **Accessibility** — motion cannot affect tab order, focus management, or screen reader announcements
5. **Performance** — animate transform and opacity only (will-change property); avoid layout/pit properties
6. **Optional** — every motion is optional; the app must be usable without motion

## Motion Timing

Use the token system — never hardcode animation timing values.

| Token | Value | Usage |
|-------|-------|-------|
| `--duration-fast` (48ms) | 48ms | Button press feedback, tooltip visibility, icon color change |
| `--duration-normal` (100ms) | 100ms | Hover transitions, tooltip fade, menu show/hide |
| `--duration-slow` (200ms) | 200ms | Dialog fade, overlay transition, card expansion |
| `--duration-very-slow` (320ms) | 320ms | Full page transitions, hero parallax |

## Motion Easing

| Token | Value | Usage |
|-------|-------|-------|
| `--easing-ease-in` | `cubic-bezier(0, 0, 0, 1)` | Elements entering from bottom (slide up) |
| `--easing-ease-out` | `cubic-bezier(1, 0, 0, 1)` | Elements exiting (slide down) |
| `--easing-ease-in-out` | `cubic-bezier(0, 0, 1, 1)` | Progress bars, loading animations |
| `--easing-linear` | `linear` | Spinner, progress bar (linear) |
| `--easing-bezier-fast` | `cubic-bezier(0.36, 0.01, 1, 0.9)` | Button press feedback (spring-like) |
| `--easing-bezier-spring` | `cubic-bezier(0.25, 1, 0.25, 1.3)` | Checkbox toggle, switch (spring) |
| `--easing-bezier-easy-out` | `cubic-bezier(0, 0.4, 0.6, 1)` | Menu exit (backwards spring) |

## Motion Examples

### Button Press Feedback

```css
.button {
  transition: transform var(--duration-fast) var(--easing-bezier-fast);
}

.button:active {
  transform: scale(0.97);
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

### Tooltip Fade

```css
.tooltip {
  opacity: 0;
  transform: translateY(8px);
  transition: opacity var(--duration-fast) var(--easing-ease-out),
              transform var(--duration-fast) var(--easing-ease-out);
}

.tooltip:hover,
.tooltip:focus-visible {
  opacity: 1;
  transform: translateY(0);
}
```

### Dialog Fade + Scale

```css
.overlay {
  opacity: 0;
  pointer-events: none;
  transition: opacity var(--duration-slow) var(--easing-ease-in-out),
              pointer-events var(--duration-slow) var(--easing-ease-in-out)
}

.overlay.open {
  opacity: 1;
  pointer-events: auto;
}

.dialog {
  transform: scale(0.95);
  transition: transform var(--duration-slow) var(--easing-bezier-spring);
}

.overlay.open .dialog {
  transform: scale(1);
}
```

### Loading Spinner

```css
.spinner {
  width: 24px;
  height: 24px;
  border: 3px solid rgba(255, 255, 255, 0.2);
  border-top-color: currentColor;
  border-radius: 50%;
  animation: spin var(--duration-very-slow) linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(90deg);
  }
  to {
    transform: rotate(0deg);
  }
}

@media (prefers-reduced-motion: reduce) {
  .spinner {
    animation: none;
    opacity: 0.5;
  }
}
```

### Skeleton Loading

```css
.skeleton {
  background: linear-gradient(
    to right,
    var(--color-neutral-900) 0%,
    var(--color-neutral-800) 50%,
    var(--color-neutral-900) 100%
  );
  background-size: 200% 100%;
  background-position: 100% 0;
  animation: shimmer var(--duration-very-slow) infinite;
}

@keyframes shimmer {
  0% {
    background-position: 100% 0;
  }
  50% {
    background-position: 50% 0;
  }
  100% {
    background-position: 0 0;
  }
}
```

### Page Fade

```css
.page {
  opacity: 0;
  transform: translateY(16px);
  transition: opacity var(--duration-slow) var(--easing-ease-out),
              transform var(--duration-slow) var(--easing-ease-out);
}

.page.loaded {
  opacity: 1;
  transform: translateY(0);
}

@media (prefers-reduced-motion: reduce) {
  .page {
    transition: none;
  }
}
```

### Tab Underline

```css
.tab {
  position: relative;
}

.tab::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background-color: var(--color-primary-900);
  transform: scaleX(0);
  transition: transform var(--duration-slow) var(--easing-bezier-easy-out);
}

.tab.active::after {
  transform: scaleX(1);
}
```

### Hero Parallax

```css
.hero {
  background-attachment: fixed;
}

@media (prefers-reduced-motion: reduce) {
  .hero {
    background-attachment: scroll;
  }
}
```

## Motion — Accessibility

Motion must not affect accessibility:

| Accessibility requirement | Motion rule |
|---------------------------|-------------|
| Tab order | Motion must not change tab order |
| Focus | Motion must not steal focus |
| Screen reader | Motion must not affect screen reader announcements |
| Reduced motion | All motions have `@media (prefers-reduced-motion: reduce)` fallback |
| Zoom | Motion must work at 200% zoom |

### Reduced Motion Media Query

```css
@media (prefers-reduced-motion: reduce) {
  /* Disable all animations and transitions */
  .animated {
    animation: none !important;
    transition: none !important;
  }

  /* Or provide a reduced alternative */
  .animated {
    animation-duration: 0ms !important;
    transition-duration: 0ms !important;
  }
}
```

### Prefers-Reduced-Motion Query

```javascript
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (!prefersReducedMotion) {
  // Enable motion
}
```

## Motion Performance

### Animate Transform and Opacity Only

```css
/* Good — fast */
.el {
  transform: translateX(100px);
  opacity: 0;
  transition: transform 200ms, opacity 200ms;
}

/* Bad — slow (triggers layout) */
.el {
  left: 100px;
  top: 100px;
}
```

### will-change Property

```css
.el {
  transition: will-change 200ms;
}
```

### Use `requestAnimationFrame` for JS Animations

```javascript
function animateElement(element, properties) {
  requestAnimationFrame(() => {
    element.style.transition = 'all 200ms';
    Object.entries(properties).forEach(([prop, value]) => {
      element.style[prop] = value;
    });
  });
}
```

## Motion Design Patterns

### Loading State → Content Transition

```css
.loading {
  opacity: 0;
  transition: opacity var(--duration-normal) var(--easing-ease-out);
}

.loading.hidden {
  opacity: 0;
}

.content {
  opacity: 0;
  transform: translateY(8px);
  transition: opacity var(--duration-normal) var(--easing-ease-out),
              transform var(--duration-normal) var(--easing-ease-out);
}

.content.visible {
  opacity: 1;
  transform: translateY(0);
}
```

### Hover Reveal

```css
.card {
  overflow: hidden;
}

.card__overlay {
  opacity: 0;
  transform: translateY(8px);
  transition: opacity var(--duration-normal) var(--easing-ease-out),
              transform var(--duration-normal) var(--easing-ease-out);
}

.card:hover .card__overlay {
  opacity: 1;
  transform: translateY(0);
}
```

### Accordion Expand/Collapse

```css
.accordion__content {
  max-height: 0;
  overflow: hidden;
  transition: max-height var(--duration-slow) var(--easing-ease-in-out);
}

.accordion.open .accordion__content {
  max-height: 500px;
}
```

### Toast Notification Slide-in

```css
.toast {
  transform: translateY(100%);
  opacity: 0;
  transition: transform var(--duration-slow) var(--easing-bezier-easy-out),
              opacity var(--duration-fast) var(--easing-ease-out);
}

.toast.enter {
  transform: translateY(0);
  opacity: 1;
}

.toast.exit {
  transform: translateY(-100%);
  opacity: 0;
}
```

### Scroll Reveal

```css
.reveal {
  opacity: 0;
  transform: translateY(16px);
  transition: opacity var(--duration-normal) var(--easing-ease-out),
              transform var(--duration-normal) var(--easing-ease-out);
}

.reveal.visible {
  opacity: 1;
  transform: translateY(0);
}
```

### Tab Switching

```css
.tab-panel {
  opacity: 0;
  transform: translateY(8px);
  transition: opacity var(--duration-normal) var(--easing-ease-out),
              transform var(--duration-normal) var(--easing-ease-out);
}

.tab-panel.active {
  opacity: 1;
  transform: translateY(0);
}
```
