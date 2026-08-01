# Dashboard / Metric Summary

> Before applying these rules, complete the user-task, information-priority and layout stages in `ux-workflow.md`. This reference refines an approved layout — the question each tile answers is decided there, not here.

KPI value, comparison and context type treatment comes from `typography.md`.

## Every tile answers one question

When adding a tile, write its question down: "How far behind target are we this month?" If the question cannot be written, remove the tile.

Twelve boxes of equal weight are not a hierarchy, they are an inventory. A dashboard's job is to determine the user's **next action**.

## Unequal composition

A bento layout is not made of equal cells — a difference in importance shows up as a difference in size.

```css
.dashboard {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  grid-auto-rows: minmax(var(--tile-row), auto);   /* not a fixed row height — see below */
  gap: var(--space-tile);
}
.tile--primary { grid-column: span 2; grid-row: span 2; }  /* headline metric */
.tile--wide    { grid-column: span 2; grid-row: span 2; }  /* trend + chart */
.tile--unit    { grid-column: span 1; }                    /* supporting metric */
.tile--pair    { grid-column: span 2; }
.tile--full    { grid-column: span 4; }
```

An equal grid is not bento, it is just a grid. `minmax(0, 1fr)` matters: `1fr` on its own lets overflowing content inflate the column.

### A fixed row height makes content escape the tile

`grid-auto-rows: var(--tile-row)` looks like the right way to get a consistent row unit. It is not: a tile whose content is taller than the row **overflows its own boundary**. The button or the reason text renders *below the tile's border*, floating on the page background. No clipping, no scrollbar, no error — the tile simply stops containing its contents.

```css
grid-auto-rows: var(--tile-row);                 /* ❌ content escapes the border */
grid-auto-rows: minmax(var(--tile-row), auto);   /* ✅ row unit is a floor, tiles can grow */
```

The failure is width-dependent: at narrow widths, where rows are `auto` anyway, everything looks correct. It only appears at the width where the row unit binds — which is usually the one width that gets reviewed least.

### Cell arithmetic has to close

If the sum of all spans is not a multiple of the column count, the grid ends with a **hole** in the last row. It reads as a tile that failed to load.

```
4 + 1 + 1 + 1 + 1 + 4 + 1 + 1 + 2 = 16 in a 4-column grid → 4 cells short of 20 → hole
```

Fix it by arithmetic, not by nudging order: widen one tile to close the row, or drop a tile that was not answering a question anyway. A trailing hole is a signal that the tile inventory was never counted.

## KPI anatomy

Four parts, in this order:

1. **Label** — what is measured, with its unit
2. **Value** — the largest step in the scale, tabular lining figures
3. **Change** — direction plus magnitude; **colour cannot be the only indicator** (an arrow icon or sign accompanies it)
4. **Context** — compared to what: "vs last month", "8% below target"

```html
<article class="tile">
  <h3 class="tile-label">Monthly usage <span class="tile-unit">GB</span></h3>
  <p class="tile-value">184,320</p>
  <p class="tile-delta tile-delta--up">
    <svg aria-hidden="true"><!-- up arrow --></svg>
    12.4% <span class="tile-context">vs last month</span>
  </p>
</article>
```

**A number without context is not information.** "184,320" on its own lets the user decide nothing.

## Threshold colours are semantic, and colour is never the only indicator

```css
:root {
  --status-ok:       oklch(62% 0.15 150);
  --status-warn:     oklch(72% 0.16  75);
  --status-critical: oklch(58% 0.20  25);
}
```

Every status colour is paired with an **icon or text**. Colour blindness aside, colour disappears in greyscale output and on dim screens.

Also: a metric going "up" is not always good (cost, failure count, latency). **The arrow carries direction, the colour carries good/bad** — do not conflate them.

### But good/bad cannot live in colour alone

That split has a hole in it, and the greyscale test finds it immediately. Remove colour and `▲ +3.1%` and `▼ −4` read identically: the direction survives in the arrow shape, the **judgement disappears**. Which means it was carried by a channel that colour-blind users, greyscale printouts and dim screens never receive.

So the context line has to state the judgement in words:

```html
<!-- ❌ direction only; "is this bad?" is answered by hue alone -->
+3.1% <span class="tile__context">vs last month</span>

<!-- ✅ the judgement survives without colour -->
+3.1% <span class="tile__context">vs last month · drifting above budget</span>
−4    <span class="tile__context">vs last week · clearing faster than arriving</span>
```

This is not verbosity: "vs last month" is a comparison, not an interpretation, and a KPI tile exists to produce an interpretation. If the judgement cannot be written in three words, the tile is probably not answering a question (see the top of this file).

