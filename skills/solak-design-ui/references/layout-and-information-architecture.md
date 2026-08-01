# Layout and Information Architecture

Stage 4 of `ux-workflow.md`. The user's task, content inventory and flow are already decided; this file turns them into a screen skeleton.

**No visual design here.** No palette, no card treatment, no shadows, no icons. The output is regions, order and behaviour — the things that are expensive to change later.

## Choosing the layout

| Need | Suitable layout |
|------|-----------------|
| Scan and compare many records | Table + persistent context + visible filter summary |
| Edit one record in detail | Grouped form + sticky save state |
| Decide from a summary | Prioritised KPI area + supporting data surface |
| Inspect details from a list | Master-detail: side panel or split view |
| Rare advanced query | Collapsible panel or drawer |
| Multi-step, expensive to reverse | Explicit steps + summary + confirmation |

Read the row that matches the primary task from Stage 1. If two rows match, the screen has two primary tasks and the scope needs splitting.

## Page regions

Name every region and what it is for. A region without a stated purpose is decoration with a border.

Typical operational screen, top to bottom:

1. **Identity and context** — where am I, what period/scope am I looking at, when was this last updated
2. **Query** — search, frequent filters, entry to advanced filters
3. **Query result state** — applied filters, result count, system status
4. **Decision surface** — the one thing the screen exists for: table, form, tile grid
5. **Selection and bulk** — what is selected, what can be done with it, pagination

Not every screen has all five. Every screen has region 4.

### Layout decision record

```md
| Region | Purpose | Priority | Position | Narrow-screen behaviour |
|--------|---------|----------|----------|-------------------------|
| ... | ... | P0/P1/P2 | ... | ... |
```

## Reading order

Order regions by the user's **task sequence**, not by visual convention. The user reads context → narrows → scans → acts; a layout that puts bulk actions above the result contradicts the order the task actually runs in.

Two rules that catch most mistakes:

- **Position carries priority before size or colour does.** Moving the decision indicator up the page is stronger than making it bigger, and it costs no visual weight.
- **DOM order is the mobile reading order.** If a region is visually repositioned with `order` or `grid-area`, check what a screen reader and a narrow viewport actually produce. Visual order and DOM order disagreeing is a bug that only appears at 320px and with a keyboard.

## Primary and secondary zones

- The primary action goes where the eye already is at the moment the user is ready to act — usually the end of the decision surface, not the top of the page
- The most frequent control stays visible without interaction
- Rare controls go behind one disclosure step; they do not get their own permanent region
- **Destructive actions live away from the primary action**, with confirmation
- Do not put unrelated controls on the same row merely to fill space (`grid.md`: a row is a semantic unit)

## Progressive disclosure

Three levels, and each needs a reason to exist:

| Level | Holds | Cost to reach |
|-------|-------|---------------|
| Always visible | P0: identity, decision, status, primary action | none |
| One step away | P1: supporting detail, advanced filters, row detail | one click / expand |
| Deep | P2: technical identifiers, audit metadata, history | detail surface |

Moving an item down a level is only legitimate when the task can still be completed. Hiding a P0 item to make a screen look calmer is information loss disguised as minimalism.

## Master-detail

| Pattern | Use when | Cost |
|---------|----------|------|
| Separate page | Detail is large; the user works in it for a while | Loses list context; back-navigation must restore filters and scroll |
| Side panel | Detail is scanned, list context matters | Narrows the list; needs a narrow-screen fallback |
| Inline expansion | Detail is small and compared across rows | Breaks row rhythm; only at low row counts |
| Modal | Genuinely blocking, single-decision | Blocks everything; **not the default** |

The default choice for "inspect a record from a list" is a **side panel**, because it preserves the applied filters and the scan position — the two things the user paid for.

A modal is correct only when the rest of the screen must not be interacted with. "It was easier to build" is not that reason.

## Sticky context

Something must remain visible when the user scrolls into the data:

- The **identity** of what they are looking at (which period, which filter set)
- Table **column headers** beyond ~15 rows (`tables.md`)
- The **identity column** under horizontal scroll
- The **save state** in a long form

Everything else may scroll away. Sticky is expensive: it costs permanent vertical space, so each sticky element must earn it.

Check the opposite too: **does critical context disappear during scroll?** A result count that scrolls away leaves the user unsure whether they are looking at 12 records or 1,200.

## Responsive reordering

Decide the narrow-screen order at wireframe time, not at CSS time.

- Region order at 320px follows importance, and must not contradict DOM order
- A region that becomes useless when narrow is removed there, not shrunk
- The narrowing strategy for the data surface is chosen and **measured**, not declared: see the 40% identity-block threshold in `tables.md`
- Filters collapse to a summary line when the chip stack would consume the viewport (`filters.md`)

## Where states live

Empty, loading, error and partial states are **regions**, not afterthoughts. Reserve their space in the wireframe:

| State | Where it appears | What it must not do |
|-------|------------------|---------------------|
| Loading | In the decision surface, at real content height | Collapse the layout, shift it when data arrives |
| First use | Replaces the decision surface | Look identical to no-results |
| No results (filtered) | Replaces the decision surface, keeps the query region | Leave the user without an exit |
| Partial | Alongside the data | Present incomplete data as complete |
| Error | Inside the affected region | Empty the whole screen for one failed region |
| Stale | Announced above the data, data still visible | Reduce the contrast of readable values |

If the wireframe has no place for these, the layout is not finished.

## ASCII wireframe template

Produce one of these before any code. It takes two minutes and settles most arguments.

```text
┌─────────────────────────────────────────────────────────────────┐
│ Page title                    Last updated          Primary CTA │
│ Short context / task description                                │
├─────────────────────────────────────────────────────────────────┤
│ Search               Quick filters                 Filters [3]  │
│ Applied filters / result count                                  │
├─────────────────────────────────────────────────────────────────┤
│ Decision indicator (one line — not a row of tiles)              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Main data surface: table / form / dashboard                     │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│ Selection summary / bulk actions / pagination                   │
└─────────────────────────────────────────────────────────────────┘

Narrow (320):
  title → applied-filter summary → [show filters] → data surface (folded)
  bulk actions move below the data
```

## Layout principles

- Arrange content by the user's task sequence
- Prioritise by **position** first, then size, then colour
- Keep controls that work together adjacent
- Do not fill a row with unrelated controls
- **Do not turn every region into a card.** A boundary is drawn only where there is a real grouping or interaction boundary (`design-quality.md`)
- Do not shrink the main data area to make room for decorative summaries
- Use the available space on operational screens — dead space on a wide screen is a grid problem with two legitimate fixes (`grid.md`)
- Mobile visual order must not contradict DOM order
- A modal is not the default solution

## Verification

- [ ] Every region named, with a stated purpose
- [ ] Reading order follows the task sequence
- [ ] Primary action placed; destructive action separated
- [ ] Main data surface chosen from the decision table, matching the primary task
- [ ] Progressive disclosure levels assigned; no P0 item hidden
- [ ] Master-detail pattern chosen with its cost accepted
- [ ] Sticky elements justified; no critical context lost on scroll
- [ ] Narrow-screen region order defined and consistent with DOM order
- [ ] Space reserved for loading, first-use, no-results, partial and error
- [ ] ASCII wireframe or semantic outline produced
