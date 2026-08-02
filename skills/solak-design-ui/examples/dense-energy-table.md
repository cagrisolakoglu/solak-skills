# Dense operational table

A worked example of a `component-refinement` on a table that operators scan several times a day. Shows the shape of a complete output, not a component to copy.

## Surface contract

- **Surface:** account usage table, settlement review screen
- **Primary user:** operations specialist, daily
- **Primary task:** find the usage records that look wrong and start investigating them
- **Success condition:** every anomalous record in the period is dismissed or assigned
- **Main decision:** is this record trustworthy enough to settle
- **Data volume:** 400 typical, 4,000 worst case
- **Data freshness:** meter reads land hourly; a run can be up to 60 minutes behind
- **Costly mistake:** settling on an unreadable meter — money moves and reversing it is a manual process
- **Primary device and input:** desktop, keyboard-heavy; occasional tablet review
- **Supported minimum width:** 320px
- **Existing tokens:** product token layer present; extended, not replaced
- **Existing typography:** product system; no new typeface
- **Loading behaviour:** real header, skeleton rows at real row height
- **Empty behaviour:** first-use and filtered no-results are separate components
- **Error behaviour:** scoped to the table; existing rows survive a failed refresh
- **Responsive strategy:** fold to cards below the measured identity-block width
- **Accessibility risks:** sticky identity column, anomaly markers carried by colour
- **Out of scope:** the filter panel above it, the page shell, the export flow

## Information priority

| Item | Class | Justification |
|------|-------|---------------|
| Account name | Identity | How the operator refers to the record out loud |
| Account ID | Identity, secondary | Needed when names collide; monospace, read character by character |
| Deviation vs trailing average | **Decision** | The one number that says "look at this" |
| Current reading | Decision | The value being trusted |
| Status | Decision | Approved / pending / disputed / unreadable |
| Previous reading | Detail | Only consulted once a record is suspect |
| Rate | Detail | Rarely changes; matters only in disputes |
| Last reading date | Detail | Staleness check during investigation |
| Tariff class | **Removed** | Supported no decision on this screen; lives in the record detail |

Deviation was a detail column three positions from the right. Promoting it to the decision block next to identity is the single change that did the most, because it is the column the task is actually about.

## Wireframe

```text
┌────────────────────────────────────────────────────────────┐
│ Period 2026-07 · 412 records            [Export] [Columns] │
├────────────────────────────────────────────────────────────┤
│ ⚠ 7 records unreadable · excluded from the total           │
├──────────────┬───────────┬──────────┬───────────┬──────────┤
│ ACCOUNT      │ DEVIATION │  CURRENT │ STATUS    │  ⋯detail │
│ (sticky)     │  (right)  │  (right) │           │          │
├──────────────┼───────────┼──────────┼───────────┼──────────┤
│ …400 rows, 28px, one separator system                      │
├────────────────────────────────────────────────────────────┤
│ Total · 405 of 412        3,102,800  (7 excluded)          │
└────────────────────────────────────────────────────────────┘
```

## Responsive

The identity block measured 52% of a 320px viewport. Horizontal scroll would leave 48% for eight columns, so rows fold to cards below 560px — the width at which the deviation column stopped fitting beside identity, not a device size.

The table lives beside a collapsible sidebar, so the fold is a **container** query: at a 1024px viewport the table has 756px with the sidebar open and 988px without, and a viewport query cannot tell those apart.

## States

| State | Behaviour |
|-------|-----------|
| Initial loading | Real header row, skeleton rows at 28px, no shift on arrival |
| Refresh | Rows stay readable at full contrast; banner names the last-updated time |
| First use | Explains the surface, offers the provisioning action |
| No results | Names the restrictive filter, offers two exits |
| Partial | 405 of 412 loaded; the 7 are named and excluded from the total |
| Error | Scoped to the table; retry is labelled "Retry meter data" |
| Row error | Row-level, the other 411 rows remain usable |

## Density and type

Dense, 28px rows: 400+ records, scanning task, desktop primary. Measured values take tabular lining figures and right alignment with headers on the same axis; the account ID is the only monospace column, because it is dictated character by character. One separator system — hairline rules, no zebra.

## TODO summary

14 items, dependency-ordered: semantics → column order → alignment and figures → sticky identity → states → responsive fold → tokens → accessibility. Executed one at a time, each validated before the next.

## Rejected alternative

**Virtualised infinite scroll instead of pagination.** It handles 4,000 rows more gracefully and it was rejected: the operator's task ends with "every anomaly in the period is resolved", and an infinite list gives no answer to *am I done*. Pagination with a visible total makes completion legible. If the worst case grows past ~10,000 the trade changes and this should be revisited.

## Validation

- ✅ Contrast 7.1:1 including status colours · ✅ keyboard completable, `focus-visible` present
- ✅ Tabular lining figures, headers on the same axis · ✅ constant precision down each column
- ✅ Missing values as `—`, excluded from the total · ✅ four states verified by screenshot
- ✅ 320px fold verified by measurement, not declaration · ✅ both themes
- ⚠️ `prefers-reduced-motion` added, not tried on a physical device

## Remaining risks

- Virtualisation untested above ~2,000 rows; the 4,000-row worst case is theoretical
- No observation of a real operator; the priority order is reasoned, not watched
- The anomaly marker's second cue is a glyph, which pushed digit alignment once before — worth re-checking whenever the marker changes
