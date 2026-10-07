# Accessibility & Screen Reader Compliance (WCAG 2025)

> Apple Human Guidelines / Microsoft Accessibility Guidelines / WCAG 2025 principles: accessible by default, keyboard-first, screen reader compatible.

## WCAG 2025 Core Criteria

| Criterion | Requirement | Implementation |
|-----------|-------------|----------------|
| Logical tab order | All focusable elements in logical tab order | Natural DOM order; `tabindex` only to fix order |
| Visible focus | Focus ring on all focusable elements | Outline or box-shadow on `:focus-visible` |
| Keyboard action | All actions keyboard accessible | `keydown` handler on every interactive element |
| ARIA roles | Correct use of ARIA roles | `role` + `aria-*` only when HTML element insufficient |
| Language | `lang` attribute on all content | `<html lang="en">` or `<meta name="description" lang="en">` |
| Alt images | All images have `alt`; decorative images `alt=""` | `alt` describes content; `alt=""` for decorative |
| Headings | One `<h1>` per page, proper hierarchy | `<h1>` → `<h2>` → `<h3>` → `<h4>` |
| Screen reader | All content announced | ARIA live regions for dynamic content |

## Focus Management

### Focus Style

```css
/* Focus ring — visible on keyboard navigation, hidden on mouse */
*:focus-visible {
  outline: 2px solid var(--color-primary-900);
  outline-offset: 4px;
}

/* For buttons */
button:focus-visible {
  box-shadow: 0 0 0 2px var(--color-primary-900),
              0 0 0 6px rgba(14479F, 0.3);
  outline: none;
}
```

### Tab Order

```html
<!-- Default: natural DOM order (recommended) -->
<nav>
  <a href="/home">Home</a>
  <a href="/about">About</a>
</nav>

<!-- Fix order with tabindex (rarely needed) -->
<input type="text" tabindex="1">
<select tabindex="2">
  <option value="option1">Option 1</option>
</select>
```

### Focus Traps (Skip Links)

```html
<nav aria-label="Primary">
  <a href="#main-content">Skip to main content</a>
</nav>
<main id="main-content">
  <!-- Main content -->
</main>
```

## ARIA Attributes

### Roles

| Role | Description | Usage |
|------|-----------|--------|
| `role="alert"` | Alerts user of important event | Use sparingly |
| `role="dialog"` | Modal dialog | Requires focus management |
| `role="progressbar"` | Progress indicator | Requires `aria-valuemin`/`aria-valuemax`/`aria-valuen` |
| `role="status"` | Status updates | Use `aria-live="polite"` or `aria-live="assertive"` |
| `role="tablist"` | Tab navigation | Requires keyboard arrow navigation |
| `role="tab"` | Individual tab | Requires `aria-selected` |
| `role="tabpanel"` | Tab panel content | Requires `aria-labelledby` |
| `role="tooltip"` | Tooltip | Requires `aria-describedby` |
| `role="search"` | Search form | Requires `aria-label` |
| `role="navigation"` | Navigation region | Requires `aria-label` |

### ARIA States

| State | Description | Usage |
|------|-----------|--------|
| `aria-expanded` | Expandable content | `true`/`false` toggle |
| `aria-selected` | Selected item | `true`/`false` toggle |
| `aria-checked` | Checkbox state | `true`/`false` toggle |
| `aria-disabled` | Disabled state | `true`/`false` toggle |
| `aria-hidden` | Hidden element | `true`/`false` toggle (prevents DOM removal) |
| `aria-busy="eased"` | Loading state | `eased`/`immediate` |
| `aria-live` | Live region | `polite`/`assertive`/`off` |
| `aria-atomic` | Atomic element | `true`/`false` |
| `aria-haspopup` | Has popup | `true`/`false`/`menu`/`dialog` |
| `aria-label` | Accessible label | Descriptive text |
| `aria-labelledby` | Accessible label from element | ID reference |
| `aria-describedby` | Accessible description from element | ID reference |

### Live Regions

```html
<!-- Announced to screen reader -->
<div aria-live="polite" aria-label="Status">
  <span id="status-text">Saving...</span>
</div>

<script>
function updateStatus(message) {
  document.getElementById('status-text').textContent = message;
}
</script>
```

**`aria-live` values**:
- `polite` — announced after next screen reader action
- `assertive` — announced immediately
- `off` — not announced (default)

### Modal Dialogs

```html
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="dialog-title"
  tabindex="-1"
>
  <div id="dialog-title">Confirm Action</div>
  <p>Are you sure?</p>
  <div class="dialog-actions">
    <button onclick="confirmAction()">Confirm</button>
    <button onclick="closeDialog()">Cancel</button>
  </div>
</div>
```

**Modal requirements**:
1. `role="dialog"` + `aria-modal="true"`
2. `tabindex="-1"` + `focus()` on mount
3. Escape key closes dialog
4. Focus returns to trigger on close
5. Scroll locked on background (`body { overflow: hidden }`)
6. `aria-labelledby` or `aria-label` for accessibility label

## Keyboard Navigation

### Tab Navigation

