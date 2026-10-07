# Accessibility (WCAG 2.2 AA)

> Target: **WCAG 2.2 Level AA**. Prefer native HTML semantics; add ARIA only when HTML is insufficient. Test with keyboard and a real screen reader (VoiceOver on macOS/iOS, Narrator or NVDA on Windows, TalkBack on Android).

## Core checklist

| Area | Requirement | Implementation notes |
|------|-------------|----------------------|
| Keyboard | All actions operable by keyboard | Native controls; custom widgets need key handlers + `tabindex="0"` |
| Focus visible | Clear focus indicator | `:focus-visible` outline / ring using `--color-focus-ring` |
| Focus order | Matches reading order | DOM order; avoid positive `tabindex` |
| Name / Role / Value | Correct accessible name | `<label>`, `aria-label`, or `aria-labelledby` |
| Contrast | Text 4.5:1 (3:1 large); UI 3:1 | Check against tokens in both themes |
| Images | Informative `alt`; decorative `alt=""` | Do not put critical text only in images |
| Headings | One `<h1>`; no level skips without reason | Structure content, do not style with random heading tags |
| Language | `<html lang="…">` | Set `lang` on passages in another language |
| Target size (2.2) | Meet AA target size / spacing | Prefer ≥24×24 CSS px with adequate spacing; 44×44 where touch-primary |
| Status messages (2.2) | Updates announced without focus move | `role="status"` / `aria-live="polite"` or `role="alert"` |
| Consistent help / auth (2.2) | Help and auth steps stay consistent | Same relative order across pages where required |

Official reference: [WCAG 2.2](https://www.w3.org/TR/WCAG22/).

## Focus

```css
*:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
}

button:focus-visible {
  outline: none;
  box-shadow:
    0 0 0 2px var(--color-bg-surface),
    0 0 0 4px var(--color-focus-ring),
    0 0 0 6px var(--color-focus-ring-outer);
}
```

- Do not remove outlines without a visible replacement.
- Modals: move focus inside on open; trap focus while open; restore focus to the trigger on close; close on Escape.

## Skip link

```html
<a class="skip-link" href="#main-content">Skip to main content</a>
…
<main id="main-content">…</main>
```

## ARIA essentials

Use ARIA to **fill gaps**, not to re-implement buttons/links.

| Attribute | Valid values / notes |
|-----------|----------------------|
| `aria-expanded` | `true` / `false` |
| `aria-selected` | `true` / `false` |
| `aria-checked` | `true` / `false` / `mixed` |
| `aria-disabled` | `true` / `false` (prefer native `disabled` when possible) |
| `aria-hidden` | `true` / `false` — hides from accessibility tree; do not hide focusable content |
| `aria-busy` | `true` / `false` only |
| `aria-live` | `off` / `polite` / `assertive` |
| `aria-valuemin` / `aria-valuemax` / `aria-valuenow` | For `role="progressbar"` / slider |
| `aria-label` / `aria-labelledby` / `aria-describedby` | Accessible name / description |

### Live regions

```html
<div role="status" aria-live="polite" aria-atomic="true" id="form-status"></div>
```

```js
function announce(message, { assertive = false } = {}) {
  let el = document.getElementById("sr-announcer");
  if (!el) {
    el = document.createElement("div");
    el.id = "sr-announcer";
    el.className = "visually-hidden";
    el.setAttribute("aria-live", "polite");
    el.setAttribute("aria-atomic", "true");
    document.body.appendChild(el);
  }
  el.setAttribute("aria-live", assertive ? "assertive" : "polite");
  el.textContent = "";
  requestAnimationFrame(() => {
    el.textContent = message;
  });
}
```

```css
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

### Dialog

```html
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="dialog-title"
  tabindex="-1"
>
  <h2 id="dialog-title">Confirm action</h2>
  <p id="dialog-desc">This cannot be undone.</p>
  <button type="button">Confirm</button>
  <button type="button">Cancel</button>
</div>
```

Requirements: labelled dialog, focus in on open, Escape closes, focus returns to trigger, background inert/scroll-locked.

## Keyboard patterns

- Links, buttons, inputs: native focus — do not add redundant handlers unless custom.
- Custom clickable: `tabindex="0"`, Enter and Space activate.
- Tabs (`role="tablist"`): arrows move between tabs; Home/End optional; selected tab `aria-selected="true"`.
- Menus: arrow navigation per [APG](https://www.w3.org/WAI/ARIA/apg/).

## Landmarks and structure

```html
<header>…</header>
<nav aria-label="Primary">…</nav>
<main>
  <h1>Page title</h1>
  …
</main>
<aside aria-label="Sidebar">…</aside>
<footer>…</footer>
```

Prefer native `<nav>`, `<main>`, `<header>`, `<footer>` over redundant roles.

## Manual testing

1. Keyboard only — Tab / Shift+Tab / Enter / Space / Escape / arrows where expected.
2. Screen reader — **VoiceOver** (macOS/iOS), **Narrator** or **NVDA** (Windows), **TalkBack** (Android).
3. Zoom 200% — content reflows; no loss of function (Reflow where applicable).
4. Light and dark themes — contrast still passes.
5. Forced colors / Windows High Contrast — smoke-check critical flows when relevant.

## Automated testing

Use **axe-core**, not a fictional `axe` npm package alone.

```bash
npm install -D @axe-core/cli axe-core
# Against a running local server:
npx axe http://localhost:3000 --exit
```

In unit/component tests (example with Vitest + Testing Library + jest-axe):

```bash
npm install -D axe-core jest-axe vitest @testing-library/react jsdom
```

```ts
import { render } from "@testing-library/react";
import { axe } from "jest-axe";
import { Dialog } from "./Dialog";

test("dialog has no serious axe violations", async () => {
  const { container } = render(<Dialog open title="Confirm">Body</Dialog>);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

Automation catches many issues; it does **not** replace keyboard + screen-reader checks.

## Practices

1. Semantic HTML first (`button`, `a`, `label`, landmarks).
2. Every interactive control has an accessible name.
3. Do not rely on color alone for state.
4. Errors: text explanation + programmatic association (`aria-describedby` / `aria-invalid`).
5. Design with accessibility as a requirement, not a retrofit.

## Platform notes (inspirational, not WCAG replacements)

| Source | Useful defaults |
|--------|-----------------|
| Apple HIG | VoiceOver compatibility; Dynamic Type; ~44pt touch targets on iOS; respect Reduce Motion |
| Fluent / WinUI | Visible focus; Narrator; respect system theme and reduced motion |
