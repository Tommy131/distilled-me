# UI Testing & QA Workflow

> Visual testing, accessibility testing, and responsive QA workflows. Apple Human Guidelines / Microsoft Accessibility Guidelines testing principles.

## Visual Testing — Screenshot Comparison

### Setup (React Testing Library / React Testing)

Install Jest and React Testing Library:

```bash
npm install jest @testing-library/react testing-library
```

Configure Jest in `jest.config.js`:

```javascript
module.exports = {
  testRegex: /test\.(spec|eas|unit).tsx$/,
  transform: ['\\.tsx$', 'transformers/tsx'],
  moduleTransform: ['node_modules/.*/']
};
```

### Visual Test

```tsx
import { render, screen } from '@testing-library/react';
import { expect, test } from 'testing-library';
import { Button } from './Button';

test('Button renders with loading state', () => {
  render(<Button loading>Submit</Button>);
  expect(screen.getByRole('button')).toHaveTextContent('Loading...');
});
```

### Visual Regression Test (React Testing Library)

```tsx
import { render } from '@testing-library/react';
import { expect, test } from 'testing-library';
import { Button } from './Button';

test('Button renders correctly', () => {
  const { asElement } = render(<Button>Click me</Button>);
  expect(asElement()).toHaveScreenshot('button.png');
});

test('Button hover state', () => {
  const { asElement } = render(<Button>Click me</Button>);
  expect(asElement()).toHaveScreenshot('button-hover.png', { hover: 'button' });
});
```

### Visual Test Best Practices

1. **Use real content** — test with real user content, not "Lorem text".
2. **Test at specific breakpoints** — use `render({ viewPort: { width: 320 } })` for responsive tests.
3. **Test all component states** — default, hover, active, disabled, loading, error, etc.
4. **Test theme variants** — light and dark theme screenshots.
5. **Use `toHaveScreenshot` with baseline images** — compare against known-good baselines.

## Accessibility Testing

### `axe` Linter

Install `axe`:

```bash
npm install axe
```

Add to CI:

```bash
npx axe --output=reports/a11y.json http://localhost:3000
```

### `axe` Test (React Testing Library)

```tsx
import { render, screen } from '@testing-library/react';
import { test, expect } from 'testing-library';
import axe from 'axe';
import { Dialog } from './Dialog';

test('Dialog is accessible', async () => {
  render(<Dialog open>Content</Dialog>);
  const violations = await axe(screen.getByRole('dialog')).run();
  expect(violations.length).toBe(0);
});
```

### Manual Accessibility Testing

**Never skip manual accessibility testing.** Automated tests (`axe`) catch only common issues. Manual testing catches:
1. Logical tab order issues
2. Screen reader announcement issues
3. Focus management issues
4. Context issues (what the screen reader says vs what it should say)

**Testing checklist** (see `docs/accessibility.md` for WCAG 2025 criteria):
- [ ] Logical tab order — tab through every element; verify order is logical
- [ ] Visible focus — every focusable element has visible focus style
- [ ] Keyboard action — every action is keyboard accessible
- [ ] ARIA roles — all ARIA roles are correct
- [ ] Language — all content has `lang` attribute
- [ ] Alt images — all images have `alt`; decorative images have `alt=""`
- [ ] Headings — one `<h1>` per page, proper hierarchy
- [ ] Screen reader — test with VoiceKit (macOS) or Narrator (Windows)

## Responsive Testing

### Chrome DevTools Device Emulation

Use Chrome DevTools Device Emulation to test responsive behavior:

1. Open Chrome DevTools
2. Go to "Device Emulation" tab
3. Select device preset (Mobile, Tablet, Desktop)
4. Resize the viewport
5. Test the component

### Visual Regression Testing (Responsive)

