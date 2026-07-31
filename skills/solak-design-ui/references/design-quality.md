# Design Quality

This skill **carries its own** quality criteria; it depends on no external rule file. The criteria below are written for working product screens, not marketing surfaces.

## The measure is decision speed, not pleasantness

A data-dense screen is judged by three questions:

1. How many **seconds** does it take to find the value being looked for?
2. Is there a **misreading** risk? (unaligned numbers, mixed units, missing data that looks like zero)
3. Does the screen say what the **next action** is?

"It looks nice" is not an answer. Aesthetics matter to the extent they serve those three — and they usually do: a screen with clear hierarchy, consistent rhythm and disciplined alignment is both faster to read and better looking.

## Restraint is the default

Restraint does **not** mean less data. It means fewer devices used to present the data. Four hundred rows stay four hundred rows; what goes down is the number of frames, shadows, colours, separators and boxes used to explain them.

Ten rules, in priority order:

1. **Hierarchy from type, space and ink — not from containers.** Before adding a box, try a size step, a weight step or more space. A screen where every group is a card is a screen with no hierarchy.
2. **One boundary per region.** No box inside a box. If a card already has a border, the table inside it does not need one too.
3. **One accent.** A second accent splits attention and no longer means anything. Status colours are semantic, separate from the accent, and never decorative.
4. **Elevation only where something actually floats.** Menus, popovers, dialogs. Static cards get a border, not a shadow. One elevation level is enough; a second needs a reason.
5. **One radius** (plus a smaller one for controls inside). Mixed radii read as unfinished.
6. **Alignment does the work decoration would.** A strict grid is the cheapest way to look designed (`grid.md`). Misalignment cannot be compensated for with colour.
7. **Space is graded, not uniform.** Generous between groups, tight inside rows. Uniform padding everywhere is the signature of a screen nobody laid out.
8. **Borders are quiet.** A separator's job is to be found when looked for, not to be seen constantly. If borders are the first thing visible, they are too strong.
9. **Ornament needs a reason.** Gradient, texture, pattern, icon — each must answer "what does this tell the user?" No answer means remove it.
10. **Motion only carries information.** State change, continuity, position. Decorative animation in an operational screen tires rather than delights.

**Greyscale test:** render the design without colour. If the hierarchy still reads, it was real. If everything flattens, hierarchy was being carried by colour — and colour is the one channel a portion of users, greyscale printouts and dim screens do not receive.

## Patterns to avoid

These are the repeatedly produced, recognisably unconsidered surfaces in this space:

- **Inventory dashboard** — twelve boxes of equal size. No hierarchy, no difference in importance; the user does not know where to start.
- **Flat table** — every column the same weight. Identity, decision and detail columns do not separate, so the eye re-finds the relevant column on every row.
- **Library default** — a Bootstrap/Quasar/shadcn/MUI component left untouched and never wired to the product's token layer. It reads as a demo, not a product.
- **Uniform spacing** — everything equally spaced. When field spacing equals group spacing, a form is a list and a dashboard is a pile.
- **One grey plus one blue** — neutral surface and a single accent with no semantic status colours. Approved, pending and disputed records all look the same.
- **Colour as the only indicator** — status conveyed by hue alone. Beyond colour blindness, it vanishes in greyscale output and on dim screens.
- **Half-built interaction** — hover exists, `focus-visible` does not; or an action that appears only on hover. Keyboard and touch users are left out.
- **Filler content** — a tile, repeated summary or "chart for the sake of a chart" added to close a gap.
- **Decorative depth** — gradients, big shadows, glass effects, while elevation communicates nothing. Depth without meaning is noise.
- **"Simplified" by shrinking** — font size reduced as the answer to clutter. The clutter became illegibility; what should have gone down is colour, separators and emphasis (`typography.md`, rule 8).
- **Thin weights** — body text at 300 or below. At 13px it turns grey on light backgrounds and blooms in dark theme. De-emphasise with ink, not weight.
- **Icon inflation** — decorative icons in headings while the data that needs an icon has none.

## Required qualities

Every meaningful surface must show at least **five**:

1. **Hierarchy through scale contrast** — the most important number is the largest; heading/body/micro are three clear steps
2. **Deliberate rhythm** — group spacing at least twice field spacing; no uniform padding
3. **Alignment discipline** — fields and columns start from shared grid lines (`grid.md`)
4. **Depth that means something** — sticky surface, sunken area, card boundary; each announces something
5. **Number typography** — tabular lining figures, alignment by type, constant precision down a column (`formatting.md`, `typography.md`)
6. **Semantic colour** — status colours separate from the functional accent, each paired with an icon or text
7. **Designed interaction** — hover, `focus-visible`, active, disabled/readonly, selected; all deliberate
8. **Compositional hierarchy** — span and tile size communicate importance; not a row of equal boxes
9. **States** — empty, first use, loading, partial, error, overflow. In this domain, quality is visible **in the states**
10. **Deliberate density** — the `comfortable`/`compact`/`dense` choice is justified (`density-and-direction.md`)

Item 9 is privileged here: a screen that looks good on the happy path but prints "No records" for empty has not been designed.

## Direction and theme

Direction selection (Swiss / editorial-dense / bento) lives in `density-and-direction.md` and is approved by the user.

- **"Clean minimal", "modern" and "nice" are not directions.** Convert them into concrete choices: type family, palette strategy, compositional decision.
- **Restraint is the default direction**, and Swiss/International is its usual expression. Anything more expressive must be justified against the three questions at the top.
- **Dark theme is not the default.** It is whatever the product wants. If both themes ship, both must look deliberate — dark is not the inverse of light (`tokens.md`).
- **One direction per screen.** A Swiss table with a bento summary above it is not two directions; it is two components inside one: shared tokens, shared typography, only composition differs.

## When a chart is needed

This skill builds charts with its own rules; no external skill is required:

- **Chart type follows the question** — change over time → line; category comparison → bar; part-to-whole → stacked bar (not pie; beyond 2-3 slices it stops being readable); distribution → histogram
- **Categorical palette: 5-6 series maximum.** More cannot be told apart; fold the tail into "other"
- **Series distinguished by colour *and* form** — line style, marker shape or direct labelling; colour cannot be the only indicator
- **If the Y axis does not start at zero, say so** — small variation otherwise looks dramatic
- **Unit on the axis label once**, never repeated on data points
- **Tooltips restate data, they do not introduce new data**; they must be keyboard reachable
- Chart colours derive from the semantic colours in `tokens.md`, so contrast and theme behaviour come for free

Deeper visualisation work (complex multi-series analysis, bespoke palette generation) can **optionally** be handed to a dedicated data-visualisation skill if one is available; this skill works fully without one.

## Checklist

- [ ] The surface looks like it belongs to a product, not like a library default
- [ ] Hierarchy built with type, space and ink before any box was added
- [ ] One boundary per region; no box inside a box
- [ ] One accent, one radius, at most one elevation level
- [ ] Group/field rhythm separates; no uniform spacing
- [ ] Status colours are semantic and paired with an icon or text
- [ ] Every interaction state designed, `focus-visible` included
- [ ] Every data state designed — the happy path alone is not enough
- [ ] No filler content; every component answers a question
- [ ] Hierarchy survives the greyscale test
- [ ] Believable as a screenshot of a real product
