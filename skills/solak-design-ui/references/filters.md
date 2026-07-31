# Filter / Search / Query Panel

## Applied filters are the single source of truth

The user must see **at all times** what is applied. Applied filters are listed as chips that stay visible even when the panel is closed, and each chip can be removed on its own.

Filter state buried inside a panel, disappearing when the panel closes, is the most common mistake here: the user looks at partial data and believes it is complete.

```html
<div class="applied-filters" aria-live="polite">
  <span class="filter-chip">
    Region: North
    <button type="button" aria-label="Remove region filter">×</button>
  </span>
  <button type="button" class="filter-clear">Clear all</button>
</div>
```

`aria-live="polite"` matters: a filter change must be announced to screen readers.

## State belongs in the URL

Filters, sort, page and search query are written to the URL. Three things this buys: the screen can be shared, the back button behaves as expected, and state survives a refresh.

Keeping filter state only in component state loses all three.

## Filtering and searching are different jobs

- **Search**: free text, matches across several fields, narrows as you type
- **Filter**: a known field with a known set of values, a deliberate choice

Loading both onto one input makes both vague. If both are needed, separate them visually and make clear how they combine (does search look within the filtered set, or override the filters?).

## Result count feedback

The effect of an applied filter is visible **as a number**: "1,284 records · 3 filters active". Where possible show the estimated count before the filter is applied — the user should not discover the outcome in an empty list.

Disabling options that would produce zero results, or marking them "(0)", prevents the wasted attempt entirely.

## Expensive filters

When a filter hits the server or is otherwise slow:

- Debounce typed input (250-400ms); no query per keystroke
- **Show that it is pending** — dim the current result, do not collapse to a skeleton
- Keep the old result on screen and swap it when the new one arrives (stale-while-revalidate); do not empty and wait
- If it is very expensive, use an explicit "Apply" button instead of auto-applying — and then show that unapplied changes exist

## The "no results" state — never leave a dead end

If the result is empty, say **which filter is responsible** and offer a way out:

> No records match these criteria. **Date range** (last 7 days) is the most restrictive filter — try widening it.
> [Widen to last 30 days] [Clear all filters]

Leaving the user to guess which filter to remove is the most common point of abandonment.

## Reset and saved views

- "Clear all" is always reachable and is a single action
- For repeated queries, saved views: named and shareable (the URL already carries the state)
- The default view is stated explicitly — the user must know how to get back to a "clean" state
- If a filter is applied by default (e.g. "active records only"), **show it as a chip**; a hidden default filter misleads the user

## Restraint in the panel

A filter panel is where control inflation starts. Three rules:

- **One control per criterion.** A date range is one control, not two disconnected inputs sitting next to each other.
- **Do not frame every criterion.** Grouping comes from spacing and a group label, not from a box around each field (`design-quality.md`).
- **Do not colour chips by category.** Chips are already distinguished by their text; a palette of chip colours turns the panel into confetti and spends colour that status needs.

## Accessibility

- Filter groups use `fieldset` + `legend`
- The chip remove button says which filter it removes via `aria-label`
- The result count lives in an `aria-live` region
- If the panel expands and collapses, use `aria-expanded`; return focus to the trigger on close
