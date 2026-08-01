# Typography

> Apply these rules at Stage 6 of `ux-workflow.md`, once the layout and data volume are known. Type size and density are not the fix for a screen whose information has no priority order.

In a data-dense surface, typography is not decoration but a **reading and comparison instrument**: the wrong figure set breaks column alignment, the wrong family slows scanning, the wrong weight destroys legibility.

> **Typography must reduce cognitive load before it adds visual identity.**

A good data-dense type system is close to invisible. The user should notice the value, the comparison, the status and the action — not the font.

**Minimalism is not** smaller text, thinner text, lower contrast, fewer labels, hidden context, dropped units, or grey everything. **Minimalism is** fewer sizes, fewer weights, fewer emphases, clear roles, predictable alignment, consistent number formatting.

Number formatting and locale (separators, decimals, units) live in `formatting.md`; this file covers family, roles, figures, weight, spacing and verification.

## Decision order

1. Detect the existing product typography system
2. Preserve usable brand and framework conventions
3. Identify surface type and density
4. Identify whether the user reads, scans, compares or enters
5. Choose typography roles
6. Choose numeric behaviour
7. Choose size, weight and line-height tokens
8. Verify loading and fallback
9. Verify accessibility, localisation and behaviour on real data
10. Report the decisions and the unresolved risks

Never choose a typeface because it looks modern.

## 1 · Use the existing system first

If the project has typography tokens, **use them**; do not stand up a parallel scale. Look for CSS custom properties, Sass variables, Tailwind theme tokens, framework typography classes, Material type configuration, design-system packages, theme providers, existing `@font-face` rules, framework font loaders, brand guidelines.

```text
src/styles/tokens.css   src/styles/theme.css   src/css/   app.css   globals.css
tailwind.config.*       quasar.config.*        theme.*    tokens.*  typography.*
```

Search commands are in `tokens.md`. A framework default **is** a system: a Material product keeps its configured type scale; a mature design system is extended through its tokens, not bypassed with component-local values. Changing a product's typeface is a brand decision, not a typography decision, and not this skill's job.

## 2 · No system? Choose deliberately

**Default: Inter Variable.** Neutral character, high x-height, legible at small sizes, unambiguous `1`/`I`/`l` and `0`/`O`, complete tabular figures, broad language coverage, 400-600 in one variable file. It behaves predictably in tables, forms and dashboards.

```css
:root {
  --font-ui: "Inter Variable", "Inter var", Inter,
             ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
```

Alternatives, each chosen for a reason rather than a mood:

| Family | Use when | Caution |
|--------|----------|---------|
| **Inter Variable** | Default; very dense operational grids | — |
| **Geist Sans** | Developer tools, configuration and admin screens, medium-density SaaS | More personality than Inter; not the safer pick for long-session dense grids |
| **IBM Plex Sans** | Engineering, infrastructure, industrial monitoring, compliance | Visible character — use it intentionally, not by accident |
| **Source Sans 3** | Report-heavy systems, documentation panels, long forms, mixed content | Optimised for reading, not for maximum density |
| **System stack** | External fonts not allowed, strict performance budget, offline or managed environments | Figure support varies — verify tabular behaviour in the actual target environment |

## 3 · Font delivery is part of the decision

The typography decision is not finished until the font is proven to load. If Inter is neither installed nor self-hosted, the browser silently drops to Arial — the rule looks applied while the result is not.

Preferred order: **self-hosted variable WOFF2** → approved framework loader → managed internal host → system stack.

```css
@font-face {
  font-family: "Inter Variable";
  src: url("/fonts/InterVariable.woff2") format("woff2");
  font-style: normal;
  font-weight: 400 600;      /* only the range actually used */
  font-display: swap;
}
```

- One variable file beats separate 400/500/600 files
- Do not load italic unless the product uses it
- Do not depend on a public CDN in restricted enterprise environments
- **Verify in devtools:** the network request succeeded and computed styles show the intended family. A CSS declaration proves nothing

Report one line:

```text
Font delivery: self-hosted variable WOFF2 | framework-managed | system fallback | existing project configuration preserved
```

