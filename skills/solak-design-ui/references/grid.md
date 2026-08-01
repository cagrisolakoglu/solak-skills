# The Column Grid

> This file is the column grid **inside a surface**: spans, cell sizing, row semantics. How the *page composition* rearranges as available width changes — region priorities, minimum usable widths, container queries, breakpoint selection — is `responsive-grid.md`. On a multi-region screen both are read.

Density sets **vertical** rhythm, the grid sets **horizontal** rhythm. Missing either one makes a surface look scattered — even when every field is individually the right size.

Symptom: each field's width is reasonable for its own content, but no field's left or right edge lines up with any other, and on a wide screen the right half of the surface is dead space. That is the signature of a form built from **content-width flex**.

## Tokens

Column count and gutter are root-level tokens like density, not component decisions.

```css
:root {
  --grid-cols: 12;
  --grid-gutter: 20px;
  --grid-row-gap: var(--space-field);
  --content-max: 76ch;        /* reading column ceiling */
}

[data-density="dense"]       { --grid-gutter: 12px; }
[data-density="comfortable"] { --grid-gutter: 24px; }

.grid {
  display: grid;
  grid-template-columns: repeat(var(--grid-cols), minmax(0, 1fr));
  gap: var(--grid-row-gap) var(--grid-gutter);
}
/* span is always expressed through grid-column-END — reason below */
.col-2  { grid-column-end: span 2; }
.col-3  { grid-column-end: span 3; }
.col-4  { grid-column-end: span 4; }
.col-5  { grid-column-end: span 5; }
.col-6  { grid-column-end: span 6; }
.col-7  { grid-column-end: span 7; }
.col-12 { grid-column-end: span 12; }
.start-1 { grid-column-start: 1; }   /* starts a new row */
```

`minmax(0, 1fr)` is mandatory: `1fr` on its own lets overflowing content (a long option label, an unwrapped number) escape the column.

## Trap: `grid-column: span N` and starting a row cancel each other

The `grid-column: span 6` shorthand writes `span 6` into the **start** value and leaves end as `auto`. When `grid-column-start: 1` is then applied to the same element to start a new row, the span information is erased and the field collapses to **one column**. Symptom: every field the same absurdly narrow width, with select and input text clipped.

```css
/* ❌ span gets overwritten by .start-1 */
.col-6  { grid-column: span 6; }
.start-1 { grid-column-start: 1; }

/* ✅ start and end are separate properties and do not collide */
.col-6  { grid-column-end: span 6; }
.start-1 { grid-column-start: 1; }
```

This breakage is caught only by screenshot — the CSS is valid and silent. After moving to a grid, **always capture an image.**

## Trap: `max-inline-size` is not a media query feature

Logical properties (`inline-size`, `max-inline-size`) are correct in component CSS, but they have **no media query equivalent** — `@media (max-inline-size: 900px)` silently never matches. Use `max-width` in media queries and `inline-size` in container queries.

```css
@media (max-width: 900px) { :root { --grid-cols: 6; } }            /* ✅ */
@container (max-inline-size: 900px) { :root { --grid-cols: 6; } }  /* ✅ container query */
```

## Reconciliation: column alignment and character width do not conflict

The forms reference says "field width matches its content" (a postcode is not full width); the grid says "edges line up". These do not conflict — there is a **division of labour**:

| Who | Decides |
|-----|---------|
| The grid column | The cell's **left edge** and the space allotted to it |
| `max-inline-size: Nch` | How much of that cell the field **fills** |

```css
.field { min-inline-size: 0; }              /* prevents overflow inside a grid cell */
.field input { inline-size: 100%; }
.field--code   { max-inline-size: 11ch; }   /* period, rate */
.field--date   { max-inline-size: 13ch; }
.field--serial { max-inline-size: 16ch; }
```

Left edges sit on the column line while the width still communicates the expected character count. Widening a field unnecessarily to align its right edge is **wrong** — what aligns is the column line, not the field box.

## The cell's span is set by its widest content, not by the input

A cell holds three things: label, input, and help or error text. The span is decided by **whichever needs the most measure** — and that is usually not the input, but the text.

Symptom: an 11-character field was given `col-2`, and the help text beneath it is squeezed into a 28-character ribbon that wraps onto two lines, while **empty columns** sit right beside it. If text is flowing through a narrow ditch with space next to it, the span is wrong.

