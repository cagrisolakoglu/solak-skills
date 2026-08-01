# Table / Data Grid

> Before applying these rules, complete the user-task, information-priority and layout stages in `ux-workflow.md`. This reference refines an approved layout — it does not decide which columns the screen needs, or whether a table is the right surface at all.

Decide density first: `density-and-direction.md`.

Numeric alignment, figure sets and identifier treatment come from `typography.md`; this file adds the table-specific behaviour around them.

## Alignment by type

| Data type | Alignment | Note |
|-----------|-----------|------|
| Text, label | Left | — |
| Number, money, percentage | **Right** + `font-variant-numeric: tabular-nums lining-nums` | Digits line up vertically, comparison becomes possible. **No monospace** (`typography.md`) |
| Technical identifier (serial, registry code, UUID, hash) | Left + **monospace** | Read character by character and dictated; not a measured number |
| Date, time | Left, fixed width | One format per table, never mixed |
| Status badge | Left | Colour **cannot be the only indicator** — text or an icon accompanies it |
| Action | Right, last column | Not sortable; may be sticky under horizontal scroll |

```css
.cell-numeric {
  text-align: right;
  font-variant-numeric: tabular-nums lining-nums;
}
```

Left-aligning a number, or using proportional figures, breaks the one job a table has: comparison. The header cell must sit on the **same** axis as the body; if a right-aligned numeric column has a left-aligned header, the eye tracks two different edges.

### The alignment class loses a specificity fight it looks like it should win

A table component that sets a base alignment on its own cells outranks the utility class that does the actual work:

```css
.mini th, .mini td { text-align: start; }   /* (0,1,1) */
.is-num            { text-align: right; }   /* (0,1,0) — loses */
```

Every money column silently falls back to left. Nothing errors, the class is still in the markup, and a code review that greps for `is-num` finds it present. Give the alignment classes the component's own scope so they outrank the base rule, and verify by reading the computed value rather than the stylesheet:

```css
.mini .is-num, .mini .num { text-align: end; font-variant-numeric: tabular-nums lining-nums; }
```

```js
getComputedStyle(cell).textAlign   // must be "end"/"right" — not "what the class says"
```

The same trap sits one level up: **component rules written as bare element selectors** (`table`, `th, td`, `tbody tr:nth-child(even) td`) apply to every table on the page, not the one they were written for. Observed consequences from a single dense-grid rule set leaking: zebra backgrounds painted over another table's scroll cue, a `min-inline-size` intended for a 12-column grid forced a 320px page to scroll sideways, and a sticky `tfoot` detached a small table's total row. A dense-grid rule set is a component. Scope it (`.data-grid table { … }`); do not let it define what a `<table>` is.

## Column priority and narrowing

Sort columns into three priorities: **identity** (which record), **decision** (the value the user came for), **detail** (everything else).

When the screen narrows, **squeezing columns is forbidden.** Three legitimate strategies:

1. **Hide** — drop detail columns, make them reachable by row expansion
2. **Fold** — collapse identity and decision columns into a single two-line cell (mobile card view)
3. **Scroll horizontally** — identity column sticky, the rest scrolls

Whichever is chosen, **declare it explicitly in the report.** An undeclared narrowing behaviour does not pass the verification gate.

### The threshold where horizontal scrolling collapses: identity block > 40%

If the sticky identity block takes more than **40% of the visible width**, the strategy works technically but not practically: at 320px a 34px checkbox plus a 132px name is 166px, leaving ~150px for one data column. The user performs a separate scroll for every value they want to see.

At that width the only legitimate option is **folding** (strategy 2): the row becomes a card, identity becomes the title, decision columns become labelled lines, and detail columns stay behind a "Details" link.

Declaring is not enough: saying "horizontal scroll was chosen" does not prove it is usable at 320px. **Measure it:** identity block width ÷ visible width. If it exceeds the threshold, either write the fold for that width or explicitly state the surface's supported lower bound (e.g. 560px).

## Sticky

- Header row: `position: sticky; top: 0` — mandatory beyond 15 rows
- Identity column: `position: sticky; left: 0` — mandatory whenever horizontal scrolling exists
- A sticky surface must be **opaque**; a translucent header makes the text beneath it unreadable
- Give sticky elements a `z-index`; at the intersection (header × first column) the corner cell must stay on top
- A sticky identity boundary (a vertical rule) only means something **while horizontal scroll exists**; without scrolling it is an unjustified vertical line

### Two mandatory table settings — without them sticky breaks silently

```css
table {
  table-layout: fixed;          /* 1 */
  border-collapse: separate;    /* 2 */
  border-spacing: 0;
  inline-size: 100%;
  min-inline-size: 1216px;      /* below this, horizontal scrolling begins */
}
```

**1 · `table-layout: fixed` plus `<colgroup>`.** Under `auto` layout, `inline-size` on a `td`/`th` is only a *suggestion*; the browser grows the column to fit content. A sticky `left` offset, however, is an exact number. When the two disagree, **content from the scrolled columns leaks out from under the sticky column** — on screen, the trailing digits of a neighbouring column appear beside the checkbox.

