---
name: solak-design-ui
description: Designs and implements UX-first, data-dense enterprise interfaces. Starts by identifying the user's primary task, the information hierarchy, the task flow and a layout skeleton; then reduces friction, chooses density and typography, produces an ordered implementation TODO and executes it step by step, validating each item before the next. Visual polish comes last, never first. Covers tables and data grids, filter and query panels, data-entry forms, report screens and metric dashboards, including their loading, empty, no-results, partial, stale, error, conflict and overflow states, and the feedback, retry, undo and confirmation behaviour around them. Tech-agnostic — semantic HTML plus CSS custom properties, adapted to whatever framework is detected. Use when the user works on a table, grid, filter panel, form, report screen or dashboard, says a screen is cluttered, slow to use or unreadable, or invokes /solak-design-ui. Self-contained: carries its own UX workflow, layout, responsive, interaction-state, quality, token, typography, formatting and chart rules, with no dependency on other skills or external rule files. Not for marketing pages, landing pages or brand surfaces.
metadata:
  version: 1.8.0
  author: cagrisolakoglu
  tags: [design, ux, frontend, ui, data-dense, tables, forms, dashboards, self-contained]
  status: beta
---

# solak-design-ui

Designs and builds the screens people work in — tables, filter panels, data-entry forms, dashboards — starting from the user's task rather than from a component.

**Task flow first, then layout, then interaction, then visual design, and implementation details last.** The aesthetic default is restraint: hierarchy comes from type, space and alignment rather than boxes, borders and colour.

## When to Use

- A table, grid, filter panel, form, report screen or dashboard is being built or reworked
- An existing screen is cluttered, slow to use, or unreadable ("400 rows, nothing stands out")
- The states real data produces are missing: empty, loading, partial, error, overflow, too many results
- A screen "feels wrong" and the cause is structural rather than cosmetic

The scope is a **principle, not a list of surface types**: any screen someone works in to reach a result. Internal tools, admin consoles, audit and review surfaces, operator consoles and component benches all qualify even though none of them is "a table" or "a dashboard". The test is: can a primary task be written in one sentence, and does a wrong reading cost something? Then the workflow applies.

Do **not** use this skill for:
- Marketing pages, landing pages, brand surfaces — persuasion, not task completion
- Building a product-wide design system from zero — larger, separate work
- Problems that are behavioural rather than design (data flow, state bugs) — fix the code directly

Charts inside dashboards **are** in scope: type, palette limits, axes and tooltips are in `references/design-quality.md`.

## Scope triage

Classify the request **before** anything else. The wrong process is a real failure: a ten-stage workflow on a missing focus ring wastes the user's time, and an inline fix on a screen redesign skips the gates that make it safe.

| Scope | Typical request | Process |
|-------|-----------------|---------|
| **Micro fix** | One alignment, focus ring, overflow or spacing defect | inspect → fix → verify |
| **Component refinement** | One table, filter panel, form group or metric area | local task check → local layout and state review → short TODO → implement |
| **Screen redesign** | A whole page, or the workflow itself changed | the full ten-stage workflow |
| **Product-wide system** | A design system across every product surface | out of scope — constrain to one representative surface, or route to a separate project |

**Micro fix** — *"The amount column is left-aligned." "The focus ring is missing." "The sticky header overlaps one column."*
Inspect the component, load the reference that owns each named defect and no more, make the smallest change, verify that one thing. **No wireframe, no product-strategy questions, no stage list.** State what you changed and how you checked it.

**Component refinement** — *"This table is too busy." "This filter panel is hard to use."*
Name the local task, review information priority, states and narrow-width behaviour for that component, write a short TODO, stay inside the component and its immediate context. Do not redesign the page around it.

**Screen redesign** — the full workflow below: surface contract, wireframe, responsive failure record, state inventory, TODO, complete validation.

Scope is set by the **work required**, not by the wording of the request. "Just fix the table" on a screen whose information priority is wrong is a refinement, not a micro fix — say so and say why before proceeding.

## Inputs

| Input | Required | Notes |
|-------|----------|-------|
| target surface | ✅ | Which screen or component. A file path, or a description to build from scratch. |
| primary user | ✅ | The role that uses the screen most often. |
| primary task | ✅ | The result the user must reach before leaving the screen, in one sentence. |
| success criterion | ✅ | How the user knows the task is done. |
| device and input | ✅ | Desktop, touch, field device, keyboard-heavy. |
| data volume and use | ✅ | How many records (typical and worst case); scanning, reading or entering. |
| usage frequency | ❌ | Daily, weekly, rare. Changes how much learning cost is acceptable. |
| costly mistake | ❌ | What a wrong decision or action costs. Drives error prevention. |
| style direction | ❌ | If not given, propose three after the layout is settled. |
| technology | ❌ | Detect from the repo; if undetectable, ask. |
| constraints | ❌ | Existing tokens or palette, accessibility target, performance budget. |

