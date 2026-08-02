# Long data-entry form

A worked example of a `component-refinement` on a 24-field record form that people fill in repeatedly.

## Surface contract

- **Surface:** usage record entry and correction
- **Primary user:** field technician on tablet; back-office clerk on desktop
- **Primary task:** enter one period's readings for one account and save them correctly
- **Success condition:** the record saves and the computed amount matches the technician's expectation
- **Main decision:** does this reading look right before committing it
- **Data volume:** 24 fields, 5 groups; 30-60 records per session
- **Data freshness:** not applicable; this is an entry surface
- **Costly mistake:** a mistyped reading becomes an invoice, and correcting it is a manual reversal
- **Primary device and input:** tablet in the field, desktop in the office; keyboard-heavy on desktop
- **Supported minimum width:** 320px
- **Loading behaviour:** field skeletons at real field height, labels never skeletonised
- **Empty behaviour:** defaults visible, never hidden
- **Error behaviour:** field-level, with input preserved
- **Responsive strategy:** two columns collapse to one at the measured width
- **Accessibility risks:** grouped radios, error association, focus order across a two-column grid
- **Out of scope:** the list screen, the approval workflow

## Grouping and order

Five `fieldset`s in the order the technician works, which is not the order the table stores:

```text
1  Identify the account      account, meter serial, period
2  Read the meter            previous, current, reading date, reader
3  Classify                  tariff, status, anomaly flag
4  Explain                   note, attachment
5  Confirm                   computed amount (read-only), save
```

The stored schema puts tariff second because it is a foreign key. Following the schema made technicians jump back and forth between the meter in front of them and a dropdown about billing. Field order follows the **hand**, not the table.

## Column decisions

Two columns only where fields are genuinely paired — previous/current reading, date/reader. Everything else is one column. A two-column form is not twice as fast to fill; it is twice as easy to lose your place in, and the tab order across a grid confuses more people than the vertical space saves.

Every field starts on a shared grid line. Field **width signals expected content**: the meter serial is 14ch, the reading is 10ch, the note is full width. A full-width input for a two-digit number tells the user the wrong thing before they type.

## Validation

On blur and on submit. Never on keystroke — a message that appears while someone is still typing their third character is noise, and they learn to ignore the region it appears in.

```text
Current reading
[ 1,284,6O0        ]  ⚠ Contains a letter: "O" at position 8. Meter readings are digits only.
```

The message says what is wrong and where. **Input is preserved** — clearing the field after a validation failure is the single most expensive thing this surface can do, because the technician no longer has the meter in front of them.

A summary appears above the actions only when submit fails, and each entry links to its field with the same wording used there. Two phrasings of one error make the user look for two problems.

## Server errors

Rendered in the same place and style as client validation, so the user does not have to learn a second error language. A partial save states exactly which fields landed:

```text
⚠ 2 of 6 fields were not saved
  Current balance and rate were rejected by the billing service. Your entries are unchanged.
```

## Unsaved state and save

Explicit save, because a reading is a committed value and auto-saving a half-entered meter read creates records nobody meant to create. Unsaved changes are visible after the first edit, with save and discard, and leaving the page is guarded. The warning clears the instant a save succeeds.

Saved confirmation is **persistent** — "Saved · 14:32" near the form title. A vanishing toast is not proof of a record that turns into money.

## Action hierarchy

```text
                                    [Save record]  [Cancel]

  Delete this record                                       (separated, quiet)
```

Save is primary, cancel is quiet, delete is separated from both and states its scope when confirming — "Delete reading for AC-4471, period 2026-07?", never "Are you sure?". In a confirmation dialog the weight flips: the destructive action is what the dialog is about, so it carries the emphasis and Cancel becomes the quiet one.

## Mobile

Single column below 40rem — the width at which the paired reading fields stopped fitting side by side at their content-signalling widths. Groups stay expanded; collapsing them to save scroll hides the structure that makes a 24-field form navigable, and the technician then cannot see how much is left.

The action bar does not stick to the bottom on mobile: it collides with the software keyboard on the exact fields where it matters.

## Rejected alternative

**A stepper wizard, one group per step.** It looks calmer and was rejected: technicians correct earlier readings after seeing the computed amount, and a wizard makes going backwards feel like undoing progress. The form is long, but it is a form, and the whole record needs to be visible at once for the check the user actually performs.

## Validation

- ✅ Fields share grid lines · ✅ widths signal content · ✅ blur + submit validation
- ✅ Input survives failure · ✅ server and client errors share one presentation
- ✅ `readonly` and `disabled` distinguishable in **both** themes
- ✅ Keyboard completable, focus order matches visual order
- ✅ Persistent save confirmation · ✅ unsaved guard clears on success
- ⚠️ Not tested on a physical tablet with a software keyboard; the sticky-bar decision is reasoned from the constraint, not observed

## Remaining risks

- No conflict handling: two clerks editing the same record will last-write-wins. Out of scope for this pass and the most likely next defect
- The 40rem collapse point was measured with English labels; a longer localisation will move it