All interactive elements must be focusable via tab:
- Links (`<a>`) — natively focusable
- Buttons (`<button>`) — natively focusable
- Inputs (`<input>`, `<select>`, `<textarea>`) — natively focusable
- Custom components — `tabindex="0"` + focus styles

### Keyboard Event Handlers

```javascript
// Enter key for custom clickable elements
function handleKeydown(event) {
  if (event.key === 'Enter' || event.key === ' ') {
    event.preventDefault();
    element.click();
  }
}

element.addEventListener('keydown', handleKeydown);
```

### Arrow Navigation for Tablists

```javascript
// Tab navigation
function handleTabKeydown(event) {
  const tabs = event.target.parentElement.querySelectorAll('[role="tab"]');
  const currentIndex = Array.from(tabs).indexOf(event.target);

  if (event.key === 'ArrowLeft') {
    event.preventDefault();
    const newIndex = (currentIndex - 1 + tabs.length) % tabs.length;
    tabs[newIndex].focus();
  }

  if (event.key === 'ArrowRight') {
    event.preventDefault();
    const newIndex = (currentIndex + 1) % tabs.length;
    tabs[newIndex].focus();
  }
}
```

## Screen Reader Compatibility

### Reading Order

```html
<!-- Correct reading order -->
<header>...</header>
<main>
  <h1>Page Title</h1>
  <p>Introduction</p>
  <article>
    <h2>Section</h2>
    <p>Content</p>
  </article>
  <aside>...</aside>
</main>
<footer>...</footer>
```

### Landmarks

```html
<header>...</header>
<nav role="navigation" aria-label="Primary">...</nav>
<main>...</main>
<aside role="complementary" aria-label="Sidebar">...</aside>
<footer>...</footer>
```

### Announce to Screen Reader

```javascript
function announce(message, assertive = false) {
  const announcer = document.getElementById('screen-reader-announcer') || createAnnouncer();
  announcer.setAttribute('aria-live', assertive ? 'assertive' : 'polite');
  announcer.textContent = message;
  setTimeout(() => { announcer.textContent = ''; }, 1000);
}

function createAnnouncer() {
  const announcer = document.createElement('div');
  announcer.id = 'screen-reader-announcer';
  announcer.setAttribute('aria-live', 'polite');
  announcer.setAttribute('aria-live-polite', 'true');
  announcer.style.cssText = 'position: absolute; clip: rect(0 0 0 0); overflow: hidden;';
  document.body.appendChild(announcer);
  return announcer;
}
```

## Accessibility Testing

### Manual Testing

1. **Keyboard-only navigation** — Tab through every element, verify logical order
2. **Screen reader test** — Test with VoiceKit (macOS) or Narrator (Windows)
3. **Color schemes** — Test in both light and dark system color schemes
4. **Font size** — Test with system font size (large, extra-large)
5. **Zoom** — Test with 200% zoom (image and text)
6. **Focus management** — Verify focus return on dialog close, modal, etc.

### Automated Testing

Install `axe`:

```bash
npm install axe
```

Add to CI:

```bash
npx axe --output=reports/a11y.json http://localhost:3000
```

### Visual Testing

See `docs/testing.md` for visual/snapshot testing setup.

## Accessibility Best Practices

1. **Semantic HTML first** — use `<button>`, `<nav>`, `<header>`, `<main>`, `<article>`, `<section>` before custom components
2. **Label everything** — every interactive element has an accessible label
3. **Describe images** — `alt` describes what the image shows; `alt=""` for decorative
4. **Avoid overuse of ARIA** — if you can use a native element, don't use ARIA
5. **Test with screen readers** — automation doesn't catch all accessibility issues
6. **Design accessible first** — don't design then add accessibility; design with accessibility as a requirement
7. **Accessible by default** — components should be accessible without extra configuration

## Apple Human Guidelines — Accessibility

| Guideline | Principle |
|-----------|----------|
| **Screen reader** | All content must be readable by VoiceKit; never hide content from screen readers |
| **Dynamic content** | Announce changes to screen readers using `AXNotification` / `AXUIA11y` |
| **Focus** | Focus must be managed explicitly for custom controls; don't rely on system focus |
| **Motion** | Respect `prefers-reduced-motion`; reduce or disable motion when the setting is enabled |
| **Typography** | Use system font styles; don't customize font sizes below 17pt (minimum for body text) |
| **Color** | Use system colors; don't override with hard-coded values |
| **Touch** | Touch targets minimum 44pt (22pt * 2); larger is better |

## Microsoft Accessibility Guidelines

| Guideline | Principle |
|-----------|----------|
| **Tab order** | Logical tab order; custom components must support tab navigation |
| **Focus** | Visible focus ring on all focusable elements |
| **Keyboard** | All actions accessible via keyboard |
| **ARIA** | Use ARIA roles and properties only when HTML elements are insufficient |
| **Screen reader** | All content announced to Narrator; live regions for dynamic content |
| **Color** | Use system colors; support for Windows Color Scheme |
| **Motion** | Respect `prefers-reduced-motion`; reduce or disable motion when the setting is enabled |
| **Touch** | Touch targets minimum 26pt (13pt * 2) |