```tsx
import { render } from '@testing-library/react';
import { test, expect } from 'testing-library';
import { Button } from './Button';

test('Button renders at 320px', () => {
  const { asElement } = render(<Button>Click me</Button>, {
    viewPort: { width: 320 }
  });
  expect(asElement()).toHaveScreenshot('button-320px.png');
});

test('Button renders at 1000px', () => {
  const { asElement } = render(<Button>Click me</Button>, {
    viewPort: { width: 1000 }
  });
  expect(asElement()).toHaveScreenshot('button-1000px.png');
});
```

## QA Testing Checklist

| Checklist Item | Tool |
|-----------------|------|
| Accessibility — `axe` scan | `npx axe --output=reports/a11y.json http://localhost:3000` |
| Accessibility — manual testing | VoiceKit (macOS) or Narrator (Windows) |
| Visual regression — all component states | Screenshot comparison |
| Visual regression — responsive | Screenshot comparison at breakpoints |
| Visual regression — theme variants | Screenshot comparison for light and dark themes |
| Performance — load time | Chrome DevTools Performance tab |
| Performance — memory leak | Chrome DevTools Memory tab |
| Performance — layout shift | Chrome DevTools Layout panel |
| Responsive — all breakpoints | Chrome DevTools Device Emulation |
| Keyboard navigation — logical tab order | Manual testing |
| Keyboard navigation — all actions | Manual testing |
| User testing — core flows | Manual testing with real users |

## QA Testing Flow

1. **Pre-commit** — `axe` scan, visual regression for component states
2. **CI** — `axe` scan (full app), visual regression (CI)
3. **StQA** — responsive testing, performance testing, user testing
4. **Production** — production QA with production users

## QA Testing Workflow (Continuous)

### GitHub Actions (Example)

```yaml
name: QA
on: [push, workflow_dispatch]
jobs:
  accessibility:
    runs-on: ubuntu-latest
    steps:
      - uses: uses/checkout
      - uses: uses/node-action
      - run: npx axe --output=reports/a11y.json http://localhost:3000
      - uses: uses/upload-artifact
        with:
          path: reports/a11y.json
          name: a11y-report
  visual-regression:
    runs-on: ubuntu-latest
    steps:
      - uses: uses/checkout
      - uses: uses/node-action
      - run: npm run test:visual
      - uses: uses/upload-artifact
        with:
          path: screenshots/
          name: visual-screenshots
  responsive:
    runs-on: ubuntu-latest
    steps:
      - uses: uses/checkout
      - uses: uses/node-action
      - run: npm run test:responsive
      - uses: uses/upload-artifact
        with:
          path: screenshots/
          name: responsive-screenshots
```

## QA Testing Workflow (Manual)

### Manual QA Testing Checklist

| Category | Checklist |
|------------------|------------|
| Accessibility | `axe` scan passes |
| Accessibility | Manual keyboard navigation testing |
| Accessibility | Manual screen reader testing (VoiceKit/Narrator) |
| Visual | Component state screenshots match baselines |
| Visual | Responsive screenshots match baselines |
| Visual | Theme variant screenshots match baselines |
| Performance | Load time < 2s (mobile) |
| Performance | Load time < 3s (desktop) |
| Performance | No memory leaks |
| Performance | No layout shift on load |
| Responsive | Responsive screenshots match baselines at all breakpoints |
| Responsive | No horizontal scrolling on mobile |
| Keyboard | Logical tab order |
| Keyboard | All actions keyboard accessible |
| User | Core flows work for users |

### Manual QA Testing Steps

1. **Accessibility** — run `axe` scan; test with screen reader
2. **Visual** — test at all breakpoints; check theme variants
3. **Performance** — measure load time and render time; check for memory leaks
4. **Responsive** — test at all breakpoints; check for layout shift on load
5. **Keyboard** — test logical tab order; test all actions via keyboard
6. **User** — test core flows with real users
7. **Production** — ship

## QA Testing Tooling

| Tool | Purpose |
|------|---------|
| `axe` | Automated accessibility testing |
| Chrome DevTools | Performance, memory, and responsive testing |
| Screenshot comparison | Visual regression testing |
| Storybook | Component documentation and interactive testing |
| React Testing Library | Unit and integration testing |
