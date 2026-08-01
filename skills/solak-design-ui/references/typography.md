# Typography

> Apply these rules at Stage 6 of `ux-workflow.md`, once the layout and data volume are known. Type size and density are not the fix for a screen whose information has no priority order.

In a data-dense surface, typography is not decoration but a **reading instrument**: the wrong figure set breaks column alignment, the wrong family slows scanning, the wrong weight destroys legibility. Number formatting and locale (separators, decimals) live in `formatting.md`; this file covers family, figures and weight.

## 1 · Use the existing system first

If the project has typography tokens, **use them**; do not stand up a parallel scale. How to find them is in `tokens.md`. A framework default is also a system: a Material-based product already has its own scale. Changing a product's typeface is a brand decision, not a typography decision, and not this skill's job.

## 2 · No system? Inter Variable

```css
:root {
  --font-ui: "Inter Variable", "Inter var", Inter,
             ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
}
```

Inter was designed for dense UI: large x-height, unambiguous `1`/`l`/`I` and `0`/`O`, a complete tabular figure set. The variable version covers 400-600 in one file.

**The fallback chain is part of the rule.** If Inter is neither installed nor self-hosted, the browser silently drops to Arial — the rule looks applied while the result is not. Three paths, in order:

1. **Self-host** (preferred) — put the `woff2` in the project, `@font-face` plus `font-display: swap`. One variable file is enough; do not download separate 400/500/600 files.
2. **Assume installed** — only when it is known to be distributed by device management.
3. **Fall back to the system font** — `system-ui` / `Segoe UI` / `-apple-system` is acceptable, but then **verify the figure set** (below), because fallback fonts differ in tabular support.

State which path was taken in the report. "We used Inter" does not prove it loaded — look at the letterforms in a screenshot.

## 3 · No monospace in tables or metrics

Do **not** use monospace for measured numbers, metrics or KPI values. Monospace gives every character equal width; in a dense table the column widens needlessly and the digits thin out, slowing the scan. A sans with tabular figures already aligns the digits — it delivers monospace's only benefit without paying its cost.

## 4 · Three settings together in numeric cells

```css
.num {
  font-variant-numeric: tabular-nums lining-nums;
  text-align: right;
}
```

- **`tabular-nums`** — every digit the same width; digits line up vertically
- **`lining-nums`** — digits sit at a uniform height. Some families default to **oldstyle** figures (descending `3`, `4`, `7`, `9`); `tabular-nums` alone does not fix this, and the column ends up aligned but visually jittery
- **Right alignment** — the alignment-by-type table is in `tables.md`
- **Constant decimal places** — fixed down the column; rationale and a per-quantity table are in `formatting.md`

None of them does its job without the others. Verification: in a column, is the **last digit** of `1,284,690` on the same vertical line as the last digit of `98,440`?

## 5 · Monospace only for technical identifiers

Monospace belongs to values that are read **character by character** and dictated aloud:

| Monospace | Not monospace |
|-----------|---------------|
| UUID, GUID | Amounts, quantities, percentages |
| Account / SKU / registry codes | Dates, times, period labels (`2026-07`) |
| Serial numbers | Person and place names |
| Endpoints, URL paths | Status labels |
| Hashes, commit SHAs | Page and record counts |
| Log lines, stack traces | Sort and filter values |

```css
:root { --font-mono: ui-monospace, "SF Mono", "Cascadia Mono", Consolas, monospace; }
.ident-tech {
  font-family: var(--font-mono);
  font-variant-numeric: tabular-nums lining-nums;
  letter-spacing: 0;
}
```

### When 3 and 5 collide: content wins, container does not

A serial number lives **in a table column**. Rule 3 says "no monospace in tables", rule 5 says "serial numbers are monospace" — the contradiction is apparent, not real:

- Rule 3 governs **measured numbers**: values that are compared, summed, averaged
- Rule 5 governs **identifiers**: values that are not compared but dictated and copied

The decision looks at **what the cell carries**, not where it sits. So: the amount column is sans plus tabular, the serial column is monospace. Both appear in the same table and that is correct — an identity column should look different, because its job is different.

