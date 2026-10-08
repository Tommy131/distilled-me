# OwO Recorder Signal patterns

This is a session-distilled implementation overlay for the OwO Recorder React web app. It captures decisions that repeatedly improved the redesign work: preserve the product contract, make dense operational data readable, and verify real states instead of trusting a static screenshot.

## Visual language

The current Recorder web implementation uses a Signal direction:

- Light semantic mapping: cool gray page background, solid white surfaces, dark slate text, and a restrained electric-blue accent.
- Dark semantic mapping: graphite/titanium page and surfaces, near-white text, and a softened light-blue accent. Do not use pure black as the page or card surface.
- Primary surfaces use a 1px border, a subtle shadow, and a 24px radius. Secondary wells use 16px; hero or full-width feature surfaces may use 32px.
- Page headings generally sit in the 32–48px range with a heavy display weight. Body copy is quieter and around 14–16px. Quantities, IDs, timestamps, scores, and balances use a mono face with tabular numerals.
- Saturated color belongs to primary CTAs and semantic states. A quiet card can use a restrained accent gradient; glass or blur should remain a supporting effect, never the only contrast boundary.

Use the project's existing `--color-*`, `--sp-*`, `--r-*`, `--text-*`, and `--font-*` variables when available. The values above describe intent; feature CSS should not hardcode them.

## Product contract during a redesign

Before changing a page, locate its API effects and event handlers. Keep these invariant unless the user asks otherwise:

- route names and permission checks;
- GET/POST/PUT/PATCH/DELETE paths, bodies, query parameters, idempotency keys, and refresh behavior;
- content order, source labels, calculations, timestamps, and business status semantics;
- destructive confirmation, error handling, and retry behavior.

Markup may be reshaped to improve hierarchy. A design change must not silently add analytics, alter sorting, remove a data field, or replace real values with demo values. Mock data belongs only in browser QA fixtures or documentation screenshots.

## Layout recipes

### User credits and bills

Keep the existing combined page and order. Put the balance summary and voucher redemption in two equal desktop cards; stack them below 1000px. The summary should make the balance dominant and place spent/held values in smaller inset wells. Keep billing status or the settings link at the bottom of that card.

Use a ledger heading with a record count. Render bills as receipt cards: source and UTC time together, signed amount aligned opposite, unit shown under the number, refund/reason notes across the card, and a horizontal row for each measured dimension. On mobile, every meter row gets its own line. Unmeasured dimensions retain their text label but must not pretend to be a numeric ARIA meter.

### Operations administration

Use an administration content max around 1200–1280px and a dedicated page header. Metrics become separate tiles; filter controls live in a labeled tool surface; records use semantic tables or cards based on the data density. Long tables scroll inside a named, keyboard-focusable container instead of widening the document. Keep `min-width: 0` on grid/flex children.

- **Sessions:** show batch actions beside the page title, visible labels for filters, and expandable owner cards with counts, storage, duration, and frozen totals. Expanded details retain the table semantics and a local overflow region.
- **Storage:** make used space and the progress bar the dominant capacity card. Show account usage as a separate ranked list. Clamp progress ARIA values to 0–100 when the visual bar is clamped, while preserving the textual over-quota message.
- **Audit:** use labeled native selects for both action and actor. A row of actor chips is unsuitable for a large directory. Preserve action filtering, actor query parameters, cursor pagination, request IDs, and reasons.
- **Plugins:** use cards that keep plugin identity, version, trust state, and the trust/revoke action together. Long identifiers wrap. Trust/revoke keeps its original request and idempotency behavior.
- **Orphan cleanup:** show file count, recording bytes, and export count as distinct metrics. Destructive cleanup remains behind the existing confirmation dialog; Escape cancellation and focus restoration are part of the UX.
- **Server cluster:** separate hardware summary, model catalog, and local model readiness into surfaces. Keep installation/risk confirmation and progress states unchanged.

## Model-state message deduplication

The preflight API can return multiple issues for several model roles. Avoid repeating a user-facing sentence once per role:

1. Translate each issue into the exact message the user will see. Use a stable semantic key when the product defines one; otherwise use the rendered message as the grouping key.
2. Keep the first occurrence order. Group identical messages under one “Needs attention”/“需要处理” heading.
3. For GPU-memory issues, union action codes with an insertion-ordered set. If no action list is supplied, use the documented default actions. Preserve unknown actions as readable fallback text.
4. Render one outer warning surface. Do not put a border around every issue or every nested step; spacing and a native list communicate hierarchy.
5. Keep genuinely different guidance separate. If all issues disappear, remove the repair surface rather than leaving an empty heading.

This rule applies to any repeated server/model warning, not only GPU memory. It belongs at the presentation boundary so API diagnostics remain complete and auditable.

## Responsive and accessibility details

- Use the existing shell breakpoints, with special attention to 320px and 390px phones. Mobile admin navigation may scroll horizontally, but the page itself must not.
- A table can have a large intrinsic minimum width only inside `.table-scroll`/equivalent local overflow. Give the region an accessible name and keyboard focus.
- Prefer native `<select>`, `<button>`, `<label>`, `<table>`, `<time>`, `<dl>`, and list semantics. Add ARIA to fill a gap, not to replace native semantics.
- Every status/error has a live-region role appropriate to urgency. Keep visible focus rings. Use 44px-ish touch targets for primary controls.
- Empty states should explain what is absent and what can happen next. Loading states reserve the final panel shape. Error states offer the existing retry or recovery action.
- Confirm irreversible actions; do not make the dangerous button the only way to dismiss the dialog. Restore focus to the trigger after cancel or completion.

## Browser QA matrix

For a changed Recorder page, run targeted tests plus build/lint, then inspect real rendered routes with mocked network responses where mutation is risky. A useful baseline is:

| Axis | Values |
| --- | --- |
| Theme | light, dark; system when supported |
| Locale | zh-CN and en when localized |
| Width | 320, 390, 768, 1024, 1440px |
| Data | populated, empty, loading, error, long labels/IDs, zero/large values |
| Interaction | primary success, validation failure, retry, destructive cancel/confirm, keyboard focus |
| Automated checks | document overflow, axe WCAG 2/2.1/2.2 AA, console/page errors |

Screenshots are evidence for review, not a substitute for behavior checks. Record which endpoints were mocked and never claim that browser fixtures exercised the real financial, deletion, queue, or model-install operation.
