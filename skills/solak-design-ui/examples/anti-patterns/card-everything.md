# Card everything

Canonical reference: `design-quality.md`, with the grouping rules in `layout-and-information-architecture.md`.

## Bad implementation

Every group gets a frame. Every frame gets a border, a shadow and a radius. Rows become cards because cards look modern.

```html
<div class="card">
  <div class="card">
    <div class="card"><label>Account</label><input></div>
    <div class="card"><label>Period</label><input></div>
  </div>
  <div class="card"><h3>Readings</h3>
    <div class="card"><label>Previous</label><input></div>
  </div>
</div>
```

```css
.card { border: 1px solid #e5e5e5; border-radius: 8px; box-shadow: 0 1px 3px rgb(0 0 0 / 8%);
        background: linear-gradient(#fff, #fafafa); padding: 16px; }
```

On a table, the same instinct turns 400 rows into 400 bordered tiles on a desktop viewport.

## Why it fails

A border is a claim that what is inside belongs together and what is outside does not. When everything is bordered, the claim is made everywhere and therefore says nothing — the user gets no grouping information at all, only visual noise.

Concretely:

- **Nested frames compound.** Three levels of border and shadow put 6px of decoration between two fields that are one idea, and the eye reads the gaps as separations.
- **Padding stacks.** Each level adds its own, so the content area shrinks while the page grows. Users scroll more to see less.
- **Density dies.** A table that fits 30 rows on screen fits 8 as cards, and a scanning task becomes a scrolling task.
- **Row cards break comparison.** The one job a table does is align values in a column so the eye can compare them. Cards destroy that alignment, which is why they belong on narrow screens where the column is gone anyway — and nowhere else.
- **Shadow plus border plus gradient is three separators doing one job**, at three times the rendering and reading cost.

## Correct direction

Group with **space first**. A larger gap between groups than within them communicates the same structure with nothing drawn.

```css
.form   { display: grid; gap: var(--space-group); }   /* between groups */
.group  { display: grid; gap: var(--space-field); }   /* within a group */
```

Escalate only when space is not enough: a hairline rule, then a surface change, then a border. Reach for a border when the group is genuinely separable — a panel that scrolls independently, a dialog, a tile whose whole point is being one unit.

**One separator system per surface.** Zebra or rules, not both. Border or shadow, not both.

Rows fold to cards **below a measured width**, when the columns no longer fit — never on desktop as a style choice.

## Detection checklist

- [ ] Is any bordered element inside another bordered element?
- [ ] Does a single component carry a border *and* a shadow *and* a gradient?
- [ ] Would removing the border lose information, or only decoration?
- [ ] Could the same grouping be shown by adjusting two gap values?
- [ ] On a table: are rows carded at a width where the columns still fit?
- [ ] Count the visible frames on the screen. Over about six, the frames have stopped meaning anything.
- [ ] Is the radius the same everywhere, applied because it is the default rather than chosen?
