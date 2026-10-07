# Component Design Patterns

> Apple Human Guidelines / Fluent Design System component principles: state machines, accessible by default, responsive from day one, theme-agnostic.

## State Machine Pattern

Every interactive component is a **finite state machine** with explicit states and transitions. Never use ad hoc state.

```typescript
// Button state machine — TypeScript
type ButtonState = 'idle' | 'loading' | 'disabled' | 'success' | 'error';

const buttonStates = {
  IDLE: {
    label: 'Submit',
    icon: 'check',
    variant: 'primary',
    disabled: false,
    accessibleLabel: 'Submit form',
  },
  LOADING: {
    label: 'Submitting...',
    icon: 'spinner',
    variant: 'primary',
    disabled: true,
    accessibleLabel: 'Submitting form, please wait',
  },
  DISABLED: {
    label: 'Submit',
    icon: null,
    variant: 'primary',
    disabled: true,
    accessibleLabel: 'Submit form (disabled)',
  },
  SUCCESS: {
    label: 'Submitted',
    icon: 'check',
    variant: 'secondary',
    disabled: true,
    accessibleLabel: 'Form submitted successfully',
  },
  ERROR: {
    label: 'Retry',
    icon: 'reload',
    variant: 'destructive',
    disabled: false,
    accessibleLabel: 'Retry submitting form',
  },
};
```

**Rule**: Every state has an `accessibleLabel`. The screen reader reads the accessible label, not the visual text.

## Component Design Principles

### 1. Responsive from Day One
Every component must be designed for ≥320px width. No "desktop-first then mobile" workflow.

### 2. Accessible by Default
Every focusable element has visible focus style, logical tab order, correct `aria-*` attributes.

### 3. Theme-Agnostic
Components consume design tokens, not direct values. No `color: #14479F` in component code.

### 4. Consistent Interaction Pattern
Same action = same interaction across the app. Click submit = submit everywhere. Drag delete = delete everywhere.

### 5. Loading States
Every data-driven component has explicit loading states (skeleton or progress). Never show loading spinners over empty data.

### 6. Error States
Every network-bound component has explicit error states with actionable recovery (retry, cancel, etc.). Never show raw API errors to users.

### 7. Empty States
Every data list has explicit empty states with helpful messaging and action items. Never show blank empty lists.

## Component States

### Form Inputs

| State | Behavior |
|-------|----------|
| Default | Bordered by `--color-border-default`, label in `--color-text-secondary` |
| Focused | Outline in `--color-primary-900`, label in `--color-text-primary` |
| Invalid | Border in `--color-destructive-900`, error message in `--color-text-destructive` |
| Disabled | Background `--color-bg-elevation-1`, text `--color-text-tertiary`, pointer none |
| Read-only | Same as disabled but keyboard tabbable, focusable |
| Required | Asterisk `*` after label in `--color-destructive-900` |

```css
.input {
  border: 1px solid var(--color-border-default);
  color: var(--color-text-primary);
  background: var(--color-bg-surface);
  transition: border-color var(--duration-normal) var(--easing-ease-in-out);
}

.input:focus {
  outline: none;
  border-color: var(--color-border-subtle);
  box-shadow: 0 0 0 2px var(--color-primary-900),
              0 0 0 4px rgba(14479F, 0.3);
}

.input:invalid {
  border-color: var(--color-destructive-900);
}

.input:disabled {
  background-color: var(--color-bg-elevation-1);
  color: var(--color-text-tertiary);
  pointer-events: none;
}
```

### Buttons

