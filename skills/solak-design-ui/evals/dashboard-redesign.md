# Dashboard redesign — a style word with no task behind it

Tests whether the skill refuses to start from an aesthetic and insists on a decision first. "Modern" carries no information about what anyone needs to do.

## Prompt

```text
Create a modern dashboard for energy operations.
```

## Scope

`screen-redesign`, from scratch. The full workflow applies, including the surface contract.

## Expected

- [ ] Classifies as a redesign and runs the workflow
- [ ] Treats "modern" as not a direction, and converts it into something concrete
- [ ] Asks its questions **once**, grouped, and only the ones that change the design — who watches this, what decision they make, what a wrong call costs, how fresh the data is
- [ ] Names one primary decision the dashboard exists to support, in one sentence
- [ ] Gives every tile a question it answers; a tile without a question is removed
- [ ] Lets importance drive size and position — the primary decision is not one tile among nine equals
- [ ] Shows freshness: last-updated time, and whether the data is live, delayed or cached
- [ ] Missing data appears as missing, with a reason, and is excluded from totals
- [ ] Status uses a second cue beyond colour
- [ ] States the reading order when the layout stacks, and derives the stacking width from a measurement
- [ ] Produces a surface contract, a wireframe, a state inventory and an ordered TODO before any styling

## Forbidden

- [ ] A wall of equally sized cards
- [ ] Choosing a visual style before the primary decision exists
- [ ] Colour as the only carrier of good/bad
- [ ] A large number with no comparison, unit, or period — a figure nobody can act on
- [ ] Missing values shown as `0`
- [ ] Assuming dark theme because "modern"
- [ ] Sparklines or charts that replace the number instead of accompanying it
- [ ] Nine tiles because a 3×3 grid looks tidy

## Notes for the reviewer

The failure mode here is a competent-looking dashboard that answers no question. It is easy to produce nine plausible energy metrics and lay them out well; the test is whether the output can state, in one sentence, the decision a person makes on this screen — and whether the layout visibly serves that decision over the other eight tiles.

Asking clarifying questions is correct here and is **not** a scope failure, provided they arrive in one message and each one changes the design.

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
