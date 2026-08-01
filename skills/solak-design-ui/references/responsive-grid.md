# Responsive Grid

> Read this at the **rough layout** stage of `ux-workflow.md`, right after the layout skeleton exists and before any styling. Regions and reading order come from `layout-and-information-architecture.md`; this file decides how that composition survives a change in available width.

Scope boundary with the other grid file: **`grid.md` is the column grid *inside* a surface** — spans, cell sizing, row semantics. **This file is the page composition** — how regions rearrange as space changes. They are read together on a multi-region screen.

> **Use fluid grids and content-driven thresholds. Device categories are planning labels, not breakpoint definitions.**

An enterprise screen has to work on large monitors, laptops, half-width split windows, tablets, phones, browser zoom, dialogs, drawers and embedded panels. A desktop split-screen window is often narrower than a tablet. Respond to width, not to device identity.

## Decision order

1. Identify the primary task and the page regions (Stages 1-5 of `ux-workflow.md`)
2. Assign each region a priority
3. Determine each region's **minimum usable width**
4. Build the wide composition
5. Reduce the width until the layout fails
6. Record the failure
7. Add the smallest transformation that fixes it
8. Repeat down to the minimum supported width
9. Verify with real data, long labels, zoom and every state

Do not start by picking `768px`, `1024px`, `1440px`. Ask: **at what width does *this* layout stop being usable?**

## Viewport queries vs container queries

| Query | Governs |
|-------|---------|
| **Viewport** (`@media`) | The page shell: application navigation, persistent sidebars, overall composition, page gutters |
| **Container** (`@container`) | Reusable components: filter panels, forms, metric groups, toolbars, cards, dialogs, drawers |

```css
.data-surface { container-type: inline-size; container-name: surface; }
@container surface (width < 48rem) { .data-surface__toolbar { grid-template-columns: 1fr; } }
```

The same component can be full width on one page and squeezed into a 24rem side panel on another. **Viewport width cannot describe both**, and a component that only listens to the viewport will render its wide layout inside a narrow drawer.

Note the unit: `rem`, not `px`. A `px` breakpoint ignores the user's text size; a `rem` breakpoint moves with it, which is what makes the 200% zoom case work without extra rules.

## Planning ranges

Names for the test matrix, not for the CSS:

| Category | Range | Typical context |
|----------|------:|-----------------|
| Small mobile | 320-374 | narrow portrait phones |
| Mobile | 375-599 | standard phones |
| Compact | 600-899 | portrait tablets, split windows |
| Medium | 900-1279 | small laptops, landscape tablets |
| Desktop | 1280-1599 | normal workspaces |
| Large | 1600+ | wide operational screens |

## The 12 / 8 / 4 planning model

A planning system, not a requirement to render twelve DOM columns.

```css
.page-grid {
  --grid-columns: 12;
  display: grid;
  grid-template-columns: repeat(var(--grid-columns), minmax(0, 1fr));
  gap: var(--grid-gap);
  padding-inline: var(--page-gutter);
}
@media (width < 80rem) { .page-grid { --grid-columns: 8; } }
@media (width < 48rem) { .page-grid { --grid-columns: 4; } }
```

Column count lives in a custom property so narrowing is one declaration, not a rewrite. Move the thresholds when the real layout fails earlier or later — the numbers above are a starting point, not a contract.

Span remapping is the trap that comes with this, and it is silent: see `grid.md`.

## Content width mode follows the task

| Mode | For | Rule |
|------|-----|------|
| **Bounded** | Forms, settings, detail pages, reports, documentation | `inline-size: min(100%, var(--layout-content-max))`, centred |
| **Workspace** | Data grids, monitoring, scheduling, side-by-side comparison | `inline-size: 100%`, only page gutters |

Do not apply a narrow marketing-style maximum to an operational data grid, and do not stretch a form across 1920px. The width model is a task decision, and it is the first thing to get wrong on a wide screen.

**Extra width must buy efficiency, not scale.** More visible columns, side-by-side comparison, a persistent detail panel, a larger plotting area, fewer modal round trips. Using 1920px to enlarge cards and whitespace wastes the screen.

## Fluid spacing

```css
:root {
  --page-gutter:  clamp(1rem, 0.5rem + 2vw, 3rem);
  --grid-gap:     clamp(0.75rem, 0.5rem + 0.8vw, 1.5rem);
  --section-gap:  clamp(1.5rem, 1rem + 1.5vw, 3rem);
  --cluster-gap:  clamp(0.5rem, 0.35rem + 0.5vw, 1rem);
}
```