| Variant | Primary / Secondary / Destructive / Tertiary |
|---------|---------|
| Default | Primary: background `--color-primary-900`, text `--color-neutral-100`; Secondary: background transparent, border `--color-border-strong`, text `--color-text-primary`; Destructive: background `--color-destructive-900`, text `--color-neutral-100`; Tertiary: background transparent, text `--color-text-primary` |
| Hover | Primary: background `--color-primary-800`; Secondary: background `--color-neutral-900`; Destructive: background `--color-destructive-800`; Tertiary: background `--color-neutral-100` |
| Active | Primary: background `--color-primary-900` with 8px translate; Secondary: background `--color-neutral-800`; Destructive: background `--color-destructive-800` with 2px translate; Tertiary: background `--color-neutral-50` |
| Disabled | All: background `--color-bg-elevation-1`, text `--color-text-tertiary`, pointer none |
| Loading | All: text "Loading...", icon spinner in center, disabled, background loading state |

```css
.button--primary {
  background-color: var(--color-primary-900);
  color: var(--color-neutral-100);
  border: none;
  padding: var(--space-3) var(--space-4);
  font-family: var(--font-label);
  border-radius: 4px;
  transition: background-color var(--duration-normal) var(--easing-ease-in-out),
              transform var(--duration-fast) var(--easing-ease-in-out);
}

.button--primary:hover {
  background-color: var(--color-primary-800);
}

.button--primary:active {
  transform: translateY(2px);
}

.button--primary:disabled {
  background-color: var(--color-bg-elevation-1);
  color: var(--color-text-tertiary);
  pointer-events: none;
  cursor: default;
}

.button--loading {
  pointer-events: none;
}

.button--loading .button__text {
  opacity: 0;
}

.button--loading .button__spinner {
  display: block;
}

.button__spinner {
  display: none;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-top-color: currentColor;
  border-radius: 50%;
  animation: spin var(--duration-slow) linear;
}
```

### Data Lists / Tables

| Pattern | When |
|---------|------|
| List (single column) | Single-column data, mobile, simple data |
| Table (horizontal) | Multi-column data on desktop |
| Cards (grid) | Rich data with images, action items, or cards |
| Infinite scroll | Large lists with pagination alternatives |
| Virtual list | Very large lists (>1000 items) |

**Table responsive pattern**: Horizontal scroll on mobile, stacked layout on narrow screens, card grid on very narrow.

### Cards

Card structure:
1. Image/Avatar (optional)
2. Title (required)
3. Description (optional)
4. Metadata (optional)
5. Actions (optional)

Card states: Default / Hover / Selected / Disabled

**Card principles**:
1. **No cards for simple data** — cards are for rich content with images, actions, or metadata. For simple tabular data, use a table or list.
2. **Consistent card heights** — use flexbox or grid to equalize card heights in a grid.
3. **No horizontal scrolling within cards** — vertical scrolling or truncation is acceptable; horizontal scrolling within a card is not.
4. **Image aspect ratios** — specify image aspect ratios (e.g., `aspect-ratio: 16/9`), never let images dictate card height.

### Navigation

| Navigation Type | Screen | Placement |
|----------------|--------|----------|
| Bottom bar | Mobile (<768px) | Bottom fixed, 56px height |
| Sidebar | Desktop (≥1000px) | Left side, 240px width, sticky |
| Tab bar | Tablet (≥768px) | Top of content area |
| Hamburger | Mobile (≥768px) | Top-right corner, opens drawer |

**Navigation principles**:
1. **Maximum 5 items** — navigation should have maximum 5 top-level items. More needs grouping or restructuring.
2. **Active state** — always show which item is active with clear visual indication.
3. **Deep nesting** — limit to 2 levels of nesting. Deeper requires breadcrumb or separate page.
4. **Keyboard navigation** — all navigation items must be keyboard accessible, with arrow-key navigation within navigation bars.

## Component Testing

Every component must have visual tests (screenshot comparison) and accessibility tests (`axe` scan). See `docs/testing.md` for testing setup.

## Component Documentation

Every component has documentation that covers:
1. Props/properties
2. State machine states and transitions
3. Slot/children API
4. Event handlers
5. Accessibility requirements
6. Responsive behavior
7. Visual states
8. Code examples

See `docs/design-process.md` for documentation workflow.