## 4 · Roles, not sizes

A token says what it is **for**. `text-caption` survives a redesign; `text-small` becomes a lie the first time the scale shifts.

| Role | Purpose |
|------|---------|
| `caption` | Metadata, timestamps, hints, secondary notes, column headers |
| `label` | Field labels, compact section labels |
| `data` | Table cells, operational values, compact form values |
| `body` | Descriptions, help text, ordinary content |
| `section` | Section headings, grouped surface titles |
| `title` | Page title |
| `metric` | Primary KPI or decision value |
| `identifier` | UUID, registry code, serial number, endpoint, hash |

Avoid `text-tiny`, `text-small`, `text-smaller`, `text-big`.

### Scale

```css
:root {
  --text-caption:    0.75rem;    /* 12px */
  --text-data:       0.8125rem;  /* 13px */
  --text-body:       0.875rem;   /* 14px */
  --text-section:    1rem;       /* 16px */
  --text-title:      1.25rem;    /* 20px */
  --text-metric-sm:  1.5rem;     /* 24px */
  --text-metric-lg:  2rem;       /* 32px */

  --leading-tight:   1.2;
  --leading-label:   1.3;
  --leading-data:    1.35;
  --leading-body:    1.45;
  --leading-reading: 1.6;

  --weight-body:   400;
  --weight-label:  500;
  --weight-strong: 600;
}
```

Five functional sizes plus two metric sizes. More than that needs justification.

### Weights are a closed set, not a continuum

A variable font accepts any value between 400 and 600, and that is the trap: components drift to 450, 550, 650, and within weeks two surfaces in the same product carry six weights nobody chose. Nothing looks broken; the family just stops reading as one system.

```text
400 — content, cells, help text
500 — labels, headers, badges
600 — the ONE emphasis step: decision column, total row, page title
```

If a component "needs" 550, the question is which of the three it belongs to. A fourth step means hierarchy is being solved with weight where it should be solved with size, space or ink. Audit it:

```bash
rg -n "font-weight: [0-9]" src   # anything but var(--weight-*) is drift
```

## 5 · Density defaults

Typography follows the density chosen in `density-and-direction.md`.

| Level | Surface text | Line height | Label | Use for |
|-------|--------------|-------------|-------|---------|
| `comfortable` | 15px | 1.45 | 13px | Touch, low record counts, reading, infrequent users, field work |
| `compact` | 14px | 1.4 | 12px | Mixed reading and scanning, 20-100 records, standard desktop |
| `dense` | 13px | 1.35 | 12px | 100+ records, expert users, comparison-heavy, desktop-first |

```css
[data-density="comfortable"] { --surface-text-size: 0.9375rem; --surface-line-height: 1.45; --surface-label-size: 0.8125rem; }
[data-density="compact"]     { --surface-text-size: 0.875rem;  --surface-line-height: 1.4;  --surface-label-size: 0.75rem; }
[data-density="dense"]       { --surface-text-size: 0.8125rem; --surface-line-height: 1.35; --surface-label-size: 0.75rem; }
```

- Never below **13px** for body text in a dense operational surface, never below **12px** for any functional text
- Row height, padding, line height, separators and alignment change **together** — shrinking the font alone is compression, not density
- Touch targets stay ≥ 44px even when the text is compact
- Accessibility constraints beat density preferences

### If the label is smaller than the body, it needs a second cue

At dense, a 12px header sits under 13px body text. That inversion is deliberate but only works **if the header carries a signal beyond size**:

```css
th { text-transform: uppercase; letter-spacing: 0.02em; color: var(--ink-strong); font-weight: var(--weight-label); }
```

Without uppercase, tracking and strong ink, a 12px/500 heading reads as "small body text" and the hierarchy inverts.

## 6 · Numeric typography

Mandatory in data-dense interfaces. Applies to money, energy, power, percentages, rates, quantities, balances, counts.

```css
.numeric {
  text-align: right;
  font-variant-numeric: tabular-nums lining-nums;
  /* explicit fallback for families with partial support */
  font-feature-settings: "tnum" 1, "lnum" 1;
}
```