```html
<!-- ❌ span sized to the input: help text wraps, 9 empty columns to the right -->
<div class="field col-2">
  <label for="period">Period</label>
  <input class="w-code" id="period" value="2026-07" readonly>
  <p class="field-hint">Open period. Closed periods cannot be edited.</p>
</div>

<!-- ✅ span sized to the text; the input stays 11ch via max-inline-size -->
<div class="field col-4">…same content…</div>
```

```css
.field-hint, .field-error { max-inline-size: 46ch; }   /* does not exceed reading measure even in a wide cell */
```

Rule: **give a cell carrying help or error text at least ~34ch.** The text's measure is the cell's job; the input's measure is `max-inline-size`'s job — they are not the same number.

Stretching the help text to the end of the row is not an alternative: it would start at the input's left edge and end at a right edge that aligns with nothing.

## Choosing spans

Fields on the same row add up to the column count; leftover space is left as empty columns, not distributed among the fields.

```html
<div class="grid">
  <div class="field col-6">…Customer…</div>
  <div class="field col-4">…Plan…</div>
  <!-- remaining 2 columns intentionally empty -->

  <div class="field col-4 start-1">…Period…</div>
  <div class="field col-3">…Record date…</div>
  <div class="field col-5">…Recorded by…</div>
</div>
```

Rule: **do not hand the row's leftover space to the last field.** Spreading "Recorded by" across 6 columns makes it look as important as "Customer"; hierarchy speaks through span.

## Related fields share a span

Fields meant to be compared (previous balance / current balance, start date / end date, min amount / max amount) get **equal spans**. A different span announces an importance difference that does not exist.

## A row is a semantic unit

Fields on the same row tell the user "these are the same kind of thing". When kinds mix, the row carries no information and merely fills space.

A usage-record form has three kinds, each taking its own row:

| Row | Fields | Why together |
|-----|--------|--------------|
| Fixed attributes | Serial number, Rate | Independent of the reading, unchanged for the record's life |
| Readings | Previous balance, Current balance | A pair to be compared → **equal span** |
| Derived | Computed amount, Trailing average | Not inputs, but results |

Putting the serial number on the same row as the previous balance implies they are the same kind of value; one is an identifier, the other a measurement. Splitting the row is not lost space, it is gained information.

The converse also holds: a narrow field alone on a row announces a **deliberate boundary**. More than two or three such rows in one group is not boundary-setting but disorder — reconsider the grouping.

## Narrowing: column count drops, spans are remapped

Setting each field to `100%` does not fix the grid, it destroys it. Reduce the column count; spans adapt.

```css
@media (max-width: 900px) { :root { --grid-cols: 6; }
  .col-4 { grid-column-end: span 3; }
  .col-5, .col-6, .col-7, .col-12 { grid-column-end: span 6; } }
@media (max-width: 560px) { :root { --grid-cols: 1; }
  [class*="col-"] { grid-column-end: span 1; } }
```

**Any span left larger than the column count overflows silently.** In a 6-column grid an unmapped `span 7` creates an implicit column; the grid becomes 7 columns wide and the surface hangs outside its container. No error, nothing in the console — visible only in a screenshot. When writing the narrowing rules, count **every** span class and do not forget the largest one in use.

`max-inline-size` **stays** on fields that collapse to one column — a serial-number field should not be full width on a phone either; otherwise it feels misaligned against the touch keyboard. Only help text and error text expand to full width.

## Dead space is a grid problem

If content clusters left on a wide screen and the right half sits empty, there are two legitimate fixes and **no third** (widening fields unnecessarily is not a fix):

1. **Narrow the container** — bound the form card with `--content-max`, centred or pinned left. Preferred for long forms.
2. **Fill the side column** — put **real** content there: a summary, recent records, a validation list. If content is being invented to fill it, go back to option 1.

A real field that has not loaded yet is also content: a "Trailing average" skeleton legitimately fills the empty columns beside a computed-value block, because the user knows that value is coming. But a tile added only to close a gap, or a repeated summary, is filler.

## Label and field alignment

With labels above fields, the label's left edge must be **the same** as the field's left edge, i.e. the column line. A label inset with `padding-inline-start` visibly breaks the grid.

## Verification

- [ ] Every field starts on a column line (check with the browser's grid overlay)
- [ ] Compared fields have equal spans
- [ ] Row leftovers sit in empty columns, not spread into the last field
- [ ] Cells carrying help or error text are ≥ 34ch; text does not wrap into a narrow ribbon
- [ ] Each row carries one kind of field (identifier / measurement / derived not mixed)
- [ ] Narrowing is done by column count, not per-field `100%`
- [ ] **Every** span class remapped when narrowing; no span exceeds the column count
- [ ] No dead space on wide screens: either the container is bounded or the side column holds real content
