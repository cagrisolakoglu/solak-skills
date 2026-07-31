---
name: solak-design-ui
description: Designs and implements data-dense product UI — tables and data grids, filter and query panels, data-entry forms, and metric dashboards. Decides row and field density deliberately, aligns numbers and text by type, designs the states real data produces (empty, loading, partial, error, overflow, too many results), and keeps every value on a token layer. Defaults to restraint: hierarchy comes from type, space and alignment rather than boxes, borders and colour. Tech-agnostic — semantic HTML plus CSS custom properties, adapted to whatever framework is detected. Use when the user works on a table, grid, filter panel, form, report screen or dashboard, says a screen is cluttered or unreadable, or invokes /solak-design-ui. Self-contained: carries its own quality criteria, token layer, typography, formatting and chart rules, with no dependency on other skills or external rule files. Not for marketing pages, landing pages or brand surfaces.
metadata:
  version: 1.2.0
  author: cagrisolakoglu
  tags: [design, frontend, ui, data-dense, tables, forms, dashboards, self-contained]
  status: draft
---

# solak-design-ui

Designs and builds the screens people work in — tables, filter panels, data-entry forms, dashboards — by deciding density and states on purpose instead of by default.

The aesthetic default is **restraint**: fewer visual devices, more alignment. Density is about how much data fits, not how much decoration surrounds it.

## When to Use

- A table or data grid is being built, or an existing one is unreadable ("400 rows, nothing stands out")
- Filter/query panel, data-entry form, report screen or metric dashboard work
- The states real data produces are missing: empty, loading, partial, error, overflow, too many results
- A screen "feels cluttered" and the cause is visual, not behavioural

Do **not** use this skill for:
- Marketing pages, landing pages, brand surfaces — out of scope
- Building a product-wide design system from zero — larger, separate work; this skill writes one surface's tokens, it does not found a system
- Problems that are behavioural rather than visual (data flow, state, bugs) — fix the code directly

Charts inside dashboards **are** in scope: type, palette limits, axes and tooltips are covered in `references/design-quality.md`.

## Inputs

| Input | Required | Notes |
|-------|----------|-------|
| target surface | ✅ | Which screen or component. A file path, or a description to build from scratch. |
| product context | ✅ | What it does, who uses it. If unknown, **ask**. |
| data volume and use | ✅ | How many records (typical and worst case); is the user scanning or reading. Density depends on it — if unknown, **ask**. |
| style direction | ❌ | If not given, propose three and get approval. |
| technology | ❌ | Detect from the repo; if undetectable, ask. |
| constraints | ❌ | Existing tokens or palette, accessibility target, performance budget. |

"Clean", "minimal", "modern" and "nice" are **not directions** — convert them into something concrete and get approval.

## Workflow

1. **Read the context** — Token layer, existing table/form patterns, theme support, framework detection (file extensions and package manifest).
2. **Identify the surface** and read **only the reference that applies**:
   - Table / data grid → `references/tables.md`
   - Filter / search / query panel → `references/filters.md`
   - Data-entry form → `references/forms.md`
   - Dashboard / metric summary → `references/dashboards.md`

   Cross-cutting references, independent of surface:
   - `references/design-quality.md` — always: quality criteria, restraint rules, patterns to avoid, chart decisions
   - `references/typography.md` — always: family, figure set, monospace scope, weight floor
   - `references/grid.md` — required on any multi-field or multi-column surface (horizontal rhythm)
   - `references/formatting.md` — required wherever numbers, dates, units or money appear
   - `references/tokens.md` — when there is no token layer, or an existing one must be read
3. **Commit to a density** — `references/density-and-direction.md`: `comfortable` / `compact` / `dense`. The decision follows three questions (record count, scanning vs reading, screen and input). State the reasoning in the report.
   Density sets **vertical** rhythm, the grid sets **horizontal** rhythm; on a multi-field surface both are decided together.