- **`tabular-nums`** — equal digit widths, so digits line up vertically
- **`lining-nums`** — uniform digit height. Some families default to **oldstyle** figures (descending `3`, `4`, `7`, `9`); `tabular-nums` alone does not fix it and the column aligns while the line jitters
- **Right alignment** — full alignment-by-type table in `tables.md`

Verification is one glance — these must share a right edge:

```text
          912.00
       18,390.25
    1,284,724.10
           -4.80
```

### The header shares the axis

```css
th[data-type="number"], td[data-type="number"] { text-align: right; }
```

A left-aligned header over right-aligned values creates two visual axes and slows every comparison in the column.

### Precision is constant down a column

```text
✅ 12.40   ❌ 12.4
   8.00       8
   0.75       0.7500
```

Precision is a **domain rule** per quantity, not a per-cell formatting choice:

| Quantity | Suggested precision |
|----------|--------------------:|
| Energy (MWh) | 3 |
| Power (MW) | 2-3 |
| Currency | 2 |
| Percentage | 1-2 |
| Record count | 0 |
| Ratio | domain-specific |

Never change precision silently to make a value fit.

### Never monospace for measured values

Monospace gives every character equal width: the column widens needlessly and the digits thin out, slowing the scan. A proportional sans with tabular figures delivers monospace's only benefit without its cost. This applies to currency, consumption, production, percentages, quantities, totals, rates and metric cards.

## 7 · Technical identifiers

Monospace belongs to values read **character by character** and dictated aloud:

| Monospace | Not monospace |
|-----------|---------------|
| UUID, GUID | Amounts, quantities, percentages |
| Registry / account / SKU codes | Dates, times, period labels (`2026-07`) |
| Serial numbers, device IDs | Person and place names |
| Endpoints, URL paths, file paths | Status labels |
| Hashes, commit SHAs | Page and record counts |
| Log lines, stack traces | Sort and filter values |

```css
:root { --font-mono: ui-monospace, "SFMono-Regular", "Cascadia Mono", Consolas, "Liberation Mono", monospace; }
.technical-identifier {
  font-family: var(--font-mono);
  font-variant-numeric: tabular-nums lining-nums;
  letter-spacing: 0;
  text-align: left;
}
```

Identifiers are not measured numbers: keep them **left-aligned**, apply no numeric or currency formatting, preserve exact casing and leading zeroes, keep them copyable, and expose the full value if truncated.

### When "no mono in tables" and "mono for identifiers" collide

A serial number lives in a table column. The contradiction is apparent, not real:

- The no-mono rule governs **measured numbers** — compared, summed, averaged
- The mono rule governs **identifiers** — not compared, but dictated and copied

The decision looks at **what the cell carries**, not where it sits. The amount column is sans plus tabular; the serial column is monospace. Both in one table is correct — an identity column *should* look different, because its job is different.

## 8 · Hierarchy

Enterprise interfaces rarely need large headings.

```text
20px / 600    page title
16px / 600    major section
14px / 500    subsection or panel heading
12px / 500    compact label or table header
13-14px / 400 content and data
24-32px / 600 primary KPI only
```

Build hierarchy in this order: **position → spacing → grouping → weight → size → colour.** Colour is the last tool, never the first.

```css
.page-title    { font-size: var(--text-title);   line-height: var(--leading-tight); font-weight: var(--weight-strong); letter-spacing: -0.02em; }
.section-title { font-size: var(--text-section); line-height: 1.35;                 font-weight: var(--weight-strong); }
.compact-label { font-size: var(--text-caption); line-height: var(--leading-label); font-weight: var(--weight-label); }
```

Do not make every card title large. Do not bold every first column.

## 9 · Letter spacing

| Where | Tracking |
|-------|----------|
| Page title | `-0.02em` |
| Metric value | `-0.025em` |
| Uppercase table header | `+0.02em` |
| Body, data, help text | normal |
| Technical identifier | `0` |

Negative tracking suits large titles and metrics only. Avoid aggressive negative tracking on small text, wide tracking on body text, and tracking used to imitate a trend.

## 10 · Uppercase