Every fluid value needs a real floor and ceiling. Keep at least a **16px page gutter** on narrow screens unless a surface is deliberately full bleed — an edge-to-edge table on a phone reads as broken, not dense.

### Where `clamp()` belongs, and where it does not

| Use it for | Never for |
|------------|-----------|
| Page gutters, section gaps | Table body text (`typography.md`) |
| Page titles, primary metric sizes | Form control heights, touch targets |
| Large workspace padding | Sticky offsets, aligned column widths, technical identifiers |

A sticky offset that clamps stops matching the column it is offsetting from, and the sticky block leaks (`tables.md`).

## Safe tracks

```css
/* ❌ long content forces the track wider than the container */
grid-template-columns: 2fr 1fr;

/* ✅ */
grid-template-columns: minmax(0, 2fr) minmax(18rem, 1fr);
.grid-child { min-inline-size: 0; }
```

For groups that should reflow on their own:

```css
.auto-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 16rem), 1fr));
  gap: var(--grid-gap);
}
```

`min(100%, 16rem)` matters: a bare `minmax(16rem, 1fr)` overflows any container narrower than 16rem — which is exactly what a drawer is.

## Region priority and minimum usable width

Every region carries a priority (from `layout-and-information-architecture.md`) **and a measured minimum width**. The minimum is what turns "it looks cramped" into a decision.

| Priority | Meaning | Narrow behaviour |
|----------|---------|------------------|
| P0 | Required for the primary task | Always visible |
| P1 | Strongly supports it | May move or collapse |
| P2 | Useful detail | May fold or go behind disclosure |
| P3 | Rare or administrative | May move to a menu or another surface |

**Never hide P0 to preserve decoration.** If a P0 region cannot hold its minimum width, the composition changes — the region does not disappear.

## Transformation order

As width decreases, in this order:

1. Reduce decorative whitespace, within token bounds
2. Wrap toolbars and control groups
3. Change column spans
4. Stack side-by-side regions
5. Move P1 below P0
6. Collapse advanced controls
7. Fold P2 detail
8. Shorten labels without losing meaning
9. Hide only explicitly low-priority content
10. Horizontal scroll, and only where comparison requires it

**Shrinking typography is not on this list** (`typography.md`, rule 8).

## Breakpoint selection

The procedure, and it is mechanical:

1. Start at the widest supported width
2. Reduce slowly
3. Stop at the first meaningful failure
4. Record it
5. Define the smallest transformation that resolves it
6. Put the breakpoint at or just before the failure
7. Continue down to the minimum supported width

Meaningful failures: overlapping controls · label wrapping that destroys meaning · the primary action pushed out of view · a side region below its minimum · a table losing comparison context · form fields losing meaningful widths · a toolbar forming unstable multi-row layouts · a sticky region eating most of the screen.

Do not add a breakpoint because a framework ships one.

### Name breakpoints by behaviour

```text
✅ layout-single-column · sidebar-stack · toolbar-wrap · filter-drawer
   table-fold · navigation-compact
❌ iphone · ipad · desktop · desktop-xl
```

The name should say **why the breakpoint exists**. `$bp-sidebar-stack: 64rem` survives a redesign; `$bp-ipad` becomes a lie the first time a split window hits that width.

## Overflow is declared, never defaulted

Every region declares one strategy: wrap · truncate with full-value access · horizontal scroll · vertical scroll · fold · move to detail · declare a supported minimum width.

A horizontal scroll region must have a visible boundary, a continuation cue, keyboard access, no focus trap, and readable sticky content (`tables.md`).

### `overflow: hidden` for a rounded corner cancels the strategy underneath it

Wrapping a table in a bordered, rounded card and adding `overflow: hidden` so the corner clips cleanly is the standard move. It also **deletes the child's overflow strategy**, and it does so silently: valid CSS, no console output, no scrollbar, no visual seam. Measured on a real component bench — the container was 286px wide, the table 780px, and 494px of columns simply did not exist for the user.

```css
/* ❌ the corner clips; so does the data */
.panel { border: 1px solid var(--warn); border-radius: var(--radius); overflow: hidden; }
.panel table { min-inline-size: 26rem; }

/* ✅ the radius moves to the scroll container, which is the element that clips anyway */
.panel        { border: 1px solid var(--warn); border-radius: var(--radius); }
.panel__scroll { overflow-x: auto; border-end-start-radius: var(--radius); border-end-end-radius: var(--radius); }
```

