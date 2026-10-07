# Component Design Patterns

> Explicit state machines, accessible by default, responsive from the start, theme via tokens only.

## State machine pattern

Every interactive component has explicit states and transitions — no ad hoc boolean soup without a model.

```ts
type ButtonState = "idle" | "loading" | "disabled" | "success" | "error";

const buttonCopy: Record<ButtonState, { label: string; accessibleLabel: string; disabled: boolean }> = {
  idle: { label: "Submit", accessibleLabel: "Submit form", disabled: false },
  loading: { label: "Submitting…", accessibleLabel: "Submitting form, please wait", disabled: true },
  disabled: { label: "Submit", accessibleLabel: "Submit form, disabled", disabled: true },
  success: { label: "Submitted", accessibleLabel: "Form submitted successfully", disabled: true },
  error: { label: "Retry", accessibleLabel: "Retry submitting form", disabled: false },
};
```

Every state that users perceive SHOULD expose an accurate accessible name (visible text and/or `aria-label`).

## Design principles

1. **Responsive from day one** — usable at the project’s minimum width (default 320px).
2. **Accessible by default** — focus styles, keyboard, names/roles.
3. **Theme-agnostic** — semantic tokens only (`var(--color-…)`), never raw `#14479F` in components.
4. **Consistent interaction** — same action → same pattern app-wide.
5. **Loading / empty / error** — data views define all three; no blank failures.

## Form inputs

| State | Behavior |
|-------|----------|
| Default | Border `--color-border-default`, label `--color-text-secondary` |
| Focused | Focus ring / border `--color-focus-ring`, label `--color-text-primary` |
| Invalid | Border `--color-text-destructive` (or dedicated destructive border token), error text linked via `aria-describedby` |
| Disabled | Muted surface/text; not in tab order if truly inert (`disabled`) |
| Read-only | Focusable when users need to read/copy; not editable |
| Required | Visible indicator + `aria-required="true"` or native `required` |

```css
.input {
  border: 1px solid var(--color-border-default);
  color: var(--color-text-primary);
  background: var(--color-bg-surface);
  border-radius: var(--radius-sm);
  padding: var(--space-3) var(--space-4);
  transition: border-color var(--duration-normal) var(--easing-standard);
}

.input:focus-visible {
  outline: none;
  border-color: var(--color-focus-ring);
  box-shadow:
    0 0 0 2px var(--color-bg-surface),
    0 0 0 4px var(--color-focus-ring-outer);
}

.input[aria-invalid="true"] {
  border-color: var(--color-text-destructive);
}

.input:disabled {
  background: var(--color-bg-elevation-1);
  color: var(--color-text-tertiary);
  cursor: not-allowed;
}
```

## Buttons

Variants: primary / secondary / destructive / tertiary.

```css
.button--primary {
  background: var(--color-bg-primary);
  color: var(--color-text-on-primary);
  border: none;
  padding: var(--space-3) var(--space-4);
  font-family: var(--font-family-sans);
  font-size: var(--font-size-label);
  font-weight: var(--font-weight-semibold);
  border-radius: var(--radius-sm);
  transition:
    background-color var(--duration-normal) var(--easing-standard),
    transform var(--duration-fast) var(--easing-standard);
}

.button--primary:hover {
  background: var(--color-bg-primary-hover);
}

.button--primary:active {
  transform: translateY(1px);
}

.button--primary:disabled {
  background: var(--color-bg-elevation-1);
  color: var(--color-text-tertiary);
  cursor: not-allowed;
  transform: none;
}

.button--loading {
  position: relative;
  color: transparent;
  pointer-events: none;
}

.button--loading::after {
  content: "";
  position: absolute;
  inset: 50% auto auto 50%;
  width: 16px;
  height: 16px;
  margin: -8px 0 0 -8px;
  border: 2px solid rgb(255 255 255 / 0.3);
  border-top-color: var(--color-text-on-primary);
  border-radius: 50%;
  animation: spin var(--duration-deliberate) linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (prefers-reduced-motion: reduce) {
  .button--primary {
    transition: none;
  }
  .button--loading::after {
    animation: none;
    border-color: var(--color-text-on-primary);
  }
}
```

Loading buttons: keep an accessible name that reflects busy state (`aria-busy="true"` and updated label).

## Data lists / tables

| Pattern | When |
|---------|------|
| List | Simple single-column data, mobile |
| Table | Multi-column comparison on wider viewports |
| Cards | Rich media + actions |
| Virtualization | Very large lists (thousands of rows) |

On narrow screens: allow horizontal scroll for complex tables **or** stack into definition lists/cards — pick one pattern per product and stay consistent.

## Cards

Structure: optional media → title → description → metadata → actions.

Rules:

1. Use cards for rich content; simple tabular data stays a table/list.
2. Equalize heights in a grid with flex/grid.
3. No horizontal scroll inside a card.
4. Set image `aspect-ratio` so layout does not jump.

## Navigation

| Viewport | Pattern | Placement |
|----------|---------|-----------|
| &lt; 768px | Bottom bar **or** top bar + drawer | Max ~5 primary destinations |
| ≥ 768px and &lt; 1024px | Top tabs or collapsible side nav | Keep primary destinations visible |
| ≥ 1024px | Sidebar (≈240px) or persistent top nav | Active state always visible |

**Hamburger / drawer:** use on small viewports when primary links do not fit. Do **not** require hamburger on desktop if a sidebar/top nav already shows the same destinations.

Principles:

1. Prefer ≤5 top-level items; group the rest.
2. Clear active state.
3. Limit nesting; use breadcrumbs for deeper hierarchy.
4. Full keyboard support (Tab into nav; arrows inside composite widgets per APG).

## Documentation per component

Document: purpose, states/transitions, props, events, a11y requirements, responsive behavior, token usage, code examples, related components. Workflow: `docs/design-process.md`.

## Testing

Visual baselines + `axe-core` for each composite widget. See `docs/testing.md`.
