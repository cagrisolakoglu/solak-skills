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

## Result — 2026-08-02, v1.7.0, clean context

Built from nothing: no file, no framework, no approved layout.

- **Scope classification:** screen redesign, full workflow. Ruled out the other three classes explicitly.
- **Routing:** the dashboard row plus the full-redesign row, then `typography.md`, `tokens.md` and `density-and-direction.md` as Stage 7 calls for them, and `tables.md` because the surface genuinely spans a metric block **and** a dense grid. Skipped `filters.md`, `forms.md`, `grid.md`.
- **References loaded:** 13 of 14 — the widest of the five runs, but a from-scratch redesign is the one scope where that is the prescribed set.
- **Expected behaviours met:** all eleven. Treated "modern" as not a direction and chose Swiss/International restraint with a stated reason; asked its seven questions in one grouped table with an assumption for each; named one primary decision in one sentence — *"decide which generating assets need action now to keep the portfolio on its committed dispatch schedule"*.
- **Forbidden behaviours observed:** none. Verified independently: no page overflow and zero console or page errors at eight widths from 320 to 1920; deviation cells **and** their header both `right` with `lining-nums tabular-nums`, all sharing one edge at x=999; six `—` cells for absent telemetry with the totals scoped *"14 of 16 assets reporting"*; one `aria-live` region; five tiles, not nine; a `Telemetry feeds` tile answering "can I trust the numbers above"; the context line stating the price is *delayed 5 min* rather than calling it live.
- **Blocking failures:** none.
- **Result: PASS**
- **Notes:** Eleven defects were found by its own measurement and screenshot passes during the build and fixed before reporting, including a metric grid querying itself (stuck at four columns at every width), an `auto` track letting tile content escape onto the next tile (sideways scroll at 6 of 13 widths), an unsized `<svg>` rendering as a 200px black triangle, and `hidden` losing to `display: flex` so the selection bar announced a row count during loading. That last one is the third independent appearance of the `hidden`-vs-`display` collision across these runs.

  **This run produced a new rule.** It reported that `document.fonts.check()` returned `true` while canvas metrics proved Inter was not loaded. Verified here directly: `document.fonts.check('16px Inter')` is `true`, `document.fonts.check('16px "Totally Not A Real Font"')` is **also** `true`, `[...document.fonts].length` is `0`, and both families measure an identical 31.1015625px. The obvious programmatic verification of the font-delivery gate does not verify anything. Encoded in `typography.md` §3 with the width-comparison test that does work.

  Declared honestly rather than faked: conflict handling out of scope (single writer, no server), offline not implemented, retry buttons report failure instead of pretending a source recovered, and Inter self-hosting impossible in an offline single file — so the fallback is measured and reported rather than claimed.