Whenever `overflow: hidden` appears on an ancestor, name the reason. If the reason is a corner, a shadow or a pseudo-element, the fix is to move the clip to the element that already scrolls. **A parent may not silently override a child's declared overflow strategy.** The check is one line at each supported width:

```js
el.scrollWidth > el.clientWidth && getComputedStyle(el).overflowX === 'hidden'   // → unreachable content
```

## Navigation, drawers and dialogs

The content grid responds to the width left **after** application navigation, not to the viewport. A 1280px viewport with a 280px sidebar is a 1000px content area, and the content must be told so — which is what container queries are for.

- Desktop: persistent sidebar, but only while the main content stays above its minimum
- Compact: collapsible or icon-rail navigation
- Mobile: overlay or a dedicated route; no permanent sidebar eating the viewport; focus returns to the trigger on close

Dialogs and drawers use container queries internally. **Do not put a desktop side-by-side layout inside a narrow drawer.** A sticky dialog action bar must not cover content or the software keyboard.

## Zoom and text scaling

Test 100 / 125 / 150 / 200%. At higher zoom sidebars stack, controls wrap, compact layouts activate, sticky headers take more height — **all of that is correct**. Do not disable zoom and do not force the desktop composition to survive it. `rem`-based breakpoints make most of this work without extra rules.

## Named areas and subgrid

```css
.page-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(var(--layout-sidebar-min), var(--layout-sidebar-max));
  grid-template-areas: "header header" "main aside";
  gap: var(--section-gap);
}
@media (width < 64rem) {
  .page-layout { grid-template-columns: 1fr; grid-template-areas: "header" "main" "aside"; }
}
```

Names describe **semantic regions**, and DOM order stays logical: visual reordering that contradicts focus order is a bug that only appears with a keyboard.

`subgrid` is the right tool when nested content must align to the parent's tracks — aligned form groups, repeated label/value rows, dashboard sections sharing column lines. Where support is missing, share track definitions through custom properties. Do not add a layout library to reproduce CSS Grid.

## Responsive tokens

```css
:root {
  --layout-columns-wide: 12;
  --layout-columns-medium: 8;
  --layout-columns-narrow: 4;
  --layout-content-max: 90rem;
  --layout-reading-max: 70ch;
  --layout-sidebar-min: 18rem;
  --layout-sidebar-max: 24rem;
}
```

Semantic names only. `--ipad-width` and `--desktop-xl-gap` encode a device guess into the token layer, and the guess ages badly.

## Surface notes

Each surface reference owns its own detail; these are the responsive hooks.

**Data grid** (`tables.md`) — classify every column and give it a minimum width, a priority and a narrow behaviour:

```md
| Column | Type | Min width | Priority | Narrow behaviour |
|--------|------|----------:|----------|------------------|
| Account | identity | 160px | P0 | sticky, or folded title |
| Usage | decision | 112px | P0 | visible |
| Account ID | technical | 140px | P2 | detail panel |
| Actions | action | 64px | P1 | overflow menu |
```

Then pick **one** primary narrowing strategy: horizontal scroll · priority hiding · row folding · card transformation · a separate compact summary. The measured threshold that forces folding (sticky identity block over ~40% of visible width) is in `tables.md`.

**Filters** (`filters.md`) — keep search visible, keep the applied-filter summary visible, move advanced criteria to a drawer. The chip-wall collapse threshold (~25% of viewport height) is in `filters.md`. Never hide applied-filter state inside a closed drawer.

**Forms** (`forms.md`) — two columns only for logically related short fields; collapse to one usable column via a container query, not a viewport query, because a form often lives in a panel.

**Dashboards** (`dashboards.md`) — `auto-fit` with `minmax(min(100%, 15rem), 1fr)`; primary metric spans 2×2 wide, full or half width on tablet, single column on mobile with **importance order preserved and no fixed row heights**.

## Performance

One semantic DOM with adaptive composition. Avoid duplicate desktop/mobile component trees, heavy charts kept mounted but hidden, layout libraries for plain Grid, continuous resize handlers, and JavaScript measurement where a CSS query suffices. Use JavaScript only when the layout depends on data or geometry CSS cannot express.

## Output

### Region inventory

```md
| Region | Priority | Min usable width | Wide | Narrow |
|--------|----------|-----------------:|------|--------|
| ... | P0/P1/P2/P3 | ... | ... | ... |
```

