# UI Testing & QA

> Visual, accessibility, and responsive QA. Pair automation (`axe-core`, screenshot diffs) with keyboard and screen-reader checks.

## Component / unit tests

```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom jsdom
```

```ts
import { render, screen } from "@testing-library/react";
import { Button } from "./Button";

test("button exposes loading state to AT", () => {
  render(<Button loading>Submit</Button>);
  expect(screen.getByRole("button", { name: /submitting|loading|submit/i })).toBeDisabled();
});
```

Prefer role + accessible name queries over class or text-only selectors.

## Accessibility automation

```bash
npm install -D axe-core jest-axe @axe-core/playwright
# CLI against a running app:
npm install -D @axe-core/cli
npx axe http://localhost:3000 --exit
```

```ts
import { render } from "@testing-library/react";
import { axe, toHaveNoViolations } from "jest-axe";
expect.extend(toHaveNoViolations);

test("page has no serious axe violations", async () => {
  const { container } = render(<App />);
  expect(await axe(container)).toHaveNoViolations();
});
```

Playwright example:

```ts
import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test("home a11y", async ({ page }) => {
  await page.goto("/");
  const results = await new AxeBuilder({ page }).analyze();
  expect(results.violations.filter((v) => v.impact === "critical" || v.impact === "serious")).toEqual([]);
});
```

## Manual accessibility

Automated tools miss focus order, announcement quality, and many keyboard traps.

Checklist (see `docs/accessibility.md` for WCAG 2.2 AA):

- [ ] Tab order matches visual order
- [ ] `:focus-visible` on every focusable control
- [ ] All actions work with keyboard only
- [ ] Screen reader: **VoiceOver** / **Narrator** / **NVDA** / **TalkBack** as relevant
- [ ] Images have correct `alt` (or empty for decorative)
- [ ] One `<h1>`; heading levels make sense
- [ ] Errors and status updates are announced
- [ ] Light and dark themes keep contrast

## Visual regression

Use Playwright, Chromatic, or Percy — not invented Testing Library screenshot APIs.

```ts
import { test, expect } from "@playwright/test";

test("button states", async ({ page }) => {
  await page.goto("/story/button");
  await expect(page.getByRole("button", { name: "Save" })).toHaveScreenshot("button-default.png");
});
```

Practices:

1. Real (or realistic) content — avoid “Lorem” when layout depends on string length.
2. Capture default / hover / focus / disabled / loading / error as needed.
3. Capture light and dark if both ship.
4. Stabilize animations (`prefers-reduced-motion` or disable in test config).

## Responsive QA

Default viewports: 320, 480, 768, 1024, 1280 (trim if the product documents a smaller set).

- [ ] No horizontal scroll at 320px for primary flows
- [ ] Touch targets adequate on narrow viewports
- [ ] Navigation pattern matches `docs/components.md` (bottom bar vs sidebar)
- [ ] No CLS when fonts/images load (space reserved)

Chrome DevTools device mode is fine for exploratory checks; CI should use Playwright viewports.

## Performance smoke

| Check | Target (default; override in DESIGN) |
|-------|--------------------------------------|
| LCP / meaningful paint | Agree per product; often &lt; 2.5s on reference hardware |
| CLS | Prefer &lt; 0.1 |
| Interaction | Buttons respond without long main-thread blocks |

Use DevTools Performance / Lighthouse as smoke, not as the only gate.

## CI sketch

```yaml
name: UI QA
on: [push, pull_request]
jobs:
  a11y-and-visual:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: npm
      - run: npm ci
      - run: npm run build
      - run: npm run test
      - run: npx playwright install --with-deps chromium
      - run: npm run test:e2e
```

Wire `test:e2e` to Playwright a11y + screenshot jobs. Upload reports/artifacts on failure.

## Pre-merge checklist

| Item | How |
|------|-----|
| axe / jest-axe / Playwright axe | CI |
| Keyboard pass on changed flows | Manual or Playwright keyboard |
| Screen reader spot-check on new widgets | Manual |
| Screenshots for new/changed components | CI baseline |
| Responsive at agreed breakpoints | Playwright + manual |
| Theme tokens used (no new raw hex in components) | Review |
| Reduced-motion path exists for new animation | Review / CSS |

## Tooling map

| Tool | Purpose |
|------|---------|
| `axe-core` / `@axe-core/cli` / `@axe-core/playwright` | Automated a11y |
| Testing Library | Behavior tests via accessibility tree |
| Playwright | E2E, screenshots, keyboard |
| Storybook (optional) | Component states + visual review |
| Browser DevTools | Performance, reflow, emulation |