4. **Choose a direction** — three options from the same reference. Justify in one sentence and **get the user's approval**. Do not assume dark theme.
5. **Use or write tokens** — If a token layer exists, **use it**; never build a parallel system. Otherwise follow `references/tokens.md`: palette, type scale, spacing, density, **column count and gutter**, duration and easing as CSS custom properties.
6. **Build** — Semantic HTML (`table`/`th`/`fieldset`/`label`, not a pile of generic `div`s). Every state from the surface reference, plus every interaction state: hover, `focus-visible`, active, disabled/readonly, selected.
7. **Motion (if any)** — `transform`, `opacity`, `clip-path` only. Write the `prefers-reduced-motion` counterpart.
8. **Verify** — Run the gates below and report the result. **Take screenshots at 320/768/1440 in both light and dark**; some breakages appear only in the image, while the CSS stays valid and silent. On a scrollable surface, capture it **while scrolled** — sticky failures show up nowhere else. Take one **greyscale** capture as well (`filter: grayscale(1)`) — it is the cheapest way to find information that exists only in colour.

This skill is **self-contained**: quality criteria, token layer, typography, formatting and chart rules all live under `references/`. It depends on no external rule file and no other skill.

## Verification gates

**Blocking** — if one fails the work is **not done**; state plainly what is missing:

- [ ] Text contrast ≥ 4.5:1 (large text ≥ 3:1), status colours included
- [ ] Colour is never the only indicator — an icon or text accompanies it
- [ ] Keyboard reachable, `focus-visible` visible, including navigation inside grids and forms
- [ ] Empty / loading / error states exist
- [ ] Measured numbers use `tabular-nums lining-nums` and are right-aligned; identifiers are left-aligned (`references/formatting.md`)
- [ ] Monospace only on technical identifiers (UUID, code, endpoint, hash); never on metrics or table numbers (`references/typography.md`)
- [ ] Number and date formats follow the product locale and are produced by `Intl`, not by hand; decimal places constant down a column
- [ ] Missing data is distinguishable from zero (`—`) and excluded from totals
- [ ] Body weight ≥ 400; de-emphasis done with ink, not weight
- [ ] No hardcoded palette, spacing or type value inside components
- [ ] No overflow at 320px **and** the narrowing strategy is actually usable at that width — declaring it is not enough (`references/tables.md`, the 40% threshold)
- [ ] Fields and columns start on shared grid lines — no "each one its own width" layout built from content-width flex (`references/grid.md`)
- [ ] `readonly` and `disabled` are distinguishable **in dark theme too**
- [ ] `references/design-quality.md`: none of the avoided patterns present, at least five required qualities met
- [ ] Greyscale capture checked: no information (status, good/bad, series identity) exists only in colour

**Reported** — if missing, say so; work does not stop:

- [ ] Partial data / too many results / overflowing cell states
- [ ] `prefers-reduced-motion` counterpart
- [ ] Both themes look deliberate
- [ ] Density choice justified
- [ ] Totals computed from raw values; any rounding discrepancy declared

## Output

```
Surface: data grid · Density: dense · Direction: Swiss/International
Reasoning: 400+ records, an operator scanning for values, desktop primary

Files
  + src/styles/tokens.css        palette, type scale, density levels
  ~ src/components/UsageTable.*

Decisions
  - dense (28px rows) + tabular-nums; numeric columns right-aligned
  - Narrowing: identity column sticky, detail columns reachable by horizontal scroll
  - Single separator system: zebra (many columns, high risk of losing the row)
  - "No results" and "first use" are separate components
  - One accent, no decorative colour; hierarchy from type scale and space

Verification
  ✅ contrast 7.1:1 · ✅ keyboard + focus-visible · ✅ tabular + lining figures
  ✅ empty/loading/error · ✅ no hardcoded values · ✅ 320px strategy usable
  ⚠️  reduced-motion added, not tried on a real device
  ⚠️  dark theme tokens exist, not verified by eye
```

## Guardrails

- **Do not design without context.** If product, user or data volume is unknown, ask.
- **Get the direction approved.** It is expensive to reverse.
- If a token layer exists, use it; never stand up a second system.
- Never overwrite existing style files **without reading them**.
- Never trade accessibility for aesthetics — contrast and focus indicators are not negotiable.
- Do not add a dependency (grid or UI library) **unless asked**; if CSS solves it, use CSS.
- **Never render missing data as zero.** It leads to wrong decisions.
- Do not drift into marketing or brand surface work; the scope is working screens.

## Examples

```
/solak-design-ui src/app/usage/page.tsx "400+ rows, operators scan for values"
/solak-design-ui "filter panel, 6 criteria, results are slow to arrive"
/solak-design-ui src/components/InvoiceTable.tsx "this table is unreadable, too busy"
```

In the third example the skill does not redesign the whole page; it keeps scope to the table and its fit with existing tokens.
