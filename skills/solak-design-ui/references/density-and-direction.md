# Density and Direction

> Decide density and direction only after the layout skeleton exists: both depend on data volume and usage behaviour, which come out of `ux-workflow.md` Stages 2-4.

In data-dense UI the **density decision matters more than the style direction.** The same table is a different product at `comfortable` than at `dense`. Make this call first.

## The density scale

| Level | Row / field height | Body text | When |
|-------|--------------------|-----------|------|
| `comfortable` | 44px | 15-16px | < 20 records, reading-oriented, touch use |
| `compact` | 36px | 14px | 20-100 records, mixed use (default) |
| `dense` | 28px | 13px + tabular lining figures | 100+ records, scanning and comparison |

```css
:root {
  /* compact — default */
  --row-height: 36px;
  --row-padding-x: 12px;
  --text-body: 0.875rem;
}

[data-density="comfortable"] { --row-height: 44px; --row-padding-x: 16px; --text-body: 0.9375rem; }
[data-density="dense"]       { --row-height: 28px; --row-padding-x: 8px;  --text-body: 0.8125rem; }
```

Density is a **token level**, not a per-component decision. If the user gets to choose it, the `data-density` attribute changes on the root surface and components read their measurements from tokens. If adding a density level means touching components, the token layer has leaked.

## Choosing the level

Three questions:

1. **How many records will be shown?** Typical case and worst case.
2. **Is the user scanning or reading?** Scanning (finding one value, comparing rows) raises density; reading lowers it.
3. **Which screen and input?** Touch or field use requires at least `comfortable` — touch targets ≥ 44px.

If the answers are unknown, **ask.** Falling back to a default is the thing this skill exists to prevent.

When the answers conflict (500 records, but touch use in the field), name the conflict for the user and pick a side: touch target size is an accessibility constraint, density is a preference — the constraint wins.

## Core principle: density is not compression

As row height goes down, these must go **up**:

- **Alignment discipline** — at `dense`, column alignment is the only thing keeping the eye from slipping between rows
- **Separator clarity** — as height shrinks, the cue dividing rows must get stronger
- **Number legibility** — tabular lining figures are mandatory at `dense`, not optional

Cutting padding and shrinking type is not density, it is illegibility (`typography.md`, rule 8).

## Three directions

| Direction | When | Typography | Colour | Composition |
|-----------|------|------------|--------|-------------|
| **Swiss / International** (default) | Operational screens: tables, filters, forms | One grotesque family, hierarchy by weight | Neutral + one functional accent + semantic status colours | Strict column grid, left-aligned |
| **Editorial-dense** | Reports, analysis, screens carrying a narrative | Serif headings + grotesque body and data | Paper surface, dark ink, one accent | Asymmetric: narrative column plus data block |
| **Bento** | Metric summaries, dashboards | Compact, number-led, tabular figures | Neutral surface + semantic threshold colours | **Unequal** cells (2x1, 1x2, 2x2) |

**Restraint is the default posture** and Swiss is its usual expression. Something more expressive is legitimate, but argue it against the three questions in `design-quality.md`.

Get the direction **approved**; it is expensive to reverse. Dark theme is not a default — it is whatever the product wants.

One direction per screen. A Swiss table with a bento summary above it is not two directions but two components inside one: shared tokens, shared typography, only composition differs.
