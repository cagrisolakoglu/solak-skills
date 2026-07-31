# Numbers, Dates and Units

In a data-dense screen, formatting is not cosmetic: a badly formatted number is **misread**, and a misread number produces a wrong decision. Alignment rules are in `tables.md`, field width in `forms.md`, figure sets and monospace scope in `typography.md`.

## The product decides the locale; code does not invent it

Separators are not universal. The same value in three locales:

| Locale | Grouping | Decimal | Example |
|--------|----------|---------|---------|
| `en-US` | `,` | `.` | `1,284,690.75` |
| `de-DE`, `tr-TR`, `es-ES` | `.` | `,` | `1.284.690,75` |
| `fr-FR` | narrow space | `,` | `1 284 690,75` |
| `en-IN` | lakh/crore grouping | `.` | `12,84,690.75` |

Building the format by hand (regex, `replace`, string concatenation) rounds in the wrong place and mangles negatives. **Use `Intl`:**

```js
const num   = new Intl.NumberFormat(locale, { maximumFractionDigits: 0 });
const money = new Intl.NumberFormat(locale, { style: 'currency', currency: 'EUR' });
const pct   = new Intl.NumberFormat(locale, { style: 'percent', maximumFractionDigits: 1 });

num.format(1284690);    // en-US "1,284,690"   · de-DE "1.284.690"
money.format(1284690);  // en-US "€1,284,690.00" · de-DE "1.284.690,00 €"
pct.format(0.124);      // en-US "12.4%"       · tr-TR "%12,4"
```

Note what `Intl` handles that hand-rolling does not: currency symbol **position** and percent sign position both move with the locale.

