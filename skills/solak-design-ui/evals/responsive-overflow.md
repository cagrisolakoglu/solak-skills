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

## Result

**NOT RUN.** Written 2026-08-02 alongside v1.7.0; no clean-context execution yet.

A run performed in the session that authored the expectations is not evidence — the routing decision would be recalled rather than reached. This one needs a fresh session with the skill installed and no prior conversation about the surface.

- Scope classification:
- Routing:
- References loaded:
- Expected behaviours met:
- Forbidden behaviours observed:
- Blocking failures:
- Result: PASS / PARTIAL / FAIL / NOT RUN
- Notes:
