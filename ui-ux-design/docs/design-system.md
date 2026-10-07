# Design System — Tokens & Architecture

> Apple Human Guidelines / Fluent Design System principles: tokens over magic values, design tokens as the only source of truth, explicit theming layer, consistent naming.

## Token Architecture

### Layer 1: Primitive Tokens (Global Design Tokens)

These tokens encode the **foundational values** — colors, spacing, typography, motion — and are never used directly in component code. They are consumed exclusively by semantic/compound tokens.

```css
/* Color tokens — semantic, never direct hex values */
--color-text-primary:          var(--color-neutral-900);
--color-text-secondary:         var(--color-neutral-700);
--color-text-tertiary:        var(--color-neutral-500);
--color-text-destructive:     var(--color-destructive-900);
--color-text-success:           var(--color-success-900);

--color-bg-surface:           var(--color-neutral-100);
--color-bg-elevation-1:        var(--color-neutral-50);
--color-bg-elevation-2:        var(--color-neutral-10);
--color-bg-overlay:          var(--color-neutral-900);

--color-border-subtle:      var(--color-neutral-400);
--color-border-default:     var(--color-neutral-600);
--color-border-strong:      var(--color-neutral-800);

/* Spacing tokens — always 8px grid or multiples of 8px */
--space-0:  0;
--space-1:  2px;
--space-2:  4px;
--space-3:  8px;
--space-4:  12px;
--space-5:  16px;
--space-6:  24px;
--space-7:  32px;
--space-8:  40px;
--space-9:  48px;
--space-10: 64px;

/* Typography tokens */
--font-display:  'Inter', 72px, 84, 800, 24px;
--font-heading:   'Inter', 32px, 64, 700, 20px;
--font-body:      'Inter', 16px, 48, 400, 14px;
--font-label:     'Inter', 14px, 42, 600, 14px;
--font-caption:   'Inter', 12px, 34, 400, 14px;

--font-weight-regular:  400;
--font-weight-semibold: 600;
--font-weight-bold:    700;

/* Motion tokens */
--duration-fast:    48ms;
--duration-normal:  100ms;
--duration-slow:     200ms;
--duration-very-slow: 320ms;

--easing-ease-in:      cubic-bezier(0, 0, 0, 1);
--easing-ease-out:     cubic-bezier(1, 0, 0, 1);
--easing-ease-in-out:  cubic-bezier(0, 0, 1, 1);
--easing-linear:     linear;

--easing-bezier-fast:    cubic-bezier(0.36, 0.01, 1, 0.9);
--easing-bezier-spring: cubic-bezier(0.25, 1, 0.25, 1.3);
--easing-bezier-easy-out: cubic-bezier(0, 0.4, 0.6, 1);
```

### Layer 2: Semantic / Compound Tokens

These tokens are the **only tokens used in component code**. They encode **intent**, not value. The same semantic token may resolve to different primitive values across themes.

```css
/* Button tokens */
--button-primary-bg-hover:       var(--color-neutral-700);
--button-primary-border-hover:  transparent;
--button-primary-text-hover:    var(--color-neutral-100);

--button-secondary-bg-hover:     var(--color-neutral-800);
--button-secondary-border-hover:   var(--color-neutral-800);
--button-secondary-text-hover:  var(--color-neutral-100);

/* Input tokens */
--input-border-color-focus:      var(--color-primary-900);
--input-border-color-error:     var(--color-destructive-900);
--input-placeholder-color:      var(--color-text-tertiary);
```

### Layer 3: Theme Tokens

Themed variants — dark/light/system. The same semantic tokens above resolve differently.

