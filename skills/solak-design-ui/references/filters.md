# Filter / Search / Query Panel

> Before applying these rules, complete the user-task, information-priority and layout stages in `ux-workflow.md`. This reference refines an approved layout — it does not decide which criteria the user actually filters by, or whether the panel belongs on this screen.

Chip values, result counts and pending-state type treatment come from `typography.md`.

## Applied filters are the single source of truth

The user must see **at all times** what is applied. Applied filters are listed as chips that stay visible even when the panel is closed, and each chip can be removed on its own.

Filter state buried inside a panel, disappearing when the panel closes, is the most common mistake here: the user looks at partial data and believes it is complete.

```html
<ul class="applied-filters" aria-label="Applied filters">
  <li class="filter-chip">
    Region: <strong>Northern Europe</strong>
    <button type="button" aria-label="Remove region filter">×</button>
  </li>
  <li><button type="button" class="filter-clear">Clear all</button></li>
</ul>
```

### A chip is never truncated

The value is the entire point of a chip. `max-inline-size` plus `text-overflow: ellipsis` clips the **end** of the text — which is exactly where the value sits:

```
❌ Date: 01.07.2026 – 3…      the applied range is unreadable
❌ Region: Northern Eu…       two regions could start the same way
❌ Channel: Partner por…
```

A chip that cannot be read is worse than no chip: the user believes they can see the filter state while they cannot. If chips do not fit, in this order:

1. **Let them wrap** to more lines — chips are short, wrapping is cheap
2. **Shorten the label, never the value** — `Customer: Enterprise` instead of `Customer type: Enterprise`; drop the label entirely when the value is self-describing
3. **Merge several values of one criterion into one chip** — `Status: Pending, Partially shipped` rather than two chips. This is also the correct semantics: removing that chip removes the status filter, not one of its values

### One live region per screen

Do **not** put `aria-live` on both the chip list and the result count. One user action then produces two announcements, and the second interrupts the first. The **result count** is the canonical live region — it is what actually changed. The chip list gets an `aria-label`; each remove button already says what it removes.

### At narrow widths the chip stack becomes the whole screen

Eight chips at 320px is roughly 250px of vertical space: the panel and the results end up entirely below the fold, and the first thing the user meets is a wall of chips.

Measure it, do not assume: **chip region height ÷ viewport height.** Past roughly a quarter of the viewport, collapse it — below the breakpoint, replace the chips with one summary line that says how many filters are active and opens the panel.

```html
<p class="applied-summary">
  <strong>7 filters active</strong> <span>+ archived excluded</span>
  <button type="button" aria-expanded="false" aria-controls="filter-panel">Show filters</button>
</p>
```

The count in that summary and the count in the result strip must be **the same number, counted the same way** (see below).

## State belongs in the URL

Filters, sort, page and search query are written to the URL. Three things this buys: the screen can be shared, the back button behaves as expected, and state survives a refresh.

Keeping filter state only in component state loses all three.

## Filtering and searching are different jobs

- **Search**: free text, matches across several fields, narrows as you type
- **Filter**: a known field with a known set of values, a deliberate choice

Loading both onto one input makes both vague. If both are needed, separate them visually and make clear how they combine (does search look within the filtered set, or override the filters?).

## Result count feedback

The effect of an applied filter is visible **as a number**: "1,284 records · 3 filters active". Where possible show the estimated count before the filter is applied — the user should not discover the outcome in an empty list.

**The filter count must agree everywhere it appears.** If the chips show seven and the result strip says eight, the "single source of truth" claim is already broken and the user cannot tell which number to trust. Decide once how a default filter is counted — either counted and named, or excluded and named — and use that same arithmetic in the chips, the summary line and the result strip:

```
7 filters active + archived excluded          ✅ consistent, and the default is visible
8 filters active                              ❌ which eight? the chips show seven
```

Disabling options that would produce zero results, or marking them "(0)", prevents the wasted attempt entirely. The "(0)" is not decoration: it is the **non-colour cue** that makes the disabled state legible. A disabled option distinguished only by faded ink disappears in dark theme, where surface lightness compresses (`tokens.md`) — the count is what still reads.

