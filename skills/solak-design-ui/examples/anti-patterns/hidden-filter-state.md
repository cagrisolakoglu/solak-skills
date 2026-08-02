# Hidden filter state

Canonical reference: `filters.md`, with the loading taxonomy in `interaction-and-states.md`.

## Bad implementation

The criteria live behind a button. The result does not explain itself.

```html
<button>Filters (3)</button>
<p>412 results</p>
<table>…</table>
```

```js
// Applied on mount, never shown anywhere.
const DEFAULTS = { period: 'last-7-days', status: 'active', region: userRegion };
```

```css
/* One component for both empty conditions. */
.empty::before { content: "No records found"; }
```

## Why it fails

- **"Filters (3)" names a count, not a state.** Three *what*? The user has to open the drawer to learn what they are looking at, and then close it to look at it — the surface makes them choose between the criteria and the result.
- **Hidden defaults are indistinguishable from bugs.** A user who never chose `region = theirs` sees a number that is wrong for the question in their head, and has no way to discover why. This is the most common cause of "the data is broken" reports that turn out to be filters.
- **One empty component for two conditions.** "No records found" cannot tell the user whether the system has no data or their query excluded all of it. Those need opposite actions — provision something, or relax something — and the screen offers neither.
- **Loading and no-results look identical.** A slow query that clears the table produces exactly the same screen as a query with no matches, so users learn to distrust both.
- **The count can drift from the table.** When the count comes from one request and the rows from another, a truncated or partially failed result shows 412 above 50 visible rows and no statement of what the 412 counts.
- **Truncated chips lose the value.** `Account: 4 sel…` tells the user there is a filter and not what it does.

## Correct direction

Applied criteria are visible **outside** any drawer, at every width, carrying their values:

```text
[Period: 2026-07 ×] [Status: pending ×] [Region: North (default)]  [Clear all]
                                              412 of 40,318 records
```

- Chips carry the **value**, not the field name.
- Defaults nobody chose appear as implicit chips, styled differently, not removable, and labelled as defaults.
- Above ~7 chips, collapse to a summary line with a count and an expander — a chip wall is its own scanning problem.
- The count states its scope: `412 of 40,318`, and if some records failed to load, `405 of 412 loaded · 7 unavailable`.

Two separate empty components:

| Condition | Copy | Recovery |
|-----------|------|----------|
| First use | "No records have been imported for this period." | Import · How this works |
| No results | "**Status: pending** takes the result from 412 to 0." | Remove that filter · Widen the period |

The no-results copy names the **most restrictive** criterion, which means computing it rather than listing all of them.

Loading keeps the previous result on screen with a stated pending line, so it can never be mistaken for emptiness (`interaction-and-states.md`).

## Detection checklist

- [ ] Can the user see which criteria produced the visible result without opening anything?
- [ ] Does every chip show its **value**, untruncated?
- [ ] Are filters applied on mount that the user never chose, and are they visible?
- [ ] Do first-use and no-results render through the same component?
- [ ] Does the no-results copy name a specific criterion, or just say "no results"?
- [ ] On a narrow screen, do the applied filters disappear with the drawer?
- [ ] Does the displayed count state what it counts, and does it match the rows?
- [ ] During a slow query, is the screen distinguishable from an empty result?