The same setting is what makes `text-overflow: ellipsis` work at all: under `auto` layout the column expands to fit, so truncation never triggers.

```html
<colgroup>
  <col class="c-select"><col class="c-name"><col class="c-serial">…
</colgroup>
```

**`fixed` layout has a cost: every column now needs an explicit width, and the table needs a `min-inline-size`.** A column left without a width receives whatever remains — and when the declared widths already exceed the container, that remainder is **zero and the column vanishes**. No ellipsis, no scrollbar, no error: the data is simply gone from the screen. The failure appears only at narrow widths, so it survives every desktop review.

```css
/* ❌ one column has no width; below ~490px it disappears entirely */
table { table-layout: fixed; inline-size: 100%; }

/* ✅ a floor for the table; the container scrolls instead of starving a column */
table { table-layout: fixed; inline-size: 100%; min-inline-size: 640px; }
.table-scroll { overflow-x: auto; }
```

Rule: under `fixed` layout, `colgroup` covers **every** column, and `min-inline-size` is the sum of those widths. Then narrowing produces a scrollbar — a visible, recoverable state — rather than silent data loss.

Any horizontally scrolling container also needs a **visible cue** that content continues; an edge fade on the scroller is enough and costs no layout. Without it users do not learn there is more to the right, and a truncated name reads as the whole value.

Widths live in one place (`colgroup`) and sticky offsets derive from the same tokens:

```css
.c-select { inline-size: var(--w-select); }
.c-name   { inline-size: var(--w-name); }
.col-select { position: sticky; left: 0; }
.col-name   { position: sticky; left: var(--w-select); }   /* offset = the REAL width of the previous column */
```

**2 · `border-collapse: separate`.** Under `collapse`, borders do not belong to the cell; a sticky cell leaves its borders behind as it scrolls and they disappear. The separator job is taken over by zebra striping, or by a faux border drawn with `::after`.

### z-index layers

| Layer | Element |
|-------|---------|
| 1 | Sticky columns in the body |
| 2 | `thead th` and `tfoot td` |
| 3 | Intersections: `thead .col-name`, `tfoot .col-name` |

If the intersection cell is not on top, two sticky surfaces overlap in the corner and the text becomes unreadable.

Every sticky cell must carry **its own opaque fill.** Writing the zebra rule on `td` rather than `tr` gives this for free:

```css
tbody tr:nth-child(even) td { background: var(--surface-zebra); }
tbody tr:nth-child(odd)  td { background: var(--surface-card); }
```

## One separator system

Zebra striping **or** horizontal rules — never both. Together they produce noise and neither does its job.

- **Zebra**: at `dense`, in a many-column table, stops the eye slipping between rows
- **Rules**: cleaner at `comfortable`/`compact`
- **Vertical rules**: only when there are column groups

If zebra is used, hover and selected states must be **stronger** than the zebra, or they are invisible.

**Zebra delta ≥ ~3% lightness.** The difference between `oklch(100%)` and `oklch(98.2%)` disappears on screen — the code says zebra, the user sees a plain table. In a dense, many-column table the smallest perceptible difference is around 3%; measure it separately in dark theme, because a delta that works in light does not necessarily work in dark.

## Overflowing cells

Long text: truncate on one line (`text-overflow: ellipsis`) **and** keep the full value reachable — a `title` attribute or tooltip. Truncating without ever exposing the full value is data loss.

Truncation only works with `table-layout: fixed` (see above). Under `auto` layout the column grows to fit and truncation never fires.

Growing row height to fit content breaks the scanning rhythm at `dense`/`compact`; fixed height plus truncation is preferred.

### Headers are never truncated

`READING T…` is not a header — it destroys the column's key. Cells truncate, headers **never**. Two ways out: widen the column enough for the header, or shorten the header ("Reading type" → "Type"). A truncated header is far more expensive than a truncated cell: a cell makes one record unreadable, a header makes the whole column unreadable.

## Units and casing in headers

Uppercase headers are a common Swiss pattern, but `text-transform: uppercase` silently breaks two things:

**1 · Unit symbols.** `kWh` → `KWH` is wrong: `k` is kilo, `W` is watt, `h` is hour — case carries meaning. `MB` vs `Mb` differs by a factor of eight. Put the unit in its own element:

```html
<th class="is-num">Usage <span class="unit">(GB)</span></th>
```
```css
th { text-transform: uppercase; }
th .unit { text-transform: none; letter-spacing: 0; }
```

**2 · Locale-specific casing.** `text-transform: uppercase` applies locale rules only when the language is declared. Without `lang`, Turkish `i` uppercases to `I` instead of `İ` (`Tip` → `TIP`, `İtirazlı` → `ITIRAZLI`), and other locales have their own cases. A correct `lang` attribute on the root element is **mandatory** — not merely an accessibility setting but a condition for producing the right letters.

## Sorting and selection