Uppercase works for short, compact headers and labels — and carries two specific risks.

**Unit symbols break.** `kWh` → `KWH` is wrong: `k` is kilo, `W` watt, `h` hour; `MB` and `Mb` differ by a factor of eight. Isolate the unit:

```html
<th><span class="header-label">CONSUMPTION</span> <span class="unit">(MWh)</span></th>
```
```css
.header-label { text-transform: uppercase; }
.unit { text-transform: none; letter-spacing: 0; }
```

**Locale casing breaks without `lang`.** CSS applies locale rules only when the language is declared. Without it Turkish `i` uppercases to `I` instead of `İ` (`Tip` → `TIP`, `İtirazlı` → `ITIRAZLI`). `<html lang="tr">` is a condition for producing the right letters, not merely an accessibility setting.

Never uppercase long sentences, help text, form descriptions or error messages.

## 11 · Line height and line length

| Content | Line height |
|---------|------------:|
| Dense table cell | 1.30-1.35 |
| Compact UI content | 1.35-1.45 |
| Form help text | 1.45-1.55 |
| Long reading text | 1.55-1.70 |
| Large KPI | 1.0-1.15 |
| Page title | 1.15-1.25 |

One global line height for every role is wrong in both directions: dense data needs rhythm, explanatory text needs room.

```css
.reading-text { max-inline-size: 65ch; }
```

Help text 35-60 characters, form descriptions 40-70, long reading content 45-75. Do not stretch prose across a desktop dashboard. Tables and numeric values are not governed by prose measure.

## 12 · Colour and contrast

Text colour is tokenised (`--ink-strong`, `--ink-body`, `--ink-muted`, `--ink-disabled`, `--ink-inverse`, plus status inks).

- Body text ≥ **4.5:1**; the 3:1 threshold applies only to text that genuinely qualifies as large
- **Muted text must still pass** — "muted" is not permission to fail contrast
- Do not build hierarchy out of low contrast alone
- Do not apply opacity to a whole data region, and never stack opacity on already-muted text (`filters.md`: staleness is announced, not dimmed)
- Status meaning never depends on hue alone

To reduce emphasis: switch to a muted **ink** token and keep the weight and letterform. Never substitute weight 300 for muted colour.

## 13 · Never below 400

At 13px, thin text turns grey on light backgrounds and falls apart under greyscale font smoothing; in dark theme the opposite happens — thin letterforms bloom and their edges smear.

## 14 · Dark theme

Dark theme typography needs its own visual check. Common failures:

- Thin text blooms and goes fuzzy
- Muted text loses contrast
- Small labels disappear
- Coloured status text becomes too bright
- Disabled and readonly become indistinguishable (`forms.md`)
- Zebra difference collapses (`tables.md`)

Rules: never assume light-theme ratios transfer; verify every ink token against every dark surface token; avoid weights below 400; check Windows rendering, not only macOS; check browser zoom at 100 / 125 / 150%.

## 15 · Responsive typography

Do not solve responsive layout by shrinking all text. Order: **change layout → change wrapping → fold or hide secondary content → cut decorative space → adjust density tokens → only then touch type size.**

```css
.page-title   { font-size: clamp(1.125rem, 2vw, 1.25rem); }
.metric-value { font-size: clamp(1.5rem, 4vw, 2rem); }
```

**Do not `clamp()` dense table body text.** A data cell should stay stable across breakpoints; the layout adapts around it, not the other way round.

## 16 · Localisation

Test with real locale content, not Lorem Ipsum.

- Declare the root `lang`
- Do not uppercase locale-sensitive content in JavaScript without locale support — `label.toLocaleUpperCase("tr-TR")`; prefer CSS casing with a correct `lang`
- Preserve unit casing
- Verify Turkish glyphs render: `i→İ  ı→I  ş→Ş  ğ→Ğ  ü→Ü  ö→Ö  ç→Ç`
- Verify long translated labels, number separators, decimals and date formats
- Never assume English label length; translated UI commonly expands 20-35%

## 17 · Per-surface requirements