**Required means required for a screen redesign.** A micro fix needs none of them, and a component refinement needs only the primary task and the data volume. Do not interrogate someone who asked for a focus ring.

Infer what you can from the repository. If something is still unknown **and materially changes the design**, ask once — all questions in one message.

"Clean", "minimal", "modern" and "nice" are **not directions** — convert them into something concrete and get approval.

## Workflow

**This is the screen-redesign process.** A component refinement runs stages 2, 3, 6, 8 and 9 scoped to the component; a micro fix runs none of it. The procedure, tables and templates live in `references/ux-workflow.md`; read it at Stage 0 and work through it.

Stage 1 of a redesign also produces the **surface contract** — the one-screen statement of user, task, volume, freshness, minimum width, state behaviour and what is out of scope. Template in `templates/design-todo.md`.

1. **Scope and existing system** — Target surface, framework, existing tokens and typography, comparable screens, supported widths, and explicitly what must **not** change.
2. **User, task and decision** — Primary user, why they come, the one-sentence primary task, the decision they make, most frequent action, costliest mistake. *Gate: if the primary task needs more than one sentence, the scope is two screens.*
3. **Content inventory and information priority** — Every item classified (identity / decision / detail / status / primary / secondary / rare) and justified. Remove or demote what supports no decision; merge duplicates. *Gate: no visible item without a stated purpose.*
4. **Task flow and friction** — Entry to completion, where the user waits, where they err, what context must survive. *Gate: the primary task has an entry, an ordered sequence and a completion state.*
5. **Rough layout** — `references/layout-and-information-architecture.md`: regions, reading order, action placement, progressive disclosure, master-detail, sticky context, narrow-screen order, and reserved space for every state. Produce an ASCII wireframe.
   Then `references/responsive-grid.md`: give each region a **minimum usable width**, build the wide composition, and **derive breakpoints by reducing width until the layout fails** — never from device names. Viewport queries drive the page shell, container queries drive reusable components. *Gate: no styling before the wireframe and the failure record exist.*
6. **Usability pass and state inventory** — Ten heuristics against the wireframe; interaction count, safe defaults, shortcuts, focus order, touch targets.
   Then `references/interaction-and-states.md`: list every state the surface can reach and give each one a trigger, what the user sees, what they can do and how it exits. States change how much space a region needs, so they are decided **here, with the wireframe, not after the styling**. *Gate: if the layout does not visibly make the task easier, revise it rather than styling around it. No state left without a recovery path.*
7. **Density, typography and direction** — Now that volume and behaviour are known: `references/density-and-direction.md`, then `references/typography.md`. Typography is **role-based, tokenised and verified with real data**: use the existing product system first; with no system, Inter Variable is the default; measured numbers take tabular lining figures and right alignment, monospace is reserved for technical identifiers, and the font is not "chosen" until its delivery is verified. Choose the direction and **get it approved**; do not assume dark theme. *Gate: density justified in one sentence.*
8. **Implementation TODO** — Dependency-ordered, file-level, one verifiable result and an acceptance criterion per item. **Five or more work items → fill in `templates/design-todo.md`. Fewer than five → an inline list in the response is enough.** The discipline is identical either way; only the artefact changes. *Gate: no code before the list exists, in one form or the other.*
9. **Execute step by step** — Per item: read the files, restate the acceptance criterion, make the smallest scoped change, run checks, validate, mark complete, record the decision. Structure before visuals; states and accessibility are not postponed.
10. **Validate and report** — Run the gates below and produce the Output block.

## Reference routing

**Read the smallest reference set that can safely complete the task.** Every reference is a real cost; loading all fourteen for a one-line fix is not thoroughness, it is noise. The machine-readable form of this table is `manifest.yaml`.

| Situation | Read |
|-----------|------|
| Micro alignment, focus or spacing defect | the reference that **owns each named defect** — one per defect, nothing more |
| Numeric formatting defect | `formatting.md` + `typography.md` |
| Responsive or overflow defect | `responsive-grid.md` + the affected surface |
| Token inconsistency | `tokens.md` + the affected surface |
| Misaligned columns inside one surface | `grid.md` + the affected surface |
| Table / data grid | `tables.md` + `formatting.md` + `typography.md` |
| Filter / search / query panel | `filters.md` + `interaction-and-states.md` |
| Data-entry form | `forms.md` + `interaction-and-states.md` |
| Dashboard / metric summary | `dashboards.md` + `formatting.md` |
| Full screen redesign | `ux-workflow.md` + `layout-and-information-architecture.md` + `responsive-grid.md` + `interaction-and-states.md` + `design-quality.md`, plus the surface row above |