```css
/* Light theme (default) */
:root[data-theme="light"], :root, :host {
  --color-primary-100:    #14479F;
  --color-neutral-100:   #FFFFFF;
  --color-neutral-50:    #FFFFFF;
  --color-neutral-900:   #1D1D1D;
  --color-text-secondary:  var(--color-neutral-700);
  --color-text-tertiary:   var(--color-neutral-500);
  --color-bg-surface:    var(--color-neutral-100);
  --color-bg-elevation-1:   var(--color-neutral-50);
  /* ... etc */
}

/* Dark theme */
:root[data-theme="dark"] {
  --color-primary-100:    #426495;
  --color-neutral-100:   #383838;
  --color-neutral-50:    #4B4B4B;
  --color-neutral-900:   #D1D1D1;
  --color-text-secondary:  var(--color-neutral-700);
  --color-text-tertiary:   var(--color-neutral-500);
  --color-bg-surface:    var(--color-neutral-100);
  --color-bg-elevation-1:  var(--color-neutral-50);
  /* ... etc — every color must have a dark variant */
}

/* System preference */
:root {
  color-scheme: light;
}
:root:root {
  color-scheme: light;
}
@media (prefers-color-scheme: dark) {
  :root {
    color-scheme: dark;
  }
}
```

**Design rule**: System-prepared color scheme applies first; user preference toggle is additive. The toggle is always visible.

## Design Token Rules

1. **No magic values** — every hex color, spacing, font-size, and border-width in component code must be a CSS variable (token).
2. **No direct primitive token usage** — components use semantic/compound tokens, never primitive tokens directly.
3. **Token name encodes intent** — `--button-primary-bg-hover`, not `--btn-bg-hover` (semantic compound).
4. **Themed variants are mandatory** — every color token must resolve in both light and dark themes.
5. **Token validation** — CI should verify: all colors have dark variants, all tokens are referenced, no orphan tokens.
6. **Token migration** — changing a primitive token should cascade through all semantic tokens. Use a token migration script.
7. **Token documentation** — every semantic token has a description in the token schema.

## Design Token Schema

```json
{
  "colors": {
    "primary": {
      "100": {
        "light": "#14479F",
        "dark": "#426495"
      }
    },
    "destructive": {
      "900": {
        "light": "#6D0707",
        "dark": "#5F2927"
      }
    }
  },
  "spacing": {
    "0": "0",
    "1": "2px",
    "2": "4px",
    "3": "8px",
    "4": "12px",
    "5": "16px",
    "6": "24px",
    "7": "32px",
    "8": "40px",
    "9": "48px",
    "10": "64px"
  },
  "typography": {
    "display": {
      "font-family": "'Inter', 72px, 84, 800, 24px"
    },
    "heading": {
      "font-family": "'Inter', 32px, 64, 700, 20px"
    },
    "body": {
      "font-family": "'Inter', 16px, 48, 400, 14px"
    },
    "label": {
      "font-family": "'Inter', 14px, 42, 600, 14px"
    },
    "caption": {
      "font-family": "'Inter', 12px, 34, 400, 14px"
    }
  },
  "motion": {
    "duration": {
      "fast": "48ms",
      "normal": "100ms",
      "slow": "200ms",
      "very-slow": "320ms"
    },
    "easing": {
      "ease-in": "cubic-bezier(0, 0, 0, 1)",
      "ease-out": "cubic-bezier(1, 0, 0, 1)",
      "ease-in-out": "cubic-bezier(0, 0, 1, 1)",
      "linear": "linear",
      "bezier-fast": "cubic-bezier(0.36, 0.01, 1, 0.9)",
      "bezier-spring": "cubic-bezier(0.25, 1, 0.25, 1.3)",
      "bezier-easy-out": "cubic-bezier(0, 0.4, 0.6, 1)"
    }
  }
}
```

## Design Token Architecture Summary

```
Primitive tokens (global) → Semantic/compound tokens (component-level) → Theme variants (light/dark/system)
```

**Token flow**:
1. User toggles theme → `[data-theme]` attribute changes
2. Semantic token resolves via theme → different primitive value
3. Component code reads semantic token → gets appropriate value
4. No component code changes — only theme changes

This is the **Apple Human Guidelines / Fluent Design System approach**: tokens as the abstraction layer, semantic intent over direct value, theme as a property, not a set of overrides.
