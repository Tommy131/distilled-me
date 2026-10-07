# Layout — Responsive & Adaptive

> Container-based layout, shared breakpoints, mobile-usable floors. Trim the breakpoint set in project docs when the product is mobile-only or embedded.

## Breakpoints (defaults)

| Breakpoint | Role | Required by default |
|------------|------|---------------------|
| `320px` | Narrow mobile floor | Yes |
| `480px` | Phone | Yes |
| `768px` | Tablet | Yes |
| `1024px` | Desktop | Yes (default desktop target) |
| `1280px` | Large desktop / content max | Optional |
| `1440px` | Wide display | Optional |

**Rules:**

- Design so primary flows work at **320px** width without horizontal scrolling.
- Desktop layouts SHOULD be verified at **≥1024px**.
- Mobile-only apps MAY omit 1024+ verification — declare in design docs.
- Embedded widgets MAY use container queries instead of viewport breakpoints.

## Container

```css
.container {
  width: 100%;
  max-width: 80rem; /* ~1280px */
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

## Page padding

```css
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

## CSS Grid

```css
.grid {
  display: grid;
  gap: var(--space-4);
  grid-template-columns: 1fr;
}

@media (min-width: 480px) {
  .grid--2 {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 768px) {
  .grid--3 {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (min-width: 1024px) {
  .grid--4 {
    grid-template-columns: repeat(4, 1fr);
  }
}
```

## Flexbox

```css
.flex {
  display: flex;
  gap: var(--space-4);
}

.flex--wrap {
  flex-wrap: wrap;
}

.flex__item {
  min-width: 0; /* prevent overflow */
}
```

Patterns: sticky footer (`flex` column + `flex: 1` main), equal-height columns (`flex: 1 1 0`), centered shells.

## Principles

1. **Content first** — base styles fit small screens; enhance upward.
2. **No horizontal scroll** on primary mobile flows.
3. **Test real breakpoints** — 320 / 480 / 768 / 1024 / 1280 as applicable.
4. **`clamp()` for fluid type/spacing** when it stays readable.
5. **Max content width** — do not stretch prose to full ultrawide.
6. Prefer **container queries** for component-level adaptation:

```css
.card-panel {
  container-type: inline-size;
}

@container (min-width: 480px) {
  .card-panel__body {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--space-4);
  }
}
```

## Fluid type (example)

```css
.fluid-heading {
  font-family: var(--font-family-sans);
  font-weight: var(--font-weight-bold);
  font-size: clamp(var(--font-size-heading), 2vw + 1rem, 2.5rem);
  line-height: var(--line-height-heading);
}
```

Do not pass typography tokens that are not lengths into `clamp()` incorrectly — use size tokens that resolve to `rem`/`px`.

## Responsive type scale (defaults)

| Breakpoint | H1 | H2 | H3 | Body | Label | Caption |
|------------|----|----|----|------|-------|---------|
| 320px | 32px | 24px | 20px | 16px | 14px | 12px |
| 768px | 40px | 28px | 24px | 16px | 14px | 12px |
| 1024px | 48px | 32px | 28px | 16px | 14px | 12px |
| 1280px | 56px | 36px | 28px | 18px | 14px | 12px |

Body text SHOULD stay ≥16px for readable web UI unless a constrained native shell documents otherwise.

## Images

```css
img {
  max-width: 100%;
  height: auto;
}

.hero-image {
  width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: cover;
}
```

Reserve space with `aspect-ratio` or width/height attributes to limit CLS.
