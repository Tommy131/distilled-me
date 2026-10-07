# Layout System — Responsive & Adaptive Design

> Apple Human Guidelines / Fluent Design System layout principles: container-based responsive design, grid system, breakpoint-driven layouts, and a strict minimum-width requirement.

## Breakpoints

| Breakpoint | Device | Minimum | Notes |
|------------|--------|---------|-------|
| `320px` | Narrow mobile | ✅ Required | Max horizontal padding ≤ `--space-4` (12px) |
| `480px` | Standard mobile | ✅ Required | Small screens |
| `768px` | Tablet | ✅ Required | Medium screens |
| `1000px` | Desktop | ✅ Required | Desktop minimum — all components must work at ≥1000px |
| `1280px` | Large desktop | Optional | Max-width container |
| `1440px` | Large display | Optional | No max-width |

**Rule**: Every component must be designed for ≥320px width and ≥1000px width. Below 320px is acceptable but not required. Below 1000px desktop components may degrade but must be usable.

## Container System

### Max-width Container

```css
/* Container — center content with max-width */
.container {
  width: 100%;
  max-width: 1440px;
  margin-inline: auto;
  padding-inline: var(--space-5);
}
@media (min-width: 768px) {
  .container {
    padding-inline: var(--space-6);
  }
}
@media (min-width: 1280px) {
  .container {
    padding-inline: var(--space-7);
  }
}
```

### Page Padding

```css
/* Page padding — responsive */
.page {
  padding-block: var(--space-5);
  padding-inline: var(--space-4);
}
@media (min-width: 768px) {
  .page {
    padding-block: var(--space-6);
    padding-inline: var(--space-5);
  }
}
@media (min-width: 1280px) {
  .page {
    padding-block: var(--space-7);
    padding-inline: var(--space-6);
  }
}
```

## Grid System

### CSS Grid

```css
/* Responsive grid */
.grid {
  display: grid;
  gap: var(--space-4);
}

/* Mobile: 1 column */
.grid--1col {
  grid-template-columns: 1fr;
}
@media (min-width: 480px) {
  .grid--2col {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (min-width: 768px) {
  .grid--3col {
    grid-template-columns: repeat(3, 1fr);
  }
}
@media (min-width: 1000px) {
  .grid--4col {
    grid-template-columns: repeat(4, 1fr);
  }
}
@media (min-width: 1280px) {
  .grid--5col {
    grid-template-columns: repeat(5, 1fr);
  }
}

/* Custom spans */
.col-span-2 {
  grid-column: span 2 / span 2;
}
@media (min-width: 768px) {
  .col-span-2 {
    grid-column: span 2 / span 2;
  }
}
```

### CSS Flexbox

```css
/* Flexbox layout */
.flex {
  display: flex;
}

.flex--row {
  flex-direction: row;
}
.flex--col {
  flex-direction: column;
}
@media (min-width: 768px) {
  .flex--row {
    flex-direction: row;
  }
  .flex--col {
    flex-direction: column;
  }
}

/* Alignment */
.flex--center {
  align-items: center;
}
.flex--between {
  justify-content: space-between;
}
.flex--end {
  justify-content: flex-end;
}

/* Wrap */
.flex--wrap {
  flex-wrap: wrap;
}
.flex--nowrap {
  flex-wrap: nowrap;
}
```

## Flexbox Layout Patterns

### Centered Content

```css
/* Centered content */
.content-centered {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}
```

### Sticky Footer

```css
/* Sticky footer */
.layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
.layout__content {
  flex-grow: 1;
}
.layout__footer {
  flex-shrink: 0;
}
```

### Equal-height Columns

```css
/* Equal-height columns — flex */
.columns {
  display: flex;
}
.columns__col {
  flex: 1 1 0;
  min-width: 0;
}
@media (min-width: 768px) {
  .columns {
    flex-direction: row;
  }
}
```

## Flexbox Principles

1. **Use flex for layout** — never for alignment alone (CSS align-self/align-items for alignment).
2. **No flex-basis tricks** — use flex: 1 1 0 or flex: 1 1 0% for equal distribution.
3. **Min-width: 0 on flex children** — prevents flex child from being wider than its content.
4. **Wrap on small screens** — use flex-wrap: wrap for horizontal layouts that stack on narrow screens.

## CSS Grid Principles

1. **Grid for complex layouts** — multi-column, multi-row, spanning.
2. **Auto-fill vs auto-fit** — use `repeat()` (repeat-fill) for fixed columns, `auto-fill` for flexible columns.
3. **Don't nest grids** — if you need nested grids, you're designing a component, not a layout.
4. **Grid gaps** — always use `gap`, never margin for inter-grid spacing.

## Responsive Design Principles

1. **Content-first** — design for the smallest screen first, then expand. Never scale up.
2. **Progressive enhancement** — mobile is the base; desktop features are progressive enhancements.
3. **No shrinking below 320px** — design for a minimum content width of 320px.
4. **No horizontal scrolling on mobile** — content must fit within the viewport.
5. **Test at real breakpoints** — 320px, 480px, 768px, 1000px, 1280px. Use Chrome DevTools Device Emulation.
6. **No CSS media queries below 320px** — no `@media (max-width: 280px)` or similar.
7. **Use `clamp()` for fluid values** — `padding: clamp(var(--space-4), 4vw, var(--space-6))`.
8. **Content width constraint** — never stretch content to fill the viewport. Always max-width.

## Fluid Typography

```css
/* Fluid typography — scales between mobile and desktop */
.fluid-text {
  font-size: clamp(
    var(--font-body),     /* minimum — mobile */
    calc(16px + 2vw),     /* variable — scales with viewport */
    var(--font-heading)    /* maximum — desktop */
  );
}
```

## Responsive Images

```css
/* Responsive images */
img {
  width: 100%;
  height: auto;
  object-fit: contain;
}

/* Cover for hero images */
.hero-image {
  width: 100%;
  height: 320px;
  object-fit: cover;
}
@media (min-width: 768px) {
  .hero-image {
    height: 480px;
  }
}

/* Responsive image sources */
img {
  object-fit: contain;
}
@media (min-width: 768px) {
  img {
    object-fit: contain;
  }
}
```

## Responsive Typography Scales

| Breakpoint | H1 | H2 | H3 | Body | Label | Caption |
|------------|---|---|---|---|---|---|
| 320px | 32px | 24px | 20px | 14px | 12px | 10px |
| 480px | 40px | 28px | 24px | 16px | 14px | 12px |
| 768px | 48px | 32px | 28px | 16px | 14px | 12px |
| 1000px | 64px | 40px | 32px | 16px | 14px | 12px |
| 1280px | 72px | 48px | 36px | 18px | 14px | 12px |

Use `clamp()` for fluid scaling between breakpoints, not `@media` queries for every step.

## Container Queries

```css
/* Container query — component adapts to container size */
@container (min-width: 480px) {
  .component {
    display: grid;
    grid-template-columns: 1fr 1fr;
  }
}
```

Container queries are preferred over media queries for component-level responsive behavior, as they respond to actual container size, not viewport size.
