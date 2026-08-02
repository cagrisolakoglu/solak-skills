# Unreadable dense table

Canonical references: `tables.md` for column behaviour, `typography.md` for figures and sizes, `formatting.md` for precision and units.

## Bad implementation

Density achieved by shrinking everything and emphasising everything.

```css
.grid td      { font-size: 11px; line-height: 1.1; }
.grid .amount { font-family: ui-monospace, monospace; text-align: left; }
.grid .key    { font-weight: 700; }
.grid .name   { font-weight: 700; }
.grid .status { font-weight: 700; }
```

```text
Account          ID            Prev       Curr    Rate   Usage      Amount
Acme Industrial  4471773481    2910004    0       80     0          0.00
Baltic Freight   4471221044    614220     619005  40     191400     7656.0
Helsinki Marine  4471005519    1004880    1001240 40     -145600    -5824
```

## Why it fails

- **11px is below the functional floor.** Not a preference: at 11px on a 1.1 line height, digit shapes stop being reliably distinguishable at a glance, which is the only thing this table is for.
- **Monospace on measured values inflates the column and thins the digits.** Monospace exists for values read character by character — serials, hashes, IDs. A money column is read as a magnitude, and the eye compares magnitudes by shape and edge, both of which monospace flattens.
- **Left-aligned numbers destroy comparison.** `7656.0` and `-5824` under `0.00` share no edge, so the reader has to parse each value instead of scanning the column. This is the single most damaging defect in the list.
- **Inconsistent precision.** `0.00`, `7656.0`, `-5824` — three precisions in one column means the decimal point moves, and the alignment that right-alignment would have bought is lost anyway.
- **Everything bold is nothing bold.** With three columns at weight 700, the eye has no entry point and defaults to reading left to right, which is the slowest possible path through a table.
- **Missing rendered as zero.** Acme's meter was unreadable. The table shows `0` usage and `0.00` amount, which is not a smaller number — it is a **wrong** one, and it propagates into the total where nobody can see it happened.
- **Proportional figures** make `111` narrower than `999`, so columns of digits do not line up even when right-aligned.

## Correct direction

```css
.grid td          { font-size: 13px; }                       /* dense floor for body text */
.grid .is-num     { text-align: right; font-variant-numeric: tabular-nums lining-nums; }
.grid th.is-num   { text-align: right; }                     /* header on the same axis */
.grid .is-tech    { font-family: var(--font-mono); }         /* identifiers only */
.grid .is-key     { font-weight: var(--weight-strong); }     /* one emphasised column */
.grid .is-detail  { color: var(--ink-muted); }               /* de-emphasise with ink, not weight */
```

```text
Account          ID              Prev       Curr   Rate     Usage       Amount
Acme Industrial  4471 7734 810   2,910,004     —     80          —            —   ⚠ unreadable
Baltic Freight   4471 2210 447     614,220  619,005  40    191,400    7,656.00
Helsinki Marine  4471 0055 190   1,004,880 1,001,240 40   -145,600   -5,824.00

Total · 2 of 3 accounts                                       45,800   1,832.00
                                              1 unreadable account excluded
```

Density comes from **row height and padding**, which cost nothing to read, not from type size, which costs everything. De-emphasis is done with ink, not by removing weight below 400.

Give the alignment class enough specificity to beat the component's own `th, td` rule — otherwise the class sits in the markup while the base rule silently wins, and the column looks unstyled for no visible reason.

## Detection checklist

- [ ] Any functional text below 12px, or dense body text below 13px?
- [ ] Is any measured number in a monospace family?
- [ ] Is any measured column left- or centre-aligned?
- [ ] Does a numeric header sit on a different edge from its column?
- [ ] Is `font-variant-numeric: tabular-nums lining-nums` actually **computed** on the cells, not merely declared in a class?
- [ ] Does the decimal count vary down any single column?
- [ ] Count the bold columns. More than one and the emphasis has cancelled out.
- [ ] Is any missing value shown as `0`, `0.00`, or an empty cell rather than `—`?
- [ ] Does the total say what it excludes?
- [ ] Are both zebra striping and horizontal rules present?
