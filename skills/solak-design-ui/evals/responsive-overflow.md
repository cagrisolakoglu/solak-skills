# Responsive overflow — measure, do not guess

Tests whether breakpoints are derived from an observed failure or copied from a device list.

## Prompt

```text
The page works on desktop but overflows on mobile.
```

## Scope

`component-refinement` at minimum — the defect is real and located, but "overflows" names a symptom, not a region. Finding which region overflows is part of the work, not a question for the user.

## Expected

- [ ] Reproduces the overflow and identifies the **actual** element, with a number: container width vs content width
- [ ] Checks whether an ancestor `overflow: hidden` is hiding the problem rather than solving it
- [ ] States a minimum usable width for the affected region
- [ ] Chooses one explicit strategy — wrap, stack, fold, scroll the region, move to detail, or declare a minimum — and says why the others were rejected
- [ ] Picks the breakpoint by reducing width until the layout fails, and names the breakpoint for the behaviour it triggers
- [ ] Uses a container query where the region's width depends on a sibling (navigation, drawer, panel) rather than on the viewport
- [ ] Verifies at 320px and at 200% zoom
- [ ] Confirms the page itself no longer scrolls sideways at any tested width

## Forbidden

- [ ] Adding 768px and 1024px breakpoints because they are the usual ones
- [ ] Shrinking font size to make content fit
- [ ] Hiding the primary action or a P0 region to gain width
- [ ] Reaching for `overflow-x: auto` on the page body as the whole fix
- [ ] Declaring the strategy without measuring it — "rows fold below 560px" with no evidence that 560 is where it breaks
- [ ] Adding a scroll region with no continuation cue and no keyboard access
- [ ] Reporting "fixed on mobile" without naming the widths tested

## Notes for the reviewer

Two failures look like success. The first is a scroll container that technically removes the overflow while leaving the content unreachable in practice — no cue, no focusability. The second is a viewport breakpoint on a component whose real constraint is the sidebar: it will pass at the tested viewport and fail the moment the sidebar collapses.

## Result — 2026-08-02, v1.7.0, clean context

Surface: a three-column settlement shell with a 1100px table inside a rounded `overflow: hidden` card, a fixed 380px drawer using viewport queries, device breakpoints at 1024/768/480, font shrunk to 13px then 12px, and the primary action plus the metric strip `display: none` below 480.

- **Scope classification:** component refinement. Argued explicitly: one defect class but four regions, and two fixes restore P0 content, which is past inspect-fix-verify.
- **Routing:** `responsive-grid.md` + the affected surface (`tables.md`), plus `ux-workflow.md` and the TODO template for the refinement path. Named the five it skipped and why.
- **References loaded:** 5 of 14.
- **Expected behaviours met:** all eight. It also **falsified the user's premise** — measured the page overflowing at every width including 1440, traced it to a `1fr` track with no `min-inline-size: 0` being widened by the table's `min-width`, and said so rather than fixing only the mobile case.
- **Forbidden behaviours observed:** none. Independently verified at ten widths from 320 to 1920: `scrollWidth == viewport` everywhere (was over at all of them), body `15px` at every width, nav / aside / metrics / **Approve run** all rendered at every width, drawer-vs-primary-action geometric overlap clean everywhere, numeric cells `right`, zero page errors.
- **Blocking failures:** none.
- **Result: PASS**
- **Notes:** Hit the `overflow: hidden` trap deliberately and named it — moved the radius clip to a new scroll container because clipping the corner would have deleted the table's scroll strategy the moment the grid fix landed. Rewrote all four breakpoints in `rem`, named for behaviour (`aside-stack` / `nav-rail` / `drawer-stack` / `row-fold`), each with its recorded failure in a comment, and put the drawer's internal grid on a **container** query because the drawer is 384px wide at 1440 and at 900 alike.

  Its own screenshots caught what its numeric assertions had reported green: the drawer covering the primary action at 1440. Worth recording — the measurement pass passed and the image did not.

  **Scope observation, not a failure:** it also introduced right-alignment and tabular figures on the money columns. The fixture had neither, so this is a genuine defect it fixed while restructuring the table region — but it was not the reported one. Disclosed, small, and adjacent to work it was already doing. Flagged as a candidate rule: during a refinement, an adjacent defect is reported unless the change already in hand touches it.

  Correctly reported unchecked rather than claimed: no loading / empty / error / stale states exist in the file, no dark theme, no drawer dismiss control, and formatting rules it was not routed to.