## Expensive filters

When a filter hits the server or is otherwise slow:

- Debounce typed input (250-400ms); no query per keystroke
- Keep the old result on screen and swap it when the new one arrives (stale-while-revalidate); do not empty and wait
- **Show that it is pending** — but see the next section for how
- If it is very expensive, use an explicit "Apply" button instead of auto-applying — and then show that unapplied changes exist

### Staleness is announced, not dimmed

> This is the canonical statement of the rule; `interaction-and-states.md` cites it and adds the general loading taxonomy, retry naming and offline behaviour.

The obvious implementation of "show it is pending" is `opacity` on the result region. **It fails the contrast gate.** `opacity: 0.45` on a table drags every value below 4.5:1 at once, and it is worst in dark theme where muted ink already sits close to the surface. The user is asked to read numbers that are no longer readable — in exchange for information that a single line of text conveys better.

```css
/* ❌ the whole result becomes illegible; every ink token loses its ratio */
.results--stale table { opacity: 0.45; }

/* ✅ full contrast preserved; the banner and the region border carry the message */
.results--stale .results__frame { border-color: var(--warn); }
.results--stale .stale-flag { display: flex; }   /* "Showing the previous result while the new query runs." */
```

Three carriers that cost no legibility:

1. **A labelled banner** above the region, stating in words what is being shown and why
2. **The region border** switched to the warning colour — a boundary already exists, so this adds no new device
3. **An indeterminate progress line** on the container's edge (2px). This is motion carrying information, which is the one legitimate use (`design-quality.md`) — and it needs a `prefers-reduced-motion` counterpart

If opacity is used at all, it must be verified against the contrast floor, applied only to strong ink, and never stacked on already-muted text. In practice the banner is enough and the dimming is not worth its cost.

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

### A selected view that no longer matches must say so

Once a saved view is selected and the user changes a filter, the view chip still looks selected while the screen no longer shows that view. The user then believes they are looking at "Pending this month" when they are looking at something else — and may save, share or report from it.

```html
<button type="button" aria-pressed="true">Pending this month <span class="view-mod">· modified</span></button>
```

Mark the divergence on the view itself, not only in the panel. "Unapplied changes exist" inside the panel is a different statement: one is about the query not having run yet, the other about the result no longer being the saved view. A long-lived screen needs both.

## Restraint in the panel

A filter panel is where control inflation starts. Three rules:

- **One control per criterion.** A date range is one control, not two disconnected inputs sitting next to each other.
- **Do not frame every criterion.** Grouping comes from spacing and a group label, not from a box around each field (`design-quality.md`).
- **Do not colour chips by category.** Chips are already distinguished by their text; a palette of chip colours turns the panel into confetti and spends colour that status needs.

## Accessibility

- Filter groups use `fieldset` + `legend`
- The chip remove button says which filter it removes via `aria-label`
- The result count lives in an `aria-live` region — and it is the **only** one on the screen
- If the panel expands and collapses, use `aria-expanded`; return focus to the trigger on close
- A range is one control but two inputs: each still needs its own accessible name ("Order date from", "Order date to"); the `–` separator is `aria-hidden`

## Verification

- [ ] Applied filters visible with the panel closed; each removable on its own
- [ ] No chip truncated; long chips wrap, labels shortened rather than values
- [ ] Several values of one criterion in one chip, not one chip per value
- [ ] Exactly one `aria-live` region (the result count)
- [ ] Chip region measured against viewport height; collapsed to a summary line at narrow widths
- [ ] Filter count identical in chips, summary and result strip; default filters counted the same way in all three
- [ ] Default-applied filters shown, not hidden
- [ ] Pending state announced by banner/border/progress — **not** by lowering contrast
- [ ] Zero-result options disabled and marked "(0)"; the count is present as the non-colour cue
- [ ] Zero-result state names the responsible filter and offers a way out
- [ ] A selected saved view that no longer matches is marked as modified
- [ ] Search and filtering visually separated, with their relationship stated
- [ ] Filter state in the URL: shareable, back button works, survives refresh