- Read `ux-workflow.md` only for a refinement or a redesign — never for a micro fix.
- Read `design-quality.md` for redesigns and broad refinements, not for every change.
- Read **one** surface reference unless the work genuinely spans two surfaces.
- Follow a cross-link when you need the rule; do not copy the rule between references.
- Facts already established earlier in the task are not re-derived.

Each surface reference opens with a **Read with** list — the cross-cutting files that surface actually needs.

### Canonical ownership

One rule, one home. Everywhere else links to it. When two files seem to disagree, the owner wins and the other file is wrong.

| Rule | Owner |
|------|-------|
| Numeric figures, type roles, minimum sizes | `typography.md` |
| Decimals, units, dates, currency, missing values | `formatting.md` |
| Breakpoint derivation, minimum widths, overflow strategy | `responsive-grid.md` |
| The column grid inside one surface | `grid.md` |
| Loading, error, retry, stale, partial, conflict, offline, undo | `interaction-and-states.md` |
| Column behaviour, alignment, sticky, totals | `tables.md` |
| Applied-filter visibility, staleness presentation | `filters.md` |
| Validation timing, `readonly` vs `disabled`, save state | `forms.md` |
| Tile questions, metric context, freshness | `dashboards.md` |
| Visual restraint, patterns to avoid, chart decisions | `design-quality.md` |
| Row height, separator system, visual direction | `density-and-direction.md` |
| The token layer itself | `tokens.md` |
| Region priority, reading order, progressive disclosure | `layout-and-information-architecture.md` |
| Stage order, gates, output format | `ux-workflow.md` |

**Take screenshots at 320/768/1440 in both themes.** Some breakages appear only in the image while the CSS stays valid and silent. On a scrollable surface, capture it **while scrolled** — sticky failures show up nowhere else.

This skill is **self-contained**: UX workflow, layout, quality criteria, token layer, typography, formatting and chart rules all live under `references/`. It depends on no external rule file and no other skill.

## Verification gates

Gates are scoped like the workflow. A **micro fix** answers only the gates its own change touches — the alignment gate for an alignment fix, the focus gate for a focus fix — plus "nothing else regressed". A **component refinement** answers every gate that applies to the component. A **screen redesign** answers all of them. Claiming a gate you did not check is worse than reporting it unchecked.

**Blocking** — if one fails the work is **not done**; state plainly what is missing:

- [ ] The primary task is written in one sentence
- [ ] Information priority documented; every initially-visible item supports a decision
- [ ] A rough layout or wireframe exists, and predates the styling
- [ ] Flow and friction evaluated
- [ ] An implementation TODO list was created and executed item by item, each validated
- [ ] Loading / first-use empty / filtered no-results / error states designed, and first-use is not the same component as no-results
- [ ] Every state in the inventory has a trigger, visible feedback, a user action and an exit condition
- [ ] Refresh keeps usable data on screen — never emptied, never dimmed to signal staleness
- [ ] Errors state what failed and what to do; retry **names what it retries** and does not clear existing content
- [ ] Destructive actions state their scope; irreversible ones confirm, routine reversible ones offer undo instead
- [ ] Critical confirmation is never toast-only; loading and pending carry text, not just a spinner
- [ ] A conditional component is actually hidden when hidden — a `display` rule on it defeats the `hidden` attribute and renders an empty strip in the success state
- [ ] Concurrent edits cannot silently overwrite newer data; user input survives a validation or request failure
- [ ] The primary task is completable by keyboard; `focus-visible` is visible
- [ ] Text contrast ≥ 4.5:1 (large text ≥ 3:1), status colours included
- [ ] Colour is never the only indicator — an icon or text accompanies it
- [ ] Measured numbers use `tabular-nums lining-nums` and are right-aligned — **headers on the same axis**; identifiers are left-aligned
- [ ] Monospace only on technical identifiers; never on metrics or table numbers
- [ ] Existing typography system inspected; typeface justified and **font delivery verified** (a CSS declaration does not prove the font loaded)
- [ ] No functional text below 12px, no dense body text below 13px; unit symbol casing preserved; root `lang` declared
- [ ] Number and date formats follow the product locale via `Intl`; decimal places constant down a column
- [ ] Missing data is distinguishable from zero (`—`) and excluded from totals
- [ ] Body weight ≥ 400, from a closed weight token set; de-emphasis done with ink
- [ ] No hardcoded palette, spacing or type value inside components; the existing token system was used, not duplicated
- [ ] No overflow at 320px **and** the narrowing strategy is measurably usable there — declaring it is not enough
- [ ] Breakpoints derived from **recorded layout failures**, not device names; each one named for the behaviour it triggers
- [ ] Container queries used for components that can be constrained (panel, drawer, dialog) — a viewport query cannot describe them
- [ ] Layout usable at 200% zoom; every region declares an overflow strategy
- [ ] Fields and columns start on shared grid lines
- [ ] `readonly` and `disabled` are distinguishable **in dark theme too**
- [ ] `references/design-quality.md`: none of the avoided patterns present, at least five required qualities met

