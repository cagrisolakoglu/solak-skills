# Arbitrary breakpoints

Canonical reference: `responsive-grid.md`.

## Bad implementation

Breakpoints copied from a device list, applied to the viewport, and made to fit by shrinking type.

```css
@media (max-width: 1024px) { .layout { grid-template-columns: 1fr 1fr; } }
@media (max-width: 768px)  { .layout { grid-template-columns: 1fr; }
                             body    { font-size: 13px; }
                             .toolbar .primary { display: none; } }
@media (max-width: 480px)  { body    { font-size: 12px; }
                             .summary { display: none; } }
```

```css
/* Inside a 380px drawer, on a 1440px viewport. */
.drawer .fields { display: grid; grid-template-columns: 1fr 1fr; }
@media (max-width: 768px) { .drawer .fields { grid-template-columns: 1fr; } }
```

## Why it fails

- **768 and 1024 describe devices from a decade ago, not this layout.** The layout breaks where its content stops fitting, which is a property of the content. The two numbers coincide only by accident, and the gap between the real failure point and the declared breakpoint is a band of widths where the page is broken and nothing fires.
- **Shrinking text to fit is taking the cost out of the user.** It also compounds: 13px then 12px, and the numbers the screen exists to communicate fall below the readable floor.
- **Hiding the primary action to gain width** removes the reason the screen exists. Narrow does not mean "wants to do less".
- **Viewport queries cannot describe a drawer.** The drawer is 380px wide at every viewport, so `max-width: 768px` never fires and it renders two columns in 380px forever. The same failure appears in dialogs, side panels, split views, and any layout with a collapsible rail — at a 1024px viewport, the main region is 756px with the rail open and 988px without, and a viewport query sees one number for both.
- **`overflow: hidden` on an ancestor** — usually added to clip a rounded corner — deletes the child's overflow strategy silently. Valid CSS, no scrollbar, no console output, and content that simply does not exist for the user.
- **Nothing was measured**, so nobody can say whether the design works at 600px or 900px. Those are ordinary window sizes and they are usually where it fails.

## Correct direction

Derive the breakpoint from an observed failure:

1. Give each region a **minimum usable width** — the width below which its job stops working.
2. Build the wide composition.
3. Reduce width until something fails. Record the failure and the number.
4. Put the breakpoint at the failure. Name it for the behaviour it triggers.

```css
/* Measured: below 52rem the 2×2 tile falls to ~170px and context wraps to three lines. */
@container main (width < 52rem) { .bento { grid-template-columns: repeat(2, minmax(0, 1fr)); } }

/* Measured: below 30rem the metric and its unit land on separate lines. */
@container main (width < 30rem) { .bento { grid-template-columns: 1fr; } }

/* The page shell — genuinely a viewport concern. */
@media (width < 44rem) { .shell { grid-template-columns: 1fr; } }
```

Container queries for anything that can be constrained by a sibling; viewport queries for the page shell only. Type sizes do not change at breakpoints; if it does not fit at the readable size, the **composition** changes.

Test 320 · 375 · 600 · 768 · 1024 · 1440, plus 200% zoom, plus a half-width window — the split-screen case that device-name breakpoints always miss.

## Detection checklist

- [ ] For each breakpoint, can you state the layout failure that produced it?
- [ ] Is any breakpoint named for a device rather than a behaviour?
- [ ] Does font size change inside any media query?
- [ ] Is any P0 region or primary action hidden to gain width?
- [ ] Does any component that can sit inside a drawer, dialog or panel use a viewport query?
- [ ] Does the page scroll horizontally at 320px?
- [ ] Is `overflow: hidden` present on an ancestor of a scrollable region — and for what reason?
- [ ] Does every region declare an overflow strategy, and does a scroll region have a cue and keyboard access?
- [ ] Was the layout checked at 600px and 900px, or only at the declared breakpoints?