- A sortable header must be a `button` (keyboard access)
- **The sortability indicator cannot depend on hover** — touch has no hover, so the indicator would never appear. Keep it persistent but quiet: `opacity: 0.3` for "sortable", `0.6` on hover, `1` for "sorted"
- With an active sort, both the direction arrow **and** which column is sorted stay visible; use `aria-sort`
- Row click and checkbox selection must **not conflict** — if clicking navigates to detail, the checkbox needs to be a separate target
- For bulk selection, state how many records are selected and the scope of "select all" (this page, or all results)

## An in-cell marker breaks number alignment

An anomalous value (a balance that went backwards, an impossible negative, a threshold breach) needs marking — leaving a minus sign as the only cue in a dense column makes it easy to miss. But in a right-aligned column a **glyph does not work**; both attempts fail:

```css
/* ❌ 1: enters the flow → shifts the number left, the column's digit alignment is over */
.is-anomaly::after { content: " ⚠"; }

/* ❌ 2: taken out of flow → preserves alignment, but sits in the empty left side of a
   right-aligned column and reads as belonging to the NEIGHBOURING column ("40 ⚠") */
.is-anomaly { position: relative; }
.is-anomaly::after { content: "⚠"; position: absolute; left: var(--cell-pad-x); }
```

The correct answer is **cell emphasis**: it neither breaks alignment nor leaves ownership ambiguous.

```css
/* ✅ the whole cell is marked; tr td specificity is needed to beat the zebra rule */
tbody tr td.is-anomaly {
  background: var(--danger-quiet);
  box-shadow: inset 2px 0 0 var(--danger);
  color: var(--danger);
  font-weight: 600;
}
```

Because colour is never the only indicator, the minus sign and the row's status label ("Disputed") accompany it; add a `title` explaining the cause ("Current balance is lower than previous — device replacement or misread").

The same rule applies to currency symbols, footnote asterisks and trend arrows: in a right-aligned column, any character added beside the number either shifts the alignment or muddies ownership. The right edge of the digits must stay on **one** vertical line; extra information goes into cell emphasis, a separate column, or a tooltip.

## The total row

If present: `position: sticky; bottom: 0`, a different weight from the body, and number alignment **identical** to the body.

State three things explicitly:

1. **What is being totalled** — the visible page or the whole filtered result: "The total covers all 412 filtered records, not the 50 visible rows."
2. **What is excluded** — "7 unreadable records are not included in the total." A total that treats missing data as zero produces wrong decisions.
3. **Columns that are not totalled** — show `—` in columns where a total is meaningless (balances, rates, dates); do not leave them blank. An empty cell does not distinguish "could not compute" from "not summable".

For rounding discrepancies (sum of displayed values ≠ displayed sum) see `formatting.md`.

## States — design all of them

> Table-specific below. The cross-cutting rules — the state inventory, choosing a feedback surface, refresh vs initial loading, retry naming, undo vs confirmation, conflict and offline — are in `interaction-and-states.md`.

| State | Design |
|-------|--------|
| First use (no data at all) | Explain what this is and suggest the first action. "No records" is not enough. |
| No results (from filters) | **Separate from first use.** Suggest which filter to relax. |
| Loading | Skeleton rows at real row height; **the header row stays real** |
| Partial load | Loaded rows visible, an indicator for the rest |
| Error | What happened plus a retry action; do not empty the table and print one error line |
| Single row | A detail view may suit better — ask |

Solving first use and "no results" with the same component is the most common mistake here: the user cannot tell whether the system is empty or their filter is bad.

In the loading skeleton, **column headers do not load** — they are known. Turning the header row into grey bars hides from the user what is coming, and the layout jitters when the text appears. Skeleton widths should match column widths rather than being random.

## Accessibility

- Use `<table>` with `<th scope="col">`; a `div` grid only when virtualisation demands it, and then with `role="grid"`
- Keyboard: actions reachable by `Tab`; sortable headers are `button`s
- The scroll container itself must be keyboard scrollable: `tabindex="0"` + `role="region"` + `aria-label`. Otherwise only a mouse can reach the columns behind a horizontal scroll
- In a virtualised table, announce the total row count to screen readers — the DOM row count does not reflect reality
- An action visible only on hover is **unreachable by keyboard**; make it visible on `focus-within` too

## Verification

- [ ] `table-layout: fixed` + `colgroup` covering **every** column; `min-inline-size` set so narrowing scrolls instead of starving a column
- [ ] Horizontal scroll has a visible cue (edge fade or persistent scrollbar)
- [ ] Sticky offsets derived from the column width tokens
- [ ] `border-collapse: separate`
- [ ] Screenshot taken **while scrolled**: nothing leaks from under the sticky column
- [ ] z-index layers: body sticky 1, thead/tfoot 2, intersection 3
- [ ] Zebra delta perceptible in both themes (≥ ~3%)
- [ ] No header truncated
- [ ] Unit symbol casing preserved; a correct `lang` attribute on the root element
- [ ] Sort indicator visible without hover
- [ ] In numeric columns every digit's right edge is on the same line (markers out of flow or replaced by cell emphasis)
- [ ] Total row: what is summed, what is excluded, which columns are not summable — all three stated
- [ ] Identity block ÷ visible width measured; at widths exceeding 40% a fold exists or a lower bound is declared
