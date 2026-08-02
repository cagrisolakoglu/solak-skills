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
