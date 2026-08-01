---
name: solak-design-ui
description: Designs and implements UX-first, data-dense enterprise interfaces. Starts by identifying the user's primary task, the information hierarchy, the task flow and a layout skeleton; then reduces friction, chooses density and typography, produces an ordered implementation TODO and executes it step by step, validating each item before the next. Visual polish comes last, never first. Covers tables and data grids, filter and query panels, data-entry forms, report screens and metric dashboards, including their loading, empty, no-results, partial, error and overflow states. Tech-agnostic — semantic HTML plus CSS custom properties, adapted to whatever framework is detected. Use when the user works on a table, grid, filter panel, form, report screen or dashboard, says a screen is cluttered, slow to use or unreadable, or invokes /solak-design-ui. Self-contained: carries its own UX workflow, layout, quality, token, typography, formatting and chart rules, with no dependency on other skills or external rule files. Not for marketing pages, landing pages or brand surfaces.
metadata:
  version: 1.4.0
  author: cagrisolakoglu
  tags: [design, ux, frontend, ui, data-dense, tables, forms, dashboards, self-contained]
  status: draft
---

# solak-design-ui

Designs and builds the screens people work in — tables, filter panels, data-entry forms, dashboards — starting from the user's task rather than from a component.

**Task flow first, then layout, then interaction, then visual design, and implementation details last.** The aesthetic default is restraint: hierarchy comes from type, space and alignment rather than boxes, borders and colour.

## When to Use

- A table, grid, filter panel, form, report screen or dashboard is being built or reworked
- An existing screen is cluttered, slow to use, or unreadable ("400 rows, nothing stands out")
- The states real data produces are missing: empty, loading, partial, error, overflow, too many results
- A screen "feels wrong" and the cause is structural rather than cosmetic

Do **not** use this skill for:
- Marketing pages, landing pages, brand surfaces — out of scope
- Building a product-wide design system from zero — larger, separate work
- Problems that are behavioural rather than design (data flow, state bugs) — fix the code directly

Charts inside dashboards **are** in scope: type, palette limits, axes and tooltips are in `references/design-quality.md`.

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

Infer what you can from the repository. If something is still unknown **and materially changes the design**, ask once — all questions in one message.

"Clean", "minimal", "modern" and "nice" are **not directions** — convert them into something concrete and get approval.

## Workflow

Ten stages. The procedure, tables and templates live in `references/ux-workflow.md`; read it at Stage 0 and work through it.

1. **Scope and existing system** — Target surface, framework, existing tokens and typography, comparable screens, supported widths, and explicitly what must **not** change.
2. **User, task and decision** — Primary user, why they come, the one-sentence primary task, the decision they make, most frequent action, costliest mistake. *Gate: if the primary task needs more than one sentence, the scope is two screens.*
3. **Content inventory and information priority** — Every item classified (identity / decision / detail / status / primary / secondary / rare) and justified. Remove or demote what supports no decision; merge duplicates. *Gate: no visible item without a stated purpose.*
4. **Task flow and friction** — Entry to completion, where the user waits, where they err, what context must survive. *Gate: the primary task has an entry, an ordered sequence and a completion state.*
5. **Rough layout** — `references/layout-and-information-architecture.md`: regions, reading order, action placement, progressive disclosure, master-detail, sticky context, narrow-screen order, and reserved space for every state. Produce an ASCII wireframe. *Gate: no styling before this exists.*
6. **Usability pass** — Ten heuristics against the wireframe; interaction count, safe defaults, shortcuts, focus order, touch targets. *Gate: if the layout does not visibly make the task easier, revise it rather than styling around it.*
7. **Density, typography and direction** — Now that volume and behaviour are known: `references/density-and-direction.md`, then `references/typography.md`. Typography is **role-based, tokenised and verified with real data**: use the existing product system first; with no system, Inter Variable is the default; measured numbers take tabular lining figures and right alignment, monospace is reserved for technical identifiers, and the font is not "chosen" until its delivery is verified. Choose the direction and **get it approved**; do not assume dark theme. *Gate: density justified in one sentence.*
8. **Implementation TODO** — Fill in `templates/design-todo.md`. Dependency-ordered, file-level, one verifiable result and an acceptance criterion per item. *Gate: no code before the list exists.*
9. **Execute step by step** — Per item: read the files, restate the acceptance criterion, make the smallest scoped change, run checks, validate, mark complete, record the decision. Structure before visuals; states and accessibility are not postponed.
10. **Validate and report** — Run the gates below and produce the Output block.

Read **only the reference that applies** to the surface, and only at Stage 9:

- Table / data grid → `references/tables.md`
- Filter / search / query panel → `references/filters.md`
- Data-entry form → `references/forms.md`
- Dashboard / metric summary → `references/dashboards.md`

Cross-cutting, independent of surface:

- `references/design-quality.md` — always: quality criteria, restraint rules, patterns to avoid, chart decisions
- `references/grid.md` — any multi-field or multi-column surface (horizontal rhythm)
- `references/formatting.md` — wherever numbers, dates, units or money appear
- `references/tokens.md` — when there is no token layer, or an existing one must be read

**Take screenshots at 320/768/1440 in both themes.** Some breakages appear only in the image while the CSS stays valid and silent. On a scrollable surface, capture it **while scrolled** — sticky failures show up nowhere else.

This skill is **self-contained**: UX workflow, layout, quality criteria, token layer, typography, formatting and chart rules all live under `references/`. It depends on no external rule file and no other skill.

## Verification gates

**Blocking** — if one fails the work is **not done**; state plainly what is missing:

- [ ] The primary task is written in one sentence
- [ ] Information priority documented; every initially-visible item supports a decision
- [ ] A rough layout or wireframe exists, and predates the styling
- [ ] Flow and friction evaluated
- [ ] An implementation TODO list was created and executed item by item, each validated
- [ ] Loading / first-use empty / filtered no-results / error states designed, and first-use is not the same component as no-results
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
- [ ] Fields and columns start on shared grid lines
- [ ] `readonly` and `disabled` are distinguishable **in dark theme too**
- [ ] `references/design-quality.md`: none of the avoided patterns present, at least five required qualities met

**Reported** — if missing, say so; work does not stop:

- [ ] Partial data / too many results / overflowing cell states
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