### Failure record

```md
| Width | Failure | Resolution |
|------:|---------|------------|
| 1040px | side panel takes the main table below its minimum | stack the panel below |
| 720px | toolbar wraps to three rows | advanced filters to a drawer |
| 520px | sticky identity block uses 46% of the width | fold rows |
| 360px | action group overlaps the title | stack actions full width |
```

### Breakpoint record

```text
Breakpoint: 64rem  (sidebar-stack)
Reason:     the filter aside takes the primary table below its minimum usable width
Change:     stack the filter panel below the result summary
```

## Verification matrix

| Width | Purpose |
|------:|---------|
| 320 | minimum narrow phone |
| 360 / 390 / 430 | common phones |
| 600 | compact tablet or narrow window |
| 768 / 834 | portrait tablet |
| 1024 | landscape tablet, small workspace |
| 1280 / 1366 / 1440 | laptop and standard desktop |
| 1600 / 1920 | large desktop |

Also: a 50% split-screen window · 125/150/200% zoom · long localised labels · large numeric values · loading, empty, error, partial and stale states · open drawers and dialogs · the software keyboard where relevant.

Three widths are not a responsive test. Three widths are three screenshots.

## Blocking gates

- [ ] The primary task is available at **every** supported width
- [ ] Breakpoints are justified by recorded failure points, not device names
- [ ] No required region overlaps or clips; P0 regions stay visible
- [ ] Narrow-screen gutter ≥ 16px unless deliberately full bleed
- [ ] DOM order matches reading and focus order
- [ ] Container queries used for reusable components that can be constrained
- [ ] The data-grid narrowing strategy is explicit and measured
- [ ] Forms collapse to one usable column
- [ ] Primary actions stay reachable; touch targets ≥ 44px in touch contexts
- [ ] Horizontal scroll regions are keyboard accessible
- [ ] Works at 320px, or a higher minimum is **declared**
- [ ] Works at 200% zoom
- [ ] Long localised labels and large numbers do not overflow decision regions
- [ ] Loading, empty, error, partial and stale states use the same responsive structure
- [ ] Extra width buys efficiency, not scale

## Anti-patterns

Design only at 1440 · device names as breakpoint logic · assume desktop means mouse and mobile means touch · shrink type to save the desktop composition · hide the primary action when narrow · make all dashboard tiles equal · turn every row into a decorative card · viewport queries for reusable components · flexible tracks without overflow control · omit `min-inline-size: 0` · visual order fighting DOM order · duplicate desktop and mobile markup · applied filters hidden in a closed drawer · sticky regions eating a mobile viewport · zero gutters on mobile · narrow content bounds on an operational workspace · form fields stretched across a large display · a breakpoint added to fix one spacing glitch · resize listeners where CSS suffices · overflow left to the browser.

## Baseline

```css
:root {
  --layout-content-max: 90rem;
  --layout-sidebar-min: 18rem;
  --layout-sidebar-max: 24rem;
  --page-gutter: clamp(1rem, 0.5rem + 2vw, 3rem);
  --grid-gap:    clamp(0.75rem, 0.5rem + 0.8vw, 1.5rem);
  --section-gap: clamp(1.5rem, 1rem + 1.5vw, 3rem);
}

.page-container { inline-size: min(100%, var(--layout-content-max)); margin-inline: auto; padding-inline: var(--page-gutter); }
.page-grid      { display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); gap: var(--grid-gap); }
.page-grid > *  { min-inline-size: 0; }
.content-with-aside {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(var(--layout-sidebar-min), var(--layout-sidebar-max));
  gap: var(--section-gap);
}
.responsive-component { container-type: inline-size; }
.auto-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 16rem), 1fr)); gap: var(--grid-gap); }

@media (width < 80rem) { .page-grid { grid-template-columns: repeat(8, minmax(0, 1fr)); } }
@media (width < 64rem) { .content-with-aside { grid-template-columns: 1fr; } }
@media (width < 48rem) { .page-grid { grid-template-columns: repeat(4, minmax(0, 1fr)); } }
@container (width < 42rem) { .component-toolbar { grid-template-columns: 1fr; } }
```

A baseline, not a breakpoint contract.

---

> A responsive grid is not three screenshots. It is a set of rules describing how information changes as available space changes. The goal is not the same layout at every size — it is the same **task, hierarchy and decision quality** at every supported width.