**Reported** — if missing, say so; work does not stop:

- [ ] Partial data / too many results / overflowing cell states
- [ ] Offline behaviour, background operations, optimistic updates — implemented or explicitly out of scope
- [ ] Data freshness shown where it matters; cached or delayed data is not labelled live
- [ ] `prefers-reduced-motion` counterpart
- [ ] Both themes look deliberate
- [ ] Density choice justified
- [ ] Totals computed from raw values; any rounding discrepancy declared
- [ ] No real user test, real-device test, dark-theme visual check, performance test or virtualisation test — state whichever was skipped

## Output

Full template in `references/ux-workflow.md`.

```
User
  Role: Operations specialist
  Primary task: Find anomalous usage records and start investigating them
  Success criterion: Every anomaly in the period is dismissed or assigned

UX decision
  Main flow: enter → narrow by period → scan deviation → open record → act → verify
  Removed friction:
    - Filter change no longer empties the table (previous result stays, staleness announced)
    - Deviation promoted from a detail column to the decision column
    - Record detail moved from a modal to a side panel; filters survive

Layout
  Main regions: 1. context + export   2. query + applied filters   3. anomaly line
                4. dense table        5. selection + bulk
  Narrow-screen strategy: rows fold to cards below 560px — the identity block
  measured 52% of a 320px viewport, so horizontal scroll was rejected

States
  Initial loading: real headers, skeleton values only, no layout shift
  Refresh: existing rows stay readable; stale banner + last-updated time
  Partial: 7 unavailable records named and excluded from totals
  Error: the failed source is named; retry affects only that source
  Destructive: bulk dismiss states its scope and offers undo for 10s
  Offline: not implemented — declared as a risk

Visual system
  Density: dense (28px rows) — 400+ records, operator scanning, desktop primary
  Direction: Swiss/International · Typography: existing product system
  Numbers: tabular + lining, right-aligned

TODO summary
  ✅ 14 completed · ⚠️ 2 validations pending · ❌ 0 blocking gaps

Changed files
  + src/styles/tokens.css
  ~ src/components/UsageTable.*
  ~ src/components/FilterPanel.*

Validation
  ✅ contrast 7.1:1 · ✅ keyboard + focus-visible · ✅ tabular + lining figures
  ✅ empty/loading/no-results/error · ✅ 320px fold verified by screenshot
  ⚠️ reduced-motion added, not tried on a real device
  ⚠️ dark theme tokens exist, not verified by eye

Remaining risks
  - Virtualisation untested above ~2,000 rows
  - No real user test performed
```

## Guardrails

- **Layout before styling.** No visual styling before the rough layout and information order exist.
- **Task before component.** Define the user's task before choosing a table, form or dashboard.
- **One primary job per screen.** If the primary task cannot be written in one sentence, split the scope.
- **No implementation without a TODO.** Build a dependency-ordered work list before coding.
- **Do not optimise the rare path first.** Never make the frequent path harder to accommodate rare controls.
- **Do not hide system state.** Loading, stale, partial, empty and error are part of the layout, not additions to it.
- **Minimalism must not remove necessary context.** Simplification that costs information is not simplification.
- **Do not ask for approval at every micro-step.** Ask only about expensive, hard-to-reverse decisions, grouped into one message.
- **Do not design without context.** If product, user, task or data volume is unknown, ask.
- If a token layer exists, use it; never stand up a second system. Never overwrite existing style files without reading them.
- Never trade accessibility for aesthetics — contrast and focus indicators are not negotiable.
- Do not add a dependency (grid or UI library) **unless asked**; if CSS solves it, use CSS.
- **Never render missing data as zero.** It leads to wrong decisions.
- Do not drift into marketing or brand surface work; the scope is working screens.

## Examples

```
/solak-design-ui src/app/usage/page.tsx "400+ rows, operators scan for anomalies"
/solak-design-ui "filter panel, 6 criteria, results are slow to arrive"
/solak-design-ui src/components/InvoiceTable.tsx "this table is unreadable, too busy"
```

The third example is a screen-level request in disguise: "too busy" is an information-priority problem, so it still runs Stages 2-6 — but scope stays on the table and its fit with existing tokens. A genuinely small defect (one misaligned column, a missing focus ring) skips to the fix.