**Tables** (`tables.md`) — 13-14px body by density, 12-13px headers; tabular lining figures for measured values; numeric headers and values right-aligned; text and identifiers left; one strong emphasis step and at most one or two decision columns; never truncate a header; keep the full value reachable when a cell truncates; preserve unit casing; verify sticky columns **while scrolled**.

```css
.data-grid    { font-family: var(--font-ui); font-size: var(--surface-text-size);
                line-height: var(--surface-line-height); font-weight: var(--weight-body); }
.data-grid th { font-size: var(--surface-label-size); line-height: var(--leading-label);
                font-weight: var(--weight-label); }
.data-grid .is-decision { font-weight: var(--weight-strong); }
.data-grid .is-numeric  { text-align: right; font-variant-numeric: tabular-nums lining-nums; }
```

**Forms** (`forms.md`) — labels above fields, never replaced by placeholders; help text visually secondary but still passing contrast, never below 12px; error text says how to fix; readonly keeps normal readability and stays distinguishable from disabled; field width communicates expected length; numeric inputs use tabular figures and right alignment where appropriate; required/optional stated consistently.

**Filters** (`filters.md`) — search and filter look like different tasks; applied filter values stay readable and **chips are never truncated**; result counts use tabular figures; default filters visible; pending state is not shown by lowering text opacity.

**Dashboards** (`dashboards.md`) — every metric carries label, value, comparison and interpretation. A large number without unit, comparison period, status meaning and freshness is not information.

```css
.metric-label   { font-size: var(--text-data); line-height: 1.3; font-weight: var(--weight-label); }
.metric-value   { font-size: clamp(var(--text-metric-sm), 3vw, var(--text-metric-lg));
                  line-height: 1; font-weight: var(--weight-strong); letter-spacing: -0.025em;
                  font-variant-numeric: tabular-nums lining-nums; }
.metric-context { font-size: var(--text-caption); line-height: var(--leading-body); }
```

## 18 · Minimalism is not shrinking the text

If a screen looks cluttered, reducing font size is the wrong fix: it converts clutter into illegibility, changes the measure, flattens hierarchy and damages accessibility.

Reduce in this order, stopping as soon as it reads:

1. **Colour** — remove every non-semantic hue
2. **Separators** — zebra *or* rules, never both; no box inside a box
3. **Emphasis** — if everything is emphasised, nothing is
4. **Content** — anything answering no question (`design-quality.md`)
5. **Space** — keep group spacing, cut decorative space

Only then consider a density level, which is a *token* decision that brings row height with it.

## 19 · Performance

WOFF2, one variable file, only the weight range in use. Preload only a font used immediately above the fold, and only one:

```html
<link rel="preload" href="/fonts/InterVariable.woff2" as="font" type="font/woff2" crossorigin>
```

Avoid loading multiple UI families; skip a mono webfont when the system mono stack suffices; use `font-display: swap` and measure the resulting layout shift. Do not drop required Turkish glyph coverage to save bytes.

## Anti-patterns

Do not: use more than one primary UI sans family · use monospace for all numbers · use thin weights in dense interfaces · go below 12px for functional text or 13px for dense body text · use more than three weights · exceed five functional sizes without justification · create component-local type scales · apply arbitrary letter spacing · uppercase long text · uppercase unit symbols · truncate table headers · hide context to look minimal · use low opacity for loading or stale data · render missing values as zero · use colour as the only status cue · bold every label · show huge dashboard numbers without context · use placeholder text as a label · add a font without checking the existing system · claim a font is used without verifying it loaded.

## Typography decision record

```text
Existing typography system: none
Typeface decision:          Inter Variable
Font delivery:              self-hosted WOFF2
Density:                    dense
Primary text size:          13px / 1.35 / 400
Label size:                 12px / 1.3 / 500
Page title size:            20px / 1.2 / 600
Weight scale:               400 / 500 / 600
Numeric figure settings:    tabular-nums + lining-nums + right alignment
Monospace usage:            registry codes and serial numbers only
Locale:                     tr-TR
Dark-theme verification:    passed visually and by contrast audit
Known limitations:          Windows ClearType not tested on physical field devices
```

## Verification