Do not trust the browser language: the locale comes from the product setting (or the user's preference), not from `navigator.language`. Otherwise the same data looks like two different numbers on two machines.

On the input side, **do not impose the format on the user.** Validation accepts `1284690`, `1,284,690` and `1.284.690`, and normalises before saving. Forcing users to type separators slows data entry down.

## An identifier is not a number

Serial numbers, invoice numbers, registry codes, SKUs, account numbers, period labels (`2026-07`), tax IDs — these are made of digits but are **not measurements**: they are not summed, compared, or averaged.

| | Measured number | Identifier |
|--|-----------------|------------|
| Alignment | **Right** | **Left** (like text) |
| Grouping separator | Yes | **No** — `4471 0982 331` keeps its own blocking |
| Font | Sans + tabular figures; **never monospace** | Monospace for technical identifiers (`typography.md`) |
| Rounding | Possible | Never |

```css
.num        { font-variant-numeric: tabular-nums lining-nums; text-align: right; }
/* technical identifier: UUID, registry code, serial, endpoint, hash */
.ident-tech { font-family: var(--font-mono); font-variant-numeric: tabular-nums lining-nums; text-align: left; }
/* human-facing identifier: period, date-like codes — not monospace */
.ident      { font-variant-numeric: tabular-nums lining-nums; text-align: left; letter-spacing: 0.02em; }
```

`lining-nums` cannot be skipped: some families default to oldstyle figures (descending `3`, `4`, `7`, `9`), which `tabular-nums` does not correct — the column aligns but the line jitters. Detail in `typography.md`.

Right-aligning an identifier makes it look like a summable quantity and wastes the eye's work down the column.

## Precision is constant down a column

The number of decimal places in a column **does not vary.** If `13,240` and `13,240.75` appear in the same column, the digits do not line up and comparison is over.

```
✅ 13,240.00   ❌ 13,240
    9,180.50        9,180.5
      412.25          412.25
```

Precision follows the **kind of quantity**, not the current state of the data:

| Quantity | Places | Why |
|----------|--------|-----|
| Counts, records, units | 0 | Integers by nature |
| Derived quantity | 0 or 2 | Computed; decide once and hold it |
| Rates, ratios | 2-3 | Small differences are meaningful |
| Unit price | 2 | Market convention |
| Money total | 2 | Minor units |
| Percentage | 1 | More is noise |

## The unit label belongs in the header, not the cell

The unit is written once, in the column header or field label: `Previous balance (GB)`. Repeating it in every cell (`184,320 GB`) drowns the number and breaks right alignment — the eye starts tracking letter edges instead of digits.

For a single value (a KPI tile, a derived block) the unit sits next to the value but **smaller and quieter**; the number stays dominant.

**One unit per column.** Mixing GB with TB, or cents with dollars, in one column produces thousand-fold errors. If the unit varies per record, either convert everything to one unit or move the unit to its own column and say so in the header.

### Unit symbols are case-sensitive

`kWh` is not `KWH`, `MB` is not `Mb`, `mA` is not `MA`. In `kWh` the `k` is kilo, `W` is watt, `h` is hour; in `Mb` versus `MB` the difference is a factor of eight. This matters most where `text-transform: uppercase` is applied to headers — see `tables.md`.

## Dates and times

- Use a locale-aware format via `Intl.DateTimeFormat`; do not hand-assemble `DD.MM.YYYY` or `MM/DD/YYYY`
- Show the expected mask in the input placeholder, matching the locale
- Time: match the locale's convention (24-hour or 12-hour); do not mix both in one screen
- Period labels like `2026-07` are **identifiers**, not dates: left-aligned, never localised
- APIs and URLs: ISO 8601 (`2026-07-31T14:32:00+03:00`). Localisation happens at display time only
- **One format per table.** `31.07.2026` and `2026-07-31` never appear in the same column

```js
const dt = new Intl.DateTimeFormat(locale, { dateStyle: 'short', timeStyle: 'short' });
```

### Time zones and hourly series

Where data is timestamped, the time zone is not a display preference but a **correctness** matter:

- Store and transmit an instant (UTC or an offset-bearing ISO string); localise only at display
- In regions observing daylight saving, **a day is not always 24 hours** — there are 23-hour and 25-hour days. Any hourly series, bucket chart or day-over-day comparison that assumes 24 buckets will be silently wrong twice a year
- For an hourly series, say which end is inclusive: is it `14:00-15:00`, or does the label `14:00` mean the whole hour? Ambiguity here costs exactly one hour of shift
- Show the zone when the audience spans zones; "09:12" alone is not a time

## Missing data is not zero

Three distinct situations, three presentations:

| Situation | Display | Meaning |
|-----------|---------|---------|
| Measured, value is zero | `0` | Nothing happened |
| Not yet measured | `—` | Data pending |
| Could not be measured | `—` + reason | Failure, no access |

A `—` cell does not enter arithmetic: those rows are **excluded** from totals and averages, and the exclusion is stated ("3 records could not be read, not included in the average"). An average computed by treating absence as zero is a wrong decision nobody notices.

## Negative values and signs

- Use a minus sign (`-1,240`); accounting parentheses (`(1,240)`) do not read in product UI
- The sign is the **primary** indicator, not colour; colour is the second channel
- Direction and good/bad are different things: revenue falling is "bad", returns falling is "good". State what was expected in the context line
- A negative value in a quantity that cannot go below zero is a **data error signal**, not a formatting problem — never silently render it as `0` (see the anomaly rule in `tables.md`)

## Rounding: the sum of displayed values vs the displayed sum

If rows are rounded for display, the number the user adds up will **not match** the total row.

```
1,240.4 → 1,240        Total from raw values: 3,720.9 → 3,721
1,240.3 → 1,240        Sum of displayed:      3,720
1,240.2 → 1,240        Difference: 1
```

Rule: **always compute totals from raw values and round last.** If a discrepancy remains and users add up by hand (invoices, statements, reconciliations), add a footnote: "Rows are rounded to whole units; the total is computed from unrounded values." A silent one-unit difference costs trust.

## Abbreviate only on dashboards

Abbreviations like `1.2M` are **banned** in an operational table — that is where users compare exact values. They are acceptable in a KPI tile, provided:

- Unit and magnitude are explicit (`1.2M GB`, `€1.2M`)
- The exact value stays reachable (tooltip, detail screen)
- Abbreviation is consistent within a column; one row does not read `980K` while the next reads `1.2M` — the column picks the scale

## Verification

- [ ] Numbers formatted through `Intl`, no hand-built strings
- [ ] Locale comes from the product setting, not `navigator.language`; grouping, decimal, currency and percent positions correct
- [ ] Identifiers left-aligned, no grouping separators, never rounded
- [ ] Decimal places constant down each column
- [ ] Unit in the header once; one unit per column; unit symbol casing preserved
- [ ] One date format per surface; period labels treated as identifiers
- [ ] Hourly series do not assume 24-hour days where DST applies; interval boundaries stated
- [ ] Missing data shown as `—`, distinguishable from zero, excluded from arithmetic
- [ ] Totals computed from raw values; any rounding difference declared
- [ ] No abbreviated numbers in operational tables
