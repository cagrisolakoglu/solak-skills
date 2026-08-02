# Table redesign — "minimal" as a trap word

Tests whether the skill converts an aesthetic word into an information-priority decision, or takes it literally and removes things the user needs.

## Prompt

```text
This table has 400 rows and is too busy. Make it more minimal.
```

## Scope

`component-refinement` — the surface is named, the complaint is structural, and nothing suggests the page around it changes. If the information priority turns out to be wrong at page level, saying so and widening scope deliberately is correct; widening it silently is not.

## Expected

- [ ] Classifies as a refinement and says why it is not a micro fix
- [ ] Names the local task — scanning and comparing 400 rows to find the ones that need action
- [ ] Converts "minimal" into something concrete and gets it confirmed, or states the interpretation it is proceeding under
- [ ] Produces an information priority (identity / decision / detail / rare) **before** any visual change
- [ ] Keeps the decision columns and demotes detail — reduction by priority, not by column count
- [ ] Justifies the density level in one sentence tied to 400 rows and a scanning task
- [ ] Measured values right-aligned, tabular lining figures, constant precision
- [ ] One separator system, not zebra plus rules plus borders
- [ ] States a narrowing strategy derived from a measurement
- [ ] Lists the states: loading, first use, filtered no-results, partial, error
- [ ] Produces a dependency-ordered TODO and executes it item by item

## Forbidden

- [ ] Folding rows to cards on desktop as the default answer to "busy"
- [ ] Introducing a grid or table library
- [ ] Monospace on measured values
- [ ] Any functional text below 12px, or dense body text below 13px, to buy space
- [ ] Missing values rendered as `0`
- [ ] Removing a column because it is visually noisy without checking whether a decision depends on it
- [ ] Choosing a visual direction before the priority exists
- [ ] Reporting "minimal" as achieved with no statement of what was removed and why

## Notes for the reviewer

"Minimal" is the trap. The correct response treats it as *fewer competing signals*, not *fewer columns*: most of the busyness in a dense table comes from every cell being emphasised at once, so removing emphasis usually beats removing data.

Watch for the quiet failure where a decision column is demoted to a detail column and the table gets calmer at the cost of the user's actual job.

## Result — 2026-08-02, v1.7.0, clean context

Surface: 13 columns at 11px, five bold columns, Courier money left-aligned, decimals alternating between one and two places, unreadable meters rendered as `0` and `0.00`, zebra plus rules plus a card border plus a shadow plus a gradient, and actions revealed only on hover.

- **Scope classification:** component refinement, citing the triage table where this request appears verbatim. Left the page shell and pagination model alone.
- **Routing:** `tables.md` + `formatting.md` + `typography.md`, plus `density-and-direction.md` (which `tables.md` lists first in its Read with), `ux-workflow.md`, `design-quality.md` and `interaction-and-states.md`. Named the seven it skipped and why.
- **References loaded:** 9 of 14 — the widest read of the five runs, and the one place routing discipline was loosest. Defensible: `design-quality.md` is permitted for a broad refinement and it added seven states, so `interaction-and-states.md` was needed.
- **Expected behaviours met:** all eleven.
- **Forbidden behaviours observed:** none. Verified independently: every body cell 13px (**up** from 11px), weights a closed set of 400/600, the account ID the only monospace column, all 30 amount cells and their header sharing **one** right edge at x=976, decimal places a single value of 2, no page overflow at 320/375/600/768/1440, no hover-hidden controls remaining, 13 columns down to 9.
- **Blocking failures:** none.
- **Result: PASS**
- **Notes:** The most valuable behaviour was reading "minimal" as *fewer competing signals* rather than *fewer columns* — and **increasing** the type size while doing it. The original had already "simplified by shrinking", which is the anti-pattern; density came back through a 28px row instead.

  Missing-vs-zero was handled exactly right, and this is worth recording precisely because a crude text scan looks like a failure: the page still contains `0.00`. Those are **genuine zeros** — meters whose current reading equals the previous one, so usage really is zero. The four unreadable meters show `—` in Previous, Current, Usage and Amount, with status `✕ Unreadable` carrying a glyph and a word alongside the colour, and a partial line stating that four of thirty are excluded from any total. Zero as a measurement and zero as a stand-in for absence are correctly separated.

  Refused a total row, with the right reason: a total over 412 records cannot be computed from the 30 on the page, and totalling the visible page while calling it "the total" is the failure `tables.md` names.

  Four defects its own screenshots caught that the CSS had hidden: `display: flex` defeating the `hidden` attribute, the zebra rule out-specifying the anomaly fill so it never painted, skeleton bars invisible against zebra rows, and detail prose clipped by the row-truncation rule. Same lesson as the responsive run — the numeric pass was green and the image was not.
