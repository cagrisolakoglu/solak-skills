# Dashboard / Metric Summary

## Every tile answers one question

When adding a tile, write its question down: "How far behind target are we this month?" If the question cannot be written, remove the tile.

Twelve boxes of equal weight are not a hierarchy, they are an inventory. A dashboard's job is to determine the user's **next action**.

## Unequal composition

A bento layout is not made of equal cells — a difference in importance shows up as a difference in size.

```css
.dashboard {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: var(--space-tile);
}
.tile--primary { grid-column: span 2; grid-row: span 2; }  /* headline metric */
.tile--wide    { grid-column: span 2; }                    /* trend */
.tile--unit    { grid-column: span 1; }                    /* supporting metric */
```

An equal grid is not bento, it is just a grid. `minmax(0, 1fr)` matters: `1fr` on its own lets overflowing content inflate the column.

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

## When a chart is needed

Chart type, categorical palette limits, axes and tooltip rules live in the **"When a chart is needed"** section of `design-quality.md`. This skill builds charts with its own rules; no external skill is required.

Two rules specific to charts inside a tile:

- **A tile chart carries no axes.** The tile's job is to answer one question; an axed, labelled chart is a different component.
- **A chart never replaces the number.** The trend shape always accompanies a value; the user must be able to read a number off the tile.

## States

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

## Accessibility

- Each tile is an `article` with a heading (`h3`); a screen reader must be able to enumerate tiles
- Decorative icons `aria-hidden="true"`; any icon carrying meaning needs a text equivalent
- Auto-refreshing values use `aria-live="polite"` — but turn it off for frequent refreshes, constant announcements are hostile
- Sparklines are `aria-hidden`; state the trend in text too ("up over the last 7 days")