**Font loading**
- [ ] The intended family appears in computed styles; the font request succeeded
- [ ] No unexpected Arial or generic fallback rendered
- [ ] Variable weight range respected; swap causes no unacceptable layout shift

**Hierarchy**
- [ ] Page title visible without dominating the data; sections distinguishable from body
- [ ] Labels distinguishable without excessive uppercase or colour
- [ ] Only one strong emphasis level; no unnecessary type sizes

**Numbers**
- [ ] Tabular lining figures; columns and their headers right-aligned on one axis
- [ ] Decimal precision and units consistent down each column
- [ ] Negative values visible without breaking alignment
- [ ] Missing values are not zero; totals align with body values

**Identifiers**
- [ ] Monospace only on technical identifiers, left-aligned
- [ ] Exact casing and leading zeroes preserved; truncated values recoverable

**Accessibility**
- [ ] Body ≥ 4.5:1, muted text still passing; no functional text below 12px, no dense body below 13px
- [ ] Readable at 200% zoom; focus indicators visible; colour is not the only status cue
- [ ] Locale-specific characters render correctly

**Responsive and theme**
- [ ] Stable at 320px; layout changes before text shrinks; metrics do not overflow tiles
- [ ] Long translated labels do not break the page; headers stay readable; prose measure bounded
- [ ] Light and dark both checked; disabled vs readonly still distinguishable; muted ink still readable in dark

## Blocking gates

- [ ] Existing typography system inspected
- [ ] Typeface choice justified and **font delivery verified**
- [ ] Body contrast meets the threshold; functional text ≥ 12px; dense data text ≥ 13px
- [ ] Measured numbers use tabular lining figures; values **and headers** right-aligned
- [ ] Monospace limited to technical identifiers
- [ ] No weight below 400; weight scale limited to 400 / 500 / 600 unless justified
- [ ] Unit casing correct; root language declared
- [ ] Missing data not rendered as zero
- [ ] Dark theme keeps text above contrast thresholds
- [ ] Usable at 320px and 200% zoom

## Default baseline

When no product typography exists:

```css
@font-face {
  font-family: "Inter Variable";
  src: url("/fonts/InterVariable.woff2") format("woff2");
  font-style: normal; font-weight: 400 600; font-display: swap;
}

:root {
  --font-ui: "Inter Variable", "Inter var", Inter,
             ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --font-mono: ui-monospace, "SFMono-Regular", "Cascadia Mono", Consolas, "Liberation Mono", monospace;

  --text-caption: 0.75rem;  --text-data: 0.8125rem;  --text-body: 0.875rem;
  --text-section: 1rem;     --text-title: 1.25rem;
  --text-metric-sm: 1.5rem; --text-metric-lg: 2rem;

  --leading-tight: 1.2;  --leading-label: 1.3;  --leading-data: 1.35;
  --leading-body: 1.45;  --leading-reading: 1.6;

  --weight-body: 400;  --weight-label: 500;  --weight-strong: 600;
}

body { font-family: var(--font-ui); font-size: var(--text-body);
       line-height: var(--leading-body); font-weight: var(--weight-body); }

.numeric              { text-align: right; font-variant-numeric: tabular-nums lining-nums; }
.technical-identifier { font-family: var(--font-mono); text-align: left; letter-spacing: 0; }
.page-title    { font-size: var(--text-title);   line-height: var(--leading-tight); font-weight: var(--weight-strong); letter-spacing: -0.02em; }
.section-title { font-size: var(--text-section); line-height: 1.35;                 font-weight: var(--weight-strong); }
.compact-label { font-size: var(--text-caption); line-height: var(--leading-label); font-weight: var(--weight-label); }
.metric-value  { font-size: clamp(var(--text-metric-sm), 3vw, var(--text-metric-lg));
                 line-height: 1; font-weight: var(--weight-strong); letter-spacing: -0.025em;
                 font-variant-numeric: tabular-nums lining-nums; }
```

---

> Carbon's role discipline, Primer's restraint, Linear's calm hierarchy, Inter's numeric clarity. The goal is not impressive typography — it is letting the user read, compare, decide and act with less effort.
