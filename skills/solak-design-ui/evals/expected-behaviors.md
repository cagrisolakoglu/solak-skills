# Shared expected behaviours

Every evaluation is judged against this list in addition to its own. Each line is one observable behaviour, not a quality adjective — "the output is good" is not checkable, "the total excludes the seven unavailable records" is.

## Process

- [ ] Classifies the scope explicitly, and the classification matches the work the request actually needs
- [ ] A micro fix stays a micro fix: no wireframe, no product-strategy questions, no stage list
- [ ] A redesign states the primary task in one sentence before anything visual
- [ ] Information priority is decided before styling, not justified after it
- [ ] Reads a small reference set and it matches the routing table
- [ ] Does not ask for approval on decisions that have an obvious default
- [ ] Asks its questions once, in one message, and only when the answer changes the work

## Data

- [ ] Missing data is distinguishable from zero and excluded from totals
- [ ] Measured numbers are right-aligned with `tabular-nums lining-nums`, headers on the same axis
- [ ] Monospace only on technical identifiers, never on metrics
- [ ] Decimal places are constant down a column; unit casing is preserved

## System

- [ ] Uses the existing token layer; does not stand up a second one
- [ ] No hardcoded palette, spacing or type value inside a component
- [ ] Does not add a grid or UI library unless asked
- [ ] Does not overwrite an existing style file without reading it

## States

- [ ] Refresh keeps usable data on screen — not emptied, not dimmed
- [ ] First-use empty and filtered no-results are separate components
- [ ] Errors say what failed and what to do; retry names what it retries
- [ ] Every error path has a recovery action

## Responsive

- [ ] Breakpoints come from a recorded layout failure, not a device name
- [ ] No overflow at 320px, and the narrowing strategy is measured rather than declared
- [ ] Text is never shrunk below the minimums to make something fit

## Honesty

- [ ] Reports what was not verified instead of implying it was
- [ ] Does not claim a gate it did not check
- [ ] Names the risks it is leaving behind

## Verification

This file is checked by reading a transcript, not by running a script. If a line here cannot be judged from a transcript, it is written wrong and should be rewritten as something observable.