A monospace identifier is **left-aligned** (an identifier is not a number, see `formatting.md`), and since monospace already aligns the characters, no `letter-spacing` is needed.

## 6 · Dense defaults

| Role | Size | Line height | Weight |
|------|------|-------------|--------|
| Body / cell | 13px | 1.35 | 400 |
| Heading / label | 12px | 1.3 | 500 |

```css
[data-density="dense"] {
  --text-body:     0.8125rem;  /* 13px */
  --leading-body:  1.35;
  --text-label:    0.75rem;    /* 12px */
  --leading-label: 1.3;
  --weight-body:   400;
  --weight-label:  500;
}
```

500 is a **default, not a ceiling**: using 600 to mark a decision column is a legitimate deviation — but it must be deliberate, and not on every heading.

### Weights are a closed token set, not a continuum

A variable font accepts any value between 400 and 600, and that is a trap: components drift to 450, 550, 650, and after a few weeks two surfaces in the same product carry six different weights that nobody chose. Nothing looks broken; the family just stops reading as one system.

Expose exactly three steps and use only those:

```css
:root {
  --weight-body:   400;   /* body, cells, help text */
  --weight-label:  500;   /* headings, labels, badges */
  --weight-strong: 600;   /* the ONE emphasis step: decision column, total row, page title */
}
```

If a component "needs" 550, the question is which of the three it actually belongs to. A fourth step means the hierarchy is being solved with weight where it should be solved with size, space or ink.

This is easy to audit and worth auditing:

```bash
rg -n "font-weight: [0-9]" src   # anything but var(--weight-*) is a drift
```

### If the heading is smaller than the body, it needs a second cue

12px headings are smaller than 13px body text. In dense product UI this is deliberate, but it only works **if the heading carries a signal beyond size**:

```css
th { text-transform: uppercase; letter-spacing: 0.04em; color: var(--ink-strong); }
```

Without uppercase, letter-spacing and strong ink, a 12px/500 heading looks like "small body text" and the hierarchy **inverts**. If using uppercase, check the traps in `tables.md` for unit symbols and locale-aware casing.

## 7 · Never below 400

Do not use 300 or thinner in a data-dense surface. At 13px, thin body text turns grey on light backgrounds and falls apart under greyscale font smoothing; in dark theme the opposite happens — thin letterforms bloom and their edges smear.

To reduce emphasis, lower the **ink**, not the weight: `--ink-body` → `--ink-muted`. The contrast floor (≥ 4.5:1) is preserved and the letterforms stay intact.

## 8 · Minimalism is not shrinking the text

If a screen looks cluttered, **reducing font size is the wrong fix**: it converts clutter into illegibility, changes the measure, flattens the hierarchy and damages accessibility.

What to reduce, in this order:

1. **Colour** — how many distinct hues are present? Remove every non-semantic one
2. **Separators** — zebra *or* rules, never both (`tables.md`); no box inside a box
3. **Emphasis** — how many elements are bold or accented? If everything is emphasised, nothing is
4. **Content** — any tile, column or field that answers no question (`design-quality.md`)
5. **Space** — keep group spacing, cut decorative space

Lowering the density level (`compact` → `dense`) is a *token* decision and comes with row height attached; shrinking `font-size` alone is not density, it is compression (`density-and-direction.md`).

## Verification

- [ ] Existing typography system used if present; no second scale created
- [ ] With no system, Inter Variable **actually loaded** (self-hosted or verified); fallback strategy reported
- [ ] No monospace on measured numbers or metrics
- [ ] Numeric cells use `tabular-nums lining-nums` + right alignment + constant decimals
- [ ] The longest and shortest number in a column end on the same vertical line
- [ ] Monospace only on technical identifiers (UUID, codes, serials, endpoints, hashes, logs); identifiers left-aligned
- [ ] At dense: body 13/1.35/400, heading 12/1.3/500; deviations deliberate
- [ ] No weight below 400; de-emphasis achieved with ink
- [ ] Weights come from a closed three-step token set; no literal `font-weight` values in components
- [ ] Clutter was not solved by shrinking text; colour, separators and emphasis were reduced instead
