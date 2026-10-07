# Design Process & Iteration Workflow

> Design process: from prototype to production, iterating on design with measurable outcomes. Apple Human Guidelines / Fluent Design System design philosophy: design iteratively, but never compromise accessibility or performance.

## Design Process — Three Phases

### Phase 1: Prototype (Minimum Viable)

1. **Define the problem** — what is the user trying to accomplish? What are the pain points?
2. **Draft layout** — wireframe or low-fidelity mockup. Focus on information hierarchy and interaction flow, not visual design.
3. **Prototype** — build a basic functional prototype in code (not a tool). This is the "testable" artifact.
4. **Validate** — test with users (or yourself). Identify what needs improvement.
5. **Iterate** — repeat steps 2-4. Each iteration should bring the prototype closer to production.

**Goal**: Identify the interaction pattern. This is where you discover what works and what doesn't.

### Phase 2: Design System Integration

1. **Define tokens** — colors, spacing, typography, motion, breakpoints for the design.
2. **Implement components** — build reusable components using design tokens (see `docs/components.md`).
3. **Document components** — for each component: states, props, accessibility requirements, code examples.
4. **Build the prototype** — assemble the prototype from design system components.

**Goal**: Establish the design system. Every component must be consistent, accessible, and theme-agnostic.

### Phase 3: Production Hardening

1. **Performance audit** — measure load time, render time, memory, and interaction response time. Optimize.
2. **Accessibility audit** — run `axe` scan. Test with screen readers. Fix issues.
3. **Responsive testing** — test at all breakpoints. Ensure no layout shift on load.
4. **User testing** — test with real users. Identify issues. Iterate.
5. **Release** — ship.

**Goal**: Make the product production-ready. No accessibility bypass, no layout shift, no performance regression.

## Iteration Workflow

### Design Iteration Checklist

When iterating on a design, go through this checklist:

- [ ] **Interaction pattern** — is the interaction pattern clear and consistent?
- [ ] **Information hierarchy** — is the information hierarchy clear? Is the most important information most prominent?
- [ ] **Accessibility** — does the new interaction pattern maintain keyboard navigation? Does screen reader read it correctly?
- [ ] **Performance** — does the new interaction pattern affect load time or render time?
- [ ] **Responsive** — does the new interaction pattern work on all device sizes?
- [ ] **Consistency** — does the new interaction pattern follow design system conventions?
- [ ] **User testing** — have you tested the new interaction pattern with users?

### Iteration Priorities (in order)

1. **Accessibility** — never iterate on a design that breaks accessibility. Accessibility is non-negotiable.
2. **Performance** — never iterate on a design that degrades performance beyond budget. Performance is a hard requirement.
3. **User feedback** — iterate on designs that users say don't work. Don't iterate on designs that users think are fine.
4. **Consistency** — iterate on inconsistencies in the design system. Consistency is a requirement.
5. **Visual polish** — iterate on visual polish last. It's the least important of all the above.

### Iteration Time Budget

| Phase | Time Budget | Notes |
|-------|-------------|-------|
| Prototype (Phase 1) | 20-30% of total time | Iterate as needed |
| Design System (Phase 2) | 30-40% of total time | Must be thorough |
| Production Hardening (Phase 3) | 30-40% of total time | Non-negotiable |
| Iteration | 10-20% of total time | Budget for iteration |

**Rule**: If you hit the iteration budget, you need to either:
1. Cut scope — ship less, not worse
2. Change the design — iterate on the design, not on the design system
3. Accept the limitation — document it in a design doc

## Design Documentation

### Design Document Template

Every significant design decision should be documented:

1. **Problem statement** — what problem is the design solving?
2. **Proposed solution** — what is the design?
3. **Constraints** — what are the constraints (performance, accessibility, responsiveness)?
4. **Constraints checklist** — how does the proposed solution address each constraint?
5. **Implementation notes** — any implementation notes (components, tokens, APIs)?
6. **Open questions** — any open questions? (These are the questions to iterate on.)

### Component Documentation Template

Every component needs documentation:

1. **Component description** — what does this component do?
2. **States** — all component states (default, hover, focus, active, disabled, loading, error, etc.)
3. **Props/properties** — what props does the component accept?
4. **Events** — what events does the component emit?
5. **Accessibility** — what are the accessibility requirements?
6. **Responsive behavior** — how does the component behave on different screen sizes?
7. **Code examples** — example code for each state.
8. **Related components** — what other components does this component interact with?

## Design Evaluation Criteria

| Criterion | Requirement |
|-----------|-----------|
| **Consistency** | All components follow the same design system conventions |
| **Accessibility** | All components pass `axe` scan with zero critical errors; keyboard navigation works |
| **Performance** | Load time < 2s (mobile), < 3s (desktop); no layout shift on load; no memory leaks |
| **Responsive** | Works on all device sizes (320px to 1440px); no horizontal scrolling on mobile |
| **Usability** | Users can accomplish their tasks without confusion; clear visual feedback for actions |
| **Maintainability** | Components are modular and reusable; code is well-documented; design system is documented |

## Design Decisions — When to Document

Document a design decision when:

1. It deviates from design system conventions
2. It involves a trade-off between competing design principles
3. It has a measurable impact on the design or implementation
4. It is likely to be questioned by users or team members

**Rule**: If you don't know if you should document, document it. Better to over-document than to lose context.
