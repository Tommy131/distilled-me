# Design Process & Iteration

> Prototype → design-system integration → production hardening. Accessibility and performance are constraints, not polish phases.

## Phase 1 — Prototype (minimum viable)

1. **Problem** — user goal and pain points.
2. **Layout** — wireframe / low-fi hierarchy and flow.
3. **Prototype in code** — testable UI beats slide-only comps for interaction work.
4. **Validate** — self-test + user feedback when available.
5. **Iterate** — refine interaction pattern before visual polish.

**Goal:** discover the interaction model.

## Phase 2 — Design system integration

1. **Tokens** — color, space, type, motion, breakpoints (`docs/design-system.md`, `assets/tokens.css`).
2. **Components** — reusable state machines (`docs/components.md`).
3. **Document** — states, props, a11y, examples.
4. **Rebuild the prototype** from system components.

**Goal:** consistency, theming, and accessible defaults.

## Phase 3 — Production hardening

1. **Performance** — measure load/interaction; fix regressions.
2. **Accessibility** — `axe-core` + keyboard + screen reader (`docs/accessibility.md`, WCAG 2.2 AA).
3. **Responsive** — agreed breakpoints; no layout shift on primary routes.
4. **User testing** — fix blocking issues.
5. **Release**.

## Iteration checklist

- [ ] Interaction pattern clear and consistent
- [ ] Information hierarchy clear
- [ ] Keyboard and screen-reader paths still work
- [ ] Performance within budget
- [ ] Responsive at agreed breakpoints
- [ ] Tokens/system conventions followed
- [ ] Feedback from users addressed when it blocks tasks

### Priority order

1. Accessibility  
2. Performance / correctness  
3. User feedback on task success  
4. Consistency  
5. Visual polish  

### Time budget (guideline)

| Phase | Share |
|-------|-------|
| Prototype | 20–30% |
| System integration | 30–40% |
| Production hardening | 30–40% |
| Extra iteration buffer | 10–20% |

If the buffer is exhausted: cut scope, change the design (not the accessibility bar), or document accepted limitations.

## Design decision record (lightweight)

For significant decisions:

1. Problem  
2. Proposed solution  
3. Constraints (a11y, performance, platforms)  
4. How constraints are met  
5. Implementation notes  
6. Open questions  

## Component doc template

1. Description  
2. States  
3. Props  
4. Events  
5. Accessibility  
6. Responsive behavior  
7. Code examples  
8. Related components  

## Evaluation criteria

| Criterion | Bar |
|-----------|-----|
| Consistency | Shared tokens and patterns |
| Accessibility | WCAG 2.2 AA intent; no critical axe issues; keyboard works |
| Performance | Budgets in DESIGN; no unbounded CLS on primary views |
| Responsive | Agreed breakpoints; no horizontal scroll on primary mobile flows |
| Usability | Users can complete tasks with clear feedback |
| Maintainability | Components reusable; system documented |

## When to document a decision

- Deviates from system conventions  
- Trades off competing principles  
- Affects a11y, performance, or information architecture  
- Likely to be questioned later  

When unsure, write a short note — cheaper than rediscovering context.
