# Filter panel with slow results

A worked example of a `component-refinement` where the complaint was speed and the defect was state communication.

## Surface contract

- **Surface:** query panel above a result table
- **Primary user:** analyst, several times a day
- **Primary task:** narrow 40,000 records to the set worth reading
- **Success condition:** the visible result is the one the current criteria describe
- **Main decision:** is this result set the right one to work from
- **Data volume:** 40,000 records; six criteria; queries take 1.5-6s
- **Data freshness:** results are a snapshot at query time
- **Costly mistake:** reading a result produced by criteria the user has since changed
- **Primary device and input:** desktop
- **Supported minimum width:** 320px
- **Loading behaviour:** previous result stays; pending stated in words
- **Empty behaviour:** first-use and no-results are separate
- **Error behaviour:** the previous result survives; retry names the query
- **Responsive strategy:** criteria move into a drawer, applied filters stay outside it
- **Accessibility risks:** one live region, chip removal by keyboard
- **Out of scope:** the query backend, the result table's columns

## The actual problem

Users reported "the filters are slow". They were, but the reported symptom was *"we think the table is empty"* — the panel cleared the result on every change and showed a spinner. A 3-second query with the previous result on screen reads as responsive; the same query against a blank table reads as broken.

Speed was not the fix. **What is on screen during the wait** was.

## Applied filters are always visible

```text
Filters   [Period: 2026-07 ×] [Status: pending ×] [Account: 4 selected ×]
          [Clear all]                                  412 of 40,318 records
```

Chips carry the **value**, not the field name — "Status" tells the user nothing, "Status: pending" tells them why the count dropped. Default filters that were never chosen appear as implicit chips, styled differently and not removable, because a hidden default is indistinguishable from a bug.

Above 7 chips the wall becomes its own scanning problem; the panel collapses to a summary line with a count and an expander.

## Pending and staleness

```text
⚠ Showing the result from 14:12 while the new query runs      [Cancel]
  ──────────────────────────────────────  264 of 412
```

Full contrast is preserved. The banner, the region border and the progress line carry the message. `opacity: 0.45` on the result was the first implementation and was reverted — it drops every value below 4.5:1 at once, worst in dark theme, and asks the user to read numbers that are no longer readable in exchange for something one line of text says better.

Typed input debounces at 300ms. The two expensive criteria use an explicit **Apply**, and unapplied changes are visible as such — a query the user thinks is running but is not is worse than a slow one.

## Empty states are two components

| State | Copy | Recovery |
|-------|------|----------|
| First use | "No records have been imported for this period yet." | Import, or how this works |
| No results | "**Status: pending** takes the result from 412 to 0 — every record here has been approved." | Remove that filter · widen the period |

Sharing one component leaves the user unable to tell whether the system is empty or their query is wrong. The no-results copy names the **most restrictive** criterion, which requires knowing which one it was — computed, not guessed.

## URL state

Period, status, account selection, sort and page live in the URL. An analyst who finds something sends a link, and the recipient sees the same result set. This also makes the back button behave the way the user already expects.

## Narrow screens

Criteria move into a drawer below 48rem — measured at the width where six controls stopped fitting in two rows. **Applied filters and the result count stay outside the drawer.** Hiding active criteria behind a closed panel is the single change that makes a filter surface untrustworthy: the numbers on screen no longer explain themselves.

## Accessibility

One `aria-live="polite"` region announces the result count when a query settles. Not the pending state, not each chip removal, not the progress line — one action, one announcement. Chips are removable by keyboard and focus moves to the next chip, or to the filter group when the last one goes.

## Rejected alternative

**Auto-apply everything with optimistic result counts.** It felt faster in a prototype and was rejected: an estimated count that later corrects itself teaches users not to trust any count on the screen. For a surface whose entire job is telling you what you are looking at, a number that might change is worse than a number that takes three seconds.

## Validation

- ✅ Previous result survives every query · ✅ contrast unchanged during refresh
- ✅ First-use and no-results are distinct components · ✅ count matches the displayed set
- ✅ Applied filters visible at every width, drawer open or closed
- ✅ Retry preserves the existing result · ✅ one live region, verified with a screen reader
- ⚠️ The 7-chip collapse threshold is reasoned, not measured against real filter usage

## Remaining risks

- No telemetry on how many criteria users actually combine; the chip threshold may be wrong in both directions
- Cancel is wired to the request but the backend does not honour cancellation, so a cancelled query still consumes capacity