### An error or status tile needs an icon, not just a tinted surface

A tile marked only by `--danger` border plus `--danger-quiet` fill becomes, in greyscale, a **slightly grey box** — indistinguishable from a normal tile. The word "Unavailable" carries the meaning, but the tile no longer reads as an error at a glance, which is the entire point of a dashboard.

Put the icon in the tile label, beside the text. One 13px glyph is enough and it is the only cue that survives every rendering condition.

## Restraint on a dashboard

This is where decoration accumulates fastest. Four rules:

- **The tile is a boundary, not an object.** One quiet border or one sunken surface — not a border *and* a shadow *and* a gradient.
- **One elevation level, and only if something floats.** Static tiles do not need shadows (`design-quality.md`).
- **Do not colour tiles by category.** Tile colour is reserved for threshold status; a palette of category colours means status has nowhere left to speak.
- **Do not repeat the unit in every part.** Unit goes in the label; the value stays clean.

## Sparklines

- No axes, no labels; the job is to show the shape of a trend
- Mark the last value with a point
- Never a substitute for the number — always shown alongside the value
- Height 24-40px; smaller makes the shape unreadable
- If the Y axis does not start at zero, say so; otherwise small variation looks dramatic

### Bound the width, and never use `preserveAspectRatio="none"`

A sparkline's shape only means something at a known aspect ratio. Let it fill a wide tile and it stretches horizontally: a 200×34 viewBox rendered into 740×34 multiplies the horizontal scale by 3.7 while the vertical stays fixed, so every slope flattens. The thing that exists to show a trend ends up showing a straight line.

```css
/* ❌ full-bleed, non-uniform: the trend disappears */
.spark { inline-size: 100%; block-size: 34px; }           /* + preserveAspectRatio="none" */

/* ✅ bounded width, uniform scaling: the shape is preserved */
.spark { inline-size: 100%; max-inline-size: 220px; block-size: 38px; }
```

Drop `preserveAspectRatio="none"` from the markup. If a sparkline genuinely must span a wide tile, the path has to be generated for the rendered width — stretching a fixed path is not the same thing.

## When a chart is needed

Chart type, categorical palette limits, axes and tooltip rules live in the **"When a chart is needed"** section of `design-quality.md`. This skill builds charts with its own rules; no external skill is required.

Two rules specific to charts inside a tile:

- **A tile chart carries no axes.** The tile's job is to answer one question; an axed, labelled chart is a different component.
- **A chart never replaces the number.** The trend shape always accompanies a value; the user must be able to read a number off the tile.

## States

> Tile-specific below. Freshness wording, refresh that preserves the current view, retry naming, background operations and the state inventory are in `interaction-and-states.md`.

| State | Design |
|-------|--------|
| No data | Keep the tile structure; instead of a value, "no data" plus the reason |
| Partial data | State which period is missing |
| Loading | Skeleton at tile size — no layout shift |
| Stale data | Last-updated time visible; it must not be mistaken for live |
| Error | Inside the tile, without emptying the whole dashboard |

**Never render missing data as zero.** This is the most expensive mistake on dashboards: it leads to wrong decisions. Zero is a measurement; absence of data is not.

## Layout and reading order

- Most important metric top-left (left-to-right reading)
- Related metrics adjacent
- A dashboard should fit one screen; if it needs scrolling there are probably two dashboards
- At `320px` it collapses to one column; the order stays the order of importance

## Verification

- [ ] Every tile's question can be written in one sentence
- [ ] Composition is unequal; span sizes communicate importance
- [ ] `grid-auto-rows: minmax(row, auto)` — no content escaping a tile boundary at any width
- [ ] Span arithmetic closes; no hole in the last row
- [ ] Every delta's good/bad readable **without colour** (stated in the context line)
- [ ] Error and status tiles carry an icon, not only a tinted surface
- [ ] Sparkline width bounded; no `preserveAspectRatio="none"`; value always shown alongside
- [ ] Missing data shown as such, never as zero; partial data names the missing period
- [ ] Last-updated time visible; stale tiles say they are stale
- [ ] Loading skeletons at tile size with real labels
- [ ] Greyscale screenshot taken and checked
- [ ] Fits one screen; at 320px collapses to one column in importance order

## Accessibility

- Each tile is an `article` with a heading (`h3`); a screen reader must be able to enumerate tiles
- Decorative icons `aria-hidden="true"`; any icon carrying meaning needs a text equivalent
- Auto-refreshing values use `aria-live="polite"` — but turn it off for frequent refreshes, constant announcements are hostile
- Sparklines are `aria-hidden`; state the trend in text too ("up over the last 7 days")
